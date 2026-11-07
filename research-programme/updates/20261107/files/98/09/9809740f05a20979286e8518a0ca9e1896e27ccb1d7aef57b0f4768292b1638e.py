from derive_annular_source_gravity_20260914 import EvidenceRun
from derive_annular_support_map_constraints_20260927 import restore_case
from annular_nested_physical_refinement_v3_20260922 import restore_refined
from annular_source_flat_native_20261002 import flat_basis,movements,shape_forms,trial_norm,divided_image
from annular_physical_native_kernel_20260928 import NativeKernel,decimals,maximum
from annular_native_trial_matrix_20261001 import transport,image_and_tangent
from derive_annular_native_shape_stress_20260928 import physical_data,nodal_transport
from search_annular_nonzero_shape_constraint_v3_20261001 import reduced_search
from analyze_annular_native_shape_state_20261001 import separator
from probe_annular_Neumann_kernel_family_20261001 import nodal_radii
from annular_native_source_hinge_20261002 import source_hinge_image
from decimal import Decimal,localcontext
from time import perf_counter
import argparse
import ctypes
import hashlib
import json
import numpy as np


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--level',choices=['fine','third'],required=True)
    parser.add_argument('--cpu',type=int,choices=[2,4],required=True)
    args = parser.parse_args()
    kernel = ctypes.windll.kernel32
    kernel.GetCurrentProcess.restype = ctypes.c_void_p
    kernel.SetProcessAffinityMask.argtypes = [ctypes.c_void_p,ctypes.c_size_t]
    if not kernel.SetProcessAffinityMask(kernel.GetCurrentProcess(),1<<args.cpu):
        raise OSError('Affinity failed')
    evidence = EvidenceRun('annular-source-flat-native-search-'+args.level+'-attempt01',__file__)
    started,deadline = perf_counter(),perf_counter()+7200
    try:
        evidence.own(evidence.root/'DERIVATION-20261002-source-flat-native-compatible-initial-data.md')
        parent_path = evidence.output.parent/'annular-null-coupled-acceleration-integrity-20261001.json'
        evidence.own(parent_path)
        parent = json.loads(parent_path.read_text())
        digests = dict(parent['hashes'])
        construction_path = evidence.output.parent/('annular-source-flat-native-state-'+args.level+'-attempt02/status.json')
        construction = json.loads(construction_path.read_text())
        evidence.own(construction_path)
        evidence.check('construction_complete',construction['state']=='complete' and all(row['passed'] for row in construction['checks']))
        for category in ['inputs','outputs']:
            digests.update(construction[category])
        for relative,expected in digests.items():
            path = (evidence.root/relative).resolve()
            if not path.is_relative_to(evidence.root) or hashlib.sha256(path.read_bytes()).hexdigest()!=expected:
                raise RuntimeError('Changed source '+relative)
        def progress(stage):
            evidence.report['progress'] = dict(stage=stage,seconds=perf_counter()-started)
            evidence.save()
            print(json.dumps(evidence.report['progress']),flush=True)
            if perf_counter()>deadline:
                raise RuntimeError('Safe stage boundary; partial outputs retained')
        def save(name,**arrays):
            path = evidence.output/(name+'.npz')
            np.savez_compressed(path,**arrays)
            evidence.own(path,'outputs')
            return str(path.relative_to(evidence.root))
        with localcontext() as context:
            context.prec = 64
            unused,old_action,sources = restore_case(evidence,digests,'MTS-primary',args.level,deadline)
            packet = json.loads((evidence.root/construction['packet_path']).read_text())
            with np.load(evidence.root/construction['states']['primary']['path'],allow_pickle=False) as archive:
                state = {name:archive[name].copy() for name in archive.files}
            loads,action = restore_refined(old_action.owner,state,packet['mesh'],packet,'primary',deadline)
            raw = construction['amplitude']*flat_basis(action.knots,action.owner.model.anchor,float(action.edges[0]),float(action.edges[-1]))
            raw_gram,collocation = trial_norm(action,raw)
            unused,triangular = np.linalg.qr(collocation,mode='reduced')
            transform = np.linalg.solve(triangular,np.eye(24))*triangular[0,0]
            transform[:,0] = np.eye(24)[:,0]
            basis = decimals(raw)@decimals(transform)
            evidence.check('QR_rank_resolved',np.linalg.cond(triangular)<1e9,float(np.linalg.cond(triangular)))
            evidence.check('QR_preserves_constructed_state',maximum(basis[:,0]-loads.coordinates[0,:-1])<Decimal('1e-40'))
            evidence.check('QR_nested_spaces',not np.any(np.tril(transform,-1)))
            basis_path = save('source-flat-basis',basis_exact=np.asarray(basis,str),raw=raw,transform=transform,
                source=np.asarray(loads.coordinates[:,-1],str),rates=loads.rates)
        engine = NativeKernel(action.mesh,packet['gram_support'],True)
        reference = NativeKernel(action.mesh,packet['gram_support'],False)
        evidence.report.update(level=args.level,basis_path=basis_path,frozen_metric=True,
            fresh_metric_is_for_constructed_balanced_state=True,shape_tests=33,trial_sizes=[8,16,24],
            rule_outputs=[],searches=[],native_constraints_solved=False,physical_evolution=False)
        for spatial,material in [(8,32),(12,48)]:
            progress('native forms '+str(material))
            labels,weights = np.polynomial.legendre.leggauss(material)
            labels,weights = labels/2,weights/2
            weights *= 6*(labels+.5)*(.5-labels)
            forms,norms,potentials = [],[],[]
            with localcontext() as context:
                context.prec = 64
                for position,label in enumerate(labels):
                    data = physical_data(engine,loads,action,label)
                    movement = movements(engine,data['edges'],data['source'])
                    field = basis*sum(decimals(data['cardinal']),Decimal(0))
                    current,potential,image,tangent,native_rate = shape_forms(engine,data,field,movement)
                    norm,unused = trial_norm(action,field,spatial,label)
                    forms.append(current)
                    norms.append(norm)
                    potentials.append(potential)
                    if position==len(labels)//2:
                        columns = [0,7,23]
                        selected = field[:,columns]
                        tests = [0,8,32]
                        rate = transport(engine,data['edges'],selected,movement[:,tests])
                        old_image,old_tangent = image_and_tangent(engine,data['edges'],selected,movement[:,tests],rate)
                        scale = max(maximum(image[:,columns]),maximum(tangent[:,tests][:,:,columns]),Decimal('1e-30'))
                        difference = max(maximum(old_image-image[:,columns]),maximum(old_tangent-tangent[:,tests][:,:,columns]))/scale
                        evidence.check(str(material)+':telescoping_atom_and_tangent_oracle',difference<Decimal('1e-32'),str(difference))
                        radius = nodal_radii(engine,data['edges'])
                        hinge = np.array([max(point-data['source'],Decimal(0)) for point in radius],dtype=object)
                        hinge_image = source_hinge_image(engine,data['edges'],data['source'])
                        evidence.check(str(material)+':all_modes_rowwise_hinge_isolation',maximum(hinge_image[:,None]*image)==0)
                        coefficients = decimals(np.linspace(-.2,.3,24))
                        trial = field@coefficients
                        scalar = engine.evaluate(data['edges'],trial,data['beta'])
                        test = 11
                        shifted = nodal_transport(engine,scalar,movement[:,test])
                        direct = sum(scalar['field_gradient']*shifted,Decimal(0))+sum(scalar['edge_gradient']*movement[:,test],Decimal(0))
                        direct += sum(scalar['load']*data['beta_radial']*movement[engine.native_edges,test],Decimal(0))
                        predicted = np.asarray(coefficients,float)@current[test]@np.asarray(coefficients,float)
                        relative = abs(float(direct)-predicted)/max(abs(float(direct)),1e-30)
                        evidence.check(str(material)+':independent_scalar_shape_adjoint',relative<2e-10,relative)
                        empty = shape_forms(reference,data,field[:,:2],movement[:,:2])
                        evidence.check(str(material)+':matched_empty_operator_forms',not np.any(empty[0]) and not np.any(empty[1]))
                    if position%8==7:
                        save('partial-'+str(material),labels=labels[:position+1],weights=weights[:position+1],
                            force_layers=np.array(forms),norm_layers=np.array(norms),potential_layers=np.array(potentials))
                        progress(str(material)+':material label '+str(position+1))
            total = np.einsum('l,lkij->kij',weights,np.array(forms))
            norm = np.einsum('l,lij->ij',weights,np.array(norms))
            potential = np.einsum('l,lij->ij',weights,np.array(potentials))
            path = save('forms-'+str(material),labels=labels,weights=weights,force_layers=np.array(forms),
                norm_layers=np.array(norms),potential_layers=np.array(potentials),forces=total,norm=norm,potential=potential)
            evidence.report['rule_outputs'].append(dict(spatial=spatial,material=material,path=path))
            evidence.save()
            for size in [8,16,24]:
                progress(str(material)+':solve source-compatible family '+str(size))
                search = reduced_search(total,norm,potential,size)
                evidence.check(str(material)+':'+str(size)+':norm_retained',search['best']['norm_relative_error']<2e-8)
                certificate = separator(total,norm,size) if material==48 else None
                record = dict(material=material,size=size,search=search,certificate=certificate)
                evidence.report['searches'].append(record)
                evidence.save()
        accepted = [row for row in evidence.report['searches'] if row['material']==48 and row['search']['frozen_root']
            and row['search']['best']['withheld_max']<1e-9]
        evidence.report.update(seconds=perf_counter()-started,live_recompute_candidates=accepted,
            source_compatibility_built_in=True,source_acceleration_fitted=False,
            no_global_theory_exclusion=True,github_action=False,subagents_used=False)
        evidence.complete()
    except Exception as error:
        evidence.fail(error)
        raise


if __name__=='__main__':
    main()


from derive_annular_source_gravity_20260914 import EvidenceRun
from annular_acceleration_archive_checks_v2_20261001 import verify_report
from annular_high_order_native_v2_20261003 import high_mesh, HighKernel
from annular_candidate_hamiltonian_20260921 import decimals
from annular_physical_native_kernel_20260928 import maximum
from analyze_annular_source_flat_state_20261002 import read_archive
from construct_annular_septic_response_20261003 import pin, third
from decimal import Decimal, localcontext
from fractions import Fraction
from scipy.sparse import coo_matrix, save_npz
from math import comb
import json
import numpy as np


def exact(value):
    value = Fraction(value)
    return Decimal(value.numerator)/Decimal(value.denominator)


def main():
    pin(4)
    evidence = EvidenceRun('annular-P7-bisection-preparation-attempt01', __file__)
    try:
        base = 'source-intake/navier-stokes/20260914/'
        parent = verify_report(evidence, base+'annular-product-source-corrected-live-primary-attempt01/status.json')
        evidence.own(evidence.root/'DERIVATION-20261003-fixed-profile-P7-bisection.md')
        coarse = json.loads((evidence.root/parent['mesh_path']).read_text())
        saved = read_archive(evidence.root/parent['states'][0]['path'])
        fine = high_mesh(coarse['gram_support'], coarse['anchor'], 7, 2)
        evidence.check('unchanged_native_support', fine['gram_support']==coarse['gram_support'] and len(fine['gram_support'])==1094)
        evidence.check('bisected_field_space', fine['count']==2*coarse['count']==15316)
        lookup = {Fraction(value):index for index,value in enumerate(fine['nodes'])}
        restriction = np.array([lookup[Fraction(value)] for value in coarse['nodes']])
        templates = []
        with localcontext() as context:
            context.prec = 75
            old_engine, new_engine = HighKernel(coarse, coarse['gram_support']), HighKernel(fine, fine['gram_support'])
            for half in range(2):
                local_rows = []
                for node in range(8):
                    point = Fraction(half,2)+Fraction(node,14)
                    weights = []
                    for column in range(8):
                        value = Fraction(1)
                        for other in range(8):
                            if other!=column:
                                value *= (point-Fraction(other,7))/(Fraction(column,7)-Fraction(other,7))
                        weights.append(value)
                    evidence.check('half'+str(half)+':node'+str(node)+':all_polynomials_through_degree7',
                        all(sum(weight*Fraction(column,7)**power for column,weight in enumerate(weights))==point**power for power in range(8)))
                    local_rows.append(weights)
                templates.append(local_rows)
            position = decimals(saved['coordinates'])
            fields = position[:, :-1].T
            fine_field = np.full((fine['count'], fields.shape[1]), Decimal(0), dtype=object)
            row_map = {}
            for cell, old_indices in enumerate(old_engine.indices):
                for half in range(2):
                    for local_index, target in enumerate(new_engine.indices[2*cell+half]):
                        if target<0:
                            continue
                        row = {int(column):weight for column,weight in zip(old_indices,templates[half][local_index]) if column>=0 and weight}
                        if int(target) in row_map and row_map[int(target)]!=row:
                            raise RuntimeError('Inconsistent shared-node embedding')
                        row_map[int(target)] = row
            for target,row in row_map.items():
                fine_field[target] = sum((exact(weight)*fields[column] for column,weight in row.items()), np.full(fields.shape[1],Decimal(0),dtype=object))
            evidence.check('old_field_nodes_exactly_retained', np.array_equal(fine_field[restriction],fields))
            coordinates = np.column_stack([fine_field.T,position[:, -1]])
            old_poly = old_engine.basis.polynomial(old_engine.indices,fields)
            new_poly = new_engine.basis.polynomial(new_engine.indices,fine_field)
            polynomial_error = Decimal(0)
            for half in range(2):
                transformed = np.full(old_poly.shape,Decimal(0),dtype=object)
                for power in range(8):
                    for output_power in range(power+1):
                        transformed[:, output_power] += old_poly[:, power]*exact(Fraction(comb(power,output_power)*half**(power-output_power),2**power))
                polynomial_error = max(polynomial_error,maximum(transformed-new_poly[half::2]))
            evidence.check('whole_cell_polynomial_identity',polynomial_error<Decimal('1e-55'),str(polynomial_error))
            old_edges=np.array(list(map(exact,coarse['edges'])),dtype=object)
            new_edges=np.array(list(map(exact,fine['edges'])),dtype=object)
            maximum_jet=Decimal(0)
            maximum_energy=Decimal(0)
            for vertex in range(len(position)):
                old_atom=old_engine.atoms(old_edges,fields[:,vertex])
                new_atom=new_engine.atoms(new_edges,fine_field[:,vertex])
                for key,offset in [('slope_left',0),('slope_right',1),('curvature_left',0),('curvature_right',1)]:
                    maximum_jet=max(maximum_jet,maximum(new_atom[key][offset::2]-old_atom[key]))
                maximum_jet=max(maximum_jet,maximum(third(new_atom)[::2,0]-third(old_atom)[:,0]),maximum(third(new_atom)[1::2,1]-third(old_atom)[:,1]))
                old_result=old_engine.evaluate(old_edges,fields[:,vertex],np.full(1094,Decimal(1),dtype=object))
                new_result=new_engine.evaluate(new_edges,fine_field[:,vertex],np.full(1094,Decimal(1),dtype=object))
                maximum_energy=max(maximum_energy,abs(new_result['energy']-old_result['energy']))
                evidence.check('vertex'+str(vertex)+':native_values',np.array_equal(fields[old_engine.native_indices,vertex],fine_field[new_engine.native_indices,vertex]))
                evidence.check('vertex'+str(vertex)+':source_jump_preserved',abs(new_result['source_jump']-old_result['source_jump'])<Decimal('1e-40'))
                evidence.check('vertex'+str(vertex)+':new_midpoint_jets_continuous',
                    max(maximum(new_atom['slope_left'][1::2]-new_atom['slope_right'][::2]),maximum(new_atom['curvature_left'][1::2]-new_atom['curvature_right'][::2]))<Decimal('1e-35'))
            evidence.check('all_old_endpoint_jets_through_third',maximum_jet<Decimal('1e-32'),str(maximum_jet))
            evidence.check('native_energy_same_reference_geometry',maximum_energy<Decimal('1e-45'),str(maximum_energy))
        rows,columns,values=[],[],[]
        for target,row in row_map.items():
            for column,weight in row.items():
                rows.append(target); columns.append(column); values.append(float(weight))
        transfer=coo_matrix((values,(rows,columns)),shape=(fine['count'],coarse['count'])).tocsr()
        mesh_path=evidence.output/'P7-bisected-mesh.json'
        mesh_path.write_text(json.dumps(fine)+'\n')
        map_path=evidence.output/'rational-bisection-map.json'
        map_path.write_text(json.dumps(dict(templates=[[[str(value) for value in row] for row in half] for half in templates],restriction=restriction.tolist()))+'\n')
        transfer_path=evidence.output/'field-prolongation.npz'
        save_npz(transfer_path,transfer)
        initial_path=evidence.output/'P7-bisected-initial.npz'
        np.savez_compressed(initial_path,coordinates=np.asarray(coordinates,str),rates=np.zeros(coordinates.shape),restriction=restriction)
        for path in [mesh_path,map_path,transfer_path,initial_path]:
            evidence.own(path,'outputs')
        evidence.report.update(mesh_path=str(mesh_path.relative_to(evidence.root)),initial_path=str(initial_path.relative_to(evidence.root)),
            transfer_path=str(transfer_path.relative_to(evidence.root)),map_path=str(map_path.relative_to(evidence.root)),
            coarse_mesh_path=parent['mesh_path'],parent_state_path=parent['states'][0]['path'],same_physical_profile=True,
            unchanged_material_vertices=len(position),native_support_count=1094,field_count=fine['count'],
            no_refit=True,source_unchanged=True,decimal_precision=75,valid_for_claim=False,github_action=False,subagents_used=False)
        evidence.complete()
    except Exception as error:
        evidence.fail(error)
        raise


if __name__=='__main__':
    main()

from derive_annular_source_gravity_20260914 import EvidenceRun
from annular_C0_transport_context_20260930 import restore
from annular_compensated_acceleration_polynomial_v2_20261001 import CompensatedPolynomial, paired_cheb
from decimal import Decimal, localcontext
from scipy.linalg import solve_banded
from time import perf_counter
import argparse
import ctypes
import hashlib
import json
import numpy as np
import sympy as sp


def trace(values):
    return np.r_[values[0,0],values[1:,0]-values[:-1,2],values[-1,2]]


def lift(mass,values):
    inverse = np.linalg.inv(mass)
    diagonal = np.r_[inverse[0,0,0],inverse[:-1,2,2]+inverse[1:,0,0],inverse[-1,2,2]]
    off = -inverse[:,0,2].copy()
    off[-1] *= -1
    scaling = 1/np.sqrt(diagonal)
    scaled_off = off*scaling[:-1]*scaling[1:]
    banded = np.zeros((3,len(diagonal)))
    banded[1] = 1
    banded[0,1:] = scaled_off
    banded[2,:-1] = scaled_off
    jumps = trace(values)
    multiplier = scaling*solve_banded((1,1),banded,scaling*jumps)
    covector = np.zeros_like(values)
    covector[:,0] = multiplier[:-1]
    covector[:,2] = -multiplier[1:]
    covector[-1,2] *= -1
    minimum = np.einsum('cij,cj->ci',inverse,covector)
    remainder = values-minimum
    quadratic = lambda left,right: float(np.einsum('ci,cij,cj->',left,mass,right))
    energy = np.array([quadratic(values,values),quadratic(minimum,minimum),
        quadratic(remainder,remainder),quadratic(minimum,remainder)])
    normal = max(float(np.max(abs(jumps))),float(np.max(abs(values))),1e-300)
    errors = dict(trace=float(np.max(abs(trace(remainder))))/normal,
        orthogonality=abs(energy[3])/max(energy[0],1e-300),
        splitting=abs(energy[0]-energy[1]-energy[2]-2*energy[3])/max(energy[0],1e-300),
        dual=abs(energy[1]-float(jumps@multiplier))/max(energy[0],1e-300))
    return minimum,remainder,energy,errors,dict(multiplier=multiplier,jumps=jumps,
        diagonal=diagonal,off_diagonal=off)


def controls(evidence):
    point = sp.symbols('x')
    basis = sp.Matrix([(1-point)*(1-2*point),4*point*(1-point),point*(2*point-1)])
    mass = (basis*basis.T).applyfunc(lambda value:sp.integrate(value,(point,0,1)))
    expected = sp.Matrix([[4,2,-1],[2,16,2],[-1,2,4]])/30
    evidence.check('P2_mass_symbolic',mass==expected)
    evidence.check('P2_trace_kernel_symbolic',mass.inv()[0,0]==9 and mass.inv()[0,2]==3)
    lengths = np.array([.17,.03,.4,.12])
    matrices = lengths[:,None,None]*np.array(expected,float)
    nodal = np.array([[0.,.3,.7],[-.1,.4,.2],[.8,.1,-.3],[.5,.6,0.]])
    minimum,remainder,energy,errors,details = lift(matrices,nodal)
    evidence.check('manufactured_jump_and_energy',max(errors.values())<1e-12 and min(energy[:3])>0,errors)
    addition = np.array([[0.,.2,.4],[.4,-.6,.1],[.1,.3,-.2],[-.2,.5,0.]])
    shifted = lift(matrices,nodal+addition)
    evidence.check('continuous_addition_cannot_change_minimum_lift',
        float(np.max(abs(shifted[0]-minimum)))<1e-12)
    evidence.check('dropping_jumps_detected',np.max(abs(details['jumps']))>.5)


def jump_oracle(evidence,name,polynomial):
    with localcontext() as context:
        context.prec = 90
        number = len(polynomial.widths)
        faces = np.unique(np.linspace(1,number-1,16).astype(int))
        rows = []
        for index,face in enumerate(faces):
            label = [Decimal('-.41'),Decimal('-.13'),Decimal('.19'),Decimal('.43')][index%4]
            selected = np.array([face-1,face])
            local = np.array([Decimal(1),Decimal(0)],dtype=object)
            denominator = paired_cheb(polynomial.exact_denominator[selected],2*label)
            motion = paired_cheb(polynomial.exact_map_left[selected],2*label)
            motion += local*paired_cheb(polynomial.exact_map_slope[selected],2*label)
            for variant,data in polynomial.exact.items():
                field = paired_cheb(data['field'][selected],2*label)
                change = paired_cheb(data['change'][selected],2*label)
                numerator = paired_cheb(data['numerator'][selected],2*label)
                gradient = (field[:,1]+2*local*field[:,2])/denominator
                delta = change[:,0]+local*(change[:,1]+local*change[:,2])
                residual = (numerator[:,0]+local*(numerator[:,1]+local*numerator[:,2]))/denominator
                jump = residual[1]-residual[0]
                field_jump = delta[1]-delta[0]
                map_jump = motion[1]-motion[0]
                predicted = field_jump-motion[1]*(gradient[1]-gradient[0])-map_jump*gradient[0]
                rows.append(dict(face=int(face),label=str(label),variant=variant,jump=str(jump),
                    field_jump=str(field_jump),map_jump=str(map_jump),identity_error=str(jump-predicted)))
        worst = max(abs(Decimal(row['identity_error'])) for row in rows)
        continuous = max(abs(Decimal(row['field_jump'])) for row in rows if row['variant']=='parent_nodal')
        map_error = max(abs(Decimal(row['map_jump'])) for row in rows)
        evidence.check(name+':actual_jump_identity',worst<Decimal('1e-60'),str(worst))
        evidence.check(name+':parent_field_continuity',continuous<Decimal('1e-60'),str(continuous))
        evidence.check(name+':map_continuity',map_error<Decimal('1e-60'),str(map_error))
        path = evidence.output/(name+'-jump-oracle.json')
        path.write_text(json.dumps(rows,indent=2),encoding='utf-8')
        evidence.own(path,'outputs')


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--branch',choices=['reference-reference','MTS-primary'],required=True)
    parser.add_argument('--cpu',type=int,choices=[2,4],required=True)
    parser.add_argument('--label',required=True)
    args = parser.parse_args()
    kernel = ctypes.windll.kernel32
    kernel.GetCurrentProcess.restype = ctypes.c_void_p
    kernel.SetProcessAffinityMask.argtypes = [ctypes.c_void_p,ctypes.c_size_t]
    if not kernel.SetProcessAffinityMask(kernel.GetCurrentProcess(),1<<args.cpu):
        raise OSError('CPU affinity failed')
    evidence = EvidenceRun(args.label,__file__)
    started,deadline = perf_counter(),perf_counter()+2400
    try:
        evidence.own(evidence.root/'DERIVATION-20261001-spatial-jump-kinetic-lifting.md')
        seal_path = evidence.output.parent/'annular-C1-integrated-stage-integrity-20261001.json'
        seal = json.loads(seal_path.read_text())
        evidence.own(seal_path)
        evidence.check('parent_complete',seal['state']=='complete' and not seal['mismatches'])
        hashes = {}
        for relative,expected in seal['hashes'].items():
            path = (evidence.root/relative).resolve()
            if not path.is_relative_to(evidence.root) or hashlib.sha256(path.read_bytes()).hexdigest()!=expected:
                raise RuntimeError('Changed parent '+relative)
            hashes[str(path.relative_to(evidence.root))] = expected
        short = 'reference' if args.branch=='reference-reference' else 'MTS'
        probe_path = evidence.output.parent/('annular-common-physical-jet-'+short+'-attempt02')/'status.json'
        probe = json.loads(probe_path.read_text())
        evidence.own(probe_path)
        evidence.check('common_jet_complete',probe['state']=='complete' and all(row['passed'] for row in probe['checks']))
        for category in ['inputs','outputs']:
            for relative,expected in probe[category].items():
                path = (evidence.root/relative).resolve()
                if not path.is_relative_to(evidence.root) or hashlib.sha256(path.read_bytes()).hexdigest()!=expected:
                    raise RuntimeError('Changed common jet '+relative)
                hashes[str(path.relative_to(evidence.root))] = expected

        def read(relative):
            path = (evidence.root/relative).resolve()
            key = str(path.relative_to(evidence.root))
            if key not in hashes or hashlib.sha256(path.read_bytes()).hexdigest()!=hashes[key]:
                raise RuntimeError('Unowned input '+relative)
            evidence.own(path)
            if path.suffix=='.json':
                return json.loads(path.read_text())
            with np.load(path,allow_pickle=False) as saved:
                return {name:saved[name].copy() for name in saved.files}

        controls(evidence)
        with localcontext() as context:
            context.prec = 80
            setups = {level:restore(evidence,args.branch,level,deadline) for level in ['fine','third']}
        evaluators = {level:item['evaluator'] for level,item in setups.items()}
        third = evaluators['third']
        live = read(str((evidence.output.parent/'annular-live-support-acceleration-attempt01/status.json').relative_to(evidence.root)))
        polynomials = {}
        with localcontext() as context:
            context.prec = 80
            for level in ['fine','third']:
                case = next(row for row in live['cases'] if row['branch']==args.branch and row['level']==level)
                directions = read(case['direction_path'])
                correction = read(case['paths']['projection'])['correction']
                polynomial = CompensatedPolynomial(evaluators[level],directions,correction,
                    setups[level]['setup']['loads'].coordinates[:,:-1].T)
                jump_oracle(evidence,level,polynomial)
                polynomials[level] = polynomial
                if perf_counter()>deadline:
                    raise RuntimeError('Safe polynomial boundary')
        evidence.report.update(branch=args.branch,rule_outputs=[],metric='common_third_background',
            fixed_source_response=True,independent_material_labels=True,full_parent_reprojection=False,
            github_action=False,subagents_used=False,valid_for_claim=False)
        variants = ['rounded_coefficients','parent_nodal']
        for spatial,material in [(8,32),(12,48)]:
            nodes,spatial_weights = np.polynomial.legendre.leggauss(spatial)
            cells = np.repeat(np.arange(len(third.widths)),spatial)
            local = np.tile((nodes+1)/2,len(third.widths))
            reference = third.edges[cells]+third.widths[cells]*local
            spatial_measure = np.repeat(third.widths,spatial)*np.tile(spatial_weights/2,len(third.widths))
            displacement = np.where(reference<0,1+reference/(-third.edges[0]),1-reference/third.edges[-1])
            label_nodes,label_weights = np.polynomial.legendre.leggauss(material)
            label_nodes,label_weights = label_nodes/2,label_weights/2
            label_weights *= 6*(label_nodes+.5)*(.5-label_nodes)
            layers,diagnostics = [],[]
            for index,(label,label_weight) in enumerate(zip(label_nodes,label_weights)):
                cardinal = np.asarray(third.action.cardinal(label)).ravel()
                source_offset = float(cardinal@(third.action.source-third.anchor))
                offsets = reference+displacement*source_offset+(1-displacement)*third.action.owner.width*label
                jacobian = np.where(reference<0,1+(source_offset-third.action.owner.width*label)/(-third.edges[0]),
                    1-(source_offset-third.action.owner.width*label)/third.edges[-1])
                radius = third.anchor+offsets
                metric_values = third.metric.evaluate(offsets,third.metric.cells(offsets))[0]
                metric = 1-2*metric_values[0]/radius
                alpha = radius**2/(np.exp(metric_values[1])*np.sqrt(metric))
                measure = spatial_measure*jacobian*alpha
                if np.min(measure)<=0 or np.min(metric)<=0:
                    raise RuntimeError('Nonpositive inherited kinetic measure')
                source = third.anchor+source_offset
                source_values = third.action.solver.values(third.action.solution,np.array([source]))[0][:,0]
                source_metric,source_lapse = 1-2*source_values[0]/source,np.exp(source_values[1])
                speed = float(cardinal@third.action.velocity)
                inertia = third.action.owner.source_mass*source_lapse**2/(source_metric*(source_lapse**2-speed**2/source_metric)**1.5)
                layer,diagnostic = [],[]
                for level in ['fine','third']:
                    selected = cells//2 if level=='fine' else cells
                    coordinate = (cells%2+local)/2 if level=='fine' else local
                    basis = np.array([(1-coordinate)*(1-2*coordinate),4*coordinate*(1-coordinate),
                        coordinate*(2*coordinate-1)]).T
                    mass = np.zeros((len(polynomials[level].widths),3,3))
                    np.add.at(mass,selected,measure[:,None,None]*basis[:,:,None]*basis[:,None,:])
                    if np.min(np.linalg.eigvalsh(mass))<=0:
                        raise RuntimeError('Nonpositive local mass')
                    for variant in variants:
                        polynomial = polynomials[level]
                        coefficients = paired_cheb(polynomial.coefficients[variant],2*label)
                        coefficients /= paired_cheb(polynomial.denominator,2*label)[:,None]
                        nodal = np.column_stack([coefficients[:,0],coefficients[:,0]+.5*coefficients[:,1]+.25*coefficients[:,2],
                            np.sum(coefficients,axis=1)])
                        minimum,remainder,energy,errors,details = lift(mass,nodal)
                        direct = coefficients[selected,0]+coordinate*(coefficients[selected,1]+coordinate*coefficients[selected,2])
                        integral = float(measure@(direct**2))
                        errors['direct_integral'] = abs(integral-energy[0])/max(energy[0],1e-300)
                        source_direction = float(cardinal@evaluators[level].source_direction)
                        source_norm = inertia*source_direction**2
                        layer.append(np.r_[energy,source_norm])
                        diagnostic.append([errors[name] for name in ['trace','orthogonality','splitting','dual','direct_integral']])
                        if index==material//2:
                            path = evidence.output/(level+'-'+variant+'-'+str(spatial)+'-'+str(material)+'-witness.npz')
                            np.savez_compressed(path,mass=mass,nodal=nodal,minimum=minimum,remainder=remainder,
                                energy=energy,label=label,source_norm=source_norm,**details)
                            evidence.own(path,'outputs')
                layers.append(layer)
                diagnostics.append(diagnostic)
                if index%8==7:
                    path = evidence.output/('partial-'+str(spatial)+'-'+str(material)+'.npz')
                    temporary = path.with_suffix('.npz.tmp')
                    with temporary.open('wb') as stream:
                        np.savez_compressed(stream,layers=np.array(layers),diagnostics=np.array(diagnostics),
                            labels=label_nodes,weights=label_weights,next_label=index+1)
                    temporary.replace(path)
                    evidence.report['progress'] = dict(spatial=spatial,material=material,label=index+1,seconds=perf_counter()-started)
                    evidence.save()
                    print(json.dumps(evidence.report['progress']),flush=True)
                    if perf_counter()>deadline:
                        raise RuntimeError('Safe completed-label boundary')
            layers,diagnostics = np.array(layers),np.array(diagnostics)
            total = np.einsum('q,qij->ij',label_weights,layers)
            worst = np.max(diagnostics,axis=(0,1))
            evidence.check(str(spatial)+':all_jump_projection_controls',np.max(worst)<2e-11,worst.tolist())
            summaries = []
            for row,(level,variant) in zip(total,[(level,variant) for level in ['fine','third'] for variant in variants]):
                wave,jump,continuous,cross,source_norm = row
                summaries.append(dict(level=level,variant=variant,wave_norm=float(wave),jump_minimum_norm=float(jump),
                    continuous_norm=float(continuous),cross_norm=float(cross),source_norm=float(source_norm),
                    jump_wave_fraction=float(jump/wave),jump_total_fraction=float(jump/(wave+source_norm)),
                    continuous_wave_fraction=float(continuous/wave)))
            path = evidence.output/('jump-lifting-'+str(spatial)+'-'+str(material)+'.npz')
            np.savez_compressed(path,layers=layers,diagnostics=diagnostics,weights=label_weights,labels=label_nodes,total=total,
                columns=np.array(['wave','minimum_jump','continuous','cross','source']))
            evidence.own(path,'outputs')
            for item in summaries:
                comparison = next(row for row in probe['rule_outputs'] if row['summary']['spatial']==spatial and row['summary']['material']==material)
                expected_gram = next(row for row in comparison['summary']['modes'] if row['variant']==item['variant'])['gram']
                position = 0 if item['level']=='fine' else 1
                expected = expected_gram[position][position]
                error = abs(item['wave_norm']+item['source_norm']-expected)/expected
                evidence.check(str(spatial)+':'+item['level']+':'+item['variant']+':common_norm_replay',error<2e-10,error)
            evidence.report['rule_outputs'].append(dict(spatial=spatial,material=material,path=str(path.relative_to(evidence.root)),
                summaries=summaries,maximum_controls=worst.tolist()))
            evidence.save()
        evidence.report.update(seconds=perf_counter()-started,finite_evolution_performed=False,
            spatial_jump_identity_derived=True,minimum_kinetic_lifting_derived=True)
        evidence.complete()
    except Exception as error:
        evidence.fail(error)
        raise


if __name__=='__main__':
    main()


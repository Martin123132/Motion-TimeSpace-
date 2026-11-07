from derive_annular_source_gravity_20260914 import EvidenceRun
from annular_C0_transport_context_20260930 import restore
from annular_compensated_acceleration_polynomial_v2_20261001 import CompensatedPolynomial, decimal_values, paired_cheb
from annular_candidate_coordinate_covectors_20260921 import local_polynomials
from annular_common_weighted_moments_20260920 import apply_rational_rows
from annular_radial_Ward_moments_20260921 import test_functions
from annular_C0_boundary_integral_20260930 import quadratic
from decimal import Decimal, localcontext
from fractions import Fraction
from copy import copy
from time import perf_counter
import argparse
import ctypes
import hashlib
import json
import numpy as np
import sympy as sp


def normalize_system(baseline, columns, scale):
    if not np.isfinite(scale) or scale<=0:
        raise ValueError('Positive geometric normalization required')
    rows = np.array([1/scale,1,1,1])
    return rows*baseline, rows[:,None]*columns/scale


def symbolic(evidence):
    scale = sp.symbols('N',positive=True)
    base = sp.Matrix(sp.symbols('B0:4'))
    columns = sp.Matrix(4,3,sp.symbols('C0:12'))
    amplitude = sp.Matrix(sp.symbols('s u a'))
    rows = sp.diag(1/scale,1,1,1)
    evidence.check('normalization_is_coordinate_change',rows*base+(rows*columns/scale)*(scale*amplitude)==rows*(base+columns*amplitude))
    shape = lambda point:[(1-point)*(1-2*point),4*point*(1-point),point*(2*point-1)]
    for child in [0,1]:
        for local in [Fraction(1,7),Fraction(2,5),Fraction(7,8)]:
            parent = (child+local)/2
            for degree in [0,1,2]:
                coarse = [point**degree for point in [Fraction(0),Fraction(1,2),Fraction(1)]]
                transferred = [sum(weight*value for weight,value in zip(shape((child+point)/2),coarse))
                    for point in [Fraction(0),Fraction(1,2),Fraction(1)]]
                value = sum(weight*sample for weight,sample in zip(shape(local),transferred))
                if value!=parent**degree:
                    raise RuntimeError('Rational transfer failed')
    evidence.check('rational_P2_nested_transfer',True)
    field_f,field_t,map_f,map_t,gradient_f,gradient_t = sp.symbols('dF dT wF wT gF gT')
    difference = (field_t-map_t*gradient_t)-(field_f-map_f*gradient_f)
    separated = -map_f*(gradient_t-gradient_f)+(field_t-field_f)-(map_t-map_f)*gradient_t
    evidence.check('background_and_transfer_commutator_identity',sp.expand(difference-separated)==0)


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
    started,deadline = perf_counter(),perf_counter()+6000
    try:
        evidence.own(evidence.root/'DERIVATION-20261001-common-physical-support-jet.md')
        seal_path = evidence.output.parent/'annular-C1-integrated-stage-integrity-20261001.json'
        seal = json.loads(seal_path.read_text())
        evidence.own(seal_path)
        evidence.check('complete_parent',seal['state']=='complete' and not seal['mismatches'])
        digests = {}
        for relative,expected in seal['hashes'].items():
            path = (evidence.root/relative).resolve()
            if not path.is_relative_to(evidence.root) or hashlib.sha256(path.read_bytes()).hexdigest()!=expected:
                raise RuntimeError('Changed parent '+relative)
            digests[str(path.relative_to(evidence.root))] = expected
        evidence.check('parent_hashes_verified',len(digests)==len(seal['hashes']),len(digests))

        def read(relative):
            path = (evidence.root/relative).resolve()
            key = str(path.relative_to(evidence.root))
            if key not in digests or hashlib.sha256(path.read_bytes()).hexdigest()!=digests[key]:
                raise RuntimeError('Unowned input '+relative)
            evidence.own(path)
            if path.suffix=='.json':
                return json.loads(path.read_text())
            with np.load(path,allow_pickle=False) as data:
                return {name:data[name].copy() for name in data.files}

        def save(name,**arrays):
            path = evidence.output/(name+'.npz')
            np.savez_compressed(path,**arrays)
            evidence.own(path,'outputs')
            return str(path.relative_to(evidence.root))

        symbolic(evidence)
        with localcontext() as context:
            context.prec = 80
            setups = {level:restore(evidence,args.branch,level,deadline) for level in ['fine','third']}
            evaluators = {level:item['evaluator'] for level,item in setups.items()}
            fine,third = evaluators['fine'],evaluators['third']
            evidence.check('same_source_and_velocity',np.array_equal(fine.action.source,third.action.source)
                and np.array_equal(fine.action.velocity,third.action.velocity))
            evidence.check('same_material_cardinals',np.array_equal(fine.action.owner.layer_rule.inverse,third.action.owner.layer_rule.inverse))
            evidence.check('nested_edges',np.array_equal(fine.edges,third.edges[::2]))
            live = read(str((evidence.output.parent/'annular-live-support-acceleration-attempt01/status.json').relative_to(evidence.root)))
            cases = {level:next(row for row in live['cases'] if row['branch']==args.branch and row['level']==level) for level in setups}
            mesh_packets = {level:read(cases[level]['sources']['packet']) for level in setups}
            evidence.check('fixed_physical_interaction_support',mesh_packets['fine']['gram_support']==mesh_packets['third']['gram_support'])
            directions = {level:read(cases[level]['direction_path']) for level in setups}
            corrections = {level:read(cases[level]['paths']['projection'])['correction'] for level in setups}
            for level in setups:
                evaluator = evaluators[level]
                source_index = int(np.argmin(abs(evaluator.edges)))
                evidence.check(level+':generator_pins',np.max(abs(evaluator.edge_vertices[:,[0,source_index,-1]]))==0)
            fine_polynomial = CompensatedPolynomial(fine,directions['fine'],corrections['fine'],setups['fine']['setup']['loads'].coordinates[:,:-1].T)
            polynomial_paths = {}
            for variant,coefficients in fine_polynomial.coefficients.items():
                polynomial_paths['fine-'+variant] = save('fine-'+variant+'-polynomial',numerator=coefficients,
                    denominator=fine_polynomial.denominator,widths=fine_polynomial.widths,degree=fine_polynomial.degree)
            short = 'reference' if args.branch=='reference-reference' else 'MTS'
            owned_third = object.__new__(CompensatedPolynomial)
            owned_third.coefficients = {}
            for variant in ['rounded_coefficients','parent_nodal']:
                relative = str((evidence.output.parent/('annular-compensated-polynomial-'+short+'-third-attempt02')/(variant+'-coefficients.npz')).relative_to(evidence.root))
                data = read(relative)
                owned_third.coefficients[variant] = data['numerator']
                owned_third.denominator,owned_third.widths = data['denominator'],data['widths']
            rows = mesh_packets['third']['prolongation']
            transferred_raw = apply_rational_rows(rows,decimal_values(directions['fine']['field_vertices']).T).T
            transferred_correction = apply_rational_rows(rows,decimal_values(corrections['fine'][:,:-1]).T).T
            edge = decimal_values(directions['fine']['edge_vertices'])
            transferred_edge = np.empty((edge.shape[0],2*edge.shape[1]-1),dtype=object)
            transferred_edge[:,::2] = edge
            transferred_edge[:,1::2] = (edge[:,:-1]+edge[:,1:])/2
            correction = np.column_stack([transferred_correction,decimal_values(corrections['fine'][:,-1])])
            transported_directions = dict(field_vertices=transferred_raw,edge_vertices=transferred_edge)
            transported = copy(third)
            transported.edge_vertices = transferred_edge
            transported.source_direction = fine.source_direction.copy()
            transported.polynomials = dict(third.polynomials)
            transported.polynomials['field_change'] = local_polynomials(third.action.mesh,(transferred_raw-transferred_correction).T)[0]
            transported_polynomial = CompensatedPolynomial(transported,transported_directions,correction,setups['third']['setup']['loads'].coordinates[:,:-1].T)
            transfer_path = save('transported-fine-candidate',
                field_vertices=np.asarray(transferred_raw,float),edge_vertices=np.asarray(transferred_edge,float),
                correction=np.asarray(correction,float),field_vertices_exact=np.asarray(transferred_raw,str),
                edge_vertices_exact=np.asarray(transferred_edge,str),correction_exact=np.asarray(correction,str),
                source_direction=fine.source_direction,restriction=np.array(mesh_packets['third']['restriction']),
                parent_direction_path=np.array(cases['fine']['direction_path']),
                parent_projection_path=np.array(cases['fine']['paths']['projection']))
            restriction = mesh_packets['third']['restriction']
            evidence.check('transported_field_restriction',np.array_equal(np.asarray(transferred_raw[:,restriction],float),directions['fine']['field_vertices']))
            evidence.check('transported_correction_restriction',np.array_equal(np.asarray(transferred_correction[:,restriction],float),corrections['fine'][:,:-1]))
            evidence.check('transported_edge_restriction',np.array_equal(np.asarray(transferred_edge[:,::2],float),directions['fine']['edge_vertices']))
            for variant,coefficients in transported_polynomial.coefficients.items():
                polynomial_paths['transported-'+variant] = save('transported-'+variant+'-polynomial',
                    numerator=coefficients,denominator=transported_polynomial.denominator,widths=transported_polynomial.widths,
                    degree=transported_polynomial.degree)
            cells = np.linspace(0,len(third.widths)-1,48).astype(int)
            labels = np.tile([-.43,-.17,.03,.29,.47,.11],8)
            local = np.tile([.13,.47,.83],16)
            for name,poly,selected,coordinates in [('fine',fine_polynomial,cells//2,(cells%2+local)/2),
                ('transported',transported_polynomial,cells,local)]:
                for variant in ['rounded_coefficients','parent_nodal']:
                    checked = poly.oracle(variant,selected,labels,coordinates)
                    evidence.check(name+':'+variant+':coefficient_oracle',checked['exact_relative']<1e-55
                        and checked['within_arithmetic_budget'],dict(exact_relative=checked['exact_relative'],binary_relative=checked['binary_relative']))
            evidence.report.update(branch=args.branch,level_pair=['fine','third'],rule_outputs=[],
                transfer_path=transfer_path,polynomial_paths=polynomial_paths,normalization='common_continuous_geometric_RMS',
                third_legacy_coefficients_reused=True,transported_old_Euler_resolved=False,
                full_current_grid_comparison_completed=False,github_action=False,subagents_used=False,valid_for_claim=False)
            fields = [fine_polynomial,owned_third,transported_polynomial]
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
                layers = []
                for index,(label,label_weight) in enumerate(zip(label_nodes,label_weights)):
                    cardinal = np.asarray(third.action.cardinal(label)).ravel()
                    source_offset = float(cardinal@(third.action.source-third.anchor))
                    offsets = reference+displacement*source_offset+(1-displacement)*third.action.owner.width*label
                    jacobian = np.where(reference<0,1+(source_offset-third.action.owner.width*label)/(-third.edges[0]),
                        1-(source_offset-third.action.owner.width*label)/third.edges[-1])
                    radius = third.anchor+offsets
                    measure = spatial_measure*jacobian
                    label_array = np.full(len(radius),label)
                    values = third.metric.evaluate(offsets,third.metric.cells(offsets))[0]
                    metric = 1-2*values[0]/radius
                    alpha = radius**2/(np.exp(values[1])*np.sqrt(metric))
                    source = third.anchor+source_offset
                    endpoints = third.anchor+np.where(reference<0,third.edges[0],third.edges[-1])+third.action.owner.width*label
                    exact_eta = test_functions(radius)[0][1]-displacement*test_functions(source)[0][1]
                    exact_eta -= (1-displacement)*test_functions(endpoints)[0][1]
                    etas = []
                    for evaluator,selected,coordinate in [(fine,cells//2,(cells%2+local)/2),(third,cells,local)]:
                        edge_values = cardinal@evaluator.edge_vertices
                        etas.append(edge_values[selected]*(1-coordinate)+edge_values[selected+1]*coordinate)
                    geometry_rows = np.array([measure@np.ones(len(radius)),measure@(exact_eta**2),
                        measure@((etas[0]-exact_eta)**2),measure@((etas[1]-exact_eta)**2),
                        measure@(etas[0]**2),measure@(etas[1]**2),measure@((etas[1]-etas[0])**2)])
                    source_values = third.action.solver.values(third.action.solution,np.array([source]))[0][:,0]
                    source_metric,source_lapse = 1-2*source_values[0]/source,np.exp(source_values[1])
                    speed = float(cardinal@third.action.velocity)
                    inertia = third.action.owner.source_mass*source_lapse**2/(source_metric*(source_lapse**2-speed**2/source_metric)**1.5)
                    source_variations = np.array([float(cardinal@fine.source_direction),float(cardinal@third.source_direction),float(cardinal@fine.source_direction)])
                    dust = inertia*np.outer(source_variations,source_variations)
                    all_grams = []
                    for variant in ['rounded_coefficients','parent_nodal']:
                        modes = np.array([poly.evaluate(variant,selected,label_array,coordinate) for poly,selected,coordinate in [
                            (fields[0],cells//2,(cells%2+local)/2),(fields[1],cells,local),(fields[2],cells,local)]])
                        gram = (modes*(measure*alpha))@modes.T
                        all_grams.append(gram+dust)
                    layers.append(np.r_[geometry_rows,np.array(all_grams).ravel()])
                    if index%8==7:
                        partial = evidence.output/('partial-'+str(spatial)+'-'+str(material)+'.npz')
                        temporary = partial.with_suffix('.npz.tmp')
                        with temporary.open('wb') as stream:
                            np.savez_compressed(stream,layers=np.array(layers),labels=label_nodes,weights=label_weights,next_label=index+1)
                        temporary.replace(partial)
                        evidence.report['progress'] = dict(spatial=spatial,material=material,label=index+1,seconds=perf_counter()-started)
                        evidence.save()
                        print(json.dumps(evidence.report['progress']),flush=True)
                        if perf_counter()>deadline:
                            raise RuntimeError('Safe common-direction boundary')
                total = label_weights@np.array(layers)
                scale = np.sqrt(total[1]/total[0])
                summaries = []
                for variant,flat in zip(['rounded_coefficients','parent_nodal'],[total[7:16],total[16:25]]):
                    gram = flat.reshape(3,3)
                    eigenvalues = np.linalg.eigvalsh(gram)
                    evidence.check(str(spatial)+':'+variant+':positive_Gram',eigenvalues[0]>=-1e-12*np.max(np.diag(gram)))
                    norm_ratio = np.sqrt(gram[1,1]/gram[0,0])
                    cosine = gram[0,1]/np.sqrt(gram[0,0]*gram[1,1])
                    best_scale = gram[0,1]/gram[0,0]
                    remainder_squared = max(0.,gram[1,1]-gram[0,1]**2/gram[0,0])
                    summaries.append(dict(variant=variant,gram=gram.tolist(),kinetic_norm_ratio=float(norm_ratio),
                        signed_cosine=float(cosine),best_scale_diagnostic_only=float(best_scale),
                        best_scale_relative_remainder=float(np.sqrt(remainder_squared/gram[1,1])),
                        transported_to_fine_norm_ratio=float(np.sqrt(gram[2,2]/gram[0,0])),
                        legacy_third_to_transported_relative_distance=float(np.sqrt(max(0.,gram[1,1]+gram[2,2]-2*gram[1,2])/gram[2,2])),
                        same_amplitude_relative_distance=float(np.sqrt(max(0.,gram[0,0]+gram[1,1]-2*gram[0,1])/gram[0,0]))))
                summary = dict(spatial=spatial,material=material,geometric_RMS=float(scale),
                    generator_relative_errors=[float(np.sqrt(total[position]/total[1])) for position in [2,3]],
                    generator_grid_relative_distance=float(np.sqrt(total[6]/total[1])),modes=summaries)
                path = save('common-'+str(spatial)+'-'+str(material),layers=np.array(layers),labels=label_nodes,
                    weights=label_weights,total=total,geometric_RMS=scale,quadrature=np.array([spatial,material]))
                evidence.report['rule_outputs'].append(dict(summary=summary,path=path))
                evidence.save()
                print(json.dumps(summary),flush=True)
            first,last = [item['summary'] for item in evidence.report['rule_outputs']]
            evidence.check('normalization_pair',abs(last['geometric_RMS']-first['geometric_RMS'])<1e-9,
                last['geometric_RMS']-first['geometric_RMS'])
            evidence.report.update(seconds=perf_counter()-started,common_candidate_constructed=True,
                no_new_physical_parameters=True,kinetic_normalization_used=False)
        for path in evidence.output.glob('partial-*.npz'):
            evidence.own(path,'outputs')
        evidence.complete()
    except Exception as error:
        for path in evidence.output.glob('partial-*.npz'):
            evidence.own(path,'outputs')
        evidence.fail(error)
        raise


if __name__=='__main__':
    main()

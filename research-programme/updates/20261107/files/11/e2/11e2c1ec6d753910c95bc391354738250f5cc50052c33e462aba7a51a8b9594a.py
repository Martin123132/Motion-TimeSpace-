from derive_annular_source_gravity_20260914 import EvidenceRun
from derive_annular_support_map_constraints_20260927 import restore_case
from annular_nested_physical_refinement_v3_20260922 import restore_refined
from annular_acceleration_archive_checks_v2_20261001 import verify_report
from annular_physical_native_kernel_20260928 import NativeKernel,maximum
from derive_annular_native_shape_stress_20260928 import physical_data
from analyze_annular_source_flat_state_20261002 import read_archive
from probe_annular_native_transmission_20261002 import hermite_values
from decimal import Decimal,localcontext
from time import perf_counter
import ctypes
import json
import numpy as np


def point_covectors(engine,data):
    native = data['edges'][engine.native_edges]
    indices = np.r_[engine.indices[:,0],engine.indices[-1,2]][engine.native_edges]
    atom = engine.atoms(data['edges'],data['field'])
    jump = atom['slope_left'][engine.anchor]-atom['slope_right'][engine.anchor-1]
    values = data['field'][indices]-jump*np.maximum(native-data['source'],Decimal(0))
    rows,coefficients,widths = [],[],[]
    for index in range(len(native)-3):
        width,coefficient = engine.stencil(native[index:index+4])
        coefficient = np.array(coefficient,dtype=object)/width.sqrt()
        rows.append(sum(coefficient*values[index:index+4],Decimal(0)))
        coefficients.append(coefficient)
        widths.append(width)
    rows = np.array(rows,dtype=object)
    image = engine.apply('template',rows)
    multiplier = engine.apply('template',engine.apply('sampling',data['beta'])*image,True)
    load = engine.apply('sampling',image**2/2,True)
    field = np.full(len(native),Decimal(0),dtype=object)
    shape = np.full(len(native),Decimal(0),dtype=object)
    for index,(coefficient,width,weight) in enumerate(zip(coefficients,widths,multiplier)):
        points = native[index:index+4]
        field[index:index+4] += weight*coefficient
        dilation = Decimal('2.5')*weight*rows[index]/width/3
        shape[index] -= dilation
        shape[index+3] += dilation
        for first in range(4):
            product = weight*coefficient[first]*values[index+first]
            for second in range(4):
                if second!=first:
                    change = product/(points[first]-points[second])
                    shape[index+first] -= change
                    shape[index+second] += change
    shape -= jump*field*(native>data['source'])
    shape += load*data['beta_radial']
    gradient = np.r_[atom['slope_left'][:1],(atom['slope_right'][:-1]+atom['slope_left'][1:])/2,atom['slope_right'][-1:]][engine.native_edges]
    return dict(field=field,shape=shape,native=native,values=data['field'][indices],beta=data['beta'],mean=gradient,jump=jump,image=image)


def main():
    kernel = ctypes.windll.kernel32
    kernel.GetCurrentProcess.restype = ctypes.c_void_p
    kernel.SetProcessAffinityMask.argtypes = [ctypes.c_void_p,ctypes.c_size_t]
    if not kernel.SetProcessAffinityMask(kernel.GetCurrentProcess(),1<<2):
        raise OSError('Affinity failed')
    evidence = EvidenceRun('annular-native-transmission-material-attempt01',__file__)
    started,deadline = perf_counter(),perf_counter()+3600
    try:
        prior = verify_report(evidence,'source-intake/navier-stokes/20260914/annular-native-interface-transmission-attempt01/status.json')
        evidence.check('transmission_probe_complete',prior['state']=='complete')
        parent_path = evidence.output.parent/'annular-source-flat-native-integrity-20261002.json'
        evidence.own(parent_path)
        digests = dict(json.loads(parent_path.read_text())['hashes'])
        labels = np.unique(np.r_[np.linspace(-.5,.5,33),np.polynomial.legendre.leggauss(32)[0]/2])
        for level in ['fine','third']:
            construction = verify_report(evidence,'source-intake/navier-stokes/20260914/annular-quadratic-core-state-'+level+'-attempt01/status.json')
            for category in ['inputs','outputs']:
                digests.update(construction[category])
            state = read_archive(evidence.root/construction['primary_state_path'])
            packet = json.loads((evidence.root/construction['packet_path']).read_text())
            central = next(row for row in prior['cases'] if row['level']==level)
            central_archive = read_archive(evidence.root/central['path'])
            active = central_archive['active']
            with localcontext() as context:
                context.prec = 64
                unused,old_action,sources = restore_case(evidence,digests,'MTS-primary',level,deadline)
                loads,action = restore_refined(old_action.owner,state,packet['mesh'],packet,'primary',deadline)
                engine = NativeKernel(action.mesh,packet['gram_support'],True)
                for label in [-.41,0.,.37]:
                    data = physical_data(engine,loads,action,label)
                    compact = point_covectors(engine,data)
                    full = engine.evaluate(data['edges'],data['field'],data['beta'])
                    indices = np.r_[engine.indices[:,0],engine.indices[-1,2]][engine.native_edges]
                    full_field = full['field_gradient'][indices]
                    full_shape = full['edge_gradient'][engine.native_edges]+full['load']*data['beta_radial']
                    errors = {}
                    for name,value,expected in [('field',compact['field'],full_field),('shape',compact['shape'],full_shape)]:
                        errors[name] = float(maximum((value-expected)[active])/max(maximum(expected[active]),Decimal('1e-40')))
                    evidence.check(level+':compact_active_covectors:'+str(label),max(errors.values())<2e-24,errors)
                field_rows,shape_rows,means,energy_rows,jets = [],[],[],[],[]
                exact_zeros = []
                nodes,weights = np.polynomial.legendre.leggauss(12)
                for count,label in enumerate(labels):
                    if perf_counter()>deadline:
                        raise RuntimeError('Safe material survey boundary')
                    data = physical_data(engine,loads,action,float(label))
                    row = point_covectors(engine,data)
                    target = row['mean'].copy()
                    for index in np.flatnonzero(active):
                        if row['field'][index]==0:
                            if row['shape'][index]!=0:
                                exact_zeros.append(dict(label=float(label),knot=int(index),C=str(row['shape'][index])))
                        else:
                            target[index] = -row['shape'][index]/row['field'][index]
                    field_rows.append(np.asarray(row['field'],float))
                    shape_rows.append(np.asarray(row['shape'],float))
                    means.append(np.asarray(target,float))
                    native,values = np.asarray(row['native'],float),np.asarray(row['values'],float)
                    left = np.asarray(target-row['field']/(2*row['beta']),float)
                    right = np.asarray(target+row['field']/(2*row['beta']),float)
                    split = np.unique(np.r_[native,action.solver.edges])
                    split = split[(split>=native[0])&(split<=native[-1])]
                    radii = ((split[:-1]+split[1:])[:,None]+np.diff(split)[:,None]*nodes[None,:])/2
                    measure = np.diff(split)[:,None]*weights[None,:]/2
                    values_at,gradient,unused = hermite_values(radii.ravel(),native,values,left,right)
                    metric_values,unused = action.solver.values(action.solution,radii.ravel())
                    speed = np.exp(metric_values[1])*np.sqrt(1-2*metric_values[0]/radii.ravel())
                    energy_rows.append(float(measure.ravel()@(radii.ravel()**2*speed*gradient**2/2)))
                    jets.append([float(value[0]) for value in hermite_values(np.array([float(data['source'])]),native,values,left,right)])
                    if count%16==0:
                        evidence.report['progress'] = dict(level=level,labels=count+1,seconds=perf_counter()-started)
                        evidence.save()
                        print(json.dumps(evidence.report['progress']),flush=True)
                field_rows,shape_rows,means = map(np.array,[field_rows,shape_rows,means])
                brackets = np.argwhere((field_rows[:-1]*field_rows[1:]<0)&active[None,:])
                roots = []
                for lower_index,knot in brackets[:4]:
                    lower,upper = float(labels[lower_index]),float(labels[lower_index+1])
                    initial = [lower,upper]
                    low_value = field_rows[lower_index,knot]
                    for repeat in range(40):
                        middle = (lower+upper)/2
                        data = physical_data(engine,loads,action,middle)
                        row = point_covectors(engine,data)
                        value = row['field'][knot]
                        if value==0:
                            lower=upper=middle
                            break
                        if float(value)*low_value>0:
                            lower,low_value = middle,float(value)
                        else:
                            upper = middle
                    roots.append(dict(knot=int(knot),initial_bracket=initial,final_bracket=[lower,upper],
                        last_label=middle,A=str(value),C=str(row['shape'][knot]),interval_certified=False))
                acceleration_record = next(row for row in construction['results'] if row['name']=='primary-16-64')
                acceleration = read_archive(evidence.root/acceleration_record['acceleration_path'])['acceleration']
                material_nodes = action.owner.layer_rule.points/2
                cardinal = np.array([action.cardinal(label).ravel() for label in material_nodes])
                source = cardinal@action.source
                metric_values,metric_derivatives = action.solver.values(action.solution,source)
                speed_square = np.exp(2*metric_values[1])*(1-2*metric_values[0]/source)
                geodesic = -speed_square*metric_derivatives[1]
                geodesic_defect = cardinal@acceleration[:,-1]-geodesic
            evidence.check(level+':finite_survey',all(np.all(np.isfinite(value)) for value in [field_rows,shape_rows,means,energy_rows,jets]))
            evidence.check(level+':source_pin_all_sampled_labels',np.max(abs(np.array(jets)[:,0]))<1e-12)
            central_index = int(np.flatnonzero(labels==0)[0])
            energy_error = abs(energy_rows[central_index]/central['integrals'][-1]['wave_energy']-1)
            evidence.check(level+':independent_central_energy_order',energy_error<2e-8,energy_error)
            archive_path = evidence.output/(level+'-material-survey.npz')
            np.savez_compressed(archive_path,labels=labels,field_load=field_rows,shape_load=shape_rows,target_mean=means,
                wave_energy=energy_rows,source_jets=jets,active=active,geodesic_acceleration=geodesic,
                geodesic_defect=geodesic_defect,material_nodes=material_nodes,brackets=brackets)
            evidence.own(archive_path,'outputs')
            evidence.report['cases'].append(dict(level=level,path=str(archive_path.relative_to(evidence.root)),labels=len(labels),
                sign_change_brackets=len(brackets),exact_zero_nonzero_C=exact_zeros,localized_roots=roots,
                maximum_target_gradient=float(np.max(abs(means))),energy_range=[min(energy_rows),max(energy_rows)],
                max_sampled_source_pin=float(np.max(abs(np.array(jets)[:,0]))),maximum_geodesic_defect=float(np.max(abs(geodesic_defect))),
                continuous_material_nonsingularity_proven=False,live_reconstruction_done=False,valid_for_claim=False))
            evidence.save()
        evidence.report.update(seconds=perf_counter()-started,scope='Frozen-metric material-denominator and energy survey; active native covectors verified against full atom oracle.',github_action=False,subagents_used=False)
        evidence.complete()
    except Exception as error:
        evidence.fail(error)
        raise


if __name__=='__main__':
    main()

from derive_annular_source_gravity_20260914 import EvidenceRun
from derive_annular_support_map_constraints_20260927 import restore_case
from annular_nested_physical_refinement_v3_20260922 import restore_refined
from annular_acceleration_archive_checks_v2_20261001 import verify_report
from annular_physical_native_kernel_20260928 import NativeKernel,maximum
from derive_annular_native_shape_stress_20260928 import physical_data
from analyze_annular_source_flat_state_20261002 import read_archive
from probe_annular_native_transmission_20261002 import hermite_values
from probe_annular_transmission_material_20261002 import point_covectors
from probe_annular_Neumann_kernel_family_20261001 import nodal_radii
from decimal import Decimal,localcontext
from time import perf_counter
import ctypes
import json
import numpy as np


def carrier_field(engine,data):
    native = data['edges'][engine.native_edges]
    fraction = np.array([abs((point-data['source'])/((data['edges'][0] if point<data['source'] else data['edges'][-1])-data['source'])) for point in native],dtype=object)
    support = (fraction>Decimal('.18'))&(fraction<Decimal('.82'))
    values = np.array([Decimal(1 if index%2==0 else -1) if selected else Decimal(0) for index,selected in enumerate(support)],dtype=object)
    radius = nodal_radii(engine,data['edges'])
    interval = np.clip(np.searchsorted(native,radius,side='right')-1,0,len(native)-2)
    coordinate = (radius-native[interval])/(native[interval+1]-native[interval])
    field = values[interval]*(1-coordinate)+values[interval+1]*coordinate
    kernel_support = np.array([np.any(support[index:index+4]) for index in range(len(native)-3)])
    image_support = np.asarray(abs(engine.template)@kernel_support.astype(float)>0).ravel()
    kernel_halo = np.asarray(abs(engine.template).T@image_support.astype(float)>0).ravel()
    active = np.asarray(abs(engine.sampling).T@image_support.astype(float)>0).ravel()
    for index in np.flatnonzero(kernel_halo):
        active[index:index+4] = True
    return field,values,active


def integrate_hermite(action,row,left,right,order):
    native,values = np.asarray(row['native'],float),np.asarray(row['values'],float)
    split = np.unique(np.r_[native,action.solver.edges])
    split = split[(split>=native[0])&(split<=native[-1])]
    nodes,weights = np.polynomial.legendre.leggauss(order)
    radii = ((split[:-1]+split[1:])[:,None]+np.diff(split)[:,None]*nodes[None,:])/2
    measure = np.diff(split)[:,None]*weights[None,:]/2
    field,gradient,unused = hermite_values(radii.ravel(),native,values,np.asarray(left,float),np.asarray(right,float))
    metric_values,unused = action.solver.values(action.solution,radii.ravel())
    speed = np.exp(metric_values[1])*np.sqrt(1-2*metric_values[0]/radii.ravel())
    energy = float(measure.ravel()@(radii.ravel()**2*speed*gradient**2/2))
    norm = float(measure.ravel()@(radii.ravel()**2/speed*field**2))
    return energy,norm


def main():
    kernel = ctypes.windll.kernel32
    kernel.GetCurrentProcess.restype = ctypes.c_void_p
    kernel.SetProcessAffinityMask.argtypes = [ctypes.c_void_p,ctypes.c_size_t]
    if not kernel.SetProcessAffinityMask(kernel.GetCurrentProcess(),1<<2):
        raise OSError('Affinity failed')
    evidence = EvidenceRun('annular-native-carrier-denominator-repair-attempt01',__file__)
    started,deadline = perf_counter(),perf_counter()+3600
    try:
        evidence.own(evidence.root/'DERIVATION-20261002-native-carrier-denominator-repair.md')
        base = 'source-intake/navier-stokes/20260914/'
        survey = verify_report(evidence,base+'annular-native-transmission-material-attempt01/status.json')
        initial = verify_report(evidence,base+'annular-native-interface-transmission-attempt01/status.json')
        evidence.check('prior_surveys_complete',survey['state']==initial['state']=='complete')
        parent_path = evidence.output.parent/'annular-source-flat-native-integrity-20261002.json'
        evidence.own(parent_path)
        digests = dict(json.loads(parent_path.read_text())['hashes'])
        labels = np.unique(np.r_[np.linspace(-.5,.5,33),np.polynomial.legendre.leggauss(32)[0]/2,
            [root['last_label'] for case in survey['cases'] for root in case['localized_roots']]])
        epsilon = None
        for level in ['fine','third']:
            construction = verify_report(evidence,base+'annular-quadratic-core-state-'+level+'-attempt01/status.json')
            for category in ['inputs','outputs']:
                digests.update(construction[category])
            state = read_archive(evidence.root/construction['primary_state_path'])
            packet = json.loads((evidence.root/construction['packet_path']).read_text())
            initial_case = next(row for row in initial['cases'] if row['level']==level)
            original_active = read_archive(evidence.root/initial_case['path'])['active']
            with localcontext() as context:
                context.prec = 64
                unused,old_action,sources = restore_case(evidence,digests,'MTS-primary',level,deadline)
                loads,action = restore_refined(old_action.owner,state,packet['mesh'],packet,'primary',deadline)
                engine = NativeKernel(action.mesh,packet['gram_support'],True)
                training = []
                if epsilon is None:
                    bound = Decimal(0)
                    for label in np.linspace(-.5,.5,17):
                        data = physical_data(engine,loads,action,float(label))
                        row = point_covectors(engine,data)
                        carrier,values,active = carrier_field(engine,data)
                        active |= original_active
                        carrier_data = dict(data,field=carrier)
                        response = point_covectors(engine,carrier_data)
                        zeros = [int(index) for index in np.flatnonzero(active) if response['field'][index]==0]
                        evidence.check('training:nonzero_carrier_covector:'+str(label),not zeros,zeros)
                        ratio = maximum(row['field'][active]/response['field'][active])
                        bound = max(bound,ratio)
                        training.append(dict(label=float(label),maximum_ratio=str(ratio)))
                    epsilon = 2*bound
                    evidence.check('positive_carrier_amplitude',epsilon>0,str(epsilon))
                    evidence.report.update(epsilon=str(epsilon),training=training,amplitude_rule='Twice maximal abs(A0/Ar) on17 fine-grid uniform training labels; no withheld/grid retuning.')
                    evidence.save()
                records = {key:[] for key in ['radius','native_values','field_load','shape_load','target_mean','left','right','beta','dominance_ratio','wave_energy','positive_norm','native_energy','source_jets','local_residual']}
                active_singular,nonpositive_margin = [],[]
                linearity_max = Decimal(0)
                for count,label in enumerate(labels):
                    if perf_counter()>deadline:
                        raise RuntimeError('Safe carrier survey boundary')
                    data = physical_data(engine,loads,action,float(label))
                    original = point_covectors(engine,data)
                    carrier,carrier_native,active = carrier_field(engine,data)
                    active |= original_active
                    response = point_covectors(engine,dict(data,field=carrier))
                    changed_data = dict(data,field=data['field']+epsilon*carrier)
                    row = point_covectors(engine,changed_data)
                    linearity_max = max(linearity_max,maximum(row['field']-original['field']-epsilon*response['field']))
                    denominator = abs(epsilon*response['field'][active])
                    dominance = np.array([float(abs(value)/scale) if scale!=0 else float('inf') for value,scale in zip(original['field'][active],denominator)])
                    if np.max(dominance)>=1:
                        nonpositive_margin.append(float(label))
                    target = row['mean'].copy()
                    for index in np.flatnonzero(active):
                        if row['field'][index]==0:
                            active_singular.append(dict(label=float(label),knot=int(index),C=str(row['shape'][index])))
                        else:
                            target[index] = -row['shape'][index]/row['field'][index]
                    left = target-row['field']/(2*row['beta'])
                    right = target+row['field']/(2*row['beta'])
                    residual = row['field']*target+row['shape']
                    energy,norm = integrate_hermite(action,row,left,right,12)
                    jet = [float(value[0]) for value in hermite_values(np.array([float(data['source'])]),np.asarray(row['native'],float),np.asarray(row['values'],float),np.asarray(left,float),np.asarray(right,float))]
                    native_energy = sum(engine.apply('sampling',row['beta'])*row['image']**2/2,Decimal(0))
                    for name,value in [('radius',row['native']),('native_values',row['values']),('field_load',row['field']),('shape_load',row['shape']),('target_mean',target),('left',left),('right',right),('beta',row['beta'])]:
                        records[name].append(np.asarray(value,float))
                    for name,value in [('dominance_ratio',np.max(dominance)),('wave_energy',energy),('positive_norm',norm),('native_energy',float(native_energy)),('source_jets',jet),('local_residual',float(maximum(residual)))]:
                        records[name].append(value)
                    if label==0:
                        full = engine.evaluate(changed_data['edges'],changed_data['field'],changed_data['beta'])
                        indices = np.r_[engine.indices[:,0],engine.indices[-1,2]][engine.native_edges]
                        full_shape = full['edge_gradient'][engine.native_edges]+full['load']*data['beta_radial']
                        oracle_error = max(maximum((full['field_gradient'][indices]-row['field'])[active]),maximum((full_shape-row['shape'])[active]))
                        evidence.check(level+':full_atom_carrier_oracle',oracle_error<Decimal('1e-35'),str(oracle_error))
                        high_energy,high_norm = integrate_hermite(action,row,left,right,24)
                        evidence.check(level+':central_energy_quadrature',abs(energy/high_energy-1)<2e-8)
                        exact_path = evidence.output/(level+'-central-exact.npz')
                        np.savez_compressed(exact_path,**{name:np.asarray(value,str) for name,value in dict(radius=row['native'],values=row['values'],A=row['field'],C=row['shape'],beta=row['beta'],mean=target,left=left,right=right,original_A=original['field'],carrier_A=response['field'],carrier_values=carrier_native,original_values=original['values']).items()},active=active)
                        evidence.own(exact_path,'outputs')
                    if count%16==0:
                        evidence.report['progress'] = dict(level=level,labels=count+1,seconds=perf_counter()-started)
                        evidence.save()
                        print(json.dumps(evidence.report['progress']),flush=True)
                evidence.check(level+':exact_field_linearity',linearity_max<Decimal('1e-35'),str(linearity_max))
                evidence.check(level+':finite_archives',all(np.all(np.isfinite(value)) for value in records.values()))
                evidence.check(level+':source_pin_preserved',np.max(abs(np.array(records['source_jets'])[:,0]))<1e-12)
                evidence.check(level+':endpoint_flux_preserved',np.max(abs(np.array(records['left'])[:,[0,-1]]))+np.max(abs(np.array(records['right'])[:,[0,-1]]))<1e-15)
                path = evidence.output/(level+'-carrier-survey.npz')
                np.savez_compressed(path,labels=labels,active=active,epsilon=np.array(str(epsilon)),**records)
                evidence.own(path,'outputs')
                central_index = int(np.flatnonzero(labels==0)[0])
                evidence.report['cases'].append(dict(level=level,path=str(path.relative_to(evidence.root)),exact_path=str(exact_path.relative_to(evidence.root)),labels=len(labels),
                    epsilon=str(epsilon),max_sampled_dominance_ratio=float(max(records['dominance_ratio'])),active_singular=active_singular,
                    labels_failing_dominance=nonpositive_margin,maximum_target_gradient=float(np.max(abs(records['target_mean']))),
                    maximum_point_residual=max(records['local_residual']),energy_range=[min(records['wave_energy']),max(records['wave_energy'])],
                    norm_range=[min(records['positive_norm']),max(records['positive_norm'])],native_energy_range=[min(records['native_energy']),max(records['native_energy'])],
                    central_wave_energy_ratio=records['wave_energy'][central_index]/initial_case['integrals'][-1]['old_wave_energy'],
                    sampled_nonzero_denominators=not active_singular and not nonpositive_margin,
                    continuous_material_bound_proven=False,own_metric_recomputed=False,source_acceleration_recomputed=False,valid_for_claim=False))
                evidence.save()
        evidence.report.update(seconds=perf_counter()-started,github_action=False,subagents_used=False,scope='Explicit changed native values; frozen-metric transmission and energy construction, not force regularization.')
        evidence.complete()
    except Exception as error:
        evidence.fail(error)
        raise


if __name__=='__main__':
    main()

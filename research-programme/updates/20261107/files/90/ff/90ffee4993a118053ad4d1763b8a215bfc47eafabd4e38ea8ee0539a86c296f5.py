from common import *
from source_adapter import dense_values
from extend import make_rhs,observables
from thermal_candidate import Thermal
from summarize import independent_algebra,comparison_samples
from phase_math import symbolic
import numpy as np
import csv


def main():
    modest()
    check_parent()
    require(read(ROOT/'split-01.end.json')['exit_code']==0,'completed split repair')
    for phase in ('inventory-01','validation-01'):
        require(read(ROOT/(phase+'.end.json'))['exit_code']==1,'historical failed gate retained')
    require(not (ROOT/'inventory/result.json').exists() and not (ROOT/'summary/result.json').exists(),'no relabelling of failures')
    destination=ROOT/'final-validation'
    destination.mkdir(exist_ok=False)
    freeze=read(ROOT/'extension/freeze.json')
    for manifest in (freeze['sources'],read(ROOT/'thermal-qualification/result.json')['source_hashes'],read(ROOT/'split-envelope/freeze.json')['sources']):
        for path,expected in manifest.items():
            require(digest(path)==expected,'immutable source '+path)
    for path,expected in read(ROOT/'thermal-qualification/protocol.json')['source_files'].items():
        require(digest(path)==expected,'defining thermal source')
    for path in ROOT.glob('*.py'):
        compile(path.read_text(),str(path),'exec')
    algebra=dict(phase=symbolic(),canonical=independent_algebra(),comparison= comparison_samples())
    rows=[]
    reports=[]
    for model in ('heavy','cold'):
        configuration=freeze['configurations'][model]
        require(digest(configuration['accepted_path'])==configuration['accepted_sha256'],'accepted data unchanged')
        parameters=configuration['thermal_parameters']
        require(all(parameters[name]>0 for name in ('cdm','baryon','photon','massless')),'positive standard species')
        require(all(value>0 for value in parameters['masses']+parameters['coefficients']),'positive massive source')
        thermal=Thermal(parameters)
        rhs=make_rhs(configuration,thermal)
        directory=ROOT/'split-envelope' if model=='heavy' else ROOT/'extension/cold'
        packets={}
        dense_reports=[]
        fine_dense=None
        for label in ('base','fine','independent'):
            dense=load(directory/(label+'-dense.npz'))
            packet=load(directory/(label+'.npz'))
            packets[label]=packet
            indices=np.unique(np.linspace(0,len(dense['segment_start'])-1,97,dtype=int))
            points=dense['segment_start'][indices]+.3819660112501051*(dense['segment_end'][indices]-dense['segment_start'][indices])
            states,derivatives=dense_values(dense,points)
            expected=np.asarray([rhs(float(point),state) for point,state in zip(points,states)])
            scales=np.maximum(np.max(abs(expected),axis=0),1e-15)
            discrepancy=float(np.max(abs(derivatives-expected)/scales[None,:]))
            require(discrepancy<GATE,'dense derivative unchanged gate '+model+' '+label)
            recovered,_=dense_values(dense,packet['efold'])
            value_error=float(np.max(abs(recovered-packet['states']))/max(float(np.max(abs(packet['states']))),1.))
            require(value_error<ALGEBRA,'serialized values')
            dense_reports.append(dict(label=label,off_node_points=len(points),normalized_derivative_error=discrepancy,value_recovery_error=value_error))
            if label=='fine':
                fine_dense=dense
        comparisons=[]
        for label in ('base','independent'):
            for quantity in ('hubble','slow_coordinates','clock','slow_error_radius','hubble_error','clock_error'):
                expected=packets['fine'][quantity]
                discrepancy=float(np.max(abs(packets[label][quantity]-expected))/max(float(np.max(abs(expected))),1e-100))
                require(discrepancy<GATE,'unchanged refinement gate')
                comparisons.append(dict(label=label,quantity=quantity,error=discrepancy))
        packet=packets['fine']
        selected=packet['a']>=freeze['target']['scale_start']*(1-1e-12)
        uncertainty=dict(hubble=float(np.max(packet['hubble_error'][selected]/packet['hubble'][selected])),
                         slow_energy_coordinates=float(np.max(packet['slow_error_radius'][selected]/np.linalg.norm(packet['slow_coordinates'][selected],axis=1))),
                         clock=float(np.max(packet['clock_error'][selected]/packet['clock'][selected])),
                         heavy_log_density=float(np.max(packet['heavy_log_width'][selected])))
        require(max(uncertainty.values())<GATE,'unchanged cold uncertainty gate')
        replay=load(ROOT/'extension'/model/'resolved-replay.npz')
        replay_states,_=dense_values(fine_dense,replay['efold'])
        mean=observables(configuration,thermal,replay['efold'],replay_states)
        slow_excess=float(np.max((np.linalg.norm(replay['coordinates'][:,0]-mean['slow_coordinates'],axis=1)-mean['slow_error_radius'])/np.maximum(np.linalg.norm(replay['coordinates'][:,0],axis=1),configuration['slow_unit'])))
        hubble_excess=float(np.max((abs(replay['hubble']-mean['hubble'])-mean['hubble_error'])/replay['hubble']))
        clock_excess=float(np.max((abs(replay['clock']-mean['clock'])-mean['clock_error'])/replay['clock']))
        require(max(slow_excess,hubble_excess,clock_excess)<ALGEBRA,'reused direct replay enclosure')
        for endpoint in ('scale_start','scale_end'):
            scale=freeze['target'][endpoint]
            index=int(np.argmin(abs(packet['a']-scale)))
            require(abs(packet['a'][index]/scale-1)<ALGEBRA,'frozen endpoint')
            momenta=next(item for item in freeze['target']['models'] if item['model']==model)['momentum_mass_ratio']
            speeds=1/np.sqrt(1+(scale/np.asarray(momenta))**2)
            require(speeds.max()<=.1+ALGEBRA,'cold represented nodes')
            rows.append(dict(model=model,endpoint=endpoint,a=float(packet['a'][index]),redshift=float(1/packet['a'][index]-1),
                             conformal_hubble_Mpc_inv=float(packet['hubble'][index]),hubble_bound_Mpc_inv=float(packet['hubble_error'][index]),
                             conformal_clock_Mpc=float(packet['clock'][index]),clock_bound_Mpc=float(packet['clock_error'][index]),
                             heavy_mean_density_Mpc_inv2=float(packet['heavy_mean'][index]),heavy_log_density_width=float(packet['heavy_log_width'][index]),
                             max_represented_speed=float(speeds.max())))
        reports.append(dict(model=model,authoritative_directory=str(directory),max_refinement_error=max(item['error'] for item in comparisons),
                            comparisons=comparisons,dense_checks=dense_reports,cold_uncertainty=uncertainty,
                            reused_replay_points=len(replay['efold']),replay_slow_excess=slow_excess,replay_hubble_excess=hubble_excess,replay_clock_excess=clock_excess))
        print(model,'refinement',reports[-1]['max_refinement_error'],'dense',max(item['normalized_derivative_error'] for item in dense_reports),'uncertainty',uncertainty,flush=True)
    with (destination/'cold-endpoints.csv').open('x',newline='',encoding='utf-8') as stream:
        writer=csv.DictWriter(stream,fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)
    with (destination/'cold-endpoints.csv').open(newline='',encoding='utf-8') as stream:
        require(len(list(csv.DictReader(stream)))==4,'CSV round trip')
    check_parent()
    write(destination/'result.json',dict(state='validated_cold_background_candidate',passed=True,reports=reports,algebra=algebra,
                                        failed_inventory_preserved=True,failed_unsplit_validation_preserved=True,
                                        tolerances_unchanged=True,cold_target_unchanged=True,scattering_bank_changed=False,new_observational_fits=0,
                                        late_exact_scalar_phase_available=False,formal_interval_arithmetic_certificate=False,
                                        physical_ode_segments=14,source_hashes=frozen_sources()))


if __name__=='__main__':
    main()

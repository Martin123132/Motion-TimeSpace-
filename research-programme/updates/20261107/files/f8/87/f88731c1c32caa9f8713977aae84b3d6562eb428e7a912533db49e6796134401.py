import argparse
from initial_state import *
from diagnostics import *


def collision_frozen(system,states,background):
    output=np.zeros_like(states)
    for index,state in enumerate(states):
        parts=system.unpack(state)
        mean=collision.mean_matrix(system.weights,parts['photon'])
        radiation=background['opacity']*(1.5*system.screen@mean@system.screen-parts['photon']+2*(system.directions@parts['velocity'])[:,None,None]*system.screen)
        flux=system.angular.moments(parts['photon'])[1]
        velocity=background['opacity']/background['ratio']*(.75*flux-parts['velocity'])
        output[index,23:26]=velocity
        output[index,26:26+9*system.count]=radiation.ravel()
    return output


def etd_step(system,moment,state,step):
    midpoint=system.background.at(moment+step/2)
    depth=midpoint['opacity']*step
    ratio=midpoint['ratio']
    def remainder(when,values):
        return system.slow_rhs(when,values)+system.collision_rhs(when,values)-collision_frozen(system,values,midpoint)
    first=remainder(moment,state)
    predictor=system.propagate_collision(state,ratio,depth)+step*system.propagate_collision(first,ratio,depth,'phi1')
    second=remainder(moment+step,predictor)
    return predictor+step*system.propagate_collision(second-first,ratio,depth,'phi2')


def compare_native(system,moment,state):
    source=GEOMETRY/'runs/native'/(system.background.label+'.npz')
    packet=np.load(source)
    index=int(np.argmin(abs(packet['modes']-.1)))
    names=list(packet['names'])
    values=packet['values'][index]
    scales=values[:,names.index('a')]
    valid=scales>0
    target=system.background.at(moment)['scale']
    names_to_compare=['delta_cdm','delta_baryon','delta_photon','delta_neutrino','v_photon','v_neutrino']
    reference=np.array([interpolate.CubicSpline(scales[valid],values[valid,names.index(name)])(target) for name in names_to_compare])
    features=observe(system,moment,state)['features'][0]
    predicted=np.r_[features[:4].real,-features[4].imag,-features[7].imag]
    envelope=np.maximum(np.maximum(abs(reference),abs(predicted)),1e-100)
    errors=abs(reference-predicted)/envelope
    return dict(names=names_to_compare,reference=reference.tolist(),predicted=predicted.tolist(),relative_errors=errors.tolist(),maximum_error=float(max(errors)))


def run(label,name,maximum,step_cap,start_scale,end_scale):
    modest()
    folder=ROOT/'runs'/name
    folder.mkdir(parents=True,exist_ok=False)
    started=time.perf_counter()
    write_json(folder/'status.json',dict(state='running',model=label,maximum=maximum,step_cap=step_cap,start_scale=start_scale,end_scale=end_scale,pid=os.getpid()))
    background=Background(label,end_scale=end_scale)
    system=CoupledSystem(background,maximum)
    moment,state,initial=initial_state(system,start_scale)
    end=background.time_at(end_scale)
    targets=np.linspace(moment,end,41)
    times=[]
    features=[]
    constraints=[]
    screens=[]
    compatibility=[]
    wards=[]
    steps=0
    for target in targets:
        while moment<target-1e-13:
            step=min(step_cap,.005*moment,target-moment)
            state=etd_step(system,moment,state,step)
            moment+=step
            steps+=1
            if not np.isfinite(state).all():
                raise FloatingPointError((name,moment,steps))
        observed=observe(system,moment,state)
        times.append(moment)
        features.append(observed['features'])
        constraints.append(observed['constraint_normalized'])
        screens.append(observed['screen_error'])
        compatibility.append([observed['second_metric_symmetry'],observed['second_metric_rate_symmetry']])
        if len(times) in [1,21,41]:
            wards.append(dict(time=moment,**ward_identity(system,moment,state)))
        if len(times)%10==0:
            write_json(folder/'progress.json',dict(samples=len(times),total_samples=41,steps=steps,time=moment,elapsed_seconds=time.perf_counter()-started))
            print(json.dumps(dict(run=name,samples=len(times),elapsed_seconds=time.perf_counter()-started)),flush=True)
    np.savez_compressed(folder/'evolution.npz',times=times,features=features,constraints=constraints,screens=screens,compatibility=compatibility,
        final_state=state,cold_numbers=system.cold_numbers,momenta=system.momenta,start_scale=start_scale,end_scale=end_scale,angular_maximum=maximum,step_cap=step_cap)
    native=compare_native(system,moment,state)
    checks=[dict(name='Native first-order density/flux endpoint',passed=native['maximum_error']<.002,value=native['maximum_error'],gate=.002),
        dict(name='Hamiltonian and momentum propagation',passed=float(np.max(constraints))<.002,value=float(np.max(constraints)),gate=.002),
        dict(name='Polarization transversality',passed=float(np.max(screens))<1e-9,value=float(np.max(screens)),gate=1e-9),
        dict(name='Mixed-metric compatibility',passed=float(np.max(compatibility))<1e-9,value=float(np.max(compatibility)),gate=1e-9)]
    finish(folder,dict(model=label,run_name=name,initial=initial,steps=steps,elapsed_seconds=time.perf_counter()-started,
        angular_maximum=maximum,step_cap=step_cap,start_scale=start_scale,end_scale=end_scale,
        native_comparison=native,checks=checks,all_checks_passed=all(row['passed'] for row in checks),ward_samples=wards,
        particular_and_primordial_separate=True,ultrarelativistic_neutrinos=True,elastic_cold_thomson=True,pressureless_baryons=True,
        no_constraint_projection_after_initialization=True,observational_fit=False),__file__,
        [ROOT/'coupled_system.py',ROOT/'initial_state.py',ROOT/'diagnostics.py',background.source,GEOMETRY/'runs/native'/(label+'.npz'),COLLISION/'runs/backgrounds'/(label+'.npz')])
    print(json.dumps(dict(run=name,checks=checks,elapsed_seconds=time.perf_counter()-started)),flush=True)


if __name__=='__main__':
    parser=argparse.ArgumentParser()
    parser.add_argument('--model',choices=['heavy','cold'],default='heavy')
    parser.add_argument('--name',required=True)
    parser.add_argument('--maximum',type=int,default=6)
    parser.add_argument('--step',type=float,default=.01)
    parser.add_argument('--start',type=float,default=1e-6)
    parser.add_argument('--end',type=float,default=1e-5)
    arguments=parser.parse_args()
    run(arguments.model,arguments.name,arguments.maximum,arguments.step,arguments.start,arguments.end)

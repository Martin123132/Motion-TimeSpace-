from __future__ import annotations

from collision_common import *


def solve(packet,max_step,polar=16):
    projectors=CollisionProjectors(polar,8)
    directions,weights,screen=projectors.directions,projectors.weights,projectors.screen
    times=packet['times']
    values=packet['values']
    names=list(packet['names'])
    mode=float(packet['mode'])
    _,theta,_,_=inherited.inherited.metric(mode,np.array([0.,0.,1.]),names,values,float(packet['baryon_fraction']))
    shear=-values[:,names.index('H')]*values[:,names.index('v_newtonian_cdm')]
    data=np.column_stack([np.log(packet['opacity']),np.log(packet['ratio']),values[:,names.index('H')],packet['cs2b'],theta,shear])
    spline=interpolate.CubicSpline(times,data)
    initial=values[0]
    mu=directions[:,2]
    pi2=(3*mu**2-1)/2
    baryon=np.array([0.,0.,-1j*initial[names.index('v_baryon_cdm')]])
    delta_b=complex(initial[names.index('delta_baryon')])
    intensity=(initial[names.index('delta_photon')]-3j*initial[names.index('v_photon')]*mu)[:,None,None]*screen/2
    tensor=np.diag([-1/3,-1/3,2/3])
    effective_shear=shear[0]+mode*.75*initial[names.index('v_photon')]
    intensity+=effective_shear/packet['opacity'][0]*(-2*(mu**2-1/3)[:,None,None]*screen+(4/3)*(screen@tensor@screen))
    samples=np.linspace(times[0],times[-1],241)
    output=[]
    def extract():
        scalar=np.trace(intensity,axis1=1,axis2=2)
        return np.array([(weights@scalar).real,(1j*(weights*mu)@scalar).real,
            (-(weights*pi2)@scalar).real,(1j*baryon[2]).real,delta_b.real])
    output.append(extract())
    current=times[0]
    steps=0
    def forcing(moment,radiation,velocity,density):
        _,_,hubble,sound2,volume,anisotropy=spline(moment)
        metric_rate=2*volume/3+2*anisotropy*(mu**2-1/3)
        radiation_source=-1j*mode*mu[:,None,None]*radiation-metric_rate[:,None,None]*screen
        velocity_source=-hubble*velocity+np.array([0.,0.,-1j*mode*sound2*density])
        density_source=-1j*mode*velocity[2]-volume
        return radiation_source,velocity_source,density_source
    for target in samples[1:]:
        while current<target-1e-12:
            step=min(max_step,.02*current,target-current)
            midpoint=current+step/2
            log_opacity,log_ratio,*_=spline(midpoint)
            ratio=math.exp(log_ratio)
            depth=step*math.exp(log_opacity)
            first_r,first_v,first_d=forcing(current,intensity,baryon,delta_b)
            homogeneous_r,homogeneous_v=projectors.apply(intensity,baryon,ratio,depth)
            source_r,source_v=projectors.apply(first_r,first_v,ratio,depth,'phi1')
            predict_r=homogeneous_r+step*source_r
            predict_v=homogeneous_v+step*source_v
            predict_d=delta_b+step*first_d
            last_r,last_v,last_d=forcing(current+step,predict_r,predict_v,predict_d)
            correction_r,correction_v=projectors.apply(last_r-first_r,last_v-first_v,ratio,depth,'phi2')
            intensity=predict_r+step*correction_r
            baryon=predict_v+step*correction_v
            delta_b=predict_d+step*(last_d-first_d)/2
            current+=step
            steps+=1
        output.append(extract())
    return samples,np.array(output),steps


def main():
    modest()
    folder=ROOT/'results/photon-baryon'
    folder.mkdir(parents=True,exist_ok=False)
    report=dict(state='running',pid=os.getpid(),completed=0,total=8)
    write_json(folder/'status.json',report)
    checks=[]
    summaries=[]
    inputs=[]
    columns=['delta_photon','v_photon','pi_photon','v_baryon_cdm','delta_baryon']
    for label in ['heavy','cold']:
        source=ROOT/'runs/backgrounds'/(label+'.npz')
        inputs.append(source)
        packet=np.load(source)
        runs=[]
        for step,polar in [(.1,16),(.05,16),(.025,16),(.025,24)]:
            started=time.monotonic()
            times,values,steps=solve(packet,step,polar)
            names=list(packet['names'])
            native=interpolate.CubicSpline(packet['times'],packet['values'][:,[names.index(name) for name in columns]])(times)
            envelopes=np.maximum(np.max(abs(native),axis=0),1e-10)
            errors=np.max(abs(values-native),axis=0)/envelopes
            path=folder/(label+'-dt'+str(step)+'-angular'+str(polar)+'.npz')
            np.savez_compressed(path,times=times,independent=values,native=native,envelopes=envelopes,errors=errors,columns=columns)
            row=dict(model=label,max_step=step,polar=polar,steps=steps,seconds=time.monotonic()-started,native_errors=errors.tolist())
            summaries.append(row)
            runs.append(values)
            report.update(completed=report['completed']+1,last=row)
            write_json(folder/'status.json',report)
            print(json.dumps(row),flush=True)
        errors=np.max(abs(runs[-1]-native),axis=0)/envelopes
        check_shape=[0,1,3,4]
        checks.extend([dict(name=label+': coupled photon/baryon density and momentum',passed=bool(np.max(errors[check_shape])<.002),errors=errors[check_shape].tolist()),
            dict(name=label+': native polarized photon quadrupole',passed=bool(errors[2]<.005),error=float(errors[2])),
            dict(name=label+': time refinement',passed=bool(np.max(abs(runs[2]-runs[1])/envelopes)<.001),errors=(np.max(abs(runs[2]-runs[1]),axis=0)/envelopes).tolist()),
            dict(name=label+': angular refinement',passed=bool(np.max(abs(runs[3]-runs[2])/envelopes)<1e-5),errors=(np.max(abs(runs[3]-runs[2]),axis=0)/envelopes).tolist())])
    passed=all(row['passed'] for row in checks)
    finish(folder,dict(checks=checks,count=len(checks),all_checks_passed=passed,summaries=summaries,
        exact_collision_eigenmodes_used=True,no_tight_coupling_closure_in_independent_solver=True,
        solved='linear coupled polarized photon transport and baryon density/velocity on prescribed native metric',
        native_background_opacity_and_barotropic_sound_speed_used=True,
        primordial_second_order_evolution_completed=False,normalization_fitted=False,
        initial_quadrupole_from_derived32_over45=True),__file__,inputs)
    assert passed,checks


if __name__=='__main__':
    main()

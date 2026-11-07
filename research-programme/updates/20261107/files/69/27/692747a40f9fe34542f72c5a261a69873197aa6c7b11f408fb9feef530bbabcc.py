from __future__ import annotations

import traceback
from scipy.special import eval_legendre
from constraint_common import *


def response(mode,times,volume_rate,shear_rate,initial,nodes,thin=1):
    selected=np.unique(np.r_[np.arange(0,len(times),thin),len(times)-1])
    spline=interpolate.CubicSpline(times[selected],np.column_stack([volume_rate,shear_rate])[selected])
    angles,weights=np.polynomial.legendre.leggauss(nodes)
    field=sum(((-1j)**order)*(2*order+1)*initial[order]*eval_legendre(order,angles) for order in range(4))
    def derivative(moment,state):
        volume,shear=spline(moment)
        return -1j*mode*angles*state-4*volume/3-4*shear*(angles**2-1/3)
    solution=integrate.solve_ivp(derivative,(times[0],times[-1]),field,method='DOP853',
        rtol=2e-9,atol=2e-11,t_eval=times,max_step=.35/mode)
    assert solution.success,solution.message
    moments=np.array([((1j)**order)*(weights*eval_legendre(order,angles))@solution.y/2 for order in range(4)]).T
    assert np.max(abs(moments.imag))<1e-9
    return moments.real,solution.nfev


def main():
    modest()
    folder=ROOT/'results/neutrino-response'
    folder.mkdir(parents=True,exist_ok=False)
    report=dict(state='running',pid=os.getpid(),completed=0,total=6)
    write_json(folder/'status.json',report)
    inputs=[]
    checks=[]
    summaries=[]
    try:
        for label in ['heavy','cold']:
            source=ROOT/'runs/native'/(label+'.npz')
            inputs.append(source)
            packet=np.load(source)
            times=packet['conformal_time']
            names=list(packet['names'])
            fb=float(packet['baryon_fraction'])
            density_ratio=(7/8)*(4/11)**(4/3)*float(packet['effective_neutrino_number'])
            neutrino_fraction=density_ratio/(1+density_ratio)
            for index,mode in enumerate(packet['modes']):
                started=time.monotonic()
                values=packet['values'][index]
                _,volume_rate,_,_=inherited.metric(mode,np.array([1.,0.,0.]),names,values,fb)
                shear_rate=-values[:,names.index('H')]*values[:,names.index('v_newtonian_cdm')]
                eta=values[0,names.index('etak')]/mode
                initial=[values[0,names.index('delta_neutrino')],values[0,names.index('v_neutrino')],
                    eta*(4/3)*(mode*times[0])**2/(15+4*neutrino_fraction),
                    eta*(4/21)*(mode*times[0])**3/(15+4*neutrino_fraction)]
                base,nfev_base=response(mode,times,volume_rate,shear_rate,initial,96)
                fine,nfev_fine=response(mode,times,volume_rate,shear_rate,initial,160)
                coarse,nfev_coarse=response(mode,times,volume_rate,shear_rate,initial,160,thin=2)
                native=values[:,[names.index('delta_neutrino'),names.index('v_neutrino')]]
                envelopes=np.maximum(np.max(abs(native),axis=0),1e-10)
                native_errors=np.max(abs(fine[:,:2]-native),axis=0)/envelopes
                angular_envelopes=np.maximum(np.max(abs(fine),axis=0),1e-10)
                angle_errors=np.max(abs(base-fine),axis=0)/angular_envelopes
                time_errors=np.max(abs(coarse-fine),axis=0)/angular_envelopes
                checks.extend([
                    dict(name=label+' k='+str(mode)+': native density/momentum agreement',passed=bool(np.max(native_errors)<.0015),errors=native_errors.tolist()),
                    dict(name=label+' k='+str(mode)+': angular96/160 convergence',passed=bool(np.max(angle_errors)<1e-6),errors=angle_errors.tolist()),
                    dict(name=label+' k='+str(mode)+': source-grid refinement',passed=bool(np.max(time_errors)<.001),errors=time_errors.tolist())])
                np.savez_compressed(folder/(label+'-'+str(mode)+'.npz'),times=times,scale=values[:,names.index('a')],
                    independent_moments=fine,angular96_moments=base,coarse_time_moments=coarse,native_density_momentum=native,
                    initial_moments=initial,envelopes=envelopes,volume_rate=volume_rate,shear_rate=shear_rate)
                summary=dict(model=label,mode=float(mode),native_errors=native_errors.tolist(),angular_errors=angle_errors.tolist(),
                    time_errors=time_errors.tolist(),nfev=[nfev_base,nfev_fine,nfev_coarse],elapsed_seconds=time.monotonic()-started)
                summaries.append(summary)
                report.update(completed=report['completed']+1,last_result=summary)
                write_json(folder/'status.json',report)
                print(json.dumps(summary),flush=True)
        passed=all(row['passed'] for row in checks)
        finish(folder,dict(checks=checks,count=len(checks),all_checks_passed=passed,summaries=summaries,
            solved='linear massless-neutrino directional transport on supplied native metric',
            independent_quadrupole_and_octupole_generated=True,native_comparison_moments=['density','momentum'],
            no_normalization_fit=True,same_tests_on_heavy_and_cold=True,primordial_initial_error_order='quadrupole O(matter/radiation*(k*tau_i)^2), omitted ell>=4 O((k*tau_i)^4)',
            massive_and_photon_collision_response_not_numerically_solved=True),__file__,inputs)
        assert passed,checks
    except BaseException as error:
        if not (folder/'COMPLETE').exists():
            report.update(state='failed',error=repr(error),traceback=traceback.format_exc())
            write_json(folder/'status.json',report)
        raise


if __name__=='__main__':
    main()

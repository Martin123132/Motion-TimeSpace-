from __future__ import annotations

import traceback
from onset_common import *


def main():
    modest()
    folder=ROOT/'results/native-comparison'
    folder.mkdir(parents=True,exist_ok=False)
    rows=[]
    extra=[]
    waves=np.array([.0001,.0002,.0004,.001,.03])
    query=np.unique(np.r_[np.linspace(math.log(1e-6),FINAL,181),np.log(np.linspace(.00018,.000265,1601))])
    scales=np.exp(query)
    names=camb.model.evolve_names
    try:
        for label in ['heavy','cold','lcdm']:
            source,native=native_for(label)
            packet_path=ROOT/'runs'/(label+'-base')/'trajectory.npz'
            packet=np.load(packet_path)
            calculated=interpolate.CubicSpline(packet['efold'],packet['values'],axis=1)(query)
            saved={name:calculated[index] for index,name in enumerate(packet['names'])}
            times=native.conformal_time(1/scales-1,tol=1e-10)
            native_values=native.get_time_evolution(waves,times,vars=names,lAccuracyBoost=4)
            assert np.isfinite(native_values).all()
            actual_scale=native_values[:,:,names.index('a')]
            assert np.all(actual_scale>0),'Native query skipped pre-initialization outputs'
            assert np.max(abs(actual_scale/scales-1))<1e-6
            path=folder/(label+'.npz')
            np.savez_compressed(path,waves=waves,scales=scales,times=times,names=names,values=native_values,derived_names=packet['names'],derived_values=calculated)
            for index,wave in enumerate(waves):
                eta=native_values[index,:,names.index('etak')]/wave
                zeta=-eta[0]/(1-wave**2*(saved['b'][0]-8*saved['s'][0])/6)
                predictions={'cold':(-4*wave**2*zeta*saved['s'],'delta_cdm'),
                    'photon':(-16*wave**2*zeta*saved['s']/3,'delta_photon'),
                    'eta':(zeta*(-1+wave**2*(saved['b']-8*saved['s'])/6),'etak')}
                for suffix in (['s','h'] if label=='heavy' else ['s'] if label=='cold' else []):
                    predictions['field_'+suffix]=(4*wave**2*zeta*saved['f_'+suffix],'mts_dphi_'+suffix)
                for quantity,(predicted,key) in predictions.items():
                    actual=native_values[index,:,names.index(key)]
                    if quantity=='eta':
                        actual=actual/wave
                    envelope=max(float(max(abs(actual))),float(max(abs(predicted))),1e-90)
                    error=float(max(abs(actual-predicted))/envelope)
                    early=scales<.00005
                    early_error=float(max(abs(actual[early]-predicted[early]))/max(max(abs(actual[early])),max(abs(predicted[early])),1e-90))
                    rows.append(dict(branch=label,k_Mpc_inverse=float(wave),quantity=quantity,
                        envelope_relative_error=error,early_envelope_error=early_error,
                        primary=bool(wave<=.0004),qualified=bool(error<.01),
                        max_k_tau=float(wave*times[-1]),zeta_from_eta=float(zeta)))
            extra.extend([source,packet_path,path])
            print(json.dumps(dict(branch=label,primary_max_error=max(row['envelope_relative_error'] for row in rows if row['branch']==label and row['primary']))),flush=True)
        finish(folder,dict(rows=rows,all_primary_passed=all(row['qualified'] for row in rows if row['primary']),
            primary_gate=.01,normalization='Single early eta normalization; no density or field fitting.',
            native_library_modified=False),__file__,extra+[NATIVE/'camb/cambdll.dll'])
    except BaseException as error:
        write_json(folder/'status.json',dict(state='failed',error=repr(error),traceback=traceback.format_exc()))
        raise


if __name__=='__main__':
    main()

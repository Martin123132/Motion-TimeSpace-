from common225 import *
import gravity225 as original

def main():
    config=protocol()
    background=gravity.ThermalBackground('heavy')
    first,last=np.array(config['spans']['known_window'])*math.log(10)
    reports=[]
    for name in config['probes']:
        def rhs(coordinate,values):
            parts=model_parts(background,coordinate)
            return parts['operator']@values+parts['forcing']*original.probe(name,coordinate,first,last)[0]
        solved=integrate.solve_ivp(rhs,(first,last),np.zeros(4),method='DOP853',rtol=3e-11,atol=1e-40,
            max_step=.005,dense_output=True)
        report=dict(probe=name,success=bool(solved.success),message=solved.message,initial_coordinate=float(first),
            final_coordinate=float(solved.t[-1]),evaluations=int(solved.nfev),saved_steps=len(solved.t),
            initial_forcing=rhs(first,np.zeros(4)).tolist(),frozen_original_sha256=digest(ROOT/'gravity225.py'),
            source_files_changed=False,finished_at=now())
        reports.append(report)
        save(ROOT/f'results/original-probe-{name}.npz',coordinate=solved.t,state=solved.y)
        print(json.dumps(report),flush=True)
    write(ROOT/'results/original-probe-diagnosis.json',dict(probes=reports,original_error_log=str(ROOT/'gravity.err.log')))

if __name__=='__main__':
    parent.old.source.modest()
    main()

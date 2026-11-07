from stage165_common import *
from stable_phase_sources import StablePhaseSources
from assemble_repair import decimal_array


def compensated_moment(temperature,values):
    result=[]
    for column in range(values.shape[1]):
        products=[float(temperature[index])*float(values[index+1,column]) for index in range(2)]
        errors=[math.fma(float(temperature[index]),float(values[index+1,column]),-products[index]) for index in range(2)]
        result.append(math.fsum([*products,*errors,-float(values[0,column])]))
    return np.asarray(result)


def main():
    modest()
    folder=ROOT/'results/phase-rounding-diagnosis'
    folder.mkdir(parents=True,exist_ok=False)
    previous=verify_packet(ROOT/'results/reference-stable')
    evaluator=StablePhaseSources()
    checks,records=[],{}
    with localcontext() as context:
        context.prec=80
        temperature=decimal_array(evaluator.data['temperature'][:2])
        for step in ['54','65','64']:
            worst={key:dict(relative=-1.) for key in ['original_dot','compensated_dot','exact_rounded_inputs','exact_unrounded_inputs']}
            maximum_agreement=0.
            for phase in np.linspace(0,1,2049):
                values,exact=evaluator.physical(phase,'cubic','terminal',step)
                rounded=decimal_array(values[[0,1,2,97]])
                original=evaluator.data['temperature']@values[1:-1]-values[0]
                accurate=compensated_moment(evaluator.data['temperature'],values)
                exact_rounded=temperature@rounded[1:3]-rounded[0]
                exact_unrounded=temperature@exact[1:3]-exact[0]
                maximum_agreement=max(maximum_agreement,float(max(abs(accurate-np.asarray(exact_rounded,dtype=float))/np.maximum(abs(values[0]),1e-300))))
                for name,defect in [('original_dot',original),('compensated_dot',accurate),('exact_rounded_inputs',np.asarray(exact_rounded,dtype=float)),('exact_unrounded_inputs',np.asarray(exact_unrounded,dtype=float))]:
                    ratios=abs(defect)/np.maximum(abs(values[0]),1e-300)
                    column=int(np.argmax(ratios))
                    if ratios[column]>worst[name]['relative']:
                        worst[name]=dict(relative=float(ratios[column]),phase=float(phase),column=column,energy=float(values[0,column]),defect=float(defect[column]))
            records[step]=worst
            test(checks,'Compensated dot matches80digit rounded-input predicate:'+step,maximum_agreement,1e-10)
            close(checks,'Reproduce stable phase dot:'+step,np.array([worst['original_dot']['relative']]),
                np.array([previous['phase_records']['terminal-cubic'][step+'_moment']]),1e-10)
    finish(folder,dict(checks=checks,records=records,source_changed=False,source_adopted=False,
        all_compensated_rounded_checks_pass=all(record['compensated_dot']['relative']<1e-10 for record in records.values())),__file__,
        [ROOT/'results/reference-stable/status.json',*evaluator.inputs])
    print(json.dumps(dict(checks=checks,records=records)),flush=True)


if __name__=='__main__':
    main()

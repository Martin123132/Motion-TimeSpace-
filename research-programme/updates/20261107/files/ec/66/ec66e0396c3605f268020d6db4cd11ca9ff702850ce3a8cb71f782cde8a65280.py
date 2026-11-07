from common import *
from source_adapter import dense_values
from extend import make_rhs
from thermal_candidate import Thermal
import numpy as np


def main():
    modest()
    check_parent()
    destination=ROOT/'dense-diagnosis'
    destination.mkdir(exist_ok=False)
    frozen=read(ROOT/'extension/freeze.json')
    rows=[]
    for model,configuration in frozen['configurations'].items():
        rhs=make_rhs(configuration,Thermal(configuration['thermal_parameters']))
        for label in ('base','fine','independent'):
            packet=load(ROOT/'extension'/model/(label+'-dense.npz'))
            indices=np.unique(np.linspace(0,len(packet['segment_start'])-1,97,dtype=int))
            widths=packet['segment_end'][indices]-packet['segment_start'][indices]
            points=packet['segment_start'][indices]+.3819660112501051*widths
            states,derivatives=dense_values(packet,points)
            expected=np.asarray([rhs(float(point),state) for point,state in zip(points,states)])
            scales=np.maximum(np.max(abs(expected),axis=0),1e-15)
            difference=abs(derivatives-expected)/scales[None,:]
            worst=np.unravel_index(np.argmax(difference),difference.shape)
            selected=worst[0]
            values=load(ROOT/'extension'/model/(label+'.npz'))
            recovered,_=dense_values(packet,values['efold'])
            recovery=float(np.max(abs(values['states']-recovered)))
            row=dict(model=model,label=label,maximum=float(difference[worst]),column=int(worst[1]),efold=float(points[selected]),
                     interval_width=float(widths[selected]),state=states[selected].tolist(),derivative=derivatives[selected].tolist(),
                     rhs=expected[selected].tolist(),normalization=scales.tolist(),maximum_by_column=difference.max(axis=0).tolist(),
                     polynomial_value_recovery_error=recovery)
            np.savez_compressed(destination/(model+'-'+label+'.npz'),efold=points,states=states,derivative=derivatives,rhs=expected,normalization=scales)
            rows.append(row)
            print(model,label,'worst',row['maximum'],'column',row['column'],'N',row['efold'],'value recovery',recovery,flush=True)
    write(destination/'result.json',dict(state='read_only_dense_diagnosis',no_new_ode_solves=True,reports=rows,failed_validator_preserved=True))


if __name__=='__main__':
    main()

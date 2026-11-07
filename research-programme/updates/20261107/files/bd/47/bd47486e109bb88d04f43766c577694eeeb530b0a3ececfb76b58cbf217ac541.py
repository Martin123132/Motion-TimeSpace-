import predict_turnover as runner
from turnover_common import *


original_measure=runner.measure_prediction


def lower_target_readout(basis,solution,baseline,window):
    minimum=float(solution['frequency'][0])
    if minimum<=basis.minimum:
        return original_measure(basis,solution,baseline,window)
    spacing=math.log(solution['frequency'][1]/minimum)
    count=int(math.ceil(math.log(minimum/basis.minimum)/spacing))
    extra_frequency=np.exp(np.linspace(math.log(basis.minimum),math.log(minimum),count+1))[:-1]
    assert len(extra_frequency)>0
    model=sys.argv[sys.argv.index('--model')+1]
    assert model in ['heavy','cold']
    background=thermal_wave.thermal.ThermalBackground(model)
    free_free=FreeFree(background,extra_frequency)
    driver,unused=make_drivers(basis,baseline,window,np.array([.2]),.1)
    extra_slopes=[]
    for coordinate in solution['coordinate']:
        theta=background.at(float(coordinate))['thermal_parameter']
        dc=tail.integrated_dc.DC_CONSTANT*theta**2/extra_frequency**2
        br=free_free.br_rates(theta)
        values=driver(float(coordinate))
        gas,hard=values[0],values[1]
        extra_slopes.append((dc[:,None]*hard+br[:,None]*gas)/(dc+br)[:,None])
    extension=np.array(extra_slopes)
    readout_solution=dict(solution)
    readout_solution['frequency']=np.r_[extra_frequency,solution['frequency']]
    for key in ['slope','source_target','first_correction']:
        readout_solution[key]=np.concatenate([extension,solution[key]],axis=1)
    metrics,outputs=original_measure(basis,readout_solution,baseline,window)
    metrics['below_mesh_hybrid_readout']='Derived gas/hard source target;no saved low-frequency future.'
    return metrics,outputs


if __name__=='__main__':
    runner.measure_prediction=lower_target_readout
    runner.main()

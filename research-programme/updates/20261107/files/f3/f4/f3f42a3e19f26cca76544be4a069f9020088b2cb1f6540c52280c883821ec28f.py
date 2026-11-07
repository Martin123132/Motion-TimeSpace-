from repair_common import *
from propagate_matched_feedback import solve_response
import argparse
import time


def readout(basis,prediction,source,solution,upper):
    reader=ShapeReadout(basis,canonical=True)
    raw=compact_defect(basis.nodes,prediction['frequency'],prediction['defect'][-1],upper)
    unresolved=raw-basis.values@source['projected_replacement'][-1]
    resolved=basis.values@solution['photon'][-1,:,:3]
    total=resolved+unresolved
    saved=basis.values@prediction['profiles'][-1]
    def residual(value):
        eta=(reader.measure*reader.frequency)@value/reader.capacity
        amplitude=reader.amplitude_matrix@value
        return value-reader.frequency[:,None]*eta-reader.templates@amplitude
    photon_scale=np.maximum(norm(saved,basis.measure),1e-300)
    moment_scale=np.maximum((reader.measure*(1+reader.frequency))@(abs(raw)+abs(basis.values@source['projected_replacement'][-1])),1e-300)
    defect=(abs((reader.measure*reader.frequency)@unresolved)+abs(reader.measure@unresolved))/moment_scale
    metrics=dict(final_photon_change_over_saved_norm=(norm(total,basis.measure)/photon_scale).tolist(),
        final_residual_change_over_saved_residual=(norm(residual(total),basis.measure)/np.maximum(norm(residual(saved),basis.measure),1e-300)).tolist(),
        final_gas_change_over_saved=(abs(solution['gas'][-1,:3])/np.maximum(abs(prediction['gas'][-1]),1e-300)).tolist(),
        final_gas_change=solution['gas'][-1,:3].tolist(),
        final_resolved_photon_norm=norm(resolved,basis.measure).tolist(),final_unresolved_norm=norm(unresolved,basis.measure).tolist(),
        final_physical_change_norm=norm(total,basis.measure).tolist(),saved_photon_norm=photon_scale.tolist(),
        final_saved_residual_norm=norm(residual(saved),basis.measure).tolist(),
        fine_vs_canonical_projection_over_replacement=(photon_norm(source['projection_quadrature_difference'][-1],basis.mass)/np.maximum(source['replacement_norm'][-1],1e-300)).tolist(),
        unresolved_energy_number_defect=float(np.max(defect)),
        resolved_component_norms=[norm(basis.values@solution['photon'][-1,:,offset:offset+3],basis.measure).tolist() for offset in [3,6,9]])
    view=dict(frequency=basis.nodes,measure=basis.measure,saved_potential=saved,replacement=raw,
        resolved_change=resolved,unresolved_change=unresolved,physical_change=total,
        residual_change=residual(total),saved_residual=residual(saved))
    return metrics,view


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--source',required=True)
    parser.add_argument('--steps',type=int,choices=[1024,2048,4096],default=2048)
    args=parser.parse_args()
    modest()
    source_folder=ROOT/'results'/args.source
    status=local_packet(source_folder)
    assert status['all_checks_passed']
    folder=ROOT/'results'/('response-'+args.source.removeprefix('sources-')+'-r'+str(args.steps))
    folder.mkdir(parents=True,exist_ok=False)
    ladder=infrared_ladder.InfraredLadder(BRANCH/'emitting-thermal-background-20261008/banks/infrared96-q700')
    basis=ladder.basis
    inputs=[source_folder/'status.json',*ladder.inputs]
    checks,models=[],{}
    started=time.monotonic()
    for model in ['heavy','cold']:
        source_path=source_folder/(model+'.npz')
        source=read_npz(source_path)
        inner_path=ROOT/'results'/str(source['inner_packet'])/'prediction.npz'
        local_packet(inner_path.parent)
        prediction=read_npz(inner_path)
        background=thermal_wave.thermal.ThermalBackground(model)
        emission=NonlocalEmission(basis,background,'nonlocal-leading',BRANCH/'infrared-source-domain-20261008/banks/s960-i256')
        inputs.extend([source_path,inner_path,inner_path.parent/'status.json',*emission.inputs,background.parent.source,background.native_constants])
        solution,errors=solve_response(model,source,args.steps,ladder,emission,background)
        metrics,view=readout(basis,prediction,source,solution,status['upper'])
        checks.extend(check(name+':'+model,value,1. if name=='energy_spectrum' else 1e-7) for name,value in errors.items())
        checks.append(check('Unresolved canonical moments:'+model,metrics['unresolved_energy_number_defect'],1e-10))
        selection=np.arange(0,args.steps+1,args.steps//128)
        snapshots={key:value[selection] for key,value in solution.items()}
        assert all(np.isfinite(value).all() for value in [*snapshots.values(),*view.values()])
        np.savez_compressed(folder/(model+'.npz'),**snapshots,**view,integration_steps=args.steps,saved_step_indices=selection)
        models[model]=dict(errors=errors,metrics=metrics)
        print(json.dumps(dict(packet=folder.name,model=model,errors=errors,metrics=metrics,seconds=time.monotonic()-started)),flush=True)
        del solution
    finish(folder,dict(checks=checks,models=models,steps=args.steps,source_packet=args.source,upper=status['upper'],
        paired_gas_exchange=True,expansion_work_included=True,resolved_and_unresolved_reported=True,
        parent_history_rerun=False,conditional_first_response=True,iterated_feedback=False,
        residuals_checked_every_step=True,saved_snapshots_not_adjacent_steps=True,seconds=time.monotonic()-started),__file__,inputs)


if __name__=='__main__':
    main()

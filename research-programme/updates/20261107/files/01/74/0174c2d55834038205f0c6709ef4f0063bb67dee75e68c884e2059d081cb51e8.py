import os
for variable in ['OPENBLAS_NUM_THREADS', 'OMP_NUM_THREADS', 'MKL_NUM_THREADS']:
    os.environ[variable] = '1'
import sys
sys.dont_write_bytecode = True
from pathlib import Path
import json
import hashlib
from datetime import datetime, timezone
ROOT = Path(__file__).resolve().parent
BRANCH = ROOT.parent
PARENT = BRANCH / 'upper-outer-frequency-temperature-test-20261020'
PARENT_SHA = 'bf3e8579057f225a5731c63d4bdd1f149f89c85aeec2ce2ed30376648036e8e9'
STARTED = '2026-10-20T18:27:30+00:00'
sys.path.insert(0, str(PARENT))
import stage176_frequency_common as saved
np, mp = saved.np, saved.mp
source, combine, norm = saved.source, saved.combine, saved.norm
import scipy.linalg as linear


def forbidden(*args, **kwargs):
    raise RuntimeError('Stage177 is saved-data-only; new physical evaluation forbidden')


def compare(checks, name, value, tolerance=1e-10):
    value = float(value)
    checks.append(dict(name=name, value=value, tolerance=tolerance,
                       passed=bool(np.isfinite(value) and value < tolerance)))


def dense(pair):
    return pair[0] + pair[1]


def main():
    source.modest()
    source.evaluate = source.models = source.context = forbidden
    assert not (ROOT / 'results/COMPLETE').exists()
    parent_path = PARENT / 'results/stage-integrity.json'
    assert saved.digest(parent_path) == PARENT_SHA
    parent = json.loads(parent_path.read_text())
    authenticated = {str(PARENT / name): checksum for name, checksum in parent['file_hashes'].items()}
    authenticated.update(parent['consumed_and_immediate_rehashed'])
    for filename, checksum in authenticated.items():
        assert saved.digest(filename) == checksum, filename
    config_path = PARENT / 'configuration.json'
    config = json.loads(config_path.read_text())
    assert config['source_prediction_tolerance'] == .01 and config['identity_tolerance'] == 1e-10
    basis_path = source.ROOT / 'results/preparation/basis.npz'
    with np.load(basis_path) as basis:
        mass = basis['mass'].copy()
    factor = linear.cholesky(mass, lower=True)

    def whiten(values):
        photons = np.moveaxis(values[..., 1:97, :], -2, -1)
        return linear.solve_triangular(factor, photons.reshape(-1, 96).T, lower=True).T.reshape(photons.shape)

    def dot(first, second):
        return np.sum(whiten(first)*whiten(second), axis=-1)

    def length(values):
        return np.sqrt(np.maximum(dot(values, values), 0.))

    def identity(name, residual, scale):
        compare(checks, name, np.max(length(residual)/np.maximum(length(scale), 1e-300)))

    configuration = dict(stage=177, started_utc=STARTED, parent_seal_sha256=PARENT_SHA,
                         source_prediction_tolerance=.01, identity_tolerance=1e-10,
                         new_source_evaluations=0, post_test_diagnostic=True,
                         prior_bookmark_normalized_sha256={
                             str(path): hashlib.sha256(path.read_text(encoding='utf-8').encode('utf-8')).hexdigest()
                             for path in [BRANCH/'RESUME-CURRENT.md', BRANCH.parent/'CURRENT_LOCAL_RESUME.md']})
    saved.write_json(ROOT / 'configuration.json', configuration)
    checks, paths = [], {parent_path, config_path, basis_path}
    frozen_path = PARENT / 'results/frozen/predictions.npz'
    target_path = PARENT / 'results/assessment/actuals.npz'
    paths.update([frozen_path, target_path])
    with np.load(frozen_path) as packet:
        groups = list(packet['groups'])
        frozen_high, frozen_low = packet['high'].copy(), packet['low'].copy()
        derivative_high, derivative_low = packet['derivative_high'].copy(), packet['derivative_low'].copy()
    with np.load(target_path) as packet:
        assert list(packet['groups']) == groups
        targets = packet['high'] + packet['low']
    complete_index = groups.index('complete_sum')
    tags = list(source.OFFSETS)
    bank = {}
    for tag in tags:
        pairs = []
        for node in config['selected']:
            key = saved.event_key(node)
            angle, electron = key.split(':electron')
            path = PARENT/'events'/tag/angle/f'electron-{int(electron):02d}.npz'
            assert str(path) in authenticated
            pair = saved.read_pair(path)
            assert pair[0].shape == pair[1].shape == (2, 6, 98, 4)
            assert np.isfinite(pair[0]).all() and np.isfinite(pair[1]).all()
            pairs.append(pair)
            paths.add(path)
        bank[tag] = pairs
        saved.write_json(ROOT/'progress.json', dict(state='reading_saved_stencils', phase=tag, events_read=len(bank)*36))
    sums = {tag: combine(pairs, [1]*36) for tag, pairs in bank.items()}
    predicted, rebuilt = saved.predictors(sums, config['delta_log_temperature'])
    for order in range(4):
        expected = (derivative_high[complete_index, order], derivative_low[complete_index, order])
        identity('Rebuild saved derivative '+str(order), dense(combine([rebuilt[order], expected], [1, -1])), dense(expected))
    for order in range(3):
        expected = (frozen_high[complete_index, order], frozen_low[complete_index, order])
        identity('Rebuild saved predictor '+str(order), dense(combine([predicted[order], expected], [1, -1])), dense(expected))
    compare(checks, 'Moving/fixed anchor identical', np.max(abs(dense(sums['anchor'])[0]-dense(sums['anchor'])[1])), 1e-300)
    derivatives = derivative_high[complete_index] + derivative_low[complete_index]
    error = dense(combine([(derivative_high[complete_index, 2], derivative_low[complete_index, 2]),
                           (derivative_high[complete_index, 3], derivative_low[complete_index, 3])], [1, -1]))
    history_error = error[0]-error[1]
    history_curvatures = derivatives[2:, 0]-derivatives[2:, 1]
    identity('Moving/fixed/history curvature-difference closure', error[0]-error[1]-history_error, error[0])
    identity('History curvature minus step difference closure', history_curvatures[0]-history_curvatures[1]-history_error, error[0])
    compare(checks, 'Independent photon metric matches original',
            np.max(abs(length(error)-norm(error,mass))/np.maximum(norm(error,mass),1e-300)))
    for component, members in [(4,[1,2,3]), (5,[0,1,2,3])]:
        identity('Component curvature closure '+str(component), sum(error[:,member] for member in members)-error[:,component], error[:,component])
    target = targets[complete_index]
    delta = config['delta_log_temperature']
    first_error = derivatives[0]-derivatives[1]
    tangent_impact = delta*first_error
    curvature_impact = .5*delta**2*error
    predicted_error = dense(combine([(frozen_high[complete_index,2],frozen_low[complete_index,2]),
                                    (frozen_high[complete_index,1],frozen_low[complete_index,1])],[1,-1]))
    identity('Prediction sensitivity split', tangent_impact+curvature_impact-predicted_error, predicted_error)
    metrics = []
    for branch, branch_name in enumerate(saved.BRANCHES):
        for component, component_name in enumerate(source.COMPONENTS):
            for history in range(4):
                fine_norm = length(derivatives[3])[branch,component,history]
                discrepancy_norm = length(error)[branch,component,history]
                target_norm = length(target)[branch,component,history]
                ratio = discrepancy_norm/max(fine_norm,1e-300)
                metrics.append(dict(branch=branch_name,component=component_name,history=history,
                    fine_curvature_norm=float(fine_norm),coarse_curvature_norm=float(length(derivatives[2])[branch,component,history]),
                    discrepancy_norm=float(discrepancy_norm),relative=float(ratio),passed=bool(ratio < .01),
                    tangent_prediction_change=float(length(tangent_impact)[branch,component,history]/max(target_norm,1e-300)),
                    curvature_prediction_change=float(length(curvature_impact)[branch,component,history]/max(target_norm,1e-300)),
                    combined_prediction_change=float(length(predicted_error)[branch,component,history]/max(target_norm,1e-300))))
    fixed_history = []
    for component, name in enumerate(source.COMPONENTS):
        for history in range(4):
            denominator = max(dot(error[0,component],error[0,component])[history],1e-300)
            fixed_projection = dot(error[1,component],error[0,component])[history]/denominator
            history_projection = dot(history_error[component],error[0,component])[history]/denominator
            compare(checks,f'{name}:{history}:fixed/history projection closure',abs(fixed_projection+history_projection-1.))
            fixed_history.append(dict(component=name,history=history,
                fixed_signed_share=float(fixed_projection),history_signed_share=float(history_projection),
                fixed_norm_over_moving=float(length(error[1,component])[history]/max(length(error[0,component])[history],1e-300)),
                history_norm_over_moving=float(length(history_error[component])[history]/max(length(error[0,component])[history],1e-300)),
                moving_fine_norm=float(length(derivatives[3,0,component])[history]),
                fixed_fine_norm=float(length(derivatives[3,1,component])[history]),
                history_fine_norm=float(length(history_curvatures[1,component])[history])))
    component_records = []
    for branch, branch_name in enumerate(saved.BRANCHES):
        denominator = np.maximum(dot(error[branch,4],error[branch,4]),1e-300)
        gain = sum(length(error[branch,index]) for index in [1,2,3])/np.maximum(length(error[branch,4]),1e-300)
        for component in [1,2,3]:
            projection = dot(error[branch,component],error[branch,4])/denominator
            for history in range(4):
                component_records.append(dict(branch=branch_name,component=source.COMPONENTS[component],history=history,
                    signed_share=float(projection[history]),norm_over_matched=float(length(error[branch,component])[history]/max(length(error[branch,4])[history],1e-300)),
                    cancellation_factor=float(gain[history])))
        for history in range(4):
            compare(checks,f'{branch_name}:{history}:component projection closure',
                    abs(sum(row['signed_share'] for row in component_records if row['branch']==branch_name and row['history']==history)-1.))
    localization = []
    for label in config['groups']:
        if label == 'complete_sum':
            continue
        index = groups.index(label)
        local_error = dense(combine([(derivative_high[index,2],derivative_low[index,2]),
                                     (derivative_high[index,3],derivative_low[index,3])],[1,-1]))
        for branch, branch_name in enumerate(saved.BRANCHES):
            for component in [0,4,5]:
                denominator = np.maximum(dot(error[branch,component],error[branch,component]),1e-300)
                projection = dot(local_error[branch,component],error[branch,component])/denominator
                for history in range(4):
                    localization.append(dict(group=label,branch=branch_name,component=source.COMPONENTS[component],
                                             history=history,signed_share=float(projection[history])))
    for kind in ['angle_', ':electron']:
        for branch_name in saved.BRANCHES:
            for component in ['control','remainder','total']:
                for history in range(4):
                    selected = [row['signed_share'] for row in localization if kind in row['group'] and
                                (row['branch'],row['component'],row['history'])==(branch_name,component,history)]
                    compare(checks,f'{kind}:{branch_name}:{component}:{history}:localization closure',abs(sum(selected)-1.))
    print('Saved-source decomposition complete; reconstructing curvature at80digits.',flush=True)
    exact = np.zeros((3,2,6,98,4))
    with mp.workdps(80):
        coefficients = [[10000,-20000,10000,0,0],[0,-80000,0,40000,40000]]
        ordered_tags = ['plus','anchor','minus','plus_half','minus_half']
        for branch,component,row,history in np.ndindex(2,6,98,4):
            values=[]
            for tag in ordered_tags:
                values.append(mp.fsum(mp.mpf(float(pair[0][branch,component,row,history]))+
                                      mp.mpf(float(pair[1][branch,component,row,history])) for pair in bank[tag]))
            coarse=mp.fsum(coefficient*value for coefficient,value in zip(coefficients[0],values))
            fine=mp.fsum(coefficient*value for coefficient,value in zip(coefficients[1],values))
            exact[:,branch,component,row,history]=[float(coarse),float(fine),float(coarse-fine)]
    precision = []
    for label,reference,reconstruction in [('coarse',derivatives[2],exact[0]),('fine',derivatives[3],exact[1]),('discrepancy',error,exact[2])]:
        relative=length(reconstruction-reference)/np.maximum(length(reference),1e-300)
        for branch,component,history in np.ndindex(relative.shape):
            compare(precision,f'{label}:{saved.BRANCHES[branch]}:{source.COMPONENTS[component]}:{history}',relative[branch,component,history])
    checks.extend(precision)
    exact_ratio=length(exact[2])/np.maximum(length(exact[1]),1e-300)
    observed_ratio=length(error)/np.maximum(length(derivatives[3]),1e-300)
    compare(checks,'High precision leaves curvature gate decisions unchanged',np.max((exact_ratio < .01)!=(observed_ratio < .01)),.5)
    history_records=[]
    for model in ['heavy','cold']:
        history_path=BRANCH/'infrared-source-domain-20261008/backgrounds'/(model+'-nonlocal-refined-6400')/'history.npz'
        tail_path=BRANCH/'dynamical-infrared-tail-20261008/runs'/(model+'-production')/'tail.npz'
        for field,path,key in [('profiles',history_path,'profiles'),('gas',history_path,'temperature_scaled'),('tail',tail_path,'slope')]:
            paths.add(path)
            assert str(path) in authenticated, path
            with np.load(path) as packet:
                grid=packet['expansion'].copy()
                values=packet[key].copy()
                tail_frequency=packet['frequency'].copy() if field=='tail' else None
            center=config['start_fraction']*grid[-1]
            nearest=int(np.argmin(abs(grid-center)))
            def interpolated(point):
                lower=int(np.clip(np.searchsorted(grid,point,side='right')-1,0,len(grid)-2))
                weight=(point-grid[lower])/(grid[lower+1]-grid[lower])
                return (1-weight)*values[lower]+weight*values[lower+1]
            def history_norm(value):
                if field=='profiles':
                    return float(np.sqrt(max(float(value@mass@value),0.)))
                if field=='tail':
                    return float(np.sqrt(max(float(np.trapezoid(value*value,x=np.log(tail_frequency))),0.)))
                return float(abs(value))
            samples={tag:interpolated(center-offset) for tag,offset in source.OFFSETS.items()}
            coarse=(samples['plus']-2*samples['anchor']+samples['minus'])/.01**2
            fine=(samples['plus_half']-2*samples['anchor']+samples['minus_half'])/.005**2
            left=-(values[nearest]-values[nearest-1])/(grid[nearest]-grid[nearest-1])
            right=-(values[nearest+1]-values[nearest])/(grid[nearest+1]-grid[nearest])
            history_records.append(dict(model=model,field=field,source_path=str(path),grid_points=len(grid),
                anchor_knot_offset=float(grid[nearest]-center),grid_spacing=float(grid[nearest+1]-grid[nearest]),
                intervals_crossed={tag:int(np.searchsorted(grid,center-offset,side='right')-1-nearest) for tag,offset in source.OFFSETS.items()},
                coarse_curvature_norm=history_norm(coarse),fine_curvature_norm=history_norm(fine),
                relative_curvature_change=history_norm(coarse-fine)/max(history_norm(fine),1e-300),
                anchor_slope_jump_relative=history_norm(right-left)/max((history_norm(right)+history_norm(left))/2,1e-300),
                norm='primal basis mass' if field=='profiles' else 'log-frequency L2' if field=='tail' else 'absolute scalar',
                diagnostic_only=True,source_gate_not_applied=True))
    output=ROOT/'results'
    output.mkdir(parents=True,exist_ok=True)
    for name,rows in [('source-metrics',metrics),('fixed-history-attribution',fixed_history),
                      ('component-attribution',component_records),('angle-electron-attribution',localization),
                      ('precision-checks',precision),('native-history-diagnostics',history_records)]:
        saved.write_json(output/(name+'.json'),rows)
    np.savez_compressed(output/'diagnostic-vectors.npz',curvature_error=error,history_error=history_error,
                        derivatives=derivatives,exact_reconstruction=exact,tangent_impact=tangent_impact,
                        curvature_impact=curvature_impact,prediction_step_change=predicted_error)
    for path in paths:
        if path==parent_path:
            assert saved.digest(path)==PARENT_SHA
        else:
            assert str(path) in authenticated and saved.digest(path)==authenticated[str(path)],path
    for filename,checksum in authenticated.items():
        assert saved.digest(filename)==checksum,filename
    scripts=list(ROOT.glob('*.py'))
    for path in scripts:
        compile(path.read_text(encoding='utf-8'),str(path),'exec')
    assert not list(ROOT.rglob('__pycache__'))
    protected=BRANCH.parent.parent/'formalization-workbench'
    modified=[str(path) for path in protected.rglob('*') if path.is_file() and path.stat().st_mtime > datetime.fromisoformat(STARTED).timestamp()]
    compare(checks,'Protected workbench mtime guard',len(modified),.5)
    code_paths={*scripts,ROOT/'ACCEPTANCE.md',ROOT/'DERIVATION.md',ROOT/'configuration.json'}
    for module in list(sys.modules.values()):
        filename=getattr(module,'__file__',None)
        if filename and Path(filename).suffix=='.py' and Path(filename).resolve().is_relative_to(BRANCH):
            path=Path(filename).resolve()
            code_paths.add(path)
            if not path.is_relative_to(ROOT):
                assert str(path) in authenticated and saved.digest(path)==authenticated[str(path)],path
    status=dict(state='complete',stage=177,finished_utc=datetime.now(timezone.utc).isoformat(),
                checks=checks,count=len(checks),all_checks_passed=all(row['passed'] for row in checks),
                input_hashes={str(path):saved.digest(path) for path in sorted(paths|code_paths)},
                authenticated_parent_inputs=authenticated,new_source_evaluations=0,reused_stencil_events=180,
                derivative_tolerance=.01,identity_tolerance=1e-10,tolerances_changed=False,
                new_node_matched_moving_curvature_gate_passed=bool(np.max(exact_ratio[0,4])<.01),
                max_independent_reconstruction_relative=max(row['value'] for row in precision),
                protected_modified_file_count=len(modified),protected_check_scope='Mtime guard since '+STARTED+'; not a pre-turn content snapshot',
                protocol_validation_only=True,history_artifact_proved=False,post_test_diagnostic=True)
    saved.write_json(output/'status.json',status)
    assert status['all_checks_passed'],'Diagnostic validation failed; keep artifacts and investigate'
    (output/'COMPLETE').write_text('complete\n',encoding='utf-8')
    saved.write_json(ROOT/'progress.json',dict(state='analysis_complete',new_source_evaluations=0))
    print(json.dumps(dict(protocol_checks=len(checks),protocol_pass=status['all_checks_passed'],
        precise_matched_curvature_max=float(np.max(exact_ratio[0,4])),
        fixed_history=[row for row in fixed_history if row['component'] in ['control','remainder'] and row['history']==1],
        components=[row for row in component_records if row['branch']=='moving_history' and row['history']==1],
        native_histories=history_records,precision_max=status['max_independent_reconstruction_relative'])),flush=True)


if __name__=='__main__':
    main()

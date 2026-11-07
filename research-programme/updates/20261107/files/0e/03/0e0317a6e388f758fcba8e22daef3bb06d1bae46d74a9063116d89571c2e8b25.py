from derive_annular_source_gravity_20260914 import EvidenceRun
from pathlib import Path
from datetime import datetime, timezone
from decimal import Decimal, localcontext
import hashlib
import json
import numpy as np


def main():
    root = Path(__file__).resolve().parents[1]
    directory = root/'source-intake/navier-stokes/20260914'
    target = directory/'annular-common-jet-jump-stage-integrity-20261001.json'
    if target.exists():
        raise FileExistsError(target)
    hashes,mismatches,records,reports = {},[],{},{}

    def verify(relative,expected=None):
        path = (root/relative).resolve()
        if path==root/'CURRENT_LOCAL_RESUME.md':
            return
        if not path.is_relative_to(root) or not path.is_file():
            raise RuntimeError('Invalid integrity source '+relative)
        key = str(path.relative_to(root))
        if key not in hashes:
            hashes[key] = hashlib.sha256(path.read_bytes()).hexdigest()
        if expected is not None and hashes[key]!=expected:
            mismatches.append(key)

    parent_path = directory/'annular-C1-integrated-stage-integrity-20261001.json'
    parent = json.loads(parent_path.read_text())
    if parent['state']!='complete' or parent['mismatches']:
        raise RuntimeError('Incomplete parent authority')
    verify(str(parent_path.relative_to(root)))
    for relative,expected in parent['hashes'].items():
        verify(relative,expected)
    complete = ['annular-common-physical-jet-reference-attempt02','annular-common-physical-jet-MTS-attempt02',
        'annular-common-jet-transfer-validation-attempt01',
        'annular-spatial-jump-reference-attempt01','annular-spatial-jump-MTS-attempt01']
    failed = ['annular-common-physical-jet-reference-attempt01','annular-common-physical-jet-MTS-attempt01']
    for name in complete+failed:
        path = directory/name/'status.json'
        report = json.loads(path.read_text())
        if name in complete:
            if report['state']!='complete' or not all(item['passed'] for item in report['checks']):
                raise RuntimeError('Incomplete stage '+name)
        else:
            broken = [item['name'] for item in report['checks'] if not item['passed']]
            if report['state']!='failed' or broken!=['normalization_is_coordinate_change']:
                raise RuntimeError('Unreconciled first attempt '+name)
        verify(str(path.relative_to(root)))
        for category in ['inputs','outputs']:
            for relative,expected in report[category].items():
                verify(relative,expected)
        for member in path.parent.iterdir():
            if member.is_file():
                verify(str(member.relative_to(root)))
        log = directory/(name+'.log')
        if log.exists():
            verify(str(log.relative_to(root)))
        records[name] = dict(state=report['state'],checks=len(report['checks']))
        reports[name] = report
    matched,layers_resummed,witnesses = {},0,[]
    with localcontext() as context:
        context.prec = 75
        for name in complete:
            report = reports[name]
            kind = 'jump' if name.startswith('annular-spatial-jump-') else 'common'
            for item in report.get('rule_outputs',[]):
                with np.load(root/item['path'],allow_pickle=False) as archive:
                    layers,weights,total = [archive[key] for key in ['layers','weights','total']]
                    flattened = layers.reshape(len(weights),-1)
                    expected = total.ravel()
                    for column in range(flattened.shape[1]):
                        terms = [Decimal.from_float(float(weight))*Decimal.from_float(float(value))
                            for weight,value in zip(weights,flattened[:,column])]
                        exact = sum(terms,Decimal(0))
                        allowance = Decimal.from_float(128*np.finfo(float).eps)*sum(map(abs,terms),Decimal(0))+Decimal('1e-90')
                        if abs(exact-Decimal.from_float(float(expected[column])))>allowance:
                            raise RuntimeError('Independent material accumulation failed')
                    labels = archive['labels']
                    key = kind+'-'+str(len(weights))
                    digest = hashlib.sha256(labels.tobytes()+weights.tobytes()).hexdigest()
                    if key in matched and matched[key]!=digest:
                        raise RuntimeError('Unmatched branch material rules')
                    matched[key] = digest
                    layers_resummed += len(weights)
            if kind!='jump':
                continue
            for path in sorted((directory/name).glob('*-witness.npz')):
                with np.load(path,allow_pickle=False) as archive:
                    mass,nodal,minimum,remainder,energy = [archive[key] for key in ['mass','nodal','minimum','remainder','energy']]
                    residual_trace = np.r_[remainder[0,0],remainder[1:,0]-remainder[:-1,2],remainder[-1,2]]
                    mass_minimum = np.einsum('cij,cj->ci',mass,minimum)
                    continuous_covector = np.r_[mass_minimum[:,1],mass_minimum[:-1,2]+mass_minimum[1:,0]]
                    trace_error = np.max(abs(residual_trace))/max(np.max(abs(nodal)),1e-300)
                    stationarity = np.max(abs(continuous_covector))/max(np.max(abs(mass_minimum)),1e-300)
                    if trace_error>2e-11 or stationarity>2e-11:
                        raise RuntimeError('Independent jump/continuous-space stationarity failed')
                    recalculated = []
                    for first,last in [(nodal,nodal),(minimum,minimum),(remainder,remainder),(minimum,remainder)]:
                        terms = [Decimal.from_float(float(first[cell,left]))*Decimal.from_float(float(mass[cell,left,right]))
                            *Decimal.from_float(float(last[cell,right]))
                            for cell in range(len(mass)) for left in range(3) for right in range(3)]
                        recalculated.append(sum(terms,Decimal(0)))
                    scale = abs(recalculated[0])
                    if any(abs(value-Decimal.from_float(float(stored)))>Decimal('2e-11')*scale
                        for value,stored in zip(recalculated,energy)):
                        raise RuntimeError('Independent local energy failed')
                    if abs(recalculated[0]-recalculated[1]-recalculated[2]-2*recalculated[3])>Decimal('2e-11')*scale:
                        raise RuntimeError('Independent energy decomposition failed')
                    boundary_upper = nodal[0,0]**2*mass[0,0,0]+nodal[-1,2]**2*mass[-1,2,2]
                    boundary_fraction = float(boundary_upper/energy[0])
                    if boundary_fraction>1e-12:
                        raise RuntimeError('Boundary contribution requires separate interpretation')
                    witnesses.append(dict(path=str(path.relative_to(root)),cells=len(mass),
                        trace_error=float(trace_error),continuous_stationarity=float(stationarity),
                        boundary_only_minimum_energy_fraction_upper_bound=boundary_fraction,
                        exact_energy=list(map(str,recalculated))))
    transfer = reports['annular-common-jet-transfer-validation-attempt01']
    if transfer['exact_witnesses_normalized']!=46 or not transfer['normalization_frozen_at_base_state']:
        raise RuntimeError('Missing exact normalized witnesses')
    compiled = []
    for name in ['probe_annular_common_physical_jet_20261001.py','probe_annular_common_physical_jet_v2_20261001.py',
        'verify_annular_common_jet_transfer_20261001.py','probe_annular_spatial_jump_lifting_20261001.py',
        'seal_annular_common_jet_jump_20261001.py']:
        path = root/'scripts'/name
        compile(path.read_text(),str(path),'exec')
        verify(str(path.relative_to(root)))
        compiled.append(name)
    for name in ['DERIVATION-20261001-common-physical-support-jet.md',
        'DERIVATION-20261001-spatial-jump-kinetic-lifting.md',
        'RECOVERY-20261001-common-jet-symbolic-comparison.json',
        'RESULTS-20261001-common-jet-and-spatial-jump-mechanism.md']:
        verify(name)
    started = datetime(2026,10,1,19,46,59,tzinfo=timezone.utc).timestamp()
    protected = root.parent/'formalization-workbench'
    changed = [str(path.relative_to(protected)) for path in protected.rglob('*')
        if path.is_file() and path.stat().st_mtime>=started]
    bytecode = list((root/'scripts').rglob('__pycache__'))
    if changed or bytecode or mismatches:
        raise RuntimeError(dict(changed=changed,bytecode=list(map(str,bytecode)),mismatches=mismatches))
    result = dict(state='complete',sealed_at=datetime.now(timezone.utc).isoformat(),hashes=hashes,mismatches=mismatches,
        unique_files_rehashed=len(hashes),authorities=records,scripts_compiled=compiled,
        material_layers_independently_resummed=layers_resummed,matched_branch_rules=matched,
        local_jump_witnesses_independently_replayed=witnesses,normalized_exact_witnesses=46,
        source_response_retained=True,full_current_grid_comparison_completed=False,
        full_parent_reprojection=False,finite_evolution_performed=False,
        protected_workbench_changed_since_turn_start=len(changed),bytecode_cache_present=False,
        pending={},current_resume_excluded=True,github_action=False,subagents_used=False,valid_for_physics_claim=False)
    with target.open('x',encoding='utf-8') as stream:
        stream.write(json.dumps(result,indent=2)+'\n')
    print(json.dumps({key:value for key,value in result.items() if key not in ['hashes','local_jump_witnesses_independently_replayed']},indent=2),flush=True)


if __name__=='__main__':
    main()


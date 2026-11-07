from __future__ import annotations

from pathlib import Path
import sympy as sp

from interior_common import ROOT, modest_process, read_json, digest, save


def main():
    modest_process()
    checks = []

    def check(name, passed, value=None):
        checks.append(dict(name=name,passed=bool(passed),value=value))
        assert passed, (name,value)

    accepted = ['map-v2','energy-v2','reduced-v2','principal-proof-v2','vacuum-join-v2','replay-v2','inspect-v2','controls-v2','potential-probe-v2']
    excluded = ['map','energy','reduced','inspect']
    reports = {label:read_json(ROOT/'results'/label/'status.json') for label in accepted}
    exact_total = 0
    for label,count in [('map-v2',6),('energy-v2',6),('reduced-v2',3),('principal-proof-v2',9),('vacuum-join-v2',6)]:
        rows = reports[label]['exact_checks']
        check(label+' exact checks',len(rows)==count and all(row['passed'] and row['residual']=='0' for row in rows))
        exact_total += count
    check('accepted and excluded evidence disjoint',not set(accepted).intersection(excluded))
    for label in excluded:
        check('rejected '+label+' preserved',(ROOT/'results'/label/'status.json').is_file())
    proof = reports['principal-proof-v2']
    check('positive new phase uniform floor',proof['local_phase_uniform_lower_numeric']>.79)
    check('positive scalar principal pivot floor',proof['scalar_principal_pivot_lower_numeric']>.28)
    check('not silently a total energy theorem',proof['full_energy_positive_claimed'] is False)
    check('not silently a canonical transformation',proof['canonical_transformation_claimed'] is False)
    check('not silently a frequency gap',proof['frequency_or_continuum_gap_claimed'] is False)
    source = reports['energy-v2']
    symbols = sp.symbols(' '.join(source['symbols']),positive=True)
    environment = dict(zip(source['symbols'],symbols))
    parse = lambda value:sp.sympify(value,locals=environment)
    radius,alpha,metric,field,gradient,rotation,potential,force,second = symbols
    beta = parse(source['coefficients']['beta'])
    pressure = (metric*gradient**2+rotation**2*field**2)/2-potential
    lapse_gradient = (1-metric+2*alpha*radius**2*pressure)/(2*radius*metric)
    expected_contact = -1/(2*alpha*radius)+beta*lapse_gradient/(4*alpha)+radius**2*gradient*(force-rotation**2*field)/4+metric*radius*gradient**2/2
    check('documented angular contact matches generated form',sp.factor(parse(source['contact_coefficients'][0])-expected_contact)==0)
    controls = reports['controls-v2']
    for row in controls['constraint_rows']:
        check(row['profile']+' version2 satisfies original constraint',row['correct_v2_relative_error']<1e-10,row['correct_v2_relative_error'])
        check(row['profile']+' independent check rejects first attempt',row['superseded_v1_relative_error']>1e-4,row['superseded_v1_relative_error'])
    check('phase square replay',controls['phase_completion_relative_error']<1e-12,controls['phase_completion_relative_error'])
    check('coupled derivative squares replay',controls['principal_square_relative_error']<1e-12,controls['principal_square_relative_error'])
    for row in reports['replay-v2']['rows']:
        label=row['profile']+' '+str(row['cells'])
        for key in ['constraint_relative_error','joined_relative_error','interior_contact_relative_error','exterior_contact_relative_error']:
            check(label+' '+key,row[key]<1e-9,row[key])
    inspection = reports['inspect-v2']
    check('sampled phase obeys analytic floor',inspection['minimum_phase_coefficient']>proof['local_phase_uniform_lower_numeric'])
    check('sampled coupled derivatives positive',inspection['minimum_normalized_gradient']>0)
    check('vacuum join does not assume a wave equation',reports['vacuum-join-v2']['no_frequency_equation_used'])
    for row in reports['potential-probe-v2']['rows']:
        check(row['method']+' simple certificate failure retained',row['negative_samples']>0 and row['minimum_scaled_potential_eigenvalue']<0)
        check(row['method']+' samples not promoted to proof',row['samples_are_continuum_proof'] is False)
    inputs=[]
    script_hashes={digest(path) for path in ROOT.glob('*.py')}
    for path in sorted(ROOT.rglob('*.json')):
        report=read_json(path)
        assert report['state']=='complete' and report['script_sha256'] in script_hashes,path
        for source,expected in report.get('input_hashes',{}).items():
            assert Path(source).is_file() and digest(source)==expected,(path,source)
        inputs.append(path)
    check('all saved report input hashes match',True,len(inputs))
    compiled=[]
    for path in sorted(ROOT.glob('*.py')):
        compile(path.read_bytes(),str(path),'exec')
        compiled.append(path.name)
    check('all authored scripts compile without bytecode',True,len(compiled))
    check('no bytecode caches',not list(ROOT.rglob('__pycache__')))
    save('validation',Path(__file__),dict(checks=checks,validation_checks=len(checks),exact_checks=exact_total,
        extra_documented_contact_identity_verified=True,accepted_result_labels=accepted,rejected_result_labels=excluded,
        coupled_principal_positivity_derived=True,full_joint_even_energy_positive_proved=False,
        canonical_transformation_proved=False,phase_uniform_lower=proof['local_phase_uniform_lower_numeric'],
        complete_exterior_contact_match=True,original_constraint_replays=len(reports['replay-v2']['rows']),
        rejected_reconstruction_controls=len(controls['constraint_rows']),compiled_scripts=compiled,
        new_background_or_wave_solves=0,github_action=False),inputs)
    print(dict(validation_checks=len(checks),exact_checks=exact_total,compiled=len(compiled),rejected_first_attempt_detected=True),flush=True)


if __name__ == '__main__':
    main()

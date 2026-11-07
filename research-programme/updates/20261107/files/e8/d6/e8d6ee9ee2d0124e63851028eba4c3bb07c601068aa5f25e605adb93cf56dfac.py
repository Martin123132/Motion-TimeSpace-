from derive_annular_source_gravity_20260914 import EvidenceRun
from annular_position_enabled_compatibility_20260930 import diagnose
from annular_exact_envelope_20261001 import envelope_search
from decimal import Decimal, localcontext
from fractions import Fraction
import hashlib
import json
import numpy as np


def main():
    evidence = EvidenceRun('annular-matter-gravity-assembly-attempt01',__file__)
    verified,summaries = {},[]

    def verify(relative,expected=None):
        path = (evidence.root/relative).resolve()
        if not path.is_relative_to(evidence.root) or not path.is_file():
            raise RuntimeError('Invalid input '+relative)
        key = str(path.relative_to(evidence.root))
        if key not in verified:
            verified[key] = hashlib.sha256(path.read_bytes()).hexdigest()
            evidence.own(path)
        if expected is not None and verified[key]!=expected:
            raise RuntimeError('Changed input '+relative)
        return path

    def status(name):
        path = evidence.output.parent/name/'status.json'
        result = json.loads(verify(str(path.relative_to(evidence.root))).read_text())
        evidence.check(name+':complete',result['state']=='complete' and all(row['passed'] for row in result['checks']))
        for category in ['inputs','outputs']:
            for relative,expected in result[category].items():
                if relative!='CURRENT_LOCAL_RESUME.md':
                    verify(relative,expected)
        return result

    def read(relative):
        path = (evidence.root/relative).resolve()
        if str(path.relative_to(evidence.root)) not in verified:
            raise RuntimeError('Unowned result '+relative)
        if path.suffix=='.json':
            return json.loads(path.read_text())
        with np.load(path,allow_pickle=False) as archive:
            return {name:archive[name].copy() for name in archive.files}

    def save(name,value):
        path = evidence.output/(name+'.json')
        with path.open('x') as stream:
            stream.write(json.dumps(value,indent=2,allow_nan=False)+'\n')
        evidence.own(path,'outputs')
        return str(path.relative_to(evidence.root))

    try:
        original = status('annular-repaired-compatibility-attempt02')
        previous = status('annular-integrated-baseline-assembly-attempt01')
        exact_witnesses = 0
        with localcontext() as context:
            context.prec = 70
            for short,branch in [('reference','reference-reference'),('MTS','MTS-primary')]:
                transport = status('annular-matter-gravity-'+short+'-third-attempt01')
                integrated = status('annular-coefficient-baseline-'+short+'-third-attempt03')
                evidence.check(short+':matching_branch',transport['branch']==branch and integrated['branch']==branch)
                high = read(integrated['rule_outputs'][-1]['path'])
                results = {(row['summary']['mode'],row['summary']['order']):read(row['path'])['summary'] for row in transport['results']}
                converted = {key:{name:[Decimal(value) for value in data[name]] for name in ['gravity','dust_radial','combined']}
                    for key,data in results.items()}
                pair = max(abs(converted[(mode,20)]['combined'][index]-converted[(mode,12)]['combined'][index])
                    for mode in ['nodal_contraction','rounded_coefficients'] for index in range(3))
                evidence.check(short+':refined_quadrature',pair<Decimal('1e-22'),str(pair))
                source_spread = np.r_[0.,[float(abs(first-last)) for first,last in zip(
                    converted[('nodal_contraction',20)]['combined'],converted[('rounded_coefficients',20)]['combined'])]]
                pair_error = np.r_[0.,[float(max(abs(converted[(mode,20)]['combined'][index]-converted[(mode,12)]['combined'][index])
                    for mode in ['nodal_contraction','rounded_coefficients'])) for index in range(3)]]
                for mode in ['nodal_contraction','rounded_coefficients']:
                    combined = converted[(mode,20)]['combined']
                    direct = [Decimal.from_float(float(high['baseline'][0]))]
                    transported = [direct[0]]
                    for index in range(3):
                        direct.append(Decimal.from_float(float(high['accumulated'][1,index+1]))
                            +Decimal.from_float(float(high['held_native'][index+1]))+combined[index])
                        transported.append(Decimal.from_float(float(high['baseline'][index+1]))+combined[index]
                            -Decimal.from_float(float(high['held_dust'][index]))-Decimal.from_float(float(high['held_gravity'][index])))
                    baseline = np.array(direct,float)
                    assembly_spread = np.array([float(abs(first-last)) for first,last in zip(direct,transported)])
                    float_loss = np.array([float(abs(value-Decimal.from_float(float(value)))) for value in direct])
                    added_error = source_spread+pair_error+assembly_spread+float_loss
                    added_error[0] = 0.
                    origin = dict(branch=branch,source_mode=mode,direct_decimal=list(map(str,direct)),
                        correction_assembly_decimal=list(map(str,transported)),
                        change_from_previous=(baseline-high['baseline']).tolist(),source_spread=source_spread.tolist(),
                        pair_error=pair_error.tolist(),assembly_spread=assembly_spread.tolist(),float_loss=float_loss.tolist(),
                        added_error=added_error.tolist(),old_allowances_retained=True,physical_precision_inferred=False,valid_for_claim=False)
                    save(short+'-'+mode+'-baseline',origin)
                    for variant in ['rounded_coefficients','parent_nodal']:
                        prior_row = next(row for row in previous['summaries'] if row['branch']==branch and row['source_variant']==variant
                            and row['baseline_scenario']=='coefficient_retained_envelope')
                        original_row = next(row for row in original['summaries'] if row['branch']==branch and row['source_variant']==variant
                            and row['baseline_variant']=='separate_C0_baseline')
                        prior,old = read(prior_row['path']),read(original_row['path'])
                        evidence.check(short+':'+mode+':'+variant+':held_columns',prior['columns']==old['columns'] and prior['column_error']==old['column_error'])
                        columns,column_error = np.array(prior['columns']),np.array(prior['column_error'])
                        for scenario,error in [('locked_original',np.array(old['baseline_error'])),
                            ('locked_previous',np.array(prior['baseline_error'])),
                            ('accounted',np.array(prior['baseline_error'])+added_error)]:
                            diagnostic = diagnose(baseline,columns,error,column_error)
                            exact = envelope_search(baseline,columns,error,column_error)
                            evidence.check(short+':'+mode+':'+variant+':'+scenario+':rank_held',diagnostic['singular_values']==prior['diagnostic']['singular_values'])
                            for orthant in exact['orthants']:
                                witness = orthant['exact_witness']
                                if witness is None:
                                    continue
                                amplitudes = [orthant['signs'][index]*Fraction(int(witness['numerator'][index]),int(witness['denominator'])) for index in range(3)]
                                for row in range(4):
                                    residual = Fraction.from_float(float(baseline[row]))+sum(
                                        Fraction.from_float(float(columns[row,index]))*amplitudes[index] for index in range(3))
                                    budget = Fraction.from_float(float(error[row]))+sum(
                                        Fraction.from_float(float(column_error[row,index]))*abs(amplitudes[index]) for index in range(3))
                                    if abs(residual)>budget:
                                        raise RuntimeError('Exact witness failed original equations')
                                exact_witnesses += 1
                            candidate = diagnostic['candidates'][0]
                            detail = dict(branch=branch,source_mode=mode,source_variant=variant,scenario=scenario,
                                baseline=baseline.tolist(),baseline_error=error.tolist(),columns=columns.tolist(),column_error=column_error.tolist(),
                                diagnostic=diagnostic,envelope_search=exact,valid_for_claim=False)
                            path = save(short+'-'+mode+'-'+variant+'-'+scenario,detail)
                            summary = dict(branch=branch,source_mode=mode,source_variant=variant,scenario=scenario,
                                rank_resolved=diagnostic['rank_resolved'],representative_h2=candidate['residual'][3],
                                representative_h2_budget=candidate['sampled_uncertainty'][3],
                                representative_within=candidate['within_sampled_uncertainty'],exact_feasible=exact['any_replayed_witness'],
                                prior_exact_original=old['envelope_search']['any_replayed_witness'],
                                prior_exact_previous=prior['envelope_search']['any_replayed_witness'],path=path,valid_for_claim=False)
                            summaries.append(summary)
                            print(json.dumps(summary),flush=True)
                evidence.report.update(summaries=summaries)
                evidence.save()
        evidence.report.update(exact_witnesses_replayed=exact_witnesses,columns_held=True,wave_native_force_held=True,
            all_old_allowances_retained=True,no_continuum_precision_inferred=True,github_action=False,subagents_used=False)
        evidence.complete()
    except Exception as error:
        evidence.fail(error)
        raise


if __name__=='__main__':
    main()

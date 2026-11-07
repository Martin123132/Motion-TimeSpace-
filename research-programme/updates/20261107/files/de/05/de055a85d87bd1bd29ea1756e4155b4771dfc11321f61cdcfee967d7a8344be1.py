from derive_annular_source_gravity_20260914 import EvidenceRun
from annular_position_enabled_compatibility_20260930 import diagnose
from annular_exact_envelope_20261001 import envelope_search
from decimal import Decimal, localcontext
from fractions import Fraction
import hashlib
import json
import numpy as np


def main():
    evidence = EvidenceRun('annular-C1-integrated-assembly-attempt01', __file__)
    verified, summaries = {}, []

    def verify(relative, expected=None):
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
        data = json.loads(verify(str(path.relative_to(evidence.root))).read_text())
        evidence.check(name+':complete',data['state']=='complete' and all(row['passed'] for row in data['checks']))
        for category in ['inputs','outputs']:
            for relative, expected in data[category].items():
                if relative!='CURRENT_LOCAL_RESUME.md':
                    verify(relative,expected)
        return data

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
        evidence.own(evidence.root/'DERIVATION-20261001-C1-integral-contract.md')
        previous = status('annular-matter-gravity-assembly-attempt01')
        witnesses = 0
        with localcontext() as context:
            context.prec = 90
            exact_float = lambda value:Decimal.from_float(float(value))
            for short,branch in [('reference','reference-reference'),('MTS','MTS-primary')]:
                wave = status('annular-C1-material-'+short+'-third-attempt01')
                matter = status('annular-C1-matter-gravity-'+short+'-third-attempt01')
                evidence.check(short+':matching_branch',wave['branch']==branch and matter['branch']==branch)
                low,high = [read(row['path']) for row in wave['rule_outputs']]
                evidence.check(short+':fixed_material_rules',np.array_equal(low['quadrature'],[12,48])
                    and np.array_equal(high['quadrature'],[12,64]))
                for order,data in [(48,low),(64,high)]:
                    replay = np.einsum('l,lrc->rc',data['weights'],data['layers'])
                    evidence.check(short+':wave_resum-'+str(order),np.array_equal(replay,data['accumulated']))
                results = {(item['summary']['mode'],item['summary']['order']):item['summary'] for item in matter['results']}
                parsed = {key:np.array([Decimal(value) for value in row['combined']],dtype=object) for key,row in results.items()}
                wave_corrections = [np.array([exact_float(new)-exact_float(old) for new,old in zip(
                    data['accumulated'][2],data['accumulated'][0])],dtype=object) for data in [low,high]]
                wave_pair = np.asarray(abs(wave_corrections[1]-wave_corrections[0]),float)
                geometry_spread = np.maximum(abs(low['accumulated'][1]-low['accumulated'][0]),
                    abs(high['accumulated'][1]-high['accumulated'][0]))
                source_spread = np.asarray(abs(parsed['nodal_contraction',20]-parsed['rounded_coefficients',20]),float)
                matter_pair = np.maximum(*[np.asarray(abs(parsed[mode,20]-parsed[mode,12]),float) for mode in matter['source_modes']])
                evidence.check(short+':matter_quadrature_gate',float(np.max(matter_pair))<1e-22,matter_pair.tolist())
                addition_spread = np.maximum(abs(low['rounding_spread']),abs(high['rounding_spread']))
                for mode in matter['source_modes']:
                    combined = parsed[mode,20]
                    old = high['historical_total']
                    complete = [exact_float(old[0])]
                    shifted = [exact_float(old[0])]
                    for index in range(3):
                        complete.append(exact_float(old[index+1])+wave_corrections[1][index]+combined[index]
                            -exact_float(high['accumulated'][3,index])-exact_float(high['gravity'][index]))
                        shifted.append(exact_float(high['revised_wave_only'][index+1])+combined[index]
                            -exact_float(high['accumulated'][3,index])-exact_float(high['gravity'][index]))
                    updated = np.array(complete,float)
                    assembly_spread = np.array([float(abs(first-last)) for first,last in zip(complete,shifted)])
                    cast_error = np.array([float(abs(value-exact_float(binary))) for value,binary in zip(complete,updated)])
                    extra = np.r_[0.,wave_pair+geometry_spread+source_spread+matter_pair+addition_spread]+assembly_spread+cast_error
                    origin = dict(branch=branch,source_mode=mode,old=old.tolist(),updated=updated.tolist(),
                        precise_updated=list(map(str,complete)),wave_delta=np.asarray(wave_corrections[1],float).tolist(),
                        matter_gravity_delta=[float(combined[index]-exact_float(high['accumulated'][3,index])
                            -exact_float(high['gravity'][index])) for index in range(3)],
                        geometry_spread=geometry_spread.tolist(),wave_pair=wave_pair.tolist(),matter_pair=matter_pair.tolist(),
                        source_spread=source_spread.tolist(),assembly_spread=assembly_spread.tolist(),cast_error=cast_error.tolist(),
                        added_error=extra.tolist(),old_allowances_retained=True,valid_for_claim=False)
                    save(short+'-'+mode+'-column',origin)
                    for variant in ['rounded_coefficients','parent_nodal']:
                        for scenario in ['locked_original','locked_previous','accounted']:
                            prior_row = next(row for row in previous['summaries'] if row['branch']==branch and row['source_mode']==mode
                                and row['source_variant']==variant and row['scenario']==scenario)
                            prior = read(prior_row['path'])
                            baseline,columns = np.array(prior['baseline']),np.array(prior['columns'])
                            baseline_error,column_error = np.array(prior['baseline_error']),np.array(prior['column_error'])
                            evidence.check(short+':'+mode+':'+variant+':'+scenario+':C1_authority',
                                np.array_equal(columns[:,1],old), (columns[:,1]-old).tolist())
                            columns[:,1] = updated
                            if scenario=='accounted':
                                column_error[:,1] += extra
                            evidence.check(short+':'+mode+':'+variant+':'+scenario+':held_terms',
                                np.array_equal(columns[:,[0,2]],np.array(prior['columns'])[:,[0,2]])
                                and np.array_equal(columns[0],np.array(prior['columns'])[0]))
                            diagnostic = diagnose(baseline,columns,baseline_error,column_error)
                            exact = envelope_search(baseline,columns,baseline_error,column_error)
                            for orthant in exact['orthants']:
                                witness = orthant['exact_witness']
                                if witness is None:
                                    continue
                                amplitudes = [orthant['signs'][index]*Fraction(int(witness['numerator'][index]),int(witness['denominator'])) for index in range(3)]
                                for row in range(4):
                                    residual = Fraction.from_float(float(baseline[row]))+sum(
                                        Fraction.from_float(float(columns[row,index]))*amplitudes[index] for index in range(3))
                                    allowance = Fraction.from_float(float(baseline_error[row]))+sum(
                                        Fraction.from_float(float(column_error[row,index]))*abs(amplitudes[index]) for index in range(3))
                                    if abs(residual)>allowance:
                                        raise RuntimeError('Invalid exact witness')
                                witnesses += 1
                            candidate = diagnostic['candidates'][0]
                            data = dict(branch=branch,source_mode=mode,source_variant=variant,scenario=scenario,
                                baseline=baseline.tolist(),baseline_error=baseline_error.tolist(),columns=columns.tolist(),
                                column_error=column_error.tolist(),diagnostic=diagnostic,envelope_search=exact,
                                prior_path=prior_row['path'],valid_for_claim=False)
                            path = save(short+'-'+mode+'-'+variant+'-'+scenario,data)
                            summary = dict(branch=branch,source_mode=mode,source_variant=variant,scenario=scenario,
                                rank_resolved=diagnostic['rank_resolved'],representative_h2=candidate['residual'][3],
                                representative_within=candidate['within_sampled_uncertainty'],
                                prior_representative_h2=prior['diagnostic']['candidates'][0]['residual'][3],
                                exact_feasible=exact['any_replayed_witness'],prior_exact_feasible=prior['envelope_search']['any_replayed_witness'],
                                path=path,valid_for_claim=False)
                            summaries.append(summary)
                            print(json.dumps(summary),flush=True)
                evidence.report.update(summaries=summaries)
                evidence.save()
        evidence.report.update(exact_witnesses_replayed=witnesses,force_baseline_C0_C2_held=True,
            original_reaction_position_uncertainties_retained=True,finite_history_established=False,
            github_action=False,subagents_used=False)
        evidence.complete()
    except Exception as error:
        evidence.fail(error)
        raise


if __name__=='__main__':
    main()

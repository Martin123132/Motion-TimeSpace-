from __future__ import annotations

from onset_common import *


def main():
    modest()
    folder=ROOT/'results/validation'
    folder.mkdir(parents=True,exist_ok=False)
    checks=[]
    inputs=[]

    def check(name,passed,value=None,limit=None):
        checks.append(dict(name=name,passed=bool(passed),value=value,limit=limit))

    def read(relative):
        path=ROOT/relative
        packet=json.loads(path.read_text())
        assert packet['state']=='complete'
        assert (path.parent/'COMPLETE').is_file()
        for source,expected in packet['input_hashes'].items():
            assert digest(source)==expected,(path,source)
        inputs.append(path)
        return packet

    symbolic=read('results/derivation/status.json')
    for row in symbolic['checks']:
        check('algebra: '+row['name'],row['passed'])
    for label in ['heavy-base','heavy-early','heavy-fine','cold-base','lcdm-base']:
        report=read('runs/'+label+'/status.json')
        check(label+' finite',report['finite'])
        check(label+' background agreement',report['max_H_relative_error']<.001,report['max_H_relative_error'],.001)
        check(label+' momentum constraint',report['max_scaled_momentum_residual']<1e-5,report['max_scaled_momentum_residual'],1e-5)
        check(label+' native exact domain',report['final_scale']<.00028)
    original=read('results/native-comparison/status.json')
    for row in original['rows']:
        if row['primary'] and row['branch']!='heavy':
            check('native '+row['branch']+' '+row['quantity']+' '+str(row['k_Mpc_inverse']),row['qualified'],row['envelope_relative_error'],.01)
    check('Original failing heavy comparisons not promoted',not original['all_primary_passed'])
    corrected=read('results/resolved-comparison-valid/status.json')
    for row in corrected['rows']:
        if row['source_variant']=='corrected-early-slow' and row['primary']:
            check('corrected native '+row['quantity']+' '+str(row['k_Mpc_inverse']),row['qualified'],row['envelope_relative_error'],.01)
    original_slow=[row for row in corrected['rows'] if row['source_variant']=='original-dense' and row['primary'] and row['quantity']=='field_s']
    check('Source defect remains exposed with dense output',all(not row['qualified'] for row in original_slow))
    precision=read('results/source-precision/status.json')
    by_label={row['label']:row for row in precision['rows']}
    check('Tiny-velocity precision control converges',by_label['component-resolved']['max_velocity_relative_error']<.001,
        by_label['component-resolved']['max_velocity_relative_error'],.001)
    check('Coarse absolute tolerance fails velocity accuracy',by_label['old-absolute-tolerance']['max_velocity_relative_error']>.01,
        by_label['old-absolute-tolerance']['max_velocity_relative_error'],.01)
    base=np.load(ROOT/'runs/heavy-base/trajectory.npz')
    base_names=base['names'].tolist()
    base_volume=float(base['values'][base_names.index('s'),-1])
    occupation=read('results/occupation/status.json')
    baseline=np.load(ROOT/'results/occupation/base.npz')['energy_response']
    for variant in ['early','fine']:
        packet=np.load(ROOT/'runs'/('heavy-'+variant)/'trajectory.npz')
        volume_error=abs(float(packet['values'][base_names.index('s'),-1])/base_volume-1)
        energy=np.load(ROOT/'results/occupation'/(variant+'.npz'))['energy_response']
        error=float(max(abs(energy-baseline))/max(abs(baseline)))
        check(variant+' volume convergence',volume_error<.001,volume_error,.001)
        check(variant+' energy-response convergence',error<.005,error,.005)
    for row in occupation['variation_diagnostics']:
        check(row['variant']+' independent energy quadrature',row['energy_transport_integral_relative_residual']<1e-3,
            row['energy_transport_integral_relative_residual'],1e-3)
    selected=occupation['selected_rows']
    summaries=[]
    for row in selected:
        peers=[candidate for candidate in occupation['rows'] if candidate['scale']==row['scale']]
        physical=np.array([peer['physical_occupation_response_Mpc2'] for peer in peers])
        wkb=np.array([peer['WKB_occupation_response_Mpc2'] for peer in peers])
        summaries.append(dict(scale=row['scale'],physical_min=float(min(physical)),physical_max=float(max(physical)),
            WKB_min=float(min(wkb)),WKB_max=float(max(wkb)),
            physical_spread_relative=float(np.ptp(physical)/abs(row['physical_occupation_response_Mpc2'])),
            WKB_spread_relative=float(np.ptp(wkb)/abs(row['WKB_occupation_response_Mpc2']))))
    condition=max(row['condition_number'] for row in occupation['rows'])
    check('Phase projection design conditioning',condition<1e5,condition,1e5)
    check('Sub-roundoff native attempt retained as failed',
        (ROOT/'results/resolved-comparison/FAILED.md').is_file() and not (ROOT/'results/resolved-comparison/COMPLETE').exists())
    for path in ROOT.glob('*.py'):
        compile(path.read_bytes(),str(path),'exec')
        check('Compile '+path.name,True)
    all_passed=all(row['passed'] for row in checks)
    report=dict(checks=checks,count=len(checks),all_checks_passed=all_passed,occupation_window_summaries=summaries,
        final_volume_response_Mpc2=base_volume,initial_native_comparison_passed=False,
        corrected_early_source_comparison_passed=corrected['corrected_primary_pass'],
        late_global_background_repaired=False,actual_survey_refit=False,new_parameters_fitted=0,
        qualification='Derived onset transport; native early-source correction is a scoped validation candidate. Full inherited slow-source regeneration and downstream sensitivity test remain next.')
    finish(folder,report,__file__,inputs)
    print(json.dumps(report),flush=True)
    if not all_passed:
        raise RuntimeError('Acceptance checks failed; see preserved validation report')


if __name__=='__main__':
    main()

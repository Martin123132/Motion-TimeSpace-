from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path

import numpy as np

from carrier import ROOT, BRANCH, PARENT, PRIOR, digest, read_json, write_json, modest_process, orbit_series, numerical_geometry, imported_hashes
from sidebands import polar_settings
from polar_source import coefficients, harmonic_value
from eccentric_source import orbit_constants
from secular import frequencies


def main():
    modest_process()
    checks, inputs = [], {}

    def check(name, passed, value=None, tolerance=None):
        checks.append(dict(name=name,passed=bool(passed),value=value,tolerance=tolerance))

    def below(name,value,tolerance):
        check(name,np.isfinite(value) and value<=tolerance,float(value),tolerance)

    def load(path,script):
        report=read_json(path)
        inputs[str(path)]=digest(path)
        check(str(path)+'complete',report['state']=='complete')
        check(str(path)+'producer current',report['script_sha256']==digest(ROOT/script))
        for source,expected in report.get('input_hashes',{}).items():
            check(str(path)+'input '+source,Path(source).is_file() and digest(source)==expected)
        return report

    exact_count=0
    for label,script,count in [('derivation','derive_carrier.py',13),('weak-field','derive_weak_field.py',7)]:
        report=load(ROOT/'results'/label/'status.json',script)
        check(label+'exact identities',len(report['checks'])==count and all(row['passed'] and row['residual']=='0' for row in report['checks']))
        exact_count+=len(report['checks'])
    mode_count=0
    for setting in ['fine','coarse']:
        for plan,count in [('pilot',14),('nodes',112),('extension',112)]:
            label=plan+'-'+setting
            directory=ROOT/'results'/label
            report=load(directory/'status.json','run_carriers.py')
            check(label+'requested count',len(report['rows'])==count)
            check(label+'completion marker',(directory/'COMPLETE').is_file())
            mode_count+=len(report['rows'])
            check(label+'unique modes',len({(row['separation'],row['sector'],row['fractional_frequency_shift']) for row in report['rows']})==count)
            for row in report['rows']:
                prefix=label+str((row['separation'],row['sector'],row['fractional_frequency_shift']))
                with np.load(directory/row['archive'],allow_pickle=False) as archive:
                    check(prefix+'finite saved solution',all(np.isfinite(archive[key]).all() for key in archive.files))
                    check(prefix+'actual interior archived',('spline_coefficients' if row['sector']=='polar' else 'interior_values') in archive.files)
                    below(prefix+'archived frequency',abs(float(archive['frequency'])/row['frequency']-1),1e-14)
                below(prefix+'Wronskian',row['Wronskian_error'],1e-7)
                below(prefix+'unit outgoing current',row['outgoing_diagnostic']['infinity_flux_normalization_error'],1e-11)
                below(prefix+'unit horizon current',row['horizon_diagnostic']['horizon_flux_normalization_error'],1e-11)
                for index,response in enumerate(row['responses']):
                    below(prefix+str(index)+'optical work',response['optical_error'],1e-10)
                    below(prefix+str(index)+'direct reconstruction',response['direct_error'],1e-7)
                if row['sector']=='polar':
                    below(prefix+'coupled interior',row['interior_maximum_residual'],1.001*polar_settings(setting)['interior_tolerance'])
                    below(prefix+'boundary condition',row['interior_boundary_residual'],1e-8)
    reports={}
    for setting in ['fine','coarse']:
        report=load(ROOT/'results'/('analysis-full-'+setting)/'status.json','analyze_carriers.py')
        reports[setting]=report
        check(setting+'17 radii',len({row['separation'] for row in report['shrinkage_laws']})==17)
        for row in report['carrier_laws']:
            below(setting+'carrier optical derivative '+str((row['separation'],row['sector'])),row['optical_second_relative_error'],1e-9)
        for row in report['shrinkage_laws']:
            prefix=setting+str((row['separation'],row['component'],row['channel']))
            below(prefix+'energy versus angular action',row['energy_angular_P2_relative_error'],1e-9)
            below(prefix+'frequency step refinement',row['frequency_step_relative_change'],1e-6)
        for row in report['finite_e_comparisons']:
            below(setting+'held-out finite-e P2 '+str((row['component'],row['channel'])),row['small_pair_relative_error'],1e-6)
        for row in report['finite_amplitude_controls']:
            below(setting+'held-out finite-e amplitude '+str((row['sector'],row['amplitude'])),row['small_pair_relative_error'],1e-6)
    resolution=[]
    for row in reports['fine']['shrinkage_laws']:
        coarse=next(other for other in reports['coarse']['shrinkage_laws'] if other['component']==row['component'] and
                    other['channel']==row['channel'] and abs(other['separation']-row['separation'])<1e-10)
        error=abs(coarse['P2']/row['P2']-1)
        resolution.append(error)
        below('P2 radial resolution '+str((row['separation'],row['component'],row['channel'])),error,1e-6)
    for semilatus in [20.,100.,332.6905215498321]:
        mass=.296546804477414
        radius=mass*semilatus
        energy,angular=orbit_constants(mass,semilatus,0.)
        frequency=2/(mass*semilatus**1.5)
        source=numerical_geometry('polar')(radius,mass,energy,angular,2,frequency,harmonic_value(2))
        def old(velocity):
            return coefficients(dict(radius=radius,coordinate_velocity=velocity,phase=0.,
                                proper_velocity=energy*velocity/(1-2*mass/radius)),mass,energy,angular,2)
        center=old(0.)
        plus,minus=old(.02),old(-.02)
        velocity_squared=((plus['delta']+minus['delta'])/2-center['delta'])/.02**2
        slope_velocity=-((plus['delta_prime']+minus['delta_prime'])/2-center['delta_prime'])/.02**2
        below('independent polar v2 delta '+str(semilatus),abs(velocity_squared/source[4]-1),1e-10)
        below('independent polar v2 slope '+str(semilatus),abs(slope_velocity/source[5]-1),1e-10)
        omega0=1/(mass*semilatus**1.5)
        estimates=[]
        for eccentricity in [.005,.01]:
            radial_frequency,angular_frequency=frequencies(mass,semilatus,eccentricity)
            estimates.append((angular_frequency/omega0-1)/eccentricity**2)
        extrapolated=(4*estimates[0]-estimates[1])/3
        below('independent geodesic clock '+str(semilatus),
              abs(extrapolated/orbit_series(semilatus)['angular_frequency_fraction']-1),1e-7)
    clock=load(ROOT/'results/clock/status.json','integrate_clock.py')
    for label,errors in clock['comparisons'].items():
        if label!='nested5':
            below(label+'integrated clock control',max(errors),1e-6)
    check('five-node phase correction is flagged and refined',max(clock['comparisons']['nested5'])>1e-6 and max(clock['comparisons']['nested9'])<1e-7)
    below('independent clock ODE',max(clock['ode_relative_errors']),1e-9)
    for channel in ['BH','body']:
        first,second=[row for row in clock['order_controls'] if row['channel']==channel]
        ratios=np.array(second['remainder'])/np.array(first['remainder'])
        below(channel+'omitted terms scale as initial e4',max(abs(ratios/4-1)),.003)
    endpoint=clock['endpoint']
    check('example strictly small-e expansion',endpoint['initial_eccentricity']==.01)
    check('eccentric clock and phase corrections have Newtonian signs',
          endpoint['eccentricity_clock_fraction_BH']>0 and endpoint['eccentricity_phase_fraction_BH']<0)
    below('finite radius deviations from derived weak-field primitives',max(abs(np.array(clock['finite_radius_corrections_to_weak']))),.03)
    prior_path=PARENT/'results/validation/status.json'
    prior=read_json(prior_path)
    inputs[str(prior_path)]=digest(prior_path)
    for primary in prior['primary_pdfs']:
        check('primary archived PDF '+primary['path'],Path(primary['path']).is_file() and digest(primary['path'])==primary['sha256'])
    failed=[row for row in checks if not row['passed']]
    directory=ROOT/'results/validation'
    directory.mkdir(parents=True,exist_ok=False)
    result=dict(state='failed' if failed else 'complete',script_sha256=digest(__file__),
           time_utc=datetime.now(timezone.utc).isoformat(),input_hashes={**inputs,**imported_hashes()},
           checks=checks,exact_checks=exact_count,wave_mode_evaluations=mode_count,
           primary_pdfs=prior['primary_pdfs'],source_urls=prior['source_urls'],
           maximum_P2_resolution=max(resolution),
           maximum_finite_P2_error=max(row['small_pair_relative_error'] for report in reports.values() for row in report['finite_e_comparisons']),
           maximum_finite_amplitude_error=max(row['small_pair_relative_error'] for report in reports.values() for row in report['finite_amplitude_controls']),
           maximum_clock_resolution=max(clock['comparisons']['coarse']),
           maximum_frequency_step_change=max(row['frequency_step_relative_change'] for report in reports.values() for row in report['shrinkage_laws']),
           note='Correlated numerical/provenance checks; frequency derivative is a controlled numerical derivative, not an eccentricity fit.')
    write_json(directory/'status.json',result,exclusive=True)
    print(dict(checks=len(checks),failed=failed[:15],wave_evaluations=mode_count,exact_checks=exact_count,
               maximum_P2_resolution=max(resolution)),flush=True)
    assert not failed,str(len(failed))+' validation failures'


if __name__=='__main__':
    main()


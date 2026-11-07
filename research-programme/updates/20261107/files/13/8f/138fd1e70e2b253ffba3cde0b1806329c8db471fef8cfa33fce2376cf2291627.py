import argparse
from thermal_event_source import *


def main(arguments):
    modest()
    mp.mp.dps=65
    folder=ROOT/'results'/arguments.name
    folder.mkdir(parents=True,exist_ok=False)
    source=PARENT/'results/angular-refinement/status.json'
    packet=json.loads(source.read_text())
    assert packet['all_checks_passed']
    benchmark=packet['result']
    energy=mp.mpf(str(benchmark['energy']))
    cosine=mp.mpf(str(benchmark['hard_cosine']))
    temperature=mp.mpf(str(benchmark['temperature']))
    profile=None if arguments.profile is None else temperature*mp.mpf(arguments.profile)
    result=matched_event_source(energy,cosine,temperature,arguments.angular,arguments.radial,
                                mp.mpf(str(benchmark['amplitude_interference_over_bare'])),
                                arguments.cutoff,profile,mp.mpf(arguments.lower))
    total=result['total']
    closure=mp.matrix([total[index+1]+total[index+5] for index in range(4)])
    rows={key:[float(value) for value in result['pieces'][key]] for key in ['total','paired','absorption_tail','hard_stimulation','born']}
    checks=[check('Full photons and independent on-shell electrons balance including dressed event shift',mp.norm(closure),1e-40),
            check('Azimuth-reflection transverse source cancels',max(abs(total[3]),abs(total[7])),1e-40),
            check('Integrated thermal soft coefficient agrees with invariant cusp',abs(result['pieces']['integrated_pole']-real.cusp(energy,cosine)),1e-18)]
    vector=[float(value) for value in total]
    report=dict(checks=checks,count=len(checks),all_checks_passed=all(row['passed'] for row in checks),
                energy=float(energy),temperature=float(temperature),hard_cosine=float(cosine),angular_order=arguments.angular,
                radial_order=arguments.radial,bose_tail_cutoff_over_temperature=arguments.cutoff,
                soft_lower_over_temperature=float(arguments.lower),profile_over_temperature=arguments.profile,
                thermal_correction_vector=vector,components=rows,
                finite_virtual_interference=float(benchmark['amplitude_interference_over_bare']),
                phase_space_correction=float(result['response']['phase_delta']),
                hard_bose_shift=float(result['response']['bose_delta']),
                virtual_matching_conversion=float(result['profile_conversion']),
                normalization='Relative to elastic Born differential rate including final hard Bose enhancement; moment units m_e=c=hbar=1',
                component_order=['event_rate','photon_energy','photon_px','photon_py','photon_pz',
                                 'electron_energy','electron_px','electron_py','electron_pz'],
                scope='Conditional resting-electron forward event source, photon-cut thermal sector; not a complete equilibrium bath collision operator',
                vacuum_component_inherited_separately=True,physical_photon_number_source_not_assigned=True,
                no_new_empirical_fit=True)
    finish(folder,report,__file__,[ROOT/'thermal_event_source.py',source,VACUUM/'ordered_real_kernel.py',VACUUM/'source_four_force.py'])
    print(json.dumps(dict(checks=len(checks),failed=[row for row in checks if not row['passed']],name=arguments.name,
                          thermal_correction_vector=vector,profile_conversion=report['virtual_matching_conversion'])),flush=True)


if __name__=='__main__':
    parser=argparse.ArgumentParser()
    parser.add_argument('--name',required=True)
    parser.add_argument('--angular',required=True,type=int)
    parser.add_argument('--radial',required=True,type=int)
    parser.add_argument('--cutoff',default=60,type=int)
    parser.add_argument('--profile')
    parser.add_argument('--lower',default='0')
    main(parser.parse_args())

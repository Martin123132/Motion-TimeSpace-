from thermal_source_common import *


def main():
    modest()
    folder=ROOT/'results/matched-source-validation'
    folder.mkdir(parents=True,exist_ok=False)
    names=['thermal-a4-r24','thermal-a6-r40','thermal-a8-r56','thermal-profile02','thermal-profile1',
           'thermal-profile3','thermal-tail80','thermal-lower4','thermal-lower6']
    paths=[ROOT/'results'/name/'status.json' for name in names]
    packets={name:json.loads(path.read_text()) for name,path in zip(names,paths)}
    assert all(packet['all_checks_passed'] for packet in packets.values())
    baseline=np.array(packets['thermal-a8-r56']['thermal_correction_vector'])
    comparison=np.array(packets['thermal-a6-r40']['thermal_correction_vector'])
    checks,rows=[],[]
    indices=[0,1,2,4,5,6,8]
    for name in ['thermal-a4-r24','thermal-a6-r40','thermal-profile02','thermal-profile1','thermal-profile3','thermal-tail80']:
        values=np.array(packets[name]['thermal_correction_vector'])
        errors=abs((values[indices]-baseline[indices])/baseline[indices])
        checks.append(check('Every nonzero source component refinement/profile/tail gate: '+name,max(errors),1e-7))
        rows.append(dict(name=name,maximum_relative_component_difference=float(max(errors))))
        if 'profile' in name:
            correction=packets[name]['virtual_matching_conversion']
            checks.append(dict(name='Dropping matched virtual conversion changes source: '+name,passed=abs(correction)>abs(baseline[0])*.001))
    low4=np.array(packets['thermal-lower4']['thermal_correction_vector'])
    low6=np.array(packets['thermal-lower6']['thermal_correction_vector'])
    ratio=(comparison[0]-low4[0])/(comparison[0]-low6[0])
    checks.append(check('Actual integrated lower-cut error decreases linearly',abs(ratio/100-1),.001))
    checks.append(check('Small lower cut resolves finite rate',abs(low6[0]/comparison[0]-1),1e-6))
    vac_force_path=VACUUM/'results/four-force-a12-r40/status.json'
    vac_rate_path=VACUUM/'results/ordered-real-a16-r56/status.json'
    vacuum_forces=json.loads(vac_force_path.read_text())
    vacuum_rates=json.loads(vac_rate_path.read_text())
    force=next(row for row in vacuum_forces['rows'] if row['energy']<.001 and row['cosine']==.1)
    rate=next(row for row in vacuum_rates['rows'] if row['energy']<.001 and row['cosine']==.1)
    vacuum=np.array([rate['matched_ratio'],*force['photon_source'],*force['electron_source']])
    born=np.array([1,*force['born_photon_source'],*force['born_electron_source']])
    full=born+vacuum+baseline
    checks.append(check('Combined inherited vacuum plus thermal four-force closes',np.linalg.norm(full[1:5]+full[5:9]),1e-18))
    ratio_energy=baseline[1]/born[1]
    checks.append(dict(name='Scalar event-rate multiplier fails energy-transfer correction',passed=abs(ratio_energy-baseline[0])>10*abs(baseline[0])))
    summary=dict(thermal_rate_correction=float(baseline[0]),thermal_photon_energy_correction=float(baseline[1]),
                 thermal_energy_transfer_fraction_of_Born=float(ratio_energy),
                 vacuum_plus_thermal_relative_rate_correction=float(vacuum[0]+baseline[0]),
                 combined_source_vector=full.tolist(),thermal_correction_vector=baseline.tolist(),
                 scope='Resting-electron conditional unpolarized forward source in an isotropic Planck photon bath; photon-cut loop sector only',
                 normalization='Born elastic differential rate including final hard Bose enhancement; energy/momentum in electron rest units')
    finish(folder,dict(checks=checks,count=len(checks),all_checks_passed=all(row['passed'] for row in checks),rows=rows,summary=summary,
                       finite_matching_profile_cancels=True,full_kinetic_operator_not_inferred_from_conditional_rate=True),__file__,
           [*paths,vac_force_path,vac_rate_path])
    print(json.dumps(dict(checks=len(checks),failed=[row for row in checks if not row['passed']],summary=summary,rows=rows)),flush=True)


if __name__=='__main__':
    main()

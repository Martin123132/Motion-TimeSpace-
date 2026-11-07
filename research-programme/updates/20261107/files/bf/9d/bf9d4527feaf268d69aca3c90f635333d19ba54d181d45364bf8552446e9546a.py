from thermal_event_source import *


def main():
    modest()
    mp.mp.dps=75
    folder=ROOT/'results/soft-endpoint'
    folder.mkdir(parents=True,exist_ok=False)
    checks,rows=[],[]
    energy=mp.mpf('.00045962015785263325')
    cosine=mp.mpf('.1')
    for soft_cosine_text,azimuth_text in [('-.4','.7'),('.6','2.1'),('.1','4.2')]:
        soft_cosine,azimuth=mp.mpf(soft_cosine_text),mp.mpf(azimuth_text)
        born=weight_vector(energy,energy/(1+energy*(1-cosine)),mp.mpf(0),cosine,soft_cosine,azimuth)
        pole=real.pole_density(*real.geometry(energy,cosine,soft_cosine,azimuth))
        samples=[]
        for fraction_text in ['1e-5','1e-7','1e-9']:
            soft=energy*mp.mpf(fraction_text)
            emission,bose_emission,emission_weight=signed_event(energy,soft,cosine,soft_cosine,azimuth,energy)
            crossed,bose_absorption,absorption_weight=signed_event(energy,-soft,cosine,soft_cosine,azimuth,energy)
            common=2*pole/soft*born
            paired=occupation(soft,energy)*(emission*bose_emission*emission_weight-crossed*bose_absorption*absorption_weight-common)
            missing_absorption=occupation(soft,energy)*(emission*bose_emission*emission_weight-common)
            number=occupation(soft,energy)*(emission*bose_emission+crossed*bose_absorption)
            samples.append(dict(soft=soft,paired=paired,missing_absorption=missing_absorption,number=number))
        label=' cosine='+soft_cosine_text+' azimuth='+azimuth_text
        first_difference=mp.norm(samples[0]['paired']-samples[1]['paired'])
        last_difference=mp.norm(samples[1]['paired']-samples[2]['paired'])
        checks.append(check('Paired finite endpoint approaches linearly'+label,abs(first_difference/last_difference/100-1),1e-3))
        checks.append(check('Finite endpoint rate stable'+label,abs(samples[1]['paired'][0]/samples[2]['paired'][0]-1),1e-6))
        ratio=abs(samples[2]['missing_absorption'][0]/samples[1]['missing_absorption'][0])
        checks.append(check('Omitting absorption exposes inverse-square divergence'+label,abs(ratio/10000-1),1e-6))
        number_limit=[sample['number']*sample['soft'] for sample in samples]
        checks.append(check('Physical photon-number moment has different infrared behavior'+label,abs(number_limit[-2]/number_limit[-1]-1),1e-6))
        checks.append(dict(name='Photon number was not projected to zero'+label,passed=bool(abs(number_limit[-1])>mp.mpf('1e-20'))))
        rows.append(dict(soft_cosine=float(soft_cosine),azimuth=float(azimuth),finite_endpoint_rate=float(samples[-1]['paired'][0]),
                         signed_photon_number_log_coefficient=float(number_limit[-1]),
                         photon_number_requires_kinetic_gain_loss_and_infrared_completion=True))
    finish(folder,dict(checks=checks,count=len(checks),all_checks_passed=all(row['passed'] for row in checks),rows=rows,
                       infrared_safe_event_moments_not_identified_with_photon_number=True),__file__,[ROOT/'thermal_event_source.py'])
    print(json.dumps(dict(checks=len(checks),failed=[row for row in checks if not row['passed']],rows=rows)),flush=True)


if __name__=='__main__':
    main()

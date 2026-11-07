from thermal_event_source import *


def main():
    modest()
    mp.mp.dps=65
    energy=mp.mpf('.00045962015785263325')
    cosine=mp.mpf('.1')
    response=phase_response(energy,cosine,energy)
    for name in ['mass_squared','hard_delta','phase_delta','bose_delta']:
        print(name,mp.nstr(response[name],18),flush=True)
    for fraction in ['.01','.0001','1e-6']:
        soft=energy*mp.mpf(fraction)
        cosine_soft,azimuth=mp.mpf('-.4'),mp.mpf('.7')
        born=weight_vector(energy,energy/(1+energy*(1-cosine)),mp.mpf(0),cosine,cosine_soft,azimuth)
        pole=real.pole_density(*real.geometry(energy,cosine,cosine_soft,azimuth))
        positive,bose_positive,positive_weight=signed_event(energy,soft,cosine,cosine_soft,azimuth,energy)
        negative,bose_negative,negative_weight=signed_event(energy,-soft,cosine,cosine_soft,azimuth,energy)
        paired=occupation(soft,energy)*(positive*bose_positive*positive_weight-negative*bose_negative*negative_weight-2*pole/soft*born)
        print('soft_pair',fraction,[mp.nstr(value,14) for value in paired],flush=True)


if __name__=='__main__':
    main()

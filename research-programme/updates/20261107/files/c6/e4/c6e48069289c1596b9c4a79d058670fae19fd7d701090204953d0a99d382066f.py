from stage168_common import *
from reconcile_reference import cardinal_weights
from fractions import Fraction


def main():
    modest()
    folder=ROOT/'results/profile-proof'
    folder.mkdir(parents=True,exist_ok=False)
    evaluator=HeldoutSources()
    checks=[]
    product=Fraction(3,4)*(Fraction(3,4)-Fraction(1,4))*(Fraction(3,4)-Fraction(1,2))*(Fraction(3,4)-1)
    assert product==Fraction(-3,128)
    for route in ['local','cubic']:
        predictor=np.array(evaluator.source_records[route]['predictor_weights'])
        error_weights=-predictor
        error_weights[3]=1
        for phase in np.linspace(0,1,129):
            warm=bubble(phase,route)
            profile=cold_bubble(phase,route)
            basic=np.array([(1-phase)*(1-2*phase)-.375*warm,warm,4*phase*(1-phase)-.75*warm,0.,phase*(2*phase-1)+.125*warm])
            close(checks,'Independent forecast/profile weight identity:'+route+':'+str(phase),
                cardinal_weights(phase,route)-profile*error_weights,basic,1e-10)
            full=evaluator.complete_packet(phase,route,'terminal',6)
            mapped=evaluator.reference_coordinates(full)
            anchors=evaluator.references['terminal_anchors'].copy()
            lower=decimal_array(anchors[:,LOW_INDICES])
            anchors[0]=evaluator.data['soft_start_source6']
            anchors[4]=evaluator.data['soft_end_source6']
            lower[0]=evaluator.full[('start',6)]
            lower[4]=evaluator.full[('end',6)]
            forecast_values,forecast_low=evaluator.combine(basic,anchors,lower)
            forecast=evaluator.reference_coordinates(SourcePacket(forecast_values,forecast_low))
            current=evaluator.groups[route][1]
            close(checks,'Current history minus defect equals frozen predictor:'+route+':'+str(phase),
                mapped.high-profile*current.high,forecast.high,1e-10)
            if route=='cubic':
                argument=Fraction.from_float(float(phase))
                exact=argument*(argument-Fraction(1,4))*(argument-Fraction(1,2))*(argument-1)/product
                close(checks,'Existing cubic cold-profile quartic identity:'+str(phase),
                    np.array([profile]),np.array([float(exact)]),1e-10)
    checks.append(dict(name='Exact fourth divided-difference coefficient E/(-3/128)',passed=True))
    finish(folder,dict(checks=checks,current_curve_unchanged=True,cold_profile_unchanged=True,
        divided_difference_multiplier='-128/3',quartic_surrogate_fourth_derivative_multiplier='-1024',
        derivative_coordinate='normalized terminal interpolation phase,not physical temperature',
        physical_temperature_law_derived=False,one_point_does_not_fix_error_history=True),evaluator.inputs)
    failures=[row for row in checks if not row['passed']]
    print(json.dumps(dict(checks=len(checks),failures=failures)),flush=True)
    assert not failures


if __name__=='__main__':
    main()

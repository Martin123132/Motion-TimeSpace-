import mpmath as mp
from emission_response import *
from increment_emitting_geometry import IncrementEmittingGeometry


def independent_thermal_derivative(frequency, data, heat, extension=0):
    mp.mp.dps = 70
    coordinate = mp.mpf(float(frequency))
    amplitude = mp.mpf(float(heat))
    profile = mp.mpf(data['value'])
    gas = mp.mpf(data['gas'])
    ratio = 1 + amplitude * gas
    planck = 1 / mp.expm1(coordinate)
    negative = mp.expm1(-coordinate * (ratio - 1) / ratio)
    positive = mp.expm1(coordinate * (ratio - 1) / ratio)
    ambient, ambient_derivative = mp.mpf(0), mp.mpf(0)
    source = data['ambient']
    for incident, companion, weight, first, second in zip(source['incident'], source['companion'], source['measure'], source['incident_profile'], source['companion_profile']):
        incident, companion, weight, first, second = map(lambda value: mp.mpf(float(value)), [incident, companion, weight, first, second])
        incident_planck, companion_planck = 1 / mp.expm1(incident), 1 / mp.expm1(companion)
        forward = 1 + amplitude * (1 + incident_planck) * first
        reverse = 1 + amplitude * companion_planck * second
        ambient += weight * forward * reverse
        ambient_derivative += weight * ((1 + incident_planck) * incident * reverse + forward * companion_planck * companion)
    deficit = amplitude * profile + (1 + amplitude * (1 + planck) * profile) * negative
    deficit_derivative = coordinate * (1 + (1 + planck) * negative) - (1 + amplitude * (1 + planck) * profile) * (1 + negative) * coordinate / ratio ** 2
    thermal_parameter = mp.mpf(float(data['theta']))
    gaunt = (1 + mp.mpf('14.16') * thermal_parameter) / (1 + mp.mpf('14.16') * thermal_parameter * ratio)
    gaunt_derivative = -gaunt * mp.mpf('14.16') * thermal_parameter / (1 + mp.mpf('14.16') * thermal_parameter * ratio)
    extra = 1 + extension * deficit
    dc = -mp.mpf(float(data['dc'])) * (gaunt * ambient * (1 + 2 * extension * deficit) * deficit_derivative
         + deficit * extra * (gaunt * ambient_derivative + gaunt_derivative * ambient)) / amplitude
    br_deficit = amplitude * profile - (1 + amplitude * planck * profile) * positive
    br_deficit_derivative = coordinate * (1 - planck * positive) - (1 + amplitude * planck * profile) * (1 + positive) * coordinate / ratio ** 2
    br_log = mp.mpf(float(data['br_thermal_log']))
    br_factor = mp.exp(br_log * (ratio - 1))
    br = -mp.mpf(float(data['br'])) * br_factor * (br_deficit_derivative + br_log * br_deficit) / amplitude
    return float(dc), float(br)


def main():
    modest()
    folder = ROOT / 'results/emission-response'
    folder.mkdir(parents=True, exist_ok=False)
    checks, rows, inputs = [], [], [ROOT / 'emission_response.py', PARENT / 'gaunt_gradient.py', PARENT / 'integrated_dc.py']
    for model in ['heavy', 'cold']:
        geometry = IncrementEmittingGeometry(model, model + '-ir96-integrated-6400')
        response = EmissionResponse(geometry)
        inputs.extend(response.inputs)
        for expansion in [.1, math.log(10)]:
            for frequency in [.00117, .137, 1.37, 8.37]:
                data = response.at(expansion, frequency)
                ambient = data['ambient']
                identity = abs(ambient['thermal'] - (5 + 2 * frequency - ambient['log_slope'])) / max(abs(ambient['thermal']), 1e-30)
                checks.append(check(model + ' Gould thermal scaling identity s=' + str(expansion) + ' x=' + str(frequency), identity, 1e-6))
                independent = independent_thermal_derivative(frequency, data, geometry.heat)
                alternative = independent_thermal_derivative(frequency, data, geometry.heat, extension=3)
                for label, actual, predicted in [('DC', independent[0], data['dc_thermal']), ('BR', independent[1], data['br_thermal'])]:
                    error = abs(actual - predicted) / max(abs(predicted), 1e-30)
                    checks.append(check(model + ' mixed common-thermal ' + label + ' s=' + str(expansion) + ' x=' + str(frequency), error, 2e-7))
                extension_error = abs(alternative[0] - independent[0]) / max(abs(independent[0]), 1e-30)
                checks.append(check(model + ' equilibrium-preserving DC extension drops out at leading thermal order s=' + str(expansion) + ' x=' + str(frequency), extension_error, 2e-7))
                step = 1e-5
                def boosted(velocity):
                    doppler = 1 - velocity
                    coordinate = frequency * doppler
                    planck = 1 / np.expm1(coordinate)
                    local_source = response.at(expansion, coordinate)['source']
                    reference_planck = 1 / np.expm1(frequency)
                    return doppler * planck * (1 + planck) * local_source / (reference_planck * (1 + reference_planck))
                difference = (boosted(step) - boosted(-step)) / (2 * step)
                error = abs(difference - data['boost']) / max(abs(data['boost']), abs(data['source']), 1e-30)
                checks.append(check(model + ' Lorentz source boost derivative s=' + str(expansion) + ' x=' + str(frequency), error, 2e-6))
                rows.append(dict(model=model, expansion=expansion, frequency=frequency, dc_common_thermal=data['dc_thermal'],
                                 dc_frozen_correction=data['dc_thermal_frozen'], br_common_thermal=data['br_thermal'],
                                 density_source=data['density_source'], background_source=data['source'], boost=data['boost']))
    finish(folder, dict(checks=checks, count=len(checks), all_checks_passed=all(row['passed'] for row in checks), rows=rows,
        mp_decimal_places=70, physical_heat_used=True,
        common_thermal_column_derived_without_off_equilibrium_G_extension=True,
        independent_BR_check='Arbitrary smooth coefficient with the sourced Gaunt first derivative; its higher derivatives enter only the next heat order.',
        angular_ambient_DC_response_derived=False,
        general_nonthermal_relativistic_DC_coefficient_derivative_derived=False), __file__, inputs)
    print(json.dumps(dict(checks=len(checks), failed=[row for row in checks if not row['passed']])), flush=True)


if __name__ == '__main__':
    main()

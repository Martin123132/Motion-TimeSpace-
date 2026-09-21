from fractions import Fraction

import numpy as np

from annular_gram_joint_action_20260909 import gram_matrices


def smooth_limit_checks():
    diagonal = [Fraction(59097,573104),Fraction(1825,25284),Fraction(491,7056),Fraction(5,72)]
    incident = [Fraction(253,50568)+Fraction(1,392),
                Fraction(253,50568)+Fraction(3,392),
                Fraction(3,392)+Fraction(1,144)+Fraction(1,392),
                Fraction(1,144)+Fraction(1,144)]
    margins = [value-weight for value,weight in zip(diagonal,incident)]
    row_bounds = [value+weight for value,weight in zip(diagonal,incident)]
    result = {'exact_diagonals':[str(value) for value in diagonal],
              'exact_incident_weights':[str(value) for value in incident],
              'exact_margins':[str(value) for value in margins],
              'exact_row_bounds':[str(value) for value in row_bounds],
              'uniform_matrix_bound':'1/8','positive_margins':all(value>0 for value in margins),
              'row_bound_proven':all(value<=Fraction(1,8) for value in row_bounds),
              'smooth_cases':[],'rough_cases':[],
              'conditional_action_difference_bound_proven':True,
              'uniform_H3_solution_bound_proven':False,'solution_convergence_proven':False,
              'full_GR_limit_proven':False}
    scalar_norm_sq = (2*np.pi)**6/2+.36
    variation_norm_sq = (2*np.pi)**6/2
    for count in [17,33,65,129]:
        radius = np.linspace(0.,1.,count)
        spacing = 1/(count-1)
        factors,sampling = gram_matrices(count)
        coefficient = 1+.2*np.cos(2*np.pi*radius)
        delta_coefficient = .3+radius
        scalar = np.sin(2*np.pi*radius)+.1*radius**3
        variation = np.cos(2*np.pi*radius)+.2*radius**2
        amplitude = factors @ scalar
        delta_amplitude = factors @ variation
        energy = float((sampling @ coefficient) @ amplitude**2/(2*spacing))
        field_variation = float((sampling @ coefficient) @ (amplitude*delta_amplitude)/spacing)
        metric_variation = float((sampling @ delta_coefficient) @ amplitude**2/(2*spacing))
        energy_bound = float(3*coefficient.max()*spacing**4*scalar_norm_sq/16)
        field_bound = float(3*coefficient.max()*spacing**4*np.sqrt(scalar_norm_sq*variation_norm_sq)/8)
        metric_bound = float(3*abs(delta_coefficient).max()*spacing**4*scalar_norm_sq/16)
        polynomial_error = float(max(abs(factors @ radius**degree).max() for degree in range(3)))
        result['smooth_cases'].append({'count':count,'spacing':spacing,'energy':energy,'energy_bound':energy_bound,
                                       'field_variation':field_variation,'field_variation_bound':field_bound,
                                       'metric_variation':metric_variation,'metric_variation_bound':metric_bound,
                                       'annihilated_quadratic_error':polynomial_error})
        rough = (-1.)**np.arange(count)
        rough_energy = float(np.sum((factors @ rough)**2)/(2*spacing))
        base_energy = float(np.sum(np.diff(rough)**2)/(2*spacing))
        result['rough_cases'].append({'count':count,'extra_energy':rough_energy,'base_energy':base_energy,
                                      'extra_to_base_ratio':rough_energy/base_energy})
    result['smooth_energy_orders'] = [float(np.log(first['energy']/second['energy'])/np.log(2.))
                                      for first,second in zip(result['smooth_cases'][:-1],result['smooth_cases'][1:])]
    result['all_bounds_satisfied'] = all(0<=row['energy']<=row['energy_bound']
                                        and abs(row['field_variation'])<=row['field_variation_bound']
                                        and abs(row['metric_variation'])<=row['metric_variation_bound']
                                        and row['annihilated_quadratic_error']<1e-12 for row in result['smooth_cases'])
    result['rough_nondecoupling_demonstrated'] = result['rough_cases'][-1]['extra_to_base_ratio']>.1
    return result


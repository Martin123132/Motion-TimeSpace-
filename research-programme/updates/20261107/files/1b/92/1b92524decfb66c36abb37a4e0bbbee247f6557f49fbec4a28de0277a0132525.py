from __future__ import annotations

from pathlib import Path
import math
import numpy as np
from scipy import integrate, optimize

from cosmology_common import ROOT, inherited, modest_process, read_json, save, candidate_profile, charged_shape


def full_profile(parameters, alpha, redshift, tolerance=2e-9):
    approximate=candidate_profile('Condensate_Lambda_free',parameters,redshift)
    omega_c=approximate['Omega_C']
    omega_d=approximate['Omega_pressureless']
    omega_lambda=approximate['Omega_Lambda']
    state0=10**parameters['log10_y0']
    field0=state0**(3/8)
    potential=lambda field:3*field**(4/3)/8+field**4/8
    force=lambda field:.5*field**(1/3)+.5*field**3
    charge=field0**2*math.sqrt(force(field0)/field0)
    initial_n=-math.log1p(redshift[-1])
    initial_y=approximate['y'][-1]
    initial_field=initial_y**(3/8)
    initial_slope=-9*(1+initial_y)/(5+9*initial_y)*initial_field
    rho0=math.sqrt(state0)*(5+3*state0)/8
    ratio0=math.sqrt(3*omega_c/(2*alpha*rho0))
    total_evaluations=0

    def integrate_at(ratio):
        def expansion(n_value, field, slope):
            phase=charge**2*np.exp(-6*n_value)/(2*field**2)
            numerator=omega_d*np.exp(-3*n_value)+inherited.OMEGA_R*np.exp(-4*n_value)+omega_lambda+2*alpha*ratio**2*(phase+potential(field))/3
            denominator=1-alpha*slope**2/3
            if np.any(field<=0) or np.any(denominator<=0):
                raise ValueError('full background left the regular positive field branch')
            return np.sqrt(numerator/denominator)

        def rhs(n_value, state):
            field,slope=state
            hubble=expansion(n_value,field,slope)
            phase2=charge**2*np.exp(-6*n_value)/field**2
            log_hubble=-.5*(3*omega_d*np.exp(-3*n_value)+4*inherited.OMEGA_R*np.exp(-4*n_value))/hubble**2-alpha*(slope**2+ratio**2*phase2/hubble**2)
            acceleration=-(3+log_hubble)*slope-ratio**2/hubble**2*(force(field)-charge**2*np.exp(-6*n_value)/field**3)
            return [slope,acceleration]

        solution=integrate.solve_ivp(rhs,(initial_n,0.),[initial_field,initial_slope],method='DOP853',rtol=tolerance,atol=tolerance/100,dense_output=True)
        if not solution.success:
            raise ValueError(solution.message)
        return solution,expansion

    def normalization(ratio):
        nonlocal total_evaluations
        solution,expansion=integrate_at(ratio)
        total_evaluations+=solution.nfev
        return float(expansion(0.,*solution.y[:,-1])-1)

    solved=optimize.root_scalar(normalization,x0=ratio0,x1=ratio0*1.001,method='secant',rtol=tolerance,xtol=tolerance*ratio0,maxiter=12)
    if not solved.converged:
        raise ValueError('physical density normalization failed')
    solution,expansion=integrate_at(solved.root)
    total_evaluations+=solution.nfev
    n_values=-np.log1p(redshift)
    field,slope=solution.sol(n_values)
    hubble=expansion(n_values,field,slope)
    return dict(E=hubble,field=field,slope=slope,mu_over_H0=float(solved.root),
        adiabatic_mu_over_H0=ratio0,initial_redshift=float(redshift[-1]),rhs_evaluations=total_evaluations,
        present_normalization_error=float(abs(hubble[0]-1)))


def main():
    modest_process()
    comparison=read_json(ROOT/'results/comparison/status.json')
    data=inherited.load_likelihood_data()
    chosen=next(row for row in comparison['fraction_profiles'] if row['parameters']['f_condensate']==.1)
    parameters=chosen['parameters']
    approximate=candidate_profile('Condensate_Lambda_free',parameters,data.z_grid)
    approximate_score=inherited.profile_likelihood(approximate['E'],data)['chi2_total']
    rows=[]
    for alpha in [.00019661998915671979,1e-5,1e-6]:
        exact=full_profile(parameters,alpha,data.z_grid)
        score=inherited.profile_likelihood(exact['E'],data)['chi2_total']
        row=dict(alpha=alpha,mu_over_H0=exact['mu_over_H0'],max_fractional_expansion_difference=float(np.max(abs(exact['E']/approximate['E']-1))),
            full_action_chi2=score,adiabatic_chi2=approximate_score,delta_chi2_from_adiabatic=score-approximate_score,
            present_normalization_error=exact['present_normalization_error'],rhs_evaluations=exact['rhs_evaluations'])
        rows.append(row)
        print(row,flush=True)
    check=full_profile(parameters,1e-6,data.z_grid,tolerance=2e-10)
    refined_score=inherited.profile_likelihood(check['E'],data)['chi2_total']
    save('adiabatic-check',Path(__file__),dict(parameters=parameters,rows=rows,
        tighter_solver_delta_chi2=refined_score-rows[-1]['full_action_chi2'],
        exact_background_equations='E^2=[Omega_d a^-3+Omega_r a^-4+Omega_Lambda+(2alpha/3)mu^2(j^2/(2a^6 h^2)+W)]/[1-alpha h_N^2/3]; h_NN=-(3+E_N/E)h_N-(mu/E)^2[W_h-j^2/(a^6 h^3)].',
        initialization='At maximum observed redshift, h and dh/dln(a) start on the charge-tracking branch. mu_star/H0 is normalized so E(0)=1, not fitted to distance residuals.',
        conditional_scale_statement='alpha=4piG v_star^2 is not fixed by the SN/BAO adiabatic fit. First row reuses the prior body example; smaller fixed values test controlled convergence, not fitted rescue coefficients.',
        scope='One nonzero-fraction diagnostic and one initial history, not an exhaustive fit of the full two-field action or a formation calculation.',
        full_action_parameters_not_counted_as_fitted_in_primary_adiabatic_table=True),
        [ROOT/'results/comparison/status.json',ROOT/'run_observational_comparison.py'])


if __name__=='__main__':
    main()

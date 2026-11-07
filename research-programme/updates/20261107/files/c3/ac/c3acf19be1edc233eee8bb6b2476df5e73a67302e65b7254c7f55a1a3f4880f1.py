from __future__ import annotations

from pathlib import Path
import csv
import numpy as np
from scipy import linalg
import sympy as sp

from cosmology_common import ROOT, inherited, modest_process, digest, save, archived_parameters, charged_shape, candidate_profile, independent_likelihood


def main():
    modest_process()
    state = sp.symbols('y',positive=True)
    density = sp.sqrt(state)*(5+3*state)
    pressure = sp.sqrt(state)*(state-1)
    slope = 24*state*(1+state)/(5+9*state)
    checks = []

    def check(name, condition, value=None):
        checks.append(dict(name=name,passed=bool(condition),value=value))
        assert condition,(name,value)

    check('charge-derived continuity',sp.simplify(sp.diff(density,state)*slope-3*(density+pressure))==0)
    check('adiabatic sound speed',sp.simplify(sp.diff(pressure,state)/sp.diff(density,state)-(3*state-1)/(5+9*state))==0)
    check('strict circular-state strong-energy sign',sp.simplify(density+3*pressure-2*sp.sqrt(state)*(1+3*state))==0)
    provenance=[]
    for label,path,expected,role in inherited.LOCKED_SOURCES:
        actual=digest(path)
        check(label+' source hash',actual==expected)
        provenance.append(dict(id=label,path=str(path),sha256=actual,role=role))
    data=inherited.load_likelihood_data()
    check('same 1624 SN light-curve rows',len(data.sn['z'])==1624)
    check('same 13 BAO vector elements',len(data.bao['rows'])==13)
    check('SN covariance dimensions',data.sn['covariance'].shape==(1624,1624))
    check('BAO covariance dimensions',data.bao['covariance'].shape==(13,13))
    for name,covariance in [('SN',data.sn['covariance']),('BAO',data.bao['covariance'])]:
        check(name+' finite symmetric covariance',np.all(np.isfinite(covariance)) and np.allclose(covariance,covariance.T,rtol=0,atol=1e-12))
        factor=linalg.cholesky(covariance,lower=True)
        check(name+' covariance positive definite',np.all(np.diag(factor)>0))
    parameters=archived_parameters()
    with (ROOT.parent.parent/'source-intake/functional_rg/5193/fit_summary.csv').open(newline='',encoding='utf-8') as handle:
        archive={row['model']:row for row in csv.DictReader(handle)}
    replay=[]
    for model in ['LCDM','wCDM','CPL','ParentScalar_Lambda_free','ParentScalar_Lambda_zero']:
        result=inherited.evaluate_model(model,parameters[model],data)
        original=float(archive[model]['chi2_total'])
        difference=result['chi2_total']-original
        check(model+' archived score reproduced',abs(difference)<2e-6,difference)
        independent=independent_likelihood(result['E'],data)
        check(model+' inverse versus Cholesky likelihood',abs(independent['chi2_total']-result['chi2_total'])<1e-7)
        replay.append(dict(model=model,chi2=result['chi2_total'],archive_chi2=original,difference=difference,independent=independent))
    for zero in [0.,.5,3.]:
        shape=charged_shape(data.z_grid,zero)
        check('charge law '+str(zero),np.max(abs(shape['charge_residual']))<1e-11)
        candidate=candidate_profile('Condensate_Lambda_free',dict(Omega_m=.3,f_condensate=0.,log10_y0=zero),data.z_grid)
        reference=inherited.baseline_e_grid('LCDM',dict(Omega_m=.3),data.z_grid)
        check('zero fraction exactly recovers LCDM '+str(zero),np.max(abs(candidate['E']-reference))<1e-14)
    save('preflight',Path(__file__),dict(checks=checks,provenance=provenance,baseline_replays=replay,
        n_SN=1624,n_BAO=13,n_scored=1637,z_max=float(data.z_grid[-1]),grid_points=len(data.z_grid),
        dataset_statement='Light-curve rows, not 1624 independent supernovae. Full covariance retained. No SH0ES calibration; two shared profiled nuisance parameters.',
        hypothesis='Closed, slowly tracking charged phase with original fractional-plus-quartic potential; preferred homogeneous branch y0>=1. No microscopic bath replacement is asserted.',
        density_budget='Omega_C=f_condensate*Omega_m; Omega_pressureless=(1-f_condensate)*Omega_m; Omega_Lambda=1-Omega_m-Omega_r. Old parent scalar is an alternative comparator, not added again.',
        no_Lambda_budget='Omega_m=1-Omega_r; positive pressureless and charged densities only.',
        source_web_urls=['https://github.com/PantheonPlusSH0ES/DataRelease','https://github.com/CobayaSampler/bao_data/blob/master/desi_bao_dr2/desi_gaussian_bao_ALL_GCcomb_cov.txt','https://www.desi.lbl.gov/2025/10/06/desi-dr2-cosmology-chains-and-data-products-released/'],
        data_redownloaded=False,likelihood_run_authorized_after_preflight=True,
        no_acceleration_result='rho_C+3p_C=positive for every circular y>0; with nonnegative dust/radiation and Lambda=0 this branch cannot accelerate. Not a theorem for all time-dependent states of the full action.'))
    print(dict(checks=len(checks),rows=1637,baseline_replays=replay),flush=True)


if __name__=='__main__':
    main()

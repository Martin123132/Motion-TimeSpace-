from __future__ import annotations

from window_common import *
from build_response import convolved_basis


def recover(basis,data,covariance):
    chol=linalg.cholesky(covariance,lower=True)
    def residual(parameters):
        bias,growth,noise=parameters
        return linalg.solve_triangular(chol,physical_vector(basis,bias,noise,growth)-data,lower=True)
    solutions=[optimize.least_squares(residual,start,bounds=([.1,.05,-10000],[4.,1.5,10000]),
        x_scale=[1,1,1000],ftol=1e-12,xtol=1e-12,gtol=1e-12,max_nfev=500)
        for start in [[1.4,.48,500],[1.,.4,0],[2.,.7,-1000]]]
    result=min(solutions,key=lambda item:np.sum(item.fun**2))
    assert result.success
    fisher=result.jac.T@result.jac
    factor=(NMOCK-len(data)-2)/(NMOCK-1)
    parameter_covariance=linalg.inv(fisher)/factor
    return dict(B=float(result.x[0]),F=float(result.x[1]),noise=float(result.x[2]),
        chi2_raw=float(result.fun@result.fun),F_error_linearized=float(np.sqrt(parameter_covariance[1,1])),
        boundary_hit=bool(np.min(result.x-np.array([.1,.05,-10000]))<1e-5 or
            np.min(np.array([4.,1.5,10000])-result.x)<1e-5),converged=bool(result.success))


def main():
    modest()
    folder=ROOT/'results/compression-test'
    folder.mkdir(parents=True,exist_ok=False)
    stats=json.loads((PARENT/'results/spectrum/status.json').read_text())
    rows=[]
    for label in ['heavy','cold','lcdm']:
        geom=geometry(label)
        template=multipole_basis('lcdm',geom=geom,template=True)
        reference=next(row for branch in stats['branches'] if branch['label']==label
            for row in branch['central'] if row['z']==REDSHIFT)
        for cap in ['NGC','SGC']:
            survey=np.load(ROOT/'results/prepared'/(cap+'.npz'))
            basis=convolved_basis(template,survey['operator'])
            real=np.load(ROOT/'results/response'/(label+'-'+cap+'.npz'))['basis']
            for kmax in [.08,.1,.12]:
                indices=select(kmax)
                covariance=survey['covariance'][np.ix_(indices,indices)]
                own=physical_vector(basis[:,indices],1.4,500,.48)
                self_fit=recover(basis[:,indices],own,covariance)
                truth=physical_vector(real[:,indices],2.)
                recovered=recover(basis[:,indices],truth,covariance)
                target=reference['velocity_sigma8_cb']
                rows.append(dict(branch=label,cap=cap,kmax=kmax,identity_injection=self_fit,
                    field_injection=recovered,F_reference_velocity_rms=target,
                    B_reference=2*reference['sigma8_cb'],F_bias=recovered['F']-target,
                    F_fractional_bias=recovered['F']/target-1,
                    F_bias_over_linearized_error=(recovered['F']-target)/recovered['F_error_linearized'],
                    geometry_policy='Same target AP geometry for truth and template to isolate shape compression.',
                    data_kind='Deterministic noiseless theory injection; actual survey window/covariance, not an observed growth fit.'))
    finish(folder,dict(rows=rows,template='LCDM cb density normalized by its sigma8, with a single free B and F.',
        inference='Diagnostic of this defined compression estimator, not reproduction of SDSS nonlinear fitting software.',
        observational_growth_fitted=False,formal_model_selection=False),__file__,
        [ROOT/'build_response.py',ROOT/'results/response/status.json',ROOT/'results/prepared/status.json',
            PARENT/'results/spectrum/status.json',PARENT/'results/spectrum/lcdm.npz',
            *sorted((ROOT/'results/response').glob('*.npz')),*sorted((ROOT/'results/prepared').glob('*.npz'))])
    print(json.dumps([row for row in rows if row['kmax']==.1],indent=2))


if __name__=='__main__':
    main()

from __future__ import annotations

import csv
from datetime import datetime, timezone
import hashlib
import importlib
import json
from pathlib import Path
import sys

import numpy as np
import psutil
from scipy import integrate, optimize

ROOT = Path(__file__).resolve().parent
BRANCH = ROOT.parent
POST = BRANCH.parent
PARENT = BRANCH/'polar-interior-schur-20261006'
sys.path.insert(0,str(POST/'scripts'))
inherited = importlib.import_module('Y5_R2FR_5193_direct_parent_scalar_SN_BAO_likelihood')
ARCHIVE = POST/'source-intake/functional_rg/5193'


def modest_process():
    process = psutil.Process()
    process.nice(psutil.BELOW_NORMAL_PRIORITY_CLASS)
    process.cpu_affinity([2])


def digest(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def read_json(path):
    return json.loads(Path(path).read_text(encoding='utf-8'))


def write_json(path, value):
    with Path(path).open('x',encoding='utf-8') as handle:
        json.dump(value,handle,indent=2,allow_nan=False)


def inputs():
    paths = {Path(__file__),Path(inherited.__file__),Path(inherited.closure_runner.__file__),
        PARENT/'results/stage-integrity.json',ARCHIVE/'parameter_estimates.csv',ARCHIVE/'fit_summary.csv',
        BRANCH/'conserved-stress-20261003/06-conserved-stress-and-parent-source.md',
        BRANCH/'conserved-stress-20261003/07-fixed-charge-bulk-continuation.md'}
    paths.update([inherited.SN_DATA,inherited.SN_COV,inherited.BAO_DATA,inherited.BAO_COV])
    return {str(path):digest(path) for path in sorted(paths)}


def save(label, script, report, extra_paths=()):
    folder = ROOT/'results'/label
    folder.mkdir(parents=True,exist_ok=False)
    hashes = inputs()
    hashes.update({str(path):digest(path) for path in extra_paths})
    output = dict(state='complete',time_utc=datetime.now(timezone.utc).isoformat(),
        script_sha256=digest(script),input_hashes=hashes,**report)
    write_json(folder/'status.json',output)
    (folder/'COMPLETE').write_text(output['time_utc']+'\n',encoding='utf-8')
    return output


def archived_parameters():
    parameters = {}
    with (ARCHIVE/'parameter_estimates.csv').open(newline='',encoding='utf-8') as handle:
        for row in csv.DictReader(handle):
            if row['parameter_role'] != 'shared_nuisance':
                parameters.setdefault(row['model'],{})[row['parameter']] = float(row['best_fit'])
    return parameters


def charged_shape(redshift, log10_y0):
    log_zero = np.log(10.)*log10_y0
    target = 1.25*log_zero+np.logaddexp(0.,log_zero)+6*np.log1p(redshift)
    log_state = log_zero+8*np.log1p(redshift)/3
    for iteration in range(12):
        fraction = 1/(1+np.exp(-log_state))
        log_state -= (1.25*log_state+np.logaddexp(0.,log_state)-target)/(1.25+fraction)
    residual = 1.25*log_state+np.logaddexp(0.,log_state)-target
    if np.max(abs(residual))>1e-11:
        raise ValueError('charge conservation root did not converge')
    state = np.exp(log_state)
    zero = np.exp(log_zero)
    density = np.sqrt(state/zero)*(5+3*state)/(5+3*zero)
    pressure_ratio = (state-1)/(5+3*state)
    sound_speed2 = (3*state-1)/(5+9*state)
    return dict(density=density,y=state,w=pressure_ratio,cs2=sound_speed2,charge_residual=residual)


def candidate_profile(model, parameters, redshift):
    fraction = parameters['f_condensate']
    omega_total = parameters.get('Omega_m',1-inherited.OMEGA_R)
    omega_condensate = fraction*omega_total
    omega_pressureless = (1-fraction)*omega_total
    omega_lambda = 1-omega_total-inherited.OMEGA_R
    if min(omega_condensate,omega_pressureless,omega_lambda)<-1e-12:
        raise ValueError('negative density budget')
    shape = charged_shape(redshift,parameters['log10_y0'])
    expansion2 = omega_pressureless*(1+redshift)**3+omega_condensate*shape['density']+inherited.OMEGA_R*(1+redshift)**4+omega_lambda
    deceleration = (omega_pressureless*(1+redshift)**3+omega_condensate*shape['density']*(1+3*shape['w'])+2*inherited.OMEGA_R*(1+redshift)**4-2*omega_lambda)/(2*expansion2)
    return dict(E=np.sqrt(expansion2),q=deceleration,Omega_C=omega_condensate,
        Omega_pressureless=omega_pressureless,Omega_Lambda=omega_lambda,**shape)


def evaluate(model, parameters, data):
    if model.startswith('Condensate'):
        background = candidate_profile(model,parameters,data.z_grid)
        return dict(**inherited.profile_likelihood(background['E'],data),E=background['E'],candidate=background)
    return inherited.evaluate_model(model,parameters,data)


def independent_likelihood(expansion, data):
    integral = integrate.cumulative_trapezoid(1/expansion,data.z_grid,initial=0)
    distance = np.interp(data.sn['z'],data.z_grid,integral)
    raw = np.asarray(data.sn['mu'])-5*np.log10(np.maximum((1+data.sn['z'])*distance,1e-12))
    from scipy.linalg import cho_factor, cho_solve
    sn_factor = cho_factor(data.sn['covariance'],lower=True)
    ones = np.ones_like(raw)
    offset = (ones@cho_solve(sn_factor,raw))/(ones@cho_solve(sn_factor,ones))
    residual = raw-offset
    chi_sn = residual@cho_solve(sn_factor,residual)
    unit = []
    for row in data.bao['rows']:
        distance = np.interp(row['z'],data.z_grid,integral)
        hubble = np.interp(row['z'],data.z_grid,expansion)
        unit.append({'DM_over_rs':distance,'DH_over_rs':1/hubble,'DV_over_rs':(row['z']*distance**2/hubble)**(1/3)}[row['quantity']])
    unit = np.asarray(unit)
    factor = cho_factor(data.bao['covariance'],lower=True)
    scale = (unit@cho_solve(factor,data.bao_observed))/(unit@cho_solve(factor,unit))
    residual_bao = data.bao_observed-scale*unit
    chi_bao = residual_bao@cho_solve(factor,residual_bao)
    return dict(chi2_SN=float(chi_sn),chi2_BAO=float(chi_bao),chi2_total=float(chi_sn+chi_bao),sn_offset=float(offset),bao_alpha=float(scale))

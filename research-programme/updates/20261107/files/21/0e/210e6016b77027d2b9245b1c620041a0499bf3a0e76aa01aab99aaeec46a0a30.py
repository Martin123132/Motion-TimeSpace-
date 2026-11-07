from __future__ import annotations
import os
for variable in ('OPENBLAS_NUM_THREADS','OMP_NUM_THREADS','MKL_NUM_THREADS','NUMEXPR_NUM_THREADS'):
    os.environ[variable]='1'
import sys
sys.dont_write_bytecode=True
from pathlib import Path
from datetime import datetime,timezone
import argparse
ROOT=Path(__file__).resolve().parent
BRANCH=ROOT.parent
PARENT=BRANCH/'full-spectrum-source-replacement-20261026'
KINETIC=BRANCH/'two-sided-physical-source-matching-20261026'
THERMAL=BRANCH/'thermal-recoil-and-spectral-response-20261007'
sys.path[:0]=[str(PARENT),str(THERMAL)]
import reconcile224 as previous
import flrw_thermal_response as gravity
from scipy import integrate,linalg
parent=previous.parent
np,mp,math,json=previous.np,previous.mp,previous.math,previous.json
read,write,save,packet,digest,check=previous.read,previous.write,previous.save,previous.packet,previous.digest,previous.check
PARENT_SHA='b739a874b6468695a30b37df894f64c49455d49a117046b17f39733b063d4704'

def now():
    return datetime.now(timezone.utc).isoformat()

def register(inputs,path):
    path=Path(path).resolve()
    assert path.is_file(),str(path)
    value=digest(path)
    assert str(path) not in inputs or inputs[str(path)]==value,str(path)
    inputs[str(path)]=value
    return path

def load(inputs,path):
    return packet(register(inputs,path))

def prepare():
    assert not (ROOT/'configuration.json').exists()
    seal_path=PARENT/'results/stage-integrity.json'
    assert digest(seal_path)==PARENT_SHA
    seal=read(seal_path)
    assert seal['qualified'] and read(PARENT/'results/independent-validation.json')['qualified']
    inputs=dict(seal['consumed_and_immediate_rehashed'])
    inputs.update({str(PARENT/name):value for name,value in seal['file_hashes'].items()})
    inputs[str(seal_path)]=PARENT_SHA
    for path,value in inputs.items():
        assert digest(path)==value,path
    legacy=[THERMAL/'flrw_thermal_response.py',THERMAL/'verify_flrw_conservation.py',
        THERMAL/'thermal_common.py',THERMAL/'70-balanced-thermal-recoil-spectral-response-and-gravity.md',
        BRANCH/'expanding-thermal-gravity-20261007/DERIVATION.md',
        BRANCH/'emitting-thermal-background-20261008/infrared_ladder.py',
        BRANCH/'infrared-source-domain-20261008/nonlocal_dc.py',
        BRANCH/'kinetic-gain-loss-20261008/evolve_derived_gaunt.py',
        BRANCH/'emitting-thermal-background-20261008/integrated_dc.py',
        BRANCH/'coupled-finite-wave-evolution-20261007/evolution_common.py']
    for path in legacy:
        register(inputs,path)
    config=dict(stage=225,turn_start='2026-10-26T15:01:34+00:00',prepared_at=now(),previous_goal_turn='progress',
        parent_sha256=PARENT_SHA,models=['heavy','cold'],counts=[2048,4096],
        spans=dict(known_window=[.8707275390625,1.],source_free_tail=[.91015625,1.]),
        probes=['constant','ramp','bump'],probe_amplitudes=[1e-3,1e-4],quadrature_orders=[64,128],
        identity_tolerance=1e-10,stress_tolerance=1e-8,nonlinear_probe_tolerance=5e-5,
        kernel_tolerance=1e-6,source_refinement_tolerance=.01,
        legacy_sources={str(path):digest(path) for path in legacy},
        protocol_hashes={path.name:digest(path) for path in [*ROOT.glob('*.py'),ROOT/'ACCEPTANCE.md',ROOT/'DERIVATION.md']},
        bank_changed=False,global_curve_changed=False,grids_changed=False,tolerances_changed=False,
        incoming_field_response='explicit independent term, zero only for labelled response probes',
        kinetic_tail_scope='retained dissipative physical model initialized by saved state; no global continuum-error certificate')
    write(ROOT/'configuration.json',config)
    write(ROOT/'inputs.json',inputs)
    print(json.dumps(dict(state='prepared',inputs=len(inputs))),flush=True)

def protocol():
    config=read(ROOT/'configuration.json')
    for name,value in config['protocol_hashes'].items():
        assert digest(ROOT/name)==value,name
    return config

def compare(rows,name,actual,expected,tolerance=1e-10):
    actual=np.asarray(actual);expected=np.asarray(expected)
    check(rows,name,np.max(abs(actual-expected))/max(float(np.max(abs(expected))),1e-300),tolerance,'identity')

def model_parts(background,coordinate):
    scale=background.start_scale*math.exp(coordinate)
    state=gravity.state_at_scale(background,scale)
    mass=background.parent.masses
    energy=3*state['hubble']**2/scale**2
    field=np.r_[mass*state['fields'],state['prime']/scale]
    frequency=scale*mass/state['hubble']
    free=np.block([[np.zeros((2,2)),np.diag(frequency)],[-np.diag(frequency),-3*np.eye(2)]])
    drive=np.r_[-frequency*field[2:],frequency*field[:2]]
    density_row=field/(2*energy)
    direct=state['photon']/(2*energy)
    operator=free+np.outer(drive,density_row)
    return dict(state=state,scale=scale,mass=mass,energy=energy,field=field,frequency=frequency,
        free=free,drive=drive,row=density_row,direct=direct,operator=operator,forcing=drive*direct)

def analytic_bound(background,first,last):
    initial=model_parts(background,first)
    end_scale=background.start_scale*math.exp(last)
    radiation=background.parent.radiation
    field_energy=(initial['field'][:2]**2+initial['field'][2:]**2)/2
    density_min=radiation/end_scale**4
    frequencies=np.sqrt(3)*background.parent.masses*end_scale**2/math.sqrt(radiation)
    drive_bound=math.sqrt(float(np.sum(2*frequencies**2*field_energy)))
    row_bound=math.sqrt(float(2*np.sum(field_energy)))/(2*density_min)
    direct_bound=background.parent.photons/(2*radiation)
    exponent=drive_bound*row_bound*(last-first)
    return dict(density_min=density_min,field_energy_initial=field_energy.tolist(),
        frequency_upper=frequencies.tolist(),Bstar=drive_bound,Cstar=row_bound,Dstar=direct_bound,
        beta=drive_bound*row_bound,exponent=exponent,source_gain=direct_bound*math.exp(exponent),
        incoming_gain=row_bound*math.exp(exponent),
        formula='abs(delta H/H)<=source_gain*sup(abs(q))+incoming_gain*norm(z_initial)')

if __name__=='__main__':
    parent.old.source.modest()
    prepare()

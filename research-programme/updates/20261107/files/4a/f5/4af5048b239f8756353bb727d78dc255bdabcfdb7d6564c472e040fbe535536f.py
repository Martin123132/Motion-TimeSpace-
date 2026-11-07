from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).resolve().parent.parent/'moving-polarized-thermal-20261008'))
from polarized_thermal_common import *
import polarized_source as source
import thermal_wave_common as thermal_wave
from consistent_spectral_basis import ConsistentBasis
from scipy import special, interpolate, integrate, linalg

ROOT=Path(__file__).resolve().parent
PARENT=ROOT.parent/'moving-polarized-thermal-20261008'
BACKGROUND=ROOT.parent/'emitting-thermal-background-20261008'
STARTED=datetime(2026,10,8,3,26,11,tzinfo=timezone.utc)
I3=np.pi**4/15


def finish(folder,report,script,extra=()):
    paths=[Path(script),ROOT/'kinetic_common.py',ROOT/'ACCEPTANCE.md',PARENT/'results/stage-integrity.json',*extra]
    report.update(state='complete',finished_utc=datetime.now(timezone.utc).isoformat(),script_sha256=digest(script),
                  input_hashes={str(path):digest(path) for path in paths})
    write_json(folder/'status.json',report)
    (folder/'COMPLETE').write_text('complete\n',encoding='utf-8')


def gas_rule(temperature,radial,polar):
    nodes,weights=special.roots_genlaguerre(radial,.5)
    energy=1+temperature*nodes
    momentum=np.sqrt(temperature*nodes*(2+temperature*nodes))
    weights=weights*energy*np.sqrt(2+temperature*nodes)
    weights/=weights.sum()
    cosines,angular_weights=np.polynomial.legendre.leggauss(polar)
    for speed,radial_weight in zip(momentum/energy,weights):
        for cosine,angular_weight in zip(cosines,angular_weights/2):
            yield speed*np.array([math.sqrt(1-cosine**2),0,cosine]),float(radial_weight*angular_weight)


def snapshot():
    metadata=json.loads((ROOT/'results/saved-state/status.json').read_text())
    with np.load(ROOT/'results/saved-state/state.npz') as saved:
        values={name:saved[name].copy() for name in saved.files}
    spectrum=interpolate.CubicSpline(values['log_frequency'],values['potential_scaled'])
    return metadata,values,spectrum

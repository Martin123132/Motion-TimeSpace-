import os
for variable in ['OPENBLAS_NUM_THREADS', 'OMP_NUM_THREADS', 'MKL_NUM_THREADS', 'NUMEXPR_NUM_THREADS']:
    os.environ[variable] = '1'
import sys
sys.dont_write_bytecode = True
from pathlib import Path
from datetime import datetime, timezone
import json
import hashlib
import argparse
import time
ROOT = Path(__file__).resolve().parent
BRANCH = ROOT.parent
PARENT = BRANCH/'anchor-photon-gas-history-split-20261020'
PARENT_SHA = '306e386d26ca11a2118fc5967e204d8f54147c2e5113df1a02a56d6eec4394c0'
STARTED = '2026-10-20T21:17:40+00:00'
sys.path.insert(0, str(PARENT))
import split_stage180 as prior
source, saved, np, mp = prior.source, prior.saved, prior.np, prior.mp
import scipy.linalg as linear
sys.path.insert(0, str(BRANCH/'infrared-source-domain-20261008'))
import nonlocal_dc as native
MODELS = ['heavy', 'cold']


def read(path):
    return json.loads(Path(path).read_text(encoding='utf-8'))


def write(path, value):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    saved.write_json(path, value)


def authenticate():
    seal_path = PARENT/'results/stage-integrity.json'
    assert saved.digest(seal_path) == PARENT_SHA
    seal = read(seal_path)
    paths = dict(seal['consumed_and_immediate_rehashed'])
    paths.update({str(PARENT/name):checksum for name,checksum in seal['file_hashes'].items()})
    paths.update(seal['next_equation_source_hashes'])
    paths[str(seal_path)] = PARENT_SHA
    for model in MODELS:
        folder = BRANCH/'infrared-source-domain-20261008/backgrounds'/f'{model}-nonlocal-refined-6400'
        metadata = read(folder/'status.json')
        for filename, checksum in metadata['input_hashes'].items():
            if filename in paths:
                assert paths[filename] == checksum, filename
            paths[filename] = checksum
        for path in [folder/'history.npz', folder/'status.json']:
            assert str(path) in paths, f'History lacks previous authenticated owner: {path}'
    for filename,checksum in paths.items():
        assert saved.digest(filename) == checksum, filename
    return paths


def prepare():
    assert not (ROOT/'configuration.json').exists()
    paths = authenticate()
    parent = read(PARENT/'configuration.json')
    assert parent['source_prediction_tolerance'] == .01 and parent['identity_tolerance'] == 1e-10
    write(ROOT/'configuration.json', dict(stage=181, started_utc=STARTED,
        parent_seal_sha256=PARENT_SHA, source_prediction_tolerance=.01, identity_tolerance=1e-10,
        anchor_fraction=.875, offsets=parent['offsets'], expansion_span=parent['expansion_span'],
        history_tags=parent['history_tags'], native_models=MODELS, arithmetic_digits=[80,100],
        interpolation='unchanged linear history interpolation',
        prior_bookmark_normalized_sha256={str(path):hashlib.sha256(path.read_text(encoding='utf-8').encode()).hexdigest()
            for path in [BRANCH/'RESUME-CURRENT.md', BRANCH.parent/'CURRENT_LOCAL_RESUME.md']}))
    write(ROOT/'authenticated-inputs.json', paths)
    write(ROOT/'progress.json', dict(state='prepared'))
    print(json.dumps(dict(prepared=True, authenticated_paths=len(paths))), flush=True)


def mp_vector(values):
    return mp.matrix([mp.mpf(float(value)) for value in values])


def mp_matrix(values):
    return mp.matrix([[mp.mpf(float(value)) for value in row] for row in values])


def bdf2_first_derivative(values, step):
    return (3*values[2:] - 4*values[1:-1] + values[:-2])/(2*step)


def exact_bdf(values, index, step):
    return (3*mp.mpf(float(values[index]))-4*mp.mpf(float(values[index-1]))+mp.mpf(float(values[index-2])))/(2*mp.mpf(float(step)))


def energy_dot(row, profile):
    return mp.fdot([mp.mpf(float(value)) for value in row], [mp.mpf(float(value)) for value in profile])


def native_replay():
    config = read(ROOT/'configuration.json')
    paths = read(ROOT/'authenticated-inputs.json')
    ladder = native.infrared_ladder.InfraredLadder(native.BACKGROUND/'banks/infrared96-q700')
    basis = ladder.basis
    used = set(ladder.inputs)
    for model in MODELS:
        folder = BRANCH/'infrared-source-domain-20261008/backgrounds'/f'{model}-nonlocal-refined-6400'
        metadata = read(folder/'status.json')
        assert metadata['all_checks_passed'] and metadata['mode']=='nonlocal-leading' and metadata['bank']=='s960-i256'
        with np.load(folder/'history.npz') as packet:
            history = {name:packet[name].copy() for name in packet.files}
        background = native.thermal_wave.thermal.ThermalBackground(model)
        emission = native.NonlocalEmission(basis, background, metadata['mode'], native.ROOT/'banks'/metadata['bank'])
        used.update(emission.inputs)
        used.update([background.parent.source, background.native_constants])
        assert background.chi == float(history['heat'])
        assert np.array_equal(basis.energy, history['energy_row'])
        assert np.array_equal(basis.temperature, history['temperature_template'])
        expansion, profiles, gas = history['expansion'], history['profiles'], history['temperature_scaled']
        step = background.end/metadata['steps']
        coordinates = np.array([(config['anchor_fraction']-config['offsets'][tag]/config['expansion_span'])*config['expansion_span']
            for tag in config['history_tags']])
        bracket_indices = sorted({int(item) for point in coordinates for item in [np.searchsorted(expansion, point, side='right')-1, np.searchsorted(expansion, point, side='right')]
            if 2 <= item < len(expansion)})
        low, high = min(bracket_indices)-2, max(bracket_indices)+2
        indices = np.arange(low, high+1)
        destination = ROOT/'results'/model
        destination.mkdir(parents=True, exist_ok=True)
        np.savez_compressed(destination/'state.npz', indices=indices, bracket_indices=bracket_indices,
            coordinates=coordinates, step=step, mass=basis.mass, energy=basis.energy, template=basis.temperature,
            **history)
        checks = []
        replay_values, records = [], []
        for index in indices:
            local = background.at(float(expansion[index]))
            rate = local['coefficient']/local['thermal_parameter']
            scattering = ladder.at(local['thermal_parameter'], 0)[:basis.count,:basis.count]
            damping = emission.at(local['thermal_parameter'], 'dcbr')
            stiffness = scattering-damping
            alpha = 1.5/step
            vector = (2*profiles[index-1]-.5*profiles[index-2])/step
            scalar = (2*gas[index-1]-.5*gas[index-2])/step
            thermal_source = -rate*stiffness@basis.temperature
            left = alpha*basis.mass-rate*stiffness
            solution = linear.solve(left, np.column_stack([basis.mass@vector, thermal_source]), assume_a='pos')
            free, response = solution[:,0], solution[:,1]
            numerator = background.chi*scalar-1-basis.energy@(alpha*free-vector)
            denominator = background.chi*(alpha+1)+alpha*(basis.energy@response)
            replay = numerator/denominator
            update = free+response*replay
            rhs = rate*stiffness@(profiles[index]-basis.temperature*gas[index])
            photon_first = linear.solve(basis.mass, rhs, assume_a='pos')
            kinetic_residual = alpha*basis.mass@profiles[index]-basis.mass@vector-rhs
            record = dict(index=int(index), u=float(expansion[index]), theta=local['thermal_parameter'], rate=rate,
                gas=float(gas[index]), replay_gas=float(replay), replay_gas_absolute_error=float(abs(replay-gas[index])),
                replay_profile_relative=float(np.linalg.norm(update-profiles[index])/np.linalg.norm(profiles[index])),
                energy_rhs=float(basis.energy@photon_first), gas_rhs=float(-gas[index]-(1+basis.energy@photon_first)/background.chi),
                kinetic_residual_relative=float(np.linalg.norm(kinetic_residual)/np.linalg.norm(rhs)),
                numerator=float(numerator), denominator=float(denominator),
                denominator_over_bare_heat=float(denominator/(background.chi*(alpha+1))),
                matrix_upper_asymmetry=float(np.linalg.norm(left-left.T)/np.linalg.norm(left)))
            with mp.workdps(80):
                heat = mp.mpf(background.chi)
                energy_first = exact_bdf(history['energy_scaled'],index,step)
                gas_first = exact_bdf(gas,index,step)
                profile_energy_first = energy_dot(basis.energy,profiles[index])*3-energy_dot(basis.energy,profiles[index-1])*4+energy_dot(basis.energy,profiles[index-2])
                profile_energy_first /= 2*mp.mpf(step)
                residual = energy_first+heat*(gas_first+mp.mpf(float(gas[index])))+1
                profile_residual = profile_energy_first+heat*(gas_first+mp.mpf(float(gas[index])))+1
                balance = mp.mpf(float(history['energy_scaled'][index]))+heat*mp.mpf(float(gas[index]))+mp.mpf(float(history['expansion_work'][index]))
                work_residual = exact_bdf(history['expansion_work'],index,step)-1-heat*mp.mpf(float(gas[index]))
                record.update(gas_bdf_first=float(gas_first), energy_bdf_first=float(energy_first),
                    balance_residual=float(balance), work_bdf_residual=float(work_residual),
                    gas_energy_bdf_residual=float(residual), profile_energy_bdf_residual=float(profile_residual),
                    energy_bdf_gas_rhs_error=float(abs(residual)/heat), profile_bdf_gas_rhs_error=float(abs(profile_residual)/heat),
                    source_rhs_gas_error=float(abs(mp.mpf(record['gas_rhs'])-gas_first)))
            records.append(record)
            replay_values.append(replay)
            if index in bracket_indices:
                np.savez_compressed(destination/f'operator-{index}.npz',
                    left=left, thermal_source=thermal_source, right=basis.mass@vector, vector=vector,
                    stiffness=stiffness, rate=rate, scalar=scalar, alpha=alpha,
                    index=index, theta=local['thermal_parameter'])
        original_values = np.interp(coordinates,expansion,gas)
        replay_values = np.array(replay_values)
        sampled_replay = np.interp(coordinates,expansion[indices],replay_values)
        np.savez_compressed(destination/'replay.npz', replay_values=replay_values, indices=indices,
            original_samples=original_values, replay_samples=sampled_replay)
        write(destination/'native-diagnostic.json', records)
        print(json.dumps(dict(model=model,native_nodes=len(indices),precision_nodes=len(bracket_indices),
            max_replay_gas_error=max(row['replay_gas_absolute_error'] for row in records),
            max_gas_rhs_error=max(row['source_rhs_gas_error'] for row in records))),flush=True)
        write(ROOT/'progress.json', dict(state='native_replay', completed_model=model, pid=os.getpid()))
    for module in list(sys.modules.values()):
        filename = getattr(module,'__file__',None)
        if filename and Path(filename).suffix=='.py' and Path(filename).is_relative_to(BRANCH) and not Path(filename).is_relative_to(ROOT):
            used.add(Path(filename))
    extras = {}
    for path in sorted(used):
        checksum = saved.digest(path)
        if str(path) in paths:
            assert checksum==paths[str(path)], str(path)
        else:
            extras[str(path)] = checksum
    write(ROOT/'additional-inputs.json',extras)
    write(ROOT/'consumed-bank-inputs.json',{str(path):saved.digest(path) for path in sorted(used)})
    write(ROOT/'progress.json',dict(state='native_complete'))


def precise_replay():
    for model in MODELS:
        folder = ROOT/'results'/model
        with np.load(folder/'state.npz') as packet:
            state = {name:packet[name].copy() for name in packet.files}
        indices = state['bracket_indices']
        for digits in [80,100]:
            result_path = folder/f'precision-{digits}.json'
            if result_path.exists():
                continue
            records = []
            with mp.workdps(digits):
                mass = mp_matrix(state['mass'])
                energy = mp_vector(state['energy'])
                template = mp_vector(state['template'])
                dual_energy = mp.lu_solve(mass.T,energy)
                heat,step = mp.mpf(float(state['heat'])),mp.mpf(float(state['step']))
                for index in indices:
                    with np.load(folder/f'operator-{index}.npz') as packet:
                        operator = {name:packet[name].copy() for name in packet.files}
                    upper = np.triu(operator['left'])+np.triu(operator['left'],1).T
                    left = mp_matrix(upper)
                    decomposition, permutation = mp.mp.LU_decomp(left)
                    def solve(right):
                        return mp.mp.U_solve(decomposition,mp.mp.L_solve(decomposition,right,permutation))
                    free = solve(mp_vector(operator['right']))
                    response = solve(mp_vector(operator['thermal_source']))
                    alpha,scalar = mp.mpf(float(operator['alpha'])),mp.mpf(float(operator['scalar']))
                    vector = mp_vector(operator['vector'])
                    numerator = heat*scalar-1-(energy.T*(alpha*free-vector))[0]
                    denominator = heat*(alpha+1)+alpha*(energy.T*response)[0]
                    gas = numerator/denominator
                    profile = free+response*gas
                    closure = (energy.T*(alpha*profile-vector))[0]+heat*((alpha+1)*gas-scalar)+1
                    stored_profile = mp_vector(state['profiles'][index])
                    stored_gas = mp.mpf(float(state['temperature_scaled'][index]))
                    stiffness = mp_matrix(operator['stiffness'])
                    rate = mp.mpf(float(operator['rate']))
                    rhs = rate*stiffness*(stored_profile-template*stored_gas)
                    energy_rhs = (dual_energy.T*rhs)[0]
                    gas_rhs = -stored_gas-(1+energy_rhs)/heat
                    gas_bdf = exact_bdf(state['temperature_scaled'],index,float(step))
                    records.append(dict(index=int(index),gas=str(gas),closure=str(closure),denominator=str(denominator),
                        numerator=str(numerator),stored_gas=str(stored_gas),gas_rhs=str(gas_rhs),
                        gas_bdf=str(gas_bdf),source_energy=str(energy_rhs),gas_rhs_error=str(gas_rhs-gas_bdf),
                        replay_error=str(gas-stored_gas),matrix_convention='original binary64 upper-triangle solve',
                        source_convention='full saved matrix and high-precision mass dual',digits=digits))
                    print(json.dumps(dict(model=model,digits=digits,index=int(index),
                        replay_error=float(gas-stored_gas),gas_rhs_error=float(gas_rhs-gas_bdf))),flush=True)
                    write(ROOT/'progress.json',dict(state='precise_replay',model=model,digits=digits,index=int(index),pid=os.getpid()))
                write(result_path,records)
    write(ROOT/'progress.json',dict(state='precision_complete'))


if __name__=='__main__':
    source.modest()
    parser = argparse.ArgumentParser()
    parser.add_argument('phase',choices=['prepare','native','precision'])
    arguments = parser.parse_args()
    {'prepare':prepare,'native':native_replay,'precision':precise_replay}[arguments.phase]()

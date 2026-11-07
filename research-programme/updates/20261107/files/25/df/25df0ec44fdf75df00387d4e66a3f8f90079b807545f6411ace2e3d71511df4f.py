from kinetic_common import *


def main():
    modest()
    folder=ROOT/'results/saved-state'
    folder.mkdir(parents=True,exist_ok=False)
    seal=json.loads((PARENT/'results/stage-integrity.json').read_text())
    for relative,expected in seal['file_hashes'].items():
        assert digest(PARENT/relative)==expected,relative
    history=BACKGROUND/'backgrounds/heavy-ir96-integrated-6400/history.npz'
    history_status=history.parent/'status.json'
    report=json.loads(history_status.read_text())
    assert report['all_checks_passed']
    basis=ConsistentBasis(**report['basis_spec'])
    with np.load(history) as saved:
        index=len(saved['expansion'])//2
        expansion=float(saved['expansion'][index])
        profile=saved['profiles'][index].copy()
        gas_temperature_scaled=float(saved['temperature_scaled'][index])
        heat=float(saved['heat'])
    background=thermal_wave.thermal.ThermalBackground('heavy')
    local=background.at(expansion)
    theta=float(local['thermal_parameter'])
    grid=np.linspace(math.log(basis.minimum),math.log(basis.maximum),4097)
    potential=basis.evaluate(np.exp(grid))@profile
    interpolator=interpolate.CubicSpline(grid,potential)
    independent=np.linspace(grid[0],grid[-1],2050)+0.
    exact_values=basis.evaluate(np.exp(independent))@profile
    interpolation_error=float(np.max(abs(interpolator(independent)-exact_values))/max(np.max(abs(exact_values)),1e-30))
    checks=[dict(name='All61 prior-stage sealed files unchanged',passed=len(seal['file_hashes'])==61),
            check('Saved spectral interpolation independently evaluated',interpolation_error,1e-6),
            dict(name='Saved radiation and gas are small departures from positive thermal state',
                 passed=bool(1+heat*gas_temperature_scaled>0 and np.min(1+heat*(1+1/np.expm1(np.exp(grid)))*potential)>0)),
            check('Parent heat parameter reproduced',abs(heat/background.chi-1),1e-12)]
    np.savez_compressed(folder/'state.npz',log_frequency=grid,potential_scaled=potential,profile=profile,
                        gas_temperature_scaled=gas_temperature_scaled,heat=heat,expansion=expansion)
    result=dict(checks=checks,count=len(checks),all_checks_passed=all(row['passed'] for row in checks),
                history_index=index,scale_factor=local['scale'],reference_temperature=theta,
                electron_temperature=theta*(1+heat*gas_temperature_scaled),gas_temperature_scaled=gas_temperature_scaled,
                heat=heat,basis_spec=report['basis_spec'],input_history=str(history),
                electron_population='Inherited dilute Maxwell-Juttner gas at the saved gas temperature.',
                reference_loop_bath='Planck reference; saved nonthermal spectrum is used in the linearized real gain-loss source.')
    finish(folder,result,__file__,[history,history_status,folder/'state.npz',
           BACKGROUND/'infrared_ladder.py',BACKGROUND/'evolve_sourced_background.py',
           ROOT.parent/'observer-frequency-projection-20261007/consistent_spectral_basis.py',
           ROOT.parent/'polarized-finite-shift-kernel-20261007/kernel_common.py',background.parent.source,background.native_constants])
    print(json.dumps(dict(checks=len(checks),failed=[row for row in checks if not row['passed']],
                          theta=theta,electron_temperature=result['electron_temperature'],gas_scaled=gas_temperature_scaled,
                          interpolation_error=interpolation_error)),flush=True)


if __name__=='__main__':
    main()

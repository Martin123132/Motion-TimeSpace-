from __future__ import annotations

from matching_common import *


def matter(folder):
    data = np.load(folder/'evolution.npz')
    status = json.loads((folder/'status.json').read_text())
    names = data['names'].tolist()
    values = data['values']
    scales = values[0,:,names.index('a')]
    standard = sum(data['background_'+key] for key in ['cdm','baryon','nu'])
    perturbation = sum(data['background_'+key][None,:]*values[:,:,names.index(column)]
        for key,column in [('cdm','delta_cdm'),('baryon','delta_baryon'),('nu','delta_nu')])
    if not status['arguments']['cold']:
        table = np.load(ROOT/'runs/matching-inputs'/(status['arguments']['input']+'.npz'))
        heavy = float(table['matching_density'])*scales
        perturbation += scales[None,:]**2*values[:,:,names.index('mts_drho_h')]
        standard = standard+heavy
    return data, perturbation/standard[None,:]


def main():
    modest()
    folder = ROOT/'results/late-comparison'
    folder.mkdir(parents=True, exist_ok=False)
    labels = ['late-200','late-225','late-250','late-225-bg4','late-225-window4',
        'late-225-degree6','late-cold','late-lcdm','late-225-raw']
    packets = {label:matter(ROOT/'runs'/label) for label in labels}
    reference = packets['late-225'][1]
    comparisons = []
    rows = []
    for label, (data, physical) in packets.items():
        late = data['requested_scale'] >= .001
        comparisons.append(dict(label=label, today_delta=physical[:,-1].tolist(),
            today_fractional_change_from_central=(physical[:,-1]/reference[:,-1]-1).tolist(),
            finite=bool(np.isfinite(physical[:,late]).all())))
    for index, mode in enumerate(MODES):
        amplitude = reference[index,-1]
        ratio = amplitude/packets['late-cold'][1][index,-1]
        lcdm_ratio = amplitude/packets['late-lcdm'][1][index,-1]
        primordial = previous.AS*(mode/.05)**(previous.NS-1)
        rows.append(dict(k_Mpc_inverse=float(mode), today_delta=float(amplitude),
            amplitude_ratio_heavy_to_slow_cold=float(ratio), power_ratio_heavy_to_slow_cold=float(ratio**2),
            amplitude_ratio_heavy_to_LCDM=float(lcdm_ratio), power_ratio_heavy_to_LCDM=float(lcdm_ratio**2),
            linear_power_Mpc_cubed=float(2*math.pi**2/mode**3*primordial*amplitude**2)))
    finish(folder, dict(rows=rows, comparisons=comparisons, primordial_amplitude=previous.AS,
        primordial_slope=previous.NS, F=.5, physical_matter_includes_heavy=True,
        spectrum_integral=False, nonlinear_prediction=False, data_fit=False,
        scope='Four conditional linear transfer samples; k=1 and5 at z=0 are not nonlinear structure predictions.'),
        __file__, [ROOT/'runs'/label/name for label in labels for name in ['status.json','evolution.npz']] +
        [ROOT/'matching_common.py'])
    print(json.dumps(dict(rows=rows, comparisons=comparisons),indent=2))


if __name__ == '__main__':
    main()

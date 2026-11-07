from __future__ import annotations

from native_common import *


def main():
    modest()
    os.environ['MPLCONFIGDIR'] = str(ROOT / 'runs/matplotlib-cache')
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt

    folder = ROOT / 'results/figures'
    folder.mkdir(parents=True, exist_ok=False)
    source = ROOT / 'results/resolved-projection-analysis/status.json'
    report = json.loads(source.read_text())
    rows = [row for row in report['matches']['final-bg8-start'] if row['center_a']==.00025]
    figure, axis = plt.subplots(figsize=(8, 4.7), layout='constrained')
    wave = [row['k_Mpc_inverse'] for row in rows]
    ratios = [row['cold_amplitude_ratio'] for row in rows]
    axis.axhline(1., color='#687880', linestyle='--', label='Matched cold control')
    axis.scatter(wave, ratios, color='#006b74', s=65, zorder=3, label='F=0.5 heavy branch: four calculated modes')
    axis.set_xscale('log')
    axis.set(xlabel='Wavenumber k [Mpc⁻¹]', ylabel='Remaining cold-matter amplitude / cold control', ylim=(.70, 1.045))
    axis.set_title('Early growth response with photons, baryons and neutrinos\na = 0.00025 (z = 3999); shared primordial curvature', loc='left', fontsize=12)
    axis.grid(alpha=.2)
    axis.legend(frameon=False, loc='lower left', fontsize=9)
    figure.text(.5, -.035, 'Conditional calculation at inherited masses and F=0.5. Not a present-day power spectrum or data fit.',
        ha='center', fontsize=9)
    figure.savefig(folder / 'early-growth-control.png', dpi=160, bbox_inches='tight')
    plt.close(figure)
    finish(folder, dict(plotted_four_modes=4, epoch_scale_factor=.00025,
        source_kind='Computed native perturbations, not observations'), __file__, [source, folder / 'early-growth-control.png'])


if __name__ == '__main__':
    main()

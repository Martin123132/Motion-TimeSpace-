from __future__ import annotations

from spectrum_common import *
os.environ['MPLCONFIGDIR']=str(ROOT/'runs/matplotlib-cache')
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt


def main():
    modest()
    report=json.loads((ROOT/'results/spectrum/status.json').read_text())
    by_label={row['label']:row for row in report['branches']}
    source=np.load(ROOT/'sources/sdss-growth/growth-only.npz')
    figure,axes=plt.subplots(1,2,figsize=(12,4.7),layout='constrained')
    palette={'heavy':'#087f8c','cold':'#c26b19','lcdm':'#535b68'}
    titles={'heavy':'Heavy benchmark (F=0.5)','cold':'Same slow field, all-cold matter','lcdm':'Matched LCDM'}
    for label in ['lcdm','cold','heavy']:
        data=np.load(ROOT/'results/spectrum'/(label+'.npz'))
        valid=(data['modes']>=.0001)&data['pressure_qualified_band']
        axes[0].loglog(data['modes'][valid],data['linear_power_Mpc3'][valid,-1],color=palette[label],label=titles[label],linewidth=1.8)
        rows=sorted([row for row in by_label[label]['central'] if row['z']<=1.5],key=lambda row:row['z'])
        axes[1].plot([row['z'] for row in rows],[row['fsigma8_cdm_m'] for row in rows],'-o',
            color=palette[label],markersize=3,label=titles[label])
    axes[0].set(xlabel='k [Mpc$^{-1}$]',ylabel='Linear matter power [Mpc$^3$]',title='Resolved native spectrum at z=0')
    axes[0].legend(fontsize=8,loc='lower left')
    axes[1].errorbar(source['redshifts'],source['mean'],yerr=np.sqrt(np.diag(source['covariance'])),
        fmt='o',color='black',capsize=3,label='SDSS growth marginals')
    axes[1].set(xlabel='Redshift',ylabel='Velocity–density growth statistic',xlim=(-.04,1.6),
        title='Conditional comparison — not a parameter fit')
    axes[1].legend(fontsize=8,loc='best')
    for axis in axes:
        axis.grid(alpha=.18)
        axis.spines[['top','right']].set_visible(False)
    figure.text(.5,-.035,'Common inherited primordial normalization; linear theory. SDSS compression/template assumptions still require forward validation.',
        ha='center',fontsize=9)
    figure.savefig(ROOT/'results/spectrum-and-growth.png',dpi=170,bbox_inches='tight')
    plt.close(figure)


if __name__=='__main__':
    main()

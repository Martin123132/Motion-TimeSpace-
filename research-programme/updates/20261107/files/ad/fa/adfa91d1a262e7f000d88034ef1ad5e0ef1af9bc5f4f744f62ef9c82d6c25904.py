from __future__ import annotations

from window_common import *
os.environ['MPLCONFIGDIR']=str(ROOT/'runs/matplotlib-cache')
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt


def main():
    modest()
    figure,axes=plt.subplots(2,2,figsize=(11.8,7.4),layout='constrained')
    colors={'heavy':'#087f8c','cold':'#c26b19','lcdm':'#535b68'}
    styles={'heavy':'-','cold':'--','lcdm':':'}
    names={'heavy':'Retained heavy benchmark','cold':'Same slow field, cold matter','lcdm':'Matched LCDM'}
    for column,cap in enumerate(['NGC','SGC']):
        survey=np.load(ROOT/'results/prepared'/(cap+'.npz'))
        observed=survey['data'];errors=np.sqrt(np.diag(survey['covariance']))
        band=(KOUT>.02)&(KOUT<.12)
        for row,ell in enumerate([0,2]):
            axis=axes[row,column]
            indices=np.arange(40)[band]+ell*40
            kvalues=survey['k_effective'][band]
            axis.errorbar(kvalues,kvalues*observed[indices],yerr=kvalues*errors[indices],fmt='o',
                color='black',markersize=4,capsize=2,label='BOSS DR12 measurements')
            for label in ['lcdm','cold','heavy']:
                packet=np.load(ROOT/'results/diagnostic-fits'/f'{label}-{cap}-0.1-2.npz')
                axis.plot(kvalues,kvalues*packet['prediction'][indices],color=colors[label],linestyle=styles[label],label=names[label])
            axis.axvspan(.1,.12,color='grey',alpha=.08)
            axis.set(xlim=(.02,.12),xlabel='k [h/Mpc]',ylabel=f'k P{ell} [(Mpc/h)$^2$]',
                title=f'{cap}, z=0.38 — '+('monopole' if ell==0 else 'quadrupole'))
            axis.spines[['top','right']].set_visible(False)
            axis.grid(alpha=.15)
    axes[0,0].legend(fontsize=8)
    figure.suptitle('Existing field predictions through the actual survey response',fontsize=15)
    figure.text(.5,-.028,'Fixed field/cosmological parameters; equal bias + noise fits per cap. Fit: .02<k<.10; shaded points outside fit. Linear diagnostic.',
        ha='center',fontsize=9)
    output=ROOT/'results/boss-window-comparison.png'
    figure.savefig(output,dpi=160,bbox_inches='tight')
    plt.close(figure)


if __name__=='__main__':
    main()

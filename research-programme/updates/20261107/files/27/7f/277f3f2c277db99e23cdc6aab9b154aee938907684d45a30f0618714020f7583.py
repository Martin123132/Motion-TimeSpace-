from __future__ import annotations

from stage_common import *
os.environ['MPLCONFIGDIR']=str(ROOT/'runs/matplotlib-cache')
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np


def main():
    modest()
    report=json.loads((ROOT/'results/late-comparison/status.json').read_text())
    labels=[str(row['k_Mpc_inverse']) for row in report['rows']]
    positions=np.arange(len(labels))
    figure,axes=plt.subplots(1,2,figsize=(11,4.6),layout='constrained')
    figure.suptitle('The retained heavy mode now evolves into late matter growth',fontsize=15,weight='bold')
    colors=['#157f89','#b35f20']
    for offset,key,color,title in [(-.18,'power_ratio_heavy_to_slow_cold',colors[0],'Relative to slow-field cold control'),
        (.18,'power_ratio_heavy_to_LCDM',colors[1],'Relative to matched LCDM')]:
        axes[0].bar(positions+offset,[row[key] for row in report['rows']],.34,color=color,label=title)
    axes[0].set(yscale='log',ylim=(.0008,1.5),xticks=positions,xticklabels=labels,
        ylabel='Linear matter power ratio at z=0',xlabel='k [Mpc$^{-1}$] — four sampled modes')
    axes[0].axhline(1,color='#333333',linewidth=.8)
    axes[0].legend(fontsize=8,loc='lower left')
    groups=[row for row in report['comparisons'] if row['label'] in ['late-200','late-250','late-225-bg4']]
    for row,marker in zip(groups,['o','s','^']):
        axes[1].plot(positions,np.array(row['today_fractional_change_from_central'])*1e6,marker,
            markersize=6,label=row['label'])
    axes[1].axhline(0,color='#333333',linewidth=.8)
    axes[1].set(xticks=positions,xticklabels=labels,xlabel='k [Mpc$^{-1}$]',
        ylabel='Change in final amplitude [parts per million]',title='Changing the handoff epoch and resolution')
    axes[1].legend(fontsize=8)
    for axis in axes:
        axis.grid(axis='y',alpha=.2)
        axis.set_axisbelow(True)
        axis.spines[['top','right']].set_visible(False)
    figure.text(.5,-.035,'Conditional F=0.5 benchmark; common primordial amplitude. Four linear samples, not a fit or nonlinear prediction.',
        ha='center',fontsize=9)
    figure.savefig(ROOT/'results/late-matter-summary.png',dpi=170,bbox_inches='tight')
    plt.close(figure)


if __name__=='__main__':
    main()

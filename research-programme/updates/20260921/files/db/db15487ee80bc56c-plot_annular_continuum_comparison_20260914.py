import os
os.environ['PYTHONDONTWRITEBYTECODE'] = '1'
for name in ['OPENBLAS_NUM_THREADS','OMP_NUM_THREADS','MKL_NUM_THREADS']:
    os.environ[name] = '1'
from navier_stokes_source_audit_20260908 import limit_process
limit_process()

import json
from annular_reference_continuum_shell_20260914 import EvidenceRun


def run():
    evidence = EvidenceRun('annular-continuum-comparison-figure-attempt01',__file__)
    try:
        os.environ['MPLCONFIGDIR'] = str(evidence.output/'matplotlib-config')
        import matplotlib
        matplotlib.use('Agg')
        import matplotlib.pyplot as plt
        from matplotlib.ticker import ScalarFormatter
        intake = evidence.root/'source-intake/navier-stokes/20260914'
        sources = [
            intake/'annular-continuum-regulator-comparison-attempt01/status.json',
            intake/'annular-continuum-physical-sampling-attempt01/status.json']
        statuses = []
        for path in sources:
            evidence.own(path)
            status = json.loads(path.read_text())
            evidence.check(path.parent.name+'_passed',status['state']=='complete' and all(row['passed'] for row in status['checks']))
            statuses.append(status)
        chart_rows = [[row for row in status['cases'] if row['time']==.06] for status in statuses]
        evidence.check('six_rows_each_panel',all(len(rows)==6 for rows in chart_rows))
        physical = chart_rows[1]
        worst_noise = max(max(row['momentum_refinement_noise']/row['momentum_energy_norm'],
                              row['gradient_refinement_noise']/row['gradient_energy_norm']) for row in physical)
        plt.rcParams.update({'font.size':11,'axes.titlesize':12,'axes.labelsize':11,
                             'axes.spines.top':False,'axes.spines.right':False})
        figure,axes = plt.subplots(1,2,figsize=(12,5.4))
        colours = {'reference':'#087E8B','MTS':'#7944B8'}
        markers = {'reference':'o','MTS':'s'}
        styles = {'reference':'--','MTS':'-'}
        labels = {'reference':'Nearest-neighbour reference','MTS':'MTS regulator'}
        titles = ['Common-coordinate comparison','Actual-position comparison']
        for axis,rows,title in zip(axes,chart_rows,titles):
            for branch in ['reference','MTS']:
                selected = sorted([row for row in rows if row['branch']==branch],key=lambda row:row['count'])
                axis.plot([row['count'] for row in selected],[row['energy_error'] for row in selected],
                          color=colours[branch],marker=markers[branch],linestyle=styles[branch],
                          linewidth=1.8,markersize=6,label=labels[branch])
            axis.set_xscale('log',base=2)
            axis.set_yscale('log')
            axis.set_xticks([33,65,129])
            axis.xaxis.set_major_formatter(ScalarFormatter())
            axis.set_ylim(1e-6,1e-3)
            axis.set_xlim(29,145)
            axis.grid(axis='y',which='major',color='#DDE1E6',linewidth=.7)
            axis.set_title(title,pad=12,loc='left')
            axis.set_xlabel('Regulator nodes')
            axis.set_ylabel('Energy-error diagnostic (pilot units)')
            axis.legend(loc='upper right',frameon=False,fontsize=9.5)
        figure.suptitle('Both regulator branches approach the independent GR solution',
                        x=.075,y=.98,ha='left',fontsize=16,fontweight='bold')
        figure.text(.075,.915,'Same pulse, shell and midpoint clock | t = 0.06 pilot units: numerical diagnostic, not the proved time interval',
                    fontsize=10.5,color='#444444')
        figure.text(.075,.065,'Continuum grids: 513 / 1,025 / 2,049. No fitted parameters or observational data.',fontsize=10,color='#444444')
        figure.text(.075,.025,'Actual-position p/gradient target-refinement differences are at most '+
                    format(100*worst_noise,'.2f')+'% of the plotted cases’ component errors; these are estimates, not rigorous bounds.',
                    fontsize=9.5,color='#444444')
        figure.subplots_adjust(left=.075,right=.98,bottom=.20,top=.81,wspace=.27)
        path = evidence.output/'continuum-comparison.png'
        figure.savefig(path,dpi=160,facecolor='white')
        plt.close(figure)
        evidence.own(path,'outputs')
        data = evidence.output/'chart-data.json'
        data.write_text(json.dumps(dict(time=.06,continuum_nodes=2049,panels=chart_rows,
                                        primary_definition='Half the joint-layer momentum-plus-gradient squared error at base labels.',
                                        physical_definition='Half the momentum-plus-gradient squared error at actual collar positions; p strictly interior.',
                                        physical_max_target_refinement_ratio=worst_noise,
                                        no_observational_claim=True),indent=2)+'\n')
        evidence.own(data,'outputs')
        for path in (evidence.output/'matplotlib-config').rglob('*'):
            if path.is_file():
                evidence.own(path,'outputs')
        evidence.check('rendered_png_nonempty',(evidence.output/'continuum-comparison.png').stat().st_size>20000)
        evidence.complete()
    except Exception as error:
        evidence.fail(error)
        raise


if __name__=='__main__':
    run()


import os
os.environ['PYTHONDONTWRITEBYTECODE'] = '1'
for name in ['OPENBLAS_NUM_THREADS','OMP_NUM_THREADS','MKL_NUM_THREADS']:
    os.environ[name] = '1'
from navier_stokes_source_audit_20260908 import limit_process
limit_process()

import json
import math
import subprocess
from pathlib import Path
from html import escape
from annular_reference_continuum_shell_20260914 import EvidenceRun


def run():
    evidence = EvidenceRun('annular-continuum-comparison-figure-attempt02',__file__)
    try:
        intake = evidence.root/'source-intake/navier-stokes/20260914'
        sources = [intake/'annular-continuum-regulator-comparison-attempt01/status.json',
                   intake/'annular-continuum-physical-sampling-attempt01/status.json']
        chart_rows = []
        for path in sources:
            evidence.own(path)
            status = json.loads(path.read_text())
            evidence.check(path.parent.name+'_passed',status['state']=='complete' and all(row['passed'] for row in status['checks']))
            chart_rows.append([row for row in status['cases'] if row['time']==.06])
        evidence.check('six_rows_each_panel',all(len(rows)==6 for rows in chart_rows))
        worst_noise = max(max(row['momentum_refinement_noise']/row['momentum_energy_norm'],
                              row['gradient_refinement_noise']/row['gradient_energy_norm']) for row in chart_rows[1])
        parts = ['<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="590" viewBox="0 0 1200 590">',
                 '<rect width="1200" height="590" fill="white"/>',
                 '<g font-family="Arial, sans-serif" fill="#232A33">']
        def label(xvalue,yvalue,value,size=13,anchor='start',extra=''):
            parts.append('<text x="'+str(xvalue)+'" y="'+str(yvalue)+'" font-size="'+str(size)+
                         '" text-anchor="'+anchor+'" '+extra+'>'+escape(value)+'</text>')
        def line(xfirst,yfirst,xsecond,ysecond,colour,width=1,dashed=False):
            parts.append('<line x1="'+str(xfirst)+'" y1="'+str(yfirst)+'" x2="'+str(xsecond)+
                         '" y2="'+str(ysecond)+'" stroke="'+colour+'" stroke-width="'+str(width)+'"'+
                         (' stroke-dasharray="7 5"' if dashed else '')+'/>')
        label(80,42,'Both regulator branches approach the independent GR solution',25,extra='font-weight="bold"')
        label(80,76,'Same pulse, shell and midpoint clock | t = 0.06 pilot units: diagnostic beyond the proved interval',15)
        colours = {'reference':'#087E8B','MTS':'#7944B8'}
        for xpos,branch,title in [(80,'reference','Nearest-neighbour reference'),(420,'MTS','MTS regulator')]:
            line(xpos,111,xpos+35,111,colours[branch],2.4,branch=='reference')
            label(xpos+46,116,title,14)
        for left,rows,title in zip([80,675],chart_rows,['Common base coordinates','Actual collar positions']):
            top,bottom,width = 188,467,445
            label(left,160,title,18,extra='font-weight="bold"')
            def map_x(count):
                return left+width*(math.log(count)-math.log(29))/(math.log(145)-math.log(29))
            def map_y(value):
                return bottom-(math.log10(value)+6)*(bottom-top)/3
            for exponent in [-6,-5,-4,-3]:
                yvalue = map_y(10**exponent)
                line(left,yvalue,left+width,yvalue,'#DDE1E6')
                label(left-12,yvalue+4,'1e'+str(exponent),12,'end')
            line(left,top,left,bottom,'#6B7280')
            line(left,bottom,left+width,bottom,'#6B7280')
            for count in [33,65,129]:
                xvalue = map_x(count)
                line(xvalue,bottom,xvalue,bottom+5,'#6B7280')
                label(xvalue,bottom+23,str(count),13,'middle')
            label(left+width/2,514,'Regulator nodes',14,'middle')
            ylabel_x = left-53
            label(ylabel_x,327,'Energy-error diagnostic (pilot units)',13,'middle',
                  'transform="rotate(-90 '+str(ylabel_x)+' 327)"')
            for branch in ['reference','MTS']:
                selected = sorted([row for row in rows if row['branch']==branch],key=lambda row:row['count'])
                points = [(map_x(row['count']),map_y(row['energy_error'])) for row in selected]
                evidence.check(title+'_'+branch+'_inside_axes',all(top<yvalue<bottom for unused_x,yvalue in points))
                parts.append('<polyline points="'+' '.join(str(xvalue)+','+str(yvalue) for xvalue,yvalue in points)+
                             '" fill="none" stroke="'+colours[branch]+'" stroke-width="2.4"'+
                             (' stroke-dasharray="7 5"' if branch=='reference' else '')+'/>')
                for xvalue,yvalue in points:
                    if branch=='reference':
                        parts.append('<circle cx="'+str(xvalue)+'" cy="'+str(yvalue)+'" r="4.6" fill="'+colours[branch]+'"/>')
                    else:
                        parts.append('<rect x="'+str(xvalue-4.3)+'" y="'+str(yvalue-4.3)+'" width="8.6" height="8.6" fill="'+colours[branch]+'"/>')
        label(80,550,'Continuum grids: 513 / 1,025 / 2,049. No fitted parameters or observational data.',13)
        label(80,577,'Actual-position target refinement: at most '+format(100*worst_noise,'.2f')+
              '% of these component errors. Refinement estimates are not rigorous bounds.',12)
        parts.extend(['</g>','</svg>'])
        svg = evidence.output/'continuum-comparison.svg'
        png = evidence.output/'continuum-comparison.png'
        svg.write_text('\n'.join(parts),encoding='utf-8')
        evidence.own(svg,'outputs')
        node = Path(r'C:\Users\ollet\.cache\codex-runtimes\codex-primary-runtime\dependencies\node\bin\node.exe')
        sharp = Path(r'C:\Users\ollet\.cache\codex-runtimes\codex-primary-runtime\dependencies\node\node_modules\sharp\dist\index.cjs')
        evidence.check('bundled_renderer_exists',node.is_file() and sharp.is_file())
        command = "const sharp=require(process.argv[1]); sharp.concurrency(1); sharp.cache(false); sharp(process.argv[2]).png().toFile(process.argv[3]).catch(error=>{process.stderr.write(String(error));process.exit(1);});"
        rendered = subprocess.run([str(node),'-e',command,str(sharp),str(svg),str(png)],
                                   capture_output=True,text=True,timeout=60,
                                   creationflags=0x08000000|0x00004000 if os.name=='nt' else 0)
        evidence.check('svg_rendered_to_png',rendered.returncode==0,rendered.stderr)
        evidence.check('png_nonempty',png.is_file() and png.stat().st_size>20000)
        evidence.own(png,'outputs')
        data = evidence.output/'chart-data.json'
        data.write_text(json.dumps(dict(time=.06,continuum_nodes=2049,panels=chart_rows,
                                        physical_max_target_refinement_ratio=worst_noise,
                                        no_observational_claim=True,
                                        rendering='Native SVG and bundled Node/Sharp; no environment installs.'),indent=2)+'\n')
        evidence.own(data,'outputs')
        evidence.complete()
    except Exception as error:
        evidence.fail(error)
        raise


if __name__=='__main__':
    run()


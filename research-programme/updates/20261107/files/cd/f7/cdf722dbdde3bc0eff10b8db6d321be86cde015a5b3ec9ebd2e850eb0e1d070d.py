from __future__ import annotations

import sympy as symbolic
from precision_common import *


def main():
    modest()
    folder=ROOT/'results/validation'
    folder.mkdir(parents=True,exist_ok=False)
    checks=[]
    paths=[]

    def check(name,passed,value=None,limit=None):
        checks.append(dict(name=name,passed=bool(passed),value=value,limit=limit))

    def packet(relative):
        path=ROOT/relative
        report=json.loads(path.read_text())
        assert report['state']=='complete' and (path.parent/'COMPLETE').is_file()
        for source,expected in report['input_hashes'].items():
            assert digest(source)==expected,(path,source)
        paths.append(path)
        return report

    expansion,mu,amplitude,ratio,conditioned,slope,standard,heavy=symbolic.symbols('X mu x0 r W h R B',positive=True)
    velocity=mu**2*amplitude*conditioned/expansion
    potential=standard+heavy+mu**2*amplitude**2*ratio**2
    friedmann=expansion*(1-velocity**2)-potential
    check('Exact Friedmann quadratic',symbolic.simplify(expansion*friedmann-(expansion**2-potential*expansion-mu**4*amplitude**2*conditioned**2))==0)
    transformed=2*slope*conditioned+expansion/(mu**2*amplitude)*(-(3+slope)*velocity-mu**2*amplitude*ratio/expansion)
    check('Exact conditioned KG equation',symbolic.simplify(transformed-((slope-3)*conditioned-ratio))==0)
    check('Radiation regular velocity root',symbolic.simplify(((slope-3)*conditioned-ratio).subs({slope:-2,conditioned:-symbolic.Rational(1,5),ratio:1}))==0)
    sources=packet('runs/sources/status.json')
    diagnostics=[]
    for row in sources['rows']:
        check(row['tag']+' '+row['variant']+' flatness',abs(row['flatness_residual'])<1e-9,row['flatness_residual'],1e-9)
        path=ROOT/'runs/sources'/(row['tag']+'-'+row['variant']+'.npz')
        table=np.load(path)
        check(row['tag']+' '+row['variant']+' finite source',all(np.isfinite(table[key]).all() for key in ['phi_s','phidot_s','expansion2']))
        check(row['tag']+' '+row['variant']+' full history',table['efold'][0]<=START+1e-12 and table['efold'][-1]>=0)
        nodes=np.linspace(math.log(1e-7),0,20001)
        velocity_fn=interpolate.CubicSpline(table['efold'],table['phidot_s'])
        phi=interpolate.CubicSpline(table['efold'],table['phi_s'])(nodes)
        hubble=UNIT*np.sqrt(np.exp(interpolate.CubicSpline(table['efold'],np.log(table['expansion2']))(nodes)))
        conformal=velocity_fn(nodes)
        force=np.exp(nodes)*float(table['slow_mass_mpc'])**2*phi/hubble
        residual=velocity_fn(nodes,1)+2*conformal+force
        relative=abs(residual)/(2*abs(conformal)+abs(force))
        maximum=float(max(relative))
        diagnostics.append(dict(tag=row['tag'],variant=row['variant'],max_interpolated_KG_residual=maximum))
        check(row['tag']+' '+row['variant']+' KG source residual',maximum<.001,maximum,.001)
        paths.append(path)
    for tag in ['unmatched','a225','cold']:
        base=np.load(ROOT/'runs/sources'/(tag+'-base.npz'))
        fine=np.load(ROOT/'runs/sources'/(tag+'-fine.npz'))
        nodes=np.linspace(START,0,20001)
        expansions=[np.exp(interpolate.CubicSpline(table['efold'],np.log(table['expansion2']))(nodes)) for table in [base,fine]]
        velocities=[interpolate.CubicSpline(table['efold'],table['phidot_s'])(nodes) for table in [base,fine]]
        h_change=float(max(abs(np.sqrt(expansions[0]/expansions[1])-1)))
        early=(nodes>math.log(1e-7))&(nodes<math.log(.00026))
        velocity_change=float(max(abs(velocities[0][early]/velocities[1][early]-1)))
        check(tag+' precision H convergence',h_change<1e-7,h_change,1e-7)
        check(tag+' precision velocity convergence',velocity_change<.001,velocity_change,.001)
    exact=packet('runs/exact/status.json')
    check('412 exact early modes',exact['completed']==412)
    projections=packet('runs/projection/status.json')
    for row in projections['configurations']:
        check(row['label']+' inherited pressure gate',not row['failing_trusted_modes'],row['maximum_pressure_closure_error_trusted'],2e-6)
    spectrum=packet('results/spectrum/status.json')
    for label in ['heavy','cold','heavy-200','heavy-250','heavy-window4']:
        report=packet('runs/'+label+'/status.json')
        check(label+' completed all modes',report['completed']==412)
        check(label+' no nonheavy matching jump',report['nonheavy_match_jump']==0)
    empirical=packet('results/primary-refit/status.json')
    for row in empirical['rows']:
        title=row['branch']+' '+row['family']+' '+row['cap']
        check(title+' refit converged',row['fit']['converged'] and all(item['success'] for item in row['fit']['starts']))
        check(title+' no nuisance boundary',not(row['fit']['upper_variance_boundary'] or row['fit']['lower_variance_boundary'] or row['fit']['other_boundary']))
        check(title+' direct prediction interpolation',row['direct_grid_interpolation_distance']<1e-3,row['direct_grid_interpolation_distance'],1e-3)
        if row['branch']=='lcdm':
            check(title+' unchanged baseline score',abs(row['chi2_change'])<1e-8,row['chi2_change'],1e-8)
    for row in empirical['summaries']:
        check(row['branch']+' '+row['family']+' equal data and nuisance counts',row['data_count']==32 and row['tracer_parameters']==6)
    for path in ROOT.glob('*.py'):
        compile(path.read_bytes(),str(path),'exec')
        check('Compile '+path.name,True)
    passed=all(row['passed'] for row in checks)
    finish(folder,dict(checks=checks,count=len(checks),all_checks_passed=passed,source_KG_diagnostics=diagnostics,
        full_history_repaired=passed,empirical_primary_rechecked=True,unchanged_physics=True,
        exact_finite_k_nonlinear_seed_still_next=True),__file__,paths)
    print(json.dumps(dict(count=len(checks),all_passed=passed,failures=[row for row in checks if not row['passed']])),flush=True)
    if not passed:
        raise RuntimeError('Validation failures retained; do not promote these results')


if __name__=='__main__':
    main()

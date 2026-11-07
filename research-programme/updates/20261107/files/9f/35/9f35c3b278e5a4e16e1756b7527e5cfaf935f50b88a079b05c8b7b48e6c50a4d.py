from common import *
from cold_math import coefficients, symbolic
import ast
import csv
import numpy as np
import sympy as sp


def extra_symbolic():
    cdm, baryon, photon, radiation, defect = sp.symbols('Rc Rb Rg Rr DeltaW', real=True)
    density = sp.symbols('d0:5', positive=True)
    speeds = sp.symbols('v0:5', positive=True)
    hubble, wave, slow_frequency, slow_velocity, heavy_velocity = sp.symbols('H k Os vs vh', positive=True)
    current = [(cdm-defect)/sp.sqrt(cdm), sp.sqrt(baryon), 2*sp.sqrt(photon)/sp.sqrt(3), 2*sp.sqrt(radiation)/sp.sqrt(3)]
    current += [2*sp.sqrt(value)/sp.sqrt(3) for value in density]
    current += [wave*slow_velocity/slow_frequency, heavy_velocity]
    expected = (cdm-defect)**2/cdm+baryon+sp.Rational(4,3)*(photon+radiation+sum(density))+(wave*slow_velocity/slow_frequency)**2+heavy_velocity**2
    checks = dict(current_dual=sp.simplify(sum(value**2 for value in current)-expected))
    for ufa in (False, True):
        radiation_factor = sp.Integer(2) if ufa else sp.Rational(4,5)
        shear = [sp.sqrt(4*photon/5), sp.sqrt(radiation_factor*radiation)]
        shear += [2*sp.sqrt(value)*velocity/sp.sqrt(5) for value, velocity in zip(density,speeds)]
        expected_shear = sp.Rational(4,5)*photon+radiation_factor*radiation+sp.Rational(4,5)*sum(value*velocity**2 for value,velocity in zip(density,speeds))
        checks['shear_dual_'+str(ufa)] = sp.simplify(sum(value**2 for value in shear)-expected_shear)
    require(all(value == 0 for value in checks.values()), 'physical dual identities')
    return {name: str(value) for name,value in checks.items()}


def gamma(matrix):
    symmetric = (matrix + matrix.T) / 2
    return float(np.linalg.eigvalsh(symmetric)[-1])


def main():
    modest()
    check_parent()
    checks, evidence, reports, aggregate = [], {}, [], []
    def check(name, condition, value=None):
        checks.append(dict(name=name, passed=bool(condition), value=value))
        require(condition, name)
    def source(path):
        evidence[str(path)] = digest(path)
    for path in STAGE.glob('*.py'):
        ast.parse(path.read_text())
        check('parse '+path.name, True)
        source(path)
    write(ROOT/'dual-symbolic.json', extra_symbolic())
    check('symbolic replay', all(value=='0' for value in symbolic().values()))
    max_error,max_algebra=0.,0.
    for family in ('half','balanced','double'):
        directory=STAGE/family
        manifest=read(directory/'inputs.json')
        for path,expected in manifest['sources'].items():
            check('frozen '+family+' '+Path(path).name,digest(path)==expected)
            source(path)
        source(directory/'inputs.json')
        source(directory/'symbolic.json')
        check(family+' symbolic',all(value=='0' for value in read(directory/'symbolic.json').values()))
        limits=read(directory/'coefficient-limits.json')
        source(directory/'coefficient-limits.json')
        check(family+' 240 limit points',len(limits['rows'])==240)
        for index,row in enumerate(limits['rows']):
            epsilon,speed,eta=row['epsilon'],row['speed'],row['eta']
            width,width_rate,diagonal0,diagonal1,cross,formula,upper=coefficients(epsilon,speed,eta)
            independent=float(np.linalg.eigvalsh([[diagonal0,cross],[cross,diagonal1]])[-1])
            check(family+' limit '+str(index),row['passed'] and abs(independent-row['actual_log_norm'])<ALGEBRA and independent<=row['upper']+ALGEBRA)
            if speed==0:
                check(family+' zero-speed '+str(index),abs(width-2*epsilon)<ALGEBRA and abs(width_rate-eta)<ALGEBRA and abs(cross+1/np.sqrt(3))<ALGEBRA)
        combined=read(directory/'result.json')
        source(directory/'result.json')
        check(family+' family pass',combined['passed'] and len(combined['reports'])==2)
        for report in combined['reports']:
            tag=family+'/'+report['model']
            source(directory/(report['model']+'-result.json'))
            check(tag+' coefficient hash',digest(report['coefficient_input']['path'])==report['coefficient_input']['sha256'])
            source(report['coefficient_input']['path'])
            check(tag+' 97 points',len(report['rows'])==97)
            check(tag+' branch evaluations',report['native_vectors']==582)
            for name,value in report['errors'].items():
                check(tag+' numerical '+name,value<GATE,value)
                max_error=max(max_error,value)
            for name,value in report['algebra'].items():
                check(tag+' algebra '+name,value<ALGEBRA,value)
                max_algebra=max(max_algebra,value)
            gamma_values={'gr':[],'poisson-spatial':[]}
            for index,row in enumerate(report['rows']):
                check(tag+' massive free '+str(index),row['massive_log_norm_max']<=row['simple_massive_bound']+ALGEBRA)
                check(tag+' physical finite '+str(index),all(np.isfinite(row[name]) and row[name]>=0 for name in ('current_row_over_H','density_row_over_k','shear_row_over_H','cdm_dual_K','density_dual_K','balanced_current_force_over_k','balanced_shear_force_over_k','balanced_primitive_over_H')))
                for branch,comparison in row['comparisons'].items():
                    actual=np.array(comparison['actual'])
                    upper=np.array(comparison['upper'])
                    scale=max(1.,float(np.max(abs(actual))))
                    check(tag+' comparison '+branch+' '+str(index),np.max(actual-upper)<=ALGEBRA*scale)
                    growth=gamma(upper)
                    formula=.5*(upper[0,0]+upper[1,1]+np.hypot(upper[0,0]-upper[1,1],upper[0,1]+upper[1,0]))
                    check(tag+' growth '+branch+' '+str(index),abs(growth-formula)<=ALGEBRA*max(1.,abs(growth)) and gamma(actual)<=growth+ALGEBRA*scale)
                    gamma_values[branch].append(growth)
            summary=dict(family=family,model=report['model'],points=97,native_branch_evaluations=582,
                         maximum_numerical_error=max(report['errors'].values()),maximum_algebra_error=max(report['algebra'].values()),
                         epsilon_min=min(row['epsilon'] for row in report['rows']),epsilon_max=max(row['epsilon'] for row in report['rows']),
                         maximum_kv_over_H=max(row['maximum_kv_over_H'] for row in report['rows']),
                         massive_log_norm_max=max(row['massive_log_norm_max'] for row in report['rows']),
                         sampled_gr_Gamma_max=max(gamma_values['gr']),sampled_poisson_Gamma_max=max(gamma_values['poisson-spatial']),
                         sampled_current_dual_max=max(row['current_row_over_H'] for row in report['rows']),
                         sampled_shear_dual_max=max(row['shear_row_over_H'] for row in report['rows']),
                         sampled_cdm_K_max=max(row['cdm_dual_K'] for row in report['rows']),
                         sampled_density_K_max=max(row['density_dual_K'] for row in report['rows']),
                         continuous_supremum_certified=False)
            aggregate.append(summary)
            reports.append(dict(family=family,model=report['model'],path=str(directory/(report['model']+'-result.json'))))
    with (ROOT/'comparisons.csv').open('x',newline='',encoding='utf-8') as stream:
        writer=csv.DictWriter(stream,fieldnames=list(aggregate[0]))
        writer.writeheader()
        writer.writerows(aggregate)
    check_parent()
    write(ROOT/'summary.json',dict(passed=True,evidence_hashes=evidence,reports=reports,comparisons=aggregate,
                                  locations=582,native_branch_evaluations=3492,distinct_coefficient_cases=240,
                                  maximum_numerical_error=max_error,maximum_algebra_error=max_algebra,
                                  new_physical_ode_solves=0,continuous_supremum_certified=False))
    write(ROOT/'validation.json',dict(passed=True,count=len(checks),checks=checks))
    print('all',len(checks),'checks passed; max numerical',max_error,'max algebra',max_algebra,flush=True)
    print(json.dumps(aggregate,indent=2),flush=True)


if __name__=='__main__':
    main()

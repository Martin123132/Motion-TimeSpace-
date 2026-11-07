from derive_annular_source_gravity_20260914 import EvidenceRun
from search_annular_nonzero_shape_constraint_v3_20261001 import whiten
from scipy.optimize import minimize
from decimal import Decimal, localcontext
from fractions import Fraction
from time import perf_counter
import hashlib
import json
import numpy as np


def positive_rational(matrix):
    count = len(matrix)
    lower = [[Fraction(int(row==column)) for column in range(count)] for row in range(count)]
    diagonal = []
    for row in range(count):
        pivot = matrix[row][row]-sum(lower[row][column]**2*diagonal[column] for column in range(row))
        if pivot<=0:
            return None
        diagonal.append(pivot)
        for last in range(row+1,count):
            lower[last][row] = (matrix[last][row]-sum(lower[last][column]*lower[row][column]*diagonal[column]
                for column in range(row)))/pivot
    return [str(value) for value in diagonal]


def separator(forces,gram,size):
    forces = (forces[:size-1,:size,:size]+forces[:size-1,:size,:size].transpose(0,2,1))/2
    gram = (gram[:size,:size]+gram[:size,:size].T)/2
    transform = whiten(gram)
    if transform is None:
        return dict(found=False,reason='trial_norm_rank_unresolved')
    operators = np.einsum('ai,kab,bj->kij',transform,forces,transform)
    scales = np.maximum(np.linalg.norm(operators,axis=(1,2)),1e-300)
    operators /= scales[:,None,None]

    def minimum(weights):
        eigenvalues,eigenvectors = np.linalg.eigh(np.einsum('k,kij->ij',weights,operators))
        vector = eigenvectors[:,0]
        derivative = np.einsum('i,kij,j->k',vector,operators,vector)
        return float(eigenvalues[0]),derivative

    candidates = []
    for test in range(size-1):
        for sign in [-1,1]:
            weights = np.zeros(size-1)
            weights[test] = sign
            candidates.append((minimum(weights)[0],weights))
    initial = sorted(candidates,key=lambda item:item[0],reverse=True)[:4]
    for unused,weights in initial:
        result = minimize(lambda value:-minimum(value)[0],weights,jac=lambda value:-minimum(value)[1],
            method='SLSQP',constraints=[dict(type='ineq',fun=lambda value:1-value@value,jac=lambda value:-2*value)],
            options=dict(maxiter=250,ftol=1e-12))
        if np.linalg.norm(result.x)>1:
            result.x /= np.linalg.norm(result.x)
        candidates.append((minimum(result.x)[0],result.x))
    margin,weights = max(candidates,key=lambda item:item[0])
    result = dict(found=False,size=size,optimized_minimum_eigenvalue=float(margin),
        computational_weights=weights.tolist(),force_scales=scales.tolist())
    if margin<=1e-8:
        return dict(result,reason='no_positive_separator_found')
    coefficients = weights/scales
    coercivity = margin/8
    rational = lambda value:Fraction.from_float(float(value))
    matrix = [[sum(rational(coefficients[test])*rational(forces[test,row,column]) for test in range(size-1))
        -rational(coercivity)*rational(gram[row,column]) for column in range(size)] for row in range(size)]
    pivots = positive_rational(matrix)
    if pivots is None:
        return dict(result,reason='rational_positive_definiteness_failed')
    return dict(result,found=True,coercivity=float(coercivity),coefficients=coefficients.tolist(),
        exact_LDL_pivots=pivots,scope='Exact positive definiteness for the symmetrized stored binary matrices only',
        implication='These fitted quadratic equations have no simultaneous nonzero root in this finite frozen-metric trial space.')


def main():
    evidence = EvidenceRun('annular-nonzero-shape-search-analysis-attempt01',__file__)
    started = perf_counter()
    try:
        reports,data = {},{}
        digests = {}
        for level in ['fine','third']:
            path = evidence.output.parent/('annular-nonzero-shape-constraint-'+level+'-attempt03')/'status.json'
            report = json.loads(path.read_text())
            evidence.own(path)
            evidence.check(level+':complete',report['state']=='complete' and all(row['passed'] for row in report['checks']))
            for category in ['inputs','outputs']:
                for relative,expected in report[category].items():
                    source = (evidence.root/relative).resolve()
                    if not source.is_relative_to(evidence.root) or hashlib.sha256(source.read_bytes()).hexdigest()!=expected:
                        raise RuntimeError('Changed search input '+relative)
                    digests[str(source.relative_to(evidence.root))] = expected
            reports[level] = report
            for item in report['rule_outputs']:
                path = evidence.root/item['path']
                evidence.own(path)
                with np.load(path,allow_pickle=False) as archive:
                    saved = {name:archive[name].copy() for name in archive.files}
                with localcontext() as context:
                    context.prec = 70
                    for total_name,layer_name in [('forces','force_layers'),('norm','norm_layers'),('potential','potential_layers')]:
                        values = saved[layer_name].reshape(len(saved['weights']),-1)
                        expected = saved[total_name].ravel()
                        worst = Decimal(0)
                        for column in range(values.shape[1]):
                            terms = [Decimal.from_float(float(weight))*Decimal.from_float(float(value))
                                for weight,value in zip(saved['weights'],values[:,column])]
                            exact = sum(terms,Decimal(0))
                            budget = Decimal.from_float(128*np.finfo(float).eps)*sum(map(abs,terms),Decimal(0))+Decimal('1e-90')
                            error = abs(exact-Decimal.from_float(float(expected[column])))
                            worst = max(worst,error/budget)
                        evidence.check(level+':'+item['branch']+':'+str(item['material'])+':'+total_name+':independent_sum',worst<=1,float(worst))
                search_path = evidence.root/item['search_path']
                evidence.own(search_path)
                search = json.loads(search_path.read_text())
                for attempted in search['searches']:
                    if 'best' not in attempted:
                        continue
                    coefficient = np.array(attempted['best']['coefficient'])
                    size = len(coefficient)
                    predicted = np.einsum('i,kij,j->k',coefficient,saved['forces'][:,:size,:size],coefficient)
                    original = np.array(attempted['best']['unscaled_forces'])
                    scale = max(float(np.max(abs(original))),1e-30)
                    evidence.check(level+':'+item['branch']+':'+str(item['material'])+':'+str(size)+':force_replay',
                        float(np.max(abs(predicted-original)))<=1e-13*scale)
                data[level,item['branch'],item['material']] = saved,search
        summaries = []
        for level in ['fine','third']:
            high,search = data[level,'MTS-primary',48]
            low,unused = data[level,'MTS-primary',32]
            for item in search['searches']:
                size = item['size']
                certificate = separator(high['forces'],high['norm'],size)
                if certificate['found']:
                    coefficients = list(map(Fraction.from_float,certificate['coefficients']))
                    coercivity = Fraction.from_float(certificate['coercivity'])
                    forms = (low['forces']+low['forces'].transpose(0,2,1))/2
                    norm = (low['norm']+low['norm'].T)/2
                    matrix = [[sum(coefficients[test]*Fraction.from_float(float(forms[test,row,column]))
                        for test in range(size-1))-coercivity*Fraction.from_float(float(norm[row,column]))
                        for column in range(size)] for row in range(size)]
                    lower_pivots = positive_rational(matrix)
                    certificate['same_separator_lower_rule_positive'] = lower_pivots is not None
                    certificate['lower_exact_LDL_pivots'] = lower_pivots
                best = item.get('best')
                row = dict(level=level,size=size,selected_root=item['frozen_root'],certificate=certificate)
                if best:
                    coefficient = np.array(best['coefficient'])
                    transform = whiten(high['norm'][:size,:size])
                    matrices = np.einsum('ai,kab,bj->kij',transform,high['forces'][:,:size,:size],transform)
                    scales = np.maximum(np.linalg.norm(matrices,axis=(1,2))*high['norm'][0,0],1e-300)
                    low_force = np.einsum('i,kij,j->k',coefficient,low['forces'][:,:size,:size],coefficient)
                    row.update(fitted_max=best['fitted_max'],withheld_max=best['withheld_max'],
                        lower_rule_all_max=float(np.max(abs(low_force)/scales)),
                        relative_field_distance=best['relative_field_distance'],coefficient=coefficient.tolist(),
                        high_unscaled_forces=best['unscaled_forces'],lower_unscaled_forces=low_force.tolist(),
                        candidate_for_live_solve=bool(item['frozen_root'] and best['withheld_max']<=1e-9
                            and np.max(abs(low_force)/scales)<=1e-9))
                summaries.append(row)
                path = evidence.output/(level+'-size'+str(size)+'.json')
                path.write_text(json.dumps(row,indent=2),encoding='utf-8')
                evidence.own(path,'outputs')
                evidence.report['cases'].append(dict(level=level,size=size,path=str(path.relative_to(evidence.root))))
                evidence.save()
        evidence.report.update(summaries=summaries,seconds=perf_counter()-started,github_action=False,subagents_used=False,
            parent_action_changed=False,full_physical_equilibrium=False,
            live_candidates=[row for row in summaries if row.get('candidate_for_live_solve')])
        evidence.complete()
    except Exception as error:
        evidence.fail(error)
        raise


if __name__=='__main__':
    main()


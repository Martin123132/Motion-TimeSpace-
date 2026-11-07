from derive_annular_source_gravity_20260914 import EvidenceRun
from derive_annular_support_map_constraints_20260927 import restore_case
from annular_nested_physical_refinement_v3_20260922 import live_refined
from annular_candidate_midpoint_20260921 import CommonCoordinateAction
from derive_annular_radial_shape_exchange_20260927 import nodal_test
from search_annular_nonzero_shape_constraint_v3_20261001 import profiles
from annular_compensated_acceleration_polynomial_v2_20261001 import decimal_values
from decimal import Decimal, localcontext
from time import perf_counter
import argparse
import ctypes
import hashlib
import json
import numpy as np


def force(action,order):
    labels,weights = np.polynomial.legendre.leggauss(order)
    labels,weights = labels/2,weights/2
    weights *= 6*(labels+.5)*(.5-labels)
    rows = []
    for label in labels:
        row = nodal_test(action,label)
        geometry = row['geometry']
        values,slopes = profiles(geometry['radius'])
        source_values = profiles(row['source'])[0]
        eta = values-geometry['displacement'][:,None]*source_values
        slope = slopes-(geometry['jacobian_source']/geometry['jacobian'])[:,None]*source_values
        with localcontext() as context:
            context.prec = 64
            changed = decimal_values(eta)*decimal_values(row['gradient'])[:,None]
            image_change = np.asarray(action.factor.apply(changed),float)
        image = action.factor_values@row['cardinal']
        gamma = geometry['gradient']
        coefficient = np.asarray(action.sampling@gamma).ravel()
        strain = 2/geometry['radius']+geometry['lapse_log_radial']+geometry['metric_radial']/(2*geometry['metric'])
        load = np.asarray(action.sampling.T@(image**2/2)).ravel()
        rows.append((coefficient*image)@image_change+np.sum((gamma*load)[:,None]*(strain[:,None]*eta-slope),axis=0))
    return labels,weights,np.array(rows),weights@np.array(rows)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--level',choices=['fine','third'],required=True)
    parser.add_argument('--cpu',type=int,choices=[2,4],required=True)
    parser.add_argument('--label',required=True)
    args = parser.parse_args()
    kernel = ctypes.windll.kernel32
    kernel.GetCurrentProcess.restype = ctypes.c_void_p
    kernel.SetProcessAffinityMask.argtypes = [ctypes.c_void_p,ctypes.c_size_t]
    if not kernel.SetProcessAffinityMask(kernel.GetCurrentProcess(),1<<args.cpu):
        raise OSError('Affinity failed')
    evidence = EvidenceRun(args.label,__file__)
    started,deadline = perf_counter(),perf_counter()+3600
    try:
        evidence.own(evidence.root/'DERIVATION-20261001-live-constraint-feedback-probe.md')
        seal_path = evidence.output.parent/'annular-common-jet-jump-stage-integrity-20261001.json'
        seal = json.loads(seal_path.read_text())
        evidence.own(seal_path)
        digests = {}
        for relative,expected in seal['hashes'].items():
            path = (evidence.root/relative).resolve()
            if not path.is_relative_to(evidence.root) or hashlib.sha256(path.read_bytes()).hexdigest()!=expected:
                raise RuntimeError('Changed inherited input '+relative)
            digests[str(path.relative_to(evidence.root))] = expected
        parent_path = evidence.output.parent/('annular-nonzero-shape-constraint-'+args.level+'-attempt03')/'status.json'
        parent = json.loads(parent_path.read_text())
        evidence.own(parent_path)
        evidence.check('state_search_complete',parent['state']=='complete' and all(row['passed'] for row in parent['checks']))
        for category in ['inputs','outputs']:
            for relative,expected in parent[category].items():
                path = (evidence.root/relative).resolve()
                if not path.is_relative_to(evidence.root) or hashlib.sha256(path.read_bytes()).hexdigest()!=expected:
                    raise RuntimeError('Changed search input '+relative)
                digests[str(path.relative_to(evidence.root))] = expected
        item = next(row for row in parent['rule_outputs'] if row['branch']=='MTS-primary' and row['material']==48)
        search_path = evidence.root/item['search_path']
        evidence.own(search_path)
        search = json.loads(search_path.read_text())
        candidate = next(row for row in search['searches'] if row['size']==10)
        coefficients = np.array(candidate['best']['coefficient'])
        basis_path = evidence.root/search['basis_path']
        evidence.own(basis_path)
        with np.load(basis_path,allow_pickle=False) as saved:
            basis = np.array([Decimal(str(value)) for value in saved['basis_exact'].ravel()],dtype=object).reshape(saved['basis_exact'].shape)
        with localcontext() as context:
            context.prec = 64
            loads,old_action,sources = restore_case(evidence,digests,'MTS-primary',args.level,deadline)
            coordinates = loads.coordinates.copy()
            coordinates[:,:-1] = np.einsum('nlb,b->nl',basis,decimal_values(coefficients)).T
        packet_path = evidence.root/sources['packet']
        evidence.own(packet_path)
        packet = json.loads(packet_path.read_text())
        evidence.check('source_and_rates_unchanged',np.array_equal(coordinates[:,-1],loads.coordinates[:,-1]))
        state_path = evidence.output/'trial-initial-data.npz'
        np.savez_compressed(state_path,coordinates=np.asarray(coordinates,str),rates=loads.rates,coefficients=coefficients,
            parent_search=np.array(str(search_path.relative_to(evidence.root))))
        evidence.own(state_path,'outputs')
        evidence.report.update(level=args.level,branch='MTS-primary',selected_size=10,
            candidate_selection='Largest predeclared trial family; not selected by withheld tests.',
            frozen_root=candidate['frozen_root'],exploratory_nonroot_feedback_probe=True,github_action=False,subagents_used=False,
            progress=dict(stage='fresh live radial solve',seconds=perf_counter()-started))
        evidence.save()
        print(json.dumps(evidence.report['progress']),flush=True)
        new_loads,action = live_refined(old_action.owner,coordinates,loads.rates,packet['mesh'],packet,'primary',deadline)
        solver,solution = action.solver,action.solution
        old_values = old_action.solver.values(old_action.solution,solver.nodes.ravel())[0].reshape(solution['state'].shape)
        old_residual = float(np.max(abs(solver.residual(old_values,'primary'))))
        new_residual = float(np.max(abs(solver.residual(solution['state'],'primary'))))
        metric = 1-2*solution['state'][0]/solver.nodes
        clock_square = np.exp(2*solution['state'][1])-solver.fields['velocity'].reshape(solver.nodes.shape)**2/metric
        evidence.check('fresh_radial_constraint',new_residual<8e-14,new_residual)
        evidence.check('untrapped_timelike_chart',np.min(metric)>0 and np.min(clock_square)>0,
            dict(minimum_F=float(np.min(metric)),minimum_clock_square=float(np.min(clock_square))))
        metric_path = evidence.output/'fresh-metric.npz'
        np.savez_compressed(metric_path,edges=solver.edges,centers=solver.centers,lengths=solver.lengths,
            coordinates=np.asarray(coordinates,str),rates=loads.rates,**solution)
        evidence.own(metric_path,'outputs')
        frozen = CommonCoordinateAction(action.owner,coordinates,loads.rates,packet['mesh'],new_loads,old_action.solver,old_action.solution,64)
        result = []
        for name,selected,order in [('frozen_replay',frozen,48),('live_low',action,32),('live_high',action,48)]:
            labels,weights,layers,total = force(selected,order)
            path = evidence.output/(name+'.npz')
            np.savez_compressed(path,labels=labels,weights=weights,layers=layers,total=total)
            evidence.own(path,'outputs')
            result.append(dict(name=name,path=str(path.relative_to(evidence.root)),force=total.tolist()))
            evidence.report['progress'] = dict(stage=name,seconds=perf_counter()-started)
            evidence.save()
            print(json.dumps(evidence.report['progress']),flush=True)
        predicted = np.array(candidate['best']['unscaled_forces'])
        replay = np.array(result[0]['force'])
        error = float(np.max(abs(replay-predicted)))
        evidence.check('independent_candidate_force_replay',error<2e-18,error)
        low,high = np.array(result[1]['force']),np.array(result[2]['force'])
        evidence.report.update(seconds=perf_counter()-started,results=result,
            old_metric_residual_on_new_field=old_residual,fresh_metric_residual=new_residual,
            maximum_mass_change=float(np.max(abs(solution['state'][0]-old_values[0]))),
            maximum_log_lapse_change=float(np.max(abs(solution['state'][1]-old_values[1]))),
            live_force_change=(high-replay).tolist(),force_quadrature_difference=(high-low).tolist(),
            live_maximum_force=float(np.max(abs(high))),frozen_maximum_force=float(np.max(abs(replay))),
            source_equations_evolved=False,source_initial_configuration_preserved=True,
            full_constrained_equilibrium_solved=False,physical_evolution_performed=False)
        evidence.complete()
    except Exception as error:
        evidence.fail(error)
        raise


if __name__=='__main__':
    main()


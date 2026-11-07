from annular_C0_transport_context_20260930 import restore
from annular_candidate_coordinate_covectors_20260921 import local_polynomials
from annular_physical_native_kernel_20260928 import decimals
from annular_candidate_energy_current_20260921 import reconstructed_solver
from annular_wave_flux_form_v2_20260929 import PolynomialTrace
import hashlib
import json
import numpy as np


def restore_velocity(evidence,branch,deadline):
    path = evidence.output.parent/'annular-matter-gravity-stage-integrity-20261001.json'
    evidence.own(path)
    seal = json.loads(path.read_text())
    evidence.check('latest_complete_parent',seal['state']=='complete' and not seal['mismatches'])
    for relative,expected in seal['hashes'].items():
        source = (evidence.root/relative).resolve()
        if not source.is_relative_to(evidence.root) or hashlib.sha256(source.read_bytes()).hexdigest()!=expected:
            raise RuntimeError('Changed C1 parent '+relative)
    restored = restore(evidence,branch,'third',deadline)
    evaluator,read,report = [restored[name] for name in ['evaluator','read','report']]
    match = lambda parent:next(row for row in parent['cases'] if row['branch']==branch and row['level']=='third')
    live = match(report('annular-live-support-acceleration-attempt01'))
    reacted = match(report('annular-old-field-reaction-attempt01'))
    reaction = read(reacted['paths']['reaction'])
    evaluator.polynomials['acceleration_change'] = local_polynomials(evaluator.action.mesh,decimals(reaction['acceleration_change'][:,:-1].T))[0]
    evaluator.reaction = reaction['acceleration_change'][:,-1]
    instant = PolynomialTrace(*reconstructed_solver(read(live['paths']['live_response'])),evaluator.anchor)
    changed_time = PolynomialTrace(*reconstructed_solver(read(reacted['paths']['corrected_metric_time'])),evaluator.anchor)
    restored.update(instant=instant,changed_time=changed_time,live=live,reacted=reacted,reaction=reaction)
    return restored


def metric_packet(restored,offsets):
    evaluator = restored['evaluator']
    values,unused,radial,unused2 = evaluator.metric.evaluate(offsets,evaluator.metric.cells(offsets))
    time = sum(item.evaluate(offsets,item.cells(offsets))[0] for item in evaluator.time_traces)
    instant = restored['instant']
    change,unused,change_r,unused2 = instant.evaluate(offsets,instant.cells(offsets))
    changed_time = restored['changed_time']
    change_t = changed_time.evaluate(offsets,changed_time.cells(offsets))[0]
    return values,radial,time,change,change_r,change_t

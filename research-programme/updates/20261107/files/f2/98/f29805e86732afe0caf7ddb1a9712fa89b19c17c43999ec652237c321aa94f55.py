from integrate_annular_C0_higher_grid_20260930 import material_rows
from annular_C0_force_product_rule_20260930 import force_packet, analytic_force
from annular_C0_material_integral_v3_20260930 import metric_traces, base_kinematics, decimal_density
from annular_source_centered_quadrature_20260929 import CenteredLabelDensity
from decimal import Decimal
import os
import numpy as np


def restore_totals(path, order, totals, corrections):
    with np.load(path, allow_pickle=False) as saved:
        if bool(saved['complete']) or int(saved['order']) != order:
            raise ValueError('Wrong order or completed partial')
        phase, next_index = str(saved['phase']), int(saved['next_index'])
        if phase not in ['volume', 'traces', 'radial-cuts'] or next_index < 0:
            raise ValueError('Invalid partial phase/index')
        if phase == 'volume' and next_index % 16:
            raise ValueError('Partial is not at a quadrature block boundary')
        for name in totals:
            for prefix, target in [('total_', totals), ('correction_', corrections)]:
                value = saved[prefix+name]
                if value.shape != target[name].shape or not np.isfinite(value).all():
                    raise ValueError('Invalid partial accumulator '+prefix+name)
                target[name] = value.copy()
    if phase != 'volume':
        totals['atoms'].fill(0.)
        corrections['atoms'].fill(0.)
    return phase, next_index


def integrate_wave(evaluator, metric_time, order, evidence, progress, save, resume=None):
    totals = {name:np.zeros(size) for name, size in [('base',4), ('volume',4), ('atoms',4), ('force',1)]}
    corrections = {name:np.zeros_like(value) for name, value in totals.items()}

    phase, next_index = 'volume', 0
    if resume is not None:
        phase, next_index = restore_totals(resume, order, totals, corrections)

    def deposit(name, block):
        updated = totals[name]+block
        corrections[name] += np.where(abs(totals[name]) >= abs(block), (totals[name]-updated)+block, (block-updated)+totals[name])
        totals[name] = updated

    def checkpoint(phase, index):
        path = evidence.output/('partial-wave-'+str(order)+'.npz')
        temporary = path.with_suffix('.npz.tmp')
        with temporary.open('wb') as stream:
            np.savez_compressed(stream, **{'total_'+name:value for name,value in totals.items()},
                **{'correction_'+name:value for name,value in corrections.items()},
                phase=phase, next_index=index, order=order, complete=False)
            stream.flush()
            os.fsync(stream.fileno())
        temporary.replace(path)
        progress('wave'+str(order)+':'+phase+':'+str(index))

    endpoints = np.concatenate([evaluator.geometry.geometry(evaluator.edges, label)[0] for label in [-.5,.5]])
    cuts = np.unique(np.r_[evaluator.radial_cuts,endpoints])
    points, weights = np.polynomial.legendre.leggauss(order)
    lengths = np.diff(cuts)
    radii = (cuts[:-1,None]+lengths[:,None]*(points+1)/2).ravel()
    measures = (lengths[:,None]*weights/2).ravel()
    if phase == 'volume' and next_index > len(radii):
        raise ValueError('Partial index exceeds regenerated quadrature')
    first_index = next_index if phase == 'volume' else len(radii)
    for start in range(first_index,len(radii),16):
        if start % 2048 == 0:
            checkpoint('volume',start)
        section = slice(start,start+16)
        density = CenteredLabelDensity(evaluator.action,radii[section],order+4)
        offsets = radii[section][density.indices]
        packet, active = evaluator.packet(density.offsets,offsets)
        rows = material_rows(evaluator,packet,offsets)
        measure = measures[section][density.indices]*density.label_weights*active
        deposit('base',rows.real@measure)
        deposit('volume',(rows.imag/1e-25)@measure)
        deposit('force',np.array([analytic_force(*force_packet(evaluator,packet,offsets))@measure]))
    checkpoint('traces',0)
    base_traces = metric_traces(evaluator.action.solver,evaluator.action.solution,evaluator.radial_cuts,evaluator.anchor)
    time_traces = sum(metric_traces(item.solver,item.solution,evaluator.radial_cuts,evaluator.anchor)[:,0]
        for item in getattr(metric_time,'responses',(metric_time,)))
    absolute_atoms = np.zeros(4)
    for start in range(0,len(evaluator.radial_cuts),8):
        if start % 256 == 0:
            checkpoint('radial-cuts',start)
        section = slice(start,start+8)
        density = CenteredLabelDensity(evaluator.action,evaluator.radial_cuts[section],order+4)
        offsets = evaluator.radial_cuts[section][density.indices]
        packet, active = evaluator.packet(density.offsets,offsets)
        columns = np.arange(len(evaluator.radial_cuts))[section][density.indices]
        kinematics = base_kinematics(packet,evaluator.anchor+offsets)
        radius = np.array([Decimal.from_float(evaluator.anchor)+Decimal.from_float(float(value)) for value in offsets],dtype=object)
        traces = [decimal_density(kinematics,radius,base_traces[side,0][:,columns],
            base_traces[side,1][:,columns],time_traces[side][:,columns]) for side in [0,1]]
        jump = np.asarray(traces[1]-traces[0],float)
        movement = packet['movement_left']+(packet['movement_right']-packet['movement_left'])*packet['local']
        measure = density.label_weights*movement*active
        deposit('atoms',jump@measure)
        absolute_atoms += abs(jump)@abs(measure)
    result = {name:totals[name]+corrections[name] for name in totals}
    result.update(complete=result['volume']+result['atoms'],absolute_atoms=absolute_atoms,
        force_difference=result['force'][0]-result['volume'][0],quadrature=np.array([order,order+4,len(radii)]))
    path = save('wave-'+str(order),**result)
    return result,path



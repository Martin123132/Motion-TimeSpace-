from derive_annular_source_gravity_20260914 import EvidenceRun
from annular_C0_transport_context_20260930 import restore
from annular_C0_transport_identity_20260930 import identity_rows
from annular_C0_decimal_transport_20260930 import eulerian_density, material_density
from mpmath import mp
from decimal import localcontext
from time import perf_counter
import ctypes
import json
import numpy as np


def converted(values):
    array = np.asarray(values)
    return np.array([mp.mpf(float(value)) for value in array.ravel()], dtype=object).reshape(array.shape)


def precise_probe(evaluator, packet, offsets):
    values, value_r, radial, radial_r = [converted(item) for item in evaluator.metric.evaluate(offsets, evaluator.metric.cells(offsets))]
    positions = [item.evaluate(offsets, item.cells(offsets)) for item in evaluator.responses]
    times = [item.evaluate(offsets, item.cells(offsets)) for item in evaluator.time_traces]
    time, time_r = converted(sum(row[0] for row in times)), converted(sum(row[1] for row in times))
    mixed = converted(sum(item.evaluate(offsets, item.cells(offsets))[0] for item in evaluator.mixed_traces))
    position, position_r = converted(sum(row[0] for row in positions)), converted(sum(row[2] for row in positions))
    radius = converted(evaluator.anchor+offsets)
    data = {key:converted(value) for key,value in packet.items()}
    movement = data['movement_left']+(data['movement_right']-data['movement_left'])*data['local']
    dilation = (data['movement_right']-data['movement_left'])/data['width']
    results = []
    for step in [mp.mpf('1e-24'),mp.mpf('1e-28')]:
        pairs = []
        for sign in [-1,1]:
            amount = sign*step
            euler = eulerian_density(data,radius,values+amount*position,radial+amount*position_r,time+amount*mixed,amount)
            material = material_density(data,radius+amount*movement,values+amount*(position+value_r*movement),
                radial+amount*(position_r+radial_r*movement),time+amount*(mixed+time_r*movement),amount)*(1+amount*dilation)
            shifted = dict(data,local=data['local']+amount/data['width'])
            transport = material_density(shifted,radius+amount,values+amount*value_r,radial+amount*radial_r,time+amount*time_r)
            pairs.append(np.array([euler,material,(movement+amount*dilation)*transport]))
        result = (pairs[1]-pairs[0])/(2*step)
        defect = result[1]-result[0]-result[2]
        scale = np.maximum.reduce([abs(result[0]),abs(result[1]),abs(result[2])])
        relative = float(np.max(abs(defect)/np.maximum(scale,mp.mpf('1e-100'))))
        results.append(dict(result=np.asarray(result,float),defect=np.asarray(defect,float),relative=relative))
    return results


def main():
    kernel = ctypes.windll.kernel32
    kernel.GetCurrentProcess.restype = ctypes.c_void_p
    kernel.SetProcessAffinityMask.argtypes = [ctypes.c_void_p, ctypes.c_size_t]
    if not kernel.SetProcessAffinityMask(kernel.GetCurrentProcess(),4):
        raise OSError('Cannot set one core')
    evidence = EvidenceRun('annular-C0-precise-transport-probe-attempt01',__file__)
    started,deadline=perf_counter(),perf_counter()+1600
    try:
        mp.dps=96
        with localcontext() as context:
            context.prec=70
            for branch in ['reference-reference','MTS-primary']:
                evaluator=restore(evidence,branch,'fine',deadline)['evaluator']
                cells=np.unique(np.linspace(0,len(evaluator.widths)-1,37).astype(int))
                indices=np.repeat(cells,9)
                labels=np.tile(np.repeat([-.37,.03,.29],3),len(cells))
                local=np.tile([.13,.47,.83],3*len(cells))
                left=evaluator.geometry.geometry(evaluator.edges[indices],labels)[0]
                right=evaluator.geometry.geometry(evaluator.edges[indices+1],labels)[0]
                offsets=left+(right-left)*local
                packet,active=evaluator.packet(labels,offsets)
                binary=identity_rows(evaluator,packet,offsets)
                scale=np.maximum.reduce([abs(binary['material']),abs(binary['eulerian']),abs(binary['transport'])])
                relative=abs(binary['defect'])/np.maximum(scale,1e-100)
                selected=np.unique(np.r_[np.linspace(0,len(offsets)-1,12).astype(int),np.argmax(relative,axis=1),
                    np.argmax(abs(binary['defect']),axis=1)])
                selected_packet={key:value[selected] for key,value in packet.items()}
                precise=precise_probe(evaluator,selected_packet,offsets[selected])
                path=evidence.output/(branch+'-precise.npz')
                np.savez_compressed(path,**binary,selected=selected,offsets=offsets,labels=labels,
                    precise_derivatives=precise[-1]['result'],precise_defect=precise[-1]['defect'])
                evidence.own(path,'outputs')
                evidence.check(branch+':active',active.all())
                evidence.check(branch+':96digit_transport',precise[-1]['relative']<1e-40,precise[-1]['relative'])
                evidence.check(branch+':step_stability',np.array_equal(precise[0]['result'],precise[1]['result']))
                differences=np.array([binary[name][:,selected] for name in ['eulerian','material','transport']])-precise[-1]['result']
                summary=dict(branch=branch,points=len(offsets),precise_points=len(selected),
                    binary_relative_error=float(np.max(relative)),binary_pointwise_1e10_gate_passed=bool(np.max(relative)<1e-10),
                    precise_relative_error=precise[-1]['relative'],binary_arithmetic_error=np.max(abs(differences),axis=2).tolist(),
                    wrong_sign_scale=float(np.max(abs(binary['wrong_sign']))),valid_for_claim=False)
                evidence.report['cases'].append(summary)
                evidence.save()
                print(json.dumps(summary),flush=True)
        evidence.report.update(seconds=perf_counter()-started,github_action=False,actual_integral_repeated=False)
        evidence.complete()
    except Exception as error:
        evidence.fail(error)
        raise


if __name__=='__main__':
    main()

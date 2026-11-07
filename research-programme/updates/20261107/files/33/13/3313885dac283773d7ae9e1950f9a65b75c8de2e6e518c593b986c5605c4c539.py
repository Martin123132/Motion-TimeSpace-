from decimal import Decimal,localcontext
from pathlib import Path
import hashlib
import json
import numpy as np
from scipy.sparse import load_npz


def verify_report(evidence,relative):
    path = evidence.root/relative
    report = json.loads(path.read_text(encoding='utf-8'))
    evidence.own(path)
    mismatches = []
    for category in ['inputs','outputs']:
        for name,expected in report[category].items():
            owned = (evidence.root/name).resolve()
            if not owned.is_relative_to(evidence.root) or not owned.is_file():
                mismatches.append(name)
            elif hashlib.sha256(owned.read_bytes()).hexdigest()!=expected:
                mismatches.append(name)
            else:
                evidence.own(owned)
    evidence.check(relative+':source_hashes',not mismatches,mismatches)
    evidence.check(relative+':prior_checks',bool(report['checks']) and all(row['passed'] for row in report['checks']))
    return report


def validate_result(evidence,result,prefix):
    with np.load(evidence.root/result['acceleration_path'],allow_pickle=False) as archive:
        data = {name:archive[name].copy() for name in archive.files}
    with np.load(evidence.root/result['gate_path'],allow_pickle=False) as archive:
        gates = {name:archive[name].copy() for name in archive.files}
    matrix = load_npz(evidence.root/result['matrix_path']).tocsr()
    for category,arrays in [('acceleration',data),('gates',gates)]:
        evidence.check(prefix+':finite_'+category,all(np.all(np.isfinite(value)) for value in arrays.values() if value.dtype.kind in 'fc'))
    acceleration,force = data['acceleration'],data['force']
    evidence.check(prefix+':dimensions',acceleration.shape==force.shape and matrix.shape==(acceleration.size,acceleration.size)
        and gates['force_layers'].shape==(result['material'],13,4,4) and len(gates['labels'])==result['material'])
    evidence.check(prefix+':rates_zero',not np.any(data['rates']))
    defect = matrix-matrix.T
    symmetry = float(np.max(np.abs(defect.data),initial=0)/max(np.max(np.abs(matrix.data)),1e-30))
    evidence.check(prefix+':mass_symmetric',symmetry<2e-12,symmetry)
    residual = matrix@acceleration.ravel()-force.ravel()
    residual_relative = float(np.max(np.abs(residual))/max(np.max(np.abs(force)),1e-30))
    evidence.check(prefix+':replayed_Euler_residual',residual_relative<2e-10,residual_relative)
    evidence.check(prefix+':stored_residual_matches',np.max(np.abs(residual-data['residual'].ravel()))<2e-13*max(np.max(np.abs(force)),1e-30))
    selected = np.unique(np.r_[np.linspace(0,acceleration.size-1,33,dtype=int),
        np.arange(acceleration.shape[0])*acceleration.shape[1]+acceleration.shape[1]-1])
    decimal_maximum = Decimal(0)
    with localcontext() as context:
        context.prec = 64
        for row in selected:
            start,stop = matrix.indptr[row:row+2]
            total = sum((Decimal.from_float(float(value))*Decimal.from_float(float(acceleration.ravel()[column]))
                for value,column in zip(matrix.data[start:stop],matrix.indices[start:stop])),Decimal(0))
            decimal_maximum = max(decimal_maximum,abs(total-Decimal.from_float(float(force.ravel()[row]))))
    decimal_relative = float(decimal_maximum)/max(float(np.max(np.abs(force))),1e-30)
    evidence.check(prefix+':independent_Decimal_rows',decimal_relative<2e-10,dict(rows=len(selected),relative=decimal_relative))
    difference = acceleration-data['edge_acceleration']-data['bulk_acceleration']
    evidence.check(prefix+':acceleration_split',np.max(np.abs(difference))<2e-13*max(np.max(np.abs(acceleration)),1e-30))
    integrated = np.einsum('layer,layerkij->kij',gates['weights'],gates['force_layers'])
    gate_scale = max(float(np.max(np.abs(integrated))),1e-30)
    evidence.check(prefix+':native_gate_integral',np.max(np.abs(integrated-gates['forms']))<2e-13*gate_scale)
    evidence.check(prefix+':gate_symmetry',np.max(np.abs(integrated-integrated.transpose(0,2,1)))<2e-13*gate_scale)
    evidence.check(prefix+':quartic_factor_six',np.max(np.abs(gates['fourth_derivative']-6*integrated[:,0,0]))<2e-13*gate_scale)
    evidence.check(prefix+':quartic_coefficient_quarter',np.max(np.abs(gates['full_coefficient']-integrated[:,0,0]/4))<2e-13*gate_scale)
    evidence.check(prefix+':gate_summary',np.max(np.abs(np.asarray(result['full_gate'])-integrated[:,0,0]))<2e-13*gate_scale)
    decomposition = integrated[:,0,0]-integrated[:,1,1]-integrated[:,2,2]-2*integrated[:,1,2]
    evidence.check(prefix+':gate_split_cross_term',np.max(np.abs(decomposition))<2e-10*gate_scale)
    evidence.check(prefix+':positive_material_weights',np.all(gates['weights']>0) and abs(np.sum(gates['weights'])-1)<2e-13)
    return dict(acceleration=acceleration,gate=integrated[:,0,0],decimal_relative=decimal_relative,
        residual_relative=residual_relative,source_acceleration=gates['source_acceleration'],
        labels=gates['labels'],normal_max=gates['normal_max'])


def compare_orders(low,high):
    difference = high['acceleration']-low['acceleration']
    gate_difference = high['gate']-low['gate']
    return dict(quadrature_acceleration_maximum_difference=float(np.max(np.abs(difference))),
        quadrature_gate_maximum_difference=float(np.max(np.abs(gate_difference))),
        quadrature_gate_relative_difference=float(np.max(np.abs(gate_difference))/max(np.max(np.abs(high['gate'])),1e-30)))


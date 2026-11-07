from derive_annular_source_gravity_20260914 import EvidenceRun
from annular_common_weighted_moments_20260920 import apply_rational_rows
from annular_horizontal_clock_evolution_20260913 import ChebyshevRule
from decimal import Decimal, localcontext
from fractions import Fraction
from pathlib import Path
import hashlib
import json
import numpy as np
import sympy as sp


def exact(value):
    if isinstance(value, Decimal):
        return value
    if isinstance(value, (str,np.str_)):
        return Decimal(str(value))
    return Decimal.from_float(float(value))


def converted(values):
    values = np.asarray(values)
    return np.array([exact(value) for value in values.ravel()],dtype=object).reshape(values.shape)


def rational(value):
    value = Fraction(value)
    return Decimal(value.numerator)/Decimal(value.denominator)


def sample(mesh, values, cell, local, cardinal):
    nodes = [values[:,index] if index>=0 else np.full(len(cardinal),Decimal(0),dtype=object)
        for index in mesh['elements'][cell]]
    width = rational(Fraction(mesh['edges'][cell+1])-Fraction(mesh['edges'][cell]))
    interpolated = nodes[0]*(1-local)*(1-2*local)+4*nodes[1]*local*(1-local)+nodes[2]*local*(2*local-1)
    gradient = (nodes[0]*(4*local-3)+nodes[1]*(4-8*local)+nodes[2]*(4*local-1))/width
    return sum(interpolated*cardinal),sum(gradient*cardinal)


def main():
    evidence = EvidenceRun('annular-common-jet-transfer-validation-attempt01',__file__)
    hashes = {}
    try:
        seal_path = evidence.output.parent/'annular-C1-integrated-stage-integrity-20261001.json'
        seal = json.loads(seal_path.read_text())
        evidence.own(seal_path)
        for relative,expected in seal['hashes'].items():
            path = (evidence.root/relative).resolve()
            if not path.is_relative_to(evidence.root) or hashlib.sha256(path.read_bytes()).hexdigest()!=expected:
                raise RuntimeError('Changed ancestor '+relative)
            hashes[str(path.relative_to(evidence.root))] = expected

        def read(relative):
            path = (evidence.root/relative).resolve()
            key = str(path.relative_to(evidence.root))
            if key not in hashes or hashlib.sha256(path.read_bytes()).hexdigest()!=hashes[key]:
                raise RuntimeError('Unowned transfer source '+relative)
            evidence.own(path)
            if path.suffix=='.json':
                return json.loads(path.read_text())
            with np.load(path,allow_pickle=False) as saved:
                return {name:saved[name].copy() for name in saved.files}

        reports = {}
        for short in ['reference','MTS']:
            path = evidence.output.parent/('annular-common-physical-jet-'+short+'-attempt02')/'status.json'
            data = json.loads(path.read_text())
            evidence.own(path)
            evidence.check(short+':probe_complete',data['state']=='complete' and all(row['passed'] for row in data['checks']))
            for category in ['inputs','outputs']:
                for relative,expected in data[category].items():
                    source = (evidence.root/relative).resolve()
                    if not source.is_relative_to(evidence.root) or hashlib.sha256(source.read_bytes()).hexdigest()!=expected:
                        raise RuntimeError('Changed complete probe '+relative)
                    hashes[str(source.relative_to(evidence.root))] = expected
            reports[short] = data
        normalizations = [data['rule_outputs'][-1]['summary']['geometric_RMS'] for data in reports.values()]
        evidence.check('same_geometric_normalization_both_branches',normalizations[0]==normalizations[1],normalizations)
        frozen_normalization = normalizations[0]
        scale,rate,acceleration = sp.symbols('N Ndot Nddot',nonzero=True)
        jet = sp.Matrix(sp.symbols('s u a'))
        transformation = sp.Matrix([[scale,0,0],[rate,scale,0],[acceleration,2*rate,scale]])
        evidence.check('time_dependent_normalization_requires_triangular_jet',
            (transformation.inv()*transformation).applyfunc(sp.simplify)==sp.eye(3))
        evidence.check('constant_normalization_is_special_case',
            transformation.subs({rate:0,acceleration:0})==scale*sp.eye(3))
        evidence.report.update(frozen_normalization=frozen_normalization,normalization_frozen_at_base_state=True,
            variable_normalization_not_used=True,github_action=False,subagents_used=False)
        live = read(str((evidence.output.parent/'annular-live-support-acceleration-attempt01/status.json').relative_to(evidence.root)))
        with localcontext() as context:
            context.prec = 90
            inverse = converted(ChebyshevRule(14).inverse)
            for short,branch in [('reference','reference-reference'),('MTS','MTS-primary')]:
                cases = {level:next(row for row in live['cases'] if row['branch']==branch and row['level']==level) for level in ['fine','third']}
                packets = {level:read(case['sources']['packet']) for level,case in cases.items()}
                states = {level:read(case['sources']['state']) for level,case in cases.items()}
                fields = {level:converted(state['coordinates'][:,:-1]) for level,state in states.items()}
                raw = read(cases['fine']['direction_path'])
                correction = read(cases['fine']['paths']['projection'])['correction']
                direction = converted(raw['field_vertices'])-converted(correction[:,:-1])
                edge = converted(raw['edge_vertices'])
                source_direction = -converted(correction[:,-1])
                transferred = read(reports[short]['transfer_path'])
                target_direction = converted(transferred['field_vertices_exact'])-converted(transferred['correction_exact'][:,:-1])
                target_edge = converted(transferred['edge_vertices_exact'])
                same_field = apply_rational_rows(packets['third']['prolongation'],fields['fine'].T).T
                lower,upper,anchor = [rational(value) for value in [packets['fine']['mesh']['edges'][0],
                    packets['fine']['mesh']['edges'][-1],packets['fine']['mesh']['anchor']]]
                width = Decimal.from_float(2e-5)
                evidence.check(short+':source_positions_shared',np.array_equal(states['fine']['coordinates'][:,-1],states['third']['coordinates'][:,-1]))
                rows = []
                for index,cell in enumerate(np.linspace(0,len(packets['third']['mesh']['elements'])-1,48).astype(int)):
                    local = rational([Fraction(1,7),Fraction(2,5),Fraction(7,8)][index%3])
                    label = rational([Fraction(-2,5),Fraction(-1,7),Fraction(1,9),Fraction(3,7)][index%4])
                    chebyshev = [Decimal(1),2*label]
                    for degree in range(2,15):
                        chebyshev.append(4*label*chebyshev[-1]-chebyshev[-2])
                    cardinal = np.array(chebyshev,dtype=object)@inverse
                    source = sum(converted(states['fine']['coordinates'][:,-1])*cardinal)
                    point = rational(packets['third']['mesh']['edges'][cell])
                    point += local*rational(Fraction(packets['third']['mesh']['edges'][cell+1])-Fraction(packets['third']['mesh']['edges'][cell]))
                    displacement = (point-lower)/(anchor-lower) if point<anchor else (upper-point)/(upper-anchor)
                    jacobian = (source-lower-width*label)/(anchor-lower) if point<anchor else (upper+width*label-source)/(upper-anchor)
                    parent_local = (Decimal(int(cell%2))+local)/2
                    field_f = sample(packets['fine']['mesh'],direction,cell//2,parent_local,cardinal)[0]
                    field_t = sample(packets['third']['mesh'],target_direction,cell,local,cardinal)[0]
                    gradient_f = sample(packets['fine']['mesh'],fields['fine'],cell//2,parent_local,cardinal)[1]/jacobian
                    gradient_t = sample(packets['third']['mesh'],fields['third'],cell,local,cardinal)[1]/jacobian
                    gradient_same = sample(packets['third']['mesh'],same_field,cell,local,cardinal)[1]/jacobian
                    motion_f = sum((edge[:,cell//2]*(1-parent_local)+edge[:,cell//2+1]*parent_local)*cardinal)
                    motion_t = sum((target_edge[:,cell]*(1-local)+target_edge[:,cell+1]*local)*cardinal)
                    speed_change = sum(source_direction*cardinal)
                    motion_f += displacement*speed_change
                    motion_t += displacement*speed_change
                    residual_f = field_f-motion_f*gradient_f
                    residual_t = field_t-motion_t*gradient_t
                    residual_same = field_t-motion_t*gradient_same
                    background = -motion_f*(gradient_t-gradient_f)
                    commutator = (field_t-field_f)-(motion_t-motion_f)*gradient_t
                    rows.append([field_t-field_f,motion_t-motion_f,gradient_same-gradient_f,
                        residual_same-residual_f,residual_t-residual_f,background,commutator,
                        residual_t-residual_f-background-commutator])
                values = np.array(rows,dtype=object)
                maxima = np.array([max(map(abs,values[:,column])) for column in range(values.shape[1])],dtype=object)
                evidence.check(short+':actual_P2_P1_transfer',max(maxima[:4])<Decimal('1e-65'),list(map(str,maxima[:4])))
                evidence.check(short+':actual_background_separation',maxima[-1]<Decimal('1e-65'),str(maxima[-1]))
                evidence.check(short+':resampled_background_not_ignored',maxima[5]>Decimal('1e-25'),str(maxima[5]))
                output = evidence.output/(short+'-exact-transfer.npz')
                np.savez_compressed(output,values=np.asarray(values,str),maxima=np.asarray(maxima,str),
                    columns=np.array(['delta_field','delta_map','prolonged_gradient_difference','same_background_e_difference',
                        'resampled_e_difference','background_gradient_term','transfer_commutator','identity_error']))
                evidence.own(output,'outputs')
                evidence.report['cases'].append(dict(branch=branch,points=len(rows),maximum_errors=list(map(str,maxima)),
                    path=str(output.relative_to(evidence.root)),transported_direction_not_reprojected=True))
                evidence.save()
        assembly = read(str((evidence.output.parent/'annular-C1-integrated-assembly-attempt01/status.json').relative_to(evidence.root)))
        rational_scale = Fraction.from_float(frozen_normalization)
        witnesses = 0
        for item in assembly['summaries']:
            data = read(item['path'])
            for orthant in data['envelope_search']['orthants']:
                witness = orthant['exact_witness']
                if witness is None:
                    continue
                amplitude = [orthant['signs'][column]*Fraction(int(witness['numerator'][column]),int(witness['denominator'])) for column in range(3)]
                normalized_amplitude = [rational_scale*value for value in amplitude]
                for row in range(4):
                    row_scale = 1/rational_scale if row==0 else Fraction(1)
                    baseline = Fraction.from_float(data['baseline'][row])
                    coefficients = [Fraction.from_float(value) for value in data['columns'][row]]
                    residual = baseline+sum(value*part for value,part in zip(coefficients,amplitude))
                    normalized = row_scale*baseline+sum(row_scale*value/rational_scale*part
                        for value,part in zip(coefficients,normalized_amplitude))
                    budget = Fraction.from_float(data['baseline_error'][row])+sum(
                        Fraction.from_float(value)*abs(part) for value,part in zip(data['column_error'][row],amplitude))
                    if normalized!=row_scale*residual or abs(normalized)>row_scale*budget:
                        raise RuntimeError('Normalization altered compatibility')
                witnesses += 1
        evidence.check('all_46_witnesses_exactly_preserved_by_fixed_normalization',witnesses==46,witnesses)
        evidence.report.update(exact_witnesses_normalized=witnesses,normalization_is_not_new_physics=True,
            common_field_transfer_verified=True,finite_evolution_performed=False)
        evidence.complete()
    except Exception as error:
        evidence.fail(error)
        raise


if __name__=='__main__':
    main()

from derive_annular_source_gravity_20260914 import EvidenceRun
from annular_anchored_projector_chart_20260916 import AnchoredProjectorChart, jet_pullback, omission_diagnostic, split_frame
from annular_locally_refined_source_action_20260916 import LocallyRefinedSourceAction
from run_annular_source_fitted_crossing_20260915 import initial
from scipy.linalg import expm
import numpy as np
import json
import time


def relative(actual, expected):
    return float(np.linalg.norm(actual-expected)/max(1., np.linalg.norm(expected)))


def main():
    evidence = EvidenceRun('annular-anchored-chart-qualification-attempt01', __file__)
    try:
        path = evidence.root/'source-intake/navier-stokes/20260914/annular-force-aware-modes-attempt01/status.json'
        evidence.own(path)
        selection = json.loads(path.read_text())
        evidence.check('inherited_selection_complete', selection['state']=='complete')
        for base_count, splits, background in [(33,2,0.), (33,2,.7), (129,8,0.)]:
            for gram in [False, True]:
                system = LocallyRefinedSourceAction(base_count, gram, background_mass=background, source_splits=splits)
                branch = 'MTS' if gram else 'reference'
                chosen = (next(row for row in selection['cases'] if row['branch']==branch)['retained_indices']
                    if base_count==129 else list(range(int(.8*system.count))))
                chart = AnchoredProjectorChart(system, chosen)
                for position in [system.anchor, system.anchor+.0003]:
                    started = time.monotonic()
                    label = '-'.join(map(str,[branch,base_count,background,position]))
                    data = chart.at(position)
                    basis, first, second = data['basis'], data['basis_b'], data['basis_bb']
                    mass, mass_b, mass_bb = data['matrices']['mass'], data['first']['mass'], data['second']['mass']
                    norm_first = first.T @ mass @ basis+basis.T @ mass_b @ basis+basis.T @ mass @ first
                    norm_second = second.T @ mass @ basis+basis.T @ mass @ second+2*first.T @ mass @ first
                    norm_second += 2*first.T @ mass_b @ basis+2*basis.T @ mass_b @ first+basis.T @ mass_bb @ basis
                    evidence.check(label+'_mass_normalization', relative(basis.T @ mass @ basis,np.eye(chart.count))<2e-10)
                    evidence.check(label+'_first_normalization', np.linalg.norm(norm_first)<2e-7, float(np.linalg.norm(norm_first)))
                    evidence.check(label+'_second_normalization', np.linalg.norm(norm_second)<2e-5, float(np.linalg.norm(norm_second)))
                    evidence.check(label+'_invariant_retained_subspace', relative(data['matrices']['stiffness'] @ basis,
                        mass @ basis @ data['stiffness'])<2e-8)
                    controls = []
                    for step in [2e-4,1e-4,5e-5,2e-5,1e-5,5e-6]:
                        samples = [chart.at(position+multiple*step)['basis'] for multiple in [-2,-1,1,2]]
                        finite_first = (samples[0]-8*samples[1]+8*samples[2]-samples[3])/(12*step)
                        finite_second = (-samples[0]+16*samples[1]-30*basis+16*samples[2]-samples[3])/(12*step**2)
                        controls.append(dict(step=step, first_error=relative(finite_first,first), second_error=relative(finite_second,second)))
                        if len(controls)>=2 and all(row['first_error']<2e-4 and row['second_error']<3e-3 for row in controls[-2:]):
                            break
                    evidence.check(label+'_independent_first_and_second_chart_derivatives', len(controls)>=2 and
                        all(row['first_error']<2e-4 and row['second_error']<3e-3 for row in controls[-2:]), controls)
                    raw = initial(system)
                    prepared = chart.prepare(raw)
                    coordinates, rates = np.split(prepared[:-1],2)
                    coordinates[-1] = position
                    data = chart.at(position)
                    dynamics = chart.dynamics(coordinates,rates)
                    pulled = jet_pullback(chart,position,coordinates,rates)
                    old = pulled['original']
                    modal, velocity, speed = coordinates[:-1], rates[:-1], rates[-1]
                    momentum = np.append(velocity+speed*data['transport'] @ modal,
                        dynamics['material']['momentum']+velocity @ data['transport'] @ modal+speed*modal @ data['square'] @ modal)
                    action = velocity @ velocity/2+speed*velocity @ data['transport'] @ modal
                    action += speed**2*(modal @ data['square'] @ modal)/2-modal @ data['stiffness'] @ modal/2+dynamics['material']['action']
                    evidence.check(label+'_pulled_action_and_canonical_momenta', abs(float(action-pulled['action']))<2e-9
                        and relative(momentum,pulled['momenta'])<2e-9)
                    old_covector = np.append(old['scalar_covector'], system.source_covector(0.,pulled['physical_coordinates'],pulled['physical_rates']))
                    covector = np.append(data['basis'].T @ old_covector[:-1]+speed*data['basis_b'].T @ old['momenta'][:-1],
                        old_covector[-1]+old_covector[:-1] @ data['basis_b'] @ modal
                        +old['momenta'][:-1] @ (data['basis_b'] @ velocity+speed*data['basis_bb'] @ modal))
                    shifted = jet_pullback(chart,position,coordinates+1e-24j*rates,rates)
                    original_rhs = covector-shifted['momenta'].imag/1e-24
                    analytic_rhs = np.append(dynamics['field_rhs'],dynamics['source_rhs'])
                    evidence.check(label+'_independent_EL_right_hand_side', relative(analytic_rhs,original_rhs)<2e-8, relative(analytic_rhs,original_rhs))
                    direction = np.sin(np.arange(chart.count+1)+.4)
                    momentum_direction = jet_pullback(chart,position,coordinates,rates+1e-24j*direction)['momenta'].imag/1e-24
                    hessian_direction = np.append(direction[:-1]+dynamics['cross']*direction[-1],
                        dynamics['cross'] @ direction[:-1]+dynamics['inertia']*direction[-1])
                    evidence.check(label+'_independent_velocity_Hessian', relative(hessian_direction,momentum_direction)<2e-9)
                    omission = omission_diagnostic(chart,coordinates,rates)
                    evidence.check(label+'_same_state_omission_force_identity', abs(omission['same_state_force']-omission['same_state_force_predicted'])<2e-10
                        and abs(omission['same_state_force'])<=omission['same_state_force_bound']+2e-12, omission['same_state_force'])
                    evidence.check(label+'_exact_kinetic_defect_law', abs(omission['kinetic_defect_square']-omission['predicted_defect_square'])
                        <2e-9*max(1.,omission['predicted_defect_square']))
                    evidence.check(label+'_source_momentum_and_energy', abs(float(momentum @ rates-action
                        -system.energy(0.,pulled['physical_coordinates'],pulled['physical_rates'])))<2e-9)
                    evidence.report['cases'].append(dict(branch=branch,base_count=base_count,splits=splits,background_mass=background,
                        position=position,retained_count=chart.count,full_count=system.count,derivative_controls=controls,
                        minimum_gap=chart.minimum_gap,minimum_overlap=chart.minimum_overlap,
                        highest_frequency=float(np.sqrt(data['values'][-1])),EL_rhs_error=relative(analytic_rhs,original_rhs),
                        source_momentum_shift=omission['source_connection_momentum'],seconds=time.monotonic()-started))
                    evidence.save()
                    print(dict(case=label,retained=chart.count,seconds=time.monotonic()-started),flush=True)
                if base_count==33:
                    full_chart = AnchoredProjectorChart(system,list(range(system.count)))
                    prepared = full_chart.prepare(initial(system))
                    coordinates,rates = np.split(prepared[:-1],2)
                    acceleration = full_chart.dynamics(coordinates,rates)['acceleration']
                    physical,physical_rates,physical_acceleration = full_chart.lift(coordinates,rates,acceleration)
                    evidence.check(branch+str(background)+'_full_rank_coordinate_equivalence', relative(physical_acceleration,
                        system.acceleration(0.,physical,physical_rates))<2e-8)
        generator = np.zeros((4,4))
        generator[0,2],generator[2,0],generator[1,3],generator[3,1] = .3,-.3,.2,-.2
        for position in [-1e-4,0.,1e-4]:
            rotation = expm(position*generator)
            diagonal = np.diag([1+position,1-position,4+position,4-position])
            diagonal_b = np.diag([1.,-1.,1.,-1.])
            stiffness = rotation @ diagonal @ rotation.T
            stiffness_b = generator @ stiffness-stiffness @ generator+rotation @ diagonal_b @ rotation.T
            stiffness_bb = generator @ stiffness_b-stiffness_b @ generator
            stiffness_bb += generator @ rotation @ diagonal_b @ rotation.T-rotation @ diagonal_b @ rotation.T @ generator
            frame = split_frame(np.eye(4),stiffness,dict(mass=np.zeros((4,4)),stiffness=stiffness_b),
                dict(mass=np.zeros((4,4)),stiffness=stiffness_bb),[0,1],1e-4)
            selected,selected_b,selected_bb = [frame[name][:,:2] for name in ['vectors','vectors_b','vectors_bb']]
            projector = selected @ selected.T
            derivative = selected_b @ selected.T+selected @ selected_b.T
            curvature = selected_bb @ selected.T+2*selected_b @ selected_b.T+selected @ selected_bb.T
            expected_b = generator @ projector-projector @ generator
            expected_bb = generator @ expected_b-expected_b @ generator
            evidence.check('internal_crossing_'+str(position), relative(derivative,expected_b)<2e-10 and relative(curvature,expected_bb)<2e-10)
        rejected = False
        try:
            split_frame(np.eye(4),np.diag([1.,1.,4.,4.]),dict(mass=np.zeros((4,4)),stiffness=np.zeros((4,4))),
                dict(mass=np.zeros((4,4)),stiffness=np.zeros((4,4))),[0,2],1e-4)
        except ValueError as error:
            rejected = 'gap closed' in str(error)
        evidence.check('retained_omitted_exact_crossing_rejected',rejected)
        evidence.report.update(smooth_chart_implemented=True,source_momentum_connection_included=True,
            original_action_unmodified=True,internal_crossings_qualified=True,external_crossing_claim=False,
            derivative_checks_not_moving_evolution=True,physical_GR_gates_unchanged=True)
        evidence.complete()
    except Exception as error:
        evidence.fail(error)
        raise


if __name__=='__main__':
    main()

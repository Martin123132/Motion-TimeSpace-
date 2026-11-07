from derive_annular_source_gravity_20260914 import EvidenceRun
from annular_C1_response_context_20261001 import restore_velocity,metric_packet
from annular_C1_coefficient_response_20261001 import analytic_response,current_values,matter_gravity_response
from probe_annular_C0_precise_transport_20260930 import converted
from annular_C0_decimal_transport_20260930 import precise_exp,precise_sqrt
from decimal import localcontext
from time import perf_counter
from mpmath import mp
import json
import numpy as np
import sympy as sp


def symbolic(evidence):
    alpha,beta,alpha_r,beta_r,alpha_t,temporal,gradient,speed,speed_r,rate_r,acceleration,map_acceleration = sp.symbols('alpha beta alpha_r beta_r alpha_t T g W W_r v_r a Z')
    integral,weighted,weighted_r,profile = sp.symbols('I V V_r h')
    variables = [alpha,beta,alpha_r,beta_r,alpha_t,temporal,speed,speed_r,rate_r,acceleration,map_acceleration,weighted,weighted_r]
    changes = sp.symbols('da db da_r db_r da_t e w w_r d_r a_change Z_change V_change Vr_change')
    delta = lambda expression:sum(sp.diff(expression,value)*change for value,change in zip(variables,changes))
    grad_time = rate_r-speed_r*gradient
    temporal_time = acceleration-map_acceleration*gradient-speed*grad_time
    momentum = (alpha_t+speed*alpha_r+speed_r*alpha)*temporal+alpha*temporal_time
    flux = alpha*speed*temporal+beta*gradient
    energy = (alpha*temporal**2+beta*gradient**2)/2
    compact = speed*(beta_r*gradient**2-alpha_r*temporal**2)/2+beta*gradient*rate_r-speed_r*energy
    original_energy_time = ((alpha_t+speed*alpha_r)*temporal**2+(-beta*alpha_t/alpha+speed*beta_r)*gradient**2)/2
    original_energy_time += alpha*temporal*temporal_time+beta*gradient*grad_time
    original = -momentum*weighted-flux*weighted_r+(original_energy_time+(speed_r+alpha_t/alpha)*energy)*integral+energy*speed*profile
    derived = delta(momentum)*(temporal*integral-weighted)+momentum*(changes[5]*integral-changes[-2])
    derived -= delta(flux)*weighted_r+flux*changes[-1]
    derived += delta(compact)*integral+(delta(energy)*speed+energy*changes[6])*profile
    evidence.check('symbolic:complete_C1_product_rule',sp.expand(delta(original)-derived)==0)
    radius,lapse,geometry,clock,kappa,density,source_mass,velocity,time = sp.symbols('r N F ell k rho M v mt',positive=True)
    change_mass,change_nu,change_velocity,change_time = sp.symbols('dm dnu dv dmt')
    clock_squared = lapse*lapse-velocity**2/geometry
    clock_squared_change = sp.diff(clock_squared,lapse)*lapse*change_nu
    clock_squared_change += sp.diff(clock_squared,velocity)*change_velocity-sp.diff(clock_squared,geometry)*2*change_mass/radius
    clock_change = (lapse*lapse*change_nu-velocity*change_velocity/geometry-velocity**2*change_mass/(radius*geometry**2))/clock
    evidence.check('symbolic:proper_clock_response',sp.expand(clock_squared_change-2*clock*clock_change)==0)
    coefficient = lapse/(kappa*sp.sqrt(geometry))
    loading = kappa*source_mass*density*sp.sqrt(geometry)*lapse/clock
    log_coefficient = change_nu+change_mass/(radius*geometry)
    loading_change = loading*(-change_mass/(radius*geometry)+change_nu-clock_change/clock)
    raw_dust_change = source_mass*density*lapse*lapse*(change_velocity+2*velocity*change_nu)/clock
    raw_dust_change -= source_mass*density*lapse*lapse*velocity*clock_change/clock**2
    gravity_change = coefficient*(change_time+log_coefficient*time)
    combined = coefficient*(change_time+change_velocity*loading+velocity*loading_change
        +log_coefficient*(time+velocity*loading))
    evidence.check('symbolic:dust_gravity_response',sp.expand(gravity_change+raw_dust_change-combined)==0)


def main():
    evidence = EvidenceRun('annular-C1-coefficient-probe-attempt02',__file__)
    started,deadline = perf_counter(),perf_counter()+1800
    try:
        evidence.own(evidence.root/'DERIVATION-20261001-C1-coefficient-current-response.md')
        symbolic(evidence)
        mp.dps = 105
        with localcontext() as context:
            context.prec = 80
            for branch in ['reference-reference','MTS-primary']:
                restored = restore_velocity(evidence,branch,deadline)
                evaluator = restored['evaluator']
                cells = np.linspace(0,len(evaluator.widths)-1,96).astype(int)
                labels = np.tile([-.47,-.33,-.11,.03,.17,.29,.37,.47],12)
                local = np.tile([.13,.47,.83],32)
                lower = evaluator.geometry.geometry(evaluator.edges[cells],labels)[0]
                upper = evaluator.geometry.geometry(evaluator.edges[cells+1],labels)[0]
                offsets = lower+(upper-lower)*local
                packet,active = evaluator.packet(labels,offsets)
                arguments = [evaluator.anchor+offsets,*metric_packet(restored,offsets)]
                binary = analytic_response(packet,*arguments)
                old = current_values(packet,*arguments,amount=1e-25j,original=True).imag/1e-25
                compact_complex = current_values(packet,*arguments,amount=1e-25j).imag/1e-25
                data = {key:converted(value) for key,value in packet.items()}
                exact_arguments = [converted(value) for value in arguments]
                exact = analytic_response(data,*exact_arguments,precise=True)
                estimates = []
                for step in [mp.mpf('1e-24'),mp.mpf('1e-29')]:
                    values = [current_values(data,*exact_arguments,amount=sign*step,precise=True,original=True) for sign in [-1,1]]
                    estimates.append((values[1]-values[0])/(2*step))
                scale = max(float(np.max(abs(exact))),1e-100)
                oracle_errors = [float(np.max(abs(estimate-exact)))/scale for estimate in estimates]
                evidence.check(branch+':all_points_active',active.all())
                evidence.check(branch+':independent_original_perturbation',max(oracle_errors)<1e-38,oracle_errors)
                target = np.asarray(exact,float)
                binary_error,old_error = binary-target,old-target
                evidence.check(branch+':analytic_complex_replay',np.max(abs(binary-compact_complex))<1e-12*scale,
                    float(np.max(abs(binary-compact_complex)))/scale)
                no_time = list(exact_arguments)
                no_time[-1] = no_time[-1]*0
                omitted_time = analytic_response(data,*no_time,precise=True)
                no_edge = dict(data,movement_left=data['displacement_left']*data['source_change'],
                    movement_right=data['displacement_right']*data['source_change'])
                omitted_edge = analytic_response(no_edge,*exact_arguments,precise=True)
                control_effects = [float(np.max(abs(value-exact))) for value in [omitted_time,omitted_edge]]
                evidence.check(branch+':omitted_response_controls_resolved',min(control_effects)>1e-50,control_effects)
                source_labels = np.linspace(-.45,.45,24)
                cardinal = evaluator.action.cardinal(source_labels)
                source_radius = cardinal@evaluator.action.source
                source_speed = cardinal@evaluator.action.velocity
                direction_speed = cardinal@evaluator.source_direction
                values,radial,time,change,change_r,change_t = metric_packet(restored,source_radius-evaluator.anchor)
                source_args = [converted(value) for value in [source_radius,values,time[0],change,change_t[0],source_speed,direction_speed,np.ones(24)]]
                mass,coupling = mp.mpf(evaluator.action.owner.source_mass),mp.mpf(evaluator.action.owner.coupling)
                combined = matter_gravity_response(*source_args,mass,coupling,precise=True)
                radius,values,mass_time,change,time_change,velocity,velocity_change,density = source_args
                def raw(amount):
                    moved = values+amount*change
                    geometry = 1-2*moved[0]/radius
                    lapse = precise_exp(moved[1])
                    speed = velocity+amount*velocity_change
                    return lapse*(mass_time+amount*time_change)/(coupling*precise_sqrt(geometry))
                    
                step = mp.mpf('1e-27')
                def full_raw(amount):
                    moved = values+amount*change
                    geometry = 1-2*moved[0]/radius
                    lapse = precise_exp(moved[1])
                    speed = velocity+amount*velocity_change
                    return raw(amount)+mass*density*lapse*lapse*speed/precise_sqrt(lapse*lapse-speed**2/geometry)
                oracle = (full_raw(step)-full_raw(-step))/(2*step)
                relative = float(np.max(abs(oracle-combined)))/max(float(np.max(abs(combined))),1e-100)
                evidence.check(branch+':dust_gravity_independent_perturbation',relative<1e-40,relative)
                path = evidence.output/(branch+'-probe.npz')
                np.savez_compressed(path,offsets=offsets,labels=labels,cells=cells,local=packet['local'],
                    analytic=binary,original_complex=old,compact_complex=compact_complex,oracle=target,
                    analytic_error=binary_error,original_error=old_error)
                evidence.own(path,'outputs')
                summary = dict(branch=branch,points=len(labels),source_points=len(source_labels),oracle_relative_errors=oracle_errors,
                    analytic_max_error=np.max(abs(binary_error),axis=1).tolist(),old_max_error=np.max(abs(old_error),axis=1).tolist(),
                    derivative_max=np.max(abs(target),axis=1).tolist(),omitted_response_effects=control_effects,
                    dust_gravity_oracle_relative=relative,integrated_C1_replaced=False,valid_for_claim=False)
                evidence.report['cases'].append(summary)
                evidence.save()
                print(json.dumps(summary),flush=True)
                if perf_counter()>deadline:
                    raise RuntimeError('Safe C1 point-probe boundary')
        evidence.report.update(seconds=perf_counter()-started,github_action=False,subagents_used=False)
        evidence.complete()
    except Exception as error:
        evidence.fail(error)
        raise


if __name__=='__main__':
    main()



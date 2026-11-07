import ast
import csv
from common import ROOT, EVOLUTION, BACKGROUND, HIERARCHY, WAVELENGTH, AVERAGE, GATE, ALGEBRA, modest, guard, check_prior, require, read, write, digest, load
import numpy as np
from scipy.interpolate import CubicSpline

def errors(prediction, target):
    return np.max(abs(prediction - target), axis=0) / np.maximum(np.max(abs(target), axis=0), 1e-30)


def physical(packet, wave):
    names = packet["observer_names"].tolist()
    get = lambda name: packet["observer"][:, names.index(name)]
    scale, hubble = get("a_native"), get("H_native")
    enthalpy = get("R") + get("Pbar")
    alpha = get("sigma") / wave
    phi = get("eta_sync") - hubble * alpha
    return dict(Phi=phi, Psi=2 * get("Weyl") - phi, D=get("D_sync") - 3 * hubble * enthalpy * alpha,
                Q=get("Q_sync") + enthalpy * get("sigma"), Pi=get("Pi"), theta_c=wave * get("sigma"),
                delta_c=get("delta_cdm64") - 3 * hubble * alpha, delta_b=get("delta_baryon64") - 3 * hubble * alpha,
                delta_gamma=get("delta_gamma64") - 4 * hubble * alpha, delta_massless=get("delta_massless64") - 4 * hubble * alpha,
                a=scale, H=hubble, R=enthalpy, Phi_rate=get("Weyl_prime") + get("Pi_prime") / (2 * wave ** 2))


def constraints(values, wave):
    expressions = dict(Hamiltonian=[2 * wave ** 2 * values["Phi"], values["D"], 3 * values["H"] * values["Q"] / wave],
                       slip=[values["Phi"], -values["Psi"], -values["Pi"] / wave ** 2],
                       momentum=[values["Phi_rate"], values["H"] * values["Psi"], -values["Q"] / (2 * wave)])
    result = {}
    for name, terms in expressions.items():
        array = np.array(terms)
        result[name] = float(np.max(abs(array.sum(axis=0))) / max(float(np.max(abs(array))), 1e-30))
    return result


def newton_budget(packet, probe_indices, wave):
    values = physical(packet, wave)
    times, scale = packet["times"], values["a"]
    poisson = -values["D"] / (2 * wave ** 2)
    momentum = -3 * values["H"] * values["Q"] / (2 * wave ** 3)
    shear = -values["Pi"] / wave ** 2
    force_scale = max(float(np.max(abs(values["Psi"]))), 1e-30)
    velocity_scale = max(float(np.max(abs(values["theta_c"]))), 1e-30)
    split = float(np.max(abs(values["Psi"] - poisson - momentum - shear)) / force_scale)
    replays = []
    for stride in (1, 2, 4):
        keep = np.unique(np.r_[np.arange(0, len(times), stride), len(times) - 1])
        antiderivative = CubicSpline(times[keep], scale[keep] * values["Psi"][keep]).antiderivative()
        replays.append((scale[0] * values["theta_c"][0] + wave ** 2 * (antiderivative(times[probe_indices]) - antiderivative(times[0]))) / scale[probe_indices])
    poisson_integral = CubicSpline(times, scale * poisson).antiderivative()
    poisson_velocity = (scale[0] * values["theta_c"][0] + wave ** 2 * (poisson_integral(times[probe_indices]) - poisson_integral(times[0]))) / scale[probe_indices]
    correction = CubicSpline(times, scale * (values["Psi"] - poisson))
    widths = np.diff(times)
    cell_budget = sum(abs(correction.c[index]) * widths ** (4 - index) / (4 - index) for index in range(4))
    accumulated = wave ** 2 * np.r_[0., np.cumsum(cell_budget)] / scale
    signed_change = replays[0] - poisson_velocity
    replay_error = float(np.max(abs(replays[0] - values["theta_c"][probe_indices])) / velocity_scale)
    source_refinement = max(float(np.max(abs(candidate - replays[0])) / velocity_scale) for candidate in replays[1:])
    bound_excess = float(np.max(np.maximum(abs(signed_change) - accumulated[probe_indices], 0)) / velocity_scale)
    report = dict(split_error=split, velocity_replay_error=replay_error, source_refinement=source_refinement, force_poisson_difference=float(np.max(abs(values["Psi"] - poisson)) / force_scale),
                  force_triangle_budget=float((np.max(abs(momentum)) + np.max(abs(shear))) / force_scale),
                  velocity_poisson_difference=float(np.max(abs(signed_change)) / velocity_scale), velocity_interpolant_budget=float(np.max(accumulated[probe_indices]) / velocity_scale),
                  bound_excess=bound_excess, passed=bool(max(split, bound_excess) < ALGEBRA and max(replay_error, source_refinement) < GATE),
                  scope="force approximation on corrected relativistic sources; not independently evolved Poisson cosmology or static local PPN")
    arrays = dict(times=times[probe_indices], a=scale[probe_indices], theta=values["theta_c"][probe_indices], theta_replayed=replays[0], theta_poisson=poisson_velocity, absolute_velocity_bound=accumulated[probe_indices],
                  force_times=times, Psi=values["Psi"], Psi_poisson=poisson, momentum_correction=momentum, shear_correction=shear)
    return report, arrays



def source_balance(packet, wave):
    terms, meta, times = packet["terms"],packet["metadata"],packet["times"]
    density,flux,pressure,density_rate,flux_rate,enthalpy,shear = [terms[:,:,index] for index in range(7)]
    hubble,metric_z = meta[:,1,None],meta[:,2,None]
    c_terms = np.array([density_rate,hubble*(density+3*pressure),wave*flux,wave*metric_z*enthalpy])
    e_terms = np.array([flux_rate,2*hubble*flux,-wave*pressure,2*wave/3*shear])
    residual_c,residual_e = c_terms.sum(axis=0),e_terms.sum(axis=0)
    predicted_c,predicted_e = np.zeros_like(residual_c),np.zeros_like(residual_e)
    predicted_c[:,1] = 3*hubble[:,0]*pressure[:,1]
    predicted_c[:,4] = wave*metric_z[:,0]*(enthalpy[:,4]-meta[:,3])
    fields = []
    for species,offset in ((5,4),(6,14)):
        field,velocity,field_rate,velocity_rate,mass,delta,delta_rate = [meta[:,offset+index] for index in range(7)]
        field_defect = field_rate-velocity
        velocity_defect = velocity_rate+2*hubble[:,0]*velocity+(meta[:,0]*mass)**2*field
        predicted_c[:,species] = velocity_defect*delta_rate+(meta[:,0]*mass)**2*field_defect*delta
        predicted_e[:,species] = wave*velocity_defect*delta
        fields.append(dict(kinematics=float(np.max(abs(field_defect))/max(np.max(abs(velocity)),1e-80)),
                           dynamics=float(np.max(abs(velocity_defect))/max(np.max(abs(velocity_rate)),np.max(abs(2*hubble[:,0]*velocity)),np.max(abs((meta[:,0]*mass)**2*field)),1e-80))))
    scales = np.array([max(np.max(abs(c_terms.sum(axis=2))),1e-80),max(np.max(abs(e_terms.sum(axis=2))),1e-80)])
    raw = np.column_stack([residual_c.sum(axis=1),residual_e.sum(axis=1)])
    predicted = np.column_stack([predicted_c.sum(axis=1),predicted_e.sum(axis=1)])
    residual = np.max(abs(raw),axis=0)/scales
    decomposition = np.max(abs(raw-predicted),axis=0)/scales
    states = np.column_stack([density.sum(axis=1),flux.sum(axis=1)])
    state_scales = np.maximum(np.max(abs(states),axis=0),1e-80)
    rhs = -np.column_stack([c_terms[1:].sum(axis=(0,2)),e_terms[1:].sum(axis=(0,2))])
    integral_rows, raw_replays,accounted_replays = [],[],[]
    for stride in (1,2,4):
        keep = np.unique(np.r_[np.arange(0,len(times),stride),len(times)-1])
        raw_integral = CubicSpline(times[keep],rhs[keep]).antiderivative()
        accounted_integral = CubicSpline(times[keep],(rhs+predicted)[keep]).antiderivative()
        raw_replay = states[0]+raw_integral(times)-raw_integral(times[0])
        accounted = states[0]+accounted_integral(times)-accounted_integral(times[0])
        integral_rows.append(dict(stride=stride,raw_error=(np.max(abs(raw_replay-states),axis=0)/state_scales).tolist(),
                                  accounted_error=(np.max(abs(accounted-states),axis=0)/state_scales).tolist()))
        raw_replays.append(raw_replay)
        accounted_replays.append(accounted)
    refinement = np.max(abs(raw_replays[-1]-raw_replays[0]),axis=0)/state_scales
    observer = packet["observer"]
    source_errors = dict(density=float(np.max(abs(states[:,0]-observer[:,2]))/max(np.max(abs(observer[:,2])),1e-80)),
                         flux=float(np.max(abs(states[:,1]-observer[:,3]))/max(np.max(abs(observer[:,3])),1e-80)),
                         shear=float(np.max(abs(shear.sum(axis=1)-observer[:,4]))/max(np.max(abs(observer[:,4])),1e-80)),
                         enthalpy=float(np.max(abs(enthalpy.sum(axis=1)-observer[:,0]-observer[:,1]))/max(np.max(abs(observer[:,0]+observer[:,1])),1e-80)))
    pass_algebra = max(*decomposition,*source_errors.values()) < ALGEBRA
    pass_numerical = max(*residual,*integral_rows[0]["raw_error"],*refinement,*[value for field in fields for value in field.values()]) < GATE
    report = dict(passed=bool(pass_algebra and pass_numerical),raw_continuity=float(residual[0]),raw_momentum=float(residual[1]),
                  algebra=decomposition.tolist(),source_errors=source_errors,fields=fields,integrals=integral_rows,
                  integral_refinement=refinement.tolist(),scales=scales.tolist(),
                  predicted_baryon_continuity=float(np.max(abs(predicted_c[:,1]))/scales[0]),
                  predicted_neutrino_continuity=float(np.max(abs(predicted_c[:,4]))/scales[0]),
                  predicted_scalar_continuity=float(np.max(abs(predicted_c[:,5:].sum(axis=1)))/scales[0]))
    arrays = dict(times=times,state=states,source_rhs=rhs,raw_residual=raw,predicted_residual=predicted,
                  raw_integral_replay=raw_replays[0],accounted_integral_replay=accounted_replays[0])
    return report,arrays

def metric_integral(packet, wave):
    values = physical(packet, wave)
    times = packet["times"]
    source = values["Q"]/(2*wave)-values["H"]*values["Psi"]
    phi_scale = max(np.max(abs(values["Phi"])),1e-80)
    curves = []
    for stride in (1,2,4):
        keep = np.unique(np.r_[np.arange(0,len(times),stride),len(times)-1])
        integral = CubicSpline(times[keep],source[keep]).antiderivative()
        curves.append(values["Phi"][0]+integral(times)-integral(times[0]))
    errors_all = [float(np.max(abs(curve-values["Phi"]))/phi_scale) for curve in curves]
    refinement = max(float(np.max(abs(curve-curves[0]))/phi_scale) for curve in curves[1:])
    observer = packet["observer"]
    raychaudhuri = -(observer[:,0]+3*observer[:,1])/6
    rate_from_geometry = observer[:,8]-raychaudhuri*observer[:,5]/wave-observer[:,28]*observer[:,6]/wave
    rate_scale = max(np.max(abs(source)),np.max(abs(values["Phi_rate"])),1e-80)
    relation = float(np.max(abs(rate_from_geometry-source))/rate_scale)
    report = dict(passed=bool(max(errors_all[0],refinement) < GATE and relation < ALGEBRA),
                  physical_Phi_integral_errors=errors_all,source_refinement=refinement,geometry_rate_identity=relation,
                  scope="Phi reconstructed from evolved eta,shear and repaired H versus integrated momentum Einstein equation")
    return report,dict(times=times,Phi=values["Phi"],Phi_replayed=curves[0],source=source,geometry_rate=rate_from_geometry)


from scipy.interpolate import PchipInterpolator


def norm(value):
    return max(float(np.max(abs(value))),1e-80)


def supnorm(value):
    return float(np.max(abs(value)))


def envelope_products(packet,wave):
    meta=packet["metadata"]
    scale,hubble,phase=packet["a"],packet["H"],packet["carrier_phase"]
    omega=scale*float(packet["mass"])
    field,velocity,field_rate,velocity_rate,_,delta,speed=[meta[:,14+index] for index in range(7)]
    rotate=np.exp(1j*phase)
    background=scale*(np.sqrt(omega)*field+1j*velocity/np.sqrt(omega))*rotate
    amplitude=packet["envelope"][:,0]+1j*packet["envelope"][:,1]
    native_amplitude=scale*(np.sqrt(omega)*delta+1j*speed/np.sqrt(omega))*rotate
    same=background*np.conjugate(amplitude)
    counter=background*amplitude/rotate**2
    density=omega/scale**2*same.real
    pressure=-omega/scale**2*counter.real
    current=wave/(2*scale**2)*(counter.imag+same.imag)
    endpoint=counter.imag/scale**2
    checks=dict(amplitude_reconstruction=supnorm(amplitude-native_amplitude)/norm(amplitude),
                density_product=supnorm(density-packet["terms"][:,6,0])/norm(packet["terms"][:,6,0]),
                pressure_product=supnorm(pressure-packet["terms"][:,6,2])/norm(packet["terms"][:,6,0]),
                current_product=supnorm(current-packet["terms"][:,6,1])/norm(packet["terms"][:,6,1]),
                endpoint_product=supnorm(endpoint-velocity*delta-field*speed)/norm(velocity*delta+field*speed))
    phase_derivative=packet["carrier_derivative"]
    defect_phi=field_rate-velocity
    defect_v=velocity_rate+2*hubble*velocity+omega**2*field
    background_chain=rotate*(scale*np.sqrt(omega)*(1.5*field+field_rate/hubble)+
                            1j*scale/np.sqrt(omega)*(.5*velocity+velocity_rate/hubble))+1j*phase_derivative*background
    background_derived=1.5*rotate**2*np.conjugate(background)+scale*rotate*(np.sqrt(omega)*defect_phi+1j*defect_v/np.sqrt(omega))/hubble+1j*(phase_derivative-omega/hubble)*background
    checks["background_chain"]=supnorm(background_chain-background_derived)/norm(background)
    metric_z=meta[:,2]
    amplitude_rate=(1.5*rotate**2*np.conjugate(amplitude)-
                    1j*wave**2/(2*omega*hubble)*(amplitude+rotate**2*np.conjugate(amplitude))-
                    1j*scale*wave*metric_z*velocity*rotate/(np.sqrt(omega)*hubble)+
                    1j*(phase_derivative-omega/hubble)*amplitude)
    gradient=wave**2/(2*omega*hubble)
    metric_coupling=wave*metric_z/(2*hubble)
    grouped_rate=(-1j*gradient*amplitude-metric_coupling*background+
                  rotate**2*((1.5-1j*gradient)*np.conjugate(amplitude)+metric_coupling*np.conjugate(background))+
                  1j*(phase_derivative-omega/hubble)*amplitude)
    checks["grouped_parent_coupling"]=supnorm(grouped_rate-amplitude_rate)/norm(amplitude)
    efolds=packet["efold"]
    replay_errors=[]
    replay_values=[]
    for stride in (1,2,4):
        keep=np.unique(np.r_[np.arange(0,len(efolds),stride),len(efolds)-1])
        integral=CubicSpline(efolds[keep],amplitude_rate[keep]).antiderivative()
        replay=amplitude[0]+integral(efolds)-integral(efolds[0])
        replay_errors.append(supnorm(replay-amplitude)/norm(amplitude))
        replay_values.append(replay)
    refinement=max(supnorm(value-replay_values[0])/norm(amplitude) for value in replay_values[1:])
    report=dict(algebra=checks,integral_errors=replay_errors,integral_refinement=refinement,
                carrier_rate_relative_defect=supnorm(phase_derivative-omega/hubble)/norm(omega/hubble),
                passed=bool(max(checks.values())<ALGEBRA and max(replay_errors[0],refinement)<GATE))
    return report,dict(efold=efolds,background_amplitude=background,amplitude=amplitude,rate=amplitude_rate,replayed=replay_values[0],
                       density=density,pressure=pressure,current=current,endpoint=endpoint)


def averaging_functions():
    owner=AVERAGE/"derive_and_test_common_domain.py"
    tree=ast.parse(owner.read_text())
    functions=[node for node in tree.body if isinstance(node,ast.FunctionDef) and node.name in ("source_arrays","averages","calculate")]
    require(len(functions)==3,"three retained pure averaging functions")
    namespace=dict(np=np,CubicSpline=CubicSpline,PchipInterpolator=PchipInterpolator,norm=norm,require=require,guard=guard,GATE=GATE,ALGEBRA=ALGEBRA,
                   CYCLES=(1,2,4,8),STRIDES=(1,2,4),CENTERS=17)
    exec(compile(ast.Module(body=functions,type_ignores=[]),str(owner),"exec"),namespace)
    return namespace["calculate"],digest(owner)


def main():
    modest()
    check_prior()
    owner=read(ROOT/"prediction-envelope-result.json")
    require(owner["state"]=="complete" and len(owner["reports"])==6,"completed36 envelope runs")
    require(owner["source_sha256"]==digest(ROOT/"run_envelope.py"),"driver source")
    native_owner=read(WAVELENGTH/"prediction-bound-result.json")
    average_owner=read(AVERAGE/"result-common.json")
    plans=read(AVERAGE/"frozen-common-windows.json")
    calculate,average_function_hash=averaging_functions()
    destination=ROOT/"comparison"
    destination.mkdir(exist_ok=False)
    reports=[]
    for family in owner["reports"]:
        guard()
        model,label,wave=family["model"],family["label"],family["wave"]
        stem=model+"-"+label
        folder=ROOT/"runs-envelope"/stem
        context=load(folder/"initial-context.npz")
        packets={}
        for case in family["cases"]:
            path=folder/case["file"]
            require(digest(path)==case["sha256"],"envelope trajectory owner")
            packet=load(path)
            expected=case["amplitude"]*context["initial"]
            initial_error=supnorm(packet["projected_state"][0]-expected)/norm(expected)
            require(initial_error<ALGEBRA,"initial native state retained")
            require(np.count_nonzero(packet["projected_state"][0][expected==0])==0,"unseeded zeros retained")
            require(np.array_equal(packet["a"],packet["observer"][:,27]),"native a exact")
            packets[case["tag"]]=packet
        parent=next(row for row in native_owner["reports"] if row["model"]==model and row["label"]==label)
        for tag in ("L128-fine","G192-fine"):
            item=next(row for row in parent["cases"] if row["tag"]==tag)
            path=WAVELENGTH/"runs-bound"/stem/item["file"]
            require(digest(path)==item["sha256"],"native-coordinate reference")
            packets["native-"+tag]=load(path)
        values={tag:physical(packet,wave) for tag,packet in packets.items()}
        signals=[name for name in values["G192-envelope-fine"] if name not in ("a","H","R")]
        comparisons=[]
        for name,left,right in [
            ("envelope precision","L128-envelope-base","L128-envelope-fine"),
            ("angular128/192","L128-envelope-fine","G192-envelope-fine"),
            ("carrier phase offset","L128-envelope-shift","L128-envelope-fine"),
            ("forward native L128","L128-envelope-fine","native-L128-fine"),
            ("forward native G192","G192-envelope-fine","native-G192-fine")]:
            state_error=float(np.max(errors(packets[left]["projected_state"],packets[right]["projected_state"])))
            source_errors={key:float(errors(values[left][key],values[right][key])) for key in signals}
            comparisons.append(dict(label=name,state_error=state_error,source_errors=source_errors,
                                    passed=bool(max(state_error,*source_errors.values())<GATE)))
        zero=bool(np.count_nonzero(packets["L128-envelope-zero"]["projected_state"])==0 and all(np.count_nonzero(values["L128-envelope-zero"][name])==0 for name in signals))
        parity=float(np.max(errors(-packets["L128-envelope-negative"]["projected_state"],packets["L128-envelope-base"]["projected_state"])))
        parity_sources=max(float(errors(-values["L128-envelope-negative"][name],values["L128-envelope-base"][name])) for name in signals)
        algebra={tag:constraints(value,wave) for tag,value in values.items() if not tag.startswith("native-")}
        balances,metrics,rotating={},{},{}
        for tag,packet in packets.items():
            if tag.startswith("native-"):
                continue
            balance,arrays=source_balance(packet,wave)
            path=destination/(stem+"-"+tag+"-balance.npz")
            np.savez_compressed(path,**arrays)
            balance.update(file=path.name,sha256=digest(path))
            balances[tag]=balance
            metric,arrays=metric_integral(packet,wave)
            path=destination/(stem+"-"+tag+"-metric.npz")
            np.savez_compressed(path,**arrays)
            metric.update(file=path.name,sha256=digest(path))
            metrics[tag]=metric
            if model=="heavy":
                rotation,arrays=envelope_products(packet,wave)
                path=destination/(stem+"-"+tag+"-amplitudes.npz")
                np.savez_compressed(path,**arrays)
                rotation.update(file=path.name,sha256=digest(path))
                rotating[tag]=rotation
        average_report,averages=calculate(packets["G192-envelope-fine"],model,wave,plans[label])
        old_family=next(row for row in average_owner["reports"] if row["model"]==model and row["label"]==label)
        old_case=old_family["cases"]["G192-fine"]
        old_path=AVERAGE/"results-common"/old_case["output"]
        require(digest(old_path)==old_case["output_sha256"],"saved averaged reference")
        old=load(old_path)
        average_comparisons={}
        for cycles,arrays in averages.items():
            density_scale=norm(old[cycles+"_matter_D"])
            selected=["matter_D","matter_P","matter_Q"]
            if model=="heavy":
                selected+=["gradient","boundary","expansion","metric","dense_defect","gauge","pressure_predicted"]
            error={key:norm(arrays[key]-old[cycles+"_"+key])/density_scale for key in selected}
            average_comparisons[cycles]=dict(errors=error,passed=max(error.values())<GATE)
        path=destination/(stem+"-averages.npz")
        np.savez_compressed(path,**{cycles+"_"+key:value for cycles,arrays in averages.items() for key,value in arrays.items()})
        average_report.update(file=path.name,sha256=digest(path))
        fine=packets["G192-envelope-fine"]
        probes=load(HIERARCHY/"runs-balanced"/model/"native-reference.npz")["probes"]
        newton,arrays=newton_budget(fine,probes,wave)
        path=destination/(stem+"-newton.npz")
        np.savez_compressed(path,**arrays)
        newton.update(file=path.name,sha256=digest(path))
        passed=bool(all(row["passed"] for row in comparisons) and zero and max(parity,parity_sources)<GATE
                    and max(value for row in algebra.values() for value in row.values())<ALGEBRA
                    and all(row["passed"] for row in balances.values()) and all(row["passed"] for row in metrics.values())
                    and all(row["passed"] for row in rotating.values())
                    and average_report["passed"] and all(row["passed"] for row in average_comparisons.values()) and newton["passed"])
        report=dict(model=model,label=label,wave=wave,passed=passed,comparisons=comparisons,zero=zero,parity=parity,
                    parity_sources=parity_sources,algebra=algebra,balance=balances,metric=metrics,rotating=rotating,
                    averages=average_report,average_comparisons=average_comparisons,newton=newton)
        reports.append(report)
        write(destination/(stem+"-result.json"),report)
        print(dict(model=model,label=label,passed=passed,comparison_errors={row["label"]:max(row["state_error"],*row["source_errors"].values()) for row in comparisons},
                   average_error=max(value for row in average_comparisons.values() for value in row["errors"].values()),
                   amplitude_replay=max([row["integral_errors"][0] for row in rotating.values()] or [0.])),flush=True)
    result=dict(passed=all(row["passed"] for row in reports),reports=reports,source_sha256=digest(__file__),
                prediction_sha256=digest(ROOT/"prediction-envelope-result.json"),averaging_function_sha256=average_function_hash,
                parent_averaging_sha256=digest(AVERAGE/"result-common.json"),gate=GATE,algebra_gate=ALGEBRA)
    write(ROOT/"comparison-result.json",result)
    require(result["passed"],"envelope comparison failed; inspect saved evidence")

if __name__=="__main__":
    main()


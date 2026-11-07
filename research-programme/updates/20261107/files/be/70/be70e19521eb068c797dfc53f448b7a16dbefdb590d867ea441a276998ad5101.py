import csv
from common import ROOT, HIERARCHY, BACKGROUND, COUPLED, WAVE, GATE, ALGEBRA, modest, guard, check_prior, require, read, write, digest, load
import numpy as np
from scipy.interpolate import CubicSpline

def errors(prediction, target):
    return np.max(abs(prediction - target), axis=0) / np.maximum(np.max(abs(target), axis=0), 1e-30)


def physical(packet):
    names = packet["observer_names"].tolist()
    get = lambda name: packet["observer"][:, names.index(name)]
    scale, hubble = get("a_native"), get("H_native")
    enthalpy = get("R") + get("Pbar")
    alpha = get("sigma") / WAVE
    phi = get("eta_sync") - hubble * alpha
    return dict(Phi=phi, Psi=2 * get("Weyl") - phi, D=get("D_sync") - 3 * hubble * enthalpy * alpha,
                Q=get("Q_sync") + enthalpy * get("sigma"), Pi=get("Pi"), theta_c=WAVE * get("sigma"),
                delta_c=get("delta_cdm64") - 3 * hubble * alpha, delta_b=get("delta_baryon64") - 3 * hubble * alpha,
                delta_gamma=get("delta_gamma64") - 4 * hubble * alpha, delta_massless=get("delta_massless64") - 4 * hubble * alpha,
                a=scale, H=hubble, R=enthalpy, Phi_rate=get("Weyl_prime") + get("Pi_prime") / (2 * WAVE ** 2))


def constraints(values):
    expressions = dict(Hamiltonian=[2 * WAVE ** 2 * values["Phi"], values["D"], 3 * values["H"] * values["Q"] / WAVE],
                       slip=[values["Phi"], -values["Psi"], -values["Pi"] / WAVE ** 2],
                       momentum=[values["Phi_rate"], values["H"] * values["Psi"], -values["Q"] / (2 * WAVE)])
    result = {}
    for name, terms in expressions.items():
        array = np.array(terms)
        result[name] = float(np.max(abs(array.sum(axis=0))) / max(float(np.max(abs(array))), 1e-30))
    return result


def newton_budget(packet, probe_indices):
    values = physical(packet)
    times, scale = packet["times"], values["a"]
    poisson = -values["D"] / (2 * WAVE ** 2)
    momentum = -3 * values["H"] * values["Q"] / (2 * WAVE ** 3)
    shear = -values["Pi"] / WAVE ** 2
    force_scale = max(float(np.max(abs(values["Psi"]))), 1e-30)
    velocity_scale = max(float(np.max(abs(values["theta_c"]))), 1e-30)
    split = float(np.max(abs(values["Psi"] - poisson - momentum - shear)) / force_scale)
    replays = []
    for stride in (1, 2, 4):
        keep = np.unique(np.r_[np.arange(0, len(times), stride), len(times) - 1])
        antiderivative = CubicSpline(times[keep], scale[keep] * values["Psi"][keep]).antiderivative()
        replays.append((scale[0] * values["theta_c"][0] + WAVE ** 2 * (antiderivative(times[probe_indices]) - antiderivative(times[0]))) / scale[probe_indices])
    poisson_integral = CubicSpline(times, scale * poisson).antiderivative()
    poisson_velocity = (scale[0] * values["theta_c"][0] + WAVE ** 2 * (poisson_integral(times[probe_indices]) - poisson_integral(times[0]))) / scale[probe_indices]
    correction = CubicSpline(times, scale * (values["Psi"] - poisson))
    widths = np.diff(times)
    cell_budget = sum(abs(correction.c[index]) * widths ** (4 - index) / (4 - index) for index in range(4))
    accumulated = WAVE ** 2 * np.r_[0., np.cumsum(cell_budget)] / scale
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



def source_balance(packet):
    terms, meta, times = packet["terms"],packet["metadata"],packet["times"]
    density,flux,pressure,density_rate,flux_rate,enthalpy,shear = [terms[:,:,index] for index in range(7)]
    hubble,metric_z = meta[:,1,None],meta[:,2,None]
    c_terms = np.array([density_rate,hubble*(density+3*pressure),WAVE*flux,WAVE*metric_z*enthalpy])
    e_terms = np.array([flux_rate,2*hubble*flux,-WAVE*pressure,2*WAVE/3*shear])
    residual_c,residual_e = c_terms.sum(axis=0),e_terms.sum(axis=0)
    predicted_c,predicted_e = np.zeros_like(residual_c),np.zeros_like(residual_e)
    predicted_c[:,1] = 3*hubble[:,0]*pressure[:,1]
    predicted_c[:,4] = WAVE*metric_z[:,0]*(enthalpy[:,4]-meta[:,3])
    fields = []
    for species,offset in ((5,4),(6,14)):
        field,velocity,field_rate,velocity_rate,mass,delta,delta_rate = [meta[:,offset+index] for index in range(7)]
        field_defect = field_rate-velocity
        velocity_defect = velocity_rate+2*hubble[:,0]*velocity+(meta[:,0]*mass)**2*field
        predicted_c[:,species] = velocity_defect*delta_rate+(meta[:,0]*mass)**2*field_defect*delta
        predicted_e[:,species] = WAVE*velocity_defect*delta
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

def metric_integral(packet):
    values = physical(packet)
    times = packet["times"]
    source = values["Q"]/(2*WAVE)-values["H"]*values["Psi"]
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
    rate_from_geometry = observer[:,8]-raychaudhuri*observer[:,5]/WAVE-observer[:,28]*observer[:,6]/WAVE
    rate_scale = max(np.max(abs(source)),np.max(abs(values["Phi_rate"])),1e-80)
    relation = float(np.max(abs(rate_from_geometry-source))/rate_scale)
    report = dict(passed=bool(max(errors_all[0],refinement) < GATE and relation < ALGEBRA),
                  physical_Phi_integral_errors=errors_all,source_refinement=refinement,geometry_rate_identity=relation,
                  scope="Phi reconstructed from evolved eta,shear and repaired H versus integrated momentum Einstein equation")
    return report,dict(times=times,Phi=values["Phi"],Phi_replayed=curves[0],source=source,geometry_rate=rate_from_geometry)

def main():
    modest()
    check_prior()
    owner = read(ROOT/"prediction-configured-result.json")
    require(owner["state"]=="complete" and len(owner["reports"])==2,"completed repaired coupled calculation")
    require(owner["source_sha256"]==digest(ROOT/"run_evolution_configured.py"),"prediction owner")
    destination = ROOT/"comparison"
    destination.mkdir(exist_ok=False)
    reports,rows = [],[]
    for model_owner in owner["reports"]:
        guard()
        model = model_owner["model"]
        original = load(HIERARCHY/"runs-balanced"/model/"native-reference.npz")
        old_coupled = load(COUPLED/"runs"/model/"G192-fine.npz")
        old_values = physical(old_coupled)
        packets = {}
        for case in model_owner["cases"]:
            path = ROOT/"runs-configured"/model/case["file"]
            require(digest(path)==case["sha256"],"case ownership")
            packet = load(path)
            require(np.array_equal(packet["efold"],load(BACKGROUND/"inputs"/(model+"-input.npz"))["efold"]),"same physical output grid")
            require(np.max(abs(packet["a"]-np.exp(packet["efold"])))==0,"physical scale")
            packets[case["tag"]] = packet
        values = {tag:physical(packet) for tag,packet in packets.items()}
        signal_names = [name for name in old_values if name not in ("a","H","R")]
        comparisons = []
        pairs = [("L64 precision","L64-base","L64-fine"),("L128 precision","L128-base","L128-fine"),
                 ("64/128 angular","L64-fine","L128-fine"),("128/G192 angular","L128-fine","G192-fine"),
                 ("background polynomial","L128-background-fine","L128-fine")]
        for label,left,right in pairs:
            state_error = float(np.max(errors(packets[left]["projected_state"],packets[right]["projected_state"])))
            source_errors = {name:float(errors(values[left][name],values[right][name])) for name in signal_names}
            comparisons.append(dict(label=label,left=left,right=right,state_error=state_error,physical_errors=source_errors,
                                    passed=bool(max(state_error,*source_errors.values()) < GATE)))
        algebra = {tag:constraints(value) for tag,value in values.items()}
        zero_state = bool(np.count_nonzero(packets["L64-zero"]["projected_state"])==0 and np.count_nonzero(packets["L64-zero"]["tail_norms"])==0)
        zero_sources = all(np.count_nonzero(values["L64-zero"][name])==0 for name in signal_names)
        negative_state = float(np.max(errors(-packets["L64-negative"]["projected_state"],packets["L64-base"]["projected_state"])))
        negative_sources = {name:float(errors(-values["L64-negative"][name],values["L64-base"][name])) for name in signal_names}
        changes = {name:float(errors(old_values[name],values["G192-fine"][name])) for name in signal_names}
        state_change = float(np.max(errors(old_coupled["projected_state"],packets["G192-fine"]["projected_state"])))
        balances,newton,metric = {},{},{}
        for tag,packet in packets.items():
            guard()
            balance,arrays = source_balance(packet)
            path = destination/(model+"-"+tag+"-balance.npz")
            np.savez_compressed(path,**arrays)
            balance.update(file=path.name,sha256=digest(path))
            balances[tag] = balance
            metric_report,metric_arrays = metric_integral(packet)
            path = destination/(model+"-"+tag+"-metric.npz")
            np.savez_compressed(path,**metric_arrays)
            metric_report.update(file=path.name,sha256=digest(path))
            metric[tag] = metric_report
            if tag in ("L64-fine","L128-fine","G192-fine"):
                budget,budget_arrays = newton_budget(packet,original["probes"])
                path = destination/(model+"-"+tag+"-newton.npz")
                np.savez_compressed(path,**budget_arrays)
                budget.update(file=path.name,sha256=digest(path))
                newton[tag] = budget
        passed = bool(all(row["passed"] for row in comparisons) and max(value for record in algebra.values() for value in record.values()) < ALGEBRA
                      and zero_state and zero_sources and max(negative_state,*negative_sources.values()) < GATE
                      and all(row["passed"] for row in balances.values()) and all(row["passed"] for row in metric.values())
                      and all(row["passed"] for row in newton.values()))
        report = dict(model=model,passed=passed,comparisons=comparisons,algebra=algebra,zero_state=zero_state,zero_sources=zero_sources,
                      negative_state=negative_state,negative_sources=negative_sources,change_from_old_coupled=changes,state_change_from_old_coupled=state_change,
                      balance=balances,metric=metric,newton=newton,initial_slice_preserved=True)
        reports.append(report)
        write(destination/(model+"-result.json"),report)
        for name in signal_names:
            rows.append(dict(model=model,observable=name,old_to_repaired=changes[name],**{comparison["label"]:comparison["physical_errors"][name] for comparison in comparisons}))
        print(dict(model=model,passed=passed,comparisons=[(row["label"],row["state_error"],max(row["physical_errors"].values())) for row in comparisons],
                   balance=balances["G192-fine"],metric=metric["G192-fine"],newton=newton["G192-fine"],changes=changes),flush=True)
    with (ROOT/"physical-comparison.csv").open("x",newline="",encoding="utf-8") as stream:
        writer=csv.DictWriter(stream,fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)
    result = dict(passed=all(row["passed"] for row in reports),reports=reports,source_sha256=digest(__file__),
                  prediction_result_sha256=digest(ROOT/"prediction-configured-result.json"),csv_sha256=digest(ROOT/"physical-comparison.csv"),
                  numerical_gate=GATE,algebra_gate=ALGEBRA,old_coupled_closeout_sha256=digest(COUPLED/"closeout.json"),
                  original_bank_unchanged=True)
    write(ROOT/"comparison-result.json",result)
    require(result["passed"],"comparison gate failed; inspect preserved evidence")

if __name__ == "__main__":
    main()


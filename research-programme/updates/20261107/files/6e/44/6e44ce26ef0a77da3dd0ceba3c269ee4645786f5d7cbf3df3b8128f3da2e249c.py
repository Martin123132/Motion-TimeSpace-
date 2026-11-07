import ast
from pathlib import Path
from common import ROOT, POST, PRIOR, GATE, ALGEBRA, require, guard, modest, read, write, digest, load, norm, verify_parent
import numpy as np
import sympy as sp
from scipy.interpolate import CubicSpline, PchipInterpolator

CYCLES = (1, 2, 4, 8)
STRIDES = (1, 2, 4)
CENTERS = 17


def symbolic():
    field, velocity, delta, speed, hubble, omega2, wave, metric, defect_phi, defect_v = sp.symbols("phi v delta u H omega2 k z ephi ev", real=True)
    field_rate = velocity + defect_phi
    velocity_rate = -2*hubble*velocity-omega2*field+defect_v
    speed_rate = -2*hubble*speed-(wave**2+omega2)*delta-wave*metric*velocity
    stress_d = velocity*speed+omega2*field*delta
    stress_p = velocity*speed-omega2*field*delta
    virial = velocity*delta+field*speed
    virial_rate = velocity_rate*delta+velocity*speed+field_rate*speed+field*speed_rate
    defects = defect_v*delta+defect_phi*speed
    remainder = virial_rate+2*hubble*virial+wave*metric*field*velocity-defects
    coefficient = wave**2/(4*omega2+wave**2)
    weight = 2*omega2/(4*omega2+wave**2)
    identities = {
        "finite_window_virial": sp.expand(2*stress_p-virial_rate-2*hubble*virial-wave**2*field*delta-wave*metric*field*velocity+defects),
        "gradient_coefficient": sp.factor(stress_p-coefficient*stress_d-weight*remainder),
        "moving_weight_derivative": sp.factor(sp.diff(weight,omega2)*2*hubble*omega2-4*hubble*omega2*wave**2/(4*omega2+wave**2)**2),
        "coefficient_weight_relation": sp.factor(weight-(1-coefficient)/2),
    }
    require(all(value == 0 for value in identities.values()), "symbolic identities")
    return {name: str(value) for name,value in identities.items()}


def windows(packet,domain):
    meta = packet["metadata"]
    omega = packet["a"]*meta[:,18]
    phase = np.unwrap(np.arctan2(-meta[:,15]/omega,meta[:,14]))
    require(np.all(np.diff(phase)>0), "monotone background phase")
    margin = max(CYCLES)*np.pi
    require(phase[-1]-phase[0]>2*margin, "enough complete cycles")
    forward = PchipInterpolator(packet["efold"],phase)
    low_phase,high_phase = float(forward(domain["left"])),float(forward(domain["right"]))
    require(high_phase-low_phase>2*margin,"common-domain complete cycles")
    centers = np.linspace(low_phase+margin,high_phase-margin,CENTERS)
    inverse = PchipInterpolator(phase,packet["efold"])
    result = {}
    for cycles in CYCLES:
        left_phase,right_phase = centers-cycles*np.pi,centers+cycles*np.pi
        left,right = inverse(left_phase),inverse(right_phase)
        result[str(cycles)] = dict(efold_left=left.tolist(),efold_right=right.tolist(),
                                  phase_left=left_phase.tolist(),phase_right=right_phase.tolist(),cycles=cycles)
    return dict(phase_start=float(phase[0]),phase_end=float(phase[-1]),centers=centers.tolist(),
                unwrapped_cycles=float((phase[-1]-phase[0])/(2*np.pi)),windows=result,
                rule="background only; 1/2/4/8 complete cycles; fixed physical-a endpoints")


def averages(times, matrix, left, right, stride):
    keep = np.unique(np.r_[np.arange(0,len(times),stride),len(times)-1])
    curve = CubicSpline(times[keep],matrix[keep])
    integral = curve.antiderivative()
    output = (integral(right)-integral(left))/(right-left)[:,None]
    return output,curve


def source_arrays(packet,model,wave):
    meta,terms,obs = packet["metadata"],packet["terms"],packet["observer"]
    hubble,metric_z,alpha = packet["H"],meta[:,2],obs[:,5]/wave
    total_d = obs[:,2]-3*hubble*(obs[:,0]+obs[:,1])*alpha
    total_q = obs[:,3]+(obs[:,0]+obs[:,1])*obs[:,5]
    total_pi = obs[:,4]
    phi = obs[:,7]-hubble*alpha
    psi = 2*obs[:,9]-phi
    poisson = -total_d/(2*wave**2)
    momentum = -3*hubble*total_q/(2*wave**3)
    shear = -total_pi/wave**2
    arrays = dict(total_D=total_d,total_Q=total_q,total_Pi=total_pi,Psi=psi,Psi_P=poisson,
                  momentum_force=momentum,shear_force=shear,absolute_force=abs(momentum)+abs(shear))
    algebra = dict(force_split=norm(psi-poisson-momentum-shear)/norm(psi))
    if model == "cold":
        arrays.update(matter_D=terms[:,0,0]-3*hubble*terms[:,0,5]*alpha,
                      matter_P=terms[:,0,2],matter_Q=terms[:,0,1]+terms[:,0,5]*obs[:,5])
        algebra["cold_pressure_zero"] = float(np.count_nonzero(arrays["matter_P"]))
        return arrays,algebra
    field,velocity,field_rate,velocity_rate,mass,delta,speed = [meta[:,14+index] for index in range(7)]
    omega2 = (packet["a"]*mass)**2
    coefficient = wave**2/(4*omega2+wave**2)
    weight = 2*omega2/(4*omega2+wave**2)
    weight_rate = 4*hubble*omega2*wave**2/(4*omega2+wave**2)**2
    defect_phi = field_rate-velocity
    defect_v = velocity_rate+2*hubble*velocity+omega2*field
    defects = defect_v*delta+defect_phi*speed
    speed_rate = -2*hubble*speed-(wave**2+omega2)*delta-wave*metric_z*velocity
    virial = velocity*delta+field*speed
    virial_rate = velocity_rate*delta+velocity*speed+field_rate*speed+field*speed_rate
    density,pressure = terms[:,6,0],terms[:,6,2]
    gauge_density = -3*hubble*velocity**2*alpha
    gauge_pressure = alpha*(velocity*velocity_rate-hubble*velocity**2-omega2*field*field_rate)
    matter_d,matter_p = density+gauge_density,pressure+gauge_pressure
    point = coefficient*density+weight*(virial_rate+2*hubble*virial+wave*metric_z*field*velocity-defects)
    array_scale = norm(density)
    algebra.update(pressure_reconstruction=norm(point-pressure)/array_scale,
                   canonical_density=norm(density-velocity*speed-omega2*field*delta)/array_scale,
                   canonical_pressure=norm(pressure-velocity*speed+omega2*field*delta)/array_scale)
    arrays.update(matter_D=matter_d,matter_P=matter_p,matter_Q=terms[:,6,1]+velocity**2*obs[:,5],
                  gradient=coefficient*matter_d,endpoint_primitive=weight*virial,
                  expansion=(2*hubble*weight-weight_rate)*virial,
                  metric=weight*wave*metric_z*field*velocity,
                  dense_defect=-weight*defects,
                  gauge=gauge_pressure-coefficient*gauge_density,
                  pressure_sync=pressure,density_sync=density,
                  gauge_density_defect=alpha*(velocity*defect_v+omega2*field*defect_phi),
                  coefficient=coefficient)
    return arrays,algebra


def calculate(packet,model,wave,plan):
    arrays,algebra = source_arrays(packet,model,wave)
    require(max(algebra.values())<ALGEBRA, "pointwise identities")
    names = list(arrays)
    matrix = np.column_stack([arrays[name] for name in names])
    clock = PchipInterpolator(packet["efold"],packet["times"])
    reports,outputs = {},{}
    for cycles in CYCLES:
        guard()
        window = plan["windows"][str(cycles)]
        left,right = clock(window["efold_left"]),clock(window["efold_right"])
        require(np.all(right>left) and left.min()>=packet["times"][0] and right.max()<=packet["times"][-1], "physical window domain")
        sets = []
        for stride in STRIDES:
            averaged,curve = averages(packet["times"],matrix,left,right,stride)
            value = {name:averaged[:,index] for index,name in enumerate(names)}
            if model=="heavy":
                column = names.index("endpoint_primitive")
                boundary = (curve(right)[:,column]-curve(left)[:,column])/(right-left)
                value["boundary"] = boundary
                value["pressure_predicted"] = sum(value[name] for name in ("gradient","boundary","expansion","metric","dense_defect","gauge"))
                value["pressure_without_boundary"] = value["pressure_predicted"]-boundary
                value["pressure_without_gauge"] = value["pressure_predicted"]-value["gauge"]
            sets.append(value)
        reference = sets[0]
        matter_scale = norm(reference["matter_D"])
        pressure_error = norm(reference["matter_P"]-reference["pressure_predicted"])/matter_scale if model=="heavy" else 0.
        refinement = {}
        for stride,value in zip(STRIDES[1:],sets[1:]):
            if model=="heavy":
                selected=("matter_D","matter_P","gradient","boundary","expansion","metric","dense_defect","gauge","pressure_predicted")
            else:
                selected=("matter_D","matter_P","matter_Q")
            refinement[str(stride)]=max(norm(value[name]-reference[name])/matter_scale for name in selected)
        force_scale = norm(reference["total_D"])/(2*wave**2)
        force_error = norm(reference["Psi"]-reference["Psi_P"])/force_scale
        bound = (norm(reference["momentum_force"])+norm(reference["shear_force"]))/force_scale
        force_identity = norm(reference["Psi"]-reference["Psi_P"]-reference["momentum_force"]-reference["shear_force"])/force_scale
        force_refinement = max(norm(value[name]-reference[name])/force_scale for value in sets[1:] for name in ("Psi","Psi_P","momentum_force","shear_force"))
        row = dict(cycles=cycles,count=CENTERS,duration_min=float(np.min(right-left)),duration_max=float(np.max(right-left)),
                   pressure_over_density=norm(reference["matter_P"])/matter_scale,
                   raw_pressure_over_density=norm(arrays["matter_P"])/norm(arrays["matter_D"]),
                   matter_density_norm=matter_scale,pressure_reconstruction_error=pressure_error,
                   integration_refinement=refinement,force_error=force_error,force_bound=bound,
                   force_identity=force_identity,force_refinement=force_refinement,
                   cold_pressure_exact_zero=bool(np.count_nonzero(reference["matter_P"])==0) if model=="cold" else None)
        if model=="heavy":
            row.update(components_over_density={name:norm(reference[name])/matter_scale for name in ("gradient","boundary","expansion","metric","dense_defect","gauge")},
                       gradient_only_error=norm(reference["matter_P"]-reference["gradient"])/matter_scale,
                       boundary_omission_error=norm(reference["matter_P"]-reference["pressure_without_boundary"])/matter_scale,
                       gauge_omission_error=norm(reference["matter_P"]-reference["pressure_without_gauge"])/matter_scale,
                       density_gauge_defect=norm(reference["gauge_density_defect"])/matter_scale,
                       coefficient_min=float(np.min(arrays["coefficient"])),coefficient_max=float(np.max(arrays["coefficient"])))
        row["passed"] = bool(max(pressure_error,*refinement.values(),force_refinement)<GATE and force_identity<ALGEBRA and force_error<=bound+ALGEBRA)
        if model=="cold":
            row["passed"] = row["passed"] and row["cold_pressure_exact_zero"]
        reports[str(cycles)] = row
        outputs[str(cycles)] = dict(left=left,right=right,**reference)
    return dict(passed=all(row["passed"] for row in reports.values()),algebra=algebra,windows=reports),outputs


def main():
    modest()
    verify_parent()
    symbolic_result=symbolic()
    write(ROOT/"symbolic-common-identities.json",dict(passed=True,identities=symbolic_result,source_sha256=digest(__file__)))
    config=dict(cycles=CYCLES,strides=STRIDES,centers=CENTERS,gate=GATE,algebra=ALGEBRA,
                cases=["G192-fine","L128-fine"],parent_sha256=digest(PRIOR/"closeout.json"),source_sha256=digest(__file__),
                protocol_sha256=digest(ROOT/"PROTOCOL.md"),source_paths=[
                    str(POST/"condensate-origin-20261003/native-heavy-matching-20261007/native/fortran/MTSTwoField.f90"),
                    str(PRIOR/"build-full-momentum/camb_python.f90")])
    require(all(Path(path).is_file() for path in config["source_paths"]),"equation paths")
    config["source_hashes"]={path:digest(path) for path in config["source_paths"]}
    write(ROOT/"config-common.json",config)
    owner=read(PRIOR/"prediction-bound-result.json")
    domain_rows=[]
    for group in owner["reports"]:
        for tag in ("G192-fine","L128-fine"):
            case=next(row for row in group["cases"] if row["tag"]==tag)
            path=PRIOR/"runs-bound"/(group["model"]+"-"+group["label"])/case["file"]
            require(digest(path)==case["sha256"],"common-domain source")
            with np.load(path) as archive:
                grid=archive["efold"]
                domain_rows.append(dict(model=group["model"],label=group["label"],tag=tag,
                                        first=float(grid[0]),second=float(grid[1]),penultimate=float(grid[-2]),last=float(grid[-1])))
    domain=dict(left=max(row["second"] for row in domain_rows),right=min(row["penultimate"] for row in domain_rows),
                full_left=max(row["first"] for row in domain_rows),full_right=min(row["last"] for row in domain_rows),
                rule="common saved physical domain, one original output cell inward on each model; no extrapolation",rows=domain_rows)
    require(domain["left"]<domain["right"],"shared physical domain")
    write(ROOT/"common-domain.json",domain)
    plans={}
    for label in ("half","balanced","double"):
        group=next(row for row in owner["reports"] if row["model"]=="heavy" and row["label"]==label)
        case=next(row for row in group["cases"] if row["tag"]=="G192-fine")
        path=PRIOR/"runs-bound"/("heavy-"+label)/case["file"]
        require(digest(path)==case["sha256"],"phase source checksum")
        packet=load(path)
        plans[label]=windows(packet,domain)
        plans[label].update(source=str(path),source_sha256=case["sha256"])
        del packet
    write(ROOT/"frozen-common-windows.json",plans)
    destination=ROOT/"results-common"
    destination.mkdir(exist_ok=False)
    reports=[]
    for group in owner["reports"]:
        model,label,wave=group["model"],group["label"],group["wave"]
        family={}
        for tag in ("G192-fine","L128-fine"):
            guard()
            case=next(row for row in group["cases"] if row["tag"]==tag)
            path=PRIOR/"runs-bound"/(model+"-"+label)/case["file"]
            require(digest(path)==case["sha256"],"sealed history")
            packet=load(path)
            report,arrays=calculate(packet,model,wave,plans[label])
            output=destination/(model+"-"+label+"-"+tag+".npz")
            np.savez_compressed(output,**{cycles+"_"+name:value for cycles,values in arrays.items() for name,value in values.items()})
            report.update(model=model,label=label,wave=wave,tag=tag,input=str(path),input_sha256=case["sha256"],
                          output=output.name,output_sha256=digest(output))
            family[tag]=(report,arrays)
            del packet
        control={}
        for cycles in CYCLES:
            key=str(cycles)
            primary,other=family["G192-fine"][1][key],family["L128-fine"][1][key]
            matter_scale=norm(primary["matter_D"])
            force_scale=norm(primary["total_D"])/(2*wave**2)
            control[key]=dict(matter=max(norm(primary[name]-other[name])/matter_scale for name in ("matter_D","matter_P","matter_Q")),
                              force=max(norm(primary[name]-other[name])/force_scale for name in ("Psi","Psi_P","momentum_force","shear_force")))
        passed=all(value[0]["passed"] for value in family.values()) and max(value for row in control.values() for value in row.values())<GATE
        result=dict(model=model,label=label,wave=wave,passed=passed,angular_control=control,
                    cases={tag:value[0] for tag,value in family.items()})
        reports.append(result)
        write(destination/(model+"-"+label+".json"),result)
        print(dict(model=model,label=label,passed=passed,pressure_ratios={key:row["pressure_over_density"] for key,row in family["G192-fine"][0]["windows"].items()},reconstruction=max(row["pressure_reconstruction_error"] for row in family["G192-fine"][0]["windows"].values())),flush=True)
    result=dict(passed=all(row["passed"] for row in reports),reports=reports,source_sha256=digest(__file__),
                config_sha256=digest(ROOT/"config-common.json"),windows_sha256=digest(ROOT/"frozen-common-windows.json"),
                identities_sha256=digest(ROOT/"symbolic-identities.json"),source_bank_changed=False,new_evolutions=0)
    write(ROOT/"result-common.json",result)
    require(result["passed"],"averaging checks failed; preserve and diagnose")

if __name__=="__main__":
    main()


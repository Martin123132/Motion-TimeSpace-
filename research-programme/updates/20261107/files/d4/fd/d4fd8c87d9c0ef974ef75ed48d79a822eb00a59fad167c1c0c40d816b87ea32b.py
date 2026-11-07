import ast
import csv
import json
from pathlib import Path
from common import ROOT, BACKGROUND, NATIVE, CLOSURE, SOURCE, PRIOR, BRIDGE, GATE, ALGEBRA, modest, guard, check_prior, require, read, write, digest, load
import numpy as np
from numpy.polynomial import Polynomial

def main():
    modest()
    check_prior()
    rows = []
    def check(name, passed, detail=None):
        rows.append(dict(check=name, passed=bool(passed), detail=detail))
    report = read(ROOT / "check-result.json")
    build = read(ROOT / "build/build-result.json")
    check("completed matched bridge", report["state"] == "complete" and report["passed"] and len(report["reports"]) == 2)
    check("unchanged tolerances", report["gate"] == GATE and report["algebra_gate"] == ALGEBRA)
    check("no new perturbation trajectory", report["no_new_perturbation_evolution"])
    check("build ownership", digest(ROOT / "build/native/camb/cambdll.dll") == build["dll_sha256"])
    check("compiler mappings removed", build["temporary_mappings_removed"] and all(not Path(drive).exists() for drive in ("R:/", "S:/", "T:/")))
    for path, checksum in build["reused_object_module_hashes"].items():
        check("preserved object " + Path(path).name, digest(path) == checksum)
    for path, checksum in build["original_input_hashes"].items():
        check("preserved parent " + path, digest(path) == checksum)
    for name, checksum in build["source_hashes"].items():
        check("compiled source " + name, digest(ROOT / "build" / name) == checksum)
    check("checker source", digest(ROOT / "check_bridge.py") == report["source_sha256"])
    original = (NATIVE / "fortran/MTSTwoField.f90").read_text()
    isolated = (ROOT / "build/MTSTwoField.f90").read_text()
    type_start, type_end = "type, extends(TDarkEnergyModel)", "public TMTSTwoField"
    check("scalar type and procedure layout preserved", original[original.index(type_start):original.index(type_end)] == isolated[isolated.index(type_start):isolated.index(type_end)])
    for name in ("MTS_Background", "MTS_Stress", "MTS_Evolve", "MTS_Diagnostics"):
        start = original.index("subroutine " + name + "(")
        end = original.index("end subroutine", start) + len("end subroutine")
        check("canonical parent routine " + name, original[start:end] in isolated)
    paths = [ROOT / "common.py", ROOT / "build_bridge.py", ROOT / "check_bridge.py", Path(__file__)]
    for path in paths:
        ast.parse(path.read_text())
        compile(path.read_text(),str(path),"exec")
        check("python syntax " + path.name, True)
    for owner in report["reports"]:
        model = owner["model"]
        guard()
        packet = load(owner["packet"])
        dense_path = BACKGROUND / "runs" / model / "dop-half-cap.npz"
        dense = load(dense_path)
        check(model+" output ownership", digest(owner["packet"]) == owner["packet_sha256"])
        check(model+" dense ownership", digest(dense_path) == owner["dense_input_sha256"])
        check(model+" finite packets", all(np.isfinite(values).all() for values in packet.values() if values.dtype.kind in "fci"))
        check(model+" paired physical probes", packet["terms"].shape == (65,7,7) and packet["observer"].shape == (65,30))
        check(model+" mapped a", np.max(abs(packet["repaired_thermal"][:,0]/packet["repaired_thermal"][:,2]-1)) < ALGEBRA)
        check(model+" physical clock observer", np.array_equal(packet["observer"][:,29],packet["dense"][:,11]))
        check(model+" physical a observer", np.array_equal(packet["observer"][:,27],packet["dense"][:,10]))
        clock_error = float(np.max(abs(packet["dense"][:,9]*packet["observer"][:,28]-1)))
        check(model+" differential clock", clock_error < GATE, clock_error)
        expected_fields = dense["initial_fields"] + packet["dense"][:,[0,2]]
        check(model+" canonical field anchoring", np.array_equal(packet["metadata"][:,4],expected_fields[:,0]) and np.array_equal(packet["metadata"][:,14],expected_fields[:,1]))
        check(model+" canonical velocity transport", np.array_equal(packet["metadata"][:,[5,15]],packet["dense"][:,[1,3]]))
        independent_values, independent_rates = [], []
        for efold in packet["efold"]:
            index = int(np.searchsorted(dense["segment_end"],efold,side="left"))
            width = dense["segment_end"][index]-dense["segment_start"][index]
            coordinate = (efold-dense["segment_start"][index])/width
            values, rates = [], []
            for component in range(5):
                polynomial = Polynomial([0.])
                for degree, coefficient in enumerate(dense["coefficients"][index,::-1,component]):
                    polynomial = (polynomial+coefficient)*Polynomial([0.,1.] if degree%2==0 else [1.,-1.])
                polynomial += dense["segment_initial"][index,component]
                values.append(polynomial(coordinate)*dense["units"][component])
                rates.append(polynomial.deriv()(coordinate)/width*dense["units"][component])
            independent_values.append(values)
            independent_rates.append(rates)
        independent = np.column_stack([independent_values,independent_rates])
        dense_scale = np.maximum(np.max(abs(packet["dense"][:,:10]),axis=0),1e-80)
        polynomial_error = float(np.max(abs(independent-packet["dense"][:,:10])/dense_scale))
        check(model+" independent dense polynomial", polynomial_error < ALGEBRA, polynomial_error)
        checks = owner["checks"]
        for label in ("dense_transport","unchanged_operator","source_hubble","thermal_inverse","continuity_decomposition","momentum_decomposition","linearity","physical_closure","physical_speeds"):
            check(model+" algebra "+label, checks[label] < ALGEBRA,checks[label])
        for label,value in checks["source_decomposition"].items():
            check(model+" source "+label,value < ALGEBRA,value)
        for label in ("raw_continuity","raw_momentum","scalar_continuity"):
            check(model+" numerical "+label,checks[label] < GATE,checks[label])
        for field_index, field in enumerate(checks["canonical_fields"]):
            for label,value in field.items():
                check(model+" field "+str(field_index)+" "+label,value < GATE,value)
        for label in ("thermal_control","thermal_changed"):
            for index,value in enumerate(checks[label]):
                check(model+" "+label+" "+str(index),value < GATE,value)
        check(model+" directional density and flux",max(checks["directional_errors"][-1]) < GATE,checks["directional_errors"][-1])
        check(model+" true zero", checks["zero"])
        check(model+" thermal RHS sensitivity",checks["thermal_rhs_change"] < GATE, checks["thermal_rhs_change"])
        check(model+" dense clock monotone",np.all(np.diff(packet["dense"][:,11])>0))
        check(model+" old perturbation treatment explicit",owner["no_new_perturbation_trajectory"])
        check(model+" exact heavy domain",float(packet["dense"][-1,10]) < .00028)
    coverage = BRIDGE / "final-stable-real-batch-rays037-038/common-coverage.json"
    check("scattering coverage preserved",digest(coverage) == "95d628bbe34ddc317e1d954d8e556271d666645e259f0eda66245be0607a0db3")
    for path in ROOT.glob("*.end.json"):
        receipt = read(path)
        check("receipt "+path.name,receipt["exit_code"] == 0)
    artifact_paths = [path for path in ROOT.rglob("*") if path.is_file()]
    protected = [NATIVE/"fortran/MTSTwoField.f90",NATIVE/"fortran/equations.f90",CLOSURE/"build/camb_python.f90",
                 SOURCE/"phase-resolved/tangent-native-result.json",PRIOR/"observer.f90",BACKGROUND/"closeout.json",coverage]
    result = dict(passed=all(row["passed"] for row in rows),count=len(rows),checks=rows,
                  check_result_sha256=digest(ROOT/"check-result.json"),build_result_sha256=digest(ROOT/"build/build-result.json"),
                  source_hashes={str(path):digest(path) for path in paths},
                  artifacts=[dict(path=str(path),sha256=digest(path)) for path in artifact_paths],
                  protected_sources={str(path):digest(path) for path in protected}, numerical_gate=GATE,algebra_gate=ALGEBRA)
    write(ROOT/"validation-result.json",result)
    print(dict(passed=result["passed"],checks=len(rows),failed=[row for row in rows if not row["passed"]]),flush=True)
    require(result["passed"],"validation failed")

if __name__ == "__main__":
    main()


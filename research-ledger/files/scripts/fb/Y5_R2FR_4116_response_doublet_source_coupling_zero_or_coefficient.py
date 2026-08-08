from __future__ import annotations

import csv
import py_compile
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List, Tuple


ROOT = Path(__file__).resolve().parents[1]
PROJECT = ROOT.parent
SOURCE_DIR = ROOT / "source-intake" / "mts_residuals"
FORMALIZATION = PROJECT / "formalization-workbench"
SCRIPT_PATH = Path(__file__).resolve()
DOC_PATH = ROOT / "4116-Y5-R2FR-response-doublet-source-coupling-zero-or-coefficient.md"

TIMESTAMP = datetime.now(timezone.utc).replace(microsecond=0).isoformat()
BRANCH_ID = "MTS_R2FR_Y5_RESPONSE_DOUBLET_JZ_COUPLING_CURRENT_SPINE_4116"
CHECKPOINT_ID = "4116"
DECISION = "JZ_COUPLING_LAW_IMPORTED_ZERO_ROUTE_UNSIGNED_PARENT_ACTION_CLAUSE_NEXT"


LOCAL_SOURCES: Dict[str, Tuple[Path, str, str]] = {
    "SRC4116_00_4115_next": (
        SOURCE_DIR / "P8_Y5_R2FR_4115_NEXT_TARGET.csv",
        "4116-Y5-R2FR-response-doublet-source-coupling-zero-or-coefficient.md",
        "4115 selected response-doublet source coupling zero or coefficient.",
    ),
    "SRC4116_01_4115_status": (
        SOURCE_DIR / "P8_Y5_R2FR_4115_STATUS.csv",
        "EVEN_RESPONSE_SCALAR_DENSITY_IMPORTED_F1_ZERO_FOUND_JZ_COUPLING_NEXT",
        "Current-chain scalar-density/double-zero handoff.",
    ),
    "SRC4116_02_3629_status": (
        SOURCE_DIR / "P8_Y5_R2FR_3629_STATUS.csv",
        "JZ_COUPLING_LAW_DERIVED_ZERO_ROUTE_UNSIGNED_COEFFICIENT_ROWS_STAGED",
        "3629 derives exact J_Z source-coupling obstruction.",
    ),
    "SRC4116_03_3629_law": (
        SOURCE_DIR / "P8_Y5_R2FR_3629_RESPONSE_DOUBLET_COUPLING_LAW.csv",
        "CL3629_3_zero_theorem_contract",
        "Response-doublet linearized source-coupling law.",
    ),
    "SRC4116_04_3629_zero_audit": (
        SOURCE_DIR / "P8_Y5_R2FR_3629_JZ_ZERO_ROUTE_AUDIT.csv",
        "JZR3629_5_verdict",
        "J_Z zero route audit: quotient descent, evenness, quadratic activation, current orthogonality, boundary.",
    ),
    "SRC4116_05_3629_coefficients": (
        SOURCE_DIR / "P8_Y5_R2FR_3629_JZ_COEFFICIENT_ROWS.csv",
        "JZC3629_8_R11_operator",
        "J_Z coefficient rows for PPN/Newton/R10/clock/WEP/Gdot/EM/R11.",
    ),
    "SRC4116_06_3629_decisions": (
        SOURCE_DIR / "P8_Y5_R2FR_3629_DECISION_GATES.csv",
        "DEC3629_3_next_target",
        "3629 decision selecting total-evenness/quotient-descent parent clause.",
    ),
    "SRC4116_07_3629_next": (
        SOURCE_DIR / "P8_Y5_R2FR_3629_NEXT_TARGET.csv",
        "3630-Y5-R2FR-parent-action-total-evenness-quotient-descent-or-JZ-bound-runner.md",
        "3629 next target: parent action total evenness and quotient descent or J_Z bound runner.",
    ),
    "SRC4116_08_script": (
        SCRIPT_PATH,
        "Y5_R2FR_4116_response_doublet_source_coupling_zero_or_coefficient.py",
        "Reproducible generator for this 4116 checkpoint.",
    ),
}


def row_base() -> dict:
    return {"timestamp_utc": TIMESTAMP, "branch_id": BRANCH_ID, "checkpoint_id": CHECKPOINT_ID}


def bool_string(value: bool) -> str:
    return "True" if value else "False"


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8-sig", errors="replace")


def parse_csv(path: Path) -> List[dict]:
    with path.open(newline="", encoding="utf-8-sig") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: List[dict]) -> None:
    if not rows:
        raise ValueError(f"no rows for {path}")
    path.parent.mkdir(parents=True, exist_ok=True)
    fieldnames: List[str] = []
    for row in rows:
        for key in row:
            if key not in fieldnames:
                fieldnames.append(key)
    with path.open("w", newline="", encoding="utf-8-sig") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def is_under(path: Path, parent: Path) -> bool:
    try:
        path.resolve().relative_to(parent.resolve())
        return True
    except ValueError:
        return False


def source_register_rows() -> List[dict]:
    rows = []
    for source_id, (path, needle, role) in LOCAL_SOURCES.items():
        text = read_text(path) if path.exists() else ""
        rows.append(
            {
                **row_base(),
                "source_id": source_id,
                "source_path": str(path),
                "exists": bool_string(path.exists()),
                "needle": needle,
                "needle_found": bool_string(path.exists() and needle in text),
                "role": role,
                "claim_allowed": bool_string(False),
                "valid_for_claim": bool_string(False),
            }
        )
    return rows


def coupling_law_rows() -> List[dict]:
    rows = [
        (
            "CL4116_0_total_action_split",
            "S_total=S_even[Z,g]+S_matter[g,Psi,Z]+S_source_norm[g,Z,Pi_M]+S_boundary[g,Z]",
            "F1=0 in S_even is not enough; any linear Z term from matter/source/boundary re-sources the local residual.",
            "DERIVED_STRUCTURE_IMPORTED",
        ),
        (
            "CL4116_1_linearized_Z_Euler",
            "L_AB Z^B + J_A + O(Z^2)=0; L_AB=-nabla_mu(H_AB nabla^mu)+M_AB",
            "Z=0 is an on-shell local solution only if J_A=0 and boundary natural source vanishes/fixes.",
            "EXACT_CONDITIONAL_COUPLING_LAW_IMPORTED",
        ),
        (
            "CL4116_2_residual_profile",
            "Z^A(x)=-(L^{-1})^{AB}J_B + boundary Green terms + O(J^2)",
            "If J_Z is nonzero, positive operator produces a finite local profile to score, not a plateau.",
            "PROFILE_BOUND_ROUTE_DERIVED",
        ),
        (
            "CL4116_3_zero_contract",
            "J_A=0 follows if every Z-coupled non-response piece descends to quotient, is even in Z, or starts at p>=2 with zero boundary source.",
            "The future parent action must satisfy this contract before local silence is derivable.",
            "ZERO_CONTRACT_WRITTEN_NOT_PARENT_SIGNED",
        ),
    ]
    return [
        {
            **row_base(),
            "law_id": law_id,
            "formula": formula,
            "meaning": meaning,
            "status": status,
            "source_id": "SRC4116_03_3629_law",
            "claim_allowed": bool_string(False),
            "valid_for_claim": bool_string(False),
        }
        for law_id, formula, meaning, status in rows
    ]


def zero_route_rows() -> List[dict]:
    rows = [
        ("JZR4116_0_quotient_descent", "Z^A vertical to quotient map and ordinary matter descends to Q_MTS", "J_A^matter=0 without tuning", "BEST_MATTER_ZERO_ROUTE_NOT_SIGNED"),
        ("JZR4116_1_Z2_even_total_action", "total local action invariant under Z -> -Z while observables are even", "all linear source terms vanish", "CANDIDATE_SYMMETRY_NOT_PARENT_DERIVED"),
        ("JZR4116_2_quadratic_activation", "memory/domain/source coupling begins at p>=2 in selector or response amplitude", "local zero kills stress value and Euler source at first order", "SUFFICIENT_CLAUSE_WRITTEN_NOT_ORIGIN_DERIVED"),
        ("JZR4116_3_charge_current_orthogonality", "extra charge/source channels have zero projection into observed Hamiltonian mass current", "mu_extra=0 before measured-GM fitting", "MASS_SOURCE_ZERO_ROUTE_NOT_SIGNED"),
        ("JZR4116_4_boundary_natural_source", "variation of S_boundary gives no natural boundary source and no linked-surface force flux", "bulk J_Z=0 is not spoiled by alpha3/source-normalization leakage", "BOUNDARY_SOURCE_OPEN"),
        ("JZR4116_5_verdict", "all matter, source-normalization, domain, memory, charge-current and boundary J_Z sources vanish as parent consequences", "response-doublet branch becomes real local-GR derivation route", "JZ_ZERO_NOT_CLAIMED_COEFFICIENT_BRANCH_REQUIRED"),
    ]
    return [
        {
            **row_base(),
            "route_id": route_id,
            "zero_condition": condition,
            "result_if_pass": result,
            "current_status": status,
            "source_id": "SRC4116_04_3629_zero_audit",
            "claim_allowed": bool_string(False),
            "valid_for_claim": bool_string(False),
        }
        for route_id, condition, result, status in rows
    ]


def coefficient_rows() -> List[dict]:
    rows = [
        ("JZC4116_0_gamma", "R3_gamma", "gamma_minus_1", "K_gamma_JZ * ||L^{-1}J_Z||_gamma", "MISSING_K_GAMMA_JZ_AND_L_INV_PROFILE", "PPN gamma bound row"),
        ("JZC4116_1_beta", "R4_beta", "beta_minus_1", "K_beta_JZ * ||L^{-1}J_Z||_beta + delta_beta_source", "MISSING_SECOND_ORDER_JZ_PROJECTION", "PPN beta/perihelion/LLR bound row"),
        ("JZC4116_2_preferred_frame", "R5_R6_R7_R8", "alpha1;alpha2;alpha3;xi", "P_PF(L^{-1}J_Z + boundary flux)", "MISSING_PREFERRED_FRAME_PROJECTION_AND_BOUNDS", "alpha_i/xi component bounds"),
        ("JZC4116_3_Newton_source", "R10_R11_Newton", "delta_Newton_MTS;alpha(lambda);mu_extra", "delta_mu_JZ=K_mu_JZ*Pi_M(L^{-1}J_Z)", "MISSING_SOURCE_MASS_AND_RANGE_PROFILE", "Newton/R10/source-normalization bounds"),
        ("JZC4116_4_clock", "R2_clock", "alpha_clock_redshift", "K_clock_JZ*frame_clock_projection(L^{-1}J_Z)", "MISSING_CLOCK_FRAME_PROJECTION", "clock/redshift bounds"),
        ("JZC4116_5_WEP_source", "R1_WEP_source_charge", "eta_source_AB", "Delta_AB ln mu_obs[J_Z]", "MISSING_SPECIES_SOURCE_COUPLING", "source-charge WEP bounds"),
        ("JZC4116_6_Gdot", "R9_Gdot", "Gdot_over_G", "partial_t ln mu_obs[J_Z]", "MISSING_TIME_DRIFT_SOURCE_PROJECTION", "local Gdot/ephemeris bounds"),
        ("JZC4116_7_EM_flux", "ENV3625_5_EM_source", "w_EM;Phi_EM_boundary", "K_EM_JZ*Poynting_or_bound_flux_projection", "MISSING_EM_FRACTION_OR_FLUX_NORMALIZATION", "EM/WEP/clock/orbital flux rows"),
        ("JZC4116_8_R11_operator", "R11_EH_operator_ledger", "non_EH_operator_coefficients", "c_JZ_operator_vector from retained L^{-1}J_Z operator family", "MISSING_EXECUTABLE_OPERATOR_VECTOR", "R11 coefficient vector bounds"),
    ]
    return [
        {
            **row_base(),
            "coupling_id": coupling_id,
            "target_row": target,
            "observable": observable,
            "prediction_template": prediction,
            "missing_input": missing,
            "required_bound_source": bound_source,
            "score_status": "not_scoreable",
            "source_id": "SRC4116_05_3629_coefficients",
            "claim_allowed": bool_string(False),
            "valid_for_claim": bool_string(False),
        }
        for coupling_id, target, observable, prediction, missing, bound_source in rows
    ]


def decision_rows() -> List[dict]:
    rows = [
        ("DEC4116_0_coupling_law", "The exact coupling obstruction is now in the active spine: even S_GK still fails if total action has linear J_Z source.", "DERIVATION_PROGRESS_IMPORTED", "use J_Z as canonical local source block"),
        ("DEC4116_1_best_zero_route", "Least-scrutiny zero route is quotient descent plus total evenness/quadratic activation.", "BEST_ROUTE_SELECTED_NOT_SIGNED", "attempt one parent action clause that signs all source pieces together"),
        ("DEC4116_2_current_claim", "J_Z=0 is not claimed because quotient matter descent, source normalization, charge-current orthogonality and boundary no-flux remain unsigned.", "NO_CLAIM", "retain coefficient rows for every local residual channel"),
        ("DEC4116_3_next", "Next target should merge quotient descent and quadratic activation into one parent-action clause, or demote J_Z to coefficient testing.", "NEXT_TARGET_SELECTED", "4117-Y5-R2FR-parent-action-total-evenness-quotient-descent-or-JZ-bound-runner.md"),
    ]
    return [
        {
            **row_base(),
            "decision_id": decision_id,
            "decision": decision,
            "status": status,
            "next_action": next_action,
            "claim_allowed": bool_string(False),
            "valid_for_claim": bool_string(False),
        }
        for decision_id, decision, status, next_action in rows
    ]


def next_target_rows() -> List[dict]:
    return [
        {
            **row_base(),
            "next_id": "NEXT4116_0",
            "target_doc": "4117-Y5-R2FR-parent-action-total-evenness-quotient-descent-or-JZ-bound-runner.md",
            "target_script": "scripts/Y5_R2FR_4117_parent_action_total_evenness_quotient_descent_or_JZ_bound_runner.py",
            "objective": "try to write the single parent-action clause that simultaneously signs quotient matter descent, total Z-evenness/quadratic activation, charge-current orthogonality, and boundary no-flux; if not, run J_Z coefficient-bound scaffolding",
            "success_gate": "J_Z=0 is parent-signed for matter, source-normalization, domain/memory, and boundary pieces, or every J_Z channel has a source-ready coefficient row with units, projection and local bound",
            "reason": "4116 shows coupling is the live bottleneck; 4117 must either turn the best route into a parent action clause or stop pretending it is derivable yet.",
            "claim_allowed": bool_string(False),
            "valid_for_claim": bool_string(False),
        }
    ]


def status_rows() -> List[dict]:
    return [
        {
            **row_base(),
            "status_id": "STATUS4116_0",
            "decision": DECISION,
            "strongest_result": "4116 imports the exact response-doublet source-coupling obstruction into the active spine: L_AB Z^B + J_A=0. The even double-zero action only gives local silence if the total matter/source/boundary action has J_Z=0.",
            "what_changed": "The coupling problem is now a concrete Euler source vector, not vague missing physics. If J_Z is nonzero, the profile is Z=-L^{-1}J_Z plus boundary terms and must be scored against local tests.",
            "still_missing": "parent-signed quotient descent, total Z-evenness/quadratic activation, charge-current orthogonality, boundary no-flux, projection coefficients and source-backed bounds",
            "claim_state": "no JZ_zero_local_GR_Newton_PPN_R10_R11_WEP_clock_Gdot_EM_source claim",
            "next_target": "4117 parent action total evenness quotient descent or JZ bound runner",
            "claim_allowed": bool_string(False),
            "valid_for_claim": bool_string(False),
        }
    ]


def generated_outputs() -> Dict[str, Path]:
    return {
        "P8_Y5_R2FR_4116_SOURCE_REGISTER": SOURCE_DIR / "P8_Y5_R2FR_4116_SOURCE_REGISTER.csv",
        "P8_Y5_R2FR_4116_JZ_COUPLING_LAW": SOURCE_DIR / "P8_Y5_R2FR_4116_JZ_COUPLING_LAW.csv",
        "P8_Y5_R2FR_4116_JZ_ZERO_ROUTE_AUDIT": SOURCE_DIR / "P8_Y5_R2FR_4116_JZ_ZERO_ROUTE_AUDIT.csv",
        "P8_Y5_R2FR_4116_JZ_COEFFICIENT_ROWS": SOURCE_DIR / "P8_Y5_R2FR_4116_JZ_COEFFICIENT_ROWS.csv",
        "P8_Y5_R2FR_4116_DECISION_GATE": SOURCE_DIR / "P8_Y5_R2FR_4116_DECISION_GATE.csv",
        "P8_Y5_R2FR_4116_NEXT_TARGET": SOURCE_DIR / "P8_Y5_R2FR_4116_NEXT_TARGET.csv",
        "P8_Y5_R2FR_4116_STATUS": SOURCE_DIR / "P8_Y5_R2FR_4116_STATUS.csv",
    }


def markdown_table(rows: List[dict], columns: List[str]) -> str:
    lines = ["| " + " | ".join(columns) + " |", "| " + " | ".join("---" for _ in columns) + " |"]
    for row in rows:
        lines.append("| " + " | ".join(str(row.get(column, "")).replace("\n", " ") for column in columns) + " |")
    return "\n".join(lines)


def write_doc() -> None:
    status = status_rows()[0]
    lines = [
        "# 4116 - response-doublet source coupling zero or coefficient",
        "",
        "## Verdict",
        "4116 imports the `3629` coupling result into the active `411x` spine. The bottleneck is now exact: for the even response-doublet branch, `L_AB Z^B + J_A = 0`, so double-zero silence requires `J_Z=0` for the total matter/source/boundary action.",
        "",
        "No `J_Z=0`, local-GR, Newton, PPN, R10/R11, WEP, clock, Gdot, or EM-source claim follows.",
        "",
        "## Strongest Current Result",
        f"- `{status['decision']}`",
        f"- {status['strongest_result']}",
        f"- {status['what_changed']}",
        "",
        "## Coupling Law",
        markdown_table(coupling_law_rows(), ["law_id", "formula", "meaning", "status"]),
        "",
        "## J_Z Zero Route Audit",
        markdown_table(zero_route_rows(), ["route_id", "zero_condition", "result_if_pass", "current_status"]),
        "",
        "## J_Z Coefficient Rows",
        markdown_table(coefficient_rows(), ["coupling_id", "target_row", "observable", "prediction_template", "missing_input", "score_status"]),
        "",
        "## Decisions",
        markdown_table(decision_rows(), ["decision_id", "decision", "status", "next_action"]),
        "",
        "## Next Target",
        markdown_table(next_target_rows(), ["target_doc", "target_script", "objective", "success_gate"]),
        "",
    ]
    DOC_PATH.write_text("\n".join(lines), encoding="utf-8")


def write_outputs() -> Dict[str, Path]:
    outputs = generated_outputs()
    write_csv(outputs["P8_Y5_R2FR_4116_SOURCE_REGISTER"], source_register_rows())
    write_csv(outputs["P8_Y5_R2FR_4116_JZ_COUPLING_LAW"], coupling_law_rows())
    write_csv(outputs["P8_Y5_R2FR_4116_JZ_ZERO_ROUTE_AUDIT"], zero_route_rows())
    write_csv(outputs["P8_Y5_R2FR_4116_JZ_COEFFICIENT_ROWS"], coefficient_rows())
    write_csv(outputs["P8_Y5_R2FR_4116_DECISION_GATE"], decision_rows())
    write_csv(outputs["P8_Y5_R2FR_4116_NEXT_TARGET"], next_target_rows())
    write_csv(outputs["P8_Y5_R2FR_4116_STATUS"], status_rows())
    write_doc()
    return outputs


def validate(outputs: Dict[str, Path]) -> List[dict]:
    checks: List[dict] = []

    def add(check_id: str, check: str, passed: bool, detail: str) -> None:
        checks.append({**row_base(), "check_id": check_id, "check": check, "passed": bool_string(passed), "detail": detail, "claim_allowed": bool_string(False)})

    missing_sources = [source_id for source_id, (path, _, _) in LOCAL_SOURCES.items() if not path.exists()]
    missing_needles = []
    for source_id, (path, needle, _) in LOCAL_SOURCES.items():
        if path.exists() and needle not in read_text(path):
            missing_needles.append(f"{source_id}:{needle}")
    add("VAL4116_0_sources_exist", "every local source path exists", not missing_sources, ";".join(missing_sources) or "all sources exist")
    add("VAL4116_1_sources_contain_needles", "every local source contains expected needle", not missing_needles, ";".join(missing_needles) or "all needles found")

    parse_ok = True
    parse_counts = {}
    for key, path in outputs.items():
        try:
            rows = parse_csv(path)
            parse_counts[key] = len(rows)
            parse_ok = parse_ok and len(rows) > 0
        except Exception as exc:
            parse_ok = False
            parse_counts[key] = repr(exc)
    add("VAL4116_2_csv_parse", "all generated CSV outputs parse and are nonempty", parse_ok, str(parse_counts))

    law_text = " ".join(" ".join(row.values()) for row in parse_csv(outputs["P8_Y5_R2FR_4116_JZ_COUPLING_LAW"]))
    law_ok = all(token in law_text for token in ["L_AB Z^B + J_A", "L^{-1}", "ZERO_CONTRACT_WRITTEN"])
    add("VAL4116_3_coupling_law", "J_Z coupling law and profile route present", law_ok, "coupling law tokens checked")

    zero_text = " ".join(" ".join(row.values()) for row in parse_csv(outputs["P8_Y5_R2FR_4116_JZ_ZERO_ROUTE_AUDIT"]))
    zero_ok = all(token in zero_text for token in ["quotient_descent", "Z2_even", "quadratic_activation", "BOUNDARY_SOURCE_OPEN", "JZ_ZERO_NOT_CLAIMED"])
    add("VAL4116_4_zero_routes", "J_Z zero routes and nonclaim verdict present", zero_ok, "zero route tokens checked")

    coeff_text = " ".join(" ".join(row.values()) for row in parse_csv(outputs["P8_Y5_R2FR_4116_JZ_COEFFICIENT_ROWS"]))
    coeff_ok = all(token in coeff_text for token in ["gamma_minus_1", "beta_minus_1", "alpha1;alpha2;alpha3;xi", "Gdot_over_G", "non_EH_operator_coefficients"])
    add("VAL4116_5_coefficients", "J_Z coefficient rows cover local test arenas", coeff_ok, "coefficient tokens checked")

    next_rows = parse_csv(outputs["P8_Y5_R2FR_4116_NEXT_TARGET"])
    next_ok = len(next_rows) == 1 and next_rows[0].get("target_doc") == "4117-Y5-R2FR-parent-action-total-evenness-quotient-descent-or-JZ-bound-runner.md"
    add("VAL4116_6_next_target", "next target is 4117 parent-action J_Z route", next_ok, str(next_rows))

    status_rows_local = parse_csv(outputs["P8_Y5_R2FR_4116_STATUS"])
    status_ok = bool(status_rows_local) and status_rows_local[0].get("decision") == DECISION and "no JZ" in status_rows_local[0].get("claim_state", "")
    add("VAL4116_7_status", "status records J_Z law and no-claim state", status_ok, "status row checked")

    all_rows = []
    for path in outputs.values():
        all_rows.extend(parse_csv(path))
    no_claim = all(row.get("claim_allowed") in ("False", "") for row in all_rows)
    add("VAL4116_8_no_claim_flags", "all generated rows remain no-claim", no_claim, f"row_count={len(all_rows)}")

    output_paths = list(outputs.values()) + [DOC_PATH]
    in_scope = all(is_under(path, ROOT) for path in output_paths)
    formalization_output = any(is_under(path, FORMALIZATION) for path in output_paths)
    formalization_touched = False
    if FORMALIZATION.exists():
        formalization_touched = any(FORMALIZATION.rglob("*R2FR_4116*")) or any(FORMALIZATION.rglob("4116-Y5-R2FR*"))
    add("VAL4116_9_scope", "outputs stay in post-checkpoint-work and not formalization-workbench", in_scope and not formalization_output and not formalization_touched, f"doc={DOC_PATH}; csv_count={len(outputs)}")

    compile_ok = True
    compile_detail = "py_compile ok"
    try:
        py_compile.compile(str(SCRIPT_PATH), doraise=True)
    except Exception as exc:
        compile_ok = False
        compile_detail = repr(exc)
    add("VAL4116_10_compile", "generator script compiles", compile_ok, compile_detail)
    return checks


def main() -> None:
    outputs = write_outputs()
    validation_rows = validate(outputs)
    validation_path = SOURCE_DIR / "P8_Y5_BRR545_4116_VALIDATION.csv"
    write_csv(validation_path, validation_rows)
    pycache = SCRIPT_PATH.parent / "__pycache__"
    if pycache.exists():
        shutil.rmtree(pycache)

    failed = [row for row in validation_rows if row["passed"] != "True"]
    print(f"wrote: {DOC_PATH}")
    for path in outputs.values():
        print(f"wrote: {path}")
    print(f"validation: {validation_path}")
    if failed:
        print("failed checks:")
        for row in failed:
            print(f"- {row['check_id']}: {row['detail']}")
        raise SystemExit(1)
    print("all validation checks passed")


if __name__ == "__main__":
    main()

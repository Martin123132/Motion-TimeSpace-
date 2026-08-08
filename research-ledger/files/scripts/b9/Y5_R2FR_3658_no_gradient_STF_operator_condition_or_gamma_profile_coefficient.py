from __future__ import annotations

import csv
import sys
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
RESIDUALS = ROOT / "source-intake" / "mts_residuals"
LOCAL_BOUNDS = ROOT / "source-intake" / "local_bounds"
FORMALIZATION = ROOT.parent / "formalization-workbench"
CHECKPOINT_ID = "3658"
BRANCH_ID = "MTS_R2FR_Y5_NO_GRADIENT_STF_OPERATOR_CONDITION_OR_GAMMA_PROFILE_COEFFICIENT_3658"
DOC = ROOT / "3658-Y5-R2FR-no-gradient-STF-operator-condition-or-gamma-profile-coefficient.md"


def stamp() -> str:
    return datetime.now(timezone.utc).isoformat()


def base(ts: str) -> dict[str, object]:
    return {
        "timestamp_utc": ts,
        "branch_id": BRANCH_ID,
        "checkpoint_id": CHECKPOINT_ID,
        "valid_for_claim": False,
    }


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace") if path.exists() else ""


def load_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fields: list[str] = []
    for row in rows:
        for key in row:
            if key not in fields:
                fields.append(key)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def parse_float(value: object) -> float | None:
    try:
        return float(str(value).strip())
    except ValueError:
        return None


def source_register(ts: str) -> list[dict[str, object]]:
    specs = [
        ("next_3657", RESIDUALS / "P8_Y5_R2FR_3657_NEXT_TARGET.csv", "no-gradient", "3657 selected no-gradient/profile target"),
        ("proof_3657", RESIDUALS / "P8_Y5_R2FR_3657_STF_ZERO_PROOF_ATTEMPT.csv", "X_prime", "radial STF counterexample"),
        ("bounds_3657", RESIDUALS / "P8_Y5_R2FR_3657_GAMMA_COEFFICIENT_BOUND_ROWS.csv", "C_gradient_TF_gamma", "gamma coefficient bound rows"),
        ("delta_3657", RESIDUALS / "P8_Y5_R2FR_3657_DELTA_GAMMA_STATUS_ROWS.csv", "S_TF_MTS", "delta gamma status"),
        ("validation_3657", RESIDUALS / "P8_Y5_BRR545_3657_VALIDATION.csv", "VAL3657_7_gamma_bound_numeric", "3657 validation"),
        ("local_bounds_R3", LOCAL_BOUNDS / "local_bound_claims.csv", "R3_gamma", "Cassini gamma bound anchor"),
        ("motion_load_02", ROOT / "02-motion-load-local-GR-reduction.md", "conditional on accepting", "conditional local-GR route"),
        ("EH_ledger_425", ROOT / "425-EH-operator-retained-ledger-and-source-normalization-test-plan.md", "same-frame EH/source premises", "EH/source premise ledger"),
        ("weak_field_3652", ROOT / "3652-Y5-R2FR-weak-field-source-Hamiltonian-GM-calibration-or-source-vector-bound.md", "delta ln mu_obs", "weak-field residual law"),
        ("local_GR_3653", ROOT / "3653-Y5-R2FR-Newton-Poisson-PPN-zero-vector-gate-or-local-GR-residual-fit.md", "delta_gamma_MTS", "local gamma residual interface"),
    ]
    rows = []
    for source_id, path, needle, role in specs:
        body = read_text(path)
        rows.append(
            {
                **base(ts),
                "source_id": source_id,
                "path": str(path),
                "exists": path.exists(),
                "needle": needle,
                "needle_found": needle in body,
                "role": role,
            }
        )
    return rows


def radial_stf_derivation_rows(ts: str) -> list[dict[str, object]]:
    return [
        {
            **base(ts),
            "derivation_id": "RSD3658_0_radial_hessian",
            "object": "radial profile Hessian STF",
            "statement": "For X=X(r), partial_i partial_j X = X_second n_i n_j + (X_prime/r)(delta_ij-n_i n_j), so the STF Hessian amplitude is X_second-X_prime/r.",
            "formula": "P_TF[partial_i partial_j X]=(X_second-X_prime/r)(n_i n_j-delta_ij/3)",
            "result_status": "RADIAL_STF_FORMULA_DERIVED",
            "claim_allowed": False,
        },
        {
            **base(ts),
            "derivation_id": "RSD3658_1_hessian_zero_solution",
            "object": "Hessian STF zero ODE",
            "statement": "The no-Hessian-STF equation X_second-X_prime/r=0 integrates to X_prime=C*r and X=X0+C*r^2/2.",
            "formula": "X_second-X_prime/r=0 => X=X0+C*r^2/2",
            "result_status": "NO_HESSIAN_STF_PROFILE_LAW_DERIVED",
            "claim_allowed": False,
        },
        {
            **base(ts),
            "derivation_id": "RSD3658_2_gradient_square_survival",
            "object": "gradient-square STF term",
            "statement": "Even when the Hessian STF vanishes, P_TF[partial_iX partial_jX]=X_prime^2(n_i n_j-delta_ij/3)=C^2*r^2(n_i n_j-delta_ij/3), so the gradient-square piece vanishes only if C=0.",
            "formula": "P_TF[partial_iX partial_jX]=C^2*r^2(n_i n_j-delta_ij/3)",
            "result_status": "GRADIENT_SQUARE_FORCES_CONSTANT_BRANCH",
            "claim_allowed": False,
        },
        {
            **base(ts),
            "derivation_id": "RSD3658_3_no_growing_branch",
            "object": "local vacuum/asymptotic condition",
            "statement": "If the local branch forbids the growing r^2 extra-field mode, then C=0, X=X0, and both Hessian-STF and gradient-square-STF terms vanish.",
            "formula": "no_growing_r2_mode and X_second-X_prime/r=0 => X_prime=0 => P_TF[partial_i partial_j X]=P_TF[partial_iX partial_jX]=0",
            "result_status": "CONDITIONAL_NO_GRADIENT_ZERO_THEOREM_DERIVED",
            "claim_allowed": False,
        },
        {
            **base(ts),
            "derivation_id": "RSD3658_4_verdict",
            "object": "parent signature status",
            "statement": "The mathematics gives a real route to zero, but MTS still needs the parent local-vacuum condition that removes growing r^2 or Yukawa-like local extra profiles.",
            "formula": "parent_local_vacuum_constant_field_clause required before delta_gamma_MTS=0",
            "result_status": "PARENT_NO_GRADIENT_CLAUSE_UNSIGNED",
            "claim_allowed": False,
        },
    ]


def gamma_profile_coefficient_rows(ts: str) -> list[dict[str, object]]:
    gamma = next(row for row in load_csv(LOCAL_BOUNDS / "local_bound_claims.csv") if row["row_id"] == "R3_gamma")
    upper = parse_float(gamma["upper_bound"])
    return [
        {
            **base(ts),
            "profile_id": "GPC3658_0_constant_branch",
            "profile": "X(r)=X0",
            "Hessian_STF_amplitude": "0",
            "gradient_square_STF_amplitude": "0",
            "gamma_coefficient_formula": "C_gradient_TF_gamma=0",
            "required_bound": upper,
            "units": gamma["units"],
            "source_row": "R3_gamma",
            "profile_status": "THEOREM_ZERO_IF_PARENT_SIGNS_CONSTANT_LOCAL_FIELD_BRANCH",
            "score_ready": False,
            "claim_allowed": False,
        },
        {
            **base(ts),
            "profile_id": "GPC3658_1_no_Hessian_STF_growing_branch",
            "profile": "X(r)=X0+C*r^2/2",
            "Hessian_STF_amplitude": "0",
            "gradient_square_STF_amplitude": "C^2*r^2",
            "gamma_coefficient_formula": "C_gradient_TF_gamma(r)=|k_G|*C^2*r^2/|Phi_N(r)|",
            "required_bound": upper,
            "units": gamma["units"],
            "source_row": "R3_gamma",
            "profile_status": "NOT_ZERO_UNLESS_C_EQUALS_ZERO_OR_kG_EQUALS_ZERO",
            "score_ready": False,
            "claim_allowed": False,
        },
        {
            **base(ts),
            "profile_id": "GPC3658_2_Yukawa_like_profile",
            "profile": "X(r)=A_X*exp(-r/lambda_X)/r",
            "Hessian_STF_amplitude": "A_X*exp(-r/lambda_X)*(3/r^3+3/(lambda_X*r^2)+1/(lambda_X^2*r))",
            "gradient_square_STF_amplitude": "A_X^2*exp(-2*r/lambda_X)*(1/r^2+1/(lambda_X*r))^2",
            "gamma_coefficient_formula": "C_gradient_TF_gamma(r)=|k_H|*|A_X|*exp(-r/lambda_X)*(3/r^3+3/(lambda_X*r^2)+1/(lambda_X^2*r))/|Phi_N(r)| + |k_G|*A_X^2*exp(-2*r/lambda_X)*(1/r^2+1/(lambda_X*r))^2/|Phi_N(r)|",
            "required_bound": upper,
            "units": gamma["units"],
            "source_row": "R3_gamma",
            "profile_status": "PROFILE_COEFFICIENT_FORMULA_DERIVED_INPUTS_MISSING",
            "score_ready": False,
            "claim_allowed": False,
        },
        {
            **base(ts),
            "profile_id": "GPC3658_3_generic_bound_inequality",
            "profile": "generic radial local extra field",
            "Hessian_STF_amplitude": "|X_second-X_prime/r|",
            "gradient_square_STF_amplitude": "|X_prime|^2",
            "gamma_coefficient_formula": "(|k_H|*|X_second-X_prime/r| + |k_G|*|X_prime|^2 + |C_nonEH_other| + |C_boundary| + |C_readout| + |C_source|)/|Phi_N| <= 2.3e-05",
            "required_bound": upper,
            "units": gamma["units"],
            "source_row": "R3_gamma",
            "profile_status": "GENERAL_PROFILE_BOUND_INTERFACE_DERIVED",
            "score_ready": False,
            "claim_allowed": False,
        },
    ]


def gamma_score_interface_rows(ts: str) -> list[dict[str, object]]:
    return [
        {
            **base(ts),
            "interface_id": "GSI3658_0_no_gradient_zero_route",
            "object": "delta_gamma_MTS",
            "route": "parent signs local constant-field/no-growing-r2/no-Yukawa-profile condition",
            "result_if_signed": "delta_gamma_MTS=0 from S_TF_MTS=0 plus readout/source/boundary silence",
            "current_status": "CONDITIONAL_ROUTE_DERIVED_PARENT_UNSIGNED",
            "claim_allowed": False,
        },
        {
            **base(ts),
            "interface_id": "GSI3658_1_profile_bound_route",
            "object": "C_gradient_TF_gamma",
            "route": "source local field amplitude A_X, range lambda_X, and operator coefficients k_H,k_G",
            "result_if_signed": "evaluate profile coefficient against C_gamma_TF_total<=2.3e-5",
            "current_status": "FORMULA_READY_NUMERIC_INPUTS_MISSING",
            "claim_allowed": False,
        },
    ]


def claim_gate_rows(ts: str) -> list[dict[str, object]]:
    specs = [
        ("CG3658_0_radial_ode", "radial Hessian-STF zero law solved", "PASSED_DERIVATION", "X_second-X_prime/r=0 gives X=X0+C*r^2/2"),
        ("CG3658_1_constant_needed", "gradient-square STF forces C=0 unless its coefficient is zero", "PASSED_DERIVATION", "no-gradient condition is stronger than no-Hessian-STF"),
        ("CG3658_2_profile_formula", "Yukawa/generic gamma profile coefficient formula written", "PASSED_FORMULA_GATE", "the gamma branch now has amplitude/range inputs to acquire"),
        ("CG3658_3_no_claim", "no gamma/local-GR pass claimed", "ACTIVE_GUARD", "parent constant-field clause and numeric inputs remain missing"),
        ("CG3658_4_next", "next step must sign constant local field branch or source A_X/lambda_X/k coefficients", "CONSTANT_FIELD_OR_PROFILE_INPUT_NEXT", "this is the shortest route to score delta_gamma_MTS"),
    ]
    return [
        {
            **base(ts),
            "gate_id": gate_id,
            "gate": gate,
            "status": status,
            "reason": reason,
            "claim_allowed": False,
        }
        for gate_id, gate, status, reason in specs
    ]


def status_rows(ts: str) -> list[dict[str, object]]:
    return [
        {
            **base(ts),
            "status": "RADIAL_NO_STF_LAW_DERIVED_PROFILE_COEFFICIENT_FORMULA_READY",
            "summary": "3658 derives the radial no-STF law: Hessian-STF zero gives X=X0+C*r^2/2, but gradient-square STF forces C=0 for a true no-gradient local branch; it also writes the Yukawa/generic gamma profile coefficient formula.",
            "claim_ceiling": "no MTS gamma prediction, local-GR pass, PPN pass, Newtonian pass, source-calibration pass, WEP/R10/clock/orbital pass, or EH-dominance pass is claimed",
            "useful_result": "The gamma residual can now close only by a parent constant-field/no-growing-profile theorem or by sourcing A_X, lambda_X, k_H, and k_G for the profile coefficient bound.",
        }
    ]


def next_rows(ts: str) -> list[dict[str, object]]:
    return [
        {
            **base(ts),
            "next_id": "NEXT3658_0",
            "target_doc": "3659-Y5-R2FR-parent-local-constant-field-theorem-or-profile-input-acquisition.md",
            "target_script": "scripts/Y5_R2FR_3659_parent_local_constant_field_theorem_or_profile_input_acquisition.py",
            "objective": "try to derive the parent local constant-field/no-growing-profile theorem; if it fails, acquire or define nonclaim inputs A_X, lambda_X, k_H, k_G for the gamma profile bound",
            "success_gate": "delta_gamma_MTS is either theorem-zero under a signed local constant-field branch or has all symbolic profile inputs registered with source/provenance placeholders refused as claims",
        }
    ]


def write_doc(sources, derivation, profiles, interfaces, gates, status_rows_, next_target) -> None:
    lines = [
        "# 3658 - No-gradient STF operator condition or gamma profile coefficient",
        "",
        f"**Status:** {status_rows_[0]['summary']}",
        "",
        f"**Claim ceiling:** {status_rows_[0]['claim_ceiling']}.",
        "",
        "## Main result",
        "",
        "This checkpoint turns the trace-free gamma obstruction into a radial profile law.",
        "",
        "For a radial local field `X(r)`,",
        "",
        "`P_TF[partial_i partial_j X] = (X_second-X_prime/r)(n_i n_j-delta_ij/3)`.",
        "",
        "Setting this to zero gives",
        "",
        "`X_second-X_prime/r=0 => X = X0 + C*r^2/2`.",
        "",
        "But the gradient-square part is",
        "",
        "`P_TF[partial_i X partial_j X] = C^2*r^2(n_i n_j-delta_ij/3)`.",
        "",
        "So a true no-STF local branch needs `C=0`, unless the parent action separately kills the gradient-square coefficient. In plain English: no growing `r^2` mode, no local Yukawa/radial profile, or no gamma pass.",
        "",
        "## Radial derivation rows",
    ]
    for row in derivation:
        lines.append(f"- `{row['derivation_id']}`: {row['result_status']} - `{row['formula']}`")
    lines.extend(["", "## Gamma profile coefficient rows"])
    for row in profiles:
        lines.append(f"- `{row['profile_id']}`: `{row['profile']}` - {row['profile_status']}")
    lines.extend(["", "## Score interfaces"])
    for row in interfaces:
        lines.append(f"- `{row['interface_id']}`: {row['current_status']} - {row['route']}")
    lines.extend(["", "## Claim gates"])
    for row in gates:
        lines.append(f"- `{row['gate_id']}`: {row['status']} - {row['gate']}")
    lines.extend(["", "## Next checkpoint", ""])
    lines.append(f"`{next_target[0]['target_doc']}` via `{next_target[0]['target_script']}`.")
    lines.extend(["", "## Sources"])
    for row in sources:
        lines.append(f"- `{row['source_id']}`: `{row['path']}` exists={row['exists']} needle_found={row['needle_found']}")
    DOC.write_text("\n".join(lines) + "\n", encoding="utf-8")


def parse_csv(path: Path) -> tuple[bool, int]:
    try:
        with path.open("r", newline="", encoding="utf-8") as handle:
            rows = list(csv.DictReader(handle))
        return True, len(rows)
    except Exception:
        return False, 0


def validate(ts, output_paths, sources, derivation, profiles, interfaces, gates, status_rows_, next_target) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []

    def add(validation_id: str, ok: bool, detail: str) -> None:
        rows.append(
            {
                "timestamp_utc": ts,
                "branch_id": BRANCH_ID,
                "checkpoint_id": CHECKPOINT_ID,
                "validation_id": validation_id,
                "result": "PASS" if ok else "FAIL",
                "detail": detail,
            }
        )

    add("VAL3658_0_sources_exist", all(row["exists"] for row in sources), "every cited local source path exists")
    add("VAL3658_1_needles_found", all(row["needle_found"] for row in sources), "every source needle found")
    add("VAL3658_2_outputs_exist", all(path.exists() for path in output_paths), "all expected 3658 outputs written")
    csv_status = [parse_csv(path) for path in output_paths if path.suffix.lower() == ".csv"]
    add("VAL3658_3_csv_parse", all(ok and count > 0 for ok, count in csv_status), "all generated CSVs parse with rows")
    add("VAL3658_4_hessian_zero_solution", any("X=X0+C*r^2/2" in row["formula"] for row in derivation), "radial Hessian-STF ODE solution recorded")
    add("VAL3658_5_gradient_square_forces_constant", any("C^2*r^2" in row["formula"] for row in derivation), "gradient-square obstruction recorded")
    add("VAL3658_6_conditional_zero_theorem", any(row["result_status"] == "CONDITIONAL_NO_GRADIENT_ZERO_THEOREM_DERIVED" for row in derivation), "conditional no-gradient zero theorem derived")
    add("VAL3658_7_yukawa_profile_formula", any(row["profile_id"] == "GPC3658_2_Yukawa_like_profile" and "lambda_X" in row["gamma_coefficient_formula"] for row in profiles), "Yukawa profile coefficient formula written")
    add("VAL3658_8_generic_bound_interface", any(row["profile_id"] == "GPC3658_3_generic_bound_inequality" and parse_float(row["required_bound"]) == 2.3e-05 for row in profiles), "generic profile bound tied to Cassini gamma")
    add("VAL3658_9_no_score_ready", not any(str(row.get("score_ready", "")).lower() == "true" for row in profiles), "profile rows remain nonclaim and not score-ready")
    add("VAL3658_10_interfaces_present", {"GSI3658_0_no_gradient_zero_route", "GSI3658_1_profile_bound_route"}.issubset({row["interface_id"] for row in interfaces}), "zero and profile routes present")
    add("VAL3658_11_claim_gates_present", {"CG3658_0_radial_ode", "CG3658_1_constant_needed", "CG3658_2_profile_formula", "CG3658_3_no_claim", "CG3658_4_next"}.issubset({row["gate_id"] for row in gates}), "core claim gates present")
    generated = sources + derivation + profiles + interfaces + gates + status_rows_ + next_target
    add("VAL3658_12_all_nonclaim", not any(str(row.get("valid_for_claim", "")).lower() == "true" or str(row.get("claim_allowed", "")).lower() == "true" for row in generated), "all generated rows remain nonclaim")
    doc_text = read_text(DOC)
    add("VAL3658_13_doc_written", "X = X0 + C*r^2/2" in doc_text and "C=0" in doc_text and "no gamma pass" in doc_text, "doc records no-gradient profile law")
    leaks: list[Path] = []
    if FORMALIZATION.exists():
        for pattern in ["*Y5_R2FR_3658*", "3658-Y5-R2FR-*", "Y5_R2FR_3658_*"]:
            leaks.extend(FORMALIZATION.rglob(pattern))
    add("VAL3658_14_no_formalization_leak", not leaks, "no 3658 checkpoint files in formalization-workbench")
    add("VAL3658_15_next_target", next_target[0]["target_doc"].startswith("3659-") and "constant-field" in next_target[0]["target_doc"], "3659 constant-field/profile input target selected")
    return rows


def main() -> int:
    ts = stamp()
    RESIDUALS.mkdir(parents=True, exist_ok=True)
    sources = source_register(ts)
    derivation = radial_stf_derivation_rows(ts)
    profiles = gamma_profile_coefficient_rows(ts)
    interfaces = gamma_score_interface_rows(ts)
    gates = claim_gate_rows(ts)
    status_rows_ = status_rows(ts)
    next_target = next_rows(ts)
    outputs = {
        "sources": RESIDUALS / "P8_Y5_R2FR_3658_SOURCE_REGISTER.csv",
        "derivation": RESIDUALS / "P8_Y5_R2FR_3658_RADIAL_STF_DERIVATION_ROWS.csv",
        "profiles": RESIDUALS / "P8_Y5_R2FR_3658_GAMMA_PROFILE_COEFFICIENT_ROWS.csv",
        "interfaces": RESIDUALS / "P8_Y5_R2FR_3658_GAMMA_SCORE_INTERFACE_ROWS.csv",
        "gates": RESIDUALS / "P8_Y5_R2FR_3658_CLAIM_GATES.csv",
        "status": RESIDUALS / "P8_Y5_R2FR_3658_STATUS.csv",
        "next": RESIDUALS / "P8_Y5_R2FR_3658_NEXT_TARGET.csv",
        "validation": RESIDUALS / "P8_Y5_BRR545_3658_VALIDATION.csv",
    }
    write_csv(outputs["sources"], sources)
    write_csv(outputs["derivation"], derivation)
    write_csv(outputs["profiles"], profiles)
    write_csv(outputs["interfaces"], interfaces)
    write_csv(outputs["gates"], gates)
    write_csv(outputs["status"], status_rows_)
    write_csv(outputs["next"], next_target)
    write_doc(sources, derivation, profiles, interfaces, gates, status_rows_, next_target)
    generated_paths = [path for key, path in outputs.items() if key != "validation"] + [DOC]
    validation = validate(ts, generated_paths, sources, derivation, profiles, interfaces, gates, status_rows_, next_target)
    write_csv(outputs["validation"], validation)
    failures = [row for row in validation if row["result"] != "PASS"]
    if failures:
        print(f"3658 validation failed: {failures}", file=sys.stderr)
        return 1
    print(f"wrote 3658 checkpoint with {len(validation)} validation checks")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

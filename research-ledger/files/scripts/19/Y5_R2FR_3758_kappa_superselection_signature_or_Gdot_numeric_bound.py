import csv
import math
import shutil
from datetime import datetime, timezone
from pathlib import Path


CHECKPOINT = "3758"
BRANCH = "MTS_R2FR_Y5_KAPPA_SUPERSELECTION_SIGNATURE_OR_GDOT_NUMERIC_BOUND_3758"
PCW = Path(
    r"D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work"
)
RESIDUALS = PCW / "source-intake" / "mts_residuals"
FORMALIZATION = PCW.parent / "formalization-workbench"
DOC_PATH = PCW / "3758-Y5-R2FR-kappa-superselection-signature-or-Gdot-numeric-bound.md"


OUTPUTS = {
    "sources": RESIDUALS / "P8_Y5_R2FR_3758_SOURCE_REGISTER.csv",
    "quotient_law": RESIDUALS / "P8_Y5_R2FR_3758_KAPPA_QUOTIENT_FLUX_LAW.csv",
    "signature_contract": RESIDUALS / "P8_Y5_R2FR_3758_KAPPA_SUPERSELECTION_ACTION_CONTRACT.csv",
    "gdot_bound": RESIDUALS / "P8_Y5_R2FR_3758_GDOT_BOUND_EVALUATION.csv",
    "runner_patch": RESIDUALS / "P8_Y5_R2FR_3758_COUPLING_RUNNER_PATCH.csv",
    "claim_gates": RESIDUALS / "P8_Y5_R2FR_3758_CLAIM_GATES.csv",
    "decision_rows": RESIDUALS / "P8_Y5_R2FR_3758_DECISION_ROWS.csv",
    "next_target": RESIDUALS / "P8_Y5_R2FR_3758_NEXT_TARGET.csv",
    "status": RESIDUALS / "P8_Y5_R2FR_3758_STATUS.csv",
    "validation": RESIDUALS / "P8_Y5_BRR545_3758_VALIDATION.csv",
}


def stamp() -> str:
    return datetime.now(timezone.utc).isoformat()


def base(timestamp: str, valid_for_claim: bool = False) -> dict[str, object]:
    return {
        "timestamp_utc": timestamp,
        "branch_id": BRANCH,
        "checkpoint_id": CHECKPOINT,
        "valid_for_claim": valid_for_claim,
    }


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        raise ValueError(f"refusing to write empty csv: {path}")
    fields: list[str] = []
    for row in rows:
        for key in row:
            if key not in fields:
                fields.append(key)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def source_paths() -> dict[str, Path]:
    return {
        "SRC3758_0_3757_doc": PCW / "3757-Y5-R2FR-first-coupling-runner-fill-or-side-flux-zero-proof.md",
        "SRC3758_1_3757_side_flux": RESIDUALS / "P8_Y5_R2FR_3757_SIDE_FLUX_ZERO_THEOREM.csv",
        "SRC3758_2_3757_gdot_fill": RESIDUALS / "P8_Y5_R2FR_3757_GDOT_CONDITIONAL_FILL.csv",
        "SRC3758_3_3757_parent_premises": RESIDUALS / "P8_Y5_R2FR_3757_PARENT_PREMISE_SIGNATURES.csv",
        "SRC3758_4_3757_runner_patch": RESIDUALS / "P8_Y5_R2FR_3757_COUPLING_RUNNER_PATCH.csv",
        "SRC3758_5_3756_exchange": RESIDUALS / "P8_Y5_R2FR_3756_PROJECTED_EXCHANGE_CLAUSES.csv",
        "SRC3758_6_3755_kappa": RESIDUALS / "P8_Y5_R2FR_3755_KAPPA_THEOREM_ROWS.csv",
        "SRC3758_7_3754_flux_law": RESIDUALS / "P8_Y5_R2FR_3754_SOURCE_WARD_FLUX_LAW_ROWS.csv",
        "SRC3758_8_meff_flux_map": RESIDUALS / "P8_SOURCE_MEASURE_MEFF_FLUX_RESIDUAL_MAP.csv",
        "SRC3758_9_gm_matrix": RESIDUALS / "P8_CONSTANT_GM_RESIDUAL_BOUND_MATRIX.csv",
        "SRC3758_10_delta_kappa_exchange": RESIDUALS / "P8_delta_kappa_source_exchange_residual.csv",
        "SRC3758_11_local_bounds": PCW / "source-intake" / "local_bounds" / "local_bound_claims.csv",
    }


def source_register(timestamp: str) -> list[dict[str, object]]:
    return [
        {
            **base(timestamp),
            "source_id": source_id,
            "source_path": str(path),
            "source_exists": path.exists(),
            "role": "3758 kappa/Gdot derivation input",
        }
        for source_id, path in source_paths().items()
    ]


def quotient_law_rows(timestamp: str) -> list[dict[str, object]]:
    entries = [
        (
            "KQ3758_0_definition",
            "kappa_eff := kappa_* C_G/C_M with C_G=ell_G(J_G), C_M=ell_M(J_M), and kappa_* a parent normalization.",
            "This is a source-coupling quotient ansatz/contract, not yet an adopted parent action term.",
            "ACTION_SIGNATURE_READY_NOT_ADOPTED",
            False,
        ),
        (
            "KQ3758_1_log_derivative",
            "d_t ln kappa_eff = d_t ln kappa_* + d_t ln C_G - d_t ln C_M.",
            "Exact for nonzero C_G and C_M.",
            "EXACT_QUOTIENT_IDENTITY",
            True,
        ),
        (
            "KQ3758_2_charge_flux_substitution",
            "d_t ln C_X = (-Phi_X + int_W Pi_X q_X)/(C_X Delta t) for X in {G,M}.",
            "Imported from the 3754/3757 Ward/Stokes flux balance.",
            "EXACT_FLUX_SUBSTITUTION",
            True,
        ),
        (
            "KQ3758_3_no_cancellation_bound",
            "|d_t ln kappa_eff| <= |d_t ln kappa_*| + |R_G| + |R_M|, where R_X := (-Phi_X + int_W Pi_X q_X)/(C_X Delta t).",
            "Uses absolute components; no tuned cancellation between gravitational and matter charge drift.",
            "BOUND_DERIVED",
            True,
        ),
        (
            "KQ3758_4_superselection_zero",
            "If kappa_* is global, C_G and C_M are cap-conserved, and Pi_X q_X/Phi_X vanish in the local tube, then d_t ln kappa_eff=0.",
            "This is the parent-signature route to Gdot=0.",
            "EXACT_CONDITIONAL_ZERO_THEOREM",
            False,
        ),
        (
            "KQ3758_5_Geff_bridge",
            "d_t ln G_eff = d_t ln kappa_eff + d_t ln Z_Poisson + d_t ln Z_frame.",
            "Z_Poisson and Z_frame carry calibration/frame residuals; they must be zeroed or bounded separately.",
            "EXACT_LOCAL_CALIBRATION_DECOMPOSITION",
            True,
        ),
        (
            "KQ3758_6_Gdot_bound",
            "|d_t ln kappa_*| + |R_G| + |R_M| + |d_t ln Z_Poisson| + |d_t ln Z_frame| <= 9.6e-15 yr^-1.",
            "This is the numeric requirement if the zero theorem is not parent-signed.",
            "NUMERIC_RESIDUAL_REQUIREMENT_DERIVED",
            True,
        ),
    ]
    return [
        {
            **base(timestamp),
            "law_id": law_id,
            "law_or_derivation": law_or_derivation,
            "premise_or_note": premise_or_note,
            "status": status,
            "derived_inside_3758": derived,
            "parent_signed": False if not derived else "identity_or_imported",
            "claim_allowed": False,
        }
        for law_id, law_or_derivation, premise_or_note, status, derived in entries
    ]


def signature_contract_rows(timestamp: str) -> list[dict[str, object]]:
    entries = [
        (
            "KS3758_0_global_block",
            "Parent configuration space must split as Q_parent = Q_dyn x K_global with kappa_* in K_global.",
            "This makes local variations delta kappa_*=0 by construction.",
            "REQUIRED_FOR_ZERO_ROUTE",
        ),
        (
            "KS3758_1_no_local_kappa_field",
            "The local action must not contain an independently propagating kappa(x) field in the Newton/PPN sector.",
            "Otherwise d_t ln kappa_eff is a live scalar residual.",
            "REQUIRED_FOR_ZERO_ROUTE",
        ),
        (
            "KS3758_2_charge_quotient_owner",
            "The action must state whether kappa_eff is fundamental, or the quotient kappa_* C_G/C_M is the emergent coupling.",
            "Without this, Gdot zero is only a calibration assumption.",
            "REQUIRED_PARENT_CHOICE",
        ),
        (
            "KS3758_3_cap_conservation",
            "The source/gravity charges C_M and C_G must be conserved in the local tube.",
            "This imports the 3757 side-flux and projected-exchange clauses.",
            "REQUIRED_FOR_ZERO_ROUTE",
        ),
        (
            "KS3758_4_poisson_frame_silence",
            "Poisson calibration and source/frame normalization factors must have no local drift or must be separately bounded.",
            "This prevents hiding Gdot in Z_Poisson or Z_frame.",
            "REQUIRED_FOR_LOCAL_GR_ROUTE",
        ),
        (
            "KS3758_5_absolute_G_policy",
            "Even if d_t G_eff=0 is derived, the absolute value of measured G is not derived until kappa_* or the charge quotient normalization is predicted.",
            "Keeps the Newton limit honest.",
            "ANTI_OVERCLAIM_POLICY",
        ),
    ]
    return [
        {
            **base(timestamp),
            "contract_id": contract_id,
            "contract_clause": contract_clause,
            "why_it_matters": why_it_matters,
            "status": status,
            "parent_signed": False,
            "claim_allowed": False,
        }
        for contract_id, contract_clause, why_it_matters, status in entries
    ]


def parse_bound_value() -> float:
    gdot_rows = read_csv(source_paths()["SRC3758_2_3757_gdot_fill"])
    gdot_row = next(row for row in gdot_rows if row["residual_id"] == "KRV3755_0_Gdot")
    bound_value = float(gdot_row["bound_value"])
    if not math.isfinite(bound_value) or bound_value <= 0:
        raise ValueError("invalid Gdot bound")
    return bound_value


def gdot_bound_rows(timestamp: str) -> list[dict[str, object]]:
    bound_value = parse_bound_value()
    return [
        {
            **base(timestamp),
            "evaluation_id": "GB3758_0_conditional_zero",
            "observable": "Gdot_over_G",
            "units": "yr^-1",
            "prediction_formula": "d_t ln G_eff = 0",
            "prediction_value": 0.0,
            "bound_value": bound_value,
            "score_status": "CONDITIONAL_NUMERIC_PASS_IF_PARENT_SIGNATURES_SIGNED",
            "required_parent_signatures": "KS3758_0_global_block;KS3758_1_no_local_kappa_field;KS3758_3_cap_conservation;KS3758_4_poisson_frame_silence",
            "valid_prediction_row": False,
            "claim_allowed": False,
        },
        {
            **base(timestamp),
            "evaluation_id": "GB3758_1_residual_bound",
            "observable": "Gdot_over_G",
            "units": "yr^-1",
            "prediction_formula": "|d_t ln kappa_*| + |R_G| + |R_M| + |d_t ln Z_Poisson| + |d_t ln Z_frame|",
            "prediction_value": "MISSING_NUMERIC_FLUX_AND_CALIBRATION_COMPONENTS",
            "bound_value": bound_value,
            "score_status": "BOUND_FORMULA_READY_NUMERIC_COMPONENTS_MISSING",
            "required_parent_signatures": "none if every residual component is numerically bounded",
            "valid_prediction_row": False,
            "claim_allowed": False,
        },
        {
            **base(timestamp),
            "evaluation_id": "GB3758_2_max_allowed_residual",
            "observable": "allowed_absolute_residual_budget",
            "units": "yr^-1",
            "prediction_formula": "residual budget must be <= LLR/Gdot bound under no-cancellation policy",
            "prediction_value": bound_value,
            "bound_value": bound_value,
            "score_status": "NUMERIC_TARGET_FOR_FUTURE_COMPONENT_FILL",
            "required_parent_signatures": "component rows must sum to <= bound",
            "valid_prediction_row": True,
            "claim_allowed": False,
        },
    ]


def runner_patch_rows(timestamp: str) -> list[dict[str, object]]:
    rows = []
    for source_row in read_csv(source_paths()["SRC3758_4_3757_runner_patch"]):
        patched = {
            **base(timestamp),
            "patched_runner_row_id": f"RUN3758_{source_row['residual_id']}",
            "source_runner_row": source_row["patched_runner_row_id"],
            "residual_id": source_row["residual_id"],
            "symbol": source_row["symbol"],
            "arena": source_row["arena"],
            "bound_value": source_row["bound_value"],
            "units": source_row["units"],
            "prediction_status_3757": source_row["prediction_status_3757"],
            "score_status_3757": source_row["score_status_3757"],
            "prediction_status_3758": source_row["prediction_status_3757"],
            "score_status_3758": source_row["score_status_3757"],
            "prediction_or_bound_formula_3758": source_row["prediction_value_3757"],
            "conditional_score_ready": source_row["conditional_score_ready"],
            "valid_prediction_row": False,
            "claim_allowed": False,
            "notes": "unchanged from 3757",
        }
        if source_row["residual_id"] == "KRV3755_0_Gdot":
            patched.update(
                {
                    "prediction_status_3758": "ZERO_OR_FLUX_BOUNDED_KAPPA_QUOTIENT_LAW",
                    "score_status_3758": "CONDITIONAL_ZERO_OR_RESIDUAL_BOUND_READY",
                    "prediction_or_bound_formula_3758": "|d_t ln kappa_*| + |R_G| + |R_M| + |d_t ln Z_Poisson| + |d_t ln Z_frame| <= 9.6e-15 yr^-1; zero if all components vanish",
                    "conditional_score_ready": True,
                    "notes": "3758 derives the exact residual budget; numeric component values remain missing",
                }
            )
        rows.append(patched)
    return rows


def claim_gate_rows(timestamp: str, grouped: dict[str, list[dict[str, object]]]) -> list[dict[str, object]]:
    all_sources = all(Path(str(row["source_path"])).exists() for row in grouped["sources"])
    gates = [
        ("CG3758_0_sources", "all 3758 source paths exist", all_sources, "path hygiene"),
        ("CG3758_1_quotient_identity", "kappa quotient log derivative law derived", True, "exact identity"),
        ("CG3758_2_flux_bound", "Gdot residual bound inequality derived", True, "no-cancellation absolute budget"),
        ("CG3758_3_kappa_parent_signed", "kappa global/superselection action contract signed", False, "contract emitted but not adopted by parent action"),
        ("CG3758_4_numeric_residual_components", "all residual components numeric", False, "flux/calibration components missing"),
        ("CG3758_5_Gdot_claim", "Gdot claim allowed", False, "conditional zero or bound not fully sourced"),
        ("CG3758_6_absolute_G_claim", "absolute measured G derived", False, "normalization kappa_* or quotient value not predicted"),
        ("CG3758_7_local_gr_claim", "local GR/PPN claim allowed", False, "PPN/source residual vector remains open"),
    ]
    return [
        {
            **base(timestamp),
            "gate_id": gate_id,
            "gate": gate,
            "passed": passed,
            "details": details,
            "claim_allowed": False,
        }
        for gate_id, gate, passed, details in gates
    ]


def decision_rows(timestamp: str) -> list[dict[str, object]]:
    entries = [
        (
            "DEC3758_0",
            "The theory does not need to derive the measured number G at this stage to recover Newton/GR; it must derive a constant local coupling and calibrate the value.",
            "focus next on signing constancy and source universality before absolute normalization",
        ),
        (
            "DEC3758_1",
            "The clean mathematical object is not a free fitted G(t), but a quotient/superselection law for kappa_eff with a flux residual budget.",
            "treat nonzero Gdot as a sum of named residual channels, not as a vague missing parameter",
        ),
        (
            "DEC3758_2",
            "If parent global-kappa cannot be signed, the fallback is still testable: fill R_G, R_M, Z_Poisson, and Z_frame components and compare their absolute sum to 9.6e-15 yr^-1.",
            "next checkpoint should choose one component and try to zero or bound it",
        ),
    ]
    return [
        {
            **base(timestamp),
            "decision_id": decision_id,
            "decision": decision,
            "action": action,
            "claim_allowed": False,
        }
        for decision_id, decision, action in entries
    ]


def next_target_rows(timestamp: str) -> list[dict[str, object]]:
    return [
        {
            **base(timestamp),
            "next_id": "NEXT3758_0",
            "target_doc": "3759-Y5-R2FR-source-universality-or-WEP-coupling-row.md",
            "target_script": "scripts/Y5_R2FR_3759_source_universality_or_WEP_coupling_row.py",
            "objective": "derive source-blind kappa/source charge universality for the WEP row, or produce a composition residual formula eta_source_AB that can be bounded against 2.8e-15",
            "reason": "Gdot now has a zero-or-flux-budget route; WEP/source universality is the next coupling gate on the path to local GR",
            "claim_allowed": False,
        }
    ]


def status_rows(timestamp: str) -> list[dict[str, object]]:
    return [
        {
            **base(timestamp),
            "status": "KAPPA_QUOTIENT_LAW_AND_GDOT_RESIDUAL_BUDGET_DERIVED",
            "summary": "3758 derives d_t ln kappa_eff as a quotient flux law. Gdot is zero if global kappa, charge conservation, and Poisson/frame silence are parent-signed; otherwise the residual budget must be <= 9.6e-15 yr^-1.",
            "claim_allowed": False,
        }
    ]


def validation_rows(timestamp: str, grouped: dict[str, list[dict[str, object]]]) -> list[dict[str, object]]:
    generated_csvs = [path for key, path in OUTPUTS.items() if key != "validation"]
    checks = [
        ("sources_exist", "all 3758 source paths exist", all(Path(str(row["source_path"])).exists() for row in grouped["sources"])),
        ("generated_csvs_parse", "all generated 3758 csvs parse", all(read_csv(path) for path in generated_csvs)),
        (
            "quotient_identity",
            "quotient log derivative identity emitted",
            any(row["law_id"] == "KQ3758_1_log_derivative" and row["status"] == "EXACT_QUOTIENT_IDENTITY" for row in grouped["quotient_law"]),
        ),
        (
            "flux_bound",
            "no-cancellation Gdot residual bound emitted",
            any(row["law_id"] == "KQ3758_6_Gdot_bound" and row["status"] == "NUMERIC_RESIDUAL_REQUIREMENT_DERIVED" for row in grouped["quotient_law"]),
        ),
        (
            "conditional_zero",
            "conditional zero theorem emitted",
            any(row["law_id"] == "KQ3758_4_superselection_zero" and row["status"] == "EXACT_CONDITIONAL_ZERO_THEOREM" for row in grouped["quotient_law"]),
        ),
        (
            "gdot_budget_bound",
            "Gdot budget uses 9.6e-15 yr^-1",
            any(str(row["bound_value"]) == "9.6e-15" for row in grouped["gdot_bound"]),
        ),
        (
            "runner_patch_nonclaim",
            "patched runner remains nonclaim",
            all(str(row["claim_allowed"]) == "False" or row["claim_allowed"] is False for row in grouped["runner_patch"]),
        ),
        (
            "absolute_G_not_claimed",
            "absolute G remains unclaimed",
            any(row["gate_id"] == "CG3758_6_absolute_G_claim" and row["passed"] is False for row in grouped["claim_gates"]),
        ),
        (
            "local_gr_not_claimed",
            "local GR remains unclaimed",
            any(row["gate_id"] == "CG3758_7_local_gr_claim" and row["passed"] is False for row in grouped["claim_gates"]),
        ),
        (
            "next_target",
            "3759 target emitted",
            grouped["next_target"][0]["target_doc"] == "3759-Y5-R2FR-source-universality-or-WEP-coupling-row.md",
        ),
        (
            "no_formalization_leak",
            "no 3758 files written to formalization-workbench",
            not FORMALIZATION.exists() or not list(FORMALIZATION.rglob("*3758*")),
        ),
    ]
    return [
        {
            **base(timestamp),
            "validation_id": validation_id,
            "description": description,
            "result": "PASS" if result else "FAIL",
            "details": "" if result else "check failed",
        }
        for validation_id, description, result in checks
    ]


def render_doc(grouped: dict[str, list[dict[str, object]]]) -> str:
    lines = [
        "# 3758 — Kappa Superselection Signature Or Gdot Numeric Bound",
        "",
        "## Status",
        "",
        f"`{grouped['status'][0]['status']}`.",
        "",
        grouped["status"][0]["summary"],
        "",
        "## Derivation",
        "",
        "This checkpoint makes the coupling problem sharper. GR does not derive the measured value of Newton's constant from pure differential geometry; it uses a coupling. For MTS the first reachable target is stronger than a fit but weaker than absolute-G derivation: derive local constancy and source universality, then leave the absolute normalization as a parent-action target.",
        "",
        "Let `kappa_eff := kappa_* C_G/C_M`, with `C_G=ell_G(J_G)` and `C_M=ell_M(J_M)`. For nonzero charges,",
        "",
        "`d_t ln kappa_eff = d_t ln kappa_* + d_t ln C_G - d_t ln C_M`.",
        "",
        "Using the Ward/Stokes balance for each charge,",
        "",
        "`d_t ln C_X = (-Phi_X + int_W Pi_X q_X)/(C_X Delta t)`.",
        "",
        "Therefore the no-cancellation Gdot budget is",
        "",
        "`|d_t ln G_eff| <= |d_t ln kappa_*| + |R_G| + |R_M| + |d_t ln Z_Poisson| + |d_t ln Z_frame|`.",
        "",
        "The local bound route is then exact: that absolute sum must be `<= 9.6e-15 yr^-1`, or every term must be parent-zero.",
        "",
        "## Kappa Quotient Law",
    ]
    for row in grouped["quotient_law"]:
        lines.append(f"- `{row['law_id']}` `{row['status']}`: {row['law_or_derivation']}")
    lines.extend(["", "## Parent Action Contract"])
    for row in grouped["signature_contract"]:
        lines.append(f"- `{row['contract_id']}` `{row['status']}`: {row['contract_clause']}")
    lines.extend(["", "## Gdot Bound Evaluation"])
    for row in grouped["gdot_bound"]:
        lines.append(
            f"- `{row['evaluation_id']}` `{row['score_status']}`: `{row['prediction_formula']}` versus `{row['bound_value']} {row['units']}` claim=`{row['claim_allowed']}`"
        )
    lines.extend(["", "## Runner Patch"])
    for row in grouped["runner_patch"]:
        lines.append(f"- `{row['patched_runner_row_id']}` `{row['score_status_3758']}`: {row['prediction_or_bound_formula_3758']}")
    lines.extend(["", "## Claim Gates"])
    for row in grouped["claim_gates"]:
        lines.append(f"- `{row['gate_id']}` pass=`{row['passed']}`: {row['gate']} — {row['details']}")
    lines.extend(["", "## Decisions"])
    for row in grouped["decision_rows"]:
        lines.append(f"- `{row['decision_id']}`: {row['decision']} Action: {row['action']}.")
    lines.extend(["", "## Next Target"])
    for row in grouped["next_target"]:
        lines.append(f"- `{row['target_doc']}`: {row['objective']}")
    lines.extend(["", "## Validation"])
    for row in grouped["validation"]:
        lines.append(f"- `{row['validation_id']}` `{row['result']}`: {row['description']}")
    lines.append("")
    return "\n".join(lines)


def main() -> None:
    timestamp = stamp()
    RESIDUALS.mkdir(parents=True, exist_ok=True)

    grouped: dict[str, list[dict[str, object]]] = {
        "sources": source_register(timestamp),
        "quotient_law": quotient_law_rows(timestamp),
        "signature_contract": signature_contract_rows(timestamp),
        "gdot_bound": gdot_bound_rows(timestamp),
        "runner_patch": runner_patch_rows(timestamp),
        "decision_rows": decision_rows(timestamp),
        "next_target": next_target_rows(timestamp),
        "status": status_rows(timestamp),
    }
    grouped["claim_gates"] = claim_gate_rows(timestamp, grouped)

    write_csv(OUTPUTS["sources"], grouped["sources"])
    write_csv(OUTPUTS["quotient_law"], grouped["quotient_law"])
    write_csv(OUTPUTS["signature_contract"], grouped["signature_contract"])
    write_csv(OUTPUTS["gdot_bound"], grouped["gdot_bound"])
    write_csv(OUTPUTS["runner_patch"], grouped["runner_patch"])
    write_csv(OUTPUTS["claim_gates"], grouped["claim_gates"])
    write_csv(OUTPUTS["decision_rows"], grouped["decision_rows"])
    write_csv(OUTPUTS["next_target"], grouped["next_target"])
    write_csv(OUTPUTS["status"], grouped["status"])

    grouped["validation"] = validation_rows(timestamp, grouped)
    write_csv(OUTPUTS["validation"], grouped["validation"])

    DOC_PATH.write_text(render_doc(grouped), encoding="utf-8")

    cache = Path(__file__).resolve().parent / "__pycache__"
    if cache.exists():
        shutil.rmtree(cache)

    failures = [row for row in grouped["validation"] if row["result"] != "PASS"]
    if failures:
        raise SystemExit(f"3758 validation failed: {failures}")
    print("wrote 3758 checkpoint: kappa quotient law and Gdot residual budget derived")


if __name__ == "__main__":
    main()

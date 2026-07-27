from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from Y5_R10_alpha_product_prediction_stub_runner_and_required_inputs import (
    BOUND_REQUIRED_COLUMNS,
    PRODUCT_REQUIRED_COLUMNS,
    run_product_runner,
)


STARTED = datetime.now(timezone.utc)
ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "source-intake" / "mts_residuals"
DOC = ROOT / "1091-Y5-R10-parent-operator-domain-no-hidden-visible-hom-theorem-or-MOMS-closure.md"
FORMALIZATION = ROOT.parent / "formalization-workbench"
RUN_DIR = ROOT / "runs" / "1091-parent-operator-domain-no-hidden-visible-hom" / "results"
PRODUCT_RUN_DIR = RUN_DIR / "product_runner"
PREDICTION_TEMPLATE = OUT / "P8_Y5_R10_1091_WEP_PRODUCT_CANDIDATE_NONCLAIM.csv"
BOUND_IMPORT = OUT / "P8_Y5_R10_1091_WEP_BOUND_IMPORT.csv"
ETA_BOUND = 2.8e-15


def stamp() -> str:
    return datetime.now(timezone.utc).isoformat()


def source_path(path_text: str) -> Path:
    path = Path(path_text)
    if path.is_absolute():
        return path
    return ROOT / path


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="ignore")


def write_csv(path: Path, rows: list[dict[str, object]], fieldnames: list[str] | None = None) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if fieldnames is None:
        fieldnames = []
        for row in rows:
            for key in row:
                if key not in fieldnames:
                    fieldnames.append(key)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow({key: row.get(key, "") for key in fieldnames})


def parse_float(value: object) -> float | None:
    try:
        return float(str(value).strip())
    except ValueError:
        return None


def md_cell(value: object) -> str:
    return str(value).replace("\n", " ").replace("|", "\\|")


def md_table(rows: list[dict[str, object]], columns: list[str]) -> str:
    if not rows:
        return "_No rows._\n"
    return "\n".join(
        [
            "| " + " | ".join(columns) + " |",
            "| " + " | ".join("---" for _ in columns) + " |",
            *["| " + " | ".join(md_cell(row.get(column, "")) for column in columns) + " |" for row in rows],
        ]
    ) + "\n"


def count_formalization_modified_since_start() -> int:
    if not FORMALIZATION.exists():
        return 0
    return sum(
        1
        for path in FORMALIZATION.rglob("*")
        if path.is_file() and datetime.fromtimestamp(path.stat().st_mtime, timezone.utc) >= STARTED
    )


def remove_pycache() -> None:
    pycache = Path(__file__).resolve().parent / "__pycache__"
    if pycache.exists():
        shutil.rmtree(pycache)


def source_register_rows() -> list[dict[str, str]]:
    specs = [
        ("SRC1091_0_1090_next", "source-intake/mts_residuals/P8_Y5_R10_1090_NEXT_TARGET.csv", "NEXT1090_0_1091", "1090 handoff."),
        ("SRC1091_1_1090_axioms", "source-intake/mts_residuals/P8_Y5_R10_1090_MISSING_AXIOM_LEDGER.csv", "AX1090_1_no_hidden_visible_hom", "missing operator-domain axiom."),
        ("SRC1091_2_1090_closure", "source-intake/mts_residuals/P8_Y5_R10_1090_CLOSURE_DEMOTION_REGISTER.csv", "CLOS1090_0_MOMS", "MOMS closure demotion."),
        ("SRC1091_3_1049_operator", "1049-Y5-R10-parent-operator-classification-symmetry-ban-or-residual-coefficient-prior.md", "OCR1049_5_verdict", "operator classification audit."),
        ("SRC1091_4_1050_product", "1050-Y5-R10-visible-hidden-product-functor-derivation-or-prior-width-source-pack.md", "PFT1050_5_verdict", "visible-hidden product functor audit."),
        ("SRC1091_5_1051_no_mixed", "1051-Y5-R10-no-mixed-hidden-visible-morphism-lemma-or-first-prior-width-chain.md", "NMM1051_5_verdict", "no-mixed morphism audit."),
        ("SRC1091_6_980_no_marker", "980-Y5-R10-no-marker-sector-functor-theorem-or-first-qbar-source-acquisition.md", "NMF980_2_scalar_obstruction_lemma", "scalar obstruction proof."),
        ("SRC1091_7_1051_balpha", "source-intake/mts_residuals/P8_Y5_R10_1051_B_ALPHA_CLOCK_PRODUCT_PRIOR_CHAIN.csv", "BAP1051_2_best_current_product", "source-backed b_alpha clock product chain."),
        ("SRC1091_8_1051_projection", "source-intake/mts_residuals/P8_Y5_R10_1051_B_ALPHA_PROJECTION_READINESS.csv", "BAPR1051_0_clock", "b_alpha projection readiness."),
        ("SRC1091_9_local_bounds", "source-intake/local_bounds/local_bound_claims.csv", "R1_WEP_source_charge", "MICROSCOPE WEP bound row."),
    ]
    rows: list[dict[str, str]] = []
    for source_id, relative_path, needle, note in specs:
        path = source_path(relative_path)
        exists = path.exists()
        text = read_text(path) if exists else ""
        needle_found = exists and needle.lower() in text.lower()
        rows.append(
            {
                "source_id": source_id,
                "relative_path": relative_path,
                "absolute_path": str(path),
                "exists": str(exists).lower(),
                "needle": needle,
                "needle_found": str(needle_found).lower(),
                "note": note,
                "valid_for_claim": "false",
                "generated_utc": stamp(),
            }
        )
    return rows


def theorem_attempt_rows() -> list[dict[str, str]]:
    return [
        {
            "theorem_id": "ODH1091_0_target",
            "claim_piece": "no hidden-visible coefficient homomorphism",
            "mathematical_statement": "Hom(C_hid, Coeff(O_vis)) = Const or absent for O_vis in {F^2, mass, Yukawa, binding, clock, source}",
            "proof_status": "TARGET_SHARP",
            "obstruction": "none at definition level",
            "effect_on_MOMS": "would sign AX1090_1 and support constants/no-shadow clauses",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "theorem_id": "ODH1091_1_trivial_invariant_algebra",
            "claim_piece": "hidden invariant algebra triviality is sufficient",
            "mathematical_statement": "O(C_hid)^inv = R implies any invariant scalar coefficient c:C_hid -> R is constant",
            "proof_status": "EXACT_CONDITIONAL_THEOREM",
            "obstruction": "current corpus has not proved O(C_hid)^inv=R",
            "effect_on_MOMS": "would close visible coefficient leakage if paired with radiative/readout closure",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "theorem_id": "ODH1091_2_scalar_obstruction",
            "claim_piece": "surviving scalar kills the theorem",
            "mathematical_statement": "if I in O(C_hid)^inv and dI != 0, then c_I=c0+epsilon I defines a nonconstant visible coefficient morphism",
            "proof_status": "COUNTEREXAMPLE_PROVED",
            "obstruction": "980 and 1051 record the scalar-invariant obstruction",
            "effect_on_MOMS": "AX1090_1 cannot be derived while I survives",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "theorem_id": "ODH1091_3_symmetry_limits",
            "claim_piece": "ordinary symmetries do not save the theorem",
            "mathematical_statement": "diffeomorphism and gauge invariance allow f(I)F^2, m_A(I) psi_bar psi, clock(I), and source weights",
            "proof_status": "INSUFFICIENT_SYMMETRY",
            "obstruction": "1049 shows covariance/gauge symmetry do not forbid the dangerous operators",
            "effect_on_MOMS": "needs stronger product/sequester/shift/triviality principle",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "theorem_id": "ODH1091_4_product_functor_limit",
            "claim_piece": "product functor theorem would work if parent-signed",
            "mathematical_statement": "S_vis = S_vis[q(Phi), theta_rep] and no Hom(C_hid,Coeff(O_vis)) removes hidden-visible coefficient maps",
            "proof_status": "EXACT_CONDITIONAL_NOT_PARENT_SIGNED",
            "obstruction": "1050 product category/no mixed morphism/radiative closure all remain unsigned",
            "effect_on_MOMS": "contract is correct but cannot be reused as proof",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "theorem_id": "ODH1091_5_radiative_readout_limit",
            "claim_piece": "bare sequester is not enough",
            "mathematical_statement": "S_bare no mixed terms does not imply S_eff/readout no mixed terms unless closure theorem holds",
            "proof_status": "RADIATIVE_READOUT_CLOSURE_UNSIGNED",
            "obstruction": "1050/1051 retain b_alpha and b_clock_i after effective/readout reductions",
            "effect_on_MOMS": "AX1090_1 would still need effective-action/readout closure",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "theorem_id": "ODH1091_6_verdict",
            "claim_piece": "parent operator-domain no-hidden-visible-hom theorem is derived",
            "mathematical_statement": "ODH1091_1 plus no scalar obstruction plus product/sequester plus radiative/readout closure",
            "proof_status": "THEOREM_NOT_DERIVED_CURRENT_CORPUS",
            "obstruction": "scalar obstruction survives; product functor/radiative closure not parent-signed",
            "effect_on_MOMS": "MOMS remains closure_candidate_not_adopted; finite residual coefficients stay live",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
    ]


def obstruction_rows() -> list[dict[str, str]]:
    return [
        {
            "obstruction_id": "OBS1091_0_invariant_scalar",
            "obstruction": "nonconstant hidden invariant scalar",
            "example": "I_hid -> f_X(I_hid)F_Q^2 or m_A(I_hid) psi_bar psi",
            "why_currently_live": "980/1051 do not prove hidden invariant algebra triviality",
            "needed_to_kill": "O(C_hid)^inv=R, exact shift/no-hair, or product functor parent signature",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "obstruction_id": "OBS1091_1_alpha_owner",
            "obstruction": "visible EM normalization owner unsigned",
            "example": "g_EM or alpha_EM as independent coefficient",
            "why_currently_live": "1050 records Maxwell descent does not fix alpha owner",
            "needed_to_kill": "parent charge-generator norm/topological level/radiative closure theorem",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "obstruction_id": "OBS1091_2_matter_spectrum",
            "obstruction": "ordinary matter spectrum/constants not parent-owned",
            "example": "m_A(I), y_A(I), B_A(I), Lambda_QCD(I)",
            "why_currently_live": "1045/1050 leave matter category and constants split unsigned",
            "needed_to_kill": "parent matter category plus fixed representation/superselection theorem",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "obstruction_id": "OBS1091_3_source_labels",
            "obstruction": "source-label forgetting not parent-signed",
            "example": "F((T_A,A)) = kappa_A T_A",
            "why_currently_live": "1050 keeps source labels and qbar_source_label retained",
            "needed_to_kill": "parent source functor to total Hilbert source before species labels",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "obstruction_id": "OBS1091_4_readout_regeneration",
            "obstruction": "radiative/effective/readout re-entry",
            "example": "loop-induced f_X F^2 or clock readout X dependence",
            "why_currently_live": "1050/1051 say bare action sequester does not automatically survive readout",
            "needed_to_kill": "effective-action/readout functor closure or retained source-backed priors",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
    ]


def moms_effect_rows() -> list[dict[str, str]]:
    return [
        {
            "effect_id": "ME1091_0_AX1090_1",
            "MOMS_component": "no hidden-visible coefficient hom axiom",
            "effect": "not derivable from current corpus",
            "consequence": "AX1090_1 remains missing, so MOMS all-in-one signature remains closure_candidate_not_adopted",
            "claim_status": "blocked",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "effect_id": "ME1091_1_constant_superselection",
            "MOMS_component": "ordinary constants fixed",
            "effect": "not secured because hidden scalars can still map into alpha/masses/clocks",
            "consequence": "b_alpha, b_mu, b_mA, b_nuc, b_clock_i remain live residuals",
            "claim_status": "blocked",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "effect_id": "ME1091_2_no_shadow_frame",
            "MOMS_component": "no shadow frame/domain marker",
            "effect": "not secured because conformal/disformal/material marker coefficient maps are legal without operator-domain ban",
            "consequence": "qbar_marker and frame residuals remain retained",
            "claim_status": "blocked",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "effect_id": "ME1091_3_qbar_zero",
            "MOMS_component": "qbar_XT=0 local branch",
            "effect": "still true only under MOMS closure assumptions",
            "consequence": "cannot claim local WEP/R10/PPN safety; must use finite residual/product route if testing",
            "claim_status": "conditional_only",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
    ]


def finite_residual_rows() -> list[dict[str, str]]:
    return [
        {
            "residual_id": "FR1091_0_b_alpha",
            "symbol": "b_alpha",
            "status": "source_backed_clock_product_only",
            "best_current_bound": "|b_alpha*tau_clock_time| <= 2.1e-18 yr^-1 at 1sigma from 1051 Yb E3/E2 row",
            "missing_for_claim": "tau_clock_time; Xhat normalization; WEP/R10 source-test alpha projection; alpha owner",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "residual_id": "FR1091_1_b_mu",
            "symbol": "b_mu",
            "status": "retained_prior_missing",
            "best_current_bound": "none claim-ready in current chain",
            "missing_for_claim": "mass-ratio sensitivity and tau/projection source rows",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "residual_id": "FR1091_2_b_mA",
            "symbol": "b_mA",
            "status": "retained_prior_missing",
            "best_current_bound": "MICROSCOPE WEP bound anchor exists but composition/projection rows are missing",
            "missing_for_claim": "composition sensitivity matrix; source/test material charge vectors; tau_WEP",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "residual_id": "FR1091_3_b_nuc",
            "symbol": "b_nuc",
            "status": "retained_prior_missing",
            "best_current_bound": "none claim-ready in current chain",
            "missing_for_claim": "nuclear/QCD/binding sensitivity sources and local projections",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "residual_id": "FR1091_4_b_clock_i",
            "symbol": "b_clock_i",
            "status": "retained_prior_missing",
            "best_current_bound": "clock anchors exist but direct readout residual model is missing",
            "missing_for_claim": "clock readout model; tau_clock; separation from alpha/mass/nuclear channels",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "residual_id": "FR1091_5_qbar_source_label",
            "symbol": "qbar_source_label",
            "status": "retained_prior_missing",
            "best_current_bound": "MICROSCOPE WEP bound anchor exists",
            "missing_for_claim": "source-label forgetting theorem or relative source-weight prior and projection",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
    ]


def prediction_rows() -> list[dict[str, str]]:
    return [
        {
            "prediction_id": "PRED1091_0_operator_domain_failed",
            "arena": "MICROSCOPE_WEP",
            "product_symbol": "P_WEP_relative_source_weight",
            "product_value": "MISSING_OPERATOR_DOMAIN_THEOREM_OR_FINITE_RESIDUAL_PRODUCT",
            "product_units": "dimensionless",
            "product_source": "source-intake/mts_residuals/P8_Y5_R10_1091_OPERATOR_DOMAIN_THEOREM_ATTEMPT.csv",
            "inputs_present": "operator-domain theorem attempt; residual map; MICROSCOPE bound",
            "required_inputs": "hidden invariant algebra triviality/product functor closure OR finite residual product rows",
            "derivation_status": "THEOREM_NOT_DERIVED_CURRENT_CORPUS",
            "valid_for_claim": "false",
            "notes": "generic product runner must refuse; no MOMS/local-WEP claim follows",
        }
    ]


def bound_import_rows() -> list[dict[str, str]]:
    return [
        {
            "bound_id": "BOUND1091_0_MICROSCOPE_WEP",
            "arena": "MICROSCOPE_WEP",
            "product_symbol": "P_WEP_relative_source_weight",
            "bound_value": f"{ETA_BOUND:.16e}",
            "bound_units": "dimensionless",
            "bound_source": "source-intake/local_bounds/local_bound_claims.csv",
            "source_row": "R1_WEP_source_charge",
            "bound_type": "absolute_eta_upper_bound",
            "valid_for_claim": "true",
            "notes": "source-backed comparator bound; MTS prediction row remains invalid",
        }
    ]


def product_status_rows(product_status: dict[str, Any]) -> list[dict[str, str]]:
    return [
        {
            "runner_id": "APR1091_0_operator_domain_stub",
            "prediction_rows": str(product_status.get("prediction_rows", "")),
            "bound_rows": str(product_status.get("bound_rows", "")),
            "valid_prediction_rows": str(product_status.get("valid_prediction_rows", "")),
            "valid_bound_rows": str(product_status.get("valid_bound_rows", "")),
            "comparison_rows": str(product_status.get("comparison_rows", "")),
            "claim_allowed": str(product_status.get("claim_allowed", "")).lower(),
            "expected_result": "reject missing operator-domain theorem and finite residual product",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        }
    ]


def claim_gate_rows(product_status: dict[str, Any]) -> list[dict[str, str]]:
    return [
        {
            "gate_id": "CG1091_0_operator_domain",
            "claim_component": "no hidden-visible hom theorem",
            "gate_pass": "false",
            "claim_allowed": "false",
            "reason": "ODH1091_6_verdict=THEOREM_NOT_DERIVED_CURRENT_CORPUS",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "gate_id": "CG1091_1_MOMS",
            "claim_component": "MOMS derived local branch",
            "gate_pass": "false",
            "claim_allowed": "false",
            "reason": "AX1090_1 remains missing; MOMS stays closure_candidate_not_adopted",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "gate_id": "CG1091_2_balpha_transfer",
            "claim_component": "clock b_alpha product transfers to WEP/R10",
            "gate_pass": "false",
            "claim_allowed": "false",
            "reason": "clock product bound lacks tau_clock, Xhat normalization, and WEP/R10 source-test projection",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "gate_id": "CG1091_3_product_runner",
            "claim_component": "WEP product runner",
            "gate_pass": str(product_status.get("valid_prediction_rows") == 0).lower(),
            "claim_allowed": "false",
            "reason": f"valid_prediction_rows={product_status.get('valid_prediction_rows')}",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
    ]


def decision_rows() -> list[dict[str, str]]:
    return [
        {
            "decision_id": "DEC1091_0_theorem_result",
            "decision": "operator-domain/no-hidden-visible-hom theorem is not derived",
            "because": "a surviving hidden invariant scalar builds exactly the forbidden visible coefficient morphism",
            "next_action": "prove hidden invariant algebra triviality or retain finite residual coefficients",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "decision_id": "DEC1091_1_MOMS_status",
            "decision": "MOMS remains a closure candidate, not adopted",
            "because": "the operator-domain axiom was the smallest missing MOMS beam and it did not close",
            "next_action": "do not use MOMS to claim local WEP/R10/PPN safety",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "decision_id": "DEC1091_2_best_next",
            "decision": "target hidden invariant algebra triviality before finite priors",
            "because": "triviality is the cleanest remaining derivation route; if it fails, finite b_alpha/tau projection becomes the practical route",
            "next_action": "attempt O(C_hid)^inv=R or build b_alpha tau/projection source chain",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
    ]


def next_target_rows() -> list[dict[str, str]]:
    return [
        {
            "next_id": "NEXT1091_0_1092",
            "next_target": "1092-Y5-R10-hidden-invariant-algebra-triviality-or-balpha-tau-projection.md",
            "objective": "try to prove the local hidden invariant algebra is trivial on the MOMS/local branch; if it fails, route to the finite b_alpha*tau_clock and WEP/R10 projection source chain without claiming transfer",
            "include": "O(C_hid)^inv=R theorem attempt; scalar no-hair/shift/exact quotient tests; b_alpha tau_clock/Xhat normalization fallback; WEP/R10 projection gates",
            "exclude": "assuming sequester by minimality; transferring clock bound to WEP/R10 without projections; invented coefficients; pair cancellation; WEP/local-GR claim; GitHub; formalization edits",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        }
    ]


def csv_outputs_parse(paths: list[Path]) -> bool:
    try:
        for path in paths:
            with path.open(newline="", encoding="utf-8") as handle:
                list(csv.DictReader(handle))
        return True
    except csv.Error:
        return False


def validate_outputs(
    outputs: dict[str, Path],
    source_rows: list[dict[str, str]],
    theorem_rows: list[dict[str, str]],
    obstruction_rows_: list[dict[str, str]],
    moms_rows: list[dict[str, str]],
    residual_rows: list[dict[str, str]],
    prediction_rows_: list[dict[str, str]],
    bound_rows_: list[dict[str, str]],
    product_status: dict[str, Any],
    claim_rows: list[dict[str, str]],
    next_rows: list[dict[str, str]],
) -> list[dict[str, str]]:
    checks: list[tuple[str, bool, str]] = []
    checks.append(("V1091_0_local_sources_exist", all(row["exists"] == "true" and row["needle_found"] == "true" for row in source_rows), "all cited source paths and needles are present"))
    checks.append(("V1091_1_theorem_not_derived", any(row["theorem_id"] == "ODH1091_6_verdict" and row["proof_status"] == "THEOREM_NOT_DERIVED_CURRENT_CORPUS" for row in theorem_rows), "operator-domain theorem ends in explicit non-derivation verdict"))
    checks.append(("V1091_2_scalar_obstruction_retained", any(row["theorem_id"] == "ODH1091_2_scalar_obstruction" and row["proof_status"] == "COUNTEREXAMPLE_PROVED" for row in theorem_rows), "scalar obstruction counterexample is retained"))
    checks.append(("V1091_3_obstructions_complete", len(obstruction_rows_) == 5 and all(row["valid_for_claim"] == "false" for row in obstruction_rows_), "operator-domain obstruction ledger is complete and nonclaim"))
    checks.append(("V1091_4_MOMS_effects_blocked", len(moms_rows) == 4 and all(row["valid_for_claim"] == "false" for row in moms_rows), "MOMS effect ledger keeps local branch blocked"))
    checks.append(("V1091_5_residuals_retained", len(residual_rows) == 6 and all(row["valid_for_claim"] == "false" for row in residual_rows), "finite residual coefficient map is retained as nonclaim"))
    checks.append(("V1091_6_prediction_missing_nonclaim", any("MISSING_OPERATOR_DOMAIN_THEOREM" in row["product_value"] and row["valid_for_claim"] == "false" for row in prediction_rows_), "prediction row remains missing theorem or finite product"))
    checks.append(("V1091_7_bound_numeric", bool(bound_rows_) and parse_float(bound_rows_[0]["bound_value"]) is not None and float(bound_rows_[0]["bound_value"]) > 0 and bound_rows_[0]["valid_for_claim"] == "true", "MICROSCOPE bound import is positive numeric"))
    checks.append(("V1091_8_product_runner_refuses", product_status.get("valid_prediction_rows") == 0 and product_status.get("claim_allowed") is False, "generic product runner reports no valid prediction rows and claim false"))
    checks.append(("V1091_9_claim_gates_safe", claim_rows and all(row["claim_allowed"] == "false" for row in claim_rows), "all claim gates deny WEP/local-GR claim"))
    checks.append(("V1091_10_next_target", any(row["next_target"].startswith("1092-Y5-R10-hidden-invariant") for row in next_rows), "1092 handoff written"))
    generated_paths = list(outputs.values()) + [DOC]
    checks.append(("V1091_11_generated_under_post_checkpoint", all(str(path.resolve()).startswith(str(ROOT.resolve())) for path in generated_paths), "all generated outputs are under post-checkpoint-work"))
    checks.append(("V1091_12_csv_parse", csv_outputs_parse([path for key, path in outputs.items() if key != "validation"]), "all 1091 CSV outputs parse cleanly"))
    checks.append(("V1091_13_formalization_untouched", count_formalization_modified_since_start() == 0, "formalization-workbench modified-file count remains zero"))
    checks.append(("V1091_SUMMARY", True, "operator-domain theorem not derived; hidden scalar obstruction survives; MOMS remains closure-candidate; finite residual route stays nonclaim"))
    return [
        {
            "check_id": check_id,
            "result": "pass" if passed else "fail",
            "detail": detail,
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        }
        for check_id, passed, detail in checks
    ]


def write_doc(
    source_rows: list[dict[str, str]],
    theorem_rows: list[dict[str, str]],
    obstruction_rows_: list[dict[str, str]],
    moms_rows: list[dict[str, str]],
    residual_rows: list[dict[str, str]],
    product_status_rows_: list[dict[str, str]],
    product_comparisons: list[dict[str, Any]],
    claim_rows: list[dict[str, str]],
    decisions: list[dict[str, str]],
    validation_rows: list[dict[str, str]],
    next_rows: list[dict[str, str]],
) -> None:
    text = "\n".join(
        [
            "# 1091-Y5-R10 parent operator-domain no-hidden-visible-hom theorem or MOMS closure",
            "",
            "## Current verdict",
            "1091 tries the smallest missing MOMS axiom: no hidden-visible coefficient homomorphisms. The clean theorem exists conditionally: if the hidden invariant algebra is trivial, or if a parent product/sequester functor is signed and survives readout, hidden motion cannot feed alpha, mass, clock, shadow-frame, or source-label coefficients. But the current corpus does not prove those assumptions. A surviving hidden scalar immediately generates the forbidden coefficient map. So MOMS remains a closure candidate, not an adopted derivation.",
            "",
            "## Source register",
            md_table(source_rows, ["source_id", "relative_path", "exists", "needle_found", "note"]),
            "## Operator-domain theorem attempt",
            md_table(theorem_rows, ["theorem_id", "claim_piece", "mathematical_statement", "proof_status", "obstruction", "effect_on_MOMS"]),
            "## Obstruction ledger",
            md_table(obstruction_rows_, ["obstruction_id", "obstruction", "example", "why_currently_live", "needed_to_kill"]),
            "## MOMS effect ledger",
            md_table(moms_rows, ["effect_id", "MOMS_component", "effect", "consequence", "claim_status"]),
            "## Finite residual route",
            md_table(residual_rows, ["residual_id", "symbol", "status", "best_current_bound", "missing_for_claim"]),
            "## Product runner status",
            md_table(product_status_rows_, ["runner_id", "valid_prediction_rows", "valid_bound_rows", "comparison_rows", "claim_allowed", "expected_result"]),
            "## Product comparison rows",
            md_table(product_comparisons, ["comparison_id", "arena", "product_symbol", "product_value", "bound_value", "comparison_status", "pass_for_claim", "issues"]),
            "## Claim gates",
            md_table(claim_rows, ["gate_id", "claim_component", "gate_pass", "claim_allowed", "reason"]),
            "## Decision ledger",
            md_table(decisions, ["decision_id", "decision", "because", "next_action"]),
            "## Validation",
            md_table(validation_rows, ["check_id", "result", "detail"]),
            "## Next target",
            md_table(next_rows, ["next_id", "next_target", "objective", "include", "exclude"]),
            "",
        ]
    )
    DOC.write_text(text, encoding="utf-8")


def main() -> None:
    source_rows = source_register_rows()
    theorem_rows = theorem_attempt_rows()
    obstruction_rows_ = obstruction_rows()
    moms_rows = moms_effect_rows()
    residual_rows = finite_residual_rows()
    prediction_rows_ = prediction_rows()
    bound_rows_ = bound_import_rows()
    next_rows = next_target_rows()

    outputs = {
        "source_register": OUT / "P8_Y5_R10_1091_SOURCE_REGISTER.csv",
        "theorem": OUT / "P8_Y5_R10_1091_OPERATOR_DOMAIN_THEOREM_ATTEMPT.csv",
        "obstructions": OUT / "P8_Y5_R10_1091_OPERATOR_DOMAIN_OBSTRUCTION_LEDGER.csv",
        "moms_effects": OUT / "P8_Y5_R10_1091_MOMS_EFFECT_LEDGER.csv",
        "finite_residuals": OUT / "P8_Y5_R10_1091_FINITE_RESIDUAL_ROUTE_MAP.csv",
        "prediction": PREDICTION_TEMPLATE,
        "bound": BOUND_IMPORT,
        "product_status": OUT / "P8_Y5_R10_1091_PRODUCT_RUNNER_STATUS.csv",
        "product_comparison": OUT / "P8_Y5_R10_1091_PRODUCT_COMPARISON_ROWS.csv",
        "claim_gates": OUT / "P8_Y5_R10_1091_CLAIM_GATES.csv",
        "decisions": OUT / "P8_Y5_R10_1091_DECISION_LEDGER.csv",
        "next_target": OUT / "P8_Y5_R10_1091_NEXT_TARGET.csv",
        "validation": OUT / "P8_Y5_BRR545_1091_VALIDATION.csv",
    }

    write_csv(outputs["source_register"], source_rows)
    write_csv(outputs["theorem"], theorem_rows)
    write_csv(outputs["obstructions"], obstruction_rows_)
    write_csv(outputs["moms_effects"], moms_rows)
    write_csv(outputs["finite_residuals"], residual_rows)
    write_csv(outputs["prediction"], prediction_rows_, PRODUCT_REQUIRED_COLUMNS)
    write_csv(outputs["bound"], bound_rows_, BOUND_REQUIRED_COLUMNS)

    product_result = run_product_runner(PREDICTION_TEMPLATE, BOUND_IMPORT, PRODUCT_RUN_DIR)
    product_status = product_result["status"]
    product_status_rows_ = product_status_rows(product_status)
    product_comparisons = product_result["comparisons"]
    claim_rows = claim_gate_rows(product_status)
    decisions = decision_rows()

    write_csv(outputs["product_status"], product_status_rows_)
    write_csv(outputs["product_comparison"], product_comparisons)
    write_csv(outputs["claim_gates"], claim_rows)
    write_csv(outputs["decisions"], decisions)
    write_csv(outputs["next_target"], next_rows)

    validation_rows = validate_outputs(
        outputs,
        source_rows,
        theorem_rows,
        obstruction_rows_,
        moms_rows,
        residual_rows,
        prediction_rows_,
        bound_rows_,
        product_status,
        claim_rows,
        next_rows,
    )
    write_csv(outputs["validation"], validation_rows)
    write_doc(
        source_rows,
        theorem_rows,
        obstruction_rows_,
        moms_rows,
        residual_rows,
        product_status_rows_,
        product_comparisons,
        claim_rows,
        decisions,
        validation_rows,
        next_rows,
    )
    remove_pycache()

    failed = [row for row in validation_rows if row["result"] != "pass"]
    print(f"wrote {DOC}")
    print(f"validation: {'PASS' if not failed else 'FAIL'}")
    for row in failed:
        print(f"{row['check_id']}: {row['detail']}")


if __name__ == "__main__":
    main()

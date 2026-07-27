from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "source-intake" / "mts_residuals"
LOCAL_BOUNDS = ROOT / "source-intake" / "local_bounds"
QUEUE = ROOT / "source-intake" / "rab-sector" / "acquisition-queue"
MICROSCOPE = ROOT / "source-intake" / "microscope" / "branch_locked_wep" / "residuals"
BETA_DOCS = ROOT / "source-intake" / "beta-source" / "docs"
FORMALIZATION = ROOT.parent / "formalization-workbench"
DOC = ROOT / "2245-Y5-R2FR-RAB-boundary-charge-QR-Kboundary-zero-or-beta-bound-first-row.md"
BRANCH_ID = "MTS_R2FR_PARENT_QLOC_RAB_BOUNDARY_QR_KBOUNDARY_OR_BETA_2245"
START_TS = datetime.now(timezone.utc).timestamp()


SOURCE_FILES = {
    "2244_doc": ROOT / "2244-Y5-R2FR-RAB-no-physical-pole-theorem-or-bounded-beta-runner.md",
    "2244_validation": OUT / "P8_Y5_BRR545_2244_VALIDATION.csv",
    "2244_next": OUT / "P8_Y5_PARENT_QLOC_2244_NEXT_TARGET.csv",
    "2244_omega_dcr": OUT / "P8_Y5_PARENT_QLOC_2244_OMEGA_DCR_CLOSURE_AUDIT.csv",
    "2244_beta": OUT / "P8_Y5_PARENT_QLOC_2244_BOUNDED_BETA_SOURCE_TEST_TEMPLATE.csv",
    "1039_doc": ROOT / "1039-Y5-R10-boundary-charge-QX-Kboundary-zero-or-beta-bound-first-row.md",
    "1039_validation": OUT / "P8_Y5_BRR545_1039_VALIDATION.csv",
    "1039_lemma": OUT / "P8_Y5_R10_1039_COMPACT_PROPER_BOUNDARY_SILENCE_LEMMA.csv",
    "1039_qk_gate": OUT / "P8_Y5_R10_1039_QX_KBOUNDARY_CLAIM_GATE.csv",
    "1039_residual": OUT / "P8_Y5_R10_1039_BOUNDARY_RESIDUAL_BETA_ROW.csv",
    "581_boundary": OUT / "P8_Y5_R10_581_BOUNDARY_CHARGE_AUDIT.csv",
    "582_boundary": OUT / "P8_Y5_R10_582_BOUNDARY_DIFFERENTIABILITY_AUDIT.csv",
    "669_theta_qx": OUT / "P8_Y5_R10_669_THETA_QX_VARIATION_LEDGER.csv",
    "671_owner_gate": OUT / "P8_Y5_R10_671_BOUNDARY_CHARGE_OWNER_GATE.csv",
    "735_proper_domain": OUT / "P8_Y5_R10_735_PROPER_BOUNDARY_DOMAIN_THEOREM.csv",
    "1019_exactness": OUT / "P8_Y5_R10_1019_BOUNDARY_EXACTNESS_CLAUSES.csv",
    "976_alpha3": OUT / "P8_Y5_R10_976_K_BOUNDARY_ALPHA3_SOURCE_ACQUISITION.csv",
    "977_alpha3_status": OUT / "P8_Y5_R10_977_K_BOUNDARY_ALPHA3_STATUS.csv",
    "local_bounds": LOCAL_BOUNDS / "local_bound_claims.csv",
    "r10_candidate": LOCAL_BOUNDS / "R10_alpha_lambda_bound_curve_1034_REVIEW_CANDIDATE_NONCLAIM.csv",
}


SOURCE_REGISTER = OUT / "P8_Y5_PARENT_QLOC_2245_SOURCE_REGISTER.csv"
COMPACT_PROPER_LEMMA = OUT / "P8_Y5_PARENT_QLOC_2245_COMPACT_PROPER_BOUNDARY_SILENCE_LEMMA.csv"
QR_KBOUNDARY_GATE = OUT / "P8_Y5_PARENT_QLOC_2245_QR_KBOUNDARY_CLAIM_GATE.csv"
BOUNDARY_RESIDUAL_ROWS = OUT / "P8_Y5_PARENT_QLOC_2245_BOUNDARY_RESIDUAL_BETA_ROW.csv"
FIRST_BETA_PROJECTION = OUT / "P8_Y5_PARENT_QLOC_2245_FIRST_BETA_PROJECTION_TEMPLATE.csv"
ALPHA3_ANCHOR_LEDGER = OUT / "P8_Y5_PARENT_QLOC_2245_ALPHA3_BOUND_ANCHOR_LEDGER.csv"
MTS_ALPHA_TEMPLATE = OUT / "R10_alpha_lambda_curve_MTS_2245_BOUNDARY_QR_KBOUNDARY_TEMPLATE_NONCLAIM.csv"
RUNNER_SMOKE = OUT / "P8_Y5_PARENT_QLOC_2245_RUNNER_SMOKE_STATUS.csv"
PLACEHOLDER_REFUSAL = OUT / "P8_Y5_PARENT_QLOC_2245_PLACEHOLDER_REFUSAL_RUNNER.csv"
CLAIM_GATES = OUT / "P8_Y5_PARENT_QLOC_2245_CLAIM_GATES.csv"
DECISION = OUT / "P8_Y5_PARENT_QLOC_2245_DECISION_LEDGER.csv"
NEXT_TARGET = OUT / "P8_Y5_PARENT_QLOC_2245_NEXT_TARGET.csv"
BRANCH_COPIES = OUT / "P8_Y5_PARENT_QLOC_2245_BRANCH_COPIES.csv"
VALIDATION = OUT / "P8_Y5_BRR545_2245_VALIDATION.csv"


COPY_TARGETS = {
    "queue_boundary": QUEUE / "JR2245_BOUNDARY_QR_KBOUNDARY_TEMPLATE_NONCLAIM.csv",
    "queue_alpha3": QUEUE / "JR2245_ALPHA3_PROJECTION_TEMPLATE_NONCLAIM.csv",
    "branch_wep": MICROSCOPE / "boundary_QR_Kboundary_or_beta_nonclaim_2245.csv",
    "beta_docs": BETA_DOCS / "BOUNDARY_QR_KBOUNDARY_OR_BETA_2245_NONCLAIM.csv",
}


GENERATED = [
    SOURCE_REGISTER,
    COMPACT_PROPER_LEMMA,
    QR_KBOUNDARY_GATE,
    BOUNDARY_RESIDUAL_ROWS,
    FIRST_BETA_PROJECTION,
    ALPHA3_ANCHOR_LEDGER,
    MTS_ALPHA_TEMPLATE,
    RUNNER_SMOKE,
    PLACEHOLDER_REFUSAL,
    CLAIM_GATES,
    DECISION,
    NEXT_TARGET,
    BRANCH_COPIES,
    VALIDATION,
]


def flags() -> dict[str, bool]:
    return {
        "numeric_value_present": False,
        "source_backed": False,
        "score_ready": False,
        "valid_prediction_row": False,
        "valid_for_claim": False,
        "claim_allowed": False,
    }


def rel(path: Path) -> str:
    try:
        return str(path.relative_to(ROOT)).replace("\\", "/")
    except ValueError:
        return str(path)


def resolve_project_path(path_text: str) -> Path:
    path = Path(path_text.strip())
    if path.is_absolute():
        return path
    return ROOT / path


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        raise ValueError(f"no rows for {path}")
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def parse_csv(path: Path) -> bool:
    read_csv(path)
    return True


def validation_pass(path: Path) -> bool:
    if not path.exists():
        return False
    rows = read_csv(path)
    if not rows:
        return False
    id_key = "check_id" if "check_id" in rows[0] else "validation_id"
    result_key = "result" if "result" in rows[0] else "status"
    overall_rows = [row for row in rows if "overall" in row.get(id_key, "").lower() or "summary" in row.get(id_key, "").lower()]
    if overall_rows:
        return all(row.get(result_key, "").lower() == "pass" for row in overall_rows)
    return all(row.get(result_key, "").lower() == "pass" for row in rows)


def source_rows() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for index, (key, path) in enumerate(SOURCE_FILES.items()):
        if key.startswith("2244"):
            role = "current R2FR boundary handoff"
        elif key.startswith("1039"):
            role = "older compact/proper boundary-silence scaffold"
        elif key.startswith(("581", "582", "669", "671", "735", "1019", "976", "977")):
            role = "boundary charge, exactness, or alpha3 provenance evidence"
        else:
            role = "external local bound anchor ledger"
        rows.append(
            {
                "branch_id": BRANCH_ID,
                "source_id": f"SRC2245_{index}_{key}",
                "source_path": rel(path),
                "path_exists": path.exists(),
                "validation_overall_pass": validation_pass(path) if key.endswith("validation") else "",
                "role": role,
                **flags(),
            }
        )
    return rows


def source_register_paths_exist() -> bool:
    return all(resolve_project_path(row["source_path"]).exists() for row in read_csv(SOURCE_REGISTER))


def compact_lemma_rows() -> list[dict[str, Any]]:
    rows = [
        ("QRK2245_0_variational_identity", "For a differentiable local generator G_R[epsilon], the possible obstruction is a finite-jet surface density k_R[delta Y,epsilon] on partial Sigma.", "delta G_R[epsilon]=bulk constraint variation + integral_partialSigma k_R[delta Y,epsilon]; Q_R is chosen to cancel or own this term.", "STRUCTURAL_IDENTITY_CONDITIONAL_ON_PARENT_G", "sets the problem; does not prove silence"),
        ("QRK2245_1_proper_collar_condition", "If epsilon_R and all finite jets entering k_R vanish on an open collar of partial Sigma, every local boundary monomial containing epsilon_R or its jets vanishes pointwise.", "support(epsilon_R) compactly contained in Sigma implies epsilon_R|partialSigma = nabla^a epsilon_R|partialSigma = 0 for required finite derivative order a.", "DERIVED_NARROW_CONDITIONAL_ZERO", "proper compact representative transformations only"),
        ("QRK2245_2_QR_zero", "Under QRK2245_1, Q_R[epsilon]=integral_partialSigma q_R[epsilon]=0 and delta Q_R[epsilon]=0.", "q_R and delta q_R are finite-jet local surface expressions in epsilon_R and fields; the epsilon_R jet factors vanish on the boundary collar.", "DERIVED_NARROW_PROPER_BRANCH_ONLY", "kills representative edge charge for compact local gauge variations, not physical source or large transformations"),
        ("QRK2245_3_Kboundary_zero", "Under QRK2245_1 for both epsilon_R and eta_R, K_boundary[epsilon,eta]=0 for any finite-jet local boundary cocycle.", "the cocycle is a surface bilinear in the generators and finite jets; every boundary term contains a vanished generator jet.", "DERIVED_NARROW_PROPER_BRANCH_ONLY", "compact proper algebra closes with zero boundary cocycle"),
        ("QRK2245_4_GR_charge_guard", "The proper-R_AB zero does not erase observed ADM/time/rotation or GR Hamiltonian charges.", "the vanishing condition applies to representative R_AB parameters only; physical Hamiltonian generators remain in the observed boundary sector.", "GUARD_RETAINED", "prevents deleting GR charges to save the MTS branch"),
        ("QRK2245_5_source_boundary_limit", "The compact/proper lemma does not prove Q_R=0 for source worldtubes, large transformations, reference-boundary terms, or range-kernel weighted edge projections.", "R10 and local source tests can involve nonzero boundary/support data; those terms are exactly the retained residual rows.", "FULL_LOCAL_CLAIM_STILL_BLOCKED", "source/test beta rows remain active"),
        ("QRK2245_6_verdict", "Q_R=0 and K_boundary=0 are derived only for the proper compact representative sub-branch.", "QRK2245_1 through QRK2245_4 close the narrow boundary algebra, while QRK2245_5 blocks promotion to R10/local-GR.", "DERIVED_NARROW_SUBLEMMA_FULL_CLAIM_BLOCKED", "useful GR-reduction hygiene, not an empirical pass"),
    ]
    return [
        {
            "branch_id": BRANCH_ID,
            "lemma_id": lemma_id,
            "statement": statement,
            "derivation": derivation,
            "status": status,
            "claim_scope": scope,
            **flags(),
        }
        for lemma_id, statement, derivation, status, scope in rows
    ]


def qk_gate_rows() -> list[dict[str, Any]]:
    rows = [
        ("QRG2245_0_proper_compact_sublemma", "proper compact representative-R_AB transformations carry no boundary charge or cocycle", "conditional_narrow_pass", "epsilon_R and required finite jets vanish on a boundary collar, forcing Q_R and K_boundary surface densities to vanish", "does not cover source worldtubes, large/non-proper transformations, reference terms, mass projection, or range-kernel edge rows"),
        ("QRG2245_1_full_QR_zero", "Q_R=0 for all local source/test boundaries", "fail_current_claim", "581/671/1019 keep edge and exactness clauses open", "B_R owner, exact primitive, counterterm, reference subtraction, and projector orthogonality remain missing"),
        ("QRG2245_2_full_Kboundary_zero", "K_boundary=0 for source/test or improper edge transformations", "fail_current_claim", "the compact-collar proof only controls finite-jet terms with vanished generator data", "parent Omega and differentiable generator bracket are still not computed"),
    ]
    return [
        {
            "branch_id": BRANCH_ID,
            "gate_id": gate_id,
            "claim": claim,
            "gate_status": status,
            "evidence": evidence,
            "not_enough_because": not_enough,
            **flags(),
        }
        for gate_id, claim, status, evidence, not_enough in rows
    ]


def residual_rows() -> list[dict[str, Any]]:
    rows = [
        ("BRES2245_0_Qbar_edge_RH", "Qbar_edge_RH(lambda)", "Qbar_edge_RH(lambda)=integral_partialSigma F_lambda epsilon_AB B_R^AB with source/reference projection", "non-proper/source boundary values are not killed by the compact representative lemma", "B_R owner; F_lambda kernel; source boundary class; Pi_M/Pi_EH projection; units"),
        ("BRES2245_1_K_boundary_alpha3", "K_boundary_alpha3", "alpha3_MTS=K_boundary_alpha3 * Phi_boundary_local", "the alpha3 preferred-frame anchor is extremely tight and is the cleanest first boundary-flux projection", "K_boundary_alpha3; Phi_boundary_local; projection normalization; theorem-zero or numeric source"),
        ("BRES2245_2_reference_mass_projection", "Pi_M^H[Q_edge]", "mass/Hamiltonian reference projector must be orthogonal to Q_edge or explicitly bounded", "a zero boundary charge proof must not delete physical GR mass/energy charges", "reference subtraction; Pi_M action on edge charge; no-double-count split"),
        ("BRES2245_3_no_double_count", "Q_bulk + Q_edge split", "bulk and edge source terms must be orthogonal or explicitly added in absolute value", "source charge cannot be hidden twice or canceled by bookkeeping", "projection rules and source split"),
    ]
    return [
        {
            "branch_id": BRANCH_ID,
            "residual_id": residual_id,
            "symbol": symbol,
            "formula_or_contract": formula,
            "why_retained": why,
            "missing_inputs": missing,
            **flags(),
        }
        for residual_id, symbol, formula, why, missing in rows
    ]


def first_projection_rows() -> list[dict[str, Any]]:
    rows = [
        ("FBP2245_0_boundary_alpha3", "K_boundary_alpha3 * Phi_boundary_local", "alpha3", "alpha3_MTS=K_boundary_alpha3 * Phi_boundary_local", "local_bound_claims.csv:alpha3 preferred-frame anchor", "4e-20", "K_boundary_alpha3;Phi_boundary_local;normalization;source_path or theorem-zero", "SOURCE_BACKED_ANCHOR_READY_PROJECTION_MISSING"),
        ("FBP2245_1_R10_edge_beta", "Qbar_edge_RH(lambda) * qbar_RT(lambda)", "alpha_R10(lambda)", "|alpha_edge(lambda)| <= |K_R^R10(lambda)| |Qbar_edge_RH(lambda)| |qbar_RT(lambda)| plus absolute tails", "R10_alpha_lambda_bound_curve_1034_REVIEW_CANDIDATE_NONCLAIM.csv", "alpha_bound(lambda) review-candidate curve", "K_R^R10(lambda);Qbar_edge_RH(lambda);qbar_RT(lambda);promoted bound curve;units", "BOUND_CURVE_REVIEW_ONLY_PROJECTION_MISSING"),
        ("FBP2245_2_absolute_tail_gate", "boundary_abs_tail", "all local arenas", "unknown Q_R/K_boundary/source-support components add in absolute value; no cancellation credit", "R10;alpha3;PPN;WEP;clock;Gdot ledgers", "multiple", "component theorem-zero or numeric bound rows", "CLAIM_BLOCKED_UNTIL_COMPONENTS_SOURCE_BACKED"),
    ]
    return [
        {
            "branch_id": BRANCH_ID,
            "projection_id": projection_id,
            "residual_symbol": symbol,
            "observable": observable,
            "projection_formula": formula,
            "empirical_anchor": anchor,
            "bound": bound,
            "required_inputs": required,
            "current_status": status,
            **flags(),
        }
        for projection_id, symbol, observable, formula, anchor, bound, required, status in rows
    ]


def alpha3_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "anchor_id": "A3A2245_0_source_bound",
            "dataset_id": "Will_2014_PPN_alpha3_table",
            "observable": "alpha3",
            "upper_bound": "4e-20",
            "units": "dimensionless",
            "reference": "local_bound_claims.csv / Will 2014 PPN alpha3 anchor",
            "use_in_2245": "anchor only for first beta projection row; not an MTS pass",
            **flags(),
        }
    ]


def alpha_template_rows() -> list[dict[str, Any]]:
    rows = [
        ("MTS_source_normalized_Newton_branch", "proper_compact_QR_Kboundary_zero_sublemma", "ALL_LOCAL_R10_RANGE", "MISSING_EXTENSION_TO_SOURCE_TEST_BOUNDARIES", "Q_R=K_boundary=0 only for compact proper representative-R_AB transformations", "template_invalid_narrow_sublemma_not_full_R10_branch"),
        ("MTS_source_normalized_Newton_branch", "boundary_alpha3_projection_template", "MISSING_NOT_R10_RANGE", "MISSING_K_BOUNDARY_ALPHA3_TIMES_PHI_BOUNDARY_LOCAL", "alpha3_MTS=K_boundary_alpha3 * Phi_boundary_local", "template_invalid_projection_coefficients_missing"),
        ("MTS_source_normalized_Newton_branch", "R10_edge_beta_template", "MISSING_PARENT_LAMBDA_R", "MISSING_KR_QBAR_EDGE_RH_QBAR_RT", "|alpha_edge| <= |K_R^R10| |Qbar_edge_RH| |qbar_RT| plus absolute tails", "template_invalid_edge_projection_missing"),
    ]
    return [
        {
            "branch_id": BRANCH_ID,
            "model_id": model,
            "template_branch": template,
            "lambda_value": lambda_value,
            "alpha_predicted": alpha,
            "force_law_form": law,
            "derivation_status": status,
            **flags(),
        }
        for model, template, lambda_value, alpha, law, status in rows
    ]


def runner_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "smoke_id": "SMOKE2245_0_runner_status",
            "valid_mts_rows": 0,
            "valid_bound_rows": 0,
            "comparison_rows": 1,
            "R10_pass_for_claim": False,
            "expected_result": "blocked_nonclaim",
            **flags(),
        }
    ]


def refusal_rows() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for row in compact_lemma_rows():
        rows.append(
            {
                "branch_id": BRANCH_ID,
                "refusal_id": row["lemma_id"].replace("QRK2245", "REF2245_QRK"),
                "object": row["statement"],
                "current_status": row["status"],
                "refusal_status": "full_boundary_claim_not_promoted",
                "failure_reasons": f"{row['status']};CLAIM_POLICY_FALSE",
                "score_eligible": False,
                **flags(),
            }
        )
    for row in qk_gate_rows():
        rows.append(
            {
                "branch_id": BRANCH_ID,
                "refusal_id": row["gate_id"].replace("QRG2245", "REF2245_QRG"),
                "object": row["claim"],
                "current_status": row["gate_status"],
                "refusal_status": "boundary_gate_not_claim_promoted",
                "failure_reasons": f"{row['not_enough_because']};CLAIM_POLICY_FALSE",
                "score_eligible": False,
                **flags(),
            }
        )
    for row in residual_rows() + first_projection_rows():
        rows.append(
            {
                "branch_id": BRANCH_ID,
                "refusal_id": row.get("residual_id", row.get("projection_id", "REF2245_UNKNOWN")).replace("BRES2245", "REF2245_BRES").replace("FBP2245", "REF2245_FBP"),
                "object": row.get("symbol", row.get("residual_symbol", "")),
                "current_status": row.get("missing_inputs", row.get("current_status", "")),
                "refusal_status": "projection_row_rejected_missing_coefficients",
                "failure_reasons": f"{row.get('missing_inputs', row.get('current_status', 'MISSING_INPUTS'))};SCORE_READY_FALSE",
                "score_eligible": False,
                **flags(),
            }
        )
    return rows


def claim_rows() -> list[dict[str, Any]]:
    rows = [
        ("CGATE2245_0_compact_proper_sublemma", "compact proper representative-R_AB boundary transformations are silent", "conditional_narrow_only", "finite-jet boundary terms vanish when the representative generator and required jets vanish on the boundary collar"),
        ("CGATE2245_1_full_local_GR", "local GR/no-pole boundary branch is fully closed", "false", "source worldtubes, reference/mass projection, exactness, counterterms, parent bracket, and matter/source readout remain unproved"),
        ("CGATE2245_2_alpha3_projection", "K_boundary alpha3 row is score-ready", "false", "alpha3 external anchor exists but K_boundary_alpha3 and Phi_boundary_local are missing"),
        ("CGATE2245_3_R10_edge", "R10 edge beta row is score-ready", "false", "R10 bound curve is review-only and K_R/Qbar_edge/qbar_RT are missing"),
    ]
    return [
        {
            "branch_id": BRANCH_ID,
            "gate_id": gate_id,
            "claim": claim,
            "gate_pass": gate_pass,
            "reason": reason,
            **flags(),
        }
        for gate_id, claim, gate_pass, reason in rows
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "decision_id": "DEC2245_0_boundary_derivation",
            "decision": "A real but narrow boundary result was derived: proper compact representative-R_AB transformations have Q_R=0 and K_boundary=0.",
            "because": "finite-jet boundary charges and cocycles vanish pointwise when the generator and required jets vanish on the boundary collar",
            "next_action": "do not promote to R10/local-GR; attack the non-proper/source boundary formula next",
            **flags(),
        },
        {
            "branch_id": BRANCH_ID,
            "decision_id": "DEC2245_1_empirical_fallback",
            "decision": "The first beta/projection fallback row is alpha3_MTS=K_boundary_alpha3*Phi_boundary_local.",
            "because": "alpha3 has a tight source-backed anchor and older files already isolated this missing K/Phi pair",
            "next_action": "derive or source K_boundary_alpha3 and Phi_boundary_local, or prove both theorem-zero",
            **flags(),
        },
        {
            "branch_id": BRANCH_ID,
            "decision_id": "DEC2245_2_next_target",
            "decision": "Next target should write the parent boundary charge formula rather than inventing a numeric coefficient.",
            "because": "a formula for B_R/Q_R decides both the no-pole route and the K_boundary_alpha3 fallback row",
            "next_action": "2246-Y5-R2FR-RAB-parent-boundary-charge-formula-BR-or-alpha3-projection-bound.md",
            **flags(),
        },
    ]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "next_target": "2246-Y5-R2FR-RAB-parent-boundary-charge-formula-BR-or-alpha3-projection-bound.md",
            "script": "scripts/Y5_R2FR_RAB_parent_boundary_charge_formula_BR_or_alpha3_projection_bound_2246.py",
            "objective": "derive the explicit parent boundary charge density B_R/Q_R from the symplectic potential and allowed boundary class; if this cannot close, build the nonclaim alpha3 projection coefficient row for K_boundary_alpha3 and Phi_boundary_local",
            "include": "Theta_Y boundary term, B_R surface density, exact/proper split, reference subtraction, Pi_M/Pi_EH projection, K_boundary cocycle formula, alpha3 projection normalization",
            "exclude": "invented K_boundary values, deleting GR charges, naked linear c_g scoring, cancellation between residuals, R10/local-GR pass claim, formalization-workbench edits, GitHub action",
            **flags(),
        }
    ]


def copy_rows() -> list[dict[str, Any]]:
    copy_sources = {
        "queue_boundary": BOUNDARY_RESIDUAL_ROWS,
        "queue_alpha3": FIRST_BETA_PROJECTION,
        "branch_wep": FIRST_BETA_PROJECTION,
        "beta_docs": FIRST_BETA_PROJECTION,
    }
    rows: list[dict[str, Any]] = []
    for copy_id, source in copy_sources.items():
        target = COPY_TARGETS[copy_id]
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(source, target)
        rows.append(
            {
                "branch_id": BRANCH_ID,
                "copy_id": copy_id,
                "source_path": rel(source),
                "target_path": rel(target),
                "copied": target.exists(),
                "parse_ok": parse_csv(target),
                **flags(),
            }
        )
    return rows


def generated_flags_false(paths: list[Path]) -> bool:
    false_values = {"", "false", "0", "no", "none", "null", "conditional_narrow_only"}
    keys = ["numeric_value_present", "source_backed", "score_ready", "valid_prediction_row", "valid_for_claim", "claim_allowed"]
    for path in paths:
        for row in read_csv(path):
            for key in keys:
                if key in row and str(row[key]).strip().lower() not in false_values:
                    return False
    return True


def compact_sublemma_present() -> bool:
    statuses = {row["status"] for row in read_csv(COMPACT_PROPER_LEMMA)}
    return "DERIVED_NARROW_PROPER_BRANCH_ONLY" in statuses and "FULL_LOCAL_CLAIM_STILL_BLOCKED" in statuses


def qk_gates_nonclaim() -> bool:
    return all(row.get("claim_allowed", "").lower() == "false" for row in read_csv(QR_KBOUNDARY_GATE))


def residuals_retained() -> bool:
    return any(row.get("symbol") == "K_boundary_alpha3" for row in read_csv(BOUNDARY_RESIDUAL_ROWS))


def first_projection_has_alpha3_anchor() -> bool:
    rows = read_csv(FIRST_BETA_PROJECTION)
    return any(row.get("observable") == "alpha3" and row.get("bound") == "4e-20" and row.get("valid_for_claim", "").lower() == "false" for row in rows)


def claim_gates_blocked() -> bool:
    return all(row.get("claim_allowed", "").lower() == "false" for row in read_csv(CLAIM_GATES))


def remove_pycache() -> None:
    pycache = ROOT / "scripts" / "__pycache__"
    if pycache.exists():
        shutil.rmtree(pycache)


def formalization_2245_artifacts_absent() -> bool:
    if not FORMALIZATION.exists():
        return True
    return not any(
        path.is_file()
        and "2245" in path.name
        and ".venv" not in path.relative_to(FORMALIZATION).parts
        for path in FORMALIZATION.rglob("*")
    )


def formalization_untouched_since_start() -> bool:
    if not FORMALIZATION.exists():
        return True
    return not any(path.is_file() and path.stat().st_mtime >= START_TS for path in FORMALIZATION.rglob("*"))


def source_register_paths_exist() -> bool:
    return all(resolve_project_path(row["source_path"]).exists() for row in read_csv(SOURCE_REGISTER))


def validation_rows(generated_paths: list[Path]) -> list[dict[str, Any]]:
    rows = [
        {
            "branch_id": BRANCH_ID,
            "check_id": "VAL2245_00_sources_exist",
            "result": "PASS" if all(path.exists() for path in SOURCE_FILES.values()) and source_register_paths_exist() else "FAIL",
            "detail": "all direct and registered 2245 source paths exist",
        },
        {
            "branch_id": BRANCH_ID,
            "check_id": "VAL2245_01_prior_validations",
            "result": "PASS" if validation_pass(SOURCE_FILES["2244_validation"]) and validation_pass(SOURCE_FILES["1039_validation"]) else "FAIL",
            "detail": "2244 and 1039 validations pass overall",
        },
        {
            "branch_id": BRANCH_ID,
            "check_id": "VAL2245_02_compact_boundary_sublemma",
            "result": "PASS" if compact_sublemma_present() else "FAIL",
            "detail": "proper compact Q_R/K_boundary zero is derived but source-boundary promotion is blocked",
        },
        {
            "branch_id": BRANCH_ID,
            "check_id": "VAL2245_03_qr_kboundary_gates_nonclaim",
            "result": "PASS" if qk_gates_nonclaim() else "FAIL",
            "detail": "Q_R/K_boundary gates keep all claims non-promoted",
        },
        {
            "branch_id": BRANCH_ID,
            "check_id": "VAL2245_04_boundary_residuals_retained",
            "result": "PASS" if residuals_retained() else "FAIL",
            "detail": "boundary source/test residuals are retained and non-scoreable",
        },
        {
            "branch_id": BRANCH_ID,
            "check_id": "VAL2245_05_first_projection_alpha3_anchor",
            "result": "PASS" if first_projection_has_alpha3_anchor() else "FAIL",
            "detail": "first beta projection uses source-backed alpha3 anchor but remains nonclaim",
        },
        {
            "branch_id": BRANCH_ID,
            "check_id": "VAL2245_06_mts_template_nonclaim",
            "result": "PASS" if all(row.get("valid_for_claim", "").lower() == "false" for row in read_csv(MTS_ALPHA_TEMPLATE)) else "FAIL",
            "detail": "MTS smoke template has no claim-valid rows",
        },
        {
            "branch_id": BRANCH_ID,
            "check_id": "VAL2245_07_runner_smoke_refuses_claim",
            "result": "PASS" if read_csv(RUNNER_SMOKE)[0].get("expected_result") == "blocked_nonclaim" else "FAIL",
            "detail": "runner smoke status refuses a claim",
        },
        {
            "branch_id": BRANCH_ID,
            "check_id": "VAL2245_08_claim_gates_blocked",
            "result": "PASS" if claim_gates_blocked() else "FAIL",
            "detail": "all public/empirical claim gates remain blocked",
        },
        {
            "branch_id": BRANCH_ID,
            "check_id": "VAL2245_09_next_target_written",
            "result": "PASS" if read_csv(NEXT_TARGET)[0]["next_target"].startswith("2246-Y5-R2FR-RAB-parent-boundary-charge") else "FAIL",
            "detail": "next target row is present",
        },
        {
            "branch_id": BRANCH_ID,
            "check_id": "VAL2245_10_csv_parse",
            "result": "PASS" if all(parse_csv(path) for path in generated_paths) else "FAIL",
            "detail": "all generated 2245 CSVs parse cleanly",
        },
        {
            "branch_id": BRANCH_ID,
            "check_id": "VAL2245_11_claim_flags_false",
            "result": "PASS" if generated_flags_false(generated_paths) else "FAIL",
            "detail": "all generated prediction/claim flags remain false",
        },
        {
            "branch_id": BRANCH_ID,
            "check_id": "VAL2245_12_branch_copies",
            "result": "PASS" if all(row["copied"] == "True" and row["parse_ok"] == "True" for row in read_csv(BRANCH_COPIES)) else "FAIL",
            "detail": "branch/quarantine nonclaim copies written",
        },
        {
            "branch_id": BRANCH_ID,
            "check_id": "VAL2245_13_pycache_absent",
            "result": "PASS" if not (ROOT / "scripts" / "__pycache__").exists() else "FAIL",
            "detail": "scripts __pycache__ absent after run",
        },
        {
            "branch_id": BRANCH_ID,
            "check_id": "VAL2245_14_formalization_no_2245",
            "result": "PASS" if formalization_2245_artifacts_absent() else "FAIL",
            "detail": "formalization-workbench has no non-venv 2245 artifacts",
        },
        {
            "branch_id": BRANCH_ID,
            "check_id": "VAL2245_15_formalization_untouched",
            "result": "PASS" if formalization_untouched_since_start() else "FAIL",
            "detail": "formalization-workbench untouched during 2245 run",
        },
    ]
    rows.append(
        {
            "branch_id": BRANCH_ID,
            "check_id": "VAL2245_OVERALL",
            "result": "PASS" if all(row["result"] == "PASS" for row in rows) else "FAIL",
            "detail": "2245 derives the narrow compact/proper Q_R and K_boundary silence sublemma, retains source-boundary residuals, stages alpha3 fallback, and selects parent B_R/Q_R formula next",
        }
    )
    return rows


def md_table(rows: list[dict[str, Any]], columns: list[str]) -> str:
    lines = [
        "| " + " | ".join(columns) + " |",
        "| " + " | ".join("---" for _ in columns) + " |",
    ]
    for row in rows:
        values = [str(row.get(column, "")).replace("\n", " ").replace("|", "\\|") for column in columns]
        lines.append("| " + " | ".join(values) + " |")
    return "\n".join(lines)


def build_doc(
    source: list[dict[str, Any]],
    lemma: list[dict[str, Any]],
    gates: list[dict[str, Any]],
    residuals: list[dict[str, Any]],
    projections: list[dict[str, Any]],
    alpha3: list[dict[str, Any]],
    alpha_template: list[dict[str, Any]],
    runner: list[dict[str, Any]],
    refusal: list[dict[str, Any]],
    claim: list[dict[str, Any]],
    decision: list[dict[str, Any]],
    next_target: list[dict[str, Any]],
    copies: list[dict[str, Any]],
    validation: list[dict[str, Any]],
) -> str:
    return "\n\n".join(
        [
            "# 2245 - Y5/R2FR R_AB Boundary Charge Q_R/Kboundary Zero or Beta-Bound First Row",
            "## Verdict\n"
            "- 2245 derives a real but narrow boundary hygiene result: for proper compact representative-`R_AB` transformations, where the generator and required finite jets vanish on a boundary collar, both `Q_R` and `K_boundary` vanish.\n"
            "- This is not a full local-GR/R10 pass. Source worldtubes, large/non-proper transformations, reference/mass projections, exactness, counterterms, and the parent bracket remain open.\n"
            "- The first concrete fallback projection is `alpha3_MTS=K_boundary_alpha3*Phi_boundary_local`, anchored to the tight `alpha3 <= 4e-20` row but nonclaim until the MTS projection coefficients are derived or sourced.\n"
            "- The result helps the no-pole route without deleting real GR charges or hiding edge/source terms.",
            "## Source Register\n"
            + md_table(source, ["source_id", "source_path", "path_exists", "validation_overall_pass", "role"]),
            "## Compact/Proper Boundary Silence Lemma\n"
            + md_table(lemma, ["lemma_id", "statement", "derivation", "status", "claim_scope"]),
            "## Q_R/Kboundary Claim Gate\n"
            + md_table(gates, ["gate_id", "claim", "gate_status", "evidence", "not_enough_because"]),
            "## Boundary Residual Beta Rows\n"
            + md_table(residuals, ["residual_id", "symbol", "formula_or_contract", "why_retained", "missing_inputs"]),
            "## First Beta Projection Template\n"
            + md_table(projections, ["projection_id", "residual_symbol", "observable", "projection_formula", "empirical_anchor", "bound", "required_inputs", "current_status"]),
            "## Alpha3 Anchor Ledger\n"
            + md_table(alpha3, ["anchor_id", "dataset_id", "observable", "upper_bound", "units", "reference", "use_in_2245"]),
            "## MTS Alpha Smoke Template\n"
            + md_table(alpha_template, ["model_id", "template_branch", "lambda_value", "alpha_predicted", "force_law_form", "derivation_status"]),
            "## Runner Smoke Status\n"
            + md_table(runner, ["smoke_id", "valid_mts_rows", "valid_bound_rows", "comparison_rows", "R10_pass_for_claim", "claim_allowed", "expected_result"]),
            "## Placeholder Refusal Runner\n"
            + md_table(refusal, ["refusal_id", "object", "current_status", "refusal_status", "failure_reasons", "score_eligible", "claim_allowed"]),
            "## Claim Gates\n"
            + md_table(claim, ["gate_id", "claim", "gate_pass", "reason", "claim_allowed"]),
            "## Decision Ledger\n"
            + md_table(decision, ["decision_id", "decision", "because", "next_action"]),
            "## Next Target\n"
            + md_table(next_target, ["next_target", "script", "objective", "include", "exclude"]),
            "## Branch Copies\n"
            + md_table(copies, ["copy_id", "source_path", "target_path", "copied", "parse_ok"]),
            "## Validation\n"
            + md_table(validation, ["check_id", "result", "detail"]),
            "## Working Interpretation\n\n"
            "This is a genuine little win, but it is the sort of win that has teeth because it is bounded. "
            "Proper compact representative changes are silent, so the no-pole branch is cleaner locally. "
            "But source and edge boundaries are still exactly where the theory can leak, so the next target has to write the actual `B_R/Q_R` surface density rather than pretending the compact lemma covers everything.",
            "",
        ]
    )


def main() -> None:
    source = source_rows()
    lemma = compact_lemma_rows()
    gates = qk_gate_rows()
    residuals = residual_rows()
    projections = first_projection_rows()
    alpha3 = alpha3_rows()
    alpha_template = alpha_template_rows()
    runner = runner_rows()
    refusal = refusal_rows()
    claim = claim_rows()
    decision = decision_rows()
    next_target = next_target_rows()

    write_csv(SOURCE_REGISTER, source)
    write_csv(COMPACT_PROPER_LEMMA, lemma)
    write_csv(QR_KBOUNDARY_GATE, gates)
    write_csv(BOUNDARY_RESIDUAL_ROWS, residuals)
    write_csv(FIRST_BETA_PROJECTION, projections)
    write_csv(ALPHA3_ANCHOR_LEDGER, alpha3)
    write_csv(MTS_ALPHA_TEMPLATE, alpha_template)
    write_csv(RUNNER_SMOKE, runner)
    write_csv(PLACEHOLDER_REFUSAL, refusal)
    write_csv(CLAIM_GATES, claim)
    write_csv(DECISION, decision)
    write_csv(NEXT_TARGET, next_target)
    copies = copy_rows()
    write_csv(BRANCH_COPIES, copies)

    remove_pycache()
    generated_before_validation = [path for path in GENERATED if path != VALIDATION]
    validation = validation_rows(generated_before_validation)
    write_csv(VALIDATION, validation)
    remove_pycache()

    DOC.write_text(
        build_doc(
            source,
            lemma,
            gates,
            residuals,
            projections,
            alpha3,
            alpha_template,
            runner,
            refusal,
            claim,
            decision,
            next_target,
            copies,
            validation,
        ),
        encoding="utf-8",
    )

    if not validation_pass(VALIDATION):
        raise SystemExit(f"2245 validation failed: {VALIDATION}")


if __name__ == "__main__":
    main()

from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


RUN_UTC = datetime.now(timezone.utc).isoformat()
ROOT = Path(__file__).resolve().parents[1]
PROJECT = ROOT.parent
RESIDUALS = ROOT / "source-intake" / "mts_residuals"
PARENT_ACTION = ROOT / "source-intake" / "parent-action"
LOCAL_BOUNDS = ROOT / "source-intake" / "local_bounds"
RAB_QUEUE = ROOT / "source-intake" / "rab-sector" / "acquisition-queue"
MICRO_COEFF = ROOT / "source-intake" / "microscope" / "branch_locked_wep" / "coefficients"
FORMALIZATION = PROJECT / "formalization-workbench"

CHECKPOINT = "2991"
BRANCH_ID = "MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428"

DOC = ROOT / "2991-Y5-R2FR-fixed-boundary-reference-theta-zero-proof-or-epsilon-Bv-source-bound-under-AX1090.md"

SRC_2990_DOC = ROOT / "2990-Y5-R2FR-sector-normal-form-branch-selection-or-first-epsilon-theta-numeric-source-row-under-AX1090.md"
SRC_2990_NEXT = RESIDUALS / "P8_Y5_R2FR_2990_NEXT_TARGET.csv"
SRC_2990_NORMAL = RESIDUALS / "P8_Y5_R2FR_2990_SELECTED_PARENT_NORMAL_FORM_CONTRACT.csv"
SRC_2990_SECTOR = RESIDUALS / "P8_Y5_R2FR_2990_SECTOR_BY_SECTOR_THETA_NORMAL_FORM_CONTRACT.csv"
SRC_2990_ACQ = RESIDUALS / "P8_Y5_R2FR_2990_FIRST_EPSILON_THETA_SOURCE_ROW_ACQUISITION_NONCLAIM.csv"
SRC_2545_EXACT = RESIDUALS / "P8_Y5_NO_SHADOW_2545_EXACT_IMPROVEMENT_CANCELLATION_DERIVATION.csv"
SRC_2546_CLASS = RESIDUALS / "P8_Y5_NO_SHADOW_2546_BOUNDARY_TERM_CLASSIFICATION.csv"
SRC_2546_MATRIX = RESIDUALS / "P8_Y5_NO_SHADOW_2546_BOUNDARY_CERTIFICATE_MATRIX.csv"
SRC_2547_SELECTOR = RESIDUALS / "P8_Y5_NO_SHADOW_2547_FIXED_REFERENCE_SELECTOR_THEOREM.csv"
SRC_2547_SIGNATURE = RESIDUALS / "P8_Y5_NO_SHADOW_2547_SIGNATURE_AUDIT.csv"
SRC_2547_DIRICHLET = RESIDUALS / "P8_Y5_NO_SHADOW_2547_DIRICHLET_ACTION_CONTRACT.csv"
SRC_2447_ZERO = RESIDUALS / "P8_Y5_PARENT_QLOC_2447_BOUNDARY_REFERENCE_S_EQ_ZERO_THEOREM_GATE.csv"
SRC_2448_OWNER = RESIDUALS / "P8_Y5_PARENT_QLOC_2448_BREF_RELATIVE_BOUNDARY_OWNER_CONTRACT.csv"
SRC_2455_EMBEDDING = RESIDUALS / "P8_Y5_PARENT_QLOC_2455_BOUNDARY_REFERENCE_EMBEDDING_DERIVATION.csv"
SRC_2544_BZERO = RESIDUALS / "P8_Y5_NO_SHADOW_2544_BZERO_NOFLUX_THEOREM_AUDIT.csv"
SRC_2544_DENOM = RESIDUALS / "P8_Y5_NO_SHADOW_2544_BOUNDARY_DENOMINATOR_DEPENDENCY.csv"

LIVE_C_PARENT = MICRO_COEFF / "C_parent_WEP_slot_import.csv"

OUTPUTS = {
    "sources": RESIDUALS / "P8_Y5_R2FR_2991_SOURCE_REGISTER.csv",
    "proof_chain": RESIDUALS / "P8_Y5_R2FR_2991_FIXED_BOUNDARY_THETA_ZERO_PROOF_CHAIN.csv",
    "clause_audit": RESIDUALS / "P8_Y5_R2FR_2991_BOUNDARY_REFERENCE_CLAUSE_AUDIT.csv",
    "epsilon": RESIDUALS / "P8_Y5_R2FR_2991_EPSILON_BV_SOURCE_BOUND_ROWS_NONCLAIM.csv",
    "gates": RESIDUALS / "P8_Y5_R2FR_2991_PROMOTION_GATES.csv",
    "decision": RESIDUALS / "P8_Y5_R2FR_2991_DECISION_LEDGER.csv",
    "next": RESIDUALS / "P8_Y5_R2FR_2991_NEXT_TARGET.csv",
    "branches": RESIDUALS / "P8_Y5_R2FR_2991_BRANCH_COPIES.csv",
    "validation": RESIDUALS / "P8_Y5_BRR545_2991_VALIDATION.csv",
}

BRANCH_OUTPUTS = {
    "proof_copy": PARENT_ACTION / "fixed_boundary_reference_theta_zero_attempt_2991_NOT_SIGNED.csv",
    "epsilon_copy": LOCAL_BOUNDS / "epsilon_Bv_source_bound_rows_2991_NONCLAIM.csv",
    "next_copy": RAB_QUEUE / "JR2991_extra_double_zero_or_epsilon_Qv_extra_next_NONCLAIM.csv",
}

for directory in {p.parent for p in OUTPUTS.values()} | {p.parent for p in BRANCH_OUTPUTS.values()} | {DOC.parent}:
    directory.mkdir(parents=True, exist_ok=True)


def text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace") if path.exists() else ""


def rows(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def anchors(path: Path, needles: list[str]) -> bool:
    haystack = text(path)
    return path.exists() and all(needle in haystack for needle in needles)


def add(row: dict[str, Any]) -> dict[str, Any]:
    return {
        **row,
        "checkpoint": CHECKPOINT,
        "branch_id": BRANCH_ID,
        "control_only": True,
        "score_ready": False,
        "valid_prediction_row": False,
        "valid_for_claim": False,
        "claim_allowed": False,
        "generated_utc": RUN_UTC,
    }


def write_csv(path: Path, out_rows: list[dict[str, Any]]) -> None:
    fieldnames: list[str] = []
    for row in out_rows:
        for key in row:
            if key not in fieldnames:
                fieldnames.append(key)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(out_rows)


def csv_ok(path: Path) -> bool:
    try:
        rows(path)
        return True
    except Exception:
        return False


def under(path: Path, parent: Path) -> bool:
    try:
        path.resolve().relative_to(parent.resolve())
        return True
    except ValueError:
        return False


def source_rows() -> list[dict[str, Any]]:
    specs = [
        ("SRC2991_00_2990_doc", SRC_2990_DOC, ["NEXT2990_0_2991", "epsilon_Bv_ambiguity"], "2990 boundary handoff"),
        ("SRC2991_01_2990_next", SRC_2990_NEXT, ["NEXT2990_0_2991", "fixed exact/topological boundary"], "selected 2991 target"),
        ("SRC2991_02_2990_normal", SRC_2990_NORMAL, ["NF2990_2_boundary", "FIRST_PROOF_TARGET_NOT_SIGNED"], "selected normal-form boundary clause"),
        ("SRC2991_03_2990_sector", SRC_2990_SECTOR, ["SNF2990_1_boundary", "epsilon_Bv_ambiguity"], "sector-by-sector boundary theta row"),
        ("SRC2991_04_2990_acq", SRC_2990_ACQ, ["ACQ2990_0_first_target_boundary", "MISSING_FIXED_REFERENCE_NO_FLUX_PROOF"], "epsilon_Bv acquisition target"),
        ("SRC2991_05_2545_exact", SRC_2545_EXACT, ["EIC2545_3_k_invariance", "Hamiltonian surface one-form cancellation"], "exact-improvement cancellation derivation"),
        ("SRC2991_06_2546_class", SRC_2546_CLASS, ["BTC2546_0_exact_improvement", "CONDITIONAL_ZERO_CLASS"], "boundary term classification"),
        ("SRC2991_07_2546_matrix", SRC_2546_MATRIX, ["BCC2546_0_parent_primitive", "MISSING_PARENT_PRIMITIVE"], "boundary certificate matrix"),
        ("SRC2991_08_2547_selector", SRC_2547_SELECTOR, ["FRS2547_0_selector_object", "DEFINITION_CONTRACT_NOT_PARENT_SIGNED"], "fixed reference selector theorem"),
        ("SRC2991_09_2547_signature", SRC_2547_SIGNATURE, ["SIG2547_0_configuration_bundle", "BLOCKED_NONCLAIM"], "fixed reference signature audit"),
        ("SRC2991_10_2547_dirichlet", SRC_2547_DIRICHLET, ["DAC2547_2_variation_domain", "CONDITIONAL_ONLY"], "Dirichlet fixed-reference action contract"),
        ("SRC2991_11_2447_zero", SRC_2447_ZERO, ["BZ2447_0_parent_boundary_phase_space", "BZ2447_7_verdict"], "boundary reference zero theorem gate"),
        ("SRC2991_12_2448_owner", SRC_2448_OWNER, ["RBO2448_0_parent_boundary_action", "RBO2448_7_verdict"], "B_ref and relative boundary owner contract"),
        ("SRC2991_13_2455_embedding", SRC_2455_EMBEDDING, ["EMB2455_2_zero_condition", "EMB2455_5_verdict"], "source-blind boundary embedding derivation"),
        ("SRC2991_14_2544_bzero", SRC_2544_BZERO, ["BZT2544_6_verdict", "ZERO_THEOREM_NOT_DERIVED"], "Bzero no-flux theorem audit"),
        ("SRC2991_15_2544_denom", SRC_2544_DENOM, ["BDD2544_2_MHref", "MISSING_M_H_REF"], "boundary denominator dependency"),
    ]
    return [
        add(
            {
                "source_id": source_id,
                "source_path": str(path),
                "role": role,
                "required_anchors": ";".join(needles),
                "exists": path.exists(),
                "anchors_found": anchors(path, needles),
            }
        )
        for source_id, path, needles, role in specs
    ]


def proof_chain_rows() -> list[dict[str, Any]]:
    data = [
        (
            "FBZ2991_0_target",
            "fixed-boundary theta-zero target",
            "Show int_S i_v(delta B_ref or Theta_boundary)=0 for compact linked local collars.",
            "TARGET_SHARP",
            "requires exact/fixed boundary class plus parent-owned vertical action, tau, surface and M_ref",
            False,
        ),
        (
            "FBZ2991_1_exact_improvement",
            "exact boundary improvement cancellation",
            "If L' = L+dmu, theta'=theta+delta mu and Q_tau'=Q_tau+i_tau mu, then delta Q_tau'-i_tau theta'=delta Q_tau-i_tau theta when [delta,i_tau]=0.",
            "CONDITIONAL_ZERO_DERIVED_NOT_CLAIM",
            "covers only exact improvements with fixed tau/surface and no corner anomaly",
            False,
        ),
        (
            "FBZ2991_2_fixed_Bref_chain_rule",
            "fixed reference chain rule",
            "If beta_ref=(S,sigma_AB,tau,C_top,B_ct)=beta_0 is parent-selected before readout and D_v beta_ref=0, then delta_v B_ref[beta_ref]=0.",
            "EXACT_CONDITIONAL_CONTRACT_NOT_PARENT_SIGNED",
            "current corpus lacks parent signature for beta_0, source-blind surface/domain, metric, tau/coframe and counterterm",
            False,
        ),
        (
            "FBZ2991_3_theta_boundary_zero",
            "boundary theta component",
            "Theta_boundary(v)=delta_v B_ref is zero only for the fixed exact/topological component satisfying FBZ2991_1..2.",
            "PARTIAL_COMPONENT_ZERO_ONLY",
            "corner, harmonic/topological, field-dependent tau/surface, unfixed reference and no-flux channels remain",
            False,
        ),
        (
            "FBZ2991_4_no_total_Bv_zero",
            "full epsilon_Bv zero theorem",
            "epsilon_Bv_ambiguity=0 would require every boundary/reference/improvement component to be exact/fixed/proper or source-bounded in one branch.",
            "TOTAL_BV_ZERO_NOT_DERIVED",
            "actual MTS boundary representative is not fully classified and fixed-reference signatures remain blocked",
            False,
        ),
        (
            "FBZ2991_5_verdict",
            "current boundary/reference theta result",
            "Carry forward the exact/fixed component cancellation, but retain epsilon_Bv_ambiguity as an explicit nonclaim residual.",
            "BV_TOTAL_NOT_CLOSED_RETAIN_EPSILON_BV",
            "do not promote Theta_parent, Omega, V_WEP, local GR or Newton from the boundary piece",
            False,
        ),
    ]
    return [
        add(
            {
                "proof_id": proof_id,
                "step": step,
                "mathematical_statement": statement,
                "current_status": status,
                "blocking_gap": gap,
                "theorem_zero_claimed": theorem_zero,
            }
        )
        for proof_id, step, statement, status, gap, theorem_zero in data
    ]


def clause_audit_rows() -> list[dict[str, Any]]:
    data = [
        ("BCA2991_0_exact_primitive", "actual boundary term has parent primitive mu or d_S b", "CONDITIONAL_ONLY", "exact component can cancel", "actual MTS boundary representative not fully classified", "epsilon_Bv_exact_commutator"),
        ("BCA2991_1_fixed_tau", "tau is fixed under the vertical/local variation", "MISSING_TAU_COFRAME_LOCK", "needed for [delta,i_tau]=0", "field-dependent tau creates commutator residual", "epsilon_Bv_tau_surface_commutator"),
        ("BCA2991_2_fixed_surface", "integration surface/collar is fixed before source/readout", "MISSING_SOURCE_BLIND_SURFACE_DOMAIN_RULE", "needed to avoid moving-boundary leakage", "surface/radius drift remains legal", "epsilon_Bv_tau_surface_commutator"),
        ("BCA2991_3_no_corner", "corner/codimension-two anomaly absent or paired", "UNCLASSIFIED_RETAINS_BOUND_ROW", "needed to use exact-improvement cancellation without edge remainder", "corner term can carry finite charge", "epsilon_Bv_corner_abs"),
        ("BCA2991_4_topological_class", "relative/topological class fixed before readout", "MISSING_CTOP_SUPERSELECTION", "needed to stop closed-but-not-exact flux", "topological/harmonic class can carry source-independent but nonzero charge", "epsilon_Bv_topological_abs"),
        ("BCA2991_5_Bref_qblind", "B_ref has no q/source/frame/radius/lambda derivative", "MISSING_PARENT_BREF_RULE", "needed to make delta_v B_ref=0 by chain rule", "reference can be a post-hoc cancellation knob", "epsilon_Bv_unfixed_reference"),
        ("BCA2991_6_projector_boundary", "projector/source-measure boundary contribution silent", "MISSING_PROJECTOR_BOUNDARY_SILENCE", "needed because boundary and Pi_M live on same surface", "delta Pi_M boundary stress can survive", "epsilon_Bv_projector_boundary"),
        ("BCA2991_7_denominator", "positive same-frame M_ref or M_H_ref exists", "MISSING_POSITIVE_SAME_FRAME_MREF", "needed to score epsilon_Bv", "zero numerator alone does not supply Newton/GR source normalization", "epsilon_Bv_denominator"),
        ("BCA2991_8_total", "all boundary clauses close together", "BOUNDARY_TOTAL_NOT_SIGNED", "would close epsilon_Bv", "at least six clauses remain unsigned", "epsilon_Bv_total_abs"),
    ]
    return [
        add(
            {
                "clause_id": clause_id,
                "clause": clause,
                "current_status": status,
                "if_closed": effect,
                "if_open": gap,
                "residual_symbol": residual,
                "clause_passed_now": status == "CONDITIONAL_ONLY",
            }
        )
        for clause_id, clause, status, effect, gap, residual in data
    ]


def epsilon_rows() -> list[dict[str, Any]]:
    data = [
        (
            "EBV2991_00_definition",
            "epsilon_Bv_ambiguity",
            "boundary/reference/improvement contribution to missing theta/current surface row",
            "epsilon_Bv_ambiguity <= sum_abs(EBV2991_01..07); no cancellation between components",
            "dimensionless_after_M_ref",
            "BOUNDARY_TOTAL_NOT_SIGNED",
            "VSP2903_1_Bv;ETH2989_02_boundary",
        ),
        (
            "EBV2991_01_exact_component",
            "epsilon_Bv_exact_commutator",
            "exact-improvement component left after k_tau invariance",
            "0 only if B=dmu, tau and surface fixed, no corner anomaly, [delta,i_tau]=0",
            "dimensionless_exact_guard",
            "CONDITIONAL_ZERO_NOT_CLAIM",
            "EIC2545_3_k_invariance",
        ),
        (
            "EBV2991_02_corner",
            "epsilon_Bv_corner_abs",
            "corner/codimension-two boundary contribution",
            "abs(int_corner K_corner)/M_ref",
            "dimensionless_corner_charge",
            "MISSING_CORNER_CLASSIFICATION_OR_BOUND",
            "BTC2546_corner_class",
        ),
        (
            "EBV2991_03_topological",
            "epsilon_Bv_topological_abs",
            "closed-but-not-exact or harmonic/topological boundary class",
            "abs(Delta C_top or harmonic boundary flux)/M_ref",
            "dimensionless_topological_charge",
            "MISSING_CTOP_SUPERSELECTION_OR_BOUND",
            "RBO2448_1_Ctop_superselection",
        ),
        (
            "EBV2991_04_tau_surface",
            "epsilon_Bv_tau_surface_commutator",
            "field-dependent tau or moving surface/collar commutator leakage",
            "abs(int_S([delta,i_tau]mu + moving_surface_term))/M_ref",
            "dimensionless_commutator_charge",
            "MISSING_TAU_SURFACE_LOCK",
            "SIG2547_1_boundary_surface;SIG2547_3_tau_coframe",
        ),
        (
            "EBV2991_05_unfixed_reference",
            "epsilon_Bv_unfixed_reference",
            "q/source/frame/radius dependent reference subtraction",
            "abs(D_v B_ref)/M_ref with derivative vector absolute-summed",
            "dimensionless_reference_drift",
            "MISSING_PARENT_BREF_RULE",
            "BDV2448_derivative_vector;VDT2457_2_chain_rule_to_Bref",
        ),
        (
            "EBV2991_06_projector_boundary",
            "epsilon_Bv_projector_boundary",
            "projector/source-measure boundary symplectic leakage",
            "abs(int_S delta Pi_M boundary + [d,Pi_M]J_H boundary)/M_ref",
            "dimensionless_projector_boundary_charge",
            "MISSING_PROJECTOR_BOUNDARY_SILENCE",
            "BZ2447_5_projector_symplectic_silence",
        ),
        (
            "EBV2991_07_denominator",
            "epsilon_Bv_denominator",
            "positive same-frame M_ref/M_H_ref missing for boundary scoring",
            "normalization guard for all epsilon_Bv components",
            "dimensionless_normalization_guard",
            "MISSING_POSITIVE_SAME_FRAME_MREF",
            "BDD2544_2_MHref",
        ),
        (
            "EBV2991_08_total",
            "epsilon_Bv_total_abs",
            "source-ready total boundary theta residual",
            "sum_abs(EBV2991_01..07)",
            "dimensionless_after_M_ref",
            "MISSING_SOURCE_BACKED_UPPER_BOUND",
            "EBV2991_00_definition",
        ),
    ]
    return [
        add(
            {
                "epsilon_id": eps_id,
                "symbol": symbol,
                "definition": definition,
                "bound_interface": formula,
                "units": units,
                "current_status": status,
                "current_value": "CONDITIONAL_ZERO_NOT_CLAIM" if eps_id == "EBV2991_01_exact_component" else "MISSING_SOURCE_BACKED_UPPER_BOUND",
                "lower_bound": "0",
                "upper_bound": "MISSING_SOURCE_BACKED_UPPER_BOUND",
                "source_anchor": anchor,
                "source_ready_template": True,
                "finite_value_present": False,
                "theorem_zero_claimed": False,
                "no_cancellation_policy": True,
            }
        )
        for eps_id, symbol, definition, formula, units, status, anchor in data
    ]


def gate_rows() -> list[dict[str, Any]]:
    data = [
        ("GATE2991_0_exact_improvement_component", "exact-improvement cancellation law available as conditional algebra", True, "CONDITIONAL_COMPONENT_ZERO_ONLY"),
        ("GATE2991_1_parent_boundary_owner", "parent boundary action owns B_ref and relative class", False, "MISSING_PARENT_BOUNDARY_ACTION_OWNER"),
        ("GATE2991_2_fixed_tau_surface", "tau and compact collar surface fixed before readout/source", False, "MISSING_TAU_SURFACE_LOCK"),
        ("GATE2991_3_no_corner_harmonic", "corner and harmonic/topological classes absent/fixed/bounded", False, "MISSING_CORNER_TOPOLOGICAL_CLASSIFICATION"),
        ("GATE2991_4_Bref_derivative_vector", "D_v B_ref derivative vector vanishes", False, "MISSING_PARENT_BREF_RULE"),
        ("GATE2991_5_projector_boundary", "projector/source-measure boundary contribution silent", False, "MISSING_PROJECTOR_BOUNDARY_SILENCE"),
        ("GATE2991_6_Mref", "positive same-frame M_ref/M_H_ref exists", False, "MISSING_POSITIVE_SAME_FRAME_MREF"),
        ("GATE2991_7_promote_Bv_zero", "promote epsilon_Bv_ambiguity=0", False, "all boundary closure gates must pass"),
        ("GATE2991_8_promote_local_GR", "promote Theta/Omega/local-GR branch", False, "not allowed from boundary-only checkpoint"),
    ]
    return [
        add(
            {
                "gate_id": gate_id,
                "gate": gate,
                "condition_passed": passed,
                "status": status,
                "promotion_allowed_now": False,
            }
        )
        for gate_id, gate, passed, status in data
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        add(
            {
                "decision_id": "DEC2991_0_real_gain",
                "decision": "Keep the exact-improvement cancellation as a real conditional component result.",
                "because": "the algebra delta(i_tau mu)-i_tau(delta mu)=0 under fixed tau/surface/no-corner clauses is valid and useful.",
                "next_action": "do not lose this gain, but do not upgrade it to full B_ref silence.",
            }
        ),
        add(
            {
                "decision_id": "DEC2991_1_total_boundary",
                "decision": "Do not promote epsilon_Bv_ambiguity=0.",
                "because": "actual MTS boundary terms are not fully classified and fixed-reference ownership, tau/surface, corner/topological, projector and M_ref clauses remain unsigned.",
                "next_action": "retain epsilon_Bv_total_abs as a source-ready nonclaim residual.",
            }
        ),
        add(
            {
                "decision_id": "DEC2991_2_next_sector",
                "decision": "Move next to the extra-sector double-zero/zero-odd-source route rather than circling boundary again.",
                "because": "boundary now has a clean component result plus explicit residual pack; local GR still needs the extra motion/time sector to be silent at linear order.",
                "next_action": "build 2992 around extra double-zero proof or epsilon_Qv_extra_piece bound rows.",
            }
        ),
    ]


def next_rows() -> list[dict[str, Any]]:
    return [
        add(
            {
                "next_id": "NEXT2991_0_2992",
                "priority": "selected_primary",
                "next_doc": "2992-Y5-R2FR-extra-double-zero-and-zero-odd-source-proof-or-epsilon-Qv-extra-bound-under-AX1090.md",
                "next_script": "scripts/Y5_R2FR_extra_double_zero_and_zero_odd_source_proof_or_epsilon_Qv_extra_bound_under_AX1090_2992.py",
                "objective": "Try to prove the silent quadratic extra-sector normal form gives first variation zero, no linear stress/readout/source vertex, and no exchange-odd local source; if not, stage epsilon_Qv_extra_piece bound rows without claiming local GR.",
                "include": "Z=0 branch;positive Hessian;dL_extra|0=0;no linear metric stress;no linear readout;zero odd source;boundary no-flux carryover;epsilon_Qv_extra fallback",
                "exclude": "C_parent import;Omega promotion;V_WEP promotion;local-GR claim;Newton claim;public/GitHub action;formalization-workbench edits",
            }
        )
    ]


def branch_rows() -> list[dict[str, Any]]:
    return [add({"copy_id": key, "path": str(path), "exists": path.exists()}) for key, path in BRANCH_OUTPUTS.items()]


def validation(all_rows: dict[str, list[dict[str, Any]]]) -> list[dict[str, Any]]:
    csv_paths = [*OUTPUTS.values(), *BRANCH_OUTPUTS.values()]
    generated = [*csv_paths, DOC]
    formal_count = sum(1 for path in FORMALIZATION.rglob("*2991*") if path.is_file()) if FORMALIZATION.exists() else 0
    component_gain = any(
        row["proof_id"] == "FBZ2991_1_exact_improvement"
        and row["current_status"] == "CONDITIONAL_ZERO_DERIVED_NOT_CLAIM"
        and not row["theorem_zero_claimed"]
        for row in all_rows["proof_chain"]
    )
    total_not_closed = any(
        row["proof_id"] == "FBZ2991_5_verdict"
        and row["current_status"] == "BV_TOTAL_NOT_CLOSED_RETAIN_EPSILON_BV"
        for row in all_rows["proof_chain"]
    )
    epsilon_nonclaim = all(
        row["source_ready_template"]
        and not row["valid_for_claim"]
        and not row["claim_allowed"]
        and not row["theorem_zero_claimed"]
        for row in all_rows["epsilon"]
    )
    checks = [
        ("VAL2991_0_sources_exist", all(row["exists"] for row in all_rows["sources"]), "all cited local source paths exist", True),
        ("VAL2991_1_anchors_found", all(row["anchors_found"] for row in all_rows["sources"]), "all cited source anchors found", True),
        ("VAL2991_2_component_gain_retained", component_gain, "exact-improvement component zero retained only conditionally", True),
        ("VAL2991_3_total_Bv_not_closed", total_not_closed, "full epsilon_Bv zero theorem not promoted", True),
        ("VAL2991_4_eps_source_ready_nonclaim", epsilon_nonclaim, "epsilon_Bv rows source-ready but nonclaim", True),
        ("VAL2991_5_no_promotion", all(not row["promotion_allowed_now"] for row in all_rows["gates"]), "no boundary or local-GR promotion allowed", True),
        ("VAL2991_6_no_live_cparent", not LIVE_C_PARENT.exists(), "C_parent_WEP_slot_import.csv not created or promoted", True),
        ("VAL2991_7_next_written", any(row["next_id"] == "NEXT2991_0_2992" for row in all_rows["next"]), "2992 next target written", True),
        ("VAL2991_8_branches_exist", all(row["exists"] for row in all_rows["branches"]), "branch copies exist", True),
        ("VAL2991_9_csvs_parse", all(csv_ok(path) for path in csv_paths), "all generated CSVs parse", True),
        ("VAL2991_10_outputs_under_post", all(under(path, ROOT) for path in generated), "all generated outputs under post-checkpoint-work", True),
        ("VAL2991_11_formalization_clean", formal_count == 0, f"no 2991 outputs in formalization-workbench (count={formal_count})", True),
        ("VAL2991_12_doc_written", DOC.exists(), "2991 markdown checkpoint exists", True),
    ]
    out_rows = [add({"validation_id": check_id, "passed": bool(passed), "check": check, "required": required}) for check_id, passed, check, required in checks]
    out_rows.append(add({"validation_id": "VAL2991_OVERALL", "passed": all(row["passed"] for row in out_rows), "check": "2991 validation overall", "required": True}))
    return out_rows


def esc(value: Any) -> str:
    return str(value).replace("|", "\\|").replace("\n", "<br>")


def table(out_rows: list[dict[str, Any]], cols: list[str]) -> str:
    if not out_rows:
        return "_No rows._"
    return "\n".join(
        [
            "| " + " | ".join(cols) + " |",
            "| " + " | ".join("---" for _ in cols) + " |",
            *["| " + " | ".join(esc(row.get(col, "")) for col in cols) + " |" for row in out_rows],
        ]
    )


def write_markdown(all_rows: dict[str, list[dict[str, Any]]]) -> None:
    outputs = [{"output": key, "path": str(path), "exists": path.exists()} for key, path in OUTPUTS.items() if key != "validation"]
    branches = [{"copy": key, "path": str(path), "exists": path.exists()} for key, path in BRANCH_OUTPUTS.items()]
    DOC.write_text(
        f"""# 2991 - Fixed Boundary/Reference Theta-Zero Proof or epsilon_Bv Source Bound

Status: `Y5_R2FR_2991_exact_boundary_improvement_component_zero_retained_conditionally_full_Bv_not_closed_epsilon_Bv_rows_staged_nonclaim`

Claim ceiling: `no_full_Bv_zero_claim_no_Theta_parent_promotion_no_Omega_promotion_no_parent_generator_no_VWEP_promotion_no_Cparent_import_no_local_GR_no_Newton_no_WEP_no_R10_no_PPN_no_clock_no_orbital_no_public_claim`

## Summary

- The real gain is narrow but useful: exact boundary improvements cancel in the Hamiltonian surface one-form when `tau`, the surface, and the corner class are fixed.
- In current `Theta_parent` language, this gives a conditional zero for the exact/fixed component of `epsilon_Bv_ambiguity`.
- The full boundary/reference sector still does not close because the actual MTS boundary representative is not fully classified and fixed-reference ownership, corner/topological, projector, tau/surface and `M_ref` clauses remain unsigned.
- Therefore `epsilon_Bv_ambiguity` is retained as an explicit nonclaim residual, now split into component rows rather than one foggy boundary objection.

## Generated Outputs

{table(outputs, ["output", "path", "exists"])}

## Branch Copies

{table(branches, ["copy", "path", "exists"])}

## Fixed Boundary Theta-Zero Proof Chain

{table(all_rows["proof_chain"], ["proof_id", "step", "current_status", "blocking_gap", "theorem_zero_claimed"])}

## Boundary Reference Clause Audit

{table(all_rows["clause_audit"], ["clause_id", "clause", "current_status", "if_open", "residual_symbol"])}

## epsilon_Bv Source-Bound Rows

{table(all_rows["epsilon"], ["epsilon_id", "symbol", "definition", "bound_interface", "current_status", "current_value"])}

## Promotion Gates

{table(all_rows["gates"], ["gate_id", "gate", "condition_passed", "status", "promotion_allowed_now"])}

## Decision Ledger

{table(all_rows["decision"], ["decision_id", "decision", "because", "next_action"])}

## Next Target

{table(all_rows["next"], ["next_id", "priority", "next_doc", "next_script", "objective", "exclude"])}

## Validation

{table(all_rows["validation"], ["validation_id", "passed", "check", "required"])}

Validation overall: `{all_rows["validation"][-1]["passed"]}`.
""",
        encoding="utf-8",
    )


def main() -> None:
    all_rows: dict[str, list[dict[str, Any]]] = {
        "sources": source_rows(),
        "proof_chain": proof_chain_rows(),
        "clause_audit": clause_audit_rows(),
        "epsilon": epsilon_rows(),
        "gates": gate_rows(),
        "decision": decision_rows(),
        "next": next_rows(),
    }
    for key, path in OUTPUTS.items():
        if key in {"branches", "validation"}:
            continue
        write_csv(path, all_rows[key])
    shutil.copyfile(OUTPUTS["proof_chain"], BRANCH_OUTPUTS["proof_copy"])
    shutil.copyfile(OUTPUTS["epsilon"], BRANCH_OUTPUTS["epsilon_copy"])
    shutil.copyfile(OUTPUTS["next"], BRANCH_OUTPUTS["next_copy"])
    all_rows["branches"] = branch_rows()
    write_csv(OUTPUTS["branches"], all_rows["branches"])
    all_rows["validation"] = validation(all_rows)
    write_csv(OUTPUTS["validation"], all_rows["validation"])
    write_markdown(all_rows)
    all_rows["validation"] = validation(all_rows)
    write_csv(OUTPUTS["validation"], all_rows["validation"])
    write_markdown(all_rows)
    print(f"2991 validation overall: {all_rows['validation'][-1]['passed']}")
    print(DOC)


if __name__ == "__main__":
    main()

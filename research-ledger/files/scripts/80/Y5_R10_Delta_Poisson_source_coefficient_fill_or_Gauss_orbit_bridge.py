from __future__ import annotations

import csv
from datetime import datetime, timezone
from pathlib import Path


STATUS = "Y5_R10_Delta_Poisson_zero_theorem_conditional_source_coefficient_pack_written_Gauss_orbit_bridge_blocked_nonclaim"
CLAIM_CEILING = "Delta_Poisson_conditional_zero_only_no_numeric_bound_no_Gauss_orbit_no_MHref_no_Newton_no_PPN_no_R10_no_local_GR_claim"
NEXT_TARGET = "702-Y5-R10-kappa-Gref-source-residual-coefficient-fill.md"

ROOT = Path(__file__).resolve().parents[1]
RESIDUALS = ROOT / "source-intake" / "mts_residuals"
DOC_PATH = ROOT / "701-Y5-R10-Delta-Poisson-source-coefficient-fill-or-Gauss-orbit-bridge.md"
FORMALIZATION_WORKBENCH = ROOT.parent / "formalization-workbench"
FORMALIZATION_CUTOFF = datetime.fromisoformat("2026-05-31T14:42:00")

OUTPUT_PATHS = [
    DOC_PATH,
    RESIDUALS / "P8_Y5_R10_701_SOURCE_REGISTER.csv",
    RESIDUALS / "P8_Y5_R10_701_DELTA_POISSON_ZERO_THEOREM_AUDIT.csv",
    RESIDUALS / "P8_Y5_R10_701_DELTA_POISSON_SOURCE_COEFFICIENT_PACK.csv",
    RESIDUALS / "P8_Y5_R10_701_GAUSS_ORBIT_BRIDGE_GATE.csv",
    RESIDUALS / "P8_Y5_R10_701_EVALUATOR.csv",
    RESIDUALS / "P8_Y5_R10_701_CLAIM_GATE_EVALUATION.csv",
    RESIDUALS / "P8_Y5_R10_701_DECISION.csv",
    RESIDUALS / "P8_Y5_R10_701_NONCLAIM_SUMMARY.csv",
    RESIDUALS / "P8_Y5_BRR545_701_VALIDATION.csv",
]

SOURCE_PATHS = {
    "402_doc": ROOT / "402-EH-source-normalization-parent-pair.md",
    "424_doc": ROOT / "424-same-frame-EH-source-Poisson-reduction-gate.md",
    "425_doc": ROOT / "425-EH-operator-retained-ledger-and-source-normalization-test-plan.md",
    "429_doc": ROOT / "429-Ward-Bianchi-exchange-owner-for-Poisson-source.md",
    "523_doc": ROOT / "523-Y5-Gauss-orbital-calibration-or-source-normalization-residual-score.md",
    "529_doc": ROOT / "529-Y5-source-calibrated-EH-family-proof-stack-or-R11-beta-fill.md",
    "531_doc": ROOT / "531-Y5-source-normalized-Newton-and-beta-residual-envelope.md",
    "652_doc": ROOT / "652-Y5-R10-WEP-source-normalization-or-common-geometry-zero-theorem.md",
    "655_doc": ROOT / "655-Y5-R10-EH-operator-selection-under-WEP-closure-or-retained-R11-vector.md",
    "657_doc": ROOT / "657-Y5-R10-source-normalization-family-first-real-R11-fill.md",
    "696_doc": ROOT / "696-Y5-R10-MHref-same-frame-denominator-or-BTF-product-bound-guard.md",
    "699_doc": ROOT / "699-Y5-R10-PG-calibration-residual-bound-source-row-or-EH-coefficient-proof.md",
    "700_doc": ROOT / "700-Y5-R10-EH-Poisson-coefficient-parent-premise-or-PG-residual-numeric-fill.md",
    "700_validation": RESIDUALS / "P8_Y5_BRR545_700_VALIDATION.csv",
    "700_algebra": RESIDUALS / "P8_Y5_R10_700_EH_POISSON_ALGEBRA_CERTIFICATE.csv",
    "700_parent": RESIDUALS / "P8_Y5_R10_700_PARENT_PREMISE_AUDIT.csv",
    "700_delta_fill": RESIDUALS / "P8_Y5_R10_700_DELTA_POISSON_FILL_ROW.csv",
    "700_gate": RESIDUALS / "P8_Y5_R10_700_CLAIM_GATE_EVALUATION.csv",
    "699_pg_source_rows": RESIDUALS / "P8_Y5_R10_699_PG_RESIDUAL_SOURCE_ROW_PACK.csv",
    "pg_contract": RESIDUALS / "P8_Hamiltonian_charge_Poisson_Gauss_calibration_CONTRACT.csv",
    "gauss_ppn_test": RESIDUALS / "P8_Y5_HAMILTONIAN_PIM_GAUSS_PPN_TEST.csv",
    "source_norm_scorecard": RESIDUALS / "P8_Y5_SOURCE_NORMALIZATION_RESIDUAL_SCORECARD.csv",
    "657_channels": RESIDUALS / "P8_Y5_R10_657_CMU_EIGHT_CHANNEL_VECTOR.csv",
    "696_denominator_audit": RESIDUALS / "P8_Y5_R10_696_MHREF_DENOMINATOR_AUDIT.csv",
}


def now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, object]], fieldnames: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, lineterminator="\n")
        writer.writeheader()
        for row in rows:
            writer.writerow({field: row.get(field, "") for field in fieldnames})


def source_list(*source_ids: str) -> str:
    return ";".join(str(SOURCE_PATHS[source_id]) for source_id in source_ids)


def validation_failures(source_id: str) -> list[dict[str, str]]:
    path = SOURCE_PATHS[source_id]
    if not path.exists():
        return [{"check_id": "missing", "result": "fail", "detail": str(path)}]
    return [row for row in read_csv(path) if row.get("result") != "pass"]


def formalization_changed_count() -> int:
    if not FORMALIZATION_WORKBENCH.exists():
        return -1
    return sum(
        1
        for candidate in FORMALIZATION_WORKBENCH.rglob("*")
        if candidate.is_file() and datetime.fromtimestamp(candidate.stat().st_mtime) > FORMALIZATION_CUTOFF
    )


def source_register_rows() -> list[dict[str, str]]:
    generated = now()
    roles = {
        "402_doc": "EH/source-normalization parent pair",
        "424_doc": "same-frame EH-source Poisson reduction gate",
        "425_doc": "EH retained ledger and source-normalization test plan",
        "429_doc": "Ward/Bianchi exchange owner for Poisson source",
        "523_doc": "Gauss/orbital calibration and source-normalization residual scorecard",
        "529_doc": "source-calibrated EH proof stack",
        "531_doc": "Newton and beta residual envelope",
        "652_doc": "WEP/source-normalization common geometry zero-theorem attempt",
        "655_doc": "EH operator selection under WEP closure",
        "657_doc": "source-normalization family first R11 fill",
        "696_doc": "M_H_ref denominator blocker",
        "699_doc": "PG calibration residual source-row handoff",
        "700_doc": "immediate predecessor and Delta_Poisson staging",
        "700_validation": "700 validation gate",
        "700_algebra": "700 EH-to-Poisson algebra certificate",
        "700_parent": "700 parent premise audit",
        "700_delta_fill": "700 unfilled Delta_Poisson row",
        "700_gate": "700 claim gate evaluation",
        "699_pg_source_rows": "699 PG residual source-row pack",
        "pg_contract": "Hamiltonian charge to Poisson/Gauss calibration contract",
        "gauss_ppn_test": "Gauss and PPN readout test ledger",
        "source_norm_scorecard": "source-normalization residual scorecard",
        "657_channels": "eight source-normalization residual channels",
        "696_denominator_audit": "M_H_ref denominator audit",
    }
    return [
        {
            "source_id": source_id,
            "path": str(path),
            "exists": "true" if path.exists() else "false",
            "role": roles[source_id],
            "generated_utc": generated,
        }
        for source_id, path in SOURCE_PATHS.items()
    ]


def zero_theorem_audit_rows() -> list[dict[str, str]]:
    generated = now()
    rows = [
        (
            "ZDP701_0_definition",
            "Delta_Poisson definition",
            "Delta_Poisson = abs((kappa_eff*c^4)/(8*pi*G_ref)-1)+abs(R_src)/(4*pi*G_ref*rho_H)",
            "definition_inherited_from_700",
            "none_definition_only",
            source_list("700_delta_fill", "700_algebra", "pg_contract"),
        ),
        (
            "ZDP701_1_kappa_Gref",
            "coefficient identity",
            "G_ref = kappa_eff*c^4/(8*pi)",
            "not_parent_signed",
            "Delta_G",
            source_list("402_doc", "424_doc", "700_parent"),
        ),
        (
            "ZDP701_2_source_residual",
            "source residual silence",
            "R_src = 0, or abs(R_src)/(4*pi*G_ref*rho_H) bounded below the local gate",
            "not_parent_signed",
            "R_src_over_4piGref_rhoH",
            source_list("429_doc", "657_doc", "657_channels", "source_norm_scorecard"),
        ),
        (
            "ZDP701_3_rho_H",
            "source density normalization",
            "rho_H is positive, local, and the same Hilbert/source density used by the Poisson operator",
            "missing_density_normalization_contract",
            "Delta_rhoH",
            source_list("523_doc", "529_doc", "652_doc", "source_norm_scorecard"),
        ),
        (
            "ZDP701_4_same_frame",
            "same observed frame",
            "source, metric, coframe, connection, and orbital readout live in the same observed frame",
            "conditional_not_parent_derived",
            "Delta_frame",
            source_list("424_doc", "700_parent"),
        ),
        (
            "ZDP701_5_EH_only",
            "EH-only operator selection",
            "R11/non-EH local operator/source vector vanishes or is bounded",
            "R11_operator_vector_unfilled",
            "epsilon_operator",
            source_list("425_doc", "655_doc", "657_channels"),
        ),
        (
            "ZDP701_6_projection_boundary",
            "projection and boundary silence",
            "projector, domain, boundary, and nonmetric exchange terms do not feed local Poisson source",
            "not_parent_signed",
            "F_projector_plus_F_boundary_plus_F_domain_plus_F_nonmetric",
            source_list("429_doc", "657_doc"),
        ),
        (
            "ZDP701_7_conditional_zero_theorem",
            "conditional zero theorem",
            "if ZDP701_1 through ZDP701_6 hold, then Delta_Poisson = 0",
            "proved_as_conditional_algebra_only",
            "parent_premises_unsigned",
            source_list("700_algebra", "700_parent", "pg_contract"),
        ),
        (
            "ZDP701_8_verdict",
            "unconditional local zero proof",
            "the present corpus must sign coefficient identity, source residual zero, rho_H normalization, same-frame ownership, EH-only selection, and boundary silence",
            "fail_current_corpus",
            "Delta_Poisson",
            source_list("700_doc", "700_parent", "700_delta_fill"),
        ),
    ]
    return [
        {
            "audit_id": audit_id,
            "clause": clause,
            "mathematical_requirement": requirement,
            "current_status": status,
            "blocking_residual": residual,
            "valid_for_claim": "false",
            "source_paths": paths,
            "generated_utc": generated,
        }
        for audit_id, clause, requirement, status, residual, paths in rows
    ]


def source_coefficient_pack_rows() -> list[dict[str, str]]:
    generated = now()
    rows = [
        (
            "DPC701_0_total_Delta_Poisson",
            "Delta_Poisson",
            "abs((kappa_eff*c^4)/(8*pi*G_ref)-1)+abs(R_src)/(4*pi*G_ref*rho_H)",
            "kappa_eff;G_ref;R_src;rho_H",
            "MISSING_VALUE_OR_THEOREM_ZERO",
            "dimensionless",
            "unfilled_after_zero_theorem_failed",
            "MISSING_PARENT_INPUTS",
            source_list("700_delta_fill", "699_pg_source_rows", "source_norm_scorecard"),
        ),
        (
            "DPC701_1_kappa_eff",
            "kappa_eff",
            "local EH/source coupling in the observed frame",
            "parent action coefficient or theorem fixing the observed EH source coefficient",
            "MISSING_PARENT_KAPPA_EFF",
            "SI_or_geometric_context_dependent",
            "unfilled",
            "MISSING_PARENT_KAPPA_SOURCE_PATH",
            source_list("402_doc", "424_doc", "655_doc", "700_parent"),
        ),
        (
            "DPC701_2_G_ref",
            "G_ref",
            "universal reference Newton coupling used by local orbital and Poisson readout",
            "constant universal G_ref independent of source species, radius, and readout",
            "MISSING_CONSTANT_UNIVERSAL_GREF",
            "m3_kg-1_s-2_or_geometric_equivalent",
            "unfilled",
            "MISSING_GREF_SOURCE_PATH",
            source_list("523_doc", "696_doc", "696_denominator_audit"),
        ),
        (
            "DPC701_3_source_residual",
            "R_src",
            "all non-EH/source-exchange/projector/boundary contributions to the local Poisson source",
            "signed zero theorem or numeric upper bound",
            "MISSING_SOURCE_RESIDUAL_BOUND",
            "Poisson_source_density_units",
            "unfilled",
            "MISSING_SOURCE_RESIDUAL_THEOREM_OR_BOUND_PATH",
            source_list("429_doc", "657_doc", "657_channels", "source_norm_scorecard"),
        ),
        (
            "DPC701_4_rho_H",
            "rho_H",
            "Hilbert/source density normalization used in the weak static source limit",
            "positive density normalization and nonrelativistic compact-source limit",
            "MISSING_RHO_H_NORMALIZATION",
            "kg_m-3_or_geometric_equivalent",
            "unfilled",
            "MISSING_RHOH_NORMALIZATION_SOURCE_PATH",
            source_list("529_doc", "652_doc", "source_norm_scorecard"),
        ),
        (
            "DPC701_5_R11_operator_vector",
            "epsilon_operator",
            "non-EH operator/source coefficient vector relative to the EH Poisson coefficient",
            "R11 operator-source coefficient vector or EH-only theorem",
            "MISSING_R11_OPERATOR_VECTOR_OR_ZERO_THEOREM",
            "dimensionless",
            "unfilled",
            "MISSING_R11_COEFFICIENT_SOURCE_PATH",
            source_list("425_doc", "655_doc", "657_channels"),
        ),
        (
            "DPC701_6_frame_projection",
            "Delta_frame",
            "mismatch between source frame and observed orbital/metric frame",
            "same-frame descent theorem or residual bound",
            "MISSING_SAME_FRAME_PROJECTION_BOUND",
            "dimensionless",
            "unfilled",
            "MISSING_FRAME_PROJECTION_SOURCE_PATH",
            source_list("424_doc", "429_doc", "700_parent"),
        ),
        (
            "DPC701_7_equation_ref",
            "equation_ref",
            "exact parent-action equation producing the local weak Poisson coefficient",
            "line/path reference to parent equation or executable coefficient extractor",
            "MISSING_EQUATION_REF",
            "not_applicable",
            "unfilled",
            "MISSING_EQUATION_SOURCE_PATH",
            source_list("402_doc", "700_algebra", "pg_contract"),
        ),
        (
            "DPC701_8_bound_formula",
            "usable nonclaim bound",
            "Delta_Poisson <= epsilon_G + epsilon_src + epsilon_frame + epsilon_operator",
            "numeric or theorem-zero epsilon vector",
            "MISSING_EPSILON_VECTOR",
            "dimensionless",
            "formula_staged_inputs_missing",
            "MISSING_EPSILON_VECTOR_SOURCE_PATH",
            source_list("657_channels", "source_norm_scorecard", "700_delta_fill"),
        ),
    ]
    return [
        {
            "coefficient_id": coefficient_id,
            "target": target,
            "definition": definition,
            "required_input": required_input,
            "value_or_bound": value_or_bound,
            "units": units,
            "current_status": status,
            "source_path": source_path,
            "valid_for_claim": "false",
            "source_paths": paths,
            "generated_utc": generated,
        }
        for coefficient_id, target, definition, required_input, value_or_bound, units, status, source_path, paths in rows
    ]


def gauss_orbit_bridge_rows() -> list[dict[str, str]]:
    generated = now()
    rows = [
        (
            "GOB701_0_Delta_Poisson_precondition",
            "Poisson source coefficient gate",
            "nabla^2 Phi = 4*pi*G_ref*rho_H*(1+delta_P) with abs(delta_P)<=Delta_Poisson",
            "Delta_Poisson numeric/theorem-zero row",
            "fail_blocked",
            "Delta_Poisson_missing",
            "cannot promote Gauss/orbit",
            source_list("700_delta_fill", "700_gate"),
        ),
        (
            "GOB701_1_Gauss_surface",
            "Gauss surface bridge",
            "surface_integral grad Phi dot dS = 4*pi*G_ref*M_H + integral R_Poisson dV",
            "regular domain, boundary silence, source density normalization",
            "blocked",
            "Delta_Gauss_surface_plus_boundary",
            "Gauss readout remains residualized",
            source_list("523_doc", "pg_contract", "gauss_ppn_test"),
        ),
        (
            "GOB701_2_MHref",
            "Hamiltonian/orbital mass identifier",
            "M_H_ref = GM_orbit/G_ref only after the source coefficient and readout are independently fixed",
            "certified positive M_H_ref and non-circular G_ref",
            "blocked",
            "MISSING_CERTIFIED_POSITIVE_M_H_REF",
            "B_TF and e_TF denominators stay blocked",
            source_list("696_doc", "696_denominator_audit"),
        ),
        (
            "GOB701_3_orbital_readout",
            "orbital acceleration readout",
            "a_r = -G_ref*M_H/r^2 + residual_orbit",
            "Gauss surface bridge plus observed geodesic/readout descent",
            "blocked",
            "Delta_orbit_readout",
            "Newton limit not promoted",
            source_list("523_doc", "531_doc", "gauss_ppn_test"),
        ),
        (
            "GOB701_4_anti_circularity",
            "anti-circularity guard",
            "do not infer G_ref from the same orbit used to prove M_H_ref or the Poisson coefficient",
            "independent source for G_ref or a parent theorem",
            "guard_active",
            "circular_GM_calibration",
            "prevents fake win",
            source_list("523_doc", "696_doc", "700_delta_fill"),
        ),
        (
            "GOB701_5_bridge_envelope",
            "conditional residual envelope",
            "abs(GM_orbit/(G_ref*M_H)-1) <= Delta_Poisson + Delta_Gauss_surface + Delta_readout + Delta_boundary + Delta_MHref",
            "numeric/theorem-zero vector for every term",
            "formula_staged_inputs_missing",
            "MISSING_BRIDGE_EPSILON_VECTOR",
            "usable as next nonclaim executable contract",
            source_list("523_doc", "696_denominator_audit", "source_norm_scorecard"),
        ),
        (
            "GOB701_6_verdict",
            "Gauss/orbit bridge claim",
            "bridge can only run after Delta_Poisson and M_H_ref are no longer placeholders",
            "Delta_Poisson cleared and M_H_ref certified",
            "fail_current_corpus",
            "Delta_Poisson_plus_MHref",
            "no Gauss, Newton, PPN, R10, or local-GR claim",
            source_list("700_doc", "700_delta_fill", "696_denominator_audit"),
        ),
    ]
    return [
        {
            "bridge_id": bridge_id,
            "step": step,
            "mathematical_form": form,
            "precondition": precondition,
            "current_status": status,
            "blocking_residual": residual,
            "claim_effect": effect,
            "valid_for_claim": "false",
            "source_paths": paths,
            "generated_utc": generated,
        }
        for bridge_id, step, form, precondition, status, residual, effect, paths in rows
    ]


def evaluator_rows() -> list[dict[str, str]]:
    generated = now()
    rows = [
        (
            "EVAL701_0_zero_theorem",
            "Can Delta_Poisson -> 0 be proved unconditionally from the current parent stack?",
            "No. The algebraic sufficiency condition is clear, but the required parent clauses are not signed.",
            "fail_blocked",
            NEXT_TARGET,
            source_list("700_parent", "700_delta_fill"),
        ),
        (
            "EVAL701_1_numeric_fill",
            "Can Delta_Poisson be filled numerically or by theorem-zero now?",
            "No. kappa_eff, G_ref, R_src, and rho_H normalization remain placeholders.",
            "fail_blocked",
            NEXT_TARGET,
            source_list("700_delta_fill", "source_norm_scorecard"),
        ),
        (
            "EVAL701_2_Gauss_orbit",
            "Can the Gauss/orbit bridge be promoted instead?",
            "No. That would smuggle the missing coefficient through the surface/orbit readout.",
            "fail_blocked",
            NEXT_TARGET,
            source_list("523_doc", "696_denominator_audit", "gauss_ppn_test"),
        ),
        (
            "EVAL701_3_best_route",
            "What is the least-scrutiny next route?",
            "Fill or derive the kappa_eff/G_ref/source-residual vector before touching Gauss or orbital mass claims.",
            "route_selected",
            NEXT_TARGET,
            source_list("402_doc", "429_doc", "657_channels", "700_delta_fill"),
        ),
    ]
    return [
        {
            "eval_id": eval_id,
            "question": question,
            "answer": answer,
            "result": result,
            "next_action": next_action,
            "valid_for_claim": "false",
            "source_paths": paths,
            "generated_utc": generated,
        }
        for eval_id, question, answer, result, next_action, paths in rows
    ]


def claim_gate_rows() -> list[dict[str, str]]:
    generated = now()
    rows = [
        ("CG701_0_sources", "all source files load", "source_register exists check", "pass_structure", "allows checkpoint only"),
        ("CG701_1_prior_700", "700 validation clean", "700 validation has no failures", "pass_structure", "inherits clean predecessor"),
        ("CG701_2_zero_theorem", "unconditional Delta_Poisson zero theorem", "parent clauses unsigned", "fail_blocked", "no Delta_Poisson=0 claim"),
        ("CG701_3_source_pack", "numeric/source coefficient fill", "MISSING_* markers remain", "fail_blocked", "no coefficient bound claim"),
        ("CG701_4_Gauss_orbit", "Gauss/orbit bridge", "Delta_Poisson and M_H_ref missing", "fail_blocked", "no Newton/orbit claim"),
        ("CG701_5_local_GR", "PPN/R10/local-GR promotion", "not reached", "fail_blocked", "no PPN/R10/local-GR claim"),
    ]
    return [
        {
            "gate_id": gate_id,
            "gate": gate,
            "observed_state": observed,
            "result": result,
            "claim_effect": effect,
            "valid_for_claim": "false",
            "source_paths": source_list("700_validation", "700_delta_fill", "696_denominator_audit", "gauss_ppn_test"),
            "generated_utc": generated,
        }
        for gate_id, gate, observed, result, effect in rows
    ]


def decision_rows() -> list[dict[str, str]]:
    generated = now()
    rows = [
        (
            "D701_0_conditional_zero",
            "Delta_Poisson zero route",
            "conditional_theorem_written",
            "Delta_Poisson vanishes if coefficient identity, source residual zero, rho_H normalization, same-frame ownership, EH-only selection, and boundary silence all hold",
            NEXT_TARGET,
        ),
        (
            "D701_1_source_fill",
            "source coefficient fill",
            "failed_current_corpus",
            "required parent inputs are still placeholders rather than sourced values or theorem zeros",
            NEXT_TARGET,
        ),
        (
            "D701_2_Gauss_orbit",
            "Gauss/orbit bridge",
            "blocked_current_corpus",
            "promoting Gauss/orbit before Delta_Poisson and M_H_ref would be circular",
            NEXT_TARGET,
        ),
        (
            "D701_3_next",
            "next target",
            "selected",
            "attack kappa_eff/G_ref/source-residual coefficient fill before any public local-GR language",
            NEXT_TARGET,
        ),
    ]
    return [
        {
            "decision_id": decision_id,
            "target": target,
            "result": result,
            "reason": reason,
            "next_action": next_action,
            "valid_for_claim": "false",
            "generated_utc": generated,
        }
        for decision_id, target, result, reason, next_action in rows
    ]


def summary_rows() -> list[dict[str, str]]:
    generated = now()
    return [
        {
            "summary_id": "S701_0",
            "status": STATUS,
            "claim_ceiling": CLAIM_CEILING,
            "main_result": "Delta_Poisson has a clean conditional zero theorem and a source-coefficient pack, but no sourced numeric/theorem-zero fill",
            "hardest_blocker": "the parent stack still has not signed kappa_eff/G_ref, source residual silence, rho_H normalization, same-frame ownership, and EH-only local operator selection",
            "next_target": NEXT_TARGET,
            "valid_for_claim": "false",
            "generated_utc": generated,
        }
    ]


def has_missing_marker(row: dict[str, str]) -> bool:
    return "MISSING" in " ".join(str(value) for value in row.values())


def validation_rows(source_rows, zero, pack, bridge, evaluator, gates, decisions, summary):
    generated = now()
    missing_sources = [row["source_id"] for row in source_rows if row["exists"] != "true"]
    prior_failures = len(validation_failures("700_validation"))
    delta_fill_rows = read_csv(SOURCE_PATHS["700_delta_fill"])
    delta_fill = delta_fill_rows[0] if delta_fill_rows else {}
    delta_still_unfilled = (
        delta_fill.get("value_or_theorem_zero") == "MISSING_VALUE_OR_THEOREM_ZERO"
        and delta_fill.get("source_path") == "MISSING_SOURCE_PATH"
    )
    no_claim = all(
        row.get("valid_for_claim") != "true"
        for group in [zero, pack, bridge, evaluator, gates, decisions, summary]
        for row in group
    )
    zero_verdict = [row for row in zero if row["audit_id"] == "ZDP701_8_verdict"][0]
    bridge_verdict = [row for row in bridge if row["bridge_id"] == "GOB701_6_verdict"][0]
    pack_unfilled = all(row["valid_for_claim"] == "false" for row in pack) and any(has_missing_marker(row) for row in pack)
    evaluator_blocked = all(row["valid_for_claim"] == "false" for row in evaluator) and any(
        row["result"] == "fail_blocked" for row in evaluator
    )
    gates_block = all(row["valid_for_claim"] == "false" for row in gates) and any(
        row["result"] == "fail_blocked" for row in gates
    )
    scoped = all(str(path).startswith(str(ROOT)) for path in OUTPUT_PATHS)
    formalization_count = formalization_changed_count()
    checks = [
        ("V701_0_source_paths_exist", not missing_sources, "all cited source paths exist" if not missing_sources else "missing=" + ";".join(missing_sources)),
        ("V701_1_prior_700_clean", prior_failures == 0, f"700_validation_failures={prior_failures}"),
        ("V701_2_700_Delta_Poisson_still_unfilled", delta_still_unfilled, "700 Delta_Poisson row remains placeholder"),
        ("V701_3_zero_theorem_audit_blocks", zero_verdict["current_status"] == "fail_current_corpus", zero_verdict["blocking_residual"]),
        ("V701_4_conditional_zero_theorem_written", any(row["audit_id"] == "ZDP701_7_conditional_zero_theorem" for row in zero), "conditional theorem row present"),
        ("V701_5_source_coefficient_pack_unfilled", pack_unfilled, f"pack_rows={len(pack)}"),
        ("V701_6_Gauss_orbit_bridge_blocked", bridge_verdict["current_status"] == "fail_current_corpus", bridge_verdict["blocking_residual"]),
        ("V701_7_evaluator_blocks_claim", evaluator_blocked, f"evaluator_rows={len(evaluator)}"),
        ("V701_8_gates_block_claim", gates_block, f"gate_rows={len(gates)}"),
        ("V701_9_no_claim_rows_promoted", no_claim, "all generated rows valid_for_claim=false"),
        ("V701_10_next_target_selected", summary[0]["next_target"] == NEXT_TARGET and decisions[-1]["next_action"] == NEXT_TARGET, NEXT_TARGET),
        ("V701_11_outputs_scoped", scoped, "all outputs under post-checkpoint-work"),
        ("V701_12_formalization_workbench_untouched", formalization_count == 0, f"formalization_changed_after_cutoff={formalization_count}"),
        ("V701_13_status_nonclaim", "no_numeric_bound" in CLAIM_CEILING and "no_local_GR_claim" in CLAIM_CEILING, CLAIM_CEILING),
    ]
    return [{"check_id": cid, "result": "pass" if ok else "fail", "detail": detail, "generated_utc": generated} for cid, ok, detail in checks]


def markdown_table(rows: list[dict[str, object]], columns: list[str]) -> str:
    if not rows:
        return "_No rows._\n"
    header = "| " + " | ".join(columns) + " |"
    divider = "| " + " | ".join("---" for _ in columns) + " |"
    body = [
        "| " + " | ".join(str(row.get(column, "")).replace("\n", " ").replace("|", "\\|") for column in columns) + " |"
        for row in rows
    ]
    return "\n".join([header, divider, *body]) + "\n"


def write_doc(source_rows, zero, pack, bridge, evaluator, gates, decisions, summary, validation) -> None:
    doc = f"""# 701 - Y5 R10 Delta Poisson Source Coefficient Fill Or Gauss Orbit Bridge

## Verdict

701 does not get the miracle, but it does get the exact contract. The local Poisson residual can be killed only by this sufficient condition:

```text
Delta_Poisson = abs((kappa_eff*c^4)/(8*pi*G_ref)-1)
              + abs(R_src)/(4*pi*G_ref*rho_H)

Delta_Poisson = 0 if:
  G_ref = kappa_eff*c^4/(8*pi),
  R_src = 0,
  rho_H > 0 and is the same source density used by the local operator,
  source/readout live in the same observed frame,
  non-EH/R11 operator-source corrections vanish,
  projector, boundary, domain, and nonmetric exchange terms are silent.
```

That is a real conditional zero theorem, not a local-GR pass. The parent stack still has not signed the coefficient identity, source residual silence, source-density normalization, same-frame ownership, EH-only local operator selection, or boundary/projection silence.

So the Gauss/orbit bridge is deliberately blocked. Trying to run it now would be smuggling the missing coupling through the back door, sneaky little gremlin that it is.

| Status | `{STATUS}` |
| Claim ceiling | `{CLAIM_CEILING}` |
| Next target | `{NEXT_TARGET}` |

## Delta Poisson Zero-Theorem Audit

{markdown_table(zero, ["audit_id", "clause", "current_status", "blocking_residual", "valid_for_claim"])}

## Source Coefficient Pack

{markdown_table(pack, ["coefficient_id", "target", "required_input", "value_or_bound", "current_status", "source_path", "valid_for_claim"])}

## Gauss Orbit Bridge Gate

{markdown_table(bridge, ["bridge_id", "step", "current_status", "blocking_residual", "claim_effect", "valid_for_claim"])}

## Evaluator

{markdown_table(evaluator, ["eval_id", "question", "answer", "result", "next_action", "valid_for_claim"])}

## Claim Gate Evaluation

{markdown_table(gates, ["gate_id", "gate", "observed_state", "result", "claim_effect", "valid_for_claim"])}

## Decision

{markdown_table(decisions, ["decision_id", "target", "result", "reason", "next_action", "valid_for_claim"])}

## Nonclaim Summary

{markdown_table(summary, ["summary_id", "status", "claim_ceiling", "main_result", "hardest_blocker", "next_target", "valid_for_claim"])}

## Source Register

{markdown_table(source_rows, ["source_id", "path", "exists", "role"])}

## Validation

{markdown_table(validation, ["check_id", "result", "detail"])}
"""
    DOC_PATH.write_text(doc, encoding="utf-8")


def main() -> None:
    source_rows = source_register_rows()
    zero = zero_theorem_audit_rows()
    pack = source_coefficient_pack_rows()
    bridge = gauss_orbit_bridge_rows()
    evaluator = evaluator_rows()
    gates = claim_gate_rows()
    decisions = decision_rows()
    summary = summary_rows()
    validation = validation_rows(source_rows, zero, pack, bridge, evaluator, gates, decisions, summary)

    write_csv(RESIDUALS / "P8_Y5_R10_701_SOURCE_REGISTER.csv", source_rows, ["source_id", "path", "exists", "role", "generated_utc"])
    write_csv(RESIDUALS / "P8_Y5_R10_701_DELTA_POISSON_ZERO_THEOREM_AUDIT.csv", zero, ["audit_id", "clause", "mathematical_requirement", "current_status", "blocking_residual", "valid_for_claim", "source_paths", "generated_utc"])
    write_csv(RESIDUALS / "P8_Y5_R10_701_DELTA_POISSON_SOURCE_COEFFICIENT_PACK.csv", pack, ["coefficient_id", "target", "definition", "required_input", "value_or_bound", "units", "current_status", "source_path", "valid_for_claim", "source_paths", "generated_utc"])
    write_csv(RESIDUALS / "P8_Y5_R10_701_GAUSS_ORBIT_BRIDGE_GATE.csv", bridge, ["bridge_id", "step", "mathematical_form", "precondition", "current_status", "blocking_residual", "claim_effect", "valid_for_claim", "source_paths", "generated_utc"])
    write_csv(RESIDUALS / "P8_Y5_R10_701_EVALUATOR.csv", evaluator, ["eval_id", "question", "answer", "result", "next_action", "valid_for_claim", "source_paths", "generated_utc"])
    write_csv(RESIDUALS / "P8_Y5_R10_701_CLAIM_GATE_EVALUATION.csv", gates, ["gate_id", "gate", "observed_state", "result", "claim_effect", "valid_for_claim", "source_paths", "generated_utc"])
    write_csv(RESIDUALS / "P8_Y5_R10_701_DECISION.csv", decisions, ["decision_id", "target", "result", "reason", "next_action", "valid_for_claim", "generated_utc"])
    write_csv(RESIDUALS / "P8_Y5_R10_701_NONCLAIM_SUMMARY.csv", summary, ["summary_id", "status", "claim_ceiling", "main_result", "hardest_blocker", "next_target", "valid_for_claim", "generated_utc"])
    write_csv(RESIDUALS / "P8_Y5_BRR545_701_VALIDATION.csv", validation, ["check_id", "result", "detail", "generated_utc"])
    write_doc(source_rows, zero, pack, bridge, evaluator, gates, decisions, summary, validation)

    failures = [row for row in validation if row["result"] != "pass"]
    print(f"status={STATUS}")
    print(f"doc={DOC_PATH}")
    print(f"zero_rows={len(zero)}")
    print(f"coefficient_pack_rows={len(pack)}")
    print(f"bridge_rows={len(bridge)}")
    print(f"validation_failures={len(failures)}")
    print(f"next_target={NEXT_TARGET}")
    if failures:
        for failure in failures:
            print(f"FAIL {failure['check_id']}: {failure['detail']}")
        raise SystemExit(1)


if __name__ == "__main__":
    main()

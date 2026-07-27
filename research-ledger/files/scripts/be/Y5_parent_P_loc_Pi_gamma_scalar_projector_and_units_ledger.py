from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "source-intake" / "mts_residuals"
MICROSCOPE = ROOT / "source-intake" / "microscope"
BRANCH_RESIDUALS = MICROSCOPE / "branch_locked_wep" / "residuals"
FORMALIZATION = ROOT.parent / "formalization-workbench"
BRANCH_ID = "MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428"
DOC = ROOT / "1523-Y5-parent-P_loc-Pi_gamma-scalar-projector-and-units-ledger.md"
START_TS = datetime.now(timezone.utc).timestamp()

SOURCE_FILES = {
    "1522_doc": ROOT / "1522-Y5-parent-q_loc-scalar-source-profile-and-normalization-first-row.md",
    "1522_next": OUT / "P8_Y5_PARENT_QLOC_1522_NEXT_TARGET.csv",
    "1522_profile": OUT / "P8_Y5_PARENT_QLOC_1522_SCALAR_SOURCE_PROFILE_DERIVATION.csv",
    "1522_norm": OUT / "P8_Y5_PARENT_QLOC_1522_NORMALIZATION_FIRST_ROW_SCHEMA.csv",
    "1522_gauss": OUT / "P8_Y5_PARENT_QLOC_1522_GAUSS_GREEN_CONTRACT.csv",
    "1522_validation": OUT / "P8_Y5_BRR545_1522_VALIDATION.csv",
    "1519_doc": ROOT / "1519-Y5-parent-observed-coframe-tau-source-frame-lock-or-MHref-first-row.md",
    "1010_doc": ROOT / "1010-Y5-R10-Gamma-Khat-action-existence-Helmholtz-or-q_loc-residual-retention.md",
    "1181_doc": ROOT / "1181-Y5-R10-PPN-KS-residual-vector-source-pack-or-parent-Q-identity-proof.md",
    "931_doc": ROOT / "931-Y5-R10-gamma-PPN-projection-coefficient-or-KBFH-bound-envelope.md",
    "1240_qr_map": OUT / "P8_Y5_R10_1240_QR_TO_PPN_MAPPING_SCHEMA.csv",
    "1244_policy": OUT / "P8_Y5_R10_1244_RUNNER_POLICY_FEED.csv",
    "1365_qbound": OUT / "P8_Y5_R10_1365_QLOC_BOUND_SOURCE_ROW.csv",
    "1366_envelope": OUT / "P8_Y5_R10_1366_QLOC_ENVELOPE_INTAKE_ROWS.csv",
    "1368_projection": OUT / "P8_Y5_R10_1368_QLOC_TO_PPN_GAMMA_PROJECTION_REQUIREMENTS.csv",
    "1369_runner": OUT / "P8_Y5_R10_1369_QLOC_GAMMA_RUNNER_SCHEMA.csv",
    "798_gamma": OUT / "P8_Y5_R10_798_GAMMA_SOURCE_EXPANSION.csv",
    "1289_kernel": OUT / "P8_Y5_R10_1289_FIRST_DERIVATIVE_TERM_ROW_NONCLAIM.csv",
    "1367_kernel": OUT / "P8_Y5_R10_1367_KMETRIC_CHAIN_KERNEL_ATTEMPT.csv",
    "776_kgamma": OUT / "P8_Y5_R10_776_KGAMMA_METRIC_RESPONSE_LEDGER.csv",
}

SOURCE_REGISTER = OUT / "P8_Y5_PARENT_QLOC_1523_SOURCE_REGISTER.csv"
PLOC_PROJECTOR_AUDIT = OUT / "P8_Y5_PARENT_QLOC_1523_PLOC_PROJECTOR_AUDIT.csv"
PIGAMMA_PROJECTOR_LEDGER = OUT / "P8_Y5_PARENT_QLOC_1523_PIGAMMA_PROJECTOR_LEDGER.csv"
UNITS_LEDGER = OUT / "P8_Y5_PARENT_QLOC_1523_UNITS_LEDGER.csv"
PROFILE_PROMOTION_GATE = OUT / "P8_Y5_PARENT_QLOC_1523_PROFILE_PROMOTION_GATE.csv"
REJECTION_LEDGER = OUT / "P8_Y5_PARENT_QLOC_1523_REJECTION_LEDGER.csv"
CLAIM_GATE = OUT / "P8_Y5_PARENT_QLOC_1523_CLAIM_GATE.csv"
DECISION = OUT / "P8_Y5_PARENT_QLOC_1523_DECISION.csv"
LOCAL_STATUS = OUT / "P8_Y5_PARENT_QLOC_1523_LOCAL_GR_NEWTON_STATUS.csv"
NEXT_TARGET = OUT / "P8_Y5_PARENT_QLOC_1523_NEXT_TARGET.csv"
VALIDATION = OUT / "P8_Y5_BRR545_1523_VALIDATION.csv"

QUARANTINE = MICROSCOPE / "quarantine" / "1523"
QUAR_PLOC = QUARANTINE / "PLOC_PROJECTOR_AUDIT_NONCLAIM.csv"
QUAR_PIGAMMA = QUARANTINE / "PIGAMMA_PROJECTOR_LEDGER_NONCLAIM.csv"
QUAR_UNITS = QUARANTINE / "QLOC_UNITS_LEDGER_NONCLAIM.csv"
QUAR_DECISION = QUARANTINE / "QLOC_DECISION_NONCLAIM.csv"
BRANCH_PLOC = BRANCH_RESIDUALS / "p_loc_projector_audit_nonclaim_1523.csv"
BRANCH_PIGAMMA = BRANCH_RESIDUALS / "pi_gamma_projector_ledger_nonclaim_1523.csv"
BRANCH_UNITS = BRANCH_RESIDUALS / "q_loc_units_ledger_nonclaim_1523.csv"
BRANCH_DECISION = BRANCH_RESIDUALS / "q_loc_decision_nonclaim_1523.csv"


def flags() -> dict[str, bool]:
    return {
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


def source_list(*keys: str) -> str:
    return "; ".join(rel(SOURCE_FILES[key]) for key in keys)


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


def generated_flags_false(paths: list[Path]) -> bool:
    false_values = {"", "false", "0", "no", "none", "null"}
    claim_keys = [
        "score_ready",
        "valid_prediction_row",
        "valid_for_claim",
        "claim_allowed",
        "accepted_for_scoring",
        "passes_for_claim",
    ]
    for path in paths:
        for row in read_csv(path):
            for key in claim_keys:
                if key in row and str(row[key]).strip().lower() not in false_values:
                    return False
    return True


def source_register_rows() -> list[dict[str, Any]]:
    rows = []
    for source_id, (key, path) in enumerate(SOURCE_FILES.items()):
        rows.append(
            {
                "same_parent_branch_id": BRANCH_ID,
                "source_id": f"SRC1523_{source_id}_{key}",
                "source_path": rel(path),
                "exists": path.exists(),
                "purpose": "input evidence for P_loc/Pi_gamma projector and q_loc units ledger",
                **flags(),
            }
        )
    return rows


def ploc_rows() -> list[dict[str, Any]]:
    rows = [
        (
            "PLOC1523_0_observed_coframe_form",
            "P_loc",
            "conditional form P_loc^mu_nu = chi_loc h_obs^mu_nu, h_obs^mu_nu=delta^mu_nu+u_obs^mu u_obs_nu",
            "CONDITIONAL_GEOMETRIC_FORM",
            "observed coframe/tau lock is not parent-signed; chi_loc/domain support is not fixed",
            source_list("1519_doc", "1010_doc"),
        ),
        (
            "PLOC1523_1_parent_ownership",
            "parent-owned projector",
            "P_loc=P_parent(q(Phi)) before readout and variation, with delta_g P_loc accounted or zero",
            "NOT_PARENT_SIGNED",
            "otherwise projection can hide force components or create projector stress",
            source_list("1010_doc", "1522_profile"),
        ),
        (
            "PLOC1523_2_idempotence_orthogonality",
            "projector algebra",
            "P_loc^2=P_loc, P_loc u_obs=0, P_loc respects local Lorentz/gauge convention",
            "FORMAL_REQUIREMENT_ONLY",
            "no source path proves this for current q_loc branch",
            source_list("1519_doc", "1365_qbound"),
        ),
        (
            "PLOC1523_3_variation_silence",
            "no projector stress",
            "delta_g P_loc=0 or all P_loc variation terms are retained in DeltaK/K_domain",
            "NOT_ZERO_DERIVED",
            "projector/domain terms remain retained channels",
            source_list("1289_kernel", "1367_kernel"),
        ),
        (
            "PLOC1523_4_verdict",
            "current MTS supplies claim-grade P_loc",
            "all projector clauses pass with source paths",
            "PLOC_NOT_PROMOTED",
            "P_loc can be used only as a schema placeholder, not scoreable evidence",
            source_list("1522_validation", "1010_doc"),
        ),
    ]
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "projector_id": projector_id,
            "quantity": quantity,
            "definition_or_requirement": definition,
            "status": status,
            "missing_or_risk": missing,
            "source_paths": sources,
            **flags(),
        }
        for projector_id, quantity, definition, status, missing, sources in rows
    ]


def pigamma_rows() -> list[dict[str, Any]]:
    rows = [
        (
            "PIG1523_0_ppn_metric_readout",
            "R_gamma",
            "under weak-field areal-radial convention, R_AB ~= 2(gamma-1)U/c^2",
            "SOURCE_SCHEMA_NONCLAIM",
            "QMAP1240 supplies the scoring schema, not a q_loc projection",
            source_list("1240_qr_map", "1244_policy"),
        ),
        (
            "PIG1523_1_scalar_channel_map",
            "Pi_gamma",
            "Pi_gamma[q_loc] := R_scalar P_obs P_loc q_loc, where R_scalar extracts the scalar trace/slip source",
            "PROJECTOR_SCHEMA_WRITTEN",
            "R_scalar/P_obs are not derived from a linearized MTS operator",
            source_list("1522_profile", "1368_projection"),
        ),
        (
            "PIG1523_2_metric_response_comparison",
            "gamma response coefficient",
            "metric residual ansatz gives gamma-1=(b-a)epsilon at first order",
            "USEFUL_ANALOGY_NOT_QLOC_MAP",
            "931 derives a metric-response projection, not the q_loc scalar-source operator",
            source_list("931_doc", "1181_doc"),
        ),
        (
            "PIG1523_3_q_loc_scalar_vs_TF",
            "scalar vs trace-free/vector pieces",
            "Pi_gamma must separate scalar trace/slip from q_loc_TF, vector, gauge, and preferred-frame pieces",
            "MISSING_DECOMPOSITION",
            "1181 and 1368 keep q_loc_TF/vector decomposition unresolved",
            source_list("1181_doc", "1368_projection"),
        ),
        (
            "PIG1523_4_operator_dependency",
            "operator-defined projector",
            "Pi_gamma is only physical after L_PPN, gauge, boundary, and readout are fixed",
            "MISSING_OPERATOR",
            "without L_PPN/R_gamma, the projector is formal",
            source_list("1369_runner", "1522_norm"),
        ),
        (
            "PIG1523_5_verdict",
            "current MTS supplies claim-grade Pi_gamma/R_scalar",
            "all scalar projector and operator clauses pass",
            "PIGAMMA_NOT_PROMOTED",
            "S_q remains a profile schema, not a source-backed prediction",
            source_list("1522_validation", "1368_projection"),
        ),
    ]
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "projector_id": projector_id,
            "quantity": quantity,
            "definition_or_requirement": definition,
            "status": status,
            "missing_or_risk": missing,
            "source_paths": sources,
            **flags(),
        }
        for projector_id, quantity, definition, status, missing, sources in rows
    ]


def units_rows() -> list[dict[str, Any]]:
    rows = [
        (
            "UNIT1523_0_Lcg",
            "L_cg",
            "L",
            "coarse-graining/fixed scale length",
            "CONDITIONAL_UNITS",
            "fixed L_cg parent contract is not live-signed",
        ),
        (
            "UNIT1523_1_Gamma_eff",
            "Gamma_eff=L_cg^-2 F(m)",
            "L^-2 if F(m) is dimensionless",
            "curvature/scalar-density seed",
            "CONDITIONAL_UNIT_CHAIN",
            "F and m units/profile are not fully parent-signed",
        ),
        (
            "UNIT1523_2_grad_Gamma",
            "nabla Gamma_eff",
            "L^-3",
            "gradient part of q_loc",
            "CONDITIONAL_UNIT_CHAIN",
            "requires derivative convention and m/L_cg profile",
        ),
        (
            "UNIT1523_3_div_Khat",
            "nabla_mu K_hat^{mu nu}",
            "L^-3 if K_hat has L^-2 stress-curvature units",
            "stress-divergence subtraction",
            "MISSING_KHAT_UNITS_CERTIFICATE",
            "K_hat metric-response match missing",
        ),
        (
            "UNIT1523_4_q_loc",
            "q_loc^nu",
            "L^-3 under geometric units",
            "projected local residual vector",
            "CONDITIONAL_UNIT_CHAIN",
            "P_loc/Pi_gamma not promoted",
        ),
        (
            "UNIT1523_5_Sq",
            "S_q=Pi_gamma[q_loc]",
            "L^-3 if Pi_gamma is dimensionless scalar projection",
            "scalar-channel weak-field source",
            "SCHEMA_ONLY",
            "Pi_gamma/R_scalar is not sourced",
        ),
        (
            "UNIT1523_6_Cop",
            "C_op in nabla^2 R_AB = C_op S_q",
            "L if R_AB is dimensionless and S_q has L^-3",
            "operator normalization / coupling constant",
            "MISSING_OPERATOR_CONSTANT",
            "cannot compute Q_loc without C_op/sign/boundary",
        ),
        (
            "UNIT1523_7_Qloc",
            "Q_loc=G_ext[S_q]",
            "L",
            "exterior scalar-hair length under Gauss/Green convention",
            "CONDITIONAL_GAUSS_UNITS",
            "C_op and boundary convention missing",
        ),
        (
            "UNIT1523_8_qloch",
            "q_loc_hat=Q_loc c^2/(G M_source)",
            "dimensionless",
            "Cassini/PPN runner amplitude",
            "MISSING_NUMERIC_VALUE",
            "Q_loc and measured GM/source row missing",
        ),
    ]
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "unit_id": unit_id,
            "quantity": quantity,
            "units": units,
            "role": role,
            "status": status,
            "missing_to_promote": missing,
            "source_paths": source_list("798_gamma", "1522_gauss", "1240_qr_map", "1365_qbound"),
            **flags(),
        }
        for unit_id, quantity, units, role, status, missing in rows
    ]


def promotion_gate_rows() -> list[dict[str, Any]]:
    rows = [
        ("PROM1523_0_Ploc", "P_loc parent-owned observed projector", "BLOCKED", "coframe/tau/domain and variation terms missing"),
        ("PROM1523_1_Pigamma", "Pi_gamma/R_scalar scalar projector", "BLOCKED", "operator/gauge/readout missing"),
        ("PROM1523_2_units", "q_loc/S_q/Q_loc/q_loc_hat units chain", "CONDITIONAL_ONLY", "Khat units, C_op, source GM missing"),
        ("PROM1523_3_Khat", "K_hat/DeltaK scalar-channel subtraction", "BLOCKED", "metric-response match and scalar profile missing"),
        ("PROM1523_4_profile", "source-backed S_q profile", "BLOCKED", "m/Lcg/support/boundary rows missing"),
        ("PROM1523_5_acceptance", "1522 profile promotion", "CLAIM_BLOCKED", "all projector/unit/profile/operator rows must close first"),
    ]
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "gate_id": gate_id,
            "promotion_item": item,
            "status": status,
            "reason": reason,
            "source_paths": source_list("1522_profile", "1522_norm", "1010_doc"),
            **flags(),
        }
        for gate_id, item, status, reason in rows
    ]


def rejection_rows() -> list[dict[str, Any]]:
    rows = [
        ("REJ1523_0_formal_projector", "treat formal P_loc as physical observed projector", "REJECTED", "needs parent-owned observed coframe and variation accounting"),
        ("REJ1523_1_trace_guess", "define Pi_gamma as trace by inspection only", "REJECTED", "needs weak-field operator/readout and gauge convention"),
        ("REJ1523_2_drop_TF_vector", "discard trace-free/vector/gauge q_loc pieces", "REJECTED", "requires decomposition and independent bounds"),
        ("REJ1523_3_Khat_ignored", "use Gamma gradient units while ignoring div K_hat", "REJECTED", "q_loc includes K_hat/DeltaK subtraction"),
        ("REJ1523_4_dimensionless_jump", "declare q_loc_hat dimensionless without Q_loc/GM", "REJECTED", "needs Green integral and measured source normalization"),
    ]
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "rejection_id": rejection_id,
            "shortcut": shortcut,
            "status": status,
            "reason": reason,
            **flags(),
        }
        for rejection_id, shortcut, status, reason in rows
    ]


def claim_gate_rows() -> list[dict[str, Any]]:
    rows = [
        ("GATE1523_0_conditional_Ploc_form", "conditional P_loc form exists", "PASS_CONDITIONAL", "spatial observed projector form can be written if coframe is signed", False),
        ("GATE1523_1_live_Ploc", "P_loc is parent-owned and variation-safe", "BLOCKED", "observed coframe/domain/variation clauses missing", False),
        ("GATE1523_2_live_Pigamma", "Pi_gamma/R_scalar is operator-derived", "BLOCKED", "L_PPN, gauge, scalar decomposition, and readout missing", False),
        ("GATE1523_3_units_chain", "unit chain is usable for scoring", "BLOCKED", "Khat units, C_op, Q_loc, GM missing", False),
        ("GATE1523_4_profile_promoted", "S_q profile can be promoted", "BLOCKED", "projector and units rows not claim-grade", False),
        ("GATE1523_5_local_GR", "local GR/PPN claim can be made", "BLOCKED_NO_CLAIM", "no scoreable q_loc scalar channel exists", False),
    ]
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "gate_id": gate_id,
            "claim": claim,
            "status": status,
            "reason": reason,
            "gate_pass": gate_pass,
            **flags(),
        }
        for gate_id, claim, status, reason, gate_pass in rows
    ]


def decision_rows() -> list[dict[str, Any]]:
    rows = [
        ("DEC1523_0_conditional_projectors", "Write conditional P_loc and Pi_gamma forms but do not promote them.", "PROJECTORS_SCHEMA_ONLY", "the forms clarify the target while respecting missing parent ownership."),
        ("DEC1523_1_units_chain", "Adopt the conditional L^-3 to dimensionless unit chain as the next ledger.", "UNITS_CONDITIONAL_NONCLAIM", "it names C_op and Q_loc as the real normalization bottlenecks."),
        ("DEC1523_2_next", "Next target is K_hat/DeltaK scalar profile or Green normalization C_op.", "NEXT_1524_KHAT_OR_COP", "without Khat subtraction and C_op, S_q cannot become a finite q_loc_hat."),
    ]
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "decision_id": decision_id,
            "decision": decision,
            "result": result,
            "rationale": rationale,
            **flags(),
        }
        for decision_id, decision, result, rationale in rows
    ]


def local_status_rows() -> list[dict[str, Any]]:
    rows = [
        ("LOCAL1523_0_Ploc", "local projector", "CONDITIONAL_ONLY", "observed coframe/domain ownership missing"),
        ("LOCAL1523_1_Pigamma", "scalar gamma projector", "SCHEMA_ONLY", "operator/readout missing"),
        ("LOCAL1523_2_units", "q_loc unit chain", "CONDITIONAL_ONLY", "Khat/C_op/Qloc/GM gaps remain"),
        ("LOCAL1523_3_PPN", "Cassini/PPN scoring", "NOT_CLAIMED", "no q_loc_hat or C_qgamma"),
        ("LOCAL1523_4_GR", "derived local GR", "NOT_CLAIMED", "q_loc and M_H_ref bottlenecks remain"),
    ]
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "status_id": status_id,
            "claim": claim,
            "current_status": status,
            "reason": reason,
            **flags(),
        }
        for status_id, claim, status, reason in rows
    ]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "next_id": "NEXT1523_0_1524",
            "next_target": "1524-Y5-parent-Khat-DeltaK-scalar-channel-profile-or-Green-normalization.md",
            "script": "scripts/Y5_parent_Khat_DeltaK_scalar_channel_profile_or_Green_normalization.py",
            "objective": "derive or source the scalar-channel projection of K_hat/DeltaK and the Green/operator normalization C_op needed to convert S_q into Q_loc and q_loc_hat",
            "do_not": "do not score PPN/Cassini, do not drop K_hat, do not import q_R, and do not claim local GR",
            **flags(),
        }
    ]


def copy_outputs() -> None:
    copies = [
        (PLOC_PROJECTOR_AUDIT, QUAR_PLOC),
        (PIGAMMA_PROJECTOR_LEDGER, QUAR_PIGAMMA),
        (UNITS_LEDGER, QUAR_UNITS),
        (DECISION, QUAR_DECISION),
        (PLOC_PROJECTOR_AUDIT, BRANCH_PLOC),
        (PIGAMMA_PROJECTOR_LEDGER, BRANCH_PIGAMMA),
        (UNITS_LEDGER, BRANCH_UNITS),
        (DECISION, BRANCH_DECISION),
    ]
    for source, destination in copies:
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(source, destination)


def remove_pycache() -> None:
    pycache = ROOT / "scripts" / "__pycache__"
    if pycache.exists():
        shutil.rmtree(pycache)


def formalization_modified_count_since_start() -> int:
    if not FORMALIZATION.exists():
        return 0
    return sum(1 for path in FORMALIZATION.rglob("*") if path.is_file() and path.stat().st_mtime >= START_TS)


def validation_rows(generated_csvs: list[Path]) -> list[dict[str, Any]]:
    sources = read_csv(SOURCE_REGISTER)
    ploc = read_csv(PLOC_PROJECTOR_AUDIT)
    pigamma = read_csv(PIGAMMA_PROJECTOR_LEDGER)
    units = read_csv(UNITS_LEDGER)
    promotion = read_csv(PROFILE_PROMOTION_GATE)
    rejections = read_csv(REJECTION_LEDGER)
    gates = read_csv(CLAIM_GATE)
    decisions = read_csv(DECISION)
    next_rows = read_csv(NEXT_TARGET)

    checks = [
        ("VAL1523_0_sources_exist", all(row["exists"] == "True" for row in sources), "all cited 1523 input source paths exist"),
        ("VAL1523_1_Ploc_conditional_not_live", any(row["projector_id"] == "PLOC1523_4_verdict" and row["status"] == "PLOC_NOT_PROMOTED" for row in ploc), "P_loc remains schema-only/nonclaim"),
        ("VAL1523_2_Pigamma_schema_not_live", any(row["projector_id"] == "PIG1523_5_verdict" and row["status"] == "PIGAMMA_NOT_PROMOTED" for row in pigamma), "Pi_gamma/R_scalar remains unpromoted"),
        ("VAL1523_3_units_chain_written", any(row["unit_id"] == "UNIT1523_4_q_loc" and "L^-3" in row["units"] for row in units) and any(row["unit_id"] == "UNIT1523_8_qloch" and row["units"] == "dimensionless" for row in units), "q_loc/S_q/Q_loc/q_loc_hat units chain is written"),
        ("VAL1523_4_units_nonclaim", any(row["unit_id"] == "UNIT1523_6_Cop" and row["status"] == "MISSING_OPERATOR_CONSTANT" for row in units), "C_op/operator normalization remains missing"),
        ("VAL1523_5_promotion_blocked", any(row["gate_id"] == "PROM1523_5_acceptance" and row["status"] == "CLAIM_BLOCKED" for row in promotion), "profile promotion gate remains blocked"),
        ("VAL1523_6_rejections_guardrails", len(rejections) >= 5 and all(row["status"] == "REJECTED" for row in rejections), "projector/trace/Khat/dimensionless shortcuts rejected"),
        ("VAL1523_7_claim_gates_block_claim", any(row["gate_id"] == "GATE1523_5_local_GR" and row["status"] == "BLOCKED_NO_CLAIM" for row in gates), "local GR claim remains blocked"),
        ("VAL1523_8_decision_next", any(row["result"] == "NEXT_1524_KHAT_OR_COP" for row in decisions), "decision selects Khat/DeltaK or C_op next"),
        ("VAL1523_9_next_target", any("1524-Y5-parent-Khat-DeltaK" in row["next_target"] for row in next_rows), "next target is Khat/DeltaK scalar channel or Green normalization"),
        ("VAL1523_10_csv_parse", all(parse_csv(path) for path in generated_csvs), "all generated 1523 CSVs parse cleanly"),
        ("VAL1523_11_claim_flags_false", generated_flags_false(generated_csvs), "all generated prediction/claim flags remain false"),
        ("VAL1523_12_branch_copies", all(path.exists() for path in [QUAR_PLOC, QUAR_PIGAMMA, QUAR_UNITS, QUAR_DECISION, BRANCH_PLOC, BRANCH_PIGAMMA, BRANCH_UNITS, BRANCH_DECISION]), "branch/quarantine nonclaim copies written"),
        ("VAL1523_13_pycache_absent", not (ROOT / "scripts" / "__pycache__").exists(), "scripts __pycache__ absent after run"),
        ("VAL1523_14_formalization_untouched", formalization_modified_count_since_start() == 0, "formalization modified-file count since start=0"),
    ]
    overall = all(result for _, result, _ in checks)
    rows = [
        {
            "same_parent_branch_id": BRANCH_ID,
            "check_id": check_id,
            "result": "PASS" if result else "FAIL",
            "detail": detail,
        }
        for check_id, result, detail in checks
    ]
    rows.append(
        {
            "same_parent_branch_id": BRANCH_ID,
            "check_id": "VAL1523_15_overall",
            "result": "PASS" if overall else "FAIL",
            "detail": "1523 writes conditional P_loc/Pi_gamma projectors and units chain, keeps them nonclaim, and selects Khat/DeltaK or C_op next"
            if overall
            else "1523 validation failed; inspect failed rows before continuing",
        }
    )
    return rows


def md_table(rows: list[dict[str, Any]], columns: list[str]) -> str:
    output = ["| " + " | ".join(columns) + " |", "| " + " | ".join("---" for _ in columns) + " |"]
    for row in rows:
        output.append(
            "| "
            + " | ".join(str(row.get(column, "")).replace("\n", " ").replace("|", "\\|") for column in columns)
            + " |"
        )
    return "\n".join(output)


def write_doc(
    sources: list[dict[str, Any]],
    ploc: list[dict[str, Any]],
    pigamma: list[dict[str, Any]],
    units: list[dict[str, Any]],
    promotion: list[dict[str, Any]],
    rejections: list[dict[str, Any]],
    gates: list[dict[str, Any]],
    decisions: list[dict[str, Any]],
    local_rows: list[dict[str, Any]],
    validation: list[dict[str, Any]],
    next_rows: list[dict[str, Any]],
) -> None:
    DOC.write_text(
        "\n".join(
            [
                "# 1523 - Parent P_loc / Pi_gamma Scalar Projector and Units Ledger",
                "",
                "## Verdict",
                "- A conditional local projector form is now explicit: `P_loc^mu_nu = chi_loc h_obs^mu_nu`, with `h_obs` built from the observed coframe.",
                "- A conditional scalar PPN projector schema is now explicit: `Pi_gamma[q_loc] := R_scalar P_obs P_loc q_loc`, but `R_scalar/P_obs/L_PPN` are not parent-derived.",
                "- The unit chain is now pinned down conditionally: `Gamma_eff ~ L^-2`, `q_loc` and `S_q ~ L^-3`, `C_op ~ L`, `Q_loc ~ L`, and `q_loc_hat` dimensionless.",
                "- Nothing is scoreable yet because `P_loc` is not parent-owned, `Pi_gamma` is not operator-derived, and `K_hat/DeltaK` plus `C_op` remain missing.",
                "",
                "## Source Register",
                md_table(sources, ["source_id", "source_path", "exists", "purpose"]),
                "",
                "## P_loc Projector Audit",
                md_table(ploc, ["projector_id", "quantity", "definition_or_requirement", "status", "missing_or_risk"]),
                "",
                "## Pi_gamma Projector Ledger",
                md_table(pigamma, ["projector_id", "quantity", "definition_or_requirement", "status", "missing_or_risk"]),
                "",
                "## Units Ledger",
                md_table(units, ["unit_id", "quantity", "units", "role", "status", "missing_to_promote"]),
                "",
                "## Profile Promotion Gate",
                md_table(promotion, ["gate_id", "promotion_item", "status", "reason"]),
                "",
                "## Rejection Ledger",
                md_table(rejections, ["rejection_id", "shortcut", "status", "reason"]),
                "",
                "## Claim Gates",
                md_table(gates, ["gate_id", "claim", "status", "reason"]),
                "",
                "## Decision",
                md_table(decisions, ["decision_id", "decision", "result", "rationale"]),
                "",
                "## Local GR / Newton Status",
                md_table(local_rows, ["status_id", "claim", "current_status", "reason"]),
                "",
                "## Validation",
                md_table(validation, ["check_id", "result", "detail"]),
                "",
                "## Next Target",
                md_table(next_rows, ["next_id", "next_target", "script", "objective", "do_not"]),
                "",
            ]
        ),
        encoding="utf-8",
    )


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    sources = source_register_rows()
    ploc = ploc_rows()
    pigamma = pigamma_rows()
    units = units_rows()
    promotion = promotion_gate_rows()
    rejections = rejection_rows()
    gates = claim_gate_rows()
    decisions = decision_rows()
    local_rows = local_status_rows()
    next_rows = next_target_rows()

    write_csv(SOURCE_REGISTER, sources)
    write_csv(PLOC_PROJECTOR_AUDIT, ploc)
    write_csv(PIGAMMA_PROJECTOR_LEDGER, pigamma)
    write_csv(UNITS_LEDGER, units)
    write_csv(PROFILE_PROMOTION_GATE, promotion)
    write_csv(REJECTION_LEDGER, rejections)
    write_csv(CLAIM_GATE, gates)
    write_csv(DECISION, decisions)
    write_csv(LOCAL_STATUS, local_rows)
    write_csv(NEXT_TARGET, next_rows)
    copy_outputs()
    remove_pycache()

    generated_csvs = [
        SOURCE_REGISTER,
        PLOC_PROJECTOR_AUDIT,
        PIGAMMA_PROJECTOR_LEDGER,
        UNITS_LEDGER,
        PROFILE_PROMOTION_GATE,
        REJECTION_LEDGER,
        CLAIM_GATE,
        DECISION,
        LOCAL_STATUS,
        NEXT_TARGET,
    ]
    validation = validation_rows(generated_csvs)
    write_csv(VALIDATION, validation)
    write_doc(sources, ploc, pigamma, units, promotion, rejections, gates, decisions, local_rows, validation, next_rows)


if __name__ == "__main__":
    main()

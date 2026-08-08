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
DOC = ROOT / "1520-Y5-parent-Lcg-contract-or-q_loc-weak-field-response-coefficient.md"
START_TS = datetime.now(timezone.utc).timestamp()

SOURCE_FILES = {
    "1519_doc": ROOT / "1519-Y5-parent-observed-coframe-tau-source-frame-lock-or-MHref-first-row.md",
    "1519_next": OUT / "P8_Y5_PARENT_FRAME_1519_NEXT_TARGET.csv",
    "1519_blockers": OUT / "P8_Y5_PARENT_FRAME_1519_LOCAL_HARD_BLOCKER_ROLLUP.csv",
    "1368_doc": ROOT / "1368-Y5-R10-RAB-m-Lcg-parent-metric-response-kernels-or-q_loc-projection-map.md",
    "1367_kernel": OUT / "P8_Y5_R10_1367_KMETRIC_CHAIN_KERNEL_ATTEMPT.csv",
    "1368_lcg": OUT / "P8_Y5_R10_1368_M_LCG_KERNEL_HUNT.csv",
    "1368_projection": OUT / "P8_Y5_R10_1368_QLOC_TO_PPN_GAMMA_PROJECTION_REQUIREMENTS.csv",
    "1369_doc": ROOT / "1369-Y5-R10-RAB-Lcg-parent-definition-metric-silence-or-q_loc-gamma-projection-runner.md",
    "1369_lcg": OUT / "P8_Y5_R10_1369_LCG_PARENT_DEFINITION_HUNT.csv",
    "1369_derivation": OUT / "P8_Y5_R10_1369_LCG_METRIC_RESPONSE_DERIVATION_LEDGER.csv",
    "1369_runner": OUT / "P8_Y5_R10_1369_QLOC_GAMMA_RUNNER_SCHEMA.csv",
    "1369_smoke": OUT / "P8_Y5_R10_1369_QLOC_GAMMA_SMOKE_RESULT.csv",
    "1369_next": OUT / "P8_Y5_R10_1369_NEXT_TARGET.csv",
    "1244_doc": ROOT / "1244-Y5-R10-QR-statistical-policy-and-GM-convention-pack.md",
    "1244_policy": OUT / "P8_Y5_R10_1244_RUNNER_POLICY_FEED.csv",
    "1181_ppn": OUT / "P8_Y5_R10_1181_EXTERNAL_PPN_SOURCE_REGISTER.csv",
    "1289_kernel": OUT / "P8_Y5_R10_1289_FIRST_DERIVATIVE_TERM_ROW_NONCLAIM.csv",
    "776_kgamma": OUT / "P8_Y5_R10_776_KGAMMA_METRIC_RESPONSE_LEDGER.csv",
}

SOURCE_REGISTER = OUT / "P8_Y5_PARENT_LCG_1520_SOURCE_REGISTER.csv"
LCG_CONTRACT_AUDIT = OUT / "P8_Y5_PARENT_LCG_1520_PARENT_CONTRACT_AUDIT.csv"
LCG_SILENCE_THEOREM = OUT / "P8_Y5_PARENT_LCG_1520_METRIC_SILENCE_THEOREM.csv"
CQGAMMA_DERIVATION = OUT / "P8_Y5_PARENT_LCG_1520_CQGAMMA_DERIVATION_ATTEMPT.csv"
QLOC_GAMMA_RUNNER = OUT / "P8_Y5_PARENT_LCG_1520_QLOC_GAMMA_RUNNER_INPUT_ROW.csv"
REJECTION_LEDGER = OUT / "P8_Y5_PARENT_LCG_1520_REJECTION_LEDGER.csv"
CLAIM_GATE = OUT / "P8_Y5_PARENT_LCG_1520_CLAIM_GATE.csv"
DECISION = OUT / "P8_Y5_PARENT_LCG_1520_DECISION.csv"
LOCAL_STATUS = OUT / "P8_Y5_PARENT_LCG_1520_LOCAL_GR_NEWTON_STATUS.csv"
NEXT_TARGET = OUT / "P8_Y5_PARENT_LCG_1520_NEXT_TARGET.csv"
VALIDATION = OUT / "P8_Y5_BRR545_1520_VALIDATION.csv"

QUARANTINE = MICROSCOPE / "quarantine" / "1520"
QUAR_LCG = QUARANTINE / "LCG_PARENT_CONTRACT_AUDIT_NONCLAIM.csv"
QUAR_CQ = QUARANTINE / "CQGAMMA_DERIVATION_ATTEMPT_NONCLAIM.csv"
QUAR_RUNNER = QUARANTINE / "QLOC_GAMMA_RUNNER_INPUT_ROW_NONCLAIM.csv"
QUAR_DECISION = QUARANTINE / "LCG_DECISION_NONCLAIM.csv"
BRANCH_LCG = BRANCH_RESIDUALS / "lcg_parent_contract_audit_nonclaim_1520.csv"
BRANCH_CQ = BRANCH_RESIDUALS / "cqgamma_derivation_attempt_nonclaim_1520.csv"
BRANCH_RUNNER = BRANCH_RESIDUALS / "q_loc_gamma_runner_input_row_nonclaim_1520.csv"
BRANCH_DECISION = BRANCH_RESIDUALS / "lcg_decision_nonclaim_1520.csv"


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
                "source_id": f"SRC1520_{source_id}_{key}",
                "source_path": rel(path),
                "exists": path.exists(),
                "purpose": "input evidence for L_cg contract and q_loc-to-gamma response fork",
                **flags(),
            }
        )
    return rows


def lcg_contract_rows() -> list[dict[str, Any]]:
    rows = [
        (
            "LCGC1520_0_fixed_scalar_parameter",
            "L_cg=L_* is a spacetime-scalar coupling/renormalization length, not a metric functional",
            "COVARIANT_IF_EXPLICIT_PARENT_CLAUSE",
            "a constant scalar parameter does not by itself break diffeomorphism covariance",
            "MISSING_PARENT_ACTION_ADOPTION;MISSING_UNITS;MISSING_SCALE_ORIGIN",
            source_list("1369_lcg", "1519_blockers"),
        ),
        (
            "LCGC1520_1_variation_order",
            "Hilbert variation holds L_* fixed before readout/domain fitting",
            "EXACT_CONTRACT_CLAUSE",
            "if L_cg is not a field and not g-dependent, delta_g L_cg=0 follows directly",
            "MISSING_VARIATION_BEFORE_READOUT_CERTIFICATE",
            source_list("1369_derivation", "1289_kernel"),
        ),
        (
            "LCGC1520_2_domain_separation",
            "coarse-graining/readout domain size ell_D is a separate observable, not the action parameter L_*",
            "REQUIRED_TO_AVOID_COVARIANCE_CHEAT",
            "otherwise cell-volume/domain/coarse-graining definitions have metric response and M_L survives",
            "MISSING_ELL_D_VS_LCG_SPLIT;MISSING_DOMAIN_NO_FLUX_CERTIFICATE",
            source_list("1368_lcg", "1369_lcg"),
        ),
        (
            "LCGC1520_3_rg_or_physical_scale",
            "observable predictions cannot depend arbitrarily on L_* without a flow/evolution/renormalization rule",
            "REQUIRED_SOURCE_OR_DERIVATION",
            "fixed external scale is legal but becomes a free physical constant unless derived, calibrated, or RG-invariant",
            "MISSING_LCG_FLOW_OR_SOURCE_ROW",
            source_list("1369_lcg", "1519_blockers"),
        ),
        (
            "LCGC1520_4_not_geometric_length",
            "L_cg is not cell volume, curvature radius, density/source length, projector radius, or boundary readout",
            "COUNTERBRANCHES_RETAINED",
            "all common geometric/coarse-graining definitions are generically metric-composite and cannot be deleted",
            "MISSING_EXCLUSION_CERTIFICATE_FOR_ALL_COMPOSITE_BRANCHES",
            source_list("1369_lcg"),
        ),
        (
            "LCGC1520_5_current_verdict",
            "current MTS parent-signs the fixed L_cg contract",
            "NOT_PARENT_SIGNED",
            "the clean contract is written, but the corpus does not yet choose it inside a parent action",
            "MISSING_SIGNED_PARENT_CONTRACT",
            source_list("1519_doc", "1369_doc"),
        ),
    ]
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "contract_id": contract_id,
            "contract_clause": clause,
            "status": status,
            "derivation_or_risk": derivation,
            "missing_to_promote": missing,
            "source_paths": sources,
            **flags(),
        }
        for contract_id, clause, status, derivation, missing, sources in rows
    ]


def lcg_silence_theorem_rows() -> list[dict[str, Any]]:
    rows = [
        (
            "ML1520_0_definition",
            "M_L^{mu nu}:=delta L_cg/delta g_{mu nu}|_{Phi,psi,L_* fixed}",
            "definition of the L_cg metric-response kernel",
            "DEFINED",
            "none",
        ),
        (
            "ML1520_1_fixed_parameter_derivative",
            "if L_cg=L_* and L_* is not a functional of g, Phi, domain, boundary, or source readout, then delta_g L_cg=0",
            "ordinary variational calculus at fixed coupling",
            "DERIVED_CONDITIONAL",
            "parent action must explicitly select L_*",
        ),
        (
            "ML1520_2_chain_term",
            "delta_g[L_cg^-2 F(m)] contains -2 L_cg^-3 F(m) M_L^{mu nu}",
            "with M_L=0 this algebraic L_cg chain term vanishes",
            "DERIVED_IF_ML_ZERO",
            "K_conn, K_domain, K_boundary, Khat comparison, and active stress still remain",
        ),
        (
            "ML1520_3_covariance_guard",
            "fixed scalar parameter is covariant only if it is not secretly a chosen coordinate/grid/domain length",
            "coordinate/domain definitions reintroduce metric and boundary response",
            "GUARD_REQUIRED",
            "must separate L_* from ell_D/readout geometry",
        ),
        (
            "ML1520_4_live_claim",
            "current MTS can set M_L^{mu nu}=0 in the live local branch",
            "the theorem is exact under hypotheses, but those hypotheses are not parent-signed",
            "NOT_CLAIMED",
            "signed parent L_cg clause or bounded composite response row",
        ),
    ]
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "theorem_id": theorem_id,
            "statement": statement,
            "derivation": derivation,
            "status": status,
            "missing_to_promote": missing,
            "source_paths": source_list("1369_derivation", "1368_lcg", "1289_kernel"),
            **flags(),
        }
        for theorem_id, statement, derivation, status, missing in rows
    ]


def cqgamma_rows() -> list[dict[str, Any]]:
    rows = [
        (
            "CQG1520_0_ppn_definition",
            "weak-field metric convention",
            "g_00=-1+2U+O(v^4), g_ij=(1+2 gamma U)delta_ij+O(v^4)",
            "gamma_minus_1 is the spatial/temporal potential slip in the chosen PPN gauge",
            "CONVENTION_ONLY",
            source_list("1181_ppn", "1244_policy"),
        ),
        (
            "CQG1520_1_generic_response",
            "generic q_loc response",
            "gamma_minus_1_q_loc = C_qgamma q_loc_hat + C_DeltaK DeltaK_hat + C_boundary B_hat + retained channels",
            "C_qgamma is a weak-field Green-operator/projection coefficient, not a number until gauge, source averaging, GM convention, and normalization are fixed",
            "DERIVED_SCHEMA",
            source_list("1368_projection", "1369_runner", "776_kgamma"),
        ),
        (
            "CQG1520_2_qR_bridge_conditional",
            "q_R bridge special case",
            "if q_loc_hat == q_R_hat with the same source averaging, sign, GM convention, and no retained channels, then C_qgamma=-1/2",
            "this follows from the existing q_R policy gamma_minus_1_QR=-q_R_hat/2, but it is not importable without the bridge",
            "CONDITIONAL_COEFFICIENT_ONLY",
            source_list("1244_doc", "1244_policy", "1368_projection"),
        ),
        (
            "CQG1520_3_operator_form",
            "operator coefficient",
            "C_qgamma = R_gamma L_PPn^{-1} P_obs P_loc N_q^{-1} under a fixed linearized field operator and normalization",
            "this is the clean non-smuggled target for a future weak-field solve",
            "OPERATOR_FORM_NONCLAIM",
            source_list("1369_runner", "1367_kernel"),
        ),
        (
            "CQG1520_4_live_value",
            "current live C_qgamma",
            "MISSING_WEAK_FIELD_RESPONSE",
            "q_loc_hat, normalization N_q, operator L_PPN, source averaging, and DeltaK/boundary split are not supplied",
            "NOT_SCORE_READY",
            source_list("1369_smoke", "1519_blockers"),
        ),
    ]
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "derivation_id": derivation_id,
            "target": target,
            "formula": formula,
            "meaning": meaning,
            "status": status,
            "source_paths": sources,
            **flags(),
        }
        for derivation_id, target, formula, meaning, status, sources in rows
    ]


def qloc_gamma_runner_rows() -> list[dict[str, Any]]:
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "row_id": "QGR1520_0_live_blocked",
            "branch": "q_loc_to_gamma_live",
            "q_loc_hat": "MISSING_QLOC_VALUE",
            "C_qgamma": "MISSING_WEAK_FIELD_RESPONSE",
            "C_qgamma_conditional_qR_bridge": "-0.5_IF_AND_ONLY_IF_QLOC_EQUALS_QR_WITH_SAME_NORMALIZATION",
            "DeltaK_hat": "MISSING_DELTAK_VALUE",
            "C_DeltaK": "MISSING_DELTAK_RESPONSE",
            "retained_channels": "DeltaK;boundary_flux;source_normalization;matter_constants;K_conn;K_domain;K_boundary",
            "gamma_minus_1_predicted": "MISSING",
            "sigma_gamma": "2.3e-05",
            "N_sigma": "1.0",
            "pass_condition": "abs(C_qgamma*q_loc_hat + retained_terms) <= N_sigma*sigma_gamma",
            "result": "BLOCKED_MISSING_QLOC_OR_RESPONSE",
            "source_paths": source_list("1181_ppn", "1244_policy", "1369_runner"),
            **flags(),
        }
    ]


def rejection_rows() -> list[dict[str, Any]]:
    rows = [
        ("REJ1520_0_fixed_grid", "call a coordinate grid spacing L_cg a covariant scalar", "REJECTED", "coordinate/domain lengths have metric/readout dependence unless separated from the action"),
        ("REJ1520_1_cell_volume_silence", "set M_L=0 when L_cg=(V_D)^(1/3)", "REJECTED", "cell-volume length has nonzero metric response and domain-motion terms"),
        ("REJ1520_2_curvature_silence", "set M_L=0 for curvature-defined L_cg", "REJECTED", "curvature length has higher-derivative metric response"),
        ("REJ1520_3_density_silence", "set M_L=0 for density/source-defined L_cg", "REJECTED", "density length needs matter/source descent and volume-measure convention"),
        ("REJ1520_4_qR_import", "use C_qgamma=-1/2 as live q_loc coefficient", "REJECTED", "that coefficient is conditional on a missing q_loc-to-q_R bridge"),
        ("REJ1520_5_single_channel_fit", "ignore DeltaK/boundary/source channels in gamma runner", "REJECTED", "no-cancellation discipline requires retained channels to be zeroed or bounded independently"),
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
        ("GATE1520_0_Lcg_silence_lemma", "fixed scalar L_cg implies M_L=0", "PASS_CONDITIONAL", "exact under fixed-parameter parent contract", False),
        ("GATE1520_1_parent_Lcg_contract_live", "current MTS parent-signs fixed L_cg", "BLOCKED", "contract is not adopted in parent action with covariance/readout/RG clauses", False),
        ("GATE1520_2_composite_Lcg_excluded", "all metric-composite L_cg branches are excluded or bounded", "BLOCKED", "volume/curvature/density/domain counterbranches remain open", False),
        ("GATE1520_3_Cqgamma_conditional", "C_qgamma=-1/2 under q_R bridge", "PASS_CONDITIONAL", "follows only if q_loc equals q_R with same convention and no retained channels", False),
        ("GATE1520_4_Cqgamma_live", "current q_loc-to-gamma response can score", "BLOCKED", "q_loc_hat, live C_qgamma, DeltaK response, and retained-channel bounds are missing", False),
        ("GATE1520_5_local_GR_or_PPN_claim", "local GR / PPN pass can be claimed", "BLOCKED_NO_CLAIM", "L_cg and q_loc-gamma forks remain conditional/nonclaim", False),
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
        ("DEC1520_0_Lcg_contract", "Keep the fixed-scalar L_cg contract as the least-scrutiny metric-silence route.", "CONTRACT_WRITTEN_NOT_CLAIMED", "it is mathematically clean but needs explicit parent-action adoption and readout separation."),
        ("DEC1520_1_composite_guard", "Do not delete M_L for geometric or source-derived L_cg definitions.", "COMPOSITE_BRANCHES_RETAINED", "common coarse-graining meanings are metric-responsive unless bounded."),
        ("DEC1520_2_Cqgamma", "Record C_qgamma=-1/2 only as a q_R-bridge conditional, not live q_loc evidence.", "CONDITIONAL_COEFFICIENT_ONLY", "the current q_loc runner still lacks response, normalization, and retained-channel split."),
        ("DEC1520_3_next", "Next target is q_loc-to-q_R bridge or weak-field operator/source profile.", "NEXT_1521_QLOC_QR_OR_OPERATOR", "this is what can turn Cassini from a comparator into a scoreable local test."),
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
        ("LOCAL1520_0_Lcg", "L_cg algebraic metric response", "CONDITIONAL_SILENCE_ONLY", "M_L=0 is exact if fixed scalar contract is parent-signed"),
        ("LOCAL1520_1_q_loc_gamma", "q_loc to PPN gamma", "SCHEMA_IMPROVED_NOT_SCORE_READY", "conditional q_R bridge coefficient exists but live C_qgamma/q_loc_hat are missing"),
        ("LOCAL1520_2_Newton", "source-normalized Newtonian limit", "NOT_CLAIMED", "M_H_ref and source equality remain missing"),
        ("LOCAL1520_3_GR", "derived local GR", "NOT_CLAIMED", "qObs/current-chain, q_loc, M_H_ref, and weak-field response remain open"),
        ("LOCAL1520_4_empirical", "Cassini/PPN use", "COMPARATOR_ONLY", "sigma_gamma is source-backed but cannot score q_loc without response bridge"),
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
            "next_id": "NEXT1520_0_1521",
            "next_target": "1521-Y5-parent-q_loc-to-qR-bridge-or-weak-field-operator-source-profile.md",
            "script": "scripts/Y5_parent_q_loc_to_qR_bridge_or_weak_field_operator_source_profile.py",
            "objective": "try to prove q_loc_hat reduces to the existing q_R convention with the same source averaging, sign, GM convention, and no retained channels; if not, build the weak-field operator/source-profile rows needed to compute C_qgamma and DeltaK response",
            "do_not": "do not import q_R policy as q_loc evidence; do not claim PPN/local-GR/R10/clock/orbital pass; do not use fitted cancellation",
            **flags(),
        }
    ]


def copy_outputs() -> None:
    copies = [
        (LCG_CONTRACT_AUDIT, QUAR_LCG),
        (CQGAMMA_DERIVATION, QUAR_CQ),
        (QLOC_GAMMA_RUNNER, QUAR_RUNNER),
        (DECISION, QUAR_DECISION),
        (LCG_CONTRACT_AUDIT, BRANCH_LCG),
        (CQGAMMA_DERIVATION, BRANCH_CQ),
        (QLOC_GAMMA_RUNNER, BRANCH_RUNNER),
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
    lcg_contract = read_csv(LCG_CONTRACT_AUDIT)
    theorem = read_csv(LCG_SILENCE_THEOREM)
    cqgamma = read_csv(CQGAMMA_DERIVATION)
    runner = read_csv(QLOC_GAMMA_RUNNER)
    rejections = read_csv(REJECTION_LEDGER)
    gates = read_csv(CLAIM_GATE)
    decisions = read_csv(DECISION)
    next_rows = read_csv(NEXT_TARGET)

    checks = [
        ("VAL1520_0_sources_exist", all(row["exists"] == "True" for row in sources), "all cited 1520 input source paths exist"),
        ("VAL1520_1_Lcg_contract_not_live", any(row["contract_id"] == "LCGC1520_5_current_verdict" and row["status"] == "NOT_PARENT_SIGNED" for row in lcg_contract), "fixed L_cg contract is written but not live-claimed"),
        ("VAL1520_2_ML_conditional_theorem", any(row["theorem_id"] == "ML1520_1_fixed_parameter_derivative" and row["status"] == "DERIVED_CONDITIONAL" for row in theorem), "M_L=0 theorem is captured as exact conditional"),
        ("VAL1520_3_covariance_guard_present", any(row["theorem_id"] == "ML1520_3_covariance_guard" and row["status"] == "GUARD_REQUIRED" for row in theorem), "covariance/readout guard is explicit"),
        ("VAL1520_4_Cqgamma_conditional_only", any(row["derivation_id"] == "CQG1520_2_qR_bridge_conditional" and row["status"] == "CONDITIONAL_COEFFICIENT_ONLY" for row in cqgamma), "C_qgamma=-1/2 is only q_R-bridge conditional"),
        ("VAL1520_5_live_runner_blocked", any(row["row_id"] == "QGR1520_0_live_blocked" and row["result"] == "BLOCKED_MISSING_QLOC_OR_RESPONSE" for row in runner), "live q_loc-gamma runner refuses missing inputs"),
        ("VAL1520_6_rejections_guardrails", len(rejections) >= 6 and all(row["status"] == "REJECTED" for row in rejections), "composite L_cg/q_R/import/cancellation shortcuts rejected"),
        ("VAL1520_7_claim_gates_block_claim", any(row["gate_id"] == "GATE1520_5_local_GR_or_PPN_claim" and row["status"] == "BLOCKED_NO_CLAIM" for row in gates), "local GR/PPN claim remains blocked"),
        ("VAL1520_8_decision_next", any(row["result"] == "NEXT_1521_QLOC_QR_OR_OPERATOR" for row in decisions), "decision selects q_loc-to-q_R bridge or weak-field operator next"),
        ("VAL1520_9_next_target", any("1521-Y5-parent-q_loc-to-qR-bridge" in row["next_target"] for row in next_rows), "next target is q_loc-to-q_R bridge or operator/source profile"),
        ("VAL1520_10_csv_parse", all(parse_csv(path) for path in generated_csvs), "all generated 1520 CSVs parse cleanly"),
        ("VAL1520_11_claim_flags_false", generated_flags_false(generated_csvs), "all generated prediction/claim flags remain false"),
        ("VAL1520_12_branch_copies", all(path.exists() for path in [QUAR_LCG, QUAR_CQ, QUAR_RUNNER, QUAR_DECISION, BRANCH_LCG, BRANCH_CQ, BRANCH_RUNNER, BRANCH_DECISION]), "branch/quarantine nonclaim copies written"),
        ("VAL1520_13_pycache_absent", not (ROOT / "scripts" / "__pycache__").exists(), "scripts __pycache__ absent after run"),
        ("VAL1520_14_formalization_untouched", formalization_modified_count_since_start() == 0, "formalization modified-file count since start=0"),
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
            "check_id": "VAL1520_15_overall",
            "result": "PASS" if overall else "FAIL",
            "detail": "1520 derives the fixed-L_cg silence lemma conditionally, refuses live promotion, records conditional C_qgamma=-1/2 only under q_R bridge, and selects q_loc-to-q_R/operator response next"
            if overall
            else "1520 validation failed; inspect failed rows before continuing",
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
    contract: list[dict[str, Any]],
    theorem: list[dict[str, Any]],
    cqgamma: list[dict[str, Any]],
    runner: list[dict[str, Any]],
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
                "# 1520 - Parent Lcg Contract or q_loc Weak-Field Response Coefficient",
                "",
                "## Verdict",
                "- The fixed-scalar `L_cg` route gives a clean conditional theorem: if `L_cg=L_*` is a parent-fixed scalar parameter held fixed in Hilbert variation, then `M_L^{mu nu}=0`.",
                "- That is not yet a live MTS claim because the parent action has not signed the fixed-scale contract, the readout/domain split, units, or scale-origin/RG rule.",
                "- The weak-field response lane improves too: `C_qgamma=-1/2` is available only under the strict bridge `q_loc_hat == q_R_hat` with identical normalization and no retained channels.",
                "- Therefore no PPN/local-GR claim is made; the next target is the `q_loc -> q_R` bridge or a direct weak-field operator/source-profile calculation.",
                "",
                "## Source Register",
                md_table(sources, ["source_id", "source_path", "exists", "purpose"]),
                "",
                "## Lcg Parent Contract Audit",
                md_table(contract, ["contract_id", "contract_clause", "status", "derivation_or_risk", "missing_to_promote"]),
                "",
                "## Lcg Metric-Silence Theorem",
                md_table(theorem, ["theorem_id", "statement", "derivation", "status", "missing_to_promote"]),
                "",
                "## Cqgamma Derivation Attempt",
                md_table(cqgamma, ["derivation_id", "target", "formula", "meaning", "status"]),
                "",
                "## q_loc Gamma Runner Input Row",
                md_table(runner, ["row_id", "branch", "q_loc_hat", "C_qgamma", "C_qgamma_conditional_qR_bridge", "result"]),
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
    contract = lcg_contract_rows()
    theorem = lcg_silence_theorem_rows()
    cqgamma = cqgamma_rows()
    runner = qloc_gamma_runner_rows()
    rejections = rejection_rows()
    gates = claim_gate_rows()
    decisions = decision_rows()
    local_rows = local_status_rows()
    next_rows = next_target_rows()

    write_csv(SOURCE_REGISTER, sources)
    write_csv(LCG_CONTRACT_AUDIT, contract)
    write_csv(LCG_SILENCE_THEOREM, theorem)
    write_csv(CQGAMMA_DERIVATION, cqgamma)
    write_csv(QLOC_GAMMA_RUNNER, runner)
    write_csv(REJECTION_LEDGER, rejections)
    write_csv(CLAIM_GATE, gates)
    write_csv(DECISION, decisions)
    write_csv(LOCAL_STATUS, local_rows)
    write_csv(NEXT_TARGET, next_rows)
    copy_outputs()
    remove_pycache()

    generated_csvs = [
        SOURCE_REGISTER,
        LCG_CONTRACT_AUDIT,
        LCG_SILENCE_THEOREM,
        CQGAMMA_DERIVATION,
        QLOC_GAMMA_RUNNER,
        REJECTION_LEDGER,
        CLAIM_GATE,
        DECISION,
        LOCAL_STATUS,
        NEXT_TARGET,
    ]
    validation = validation_rows(generated_csvs)
    write_csv(VALIDATION, validation)
    write_doc(sources, contract, theorem, cqgamma, runner, rejections, gates, decisions, local_rows, validation, next_rows)


if __name__ == "__main__":
    main()

from __future__ import annotations

import csv
import shutil
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
FORMALIZATION = ROOT.parent / "formalization-workbench"
OUT = ROOT / "source-intake" / "mts_residuals"
MICROSCOPE = ROOT / "source-intake" / "microscope"
QUARANTINE = MICROSCOPE / "quarantine" / "1617"
INPUT_1617 = QUARANTINE / "input"
BRANCH_RESIDUALS = MICROSCOPE / "branch_locked_wep" / "residuals"
BRANCH_ID = "MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428"
DOC = ROOT / "1617-Y5-R2FR-q_loc-action-reopen-pack-or-residual-bound-roadmap.md"

SOURCE_FILES = {
    "1616_doc": ROOT / "1616-Y5-R2FR-local-branch-status-register-and-reopen-roadmap.md",
    "1616_validation": OUT / "P8_Y5_BRR545_1616_VALIDATION.csv",
    "1616_next": OUT / "P8_Y5_PARENT_QLOC_1616_NEXT_TARGET.csv",
    "1616_status": OUT / "P8_Y5_PARENT_QLOC_1616_LOCAL_BRANCH_STATUS_REGISTER.csv",
    "1616_ranking": OUT / "P8_Y5_PARENT_QLOC_1616_ROUTE_PRIORITY_RANKING.csv",
    "1616_guard": OUT / "P8_Y5_PARENT_QLOC_1616_CLAIM_DRIFT_GUARD.csv",
    "1010_doc": ROOT / "1010-Y5-R10-Gamma-Khat-action-existence-Helmholtz-or-q_loc-residual-retention.md",
    "1010_theorem": OUT / "P8_Y5_R10_1010_THEOREM_ATTEMPT.csv",
    "1010_schema": OUT / "P8_Y5_R10_1010_HELMHOLTZ_ACTION_SCHEMA.csv",
    "1010_residual": OUT / "P8_Y5_R10_1010_RESIDUAL_RETENTION_LEDGER.csv",
    "1011_doc": ROOT / "1011-Y5-R10-response-doublet-source-current-zero-or-q_loc-bound-fill.md",
    "1011_doublet": OUT / "P8_Y5_R10_1011_RESPONSED_DOUBLET_THEOREM_ATTEMPT.csv",
    "1011_bounds": OUT / "P8_Y5_R10_1011_QLOC_BOUND_FILL_ROWS.csv",
    "1011_decision": OUT / "P8_Y5_R10_1011_DECISION_LEDGER.csv",
    "513_rewrite": OUT / "P8_GAMMA_KHAT_QLOC_STRESS_REWRITE.csv",
    "513_contract": OUT / "P8_GAMMA_KHAT_QLOC_FIRST_VARIATION_CONTRACT.csv",
    "515_match": OUT / "P8_GK_METRIC_RESPONSE_MATCH_AUDIT.csv",
    "516_owner": OUT / "P8_GAMMA_OWNER_CANDIDATE_ACTION.csv",
}

NEEDLES = {
    "1616_doc": ["q_loc_action_reopen_pack", "VAL1616_OVERALL"],
    "1616_validation": ["VAL1616_OVERALL", "PASS"],
    "1616_next": ["1617-Y5-R2FR-q_loc-action-reopen-pack-or-residual-bound-roadmap.md", "q_loc reopen pack"],
    "1616_status": ["LBS1616_1_q_loc_action", "OPEN_HIGHEST_LEVERAGE_DERIVATION"],
    "1616_ranking": ["q_loc_action_reopen_pack", "True"],
    "1616_guard": ["CDG1616_3_q_loc", "BLOCK_IF_QLOC_RETAINED"],
    "1010_doc": ["DEC1010_0_derivation_route_precise", "q_loc=0"],
    "1010_theorem": ["GKT1010_6_verdict", "fail_current_claim"],
    "1010_schema": ["HGS1010_4_residual_retention", "q_loc residual"],
    "1010_residual": ["QRES1010_0_q_loc_vector", "retained_until_S_GK_proved"],
    "1011_doc": ["response-doublet double-zero remains a viable conditional route", "q_loc bound-fill rows are staged as nonclaim"],
    "1011_doublet": ["RDT1011_7_verdict", "fail_current_claim"],
    "1011_bounds": ["QBF1011_0_compact_shell_budget", "anchor_proxy_not_claim_curve"],
    "1011_decision": ["DEC1011_1_Y5_is_root_pressure", "source normalization is exchange-even"],
    "513_rewrite": ["SR513_0_define_extra_stress", "algebraic_identity"],
    "513_contract": ["GK513_0_action_existence", "not_supplied"],
    "515_match": ["MA515_1_Khat_metric_response", "fail_for_current_claim"],
    "516_owner": ["GO516_B_positive_auxiliary_energy_density", "candidate_but_source_current_zero_not_derived"],
}

SOURCE_REGISTER = OUT / "P8_Y5_PARENT_QLOC_1617_SOURCE_REGISTER.csv"
REOPEN_PACK = OUT / "P8_Y5_PARENT_QLOC_1617_QLOC_ACTION_REOPEN_PACK.csv"
CERTIFICATE_LEDGER = OUT / "P8_Y5_PARENT_QLOC_1617_CERTIFICATE_STATUS_LEDGER.csv"
RESIDUAL_BOUND_ROADMAP = OUT / "P8_Y5_PARENT_QLOC_1617_RESIDUAL_BOUND_ROADMAP.csv"
BOUND_INPUT_RANKING = OUT / "P8_Y5_PARENT_QLOC_1617_BOUND_INPUT_PRIORITY_RANKING.csv"
RUNNER = OUT / "P8_Y5_PARENT_QLOC_1617_RUNNER.csv"
CLAIM_GATE = OUT / "P8_Y5_PARENT_QLOC_1617_CLAIM_GATE.csv"
DECISION = OUT / "P8_Y5_PARENT_QLOC_1617_DECISION.csv"
NEXT_TARGET = OUT / "P8_Y5_PARENT_QLOC_1617_NEXT_TARGET.csv"
VALIDATION = OUT / "P8_Y5_BRR545_1617_VALIDATION.csv"

COPY_TARGETS = {
    REOPEN_PACK: [
        QUARANTINE / "QLOC_ACTION_REOPEN_PACK_NONCLAIM.csv",
        BRANCH_RESIDUALS / "R2FR_q_loc_action_reopen_pack_nonclaim_1617.csv",
    ],
    CERTIFICATE_LEDGER: [
        QUARANTINE / "CERTIFICATE_STATUS_LEDGER_NONCLAIM.csv",
        BRANCH_RESIDUALS / "R2FR_q_loc_certificate_status_ledger_nonclaim_1617.csv",
    ],
    RESIDUAL_BOUND_ROADMAP: [
        QUARANTINE / "RESIDUAL_BOUND_ROADMAP_NONCLAIM.csv",
        BRANCH_RESIDUALS / "R2FR_q_loc_residual_bound_roadmap_nonclaim_1617.csv",
    ],
    BOUND_INPUT_RANKING: [
        QUARANTINE / "BOUND_INPUT_PRIORITY_RANKING_NONCLAIM.csv",
        BRANCH_RESIDUALS / "R2FR_q_loc_bound_input_priority_ranking_nonclaim_1617.csv",
    ],
    CLAIM_GATE: [
        QUARANTINE / "CLAIM_GATE_CLOSED.csv",
        BRANCH_RESIDUALS / "R2FR_claim_gate_closed_1617.csv",
    ],
}


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def rel(path: Path) -> str:
    try:
        return path.relative_to(ROOT).as_posix()
    except ValueError:
        return str(path)


def truthy(value: Any) -> bool:
    return str(value).strip().lower() in {"true", "1", "yes", "y"}


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def source_register_rows() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for index, (source_id, path) in enumerate(SOURCE_FILES.items()):
        text = read_text(path) if path.exists() else ""
        needles = NEEDLES[source_id]
        rows.append(
            {
                "same_parent_branch_id": BRANCH_ID,
                "source_id": f"SRC1617_{index}_{source_id}",
                "source_path": rel(path) if path.exists() else str(path),
                "exists": path.exists(),
                "needle_found": all(needle in text for needle in needles),
                "needles": "; ".join(needles),
                "source_role": "1617_q_loc_action_reopen_pack_input",
                "valid_for_claim": False,
                "claim_allowed": False,
            }
        )
    return rows


def reopen_pack_rows() -> list[dict[str, Any]]:
    rows = [
        (
            "QRA1617_0_stress_divergence_identity",
            "exact algebraic identity",
            "T_GK^{mu nu}=Gamma_eff g^{mu nu}-K_hat^{mu nu}; q_loc^nu=P_loc nabla_mu T_GK^{mu nu}",
            "CLOSED_EXACT_RECLASSIFICATION",
            "q_loc is a projected Ward/source-exchange residual, not a fundamental field",
            "does not prove q_loc=0",
        ),
        (
            "QRA1617_1_candidate_action",
            "S_GK action existence",
            "find diffeomorphism-invariant S_GK whose Hilbert stress is T_GK",
            "MISSING_PARENT_ACTION",
            "would put q_loc under Ward/Euler control",
            "current S_GK candidate not matched to MTS symbols",
        ),
        (
            "QRA1617_2_metric_response",
            "K_hat metric response",
            "K_hat = K_metric[Gamma_eff] including derivative/boundary terms",
            "MISSING_METRIC_RESPONSE_MATCH",
            "would prevent Gamma/Khat from being independent knobs",
            "515 audit says fail_for_current_claim",
        ),
        (
            "QRA1617_3_Helmholtz",
            "variational Helmholtz symmetry",
            "second metric variation of sqrt(-g)T_GK is symmetric up to boundary/gauge terms",
            "NOT_CHECKED",
            "would establish that proposed stress can come from an action",
            "no current second-variation calculation exists",
        ),
        (
            "QRA1617_4_Euler_double_zero",
            "Euler/source-current zero and local double-zero",
            "E_A=0, source-current=0, boundary=0, T_GK(Phi0)=0 and partial_A T_GK(Phi0)=0",
            "MISSING_EULER_DOUBLE_ZERO",
            "would derive q_loc=0 or second-order/exponentially suppressed leakage",
            "1011 keeps J_Z/B_Z/Y5/Y6/PPN lock open",
        ),
        (
            "QRA1617_5_projector_boundary",
            "P_loc and boundary/no-flux ownership",
            "P_loc fixed by parent branch and boundary symplectic flux vanishes or is bounded",
            "MISSING_PROJECTOR_BOUNDARY_CERTIFICATE",
            "would stop projection/boundary terms hiding a force",
            "source-measure/worldtube bridge still open",
        ),
        (
            "QRA1617_6_residual_bound_fallback",
            "strict q_loc residual-bound branch",
            "if derivation fails, fill q_loc profile/projection coefficients with units and source paths",
            "OPEN_NONCLAIM_FALLBACK",
            "keeps route testable against PPN/R11/clock/orbital/source-normalization gates",
            "1011 bound rows are proxy/template and not claim-ready",
        ),
    ]
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "pack_id": pack_id,
            "certificate": certificate,
            "required_form": required_form,
            "status": status,
            "effect_if_closed": effect,
            "blocking_gap": gap,
            "closed_in_1617": status == "CLOSED_EXACT_RECLASSIFICATION",
            "reopens_local_claim": False,
            "score_ready": False,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        }
        for pack_id, certificate, required_form, status, effect, gap in rows
    ]


def certificate_ledger_rows() -> list[dict[str, Any]]:
    rows = [
        ("CERT1617_0_identity", "stress-divergence identity", "CLOSED_EXACT", "P8_GAMMA_KHAT_QLOC_STRESS_REWRITE.csv", "safe to use as definition/reclassification"),
        ("CERT1617_1_action", "S_GK action source", "OPEN_MISSING", "P8_GAMMA_KHAT_QLOC_FIRST_VARIATION_CONTRACT.csv", "highest proof blocker"),
        ("CERT1617_2_metric_response", "Gamma/Khat metric-response match", "OPEN_FAIL_CURRENT", "P8_GK_METRIC_RESPONSE_MATCH_AUDIT.csv", "must compare tensor structure"),
        ("CERT1617_3_helmholtz", "Helmholtz second-variation symmetry", "OPEN_NOT_CHECKED", "P8_Y5_R10_1010_THEOREM_ATTEMPT.csv", "best next calculational clause"),
        ("CERT1617_4_source_current", "response-doublet source-current zero", "OPEN_FAIL_CURRENT", "P8_Y5_R10_1011_RESPONSED_DOUBLET_THEOREM_ATTEMPT.csv", "Y5/Y6 hard pressure"),
        ("CERT1617_5_ppn_lock", "q_loc to PPN/source-normalization lock", "OPEN_NOT_DERIVED", "P8_Y5_R10_1011_RESPONSED_DOUBLET_THEOREM_ATTEMPT.csv", "needed for observable residual bounds"),
        ("CERT1617_6_bounds", "q_loc numeric/source-backed bound inputs", "OPEN_PROXY_ONLY", "P8_Y5_R10_1011_QLOC_BOUND_FILL_ROWS.csv", "fallback is not claim-ready"),
    ]
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "certificate_id": certificate_id,
            "certificate": certificate,
            "status": status,
            "source_anchor": source_anchor,
            "interpretation": interpretation,
            "reopens_local_claim": False,
            "score_ready": False,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        }
        for certificate_id, certificate, status, source_anchor, interpretation in rows
    ]


def residual_bound_roadmap_rows() -> list[dict[str, Any]]:
    rows = [
        ("QBRM1617_0_q_loc_profile", "q_loc^nu profile or operator vector", "source-backed local profile with units and normalization", "MISSING_PROFILE", "foundation for all residual tests"),
        ("QBRM1617_1_PPN_lock", "weak-field metric/PPN map", "map q_loc profile to gamma,beta,alpha_i,xi or prove silence", "MISSING_PPN_MAP", "required for local GR/PPN comparison"),
        ("QBRM1617_2_source_norm", "R11/source-normalization coefficient", "map q_loc to source/GM/M_eff residual without borrowing measured GM", "MISSING_SOURCE_NORMALIZATION_OWNER", "root Newton normalization pressure"),
        ("QBRM1617_3_alpha3", "alpha3/self-acceleration channel", "q_loc-to-alpha3 coefficient with units and source path", "MISSING_ALPHA3_COEFFICIENT", "ultratight preferred-frame guard"),
        ("QBRM1617_4_time", "Gdot/GMdot/time component", "time projection with yr^-1 units and clock/source convention", "MISSING_TIME_PROJECTION", "clock/orbital drift guard"),
        ("QBRM1617_5_boundary", "boundary/symplectic flux bound", "no-flux theorem or radial M_eff/source-measure bound", "MISSING_BOUNDARY_FLUX_BOUND", "prevents bulk-zero boundary leakage"),
        ("QBRM1617_6_Y6_stress", "extra stress residual", "stress/PPN bound or topological invisibility proof", "MISSING_Y6_STRESS_BOUND", "retained non-EH stress debt"),
    ]
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "roadmap_id": roadmap_id,
            "bound_input": bound_input,
            "required_row": required_row,
            "current_status": status,
            "why_it_matters": why,
            "score_ready": False,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        }
        for roadmap_id, bound_input, required_row, status, why in rows
    ]


def bound_input_ranking_rows() -> list[dict[str, Any]]:
    rows = [
        (1, "metric_response_helmholtz_check", "derivation", "if Helmholtz fails, action route collapses quickly", "compute metric-response/Helmholtz obstruction for candidate S_GK"),
        (2, "Y5_source_normalization_owner", "derivation_or_bound", "1011 says Y5 is root pressure for Newton/GR recovery", "derive mass/source-normalization owner theorem or source coefficient row"),
        (3, "q_loc_profile_operator_vector", "bound", "fallback branch needs actual profile/operator vector before any test", "define q_loc operator vector with units and source path"),
        (4, "PPN_metric_tail_map", "bound", "without observable map q_loc cannot be compared to GR/PPN", "derive weak-field metric response or projection matrix"),
        (5, "boundary_flux_bound", "derivation_or_bound", "bulk Ward zero can still leak through boundary/source-measure", "prove no-flux or stage radial bound"),
    ]
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "priority_rank": rank,
            "input_id": input_id,
            "route_type": route_type,
            "reason": reason,
            "recommended_next_action": action,
            "selected_next": rank == 1,
            "score_ready": False,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        }
        for rank, input_id, route_type, reason, action in rows
    ]


def runner_rows() -> list[dict[str, Any]]:
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "runner_id": "RUN1617_0_identity",
            "input_state": "513 stress-divergence identity imported",
            "runner_result": "CLOSE_QLOC_RECLASSIFICATION_ONLY",
            "effect": "q_loc treated as projected stress-divergence residual, not fundamental field",
            "score_ready": False,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "runner_id": "RUN1617_1_action_route",
            "input_state": "action/metric-response/Helmholtz/Euler certificates open",
            "runner_result": "DO_NOT_REOPEN_LOCAL_GR",
            "effect": "derived local GR remains blocked",
            "score_ready": False,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "runner_id": "RUN1617_2_next",
            "input_state": "metric-response and Helmholtz are the fastest falsifiable action clauses",
            "runner_result": "SELECT_METRIC_RESPONSE_HELMHOLTZ_AUDIT_NEXT",
            "effect": "next step attacks a concrete derivation gate",
            "score_ready": False,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]


def claim_gate_rows() -> list[dict[str, Any]]:
    gates = [
        ("CG1617_0_identity", "q_loc residual identity", "CLOSED_DEFINITION_ONLY", "algebraic reclassification closes but does not prove zero"),
        ("CG1617_1_SGK", "S_GK parent action", "BLOCKED", "candidate action not matched to MTS symbols"),
        ("CG1617_2_metric_response", "K_hat metric response", "BLOCKED", "metric-response tensor match absent"),
        ("CG1617_3_helmholtz", "Helmholtz variational stress", "BLOCKED", "second variation symmetry not checked"),
        ("CG1617_4_euler_double_zero", "Euler/source-current zero and double-zero", "BLOCKED", "Y5/Y6/PPN/boundary terms remain open"),
        ("CG1617_5_residual_bound", "claim-ready q_loc bound", "BLOCKED", "bound rows are proxy/template and mappings missing"),
        ("CG1617_6_local_GR", "derived local GR/Newton recovery", "BLOCKED", "1616 demotion remains active"),
    ]
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "gate_id": gate_id,
            "claim": claim,
            "status": status,
            "reason": reason,
            "valid_for_claim": False,
            "claim_allowed": False,
        }
        for gate_id, claim, status, reason in gates
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "decision_id": "DEC1617_0_identity",
            "decision": "QLOC_EXACTLY_RECLASSIFIED_AS_PROJECTED_STRESS_DIVERGENCE",
            "reason": "513 stress rewrite gives exact T_GK identity",
            "next_action": "use q_loc as residual object, not a standalone field",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "decision_id": "DEC1617_1_no_promotion",
            "decision": "LOCAL_GR_NOT_REOPENED",
            "reason": "S_GK, metric response, Helmholtz, Euler/double-zero, boundary and observable map certificates remain open",
            "next_action": "attack metric-response/Helmholtz first",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "decision_id": "DEC1617_2_next",
            "decision": "NEXT_1618_METRIC_RESPONSE_HELMHOLTZ_AUDIT_OR_QLOC_BOUND_SCHEMA",
            "reason": "metric-response/Helmholtz is the fastest sharp test of whether q_loc can be action-owned",
            "next_action": "compare candidate S_GK stress variation against K_hat/Gamma structure; otherwise harden q_loc bound schema",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "next_target": "1618-Y5-R2FR-metric-response-Helmholtz-audit-or-q_loc-bound-schema.md",
            "script": "scripts/Y5_R2FR_metric_response_Helmholtz_audit_or_q_loc_bound_schema.py",
            "objective": "test the metric-response/Helmholtz gate for candidate S_GK; if it fails, harden q_loc residual-bound schema",
            "success_condition": "one concrete action-ownership clause is passed/failed with source anchors, or q_loc bound schema is upgraded without local-GR promotion",
            "do_not": "do not use plateau axiom, bookkeeping stress, EH-only import, fitted cancellation, measured-G absorption, or public/local-GR claims",
            "score_ready": False,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        }
    ]


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
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


def copy_outputs() -> None:
    for source, targets in COPY_TARGETS.items():
        for target in targets:
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(source, target)


def remove_pycache() -> None:
    pycache = Path(__file__).resolve().parent / "__pycache__"
    if pycache.exists():
        shutil.rmtree(pycache)


def csv_parses(paths: list[Path]) -> bool:
    try:
        for path in paths:
            read_csv(path)
    except Exception:
        return False
    return True


def no_claim_flags(paths: list[Path]) -> bool:
    for path in paths:
        for row in read_csv(path):
            for field in ("reopens_local_claim", "score_ready", "valid_prediction_row", "valid_for_claim", "claim_allowed"):
                if truthy(row.get(field, "")):
                    return False
    return True


def no_formalization_1617() -> bool:
    if not FORMALIZATION.exists():
        return True
    artifact_markers = (
        "1617-Y5",
        "P8_Y5_PARENT_QLOC_1617",
        "P8_Y5_BRR545_1617",
        "Y5_R2FR_q_loc_action_reopen_pack_or_residual_bound_roadmap",
        "R2FR_q_loc_action",
        "R2FR_q_loc_certificate",
        "R2FR_q_loc_residual_bound",
    )
    return not any(any(marker in path.name for marker in artifact_markers) for path in FORMALIZATION.rglob("*"))


def validation_rows(generated_csvs: list[Path]) -> list[dict[str, Any]]:
    sources = source_register_rows()
    pack = read_csv(REOPEN_PACK)
    certs = read_csv(CERTIFICATE_LEDGER)
    roadmap = read_csv(RESIDUAL_BOUND_ROADMAP)
    ranking = read_csv(BOUND_INPUT_RANKING)
    runner = read_csv(RUNNER)
    gates = read_csv(CLAIM_GATE)
    decisions = read_csv(DECISION)
    copies = [target for targets in COPY_TARGETS.values() for target in targets]
    checks = [
        ("VAL1617_0_sources_exist", all(truthy(row["exists"]) for row in sources), "all cited 1617 local source paths exist"),
        ("VAL1617_1_needles_found", all(truthy(row["needle_found"]) for row in sources), "all required 1617 source needles found"),
        ("VAL1617_2_input_dir_ready", INPUT_1617.exists(), "1617 quarantine input directory exists"),
        ("VAL1617_3_identity_closed", any(row["pack_id"] == "QRA1617_0_stress_divergence_identity" and row["status"] == "CLOSED_EXACT_RECLASSIFICATION" for row in pack), "q_loc stress-divergence identity closed as reclassification"),
        ("VAL1617_4_no_local_reopen", all(row["reopens_local_claim"].lower() == "false" for row in pack), "reopen pack does not reopen local claims"),
        ("VAL1617_5_certificate_ledger", len(certs) >= 7 and any(row["certificate_id"] == "CERT1617_3_helmholtz" for row in certs), "certificate ledger covers action/metric/Helmholtz/source/bound clauses"),
        ("VAL1617_6_bound_roadmap", len(roadmap) >= 7 and all(row["valid_for_claim"].lower() == "false" for row in roadmap), "residual bound roadmap remains nonclaim"),
        ("VAL1617_7_metric_helmholtz_ranked_first", any(row["priority_rank"] == "1" and row["input_id"] == "metric_response_helmholtz_check" and row["selected_next"].lower() == "true" for row in ranking), "metric-response/Helmholtz check ranked first"),
        ("VAL1617_8_runner_selects_next", any(row["runner_id"] == "RUN1617_2_next" and row["runner_result"] == "SELECT_METRIC_RESPONSE_HELMHOLTZ_AUDIT_NEXT" for row in runner), "runner selects metric-response/Helmholtz audit next"),
        ("VAL1617_9_claim_gates_closed", gates and all(row["claim_allowed"].lower() == "false" for row in gates), "all 1617 claim gates remain nonclaim"),
        ("VAL1617_10_decision_next", any(row["decision"] == "NEXT_1618_METRIC_RESPONSE_HELMHOLTZ_AUDIT_OR_QLOC_BOUND_SCHEMA" for row in decisions), "decision selects 1618 metric-response/Helmholtz audit"),
        ("VAL1617_11_csv_parse", csv_parses(generated_csvs), "all generated 1617 CSVs parse"),
        ("VAL1617_12_claim_safety_flags", no_claim_flags(generated_csvs), "no generated 1617 rows reopen local claims, score-ready rows, prediction rows, valid-for-claim, or claim-allowed"),
        ("VAL1617_13_branch_copies", all(path.exists() for path in copies), "branch/quarantine nonclaim copies exist"),
        ("VAL1617_14_pycache_absent", not (Path(__file__).resolve().parent / "__pycache__").exists(), "scripts __pycache__ absent"),
        ("VAL1617_15_formalization_untouched", no_formalization_1617(), "no 1617 outputs found under formalization-workbench"),
    ]
    rows = [
        {
            "same_parent_branch_id": BRANCH_ID,
            "check_id": check_id,
            "result": "PASS" if ok else "FAIL",
            "detail": detail,
        }
        for check_id, ok, detail in checks
    ]
    rows.append(
        {
            "same_parent_branch_id": BRANCH_ID,
            "check_id": "VAL1617_OVERALL",
            "result": "PASS" if all(row["result"] == "PASS" for row in rows) else "FAIL",
            "detail": "1617 q_loc action reopen pack or residual-bound roadmap validation",
        }
    )
    return rows


def md_table(rows: list[dict[str, Any]], columns: list[str]) -> str:
    header = "| " + " | ".join(columns) + " |"
    sep = "| " + " | ".join("---" for _ in columns) + " |"
    body = []
    for row in rows:
        body.append("| " + " | ".join(str(row.get(column, "")).replace("\n", " ").replace("|", "/") for column in columns) + " |")
    return "\n".join([header, sep, *body])


def write_doc(
    sources: list[dict[str, Any]],
    pack: list[dict[str, Any]],
    certs: list[dict[str, Any]],
    roadmap: list[dict[str, Any]],
    ranking: list[dict[str, Any]],
    runner: list[dict[str, Any]],
    gates: list[dict[str, Any]],
    decisions: list[dict[str, Any]],
    next_rows: list[dict[str, Any]],
    validation: list[dict[str, Any]],
) -> None:
    DOC.write_text(
        "\n\n".join(
            [
                "# 1617 - R2/fR q_loc Action Reopen Pack Or Residual-Bound Roadmap",
                "## Verdict\n"
                "- 1617 closes one modest but important clause: `q_loc` is exactly a projected divergence of `T_GK = Gamma_eff g - K_hat`, so it is a residual object rather than a new fundamental field.\n"
                "- This does not derive `q_loc=0`; action existence, metric-response match, Helmholtz symmetry, Euler/double-zero, projector and boundary clauses remain open.\n"
                "- The response-doublet route remains a serious conditional mechanism, but 1011 keeps Y5/Y6, source-current, boundary, and PPN-lock blockers live.\n"
                "- The residual-bound fallback is organized, but current q_loc bound rows are proxy/template only and not claim-ready.\n"
                "- No WEP, R10, PPN, clock, orbital, Newton, local-GR, beta/coupling, or public claim is made.",
                "## Source Register",
                md_table(sources, ["source_id", "source_path", "exists", "needle_found", "needles"]),
                "## q_loc Action Reopen Pack",
                md_table(pack, ["pack_id", "certificate", "status", "effect_if_closed", "blocking_gap", "closed_in_1617"]),
                "## Certificate Status Ledger",
                md_table(certs, ["certificate_id", "certificate", "status", "source_anchor", "interpretation"]),
                "## Residual Bound Roadmap",
                md_table(roadmap, ["roadmap_id", "bound_input", "required_row", "current_status", "why_it_matters"]),
                "## Bound Input Priority Ranking",
                md_table(ranking, ["priority_rank", "input_id", "route_type", "reason", "recommended_next_action", "selected_next"]),
                "## Runner",
                md_table(runner, ["runner_id", "input_state", "runner_result", "effect"]),
                "## Claim Gates",
                md_table(gates, ["gate_id", "claim", "status", "reason"]),
                "## Decision",
                md_table(decisions, ["decision_id", "decision", "reason", "next_action"]),
                "## Next Target",
                md_table(next_rows, ["next_target", "script", "objective", "success_condition", "do_not"]),
                "## Validation",
                md_table(validation, ["check_id", "result", "detail"]),
            ]
        )
        + "\n",
        encoding="utf-8",
    )


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    INPUT_1617.mkdir(parents=True, exist_ok=True)
    sources = source_register_rows()
    pack = reopen_pack_rows()
    certs = certificate_ledger_rows()
    roadmap = residual_bound_roadmap_rows()
    ranking = bound_input_ranking_rows()
    runner = runner_rows()
    gates = claim_gate_rows()
    decisions = decision_rows()
    next_rows = next_target_rows()
    generated_csvs = [
        SOURCE_REGISTER,
        REOPEN_PACK,
        CERTIFICATE_LEDGER,
        RESIDUAL_BOUND_ROADMAP,
        BOUND_INPUT_RANKING,
        RUNNER,
        CLAIM_GATE,
        DECISION,
        NEXT_TARGET,
    ]
    write_csv(SOURCE_REGISTER, sources)
    write_csv(REOPEN_PACK, pack)
    write_csv(CERTIFICATE_LEDGER, certs)
    write_csv(RESIDUAL_BOUND_ROADMAP, roadmap)
    write_csv(BOUND_INPUT_RANKING, ranking)
    write_csv(RUNNER, runner)
    write_csv(CLAIM_GATE, gates)
    write_csv(DECISION, decisions)
    write_csv(NEXT_TARGET, next_rows)
    copy_outputs()
    remove_pycache()
    validation = validation_rows(generated_csvs)
    write_csv(VALIDATION, validation)
    write_doc(sources, pack, certs, roadmap, ranking, runner, gates, decisions, next_rows, validation)


if __name__ == "__main__":
    main()

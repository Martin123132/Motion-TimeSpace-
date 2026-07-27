from __future__ import annotations

import csv
import shutil
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
FORMALIZATION = ROOT.parent / "formalization-workbench"
OUT = ROOT / "source-intake" / "mts_residuals"
MICROSCOPE = ROOT / "source-intake" / "microscope"
RAB_SECTOR = ROOT / "source-intake" / "rab-sector"
QUEUE = RAB_SECTOR / "acquisition-queue"
QUARANTINE = MICROSCOPE / "quarantine" / "1648"
BRANCH_RESIDUALS = MICROSCOPE / "branch_locked_wep" / "residuals"
BRANCH_ID = "MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428"
DOC = ROOT / "1648-Y5-R2FR-observed-reduced-boundary-source-flux-zero-or-deltaH-curl-component-fill.md"

SOURCE_FILES = {
    "1647_doc": ROOT / "1647-Y5-R2FR-hybrid-EH-quotient-current-owner-or-deltaH-curl-source-fill.md",
    "1647_validation": OUT / "P8_Y5_BRR545_1647_VALIDATION.csv",
    "1647_next": OUT / "P8_Y5_PARENT_QLOC_1647_NEXT_TARGET.csv",
    "1647_curl": OUT / "P8_Y5_PARENT_QLOC_1647_DELTAH_CURL_DECOMPOSITION.csv",
    "1647_fallback": OUT / "P8_Y5_PARENT_QLOC_1647_DELTAH_CURL_SOURCE_FILL_FALLBACK.csv",
    "773_doc": ROOT / "773-Y5-R10-observed-reduced-boundary-source-flux-zero-or-deltaH-curl-component-fill.md",
    "773_validation": OUT / "P8_Y5_BRR545_773_VALIDATION.csv",
    "773_attempt": OUT / "P8_Y5_R10_773_OBSERVED_FLUX_ZERO_ATTEMPT.csv",
    "773_clause_gate": OUT / "P8_Y5_R10_773_OBSERVED_FLUX_ZERO_CLAUSE_GATE.csv",
    "773_component_split": OUT / "P8_Y5_R10_773_OBSERVED_FLUX_COMPONENT_SPLIT.csv",
    "773_component_fill": OUT / "P8_Y5_R10_773_DELTAH_CURL_COMPONENT_FILL.csv",
    "773_decision": OUT / "P8_Y5_R10_773_DECISION_MATRIX.csv",
    "774_doc": ROOT / "774-Y5-R10-reduced-GK-symbol-match-or-observed-boundary-flux-input-runner.md",
    "774_validation": OUT / "P8_Y5_BRR545_774_VALIDATION.csv",
    "774_reentry": OUT / "P8_Y5_R10_774_REDUCED_GK_SYMBOL_MATCH_REENTRY_AUDIT.csv",
    "774_schema": OUT / "P8_Y5_R10_774_BOBS_INPUT_RUNNER_SCHEMA.csv",
    "774_dryrun": OUT / "P8_Y5_R10_774_BOBS_INPUT_RUNNER_DRYRUN.csv",
    "774_decision": OUT / "P8_Y5_R10_774_DECISION_MATRIX.csv",
}

NEEDLES = {
    "1647_doc": ["B_observed_reduced_flux_over_MH", "observed reduced Ward/no-flux"],
    "1647_validation": ["VAL1647_OVERALL", "PASS"],
    "1647_next": ["1648-Y5-R2FR-observed-reduced-boundary-source-flux-zero-or-deltaH-curl-component-fill.md"],
    "1647_curl": ["CDC1647_2_observed_reduced_boundary_flux", "OPEN_PRIMARY_NEXT_TARGET"],
    "1647_fallback": ["HSF1647_0_observed_reduced_boundary_flux", "MISSING_OBSERVED_REDUCED_BOUNDARY_FLUX_ZERO_OR_NUMERIC"],
    "773_doc": ["reduced Ward/no-flux path is mathematically clean", "B_observed_reduced_flux_over_MH"],
    "773_validation": ["V773_9_next_target_selected", "pass"],
    "773_attempt": ["OFZ773_3_current_MTS_verdict", "fail_current_corpus"],
    "773_clause_gate": ["OFC773_0", "blocked"],
    "773_component_split": ["OFS773_5_total_observed_reduced_flux", "B_observed_reduced_flux_over_MH"],
    "773_component_fill": ["BCF773_5_total_B_observed", "MISSING_COMPONENTS"],
    "773_decision": ["D773_2_component_fill_staged", "B_observed_reduced_flux_over_MH"],
    "774_doc": ["reduced GK symbol match still fails for current MTS", "observed `B_obs` component runner"],
    "774_validation": ["V774_10_next_target_selected", "pass"],
    "774_reentry": ["RGM774_7_verdict", "fail_current_corpus"],
    "774_schema": ["BIR774_5_total_Bobs", "MISSING_COMPONENTS"],
    "774_dryrun": ["BDR774_0_symbol_match_certificate_absent", "blocked"],
    "774_decision": ["D774_2_Bobs_runner_staged", "observed-boundary-flux input runner"],
}

SOURCE_REGISTER = OUT / "P8_Y5_PARENT_QLOC_1648_SOURCE_REGISTER.csv"
THEOREM_ATTEMPT = OUT / "P8_Y5_PARENT_QLOC_1648_OBSERVED_REDUCED_FLUX_THEOREM_ATTEMPT.csv"
CLAUSE_GATE = OUT / "P8_Y5_PARENT_QLOC_1648_OBSERVED_FLUX_ZERO_CLAUSE_GATE.csv"
COMPONENT_FILL = OUT / "P8_Y5_PARENT_QLOC_1648_DELTAH_CURL_COMPONENT_FILL.csv"
INPUT_RUNNER = OUT / "P8_Y5_PARENT_QLOC_1648_BOBS_INPUT_RUNNER_DRYRUN.csv"
DECISION = OUT / "P8_Y5_PARENT_QLOC_1648_DECISION.csv"
CLAIM_GATE = OUT / "P8_Y5_PARENT_QLOC_1648_CLAIM_GATE.csv"
NEXT_TARGET = OUT / "P8_Y5_PARENT_QLOC_1648_NEXT_TARGET.csv"
VALIDATION = OUT / "P8_Y5_BRR545_1648_VALIDATION.csv"

GENERATED = [
    SOURCE_REGISTER,
    THEOREM_ATTEMPT,
    CLAUSE_GATE,
    COMPONENT_FILL,
    INPUT_RUNNER,
    DECISION,
    CLAIM_GATE,
    NEXT_TARGET,
]

CLAIM_CHECKED = [
    THEOREM_ATTEMPT,
    CLAUSE_GATE,
    COMPONENT_FILL,
    INPUT_RUNNER,
    DECISION,
    CLAIM_GATE,
    NEXT_TARGET,
]


def ensure_dirs() -> None:
    for directory_path in [OUT, QUARANTINE, BRANCH_RESIDUALS, QUEUE]:
        directory_path.mkdir(parents=True, exist_ok=True)


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace") if path.exists() else ""


def rel(path: Path) -> str:
    try:
        return str(path.relative_to(ROOT))
    except ValueError:
        return str(path)


def write_csv(path: Path, rows: list[dict[str, object]]) -> None:
    if not rows:
        raise ValueError(f"cannot write empty csv: {path}")
    path.parent.mkdir(parents=True, exist_ok=True)
    fieldnames = list(rows[0].keys())
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def csv_rows(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def bool_string(value: object) -> str:
    return str(value).strip().lower()


def all_claim_flags_false(paths: list[Path]) -> bool:
    flag_names = {"valid_for_claim", "valid_for_mts_claim", "claim_allowed", "score_allowed"}
    for path in paths:
        for row in csv_rows(path):
            for flag_name in flag_names.intersection(row):
                if bool_string(row[flag_name]) == "true":
                    return False
    return True


def source_register_rows() -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    for source_id, path in SOURCE_FILES.items():
        text = read_text(path)
        needles = NEEDLES[source_id]
        rows.append(
            {
                "branch_id": BRANCH_ID,
                "source_id": source_id,
                "path": str(path),
                "path_exists": path.exists(),
                "needles_found": all(needle in text for needle in needles),
                "needles": "; ".join(needles),
                "role": "1648 observed reduced boundary/source flux theorem and component-fill checkpoint",
                "valid_for_claim": False,
                "claim_allowed": False,
            }
        )
    return rows


def theorem_attempt_rows() -> list[dict[str, object]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "attempt_id": "OFZ1648_0_reduced_Ward_identity",
            "target": "observed reduced boundary/source flux",
            "identity": "q_loc^nu = P_loc nabla_mu T_GK^{mu nu} = P_loc(sum_A E_A nabla^nu Phi_A + B_obs^nu)",
            "premises": "reduced action ownership; metric response K_hat; parent-owned P_loc; on-shell reduced fields; fixed boundary/reference; no source-measure leakage",
            "current_status": "CONDITIONAL_IDENTITY_AVAILABLE",
            "why_not_zero": "E_A, B_obs, source-measure, corner/edge, and projector terms can survive",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "attempt_id": "OFZ1648_1_compact_exterior_no_flux_contract",
            "target": "B_observed_reduced_flux_over_MH",
            "identity": "If S_red is parent-owned/diffeomorphism invariant, E_A=0, P_loc descends, and all observed boundary/source-measure flux is exact/proper/fixed-reference, then P_loc B_obs^nu=0",
            "premises": "OFC1648_0 through OFC1648_6 all pass together",
            "current_status": "CONDITIONAL_THEOREM_CONTRACT_WRITTEN",
            "why_not_zero": "premises unsigned for current claim",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "attempt_id": "OFZ1648_2_boundary_source_flux_zero_attempt",
            "target": "P_loc B_boundary^nu plus reduced observed source flux",
            "identity": "B_obs^nu := B_GK^nu + B_corner^nu + B_source_measure^nu + B_projector^nu",
            "premises": "boundary collar silence; no improper observed edge modes; same-frame source measure; no post-readout projector; no hidden ADM subtraction",
            "current_status": "FAIL_CURRENT_CLAIM",
            "why_not_zero": "observed boundary/source flux remains live",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "attempt_id": "OFZ1648_3_current_MTS_verdict",
            "target": "promote observed reduced flux zero",
            "identity": "B_observed_reduced_flux_over_MH = 0",
            "premises": "S_red, Gamma_eff/K_hat/P_loc ownership, Euler equations, no-flux boundary, source-measure silence, projector descent, tau/surface lock",
            "current_status": "FAIL_CURRENT_CLAIM",
            "why_not_zero": "reduced GK symbol match and observed no-flux components are not parent-signed",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "attempt_id": "OFZ1648_4_no_smuggling_gate",
            "target": "boundary condition discipline",
            "identity": "proper representative boundary zero cannot be reused as observed reduced no-flux condition",
            "premises": "observed boundary condition must be parent/domain/theorem signed, not imposed after readout to erase physical flux",
            "current_status": "DISCIPLINE_GATE_PASSED",
            "why_not_zero": "observed reduced flux still needs owner theorem or source-backed bound",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]


def clause_gate_rows() -> list[dict[str, object]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "clause_id": "OFC1648_0_Sred_owner",
            "required_clause": "S_red is a parent-owned reduced diffeomorphism-invariant action on Q_obs^hybrid",
            "would_kill": "turns q_loc into a Ward/Euler/boundary identity rather than a symbol",
            "current_status": "BLOCKED",
            "failure_if_missing": "q_loc residual is not a theorem-owned divergence",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "clause_id": "OFC1648_1_Gamma_Khat_Ploc_owner",
            "required_clause": "Gamma_eff, K_hat, and P_loc are the reduced variational objects",
            "would_kill": "identifies B_obs terms and prevents symbol-level substitution",
            "current_status": "BLOCKED_BY_REDUCED_GK_SYMBOL_MATCH",
            "failure_if_missing": "K_hat/Gamma/P_loc can hide independent residuals",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "clause_id": "OFC1648_2_bulk_Euler_on_shell",
            "required_clause": "all reduced fields are on shell in the compact exterior",
            "would_kill": "B_obs_bulk_Euler_over_MH",
            "current_status": "BLOCKED",
            "failure_if_missing": "bulk Euler flux remains a deltaH curl component",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "clause_id": "OFC1648_3_boundary_reference_no_flux",
            "required_clause": "observed boundary/corner/reference terms are fixed, exact, proper, or theorem-cancelled",
            "would_kill": "B_obs_boundary_improvement_over_MH and B_obs_corner_edge_over_MH",
            "current_status": "BLOCKED",
            "failure_if_missing": "finite compact-boundary Hamiltonian flux can survive",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "clause_id": "OFC1648_4_source_measure_silence",
            "required_clause": "source-measure and hidden mass-normalization flux are zero or explicitly bounded",
            "would_kill": "B_obs_source_measure_over_MH",
            "current_status": "BLOCKED",
            "failure_if_missing": "Y5/source-normalization flux remains live",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "clause_id": "OFC1648_5_projector_descent",
            "required_clause": "P_loc/Pi_M descends without commutator/domain leakage",
            "would_kill": "B_obs_projector_commutator_over_MH",
            "current_status": "BLOCKED",
            "failure_if_missing": "projector commutator flux remains live",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "clause_id": "OFC1648_6_tau_surface_lock",
            "required_clause": "same tau, surface/domain, and reference branch are fixed before readout",
            "would_kill": "tau/surface/reference part of the same observed flux chain",
            "current_status": "BLOCKED",
            "failure_if_missing": "observed no-flux theorem can be shifted by readout choices",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]


def component_fill_rows() -> list[dict[str, object]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "fill_id": "BCF1648_0_bulk_Euler_flux",
            "quantity": "B_obs_bulk_Euler_over_MH",
            "definition": "abs(P_loc sum_A E_A nabla^nu Phi_A contribution to curl(deltaH))/M_H_ref",
            "required_columns": "system_id;annulus;field_A;E_A;nabla_Phi_A;P_loc_component;M_H_ref;units;source_path;valid_for_claim",
            "current_status": "MISSING_REDUCED_EULER_ZERO_OR_NUMERIC",
            "claim_gate": "on-shell reduced-field theorem or source-backed compact-exterior bound",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "fill_id": "BCF1648_1_boundary_improvement_flux",
            "quantity": "B_obs_boundary_improvement_over_MH",
            "definition": "abs(P_loc B_GK^nu plus reference/improvement contribution to curl(deltaH))/M_H_ref",
            "required_columns": "system_id;surface_id;boundary_class;B_GK_component;B_ref_component;P_loc_component;M_H_ref;units;source_path;valid_for_claim",
            "current_status": "MISSING_BOUNDARY_REFERENCE_NO_FLUX_OR_NUMERIC",
            "claim_gate": "fixed-reference no-flux theorem or explicit finite-boundary flux bound",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "fill_id": "BCF1648_2_source_measure_flux",
            "quantity": "B_obs_source_measure_over_MH",
            "definition": "abs(P_loc B_source_measure^nu or C_qmu q_loc projection contribution)/M_H_ref",
            "required_columns": "system_id;source_measure_rule;C_qmu;q_loc_component;M_H_ref;units;source_path;valid_for_claim",
            "current_status": "MISSING_SOURCE_MEASURE_SILENCE_OR_NUMERIC",
            "claim_gate": "same-frame source-measure theorem or explicit source-backed flux bound",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "fill_id": "BCF1648_3_corner_edge_flux",
            "quantity": "B_obs_corner_edge_over_MH",
            "definition": "abs(non-proper observed edge/corner symplectic flux)/M_H_ref",
            "required_columns": "system_id;corner_or_edge_mode;flux_value;M_H_ref;units;source_path;valid_for_claim",
            "current_status": "MISSING_OBSERVED_EDGE_ZERO_OR_NUMERIC",
            "claim_gate": "observed edge/corner theorem-zero or explicit finite flux bound",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "fill_id": "BCF1648_4_projector_commutator_flux",
            "quantity": "B_obs_projector_commutator_over_MH",
            "definition": "abs(integral_A [d,P_loc]J_red or [d,Pi_M]J_H contribution)/M_H_ref",
            "required_columns": "system_id;projector_id;commutator_value;domain_dependence;M_H_ref;units;source_path;valid_for_claim",
            "current_status": "MISSING_PROJECTOR_DESCENT_ZERO_OR_NUMERIC",
            "claim_gate": "parent-owned topological/projector descent theorem or finite commutator bound",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "fill_id": "BCF1648_5_total_B_observed",
            "quantity": "B_observed_reduced_flux_over_MH",
            "definition": "sum of nonnegative observed reduced flux components with no cancellation credit",
            "required_columns": "component_id;value;units;source_path;zero_theorem_or_bound;no_cancellation_flag;valid_for_claim",
            "current_status": "MISSING_COMPONENTS",
            "claim_gate": "all BCF1648 component rows zero/bounded with no placeholders",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]


def input_runner_rows() -> list[dict[str, object]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "run_id": "BIR1648_0_no_candidate",
            "quantity": "B_observed_reduced_flux_over_MH",
            "input_status": "MISSING_COMPONENTS",
            "computed_status": "BLOCKED_MISSING_COMPONENTS",
            "score_allowed": False,
            "claim_allowed": False,
            "valid_for_mts_claim": False,
            "failure_reasons": "MISSING_M_H_REF;MISSING_BULK_EULER;MISSING_BOUNDARY_IMPROVEMENT;MISSING_SOURCE_MEASURE;MISSING_CORNER_EDGE;MISSING_PROJECTOR_COMMUTATOR;VALID_FOR_CLAIM_FALSE",
        }
    ]


def decision_rows() -> list[dict[str, object]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "decision_id": "DEC1648_0_conditional_theorem_retained",
            "decision": "retain the compact-exterior reduced Ward no-flux theorem as a contract",
            "reason": "it is the correct mathematical route if S_red and all reduced boundary/source/projector clauses are parent-owned",
            "effect": "the no-flux theorem remains a target, not a claim",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "decision_id": "DEC1648_1_zero_not_promoted",
            "decision": "do not promote observed reduced boundary/source flux to zero for current MTS",
            "reason": "Gamma_eff/K_hat/P_loc ownership, Euler equations, boundary/reference no-flux, source-measure silence, projector descent, and tau/surface lock are not jointly signed",
            "effect": "B_observed_reduced_flux_over_MH remains a live deltaH curl component",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "decision_id": "DEC1648_2_component_fill_staged",
            "decision": "stage B_observed_reduced_flux_over_MH as decomposed deltaH curl component rows",
            "reason": "if the theorem route fails, the component must be bounded rather than erased",
            "effect": "future runner can accept only real zero/source-backed component rows",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "decision_id": "DEC1648_3_next_symbol_match",
            "decision": "attack reduced GK symbol match before numeric B_obs scoring",
            "reason": "the no-flux theorem cannot be evaluated until Gamma_eff, K_hat, and P_loc are parent-owned reduced variational objects",
            "effect": "1649 should test reduced GK symbol match or keep B_obs input runner blocked",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]


def claim_gate_rows() -> list[dict[str, object]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "gate_id": "CG1648_0_reduced_no_flux",
            "claim": "B_observed_reduced_flux_over_MH is theorem-zero",
            "gate_pass": False,
            "status": "BLOCKED",
            "blocker": "REDUCED_GK_SYMBOL_MATCH_AND_NO_FLUX_CLAUSES_UNSIGNED",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "gate_id": "CG1648_1_component_runner",
            "claim": "B_obs component runner can score",
            "gate_pass": False,
            "status": "NOT_SCORED",
            "blocker": "component rows and M_H_ref are missing",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "gate_id": "CG1648_2_no_smuggling",
            "claim": "representative proper-zero may be reused as observed no-flux",
            "gate_pass": False,
            "status": "REFUSED",
            "blocker": "REPRESENTATIVE_ZERO_IS_NOT_OBSERVED_FLUX_ZERO",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "gate_id": "CG1648_3_local_GR_PPN_R10",
            "claim": "local GR, PPN, R10, or Newton pass follows from 1648",
            "gate_pass": False,
            "status": "NO_CLAIM",
            "blocker": "observed reduced flux remains live",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "gate_id": "CG1648_4_guardrail",
            "claim": "observed reduced flux guardrail is installed",
            "gate_pass": True,
            "status": "PASS_AS_INTERNAL_GUARDRAIL_ONLY",
            "blocker": "guardrail is not evidence",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]


def next_target_rows() -> list[dict[str, object]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "next_target": "1649-Y5-R2FR-reduced-GK-symbol-match-or-observed-boundary-flux-input-runner.md",
            "script": "scripts/Y5_R2FR_reduced_GK_symbol_match_or_observed_boundary_flux_input_runner.py",
            "objective": "test whether Gamma_eff, K_hat, and P_loc are parent-owned reduced variational objects; otherwise keep the B_obs input runner blocked with explicit missing components",
            "success_condition": "S_GK^hyb supplies Gamma_eff scalar density, K_hat metric response, P_loc descent, Helmholtz/integrability, and observed boundary/source metric-variation accounting, or B_obs rows remain nonclaim",
            "guardrails": "no symbol substitution; no representative-zero reuse; no fitted boundary condition; no PPN/local-GR/R10 claim; no orbital-GM denominator",
            "valid_for_mts_claim": False,
            "claim_allowed": False,
            "score_allowed": False,
        }
    ]


def copy_outputs() -> None:
    for path in GENERATED + [VALIDATION]:
        if path.exists():
            shutil.copy2(path, QUARANTINE / path.name)
            shutil.copy2(path, BRANCH_RESIDUALS / path.name)
    shutil.copy2(THEOREM_ATTEMPT, QUEUE / "JR1648_OBSERVED_REDUCED_FLUX_THEOREM_ATTEMPT_NONCLAIM.csv")
    shutil.copy2(COMPONENT_FILL, QUEUE / "JR1648_DELTAH_CURL_COMPONENT_FILL_NONCLAIM.csv")
    shutil.copy2(NEXT_TARGET, QUEUE / "JR1648_NEXT_TARGET_NONCLAIM.csv")


def remove_pycache() -> None:
    pycache = ROOT / "scripts" / "__pycache__"
    if pycache.exists():
        shutil.rmtree(pycache)


def validation_rows() -> list[dict[str, object]]:
    sources = csv_rows(SOURCE_REGISTER)
    theorem = csv_rows(THEOREM_ATTEMPT)
    clauses = csv_rows(CLAUSE_GATE)
    components = csv_rows(COMPONENT_FILL)
    runner = csv_rows(INPUT_RUNNER)
    decisions = csv_rows(DECISION)
    gates = csv_rows(CLAIM_GATE)
    next_targets = csv_rows(NEXT_TARGET)
    checks = [
        (
            "VAL1648_0_sources_exist",
            all(bool_string(row["path_exists"]) == "true" and bool_string(row["needles_found"]) == "true" for row in sources),
            "all cited 1648 source paths exist and needles are present",
        ),
        (
            "VAL1648_1_theorem_contract_written",
            any(row["attempt_id"] == "OFZ1648_1_compact_exterior_no_flux_contract" for row in theorem),
            "observed reduced Ward/no-flux contract is written",
        ),
        (
            "VAL1648_2_zero_not_promoted",
            any(row["attempt_id"] == "OFZ1648_3_current_MTS_verdict" and row["current_status"] == "FAIL_CURRENT_CLAIM" for row in theorem),
            "current MTS verdict keeps observed flux nonzero/nonclaim",
        ),
        (
            "VAL1648_3_clause_gate_complete",
            len(clauses) >= 7 and all(bool_string(row["valid_for_claim"]) == "false" for row in clauses),
            "all observed flux zero clauses are enumerated and nonclaim",
        ),
        (
            "VAL1648_4_component_fill_complete",
            any(row["fill_id"] == "BCF1648_5_total_B_observed" for row in components)
            and all(bool_string(row["valid_for_claim"]) == "false" for row in components),
            "B_obs component fill rows are staged as nonclaim",
        ),
        (
            "VAL1648_5_runner_blocks_without_data",
            runner[0]["computed_status"] == "BLOCKED_MISSING_COMPONENTS" and bool_string(runner[0]["score_allowed"]) == "false",
            "dry-run runner refuses absent component data",
        ),
        (
            "VAL1648_6_no_smuggling_gate",
            any(row["gate_id"] == "CG1648_2_no_smuggling" and row["status"] == "REFUSED" for row in gates),
            "representative zero reuse is refused",
        ),
        (
            "VAL1648_7_next_symbol_match_selected",
            any(row["decision_id"] == "DEC1648_3_next_symbol_match" for row in decisions),
            "reduced GK symbol match selected next",
        ),
        (
            "VAL1648_8_claim_gates_safe",
            any(row["gate_id"] == "CG1648_4_guardrail" and row["status"] == "PASS_AS_INTERNAL_GUARDRAIL_ONLY" for row in gates)
            and all(bool_string(row["claim_allowed"]) == "false" for row in gates),
            "all claim gates keep MTS claims false",
        ),
        (
            "VAL1648_9_next_target_selected",
            next_targets[0]["next_target"] == "1649-Y5-R2FR-reduced-GK-symbol-match-or-observed-boundary-flux-input-runner.md",
            "next target selects reduced GK symbol match",
        ),
        (
            "VAL1648_10_csv_parse",
            all(len(csv_rows(path)) > 0 for path in GENERATED),
            "all generated 1648 CSVs parse",
        ),
        (
            "VAL1648_11_no_mts_claim_flags",
            all_claim_flags_false(CLAIM_CHECKED),
            "all 1648 generated rows keep MTS claim/no-score flags false",
        ),
        (
            "VAL1648_12_branch_copies",
            all((QUARANTINE / path.name).exists() and (BRANCH_RESIDUALS / path.name).exists() for path in GENERATED),
            "branch/quarantine copies exist",
        ),
        (
            "VAL1648_13_queue_copies",
            all(
                path.exists()
                for path in [
                    QUEUE / "JR1648_OBSERVED_REDUCED_FLUX_THEOREM_ATTEMPT_NONCLAIM.csv",
                    QUEUE / "JR1648_DELTAH_CURL_COMPONENT_FILL_NONCLAIM.csv",
                    QUEUE / "JR1648_NEXT_TARGET_NONCLAIM.csv",
                ]
            ),
            "acquisition queue nonclaim copies exist",
        ),
        (
            "VAL1648_14_pycache_absent",
            not (ROOT / "scripts" / "__pycache__").exists(),
            "scripts __pycache__ absent",
        ),
        (
            "VAL1648_15_formalization_untouched",
            not any(FORMALIZATION.rglob("*1648*")) if FORMALIZATION.exists() else True,
            "no 1648 outputs found under formalization-workbench",
        ),
    ]
    overall = all(result for _, result, _ in checks)
    rows = [
        {
            "check_id": check_id,
            "result": "PASS" if result else "FAIL",
            "detail": detail,
            "valid_for_mts_claim": False,
            "claim_allowed": False,
        }
        for check_id, result, detail in checks
    ]
    rows.append(
        {
            "check_id": "VAL1648_OVERALL",
            "result": "PASS" if overall else "FAIL",
            "detail": "1648 observed reduced boundary/source flux and deltaH curl component validation",
            "valid_for_mts_claim": False,
            "claim_allowed": False,
        }
    )
    return rows


def markdown_table(rows: list[dict[str, object]], columns: list[str]) -> str:
    header = "| " + " | ".join(columns) + " |"
    separator = "| " + " | ".join("---" for _ in columns) + " |"
    body = []
    for row in rows:
        cells = [str(row.get(column, "")).replace("\n", " ").replace("|", "/") for column in columns]
        body.append("| " + " | ".join(cells) + " |")
    return "\n".join([header, separator, *body])


def write_doc() -> None:
    sources = csv_rows(SOURCE_REGISTER)
    theorem = csv_rows(THEOREM_ATTEMPT)
    clauses = csv_rows(CLAUSE_GATE)
    components = csv_rows(COMPONENT_FILL)
    runner = csv_rows(INPUT_RUNNER)
    decisions = csv_rows(DECISION)
    gates = csv_rows(CLAIM_GATE)
    next_targets = csv_rows(NEXT_TARGET)
    validation = csv_rows(VALIDATION)
    content = f"""# 1648 - Observed Reduced Boundary Source Flux Zero Or deltaH Curl Component Fill

**Private status:** nonclaim checkpoint. No observed reduced flux zero, `delta_H_tau` zero, stable Hamiltonian charge, `M_H_ref`, `M_*`, PPN pass, local-GR pass, Newton pass, R10 pass, WEP pass, clock pass, or orbital pass is claimed.

## Verdict

The reduced Ward/no-flux theorem is now the clean route:

```text
q_loc^nu = P_loc nabla_mu T_GK^{{mu nu}}
         = P_loc(sum_A E_A nabla^nu Phi_A + B_obs^nu)

B_obs^nu = B_GK^nu + B_corner^nu + B_source_measure^nu + B_projector^nu
```

If `S_red` is parent-owned, `Gamma_eff/K_hat/P_loc` are the actual reduced variational objects, reduced fields are on shell, and observed boundary/source/projector terms are fixed/exact/silent, then `B_observed_reduced_flux_over_MH` can vanish.

Current MTS does **not** yet satisfy those clauses. So `B_observed_reduced_flux_over_MH` remains a live `delta_H_tau` curl component, and representative proper-boundary zeros are not allowed to erase it.

## Source Register

{markdown_table(sources, ["source_id", "path", "path_exists", "needles_found", "role"])}

## Observed Reduced Flux Theorem Attempt

{markdown_table(theorem, ["attempt_id", "target", "identity", "current_status", "why_not_zero"])}

## Clause Gate

{markdown_table(clauses, ["clause_id", "required_clause", "would_kill", "current_status", "failure_if_missing"])}

## deltaH Curl Component Fill

{markdown_table(components, ["fill_id", "quantity", "definition", "current_status", "claim_gate"])}

## Bobs Input Runner Dry Run

{markdown_table(runner, ["run_id", "quantity", "input_status", "computed_status", "failure_reasons"])}

## Decisions

{markdown_table(decisions, ["decision_id", "decision", "reason", "effect"])}

## Claim Gates

{markdown_table(gates, ["gate_id", "claim", "gate_pass", "status", "blocker"])}

## Next Target

{markdown_table(next_targets, ["next_target", "script", "objective", "success_condition"])}

## Validation

{markdown_table(validation, ["check_id", "result", "detail"])}
"""
    DOC.write_text(content, encoding="utf-8")


def main() -> None:
    ensure_dirs()
    outputs = {
        SOURCE_REGISTER: source_register_rows(),
        THEOREM_ATTEMPT: theorem_attempt_rows(),
        CLAUSE_GATE: clause_gate_rows(),
        COMPONENT_FILL: component_fill_rows(),
        INPUT_RUNNER: input_runner_rows(),
        DECISION: decision_rows(),
        CLAIM_GATE: claim_gate_rows(),
        NEXT_TARGET: next_target_rows(),
    }
    for path, rows in outputs.items():
        write_csv(path, rows)
    copy_outputs()
    remove_pycache()
    write_csv(VALIDATION, validation_rows())
    copy_outputs()
    write_doc()
    remove_pycache()
    print(f"wrote {rel(DOC)}")
    print(f"validation {rel(VALIDATION)}")


if __name__ == "__main__":
    main()

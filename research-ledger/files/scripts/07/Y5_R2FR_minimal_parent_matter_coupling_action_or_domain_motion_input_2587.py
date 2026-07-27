from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
PROJECT = ROOT.parent
OUT = ROOT / "source-intake" / "mts_residuals"
QUEUE = ROOT / "source-intake" / "rab-sector" / "acquisition-queue"
LOCAL_BOUNDS = ROOT / "source-intake" / "local_bounds"
FORMALIZATION = PROJECT / "formalization-workbench"

BRANCH_ID = "MTS_R2FR_MIN_PARENT_MATTER_COUPLING_2587"
CHECKPOINT_ID = "2587"

DOC = ROOT / "2587-Y5-R2FR-minimal-parent-matter-coupling-action-or-domain-motion-input.md"

OUTPUTS = {
    "source_register": OUT / "P8_Y5_MIN_PARENT_MATTER_2587_SOURCE_REGISTER.csv",
    "action_contract": OUT / "P8_Y5_MIN_PARENT_MATTER_2587_ACTION_CONTRACT.csv",
    "adoption_gate": OUT / "P8_Y5_MIN_PARENT_MATTER_2587_ADOPTION_GATE.csv",
    "countermodel_tests": OUT / "P8_Y5_MIN_PARENT_MATTER_2587_COUNTERMODEL_TESTS.csv",
    "domain_rows": OUT / "P8_Y5_MIN_PARENT_MATTER_2587_DOMAIN_MOTION_ROWS.csv",
    "runner_refusal": OUT / "P8_Y5_MIN_PARENT_MATTER_2587_RUNNER_REFUSAL.csv",
    "claim_gates": OUT / "P8_Y5_MIN_PARENT_MATTER_2587_CLAIM_GATES.csv",
    "decision_ledger": OUT / "P8_Y5_MIN_PARENT_MATTER_2587_DECISION_LEDGER.csv",
    "next_target": OUT / "P8_Y5_MIN_PARENT_MATTER_2587_NEXT_TARGET.csv",
    "branch_copies": OUT / "P8_Y5_MIN_PARENT_MATTER_2587_BRANCH_COPIES.csv",
    "validation": OUT / "P8_Y5_BRR545_2587_VALIDATION.csv",
}

COPY_TARGETS = {
    "action_contract": QUEUE / "JR2587_MIN_PARENT_MATTER_ACTION_CONTRACT_NONCLAIM.csv",
    "adoption_gate": QUEUE / "JR2587_PARENT_ACTION_ADOPTION_GATE_NONCLAIM.csv",
    "domain_rows": LOCAL_BOUNDS / "Minimal_parent_matter_domain_rows_2587_NONCLAIM.csv",
    "next_target": QUEUE / "JR2587_OBSERVED_STACK_Q_EOBS_TAU_NEXT.csv",
}


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def with_stamp(row: dict[str, Any]) -> dict[str, Any]:
    return {
        "timestamp_utc": utc_now(),
        "branch_id": BRANCH_ID,
        "checkpoint_id": CHECKPOINT_ID,
        **row,
    }


def row_value(value: Any) -> str:
    if isinstance(value, bool):
        return "true" if value else "false"
    if isinstance(value, Path):
        return str(value)
    if isinstance(value, (list, tuple)):
        return ";".join(str(item) for item in value)
    if value is None:
        return ""
    return str(value)


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        raise ValueError(f"cannot write empty CSV: {path}")
    fields: list[str] = []
    for row in rows:
        for key in row:
            if key not in fields:
                fields.append(key)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        for row in rows:
            writer.writerow({field: row_value(row.get(field, "")) for field in fields})


def csv_parses(path: Path) -> tuple[bool, int, str]:
    try:
        with path.open("r", newline="", encoding="utf-8") as handle:
            rows = list(csv.DictReader(handle))
        return bool(rows), len(rows), ""
    except Exception as exc:  # pragma: no cover - validation reports the error.
        return False, 0, str(exc)


def path_has_needles(path: Path, needles: list[str]) -> list[str]:
    if not path.exists():
        return needles
    text = path.read_text(encoding="utf-8", errors="replace")
    return [needle for needle in needles if needle not in text]


def source_register_rows() -> list[dict[str, Any]]:
    source_specs = [
        {
            "source_id": "SRC2587_00_2586_handoff",
            "source_path": ROOT / "2586-Y5-R2FR-source-worldtube-current-complex-owner-or-Jdomain-bound-fill.md",
            "needles": ["NEXT2586_0_selected", "HCC2586_0_primary_current", "VAL2586_OVERALL"],
            "role": "active handoff selecting minimal parent matter-coupling action",
        },
        {
            "source_id": "SRC2587_01_2526_prior_action",
            "source_path": ROOT / "2526-Y5-R2FR-minimal-parent-matter-coupling-action-or-domain-motion-input.md",
            "needles": ["MCA2526_2_minimal_matter_terms", "MCA2526_7_current_verdict", "VAL2526_OVERALL"],
            "role": "prior minimal parent matter-coupling candidate and verdict",
        },
        {
            "source_id": "SRC2587_02_2389_current_density",
            "source_path": ROOT / "2389-Y5-R2FR-parent-matter-action-current-density-or-JH-owner-leak-values.md",
            "needles": ["MCD2389_1_coframe_variation", "MCD2389_5_verdict", "VAL2389_OVERALL"],
            "role": "observed-frame matter-current density grammar and ownership blockers",
        },
        {
            "source_id": "SRC2587_03_2557_conservation",
            "source_path": ROOT / "2557-Y5-R2FR-Hilbert-current-conservation-scale-and-clock-compatibility-gate.md",
            "needles": ["DIV2557_1_full_product_rule", "SCL2557_5_current_status", "VAL2557_OVERALL"],
            "role": "Hilbert-current divergence, tau leak, and ell_J scale blockers",
        },
        {
            "source_id": "SRC2587_04_2467_conservation",
            "source_path": ROOT / "2467-Y5-R2FR-Hilbert-current-conservation-scale-and-clock-compatibility-gate.md",
            "needles": ["DIV2467_1_full_divergence", "SCL2467_5_current_status", "VAL2467_OVERALL"],
            "role": "earlier Hilbert-current conservation/scale gate",
        },
        {
            "source_id": "SRC2587_05_2586_contract",
            "source_path": QUEUE / "JR2586_HILBERT_CURRENT_CONTRACT_NONCLAIM.csv",
            "needles": ["HCC2586_0_primary_current", "REJECTED_AS_DERIVATION"],
            "role": "current Hilbert source contract and fitted-GM rejection",
        },
        {
            "source_id": "SRC2587_06_2586_domain_rows",
            "source_path": LOCAL_BOUNDS / "Source_worldtube_Jdomain_bound_rows_2586_NONCLAIM.csv",
            "needles": ["JD2586_0_current_descent", "JD2586_TOTAL"],
            "role": "current source-worldtube/domain residual rows",
        },
        {
            "source_id": "SRC2587_07_2586_validation",
            "source_path": OUT / "P8_Y5_BRR545_2586_VALIDATION.csv",
            "needles": ["VAL2586_OVERALL", "PASS"],
            "role": "previous checkpoint validation",
        },
    ]
    rows: list[dict[str, Any]] = []
    for source in source_specs:
        source_path = source["source_path"]
        missing_needles = path_has_needles(source_path, source["needles"])
        rows.append(
            with_stamp(
                {
                    "source_id": source["source_id"],
                    "source_path": source_path,
                    "exists": source_path.exists(),
                    "missing_needles": missing_needles,
                    "source_pass": source_path.exists() and not missing_needles,
                    "role": source["role"],
                }
            )
        )
    return rows


def action_contract_rows() -> list[dict[str, Any]]:
    rows = [
        {
            "clause_id": "MCA2587_0_parent_split",
            "clause": "minimal parent split",
            "formal_statement": "S_parent[Phi,psi]=S_geom[Phi]+sum_A S_A[psi_A;q(Phi),theta_A]+S_boundary[q(Phi)]",
            "conditional_gain": "keeps matter coupled through a quotient-owned observed stack rather than fitted source slots",
            "current_status": "CANDIDATE_FORM_WRITTEN_NOT_PARENT_DERIVED",
            "missing_for_claim": "parent action adoption certificate from MTS core variables",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "clause_id": "MCA2587_1_observed_stack",
            "clause": "single observed matter stack",
            "formal_statement": "e_obs=e_obs(q(Phi)), D_obs=D_obs(q(Phi)), A_obs=A_obs(q(Phi)), tau=tau(q(Phi)), ell_J=ell_J(q(Phi))",
            "conditional_gain": "one stack controls matter, clocks, rods, source current and orbital readout",
            "current_status": "REQUIRED_NOT_PARENT_SIGNED",
            "missing_for_claim": "q/e_obs/tau/ell_J ownership and same-frame lock",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "clause_id": "MCA2587_2_minimal_matter_terms",
            "clause": "ordinary matter Lagrangian",
            "formal_statement": "S_A=int mu_obs(qPhi) L_A(psi_A,D_obs(qPhi)psi_A,e_obs(qPhi),A_obs(qPhi),theta_A)",
            "conditional_gain": "gives S_matter=Sbar_matter[q(Phi),psi,theta] and conditionally signs matter-current descent",
            "current_status": "CONDITIONAL_CONTRACT_ONLY",
            "missing_for_claim": "derivation that this is the unique MTS matter grammar",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "clause_id": "MCA2587_3_no_source_only_slot",
            "clause": "forbid source-only couplings",
            "formal_statement": "no w_A(X)S_A, no c_A(X)J_A rescaling, no source/domain marker in L_A, no shadow conformal/disformal source frame before variation",
            "conditional_gain": "kills species/source-current/source-marker countermodels if parent-adopted",
            "current_status": "CONDITIONALLY_SIGNED_BY_CANDIDATE_ONLY",
            "missing_for_claim": "object-language uniqueness or no-Hom/no-extra-slot proof",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "clause_id": "MCA2587_4_variation_before_readout",
            "clause": "variation order",
            "formal_statement": "T_H and J_H[tau] are functional derivatives of S_parent before material projection, support fitting, orbital calibration or arena readout",
            "conditional_gain": "blocks post-variation source-mask manufacture",
            "current_status": "CONDITIONAL_WORKFLOW_CONTRACT",
            "missing_for_claim": "parent workflow/readout-order theorem",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "clause_id": "MCA2587_5_boundary_support_silence",
            "clause": "boundary and support terms cannot carry hidden source mass",
            "formal_statement": "delta S_boundary and support/jump terms are fixed before readout and cannot absorb GM, ell_J, tau or source-domain shifts",
            "conditional_gain": "prevents boundary bookkeeping from becoming measured-GM calibration",
            "current_status": "MISSING_BOUNDARY_SUPPORT_ZERO_OR_BOUND",
            "missing_for_claim": "jump ledger, compact support theorem and fixed reference/no-flux certificate",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "clause_id": "MCA2587_6_descent_output",
            "clause": "conditional source-current descent theorem",
            "formal_statement": "if MCA2587_0..5 and q/v verticality hold, then delta_v S_matter=0 modulo Euler/gauge/boundary and J_H=q^*Jbar_H",
            "conditional_gain": "would sign the coupling side of 2586 source-current descent",
            "current_status": "EXACT_CONDITIONAL_OUTPUT",
            "missing_for_claim": "q/e_obs/tau/ell_J and action-adoption antecedents",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "clause_id": "MCA2587_7_current_verdict",
            "clause": "current MTS adoption status",
            "formal_statement": "no cited source derives MCA2587 as the unique parent matter coupling from MTS core variables",
            "conditional_gain": "disciplined ansatz is retained without promotion",
            "current_status": "MINIMAL_PARENT_MATTER_ACTION_NOT_DERIVED_CURRENT_CORPUS",
            "missing_for_claim": "source-backed adoption from MTS core and observed-stack ownership",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]
    return [with_stamp(row) for row in rows]


def adoption_gate_rows() -> list[dict[str, Any]]:
    rows = [
        {
            "gate_id": "AD2587_0_action_adoption",
            "required_signature": "MTS core derives or explicitly adopts MCA2587",
            "evidence_needed": "source path showing S_parent matter sector and why no other source slot is allowed",
            "current_status": "MISSING_ACTION_ADOPTION_CERTIFICATE",
            "blocks": "turning contract into theorem",
            "gate_pass": False,
            "valid_for_claim": False,
        },
        {
            "gate_id": "AD2587_1_q_object",
            "required_signature": "q(Phi) object is parent-owned and defined on an open local branch",
            "evidence_needed": "q map, Dq, vertical basis and source stack domain",
            "current_status": "MISSING_Q_STACK_OWNER",
            "blocks": "S_matter=Sbar[q(Phi),psi] descent",
            "gate_pass": False,
            "valid_for_claim": False,
        },
        {
            "gate_id": "AD2587_2_eobs_tau",
            "required_signature": "e_obs(q) and tau(q) are the same parent-owned frame used by clocks, source current and readout",
            "evidence_needed": "observed coframe pullback and tau selector theorem",
            "current_status": "MISSING_EOBS_TAU_SAME_FRAME_LOCK",
            "blocks": "same source current for GR/Newton/clock/orbital tests",
            "gate_pass": False,
            "valid_for_claim": False,
        },
        {
            "gate_id": "AD2587_3_ellJ",
            "required_signature": "ell_J is fixed by parent action, not empirical GM",
            "evidence_needed": "action normalization, spectrum/gap, or universal parent length source",
            "current_status": "MISSING_PARENT_ELLJ_SCALE",
            "blocks": "source-current normalization and q_loc amplitude",
            "gate_pass": False,
            "valid_for_claim": False,
        },
        {
            "gate_id": "AD2587_4_no_source_slot",
            "required_signature": "no direct source-only/material marker slots exist",
            "evidence_needed": "grammar/representation proof excluding w_A(X), c_A(X), source masks and shadow frames",
            "current_status": "CONTRACT_ONLY_NOT_UNIQUENESS_PROOF",
            "blocks": "WEP/source-normalization countermodels",
            "gate_pass": False,
            "valid_for_claim": False,
        },
        {
            "gate_id": "AD2587_5_boundary_support",
            "required_signature": "boundary/support/jump terms are zero or source-backed bounded",
            "evidence_needed": "compact-support, jump and fixed-reference no-flux ledger",
            "current_status": "MISSING_BOUNDARY_SUPPORT_LEDGER",
            "blocks": "domain-motion fallback rows",
            "gate_pass": False,
            "valid_for_claim": False,
        },
    ]
    return [with_stamp(row) for row in rows]


def countermodel_rows() -> list[dict[str, Any]]:
    rows = [
        {
            "test_id": "CMT2587_0_species_weight",
            "countermodel": "S_matter -> sum_A w_A(X) S_A",
            "candidate_response": "forbidden by no-source-only slot",
            "current_result": "EXCLUDED_IF_CANDIDATE_PARENT_ADOPTED_NOT_BY_CURRENT_CORPUS",
            "residual_if_allowed": "J_species_source_charge",
            "claim_allowed": False,
        },
        {
            "test_id": "CMT2587_1_current_rescale",
            "countermodel": "J_H -> c_A(X) J_H or ell_J depends on source class",
            "candidate_response": "forbidden by fixed ell_J and no current rescaling",
            "current_result": "EXCLUDED_IF_CANDIDATE_PARENT_ADOPTED_NOT_BY_CURRENT_CORPUS",
            "residual_if_allowed": "E_ellJ_scale;eta_source_AB",
            "claim_allowed": False,
        },
        {
            "test_id": "CMT2587_2_shadow_frame",
            "countermodel": "ordinary matter sees source-dependent conformal/disformal shadow frame",
            "candidate_response": "forbidden by single observed stack",
            "current_result": "EXCLUDED_IF_CANDIDATE_PARENT_ADOPTED_NOT_BY_CURRENT_CORPUS",
            "residual_if_allowed": "Delta_frame_source",
            "claim_allowed": False,
        },
        {
            "test_id": "CMT2587_3_post_variation_selector",
            "countermodel": "material/readout projection changes source current after variation",
            "candidate_response": "forbidden by variation-before-readout",
            "current_result": "EXCLUDED_IF_CANDIDATE_PARENT_ADOPTED_NOT_BY_CURRENT_CORPUS",
            "residual_if_allowed": "E_domain_motion;J_readout_selector",
            "claim_allowed": False,
        },
        {
            "test_id": "CMT2587_4_q_missing",
            "countermodel": "candidate uses q stack that is not derived from parent variables",
            "candidate_response": "not solved by matter coupling alone",
            "current_result": "RETAINED_AS_NEXT_OBSERVED_STACK_GATE",
            "residual_if_allowed": "Dq_vertical_leak;epsilon_q_owner",
            "claim_allowed": False,
        },
    ]
    return [with_stamp(row) for row in rows]


def domain_rows() -> list[dict[str, Any]]:
    rows = [
        {
            "row_id": "DM2587_0_action_adoption",
            "symbol": "E_action_adoption",
            "definition": "failure of current MTS core to derive/adopt the minimal parent matter action",
            "needed_for_claim": "source-backed parent action clause or adoption certificate",
            "current_status": "MISSING_ACTION_ADOPTION_CERTIFICATE",
            "units": "dimensionless_gate_or_action_norm",
            "observable_link": "source_current_descent;Newton;local_GR",
            "numeric_value": "MISSING_NUMERIC_VALUE",
            "source_path": "MISSING_SOURCE_PATH",
            "score_ready": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "row_id": "DM2587_1_q_stack",
            "symbol": "epsilon_q_stack",
            "definition": "q/e_obs observed-stack ownership leak",
            "needed_for_claim": "q object and e_obs(q) same-frame theorem",
            "current_status": "MISSING_Q_EOBS_OWNER_OR_BOUND",
            "units": "dimensionless",
            "observable_link": "frame_source;source_normalization;PPN;clock",
            "numeric_value": "MISSING_NUMERIC_VALUE",
            "source_path": "MISSING_SOURCE_PATH",
            "score_ready": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "row_id": "DM2587_2_tau_ellJ",
            "symbol": "epsilon_tau_ellJ",
            "definition": "tau selector and ell_J parent-scale mismatch",
            "needed_for_claim": "same-frame tau plus parent ell_J scale theorem or finite drift bounds",
            "current_status": "MISSING_TAU_ELLJ_OWNER_OR_BOUND",
            "units": "dimensionless_or_scale_drift",
            "observable_link": "clock;Gdot;orbital;PPN",
            "numeric_value": "MISSING_NUMERIC_VALUE",
            "source_path": "MISSING_SOURCE_PATH",
            "score_ready": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "row_id": "DM2587_3_source_slot",
            "symbol": "epsilon_source_slot",
            "definition": "hidden source-only weights, current rescalings, source masks or marker matter lift",
            "needed_for_claim": "no-source-slot uniqueness theorem or finite hidden-slot bound",
            "current_status": "MISSING_NO_SOURCE_SLOT_PROOF_OR_BOUND",
            "units": "dimensionless",
            "observable_link": "WEP;R11;source_normalization",
            "numeric_value": "MISSING_NUMERIC_VALUE",
            "source_path": "MISSING_SOURCE_PATH",
            "score_ready": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "row_id": "DM2587_4_boundary_support",
            "symbol": "epsilon_boundary_support",
            "definition": "boundary/support/jump term in matter variation that can alter source current",
            "needed_for_claim": "fixed support/no-flux theorem or source-backed jump ledger",
            "current_status": "MISSING_BOUNDARY_SUPPORT_ZERO_OR_BOUND",
            "units": "GM_flux_or_dimensionless_after_MHref",
            "observable_link": "Newton;R10;R11;orbital",
            "numeric_value": "MISSING_NUMERIC_VALUE",
            "source_path": "MISSING_SOURCE_PATH",
            "score_ready": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "row_id": "DM2587_TOTAL",
            "symbol": "E_matter_action",
            "definition": "absolute no-cancellation parent matter-action adoption/source-current descent obstruction",
            "needed_for_claim": "all action/observed-stack/tau/ellJ/source-slot/support components theorem-zero or source-backed finite",
            "current_status": "TOTAL_PARENT_MATTER_ACTION_RETAINED_NONCLAIM",
            "units": "dimensionless_after_common_source_normalization",
            "observable_link": "J_domain;PiM_chainmap;Newton;PPN;R10;R11;local_GR",
            "numeric_value": "MISSING_COMPONENT_VALUES",
            "source_path": "THIS_CHECKPOINT_SYMBOLIC_LEDGER_ONLY",
            "score_ready": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]
    return [with_stamp(row) for row in rows]


def runner_refusal_rows(rows_in: list[dict[str, Any]]) -> list[dict[str, Any]]:
    rows = []
    for row in rows_in:
        rows.append(
            with_stamp(
                {
                    "runner_id": f"DMR2587_{row['row_id']}",
                    "target_id": row["row_id"],
                    "symbol": row["symbol"],
                    "verdict": "REFUSED_CLAIM_RETAINED_UNFILLED",
                    "failure_reasons": "MISSING_ZERO_THEOREM_OR_NUMERIC_VALUE;MISSING_SOURCE_PATH;VALID_FOR_CLAIM_FALSE",
                    "score_ready": False,
                    "claim_allowed": False,
                }
            )
        )
    return rows


def claim_gate_rows() -> list[dict[str, Any]]:
    rows = [
        {
            "gate_id": "CG2587_0_candidate_written",
            "claim": "minimal parent matter-coupling action contract is written",
            "gate_status": "PASS_NONCLAIM",
            "reason": "single observed stack and no-source-slot grammar are explicit",
            "gate_pass": True,
            "claim_allowed": False,
        },
        {
            "gate_id": "CG2587_1_action_derived",
            "claim": "MCA2587 is derived/adopted by current MTS core",
            "gate_status": "BLOCKED_NONCLAIM",
            "reason": "no parent action adoption certificate or uniqueness proof exists",
            "gate_pass": False,
            "claim_allowed": False,
        },
        {
            "gate_id": "CG2587_2_source_current_descent",
            "claim": "J_H=q^*Jbar_H and J_v^matter=0 for current MTS",
            "gate_status": "BLOCKED_NONCLAIM",
            "reason": "q/e_obs/tau/ell_J ownership and q/v verticality remain unsigned",
            "gate_pass": False,
            "claim_allowed": False,
        },
        {
            "gate_id": "CG2587_3_domain_rows_score",
            "claim": "domain-motion/source-current rows are score-ready",
            "gate_status": "BLOCKED_NONCLAIM",
            "reason": "rows lack numeric values, source paths, units normalization and common denominator",
            "gate_pass": False,
            "claim_allowed": False,
        },
        {
            "gate_id": "CG2587_4_Newton_local_GR",
            "claim": "Newton/local-GR source bridge is derived",
            "gate_status": "BLOCKED_NONCLAIM",
            "reason": "matter coupling is a disciplined contract, not yet a parent theorem",
            "gate_pass": False,
            "claim_allowed": False,
        },
    ]
    return [with_stamp(row) for row in rows]


def decision_rows() -> list[dict[str, Any]]:
    rows = [
        {
            "decision_id": "DEC2587_0_contract_status",
            "decision": "RETAIN_MINIMAL_MATTER_ACTION_AS_LEAST_SCRUTINY_CONTRACT",
            "reason": "standard single observed-stack coupling is the cleanest route and blocks source-only loopholes if parent-adopted",
            "effect": "use MCA2587 as a contract, not a theorem",
        },
        {
            "decision_id": "DEC2587_1_no_promotion",
            "decision": "DO_NOT_PROMOTE_SOURCE_CURRENT_DESCENT",
            "reason": "q/e_obs/tau/ell_J, action adoption, variation order, support and no-source-slot uniqueness remain unsigned",
            "effect": "Newton/local-GR/source-normalization claims stay blocked",
        },
        {
            "decision_id": "DEC2587_2_next",
            "decision": "OBSERVED_STACK_Q_EOBS_TAU_SELECTED_NEXT",
            "reason": "the minimal action contract cannot sign J_H descent until the observed stack q/e_obs/tau/ell_J is parent-owned",
            "effect": "2588 should derive observed-stack ownership or fill q/frame/tau/source leak rows",
        },
    ]
    return [with_stamp(row) for row in rows]


def next_target_rows() -> list[dict[str, Any]]:
    rows = [
        {
            "route_id": "NEXT2587_0_selected",
            "selection_status": "selected",
            "target_file": "2588-Y5-R2FR-observed-stack-q-eobs-tau-parent-owner-or-source-leak-fill.md",
            "target_script": "scripts/Y5_R2FR_observed_stack_q_eobs_tau_parent_owner_or_source_leak_fill_2588.py",
            "task": "derive a single parent-owned observed stack q(Phi), e_obs(q), tau(q), and ell_J(q) used by matter, clocks, rods, orbital readout and Hilbert source charge, or fill q/frame/tau/ellJ leak rows with units and source paths",
            "acceptance_target": "observed-stack ownership signs the antecedent for MCA2587 and J_H=q^*Jbar_H, or epsilon_q_stack/Delta_frame_source/epsilon_tau_ellJ remain source-ready nonclaim residual rows",
            "guardrails": "no standard-GR minimal-coupling import as MTS proof; no fitted GM; no post-readout frame or tau; no source-only slot; no Newton/local-GR claim; no GitHub; no formalization-workbench edits",
        }
    ]
    return [with_stamp(row) for row in rows]


def copy_branch_outputs() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for copy_id, target_path in COPY_TARGETS.items():
        source_path = OUTPUTS[copy_id]
        target_path.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(source_path, target_path)
        rows.append(
            with_stamp(
                {
                    "copy_id": f"COPY2587_{copy_id}",
                    "source_path": source_path,
                    "target_path": target_path,
                    "source_exists": source_path.exists(),
                    "target_exists": target_path.exists(),
                }
            )
        )
    return rows


def validation_rows(data: dict[str, list[dict[str, Any]]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []

    def add(check_id: str, condition: bool, notes: str, detail: str = "") -> None:
        rows.append(
            with_stamp(
                {
                    "check_id": check_id,
                    "status": "PASS" if condition else "FAIL",
                    "notes": notes,
                    "detail": detail,
                }
            )
        )

    add("VAL2587_00_sources_exist", all(row["source_pass"] is True for row in data["sources"]), "all cited local source paths exist and needles are present")
    add(
        "VAL2587_01_candidate_written",
        any(row["clause_id"] == "MCA2587_2_minimal_matter_terms" for row in data["action_contract"]),
        "minimal parent matter action contract is written",
    )
    add(
        "VAL2587_02_current_verdict_blocked",
        any(row["clause_id"] == "MCA2587_7_current_verdict" and row["valid_for_claim"] is False for row in data["action_contract"]),
        "current corpus action adoption remains blocked",
    )
    add(
        "VAL2587_03_adoption_gates_blocked",
        all(row["gate_pass"] is False and row["valid_for_claim"] is False for row in data["adoption_gate"]),
        "all parent action adoption gates remain blocked",
    )
    add(
        "VAL2587_04_no_source_slot_guardrails",
        any(row["test_id"] == "CMT2587_0_species_weight" for row in data["countermodels"])
        and all(row["claim_allowed"] is False for row in data["countermodels"]),
        "source-only countermodels are rejected as derivation",
    )
    add(
        "VAL2587_05_domain_rows_nonclaim",
        all(row["score_ready"] is False and row["valid_for_claim"] is False and row["claim_allowed"] is False for row in data["domain_rows"]),
        "domain/action residual rows remain nonclaim",
    )
    add(
        "VAL2587_06_runner_refuses",
        all(row["score_ready"] is False and row["claim_allowed"] is False for row in data["runner_refusal"]),
        "runner refuses unfilled domain/action rows",
    )
    add(
        "VAL2587_07_claim_gates_safe",
        all(row["claim_allowed"] is False for row in data["claim_gates"]),
        "no source-current, Newton or local-GR claim is allowed",
    )
    add(
        "VAL2587_08_next_target_written",
        any(row["route_id"] == "NEXT2587_0_selected" for row in data["next"]),
        "2588 observed-stack owner target selected",
    )
    add(
        "VAL2587_09_branch_copies",
        all(row["source_exists"] is True and row["target_exists"] is True for row in data["copies"]),
        "nonclaim branch copies exist",
    )

    formalization_artifacts = []
    if FORMALIZATION.exists():
        for pattern in (
            "*2587-Y5-R2FR-minimal-parent-matter*",
            "*Y5_R2FR_minimal_parent_matter_coupling*",
            "*P8_Y5_MIN_PARENT_MATTER_2587*",
            "*JR2587*",
        ):
            formalization_artifacts.extend(FORMALIZATION.rglob(pattern))
    add(
        "VAL2587_10_no_formalization_artifacts",
        not formalization_artifacts,
        "no 2587 artifacts were written to formalization-workbench",
        ";".join(str(path) for path in formalization_artifacts),
    )

    for key, path in OUTPUTS.items():
        if key == "validation":
            continue
        parsed, count, error = csv_parses(path)
        add(f"VAL2587_CSV_{path.stem}", parsed and count > 0, f"CSV parses with {count} rows", error)
    for key, path in COPY_TARGETS.items():
        parsed, count, error = csv_parses(path)
        add(f"VAL2587_COPY_CSV_{key}", parsed and count > 0, f"copy CSV parses with {count} rows", error)

    overall = all(row["status"] == "PASS" for row in rows)
    add(
        "VAL2587_OVERALL",
        overall,
        "2587 writes the minimal parent matter-coupling action contract, keeps current MTS nonclaim, stages domain/action rows, and selects observed-stack ownership next",
    )
    return rows


def markdown_table(rows: list[dict[str, Any]], columns: list[str]) -> str:
    header = "| " + " | ".join(columns) + " |"
    separator = "| " + " | ".join("---" for _ in columns) + " |"
    lines = [header, separator]
    for row in rows:
        values = [row_value(row.get(column, "")).replace("\n", " ") for column in columns]
        lines.append("| " + " | ".join(values) + " |")
    return "\n".join(lines)


def write_doc(data: dict[str, list[dict[str, Any]]]) -> None:
    sections = [
        "# 2587 Y5 R2FR minimal parent matter-coupling action or domain-motion input",
        "",
        "**Status:** private nonclaim derivation checkpoint. The minimal single-observed-stack matter action is written as the least-scrutiny contract, but it is not derived from current MTS core variables.",
        "",
        "**Main result:** the best parent matter route is explicit: ordinary matter sees only the quotient-owned observed stack `q(Phi) -> e_obs, D_obs, A_obs, tau, ell_J`, variation happens before readout, and source-only weights/masks/shadow frames are forbidden. If this action were parent-adopted, it would conditionally sign `J_H=q^*Jbar_H`. Current MTS has not yet derived or adopted it, so `E_matter_action` and the domain-motion/source-current rows remain nonclaim.",
        "",
        "## Source Register",
        markdown_table(data["sources"], ["source_id", "source_path", "exists", "missing_needles", "source_pass", "role"]),
        "",
        "## Action Contract",
        markdown_table(data["action_contract"], ["clause_id", "clause", "formal_statement", "conditional_gain", "current_status", "missing_for_claim", "valid_for_claim", "claim_allowed"]),
        "",
        "## Adoption Gate",
        markdown_table(data["adoption_gate"], ["gate_id", "required_signature", "evidence_needed", "current_status", "blocks", "gate_pass", "valid_for_claim"]),
        "",
        "## Countermodel Tests",
        markdown_table(data["countermodels"], ["test_id", "countermodel", "candidate_response", "current_result", "residual_if_allowed", "claim_allowed"]),
        "",
        "## Domain Motion Rows",
        markdown_table(data["domain_rows"], ["row_id", "symbol", "definition", "needed_for_claim", "current_status", "units", "observable_link", "numeric_value", "source_path", "score_ready", "valid_for_claim", "claim_allowed"]),
        "",
        "## Runner Refusal",
        markdown_table(data["runner_refusal"], ["runner_id", "target_id", "symbol", "verdict", "failure_reasons", "score_ready", "claim_allowed"]),
        "",
        "## Claim Gates",
        markdown_table(data["claim_gates"], ["gate_id", "claim", "gate_status", "reason", "gate_pass", "claim_allowed"]),
        "",
        "## Decision Ledger",
        markdown_table(data["decisions"], ["decision_id", "decision", "reason", "effect"]),
        "",
        "## Next Target",
        markdown_table(data["next"], ["route_id", "selection_status", "target_file", "target_script", "task", "acceptance_target", "guardrails"]),
        "",
        "## Branch Copies",
        markdown_table(data["copies"], ["copy_id", "source_path", "target_path", "source_exists", "target_exists"]),
        "",
        "## Validation",
        markdown_table(data["validations"], ["check_id", "status", "notes", "detail"]),
        "",
    ]
    DOC.write_text("\n".join(sections), encoding="utf-8")


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    QUEUE.mkdir(parents=True, exist_ok=True)
    LOCAL_BOUNDS.mkdir(parents=True, exist_ok=True)

    domain_rows_data = domain_rows()
    data = {
        "sources": source_register_rows(),
        "action_contract": action_contract_rows(),
        "adoption_gate": adoption_gate_rows(),
        "countermodels": countermodel_rows(),
        "domain_rows": domain_rows_data,
        "runner_refusal": runner_refusal_rows(domain_rows_data),
        "claim_gates": claim_gate_rows(),
        "decisions": decision_rows(),
        "next": next_target_rows(),
    }

    write_csv(OUTPUTS["source_register"], data["sources"])
    write_csv(OUTPUTS["action_contract"], data["action_contract"])
    write_csv(OUTPUTS["adoption_gate"], data["adoption_gate"])
    write_csv(OUTPUTS["countermodel_tests"], data["countermodels"])
    write_csv(OUTPUTS["domain_rows"], data["domain_rows"])
    write_csv(OUTPUTS["runner_refusal"], data["runner_refusal"])
    write_csv(OUTPUTS["claim_gates"], data["claim_gates"])
    write_csv(OUTPUTS["decision_ledger"], data["decisions"])
    write_csv(OUTPUTS["next_target"], data["next"])

    data["copies"] = copy_branch_outputs()
    write_csv(OUTPUTS["branch_copies"], data["copies"])

    data["validations"] = validation_rows(data)
    write_csv(OUTPUTS["validation"], data["validations"])
    write_doc(data)

    overall = next(row for row in data["validations"] if row["check_id"] == "VAL2587_OVERALL")
    print(f"{overall['check_id']} {overall['status']}: {overall['notes']}")
    print(f"doc={DOC}")
    print(f"validation={OUTPUTS['validation']}")


if __name__ == "__main__":
    main()

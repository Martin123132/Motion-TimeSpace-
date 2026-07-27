from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path


CHECKPOINT_ID = "2547"
BRANCH_ID = "MTS_R2FR_FIXED_REFERENCE_SELECTOR_OR_DELTA_REF_ROW_2547"
POST_ROOT = Path(__file__).resolve().parents[1]
PROJECT_ROOT = POST_ROOT.parent
RESIDUALS = POST_ROOT / "source-intake" / "mts_residuals"
DOC_PATH = POST_ROOT / "2547-Y5-R2FR-fixed-reference-selector-or-Delta-ref-row.md"
FORMALIZATION_WORKBENCH = PROJECT_ROOT / "formalization-workbench"

OUTPUTS = {
    "source": RESIDUALS / "P8_Y5_NO_SHADOW_2547_SOURCE_REGISTER.csv",
    "selector": RESIDUALS / "P8_Y5_NO_SHADOW_2547_FIXED_REFERENCE_SELECTOR_THEOREM.csv",
    "contract": RESIDUALS / "P8_Y5_NO_SHADOW_2547_DIRICHLET_ACTION_CONTRACT.csv",
    "signature": RESIDUALS / "P8_Y5_NO_SHADOW_2547_SIGNATURE_AUDIT.csv",
    "bounds": RESIDUALS / "P8_Y5_NO_SHADOW_2547_DELTA_REF_BOUND_ROWS.csv",
    "decision": RESIDUALS / "P8_Y5_NO_SHADOW_2547_DECISION_LEDGER.csv",
    "claims": RESIDUALS / "P8_Y5_NO_SHADOW_2547_CLAIM_GATES.csv",
    "refusal": RESIDUALS / "P8_Y5_NO_SHADOW_2547_REFUSAL_RUNNER.csv",
    "next": RESIDUALS / "P8_Y5_NO_SHADOW_2547_NEXT_TARGET.csv",
    "copies": RESIDUALS / "P8_Y5_NO_SHADOW_2547_BRANCH_COPIES.csv",
    "validation": RESIDUALS / "P8_Y5_BRR545_2547_VALIDATION.csv",
}

BRANCH_COPIES = {
    "selector": POST_ROOT / "source-intake" / "hamiltonian-source" / "Fixed_reference_selector_2547_NONCLAIM.csv",
    "bounds": POST_ROOT / "source-intake" / "local_bounds" / "Delta_ref_bound_rows_2547_NONCLAIM.csv",
    "contract": POST_ROOT / "source-intake" / "rab-sector" / "acquisition-queue" / "JR2547_DIRICHLET_ACTION_CONTRACT_NONCLAIM.csv",
    "next": POST_ROOT / "source-intake" / "rab-sector" / "acquisition-queue" / "SIGNATURE_HUNT2548_NEXT_TARGET_NONCLAIM.csv",
}

SOURCE_SPECS = [
    (
        "SRC2547_00_2546_doc",
        "2546-Y5-R2FR-boundary-term-classification-exact-vs-corner-reference.md",
        ["BTC2546_4_fixed_reference", "NEXT2546_0_selected", "CG2546_5_local_GR_Newton"],
        "immediate handoff selecting fixed-reference selector",
    ),
    (
        "SRC2547_01_2546_validation",
        "source-intake/mts_residuals/P8_Y5_BRR545_2546_VALIDATION.csv",
        ["VAL2546_OVERALL,PASS"],
        "2546 validation anchor",
    ),
    (
        "SRC2547_02_2457_doc",
        "2457-Y5-R2FR-parent-Dirichlet-boundary-action-contract-or-Delta-ref-bound-values.md",
        ["PAC2457_0_parent_fields", "VDT2457_2_chain_rule_to_Bref", "NEXT2457_0_selected"],
        "strongest existing Dirichlet/fixed-boundary reference contract",
    ),
    (
        "SRC2547_03_2457_contract",
        "source-intake/mts_residuals/P8_Y5_PARENT_QLOC_2457_PARENT_ACTION_CONTRACT.csv",
        ["PAC2457_0_parent_fields", "C_D(beta_0)", "PAC2457_5_no_shortcut_guard"],
        "machine-readable parent action contract",
    ),
    (
        "SRC2547_04_2457_variational",
        "source-intake/mts_residuals/P8_Y5_PARENT_QLOC_2457_VARIATIONAL_DOMAIN_THEOREM.csv",
        ["VDT2457_2_chain_rule_to_Bref", "D_a B_ref", "PASS_AS_CONTRACT"],
        "fixed beta_0 implies B_ref q/source silence as conditional theorem",
    ),
    (
        "SRC2547_05_2457_signature",
        "source-intake/mts_residuals/P8_Y5_PARENT_QLOC_2457_CONTRACT_SIGNATURE_AUDIT.csv",
        ["SIG2457_7_denominator", "MISSING_SAME_FRAME_N_E_OR_MHREF", "BLOCKED_NONCLAIM"],
        "current missing signature audit",
    ),
    (
        "SRC2547_06_2457_bounds",
        "source-intake/mts_residuals/P8_Y5_PARENT_QLOC_2457_DELTA_REF_BOUND_VALUE_INPUTS.csv",
        ["BVI2457_4_total_first_bound_value", "NOT_COMPUTED_COMPONENTS_MISSING"],
        "nonclaim Delta_ref bound-value input precedent",
    ),
    (
        "SRC2547_07_2456_dirichlet",
        "source-intake/mts_residuals/P8_Y5_PARENT_QLOC_2456_DIRICHLET_REFERENCE_BRANCH.csv",
        ["DIR2456_3_chain_rule_zero", "FAIL_CURRENT_CLAIM_BUT_ROUTE_IS_SHARPENED"],
        "Dirichlet reference branch precursor",
    ),
    (
        "SRC2547_08_2455_leak_law",
        "source-intake/mts_residuals/P8_Y5_PARENT_QLOC_2455_BOUNDARY_REFERENCE_EMBEDDING_DERIVATION.csv",
        ["EMB2455_1_variation_law", "EMB2455_4_finite_bound"],
        "exact B_ref leak law and finite bound fallback",
    ),
    (
        "SRC2547_09_2453_ift",
        "source-intake/mts_residuals/P8_Y5_PARENT_QLOC_2453_IMPLICIT_FUNCTION_DERIVATION.csv",
        ["IFT2453_4_chain_to_Bref", "D_x B_ref"],
        "implicit-function selector proof route",
    ),
    (
        "SRC2547_10_1771_boundary",
        "1771-Y5-R2FR-sector-action-variation-and-local-scaling-silence-or-operator-bounds.md",
        ["boundary/reference/improvement", "fixed before readout"],
        "older warning that reference terms can fake closure",
    ),
]


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def rel(path: Path) -> str:
    try:
        return path.relative_to(POST_ROOT).as_posix()
    except ValueError:
        return path.as_posix()


def write_csv(path: Path, rows: list[dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        raise ValueError(f"no rows for {path}")
    fields: list[str] = []
    for row in rows:
        for key in row:
            if key not in fields:
                fields.append(key)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        for row in rows:
            writer.writerow({field: row.get(field, "") for field in fields})


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def contains(path: Path, needle: str) -> bool:
    return path.exists() and needle in path.read_text(encoding="utf-8", errors="replace")


def stamp(row: dict[str, object]) -> dict[str, object]:
    return {
        "timestamp_utc": utc_now(),
        "branch_id": BRANCH_ID,
        "checkpoint_id": CHECKPOINT_ID,
        "valid_for_claim": "false",
        "claim_allowed": "false",
        **row,
    }


def no_claim(extra: dict[str, object] | None = None) -> dict[str, object]:
    row: dict[str, object] = {
        "parent_signed": "false",
        "theorem_zero": "false",
        "numeric_prediction_present": "false",
        "same_branch_locked": "false",
        "projection_ready": "false",
        "score_ready": "false",
        "valid_for_claim": "false",
        "claim_allowed": "false",
    }
    if extra:
        row.update(extra)
    return row


def source_register() -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    for source_id, source_path, needles, role in SOURCE_SPECS:
        path = POST_ROOT / source_path
        rows.append(
            stamp(
                {
                    "row_id": source_id,
                    "source_path": str(path),
                    "exists": str(path.exists()).lower(),
                    "needles": "; ".join(needles),
                    "needles_found": str(all(contains(path, needle) for needle in needles)).lower(),
                    "source_role": role,
                }
            )
        )
    return rows


def selector_rows() -> list[dict[str, object]]:
    rows = [
        {
            "row_id": "FRS2547_0_selector_object",
            "step": "fixed reference data object",
            "statement": "Define beta_ref=(S,sigma_AB,tau,C_top,B_ct) as the reference-boundary datum controlled before local q/source/readout variations.",
            "formula": "beta_ref(Phi)|dM = beta_0",
            "result": "the reference problem becomes a boundary-data ownership problem",
            "current_status": "DEFINITION_CONTRACT_NOT_PARENT_SIGNED",
        },
        {
            "row_id": "FRS2547_1_configuration_domain",
            "step": "Dirichlet configuration bundle",
            "statement": "If the parent theory declares C_D(beta_0)={Phi: beta_ref(Phi)|dM=beta_0}, allowed q/source variations are tangent to C_D(beta_0).",
            "formula": "delta_a Phi in T C_D(beta_0) => D_a beta_ref=0 for a in {q,source}",
            "result": "D_a S=D_a sigma_AB=D_a tau=D_a C_top=D_a B_ct=0",
            "current_status": "CONDITIONAL_THEOREM_AS_CONTRACT",
        },
        {
            "row_id": "FRS2547_2_chain_rule_to_Bref",
            "step": "reference silence",
            "statement": "Insert the component zeros into the 2455 leak law.",
            "formula": "D_a B_ref=<dB/dsigma,D_a sigma>+<dB/dtau,D_a tau>+<dB/dC_top,D_a C_top>+D_a B_ct=0",
            "result": "partial_q B_ref=partial_source B_ref=0 without cancellation",
            "current_status": "PASS_AS_CONDITIONAL_CONTRACT",
        },
        {
            "row_id": "FRS2547_3_to_Href_Deltaref",
            "step": "reference Hamiltonian component",
            "statement": "If H_ref is fixed by the same beta_0 and the denominator is same-frame parent-owned, the reference part of Delta_ref is q/source silent.",
            "formula": "D_a Delta_ref=0 if H_ref=H_ref[beta_0], tau_H=tau_source=tau_readout, and M_H_ref>0 is parent-owned",
            "result": "reference residual can vanish only under parent signature plus same-frame denominator",
            "current_status": "BLOCKED_ON_SIGNATURE_AND_MHREF",
        },
        {
            "row_id": "FRS2547_4_no_shortcuts",
            "step": "anti-laundering rule",
            "statement": "Observed GM, fitted mass, readout radius, residual sign, and post-hoc counterterm choices cannot enter beta_0, B_ref, H_ref, or M_H_ref.",
            "formula": "partial_{GM_obs,M_fit,residual,readout} beta_0 = 0 and partial_{same} B_ct = 0",
            "result": "prevents proving Newton/GR by importing Newton/GR",
            "current_status": "GUARDRAIL_DERIVED_NONCLAIM",
        },
        {
            "row_id": "FRS2547_5_verdict",
            "step": "current verdict",
            "statement": "The exact fixed-reference selector contract is written, but the active corpus has not signed its required parent action clauses.",
            "formula": "PAC/SIG signatures missing => Delta_ref=0 not claim-grade",
            "result": "retain Delta_ref bound rows and hunt parent signatures",
            "current_status": "THEOREM_NOT_PROMOTED_RETAIN_DELTA_REF",
        },
    ]
    return [stamp(no_claim(row)) for row in rows]


def contract_rows() -> list[dict[str, object]]:
    rows = [
        ("DAC2547_0_parent_bundle", "Parent configuration bundle declares fixed beta_0.", "C_D(beta_0)={Phi: beta_ref(Phi)|dM=beta_0}", "owns the reference branch before source/readout", "MISSING_PARENT_CONFIGURATION_BUNDLE", "BLOCKED_NONCLAIM"),
        ("DAC2547_1_action_variation", "Parent action is varied at fixed beta_0.", "S_D[Phi;beta_0]=int_M L_MTS+int_dM B_D(Phi;beta_0)+S_matter[q(Phi),Psi;beta_0]", "makes reference data a variational boundary condition, not an empirical fit", "MISSING_PARENT_ACTION_WITH_FIXED_BETA0", "BLOCKED_NONCLAIM"),
        ("DAC2547_2_variation_domain", "Allowed local q/source/readout variations lie in ker(D beta_ref).", "D_a beta_ref=0 for a in {q,source}", "turns the selector criterion into a theorem when parent-signed", "MISSING_VARIATIONAL_DOMAIN_CERTIFICATE", "CONDITIONAL_ONLY"),
        ("DAC2547_3_reference_functional", "B_ref and H_ref depend only on beta_ref and fixed counterterm/topological class.", "B_ref=B_ref[beta_0,B_ct(C_top0)]; H_ref=H_ref[beta_0]", "blocks source/GM/counterterm leakage", "MISSING_REFERENCE_FUNCTIONAL_OWNERSHIP", "BLOCKED_NONCLAIM"),
        ("DAC2547_4_tau_coframe_lock", "Same tau/coframe defines source, charge, clocks, boundary and readout.", "tau_source=tau_charge=tau_clock=tau_boundary=tau_readout=tau_0", "needed for same-frame M_H_ref and later PPN bridge", "MISSING_TAU_COFRAME_LOCK", "BLOCKED_NONCLAIM"),
        ("DAC2547_5_no_shortcut_guard", "No observed-GM surface, orbital-GM denominator, or cancellation counterterm can fill a missing clause.", "claim_allowed=false if beta_0, B_ct or M_H_ref are inferred from target readout", "keeps the route derivational rather than post-hoc", "GUARDRAIL_INSTALLED", "GUARDRAIL_PASS_NONCLAIM"),
    ]
    return [
        stamp(
            no_claim(
                {
                    "row_id": row_id,
                    "clause": clause,
                    "formula": formula,
                    "derivation_role": role,
                    "current_signature": signature,
                    "status": status,
                }
            )
        )
        for row_id, clause, formula, role, signature, status in rows
    ]


def signature_rows() -> list[dict[str, object]]:
    rows = [
        ("SIG2547_0_configuration_bundle", "C_D(beta_0) declared by parent theory", "MISSING_PARENT_CONFIGURATION_BUNDLE", "without this, fixed beta_0 is an imposed closure", "DAC2547_0_parent_bundle"),
        ("SIG2547_1_boundary_surface", "S/domain fixed before source/readout", "MISSING_SOURCE_BLIND_SURFACE_DOMAIN_RULE", "prevents observed-GM boundary laundering", "DAC2547_2_variation_domain"),
        ("SIG2547_2_boundary_metric", "sigma_AB fixed or source-blind by parent boundary condition", "MISSING_BOUNDARY_METRIC_ZERO_CERTIFICATE", "main B_ref embedding input", "FRS2547_2_chain_rule_to_Bref"),
        ("SIG2547_3_tau_coframe", "tau/coframe fixed and shared by charge/clocks/readout", "MISSING_TAU_COFRAME_LOCK", "same-frame reference and PPN bridge", "DAC2547_4_tau_coframe_lock"),
        ("SIG2547_4_topology", "C_top superselected before local variation", "MISSING_CTOP_SUPERSELECTION_CERTIFICATE", "prevents source-selected class switching", "DAC2547_3_reference_functional"),
        ("SIG2547_5_counterterm", "B_ct fixed by boundary variational principle", "MISSING_COUNTERTERM_ZERO_CERTIFICATE", "prevents cancellation-based proof", "DAC2547_3_reference_functional"),
        ("SIG2547_6_embedding", "embedding Hessian/operator norm controlled", "MISSING_EMBEDDING_HESSIAN_OR_OPERATOR_NORM", "prevents hidden non-rigid reference drift", "FRS2547_2_chain_rule_to_Bref"),
        ("SIG2547_7_denominator", "positive same-frame M_H_ref or N_E exists", "MISSING_SAME_FRAME_N_E_OR_MHREF", "normalizes residual without circular orbital-GM import", "FRS2547_3_to_Href_Deltaref"),
        ("SIG2547_8_source_paths", "all signatures have source paths/equation refs", "MISSING_SOURCE_PATHS_FOR_PROMOTION", "required before any valid_for_claim switch", "all rows"),
    ]
    return [
        stamp(
            no_claim(
                {
                    "row_id": row_id,
                    "required_signature": required,
                    "current_fill": current,
                    "why_required": why,
                    "blocks": blocks,
                    "status": "BLOCKED_NONCLAIM",
                }
            )
        )
        for row_id, required, current, why, blocks in rows
    ]


def bound_rows() -> list[dict[str, object]]:
    rows = [
        {
            "row_id": "DRB2547_0_zero_contract_switch",
            "quantity": "Delta_ref_q_source_component_over_MH",
            "bound_formula": "0 only if all DAC2547 and SIG2547 clauses are parent-signed",
            "required_inputs": "parent action with fixed beta_0; tau/coframe lock; C_top/B_ct rules; embedding control; positive same-frame M_H_ref",
            "current_value": "NOT_ALLOWED_AS_VALUE",
            "status": "ZERO_SWITCH_BLOCKED_NONCLAIM",
        },
        {
            "row_id": "DRB2547_1_metric_leak",
            "quantity": "C_sigma*max(||D_q sigma||,||D_source sigma||)/M_H_ref",
            "bound_formula": "metric boundary-data leak normalized by same-frame denominator",
            "required_inputs": "regular_embedding_class; C_sigma; norm_Dq_sigma; norm_Dsource_sigma; M_H_ref; source_path",
            "current_value": "MISSING_VALUE",
            "status": "MISSING_BOUND_VALUE",
        },
        {
            "row_id": "DRB2547_2_tau_leak",
            "quantity": "C_tau*max(||D_q tau||,||D_source tau||)/M_H_ref",
            "bound_formula": "tau/coframe leak normalized by same-frame denominator",
            "required_inputs": "tau_frame_id; C_tau; norm_Dq_tau; norm_Dsource_tau; M_H_ref; source_path",
            "current_value": "MISSING_VALUE",
            "status": "MISSING_BOUND_VALUE",
        },
        {
            "row_id": "DRB2547_3_topology_counterterm_leak",
            "quantity": "max(C_top|D_a C_top|+|D_a B_ct|)/M_H_ref",
            "bound_formula": "topological class and counterterm leak with no cancellation",
            "required_inputs": "C_top rule; B_ct rule; derivatives; M_H_ref; source_path",
            "current_value": "MISSING_VALUE",
            "status": "MISSING_BOUND_VALUE",
        },
        {
            "row_id": "DRB2547_4_total_absolute",
            "quantity": "Delta_ref_over_MH",
            "bound_formula": "absolute sum of metric, tau, topology/counterterm and branch-drift components over M_H_ref",
            "required_inputs": "DRB2547_1 through DRB2547_3; selector branch drift; positive same-frame M_H_ref; no-cancellation guard",
            "current_value": "NOT_COMPUTED_COMPONENTS_MISSING",
            "status": "PRIMARY_NONCLAIM_BOUND_ROW",
        },
    ]
    return [stamp(no_claim({**row, "score_ready": "false"})) for row in rows]


def decision_rows() -> list[dict[str, object]]:
    rows = [
        {
            "row_id": "DEC2547_0_contract_result",
            "decision": "retain fixed-reference zero route as an exact parent-action contract",
            "reason": "the 2455 leak law plus fixed beta_0 variational domain gives D_a B_ref=0 without plateau axiom or cancellation",
            "consequence": "the local branch has a real derivational target, not just a closure wish",
            "status": "CONTRACT_ACCEPTED_NONCLAIM",
        },
        {
            "row_id": "DEC2547_1_no_promotion",
            "decision": "do not promote Delta_ref=0 for current MTS",
            "reason": "configuration bundle, boundary action, tau/coframe, topology, counterterm, embedding and denominator signatures are still missing",
            "consequence": "Delta_ref remains live and non-score-ready",
            "status": "THEOREM_NOT_PARENT_SIGNED",
        },
        {
            "row_id": "DEC2547_2_next",
            "decision": "search for existing parent-action signatures before inventing new closure",
            "reason": "the required contract is explicit enough to audit the corpus for matches",
            "consequence": "2548 should run a signature hunt or demote the reference-zero route to closure-only",
            "status": "SELECT_2548_SIGNATURE_HUNT",
        },
        {
            "row_id": "DEC2547_3_no_github",
            "decision": "keep private",
            "reason": "this is proof scaffolding, not a local-GR result",
            "consequence": "no GitHub/public claim",
            "status": "PRIVATE_NONCLAIM",
        },
    ]
    return [stamp(no_claim(row)) for row in rows]


def claim_gate_rows() -> list[dict[str, object]]:
    rows = [
        ("CG2547_0_fixed_reference_contract", "exact sufficient contract for B_ref q/source silence", "PASS_AS_CONTRACT_ONLY", "mathematical route accepted but not claim-grade"),
        ("CG2547_1_parent_signature", "current corpus proves parent action satisfies fixed beta_0 contract", "FAIL", "all required signatures remain missing"),
        ("CG2547_2_Delta_ref_zero", "Delta_ref q/source leak equals zero for current MTS", "FAIL_NONCLAIM", "zero switch blocked until parent signatures and M_H_ref are present"),
        ("CG2547_3_finite_bound", "finite source-backed Delta_ref bound ready", "FAIL", "bound rows are schema-only with missing values"),
        ("CG2547_4_MHref", "positive same-frame M_H_ref/N_E", "FAIL", "normalization remains blocked"),
        ("CG2547_5_local_GR_Newton", "local GR/Newton/PPN recovery", "FAIL_NONCLAIM", "reference, denominator and source-measure gates remain open"),
    ]
    return [
        stamp(no_claim({"row_id": row_id, "gate": gate, "gate_status": status, "claim_effect": effect}))
        for row_id, gate, status, effect in rows
    ]


def refusal_rows() -> list[dict[str, object]]:
    rows = [
        ("REF2547_0_assume_beta_fixed", "assume beta_ref is fixed without parent configuration bundle", "false", "that would be a closure axiom, not a derived fixed-reference theorem", "SIG2547_0_configuration_bundle;DAC2547_0_parent_bundle"),
        ("REF2547_1_GM_boundary", "choose boundary surface or reference by observed GM/fitted mass", "false", "this imports Newton/source normalization before deriving it", "DAC2547_5_no_shortcut_guard;SIG2547_1_boundary_surface"),
        ("REF2547_2_counterterm_cancel", "choose B_ct after seeing the residual", "false", "post-readout counterterms are cancellation knobs", "SIG2547_5_counterterm;DRB2547_3_topology_counterterm_leak"),
        ("REF2547_3_score_bound_now", "score Delta_ref_over_MH now", "false", "component values and same-frame denominator are missing", "DRB2547_1_metric_leak;DRB2547_4_total_absolute;SIG2547_7_denominator"),
        ("REF2547_4_public_claim", "publish this as local GR/Newton evidence", "false", "fixed-reference contract is progress but not a closed branch", "CG2547_1_parent_signature;CG2547_5_local_GR_Newton"),
    ]
    return [
        stamp(
            no_claim(
                {
                    "row_id": row_id,
                    "claim": claim,
                    "allowed": allowed,
                    "reason": reason,
                    "blocking_rows": blockers,
                }
            )
        )
        for row_id, claim, allowed, reason, blockers in rows
    ]


def next_rows() -> list[dict[str, object]]:
    rows = [
        {
            "row_id": "NEXT2547_0_selected",
            "priority": "selected",
            "next_file": "2548-Y5-R2FR-parent-action-signature-hunt-or-reference-route-demotion.md",
            "next_script": "scripts/Y5_R2FR_parent_action_signature_hunt_or_reference_route_demotion_2548.py",
            "success_condition": "find source-backed parent-action signatures for fixed beta_0, tau/coframe lock, C_top superselection, B_ct rule, embedding control and same-frame M_H_ref",
            "fallback_condition": "demote fixed-reference zero to explicit closure-only and move to finite Delta_ref bound-value acquisition ledger",
        },
        {
            "row_id": "NEXT2547_1_parallel",
            "priority": "parallel",
            "next_file": "2548b-Y5-R2FR-same-frame-MHref-sidecar-or-denominator-row.md",
            "next_script": "scripts/Y5_R2FR_same_frame_MHref_sidecar_or_denominator_row_2548b.py",
            "success_condition": "derive positive same-frame M_H_ref/N_E compatible with beta_0 and tau/coframe lock",
            "fallback_condition": "keep all normalized Delta_ref/Brem rows non-score-ready",
        },
        {
            "row_id": "NEXT2547_2_parallel",
            "priority": "parallel",
            "next_file": "2548c-Y5-R2FR-boundary-data-leak-first-source-values.md",
            "next_script": "scripts/Y5_R2FR_boundary_data_leak_first_source_values_2548c.py",
            "success_condition": "fill at least one finite metric/tau/topology/counterterm leak value with source path, units and no-cancellation guard",
            "fallback_condition": "retain MISSING_VALUE rows and do not score Delta_ref",
        },
    ]
    return [stamp(no_claim(row)) for row in rows]


def branch_copy_rows() -> list[dict[str, object]]:
    copies = {
        BRANCH_COPIES["selector"]: selector_rows(),
        BRANCH_COPIES["bounds"]: bound_rows(),
        BRANCH_COPIES["contract"]: contract_rows(),
        BRANCH_COPIES["next"]: next_rows(),
    }
    rows: list[dict[str, object]] = []
    for path, payload in copies.items():
        write_csv(path, payload)
        rows.append(
            stamp(
                {
                    "row_id": f"COPY2547_{len(rows)}",
                    "copy_path": str(path),
                    "exists": str(path.exists()).lower(),
                    "purpose": "nonclaim branch handoff copy",
                }
            )
        )
    return rows


def csv_has(path: Path, needle: str) -> bool:
    return path.exists() and needle in path.read_text(encoding="utf-8", errors="replace")


def all_flags_false(paths: list[Path]) -> bool:
    watched = {"valid_for_claim", "claim_allowed", "score_ready", "parent_signed", "theorem_zero", "numeric_prediction_present"}
    for path in paths:
        for row in read_csv(path):
            for key in watched.intersection(row):
                if str(row[key]).strip().lower() in {"true", "yes", "1", "pass_for_claim"}:
                    return False
    return True


def validation_rows(outputs: dict[str, Path], sources: list[dict[str, object]]) -> list[dict[str, object]]:
    generated = list(outputs.values())
    generated_before_validation = [path for key, path in outputs.items() if key != "validation"]
    checks: list[tuple[str, bool, str]] = []
    checks.append(("VAL2547_00_required_sources_exist", all(row["exists"] == "true" for row in sources), "all required source paths exist"))
    checks.append(("VAL2547_01_required_needles_found", all(row["needles_found"] == "true" for row in sources), "all source needles found"))
    checks.append(("VAL2547_02_outputs_exist", all(path.exists() for path in generated_before_validation), "all 2547 output files written before validation"))
    csv_parse_ok = True
    for path in generated_before_validation:
        try:
            csv_parse_ok = csv_parse_ok and len(read_csv(path)) > 0
        except Exception:
            csv_parse_ok = False
    checks.append(("VAL2547_03_csv_parse", csv_parse_ok, "all generated CSV files parse and contain rows"))
    checks.append(("VAL2547_04_selector_contract_present", csv_has(outputs["selector"], "FRS2547_2_chain_rule_to_Bref") and csv_has(outputs["contract"], "DAC2547_0_parent_bundle"), "fixed-reference contract and chain-rule theorem present"))
    checks.append(("VAL2547_05_signature_blockers_present", csv_has(outputs["signature"], "SIG2547_7_denominator") and csv_has(outputs["signature"], "MISSING_SAME_FRAME_N_E_OR_MHREF"), "signature blockers explicit"))
    checks.append(("VAL2547_06_bounds_nonready", csv_has(outputs["bounds"], "DRB2547_4_total_absolute") and csv_has(outputs["bounds"], "NOT_COMPUTED_COMPONENTS_MISSING"), "Delta_ref bound rows remain non-score-ready"))
    checks.append(("VAL2547_07_no_shortcut_refusals", csv_has(outputs["refusal"], "REF2547_1_GM_boundary") and csv_has(outputs["refusal"], "REF2547_2_counterterm_cancel"), "GM boundary and counterterm cancellation refused"))
    checks.append(("VAL2547_08_global_claims_blocked", csv_has(outputs["claims"], "CG2547_5_local_GR_Newton") and csv_has(outputs["claims"], "FAIL_NONCLAIM"), "global/local claims remain blocked"))
    checks.append(("VAL2547_09_next_selected", csv_has(outputs["next"], "NEXT2547_0_selected") and csv_has(outputs["next"], "2548-Y5-R2FR-parent-action-signature-hunt-or-reference-route-demotion.md"), "signature hunt/demotion selected next"))
    checks.append(("VAL2547_10_branch_copies", all(path.exists() for path in BRANCH_COPIES.values()), "all nonclaim branch copies exist"))
    checks.append(("VAL2547_11_no_positive_claim_flags", all_flags_false(generated_before_validation + list(BRANCH_COPIES.values())), "all generated claim/readiness flags remain negative"))
    checks.append(("VAL2547_12_formalization_untouched", FORMALIZATION_WORKBENCH.exists() and all(str(path).startswith(str(POST_ROOT)) for path in generated + list(BRANCH_COPIES.values()) + [DOC_PATH]), "generator writes only under post-checkpoint-work"))
    checks.append(("VAL2547_13_pycache_absent", not (POST_ROOT / "scripts" / "__pycache__").exists(), "scripts __pycache__ absent"))
    overall = all(ok for _, ok, _ in checks)
    rows = [
        stamp(
            {
                "row_id": row_id,
                "status": "PASS" if ok else "FAIL",
                "detail": detail,
            }
        )
        for row_id, ok, detail in checks
    ]
    rows.append(
        stamp(
            {
                "row_id": "VAL2547_OVERALL",
                "status": "PASS" if overall else "FAIL",
                "detail": "2547 writes the exact fixed-reference selector contract, blocks promotion without parent signatures/MHref, stages Delta_ref bounds, and selects signature hunt/demotion next",
            }
        )
    )
    return rows


def table(columns: list[str], rows: list[dict[str, object]]) -> str:
    header = "| " + " | ".join(columns) + " |"
    sep = "| " + " | ".join("---" for _ in columns) + " |"
    lines = [header, sep]
    for row in rows:
        lines.append("| " + " | ".join(str(row.get(col, "")).replace("\n", " ") for col in columns) + " |")
    return "\n".join(lines)


def write_doc(outputs: dict[str, Path]) -> None:
    sources = read_csv(outputs["source"])
    selector = read_csv(outputs["selector"])
    contract = read_csv(outputs["contract"])
    signature = read_csv(outputs["signature"])
    bounds = read_csv(outputs["bounds"])
    decision = read_csv(outputs["decision"])
    claims = read_csv(outputs["claims"])
    refusals = read_csv(outputs["refusal"])
    next_target = read_csv(outputs["next"])
    validation = read_csv(outputs["validation"])

    md = f"""# 2547 - fixed reference selector or Delta-ref row

## Result

2547 pins the fixed-reference route to an exact parent-action contract.

The useful theorem is narrow and clean: if the parent action owns a fixed boundary datum
`beta_ref=(S,sigma_AB,tau,C_top,B_ct)=beta_0` and local q/source/readout variations stay inside
`C_D(beta_0)`, then the 2455 leak law gives `D_a B_ref=0` for `a in {{q,source}}` without using a plateau axiom,
post-fit counterterm, observed-GM surface, or sign cancellation.

The current corpus still does not source the required parent signatures or a positive same-frame `M_H_ref/N_E`, so
`Delta_ref=0`, local GR, Newton, PPN, R10, clock, orbital, and GitHub/public claims remain blocked.

## Source Register

{table(["row_id", "source_path", "exists", "needles_found", "source_role"], sources)}

## Fixed Reference Selector Theorem

{table(["row_id", "step", "statement", "formula", "result", "current_status"], selector)}

## Dirichlet Action Contract

{table(["row_id", "clause", "formula", "derivation_role", "current_signature", "status"], contract)}

## Signature Audit

{table(["row_id", "required_signature", "current_fill", "why_required", "blocks", "status"], signature)}

## Delta-ref Bound Rows

{table(["row_id", "quantity", "bound_formula", "required_inputs", "current_value", "status", "score_ready"], bounds)}

## Decision Ledger

{table(["row_id", "decision", "reason", "consequence", "status"], decision)}

## Claim Gates

{table(["row_id", "gate", "gate_status", "claim_effect"], claims)}

## Refusal Runner

{table(["row_id", "claim", "allowed", "reason", "blocking_rows"], refusals)}

## Next Target

{table(["row_id", "priority", "next_file", "success_condition", "fallback_condition"], next_target)}

## Validation

{table(["row_id", "status", "detail"], validation)}

## Generated Files

- `{rel(outputs["source"])}`
- `{rel(outputs["selector"])}`
- `{rel(outputs["contract"])}`
- `{rel(outputs["signature"])}`
- `{rel(outputs["bounds"])}`
- `{rel(outputs["decision"])}`
- `{rel(outputs["claims"])}`
- `{rel(outputs["refusal"])}`
- `{rel(outputs["next"])}`
- `{rel(outputs["copies"])}`
- `{rel(outputs["validation"])}`

## Practical Status

This is a strong-but-private step.  The reference problem is no longer "please be quiet, B_ref"; it is now a signed
parent-boundary-condition problem.  If we can find this fixed-beta signature in the corpus, the reference leak has a
real derivation route.  If we cannot, the honest move is to demote the zero route to closure-only and fill finite
`Delta_ref` bounds.  That is the next hunt.
"""
    DOC_PATH.write_text(md, encoding="utf-8")


def remove_pycache() -> None:
    pycache = POST_ROOT / "scripts" / "__pycache__"
    if pycache.exists():
        shutil.rmtree(pycache)


def main() -> int:
    remove_pycache()
    sources = source_register()
    write_csv(OUTPUTS["source"], sources)
    write_csv(OUTPUTS["selector"], selector_rows())
    write_csv(OUTPUTS["contract"], contract_rows())
    write_csv(OUTPUTS["signature"], signature_rows())
    write_csv(OUTPUTS["bounds"], bound_rows())
    write_csv(OUTPUTS["decision"], decision_rows())
    write_csv(OUTPUTS["claims"], claim_gate_rows())
    write_csv(OUTPUTS["refusal"], refusal_rows())
    write_csv(OUTPUTS["next"], next_rows())
    write_csv(OUTPUTS["copies"], branch_copy_rows())
    validation = validation_rows(OUTPUTS, sources)
    write_csv(OUTPUTS["validation"], validation)
    write_doc(OUTPUTS)
    remove_pycache()

    for row in validation:
        line = f"{row['row_id']},{row['status']},{row['detail']}"
        print(line.encode("ascii", errors="replace").decode("ascii"))
    return 0 if validation[-1]["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())

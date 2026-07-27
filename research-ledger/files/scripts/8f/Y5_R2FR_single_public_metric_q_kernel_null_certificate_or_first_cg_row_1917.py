from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "source-intake" / "mts_residuals"
MICROSCOPE_RESIDUALS = ROOT / "source-intake" / "microscope" / "branch_locked_wep" / "residuals"
QUEUE = ROOT / "source-intake" / "rab-sector" / "acquisition-queue"
SOURCE_WEIGHT_DOCS = ROOT / "source-intake" / "source-weight" / "docs"
QUARANTINE = ROOT / "source-intake" / "microscope" / "quarantine" / "1917"
FORMALIZATION = ROOT.parent / "formalization-workbench"

DOC = ROOT / "1917-Y5-R2FR-single-public-metric-q-kernel-null-certificate-or-first-cg-row.md"
BRANCH_ID = "MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428"
GENERATED_UTC = datetime.now(timezone.utc).isoformat()


INPUTS = {
    "1916_doc": ROOT / "1916-Y5-R2FR-frame-residual-zero-proof-or-source-bound-row.md",
    "1916_validation": OUT / "P8_Y5_BRR545_1916_VALIDATION.csv",
    "1916_zero_gate": OUT / "P8_Y5_PARENT_QLOC_1916_FRAME_ZERO_PROOF_GATE.csv",
    "1916_signature_contract": OUT / "P8_Y5_PARENT_QLOC_1916_PARENT_SIGNATURE_CONTRACT.csv",
    "1916_cg_row": OUT / "P8_Y5_PARENT_QLOC_1916_FRAME_SOURCE_BOUND_ROWS_NONCLAIM.csv",
    "1916_next": OUT / "P8_Y5_PARENT_QLOC_1916_NEXT_TARGET.csv",
    "1029_doc": ROOT / "1029-Y5-R10-cg-no-shadow-frame-theorem-or-first-numeric-coupling-row.md",
    "1029_validation": OUT / "P8_Y5_BRR545_1029_VALIDATION.csv",
    "1029_no_shadow": OUT / "P8_Y5_R10_1029_NO_SHADOW_FRAME_THEOREM_AUDIT.csv",
    "1029_cg_intake": OUT / "P8_Y5_R10_1029_CG_INTAKE_TEMPLATE.csv",
    "1030_doc": ROOT / "1030-Y5-R10-single-public-metric-parent-action-derivation-or-cg-provenance-gate.md",
    "1030_validation": OUT / "P8_Y5_BRR545_1030_VALIDATION.csv",
    "1030_spm_audit": OUT / "P8_Y5_R10_1030_SINGLE_PUBLIC_METRIC_DERIVATION_AUDIT.csv",
    "1030_action_contract": OUT / "P8_Y5_R10_1030_PUBLIC_METRIC_ACTION_CONTRACT.csv",
    "1030_cg_gate": OUT / "P8_Y5_R10_1030_CG_PROVENANCE_GATE_BINDING.csv",
    "1031_doc": ROOT / "1031-Y5-R10-quotient-naturality-terminal-public-metric-proof-or-spm-closure.md",
    "1031_validation": OUT / "P8_Y5_BRR545_1031_VALIDATION.csv",
    "1031_terminal_audit": OUT / "P8_Y5_R10_1031_TERMINAL_PUBLIC_METRIC_PROOF_AUDIT.csv",
    "1031_spm_closure": OUT / "P8_Y5_R10_1031_SPM_CLOSURE_BRANCH.csv",
    "1031_finite_cg": OUT / "P8_Y5_R10_1031_FINITE_CG_TAU_FALLBACK.csv",
    "946_kernel": OUT / "P8_Y5_R10_946_KERNEL_CERTIFICATE_AUDIT.csv",
    "946_cg_interface": OUT / "P8_Y5_R10_946_CG_BA_BOUND_INTERFACE.csv",
    "947_projection": OUT / "P8_Y5_R10_947_PROJECTION_FILL_ATTEMPT.csv",
    "947_claim_gate": OUT / "P8_Y5_R10_947_CLAIM_GATE.csv",
}


SOURCE_NEEDLES = {
    "1916_doc": ["ZFG1916_7_total", "NEXT1916_0_primary"],
    "1916_validation": ["VAL1916_OVERALL", "PASS"],
    "1916_zero_gate": ["ZFG1916_7_total", "FRAME_ZERO_NOT_PROVED_CURRENT_CORPUS"],
    "1916_signature_contract": ["PSC1916_3_single_public_frame", "PSC1916_1_kernel_null"],
    "1916_cg_row": ["FSB1916_0_cg_weyl", "MISSING_PARENT_ZERO_OR_NUMERIC_CG"],
    "1916_next": ["NEXT1916_0_primary", "1917-Y5-R2FR-single-public-metric-q-kernel-null-certificate-or-first-cg-row.md"],
    "1029_doc": ["no-shadow-frame theorem", "Current MTS still cannot claim"],
    "1029_validation": ["V1029_14_formalization_untouched", "pass"],
    "1029_no_shadow": ["NST1029_6_verdict", "FAIL_CURRENT_CLAIM"],
    "1029_cg_intake": ["CGI1029_1_finite_cg_R10", "MISSING_PARENT_INPUT"],
    "1030_doc": ["single-public-metric parent action", "Claim ceiling"],
    "1030_validation": ["V1030_13_formalization_untouched", "pass"],
    "1030_spm_audit": ["SPD1030_6_verdict", "NOT_DERIVED_CURRENT_CORPUS"],
    "1030_action_contract": ["SPM1030_6_contract_verdict", "CONTRACT_READY_NOT_CURRENT_THEOREM"],
    "1030_cg_gate": ["CPG1030_1_finite_cg_value", "MISSING_PARENT_INPUT_AND_SOURCE"],
    "1031_doc": ["terminal public metric proof", "demoted to an explicit nonclaim closure"],
    "1031_validation": ["V1031_13_formalization_untouched", "pass"],
    "1031_terminal_audit": ["TPM1031_6_verdict", "NOT_DERIVED_CURRENT_CORPUS"],
    "1031_spm_closure": ["SPMC1031_0_closure_name", "AVAILABLE_AS_CLOSURE_ONLY"],
    "1031_finite_cg": ["FCG1031_0_cg_value", "MISSING_PARENT_INPUT_OR_THEOREM"],
    "946_kernel": ["KCERT946_3_matter_invisibility", "conditional_not_parent_signed"],
    "946_cg_interface": ["CGB946_0_cg_R10", "MISSING_PARENT_CG_AND_TAU_R10"],
    "947_projection": ["PFA947_4_cg_parent_value", "MISSING_PARENT_CG"],
    "947_claim_gate": ["CGATE947_0_R10_score", "false"],
}


OUTPUTS = {
    "source_register": OUT / "P8_Y5_PARENT_QLOC_1917_SOURCE_REGISTER.csv",
    "spm_qkernel_audit": OUT / "P8_Y5_PARENT_QLOC_1917_SINGLE_PUBLIC_METRIC_QKERNEL_AUDIT.csv",
    "terminal_counterexamples": OUT / "P8_Y5_PARENT_QLOC_1917_TERMINALITY_COUNTEREXAMPLE_LEDGER.csv",
    "cg_first_row": OUT / "P8_Y5_PARENT_QLOC_1917_FIRST_CG_ROW_NONCLAIM.csv",
    "cg_projection_blockers": OUT / "P8_Y5_PARENT_QLOC_1917_CG_PROJECTION_BLOCKER_LEDGER_NONCLAIM.csv",
    "closure_policy": OUT / "P8_Y5_PARENT_QLOC_1917_SPM_CLOSURE_POLICY_NONCLAIM.csv",
    "claim_gate": OUT / "P8_Y5_PARENT_QLOC_1917_CLAIM_GATE.csv",
    "decision": OUT / "P8_Y5_PARENT_QLOC_1917_DECISION_LEDGER.csv",
    "next_target": OUT / "P8_Y5_PARENT_QLOC_1917_NEXT_TARGET.csv",
    "project_status": OUT / "P8_Y5_PARENT_QLOC_1917_PROJECT_STATUS_SNAPSHOT.csv",
    "validation": OUT / "P8_Y5_BRR545_1917_VALIDATION.csv",
}


BRANCH_COPIES = {
    "spm_qkernel_audit": SOURCE_WEIGHT_DOCS / "SINGLE_PUBLIC_METRIC_QKERNEL_AUDIT_1917_NONCLAIM.csv",
    "cg_first_row": MICROSCOPE_RESIDUALS / OUTPUTS["cg_first_row"].name,
    "cg_projection_blockers": QUEUE / "JR1917_CG_PROJECTION_BLOCKERS_NONCLAIM.csv",
    "closure_policy": QUARANTINE / OUTPUTS["closure_policy"].name,
}


def ensure_dirs() -> None:
    for path in [OUT, MICROSCOPE_RESIDUALS, QUEUE, SOURCE_WEIGHT_DOCS, QUARANTINE]:
        path.mkdir(parents=True, exist_ok=True)


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    if not rows:
        raise ValueError(f"no rows supplied for {path}")
    path.parent.mkdir(parents=True, exist_ok=True)
    fieldnames: list[str] = []
    for row in rows:
        for key in row:
            if key not in fieldnames:
                fieldnames.append(key)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def csv_rows(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def source_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def bool_string(value: Any) -> str:
    return str(value).strip().lower()


def markdown_escape(value: Any) -> str:
    return str(value).replace("|", "\\|").replace("\n", "<br>")


def markdown_table(rows: list[dict[str, Any]]) -> str:
    if not rows:
        return "_No rows._"
    headers: list[str] = []
    for row in rows:
        for key in row:
            if key not in headers:
                headers.append(key)
    lines = [
        "| " + " | ".join(headers) + " |",
        "| " + " | ".join("---" for _ in headers) + " |",
    ]
    for row in rows:
        lines.append("| " + " | ".join(markdown_escape(row.get(header, "")) for header in headers) + " |")
    return "\n".join(lines)


def build_source_register() -> list[dict[str, Any]]:
    rows = []
    for key, path in INPUTS.items():
        needles = SOURCE_NEEDLES[key]
        exists = path.exists()
        text = source_text(path) if exists else ""
        missing = [needle for needle in needles if needle not in text]
        status = "EXISTS_NEEDLES_CONFIRMED" if exists and not missing else "MISSING_OR_NEEDLE_FAILED"
        rows.append(
            {
                "branch_id": BRANCH_ID,
                "source_key": key,
                "source_path": str(path),
                "needed_for": "1917 single-public-metric/q-kernel proof or first c_g row",
                "needles": ";".join(needles),
                "status": status,
                "missing_needles": ";".join(missing),
                "valid_for_claim": False,
                "claim_allowed": False,
                "generated_utc": GENERATED_UTC,
            }
        )
    return rows


def build_spm_qkernel_audit() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "audit_id": "SPQ1917_0_target",
            "claim_piece": "derive single public metric/coframe plus q-kernel nullness",
            "mathematical_form": "S_matter = Sbar[Psi,e_pub(q(Phi)),omega[e_pub],theta(q)] and v in ker(Dq) is null/matter-invisible",
            "best_current_evidence": "SPD1030_0 target; PSC1916_0..PSC1916_3",
            "current_status": "TARGET_SHARP_NOT_PROOF",
            "what_would_close": "parent action supplies Q_obs, e_pub, matter-interface restriction, and q-kernel null certificate",
            "blocks_if_missing": "c_g/b_g remains a live retained coefficient",
            "parent_signed": False,
            "valid_for_claim": False,
            "claim_allowed": False,
            "generated_utc": GENERATED_UTC,
        },
        {
            "branch_id": BRANCH_ID,
            "audit_id": "SPQ1917_1_covariance_ward_wep_shortcuts",
            "claim_piece": "derive no shadow frame from covariance, Ward identities, or WEP",
            "mathematical_form": "covariant S_m[Psi,A_g(X)^2g] and common A_g can satisfy Ward/WEP-like checks",
            "best_current_evidence": "SPD1030_1, SPD1030_2, SPD1030_3",
            "current_status": "SHORTCUTS_FAIL",
            "what_would_close": "none; these are necessary consistency checks, not action-domain exclusions",
            "blocks_if_missing": "do not use WEP silence or conservation as c_g=0 proof",
            "parent_signed": False,
            "valid_for_claim": False,
            "claim_allowed": False,
            "generated_utc": GENERATED_UTC,
        },
        {
            "branch_id": BRANCH_ID,
            "audit_id": "SPQ1917_2_terminal_public_metric",
            "claim_piece": "terminal public metric/coframe object",
            "mathematical_form": "there exists e_pub in Q_obs such that every ordinary frame E has unique observable-equivalence morphism E -> e_pub",
            "best_current_evidence": "TPM1031_1 terminal object candidate",
            "current_status": "CONDITIONAL_UNIVERSAL_PROPERTY_WRITTEN",
            "what_would_close": "parent-derived ordinary-observable category plus terminal object, not selected by hand",
            "blocks_if_missing": "terminality remains a closure construction, not parent theorem",
            "parent_signed": False,
            "valid_for_claim": False,
            "claim_allowed": False,
            "generated_utc": GENERATED_UTC,
        },
        {
            "branch_id": BRANCH_ID,
            "audit_id": "SPQ1917_3_matter_interface_restriction",
            "claim_piece": "matter action factors through terminal evaluation before seeing any non-terminal frame",
            "mathematical_form": "S_A = Sbar_A[Psi_A,Eval(e_pub(q(Phi))),theta_A(q)] and not S_A[Psi_A,E_A(q),labels]",
            "best_current_evidence": "TPM1031_2 needed extra premise; SPM1030_1 matter functor domain",
            "current_status": "NEEDED_EXTRA_PREMISE_NOT_PARENT_DERIVED",
            "what_would_close": "parent action-domain theorem excluding pre-terminal E_A and label dependence",
            "blocks_if_missing": "matter can still use a shadow frame before the terminal map",
            "parent_signed": False,
            "valid_for_claim": False,
            "claim_allowed": False,
            "generated_utc": GENERATED_UTC,
        },
        {
            "branch_id": BRANCH_ID,
            "audit_id": "SPQ1917_4_qkernel_null",
            "claim_piece": "ker(Dq) directions are physical gauge/null and matter-invisible",
            "mathematical_form": "i_v Omega_parent=0, i_v Theta_parent=dB_v with zero local flux, and Lie_v S_matter=0",
            "best_current_evidence": "KCERT946_0..KCERT946_3; PSC1916_1",
            "current_status": "FAILED_CURRENT_CORPUS",
            "what_would_close": "bulk null, boundary primitive, no-marker, and matter invisibility signed in one branch",
            "blocks_if_missing": "Dq[v]=0 is not enough to make v physically silent",
            "parent_signed": False,
            "valid_for_claim": False,
            "claim_allowed": False,
            "generated_utc": GENERATED_UTC,
        },
        {
            "branch_id": BRANCH_ID,
            "audit_id": "SPQ1917_5_field_rename_guard",
            "claim_piece": "frame dependence cannot be hidden in constants, source weights, G_eff, clocks, or boundary support",
            "mathematical_form": "same parent ledger owns e_pub, theta_A, alpha_EM, G_eff, T_total, tau/readout, and W_source",
            "best_current_evidence": "TPM1031_4; SPM1030_4; SPM1030_5",
            "current_status": "REQUIRED_GUARD_NOT_PARENT_SIGNED",
            "what_would_close": "constant/source/readout/boundary residuals zeroed or retained in the same branch",
            "blocks_if_missing": "c_g=0 can just reappear as b_A, b_alpha, q_nonH, or Delta_W_support",
            "parent_signed": False,
            "valid_for_claim": False,
            "claim_allowed": False,
            "generated_utc": GENERATED_UTC,
        },
        {
            "branch_id": BRANCH_ID,
            "audit_id": "SPQ1917_6_total_verdict",
            "claim_piece": "single-public-metric/q-kernel theorem establishes c_g=0",
            "mathematical_form": "SPQ1917_2 + SPQ1917_3 + SPQ1917_4 + SPQ1917_5 => no independent A_g(Xhat) slot and c_g=0",
            "best_current_evidence": "TPM1031_6 verdict; SPD1030_6 verdict; ZFG1916_7 total",
            "current_status": "NOT_DERIVED_CURRENT_CORPUS_CLOSURE_ONLY",
            "what_would_close": "all parent signatures above sourced in one branch",
            "blocks_if_missing": "stage first c_g row as nonclaim and keep SPM as closure only",
            "parent_signed": False,
            "valid_for_claim": False,
            "claim_allowed": False,
            "generated_utc": GENERATED_UTC,
        },
    ]


def build_terminal_counterexamples() -> list[dict[str, Any]]:
    rows = [
        (
            "TCE1917_0_terminal_but_functor_uses_E",
            "terminal e_pub exists",
            "S_A[Psi_A,E_A(q),theta_A] is evaluated before unique E_A -> e_pub",
            "matter still sees species/readout frame",
            "matter-interface functor must be terminal-evaluation only",
        ),
        (
            "TCE1917_1_terminal_with_labels",
            "unique map to e_pub exists",
            "objects carry labels L or natural transformations and S_matter depends on L",
            "source weights, markers, or constants survive terminality",
            "ordinary matter functor must forget non-public labels before action evaluation",
        ),
        (
            "TCE1917_2_terminal_after_frame_rename",
            "metric object is terminal",
            "move A_g(Xhat) into m_A(Xhat), alpha_EM(Xhat), G_eff(Xhat), or tau readout",
            "c_g zero is only a notation move",
            "field-rename guard across geometry, constants, sources, clocks, and support",
        ),
        (
            "TCE1917_3_terminal_not_kernel_owned",
            "e_pub is selected as public object",
            "Dq-kernel directions are not presymplectic-null or boundary silent",
            "representative motion is physical and can source finite coupling",
            "q-kernel null certificate",
        ),
        (
            "TCE1917_4_common_frame_WEP_silent",
            "universal A_g is common to all species",
            "eta_AB can vanish while c_g still affects R10, PPN, clock, source normalization, or orbital response",
            "WEP-only success does not prove no shadow frame",
            "cross-arena c_g projection or no-shadow theorem",
        ),
    ]
    return [
        {
            "branch_id": BRANCH_ID,
            "counterexample_id": counterexample_id,
            "premise_satisfied": premise_satisfied,
            "construction": construction,
            "what_breaks": what_breaks,
            "required_repair": required_repair,
            "blocks_spm_theorem": True,
            "valid_for_claim": False,
            "claim_allowed": False,
            "generated_utc": GENERATED_UTC,
        }
        for counterexample_id, premise_satisfied, construction, what_breaks, required_repair in rows
    ]


def build_cg_first_row() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "row_id": "CG1917_0_first_cg_row",
            "symbol": "c_g/b_g",
            "branch_type": "finite_frame_leak_or_parent_zero",
            "definition": "c_g := Lie_v ln A_g, the vertical derivative of a common conformal/Weyl matter-source frame relative to the public observed coframe",
            "normal_form": "delta_X S_matter contains sqrt(-g) T c_g delta Xhat plus branch-declared normalization terms",
            "zero_route": "c_g=0 if single-public-metric/no-extra-frame action slot and q-kernel null certificate are parent-signed",
            "finite_route": "numeric c_g with units, source path, source row id, uncertainty/prior, and derivation status",
            "source_path": "MISSING_PARENT_SOURCE",
            "source_row_id": "MISSING_SOURCE_ROW_ID",
            "candidate_value": "MISSING_PARENT_INPUT",
            "units": "dimensionless",
            "uncertainty_or_prior": "MISSING_UNCERTAINTY",
            "normalization": "MISSING_XHAT_NORMALIZATION",
            "arena_projection": "MISSING_ARENA_PROJECTION",
            "observable_links": "R10;PPN;WEP;clock;source_normalization;orbital_common_mode",
            "source_ids": "FSB1916_0_cg_weyl;CGI1029_1_finite_cg_R10;CPG1030_1_finite_cg_value;FCG1031_0_cg_value;PFA947_4_cg_parent_value",
            "current_status": "FIRST_CG_ROW_STAGED_SOURCE_READY_BUT_UNFILLED_NONCLAIM",
            "score_ready": False,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
            "generated_utc": GENERATED_UTC,
        }
    ]


def build_cg_projection_blockers() -> list[dict[str, Any]]:
    blockers = [
        (
            "CGBL1917_0_parent_value",
            "numeric c_g or parent-signed c_g=0 theorem",
            "MISSING_PARENT_INPUT_OR_THEOREM",
            "CPG1030_0_zero_branch;CPG1030_1_finite_cg_value;FCG1031_0_cg_value",
            "prove single-public-metric/q-kernel theorem or source finite c_g",
        ),
        (
            "CGBL1917_1_Xhat_normalization",
            "normalization of Xhat and A_g convention",
            "MISSING_XHAT_NORMALIZATION",
            "NST1029_5_matter_variation_trace;FSB1916_0_cg_weyl",
            "define dimensionless c_g convention before any projection",
        ),
        (
            "CGBL1917_2_tau_R10",
            "K_X(lambda), Qbar_XH, tau_R10, source/test profile, and bound-curve link",
            "MISSING_TAU_R10_AND_PARENT_CG",
            "PFA947_0_R10_projection;CGB946_0_cg_R10;FCG1031_1_tau_R10",
            "source branch-locked R10 projection kernel after parent c_g is available",
        ),
        (
            "CGBL1917_3_PPN_response",
            "M_gamma/M_beta weak-field response matrix with gauge/frame certificate",
            "MISSING_PPN_RESPONSE_MATRIX",
            "PFA947_1_PPN_projection;CGB946_1_cg_PPN_gamma;CGB946_2_cg_PPN_beta;FCG1031_2_tau_PPN",
            "derive local weak-field response before PPN comparison",
        ),
        (
            "CGBL1917_4_clock_common_mode",
            "clock/tau sensitivity split separate from constants sector",
            "MISSING_CLOCK_SPLIT_AND_CONSTANT_SECTOR_LOCK",
            "PFA947_3_clock_product_projection;APR1916_3_clock_drift",
            "do not treat common frame as WEP-only; source clock/common-mode projection",
        ),
        (
            "CGBL1917_5_no_cancellation",
            "absolute local envelope with no cancellation against b_A/b_dis/q_nonH/Delta_W",
            "ABSOLUTE_ENVELOPE_REQUIRED",
            "CPG1030_4_no_cancellation;NSG1916_0_absolute_envelope",
            "sum absolute components until a parent identity proves cancellation",
        ),
    ]
    return [
        {
            "branch_id": BRANCH_ID,
            "blocker_id": blocker_id,
            "needed_input": needed_input,
            "current_status": current_status,
            "source_ids": source_ids,
            "next_action": next_action,
            "valid_for_claim": False,
            "claim_allowed": False,
            "generated_utc": GENERATED_UTC,
        }
        for blocker_id, needed_input, current_status, source_ids, next_action in blockers
    ]


def build_closure_policy() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "policy_id": "SPMC1917_0_closure_name",
            "closure": "Single Public Metric closure",
            "allowed_language": "closure/selection principle or explicit branch assumption",
            "forbidden_language": "derived parent theorem; local-GR pass; c_g=0 evidence",
            "mathematical_form": "S_matter restricted by closure to Sbar[Psi,e_pub(q),omega[e_pub],theta(q)]",
            "status": "AVAILABLE_AS_CLOSURE_ONLY",
            "valid_for_claim": False,
            "claim_allowed": False,
            "generated_utc": GENERATED_UTC,
        },
        {
            "branch_id": BRANCH_ID,
            "policy_id": "SPMC1917_1_cg_effect",
            "closure": "c_g inside SPM closure",
            "allowed_language": "c_g is absent/zero inside the closure branch",
            "forbidden_language": "c_g is theorem-zero in MTS without parent proof",
            "mathematical_form": "no independent A_g(Xhat)e_pub slot in the closure action domain",
            "status": "CONDITIONAL_BRANCH_SIMPLIFICATION_NOT_PARENT_THEOREM",
            "valid_for_claim": False,
            "claim_allowed": False,
            "generated_utc": GENERATED_UTC,
        },
        {
            "branch_id": BRANCH_ID,
            "policy_id": "SPMC1917_2_remaining_residuals",
            "closure": "anti-overclaim residue",
            "allowed_language": "b_A, b_alpha, b_dis, q_nonH, Delta_tau_n, Delta_W_support, measured-GM, and left-hand EH/Newton gates remain separate",
            "forbidden_language": "SPM closure alone proves full local GR/Newton reduction",
            "mathematical_form": "closure removes only the independent common frame slot unless extended by parent signatures",
            "status": "RETAIN_RESIDUALS",
            "valid_for_claim": False,
            "claim_allowed": False,
            "generated_utc": GENERATED_UTC,
        },
    ]


def build_claim_gate() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "gate_id": "CG1917_0_sources",
            "claim": "all 1917 cited sources exist",
            "required_condition": "source register rows are confirmed",
            "current_status": "SOURCE_REGISTER_PASS_IF_VALIDATION_PASS",
            "gate_pass": True,
            "valid_for_claim": False,
            "claim_allowed": False,
            "generated_utc": GENERATED_UTC,
        },
        {
            "branch_id": BRANCH_ID,
            "gate_id": "CG1917_1_spm_theorem",
            "claim": "single-public-metric/q-kernel theorem is derived",
            "required_condition": "SPQ1917_2 through SPQ1917_5 parent-signed",
            "current_status": "FALSE_NOT_DERIVED_CURRENT_CORPUS",
            "gate_pass": False,
            "valid_for_claim": False,
            "claim_allowed": False,
            "generated_utc": GENERATED_UTC,
        },
        {
            "branch_id": BRANCH_ID,
            "gate_id": "CG1917_2_cg_zero",
            "claim": "c_g=0 by parent theorem",
            "required_condition": "SPM theorem plus no-shadow/no-field-rename guard",
            "current_status": "FALSE_CLOSURE_ONLY",
            "gate_pass": False,
            "valid_for_claim": False,
            "claim_allowed": False,
            "generated_utc": GENERATED_UTC,
        },
        {
            "branch_id": BRANCH_ID,
            "gate_id": "CG1917_3_finite_cg_score",
            "claim": "finite c_g row can be scored",
            "required_condition": "numeric c_g/source path/source row id/uncertainty/projection kernels",
            "current_status": "FALSE_FIRST_ROW_UNFILLED",
            "gate_pass": False,
            "valid_for_claim": False,
            "claim_allowed": False,
            "generated_utc": GENERATED_UTC,
        },
        {
            "branch_id": BRANCH_ID,
            "gate_id": "CG1917_4_local_gr",
            "claim": "local GR/Newton/WEP/PPN/R10/clock/orbital pass follows",
            "required_condition": "frame residual theorem-zero or source-backed plus other residuals and arena kernels closed",
            "current_status": "CLAIM_BLOCKED",
            "gate_pass": False,
            "valid_for_claim": False,
            "claim_allowed": False,
            "generated_utc": GENERATED_UTC,
        },
    ]


def build_decision() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "decision_id": "DEC1917_0_spm_result",
            "decision": "SPM_ROUTE_RETAINED_AS_CLOSURE_ONLY",
            "reason": "Terminal public metric plus quotient naturality still needs parent-derived matter-interface restriction and q-kernel nullness.",
            "consequence": "Do not claim c_g=0 from terminality alone.",
            "valid_for_claim": False,
            "claim_allowed": False,
            "generated_utc": GENERATED_UTC,
        },
        {
            "branch_id": BRANCH_ID,
            "decision_id": "DEC1917_1_cg_row",
            "decision": "FIRST_CG_ROW_STAGED_BUT_UNFILLED",
            "reason": "The zero theorem remains unsigned and no numeric parent c_g/source/projection exists.",
            "consequence": "c_g is now a concrete first-row acquisition target rather than a vague coupling problem.",
            "valid_for_claim": False,
            "claim_allowed": False,
            "generated_utc": GENERATED_UTC,
        },
        {
            "branch_id": BRANCH_ID,
            "decision_id": "DEC1917_2_next_route",
            "decision": "NARROW_TO_PARENT_CG_OR_QKERNEL_CERTIFICATE",
            "reason": "Broad SPM rhetoric is exhausted; the next useful work is a parent source for c_g or a real q-kernel/matter-interface proof.",
            "consequence": "1918 should either produce source evidence for c_g=0/finite c_g or explicitly demote the frame route to closure-only.",
            "valid_for_claim": False,
            "claim_allowed": False,
            "generated_utc": GENERATED_UTC,
        },
    ]


def build_next_target() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "route_id": "NEXT1917_0_primary",
            "selection_status": "selected",
            "target_doc": "1918-Y5-R2FR-parent-cg-source-or-qkernel-matter-interface-proof.md",
            "target_script": "scripts/Y5_R2FR_parent_cg_source_or_qkernel_matter_interface_proof_1918.py",
            "objective": "try one last narrow derivation/source pass for c_g: either parent-sign the q-kernel plus matter-interface theorem that removes A_g, or source a finite c_g parent value/projection row; otherwise demote SPM/frame-zero to closure-only explicitly",
            "success_condition": "c_g gets a parent theorem-zero source path, a finite source-backed nonclaim row, or an explicit closure-only demotion with blockers preserved",
            "do_not": "do not use terminality alone, WEP silence, covariance, Ward identities, or empirical bounds as c_g proof",
            "valid_for_claim": False,
            "claim_allowed": False,
            "generated_utc": GENERATED_UTC,
        }
    ]


def build_project_status() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "status_id": "STAT1917_0_gain",
            "area": "single-public-metric route",
            "summary": "1917 consolidates the SPM/q-kernel evidence and proves it is closure-only in the current corpus.",
            "risk_level": "THEOREM_NOT_CLOSED_BUT_SCOPE_SHARPENED",
            "project_meaning": "we stopped the biggest possible self-deception: terminality is not automatically an action-domain exclusion",
            "next_action": "narrow parent c_g/q-kernel proof or demote closure explicitly",
            "valid_for_claim": False,
            "claim_allowed": False,
            "generated_utc": GENERATED_UTC,
        },
        {
            "branch_id": BRANCH_ID,
            "status_id": "STAT1917_1_cg",
            "area": "c_g fallback",
            "summary": "The first c_g/b_g row now exists as a branch-locked acquisition target but has no parent value or projection.",
            "risk_level": "DATA_FACING_SCHEMA_ONLY",
            "project_meaning": "the coupling problem is no longer foggy; it has a named first row and named blockers",
            "next_action": "source parent c_g or prove no A_g slot",
            "valid_for_claim": False,
            "claim_allowed": False,
            "generated_utc": GENERATED_UTC,
        },
        {
            "branch_id": BRANCH_ID,
            "status_id": "STAT1917_2_guard",
            "area": "claim discipline",
            "summary": "No local-GR, c_g=0, finite-c_g, WEP, R10, PPN, clock, or orbital claim is allowed from 1917.",
            "risk_level": "CLAIM_DISCIPLINE_MAINTAINED",
            "project_meaning": "we are still deriving instead of scoring ghosts",
            "next_action": "keep frame route private/nonclaim until one theorem/source row is real",
            "valid_for_claim": False,
            "claim_allowed": False,
            "generated_utc": GENERATED_UTC,
        },
    ]


def build_rows() -> dict[str, list[dict[str, Any]]]:
    return {
        "source_register": build_source_register(),
        "spm_qkernel_audit": build_spm_qkernel_audit(),
        "terminal_counterexamples": build_terminal_counterexamples(),
        "cg_first_row": build_cg_first_row(),
        "cg_projection_blockers": build_cg_projection_blockers(),
        "closure_policy": build_closure_policy(),
        "claim_gate": build_claim_gate(),
        "decision": build_decision(),
        "next_target": build_next_target(),
        "project_status": build_project_status(),
    }


def copy_branch_artifacts() -> None:
    for key, destination in BRANCH_COPIES.items():
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(OUTPUTS[key], destination)


def remove_pycache() -> None:
    pycache = Path(__file__).resolve().parent / "__pycache__"
    if pycache.exists():
        shutil.rmtree(pycache)


def claim_flags_safe(paths: list[Path]) -> tuple[bool, str]:
    unsafe: list[str] = []
    for path in paths:
        for row in csv_rows(path):
            if "valid_for_claim" in row and bool_string(row["valid_for_claim"]) != "false":
                unsafe.append(f"{path.name}:valid_for_claim")
            if "claim_allowed" in row and bool_string(row["claim_allowed"]) != "false":
                unsafe.append(f"{path.name}:claim_allowed")
    return not unsafe, "claim flags all false" if not unsafe else ";".join(unsafe)


def csv_parse_check(paths: list[Path]) -> tuple[bool, str]:
    failures: list[str] = []
    for path in paths:
        try:
            rows = csv_rows(path)
        except Exception as exc:
            failures.append(f"{path.name}:{exc}")
            continue
        if not rows:
            failures.append(f"{path.name}:no_rows")
    return not failures, "all generated CSVs parse with rows" if not failures else ";".join(failures)


def validation_rows() -> list[dict[str, Any]]:
    generated_without_validation = [path for key, path in OUTPUTS.items() if key != "validation"]
    checks: list[dict[str, Any]] = []
    source_rows_loaded = csv_rows(OUTPUTS["source_register"])
    checks.append(
        {
            "validation_id": "VAL1917_00_sources",
            "status": "PASS" if all(row["status"] == "EXISTS_NEEDLES_CONFIRMED" for row in source_rows_loaded) else "FAIL",
            "detail": "all local source paths exist and needles found",
            "valid_for_claim": False,
            "claim_allowed": False,
        }
    )
    spm_rows = csv_rows(OUTPUTS["spm_qkernel_audit"])
    checks.append(
        {
            "validation_id": "VAL1917_01_spm_qkernel",
            "status": "PASS"
            if any(row["audit_id"] == "SPQ1917_6_total_verdict" and row["current_status"] == "NOT_DERIVED_CURRENT_CORPUS_CLOSURE_ONLY" for row in spm_rows)
            and all(bool_string(row["parent_signed"]) == "false" for row in spm_rows)
            else "FAIL",
            "detail": "SPM/q-kernel route remains closure-only, not theorem",
            "valid_for_claim": False,
            "claim_allowed": False,
        }
    )
    counter_rows = csv_rows(OUTPUTS["terminal_counterexamples"])
    checks.append(
        {
            "validation_id": "VAL1917_02_counterexamples",
            "status": "PASS" if len(counter_rows) >= 4 and all(bool_string(row["blocks_spm_theorem"]) == "true" for row in counter_rows) else "FAIL",
            "detail": "terminality counterexamples retained",
            "valid_for_claim": False,
            "claim_allowed": False,
        }
    )
    cg_rows = csv_rows(OUTPUTS["cg_first_row"])
    checks.append(
        {
            "validation_id": "VAL1917_03_first_cg_row",
            "status": "PASS"
            if len(cg_rows) == 1
            and cg_rows[0]["current_status"] == "FIRST_CG_ROW_STAGED_SOURCE_READY_BUT_UNFILLED_NONCLAIM"
            and cg_rows[0]["candidate_value"] == "MISSING_PARENT_INPUT"
            and bool_string(cg_rows[0]["score_ready"]) == "false"
            else "FAIL",
            "detail": "first c_g row staged but unfilled/nonclaim",
            "valid_for_claim": False,
            "claim_allowed": False,
        }
    )
    blockers = csv_rows(OUTPUTS["cg_projection_blockers"])
    checks.append(
        {
            "validation_id": "VAL1917_04_cg_blockers",
            "status": "PASS" if len(blockers) >= 5 and all(bool_string(row["valid_for_claim"]) == "false" for row in blockers) else "FAIL",
            "detail": "c_g projection blockers retained",
            "valid_for_claim": False,
            "claim_allowed": False,
        }
    )
    closure_rows = csv_rows(OUTPUTS["closure_policy"])
    checks.append(
        {
            "validation_id": "VAL1917_05_closure_policy",
            "status": "PASS" if any(row["status"] == "AVAILABLE_AS_CLOSURE_ONLY" for row in closure_rows) else "FAIL",
            "detail": "SPM language limited to closure-only",
            "valid_for_claim": False,
            "claim_allowed": False,
        }
    )
    gates = csv_rows(OUTPUTS["claim_gate"])
    checks.append(
        {
            "validation_id": "VAL1917_06_claim_gate",
            "status": "PASS" if any(row["gate_id"] == "CG1917_4_local_gr" and row["current_status"] == "CLAIM_BLOCKED" for row in gates) else "FAIL",
            "detail": "claim remains blocked",
            "valid_for_claim": False,
            "claim_allowed": False,
        }
    )
    next_rows = csv_rows(OUTPUTS["next_target"])
    checks.append(
        {
            "validation_id": "VAL1917_07_next_target",
            "status": "PASS" if any(row["route_id"] == "NEXT1917_0_primary" and row["selection_status"] == "selected" for row in next_rows) else "FAIL",
            "detail": "1918 parent c_g/q-kernel route selected",
            "valid_for_claim": False,
            "claim_allowed": False,
        }
    )
    flags_ok, flags_detail = claim_flags_safe(generated_without_validation)
    checks.append(
        {
            "validation_id": "VAL1917_08_claim_flags_safe",
            "status": "PASS" if flags_ok else "FAIL",
            "detail": flags_detail,
            "valid_for_claim": False,
            "claim_allowed": False,
        }
    )
    parse_ok, parse_detail = csv_parse_check(generated_without_validation)
    checks.append(
        {
            "validation_id": "VAL1917_09_csv_parse",
            "status": "PASS" if parse_ok else "FAIL",
            "detail": parse_detail,
            "valid_for_claim": False,
            "claim_allowed": False,
        }
    )
    checks.append(
        {
            "validation_id": "VAL1917_10_branch_copies",
            "status": "PASS" if all(path.exists() for path in BRANCH_COPIES.values()) else "FAIL",
            "detail": "; ".join(str(path) for path in BRANCH_COPIES.values()),
            "valid_for_claim": False,
            "claim_allowed": False,
        }
    )
    pycache = Path(__file__).resolve().parent / "__pycache__"
    checks.append(
        {
            "validation_id": "VAL1917_11_pycache_absent",
            "status": "PASS" if not pycache.exists() else "FAIL",
            "detail": str(pycache),
            "valid_for_claim": False,
            "claim_allowed": False,
        }
    )
    formalization_hits = []
    if FORMALIZATION.exists():
        artifact_needles = [
            "1917-Y5-R2FR-single-public-metric",
            "P8_Y5_PARENT_QLOC_1917",
            "Y5_R2FR_single_public_metric_q_kernel_null_certificate_or_first_cg_row_1917",
        ]
        formalization_hits = [
            path
            for path in FORMALIZATION.rglob("*")
            if path.is_file() and any(needle in path.name for needle in artifact_needles)
        ]
    checks.append(
        {
            "validation_id": "VAL1917_12_formalization_untouched",
            "status": "PASS" if not formalization_hits else "FAIL",
            "detail": f"formalization_1917_artifact_count={len(formalization_hits)}",
            "valid_for_claim": False,
            "claim_allowed": False,
        }
    )
    fail_count = sum(1 for row in checks if row["status"] != "PASS")
    checks.append(
        {
            "validation_id": "VAL1917_OVERALL",
            "status": "PASS" if fail_count == 0 else "FAIL",
            "detail": "1917 single-public-metric q-kernel certificate or first c_g row",
            "valid_for_claim": False,
            "claim_allowed": False,
        }
    )
    return checks


def write_doc(rows_by_name: dict[str, list[dict[str, Any]]]) -> None:
    validation = csv_rows(OUTPUTS["validation"])
    content = f"""# 1917 - Single Public Metric q-Kernel Null Certificate Or First c_g Row

## Purpose

This checkpoint follows the 1916 target. It tests whether the single-public-metric/no-shadow-frame clause plus a q-kernel null certificate can be promoted to a parent theorem. If not, it stages the first concrete `c_g/b_g` row as a nonclaim acquisition target.

## Result

- The single-public-metric route is still useful, but currently closure-only.
- Terminality alone does not forbid matter from depending on a non-terminal frame, label, constant, or source normalization before mapping to the terminal/public object.
- The q-kernel remains unsigned: `Dq[v]=0` is not enough unless the parent proves null/gauge behaviour, boundary silence, and matter invisibility.
- The first `c_g/b_g` row is now explicit and branch-locked, but unfilled: no parent value/theorem source, no uncertainty, no `Xhat` normalization, and no arena projection.
- Claim status remains blocked.

## Source Register

{markdown_table(rows_by_name["source_register"])}

## Single-Public-Metric q-Kernel Audit

{markdown_table(rows_by_name["spm_qkernel_audit"])}

## Terminality Counterexamples

{markdown_table(rows_by_name["terminal_counterexamples"])}

## First c_g Row

{markdown_table(rows_by_name["cg_first_row"])}

## c_g Projection Blocker Ledger

{markdown_table(rows_by_name["cg_projection_blockers"])}

## SPM Closure Policy

{markdown_table(rows_by_name["closure_policy"])}

## Claim Gate

{markdown_table(rows_by_name["claim_gate"])}

## Decision Ledger

{markdown_table(rows_by_name["decision"])}

## Next Target

{markdown_table(rows_by_name["next_target"])}

## Project Status Snapshot

{markdown_table(rows_by_name["project_status"])}

## Validation

{markdown_table(validation)}
"""
    DOC.write_text(content, encoding="utf-8")


def main() -> None:
    ensure_dirs()
    remove_pycache()
    rows_by_name = build_rows()
    for key, rows in rows_by_name.items():
        write_csv(OUTPUTS[key], rows)
    copy_branch_artifacts()
    remove_pycache()
    write_csv(OUTPUTS["validation"], validation_rows())
    write_doc(rows_by_name)


if __name__ == "__main__":
    main()

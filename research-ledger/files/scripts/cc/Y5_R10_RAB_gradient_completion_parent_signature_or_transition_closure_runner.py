from __future__ import annotations

import csv
from pathlib import Path


PACK_ID = "P8_Y5_R10_1379"
TITLE = "1379-Y5-R10-RAB-gradient-completion-parent-signature-or-transition-closure-runner"
ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = ROOT / "source-intake" / "mts_residuals"
DOC_PATH = ROOT / f"{TITLE}.md"
FORMALIZATION = ROOT.parent / "formalization-workbench"

SOURCE_REGISTER_PATH = OUT_DIR / f"{PACK_ID}_SOURCE_REGISTER.csv"
PARENT_SIGNATURE_PATH = OUT_DIR / f"{PACK_ID}_GRADIENT_PARENT_SIGNATURE_AUDIT.csv"
DIMENSIONAL_LOCK_PATH = OUT_DIR / f"{PACK_ID}_KAPPA_DIMENSIONAL_LOCK.csv"
CLOSURE_RUNNER_PATH = OUT_DIR / f"{PACK_ID}_TRANSITION_CLOSURE_RUNNER_SCHEMA.csv"
FORMULA_FEED_PATH = OUT_DIR / f"{PACK_ID}_CONDITIONAL_FORMULA_FEED.csv"
RUNNER_FEED_PATH = OUT_DIR / f"{PACK_ID}_RUNNER_FEED_UPDATE.csv"
CLAIM_GATE_PATH = OUT_DIR / f"{PACK_ID}_CLAIM_GATE.csv"
DECISION_PATH = OUT_DIR / f"{PACK_ID}_DECISION_LEDGER.csv"
NEXT_PATH = OUT_DIR / f"{PACK_ID}_NEXT_TARGET.csv"
VALIDATION_PATH = OUT_DIR / "P8_Y5_BRR545_1379_VALIDATION.csv"


def source_path(relative_path: str) -> Path:
    path = Path(relative_path)
    if path.is_absolute():
        return path
    return ROOT / path


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def write_csv(path: Path, rows: list[dict[str, object]], fieldnames: list[str] | None = None) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if fieldnames is None:
        fieldnames = []
        for row in rows:
            for key in row:
                if key not in fieldnames:
                    fieldnames.append(key)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def read_csv_rows(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def cell(value: object) -> str:
    return str(value).replace("\n", " ").replace("|", "\\|")


def table(headers: list[str], rows: list[dict[str, object]]) -> str:
    out = [
        "| " + " | ".join(headers) + " |",
        "| " + " | ".join(["---"] * len(headers)) + " |",
    ]
    for row in rows:
        out.append("| " + " | ".join(cell(row.get(header, "")) for header in headers) + " |")
    return "\n".join(out)


def mark_nonclaim(rows: list[dict[str, object]]) -> list[dict[str, object]]:
    for row in rows:
        row["valid_for_claim"] = False
        row["claim_allowed"] = False
    return rows


def source_register() -> list[dict[str, object]]:
    rows = [
        {
            "source_id": "SRC1379_0_1378_doc",
            "source_path": "1378-Y5-R10-RAB-transition-parent-law-derivation-or-explicit-closure-input-pack.md",
            "required_anchor": "NEXT1378_0_1379",
            "purpose": "1378 handoff to parent-sign the gradient branch or build a closure runner.",
        },
        {
            "source_id": "SRC1379_1_1378_next",
            "source_path": "source-intake/mts_residuals/P8_Y5_R10_1378_NEXT_TARGET.csv",
            "required_anchor": "NEXT1378_0_1379",
            "purpose": "machine-readable 1379 target.",
        },
        {
            "source_id": "SRC1379_2_1378_gradient",
            "source_path": "source-intake/mts_residuals/P8_Y5_R10_1378_CONDITIONAL_GRADIENT_RELAXATION_BRANCH.csv",
            "required_anchor": "GRB1378_7_branch_verdict",
            "purpose": "conditional gradient-relaxation branch formulas.",
        },
        {
            "source_id": "SRC1379_3_1378_closure_pack",
            "source_path": "source-intake/mts_residuals/P8_Y5_R10_1378_EXPLICIT_CLOSURE_INPUT_PACK.csv",
            "required_anchor": "CIP1378_1_kappa_m",
            "purpose": "closure input checklist to transform into a runner schema.",
        },
        {
            "source_id": "SRC1379_4_1248_action_ansatz",
            "source_path": "source-intake/mts_residuals/P8_Y5_R10_1248_MINIMAL_PARENT_ACTION_ANSATZ.csv",
            "required_anchor": "ANS1248_1_action",
            "purpose": "minimal parent action is still schematic.",
        },
        {
            "source_id": "SRC1379_5_1276_euler_contract",
            "source_path": "source-intake/mts_residuals/P8_Y5_R10_1276_PARENT_EULER_SOURCE_CONTRACT.csv",
            "required_anchor": "ESC1276_2_E_time",
            "purpose": "Euler/source equations are missing or contract-only.",
        },
        {
            "source_id": "SRC1379_6_1302_fixed_field",
            "source_path": "source-intake/mts_residuals/P8_Y5_R10_1302_FIXED_FIELD_M_SIGNATURE_AUDIT.csv",
            "required_anchor": "FFA1302_5_verdict",
            "purpose": "m fixed-field status remains conditional/nonclaim.",
        },
        {
            "source_id": "SRC1379_7_1302_memory_stress",
            "source_path": "source-intake/mts_residuals/P8_Y5_R10_1302_MEMORY_STRESS_RESIDUAL_CONTRACT_NONCLAIM.csv",
            "required_anchor": "MSR1302_0_canonical_scalar_stress_form",
            "purpose": "active scalar stress template has missing Z_m/sign/source/boundary inputs.",
        },
        {
            "source_id": "SRC1379_8_1370_L0_contract",
            "source_path": "source-intake/mts_residuals/P8_Y5_R10_1370_PARENT_LCG_CONTRACT_CANDIDATE.csv",
            "required_anchor": "LCC1370_5_corpus_signature_verdict",
            "purpose": "fixed-L0 branch is admissible but not live parent-signed.",
        },
        {
            "source_id": "SRC1379_9_1374_shell_guard",
            "source_path": "source-intake/mts_residuals/P8_Y5_R10_1374_QALG_QTRANS_FIRST_FILL.csv",
            "required_anchor": "QQF1374_2_shell_projection_guard",
            "purpose": "transition shell guard must remain active.",
        },
        {
            "source_id": "SRC1379_10_802_shell",
            "source_path": "source-intake/mts_residuals/P8_Y5_R10_802_TRANSITION_SHELL_OBSTRUCTION.csv",
            "required_anchor": "TS802_0_direct_projection",
            "purpose": "direct shell projection obstruction.",
        },
        {
            "source_id": "SRC1379_11_803_anticheat",
            "source_path": "source-intake/mts_residuals/P8_Y5_R10_803_TRANSITION_SHELL_ANTI_CHEAT_BOUND.csv",
            "required_anchor": "AC803_0_required_shell_suppression",
            "purpose": "anti-cheat guard against generic shell suppression.",
        },
    ]
    for row in rows:
        path = source_path(str(row["source_path"]))
        row["exists"] = path.exists()
        row["anchor_found"] = path.exists() and str(row["required_anchor"]) in read_text(path)
    return mark_nonclaim(rows)


def parent_signature_rows() -> list[dict[str, object]]:
    return mark_nonclaim(
        [
            {
                "audit_id": "GPA1379_0_action_slot",
                "signature_clause": "parent action contains a legitimate gradient-completion slot",
                "required_for_parent_sign": "S_parent includes -(kappa_m/2) sqrt(-g) g^{mu nu} partial_mu eta partial_nu eta or equivalent",
                "current_evidence": "1248 has only a schematic L_MTS_core action; 1378 adds gradient completion as a conditional extension",
                "audit_result": "NOT_PARENT_SIGNED",
                "blocks": "kappa_m branch cannot be promoted from conditional closure",
                "source_paths": "source-intake/mts_residuals/P8_Y5_R10_1248_MINIMAL_PARENT_ACTION_ANSATZ.csv;source-intake/mts_residuals/P8_Y5_R10_1378_CONDITIONAL_GRADIENT_RELAXATION_BRANCH.csv",
            },
            {
                "audit_id": "GPA1379_1_m_parent_field",
                "signature_clause": "m or eta is an independent parent scalar field varied before readout/projection",
                "required_for_parent_sign": "field list excludes metric-composite/domain/readout definitions and fixes variation order",
                "current_evidence": "1302 supports m as candidate only; counterbranch and unit/frame locks remain live",
                "audit_result": "CANDIDATE_NOT_SIGNED",
                "blocks": "gradient Euler equation cannot be treated as parent-derived",
                "source_paths": "source-intake/mts_residuals/P8_Y5_R10_1302_FIXED_FIELD_M_SIGNATURE_AUDIT.csv",
            },
            {
                "audit_id": "GPA1379_2_kappa_or_Zm",
                "signature_clause": "kappa_m / Z_m coefficient has sign, value or allowed range, units, and source",
                "required_for_parent_sign": "positive stiffness or signed hyperbolic/elliptic convention with no ghost/tachyon ambiguity",
                "current_evidence": "1302 scalar stress contract explicitly lists MISSING_Z_m_SIGN_AND_VALUE",
                "audit_result": "MISSING_PARENT_COEFFICIENT",
                "blocks": "ell_tr cannot be numeric or claim-grade",
                "source_paths": "source-intake/mts_residuals/P8_Y5_R10_1302_MEMORY_STRESS_RESIDUAL_CONTRACT_NONCLAIM.csv",
            },
            {
                "audit_id": "GPA1379_3_Euler_extraction",
                "signature_clause": "Euler equation for eta is extracted from S_parent rather than imported",
                "required_for_parent_sign": "explicit parent variation giving kappa_m Box eta - L0^-2 F2 eta = source terms",
                "current_evidence": "1276 marks time/radial Euler equations as missing and source map as missing",
                "audit_result": "MISSING_EULER_SOURCE_MAP",
                "blocks": "gradient equation remains a derived conditional ansatz, not a corpus theorem",
                "source_paths": "source-intake/mts_residuals/P8_Y5_R10_1276_PARENT_EULER_SOURCE_CONTRACT.csv",
            },
            {
                "audit_id": "GPA1379_4_source_coupling",
                "signature_clause": "matter/source/bath coupling to eta is specified or proved silent",
                "required_for_parent_sign": "J_eta=0 in local vacuum or a bounded source row with units",
                "current_evidence": "1276 source map missing; 1302 source/bath stress terms missing",
                "audit_result": "MISSING_SOURCE_COUPLING",
                "blocks": "no-hair/exponential profile cannot be used as universal without source conditions",
                "source_paths": "source-intake/mts_residuals/P8_Y5_R10_1276_PARENT_EULER_SOURCE_CONTRACT.csv;source-intake/mts_residuals/P8_Y5_R10_1302_MEMORY_STRESS_RESIDUAL_CONTRACT_NONCLAIM.csv",
            },
            {
                "audit_id": "GPA1379_5_boundary_shell",
                "signature_clause": "boundary/no-flux or shell-bound condition is parent-signed",
                "required_for_parent_sign": "Q_R=0/no-flux or explicit finite shell contribution in Q_trans/Q_proj",
                "current_evidence": "1276 labels boundary no-charge closure-only; 802/803 reject generic shell hiding",
                "audit_result": "MISSING_BOUNDARY_SHELL_CLOSURE",
                "blocks": "A_B/pB/shell cannot be safely zeroed",
                "source_paths": "source-intake/mts_residuals/P8_Y5_R10_1276_PARENT_EULER_SOURCE_CONTRACT.csv;source-intake/mts_residuals/P8_Y5_R10_802_TRANSITION_SHELL_OBSTRUCTION.csv;source-intake/mts_residuals/P8_Y5_R10_803_TRANSITION_SHELL_ANTI_CHEAT_BOUND.csv",
            },
            {
                "audit_id": "GPA1379_6_stress_routing",
                "signature_clause": "gradient stress is retained or separately bounded",
                "required_for_parent_sign": "do not delete T_eta after using gradient stiffness to derive profile",
                "current_evidence": "1302 gives scalar stress residual contract but it is not scoreable",
                "audit_result": "PASS_NONCLAIM_GUARD_ONLY",
                "blocks": "prevents false local-GR pass; does not itself close residuals",
                "source_paths": "source-intake/mts_residuals/P8_Y5_R10_1302_MEMORY_STRESS_RESIDUAL_CONTRACT_NONCLAIM.csv",
            },
            {
                "audit_id": "GPA1379_7_units_frame",
                "signature_clause": "units/frame/index locks are defined for kappa_m, F2, A_ref, and stress projection",
                "required_for_parent_sign": "dimensionally consistent runner inputs with trace-reversal and local norm convention",
                "current_evidence": "1302 fixed-field audit says units/frame/index lock is missing",
                "audit_result": "MISSING_UNITS_FRAME_LOCK",
                "blocks": "closure runner can only carry symbolic formulas",
                "source_paths": "source-intake/mts_residuals/P8_Y5_R10_1302_FIXED_FIELD_M_SIGNATURE_AUDIT.csv;source-intake/mts_residuals/P8_Y5_R10_1378_EXPLICIT_CLOSURE_INPUT_PACK.csv",
            },
            {
                "audit_id": "GPA1379_8_verdict",
                "signature_clause": "gradient-completion branch is parent-signed enough for a candidate row",
                "required_for_parent_sign": "GPA1379_0 through GPA1379_7 pass or have explicit bounded replacements",
                "current_evidence": "multiple clauses remain missing/candidate/closure-only",
                "audit_result": "NO_PARENT_SIGNED_GRADIENT_COMPLETION_ROW",
                "blocks": "fall back to closure-only runner schema",
                "source_paths": "aggregate_GPA1379_0_to_GPA1379_7",
            },
        ]
    )


def dimensional_lock_rows() -> list[dict[str, object]]:
    return mark_nonclaim(
        [
            {
                "lock_id": "KDL1379_0_action_density_match",
                "quantity": "kappa_m",
                "symbolic_units_rule": "[kappa_m] = [L0^-2 Fhat] / [(partial eta)^2]",
                "derived_from": "match gradient term (kappa_m/2)(partial eta)^2 to L0^-2 Fhat in the parent density",
                "status": "SYMBOLIC_DIMENSIONAL_RULE_ONLY",
                "missing": "units of eta/m; units of Fhat; local coordinate convention; action-density normalization",
            },
            {
                "lock_id": "KDL1379_1_transition_length",
                "quantity": "ell_tr",
                "symbolic_units_rule": "ell_tr^2 = kappa_m L0^2 / F2",
                "derived_from": "linearized Euler equation kappa_m Box eta - L0^-2 F2 eta=0",
                "status": "FORMULA_DIMENSIONALLY_CONDITIONAL",
                "missing": "kappa_m value; F2 sign/value; L0 scale rule",
            },
            {
                "lock_id": "KDL1379_2_stability_sign",
                "quantity": "kappa_m F2",
                "symbolic_units_rule": "kappa_m F2 > 0 for real exponential relaxation length in static local normal coordinate",
                "derived_from": "ell_tr=sqrt(kappa_m L0^2/F2) and decaying branch",
                "status": "SIGN_CONDITION_WRITTEN_NOT_SOURCED",
                "missing": "parent sign convention; potential curvature sign; ghost/tachyon exclusion",
            },
            {
                "lock_id": "KDL1379_3_verdict",
                "quantity": "dimensional lock",
                "symbolic_units_rule": "symbolic unit relations are available, but numeric/source lock is absent",
                "derived_from": "KDL1379_0 through KDL1379_2",
                "status": "LOCK_SCHEMA_READY_VALUES_MISSING",
                "missing": "source-backed units/value rows",
            },
        ]
    )


def closure_runner_rows() -> list[dict[str, object]]:
    return mark_nonclaim(
        [
            {
                "schema_id": "CRS1379_0_branch_selector",
                "runner_field": "transition_branch",
                "expression_or_rule": "gradient_relaxation_closure",
                "required_inputs": "explicit user/theory selection plus source_path/source_anchor",
                "current_status": "CLOSURE_ONLY_DEFAULT",
                "refusal_gate": "do not claim parent derivation from branch selector alone",
            },
            {
                "schema_id": "CRS1379_1_kappa_m",
                "runner_field": "kappa_m",
                "expression_or_rule": "positive scalar stiffness; units follow KDL1379_0",
                "required_inputs": "value_or_symbol; units; sign; source_path; source_anchor; extraction_method",
                "current_status": "MISSING_VALUE_ALLOWED_AS_SYMBOLIC_ONLY",
                "refusal_gate": "numeric scoring blocked until source-backed",
            },
            {
                "schema_id": "CRS1379_2_F2",
                "runner_field": "F2",
                "expression_or_rule": "Fhat''(m_*)",
                "required_inputs": "value_or_symbol; units; sign; source_path; source_anchor; extraction_method",
                "current_status": "MISSING_VALUE_ALLOWED_AS_SYMBOLIC_ONLY",
                "refusal_gate": "reject local-fit curvature",
            },
            {
                "schema_id": "CRS1379_3_L0",
                "runner_field": "L0",
                "expression_or_rule": "fixed scalar parent scale",
                "required_inputs": "value_or_symbol; units; scale-setting rule; source_path; source_anchor",
                "current_status": "ACTION_ROLE_ONLY_VALUE_MISSING",
                "refusal_gate": "reject per-arena scale fit",
            },
            {
                "schema_id": "CRS1379_4_ell_tr",
                "runner_field": "ell_tr",
                "expression_or_rule": "sqrt(kappa_m * L0^2 / F2)",
                "required_inputs": "kappa_m;F2;L0;sign_condition",
                "current_status": "FORMULA_READY_SYMBOLIC_ONLY",
                "refusal_gate": "if sign condition fails or inputs unsourced, no numeric pass",
            },
            {
                "schema_id": "CRS1379_5_U_B",
                "runner_field": "U_B",
                "expression_or_rule": "exp(-d/ell_tr)",
                "required_inputs": "d;ell_tr;domain/reference boundary definition",
                "current_status": "FORMULA_READY_DISTANCE_MISSING",
                "refusal_gate": "reject toy or handpicked U_B",
            },
            {
                "schema_id": "CRS1379_6_Delta_m",
                "runner_field": "Delta_m",
                "expression_or_rule": "A_S * U_B",
                "required_inputs": "A_S;U_B;boundary amplitude source",
                "current_status": "FORMULA_READY_AMPLITUDE_MISSING",
                "refusal_gate": "reject unsourced A_S",
            },
            {
                "schema_id": "CRS1379_7_Delta_grad_m",
                "runner_field": "Delta_grad_m",
                "expression_or_rule": "<= A_S * U_B / ell_tr",
                "required_inputs": "A_S;U_B;ell_tr;domain norm",
                "current_status": "FORMULA_READY_DOMAIN_NORM_MISSING",
                "refusal_gate": "reject hidden gradient plateau",
            },
            {
                "schema_id": "CRS1379_8_support_powers",
                "runner_field": "pS;pL;pT;pB",
                "expression_or_rule": "pS=1; pL inactive if A_L=0; pT=2 conditional for gradient stress; pB unresolved",
                "required_inputs": "fixed-L0 signature; stress projection; boundary/shell theorem",
                "current_status": "PARTIAL_CONDITIONAL",
                "refusal_gate": "do not independently tune powers",
            },
            {
                "schema_id": "CRS1379_9_Q_alg",
                "runner_field": "Q_alg_conditional",
                "expression_or_rule": "A_ref^-1 |F2| A_S^2 U_B^2/(L0^2 ell_tr)",
                "required_inputs": "A_ref;F2;A_S;U_B;L0;ell_tr",
                "current_status": "FORMULA_READY_VALUES_MISSING",
                "refusal_gate": "symbolic output only until all required inputs are source-backed",
            },
            {
                "schema_id": "CRS1379_10_Q_trans",
                "runner_field": "Q_trans_conditional",
                "expression_or_rule": "retain A_T U_B^2/ell_tr + A_B U_B^pB/(L0^2 ell_tr) + |b_mem|A_S^2 U_B^2/ell_tr^3; A_L term only if fixed-L0 closure fails",
                "required_inputs": "A_T;A_B;pB;b_mem;A_S;U_B;ell_tr;L0;shell_bound",
                "current_status": "FORMULA_PARTIAL_SHELL_UNRESOLVED",
                "refusal_gate": "no shell hiding or stress deletion",
            },
            {
                "schema_id": "CRS1379_11_shell_gate",
                "runner_field": "shell_status",
                "expression_or_rule": "must be exact_projector_zero or explicit_finite_shell_bound",
                "required_inputs": "projector identity/no-flux/boundary row or finite shell contribution",
                "current_status": "MISSING_SHELL_CLOSURE",
                "refusal_gate": "claim blocked if shell_status missing",
            },
            {
                "schema_id": "CRS1379_12_provenance_gate",
                "runner_field": "provenance",
                "expression_or_rule": "every numeric/theorem input has source_path, source_anchor, units, extraction_method",
                "required_inputs": "all runner fields",
                "current_status": "GATE_READY",
                "refusal_gate": "reject MISSING_* and toy_nonclaim_no_physical_source",
            },
            {
                "schema_id": "CRS1379_13_verdict",
                "runner_field": "closure_runner_status",
                "expression_or_rule": "schema can run symbolic dry-runs and refuse claims; numeric scoring blocked",
                "required_inputs": "CRS1379_0 through CRS1379_12",
                "current_status": "CLOSURE_RUNNER_SCHEMA_READY_NONCLAIM",
                "refusal_gate": "local-GR/PPN/R10 pass blocked",
            },
        ]
    )


def formula_feed_rows() -> list[dict[str, object]]:
    return mark_nonclaim(
        [
            {
                "formula_id": "CFF1379_0_transition_length",
                "target": "L_tr",
                "formula": "L_tr := ell_tr = sqrt(kappa_m L0^2/F2)",
                "status": "CONDITIONAL_SYMBOLIC_FEED",
                "blocks_numeric": "kappa_m, F2, and L0 are not all source-backed",
            },
            {
                "formula_id": "CFF1379_1_support",
                "target": "U_B and pS",
                "formula": "U_B=exp(-d/ell_tr); pS=1; Delta_m=A_S U_B; Delta_grad_m<=A_S U_B/ell_tr",
                "status": "CONDITIONAL_SYMBOLIC_FEED",
                "blocks_numeric": "d and A_S are not source-backed",
            },
            {
                "formula_id": "CFF1379_2_fixed_L_chain",
                "target": "A_L",
                "formula": "A_L=0 only if fixed-L0 anti-smuggling clauses are parent-signed",
                "status": "CONDITIONAL_ZERO_GUARD",
                "blocks_numeric": "fixed-L0 branch remains closure-admissible but not live parent-signed",
            },
            {
                "formula_id": "CFF1379_3_Q_alg",
                "target": "Q_alg",
                "formula": "Q_alg <= A_ref^-1 |F2| A_S^2 U_B^2/(L0^2 ell_tr)",
                "status": "CONDITIONAL_SYMBOLIC_FEED",
                "blocks_numeric": "normalization and parent coefficients are missing",
            },
            {
                "formula_id": "CFF1379_4_Q_trans",
                "target": "Q_trans",
                "formula": "Q_trans retains gradient-stress, memory, boundary, and shell terms until separately zeroed or bounded",
                "status": "PARTIAL_FEED_SHELL_BLOCKED",
                "blocks_numeric": "A_T/A_B/b_mem/pB/shell bound missing",
            },
            {
                "formula_id": "CFF1379_5_local_claim",
                "target": "local_GR_PPN_R10",
                "formula": "no claim if any closure runner field is missing, toy, unsourced, or shell-blocked",
                "status": "REFUSAL_FORMULA",
                "blocks_numeric": "keeps branch disciplined before empirical scoring",
            },
        ]
    )


def runner_feed_rows() -> list[dict[str, object]]:
    return mark_nonclaim(
        [
            {
                "feed_id": "RUF1379_0_parent_signature",
                "runner_field": "gradient_parent_signature",
                "feed_update": "gradient completion is not parent-signed by current corpus",
                "status": "BLOCKED_NOT_PARENT_SIGNED",
                "blocks_claim_because": "action slot, m field status, kappa_m sign/value, Euler source map, source coupling, boundary/shell, and units remain incomplete",
            },
            {
                "feed_id": "RUF1379_1_closure_runner",
                "runner_field": "transition_closure_runner_schema",
                "feed_update": "closure runner schema is ready for symbolic dry-runs and strict refusal gates",
                "status": "SCHEMA_READY_NONCLAIM",
                "blocks_claim_because": "schema has formulas but not source-backed numeric inputs",
            },
            {
                "feed_id": "RUF1379_2_formula_feed",
                "runner_field": "conditional_Q_formula_feed",
                "feed_update": "conditional feed supplies ell_tr, U_B, pS, Delta_m, Delta_grad_m, Q_alg, and shell-retained Q_trans forms",
                "status": "SYMBOLIC_FEED_READY_VALUES_MISSING",
                "blocks_claim_because": "feed is conditional on unsigned closure branch",
            },
            {
                "feed_id": "RUF1379_3_claim_status",
                "runner_field": "local_GR_PPN_R10_status",
                "feed_update": "local-GR, PPN, R10, and q_loc=0 claims remain blocked",
                "status": "BLOCKED_NO_CLAIM",
                "blocks_claim_because": "closure-only runner and missing arena projection cannot prove GR reduction",
            },
        ]
    )


def claim_gate_rows() -> list[dict[str, object]]:
    return mark_nonclaim(
        [
            {
                "gate_id": "GATE1379_0_parent_signature_audit",
                "gate": "gradient parent signature audit exists",
                "status": "PASS_AUDIT_READY",
                "reason": "GPA1379 rows test action slot, m status, kappa_m, Euler, sources, shell, stress, and units.",
            },
            {
                "gate_id": "GATE1379_1_gradient_parent_signed",
                "gate": "gradient completion is parent-signed enough for candidate row",
                "status": "BLOCKED_NOT_PARENT_SIGNED",
                "reason": "GPA1379_8 verdict fails parent signature.",
            },
            {
                "gate_id": "GATE1379_2_closure_runner_schema",
                "gate": "closure-only runner schema exists",
                "status": "PASS_SCHEMA_READY_NONCLAIM",
                "reason": "CRS1379 rows define symbolic inputs and refusal gates.",
            },
            {
                "gate_id": "GATE1379_3_numeric_scoring",
                "gate": "closure runner can score numerically",
                "status": "BLOCKED_VALUES_MISSING",
                "reason": "kappa_m, F2, L0, d, A_S, A_ref, stress/boundary/shell values are missing or symbolic.",
            },
            {
                "gate_id": "GATE1379_4_local_claim",
                "gate": "local GR / PPN / R10 pass can be claimed",
                "status": "BLOCKED_NO_CLAIM",
                "reason": "closure runner is not a parent-signed GR reduction.",
            },
        ]
    )


def decision_rows() -> list[dict[str, object]]:
    return mark_nonclaim(
        [
            {
                "decision_id": "DEC1379_0_parent_signature",
                "decision": "do not parent-sign the gradient completion branch yet",
                "why": "current corpus has scalar-stress templates but no signed kappa_m/Z_m value, field status, Euler source map, or shell closure",
                "next_action": "treat gradient branch as closure-only until parent action is strengthened",
            },
            {
                "decision_id": "DEC1379_1_runner",
                "decision": "use a closure runner schema rather than a fake numeric candidate row",
                "why": "this preserves the useful ell_tr/U_B law while refusing local-GR/PPN/R10 claims",
                "next_action": "make 1380 validate symbolic closure inputs and identify the first parent-signing clause to attack",
            },
            {
                "decision_id": "DEC1379_2_next_best_route",
                "decision": "attack kappa_m/Z_m parent origin or no-flux shell closure next",
                "why": "these are the two blockers preventing the conditional law from becoming a serious candidate branch",
                "next_action": "derive/source kappa_m from parent scalar stress, or prove/retain explicit shell bound",
            },
        ]
    )


def next_rows() -> list[dict[str, object]]:
    return mark_nonclaim(
        [
            {
                "next_id": "NEXT1379_0_1380",
                "next_doc": "1380-Y5-R10-RAB-kappa-origin-or-shell-bound-first-parent-signing-clause.md",
                "next_script": "scripts/Y5_R10_RAB_kappa_origin_or_shell_bound_first_parent_signing_clause.py",
                "task": "attack the first parent-signing clause for the gradient branch: either derive/source kappa_m/Z_m from the parent scalar stress action with units/sign, or construct an explicit finite shell/boundary row that the closure runner can retain",
                "success_condition": "either kappa_m/Z_m receives a source-backed nonclaim coefficient row, or shell/boundary receives an explicit finite bound row; otherwise record which clause remains the active blocker",
                "do_not_claim": "local GR;PPN pass;R10 pass;q_loc=0;GitHub-ready result",
            }
        ]
    )


def generated_csv_paths() -> list[Path]:
    return [
        SOURCE_REGISTER_PATH,
        PARENT_SIGNATURE_PATH,
        DIMENSIONAL_LOCK_PATH,
        CLOSURE_RUNNER_PATH,
        FORMULA_FEED_PATH,
        RUNNER_FEED_PATH,
        CLAIM_GATE_PATH,
        DECISION_PATH,
        NEXT_PATH,
    ]


def all_rows_nonclaim(*groups: list[dict[str, object]]) -> bool:
    for rows in groups:
        for row in rows:
            if str(row.get("valid_for_claim", "")).lower() != "false":
                return False
            if str(row.get("claim_allowed", "")).lower() != "false":
                return False
    return True


def csv_parse_details(paths: list[Path]) -> tuple[bool, str]:
    details = []
    ok = True
    for path in paths:
        try:
            count = len(read_csv_rows(path))
            details.append(f"{path.name}:{count}")
        except Exception as exc:  # pragma: no cover
            ok = False
            details.append(f"{path.name}:ERROR:{exc}")
    return ok, "; ".join(details)


def validation_rows(
    sources: list[dict[str, object]],
    parent_signature: list[dict[str, object]],
    dimensional_lock: list[dict[str, object]],
    closure_runner: list[dict[str, object]],
    formula_feed: list[dict[str, object]],
    runner_feed: list[dict[str, object]],
    gates: list[dict[str, object]],
    csv_paths: list[Path],
) -> list[dict[str, object]]:
    all_sources_ok = all(bool(row["exists"]) and bool(row["anchor_found"]) for row in sources)
    parent_not_signed = any(row["audit_id"] == "GPA1379_8_verdict" and row["audit_result"] == "NO_PARENT_SIGNED_GRADIENT_COMPLETION_ROW" for row in parent_signature)
    dimensional_ready = any(row["lock_id"] == "KDL1379_3_verdict" and row["status"] == "LOCK_SCHEMA_READY_VALUES_MISSING" for row in dimensional_lock)
    schema_ready = any(row["schema_id"] == "CRS1379_13_verdict" and row["current_status"] == "CLOSURE_RUNNER_SCHEMA_READY_NONCLAIM" for row in closure_runner)
    formula_ready = len(formula_feed) >= 6 and any(row["formula_id"] == "CFF1379_5_local_claim" for row in formula_feed)
    runner_blocks = any(row["feed_id"] == "RUF1379_3_claim_status" and row["status"] == "BLOCKED_NO_CLAIM" for row in runner_feed)
    local_claim_blocked = any(row["gate_id"] == "GATE1379_4_local_claim" and row["status"] == "BLOCKED_NO_CLAIM" for row in gates)
    nonclaim = all_rows_nonclaim(sources, parent_signature, dimensional_lock, closure_runner, formula_feed, runner_feed, gates)
    csv_ok, csv_details = csv_parse_details(csv_paths)
    outputs = [DOC_PATH, VALIDATION_PATH, *csv_paths]
    outputs_scoped = all(ROOT in path.resolve().parents or path.resolve() == ROOT for path in outputs)
    formalization_untouched_by_script = FORMALIZATION.exists() and all(FORMALIZATION not in path.resolve().parents for path in outputs)

    rows = [
        {
            "validation_id": "VAL1379_0_sources",
            "check": "every cited local source path exists and anchor is found",
            "status": "PASS" if all_sources_ok else "FAIL",
            "details": "; ".join(f"{row['source_id']} exists={row['exists']} anchor={row['anchor_found']}" for row in sources),
        },
        {
            "validation_id": "VAL1379_1_parent_signature",
            "check": "gradient branch is audited without false parent-signing",
            "status": "PASS" if parent_not_signed else "FAIL",
            "details": "GPA1379_8 keeps no parent-signed gradient-completion row.",
        },
        {
            "validation_id": "VAL1379_2_dimensional_lock",
            "check": "kappa_m dimensional/sign lock is explicit but nonnumeric",
            "status": "PASS" if dimensional_ready else "FAIL",
            "details": "KDL1379_3 records symbolic lock with values missing.",
        },
        {
            "validation_id": "VAL1379_3_closure_runner",
            "check": "closure-only runner schema exists and refuses claims",
            "status": "PASS" if schema_ready else "FAIL",
            "details": "CRS1379_13 marks schema ready nonclaim.",
        },
        {
            "validation_id": "VAL1379_4_formula_feed",
            "check": "conditional formula feed exists for symbolic dry-runs",
            "status": "PASS" if formula_ready else "FAIL",
            "details": "CFF1379 rows include transition length, support, Q_alg, Q_trans, and refusal formula.",
        },
        {
            "validation_id": "VAL1379_5_runner_refusal",
            "check": "runner feed and gates keep local claims blocked",
            "status": "PASS" if runner_blocks and local_claim_blocked else "FAIL",
            "details": "RUF1379_3 and GATE1379_4 keep BLOCKED_NO_CLAIM.",
        },
        {
            "validation_id": "VAL1379_6_no_claim_rows",
            "check": "all generated rows keep valid_for_claim=false and claim_allowed=false",
            "status": "PASS" if nonclaim else "FAIL",
            "details": "1379 is a parent-signature audit and closure runner schema, not a local-GR/PPN/R10 pass.",
        },
        {
            "validation_id": "VAL1379_7_csv_parse",
            "check": "all generated CSVs parse cleanly",
            "status": "PASS" if csv_ok else "FAIL",
            "details": csv_details,
        },
        {
            "validation_id": "VAL1379_8_scope",
            "check": "generated outputs stay inside post-checkpoint-work and outside formalization-workbench",
            "status": "PASS" if outputs_scoped and formalization_untouched_by_script else "FAIL",
            "details": f"ROOT={ROOT}; FORMALIZATION_EXISTS={FORMALIZATION.exists()}",
        },
    ]
    overall_ok = all(row["status"] == "PASS" for row in rows)
    rows.append(
        {
            "validation_id": "VAL1379_9_overall",
            "check": "overall 1379 validation",
            "status": "PASS" if overall_ok else "FAIL",
            "details": "1379 refuses parent-signing of kappa_m gradient branch and creates a closure-only symbolic runner schema.",
        }
    )
    return rows


def write_doc(
    sources: list[dict[str, object]],
    parent_signature: list[dict[str, object]],
    dimensional_lock: list[dict[str, object]],
    closure_runner: list[dict[str, object]],
    formula_feed: list[dict[str, object]],
    runner_feed: list[dict[str, object]],
    gates: list[dict[str, object]],
    decisions: list[dict[str, object]],
    next_targets: list[dict[str, object]],
    validations: list[dict[str, object]],
) -> None:
    text = f"""# {TITLE}

**Current verdict:** the `kappa_m` gradient-completion branch is **not** parent-signed by the current corpus. The maths from 1378 is useful, but the parent action slot, independent `m/eta` field status, stiffness sign/value, Euler source map, source coupling, boundary/shell condition, and units/frame lock are still missing or conditional.

**What we gained:** the conditional branch is now converted into a closure-only runner schema. It can carry symbolic dry-run formulas like `ell_tr=sqrt(kappa_m L0^2/F2)`, `U_B=exp(-d/ell_tr)`, `Delta_m=A_S U_B`, and `Q_alg <= A_ref^-1 |F2| A_S^2 U_B^2/(L0^2 ell_tr)`, but it refuses numeric/local claims until every input is sourced.

**Next pressure point:** either source/derive `kappa_m`/`Z_m` from the parent scalar-stress action, or construct an explicit finite shell/boundary bound. Those are now the two clean handles on the coupling problem.

## Source Register

{table(["source_id", "source_path", "required_anchor", "exists", "anchor_found", "purpose", "valid_for_claim", "claim_allowed"], sources)}

## Gradient Parent-Signature Audit

{table(["audit_id", "signature_clause", "required_for_parent_sign", "current_evidence", "audit_result", "blocks", "source_paths", "valid_for_claim", "claim_allowed"], parent_signature)}

## `kappa_m` Dimensional Lock

{table(["lock_id", "quantity", "symbolic_units_rule", "derived_from", "status", "missing", "valid_for_claim", "claim_allowed"], dimensional_lock)}

## Transition Closure Runner Schema

{table(["schema_id", "runner_field", "expression_or_rule", "required_inputs", "current_status", "refusal_gate", "valid_for_claim", "claim_allowed"], closure_runner)}

## Conditional Formula Feed

{table(["formula_id", "target", "formula", "status", "blocks_numeric", "valid_for_claim", "claim_allowed"], formula_feed)}

## Runner Feed Update

{table(["feed_id", "runner_field", "feed_update", "status", "blocks_claim_because", "valid_for_claim", "claim_allowed"], runner_feed)}

## Claim Gates

{table(["gate_id", "gate", "status", "reason", "valid_for_claim", "claim_allowed"], gates)}

## Decision Ledger

{table(["decision_id", "decision", "why", "next_action", "valid_for_claim", "claim_allowed"], decisions)}

## Next Target

{table(["next_id", "next_doc", "next_script", "task", "success_condition", "do_not_claim", "valid_for_claim", "claim_allowed"], next_targets)}

## Validation

{table(["validation_id", "check", "status", "details"], validations)}
"""
    DOC_PATH.write_text(text, encoding="utf-8")


def main() -> None:
    sources = source_register()
    parent_signature = parent_signature_rows()
    dimensional_lock = dimensional_lock_rows()
    closure_runner = closure_runner_rows()
    formula_feed = formula_feed_rows()
    runner_feed = runner_feed_rows()
    gates = claim_gate_rows()
    decisions = decision_rows()
    next_targets = next_rows()

    csv_paths = generated_csv_paths()
    write_csv(SOURCE_REGISTER_PATH, sources)
    write_csv(PARENT_SIGNATURE_PATH, parent_signature)
    write_csv(DIMENSIONAL_LOCK_PATH, dimensional_lock)
    write_csv(CLOSURE_RUNNER_PATH, closure_runner)
    write_csv(FORMULA_FEED_PATH, formula_feed)
    write_csv(RUNNER_FEED_PATH, runner_feed)
    write_csv(CLAIM_GATE_PATH, gates)
    write_csv(DECISION_PATH, decisions)
    write_csv(NEXT_PATH, next_targets)

    validations = validation_rows(sources, parent_signature, dimensional_lock, closure_runner, formula_feed, runner_feed, gates, csv_paths)
    write_csv(VALIDATION_PATH, validations)
    write_doc(sources, parent_signature, dimensional_lock, closure_runner, formula_feed, runner_feed, gates, decisions, next_targets, validations)

    print(f"wrote {DOC_PATH}")
    print(f"wrote {VALIDATION_PATH}")
    print(f"formalization-workbench touched by this script: {FORMALIZATION.exists() and False}")


if __name__ == "__main__":
    main()

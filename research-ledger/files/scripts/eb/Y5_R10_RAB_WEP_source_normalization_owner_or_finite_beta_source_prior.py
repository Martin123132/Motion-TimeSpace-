from __future__ import annotations

import csv
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
SRC_DIR = Path("source-intake/mts_residuals")

DOC_PATH = Path("1403-Y5-R10-RAB-WEP-source-normalization-owner-or-finite-beta-source-prior.md")
SOURCE_REGISTER_PATH = SRC_DIR / "P8_Y5_R10_1403_SOURCE_REGISTER.csv"
OWNER_AUDIT_PATH = SRC_DIR / "P8_Y5_R10_1403_WEP_SOURCE_OWNER_AUDIT.csv"
BETA_PRIOR_PATH = SRC_DIR / "P8_Y5_R10_1403_BETA_SOURCE_TAU_WEP_PRIOR.csv"
PRESSURE_GATE_PATH = SRC_DIR / "P8_Y5_R10_1403_WEP_PRESSURE_GATE.csv"
CLAIM_GATE_PATH = SRC_DIR / "P8_Y5_R10_1403_CLAIM_GATE.csv"
DECISION_LEDGER_PATH = SRC_DIR / "P8_Y5_R10_1403_DECISION_LEDGER.csv"
NEXT_TARGET_PATH = SRC_DIR / "P8_Y5_R10_1403_NEXT_TARGET.csv"
VALIDATION_PATH = SRC_DIR / "P8_Y5_BRR545_1403_VALIDATION.csv"

STATUS = (
    "Y5_R10_1403_WEP_source_normalization_owner_not_derived_"
    "finite_beta_source_tau_WEP_prior_written_nonclaim"
)
CLAIM_CEILING = (
    "WEP_source_owner_or_finite_prior_only_no_WEP_pass_no_clock_transfer_no_R10_transfer_"
    "no_PPN_no_Newton_no_local_GR_pass"
)

SOURCE_ROWS = [
    {
        "source_id": "SRC1403_0_1402_doc",
        "source_path": "1402-Y5-R10-RAB-local-domain-tau-transfer-theorem-or-arena-isolation-ledger.md",
        "required_anchor": "NEXT1402_0_1403",
        "purpose": "handoff selecting WEP source normalization owner or finite prior",
    },
    {
        "source_id": "SRC1403_1_1402_isolation",
        "source_path": "source-intake/mts_residuals/P8_Y5_R10_1402_ARENA_ISOLATION_LEDGER.csv",
        "required_anchor": "ISO1402_1_WEP",
        "purpose": "WEP arena isolated from clock/R10/PPN",
    },
    {
        "source_id": "SRC1403_2_1402_matrix",
        "source_path": "source-intake/mts_residuals/P8_Y5_R10_1402_DOMAIN_TRANSFER_MATRIX.csv",
        "required_anchor": "DTM1402_0_clock_to_WEP",
        "purpose": "clock-to-WEP transfer forbidden without parent theorem",
    },
    {
        "source_id": "SRC1403_3_1401_targets",
        "source_path": "source-intake/mts_residuals/P8_Y5_R10_1401_PRESSURE_TARGET_LEDGER.csv",
        "required_anchor": "PT1401_2_WEP_robust_surface",
        "purpose": "WEP pressure target ledger",
    },
    {
        "source_id": "SRC1403_4_1401_map",
        "source_path": "source-intake/mts_residuals/P8_Y5_R10_1401_RESIDUAL_SOURCE_MAP.csv",
        "required_anchor": "RSM1401_6_WEP",
        "purpose": "WEP residual source map",
    },
    {
        "source_id": "SRC1403_5_988_WEP",
        "source_path": "source-intake/mts_residuals/P8_Y5_R10_988_WEP_ALPHA_PRESSURE_IMPORT.csv",
        "required_anchor": "WEP988_WAS651_2_clock_screen_only",
        "purpose": "alpha-only and robust WEP pressure targets plus clock-screen warning",
    },
    {
        "source_id": "SRC1403_6_989_beta_source",
        "source_path": "source-intake/mts_residuals/P8_Y5_R10_989_BETA_SOURCE_OWNER_LEDGER.csv",
        "required_anchor": "BSO989_3_not_clock_screen",
        "purpose": "beta_source_alpha source owner remains unowned",
    },
    {
        "source_id": "SRC1403_7_988_joint",
        "source_path": "source-intake/mts_residuals/P8_Y5_R10_988_JOINT_ALPHA_VARIABLE_GATE.csv",
        "required_anchor": "JAV988_2_WEP_product",
        "purpose": "WEP product form and clock transfer warning",
    },
    {
        "source_id": "SRC1403_8_1400_vector",
        "source_path": "source-intake/mts_residuals/P8_Y5_R10_1400_FINITE_EM_LOCAL_RESIDUAL_VECTOR.csv",
        "required_anchor": "REM1400_6_WEP",
        "purpose": "finite EM local residual WEP component",
    },
    {
        "source_id": "SRC1403_9_this_script",
        "source_path": "scripts/Y5_R10_RAB_WEP_source_normalization_owner_or_finite_beta_source_prior.py",
        "required_anchor": "STATUS",
        "purpose": "1403 generator",
    },
]


def clean(value: Any) -> str:
    return str(value).replace("\n", " ").strip()


def write_csv(path: Path, rows: list[dict[str, Any]], columns: list[str] | None = None) -> None:
    full_path = ROOT / path
    full_path.parent.mkdir(parents=True, exist_ok=True)
    if columns is None:
        columns = list(rows[0].keys()) if rows else []
    with full_path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=columns)
        writer.writeheader()
        for row in rows:
            writer.writerow({column: clean(row.get(column, "")) for column in columns})


def md_table(rows: list[dict[str, Any]], columns: list[str] | None = None) -> str:
    if not rows:
        return ""
    if columns is None:
        columns = list(rows[0].keys())
    header = "| " + " | ".join(columns) + " |"
    divider = "| " + " | ".join("---" for _ in columns) + " |"
    body = [
        "| " + " | ".join(clean(row.get(column, "")).replace("|", "\\|") for column in columns) + " |"
        for row in rows
    ]
    return "\n".join([header, divider, *body])


def anchor_found(path: Path, anchor: str) -> bool:
    if not path.exists():
        return False
    return anchor in path.read_text(encoding="utf-8", errors="ignore")


def source_register_rows() -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    for source in SOURCE_ROWS:
        source_path = ROOT / source["source_path"]
        rows.append(
            {
                **source,
                "exists": str(source_path.exists()),
                "anchor_found": str(anchor_found(source_path, source["required_anchor"])),
                "valid_for_claim": "False",
                "claim_allowed": "False",
            }
        )
    return rows


def owner_audit_rows() -> list[dict[str, str]]:
    return [
        {
            "audit_id": "WSO1403_0_same_TQ_current",
            "owner_clause": "WEP source current descends from the same T_Q owner as the EM coupling",
            "mathematical_form": "J_Q, charge labels, A_Q coupling, and source/test normalization are one Noether object",
            "current_evidence": "989 leaves charge-current/source normalization unsigned",
            "status": "UNSIGNED",
            "if_closed": "beta_source_alpha cannot float independently",
            "valid_for_claim": "False",
            "claim_allowed": "False",
        },
        {
            "audit_id": "WSO1403_1_tau_WEP_domain",
            "owner_clause": "tau_WEP is generated by a parent local domain map",
            "mathematical_form": "tau_WEP = T_WEP[D_parent(source,test,local lab)]",
            "current_evidence": "1402 says shared tau/domain transfer is not derived",
            "status": "UNSIGNED",
            "if_closed": "WEP pressure can be tied to the finite EM branch without importing clock screen",
            "valid_for_claim": "False",
            "claim_allowed": "False",
        },
        {
            "audit_id": "WSO1403_2_composition_charge_normalization",
            "owner_clause": "WEP composition charges are normalized in the same convention as the EM residual",
            "mathematical_form": "DeltaQ_alpha_AB, binding charges, and b_alpha_EM use one source/test convention",
            "current_evidence": "988 quarantines normalization collisions between rough proxy and DD-style charge",
            "status": "UNSIGNED",
            "if_closed": "WEP alpha-only and robust pressure rows become comparable to the residual vector",
            "valid_for_claim": "False",
            "claim_allowed": "False",
        },
        {
            "audit_id": "WSO1403_3_no_clock_screen",
            "owner_clause": "clock screening is not reused as WEP force-source normalization",
            "mathematical_form": "S_clock does not set beta_source_alpha*tau_WEP unless a parent theorem proves it",
            "current_evidence": "989 BSO989_3 and 1402 isolation ledger explicitly forbid this shortcut",
            "status": "DISCIPLINE_SIGNED_NOT_SOURCE_OWNER",
            "if_closed": "prevents false WEP pass by clock-only suppression",
            "valid_for_claim": "False",
            "claim_allowed": "False",
        },
        {
            "audit_id": "WSO1403_4_binding_term_owner",
            "owner_clause": "surface/binding WEP response is either theorem-zero or source-backed",
            "mathematical_form": "C_WEP_EM includes DeltaQ_alpha beta_source_alpha b_alpha tau_WEP plus binding terms",
            "current_evidence": "robust target exists, but beta_EM/binding map remains missing",
            "status": "UNSIGNED",
            "if_closed": "robust WEP pressure target can be used without hiding beta_EM",
            "valid_for_claim": "False",
            "claim_allowed": "False",
        },
        {
            "audit_id": "WSO1403_5_conditional_zero",
            "owner_clause": "WEP source normalization theorem",
            "mathematical_form": "if WSO1403_0..4 close with no finite source residual, then beta_source_alpha*tau_WEP is theorem-zero or parent-owned",
            "current_evidence": "clauses named but not parent-signed",
            "status": "EXACT_CONDITIONAL_THEOREM_READY_NOT_PROMOTED",
            "if_closed": "WEP finite branch could be demoted or bounded consistently",
            "valid_for_claim": "False",
            "claim_allowed": "False",
        },
        {
            "audit_id": "WSO1403_6_current_verdict",
            "owner_clause": "current WEP source owner status",
            "mathematical_form": "B_WEP := beta_source_alpha*tau_WEP remains finite/nonclaim",
            "current_evidence": "source owner, tau_WEP, composition normalization, and binding map are missing",
            "status": "OWNER_NOT_DERIVED_FINITE_PRIOR_REQUIRED",
            "if_closed": "replace finite prior with theorem-zero/source-owned WEP map",
            "valid_for_claim": "False",
            "claim_allowed": "False",
        },
    ]


def beta_prior_rows() -> list[dict[str, str]]:
    return [
        {
            "prior_id": "BWP1403_0_definition",
            "quantity": "B_WEP := beta_source_alpha*tau_WEP",
            "role": "finite WEP force-source/domain product for the alphaEM branch",
            "formula": "eta_AB_alpha = DeltaQ_alpha_AB * b_alpha_EM * B_WEP",
            "best_available_value": "MISSING_SOURCE_TAU_PRODUCT",
            "source": "1403 definition from 988/989/1401",
            "status": "FINITE_PRIOR_NONCLAIM",
            "valid_for_claim": "False",
            "claim_allowed": "False",
        },
        {
            "prior_id": "BWP1403_1_alpha_only_target",
            "quantity": "|B_WEP| max, alpha-only smoke convention",
            "role": "survival target if b_alpha_EM and tau convention are unit-normalized",
            "formula": "eta_bound/unit_source_eta_prediction",
            "best_available_value": "4.797780522732e-05",
            "source": "P8_Y5_R10_988_WEP_ALPHA_PRESSURE_IMPORT.csv::WEP988_WAS651_0_alpha_Coulomb",
            "status": "TARGET_ONLY_NOT_DERIVED",
            "valid_for_claim": "False",
            "claim_allowed": "False",
        },
        {
            "prior_id": "BWP1403_2_robust_surface_target",
            "quantity": "|B_WEP| max, robust surface-including smoke convention",
            "role": "more conservative survival target if surface/binding channel is retained",
            "formula": "eta_bound/unit_source_eta_prediction",
            "best_available_value": "2.887280314062e-05",
            "source": "P8_Y5_R10_988_WEP_ALPHA_PRESSURE_IMPORT.csv::WEP988_WAS651_1_surface_binding",
            "status": "TARGET_ONLY_NOT_DERIVED",
            "valid_for_claim": "False",
            "claim_allowed": "False",
        },
        {
            "prior_id": "BWP1403_3_clock_transfer_exclusion",
            "quantity": "S_clock -> B_WEP",
            "role": "forbidden shortcut",
            "formula": "B_WEP != S_clock unless parent theorem proves equality",
            "best_available_value": "FORBIDDEN_BY_1402_ISOLATION",
            "source": "P8_Y5_R10_1402_DOMAIN_TRANSFER_MATRIX.csv::DTM1402_0_clock_to_WEP",
            "status": "TRANSFER_FORBIDDEN",
            "valid_for_claim": "False",
            "claim_allowed": "False",
        },
        {
            "prior_id": "BWP1403_4_binding_guard",
            "quantity": "B_WEP robust binding guard",
            "role": "prevents alpha-only row from hiding surface/binding response",
            "formula": "use robust target unless beta_EM/binding term is theorem-zero",
            "best_available_value": "2.887280314062e-05 preferred for conservative pressure",
            "source": "P8_Y5_R10_988_WEP_ALPHA_PRESSURE_IMPORT.csv::WEP988_WAS651_1_surface_binding",
            "status": "ROBUST_TARGET_POLICY_NONCLAIM",
            "valid_for_claim": "False",
            "claim_allowed": "False",
        },
        {
            "prior_id": "BWP1403_5_local_PPN_guard",
            "quantity": "B_WEP -> local PPN",
            "role": "forbidden local-GR transfer",
            "formula": "delta PPN_i requires A_i projection coefficients, not just WEP target",
            "best_available_value": "MISSING_LOCAL_COMPOSITION_PROJECTION",
            "source": "P8_Y5_R10_1402_DOMAIN_TRANSFER_MATRIX.csv::DTM1402_4_WEP_to_PPN",
            "status": "LOCAL_TRANSFER_BLOCKED",
            "valid_for_claim": "False",
            "claim_allowed": "False",
        },
        {
            "prior_id": "BWP1403_6_verdict",
            "quantity": "B_WEP prior status",
            "role": "finite empirical prior lane",
            "formula": "keep B_WEP explicit until theorem-zero or source-backed",
            "best_available_value": "NONCLAIM_PRIOR_WITH_TARGETS",
            "source": "1403 checkpoint",
            "status": "READY_AS_PRESSURE_PRIOR_NOT_EVIDENCE",
            "valid_for_claim": "False",
            "claim_allowed": "False",
        },
    ]


def pressure_gate_rows() -> list[dict[str, str]]:
    return [
        {
            "gate_id": "WPG1403_0_alpha_only",
            "channel": "alpha/Coulomb WEP",
            "eta_bound": "2.800000e-15",
            "delta_Q_abs": "1.989808886825e-03",
            "unit_source_eta_prediction": "5.836031862511e-11",
            "overshoot_factor": "2.084297e+04",
            "required_abs_B_WEP_max": "4.797780522732e-05",
            "status": "TARGET_ONLY_NOT_PASS",
            "valid_for_claim": "False",
            "claim_allowed": "False",
        },
        {
            "gate_id": "WPG1403_1_robust_surface",
            "channel": "surface/binding WEP",
            "eta_bound": "2.800000e-15",
            "delta_Q_abs": "3.306456347405e-03",
            "unit_source_eta_prediction": "9.697707515141e-11",
            "overshoot_factor": "3.463467e+04",
            "required_abs_B_WEP_max": "2.887280314062e-05",
            "status": "TARGET_ONLY_NOT_PASS",
            "valid_for_claim": "False",
            "claim_allowed": "False",
        },
        {
            "gate_id": "WPG1403_2_owner_gate",
            "channel": "WEP source owner",
            "eta_bound": "not_applicable",
            "delta_Q_abs": "not_applicable",
            "unit_source_eta_prediction": "not_applicable",
            "overshoot_factor": "not_applicable",
            "required_abs_B_WEP_max": "must be theorem-zero or source-backed",
            "status": "BLOCKED_SOURCE_OWNER_MISSING",
            "valid_for_claim": "False",
            "claim_allowed": "False",
        },
        {
            "gate_id": "WPG1403_3_tau_gate",
            "channel": "tau_WEP domain",
            "eta_bound": "not_applicable",
            "delta_Q_abs": "not_applicable",
            "unit_source_eta_prediction": "not_applicable",
            "overshoot_factor": "not_applicable",
            "required_abs_B_WEP_max": "must define tau_WEP before scoring",
            "status": "BLOCKED_TAU_WEP_MISSING",
            "valid_for_claim": "False",
            "claim_allowed": "False",
        },
        {
            "gate_id": "WPG1403_4_verdict",
            "channel": "WEP finite EM branch",
            "eta_bound": "2.800000e-15 reference pressure",
            "delta_Q_abs": "channel-dependent",
            "unit_source_eta_prediction": "unit source fails both smoke channels",
            "overshoot_factor": "2.084297e+04 to 3.463467e+04",
            "required_abs_B_WEP_max": "4.797780522732e-05 alpha-only; 2.887280314062e-05 robust",
            "status": "WEP_PRESSURE_GATE_WRITTEN_NO_PASS",
            "valid_for_claim": "False",
            "claim_allowed": "False",
        },
    ]


def claim_gate_rows() -> list[dict[str, str]]:
    return [
        {
            "claim_id": "GATE1403_0_owner",
            "claim": "WEP source normalization is parent-owned",
            "status": "BLOCKED_NO_CLAIM",
            "reason": "same-owner current/source geometry and tau_WEP are unsigned",
            "valid_for_claim": "False",
            "claim_allowed": "False",
        },
        {
            "claim_id": "GATE1403_1_WEP_pass",
            "claim": "WEP branch passes",
            "status": "BLOCKED_NO_CLAIM",
            "reason": "pressure targets are numeric but B_WEP is not derived or fitted with claim provenance",
            "valid_for_claim": "False",
            "claim_allowed": "False",
        },
        {
            "claim_id": "GATE1403_2_clock_transfer",
            "claim": "clock product relieves WEP",
            "status": "BLOCKED_NO_CLAIM",
            "reason": "1402 forbids clock-to-WEP transfer without parent theorem",
            "valid_for_claim": "False",
            "claim_allowed": "False",
        },
        {
            "claim_id": "GATE1403_3_R10_or_PPN_transfer",
            "claim": "WEP target relieves R10 or PPN",
            "status": "BLOCKED_NO_CLAIM",
            "reason": "R10 material kernel and local PPN projection coefficients are missing",
            "valid_for_claim": "False",
            "claim_allowed": "False",
        },
        {
            "claim_id": "GATE1403_4_local_GR",
            "claim": "local GR/Newton reduction can be claimed",
            "status": "BLOCKED_NO_CLAIM",
            "reason": "WEP pressure target is not a local-GR proof and R_EM_local remains unbounded",
            "valid_for_claim": "False",
            "claim_allowed": "False",
        },
    ]


def decision_rows() -> list[dict[str, str]]:
    return [
        {
            "decision_id": "DEC1403_0_owner_status",
            "decision": "do not promote WEP source owner",
            "reason": "source normalization, tau_WEP, composition normalization, and binding map are missing",
            "consequence": "retain B_WEP as finite nonclaim prior",
            "valid_for_claim": "False",
            "claim_allowed": "False",
        },
        {
            "decision_id": "DEC1403_1_pressure_policy",
            "decision": "use robust target as conservative pressure lane",
            "reason": "alpha-only target can hide surface/binding response unless beta_EM is theorem-zero",
            "consequence": "2.887280314062e-05 is the conservative survival target for future finite-prior runs",
            "valid_for_claim": "False",
            "claim_allowed": "False",
        },
        {
            "decision_id": "DEC1403_2_next",
            "decision": "attack composition/binding normalization next",
            "reason": "even with B_WEP prior, WEP cannot score until DeltaQ and binding terms share a convention",
            "consequence": "next target 1404",
            "valid_for_claim": "False",
            "claim_allowed": "False",
        },
    ]


def next_target_rows() -> list[dict[str, str]]:
    return [
        {
            "next_id": "NEXT1403_0_1404",
            "target_doc": "1404-Y5-R10-RAB-WEP-composition-binding-normalization-or-material-prior-map.md",
            "target_script": "scripts/Y5_R10_RAB_WEP_composition_binding_normalization_or_material_prior_map.py",
            "task": "derive a common WEP composition/binding charge normalization for alpha/Coulomb and surface/binding channels, or write material prior rows that keep WEP nonclaim",
            "success_condition": "DeltaQ_alpha, surface/binding response, beta_EM, and material conventions are either common-source normalized or explicitly blocked as finite priors",
            "do_not_claim": "WEP pass;clock pass;R10 pass;PPN pass;Newton limit;local GR;lambda_A=0;q_loc=0;GitHub-ready result",
            "valid_for_claim": "False",
            "claim_allowed": "False",
        }
    ]


def validation_rows(
    sources: list[dict[str, str]],
    owner: list[dict[str, str]],
    prior: list[dict[str, str]],
    pressure: list[dict[str, str]],
    gates: list[dict[str, str]],
) -> list[dict[str, str]]:
    source_ok = all(row["exists"] == "True" and row["anchor_found"] == "True" for row in sources)
    owner_blocked = any(
        row["audit_id"] == "WSO1403_6_current_verdict"
        and row["status"] == "OWNER_NOT_DERIVED_FINITE_PRIOR_REQUIRED"
        for row in owner
    )
    conditional_present = any(
        row["audit_id"] == "WSO1403_5_conditional_zero"
        and row["status"] == "EXACT_CONDITIONAL_THEOREM_READY_NOT_PROMOTED"
        for row in owner
    )
    prior_nonclaim = all(row["valid_for_claim"] == "False" and row["claim_allowed"] == "False" for row in prior)
    targets_present = any(row["prior_id"] == "BWP1403_1_alpha_only_target" and row["best_available_value"] == "4.797780522732e-05" for row in prior) and any(row["prior_id"] == "BWP1403_2_robust_surface_target" and row["best_available_value"] == "2.887280314062e-05" for row in prior)
    pressure_nonclaim = all(row["valid_for_claim"] == "False" and row["claim_allowed"] == "False" for row in pressure)
    pressure_blocks = any(row["gate_id"] == "WPG1403_4_verdict" and row["status"] == "WEP_PRESSURE_GATE_WRITTEN_NO_PASS" for row in pressure)
    gates_blocked = all(row["claim_allowed"] == "False" and row["status"] == "BLOCKED_NO_CLAIM" for row in gates)
    output_paths = [
        DOC_PATH,
        SOURCE_REGISTER_PATH,
        OWNER_AUDIT_PATH,
        BETA_PRIOR_PATH,
        PRESSURE_GATE_PATH,
        CLAIM_GATE_PATH,
        DECISION_LEDGER_PATH,
        NEXT_TARGET_PATH,
        VALIDATION_PATH,
    ]
    scope_ok = all("formalization-workbench" not in str(ROOT / path) for path in output_paths)
    all_ok = source_ok and owner_blocked and conditional_present and prior_nonclaim and targets_present and pressure_nonclaim and pressure_blocks and gates_blocked and scope_ok
    now = datetime.now(timezone.utc).isoformat()
    return [
        {
            "check_id": "VAL1403_0_sources",
            "status": "PASS" if source_ok else "FAIL",
            "detail": "all cited source paths exist and anchors are present",
            "generated_utc": now,
        },
        {
            "check_id": "VAL1403_1_owner_audit",
            "status": "PASS" if owner_blocked and conditional_present else "FAIL",
            "detail": "WEP source owner theorem is exact conditional only and not promoted",
            "generated_utc": now,
        },
        {
            "check_id": "VAL1403_2_beta_prior",
            "status": "PASS" if prior_nonclaim and targets_present else "FAIL",
            "detail": "B_WEP finite prior rows include alpha-only and robust targets and remain nonclaim",
            "generated_utc": now,
        },
        {
            "check_id": "VAL1403_3_pressure_gate",
            "status": "PASS" if pressure_nonclaim and pressure_blocks else "FAIL",
            "detail": "WEP pressure gate is written and blocks pass claims",
            "generated_utc": now,
        },
        {
            "check_id": "VAL1403_4_claim_refusal",
            "status": "PASS" if gates_blocked else "FAIL",
            "detail": "WEP, clock-transfer, R10/PPN transfer, and local-GR claims are refused",
            "generated_utc": now,
        },
        {
            "check_id": "VAL1403_5_scope",
            "status": "PASS" if scope_ok else "FAIL",
            "detail": "outputs are confined to post-checkpoint-work paths",
            "generated_utc": now,
        },
        {
            "check_id": "VAL1403_6_overall",
            "status": "PASS" if all_ok else "FAIL",
            "detail": "1403 retains WEP source normalization as finite nonclaim prior with explicit pressure targets",
            "generated_utc": now,
        },
    ]


def write_doc(
    sources: list[dict[str, str]],
    owner: list[dict[str, str]],
    prior: list[dict[str, str]],
    pressure: list[dict[str, str]],
    gates: list[dict[str, str]],
    decisions: list[dict[str, str]],
    next_target: list[dict[str, str]],
    validation: list[dict[str, str]],
) -> None:
    body = f"""# 1403 Y5 R10 RAB: WEP Source Normalization Owner Or Finite Beta Source Prior

Status: `{STATUS}`

Claim ceiling: `{CLAIM_CEILING}`

**Current verdict:** WEP source normalization is not derived. The useful object is now `B_WEP := beta_source_alpha*tau_WEP`, but it remains a finite nonclaim prior rather than a parent-owned suppression.

**Discipline move:** keep the WEP numeric targets as pressure targets only. The alpha-only target is `4.797780522732e-05`; the robust surface/binding target is `2.887280314062e-05`. Neither is a WEP pass without a source owner, tau map, and composition/binding normalization.

## Source Register

{md_table(sources)}

## WEP Source Owner Audit

{md_table(owner)}

## `B_WEP = beta_source_alpha*tau_WEP` Prior

{md_table(prior)}

## WEP Pressure Gate

{md_table(pressure)}

## Claim Gates

{md_table(gates)}

## Decision Ledger

{md_table(decisions)}

## Next Target

{md_table(next_target)}

## Validation

{md_table(validation)}
"""
    (ROOT / DOC_PATH).write_text(body, encoding="utf-8")


def main() -> None:
    sources = source_register_rows()
    owner = owner_audit_rows()
    prior = beta_prior_rows()
    pressure = pressure_gate_rows()
    gates = claim_gate_rows()
    decisions = decision_rows()
    next_target = next_target_rows()
    validation = validation_rows(sources, owner, prior, pressure, gates)

    write_csv(SOURCE_REGISTER_PATH, sources)
    write_csv(OWNER_AUDIT_PATH, owner)
    write_csv(BETA_PRIOR_PATH, prior)
    write_csv(PRESSURE_GATE_PATH, pressure)
    write_csv(CLAIM_GATE_PATH, gates)
    write_csv(DECISION_LEDGER_PATH, decisions)
    write_csv(NEXT_TARGET_PATH, next_target)
    write_csv(VALIDATION_PATH, validation)
    write_doc(sources, owner, prior, pressure, gates, decisions, next_target, validation)

    failed = [row for row in validation if row["status"] != "PASS"]
    if failed:
        raise SystemExit(f"1403 validation failed: {failed}")
    print(STATUS)
    print(ROOT / DOC_PATH)
    print(ROOT / VALIDATION_PATH)


if __name__ == "__main__":
    main()

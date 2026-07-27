from __future__ import annotations

import csv
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
SRC_DIR = Path("source-intake/mts_residuals")

DOC_PATH = Path("1405-Y5-R10-RAB-parent-WEP-material-response-current-or-vector-prior-bound.md")
SOURCE_REGISTER_PATH = SRC_DIR / "P8_Y5_R10_1405_SOURCE_REGISTER.csv"
CURRENT_DERIVATION_PATH = SRC_DIR / "P8_Y5_R10_1405_PARENT_WEP_RESPONSE_CURRENT_DERIVATION.csv"
SECTOR_VECTOR_PATH = SRC_DIR / "P8_Y5_R10_1405_SECTOR_RESPONSE_VECTOR_MAP.csv"
VECTOR_PRIOR_BOUND_PATH = SRC_DIR / "P8_Y5_R10_1405_VECTOR_PRIOR_BOUND_ROWS.csv"
COMMON_OWNER_ZERO_PATH = SRC_DIR / "P8_Y5_R10_1405_COMMON_OWNER_ZERO_GATE.csv"
CLAIM_GATE_PATH = SRC_DIR / "P8_Y5_R10_1405_CLAIM_GATE.csv"
DECISION_LEDGER_PATH = SRC_DIR / "P8_Y5_R10_1405_DECISION_LEDGER.csv"
NEXT_TARGET_PATH = SRC_DIR / "P8_Y5_R10_1405_NEXT_TARGET.csv"
VALIDATION_PATH = SRC_DIR / "P8_Y5_BRR545_1405_VALIDATION.csv"

STATUS = (
    "Y5_R10_1405_parent_WEP_material_response_current_identity_derived_"
    "parent_coefficients_missing_vector_prior_bounds_written_nonclaim"
)
CLAIM_CEILING = (
    "response_current_identity_and_vector_prior_only_no_WEP_pass_no_clock_transfer_"
    "no_R10_transfer_no_PPN_no_Newton_no_local_GR_pass"
)

ETA_BOUND = "2.800000e-15"
DELTA_Q_ALPHA = "-1.989808886825000e-03"
DELTA_Q_SURFACE = "-3.306456347405000e-03"
ALPHA_TARGET = "4.797780522732e-05"
SURFACE_TARGET = "2.887280314062e-05"
CANCELLATION_RATIO = "-6.017949967452794e-01"


def clean(value: Any) -> str:
    return str(value).replace("\n", " ").replace("\r", " ").strip()


def md_cell(value: Any) -> str:
    return clean(value).replace("|", "\\|")


def write_csv(relative_path: Path, rows: list[dict[str, Any]]) -> None:
    path = ROOT / relative_path
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        raise ValueError(f"no rows supplied for {relative_path}")
    fieldnames = list(rows[0].keys())
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow({key: clean(row.get(key, "")) for key in fieldnames})


def md_table(rows: list[dict[str, Any]]) -> str:
    if not rows:
        return ""
    headers = list(rows[0].keys())
    lines = [
        "| " + " | ".join(headers) + " |",
        "| " + " | ".join(["---"] * len(headers)) + " |",
    ]
    for row in rows:
        lines.append("| " + " | ".join(md_cell(row.get(header, "")) for header in headers) + " |")
    return "\n".join(lines)


def anchor_found(relative_path: str, anchor: str) -> bool:
    path = ROOT / relative_path
    if not path.exists():
        return False
    return anchor in path.read_text(encoding="utf-8", errors="ignore")


def source_register_rows() -> list[dict[str, Any]]:
    rows = [
        {
            "source_id": "SRC1405_0_1404_doc",
            "source_path": "1404-Y5-R10-RAB-WEP-composition-binding-normalization-or-material-prior-map.md",
            "anchor": "NEXT1404_0_1405",
            "role": "prior checkpoint selecting parent WEP material response current as next target",
        },
        {
            "source_id": "SRC1405_1_1404_audit",
            "source_path": "source-intake/mts_residuals/P8_Y5_R10_1404_COMPOSITION_BINDING_NORMALIZATION_AUDIT.csv",
            "anchor": "CBN1404_2_parent_coefficients",
            "role": "declares parent material coefficients missing",
        },
        {
            "source_id": "SRC1405_2_1404_material",
            "source_path": "source-intake/mts_residuals/P8_Y5_R10_1404_MATERIAL_PRIOR_MAP.csv",
            "anchor": "MPM1404_7_parent_coefficient_vector",
            "role": "imports missing P_WEP^I vector state",
        },
        {
            "source_id": "SRC1405_3_1404_pressure",
            "source_path": "source-intake/mts_residuals/P8_Y5_R10_1404_WEP_VECTOR_PRESSURE_GATE.csv",
            "anchor": "VPG1404_2_vector_inequality",
            "role": "imports full WEP vector inequality gate",
        },
        {
            "source_id": "SRC1405_4_1404_cancel",
            "source_path": "source-intake/mts_residuals/P8_Y5_R10_1404_ONE_PAIR_CANCELLATION_GUARD.csv",
            "anchor": "OCG1404_0_pair_line",
            "role": "imports one-pair cancellation prohibition",
        },
        {
            "source_id": "SRC1405_5_1394_composition",
            "source_path": "source-intake/mts_residuals/P8_Y5_R10_1394_BULK_MATERIAL_COMPOSITION_MAP.csv",
            "anchor": "MCM1394_6_composition_verdict",
            "role": "source/test sector-fraction decomposition",
        },
        {
            "source_id": "SRC1405_6_1394_inheritance",
            "source_path": "source-intake/mts_residuals/P8_Y5_R10_1394_BINDING_INHERITANCE_PROOF_ATTEMPT.csv",
            "anchor": "BIH1394_5_current_verdict",
            "role": "binding inheritance not closed",
        },
        {
            "source_id": "SRC1405_7_1394_interface",
            "source_path": "source-intake/mts_residuals/P8_Y5_R10_1394_BINDING_TO_BETA_INTERFACE_GATE.csv",
            "anchor": "BTB1394_4_verdict",
            "role": "binding rows must close before scoring",
        },
        {
            "source_id": "SRC1405_8_1395_sector_pack",
            "source_path": "source-intake/mts_residuals/P8_Y5_R10_1395_BINDING_SECTOR_BETA_SOURCE_PACK.csv",
            "anchor": "SBP1395_5_pack_verdict",
            "role": "sector beta source pack remains unfilled",
        },
        {
            "source_id": "SRC1405_9_1079_tensor_contract",
            "source_path": "source-intake/mts_residuals/P8_Y5_R10_1079_MATERIAL_TENSOR_CONTRACT.csv",
            "anchor": "MTC1079_0_basis",
            "role": "basis contract for response current",
        },
        {
            "source_id": "SRC1405_10_1081_basis_attempt",
            "source_path": "source-intake/mts_residuals/P8_Y5_R10_1081_PARENT_WEP_BASIS_DERIVATION_ATTEMPT.csv",
            "anchor": "PB1081_4_verdict",
            "role": "prior parent basis derivation failed",
        },
        {
            "source_id": "SRC1405_11_1068_requirements",
            "source_path": "source-intake/mts_residuals/P8_Y5_R10_1068_MATERIAL_RESPONSE_REQUIREMENTS.csv",
            "anchor": "MAT1068_2_full_tensor",
            "role": "full material tensor still missing",
        },
        {
            "source_id": "SRC1405_12_1402_isolation",
            "source_path": "source-intake/mts_residuals/P8_Y5_R10_1402_ARENA_ISOLATION_LEDGER.csv",
            "anchor": "ISO1402_1_WEP",
            "role": "blocks transfer from WEP to other local arenas",
        },
        {
            "source_id": "SRC1405_13_this_script",
            "source_path": "scripts/Y5_R10_RAB_parent_WEP_material_response_current_or_vector_prior_bound.py",
            "anchor": "STATUS",
            "role": "generator for this checkpoint",
        },
    ]
    for row in rows:
        row["path_exists"] = (ROOT / row["source_path"]).exists()
        row["anchor_found"] = anchor_found(row["source_path"], row["anchor"])
        row["valid_for_claim"] = False
        row["claim_allowed"] = False
    return rows


def current_derivation_rows() -> list[dict[str, Any]]:
    return [
        {
            "derivation_id": "WRC1405_0_matter_action",
            "statement": "For a compact test body A with effective mass m_A(X), S_A=-int m_A(X) ds.",
            "formula": "alpha_A^a := partial ln m_A / partial X_a",
            "status": "STANDARD_WORLDLINE_RESPONSE_IDENTITY",
            "missing_for_claim": "parent field coordinates X_a and normalization of ds/coframe in MTS local limit",
            "consequence": "defines the WEP response current but not its MTS values",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "derivation_id": "WRC1405_1_response_current",
            "statement": "The material response current is the variation of the matter action along the parent local field direction.",
            "formula": "J_A^a = -(delta S_A/dX_a)/int rho_A ds = partial ln m_A / partial X_a = alpha_A^a",
            "status": "LINEAR_RESPONSE_IDENTITY_DERIVED",
            "missing_for_claim": "source-backed parent generator basis and units",
            "consequence": "WEP can be handled as a current problem rather than an ad hoc scalar",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "derivation_id": "WRC1405_2_sector_decomposition",
            "statement": "If m_A=sum_s E_s,A and beta_s^a:=partial ln E_s,A/partial X_a at the background, then alpha_A^a=sum_s f_s,A beta_s^a.",
            "formula": "f_s,A:=E_s,A/m_A ; alpha_A^a=sum_s f_s,A beta_s^a",
            "status": "LINEAR_SECTOR_IDENTITY_DERIVED",
            "missing_for_claim": "real f_s,A, beta_s^a, and uncertainties for all relevant sectors",
            "consequence": "1394/1395 rows become the right skeleton for P_I",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "derivation_id": "WRC1405_3_differential_response",
            "statement": "The differential WEP response is a sector-fraction contrast contracted with sector beta vectors.",
            "formula": "Delta alpha_AB^a=sum_s (f_s,A-f_s,B) beta_s^a",
            "status": "LINEAR_DIFFERENTIAL_IDENTITY_DERIVED",
            "missing_for_claim": "full material tensor Delta f_s,AB and parent beta_s^a values",
            "consequence": "one-pair DeltaQ rows are proxy components, not a parent-complete tensor",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "derivation_id": "WRC1405_4_source_contraction",
            "statement": "A lab WEP signal requires the test differential response to be contracted with the source response and local kernel.",
            "formula": "eta_AB ~= Delta alpha_AB^a K_ab(lambda,lab) alpha_source^b",
            "status": "CONDITIONAL_SIGNAL_FORM_DERIVED",
            "missing_for_claim": "K_ab, alpha_source^b, tau_WEP, range/profile and readout normalization",
            "consequence": "WEP cannot be transferred from clocks/R10 without a domain theorem",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "derivation_id": "WRC1405_5_sector_prior_compression",
            "statement": "Define a sector pressure coefficient P_s by contracting beta_s with the source response and kernel.",
            "formula": "P_s := beta_s^a K_ab alpha_source^b ; eta_AB=sum_s Delta f_s,AB P_s",
            "status": "VECTOR_PRIOR_FORM_DERIVED_NONCLAIM",
            "missing_for_claim": "P_s values or theorem-zero/source-owned derivation",
            "consequence": "1404 P_WEP^I is now tied to a matter-current identity",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "derivation_id": "WRC1405_6_common_owner_zero",
            "statement": "If all sectors share the same parent response beta_s^a=beta_*^a, then alpha_A^a=beta_*^a for all A and Delta alpha_AB^a=0.",
            "formula": "beta_s^a=beta_*^a for all s -> Delta alpha_AB^a=(sum_s Delta f_s,AB) beta_*^a=0",
            "status": "EXACT_CONDITIONAL_WEP_ZERO_LEMMA",
            "missing_for_claim": "proof that electronic, nuclear, EM binding, and other sectors inherit one common owner",
            "consequence": "the clean route is a universal matter-owner theorem, not material tuning",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "derivation_id": "WRC1405_7_current_verdict",
            "statement": "The current identity is derived, but MTS parent coefficients are not filled.",
            "formula": "derived identity yes; predictive P_s no",
            "status": "IDENTITY_DERIVED_PARENT_VALUES_MISSING",
            "missing_for_claim": "beta_s^a, K_ab, alpha_source^b, full Delta f_s,AB",
            "consequence": "write vector-prior bounds and keep WEP/local-GR nonclaim",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]


def sector_vector_rows() -> list[dict[str, Any]]:
    sectors = [
        ("SVP1405_0_alpha", "P_alpha", "alpha/Coulomb proxy sector", DELTA_Q_ALPHA, ALPHA_TARGET, "proxy from 1086/1404", "MISSING_PARENT_VALUE"),
        ("SVP1405_1_surface", "P_surface", "surface/binding proxy sector", DELTA_Q_SURFACE, SURFACE_TARGET, "proxy from 1086/1404", "MISSING_PARENT_VALUE"),
        ("SVP1405_2_electronic", "P_e", "electronic/atomic mass and clock standard sector", "MISSING_DELTA_F_E", "MISSING_BOUND", "1395 beta_e row named only", "MISSING_PARENT_VALUE"),
        ("SVP1405_3_nuclear", "P_nuc", "nuclear binding/composite rest mass sector", "MISSING_DELTA_F_NUC", "MISSING_BOUND", "1395 beta_nuc row named only", "MISSING_PARENT_VALUE"),
        ("SVP1405_4_EM", "P_EM", "EM binding/charge/fine-structure sector", "MISSING_DELTA_F_EM", "MISSING_BOUND", "1395 beta_EM row named only", "MISSING_PARENT_VALUE"),
        ("SVP1405_5_other", "P_other", "other binding/readout guard sector", "MISSING_DELTA_F_OTHER", "MISSING_BOUND", "1395 beta_other guard", "MISSING_PARENT_VALUE"),
    ]
    rows = []
    for row_id, coefficient, sector, material_contrast, pressure_target, source, parent_status in sectors:
        rows.append(
            {
                "sector_id": row_id,
                "coefficient": coefficient,
                "sector": sector,
                "definition": "P_s := beta_s^a K_ab alpha_source^b",
                "material_contrast": material_contrast,
                "pressure_target": pressure_target,
                "source": source,
                "parent_status": parent_status,
                "status": "VECTOR_COMPONENT_NONCLAIM",
                "valid_for_claim": False,
                "claim_allowed": False,
            }
        )
    rows.append(
        {
            "sector_id": "SVP1405_6_vector_verdict",
            "coefficient": "P_vector",
            "sector": "all WEP material response sectors",
            "definition": "eta_AB=sum_s Delta f_s,AB P_s",
            "material_contrast": "MISSING_FULL_DELTA_F_TENSOR",
            "pressure_target": ETA_BOUND,
            "source": "1405 current identity",
            "parent_status": "MISSING_PARENT_VECTOR",
            "status": "VECTOR_MAP_READY_VALUES_MISSING",
            "valid_for_claim": False,
            "claim_allowed": False,
        }
    )
    return rows


def vector_prior_rows() -> list[dict[str, Any]]:
    return [
        {
            "bound_id": "VPB1405_0_alpha_single_component",
            "object": "P_alpha",
            "inequality": f"abs(P_alpha) <= {ALPHA_TARGET} if all other P_s=0",
            "basis": "single-component diagnostic only",
            "status": "TARGET_ONLY_NOT_PASS",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "bound_id": "VPB1405_1_surface_single_component",
            "object": "P_surface",
            "inequality": f"abs(P_surface) <= {SURFACE_TARGET} if all other P_s=0",
            "basis": "single-component diagnostic only",
            "status": "TARGET_ONLY_NOT_PASS",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "bound_id": "VPB1405_2_two_component_pair",
            "object": "P_alpha,P_surface",
            "inequality": f"abs(({DELTA_Q_ALPHA})*P_alpha + ({DELTA_Q_SURFACE})*P_surface) <= {ETA_BOUND}",
            "basis": "Ti/Pt proxy-pair two-component pressure",
            "status": "PAIR_PRESSURE_ONLY_NOT_PARENT_COMPLETE",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "bound_id": "VPB1405_3_no_cancellation",
            "object": "P_surface/P_alpha",
            "inequality": f"P_surface/P_alpha = {CANCELLATION_RATIO} is forbidden as a theory claim",
            "basis": "one-pair cancellation guard",
            "status": "CANCELLATION_FORBIDDEN",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "bound_id": "VPB1405_4_full_vector",
            "object": "P_s full vector",
            "inequality": f"abs(sum_s Delta f_s,AB P_s) <= {ETA_BOUND} for every relevant material pair",
            "basis": "requires full Delta f tensor and all-material/multi-pair evidence",
            "status": "FULL_VECTOR_BOUND_NOT_ACQUIRED",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "bound_id": "VPB1405_5_verdict",
            "object": "WEP vector prior",
            "inequality": "identity derived; bounds remain pressure-only",
            "basis": "parent values and full material tensor missing",
            "status": "VECTOR_PRIOR_BOUNDS_WRITTEN_NO_PASS",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]


def common_owner_zero_rows() -> list[dict[str, Any]]:
    return [
        {
            "gate_id": "COZ1405_0_universal_matter_owner",
            "zero_clause": "all material sectors inherit one local matter owner",
            "formula": "beta_s^a=beta_*^a for every sector s",
            "status": "UNSIGNED",
            "missing": "parent proof for electronic, nuclear, EM binding, and other sectors",
            "consequence": "would theorem-zero WEP differential response",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "gate_id": "COZ1405_1_fraction_sum",
            "zero_clause": "material fractions sum to one for each body",
            "formula": "sum_s f_s,A=1 and sum_s Delta f_s,AB=0",
            "status": "KINEMATIC_IDENTITY_ASSUMED_FOR_DECOMPOSITION",
            "missing": "complete sector basis and mass-energy bookkeeping",
            "consequence": "common beta owner would cancel exactly",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "gate_id": "COZ1405_2_binding_inheritance",
            "zero_clause": "binding sectors do not introduce independent beta_s",
            "formula": "beta_nuc=beta_EM=beta_e=beta_* or binding beta_s=0",
            "status": "UNSIGNED",
            "missing": "1394/1395 binding inheritance not closed",
            "consequence": "binding remains the dangerous non-universal channel",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "gate_id": "COZ1405_3_source_kernel",
            "zero_clause": "source contraction and local kernel do not reintroduce material dependence",
            "formula": "K_ab alpha_source^b is common for the test pair",
            "status": "UNSIGNED",
            "missing": "tau_WEP, K_ab, alpha_source^b",
            "consequence": "cannot score WEP or transfer to PPN",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "gate_id": "COZ1405_4_conditional_result",
            "zero_clause": "if COZ1405_0..3 close, WEP differential response is theorem-zero at linear order",
            "formula": "Delta alpha_AB^a=0 -> eta_AB=0",
            "status": "EXACT_CONDITIONAL_THEOREM_READY_NOT_PROMOTED",
            "missing": "all unsigned clauses above",
            "consequence": "best next derivation target is common matter-owner proof",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "gate_id": "COZ1405_5_current_verdict",
            "zero_clause": "current WEP zero status",
            "formula": "conditional zero exists but is not signed",
            "status": "COMMON_OWNER_ZERO_NOT_PROVED",
            "missing": "universal matter-owner theorem",
            "consequence": "retain vector priors; no WEP pass",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]


def claim_gate_rows() -> list[dict[str, Any]]:
    return [
        {
            "claim_id": "GATE1405_0_current_identity",
            "claim": "parent WEP response-current identity is available",
            "status": "LIMITED_IDENTITY_ONLY_NO_PREDICTION",
            "reason": "variation identity is derived but parent coordinates/coefficient values are missing",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "claim_id": "GATE1405_1_WEP_pass",
            "claim": "WEP branch passes",
            "status": "BLOCKED_NO_CLAIM",
            "reason": "P_s values and full Delta f tensor are missing",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "claim_id": "GATE1405_2_common_owner_zero",
            "claim": "WEP is theorem-zero by common matter owner",
            "status": "BLOCKED_NO_CLAIM",
            "reason": "universal matter-owner theorem is not signed",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "claim_id": "GATE1405_3_transfer",
            "claim": "WEP current identity transfers to clocks, R10, PPN, or orbital tests",
            "status": "BLOCKED_NO_CLAIM",
            "reason": "1402 arena isolation still blocks cross-arena transfer",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "claim_id": "GATE1405_4_local_GR",
            "claim": "local GR/Newton reduction can be claimed",
            "status": "BLOCKED_NO_CLAIM",
            "reason": "WEP current identity does not close q_loc, lambda_A, EM residuals, or PPN projection",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        {
            "decision_id": "DEC1405_0_derivation_credit",
            "decision": "promote the response-current identity as a real derived structure",
            "basis": "variation of worldline/mass matter action gives alpha_A^a and sector decomposition",
            "action": "use eta_AB=sum_s Delta f_s,AB P_s as the WEP working form",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "decision_id": "DEC1405_1_no_prediction",
            "decision": "do not promote WEP prediction/pass",
            "basis": "P_s values, K_ab, source response, and full material tensor are missing",
            "action": "retain explicit vector-prior bound rows",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "decision_id": "DEC1405_2_best_route",
            "decision": "try common matter-owner zero theorem next",
            "basis": "if all sectors share beta_*^a, WEP cancels exactly without pair tuning",
            "action": "derive from quotient-invariant/universal matter action or demote to vector priors",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        {
            "next_id": "NEXT1405_0_1406",
            "target_doc": "1406-Y5-R10-RAB-common-matter-owner-WEP-zero-theorem-or-sector-beta-acquisition.md",
            "target_script": "scripts/Y5_R10_RAB_common_matter_owner_WEP_zero_theorem_or_sector_beta_acquisition.py",
            "task": "prove the common matter-owner theorem beta_s^a=beta_*^a for all material sectors, or acquire explicit sector beta/source rows for the WEP vector prior",
            "success_condition": "either Delta alpha_AB^a=0 follows from a parent universal matter action, or beta_e, beta_nuc, beta_EM, beta_other and K_ab alpha_source^b are explicit nonclaim source rows",
            "do_not_claim": "WEP pass;clock pass;R10 pass;PPN pass;Newton limit;local GR;lambda_A=0;q_loc=0;GitHub-ready result",
            "valid_for_claim": False,
            "claim_allowed": False,
        }
    ]


def validation_rows(
    sources: list[dict[str, Any]],
    derivation: list[dict[str, Any]],
    sectors: list[dict[str, Any]],
    bounds: list[dict[str, Any]],
    zero: list[dict[str, Any]],
    gates: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    now = datetime.now(timezone.utc).isoformat()

    def row(check_id: str, status: bool, detail: str) -> dict[str, Any]:
        return {
            "check_id": check_id,
            "status": "PASS" if status else "FAIL",
            "detail": detail,
            "timestamp_utc": now,
        }

    all_sources_ok = all(r["path_exists"] and r["anchor_found"] for r in sources)
    derivation_ok = (
        any(r["derivation_id"] == "WRC1405_1_response_current" and r["status"] == "LINEAR_RESPONSE_IDENTITY_DERIVED" for r in derivation)
        and any(r["derivation_id"] == "WRC1405_5_sector_prior_compression" for r in derivation)
        and any(r["derivation_id"] == "WRC1405_7_current_verdict" and r["status"] == "IDENTITY_DERIVED_PARENT_VALUES_MISSING" for r in derivation)
        and all(str(r["claim_allowed"]) == "False" for r in derivation)
    )
    sectors_ok = (
        any(r["coefficient"] == "P_alpha" and r["material_contrast"] == DELTA_Q_ALPHA for r in sectors)
        and any(r["coefficient"] == "P_surface" and r["material_contrast"] == DELTA_Q_SURFACE for r in sectors)
        and any(r["coefficient"] == "P_vector" and r["parent_status"] == "MISSING_PARENT_VECTOR" for r in sectors)
        and all(str(r["valid_for_claim"]) == "False" for r in sectors)
    )
    bounds_ok = (
        any(r["bound_id"] == "VPB1405_2_two_component_pair" and ETA_BOUND in r["inequality"] for r in bounds)
        and any(r["bound_id"] == "VPB1405_3_no_cancellation" and CANCELLATION_RATIO in r["inequality"] for r in bounds)
        and any(r["bound_id"] == "VPB1405_5_verdict" and r["status"] == "VECTOR_PRIOR_BOUNDS_WRITTEN_NO_PASS" for r in bounds)
        and all(str(r["claim_allowed"]) == "False" for r in bounds)
    )
    zero_ok = (
        any(r["gate_id"] == "COZ1405_4_conditional_result" and r["status"] == "EXACT_CONDITIONAL_THEOREM_READY_NOT_PROMOTED" for r in zero)
        and any(r["gate_id"] == "COZ1405_5_current_verdict" and r["status"] == "COMMON_OWNER_ZERO_NOT_PROVED" for r in zero)
        and all(str(r["valid_for_claim"]) == "False" for r in zero)
    )
    claims_ok = (
        any(r["claim_id"] == "GATE1405_0_current_identity" and r["status"] == "LIMITED_IDENTITY_ONLY_NO_PREDICTION" for r in gates)
        and all(str(r["claim_allowed"]) == "False" for r in gates)
        and all(("NO_CLAIM" in r["status"]) or r["status"] == "LIMITED_IDENTITY_ONLY_NO_PREDICTION" for r in gates)
    )
    output_paths = [
        DOC_PATH,
        SOURCE_REGISTER_PATH,
        CURRENT_DERIVATION_PATH,
        SECTOR_VECTOR_PATH,
        VECTOR_PRIOR_BOUND_PATH,
        COMMON_OWNER_ZERO_PATH,
        CLAIM_GATE_PATH,
        DECISION_LEDGER_PATH,
        NEXT_TARGET_PATH,
        VALIDATION_PATH,
    ]
    scope_ok = all(str((ROOT / path).resolve()).startswith(str(ROOT.resolve())) for path in output_paths)

    checks = [
        row("VAL1405_0_sources", all_sources_ok, "all cited source paths exist and anchors are present"),
        row("VAL1405_1_current_identity", derivation_ok, "response current and sector vector identities are derived but nonclaim"),
        row("VAL1405_2_sector_vector", sectors_ok, "sector vector map includes alpha/surface proxies and missing parent vector"),
        row("VAL1405_3_vector_bounds", bounds_ok, "vector prior bounds and cancellation refusal are written"),
        row("VAL1405_4_common_owner_zero", zero_ok, "common-owner WEP zero remains exact conditional only"),
        row("VAL1405_5_claim_refusal", claims_ok, "WEP, transfer, and local-GR claims are refused"),
        row("VAL1405_6_scope", scope_ok, "outputs are confined to post-checkpoint-work paths"),
    ]
    overall = all(check["status"] == "PASS" for check in checks)
    checks.append(
        row(
            "VAL1405_7_overall",
            overall,
            "1405 derives the WEP response-current identity and retains finite vector priors without claims",
        )
    )
    return checks


def write_doc(
    sources: list[dict[str, Any]],
    derivation: list[dict[str, Any]],
    sectors: list[dict[str, Any]],
    bounds: list[dict[str, Any]],
    zero: list[dict[str, Any]],
    gates: list[dict[str, Any]],
    decisions: list[dict[str, Any]],
    next_target: list[dict[str, Any]],
    validation: list[dict[str, Any]],
) -> None:
    body = f"""# 1405 — Parent WEP Material Response Current Or Vector Prior Bound

**Status:** `{STATUS}`

**Current verdict:** useful progress. The WEP material-response current identity is derivable: `J_A^a = partial ln m_A / partial X_a`, `alpha_A^a=sum_s f_s,A beta_s^a`, and `eta_AB ~= Delta alpha_AB^a K_ab alpha_source^b`. But the parent values of `beta_s^a`, `K_ab`, `alpha_source^b`, and the full material tensor are still missing.

**Discipline move:** this is a real structural win, not a WEP pass. The branch now has a proper current/vector language; claims remain blocked until the common matter-owner zero theorem is proved or the sector vector `P_s` is source-filled.

**Claim ceiling:** `{CLAIM_CEILING}`

## Source Register

{md_table(sources)}

## Parent WEP Response Current Derivation

{md_table(derivation)}

## Sector Response Vector Map

{md_table(sectors)}

## Vector Prior Bound Rows

{md_table(bounds)}

## Common Owner Zero Gate

{md_table(zero)}

## Claim Gate

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
    derivation = current_derivation_rows()
    sectors = sector_vector_rows()
    bounds = vector_prior_rows()
    zero = common_owner_zero_rows()
    gates = claim_gate_rows()
    decisions = decision_rows()
    next_target = next_target_rows()
    validation = validation_rows(sources, derivation, sectors, bounds, zero, gates)

    write_csv(SOURCE_REGISTER_PATH, sources)
    write_csv(CURRENT_DERIVATION_PATH, derivation)
    write_csv(SECTOR_VECTOR_PATH, sectors)
    write_csv(VECTOR_PRIOR_BOUND_PATH, bounds)
    write_csv(COMMON_OWNER_ZERO_PATH, zero)
    write_csv(CLAIM_GATE_PATH, gates)
    write_csv(DECISION_LEDGER_PATH, decisions)
    write_csv(NEXT_TARGET_PATH, next_target)
    write_csv(VALIDATION_PATH, validation)
    write_doc(sources, derivation, sectors, bounds, zero, gates, decisions, next_target, validation)

    failed = [row for row in validation if row["status"] != "PASS"]
    if failed:
        raise SystemExit(f"1405 validation failed: {failed}")
    print(STATUS)
    print(ROOT / DOC_PATH)
    print(ROOT / VALIDATION_PATH)


if __name__ == "__main__":
    main()

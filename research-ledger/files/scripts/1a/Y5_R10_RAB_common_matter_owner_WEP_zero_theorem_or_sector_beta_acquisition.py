from __future__ import annotations

import csv
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
SRC_DIR = Path("source-intake/mts_residuals")

DOC_PATH = Path("1406-Y5-R10-RAB-common-matter-owner-WEP-zero-theorem-or-sector-beta-acquisition.md")
SOURCE_REGISTER_PATH = SRC_DIR / "P8_Y5_R10_1406_SOURCE_REGISTER.csv"
THEOREM_AUDIT_PATH = SRC_DIR / "P8_Y5_R10_1406_COMMON_MATTER_OWNER_WEP_ZERO_AUDIT.csv"
COUNTERMODEL_PATH = SRC_DIR / "P8_Y5_R10_1406_WEP_OWNER_COUNTERMODEL_LEDGER.csv"
SECTOR_ACQUISITION_PATH = SRC_DIR / "P8_Y5_R10_1406_SECTOR_BETA_SOURCE_ACQUISITION.csv"
ZERO_OR_BOUND_PATH = SRC_DIR / "P8_Y5_R10_1406_ZERO_OR_BOUND_DECISION_GATE.csv"
CLAIM_GATE_PATH = SRC_DIR / "P8_Y5_R10_1406_CLAIM_GATE.csv"
DECISION_LEDGER_PATH = SRC_DIR / "P8_Y5_R10_1406_DECISION_LEDGER.csv"
NEXT_TARGET_PATH = SRC_DIR / "P8_Y5_R10_1406_NEXT_TARGET.csv"
VALIDATION_PATH = SRC_DIR / "P8_Y5_BRR545_1406_VALIDATION.csv"

STATUS = (
    "Y5_R10_1406_common_matter_owner_WEP_zero_exact_conditional_"
    "not_parent_signed_sector_beta_acquisition_written_nonclaim"
)
CLAIM_CEILING = (
    "conditional_common_owner_WEP_zero_or_sector_beta_acquisition_only_no_WEP_pass_"
    "no_clock_transfer_no_R10_transfer_no_PPN_no_Newton_no_local_GR_pass"
)


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
            "source_id": "SRC1406_0_1405_doc",
            "source_path": "1405-Y5-R10-RAB-parent-WEP-material-response-current-or-vector-prior-bound.md",
            "anchor": "NEXT1405_0_1406",
            "role": "prior checkpoint selecting common matter-owner WEP zero theorem as next target",
        },
        {
            "source_id": "SRC1406_1_1405_current",
            "source_path": "source-intake/mts_residuals/P8_Y5_R10_1405_PARENT_WEP_RESPONSE_CURRENT_DERIVATION.csv",
            "anchor": "WRC1405_6_common_owner_zero",
            "role": "imports exact conditional WEP zero lemma from response-current identity",
        },
        {
            "source_id": "SRC1406_2_1405_zero",
            "source_path": "source-intake/mts_residuals/P8_Y5_R10_1405_COMMON_OWNER_ZERO_GATE.csv",
            "anchor": "COZ1405_5_current_verdict",
            "role": "imports current common-owner zero as unproved",
        },
        {
            "source_id": "SRC1406_3_1395_sector_zero",
            "source_path": "source-intake/mts_residuals/P8_Y5_R10_1395_SECTOR_BETA_ZERO_THEOREM_ATTEMPT.csv",
            "anchor": "SBZ1395_5_current_verdict",
            "role": "sector beta zero attempt remains unsigned",
        },
        {
            "source_id": "SRC1406_4_1395_sector_pack",
            "source_path": "source-intake/mts_residuals/P8_Y5_R10_1395_BINDING_SECTOR_BETA_SOURCE_PACK.csv",
            "anchor": "SBP1395_5_pack_verdict",
            "role": "sector beta source pack exists but is not value-filled",
        },
        {
            "source_id": "SRC1406_5_1338_status",
            "source_path": "source-intake/mts_residuals/P8_Y5_R10_1338_COMMON_MODE_THEOREM_STATUS.csv",
            "anchor": "THMSTAT1338_0_no_source_slot",
            "role": "latest common-mode status: NoSourceOnlySpeciesSlot is closure, not derived",
        },
        {
            "source_id": "SRC1406_6_1332_theorem",
            "source_path": "source-intake/mts_residuals/P8_Y5_R10_1332_COMMON_MODE_SOURCE_THEOREM.csv",
            "anchor": "CMT1332_2_countermodel",
            "role": "common-mode theorem and w_A countermodel",
        },
        {
            "source_id": "SRC1406_7_1077_WEP_owner",
            "source_path": "source-intake/mts_residuals/P8_Y5_R10_1077_PARENT_WEP_COUPLING_OWNER_THEOREM_ATTEMPT.csv",
            "anchor": "WCO1077_5_verdict",
            "role": "older parent WEP owner theorem attempt remains not closed",
        },
        {
            "source_id": "SRC1406_8_1079_narrow_current",
            "source_path": "source-intake/mts_residuals/P8_Y5_R10_1079_NARROW_CURRENT_OWNER_THEOREM_ATTEMPT.csv",
            "anchor": "NCO1079_6_verdict",
            "role": "narrow current owner kills post-variation tricks but not pre-variation weights",
        },
        {
            "source_id": "SRC1406_9_1087_descent",
            "source_path": "source-intake/mts_residuals/P8_Y5_R10_1087_PARENT_MATTER_DESCENT_ATTEMPT.csv",
            "anchor": "PMD1087_6_verdict",
            "role": "parent matter descent zero is not signed",
        },
        {
            "source_id": "SRC1406_10_1045_functor",
            "source_path": "source-intake/mts_residuals/P8_Y5_R10_1045_PARENT_MATTER_FUNCTOR_SIGNATURE_AUDIT.csv",
            "anchor": "MFS1045_6_verdict",
            "role": "parent matter functor signature fails current claim",
        },
        {
            "source_id": "SRC1406_11_1310_signature",
            "source_path": "source-intake/mts_residuals/P8_Y5_R10_1310_OWNER_SIGNATURE_REPAIR_ATTEMPT.csv",
            "anchor": "OSA1310_5_verdict",
            "role": "ordinary constant/action owner signature repair still fails",
        },
        {
            "source_id": "SRC1406_12_1402_isolation",
            "source_path": "source-intake/mts_residuals/P8_Y5_R10_1402_ARENA_ISOLATION_LEDGER.csv",
            "anchor": "ISO1402_1_WEP",
            "role": "arena isolation still blocks WEP transfer",
        },
        {
            "source_id": "SRC1406_13_this_script",
            "source_path": "scripts/Y5_R10_RAB_common_matter_owner_WEP_zero_theorem_or_sector_beta_acquisition.py",
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


def theorem_audit_rows() -> list[dict[str, Any]]:
    return [
        {
            "audit_id": "CMO1406_0_observed_frame",
            "required_clause": "all ordinary material sectors couple through one descended observed coframe/metric",
            "mathematical_role": "gives a common ds and Hilbert variation frame for sector energies",
            "current_evidence": "1045/1087/1332 provide the required contract but do not sign the full parent functor",
            "status": "CONDITIONAL_CONTRACT_NOT_PARENT_SIGNED",
            "if_signed": "sector response can be compared in one frame",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "audit_id": "CMO1406_1_single_matter_functional",
            "required_clause": "ordinary matter is one functional S_matter[Psi,e_obs,theta_rep] rather than independent source-weighted pieces",
            "mathematical_role": "prevents species-indexed action weights from entering before variation",
            "current_evidence": "1338 says NoSourceOnlySpeciesSlot is not derived and remains an explicit closure condition",
            "status": "UNSIGNED_CLOSURE_CONDITION",
            "if_signed": "pre-variation w_A countermodel is killed",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "audit_id": "CMO1406_2_no_source_only_weights",
            "required_clause": "no w_A(X), kappa_A(X), source-only material multiplier, or inert species slot exists in the parent grammar",
            "mathematical_role": "forces source/readout differences to be downstream calibration, not gravitational source",
            "current_evidence": "1079 kills post-variation selectors only conditionally; 1310 source-weight exclusion is unsigned",
            "status": "UNSIGNED_PRE_VARIATION_LEAK_SURVIVES",
            "if_signed": "relative source weights collapse into common mode",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "audit_id": "CMO1406_3_constant_spectrum_owner",
            "required_clause": "masses, Yukawas, Lambda_QCD, binding energies, alpha_EM, and clock constants are representation/superselection data or explicit residual fields",
            "mathematical_role": "forbids beta_e, beta_nuc, beta_EM, beta_other as hidden X-dependent matter-spectrum vertices",
            "current_evidence": "1087 and 1310 mark material constants/matter spectrum owner not parent-signed",
            "status": "UNSIGNED_MATTER_SPECTRUM_OWNER",
            "if_signed": "sector beta rows theorem-zero or become explicit residual fields",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "audit_id": "CMO1406_4_binding_inheritance",
            "required_clause": "electronic, nuclear, EM binding, and other sectors inherit the same beta_* or are individually theorem-zero",
            "mathematical_role": "makes beta_s^a=beta_*^a for every sector s",
            "current_evidence": "1395 sector beta zero theorem is conditional; EM-lock and nuclear/constant owners remain active blockers",
            "status": "UNSIGNED_SECTOR_BETA_ZERO",
            "if_signed": "Delta alpha_AB^a=(sum_s Delta f_s,AB) beta_*^a=0",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "audit_id": "CMO1406_5_source_kernel_owner",
            "required_clause": "K_ab alpha_source^b and tau_WEP are common source/kernel objects, not material-pair selectors",
            "mathematical_role": "prevents WEP zero from being reopened by source worldtube/readout kernels",
            "current_evidence": "1405 retains K_ab, alpha_source^b, tau_WEP as missing; 1402 arena isolation blocks transfer",
            "status": "UNSIGNED_SOURCE_KERNEL",
            "if_signed": "zero differential response remains zero after source contraction",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "audit_id": "CMO1406_6_exact_zero_theorem",
            "required_clause": "if CMO1406_0..5 are signed, WEP is theorem-zero at linear order",
            "mathematical_role": "beta_s^a=beta_*^a and sum_s Delta f_s,AB=0 imply Delta alpha_AB^a=0 and eta_AB=0",
            "current_evidence": "1405 response-current identity plus 1395 conditional sector sum",
            "status": "EXACT_CONDITIONAL_THEOREM_READY_NOT_PROMOTED",
            "if_signed": "WEP branch can be demoted from finite vector prior to theorem-zero at linear order",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "audit_id": "CMO1406_7_current_verdict",
            "required_clause": "current common matter-owner status",
            "mathematical_role": "decide theorem-zero or source acquisition",
            "current_evidence": "NoSourceOnlySpeciesSlot, matter spectrum owner, binding inheritance, and source kernel are unsigned",
            "status": "COMMON_MATTER_OWNER_NOT_PROVED_SECTOR_BETA_ACQUISITION_REQUIRED",
            "if_signed": "not yet applicable",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]


def countermodel_rows() -> list[dict[str, Any]]:
    return [
        {
            "countermodel_id": "CTR1406_0_pre_action_weight",
            "form": "S_matter -> sum_A w_A(X) S_A",
            "why_survives": "Hilbert variation inherits w_A if inserted before variation; 1079 says narrow current ownership does not kill it",
            "kills_clause": "CMO1406_1_single_matter_functional;CMO1406_2_no_source_only_weights",
            "required_repair": "parent object-language/action-measure rule forbidding source-only species slots",
            "status": "LIVE_COUNTERMODEL",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "countermodel_id": "CTR1406_1_matter_spectrum_vertex",
            "form": "m_e(X), y_q(X), Lambda_QCD(X), B_nuc(X), or alpha_EM(X) in the effective matter spectrum",
            "why_survives": "1310 matter spectrum owner is not parent-signed",
            "kills_clause": "CMO1406_3_constant_spectrum_owner;CMO1406_4_binding_inheritance",
            "required_repair": "representation/superselection theorem or explicit residual coefficient rows",
            "status": "LIVE_COUNTERMODEL",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "countermodel_id": "CTR1406_2_EM_lock_failure",
            "form": "independent EM binding or alpha_EM response, including unowned Maxwell normalization/counterterm",
            "why_survives": "1395 and later EM-lock chain keep beta_EM/alpha_EM blockers active",
            "kills_clause": "CMO1406_4_binding_inheritance",
            "required_repair": "unique EM/gauge kinetic owner or finite beta_EM source row",
            "status": "LIVE_COUNTERMODEL",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "countermodel_id": "CTR1406_3_source_kernel_marker",
            "form": "K_ab, tau_WEP, worldtube/readout marker, or material selector depends on source/test material",
            "why_survives": "1405 source kernel and 1402 arena/domain transfer remain missing",
            "kills_clause": "CMO1406_5_source_kernel_owner",
            "required_repair": "source kernel/domain theorem or explicit WEP kernel acquisition rows",
            "status": "LIVE_COUNTERMODEL",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "countermodel_id": "CTR1406_4_pair_cancellation",
            "form": "choose sector betas to cancel TA6V-PtRh10 only",
            "why_survives": "one-pair line can always be tuned but is not all-material invariant",
            "kills_clause": "none; it is forbidden discipline, not proof",
            "required_repair": "all-material theorem or multi-material bound fit, not pair-line tuning",
            "status": "FORBIDDEN_NOT_EVIDENCE",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]


def sector_acquisition_rows() -> list[dict[str, Any]]:
    rows = [
        ("SBAQ1406_0_beta_e", "beta_e^a", "electronic/atomic mass and clock standard sector", "partial ln E_e / partial X_a", "MISSING_SOURCE_OR_ZERO_THEOREM", "clock/fine-structure;WEP;R10"),
        ("SBAQ1406_1_beta_nuc", "beta_nuc^a", "nuclear/QCD binding sector", "partial ln E_nuc / partial X_a", "MISSING_SOURCE_OR_ZERO_THEOREM", "WEP;orbital;R10"),
        ("SBAQ1406_2_beta_EM", "beta_EM^a", "EM binding/charge/fine-structure sector", "partial ln E_EM / partial X_a", "MISSING_SOURCE_OR_ZERO_THEOREM", "WEP;clock;R10"),
        ("SBAQ1406_3_beta_other", "beta_other^a", "other binding/readout guard sector", "partial ln E_other / partial X_a", "MISSING_SOURCE_OR_ZERO_THEOREM", "WEP;PPN;readout"),
        ("SBAQ1406_4_U_source", "U_a := K_ab alpha_source^b", "WEP source/kernel contraction", "K_ab(lambda,lab) alpha_source^b", "MISSING_SOURCE_KERNEL", "WEP only until transfer theorem"),
        ("SBAQ1406_5_Delta_f_tensor", "Delta f_s,AB", "full material contrast tensor", "f_s,A - f_s,B for all relevant material pairs", "MISSING_FULL_MATERIAL_TENSOR", "WEP material scoring"),
        ("SBAQ1406_6_NoSourceOnlySpeciesSlot", "parent grammar certificate", "no species/source-only action slot", "Arg(S_parent) excludes w_A(X)S_A and kappa_A(X)T_A", "MISSING_PARENT_SIGNATURE", "WEP/local source universality"),
    ]
    out = []
    for acquisition_id, quantity, sector_or_object, definition, value_status, arena_use in rows:
        out.append(
            {
                "acquisition_id": acquisition_id,
                "quantity": quantity,
                "sector_or_object": sector_or_object,
                "definition": definition,
                "value_status": value_status,
                "required_source": "parent theorem or explicit coefficient/source row with units and arena projection",
                "arena_use": arena_use,
                "valid_for_claim": False,
                "claim_allowed": False,
            }
        )
    out.append(
        {
            "acquisition_id": "SBAQ1406_7_verdict",
            "quantity": "sector_beta_acquisition_pack",
            "sector_or_object": "all WEP material/current rows",
            "definition": "fill beta_s^a and U_a or prove common owner",
            "value_status": "ACQUISITION_REQUIRED_NONCLAIM",
            "required_source": "CMO theorem closure or explicit sector beta/source rows",
            "arena_use": "WEP pressure only until transfer gates close",
            "valid_for_claim": False,
            "claim_allowed": False,
        }
    )
    return out


def zero_or_bound_rows() -> list[dict[str, Any]]:
    return [
        {
            "gate_id": "ZOB1406_0_zero_route",
            "route": "prove common matter-owner WEP zero",
            "required_inputs": "CMO1406_0..5 parent-signed",
            "current_status": "BLOCKED_UNSIGNED",
            "allowed_output": "conditional theorem only",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "gate_id": "ZOB1406_1_bound_route",
            "route": "explicit sector beta/source vector prior",
            "required_inputs": "beta_e,beta_nuc,beta_EM,beta_other,U_a,Delta f tensor",
            "current_status": "ACQUISITION_REQUIRED",
            "allowed_output": "nonclaim source rows and pressure inequalities",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "gate_id": "ZOB1406_2_transfer_guard",
            "route": "reuse WEP common-owner result for R10/clocks/PPN/local GR",
            "required_inputs": "1402 domain transfer theorem plus arena projection coefficients",
            "current_status": "BLOCKED_BY_ARENA_ISOLATION",
            "allowed_output": "no transfer",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "gate_id": "ZOB1406_3_decision",
            "route": "current branch decision",
            "required_inputs": "zero theorem closure or sector source rows",
            "current_status": "COMMON_OWNER_NOT_PROVED_USE_SECTOR_ACQUISITION",
            "allowed_output": "1407 coefficient acquisition/schema gate",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
    ]


def claim_gate_rows() -> list[dict[str, Any]]:
    return [
        {
            "claim_id": "GATE1406_0_common_owner_zero",
            "claim": "common matter-owner WEP zero is proved",
            "status": "BLOCKED_NO_CLAIM",
            "reason": "NoSourceOnlySpeciesSlot and matter-spectrum/source-kernel owner clauses are unsigned",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "claim_id": "GATE1406_1_sector_beta_zero",
            "claim": "beta_e, beta_nuc, beta_EM, and beta_other are zero/source-owned",
            "status": "BLOCKED_NO_CLAIM",
            "reason": "1395 sector beta zero attempt remains conditional with active EM/nuclear/constant blockers",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "claim_id": "GATE1406_2_WEP_pass",
            "claim": "WEP branch passes",
            "status": "BLOCKED_NO_CLAIM",
            "reason": "no sector values, source kernel, or full material tensor are available",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "claim_id": "GATE1406_3_transfer",
            "claim": "WEP branch transfers to clocks, R10, PPN, or orbital arenas",
            "status": "BLOCKED_NO_CLAIM",
            "reason": "1402 arena isolation and missing projection coefficients still apply",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "claim_id": "GATE1406_4_local_GR",
            "claim": "local GR/Newton reduction can be claimed",
            "status": "BLOCKED_NO_CLAIM",
            "reason": "conditional WEP zero does not close q_loc, lambda_A, EM residuals, PPN projection, or source kernel",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        {
            "decision_id": "DEC1406_0_theorem_status",
            "decision": "do not promote common matter-owner WEP zero",
            "basis": "exact theorem exists only under unsigned parent signature clauses",
            "action": "record as conditional theorem and keep finite branch live",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "decision_id": "DEC1406_1_main_blocker",
            "decision": "name NoSourceOnlySpeciesSlot as the clean blocker",
            "basis": "1338 explicitly classifies it as closure condition, not derived primitive",
            "action": "future derivation must target parent grammar/action-domain certificate",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "decision_id": "DEC1406_2_fallback",
            "decision": "prepare sector beta acquisition route",
            "basis": "if theorem route does not close, WEP can still be tested by explicit vector coefficients",
            "action": "build 1407 coefficient schema/gate for beta_s and U_a",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        {
            "next_id": "NEXT1406_0_1407",
            "target_doc": "1407-Y5-R10-RAB-NoSourceOnlySpeciesSlot-proof-or-sector-beta-source-schema.md",
            "target_script": "scripts/Y5_R10_RAB_NoSourceOnlySpeciesSlot_proof_or_sector_beta_source_schema.py",
            "task": "try to prove the parent grammar/action-domain excludes source-only species slots; if not, build strict sector beta/source coefficient schema for beta_e, beta_nuc, beta_EM, beta_other, U_a, and Delta f_s,AB",
            "success_condition": "either NoSourceOnlySpeciesSlot is parent-signed, or every finite WEP sector coefficient has a nonclaim source row with units, arena projection, and no pair-cancellation credit",
            "do_not_claim": "WEP pass;clock pass;R10 pass;PPN pass;Newton limit;local GR;lambda_A=0;q_loc=0;GitHub-ready result",
            "valid_for_claim": False,
            "claim_allowed": False,
        }
    ]


def validation_rows(
    sources: list[dict[str, Any]],
    theorem: list[dict[str, Any]],
    counters: list[dict[str, Any]],
    acquisition: list[dict[str, Any]],
    zero_or_bound: list[dict[str, Any]],
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
    theorem_ok = (
        any(r["audit_id"] == "CMO1406_6_exact_zero_theorem" and r["status"] == "EXACT_CONDITIONAL_THEOREM_READY_NOT_PROMOTED" for r in theorem)
        and any(r["audit_id"] == "CMO1406_7_current_verdict" and r["status"] == "COMMON_MATTER_OWNER_NOT_PROVED_SECTOR_BETA_ACQUISITION_REQUIRED" for r in theorem)
        and all(str(r["claim_allowed"]) == "False" for r in theorem)
    )
    counter_ok = (
        any(r["countermodel_id"] == "CTR1406_0_pre_action_weight" and r["status"] == "LIVE_COUNTERMODEL" for r in counters)
        and any(r["countermodel_id"] == "CTR1406_4_pair_cancellation" and r["status"] == "FORBIDDEN_NOT_EVIDENCE" for r in counters)
        and all(str(r["valid_for_claim"]) == "False" for r in counters)
    )
    acquisition_ok = (
        any(r["quantity"] == "beta_e^a" and r["value_status"] == "MISSING_SOURCE_OR_ZERO_THEOREM" for r in acquisition)
        and any(r["quantity"] == "beta_EM^a" and r["value_status"] == "MISSING_SOURCE_OR_ZERO_THEOREM" for r in acquisition)
        and any(r["quantity"] == "U_a := K_ab alpha_source^b" and r["value_status"] == "MISSING_SOURCE_KERNEL" for r in acquisition)
        and any(r["acquisition_id"] == "SBAQ1406_7_verdict" for r in acquisition)
        and all(str(r["claim_allowed"]) == "False" for r in acquisition)
    )
    route_ok = (
        any(r["gate_id"] == "ZOB1406_0_zero_route" and r["current_status"] == "BLOCKED_UNSIGNED" for r in zero_or_bound)
        and any(r["gate_id"] == "ZOB1406_3_decision" and r["current_status"] == "COMMON_OWNER_NOT_PROVED_USE_SECTOR_ACQUISITION" for r in zero_or_bound)
        and all(str(r["valid_for_claim"]) == "False" for r in zero_or_bound)
    )
    claims_ok = all(str(r["claim_allowed"]) == "False" and "NO_CLAIM" in r["status"] for r in gates)
    output_paths = [
        DOC_PATH,
        SOURCE_REGISTER_PATH,
        THEOREM_AUDIT_PATH,
        COUNTERMODEL_PATH,
        SECTOR_ACQUISITION_PATH,
        ZERO_OR_BOUND_PATH,
        CLAIM_GATE_PATH,
        DECISION_LEDGER_PATH,
        NEXT_TARGET_PATH,
        VALIDATION_PATH,
    ]
    scope_ok = all(str((ROOT / path).resolve()).startswith(str(ROOT.resolve())) for path in output_paths)

    checks = [
        row("VAL1406_0_sources", all_sources_ok, "all cited local source paths exist and anchors are present"),
        row("VAL1406_1_theorem_audit", theorem_ok, "common matter-owner WEP zero remains exact conditional only"),
        row("VAL1406_2_countermodels", counter_ok, "live pre-action/source and spectrum countermodels are recorded"),
        row("VAL1406_3_sector_acquisition", acquisition_ok, "sector beta/source acquisition rows are present and nonclaim"),
        row("VAL1406_4_zero_or_bound", route_ok, "route decision selects sector acquisition unless theorem clauses close"),
        row("VAL1406_5_claim_refusal", claims_ok, "WEP, transfer, and local-GR claims are refused"),
        row("VAL1406_6_scope", scope_ok, "outputs are confined to post-checkpoint-work paths"),
    ]
    overall = all(check["status"] == "PASS" for check in checks)
    checks.append(
        row(
            "VAL1406_7_overall",
            overall,
            "1406 preserves the exact WEP zero theorem as conditional and opens strict sector beta acquisition",
        )
    )
    return checks


def write_doc(
    sources: list[dict[str, Any]],
    theorem: list[dict[str, Any]],
    counters: list[dict[str, Any]],
    acquisition: list[dict[str, Any]],
    zero_or_bound: list[dict[str, Any]],
    gates: list[dict[str, Any]],
    decisions: list[dict[str, Any]],
    next_target: list[dict[str, Any]],
    validation: list[dict[str, Any]],
) -> None:
    body = f"""# 1406 — Common Matter-Owner WEP Zero Theorem Or Sector Beta Acquisition

**Status:** `{STATUS}`

**Current verdict:** the clean theorem exists but is not parent-signed. If every ordinary sector inherits one matter owner, then `beta_s^a=beta_*^a`, `sum_s Delta f_s,AB=0`, and therefore `Delta alpha_AB^a=0 -> eta_AB=0`. Current corpus still leaves `NoSourceOnlySpeciesSlot`, matter-spectrum ownership, binding inheritance, and the WEP source kernel unsigned.

**Discipline move:** no WEP pass. The honest fork is now sharp: either prove the parent grammar forbids source-only species slots, or fill explicit sector beta/source rows for `beta_e`, `beta_nuc`, `beta_EM`, `beta_other`, `U_a := K_ab alpha_source^b`, and `Delta f_s,AB`.

**Claim ceiling:** `{CLAIM_CEILING}`

## Source Register

{md_table(sources)}

## Common Matter-Owner WEP Zero Audit

{md_table(theorem)}

## WEP Owner Countermodel Ledger

{md_table(counters)}

## Sector Beta Source Acquisition

{md_table(acquisition)}

## Zero Or Bound Decision Gate

{md_table(zero_or_bound)}

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
    theorem = theorem_audit_rows()
    counters = countermodel_rows()
    acquisition = sector_acquisition_rows()
    zero_or_bound = zero_or_bound_rows()
    gates = claim_gate_rows()
    decisions = decision_rows()
    next_target = next_target_rows()
    validation = validation_rows(sources, theorem, counters, acquisition, zero_or_bound, gates)

    write_csv(SOURCE_REGISTER_PATH, sources)
    write_csv(THEOREM_AUDIT_PATH, theorem)
    write_csv(COUNTERMODEL_PATH, counters)
    write_csv(SECTOR_ACQUISITION_PATH, acquisition)
    write_csv(ZERO_OR_BOUND_PATH, zero_or_bound)
    write_csv(CLAIM_GATE_PATH, gates)
    write_csv(DECISION_LEDGER_PATH, decisions)
    write_csv(NEXT_TARGET_PATH, next_target)
    write_csv(VALIDATION_PATH, validation)
    write_doc(sources, theorem, counters, acquisition, zero_or_bound, gates, decisions, next_target, validation)

    failed = [row for row in validation if row["status"] != "PASS"]
    if failed:
        raise SystemExit(f"1406 validation failed: {failed}")
    print(STATUS)
    print(ROOT / DOC_PATH)
    print(ROOT / VALIDATION_PATH)


if __name__ == "__main__":
    main()

from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


SCRIPT_START_UTC = datetime.now(timezone.utc)

ROOT = Path(__file__).resolve().parents[1]
PROJECT = ROOT.parent
RESIDUALS = ROOT / "source-intake" / "mts_residuals"
LOCAL_BOUNDS = ROOT / "source-intake" / "local_bounds"
SOURCE_WEIGHT = ROOT / "source-intake" / "source-weight"
RAB_QUEUE = ROOT / "source-intake" / "rab-sector" / "acquisition-queue"
BETA_DOCS = ROOT / "source-intake" / "beta-source" / "docs"
FORMALIZATION = PROJECT / "formalization-workbench"

DOC = ROOT / "2871-Y5-R2FR-QCAB-parent-source-equation-or-finite-row-under-AX1090.md"

SRC_2870_DOC = ROOT / "2870-Y5-R2FR-first-triplet-deep-source-extraction-under-AX1090.md"
SRC_2870_REVIEW = RESIDUALS / "P8_Y5_R2FR_2870_FIRST_TRIPLET_CANDIDATE_REVIEW.csv"
SRC_2870_EXTRACTION = RESIDUALS / "P8_Y5_R2FR_2870_DEEP_EXTRACTION_RESULTS.csv"
SRC_2870_REQUESTS = RESIDUALS / "P8_Y5_R2FR_2870_REFINED_SOURCE_REQUESTS.csv"
SRC_2870_NEXT = RESIDUALS / "P8_Y5_R2FR_2870_NEXT_TARGET.csv"
SRC_2870_VALIDATION = RESIDUALS / "P8_Y5_BRR545_2870_VALIDATION.csv"

SRC_2863_EVIDENCE = RESIDUALS / "P8_Y5_R2FR_2863_QCAB_SOURCE_EVIDENCE_SCAN.csv"
SRC_2863_ZERO = RESIDUALS / "P8_Y5_R2FR_2863_QCAB_PARENT_ZERO_PROOF_AUDIT.csv"
SRC_2863_ACCEPTANCE = RESIDUALS / "P8_Y5_R2FR_2863_QCAB_ACCEPTANCE_GATE.csv"
SRC_2863_BLOCKERS = RESIDUALS / "P8_Y5_R2FR_2863_QCAB_BLOCKER_LEDGER.csv"

SRC_2844_FLUX = RESIDUALS / "P8_Y5_R2FR_2844_CAB_GREEN_FLUX_IDENTITY.csv"
SRC_2844_PACK = RESIDUALS / "P8_Y5_R2FR_2844_CAB_AMPLITUDE_SOURCE_PACK.csv"
SRC_2844_CONTRACT = RESIDUALS / "P8_Y5_R2FR_2844_PARENT_AMPLITUDE_CONTRACT.csv"

SRC_2855_EQUATION_DRAFT = RESIDUALS / "P8_Y5_R2FR_2855_PARENT_SOURCE_EQUATION_DRAFT.csv"
SRC_2861_SCAN = RESIDUALS / "P8_Y5_R2FR_2861_FIRST_ROW_SOURCE_SCAN.csv"
SRC_2861_ACCEPT = RESIDUALS / "P8_Y5_R2FR_2861_FIRST_ROW_ACCEPTANCE_TEST.csv"
SRC_2869_REQUESTS = RESIDUALS / "P8_Y5_R2FR_2869_EXACT_SOURCE_REQUESTS.csv"

OUTPUTS = {
    "sources": RESIDUALS / "P8_Y5_R2FR_2871_SOURCE_REGISTER.csv",
    "review": RESIDUALS / "P8_Y5_R2FR_2871_QCAB_EVIDENCE_REVIEW.csv",
    "source_law": RESIDUALS / "P8_Y5_R2FR_2871_QCAB_SOURCE_EQUATION_AUDIT.csv",
    "zero_audit": RESIDUALS / "P8_Y5_R2FR_2871_QCAB_PARENT_ZERO_AUDIT.csv",
    "template": RESIDUALS / "P8_Y5_R2FR_2871_QCAB_FINITE_ROW_TEMPLATE_NONCLAIM.csv",
    "gates": RESIDUALS / "P8_Y5_R2FR_2871_ACCEPTANCE_GATES.csv",
    "request": RESIDUALS / "P8_Y5_R2FR_2871_NARROW_SOURCE_REQUEST.csv",
    "runner": RESIDUALS / "P8_Y5_R2FR_2871_RUNNER_STATUS.csv",
    "decision": RESIDUALS / "P8_Y5_R2FR_2871_DECISION_LEDGER.csv",
    "next": RESIDUALS / "P8_Y5_R2FR_2871_NEXT_TARGET.csv",
    "branches": RESIDUALS / "P8_Y5_R2FR_2871_BRANCH_COPIES.csv",
    "validation": RESIDUALS / "P8_Y5_BRR545_2871_VALIDATION.csv",
}

BRANCH_OUTPUTS = {
    "law_copy": LOCAL_BOUNDS / "RAB_QCAB_SOURCE_EQUATION_AUDIT_2871_NONCLAIM.csv",
    "request_copy": SOURCE_WEIGHT / "RAB_QCAB_NARROW_SOURCE_REQUEST_2871_NONCLAIM.csv",
    "template_copy": BETA_DOCS / "RAB_QCAB_FINITE_ROW_TEMPLATE_2871_NONCLAIM.csv",
    "next_queue": RAB_QUEUE / "JR2871_qReff_parent_source_equation_NEXT.csv",
}

for directory in {path.parent for path in OUTPUTS.values()} | {path.parent for path in BRANCH_OUTPUTS.values()} | {DOC.parent}:
    directory.mkdir(parents=True, exist_ok=True)


def now() -> str:
    return datetime.now(timezone.utc).isoformat()


def read_text(path: Path) -> str:
    if not path.exists():
        return ""
    return path.read_text(encoding="utf-8", errors="replace")


def anchors_present(path: Path, anchors: str) -> tuple[bool, str]:
    if not path.exists():
        return False, anchors
    text = read_text(path)
    missing = [anchor for anchor in anchors.split(";") if anchor and anchor not in text]
    return not missing, ";".join(missing)


def add_common(row: dict[str, Any]) -> dict[str, Any]:
    row.update(
        {
            "control_only": True,
            "score_ready": False,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
            "generated_utc": now(),
        }
    )
    return row


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
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


def csv_parses(path: Path) -> bool:
    try:
        with path.open(newline="", encoding="utf-8") as handle:
            list(csv.DictReader(handle))
        return True
    except Exception:
        return False


def source_register_rows() -> list[dict[str, Any]]:
    specs = [
        ("SRC2871_0_2870_doc", SRC_2870_DOC, "NEXT2870_0_2871;EXT2870_CAB;REQ2870_CAB;VAL2870_OVERALL", "2870 selected Q_CAB-only extraction"),
        ("SRC2871_1_2870_review", SRC_2870_REVIEW, "REV2870_CAND2869_CAB_01;REV2870_CAND2869_CAB_15", "Q_CAB candidate review"),
        ("SRC2871_2_2870_extraction", SRC_2870_EXTRACTION, "EXT2870_CAB", "Q_CAB deep extraction refusal"),
        ("SRC2871_3_2870_requests", SRC_2870_REQUESTS, "REQ2870_CAB", "refined Q_CAB source request"),
        ("SRC2871_4_2870_next", SRC_2870_NEXT, "NEXT2870_0_2871", "handoff to 2871"),
        ("SRC2871_5_2870_validation", SRC_2870_VALIDATION, "VAL2870_OVERALL", "2870 validation"),
        ("SRC2871_6_2863_evidence", SRC_2863_EVIDENCE, "EVID2863_0_surface_definition;EVID2863_1_source_integral;EVID2863_5_balance_relation", "prior Q_CAB source evidence scan"),
        ("SRC2871_7_2863_zero", SRC_2863_ZERO, "ZP2863_0_gauss_zero_skeleton;ZP2863_6_verdict", "prior Q_CAB parent-zero audit"),
        ("SRC2871_8_2863_acceptance", SRC_2863_ACCEPTANCE, "ACC2863_0_value_or_zero;ACC2863_5_local_claim_guard", "prior Q_CAB acceptance gate"),
        ("SRC2871_9_2863_blockers", SRC_2863_BLOCKERS, "BLOCK2863_0_Q_CAB_PARENT_INPUT;BLOCK2863_4_GREEN_SIGN", "prior Q_CAB blocker ledger"),
        ("SRC2871_10_2844_flux", SRC_2844_FLUX, "FLUX2844_1_surface_amplitude;FLUX2844_2_source_charge;FLUX2844_4_local_ppn_amplitude;FLUX2844_5_local_suppression_condition", "surface and conditional Gauss law"),
        ("SRC2871_11_2844_pack", SRC_2844_PACK, "PACK2844_0_Q_CAB;PACK2844_1_J_CAB;PACK2844_2_L_CAB;PACK2844_3_B_CAB", "missing Q_CAB source slots"),
        ("SRC2871_12_2844_contract", SRC_2844_CONTRACT, "CONTRACT2844_0_operator;CONTRACT2844_1_source_current;CONTRACT2844_2_boundary;CONTRACT2844_5_sign", "parent amplitude contract"),
        ("SRC2871_13_2855_source_equation", SRC_2855_EQUATION_DRAFT, "PEQ2855_0_CAB_source;PEQ2855_3_amp_current_identity", "draft parent source equation"),
        ("SRC2871_14_2861_scan", SRC_2861_SCAN, "SCAN2861_0_Q_CAB", "first-row source scan"),
        ("SRC2871_15_2861_accept", SRC_2861_ACCEPT, "ACC2861_0_Q_CAB_numeric", "first-row acceptance test"),
        ("SRC2871_16_2869_requests", SRC_2869_REQUESTS, "REQ2869_CAB", "exact source request lineage"),
    ]
    rows: list[dict[str, Any]] = []
    for source_id, path, anchors, role in specs:
        found, missing = anchors_present(path, anchors)
        rows.append(
            add_common(
                {
                    "source_id": source_id,
                    "source_path": str(path),
                    "anchors": anchors,
                    "role": role,
                    "path_exists": path.exists(),
                    "anchors_found": found,
                    "missing_anchors": missing,
                }
            )
        )
    return rows


def evidence_review_rows() -> list[dict[str, Any]]:
    rows = [
        {
            "review_id": "REV2871_0_surface_definition",
            "quantity": "Q_CAB",
            "source_path": str(SRC_2844_FLUX),
            "source_anchor": "FLUX2844_1_surface_amplitude",
            "candidate": "Q_CAB=4*pi*A_CAB with A_CAB from the exterior surface flux",
            "verdict": "SYMBOLIC_IDENTITY_ONLY",
            "reason_not_accepted": "defines the amplitude but does not provide a finite source value, parent-zero theorem, units, or owned boundary/sign convention",
        },
        {
            "review_id": "REV2871_1_conditional_source_integral",
            "quantity": "Q_CAB",
            "source_path": str(SRC_2844_FLUX),
            "source_anchor": "FLUX2844_2_source_charge",
            "candidate": "if Laplacian C_AB=-rho_CAB then A_CAB=(1/(4*pi))*int rho_CAB d^3x plus boundary/corner terms",
            "verdict": "CONDITIONAL_GAUSS_LAW_ONLY",
            "reason_not_accepted": "operator, source density, boundary/corner policy, and Green/sign convention are explicitly not parent-owned",
        },
        {
            "review_id": "REV2871_2_source_pack_slot",
            "quantity": "Q_CAB",
            "source_path": str(SRC_2844_PACK),
            "source_anchor": "PACK2844_0_Q_CAB",
            "candidate": "source pack records Q_CAB=4*pi*A_CAB as the integrated target-map monopole charge",
            "verdict": "MISSING_PARENT_INPUT",
            "reason_not_accepted": "the row is a slot/request, not a source-backed finite row",
        },
        {
            "review_id": "REV2871_3_operator_slot",
            "quantity": "L_CAB",
            "source_path": str(SRC_2844_PACK),
            "source_anchor": "PACK2844_2_L_CAB",
            "candidate": "operator acting on target map in exterior branch",
            "verdict": "MISSING_OPERATOR",
            "reason_not_accepted": "the Laplacian/Yukawa/common-kernel form remains a required derivation, not an accepted input",
        },
        {
            "review_id": "REV2871_4_source_density_slot",
            "quantity": "J_CAB/rho_CAB",
            "source_path": str(SRC_2844_PACK),
            "source_anchor": "PACK2844_1_J_CAB",
            "candidate": "local source density generating C_AB",
            "verdict": "MISSING_SOURCE_DENSITY",
            "reason_not_accepted": "no parent target-source functional or source-zero theorem is present",
        },
        {
            "review_id": "REV2871_5_draft_parent_equation",
            "quantity": "Q_CAB",
            "source_path": str(SRC_2855_EQUATION_DRAFT),
            "source_anchor": "PEQ2855_0_CAB_source",
            "candidate": "L_CAB C_AB=J_CAB; Q_CAB=integral_W J_CAB dV + surface_integral_boundary B_CAB",
            "verdict": "DRAFT_EQUATION_NOT_PARENT_DERIVED",
            "reason_not_accepted": "draft gives the right contract shape but marks parent L_CAB, J_CAB, boundary/corner policy and charge units missing",
        },
        {
            "review_id": "REV2871_6_deep_extraction",
            "quantity": "Q_CAB",
            "source_path": str(SRC_2870_EXTRACTION),
            "source_anchor": "EXT2870_CAB",
            "candidate": "2870 deep extraction over top Q_CAB candidates",
            "verdict": "NO_ACCEPTED_SOURCE_ROW",
            "reason_not_accepted": "15 reviewed candidates were blockers, requests, schemas, placeholders, or closure-only rows",
        },
        {
            "review_id": "REV2871_7_parent_zero_prior",
            "quantity": "Q_CAB",
            "source_path": str(SRC_2863_ZERO),
            "source_anchor": "ZP2863_6_verdict",
            "candidate": "Q_CAB finite first row or Q_CAB=0 parent theorem",
            "verdict": "NOT_ACCEPTED",
            "reason_not_accepted": "prior zero-proof audit keeps Q_CAB missing parent input",
        },
    ]
    for row in rows:
        row.update(
            {
                "accepted_source_row": False,
                "finite_numeric_value_present": False,
                "parent_zero_theorem_present": False,
            }
        )
    return [add_common(row) for row in rows]


def source_law_rows() -> list[dict[str, Any]]:
    rows = [
        {
            "law_id": "LAW2871_0_surface_to_charge",
            "clause": "exterior amplitude definition",
            "conditional_statement": "For an exterior branch C_AB(r,Omega)=A_CAB/r+C_reg with no angular monopole ambiguity, define Q_CAB:=4*pi*A_CAB.",
            "derived_status": "DERIVED_CONDITIONAL_IDENTITY",
            "parent_status": "IDENTITY_ONLY_NOT_SOURCE_VALUE",
            "missing_for_claim": "finite A_CAB or a source/zero theorem fixing A_CAB",
            "source_path": str(SRC_2844_FLUX),
            "source_anchor": "FLUX2844_1_surface_amplitude",
        },
        {
            "law_id": "LAW2871_1_operator_source_contract",
            "clause": "parent source equation contract",
            "conditional_statement": "If the parent action yields L_CAB C_AB=J_CAB and the exterior Green convention matches C_AB=Q_CAB/(4*pi*r)+regular, then Q_CAB=int_W J_CAB dV + surface_integral_boundary B_CAB, up to the signed orientation convention owned by L_CAB.",
            "derived_status": "DERIVED_CONDITIONAL_CONTRACT",
            "parent_status": "DRAFT_NOT_PARENT_SIGNED",
            "missing_for_claim": "parent L_CAB; J_CAB/rho_CAB source functional; B_CAB boundary policy; units; branch id; sign/common Green owner",
            "source_path": str(SRC_2855_EQUATION_DRAFT),
            "source_anchor": "PEQ2855_0_CAB_source",
        },
        {
            "law_id": "LAW2871_2_operator_owner",
            "clause": "L_CAB operator",
            "conditional_statement": "The source integral only has a fixed 4*pi normalization after L_CAB and its exterior Green kernel are specified.",
            "derived_status": "REQUIRED_CLAUSE_IDENTIFIED",
            "parent_status": "MISSING_OPERATOR",
            "missing_for_claim": "prove Laplacian/Yukawa/common-kernel form or cite parent field equation",
            "source_path": str(SRC_2844_PACK),
            "source_anchor": "PACK2844_2_L_CAB",
        },
        {
            "law_id": "LAW2871_3_source_density_owner",
            "clause": "J_CAB or rho_CAB source",
            "conditional_statement": "A finite Q_CAB row requires either numeric/source-backed int_W J_CAB dV or a theorem that J_CAB is exact/silent in the monopole channel.",
            "derived_status": "REQUIRED_CLAUSE_IDENTIFIED",
            "parent_status": "MISSING_SOURCE_DENSITY",
            "missing_for_claim": "derive target source functional from parent matter/action variation",
            "source_path": str(SRC_2844_PACK),
            "source_anchor": "PACK2844_1_J_CAB",
        },
        {
            "law_id": "LAW2871_4_boundary_owner",
            "clause": "boundary/corner flux",
            "conditional_statement": "The charge law is not closed unless B_CAB is proven zero for the local worldtube or explicitly included in Q_CAB.",
            "derived_status": "REQUIRED_CLAUSE_IDENTIFIED",
            "parent_status": "MISSING_BOUNDARY_INPUT",
            "missing_for_claim": "boundary/corner silence theorem or finite boundary term",
            "source_path": str(SRC_2844_PACK),
            "source_anchor": "PACK2844_3_B_CAB",
        },
        {
            "law_id": "LAW2871_5_common_green_sign",
            "clause": "shared Green/sign convention",
            "conditional_statement": "Q_CAB can only enter A_total=(sigma_R*q_R_eff+Q_CAB)/(4*pi) after C_AB and delta_R share one radial 4*pi convention and one sign orientation.",
            "derived_status": "REQUIRED_CLAUSE_IDENTIFIED",
            "parent_status": "MISSING_SIGN_CONVENTION",
            "missing_for_claim": "parent-owned common Green convention and sigma_R_source_sign",
            "source_path": str(SRC_2844_CONTRACT),
            "source_anchor": "CONTRACT2844_0_operator;CONTRACT2844_5_sign",
        },
        {
            "law_id": "LAW2871_6_verdict",
            "clause": "Q_CAB source law acceptance",
            "conditional_statement": "The exact contract is now explicit, but it remains a contract: no accepted finite Q_CAB value and no parent-zero theorem were found.",
            "derived_status": "CONTRACT_WRITTEN",
            "parent_status": "NOT_ACCEPTED_FOR_CLAIM",
            "missing_for_claim": "all of L_CAB, J_CAB/rho_CAB, B_CAB, units, branch id, and shared Green/sign convention",
            "source_path": str(SRC_2870_EXTRACTION),
            "source_anchor": "EXT2870_CAB",
        },
    ]
    for row in rows:
        row.update(
            {
                "source_equation_parent_accepted": False,
                "finite_row_ready": False,
                "parent_zero_ready": False,
            }
        )
    return [add_common(row) for row in rows]


def zero_audit_rows() -> list[dict[str, Any]]:
    rows = [
        {
            "zero_id": "ZERO2871_0_source_silence",
            "theorem_route": "J_CAB=0 for ordinary compact matter",
            "needed_premise": "parent matter/action variation has no target-map source in the monopole sector",
            "current_status": "NOT_DERIVED",
            "blocker": "MISSING_SOURCE_DENSITY_ZERO_THEOREM",
            "source_path": str(SRC_2863_ZERO),
            "source_anchor": "ZP2863_1_no_source_density",
        },
        {
            "zero_id": "ZERO2871_1_exact_divergence",
            "theorem_route": "J_CAB=dK_CAB with zero net monopole",
            "needed_premise": "parent Noether/Bianchi identity owns K_CAB and its boundary domain",
            "current_status": "ROUTE_OPEN_BUT_UNSOURCED",
            "blocker": "MISSING_CAB_GAUGE_OR_COHOMOLOGY_OWNER",
            "source_path": str(SRC_2863_ZERO),
            "source_anchor": "ZP2863_3_pure_gauge_or_cohomology_zero",
        },
        {
            "zero_id": "ZERO2871_2_boundary_silence",
            "theorem_route": "surface_integral_boundary B_CAB=0",
            "needed_premise": "closed local worldtube or exact boundary primitive with no unowned charge",
            "current_status": "NOT_DERIVED",
            "blocker": "MISSING_BOUNDARY_FLUX_LAW",
            "source_path": str(SRC_2863_ZERO),
            "source_anchor": "ZP2863_2_boundary_silence",
        },
        {
            "zero_id": "ZERO2871_3_balance_identity",
            "theorem_route": "Q_CAB=-sigma_R*q_R_eff from shared parent current",
            "needed_premise": "one parent identity fixes both projections and forbids independent rescaling",
            "current_status": "CONDITIONAL_RELATION_NOT_QCAB_ZERO",
            "blocker": "MISSING_RATIO_OWNER_SIGMA_SOURCE_SIGN_AND_QREFF",
            "source_path": str(SRC_2855_EQUATION_DRAFT),
            "source_anchor": "PEQ2855_3_amp_current_identity",
        },
        {
            "zero_id": "ZERO2871_4_rescaling_obstruction",
            "theorem_route": "normalization uniqueness forbids arbitrary Q_CAB scaling",
            "needed_premise": "parent action fixes target current normalization before readout",
            "current_status": "COUNTEREXAMPLE_SURVIVES",
            "blocker": "CURRENT_OWNER_NOT_SIGNED",
            "source_path": str(SRC_2863_ZERO),
            "source_anchor": "ZP2863_5_rescaling_obstruction",
        },
        {
            "zero_id": "ZERO2871_5_verdict",
            "theorem_route": "Q_CAB=0 parent theorem",
            "needed_premise": "source silence/exact divergence, boundary silence, and normalization owner all close together",
            "current_status": "NOT_ACCEPTED",
            "blocker": "Q_CAB_ZERO_NOT_PARENT_SIGNED",
            "source_path": str(SRC_2863_ZERO),
            "source_anchor": "ZP2863_6_verdict",
        },
    ]
    for row in rows:
        row.update(
            {
                "parent_signed": False,
                "qcab_zero_accepted": False,
                "accepted_source_row": False,
            }
        )
    return [add_common(row) for row in rows]


def template_rows() -> list[dict[str, Any]]:
    rows = [
        {
            "template_id": "TPL2871_0_QCAB_parent_source_row",
            "quantity": "Q_CAB",
            "required_equation": "L_CAB C_AB = J_CAB; Q_CAB = int_W J_CAB dV + surface_integral_boundary B_CAB = 4*pi*A_CAB",
            "value": "MISSING_Q_CAB",
            "units": "MISSING_UNITS",
            "source_path": "MISSING_PARENT_SOURCE_PATH",
            "equation_anchor": "MISSING_EQUATION_ANCHOR",
            "branch_id": "MISSING_BRANCH_ID",
            "status": "TEMPLATE_ONLY_NOT_LIVE_ROW",
            "ready_for_runner": False,
        },
        {
            "template_id": "TPL2871_1_LCAB_operator",
            "quantity": "L_CAB",
            "required_equation": "parent target-map Euler-Lagrange/operator equation with exterior Green kernel",
            "value": "MISSING_L_CAB",
            "units": "MISSING_OPERATOR_UNITS",
            "source_path": "MISSING_PARENT_SOURCE_PATH",
            "equation_anchor": "MISSING_OPERATOR_ANCHOR",
            "branch_id": "MISSING_BRANCH_ID",
            "status": "TEMPLATE_ONLY_NOT_LIVE_ROW",
            "ready_for_runner": False,
        },
        {
            "template_id": "TPL2871_2_JCAB_source",
            "quantity": "J_CAB/rho_CAB",
            "required_equation": "source functional from parent variation or source-zero theorem",
            "value": "MISSING_J_CAB_OR_ZERO_THEOREM",
            "units": "MISSING_SOURCE_DENSITY_UNITS",
            "source_path": "MISSING_PARENT_SOURCE_PATH",
            "equation_anchor": "MISSING_SOURCE_ANCHOR",
            "branch_id": "MISSING_BRANCH_ID",
            "status": "TEMPLATE_ONLY_NOT_LIVE_ROW",
            "ready_for_runner": False,
        },
        {
            "template_id": "TPL2871_3_BCAB_boundary",
            "quantity": "B_CAB",
            "required_equation": "boundary/corner flux is zero or included in Q_CAB",
            "value": "MISSING_B_CAB_BOUNDARY_POLICY",
            "units": "MISSING_BOUNDARY_UNITS",
            "source_path": "MISSING_PARENT_SOURCE_PATH",
            "equation_anchor": "MISSING_BOUNDARY_ANCHOR",
            "branch_id": "MISSING_BRANCH_ID",
            "status": "TEMPLATE_ONLY_NOT_LIVE_ROW",
            "ready_for_runner": False,
        },
    ]
    for row in rows:
        row.update(
            {
                "accepted_source_row": False,
                "finite_numeric_value_present": False,
                "parent_zero_theorem_present": False,
            }
        )
    return [add_common(row) for row in rows]


def gate_rows() -> list[dict[str, Any]]:
    specs = [
        ("GATE2871_0_finite_value_or_zero", "finite Q_CAB value or parent-zero theorem", "FAIL", "no numeric finite row and no parent-signed zero theorem"),
        ("GATE2871_1_parent_source_equation", "L_CAB C_AB=J_CAB accepted as parent-derived", "FAIL", "source equation is only a conditional contract/draft"),
        ("GATE2871_2_operator_source", "L_CAB and J_CAB/rho_CAB are both sourced", "FAIL", "operator and source density remain missing"),
        ("GATE2871_3_boundary", "B_CAB boundary/corner policy closed", "FAIL", "boundary flux law missing"),
        ("GATE2871_4_common_green_sign", "shared 4*pi radial Green/sign convention closed", "FAIL", "common kernel/sign convention not parent-owned"),
        ("GATE2871_5_units_branch_source", "units, branch id, source path and equation anchor complete", "FAIL", "template still contains MISSING_* fields"),
        ("GATE2871_6_Atotal_unlock", "A_total numerator can use Q_CAB", "FAIL", "Q_CAB remains blocked and q_R_eff/sigma/common Green are also unaccepted"),
        ("GATE2871_7_local_claim_guard", "local GR/Newton claim allowed", "FAIL", "Q_CAB-only work cannot establish full local PPN vector"),
    ]
    return [
        add_common(
            {
                "gate_id": gate_id,
                "criterion": criterion,
                "result": result,
                "reason": reason,
                "gate_passed": False,
                "runner_ready": False,
            }
        )
        for gate_id, criterion, result, reason in specs
    ]


def request_rows() -> list[dict[str, Any]]:
    return [
        add_common(
            {
                "request_id": "REQ2871_QCAB_PARENT_SOURCE_ROW",
                "quantity": "Q_CAB",
                "needed_source": "one parent-owned Q_CAB source row or theorem-zero proof",
                "narrow_request": "Provide the exact parent equation for the target-map amplitude sector: L_CAB C_AB=J_CAB with the exterior Green convention C_AB=Q_CAB/(4*pi*r)+regular, plus Q_CAB=int_W J_CAB dV + boundary term or Q_CAB=0 theorem. It must include L_CAB, J_CAB/rho_CAB, B_CAB policy, units, branch id, source path, equation anchor, and the sign/common-Green convention tying it to q_R_eff and sigma_R_source_sign.",
                "must_not_be": "schema row; source request; blocker ledger; closure-only U_amp relation; fitted cancellation; profile-import sign",
                "status": "OPEN_SOURCE_REQUEST",
                "ready_for_runner": False,
            }
        )
    ]


def runner_rows() -> list[dict[str, Any]]:
    return [
        add_common(
            {
                "runner_id": "RUN2871_0_QCAB_gate",
                "status": "REFUSED",
                "accepted_qcab_rows": 0,
                "required_qcab_rows": 1,
                "accepted_first_triplet_rows": 0,
                "required_first_triplet_rows": 4,
                "reason": "conditional Q_CAB law was written, but no finite/source-backed Q_CAB value or parent-zero theorem passed the gates",
                "runner_ready": False,
                "score_allowed": False,
            }
        )
    ]


def decision_rows() -> list[dict[str, Any]]:
    specs = [
        ("DEC2871_0_contract", "Write exact Q_CAB contract.", "COMPLETE_CONDITIONAL", "Q_CAB must be the Gauss/source charge of L_CAB C_AB=J_CAB under the shared 4*pi radial Green convention."),
        ("DEC2871_1_acceptance", "Promote Q_CAB to accepted row.", "REJECTED", "operator, source density, boundary policy, units and shared sign/Green owner remain missing."),
        ("DEC2871_2_zero", "Prove Q_CAB=0.", "NOT_PROVEN", "source silence/exact divergence and boundary silence are not parent-signed."),
        ("DEC2871_3_runner", "Unlock A_total runner.", "REFUSED", "Q_CAB is still unaccepted and the rest of the first triplet is also missing."),
        ("DEC2871_4_next", "Move to q_R_eff single-row source equation.", "SELECTED_2872", "Q_CAB now has the narrowest possible request; the next numerator leg should receive the same focused treatment."),
    ]
    return [
        add_common(
            {
                "decision_id": decision_id,
                "decision": decision,
                "result": result,
                "because": because,
            }
        )
        for decision_id, decision, result, because in specs
    ]


def next_rows() -> list[dict[str, Any]]:
    return [
        add_common(
            {
                "next_id": "NEXT2871_0_2872",
                "status": "selected_primary",
                "target_doc": "2872-Y5-R2FR-qReff-parent-source-equation-or-finite-row-under-AX1090.md",
                "target_script": "scripts/Y5_R2FR_qReff_parent_source_equation_or_finite_row_under_AX1090_2872.py",
                "mission": "focus on q_R_eff only: derive/source L_R delta_R=J_R and q_R_eff as a finite compact-source Green charge or parent-zero theorem, including S_R/Z_R, ell_R/long-range limit, boundary policy, units, source path and equation anchor; no A_total scoring until the whole first triplet passes",
                "selected": True,
            }
        )
    ]


def branch_rows() -> list[dict[str, Any]]:
    specs = [
        ("COPY2871_0_law", OUTPUTS["source_law"], BRANCH_OUTPUTS["law_copy"], "Q_CAB conditional source-equation audit nonclaim copy"),
        ("COPY2871_1_request", OUTPUTS["request"], BRANCH_OUTPUTS["request_copy"], "narrow Q_CAB source request nonclaim copy"),
        ("COPY2871_2_template", OUTPUTS["template"], BRANCH_OUTPUTS["template_copy"], "Q_CAB finite-row template nonclaim copy"),
        ("COPY2871_3_next_queue", OUTPUTS["next"], BRANCH_OUTPUTS["next_queue"], "RAB queue handoff to q_R_eff single-row focus"),
    ]
    rows: list[dict[str, Any]] = []
    for copy_id, source_table, copy_path, purpose in specs:
        copy_path.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(source_table, copy_path)
        rows.append(
            add_common(
                {
                    "copy_id": copy_id,
                    "source_table": str(source_table),
                    "copy_path": str(copy_path),
                    "purpose": purpose,
                    "exists": copy_path.exists(),
                }
            )
        )
    return rows


def no_claim_flags(rows_by_name: dict[str, list[dict[str, Any]]]) -> bool:
    forbidden_true_fields = {
        "valid_for_claim",
        "claim_allowed",
        "score_ready",
        "valid_prediction_row",
        "accepted_source_row",
        "finite_numeric_value_present",
        "parent_zero_theorem_present",
        "source_equation_parent_accepted",
        "finite_row_ready",
        "parent_zero_ready",
        "parent_signed",
        "qcab_zero_accepted",
        "ready_for_runner",
        "gate_passed",
        "runner_ready",
        "score_allowed",
    }
    for rows in rows_by_name.values():
        for row in rows:
            for key, value in row.items():
                if key in forbidden_true_fields and str(value).lower() == "true":
                    return False
    return True


def cited_paths_exist(rows_by_name: dict[str, list[dict[str, Any]]]) -> bool:
    path_keys = {"source_path", "source_table", "copy_path"}
    for rows in rows_by_name.values():
        for row in rows:
            for key, value in row.items():
                if key not in path_keys:
                    continue
                if value in {"", None}:
                    continue
                text = str(value)
                if text.startswith("MISSING_"):
                    continue
                if not Path(text).exists():
                    return False
    return True


def template_missing_markers(rows: list[dict[str, Any]]) -> bool:
    if not rows:
        return False
    return all(any(str(value).startswith("MISSING_") for value in row.values()) for row in rows)


def generated_under_root() -> bool:
    paths = list(OUTPUTS.values()) + list(BRANCH_OUTPUTS.values()) + [DOC]
    for path in paths:
        try:
            path.resolve().relative_to(ROOT.resolve())
        except ValueError:
            return False
    return True


def formalization_untouched() -> bool:
    if not FORMALIZATION.exists():
        return True
    for path in FORMALIZATION.rglob("*"):
        if path.is_file():
            modified = datetime.fromtimestamp(path.stat().st_mtime, timezone.utc)
            if modified > SCRIPT_START_UTC:
                return False
    return True


def pycache_absent() -> bool:
    return not (ROOT / "scripts" / "__pycache__").exists()


def remove_pycache() -> None:
    pycache = ROOT / "scripts" / "__pycache__"
    if pycache.exists():
        shutil.rmtree(pycache)


def validation_rows(rows_by_name: dict[str, list[dict[str, Any]]]) -> list[dict[str, Any]]:
    output_paths = [path for path in OUTPUTS.values() if path != OUTPUTS["validation"]]
    branch_paths = list(BRANCH_OUTPUTS.values())
    checks = [
        ("VAL2871_0_sources_exist", all(row["path_exists"] for row in rows_by_name["sources"]), "all registered source paths exist"),
        ("VAL2871_1_source_anchors", all(row["anchors_found"] for row in rows_by_name["sources"]), "all registered source anchors were found"),
        ("VAL2871_2_evidence_review_complete", len(rows_by_name["review"]) >= 8 and all(not row["accepted_source_row"] for row in rows_by_name["review"]), "Q_CAB evidence reviewed and none accepted"),
        ("VAL2871_3_source_contract_written", any(row["law_id"] == "LAW2871_1_operator_source_contract" and row["derived_status"] == "DERIVED_CONDITIONAL_CONTRACT" for row in rows_by_name["source_law"]), "conditional L_CAB/J_CAB source contract written"),
        ("VAL2871_4_source_law_not_accepted", all(not row["source_equation_parent_accepted"] for row in rows_by_name["source_law"]), "source law remains nonclaim until parent clauses close"),
        ("VAL2871_5_zero_not_proven", all(not row["qcab_zero_accepted"] for row in rows_by_name["zero_audit"]), "Q_CAB parent-zero theorem remains unproved"),
        ("VAL2871_6_template_nonclaim_missing_markers", template_missing_markers(rows_by_name["template"]) and all(not row["ready_for_runner"] for row in rows_by_name["template"]), "finite row template contains explicit MISSING markers and is not runner-ready"),
        ("VAL2871_7_gates_fail_closed", all(not row["gate_passed"] for row in rows_by_name["gates"]), "all Q_CAB acceptance gates fail closed"),
        ("VAL2871_8_request_open", rows_by_name["request"][0]["status"] == "OPEN_SOURCE_REQUEST", "narrow Q_CAB source request emitted"),
        ("VAL2871_9_runner_refused", all(row["status"] == "REFUSED" and not row["runner_ready"] for row in rows_by_name["runner"]), "runner remains refused"),
        ("VAL2871_10_next_target_2872", rows_by_name["next"][0]["next_id"] == "NEXT2871_0_2872", "q_R_eff single-row focus selected next"),
        ("VAL2871_11_outputs_exist", all(path.exists() for path in output_paths), "all generated CSV outputs exist before validation write"),
        ("VAL2871_12_branch_outputs_exist", all(path.exists() for path in branch_paths), "branch copies were written"),
        ("VAL2871_13_csv_parse", all(csv_parses(path) for path in output_paths), "all generated CSV outputs parse"),
        ("VAL2871_14_cited_paths_exist", cited_paths_exist(rows_by_name), "all cited local paths exist, ignoring explicit MISSING placeholders"),
        ("VAL2871_15_no_claim_flags", no_claim_flags(rows_by_name), "no claim/score/prediction flags are true"),
        ("VAL2871_16_generated_under_post_checkpoint", generated_under_root(), "all generated artifacts remain under post-checkpoint-work"),
        ("VAL2871_17_formalization_untouched", formalization_untouched(), "formalization-workbench was not modified during this run"),
        ("VAL2871_18_pycache_absent", pycache_absent(), "scripts __pycache__ absent during validation"),
    ]
    rows = [
        {
            "validation_id": validation_id,
            "passed": passed,
            "detail": detail,
            "timestamp_utc": now(),
        }
        for validation_id, passed, detail in checks
    ]
    rows.append(
        {
            "validation_id": "VAL2871_OVERALL",
            "passed": all(row["passed"] for row in rows),
            "detail": "2871 wrote the exact conditional Q_CAB source-equation contract, rejected claim promotion, kept A_total locked, emitted the narrow Q_CAB source request, and selected q_R_eff for the next single-row gate.",
            "timestamp_utc": now(),
        }
    )
    return rows


def markdown_table(rows: list[dict[str, Any]], columns: list[str]) -> str:
    header = "| " + " | ".join(columns) + " |"
    separator = "| " + " | ".join("---" for _ in columns) + " |"
    lines = [header, separator]
    for row in rows:
        values = [str(row.get(column, "")).replace("\n", " ") for column in columns]
        lines.append("| " + " | ".join(values) + " |")
    return "\n".join(lines)


def write_doc(rows: dict[str, list[dict[str, Any]]]) -> None:
    lines = [
        "# 2871 - Y5 R2FR Q_CAB Parent Source Equation Or Finite Row Under AX1090",
        "",
        "Status: `Y5_R2FR_2871_QCAB_conditional_source_contract_written_parent_row_not_accepted_qReff_next`",
        "",
        "## Private Verdict",
        "",
        "2871 narrowed the `Q_CAB` problem to an exact contract rather than a vague gap. The clean conditional law is:",
        "",
        "`L_CAB C_AB=J_CAB` and `C_AB=Q_CAB/(4*pi*r)+regular` imply `Q_CAB=int_W J_CAB dV + surface_integral_boundary B_CAB`, with the sign and `4*pi` normalization owned by the same exterior Green convention used for `q_R_eff`.",
        "",
        "That is a useful derivation target, not yet a claim. The corpus still lacks the parent-owned `L_CAB`, `J_CAB/rho_CAB`, boundary/corner policy, units, branch id, and shared Green/sign convention. `Q_CAB=0` also remains unproved because source silence, exact-divergence/cohomology, and boundary silence are not parent-signed.",
        "",
        "`A_total` therefore stays locked. The next best attack is to give `q_R_eff` the same single-row treatment, because Q_CAB now has the narrowest source request we can honestly write.",
        "",
        "## Source Register",
        "",
        markdown_table(rows["sources"], ["source_id", "role", "path_exists", "anchors_found", "missing_anchors", "valid_for_claim"]),
        "",
        "## Q_CAB Evidence Review",
        "",
        markdown_table(rows["review"], ["review_id", "quantity", "source_path", "source_anchor", "verdict", "accepted_source_row", "reason_not_accepted", "valid_for_claim"]),
        "",
        "## Source Equation Audit",
        "",
        markdown_table(rows["source_law"], ["law_id", "clause", "derived_status", "parent_status", "missing_for_claim", "source_equation_parent_accepted", "valid_for_claim"]),
        "",
        "## Parent Zero Audit",
        "",
        markdown_table(rows["zero_audit"], ["zero_id", "theorem_route", "current_status", "blocker", "parent_signed", "qcab_zero_accepted", "valid_for_claim"]),
        "",
        "## Finite Row Template",
        "",
        markdown_table(rows["template"], ["template_id", "quantity", "value", "units", "source_path", "equation_anchor", "ready_for_runner", "valid_for_claim"]),
        "",
        "## Acceptance Gates",
        "",
        markdown_table(rows["gates"], ["gate_id", "criterion", "result", "reason", "gate_passed", "valid_for_claim"]),
        "",
        "## Narrow Source Request",
        "",
        markdown_table(rows["request"], ["request_id", "quantity", "needed_source", "narrow_request", "status", "ready_for_runner", "valid_for_claim"]),
        "",
        "## Runner Status",
        "",
        markdown_table(rows["runner"], ["runner_id", "status", "accepted_qcab_rows", "required_qcab_rows", "accepted_first_triplet_rows", "required_first_triplet_rows", "reason", "runner_ready", "score_allowed", "valid_for_claim"]),
        "",
        "## Decision Ledger",
        "",
        markdown_table(rows["decision"], ["decision_id", "decision", "result", "because", "valid_for_claim"]),
        "",
        "## Next Target",
        "",
        markdown_table(rows["next"], ["next_id", "status", "target_doc", "target_script", "mission", "selected", "valid_for_claim"]),
        "",
        "## Branch Copies",
        "",
        markdown_table(rows["branches"], ["copy_id", "source_table", "copy_path", "purpose", "exists", "valid_for_claim"]),
        "",
        "## Validation",
        "",
        markdown_table(rows["validation"], ["validation_id", "passed", "detail", "timestamp_utc"]),
        "",
    ]
    DOC.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    rows: dict[str, list[dict[str, Any]]] = {}
    rows["sources"] = source_register_rows()
    rows["review"] = evidence_review_rows()
    rows["source_law"] = source_law_rows()
    rows["zero_audit"] = zero_audit_rows()
    rows["template"] = template_rows()
    rows["gates"] = gate_rows()
    rows["request"] = request_rows()
    rows["runner"] = runner_rows()
    rows["decision"] = decision_rows()
    rows["next"] = next_rows()

    for key in ["sources", "review", "source_law", "zero_audit", "template", "gates", "request", "runner", "decision", "next"]:
        write_csv(OUTPUTS[key], rows[key])

    rows["branches"] = branch_rows()
    write_csv(OUTPUTS["branches"], rows["branches"])
    remove_pycache()
    rows["validation"] = validation_rows(rows)
    write_csv(OUTPUTS["validation"], rows["validation"])
    write_doc(rows)

    overall = next(row for row in rows["validation"] if row["validation_id"] == "VAL2871_OVERALL")
    print(f"wrote {DOC}")
    print(f"VAL2871_OVERALL={overall['passed']}")


if __name__ == "__main__":
    main()

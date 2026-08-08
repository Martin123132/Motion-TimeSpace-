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

DOC = ROOT / "2863-Y5-R2FR-QCAB-first-source-row-or-parent-zero-owner-under-AX1090.md"

SRC_2862_DOC = ROOT / "2862-Y5-R2FR-first-row-source-request-pack-and-sigmaR-disambiguation-under-AX1090.md"
SRC_2862_NEXT = RESIDUALS / "P8_Y5_R2FR_2862_NEXT_TARGET.csv"
SRC_2862_REQUESTS = RESIDUALS / "P8_Y5_R2FR_2862_FIRST_ROW_SOURCE_REQUEST_PACK.csv"
SRC_2862_VALIDATION = RESIDUALS / "P8_Y5_BRR545_2862_VALIDATION.csv"
SRC_2844_DOC = ROOT / "2844-Y5-R2FR-CAB-one-over-r-amplitude-law-or-parent-cancellation-theorem-under-AX1090.md"
SRC_2844_FLUX = RESIDUALS / "P8_Y5_R2FR_2844_CAB_GREEN_FLUX_IDENTITY.csv"
SRC_2844_PACK = RESIDUALS / "P8_Y5_R2FR_2844_CAB_AMPLITUDE_SOURCE_PACK.csv"
SRC_2844_CONTRACT = RESIDUALS / "P8_Y5_R2FR_2844_PARENT_AMPLITUDE_CONTRACT.csv"
SRC_2849_SCAN = RESIDUALS / "P8_Y5_R2FR_2849_CORE_AMPLITUDE_SOURCE_SCAN.csv"
SRC_2849_ZERO = RESIDUALS / "P8_Y5_R2FR_2849_PARENT_ZERO_OWNER_ATTEMPT.csv"
SRC_2850_HUNT = RESIDUALS / "P8_Y5_R2FR_2850_PARENT_EQUATION_HUNT_LEDGER.csv"
SRC_2850_DOC = ROOT / "2850-Y5-R2FR-core-amplitude-parent-source-equation-hunt-or-manual-source-ledger-under-AX1090.md"
SRC_2851_DOC = ROOT / "2851-Y5-R2FR-minimal-parent-amplitude-owner-ansatz-or-no-go-under-AX1090.md"
SRC_2852_OWNER = RESIDUALS / "P8_Y5_R2FR_2852_OWNER_ACCEPTANCE_TEST.csv"
SRC_2854_SCAN = RESIDUALS / "P8_Y5_R2FR_2854_REAL_SOURCE_ACQUISITION_SCAN.csv"
SRC_2854_BLOCKER = RESIDUALS / "P8_Y5_R2FR_2854_BLOCKER_LEDGER.csv"
SRC_1078_DOC = ROOT / "1078-Y5-R10-parent-action-object-language-measure-current-owner-proof-stack.md"
SRC_1884_DOC = ROOT / "1884-Y5-R2FR-no-boundary-charge-source-descent-or-delta-p-input-contract.md"
SRC_2631_DOC = ROOT / "2631-Y5-R2FR-current-branch-no-shadow-full-PPN-vector-or-residual-kernel-fill.md"

OUTPUTS = {
    "sources": RESIDUALS / "P8_Y5_R2FR_2863_SOURCE_REGISTER.csv",
    "evidence": RESIDUALS / "P8_Y5_R2FR_2863_QCAB_SOURCE_EVIDENCE_SCAN.csv",
    "zero_audit": RESIDUALS / "P8_Y5_R2FR_2863_QCAB_PARENT_ZERO_PROOF_AUDIT.csv",
    "acceptance": RESIDUALS / "P8_Y5_R2FR_2863_QCAB_ACCEPTANCE_GATE.csv",
    "template": RESIDUALS / "P8_Y5_R2FR_2863_QCAB_FIRST_ROW_TEMPLATE_NONCLAIM.csv",
    "blockers": RESIDUALS / "P8_Y5_R2FR_2863_QCAB_BLOCKER_LEDGER.csv",
    "decision": RESIDUALS / "P8_Y5_R2FR_2863_DECISION_LEDGER.csv",
    "next": RESIDUALS / "P8_Y5_R2FR_2863_NEXT_TARGET.csv",
    "branches": RESIDUALS / "P8_Y5_R2FR_2863_BRANCH_COPIES.csv",
    "validation": RESIDUALS / "P8_Y5_BRR545_2863_VALIDATION.csv",
}

BRANCH_OUTPUTS = {
    "evidence_copy": LOCAL_BOUNDS / "RAB_QCAB_SOURCE_EVIDENCE_SCAN_2863_NONCLAIM.csv",
    "blocker_copy": SOURCE_WEIGHT / "RAB_QCAB_BLOCKER_LEDGER_2863_NONCLAIM.csv",
    "next_queue": RAB_QUEUE / "JR2863_qReff_first_source_or_parent_normalization_NEXT.csv",
    "template_copy": BETA_DOCS / "RAB_QCAB_FIRST_ROW_TEMPLATE_2863_NONCLAIM.csv",
}

for directory in {path.parent for path in OUTPUTS.values()} | {path.parent for path in BRANCH_OUTPUTS.values()} | {DOC.parent}:
    directory.mkdir(parents=True, exist_ok=True)


def now() -> str:
    return datetime.now(timezone.utc).isoformat()


def bool_text(value: bool) -> str:
    return "True" if value else "False"


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
    if not rows:
        path.write_text("", encoding="utf-8")
        return
    fieldnames: list[str] = []
    for row in rows:
        for key in row:
            if key not in fieldnames:
                fieldnames.append(key)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow(row)


def csv_parses(path: Path) -> bool:
    try:
        with path.open(newline="", encoding="utf-8") as handle:
            list(csv.DictReader(handle))
        return True
    except Exception:
        return False


def source_register_rows() -> list[dict[str, Any]]:
    specs = [
        ("SRC2863_0_2862_doc", SRC_2862_DOC, "NEXT2862_0_2863;VAL2862_OVERALL", "2862 handoff selects Q_CAB hunt"),
        ("SRC2863_1_2862_next", SRC_2862_NEXT, "NEXT2862_0_2863", "selected 2863 next target"),
        ("SRC2863_2_2862_requests", SRC_2862_REQUESTS, "REQ2862_0_Q_CAB;REQ2862_1_q_R_eff", "exact source requests"),
        ("SRC2863_3_2862_validation", SRC_2862_VALIDATION, "VAL2862_OVERALL", "2862 validation"),
        ("SRC2863_4_2844_doc", SRC_2844_DOC, "FLUX2844_2_source_charge;PACK2844_0_Q_CAB;CONTRACT2844_1_source_current", "Q_CAB amplitude law doc"),
        ("SRC2863_5_2844_flux", SRC_2844_FLUX, "FLUX2844_1_surface_amplitude;FLUX2844_2_source_charge;FLUX2844_5_local_suppression_condition", "Gauss/source identities"),
        ("SRC2863_6_2844_pack", SRC_2844_PACK, "PACK2844_0_Q_CAB;PACK2844_1_J_CAB;PACK2844_3_B_CAB", "Q_CAB input slots"),
        ("SRC2863_7_2844_contract", SRC_2844_CONTRACT, "CONTRACT2844_0_operator;CONTRACT2844_1_source_current;CONTRACT2844_2_boundary", "parent amplitude contract"),
        ("SRC2863_8_2849_scan", SRC_2849_SCAN, "SCAN2849_0_Q_CAB;SCAN2849_7_relation", "core amplitude source scan"),
        ("SRC2863_9_2849_zero", SRC_2849_ZERO, "PZ2849_0_charge_balance_condition;PZ2849_6_verdict", "parent zero-owner attempt"),
        ("SRC2863_10_2850_hunt", SRC_2850_HUNT, "HUNT2850_0_Q_CAB;HUNT2850_4_relation", "parent equation hunt"),
        ("SRC2863_11_2850_doc", SRC_2850_DOC, "MAN2850_1_CAB_equation;ROUTE2850_0_shared_parent_current", "manual source ledger and route ranking"),
        ("SRC2863_12_2851_doc", SRC_2851_DOC, "ANS2851_0_general_source_doublet;ALG2851_3_identity;NG2851_3_boundary_shift", "minimal source-doublet ansatz"),
        ("SRC2863_13_2852_owner", SRC_2852_OWNER, "OWN2852_0_ratio_fixed_before_fit;OWN2852_5_verdict", "source-doublet owner acceptance test"),
        ("SRC2863_14_2854_scan", SRC_2854_SCAN, "SCAN2854_0_Q_CAB", "real source acquisition scan"),
        ("SRC2863_15_2854_blocker", SRC_2854_BLOCKER, "BLOCK2854_0_Q_CAB", "Q_CAB blocker"),
        ("SRC2863_16_1078_current_owner", SRC_1078_DOC, "CO1078_3_current_rescaling_counterexample;CO1078_4_verdict", "current-owner obstruction"),
        ("SRC2863_17_1884_boundary", SRC_1884_DOC, "NBC1884_4_no_boundary_charge_parent_signature", "boundary/source descent obstruction"),
        ("SRC2863_18_2631_full_vector", SRC_2631_DOC, "PPNV2631_8_total_abs;RG2631_0_no_gamma_only", "full-vector guard"),
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


def evidence_rows() -> list[dict[str, Any]]:
    rows = [
        {
            "evidence_id": "EVID2863_0_surface_definition",
            "quantity": "Q_CAB",
            "candidate_type": "surface_amplitude_definition",
            "source_path": str(SRC_2844_FLUX),
            "source_anchor": "FLUX2844_1_surface_amplitude",
            "evidence": "A_CAB=-(1/(4*pi))*lim_{R->infty} int R^2 partial_r C_AB dOmega; Q_CAB=4*pi*A_CAB",
            "status": "IDENTITY_ONLY",
            "missing_for_acceptance": "finite value or theorem-zero owner; exterior domain; units; sign and boundary convention",
        },
        {
            "evidence_id": "EVID2863_1_source_integral",
            "quantity": "Q_CAB",
            "candidate_type": "conditional_source_integral",
            "source_path": str(SRC_2844_FLUX),
            "source_anchor": "FLUX2844_2_source_charge",
            "evidence": "if Laplacian C_AB=-rho_CAB, then A_CAB=(1/(4*pi))*int rho_CAB d^3x plus boundary/corner terms",
            "status": "CONDITIONAL_IDENTITY_ONLY",
            "missing_for_acceptance": "parent L_CAB operator; rho_CAB/J_CAB definition; boundary/corner policy; Green convention",
        },
        {
            "evidence_id": "EVID2863_2_pack_slot",
            "quantity": "Q_CAB",
            "candidate_type": "source_pack_slot",
            "source_path": str(SRC_2844_PACK),
            "source_anchor": "PACK2844_0_Q_CAB",
            "evidence": "Q_CAB=4*pi*A_CAB is recorded as integrated target-map monopole charge",
            "status": "MISSING_PARENT_INPUT",
            "missing_for_acceptance": "derive from target current or source as finite row",
        },
        {
            "evidence_id": "EVID2863_3_parent_equation_hunt",
            "quantity": "Q_CAB",
            "candidate_type": "parent_equation_hunt",
            "source_path": str(SRC_2850_HUNT),
            "source_anchor": "HUNT2850_0_Q_CAB",
            "evidence": "definition-only candidate found",
            "status": "FOUND_DEFINITION_ONLY_PARENT_EQUATION_MISSING",
            "missing_for_acceptance": "needs L_CAB C_AB=J_CAB, Q_CAB=int J_CAB with boundary terms and Green normalization",
        },
        {
            "evidence_id": "EVID2863_4_real_acquisition_scan",
            "quantity": "Q_CAB",
            "candidate_type": "real_source_scan",
            "source_path": str(SRC_2854_SCAN),
            "source_anchor": "SCAN2854_0_Q_CAB",
            "evidence": "definition/status row found",
            "status": "NO_ACCEPTED_SOURCE_FOUND",
            "missing_for_acceptance": "no finite numeric Q_CAB and no parent-signed zero theorem",
        },
        {
            "evidence_id": "EVID2863_5_balance_relation",
            "quantity": "Q_CAB",
            "candidate_type": "charge_balance_condition",
            "source_path": str(SRC_2844_FLUX),
            "source_anchor": "FLUX2844_5_local_suppression_condition",
            "evidence": "A_total=0 iff Q_CAB=-sigma_R*q_R_eff",
            "status": "CONDITION_AVAILABLE_PARENT_PROOF_MISSING",
            "missing_for_acceptance": "single parent current/action theorem enforcing relation and fixing normalization",
        },
    ]
    for row in rows:
        row.update(
            {
                "accepted_source_row": False,
                "finite_numeric_value_present": False,
                "theorem_zero_owner_present": False,
            }
        )
    return [add_common(row) for row in rows]


def zero_audit_rows() -> list[dict[str, Any]]:
    rows = [
        {
            "proof_id": "ZP2863_0_gauss_zero_skeleton",
            "theorem_candidate": "Q_CAB=0 from Gauss/source law",
            "required_premise": "int rho_CAB d^3x plus boundary/corner flux equals zero in the parent convention",
            "current_evidence": "FLUX2844_2 gives the conditional integral law",
            "status": "VALID_SKELETON_NOT_PARENT_SIGNED",
            "blocker": "MISSING_RHO_CAB_ZERO_OR_EXACT_DIVERGENCE_AND_BOUNDARY_CERTIFICATE",
        },
        {
            "proof_id": "ZP2863_1_no_source_density",
            "theorem_candidate": "rho_CAB/J_CAB vanishes for ordinary compact matter",
            "required_premise": "parent matter action has no target-map source current in this sector",
            "current_evidence": "PACK2844_1_J_CAB marks source density missing",
            "status": "NOT_DERIVED",
            "blocker": "MISSING_SOURCE_DENSITY_ZERO_THEOREM",
        },
        {
            "proof_id": "ZP2863_2_boundary_silence",
            "theorem_candidate": "boundary/corner flux vanishes or is included in Q_CAB",
            "required_premise": "closed domain or exact boundary primitive with no unowned charge",
            "current_evidence": "CONTRACT2844_2 and NBC1884_4 keep boundary/source descent unsigned",
            "status": "NOT_DERIVED",
            "blocker": "MISSING_BOUNDARY_FLUX_LAW",
        },
        {
            "proof_id": "ZP2863_3_pure_gauge_or_cohomology_zero",
            "theorem_candidate": "C_AB source is pure gauge/exact divergence with zero monopole cohomology",
            "required_premise": "parent gauge/cohomology owner for C_AB and its boundary domain",
            "current_evidence": "no accepted C_AB cohomology/gauge owner found in the Q_CAB source trail",
            "status": "ROUTE_OPEN_BUT_UNSOURCED",
            "blocker": "MISSING_CAB_GAUGE_OR_COHOMOLOGY_OWNER",
        },
        {
            "proof_id": "ZP2863_4_shared_current_balance",
            "theorem_candidate": "Q_CAB=-sigma_R*q_R_eff from a shared parent current",
            "required_premise": "one parent owner fixes both projections and forbids independent rescaling",
            "current_evidence": "2851 gives conditional algebra; 2852 owner tests fail",
            "status": "CONDITIONAL_RELATION_NOT_QCAB_ZERO",
            "blocker": "MISSING_RATIO_OWNER_AND_SIGMA_SOURCE_SIGN",
        },
        {
            "proof_id": "ZP2863_5_rescaling_obstruction",
            "theorem_candidate": "normalization uniqueness for Q_CAB",
            "required_premise": "current rescaling J_A -> c_A J_A is forbidden by parent action",
            "current_evidence": "CO1078_3 says the rescaling counterexample survives",
            "status": "COUNTEREXAMPLE_SURVIVES",
            "blocker": "CURRENT_OWNER_NOT_SIGNED",
        },
        {
            "proof_id": "ZP2863_6_verdict",
            "theorem_candidate": "Q_CAB finite first row or Q_CAB=0 parent theorem",
            "required_premise": "all Q_CAB source, boundary, operator, sign, and owner clauses close",
            "current_evidence": "prior source scans find only symbolic/missing rows",
            "status": "NOT_ACCEPTED",
            "blocker": "Q_CAB_REMAINS_MISSING_PARENT_INPUT",
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


def acceptance_rows() -> list[dict[str, Any]]:
    rows = [
        ("ACC2863_0_value_or_zero", "finite Q_CAB value or theorem-zero owner", "FAIL", "no numeric Q_CAB and no parent-zero theorem"),
        ("ACC2863_1_parent_equation", "L_CAB C_AB=J_CAB with charge integral", "FAIL", "parent target-map equation missing"),
        ("ACC2863_2_green_convention", "same exterior Green normalization as q_R_eff", "FAIL", "common kernel/sign convention not parent-owned"),
        ("ACC2863_3_boundary_policy", "boundary/corner flux zero or included", "FAIL", "boundary flux law missing"),
        ("ACC2863_4_units_branch", "units, sign convention, branch id, source path, equation anchor", "FAIL", "only symbolic/status rows found"),
        ("ACC2863_5_local_claim_guard", "Q_CAB row sufficient for local GR/Newton claim", "FAIL", "q_R_eff, sigma_R_source_sign, GM, tail and full vector remain missing"),
    ]
    return [
        add_common(
            {
                "acceptance_id": acceptance_id,
                "criterion": criterion,
                "result": result,
                "reason": reason,
                "accepted_ready": False,
                "gate_passed": False,
                "runner_ready": False,
            }
        )
        for acceptance_id, criterion, result, reason in rows
    ]


def template_rows() -> list[dict[str, Any]]:
    return [
        add_common(
            {
                "template_id": "TEMPLATE2863_0_Q_CAB_first_row_nonclaim",
                "branch_id": "R2FR_local_PPN_constant_limit_after_Uamp_demotion",
                "quantity": "Q_CAB",
                "value": "MISSING_Q_CAB",
                "units": "MISSING_Q_CAB_UNITS",
                "source_path": "",
                "equation_anchor": "MISSING_Q_CAB_EQUATION_ANCHOR",
                "operator_convention": "MISSING_L_CAB_OPERATOR",
                "green_convention": "MISSING_COMMON_GREEN_CONVENTION",
                "boundary_policy": "MISSING_BOUNDARY_POLICY",
                "sign_convention": "MISSING_SIGN_CONVENTION",
                "parent_zero_owner": "MISSING_PARENT_ZERO_OWNER",
                "first_row_ready": False,
                "accepted_source_row": False,
            }
        )
    ]


def blocker_rows() -> list[dict[str, Any]]:
    specs = [
        ("BLOCK2863_0_Q_CAB_PARENT_INPUT", "Q_CAB", "MISSING_PARENT_INPUT", "derive/source finite target-map monopole charge or parent-zero theorem", "blocks A_total numerator"),
        ("BLOCK2863_1_L_CAB_OPERATOR", "L_CAB", "MISSING_OPERATOR", "supply parent target-map operator and exterior Green kernel", "blocks Q_CAB integral"),
        ("BLOCK2863_2_J_CAB_SOURCE", "rho_CAB/J_CAB", "MISSING_SOURCE_DENSITY", "derive target source density or prove source silence/exact divergence", "blocks finite value or zero proof"),
        ("BLOCK2863_3_B_CAB_BOUNDARY", "B_CAB", "MISSING_BOUNDARY_FLUX_LAW", "prove boundary/corner flux vanishes or include it in Q_CAB", "blocks Gauss charge"),
        ("BLOCK2863_4_GREEN_SIGN", "Q_CAB convention", "MISSING_GREEN_SIGN_CONVENTION", "bind Q_CAB to same convention as q_R_eff and sigma_R_source_sign", "blocks strict runner"),
        ("BLOCK2863_5_PARENT_OWNER", "Q_CAB zero owner", "CURRENT_OWNER_NOT_SIGNED", "close rescaling/source-owner obstruction before theorem-zero", "blocks parent-zero promotion"),
        ("BLOCK2863_6_HANDOFF", "q_R_eff", "NEXT_CORE_ROW_AFTER_QCAB_BLOCKED", "attempt q_R_eff first source row while carrying Q_CAB blocker explicitly", "opens 2864 without claiming Q_CAB"),
    ]
    return [
        add_common(
            {
                "blocker_id": blocker_id,
                "quantity": quantity,
                "blocker_code": blocker_code,
                "required_resolution": required_resolution,
                "blocks": blocks,
                "accepted_source_row": False,
            }
        )
        for blocker_id, quantity, blocker_code, required_resolution, blocks in specs
    ]


def decision_rows() -> list[dict[str, Any]]:
    specs = [
        ("DEC2863_0_scan", "Q_CAB source scan completed.", "NO_ACCEPTED_SOURCE_ROW", "only identities, missing-source rows and conditional relations were found"),
        ("DEC2863_1_zero_skeleton", "Q_CAB zero theorem skeleton written.", "SKELETON_USEFUL_BUT_UNSIGNED", "Gauss/source law shows exactly what would prove zero, but source/boundary/operator clauses are unsigned"),
        ("DEC2863_2_keep_blocker", "Q_CAB remains blocked.", "MISSING_PARENT_INPUT", "do not import symbolic Q_CAB as numeric or theorem-zero evidence"),
        ("DEC2863_3_next", "Move to q_R_eff with Q_CAB blocker carried forward.", "SELECTED_2864", "the next finite row is the other numerator leg of A_total"),
        ("DEC2863_4_no_claim", "No local-GR/Newton/PPN claim.", "LOCKED", "Q_CAB, q_R_eff, sigma_R_source_sign, GM, tail and full-vector rows remain missing"),
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
                "next_id": "NEXT2863_0_2864",
                "status": "selected_primary",
                "target_doc": "2864-Y5-R2FR-qReff-first-source-row-or-parent-normalization-owner-under-AX1090.md",
                "target_script": "scripts/Y5_R2FR_qReff_first_source_row_or_parent_normalization_owner_under_AX1090_2864.py",
                "mission": "attempt to extract a real q_R_eff finite Green charge or parent normalization owner in the same convention as Q_CAB; carry Q_CAB as an explicit blocker and refuse A_total scoring until both numerator legs and sigma_R_source_sign are sourced",
                "selected": True,
            }
        )
    ]


def branch_rows() -> list[dict[str, Any]]:
    specs = [
        ("COPY2863_0_evidence", OUTPUTS["evidence"], BRANCH_OUTPUTS["evidence_copy"], "Q_CAB evidence scan nonclaim copy"),
        ("COPY2863_1_blockers", OUTPUTS["blockers"], BRANCH_OUTPUTS["blocker_copy"], "Q_CAB blocker ledger nonclaim copy"),
        ("COPY2863_2_next_queue", OUTPUTS["next"], BRANCH_OUTPUTS["next_queue"], "RAB queue handoff to 2864"),
        ("COPY2863_3_template", OUTPUTS["template"], BRANCH_OUTPUTS["template_copy"], "Q_CAB first-row template nonclaim copy"),
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
        "qcab_zero_accepted",
        "theorem_zero_owner_present",
        "finite_numeric_value_present",
        "first_row_ready",
        "accepted_ready",
        "gate_passed",
        "runner_ready",
    }
    for rows in rows_by_name.values():
        for row in rows:
            for key, value in row.items():
                if key in forbidden_true_fields and str(value).lower() == "true":
                    return False
    return True


def cited_paths_exist(rows_by_name: dict[str, list[dict[str, Any]]]) -> bool:
    for rows in rows_by_name.values():
        for row in rows:
            for key, value in row.items():
                if not key.endswith("_path") and key not in {"source_table", "copy_path"}:
                    continue
                if value in {"", None}:
                    continue
                path_text = str(value)
                if path_text.startswith("scripts/") or path_text.startswith("scripts\\"):
                    continue
                if not Path(path_text).exists():
                    return False
    return True


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


def validation_rows(rows_by_name: dict[str, list[dict[str, Any]]]) -> list[dict[str, Any]]:
    output_paths = [path for path in OUTPUTS.values() if path != OUTPUTS["validation"]]
    branch_paths = list(BRANCH_OUTPUTS.values())
    checks = [
        ("VAL2863_0_sources_exist", all(row["path_exists"] for row in rows_by_name["sources"]), "all registered source paths exist"),
        ("VAL2863_1_source_anchors", all(row["anchors_found"] for row in rows_by_name["sources"]), "all registered anchors were found"),
        ("VAL2863_2_evidence_scan_covers_QCAB", len(rows_by_name["evidence"]) >= 6 and any(row["source_anchor"] == "FLUX2844_2_source_charge" for row in rows_by_name["evidence"]), "Q_CAB evidence scan covers surface/source/pack/hunt/relation rows"),
        ("VAL2863_3_no_accepted_QCAB_row", all(not row["accepted_source_row"] for row in rows_by_name["evidence"]), "no Q_CAB finite source row was accepted"),
        ("VAL2863_4_zero_proof_rejected", any(row["proof_id"] == "ZP2863_6_verdict" and row["status"] == "NOT_ACCEPTED" for row in rows_by_name["zero_audit"]), "Q_CAB zero theorem remains unsigned"),
        ("VAL2863_5_acceptance_gates_fail_closed", all(not row["gate_passed"] for row in rows_by_name["acceptance"]), "all Q_CAB acceptance gates fail closed"),
        ("VAL2863_6_template_blocked", rows_by_name["template"][0]["value"] == "MISSING_Q_CAB" and not rows_by_name["template"][0]["first_row_ready"], "Q_CAB template remains nonclaim"),
        ("VAL2863_7_blocker_written", any(row["blocker_id"] == "BLOCK2863_0_Q_CAB_PARENT_INPUT" for row in rows_by_name["blockers"]), "explicit Q_CAB blocker written"),
        ("VAL2863_8_next_target_2864", rows_by_name["next"][0]["next_id"] == "NEXT2863_0_2864" and "q_R_eff" in rows_by_name["next"][0]["mission"], "q_R_eff first-source target selected"),
        ("VAL2863_9_outputs_exist", all(path.exists() for path in output_paths), "all generated output paths exist before validation write"),
        ("VAL2863_10_branch_outputs_exist", all(path.exists() for path in branch_paths), "branch copies were written"),
        ("VAL2863_11_csv_parse", all(csv_parses(path) for path in output_paths), "all generated CSV outputs parse"),
        ("VAL2863_12_cited_paths_exist", cited_paths_exist(rows_by_name), "all cited local file/copy paths in generated rows exist"),
        ("VAL2863_13_no_claim_flags", no_claim_flags(rows_by_name), "no claim/score/prediction flags are true"),
        ("VAL2863_14_generated_under_post_checkpoint", generated_under_root(), "all generated artifacts remain under post-checkpoint-work"),
        ("VAL2863_15_formalization_untouched", formalization_untouched(), "formalization-workbench was not modified during this run"),
        ("VAL2863_16_pycache_absent", pycache_absent(), "scripts __pycache__ absent during validation"),
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
    overall = all(row["passed"] for row in rows)
    rows.append(
        {
            "validation_id": "VAL2863_OVERALL",
            "passed": overall,
            "detail": "2863 found no accepted Q_CAB source row or parent-zero owner, wrote the exact Q_CAB proof blockers, kept all claims blocked, and selected q_R_eff first-source acquisition for 2864.",
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
        "# 2863 - Y5 R2FR Q_CAB First Source Row Or Parent Zero-Owner Under AX1090",
        "",
        "Status: `Y5_R2FR_2863_QCAB_no_first_row_zero_owner_unsigned_qReff_next`",
        "",
        "## Private Verdict",
        "",
        "2863 tried the narrow derivation-first route for `Q_CAB`.",
        "",
        "The exact skeleton is clean:",
        "",
        "```text",
        "C_AB(r)=A_CAB/r+C_AB_reg(r)",
        "Q_CAB:=4*pi*A_CAB",
        "if L_CAB C_AB=-rho_CAB in the shared Green convention,",
        "then Q_CAB = integral rho_CAB d^3x + boundary/corner flux",
        "```",
        "",
        "So a parent theorem could set `Q_CAB=0` by proving source silence/exact divergence plus boundary silence, or could supply a finite numeric row by sourcing the charge integral. The current corpus does neither. The strongest result remains the conditional balance target `Q_CAB=-sigma_R_source_sign*q_R_eff`, not a parent-owned theorem.",
        "",
        "The strict runner therefore stays blocked. `Q_CAB` is carried forward as an explicit blocker, and the next finite route is `q_R_eff` source/normalization acquisition.",
        "",
        "## Source Register",
        "",
        markdown_table(rows["sources"], ["source_id", "role", "path_exists", "anchors_found", "missing_anchors", "valid_for_claim"]),
        "",
        "## Q_CAB Source Evidence Scan",
        "",
        markdown_table(rows["evidence"], ["evidence_id", "candidate_type", "source_anchor", "status", "missing_for_acceptance", "accepted_source_row", "valid_for_claim"]),
        "",
        "## Parent Zero Proof Audit",
        "",
        markdown_table(rows["zero_audit"], ["proof_id", "theorem_candidate", "status", "blocker", "parent_signed", "qcab_zero_accepted", "valid_for_claim"]),
        "",
        "## Q_CAB Acceptance Gate",
        "",
        markdown_table(rows["acceptance"], ["acceptance_id", "criterion", "result", "reason", "gate_passed", "valid_for_claim"]),
        "",
        "## First Row Template",
        "",
        markdown_table(rows["template"], ["template_id", "quantity", "value", "operator_convention", "boundary_policy", "parent_zero_owner", "first_row_ready", "valid_for_claim"]),
        "",
        "## Q_CAB Blocker Ledger",
        "",
        markdown_table(rows["blockers"], ["blocker_id", "quantity", "blocker_code", "required_resolution", "blocks", "valid_for_claim"]),
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
    rows["evidence"] = evidence_rows()
    rows["zero_audit"] = zero_audit_rows()
    rows["acceptance"] = acceptance_rows()
    rows["template"] = template_rows()
    rows["blockers"] = blocker_rows()
    rows["decision"] = decision_rows()
    rows["next"] = next_rows()

    for key in ["sources", "evidence", "zero_audit", "acceptance", "template", "blockers", "decision", "next"]:
        write_csv(OUTPUTS[key], rows[key])

    rows["branches"] = branch_rows()
    write_csv(OUTPUTS["branches"], rows["branches"])
    rows["validation"] = validation_rows(rows)
    write_csv(OUTPUTS["validation"], rows["validation"])
    write_doc(rows)

    overall = next(row for row in rows["validation"] if row["validation_id"] == "VAL2863_OVERALL")
    print(f"wrote {DOC}")
    print(f"VAL2863_OVERALL={bool_text(bool(overall['passed']))}")


if __name__ == "__main__":
    main()

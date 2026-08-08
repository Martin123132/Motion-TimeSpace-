from __future__ import annotations

import csv
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


CHECKPOINT = "2710"
BRANCH_ID = "Y5_R2FR_PARENT_ACTION_OWNER_CONSTRUCTION_SOURCE_HUNT_OR_FALSIFIER_TEST_2710"
START_UTC = datetime.now(timezone.utc)

ROOT = Path(__file__).resolve().parents[1]
SOURCE_INTAKE = ROOT / "source-intake"
RESIDUALS = SOURCE_INTAKE / "mts_residuals"
LOCAL_BOUNDS = SOURCE_INTAKE / "local_bounds"
SOURCE_WEIGHT = SOURCE_INTAKE / "source-weight"
RAB_QUEUE = SOURCE_INTAKE / "rab-sector" / "acquisition-queue"
FORMALIZATION_WORKBENCH = ROOT.parent / "formalization-workbench"

DOC_PATH = ROOT / "2710-Y5-R2FR-parent-action-owner-construction-source-hunt-or-falsifier-test.md"

OUTPUTS = {
    "source_register": RESIDUALS / "P8_Y5_R2FR_2710_SOURCE_REGISTER.csv",
    "owner_source_hunt": RESIDUALS / "P8_Y5_R2FR_2710_OWNER_SOURCE_HUNT.csv",
    "parent_object_normal_form": RESIDUALS / "P8_Y5_R2FR_2710_PARENT_OBJECT_NORMAL_FORM.csv",
    "owner_clause_audit": RESIDUALS / "P8_Y5_R2FR_2710_OWNER_CLAUSE_AUDIT.csv",
    "irreducible_falsifier_gate": RESIDUALS / "P8_Y5_R2FR_2710_IRREDUCIBLE_FALSIFIER_GATE.csv",
    "branch_decision": RESIDUALS / "P8_Y5_R2FR_2710_BRANCH_DECISION.csv",
    "claim_gates": RESIDUALS / "P8_Y5_R2FR_2710_CLAIM_GATES.csv",
    "next_target": RESIDUALS / "P8_Y5_R2FR_2710_NEXT_TARGET.csv",
    "project_status": RESIDUALS / "P8_Y5_R2FR_2710_PROJECT_STATUS_SNAPSHOT.csv",
    "branch_copies": RESIDUALS / "P8_Y5_R2FR_2710_BRANCH_COPIES.csv",
    "validation": RESIDUALS / f"P8_Y5_BRR545_{CHECKPOINT}_VALIDATION.csv",
}

BRANCH_OUTPUTS = {
    "local_owner_gate": LOCAL_BOUNDS / "parent_action_owner_gate_2710_NONCLAIM.csv",
    "source_weight_parent_object": SOURCE_WEIGHT / "AX1090_0_PARENT_OBJECT_OWNER_GATE_2710_NONCLAIM.csv",
    "rab_next": RAB_QUEUE / "JR2710_PARENT_OBJECT_AXIOM_DERIVATION_NEXT.csv",
}

SOURCE_SPECS: list[dict[str, Any]] = [
    {
        "source_id": "SRC2710_2709_HANDOFF",
        "relative_path": "2709-Y5-R2FR-minimal-parent-action-signature-synthesis-or-closure-falsification.md",
        "required_needles": ["MPS2709_A_strict_quotient_EH_topological_vertical", "FAL2709_0_no_single_parent_owner", "NEXT2709_0_selected"],
        "purpose": "imports parent-action owner source-hunt target",
    },
    {
        "source_id": "SRC2710_1008_THETA_QTAU",
        "relative_path": "1008-Y5-R10-parent-theta-Qtau-extraction-or-charge-decomposition-runner.md",
        "required_needles": ["PVA1008_0_parent_action", "PVA1008_2_J_tau", "PVA1008_6_verdict"],
        "purpose": "imports parent variation/theta/Q_tau extraction failure",
    },
    {
        "source_id": "SRC2710_1009_CURRENT_CHAIN",
        "relative_path": "1009-Y5-R10-parent-current-chain-action-contract-or-sector-variation-runner.md",
        "required_needles": ["PCS1009_9_total_parent_contract", "SVC1009_6_total_parent_switch_unsigned", "DEC1009_0_contract_not_parent_action"],
        "purpose": "imports total parent-current-chain contract and refusal",
    },
    {
        "source_id": "SRC2710_1018_SECTOR_OWNER",
        "relative_path": "1018-Y5-R10-sector-Lagrangian-boundary-owner-or-FB5540-source-row.md",
        "required_needles": ["LOC1018_0_LX_owner", "LOC1018_8_verdict", "RT1018_5_verdict"],
        "purpose": "imports sector Lagrangian/boundary owner map and closure failure",
    },
    {
        "source_id": "SRC2710_1023_QVX_DEMOTION",
        "relative_path": "1023-Y5-R10-q-vX-action-descent-certificate-or-scalar-nohair-demotion.md",
        "required_needles": ["QVC1023_8_verdict", "DEM1023_0_scope", "DEC1023_2_future_reopen"],
        "purpose": "imports q/vX/action certificate demotion",
    },
    {
        "source_id": "SRC2710_1029_NO_SHADOW",
        "relative_path": "1029-Y5-R10-cg-no-shadow-frame-theorem-or-first-numeric-coupling-row.md",
        "required_needles": ["NST1029_6_verdict", "CE1029_0_scalar_tensor_common_frame", "CGATE1029_1_cg_zero"],
        "purpose": "imports no-shadow-frame conditional theorem and common-frame counterexample",
    },
    {
        "source_id": "SRC2710_1089_MOMS_COVERAGE",
        "relative_path": "source-intake/mts_residuals/P8_Y5_R10_1089_MOMS_CLAUSE_COVERAGE_MATRIX.csv",
        "required_needles": ["MOMS1088_7_all_in_one", "NO_PARENT_SIGNATURE_SOURCE_FOUND", "derive one parent ordinary-matter action signature"],
        "purpose": "imports all-in-one MOMS source hunt failure",
    },
    {
        "source_id": "SRC2710_1090_SYNTHESIS",
        "relative_path": "source-intake/mts_residuals/P8_Y5_R10_1090_SYNTHESIS_ATTEMPT.csv",
        "required_needles": ["SYN1090_1_action_object", "SYN1090_8_verdict", "SYNTHESIS_FAILS_MISSING_AXIOMS"],
        "purpose": "imports MOMS synthesis failure and parent-object missing axiom",
    },
    {
        "source_id": "SRC2710_1090_AXIOMS",
        "relative_path": "source-intake/mts_residuals/P8_Y5_R10_1090_MISSING_AXIOM_LEDGER.csv",
        "required_needles": ["AX1090_0_parent_object", "MISSING_AXIOM_NOT_ADOPTED", "AX1090_4_variation_domain_order"],
        "purpose": "imports exact missing axioms not adopted as claims",
    },
    {
        "source_id": "SRC2710_1106_CLOSURE_PACK",
        "relative_path": "1106-Y5-R10-minimal-explicit-closure-pack-independence-audit-or-first-source-backed-coefficient-row.md",
        "required_needles": ["MIN1106_A", "MIN1106_B", "DEC1106_0_pack_reduction"],
        "purpose": "imports reduced closure pack and non-adoption decision",
    },
    {
        "source_id": "SRC2710_1276_EH_FIXED_POINT",
        "relative_path": "1276-Y5-R10-RAB-parent-Euler-source-map-contract-or-closure-baseline-scorecard.md",
        "required_needles": ["ESC1276_1_local_EH_fixed_point", "PG1276_0_EH_fixed_point", "CANDIDATE_NOT_DERIVED"],
        "purpose": "imports local EH fixed-point scaffold and blocked promotion gate",
    },
    {
        "source_id": "SRC2710_990_PARENT_CONTRACT",
        "relative_path": "source-intake/mts_residuals/P8_Y5_R10_990_PARENT_ACTION_CONTRACT.csv",
        "required_needles": ["PAC990_0_parent_fields_and_quotient", "PAC990_5_Ward_Bianchi", "PAC990_6_PPN_readout"],
        "purpose": "imports local GR/Newton parent action requirements",
    },
]


def stamp() -> str:
    return datetime.now(timezone.utc).isoformat()


def as_bool(value: bool) -> str:
    return "true" if value else "false"


def path_for(relative_path: str) -> Path:
    return ROOT / relative_path


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace") if path.exists() else ""


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        raise ValueError(f"Refusing to write empty CSV: {path}")
    fieldnames = list(rows[0].keys())
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def parse_csv(path: Path) -> tuple[bool, int, str]:
    try:
        with path.open(newline="", encoding="utf-8") as handle:
            reader = csv.DictReader(handle)
            rows = list(reader)
            if not reader.fieldnames:
                return False, 0, "missing_header"
            return True, len(rows), "parsed"
    except Exception as exc:
        return False, 0, f"{type(exc).__name__}: {exc}"


def markdown_table(rows: list[dict[str, Any]]) -> str:
    if not rows:
        return "_No rows._"
    headers = list(rows[0].keys())
    lines = ["| " + " | ".join(headers) + " |", "| " + " | ".join("---" for _ in headers) + " |"]
    for row in rows:
        cells = [str(row.get(header, "")).replace("|", "\\|").replace("\n", "<br>") for header in headers]
        lines.append("| " + " | ".join(cells) + " |")
    return "\n".join(lines)


def source_register_rows() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for spec in SOURCE_SPECS:
        path = path_for(spec["relative_path"])
        text = read_text(path)
        needles = list(spec["required_needles"])
        found = [needle for needle in needles if needle in text]
        missing = [needle for needle in needles if needle not in text]
        rows.append(
            {
                "source_id": spec["source_id"],
                "relative_path": spec["relative_path"],
                "absolute_path": str(path),
                "exists": as_bool(path.exists()),
                "required_needles": ";".join(needles),
                "found_needles": ";".join(found),
                "missing_needles": ";".join(missing),
                "purpose": spec["purpose"],
                "valid_for_claim": "false",
                "timestamp_utc": stamp(),
            }
        )
    return rows


def owner_source_hunt_rows() -> list[dict[str, Any]]:
    return [
        {
            "hunt_id": "HUNT2710_0_2709_candidate",
            "candidate_source": "2709 MPS2709_A",
            "owner_coverage": "single target skeleton for q, V, EH observed branch, MOMS matter, boundary, Ward/Bianchi, H_tau",
            "source_status": "THEOREM_TARGET_NOT_SOURCE",
            "what_it_gives": "a coherent normal form for the parent action we need",
            "what_it_does_not_give": "actual parent variation, sector certificates, or H_tau source ownership",
            "owner_acquired": "false",
            "valid_for_claim": "false",
            "timestamp_utc": stamp(),
        },
        {
            "hunt_id": "HUNT2710_1_1009_total_parent",
            "candidate_source": "1009 PCS1009_9/SVC1009_6",
            "owner_coverage": "total parent current-chain contract",
            "source_status": "CONTRACT_REJECTED_WITHOUT_SECTOR_CERTIFICATES",
            "what_it_gives": "required form delta S_parent=E_A delta Phi^A+d theta_MTS and J_tau=dQ_tau^MTS+C_tau",
            "what_it_does_not_give": "existing action source, sector stress/Euler/boundary/tau certificates",
            "owner_acquired": "false",
            "valid_for_claim": "false",
            "timestamp_utc": stamp(),
        },
        {
            "hunt_id": "HUNT2710_2_1008_noether",
            "candidate_source": "1008 PVA1008",
            "owner_coverage": "theta_MTS, J_tau, Q_tau^MTS shape",
            "source_status": "FORMAL_SHAPE_NO_OWNER",
            "what_it_gives": "Noether/current extraction formula that any parent action must satisfy",
            "what_it_does_not_give": "full sector variation and tau action across metric, matter, representative, boundary/reference fields",
            "owner_acquired": "false",
            "valid_for_claim": "false",
            "timestamp_utc": stamp(),
        },
        {
            "hunt_id": "HUNT2710_3_1018_sector_owner",
            "candidate_source": "1018 LOC1018 owner map",
            "owner_coverage": "L_X, Theta_X/Q_X, boundary class, tau, MHref",
            "source_status": "OWNER_MAP_SHARP_NO_CLOSURE",
            "what_it_gives": "exact list of local source-charge owners needed for FB5540/local GR",
            "what_it_does_not_give": "parent-signed L_X, boundary differentiability, tau lock, MHref/source equality",
            "owner_acquired": "false",
            "valid_for_claim": "false",
            "timestamp_utc": stamp(),
        },
        {
            "hunt_id": "HUNT2710_4_1023_qvx",
            "candidate_source": "1023 q/vX certificate",
            "owner_coverage": "q, v_X, action descent, matter descent, boundary silence, degree count",
            "source_status": "CERTIFICATE_FAILS_CURRENT_MTS",
            "what_it_gives": "future reopen condition for the clean quotient no-pole route",
            "what_it_does_not_give": "field-by-field vertical action, parent action descent, boundary silence, degree count",
            "owner_acquired": "false",
            "valid_for_claim": "false",
            "timestamp_utc": stamp(),
        },
        {
            "hunt_id": "HUNT2710_5_1089_1090_MOMS",
            "candidate_source": "1089 coverage and 1090 synthesis",
            "owner_coverage": "ordinary matter action signature",
            "source_status": "NO_PARENT_SIGNATURE_SOURCE_FOUND",
            "what_it_gives": "clause-by-clause evidence that all MOMS pieces are named",
            "what_it_does_not_give": "one parent ordinary-matter action signature or missing axioms AX1090_0..4",
            "owner_acquired": "false",
            "valid_for_claim": "false",
            "timestamp_utc": stamp(),
        },
        {
            "hunt_id": "HUNT2710_6_1276_EH_fixed_point",
            "candidate_source": "1276 A511/local EH fixed point scaffold",
            "owner_coverage": "local EH fixed point and Euler/source map",
            "source_status": "CANDIDATE_NOT_DERIVED",
            "what_it_gives": "least-ad-hoc route to inherit GR Euler equations if A511 blocks close",
            "what_it_does_not_give": "parent-signed local EH fixed point, Euler pair, source map, or boundary no-charge theorem",
            "owner_acquired": "false",
            "valid_for_claim": "false",
            "timestamp_utc": stamp(),
        },
        {
            "hunt_id": "HUNT2710_7_verdict",
            "candidate_source": "integrated source hunt",
            "owner_coverage": "full MPS2709_A parent action owner",
            "source_status": "OWNER_NOT_ACQUIRED",
            "what_it_gives": "the exact first irreducible missing object is isolated",
            "what_it_does_not_give": "local GR/Newton derivation",
            "owner_acquired": "false",
            "valid_for_claim": "false",
            "timestamp_utc": stamp(),
        },
    ]


def parent_object_normal_form_rows() -> list[dict[str, Any]]:
    return [
        {
            "normal_id": "PO2710_0_parent_object",
            "object": "one parent action object before readout",
            "required_normal_form": "S_parent[Phi,Psi;theta]=int_M L_parent(Phi,dPhi,Psi,dPsi,theta)+int_boundary B_parent with Conf_parent, boundary class, and readout maps declared before variation",
            "why_first": "without a single owner, contracts for q, matter, source charge, and boundary cannot promote each other",
            "current_status": "AX1090_0_PARENT_OBJECT_MISSING",
            "promotion_condition": "derive the parent object from MTS primitives or mark it as an explicit closure axiom",
            "valid_for_claim": "false",
            "timestamp_utc": stamp(),
        },
        {
            "normal_id": "PO2710_1_variation_owner",
            "object": "first variation and Noether current",
            "required_normal_form": "delta L_parent=E_A delta Phi^A+d theta_MTS(delta Phi); J_tau=theta_MTS(L_tau Phi)-i_tau L_parent=dQ_tau^MTS+C_tau",
            "why_first": "H_tau/source charge, Ward/Bianchi, and boundary flux require theta/Q ownership",
            "current_status": "FORMAL_SHAPE_NO_OWNER",
            "promotion_condition": "extract theta_MTS and Q_tau^MTS sector-by-sector from the same S_parent",
            "valid_for_claim": "false",
            "timestamp_utc": stamp(),
        },
        {
            "normal_id": "PO2710_2_qV_owner",
            "object": "quotient and vertical sector",
            "required_normal_form": "q:Conf_parent->Q_obs, V=ker(Dq), v_X in V, and V is gauge/topological/constrained or retained with a degree count",
            "why_first": "no-pole/source-zero route depends on X being representative data rather than a local physical pole",
            "current_status": "CONDITIONAL_NOT_PARENT_SIGNED",
            "promotion_condition": "field-by-field v_X action, presymplectic null/constraint algebra, boundary differentiability, and degree count",
            "valid_for_claim": "false",
            "timestamp_utc": stamp(),
        },
        {
            "normal_id": "PO2710_3_matter_domain",
            "object": "ordinary matter functor and action measure",
            "required_normal_form": "S_matter=sum_A S_A[Psi_A,E(q(Phi)),Omega(E),A_obs(q(Phi)),theta_A] with one measure/current normalization, fixed theta_A, no w_A(X), no shadow frame, no marker/domain slot",
            "why_first": "this is the only clean way to make qbar_XT/J_matter/c_g structural zeros",
            "current_status": "MOMS_CONDITIONAL_NOT_DERIVED",
            "promotion_condition": "derive AX1090_1..4 or retain finite coefficient rows",
            "valid_for_claim": "false",
            "timestamp_utc": stamp(),
        },
        {
            "normal_id": "PO2710_4_boundary_readout",
            "object": "boundary/domain/readout order",
            "required_normal_form": "all boundary charges, support shifts, domain selectors, projector tails, and readout maps are varied before projection or retained as explicit residual vectors",
            "why_first": "representative zero cannot become observed zero unless this is signed",
            "current_status": "MISSING_BOUNDARY_DOMAIN_CERTIFICATE",
            "promotion_condition": "prove zero-flux/no-charge/readout-order theorem or source absolute residual rows",
            "valid_for_claim": "false",
            "timestamp_utc": stamp(),
        },
        {
            "normal_id": "PO2710_5_Htau_source",
            "object": "Hamiltonian source charge and Newtonian source equality",
            "required_normal_form": "H_tau=int_S Q_tau^MTS + fixed reference terms, integrable with tau_source=tau_clock=tau_readout and M_H_ref not imported from orbital GM",
            "why_first": "Newton/PPN/local-GR require measured source mass from the same parent current chain",
            "current_status": "MISSING_HTAU_OWNER",
            "promotion_condition": "derive integrability, fixed reference, tau lock, source support, and Poisson/Gauss bridge",
            "valid_for_claim": "false",
            "timestamp_utc": stamp(),
        },
        {
            "normal_id": "PO2710_6_local_EH_readout",
            "object": "EH fixed point and weak-field readout",
            "required_normal_form": "S_parent|local=S_EH[g_obs,kappa0]+S_matter[psi,g_obs]+silent/topological extras+boundary, then derive Euler pair, Poisson/Newton, and PPN vector",
            "why_first": "this is the actual GR/Newton reduction, not just source-zero",
            "current_status": "CANDIDATE_NOT_DERIVED",
            "promotion_condition": "parent-sign A511-style action blocks and prove extra first variations vanish or are bounded",
            "valid_for_claim": "false",
            "timestamp_utc": stamp(),
        },
        {
            "normal_id": "PO2710_7_verdict",
            "object": "parent owner normal form closure",
            "required_normal_form": "PO2710_0 through PO2710_6 close in one branch",
            "why_first": "this is the exact contract a future parent action must satisfy",
            "current_status": "NOT_CLOSED",
            "promotion_condition": "derive one branch or explicitly demote local transition route to closure-only",
            "valid_for_claim": "false",
            "timestamp_utc": stamp(),
        },
    ]


def owner_clause_audit_rows() -> list[dict[str, Any]]:
    return [
        {
            "clause_id": "AUD2710_0_parent_object",
            "clause": "AX1090_0 parent object",
            "best_source": "1090 AX1090_0; 1009 PCS1009_9",
            "audit_result": "MISSING_AXIOM_NOT_ADOPTED",
            "first_order_priority": "1",
            "why_priority": "all other owner clauses rely on a single action object before readout",
            "claim_pass": "false",
            "valid_for_claim": "false",
            "timestamp_utc": stamp(),
        },
        {
            "clause_id": "AUD2710_1_variation",
            "clause": "delta L, theta_MTS, Q_tau^MTS",
            "best_source": "1008 PVA1008; 1009 sector contract",
            "audit_result": "FORMAL_SHAPE_NO_OWNER",
            "first_order_priority": "2",
            "why_priority": "source charge and Ward/Bianchi cannot be evaluated without theta/Q",
            "claim_pass": "false",
            "valid_for_claim": "false",
            "timestamp_utc": stamp(),
        },
        {
            "clause_id": "AUD2710_2_qV",
            "clause": "q, V=ker(Dq), field-by-field vertical generator and degree count",
            "best_source": "1023 q/vX certificate; 1018 no-pole quotient route",
            "audit_result": "CONDITIONAL_CERTIFICATE_FAILS_CURRENT_MTS",
            "first_order_priority": "3",
            "why_priority": "needed to kill the local X pole structurally",
            "claim_pass": "false",
            "valid_for_claim": "false",
            "timestamp_utc": stamp(),
        },
        {
            "clause_id": "AUD2710_3_matter",
            "clause": "MOMS/ordinary matter action signature",
            "best_source": "1089 coverage; 1090 synthesis; 1088 theorem",
            "audit_result": "NO_PARENT_SIGNATURE_SOURCE_FOUND",
            "first_order_priority": "4",
            "why_priority": "needed to kill qbar_XT/J_matter/c_g",
            "claim_pass": "false",
            "valid_for_claim": "false",
            "timestamp_utc": stamp(),
        },
        {
            "clause_id": "AUD2710_4_boundary",
            "clause": "boundary/domain/readout silence",
            "best_source": "1018 owner map; 1023 demotion; 2709 falsifier ledger",
            "audit_result": "MISSING_BOUNDARY_DOMAIN_CERTIFICATE",
            "first_order_priority": "5",
            "why_priority": "needed before representative zero can become observed zero",
            "claim_pass": "false",
            "valid_for_claim": "false",
            "timestamp_utc": stamp(),
        },
        {
            "clause_id": "AUD2710_5_EH_Newton",
            "clause": "local EH fixed point and H_tau source equality",
            "best_source": "1276 EH fixed point; 990 GR/Newton ladder",
            "audit_result": "CANDIDATE_NOT_DERIVED_NOT_REACHED",
            "first_order_priority": "6",
            "why_priority": "actual local GR/Newton proof lives here after parent owner gates",
            "claim_pass": "false",
            "valid_for_claim": "false",
            "timestamp_utc": stamp(),
        },
        {
            "clause_id": "AUD2710_6_verdict",
            "clause": "current parent action owner acquisition",
            "best_source": "integrated 2710 hunt",
            "audit_result": "OWNER_NOT_ACQUIRED_FIRST_GATE_AX1090_0",
            "first_order_priority": "verdict",
            "why_priority": "the first irreducible target is to derive or explicitly adopt/demote the parent action object",
            "claim_pass": "false",
            "valid_for_claim": "false",
            "timestamp_utc": stamp(),
        },
    ]


def irreducible_falsifier_rows() -> list[dict[str, Any]]:
    return [
        {
            "falsifier_id": "F2710_0_first_gate",
            "falsifier": "no single parent action object whose domain is defined before readout/projection/fitting",
            "source_basis": "AX1090_0_parent_object plus SVC1009_6_total_parent_switch_unsigned",
            "falsifies_now": "current derivation of MPS2709_A as a theorem",
            "does_not_falsify": "MPS2709_A as a future theorem target or explicit closure axiom",
            "repair": "derive AX1090_0 from MTS primitives or explicitly demote the local transition route to closure-only",
            "status": "FIRST_IRREDUCIBLE_GATE",
            "valid_for_claim": "false",
            "timestamp_utc": stamp(),
        },
        {
            "falsifier_id": "F2710_1_sector_certificates",
            "falsifier": "declaring S_parent=sum sectors without each sector field list, first variation, stress, boundary, tau action and source path",
            "source_basis": "1009 SVR1009_6 refusal",
            "falsifies_now": "total parent switch shortcut",
            "does_not_falsify": "a future sector-by-sector derivation",
            "repair": "supply sector certificates or reduce to a smaller parent action with explicit retained residuals",
            "status": "ACTIVE_BLOCKER",
            "valid_for_claim": "false",
            "timestamp_utc": stamp(),
        },
        {
            "falsifier_id": "F2710_2_MOMS_axioms",
            "falsifier": "ordinary matter signature requires missing axioms AX1090_1 through AX1090_4",
            "source_basis": "1090 missing axiom ledger",
            "falsifies_now": "qbar_XT/J_matter/c_g zero as derived theorem",
            "does_not_falsify": "conditional MOMS theorem",
            "repair": "derive no-hidden-visible hom, common measure/current owner, fixed constants, and variation-before-readout",
            "status": "ACTIVE_BLOCKER",
            "valid_for_claim": "false",
            "timestamp_utc": stamp(),
        },
        {
            "falsifier_id": "F2710_3_Htau_source",
            "falsifier": "H_tau/Q_tau/M_H_ref source charge is formal, not owned or integrable",
            "source_basis": "1008 PVA1008 and 1018 LOC1018_6/7",
            "falsifies_now": "Newton/source normalization pass",
            "does_not_falsify": "EH comparison shape as a template",
            "repair": "derive theta/Q_tau and source equality without importing orbital GM",
            "status": "ACTIVE_BLOCKER",
            "valid_for_claim": "false",
            "timestamp_utc": stamp(),
        },
    ]


def branch_decision_rows() -> list[dict[str, Any]]:
    return [
        {
            "decision_id": "DEC2710_0_owner_hunt",
            "decision": "PARENT_ACTION_OWNER_NOT_ACQUIRED",
            "rationale": "many contracts and candidate scaffolds exist, but no source signs the one parent object before readout with sector variations and source charge",
            "claim_effect": "no C_X, qbar_XT, c_g, Newton, PPN, R10, WEP, clock, orbital or local-GR claim",
            "next_action": "attack AX1090_0 parent object directly",
            "valid_for_claim": "false",
            "timestamp_utc": stamp(),
        },
        {
            "decision_id": "DEC2710_1_first_gate",
            "decision": "FIRST_IRREDUCIBLE_GATE_IS_AX1090_0_PARENT_OBJECT",
            "rationale": "without the parent action object, deriving no-shadow, MOMS, boundary silence, or H_tau can only produce conditional subtheorems",
            "claim_effect": "downstream gates stay blocked until AX1090_0 is derived or explicitly adopted as closure",
            "next_action": "2711 derive AX1090_0 from MTS primitive action grammar or demote the local transition route",
            "valid_for_claim": "false",
            "timestamp_utc": stamp(),
        },
        {
            "decision_id": "DEC2710_2_project_read",
            "decision": "NOT_DEAD_BUT_NOW_AT_PARENT_OBJECT_LEVEL",
            "rationale": "no hard contradiction to a strict parent branch was found; the problem has moved upstream to whether MTS can own the parent action rather than insert it",
            "claim_effect": "project remains viable as a theorem target but not claim-ready",
            "next_action": "stop circling coupling coefficients until parent object is tried",
            "valid_for_claim": "false",
            "timestamp_utc": stamp(),
        },
    ]


def claim_gate_rows() -> list[dict[str, Any]]:
    return [
        {
            "claim_gate_id": "CG2710_0_owner_source",
            "gate": "parent action owner acquired",
            "status": "FAIL_OWNER_NOT_ACQUIRED",
            "gate_passed": "false",
            "claim_allowed": "false",
            "reason": "AX1090_0 parent object remains missing/not adopted",
            "timestamp_utc": stamp(),
        },
        {
            "claim_gate_id": "CG2710_1_normal_form",
            "gate": "exact parent owner normal form written",
            "status": "PASS_CONTRACT_ONLY",
            "gate_passed": "true",
            "claim_allowed": "false",
            "reason": "normal form is a future proof contract, not evidence",
            "timestamp_utc": stamp(),
        },
        {
            "claim_gate_id": "CG2710_2_local_GR",
            "gate": "local GR/Newton/PPN re-entry",
            "status": "FAIL_NOT_REACHED",
            "gate_passed": "false",
            "claim_allowed": "false",
            "reason": "local EH fixed point and H_tau source equality remain downstream and unsigned",
            "timestamp_utc": stamp(),
        },
        {
            "claim_gate_id": "CG2710_3_finite_tests",
            "gate": "finite local empirical rows score-ready",
            "status": "FAIL_DEFERRED",
            "gate_passed": "false",
            "claim_allowed": "false",
            "reason": "finite coefficients/projections remain nonclaim and should not replace parent derivation yet",
            "timestamp_utc": stamp(),
        },
        {
            "claim_gate_id": "CG2710_4_private",
            "gate": "GitHub/public action",
            "status": "PRIVATE_NO_ACTION",
            "gate_passed": "false",
            "claim_allowed": "false",
            "reason": "private checkpoint only",
            "timestamp_utc": stamp(),
        },
    ]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        {
            "next_id": "NEXT2710_0_selected",
            "selection": "selected_primary",
            "target_doc": "2711-Y5-R2FR-AX1090-parent-object-derivation-from-MTS-primitives-or-explicit-closure.md",
            "target_script": "scripts/Y5_R2FR_AX1090_parent_object_derivation_from_MTS_primitives_or_explicit_closure_2711.py",
            "task": "try to derive AX1090_0: one parent action object whose configuration/domain/readout order is defined before variation from MTS primitives; if this cannot be derived, mark it as an explicit local-transition closure axiom and route downstream local-GR work accordingly",
            "success_condition": "either AX1090_0 is parent-derived from existing MTS primitive action grammar with source paths and variation domain, or the local parent-action route is explicitly closure-only at the parent-object level",
            "forbidden_shortcuts": "declare S_parent by taste; import EH as total parent action; use MOMS/no-shadow closure as proof; claim GR/Newton; run local empirical passes with placeholders; GitHub action; formalization-workbench edits",
            "valid_for_claim": "false",
            "timestamp_utc": stamp(),
        }
    ]


def project_status_rows() -> list[dict[str, Any]]:
    return [
        {
            "status_id": "STATUS2710_0_level",
            "topic": "derivation level",
            "status": "UPSTREAM_PARENT_OBJECT_GATE",
            "meaning": "the next proof is not another coefficient/coupling check; it is whether MTS derives one parent action object before readout",
            "next_action": "derive or closure-label AX1090_0",
            "claim_allowed": "false",
            "timestamp_utc": stamp(),
        },
        {
            "status_id": "STATUS2710_1_viability",
            "topic": "project risk",
            "status": "VIABLE_THEOREM_TARGET_NOT_CLAIM_READY",
            "meaning": "the strict route remains coherent, but it lives or dies on parent-object ownership",
            "next_action": "attack primitive action grammar",
            "claim_allowed": "false",
            "timestamp_utc": stamp(),
        },
        {
            "status_id": "STATUS2710_2_empirical",
            "topic": "testing",
            "status": "DEFER_LOCAL_TEST_CLAIMS",
            "meaning": "SPARC/cosmology may still be useful elsewhere, but local-GR/R10/PPN testing should wait for parent object or finite source rows",
            "next_action": "no placeholder local claims",
            "claim_allowed": "false",
            "timestamp_utc": stamp(),
        },
        {
            "status_id": "STATUS2710_3_private",
            "topic": "public/GitHub",
            "status": "NO_ACTION_PRIVATE",
            "meaning": "all artifacts remain private in post-checkpoint-work",
            "next_action": "keep private",
            "claim_allowed": "false",
            "timestamp_utc": stamp(),
        },
    ]


def branch_copy_rows() -> list[dict[str, Any]]:
    return [
        {
            "copy_id": key,
            "path": str(path),
            "relative_path": str(path.relative_to(ROOT)),
            "exists_after_run": as_bool(path.exists()),
            "valid_for_claim": "false",
            "timestamp_utc": stamp(),
        }
        for key, path in BRANCH_OUTPUTS.items()
    ]


def formalization_recent_change_count() -> int:
    if not FORMALIZATION_WORKBENCH.exists():
        return 0
    threshold = START_UTC.timestamp() - 2.0
    count = 0
    for path in FORMALIZATION_WORKBENCH.rglob("*"):
        try:
            if path.is_file() and path.stat().st_mtime >= threshold:
                count += 1
        except OSError:
            continue
    return count


def validate(generated_paths: dict[str, Path], rows_by_name: dict[str, list[dict[str, Any]]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []

    def add(check_id: str, passed: bool, detail: str) -> None:
        rows.append({"check_id": check_id, "passed": as_bool(passed), "detail": detail, "timestamp_utc": stamp()})

    sources = rows_by_name["source_register"]
    add("VAL2710_0_sources_exist", all(row["exists"] == "true" for row in sources), "all cited local source paths exist")
    add("VAL2710_1_needles_found", all(not row["missing_needles"] for row in sources), "all required source needles were found")

    hunt = rows_by_name["owner_source_hunt"]
    add("VAL2710_2_owner_hunt_verdict", any(row["hunt_id"] == "HUNT2710_7_verdict" and row["source_status"] == "OWNER_NOT_ACQUIRED" for row in hunt), "owner source hunt explicitly fails acquisition")
    add("VAL2710_3_no_owner_acquired", all(row["owner_acquired"] == "false" for row in hunt), "no source-hunt row claims owner acquisition")

    normal = rows_by_name["parent_object_normal_form"]
    add("VAL2710_4_normal_form_complete", len(normal) >= 8 and any(row["normal_id"] == "PO2710_7_verdict" and row["current_status"] == "NOT_CLOSED" for row in normal), "parent object normal form is complete and not closed")
    add("VAL2710_5_normal_form_nonclaim", all(row["valid_for_claim"] == "false" for row in normal), "normal form rows are nonclaim")

    audit = rows_by_name["owner_clause_audit"]
    add("VAL2710_6_first_gate_AX1090", any(row["clause_id"] == "AUD2710_0_parent_object" and row["audit_result"] == "MISSING_AXIOM_NOT_ADOPTED" for row in audit), "AX1090 parent object is first owner gate")
    add("VAL2710_7_no_clause_claims", all(row["claim_pass"] == "false" and row["valid_for_claim"] == "false" for row in audit), "no owner clause claims a pass")

    falsifiers = rows_by_name["irreducible_falsifier_gate"]
    add("VAL2710_8_irreducible_falsifier", any(row["falsifier_id"] == "F2710_0_first_gate" and row["status"] == "FIRST_IRREDUCIBLE_GATE" for row in falsifiers), "first irreducible falsifier gate recorded")
    add("VAL2710_9_claims_blocked", all(row["claim_allowed"] == "false" for row in rows_by_name["claim_gates"]), "all claim gates keep claim_allowed=false")
    add("VAL2710_10_next_2711", any(row["next_id"] == "NEXT2710_0_selected" and "2711" in row["target_doc"] for row in rows_by_name["next_target"]), "2711 target selected")
    add("VAL2710_11_no_formalization_outputs", not any("formalization-workbench" in str(path).lower() for path in generated_paths.values()), "no output path points into formalization-workbench")
    add("VAL2710_12_no_formalization_recent_changes", formalization_recent_change_count() == 0, f"formalization_recent_changed_count={formalization_recent_change_count()}")
    add("VAL2710_13_no_github_outputs", not any(".git" in str(path).lower() or "github" in str(path).lower() for path in generated_paths.values()), "no GitHub/public-output path was written")

    for key, path in generated_paths.items():
        ok, count, detail = parse_csv(path)
        add(f"VAL2710_PARSE_{key}", ok and count > 0, f"{detail}; rows={count}")

    core = [row for row in rows if not row["check_id"].startswith("VAL2710_PARSE_validation")]
    add(
        "VAL2710_OVERALL",
        all(row["passed"] == "true" for row in core),
        "2710 sources the parent-action owner hunt, finds no acquired owner, isolates AX1090_0 parent object as the first irreducible gate, writes the exact parent-object normal form, blocks all claims, and selects AX1090 derivation for 2711",
    )
    return rows


def write_doc(rows_by_name: dict[str, list[dict[str, Any]]]) -> None:
    sections = [
        ("Owner Source Hunt", rows_by_name["owner_source_hunt"]),
        ("Parent Object Normal Form", rows_by_name["parent_object_normal_form"]),
        ("Owner Clause Audit", rows_by_name["owner_clause_audit"]),
        ("Irreducible Falsifier Gate", rows_by_name["irreducible_falsifier_gate"]),
        ("Branch Decisions", rows_by_name["branch_decision"]),
        ("Source Register", rows_by_name["source_register"]),
        ("Claim Gates", rows_by_name["claim_gates"]),
        ("Next Target", rows_by_name["next_target"]),
        ("Project Status", rows_by_name["project_status"]),
        ("Validation", rows_by_name["validation"]),
    ]
    lines = [
        "# 2710: Parent Action Owner Construction Source Hunt Or Falsifier Test",
        "",
        f"**Branch:** `{BRANCH_ID}`",
        "",
        "## Private Verdict",
        "",
        "2710 does not find an acquired parent-action owner. The corpus has strong contracts, useful owner maps, and a coherent 2709 parent-action target, but no single source signs the parent object before readout/projection/fitting with sector variations, boundary class, matter functor, and `H_tau` source charge. The first irreducible gate is now `AX1090_0_parent_object`: either derive the one parent action object from MTS primitives, or demote the local transition route to an explicit closure at the parent-object level.",
        "",
        "## Bottom Line",
        "",
        "- This is progress: the missing object is no longer a foggy coupling; it is the parent action object itself.",
        "- Current result: no local GR/Newton claim, no `qbar_XT=0`, no `c_g=0`, no R10/PPN/WEP/source-charge pass.",
        "- The strict route is not contradicted; it is simply unsigned until `AX1090_0` is derived or closure-labelled.",
        "- Best next move: 2711 attacks `AX1090_0` directly from MTS primitive action grammar.",
        "",
    ]
    for title, rows in sections:
        lines.extend([f"## {title}", "", markdown_table(rows), ""])
    DOC_PATH.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    rows_by_name: dict[str, list[dict[str, Any]]] = {
        "source_register": source_register_rows(),
        "owner_source_hunt": owner_source_hunt_rows(),
        "parent_object_normal_form": parent_object_normal_form_rows(),
        "owner_clause_audit": owner_clause_audit_rows(),
        "irreducible_falsifier_gate": irreducible_falsifier_rows(),
        "branch_decision": branch_decision_rows(),
        "claim_gates": claim_gate_rows(),
        "next_target": next_target_rows(),
        "project_status": project_status_rows(),
    }

    for name, path in OUTPUTS.items():
        if name in {"validation", "branch_copies"}:
            continue
        write_csv(path, rows_by_name[name])

    write_csv(BRANCH_OUTPUTS["local_owner_gate"], rows_by_name["parent_object_normal_form"])
    write_csv(BRANCH_OUTPUTS["source_weight_parent_object"], rows_by_name["owner_clause_audit"])
    write_csv(BRANCH_OUTPUTS["rab_next"], rows_by_name["next_target"])

    branch_rows = branch_copy_rows()
    rows_by_name["branch_copies"] = branch_rows
    write_csv(OUTPUTS["branch_copies"], branch_rows)

    generated_paths = {name: path for name, path in OUTPUTS.items() if name != "validation"}
    generated_paths.update(BRANCH_OUTPUTS)
    validation = validate(generated_paths, rows_by_name)
    rows_by_name["validation"] = validation
    write_csv(OUTPUTS["validation"], validation)

    write_doc(rows_by_name)
    print(f"wrote {DOC_PATH}")
    print(f"wrote {OUTPUTS['validation']}")


if __name__ == "__main__":
    main()

from __future__ import annotations

import csv
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


CHECKPOINT = "2715"
BRANCH_ID = "Y5_R2FR_MINIMAL_WEAK_FIELD_AUXILIARY_ACTION_GATE_UNDER_AX1090_CLOSURE_2715"
START_UTC = datetime.now(timezone.utc)

ROOT = Path(__file__).resolve().parents[1]
SOURCE_INTAKE = ROOT / "source-intake"
RESIDUALS = SOURCE_INTAKE / "mts_residuals"
LOCAL_BOUNDS = SOURCE_INTAKE / "local_bounds"
SOURCE_WEIGHT = SOURCE_INTAKE / "source-weight"
RAB_QUEUE = SOURCE_INTAKE / "rab-sector" / "acquisition-queue"
FORMALIZATION_WORKBENCH = ROOT.parent / "formalization-workbench"

DOC_PATH = ROOT / "2715-Y5-R2FR-minimal-weak-field-auxiliary-action-gate-under-AX1090-closure.md"

OUTPUTS = {
    "source_register": RESIDUALS / "P8_Y5_R2FR_2715_SOURCE_REGISTER.csv",
    "minimal_ansatz_gate": RESIDUALS / "P8_Y5_R2FR_2715_MINIMAL_WEAK_FIELD_ANSATZ_GATE.csv",
    "auxiliary_compatibility_audit": RESIDUALS / "P8_Y5_R2FR_2715_AUXILIARY_COMPATIBILITY_AUDIT.csv",
    "zero_premise_status": RESIDUALS / "P8_Y5_R2FR_2715_QR_BETA_ZERO_PREMISE_STATUS.csv",
    "finite_residual_fallback": RESIDUALS / "P8_Y5_R2FR_2715_FINITE_ZR_QR_FALLBACK.csv",
    "claim_gates": RESIDUALS / "P8_Y5_R2FR_2715_CLAIM_GATES.csv",
    "blocker_stack": RESIDUALS / "P8_Y5_R2FR_2715_CURRENT_BLOCKER_STACK.csv",
    "decision_ledger": RESIDUALS / "P8_Y5_R2FR_2715_DECISION_LEDGER.csv",
    "next_target": RESIDUALS / "P8_Y5_R2FR_2715_NEXT_TARGET.csv",
    "project_status": RESIDUALS / "P8_Y5_R2FR_2715_PROJECT_STATUS_SNAPSHOT.csv",
    "branch_copies": RESIDUALS / "P8_Y5_R2FR_2715_BRANCH_COPIES.csv",
    "validation": RESIDUALS / f"P8_Y5_BRR545_{CHECKPOINT}_VALIDATION.csv",
}

BRANCH_OUTPUTS = {
    "local_bounds_gate": LOCAL_BOUNDS / "minimal_weak_field_auxiliary_gate_2715_NONCLAIM.csv",
    "source_weight_gate": SOURCE_WEIGHT / "finite_ZR_qR_fallback_gate_2715_NONCLAIM.csv",
    "rab_next": RAB_QUEUE / "JR2715_PARENT_PROTECTION_OR_FINITE_ZR_NEXT.csv",
}

SOURCE_SPECS: list[dict[str, Any]] = [
    {
        "source_id": "SRC2715_2714_HANDOFF",
        "relative_path": "2714-Y5-R2FR-lambda-phi-zero-bound-or-Khat-adoption-under-AX1090-closure.md",
        "required_needles": ["WFR2714_1_minimal_ansatz", "WFR2714_2_lambdaR_auxiliary", "NEXT2714_0_selected", "VAL2714_OVERALL"],
        "purpose": "imports the R2FR weak-field auxiliary action target",
    },
    {
        "source_id": "SRC2715_2711_AX1090_CLOSURE",
        "relative_path": "2711-Y5-R2FR-AX1090-parent-object-derivation-from-MTS-primitives-or-explicit-closure.md",
        "required_needles": ["AX1090_0_LC", "NEXT2711_0_selected", "VAL2711_OVERALL"],
        "purpose": "keeps this repair under explicit AX1090 closure rather than parent-object proof",
    },
    {
        "source_id": "SRC2715_1561_MINIMAL_ANSATZ",
        "relative_path": "1561-Y5-minimal-parent-weak-field-action-ansatz-and-Euler-Ward-PPN-gate.md",
        "required_needles": ["ANS1561_A_EH_lambdaR_silent", "EUL1561_1_lambda_variation", "RUN1561_4_claim", "VAL1561_OVERALL"],
        "purpose": "imports the EH + lambda_R R_AB weak-field repair ansatz",
    },
    {
        "source_id": "SRC2715_1562_LAMBDAR_TEST",
        "relative_path": "1562-Y5-lambdaR-parent-origin-zero-stress-and-first-class-constraint-test.md",
        "required_needles": ["ROUTE1562_1_second_class_auxiliary", "STR1562_5_current", "GATE1562_4_qR", "VAL1562_OVERALL"],
        "purpose": "imports lambda_R parent-origin/zero-stress and auxiliary route audit",
    },
    {
        "source_id": "SRC2715_1563_AUX_GRAMMAR",
        "relative_path": "1563-Y5-RAB-auxiliary-compatibility-parent-sort-and-no-derivative-grammar.md",
        "required_needles": ["SORT1563_0_auxiliary_coordinate", "GRAM1563_5_verdict", "ELIM1563_4_current", "VAL1563_OVERALL"],
        "purpose": "imports parent sort and no-derivative grammar blockers",
    },
    {
        "source_id": "SRC2715_1564_VERTICAL_NULL",
        "relative_path": "1564-Y5-RAB-vertical-null-presymplectic-degeneracy-or-finite-ZR-intake.md",
        "required_needles": ["NULL1564_5_verdict", "KIN1564_1_null_contradiction", "INTAKE1564_1_accepted", "VAL1564_OVERALL"],
        "purpose": "imports vertical-null exact conditional route and empty finite intake status",
    },
    {
        "source_id": "SRC2715_1567_PROTECTION_CONTRACT",
        "relative_path": "1567-Y5-RAB-parent-protection-contract-or-live-finite-ZR-source-acquisition.md",
        "required_needles": ["CON1567_6_joint_contract", "THM1567_0_statement", "ACQ1567_1_ZR", "VAL1567_OVERALL"],
        "purpose": "imports the joint parent protection contract and finite residual acquisition queue",
    },
    {
        "source_id": "SRC2715_1568_PRIMITIVE_RECHECK",
        "relative_path": "1568-Y5-RAB-parent-contract-derivation-from-MTS-primitives-or-first-live-ZR-row.md",
        "required_needles": ["GAP1568_6_joint", "RUN1568_1_primitive_contract", "COEFF1568_0_ZR", "VAL1568_OVERALL"],
        "purpose": "imports failed primitive derivation and missing internal coefficient status",
    },
    {
        "source_id": "SRC2715_2692_LOCAL_GR_CONTRACT",
        "relative_path": "2692-Y5-R2FR-GR-left-hand-Einstein-Newton-limit-or-operator-residual-pack.md",
        "required_needles": ["LHS2692_9_verdict", "NP2692_7_verdict", "ORP2692_10_total_abs_envelope", "VAL2692_OVERALL"],
        "purpose": "imports exact conditional GR/Newton contract and operator residual discipline",
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
                "claim_allowed": "false",
                "timestamp_utc": stamp(),
            }
        )
    return rows


def minimal_ansatz_gate_rows() -> list[dict[str, Any]]:
    return [
        {
            "gate_id": "MWA2715_0_ansatz",
            "candidate_action": "S_EH[g_obs] + S_matter[g_obs,Psi] + int sqrt(-g) lambda_R R_AB + S_silent[Phi,g_obs] + S_boundary",
            "conditional_payoff": "delta_{lambda_R} gives R_AB=0, hence q_R=0, and EH weak-field core gives beta=1 if source/readout is owned",
            "current_status": "BEST_CONDITIONAL_ANSATZ_NOT_ADOPTED",
            "why_not_adopted": "AX1090 is closure-only; lambda_R parent origin/zero-stress, source charge, boundary reference, extra-sector silence and MTS symbol match are unsigned",
            "source_anchor": "1561 ANS1561_A_EH_lambdaR_silent; 2714 WFR2714_1_minimal_ansatz",
            "valid_for_claim": "false",
            "claim_allowed": "false",
            "timestamp_utc": stamp(),
        },
        {
            "gate_id": "MWA2715_1_lambda_variation",
            "candidate_action": "int sqrt(-g) lambda_R R_AB",
            "conditional_payoff": "variation with respect to lambda_R formally enforces R_AB=0",
            "current_status": "FORMAL_PASS_ONLY",
            "why_not_adopted": "a multiplier that enforces the desired closure is not a derivation unless parent origin and stress silence are proved",
            "source_anchor": "1561 EUL1561_1_lambda_variation; 1562 ORG1562_0_delta_lambda",
            "valid_for_claim": "false",
            "claim_allowed": "false",
            "timestamp_utc": stamp(),
        },
        {
            "gate_id": "MWA2715_2_beta_completion",
            "candidate_action": "EH weak-field sector plus universal matter/source readout",
            "conditional_payoff": "second-order weak-field completion yields beta=1",
            "current_status": "CONDITIONAL_EH_PASS_BLOCKED",
            "why_not_adopted": "source/Pi_M/Hilbert charge equality, boundary reference, and MTS adoption remain unsigned; EH cannot be imported as proof",
            "source_anchor": "1561 WPPN1561_2_beta; 2692 NP2692_6_ppn_extension",
            "valid_for_claim": "false",
            "claim_allowed": "false",
            "timestamp_utc": stamp(),
        },
        {
            "gate_id": "MWA2715_3_AX1090_status",
            "candidate_action": "minimal ansatz under AX1090_0_LC",
            "conditional_payoff": "organizes the weak-field proof attempt without pretending the parent object was derived",
            "current_status": "CLOSURE_ORGANIZER_NOT_PARENT_PROOF",
            "why_not_adopted": "2711 explicitly marks AX1090_0 as closure-only",
            "source_anchor": "2711 AX1090_0_LC; 2715 source register",
            "valid_for_claim": "false",
            "claim_allowed": "false",
            "timestamp_utc": stamp(),
        },
    ]


def auxiliary_compatibility_audit_rows() -> list[dict[str, Any]]:
    return [
        {
            "audit_id": "AUX2715_0_second_class_route",
            "condition": "R_AB and Lambda_R form an auxiliary compatibility pair eliminated before readout",
            "mathematical_effect": "can remove q_R hair without a propagating reciprocal scalar",
            "current_status": "EXACT_CONDITIONAL_NOT_PARENT_SIGNED",
            "missing_to_promote": "parent sort, no-derivative grammar, matter descent, boundary silence, readout stability",
            "source_anchor": "1562 ROUTE1562_1_second_class_auxiliary; 1563 ELIM1563_4_current",
            "valid_for_claim": "false",
            "claim_allowed": "false",
            "timestamp_utc": stamp(),
        },
        {
            "audit_id": "AUX2715_1_parent_sort",
            "condition": "R_AB is typed as auxiliary/vertical compatibility coordinate, not physical scalar",
            "mathematical_effect": "blocks physical kinetic terms by sort rather than by wish",
            "current_status": "CANDIDATE_NOT_PARENT_SIGNED",
            "missing_to_promote": "typed parent field list derived from MTS primitives",
            "source_anchor": "1563 SORT1563_0_auxiliary_coordinate; 1568 GAP1568_0_sorts",
            "valid_for_claim": "false",
            "claim_allowed": "false",
            "timestamp_utc": stamp(),
        },
        {
            "audit_id": "AUX2715_2_no_derivative_grammar",
            "condition": "no D R_AB, no D Lambda_R, no vertical metric/connection constructors",
            "mathematical_effect": "would set Z_R/M_R^2 derivative residuals to zero at parent grammar level",
            "current_status": "REQUIRED_UNSIGNED",
            "missing_to_promote": "operator-exhaustion theorem from parent action image",
            "source_anchor": "1563 GRAM1563_5_verdict; 1567 CON1567_5_operator_exclusion",
            "valid_for_claim": "false",
            "claim_allowed": "false",
            "timestamp_utc": stamp(),
        },
        {
            "audit_id": "AUX2715_3_vertical_null_route",
            "condition": "R_AB is parent presymplectic-null with no boundary charge",
            "mathematical_effect": "nonzero Z_R |D R_AB|^2 contradicts nullness",
            "current_status": "CONDITIONAL_CONTRADICTION_WRITTEN_NOT_PARENT_PROVED",
            "missing_to_promote": "parent theta/Omega/v_R and zero boundary charge",
            "source_anchor": "1564 NULL1564_5_verdict; 1564 KIN1564_1_null_contradiction",
            "valid_for_claim": "false",
            "claim_allowed": "false",
            "timestamp_utc": stamp(),
        },
        {
            "audit_id": "AUX2715_4_joint_contract",
            "condition": "CON1567_0 through CON1567_5 all parent-signed",
            "mathematical_effect": "J_R=B_R=readout_regen=Z_R=0 and second-class route closes",
            "current_status": "CONTRACT_WRITTEN_NOT_SIGNED",
            "missing_to_promote": "primitive derivation of typed sorts, action image, matter descent, boundary descent, readout closure and operator exclusion",
            "source_anchor": "1567 CON1567_6_joint_contract; 1567 THM1567_0_statement",
            "valid_for_claim": "false",
            "claim_allowed": "false",
            "timestamp_utc": stamp(),
        },
    ]


def zero_premise_status_rows() -> list[dict[str, Any]]:
    return [
        {
            "premise_id": "ZP2715_0_qR_zero",
            "target": "q_R=0",
            "required_route": "R_AB=0 from parent-owned lambda_R/R_AB auxiliary constraint, or Z_R/J_R/B_R theorem-zero",
            "current_status": "BLOCKED_NO_PARENT_ZERO_ROUTE",
            "reason": "lambda_R formal variation works only after parent-origin and zero-stress gates close; auxiliary contract is unsigned",
            "local_claim_effect": "gamma=1 not parent-derived",
            "valid_for_claim": "false",
            "claim_allowed": "false",
            "timestamp_utc": stamp(),
        },
        {
            "premise_id": "ZP2715_1_delta_beta_zero",
            "target": "delta_beta=0",
            "required_route": "EH second-order weak-field completion plus source/readout/boundary ownership",
            "current_status": "BLOCKED_SOURCE_READOUT_AND_ADOPTION",
            "reason": "EH completion is conditional; source charge/Pi_M/boundary and MTS adoption gates remain open",
            "local_claim_effect": "beta=1 not parent-derived",
            "valid_for_claim": "false",
            "claim_allowed": "false",
            "timestamp_utc": stamp(),
        },
        {
            "premise_id": "ZP2715_2_newton_source",
            "target": "Newton/Poisson source normalization",
            "required_route": "Hilbert/source/worldtube/Gauss charge equality before fitted GM",
            "current_status": "BLOCKED_SOURCE_CHARGE_GLUE",
            "reason": "2692 and 1561 keep Pi_M/Hilbert/Hamiltonian source charge equality unsigned",
            "local_claim_effect": "Newton inverse-square law remains conditional",
            "valid_for_claim": "false",
            "claim_allowed": "false",
            "timestamp_utc": stamp(),
        },
        {
            "premise_id": "ZP2715_3_local_GR_total",
            "target": "local GR/Newton/PPN reduction",
            "required_route": "q_R=0, delta_beta=0, source normalization, boundary/reference, no extra-sector residuals and q_loc/DeltaK closure",
            "current_status": "NOT_DERIVED_BOUNDED_CLOSURE_CONTROL_ONLY",
            "reason": "minimal ansatz is a repair target under AX1090 closure, not a signed MTS parent action",
            "local_claim_effect": "no local-GR claim",
            "valid_for_claim": "false",
            "claim_allowed": "false",
            "timestamp_utc": stamp(),
        },
    ]


def finite_residual_fallback_rows() -> list[dict[str, Any]]:
    return [
        {
            "fallback_id": "FRF2715_0_ZR",
            "quantity": "Z_R",
            "meaning": "finite gradient coefficient for R_AB if no-derivative grammar fails",
            "current_status": "MISSING_THEOREM_ZERO_OR_NUMERIC_VALUE",
            "needed_for_score": "source-backed value or theorem-zero; units; normalization; parent action block; source path; arena projection",
            "source_anchor": "1567 ACQ1567_1_ZR; 1568 COEFF1568_0_ZR",
            "valid_for_claim": "false",
            "claim_allowed": "false",
            "timestamp_utc": stamp(),
        },
        {
            "fallback_id": "FRF2715_1_MR2",
            "quantity": "M_R^2",
            "meaning": "mass/screening scale for finite R_AB residual",
            "current_status": "MISSING_INTERNAL_COEFFICIENT",
            "needed_for_score": "parent Hessian or sourced scale defining ell_R=sqrt(Z_R/M_R^2)",
            "source_anchor": "1563 FALL1563_1_MR2; 1567 acquisition queue",
            "valid_for_claim": "false",
            "claim_allowed": "false",
            "timestamp_utc": stamp(),
        },
        {
            "fallback_id": "FRF2715_2_JR_BR",
            "quantity": "J_R;B_R",
            "meaning": "direct source coupling and boundary reciprocal charge",
            "current_status": "MISSING_SOURCE_AND_BOUNDARY_THEOREMS",
            "needed_for_score": "matter descent/source silence or finite coupling row; boundary no-hair or flux bound",
            "source_anchor": "1563 FALL1563_2_JR; 1563 FALL1563_3_BR; 1567 CON1567_3_boundary_functor",
            "valid_for_claim": "false",
            "claim_allowed": "false",
            "timestamp_utc": stamp(),
        },
        {
            "fallback_id": "FRF2715_3_tau_projection",
            "quantity": "tau_R10 or local arena projection kernel",
            "meaning": "map finite R_AB residual into R10/PPN/clock/orbital tests",
            "current_status": "MISSING_INTERNAL_PROJECTION",
            "needed_for_score": "local source path, source anchor, units, normalization and projection; external bounds alone are not coefficients",
            "source_anchor": "1568 NEXT1568_0_1569; 1568 BOUND1568_R10_EOTWASH_PRL_2021",
            "valid_for_claim": "false",
            "claim_allowed": "false",
            "timestamp_utc": stamp(),
        },
    ]


def claim_gate_rows() -> list[dict[str, Any]]:
    gates = [
        ("CG2715_0_minimal_ansatz", "minimal weak-field ansatz adopted as current MTS parent action", "BLOCKED", "AX1090 is closure-only; symbol/source/boundary gates open"),
        ("CG2715_1_lambdaR_origin", "lambda_R parent origin proved", "BLOCKED", "origin remains inserted/motivated, not primitive-derived"),
        ("CG2715_2_lambdaR_stress", "lambda_R/R_AB sector zero-stress", "BLOCKED", "E_R/source/boundary/readout silence not signed"),
        ("CG2715_3_auxiliary_contract", "R_AB auxiliary/no-derivative protection contract", "BLOCKED", "joint contract written but not parent-derived"),
        ("CG2715_4_qR_zero", "q_R=0 parent prediction", "BLOCKED", "no accepted parent zero route"),
        ("CG2715_5_beta_zero", "delta_beta=0 parent prediction", "BLOCKED", "second-order source/readout completion conditional only"),
        ("CG2715_6_finite_fallback", "finite Z_R/q_R residual score-ready", "BLOCKED", "no internal source-backed coefficient/projection row exists"),
        ("CG2715_7_local_GR", "local GR/Newton/PPN reduction", "BLOCKED_NO_CLAIM", "bounded closure control remains the honest status"),
        ("CG2715_8_public_or_github", "public/GitHub action", "BLOCKED", "private checkpoint only"),
    ]
    return [
        {
            "claim_gate_id": gate_id,
            "gate": gate,
            "status": status,
            "gate_passed": "false",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "reason": reason,
            "timestamp_utc": stamp(),
        }
        for gate_id, gate, status, reason in gates
    ]


def blocker_stack_rows() -> list[dict[str, Any]]:
    blockers = [
        ("BLK2715_0_AX1090", "parent object is closure-only", "minimal weak-field action is a repair scaffold, not proof", "derive AX1090 from primitives or keep closure label"),
        ("BLK2715_1_lambdaR", "lambda_R origin and zero-stress missing", "q_R=0 cannot be claimed", "prove auxiliary compatibility or retain bounded q_R"),
        ("BLK2715_2_auxiliary_sort", "R_AB parent sort/no-derivative grammar unsigned", "Z_R=0 cannot be theorem-zero", "derive parent protection contract or source finite Z_R"),
        ("BLK2715_3_source_readout", "source/Pi_M/boundary charge equality missing", "Newton and beta readout remain conditional", "close source/worldtube/Gauss/boundary chain"),
        ("BLK2715_4_extra_sectors", "silent sectors and q_loc/DeltaK unresolved", "local GR cannot be promoted from q_R/beta alone", "continue residual gates after weak-field branch"),
        ("BLK2715_5_finite_rows", "finite Z_R/q_R rows not source-ready", "bounded closure cannot score", "fill theorem-zero or source-backed coefficient/projection row"),
    ]
    return [
        {
            "blocker_id": blocker_id,
            "blocker": blocker,
            "effect": effect,
            "next_action": next_action,
            "valid_for_claim": "false",
            "claim_allowed": "false",
            "timestamp_utc": stamp(),
        }
        for blocker_id, blocker, effect, next_action in blockers
    ]


def decision_ledger_rows() -> list[dict[str, Any]]:
    return [
        {
            "decision_id": "DEC2715_0_ansatz",
            "decision": "Keep the minimal weak-field action ansatz as the best conditional repair scaffold.",
            "rationale": "it is the least-cheaty route to q_R=0 and beta=1 because it states every parent/stress/source/readout premise explicitly",
            "next_action": "do not adopt it until lambda_R/auxiliary/source gates are signed",
            "valid_for_claim": "false",
            "claim_allowed": "false",
            "timestamp_utc": stamp(),
        },
        {
            "decision_id": "DEC2715_1_zero_status",
            "decision": "Do not claim q_R=0 or delta_beta=0.",
            "rationale": "formal variation and EH completion are conditional; parent origin, zero-stress, source normalization and MTS adoption are missing",
            "next_action": "retain q_R/delta_beta bounded closure controls",
            "valid_for_claim": "false",
            "claim_allowed": "false",
            "timestamp_utc": stamp(),
        },
        {
            "decision_id": "DEC2715_2_next",
            "decision": "Attack the parent protection contract or fill the first finite Z_R/tau projection row next.",
            "rationale": "1567/1568 show theorem-zero depends on the joint contract, while fallback scoring needs an internal coefficient/projection rather than external bounds alone",
            "next_action": "run 2716 parent protection contract repair or finite Z_R/tau projection under AX1090 closure",
            "valid_for_claim": "false",
            "claim_allowed": "false",
            "timestamp_utc": stamp(),
        },
        {
            "decision_id": "DEC2715_3_claim_policy",
            "decision": "Keep all local claims private and blocked.",
            "rationale": "this checkpoint improves the derivation gate; it is not a derived GR/Newton result",
            "next_action": "continue disciplined private derivation-first route",
            "valid_for_claim": "false",
            "claim_allowed": "false",
            "timestamp_utc": stamp(),
        },
    ]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        {
            "next_id": "NEXT2715_0_selected",
            "status": "selected_primary",
            "target_doc": "2716-Y5-R2FR-parent-protection-contract-or-finite-ZR-row-under-AX1090-closure.md",
            "target_script": "scripts/Y5_R2FR_parent_protection_contract_or_finite_ZR_row_under_AX1090_closure_2716.py",
            "purpose": "try to parent-sign one clause of the R_AB protection contract under AX1090 closure; if no clause can be signed, create the first strict nonclaim finite Z_R/J_R/B_R/tau projection row with units, source path, normalization and arena map",
            "acceptance_condition": "one protection-contract clause becomes parent-signed or one finite fallback row becomes source-ready nonclaim; no local-GR/PPN/R10 score is claimed",
            "forbidden_shortcuts": "treat external bounds as MTS coefficients; promote closure multiplier to derivation; use placeholder Z_R/M_R/J_R/B_R; score local tests; GitHub action; edit formalization-workbench",
            "ready_to_run": "true",
            "valid_for_claim": "false",
            "claim_allowed": "false",
            "timestamp_utc": stamp(),
        }
    ]


def project_status_rows() -> list[dict[str, Any]]:
    return [
        {
            "status_id": "STATUS2715_0_weak_field",
            "topic": "weak-field parent action",
            "status": "BEST_CONDITIONAL_ANSATZ_NOT_ADOPTED",
            "meaning": "the route is coherent but remains a repair scaffold under AX1090 closure",
            "next_action": "parent-sign protection contract or finite residual row",
            "claim_allowed": "false",
            "timestamp_utc": stamp(),
        },
        {
            "status_id": "STATUS2715_1_qR_beta",
            "topic": "q_R and beta",
            "status": "BOUNDED_CLOSURE_CONTROL",
            "meaning": "q_R=0 and beta=1 are not parent-derived yet",
            "next_action": "keep 1559-style controls while deriving parent gates",
            "claim_allowed": "false",
            "timestamp_utc": stamp(),
        },
        {
            "status_id": "STATUS2715_2_fallback",
            "topic": "finite Z_R/q_R",
            "status": "FALLBACK_ACTIVE_NOT_SCORE_READY",
            "meaning": "finite residual workflow is valid but lacks internal coefficient/projection rows",
            "next_action": "run 2716 finite row/protection contract gate",
            "claim_allowed": "false",
            "timestamp_utc": stamp(),
        },
        {
            "status_id": "STATUS2715_3_private",
            "topic": "public/GitHub",
            "status": "NO_ACTION_PRIVATE",
            "meaning": "no public or GitHub work performed",
            "next_action": "continue in post-checkpoint-work",
            "claim_allowed": "false",
            "timestamp_utc": stamp(),
        },
    ]


def branch_copy_rows() -> list[dict[str, Any]]:
    return [
        {
            "copy_id": "BC2715_0_local_bounds",
            "source_table": "P8_Y5_R2FR_2715_QR_BETA_ZERO_PREMISE_STATUS.csv",
            "copy_path": str(BRANCH_OUTPUTS["local_bounds_gate"]),
            "purpose": "quarantine nonclaim weak-field/local-bound gate",
            "valid_for_claim": "false",
            "claim_allowed": "false",
            "timestamp_utc": stamp(),
        },
        {
            "copy_id": "BC2715_1_source_weight",
            "source_table": "P8_Y5_R2FR_2715_FINITE_ZR_QR_FALLBACK.csv",
            "copy_path": str(BRANCH_OUTPUTS["source_weight_gate"]),
            "purpose": "quarantine nonclaim finite ZR/qR fallback gate",
            "valid_for_claim": "false",
            "claim_allowed": "false",
            "timestamp_utc": stamp(),
        },
        {
            "copy_id": "BC2715_2_rab_queue",
            "source_table": "P8_Y5_R2FR_2715_NEXT_TARGET.csv",
            "copy_path": str(BRANCH_OUTPUTS["rab_next"]),
            "purpose": "queue 2716 parent protection or finite ZR row",
            "valid_for_claim": "false",
            "claim_allowed": "false",
            "timestamp_utc": stamp(),
        },
    ]


def formalization_recent_change_count() -> int:
    if not FORMALIZATION_WORKBENCH.exists():
        return 0
    count = 0
    threshold = START_UTC.timestamp() - 1.0
    for path in FORMALIZATION_WORKBENCH.rglob("*"):
        try:
            if path.is_file() and path.stat().st_mtime >= threshold:
                count += 1
        except OSError:
            continue
    return count


def validation_rows(rows_by_name: dict[str, list[dict[str, Any]]], generated_paths: dict[str, Path]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []

    def add(validation_id: str, passed: bool, details: str) -> None:
        rows.append(
            {
                "validation_id": validation_id,
                "passed": as_bool(passed),
                "details": details,
                "timestamp_utc": stamp(),
            }
        )

    sources = rows_by_name["source_register"]
    add("VAL2715_0_sources_exist", all(row["exists"] == "true" and row["missing_needles"] == "" for row in sources), f"sources_checked={len(sources)}")
    add(
        "VAL2715_1_ansatz_registered_nonclaim",
        any(row["gate_id"] == "MWA2715_0_ansatz" and row["current_status"] == "BEST_CONDITIONAL_ANSATZ_NOT_ADOPTED" for row in rows_by_name["minimal_ansatz_gate"]),
        "minimal weak-field ansatz exists but is not adopted",
    )
    add(
        "VAL2715_2_auxiliary_unsigned",
        any(row["audit_id"] == "AUX2715_4_joint_contract" and row["current_status"] == "CONTRACT_WRITTEN_NOT_SIGNED" for row in rows_by_name["auxiliary_compatibility_audit"]),
        "joint auxiliary protection contract remains unsigned",
    )
    add(
        "VAL2715_3_zero_premises_blocked",
        all(row["valid_for_claim"] == "false" and row["claim_allowed"] == "false" for row in rows_by_name["zero_premise_status"]),
        "qR/beta/Newton/local GR premises remain nonclaim",
    )
    add(
        "VAL2715_4_fallback_active",
        any(row["fallback_id"] == "FRF2715_0_ZR" and "MISSING" in row["current_status"] for row in rows_by_name["finite_residual_fallback"]),
        "finite ZR fallback is active but not source-ready",
    )
    add(
        "VAL2715_5_claims_blocked",
        all(row["valid_for_claim"] == "false" and row["claim_allowed"] == "false" for row in rows_by_name["claim_gates"]),
        "all claim gates remain blocked",
    )
    add(
        "VAL2715_6_next_target_selected",
        any(row["next_id"] == "NEXT2715_0_selected" and "2716" in row["target_doc"] for row in rows_by_name["next_target"]),
        "2716 parent protection or finite ZR row selected",
    )
    add("VAL2715_7_branch_copies_declared", len(rows_by_name["branch_copies"]) == len(BRANCH_OUTPUTS), f"branch_copy_rows={len(rows_by_name['branch_copies'])}")

    parse_ok = True
    parse_details = []
    for path in generated_paths.values():
        if path.suffix.lower() != ".csv" or path == OUTPUTS["validation"]:
            continue
        ok, row_count, detail = parse_csv(path)
        parse_ok = parse_ok and ok
        parse_details.append(f"{path.name}:{row_count}:{detail}")
    add("VAL2715_8_csv_parse", parse_ok, "; ".join(parse_details))

    add("VAL2715_9_no_formalization_outputs", not any("formalization-workbench" in str(path).lower() for path in generated_paths.values()), "no output path points into formalization-workbench")
    recent_formalization = formalization_recent_change_count()
    add("VAL2715_10_no_formalization_recent_changes", recent_formalization == 0, f"formalization_recent_changed_count={recent_formalization}")
    add("VAL2715_11_no_github_outputs", not any(".git" in str(path).lower() or "github" in str(path).lower() for path in generated_paths.values()), "no GitHub/public-output path was written")
    add(
        "VAL2715_12_nonclaim_policy",
        all(
            row.get("valid_for_claim") == "false" and row.get("claim_allowed", "false") == "false"
            for table in rows_by_name.values()
            for row in table
            if "valid_for_claim" in row
        ),
        "generated tables keep valid_for_claim=false and claim_allowed=false",
    )

    overall = all(row["passed"] == "true" for row in rows)
    add(
        "VAL2715_OVERALL",
        overall,
        "2715 formalizes the AX1090-aware minimal weak-field auxiliary action gate, keeps q_R/beta/local-GR nonclaim, retains finite ZR/qR fallback, and selects 2716 parent protection or finite row work",
    )
    return rows


def write_doc(rows_by_name: dict[str, list[dict[str, Any]]]) -> None:
    sections = [
        "# 2715 Y5 R2FR minimal weak-field auxiliary action gate under AX1090 closure",
        "",
        f"**Branch:** `{BRANCH_ID}`",
        "",
        "## Private Verdict",
        "",
        "2715 writes the weak-field gate cleanly. The minimal repair ansatz `S_EH + S_matter + int sqrt(-g) lambda_R R_AB + S_silent + S_boundary` is the best conditional route currently on the table: it would give `R_AB=0`, hence `q_R=0`, and the EH weak-field core would give `beta=1` if the source/readout chain were owned.",
        "",
        "But it is not a derivation yet. Under the current AX1090 closure label, `lambda_R` still lacks parent origin and zero-stress proof; `R_AB` is not parent-signed as an auxiliary/vertical compatibility coordinate; no-derivative grammar is unsigned; source/Pi_M/boundary charge ownership is open; and finite `Z_R/q_R` fallback rows are not source-ready. So local GR/Newton/PPN remains a bounded closure-control lane, not a claimed MTS theorem.",
        "",
        "## Source Register",
        markdown_table(rows_by_name["source_register"]),
        "",
        "## Minimal Weak-Field Ansatz Gate",
        markdown_table(rows_by_name["minimal_ansatz_gate"]),
        "",
        "## Auxiliary Compatibility Audit",
        markdown_table(rows_by_name["auxiliary_compatibility_audit"]),
        "",
        "## qR and Beta Zero Premise Status",
        markdown_table(rows_by_name["zero_premise_status"]),
        "",
        "## Finite ZR/qR Fallback",
        markdown_table(rows_by_name["finite_residual_fallback"]),
        "",
        "## Claim Gates",
        markdown_table(rows_by_name["claim_gates"]),
        "",
        "## Current Blocker Stack",
        markdown_table(rows_by_name["blocker_stack"]),
        "",
        "## Decision Ledger",
        markdown_table(rows_by_name["decision_ledger"]),
        "",
        "## Next Target",
        markdown_table(rows_by_name["next_target"]),
        "",
        "## Project Status Snapshot",
        markdown_table(rows_by_name["project_status"]),
        "",
        "## Branch Copies",
        markdown_table(rows_by_name["branch_copies"]),
        "",
        "## Validation",
        markdown_table(rows_by_name["validation"]),
        "",
        "## Plain-English Read",
        "",
        "- This is the right shape of a GR/Newton bridge, but not yet a proof.",
        "- The current bottleneck is not algebra; it is parent ownership of the auxiliary constraint and source/readout chain.",
        "- If the protection contract closes, `q_R` hair can die cleanly; if not, finite `Z_R/q_R` rows must carry the local tests.",
        "- The next move is 2716: parent-sign one protection clause or fill one strict finite fallback row.",
    ]
    DOC_PATH.write_text("\n".join(sections) + "\n", encoding="utf-8")


def main() -> None:
    rows_by_name: dict[str, list[dict[str, Any]]] = {
        "source_register": source_register_rows(),
        "minimal_ansatz_gate": minimal_ansatz_gate_rows(),
        "auxiliary_compatibility_audit": auxiliary_compatibility_audit_rows(),
        "zero_premise_status": zero_premise_status_rows(),
        "finite_residual_fallback": finite_residual_fallback_rows(),
        "claim_gates": claim_gate_rows(),
        "blocker_stack": blocker_stack_rows(),
        "decision_ledger": decision_ledger_rows(),
        "next_target": next_target_rows(),
        "project_status": project_status_rows(),
        "branch_copies": branch_copy_rows(),
    }

    generated_paths = dict(OUTPUTS)
    generated_paths.update(BRANCH_OUTPUTS)
    generated_paths["doc"] = DOC_PATH

    for key, path in OUTPUTS.items():
        if key == "validation":
            continue
        write_csv(path, rows_by_name[key])

    write_csv(BRANCH_OUTPUTS["local_bounds_gate"], rows_by_name["zero_premise_status"])
    write_csv(BRANCH_OUTPUTS["source_weight_gate"], rows_by_name["finite_residual_fallback"])
    write_csv(BRANCH_OUTPUTS["rab_next"], rows_by_name["next_target"])

    rows_by_name["validation"] = validation_rows(rows_by_name, generated_paths)
    write_csv(OUTPUTS["validation"], rows_by_name["validation"])
    write_doc(rows_by_name)

    overall = next(row for row in rows_by_name["validation"] if row["validation_id"] == "VAL2715_OVERALL")
    print(f"2715 complete: {overall['passed']} - {overall['details']}")
    print(DOC_PATH)


if __name__ == "__main__":
    main()

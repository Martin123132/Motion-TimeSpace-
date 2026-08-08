from __future__ import annotations

import csv
import shutil
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
PROJECT_ROOT = ROOT.parent
FORMALIZATION = PROJECT_ROOT / "formalization-workbench"
OUT = ROOT / "source-intake" / "mts_residuals"
QUEUE = ROOT / "source-intake" / "rab-sector" / "acquisition-queue"
MICROSCOPE = ROOT / "source-intake" / "microscope" / "branch_locked_wep" / "residuals"
BETA_DOCS = ROOT / "source-intake" / "beta-source" / "docs"

BRANCH_ID = "MTS_R2FR_RAB_LAMBDAR_ORIGIN_OR_BACKREACTION_ELIMINATION_2267"
DOC = ROOT / "2267-Y5-R2FR-RAB-lambdaR-origin-or-backreaction-elimination.md"


SOURCES: list[dict[str, Any]] = [
    {
        "source_id": "SRC2267_00_2266_doc",
        "source_key": "2266_doc",
        "source_path": ROOT / "2266-Y5-R2FR-RAB-parent-ThetaR-construction-or-qR-prior-width-source.md",
        "needles": ["TD2266_1_algebraic_multiplier_block", "LBC2266_5_verdict", "NEXT2266_0_primary"],
        "role": "handoff: algebraic block Theta_R=0 but lambda_R origin/backreaction open",
    },
    {
        "source_id": "SRC2267_01_2266_validation",
        "source_key": "2266_validation",
        "source_path": OUT / "P8_Y5_BRR545_2266_VALIDATION.csv",
        "needles": ["VAL2266_OVERALL", "PASS"],
        "role": "confirms 2266 passed before 2267 starts",
    },
    {
        "source_id": "SRC2267_02_2266_backreaction",
        "source_key": "2266_backreaction",
        "source_path": OUT / "P8_Y5_PARENT_QLOC_2266_LAMBDAR_BACKREACTION_CONTRACT.csv",
        "needles": ["LBC2266_1_backreaction_zero", "LBC2266_5_verdict"],
        "role": "machine-readable lambda_R backreaction contract",
    },
    {
        "source_id": "SRC2267_03_constraint_07",
        "source_key": "constraint_07",
        "source_path": ROOT / "07-nonpropagating-reciprocity-constraint.md",
        "needles": ["S_constraint = integral lambda_R R_AB", "no R_AB kinetic term", "parent origin is still open"],
        "role": "original nonpropagating multiplier proposal",
    },
    {
        "source_id": "SRC2267_04_observer_10",
        "source_key": "observer_10",
        "source_path": ROOT / "10-observer-map-symplectic-contract.md",
        "needles": ["R_AB = ln(T^2 S)", "J_q = 1", "contract not satisfied"],
        "role": "observer-cell target for reduced-configuration branch",
    },
    {
        "source_id": "SRC2267_05_noether_12",
        "source_key": "noether_12",
        "source_path": ROOT / "12-gauge-noether-origin-audit.md",
        "needles": ["Noether identity", "first-class parent constraint", "closure-only"],
        "role": "warning that symmetry identities alone do not impose R_AB=0",
    },
    {
        "source_id": "SRC2267_06_micro_action",
        "source_key": "micro_action",
        "source_path": PROJECT_ROOT / "core-mts-framework" / "action-principle" / "the-fundamental-action-of-motion-timespace-field-theory.md",
        "needles": ["A_MTS[ψ]", "g_{μν} = η_{μν}", "∂²_t ψ"],
        "role": "primitive psi action candidate for a pre-variation quotient origin",
    },
]


OUTPUTS = {
    "source_register": OUT / "P8_Y5_PARENT_QLOC_2267_SOURCE_REGISTER.csv",
    "backreaction_derivation": OUT / "P8_Y5_PARENT_QLOC_2267_MULTIPLIER_BACKREACTION_DERIVATION.csv",
    "route_matrix": OUT / "P8_Y5_PARENT_QLOC_2267_LAMBDAR_ROUTE_MATRIX.csv",
    "origin_contract": OUT / "P8_Y5_PARENT_QLOC_2267_LAMBDAR_ORIGIN_CONTRACT.csv",
    "reduced_config": OUT / "P8_Y5_PARENT_QLOC_2267_REDUCED_CONFIGURATION_SEED.csv",
    "refusal": OUT / "P8_Y5_PARENT_QLOC_2267_REFUSAL_RUNNER.csv",
    "claim_gates": OUT / "P8_Y5_PARENT_QLOC_2267_CLAIM_GATES.csv",
    "decision": OUT / "P8_Y5_PARENT_QLOC_2267_DECISION_LEDGER.csv",
    "next_target": OUT / "P8_Y5_PARENT_QLOC_2267_NEXT_TARGET.csv",
    "branch_copies": OUT / "P8_Y5_PARENT_QLOC_2267_BRANCH_COPIES.csv",
    "validation": OUT / "P8_Y5_BRR545_2267_VALIDATION.csv",
}


COPY_TARGETS = {
    "queue_origin": QUEUE / "JR2267_LAMBDAR_ORIGIN_CONTRACT_NONCLAIM.csv",
    "queue_reduced": QUEUE / "JR2267_REDUCED_CONFIGURATION_SEED_NONCLAIM.csv",
    "branch_wep": MICROSCOPE / "RAB_lambdaR_backreaction_and_reduced_config_refusal_2267.csv",
    "beta_docs": BETA_DOCS / "RAB_LAMBDAR_ORIGIN_OR_BACKREACTION_2267_NONCLAIM.csv",
}


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        raise ValueError(f"no rows for {path}")
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def parse_csv(path: Path) -> bool:
    read_csv(path)
    return True


def rel(path: Path) -> str:
    try:
        return str(path.relative_to(ROOT)).replace("\\", "/")
    except ValueError:
        try:
            return str(path.relative_to(PROJECT_ROOT)).replace("\\", "/")
        except ValueError:
            return str(path)


def validation_pass(path: Path) -> bool:
    if not path.exists():
        return False
    rows = read_csv(path)
    if not rows:
        return False
    id_key = next((key for key in ("check_id", "validation_id", "id") if key in rows[0]), "")
    result_key = next((key for key in ("result", "status") if key in rows[0]), "")
    if not result_key:
        return False
    overall = [row for row in rows if id_key and "overall" in row.get(id_key, "").lower()]
    return all(row.get(result_key, "").lower() == "pass" for row in (overall or rows))


def source_path(key: str) -> Path:
    return next(source["source_path"] for source in SOURCES if source["source_key"] == key)


def source_refs(*keys: str) -> str:
    return ";".join(rel(source_path(key)) for key in keys)


def source_register_rows() -> list[dict[str, Any]]:
    rows = []
    for source in SOURCES:
        path = source["source_path"]
        exists = path.exists()
        text = read_text(path) if exists else ""
        rows.append(
            {
                "branch_id": BRANCH_ID,
                "source_id": source["source_id"],
                "source_key": source["source_key"],
                "source_path": rel(path),
                "exists": exists,
                "needles": ";".join(source["needles"]),
                "needles_present": exists and all(needle in text for needle in source["needles"]),
                "validation_overall_pass": validation_pass(path) if "validation" in source["source_key"] else "",
                "role": source["role"],
                "valid_for_claim": False,
            }
        )
    return rows


def backreaction_derivation_rows() -> list[dict[str, Any]]:
    return [
        {
            "derivation_id": "LBD2267_0_generic_action",
            "statement": "Take S[Y,lambda_R]=S0[Y]+int mu lambda_R C_R[Y] with C_R=R_AB=ln(T^2S).",
            "result": "delta_lambda S gives C_R[Y]=0; delta_Y S gives E0_A + lambda_R D_A C_R plus measure terms proportional to C_R.",
            "status": "GENERIC_MULTIPLIER_EQUATIONS_WRITTEN",
            "implication": "the multiplier enforces the constraint but generically modifies the Y equations",
            "valid_for_claim": False,
        },
        {
            "derivation_id": "LBD2267_1_on_constraint_surface",
            "statement": "On C_R=0, the measure term drops but lambda_R D_A C_R remains.",
            "result": "The reduced equations equal the original local GR/Newton equations only if lambda_R D_A C_R=0 in physical directions.",
            "status": "GENERIC_MULTIPLIER_BACKREACTION_PRESENT",
            "implication": "a post-variation multiplier is not automatically harmless",
            "valid_for_claim": False,
        },
        {
            "derivation_id": "LBD2267_2_harmless_conditions",
            "statement": "Backreaction is harmless only under one of three gates.",
            "result": "Gate A: lambda_R=0 on shell; Gate B: D_A C_R is pure gauge/constraint-combination; Gate C: C_R=0 is imposed before variation by reduced configuration/quotient variables.",
            "status": "BACKREACTION_ESCAPE_GATES_DEFINED",
            "implication": "2267 must choose a real gate rather than relying on the multiplier alone",
            "valid_for_claim": False,
        },
        {
            "derivation_id": "LBD2267_3_current_corpus_test",
            "statement": "Search current handoff sources for Gate A/B/C completion.",
            "result": "No source proves lambda_R=0, pure-gauge D C_R, or a parent reduced-configuration quotient from psi/phase-volume primitives.",
            "status": "NO_BACKREACTION_GATE_CLOSED_CURRENT_CORPUS",
            "implication": "dynamic lambda_R route remains closure-only unless 2268 closes reduced configuration",
            "valid_for_claim": False,
        },
    ]


def route_matrix_rows() -> list[dict[str, Any]]:
    return [
        {
            "route_id": "LRR2267_0_reduced_configuration",
            "route": "pre-variation reduced configuration / quotient",
            "mechanism": "parameterize local reciprocal geometry with C_R=R_AB=0 before variation, e.g. A=T^2=e^{2Phi}, B=S=e^{-2Phi}, so no lambda_R backreaction exists",
            "needed_evidence": "derive the reduced configuration from psi/phase-volume/quotient primitives, not from GR solution knowledge",
            "rank": 1,
            "current_status": "BEST_ROUTE_NOT_DERIVED",
            "valid_for_claim": False,
        },
        {
            "route_id": "LRR2267_1_first_class_constraint",
            "route": "first-class momentum-map constraint",
            "mechanism": "lambda_R is a gauge multiplier for C_R; physical variables are quotient directions and D C_R is vertical",
            "needed_evidence": "Omega_R, generator v_R, bracket closure, boundary charge zero, matter descent",
            "rank": 2,
            "current_status": "VIABLE_BUT_OMEGA_GENERATOR_MISSING",
            "valid_for_claim": False,
        },
        {
            "route_id": "LRR2267_2_lambda_zero_on_shell",
            "route": "dynamic multiplier with lambda_R=0",
            "mechanism": "field equations plus boundary conditions force lambda_R=0 after imposing R_AB=0",
            "needed_evidence": "explicit base action weak-field equations showing independent combination fixes lambda_R=0",
            "rank": 3,
            "current_status": "POSSIBLE_BUT_EQUATIONS_MISSING",
            "valid_for_claim": False,
        },
        {
            "route_id": "LRR2267_3_stiff_finite_mode",
            "route": "finite stiffness residual",
            "mechanism": "replace hard multiplier by stiff parent operator, e.g. M_R^2 R_AB^2/2, giving finite q_R controlled by source/stiffness",
            "needed_evidence": "parent stiffness M_R, source normalization, q_R projection",
            "rank": 4,
            "current_status": "TESTABLE_FALLBACK_NOT_LOCAL_GR_DERIVATION",
            "valid_for_claim": False,
        },
        {
            "route_id": "LRR2267_4_posthoc_multiplier",
            "route": "post-hoc lambda_R added to metric variables",
            "mechanism": "insert lambda_R R_AB after choosing local metric variables",
            "needed_evidence": "rejected unless one of the backreaction gates closes",
            "rank": 5,
            "current_status": "REJECT_AS_STANDALONE_DERIVATION",
            "valid_for_claim": False,
        },
    ]


def origin_contract_rows() -> list[dict[str, Any]]:
    return [
        {
            "contract_id": "LOC2267_0_phase_volume_origin",
            "required_input": "derive J_q=1 as a pre-variation phase-volume/measure constraint",
            "test": "show the primitive MTS cell map has unit reciprocal Jacobian on the local vacuum branch before invoking Schwarzschild/GR",
            "status": "MISSING_PHASE_VOLUME_PROOF",
            "valid_for_claim": False,
        },
        {
            "contract_id": "LOC2267_1_psi_quotient_origin",
            "required_input": "derive R_AB as a quotient-vertical or nonphysical readout direction from psi covariance",
            "test": "construct q:psi-data -> reduced geometry and prove R_AB lies in ker(Dq) or is absent from reduced variables",
            "status": "MISSING_PSI_TO_QUOTIENT_MAP",
            "valid_for_claim": False,
        },
        {
            "contract_id": "LOC2267_2_lambda_zero",
            "required_input": "prove lambda_R=0 on shell if dynamic multiplier is retained",
            "test": "compute weak-field E_T/E_S combinations and show boundary/vacuum equations force lambda_R=0",
            "status": "MISSING_WEAK_FIELD_MULTIPLIER_EQUATIONS",
            "valid_for_claim": False,
        },
        {
            "contract_id": "LOC2267_3_matter_compatibility",
            "required_input": "prove matter/readout does not source C_R after reduction",
            "test": "show S_matter depends only on reduced variables or source leg is zero to PPN/WEP/clock order",
            "status": "MISSING_MATTER_DESCENT",
            "valid_for_claim": False,
        },
        {
            "contract_id": "LOC2267_4_verdict",
            "required_input": "claim-grade lambda_R origin/backreaction gate",
            "test": "LOC2267_0 through LOC2267_3, or a first-class equivalent, pass jointly",
            "status": "LAMBDAR_ORIGIN_NOT_DERIVED_CURRENT_CORPUS",
            "valid_for_claim": False,
        },
    ]


def reduced_config_rows() -> list[dict[str, Any]]:
    return [
        {
            "seed_id": "RCS2267_0_local_parametrization",
            "object": "local reciprocal reduced variables",
            "formula": "A=T^2=e^{2Phi(r)}, B=S=e^{-2Phi(r)} so R_AB=ln(AB)=0 identically",
            "use": "candidate pre-variation configuration seed for 2268",
            "risk": "must be derived from MTS primitives; otherwise it is just GR closure",
            "status": "SEED_READY_NOT_CLAIM",
            "valid_for_claim": False,
        },
        {
            "seed_id": "RCS2267_1_weak_field_link",
            "object": "Newtonian limit seed",
            "formula": "if A=1-L+O(L^2), then B=A^{-1}=1+L+O(L^2) and gamma=1 at first PPN order",
            "use": "shows why the reduced branch would hit local GR at leading order if derived",
            "risk": "beta and conservation still require second-order parent expansion",
            "status": "CONDITIONAL_LIMIT_ONLY",
            "valid_for_claim": False,
        },
        {
            "seed_id": "RCS2267_2_finite_fallback",
            "object": "finite residual fallback",
            "formula": "R_AB=q_R L+O(L^2) if reduced configuration fails",
            "use": "keeps empirical branch ready for PPN/R10/clock/orbital gates",
            "risk": "q_R still needs parent source or prior width",
            "status": "NONCLAIM_FALLBACK",
            "valid_for_claim": False,
        },
    ]


def refusal_rows() -> list[dict[str, Any]]:
    return [
        {
            "refusal_id": "REF2267_0_multiplier_derivation",
            "attempted_claim": "post-hoc lambda_R multiplier derives local GR",
            "runner_result": "REJECTED_AS_STANDALONE",
            "blocked_by": "generic lambda_R D_A C_R backreaction remains",
            "score_eligible": False,
            "valid_for_claim": False,
        },
        {
            "refusal_id": "REF2267_1_reduced_config_claim",
            "attempted_claim": "reduced configuration is derived",
            "runner_result": "BLOCKED",
            "blocked_by": "phase-volume/psi quotient origin missing",
            "score_eligible": False,
            "valid_for_claim": False,
        },
        {
            "refusal_id": "REF2267_2_local_GR",
            "attempted_claim": "derived local GR/Newton/PPN",
            "runner_result": "BLOCKED",
            "blocked_by": "LOC2267_4_verdict=LAMBDAR_ORIGIN_NOT_DERIVED_CURRENT_CORPUS",
            "score_eligible": False,
            "valid_for_claim": False,
        },
        {
            "refusal_id": "REF2267_3_qR_score",
            "attempted_claim": "finite q_R branch can be scored",
            "runner_result": "BLOCKED",
            "blocked_by": "finite q_R parent source/prior width absent",
            "score_eligible": False,
            "valid_for_claim": False,
        },
    ]


def claim_gate_rows() -> list[dict[str, Any]]:
    return [
        {
            "claim_id": "CG2267_0_backreaction_eliminated",
            "claim": "lambda_R backreaction eliminated",
            "gate_pass": False,
            "reason": "no lambda_R=0, pure-gauge DC_R, or reduced-configuration origin proof",
            "valid_for_claim": False,
        },
        {
            "claim_id": "CG2267_1_reduced_configuration",
            "claim": "pre-variation reduced configuration derived",
            "gate_pass": False,
            "reason": "seed written but not derived from MTS primitives",
            "valid_for_claim": False,
        },
        {
            "claim_id": "CG2267_2_local_GR",
            "claim": "derived local GR/Newton branch",
            "gate_pass": False,
            "reason": "not yet achieved",
            "valid_for_claim": False,
        },
        {
            "claim_id": "CG2267_3_finite_residual",
            "claim": "finite q_R residual has source-backed value",
            "gate_pass": False,
            "reason": "parent source/prior width missing",
            "valid_for_claim": False,
        },
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        {
            "decision_id": "DEC2267_0_multiplier_backreaction",
            "decision": "POSTHOC_MULTIPLIER_REJECTED_AS_STANDALONE_DERIVATION",
            "reason": "generic multiplier variation leaves lambda_R D_A R_AB in the physical equations",
            "next_action": "do not use lambda_R alone as the local-GR proof",
            "valid_for_claim": False,
        },
        {
            "decision_id": "DEC2267_1_best_route",
            "decision": "REDUCED_CONFIGURATION_OR_QUOTIENT_IS_BEST_ROUTE",
            "reason": "pre-variation variables avoid multiplier backreaction and can make R_AB=0 kinematic if derived from MTS primitives",
            "next_action": "try to derive A=e^{2Phi}, B=e^{-2Phi} / J_q=1 from phase-volume or psi quotient",
            "valid_for_claim": False,
        },
        {
            "decision_id": "DEC2267_2_fallback",
            "decision": "FINITE_STIFFNESS_BRANCH_REMAINS_FALLBACK",
            "reason": "if reduced configuration fails, q_R must be sourced from a parent stiffness/operator and tested",
            "next_action": "do not borrow local bounds as values",
            "valid_for_claim": False,
        },
        {
            "decision_id": "DEC2267_3_next",
            "decision": "REDUCED_CONFIGURATION_DERIVATION_NEXT",
            "reason": "this is now the cleanest path to local GR without multiplier backreaction",
            "next_action": "2268-Y5-R2FR-RAB-reduced-configuration-parametrization-or-finite-stiffness-row.md",
            "valid_for_claim": False,
        },
    ]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        {
            "route_id": "NEXT2267_0_primary",
            "next_target": "2268-Y5-R2FR-RAB-reduced-configuration-parametrization-or-finite-stiffness-row.md",
            "script": "scripts/Y5_R2FR_RAB_reduced_configuration_parametrization_or_finite_stiffness_row_2268.py",
            "objective": "try to derive the reciprocal reduced configuration A=e^{2Phi}, B=e^{-2Phi} from MTS phase-volume/psi quotient primitives; if it fails, open the finite stiffness q_R row",
            "selection_status": "selected",
            "success_condition": "R_AB=0 becomes pre-variation/kinematic from MTS primitives, or the branch is demoted and a finite stiffness residual row is sourced nonclaim",
        }
    ]


def branch_copy_rows() -> list[dict[str, Any]]:
    return [
        {
            "copy_id": "BC2267_origin",
            "source_path": rel(OUTPUTS["origin_contract"]),
            "target_path": rel(COPY_TARGETS["queue_origin"]),
            "target_exists": COPY_TARGETS["queue_origin"].exists(),
            "target_parses": parse_csv(COPY_TARGETS["queue_origin"]),
            "reason": "lambda_R origin/backreaction contract copied as nonclaim queue",
        },
        {
            "copy_id": "BC2267_reduced",
            "source_path": rel(OUTPUTS["reduced_config"]),
            "target_path": rel(COPY_TARGETS["queue_reduced"]),
            "target_exists": COPY_TARGETS["queue_reduced"].exists(),
            "target_parses": parse_csv(COPY_TARGETS["queue_reduced"]),
            "reason": "reduced-configuration seed copied as nonclaim queue",
        },
        {
            "copy_id": "BC2267_branch_wep",
            "source_path": rel(OUTPUTS["claim_gates"]),
            "target_path": rel(COPY_TARGETS["branch_wep"]),
            "target_exists": COPY_TARGETS["branch_wep"].exists(),
            "target_parses": parse_csv(COPY_TARGETS["branch_wep"]),
            "reason": "branch-locked WEP/local refusal gates",
        },
        {
            "copy_id": "BC2267_beta_docs",
            "source_path": rel(OUTPUTS["decision"]),
            "target_path": rel(COPY_TARGETS["beta_docs"]),
            "target_exists": COPY_TARGETS["beta_docs"].exists(),
            "target_parses": parse_csv(COPY_TARGETS["beta_docs"]),
            "reason": "portable lambda_R/reduced-configuration decision ledger",
        },
    ]


def table(headers: list[str], rows: list[dict[str, Any]]) -> str:
    lines = [
        "| " + " | ".join(headers) + " |",
        "| " + " | ".join("---" for _ in headers) + " |",
    ]
    for row in rows:
        lines.append("| " + " | ".join(str(row.get(header, "")).replace("\n", " ") for header in headers) + " |")
    return "\n".join(lines)


def validation_rows() -> list[dict[str, Any]]:
    source_rows = read_csv(OUTPUTS["source_register"])
    backreaction = read_csv(OUTPUTS["backreaction_derivation"])
    routes = read_csv(OUTPUTS["route_matrix"])
    origin = read_csv(OUTPUTS["origin_contract"])
    reduced = read_csv(OUTPUTS["reduced_config"])
    refusal = read_csv(OUTPUTS["refusal"])
    claims = read_csv(OUTPUTS["claim_gates"])
    next_rows = read_csv(OUTPUTS["next_target"])
    generated_csvs = [path for key, path in OUTPUTS.items() if key != "validation"]
    checks = [
        ("VAL2267_0_sources_exist", all(row["exists"].lower() == "true" for row in source_rows), "all cited source paths exist"),
        ("VAL2267_1_needles_present", all(row["needles_present"].lower() == "true" for row in source_rows), "all cited source needles are present"),
        (
            "VAL2267_2_prior_validation",
            any(row["source_key"] == "2266_validation" and row["validation_overall_pass"].lower() == "true" for row in source_rows),
            "2266 validation passes",
        ),
        (
            "VAL2267_3_generic_backreaction_written",
            any(row["derivation_id"] == "LBD2267_1_on_constraint_surface" and row["status"] == "GENERIC_MULTIPLIER_BACKREACTION_PRESENT" for row in backreaction),
            "generic multiplier backreaction is derived",
        ),
        (
            "VAL2267_4_escape_gates_defined",
            any(row["derivation_id"] == "LBD2267_2_harmless_conditions" and row["status"] == "BACKREACTION_ESCAPE_GATES_DEFINED" for row in backreaction),
            "lambda_R harmlessness gates are defined",
        ),
        (
            "VAL2267_5_route_selection",
            any(row["route_id"] == "LRR2267_0_reduced_configuration" and row["current_status"] == "BEST_ROUTE_NOT_DERIVED" for row in routes)
            and any(row["route_id"] == "LRR2267_4_posthoc_multiplier" and row["current_status"] == "REJECT_AS_STANDALONE_DERIVATION" for row in routes),
            "reduced configuration selected and posthoc multiplier rejected",
        ),
        (
            "VAL2267_6_origin_contract_unsigned",
            any(row["contract_id"] == "LOC2267_4_verdict" and row["status"] == "LAMBDAR_ORIGIN_NOT_DERIVED_CURRENT_CORPUS" for row in origin)
            and all(row["valid_for_claim"].lower() == "false" for row in origin),
            "lambda_R origin contract remains unsigned",
        ),
        (
            "VAL2267_7_reduced_seed_nonclaim",
            len(reduced) >= 3 and all(row["valid_for_claim"].lower() == "false" for row in reduced),
            "reduced-configuration seed written as nonclaim",
        ),
        (
            "VAL2267_8_refusal_blocks",
            all(row["score_eligible"].lower() == "false" and row["valid_for_claim"].lower() == "false" for row in refusal),
            "refusal runner blocks local claims",
        ),
        (
            "VAL2267_9_claim_gates_blocked",
            all(row["gate_pass"].lower() == "false" and row["valid_for_claim"].lower() == "false" for row in claims),
            "claim gates are all blocked",
        ),
        (
            "VAL2267_10_next_selected",
            any(row["route_id"] == "NEXT2267_0_primary" and row["selection_status"] == "selected" for row in next_rows),
            "2268 target selected",
        ),
        ("VAL2267_11_csv_parse", all(parse_csv(path) for path in generated_csvs), "all generated 2267 CSVs parse"),
        (
            "VAL2267_12_no_claim_flags",
            not any(
                row.get(key, "").lower() == "true"
                for path in generated_csvs
                for row in read_csv(path)
                for key in ("score_ready", "accepted_ready", "valid_for_claim", "claim_allowed", "gate_pass")
            ),
            "no generated score/claim/gate flags are true",
        ),
        (
            "VAL2267_13_branch_copies",
            all(row["target_exists"].lower() == "true" and row["target_parses"].lower() == "true" for row in read_csv(OUTPUTS["branch_copies"])),
            "branch/queue copies exist and parse",
        ),
        ("VAL2267_14_pycache_absent", not (ROOT / "scripts" / "__pycache__").exists(), "scripts __pycache__ absent"),
        (
            "VAL2267_15_formalization_no_2267",
            not any(
                path.is_file()
                and (path.name.startswith("2267-") or (path.name.startswith("P8_Y5") and "2267" in path.name))
                for path in FORMALIZATION.rglob("*")
            ),
            "formalization-workbench has no 2267 output files",
        ),
    ]
    rows = [
        {
            "branch_id": BRANCH_ID,
            "check_id": check_id,
            "result": "PASS" if passed else "FAIL",
            "detail": detail,
        }
        for check_id, passed, detail in checks
    ]
    rows.append(
        {
            "branch_id": BRANCH_ID,
            "check_id": "VAL2267_OVERALL",
            "result": "PASS" if all(row["result"] == "PASS" for row in rows) else "FAIL",
            "detail": "2267 derives the generic lambda_R backreaction obstruction, rejects posthoc multipliers as standalone derivations, and selects reduced configuration for 2268",
        }
    )
    return rows


def write_doc() -> None:
    source_rows = read_csv(OUTPUTS["source_register"])
    backreaction = read_csv(OUTPUTS["backreaction_derivation"])
    routes = read_csv(OUTPUTS["route_matrix"])
    origin = read_csv(OUTPUTS["origin_contract"])
    reduced = read_csv(OUTPUTS["reduced_config"])
    refusal = read_csv(OUTPUTS["refusal"])
    claims = read_csv(OUTPUTS["claim_gates"])
    decisions = read_csv(OUTPUTS["decision"])
    next_rows = read_csv(OUTPUTS["next_target"])
    copies = read_csv(OUTPUTS["branch_copies"])
    validation = read_csv(OUTPUTS["validation"])
    sections = [
        "# 2267 - Y5/R2FR R_AB lambda_R Origin Or Backreaction Elimination",
        "",
        "## Verdict",
        "",
        "2267 is a necessary honesty gate. A pure algebraic `lambda_R R_AB` block can enforce `R_AB=0`, but if it is added as a post-hoc multiplier on physical metric/readout variables, its variation generically leaves a `lambda_R D_A R_AB` term in the field equations. That is backreaction. It means the multiplier route does not derive local GR by itself.",
        "",
        "The cleanest route is therefore not a dynamic multiplier inserted after the fact. It is a pre-variation reduced configuration or quotient: build the local reciprocal branch with `R_AB=0` already absent/kinematic, then vary only the reduced variables. A seed parametrization is `A=T^2=e^{2Phi(r)}`, `B=S=e^{-2Phi(r)}`, giving `AB=1` identically. But that seed is not a claim until it is derived from MTS phase-volume or psi-quotient primitives.",
        "",
        "So this is progress with teeth: the unsafe route is demoted, the best route is identified, and the next target is the reduced-configuration derivation. No local-GR/Newton, PPN, R10, WEP, clock, orbital, `R_AB=0`, `Q_R=0`, or finite residual pass claim is made.",
        "",
        "## Source Register",
        table(["source_id", "source_key", "source_path", "exists", "needles_present", "validation_overall_pass", "role"], source_rows),
        "",
        "## Multiplier Backreaction Derivation",
        table(["derivation_id", "statement", "result", "status", "implication", "valid_for_claim"], backreaction),
        "",
        "## lambda_R Route Matrix",
        table(["route_id", "route", "mechanism", "needed_evidence", "rank", "current_status", "valid_for_claim"], routes),
        "",
        "## lambda_R Origin Contract",
        table(["contract_id", "required_input", "test", "status", "valid_for_claim"], origin),
        "",
        "## Reduced Configuration Seed",
        table(["seed_id", "object", "formula", "use", "risk", "status", "valid_for_claim"], reduced),
        "",
        "## Refusal Runner",
        table(["refusal_id", "attempted_claim", "runner_result", "blocked_by", "score_eligible", "valid_for_claim"], refusal),
        "",
        "## Claim Gates",
        table(["claim_id", "claim", "gate_pass", "reason", "valid_for_claim"], claims),
        "",
        "## Decision Ledger",
        table(["decision_id", "decision", "reason", "next_action", "valid_for_claim"], decisions),
        "",
        "## Next Target",
        table(["route_id", "next_target", "script", "objective", "selection_status", "success_condition"], next_rows),
        "",
        "## Branch Copies",
        table(["copy_id", "source_path", "target_path", "target_exists", "target_parses", "reason"], copies),
        "",
        "## Validation",
        table(["check_id", "result", "detail"], validation),
        "",
        "## Working Interpretation",
        "",
        "This is the sharpest state of the local-GR problem so far. We should stop trying to make a post-hoc multiplier carry the whole theory. The Mayweather route is reduced configuration: derive the reciprocal local geometry before variation, so there is no multiplier backreaction to defend. If we cannot derive that from MTS primitives, we pivot cleanly to finite stiffness and test `q_R` as a residual.",
    ]
    DOC.write_text("\n".join(sections), encoding="utf-8")


def main() -> None:
    for directory in (OUT, QUEUE, MICROSCOPE, BETA_DOCS):
        directory.mkdir(parents=True, exist_ok=True)

    write_csv(OUTPUTS["source_register"], source_register_rows())
    write_csv(OUTPUTS["backreaction_derivation"], backreaction_derivation_rows())
    write_csv(OUTPUTS["route_matrix"], route_matrix_rows())
    write_csv(OUTPUTS["origin_contract"], origin_contract_rows())
    write_csv(OUTPUTS["reduced_config"], reduced_config_rows())
    write_csv(OUTPUTS["refusal"], refusal_rows())
    write_csv(OUTPUTS["claim_gates"], claim_gate_rows())
    write_csv(OUTPUTS["decision"], decision_rows())
    write_csv(OUTPUTS["next_target"], next_target_rows())

    shutil.copyfile(OUTPUTS["origin_contract"], COPY_TARGETS["queue_origin"])
    shutil.copyfile(OUTPUTS["reduced_config"], COPY_TARGETS["queue_reduced"])
    shutil.copyfile(OUTPUTS["claim_gates"], COPY_TARGETS["branch_wep"])
    shutil.copyfile(OUTPUTS["decision"], COPY_TARGETS["beta_docs"])
    write_csv(OUTPUTS["branch_copies"], branch_copy_rows())

    pycache = ROOT / "scripts" / "__pycache__"
    if pycache.exists():
        shutil.rmtree(pycache)

    write_csv(OUTPUTS["validation"], validation_rows())
    write_doc()

    print(f"wrote {DOC}")
    print(f"wrote {OUTPUTS['validation']}")


if __name__ == "__main__":
    main()

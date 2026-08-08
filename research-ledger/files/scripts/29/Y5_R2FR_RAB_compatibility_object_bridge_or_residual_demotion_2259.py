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

BRANCH_ID = "MTS_R2FR_PARENT_QLOC_RAB_COMPATIBILITY_BRIDGE_2259"
DOC = ROOT / "2259-Y5-R2FR-RAB-compatibility-object-bridge-or-residual-demotion.md"


SOURCES: list[dict[str, Any]] = [
    {
        "source_id": "SRC2259_00_2258_doc",
        "source_key": "2258_doc",
        "source_path": ROOT / "2258-Y5-R2FR-RAB-ZR-MR2-sign-gap-and-zero-mode-certificate.md",
        "needles": ["DEC2258_2_best_route", "NEXT2258_0_primary", "SIGN_GAP_CERTIFICATE_NOT_CLOSED"],
        "role": "current handoff: sign/gap failed and compatibility-object bridge selected",
    },
    {
        "source_id": "SRC2259_01_2258_validation",
        "source_key": "2258_validation",
        "source_path": OUT / "P8_Y5_BRR545_2258_VALIDATION.csv",
        "needles": ["VAL2258_OVERALL", "PASS"],
        "role": "confirms 2258 passed before 2259 starts",
    },
    {
        "source_id": "SRC2259_02_2171_doc",
        "source_key": "2171_doc",
        "source_path": ROOT / "2171-Y5-R2FR-compatibility-object-category-principle-or-finite-local-source-row.md",
        "needles": ["CAT2171_6_verdict", "VG2171_6_result", "NEXT2171_0_2172"],
        "role": "prior compatibility-object audit: type-only rejected, Noether/generator route selected",
    },
    {
        "source_id": "SRC2259_03_2171_validation",
        "source_key": "2171_validation",
        "source_path": OUT / "P8_Y5_BRR545_2171_VALIDATION.csv",
        "needles": ["VAL2171_OVERALL", "PASS"],
        "role": "confirms 2171 passed",
    },
    {
        "source_id": "SRC2259_04_2172_doc",
        "source_key": "2172_doc",
        "source_path": ROOT / "2172-Y5-R2FR-radial-cell-vertical-gauge-noether-identity-or-coefficient-basis.md",
        "needles": ["NO_NONTRIVIAL_VERTICAL_GENERATOR_CURRENT_READOUT", "DEC2172_3_next", "VAL2172_OVERALL"],
        "role": "prior no-go: current readout has no nontrivial C_R vertical gauge generator",
    },
    {
        "source_id": "SRC2259_05_2172_validation",
        "source_key": "2172_validation",
        "source_path": OUT / "P8_Y5_BRR545_2172_VALIDATION.csv",
        "needles": ["VAL2172_OVERALL", "PASS"],
        "role": "confirms 2172 passed",
    },
    {
        "source_id": "SRC2259_06_2236_doc",
        "source_key": "2236_doc",
        "source_path": ROOT / "2236-Y5-R2FR-RAB-auxiliary-compatibility-parent-sort-and-no-derivative-grammar.md",
        "needles": ["SORT2236_0_auxiliary_coordinate", "GRAM2236_5_verdict", "ELIM2236_4_current"],
        "role": "prior auxiliary compatibility grammar: exact conditional, parent sort/grammar unsigned",
    },
    {
        "source_id": "SRC2259_07_2237_doc",
        "source_key": "2237_doc",
        "source_path": ROOT / "2237-Y5-R2FR-RAB-vertical-null-presymplectic-degeneracy-or-finite-ZR-intake.md",
        "needles": ["NULL2237_5_verdict", "KIN2237_1_null_contradiction", "VAL2237_OVERALL"],
        "role": "prior presymplectic-null theorem shape: exact conditional, parent proof missing",
    },
    {
        "source_id": "SRC2259_08_2237_validation",
        "source_key": "2237_validation",
        "source_path": OUT / "P8_Y5_BRR545_2237_VALIDATION.csv",
        "needles": ["VAL2237_OVERALL", "PASS"],
        "role": "confirms 2237 passed",
    },
    {
        "source_id": "SRC2259_09_2238_doc",
        "source_key": "2238_doc",
        "source_path": ROOT / "2238-Y5-R2FR-RAB-parent-theta-Omega-vR-fill-or-finite-ZR-source-row.md",
        "needles": ["TO2238_0_theta_R", "VR2238_4_verdict", "DEC2238_2_best_route"],
        "role": "prior theta/Omega/v_R fill: first-class v_R rejected, second-class elimination retained",
    },
    {
        "source_id": "SRC2259_10_2238_validation",
        "source_key": "2238_validation",
        "source_path": OUT / "P8_Y5_BRR545_2238_VALIDATION.csv",
        "needles": ["VAL2238_OVERALL", "PASS"],
        "role": "confirms 2238 passed",
    },
    {
        "source_id": "SRC2259_11_2258_demotion",
        "source_key": "2258_demotion",
        "source_path": OUT / "P8_Y5_PARENT_QLOC_2258_RESIDUAL_DEMOTION_QUEUE.csv",
        "needles": ["RD2258_0_ZR", "RD2258_4_projection"],
        "role": "current finite residual demotion queue",
    },
]


OUTPUTS = {
    "source_register": OUT / "P8_Y5_PARENT_QLOC_2259_SOURCE_REGISTER.csv",
    "bridge_audit": OUT / "P8_Y5_PARENT_QLOC_2259_COMPATIBILITY_BRIDGE_AUDIT.csv",
    "route_matrix": OUT / "P8_Y5_PARENT_QLOC_2259_ROUTE_MATRIX.csv",
    "second_class_contract": OUT / "P8_Y5_PARENT_QLOC_2259_SECOND_CLASS_AUXILIARY_CONTRACT.csv",
    "demotion_queue": OUT / "P8_Y5_PARENT_QLOC_2259_RESIDUAL_DEMOTION_QUEUE.csv",
    "refusal": OUT / "P8_Y5_PARENT_QLOC_2259_REFUSAL_RUNNER.csv",
    "claim_gates": OUT / "P8_Y5_PARENT_QLOC_2259_CLAIM_GATES.csv",
    "decision": OUT / "P8_Y5_PARENT_QLOC_2259_DECISION_LEDGER.csv",
    "next_target": OUT / "P8_Y5_PARENT_QLOC_2259_NEXT_TARGET.csv",
    "branch_copies": OUT / "P8_Y5_PARENT_QLOC_2259_BRANCH_COPIES.csv",
    "validation": OUT / "P8_Y5_BRR545_2259_VALIDATION.csv",
}


COPY_TARGETS = {
    "queue_bridge": QUEUE / "JR2259_RAB_COMPATIBILITY_BRIDGE_NONCLAIM.csv",
    "queue_demotion": QUEUE / "JR2259_RAB_RESIDUAL_DEMOTION_QUEUE_NONCLAIM.csv",
    "branch_wep": MICROSCOPE / "RAB_compatibility_bridge_nonclaim_2259.csv",
    "beta_docs": BETA_DOCS / "RAB_COMPATIBILITY_BRIDGE_2259_NONCLAIM.csv",
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
        return str(path)


def validation_pass(path: Path) -> bool:
    if not path.exists():
        return False
    rows = read_csv(path)
    if not rows:
        return False
    id_keys = ["check_id", "validation_id", "validation_id", "id"]
    result_keys = ["result", "status"]
    id_key = next((key for key in id_keys if key in rows[0]), "")
    result_key = next((key for key in result_keys if key in rows[0]), "")
    if not result_key:
        return False
    if id_key:
        overall = [row for row in rows if "overall" in row.get(id_key, "").lower()]
    else:
        overall = []
    return all(row.get(result_key, "").lower() == "pass" for row in (overall or rows))


def false_flags() -> dict[str, bool]:
    return {
        "theorem_zero": False,
        "parent_signed": False,
        "source_backed": False,
        "score_ready": False,
        "valid_for_claim": False,
        "claim_allowed": False,
    }


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
                "claim_allowed": False,
            }
        )
    return rows


def src(*keys: str) -> str:
    by_key = {source["source_key"]: source["source_path"] for source in SOURCES}
    return ";".join(rel(by_key[key]) for key in keys)


def bridge_audit_rows() -> list[dict[str, Any]]:
    entries = [
        (
            "BR2259_0_type_only",
            "compatibility label/type-only route",
            "declare R_AB/C_R compatibility data rather than physical field",
            "REJECTED",
            "2171 countermodels show coframe derivative, potential, source prefactor, shadow-frame, and boundary-charge slots remain legal.",
            src("2171_doc"),
        ),
        (
            "BR2259_1_current_vertical_gauge",
            "current-readout vertical gauge route",
            "find v_R with delta C_R != 0 and delta e_obs = 0",
            "REJECTED_FOR_CURRENT_READOUT",
            "2172 proves current T,sqrt(S) coframe has no nontrivial C_R vertical generator and derives a leak lower bound.",
            src("2172_doc"),
        ),
        (
            "BR2259_2_presymplectic_null",
            "presymplectic-null vertical fibre route",
            "prove R_AB direction lies in ker(Omega_parent)=ker(Dq) with no boundary charge",
            "EXACT_CONDITIONAL_NOT_PARENT_SIGNED",
            "2237 gives the contradiction with nonzero Z_R if true nullness is proved, but theta/Omega/v_R/no-vertical-metric inputs remain missing.",
            src("2237_doc"),
        ),
        (
            "BR2259_3_first_class_vR",
            "first-class pure R_AB shift route",
            "use pure delta R_AB=eta, delta q=0 as a gauge orbit",
            "REJECTED_OFFSHELL_TANGENCY",
            "2238 shows pure R_AB shifts fail compatibility-surface tangency; compatibility-preserving shifts are not q-vertical.",
            src("2238_doc"),
        ),
        (
            "BR2259_4_second_class_auxiliary",
            "second-class auxiliary compatibility block",
            "parent-owned Lambda_R(R_AB-C_AB[q,theta,top]) block with no derivative grammar and source/boundary/readout protection",
            "BEST_REMAINING_DERIVATION_ROUTE_CONDITIONAL",
            "2238 fills theta_R=Omega_R=Pi_R^n=0 inside an algebraic auxiliary block, but parent ownership and protections are unsigned.",
            src("2236_doc", "2238_doc"),
        ),
        (
            "BR2259_5_residual_demotion",
            "finite residual branch",
            "retain Z_R, M_R^2, J_R, Q_R, b_R/d_R/w_R, boundary, and projection rows if protections fail",
            "RETAINED_NONCLAIM_FALLBACK",
            "2258 and 2171 queues already define the finite residual objects; none are source-backed/score-ready.",
            src("2258_demotion", "2171_doc"),
        ),
        (
            "BR2259_6_verdict",
            "compatibility-object bridge",
            "current corpus proves R_AB/C_R is non-dynamical before local readout",
            "BRIDGE_NOT_CLOSED_ROUTE_NARROWED",
            "the bridge rejects label/gauge shortcuts and narrows the live proof route to second-class auxiliary elimination protections.",
            src("2258_doc", "2172_doc", "2238_doc"),
        ),
    ]
    return [
        {
            "branch_id": BRANCH_ID,
            "audit_id": audit_id,
            "route": route,
            "required_statement": required,
            "current_status": status,
            "reason": reason,
            "source_paths": source_paths,
            **false_flags(),
        }
        for audit_id, route, required, status, reason, source_paths in entries
    ]


def route_matrix_rows() -> list[dict[str, Any]]:
    entries = [
        (
            "ROUTE2259_0_label",
            "type/label compatibility",
            "lowest",
            "rejected",
            "too weak: derivative, potential, source and boundary countermodels survive",
        ),
        (
            "ROUTE2259_1_readout_vertical_gauge",
            "first-class hidden gauge under current readout",
            "low",
            "rejected",
            "2172 current coframe kernel obstruction",
        ),
        (
            "ROUTE2259_2_presymplectic_null",
            "parent presymplectic-null fibre",
            "medium",
            "held_conditional",
            "beautiful if parent theta/Omega/v_R/no-boundary data are supplied; not currently signed",
        ),
        (
            "ROUTE2259_3_second_class_auxiliary",
            "parent second-class auxiliary compatibility block",
            "highest",
            "selected_nonclaim",
            "best remaining derivation route after first-class/gauge routes fail",
        ),
        (
            "ROUTE2259_4_readout_rebuild",
            "new Q_vis/E readout functor rebuild",
            "medium",
            "held_parallel",
            "could bypass 2172 only if parent owns a different observed coframe map",
        ),
        (
            "ROUTE2259_5_finite_residual",
            "finite residual coefficient programme",
            "fallback",
            "retained_nonclaim",
            "mandatory if second-class protections fail",
        ),
    ]
    return [
        {
            "branch_id": BRANCH_ID,
            "route_id": route_id,
            "route": route,
            "priority": priority,
            "selection_status": status,
            "reason": reason,
            **false_flags(),
        }
        for route_id, route, priority, status, reason in entries
    ]


def second_class_contract_rows() -> list[dict[str, Any]]:
    entries = [
        (
            "SC2259_0_parent_block",
            "parent-owned auxiliary block",
            "S_Raux = integral mu_parent Lambda_R^{AB}(R_AB-C_AB[q,theta,top])",
            "MISSING_PARENT_OWNERSHIP_OF_BLOCK",
            "without this the block is a closure insertion",
        ),
        (
            "SC2259_1_operator_exclusion",
            "no-derivative/no-vertical-metric grammar",
            "ParentGenerate excludes D R_AB, D Lambda_R, G_vert, nabla_vert, and boundary derivative terms",
            "MISSING_OPERATOR_EXCLUSION_THEOREM",
            "needed for theta_R=Omega_R=Pi_R^n=0 and Z_R=0",
        ),
        (
            "SC2259_2_source_silence",
            "source silence",
            "E_R gives Lambda_R=0 because J_R, source-only prefactors, and matter descent leaks vanish",
            "MISSING_JR_ZERO_AND_MATTER_DESCENT",
            "needed to stop active-source coupling returning through Lambda_R",
        ),
        (
            "SC2259_3_boundary_silence",
            "boundary/corner silence",
            "B_R, Pi_R, Q_R, and admitted corner terms carry no R_AB/C_R charge",
            "MISSING_BOUNDARY_NO_CHARGE_THEOREM",
            "needed to stop exterior reciprocal hair",
        ),
        (
            "SC2259_4_readout_stability",
            "readout stability after elimination",
            "R_AB=C_AB is imposed before local readout and does not regenerate b_R/d_R/endpoints/tau leaks",
            "MISSING_READOUT_STABILITY_DESCENT",
            "needed for PPN/clock/orbital silence",
        ),
        (
            "SC2259_5_total",
            "second-class auxiliary local-GR route",
            "all four protections close together before any local GR/Newton claim",
            "SECOND_CLASS_ROUTE_NOT_ACTIVATED",
            "best route, not a claim",
        ),
    ]
    return [
        {
            "branch_id": BRANCH_ID,
            "contract_id": contract_id,
            "clause": clause,
            "required_statement": required,
            "current_status": status,
            "failure_effect": effect,
            "source_paths": src("2236_doc", "2238_doc", "2172_doc"),
            **false_flags(),
        }
        for contract_id, clause, required, status, effect in entries
    ]


def demotion_queue_rows() -> list[dict[str, Any]]:
    entries = [
        ("DM2259_0_ZR", "Z_R/Z_RR/Z_RY", "operator exclusion fails -> source finite kinetic/cross rows", "MISSING_SOURCE_BACKED_OPERATOR_INPUTS", "R10;PPN;clock;orbital"),
        ("DM2259_1_MR2", "M_R^2/lambda_R", "auxiliary mass/range branch survives -> source mass-gap/range rows", "MISSING_SOURCE_BACKED_MASS_RANGE", "R10;clock;orbital"),
        ("DM2259_2_JR_wR", "J_R/w_R/beta_source", "matter/source descent fails -> source finite source-coupling rows", "MISSING_SOURCE_COUPLING_ROWS", "WEP;PPN;R10;local_GR"),
        ("DM2259_3_QR_boundary", "Q_R/Phi_boundary/B_R", "boundary silence fails -> source boundary/exterior hair rows", "MISSING_BOUNDARY_CHARGE_ROWS", "PPN;orbital;light_time"),
        ("DM2259_4_readout", "b_R/d_R/endpoint_tau", "readout stability fails -> source coframe/disformal/endpoint projection rows", "MISSING_READOUT_PROJECTION_ROWS", "PPN;clock;orbital"),
        ("DM2259_5_projection", "q_loc/local residual envelope", "any finite row survives -> map into arenas with no-cancellation envelope", "MISSING_ARENA_PROJECTION_KERNELS", "all_local_arenas"),
    ]
    return [
        {
            "branch_id": BRANCH_ID,
            "queue_id": queue_id,
            "object": object_name,
            "demotion_trigger": trigger,
            "current_status": status,
            "observable_link": arena,
            "source_paths": src("2258_demotion", "2171_doc", "2172_doc"),
            **false_flags(),
        }
        for queue_id, object_name, trigger, status, arena in entries
    ]


def refusal_rows() -> list[dict[str, Any]]:
    entries = [
        ("REF2259_0_bridge", "compatibility-object bridge closes", "BLOCKED", "BR2259_6_verdict=BRIDGE_NOT_CLOSED_ROUTE_NARROWED"),
        ("REF2259_1_label", "type-only compatibility proves non-dynamical R_AB/C_R", "BLOCKED", "2171 countermodels survive"),
        ("REF2259_2_first_class", "first-class/current-readout vertical gauge removes C_R", "BLOCKED", "2172 verticality obstruction and 2238 tangency failure"),
        ("REF2259_3_second_class", "second-class auxiliary elimination gives local GR", "BLOCKED", "parent block plus source/boundary/readout/operator protections unsigned"),
        ("REF2259_4_local_tests", "R10/PPN/clock/orbital scores are allowed", "BLOCKED", "finite residual rows are not source-backed and projection kernels missing"),
    ]
    return [
        {
            "branch_id": BRANCH_ID,
            "refusal_id": refusal_id,
            "attempted_claim": claim,
            "runner_result": result,
            "blocked_by": blocked_by,
            "score_eligible": False,
            **false_flags(),
        }
        for refusal_id, claim, result, blocked_by in entries
    ]


def claim_gate_rows() -> list[dict[str, Any]]:
    entries = [
        ("CG2259_0_bridge", "R_AB/C_R non-dynamical compatibility object", "bridge route is narrowed but not closed"),
        ("CG2259_1_second_class", "second-class auxiliary block parent-owned", "block, sort and C_AB map not parent-signed"),
        ("CG2259_2_operator", "Z_R=0/operator exclusion", "no-derivative/no-vertical-metric grammar not parent-derived"),
        ("CG2259_3_source_boundary", "J_R=0 and Q_R/B_R=0", "matter and boundary descent still unsigned"),
        ("CG2259_4_readout", "readout stability and projection silence", "b_R/d_R/endpoint/tau projection not closed"),
        ("CG2259_5_local_GR_Newton", "derived local GR/Newton recovery", "all upstream gates remain nonclaim"),
    ]
    return [
        {
            "branch_id": BRANCH_ID,
            "claim_id": claim_id,
            "claim": claim,
            "gate_pass": False,
            "reason": reason,
            **false_flags(),
        }
        for claim_id, claim, reason in entries
    ]


def decision_rows() -> list[dict[str, Any]]:
    entries = [
        (
            "DEC2259_0_status",
            "COMPATIBILITY_BRIDGE_NOT_CLOSED",
            "2259 rejects label-only and current-readout first-class gauge shortcuts, and imports the presymplectic-null no-claim result.",
            "keep branch private/nonclaim",
        ),
        (
            "DEC2259_1_best_route",
            "SECOND_CLASS_AUXILIARY_ROUTE_SELECTED_NONCLAIM",
            "the remaining clean derivation route is not gauge magic; it is parent-owned algebraic elimination with four protection clauses.",
            "attack source/boundary/readout/operator protections",
        ),
        (
            "DEC2259_2_claim_ceiling",
            "NO_LOCAL_GR_OR_ARENA_CLAIM",
            "no theorem-zero route or source-backed residual envelope is complete.",
            "refuse local-GR/Newton/R10/PPN/clock/orbital claims",
        ),
        (
            "DEC2259_3_fallback",
            "FINITE_RESIDUAL_DEMOTION_READY",
            "if any protection fails, the corresponding finite row must be sourced rather than assumed away.",
            "carry residual queue",
        ),
        (
            "DEC2259_4_next",
            "SOURCE_BOUNDARY_READOUT_OPERATOR_PROTECTION_NEXT",
            "these are the decisive clauses for second-class elimination and exactly match the route isolated by 2238.",
            "2260-Y5-R2FR-RAB-source-boundary-readout-operator-protection-or-residual-validator.md",
        ),
    ]
    return [
        {
            "branch_id": BRANCH_ID,
            "decision_id": decision_id,
            "decision": decision,
            "reason": reason,
            "next_action": next_action,
            **false_flags(),
        }
        for decision_id, decision, reason, next_action in entries
    ]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "route_id": "NEXT2259_0_primary",
            "next_target": "2260-Y5-R2FR-RAB-source-boundary-readout-operator-protection-or-residual-validator.md",
            "script": "scripts/Y5_R2FR_RAB_source_boundary_readout_operator_protection_or_residual_validator_2260.py",
            "objective": "prove or reject the four protections needed for second-class auxiliary elimination: source silence, boundary silence, readout stability, and operator exclusion; if they fail, validate finite residual rows without scoring placeholders",
            "selection_status": "selected",
            "success_condition": "all four protections become parent-signed before local-GR claim, or the branch is explicitly demoted to finite residual rows with no claim",
            "forbidden_claims": "type-only compatibility; current-readout vertical gauge; first-class v_R; local-GR/Newton/R10/PPN pass; placeholder residual scoring",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "route_id": "NEXT2259_1_parallel",
            "next_target": "2260b-Y5-R2FR-RAB-first-source-backed-residual-row-acquisition.md",
            "script": "scripts/Y5_R2FR_RAB_first_source_backed_residual_row_acquisition_2260b.py",
            "objective": "if protection proof stalls, acquire one real source-backed finite row from the demotion queue",
            "selection_status": "held_parallel",
            "success_condition": "one residual component has source path, units, normalization, and arena projection while still nonclaim",
            "forbidden_claims": "external bound as MTS prediction; symbolic row scoring; cancellation between residual channels",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]


def copy_branch_rows() -> list[dict[str, Any]]:
    copies = [
        ("bridge", OUTPUTS["bridge_audit"], COPY_TARGETS["queue_bridge"], "compatibility bridge route audit"),
        ("demotion", OUTPUTS["demotion_queue"], COPY_TARGETS["queue_demotion"], "finite residual demotion queue after bridge audit"),
        ("branch_wep", OUTPUTS["claim_gates"], COPY_TARGETS["branch_wep"], "branch-locked local/WEP refusal gates"),
        ("beta_docs", OUTPUTS["decision"], COPY_TARGETS["beta_docs"], "portable compatibility bridge decision ledger"),
    ]
    rows = []
    for copy_id, source_path, target_path, reason in copies:
        target_path.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(source_path, target_path)
        rows.append(
            {
                "branch_id": BRANCH_ID,
                "copy_id": f"BC2259_{copy_id}",
                "source_path": rel(source_path),
                "target_path": rel(target_path),
                "target_exists": target_path.exists(),
                "target_parses": parse_csv(target_path),
                "reason": reason,
                "valid_for_claim": False,
                "claim_allowed": False,
            }
        )
    return rows


def markdown_table(rows: list[dict[str, Any]], columns: list[str]) -> str:
    lines = ["| " + " | ".join(columns) + " |", "| " + " | ".join("---" for _ in columns) + " |"]
    for row in rows:
        values = [str(row.get(column, "")).replace("\n", " ").replace("|", "\\|") for column in columns]
        lines.append("| " + " | ".join(values) + " |")
    return "\n".join(lines)


def validation_rows(paths: list[Path]) -> list[dict[str, Any]]:
    source_rows = read_csv(OUTPUTS["source_register"])
    bridge = read_csv(OUTPUTS["bridge_audit"])
    routes = read_csv(OUTPUTS["route_matrix"])
    second_class = read_csv(OUTPUTS["second_class_contract"])
    demotion = read_csv(OUTPUTS["demotion_queue"])
    refusals = read_csv(OUTPUTS["refusal"])
    claims = read_csv(OUTPUTS["claim_gates"])
    decisions = read_csv(OUTPUTS["decision"])
    next_targets = read_csv(OUTPUTS["next_target"])
    copies = read_csv(OUTPUTS["branch_copies"])

    def check(check_id: str, passed: bool, detail: str) -> dict[str, Any]:
        return {"branch_id": BRANCH_ID, "check_id": check_id, "result": "PASS" if passed else "FAIL", "detail": detail}

    csv_parse_ok = True
    for path in paths:
        try:
            parse_csv(path)
        except Exception:
            csv_parse_ok = False

    formalization_2259 = []
    if FORMALIZATION.exists():
        formalization_2259 = [path for path in FORMALIZATION.rglob("*2259*") if path.is_file()]

    bridge_routes = {row["route"] for row in bridge}
    route_statuses = {row["route_id"]: row["selection_status"] for row in routes}
    contract_clauses = {row["clause"] for row in second_class}
    all_rows = [row for path in paths for row in read_csv(path)]

    rows = [
        check("VAL2259_0_sources_exist", all(row["exists"] == "True" for row in source_rows), "all cited source paths exist"),
        check("VAL2259_1_needles_present", all(row["needles_present"] == "True" for row in source_rows), "all cited source needles are present"),
        check("VAL2259_2_prior_validations", all(row["validation_overall_pass"] in ("", "True") for row in source_rows), "2258, 2171, 2172, 2237, and 2238 validations pass where checked"),
        check("VAL2259_3_bridge_coverage", {"compatibility label/type-only route", "current-readout vertical gauge route", "presymplectic-null vertical fibre route", "first-class pure R_AB shift route", "second-class auxiliary compatibility block", "finite residual branch"}.issubset(bridge_routes), "bridge audit covers rejected, conditional, selected, and fallback routes"),
        check("VAL2259_4_route_selection", route_statuses.get("ROUTE2259_3_second_class_auxiliary") == "selected_nonclaim" and route_statuses.get("ROUTE2259_5_finite_residual") == "retained_nonclaim", "second-class auxiliary route selected nonclaim with finite fallback retained"),
        check("VAL2259_5_second_class_contract", {"parent-owned auxiliary block", "no-derivative/no-vertical-metric grammar", "source silence", "boundary/corner silence", "readout stability after elimination", "second-class auxiliary local-GR route"}.issubset(contract_clauses), "second-class contract covers parent block, operator, source, boundary, readout and verdict clauses"),
        check("VAL2259_6_second_class_not_activated", any(row["contract_id"] == "SC2259_5_total" and row["current_status"] == "SECOND_CLASS_ROUTE_NOT_ACTIVATED" for row in second_class), "second-class route remains unactivated"),
        check("VAL2259_7_demotion_queue_retained", len(demotion) == 6 and all(row["valid_for_claim"] == "False" for row in demotion), "finite residual demotion queue retained as nonclaim"),
        check("VAL2259_8_runner_refuses", all(row["runner_result"] == "BLOCKED" for row in refusals), "refusal runner blocks all current claims"),
        check("VAL2259_9_claim_gates_blocked", all(row["gate_pass"] == "False" for row in claims), "claim gates are blocked"),
        check("VAL2259_10_decision_next", any(row["decision_id"] == "DEC2259_4_next" and row["decision"] == "SOURCE_BOUNDARY_READOUT_OPERATOR_PROTECTION_NEXT" for row in decisions), "decision selects protection proof next"),
        check("VAL2259_11_next_selected", any(row["route_id"] == "NEXT2259_0_primary" and row["selection_status"] == "selected" for row in next_targets), "next target selected"),
        check("VAL2259_12_csv_parse", csv_parse_ok, "all generated 2259 CSVs parse"),
        check("VAL2259_13_no_claim_flags", all(row.get("valid_for_claim", "False") != "True" and row.get("claim_allowed", "False") != "True" and row.get("theorem_zero", "False") != "True" and row.get("parent_signed", "False") != "True" and row.get("score_ready", "False") != "True" and row.get("source_backed", "False") != "True" for row in all_rows), "no generated theorem/parent/source/score/claim flags are true"),
        check("VAL2259_14_branch_copies", all(row["target_exists"] == "True" and row["target_parses"] == "True" for row in copies), "branch/queue copies exist and parse"),
        check("VAL2259_15_pycache_absent", not (ROOT / "scripts" / "__pycache__").exists(), "scripts __pycache__ absent"),
        check("VAL2259_16_formalization_no_2259", not formalization_2259, "formalization-workbench has no 2259 outputs"),
    ]
    rows.append(
        check(
            "VAL2259_OVERALL",
            all(row["result"] == "PASS" for row in rows),
            "2259 bridges the current R_AB branch to prior compatibility-object evidence, rejects label/gauge shortcuts, selects second-class auxiliary protection next, and retains finite residual demotion",
        )
    )
    return rows


def remove_pycache() -> None:
    pycache = ROOT / "scripts" / "__pycache__"
    if pycache.exists():
        shutil.rmtree(pycache)


def build_doc(
    source_rows: list[dict[str, Any]],
    bridge: list[dict[str, Any]],
    routes: list[dict[str, Any]],
    second_class: list[dict[str, Any]],
    demotion: list[dict[str, Any]],
    refusals: list[dict[str, Any]],
    claims: list[dict[str, Any]],
    decisions: list[dict[str, Any]],
    next_targets: list[dict[str, Any]],
    copies: list[dict[str, Any]],
    validation: list[dict[str, Any]],
) -> str:
    return "\n\n".join(
        [
            "# 2259 - Y5/R2FR R_AB Compatibility-Object Bridge Or Residual Demotion",
            "## Verdict\n\n2259 does not close the compatibility-object proof, but it does stop the branch from circling. The label/type-only route is rejected, the current-readout vertical-gauge route is rejected by the 2172 coframe-kernel obstruction, and the first-class pure `R_AB` shift route is rejected by the 2238 tangency test.\n\nThe remaining clean derivation path is second-class auxiliary elimination: a parent-owned algebraic `Lambda_R(R_AB-C_AB)` block plus source silence, boundary silence, readout stability, and operator exclusion. If those protections fail, the branch must demote to explicit finite residual rows. No local-GR/Newton, R10, PPN, clock, or orbital claim is made.",
            "## Source Register\n" + markdown_table(source_rows, ["source_id", "source_key", "source_path", "exists", "needles_present", "validation_overall_pass", "role"]),
            "## Compatibility Bridge Audit\n" + markdown_table(bridge, ["audit_id", "route", "required_statement", "current_status", "reason", "valid_for_claim"]),
            "## Route Matrix\n" + markdown_table(routes, ["route_id", "route", "priority", "selection_status", "reason", "valid_for_claim"]),
            "## Second-Class Auxiliary Contract\n" + markdown_table(second_class, ["contract_id", "clause", "required_statement", "current_status", "failure_effect", "valid_for_claim"]),
            "## Residual Demotion Queue\n" + markdown_table(demotion, ["queue_id", "object", "demotion_trigger", "current_status", "observable_link", "valid_for_claim"]),
            "## Refusal Runner\n" + markdown_table(refusals, ["refusal_id", "attempted_claim", "runner_result", "blocked_by", "score_eligible", "valid_for_claim"]),
            "## Claim Gates\n" + markdown_table(claims, ["claim_id", "claim", "gate_pass", "reason", "valid_for_claim"]),
            "## Decision Ledger\n" + markdown_table(decisions, ["decision_id", "decision", "reason", "next_action", "valid_for_claim"]),
            "## Next Target\n" + markdown_table(next_targets, ["route_id", "next_target", "script", "objective", "selection_status", "success_condition"]),
            "## Branch Copies\n" + markdown_table(copies, ["copy_id", "source_path", "target_path", "target_exists", "target_parses", "reason"]),
            "## Validation\n" + markdown_table(validation, ["check_id", "result", "detail"]),
            "## Working Interpretation\n\nThis is good narrowing. The project is no longer pretending every route is equally alive. First-class gauge is not the path under the current readout. The live proof target is now engineering-like: can the parent action really own an algebraic compatibility block and protect it from source, boundary, readout, and derivative regeneration? If yes, local GR recovery becomes much more serious. If no, the finite-residual programme is not a failure; it is the honest empirical fallback.",
        ]
    ) + "\n"


def main() -> None:
    remove_pycache()

    source_rows = source_register_rows()
    bridge = bridge_audit_rows()
    routes = route_matrix_rows()
    second_class = second_class_contract_rows()
    demotion = demotion_queue_rows()
    refusals = refusal_rows()
    claims = claim_gate_rows()
    decisions = decision_rows()
    next_targets = next_target_rows()

    write_csv(OUTPUTS["source_register"], source_rows)
    write_csv(OUTPUTS["bridge_audit"], bridge)
    write_csv(OUTPUTS["route_matrix"], routes)
    write_csv(OUTPUTS["second_class_contract"], second_class)
    write_csv(OUTPUTS["demotion_queue"], demotion)
    write_csv(OUTPUTS["refusal"], refusals)
    write_csv(OUTPUTS["claim_gates"], claims)
    write_csv(OUTPUTS["decision"], decisions)
    write_csv(OUTPUTS["next_target"], next_targets)

    copies = copy_branch_rows()
    write_csv(OUTPUTS["branch_copies"], copies)

    generated = [
        OUTPUTS["source_register"],
        OUTPUTS["bridge_audit"],
        OUTPUTS["route_matrix"],
        OUTPUTS["second_class_contract"],
        OUTPUTS["demotion_queue"],
        OUTPUTS["refusal"],
        OUTPUTS["claim_gates"],
        OUTPUTS["decision"],
        OUTPUTS["next_target"],
        OUTPUTS["branch_copies"],
    ]

    validation = validation_rows(generated)
    write_csv(OUTPUTS["validation"], validation)
    remove_pycache()
    validation = validation_rows(generated)
    write_csv(OUTPUTS["validation"], validation)

    DOC.write_text(
        build_doc(source_rows, bridge, routes, second_class, demotion, refusals, claims, decisions, next_targets, copies, validation),
        encoding="utf-8",
    )

    if not all(row["result"] == "PASS" for row in validation):
        raise SystemExit("2259 validation failed")

    print(f"wrote {DOC}")
    print(f"wrote {OUTPUTS['validation']}")


if __name__ == "__main__":
    main()

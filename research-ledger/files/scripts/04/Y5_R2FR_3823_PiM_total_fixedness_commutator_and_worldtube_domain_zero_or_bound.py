from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Iterable


CHECKPOINT = "3823"
BRANCH = "MTS_R2FR_Y5_PIM_TOTAL_FIXEDNESS_COMMUTATOR_AND_WORLDTUBE_DOMAIN_ZERO_OR_BOUND_3823"

PCW = Path(__file__).resolve().parents[1]
ROOT = PCW.parent
FWB = ROOT / "formalization-workbench"
OUT = PCW / "source-intake" / "mts_residuals"
DOC_PATH = PCW / "3823-Y5-R2FR-PiM-total-fixedness-commutator-and-worldtube-domain-zero-or-bound.md"
SPINE_PATH = PCW / "LOCAL_GR_COUPLING_SPINE_CURRENT_STATE.md"

P_3822 = PCW / "3822-Y5-R2FR-independent-source-ledger-and-local-test-ready-source-rows.md"
P_1013 = PCW / "1013-Y5-R10-PiM-JH-flux-closure-or-measured-GM-obstruction-score.md"
P_1014 = PCW / "1014-Y5-R10-PiM-commutator-projector-variation-zero-or-coefficient-bound.md"
P_1016 = PCW / "1016-Y5-R10-parent-worldtube-source-measure-selector-or-R_eq-first-input.md"
P_3777 = PCW / "3777-Y5-R2FR-PiM-total-system-domain-and-EM-field-energy-source-map.md"

CSV_3822_LEDGER = OUT / "P8_Y5_R2FR_3822_LOCAL_ARENA_SOURCE_LEDGER.csv"
CSV_3822_TEST = OUT / "P8_Y5_R2FR_3822_LOCAL_TEST_READY_SOURCE_ROWS.csv"
CSV_1013_FLUX = OUT / "P8_Y5_R10_1013_PIM_JH_FLUX_THEOREM_ATTEMPT.csv"
CSV_1013_OBS = OUT / "P8_Y5_R10_1013_MEASURED_GM_OBSTRUCTION_VECTOR.csv"
CSV_1014_THEOREM = OUT / "P8_Y5_R10_1014_PIM_COMMUTATOR_THEOREM_ATTEMPT.csv"
CSV_1014_BOUNDS = OUT / "P8_Y5_R10_1014_COEFFICIENT_BOUND_ROWS.csv"
CSV_1014_ROUTE = OUT / "P8_Y5_R10_1014_ROUTE_SPLIT.csv"
CSV_1016_CONTRACT = OUT / "P8_Y5_R10_1016_PARENT_SELECTOR_CONTRACT.csv"
CSV_3777_PROJECTOR = OUT / "P8_Y5_R2FR_3777_PIM_TOTAL_PROJECTOR_CONSTRUCTION.csv"
CSV_3777_CLOSURE = OUT / "P8_Y5_R2FR_3777_PIM_TOTAL_CLOSURE_ATTEMPT.csv"

OUTPUTS = {
    "sources": OUT / "P8_Y5_R2FR_3823_SOURCE_REGISTER.csv",
    "fixedness": OUT / "P8_Y5_R2FR_3823_PIM_TOTAL_FIXEDNESS_THEOREM.csv",
    "commutator": OUT / "P8_Y5_R2FR_3823_COMMUTATOR_ZERO_OR_BOUND.csv",
    "domain": OUT / "P8_Y5_R2FR_3823_WORLDTUBE_DOMAIN_STABILITY.csv",
    "arena_map": OUT / "P8_Y5_R2FR_3823_ARENA_PIM_RESIDUAL_MAP.csv",
    "residuals": OUT / "P8_Y5_R2FR_3823_PIM_TOTAL_RESIDUAL_ROWS.csv",
    "gates": OUT / "P8_Y5_R2FR_3823_CLAIM_GATES.csv",
    "decisions": OUT / "P8_Y5_R2FR_3823_DECISION_ROWS.csv",
    "next": OUT / "P8_Y5_R2FR_3823_NEXT_TARGET.csv",
    "status": OUT / "P8_Y5_R2FR_3823_STATUS.csv",
    "validation": OUT / "P8_Y5_BRR545_3823_VALIDATION.csv",
}

SOURCE_SPECS = [
    ("SRC3823_0_3822_doc", P_3822, "Local Arena Source Ledger"),
    ("SRC3823_1_3822_ledger", CSV_3822_LEDGER, "ARENA3822_0_R10_lab"),
    ("SRC3823_2_3822_test", CSV_3822_TEST, "LTR3822_0_R10_alpha_lambda"),
    ("SRC3823_3_1013_doc", P_1013, "compact-exterior closure"),
    ("SRC3823_4_1013_flux", CSV_1013_FLUX, "PFC1013_2_product_rule"),
    ("SRC3823_5_1013_obs", CSV_1013_OBS, "OBS1013_1_PiM_commutator"),
    ("SRC3823_6_1014_doc", P_1014, "[d,Pi_M]J_H=0"),
    ("SRC3823_7_1014_theorem", CSV_1014_THEOREM, "PCT1014_2_commutator_zero"),
    ("SRC3823_8_1014_bounds", CSV_1014_BOUNDS, "PCC1014_1_I_commutator"),
    ("SRC3823_9_1014_route", CSV_1014_ROUTE, "PRS1014_0_topological_metric_independent"),
    ("SRC3823_10_1016_doc", P_1016, "W_source = closure(supp J_H[tau])"),
    ("SRC3823_11_1016_contract", CSV_1016_CONTRACT, "PSC1016_6_PiM_Hamiltonian_map"),
    ("SRC3823_12_3777_doc", P_3777, "Pi_M Total Projector Construction"),
    ("SRC3823_13_3777_projector", CSV_3777_PROJECTOR, "PIM3777_2_projector_definition"),
    ("SRC3823_14_3777_closure", CSV_3777_CLOSURE, "PCA3777_0_projector_defined"),
]


def now_utc() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def read_text(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        return path.read_text(encoding="utf-8-sig", errors="replace")


def base_row(timestamp: str) -> dict[str, str]:
    return {
        "timestamp_utc": timestamp,
        "branch_id": BRANCH,
        "checkpoint_id": CHECKPOINT,
        "valid_for_claim": "false",
        "claim_allowed": "false",
    }


def write_csv(path: Path, rows: Iterable[dict[str, str]]) -> None:
    rows = list(rows)
    path.parent.mkdir(parents=True, exist_ok=True)
    fields: list[str] = []
    for row in rows:
        for key in row:
            if key not in fields:
                fields.append(key)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def parse_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def source_rows(timestamp: str) -> list[dict[str, str]]:
    rows = []
    for source_id, path, needle in SOURCE_SPECS:
        exists = path.exists()
        text = read_text(path) if exists else ""
        rows.append(
            {
                **base_row(timestamp),
                "source_id": source_id,
                "path": str(path),
                "needle": needle,
                "exists": str(exists),
                "needle_found": str(needle in text),
                "source_role": "PiM total fixedness and commutator input",
            }
        )
    return rows


def fixedness_rows(timestamp: str) -> list[dict[str, str]]:
    rows = [
        {
            "theorem_id": "PFX3823_0_projector_type_split",
            "status": "EXACT_BRANCH_SPLIT",
            "statement": "Pi_M_total is safe only as a fixed linear source-charge projection over a fixed worldtube/homology class; Hodge, readout, radius-fit or moving-domain projectors carry variation stress.",
            "zero_condition": "Pi_M_total depends on parent source structure, tau, W_source and [S_link], not on the tested readout residual.",
            "failure_residual": "R_projector_variation",
        },
        {
            "theorem_id": "PFX3823_1_fixed_integral_projector",
            "status": "EXACT_CONDITIONAL_ZERO_ROUTE",
            "statement": "If Pi_M_total is the fixed integral map M_H,total=int_{Sigma cap D_total(W)} n_a J_M,total^a dSigma plus declared fixed tail terms, then dPi_M_total=0 on the exterior annulus.",
            "zero_condition": "fixed D_total(W), fixed tau, fixed homology class, fixed tail rule, no metric/readout-dependent refit",
            "failure_residual": "R_domain_motion + R_projector_stress",
        },
        {
            "theorem_id": "PFX3823_2_parent_owned_selector",
            "status": "CONDITIONAL_OWNER_CONTRACT",
            "statement": "The source worldtube must be selected by support of the total Hilbert/Hamiltonian current before readout: W_source=closure(supp J_M,total[tau]).",
            "zero_condition": "J_M,total and tau are parent-owned and support compactness/regularity holds",
            "failure_residual": "R_worldtube_selector",
        },
        {
            "theorem_id": "PFX3823_3_Hodge_route_demoted",
            "status": "DEMOTE_UNLESS_BOUNDED",
            "statement": "If Pi_M is a Hodge/DeWitt/metric projector, delta_g Pi_M creates an effective projector-stress source and cannot be silently used for local GR.",
            "zero_condition": "use fixed topological/integral projector instead, or source a projector-stress bound",
            "failure_residual": "R_projector_stress",
        },
        {
            "theorem_id": "PFX3823_4_verdict",
            "status": "MECHANISM_CONSTRUCTED_NOT_PARENT_SIGNED",
            "statement": "The clean path is fixed integral Pi_M_total over a total-system domain. It kills the commutator conditionally, but current MTS still needs parent ownership of tau, W_source, tails and Hilbert equality.",
            "zero_condition": "all 3823 zero conditions plus R_eq equality are signed",
            "failure_residual": "R_PiM_total",
        },
    ]
    return [{**base_row(timestamp), **row} for row in rows]


def commutator_rows(timestamp: str) -> list[dict[str, str]]:
    rows = [
        {
            "commutator_id": "COM3823_0_product_rule",
            "status": "EXACT_IDENTITY",
            "formula": "d(Pi_M J_H)=Pi_M dJ_H + [d,Pi_M]J_H",
            "interpretation": "Flux closure fails through current nonconservation or projector/domain variation.",
            "bound_if_unsigned": "I_commutator",
        },
        {
            "commutator_id": "COM3823_1_fixed_projector_zero",
            "status": "EXACT_CONDITIONAL_ZERO",
            "formula": "[d,Pi_M_total]J_H=0 if dPi_M_total=0 on the annulus",
            "interpretation": "A fixed linear integral/source-charge projector commutes with exterior d/Stokes transport.",
            "bound_if_unsigned": "R_projector_variation",
        },
        {
            "commutator_id": "COM3823_2_moving_boundary_term",
            "status": "FINITE_RESIDUAL_FORM",
            "formula": "[d,Pi_M]J_H -> integral_{partial D moving} i_v J_H + delta_tail_rule",
            "interpretation": "If the domain or tail cutoff moves with readout, the commutator becomes a boundary-flux residual.",
            "bound_if_unsigned": "R_domain_motion",
        },
        {
            "commutator_id": "COM3823_3_metric_projector_term",
            "status": "FINITE_RESIDUAL_FORM",
            "formula": "delta_g Pi_H(g) maps to projector_stress_beta_equiv and source-kernel tails",
            "interpretation": "Metric-dependent projection is allowed only as a bounded extra source/readout term.",
            "bound_if_unsigned": "R_projector_stress",
        },
        {
            "commutator_id": "COM3823_4_closure_needed",
            "status": "NOT_A_FULL_FLUX_CLAIM",
            "formula": "d(Pi_M J_H)=0 also needs Pi_M dJ_H=0 and R_eq equality",
            "interpretation": "3823 kills or bounds the commutator channel; it does not yet prove topological equality or total flux closure.",
            "bound_if_unsigned": "R_eq + R_flux_leak",
        },
    ]
    return [{**base_row(timestamp), **row} for row in rows]


def domain_rows(timestamp: str) -> list[dict[str, str]]:
    rows = [
        {
            "domain_id": "DOM3823_0_pre_readout_worldtube",
            "status": "EXACT_CONDITIONAL_SELECTOR",
            "condition": "W_source=closure(supp J_M,total[tau]) is fixed before any orbital/R10/PPN fit",
            "result": "source support cannot chase the measured residual",
            "residual_if_missing": "R_worldtube_selector",
        },
        {
            "domain_id": "DOM3823_1_homology_surface_lock",
            "status": "EXACT_CONDITIONAL_STOKES_LOCK",
            "condition": "S1 and S2 link the same W_source and are homologous in the source-free exterior",
            "result": "surface charge does not depend on which linked exterior surface is used",
            "residual_if_missing": "R_linking_homology",
        },
        {
            "domain_id": "DOM3823_2_total_system_tail_rule",
            "status": "EXACT_TOTAL_DOMAIN_REQUIREMENT",
            "condition": "D_total includes matter, EM, Poynting, binding, apparatus, theta/source support or declares tail bounds",
            "result": "matter-only cuts cannot create fake mu_extra or fake source-normalization errors",
            "residual_if_missing": "R_open_domain",
        },
        {
            "domain_id": "DOM3823_3_flux_silence_or_bound",
            "status": "ZERO_OR_BOUND_CONDITION",
            "condition": "int_annulus d(Pi_M_total J_M,total)=0 or finite epsilon_flux is retained",
            "result": "compact-exterior charge closure is either real or explicitly bounded",
            "residual_if_missing": "R_flux_leak",
        },
        {
            "domain_id": "DOM3823_4_arena_transfer",
            "status": "ARENA_KERNEL_CONDITION",
            "condition": "same Pi_M_total/source-domain rule is reused across R10, WEP, PPN, clocks, orbital and EM rows",
            "result": "no per-arena source projector tuning",
            "residual_if_missing": "R_arena_projector_tuning",
        },
    ]
    return [{**base_row(timestamp), **row} for row in rows]


def arena_map_rows(timestamp: str) -> list[dict[str, str]]:
    rows = []
    arenas = [
        ("R10_short_range_lab", "R_PiM_commutator + R_domain_motion + R_open_domain", "mass/geometry source pack needs fixed source kernel"),
        ("WEP_MICROSCOPE_lab", "R_PiM_commutator + R_worldtube_selector + R_arena_projector_tuning", "material/source projection kernel must be fixed before eta scoring"),
        ("PPN_gamma_beta", "R_projector_stress + R_mu_split + R_PiM_commutator", "metric-dependent projector would contaminate gamma/beta"),
        ("clock_redshift_Gdot", "R_worldtube_selector + R_covariant_frame + R_clock_tau", "tau/source selector must not be clock-fitted"),
        ("orbital_GM_Gauss", "R_mu_split + R_domain_motion + R_linking_homology", "mu_fit stays product-only until source-domain lock"),
        ("EM_Poynting_source_stress", "R_open_domain + R_flux_leak + R_projector_stress", "field support/tail flux must be included or bounded"),
    ]
    for index, (arena, residual_vector, meaning) in enumerate(arenas):
        rows.append(
            {
                **base_row(timestamp),
                "map_id": f"APM3823_{index}",
                "arena": arena,
                "PiM_status": "conditional_zero_or_bound",
                "residual_vector": residual_vector,
                "meaning": meaning,
                "claim_policy": "no local claim until residual vector is theorem-zero or source-backed bounded",
            }
        )
    return rows


def residual_rows(timestamp: str) -> list[dict[str, str]]:
    specs = [
        ("R3823_0_projector_variation", "R_projector_variation", "failure of dPi_M_total=0 for the chosen source projector", "||dPi_M_total|| weighted by J_H"),
        ("R3823_1_domain_motion", "R_domain_motion", "moving source-domain/tail cutoff contribution", "abs(integral_moving_boundary i_v J_H)/M_ref"),
        ("R3823_2_projector_stress", "R_projector_stress", "metric/Hodge projector variation stress equivalent", "projector_stress_beta_equiv or operator norm"),
        ("R3823_3_worldtube_selector", "R_worldtube_selector", "source support not fixed by parent Hilbert current before readout", "Boolean selector failure or support-shift norm"),
        ("R3823_4_linking_homology", "R_linking_homology", "linked exterior surfaces not homologous around one fixed source", "abs(Q[S2]-Q[S1])/M_ref"),
        ("R3823_5_arena_tuning", "R_arena_projector_tuning", "different source projector used per arena", "max arena-to-arena projector mismatch"),
        ("R3823_6_total", "R_PiM_total", "total PiM fixedness/domain/commutator residual", "sum_abs(R_projector_variation,R_domain_motion,R_projector_stress,R_worldtube_selector,R_linking_homology,R_arena_projector_tuning)"),
    ]
    return [
        {
            **base_row(timestamp),
            "residual_id": residual_id,
            "symbol": symbol,
            "definition": definition,
            "bound_formula": formula,
            "units": "dimensionless_or_source_flux_after_normalization",
            "current_status": "ZERO_IF_FIXED_INTEGRAL_PROJECTOR_ELSE_BOUND_REQUIRED",
            "exit_requirement": "theorem-zero from parent fixed PiM_total or source-backed arena bound",
        }
        for residual_id, symbol, definition, formula in specs
    ]


def gate_rows(timestamp: str, grouped: dict[str, list[dict[str, str]]]) -> list[dict[str, str]]:
    sources_pass = all(row["exists"] == "True" and row["needle_found"] == "True" for row in grouped["sources"])
    rows = [
        ("GATE3823_0_sources", "PASS_NONCLAIM" if sources_pass else "FAIL", "all source paths and needles present" if sources_pass else "missing source path or needle"),
        ("GATE3823_1_fixed_projector_route", "PASS_CONDITIONAL_ZERO", "fixed integral PiM_total gives commutator zero conditionally"),
        ("GATE3823_2_moving_projector_bound", "PASS_BOUND_SCHEMA", "moving/Hodge/readout projectors converted to residual bounds"),
        ("GATE3823_3_worldtube_domain", "PASS_NONCLAIM", "pre-readout worldtube/domain lock conditions emitted"),
        ("GATE3823_4_arena_transfer", "PASS_NONCLAIM", "same PiM residual vector mapped to local arenas"),
        ("GATE3823_5_R_eq_flux_closure", "BLOCKED_NEXT_PROOF", "topological Hilbert equality and boundary primitive still open"),
        ("GATE3823_6_Newton_local_GR_claim", "BLOCKED", "local GR/Newton still waits on R_eq/flux closure, source ledger and PPN/readout gates"),
    ]
    return [
        {
            **base_row(timestamp),
            "gate_id": gate_id,
            "gate_status": status,
            "claim_allowed": "false",
            "detail": detail,
        }
        for gate_id, status, detail in rows
    ]


def decision_rows(timestamp: str) -> list[dict[str, str]]:
    rows = [
        {
            "decision_id": "DEC3823_0_fixed_integral_projector_selected",
            "decision": "Use fixed integral PiM_total as the clean local source projector route.",
            "rationale": "It is the route that can make [d,Pi_M]J_H vanish without hiding projector stress.",
            "next_action": "make R_eq/topological Hilbert equality the next proof target",
        },
        {
            "decision_id": "DEC3823_1_Hodge_projector_demoted",
            "decision": "Demote Hodge/metric/readout-dependent projectors unless bounded.",
            "rationale": "They create delta Pi_M stress and can mimic source mass calibration.",
            "next_action": "retain R_projector_stress in every affected arena",
        },
        {
            "decision_id": "DEC3823_2_next_target",
            "decision": "Attack R_eq and boundary primitive equality next.",
            "rationale": "The commutator can now be zeroed conditionally; flux closure still needs Pi_M J_H = J_M_top + dB_zero.",
            "next_action": "3824",
        },
    ]
    return [{**base_row(timestamp), **row} for row in rows]


def next_rows(timestamp: str) -> list[dict[str, str]]:
    return [
        {
            **base_row(timestamp),
            "target_doc": "3824-Y5-R2FR-topological-Hilbert-equality-R_eq-and-boundary-primitive-zero-or-bound.md",
            "target_script": "scripts/Y5_R2FR_3824_topological_Hilbert_equality_R_eq_and_boundary_primitive_zero_or_bound.py",
            "objective": "Try to prove or bound the remaining R_eq equality Pi_M J_H = J_M_top + dB_zero and boundary primitive flux needed for compact-exterior source closure.",
            "success_gate": "Either R_eq and B_zero_flux vanish in the fixed PiM_total branch, or each local arena receives finite R_eq/B_zero residual components.",
            "avoid": "do not claim Newton/local GR; do not use orbital GM as source mass; do not edit formalization-workbench; do not use GitHub",
        }
    ]


def status_rows(timestamp: str) -> list[dict[str, str]]:
    return [
        {
            **base_row(timestamp),
            "status": "PASS_NONCLAIM_PIM_FIXEDNESS_COMMUTATOR_ZERO_OR_BOUND_BUILT",
            "summary": "3823 constructs the fixed-integral PiM_total commutator-zero route, demotes moving/Hodge projectors to residuals, maps PiM residuals to local arenas, and selects R_eq boundary equality next.",
        }
    ]


def md_table(rows: list[dict[str, str]], columns: list[str]) -> str:
    header = "| " + " | ".join(columns) + " |"
    sep = "| " + " | ".join(["---"] * len(columns)) + " |"
    body = []
    for row in rows:
        body.append("| " + " | ".join(str(row.get(col, "")).replace("\n", " ").replace("|", "/") for col in columns) + " |")
    return "\n".join([header, sep, *body])


def write_markdown(grouped: dict[str, list[dict[str, str]]]) -> None:
    text = f"""# 3823 - PiM Total Fixedness, Commutator, And Worldtube Domain Zero Or Bound

## Status

`PASS_NONCLAIM_PIM_FIXEDNESS_COMMUTATOR_ZERO_OR_BOUND_BUILT`

This checkpoint builds the clean projector route. If `Pi_M_total` is a fixed integral/source-charge projector over a fixed total-system worldtube and homology class, `[d,Pi_M]J_H` vanishes conditionally. If the projector is Hodge/metric/readout dependent or the domain moves, the effect is retained as explicit source residuals.

## PiM Total Fixedness Theorem

{md_table(grouped["fixedness"], ["theorem_id", "status", "statement", "zero_condition", "failure_residual"])}

## Commutator Zero Or Bound

{md_table(grouped["commutator"], ["commutator_id", "status", "formula", "interpretation", "bound_if_unsigned"])}

## Worldtube Domain Stability

{md_table(grouped["domain"], ["domain_id", "status", "condition", "result", "residual_if_missing"])}

## Arena PiM Residual Map

{md_table(grouped["arena_map"], ["map_id", "arena", "PiM_status", "residual_vector", "meaning"])}

## Residual Rows

{md_table(grouped["residuals"], ["residual_id", "symbol", "definition", "bound_formula", "current_status"])}

## Claim Gates

{md_table(grouped["gates"], ["gate_id", "gate_status", "claim_allowed", "detail"])}

## Next Target

`3824-Y5-R2FR-topological-Hilbert-equality-R_eq-and-boundary-primitive-zero-or-bound.md`

Target: prove or bound `Pi_M J_H = J_M_top + dB_zero` and the boundary primitive flux needed for compact-exterior source closure.

## Machine Outputs

{md_table(grouped["status"], ["status", "summary"])}
"""
    DOC_PATH.write_text(text, encoding="utf-8")


def update_spine() -> None:
    if not SPINE_PATH.exists():
        return
    text = read_text(SPINE_PATH)
    text = text.replace(
        "# Local GR Coupling Spine - Current State After 3822",
        "# Local GR Coupling Spine - Current State After 3823",
    )
    paragraph = (
        "`3823` sharpens the source projector: the clean route is a fixed integral `Pi_M_total` over a fixed total-system worldtube/homology class, which gives "
        "`[d,Pi_M]J_H=0` conditionally because `dPi_M_total=0` on the exterior annulus. Moving domains, Hodge/metric projectors, readout-dependent masks, and arena-specific source projectors are demoted to finite residuals "
        "`R_projector_variation`, `R_domain_motion`, `R_projector_stress`, `R_worldtube_selector`, and `R_arena_projector_tuning`. This removes one major calibration-smuggling route, but full compact-exterior closure still needs `R_eq` and boundary primitive equality.\n\n"
    )
    if "`3823` sharpens the source projector" not in text:
        marker = "`3822` turns the active-mass/source-normalization route"
        index = text.find(marker)
        if index != -1:
            line_end = text.find("\n\n", index)
            if line_end != -1:
                text = text[: line_end + 2] + paragraph + text[line_end + 2 :]
    old_target = """`3823-Y5-R2FR-PiM-total-fixedness-commutator-and-worldtube-domain-zero-or-bound.md`

Target: prove or bound `Pi_M_total` fixedness, `[d,Pi_M]J_H`, and source worldtube/domain stability so the 3822 local arena rows can receive a real source-normalization kernel.

This is the best next move because the source rows are now tagged; the main remaining mathematical risk is that the projector/source domain moves with readout and reintroduces hidden `GM` calibration.
"""
    new_target = """`3824-Y5-R2FR-topological-Hilbert-equality-R_eq-and-boundary-primitive-zero-or-bound.md`

Target: prove or bound the remaining equality `Pi_M J_H = J_M_top + dB_zero` and boundary primitive flux needed for compact-exterior source closure.

This is the best next move because 3823 conditionally kills the projector commutator; the remaining source-kernel obstruction is whether the closed topological current is actually the observed Hilbert mass current.
"""
    text = text.replace(old_target, new_target)
    artifacts = [
        "source-intake\\mts_residuals\\P8_Y5_R2FR_3823_PIM_TOTAL_FIXEDNESS_THEOREM.csv",
        "source-intake\\mts_residuals\\P8_Y5_R2FR_3823_COMMUTATOR_ZERO_OR_BOUND.csv",
        "source-intake\\mts_residuals\\P8_Y5_R2FR_3823_WORLDTUBE_DOMAIN_STABILITY.csv",
        "source-intake\\mts_residuals\\P8_Y5_R2FR_3823_ARENA_PIM_RESIDUAL_MAP.csv",
        "source-intake\\mts_residuals\\P8_Y5_R2FR_3823_PIM_TOTAL_RESIDUAL_ROWS.csv",
        "source-intake\\mts_residuals\\P8_Y5_BRR545_3823_VALIDATION.csv",
    ]
    insertion = "".join(f"- `{artifact}`\n" for artifact in artifacts)
    if artifacts[0] not in text:
        text = text.replace("## Machine Artifacts\n\n", "## Machine Artifacts\n\n" + insertion)
    SPINE_PATH.write_text(text, encoding="utf-8")


def cleanup_pycache() -> None:
    cache = PCW / "scripts" / "__pycache__"
    if cache.exists() and cache.is_dir():
        shutil.rmtree(cache)


def validation_rows(timestamp: str, grouped: dict[str, list[dict[str, str]]]) -> list[dict[str, str]]:
    rows = []

    def add(check_id: str, result: bool, detail: str) -> None:
        rows.append(
            {
                "timestamp_utc": timestamp,
                "branch_id": BRANCH,
                "checkpoint_id": CHECKPOINT,
                "check_id": check_id,
                "result": "PASS" if result else "FAIL",
                "detail": detail,
            }
        )

    add("sources_exist", all(row["exists"] == "True" for row in grouped["sources"]), "every cited source path exists")
    add("needles_found", all(row["needle_found"] == "True" for row in grouped["sources"]), "every cited source needle was found")
    csv_ok = True
    for key, path in OUTPUTS.items():
        if key == "validation":
            continue
        try:
            csv_ok = csv_ok and path.exists() and len(parse_csv(path)) > 0
        except Exception:
            csv_ok = False
    add("csv_outputs_parse", csv_ok, "all generated CSV outputs exist and parse")
    add("doc_written", DOC_PATH.exists() and "PiM Total Fixedness Theorem" in read_text(DOC_PATH), "3823 markdown document written")
    add("fixed_projector_zero_route", any(row["theorem_id"] == "PFX3823_1_fixed_integral_projector" for row in grouped["fixedness"]), "fixed integral PiM zero route emitted")
    add("commutator_identity_written", any(row["commutator_id"] == "COM3823_0_product_rule" for row in grouped["commutator"]), "commutator product identity emitted")
    add("moving_projector_bound_written", any(row["commutator_id"] == "COM3823_2_moving_boundary_term" for row in grouped["commutator"]), "moving-domain residual emitted")
    add("arena_map_written", len(grouped["arena_map"]) >= 6, "PiM residuals mapped to local arenas")
    add("residual_total_row", any(row["symbol"] == "R_PiM_total" for row in grouped["residuals"]), "total PiM residual emitted")
    add("claim_gates_closed", all(row.get("claim_allowed") == "false" for row in grouped["gates"]), "no claim gate allows a claim")
    add("local_gr_blocked", any(row["gate_id"] == "GATE3823_6_Newton_local_GR_claim" and row["gate_status"] == "BLOCKED" for row in grouped["gates"]), "Newton/local GR claim remains blocked")
    add("next_target_selected", grouped["next"][0]["target_doc"].startswith("3824-Y5"), "3824 R_eq target selected")
    spine_text = read_text(SPINE_PATH) if SPINE_PATH.exists() else ""
    add("spine_updated", "Current State After 3823" in spine_text and "3824-Y5-R2FR-topological-Hilbert" in spine_text, "live spine updated to 3823 and 3824 target")
    fwb_hits = list(FWB.rglob("*3823*")) if FWB.exists() else []
    add("formalization_clean", len(fwb_hits) == 0, "no 3823 files written under formalization-workbench")
    add("pycache_removed", not (PCW / "scripts" / "__pycache__").exists(), "scripts __pycache__ removed")
    bad_chars = "\ufffd" in read_text(DOC_PATH) or "\ufffd" in read_text(Path(__file__)) or "\ufffd" in spine_text
    add("bad_chars_clean", not bad_chars, "new doc/script/spine contain no mojibake replacement characters")
    return rows


def main() -> None:
    timestamp = now_utc()
    grouped: dict[str, list[dict[str, str]]] = {}
    grouped["sources"] = source_rows(timestamp)
    grouped["fixedness"] = fixedness_rows(timestamp)
    grouped["commutator"] = commutator_rows(timestamp)
    grouped["domain"] = domain_rows(timestamp)
    grouped["arena_map"] = arena_map_rows(timestamp)
    grouped["residuals"] = residual_rows(timestamp)
    grouped["gates"] = gate_rows(timestamp, grouped)
    grouped["decisions"] = decision_rows(timestamp)
    grouped["next"] = next_rows(timestamp)
    grouped["status"] = status_rows(timestamp)
    grouped["validation"] = [
        {
            "timestamp_utc": timestamp,
            "branch_id": BRANCH,
            "checkpoint_id": CHECKPOINT,
            "check_id": "pending",
            "result": "PASS",
            "detail": "placeholder before final validation",
        }
    ]
    for key, path in OUTPUTS.items():
        if key != "validation":
            write_csv(path, grouped[key])
    write_markdown(grouped)
    update_spine()
    cleanup_pycache()
    grouped["validation"] = validation_rows(timestamp, grouped)
    write_csv(OUTPUTS["validation"], grouped["validation"])
    write_markdown(grouped)
    cleanup_pycache()
    failed = [row for row in grouped["validation"] if row["result"] != "PASS"]
    print(grouped["status"][0]["status"])
    print(f"wrote {DOC_PATH}")
    if failed:
        raise SystemExit(f"validation failed: {failed}")


if __name__ == "__main__":
    main()

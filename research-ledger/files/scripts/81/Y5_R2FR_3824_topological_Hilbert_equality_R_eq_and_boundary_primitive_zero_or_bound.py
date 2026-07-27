from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Iterable


CHECKPOINT = "3824"
BRANCH = "MTS_R2FR_Y5_TOPOLOGICAL_HILBERT_EQUALITY_R_EQ_AND_BOUNDARY_PRIMITIVE_ZERO_OR_BOUND_3824"

PCW = Path(__file__).resolve().parents[1]
ROOT = PCW.parent
FWB = ROOT / "formalization-workbench"
OUT = PCW / "source-intake" / "mts_residuals"
DOC_PATH = PCW / "3824-Y5-R2FR-topological-Hilbert-equality-R_eq-and-boundary-primitive-zero-or-bound.md"
SPINE_PATH = PCW / "LOCAL_GR_COUPLING_SPINE_CURRENT_STATE.md"

P_3823 = PCW / "3823-Y5-R2FR-PiM-total-fixedness-commutator-and-worldtube-domain-zero-or-bound.md"
P_1015 = PCW / "1015-Y5-R10-topological-Hilbert-equality-or-R_eq-bound-runner.md"
P_1016 = PCW / "1016-Y5-R10-parent-worldtube-source-measure-selector-or-R_eq-first-input.md"
P_3777 = PCW / "3777-Y5-R2FR-PiM-total-system-domain-and-EM-field-energy-source-map.md"

CSV_3823_FIXED = OUT / "P8_Y5_R2FR_3823_PIM_TOTAL_FIXEDNESS_THEOREM.csv"
CSV_3823_COMM = OUT / "P8_Y5_R2FR_3823_COMMUTATOR_ZERO_OR_BOUND.csv"
CSV_3823_RESID = OUT / "P8_Y5_R2FR_3823_PIM_TOTAL_RESIDUAL_ROWS.csv"
CSV_1015_SOL = OUT / "P8_Y5_R10_1015_DE_RHAM_SAME_OBJECT_LEMMA.csv"
CSV_1015_HEA = OUT / "P8_Y5_R10_1015_HILBERT_TO_TOPOLOGICAL_EQUALITY_AUDIT.csv"
CSV_1015_REB = OUT / "P8_Y5_R10_1015_R_EQ_BOUND_INPUT_ROWS.csv"
CSV_1015_GATE = OUT / "P8_Y5_R10_1015_CLAIM_GATE.csv"
CSV_1016_CONTRACT = OUT / "P8_Y5_R10_1016_PARENT_SELECTOR_CONTRACT.csv"
CSV_3777_PROJECTOR = OUT / "P8_Y5_R2FR_3777_PIM_TOTAL_PROJECTOR_CONSTRUCTION.csv"
CSV_BOUNDARY_CONTRACT = OUT / "P8_mass_current_Hamiltonian_boundary_charge_CONTRACT.csv"
CSV_BOUNDARY_ACTION = OUT / "P8_Y5_BOUNDARY_REFERENCE_MINIMAL_ACTION_CONTRACT.csv"
CSV_BOUNDARY_CHAIN = OUT / "P8_Y5_BOUNDARY_REFERENCE_CONDITIONAL_THEOREM_CHAIN.csv"
CSV_BOUNDARY_STATUS = OUT / "P8_Y5_BOUNDARY_REFERENCE_FIRST_ROW_STATUS.csv"

OUTPUTS = {
    "sources": OUT / "P8_Y5_R2FR_3824_SOURCE_REGISTER.csv",
    "same_object": OUT / "P8_Y5_R2FR_3824_SAME_OBJECT_DE_RHAM_THEOREM.csv",
    "equality": OUT / "P8_Y5_R2FR_3824_TOPOLOGICAL_HILBERT_EQUALITY_GATE.csv",
    "boundary": OUT / "P8_Y5_R2FR_3824_BOUNDARY_PRIMITIVE_ZERO_OR_BOUND.csv",
    "arena_map": OUT / "P8_Y5_R2FR_3824_ARENA_R_EQ_RESIDUAL_MAP.csv",
    "residuals": OUT / "P8_Y5_R2FR_3824_R_EQ_BOUNDARY_RESIDUAL_ROWS.csv",
    "gates": OUT / "P8_Y5_R2FR_3824_CLAIM_GATES.csv",
    "decisions": OUT / "P8_Y5_R2FR_3824_DECISION_ROWS.csv",
    "next": OUT / "P8_Y5_R2FR_3824_NEXT_TARGET.csv",
    "status": OUT / "P8_Y5_R2FR_3824_STATUS.csv",
    "validation": OUT / "P8_Y5_BRR545_3824_VALIDATION.csv",
}

SOURCE_SPECS = [
    ("SRC3824_0_3823_doc", P_3823, "R_eq + R_flux_leak"),
    ("SRC3824_1_3823_fixed", CSV_3823_FIXED, "PFX3823_1_fixed_integral_projector"),
    ("SRC3824_2_3823_comm", CSV_3823_COMM, "COM3823_4_closure_needed"),
    ("SRC3824_3_3823_resid", CSV_3823_RESID, "R3823_6_total"),
    ("SRC3824_4_1015_doc", P_1015, "same-object lemma"),
    ("SRC3824_5_1015_SOL", CSV_1015_SOL, "SOL1015_3_de_rham_equality"),
    ("SRC3824_6_1015_HEA", CSV_1015_HEA, "HEA1015_3_Hilbert_to_PiM_charge_map"),
    ("SRC3824_7_1015_REB", CSV_1015_REB, "REB1015_0_R_eq_integral"),
    ("SRC3824_8_1015_gate", CSV_1015_GATE, "CG1015_3_topological_Hilbert_equality"),
    ("SRC3824_9_1016_doc", P_1016, "W_source = closure(supp J_H[tau])"),
    ("SRC3824_10_1016_contract", CSV_1016_CONTRACT, "PSC1016_5_dressed_source_charge"),
    ("SRC3824_11_3777_doc", P_3777, "Pi_M Total Projector Construction"),
    ("SRC3824_12_3777_projector", CSV_3777_PROJECTOR, "PIM3777_2_projector_definition"),
    ("SRC3824_13_boundary_contract", CSV_BOUNDARY_CONTRACT, "HC4_charge_equals_PiM_Hilbert_mass"),
    ("SRC3824_14_boundary_action", CSV_BOUNDARY_ACTION, "MAC545_3_boundary_exact_cohomology_zero"),
    ("SRC3824_15_boundary_chain", CSV_BOUNDARY_CHAIN, "CT545_2_boundary_flux_zero"),
    ("SRC3824_16_boundary_status", CSV_BOUNDARY_STATUS, "B_zero_flux"),
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
                "source_role": "R_eq/topological Hilbert equality and boundary primitive input",
            }
        )
    return rows


def same_object_rows(timestamp: str) -> list[dict[str, str]]:
    rows = [
        {
            "theorem_id": "SOD3824_0_fixed_worldtube",
            "status": "EXACT_CONDITIONAL_INPUT",
            "statement": "The topological and Hilbert currents must be attached to the same parent-selected compact total source worldtube W_source.",
            "mathematical_form": "W_source=closure(supp J_M,total[tau]) fixed before readout",
            "if_missing": "closed topological current can conserve the wrong object",
        },
        {
            "theorem_id": "SOD3824_1_same_charge_normalization",
            "status": "EXACT_CONDITIONAL_INPUT",
            "statement": "The topological charge Q_M must equal the same-frame dressed Hilbert/Hamiltonian source charge, not a bare label.",
            "mathematical_form": "Q_M = M_H_ref = c^-2*(H_tau[W,S]-H_ref)",
            "if_missing": "topological charge may be independent of active mass",
        },
        {
            "theorem_id": "SOD3824_2_poincare_dual_representative",
            "status": "EXACT_CONDITIONAL_CONSTRUCTION",
            "statement": "Choose omega_M_top as the Poincare dual representative of the same W_source and homology class.",
            "mathematical_form": "J_M_top=Q_M omega_M_top, d omega_M_top=0, integral_link omega_M_top=1",
            "if_missing": "closed current has no guaranteed relation to Hilbert support",
        },
        {
            "theorem_id": "SOD3824_3_de_rham_same_class",
            "status": "MATHEMATICAL_LEMMA_PASS_CONDITIONAL",
            "statement": "If Pi_M J_H and J_M_top are closed currents in the same compact-support de Rham class, their difference is exact.",
            "mathematical_form": "Pi_M J_H - J_M_top = dB_zero when R_eq=0",
            "if_missing": "retain R_eq as same-class failure",
        },
        {
            "theorem_id": "SOD3824_4_3823_import",
            "status": "COMMUTATOR_CHANNEL_CONDITIONALLY_REMOVED",
            "statement": "The 3823 fixed-integral Pi_M_total branch supplies the missing chain-map condition, so [d,Pi_M]J_H is no longer the main obstruction on this route.",
            "mathematical_form": "dPi_M_total=0 -> [d,Pi_M]J_H=0",
            "if_missing": "fall back to R_PiM_total",
        },
        {
            "theorem_id": "SOD3824_5_verdict",
            "status": "MECHANISM_CONSTRUCTED_NOT_PARENT_SIGNED",
            "statement": "R_eq can be zeroed in the fixed-projector, same-worldtube, same-charge, same-class branch; current MTS still needs parent signatures and boundary primitive control.",
            "mathematical_form": "R_eq=0 if SOD3824_0 through SOD3824_4 are signed",
            "if_missing": "use finite R_eq envelope",
        },
    ]
    return [{**base_row(timestamp), **row} for row in rows]


def equality_rows(timestamp: str) -> list[dict[str, str]]:
    rows = [
        {
            "equality_id": "EQ3824_0_exact_decomposition",
            "status": "EXACT_DECOMPOSITION",
            "formula": "Pi_M J_H = J_M_top + dB_zero + R_eq",
            "meaning": "This is the honest source-kernel equality: topological object, exact improvement, and residual class are separate.",
            "zero_or_bound": "R_eq=0 by same-object theorem, or bound finite shell integral of R_eq",
        },
        {
            "equality_id": "EQ3824_1_surface_charge_equality",
            "status": "EXACT_CONDITIONAL_STOKES_RESULT",
            "formula": "int_S Pi_M J_H = Q_M + int_S dB_zero + int_S R_eq",
            "meaning": "Surface charge equals topological/Hilbert mass only if boundary primitive and residual integrals vanish or are bounded.",
            "zero_or_bound": "B_zero_flux=0 and R_eq_integral=0, or retain both",
        },
        {
            "equality_id": "EQ3824_2_boundary_reference_role",
            "status": "BOUNDARY_GATE_EXPOSED",
            "formula": "Delta_Q = B_zero_flux + Delta_symp + R_eq_integral",
            "meaning": "The remaining ambiguity is not hidden in mass: it is a boundary/reference/same-class residual.",
            "zero_or_bound": "derive boundary primitive zero or source-backed epsilon_boundary_reference_abs",
        },
        {
            "equality_id": "EQ3824_3_compact_exterior_closure",
            "status": "NOT_YET_FULL_CLOSURE",
            "formula": "d(Pi_M J_H)=0 requires 3823 commutator zero plus R_eq/B_zero/extra-channel silence",
            "meaning": "3824 improves equality, but does not by itself claim Gauss/Newton closure.",
            "zero_or_bound": "next target must close boundary/reference and compact flux",
        },
    ]
    return [{**base_row(timestamp), **row} for row in rows]


def boundary_rows(timestamp: str) -> list[dict[str, str]]:
    specs = [
        ("BPR3824_0_B_zero_flux", "B_zero_flux", "linked-surface flux of exact/improvement primitive", "int_S2 dB_zero - int_S1 dB_zero or int_A d(dB_zero) with cohomology defects", "zero if boundary exact form is cohomologically trivial and reference locked"),
        ("BPR3824_1_Delta_symp", "Delta_symp", "symplectic/reference subtraction drift between linked surfaces", "int_dA(omega_extra+omega_ref+omega_PiM)", "zero if parent symplectic current, reference, and projector stress are fixed"),
        ("BPR3824_2_R_eq_integral", "R_eq_integral", "finite-shell integral of same-class failure", "int_shell |Pi_M J_H - J_M_top - dB_zero| / M_H_ref", "zero if same compact de Rham class is parent-signed"),
        ("BPR3824_3_MHref_denominator", "M_H_ref", "positive same-frame source denominator", "c^-2*(H_tau-H_ref)", "needed so residuals are physical dimensionless source errors"),
        ("BPR3824_4_boundary_total", "epsilon_boundary_R_eq_total", "total equality/boundary residual", "sum_abs(B_zero_flux,Delta_symp,R_eq_integral)/M_H_ref", "feeds local test rows until zeroed or sourced"),
    ]
    return [
        {
            **base_row(timestamp),
            "boundary_id": boundary_id,
            "symbol": symbol,
            "definition": definition,
            "bound_formula": formula,
            "exit_requirement": exit_requirement,
            "current_status": "ZERO_IF_PARENT_BOUNDARY_CONTRACT_SIGNED_ELSE_BOUND_REQUIRED",
        }
        for boundary_id, symbol, definition, formula, exit_requirement in specs
    ]


def arena_map_rows(timestamp: str) -> list[dict[str, str]]:
    arenas = [
        ("R10_short_range_lab", "R_eq_integral+B_zero_flux+M_H_ref", "R10 alpha rows cannot claim until source mass and boundary equality are source-backed"),
        ("WEP_MICROSCOPE_lab", "R_eq_integral+Delta_worldtube_domain+epsilon_parent_exchange", "same topological/Hilbert source measure must feed material response"),
        ("PPN_gamma_beta", "R_eq_integral+B_zero_flux+projector_stress_beta_equiv", "PPN metric residuals cannot absorb source equality defects"),
        ("clock_redshift_Gdot", "Delta_symp+B_zero_flux+M_H_ref", "clock/tau reference cannot define the source potential it tests"),
        ("orbital_GM_Gauss", "R_eq_integral+B_zero_flux+R_mu_split", "orbital mu remains product evidence until equality and boundary primitive close"),
        ("EM_Poynting_source_stress", "R_eq_integral+B_zero_flux+Delta_extra_vector", "EM/Poynting stress must be same Hilbert source or retained as mu_extra"),
    ]
    return [
        {
            **base_row(timestamp),
            "map_id": f"REQ3824_{index}",
            "arena": arena,
            "R_eq_boundary_vector": vector,
            "meaning": meaning,
            "claim_policy": "nonclaim until R_eq/B_zero/MHref components are theorem-zero or source-backed bounded",
        }
        for index, (arena, vector, meaning) in enumerate(arenas)
    ]


def residual_rows(timestamp: str) -> list[dict[str, str]]:
    specs = [
        ("R3824_0_same_class", "R_eq_integral", "same de Rham class failure between Pi_M J_H and J_M_top+dB_zero", "int_shell |Pi_M J_H-J_M_top-dB_zero|/M_H_ref"),
        ("R3824_1_boundary_primitive", "B_zero_flux", "boundary primitive/improvement flux through linked compact surfaces", "|int_S dB_zero|/M_H_ref"),
        ("R3824_2_symplectic_reference", "Delta_symp", "Hamiltonian reference/symplectic subtraction drift", "|Delta_symp|/M_H_ref"),
        ("R3824_3_worldtube_class", "Delta_worldtube_domain", "topological/Hilbert worldtube/domain mismatch", "|Delta Q_domain|/M_H_ref"),
        ("R3824_4_denominator", "R_MHref_positive", "missing positive same-frame Hilbert denominator", "MISSING_M_H_ref_or_sign"),
        ("R3824_5_total", "R_eq_boundary_total", "total topological-Hilbert equality and boundary primitive residual", "sum_abs(R_eq_integral,B_zero_flux,Delta_symp,Delta_worldtube_domain,R_MHref_positive)"),
    ]
    return [
        {
            **base_row(timestamp),
            "residual_id": residual_id,
            "symbol": symbol,
            "definition": definition,
            "bound_formula": formula,
            "units": "dimensionless_after_MHref_normalization_or_structural_if_denominator_missing",
            "current_status": "ZERO_IF_SAME_OBJECT_AND_BOUNDARY_PRIMITIVE_SIGNED_ELSE_BOUND_REQUIRED",
            "exit_requirement": "parent theorem-zero or source-backed finite bound",
        }
        for residual_id, symbol, definition, formula in specs
    ]


def gate_rows(timestamp: str, grouped: dict[str, list[dict[str, str]]]) -> list[dict[str, str]]:
    sources_pass = all(row["exists"] == "True" and row["needle_found"] == "True" for row in grouped["sources"])
    rows = [
        ("GATE3824_0_sources", "PASS_NONCLAIM" if sources_pass else "FAIL", "all source paths and needles present" if sources_pass else "missing source path or needle"),
        ("GATE3824_1_same_object_math", "PASS_CONDITIONAL_ZERO", "de Rham same-object route strengthened with fixed PiM_total"),
        ("GATE3824_2_R_eq_zero_route", "PASS_CONDITIONAL_ZERO", "R_eq can vanish if same worldtube/source measure/class are parent-signed"),
        ("GATE3824_3_boundary_primitive", "BLOCKED_BOUND_REQUIRED", "B_zero_flux and Delta_symp remain unsigned boundary/reference terms"),
        ("GATE3824_4_MHref_denominator", "BLOCKED_INPUT_REQUIRED", "positive same-frame M_H_ref remains needed for claim-grade normalization"),
        ("GATE3824_5_arena_map", "PASS_NONCLAIM", "R_eq/boundary residuals mapped to local test arenas"),
        ("GATE3824_6_Newton_local_GR_claim", "BLOCKED", "local GR/Newton still waits on boundary/reference/MHref plus PPN/readout gates"),
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
            "decision_id": "DEC3824_0_R_eq_route_strengthened",
            "decision": "Treat R_eq as conditionally zeroable, not a permanent vague missing row.",
            "rationale": "3823 supplies fixed PiM_total; 1015 supplies same-class de Rham exactness; together they give a real same-object theorem path.",
            "next_action": "attack boundary primitive/reference and M_H_ref normalization",
        },
        {
            "decision_id": "DEC3824_1_boundary_not_optional",
            "decision": "Do not promote equality while B_zero_flux or Delta_symp are unsigned.",
            "rationale": "Exact labels do not stop finite boundary charges unless cohomology/reference conditions are fixed.",
            "next_action": "3825 boundary reference theorem or first finite row",
        },
        {
            "decision_id": "DEC3824_2_next_target",
            "decision": "Move to boundary-reference primitive and denominator lock.",
            "rationale": "The equality route now fails mainly at boundary/reference/M_H_ref, not at projector commutator.",
            "next_action": "3825",
        },
    ]
    return [{**base_row(timestamp), **row} for row in rows]


def next_rows(timestamp: str) -> list[dict[str, str]]:
    return [
        {
            **base_row(timestamp),
            "target_doc": "3825-Y5-R2FR-boundary-reference-primitive-and-MHref-denominator-zero-or-first-source-row.md",
            "target_script": "scripts/Y5_R2FR_3825_boundary_reference_primitive_and_MHref_denominator_zero_or_first_source_row.py",
            "objective": "Try to prove or bound B_zero_flux, Delta_symp, and positive M_H_ref denominator using the minimal boundary/reference action contract; otherwise emit the first source-ready finite rows.",
            "success_gate": "Either boundary/reference primitive terms and denominator are parent-owned enough to feed source normalization, or finite source-ready rows exist with units and no claim gate opens.",
            "avoid": "do not claim Newton/local GR; do not use orbital GM as source mass; do not edit formalization-workbench; do not use GitHub",
        }
    ]


def status_rows(timestamp: str) -> list[dict[str, str]]:
    return [
        {
            **base_row(timestamp),
            "status": "PASS_NONCLAIM_R_EQ_SAME_OBJECT_ROUTE_AND_BOUNDARY_RESIDUALS_BUILT",
            "summary": "3824 strengthens the topological-Hilbert equality route with fixed PiM_total, makes R_eq conditionally zeroable, keeps boundary/reference and M_H_ref as explicit finite blockers, and selects 3825.",
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
    text = f"""# 3824 - Topological-Hilbert Equality R_eq And Boundary Primitive Zero Or Bound

## Status

`PASS_NONCLAIM_R_EQ_SAME_OBJECT_ROUTE_AND_BOUNDARY_RESIDUALS_BUILT`

This checkpoint strengthens the old same-object lemma using the new fixed-`Pi_M_total` branch. `R_eq` is no longer just a foggy blocker: it is zero if the fixed Hilbert source worldtube, same source charge, Poincare dual representative, and fixed projector conditions are parent-signed. The boundary/reference primitive and positive `M_H_ref` denominator still block any Newton/local-GR claim.

## Same-Object de Rham Theorem

{md_table(grouped["same_object"], ["theorem_id", "status", "statement", "mathematical_form", "if_missing"])}

## Topological-Hilbert Equality Gate

{md_table(grouped["equality"], ["equality_id", "status", "formula", "meaning", "zero_or_bound"])}

## Boundary Primitive Zero Or Bound

{md_table(grouped["boundary"], ["boundary_id", "symbol", "definition", "bound_formula", "exit_requirement"])}

## Arena R_eq Residual Map

{md_table(grouped["arena_map"], ["map_id", "arena", "R_eq_boundary_vector", "meaning"])}

## Residual Rows

{md_table(grouped["residuals"], ["residual_id", "symbol", "definition", "bound_formula", "current_status"])}

## Claim Gates

{md_table(grouped["gates"], ["gate_id", "gate_status", "claim_allowed", "detail"])}

## Next Target

`3825-Y5-R2FR-boundary-reference-primitive-and-MHref-denominator-zero-or-first-source-row.md`

Target: prove or bound `B_zero_flux`, `Delta_symp`, and positive `M_H_ref` using the minimal boundary/reference action contract, or emit first source-ready finite rows.

## Machine Outputs

{md_table(grouped["status"], ["status", "summary"])}
"""
    DOC_PATH.write_text(text, encoding="utf-8")


def update_spine() -> None:
    if not SPINE_PATH.exists():
        return
    text = read_text(SPINE_PATH)
    text = text.replace(
        "# Local GR Coupling Spine - Current State After 3823",
        "# Local GR Coupling Spine - Current State After 3824",
    )
    paragraph = (
        "`3824` strengthens the topological-Hilbert equality route: with the fixed `Pi_M_total` branch from 3823, the same-object de Rham lemma now says "
        "`Pi_M J_H = J_M_top + dB_zero` and `R_eq=0` if the compact Hilbert worldtube, same-frame dressed source charge, Poincare-dual representative, and fixed chain-map conditions are parent-signed. "
        "The remaining obstruction is sharper: finite `B_zero_flux`, `Delta_symp`, and positive `M_H_ref` denominator must be proved or source-backed. No Newton/local-GR claim opens.\n\n"
    )
    if "`3824` strengthens the topological-Hilbert equality route" not in text:
        marker = "`3823` sharpens the source projector"
        index = text.find(marker)
        if index != -1:
            line_end = text.find("\n\n", index)
            if line_end != -1:
                text = text[: line_end + 2] + paragraph + text[line_end + 2 :]
    old_target = """`3824-Y5-R2FR-topological-Hilbert-equality-R_eq-and-boundary-primitive-zero-or-bound.md`

Target: prove or bound the remaining equality `Pi_M J_H = J_M_top + dB_zero` and boundary primitive flux needed for compact-exterior source closure.

This is the best next move because 3823 conditionally kills the projector commutator; the remaining source-kernel obstruction is whether the closed topological current is actually the observed Hilbert mass current.
"""
    new_target = """`3825-Y5-R2FR-boundary-reference-primitive-and-MHref-denominator-zero-or-first-source-row.md`

Target: prove or bound `B_zero_flux`, `Delta_symp`, and positive `M_H_ref` using the minimal boundary/reference action contract, or emit first source-ready finite rows.

This is the best next move because 3824 makes `R_eq` conditionally zeroable; the equality route now bottlenecks on boundary/reference primitive terms and denominator normalization.
"""
    text = text.replace(old_target, new_target)
    artifacts = [
        "source-intake\\mts_residuals\\P8_Y5_R2FR_3824_SAME_OBJECT_DE_RHAM_THEOREM.csv",
        "source-intake\\mts_residuals\\P8_Y5_R2FR_3824_TOPOLOGICAL_HILBERT_EQUALITY_GATE.csv",
        "source-intake\\mts_residuals\\P8_Y5_R2FR_3824_BOUNDARY_PRIMITIVE_ZERO_OR_BOUND.csv",
        "source-intake\\mts_residuals\\P8_Y5_R2FR_3824_ARENA_R_EQ_RESIDUAL_MAP.csv",
        "source-intake\\mts_residuals\\P8_Y5_R2FR_3824_R_EQ_BOUNDARY_RESIDUAL_ROWS.csv",
        "source-intake\\mts_residuals\\P8_Y5_BRR545_3824_VALIDATION.csv",
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
    add("doc_written", DOC_PATH.exists() and "Same-Object de Rham Theorem" in read_text(DOC_PATH), "3824 markdown document written")
    add("same_object_theorem_written", any(row["theorem_id"] == "SOD3824_3_de_rham_same_class" for row in grouped["same_object"]), "same-object de Rham theorem emitted")
    add("fixed_pim_imported", any(row["theorem_id"] == "SOD3824_4_3823_import" for row in grouped["same_object"]), "3823 fixed PiM import emitted")
    add("equality_decomposition_written", any(row["equality_id"] == "EQ3824_0_exact_decomposition" for row in grouped["equality"]), "PiM/Hilbert/topological decomposition emitted")
    add("boundary_terms_retained", any(row["symbol"] == "B_zero_flux" for row in grouped["boundary"]) and any(row["symbol"] == "Delta_symp" for row in grouped["boundary"]), "boundary/reference terms retained")
    add("arena_map_written", len(grouped["arena_map"]) >= 6, "R_eq residuals mapped to local arenas")
    add("residual_total_row", any(row["symbol"] == "R_eq_boundary_total" for row in grouped["residuals"]), "total R_eq boundary residual emitted")
    add("claim_gates_closed", all(row.get("claim_allowed") == "false" for row in grouped["gates"]), "no claim gate allows a claim")
    add("local_gr_blocked", any(row["gate_id"] == "GATE3824_6_Newton_local_GR_claim" and row["gate_status"] == "BLOCKED" for row in grouped["gates"]), "Newton/local GR claim remains blocked")
    add("next_target_selected", grouped["next"][0]["target_doc"].startswith("3825-Y5"), "3825 boundary/MHref target selected")
    spine_text = read_text(SPINE_PATH) if SPINE_PATH.exists() else ""
    add("spine_updated", "Current State After 3824" in spine_text and "3825-Y5-R2FR-boundary-reference" in spine_text, "live spine updated to 3824 and 3825 target")
    fwb_hits = list(FWB.rglob("*3824*")) if FWB.exists() else []
    add("formalization_clean", len(fwb_hits) == 0, "no 3824 files written under formalization-workbench")
    add("pycache_removed", not (PCW / "scripts" / "__pycache__").exists(), "scripts __pycache__ removed")
    bad_chars = "\ufffd" in read_text(DOC_PATH) or "\ufffd" in read_text(Path(__file__)) or "\ufffd" in spine_text
    add("bad_chars_clean", not bad_chars, "new doc/script/spine contain no mojibake replacement characters")
    return rows


def main() -> None:
    timestamp = now_utc()
    grouped: dict[str, list[dict[str, str]]] = {}
    grouped["sources"] = source_rows(timestamp)
    grouped["same_object"] = same_object_rows(timestamp)
    grouped["equality"] = equality_rows(timestamp)
    grouped["boundary"] = boundary_rows(timestamp)
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

from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Iterable


CHECKPOINT = "3825"
BRANCH = "MTS_R2FR_Y5_BOUNDARY_REFERENCE_PRIMITIVE_AND_MHREF_DENOMINATOR_ZERO_OR_FIRST_SOURCE_ROW_3825"

PCW = Path(__file__).resolve().parents[1]
ROOT = PCW.parent
FWB = ROOT / "formalization-workbench"
OUT = PCW / "source-intake" / "mts_residuals"
DOC_PATH = PCW / "3825-Y5-R2FR-boundary-reference-primitive-and-MHref-denominator-zero-or-first-source-row.md"
SPINE_PATH = PCW / "LOCAL_GR_COUPLING_SPINE_CURRENT_STATE.md"

P_3824 = PCW / "3824-Y5-R2FR-topological-Hilbert-equality-R_eq-and-boundary-primitive-zero-or-bound.md"
P_3821 = PCW / "3821-Y5-R2FR-closed-system-stress-virial-cancellation-or-pressure-binding-bound.md"
P_3820 = PCW / "3820-Y5-R2FR-Komar-Tolman-active-mass-and-independent-source-ledger.md"
P_1006 = PCW / "1006-Y5-R10-MHref-positive-same-frame-denominator-or-Htau-source-row.md"

CSV_3824_BOUNDARY = OUT / "P8_Y5_R2FR_3824_BOUNDARY_PRIMITIVE_ZERO_OR_BOUND.csv"
CSV_3824_RESID = OUT / "P8_Y5_R2FR_3824_R_EQ_BOUNDARY_RESIDUAL_ROWS.csv"
CSV_3824_NEXT = OUT / "P8_Y5_R2FR_3824_NEXT_TARGET.csv"
CSV_BOUNDARY_ACTION = OUT / "P8_Y5_BOUNDARY_REFERENCE_MINIMAL_ACTION_CONTRACT.csv"
CSV_BOUNDARY_CHAIN = OUT / "P8_Y5_BOUNDARY_REFERENCE_CONDITIONAL_THEOREM_CHAIN.csv"
CSV_BOUNDARY_STATUS = OUT / "P8_Y5_BOUNDARY_REFERENCE_FIRST_ROW_STATUS.csv"
CSV_1006_AUDIT = OUT / "P8_Y5_R10_1006_MHREF_DENOMINATOR_THEOREM_AUDIT.csv"
CSV_1006_SCHEMA = OUT / "P8_Y5_R10_1006_DENOMINATOR_SOURCE_SCHEMA.csv"
CSV_1006_REFUSAL = OUT / "P8_Y5_R10_1006_REFUSAL_LEDGER.csv"
CSV_3820_KOMAR = OUT / "P8_Y5_R2FR_3820_KOMAR_TOLMAN_ACTIVE_MASS_DERIVATION.csv"
CSV_3821_VIRIAL = OUT / "P8_Y5_R2FR_3821_STRESS_VIRIAL_THEOREM.csv"

OUTPUTS = {
    "sources": OUT / "P8_Y5_R2FR_3825_SOURCE_REGISTER.csv",
    "boundary_theorem": OUT / "P8_Y5_R2FR_3825_BOUNDARY_REFERENCE_ZERO_THEOREM.csv",
    "denominator": OUT / "P8_Y5_R2FR_3825_MHREF_POSITIVE_DENOMINATOR_LAW.csv",
    "first_rows": OUT / "P8_Y5_R2FR_3825_FIRST_SOURCE_READY_BOUNDARY_MHREF_ROWS.csv",
    "arena_map": OUT / "P8_Y5_R2FR_3825_BOUNDARY_MHREF_ARENA_MAP.csv",
    "residuals": OUT / "P8_Y5_R2FR_3825_BOUNDARY_MHREF_RESIDUAL_ROWS.csv",
    "gates": OUT / "P8_Y5_R2FR_3825_CLAIM_GATES.csv",
    "decisions": OUT / "P8_Y5_R2FR_3825_DECISION_ROWS.csv",
    "next": OUT / "P8_Y5_R2FR_3825_NEXT_TARGET.csv",
    "status": OUT / "P8_Y5_R2FR_3825_STATUS.csv",
    "validation": OUT / "P8_Y5_BRR545_3825_VALIDATION.csv",
}

SOURCE_SPECS = [
    ("SRC3825_0_3824_doc", P_3824, "Boundary Primitive Zero Or Bound"),
    ("SRC3825_1_3824_boundary", CSV_3824_BOUNDARY, "BPR3824_0_B_zero_flux"),
    ("SRC3825_2_3824_resid", CSV_3824_RESID, "R3824_5_total"),
    ("SRC3825_3_3824_next", CSV_3824_NEXT, "3825-Y5-R2FR-boundary-reference-primitive"),
    ("SRC3825_4_boundary_action", CSV_BOUNDARY_ACTION, "MAC545_6_positive_measured_denominator"),
    ("SRC3825_5_boundary_chain", CSV_BOUNDARY_CHAIN, "CT545_5_conditional_plateau"),
    ("SRC3825_6_boundary_status", CSV_BOUNDARY_STATUS, "epsilon_boundary_reference_abs"),
    ("SRC3825_7_1006_doc", P_1006, "positive same-frame M_H_ref"),
    ("SRC3825_8_1006_audit", CSV_1006_AUDIT, "MHA1006_4_positivity"),
    ("SRC3825_9_1006_schema", CSV_1006_SCHEMA, "MHS1006_0_Htau_minus_Href"),
    ("SRC3825_10_1006_refusal", CSV_1006_REFUSAL, "MRF1006_3_orbital_GM_substitution"),
    ("SRC3825_11_3820_doc", P_3820, "Komar/Tolman active-mass route"),
    ("SRC3825_12_3820_komar", CSV_3820_KOMAR, "KT3820_4_slow_weak_Newton_limit"),
    ("SRC3825_13_3821_doc", P_3821, "closed stationary total source"),
    ("SRC3825_14_3821_virial", CSV_3821_VIRIAL, "SVT3821_2_trace_cancellation"),
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
                "source_role": "boundary reference primitive and MHref denominator input",
            }
        )
    return rows


def boundary_theorem_rows(timestamp: str) -> list[dict[str, str]]:
    rows = [
        {
            "theorem_id": "BRT3825_0_covariant_boundary_charge",
            "status": "EXACT_CONDITIONAL_CHARGE_SETUP",
            "statement": "If a covariant parent action fixes L, Theta, and B_ref before readout, B_zero_flux and Delta_symp are derived charge terms rather than adjustable constants.",
            "formula": "delta L = E_A delta Phi^A + dTheta; J_tau=Theta(Phi,L_tau Phi)-i_tau L",
            "zero_condition": "MAC545_0 parent action and boundary term are owned",
        },
        {
            "theorem_id": "BRT3825_1_annulus_stokes",
            "status": "EXACT_CONDITIONAL_ZERO",
            "statement": "On a source-free exterior annulus with constraints and exchange terms silent, linked surface charge drift vanishes by Stokes.",
            "formula": "int_S2 q_tau - int_S1 q_tau = int_A d q_tau = 0",
            "zero_condition": "MAC545_1 plus closed C terms",
        },
        {
            "theorem_id": "BRT3825_2_B_zero_flux_zero",
            "status": "EXACT_CONDITIONAL_ZERO",
            "statement": "An exact boundary/improvement term has zero linked-surface flux only when it is cohomologically trivial on the annulus and carries no vector/tensor/source hair.",
            "formula": "B_zero_flux = int_S2 B_imp - int_S1 B_imp = int_A dB_imp = 0",
            "zero_condition": "MAC545_3 and MAC545_4",
        },
        {
            "theorem_id": "BRT3825_3_Delta_symp_zero",
            "status": "EXACT_CONDITIONAL_ZERO",
            "statement": "The symplectic/reference drift vanishes only when the reference is locked and the fixed PiM projector carries no exterior symplectic stress.",
            "formula": "Delta_symp = int_dA(omega_extra + omega_ref + omega_PiM) = 0",
            "zero_condition": "MAC545_2 and MAC545_5 plus 3823 fixed PiM_total",
        },
        {
            "theorem_id": "BRT3825_4_no_plateau_axiom",
            "status": "CONDITIONAL_MECHANISM_NOT_AXIOM",
            "statement": "The boundary/reference numerator vanishes by covariant charge/Stokes/cohomology/reference-lock conditions, not by adding a local plateau axiom.",
            "formula": "epsilon_BR numerator = B_zero_flux + Delta_symp -> 0 under MAC545_0..5",
            "zero_condition": "all parent boundary clauses signed",
        },
        {
            "theorem_id": "BRT3825_5_verdict",
            "status": "ZERO_ROUTE_WRITTEN_FIRST_ROWS_REQUIRED",
            "statement": "The zero route is exact conditionally, but current MTS has no claim-valid parent boundary theorem or source-backed B_zero/Delta_symp row.",
            "formula": "use finite first rows until signed",
            "zero_condition": "not currently met",
        },
    ]
    return [{**base_row(timestamp), **row} for row in rows]


def denominator_rows(timestamp: str) -> list[dict[str, str]]:
    rows = [
        {
            "law_id": "MHD3825_0_charge_definition",
            "status": "EXACT_CONDITIONAL_DEFINITION",
            "statement": "The denominator is the same-frame Hamiltonian/active source charge, not orbital GM.",
            "formula": "M_H_ref = c^-2*(H_tau[S_link]-H_ref)",
            "required_evidence": "finite H_tau, fixed H_ref, tau/coframe lock, source worldtube, units",
        },
        {
            "law_id": "MHD3825_1_Komar_Tolman_energy_route",
            "status": "EXACT_CONDITIONAL_POSITIVE_ENERGY_ROUTE",
            "statement": "For a closed stationary total source, 3820/3821 reduce the active charge to total energy over c^2 plus finite correction terms.",
            "formula": "M_H_ref = E_total/c^2 + R_boundary + R_nonEH + R_pressure_binding",
            "required_evidence": "closed total source, positive energy/reference, stress-virial residuals zero or bounded",
        },
        {
            "law_id": "MHD3825_2_positivity_condition",
            "status": "CONDITIONAL_POSITIVITY_NOT_CLAIMED",
            "statement": "M_H_ref is positive if E_total-H_ref is positive and boundary/reference/extra-sector subtraction cannot over-remove the source charge.",
            "formula": "M_H_ref>0 if E_total >= E_ref + |R_boundary+R_extra|",
            "required_evidence": "positive-energy theorem or source-backed lower bound",
        },
        {
            "law_id": "MHD3825_3_anti_circularity",
            "status": "EXACT_GUARD",
            "statement": "GM_orbit/G_ref remains forbidden as the source denominator for the same Newton/local-GR claim.",
            "formula": "M_H_ref != mu_fit/G_ref unless Poisson/Gauss/source bridge is already derived independently",
            "required_evidence": "not_orbital_GM_imported=true",
        },
        {
            "law_id": "MHD3825_4_verdict",
            "status": "FIRST_ROW_NEEDED_NOT_CLAIM",
            "statement": "The denominator route is physically coherent after 3820/3821, but it still needs a sourced row or a parent positive-energy/boundary theorem.",
            "formula": "M_H_ref row must include units, tau_frame_id, coframe_id, boundary_domain, counterterm convention and source path",
            "required_evidence": "MHS1006 schema filled without MISSING markers",
        },
    ]
    return [{**base_row(timestamp), **row} for row in rows]


def first_source_rows(timestamp: str) -> list[dict[str, str]]:
    rows = [
        {
            "row_id": "FSR3825_0_B_zero_flux",
            "quantity": "B_zero_flux",
            "formula": "int_S2 B_imp - int_S1 B_imp",
            "units": "GM_flux_or_dimensionless_after_MHref",
            "required_columns": "system_id;S_inner;S_outer;B_imp_form;cohomology_certificate;reference_id;value;units;source_path;equation_ref;valid_for_claim",
            "current_value": "MISSING_B_ZERO_FLUX",
            "source_ready_status": "SCHEMA_READY_VALUE_MISSING",
        },
        {
            "row_id": "FSR3825_1_Delta_symp",
            "quantity": "Delta_symp",
            "formula": "int_dA(omega_extra+omega_ref+omega_PiM)",
            "units": "GM_flux_or_dimensionless_after_MHref",
            "required_columns": "system_id;annulus_id;symplectic_current;reference_lock;PiM_stress_status;value;units;source_path;equation_ref;valid_for_claim",
            "current_value": "MISSING_DELTA_SYMP",
            "source_ready_status": "SCHEMA_READY_VALUE_MISSING",
        },
        {
            "row_id": "FSR3825_2_MHref",
            "quantity": "M_H_ref",
            "formula": "c^-2*(H_tau-H_ref)",
            "units": "mass",
            "required_columns": "system_id;H_tau;H_tau_units;H_ref;H_ref_units;M_H_ref;M_H_ref_units;tau_frame_id;coframe_id;boundary_domain;counterterm_convention;positivity_certificate;not_orbital_GM_imported;source_path;equation_ref;valid_for_claim",
            "current_value": "MISSING_M_H_REF",
            "source_ready_status": "SCHEMA_READY_VALUE_MISSING",
        },
        {
            "row_id": "FSR3825_3_epsilon_boundary_reference_abs",
            "quantity": "epsilon_boundary_reference_abs",
            "formula": "(abs(B_zero_flux)+abs(Delta_symp))/M_H_ref",
            "units": "dimensionless",
            "required_columns": "system_id;B_zero_flux;Delta_symp;M_H_ref;component_units_match;no_cancellation_sum;source_path;equation_ref;valid_for_claim",
            "current_value": "MISSING_COMPONENT_INPUTS",
            "source_ready_status": "SCHEMA_READY_COMPONENTS_MISSING",
        },
        {
            "row_id": "FSR3825_4_boundary_MHref_bundle",
            "quantity": "boundary_MHref_bundle",
            "formula": "bundle(B_zero_flux,Delta_symp,M_H_ref,epsilon_boundary_reference_abs)",
            "units": "mixed_declared_per_component",
            "required_columns": "system_id;all_component_row_ids;all_source_paths;all_units;all_valid_for_claim;claim_allowed",
            "current_value": "BUNDLE_NONCLAIM_UNTIL_COMPONENTS_VALID",
            "source_ready_status": "BUNDLE_SCHEMA_READY_NONCLAIM",
        },
    ]
    return [{**base_row(timestamp), **row} for row in rows]


def arena_map_rows(timestamp: str) -> list[dict[str, str]]:
    arenas = [
        ("R10_short_range_lab", "B_zero_flux+Delta_symp+M_H_ref", "R10 source normalization can use lab mass only after boundary/MHref bundle is filled"),
        ("WEP_MICROSCOPE_lab", "Delta_symp+M_H_ref+tau_frame_id", "WEP material/source weights must share the same denominator frame"),
        ("PPN_gamma_beta", "B_zero_flux+Delta_symp+projector_stress", "PPN residuals cannot absorb boundary/reference drift"),
        ("clock_redshift_Gdot", "Delta_symp+H_ref+tau_frame_id", "clock potential cannot set its own boundary reference"),
        ("orbital_GM_Gauss", "M_H_ref+not_orbital_GM_imported+B_zero_flux", "orbital mu remains product evidence until denominator is independent"),
        ("EM_Poynting_source_stress", "B_zero_flux+Delta_symp+total_domain_tail", "EM field support must be in the same boundary/reference bundle or retained"),
    ]
    return [
        {
            **base_row(timestamp),
            "map_id": f"BMA3825_{index}",
            "arena": arena,
            "boundary_MHref_vector": vector,
            "meaning": meaning,
            "claim_policy": "nonclaim until the boundary/MHref bundle is theorem-zero or source-backed",
        }
        for index, (arena, vector, meaning) in enumerate(arenas)
    ]


def residual_rows(timestamp: str) -> list[dict[str, str]]:
    specs = [
        ("R3825_0_B_zero_flux", "B_zero_flux", "boundary/improvement linked-surface flux numerator", "MISSING_B_ZERO_FLUX or theorem-zero"),
        ("R3825_1_Delta_symp", "Delta_symp", "Hamiltonian reference/symplectic drift numerator", "MISSING_DELTA_SYMP or theorem-zero"),
        ("R3825_2_MHref", "R_MHref_denominator", "positive same-frame source denominator failure", "MISSING_M_H_REF or positivity/sign failure"),
        ("R3825_3_boundary_reference_abs", "epsilon_boundary_reference_abs", "absolute boundary/reference residual envelope", "(abs(B_zero_flux)+abs(Delta_symp))/M_H_ref"),
        ("R3825_4_total", "R_boundary_MHref_total", "combined boundary/reference/denominator obstruction", "epsilon_boundary_reference_abs + R_MHref_denominator"),
    ]
    return [
        {
            **base_row(timestamp),
            "residual_id": residual_id,
            "symbol": symbol,
            "definition": definition,
            "bound_formula": formula,
            "units": "dimensionless_or_component_units_declared",
            "current_status": "FIRST_SOURCE_ROW_READY_BUT_UNFILLED",
            "exit_requirement": "parent theorem-zero or source-backed filled row with no MISSING markers",
        }
        for residual_id, symbol, definition, formula in specs
    ]


def gate_rows(timestamp: str, grouped: dict[str, list[dict[str, str]]]) -> list[dict[str, str]]:
    sources_pass = all(row["exists"] == "True" and row["needle_found"] == "True" for row in grouped["sources"])
    all_first_rows_nonclaim = all(row["valid_for_claim"] == "false" and row["claim_allowed"] == "false" for row in grouped["first_rows"])
    rows = [
        ("GATE3825_0_sources", "PASS_NONCLAIM" if sources_pass else "FAIL", "all source paths and needles present" if sources_pass else "missing source path or needle"),
        ("GATE3825_1_boundary_zero_route", "PASS_CONDITIONAL_ZERO", "B_zero_flux/Delta_symp zero route derived from MAC545 clauses"),
        ("GATE3825_2_MHref_positive_route", "PASS_CONDITIONAL_ZERO", "positive MHref route derived from active energy plus stress-virial branch"),
        ("GATE3825_3_first_source_rows", "PASS_NONCLAIM" if all_first_rows_nonclaim else "FAIL", "first source-ready rows emitted but remain nonclaim"),
        ("GATE3825_4_orbital_GM_guard", "PASS_GUARD", "M_H_ref row requires not_orbital_GM_imported"),
        ("GATE3825_5_claim_ready_boundary_bundle", "BLOCKED_INPUT_REQUIRED", "B_zero_flux, Delta_symp, M_H_ref values/theorems are not claim-valid"),
        ("GATE3825_6_Newton_local_GR_claim", "BLOCKED", "local GR/Newton still waits on filled boundary/MHref bundle plus compact exterior/PPN readout gates"),
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
            "decision_id": "DEC3825_0_boundary_zero_route_kept",
            "decision": "Keep the boundary primitive zero route, but only as a conditional theorem.",
            "rationale": "MAC545 gives a real mechanism, but current corpus has no parent-owned boundary action/reference lock.",
            "next_action": "fill or derive the boundary/MHref bundle before claims",
        },
        {
            "decision_id": "DEC3825_1_first_rows_installed",
            "decision": "Use the first source-ready rows as the next empirical plumbing target.",
            "rationale": "The blocker is now concrete fields with units, not an unnamed missing thing.",
            "next_action": "assemble compact-exterior kernel scorecard with these rows as inputs",
        },
        {
            "decision_id": "DEC3825_2_next_target",
            "decision": "Move to compact-exterior source-kernel closure scorecard.",
            "rationale": "We now have conditional routes and finite rows for PiM, R_eq, boundary, and MHref; the next step is an integrated kernel gate.",
            "next_action": "3826",
        },
    ]
    return [{**base_row(timestamp), **row} for row in rows]


def next_rows(timestamp: str) -> list[dict[str, str]]:
    return [
        {
            **base_row(timestamp),
            "target_doc": "3826-Y5-R2FR-compact-exterior-source-kernel-closure-scorecard.md",
            "target_script": "scripts/Y5_R2FR_3826_compact_exterior_source_kernel_closure_scorecard.py",
            "objective": "Integrate the PiM commutator, R_eq, boundary/reference, M_H_ref, stress-virial and local arena rows into one compact-exterior source-kernel closure scorecard.",
            "success_gate": "A single source-kernel scorecard shows which clauses are theorem-zero, source-row-ready, filled, or blocking for R10/WEP/PPN/clock/orbital/EM without opening claims.",
            "avoid": "do not claim Newton/local GR; do not use orbital GM as source mass; do not edit formalization-workbench; do not use GitHub",
        }
    ]


def status_rows(timestamp: str) -> list[dict[str, str]]:
    return [
        {
            **base_row(timestamp),
            "status": "PASS_NONCLAIM_BOUNDARY_REFERENCE_AND_MHREF_FIRST_ROWS_BUILT",
            "summary": "3825 derives conditional boundary/reference and positive-MHref zero routes, emits first source-ready finite rows for B_zero_flux/Delta_symp/MHref, and selects the compact-exterior source-kernel scorecard next.",
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
    text = f"""# 3825 - Boundary Reference Primitive And MHref Denominator Zero Or First Source Row

## Status

`PASS_NONCLAIM_BOUNDARY_REFERENCE_AND_MHREF_FIRST_ROWS_BUILT`

This checkpoint turns the last loose boundary/denominator obstruction into concrete zero routes plus first source-ready rows. `B_zero_flux` and `Delta_symp` vanish only under the minimal boundary/reference action clauses. `M_H_ref` is positive only through the active-energy/stress-virial route or a source-backed row. Nothing here opens a Newton/local-GR claim.

## Boundary Reference Zero Theorem

{md_table(grouped["boundary_theorem"], ["theorem_id", "status", "statement", "formula", "zero_condition"])}

## MHref Positive Denominator Law

{md_table(grouped["denominator"], ["law_id", "status", "statement", "formula", "required_evidence"])}

## First Source-Ready Rows

{md_table(grouped["first_rows"], ["row_id", "quantity", "formula", "units", "current_value", "source_ready_status"])}

## Boundary/MHref Arena Map

{md_table(grouped["arena_map"], ["map_id", "arena", "boundary_MHref_vector", "meaning"])}

## Residual Rows

{md_table(grouped["residuals"], ["residual_id", "symbol", "definition", "bound_formula", "current_status"])}

## Claim Gates

{md_table(grouped["gates"], ["gate_id", "gate_status", "claim_allowed", "detail"])}

## Next Target

`3826-Y5-R2FR-compact-exterior-source-kernel-closure-scorecard.md`

Target: integrate PiM, `R_eq`, boundary/reference, `M_H_ref`, stress-virial, and local arena rows into one compact-exterior source-kernel closure scorecard.

## Machine Outputs

{md_table(grouped["status"], ["status", "summary"])}
"""
    DOC_PATH.write_text(text, encoding="utf-8")


def update_spine() -> None:
    if not SPINE_PATH.exists():
        return
    text = read_text(SPINE_PATH)
    text = text.replace(
        "# Local GR Coupling Spine - Current State After 3824",
        "# Local GR Coupling Spine - Current State After 3825",
    )
    paragraph = (
        "`3825` converts the boundary/reference and denominator obstruction into concrete zero routes plus first source-ready rows: "
        "`B_zero_flux=0` needs a cohomologically trivial exact/improvement boundary form and no vector/tensor/source hair; `Delta_symp=0` needs a locked reference and fixed exterior symplectic/projector data; "
        "`M_H_ref>0` follows conditionally from the active-energy/stress-virial branch or from a filled same-frame `H_tau-H_ref` row. Current MTS has schema-ready rows, not claim-valid values, so the branch remains nonclaim.\n\n"
    )
    if "`3825` converts the boundary/reference and denominator obstruction" not in text:
        marker = "`3824` strengthens the topological-Hilbert equality route"
        index = text.find(marker)
        if index != -1:
            line_end = text.find("\n\n", index)
            if line_end != -1:
                text = text[: line_end + 2] + paragraph + text[line_end + 2 :]
    old_target = """`3825-Y5-R2FR-boundary-reference-primitive-and-MHref-denominator-zero-or-first-source-row.md`

Target: prove or bound `B_zero_flux`, `Delta_symp`, and positive `M_H_ref` using the minimal boundary/reference action contract, or emit first source-ready finite rows.

This is the best next move because 3824 makes `R_eq` conditionally zeroable; the equality route now bottlenecks on boundary/reference primitive terms and denominator normalization.
"""
    new_target = """`3826-Y5-R2FR-compact-exterior-source-kernel-closure-scorecard.md`

Target: integrate the PiM commutator, `R_eq`, boundary/reference, `M_H_ref`, stress-virial and local arena rows into one compact-exterior source-kernel closure scorecard.

This is the best next move because the individual source-kernel clauses now have zero routes or finite rows; the project needs one integrated gate to show exactly what remains before local Newton/GR testing.
"""
    text = text.replace(old_target, new_target)
    artifacts = [
        "source-intake\\mts_residuals\\P8_Y5_R2FR_3825_BOUNDARY_REFERENCE_ZERO_THEOREM.csv",
        "source-intake\\mts_residuals\\P8_Y5_R2FR_3825_MHREF_POSITIVE_DENOMINATOR_LAW.csv",
        "source-intake\\mts_residuals\\P8_Y5_R2FR_3825_FIRST_SOURCE_READY_BOUNDARY_MHREF_ROWS.csv",
        "source-intake\\mts_residuals\\P8_Y5_R2FR_3825_BOUNDARY_MHREF_ARENA_MAP.csv",
        "source-intake\\mts_residuals\\P8_Y5_R2FR_3825_BOUNDARY_MHREF_RESIDUAL_ROWS.csv",
        "source-intake\\mts_residuals\\P8_Y5_BRR545_3825_VALIDATION.csv",
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
    add("doc_written", DOC_PATH.exists() and "First Source-Ready Rows" in read_text(DOC_PATH), "3825 markdown document written")
    add("boundary_zero_theorem_written", any(row["theorem_id"] == "BRT3825_2_B_zero_flux_zero" for row in grouped["boundary_theorem"]), "B_zero conditional theorem emitted")
    add("delta_symp_theorem_written", any(row["theorem_id"] == "BRT3825_3_Delta_symp_zero" for row in grouped["boundary_theorem"]), "Delta_symp conditional theorem emitted")
    add("mhref_law_written", any(row["law_id"] == "MHD3825_2_positivity_condition" for row in grouped["denominator"]), "M_H_ref positivity law emitted")
    add("first_rows_nonclaim", all(row["valid_for_claim"] == "false" and row["claim_allowed"] == "false" for row in grouped["first_rows"]), "first source-ready rows remain nonclaim")
    add("first_rows_have_units", all(row.get("units") for row in grouped["first_rows"]), "first rows declare units")
    add("anti_circularity_guard", any(row["law_id"] == "MHD3825_3_anti_circularity" for row in grouped["denominator"]), "orbital GM anti-circularity guard retained")
    add("residual_total_row", any(row["symbol"] == "R_boundary_MHref_total" for row in grouped["residuals"]), "total boundary/MHref residual emitted")
    add("claim_gates_closed", all(row.get("claim_allowed") == "false" for row in grouped["gates"]), "no claim gate allows a claim")
    add("local_gr_blocked", any(row["gate_id"] == "GATE3825_6_Newton_local_GR_claim" and row["gate_status"] == "BLOCKED" for row in grouped["gates"]), "Newton/local GR claim remains blocked")
    add("next_target_selected", grouped["next"][0]["target_doc"].startswith("3826-Y5"), "3826 scorecard target selected")
    spine_text = read_text(SPINE_PATH) if SPINE_PATH.exists() else ""
    add("spine_updated", "Current State After 3825" in spine_text and "3826-Y5-R2FR-compact-exterior" in spine_text, "live spine updated to 3825 and 3826 target")
    fwb_hits = [path for path in FWB.rglob("*3825*") if path.is_file()] if FWB.exists() else []
    add("formalization_clean", len(fwb_hits) == 0, "no 3825 files written under formalization-workbench")
    add("pycache_removed", not (PCW / "scripts" / "__pycache__").exists(), "scripts __pycache__ removed")
    bad_chars = "\ufffd" in read_text(DOC_PATH) or "\ufffd" in read_text(Path(__file__)) or "\ufffd" in spine_text
    add("bad_chars_clean", not bad_chars, "new doc/script/spine contain no mojibake replacement characters")
    return rows


def main() -> None:
    timestamp = now_utc()
    grouped: dict[str, list[dict[str, str]]] = {}
    grouped["sources"] = source_rows(timestamp)
    grouped["boundary_theorem"] = boundary_theorem_rows(timestamp)
    grouped["denominator"] = denominator_rows(timestamp)
    grouped["first_rows"] = first_source_rows(timestamp)
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

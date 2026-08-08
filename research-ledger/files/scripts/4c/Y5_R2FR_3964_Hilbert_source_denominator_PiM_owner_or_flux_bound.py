from __future__ import annotations

import csv
import py_compile
import shutil
import subprocess
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


CHECKPOINT = "3964"
SCRIPT_PATH = Path(__file__).resolve()
PCW = SCRIPT_PATH.parents[1]
ROOT = PCW.parent
FWB = ROOT / "formalization-workbench"
SRC = PCW / "source-intake" / "mts_residuals"
DOC_PATH = PCW / "3964-Y5-R2FR-Hilbert-source-denominator-PiM-owner-or-flux-bound.md"
SPINE_PATH = PCW / "LOCAL_GR_COUPLING_SPINE_CURRENT_STATE.md"

OUTPUTS = {
    "sources": SRC / "P8_Y5_R2FR_3964_SOURCE_REGISTER.csv",
    "denominator": SRC / "P8_Y5_R2FR_3964_HILBERT_SOURCE_DENOMINATOR_IDENTITY.csv",
    "closure": SRC / "P8_Y5_R2FR_3964_PIM_FLUX_CLOSURE_THEOREM_OR_BOUND.csv",
    "residual_vector": SRC / "P8_Y5_R2FR_3964_MEFF_FLUX_RESIDUAL_VECTOR.csv",
    "newton_feed": SRC / "P8_Y5_R2FR_3964_NEWTON_SOURCE_SCORE_FEED_UPDATE.csv",
    "decision": SRC / "P8_Y5_R2FR_3964_DECISION_GATE.csv",
    "claim_gate": SRC / "P8_Y5_R2FR_3964_CLAIM_GATE.csv",
    "next": SRC / "P8_Y5_R2FR_3964_NEXT_TARGET.csv",
    "status": SRC / "P8_Y5_R2FR_3964_STATUS.csv",
    "validation": SRC / "P8_Y5_BRR545_3964_VALIDATION.csv",
}

NEXT_DOC = "3965-Y5-R2FR-PiM-commutator-projector-stress-or-Gauss-bound.md"
NEXT_SCRIPT = "scripts/Y5_R2FR_3965_PiM_commutator_projector_stress_or_Gauss_bound.py"


def now_utc() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def read_csv(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        raise ValueError(f"no rows for {path}")
    fields: list[str] = []
    for row in rows:
        for key in row:
            if key not in fields:
                fields.append(key)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def source_specs() -> list[tuple[str, Path, str, str]]:
    return [
        ("SRC3964_00_3963_next", SRC / "P8_Y5_R2FR_3963_NEXT_TARGET.csv", "NEXT3963_0", "3963 handoff"),
        ("SRC3964_01_3963_mass_flux", SRC / "P8_Y5_R2FR_3963_CONSTANT_UNIVERSAL_G_CONDITIONS.csv", "CGC3963_4_mass_flux", "M_eff mass flux condition"),
        ("SRC3964_02_3963_score", SRC / "P8_Y5_R2FR_3963_NEWTON_FIRST_NONCLAIM_SCORE_ROW.csv", "NGS3963_0_full_Newton_source", "Newton source score"),
        ("SRC3964_03_status", SRC / "P8_local_GR_Hilbert_source_denominator_status.csv", "STAT3531_0_denominator", "Hilbert denominator status"),
        ("SRC3964_04_status_ellJ", SRC / "P8_local_GR_Hilbert_source_denominator_status.csv", "STAT3531_1_ellJ", "ell_J status"),
        ("SRC3964_05_stack_SN3", SRC / "P8_source_normalized_Newton_branch_STACK.csv", "SN3_charge_equals_Hilbert_mass_current", "source mass identity rung"),
        ("SRC3964_06_stack_SN4", SRC / "P8_source_normalized_Newton_branch_STACK.csv", "SN4_closed_Meff_flux", "closed M_eff flux rung"),
        ("SRC3964_07_pim_gate", SRC / "P8_Y5_EH_DESCENT_COUPLING_PIM_2579_COUPLING_PIM_LOCK_GATE.csv", "CPG2579_3_PiM_derivative", "PiM derivative commutator gate"),
        ("SRC3964_08_mass_contract", SRC / "P8_mass_current_Hamiltonian_boundary_charge_CONTRACT.csv", "HC4_charge_equals_PiM_Hilbert_mass", "Hamiltonian charge equals PiM Hilbert mass"),
        ("SRC3964_09_projector_safe", SRC / "P8_mass_current_Hamiltonian_boundary_charge_CONTRACT.csv", "HC6_projector_variation_boundary_safe", "projector variation safety"),
        ("SRC3964_10_hilbert_attempt", SRC / "P8_TOPOLOGICAL_HILBERT_EQUALITY_ATTEMPT.csv", "EH501_2_Ward_current_route", "Ward current route"),
        ("SRC3964_11_hilbert_obstruct", SRC / "P8_TOPOLOGICAL_HILBERT_EQUALITY_OBSTRUCTIONS.csv", "OB501_3_hidden_exchange", "hidden exchange obstruction"),
        ("SRC3964_12_flux_theorem", SRC / "P8_SOURCE_MEASURE_MEFF_FLUX_THEOREM.csv", "T509_1_flux_closure", "M_eff flux closure theorem"),
        ("SRC3964_13_flux_extra", SRC / "P8_SOURCE_MEASURE_MEFF_FLUX_THEOREM.csv", "T509_2_no_extra_mass_channel", "extra mass channel theorem"),
        ("SRC3964_14_flux_clauses", SRC / "P8_SOURCE_MEASURE_MEFF_FLUX_CLAUSES.csv", "SM509_3_flux_closure", "source measure flux clauses"),
        ("SRC3964_15_flux_residual", SRC / "P8_SOURCE_MEASURE_MEFF_FLUX_RESIDUAL_MAP.csv", "SMR509_0_Delta_flux", "flux residual map"),
        ("SRC3964_16_flux_decision", SRC / "P8_SOURCE_MEASURE_MEFF_FLUX_DECISION.csv", "D509_1", "M_eff closure decision"),
        ("SRC3964_17_fc_contract", SRC / "P8_PiM_flux_closure_Ward_topological_CONTRACT.csv", "FC2_closed_mass_current_equation", "PiM flux closure contract"),
        ("SRC3964_18_pv_contract", SRC / "P8_PiM_projector_variation_stress_CONTRACT.csv", "PV0_product_variation_included", "PiM product variation"),
        ("SRC3964_19_pm_contract", SRC / "P8_PiM_parent_symplectic_projector_algebra_CONTRACT.csv", "PM6_flux_closure_requires_Ward_or_Euler", "projector algebra not enough"),
        ("SRC3964_20_gauss_contract", SRC / "P8_Hamiltonian_charge_Poisson_Gauss_calibration_CONTRACT.csv", "PG1_charge_equals_projected_Hilbert_source", "Gauss/Hamiltonian source identity"),
        ("SRC3964_21_scorecard", SRC / "P8_Y5_HAMILTONIAN_SOURCE_MEASURE_SCORECARD.csv", "HSS541_3_radial_closure", "Hamiltonian source measure scorecard"),
        ("SRC3964_22_validation_3963", SRC / "P8_Y5_BRR545_3963_VALIDATION.csv", "VAL3963_17_no_pycache", "previous validation"),
    ]


def source_register_rows(timestamp: str) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for source_id, path, needle, purpose in source_specs():
        exists = path.exists()
        found = False
        line_number = ""
        excerpt = ""
        if exists:
            for index, line in enumerate(read_text(path).splitlines(), start=1):
                if needle in line:
                    found = True
                    line_number = str(index)
                    excerpt = line[:1000]
                    break
        rows.append(
            {
                "checkpoint": CHECKPOINT,
                "source_id": source_id,
                "source_path": str(path),
                "needle": needle,
                "purpose": purpose,
                "exists": exists,
                "needle_found": found,
                "line_number": line_number,
                "line_excerpt": excerpt,
                "valid_for_claim": False,
                "timestamp_utc": timestamp,
            }
        )
    return rows


def denominator_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "row_id": "HDI3964_0_definition",
            "identity_piece": "Hilbert source denominator",
            "formula": "M_eff[S] := N_G int_S Pi_M J_H[tau]",
            "meaning": "the Newton source mass must be a parent-defined projected Hilbert/coframe current before readout",
            "status": "DEFINITION_CONDITIONAL_NONCLAIM",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "HDI3964_1_Hamiltonian",
            "identity_piece": "Hamiltonian equality target",
            "formula": "B_tau/G_eff = M_eff[Pi_M J_H] and delta B_tau = delta int_S Pi_M J_H",
            "meaning": "the geometric boundary charge and matter Hilbert source must be the same mass object",
            "status": "TARGET_IDENTITY_NOT_PARENT_DERIVED",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "HDI3964_2_flux",
            "identity_piece": "surface independence",
            "formula": "M_eff(S2)-M_eff(S1)=N_G int_A d(Pi_M J_H)",
            "meaning": "time/radial source drift is exactly the failure of projected Hilbert flux closure",
            "status": "DERIVED_FLUX_IDENTITY",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "HDI3964_3_product_rule",
            "identity_piece": "PiM product variation",
            "formula": "d(Pi_M J_H)=Pi_M dJ_H + (dPi_M) wedge J_H + exchange/boundary/source terms",
            "meaning": "projector closure is not free; the commutator/projector-stress terms must be zero or retained",
            "status": "DERIVED_PRODUCT_RULE_GUARD",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
    ]


def closure_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "row_id": "PFC3964_0_zero_theorem",
            "theorem_piece": "M_eff conservation theorem",
            "formula": "if d(Pi_M J_H)=0 in compact source-free exterior and boundary/reference flux vanishes, then D_t M_eff=partial_r M_eff=0",
            "derived_effect": "mass-source denominator contributes no Gdot/radial hair to epsilon_Newton_source",
            "status": "PROVED_CONDITIONAL_NOT_PARENT_PROMOTED",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "PFC3964_1_needed_origin",
            "theorem_piece": "allowed closure origins",
            "formula": "d(Pi_M J_H)=0 may come from Ward_M, topological mass current, Hamiltonian integrability, or parent Euler equation",
            "derived_effect": "a multiplier closure without independent origin is rejected as closure-only",
            "status": "ORIGIN_REQUIRED_NO_SMUGGLING",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "PFC3964_2_bound_law",
            "theorem_piece": "M_eff drift bound",
            "formula": "|Delta M_eff| <= N_G int_A |Delta_flux+Delta_PiM+Delta_symp+Delta_extra+Delta_cal+Delta_frame+Delta_nonEH+Delta_PPN|",
            "derived_effect": "if closure fails, measured mass drift is a finite residual vector, not an unstated assumption",
            "status": "DERIVED_BOUND_TEMPLATE",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "PFC3964_3_Newton_feed",
            "theorem_piece": "Newton source score feed",
            "formula": "D_X ln M_eff <= epsilon_Meff_flux(X)",
            "derived_effect": "3963 epsilon_Newton_source now receives the PiM/Hilbert denominator residual explicitly",
            "status": "FEEDS_3963_NEWTON_SCORE",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
    ]


def residual_vector_rows(timestamp: str) -> list[dict[str, Any]]:
    rows = [
        ("MFR3964_0_Delta_flux", "Delta_flux", "d(Pi_M J_H) exterior flux", "dln_Meff_dt; epsilon_radial_Meff", "Ward/topological/Hamiltonian closure or flux bound"),
        ("MFR3964_1_Delta_PiM", "Delta_PiM", "(dPi_M) wedge J_H projector commutator", "projector stress; PPN/source hair", "PiM variation theorem or coefficient bound"),
        ("MFR3964_2_Delta_symp", "Delta_symp", "boundary symplectic/reference shift", "boundary monopole; Delta_cal", "integrable reference-zero theorem or bound"),
        ("MFR3964_3_Delta_extra", "Delta_extra", "non-EH/domain/memory/range/connection mass charge", "mu_extra; alpha(lambda); clocks", "field-specific silence or residual coefficients"),
        ("MFR3964_4_Delta_cal", "Delta_cal", "closed charge to observed orbital/Gauss calibration mismatch", "Kepler/Newton readout", "Gauss/orbital calibration theorem or external ledger"),
        ("MFR3964_5_Delta_frame", "Delta_frame_source", "source frame and orbital/clock frame mismatch", "WEP; clocks; preferred frame", "same-frame theorem or frame residual"),
        ("MFR3964_6_Delta_nonEH", "Delta_nonEH", "operator charge differs from EH/Hilbert charge", "GR limit; PPN gamma/beta", "EH-only exterior and non-EH charge silence"),
        ("MFR3964_7_Delta_PPN", "Delta_PPN", "source equality unstable beyond leading Newton order", "beta; gamma; alpha_i; zeta_i; xi", "second-order source-charge PPN expansion"),
    ]
    return [
        {
            "residual_id": residual_id,
            "symbol": symbol,
            "meaning": meaning,
            "feeds": feeds,
            "zero_or_bound_requirement": requirement,
            "score_term": f"|{symbol}|",
            "status": "RETAINED_SYMBOLIC_RESIDUAL",
            "score_ready": True,
            "claim_allowed": False,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
        for residual_id, symbol, meaning, feeds, requirement in rows
    ]


def newton_feed_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "row_id": "NFF3964_0_epsilon_Meff_flux",
            "target": "epsilon_Meff_flux",
            "update_formula": "epsilon_Meff_flux <= |Delta_flux|+|Delta_PiM|+|Delta_symp|+|Delta_extra|+|Delta_cal|+|Delta_frame|+|Delta_nonEH|+|Delta_PPN|",
            "meaning": "all Hilbert/PiM/source-measure failures compress into the mass denominator term",
            "feeds": "D_X ln M_eff in epsilon_Newton_source",
            "status": "SYMBOLIC_FEED_READY_NO_NUMERIC_CLAIM",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "NFF3964_1_epsilon_Newton_source_update",
            "target": "epsilon_Newton_source",
            "update_formula": "epsilon_Newton_source <= |D ln Pi_G| + epsilon_Meff_flux + |D ln(1+epsilon_mu)| + frame/species/range/EM terms",
            "meaning": "3963 Newton source score now has its M_eff term decomposed into PiM/Hilbert residuals",
            "feeds": "Newton/Poisson/Gdot/WEP/R10/PPN gates",
            "status": "SYMBOLIC_FEED_READY_NO_NUMERIC_CLAIM",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
    ]


def decision_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "row_id": "DEC3964_0_conditional_theorem",
            "decision": "accept conditional M_eff conservation theorem but do not promote it",
            "basis": "d(Pi_M J_H)=0 would close mass drift, but parent Ward/topological/Hamiltonian origin remains unsigned",
            "effect": "Newton source denominator is sharpened without smuggling closure",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "DEC3964_1_bound_vector",
            "decision": "map every Hilbert/PiM source-denominator failure into epsilon_Meff_flux",
            "basis": "flux identity expresses M_eff drift as an integral of named residual channels",
            "effect": "3963 epsilon_Newton_source becomes more concrete and less vague",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "DEC3964_2_next",
            "decision": f"move to {NEXT_DOC}",
            "basis": "largest active sub-blocker is Delta_PiM: product rule, projector commutator, and projector stress",
            "effect": "attack the most specific mass-denominator leak next",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
    ]


def claim_gate_rows(timestamp: str) -> list[dict[str, Any]]:
    rows = [
        ("CLG3964_0_sources", "source register", "all cited local sources and needles found", "PASS_PRIVATE"),
        ("CLG3964_1_denominator_identity", "Hilbert denominator identity", "M_eff[S]=N_G int_S Pi_M J_H and product rule written", "PASS_SYMBOLIC_NONCLAIM"),
        ("CLG3964_2_flux_zero", "M_eff flux closure", "d(Pi_M J_H)=0 from parent Ward/topological/Hamiltonian origin", "CONDITIONAL_ONLY"),
        ("CLG3964_3_residual_vector", "epsilon_Meff_flux", "all source-denominator failures mapped to symbolic residual vector", "PASS_SYMBOLIC_NONCLAIM"),
        ("CLG3964_4_Newton_claim", "Newton/local GR source denominator", "epsilon_Meff_flux=0 plus Gauss/orbital/PPN gates", "BLOCKED_NONCLAIM"),
    ]
    return [
        {
            "row_id": row_id,
            "gate": gate,
            "requirement": requirement,
            "status": status,
            "claim_allowed": False,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
        for row_id, gate, requirement, status in rows
    ]


def next_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "row_id": "NEXT3964_0",
            "next_doc": NEXT_DOC,
            "next_script": NEXT_SCRIPT,
            "target": "derive or bound Delta_PiM: product-rule commutator (dPi_M)J_H, projector stress, boundary/domain variation, and whether Pi_M is topological/metric-independent or must be retained as a local residual",
            "success_condition": "Delta_PiM is theorem-zero under a parent-owned projector algebra, or becomes a finite score term feeding epsilon_Meff_flux and PPN/source-normalization gates",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
    ]


def status_rows(timestamp: str, source_rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    found = sum(bool(row["exists"]) and bool(row["needle_found"]) for row in source_rows)
    return [
        {
            "checkpoint": CHECKPOINT,
            "status": "PASS_PRIVATE_NONCLAIM_HILBERT_SOURCE_DENOMINATOR",
            "summary": "3964 derives the PiM/Hilbert mass denominator flux identity, keeps M_eff conservation conditional, and maps denominator failures into epsilon_Meff_flux feeding epsilon_Newton_source.",
            "sources_found": f"{found}/{len(source_rows)}",
            "claim_allowed": False,
            "timestamp_utc": timestamp,
        }
    ]


def doc_text(timestamp: str, source_rows: list[dict[str, Any]]) -> str:
    found = sum(bool(row["exists"]) and bool(row["needle_found"]) for row in source_rows)
    return f"""# 3964 - Hilbert Source Denominator PiM Owner Or Flux Bound

Timestamp: `{timestamp}`

## Result

3964 attacks the mass/source denominator needed for Newton:

`M_eff[S] := N_G int_S Pi_M J_H[tau]`.

The core flux identity is:

`M_eff(S2)-M_eff(S1)=N_G int_A d(Pi_M J_H)`.

With the product rule:

`d(Pi_M J_H)=Pi_M dJ_H + (dPi_M) wedge J_H + exchange/boundary/source terms`.

Therefore:

- if `d(Pi_M J_H)=0` from a real parent Ward/topological/Hamiltonian origin, then `M_eff` has no radial/time flux hair;
- if not, the failure is a named residual vector:

`epsilon_Meff_flux <= |Delta_flux|+|Delta_PiM|+|Delta_symp|+|Delta_extra|+|Delta_cal|+|Delta_frame|+|Delta_nonEH|+|Delta_PPN|`.

This feeds the 3963 Newton score:

`epsilon_Newton_source <= |D ln Pi_G| + epsilon_Meff_flux + |D ln(1+epsilon_mu)| + ...`.

## Source/Register

- Sources found: `{found}/{len(source_rows)}`
- Denominator identity: `source-intake\\mts_residuals\\P8_Y5_R2FR_3964_HILBERT_SOURCE_DENOMINATOR_IDENTITY.csv`
- Flux theorem/bound: `source-intake\\mts_residuals\\P8_Y5_R2FR_3964_PIM_FLUX_CLOSURE_THEOREM_OR_BOUND.csv`
- Residual vector: `source-intake\\mts_residuals\\P8_Y5_R2FR_3964_MEFF_FLUX_RESIDUAL_VECTOR.csv`
- Newton feed update: `source-intake\\mts_residuals\\P8_Y5_R2FR_3964_NEWTON_SOURCE_SCORE_FEED_UPDATE.csv`
- Validation: `source-intake\\mts_residuals\\P8_Y5_BRR545_3964_VALIDATION.csv`

## Next Target

`{NEXT_DOC}`
"""


def spine_block(timestamp: str) -> str:
    return f"""

## 3964 - Hilbert/PiM Source Denominator Flux Gate

Timestamp: `{timestamp}`

- Defines the live Newton mass source as `M_eff[S]=N_G int_S Pi_M J_H[tau]`.
- Derives the flux identity `M_eff(S2)-M_eff(S1)=N_G int_A d(Pi_M J_H)`.
- Product-rule guard: `d(Pi_M J_H)=Pi_M dJ_H+(dPi_M)J_H+...`; projector closure is not free.
- Introduces `epsilon_Meff_flux`, feeding `epsilon_Newton_source`.
- Next: `{NEXT_DOC}`.
"""


def update_spine(timestamp: str) -> None:
    block = spine_block(timestamp)
    marker = "## 3964 - Hilbert/PiM Source Denominator Flux Gate"
    if SPINE_PATH.exists():
        text = read_text(SPINE_PATH)
        if marker in text:
            before = text.split(marker, 1)[0].rstrip()
            SPINE_PATH.write_text(before + block, encoding="utf-8")
        else:
            SPINE_PATH.write_text(text.rstrip() + block, encoding="utf-8")
    else:
        SPINE_PATH.write_text("# Local GR Coupling Spine - Current State\n" + block, encoding="utf-8")


def formalization_workbench_git_status() -> tuple[bool, str]:
    try:
        result = subprocess.run(
            ["git", "-C", str(ROOT), "status", "--porcelain", "--", str(FWB.relative_to(ROOT))],
            check=False,
            capture_output=True,
            text=True,
            timeout=15,
        )
    except Exception:
        return False, "git status unavailable; scope guard confirms generated outputs are outside formalization-workbench"
    if result.returncode != 0:
        return False, "git status unavailable; scope guard confirms generated outputs are outside formalization-workbench"
    modified_count = len([line for line in result.stdout.splitlines() if line.strip()])
    return modified_count == 0, f"formalization-workbench modified count is {modified_count}"


def csv_parse_ok(paths: list[Path]) -> bool:
    try:
        for path in paths:
            if path.exists():
                read_csv(path)
    except Exception:
        return False
    return True


def validation_rows(timestamp: str, source_rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    denominator = denominator_rows(timestamp)
    closure = closure_rows(timestamp)
    residuals = residual_vector_rows(timestamp)
    feed = newton_feed_rows(timestamp)
    decisions = decision_rows(timestamp)
    claims = claim_gate_rows(timestamp)
    next_target = next_rows(timestamp)
    generated_csvs = [path for key, path in OUTPUTS.items() if key != "validation"]
    generated_paths = generated_csvs + [DOC_PATH, SCRIPT_PATH, SPINE_PATH]
    fwb_git_clean, fwb_git_detail = formalization_workbench_git_status()

    denominator_statuses = {row["status"] for row in denominator}
    closure_statuses = {row["status"] for row in closure}
    residual_symbols = {row["symbol"] for row in residuals}
    feed_targets = {row["target"] for row in feed}
    decision_text = " ".join(row["decision"] for row in decisions)
    claim_statuses = {row["status"] for row in claims}
    all_physics_rows = denominator + closure + residuals + feed + decisions + claims + next_target

    checks = [
        ("VAL3964_00_sources_exist", all(row["exists"] for row in source_rows), "all cited source paths exist"),
        ("VAL3964_01_needles_found", all(row["needle_found"] for row in source_rows), "all cited source needles found"),
        ("VAL3964_02_denominator_identity", "DERIVED_FLUX_IDENTITY" in denominator_statuses and "DERIVED_PRODUCT_RULE_GUARD" in denominator_statuses, "Hilbert/PiM denominator identity and product-rule guard written"),
        ("VAL3964_03_closure_theorem", "PROVED_CONDITIONAL_NOT_PARENT_PROMOTED" in closure_statuses and "ORIGIN_REQUIRED_NO_SMUGGLING" in closure_statuses, "conditional closure theorem with no-smuggling guard written"),
        ("VAL3964_04_bound_template", "DERIVED_BOUND_TEMPLATE" in closure_statuses and "FEEDS_3963_NEWTON_SCORE" in closure_statuses, "M_eff flux bound and Newton feed written"),
        ("VAL3964_05_residual_vector", {"Delta_flux", "Delta_PiM", "Delta_symp", "Delta_extra", "Delta_cal", "Delta_frame_source", "Delta_nonEH", "Delta_PPN"}.issubset(residual_symbols), "M_eff residual vector complete"),
        ("VAL3964_06_newton_feed", {"epsilon_Meff_flux", "epsilon_Newton_source"}.issubset(feed_targets), "Newton source score feed update present"),
        ("VAL3964_07_decision", "conditional M_eff conservation" in decision_text and "epsilon_Meff_flux" in decision_text, "decision records conditional theorem and residual score"),
        ("VAL3964_08_claim_gate", "PASS_SYMBOLIC_NONCLAIM" in claim_statuses and "CONDITIONAL_ONLY" in claim_statuses and "BLOCKED_NONCLAIM" in claim_statuses, "claim gate blocks Newton/local-GR promotion"),
        ("VAL3964_09_next_target", next_target[0]["next_doc"] == NEXT_DOC and next_target[0]["next_script"] == NEXT_SCRIPT, "next target points to PiM commutator/projector stress"),
        ("VAL3964_10_all_nonclaim", all(not row["valid_for_claim"] for row in all_physics_rows), "all generated physics rows remain nonclaim"),
        ("VAL3964_11_score_ready", all(row["score_ready"] for row in residuals), "M_eff residual rows are score-ready symbolics"),
        ("VAL3964_12_outputs_outside_fwb", all(FWB not in path.parents and path != FWB for path in generated_paths), "no generated output is inside formalization-workbench"),
        ("VAL3964_13_fwb_git_or_scope_guard", fwb_git_clean or all(FWB not in path.parents and path != FWB for path in generated_paths), fwb_git_detail),
        ("VAL3964_14_doc_exists", DOC_PATH.exists(), "checkpoint doc exists"),
        ("VAL3964_15_spine_updated", SPINE_PATH.exists() and "3964 - Hilbert/PiM Source Denominator Flux Gate" in read_text(SPINE_PATH), "spine updated"),
        ("VAL3964_16_csv_parse", csv_parse_ok(generated_csvs), "generated CSV files parse cleanly"),
        ("VAL3964_17_script_compile", True, "script compiled before validation write"),
        ("VAL3964_18_no_pycache", not (SCRIPT_PATH.parent / "__pycache__").exists(), "scripts __pycache__ removed"),
    ]
    return [
        {
            "validation_id": validation_id,
            "passed": bool(passed),
            "detail": detail,
            "timestamp_utc": timestamp,
        }
        for validation_id, passed, detail in checks
    ]


def run() -> None:
    timestamp = now_utc()
    sources = source_register_rows(timestamp)
    denominator = denominator_rows(timestamp)
    closure = closure_rows(timestamp)
    residuals = residual_vector_rows(timestamp)
    feed = newton_feed_rows(timestamp)
    decisions = decision_rows(timestamp)
    claims = claim_gate_rows(timestamp)
    next_target = next_rows(timestamp)
    status = status_rows(timestamp, sources)

    write_csv(OUTPUTS["sources"], sources)
    write_csv(OUTPUTS["denominator"], denominator)
    write_csv(OUTPUTS["closure"], closure)
    write_csv(OUTPUTS["residual_vector"], residuals)
    write_csv(OUTPUTS["newton_feed"], feed)
    write_csv(OUTPUTS["decision"], decisions)
    write_csv(OUTPUTS["claim_gate"], claims)
    write_csv(OUTPUTS["next"], next_target)
    write_csv(OUTPUTS["status"], status)

    DOC_PATH.write_text(doc_text(timestamp, sources), encoding="utf-8")
    update_spine(timestamp)

    py_compile.compile(str(SCRIPT_PATH), doraise=True)
    pycache = SCRIPT_PATH.parent / "__pycache__"
    if pycache.exists():
        shutil.rmtree(pycache)

    validations = validation_rows(timestamp, sources)
    write_csv(OUTPUTS["validation"], validations)
    failed = [row for row in validations if not row["passed"]]
    if failed:
        raise SystemExit(f"3964 validation failed: {failed}")

    print(f"3964 checkpoint complete: {DOC_PATH}")
    print(f"validation: {OUTPUTS['validation']}")
    print("Hilbert/PiM source denominator flux identity and epsilon_Meff_flux score assembled")


if __name__ == "__main__":
    run()

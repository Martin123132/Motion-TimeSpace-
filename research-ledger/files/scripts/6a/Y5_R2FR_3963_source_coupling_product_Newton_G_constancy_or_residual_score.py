from __future__ import annotations

import csv
import py_compile
import shutil
import subprocess
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


CHECKPOINT = "3963"
SCRIPT_PATH = Path(__file__).resolve()
PCW = SCRIPT_PATH.parents[1]
ROOT = PCW.parent
FWB = ROOT / "formalization-workbench"
SRC = PCW / "source-intake" / "mts_residuals"
DOC_PATH = PCW / "3963-Y5-R2FR-source-coupling-product-Newton-G-constancy-or-residual-score.md"
SPINE_PATH = PCW / "LOCAL_GR_COUPLING_SPINE_CURRENT_STATE.md"

OUTPUTS = {
    "sources": SRC / "P8_Y5_R2FR_3963_SOURCE_REGISTER.csv",
    "identity": SRC / "P8_Y5_R2FR_3963_NEWTON_G_PRODUCT_IDENTITY.csv",
    "conditions": SRC / "P8_Y5_R2FR_3963_CONSTANT_UNIVERSAL_G_CONDITIONS.csv",
    "vector": SRC / "P8_Y5_R2FR_3963_NEWTON_SOURCE_RESIDUAL_VECTOR.csv",
    "score": SRC / "P8_Y5_R2FR_3963_NEWTON_FIRST_NONCLAIM_SCORE_ROW.csv",
    "decision": SRC / "P8_Y5_R2FR_3963_DECISION_GATE.csv",
    "claim_gate": SRC / "P8_Y5_R2FR_3963_CLAIM_GATE.csv",
    "next": SRC / "P8_Y5_R2FR_3963_NEXT_TARGET.csv",
    "status": SRC / "P8_Y5_R2FR_3963_STATUS.csv",
    "validation": SRC / "P8_Y5_BRR545_3963_VALIDATION.csv",
}

NEXT_DOC = "3964-Y5-R2FR-Hilbert-source-denominator-PiM-owner-or-flux-bound.md"
NEXT_SCRIPT = "scripts/Y5_R2FR_3964_Hilbert_source_denominator_PiM_owner_or_flux_bound.py"


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
        ("SRC3963_00_3962_next", SRC / "P8_Y5_R2FR_3962_NEXT_TARGET.csv", "NEXT3962_0", "3962 handoff"),
        ("SRC3963_01_3954_newton", SRC / "P8_Y5_R2FR_3954_Z_SOURCE_CURRENT_THEOREM.csv", "SCT3954_4_Newton_calibration", "Newton calibration law"),
        ("SRC3963_02_3954_G", SRC / "P8_Y5_R2FR_3954_Z_SOURCE_CURRENT_THEOREM.csv", "SCT3954_5_GR_Newton_constant_status", "Newton G status"),
        ("SRC3963_03_3954_product", SRC / "P8_Y5_R2FR_3954_PPN_SOURCE_NORMALIZATION_RESIDUAL_MAP.csv", "PPN3954_7_Geff_product", "G_eff product drift"),
        ("SRC3963_04_3959_G", SRC / "P8_Y5_R2FR_3959_CA_TOTAL_CURRENT_BOUND_LAW.csv", "CAB3959_6_Newton_G_constant", "Newton G product row"),
        ("SRC3963_05_local_status", SRC / "P8_local_GR_kappa_G_Newtonian_gate_status.csv", "STAT3530_1_product", "kappa/G product lock"),
        ("SRC3963_06_kappa_contract", SRC / "P8_constant_universal_Geff_kappa_CONTRACT.csv", "CU1_global_coupling_status", "global coupling status"),
        ("SRC3963_07_kappa_species", SRC / "P8_constant_universal_Geff_kappa_CONTRACT.csv", "CU3_species_source_blindness", "species/source blindness"),
        ("SRC3963_08_kappa_residual", SRC / "P8_CONSTANT_KAPPA_RESIDUAL_MAP.csv", "KR508_0_time_drift", "kappa residual map"),
        ("SRC3963_09_superselection", SRC / "P8_CONSTANT_KAPPA_SUPERSELECTION_THEOREM.csv", "T508_1_topological_zeroform", "topological zeroform kappa theorem"),
        ("SRC3963_10_GM_attempt", SRC / "P8_CONSTANT_GM_ZERO_THEOREM_ATTEMPT.csv", "Z0_decomposition_identity", "measured GM identity"),
        ("SRC3963_11_GM_missing", SRC / "P8_CONSTANT_GM_ZERO_THEOREM_ATTEMPT.csv", "Z3_mu_extra_zero_or_universal_constant", "epsilon_mu missing"),
        ("SRC3963_12_GM_matrix", SRC / "P8_CONSTANT_GM_RESIDUAL_BOUND_MATRIX.csv", "P8_Geff_time_drift", "Gdot bound matrix"),
        ("SRC3963_13_R11_min", SRC / "P8_R11_SOURCE_NORMALIZATION_OPERATOR_MINIMUM_FILL.csv", "R11SN_6_time_drift", "source normalization minimum fill"),
        ("SRC3963_14_R11_decision", SRC / "P8_R11_SOURCE_NORMALIZATION_DECISION.csv", "D2_Newton_gate", "Newton gate blocked"),
        ("SRC3963_15_stack", SRC / "P8_source_normalized_Newton_branch_STACK.csv", "SN7_constant_universal_Geff", "Newton branch stack"),
        ("SRC3963_16_hilbert_status", SRC / "P8_local_GR_Hilbert_source_denominator_status.csv", "STAT3531_1_ellJ", "ell_J residual decomposition"),
        ("SRC3963_17_EM_score", SRC / "P8_Y5_R2FR_3962_EM_FIRST_NONCLAIM_SCORE_ROW.csv", "EMS3962_0_full_vector", "EM score feed"),
        ("SRC3963_18_validation_3962", SRC / "P8_Y5_BRR545_3962_VALIDATION.csv", "VAL3962_18_no_pycache", "previous validation"),
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


def identity_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "row_id": "NGI3963_0_product",
            "identity_piece": "source-coupling product",
            "formula": "Pi_G := G_ref w_common ell_J R_frame, with G_eff proportional to Pi_G^(-1)",
            "meaning": "the local Newton coupling is a product of EH normalization, common matter action weight, source-current scale, and frame/readout factor",
            "status": "BOOKKEEPING_IDENTITY_CURRENT_NONCLAIM",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "NGI3963_1_measured_mu",
            "identity_piece": "measured source strength",
            "formula": "mu_obs := G_eff M_eff (1+epsilon_mu)",
            "meaning": "observed GM can be constant even while hidden pieces drift; no tuned cancellation is accepted as derivation",
            "status": "DECOMPOSITION_IDENTITY",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "NGI3963_2_log_derivative",
            "identity_piece": "constancy derivative",
            "formula": "D_X ln mu_obs = -D_X ln Pi_G + D_X ln M_eff + D_X ln(1+epsilon_mu)",
            "meaning": "Newtonian constancy requires each term theorem-zero or bounded without hidden cancellation",
            "status": "DERIVED_RESIDUAL_LAW",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "NGI3963_3_absolute_G",
            "identity_piece": "absolute G status",
            "formula": "G_N numerical value = calibration/global parent scale unless kappa_MTS is parent-owned",
            "meaning": "the serious derivable target is constancy/universality, not pretending the numerical SI value follows without a parent scale",
            "status": "NO_ABSOLUTE_G_CLAIM",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
    ]


def condition_rows(timestamp: str) -> list[dict[str, Any]]:
    rows = [
        ("CGC3963_0_global", "global/superselection coupling", "D_X ln G_ref = 0", "time/radial/range drift from base EH coupling", "CONDITIONAL_ZERO_ROUTE"),
        ("CGC3963_1_common_weight", "common matter density-line weight", "D_X ln w_common = 0 or common constant calibration", "species/source-weight drift", "CONDITIONAL_ZERO_ROUTE"),
        ("CGC3963_2_ellJ", "source-current scale ell_J", "D_X ln ell_J = 0 before readout/tests", "source-current normalization drift", "OPEN_OWNER_ROUTE"),
        ("CGC3963_3_frame", "same observed source/readout frame", "D_X ln R_frame = 0 and delta_frame_source=0", "frame/source calibration split", "OPEN_OWNER_ROUTE"),
        ("CGC3963_4_mass_flux", "conserved Hilbert source mass", "D_X ln M_eff = 0 via Pi_M J_H closure", "mass flux/time/radial hair", "NEXT_TARGET"),
        ("CGC3963_5_epsilon_mu", "extra source normalization", "D_X ln(1+epsilon_mu)=0 or epsilon_mu=constant universal calibration", "boundary/bulk/domain/memory/projector source hair", "OPEN_VECTOR_ROUTE"),
        ("CGC3963_6_no_cancellation", "no tuned cancellation", "each derivative component zero/bounded separately", "post-hoc fit hiding drift", "POLICY_REQUIRED"),
    ]
    return [
        {
            "condition_id": condition_id,
            "condition": condition,
            "math_requirement": requirement,
            "blocks_if_missing": blocks,
            "status": status,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
        for condition_id, condition, requirement, blocks, status in rows
    ]


def vector_rows(timestamp: str) -> list[dict[str, Any]]:
    rows = [
        ("NSV3963_0_time", "dln_mu_obs_dt", "|-dlnPi_G_dt + dlnM_eff_dt + dln(1+epsilon_mu)_dt|", "Gdot/G", "bound target from prior matrix: 9.6e-15 yr^-1 or theorem-zero"),
        ("NSV3963_1_radial", "partial_r_ln_mu_obs", "|-partial_r lnPi_G + partial_r lnM_eff + partial_r ln(1+epsilon_mu)|", "Newton inverse-square/R10 radial hair", "zero radial hair or mapped profile bound"),
        ("NSV3963_2_range", "alpha_mu(lambda)", "|alpha_kappa(lambda)+alpha_M(lambda)+alpha_epsilon(lambda)|", "R10 fifth force", "alpha(lambda) curve or theorem-zero"),
        ("NSV3963_3_species", "eta_source_AB", "|Delta_AB lnPi_G| + |Delta_AB lnM_eff| + |Delta_AB ln(1+epsilon_mu)|", "WEP source charge", "source-label blindness or WEP bound"),
        ("NSV3963_4_frame", "delta_frame_source", "|Delta_frame ln Pi_G| + |Delta_frame lnM_eff| + |Delta_frame epsilon_mu|", "clock/WEP/local frame split", "same-frame theorem or bound"),
        ("NSV3963_5_mu_extra", "epsilon_mu_vector", "sum |epsilon_boundary, epsilon_domain, epsilon_bulk_X, epsilon_nonEH, epsilon_species, epsilon_time|", "Newton/PPN/R11 source normalization", "row-wise theorem-zero or numeric bound"),
        ("NSV3963_6_EM_feed", "epsilon_EM_residual", "K_EMsource epsilon_EM_residual", "EM alpha/clocks/source leakage", "feeds from 3962 symbolic score"),
    ]
    return [
        {
            "component_id": component_id,
            "symbol": symbol,
            "score_term": score_term,
            "observable_links": links,
            "required_evidence": evidence,
            "status": "SYMBOLIC_RESIDUAL_NOT_NUMERIC",
            "score_ready": True,
            "claim_allowed": False,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
        for component_id, symbol, score_term, links, evidence in rows
    ]


def score_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "score_id": "NGS3963_0_full_Newton_source",
            "score_name": "epsilon_Newton_source",
            "formula": "epsilon_Newton_source <= |D ln Pi_G| + |D ln M_eff| + |D ln(1+epsilon_mu)| + |delta_frame_source| + |eta_source_AB| + |alpha_mu(lambda)| + K_EMsource epsilon_EM_residual",
            "zero_condition": "Pi_G parent-constant, M_eff conserved, epsilon_mu constant/universal or zero, same-frame readout, source-label blindness, range/radial silence, and EM score zero",
            "current_status": "FIRST_NONCLAIM_SYMBOLIC_SCORE_ROW",
            "score_ready": True,
            "claim_allowed": False,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "score_id": "NGS3963_1_Newtonian_limit",
            "score_name": "Delta_Newton_source_side",
            "formula": "nabla^2 Phi = 4 pi G0 rho_H + R_Newton_source, with |R_Newton_source| <= K_N epsilon_Newton_source",
            "zero_condition": "epsilon_Newton_source=0 and EH/Poisson operator/readout gates close",
            "current_status": "POISSON_SOURCE_SIDE_SCORE_TEMPLATE",
            "score_ready": True,
            "claim_allowed": False,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
    ]


def decision_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "row_id": "DEC3963_0_no_absolute_G_claim",
            "decision": "do not claim an absolute numerical derivation of G_N",
            "basis": "existing gates treat kappa/G as calibrated/global unless parent scale kappa_MTS is supplied",
            "effect": "keeps the framework aligned with GR-style coupling calibration instead of fake numerology",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "DEC3963_1_constancy_target",
            "decision": "make constancy/universality of the source-coupling product the live derivation target",
            "basis": "D_X ln mu_obs decomposes into Pi_G, M_eff, and epsilon_mu terms",
            "effect": "Newtonian recovery becomes a no-hidden-drift theorem or residual score",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "DEC3963_2_next",
            "decision": f"move to {NEXT_DOC}",
            "basis": "the biggest non-symbolic blocker is M_eff/Pi_M/Hilbert source denominator ownership",
            "effect": "attack the mass/source denominator needed for Poisson/Newton rather than circling constants",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
    ]


def claim_gate_rows(timestamp: str) -> list[dict[str, Any]]:
    rows = [
        ("CLG3963_0_sources", "source register", "all cited local sources and needles found", "PASS_PRIVATE"),
        ("CLG3963_1_product_identity", "Newton product identity", "Pi_G and mu_obs decomposition written", "PASS_SYMBOLIC_NONCLAIM"),
        ("CLG3963_2_constancy", "constant universal G_eff", "Pi_G is parent-constant/source-blind/range-blind/frame-blind", "CONDITIONAL_ONLY"),
        ("CLG3963_3_mass_source", "M_eff Hilbert source denominator", "Pi_M J_H source mass conserved and same-frame", "NEXT_TARGET_REQUIRED"),
        ("CLG3963_4_Newton_claim", "Newton/local GR source side", "epsilon_Newton_source=0 plus EH/Poisson/readout gates", "BLOCKED_NONCLAIM"),
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
            "row_id": "NEXT3963_0",
            "next_doc": NEXT_DOC,
            "next_script": NEXT_SCRIPT,
            "target": "derive or bound the Hilbert source denominator and Pi_M owner: show M_eff[Pi_M J_H] is conserved, same-frame, and equals the Hamiltonian/Gauss source, or produce flux/projector residual scores",
            "success_condition": "M_eff drift, Pi_M commutator, projector stress, and boundary/source flux are theorem-zero or feed epsilon_Newton_source as finite nonclaim residuals",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
    ]


def status_rows(timestamp: str, source_rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    found = sum(bool(row["exists"]) and bool(row["needle_found"]) for row in source_rows)
    return [
        {
            "checkpoint": CHECKPOINT,
            "status": "PASS_PRIVATE_NONCLAIM_NEWTON_COUPLING_SCORE",
            "summary": "3963 derives the measured Newton source-coupling product law, refuses an absolute numerical G claim without parent scale, and creates epsilon_Newton_source as a first symbolic residual score feeding Gdot/WEP/R10/PPN/Newton gates.",
            "sources_found": f"{found}/{len(source_rows)}",
            "claim_allowed": False,
            "timestamp_utc": timestamp,
        }
    ]


def doc_text(timestamp: str, source_rows: list[dict[str, Any]]) -> str:
    found = sum(bool(row["exists"]) and bool(row["needle_found"]) for row in source_rows)
    return f"""# 3963 - Source-Coupling Product Newton G Constancy Or Residual Score

Timestamp: `{timestamp}`

## Result

3963 makes the Newton/G issue precise.

No absolute numerical `G_N` claim is made. Without a parent-owned `kappa_MTS` or absolute parent scale, the numerical value of `G` is a calibrated/global constant, just as in standard GR practice.

The serious derivable target is constancy and universality:

`Pi_G := G_ref w_common ell_J R_frame`

`G_eff proportional to Pi_G^(-1)`

`mu_obs := G_eff M_eff(1+epsilon_mu)`

so

`D_X ln mu_obs = -D_X ln Pi_G + D_X ln M_eff + D_X ln(1+epsilon_mu)`.

That gives the first symbolic source-coupling score:

`epsilon_Newton_source <= |D ln Pi_G| + |D ln M_eff| + |D ln(1+epsilon_mu)| + |delta_frame_source| + |eta_source_AB| + |alpha_mu(lambda)| + K_EMsource epsilon_EM_residual`.

## Meaning

Newtonian recovery now has a clean fork:

- prove every derivative/source/range/frame/species piece is zero by parent structure;
- or score each surviving term against Gdot, WEP, R10, PPN, clocks, and orbital constraints.

## Source/Register

- Sources found: `{found}/{len(source_rows)}`
- Product identity: `source-intake\\mts_residuals\\P8_Y5_R2FR_3963_NEWTON_G_PRODUCT_IDENTITY.csv`
- Constancy conditions: `source-intake\\mts_residuals\\P8_Y5_R2FR_3963_CONSTANT_UNIVERSAL_G_CONDITIONS.csv`
- Residual vector: `source-intake\\mts_residuals\\P8_Y5_R2FR_3963_NEWTON_SOURCE_RESIDUAL_VECTOR.csv`
- First score: `source-intake\\mts_residuals\\P8_Y5_R2FR_3963_NEWTON_FIRST_NONCLAIM_SCORE_ROW.csv`
- Validation: `source-intake\\mts_residuals\\P8_Y5_BRR545_3963_VALIDATION.csv`

## Next Target

`{NEXT_DOC}`
"""


def spine_block(timestamp: str) -> str:
    return f"""

## 3963 - Newton Source-Coupling Product Score

Timestamp: `{timestamp}`

- Refuses an absolute numerical `G_N` claim without parent-owned `kappa_MTS` or parent scale.
- Derives the measured source-coupling residual law: `D_X ln mu_obs = -D_X ln Pi_G + D_X ln M_eff + D_X ln(1+epsilon_mu)`.
- Creates `epsilon_Newton_source` as a symbolic residual score feeding Gdot/WEP/R10/PPN/Newton gates.
- Next: `{NEXT_DOC}`.
"""


def update_spine(timestamp: str) -> None:
    block = spine_block(timestamp)
    marker = "## 3963 - Newton Source-Coupling Product Score"
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
    identities = identity_rows(timestamp)
    conditions = condition_rows(timestamp)
    vector = vector_rows(timestamp)
    scores = score_rows(timestamp)
    decisions = decision_rows(timestamp)
    claims = claim_gate_rows(timestamp)
    next_target = next_rows(timestamp)
    generated_csvs = [path for key, path in OUTPUTS.items() if key != "validation"]
    generated_paths = generated_csvs + [DOC_PATH, SCRIPT_PATH, SPINE_PATH]
    fwb_git_clean, fwb_git_detail = formalization_workbench_git_status()

    identity_statuses = {row["status"] for row in identities}
    condition_statuses = {row["status"] for row in conditions}
    vector_symbols = {row["symbol"] for row in vector}
    score_names = {row["score_name"] for row in scores}
    decision_text = " ".join(row["decision"] for row in decisions)
    claim_statuses = {row["status"] for row in claims}
    all_physics_rows = identities + conditions + vector + scores + decisions + claims + next_target

    checks = [
        ("VAL3963_00_sources_exist", all(row["exists"] for row in source_rows), "all cited source paths exist"),
        ("VAL3963_01_needles_found", all(row["needle_found"] for row in source_rows), "all cited source needles found"),
        ("VAL3963_02_identity", "DERIVED_RESIDUAL_LAW" in identity_statuses and "NO_ABSOLUTE_G_CLAIM" in identity_statuses, "Newton product identity and no absolute G claim written"),
        ("VAL3963_03_conditions", {"CONDITIONAL_ZERO_ROUTE", "OPEN_OWNER_ROUTE", "NEXT_TARGET", "OPEN_VECTOR_ROUTE", "POLICY_REQUIRED"}.issubset(condition_statuses), "constancy/universality conditions covered"),
        ("VAL3963_04_vector", {"dln_mu_obs_dt", "partial_r_ln_mu_obs", "alpha_mu(lambda)", "eta_source_AB", "delta_frame_source", "epsilon_mu_vector", "epsilon_EM_residual"}.issubset(vector_symbols), "Newton source residual vector complete"),
        ("VAL3963_05_score", {"epsilon_Newton_source", "Delta_Newton_source_side"}.issubset(score_names), "Newton symbolic score rows written"),
        ("VAL3963_06_decision", "do not claim an absolute numerical derivation" in decision_text and "constancy/universality" in decision_text, "decision records correct G stance"),
        ("VAL3963_07_claim_gate", "PASS_SYMBOLIC_NONCLAIM" in claim_statuses and "CONDITIONAL_ONLY" in claim_statuses and "NEXT_TARGET_REQUIRED" in claim_statuses and "BLOCKED_NONCLAIM" in claim_statuses, "claim gate blocks Newton/local-GR promotion"),
        ("VAL3963_08_next_target", next_target[0]["next_doc"] == NEXT_DOC and next_target[0]["next_script"] == NEXT_SCRIPT, "next target points to Hilbert/PiM source denominator"),
        ("VAL3963_09_all_nonclaim", all(not row["valid_for_claim"] for row in all_physics_rows), "all generated physics rows remain nonclaim"),
        ("VAL3963_10_score_ready", all(row["score_ready"] for row in scores) and all(row["score_ready"] for row in vector), "symbolic Newton rows are score-ready"),
        ("VAL3963_11_outputs_outside_fwb", all(FWB not in path.parents and path != FWB for path in generated_paths), "no generated output is inside formalization-workbench"),
        ("VAL3963_12_fwb_git_or_scope_guard", fwb_git_clean or all(FWB not in path.parents and path != FWB for path in generated_paths), fwb_git_detail),
        ("VAL3963_13_doc_exists", DOC_PATH.exists(), "checkpoint doc exists"),
        ("VAL3963_14_spine_updated", SPINE_PATH.exists() and "3963 - Newton Source-Coupling Product Score" in read_text(SPINE_PATH), "spine updated"),
        ("VAL3963_15_csv_parse", csv_parse_ok(generated_csvs), "generated CSV files parse cleanly"),
        ("VAL3963_16_script_compile", True, "script compiled before validation write"),
        ("VAL3963_17_no_pycache", not (SCRIPT_PATH.parent / "__pycache__").exists(), "scripts __pycache__ removed"),
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
    identities = identity_rows(timestamp)
    conditions = condition_rows(timestamp)
    vector = vector_rows(timestamp)
    scores = score_rows(timestamp)
    decisions = decision_rows(timestamp)
    claims = claim_gate_rows(timestamp)
    next_target = next_rows(timestamp)
    status = status_rows(timestamp, sources)

    write_csv(OUTPUTS["sources"], sources)
    write_csv(OUTPUTS["identity"], identities)
    write_csv(OUTPUTS["conditions"], conditions)
    write_csv(OUTPUTS["vector"], vector)
    write_csv(OUTPUTS["score"], scores)
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
        raise SystemExit(f"3963 validation failed: {failed}")

    print(f"3963 checkpoint complete: {DOC_PATH}")
    print(f"validation: {OUTPUTS['validation']}")
    print("Newton/source coupling product residual score assembled; no absolute G claim made")


if __name__ == "__main__":
    run()

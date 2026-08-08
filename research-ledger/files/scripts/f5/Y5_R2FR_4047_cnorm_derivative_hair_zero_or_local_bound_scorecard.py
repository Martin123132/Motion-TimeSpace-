from __future__ import annotations

import csv
import py_compile
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, Iterable, List


ROOT = Path(__file__).resolve().parents[1]
PROJECT = ROOT.parent
SOURCE_DIR = ROOT / "source-intake" / "mts_residuals"
FORMALIZATION = PROJECT / "formalization-workbench"
SCRIPT_PATH = Path(__file__).resolve()
DOC_PATH = ROOT / "4047-Y5-R2FR-cnorm-derivative-hair-zero-or-local-bound-scorecard.md"

OUTPUTS = {
    "source_register": SOURCE_DIR / "P8_Y5_R2FR_4047_SOURCE_REGISTER.csv",
    "component_decomposition": SOURCE_DIR / "P8_Y5_R2FR_4047_CNORM_COMPONENT_DECOMPOSITION.csv",
    "selected_zero_theorem": SOURCE_DIR / "P8_Y5_R2FR_4047_SELECTED_ZERO_THEOREM.csv",
    "channel_rollup": SOURCE_DIR / "P8_Y5_R2FR_4047_ZEROED_CHANNEL_ROLLUP.csv",
    "fallback_bound": SOURCE_DIR / "P8_Y5_R2FR_4047_FALLBACK_BOUND_VECTOR.csv",
    "local_gr_gate": SOURCE_DIR / "P8_Y5_R2FR_4047_LOCAL_GR_GATE_UPDATE.csv",
    "evaluator": SOURCE_DIR / "P8_Y5_R2FR_4047_EVALUATOR_RESULTS.csv",
    "decision_gate": SOURCE_DIR / "P8_Y5_R2FR_4047_DECISION_GATE.csv",
    "claim_gate": SOURCE_DIR / "P8_Y5_R2FR_4047_CLAIM_GATE.csv",
    "remaining_residuals": SOURCE_DIR / "P8_Y5_R2FR_4047_REMAINING_LOCAL_RESIDUAL_VECTOR.csv",
    "next_target": SOURCE_DIR / "P8_Y5_R2FR_4047_NEXT_TARGET.csv",
    "status": SOURCE_DIR / "P8_Y5_R2FR_4047_STATUS.csv",
    "validation": SOURCE_DIR / "P8_Y5_BRR545_4047_VALIDATION.csv",
}


def timestamp() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def write_csv(path: Path, rows: List[Dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        raise ValueError(f"empty rows for {path}")
    fields: List[str] = []
    for row in rows:
        for key in row:
            if key not in fields:
                fields.append(key)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def source_rows(ts: str) -> List[Dict[str, object]]:
    specs = [
        ("SRC4047_00", SOURCE_DIR / "P8_Y5_R2FR_4041_CNORM_SPLIT.csv", "Delta_source_norm = D_a ln mu_obs = D_a ln G_obs", "4041 c_norm split into G, source mass, and epsilon factors"),
        ("SRC4047_01", SOURCE_DIR / "P8_Y5_R2FR_4041_KAPPA_OBS_ROUTING.csv", "spacetime-varying coupling is physical", "4041 Bianchi guard against hiding drift"),
        ("SRC4047_02", SOURCE_DIR / "P8_Y5_R2FR_4016_GREF_SUPERSELECTION_THEOREM.csv", "D_X ln G_ref=0", "fixed coupling branch gives G derivative silence"),
        ("SRC4047_03", SOURCE_DIR / "P8_Y5_R2FR_4016_GLOBAL_COUPLING_AUDIT.csv", "parent configuration splits dynamical fields from K_G", "records unsigned status of global coupling superselection"),
        ("SRC4047_04", SOURCE_DIR / "P8_Y5_R2FR_4015_GAUSS_POISSON_GREF_NEWTON_THEOREM.csv", "MTS may likewise calibrate G_ref", "Newton constant policy and calibration guard"),
        ("SRC4047_05", SOURCE_DIR / "P8_Y5_R2FR_4011_HILBERT_WORLDTUBE_LOCK_THEOREM.csv", "D_v W_H=0", "worldtube/support descent needed for source mass constancy"),
        ("SRC4047_06", SOURCE_DIR / "P8_Y5_R2FR_4012_PIM_HTAU_CHARGE_LOCK_THEOREM.csv", "M_H_ref=H_tau-H_ref=Mbar_H_ref(q(Phi))", "Pi_M/H_tau/Hilbert mass-charge lock"),
        ("SRC4047_07", SOURCE_DIR / "P8_Y5_R2FR_4038_POYNTING_NO_FLUX_THEOREM.csv", "c_Poynting * Phi_EM_rad = 0", "Poynting/boundary no-flux source-mass guard"),
        ("SRC4047_08", SOURCE_DIR / "P8_Y5_R2FR_4043_SELECTED_BRANCH_ZERO_THEOREM.csv", "No local domain preferred-momentum flux is generated.", "projector/domain source-normalization silence"),
        ("SRC4047_09", ROOT / "4046-Y5-R2FR-memory-tail-support-gap-zero-theorem-or-tail-bound-inputs.md", "Delta_cZ_selected=0", "4046 memory tail closure carried forward"),
        ("SRC4047_10", SOURCE_DIR / "P8_Y5_R2FR_3954_LOCAL_COUPLING_PRODUCT_GATE.csv", "D_X ln product must vanish", "local coupling product derivative target"),
        ("SRC4047_11", SOURCE_DIR / "P8_Y5_R2FR_3954_Z_SOURCE_CURRENT_THEOREM.csv", "J_A|0=0", "source-current silence theorem"),
        ("SRC4047_12", SOURCE_DIR / "P8_Y5_R2FR_4018_SECOND_ORDER_PPN_STABILITY_THEOREM.csv", "source prefactors are absent", "PPN second-order source-prefactor guard"),
        ("SRC4047_13", SOURCE_DIR / "P8_Y5_R2FR_4019_NO_EXTRA_OPERATOR_THEOREM.csv", "EH field equation with fixed K_G", "EH-only local exterior route"),
        ("SRC4047_14", SOURCE_DIR / "P8_SOURCE_NORMALIZATION_DERIVED_ZERO_TARGETS.csv", "parent compact-exterior source identity gives d(Pi_M J)=0", "source-normalization channel zero targets"),
        ("SRC4047_15", SOURCE_DIR / "P8_R11_SOURCE_NORMALIZATION_OPERATOR_MINIMUM_FILL.csv", "epsilon_radial_Meff", "fallback coefficient list for nonzero c_norm channels"),
    ]
    rows: List[Dict[str, object]] = []
    for source_id, path, needle, role in specs:
        exists = path.exists()
        text = read_text(path) if exists else ""
        rows.append(
            {
                "source_id": source_id,
                "path": str(path),
                "exists": exists,
                "needle": needle,
                "needle_found": needle in text,
                "role": role,
                "timestamp_utc": ts,
            }
        )
    return rows


def component_decomposition_rows(ts: str) -> List[Dict[str, object]]:
    return [
        {
            "component_id": "CN4047_0_Gobs",
            "symbol": "D_a ln G_obs",
            "source_formula": "D_a ln G_obs = -D_a ln(1/kappa_*+2*c_I*phi_*)",
            "selected_branch_law": "D_a ln G_obs=0 when the same fixed K_G/kappa_* branch sets EH, Newton, PPN, and source readout before local variation",
            "fallback_if_unsigned": "epsilon_Gref_superselection_4016",
            "status": "ZERO_IN_SELECTED_FIXED_COUPLING_BRANCH_ELSE_BOUND",
            "valid_for_public_claim": False,
            "timestamp_utc": ts,
        },
        {
            "component_id": "CN4047_1_Meff",
            "symbol": "D_a ln M_eff",
            "source_formula": "D_a ln M_eff from d(Pi_M J_H) and source-measure flux",
            "selected_branch_law": "D_a ln M_eff=0 when Pi_M J_H=J_M_top+dB_zero, M_H_ref=H_tau-H_ref is q-basic, and exterior flux/reference terms vanish",
            "fallback_if_unsigned": "epsilon_support_4011 + epsilon_charge_4012 + boundary/Poynting finite rows",
            "status": "ZERO_IN_SELECTED_SAME_SOURCE_CHARGE_BRANCH_ELSE_BOUND",
            "valid_for_public_claim": False,
            "timestamp_utc": ts,
        },
        {
            "component_id": "CN4047_2_epsilon",
            "symbol": "D_a ln(1+epsilon_mu)",
            "source_formula": "extra/source-frame/projector/species normalization derivative",
            "selected_branch_law": "D_a ln(1+epsilon_mu)=0 when no source-only prefactor exists, the source-label-forgetting functor holds, and projector/domain/memory/nonEH leakage is silent",
            "fallback_if_unsigned": "epsilon_source_norm_extra_4047",
            "status": "ZERO_IN_SELECTED_NO_SOURCE_PREF_BRANCH_ELSE_BOUND",
            "valid_for_public_claim": False,
            "timestamp_utc": ts,
        },
        {
            "component_id": "CN4047_3_total",
            "symbol": "Delta_cnorm_selected",
            "source_formula": "Delta_cnorm = |D ln G_obs| + |D ln M_eff| + |D ln(1+epsilon_mu)| as an absolute no-cancellation envelope",
            "selected_branch_law": "0+0+0=0",
            "fallback_if_unsigned": "Delta_cnorm_fallback <= eps_G + eps_Meff + eps_epsilon_mu",
            "status": "ZERO_IN_PRIVATE_SELECTED_BRANCH_ELSE_FALLBACK",
            "valid_for_public_claim": False,
            "timestamp_utc": ts,
        },
    ]


def selected_zero_theorem_rows(ts: str) -> List[Dict[str, object]]:
    return [
        {
            "theorem_id": "CZT4047_0_split",
            "premise": "4041 c_norm split",
            "formula": "Delta_cnorm = |D ln G_obs| + |D ln M_eff| + |D ln(1+epsilon_mu)|",
            "result": "each derivative channel must be zero separately; no cancellation is allowed",
            "status": "NO_CANCELLATION_SPLIT_ACCEPTED",
            "valid_for_public_claim": False,
            "timestamp_utc": ts,
        },
        {
            "theorem_id": "CZT4047_1_Gobs_zero",
            "premise": "fixed global coupling branch",
            "formula": "G_obs=G_ref=c^4 kappa_*/(8*pi), delta_local kappa_*=0, D_a phi_*=0",
            "result": "D_a ln G_obs=0 for local time, radial, range, source, frame, domain, memory, and projector directions",
            "status": "ZERO_IN_PRIVATE_SELECTED_BRANCH",
            "valid_for_public_claim": False,
            "timestamp_utc": ts,
        },
        {
            "theorem_id": "CZT4047_2_Meff_zero",
            "premise": "same Hilbert/H_tau/Pi_M source charge with zero exterior flux",
            "formula": "M_eff=M_H_ref=H_tau[S_outer]-H_ref=Mbar_H_ref(q(Phi)); D_a M_eff=0",
            "result": "projected source mass has no radial/source/frame/support derivative hair in the compact exterior branch",
            "status": "ZERO_IN_PRIVATE_SELECTED_BRANCH",
            "valid_for_public_claim": False,
            "timestamp_utc": ts,
        },
        {
            "theorem_id": "CZT4047_3_epsilon_zero",
            "premise": "no source-only weights plus prior local silence packets",
            "formula": "epsilon_mu=epsilon_direct+epsilon_measure+epsilon_support+epsilon_projector+epsilon_memory+epsilon_nonEH=0",
            "result": "no residual source-normalization derivative can be attached to matter labels, domain projectors, memory tails, or non-EH local operators",
            "status": "ZERO_IN_PRIVATE_SELECTED_BRANCH",
            "valid_for_public_claim": False,
            "timestamp_utc": ts,
        },
        {
            "theorem_id": "CZT4047_4_total_zero",
            "premise": "all three c_norm derivative channels vanish separately",
            "formula": "Delta_cnorm_selected=0",
            "result": "the selected local branch no longer carries c_norm derivative hair",
            "status": "ZERO_IN_PRIVATE_SELECTED_BRANCH",
            "valid_for_public_claim": False,
            "timestamp_utc": ts,
        },
        {
            "theorem_id": "CZT4047_5_scope_guard",
            "premise": "private branch adoption is still not final parent-action theorem",
            "formula": "selected local compact PPN/Newton branch != public all-sector MTS theorem",
            "result": "full local-GR/public claim remains blocked until the parent packet is adopted or bound rows pass",
            "status": "PUBLIC_CLAIM_BLOCKED",
            "valid_for_public_claim": False,
            "timestamp_utc": ts,
        },
    ]


def channel_rollup_rows(ts: str) -> List[Dict[str, object]]:
    rows = [
        ("ROLL4047_0_radial", "radial_Meff_hair", "epsilon_radial_Meff", "D_a ln M_eff=0 from q-basic M_H_ref plus no exterior source flux", "ZERO_IN_PRIVATE_SELECTED_BRANCH_ELSE_SUPPORT_CHARGE_BOUND"),
        ("ROLL4047_1_boundary", "boundary_monopole_shift", "epsilon_boundary", "fixed source-blind boundary/reference plus Poynting no-flux rows remove boundary source shift", "ZERO_IN_PRIVATE_SELECTED_BRANCH_ELSE_BOUNDARY_BOUND"),
        ("ROLL4047_2_domain", "domain_projector_mass", "epsilon_domain_projector", "4043 projector/domain stress/readout denominator silence removes second projector mass", "ZERO_IN_PRIVATE_SELECTED_BRANCH_ELSE_ALPHA_XI_BOUND"),
        ("ROLL4047_3_bulk", "bulk_X_Yukawa_tail", "epsilon_bulk_X", "4046 reset/no-incoming memory branch removes compact local tail; finite-range fallback retained if reset rejected", "ZERO_IN_PRIVATE_SELECTED_BRANCH_ELSE_R10_RANGE_BOUND"),
        ("ROLL4047_4_nonEH", "nonEH_operator_potential", "epsilon_nonEH_source", "4019 EH-only local exterior removes non-EH source potential in selected branch", "ZERO_IN_PRIVATE_SELECTED_BRANCH_ELSE_PPN_OPERATOR_BOUND"),
        ("ROLL4047_5_species", "species_source_charge", "epsilon_species_A", "source-label-forgetting/no Hom(source label to weight) removes species/source charge derivative", "ZERO_IN_PRIVATE_SELECTED_BRANCH_ELSE_WEP_BOUND"),
        ("ROLL4047_6_time", "time_drift", "epsilon_time_drift", "fixed K_G plus stationary compact source branch removes local Gdot/time drift", "ZERO_IN_PRIVATE_SELECTED_BRANCH_ELSE_GDOT_BOUND"),
        ("ROLL4047_7_calibration", "absolute_calibration_offset", "epsilon_calibration", "constant common calibration is allowed only as universal branch constant, not derivative hair or numerical G prediction", "CALIBRATION_CONSTANT_ONLY_NO_ABSOLUTE_G_CLAIM"),
    ]
    return [
        {
            "rollup_id": row_id,
            "p8_channel": channel,
            "coefficient_symbol": coeff,
            "selected_branch_resolution": resolution,
            "status": status,
            "valid_for_public_claim": False,
            "timestamp_utc": ts,
        }
        for row_id, channel, coeff, resolution, status in rows
    ]


def fallback_bound_rows(ts: str) -> List[Dict[str, object]]:
    return [
        {
            "bound_id": "CB4047_0_G",
            "symbol": "epsilon_G",
            "used_if": "fixed K_G/kappa_* superselection or same-branch calibration is rejected",
            "bound_formula": "|D ln G_obs| <= epsilon_Gref_superselection_4016",
            "arena_links": "Gdot, PPN, orbital, R10/range if range-dependent coupling survives",
            "valid_for_claim": False,
            "timestamp_utc": ts,
        },
        {
            "bound_id": "CB4047_1_Meff",
            "symbol": "epsilon_Meff",
            "used_if": "same Hilbert/H_tau/Pi_M charge, support lock, or no-flux source measure closure is rejected",
            "bound_formula": "|D ln M_eff| <= epsilon_support_4011 + epsilon_charge_4012 + epsilon_boundary_flux + epsilon_EM_once",
            "arena_links": "orbital GM, PPN source mass, clocks, compact-source WEP",
            "valid_for_claim": False,
            "timestamp_utc": ts,
        },
        {
            "bound_id": "CB4047_2_epsmu",
            "symbol": "epsilon_mu_derivative",
            "used_if": "source-only prefactor exclusion, projector/domain silence, memory reset, or EH-only local exterior is rejected",
            "bound_formula": "|D ln(1+epsilon_mu)| <= |epsilon_species_A|+|epsilon_domain_projector|+|epsilon_bulk_X|+|epsilon_nonEH_source|+|epsilon_time_drift|+|epsilon_boundary|",
            "arena_links": "WEP, PPN alpha/xi/zeta, R10 alpha(lambda), Gdot, clock/orbital drifts",
            "valid_for_claim": False,
            "timestamp_utc": ts,
        },
        {
            "bound_id": "CB4047_3_total",
            "symbol": "Delta_cnorm_fallback",
            "used_if": "any selected-branch zero clause is not parent-signed",
            "bound_formula": "Delta_cnorm_fallback <= epsilon_G + epsilon_Meff + epsilon_mu_derivative",
            "arena_links": "absolute no-cancellation envelope over local arenas",
            "valid_for_claim": False,
            "timestamp_utc": ts,
        },
    ]


def local_gr_gate_rows(ts: str) -> List[Dict[str, object]]:
    return [
        {
            "gate_id": "LG4047_0_cZ",
            "gate": "Delta_cZ_selected",
            "previous_status": "ZERO_IN_PRIVATE_SELECTED_RESET_BRANCH from 4046",
            "new_status": "carried_zero",
            "public_claim": False,
            "timestamp_utc": ts,
        },
        {
            "gate_id": "LG4047_1_cnorm",
            "gate": "Delta_cnorm_selected",
            "previous_status": "live derivative hair",
            "new_status": "zero in private selected fixed-coupling/same-source/no-prefactor branch",
            "public_claim": False,
            "timestamp_utc": ts,
        },
        {
            "gate_id": "LG4047_2_parent",
            "gate": "Parent_packet_adoption",
            "previous_status": "live",
            "new_status": "only hard live selected-branch adoption gate after cZ/cnorm reductions",
            "public_claim": False,
            "timestamp_utc": ts,
        },
    ]


def evaluator_rows(ts: str) -> List[Dict[str, object]]:
    return [
        {
            "case_id": "CASE4047_0_selected_branch",
            "verdict": "CNORM_ZERO_IN_PRIVATE_SELECTED_BRANCH",
            "result": "With fixed K_G, same Hilbert/H_tau/Pi_M source charge, no exterior flux, no source-only prefactors, projector/domain silence, memory-tail reset, and EH-only local exterior, Delta_cnorm_selected=0.",
            "valid_for_public_claim": False,
            "timestamp_utc": ts,
        },
        {
            "case_id": "CASE4047_1_if_any_clause_rejected",
            "verdict": "CNORM_BOUND_VECTOR_REQUIRED",
            "result": "If any zero clause is not parent-signed, keep the absolute bound Delta_cnorm_fallback <= epsilon_G + epsilon_Meff + epsilon_mu_derivative.",
            "valid_for_public_claim": False,
            "timestamp_utc": ts,
        },
        {
            "case_id": "CASE4047_2_project_status",
            "verdict": "LOCAL_BRANCH_NARROWED_TO_PARENT_PACKET_ADOPTION",
            "result": "In the selected private branch, cZ and c_norm are now zero; public/local-GR status still requires parent packet adoption or sourced fallback bounds.",
            "valid_for_public_claim": False,
            "timestamp_utc": ts,
        },
    ]


def decision_gate_rows(ts: str) -> List[Dict[str, object]]:
    return [
        {
            "decision_id": "DEC4047_0_result",
            "decision": "accept selected-branch c_norm zero as private theorem candidate",
            "reason": "all three derivative channels reduce separately to existing fixed-coupling, same-source, and no-prefactor packets",
            "next_action": "try to promote the selected local packet into one parent-action adoption contract",
            "valid_for_public_claim": False,
            "timestamp_utc": ts,
        },
        {
            "decision_id": "DEC4047_1_no_claim",
            "decision": "do not claim local GR publicly from 4047",
            "reason": "the selected branch still depends on parent packet adoption; fallback bound rows remain active if adoption fails",
            "next_action": "write 4048 parent packet adoption or fallback scorecard",
            "valid_for_public_claim": False,
            "timestamp_utc": ts,
        },
    ]


def claim_gate_rows(ts: str) -> List[Dict[str, object]]:
    return [
        {
            "claim_id": "CLAIM4047_0_private",
            "claim": "Delta_cnorm_selected=0 in the private selected compact local branch",
            "allowed": True,
            "public_claim": False,
            "scope": "internal theorem candidate only",
            "timestamp_utc": ts,
        },
        {
            "claim_id": "CLAIM4047_1_public_local_GR",
            "claim": "MTS has a public completed local-GR derivation",
            "allowed": False,
            "public_claim": False,
            "scope": "blocked by parent packet adoption and fallback-bound requirements",
            "timestamp_utc": ts,
        },
    ]


def remaining_residual_rows(ts: str) -> List[Dict[str, object]]:
    return [
        {
            "residual_id": "REM4047_0_parent",
            "symbol": "Parent_packet_adoption",
            "residual": "selected local fixed-coupling/same-source/no-prefactor/reset packet must be adopted as one parent-action theorem rather than a stitched branch ledger",
            "current_route": "4048 parent adoption contract or fallback scorecard",
            "timestamp_utc": ts,
        },
        {
            "residual_id": "REM4047_1_cnorm_fallback",
            "symbol": "Delta_cnorm_fallback_if_source_packet_rejected",
            "residual": "finite bound vector if fixed K_G, same-source charge, no-prefactor, projector/domain, memory-reset, or EH-only clauses are rejected",
            "current_route": "source-backed local bound rows",
            "timestamp_utc": ts,
        },
        {
            "residual_id": "REM4047_2_cZ_fallback",
            "symbol": "Delta_cZ_fallback_if_reset_rejected",
            "residual": "finite memory suppression bound if local reset/no-incoming branch is rejected",
            "current_route": "3895/3931 suppression inputs",
            "timestamp_utc": ts,
        },
    ]


def next_target_rows(ts: str) -> List[Dict[str, object]]:
    return [
        {
            "row_id": "NEXT4047_0",
            "next_doc": "4048-Y5-R2FR-parent-selected-local-packet-adoption-or-fallback-scorecard.md",
            "next_script": "scripts/Y5_R2FR_4048_parent_selected_local_packet_adoption_or_fallback_scorecard.py",
            "reason": "cZ and c_norm are zero in the private selected branch; the real remaining leap is making that selected packet one parent-action theorem or demoting it to closure/fallback",
            "timestamp_utc": ts,
        }
    ]


def status_rows(ts: str) -> List[Dict[str, object]]:
    return [
        {
            "status_id": "STAT4047",
            "status": "CZ_AND_CNORM_ZERO_IN_PRIVATE_SELECTED_BRANCH_PARENT_ADOPTION_NEXT",
            "public_claim": False,
            "timestamp_utc": ts,
        }
    ]


def doc_text(ts: str, source_count: int) -> str:
    return f"""# 4047 - c_norm Derivative Hair Zero Or Local Bound Scorecard

- Timestamp: `{ts}`
- Status: `private_nonclaim_checkpoint`
- Scope: `post-checkpoint-work` only; no `formalization-workbench` edits.
- Source needles found: `{source_count}/16`.

## What Actually Moved

4047 turns `Delta_cnorm_envelope` from a live phrase into a three-term derivative split:

`Delta_cnorm = |D ln G_obs| + |D ln M_eff| + |D ln(1+epsilon_mu)|`.

In the private selected compact local branch:

- `D ln G_obs=0` from the fixed `K_G/kappa_*` coupling branch;
- `D ln M_eff=0` from same Hilbert/H_tau/Pi_M source charge plus zero exterior flux;
- `D ln(1+epsilon_mu)=0` from no source-only prefactors, projector/domain silence, memory-tail reset, and EH-only local exterior.

Therefore `Delta_cnorm_selected=0` in the private selected local branch.

## What Is Not Being Claimed

This does not predict the numerical value of Newton's constant, and it is not a public local-GR proof. It says the derivative hair can be removed if the selected local packet is adopted as one parent-action branch. If any clause is rejected, use the fallback bound vector:

`Delta_cnorm_fallback <= epsilon_G + epsilon_Meff + epsilon_mu_derivative`.

## Current Verdict

- Current evaluator result: `CNORM_ZERO_IN_PRIVATE_SELECTED_BRANCH`.
- Claim result: `NO_PUBLIC_LOCAL_GR_CLAIM_FROM_4047`.
- In the selected private branch, `Delta_cZ_selected=0` and `Delta_cnorm_selected=0`.
- Remaining live gate: `Parent_packet_adoption`, plus fallback rows if the selected packet is rejected.

## Next Target

- `4048-Y5-R2FR-parent-selected-local-packet-adoption-or-fallback-scorecard.md`
- `scripts/Y5_R2FR_4048_parent_selected_local_packet_adoption_or_fallback_scorecard.py`
"""


def validate_outputs(source_register: List[Dict[str, object]], tables: Dict[str, List[Dict[str, object]]]) -> List[Dict[str, object]]:
    def all_rows_have_false_public(rows: Iterable[Dict[str, object]]) -> bool:
        for row in rows:
            if "valid_for_public_claim" in row and row["valid_for_public_claim"] is not False:
                return False
            if "public_claim" in row and row["public_claim"] is not False:
                return False
        return True

    validation = [
        ("VAL4047_00_sources_exist", all(row["exists"] for row in source_register), "all cited source paths exist"),
        ("VAL4047_01_needles_found", all(row["needle_found"] for row in source_register), "all source needles found"),
        ("VAL4047_02_split_terms", len(tables["component_decomposition"]) == 4, "G, M_eff, epsilon_mu and total rows present"),
        ("VAL4047_03_Gobs_zero", any(row["symbol"] == "D_a ln G_obs" and "ZERO" in row["status"] for row in tables["component_decomposition"]), "G_obs derivative zero row present"),
        ("VAL4047_04_Meff_zero", any(row["symbol"] == "D_a ln M_eff" and "ZERO" in row["status"] for row in tables["component_decomposition"]), "M_eff derivative zero row present"),
        ("VAL4047_05_epsilon_zero", any(row["symbol"] == "D_a ln(1+epsilon_mu)" and "ZERO" in row["status"] for row in tables["component_decomposition"]), "epsilon_mu derivative zero row present"),
        ("VAL4047_06_total_zero", any(row["symbol"] == "Delta_cnorm_selected" and "0+0+0=0" in row["selected_branch_law"] for row in tables["component_decomposition"]), "total c_norm selected zero row present"),
        ("VAL4047_07_no_cancellation", any("no cancellation" in row["result"].lower() for row in tables["selected_zero_theorem"]), "absolute no-cancellation split present"),
        ("VAL4047_08_channel_rollup", len(tables["channel_rollup"]) == 8, "all eight source-normalization channels rolled up"),
        ("VAL4047_09_fallback_G", any(row["symbol"] == "epsilon_G" for row in tables["fallback_bound"]), "G fallback bound present"),
        ("VAL4047_10_fallback_Meff", any(row["symbol"] == "epsilon_Meff" for row in tables["fallback_bound"]), "M_eff fallback bound present"),
        ("VAL4047_11_fallback_epsmu", any(row["symbol"] == "epsilon_mu_derivative" for row in tables["fallback_bound"]), "epsilon_mu fallback bound present"),
        ("VAL4047_12_fallback_total", any(row["symbol"] == "Delta_cnorm_fallback" for row in tables["fallback_bound"]), "total fallback bound present"),
        ("VAL4047_13_cZ_carried", any(row["gate"] == "Delta_cZ_selected" and row["new_status"] == "carried_zero" for row in tables["local_gr_gate"]), "4046 cZ zero carried forward"),
        ("VAL4047_14_cnorm_gate", any(row["gate"] == "Delta_cnorm_selected" and "zero" in row["new_status"] for row in tables["local_gr_gate"]), "c_norm gate updated"),
        ("VAL4047_15_parent_remaining", any(row["symbol"] == "Parent_packet_adoption" for row in tables["remaining_residuals"]), "parent adoption remains"),
        ("VAL4047_16_cnorm_fallback_remaining", any(row["symbol"] == "Delta_cnorm_fallback_if_source_packet_rejected" for row in tables["remaining_residuals"]), "c_norm fallback retained"),
        ("VAL4047_17_public_blocked", any(row["allowed"] is False and "public" in row["claim"].lower() for row in tables["claim_gate"]), "public local-GR claim blocked"),
        ("VAL4047_18_evaluator_zero", any(row["verdict"] == "CNORM_ZERO_IN_PRIVATE_SELECTED_BRANCH" for row in tables["evaluator"]), "c_norm zero evaluator present"),
        ("VAL4047_19_evaluator_fallback", any(row["verdict"] == "CNORM_BOUND_VECTOR_REQUIRED" for row in tables["evaluator"]), "fallback evaluator present"),
        ("VAL4047_20_next_target", len(tables["next_target"]) == 1 and "4048" in tables["next_target"][0]["next_doc"], "4048 next target present"),
        ("VAL4047_21_doc_written", DOC_PATH.exists(), "checkpoint doc written"),
        ("VAL4047_22_no_formalization_output", not any(str(path).startswith(str(FORMALIZATION)) for path in OUTPUTS.values()), "no output targets formalization-workbench"),
        ("VAL4047_23_script_compiles", script_compiles(), "script compiles"),
        ("VAL4047_24_private_guard", all(all_rows_have_false_public(rows) for rows in tables.values()), "public-claim guard retained"),
    ]
    return [
        {"check_id": check_id, "passed": passed, "detail": detail}
        for check_id, passed, detail in validation
    ]


def script_compiles() -> bool:
    try:
        py_compile.compile(str(SCRIPT_PATH), doraise=True)
        return True
    except py_compile.PyCompileError:
        return False


def main() -> None:
    ts = timestamp()
    SOURCE_DIR.mkdir(parents=True, exist_ok=True)

    sources = source_rows(ts)
    source_count = sum(1 for row in sources if row["needle_found"])
    tables: Dict[str, List[Dict[str, object]]] = {
        "component_decomposition": component_decomposition_rows(ts),
        "selected_zero_theorem": selected_zero_theorem_rows(ts),
        "channel_rollup": channel_rollup_rows(ts),
        "fallback_bound": fallback_bound_rows(ts),
        "local_gr_gate": local_gr_gate_rows(ts),
        "evaluator": evaluator_rows(ts),
        "decision_gate": decision_gate_rows(ts),
        "claim_gate": claim_gate_rows(ts),
        "remaining_residuals": remaining_residual_rows(ts),
        "next_target": next_target_rows(ts),
        "status": status_rows(ts),
    }

    DOC_PATH.write_text(doc_text(ts, source_count), encoding="utf-8")
    write_csv(OUTPUTS["source_register"], sources)
    for key, rows in tables.items():
        write_csv(OUTPUTS[key], rows)

    validation_rows = validate_outputs(sources, tables)
    write_csv(OUTPUTS["validation"], validation_rows)

    cache_dir = SCRIPT_PATH.parent / "__pycache__"
    if cache_dir.exists():
        shutil.rmtree(cache_dir)

    failures = [row for row in validation_rows if not row["passed"]]
    print(f"wrote {DOC_PATH}")
    print(f"validation rows: {len(validation_rows)}")
    print(f"validation failures: {len(failures)}")
    for failure in failures:
        print(f"FAIL {failure['check_id']}: {failure['detail']}")


if __name__ == "__main__":
    main()

from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
REPO = ROOT.parent
FW = REPO / "formalization-workbench"
OUT = ROOT / "source-intake" / "mts_residuals"
PYCACHE = ROOT / "scripts" / "__pycache__"
DOC = ROOT / "3365-Y5-R2FR-DeltaGM-extra-mass-projection-bound-row-under-AX1090.md"
RUN_UTC = datetime.now(timezone.utc).isoformat()

WEP_BOUND = 2.8e-15
DOTG_BOUND = 4.0e-14
DOTG_INTERNAL_TARGET = 9.6e-15
R10_ALPHA_ANCHOR_LAMBDA_M = 3.86e-5

LOCAL_SOURCES = [
    ("LSRC3365_0_3364_doc", ROOT / "3364-Y5-R2FR-no-source-prefactor-grammar-or-WEP-projection-owner-under-AX1090.md", "3364 handoff"),
    ("LSRC3365_1_3364_next", OUT / "P8_Y5_R2FR_3364_NEXT_TARGET.csv", "3364 next target"),
    ("LSRC3365_2_3364_update", OUT / "P8_Y5_R2FR_3364_MICROSCOPE_BOUND_STATUS_UPDATE.csv", "3364 MICROSCOPE bound status"),
    ("LSRC3365_3_3109_source_mass", OUT / "P8_Y5_R2FR_3109_SOURCE_MASS_LOCK_DELTA_GM_ROWS.csv", "source-mass lock DeltaGM rows"),
    ("LSRC3365_4_charge_residuals", OUT / "P8_charge_current_equality_RESIDUAL_DECOMPOSITION.csv", "charge-current residual decomposition"),
    ("LSRC3365_5_r11_source_norm", OUT / "P8_R11_SOURCE_NORMALIZATION_OPERATOR_MINIMUM_FILL.csv", "R11 source-normalization operator rows"),
    ("LSRC3365_6_calibration", OUT / "P8_CALIBRATION_LOCK_ATTEMPT.csv", "calibration lock attempt"),
    ("LSRC3365_7_3363_bound", OUT / "P8_Y5_R2FR_3363_FIRST_SOURCE_NORMALIZATION_BOUND_ROW.csv", "MICROSCOPE species/source bound"),
    ("LSRC3365_8_dotg_source", OUT / "P8_Y5_R2FR_2933_COUPLING_BOUND_SOURCE_ACQUISITION.csv", "MESSENGER dotG source-backed comparator"),
    ("LSRC3365_9_dotg_transfer", OUT / "P8_Y5_R2FR_2934_DOTG_BOUND_TRANSFER_SCORECARD.csv", "dotG transfer scorecard"),
    ("LSRC3365_10_r10_bound_rows", OUT / "P8_Y5_R2FR_3012_R10_BOUND_ROWS_NONCLAIM.csv", "R10 bound rows"),
    ("LSRC3365_11_r10_anchor_rows", OUT / "P8_Y5_R2FR_2935_R10_SOURCE_BACKED_ANCHOR_ROWS.csv", "R10 source-backed anchors"),
    ("LSRC3365_12_ppn_vector", OUT / "P8_Y5_R2FR_3110_LOCAL_PPN_RESIDUAL_VECTOR.csv", "local PPN residual vector"),
    ("LSRC3365_13_3357_scope", OUT / "P8_Y5_R2FR_3357_CLAIM_SCOPE_SEPARATION.csv", "AX1090 source-side scope separation"),
    ("LSRC3365_14_3362_gref", OUT / "P8_Y5_R2FR_3362_GREF_OWNER_AND_NEWTON_LIMIT.csv", "Gref owner and Newton limit"),
]

OUTPUTS = {
    "local_sources": OUT / "P8_Y5_R2FR_3365_LOCAL_SOURCE_REGISTER.csv",
    "split_theorem": OUT / "P8_Y5_R2FR_3365_DELTAGM_SPLIT_THEOREM.csv",
    "component_matrix": OUT / "P8_Y5_R2FR_3365_DELTAGM_COMPONENT_MATRIX.csv",
    "bound_status": OUT / "P8_Y5_R2FR_3365_DELTAGM_BOUND_STATUS.csv",
    "runner": OUT / "P8_Y5_R2FR_3365_DELTAGM_RUNNER_NONCLAIM.csv",
    "gates": OUT / "P8_Y5_R2FR_3365_PROMOTION_GATES.csv",
    "decision": OUT / "P8_Y5_R2FR_3365_DECISION_LEDGER.csv",
    "next": OUT / "P8_Y5_R2FR_3365_NEXT_TARGET.csv",
    "validation": OUT / "P8_Y5_BRR545_3365_VALIDATION.csv",
}


def bool_str(value: bool) -> str:
    return "true" if value else "false"


def compact(value: Any, limit: int = 1800) -> str:
    text = " ".join(str(value).split())
    return text if len(text) <= limit else text[: limit - 3] + "..."


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        path.write_text("", encoding="utf-8")
        return
    fieldnames: list[str] = []
    for row in rows:
        for key in row:
            if key not in fieldnames:
                fieldnames.append(key)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow({key: compact(row.get(key, "")) for key in fieldnames})


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def parseable(path: Path) -> bool:
    try:
        if path.suffix.lower() == ".csv":
            read_csv(path)
        else:
            path.read_text(encoding="utf-8")
        return True
    except Exception:
        return False


def table(rows: list[dict[str, Any]]) -> str:
    if not rows:
        return "_No rows._\n"
    headers: list[str] = []
    for row in rows:
        for key in row:
            if key not in headers:
                headers.append(key)
    lines = [
        "| " + " | ".join(headers) + " |",
        "| " + " | ".join("---" for _ in headers) + " |",
    ]
    for row in rows:
        lines.append("| " + " | ".join(compact(row.get(key, ""), 260).replace("|", "\\|") for key in headers) + " |")
    return "\n".join(lines) + "\n"


def local_source_rows() -> list[dict[str, Any]]:
    return [
        {
            "source_id": source_id,
            "path": str(path),
            "exists": bool_str(path.exists()),
            "parseable": bool_str(path.exists() and parseable(path)),
            "usage": usage,
            "valid_for_claim": "false",
        }
        for source_id, path, usage in LOCAL_SOURCES
    ]


def split_theorem_rows() -> list[dict[str, Any]]:
    return [
        {
            "theorem_id": "DGM3365_0_observed_GM_split",
            "statement": "Observed Newtonian GM splits into one allowed common calibration and a vector of observable residuals.",
            "math_form": "mu_obs = G_ref M_H (1 + eps_common) + G_ref M_H * eps_obs_vector",
            "result": "EXACT_DECOMPOSITION",
            "use": "prevents a universal fitted GM constant from hiding time, range, species, frame, non-EH, or boundary physics",
            "claim_status": "nonclaim_split",
            "valid_for_claim": "false",
        },
        {
            "theorem_id": "DGM3365_1_common_calibration_degeneracy",
            "statement": "A source-blind constant monopole is degenerate with the definition of G_ref M_H at first Newtonian order.",
            "math_form": "G_ref M_H(1+eps0)/r^2 = G'_ref M'_H/r^2 if eps0 is universal and derivative-silent",
            "result": "EXACT_FIRST_ORDER_DEGENERACY",
            "use": "local GR reduction does not require deriving the numerical value of a universal constant G, but does require proving no nonconstant/source-dependent leftovers",
            "claim_status": "allowed_parameter_not_derived_constant",
            "valid_for_claim": "false",
        },
        {
            "theorem_id": "DGM3365_2_observable_residual_rule",
            "statement": "Any species, time, range, radial, frame, boundary, non-EH, or second-order PPN dependence is observable and cannot be absorbed into calibrated GM.",
            "math_form": "eps_obs_vector = {eps_species, dot eps_time, eps_range(lambda), partial_r eps, eps_frame, eps_nonEH, eps_boundary, eps_symp, eps_PPN2}",
            "result": "EXACT_NO_ABSORPTION_RULE",
            "use": "turns DeltaGM into component rows instead of one vague source-normalization blocker",
            "claim_status": "policy_theorem",
            "valid_for_claim": "false",
        },
        {
            "theorem_id": "DGM3365_3_total_bound_not_scalar_yet",
            "statement": "There is not yet a single meaningful total DeltaGM scalar bound because the live pieces have different arena maps and units.",
            "math_form": "epsilon_total cannot combine dimensionless WEP, yr^-1 dotG, alpha(lambda), PPN coefficients, and mass-charge offsets without arena kernels",
            "result": "RUNNER_REFUSAL_THEOREM",
            "use": "forces componentwise bounds/theorems before local GR/Newton promotion",
            "claim_status": "no_total_bound_claim",
            "valid_for_claim": "false",
        },
        {
            "theorem_id": "DGM3365_4_promotion_condition",
            "statement": "The source-normalized Newton branch can be promoted only if common calibration is fixed/allowed and every observable residual row is theorem-zero or source-backed below its arena gate.",
            "math_form": "eps_common universal + for all i in obs_vector: eps_i=0 or |Pi_arena eps_i| <= bound_i",
            "result": "PROMOTION_CONTRACT_DERIVED",
            "use": "gives a concrete pass/fail contract for the Y5 source-mass side",
            "claim_status": "contract_not_satisfied",
            "valid_for_claim": "false",
        },
    ]


def component_matrix_rows() -> list[dict[str, Any]]:
    return [
        {
            "component_id": "DGMC3365_0_common_constant",
            "symbol": "eps_common",
            "meaning": "universal absolute calibration offset in G_ref M_H",
            "classification": "harmless_only_if_parent_fixed_universal_constant",
            "current_status": "CONDITIONAL_NOT_PARENT_FIXED",
            "observable_gate": "derivative/species/range/frame silence plus fixed reference",
            "fallback": "retain epsilon_calibration as closure parameter",
            "valid_for_claim": "false",
        },
        {
            "component_id": "DGMC3365_1_species_source_weight",
            "symbol": "eps_species_AB or Delta_w_AB",
            "meaning": "composition/species dependent source normalization",
            "classification": "observable_WEP_source_residual",
            "current_status": "SOURCE_BACKED_EXTERNAL_BOUND_NONCLAIM",
            "observable_gate": "|Delta_w_TiPt| <= 2.8e-15 only after tau_WEP/source-readout map",
            "fallback": "3363 MICROSCOPE row",
            "valid_for_claim": "false",
        },
        {
            "component_id": "DGMC3365_2_time_drift",
            "symbol": "d_t ln mu_obs",
            "meaning": "time drift of G_eff M_eff or source normalization",
            "classification": "observable_orbital_clock_residual",
            "current_status": "SOURCE_BACKED_COMPARATOR_NONCLAIM",
            "observable_gate": "|dotG/G| < 4e-14 yr^-1 comparator; internal local lock target 9.6e-15 yr^-1 remains unmet",
            "fallback": "MESSENGER/dotG row plus source-mass/readout disentanglement",
            "valid_for_claim": "false",
        },
        {
            "component_id": "DGMC3365_3_radial_range_hair",
            "symbol": "partial_r ln mu_obs or alpha(lambda)",
            "meaning": "range-dependent or radial finite-force source normalization tail",
            "classification": "observable_R10_or_orbital_residual",
            "current_status": "ANCHOR_ONLY_R10_NONCLAIM",
            "observable_gate": "alpha(lambda) full curve or parent no-hair theorem required",
            "fallback": "Eot-Wash alpha=1 at 38.6 microm anchor only",
            "valid_for_claim": "false",
        },
        {
            "component_id": "DGMC3365_4_nonEH_charge",
            "symbol": "R_nonEH_charge",
            "meaning": "non-EH curvature/operator contribution to source charge",
            "classification": "observable_PPN_R10_R11_residual",
            "current_status": "MISSING_COEFFICIENT_VECTOR",
            "observable_gate": "EH-only theorem or coefficient vector with gamma/beta/R10 maps",
            "fallback": "R11 non-EH operator vector",
            "valid_for_claim": "false",
        },
        {
            "component_id": "DGMC3365_5_symplectic_reference",
            "symbol": "R_symp_reference",
            "meaning": "nonintegrable/reference/counterterm source charge shift",
            "classification": "observable_boundary_reference_residual",
            "current_status": "MISSING_INTEGRABILITY_AND_REFERENCE_OWNER",
            "observable_gate": "fixed H_ref and integrable Hamiltonian charge",
            "fallback": "symplectic/reference residual row",
            "valid_for_claim": "false",
        },
        {
            "component_id": "DGMC3365_6_extra_projector_boundary",
            "symbol": "R_extra + R_projector + R_boundary",
            "meaning": "memory/projector/domain/boundary independent mass-channel charge",
            "classification": "observable_extra_mass_projection",
            "current_status": "MISSING_NOHAIR_OR_NUMERIC_PRODUCTS",
            "observable_gate": "topological/no-hair/no-flux theorem or product bounds",
            "fallback": "boundary/domain/projector source-normalization rows",
            "valid_for_claim": "false",
        },
        {
            "component_id": "DGMC3365_7_time_frame",
            "symbol": "R_time_frame",
            "meaning": "source time, charge time, clock time, orbital time, or MTS traversal parameter mismatch",
            "classification": "observable_frame_clock_orbital_residual",
            "current_status": "NOT_SIGNED",
            "observable_gate": "tau_source=tau_charge=tau_clock=tau_orbit=tau_pub",
            "fallback": "frame/readout residual row",
            "valid_for_claim": "false",
        },
        {
            "component_id": "DGMC3365_8_worldtube_support",
            "symbol": "R_worldtube_support",
            "meaning": "source support/linking surface changes after readout",
            "classification": "observable_source_worldtube_residual",
            "current_status": "MISSING_FIXED_SUPPORT_THEOREM",
            "observable_gate": "W_source fixed by Hilbert support before orbital fit",
            "fallback": "worldtube/source support residual row",
            "valid_for_claim": "false",
        },
        {
            "component_id": "DGMC3365_9_second_order_PPN",
            "symbol": "Delta_GM_PPN, gamma-1, beta-1",
            "meaning": "first-order GM normalization may pass while second-order source stability fails",
            "classification": "observable_PPN_residual",
            "current_status": "MISSING_COMPONENT_INPUTS",
            "observable_gate": "gamma=1 and beta=1 after source normalization",
            "fallback": "PPN residual vector",
            "valid_for_claim": "false",
        },
    ]


def bound_status_rows() -> list[dict[str, Any]]:
    return [
        {
            "bound_id": "DGB3365_0_WEP_species",
            "component": "DGMC3365_1_species_source_weight",
            "external_bound": f"{WEP_BOUND:.12e}",
            "units": "dimensionless",
            "source": "MICROSCOPE Ti/Pt 3363 row",
            "source_backed": "true",
            "projection_ready": "false",
            "why_not_claim": "tau_WEP/source-readout/no-prefactor grammar unsigned",
            "valid_for_component_bound": "true",
            "valid_for_claim": "false",
        },
        {
            "bound_id": "DGB3365_1_dotG_time",
            "component": "DGMC3365_2_time_drift",
            "external_bound": f"{DOTG_BOUND:.12e}",
            "units": "yr^-1",
            "source": "MESSENGER dotG comparator",
            "source_backed": "true",
            "projection_ready": "false",
            "why_not_claim": "dotG/G is not equal to parent kappa drift until source mass/readout/frame terms are zeroed",
            "valid_for_component_bound": "true",
            "valid_for_claim": "false",
        },
        {
            "bound_id": "DGB3365_2_R10_anchor",
            "component": "DGMC3365_3_radial_range_hair",
            "external_bound": "alpha=1 at lambda=3.86e-5 m",
            "units": "dimensionless_at_length_anchor",
            "source": "Eot-Wash 2020 anchor rows",
            "source_backed": "true_anchor_only",
            "projection_ready": "false",
            "why_not_claim": "not a full alpha(lambda) curve and no MTS alpha projection",
            "valid_for_component_bound": "anchor_only",
            "valid_for_claim": "false",
        },
        {
            "bound_id": "DGB3365_3_common_constant",
            "component": "DGMC3365_0_common_constant",
            "external_bound": "not_observable_as_first_order_Newtonian_scalar",
            "units": "dimensionless",
            "source": "calibration degeneracy theorem",
            "source_backed": "theorem_internal",
            "projection_ready": "conditional",
            "why_not_claim": "parent-fixed universal constant not signed",
            "valid_for_component_bound": "policy_only",
            "valid_for_claim": "false",
        },
        {
            "bound_id": "DGB3365_4_remaining_total",
            "component": "DGMC3365_4_to_DGMC3365_9",
            "external_bound": "MISSING_COMPONENT_BOUNDS",
            "units": "mixed",
            "source": "source mass/R11/PPN ledgers",
            "source_backed": "false",
            "projection_ready": "false",
            "why_not_claim": "non-EH, symplectic, boundary/projector, frame, worldtube, and PPN source rows are unbounded",
            "valid_for_component_bound": "false",
            "valid_for_claim": "false",
        },
    ]


def runner_rows() -> list[dict[str, Any]]:
    return [
        {
            "run_id": "DGRUN3365_0_common_constant_absorption_smoke",
            "input_case": "eps_common=0.1, all observable residuals zero",
            "runner_result": "FIRST_ORDER_NEWTON_DEGENERATE_NONCLAIM",
            "reason": "a universal source-blind constant can be reabsorbed into G_ref M_H at first Newtonian order",
            "local_GR_effect": "not a failure if parent-fixed and derivative/species/range/frame silent",
            "valid_for_claim": "false",
        },
        {
            "run_id": "DGRUN3365_1_species_bound_smoke",
            "input_case": "eps_species_TiPt=1.4e-15",
            "runner_result": "PASS_WEP_COMPONENT_SMOKE_NONCLAIM",
            "reason": "toy value is below 2.8e-15 but lacks MTS parent/tau projection",
            "local_GR_effect": "nonclaim",
            "valid_for_claim": "false",
        },
        {
            "run_id": "DGRUN3365_2_species_fail_smoke",
            "input_case": "eps_species_TiPt=5.6e-15",
            "runner_result": "FAIL_WEP_COMPONENT_SMOKE_NONCLAIM",
            "reason": "toy value exceeds 2.8e-15 component target",
            "local_GR_effect": "would fail if this were a real parent coefficient and tau_WEP=1",
            "valid_for_claim": "false",
        },
        {
            "run_id": "DGRUN3365_3_total_scalar_refusal",
            "input_case": "ask for one DeltaGM_total pass/fail number",
            "runner_result": "REFUSE_TOTAL_SCALAR_BOUND",
            "reason": "live rows mix dimensionless WEP, yr^-1 time drift, alpha(lambda), PPN coefficients, and mass-charge offsets; no common arena kernel",
            "local_GR_effect": "must score componentwise or derive zero",
            "valid_for_claim": "false",
        },
        {
            "run_id": "DGRUN3365_4_real_MTS_row_refusal",
            "input_case": "real source-normalized local GR claim",
            "runner_result": "REFUSE_MISSING_COMPONENT_INPUTS",
            "reason": "R_nonEH/R_symp/R_extra/R_boundary/R_time_frame/R_worldtube/PPN source rows are not zeroed or bounded",
            "local_GR_effect": "no source-normalized Newton/local-GR promotion",
            "valid_for_claim": "false",
        },
    ]


def promotion_gate_rows() -> list[dict[str, Any]]:
    return [
        {
            "gate_id": "GATE3365_0_DeltaGM_split_theorem",
            "claim": "DeltaGM is split into common calibration and observable residual vector",
            "passed": "true",
            "reason": "exact decomposition and no-absorption rule are stated",
            "valid_for_claim": "false",
        },
        {
            "gate_id": "GATE3365_1_common_constant_parent_fixed",
            "claim": "common constant calibration is parent-fixed and harmless",
            "passed": "false",
            "reason": "universal constant is allowed in principle but not parent-fixed in current corpus",
            "valid_for_claim": "false",
        },
        {
            "gate_id": "GATE3365_2_all_observable_components_zero_or_bounded",
            "claim": "all observable DeltaGM components are zero or source-backed below arena gates",
            "passed": "false",
            "reason": "only WEP and dotG comparator rows plus R10 anchor exist; most mass-charge rows are missing",
            "valid_for_claim": "false",
        },
        {
            "gate_id": "GATE3365_3_total_DeltaGM_scalar_bound",
            "claim": "a single total DeltaGM scalar bound is available",
            "passed": "false",
            "reason": "component units/arena kernels differ and cannot be summed honestly",
            "valid_for_claim": "false",
        },
        {
            "gate_id": "GATE3365_4_source_normalized_Newton",
            "claim": "source-normalized Newtonian branch is claim-ready",
            "passed": "false",
            "reason": "source mass lock and observable residual vector remain open",
            "valid_for_claim": "false",
        },
        {
            "gate_id": "GATE3365_5_local_GR_claim",
            "claim": "local GR branch is claim-ready",
            "passed": "false",
            "reason": "even if first-order common GM is calibrated, PPN/R11/source-mass components are not closed",
            "valid_for_claim": "false",
        },
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        {
            "decision_id": "DEC3365_0",
            "question": "Did 3365 bound total DeltaGM?",
            "answer": "no single total scalar bound is honest yet",
            "reason": "the live source-mass pieces have different observables and units; they must be componentwise theorem-zero or bounded",
            "next_action": "choose either WEP live projection acquisition or source-mass component theorem/bound rows",
            "valid_for_claim": "false",
        },
        {
            "decision_id": "DEC3365_1",
            "question": "Did 3365 reduce the fog?",
            "answer": "yes",
            "reason": "common calibration is separated from observable species/time/range/frame/non-EH/boundary/PPN residuals",
            "next_action": "stop treating fitted GM as a magic pass or fail; use the component matrix",
            "valid_for_claim": "false",
        },
        {
            "decision_id": "DEC3365_2",
            "question": "What is the best next practical route?",
            "answer": "WEP projection is the cleanest quantitative route; DeltaGM mass-charge rows are the deeper Newton route",
            "reason": "3363 already has a tight WEP number, while total source mass components still lack live coefficients",
            "next_action": "3366 should either acquire/refuse WEP projection files or build the first non-EH/boundary source-mass component row",
            "valid_for_claim": "false",
        },
    ]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        {
            "target_id": "3366-Y5-R2FR-WEP-live-projection-file-acquisition-or-refusal-under-AX1090.md",
            "target_script": "scripts/Y5_R2FR_3366_WEP_live_projection_file_acquisition_or_refusal.py",
            "objective": "acquire or formally refuse the live C_parent, R_source, R_material, K_CMSM and tau_WEP files needed to turn the 3363 MICROSCOPE bound into an executable MTS projection row",
            "why_next": "WEP is the tightest existing numeric source-normalization bound, but it cannot score until the projection is real",
            "valid_for_claim": "false",
        },
        {
            "target_id": "3367-Y5-R2FR-first-DeltaGM-mass-charge-component-row-under-AX1090.md",
            "target_script": "scripts/Y5_R2FR_3367_first_DeltaGM_mass_charge_component_row.py",
            "objective": "pick the first total-source-mass component among R_nonEH, R_symp, R_extra, R_boundary, R_time_frame, or R_worldtube and derive a zero theorem or source-backed numeric row",
            "why_next": "source-normalized Newton needs total source mass closure, not only relative WEP/source-weight bounds",
            "valid_for_claim": "false",
        },
    ]


def validation_rows() -> list[dict[str, Any]]:
    output_paths = [path for key, path in OUTPUTS.items() if key != "validation"]
    sources = local_source_rows()
    split = split_theorem_rows()
    components = component_matrix_rows()
    bounds = bound_status_rows()
    runner = runner_rows()
    gates = promotion_gate_rows()
    next_rows = next_target_rows()
    checks: list[dict[str, Any]] = []

    def add(check_id: str, check: str, passed: bool, detail: str = "") -> None:
        checks.append({"check_id": check_id, "check": check, "passed": bool_str(passed), "detail": detail})

    add("VAL3365_0_local_sources_exist", "all cited local source paths exist", all(row["exists"] == "true" for row in sources))
    add("VAL3365_1_local_sources_parse", "all cited local source paths parse", all(row["parseable"] == "true" for row in sources))
    add("VAL3365_2_outputs_parse", "all 3365 non-validation outputs parse", all(path.exists() and parseable(path) for path in output_paths))
    add(
        "VAL3365_3_split_theorem_complete",
        "split theorem includes decomposition, common calibration, no-absorption rule, total-bound refusal, and promotion condition",
        {row["theorem_id"] for row in split}
        == {
            "DGM3365_0_observed_GM_split",
            "DGM3365_1_common_calibration_degeneracy",
            "DGM3365_2_observable_residual_rule",
            "DGM3365_3_total_bound_not_scalar_yet",
            "DGM3365_4_promotion_condition",
        },
    )
    add(
        "VAL3365_4_component_coverage",
        "component matrix covers common, species, time, range, nonEH, symplectic, extra/boundary, frame, worldtube, and PPN",
        {row["component_id"] for row in components}
        == {
            "DGMC3365_0_common_constant",
            "DGMC3365_1_species_source_weight",
            "DGMC3365_2_time_drift",
            "DGMC3365_3_radial_range_hair",
            "DGMC3365_4_nonEH_charge",
            "DGMC3365_5_symplectic_reference",
            "DGMC3365_6_extra_projector_boundary",
            "DGMC3365_7_time_frame",
            "DGMC3365_8_worldtube_support",
            "DGMC3365_9_second_order_PPN",
        },
    )
    add(
        "VAL3365_5_source_backed_bounds_retained_nonclaim",
        "bound status includes WEP and dotG source-backed rows while keeping them nonclaim",
        any(row["bound_id"] == "DGB3365_0_WEP_species" and row["source_backed"] == "true" and row["valid_for_claim"] == "false" for row in bounds)
        and any(row["bound_id"] == "DGB3365_1_dotG_time" and row["source_backed"] == "true" and row["valid_for_claim"] == "false" for row in bounds),
    )
    add(
        "VAL3365_6_total_scalar_refused",
        "runner refuses a single total DeltaGM scalar bound",
        any(row["runner_result"] == "REFUSE_TOTAL_SCALAR_BOUND" for row in runner),
    )
    add(
        "VAL3365_7_no_overclaim",
        "common parent-fixed, all components bounded, total scalar bound, Newton and local GR gates remain false",
        all(
            row["passed"] == "false"
            for row in gates
            if row["gate_id"]
            in {
                "GATE3365_1_common_constant_parent_fixed",
                "GATE3365_2_all_observable_components_zero_or_bounded",
                "GATE3365_3_total_DeltaGM_scalar_bound",
                "GATE3365_4_source_normalized_Newton",
                "GATE3365_5_local_GR_claim",
            }
        )
        and all(row["valid_for_claim"] == "false" for row in split + components + bounds + runner + gates),
    )
    add(
        "VAL3365_8_next_targets_projection_and_mass_component",
        "next targets cover WEP live projection and first DeltaGM mass-charge component row",
        any("WEP-live-projection" in row["target_id"] for row in next_rows)
        and any("first-DeltaGM-mass-charge-component" in row["target_id"] for row in next_rows),
    )
    add(
        "VAL3365_9_write_scope_outside_formalization",
        "all 3365 write targets are outside formalization-workbench",
        all(FW not in path.parents and path != FW for path in [DOC, *output_paths, OUTPUTS["validation"]]),
        "write_targets=" + str(len([DOC, *output_paths, OUTPUTS["validation"]])),
    )
    overall = all(row["passed"] == "true" for row in checks)
    add("VAL3365_10_overall", "3365 validation overall", overall, "all required checks passed" if overall else "one or more checks failed")
    return checks


def write_doc(
    sources: list[dict[str, Any]],
    split: list[dict[str, Any]],
    components: list[dict[str, Any]],
    bounds: list[dict[str, Any]],
    runner: list[dict[str, Any]],
    gates: list[dict[str, Any]],
    decisions: list[dict[str, Any]],
    next_rows: list[dict[str, Any]],
    validations: list[dict[str, Any]],
) -> None:
    sections = [
        "# 3365 - DeltaGM Extra-Mass Projection Bound Row Under AX1090",
        "",
        f"Generated: `{RUN_UTC}`",
        "",
        "## Summary",
        "- This checkpoint attacks the total measured-GM/source-mass side of Y5.",
        "- Real gain: `DeltaGM` is split into a harmless-only-if-universal common calibration and observable residuals: species, time drift, range/radial hair, frame/readout, non-EH charge, boundary/projector/extra mass, worldtube support, and PPN second-order source stability.",
        "- Important derivation: a universal constant `G_ref M_H` offset is first-order Newton-degenerate, so local GR reduction does not require computing the numerical value of `G`; it does require proving that no derivative/source/range/frame residual survives.",
        "- Existing real bounds are componentwise only: MICROSCOPE gives a WEP/source-weight target, MESSENGER gives a dotG comparator, and R10 has an anchor-only alpha row. These cannot be honestly summed into one `DeltaGM_total` scalar.",
        "- No Newton/local-GR claim is promoted; next useful work is either making the WEP projection executable or filling the first total-source-mass component row.",
        "",
        "## Local Source Register",
        table(sources),
        "## DeltaGM Split Theorem",
        table(split),
        "## DeltaGM Component Matrix",
        table(components),
        "## DeltaGM Bound Status",
        table(bounds),
        "## DeltaGM Runner Nonclaim",
        table(runner),
        "## Promotion Gates",
        table(gates),
        "## Decision Ledger",
        table(decisions),
        "## Next Target",
        table(next_rows),
        "## Validation",
        table(validations),
    ]
    DOC.write_text("\n".join(sections), encoding="utf-8")


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    rows_by_output = {
        "local_sources": local_source_rows(),
        "split_theorem": split_theorem_rows(),
        "component_matrix": component_matrix_rows(),
        "bound_status": bound_status_rows(),
        "runner": runner_rows(),
        "gates": promotion_gate_rows(),
        "decision": decision_rows(),
        "next": next_target_rows(),
    }
    for key, rows in rows_by_output.items():
        write_csv(OUTPUTS[key], rows)
    validations = validation_rows()
    write_csv(OUTPUTS["validation"], validations)
    write_doc(
        rows_by_output["local_sources"],
        rows_by_output["split_theorem"],
        rows_by_output["component_matrix"],
        rows_by_output["bound_status"],
        rows_by_output["runner"],
        rows_by_output["gates"],
        rows_by_output["decision"],
        rows_by_output["next"],
        validations,
    )
    if PYCACHE.exists():
        shutil.rmtree(PYCACHE)


if __name__ == "__main__":
    main()

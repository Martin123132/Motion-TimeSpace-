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
DOC = ROOT / "3380-Y5-R2FR-parent-type-system-or-source-prefactor-bound-acquisition-under-AX1090.md"
RUN_UTC = datetime.now(timezone.utc).isoformat()

OUTPUTS = {
    "source_register": OUT / "P8_Y5_R2FR_3380_SOURCE_REGISTER.csv",
    "object_language": OUT / "P8_Y5_R2FR_3380_PARENT_OBJECT_LANGUAGE.csv",
    "formation_rules": OUT / "P8_Y5_R2FR_3380_ACTION_FORMATION_RULES.csv",
    "type_theorem": OUT / "P8_Y5_R2FR_3380_TYPE_SYSTEM_THEOREM_ATTEMPT.csv",
    "homset_firewall": OUT / "P8_Y5_R2FR_3380_FORBIDDEN_HOMSET_FIREWALL.csv",
    "bound_matrix": OUT / "P8_Y5_R2FR_3380_SOURCE_PREFACTOR_BOUND_ACQUISITION_MATRIX.csv",
    "component_rows": OUT / "P8_Y5_R2FR_3380_SOURCE_PREF_COMPONENT_ROWS_NONCLAIM.csv",
    "arena_requirements": OUT / "P8_Y5_R2FR_3380_ARENA_PROJECTION_REQUIREMENTS.csv",
    "countermodel_map": OUT / "P8_Y5_R2FR_3380_COUNTERMODEL_SURVIVOR_MAP.csv",
    "runner": OUT / "P8_Y5_R2FR_3380_RUNNER_NONCLAIM.csv",
    "gates": OUT / "P8_Y5_R2FR_3380_PROMOTION_GATES.csv",
    "decision": OUT / "P8_Y5_R2FR_3380_DECISION_LEDGER.csv",
    "next": OUT / "P8_Y5_R2FR_3380_NEXT_TARGET.csv",
    "validation": OUT / "P8_Y5_BRR545_3380_VALIDATION.csv",
}

LOCAL_SOURCES = [
    ("SRC3380_0_3379_doc", ROOT / "3379-Y5-R2FR-parent-action-adoption-no-extension-or-source-prefactor-bound-under-AX1090.md", "3379 adoption/no-extension handoff"),
    ("SRC3380_1_3379_next", OUT / "P8_Y5_R2FR_3379_NEXT_TARGET.csv", "3379 selected parent type-system target"),
    ("SRC3380_2_3379_theorem", OUT / "P8_Y5_R2FR_3379_PARENT_ACTION_ADOPTION_NO_EXTENSION_THEOREM.csv", "3379 conditional no-source-prefactor theorem"),
    ("SRC3380_3_3379_bound_rows", OUT / "P8_Y5_R2FR_3379_SOURCE_PREF_MARKER_BOUND_ROWS_NONCLAIM.csv", "3379 retained finite residual rows"),
    ("SRC3380_4_3379_countermodels", OUT / "P8_Y5_R2FR_3379_SURVIVING_COUNTERMODEL_LEDGER.csv", "3379 surviving countermodels"),
    ("SRC3380_5_3378_action_line", OUT / "P8_Y5_R2FR_3378_MINIMAL_PARENT_ACTION_LINE.csv", "3378 minimal parent action line"),
    ("SRC3380_6_3377_kappa", OUT / "P8_Y5_R2FR_3377_WEAK_FIELD_SOURCE_NORMALIZATION_THEOREM.csv", "3377 weak-field source normalization"),
    ("SRC3380_7_3364_microscope_status", OUT / "P8_Y5_R2FR_3364_MICROSCOPE_BOUND_STATUS_UPDATE.csv", "MICROSCOPE source-prefactor status"),
    ("SRC3380_8_3260_microscope_inputs", OUT / "P8_Y5_R2FR_3260_MICROSCOPE_DD_BOUND_INPUTS.csv", "MICROSCOPE bound numerical source intake"),
    ("SRC3380_9_3166_cassini", OUT / "P8_Y5_R2FR_3166_CASSINI_GAMMA_SOURCE_INTAKE.csv", "Cassini PPN gamma source intake"),
    ("SRC3380_10_3012_r10", OUT / "P8_Y5_R2FR_3012_R10_BOUND_ROWS_NONCLAIM.csv", "R10 alpha-lambda bound source/anchor ledger"),
    ("SRC3380_11_2702_r10_contract", OUT / "P8_Y5_R2FR_2702_R10_BOUND_CURVE_DIGITIZATION_CONTRACT.csv", "R10 full-curve acquisition contract"),
    ("SRC3380_12_2675_clock", OUT / "P8_Y5_R2FR_2675_SPECIES_CLOCK_FIRST_BOUND_FILL_NONCLAIM.csv", "clock/species source-prefactor nonclaim fill"),
]

BAD_STATUS_TOKENS = (
    "MISSING",
    "NOT_DERIVED",
    "NOT_PROVED",
    "NOT_SIGNED",
    "NOT_PARENT",
    "UNSIGNED",
    "CONDITIONAL",
    "COUNTERMODEL",
    "SURVIVES",
    "LIVE",
    "NONCLAIM",
    "FALSE",
    "FAIL",
    "OPEN",
    "BLOCKED",
)


def bool_text(value: bool) -> str:
    return "true" if value else "false"


def parse_csv(path: Path) -> tuple[bool, str]:
    try:
        with path.open("r", encoding="utf-8-sig", newline="") as handle:
            list(csv.DictReader(handle))
        return True, ""
    except Exception as exc:  # noqa: BLE001
        return False, f"{type(exc).__name__}: {exc}"


def parse_text(path: Path) -> tuple[bool, str]:
    try:
        path.read_text(encoding="utf-8", errors="replace")
        return True, ""
    except Exception as exc:  # noqa: BLE001
        return False, f"{type(exc).__name__}: {exc}"


def read_csv_rows(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    headers: list[str] = []
    for row in rows:
        for key in row:
            if key not in headers:
                headers.append(key)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=headers)
        writer.writeheader()
        writer.writerows(rows)


def md_escape(value: Any) -> str:
    return str(value).replace("|", "\\|").replace("\n", "<br>")


def md_table(rows: list[dict[str, Any]]) -> str:
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
        lines.append("| " + " | ".join(md_escape(row.get(header, "")) for header in headers) + " |")
    return "\n".join(lines) + "\n"


def source_rows() -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    for source_id, path, role in LOCAL_SOURCES:
        exists = path.exists()
        if not exists:
            parse_ok, parse_error = False, "missing"
        elif path.suffix.lower() == ".csv":
            parse_ok, parse_error = parse_csv(path)
        else:
            parse_ok, parse_error = parse_text(path)
        rows.append(
            {
                "source_id": source_id,
                "source_path": str(path),
                "exists": bool_text(exists),
                "parse_ok": bool_text(parse_ok),
                "role": role,
                "parse_error": parse_error,
                "valid_for_claim": "false",
            }
        )
    return rows


def object_language_rows() -> list[dict[str, str]]:
    return [
        {
            "object_id": "OBJ3380_0_parent_configuration",
            "sort": "Conf_parent",
            "allowed_elements": "Phi=(M,T,S-sector fields, universal constants, gauge bundles, boundary/reference data fixed before variation)",
            "forbidden_elements": "source labels chosen after solving; readout-channel weights; fitted source masks",
            "purpose": "closed parent domain before action variation",
            "current_status": "CANDIDATE_GRAMMAR_NOT_PARENT_SIGNED",
            "valid_for_claim": "false",
        },
        {
            "object_id": "OBJ3380_1_observed_geometry",
            "sort": "Geom_obs",
            "allowed_elements": "q(Phi), e_obs(qPhi), g_obs=e_obs^T eta e_obs, nabla_obs, volume density dmu_obs",
            "forbidden_elements": "second source metric e_source=A(X)e_obs or disformal source frame not reducible to q(Phi)",
            "purpose": "single geometry seen by inertial motion and Hilbert source variation",
            "current_status": "STRUCTURAL_RULE_DEFINED",
            "valid_for_claim": "false",
        },
        {
            "object_id": "OBJ3380_2_matter_bundle",
            "sort": "Matter_A",
            "allowed_elements": "psi_A, representation rho_A, quotient-owned masses/charges/constants theta_A(qPhi), gauge connection A_obs",
            "forbidden_elements": "species-dependent active-source multipliers w_A(X) outside theta_A; hidden source charge not in rho_A",
            "purpose": "ordinary matter enters through one observed stack, not a separate source-coupling leg",
            "current_status": "STRUCTURAL_RULE_DEFINED",
            "valid_for_claim": "false",
        },
        {
            "object_id": "OBJ3380_3_universal_scale",
            "sort": "UniversalConst",
            "allowed_elements": "one common kappa_MTS or G_ref normalization; c as unit/cone constant; hbar if quantum sector is present",
            "forbidden_elements": "species/readout dependent kappa_A, kappa_H, kappa_W, kappa_source",
            "purpose": "permit GR/Newton normalization without relative source prefactors",
            "current_status": "ALLOWED_COMMON_MODE_ONLY",
            "valid_for_claim": "false",
        },
        {
            "object_id": "OBJ3380_4_readout_arena",
            "sort": "ReadoutObs",
            "allowed_elements": "post-solution maps to clocks, R10, PPN, orbital, SPARC, cosmology and EM observables",
            "forbidden_elements": "readout object reentering S_matter before Hilbert variation",
            "purpose": "separate prediction extraction from source definition",
            "current_status": "REENTRY_FIREWALL_DEFINED_NOT_DERIVED",
            "valid_for_claim": "false",
        },
        {
            "object_id": "OBJ3380_5_boundary_reference",
            "sort": "BoundaryRef",
            "allowed_elements": "source-blind fixed primitive/reference subtraction and zero-flux boundary class",
            "forbidden_elements": "source-dependent H_ref or B_ref that shifts active mass",
            "purpose": "prevent boundary bookkeeping from becoming a source scale",
            "current_status": "USES_3376_BOUNDARY_CONTRACT",
            "valid_for_claim": "false",
        },
    ]


def formation_rule_rows() -> list[dict[str, str]]:
    return [
        {
            "rule_id": "FORM3380_0_action_scalar_density",
            "formation_rule": "Action terms must be scalar densities constructed from Conf_parent objects before variation.",
            "consequence": "No coefficient can depend on a readout-only object or post-solution residual.",
            "breaks_if_missing": "readout reentry can manufacture source prefactors after the fact",
            "status": "REQUIRED_RULE",
            "valid_for_claim": "false",
        },
        {
            "rule_id": "FORM3380_1_single_measure",
            "formation_rule": "All ordinary matter actions use the same observed measure dmu_obs[q(Phi)].",
            "consequence": "A species-dependent measure or source frame is untypeable unless added as a new parent field.",
            "breaks_if_missing": "WEP-blind conformal/disformal source metrics survive",
            "status": "REQUIRED_RULE",
            "valid_for_claim": "false",
        },
        {
            "rule_id": "FORM3380_2_matter_functor",
            "formation_rule": "S_A has type S_A[psi_A; e_obs(qPhi), nabla_obs, A_obs, theta_A(qPhi), rho_A].",
            "consequence": "Allowed species differences are inertial/gauge/representation data, not active gravitational prefactors.",
            "breaks_if_missing": "w_A S_A remains a covariant action",
            "status": "REQUIRED_RULE",
            "valid_for_claim": "false",
        },
        {
            "rule_id": "FORM3380_3_common_source_normalization",
            "formation_rule": "The Hilbert source is T_munu=-(2/sqrt(-g_obs)) delta S_matter/delta g_obs^munu with one common kappa_MTS.",
            "consequence": "Newtonian G_ref is calibrated once, not per species/channel.",
            "breaks_if_missing": "kappa_A or a_W/a_H can alter active mass while preserving covariance",
            "status": "REQUIRED_RULE",
            "valid_for_claim": "false",
        },
        {
            "rule_id": "FORM3380_4_no_hidden_homsets",
            "formation_rule": "The grammar contains no Hom(SpeciesLabel, SourceScale), Hom(ReadoutChannel, SourceScale), Hom(HiddenInvariant, MatterWeight), or Hom(PostProjector, SourceCurrent).",
            "consequence": "source-only prefactors are not merely set to zero; they cannot be formed",
            "breaks_if_missing": "the same symbols return as legal residuals",
            "status": "EXACT_IF_PARENT_LANGUAGE_CLOSED",
            "valid_for_claim": "false",
        },
        {
            "rule_id": "FORM3380_5_no_extension_by_absence",
            "formation_rule": "Absence of a term is evidence only if the parent object language proves no legal constructor for it.",
            "consequence": "the route avoids smuggling a plateau/closure axiom",
            "breaks_if_missing": "local GR is assumed rather than derived",
            "status": "PROJECT_DISCIPLINE_RULE",
            "valid_for_claim": "false",
        },
    ]


def type_theorem_rows() -> list[dict[str, str]]:
    return [
        {
            "theorem_id": "TTS3380_0_statement",
            "claim_piece": "parent type-system source universality theorem",
            "statement": "In the object language OBJ3380 with formation rules FORM3380, every well-typed ordinary matter contribution has one observed measure and one Hilbert source normalization; source-only weights w_A(X), kappa_A(X), readout-channel source factors and marker source functors are not constructible.",
            "proof_status": "EXACT_CONDITIONAL_STRUCTURAL_THEOREM",
            "proof_or_failure": "The theorem is by structural induction on action constructors: base constructors contain only q-owned geometry, matter bundle data and universal constants; product/sum/derivative/contraction/integration preserve the absence of SourceScale-valued Hom-sets; no rule introduces SpeciesLabel->SourceScale or Readout->SourceScale.",
            "residual_if_missing": "epsilon_source_pref_marker_abs",
            "valid_for_claim": "false",
        },
        {
            "theorem_id": "TTS3380_1_base_cases",
            "claim_piece": "base terms",
            "statement": "Kinetic, mass, gauge and interaction base terms are functions of psi_A, e_obs(qPhi), nabla_obs, A_obs, rho_A and theta_A(qPhi).",
            "proof_status": "PROVED_WITHIN_CANDIDATE_GRAMMAR",
            "proof_or_failure": "No base constructor returns a bare source scale, source mask or readout-channel multiplier.",
            "residual_if_missing": "Delta_w_AB;b_marker",
            "valid_for_claim": "false",
        },
        {
            "theorem_id": "TTS3380_2_induction_step",
            "claim_piece": "closure under allowed operations",
            "statement": "If terms t_i contain no active-source prefactor morphism, then sums, products, contractions, covariant derivatives with nabla_obs, gauge derivatives and integration over dmu_obs also contain none.",
            "proof_status": "PROVED_WITHIN_CANDIDATE_GRAMMAR",
            "proof_or_failure": "Allowed operations change tensor/scalar-density type only; they do not create new coefficient domains.",
            "residual_if_missing": "C_eff_source_tail",
            "valid_for_claim": "false",
        },
        {
            "theorem_id": "TTS3380_3_universal_constant_exception",
            "claim_piece": "common normalization exception",
            "statement": "A universal common multiplicative action scale is allowed only if it multiplies every matter sector identically and is absorbed into kappa_MTS/G_ref.",
            "proof_status": "EXACT_COMMON_MODE_EXCEPTION",
            "proof_or_failure": "A common scale commutes with Hilbert variation and changes only the global source normalization; relative source physics starts only at non-common weights.",
            "residual_if_missing": "G_ref_calibration_owner;Delta_w_AB",
            "valid_for_claim": "false",
        },
        {
            "theorem_id": "TTS3380_4_current_MTS_adoption",
            "claim_piece": "current corpus adoption",
            "statement": "Current MTS must derive OBJ3380/FORM3380 from its own motion-time-space primitives rather than choosing them as a repair grammar.",
            "proof_status": "NOT_PARENT_SIGNED",
            "proof_or_failure": "3379 proved Ward/Bianchi is insufficient, and 3380 still lacks a derivation that the MTS primitive language has exactly these objects and no legal extension.",
            "residual_if_missing": "E_no_extension_minimality",
            "valid_for_claim": "false",
        },
        {
            "theorem_id": "TTS3380_5_verdict",
            "claim_piece": "local-GR source coupling",
            "statement": "The source-coupling gap is sharpened from vague missing coupling to one adoption theorem: prove MTS forces OBJ3380/FORM3380, or retain finite bounded residuals.",
            "proof_status": "MAJOR_REDUCTION_NOT_FINAL_CLAIM",
            "proof_or_failure": "This is progress: the remaining coupling problem is no longer a bag of loose symbols, but a parent-language adoption problem plus named empirical residuals.",
            "residual_if_missing": "epsilon_source_pref_marker_abs",
            "valid_for_claim": "false",
        },
    ]


def homset_firewall_rows() -> list[dict[str, str]]:
    return [
        {
            "firewall_id": "HOM3380_0_species_weight",
            "forbidden_homset": "Hom(SpeciesLabel, SourceScale)",
            "kills_term": "w_A(X)S_A; kappa_A(X)T_A",
            "why_forbidden_in_candidate": "species labels classify matter bundle representations; they are not scalar fields or universal constants in Conf_parent",
            "survives_without_firewall": "pre-action weighted matter remains covariant and Ward-compatible",
            "bound_if_survives": "Delta_w_AB via WEP/MICROSCOPE/source-normalization",
            "status": "FORBIDDEN_CONDITIONALLY",
            "valid_for_claim": "false",
        },
        {
            "firewall_id": "HOM3380_1_readout_channel_weight",
            "forbidden_homset": "Hom(ReadoutChannel, SourceScale)",
            "kills_term": "a_W/a_H source-channel rescaling; epsilon_Wchan",
            "why_forbidden_in_candidate": "readout channels are post-solution maps, not parent action arguments",
            "survives_without_firewall": "different observational channels can calibrate different active masses",
            "bound_if_survives": "clock/orbit/PPN cross-calibration",
            "status": "FORBIDDEN_CONDITIONALLY",
            "valid_for_claim": "false",
        },
        {
            "firewall_id": "HOM3380_2_hidden_frame",
            "forbidden_homset": "Hom(HiddenInvariant, SourceMetric)",
            "kills_term": "e_source=A(X)e_obs; disformal source frame; c_g_b_dis",
            "why_forbidden_in_candidate": "all source variation is with respect to g_obs(qPhi); a second source metric is a new parent field",
            "survives_without_firewall": "WEP-blind common frame can pass species tests while shifting PPN/R10/clocks",
            "bound_if_survives": "Cassini gamma, R10 alpha(lambda), clock redshift/frequency comparisons",
            "status": "FORBIDDEN_CONDITIONALLY",
            "valid_for_claim": "false",
        },
        {
            "firewall_id": "HOM3380_3_marker_functor",
            "forbidden_homset": "Hom(MaterialMarker, MatterWeight)",
            "kills_term": "b_marker; b_alpha; isotope/material/preparation source functors",
            "why_forbidden_in_candidate": "material markers may enter theta_A only as inertial/gauge data, not as active source weights",
            "survives_without_firewall": "co-moving material constants can behave like hidden source labels",
            "bound_if_survives": "MICROSCOPE/composition tests and clock/fine-structure bounds",
            "status": "FORBIDDEN_CONDITIONALLY",
            "valid_for_claim": "false",
        },
        {
            "firewall_id": "HOM3380_4_post_projector_source",
            "forbidden_homset": "Hom(PostProjector, SourceCurrent)",
            "kills_term": "Pi_M source-tail selection after residual inspection",
            "why_forbidden_in_candidate": "Pi_M and arena projectors may extract observables but cannot alter the varied Hilbert source",
            "survives_without_firewall": "projection can hide non-Hilbert tails or tune active mass",
            "bound_if_survives": "C_eff_source_tail in PPN/R10/orbital/worldtube projections",
            "status": "FORBIDDEN_CONDITIONALLY",
            "valid_for_claim": "false",
        },
        {
            "firewall_id": "HOM3380_5_boundary_source_weight",
            "forbidden_homset": "Hom(SourceDomain, BoundaryReferenceScale)",
            "kills_term": "source-dependent H_ref/B_ref active-mass absorption",
            "why_forbidden_in_candidate": "boundary references are fixed before variation and source-blind",
            "survives_without_firewall": "GM can be shifted by reference subtraction instead of dynamics",
            "bound_if_survives": "orbital GM, local mass normalization, PPN source charge",
            "status": "FORBIDDEN_CONDITIONALLY",
            "valid_for_claim": "false",
        },
    ]


def first_value(path: Path, column: str, default: str = "not_available") -> str:
    for row in read_csv_rows(path):
        value = row.get(column, "").strip()
        if value:
            return value
    return default


def bound_matrix_rows() -> list[dict[str, str]]:
    microscope_status = OUT / "P8_Y5_R2FR_3364_MICROSCOPE_BOUND_STATUS_UPDATE.csv"
    microscope_inputs = OUT / "P8_Y5_R2FR_3260_MICROSCOPE_DD_BOUND_INPUTS.csv"
    cassini = OUT / "P8_Y5_R2FR_3166_CASSINI_GAMMA_SOURCE_INTAKE.csv"
    r10 = OUT / "P8_Y5_R2FR_3012_R10_BOUND_ROWS_NONCLAIM.csv"
    r10_contract = OUT / "P8_Y5_R2FR_2702_R10_BOUND_CURVE_DIGITIZATION_CONTRACT.csv"
    clock = OUT / "P8_Y5_R2FR_2675_SPECIES_CLOCK_FIRST_BOUND_FILL_NONCLAIM.csv"
    return [
        {
            "bound_id": "BND3380_0_Delta_w_AB_MICROSCOPE",
            "residual_symbol": "Delta_w_AB",
            "arena": "WEP/source species",
            "external_bound_or_anchor": first_value(microscope_status, "external_bound_abs", "2.8e-15"),
            "units": "dimensionless",
            "source_path": str(microscope_status),
            "source_status": "LOCAL_BOUND_ROW_VALID_BUT_MTS_PROJECTION_BLOCKED",
            "missing_mts_inputs": "parent type-system adoption; tau_WEP projection owner; no-cancellation rule",
            "valid_external_bound": "true",
            "valid_mts_prediction_row": "false",
            "valid_for_claim": "false",
        },
        {
            "bound_id": "BND3380_1_eta_TiPt_MICROSCOPE",
            "residual_symbol": "eta_TiPt_source_prefactor",
            "arena": "WEP/composition",
            "external_bound_or_anchor": first_value(microscope_inputs, "value", "-1.5e-15"),
            "units": "dimensionless central value plus uncertainties in source file",
            "source_path": str(microscope_inputs),
            "source_status": "NUMERIC_INPUTS_PRESENT_NONCLAIM",
            "missing_mts_inputs": "official sensitivity map; parent coefficients C_i; source-label zero theorem",
            "valid_external_bound": "true",
            "valid_mts_prediction_row": "false",
            "valid_for_claim": "false",
        },
        {
            "bound_id": "BND3380_2_cg_bdis_Cassini",
            "residual_symbol": "c_g_b_dis",
            "arena": "PPN_gamma",
            "external_bound_or_anchor": first_value(cassini, "abs_envelope_2sigma", "6.7e-05"),
            "units": "dimensionless gamma_minus_one envelope",
            "source_path": str(cassini),
            "source_status": "LOCAL_CASSINI_SOURCE_INTAKE_PRESENT",
            "missing_mts_inputs": "Pi_gamma projection; mapping from hidden frame coefficients to gamma",
            "valid_external_bound": "true",
            "valid_mts_prediction_row": "false",
            "valid_for_claim": "false",
        },
        {
            "bound_id": "BND3380_3_R10_alpha_lambda",
            "residual_symbol": "c_g_b_dis;C_eff_source_tail",
            "arena": "short_range_R10",
            "external_bound_or_anchor": f"alpha={first_value(r10, 'alpha_bound', '1.0')} at lambda={first_value(r10, 'lambda_value', '3.86e-5')} {first_value(r10, 'lambda_units', 'm')}",
            "units": "dimensionless alpha and metre lambda",
            "source_path": str(r10),
            "source_status": "ANCHOR_ONLY_NON_CURVE",
            "missing_mts_inputs": "full digitized alpha(lambda) curve; R10 projection; parent source coefficient",
            "valid_external_bound": "false",
            "valid_mts_prediction_row": "false",
            "valid_for_claim": "false",
        },
        {
            "bound_id": "BND3380_4_R10_full_curve_contract",
            "residual_symbol": "R10_curve_requirement",
            "arena": "short_range_R10",
            "external_bound_or_anchor": "full_curve_required",
            "units": "lambda in m; alpha dimensionless",
            "source_path": str(r10_contract),
            "source_status": "ACQUISITION_CONTRACT_PRESENT",
            "missing_mts_inputs": "dense curve/table or audited digitization; no interpolation from single anchor",
            "valid_external_bound": "false",
            "valid_mts_prediction_row": "false",
            "valid_for_claim": "false",
        },
        {
            "bound_id": "BND3380_5_clock_marker",
            "residual_symbol": "b_marker;b_alpha;epsilon_Wchan",
            "arena": "clock/fine-structure/species channel",
            "external_bound_or_anchor": first_value(clock, "comparison_bound_or_scale", "2.8e-15"),
            "units": "dimensionless scale from source file",
            "source_path": str(clock),
            "source_status": "NONCLAIM_FILL_PRESENT",
            "missing_mts_inputs": "clock transition sensitivities; parent coefficient owner; no-marker theorem",
            "valid_external_bound": "false",
            "valid_mts_prediction_row": "false",
            "valid_for_claim": "false",
        },
    ]


def component_rows() -> list[dict[str, str]]:
    return [
        {
            "component_id": "COMP3380_0_Delta_w_AB",
            "symbol": "Delta_w_AB",
            "definition": "relative species/source active gravitational prefactor after removing a universal common scale",
            "candidate_zero_route": "Hom(SpeciesLabel, SourceScale) absent in parent type-system",
            "bound_route": "MICROSCOPE/WEP composition differential acceleration",
            "current_status": "ZERO_ROUTE_CONDITIONAL_BOUND_ROUTE_NONCLAIM",
            "valid_for_claim": "false",
        },
        {
            "component_id": "COMP3380_1_epsilon_Wchan",
            "symbol": "epsilon_Wchan",
            "definition": "readout-channel active source prefactor residual",
            "candidate_zero_route": "ReadoutObs is post-solution only and cannot feed S_matter",
            "bound_route": "cross-channel clocks, orbital GM, PPN and local calibration",
            "current_status": "ZERO_ROUTE_CONDITIONAL_NUMERIC_MAP_MISSING",
            "valid_for_claim": "false",
        },
        {
            "component_id": "COMP3380_2_cg_bdis",
            "symbol": "c_g_b_dis",
            "definition": "common hidden conformal/disformal source-frame residual",
            "candidate_zero_route": "single observed geometry g_obs(qPhi) is the only Hilbert-variation metric",
            "bound_route": "Cassini gamma, R10 alpha(lambda), clock redshift, orbital precession",
            "current_status": "ZERO_ROUTE_CONDITIONAL_ARENA_MAP_MISSING",
            "valid_for_claim": "false",
        },
        {
            "component_id": "COMP3380_3_b_marker",
            "symbol": "b_marker",
            "definition": "material/isotope/constant marker sensitivity in active source coupling",
            "candidate_zero_route": "material labels remain inertial/gauge data, not SourceScale objects",
            "bound_route": "WEP plus clock/fine-structure marker sensitivity rows",
            "current_status": "ZERO_ROUTE_CONDITIONAL_SENSITIVITY_MAP_MISSING",
            "valid_for_claim": "false",
        },
        {
            "component_id": "COMP3380_4_C_eff_source_tail",
            "symbol": "C_eff_source_tail",
            "definition": "effective/radiative/readout reentry source coefficient outside parent grammar",
            "candidate_zero_route": "variation-before-readout firewall plus no post-projector source Hom-set",
            "bound_route": "PPN/R10/orbital residual vector with no-cancellation rule",
            "current_status": "ZERO_ROUTE_CONDITIONAL_EFFECTIVE_MAP_MISSING",
            "valid_for_claim": "false",
        },
        {
            "component_id": "COMP3380_5_epsilon_source_pref_marker_abs",
            "symbol": "epsilon_source_pref_marker_abs",
            "definition": "absolute envelope over all retained source prefactor, frame, marker and reentry residuals",
            "candidate_zero_route": "all HOM3380 firewalls parent-signed",
            "bound_route": "sum/envelope over WEP, PPN, R10, clock and orbital constraints",
            "current_status": "ENVELOPE_DEFINED_NUMERIC_PROJECTION_MISSING",
            "valid_for_claim": "false",
        },
    ]


def arena_requirement_rows() -> list[dict[str, str]]:
    return [
        {
            "arena_id": "ARENA3380_0_WEP",
            "arena": "MICROSCOPE/WEP",
            "required_projection": "eta_AB = Delta_w_AB + material marker terms + hidden source-frame differential terms, with no-cancellation policy",
            "current_input_status": "external bound present; MTS coefficient/projection missing",
            "claim_gate": "blocked until parent zero theorem or numeric C_i sensitivity map exists",
            "valid_for_claim": "false",
        },
        {
            "arena_id": "ARENA3380_1_PPN",
            "arena": "local PPN",
            "required_projection": "(gamma-1,beta-1,alpha_i,zeta_i,xi) as functions of c_g,b_dis,C_eff_source_tail,epsilon_Wchan",
            "current_input_status": "Cassini gamma source intake present only for one component",
            "claim_gate": "blocked until full vector map and source-prefactor guard exist",
            "valid_for_claim": "false",
        },
        {
            "arena_id": "ARENA3380_2_R10",
            "arena": "short-range inverse-square-law",
            "required_projection": "alpha_pred(lambda)=F[bulk/test/source beta legs, hidden-frame coefficients, support tails]",
            "current_input_status": "anchor rows exist; full bound curve and MTS prediction values missing",
            "claim_gate": "blocked until full alpha(lambda) curve and numeric parent coefficients exist",
            "valid_for_claim": "false",
        },
        {
            "arena_id": "ARENA3380_3_clocks",
            "arena": "clock/fine-structure/redshift",
            "required_projection": "frequency ratio/redshift residuals as functions of b_alpha,b_marker,c_g,b_dis and source-channel calibration",
            "current_input_status": "species-clock nonclaim fill exists; sensitivities/parent coefficients missing",
            "claim_gate": "blocked until transition sensitivity map and parent owner are sourced",
            "valid_for_claim": "false",
        },
        {
            "arena_id": "ARENA3380_4_orbital",
            "arena": "orbital/Newtonian GM",
            "required_projection": "GM_obs = G_ref M_Hilbert (1 + source-prefactor + boundary + projection residuals)",
            "current_input_status": "weak-field G_ref/kappa route conditional; source prefactor unresolved",
            "claim_gate": "blocked until source universal coupling or finite GM residual bound",
            "valid_for_claim": "false",
        },
    ]


def countermodel_map_rows() -> list[dict[str, str]]:
    return [
        {
            "countermodel_id": "CM3380_0_pre_action_weight",
            "3379_countermodel": "S_matter=sum_A w_A S_A",
            "3380_status": "KILLED_IF_HOM3380_0_SIGNED",
            "why_not_killed_now": "current corpus has not proved SpeciesLabel lacks a source-scale morphism",
            "repair": "derive parent object language from M/T/S primitives or keep Delta_w_AB bound",
            "valid_for_claim": "false",
        },
        {
            "countermodel_id": "CM3380_1_common_hidden_frame",
            "3379_countermodel": "e_source=A_g(X)e_obs",
            "3380_status": "KILLED_IF_HOM3380_2_SIGNED",
            "why_not_killed_now": "single observed geometry is a candidate rule, not yet forced by MTS",
            "repair": "prove no second source metric or bound c_g_b_dis",
            "valid_for_claim": "false",
        },
        {
            "countermodel_id": "CM3380_2_marker_scalar",
            "3379_countermodel": "theta_A(qPhi,I_perp) marker source functor",
            "3380_status": "KILLED_IF_HOM3380_3_SIGNED_AND_THETA_SUPERSELECTED",
            "why_not_killed_now": "co-moving material constants can still be typed unless theta_A ownership is fixed",
            "repair": "derive marker superselection or bound b_marker/b_alpha",
            "valid_for_claim": "false",
        },
        {
            "countermodel_id": "CM3380_3_effective_reentry",
            "3379_countermodel": "Z_eff/readout map reenters before source comparison",
            "3380_status": "KILLED_IF_FORM3380_0_AND_HOM3380_4_SIGNED",
            "why_not_killed_now": "variation-before-readout firewall is a contract, not yet a parent derivation",
            "repair": "prove no-reentry theorem or bound C_eff_source_tail",
            "valid_for_claim": "false",
        },
        {
            "countermodel_id": "CM3380_4_boundary_absorption",
            "3379_countermodel": "source-dependent boundary reference shifts active mass",
            "3380_status": "KILLED_IF_HOM3380_5_AND_ZERO_FLUX_CONTRACT_SIGNED",
            "why_not_killed_now": "3376 zero-flux branch helps but does not alone prove source-blind reference adoption",
            "repair": "prove boundary reference lock or bound boundary contribution to GM",
            "valid_for_claim": "false",
        },
    ]


def runner_rows() -> list[dict[str, str]]:
    return [
        {
            "run_id": "RUN3380_0_structural_type_theorem",
            "test": "derive source universality from candidate object-language formation rules",
            "result": "PASS_CONDITIONAL_STRUCTURAL_THEOREM",
            "detail": "within OBJ3380/FORM3380, source-only prefactors cannot be constructed because the needed Hom-sets are absent",
            "claim_allowed": "false",
            "valid_for_claim": "false",
        },
        {
            "run_id": "RUN3380_1_not_ward_only",
            "test": "try to use conservation/covariance alone",
            "result": "REFUSED_INSUFFICIENT",
            "detail": "3379 countermodel w_A S_A remains covariant; 3380 therefore uses typing, not Ward identity alone",
            "claim_allowed": "false",
            "valid_for_claim": "false",
        },
        {
            "run_id": "RUN3380_2_current_adoption",
            "test": "promote candidate type-system as current MTS parent signature",
            "result": "BLOCKED_NOT_PARENT_SIGNED",
            "detail": "the candidate grammar has not been derived from the primitive M/T/S object language",
            "claim_allowed": "false",
            "valid_for_claim": "false",
        },
        {
            "run_id": "RUN3380_3_bound_inventory",
            "test": "source finite fallback rows for WEP, Cassini/PPN, R10 and clocks",
            "result": "PASS_NONCLAIM_ACQUISITION_MATRIX",
            "detail": "local bound/intake rows are connected to residuals but MTS predictions remain missing or conditional",
            "claim_allowed": "false",
            "valid_for_claim": "false",
        },
        {
            "run_id": "RUN3380_4_firewall",
            "test": "prevent accidental local-GR/source-coupling claim",
            "result": "PASS_CLAIM_FIREWALL",
            "detail": "all rows remain valid_for_claim=false until parent adoption or numeric residual projections are supplied",
            "claim_allowed": "false",
            "valid_for_claim": "false",
        },
    ]


def gate_rows(source_ok: bool) -> list[dict[str, str]]:
    return [
        {
            "gate_id": "GATE3380_0_sources",
            "claim": "all 3380 local inputs exist and parse",
            "gate_pass": bool_text(source_ok),
            "reason": "source register checks 3379 handoff plus WEP/Cassini/R10/clock fallback files",
            "claim_allowed": "false",
            "valid_for_claim": "false",
        },
        {
            "gate_id": "GATE3380_1_conditional_type_theorem",
            "claim": "candidate parent grammar forbids source-only prefactors",
            "gate_pass": "true",
            "reason": "structural induction and Hom-set firewall prove the theorem inside the candidate grammar",
            "claim_allowed": "false",
            "valid_for_claim": "false",
        },
        {
            "gate_id": "GATE3380_2_parent_adoption",
            "claim": "MTS core forces this grammar uniquely",
            "gate_pass": "false",
            "reason": "adoption from motion/time/space primitives is the next theorem, not completed here",
            "claim_allowed": "false",
            "valid_for_claim": "false",
        },
        {
            "gate_id": "GATE3380_3_empirical_bound_ready",
            "claim": "finite source-prefactor residuals are score-ready",
            "gate_pass": "false",
            "reason": "external bound rows exist, but MTS parent coefficients/projections are missing or nonclaim",
            "claim_allowed": "false",
            "valid_for_claim": "false",
        },
        {
            "gate_id": "GATE3380_4_local_GR_source_coupling",
            "claim": "local GR/Newton source coupling is derived",
            "gate_pass": "false",
            "reason": "needs GATE3380_2 or numeric residual bounds to pass",
            "claim_allowed": "false",
            "valid_for_claim": "false",
        },
    ]


def decision_rows() -> list[dict[str, str]]:
    return [
        {
            "decision_id": "DEC3380_0_main_progress",
            "decision": "The coupling gap is now a precise parent type-system adoption problem.",
            "because": "Within the candidate object language, source-only prefactors require forbidden Hom-sets and are untypeable by structural induction.",
            "next_action": "derive the candidate object language from the primitive motion/time/space framework",
            "valid_for_claim": "false",
        },
        {
            "decision_id": "DEC3380_1_not_public_claim",
            "decision": "Do not claim local-GR source coupling yet.",
            "because": "The type theorem is exact only after adoption; current MTS has not proved it uniquely follows from its core primitives.",
            "next_action": "keep all source-prefactor rows nonclaim",
            "valid_for_claim": "false",
        },
        {
            "decision_id": "DEC3380_2_bound_fallback",
            "decision": "The fallback empirical route is now staged but not score-ready.",
            "because": "MICROSCOPE/Cassini/R10/clock local rows are linked to residuals, but MTS projections/coefficients remain missing.",
            "next_action": "if derivation fails, turn the staged matrix into numeric WEP/PPN/R10/clock residual runners",
            "valid_for_claim": "false",
        },
    ]


def next_rows() -> list[dict[str, str]]:
    return [
        {
            "target_id": "3381-Y5-R2FR-MTS-triad-parent-object-language-adoption-or-minimal-coupling-axiom-under-AX1090.md",
            "target_script": "scripts/Y5_R2FR_3381_MTS_triad_parent_object_language_adoption_or_minimal_coupling_axiom.py",
            "objective": "derive OBJ3380/FORM3380 from motion-time-space primitives; if it cannot be derived, isolate the smallest honest universal-coupling axiom instead of hiding it",
            "why_next": "3380 proves the type theorem inside a candidate grammar; the only way forward is to show MTS itself forces that grammar",
            "valid_for_claim": "false",
        },
        {
            "target_id": "3382-Y5-R2FR-source-prefactor-bound-runner-WEP-PPN-R10-clock-under-AX1090.md",
            "target_script": "scripts/Y5_R2FR_3382_source_prefactor_bound_runner_WEP_PPN_R10_clock.py",
            "objective": "build numeric nonclaim runners for Delta_w_AB, c_g_b_dis, b_marker and C_eff_source_tail if the adoption theorem fails",
            "why_next": "finite bounds are the fallback if the pure derivation route stops at a minimal coupling axiom",
            "valid_for_claim": "false",
        },
    ]


def all_claim_flags_false(paths: list[Path]) -> tuple[bool, str]:
    offenders: list[str] = []
    for path in paths:
        if not path.exists() or path.suffix.lower() != ".csv":
            continue
        for index, row in enumerate(read_csv_rows(path), start=2):
            if "valid_for_claim" in row and row["valid_for_claim"].strip().lower() != "false":
                offenders.append(f"{path.name}:line{index}:{row['valid_for_claim']}")
    return not offenders, "; ".join(offenders)


def validate(rows_by_name: dict[str, list[dict[str, Any]]]) -> list[dict[str, str]]:
    source_ok = all(row["exists"] == "true" and row["parse_ok"] == "true" for row in rows_by_name["source_register"])
    output_csvs = [path for key, path in OUTPUTS.items() if key != "validation" and path.suffix.lower() == ".csv"]
    parse_results = [parse_csv(path)[0] for path in output_csvs if path.exists()]
    flags_ok, flag_detail = all_claim_flags_false(output_csvs)
    formalization_hits = [
        hit
        for hit in FW.rglob("*3380*")
        if hit.name.startswith(("3380-Y5", "P8_Y5_R2FR_3380", "P8_Y5_BRR545_3380", "Y5_R2FR_3380"))
    ] if FW.exists() else []
    theorem_ids = {row["theorem_id"] for row in rows_by_name["type_theorem"]}
    object_ids = {row["object_id"] for row in rows_by_name["object_language"]}
    rule_ids = {row["rule_id"] for row in rows_by_name["formation_rules"]}
    firewall_ids = {row["firewall_id"] for row in rows_by_name["homset_firewall"]}
    bound_ids = {row["bound_id"] for row in rows_by_name["bound_matrix"]}
    component_symbols = {row["symbol"] for row in rows_by_name["component_rows"]}
    runner_results = {row["result"] for row in rows_by_name["runner"]}
    gate_map = {row["gate_id"]: row["gate_pass"] for row in rows_by_name["gates"]}
    theorem_text = " ".join(row.get("proof_or_failure", "") for row in rows_by_name["type_theorem"])
    checks = [
        ("VAL3380_0_sources_exist_parse", "all cited 3380 source paths exist and parse", source_ok, ""),
        ("VAL3380_1_outputs_parse", "all generated CSV outputs parse cleanly", len(parse_results) == len(output_csvs) and all(parse_results), f"parsed={sum(1 for ok in parse_results if ok)} expected={len(output_csvs)}"),
        ("VAL3380_2_object_language", "object language covers parent configuration, observed geometry, matter, universal constants, readout and boundary reference", {"OBJ3380_0_parent_configuration", "OBJ3380_1_observed_geometry", "OBJ3380_2_matter_bundle", "OBJ3380_3_universal_scale", "OBJ3380_4_readout_arena", "OBJ3380_5_boundary_reference"}.issubset(object_ids), ""),
        ("VAL3380_3_formation_rules", "formation rules cover scalar density, single measure, matter functor, common source normalization, no hidden Hom-sets and no-extension discipline", {"FORM3380_0_action_scalar_density", "FORM3380_1_single_measure", "FORM3380_2_matter_functor", "FORM3380_3_common_source_normalization", "FORM3380_4_no_hidden_homsets", "FORM3380_5_no_extension_by_absence"}.issubset(rule_ids), ""),
        ("VAL3380_4_type_theorem", "type theorem includes statement, base cases, induction, common-mode exception, adoption blocker and verdict", {"TTS3380_0_statement", "TTS3380_1_base_cases", "TTS3380_2_induction_step", "TTS3380_3_universal_constant_exception", "TTS3380_4_current_MTS_adoption", "TTS3380_5_verdict"}.issubset(theorem_ids) and "structural induction" in theorem_text, ""),
        ("VAL3380_5_homset_firewall", "firewall covers species, readout, hidden frame, marker, post-projector and boundary source Hom-sets", {"HOM3380_0_species_weight", "HOM3380_1_readout_channel_weight", "HOM3380_2_hidden_frame", "HOM3380_3_marker_functor", "HOM3380_4_post_projector_source", "HOM3380_5_boundary_source_weight"}.issubset(firewall_ids), ""),
        ("VAL3380_6_bound_matrix", "bound matrix links WEP, MICROSCOPE inputs, Cassini, R10 anchor/curve contract and clocks", {"BND3380_0_Delta_w_AB_MICROSCOPE", "BND3380_1_eta_TiPt_MICROSCOPE", "BND3380_2_cg_bdis_Cassini", "BND3380_3_R10_alpha_lambda", "BND3380_4_R10_full_curve_contract", "BND3380_5_clock_marker"}.issubset(bound_ids), ""),
        ("VAL3380_7_component_rows", "component rows cover Delta_w_AB, epsilon_Wchan, c_g_b_dis, b_marker, C_eff_source_tail and envelope", {"Delta_w_AB", "epsilon_Wchan", "c_g_b_dis", "b_marker", "C_eff_source_tail", "epsilon_source_pref_marker_abs"}.issubset(component_symbols), ""),
        ("VAL3380_8_runner_firewall", "runner passes conditional theorem and blocks current claim", {"PASS_CONDITIONAL_STRUCTURAL_THEOREM", "REFUSED_INSUFFICIENT", "BLOCKED_NOT_PARENT_SIGNED", "PASS_NONCLAIM_ACQUISITION_MATRIX", "PASS_CLAIM_FIREWALL"}.issubset(runner_results), ""),
        ("VAL3380_9_gates_block_local", "gates pass conditional type theorem but block adoption, empirical score and local GR", gate_map.get("GATE3380_1_conditional_type_theorem") == "true" and gate_map.get("GATE3380_2_parent_adoption") == "false" and gate_map.get("GATE3380_4_local_GR_source_coupling") == "false", ""),
        ("VAL3380_10_no_overclaim_flags", "all generated rows with valid_for_claim remain false", flags_ok, flag_detail),
        ("VAL3380_11_next_target", "next target moves to MTS triad adoption or minimal coupling axiom", rows_by_name["next"][0]["target_id"].startswith("3381-Y5-R2FR-MTS-triad-parent-object-language"), ""),
        ("VAL3380_12_write_scope_outside_formalization", "no 3380 files were written under formalization-workbench", not formalization_hits, f"hits={len(formalization_hits)}"),
    ]
    checks.append(("VAL3380_13_overall", "3380 validation overall", all(passed for _, _, passed, _ in checks), "all required checks passed" if all(passed for _, _, passed, _ in checks) else "one or more checks failed"))
    return [{"check_id": check_id, "check": check, "passed": bool_text(passed), "detail": detail} for check_id, check, passed, detail in checks]


def write_doc(rows_by_name: dict[str, list[dict[str, Any]]]) -> None:
    lines = [
        "# 3380 - Y5/R2FR parent type-system or source-prefactor bound acquisition under AX1090",
        "",
        "## Summary",
        "- 3380 does not just list the coupling gap again. It turns the gap into an exact parent object-language problem.",
        "- Main derivation: inside the candidate type-system `OBJ3380/FORM3380`, source-only weights are untypeable. The proof is structural: allowed constructors never create the Hom-sets needed for `w_A`, `kappa_A`, hidden source frames, marker weights, readout reentry, or boundary source scales.",
        "- This is a real narrowing: the remaining local-GR source-coupling task is now either to derive this type-system from the MTS motion/time/space primitives, or to admit a minimal universal-coupling axiom.",
        "- Current verdict: not a public/local-GR claim. The theorem is exact only after parent adoption, and current MTS has not yet proved that adoption.",
        "- Fallback: WEP/MICROSCOPE, Cassini/PPN, R10, clock and orbital arenas are staged as finite nonclaim residual routes.",
        "- Next best strike: derive `OBJ3380/FORM3380` from the primitive MTS triad, not from a repair ansatz.",
        "",
        "## Source Register",
        md_table(rows_by_name["source_register"]),
        "## Parent Object Language",
        md_table(rows_by_name["object_language"]),
        "## Action Formation Rules",
        md_table(rows_by_name["formation_rules"]),
        "## Type-system Theorem Attempt",
        md_table(rows_by_name["type_theorem"]),
        "## Forbidden Hom-set Firewall",
        md_table(rows_by_name["homset_firewall"]),
        "## Source-prefactor Bound Acquisition Matrix",
        md_table(rows_by_name["bound_matrix"]),
        "## Component Rows",
        md_table(rows_by_name["component_rows"]),
        "## Arena Projection Requirements",
        md_table(rows_by_name["arena_requirements"]),
        "## Countermodel Survivor Map",
        md_table(rows_by_name["countermodel_map"]),
        "## Nonclaim Runner",
        md_table(rows_by_name["runner"]),
        "## Promotion Gates",
        md_table(rows_by_name["gates"]),
        "## Decision Ledger",
        md_table(rows_by_name["decision"]),
        "## Validation",
        md_table(rows_by_name["validation"]),
        "## Next Target",
        md_table(rows_by_name["next"]),
    ]
    DOC.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    source_register = source_rows()
    source_ok = all(row["exists"] == "true" and row["parse_ok"] == "true" for row in source_register)
    rows_by_name: dict[str, list[dict[str, Any]]] = {
        "source_register": source_register,
        "object_language": object_language_rows(),
        "formation_rules": formation_rule_rows(),
        "type_theorem": type_theorem_rows(),
        "homset_firewall": homset_firewall_rows(),
        "bound_matrix": bound_matrix_rows(),
        "component_rows": component_rows(),
        "arena_requirements": arena_requirement_rows(),
        "countermodel_map": countermodel_map_rows(),
        "runner": runner_rows(),
        "gates": gate_rows(source_ok),
        "decision": decision_rows(),
        "next": next_rows(),
    }
    for name, rows in rows_by_name.items():
        write_csv(OUTPUTS[name], rows)
    rows_by_name["validation"] = validate(rows_by_name)
    write_csv(OUTPUTS["validation"], rows_by_name["validation"])
    write_doc(rows_by_name)
    if PYCACHE.exists():
        shutil.rmtree(PYCACHE)
    print(f"Wrote {DOC}")
    print(f"Wrote {len(OUTPUTS)} CSV outputs under {OUT}")
    print(f"Generated UTC {RUN_UTC}")


if __name__ == "__main__":
    main()

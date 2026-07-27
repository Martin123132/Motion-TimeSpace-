from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


BRANCH_ID = "MTS_R2FR_NOSOURCEONLYSPECIES_OR_SOURCE_PROFILE_VECTOR_2328"

ROOT = Path(__file__).resolve().parents[1]
PROJECT = ROOT.parent
FORMALIZATION = PROJECT / "formalization-workbench"
OUT = ROOT / "source-intake" / "mts_residuals"
RAB_QUEUE = ROOT / "source-intake" / "rab-sector" / "acquisition-queue"
MICRO_RESIDUALS = ROOT / "source-intake" / "microscope" / "branch_locked_wep" / "residuals"
BETA_DOCS = ROOT / "source-intake" / "beta-source" / "docs"

DOC = ROOT / "2328-Y5-R2FR-NoSourceOnlySpeciesSlot-or-source-profile-vector-first-row.md"

PATHS = {
    "2327_doc": ROOT / "2327-Y5-R2FR-source-GM-profile-universality-or-LsourceGM-bound.md",
    "2327_validation": OUT / "P8_Y5_BRR545_2327_VALIDATION.csv",
    "2327_universality": OUT / "P8_Y5_PARENT_QLOC_2327_SOURCE_GM_UNIVERSALITY_ATTEMPT.csv",
    "2327_inputs": OUT / "P8_Y5_PARENT_QLOC_2327_PROFILE_GM_INPUT_LEDGER.csv",
    "2327_bound": OUT / "P8_Y5_PARENT_QLOC_2327_LSOURCEGM_BOUND_ROW.csv",
    "1079_theorem": OUT / "P8_Y5_R10_1079_NARROW_CURRENT_OWNER_THEOREM_ATTEMPT.csv",
    "1079_premise": OUT / "P8_Y5_R10_1079_CURRENT_OWNER_PREMISE_LEDGER.csv",
    "1079_counter": OUT / "P8_Y5_R10_1079_COUNTEREXAMPLE_RESOLUTION_MATRIX.csv",
    "1332_common": OUT / "P8_Y5_R10_1332_COMMON_MODE_SOURCE_THEOREM.csv",
    "1332_premise": OUT / "P8_Y5_R10_1332_COMMON_MODE_PREMISE_AUDIT.csv",
    "1333_attempt": OUT / "P8_Y5_R10_1333_NO_SOURCE_PREFACTOR_DERIVATION_ATTEMPT.csv",
    "1333_counter": OUT / "P8_Y5_R10_1333_SOURCE_PREFACTOR_COUNTERMODEL_LEDGER.csv",
    "1333_schema": OUT / "P8_Y5_R10_1333_PARENT_SCHEMA_OPTIONS.csv",
    "1337_contract": OUT / "P8_Y5_R10_1337_MINIMAL_PARENT_ACTION_CONTRACT.csv",
    "1337_reduction": OUT / "P8_Y5_R10_1337_COMMON_MODE_PREMISE_REDUCTION.csv",
    "1337_counter": OUT / "P8_Y5_R10_1337_ADMISSIBLE_COUNTERMODEL_LEDGER.csv",
    "1424_contract": OUT / "P8_Y5_R10_1424_SOURCE_VECTOR_CONTRACT.csv",
    "1425_premise": OUT / "P8_Y5_R10_1425_COMMON_MODE_PREMISE_AUDIT.csv",
    "1425_zero": OUT / "P8_Y5_R10_1425_COMMON_MODE_WEP_ZERO_PROOF_ATTEMPT.csv",
    "2125_common": OUT / "P8_Y5_PARENT_QLOC_2125_COMMON_MODE_DESCENT_AUDIT.csv",
    "2200_source": OUT / "P8_Y5_PARENT_QLOC_2200_PPN_VECTOR_SOURCE_ROW.csv",
}

SOURCES = [
    ("SRC2328_00_2327_doc", "2327_doc", PATHS["2327_doc"], ["NEXT2327_0", "NoSourceOnlySpeciesSlot"], "2327 handoff"),
    ("SRC2328_01_2327_validation", "2327_validation", PATHS["2327_validation"], ["VAL2327_OVERALL", "PASS"], "2327 validation"),
    ("SRC2328_02_2327_universality", "2327_universality", PATHS["2327_universality"], ["UGM2327_2_no_source_only_species_slot", "SHARPEST_MISSING_PREMISE"], "source-GM missing clause"),
    ("SRC2328_03_2327_inputs", "2327_inputs", PATHS["2327_inputs"], ["PGI2327_0_no_source_only_species_slot", "EXACT_HIGH_PRESSURE_MISSING_CLAUSE"], "2327 input ledger"),
    ("SRC2328_04_2327_bound", "2327_bound", PATHS["2327_bound"], ["LSGM2327_0_bound_contract", "epsilon_sigma_source_GM"], "LsourceGM fallback route"),
    ("SRC2328_05_1079_theorem", "1079_theorem", PATHS["1079_theorem"], ["NCO1079_1_hilbert_variation", "NCO1079_5_species_action_weight"], "current-owner theorem"),
    ("SRC2328_06_1079_premise", "1079_premise", PATHS["1079_premise"], ["PR1079_4_no_pre_action_species_weight", "NOT_SIGNED"], "current-owner premise ledger"),
    ("SRC2328_07_1079_counter", "1079_counter", PATHS["1079_counter"], ["CER1079_0_species_action_weight", "SURVIVES"], "current-owner counterexample"),
    ("SRC2328_08_1332_common", "1332_common", PATHS["1332_common"], ["CMT1332_0", "common"], "common-mode theorem basis"),
    ("SRC2328_09_1332_premise", "1332_premise", PATHS["1332_premise"], ["no independent species/source prefactors", "valid_for_claim"], "common-mode premise audit"),
    ("SRC2328_10_1333_attempt", "1333_attempt", PATHS["1333_attempt"], ["NSP1333_4_minimal_schema", "NOT_DERIVED_CURRENT_CORPUS"], "no-source-prefactor derivation attempt"),
    ("SRC2328_11_1333_counter", "1333_counter", PATHS["1333_counter"], ["CM1333_0_relative_species_weight", "LIVE_COUNTERMODEL"], "source-prefactor countermodel"),
    ("SRC2328_12_1333_schema", "1333_schema", PATHS["1333_schema"], ["SCHEMA1333_0_strict_minimal_matter", "SCHEMA1333_1_finite_prefactor_branch"], "parent schema fork"),
    ("SRC2328_13_1337_contract", "1337_contract", PATHS["1337_contract"], ["PACT1337_2_no_source_only_species_slot", "SHARPEST_REQUIRED_PARENT_PREMISE"], "minimal parent action contract"),
    ("SRC2328_14_1337_reduction", "1337_reduction", PATHS["1337_reduction"], ["RED1337_3_no_source_only_species_slot", "SHARPEST_MISSING_PREMISE"], "premise reduction"),
    ("SRC2328_15_1337_counter", "1337_counter", PATHS["1337_counter"], ["CM1337_0_relative_source_weight", "LIVE_UNLESS_NO_SOURCE_SLOT_PARENT_SIGNED"], "admissible countermodel"),
    ("SRC2328_16_1424_contract", "1424_contract", PATHS["1424_contract"], ["SRCMAP1424_0_R_source", "MISSING_SOURCE_VECTOR"], "source vector contract"),
    ("SRC2328_17_1425_premise", "1425_premise", PATHS["1425_premise"], ["PREM1425_3_no_relative_source_prefactors", "EXACT_HIGH_PRESSURE_MISSING_CLAUSE"], "WEP premise audit"),
    ("SRC2328_18_1425_zero", "1425_zero", PATHS["1425_zero"], ["CMZ1425_3_no_relative_prefactor", "NOT_DERIVED_CURRENT_CORPUS"], "common-mode zero attempt"),
    ("SRC2328_19_2125_common", "2125_common", PATHS["2125_common"], ["CMD2125_1_minimal_missing_clause", "LIVE_COUNTERMODEL"], "common-mode descent audit"),
    ("SRC2328_20_2200_source", "2200_source", PATHS["2200_source"], ["PVS2200_2_vector_contract", "0.005788015401465051"], "PPN vector budget"),
]

OUTPUTS = {
    "sources": OUT / "P8_Y5_PARENT_QLOC_2328_SOURCE_REGISTER.csv",
    "derivation": OUT / "P8_Y5_PARENT_QLOC_2328_NO_SOURCE_ONLY_SPECIES_SLOT_DERIVATION_ATTEMPT.csv",
    "contract": OUT / "P8_Y5_PARENT_QLOC_2328_PARENT_ACTION_CONTRACT.csv",
    "profile": OUT / "P8_Y5_PARENT_QLOC_2328_SOURCE_PROFILE_VECTOR_FIRST_ROW.csv",
    "countermodel": OUT / "P8_Y5_PARENT_QLOC_2328_COUNTERMODEL_DECISION_LEDGER.csv",
    "claims": OUT / "P8_Y5_PARENT_QLOC_2328_CLAIM_GATES.csv",
    "refusal": OUT / "P8_Y5_PARENT_QLOC_2328_REFUSAL_RUNNER.csv",
    "next": OUT / "P8_Y5_PARENT_QLOC_2328_NEXT_TARGET.csv",
    "copies": OUT / "P8_Y5_PARENT_QLOC_2328_BRANCH_COPIES.csv",
    "validation": OUT / "P8_Y5_BRR545_2328_VALIDATION.csv",
}

BRANCH_COPY_SPECS = [
    ("COPY2328_0_derivation", OUTPUTS["derivation"], BETA_DOCS / "NO_SOURCE_ONLY_SPECIES_SLOT_DERIVATION_ATTEMPT_2328_NONCLAIM.csv"),
    ("COPY2328_1_profile", OUTPUTS["profile"], MICRO_RESIDUALS / "source_profile_vector_first_row_nonclaim_2328.csv"),
    ("COPY2328_2_contract", OUTPUTS["contract"], RAB_QUEUE / "JR2328_PARENT_ACTION_CONTRACT_NONCLAIM.csv"),
]


def timestamp() -> str:
    return datetime.now(timezone.utc).isoformat()


def bool_text(value: bool) -> str:
    return "true" if value else "false"


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def write_csv(path: Path, rows: list[dict[str, Any]], fieldnames: list[str] | None = None) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if fieldnames is None:
        fieldnames = []
        for row in rows:
            for key in row:
                if key not in fieldnames:
                    fieldnames.append(key)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def read_csv_rows(path: Path) -> list[dict[str, str]]:
    with path.open("r", newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def needle_status(path: Path, needles: list[str]) -> tuple[bool, str]:
    if not path.exists():
        return False, "missing_file"
    text = read_text(path)
    missing = [needle for needle in needles if needle not in text]
    if missing:
        return False, "missing_needles=" + ";".join(missing)
    return True, "all_needles_found"


def relative_path(path: Path) -> str:
    try:
        return str(path.relative_to(ROOT))
    except ValueError:
        return str(path)


def markdown_table(rows: list[dict[str, Any]], fields: list[str]) -> str:
    lines = [
        "| " + " | ".join(fields) + " |",
        "| " + " | ".join("---" for _ in fields) + " |",
    ]
    for row in rows:
        values = [str(row.get(field, "")).replace("\n", " ").replace("|", "\\|") for field in fields]
        lines.append("| " + " | ".join(values) + " |")
    return "\n".join(lines)


def build_sources() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for row_id, key, path, needles, role in SOURCES:
        found, note = needle_status(path, needles)
        rows.append(
            {
                "timestamp_utc": timestamp(),
                "branch_id": BRANCH_ID,
                "row_id": row_id,
                "source_key": key,
                "source_path": str(path),
                "exists": bool_text(path.exists()),
                "needles": ";".join(needles),
                "needles_found": bool_text(found),
                "source_role": role,
                "valid_for_claim": "false",
                "notes": note,
            }
        )
    return rows


def build_derivation_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "row_id": "NSOS2328_0_target",
            "claim_piece": "NoSourceOnlySpeciesSlot",
            "formal_statement": "There is no admissible parent morphism SpeciesLabel -> Coeff_active_source that multiplies the gravitational source strength independently of non-gravitational matter normalization.",
            "result": "TARGET_SHARPENED",
            "gap_or_status": "this is the exact clause needed by 2327 to set epsilon_sigma_source_GM=0",
            "source_anchor": "UGM2327_2_no_source_only_species_slot;PACT1337_2_no_source_only_species_slot",
            "parent_signed": "false",
            "valid_for_claim": "false",
            "claim_allowed": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "NSOS2328_1_covariance",
            "claim_piece": "covariance forbids source-only weights",
            "formal_statement": "Diffeomorphism covariance alone excludes S_m=sum_A w_A S_A with constant scalar w_A.",
            "result": "FAIL_COUNTERMODEL_SURVIVES",
            "gap_or_status": "constant species weights remain scalar and covariant",
            "source_anchor": "NSP1333_1_covariance;CM1333_0_relative_species_weight",
            "parent_signed": "false",
            "valid_for_claim": "false",
            "claim_allowed": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "NSOS2328_2_hilbert_current",
            "claim_piece": "Hilbert-current ownership forbids source-only weights",
            "formal_statement": "Once S_matter is fixed, the gravitational source is the Hilbert variation with respect to e_obs/g_obs before readout.",
            "result": "EXACT_SUBTHEOREM_BUT_NOT_ENOUGH",
            "gap_or_status": "kills post-variation source rescaling, but pre-variation w_A inside the action is inherited by Hilbert stress",
            "source_anchor": "NCO1079_1_hilbert_variation;NCO1079_5_species_action_weight",
            "parent_signed": "false",
            "valid_for_claim": "false",
            "claim_allowed": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "NSOS2328_3_field_rescaling",
            "claim_piece": "field normalization removes source-only weights",
            "formal_statement": "All w_A can be absorbed into field redefinitions without changing physical source response.",
            "result": "FAIL_NOT_GENERAL",
            "gap_or_status": "interactions, quantum normalization, charges, masses, and clock standards can move the prefactor into theta_A rather than delete it",
            "source_anchor": "NSP1333_3_field_rescaling;CER1079_2_disconnected_material_components",
            "parent_signed": "false",
            "valid_for_claim": "false",
            "claim_allowed": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "NSOS2328_4_source_blind_functor",
            "claim_piece": "source-blind matter functor theorem",
            "formal_statement": "If ordinary matter is a source-blind descended functor with one observed measure, one Hilbert source natural transformation, and no independent species-to-source coefficient object, then w_A is either common calibration, an ordinary theta_A constant, or inadmissible.",
            "result": "EXACT_CONDITIONAL_THEOREM",
            "gap_or_status": "this is the clean parent-action theorem form, but the current corpus has not parent-signed the functor/admissibility clauses",
            "source_anchor": "PACT1337_0_observed_frame;PACT1337_1_single_matter_functional;PACT1337_2_no_source_only_species_slot;RED1337_3_no_source_only_species_slot",
            "parent_signed": "false",
            "valid_for_claim": "false",
            "claim_allowed": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "NSOS2328_5_common_scale",
            "claim_piece": "common source scale quotient",
            "formal_statement": "A single common factor multiplying total T_matter is not a WEP/PPN source residual; it is absorbed into kappa/G_N/GM calibration once.",
            "result": "EXACT_IF_SINGLE_SCALE",
            "gap_or_status": "relative species/source coefficients still require the no-source-only slot or finite vector route",
            "source_anchor": "PACT1337_3_common_calibration;RED1337_4_calibration_quotient;GCG1425_0_common_scale",
            "parent_signed": "false",
            "valid_for_claim": "false",
            "claim_allowed": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "NSOS2328_6_verdict",
            "claim_piece": "promote NoSourceOnlySpeciesSlot now",
            "formal_statement": "The active MTS corpus derives NoSourceOnlySpeciesSlot without adding a parent action admissibility clause.",
            "result": "NOT_DERIVED_PARENT_CONTRACT_READY",
            "gap_or_status": "the clean theorem has been isolated, but it still requires a parent-signed action/functor contract; finite source-profile row remains live",
            "source_anchor": "NSOS2328_1_covariance through NSOS2328_5_common_scale",
            "parent_signed": "false",
            "valid_for_claim": "false",
            "claim_allowed": "false",
        },
    ]


def build_contract_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "row_id": "PAC2328_0_observed_quotient_frame",
            "contract_clause": "ordinary matter sees only the observed quotient frame",
            "mathematical_form": "q(Phi) -> (M,g_obs,e_obs,theta_obs); S_m factors through this data",
            "what_it_forbids": "representative-only vertical fields entering ordinary matter source strength",
            "status": "CONTRACT_READY_NOT_PARENT_SIGNED",
            "needed_for_zero": "true",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "PAC2328_1_single_measure_source_scale",
            "contract_clause": "one observed measure and one active-source normalization for ordinary matter",
            "mathematical_form": "S_m = integral mu_obs L_m(j^k Psi_A,e_obs,theta_A) with no species-dependent mu_A or kappa_A",
            "what_it_forbids": "species-dependent gravitational measure/source scales",
            "status": "MINIMAL_PARENT_CONTRACT_CLAUSE",
            "needed_for_zero": "true",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "PAC2328_2_no_source_only_species_slot",
            "contract_clause": "species labels have no active-source coefficient morphism",
            "mathematical_form": "Hom(SpeciesLabel,Coeff_active_source)=empty except one common calibration quotient",
            "what_it_forbids": "S_m=sum_A w_A S_A where w_A changes active source strength independent of theta_A",
            "status": "SHARPEST_REQUIRED_PARENT_PREMISE",
            "needed_for_zero": "true",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "PAC2328_3_theta_ownership",
            "contract_clause": "species constants live in theta_A and affect both inertial/material physics and source through the same matter functional",
            "mathematical_form": "theta_A may contain masses, charges, spin representation and internal couplings, but not an independent gravitational-source multiplier",
            "what_it_forbids": "renaming source-only w_A as an ordinary constant without changing non-gravitational normalization",
            "status": "CONTRACT_READY_NEEDS_PARENT_SIGNATURE",
            "needed_for_zero": "true",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "PAC2328_4_hilbert_source_before_readout",
            "contract_clause": "source current is Hilbert variation before arena/readout projection",
            "mathematical_form": "T_H := delta S_m/delta e_obs; K_arena and Pi_gamma act downstream",
            "what_it_forbids": "post-variation material/readout selector redefining the source tensor",
            "status": "EXACT_SUBTHEOREM_CONDITIONAL",
            "needed_for_zero": "true",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "PAC2328_5_nonhilbert_silence",
            "contract_clause": "non-Hilbert, boundary, marker, and readout source currents vanish, are exact/projected silent, or are retained",
            "mathematical_form": "J_source = T_Hilbert_total + J_residual, with J_residual=0 only by parent proof",
            "what_it_forbids": "hiding species source weights in boundary/readout/non-Hilbert currents",
            "status": "OPEN_PARALLEL_GATE",
            "needed_for_zero": "true",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "PAC2328_6_verdict",
            "contract_clause": "parent action contract closes source-only species slot",
            "mathematical_form": "PAC2328_0 through PAC2328_5 all parent-signed",
            "what_it_forbids": "all known source-only species slot countermodels",
            "status": "CONTRACT_EXACT_BUT_UNSIGNED",
            "needed_for_zero": "true",
            "valid_for_claim": "false",
        },
    ]


def build_profile_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "row_id": "SPV2328_0_schema",
            "object": "R_source_profile^Earth",
            "definition": "orbit/worldtube-weighted source response vector in the same parent basis as material/source projection",
            "normal_form": "R_source_profile = Normalize[ integral_Earth W_arena(x,t;e_obs,orbit,mask) rho_E(x) R_source(x,theta_E) dmu_obs ]",
            "units": "dimensionless vector after declared normalization",
            "required_inputs": "basis_id; W_arena; rho_E profile; composition/source map; support worldtube; same-frame e_obs; GM calibration",
            "current_status": "SCHEMA_READY_VALUES_MISSING",
            "score_ready": "false",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "SPV2328_1_source_weight_residual",
            "object": "Delta_w_source_profile",
            "definition": "non-common source/profile residual left after one universal GM calibration is removed",
            "normal_form": "Delta_w_source_profile = R_source_profile - Pi_common(R_source_profile)",
            "units": "dimensionless source-response vector",
            "required_inputs": "common-mode projector; source vector basis; calibration quotient; uncertainty envelope",
            "current_status": "MISSING_SOURCE_VECTOR_OR_THEOREM_ZERO",
            "score_ready": "false",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "SPV2328_2_epsilon_link",
            "object": "epsilon_sigma_source_GM",
            "definition": "protocol/source-GM leakage norm produced by the retained source vector and calibration convention",
            "normal_form": "epsilon_sigma_source_GM <= ||D_v R_source_profile|| + ||D_v sigma_GM_common_mode||",
            "units": "declared_protocol_norm",
            "required_inputs": "vertical variation convention; source profile vector; GM calibration equation",
            "current_status": "MISSING_NUMERIC_OR_ZERO_CERTIFICATE",
            "score_ready": "false",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "SPV2328_3_LsourceGM_product",
            "object": "source_GM PPN/local residual",
            "definition": "finite fallback if NoSourceOnlySpeciesSlot remains unsigned",
            "normal_form": "|Pi_gamma C_source_GM| <= |Pi_gamma| L_source_GM epsilon_sigma_source_GM <= 0.005788015401465051",
            "units": "dimensionless PPN alpha-vector budget",
            "required_inputs": "L_source_GM; Pi_gamma; epsilon_sigma_source_GM; absolute-budget policy",
            "current_status": "CONTRACT_READY_VALUES_MISSING",
            "score_ready": "false",
            "valid_for_claim": "false",
        },
    ]


def build_countermodel_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "row_id": "CMD2328_0_relative_species_weight",
            "countermodel": "S_m=sum_A (1+epsilon_A) S_A[Psi_A,e_obs,theta_A]",
            "survives": "covariance; additivity; Hilbert variation; quotient descent if epsilon_A is declared observed",
            "killed_by": "PAC2328_2_no_source_only_species_slot plus PAC2328_3_theta_ownership",
            "if_not_killed": "retained Delta_w_source_profile/source residual vector required",
            "decision": "LIVE_UNTIL_PARENT_CONTRACT_SIGNED",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "CMD2328_1_species_measure_weight",
            "countermodel": "S_m=sum_A integral w_A mu_obs L_A",
            "survives": "scalar density covariance if w_A is constant",
            "killed_by": "PAC2328_1_single_measure_source_scale",
            "if_not_killed": "finite source/vector branch required",
            "decision": "LIVE_UNTIL_PARENT_CONTRACT_SIGNED",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "CMD2328_2_hidden_nonhilbert_current",
            "countermodel": "J_source=T_Hilbert+sum_A zeta_A J_A_nonHilbert",
            "survives": "can be covariant if J_A is conserved or boundary/readout-owned",
            "killed_by": "PAC2328_5_nonhilbert_silence",
            "if_not_killed": "explicit residual/source-current row required",
            "decision": "LIVE_UNTIL_SILENCE_OR_BOUND",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "CMD2328_3_common_scale",
            "countermodel": "S_m=w_common sum_A S_A",
            "survives": "allowed as one common normalization",
            "killed_by": "not killed; quotient-calibrated into measured kappa/G_N/GM",
            "if_not_killed": "not a composition residual if genuinely common",
            "decision": "ALLOWED_COMMON_CALIBRATION_ONLY",
            "valid_for_claim": "false",
        },
    ]


def build_claim_rows() -> list[dict[str, Any]]:
    return [
        {"branch_id": BRANCH_ID, "row_id": "CG2328_0_sources", "gate": "source paths and needles valid", "passed": "true", "claim_effect": "audit reproducible", "valid_for_claim": "false"},
        {"branch_id": BRANCH_ID, "row_id": "CG2328_1_conditional_theorem", "gate": "source-blind functor theorem exact conditionally", "passed": "true", "claim_effect": "parent-action contract isolated", "valid_for_claim": "false"},
        {"branch_id": BRANCH_ID, "row_id": "CG2328_2_active_NoSourceOnlySpeciesSlot", "gate": "NoSourceOnlySpeciesSlot parent-signed now", "passed": "false", "claim_effect": "requires PAC2328 contract signature", "valid_for_claim": "false"},
        {"branch_id": BRANCH_ID, "row_id": "CG2328_3_profile_vector_score", "gate": "source profile vector numerically score-ready", "passed": "false", "claim_effect": "schema only; no finite source row claim", "valid_for_claim": "false"},
        {"branch_id": BRANCH_ID, "row_id": "CG2328_4_source_GM_zero", "gate": "epsilon_sigma_source_GM=0 promoted", "passed": "false", "claim_effect": "NoSourceOnlySpeciesSlot not active", "valid_for_claim": "false"},
        {"branch_id": BRANCH_ID, "row_id": "CG2328_5_local_GR_Newton", "gate": "local GR/Newton recovery derived", "passed": "false", "claim_effect": "still private theorem-building work", "valid_for_claim": "false"},
        {"branch_id": BRANCH_ID, "row_id": "CG2328_6_github_public_update", "gate": "safe to push as public evidence", "passed": "false", "claim_effect": "checkpoint is useful but not public-claim safe", "valid_for_claim": "false"},
    ]


def build_refusal_rows() -> list[dict[str, Any]]:
    return [
        {"branch_id": BRANCH_ID, "row_id": "REF2328_0_covariance_shortcut", "claim": "covariance alone proves NoSourceOnlySpeciesSlot", "allowed": "false", "reason": "constant scalar species weights remain covariant", "blocking_rows": "NSOS2328_1_covariance;CMD2328_0_relative_species_weight", "valid_for_claim": "false"},
        {"branch_id": BRANCH_ID, "row_id": "REF2328_1_hilbert_shortcut", "claim": "Hilbert source ownership alone kills pre-action w_A", "allowed": "false", "reason": "Hilbert variation inherits weights already inserted in S_matter", "blocking_rows": "NSOS2328_2_hilbert_current;NCO1079_5_species_action_weight", "valid_for_claim": "false"},
        {"branch_id": BRANCH_ID, "row_id": "REF2328_2_minimality_as_proof", "claim": "strict minimal matter schema is proved because it is elegant", "allowed": "false", "reason": "minimal schema must be parent-signed, not chosen after local tests", "blocking_rows": "NSOS2328_4_source_blind_functor;PAC2328_6_verdict", "valid_for_claim": "false"},
        {"branch_id": BRANCH_ID, "row_id": "REF2328_3_profile_claim", "claim": "source profile vector row is a prediction", "allowed": "false", "reason": "first row is schema/acquisition only; no data, units, basis, or GM equation are filled", "blocking_rows": "SPV2328_0_schema through SPV2328_3_LsourceGM_product", "valid_for_claim": "false"},
        {"branch_id": BRANCH_ID, "row_id": "REF2328_4_public_claim", "claim": "publish 2328 as local-GR/PPN/source_GM pass", "allowed": "false", "reason": "2328 isolates the parent-action contract; it does not activate it or score the finite branch", "blocking_rows": "CG2328_5_local_GR_Newton;CG2328_6_github_public_update", "valid_for_claim": "false"},
    ]


def build_next_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "row_id": "NEXT2328_0",
            "next_target": "2329-Y5-R2FR-parent-action-source-blind-functor-signature.md",
            "why": "2328 found the cleanest route: try to parent-sign PAC2328_0..5 as a source-blind matter functor instead of patching individual source leaks.",
            "claim_status": "private_derivation_next_step",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "NEXT2328_1",
            "next_target": "2329b-Y5-R2FR-source-profile-vector-acquisition-skeleton.md",
            "why": "if the parent action contract cannot be signed, the fallback is a finite source-profile vector with declared basis, units, frame and GM calibration.",
            "claim_status": "fallback_nonclaim",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "NEXT2328_2",
            "next_target": "private-publish-readiness-summary",
            "why": "GitHub should wait until either the parent action signature is cleanly written or the finite branch is explicitly framed as nonclaim acquisition.",
            "claim_status": "no_github_yet",
            "valid_for_claim": "false",
        },
    ]


def copy_branch_outputs() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for row_id, src, dest in BRANCH_COPY_SPECS:
        dest.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(src, dest)
        rows.append(
            {
                "branch_id": BRANCH_ID,
                "row_id": row_id,
                "source_csv": relative_path(src),
                "branch_copy_path": str(dest),
                "copy_exists": bool_text(dest.exists()),
                "row_count": str(len(read_csv_rows(dest))),
                "valid_for_claim": "false",
            }
        )
    return rows


def build_validation_rows(source_rows: list[dict[str, Any]], branch_copy_rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    generated_paths = [path for key, path in OUTPUTS.items() if key != "validation"]
    generated_paths += [Path(row["branch_copy_path"]) for row in branch_copy_rows]
    rows: list[dict[str, Any]] = []

    def add(row_id: str, passed: bool, detail: str) -> None:
        rows.append(
            {
                "branch_id": BRANCH_ID,
                "row_id": row_id,
                "status": "PASS" if passed else "FAIL",
                "detail": detail,
                "valid_for_claim": "false",
            }
        )

    add("VAL2328_00_sources_exist", all(row["exists"] == "true" for row in source_rows), "every cited source path exists")
    add("VAL2328_01_needles_found", all(row["needles_found"] == "true" for row in source_rows), "all source needles were found")
    derivation_rows = read_csv_rows(OUTPUTS["derivation"])
    add("VAL2328_02_conditional_theorem", any(row.get("row_id") == "NSOS2328_4_source_blind_functor" and row.get("result") == "EXACT_CONDITIONAL_THEOREM" for row in derivation_rows), "source-blind functor theorem isolated")
    add("VAL2328_03_active_not_promoted", any(row.get("row_id") == "NSOS2328_6_verdict" and row.get("result") == "NOT_DERIVED_PARENT_CONTRACT_READY" for row in derivation_rows), "NoSourceOnlySpeciesSlot not promoted")
    contract_rows = read_csv_rows(OUTPUTS["contract"])
    add("VAL2328_04_contract_complete", len(contract_rows) >= 7 and any(row.get("row_id") == "PAC2328_6_verdict" for row in contract_rows), "parent action contract rows populated")
    profile_rows = read_csv_rows(OUTPUTS["profile"])
    add("VAL2328_05_profile_schema", any(row.get("row_id") == "SPV2328_0_schema" and row.get("current_status") == "SCHEMA_READY_VALUES_MISSING" for row in profile_rows), "source profile vector first row schema exists")
    add("VAL2328_06_profile_nonready", all(row.get("score_ready") == "false" for row in profile_rows), "source profile rows remain non-score-ready")
    counter_rows = read_csv_rows(OUTPUTS["countermodel"])
    add("VAL2328_07_countermodels_retained", any(row.get("decision") == "LIVE_UNTIL_PARENT_CONTRACT_SIGNED" for row in counter_rows), "live countermodels retained unless parent contract signed")
    claim_rows = read_csv_rows(OUTPUTS["claims"])
    add("VAL2328_08_claim_gates_block", any(row.get("row_id") == "CG2328_5_local_GR_Newton" and row.get("passed") == "false" for row in claim_rows), "local GR/Newton claim remains blocked")
    add("VAL2328_09_github_blocked", any(row.get("row_id") == "CG2328_6_github_public_update" and row.get("passed") == "false" for row in claim_rows), "public GitHub update not recommended as evidence")
    refusal_rows = read_csv_rows(OUTPUTS["refusal"])
    add("VAL2328_10_refusals_block", all(row.get("allowed") == "false" for row in refusal_rows), "refusal runner blocks shortcut claims")
    add("VAL2328_11_next_target", len(read_csv_rows(OUTPUTS["next"])) >= 2, "next targets selected")
    add("VAL2328_12_branch_copies_parse", all(Path(row["branch_copy_path"]).exists() and int(row["row_count"]) > 0 for row in branch_copy_rows), "branch copies exist and parse")
    claim_flags: list[str] = []
    for path in generated_paths:
        for index, row in enumerate(read_csv_rows(path), start=2):
            if str(row.get("valid_for_claim", "")).lower() == "true":
                claim_flags.append(f"{path.name}:{index}")
    add("VAL2328_13_no_claim_flags", not claim_flags, "no generated row is valid_for_claim=true" if not claim_flags else ";".join(claim_flags))
    formalization_hits: list[Path] = []
    if FORMALIZATION.exists():
        checkpoint_patterns = ("*P8_Y5*2328*.csv", "*2328-Y5*.md", "*NOSOURCE*2328*", "*SOURCE_PROFILE_VECTOR*2328*")
        for pattern in checkpoint_patterns:
            formalization_hits.extend(FORMALIZATION.rglob(pattern))
    add("VAL2328_14_formalization_untouched_by_2328", not formalization_hits, "no 2328 checkpoint output appears in formalization-workbench" if not formalization_hits else ";".join(str(path) for path in formalization_hits[:5]))
    add("VAL2328_OVERALL", all(row["status"] == "PASS" for row in rows), "2328 isolates the exact NoSourceOnlySpeciesSlot parent-action contract, refuses covariance/Hilbert/minimality shortcuts, stages a nonclaim source-profile vector row, and recommends no GitHub evidence update yet.")
    return rows


def write_doc(
    source_rows: list[dict[str, Any]],
    derivation_rows: list[dict[str, Any]],
    contract_rows: list[dict[str, Any]],
    profile_rows: list[dict[str, Any]],
    countermodel_rows: list[dict[str, Any]],
    claim_rows: list[dict[str, Any]],
    refusal_rows: list[dict[str, Any]],
    next_rows: list[dict[str, Any]],
    branch_copy_rows: list[dict[str, Any]],
    validation_rows: list[dict[str, Any]],
) -> None:
    content = f"""# 2328 - NoSourceOnlySpeciesSlot Or Source Profile Vector First Row

## Summary

2328 attacks the coupling throat directly. The clean result is not a full active proof yet, but it is a sharper theorem:

If ordinary matter is a source-blind descended functor with one observed frame, one measure/source scale, one Hilbert
source natural transformation before readout, no species-to-active-source coefficient object, and no hidden
non-Hilbert/readout current, then any apparent `w_A` is either:

1. a single common calibration absorbed into measured `G_N/GM`,
2. an ordinary matter constant inside `theta_A` that affects non-gravitational normalization too, or
3. inadmissible as a source-only spurion.

That would close the `NoSourceOnlySpeciesSlot` gate and greatly strengthen the GR/Newton reduction route. But the active
corpus has not parent-signed that full action/functor contract, so the theorem remains conditional and the fallback
finite source-profile vector row stays live.

This checkpoint is private theorem-building, not public evidence.

## Source Register

{markdown_table(source_rows, ["row_id", "source_key", "source_path", "exists", "needles_found", "source_role", "valid_for_claim"])}

## NoSourceOnlySpeciesSlot Derivation Attempt

{markdown_table(derivation_rows, ["row_id", "claim_piece", "formal_statement", "result", "gap_or_status", "source_anchor", "valid_for_claim"])}

## Parent Action Contract

{markdown_table(contract_rows, ["row_id", "contract_clause", "mathematical_form", "what_it_forbids", "status", "needed_for_zero", "valid_for_claim"])}

## Source Profile Vector First Row

{markdown_table(profile_rows, ["row_id", "object", "definition", "normal_form", "units", "current_status", "score_ready", "valid_for_claim"])}

## Countermodel Decision Ledger

{markdown_table(countermodel_rows, ["row_id", "countermodel", "survives", "killed_by", "if_not_killed", "decision", "valid_for_claim"])}

## Claim Gates

{markdown_table(claim_rows, ["row_id", "gate", "passed", "claim_effect", "valid_for_claim"])}

## Refusal Runner

{markdown_table(refusal_rows, ["row_id", "claim", "allowed", "reason", "blocking_rows", "valid_for_claim"])}

## Next Target

{markdown_table(next_rows, ["row_id", "next_target", "why", "claim_status", "valid_for_claim"])}

## Branch Copies

{markdown_table(branch_copy_rows, ["row_id", "source_csv", "branch_copy_path", "copy_exists", "row_count", "valid_for_claim"])}

## Validation

{markdown_table(validation_rows, ["row_id", "status", "detail", "valid_for_claim"])}
"""
    DOC.write_text(content, encoding="utf-8")


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    rows_by_output = {
        "sources": build_sources(),
        "derivation": build_derivation_rows(),
        "contract": build_contract_rows(),
        "profile": build_profile_rows(),
        "countermodel": build_countermodel_rows(),
        "claims": build_claim_rows(),
        "refusal": build_refusal_rows(),
        "next": build_next_rows(),
    }
    for key, rows in rows_by_output.items():
        write_csv(OUTPUTS[key], rows)
    branch_copy_rows = copy_branch_outputs()
    write_csv(OUTPUTS["copies"], branch_copy_rows)
    validation_rows = build_validation_rows(rows_by_output["sources"], branch_copy_rows)
    write_csv(OUTPUTS["validation"], validation_rows)
    write_doc(
        rows_by_output["sources"],
        rows_by_output["derivation"],
        rows_by_output["contract"],
        rows_by_output["profile"],
        rows_by_output["countermodel"],
        rows_by_output["claims"],
        rows_by_output["refusal"],
        rows_by_output["next"],
        branch_copy_rows,
        validation_rows,
    )
    failed = [row for row in validation_rows if row["status"] != "PASS"]
    if failed:
        raise SystemExit("2328 validation failed: " + "; ".join(row["row_id"] for row in failed))
    print(f"wrote {DOC}")
    print(f"wrote {OUTPUTS['validation']}")


if __name__ == "__main__":
    main()

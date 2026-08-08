from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
PROJECT = ROOT.parent
RESIDUALS = ROOT / "source-intake" / "mts_residuals"
QUEUE = ROOT / "source-intake" / "rab-sector" / "acquisition-queue"
LOCAL_BOUNDS = ROOT / "source-intake" / "local_bounds"
SOURCE_WEIGHT = ROOT / "source-intake" / "source-weight" / "docs"
MICROSCOPE = ROOT / "source-intake" / "microscope" / "branch_locked_wep" / "residuals"
FORMALIZATION = PROJECT / "formalization-workbench"
DOC_PATH = ROOT / "2646-Y5-R2FR-matter-normalization-owner-or-Delta-w-species-coefficient-source-row.md"

CHECKPOINT = "2646"
BRANCH_ID = "Y5_R2FR_MATTER_NORMALIZATION_OWNER_OR_DELTAW_COEFFICIENT_ROW_2646"
PREFIX = "P8_Y5_MATTER_NORMALIZATION_OWNER_2646"

OUTPUTS = {
    "source_register": RESIDUALS / f"{PREFIX}_SOURCE_REGISTER.csv",
    "owner_attempt": RESIDUALS / f"{PREFIX}_OWNER_THEOREM_ATTEMPT.csv",
    "standard_owner_audit": RESIDUALS / f"{PREFIX}_STANDARD_OWNER_AUDIT.csv",
    "coefficient_rows": RESIDUALS / f"{PREFIX}_DELTAW_SPECIES_COEFFICIENT_ROWS_NONCLAIM.csv",
    "projection_requirements": RESIDUALS / f"{PREFIX}_PROJECTION_REQUIREMENTS.csv",
    "validator_cases": RESIDUALS / f"{PREFIX}_VALIDATOR_CASES.csv",
    "validator_results": RESIDUALS / f"{PREFIX}_VALIDATOR_RESULTS.csv",
    "claim_gates": RESIDUALS / f"{PREFIX}_CLAIM_GATES.csv",
    "decision": RESIDUALS / f"{PREFIX}_DECISION_LEDGER.csv",
    "next_target": RESIDUALS / f"{PREFIX}_NEXT_TARGET.csv",
    "branch_copies": RESIDUALS / f"{PREFIX}_BRANCH_COPIES.csv",
    "validation": RESIDUALS / f"P8_Y5_BRR545_{CHECKPOINT}_VALIDATION.csv",
}

BRANCH_COPIES = {
    "queue": QUEUE / "JR2646_MATTER_NORMALIZATION_OWNER_DELTAW_NONCLAIM.csv",
    "local_bounds": LOCAL_BOUNDS / "Delta_w_species_owner_2646_NONCLAIM.csv",
    "source_weight": SOURCE_WEIGHT / "DELTAW_SPECIES2646_COEFFICIENT_ROW_NONCLAIM.csv",
    "microscope": MICROSCOPE / "P8_Y5_2646_DELTAW_SPECIES_WEP_NONCLAIM.csv",
}

SOURCES = [
    {
        "source_id": "SRC2646_00_2645",
        "role": "immediate current branch handoff",
        "path": ROOT / "2645-Y5-R2FR-no-source-prefactor-parent-action-clause-or-first-JH-DqZ-component-row.md",
        "needles": ["NSP2645_7_verdict", "XIC2645_1_Delta_w_species", "VAL2645_OVERALL"],
    },
    {
        "source_id": "SRC2646_01_1891",
        "role": "older matter-normalization owner and coefficient row",
        "path": ROOT / "1891-Y5-R2FR-matter-normalization-owner-or-deltaw-species-coefficient-source-row.md",
        "needles": ["MNO1891_5_verdict", "DWS1891_0_delta_w_species_coefficient_slot", "VAL1891_OVERALL"],
    },
    {
        "source_id": "SRC2646_02_1896",
        "role": "sort-disjointness/no-Hom route and finite Delta_w basis",
        "path": ROOT / "1896-Y5-R2FR-parent-sort-disjointness-nohom-proof-or-finite-deltaw-basis.md",
        "needles": ["NHG1896_1_no_species_hom", "DWB1896_0_vector_space", "DWB1896_1_preaction_species"],
    },
    {
        "source_id": "SRC2646_03_1904",
        "role": "constructor exhaustion/action-scale owner gap",
        "path": ROOT / "1904-Y5-R2FR-parent-action-constructor-exhaustion-or-action-scale-owner.md",
        "needles": ["ASO1904_4_parent_gap", "NEXT1904_0_primary"],
    },
    {
        "source_id": "SRC2646_04_1098_owner",
        "role": "ordinary constant/source-weight owner signature",
        "path": RESIDUALS / "P8_Y5_R10_1098_ORDINARY_CONSTANT_OWNER_SIGNATURE_ATTEMPT.csv",
        "needles": ["OCS1098_4_source_weight_exclusion", "no species/source-only gravitational weights", "UNSIGNED"],
    },
    {
        "source_id": "SRC2646_05_1098_forbidden",
        "role": "forbidden vertex audit retaining source weights",
        "path": RESIDUALS / "P8_Y5_R10_1098_FORBIDDEN_VERTEX_AUDIT.csv",
        "needles": ["FV1098_6_source_weight_X", "forbidden_required_but_currently_legal"],
    },
    {
        "source_id": "SRC2646_06_1088",
        "role": "minimal ordinary matter action signature",
        "path": RESIDUALS / "P8_Y5_R10_1088_MINIMAL_SIGNATURE_CLAUSE.csv",
        "needles": ["MOMS1088_4_no_species_weights", "PRE_ACTION_WEIGHT_EXCLUSION_UNSIGNED"],
    },
    {
        "source_id": "SRC2646_07_1045",
        "role": "parent matter functor signature audit",
        "path": RESIDUALS / "P8_Y5_R10_1045_PARENT_MATTER_FUNCTOR_SIGNATURE_AUDIT.csv",
        "needles": ["MFS1045_2_matter_bundle_functor", "MATTER_CATEGORY_NOT_PARENT_CONSTRUCTED"],
    },
    {
        "source_id": "SRC2646_08_1488",
        "role": "fixed constants/common calibration guard",
        "path": RESIDUALS / "P8_Y5_R10_1488_FIXED_CONSTANTS_REPRESENTATION_GATE.csv",
        "needles": ["FCR1488_2_common_calibration", "CONSTANT_DEBT_RETAINED"],
    },
]


def timestamp() -> str:
    return datetime.now(timezone.utc).isoformat()


def base_row(**kwargs: Any) -> dict[str, Any]:
    row: dict[str, Any] = {
        "timestamp_utc": timestamp(),
        "checkpoint": CHECKPOINT,
        "branch_id": BRANCH_ID,
        "valid_for_claim": "False",
        "claim_allowed": "False",
    }
    row.update(kwargs)
    return row


def read_text(path: Path) -> str:
    if not path.exists():
        return ""
    return path.read_text(encoding="utf-8", errors="ignore")


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    if not rows:
        raise ValueError(f"No rows for {path}")
    path.parent.mkdir(parents=True, exist_ok=True)
    fieldnames: list[str] = []
    for row in rows:
        for key in row:
            if key not in fieldnames:
                fieldnames.append(key)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def csv_parses(path: Path) -> bool:
    try:
        return bool(read_csv(path))
    except Exception:
        return False


def md_escape(value: Any) -> str:
    return str(value).replace("|", "\\|").replace("\n", "<br>")


def md_table(rows: list[dict[str, Any]], columns: list[str] | None = None) -> str:
    if not rows:
        return "_No rows._"
    if columns is None:
        columns = []
        for row in rows:
            for key in row:
                if key not in columns:
                    columns.append(key)
    lines = [
        "| " + " | ".join(columns) + " |",
        "| " + " | ".join(["---"] * len(columns)) + " |",
    ]
    for row in rows:
        lines.append("| " + " | ".join(md_escape(row.get(column, "")) for column in columns) + " |")
    return "\n".join(lines)


def remove_pycache() -> None:
    cache = ROOT / "scripts" / "__pycache__"
    if cache.exists():
        shutil.rmtree(cache)


def formalization_has_2646_artifacts() -> bool:
    if not FORMALIZATION.exists():
        return False
    patterns = (
        "*2646-Y5-R2FR*",
        "*P8_Y5_MATTER_NORMALIZATION_OWNER_2646*",
        "*P8_Y5_BRR545_2646*",
        "*Y5_R2FR_matter_normalization_owner_or_Delta_w_species_coefficient_source_row_2646*",
        "*JR2646*",
    )
    return any(path.is_file() for pattern in patterns for path in FORMALIZATION.rglob(pattern))


def source_register_rows() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for source in SOURCES:
        text = read_text(source["path"])
        found = [needle for needle in source["needles"] if needle in text]
        rows.append(
            base_row(
                source_id=source["source_id"],
                role=source["role"],
                source_path=str(source["path"]),
                path_exists=str(source["path"].exists()),
                required_needles=";".join(source["needles"]),
                found_needles=";".join(found),
                needles_present=str(source["path"].exists() and len(found) == len(source["needles"])),
            )
        )
    return rows


def owner_attempt_rows() -> list[dict[str, Any]]:
    return [
        base_row(
            theorem_id="MNO2646_0_target",
            claim_piece="matter-normalization owner",
            formal_statement="Ordinary matter normalization is owned by nongravitational representation/current data before gravitational source extraction; no active-source-only scalar w_A is an allowed parent datum.",
            status="TARGET_SHARP",
            proof_status="attempted",
            if_signed="Delta_w_species becomes theorem-zero rather than fitted or bounded.",
            obstruction="must be derived from the parent action grammar, not imposed after local tests complain.",
            source_anchor="2645:XIC2645_1_Delta_w_species;1891:MNO1891_0_target",
        ),
        base_row(
            theorem_id="MNO2646_1_conditional_owner_lemma",
            claim_piece="conditional double-counting theorem",
            formal_statement="If S_matter=sum_A S_A[Psi_A,e_obs,A_obs,theta_A], theta_A are owned/fixed, one action-density line is shared, and J_H=delta S_matter/delta e_obs before readout, then adding sum_A epsilon_A S_A or kappa_A T_A is extra source structure, not measured matter.",
            status="EXACT_CONDITIONAL_THEOREM",
            proof_status="conditional only",
            if_signed="pre-action source weights are duplicate/ill-typed objects.",
            obstruction="the parent has not yet signed the one action-density line, no-Hom source slot, and radiative/readout stability together.",
            source_anchor="1891:MNO1891_1_conditional_double_counting;1088:MOMS1088_4_no_species_weights",
        ),
        base_row(
            theorem_id="MNO2646_2_natural_nohom_route",
            claim_piece="species label cannot map to source coefficient",
            formal_statement="In a typed parent category, SpeciesLabel has no natural morphism to ActiveSourceWeight except the universal scalar endomorphism of the action-density line.",
            status="EXACT_IF_PARENT_SORTS_SIGNED",
            proof_status="unsigned support",
            if_signed="relative species prefactors are not legal endomorphisms; only common calibration remains.",
            obstruction="sort disjointness/no-Hom is written but not parent-derived for the actual matter category.",
            source_anchor="1896:NHG1896_1_no_species_hom;1045:MFS1045_2_matter_bundle_functor",
        ),
        base_row(
            theorem_id="MNO2646_3_constant_owner_separation",
            claim_piece="constants are not active source weights",
            formal_statement="Masses, charges, spectra, alpha and binding data may be representation/current standards, but that ownership does not license a separate gravitational source multiplier.",
            status="SEPARATION_CLEAN_NOT_ZERO_PROOF",
            proof_status="support only",
            if_signed="prevents smuggling Delta_w_species under alpha/mass/clock language.",
            obstruction="fixed constants and source-current exclusion are separate owner clauses and neither is fully parent-signed.",
            source_anchor="1098:OCS1098_4_source_weight_exclusion;1488:FCR1488_2_common_calibration",
        ),
        base_row(
            theorem_id="MNO2646_4_measure_action_density_line",
            claim_piece="single action-density line owner",
            formal_statement="All ordinary sectors integrate into the same parent action-density line with one measure/hbar normalization and no species-only Jacobian.",
            status="ACTION_DENSITY_LINE_OWNER_NOT_DERIVED",
            proof_status="open",
            if_signed="relative action weights cannot hide as a measure convention.",
            obstruction="constructor exhaustion/action-scale owner and hbar/measure descent remain unsigned.",
            source_anchor="1904:ASO1904_4_parent_gap;1888:ASO1888_7_verdict",
        ),
        base_row(
            theorem_id="MNO2646_5_countermodel",
            claim_piece="source-only relative weight countermodel",
            formal_statement="S_matter=sum_A(1+epsilon_A)S_A can preserve many ordinary equations/readouts while Hilbert variation yields a weighted active source.",
            status="COUNTERMODEL_RETAINED",
            proof_status="blocks promotion",
            if_signed="none; this is the failure mode a real parent theorem must kill.",
            obstruction="classical EOM division, Ward identities, and field redefinitions do not remove the active Hilbert source weighting in general.",
            source_anchor="2645:NSP2645_5_pre_action_countermodel;1098:FV1098_6_source_weight_X",
        ),
        base_row(
            theorem_id="MNO2646_6_verdict",
            claim_piece="promote matter-normalization owner for current branch",
            formal_statement="ordinary matter standards fully own normalization and exclude every active-source-only relative coefficient before variation",
            status="MATTER_NORMALIZATION_OWNER_NOT_DERIVED",
            proof_status="failed-to-close",
            if_signed="Delta_w_species and its JH/DqZ injections collapse to zero.",
            obstruction="parent matter category, one action-density line, source-weight exclusion, no-Hom sort disjointness, and readout/radiative closure remain unsigned together.",
            source_anchor="MNO2646_0 through MNO2646_5",
        ),
    ]


def standard_owner_audit_rows() -> list[dict[str, Any]]:
    return [
        base_row(
            audit_id="SOA2646_0_matter_bundle",
            standard="ordinary matter bundle/action signature",
            owner_requirement="Psi_A, e_obs, A_obs and theta_A are assigned by one parent matter functor before local tests.",
            current_status="MATTER_CATEGORY_NOT_PARENT_CONSTRUCTED",
            gap="no corpus-level parent matter category/action signature is signed for all ordinary species.",
            source_anchor="1045:MFS1045_2_matter_bundle_functor;1088:MOMS1088_0_action_form",
        ),
        base_row(
            audit_id="SOA2646_1_source_weight_exclusion",
            standard="active gravitational source current",
            owner_requirement="J_H is the observed-coframe Hilbert derivative of the same common matter action; no w_A, kappa_A or material-only source multiplier.",
            current_status="UNSIGNED_SOURCE_WEIGHT_EXCLUSION",
            gap="source-current Ward conservation does not by itself choose species-blind source coupling.",
            source_anchor="1098:OCS1098_4_source_weight_exclusion;2645:NSP2645_4_Ward_support_not_proof",
        ),
        base_row(
            audit_id="SOA2646_2_constants",
            standard="mass/charge/alpha/clock constants",
            owner_requirement="constants are fixed representation/superselection data or explicit retained residual fields with their own projections.",
            current_status="CONSTANT_OWNER_NOT_SOURCE_OWNER",
            gap="constant ownership can remove some marker channels, but it does not prove no active-source-only prefactor.",
            source_anchor="1488:FCR1488_3_verdict;1891:MNO1891_3_countermodel",
        ),
        base_row(
            audit_id="SOA2646_3_action_measure",
            standard="hbar/action measure/common density line",
            owner_requirement="one action scale and one measure/Jacobian for all ordinary sectors.",
            current_status="ACTION_SCALE_OWNER_NOT_PARENT_SIGNED",
            gap="species-only measure Jacobians can mimic Delta_w unless parent-forbidden.",
            source_anchor="1904:ASO1904_4_parent_gap;1888:ASO1888_7_verdict",
        ),
        base_row(
            audit_id="SOA2646_4_readout_radiative",
            standard="effective/readout closure",
            owner_requirement="forbidden source weights do not return through boundary terms, readout maps, renormalization, or material markers.",
            current_status="READOUT_RADIATIVE_CLOSURE_UNSIGNED",
            gap="bare action silence would not be enough for clock/WEP/PPN scoring without this closure.",
            source_anchor="2645:NSP2645_6_measure_coframe_readout;2214:DSD2214_0_exact_chain_rule",
        ),
        base_row(
            audit_id="SOA2646_5_verdict",
            standard="complete matter-normalization owner",
            owner_requirement="matter bundle + source-current owner + fixed constants + action-density line + readout closure all parent-signed together.",
            current_status="OWNER_PACKAGE_NOT_DERIVED",
            gap="strong conditional path exists, but current branch must retain Delta_w_species.",
            source_anchor="SOA2646_0 through SOA2646_4",
        ),
    ]


def coefficient_rows() -> list[dict[str, Any]]:
    return [
        base_row(
            coefficient_id="DWS2646_0_delta_w_species",
            vector="Xi_JH_DqZ_A",
            component="Delta_w_species",
            coefficient_symbol="epsilon_A",
            definition="relative active-source/action normalization after projecting out the universal common mode",
            basis_formula="w_A = w_common*(1+epsilon_A), with sum_A p_A epsilon_A = 0 for the declared material/source composition vector p_A",
            coefficient_origin="symbolic free coefficient retained because the matter-normalization/no-source-prefactor owner is not parent-derived",
            current_value="SYMBOLIC_FREE_COEFFICIENT_NO_PARENT_VALUE",
            units="dimensionless",
            source_path=str(OUTPUTS["owner_attempt"]),
            source_anchor="MNO2646_6_verdict",
            zero_route_status="MATTER_NORMALIZATION_OWNER_NOT_DERIVED",
            missing_for_claim="parent numeric/symbolic epsilon_A vector or theorem-zero; material basis p_A; no-cancellation norm; tau/K/Qbar/arena projections",
            score_ready="False",
            valid_prediction_row="False",
        ),
        base_row(
            coefficient_id="DWS2646_1_common_mode_projector",
            vector="Delta_w_species",
            component="P_perp_common_mode",
            coefficient_symbol="P_perp",
            definition="projector removing the single universal calibration mode before local scoring",
            basis_formula="Delta_w_species = P_perp w, P_perp = I - u p^T/(p^T u) after p_A is sourced",
            coefficient_origin="common-mode guard; prevents hiding relative source weights in fitted G_N or GM",
            current_value="SYMBOLIC_PROJECTOR_NO_ARENA_COMPOSITION_VECTOR",
            units="dimensionless",
            source_path=str(OUTPUTS["standard_owner_audit"]),
            source_anchor="SOA2646_2_constants;SOA2646_3_action_measure",
            zero_route_status="COMMON_MODE_NOT_RELATIVE_PROOF",
            missing_for_claim="arena composition weights and proof that only the universal silent mode is calibratable",
            score_ready="False",
            valid_prediction_row="False",
        ),
        base_row(
            coefficient_id="DWS2646_2_Xi_injection_rule",
            vector="Xi_JH_DqZ_A",
            component="Delta_w_species_to_JH_DqZ",
            coefficient_symbol="P_source_Delta_w",
            definition="bookkeeping map injecting relative source weights into eps_JH_Z_abs and E_DqZ_A until the owner theorem closes",
            basis_formula="Xi_A gets +||P_source Delta_w_species|| + ||P_DqZ Delta_w_species|| in the declared absolute/no-cancellation norm",
            coefficient_origin="Hilbert variation of weighted action plus Qvis/DqZ chain-rule leakage",
            current_value="SCHEMA_ONLY_PARENT_PROJECTORS_MISSING",
            units="dimensionless residual norm",
            source_path=str(OUTPUTS["coefficient_rows"]),
            source_anchor="2645:XIC2645_2_JH_injection;2645:XIC2645_3_DqZ_injection",
            zero_route_status="SOURCE_PROJECTORS_NOT_DERIVED",
            missing_for_claim="P_source, P_DqZ, material source basis, norm, and parent epsilon_A values",
            score_ready="False",
            valid_prediction_row="False",
        ),
    ]


def projection_requirement_rows() -> list[dict[str, Any]]:
    return [
        base_row(projection_id="PRJ2646_0_core", arena="core coefficient row", formula="Delta_w_species=P_perp{epsilon_A}", required_inputs="parent epsilon_A vector or owner theorem-zero; p_A material/source basis; norm; no-cancellation convention", current_status="SYMBOLIC_COMPONENT_ONLY_PARENT_COEFFICIENT_MISSING", score_ready="False"),
        base_row(projection_id="PRJ2646_1_WEP", arena="WEP/composition tests", formula="eta_AB = tau_WEP * (DeltaQ_AB dot Delta_w_species) plus retained beta/source-test legs", required_inputs="test/source compositions; tau_WEP; force/readout convention; parent epsilon_A vector", current_status="MISSING_WEP_MATERIAL_AND_PARENT_COEFFICIENTS", score_ready="False"),
        base_row(projection_id="PRJ2646_2_R10", arena="R10/short-range", formula="alpha_Delta_w(lambda)=K_R10(lambda)*Qbar_source_test(lambda) dot Delta_w_species", required_inputs="K_R10(lambda); Qbar source-test; tau_R10(lambda); kernel/range convention; real bound curve; parent epsilon_A vector", current_status="MISSING_R10_K_QBAR_TAU_PARENT_COEFFICIENTS", score_ready="False"),
        base_row(projection_id="PRJ2646_3_PPN", arena="PPN/Newton source normalization", formula="Delta PPN_source <= K_PPN*(||Delta_w_species||+||beta_w_source/test||)", required_inputs="weak-field source operator; source/test split; GM common-mode guard; parent epsilon_A vector", current_status="MISSING_PPN_OPERATOR_NORM", score_ready="False"),
        base_row(projection_id="PRJ2646_4_clock", arena="clock/frequency", formula="|Delta nu_i/nu_i| <= |K_clock_i dot Delta_w_species| |tau_clock| after alpha/mass split", required_inputs="clock sensitivity vector; source body composition; tau_clock; constant-owner split", current_status="MISSING_CLOCK_SENSITIVITY_PROJECTION", score_ready="False"),
        base_row(projection_id="PRJ2646_5_orbital", arena="orbital/GM", formula="Delta(GM)_obs/GM <= K_orbital dot Delta_w_species after common GM mode removal", required_inputs="source body composition; orbital convention; tau_orbital; inverse-square/source map; parent epsilon_A vector", current_status="MISSING_ORBITAL_SOURCE_PROJECTION", score_ready="False"),
    ]


def validator_case_rows() -> list[dict[str, Any]]:
    return [
        base_row(case_id="CASE2646_0_owner_unsigned", owner_signed="False", coefficient_value="symbolic_free", projection_ready="False", bound_anchor="False", G_absorption="False", cancellation="False", expected_status="REFUSED_MATTER_NORMALIZATION_OWNER_UNSIGNED"),
        base_row(case_id="CASE2646_1_constant_owner_only", owner_signed="False", coefficient_value="constant_owner_contract", projection_ready="False", bound_anchor="False", G_absorption="False", cancellation="False", expected_status="REFUSED_CONSTANT_OWNER_NOT_SOURCE_OWNER"),
        base_row(case_id="CASE2646_2_nohom_unsigned", owner_signed="False", coefficient_value="nohom_contract_only", projection_ready="False", bound_anchor="False", G_absorption="False", cancellation="False", expected_status="REFUSED_NOHOM_SORTS_NOT_PARENT_SIGNED"),
        base_row(case_id="CASE2646_3_missing_coefficient", owner_signed="True", coefficient_value="missing", projection_ready="True", bound_anchor="False", G_absorption="False", cancellation="False", expected_status="REFUSED_MISSING_PARENT_EPSILON_VECTOR"),
        base_row(case_id="CASE2646_4_bound_anchor", owner_signed="True", coefficient_value="parent_numeric", projection_ready="True", bound_anchor="True", G_absorption="False", cancellation="False", expected_status="REFUSED_BOUND_ANCHOR_NOT_PREDICTION"),
        base_row(case_id="CASE2646_5_missing_projection", owner_signed="True", coefficient_value="parent_numeric", projection_ready="False", bound_anchor="False", G_absorption="False", cancellation="False", expected_status="REFUSED_MISSING_ARENA_PROJECTION"),
        base_row(case_id="CASE2646_6_G_absorption", owner_signed="True", coefficient_value="parent_numeric", projection_ready="True", bound_anchor="False", G_absorption="True", cancellation="False", expected_status="REFUSED_G_ABSORPTION_WITHOUT_COMMON_MODE_PROOF"),
        base_row(case_id="CASE2646_7_cancellation", owner_signed="True", coefficient_value="parent_numeric", projection_ready="True", bound_anchor="False", G_absorption="False", cancellation="True", expected_status="REFUSED_CANCELLATION_ONLY"),
        base_row(case_id="CASE2646_8_schema_only", owner_signed="True", coefficient_value="projector_schema_only", projection_ready="False", bound_anchor="False", G_absorption="False", cancellation="False", expected_status="SCHEMA_ONLY_NOT_EVIDENCE"),
    ]


def classify_case(row: dict[str, Any]) -> str:
    if row.get("coefficient_value") == "constant_owner_contract":
        return "REFUSED_CONSTANT_OWNER_NOT_SOURCE_OWNER"
    if row.get("coefficient_value") == "nohom_contract_only":
        return "REFUSED_NOHOM_SORTS_NOT_PARENT_SIGNED"
    if row.get("owner_signed") != "True":
        return "REFUSED_MATTER_NORMALIZATION_OWNER_UNSIGNED"
    if row.get("bound_anchor") == "True":
        return "REFUSED_BOUND_ANCHOR_NOT_PREDICTION"
    if row.get("G_absorption") == "True":
        return "REFUSED_G_ABSORPTION_WITHOUT_COMMON_MODE_PROOF"
    if row.get("cancellation") == "True":
        return "REFUSED_CANCELLATION_ONLY"
    if row.get("coefficient_value") == "projector_schema_only":
        return "SCHEMA_ONLY_NOT_EVIDENCE"
    if row.get("coefficient_value") == "missing":
        return "REFUSED_MISSING_PARENT_EPSILON_VECTOR"
    if row.get("projection_ready") != "True":
        return "REFUSED_MISSING_ARENA_PROJECTION"
    return "FINITE_COEFFICIENT_READY_NONCLAIM"


def validator_result_rows(cases: list[dict[str, Any]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for case in cases:
        observed = classify_case(case)
        row = dict(case)
        row.update(
            {
                "observed_status": observed,
                "status_matches_expected": str(observed == case["expected_status"]),
                "valid_prediction_row": "False",
                "score_ready": "False",
                "valid_for_claim": "False",
                "claim_allowed": "False",
            }
        )
        rows.append(row)
    return rows


def claim_gate_rows() -> list[dict[str, Any]]:
    return [
        base_row(gate_id="CG2646_0_owner_theorem", claim="matter-normalization owner is parent-signed", allowed="False", blocker="parent matter category/action-density line/source-weight exclusion package remains unsigned"),
        base_row(gate_id="CG2646_1_delta_w_zero", claim="Delta_w_species theorem-zero", allowed="False", blocker="owner theorem not derived and source-only prefactor countermodel retained"),
        base_row(gate_id="CG2646_2_coefficient_score", claim="Delta_w_species coefficient row is score-ready", allowed="False", blocker="epsilon_A vector, p_A basis, norm and arena projections are missing"),
        base_row(gate_id="CG2646_3_arena_predictions", claim="WEP/R10/PPN/clock/orbital predictions exist", allowed="False", blocker="projection requirements are contracts, not predictions"),
        base_row(gate_id="CG2646_4_GR_Newton_reduction", claim="local GR/Newton source coupling is derived", allowed="False", blocker="finite Xi_JH_DqZ_A coupling residual remains live"),
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        base_row(
            decision_id="DEC2646_0_theorem_result",
            decision="MATTER_NORMALIZATION_OWNER_NOT_DERIVED",
            rationale="The double-counting/no-Hom route is sharp, but current sources do not sign the parent matter category, action-density line, source-weight exclusion, and readout closure together.",
            consequence="do not claim Delta_w_species=0.",
        ),
        base_row(
            decision_id="DEC2646_1_component_result",
            decision="DELTA_W_SPECIES_RETAINED_AS_SYMBOLIC_COEFFICIENT_ROW",
            rationale="The coupling gap is now an explicit component with units, source anchor, common-mode projector, and arena projection requirements.",
            consequence="future testing can target a declared vector instead of vague coupling debt.",
        ),
        base_row(
            decision_id="DEC2646_2_next_strategy",
            decision="SELECT_2647_ORDINARY_MATTER_ACTION_SIGNATURE_OR_DELTAW_PROJECTION_KERNELS",
            rationale="The least-handwavy next route is to sign the ordinary matter action signature; the empirical fallback is to build actual projection kernels while keeping epsilon_A nonclaim.",
            consequence="move from owner language to a concrete parent action signature/projection-kernel gate.",
        ),
    ]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        base_row(
            next_id="NEXT2646_0_selected",
            next_doc="2647-Y5-R2FR-ordinary-matter-action-signature-or-Delta-w-projection-kernels.md",
            next_script="scripts/Y5_R2FR_ordinary_matter_action_signature_or_Delta_w_projection_kernels_2647.py",
            objective="Try to parent-sign the ordinary-matter action signature that owns e_obs, A_obs, theta_A, J_H and no w_A slots; if it fails, build nonclaim WEP/R10/PPN/clock/orbital projection kernels for Delta_w_species.",
            include="single matter functor; action-density line; no-Hom source slot; common-mode projector; arena p_A vectors; tau/K/Qbar kernel contracts",
            exclude="constant-owner shortcut; Ward-only proof; field-rescaling/classical-EOM proof; G_N/GM absorption; bound-as-prediction; local-GR/Newton claim; GitHub action; formalization-workbench edits",
        )
    ]


def branch_copy_rows(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    copy_rows: list[dict[str, Any]] = []
    for copy_id, path in BRANCH_COPIES.items():
        write_csv(path, rows)
        copy_rows.append(
            base_row(
                copy_id=copy_id,
                copy_path=str(path),
                path_exists=str(path.exists()),
                csv_parses=str(csv_parses(path)),
                contents="2646 Delta_w_species coefficient rows, nonclaim",
            )
        )
    return copy_rows


def validation_rows(generated_paths: list[Path], rows_by_name: dict[str, list[dict[str, Any]]]) -> list[dict[str, Any]]:
    source_rows = rows_by_name["source_register"]
    owner_rows = rows_by_name["owner_attempt"]
    audit_rows = rows_by_name["standard_owner_audit"]
    coefficient_rows_ = rows_by_name["coefficient_rows"]
    projection_rows = rows_by_name["projection_requirements"]
    result_rows = rows_by_name["validator_results"]
    gate_rows = rows_by_name["claim_gates"]
    decision_rows_ = rows_by_name["decision"]
    next_rows = rows_by_name["next_target"]
    branch_rows = rows_by_name["branch_copies"]
    checks = [
        ("VAL2646_00_sources", all(row["path_exists"] == "True" and row["needles_present"] == "True" for row in source_rows), "all cited source paths exist and required needles are present"),
        ("VAL2646_01_owner_not_promoted", any(row["theorem_id"] == "MNO2646_6_verdict" and row["status"] == "MATTER_NORMALIZATION_OWNER_NOT_DERIVED" for row in owner_rows), "matter-normalization owner is not promoted"),
        ("VAL2646_02_nohom_conditional_only", any(row["theorem_id"] == "MNO2646_2_natural_nohom_route" and row["status"] == "EXACT_IF_PARENT_SORTS_SIGNED" for row in owner_rows), "no-Hom route retained as conditional"),
        ("VAL2646_03_owner_audit_complete", any(row["audit_id"] == "SOA2646_5_verdict" and row["current_status"] == "OWNER_PACKAGE_NOT_DERIVED" for row in audit_rows), "owner package audit remains unsigned"),
        ("VAL2646_04_coefficient_nonclaim", any(row["coefficient_id"] == "DWS2646_0_delta_w_species" and row["current_value"] == "SYMBOLIC_FREE_COEFFICIENT_NO_PARENT_VALUE" and row["score_ready"] == "False" for row in coefficient_rows_), "Delta_w_species coefficient row is symbolic nonclaim"),
        ("VAL2646_05_projection_requirements", {"PRJ2646_1_WEP", "PRJ2646_2_R10", "PRJ2646_3_PPN", "PRJ2646_4_clock", "PRJ2646_5_orbital"}.issubset({row["projection_id"] for row in projection_rows}), "WEP/R10/PPN/clock/orbital projection requirements are present"),
        ("VAL2646_06_validator_refusals", all(row["status_matches_expected"] == "True" and row["valid_for_claim"] == "False" for row in result_rows), "validator refuses owner/coefficient shortcuts"),
        ("VAL2646_07_claim_gates_false", all(row["allowed"] == "False" and row["valid_for_claim"] == "False" for row in gate_rows), "all claim gates remain blocked"),
        ("VAL2646_08_decision_next", any(row["decision"] == "SELECT_2647_ORDINARY_MATTER_ACTION_SIGNATURE_OR_DELTAW_PROJECTION_KERNELS" for row in decision_rows_), "decision selects 2647 action signature/projection kernels"),
        ("VAL2646_09_next_target", any(row["next_doc"].startswith("2647-Y5-R2FR-ordinary-matter-action-signature") for row in next_rows), "2647 next target is recorded"),
        ("VAL2646_10_branch_copies", all(row["path_exists"] == "True" and row["csv_parses"] == "True" for row in branch_rows), "branch copies exist and parse"),
        ("VAL2646_11_csv_parse", all(csv_parses(path) for path in generated_paths if path.suffix.lower() == ".csv"), "all generated CSVs parse cleanly"),
        ("VAL2646_12_formalization_untouched", not formalization_has_2646_artifacts(), "no 2646 outputs are written under formalization-workbench"),
        ("VAL2646_13_pycache_absent", not (ROOT / "scripts" / "__pycache__").exists(), "scripts __pycache__ absent"),
    ]
    rows = [base_row(validation_id=check_id, status="PASS" if passed else "FAIL", detail=detail) for check_id, passed, detail in checks]
    rows.append(
        base_row(
            validation_id="VAL2646_OVERALL",
            status="PASS" if all(row["status"] == "PASS" for row in rows) else "FAIL",
            detail="2646 keeps matter-normalization owner unsigned, stages Delta_w_species coefficient rows, and selects ordinary matter action signature/projection kernels next",
        )
    )
    return rows


def write_doc(rows_by_name: dict[str, list[dict[str, Any]]]) -> None:
    DOC_PATH.write_text(
        "\n\n".join(
            [
                "# 2646 - Y5/R2FR Matter-Normalization Owner Or Delta-w Species Coefficient Source Row",
                "**Status:** derivation-first coupling checkpoint. The conditional double-counting/no-Hom route is sharp, but the parent matter-normalization owner is still not derived.",
                "**Main result:** `Delta_w_species` is retained as a symbolic, dimensionless, nonclaim coefficient row inside `Xi_JH_DqZ_A`; no WEP/R10/PPN/clock/orbital/local-GR claim follows.",
                "## Source register",
                md_table(rows_by_name["source_register"], ["source_id", "role", "source_path", "path_exists", "needles_present", "valid_for_claim"]),
                "## Matter-normalization owner theorem attempt",
                md_table(rows_by_name["owner_attempt"], ["theorem_id", "claim_piece", "status", "formal_statement", "proof_status", "obstruction", "source_anchor", "valid_for_claim"]),
                "## Standard owner audit",
                md_table(rows_by_name["standard_owner_audit"], ["audit_id", "standard", "owner_requirement", "current_status", "gap", "source_anchor", "valid_for_claim"]),
                "## Delta_w species coefficient rows",
                md_table(rows_by_name["coefficient_rows"], ["coefficient_id", "vector", "component", "coefficient_symbol", "basis_formula", "current_value", "zero_route_status", "missing_for_claim", "score_ready", "valid_prediction_row", "valid_for_claim"]),
                "## Projection requirements",
                md_table(rows_by_name["projection_requirements"], ["projection_id", "arena", "formula", "required_inputs", "current_status", "score_ready", "valid_for_claim"]),
                "## Validator cases",
                md_table(rows_by_name["validator_cases"], ["case_id", "expected_status", "valid_for_claim"]),
                "## Validator results",
                md_table(rows_by_name["validator_results"], ["case_id", "observed_status", "status_matches_expected", "valid_prediction_row", "score_ready", "valid_for_claim"]),
                "## Claim gates",
                md_table(rows_by_name["claim_gates"], ["gate_id", "claim", "allowed", "blocker", "valid_for_claim"]),
                "## Decision ledger",
                md_table(rows_by_name["decision"], ["decision_id", "decision", "rationale", "consequence", "valid_for_claim"]),
                "## Next target",
                md_table(rows_by_name["next_target"], ["next_id", "next_doc", "next_script", "objective", "include", "exclude", "valid_for_claim"]),
                "## Branch copies",
                md_table(rows_by_name["branch_copies"], ["copy_id", "copy_path", "path_exists", "csv_parses", "contents", "valid_for_claim"]),
                "## Validation",
                md_table(rows_by_name["validation"], ["validation_id", "status", "detail", "valid_for_claim"]),
            ]
        )
        + "\n",
        encoding="utf-8",
    )


def main() -> None:
    for directory in (RESIDUALS, QUEUE, LOCAL_BOUNDS, SOURCE_WEIGHT, MICROSCOPE):
        directory.mkdir(parents=True, exist_ok=True)
    remove_pycache()

    cases = validator_case_rows()
    rows_by_name: dict[str, list[dict[str, Any]]] = {
        "source_register": source_register_rows(),
        "owner_attempt": owner_attempt_rows(),
        "standard_owner_audit": standard_owner_audit_rows(),
        "coefficient_rows": coefficient_rows(),
        "projection_requirements": projection_requirement_rows(),
        "validator_cases": cases,
        "validator_results": validator_result_rows(cases),
        "claim_gates": claim_gate_rows(),
        "decision": decision_rows(),
        "next_target": next_target_rows(),
    }
    rows_by_name["branch_copies"] = branch_copy_rows(rows_by_name["coefficient_rows"])

    for name, rows in rows_by_name.items():
        if name in OUTPUTS and name != "validation":
            write_csv(OUTPUTS[name], rows)

    generated = [path for key, path in OUTPUTS.items() if key != "validation"] + list(BRANCH_COPIES.values())
    rows_by_name["validation"] = validation_rows(generated, rows_by_name)
    write_csv(OUTPUTS["validation"], rows_by_name["validation"])
    write_doc(rows_by_name)
    remove_pycache()


if __name__ == "__main__":
    main()

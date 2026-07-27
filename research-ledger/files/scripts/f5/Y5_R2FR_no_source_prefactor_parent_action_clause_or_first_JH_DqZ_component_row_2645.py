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
DOC_PATH = ROOT / "2645-Y5-R2FR-no-source-prefactor-parent-action-clause-or-first-JH-DqZ-component-row.md"

CHECKPOINT = "2645"
BRANCH_ID = "Y5_R2FR_NO_SOURCE_PREFACTOR_OR_FIRST_JH_DQZ_COMPONENT_ROW_2645"
PREFIX = "P8_Y5_NO_SOURCE_PREFACTOR_2645"

OUTPUTS = {
    "source_register": RESIDUALS / f"{PREFIX}_SOURCE_REGISTER.csv",
    "clause_attempt": RESIDUALS / f"{PREFIX}_PARENT_ACTION_CLAUSE_ATTEMPT.csv",
    "component_rows": RESIDUALS / f"{PREFIX}_FIRST_XI_JH_DQZ_COMPONENT_ROW_NONCLAIM.csv",
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
    "queue": QUEUE / "JR2645_NO_SOURCE_PREFACTOR_OR_XI_COMPONENT_NONCLAIM.csv",
    "local_bounds": LOCAL_BOUNDS / "JH_DqZ_Delta_w_component_2645_NONCLAIM.csv",
    "source_weight": SOURCE_WEIGHT / "DELTAW_SPECIES2645_FIRST_JH_DQZ_COMPONENT_ROW_NONCLAIM.csv",
    "microscope": MICROSCOPE / "P8_Y5_2645_DELTAW_JH_DQZ_WEP_NONCLAIM.csv",
}

SOURCES = [
    {
        "source_id": "SRC2645_00_2644",
        "role": "immediate Qvis/JH/DqZ finite-vector handoff",
        "path": ROOT / "2644-Y5-R2FR-Qvis-object-language-no-source-slot-or-finite-JH-DqZ-vector.md",
        "needles": ["QOL2644_3_no_source_prefactor", "FJV2644_0_master_vector", "VAL2644_OVERALL"],
    },
    {
        "source_id": "SRC2645_01_1890",
        "role": "direct no-source-prefactor theorem attempt and first Delta_w row",
        "path": ROOT / "1890-Y5-R2FR-no-source-prefactor-parent-action-clause-or-component-basis-first-source-row.md",
        "needles": ["NSP1890_7_verdict", "DWS1890_0_species_prefactor_component", "VAL1890_OVERALL"],
    },
    {
        "source_id": "SRC2645_02_1889",
        "role": "Ward owner support and pre-action weight countermodel",
        "path": ROOT / "1889-Y5-R2FR-source-current-Ward-owner-or-real-deltaw-component-basis.md",
        "needles": ["SWO1889_5_pre_action_weight_leak", "CB1889_1_pre_action_species_prefactor", "VAL1889_OVERALL"],
    },
    {
        "source_id": "SRC2645_03_1888",
        "role": "action-scale owner and finite Delta_w vector",
        "path": ROOT / "1888-Y5-R2FR-action-scale-owner-readout-stability-or-finite-deltaw-vector.md",
        "needles": ["ASO1888_7_verdict", "FDV1888_0_core_vector", "VAL1888_OVERALL"],
    },
    {
        "source_id": "SRC2645_04_1886",
        "role": "common matter no-source-only slot proof attempt",
        "path": ROOT / "1886-Y5-R2FR-common-matter-no-source-only-slot-proof-or-finite-wR-row.md",
        "needles": ["NSS1886_7_verdict", "CMS1886_6_verdict", "VAL1886_OVERALL"],
    },
    {
        "source_id": "SRC2645_05_1628",
        "role": "Hilbert source-owner conditional and pre-action counterexample",
        "path": ROOT / "1628-Y5-R2FR-matter-descent-source-owner-certificate-or-JR-bound-acquisition.md",
        "needles": ["SOC1628_1_hilbert_owner", "CE1628_0_pre_action_weight", "VAL1628_OVERALL"],
    },
    {
        "source_id": "SRC2645_06_2214",
        "role": "chain-rule source/DqZ coefficient map",
        "path": ROOT / "2214-Y5-R2FR-algebraic-residual-coefficient-map-or-DqZ-source-descent-proof.md",
        "needles": ["DSD2214_0_exact_chain_rule", "CM2214_1_J_source", "VAL2214_OVERALL"],
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


def formalization_has_2645_artifacts() -> bool:
    if not FORMALIZATION.exists():
        return False
    patterns = (
        "*2645-Y5-R2FR*",
        "*P8_Y5_NO_SOURCE_PREFACTOR_2645*",
        "*P8_Y5_BRR545_2645*",
        "*Y5_R2FR_no_source_prefactor_parent_action_clause_or_first_JH_DqZ_component_row_2645*",
        "*JR2645*",
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


def clause_attempt_rows() -> list[dict[str, Any]]:
    return [
        base_row(
            clause_id="NSP2645_0_target",
            clause="parent no-source-prefactor/no-double-counting matter-normalization clause",
            formal_statement="Allowed[S_matter] excludes w_A(Z)S_A, kappa_A(Z)T_A, and source-only species weights unless the factor is universal, derivative-silent, and removed by the common-mode calibration.",
            status="TARGET_EXACT",
            proof_status="not proven",
            consequence_if_signed="Delta_w_species, beta_w_source/test, w_R and the source part of Xi_JH_DqZ_A become theorem-zero after the common-mode guard.",
            missing_to_claim="parent action-scale owner, matter-normalization owner, typed source-label forgetting, no-spurion/readout stability, and measure/coframe descent",
            source_anchor="2644:QOL2644_3_no_source_prefactor;1890:NSP1890_7_verdict",
        ),
        base_row(
            clause_id="NSP2645_1_exact_if_signed",
            clause="Hilbert source owner after common action is fixed",
            formal_statement="If S_matter=sum_A S_A[Psi_A,Q_vis,theta_A] and T_total=delta S_matter/delta Q_vis, the source object is T_total rather than the labeled set {(T_A,A)}.",
            status="EXACT_CONDITIONAL",
            proof_status="conditional only",
            consequence_if_signed="post-variation source rescaling is killed and source-label forgetting can be applied cleanly.",
            missing_to_claim="the same parent package must first forbid pre-action source weights.",
            source_anchor="1628:SOC1628_1_hilbert_owner;1890:NSP1890_1_exact_conditional_lemma",
        ),
        base_row(
            clause_id="NSP2645_2_action_scale_owner",
            clause="single action/measure/hbar owner",
            formal_statement="All ordinary matter sectors share one parent action scale and one species-blind measure/Jacobian before variation.",
            status="ACTION_SCALE_OWNER_NOT_DERIVED",
            proof_status="open",
            consequence_if_signed="relative weights cannot be hidden as arbitrary action normalizations.",
            missing_to_claim="hbar_parent, Dmu_parent/Jacobian, current owner, path-integral/statistical measure and readout stability in one parent theorem",
            source_anchor="1888:ASO1888_7_verdict",
        ),
        base_row(
            clause_id="NSP2645_3_source_label_forgetting",
            clause="source functor forgets species labels",
            formal_statement="The gravitational/source functor accepts only the total observed source object and not a source-domain label capable of carrying w_A.",
            status="TYPED_OBJECT_LANGUAGE_NOT_PARENT_SIGNED",
            proof_status="open",
            consequence_if_signed="species-indexed active-source multipliers become ill-typed.",
            missing_to_claim="parent object-language constructor list plus no hidden marker/spurion return",
            source_anchor="1886:NSS1886_7_verdict;1889:CB1889_1_pre_action_species_prefactor",
        ),
        base_row(
            clause_id="NSP2645_4_Ward_support_not_proof",
            clause="Ward conservation is support, not proof",
            formal_statement="Ward identities conserve the current selected by the action; they do not by themselves select species-blind gravitational coupling.",
            status="SUPPORT_ONLY_NOT_PROOF",
            proof_status="insufficient route",
            consequence_if_signed="Ward/current owner can police a signed common action, but cannot ban w_A alone.",
            missing_to_claim="no-source-prefactor clause must be independent of the Ward identity.",
            source_anchor="1889:SWO1889_5_pre_action_weight_leak",
        ),
        base_row(
            clause_id="NSP2645_5_pre_action_countermodel",
            clause="pre-action weighted matter countermodel",
            formal_statement="S_matter=sum_A w_A S_A can remain covariant, additive, and Ward-compatible while Hilbert variation yields T_source=sum_A w_A T_A.",
            status="COUNTERMODEL_SURVIVES",
            proof_status="blocks theorem-zero",
            consequence_if_signed="none; this is the live obstruction that forces a parent grammar theorem or finite component row.",
            missing_to_claim="parent rule making w_A untypeable rather than merely absent from a preferred ansatz",
            source_anchor="1628:CE1628_0_pre_action_weight;1889:SWO1889_5_pre_action_weight_leak;1890:NSP1890_6_countermodel",
        ),
        base_row(
            clause_id="NSP2645_6_measure_coframe_readout",
            clause="measure/coframe/readout descent without representative source slots",
            formal_statement="The observed coframe, source measure, boundary projector and readout map must descend through Q_vis without carrying a representative-dependent source coefficient.",
            status="DESCENT_PACKAGE_UNSIGNED",
            proof_status="open",
            consequence_if_signed="pre-action, boundary, coframe and readout source leaks can be separated from true matter data.",
            missing_to_claim="Dq/tau projectability, no boundary projector leak, no qbar/theta marker and no b_g observed-frame leak",
            source_anchor="2214:DSD2214_0_exact_chain_rule;2644:FJV2644_0_master_vector",
        ),
        base_row(
            clause_id="NSP2645_7_verdict",
            clause="no-source-prefactor theorem is derived",
            formal_statement="parent matter-normalization owner + typed object language + single action/measure owner + no marker/readout spurion => partial S_matter/partial w_A undefined.",
            status="NO_SOURCE_PREFACTOR_PARENT_CLAUSE_NOT_DERIVED",
            proof_status="failed-to-close",
            consequence_if_signed="local-GR source side could move from finite Xi vector to a projected-mass/left-hand-side gate.",
            missing_to_claim="the parent action still lacks a signed theorem that forbids w_A(Z)S_A before variation.",
            source_anchor="NSP2645_0 through NSP2645_6",
        ),
    ]


def component_rows() -> list[dict[str, Any]]:
    return [
        base_row(
            component_id="XIC2645_0_master_slot",
            vector="Xi_JH_DqZ_A",
            symbol="Xi_A",
            component="master local source/readout residual vector",
            formula="Xi_A = eps_JH_Z_abs + E_DqZ_A + Delta_w_species_A + beta_w_source/test_A + eps_theta_marker_A + qbar_marker_A + b_g_A + boundary_projector_A",
            coefficient_origin="2644 finite-vector contract",
            units="dimensionless residual norm after declared projection",
            current_value="MISSING_COMPONENT_VALUES",
            status="VECTOR_CONTRACT_READY_VALUES_MISSING",
            arenas="Newton;PPN;WEP;R10;clock;EM;orbital",
            score_ready="False",
        ),
        base_row(
            component_id="XIC2645_1_Delta_w_species",
            vector="Xi_JH_DqZ_A",
            symbol="Delta_w_species",
            component="relative pre-variation species/action/source prefactor after common-mode projection",
            formula="w_A = w_common*(1+epsilon_A), with sum_A p_A epsilon_A = 0 for the declared material/source weights p_A",
            coefficient_origin="pre-action source-only prefactor w_A S_A if no-source-prefactor theorem fails",
            units="dimensionless",
            current_value="MISSING_PARENT_NUMERIC_COEFFICIENT",
            status="NONCLAIM_COMPONENT_DEFINED_NUMERIC_VALUE_MISSING",
            source_anchor="1890:DWS1890_0_species_prefactor_component;1889:CB1889_1_pre_action_species_prefactor",
            required_to_score="parent theorem-zero or numeric epsilon_A vector with component basis, norm, source path, tau, K/Qbar and material projections",
            arenas="WEP;R10;PPN;clock;orbital;Newton source normalization",
            score_ready="False",
        ),
        base_row(
            component_id="XIC2645_2_JH_injection",
            vector="Xi_JH_DqZ_A",
            symbol="eps_JH_Z_abs <- Delta_w_species",
            component="source-current forcing induced by relative action/source weights",
            formula="eps_JH_Z_abs includes ||P_source Delta_w_species|| in the declared no-cancellation norm",
            coefficient_origin="Hilbert source of weighted action",
            units="dimensionless source-current residual",
            current_value="MISSING_PARENT_PROJECTION_AND_NORM",
            status="NONCLAIM_INJECTION_RULE_ONLY",
            source_anchor="1628:SOC1628_1_hilbert_owner;2214:CM2214_1_J_source",
            required_to_score="basis projector P_source, material weights, no-cancellation norm and parent coefficient values",
            arenas="Newton;PPN;WEP",
            score_ready="False",
        ),
        base_row(
            component_id="XIC2645_3_DqZ_injection",
            vector="Xi_JH_DqZ_A",
            symbol="E_DqZ_A <- Delta_w_species",
            component="DqZ/source descent leak if the weighted source retains a vertical representative label",
            formula="E_DqZ_A gets a Delta_w contribution unless the source functor both forgets A and descends through Q_vis.",
            coefficient_origin="Qvis chain-rule map plus source-label countermodel",
            units="dimensionless projected descent residual",
            current_value="MISSING_DqZ_SOURCE_LABEL_PROJECTOR",
            status="NONCLAIM_INJECTION_RULE_ONLY",
            source_anchor="2214:DSD2214_0_exact_chain_rule;2644:FJV2644_0_master_vector",
            required_to_score="DqZ projector, qbar/material marker audit and source-label forgetting theorem or finite coefficient",
            arenas="PPN;WEP;R10;clock",
            score_ready="False",
        ),
        base_row(
            component_id="XIC2645_4_common_mode_guard",
            vector="Delta_w_species",
            symbol="P_perp w",
            component="universal common mode removal",
            formula="P_perp removes the single measured G_N/GM calibration mode; only relative weights may be bounded or zeroed.",
            coefficient_origin="no G_N/GM absorption guard",
            units="dimensionless",
            current_value="PROJECTOR_SCHEMA_ONLY",
            status="COMMON_MODE_GUARD_DEFINED_NO_NUMERIC_VECTOR",
            source_anchor="2644:FJV2644_8_policy",
            required_to_score="declared p_A material/source composition and no-cancellation norm",
            arenas="all local arenas",
            score_ready="False",
        ),
        base_row(
            component_id="XIC2645_5_no_cancellation_policy",
            vector="Xi_JH_DqZ_A",
            symbol="||Xi_A||_1_or_declared_norm",
            component="no cancellation among independent residual heads",
            formula="A local pass cannot rely on cancellation between Delta_w, marker, coframe, boundary or DqZ heads unless a parent identity proves it.",
            coefficient_origin="finite-vector validator guard",
            units="dimensionless residual norm",
            current_value="POLICY_ACTIVE",
            status="GUARD_ACTIVE_NOT_EVIDENCE",
            source_anchor="2644:FJV2644_8_policy",
            required_to_score="independent theorem-zero or source-backed finite bound for every head",
            arenas="all local arenas",
            score_ready="False",
        ),
    ]


def projection_requirement_rows() -> list[dict[str, Any]]:
    return [
        base_row(
            projection_id="PRJ2645_0_core",
            arena="core finite-vector row",
            required_inputs="epsilon_A component basis; p_A common-mode projector; declared norm; coefficient source path; units; no-cancellation policy",
            blocker="MISSING_PARENT_NUMERIC_COEFFICIENT",
            valid_output_if_filled="Delta_w_species finite component row, still nonclaim until arena projections pass",
        ),
        base_row(
            projection_id="PRJ2645_1_WEP",
            arena="WEP/MICROSCOPE-like composition tests",
            required_inputs="source/test material composition vectors; beta_w_source; beta_w_test; Ti/Pt or declared pair sensitivities; tau_WEP; no common-mode absorption",
            blocker="MISSING_SOURCE_TEST_MATERIAL_PROJECTIONS",
            valid_output_if_filled="composition-dependent differential acceleration residual",
        ),
        base_row(
            projection_id="PRJ2645_2_R10",
            arena="R10/short-range force",
            required_inputs="tau_R10(lambda); K_X; Qbar_XH; material/source composition; lambda_X; contact/finite-range mapping; real bound curve row",
            blocker="MISSING_TAU_R10_K_QBAR_LAMBDA_PROJECTION",
            valid_output_if_filled="alpha(lambda) prediction row, not a bound-anchor shortcut",
        ),
        base_row(
            projection_id="PRJ2645_3_PPN",
            arena="PPN/Newton source normalization",
            required_inputs="map from Delta_w_species to gamma/beta/source mass; inertial vs active source split; common GM calibration guard; environment dependence",
            blocker="MISSING_PPN_SOURCE_PROJECTION",
            valid_output_if_filled="PPN residual vector with common-mode removed",
        ),
        base_row(
            projection_id="PRJ2645_4_clock",
            arena="clock/frequency comparisons",
            required_inputs="clock transition sensitivities to Delta_w basis; tau_clock; material marker audit; source/readout separation",
            blocker="MISSING_CLOCK_SENSITIVITY_PROJECTION",
            valid_output_if_filled="clock residual coefficient row",
        ),
        base_row(
            projection_id="PRJ2645_5_orbital",
            arena="orbital systems",
            required_inputs="active/inertial mass split; GM common-mode removal; body composition/source weights; tau_orbital; secular observable map",
            blocker="MISSING_ORBITAL_SOURCE_PROJECTION",
            valid_output_if_filled="orbital residual vector without hiding relative weights in fitted GM",
        ),
    ]


def validator_case_rows() -> list[dict[str, Any]]:
    return [
        base_row(case_id="CASE2645_0_parent_unsigned", route="theorem_zero", theorem_signed="False", ward_only="False", classical_eom_shortcut="False", field_rescale_shortcut="False", parent_numeric_coefficient="False", tau_projection="False", K_Qbar_projection="False", bound_anchor="False", G_absorption="False", cancellation="False", expected_status="REFUSED_NO_SOURCE_PREFACTOR_UNSIGNED"),
        base_row(case_id="CASE2645_1_Ward_only", route="theorem_zero", theorem_signed="False", ward_only="True", classical_eom_shortcut="False", field_rescale_shortcut="False", parent_numeric_coefficient="False", tau_projection="False", K_Qbar_projection="False", bound_anchor="False", G_absorption="False", cancellation="False", expected_status="REFUSED_WARD_ONLY_NOT_SPECIES_BLIND"),
        base_row(case_id="CASE2645_2_classical_EOM", route="theorem_zero", theorem_signed="False", ward_only="False", classical_eom_shortcut="True", field_rescale_shortcut="False", parent_numeric_coefficient="False", tau_projection="False", K_Qbar_projection="False", bound_anchor="False", G_absorption="False", cancellation="False", expected_status="REFUSED_CLASSICAL_EOM_NOT_SOURCE_UNIVERSALITY"),
        base_row(case_id="CASE2645_3_field_rescale", route="theorem_zero", theorem_signed="False", ward_only="False", classical_eom_shortcut="False", field_rescale_shortcut="True", parent_numeric_coefficient="False", tau_projection="False", K_Qbar_projection="False", bound_anchor="False", G_absorption="False", cancellation="False", expected_status="REFUSED_FIELD_RESCALING_NOT_GENERAL"),
        base_row(case_id="CASE2645_4_missing_numeric", route="finite_component", theorem_signed="False", ward_only="False", classical_eom_shortcut="False", field_rescale_shortcut="False", parent_numeric_coefficient="False", tau_projection="True", K_Qbar_projection="True", bound_anchor="False", G_absorption="False", cancellation="False", expected_status="REFUSED_MISSING_PARENT_NUMERIC_COEFFICIENT"),
        base_row(case_id="CASE2645_5_bound_anchor", route="finite_component", theorem_signed="False", ward_only="False", classical_eom_shortcut="False", field_rescale_shortcut="False", parent_numeric_coefficient="False", tau_projection="True", K_Qbar_projection="True", bound_anchor="True", G_absorption="False", cancellation="False", expected_status="REFUSED_BOUND_ANCHOR_NOT_PREDICTION"),
        base_row(case_id="CASE2645_6_missing_tau", route="finite_component", theorem_signed="False", ward_only="False", classical_eom_shortcut="False", field_rescale_shortcut="False", parent_numeric_coefficient="True", tau_projection="False", K_Qbar_projection="True", bound_anchor="False", G_absorption="False", cancellation="False", expected_status="REFUSED_MISSING_TAU_PROJECTION"),
        base_row(case_id="CASE2645_7_missing_K_Qbar", route="finite_component", theorem_signed="False", ward_only="False", classical_eom_shortcut="False", field_rescale_shortcut="False", parent_numeric_coefficient="True", tau_projection="True", K_Qbar_projection="False", bound_anchor="False", G_absorption="False", cancellation="False", expected_status="REFUSED_MISSING_K_QBAR_PROJECTION"),
        base_row(case_id="CASE2645_8_G_absorption", route="finite_component", theorem_signed="False", ward_only="False", classical_eom_shortcut="False", field_rescale_shortcut="False", parent_numeric_coefficient="True", tau_projection="True", K_Qbar_projection="True", bound_anchor="False", G_absorption="True", cancellation="False", expected_status="REFUSED_G_ABSORPTION_WITHOUT_COMMON_MODE_PROOF"),
        base_row(case_id="CASE2645_9_cancellation", route="finite_component", theorem_signed="False", ward_only="False", classical_eom_shortcut="False", field_rescale_shortcut="False", parent_numeric_coefficient="True", tau_projection="True", K_Qbar_projection="True", bound_anchor="False", G_absorption="False", cancellation="True", expected_status="REFUSED_CANCELLATION_ONLY"),
        base_row(case_id="CASE2645_10_schema_only", route="finite_component", theorem_signed="False", ward_only="False", classical_eom_shortcut="False", field_rescale_shortcut="False", parent_numeric_coefficient="False", tau_projection="False", K_Qbar_projection="False", bound_anchor="False", G_absorption="False", cancellation="False", expected_status="SCHEMA_ONLY_NOT_EVIDENCE"),
    ]


def classify_case(row: dict[str, Any]) -> str:
    if row.get("ward_only") == "True":
        return "REFUSED_WARD_ONLY_NOT_SPECIES_BLIND"
    if row.get("classical_eom_shortcut") == "True":
        return "REFUSED_CLASSICAL_EOM_NOT_SOURCE_UNIVERSALITY"
    if row.get("field_rescale_shortcut") == "True":
        return "REFUSED_FIELD_RESCALING_NOT_GENERAL"
    if row.get("route") == "theorem_zero":
        if row.get("theorem_signed") != "True":
            return "REFUSED_NO_SOURCE_PREFACTOR_UNSIGNED"
        return "THEOREM_ZERO_READY_NONCLAIM"
    if row.get("bound_anchor") == "True":
        return "REFUSED_BOUND_ANCHOR_NOT_PREDICTION"
    if row.get("G_absorption") == "True":
        return "REFUSED_G_ABSORPTION_WITHOUT_COMMON_MODE_PROOF"
    if row.get("cancellation") == "True":
        return "REFUSED_CANCELLATION_ONLY"
    if row.get("parent_numeric_coefficient") != "True" and row.get("tau_projection") != "True" and row.get("K_Qbar_projection") != "True":
        return "SCHEMA_ONLY_NOT_EVIDENCE"
    if row.get("parent_numeric_coefficient") != "True":
        return "REFUSED_MISSING_PARENT_NUMERIC_COEFFICIENT"
    if row.get("tau_projection") != "True":
        return "REFUSED_MISSING_TAU_PROJECTION"
    if row.get("K_Qbar_projection") != "True":
        return "REFUSED_MISSING_K_QBAR_PROJECTION"
    return "FINITE_COMPONENT_ROW_SCHEMA_READY_NONCLAIM"


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
        base_row(gate_id="CG2645_0_no_source_prefactor_theorem", claim="parent action forbids pre-action source/species prefactors", allowed="False", blocker="pre-action w_A S_A countermodel survives; owner/typing/descent package unsigned"),
        base_row(gate_id="CG2645_1_Delta_w_species_zero", claim="Delta_w_species theorem-zero", allowed="False", blocker="no-source-prefactor and matter-normalization owner not parent-signed"),
        base_row(gate_id="CG2645_2_finite_component_score", claim="Delta_w_species finite component is score-ready", allowed="False", blocker="numeric parent coefficient, material basis, tau/K/Qbar projections and norm are missing"),
        base_row(gate_id="CG2645_3_local_arena_pass", claim="WEP/R10/PPN/clock/orbital branches pass", allowed="False", blocker="all arena projections remain acquisition requirements, not predictions"),
        base_row(gate_id="CG2645_4_local_GR_Newton_source", claim="local GR/Newton source side is derived", allowed="False", blocker="Xi_JH_DqZ_A remains a finite nonclaim vector; left-hand and projected-mass gates also remain open"),
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        base_row(
            decision_id="DEC2645_0_main_result",
            decision="NO_SOURCE_PREFACTOR_CLAUSE_NOT_DERIVED",
            rationale="Ward conservation, Hilbert ownership and Qvis descent become powerful only after the parent bans pre-action source weights; the current corpus still does not sign that ban.",
            consequence="do not claim local GR/Newton source closure from this route.",
        ),
        base_row(
            decision_id="DEC2645_1_component_row",
            decision="INSTALL_DELTA_W_SPECIES_IN_XI_JH_DQZ_VECTOR",
            rationale="The missing coupling is now represented as an explicit finite residual component rather than a hidden assumption.",
            consequence="WEP/R10/PPN/clock/orbital work must project this component or derive it to zero.",
        ),
        base_row(
            decision_id="DEC2645_2_best_next",
            decision="SELECT_2646_MATTER_NORMALIZATION_OWNER_OR_DELTAW_SPECIES_COEFFICIENT_SOURCE_ROW",
            rationale="The highest-leverage next proof is to derive the matter-normalization owner; failing that, the next honest move is a sourced coefficient row.",
            consequence="attack the coupling directly rather than circling it through arena bounds.",
        ),
    ]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        base_row(
            next_id="NEXT2645_0_selected",
            next_doc="2646-Y5-R2FR-matter-normalization-owner-or-Delta-w-species-coefficient-source-row.md",
            next_script="scripts/Y5_R2FR_matter_normalization_owner_or_Delta_w_species_coefficient_source_row_2646.py",
            objective="Try to derive the parent matter-normalization owner that makes source-only w_A a double-counting/ill-typed object; if it fails, source the first explicit Delta_w_species coefficient row as nonclaim.",
            include="nongravitational representation/current ownership; hbar/action-measure owner; source-label forgetting; common-mode projector; numeric/symbolic coefficient slot; WEP/R10/PPN/clock/orbital projection requirements",
            exclude="Ward-only proof; field-rescaling shortcut; fitted G_N/GM absorption; experimental bound as prediction; local-GR/Newton claim; GitHub action; formalization-workbench edits",
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
                contents="2645 first Xi_JH_DqZ/Delta_w_species nonclaim component row",
            )
        )
    return copy_rows


def validation_rows(generated_paths: list[Path], rows_by_name: dict[str, list[dict[str, Any]]]) -> list[dict[str, Any]]:
    source_rows = rows_by_name["source_register"]
    clause_rows = rows_by_name["clause_attempt"]
    component_rows_ = rows_by_name["component_rows"]
    projection_rows = rows_by_name["projection_requirements"]
    result_rows = rows_by_name["validator_results"]
    gate_rows = rows_by_name["claim_gates"]
    decision_rows_ = rows_by_name["decision"]
    next_rows = rows_by_name["next_target"]
    branch_rows = rows_by_name["branch_copies"]
    checks = [
        ("VAL2645_00_sources", all(row["path_exists"] == "True" and row["needles_present"] == "True" for row in source_rows), "all cited source paths exist and required needles are present"),
        ("VAL2645_01_theorem_not_promoted", any(row["clause_id"] == "NSP2645_7_verdict" and row["status"] == "NO_SOURCE_PREFACTOR_PARENT_CLAUSE_NOT_DERIVED" for row in clause_rows), "no-source-prefactor theorem is not promoted"),
        ("VAL2645_02_Ward_support_only", any(row["clause_id"] == "NSP2645_4_Ward_support_not_proof" and row["status"] == "SUPPORT_ONLY_NOT_PROOF" for row in clause_rows), "Ward owner is retained as support, not a proof"),
        ("VAL2645_03_countermodel_retained", any(row["clause_id"] == "NSP2645_5_pre_action_countermodel" and row["status"] == "COUNTERMODEL_SURVIVES" for row in clause_rows), "pre-action w_A S_A countermodel remains explicit"),
        ("VAL2645_04_component_nonclaim", any(row["component_id"] == "XIC2645_1_Delta_w_species" and row["status"] == "NONCLAIM_COMPONENT_DEFINED_NUMERIC_VALUE_MISSING" and row["score_ready"] == "False" for row in component_rows_), "Delta_w_species first Xi component row is staged as nonclaim"),
        ("VAL2645_05_projection_requirements", {"PRJ2645_1_WEP", "PRJ2645_2_R10", "PRJ2645_3_PPN", "PRJ2645_4_clock", "PRJ2645_5_orbital"}.issubset({row["projection_id"] for row in projection_rows}), "WEP/R10/PPN/clock/orbital projection requirements are present"),
        ("VAL2645_06_validator_refusals", all(row["status_matches_expected"] == "True" and row["valid_for_claim"] == "False" for row in result_rows), "validator refuses unsafe theorem and finite-component shortcuts"),
        ("VAL2645_07_claim_gates_false", all(row["allowed"] == "False" and row["valid_for_claim"] == "False" for row in gate_rows), "all claim gates remain blocked"),
        ("VAL2645_08_decision_next", any(row["decision"] == "SELECT_2646_MATTER_NORMALIZATION_OWNER_OR_DELTAW_SPECIES_COEFFICIENT_SOURCE_ROW" for row in decision_rows_), "decision selects 2646 matter-normalization owner/coefficient route"),
        ("VAL2645_09_next_target", any(row["next_doc"].startswith("2646-Y5-R2FR-matter-normalization-owner") for row in next_rows), "2646 next target is recorded"),
        ("VAL2645_10_branch_copies", all(row["path_exists"] == "True" and row["csv_parses"] == "True" for row in branch_rows), "branch copies exist and parse"),
        ("VAL2645_11_csv_parse", all(csv_parses(path) for path in generated_paths if path.suffix.lower() == ".csv"), "all generated CSVs parse cleanly"),
        ("VAL2645_12_formalization_untouched", not formalization_has_2645_artifacts(), "no 2645 outputs are written under formalization-workbench"),
        ("VAL2645_13_pycache_absent", not (ROOT / "scripts" / "__pycache__").exists(), "scripts __pycache__ absent"),
    ]
    rows = [base_row(validation_id=check_id, status="PASS" if passed else "FAIL", detail=detail) for check_id, passed, detail in checks]
    rows.append(
        base_row(
            validation_id="VAL2645_OVERALL",
            status="PASS" if all(row["status"] == "PASS" for row in rows) else "FAIL",
            detail="2645 refuses no-source-prefactor promotion, installs Delta_w_species as the first Xi_JH_DqZ finite component row, and selects matter-normalization owner as next target",
        )
    )
    return rows


def write_doc(rows_by_name: dict[str, list[dict[str, Any]]]) -> None:
    DOC_PATH.write_text(
        "\n\n".join(
            [
                "# 2645 - Y5/R2FR No-Source-Prefactor Parent Action Clause Or First JH/DqZ Component Row",
                "**Status:** derivation-first coupling checkpoint. The no-source-prefactor clause is still not parent-derived; the pre-action `w_A(Z) S_A` countermodel remains live.",
                "**Main result:** the coupling gap is now made explicit as `Delta_w_species` inside the finite `Xi_JH_DqZ_A` vector. This is not a local-GR/Newton, WEP, R10, PPN, clock, or orbital claim.",
                "## Source register",
                md_table(rows_by_name["source_register"], ["source_id", "role", "source_path", "path_exists", "needles_present", "valid_for_claim"]),
                "## Parent action clause attempt",
                md_table(rows_by_name["clause_attempt"], ["clause_id", "clause", "status", "formal_statement", "proof_status", "missing_to_claim", "source_anchor", "valid_for_claim"]),
                "## First Xi/JH/DqZ component rows",
                md_table(rows_by_name["component_rows"], ["component_id", "vector", "symbol", "component", "formula", "current_value", "status", "required_to_score", "arenas", "score_ready", "valid_for_claim"]),
                "## Projection requirements",
                md_table(rows_by_name["projection_requirements"], ["projection_id", "arena", "required_inputs", "blocker", "valid_output_if_filled", "valid_for_claim"]),
                "## Validator cases",
                md_table(rows_by_name["validator_cases"], ["case_id", "route", "expected_status", "valid_for_claim"]),
                "## Validator results",
                md_table(rows_by_name["validator_results"], ["case_id", "route", "observed_status", "status_matches_expected", "valid_prediction_row", "score_ready", "valid_for_claim"]),
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
        "clause_attempt": clause_attempt_rows(),
        "component_rows": component_rows(),
        "projection_requirements": projection_requirement_rows(),
        "validator_cases": cases,
        "validator_results": validator_result_rows(cases),
        "claim_gates": claim_gate_rows(),
        "decision": decision_rows(),
        "next_target": next_target_rows(),
    }
    rows_by_name["branch_copies"] = branch_copy_rows(rows_by_name["component_rows"])

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

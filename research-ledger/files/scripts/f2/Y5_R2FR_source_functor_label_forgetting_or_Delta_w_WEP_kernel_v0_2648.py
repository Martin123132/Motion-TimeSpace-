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
DOC_PATH = ROOT / "2648-Y5-R2FR-source-functor-label-forgetting-or-Delta-w-WEP-kernel-v0.md"

CHECKPOINT = "2648"
BRANCH_ID = "Y5_R2FR_SOURCE_FUNCTOR_LABEL_FORGETTING_OR_DELTAW_WEP_KERNEL_2648"
PREFIX = "P8_Y5_SOURCE_FUNCTOR_LABEL_FORGETTING_2648"

OUTPUTS = {
    "source_register": RESIDUALS / f"{PREFIX}_SOURCE_REGISTER.csv",
    "label_forgetting_attempt": RESIDUALS / f"{PREFIX}_LABEL_FORGETTING_ATTEMPT.csv",
    "clause_audit": RESIDUALS / f"{PREFIX}_CLAUSE_AUDIT.csv",
    "wep_kernel": RESIDUALS / f"{PREFIX}_DELTAW_WEP_KERNEL_V0_NONCLAIM.csv",
    "wep_requirements": RESIDUALS / f"{PREFIX}_WEP_REQUIREMENTS.csv",
    "validator_cases": RESIDUALS / f"{PREFIX}_VALIDATOR_CASES.csv",
    "validator_results": RESIDUALS / f"{PREFIX}_VALIDATOR_RESULTS.csv",
    "claim_gates": RESIDUALS / f"{PREFIX}_CLAIM_GATES.csv",
    "decision": RESIDUALS / f"{PREFIX}_DECISION_LEDGER.csv",
    "next_target": RESIDUALS / f"{PREFIX}_NEXT_TARGET.csv",
    "branch_copies": RESIDUALS / f"{PREFIX}_BRANCH_COPIES.csv",
    "validation": RESIDUALS / f"P8_Y5_BRR545_{CHECKPOINT}_VALIDATION.csv",
}

BRANCH_COPIES = {
    "queue": QUEUE / "JR2648_SOURCE_LABEL_FORGETTING_WEP_KERNEL_NONCLAIM.csv",
    "local_bounds": LOCAL_BOUNDS / "Delta_w_WEP_kernel_v0_2648_NONCLAIM.csv",
    "source_weight": SOURCE_WEIGHT / "DELTAW_WEP_KERNEL_V0_2648_NONCLAIM.csv",
    "microscope": MICROSCOPE / "P8_Y5_2648_DELTAW_WEP_KERNEL_V0_NONCLAIM.csv",
}

SOURCES = [
    {
        "source_id": "SRC2648_00_2647",
        "role": "immediate ordinary-matter signature handoff",
        "path": ROOT / "2647-Y5-R2FR-ordinary-matter-action-signature-or-Delta-w-projection-kernels.md",
        "needles": ["OMC2647_4_source_functor_label_forgetting", "DK2647_1_WEP", "VAL2647_OVERALL"],
    },
    {
        "source_id": "SRC2648_01_1893",
        "role": "older source-functor label-forgetting and WEP kernel v0",
        "path": ROOT / "1893-Y5-R2FR-source-functor-label-forgetting-or-deltaw-wep-kernel-v0.md",
        "needles": ["SFL1893_5_verdict", "WEPK1893_5_acceptance", "VAL1893_OVERALL"],
    },
    {
        "source_id": "SRC2648_02_1898",
        "role": "readout/variation commutator and WEP row v1 blockers",
        "path": ROOT / "1898-Y5-R2FR-readout-variation-commutator-zero-or-wep-projection-row-v1.md",
        "needles": ["RVC1898_5_verdict", "WEP1898_7_verdict", "VAL1898_OVERALL"],
    },
    {
        "source_id": "SRC2648_03_2645",
        "role": "Hilbert source owner, Ward-not-proof and pre-action countermodel",
        "path": ROOT / "2645-Y5-R2FR-no-source-prefactor-parent-action-clause-or-first-JH-DqZ-component-row.md",
        "needles": ["NSP2645_1_exact_if_signed", "NSP2645_4_Ward_support_not_proof", "NSP2645_5_pre_action_countermodel"],
    },
    {
        "source_id": "SRC2648_04_2646",
        "role": "matter-normalization owner verdict and Delta_w coefficient",
        "path": ROOT / "2646-Y5-R2FR-matter-normalization-owner-or-Delta-w-species-coefficient-source-row.md",
        "needles": ["MNO2646_6_verdict", "DWS2646_0_delta_w_species", "VAL2646_OVERALL"],
    },
    {
        "source_id": "SRC2648_05_1628",
        "role": "Hilbert source owner conditional and pre-action weight counterexample",
        "path": ROOT / "1628-Y5-R2FR-matter-descent-source-owner-certificate-or-JR-bound-acquisition.md",
        "needles": ["SOC1628_1_hilbert_owner", "CE1628_0_pre_action_weight", "VAL1628_OVERALL"],
    },
    {
        "source_id": "SRC2648_06_1889",
        "role": "Ward-owner limitation and source prefactor countermodel",
        "path": ROOT / "1889-Y5-R2FR-source-current-Ward-owner-or-real-deltaw-component-basis.md",
        "needles": ["SWO1889_5_pre_action_weight_leak", "VAL1889_OVERALL"],
    },
    {
        "source_id": "SRC2648_07_1066_tau",
        "role": "tau_WEP projection contract",
        "path": ROOT / "1066-Y5-R10-parent-action-syntax-source-scalar-exclusion-or-WEP-Delta-w-prior-width.md",
        "needles": ["TWP1066_7_verdict", "PROJECTION_CONTRACT_WRITTEN_NOT_DERIVED"],
    },
    {
        "source_id": "SRC2648_08_1080_bound",
        "role": "MICROSCOPE WEP bound anchor",
        "path": ROOT / "1080-Y5-R10-finite-WEP-source-vector-and-material-tensor-acquisition-pack.md",
        "needles": ["BOUND1080_0_MICROSCOPE_WEP_source_charge", "2.8e-15"],
    },
    {
        "source_id": "SRC2648_09_1225_acquisition",
        "role": "tau/readout/source acquisition table",
        "path": ROOT / "1225-Y5-R10-tau-WEP-source-worldtube-readout-projection.md",
        "needles": ["ACQ1225_0_official_readout_arrays", "ACQ1225_1_product_convention", "VAL1225_4_acquisition_table_complete"],
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


def formalization_has_2648_artifacts() -> bool:
    if not FORMALIZATION.exists():
        return False
    patterns = (
        "*2648-Y5-R2FR*",
        "*P8_Y5_SOURCE_FUNCTOR_LABEL_FORGETTING_2648*",
        "*P8_Y5_BRR545_2648*",
        "*Y5_R2FR_source_functor_label_forgetting_or_Delta_w_WEP_kernel_v0_2648*",
        "*JR2648*",
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


def label_forgetting_rows() -> list[dict[str, Any]]:
    return [
        base_row(
            attempt_id="SFL2648_0_target",
            claim_piece="source functor label forgetting",
            formal_statement="q_src({(T_A,A)})=T_total and F_src(q_src({(T_A,A)}))=kappa_univ T_total, with no access to A labels, w_A, kappa_A, material masks, source preparation labels, or post-readout selectors.",
            status="TARGET_SHARP",
            derivation_or_obstruction="this is the narrow theorem that would erase Delta_w_species from the source domain.",
            source_anchor="2647:OMC2647_4_source_functor_label_forgetting;1893:SFL1893_0_target",
        ),
        base_row(
            attempt_id="SFL2648_1_hilbert_owner_if_common_action",
            claim_piece="Hilbert source object",
            formal_statement="If one common action is fixed and varied before readout, J_H=delta S_matter/delta e_obs returns the total Hilbert source object T_total.",
            status="EXACT_CONDITIONAL_SUBTHEOREM",
            derivation_or_obstruction="kills post-variation source rescaling only after common action and no-preaction-weight premises.",
            source_anchor="1628:SOC1628_1_hilbert_owner;2645:NSP2645_1_exact_if_signed",
        ),
        base_row(
            attempt_id="SFL2648_2_ward_not_enough",
            claim_piece="Ward conservation bridge",
            formal_statement="Diffeomorphism invariance conserves the current chosen by the action, but does not choose the source functor domain or forbid species-weighted conserved sums.",
            status="WARD_ONLY_NOT_SPECIES_BLIND",
            derivation_or_obstruction="E_munu=sum_A kappa_A T_A_munu can remain conserved for constant kappa_A if labels survive.",
            source_anchor="1893:SFL1893_1_ward_bridge;1889:SWO1889_5_pre_action_weight_leak",
        ),
        base_row(
            attempt_id="SFL2648_3_conditional_uniqueness",
            claim_piece="label-forgotten covariant additive source",
            formal_statement="If F_src only sees T_total, is local/covariant/additive/natural on one observed coframe, and has one calibrated source scale, then F_src(T_total)=kappa_univ T_total.",
            status="EXACT_CONDITIONAL_THEOREM",
            derivation_or_obstruction="relative weights cannot be formed once source labels are absent, but the label-forgetting quotient is not parent-signed.",
            source_anchor="1893:SFL1893_3_conditional_uniqueness",
        ),
        base_row(
            attempt_id="SFL2648_4_preaction_prefactor_obstruction",
            claim_piece="pre-action weight leak",
            formal_statement="S_matter=sum_A w_A S_A still Hilbert-varies to T_source=sum_A w_A T_A if w_A is legal before variation.",
            status="PRE_ACTION_WEIGHT_COUNTERMODEL_SURVIVES",
            derivation_or_obstruction="source-label forgetting must pair with no pre-action source prefactors and no spurion return.",
            source_anchor="1893:SFL1893_4_prefactor_obstruction;2645:NSP2645_5_pre_action_countermodel",
        ),
        base_row(
            attempt_id="SFL2648_5_verdict",
            claim_piece="promote source-label forgetting for current MTS",
            formal_statement="the parent source functor forgets species labels and returns only total Hilbert stress-energy before coupling selection",
            status="SOURCE_FUNCTOR_LABEL_FORGETTING_NOT_PARENT_DERIVED",
            derivation_or_obstruction="domain quotient, no-prefactor theorem, no spurion/readout return, and projected-mass calibration remain unsigned.",
            source_anchor="SFL2648_0 through SFL2648_4",
        ),
    ]


def clause_audit_rows() -> list[dict[str, Any]]:
    return [
        base_row(clause_id="LFA2648_0_domain_quotient", clause="source-domain quotient q_src exists before coupling", required_identity="q_src maps labelled ordinary matter source family {(T_A,A)} to T_total=sum_A T_A", current_status="SOURCE_DOMAIN_QUOTIENT_NOT_CONSTRUCTED", if_signed="species labels cannot feed coupling selection", if_unsigned="kappa_A or epsilon_A remains legal", source_anchor="1893:SFL1893_0_target"),
        base_row(clause_id="LFA2648_1_no_prefactors", clause="no pre-action source prefactors", required_identity="w_A S_A and kappa_A T_A are illegal parent objects before variation", current_status="NO_SOURCE_PREFACTOR_NOT_DERIVED", if_signed="weighted Hilbert source countermodel killed", if_unsigned="Delta_w_species remains live", source_anchor="2646:MNO2646_6_verdict"),
        base_row(clause_id="LFA2648_2_variation_before_readout", clause="variation before source/readout selection", required_identity="J_H is computed from S_matter before readout/projector/arena maps act", current_status="CONDITIONAL_ONLY", if_signed="postprocessing cannot redefine source", if_unsigned="readout/effective/projector commutators survive", source_anchor="1898:RVC1898_1_pure_postprocessing_zero;1898:RVC1898_5_verdict"),
        base_row(clause_id="LFA2648_3_no_spurion_return", clause="no hidden/readout/domain marker returns labels", required_identity="partial_A kappa=partial_marker kappa=partial_boundary kappa=partial_readout kappa=0", current_status="NO_SPURION_RETURN_NOT_PARENT_SIGNED", if_signed="label forgetting survives boundary/readout routes", if_unsigned="species dependence can return after the source map", source_anchor="1893:LFA1893_3_no_spurion_return"),
        base_row(clause_id="LFA2648_4_projected_mass_calibration", clause="common source scale only after universality", required_identity="kappa_univ/G/GM common mode is calibrated only after no species/time/range/frame dependence is signed", current_status="COMMON_MODE_GUARD_UNSIGNED", if_signed="only one universal source scale remains", if_unsigned="relative weights can hide in calibration", source_anchor="2646:DWS2646_1_common_mode_projector"),
        base_row(clause_id="LFA2648_5_verdict", clause="source-label forgetting is parent-derived", required_identity="LFA2648_0 through LFA2648_4 all parent-signed", current_status="SOURCE_LABEL_FORGETTING_NOT_DERIVED", if_signed="Delta_w_species=0 can be promoted on source side", if_unsigned="WEP kernel v0 remains nonclaim fallback", source_anchor="LFA2648_0 through LFA2648_4"),
    ]


def wep_kernel_rows() -> list[dict[str, Any]]:
    return [
        base_row(
            kernel_id="WEPK2648_0_formula",
            arena="WEP_MICROSCOPE_TiPt",
            object="branch-locked Delta_w WEP product",
            formula="eta_pred(Ti,Pt)=tau_WEP*K_WEP[Earth,orbit,readout,TiPt] dot epsilon_perp",
            normalized_formula="eta_pred=|sum_X C_parent_X * R_material_X(TA6V-PtRh10) * tau_eff_X|",
            current_status="FORMULA_LOCKED_INPUTS_MISSING",
            required_inputs="parent epsilon/C_parent vector; full material tensor; tau_eff/source/readout kernel; product convention; branch lock",
            bound_anchor="2.8e-15 comparator only after eta_pred exists",
            units="dimensionless eta",
            score_ready="False",
            valid_prediction_row="False",
        ),
        base_row(
            kernel_id="WEPK2648_1_parent_coefficient",
            arena="WEP_MICROSCOPE_TiPt",
            object="epsilon_perp or C_parent_X",
            formula="epsilon_perp=P_perp epsilon or C_parent_X=delta S_parent/delta V_WEP,X",
            normalized_formula="same X basis must be shared by parent coefficient, material tensor and tau_eff",
            current_status="MISSING_PARENT_EPSILON_OR_C_PARENT_VECTOR",
            required_inputs="parent numeric/theorem-zero coefficient vector with units/sign/source path",
            bound_anchor="not supplied by MICROSCOPE bound",
            units="dimensionless or declared parent-basis units",
            score_ready="False",
            valid_prediction_row="False",
        ),
        base_row(
            kernel_id="WEPK2648_2_material_tensor",
            arena="WEP_MICROSCOPE_TiPt",
            object="DeltaQ_TiPt / R_material_X",
            formula="full TA6V-minus-PtRh10 response tensor in the same parent basis as epsilon_perp",
            normalized_formula="not DD proxy only and not Ye-only smoke context",
            current_status="MISSING_FULL_PARENT_MATERIAL_TENSOR",
            required_inputs="isotope/alloy averaged material response tensor and double-counting rule",
            bound_anchor="context proxies not claim tensor",
            units="parent-basis response units",
            score_ready="False",
            valid_prediction_row="False",
        ),
        base_row(
            kernel_id="WEPK2648_3_tau_eff",
            arena="WEP_MICROSCOPE_TiPt",
            object="tau_WEP / tau_eff_X",
            formula="tau_eff_X=<K_CMSM^a(t,s) R_source_a^X(t,s)> over accepted sessions/masks/orbit weights",
            normalized_formula="readout/source/orbit functional converting source coupling to eta channel",
            current_status="SYMBOLIC_ONLY_NO_NUMERIC_OUTPUT",
            required_inputs="official CMSM arrays, Earth/source stress worldtube, orbit/session average, product convention",
            bound_anchor="tau_eff not filled; tau=1 shortcut forbidden",
            units="declared by readout/source normalization",
            score_ready="False",
            valid_prediction_row="False",
        ),
        base_row(
            kernel_id="WEPK2648_4_branch_and_shortcut_guards",
            arena="WEP_MICROSCOPE_TiPt",
            object="same branch/product/no-shortcut gate",
            formula="all factors share branch id, units/sign, and refuse tau=1, DD-as-MTS, surrogate arrays, bound inversion, or measured-G absorption",
            normalized_formula="schema guard rather than physics claim",
            current_status="GUARD_EXISTS_NONCLAIM",
            required_inputs="branch-locked files for all numeric rows and accepted product convention",
            bound_anchor="guard only",
            units="dimensionless eta after declared convention",
            score_ready="False",
            valid_prediction_row="False",
        ),
        base_row(
            kernel_id="WEPK2648_5_acceptance",
            arena="WEP_MICROSCOPE_TiPt",
            object="WEP kernel v0 acceptance verdict",
            formula="score only if parent coefficient, material tensor, tau_eff, product convention and branch lock are all sourced",
            normalized_formula="bound anchor is comparator only after eta_pred exists",
            current_status="WEP_KERNEL_V0_BLOCKED_NONCLAIM",
            required_inputs="WEPK2648_1 through WEPK2648_4 promoted from missing/nonclaim to sourced rows",
            bound_anchor="2.8e-15 not used as prediction",
            units="dimensionless eta",
            score_ready="False",
            valid_prediction_row="False",
        ),
    ]


def wep_requirement_rows() -> list[dict[str, Any]]:
    return [
        base_row(requirement_id="WR2648_0_parent_values", object="Delta_w_eff", current_status="MISSING_RESIDUAL_VALUES", needed_source="parent epsilon_A/C_parent vector or theorem-zero certificate", blocker="no source-label theorem and no parent coefficient vector"),
        base_row(requirement_id="WR2648_1_source_worldtube", object="K_source", current_status="MISSING_SOURCE_PROFILE_WEIGHTING", needed_source="Earth/source stress profile and composition/source convention", blocker="source worldtube not imported into branch"),
        base_row(requirement_id="WR2648_2_material_tensor", object="K_material", current_status="MISSING_FULL_MATERIAL_TENSOR", needed_source="full Ti/Pt material response tensor in Delta_w basis", blocker="proxy material contexts are not claim-grade tensor"),
        base_row(requirement_id="WR2648_3_readout_arrays", object="K_readout", current_status="OFFICIAL_ARRAYS_NOT_IMPORTED", needed_source="official MICROSCOPE CMSM/export arrays or exact validated equivalent", blocker="no official readout arrays in branch"),
        base_row(requirement_id="WR2648_4_force_map", object="eta convention", current_status="MISSING_FORCE_READOUT_MAP", needed_source="source residual to differential acceleration map in observed frame", blocker="force/readout map not signed"),
        base_row(requirement_id="WR2648_5_tau_wep", object="projection product", current_status="TAU_WEP_PROJECTION_NOT_DERIVED", needed_source="derived/sourced tau_WEP; tau_WEP=1 shortcut forbidden", blocker="tau/source/readout product convention missing"),
        base_row(requirement_id="WR2648_6_no_cancellation", object="comparison policy", current_status="NO_CANCELLATION_POLICY_ENFORCED_NONCLAIM", needed_source="absolute/no-cancellation envelope unless parent identity proves signed cancellation", blocker="policy active, not evidence"),
    ]


def validator_case_rows() -> list[dict[str, Any]]:
    return [
        base_row(case_id="CASE2648_0_label_unsigned", label_forgetting_signed="False", ward_only="False", no_prefactor_signed="False", parent_values="False", material_tensor="False", tau_eff="False", readout_arrays="False", bound_anchor_only="False", expected_status="REFUSED_SOURCE_LABEL_FORGETTING_UNSIGNED"),
        base_row(case_id="CASE2648_1_Ward_only", label_forgetting_signed="False", ward_only="True", no_prefactor_signed="False", parent_values="False", material_tensor="False", tau_eff="False", readout_arrays="False", bound_anchor_only="False", expected_status="REFUSED_WARD_ONLY_NOT_LABEL_FORGETTING"),
        base_row(case_id="CASE2648_2_no_prefactor_missing", label_forgetting_signed="True", ward_only="False", no_prefactor_signed="False", parent_values="False", material_tensor="False", tau_eff="False", readout_arrays="False", bound_anchor_only="False", expected_status="REFUSED_NO_SOURCE_PREFACTOR_UNSIGNED"),
        base_row(case_id="CASE2648_3_parent_values_missing", label_forgetting_signed="True", ward_only="False", no_prefactor_signed="True", parent_values="False", material_tensor="True", tau_eff="True", readout_arrays="True", bound_anchor_only="False", expected_status="REFUSED_PARENT_COEFFICIENTS_MISSING"),
        base_row(case_id="CASE2648_4_material_missing", label_forgetting_signed="True", ward_only="False", no_prefactor_signed="True", parent_values="True", material_tensor="False", tau_eff="True", readout_arrays="True", bound_anchor_only="False", expected_status="REFUSED_MATERIAL_TENSOR_MISSING"),
        base_row(case_id="CASE2648_5_tau_missing", label_forgetting_signed="True", ward_only="False", no_prefactor_signed="True", parent_values="True", material_tensor="True", tau_eff="False", readout_arrays="True", bound_anchor_only="False", expected_status="REFUSED_TAU_WEP_MISSING"),
        base_row(case_id="CASE2648_6_readout_missing", label_forgetting_signed="True", ward_only="False", no_prefactor_signed="True", parent_values="True", material_tensor="True", tau_eff="True", readout_arrays="False", bound_anchor_only="False", expected_status="REFUSED_READOUT_ARRAYS_MISSING"),
        base_row(case_id="CASE2648_7_bound_anchor", label_forgetting_signed="True", ward_only="False", no_prefactor_signed="True", parent_values="True", material_tensor="True", tau_eff="True", readout_arrays="True", bound_anchor_only="True", expected_status="REFUSED_BOUND_ANCHOR_NOT_PREDICTION"),
        base_row(case_id="CASE2648_8_schema_only", label_forgetting_signed="False", ward_only="False", no_prefactor_signed="False", parent_values="schema", material_tensor="schema", tau_eff="schema", readout_arrays="schema", bound_anchor_only="False", expected_status="SCHEMA_ONLY_NOT_EVIDENCE"),
    ]


def classify_case(row: dict[str, Any]) -> str:
    if row.get("ward_only") == "True":
        return "REFUSED_WARD_ONLY_NOT_LABEL_FORGETTING"
    if row.get("parent_values") == "schema":
        return "SCHEMA_ONLY_NOT_EVIDENCE"
    if row.get("label_forgetting_signed") != "True":
        return "REFUSED_SOURCE_LABEL_FORGETTING_UNSIGNED"
    if row.get("no_prefactor_signed") != "True":
        return "REFUSED_NO_SOURCE_PREFACTOR_UNSIGNED"
    if row.get("parent_values") != "True":
        return "REFUSED_PARENT_COEFFICIENTS_MISSING"
    if row.get("material_tensor") != "True":
        return "REFUSED_MATERIAL_TENSOR_MISSING"
    if row.get("tau_eff") != "True":
        return "REFUSED_TAU_WEP_MISSING"
    if row.get("readout_arrays") != "True":
        return "REFUSED_READOUT_ARRAYS_MISSING"
    if row.get("bound_anchor_only") == "True":
        return "REFUSED_BOUND_ANCHOR_NOT_PREDICTION"
    return "WEP_KERNEL_READY_NONCLAIM"


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
        base_row(gate_id="CG2648_0_label_forgetting", claim="source functor forgets species labels before coupling selection", allowed="False", blocker="source-domain quotient/no-spurion/no-prefactor package unsigned"),
        base_row(gate_id="CG2648_1_delta_w_zero", claim="Delta_w_species theorem-zero", allowed="False", blocker="label forgetting and no-source-prefactor theorem not parent-derived together"),
        base_row(gate_id="CG2648_2_wep_kernel", claim="WEP kernel has parent coefficient, material tensor, tau/readout/source map and branch guards", allowed="False", blocker="all claim-critical WEP inputs remain missing or symbolic"),
        base_row(gate_id="CG2648_3_bound_use", claim="MICROSCOPE bound can be used as prediction", allowed="False", blocker="bound is comparator only after eta_pred exists"),
        base_row(gate_id="CG2648_4_local_GR_WEP", claim="source-coupling local GR/WEP branch can claim pass", allowed="False", blocker="source-label theorem and executable WEP row remain blocked"),
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        base_row(decision_id="DEC2648_0_label_result", decision="SOURCE_FUNCTOR_LABEL_FORGETTING_NOT_DERIVED", rationale="the conditional theorem is clean, but q_src/domain quotient, no-prefactor, no-spurion return and projected-mass calibration are not parent-signed together", consequence="do not claim Delta_w_species=0"),
        base_row(decision_id="DEC2648_1_wep_kernel", decision="WEP_KERNEL_V0_STAGED_NONCLAIM", rationale="WEP formula now has explicit parent coefficient/material/tau/readout blockers and refuses bound-as-prediction", consequence="empirical branch is shaped but not executable"),
        base_row(decision_id="DEC2648_2_next", decision="SELECT_2649_SOURCE_DOMAIN_QUOTIENT_OR_WEP_MATERIAL_TENSOR_INTAKE", rationale="the missing theory object is q_src; the most concrete empirical fallback is the material tensor/tau/readout intake", consequence="attack q_src first, keep WEP input pack as fallback"),
    ]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        base_row(
            next_id="NEXT2648_0_selected",
            next_doc="2649-Y5-R2FR-source-domain-quotient-constructor-or-WEP-material-tensor-intake.md",
            next_script="scripts/Y5_R2FR_source_domain_quotient_constructor_or_WEP_material_tensor_intake_2649.py",
            objective="Try to construct the parent source-domain quotient q_src that maps labelled species currents to total Hilbert stress before coupling; if it fails, stage WEP material tensor/tau/readout intake rows without scoring.",
            include="q_src domain/codomain; total Hilbert source; no species/source label codomain; no pre-action prefactor; WEP material tensor; tau/readout/source acquisition requirements",
            exclude="Ward-only proof; MICROSCOPE bound as prediction; tau=1 shortcut; proxy material vectors as claim tensors; WEP/local-GR claim; GitHub action; formalization-workbench edits",
        )
    ]


def branch_copy_rows(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    copy_rows: list[dict[str, Any]] = []
    for copy_id, path in BRANCH_COPIES.items():
        write_csv(path, rows)
        copy_rows.append(base_row(copy_id=copy_id, copy_path=str(path), path_exists=str(path.exists()), csv_parses=str(csv_parses(path)), contents="2648 source-label/WEP kernel v0 nonclaim rows"))
    return copy_rows


def validation_rows(generated_paths: list[Path], rows_by_name: dict[str, list[dict[str, Any]]]) -> list[dict[str, Any]]:
    source_rows = rows_by_name["source_register"]
    label_rows = rows_by_name["label_forgetting_attempt"]
    clause_rows = rows_by_name["clause_audit"]
    kernel_rows = rows_by_name["wep_kernel"]
    req_rows = rows_by_name["wep_requirements"]
    result_rows = rows_by_name["validator_results"]
    gate_rows = rows_by_name["claim_gates"]
    decision_rows_ = rows_by_name["decision"]
    next_rows = rows_by_name["next_target"]
    branch_rows = rows_by_name["branch_copies"]
    checks = [
        ("VAL2648_00_sources", all(row["path_exists"] == "True" and row["needles_present"] == "True" for row in source_rows), "all cited source paths exist and required needles are present"),
        ("VAL2648_01_label_not_promoted", any(row["attempt_id"] == "SFL2648_5_verdict" and row["status"] == "SOURCE_FUNCTOR_LABEL_FORGETTING_NOT_PARENT_DERIVED" for row in label_rows), "source-label forgetting remains unsigned"),
        ("VAL2648_02_clause_audit", any(row["clause_id"] == "LFA2648_5_verdict" and row["current_status"] == "SOURCE_LABEL_FORGETTING_NOT_DERIVED" for row in clause_rows), "clause audit records nonclaim verdict"),
        ("VAL2648_03_wep_kernel_v0", any(row["kernel_id"] == "WEPK2648_5_acceptance" and row["current_status"] == "WEP_KERNEL_V0_BLOCKED_NONCLAIM" for row in kernel_rows) and all(row["score_ready"] == "False" for row in kernel_rows), "WEP kernel v0 exists but is nonclaim/not score-ready"),
        ("VAL2648_04_wep_requirements", {"WR2648_0_parent_values", "WR2648_2_material_tensor", "WR2648_3_readout_arrays", "WR2648_5_tau_wep"}.issubset({row["requirement_id"] for row in req_rows}), "claim-critical WEP requirements are explicit"),
        ("VAL2648_05_validator_refusals", all(row["status_matches_expected"] == "True" and row["valid_for_claim"] == "False" for row in result_rows), "validator refuses Ward-only, unsigned label forgetting, missing prefactor theorem, missing WEP inputs, bound shortcuts and schema-only rows"),
        ("VAL2648_06_claim_gates_false", all(row["allowed"] == "False" and row["valid_for_claim"] == "False" for row in gate_rows), "all claim gates remain blocked"),
        ("VAL2648_07_decision_next", any(row["decision"] == "SELECT_2649_SOURCE_DOMAIN_QUOTIENT_OR_WEP_MATERIAL_TENSOR_INTAKE" for row in decision_rows_), "decision selects q_src/WEP material intake next"),
        ("VAL2648_08_next_target", any(row["next_doc"].startswith("2649-Y5-R2FR-source-domain-quotient") for row in next_rows), "2649 next target is recorded"),
        ("VAL2648_09_branch_copies", all(row["path_exists"] == "True" and row["csv_parses"] == "True" for row in branch_rows), "branch copies exist and parse"),
        ("VAL2648_10_csv_parse", all(csv_parses(path) for path in generated_paths if path.suffix.lower() == ".csv"), "all generated CSVs parse cleanly"),
        ("VAL2648_11_formalization_untouched", not formalization_has_2648_artifacts(), "no 2648 outputs are written under formalization-workbench"),
        ("VAL2648_12_pycache_absent", not (ROOT / "scripts" / "__pycache__").exists(), "scripts __pycache__ absent"),
    ]
    rows = [base_row(validation_id=check_id, status="PASS" if passed else "FAIL", detail=detail) for check_id, passed, detail in checks]
    rows.append(base_row(validation_id="VAL2648_OVERALL", status="PASS" if all(row["status"] == "PASS" for row in rows) else "FAIL", detail="2648 keeps source-label forgetting unsigned, stages WEP kernel v0 nonclaim, and selects source-domain quotient/WEP material intake next"))
    return rows


def write_doc(rows_by_name: dict[str, list[dict[str, Any]]]) -> None:
    DOC_PATH.write_text(
        "\n\n".join(
            [
                "# 2648 - Y5/R2FR Source-Functor Label Forgetting Or Delta-w WEP Kernel v0",
                "**Status:** source-label forgetting remains a clean conditional theorem, not a parent-signed result.",
                "**Main result:** `Delta_w_species` cannot be erased yet. WEP kernel v0 is staged as a nonclaim formula/input ledger; the MICROSCOPE bound is a comparator only after `eta_pred` exists.",
                "## Source register",
                md_table(rows_by_name["source_register"], ["source_id", "role", "source_path", "path_exists", "needles_present", "valid_for_claim"]),
                "## Source-functor label-forgetting attempt",
                md_table(rows_by_name["label_forgetting_attempt"], ["attempt_id", "claim_piece", "status", "formal_statement", "derivation_or_obstruction", "source_anchor", "valid_for_claim"]),
                "## Label-forgetting clause audit",
                md_table(rows_by_name["clause_audit"], ["clause_id", "clause", "required_identity", "current_status", "if_signed", "if_unsigned", "source_anchor", "valid_for_claim"]),
                "## Delta_w WEP kernel v0",
                md_table(rows_by_name["wep_kernel"], ["kernel_id", "arena", "object", "formula", "current_status", "required_inputs", "bound_anchor", "units", "score_ready", "valid_prediction_row", "valid_for_claim"]),
                "## WEP requirements",
                md_table(rows_by_name["wep_requirements"], ["requirement_id", "object", "current_status", "needed_source", "blocker", "valid_for_claim"]),
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
        "label_forgetting_attempt": label_forgetting_rows(),
        "clause_audit": clause_audit_rows(),
        "wep_kernel": wep_kernel_rows(),
        "wep_requirements": wep_requirement_rows(),
        "validator_cases": cases,
        "validator_results": validator_result_rows(cases),
        "claim_gates": claim_gate_rows(),
        "decision": decision_rows(),
        "next_target": next_target_rows(),
    }
    rows_by_name["branch_copies"] = branch_copy_rows(rows_by_name["wep_kernel"])

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

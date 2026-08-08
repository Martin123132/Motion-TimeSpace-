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
DOC_PATH = ROOT / "2649-Y5-R2FR-source-domain-quotient-constructor-or-WEP-material-tensor-intake.md"

CHECKPOINT = "2649"
BRANCH_ID = "Y5_R2FR_SOURCE_DOMAIN_QUOTIENT_OR_WEP_MATERIAL_INTAKE_2649"
PREFIX = "P8_Y5_SOURCE_DOMAIN_QUOTIENT_2649"

OUTPUTS = {
    "source_register": RESIDUALS / f"{PREFIX}_SOURCE_REGISTER.csv",
    "qsrc_constructor": RESIDUALS / f"{PREFIX}_QSRC_CONSTRUCTOR_ATTEMPT.csv",
    "qsrc_gate": RESIDUALS / f"{PREFIX}_QSRC_CLAUSE_GATE.csv",
    "wep_intake": RESIDUALS / f"{PREFIX}_WEP_MATERIAL_TENSOR_INTAKE_NONCLAIM.csv",
    "validator_cases": RESIDUALS / f"{PREFIX}_VALIDATOR_CASES.csv",
    "validator_results": RESIDUALS / f"{PREFIX}_VALIDATOR_RESULTS.csv",
    "claim_gates": RESIDUALS / f"{PREFIX}_CLAIM_GATES.csv",
    "decision": RESIDUALS / f"{PREFIX}_DECISION_LEDGER.csv",
    "next_target": RESIDUALS / f"{PREFIX}_NEXT_TARGET.csv",
    "branch_copies": RESIDUALS / f"{PREFIX}_BRANCH_COPIES.csv",
    "validation": RESIDUALS / f"P8_Y5_BRR545_{CHECKPOINT}_VALIDATION.csv",
}

BRANCH_COPIES = {
    "queue": QUEUE / "JR2649_QSRC_WEP_MATERIAL_INTAKE_NONCLAIM.csv",
    "local_bounds": LOCAL_BOUNDS / "qsrc_WEP_material_tensor_2649_NONCLAIM.csv",
    "source_weight": SOURCE_WEIGHT / "QSRC_WEP_MATERIAL_TENSOR_2649_NONCLAIM.csv",
    "microscope": MICROSCOPE / "P8_Y5_2649_QSRC_WEP_MATERIAL_NONCLAIM.csv",
}

SOURCES = [
    {
        "source_id": "SRC2649_00_2648",
        "role": "immediate source-label/WEP kernel handoff",
        "path": ROOT / "2648-Y5-R2FR-source-functor-label-forgetting-or-Delta-w-WEP-kernel-v0.md",
        "needles": ["SFL2648_5_verdict", "WEPK2648_5_acceptance", "VAL2648_OVERALL"],
    },
    {
        "source_id": "SRC2649_01_1894",
        "role": "older q_src constructor and material intake",
        "path": ROOT / "1894-Y5-R2FR-source-domain-quotient-constructor-or-wep-material-tensor-intake.md",
        "needles": ["QSRC1894_5_verdict", "WMI1894_3_full_parent_tensor", "VAL1894_OVERALL"],
    },
    {
        "source_id": "SRC2649_02_2645",
        "role": "pre-action weight countermodel",
        "path": ROOT / "2645-Y5-R2FR-no-source-prefactor-parent-action-clause-or-first-JH-DqZ-component-row.md",
        "needles": ["NSP2645_5_pre_action_countermodel", "NSP2645_7_verdict"],
    },
    {
        "source_id": "SRC2649_03_2646",
        "role": "matter-normalization owner and Delta_w coefficient",
        "path": ROOT / "2646-Y5-R2FR-matter-normalization-owner-or-Delta-w-species-coefficient-source-row.md",
        "needles": ["MNO2646_6_verdict", "DWS2646_0_delta_w_species"],
    },
    {
        "source_id": "SRC2649_04_953",
        "role": "source functor quotient theorem lineage",
        "path": ROOT / "953-Y5-R10-no-species-label-source-functor-theorem-or-filled-coefficient-intake-review.md",
        "needles": ["PMC953_1_label_forgetting_quotient", "Status:"],
    },
    {
        "source_id": "SRC2649_05_954",
        "role": "parent label-forgetting clause gate",
        "path": ROOT / "954-Y5-R10-parent-matter-category-no-species-label-clause-or-source-functor-countermodel-bound.md",
        "needles": ["CGATE954_0_parent_label_forgetting", "exact contract written but unsigned"],
    },
    {
        "source_id": "SRC2649_06_1066",
        "role": "tau_WEP and material/force/readout projection contract",
        "path": ROOT / "1066-Y5-R10-parent-action-syntax-source-scalar-exclusion-or-WEP-Delta-w-prior-width.md",
        "needles": ["TWP1066_7_verdict", "TWP1066_5_no_unity_shortcut", "TWP1066_3_material_response"],
    },
    {
        "source_id": "SRC2649_07_1080",
        "role": "finite WEP source vector and material candidates",
        "path": ROOT / "1080-Y5-R10-finite-WEP-source-vector-and-material-tensor-acquisition-pack.md",
        "needles": ["BOUND1080_0_MICROSCOPE_WEP_source_charge", "2.8e-15"],
    },
    {
        "source_id": "SRC2649_08_1225",
        "role": "official readout/source acquisition table",
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


def formalization_has_2649_artifacts() -> bool:
    if not FORMALIZATION.exists():
        return False
    patterns = (
        "*2649-Y5-R2FR*",
        "*P8_Y5_SOURCE_DOMAIN_QUOTIENT_2649*",
        "*P8_Y5_BRR545_2649*",
        "*Y5_R2FR_source_domain_quotient_constructor_or_WEP_material_tensor_intake_2649*",
        "*JR2649*",
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


def qsrc_constructor_rows() -> list[dict[str, Any]]:
    return [
        base_row(
            constructor_id="QSRC2649_0_definition",
            claim_piece="source-domain quotient object",
            formal_statement="For a labelled finite family J_lab={(T_A,A)}, define J_lab ~ J'_lab iff sum_A T_A=sum_B T'_B as the total Hilbert/coframe current on the observed frame; q_src(J_lab)=T_total.",
            status="MATHEMATICAL_CONSTRUCTOR_WRITTEN",
            proof_or_obstruction="the quotient is a clean mathematical map, but parent physics must require all source couplings to factor through it.",
            source_anchor="1894:QSRC1894_0_definition;953:PMC953_1_label_forgetting_quotient",
            parent_signed="False",
        ),
        base_row(
            constructor_id="QSRC2649_1_factorization_theorem",
            claim_piece="unique source map after quotient",
            formal_statement="If F_src is local, covariant, additive/natural and has domain Im(q_src), then F_src(T_total)=kappa_univ T_total up to one calibrated common source scale.",
            status="EXACT_CONDITIONAL_THEOREM",
            proof_or_obstruction="relative kappa_A cannot be formed once A labels are removed from the domain.",
            source_anchor="1894:QSRC1894_1_factorization_theorem;2648:SFL2648_3_conditional_uniqueness",
            parent_signed="False",
        ),
        base_row(
            constructor_id="QSRC2649_2_parent_adoption_gap",
            claim_piece="parent adoption of q_src",
            formal_statement="The parent action/category declares C_parent -> C_source to be q_src before coupling selection and provides no morphism from labels, hidden markers or readout masks into source coefficients.",
            status="SOURCE_DOMAIN_QUOTIENT_NOT_PARENT_SIGNED",
            proof_or_obstruction="current files state the missing clause, but do not derive it from MTS primitives or a single parent action grammar.",
            source_anchor="1894:QSRC1894_2_parent_gap;2648:LFA2648_0_domain_quotient",
            parent_signed="False",
        ),
        base_row(
            constructor_id="QSRC2649_3_no_prefactor_bypass",
            claim_piece="quotient bypass by legal pre-action weights",
            formal_statement="If S_matter=sum_A w_A S_A is legal before variation, q_src receives the already-weighted Hilbert source sum_A w_A T_A rather than the unweighted T_total.",
            status="PREACTION_WEIGHT_BYPASS_SURVIVES",
            proof_or_obstruction="q_src alone cannot kill Delta_w_species; it needs the no-source-prefactor/object-language theorem.",
            source_anchor="2645:NSP2645_5_pre_action_countermodel;2646:MNO2646_6_verdict",
            parent_signed="False",
        ),
        base_row(
            constructor_id="QSRC2649_4_spurion_and_projector_gap",
            claim_piece="label return after quotient",
            formal_statement="Hidden marker, boundary, domain, readout and source-worldtube projectors must not reintroduce label-dependent source coefficients after q_src.",
            status="NO_SPURION_AND_PROJECTOR_GATES_OPEN",
            proof_or_obstruction="readout/source-worldtube/projector commutators remain finite routes in the WEP branch.",
            source_anchor="2648:LFA2648_3_no_spurion_return;1898:RVC1898_5_verdict",
            parent_signed="False",
        ),
        base_row(
            constructor_id="QSRC2649_5_projected_mass_gap",
            claim_piece="Newton/GM projection after q_src",
            formal_statement="Even if q_src is adopted, Newton/GM source normalization needs a closed calibrated mass projector with no exchange, boundary, anomaly, range or time-drift leakage.",
            status="PROJECTED_MASS_CALIBRATION_OPEN",
            proof_or_obstruction="source-domain quotient attacks species weights but not the entire Newtonian source calibration problem.",
            source_anchor="1894:QSRC1894_4_projected_mass_gap",
            parent_signed="False",
        ),
        base_row(
            constructor_id="QSRC2649_6_verdict",
            claim_piece="promote q_src constructor as current MTS theorem",
            formal_statement="The current MTS parent theory forces all ordinary source coupling maps to factor through q_src(J_lab)=sum_A T_A.",
            status="SOURCE_DOMAIN_QUOTIENT_CONSTRUCTOR_NOT_PARENT_DERIVED",
            proof_or_obstruction="constructor is exact as a contract, but parent adoption, no-prefactor exclusion, no-spurion/projector silence and projected mass calibration remain unsigned.",
            source_anchor="QSRC2649_0 through QSRC2649_5",
            parent_signed="False",
        ),
    ]


def qsrc_gate_rows() -> list[dict[str, Any]]:
    return [
        base_row(gate_id="QG2649_0_parent_category", required_clause="parent source category declares q_src before F_src is formed", formal_condition="C_parent -> C_source quotients labelled current families by total Hilbert current", current_status="EXACT_MISSING_CLAUSE_NOT_PARENT_SIGNED", if_pass="source labels absent from coupling arguments", if_fail="kappa_A and Delta_w_species stay legal", gate_pass="False"),
        base_row(gate_id="QG2649_1_total_hilbert_source", required_clause="active source is total Hilbert/coframe derivative of one matter action", formal_condition="T_total=delta S_matter/delta e_obs=sum_A delta S_A/delta e_obs", current_status="CONDITIONAL_MATH_CLEAN_NOT_PARENT_COMPLETE", if_pass="labelled decomposition becomes bookkeeping after variation", if_fail="source current can be fitted/readout-defined", gate_pass="False"),
        base_row(gate_id="QG2649_2_no_source_prefactors", required_clause="no source-only species prefactor is an argument of S_matter", formal_condition="partial S_matter/partial w_A undefined or forbidden for source-only w_A", current_status="EXACT_HIGH_PRESSURE_MISSING_CLAUSE", if_pass="weighted-source countermodel killed", if_fail="q_src can receive already-weighted source terms", gate_pass="False"),
        base_row(gate_id="QG2649_3_no_spurion_projector", required_clause="no hidden marker/readout/source-worldtube projector reintroduces labels", formal_condition="partial_A kappa=partial_marker kappa=partial_readout kappa=0 and projector commutators vanish or are bounded", current_status="NO_SPURION_AND_PROJECTOR_GATES_OPEN", if_pass="label forgetting survives local readout", if_fail="Delta_w_marker_hidden/projector transfer remains live", gate_pass="False"),
        base_row(gate_id="QG2649_4_projected_mass", required_clause="measured-GM mass projector is closed and calibrated", formal_condition="d(Pi_M J_Hilbert)=0 with no exchange/boundary/anomaly flux and one common G_ref calibration", current_status="PROJECTED_FLUX_OPEN", if_pass="Newtonian source normalization can follow", if_fail="orbital/Newton residual remains separate", gate_pass="False"),
        base_row(gate_id="QG2649_5_verdict", required_clause="q_src can be used as theorem-zero source coupling gate", formal_condition="QG2649_0 through QG2649_4 all pass", current_status="QSRC_CLAIM_BLOCKED", if_pass="Delta_w_species source side theorem-zero subject to left-hand gates", if_fail="finite Delta_w/WEP material tensor intake remains honest route", gate_pass="False"),
    ]


def wep_intake_rows() -> list[dict[str, Any]]:
    return [
        base_row(intake_id="WMI2649_0_pair_context", arena="WEP_MICROSCOPE_TiPt", object="TA6V_minus_PtRh10 material pair", value_or_status="TA6V=Ti0.90 Al0.06 V0.04; PtRh10=Pt0.90 Rh0.10", filled_level="SOURCE_BACKED_COMPOSITION_CONTEXT", missing_for_claim="parent response basis and full material tensor", units="mass fractions", score_ready="False", valid_prediction_row="False"),
        base_row(intake_id="WMI2649_1_bound_anchor", arena="WEP_MICROSCOPE_TiPt", object="MICROSCOPE eta bound comparator", value_or_status="2.8e-15", filled_level="BOUND_ANCHOR_ONLY", missing_for_claim="eta_pred from parent coefficient x material tensor x tau/readout product", units="dimensionless eta", score_ready="False", valid_prediction_row="False"),
        base_row(intake_id="WMI2649_2_proxy_vectors", arena="WEP_MICROSCOPE_TiPt", object="proxy charge vectors", value_or_status="Z/A, neutron-excess, electron-mass and alpha/Coulomb smoke contexts exist", filled_level="PROXY_CONTEXT_ONLY", missing_for_claim="MTS parent response basis, no-double-counting rule, tau_eff and source coefficient owner", units="dimensionless proxies", score_ready="False", valid_prediction_row="False"),
        base_row(intake_id="WMI2649_3_full_parent_tensor", arena="WEP_MICROSCOPE_TiPt", object="full parent-basis TA6V-minus-PtRh10 material tensor", value_or_status="MISSING_FULL_PARENT_MATERIAL_TENSOR", filled_level="BLOCKED", missing_for_claim="parent basis, full response map, isotope/alloy averaging, source/readout environment stack", units="parent-basis response units", score_ready="False", valid_prediction_row="False"),
        base_row(intake_id="WMI2649_4_parent_coefficient_dependency", arena="WEP_MICROSCOPE_TiPt", object="parent epsilon/C_parent vector dependency", value_or_status="MISSING_PARENT_EPSILON_OR_C_PARENT_VECTOR", filled_level="BLOCKED", missing_for_claim="parent numeric/theorem-zero coefficient vector with units/sign/source path", units="dimensionless or declared parent-basis units", score_ready="False", valid_prediction_row="False"),
        base_row(intake_id="WMI2649_5_tau_readout_dependency", arena="WEP_MICROSCOPE_TiPt", object="tau_eff/source/readout dependency", value_or_status="TAU_EFF_NOT_FILLED; OFFICIAL_ARRAYS_NOT_IMPORTED; PRODUCT_CONVENTION_NOT_FILLED", filled_level="BLOCKED", missing_for_claim="official CMSM arrays, Earth/source worldtube, orbit/session average, product convention and force map", units="declared by readout/source normalization", score_ready="False", valid_prediction_row="False"),
        base_row(intake_id="WMI2649_6_acceptance", arena="WEP_MICROSCOPE_TiPt", object="material tensor intake acceptance", value_or_status="WEP_MATERIAL_TENSOR_INTAKE_BLOCKED_NONCLAIM", filled_level="NONCLAIM_CONTEXT_ONLY", missing_for_claim="full parent tensor plus parent coefficient vector plus tau_eff/readout; MICROSCOPE bound remains comparator only", units="dimensionless eta only after product convention", score_ready="False", valid_prediction_row="False"),
    ]


def validator_case_rows() -> list[dict[str, Any]]:
    return [
        base_row(case_id="CASE2649_0_qsrc_math_only", qsrc_parent_signed="False", no_prefactor_signed="False", ward_only="False", material_level="context_only", proxy_as_tensor="False", bound_as_prediction="False", expected_status="REFUSED_QSRC_CONSTRUCTOR_NOT_PARENT_DERIVED"),
        base_row(case_id="CASE2649_1_ward_shortcut", qsrc_parent_signed="False", no_prefactor_signed="False", ward_only="True", material_level="context_only", proxy_as_tensor="False", bound_as_prediction="False", expected_status="REFUSED_WARD_ONLY_NOT_LABEL_FORGETTING"),
        base_row(case_id="CASE2649_2_no_prefactor_missing", qsrc_parent_signed="True", no_prefactor_signed="False", ward_only="False", material_level="context_only", proxy_as_tensor="False", bound_as_prediction="False", expected_status="REFUSED_PREACTION_WEIGHT_BYPASS_SURVIVES"),
        base_row(case_id="CASE2649_3_proxy_tensor", qsrc_parent_signed="True", no_prefactor_signed="True", ward_only="False", material_level="proxy_only", proxy_as_tensor="True", bound_as_prediction="False", expected_status="REFUSED_PROXY_MATERIAL_VECTOR_NOT_PARENT_TENSOR"),
        base_row(case_id="CASE2649_4_full_tensor_missing", qsrc_parent_signed="True", no_prefactor_signed="True", ward_only="False", material_level="missing_full_tensor", proxy_as_tensor="False", bound_as_prediction="False", expected_status="REFUSED_FULL_PARENT_MATERIAL_TENSOR_MISSING"),
        base_row(case_id="CASE2649_5_bound_shortcut", qsrc_parent_signed="True", no_prefactor_signed="True", ward_only="False", material_level="full_tensor", proxy_as_tensor="False", bound_as_prediction="True", expected_status="REFUSED_BOUND_ANCHOR_NOT_PREDICTION"),
        base_row(case_id="CASE2649_6_tau_readout_missing", qsrc_parent_signed="True", no_prefactor_signed="True", ward_only="False", material_level="full_tensor", proxy_as_tensor="False", bound_as_prediction="False", tau_readout_ready="False", expected_status="REFUSED_TAU_READOUT_SOURCE_MISSING"),
    ]


def classify_case(row: dict[str, Any]) -> str:
    if row.get("ward_only") == "True":
        return "REFUSED_WARD_ONLY_NOT_LABEL_FORGETTING"
    if row.get("qsrc_parent_signed") != "True":
        return "REFUSED_QSRC_CONSTRUCTOR_NOT_PARENT_DERIVED"
    if row.get("no_prefactor_signed") != "True":
        return "REFUSED_PREACTION_WEIGHT_BYPASS_SURVIVES"
    if row.get("proxy_as_tensor") == "True":
        return "REFUSED_PROXY_MATERIAL_VECTOR_NOT_PARENT_TENSOR"
    if row.get("material_level") == "missing_full_tensor":
        return "REFUSED_FULL_PARENT_MATERIAL_TENSOR_MISSING"
    if row.get("bound_as_prediction") == "True":
        return "REFUSED_BOUND_ANCHOR_NOT_PREDICTION"
    if row.get("tau_readout_ready") == "False":
        return "REFUSED_TAU_READOUT_SOURCE_MISSING"
    return "QSRC_WEP_READY_NONCLAIM"


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
        base_row(gate_id="CG2649_0_qsrc", claim="parent action/category forces all ordinary source maps through q_src", allowed="False", blocker="q_src is mathematical contract, not parent theorem"),
        base_row(gate_id="CG2649_1_no_prefactor", claim="no source-only pre-action species prefactor can enter before q_src", allowed="False", blocker="pre-action w_A bypass survives"),
        base_row(gate_id="CG2649_2_material_tensor", claim="WEP material tensor is full parent-basis tensor", allowed="False", blocker="only composition/proxy context exists"),
        base_row(gate_id="CG2649_3_tau_readout", claim="WEP tau/readout/source product is executable", allowed="False", blocker="official arrays/source worldtube/product convention missing"),
        base_row(gate_id="CG2649_4_local_source_WEP", claim="local source/WEP branch can claim derived or scored pass", allowed="False", blocker="q_src and WEP inputs blocked"),
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        base_row(decision_id="DEC2649_0_qsrc", decision="QSRC_CONSTRUCTOR_WRITTEN_NOT_PARENT_THEOREM", rationale="q_src is mathematically clean but parent factorization/no-prefactor/no-spurion/projected-mass clauses are unsigned", consequence="do not use q_src to erase Delta_w_species yet"),
        base_row(decision_id="DEC2649_1_wep_material", decision="WEP_MATERIAL_CONTEXT_STAGED_NONCLAIM", rationale="composition/proxy context exists, but the full parent-basis material tensor and tau/readout product are missing", consequence="no WEP score from proxies or MICROSCOPE bound anchor"),
        base_row(decision_id="DEC2649_2_next", decision="SELECT_2650_NO_SOURCE_PREF_OBJECT_LANGUAGE_OR_PARENT_MATERIAL_TENSOR_BASIS", rationale="q_src fails mainly because a legal pre-action w_A can encode labels before quotient; empirical fallback needs a parent material response basis", consequence="attack object-language exclusion or build tensor-basis intake"),
    ]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        base_row(
            next_id="NEXT2649_0_selected",
            next_doc="2650-Y5-R2FR-no-source-prefactor-object-language-proof-or-parent-material-tensor-basis.md",
            next_script="scripts/Y5_R2FR_no_source_prefactor_object_language_proof_or_parent_material_tensor_basis_2650.py",
            objective="Try to prove source-only w_A is not a well-typed parent object before variation; if it fails, build the parent material tensor basis needed for WEP without promoting proxy vectors.",
            include="object-language exclusion; action-density line; source-label quotient; pre-action weight bypass; parent material response basis; WEP tensor/tau/readout dependencies",
            exclude="Ward-only label forgetting; q_src as theorem by definition; proxy WEP tensor scoring; MICROSCOPE bound as prediction; tau=1 shortcut; WEP/local-GR claim; GitHub action; formalization-workbench edits",
        )
    ]


def branch_copy_rows(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    copy_rows: list[dict[str, Any]] = []
    for copy_id, path in BRANCH_COPIES.items():
        write_csv(path, rows)
        copy_rows.append(base_row(copy_id=copy_id, copy_path=str(path), path_exists=str(path.exists()), csv_parses=str(csv_parses(path)), contents="2649 q_src and WEP material intake nonclaim rows"))
    return copy_rows


def validation_rows(generated_paths: list[Path], rows_by_name: dict[str, list[dict[str, Any]]]) -> list[dict[str, Any]]:
    source_rows = rows_by_name["source_register"]
    qsrc_rows = rows_by_name["qsrc_constructor"]
    gate_rows_ = rows_by_name["qsrc_gate"]
    intake_rows = rows_by_name["wep_intake"]
    result_rows = rows_by_name["validator_results"]
    claim_rows = rows_by_name["claim_gates"]
    decision_rows_ = rows_by_name["decision"]
    next_rows = rows_by_name["next_target"]
    branch_rows = rows_by_name["branch_copies"]
    checks = [
        ("VAL2649_00_sources", all(row["path_exists"] == "True" and row["needles_present"] == "True" for row in source_rows), "all cited source paths exist and required needles are present"),
        ("VAL2649_01_qsrc_verdict", any(row["constructor_id"] == "QSRC2649_6_verdict" and row["status"] == "SOURCE_DOMAIN_QUOTIENT_CONSTRUCTOR_NOT_PARENT_DERIVED" for row in qsrc_rows), "q_src constructor is contract-only, not parent theorem"),
        ("VAL2649_02_qsrc_gate", any(row["gate_id"] == "QG2649_5_verdict" and row["current_status"] == "QSRC_CLAIM_BLOCKED" for row in gate_rows_), "q_src claim gate remains blocked"),
        ("VAL2649_03_wep_material_intake", any(row["intake_id"] == "WMI2649_3_full_parent_tensor" and row["value_or_status"] == "MISSING_FULL_PARENT_MATERIAL_TENSOR" for row in intake_rows) and any(row["intake_id"] == "WMI2649_6_acceptance" and row["score_ready"] == "False" for row in intake_rows), "WEP material context staged but full parent tensor remains missing/nonclaim"),
        ("VAL2649_04_validator_refusals", all(row["status_matches_expected"] == "True" and row["valid_for_claim"] == "False" for row in result_rows), "validator refuses q_src math-only, Ward shortcut, preaction bypass, proxy tensor, missing tensor, tau/readout missing and bound shortcut"),
        ("VAL2649_05_claim_gates_false", all(row["allowed"] == "False" and row["valid_for_claim"] == "False" for row in claim_rows), "all claim gates remain blocked"),
        ("VAL2649_06_decision_next", any(row["decision"] == "SELECT_2650_NO_SOURCE_PREF_OBJECT_LANGUAGE_OR_PARENT_MATERIAL_TENSOR_BASIS" for row in decision_rows_), "decision selects 2650 object-language/material-basis route"),
        ("VAL2649_07_next_target", any(row["next_doc"].startswith("2650-Y5-R2FR-no-source-prefactor") for row in next_rows), "2650 next target is recorded"),
        ("VAL2649_08_branch_copies", all(row["path_exists"] == "True" and row["csv_parses"] == "True" for row in branch_rows), "branch copies exist and parse"),
        ("VAL2649_09_csv_parse", all(csv_parses(path) for path in generated_paths if path.suffix.lower() == ".csv"), "all generated CSVs parse cleanly"),
        ("VAL2649_10_formalization_untouched", not formalization_has_2649_artifacts(), "no 2649 outputs are written under formalization-workbench"),
        ("VAL2649_11_pycache_absent", not (ROOT / "scripts" / "__pycache__").exists(), "scripts __pycache__ absent"),
    ]
    rows = [base_row(validation_id=check_id, status="PASS" if passed else "FAIL", detail=detail) for check_id, passed, detail in checks]
    rows.append(base_row(validation_id="VAL2649_OVERALL", status="PASS" if all(row["status"] == "PASS" for row in rows) else "FAIL", detail="2649 constructs q_src as a contract, blocks parent promotion, stages WEP material intake nonclaim, and selects no-source-prefactor/material-basis next"))
    return rows


def write_doc(rows_by_name: dict[str, list[dict[str, Any]]]) -> None:
    DOC_PATH.write_text(
        "\n\n".join(
            [
                "# 2649 - Y5/R2FR Source-Domain Quotient Constructor Or WEP Material Tensor Intake",
                "**Status:** `q_src` is cleanly constructible as a mathematical quotient, but not parent-signed as the required source-domain route.",
                "**Main result:** `q_src` cannot yet erase `Delta_w_species` because pre-action `w_A` can encode labels before the quotient. WEP material/tau/readout intake remains nonclaim.",
                "## Source register",
                md_table(rows_by_name["source_register"], ["source_id", "role", "source_path", "path_exists", "needles_present", "valid_for_claim"]),
                "## q_src constructor attempt",
                md_table(rows_by_name["qsrc_constructor"], ["constructor_id", "claim_piece", "status", "formal_statement", "proof_or_obstruction", "source_anchor", "parent_signed", "valid_for_claim"]),
                "## q_src clause gate",
                md_table(rows_by_name["qsrc_gate"], ["gate_id", "required_clause", "formal_condition", "current_status", "if_pass", "if_fail", "gate_pass", "valid_for_claim"]),
                "## WEP material tensor intake",
                md_table(rows_by_name["wep_intake"], ["intake_id", "arena", "object", "value_or_status", "filled_level", "missing_for_claim", "units", "score_ready", "valid_prediction_row", "valid_for_claim"]),
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
        "qsrc_constructor": qsrc_constructor_rows(),
        "qsrc_gate": qsrc_gate_rows(),
        "wep_intake": wep_intake_rows(),
        "validator_cases": cases,
        "validator_results": validator_result_rows(cases),
        "claim_gates": claim_gate_rows(),
        "decision": decision_rows(),
        "next_target": next_target_rows(),
    }
    rows_by_name["branch_copies"] = branch_copy_rows(rows_by_name["wep_intake"])

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

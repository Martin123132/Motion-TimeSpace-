from __future__ import annotations

import csv
import math
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
QUARANTINE = ROOT / "source-intake" / "microscope" / "quarantine" / "2660"
FORMALIZATION = PROJECT / "formalization-workbench"
DOC_PATH = ROOT / "2660-Y5-R2FR-coupling-residual-vector-runner-or-visible-domain-signature-proof.md"

CHECKPOINT = "2660"
BRANCH_ID = "Y5_R2FR_COUPLING_RESIDUAL_VECTOR_RUNNER_2660"
PARENT_BRANCH = "Y5_R2FR_NO_HIDDEN_VISIBLE_HOM_OPERATOR_DOMAIN_2659"
PREFIX = "P8_Y5_COUPLING_VECTOR_2660"
MISSING_TOKENS = ("MISSING", "PLACEHOLDER", "TEMPLATE", "UNSIGNED", "NOT_DERIVED", "NOT_SOURCE", "PENDING")

OUTPUTS = {
    "source_register": RESIDUALS / f"{PREFIX}_SOURCE_REGISTER.csv",
    "visible_domain_proof_lane": RESIDUALS / f"{PREFIX}_VISIBLE_DOMAIN_PROOF_LANE.csv",
    "coupling_vector_schema": RESIDUALS / f"{PREFIX}_COUPLING_RESIDUAL_VECTOR_SCHEMA.csv",
    "arena_projection_matrix": RESIDUALS / f"{PREFIX}_ARENA_PROJECTION_MATRIX.csv",
    "input_requirements": RESIDUALS / f"{PREFIX}_EXECUTABLE_INPUT_REQUIREMENTS.csv",
    "runner_results": RESIDUALS / f"{PREFIX}_RUNNER_REFUSAL_RESULTS.csv",
    "score_envelope": RESIDUALS / f"{PREFIX}_NO_CANCELLATION_SCORE_ENVELOPE.csv",
    "claim_gates": RESIDUALS / f"{PREFIX}_CLAIM_GATES.csv",
    "decision": RESIDUALS / f"{PREFIX}_DECISION_LEDGER.csv",
    "next_target": RESIDUALS / f"{PREFIX}_NEXT_TARGET.csv",
    "project_status": RESIDUALS / f"{PREFIX}_PROJECT_STATUS_SNAPSHOT.csv",
    "branch_copies": RESIDUALS / f"{PREFIX}_BRANCH_COPIES.csv",
    "validation": RESIDUALS / f"P8_Y5_BRR545_{CHECKPOINT}_VALIDATION.csv",
}

BRANCH_COPIES = {
    "queue": QUEUE / "JR2660_COUPLING_VECTOR_INPUT_QUEUE_NONCLAIM.csv",
    "local_bounds": LOCAL_BOUNDS / "coupling_residual_vector_2660_NONCLAIM.csv",
    "source_weight": SOURCE_WEIGHT / "COUPLING_VECTOR_RUNNER_2660_NONCLAIM.csv",
    "microscope": MICROSCOPE / "P8_Y5_2660_COUPLING_VECTOR_SCHEMA.csv",
    "quarantine": QUARANTINE / "P8_Y5_2660_RUNNER_REFUSAL_RESULTS.csv",
}

SOURCE_SPECS: dict[str, dict[str, Any]] = {
    "2659_doc": {
        "path": ROOT / "2659-Y5-R2FR-no-hidden-visible-hom-operator-domain-theorem-or-finite-source-row.md",
        "needles": ["ODT2659_1_exact_typed_theorem", "FRV2659_6_acceptance", "VAL2659_OVERALL"],
        "role": "immediate handoff: conditional operator-domain theorem and finite coupling vector selected",
    },
    "2658_doc": {
        "path": ROOT / "2658-Y5-R2FR-neighbourhood-quotient-descent-or-MOMS-parent-signature-source-map.md",
        "needles": ["NQD2658_5_verdict", "MOMS2658_7_verdict", "VAL2658_OVERALL"],
        "role": "neighbourhood descent and MOMS source map remain unsigned",
    },
    "1032_doc": {
        "path": ROOT / "1032-Y5-R10-spm-closure-ledger-and-finite-cg-tau-acquisition-runner.md",
        "needles": ["ACQ1032_1_finite_cg_value", "READY1032_0_R10_finite", "V1032_SUMMARY"],
        "role": "finite c_g/tau acquisition precedent and R10 readiness formula",
    },
    "1706_doc": {
        "path": ROOT / "1706-Y5-R2FR-Delta-w-parent-zero-final-route-or-direct-product-only.md",
        "needles": ["DEM1706_0_split_formula", "ZSG1706_7_verdict", "VAL1706_OVERALL"],
        "role": "source-weight split demotion and direct WEP product guard",
    },
    "1044_doc": {
        "path": ROOT / "1044-Y5-R10-matter-pullback-JX-zero-or-qbarXT-bound-row.md",
        "needles": ["MPD1044_3_constants_zero", "MPD1044_7_exact_theorem_if_signed", "V1044_SUMMARY"],
        "role": "constant marker and matter-pullback conditional theorem",
    },
    "1045_doc": {
        "path": ROOT / "1045-Y5-R10-parent-matter-functor-descent-signature-or-qbar-component-fill.md",
        "needles": ["MFS1045_4_no_shadow_frame", "MFS1045_6_verdict", "V1045_SUMMARY"],
        "role": "no-shadow frame and parent matter functor gap",
    },
    "2656_doc": {
        "path": ROOT / "2656-Y5-R2FR-official-MICROSCOPE-readout-data-dry-run-or-source-worldtube-residual-bound.md",
        "needles": ["SRB2656_5_verdict", "CG2656_1_residual_bound", "VAL2656_OVERALL"],
        "role": "WEP/source-worldtube readout kernel and tau_WEP missing-input gate",
    },
    "1933_doc": {
        "path": ROOT / "1933-Y5-R2FR-coefficient-descent-typing-proof-or-finite-source-row-selection.md",
        "needles": ["TYPE1933_4_verdict", "QDT1933_3_verdict", "VAL1933_OVERALL"],
        "role": "coefficient descent iff fibre-invariance theorem remains conditional",
    },
}


def stamp() -> str:
    return datetime.now(timezone.utc).isoformat()


def ensure_dirs() -> None:
    for path in list(OUTPUTS.values()) + list(BRANCH_COPIES.values()) + [DOC_PATH]:
        path.parent.mkdir(parents=True, exist_ok=True)


def remove_pycache() -> None:
    pycache = ROOT / "scripts" / "__pycache__"
    if pycache.exists():
        shutil.rmtree(pycache)


def read_text(path: Path) -> str:
    if not path.exists() or not path.is_file():
        return ""
    return path.read_text(encoding="utf-8", errors="replace")


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    if not rows:
        raise ValueError(f"refusing to write empty csv: {path}")
    path.parent.mkdir(parents=True, exist_ok=True)
    fieldnames: list[str] = []
    for row in rows:
        for key in row:
            if key not in fieldnames:
                fieldnames.append(key)
    with path.open("w", newline="", encoding="utf-8") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow({field: row.get(field, "") for field in fieldnames})


def csv_rows(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as csvfile:
        return list(csv.DictReader(csvfile))


def markdown_table(rows: list[dict[str, Any]]) -> str:
    if not rows:
        return ""
    fieldnames: list[str] = []
    for row in rows:
        for key in row:
            if key not in fieldnames:
                fieldnames.append(key)
    header = "| " + " | ".join(fieldnames) + " |"
    separator = "| " + " | ".join("---" for _ in fieldnames) + " |"
    body: list[str] = []
    for row in rows:
        values = [str(row.get(field, "")).replace("\n", " ").replace("|", "\\|") for field in fieldnames]
        body.append("| " + " | ".join(values) + " |")
    return "\n".join([header, separator, *body])


def has_missing(value: Any) -> bool:
    text = str(value)
    return any(token in text for token in MISSING_TOKENS)


def is_numeric(value: Any) -> bool:
    try:
        number = float(value)
    except (TypeError, ValueError):
        return False
    return math.isfinite(number)


def source_register_rows() -> list[dict[str, Any]]:
    generated = stamp()
    rows: list[dict[str, Any]] = []
    for source_id, spec in SOURCE_SPECS.items():
        path = Path(spec["path"])
        text = read_text(path)
        missing = [needle for needle in spec["needles"] if needle not in text]
        rows.append(
            {
                "source_id": f"SRC2660_{source_id}",
                "role": spec["role"],
                "path": str(path),
                "exists": path.exists(),
                "needles_required": len(spec["needles"]),
                "missing_needles": "; ".join(missing),
                "status": "EXISTS_NEEDLES_CONFIRMED" if path.exists() and not missing else "MISSING_SOURCE_OR_NEEDLE",
                "valid_for_claim": False,
                "timestamp_utc": generated,
            }
        )
    return rows


def visible_domain_proof_lane_rows() -> list[dict[str, Any]]:
    generated = stamp()
    rows = [
        {
            "proof_id": "VDP2660_0_domain_target",
            "premise": "ordinary visible coefficient algebra",
            "required_statement": "A_ord = q^*A_Q plus A_fixed for visible matter/readout coefficients",
            "if_signed": "hidden-visible homomorphisms become ill-typed",
            "current_status": "TARGET_EXACT",
            "source_ref": "2659:ODT2659_1_exact_typed_theorem",
        },
        {
            "proof_id": "VDP2660_1_fibre_invariance",
            "premise": "visible coefficients are constant on q-fibres",
            "required_statement": "dc_vis(v_X)=0 for every vertical v_X in ker(Dq)",
            "if_signed": "local coupling zero can use the quotient theorem without a closure axiom",
            "current_status": "CONDITIONAL_THEOREM_AVAILABLE",
            "source_ref": "1933:QDT1933_3_verdict",
        },
        {
            "proof_id": "VDP2660_2_fixed_constants",
            "premise": "ordinary constants are fixed representation data",
            "required_statement": "dtheta_A(v_X)=0 for alpha_EM, masses, charges, clocks and material standards",
            "if_signed": "constant/marker rows become theorem-zero",
            "current_status": "UNSIGNED",
            "source_ref": "1044:MPD1044_3_constants_zero",
        },
        {
            "proof_id": "VDP2660_3_no_extra_slots",
            "premise": "ordinary matter has no hidden frame/source/readout argument",
            "required_statement": "S_ord cannot depend on A_g(X), B_g(X), source-only metric frames, or post-readout coefficient maps",
            "if_signed": "c_g, b_dis and readout selector rows become theorem-zero",
            "current_status": "UNSIGNED_CLOSURE_ONLY",
            "source_ref": "1045:MFS1045_4_no_shadow_frame;1032:SPML1032_0_branch_definition",
        },
        {
            "proof_id": "VDP2660_4_no_source_weights",
            "premise": "one global ordinary current/action normalization",
            "required_statement": "w_A(X), Delta_w_X and direct source-only coefficient maps are not allowed operators",
            "if_signed": "WEP/source-weight residual can be zeroed by theorem",
            "current_status": "UNSIGNED",
            "source_ref": "1706:DEM1706_0_split_formula",
        },
        {
            "proof_id": "VDP2660_5_verdict",
            "premise": "2660 visible-domain signature proof lane",
            "required_statement": "all rows above are parent-signed by a single ordinary matter/domain construction",
            "if_signed": "coupling vector collapses to retained boundary/domain source tails",
            "current_status": "VISIBLE_DOMAIN_SIGNATURE_NOT_PARENT_DERIVED",
            "source_ref": "2659:ODT2659_6_verdict",
        },
    ]
    return [
        {
            "branch_id": BRANCH_ID,
            **row,
            "parent_signed": False,
            "valid_for_claim": False,
            "timestamp_utc": generated,
        }
        for row in rows
    ]


def coupling_vector_schema_rows() -> list[dict[str, Any]]:
    generated = stamp()
    rows = [
        {
            "component_id": "CV2660_0_c_g",
            "coefficient": "c_g",
            "coefficient_value": "MISSING_C_G",
            "units": "dimensionless",
            "theorem_zero_status": "MISSING_VISIBLE_DOMAIN_SIGNATURE_OR_SPM_CLOSURE_ONLY",
            "projection_required": "tau_R10;tau_PPN;tau_clock;tau_source",
            "source_path": "MISSING_PARENT_SOURCE",
            "source_row": "MISSING_SOURCE_ROW_ID",
            "arena_links": "R10;PPN;clock_common;source_normalization",
            "contribution_formula": "abs(c_g) * (abs(tau_R10*K_R10) + abs(tau_PPN*R_PPN) + abs(tau_clock*R_clock) + abs(tau_source*R_source))",
        },
        {
            "component_id": "CV2660_1_b_dis",
            "coefficient": "b_dis",
            "coefficient_value": "MISSING_B_DIS",
            "units": "dimensionless",
            "theorem_zero_status": "MISSING_NO_SHADOW_FRAME_SIGNATURE",
            "projection_required": "tau_PPN;tau_clock;tau_orbital",
            "source_path": "MISSING_PARENT_SOURCE",
            "source_row": "MISSING_SOURCE_ROW_ID",
            "arena_links": "PPN;clock;orbital",
            "contribution_formula": "abs(b_dis) * (abs(tau_PPN*R_dis_PPN) + abs(tau_clock*R_dis_clock) + abs(tau_orbital*R_dis_orbital))",
        },
        {
            "component_id": "CV2660_2_b_alpha",
            "coefficient": "dln_alpha_EM_dX",
            "coefficient_value": "MISSING_DALPHA_DX",
            "units": "per_parent_X_unit",
            "theorem_zero_status": "MISSING_FIXED_CONSTANT_SECTOR",
            "projection_required": "tau_clock;tau_EM;tau_WEP_material",
            "source_path": "MISSING_PARENT_SOURCE",
            "source_row": "MISSING_SOURCE_ROW_ID",
            "arena_links": "EM;clocks;WEP_material",
            "contribution_formula": "abs(dln_alpha_EM_dX) * (abs(tau_clock*S_alpha_clock) + abs(tau_EM*S_alpha_EM) + abs(tau_WEP_material*S_alpha_material))",
        },
        {
            "component_id": "CV2660_3_b_mass",
            "coefficient": "dln_m_A_dX",
            "coefficient_value": "MISSING_DMASS_DX_VECTOR",
            "units": "per_parent_X_unit",
            "theorem_zero_status": "MISSING_FIXED_CONSTANT_AND_MATERIAL_SECTOR",
            "projection_required": "tau_WEP;tau_clock;tau_orbital",
            "source_path": "MISSING_PARENT_SOURCE",
            "source_row": "MISSING_SOURCE_ROW_ID",
            "arena_links": "WEP;clocks;orbital;source_mass",
            "contribution_formula": "sum_A abs(dln_m_A_dX * material_fraction_A) * abs(tau_material_A)",
        },
        {
            "component_id": "CV2660_4_P_WEP_source_weight",
            "coefficient": "P_WEP_source_weight",
            "coefficient_value": "MISSING_DIRECT_WEP_PRODUCT",
            "units": "dimensionless_eta_like",
            "theorem_zero_status": "MISSING_GLOBAL_SOURCE_COUPLING_THEOREM",
            "projection_required": "official_MICROSCOPE_readout_or_tau_WEP",
            "source_path": "MISSING_SOURCE_MATERIAL_READOUT_ARTIFACTS",
            "source_row": "MISSING_DIRECT_PRODUCT_ROW",
            "arena_links": "MICROSCOPE_WEP;local_GR_source_side",
            "contribution_formula": "abs(P_WEP_source_weight)",
        },
        {
            "component_id": "CV2660_5_q_nonH",
            "coefficient": "q_nonH_domain_tail",
            "coefficient_value": "MISSING_Q_NONH_DOMAIN_TAIL",
            "units": "arena_normalized",
            "theorem_zero_status": "MISSING_HILBERT_DOMAIN_SUPPORT_THEOREM",
            "projection_required": "tau_R10;tau_PPN;tau_orbital;tau_WEP",
            "source_path": "MISSING_PARENT_SOURCE",
            "source_row": "MISSING_SOURCE_ROW_ID",
            "arena_links": "R10;PPN;orbital;WEP;measured_GM",
            "contribution_formula": "abs(q_nonH) + abs(Delta_W_support) + abs(q_boundary) + abs(q_domain)",
        },
        {
            "component_id": "CV2660_6_tau_pack",
            "coefficient": "tau_projection_pack",
            "coefficient_value": "MISSING_TAU_R10_TAU_PPN_TAU_WEP_TAU_CLOCK_TAU_ORBITAL",
            "units": "arena_specific",
            "theorem_zero_status": "NOT_A_ZERO_COEFFICIENT",
            "projection_required": "all arenas require projection conventions",
            "source_path": "MISSING_ARENA_PROJECTION_SOURCES",
            "source_row": "MISSING_PROJECTION_ROW_IDS",
            "arena_links": "R10;PPN;WEP;clocks;orbital;EM",
            "contribution_formula": "transfer factors multiply all finite coupling coefficients; tau=1 shortcut is forbidden",
        },
        {
            "component_id": "CV2660_7_total_policy",
            "coefficient": "coupling_vector_total",
            "coefficient_value": "NOT_NUMERIC_SUM_VALUES_MISSING",
            "units": "arena_specific_abs_envelope",
            "theorem_zero_status": "VECTOR_TOTAL_REQUIRES_ALL_COMPONENTS",
            "projection_required": "all nonzero components theorem-zero or source-backed numeric",
            "source_path": "this checkpoint",
            "source_row": "CV2660_0 through CV2660_6",
            "arena_links": "all local arenas",
            "contribution_formula": "Residual_bound(arena) <= sum_i abs(projection_i(arena) * coefficient_i) + retained_tail_abs",
        },
    ]
    return [
        {
            "branch_id": BRANCH_ID,
            **row,
            "score_ready": False,
            "valid_for_claim": False,
            "timestamp_utc": generated,
        }
        for row in rows
    ]


def arena_projection_matrix_rows() -> list[dict[str, Any]]:
    generated = stamp()
    rows = [
        {
            "arena_id": "APM2660_0_R10",
            "arena": "R10 fifth-force",
            "observable": "alpha_R10(lambda)",
            "vector_components": "c_g;b_alpha;b_mass;q_nonH;tau_R10",
            "score_formula": "alpha_R10(lambda) = K_X(lambda) Qbar_XH tau_R10 c_g + tail_alpha_abs(lambda)",
            "required_sources": "R10 bound curve;K_X(lambda);Qbar_XH;tau_R10;profile convention;coefficient values",
            "current_status": "NOT_SCORE_READY",
        },
        {
            "arena_id": "APM2660_1_PPN",
            "arena": "PPN/local solar-system",
            "observable": "gamma,beta,preferred-frame residual vector",
            "vector_components": "c_g;b_dis;q_nonH;tau_PPN",
            "score_formula": "||Delta_PPN|| <= |tau_PPN,cg c_g| + |tau_PPN,dis b_dis| + |tail_PPN|",
            "required_sources": "PPN response matrix;arena projection;coefficient values;Cassini/ephemeris bounds",
            "current_status": "NOT_SCORE_READY",
        },
        {
            "arena_id": "APM2660_2_WEP_MICROSCOPE",
            "arena": "MICROSCOPE/WEP",
            "observable": "eta_TiPt or direct source-weight product",
            "vector_components": "P_WEP_source_weight;b_mass;b_alpha;q_nonH;tau_WEP",
            "score_formula": "|eta_res| <= |P_WEP_source_weight| + |material_marker_terms| + |readout_tail|",
            "required_sources": "direct product or official source/material/readout artifacts;no split Delta_w default",
            "current_status": "NOT_SCORE_READY",
        },
        {
            "arena_id": "APM2660_3_clocks_EM",
            "arena": "clocks/EM/fine-structure",
            "observable": "clock redshift/frequency/fine-structure drift residual",
            "vector_components": "b_alpha;b_mass;c_g;b_dis;tau_clock;tau_EM",
            "score_formula": "|Delta_clock| <= |S_alpha b_alpha| + |S_mass b_mass| + |frame_terms|",
            "required_sources": "clock sensitivities;EM projection;constant-sector theorem or coefficients",
            "current_status": "NOT_SCORE_READY",
        },
        {
            "arena_id": "APM2660_4_orbital_Newton",
            "arena": "orbital/Newton source side",
            "observable": "measured GM/orbital residual",
            "vector_components": "q_nonH;b_mass;c_g;b_dis;tau_orbital",
            "score_formula": "|Delta_GM| <= |source_mass_marker| + |domain_tail| + |frame_tail|",
            "required_sources": "same-frame source mass;Hilbert/worldtube equality;orbital projection",
            "current_status": "NOT_SCORE_READY",
        },
        {
            "arena_id": "APM2660_5_local_GR_gate",
            "arena": "local GR/Newton reduction",
            "observable": "all local right-hand coupling residuals",
            "vector_components": "all vector components plus left-hand EH/Newton gates",
            "score_formula": "local pass requires every vector component theorem-zero/source-bounded plus separate left-hand field-equation limits",
            "required_sources": "visible-domain theorem or complete vector;Bianchi/conservation;EH/Newton limit",
            "current_status": "BLOCKED_NOT_A_SINGLE_VECTOR_CLAIM",
        },
    ]
    return [
        {
            "branch_id": BRANCH_ID,
            **row,
            "score_ready": False,
            "valid_for_claim": False,
            "timestamp_utc": generated,
        }
        for row in rows
    ]


def input_requirement_rows() -> list[dict[str, Any]]:
    generated = stamp()
    rows = [
        ("REQ2660_0_numeric_or_zero", "each coefficient must be either parent theorem-zero or numeric source-backed", "coefficient_value;theorem_zero_status;source_path;source_row"),
        ("REQ2660_1_units", "every numeric coefficient and projection must declare units and normalization", "units;projection_required;arena convention"),
        ("REQ2660_2_projection", "each arena must have a derived/source projection factor, never tau=1 by default", "tau_R10;tau_PPN;tau_WEP;tau_clock;tau_orbital"),
        ("REQ2660_3_source_paths", "all claim-valid rows need existing source paths and row ids", "source_path;source_row"),
        ("REQ2660_4_no_missing", "no MISSING/PENDING/PLACEHOLDER markers may survive in score rows", "all fields"),
        ("REQ2660_5_no_cancellation", "total residual must be an absolute envelope, not cancellation between unknown signs", "score_envelope"),
        ("REQ2660_6_branch_separation", "SPM closure, theorem-zero and finite-vector branches must be reported separately", "branch_id;theorem_zero_status"),
    ]
    return [
        {
            "branch_id": BRANCH_ID,
            "requirement_id": requirement_id,
            "requirement": requirement,
            "applies_to_fields": fields,
            "status": "ACTIVE_REQUIREMENT",
            "valid_for_claim": False,
            "timestamp_utc": generated,
        }
        for requirement_id, requirement, fields in rows
    ]


def evaluate_vector_row(row: dict[str, Any]) -> dict[str, Any]:
    missing_fields = []
    for field in ("coefficient_value", "source_path", "source_row", "projection_required", "theorem_zero_status"):
        if has_missing(row.get(field, "")):
            missing_fields.append(field)
    numeric = is_numeric(row.get("coefficient_value"))
    theorem_zero = str(row.get("theorem_zero_status", "")).startswith("PARENT_SIGNED_ZERO")
    if row["component_id"] == "CV2660_7_total_policy":
        status = "REJECTED_COMPONENT_VALUES_MISSING"
    elif theorem_zero:
        status = "ACCEPT_THEOREM_ZERO_NONCLAIM"
    elif numeric and not missing_fields:
        status = "RUNNER_READY_NONCLAIM"
    else:
        status = "REJECTED_MISSING_PROVENANCE"
    return {
        "branch_id": BRANCH_ID,
        "result_id": f"RUN2660_{row['component_id'].split('_')[-1]}",
        "component_id": row["component_id"],
        "coefficient": row["coefficient"],
        "numeric_value": numeric,
        "theorem_zero": theorem_zero,
        "missing_fields": ";".join(missing_fields),
        "runner_status": status,
        "score_ready": False,
        "claim_allowed": False,
        "valid_for_claim": False,
        "timestamp_utc": stamp(),
    }


def runner_result_rows(vector_rows: list[dict[str, Any]], arena_rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    rows = [evaluate_vector_row(row) for row in vector_rows]
    for arena in arena_rows:
        rows.append(
            {
                "branch_id": BRANCH_ID,
                "result_id": f"RUN2660_{arena['arena_id'].split('_')[-1]}",
                "component_id": arena["arena_id"],
                "coefficient": arena["observable"],
                "numeric_value": False,
                "theorem_zero": False,
                "missing_fields": "arena_projection;coefficient_values;source_paths",
                "runner_status": "REJECTED_ARENA_NOT_SCORE_READY",
                "score_ready": False,
                "claim_allowed": False,
                "valid_for_claim": False,
                "timestamp_utc": stamp(),
            }
        )
    return rows


def score_envelope_rows() -> list[dict[str, Any]]:
    generated = stamp()
    rows = [
        {
            "envelope_id": "ENV2660_0_R10",
            "arena": "R10",
            "absolute_envelope": "|alpha_R10(lambda)| <= |K_X(lambda) Qbar_XH tau_R10 c_g| + |alpha_constant_tail| + |alpha_nonH_tail|",
            "claim_rule": "score only when every term is theorem-zero or source-backed numeric over lambda grid",
        },
        {
            "envelope_id": "ENV2660_1_PPN",
            "arena": "PPN",
            "absolute_envelope": "||Delta_PPN|| <= |R_cg c_g| + |R_dis b_dis| + |R_nonH q_nonH|",
            "claim_rule": "no cancellation between PPN components; use norm or componentwise absolute bounds",
        },
        {
            "envelope_id": "ENV2660_2_WEP",
            "arena": "WEP",
            "absolute_envelope": "|eta| <= |P_WEP_source_weight| + |eta_constants| + |eta_readout_tail|",
            "claim_rule": "direct product or official readout artifacts required; split Delta_w*tau_WEP is diagnostic only",
        },
        {
            "envelope_id": "ENV2660_3_clock_EM",
            "arena": "clocks/EM",
            "absolute_envelope": "|Delta_clock| <= |S_alpha dln_alpha/dX| + |S_mass dln_m/dX| + |frame_tail|",
            "claim_rule": "clock sensitivities and constant-sector inputs must be sourced",
        },
        {
            "envelope_id": "ENV2660_4_global",
            "arena": "local GR right-hand source side",
            "absolute_envelope": "Residual_source <= sum_i |projection_i * coefficient_i| + retained_boundary_domain_abs",
            "claim_rule": "all source-side terms closed does not by itself close left-hand EH/Newton/Bianchi gates",
        },
    ]
    return [
        {
            "branch_id": BRANCH_ID,
            **row,
            "no_cancellation": True,
            "score_ready": False,
            "valid_for_claim": False,
            "timestamp_utc": generated,
        }
        for row in rows
    ]


def claim_gate_rows() -> list[dict[str, Any]]:
    generated = stamp()
    rows = [
        ("CG2660_0_visible_domain", "visible coefficient domain signature is parent-derived", "FAIL_VISIBLE_DOMAIN_SIGNATURE_NOT_PARENT_DERIVED", "VDP2660_5_verdict"),
        ("CG2660_1_vector_executable", "coupling residual vector has score-ready rows", "FAIL_VECTOR_ROWS_REJECTED", "RUN2660 results"),
        ("CG2660_2_arena_projection", "R10/PPN/WEP/clock/orbital projections are sourced", "FAIL_PROJECTIONS_MISSING", "APM2660 rows"),
        ("CG2660_3_no_cancellation", "absolute envelope policy is active", "PASS_GUARD_NO_CANCELLATION", "ENV2660 rows"),
        ("CG2660_4_local_GR_claim", "local GR/Newton reduction can be claimed", "CLAIM_BLOCKED", "visible domain unsigned; vector non-executable; left-hand gates separate"),
    ]
    return [
        {
            "branch_id": BRANCH_ID,
            "gate_id": gate_id,
            "requirement": requirement,
            "current_status": status,
            "evidence_ref": evidence_ref,
            "gate_pass": False,
            "blocks_claim": True,
            "valid_for_claim": False,
            "timestamp_utc": generated,
        }
        for gate_id, requirement, status, evidence_ref in rows
    ]


def decision_rows() -> list[dict[str, Any]]:
    generated = stamp()
    rows = [
        {
            "decision_id": "DEC2660_0_runner_status",
            "decision": "the fallback is now a vector runner, not a single coupling scalar",
            "reason": "single c_g fallback misses constants, source weights, disformal slots, non-Hilbert tails and arena transfers",
            "next_action": "fill the first arena projection rather than inventing coefficient values",
        },
        {
            "decision_id": "DEC2660_1_best_first_input",
            "decision": "tau_R10/profile projection is the cleanest first finite input",
            "reason": "R10 has the sharpest symbolic formula from 1032 and needs a projection convention before any c_g score",
            "next_action": "derive or source tau_R10, K_X(lambda), Qbar_XH and profile normalization",
        },
        {
            "decision_id": "DEC2660_2_theorem_lane",
            "decision": "keep the visible-domain proof lane open but do not spend the next step only circling it",
            "reason": "the conditional theorem is exact; what is missing is source/signature evidence, while the vector runner can make testing concrete now",
            "next_action": "2661 should focus on R10 projection derivation/acquisition with proof-lane hooks",
        },
    ]
    return [
        {
            "branch_id": BRANCH_ID,
            **row,
            "claim_allowed": False,
            "valid_for_claim": False,
            "timestamp_utc": generated,
        }
        for row in rows
    ]


def next_target_rows() -> list[dict[str, Any]]:
    generated = stamp()
    return [
        {
            "branch_id": BRANCH_ID,
            "next_id": "NEXT2660_0_selected",
            "status": "selected",
            "next_doc": "2661-Y5-R2FR-R10-projection-first-fill-or-visible-domain-source-signature.md",
            "next_script": "scripts/Y5_R2FR_R10_projection_first_fill_or_visible_domain_source_signature_2661.py",
            "task": "derive or source the R10 projection slice of the coupling vector: tau_R10, K_X(lambda), Qbar_XH, source/test profile convention, and alpha(lambda) linkage",
            "must_include": "no tau=1 shortcut; no invented c_g; profile normalization; source paths; units; no-cancellation tail envelope; visible-domain zero switch only if parent-signed",
            "must_exclude": "R10 pass claim, scalar-only c_g score, closure-only SPM as derived proof, cancellation, GitHub action, formalization-workbench edits",
            "claim_allowed": False,
            "valid_for_claim": False,
            "timestamp_utc": generated,
        }
    ]


def project_status_rows() -> list[dict[str, Any]]:
    generated = stamp()
    rows = [
        ("STAT2660_0_progress", "coupling fallback", "EXECUTABLE_SCHEMA_BUILT", "the local coupling fallback is now a component vector with arena projections and runner refusal logic"),
        ("STAT2660_1_derivation", "visible-domain theorem", "EXACT_CONDITIONAL_NOT_PARENT_SIGNED", "proof lane remains sharp but unsigned; no theorem-zero promotion"),
        ("STAT2660_2_testing", "test readiness", "RUNNER_READY_SCHEMA_NOT_SCORE_READY", "the schema can reject placeholders now and accept sourced rows later"),
        ("STAT2660_3_best_next", "next route", "R10_PROJECTION_FIRST", "derive/source tau_R10 and profile convention first because it unlocks the cleanest finite-vector smoke test"),
    ]
    return [
        {
            "branch_id": BRANCH_ID,
            "status_id": status_id,
            "topic": topic,
            "status": status,
            "detail": detail,
            "claim_allowed": False,
            "valid_for_claim": False,
            "timestamp_utc": generated,
        }
        for status_id, topic, status, detail in rows
    ]


def build_rows() -> dict[str, list[dict[str, Any]]]:
    vector_rows = coupling_vector_schema_rows()
    arena_rows = arena_projection_matrix_rows()
    return {
        "source_register": source_register_rows(),
        "visible_domain_proof_lane": visible_domain_proof_lane_rows(),
        "coupling_vector_schema": vector_rows,
        "arena_projection_matrix": arena_rows,
        "input_requirements": input_requirement_rows(),
        "runner_results": runner_result_rows(vector_rows, arena_rows),
        "score_envelope": score_envelope_rows(),
        "claim_gates": claim_gate_rows(),
        "decision": decision_rows(),
        "next_target": next_target_rows(),
        "project_status": project_status_rows(),
    }


def branch_copy_rows() -> list[dict[str, Any]]:
    generated = stamp()
    copy_specs = {
        "queue": (OUTPUTS["input_requirements"], BRANCH_COPIES["queue"], "coupling vector input requirements queue"),
        "local_bounds": (OUTPUTS["coupling_vector_schema"], BRANCH_COPIES["local_bounds"], "local-bound coupling vector schema"),
        "source_weight": (OUTPUTS["score_envelope"], BRANCH_COPIES["source_weight"], "no-cancellation coupling envelope"),
        "microscope": (OUTPUTS["coupling_vector_schema"], BRANCH_COPIES["microscope"], "WEP/MICROSCOPE-visible coupling vector schema"),
        "quarantine": (OUTPUTS["runner_results"], BRANCH_COPIES["quarantine"], "runner refusal/quarantine results"),
    }
    rows: list[dict[str, Any]] = []
    for copy_id, (source, destination, role) in copy_specs.items():
        destination.parent.mkdir(parents=True, exist_ok=True)
        if source.exists():
            shutil.copyfile(source, destination)
        parseable = False
        if destination.exists():
            try:
                csv_rows(destination)
                parseable = True
            except Exception:
                parseable = False
        rows.append(
            {
                "copy_id": f"COPY2660_{copy_id}",
                "role": role,
                "source": str(source),
                "destination": str(destination),
                "exists": destination.exists(),
                "parseable_csv": parseable,
                "valid_for_claim": False,
                "timestamp_utc": generated,
            }
        )
    return rows


def generated_paths() -> list[Path]:
    return [path for key, path in OUTPUTS.items() if key != "validation"] + list(BRANCH_COPIES.values())


def all_csv_parse(paths: list[Path]) -> bool:
    for path in paths:
        if path.suffix.lower() != ".csv":
            continue
        try:
            csv_rows(path)
        except Exception:
            return False
    return True


def formalization_hit_count() -> int:
    if not FORMALIZATION.exists():
        return 0
    patterns = [
        "*2660-Y5-R2FR*",
        f"*{PREFIX}*",
        "*P8_Y5_BRR545_2660*",
        "*Y5_R2FR_coupling_residual_vector_runner_or_visible_domain_signature_proof_2660*",
        "*JR2660*",
    ]
    hits: list[Path] = []
    for pattern in patterns:
        hits.extend(FORMALIZATION.rglob(pattern))
    return len([path for path in hits if path.is_file()])


def validation_rows(rows: dict[str, list[dict[str, Any]]], paths: list[Path]) -> list[dict[str, Any]]:
    source_ok = all(row["status"] == "EXISTS_NEEDLES_CONFIRMED" for row in rows["source_register"])
    proof_ok = any(row["proof_id"] == "VDP2660_5_verdict" and row["current_status"] == "VISIBLE_DOMAIN_SIGNATURE_NOT_PARENT_DERIVED" for row in rows["visible_domain_proof_lane"])
    vector_ok = len(rows["coupling_vector_schema"]) == 8 and any(row["component_id"] == "CV2660_7_total_policy" for row in rows["coupling_vector_schema"])
    arena_ok = len(rows["arena_projection_matrix"]) == 6 and all(not row["score_ready"] for row in rows["arena_projection_matrix"])
    runner_ok = len(rows["runner_results"]) == len(rows["coupling_vector_schema"]) + len(rows["arena_projection_matrix"]) and all(not row["score_ready"] and not row["claim_allowed"] for row in rows["runner_results"]) and any(row["runner_status"] == "REJECTED_MISSING_PROVENANCE" for row in rows["runner_results"])
    envelope_ok = len(rows["score_envelope"]) == 5 and all(row["no_cancellation"] and not row["score_ready"] for row in rows["score_envelope"])
    claim_ok = any(row["gate_id"] == "CG2660_4_local_GR_claim" and row["current_status"] == "CLAIM_BLOCKED" for row in rows["claim_gates"]) and all(not row["gate_pass"] and row["blocks_claim"] for row in rows["claim_gates"])
    next_ok = any("2661-Y5-R2FR-R10-projection-first-fill" in row["next_doc"] for row in rows["next_target"])
    branch_ok = all(row["exists"] and row["parseable_csv"] for row in rows["branch_copies"])
    csv_ok = all_csv_parse(paths)
    formal_ok = formalization_hit_count() == 0
    pycache_ok = not (ROOT / "scripts" / "__pycache__").exists()
    checks = [
        ("VAL2660_00_sources", source_ok, "all cited source paths exist and required needles are present"),
        ("VAL2660_01_proof_lane", proof_ok, "visible-domain theorem lane remains exact but not parent-derived"),
        ("VAL2660_02_vector_schema", vector_ok, "coupling residual vector schema covers components and total policy"),
        ("VAL2660_03_arena_projection", arena_ok, "arena projection matrix covers R10, PPN, WEP, clocks/EM, orbital and local-GR gate"),
        ("VAL2660_04_runner_refuses", runner_ok, "runner refuses missing-provenance/vector-placeholder rows"),
        ("VAL2660_05_no_cancellation", envelope_ok, "no-cancellation absolute envelopes are installed"),
        ("VAL2660_06_claim_gates_blocked", claim_ok, "claim gates block local and arena claims"),
        ("VAL2660_07_next_target", next_ok, "2661 R10 projection first-fill target selected"),
        ("VAL2660_08_branch_copies", branch_ok, "branch copies exist and parse"),
        ("VAL2660_09_csv_parse", csv_ok, "all generated CSVs parse cleanly"),
        ("VAL2660_10_formalization_untouched", formal_ok, "no 2660 outputs are written under formalization-workbench"),
        ("VAL2660_11_pycache_absent", pycache_ok, "scripts __pycache__ absent"),
    ]
    generated = stamp()
    out = [
        {
            "timestamp_utc": generated,
            "checkpoint": CHECKPOINT,
            "branch_id": BRANCH_ID,
            "valid_for_claim": False,
            "claim_allowed": False,
            "validation_id": validation_id,
            "status": "PASS" if passed else "FAIL",
            "detail": detail,
        }
        for validation_id, passed, detail in checks
    ]
    out.append(
        {
            "timestamp_utc": generated,
            "checkpoint": CHECKPOINT,
            "branch_id": BRANCH_ID,
            "valid_for_claim": False,
            "claim_allowed": False,
            "validation_id": "VAL2660_OVERALL",
            "status": "PASS" if all(row["status"] == "PASS" for row in out) else "FAIL",
            "detail": "2660 builds an executable coupling residual vector schema, refuses placeholder scoring, keeps the visible-domain proof lane open, and selects R10 projection first-fill next",
        }
    )
    return out


def write_doc(rows: dict[str, list[dict[str, Any]]]) -> None:
    validation = csv_rows(OUTPUTS["validation"])
    content = f"""# 2660 - Coupling Residual Vector Runner Or Visible Domain Signature Proof

## Purpose

This checkpoint turns the unsigned coupling theorem into an engineering object: a residual vector runner. The visible-domain proof lane remains open, but the fallback is now explicit, multi-component and arena-projected.

## Result

- The visible-domain theorem remains exact but unsigned: if `A_ord = q^*A_Q + A_fixed`, hidden-visible coupling maps vanish by type/domain exclusion.
- The fallback is no longer a vague scalar. It is a vector: `c_g`, `b_dis`, constant/marker coefficients, direct WEP source-weight product, non-Hilbert/domain tails, and arena transfer factors.
- The runner refuses every current row because the entries are missing theorem-zero status, numeric values, source paths, or projection conventions.
- The next practical target is the R10 projection slice: `tau_R10`, `K_X(lambda)`, `Qbar_XH`, profile normalization, and alpha(lambda) linkage.

## Source Register

{markdown_table(rows["source_register"])}

## Visible-Domain Proof Lane

{markdown_table(rows["visible_domain_proof_lane"])}

## Coupling Residual Vector Schema

{markdown_table(rows["coupling_vector_schema"])}

## Arena Projection Matrix

{markdown_table(rows["arena_projection_matrix"])}

## Executable Input Requirements

{markdown_table(rows["input_requirements"])}

## Runner Refusal Results

{markdown_table(rows["runner_results"])}

## No-Cancellation Score Envelope

{markdown_table(rows["score_envelope"])}

## Claim Gates

{markdown_table(rows["claim_gates"])}

## Decision Ledger

{markdown_table(rows["decision"])}

## Next Target

{markdown_table(rows["next_target"])}

## Project Status Snapshot

{markdown_table(rows["project_status"])}

## Branch Copies

{markdown_table(rows["branch_copies"])}

## Validation

{markdown_table(validation)}
"""
    DOC_PATH.write_text(content, encoding="utf-8")


def main() -> None:
    ensure_dirs()
    remove_pycache()
    rows = build_rows()
    for name, table in rows.items():
        if name in OUTPUTS and name != "validation":
            write_csv(OUTPUTS[name], table)
    rows["branch_copies"] = branch_copy_rows()
    write_csv(OUTPUTS["branch_copies"], rows["branch_copies"])
    remove_pycache()
    rows["validation"] = validation_rows(rows, generated_paths())
    write_csv(OUTPUTS["validation"], rows["validation"])
    write_doc(rows)
    remove_pycache()


if __name__ == "__main__":
    main()

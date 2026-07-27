from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
PROJECT_ROOT = ROOT.parent
FORMALIZATION = PROJECT_ROOT / "formalization-workbench"
OUT = ROOT / "source-intake" / "mts_residuals"
QUEUE = ROOT / "source-intake" / "rab-sector" / "acquisition-queue"
MICROSCOPE = ROOT / "source-intake" / "microscope" / "branch_locked_wep" / "residuals"
BETA_DOCS = ROOT / "source-intake" / "beta-source" / "docs"

BRANCH_ID = "MTS_R2FR_FINITE_Q_PPN_R10_PROJECTION_MATRIX_OR_INPUT_SOURCE_PACK_2285"
START_TS = datetime.now(timezone.utc).timestamp()
DOC = ROOT / "2285-Y5-R2FR-finite-q-PPN-R10-projection-matrix-or-input-source-pack.md"


SOURCES: list[dict[str, Any]] = [
    {
        "source_id": "SRC2285_00_2284_doc",
        "source_key": "2284_finite_q_handoff",
        "source_path": ROOT / "2284-Y5-R2FR-finite-q-residual-coefficient-source-or-local-benchmark-runner.md",
        "needles": ["BUILD_FINITE_Q_PROJECTION_MATRIX_OR_INPUT_SOURCE_PACK_NEXT", "q_R=j_q/M_q^2", "MISSING_OBSERVABLE_PROJECTION"],
        "role": "handoff selecting finite-q observable projection matrix",
    },
    {
        "source_id": "SRC2285_01_2284_validation",
        "source_key": "2284_validation",
        "source_path": OUT / "P8_Y5_BRR545_2284_VALIDATION.csv",
        "needles": ["VAL2284_OVERALL", "PASS"],
        "role": "confirms 2284 passed before 2285 starts",
    },
    {
        "source_id": "SRC2285_02_2231_ppn_dictionary",
        "source_key": "2231_ppn_coefficient_derivation",
        "source_path": OUT / "P8_Y5_PARENT_QLOC_2231_PPN_COEFFICIENT_DERIVATION.csv",
        "needles": ["PPNC2231_0_qR_gamma", "DERIVED_PPN_DICTIONARY_NOT_PARENT_PREDICTION", "PPNC2231_6_perihelion_degeneracy"],
        "role": "PPN translation coefficients for q_R and delta_beta",
    },
    {
        "source_id": "SRC2285_03_2231_readiness",
        "source_key": "2231_readiness_matrix",
        "source_path": OUT / "P8_Y5_PARENT_QLOC_2231_COEFFICIENT_READINESS_MATRIX.csv",
        "needles": ["READY2231_7_R10", "REJECTED_PENDING_INPUTS", "READY2231_8_tracefree"],
        "role": "readiness matrix separating translation from parent prediction",
    },
    {
        "source_id": "SRC2285_04_2230_bound_links",
        "source_key": "2230_local_bound_links",
        "source_path": OUT / "P8_Y5_PARENT_QLOC_2230_LOCAL_BOUND_LINKS.csv",
        "needles": ["BL2230_R3_gamma", "BL2230_R10_fifth_force", "SYMBOLIC_CURVE_REQUIRED"],
        "role": "local comparator rows and R10 symbolic-curve guard",
    },
    {
        "source_id": "SRC2285_05_06_reciprocal_charge",
        "source_key": "06_reciprocal_charge_source_neutrality",
        "source_path": ROOT / "06-reciprocal-charge-source-neutrality.md",
        "needles": ["gamma - 1 ~= q_R", "|q_R| <= 1e-5", "source neutrality parent-derived"],
        "role": "early q_R gamma danger and source-neutrality obstruction",
    },
    {
        "source_id": "SRC2285_06_1012_source_norm_vector",
        "source_key": "1012_R11_source_normalization_vector",
        "source_path": OUT / "P8_Y5_R10_1012_R11_SOURCE_NORMALIZATION_COEFFICIENT_VECTOR.csv",
        "needles": ["Y5C1012_0_radial_Meff_hair", "retained_unfilled", "Y5C1012_7_absolute_calibration_offset"],
        "role": "source-normalization residual coefficient vector",
    },
    {
        "source_id": "SRC2285_07_1012_constant_GM",
        "source_key": "1012_constant_GM_rows",
        "source_path": OUT / "P8_Y5_R10_1012_CONSTANT_GM_RESIDUAL_ROWS.csv",
        "needles": ["GM1012_4_range_dependence", "MISSING_EXECUTABLE_ALPHA_LAMBDA_CURVE_OR_ZERO_THEOREM", "GM1012_6_nonlinear_beta_source"],
        "role": "constant-GM/source-normalization residual rows",
    },
    {
        "source_id": "SRC2285_08_1024_alpha_rows",
        "source_key": "1024_R10_alpha_rows",
        "source_path": OUT / "P8_Y5_R10_1024_ALPHA_COEFFICIENT_ROWS.csv",
        "needles": ["ALPHA1024_3_bulk_R10_projection", "MISSING_ARENA_PROJECTION", "ALPHA1024_5_no_cancellation_guard"],
        "role": "R10 alpha(lambda) projection source-pack schema",
    },
    {
        "source_id": "SRC2285_09_1010_q_loc",
        "source_key": "1010_q_loc_retention",
        "source_path": ROOT / "1010-Y5-R10-Gamma-Khat-action-existence-Helmholtz-or-q_loc-residual-retention.md",
        "needles": ["QRES1010_0_q_loc_vector", "PPN alpha_i/xi", "q_loc is retained as an explicit residual"],
        "role": "q_loc residual retained until parent action route closes",
    },
]


OUTPUTS = {
    "source_register": OUT / "P8_Y5_PARENT_QLOC_2285_SOURCE_REGISTER.csv",
    "state_vector": OUT / "P8_Y5_PARENT_QLOC_2285_POBS_STATE_VECTOR.csv",
    "projection_matrix": OUT / "P8_Y5_PARENT_QLOC_2285_PROJECTION_MATRIX_NONCLAIM.csv",
    "source_pack": OUT / "P8_Y5_PARENT_QLOC_2285_COEFFICIENT_SOURCE_PACK.csv",
    "arena_runner": OUT / "P8_Y5_PARENT_QLOC_2285_ARENA_RUNNER_NONCLAIM.csv",
    "zero_requirements": OUT / "P8_Y5_PARENT_QLOC_2285_ZERO_CONDITION_REQUIREMENTS.csv",
    "claim_gates": OUT / "P8_Y5_PARENT_QLOC_2285_CLAIM_GATES.csv",
    "refusal": OUT / "P8_Y5_PARENT_QLOC_2285_REFUSAL_RUNNER.csv",
    "decision": OUT / "P8_Y5_PARENT_QLOC_2285_DECISION_LEDGER.csv",
    "next_target": OUT / "P8_Y5_PARENT_QLOC_2285_NEXT_TARGET.csv",
    "branch_copies": OUT / "P8_Y5_PARENT_QLOC_2285_BRANCH_COPIES.csv",
    "validation": OUT / "P8_Y5_BRR545_2285_VALIDATION.csv",
}


COPY_TARGETS = {
    "queue_projection_matrix": (
        OUTPUTS["projection_matrix"],
        QUEUE / "JR2285_POBS_PROJECTION_MATRIX_NONCLAIM.csv",
    ),
    "queue_source_pack": (
        OUTPUTS["source_pack"],
        QUEUE / "JR2285_COEFFICIENT_SOURCE_PACK_NONCLAIM.csv",
    ),
    "branch_wep_refusal": (
        OUTPUTS["refusal"],
        MICROSCOPE / "RAB_POBS_projection_refusal_2285.csv",
    ),
    "beta_docs_projection": (
        OUTPUTS["projection_matrix"],
        BETA_DOCS / "RAB_POBS_MATRIX_2285_NONCLAIM.csv",
    ),
}


def stringify(value: Any) -> str:
    if isinstance(value, bool):
        return "True" if value else "False"
    return str(value)


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace") if path.exists() else ""


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        raise ValueError(f"no rows for {path}")
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        for row in rows:
            writer.writerow({key: stringify(value) for key, value in row.items()})


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def csv_parses(path: Path) -> bool:
    try:
        read_csv(path)
        return True
    except Exception:
        return False


def validation_pass(path: Path) -> bool:
    if not path.exists() or not csv_parses(path):
        return False
    rows = read_csv(path)
    if not rows:
        return False
    id_key = "check_id" if "check_id" in rows[0] else "validation_id"
    result_key = "result" if "result" in rows[0] else "status"
    overall_rows = [row for row in rows if "overall" in row.get(id_key, "").lower()]
    if overall_rows:
        return all(row.get(result_key, "").upper() == "PASS" for row in overall_rows)
    return all(row.get(result_key, "").upper() == "PASS" for row in rows)


def remove_pycache() -> None:
    pycache = ROOT / "scripts" / "__pycache__"
    if pycache.exists():
        shutil.rmtree(pycache)


def ignored_environment_path(path: Path) -> bool:
    ignored_parts = {".venv", ".venv-score", "__pycache__", "site-packages", ".git"}
    return any(part in ignored_parts for part in path.parts)


def formalization_has_2285_artifacts() -> bool:
    if not FORMALIZATION.exists():
        return False
    for candidate in FORMALIZATION.rglob("*2285*"):
        if candidate.is_file() and not ignored_environment_path(candidate.relative_to(FORMALIZATION)):
            return True
    return False


def formalization_touched_since_start() -> bool:
    if not FORMALIZATION.exists():
        return False
    for candidate in FORMALIZATION.rglob("*"):
        if candidate.is_file() and not ignored_environment_path(candidate.relative_to(FORMALIZATION)):
            if candidate.stat().st_mtime >= START_TS:
                return True
    return False


def table(headers: list[str], rows: list[dict[str, Any]]) -> str:
    def cell(value: Any) -> str:
        return stringify(value).replace("\n", " ").replace("|", "\\|")

    lines = [
        "| " + " | ".join(headers) + " |",
        "| " + " | ".join("---" for _ in headers) + " |",
    ]
    for row in rows:
        lines.append("| " + " | ".join(cell(row.get(header, "")) for header in headers) + " |")
    return "\n".join(lines)


def source_register_rows() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for source in SOURCES:
        source_path = Path(source["source_path"])
        source_text = read_text(source_path)
        needles = source["needles"]
        rows.append(
            {
                "branch_id": BRANCH_ID,
                "source_id": source["source_id"],
                "source_key": source["source_key"],
                "source_path": source_path,
                "exists": source_path.exists(),
                "needles": "; ".join(needles),
                "needles_present": all(needle in source_text for needle in needles),
                "role": source["role"],
                "valid_for_claim": False,
            }
        )
    return rows


def state_vector_rows() -> list[dict[str, Any]]:
    entries = [
        ("STATE2285_0_qR", "q_R", "scalar reciprocal finite residual", "q_R=j_q/M_q^2 when algebraic finite-q branch is sourced", "M_q^2;j_q;normalization", "MISSING_PARENT_COEFFICIENTS"),
        ("STATE2285_1_QR_hair", "Q_R", "boundary/gradient reciprocal hair", "exterior R_AB hair charge if nabla q or surface momentum survives", "operator inventory; boundary condition; source reciprocal momentum", "MISSING_NO_GRADIENT_NO_HAIR_GUARD"),
        ("STATE2285_2_lambda_q", "lambda_q", "finite q range", "lambda_q=sqrt(Z_q/M_q^2) if a gradient branch exists", "Z_q;M_q^2;units", "MISSING_OPERATOR_RANGE_INPUTS"),
        ("STATE2285_3_delta_beta", "delta_beta", "nonlinear PPN completion drift", "delta_beta=beta-1 in the local PPN dictionary", "second-order weak-field completion", "MISSING_PARENT_BETA_COMPLETION"),
        ("STATE2285_4_alpha_clock", "alpha_clock", "clock/load readout anomaly", "phenomenological redshift residual parameter", "clock/coframe/matter descent", "MISSING_CLOCK_READOUT_MAP"),
        ("STATE2285_5_epsilon_matter", "epsilon_matter", "matter/coframe universality spread", "phenomenological WEP residual parameter", "universal matter action descent", "MISSING_UNIVERSAL_MATTER_COUPLING"),
        ("STATE2285_6_sigma_Gdot", "sigma_Gdot", "source-normalization time drift", "Gdot/source drift channel", "source stationarity theorem or numeric drift coefficient", "MISSING_SOURCE_STATIONARITY"),
        ("STATE2285_7_epsilon_frame", "epsilon_frame_1;epsilon_frame_2", "preferred-frame/coframe leakage", "alpha1/alpha2 response channels", "frame/coframe descent and spin/aniso response", "MISSING_FRAME_RESPONSE"),
        ("STATE2285_8_epsilon_flux", "epsilon_flux", "source flux or preferred-location leakage", "alpha3/xi response channel", "boundary/no-charge/source-flux theorem", "MISSING_BOUNDARY_FLUX_RESPONSE"),
        ("STATE2285_9_hTF", "h_TF_residual", "tracefree tensor/coframe transfer residual", "vector/tensor PPN residual not fixed by scalar R_AB", "tensor/coframe response matrix", "MISSING_TRACEFREE_RESPONSE_MATRIX"),
        ("STATE2285_10_mu_extra", "epsilon_mu_extra[0..7]", "source-normalization extra channels", "radial, boundary, domain, bulk, nonEH, species, time, calibration source rows", "1012 R11 coefficient vector theorem-zero or values", "RETAINED_UNFILLED_SOURCE_NORMALIZATION_VECTOR"),
        ("STATE2285_11_alpha_R10", "alpha_R10(lambda)", "R10 finite-range/fifth-force response", "alpha_bulk+alpha_edge+source-normalization range components", "lambda;K;Qbar;qbar;curve;no-cancellation guard", "MISSING_R10_ARENA_PROJECTION"),
        ("STATE2285_12_q_loc", "q_loc^nu", "local force residual vector", "P_loc(nabla^nu Gamma_eff - nabla_mu K_hat^{mu nu})", "S_GK;metric response;Helmholtz;Euler;boundary", "RETAINED_QLOC_RESIDUAL"),
    ]
    return [
        {
            "state_id": state_id,
            "symbol": symbol,
            "meaning": meaning,
            "definition_or_formula": definition,
            "required_parent_inputs": required,
            "current_status": status,
            "translation_ready": symbol in {"delta_beta"},
            "parent_prediction_ready": False,
            "score_ready": False,
            "valid_for_claim": False,
        }
        for state_id, symbol, meaning, definition, required, status in entries
    ]


def projection_matrix_rows() -> list[dict[str, Any]]:
    return [
        {
            "matrix_id": "POBS2285_0_gamma",
            "observable": "gamma_minus_1",
            "projection_formula": "gamma_minus_1 = 1*q_R + C_gamma_mu*epsilon_mu_extra + C_gamma_qloc*q_loc + ...",
            "known_coefficients": "q_R:1",
            "symbolic_coefficients": "C_gamma_mu;C_gamma_qloc",
            "coefficient_source": "2231 PPN dictionary plus 1012/1010 retained residual rows",
            "translation_status": "Q_R_TRANSLATION_DERIVED_PARENT_QR_MISSING",
            "parent_prediction_ready": False,
            "score_ready": False,
            "valid_prediction_row": False,
            "valid_for_claim": False,
        },
        {
            "matrix_id": "POBS2285_1_beta",
            "observable": "beta_minus_1",
            "projection_formula": "beta_minus_1 = 1*delta_beta + C_beta_source*epsilon_mu_extra + ...",
            "known_coefficients": "delta_beta:1",
            "symbolic_coefficients": "C_beta_source",
            "coefficient_source": "2231 beta definition plus 1012 nonlinear beta source row",
            "translation_status": "BETA_TRANSLATION_DERIVED_PARENT_COMPLETION_MISSING",
            "parent_prediction_ready": False,
            "score_ready": False,
            "valid_prediction_row": False,
            "valid_for_claim": False,
        },
        {
            "matrix_id": "POBS2285_2_light_bending",
            "observable": "solar_light_bending_residual_arcsec",
            "projection_formula": "delta_theta = 0.8756216406841224*q_R + C_light_mu*epsilon_mu_extra + ...",
            "known_coefficients": "q_R:0.8756216406841224 arcsec",
            "symbolic_coefficients": "C_light_mu",
            "coefficient_source": "2231 standard PPN scaling",
            "translation_status": "TRANSLATION_DERIVED_PARENT_QR_MISSING",
            "parent_prediction_ready": False,
            "score_ready": False,
            "valid_prediction_row": False,
            "valid_for_claim": False,
        },
        {
            "matrix_id": "POBS2285_3_shapiro",
            "observable": "solar_Shapiro_residual_microseconds",
            "projection_formula": "delta_t = 59.7375179242781*q_R + C_shapiro_mu*epsilon_mu_extra + ...",
            "known_coefficients": "q_R:59.7375179242781 microseconds",
            "symbolic_coefficients": "C_shapiro_mu",
            "coefficient_source": "2231 standard PPN scaling",
            "translation_status": "TRANSLATION_DERIVED_PARENT_QR_MISSING",
            "parent_prediction_ready": False,
            "score_ready": False,
            "valid_prediction_row": False,
            "valid_for_claim": False,
        },
        {
            "matrix_id": "POBS2285_4_mercury",
            "observable": "Mercury_perihelion_residual_arcsec_per_century",
            "projection_formula": "delta_omega = 28.65467507274745*q_R -14.32733753637373*delta_beta + C_peri_mu*epsilon_mu_extra + ...",
            "known_coefficients": "q_R:28.65467507274745; delta_beta:-14.32733753637373",
            "symbolic_coefficients": "C_peri_mu",
            "coefficient_source": "2231 perihelion degeneracy and 1012 source-normalization rows",
            "translation_status": "TWO_PARAMETER_PPN_TRANSLATION_DERIVED_PARENT_VALUES_MISSING",
            "parent_prediction_ready": False,
            "score_ready": False,
            "valid_prediction_row": False,
            "valid_for_claim": False,
        },
        {
            "matrix_id": "POBS2285_5_clock",
            "observable": "clock_redshift_residual",
            "projection_formula": "delta_clock = 1*alpha_clock + C_clock_mu*epsilon_mu_extra + C_clock_frame*delta_frame_source + ...",
            "known_coefficients": "alpha_clock:1 phenomenological definition",
            "symbolic_coefficients": "C_clock_mu;C_clock_frame",
            "coefficient_source": "2231 phenomenological clock row plus 1012 source/frame rows",
            "translation_status": "PHENOMENOLOGICAL_TRANSLATION_ONLY",
            "parent_prediction_ready": False,
            "score_ready": False,
            "valid_prediction_row": False,
            "valid_for_claim": False,
        },
        {
            "matrix_id": "POBS2285_6_wep",
            "observable": "eta_WEP",
            "projection_formula": "eta = 1*epsilon_matter + C_eta_species*epsilon_species_A + ...",
            "known_coefficients": "epsilon_matter:1 phenomenological proxy",
            "symbolic_coefficients": "C_eta_species",
            "coefficient_source": "2231 WEP proxy plus 1012 species source-charge row",
            "translation_status": "PHENOMENOLOGICAL_TRANSLATION_ONLY",
            "parent_prediction_ready": False,
            "score_ready": False,
            "valid_prediction_row": False,
            "valid_for_claim": False,
        },
        {
            "matrix_id": "POBS2285_7_Gdot",
            "observable": "Gdot_over_G",
            "projection_formula": "Gdot/G = C_Gdot*sigma_Gdot + dln_Geff_dt + dln_Meff_dt + ...",
            "known_coefficients": "none parent-signed",
            "symbolic_coefficients": "C_Gdot;dln_Geff_dt;dln_Meff_dt",
            "coefficient_source": "1012 constant-GM residual rows",
            "translation_status": "SOURCE_NORMALIZATION_INPUTS_MISSING",
            "parent_prediction_ready": False,
            "score_ready": False,
            "valid_prediction_row": False,
            "valid_for_claim": False,
        },
        {
            "matrix_id": "POBS2285_8_preferred_frame",
            "observable": "alpha1_alpha2",
            "projection_formula": "alpha1=C_alpha1*epsilon_frame_1 + M_TF1*h_TF; alpha2=C_alpha2*epsilon_frame_2 + M_TF2*h_TF",
            "known_coefficients": "none parent-signed",
            "symbolic_coefficients": "C_alpha1;C_alpha2;M_TF1;M_TF2",
            "coefficient_source": "2231 readiness/rejection matrix",
            "translation_status": "FRAME_TRACEFREE_RESPONSE_MISSING",
            "parent_prediction_ready": False,
            "score_ready": False,
            "valid_prediction_row": False,
            "valid_for_claim": False,
        },
        {
            "matrix_id": "POBS2285_9_flux_location",
            "observable": "alpha3_xi",
            "projection_formula": "alpha3=C_alpha3*epsilon_flux + B_alpha3; xi=C_xi*epsilon_flux + B_xi",
            "known_coefficients": "none parent-signed",
            "symbolic_coefficients": "C_alpha3;C_xi;B_alpha3;B_xi",
            "coefficient_source": "2231 rejection matrix and 1010 boundary/source residual row",
            "translation_status": "BOUNDARY_FLUX_RESPONSE_MISSING",
            "parent_prediction_ready": False,
            "score_ready": False,
            "valid_prediction_row": False,
            "valid_for_claim": False,
        },
        {
            "matrix_id": "POBS2285_10_R10",
            "observable": "alpha(lambda)",
            "projection_formula": "alpha_total(lambda)=K_q(lambda) Qbar_qH qbar_qT + K_edge Qbar_edge_H qbar_edge_T + alpha_R11(lambda)",
            "known_coefficients": "none parent-signed",
            "symbolic_coefficients": "K_q;Qbar_qH;qbar_qT;K_edge;Qbar_edge_H;qbar_edge_T;alpha_R11",
            "coefficient_source": "1024 alpha coefficient rows and 2230 R10 symbolic bound row",
            "translation_status": "R10_RANGE_AND_ARENA_PROJECTION_MISSING",
            "parent_prediction_ready": False,
            "score_ready": False,
            "valid_prediction_row": False,
            "valid_for_claim": False,
        },
        {
            "matrix_id": "POBS2285_11_q_loc_force",
            "observable": "local_force_PPN_source_vector",
            "projection_formula": "Y_loc = P_obs[q_loc^nu] with q_loc^nu=P_loc(nabla^nu Gamma_eff - nabla_mu K_hat^{mu nu})",
            "known_coefficients": "none parent-signed",
            "symbolic_coefficients": "P_obs_qnu;metric_response_gap;boundary_gap",
            "coefficient_source": "1010 q_loc residual retention",
            "translation_status": "QLOC_OBSERVABLE_MAP_MISSING",
            "parent_prediction_ready": False,
            "score_ready": False,
            "valid_prediction_row": False,
            "valid_for_claim": False,
        },
    ]


def source_pack_rows() -> list[dict[str, Any]]:
    entries = [
        ("PACK2285_0_qR", "q_R", "M_q^2;j_q;normalization", "2284 finite-q audit; 2268/2269/2270 coefficient intake", "derive parent Hessian and q-source leg, or prove j_q=0", "MISSING_PARENT_COEFFICIENTS"),
        ("PACK2285_1_QR_hair", "Q_R", "operator inventory;boundary reciprocal momentum Pi_R", "06 reciprocal charge source neutrality; 2284 no-gradient guard", "prove no-gradient/no-hair or source reciprocal neutrality", "MISSING_NO_HAIR_OR_SOURCE_NEUTRALITY"),
        ("PACK2285_2_delta_beta", "delta_beta", "second-order weak-field completion", "2231 beta definition; 1012 nonlinear beta source row", "derive beta=1 or finite delta_beta from parent weak-field expansion", "MISSING_PARENT_BETA_COMPLETION"),
        ("PACK2285_3_clock_matter", "alpha_clock;epsilon_matter", "universal matter/coframe/clock descent", "2229/2231 matter and clock rows", "prove one observed coframe for matter, clocks, photons, and orbital readout", "MISSING_MATTER_COFRAME_DESCENT"),
        ("PACK2285_4_source_norm", "epsilon_mu_extra[0..7]", "R11 source-normalization vector values or theorem zeros", "1012 R11 source-normalization coefficient vector", "derive Pi_M J_H flux closure, worldtube glue, and no extra mu channels", "RETAINED_UNFILLED_SOURCE_NORMALIZATION_VECTOR"),
        ("PACK2285_5_R10_range", "alpha(lambda);lambda_q", "Z_q;M_q^2;lambda;K;Qbar;qbar;no-cancellation guard", "1024 alpha rows and 2230 R10 symbolic bound row", "derive range/arena projection or keep source-pack rows unscored", "MISSING_R10_RANGE_AND_PROJECTION"),
        ("PACK2285_6_q_loc", "q_loc^nu", "S_GK;metric response;Helmholtz;Euler double-zero;boundary", "1010 q_loc retained residual ledger", "derive q_loc zero or source observable map for retained residual", "MISSING_QLOC_ACTION_RESPONSE_MAP"),
        ("PACK2285_7_tracefree", "h_TF_residual", "tensor/coframe transfer matrix M_TF", "2231 tracefree readiness row", "derive tracefree response matrix before vector/tensor PPN scoring", "MISSING_TRACEFREE_RESPONSE_MATRIX"),
    ]
    return [
        {
            "pack_id": pack_id,
            "target_symbol": symbol,
            "required_inputs": required,
            "source_basis": source_basis,
            "reentry_condition": reentry,
            "current_status": status,
            "parent_prediction_ready": False,
            "score_ready": False,
            "valid_for_claim": False,
        }
        for pack_id, symbol, required, source_basis, reentry, status in entries
    ]


def arena_runner_rows() -> list[dict[str, Any]]:
    entries = [
        ("ARENA2285_0_PPN_scalar", "gamma,beta,light,Shapiro,perihelion", "q_R and delta_beta translations exist", "blocked until parent predicts q_R and delta_beta"),
        ("ARENA2285_1_clocks_WEP", "clock redshift and WEP", "phenomenological proxy rows exist", "blocked until matter/coframe descent predicts alpha_clock and epsilon_matter"),
        ("ARENA2285_2_source_norm", "Gdot/source normalization/orbital GM", "1012 residual vector exists", "blocked until source-normalization rows are zeroed or valued"),
        ("ARENA2285_3_R10", "alpha(lambda) fifth-force curve", "1024 source-pack schema exists", "blocked until range, coupling, and comparator curve are source-backed"),
        ("ARENA2285_4_vector_tensor", "alpha1 alpha2 alpha3 xi tracefree", "symbolic response slots exist", "blocked until frame/boundary/tracefree response matrices are derived"),
        ("ARENA2285_5_q_loc", "local force residual vector", "1010 q_loc retained row exists", "blocked until q_loc zero theorem or P_obs_qnu map exists"),
    ]
    return [
        {
            "runner_id": runner_id,
            "arena": arena,
            "available_translation": available,
            "runner_status": blocked,
            "claim_allowed": False,
            "score_ready": False,
            "valid_for_claim": False,
        }
        for runner_id, arena, available, blocked in entries
    ]


def zero_requirement_rows() -> list[dict[str, Any]]:
    entries = [
        ("ZERO2285_0_qR_zero", "q_R=0", "j_q=0 or no physical q source while M_q^2>0 in same normalization", "parent Hessian/source theorem", "not proven"),
        ("ZERO2285_1_QR_zero", "Q_R=0", "no-gradient/no-boundary-hair or source reciprocal neutrality Pi_R=0", "operator inventory plus boundary/source theorem", "not proven"),
        ("ZERO2285_2_delta_beta_zero", "delta_beta=0", "second-order weak-field completion matches beta=1", "parent weak-field expansion to O(L^2)", "not proven"),
        ("ZERO2285_3_matter_clock_zero", "alpha_clock=epsilon_matter=0", "same coframe and universal matter coupling for clocks/matter/photons/orbits", "matter action descent", "not proven"),
        ("ZERO2285_4_source_norm_zero", "epsilon_mu_extra=0", "Pi_M J_H flux closure, worldtube glue, no extra mu channels", "source-normalization owner theorem", "not proven"),
        ("ZERO2285_5_R10_zero", "alpha(lambda)=0 or bounded", "positive source-free range theorem or explicit alpha components below bounds", "Z/M/J/boundary/projection/no-cancellation inputs", "not proven"),
        ("ZERO2285_6_q_loc_zero", "q_loc^nu=0", "S_GK action, metric response, Helmholtz, Euler double-zero, and boundary no-flux", "Gamma/Khat parent action route", "not proven"),
    ]
    return [
        {
            "zero_id": zero_id,
            "target_zero": target,
            "condition": condition,
            "required_source": required_source,
            "current_status": status,
            "claim_allowed": False,
            "valid_for_claim": False,
        }
        for zero_id, target, condition, required_source, status in entries
    ]


def claim_gate_rows() -> list[dict[str, Any]]:
    return [
        {"claim_id": "CG2285_0_projection_matrix_written", "claim": "P_obs projection matrix/source pack exists", "gate_pass": True, "reason": "matrix covers PPN, clocks/WEP, source normalization, R10, vector/tensor, and q_loc channels", "valid_for_claim": False},
        {"claim_id": "CG2285_1_qR_delta_beta_translation", "claim": "q_R and delta_beta PPN translations are source-backed", "gate_pass": True, "reason": "2231 coefficients are imported as translations only", "valid_for_claim": False},
        {"claim_id": "CG2285_2_parent_predictions", "claim": "parent action predicts q_R, delta_beta, and local residual vector", "gate_pass": False, "reason": "M_q^2, j_q, beta completion, q_loc action route, and source normalization are missing", "valid_for_claim": False},
        {"claim_id": "CG2285_3_R10_score_ready", "claim": "R10 alpha(lambda) branch is score-ready", "gate_pass": False, "reason": "range, coupling, projection, no-cancellation guard, and real curve inputs remain missing", "valid_for_claim": False},
        {"claim_id": "CG2285_4_local_GR_Newton", "claim": "local GR/Newton recovery is derived", "gate_pass": False, "reason": "projection matrix is nonclaim and zero conditions are not parent-derived", "valid_for_claim": False},
    ]


def refusal_rows() -> list[dict[str, Any]]:
    entries = [
        ("REF2285_0_score_translation", "use q_R/beta translations as MTS prediction score", "REFUSED_PARENT_VALUES_MISSING", "translation coefficients exist but parent q_R/delta_beta values or zeros are missing"),
        ("REF2285_1_score_R10", "score alpha(lambda) from symbolic R10 row", "REFUSED_RANGE_PROJECTION_MISSING", "R10 still lacks Z/M/range/coupling/projection/no-cancellation inputs"),
        ("REF2285_2_claim_source_norm", "absorb source-normalization residual into measured GM", "REFUSED_NO_ABSORPTION_CHEAT", "1012 keeps source-normalization vector explicit and unfilled"),
        ("REF2285_3_claim_q_loc_zero", "set q_loc^nu=0 by plateau or bookkeeping stress", "REFUSED_QLOC_ACTION_ROUTE_MISSING", "1010 keeps q_loc retained until S_GK/metric-response/Helmholtz/Euler/boundary clauses close"),
        ("REF2285_4_local_GR", "claim local GR/Newton from projection matrix", "REFUSED_MATRIX_IS_NOT_PARENT_DERIVATION", "matrix is a translation/source-pack, not a zero theorem"),
    ]
    return [
        {
            "refusal_id": refusal_id,
            "attempted_claim": attempted_claim,
            "runner_result": result,
            "blocked_by": blocked_by,
            "score_eligible": False,
            "valid_for_claim": False,
        }
        for refusal_id, attempted_claim, result, blocked_by in entries
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        {
            "decision_id": "DEC2285_0_projection_result",
            "decision": "POBS_MATRIX_WRITTEN_NONCLAIM",
            "reason": "finite q now has a concrete observable vector instead of a vague local-test promise",
            "next_action": "use matrix to decide which parent coefficients are most valuable to derive first",
            "valid_for_claim": False,
        },
        {
            "decision_id": "DEC2285_1_best_leap",
            "decision": "ATTACK_PARENT_WEAK_FIELD_EXPANSION_NEXT",
            "reason": "q_R and delta_beta are the channels with actual PPN translations; deriving their parent values gives the fastest local-GR/Newton progress",
            "next_action": "derive M_q^2, j_q, and delta_beta from one weak-field parent expansion",
            "valid_for_claim": False,
        },
        {
            "decision_id": "DEC2285_2_no_public_claim",
            "decision": "NO_GITHUB_OR_LOCAL_GR_CLAIM",
            "reason": "matrix is useful but parent predictions and zero conditions remain missing",
            "next_action": "keep work private and derivation-first",
            "valid_for_claim": False,
        },
    ]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        {
            "route_id": "NEXT2285_0_primary",
            "next_target": "2286-Y5-R2FR-parent-weak-field-Mq-jq-delta-beta-source-or-zero-theorem.md",
            "script": "scripts/Y5_R2FR_parent_weak_field_Mq_jq_delta_beta_source_or_zero_theorem_2286.py",
            "objective": "derive or explicitly fail the shared weak-field parent expansion that supplies M_q^2, j_q, q_R=j_q/M_q^2, and the second-order beta completion delta_beta in one normalization; if derivation fails, stage finite nonclaim inputs",
            "selection_status": "selected",
            "success_condition": "either q_R and delta_beta become parent-predicted/theorem-zero inputs for the 2285 P_obs matrix, or the exact missing parent-action clauses are queued without local-GR/Newton claims",
            "valid_for_claim": False,
        }
    ]


def generated_claim_flags_false(paths: list[Path]) -> bool:
    false_values = {"", "false", "0", "no", "none", "null"}
    guarded_keys = {
        "parent_prediction_ready",
        "score_ready",
        "valid_prediction_row",
        "valid_for_claim",
        "claim_allowed",
        "score_eligible",
    }
    for path in paths:
        for row in read_csv(path):
            for key, value in row.items():
                if key in guarded_keys and value.strip().lower() not in false_values:
                    return False
    return True


def copy_branch_files() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for copy_id, (source_path, target_path) in COPY_TARGETS.items():
        target_path.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(source_path, target_path)
        rows.append(
            {
                "copy_id": copy_id,
                "source_path": source_path,
                "target_path": target_path,
                "target_exists": target_path.exists(),
                "target_parses": csv_parses(target_path),
                "reason": "branch copy for finite-q P_obs projection matrix/source pack",
            }
        )
    return rows


def validation_rows(all_generated_before_validation: list[Path], branch_copy_rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    source_rows = read_csv(OUTPUTS["source_register"])
    state_rows = read_csv(OUTPUTS["state_vector"])
    matrix_rows = read_csv(OUTPUTS["projection_matrix"])
    pack_rows = read_csv(OUTPUTS["source_pack"])
    arena_rows = read_csv(OUTPUTS["arena_runner"])
    zero_rows = read_csv(OUTPUTS["zero_requirements"])
    gate_rows = read_csv(OUTPUTS["claim_gates"])
    refusal_runner_rows = read_csv(OUTPUTS["refusal"])
    decision_ledger_rows = read_csv(OUTPUTS["decision"])
    next_rows = read_csv(OUTPUTS["next_target"])

    observables = {row["observable"] for row in matrix_rows}
    state_symbols = ";".join(row["symbol"] for row in state_rows)
    checks = [
        ("VAL2285_0_sources_exist", all(row["exists"] == "True" for row in source_rows), "all cited source paths exist"),
        ("VAL2285_1_needles_present", all(row["needles_present"] == "True" for row in source_rows), "all cited source needles are present"),
        ("VAL2285_2_prior_validation", validation_pass(OUT / "P8_Y5_BRR545_2284_VALIDATION.csv"), "2284 validation passes before 2285"),
        (
            "VAL2285_3_state_vector_complete",
            all(symbol in state_symbols for symbol in ["q_R", "Q_R", "lambda_q", "delta_beta", "alpha_clock", "epsilon_matter", "sigma_Gdot", "epsilon_mu_extra", "alpha_R10", "q_loc"]),
            "state vector covers finite q, hair, range, PPN, source-normalization, R10, and q_loc channels",
        ),
        (
            "VAL2285_4_ppn_coefficients_present",
            any(row["observable"] == "gamma_minus_1" and "q_R:1" in row["known_coefficients"] for row in matrix_rows)
            and any(row["observable"] == "Mercury_perihelion_residual_arcsec_per_century" and "delta_beta:-14.32733753637373" in row["known_coefficients"] for row in matrix_rows),
            "PPN q_R and delta_beta translation coefficients are present",
        ),
        (
            "VAL2285_5_projection_arenas_complete",
            observables
            >= {
                "gamma_minus_1",
                "beta_minus_1",
                "solar_light_bending_residual_arcsec",
                "solar_Shapiro_residual_microseconds",
                "Mercury_perihelion_residual_arcsec_per_century",
                "clock_redshift_residual",
                "eta_WEP",
                "Gdot_over_G",
                "alpha1_alpha2",
                "alpha3_xi",
                "alpha(lambda)",
                "local_force_PPN_source_vector",
            },
            "projection matrix covers local scalar, clock/WEP, source, R10, vector/tensor, and q_loc arenas",
        ),
        (
            "VAL2285_6_R10_blocked",
            any(row["observable"] == "alpha(lambda)" and row["translation_status"] == "R10_RANGE_AND_ARENA_PROJECTION_MISSING" for row in matrix_rows),
            "R10 row remains blocked until range/projection inputs exist",
        ),
        (
            "VAL2285_7_source_pack_complete",
            {row["target_symbol"] for row in pack_rows}
            >= {"q_R", "Q_R", "delta_beta", "alpha_clock;epsilon_matter", "epsilon_mu_extra[0..7]", "alpha(lambda);lambda_q", "q_loc^nu", "h_TF_residual"},
            "coefficient source pack covers every retained channel",
        ),
        (
            "VAL2285_8_arena_runner_blocks_claims",
            all(row["claim_allowed"] == "False" and row["score_ready"] == "False" for row in arena_rows),
            "arena runner blocks scoring while parent predictions are missing",
        ),
        (
            "VAL2285_9_zero_requirements_written",
            len(zero_rows) >= 7 and all(row["claim_allowed"] == "False" for row in zero_rows),
            "zero-condition requirements are explicit and nonclaim",
        ),
        (
            "VAL2285_10_claims_blocked",
            any(row["claim_id"] == "CG2285_4_local_GR_Newton" and row["gate_pass"] == "False" for row in gate_rows)
            and any(row["runner_result"] == "REFUSED_MATRIX_IS_NOT_PARENT_DERIVATION" for row in refusal_runner_rows),
            "local GR/Newton claim remains blocked",
        ),
        (
            "VAL2285_11_next_selected",
            any(row["next_target"] == "2286-Y5-R2FR-parent-weak-field-Mq-jq-delta-beta-source-or-zero-theorem.md" for row in next_rows)
            and any(row["decision"] == "ATTACK_PARENT_WEAK_FIELD_EXPANSION_NEXT" for row in decision_ledger_rows),
            "2286 parent weak-field expansion target selected",
        ),
        ("VAL2285_12_csv_parse", all(csv_parses(path) for path in all_generated_before_validation), "all generated 2285 CSVs parse before validation file"),
        ("VAL2285_13_no_claim_flags", generated_claim_flags_false(all_generated_before_validation), "all generated claim/score flags remain false"),
        ("VAL2285_14_branch_copies", all(row["target_exists"] and row["target_parses"] for row in branch_copy_rows), "branch/queue copies exist and parse"),
        ("VAL2285_15_pycache_absent", not (ROOT / "scripts" / "__pycache__").exists(), "scripts __pycache__ absent after run"),
        ("VAL2285_16_formalization_no_2285", not formalization_has_2285_artifacts(), "formalization-workbench has no non-venv 2285 artifacts"),
        ("VAL2285_17_formalization_untouched", not formalization_touched_since_start(), "formalization-workbench untouched during 2285 run"),
    ]
    rows = [
        {
            "check_id": check_id,
            "result": "PASS" if passed else "FAIL",
            "detail": detail,
        }
        for check_id, passed, detail in checks
    ]
    overall_pass = all(row["result"] == "PASS" for row in rows)
    rows.append(
        {
            "check_id": "VAL2285_OVERALL",
            "result": "PASS" if overall_pass else "FAIL",
            "detail": "2285 writes the finite-q P_obs projection matrix/source pack, imports q_R/delta_beta PPN translations, keeps all local claims blocked, and selects parent weak-field expansion next",
        }
    )
    return rows


def write_markdown(
    sources: list[dict[str, Any]],
    states: list[dict[str, Any]],
    matrix: list[dict[str, Any]],
    source_pack: list[dict[str, Any]],
    arena_runner: list[dict[str, Any]],
    zero_requirements: list[dict[str, Any]],
    claim_gates: list[dict[str, Any]],
    refusal: list[dict[str, Any]],
    decisions: list[dict[str, Any]],
    next_target: list[dict[str, Any]],
    branch_copies: list[dict[str, Any]],
    validation: list[dict[str, Any]],
) -> None:
    content = f"""# 2285 - Y5/R2FR Finite q PPN/R10 Projection Matrix Or Input Source Pack

## Verdict

This checkpoint builds the local observable bridge that 2284 asked for. The matrix is useful, but it is not a local-GR proof.

The clean part is the PPN dictionary already earned by 2231: `gamma-1 = q_R`, light bending and Shapiro carry the GR/2 response, and Mercury carries the two-parameter structure `28.65467507274745 q_R - 14.32733753637373 delta_beta` in arcsec/century. That means the finite-`q` branch now has a real local test language.

The hard part remains parent ownership. `q_R`, `delta_beta`, source normalization, R10 range/coupling, tracefree response, and `q_loc^nu` are not parent-predicted yet. So 2285 is a projection/source-pack checkpoint: it tells us exactly where each residual lands, and exactly what theorem or coefficient is needed before scoring.

## Source Register
{table(["source_id", "source_key", "source_path", "exists", "needles_present", "role", "valid_for_claim"], sources)}

## P_obs State Vector
{table(["state_id", "symbol", "meaning", "definition_or_formula", "required_parent_inputs", "current_status", "translation_ready", "parent_prediction_ready", "score_ready", "valid_for_claim"], states)}

## Projection Matrix
{table(["matrix_id", "observable", "projection_formula", "known_coefficients", "symbolic_coefficients", "coefficient_source", "translation_status", "parent_prediction_ready", "score_ready", "valid_prediction_row", "valid_for_claim"], matrix)}

## Coefficient Source Pack
{table(["pack_id", "target_symbol", "required_inputs", "source_basis", "reentry_condition", "current_status", "parent_prediction_ready", "score_ready", "valid_for_claim"], source_pack)}

## Arena Runner
{table(["runner_id", "arena", "available_translation", "runner_status", "claim_allowed", "score_ready", "valid_for_claim"], arena_runner)}

## Zero Condition Requirements
{table(["zero_id", "target_zero", "condition", "required_source", "current_status", "claim_allowed", "valid_for_claim"], zero_requirements)}

## Claim Gates
{table(["claim_id", "claim", "gate_pass", "reason", "valid_for_claim"], claim_gates)}

## Refusal Runner
{table(["refusal_id", "attempted_claim", "runner_result", "blocked_by", "score_eligible", "valid_for_claim"], refusal)}

## Decision Ledger
{table(["decision_id", "decision", "reason", "next_action", "valid_for_claim"], decisions)}

## Next Target
{table(["route_id", "next_target", "script", "objective", "selection_status", "success_condition", "valid_for_claim"], next_target)}

## Branch Copies
{table(["copy_id", "source_path", "target_path", "target_exists", "target_parses", "reason"], branch_copies)}

## Validation
{table(["check_id", "result", "detail"], validation)}

## Working Interpretation

This is the bit where the theory starts to look less like smoke and more like an instrument panel. The panel now has named gauges. The next job is not another broad audit; it is a direct derivation attempt for the most valuable gauges: `M_q^2`, `j_q`, `q_R`, and `delta_beta` from the same weak-field parent expansion.
"""
    DOC.write_text(content, encoding="utf-8")


def main() -> None:
    remove_pycache()
    sources = source_register_rows()
    states = state_vector_rows()
    matrix = projection_matrix_rows()
    source_pack = source_pack_rows()
    arena_runner = arena_runner_rows()
    zero_requirements = zero_requirement_rows()
    claim_gates = claim_gate_rows()
    refusal = refusal_rows()
    decisions = decision_rows()
    next_target = next_target_rows()

    write_csv(OUTPUTS["source_register"], sources)
    write_csv(OUTPUTS["state_vector"], states)
    write_csv(OUTPUTS["projection_matrix"], matrix)
    write_csv(OUTPUTS["source_pack"], source_pack)
    write_csv(OUTPUTS["arena_runner"], arena_runner)
    write_csv(OUTPUTS["zero_requirements"], zero_requirements)
    write_csv(OUTPUTS["claim_gates"], claim_gates)
    write_csv(OUTPUTS["refusal"], refusal)
    write_csv(OUTPUTS["decision"], decisions)
    write_csv(OUTPUTS["next_target"], next_target)

    branch_copies = copy_branch_files()
    write_csv(OUTPUTS["branch_copies"], branch_copies)

    generated_before_validation = [
        OUTPUTS["source_register"],
        OUTPUTS["state_vector"],
        OUTPUTS["projection_matrix"],
        OUTPUTS["source_pack"],
        OUTPUTS["arena_runner"],
        OUTPUTS["zero_requirements"],
        OUTPUTS["claim_gates"],
        OUTPUTS["refusal"],
        OUTPUTS["decision"],
        OUTPUTS["next_target"],
        OUTPUTS["branch_copies"],
    ]
    remove_pycache()
    validation = validation_rows(generated_before_validation, branch_copies)
    write_csv(OUTPUTS["validation"], validation)
    write_markdown(
        sources,
        states,
        matrix,
        source_pack,
        arena_runner,
        zero_requirements,
        claim_gates,
        refusal,
        decisions,
        next_target,
        branch_copies,
        validation,
    )
    remove_pycache()

    failed = [row for row in validation if row["result"] != "PASS"]
    if failed:
        failed_ids = ", ".join(row["check_id"] for row in failed)
        raise SystemExit(f"2285 validation failed: {failed_ids}")
    print(f"Wrote {DOC}")
    print(f"Wrote {OUTPUTS['validation']}")


if __name__ == "__main__":
    main()

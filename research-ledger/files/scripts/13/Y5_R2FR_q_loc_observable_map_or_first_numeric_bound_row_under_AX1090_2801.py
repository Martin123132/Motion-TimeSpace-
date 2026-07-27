from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


RUN_STARTED_UTC = datetime.now(timezone.utc)
ROOT = Path(r"D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main")
WORK = ROOT / "post-checkpoint-work"
FORMALIZATION = ROOT / "formalization-workbench"
MTS = WORK / "source-intake" / "mts_residuals"
RAB_QUEUE = WORK / "source-intake" / "rab-sector" / "acquisition-queue"
BETA_DOCS = WORK / "source-intake" / "beta-source" / "docs"
MICROSCOPE_DIR = WORK / "source-intake" / "microscope" / "branch_locked_wep" / "residuals"
SCRIPTS = WORK / "scripts"
DOC = WORK / "2801-Y5-R2FR-q_loc-observable-map-or-first-numeric-bound-row-under-AX1090.md"

OUTPUTS = {
    "sources": MTS / "P8_Y5_R2FR_2801_SOURCE_REGISTER.csv",
    "maps": MTS / "P8_Y5_R2FR_2801_QLOC_OBSERVABLE_MAP_ATTEMPT.csv",
    "requirements": MTS / "P8_Y5_R2FR_2801_OBSERVABLE_PROJECTION_REQUIREMENTS.csv",
    "numeric_bound": MTS / "P8_Y5_R2FR_2801_FIRST_NUMERIC_BOUND_ROW_ATTEMPT.csv",
    "runner": MTS / "P8_Y5_R2FR_2801_COEFFICIENT_RUNNER.csv",
    "gm_residuals": MTS / "P8_Y5_R2FR_2801_CONSTANT_GM_SOURCE_NORMALIZATION_RESIDUAL_ROWS.csv",
    "no_cancellation": MTS / "P8_Y5_R2FR_2801_NO_CANCELLATION_POLICY.csv",
    "gates": MTS / "P8_Y5_R2FR_2801_CLAIM_GATES.csv",
    "decision": MTS / "P8_Y5_R2FR_2801_DECISION_LEDGER.csv",
    "next": MTS / "P8_Y5_R2FR_2801_NEXT_TARGET.csv",
    "branches": MTS / "P8_Y5_R2FR_2801_BRANCH_COPIES.csv",
    "validation": MTS / "P8_Y5_BRR545_2801_VALIDATION.csv",
}

BRANCH_OUTPUTS = {
    "map_queue": RAB_QUEUE / "JR2801_QLOC_OBSERVABLE_MAP_NONCLAIM.csv",
    "numeric_queue": RAB_QUEUE / "JR2801_FIRST_NUMERIC_BOUND_ROW_NONCLAIM.csv",
    "source_norm_queue": RAB_QUEUE / "JR2801_SOURCE_NORMALIZATION_RESIDUAL_NONCLAIM.csv",
    "beta_doc": BETA_DOCS / "QLOC_OBSERVABLE_MAP_2801_NONCLAIM.csv",
    "microscope_copy": MICROSCOPE_DIR / "microscope_qloc_observable_map_2801_nonclaim.csv",
    "next_queue": RAB_QUEUE / "JR2801_FIRST_REAL_QLOC_MAP_OR_SOURCE_ROW_NEXT.csv",
}


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def sp(path: Path) -> str:
    return str(path)


def ensure_dirs() -> None:
    for path in {p.parent for p in OUTPUTS.values()} | {p.parent for p in BRANCH_OUTPUTS.values()} | {DOC.parent}:
        path.mkdir(parents=True, exist_ok=True)


def read_text(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8", errors="replace")
    except FileNotFoundError:
        return ""


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        path.write_text("", encoding="utf-8")
        return
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def csv_parses(path: Path) -> bool:
    try:
        if not path.exists():
            return False
        with path.open("r", encoding="utf-8", newline="") as handle:
            list(csv.DictReader(handle))
        return True
    except csv.Error:
        return False


def source_entries() -> list[tuple[str, Path, str]]:
    return [
        ("2800_next", MTS / "P8_Y5_R2FR_2800_NEXT_TARGET.csv", "authoritative 2801 target"),
        ("2800_bound_fill", MTS / "P8_Y5_R2FR_2800_QLOC_BOUND_FILL_ROWS.csv", "q_loc proxy/template bound rows"),
        ("2800_even_debt", MTS / "P8_Y5_R2FR_2800_EVEN_DEBT_LEDGER.csv", "Y5/Y6 even debts that survive doublet symmetry"),
        ("2799_q_loc_residual", MTS / "P8_Y5_R2FR_2799_QLOC_RESIDUAL_RETENTION_LEDGER.csv", "retained q_loc residual definition"),
        ("2799_bound_interface", MTS / "P8_Y5_R2FR_2799_QLOC_BOUND_INTERFACE_ROLLED_FORWARD.csv", "rolled-forward q_loc bound interface"),
        ("2733_bound_interface", MTS / "P8_Y5_R2FR_2733_QLOC_RESIDUAL_BOUND_INTERFACE.csv", "original q_loc residual bound interface"),
        ("2733_zero_gate", MTS / "P8_Y5_R2FR_2733_ZERO_THEOREM_GATE.csv", "zero-theorem gate analogue"),
        ("2728_JX_audit", MTS / "P8_Y5_R2FR_2728_JX_ZERO_COMPONENT_AUDIT.csv", "source-current component audit"),
        ("2729_memory_signature", MTS / "P8_Y5_R2FR_2729_PARENT_MEMORY_SIGNATURE_CONTRACT.csv", "memory/boundary signature contract"),
        ("1012_owner_theorem_analogue", MTS / "P8_Y5_R10_1012_Y5_OWNER_THEOREM_ATTEMPT.csv", "source-normalization owner theorem analogue"),
        ("1012_coefficient_vector_analogue", MTS / "P8_Y5_R10_1012_R11_SOURCE_NORMALIZATION_COEFFICIENT_VECTOR.csv", "source-normalization coefficient analogue"),
        ("1012_constant_GM_analogue", MTS / "P8_Y5_R10_1012_CONSTANT_GM_RESIDUAL_ROWS.csv", "constant measured-GM residual analogue"),
        ("1012_claim_gate_analogue", MTS / "P8_Y5_R10_1012_CLAIM_GATE.csv", "claim-gate analogue"),
    ]


def build_sources() -> list[dict[str, Any]]:
    return [
        {
            "source_id": source_id,
            "path": sp(path),
            "exists": path.exists(),
            "role": role,
            "contains_text": bool(read_text(path).strip()) if path.exists() else False,
            "valid_for_claim": False,
            "generated_utc": utc_now(),
        }
        for source_id, path, role in source_entries()
    ]


def build_map_rows() -> list[dict[str, Any]]:
    source_2799 = MTS / "P8_Y5_R2FR_2799_QLOC_RESIDUAL_RETENTION_LEDGER.csv"
    source_2733 = MTS / "P8_Y5_R2FR_2733_QLOC_RESIDUAL_BOUND_INTERFACE.csv"
    source_1012 = MTS / "P8_Y5_R10_1012_R11_SOURCE_NORMALIZATION_COEFFICIENT_VECTOR.csv"
    rows = [
        (
            "QMAP2801_0_K_PPN",
            "K_PPN^a",
            "PPN",
            "Delta_PPN^a <= K_PPN^a ||q_loc||_D",
            "gamma_minus_1; beta_minus_1; alpha1; alpha2; alpha3; xi",
            "dimensionless PPN vector per q_loc norm unit",
            "MISSING_WEAK_FIELD_METRIC_SOLUTION",
            "linearized metric Green map from q_loc to g_00,g_0i,g_ij; PPN gauge normalization; source model",
            source_2733,
        ),
        (
            "QMAP2801_1_K_WEP",
            "K_WEP^{AB}",
            "WEP",
            "eta_AB <= K_WEP^{AB} ||q_loc||_D",
            "MICROSCOPE-like eta_AB; direct geometry force difference",
            "dimensionless eta per q_loc norm unit",
            "MISSING_SOURCE_TEST_BODY_PROJECTION",
            "species/test-body response coefficients; same-frame matter readout; source charge map",
            source_1012,
        ),
        (
            "QMAP2801_2_K_clock",
            "K_clock^i",
            "clocks",
            "|delta nu_i/nu_i| <= K_clock^i ||q_loc||_D",
            "clock redshift; frequency drift; local coframe residual",
            "dimensionless fractional frequency per q_loc norm unit",
            "MISSING_CLOCK_READOUT_MAP",
            "clock Hamiltonian/coframe map; local time projection q_loc^0; units for integration time",
            source_2799,
        ),
        (
            "QMAP2801_3_K_orbital",
            "K_orbital",
            "orbital",
            "|delta a_r| or |d ln mu_obs/dt| <= K_orbital ||q_loc||_D",
            "perihelion/orbit residual; Gdot_over_G; GMdot_over_GM",
            "acceleration or yr^-1 per q_loc norm unit",
            "MISSING_ORBITAL_SOURCE_MODEL",
            "source worldtube measure; orbital averaging kernel; time/radial projection; observed-GM split",
            MTS / "P8_Y5_R10_1012_CONSTANT_GM_RESIDUAL_ROWS.csv",
        ),
        (
            "QMAP2801_4_K_source",
            "K_source",
            "source-normalization",
            "|epsilon_mu| <= K_source ||q_loc||_D",
            "measured-GM/source-normalization residual; Newton/Poisson owner",
            "dimensionless source mass residual per q_loc norm unit",
            "MISSING_Y5_OWNER_OR_NUMERIC_COEFFICIENT",
            "same charge must source Poisson, Gauss, orbit, and clocks before any measured-G absorption is allowed",
            source_1012,
        ),
        (
            "QMAP2801_5_alpha3",
            "c_alpha3",
            "preferred-frame PPN",
            "alpha3 = c_alpha3 . q_loc + higher-order terms",
            "alpha3 pressure channel",
            "dimensionless",
            "MISSING_QLOC_TO_ALPHA3_COEFFICIENT",
            "preferred-frame vector projection and gauge-fixed q_loc component basis",
            MTS / "P8_Y5_R2FR_2800_QLOC_BOUND_FILL_ROWS.csv",
        ),
        (
            "QMAP2801_6_eta",
            "c_eta_AB",
            "WEP",
            "eta_AB = c_eta_AB . q_loc + higher-order terms",
            "WEP eta-equivalent channel",
            "dimensionless",
            "MISSING_QLOC_TO_ETA_COEFFICIENT",
            "species-response derivative and source/test-body split",
            MTS / "P8_Y5_R2FR_2800_QLOC_BOUND_FILL_ROWS.csv",
        ),
        (
            "QMAP2801_7_Gdot",
            "c_Gdot",
            "time/orbital",
            "d ln G_eff/dt = c_Gdot . q_loc^0 + higher-order terms",
            "Gdot_over_G; GMdot_over_GM",
            "yr^-1",
            "MISSING_TIME_COMPONENT_AND_UNITS",
            "time projection, stationarity theorem, and conversion from model time to yr^-1",
            MTS / "P8_Y5_R2FR_2800_QLOC_BOUND_FILL_ROWS.csv",
        ),
    ]
    return [
        {
            "map_id": row[0],
            "coefficient_symbol": row[1],
            "arena": row[2],
            "map_form": row[3],
            "observable_link": row[4],
            "units_required": row[5],
            "status": row[6],
            "missing_inputs": row[7],
            "source_path": sp(row[8]),
            "map_numeric": False,
            "claim_allowed": False,
            "valid_for_claim": False,
            "generated_utc": utc_now(),
        }
        for row in rows
    ]


def build_requirement_rows() -> list[dict[str, Any]]:
    rows = [
        ("REQ2801_0_q_loc_units", "q_loc norm and component units", "declare whether q_loc is dimensionless, inverse length, force density, or stress-divergence projection", "MISSING_QLOC_UNIT_CONVENTION", "blocks every numeric map"),
        ("REQ2801_1_linearized_solution", "weak-field metric response", "solve or source linearized equations linking q_loc/Delta_K to h_mu_nu", "MISSING_WEAK_FIELD_GREEN_FUNCTION", "blocks PPN"),
        ("REQ2801_2_matter_readout", "matter/test-body readout", "derive species-blind or species-indexed response coefficients", "MISSING_TEST_BODY_RESPONSE", "blocks WEP and clocks"),
        ("REQ2801_3_source_owner", "source-normalization owner", "prove same parent charge sources Poisson/Gauss/orbit/clocks without measured-G absorption", "MISSING_Y5_OWNER", "blocks orbital/source rows"),
        ("REQ2801_4_bounds", "official arena bounds", "attach source-backed bound values after observable maps exist", "WAITING_ON_MAPS", "bound values alone are not enough"),
        ("REQ2801_5_no_cancellation", "no fitted cancellation", "score each residual channel without hiding one in measured G or cancelling unrelated terms", "POLICY_INSTALLED_NOT_YET_SCORABLE", "prevents false local-GR pass"),
    ]
    return [
        {
            "requirement_id": row[0],
            "requirement": row[1],
            "mathematical_need": row[2],
            "current_status": row[3],
            "why_it_matters": row[4],
            "valid_for_claim": False,
            "generated_utc": utc_now(),
        }
        for row in rows
    ]


def build_numeric_bound_rows() -> list[dict[str, Any]]:
    rows = [
        (
            "NB2801_0_compact_shell_proxy",
            "max |P_loc d_rel J_rel| or equivalent q_loc leakage",
            "7.432631961576971e-06",
            "dimensionless_proxy",
            "P8_Y5_R2FR_2800_QLOC_BOUND_FILL_ROWS.csv",
            "numeric-looking proxy only; not an observable and not a sourced physical bound",
            "ANCHOR_PROXY_NOT_CLAIM_BOUND",
        ),
        (
            "NB2801_1_alpha3",
            "alpha3-equivalent q_loc channel",
            "MISSING_QLOC_TO_ALPHA3_COEFFICIENT",
            "dimensionless",
            "P8_Y5_R2FR_2800_QLOC_BOUND_FILL_ROWS.csv",
            "requires c_alpha3 map before official bound can score",
            "MISSING_MAP",
        ),
        (
            "NB2801_2_WEP_eta",
            "eta_AB-equivalent q_loc channel",
            "MISSING_QLOC_TO_ETA_COEFFICIENT",
            "dimensionless",
            "P8_Y5_R2FR_2800_QLOC_BOUND_FILL_ROWS.csv",
            "requires species/source/test-body map before WEP bound can score",
            "MISSING_MAP",
        ),
        (
            "NB2801_3_time_orbital",
            "d ln G_eff/dt or d ln mu_obs/dt q_loc channel",
            "MISSING_TIME_COMPONENT_AND_UNITS",
            "yr^-1",
            "P8_Y5_R2FR_2800_QLOC_BOUND_FILL_ROWS.csv",
            "requires q_loc^0 projection, stationarity, and unit conversion",
            "MISSING_TIME_MAP",
        ),
        (
            "NB2801_4_source_normalization",
            "epsilon_mu source-normalization q_loc channel",
            "MISSING_Y5_OWNER_OR_NUMERIC_COEFFICIENT",
            "dimensionless_or_operator_units",
            "P8_Y5_R10_1012_R11_SOURCE_NORMALIZATION_COEFFICIENT_VECTOR.csv",
            "requires owner theorem or coefficient vector before measured-G/Poisson/orbit rows can score",
            "MISSING_SOURCE_OWNER",
        ),
    ]
    return [
        {
            "bound_row_id": row[0],
            "quantity": row[1],
            "candidate_value": row[2],
            "candidate_units": row[3],
            "source_path": sp(MTS / row[4]),
            "interpretation": row[5],
            "status": row[6],
            "is_numeric": row[0] == "NB2801_0_compact_shell_proxy",
            "observable_bound_exists": False,
            "claim_allowed": False,
            "valid_for_claim": False,
            "generated_utc": utc_now(),
        }
        for row in rows
    ]


def build_runner_rows(maps: list[dict[str, Any]], numeric_rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for index, row in enumerate(maps):
        rows.append(
            {
                "runner_id": f"RUN2801_MAP_{index}",
                "input_id": row["map_id"],
                "input_type": "observable_map",
                "schema_ok": True,
                "numeric_value_ok": False,
                "units_ok": False,
                "source_path_exists": Path(row["source_path"]).exists(),
                "score_ready": False,
                "claim_allowed": False,
                "failure_reasons": f"{row['status']};{row['missing_inputs']}",
                "valid_for_claim": False,
                "generated_utc": utc_now(),
            }
        )
    for index, row in enumerate(numeric_rows):
        rows.append(
            {
                "runner_id": f"RUN2801_BOUND_{index}",
                "input_id": row["bound_row_id"],
                "input_type": "numeric_bound_attempt",
                "schema_ok": True,
                "numeric_value_ok": bool(row["is_numeric"]),
                "units_ok": row["candidate_units"] not in {"dimensionless_proxy", "dimensionless_or_operator_units"},
                "source_path_exists": Path(row["source_path"]).exists(),
                "score_ready": False,
                "claim_allowed": False,
                "failure_reasons": "OBSERVABLE_BOUND_MISSING;VALID_FOR_CLAIM_FALSE" if row["is_numeric"] else f"{row['status']};VALID_FOR_CLAIM_FALSE",
                "valid_for_claim": False,
                "generated_utc": utc_now(),
            }
        )
    return rows


def build_gm_residual_rows() -> list[dict[str, Any]]:
    rows = [
        ("GM2801_0_measured_G_absorption_guard", "delta_mu_absorb", "measured-G/GM calibration cannot absorb q_loc hair", "MISSING_NO_ABSORPTION_SCORE", "dimensionless", "must score residual separately"),
        ("GM2801_1_constant_G_eff", "d ln G_eff/dt", "time drift sourced by q_loc^0", "MISSING_TIME_COMPONENT_AND_UNITS", "yr^-1", "stationarity or numeric c_Gdot required"),
        ("GM2801_2_source_mass_flux", "d ln M_eff/dt", "source worldtube flux sourced by q_loc/source current", "MISSING_WORLD_TUBE_SOURCE_OWNER", "yr^-1", "source conservation theorem required"),
        ("GM2801_3_radial_source_hair", "partial_r ln mu_obs", "radial source hair from q_loc/Delta_K", "MISSING_RADIAL_PROFILE_OR_ZERO_THEOREM", "inverse_length", "radial profile or no-hair theorem required"),
        ("GM2801_4_species_source_charge", "eta_source_AB", "species-dependent source charge from q_loc matter readout", "MISSING_SPECIES_RESPONSE", "dimensionless", "selector-blind source theorem or species vector required"),
        ("GM2801_5_Poisson_orbit_owner", "delta_Poisson_orbit", "same charge must source Poisson and orbital acceleration", "MISSING_Y5_OWNER", "dimensionless", "Y5 owner theorem required"),
    ]
    return [
        {
            "gm_row_id": row[0],
            "symbol": row[1],
            "observable_link": row[2],
            "current_status": row[3],
            "units_required": row[4],
            "required_repair": row[5],
            "source_path": sp(MTS / "P8_Y5_R10_1012_CONSTANT_GM_RESIDUAL_ROWS.csv"),
            "claim_allowed": False,
            "valid_for_claim": False,
            "generated_utc": utc_now(),
        }
        for row in rows
    ]


def build_no_cancellation_rows() -> list[dict[str, Any]]:
    rows = [
        ("NC2801_0_no_measured_G_absorption", "do not hide q_loc/source-normalization hair inside fitted measured G or GM", "installed", "blocks false Newton/local-GR pass"),
        ("NC2801_1_no_cross_arena_cancellation", "do not cancel PPN residual against WEP/clock/orbital residual by fitted tuning", "installed", "keeps rows independently scoreable"),
        ("NC2801_2_absolute_values_first", "score absolute residual components before signed sums or degeneracy fits", "installed", "prevents non-physical cancellation wins"),
        ("NC2801_3_claim_requires_maps", "a numeric proxy is not evidence until q_loc-to-observable map and physical units exist", "installed", "keeps NB2801_0 nonclaim"),
    ]
    return [
        {
            "policy_id": row[0],
            "policy": row[1],
            "status": row[2],
            "reason": row[3],
            "gate_pass": True,
            "claim_allowed": False,
            "valid_for_claim": False,
            "generated_utc": utc_now(),
        }
        for row in rows
    ]


def build_gate_rows() -> list[dict[str, Any]]:
    rows = [
        ("CG2801_0_q_loc_observable_map", "q_loc observable projection maps are claim-ready", False, "K_PPN, K_WEP, K_clock, K_orbital, and K_source remain missing numeric/theorem coefficients"),
        ("CG2801_1_first_numeric_bound", "first numeric q_loc bound row is physical and source-backed", False, "7.432631961576971e-06 row is a dimensionless proxy, not an observable bound"),
        ("CG2801_2_PPN_reopen", "PPN/local-GR branch can reopen", False, "weak-field metric solution and PPN gauge normalization are missing"),
        ("CG2801_3_WEP_reopen", "WEP branch can reopen", False, "source/test-body matter response and eta coefficients are missing"),
        ("CG2801_4_source_normalization", "measured-G/source-normalization branch can reopen", False, "Y5 owner theorem or coefficient vector remains missing"),
        ("CG2801_5_no_cancellation_policy", "no-cancellation/no-absorption guardrail is installed", True, "guardrail is installed but does not create evidence"),
        ("CG2801_6_nonclaim_pack_ready", "2801 nonclaim observable-map pack is ready for next derivation target", True, "schemas, source paths, and failure modes are explicit"),
    ]
    return [
        {
            "gate_id": row[0],
            "claim": row[1],
            "gate_pass": row[2],
            "reason": row[3],
            "claim_allowed": False,
            "valid_for_claim": False,
            "generated_utc": utc_now(),
        }
        for row in rows
    ]


def build_decision_rows() -> list[dict[str, Any]]:
    rows = [
        ("DEC2801_0_map_attempt", "observable maps are specified but not filled", "we now know exactly which coefficients must exist before q_loc can face PPN/WEP/clock/orbital data", "derive one coefficient rather than widening the table again"),
        ("DEC2801_1_numeric_proxy", "the first numeric-looking row remains nonclaim", "the compact-shell value has no physical units and no observable map", "do not score local-GR/WEP from it"),
        ("DEC2801_2_best_route", "attack K_source/K_PPN first", "source-normalization and weak-field metric response are the shared bottlenecks for Newton, GR, PPN, WEP, and orbital rows", "2802 should derive a first real q_loc observable coefficient or explicitly demote the map route"),
    ]
    return [
        {
            "decision_id": row[0],
            "decision": row[1],
            "because": row[2],
            "next_action": row[3],
            "valid_for_claim": False,
            "generated_utc": utc_now(),
        }
        for row in rows
    ]


def build_next_rows() -> list[dict[str, Any]]:
    return [
        {
            "next_id": "NEXT2801_0_2802",
            "next_target": "2802-Y5-R2FR-first-real-q_loc-observable-coefficient-or-Y5-source-owner-under-AX1090.md",
            "script": "scripts/Y5_R2FR_first_real_q_loc_observable_coefficient_or_Y5_source_owner_under_AX1090_2802.py",
            "objective": "derive one real q_loc-to-observable coefficient, preferably K_source or K_PPN, or demote observable-map closure to explicit residual budget",
            "include": "linearized weak-field map; q_loc units; Poisson/Gauss/orbit/source owner; K_source; K_PPN; no measured-G absorption",
            "exclude": "proxy scoring; fitted cancellation; all-arena claim; local-GR/WEP claim; GitHub; formalization edits",
            "valid_for_claim": False,
            "generated_utc": utc_now(),
        }
    ]


def copy_branches() -> list[dict[str, Any]]:
    copy_plan = [
        (OUTPUTS["maps"], BRANCH_OUTPUTS["map_queue"], "map_queue"),
        (OUTPUTS["numeric_bound"], BRANCH_OUTPUTS["numeric_queue"], "numeric_queue"),
        (OUTPUTS["gm_residuals"], BRANCH_OUTPUTS["source_norm_queue"], "source_norm_queue"),
        (OUTPUTS["maps"], BRANCH_OUTPUTS["beta_doc"], "beta_doc"),
        (OUTPUTS["gates"], BRANCH_OUTPUTS["microscope_copy"], "microscope_copy"),
        (OUTPUTS["next"], BRANCH_OUTPUTS["next_queue"], "next_queue"),
    ]
    rows = []
    for source, destination, label in copy_plan:
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(source, destination)
        rows.append(
            {
                "copy_id": f"BC2801_{label}",
                "source": sp(source),
                "destination": sp(destination),
                "exists": destination.exists(),
                "valid_for_claim": False,
                "generated_utc": utc_now(),
            }
        )
    return rows


def formalization_untouched_since_run() -> bool:
    if not FORMALIZATION.exists():
        return True
    threshold = RUN_STARTED_UTC.timestamp()
    return not any(path.is_file() and path.stat().st_mtime >= threshold for path in FORMALIZATION.rglob("*"))


def claim_flags_true(sections: dict[str, list[dict[str, Any]]]) -> bool:
    for key, rows in sections.items():
        if key == "validation":
            continue
        for row in rows:
            if str(row.get("valid_for_claim", "false")).lower() == "true":
                return True
            if str(row.get("claim_allowed", "false")).lower() == "true":
                return True
    return False


def cited_source_paths_exist(sections: dict[str, list[dict[str, Any]]]) -> bool:
    paths: list[Path] = []
    for rows in sections.values():
        for row in rows:
            source_path = row.get("source_path")
            if source_path:
                paths.append(Path(str(source_path)))
            copy_source = row.get("source")
            if copy_source:
                paths.append(Path(str(copy_source)))
            copy_destination = row.get("destination")
            if copy_destination:
                paths.append(Path(str(copy_destination)))
    return all(path.exists() for path in paths)


def build_validation(sections: dict[str, list[dict[str, Any]]]) -> list[dict[str, Any]]:
    generated_paths = [path for key, path in OUTPUTS.items() if key != "validation"] + list(BRANCH_OUTPUTS.values())
    map_statuses = {row["status"] for row in sections["maps"]}
    checks = [
        ("VAL2801_0_sources_exist", all(row["exists"] for row in sections["sources"]), "all source-register paths exist"),
        ("VAL2801_1_sources_nonempty", all(row["contains_text"] for row in sections["sources"]), "all source-register paths contain text"),
        ("VAL2801_2_map_rows_present", {row["coefficient_symbol"] for row in sections["maps"]} >= {"K_PPN^a", "K_WEP^{AB}", "K_clock^i", "K_orbital", "K_source"}, "all required K maps are represented"),
        ("VAL2801_3_required_missing_flags_present", {"MISSING_WEAK_FIELD_METRIC_SOLUTION", "MISSING_SOURCE_TEST_BODY_PROJECTION", "MISSING_CLOCK_READOUT_MAP", "MISSING_ORBITAL_SOURCE_MODEL", "MISSING_Y5_OWNER_OR_NUMERIC_COEFFICIENT"} <= map_statuses, "major missing-map flags are explicit"),
        ("VAL2801_4_numeric_proxy_nonclaim", any(row["bound_row_id"] == "NB2801_0_compact_shell_proxy" and row["status"] == "ANCHOR_PROXY_NOT_CLAIM_BOUND" and str(row["claim_allowed"]).lower() == "false" for row in sections["numeric_bound"]), "compact-shell proxy is explicitly nonclaim"),
        ("VAL2801_5_runner_refuses_all", all(str(row["score_ready"]).lower() == "false" and str(row["claim_allowed"]).lower() == "false" for row in sections["runner"]), "runner refuses every map/bound row"),
        ("VAL2801_6_no_cancellation_installed", all(str(row["gate_pass"]).lower() == "true" and str(row["claim_allowed"]).lower() == "false" for row in sections["no_cancellation"]), "no-cancellation policies are installed but nonclaim"),
        ("VAL2801_7_source_normalization_residuals_present", len(sections["gm_residuals"]) >= 6, "source-normalization/constant-GM residual rows are staged"),
        ("VAL2801_8_claim_gates_safe", all(str(row["claim_allowed"]).lower() == "false" for row in sections["gates"]), "all claim gates keep claims blocked"),
        ("VAL2801_9_next_target_2802", any(row["next_id"] == "NEXT2801_0_2802" for row in sections["next"]), "next target is 2802"),
        ("VAL2801_10_branch_outputs_exist", all(path.exists() for path in BRANCH_OUTPUTS.values()), "branch copies were written"),
        ("VAL2801_11_outputs_exist", all(path.exists() for path in generated_paths), "all generated output paths exist"),
        ("VAL2801_12_csv_parse", all(csv_parses(path) for path in generated_paths), "all generated CSV outputs parse"),
        ("VAL2801_13_cited_source_paths_exist", cited_source_paths_exist(sections), "all cited source/copy paths in generated rows exist"),
        ("VAL2801_14_no_claim_flags", not claim_flags_true(sections), "no valid_for_claim or claim_allowed flag is true"),
        ("VAL2801_15_generated_under_post_checkpoint", all(str(path).startswith(str(WORK)) for path in generated_paths + [DOC]), "all generated artifacts remain under post-checkpoint-work"),
        ("VAL2801_16_formalization_untouched", formalization_untouched_since_run(), "formalization-workbench was not modified during this run"),
        ("VAL2801_17_pycache_absent", not (SCRIPTS / "__pycache__").exists(), "scripts __pycache__ absent before compile step"),
    ]
    rows = [{"validation_id": check_id, "passed": bool(passed), "detail": detail, "generated_utc": utc_now()} for check_id, passed, detail in checks]
    rows.append(
        {
            "validation_id": "VAL2801_OVERALL",
            "passed": all(row["passed"] for row in rows),
            "detail": "2801 specifies q_loc observable maps and first numeric-bound failure modes, refuses all claims, and selects first-real-coefficient/Y5-source-owner derivation as 2802.",
            "generated_utc": utc_now(),
        }
    )
    return rows


def markdown_table(rows: list[dict[str, Any]], columns: list[str]) -> str:
    if not rows:
        return "_No rows._"
    header = "| " + " | ".join(columns) + " |"
    separator = "| " + " | ".join("---" for _ in columns) + " |"
    body = [
        "| " + " | ".join(str(row.get(column, "")).replace("\n", " ").replace("|", "\\|") for column in columns) + " |"
        for row in rows
    ]
    return "\n".join([header, separator, *body])


def build_doc(sections: dict[str, list[dict[str, Any]]]) -> str:
    lines = [
        "# 2801 - Y5 R2FR q_loc Observable Map Or First Numeric Bound Row Under AX1090",
        "",
        "## Private Verdict",
        "",
        "2801 turns the retained `q_loc^nu = P_loc(nabla^nu Gamma_eff - nabla_mu K_hat^{mu nu})` residual into explicit observable-map contracts.",
        "",
        "The good news: the bottleneck is now sharp. The theory needs actual maps `K_PPN`, `K_WEP`, `K_clock`, `K_orbital`, and `K_source`, not another broad residual ledger.",
        "",
        "The hard news: none of those coefficients is parent-signed or numerically sourced yet. The compact-shell value `7.432631961576971e-06` is useful bookkeeping, but it is still a dimensionless proxy and cannot score PPN, WEP, clocks, or orbital/source-normalization tests.",
        "",
        "Therefore 2801 makes no local-GR, WEP, PPN, clock, orbital, or source-normalization claim. The next best move is to derive one real coefficient, preferably `K_source` or `K_PPN`, because those are the shared gates for Newton/GR recovery.",
        "",
        "## Observable Map Attempt",
        markdown_table(sections["maps"], ["map_id", "coefficient_symbol", "arena", "map_form", "status", "missing_inputs"]),
        "",
        "## Projection Requirements",
        markdown_table(sections["requirements"], ["requirement_id", "requirement", "current_status", "why_it_matters"]),
        "",
        "## First Numeric Bound Row Attempt",
        markdown_table(sections["numeric_bound"], ["bound_row_id", "quantity", "candidate_value", "candidate_units", "status", "interpretation"]),
        "",
        "## Coefficient Runner",
        markdown_table(sections["runner"], ["runner_id", "input_id", "input_type", "numeric_value_ok", "units_ok", "source_path_exists", "score_ready", "claim_allowed", "failure_reasons"]),
        "",
        "## Constant-GM / Source-Normalization Residual Rows",
        markdown_table(sections["gm_residuals"], ["gm_row_id", "symbol", "observable_link", "current_status", "units_required", "required_repair"]),
        "",
        "## No-Cancellation Policy",
        markdown_table(sections["no_cancellation"], ["policy_id", "policy", "status", "reason"]),
        "",
        "## Claim Gates",
        markdown_table(sections["gates"], ["gate_id", "claim", "gate_pass", "claim_allowed", "reason"]),
        "",
        "## Decision Ledger",
        markdown_table(sections["decision"], ["decision_id", "decision", "because", "next_action"]),
        "",
        "## Validation",
        markdown_table(sections["validation"], ["validation_id", "passed", "detail"]),
        "",
        "## Next Target",
        markdown_table(sections["next"], ["next_id", "next_target", "objective", "include", "exclude"]),
        "",
    ]
    return "\n".join(lines)


def main() -> None:
    ensure_dirs()
    if (SCRIPTS / "__pycache__").exists():
        shutil.rmtree(SCRIPTS / "__pycache__")

    sections: dict[str, list[dict[str, Any]]] = {
        "sources": build_sources(),
        "maps": build_map_rows(),
        "requirements": build_requirement_rows(),
        "numeric_bound": build_numeric_bound_rows(),
    }
    sections["runner"] = build_runner_rows(sections["maps"], sections["numeric_bound"])
    sections["gm_residuals"] = build_gm_residual_rows()
    sections["no_cancellation"] = build_no_cancellation_rows()
    sections["gates"] = build_gate_rows()
    sections["decision"] = build_decision_rows()
    sections["next"] = build_next_rows()

    for key, rows in sections.items():
        if key in OUTPUTS:
            write_csv(OUTPUTS[key], rows)
    sections["branches"] = copy_branches()
    write_csv(OUTPUTS["branches"], sections["branches"])
    sections["validation"] = build_validation(sections)
    write_csv(OUTPUTS["validation"], sections["validation"])
    DOC.write_text(build_doc(sections), encoding="utf-8")
    print(f"wrote {DOC}")
    print(f"validation overall: {sections['validation'][-1]['passed']}")


if __name__ == "__main__":
    main()

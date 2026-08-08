from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


SCRIPT_START_UTC = datetime.now(timezone.utc)

ROOT = Path(__file__).resolve().parents[1]
PROJECT = ROOT.parent
RESIDUALS = ROOT / "source-intake" / "mts_residuals"
LOCAL_BOUNDS = ROOT / "source-intake" / "local_bounds"
RAB_QUEUE = ROOT / "source-intake" / "rab-sector" / "acquisition-queue"
PARENT_ACTION = ROOT / "source-intake" / "parent-action"
FORMALIZATION = PROJECT / "formalization-workbench"

CHECKPOINT = "2933"
BRANCH_ID = "MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428"
RUN_UTC = SCRIPT_START_UTC.isoformat()

DOC = ROOT / "2933-Y5-R2FR-kappa-drift-range-source-bound-first-value-or-ellJ-owner-under-AX1090.md"

SRC_2932_DOC = ROOT / "2932-Y5-R2FR-kappa-ellJ-constant-proof-or-first-coupling-source-bound-under-AX1090.md"
SRC_2932_NEXT = RESIDUALS / "P8_Y5_R2FR_2932_NEXT_TARGET.csv"
SRC_2932_BOUND_LEDGER = RESIDUALS / "P8_Y5_R2FR_2932_COUPLING_FIRST_BOUND_ACQUISITION_LEDGER.csv"
SRC_2932_CONSTANT_AUDIT = RESIDUALS / "P8_Y5_R2FR_2932_KAPPA_ELLJ_CONSTANT_PROOF_AUDIT.csv"
SRC_2932_REENTRY = RESIDUALS / "P8_Y5_R2FR_2932_TOPOLOGICAL_KAPPA_REENTRY_AUDIT.csv"
SRC_2932_CLAIMS = RESIDUALS / "P8_Y5_R2FR_2932_CLAIM_GATES.csv"
SRC_2932_VALIDATION = RESIDUALS / "P8_Y5_BRR545_2932_VALIDATION.csv"

SRC_2931_RESIDUAL = RESIDUALS / "P8_Y5_R2FR_2931_MTS_COEFFICIENT_RESIDUAL_DECOMPOSITION.csv"
SRC_2928_COUPLING = RESIDUALS / "P8_Y5_R2FR_2928_KAPPA_ELLJ_COUPLING_BASELINE_ROWS.csv"
SRC_2578_LEDGER = RESIDUALS / "P8_Y5_PIM_HAMILTONIAN_COUPLING_2578_RESIDUAL_INPUT_LEDGER.csv"
SRC_2695_KAPPA = RESIDUALS / "P8_Y5_R2FR_2695_KAPPA_RESIDUAL_VALUE_REQUIREMENTS_NONCLAIM.csv"
SRC_KAPPA_MAP = RESIDUALS / "P8_CONSTANT_KAPPA_RESIDUAL_MAP.csv"

GENOVA_URL = "https://www.nature.com/articles/s41467-017-02558-1"
GENOVA_DOI = "10.1038/s41467-017-02558-1"
GENOVA_TITLE = "Solar system expansion and strong equivalence principle as seen by the NASA MESSENGER mission"
GENOVA_BOUND_ABS_DOTG_PER_YEAR = 4.0e-14
TARGET_2932_DOTG_PER_YEAR = 9.6e-15

OUTPUTS = {
    "sources": RESIDUALS / "P8_Y5_R2FR_2933_SOURCE_REGISTER.csv",
    "bound_source": RESIDUALS / "P8_Y5_R2FR_2933_COUPLING_BOUND_SOURCE_ACQUISITION.csv",
    "projection_gate": RESIDUALS / "P8_Y5_R2FR_2933_DOTG_KAPPA_PROJECTION_GATE.csv",
    "first_value": RESIDUALS / "P8_Y5_R2FR_2933_FIRST_VALUE_STATUS.csv",
    "claims": RESIDUALS / "P8_Y5_R2FR_2933_CLAIM_GATES.csv",
    "decision": RESIDUALS / "P8_Y5_R2FR_2933_DECISION_LEDGER.csv",
    "next": RESIDUALS / "P8_Y5_R2FR_2933_NEXT_TARGET.csv",
    "branches": RESIDUALS / "P8_Y5_R2FR_2933_BRANCH_COPIES.csv",
    "validation": RESIDUALS / "P8_Y5_BRR545_2933_VALIDATION.csv",
}

BRANCH_OUTPUTS = {
    "bound_source_copy": LOCAL_BOUNDS / "Kappa_drift_first_source_bound_2933_NONCLAIM.csv",
    "projection_gate_copy": PARENT_ACTION / "DotG_to_kappa_projection_gate_2933_NONCLAIM.csv",
    "next_copy": RAB_QUEUE / "JR2933_DOTG_TO_KAPPA_OR_ELLJ_OWNER_NEXT_NONCLAIM.csv",
}

for directory in {path.parent for path in OUTPUTS.values()} | {path.parent for path in BRANCH_OUTPUTS.values()} | {DOC.parent}:
    directory.mkdir(parents=True, exist_ok=True)


def read_text(path: Path) -> str:
    if not path.exists():
        return ""
    return path.read_text(encoding="utf-8", errors="replace")


def read_csv_rows(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def csv_parses(path: Path) -> bool:
    try:
        read_csv_rows(path)
        return True
    except Exception:
        return False


def anchors_present(path: Path, anchors: str) -> tuple[bool, str]:
    if not path.exists():
        return False, anchors
    text = read_text(path)
    missing = [anchor for anchor in anchors.split(";") if anchor and anchor not in text]
    return not missing, ";".join(missing)


def add_common(row: dict[str, Any]) -> dict[str, Any]:
    row.update(
        {
            "checkpoint": CHECKPOINT,
            "branch_id": BRANCH_ID,
            "control_only": True,
            "score_ready": False,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
            "generated_utc": RUN_UTC,
        }
    )
    return row


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    fieldnames: list[str] = []
    for row in rows:
        for key in row:
            if key not in fieldnames:
                fieldnames.append(key)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def as_bool(value: Any) -> bool:
    return str(value).strip().lower() in {"1", "true", "yes", "y"}


def is_under(path: Path, parent: Path) -> bool:
    try:
        path.resolve().relative_to(parent.resolve())
        return True
    except ValueError:
        return False


def md_escape(value: Any) -> str:
    return str(value).replace("|", "\\|").replace("\n", "<br>")


def md_table(rows: list[dict[str, Any]], columns: list[str] | None = None) -> str:
    if not rows:
        return "_No rows._"
    selected = columns or list(rows[0].keys())
    header = "| " + " | ".join(selected) + " |"
    separator = "| " + " | ".join("---" for _ in selected) + " |"
    body = ["| " + " | ".join(md_escape(row.get(column, "")) for column in selected) + " |" for row in rows]
    return "\n".join([header, separator, *body])


def source_register_rows() -> list[dict[str, Any]]:
    local_specs = [
        ("SRC2933_00_2932_doc", SRC_2932_DOC, "NEXT2932_0_2933;dln_Geff_dt;alpha_kappa(lambda);Validation overall: `True`", "2932 selected first coupling bound or ellJ owner"),
        ("SRC2933_01_2932_next", SRC_2932_NEXT, "NEXT2932_0_2933;source-backed nonclaim value/bound", "machine-readable 2933 target"),
        ("SRC2933_02_2932_bound_ledger", SRC_2932_BOUND_LEDGER, "CBL2932_0_dln_Geff_dt;CBL2932_2_alpha_kappa_lambda;CBL2932_8_total", "coupling rows needing first finite fill"),
        ("SRC2933_03_2932_constant_audit", SRC_2932_CONSTANT_AUDIT, "KLC2932_0_kappa_route;KLC2932_5_coupling_total", "kappa/ellJ constant theorem audit"),
        ("SRC2933_04_2932_reentry", SRC_2932_REENTRY, "KTR2932_0_action;KTR2932_6_verdict", "topological kappa reentry status"),
        ("SRC2933_05_2932_claims", SRC_2932_CLAIMS, "CG2932_1_kappa_claim;CG2932_2_ellJ_claim;CG2932_3_first_bound", "2932 claim ceiling"),
        ("SRC2933_06_2932_validation", SRC_2932_VALIDATION, "VAL2932_OVERALL;True", "2932 validation summary"),
        ("SRC2933_07_2931_residual", SRC_2931_RESIDUAL, "CRD2931_5_coupling;Delta_coupling_source_abs", "source coefficient residual with coupling heads"),
        ("SRC2933_08_2928_coupling", SRC_2928_COUPLING, "CB2928_0_kappa_alpha3;CB2928_1_ellJ_alpha3;CB2928_3_coupling_total", "coupling baseline rows"),
        ("SRC2933_09_2578_ledger", SRC_2578_LEDGER, "RES2578_7_delta_kappa;RES2578_8_delta_ellJ;RES2578_9_total", "PiM/Hamiltonian coupling residual ledger"),
        ("SRC2933_10_2695_kappa", SRC_2695_KAPPA, "KRR2695_0_time_drift;KRR2695_2_range_dependence;KRR2695_5_bianchi_exchange", "kappa residual value requirements"),
        ("SRC2933_11_kappa_map", SRC_KAPPA_MAP, "KR508_0_time_drift;KR508_2_range_dependence;KR508_5_Bianchi_exchange", "constant-kappa residual map"),
    ]
    rows: list[dict[str, Any]] = []
    for source_id, source_path, anchors, role in local_specs:
        found, missing = anchors_present(source_path, anchors)
        rows.append(
            add_common(
                {
                    "source_id": source_id,
                    "source_type": "local_file",
                    "source_path": str(source_path),
                    "source_url": "",
                    "source_doi": "",
                    "anchors": anchors,
                    "role": role,
                    "path_exists": source_path.exists(),
                    "anchors_found": found,
                    "missing_anchors": missing,
                }
            )
        )
    rows.append(
        add_common(
            {
                "source_id": "SRC2933_12_genova_2018_messenger",
                "source_type": "external_primary_article",
                "source_path": "",
                "source_url": GENOVA_URL,
                "source_doi": GENOVA_DOI,
                "source_title": GENOVA_TITLE,
                "source_year": 2018,
                "anchors": "Nature page lines 60-62;114;170",
                "role": "source-backed finite comparator for local time-drift of effective gravitational coupling",
                "path_exists": True,
                "anchors_found": True,
                "missing_anchors": "",
            }
        )
    )
    return rows


def bound_source_rows() -> list[dict[str, Any]]:
    ratio_to_2932 = GENOVA_BOUND_ABS_DOTG_PER_YEAR / TARGET_2932_DOTG_PER_YEAR
    rows = [
        {
            "bound_id": "BND2933_0_dotG_over_G_messenger",
            "symbol": "dln_Geff_dt",
            "candidate_mts_symbol": "D_t ln kappa_eff",
            "arena": "solar_system_orbital;Mercury;MESSENGER",
            "source_title": GENOVA_TITLE,
            "source_url": GENOVA_URL,
            "source_doi": GENOVA_DOI,
            "source_year": 2018,
            "reported_bound_abs": GENOVA_BOUND_ABS_DOTG_PER_YEAR,
            "units": "yr^-1",
            "bound_interpretation": "absolute upper comparator for |dotG/G| from Mercury/MESSENGER plus solar mass-loss modeling",
            "source_anchor": "article abstract reports |dotG|/G < 4e-14 per year; results line repeats lower than 4.0e-14 per year",
            "extraction_method": "manual_source_anchor_from_primary_article_page",
            "numeric_value_present": True,
            "source_backed": True,
            "target_2932_abs": TARGET_2932_DOTG_PER_YEAR,
            "target_2932_units": "yr^-1",
            "ratio_bound_to_2932_target": ratio_to_2932,
            "meets_2932_target": GENOVA_BOUND_ABS_DOTG_PER_YEAR <= TARGET_2932_DOTG_PER_YEAR,
            "use_in_mts": "COMPARATOR_ONLY_UNTIL_DOTG_TO_KAPPA_PROJECTION_DERIVED",
            "status": "FINITE_SOURCE_BACKED_COMPARATOR_ACQUIRED_NONCLAIM",
        },
        {
            "bound_id": "BND2933_1_alpha_kappa_lambda",
            "symbol": "alpha_kappa(lambda)",
            "candidate_mts_symbol": "finite_range_running_kappa_projection",
            "arena": "R10_fifth_force",
            "source_title": "",
            "source_url": "",
            "source_doi": "",
            "source_year": "",
            "reported_bound_abs": "",
            "units": "range_dependent",
            "bound_interpretation": "not filled in 2933; keep 2932 R10 alpha curve acquisition separate",
            "source_anchor": "",
            "extraction_method": "not_attempted_this_checkpoint",
            "numeric_value_present": False,
            "source_backed": False,
            "target_2932_abs": "",
            "target_2932_units": "",
            "ratio_bound_to_2932_target": "",
            "meets_2932_target": False,
            "use_in_mts": "BLOCKED_PENDING_REAL_ALPHA_LAMBDA_CURVE",
            "status": "OPEN",
        },
        {
            "bound_id": "BND2933_2_ellJ_owner",
            "symbol": "Dln(ell_J)",
            "candidate_mts_symbol": "source_current_scale_drift",
            "arena": "source_current;Newton;WEP;PPN",
            "source_title": "",
            "source_url": "",
            "source_doi": "",
            "source_year": "",
            "reported_bound_abs": "",
            "units": "dimensionless_or_yr^-1_after_owner_map",
            "bound_interpretation": "no source-current owner theorem found in 2933; deferred to 2934 fallback",
            "source_anchor": "",
            "extraction_method": "theorem_attempt_deferred",
            "numeric_value_present": False,
            "source_backed": False,
            "target_2932_abs": "",
            "target_2932_units": "",
            "ratio_bound_to_2932_target": "",
            "meets_2932_target": False,
            "use_in_mts": "BLOCKED_PENDING_ELLJ_OWNER_THEOREM",
            "status": "OPEN",
        },
    ]
    return [add_common(row) for row in rows]


def projection_gate_rows() -> list[dict[str, Any]]:
    rows = [
        {
            "gate_id": "PG2933_0_observed_bound",
            "clause": "finite observed comparator exists",
            "required_identity": "|dotG/G| < 4.0e-14 yr^-1",
            "status": "PASS_SOURCE_BACKED",
            "reason": "Genova et al. MESSENGER analysis gives a finite solar-system bound",
            "condition_passed": True,
            "blocks_claim": False,
        },
        {
            "gate_id": "PG2933_1_weak_field_map",
            "clause": "derive effective Newton coupling",
            "required_identity": "Poisson limit: nabla^2 Phi = 4*pi*G_eff*rho_source with G_eff=C_source*kappa_MTS*ell_J^p_J*R_frame",
            "status": "MAP_NOT_PARENT_DERIVED",
            "reason": "current corpus has not signed C_source, p_J, reference/frame and measured-GM absorption policy",
            "condition_passed": False,
            "blocks_claim": True,
        },
        {
            "gate_id": "PG2933_2_log_derivative",
            "clause": "turn dotG/G into kappa drift",
            "required_identity": "D_t ln G_eff = D_t ln kappa_MTS + p_J D_t ln ell_J + D_t ln C_source + D_t ln R_frame",
            "status": "DERIVED_AS_BOOKKEEPING_IDENTITY_ONLY",
            "reason": "identity shows exactly why dotG/G cannot yet be read as D_t ln kappa_MTS alone",
            "condition_passed": True,
            "blocks_claim": True,
        },
        {
            "gate_id": "PG2933_3_solar_mass_disentanglement",
            "clause": "separate G variation from source mass/readout variation",
            "required_identity": "dot(GM_sun)/(GM_sun)=dotG/G+dotM_sun/M_sun and MTS source mass normalization has no hidden drift",
            "status": "SOURCE_MASS_NORMALIZATION_OPEN",
            "reason": "external paper performs solar mass-loss modeling, but MTS still needs its own source-current mass owner",
            "condition_passed": False,
            "blocks_claim": True,
        },
        {
            "gate_id": "PG2933_4_arena_transfer",
            "clause": "transfer Mercury/Solar-system bound to local MTS coupling residual",
            "required_identity": "same G_eff branch controls Mercury orbit, local Newtonian lab readout, clocks, R10 and alpha3 with no arena-dependent hair",
            "status": "ARENA_UNIVERSALITY_NOT_DERIVED",
            "reason": "2932 left source/frame/domain blindness unsigned",
            "condition_passed": False,
            "blocks_claim": True,
        },
        {
            "gate_id": "PG2933_5_verdict",
            "clause": "first finite coupling value",
            "required_identity": "a source-backed finite comparator exists, but no MTS prediction/pass claim is promoted",
            "status": "FIRST_COMPARATOR_FILLED_MTS_PROJECTION_BLOCKED",
            "reason": "this is progress from symbolic blocker to bounded target, not evidence that MTS satisfies it",
            "condition_passed": True,
            "blocks_claim": True,
        },
    ]
    return [add_common(row) for row in rows]


def first_value_rows(bound_rows: list[dict[str, Any]], projection_rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    source_bound_filled = any(row["bound_id"] == "BND2933_0_dotG_over_G_messenger" and as_bool(row["numeric_value_present"]) and as_bool(row["source_backed"]) for row in bound_rows)
    projection_blocked = any(as_bool(row["blocks_claim"]) and not as_bool(row["condition_passed"]) for row in projection_rows)
    ratio_to_2932 = GENOVA_BOUND_ABS_DOTG_PER_YEAR / TARGET_2932_DOTG_PER_YEAR
    rows = [
        {
            "status_id": "FVS2933_0_first_value",
            "symbol": "dln_Geff_dt",
            "value_type": "external_bound_comparator",
            "finite_value_or_bound": GENOVA_BOUND_ABS_DOTG_PER_YEAR,
            "units": "yr^-1",
            "source_backed": source_bound_filled,
            "maps_to_mts_prediction": False,
            "projection_blocked": projection_blocked,
            "target_2932": TARGET_2932_DOTG_PER_YEAR,
            "ratio_to_target": ratio_to_2932,
            "target_pass": GENOVA_BOUND_ABS_DOTG_PER_YEAR <= TARGET_2932_DOTG_PER_YEAR,
            "verdict": "FIRST_SOURCE_BACKED_COMPARATOR_FILLED_BUT_NOT_STRONG_ENOUGH_FOR_2932_TARGET_AND_NOT_PROJECTED_TO_KAPPA",
        },
        {
            "status_id": "FVS2933_1_local_GR",
            "symbol": "local_GR_recovery",
            "value_type": "claim_gate",
            "finite_value_or_bound": "",
            "units": "",
            "source_backed": source_bound_filled,
            "maps_to_mts_prediction": False,
            "projection_blocked": projection_blocked,
            "target_2932": "",
            "ratio_to_target": "",
            "target_pass": False,
            "verdict": "LOCAL_GR_STILL_BLOCKED_UNTIL_GEFF_KAPPA_ELLJ_SOURCE_MAP_DERIVED",
        },
    ]
    return [add_common(row) for row in rows]


def claim_gate_rows() -> list[dict[str, Any]]:
    specs = [
        ("CG2933_0_source_bound", "finite external |dotG/G| comparator acquired", "PASS_NONCLAIM", "source-backed bound exists with units", True),
        ("CG2933_1_kappa_claim", "D_t ln kappa_MTS is bounded by |dotG/G|", "BLOCKED_NONCLAIM", "requires G_eff(kappa,ell_J,C_source,R_frame) projection theorem", False),
        ("CG2933_2_ellJ_claim", "D_t ln ell_J=0 or bounded", "BLOCKED_NONCLAIM", "source-current scale owner remains open", False),
        ("CG2933_3_local_GR", "MTS reduces to local GR/Newton through constant coupling", "BLOCKED_NONCLAIM", "coupling baseline package still has active residuals", False),
        ("CG2933_4_r10_alpha", "alpha_kappa(lambda) curve or theorem-zero acquired", "BLOCKED_NONCLAIM", "R10 range curve not filled in this checkpoint", False),
        ("CG2933_5_verdict", "2933 promotes any empirical pass claim", "NO_PROMOTION_ALLOWED", "only comparator acquisition and projection gate are complete", False),
    ]
    return [
        add_common(
            {
                "claim_id": claim_id,
                "claim": claim,
                "status": status,
                "reason": reason,
                "condition_passed": condition_passed,
            }
        )
        for claim_id, claim, status, reason, condition_passed in specs
    ]


def decision_rows() -> list[dict[str, Any]]:
    specs = [
        ("DEC2933_0_bound", "retain MESSENGER dotG/G as first finite source-backed comparator", "it gives a real number, units and source path for the coupling drift ledger", "use it only through a projection gate", False),
        ("DEC2933_1_projection", "do not equate dotG/G with D_t ln kappa_MTS yet", "ell_J/source/current/reference/frame factors can absorb or mimic drift", "derive G_eff source map next", False),
        ("DEC2933_2_target", "2932 9.6e-15 target is stricter than the 4.0e-14 comparator", "the source bound is useful but not a pass against that internal target", "search tighter bound or derive theorem-zero after projection", False),
        ("DEC2933_3_next", "select dotG-to-kappa projection theorem or ellJ owner", "this is the non-looping bridge from data ledger to derivable local GR", "2934 should derive G_eff(kappa,ell_J) or fail explicitly", False),
    ]
    return [
        add_common(
            {
                "decision_id": decision_id,
                "decision": decision,
                "reason": reason,
                "action": action,
            }
        )
        for decision_id, decision, reason, action, _ in specs
    ]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        add_common(
            {
                "next_id": "NEXT2933_0_2934",
                "selection": "selected_primary",
                "target_doc": "2934-Y5-R2FR-dotG-to-kappa-projection-theorem-or-ellJ-owner-source-current-normalization-under-AX1090.md",
                "target_script": "scripts/Y5_R2FR_dotG_to_kappa_projection_theorem_or_ellJ_owner_source_current_normalization_under_AX1090_2934.py",
                "objective": "derive the weak-field source map G_eff=C_source*kappa_MTS*ell_J^p_J*R_frame and its log derivative, or prove the ell_J owner/source-current normalization theorem",
                "acceptance_gate": "dotG/G can be projected to a specific MTS residual head only if C_source, p_J, ell_J drift, reference/frame and source mass normalization are parent-signed or independently bounded",
                "fallback": "if projection theorem fails, emit closure row for source/current coupling and move to R10 alpha(lambda) real curve acquisition",
            }
        )
    ]


def branch_copy_rows() -> list[dict[str, Any]]:
    copy_specs = [
        ("bound_source_copy", OUTPUTS["bound_source"], BRANCH_OUTPUTS["bound_source_copy"]),
        ("projection_gate_copy", OUTPUTS["projection_gate"], BRANCH_OUTPUTS["projection_gate_copy"]),
        ("next_copy", OUTPUTS["next"], BRANCH_OUTPUTS["next_copy"]),
    ]
    rows = []
    for copy_id, source_path, destination_path in copy_specs:
        shutil.copyfile(source_path, destination_path)
        rows.append(
            add_common(
                {
                    "copy_id": copy_id,
                    "source_path": str(source_path),
                    "destination_path": str(destination_path),
                    "source_exists": source_path.exists(),
                    "destination_exists": destination_path.exists(),
                    "destination_parses": csv_parses(destination_path),
                }
            )
        )
    return rows


def validation_rows(rows_by_name: dict[str, list[dict[str, Any]]]) -> list[dict[str, Any]]:
    local_source_rows = [row for row in rows_by_name["sources"] if row["source_type"] == "local_file"]
    external_source_rows = [row for row in rows_by_name["sources"] if row["source_type"] == "external_primary_article"]
    output_paths = list(OUTPUTS.values())
    branch_paths = list(BRANCH_OUTPUTS.values())
    finite_bound_rows = [row for row in rows_by_name["bound_source"] if row["bound_id"] == "BND2933_0_dotG_over_G_messenger"]
    projection_blocks_claim = any(as_bool(row["blocks_claim"]) for row in rows_by_name["projection_gate"] if row["gate_id"] != "PG2933_0_observed_bound")
    no_claims_promoted = all(not as_bool(row.get("claim_allowed")) and not as_bool(row.get("valid_for_claim")) for rows in rows_by_name.values() for row in rows)
    no_prediction_rows = all(not as_bool(row.get("valid_prediction_row")) and not as_bool(row.get("score_ready")) for rows in rows_by_name.values() for row in rows)
    formalization_output_count = sum(1 for path in output_paths + branch_paths + [DOC] if is_under(path, FORMALIZATION))
    checks = [
        ("VAL2933_0_local_sources_exist", all(as_bool(row["path_exists"]) for row in local_source_rows), "all cited local source paths exist"),
        ("VAL2933_1_local_anchors_found", all(as_bool(row["anchors_found"]) for row in local_source_rows), "all cited local source anchors found"),
        ("VAL2933_2_external_source_recorded", len(external_source_rows) == 1 and bool(external_source_rows[0]["source_url"]) and bool(external_source_rows[0]["source_doi"]), "external source URL and DOI recorded"),
        ("VAL2933_3_finite_bound_numeric_positive", len(finite_bound_rows) == 1 and float(finite_bound_rows[0]["reported_bound_abs"]) > 0 and finite_bound_rows[0]["units"] == "yr^-1", "finite dotG/G bound is positive numeric with units"),
        ("VAL2933_4_first_value_nonclaim", as_bool(rows_by_name["first_value"][0]["source_backed"]) and not as_bool(rows_by_name["first_value"][0]["maps_to_mts_prediction"]), "first value is source-backed comparator but not an MTS prediction"),
        ("VAL2933_5_projection_blocks_claim", projection_blocks_claim, "projection gate blocks dotG/G to kappa claim"),
        ("VAL2933_6_no_claims_promoted", no_claims_promoted, "no 2933 row is promoted to valid_for_claim"),
        ("VAL2933_7_no_prediction_rows", no_prediction_rows, "no score-ready prediction rows emitted"),
        ("VAL2933_8_outputs_parse", all(csv_parses(path) for path in output_paths), "all 2933 output CSVs parse"),
        ("VAL2933_9_branch_copies_parse", all(csv_parses(path) for path in branch_paths), "all branch copies parse"),
        ("VAL2933_10_doc_exists", DOC.exists(), "2933 markdown doc exists"),
        ("VAL2933_11_next_target_selected", rows_by_name["next"][0]["target_doc"].startswith("2934-"), "2934 target selected"),
        ("VAL2933_12_outputs_under_post_checkpoint", all(is_under(path, ROOT) for path in output_paths + branch_paths + [DOC]), "all outputs remain under post-checkpoint-work"),
        ("VAL2933_13_sources_not_formalization", FORMALIZATION.exists() and not any(is_under(Path(row["source_path"]), FORMALIZATION) for row in local_source_rows), "no formalization-workbench source dependency"),
        ("VAL2933_14_no_formalization_2933_outputs", formalization_output_count == 0, "no formalization-workbench 2933 outputs"),
    ]
    rows = [
        add_common(
            {
                "validation_id": validation_id,
                "passed": passed,
                "check": check,
                "required": True,
            }
        )
        for validation_id, passed, check in checks
    ]
    overall = all(as_bool(row["passed"]) for row in rows)
    rows.append(
        add_common(
            {
                "validation_id": "VAL2933_OVERALL",
                "passed": overall,
                "check": "2933 validation overall",
                "required": True,
            }
        )
    )
    return rows


def render_doc(rows_by_name: dict[str, list[dict[str, Any]]]) -> str:
    status = "Y5_R2FR_2933_first_finite_dotG_source_bound_acquired_projection_to_kappa_blocked_2934_next"
    claim_ceiling = "dotG_source_bound_yes_MTS_kappa_projection_no_ellJ_owner_no_local_GR_no_Newton_no_beta_no_alpha3_no_R10_no_GitHub_claim"
    return "\n\n".join(
        [
            "# 2933 — Y5 R2FR: kappa drift/range source-bound first value or ellJ owner under AX1090",
            f"Status: `{status}`",
            f"Claim ceiling: `{claim_ceiling}`",
            "## Summary",
            (
                "2933 gets one real number into the coupling ledger without pretending it proves MTS: "
                f"the MESSENGER/Mercury solar-system result gives a source-backed comparator "
                f"`|dotG/G| < {GENOVA_BOUND_ABS_DOTG_PER_YEAR:.1e} yr^-1`. "
                "This fills the first finite `dln_Geff_dt` bound row, but it does **not** yet bound "
                "`D_t ln kappa_MTS` because the weak-field source map from MTS variables into measured "
                "`G_eff` is not parent-derived."
            ),
            (
                "The bookkeeping identity we now need to derive is:\n\n"
                "`D_t ln G_eff = D_t ln kappa_MTS + p_J D_t ln ell_J + D_t ln C_source + D_t ln R_frame`.\n\n"
                "Unless `p_J`, `ell_J`, source normalization, reference absorption and frame/domain policy are signed, "
                "the external `dotG/G` number stays a comparator, not a prediction pass."
            ),
            "## Source Register",
            md_table(rows_by_name["sources"], ["source_id", "source_type", "source_path", "source_url", "source_doi", "path_exists", "anchors_found", "role"]),
            "## Bound Source Acquisition",
            md_table(rows_by_name["bound_source"], ["bound_id", "symbol", "candidate_mts_symbol", "arena", "reported_bound_abs", "units", "target_2932_abs", "ratio_bound_to_2932_target", "meets_2932_target", "status", "use_in_mts"]),
            "## dotG to kappa Projection Gate",
            md_table(rows_by_name["projection_gate"], ["gate_id", "clause", "required_identity", "status", "condition_passed", "blocks_claim", "reason"]),
            "## First Value Status",
            md_table(rows_by_name["first_value"], ["status_id", "symbol", "value_type", "finite_value_or_bound", "units", "source_backed", "maps_to_mts_prediction", "projection_blocked", "target_pass", "verdict"]),
            "## Claim Gates",
            md_table(rows_by_name["claims"], ["claim_id", "claim", "status", "condition_passed", "reason"]),
            "## Decisions",
            md_table(rows_by_name["decision"], ["decision_id", "decision", "reason", "action"]),
            "## Next Target",
            md_table(rows_by_name["next"], ["next_id", "selection", "target_doc", "target_script", "objective", "acceptance_gate", "fallback"]),
            "## Branch Copies",
            md_table(rows_by_name["branches"], ["copy_id", "source_path", "destination_path", "source_exists", "destination_exists", "destination_parses"]),
            "## Validation",
            md_table(rows_by_name["validation"], ["validation_id", "passed", "check", "required"]),
            f"Validation overall: `{rows_by_name['validation'][-1]['passed']}`.",
            "## Bottom Line",
            (
                "This is a useful forward step, not a win lap. The coupling branch now has one finite external "
                "number with provenance, so the local-GR obstruction is less foggy. But the MTS-specific move is still "
                "to derive `G_eff(kappa_MTS, ell_J, C_source, R_frame)` from the parent action/source normalization. "
                "If that map closes cleanly, the bound can start biting the actual theory. If it does not close, "
                "the coupling route remains closure-only."
            ),
            "## Non-Claims",
            "- no `D_t ln kappa_MTS` bound is claimed from `dotG/G`;\n- no `D_t ln ell_J` theorem or value is claimed;\n- no local-GR/Newton/PPN/R10 pass is claimed;\n- no GitHub/public claim is made.",
        ]
    ) + "\n"


def main() -> None:
    rows_by_name: dict[str, list[dict[str, Any]]] = {}
    rows_by_name["sources"] = source_register_rows()
    rows_by_name["bound_source"] = bound_source_rows()
    rows_by_name["projection_gate"] = projection_gate_rows()
    rows_by_name["first_value"] = first_value_rows(rows_by_name["bound_source"], rows_by_name["projection_gate"])
    rows_by_name["claims"] = claim_gate_rows()
    rows_by_name["decision"] = decision_rows()
    rows_by_name["next"] = next_target_rows()

    for key in ["sources", "bound_source", "projection_gate", "first_value", "claims", "decision", "next"]:
        write_csv(OUTPUTS[key], rows_by_name[key])

    rows_by_name["branches"] = branch_copy_rows()
    write_csv(OUTPUTS["branches"], rows_by_name["branches"])

    DOC.write_text("# 2933 — validation pending\n", encoding="utf-8")

    rows_by_name["validation"] = validation_rows(rows_by_name)
    write_csv(OUTPUTS["validation"], rows_by_name["validation"])
    DOC.write_text(render_doc(rows_by_name), encoding="utf-8")

    print(f"wrote {DOC}")
    print(f"validation overall: {rows_by_name['validation'][-1]['passed']}")


if __name__ == "__main__":
    main()

from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "source-intake" / "mts_residuals"
LOCAL_BOUNDS = ROOT / "source-intake" / "local_bounds"
MICROSCOPE = ROOT / "source-intake" / "microscope"
BRANCH_RESIDUALS = MICROSCOPE / "branch_locked_wep" / "residuals"
FORMALIZATION = ROOT.parent / "formalization-workbench"
BRANCH_ID = "MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428"
DOC = ROOT / "1547-Y5-compact-worldtube-profile-template-and-arena-map.md"
START_TS = datetime.now(timezone.utc).timestamp()

SOURCE_FILES = {
    "1546_doc": ROOT / "1546-Y5-Tsource-worldtube-normalization-or-source-profile-acquisition.md",
    "1546_validation": OUT / "P8_Y5_BRR545_1546_VALIDATION.csv",
    "1546_next": OUT / "P8_Y5_PARENT_QLOC_1546_NEXT_TARGET.csv",
    "1546_worldtube": OUT / "P8_Y5_PARENT_QLOC_1546_WORLDTUBE_REQUIREMENTS.csv",
    "1546_tsource_def": OUT / "P8_Y5_PARENT_QLOC_1546_TSOURCE_DEFINITION_CANDIDATES.csv",
    "1546_arena": OUT / "P8_Y5_PARENT_QLOC_1546_TSOURCE_ARENA_COMPATIBILITY.csv",
    "1543_arenas": OUT / "P8_Y5_PARENT_QLOC_1543_ARENA_PROJECTION_PACK.csv",
    "1544_projection": OUT / "P8_Y5_PARENT_QLOC_1544_LOCAL_PROJECTION_CONTRACT.csv",
    "source_current": OUT / "P8_source_current_Ward_universality_CONTRACT.csv",
    "source_owner": OUT / "P8_source_owner_parent_action_terms_CONTRACT.csv",
    "source_normalization_owner": OUT / "P8_Y5_SOURCE_NORMALIZATION_OWNER_THEOREM.csv",
    "source_measure_flux": OUT / "P8_SOURCE_MEASURE_MEFF_FLUX_THEOREM.csv",
    "local_bound_claims": LOCAL_BOUNDS / "local_bound_claims.csv",
    "r10_review_curve": LOCAL_BOUNDS / "R10_alpha_lambda_bound_curve_1034_REVIEW_CANDIDATE_NONCLAIM.csv",
}

SOURCE_REGISTER = OUT / "P8_Y5_PARENT_QLOC_1547_SOURCE_REGISTER.csv"
PROFILE_TEMPLATE = OUT / "P8_Y5_PARENT_QLOC_1547_COMPACT_PROFILE_TEMPLATE.csv"
SUPPORT_CONVENTIONS = OUT / "P8_Y5_PARENT_QLOC_1547_SUPPORT_DOMAIN_CONVENTIONS.csv"
ARENA_MAP = OUT / "P8_Y5_PARENT_QLOC_1547_ARENA_MAP_REQUIREMENTS.csv"
NO_RETUNING_GUARD = OUT / "P8_Y5_PARENT_QLOC_1547_NO_RETUNING_GUARD.csv"
REFUSAL_RUNNER = OUT / "P8_Y5_PARENT_QLOC_1547_PROFILE_REFUSAL_RUNNER_NONCLAIM.csv"
CLAIM_GATE = OUT / "P8_Y5_PARENT_QLOC_1547_CLAIM_GATE.csv"
DECISION = OUT / "P8_Y5_PARENT_QLOC_1547_DECISION.csv"
NEXT_TARGET = OUT / "P8_Y5_PARENT_QLOC_1547_NEXT_TARGET.csv"
VALIDATION = OUT / "P8_Y5_BRR545_1547_VALIDATION.csv"

QUARANTINE = MICROSCOPE / "quarantine" / "1547"
QUAR_PROFILE = QUARANTINE / "COMPACT_PROFILE_TEMPLATE_NONCLAIM.csv"
QUAR_SUPPORT = QUARANTINE / "SUPPORT_DOMAIN_CONVENTIONS_NONCLAIM.csv"
QUAR_ARENA = QUARANTINE / "ARENA_MAP_REQUIREMENTS_NONCLAIM.csv"
QUAR_GUARD = QUARANTINE / "NO_RETUNING_GUARD_NONCLAIM.csv"
QUAR_RUNNER = QUARANTINE / "PROFILE_REFUSAL_RUNNER_NONCLAIM.csv"
QUAR_DECISION = QUARANTINE / "DECISION_NONCLAIM.csv"
BRANCH_PROFILE = BRANCH_RESIDUALS / "compact_worldtube_profile_template_nonclaim_1547.csv"
BRANCH_SUPPORT = BRANCH_RESIDUALS / "support_domain_conventions_nonclaim_1547.csv"
BRANCH_ARENA = BRANCH_RESIDUALS / "arena_map_requirements_nonclaim_1547.csv"
BRANCH_GUARD = BRANCH_RESIDUALS / "no_retuning_guard_nonclaim_1547.csv"
BRANCH_RUNNER = BRANCH_RESIDUALS / "profile_refusal_runner_nonclaim_1547.csv"
BRANCH_DECISION = BRANCH_RESIDUALS / "profile_decision_nonclaim_1547.csv"


def flags() -> dict[str, bool]:
    return {
        "numeric_value_present": False,
        "source_backed": False,
        "score_ready": False,
        "valid_prediction_row": False,
        "valid_for_claim": False,
        "claim_allowed": False,
    }


def rel(path: Path) -> str:
    try:
        return str(path.relative_to(ROOT)).replace("\\", "/")
    except ValueError:
        return str(path)


def source_list(*keys: str) -> str:
    return "; ".join(rel(SOURCE_FILES[key]) for key in keys)


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        raise ValueError(f"no rows for {path}")
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def parse_csv(path: Path) -> bool:
    read_csv(path)
    return True


def generated_flags_false(paths: list[Path]) -> bool:
    false_values = {"", "false", "0", "no", "none", "null"}
    claim_keys = [
        "numeric_value_present",
        "source_backed",
        "score_ready",
        "valid_prediction_row",
        "valid_for_claim",
        "claim_allowed",
        "accepted_for_scoring",
        "passes_for_claim",
    ]
    for path in paths:
        for row in read_csv(path):
            for key in claim_keys:
                if key in row and str(row[key]).strip().lower() not in false_values:
                    return False
    return True


def source_register_rows() -> list[dict[str, Any]]:
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "source_id": f"SRC1547_{index}_{key}",
            "source_path": rel(path),
            "exists": path.exists(),
            "purpose": "input evidence for compact worldtube profile template and arena map",
            **flags(),
        }
        for index, (key, path) in enumerate(SOURCE_FILES.items())
    ]


def compact_profile_template_rows() -> list[dict[str, Any]]:
    profile_rows = [
        {
            "profile_id": "WTP1547_0_shared_core",
            "arena": "shared_core",
            "source_body_convention": "one compact source family W[source] used before any arena projection",
            "worldtube_symbol": "W_src",
            "source_current_symbol": "J_q := delta S_matter / delta q or same-frame tau_a^mu equivalent",
            "profile_shape_family": "to_be_sourced: smooth compact body or distributional limit with declared regulator",
            "support_domain": "compact support inside W_src plus exterior matching domain M\\W_src",
            "boundary_or_excision_convention": "boundary flux/excision convention must be declared before scoring",
            "normalization_condition": "T_source_norm := ||J_q||_{source,W_src,E*}; not orbital GM",
            "units_needed": "dual units paired with C_qm so 1/2*T_source_norm*C_qm has E* forcing units",
            "projection_symbol": "feeds Pi_R10, Pi_PPN, Pi_clock, Pi_orbital, and Pi_local through fixed theta_src",
            "forbidden_shortcut": "do not tune theta_src separately per arena",
            "current_status": "TEMPLATE_ONLY_MISSING_PARENT_PROFILE",
            "source_paths": source_list("1546_worldtube", "1546_tsource_def", "source_current", "source_owner"),
        },
        {
            "profile_id": "WTP1547_1_R10",
            "arena": "R10",
            "source_body_convention": "same W_src plus explicit source/test body material convention for inverse-square experiment",
            "worldtube_symbol": "W_R10 := projection of W_src into short-range lab geometry",
            "source_current_symbol": "J_q[W_src] carried into Pi_R10(lambda)",
            "profile_shape_family": "requires lambda-scale source/test geometry and material profile",
            "support_domain": "lab source/test bodies with lambda-dependent separation support",
            "boundary_or_excision_convention": "finite-size and shielding boundaries must be declared",
            "normalization_condition": "use shared T_source_norm; R10 may only supply Pi_R10(lambda)",
            "units_needed": "alpha(lambda) dimensionless output; lambda length units; profile units inherited from shared norm",
            "projection_symbol": "alpha_R10(lambda) <= Pi_R10(lambda; W_src)*N_pair",
            "forbidden_shortcut": "do not replace W_src or T_source_norm with fitted alpha(lambda)",
            "current_status": "MISSING_R10_PROFILE_MAP",
            "source_paths": source_list("1543_arenas", "1546_arena", "local_bound_claims", "r10_review_curve"),
        },
        {
            "profile_id": "WTP1547_2_PPN",
            "arena": "PPN",
            "source_body_convention": "same W_src mapped to weak-field stress/current moments",
            "worldtube_symbol": "W_PPN := weak-field exterior of W_src",
            "source_current_symbol": "J_q[W_src] and T^{mu nu}[e_obs, psi] moments",
            "profile_shape_family": "requires mass/current/stress multipole map and gauge convention",
            "support_domain": "near-zone source plus asymptotic PPN matching region",
            "boundary_or_excision_convention": "matching surface and gauge-fixing convention must be declared",
            "normalization_condition": "same T_source_norm; PPN response matrix cannot redefine source strength",
            "units_needed": "dimensionless PPN residual vector after projection",
            "projection_symbol": "Delta_PPN <= Pi_PPN[W_src,gauge]*N_lock",
            "forbidden_shortcut": "do not absorb residual into gamma, beta, or preferred-frame fit by retuning source norm",
            "current_status": "MISSING_PPN_PROFILE_MAP",
            "source_paths": source_list("1543_arenas", "1544_projection", "1546_arena", "local_bound_claims"),
        },
        {
            "profile_id": "WTP1547_3_clock",
            "arena": "clock",
            "source_body_convention": "same W_src plus explicit clock/readout sensitivity convention",
            "worldtube_symbol": "W_clock := W_src seen by local redshift/frequency readout",
            "source_current_symbol": "J_q[W_src] with clock sensitivity split from source normalization",
            "profile_shape_family": "requires source-to-clock potential/readout map and constants split",
            "support_domain": "source worldtube, clock worldline, photon/signal path, and calibration interval",
            "boundary_or_excision_convention": "calibration boundary and no-shadow-clock-frame convention must be declared",
            "normalization_condition": "same T_source_norm; clock sensitivity is an arena projection coefficient",
            "units_needed": "dimensionless delta ln nu or alpha_clock residual",
            "projection_symbol": "|delta ln nu| <= Pi_clock[W_src,readout]*N_lock",
            "forbidden_shortcut": "do not hide source residual in clock calibration or constants redefinition",
            "current_status": "MISSING_CLOCK_PROFILE_MAP",
            "source_paths": source_list("1543_arenas", "1544_projection", "1546_arena", "local_bound_claims"),
        },
        {
            "profile_id": "WTP1547_4_orbital",
            "arena": "orbital",
            "source_body_convention": "same W_src compared against orbital readout after source norm is independently defined",
            "worldtube_symbol": "W_orb := compact source plus orbital exterior matching zone",
            "source_current_symbol": "J_q[W_src] with orbital response map separated from Kepler mass readout",
            "profile_shape_family": "requires source measure, flux closure, and orbital acceleration map",
            "support_domain": "source interior, orbital exterior, and matching surface",
            "boundary_or_excision_convention": "worldtube boundary and flux leakage convention must be declared",
            "normalization_condition": "same T_source_norm; orbital GM is output/comparison only",
            "units_needed": "dimensionless delta a/a or delta GM/GM after projection",
            "projection_symbol": "|delta a/a| <= Pi_orbital[W_src]*N_lock",
            "forbidden_shortcut": "do not import fitted Kepler GM as T_source_norm",
            "current_status": "MISSING_ORBITAL_PROFILE_MAP",
            "source_paths": source_list("1543_arenas", "1546_arena", "source_measure_flux", "source_normalization_owner", "local_bound_claims"),
        },
        {
            "profile_id": "WTP1547_5_local_GR",
            "arena": "local_GR",
            "source_body_convention": "same W_src must feed the local GR/Newton reduction vector",
            "worldtube_symbol": "W_local := local compact source plus GR exterior comparison region",
            "source_current_symbol": "J_q[W_src] inserted into S_cg_norm and N_lock",
            "profile_shape_family": "requires Kmetric map, PPN residual vector, and source/boundary residual accounting",
            "support_domain": "local compact source, vacuum exterior, and matching surface",
            "boundary_or_excision_convention": "boundary leakage and hidden-kernel terms must remain explicit",
            "normalization_condition": "same T_source_norm; no absorption into Newtonian mass calibration",
            "units_needed": "local residual vector units matched to Pi_local*N_lock",
            "projection_symbol": "residual_local <= Pi_local[W_src]*N_lock",
            "forbidden_shortcut": "do not claim GR limit until source profile and all finite residuals are bounded",
            "current_status": "BLOCKED_NO_CLAIM",
            "source_paths": source_list("1544_projection", "1546_worldtube", "1546_arena", "source_current"),
        },
    ]
    return [{**{"same_parent_branch_id": BRANCH_ID}, **row, **flags()} for row in profile_rows]


def support_domain_convention_rows() -> list[dict[str, Any]]:
    convention_rows = [
        ("SUP1547_0_same_frame", "same-frame convention", "all source, clock, photon, orbital, and metric readouts use the same e_obs/q_loc frame", "CONDITIONAL_NOT_PARENT_SIGNED"),
        ("SUP1547_1_compact_support", "compact support", "W_src must define interior support, exterior domain, and matching surface", "MISSING_SOURCE_PROFILE"),
        ("SUP1547_2_regularization", "regularization/excision", "point or ring limits require a regulator/excision rule before norms are finite", "MISSING_REGULATOR"),
        ("SUP1547_3_boundary_flux", "boundary flux", "flux/leakage through partial W_src must be included or proved zero", "MISSING_BOUNDARY_LEDGER"),
        ("SUP1547_4_unit_pairing", "dual norm units", "T_source_norm and C_qm units must pair into the S_cg envelope units", "MISSING_UNITS"),
        ("SUP1547_5_shared_parameters", "shared profile parameters", "theta_src may be projected differently by arenas but cannot be fitted independently per arena", "PASS_GUARD_NONCLAIM"),
        ("SUP1547_6_source_provenance", "source path provenance", "every numeric profile row must cite parent/source text, extraction method, and confidence", "MISSING_NUMERIC_PROFILE"),
    ]
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "convention_id": convention_id,
            "convention": convention,
            "requirement": requirement,
            "current_status": current_status,
            "source_paths": source_list("1546_worldtube", "1546_tsource_def", "source_measure_flux", "source_normalization_owner"),
            **flags(),
        }
        for convention_id, convention, requirement, current_status in convention_rows
    ]


def arena_map_requirement_rows() -> list[dict[str, Any]]:
    arena_rows = [
        (
            "MAP1547_0_R10",
            "R10",
            "alpha_R10(lambda) <= Pi_R10(lambda; W_src, theta_src) * [U_B_max*S_cg_norm + C_inner*|Q_m^H|]",
            "lambda; bound curve; source/test body geometry; material convention; Pi_R10 operator; shared theta_src",
            "MISSING_R10_PROFILE_MAP",
        ),
        (
            "MAP1547_1_PPN",
            "PPN",
            "Delta_PPN <= Pi_PPN(W_src, gauge, theta_src) * N_lock",
            "weak-field metric map; response matrix; gauge convention; source multipoles; shared theta_src",
            "MISSING_PPN_PROFILE_MAP",
        ),
        (
            "MAP1547_2_clock",
            "clock",
            "|delta ln nu| <= Pi_clock(W_src, readout, theta_src) * N_lock",
            "clock sensitivity matrix; constants split; calibration convention; no shadow-clock frame; shared theta_src",
            "MISSING_CLOCK_PROFILE_MAP",
        ),
        (
            "MAP1547_3_orbital",
            "orbital",
            "|delta a/a| or |delta GM/GM| <= Pi_orbital(W_src, theta_src) * N_lock",
            "source measure; flux closure; exterior matching; orbital readout map; shared theta_src",
            "MISSING_ORBITAL_PROFILE_MAP",
        ),
        (
            "MAP1547_4_local_GR",
            "local_GR",
            "residual_local <= Pi_local(W_src, theta_src) * N_lock with S_cg and boundary terms explicit",
            "Kmetric conversion; PPN residual vector; source/boundary residuals; hidden-kernel terms; shared theta_src",
            "BLOCKED_NO_CLAIM",
        ),
    ]
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "map_id": map_id,
            "arena": arena,
            "projection_contract": projection_contract,
            "required_inputs": required_inputs,
            "current_status": current_status,
            "source_paths": source_list("1543_arenas", "1544_projection", "1546_arena", "local_bound_claims"),
            **flags(),
        }
        for map_id, arena, projection_contract, required_inputs, current_status in arena_rows
    ]


def no_retuning_guard_rows() -> list[dict[str, Any]]:
    guard_rows = [
        ("NRT1547_0_shared_theta", "theta_src shared", "the compact profile parameters are selected once before arena projection", "PASS_GUARD_NONCLAIM"),
        ("NRT1547_1_projection_only", "arena projection only", "arenas may have Pi_arena operators but may not redefine T_source_norm", "PASS_GUARD_NONCLAIM"),
        ("NRT1547_2_no_orbital_GM_import", "no orbital GM import", "Kepler/ephemeris GM is a comparison output, not a source-normalization input", "PASS_GUARD_NONCLAIM"),
        ("NRT1547_3_no_bound_curve_fit", "no R10 bound-curve fit as source", "alpha(lambda) bound data cannot define the source current profile", "PASS_GUARD_NONCLAIM"),
        ("NRT1547_4_no_clock_calibration_absorption", "no clock calibration absorption", "frequency calibration cannot hide source residuals", "PASS_GUARD_NONCLAIM"),
        ("NRT1547_5_failure_policy", "failure policy", "if one arena needs a different theta_src, the shared-profile branch fails or splits into an explicit closure", "PASS_GUARD_NONCLAIM"),
    ]
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "guard_id": guard_id,
            "guard": guard,
            "statement": statement,
            "current_status": current_status,
            "source_paths": source_list("1546_worldtube", "1546_arena", "1543_arenas"),
            **flags(),
        }
        for guard_id, guard, statement, current_status in guard_rows
    ]


def refusal_runner_rows() -> list[dict[str, Any]]:
    runner_rows = [
        ("RUN1547_0_profile_numeric", "source-backed compact profile present", "REFUSED_MISSING_PROFILE", "no numeric/source-backed W_src or J_q profile has been supplied"),
        ("RUN1547_1_units", "units and dual norm declared", "REFUSED_MISSING_UNITS", "T_source_norm/C_qm dual pairing remains unscored"),
        ("RUN1547_2_support", "support/domain/excision complete", "REFUSED_MISSING_DOMAIN", "support and boundary conventions are templates only"),
        ("RUN1547_3_no_orbital_import", "orbital GM shortcut blocked", "PASS_GUARD", "orbital GM import remains rejected"),
        ("RUN1547_4_no_retuning", "per-arena retuning blocked", "PASS_GUARD", "theta_src must be shared across arena projections"),
        ("RUN1547_5_arena_maps", "arena projection maps computable", "REFUSED_MISSING_ARENA_MAPS", "Pi_R10/Pi_PPN/Pi_clock/Pi_orbital/Pi_local are not sourced"),
        ("RUN1547_6_score_status", "T_source_norm score-ready", "REFUSED_NOT_SCORE_READY", "template rows are legal scaffolding, not claim rows"),
    ]
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "runner_id": runner_id,
            "check": check,
            "current_status": current_status,
            "reason": reason,
            "accepted_for_scoring": False,
            "passes_for_claim": False,
            **flags(),
        }
        for runner_id, check, current_status, reason in runner_rows
    ]


def claim_gate_rows() -> list[dict[str, Any]]:
    gate_rows = [
        ("GATE1547_0_template", "compact profile template written", "PASS_NONCLAIM", "fillable shared W_src rows exist"),
        ("GATE1547_1_support", "support/domain conventions written", "PASS_NONCLAIM", "support, regularization, boundary, unit, and provenance needs are explicit"),
        ("GATE1547_2_no_retuning", "no per-arena retuning guard", "PASS_GUARD", "shared theta_src rule is explicit"),
        ("GATE1547_3_Tsource_score", "T_source_norm score-ready", "BLOCKED", "numeric/source-backed compact profile and units missing"),
        ("GATE1547_4_arena_scores", "R10/PPN/clock/orbital score-ready", "BLOCKED_NO_CLAIM", "arena projection maps remain missing"),
        ("GATE1547_5_local_GR", "local GR/Newton reduction claim", "BLOCKED_NO_CLAIM", "local residual vector cannot be closed from template rows"),
    ]
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "gate_id": gate_id,
            "claim": claim,
            "status": status,
            "reason": reason,
            **flags(),
        }
        for gate_id, claim, status, reason in gate_rows
    ]


def decision_rows() -> list[dict[str, Any]]:
    decision_items = [
        ("DEC1547_0_progress", "The worldtube profile branch now has a fillable shared-template contract.", "PROFILE_TEMPLATE_WRITTEN", "we can ask for one source profile instead of retuning every arena"),
        ("DEC1547_1_no_score", "Do not score T_source_norm yet.", "PROFILE_UNITS_AND_ARENA_MAPS_MISSING", "current rows are scaffolding only"),
        ("DEC1547_2_guard", "Per-arena retuning is forbidden.", "NO_RETUNING_RULE_ACTIVE", "otherwise R10, PPN, clock, and orbit would become separate patches"),
        ("DEC1547_3_next", "Next target is a shared symbolic profile runner or source-data acquisition ledger.", "NEXT_1548_SHARED_PROFILE", "try to instantiate the first shared W_src/J_q row, or record exactly why it cannot yet be sourced"),
    ]
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "decision_id": decision_id,
            "decision": decision,
            "result": result,
            "rationale": rationale,
            **flags(),
        }
        for decision_id, decision, result, rationale in decision_items
    ]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "next_id": "NEXT1547_0_1548",
            "next_target": "1548-Y5-shared-worldtube-profile-symbolic-runner-or-source-data-acquisition.md",
            "script": "scripts/Y5_shared_worldtube_profile_symbolic_runner_or_source_data_acquisition.py",
            "objective": "try to instantiate one shared symbolic compact-source profile with units/support conventions, or produce a source acquisition ledger if parent inputs are absent",
            "do_not": "do not insert numeric placeholder profiles; do not tune profile parameters per arena; do not claim R10, PPN, clock, orbital, or local-GR passes",
            **flags(),
        }
    ]


def copy_outputs() -> None:
    copies = [
        (PROFILE_TEMPLATE, QUAR_PROFILE),
        (SUPPORT_CONVENTIONS, QUAR_SUPPORT),
        (ARENA_MAP, QUAR_ARENA),
        (NO_RETUNING_GUARD, QUAR_GUARD),
        (REFUSAL_RUNNER, QUAR_RUNNER),
        (DECISION, QUAR_DECISION),
        (PROFILE_TEMPLATE, BRANCH_PROFILE),
        (SUPPORT_CONVENTIONS, BRANCH_SUPPORT),
        (ARENA_MAP, BRANCH_ARENA),
        (NO_RETUNING_GUARD, BRANCH_GUARD),
        (REFUSAL_RUNNER, BRANCH_RUNNER),
        (DECISION, BRANCH_DECISION),
    ]
    for source, destination in copies:
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(source, destination)


def remove_pycache() -> None:
    pycache = ROOT / "scripts" / "__pycache__"
    if pycache.exists():
        shutil.rmtree(pycache)


def formalization_modified_count_since_start() -> int:
    if not FORMALIZATION.exists():
        return 0
    return sum(1 for path in FORMALIZATION.rglob("*") if path.is_file() and path.stat().st_mtime >= START_TS)


def validation_rows(generated_csvs: list[Path]) -> list[dict[str, Any]]:
    sources = read_csv(SOURCE_REGISTER)
    profiles = read_csv(PROFILE_TEMPLATE)
    support_rows = read_csv(SUPPORT_CONVENTIONS)
    arena_rows = read_csv(ARENA_MAP)
    guard_rows = read_csv(NO_RETUNING_GUARD)
    runner_rows = read_csv(REFUSAL_RUNNER)
    gate_rows = read_csv(CLAIM_GATE)
    decision_items = read_csv(DECISION)
    next_rows = read_csv(NEXT_TARGET)

    required_arenas = {"shared_core", "R10", "PPN", "clock", "orbital", "local_GR"}
    profile_arenas = {row["arena"] for row in profiles}
    checks = [
        ("VAL1547_0_sources_exist", all(row["exists"] == "True" for row in sources), "all cited 1547 source paths exist"),
        ("VAL1547_1_profile_template_arenas", required_arenas.issubset(profile_arenas), "profile template covers shared core, R10, PPN, clock, orbital, and local_GR"),
        ("VAL1547_2_support_conventions", len(support_rows) >= 7 and any(row["convention_id"] == "SUP1547_5_shared_parameters" for row in support_rows), "support/domain/unit/provenance conventions written"),
        ("VAL1547_3_arena_maps", len(arena_rows) >= 5 and all(row["current_status"] in {"MISSING_R10_PROFILE_MAP", "MISSING_PPN_PROFILE_MAP", "MISSING_CLOCK_PROFILE_MAP", "MISSING_ORBITAL_PROFILE_MAP", "BLOCKED_NO_CLAIM"} for row in arena_rows), "arena map requirements remain explicitly blocked"),
        ("VAL1547_4_no_retuning_guard", any(row["guard_id"] == "NRT1547_0_shared_theta" and row["current_status"] == "PASS_GUARD_NONCLAIM" for row in guard_rows), "shared theta/no-retuning guard active"),
        ("VAL1547_5_orbital_import_rejected", any(row["guard_id"] == "NRT1547_2_no_orbital_GM_import" and row["current_status"] == "PASS_GUARD_NONCLAIM" for row in guard_rows), "orbital GM import remains rejected"),
        ("VAL1547_6_runner_refuses_score", any(row["runner_id"] == "RUN1547_6_score_status" and row["current_status"] == "REFUSED_NOT_SCORE_READY" for row in runner_rows), "profile runner refuses scoring"),
        ("VAL1547_7_claim_gates_block", any(row["gate_id"] == "GATE1547_5_local_GR" and row["status"] == "BLOCKED_NO_CLAIM" for row in gate_rows), "local GR claim remains blocked"),
        ("VAL1547_8_decision_next", any(row["result"] == "NEXT_1548_SHARED_PROFILE" for row in decision_items), "decision selects shared profile runner/source acquisition next"),
        ("VAL1547_9_next_target", any("1548-Y5-shared-worldtube-profile" in row["next_target"] for row in next_rows), "next target is shared worldtube profile runner or source acquisition"),
        ("VAL1547_10_csv_parse", all(parse_csv(path) for path in generated_csvs), "all generated 1547 CSVs parse cleanly"),
        ("VAL1547_11_claim_flags_false", generated_flags_false(generated_csvs), "all generated prediction/claim flags remain false"),
        ("VAL1547_12_branch_copies", all(path.exists() for path in [QUAR_PROFILE, QUAR_SUPPORT, QUAR_ARENA, QUAR_GUARD, QUAR_RUNNER, QUAR_DECISION, BRANCH_PROFILE, BRANCH_SUPPORT, BRANCH_ARENA, BRANCH_GUARD, BRANCH_RUNNER, BRANCH_DECISION]), "branch/quarantine nonclaim copies written"),
        ("VAL1547_13_pycache_absent", not (ROOT / "scripts" / "__pycache__").exists(), "scripts __pycache__ absent after run"),
        ("VAL1547_14_formalization_untouched", formalization_modified_count_since_start() == 0, "formalization modified-file count since start=0"),
    ]
    overall = all(result for _, result, _ in checks)
    rows = [
        {
            "same_parent_branch_id": BRANCH_ID,
            "check_id": check_id,
            "result": "PASS" if result else "FAIL",
            "detail": detail,
        }
        for check_id, result, detail in checks
    ]
    rows.append(
        {
            "same_parent_branch_id": BRANCH_ID,
            "check_id": "VAL1547_15_overall",
            "result": "PASS" if overall else "FAIL",
            "detail": "1547 writes the compact worldtube profile template, support/domain conventions, arena map requirements, and no-retuning guard while keeping all local claims blocked"
            if overall
            else "1547 validation failed; inspect failed rows before continuing",
        }
    )
    return rows


def md_table(rows: list[dict[str, Any]], columns: list[str]) -> str:
    output = ["| " + " | ".join(columns) + " |", "| " + " | ".join("---" for _ in columns) + " |"]
    for row in rows:
        output.append(
            "| "
            + " | ".join(str(row.get(column, "")).replace("\n", " ").replace("|", "\\|") for column in columns)
            + " |"
        )
    return "\n".join(output)


def write_doc(
    sources: list[dict[str, Any]],
    profiles: list[dict[str, Any]],
    support_rows: list[dict[str, Any]],
    arena_rows: list[dict[str, Any]],
    guard_rows: list[dict[str, Any]],
    runner_rows: list[dict[str, Any]],
    gate_rows: list[dict[str, Any]],
    decision_items: list[dict[str, Any]],
    validation: list[dict[str, Any]],
    next_rows: list[dict[str, Any]],
) -> None:
    DOC.write_text(
        "\n".join(
            [
                "# 1547 - Compact Worldtube Profile Template and Arena Map",
                "",
                "## Verdict",
                "- A shared compact-source template now exists for `W_src`, `J_q`, `T_source_norm`, support/domain conventions, and arena projections.",
                "- The important guard is now explicit: arenas may have different projection operators, but they may not retune the compact profile parameters independently.",
                "- R10, PPN, clock, orbital, and local-GR rows are fillable contracts only; no numeric profile or claim row is promoted.",
                "- Orbital `GM`, R10 bound curves, clock calibration, and PPN fitted residuals remain forbidden as source-normalization inputs.",
                "- Next step is to attempt one shared symbolic profile row, or write the exact source-data acquisition ledger if the parent action cannot supply it yet.",
                "",
                "## Source Register",
                md_table(sources, ["source_id", "source_path", "exists", "purpose"]),
                "",
                "## Compact Profile Template",
                md_table(profiles, ["profile_id", "arena", "worldtube_symbol", "source_current_symbol", "normalization_condition", "projection_symbol", "current_status"]),
                "",
                "## Support and Domain Conventions",
                md_table(support_rows, ["convention_id", "convention", "requirement", "current_status"]),
                "",
                "## Arena Map Requirements",
                md_table(arena_rows, ["map_id", "arena", "projection_contract", "required_inputs", "current_status"]),
                "",
                "## No-Retuning Guard",
                md_table(guard_rows, ["guard_id", "guard", "statement", "current_status"]),
                "",
                "## Refusal Runner",
                md_table(runner_rows, ["runner_id", "check", "current_status", "reason"]),
                "",
                "## Claim Gates",
                md_table(gate_rows, ["gate_id", "claim", "status", "reason"]),
                "",
                "## Decision",
                md_table(decision_items, ["decision_id", "decision", "result", "rationale"]),
                "",
                "## Validation",
                md_table(validation, ["check_id", "result", "detail"]),
                "",
                "## Next Target",
                md_table(next_rows, ["next_id", "next_target", "script", "objective", "do_not"]),
                "",
            ]
        ),
        encoding="utf-8",
    )


def main() -> None:
    sources = source_register_rows()
    profiles = compact_profile_template_rows()
    support_rows = support_domain_convention_rows()
    arena_rows = arena_map_requirement_rows()
    guard_rows = no_retuning_guard_rows()
    runner_rows = refusal_runner_rows()
    gate_rows = claim_gate_rows()
    decision_items = decision_rows()
    next_rows = next_target_rows()

    write_csv(SOURCE_REGISTER, sources)
    write_csv(PROFILE_TEMPLATE, profiles)
    write_csv(SUPPORT_CONVENTIONS, support_rows)
    write_csv(ARENA_MAP, arena_rows)
    write_csv(NO_RETUNING_GUARD, guard_rows)
    write_csv(REFUSAL_RUNNER, runner_rows)
    write_csv(CLAIM_GATE, gate_rows)
    write_csv(DECISION, decision_items)
    write_csv(NEXT_TARGET, next_rows)
    copy_outputs()
    remove_pycache()

    generated_csvs = [
        SOURCE_REGISTER,
        PROFILE_TEMPLATE,
        SUPPORT_CONVENTIONS,
        ARENA_MAP,
        NO_RETUNING_GUARD,
        REFUSAL_RUNNER,
        CLAIM_GATE,
        DECISION,
        NEXT_TARGET,
    ]
    validation = validation_rows(generated_csvs)
    write_csv(VALIDATION, validation)
    write_doc(sources, profiles, support_rows, arena_rows, guard_rows, runner_rows, gate_rows, decision_items, validation, next_rows)


if __name__ == "__main__":
    main()

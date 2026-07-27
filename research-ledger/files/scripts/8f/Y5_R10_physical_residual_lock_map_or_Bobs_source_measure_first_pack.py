from __future__ import annotations

import csv
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


POST_CHECKPOINT = Path(__file__).resolve().parents[1]
REPO_ROOT = POST_CHECKPOINT.parent
RESIDUALS = POST_CHECKPOINT / "source-intake" / "mts_residuals"
FORMALIZATION = REPO_ROOT / "formalization-workbench"

OUTPUT_DOC = POST_CHECKPOINT / "777-Y5-R10-physical-residual-lock-map-or-Bobs-source-measure-first-pack.md"
NEXT_TARGET = "778-Y5-R10-coupling-descent-input-pack-or-physical-lock-rank-proof.md"
STATUS = "Y5_R10_777_physical_residual_lock_map_attempted_not_proved_Bobs_source_measure_first_pack_staged_nonclaim"
CLAIM_CEILING = "physical_residual_lock_map_and_Bobs_source_measure_schema_only_no_R_equals_physical_zero_proof_no_Bobs_bound_no_Newton_PPN_R10_R11_or_local_GR_claim"
FORMALIZATION_CUTOFF = datetime(2026, 5, 31, 14, 42, 0)

SOURCE_REGISTER_PATH = RESIDUALS / "P8_Y5_R10_777_SOURCE_REGISTER.csv"
LOCK_MAP_PATH = RESIDUALS / "P8_Y5_R10_777_PHYSICAL_RESIDUAL_LOCK_MAP.csv"
RANK_GATE_PATH = RESIDUALS / "P8_Y5_R10_777_LOCK_RANK_AND_NULLSPACE_GATE.csv"
BOBS_SOURCE_MEASURE_PACK_PATH = RESIDUALS / "P8_Y5_R10_777_BOBS_SOURCE_MEASURE_FIRST_PACK.csv"
DECISION_MATRIX_PATH = RESIDUALS / "P8_Y5_R10_777_DECISION_MATRIX.csv"
NONCLAIM_SUMMARY_PATH = RESIDUALS / "P8_Y5_R10_777_NONCLAIM_SUMMARY.csv"
VALIDATION_PATH = RESIDUALS / "P8_Y5_BRR545_777_VALIDATION.csv"

CANDIDATE_ARTIFACTS = [
    RESIDUALS / "P8_Y5_R10_777_PHYSICAL_RESIDUAL_LOCK_CERTIFICATE.csv",
    RESIDUALS / "P8_Y5_R10_777_LOCK_RANK_MATRIX_NUMERIC.csv",
    RESIDUALS / "P8_Y5_R10_777_BOBS_SOURCE_MEASURE_COUPLING_DESCENT_INPUT_CANDIDATE.csv",
    RESIDUALS / "P8_Y5_R10_777_BOBS_CQMU_COEFFICIENT_INPUT_CANDIDATE.csv",
    RESIDUALS / "P8_Y5_R10_777_BOBS_SOURCE_FLUX_VALUE_INPUT_CANDIDATE.csv",
    RESIDUALS / "P8_Y5_R10_777_BOBS_EM_CLOCK_ORBIT_READOUT_INPUT_CANDIDATE.csv",
    RESIDUALS / "P8_Y5_R10_777_BOBS_TOTAL_SOURCE_MEASURE_CLAIM.csv",
    RESIDUALS / "P8_Y5_R10_777_LOCAL_GR_REENTRY_CANDIDATE.csv",
]

OUTPUT_PATHS = [
    OUTPUT_DOC,
    SOURCE_REGISTER_PATH,
    LOCK_MAP_PATH,
    RANK_GATE_PATH,
    BOBS_SOURCE_MEASURE_PACK_PATH,
    DECISION_MATRIX_PATH,
    NONCLAIM_SUMMARY_PATH,
    VALIDATION_PATH,
]

SOURCES: dict[str, dict[str, Any]] = {
    "776_doc": {
        "path": POST_CHECKPOINT / "776-Y5-R10-response-displacement-action-variation-ledger-or-Bobs-first-source-pack.md",
        "needles": ["RAV776_2_formal_double_zero", "BFP776_0_priority_source_measure"],
        "role": "immediate 777 handoff: formal double-zero plus B_obs source-measure priority",
    },
    "776_validation": {
        "path": RESIDUALS / "P8_Y5_BRR545_776_VALIDATION.csv",
        "needles": ["V776_4_formal_double_zero_recorded", "pass"],
        "role": "prior validation guard",
    },
    "776_variation": {
        "path": RESIDUALS / "P8_Y5_R10_776_RESPONSE_DISPLACEMENT_VARIATION_LEDGER.csv",
        "needles": ["RAV776_2_formal_double_zero", "RAV776_4_source_measure_coupling"],
        "role": "formal auxiliary zero and source-measure obstruction",
    },
    "776_first_source_pack": {
        "path": RESIDUALS / "P8_Y5_R10_776_BOBS_FIRST_SOURCE_PACK.csv",
        "needles": ["BFP776_0_priority_source_measure", "MISSING_COUPLING_DESCENT_OR_NUMERIC_SOURCE"],
        "role": "B_obs first source pack handoff",
    },
    "757_doc": {
        "path": POST_CHECKPOINT / "757-Y5-R10-response-doublet-physical-lock-or-real-q_loc-component-input.md",
        "needles": ["physical_lock_not_proved", "RVB757_0_q_loc_vector"],
        "role": "older physical lock warning",
    },
    "758_lock_gate": {
        "path": RESIDUALS / "P8_Y5_R10_758_FULL_RESIDUAL_VECTOR_LOCK_GATE.csv",
        "needles": ["FLG758_0_q_loc", "FLG758_5_coupling"],
        "role": "full residual-vector lock gates",
    },
    "759_coupling_audit": {
        "path": RESIDUALS / "P8_Y5_R10_759_COUPLING_OWNER_ACTION_AUDIT.csv",
        "needles": ["COA759_0_single_observed_geometry", "COA759_6_verdict"],
        "role": "coupling-owner audit that keeps source/readout descent unsigned",
    },
    "759_coupling_runner": {
        "path": RESIDUALS / "P8_Y5_R10_759_COUPLING_RESIDUAL_ACQUISITION_RUNNER.csv",
        "needles": ["CAR759_0_coupling_descent_input", "CAR759_5_PPN_coupling_response"],
        "role": "source/readout/coupling acquisition schemas",
    },
}


def utc_stamp() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def read_csv_rows(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def text_contains(path: Path, needles: list[str]) -> bool:
    if not path.exists():
        return False
    text = path.read_text(encoding="utf-8", errors="replace")
    return all(needle in text for needle in needles)


def write_csv(path: Path, rows: list[dict[str, Any]], fieldnames: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, extrasaction="ignore", lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def bool_string(value: bool) -> str:
    return "true" if value else "false"


def markdown_cell(value: Any) -> str:
    return str(value).replace("|", "\\|").replace("\n", "<br>")


def markdown_table(rows: list[dict[str, Any]], columns: list[str]) -> str:
    if not rows:
        return "_No rows._"
    header = "| " + " | ".join(columns) + " |"
    divider = "| " + " | ".join("---" for _ in columns) + " |"
    body = ["| " + " | ".join(markdown_cell(row.get(column, "")) for column in columns) + " |" for row in rows]
    return "\n".join([header, divider, *body])


def under_post_checkpoint(path: Path) -> bool:
    try:
        path.resolve().relative_to(POST_CHECKPOINT.resolve())
        return True
    except ValueError:
        return False


def formalization_changed_after_cutoff() -> int:
    if not FORMALIZATION.exists():
        return -1
    changed_count = 0
    for scanned_path in FORMALIZATION.rglob("*"):
        if scanned_path.is_file() and datetime.fromtimestamp(scanned_path.stat().st_mtime) > FORMALIZATION_CUTOFF:
            changed_count += 1
    return changed_count


def validation_clean(number: int) -> bool:
    path = RESIDUALS / f"P8_Y5_BRR545_{number}_VALIDATION.csv"
    rows = read_csv_rows(path)
    return path.exists() and bool(rows) and all(row.get("result") == "pass" for row in rows)


def make_source_register(generated_utc: str) -> list[dict[str, Any]]:
    return [
        {
            "source_id": source_id,
            "path": str(source_spec["path"]),
            "exists": bool_string(Path(source_spec["path"]).exists()),
            "needle_check": bool_string(text_contains(Path(source_spec["path"]), source_spec["needles"])),
            "role": source_spec["role"],
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        }
        for source_id, source_spec in SOURCES.items()
    ]


def lock_map_rows(generated_utc: str) -> list[dict[str, Any]]:
    return [
        {
            "lock_id": "PRL777_0_q_loc_vector",
            "physical_channel": "q_loc vector",
            "physical_residual": "q_loc^nu/q_* = P_loc(nabla^nu Gamma_eff - nabla_mu K_hat^{mu nu})/q_*",
            "required_lock": "R^A must map full-rank onto all observed q_loc^nu components in the local frame",
            "current_status": "not_closed",
            "blocker": "MISSING_GAMMA_EFF_KHAT_PLOC_OWNER_AND_COMPONENT_DATA",
            "test_arena": "alpha3, PPN, local force/R10, compact-orbit residuals",
            "next_input": "theorem-zero q_loc or sourced q_loc component profile",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "lock_id": "PRL777_1_Y5_source_normalization",
            "physical_channel": "Y5 measured-GM/source normalization",
            "physical_residual": "epsilon_mu = Delta(GM)_measured/(GM)_GR or equivalent source-current residual",
            "required_lock": "source current, Pi_M/Gauss normalization, and orbital readout must descend from the same parent variables",
            "current_status": "not_closed",
            "blocker": "MISSING_SOURCE_CURRENT_CLOSURE_AND_GAUSS_ORBITAL_CALIBRATION",
            "test_arena": "Newtonian limit, local ephemerides, source-mass calibration",
            "next_input": "parent-signed Y5 source-current descent or finite epsilon_mu bound",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "lock_id": "PRL777_2_Y6_extra_stress",
            "physical_channel": "Y6 extra stress/local exterior metric",
            "physical_residual": "DeltaT_extra/T_* and induced weak-field metric response",
            "required_lock": "non-EH stress must be topological/improvement-invisible or coercively included in R_phys",
            "current_status": "not_closed",
            "blocker": "EXCHANGE_EVEN_CONSERVED_STRESS_CAN_LIVE_IN_QLOC_KERNEL",
            "test_arena": "GR exterior recovery, beta/gamma, compact-orbit residuals",
            "next_input": "stress decomposition plus metric response matrix",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "lock_id": "PRL777_3_PPN_vector",
            "physical_channel": "full PPN residual vector",
            "physical_residual": "Delta{gamma,beta,alpha_i,xi,zeta_i,Gdot,R11}",
            "required_lock": "linear weak-field response W^I_A = partial PPN^I/partial R^A must be sourced and full-rank or theorem-zero",
            "current_status": "not_closed",
            "blocker": "MISSING_PPN_RESPONSE_OPERATOR_AND_GAUGE_FRAME_CERTIFICATE",
            "test_arena": "PPN, clocks, orbits, light propagation, R11",
            "next_input": "PPN response matrix W^I_A with source conditions",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "lock_id": "PRL777_4_boundary_harmonic_flux",
            "physical_channel": "boundary/harmonic flux",
            "physical_residual": "B_obs_boundary/M_H plus Hodge and projector leakage",
            "required_lock": "boundary and Hodge pieces must be inside the residual norm or killed by compact no-flux theorem",
            "current_status": "not_closed",
            "blocker": "MISSING_HODGE_FLUX_BOUNDARY_OPERATOR_AND_PROJECTOR_DESCENT",
            "test_arena": "compact-local vacuum, local action variation, domain transitions",
            "next_input": "boundary operator/no-flux theorem or sourced B_obs component rows",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "lock_id": "PRL777_5_coupling_source_measure",
            "physical_channel": "matter/source/readout coupling",
            "physical_residual": "DeltaCoupling_A and B_obs_source_measure/M_H",
            "required_lock": "matter, clocks, photons, source charge, orbit readout, and EM interface must descend from one observed geometry/source structure",
            "current_status": "partial_only_not_closed",
            "blocker": "MISSING_QUOTIENT_MATTER_SOURCE_READOUT_DESCENT",
            "test_arena": "WEP, clocks, EM/charge, source normalization, orbit readout, PPN coupling",
            "next_input": "coupling descent input pack or finite source-measure coefficient bounds",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "lock_id": "PRL777_6_verdict",
            "physical_channel": "physical residual lock certificate",
            "physical_residual": "R_phys = {q_loc^nu/q_*, epsilon_mu, DeltaT_extra/T_*, DeltaPPN_I, B_obs/M_H, DeltaCoupling_A}",
            "required_lock": "there must exist a parent-signed full-rank map L^I_A from auxiliary R^A to every observed residual channel with no silent nullspace",
            "current_status": "physical_lock_not_proved",
            "blocker": "FORMAL_R_EQUALS_ZERO_NOT_EQUIVALENT_TO_OBSERVED_RESIDUAL_ZERO",
            "test_arena": "all local-GR recovery gates",
            "next_input": NEXT_TARGET,
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
    ]


def rank_gate_rows(generated_utc: str) -> list[dict[str, Any]]:
    return [
        {
            "rank_gate_id": "RNG777_0_full_rank_required",
            "criterion": "Define L^I_A := partial R_phys^I / partial R^A around the local-GR background and require rank(L)=dim(R_phys) after gauge quotient.",
            "current_status": "not_satisfied",
            "failure_mode": "No sourced L^I_A exists for q_loc/Y5/Y6/PPN/boundary/coupling channels.",
            "claim_effect": "formal double-zero cannot be promoted",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "rank_gate_id": "RNG777_1_q_loc_kernel_risk",
            "criterion": "ker(L_q_loc) must not contain Y5/Y6/PPN/coupling directions that change observed local physics.",
            "current_status": "open_kernel_risk",
            "failure_mode": "q_loc-only lock can miss exchange-even stress, measured-GM shifts, and coupling/readout leakage.",
            "claim_effect": "q_loc zero alone is not local-GR recovery",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "rank_gate_id": "RNG777_2_source_measure_priority",
            "criterion": "B_obs_source_measure must be theorem-zero or bounded before measured-GM/orbit/clock/EM readouts can be trusted.",
            "current_status": "highest_priority_input",
            "failure_mode": "source/readout leakage can mimic a geometry failure or hide a geometry success.",
            "claim_effect": "stage B_obs source-measure first pack",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "rank_gate_id": "RNG777_3_formal_double_zero_limit",
            "criterion": "gamma_R = 1/2 R^A G_AB R^B gives partial gamma_R|R=0=0 only for the auxiliary coordinates it actually owns.",
            "current_status": "formal_only",
            "failure_mode": "No proof that auxiliary R^A spans physical residual vector R_phys^I.",
            "claim_effect": "retain mechanism but not as physical proof",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
    ]


def bobs_source_measure_rows(generated_utc: str) -> list[dict[str, Any]]:
    return [
        {
            "pack_id": "BSM777_0_coupling_descent_input",
            "target_quantity": "coupling/source/readout descent certificate",
            "candidate_artifact": str(RESIDUALS / "P8_Y5_R10_777_BOBS_SOURCE_MEASURE_COUPLING_DESCENT_INPUT_CANDIDATE.csv"),
            "required_columns": "system_id;source_channel;matter_action_owner;uses_e_obs;uses_q_parent;hidden_frame_map;coupling_descent_status;source_path;valid_for_claim",
            "why_needed": "without quotient matter/source/readout descent, source-measure flux cannot be set to zero",
            "current_status": "MISSING_COUPLING_DESCENT_INPUT",
            "claim_gate": "all sectors use the same parent-owned observed geometry with no hidden representative map",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "pack_id": "BSM777_1_Cqmu_coefficient_input",
            "target_quantity": "C_qmu coefficient for q_loc/source-measure leakage",
            "candidate_artifact": str(RESIDUALS / "P8_Y5_R10_777_BOBS_CQMU_COEFFICIENT_INPUT_CANDIDATE.csv"),
            "required_columns": "system_id;source_channel;C_qmu;units;q_loc_component;M_H_ref;normalization;source_path;valid_for_claim",
            "why_needed": "finite coupling coefficient is required before B_obs_source_measure/M_H can be bounded",
            "current_status": "MISSING_NUMERIC_CQMU_OR_THEOREM_ZERO",
            "claim_gate": "C_qmu numeric with units/source path or parent theorem C_qmu=0",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "pack_id": "BSM777_2_source_flux_value_input",
            "target_quantity": "source-measure flux value",
            "candidate_artifact": str(RESIDUALS / "P8_Y5_R10_777_BOBS_SOURCE_FLUX_VALUE_INPUT_CANDIDATE.csv"),
            "required_columns": "system_id;annulus_or_surface;flux_value;M_H_ref;units;source_path;assumptions;valid_for_claim",
            "why_needed": "the B_obs channel needs an actual surface/annulus flux or a no-flux theorem",
            "current_status": "MISSING_SOURCE_FLUX_VALUE",
            "claim_gate": "sourced finite value, uncertainty, units, and no-cancellation accounting",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "pack_id": "BSM777_3_EM_clock_orbit_readout_input",
            "target_quantity": "EM/clock/orbit readout coupling response",
            "candidate_artifact": str(RESIDUALS / "P8_Y5_R10_777_BOBS_EM_CLOCK_ORBIT_READOUT_INPUT_CANDIDATE.csv"),
            "required_columns": "sector;readout_functional;uses_e_obs;uses_hidden_map;coefficient;units;source_path;valid_for_claim",
            "why_needed": "readout leakage can produce apparent EM, clock, orbit, or source-mass effects without changing q_loc",
            "current_status": "MISSING_READOUT_RESPONSE_INPUT",
            "claim_gate": "readouts descend through e_obs and hidden maps are absent or bounded",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "pack_id": "BSM777_4_total_source_measure",
            "target_quantity": "B_obs_source_measure_over_MH total guard",
            "candidate_artifact": str(RESIDUALS / "P8_Y5_R10_777_BOBS_TOTAL_SOURCE_MEASURE_CLAIM.csv"),
            "required_columns": "component_id;value;units;source_path;zero_theorem_or_bound;no_cancellation_flag;valid_for_claim",
            "why_needed": "unknown components cannot cancel each other into a claim",
            "current_status": "MISSING_ALL_COMPONENTS_NO_CANCELLATION_TOTAL",
            "claim_gate": "all component packs valid_for_claim=true before total can be valid",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
    ]


def decision_rows(generated_utc: str) -> list[dict[str, Any]]:
    return [
        {
            "decision_id": "D777_0_formal_double_zero_retained",
            "decision": "retain response-displacement double-zero as a formal mechanism only",
            "reason": "the quadratic auxiliary action still gives F_1=0 at R=0 if no linear source term appears",
            "claim_status": "formal_only",
            "next_target": NEXT_TARGET,
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "decision_id": "D777_1_physical_lock_not_promoted",
            "decision": "do not promote R^A=0 to physical residual zero",
            "reason": "the full-rank map from R^A to q_loc/Y5/Y6/PPN/boundary/coupling residuals is not parent-signed",
            "claim_status": "blocked_for_claim",
            "next_target": NEXT_TARGET,
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "decision_id": "D777_2_source_measure_pack_staged",
            "decision": "stage B_obs source-measure first pack before claiming local-GR recovery",
            "reason": "source/readout/coupling leakage is the highest-leverage missing input after 776",
            "claim_status": "schema_only",
            "next_target": NEXT_TARGET,
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "decision_id": "D777_3_next_target",
            "decision": "either fill coupling descent input pack or prove the physical lock rank theorem",
            "reason": "that is the clean fork between evidence acquisition and a real parent-action derivation",
            "claim_status": "next_target_selected",
            "next_target": NEXT_TARGET,
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
    ]


def summary_rows(generated_utc: str) -> list[dict[str, Any]]:
    return [
        {
            "status": STATUS,
            "claim_ceiling": CLAIM_CEILING,
            "main_result": "the formal double-zero survives, but the physical residual lock map fails current-corpus proof; source-measure/coupling inputs are now the first concrete pack",
            "hard_blocker": "no parent-signed full-rank L^I_A map from auxiliary R^A to observed q_loc/Y5/Y6/PPN/boundary/coupling residuals",
            "next_target": NEXT_TARGET,
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        }
    ]


def all_generated_rows(*row_groups: list[dict[str, Any]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for group in row_groups:
        rows.extend(group)
    return rows


def validation_rows(
    sources: list[dict[str, Any]],
    lock_map: list[dict[str, Any]],
    rank_gate: list[dict[str, Any]],
    bobs_source_measure: list[dict[str, Any]],
    decisions: list[dict[str, Any]],
    summary: list[dict[str, Any]],
) -> list[dict[str, str]]:
    expected_lock_ids = {
        "PRL777_0_q_loc_vector",
        "PRL777_1_Y5_source_normalization",
        "PRL777_2_Y6_extra_stress",
        "PRL777_3_PPN_vector",
        "PRL777_4_boundary_harmonic_flux",
        "PRL777_5_coupling_source_measure",
        "PRL777_6_verdict",
    }
    expected_rank_ids = {
        "RNG777_0_full_rank_required",
        "RNG777_1_q_loc_kernel_risk",
        "RNG777_2_source_measure_priority",
        "RNG777_3_formal_double_zero_limit",
    }
    expected_bobs_ids = {
        "BSM777_0_coupling_descent_input",
        "BSM777_1_Cqmu_coefficient_input",
        "BSM777_2_source_flux_value_input",
        "BSM777_3_EM_clock_orbit_readout_input",
        "BSM777_4_total_source_measure",
    }

    source_paths_exist = all(row["exists"] == "true" for row in sources)
    source_needles_present = all(row["needle_check"] == "true" for row in sources)
    prior_665_776_clean = all(validation_clean(number) for number in range(665, 777))
    lock_map_complete = expected_lock_ids.issubset({row["lock_id"] for row in lock_map})
    lock_verdict_not_proved = any(
        row["lock_id"] == "PRL777_6_verdict" and row["current_status"] == "physical_lock_not_proved"
        for row in lock_map
    )
    rank_gate_complete = expected_rank_ids.issubset({row["rank_gate_id"] for row in rank_gate})
    source_measure_pack_complete = expected_bobs_ids.issubset({row["pack_id"] for row in bobs_source_measure})
    source_measure_pack_missing = all("MISSING" in row["current_status"] for row in bobs_source_measure)
    no_claim_rows_promoted = all(
        str(row.get("valid_for_claim", "")).lower() == "false"
        for row in all_generated_rows(sources, lock_map, rank_gate, bobs_source_measure, decisions, summary)
    )
    next_target_selected = summary[0]["next_target"] == NEXT_TARGET and any(row["decision_id"] == "D777_3_next_target" for row in decisions)
    candidate_artifacts_not_faked = all(not path.exists() for path in CANDIDATE_ARTIFACTS)
    output_scope_ok = all(under_post_checkpoint(path) for path in OUTPUT_PATHS)
    formalization_count = formalization_changed_after_cutoff()
    formalization_untouched = formalization_count == 0

    checks = [
        ("V777_0_source_paths_exist", source_paths_exist, f"source_rows={len(sources)}"),
        ("V777_1_source_needles_present", source_needles_present, "all local source needles present"),
        ("V777_2_prior_665_776_clean", prior_665_776_clean, "665-776 validation rows have no failures"),
        ("V777_3_lock_map_complete", lock_map_complete, "q_loc/Y5/Y6/PPN/boundary/coupling lock rows complete"),
        ("V777_4_lock_verdict_not_proved", lock_verdict_not_proved, "formal R=0 not promoted to physical residual zero"),
        ("V777_5_rank_gate_complete", rank_gate_complete, "rank/nullspace criteria recorded"),
        ("V777_6_Bobs_source_measure_pack_complete", source_measure_pack_complete, "B_obs source-measure first pack rows complete"),
        ("V777_7_Bobs_source_measure_missing_markers", source_measure_pack_missing, "source-measure pack rows remain MISSING_*"),
        ("V777_8_no_claim_rows_promoted", no_claim_rows_promoted, "all generated rows valid_for_claim=false"),
        ("V777_9_next_target_selected", next_target_selected, NEXT_TARGET),
        ("V777_10_candidate_artifacts_not_faked", candidate_artifacts_not_faked, "no physical-lock/source-measure/local-GR claim artifacts fabricated"),
        ("V777_11_outputs_scoped", output_scope_ok, "all outputs under post-checkpoint-work"),
        ("V777_12_formalization_workbench_untouched", formalization_untouched, f"formalization_changed_after_cutoff={formalization_count}"),
        ("V777_13_validation_rows_ready", True, "validation table constructed"),
    ]
    return [
        {"check_id": check_id, "result": "pass" if passed else "fail", "detail": detail}
        for check_id, passed, detail in checks
    ]


def build_doc(
    sources: list[dict[str, Any]],
    lock_map: list[dict[str, Any]],
    rank_gate: list[dict[str, Any]],
    bobs_source_measure: list[dict[str, Any]],
    decisions: list[dict[str, Any]],
    summary: list[dict[str, Any]],
    validation: list[dict[str, str]],
) -> None:
    text = f"""# 777 - Y5 R10 Physical Residual Lock Map Or Bobs Source-Measure First Pack

Current result: **the formal response-displacement double-zero is useful, but it still does not prove local GR**. The missing bridge is now explicit: the auxiliary zero `R^A=0` must be locked by a parent-signed, full-rank map onto the observed residual vector `R_phys = {{q_loc^nu/q_*, epsilon_mu, DeltaT_extra/T_*, DeltaPPN_I, B_obs/M_H, DeltaCoupling_A}}`. Current MTS has no such full-rank lock yet, so 777 stages the source-measure/coupling pack as the next concrete place to either derive zero or source a bound.

## Status

{markdown_table(summary, ["status", "claim_ceiling", "main_result", "hard_blocker", "next_target", "valid_for_claim"])}

## Physical Residual Lock Map

{markdown_table(lock_map, ["lock_id", "physical_channel", "physical_residual", "required_lock", "current_status", "blocker", "test_arena", "next_input", "valid_for_claim"])}

## Rank And Nullspace Gate

{markdown_table(rank_gate, ["rank_gate_id", "criterion", "current_status", "failure_mode", "claim_effect", "valid_for_claim"])}

## Bobs Source-Measure First Pack

{markdown_table(bobs_source_measure, ["pack_id", "target_quantity", "candidate_artifact", "required_columns", "why_needed", "current_status", "claim_gate", "valid_for_claim"])}

## Decision Matrix

{markdown_table(decisions, ["decision_id", "decision", "reason", "claim_status", "next_target", "valid_for_claim"])}

## Source Register

{markdown_table(sources, ["source_id", "path", "exists", "needle_check", "role", "valid_for_claim"])}

## Validation

{markdown_table(validation, ["check_id", "result", "detail"])}

## Verdict

The important thing is that this is no longer vague. The local branch is not dead, but it has a precise missing theorem: construct `L^I_A = partial R_phys^I/partial R^A`, prove it has no physical nullspace after gauge quotient, and prove source/boundary/coupling terms are silent. If that cannot be done directly, the honest route is to populate the source-measure pack and bound the leakage.

## Next Target

`{NEXT_TARGET}`
"""
    OUTPUT_DOC.write_text(text, encoding="utf-8")


def main() -> None:
    generated_utc = utc_stamp()
    sources = make_source_register(generated_utc)
    lock_map = lock_map_rows(generated_utc)
    rank_gate = rank_gate_rows(generated_utc)
    bobs_source_measure = bobs_source_measure_rows(generated_utc)
    decisions = decision_rows(generated_utc)
    summary = summary_rows(generated_utc)
    validation = validation_rows(sources, lock_map, rank_gate, bobs_source_measure, decisions, summary)

    write_csv(SOURCE_REGISTER_PATH, sources, ["source_id", "path", "exists", "needle_check", "role", "valid_for_claim", "generated_utc"])
    write_csv(LOCK_MAP_PATH, lock_map, ["lock_id", "physical_channel", "physical_residual", "required_lock", "current_status", "blocker", "test_arena", "next_input", "valid_for_claim", "generated_utc"])
    write_csv(RANK_GATE_PATH, rank_gate, ["rank_gate_id", "criterion", "current_status", "failure_mode", "claim_effect", "valid_for_claim", "generated_utc"])
    write_csv(BOBS_SOURCE_MEASURE_PACK_PATH, bobs_source_measure, ["pack_id", "target_quantity", "candidate_artifact", "required_columns", "why_needed", "current_status", "claim_gate", "valid_for_claim", "generated_utc"])
    write_csv(DECISION_MATRIX_PATH, decisions, ["decision_id", "decision", "reason", "claim_status", "next_target", "valid_for_claim", "generated_utc"])
    write_csv(NONCLAIM_SUMMARY_PATH, summary, ["status", "claim_ceiling", "main_result", "hard_blocker", "next_target", "valid_for_claim", "generated_utc"])
    write_csv(VALIDATION_PATH, validation, ["check_id", "result", "detail"])
    build_doc(sources, lock_map, rank_gate, bobs_source_measure, decisions, summary, validation)

    failures = [row for row in validation if row["result"] != "pass"]
    if failures:
        failure_text = "; ".join(f"{row['check_id']}={row['detail']}" for row in failures)
        raise SystemExit(f"777 validation failed: {failure_text}")

    print(f"wrote {OUTPUT_DOC}")
    print(f"wrote {VALIDATION_PATH}")
    print(f"status={STATUS}")
    print(f"next={NEXT_TARGET}")


if __name__ == "__main__":
    main()

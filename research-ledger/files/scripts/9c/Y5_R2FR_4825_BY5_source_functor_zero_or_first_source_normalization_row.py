from __future__ import annotations

import csv
import py_compile
import shutil
import subprocess
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(r"D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main")
POST = ROOT / "post-checkpoint-work"
FORMAL = ROOT / "formalization-workbench"
SOURCE_DIR = POST / "source-intake" / "mts_residuals"
SCRIPT_DIR = POST / "scripts"

CHECKPOINT = "4825"
CLAIM_ID = "L-667"
MARKER = "PPC4161_BY5_SOURCE_FUNCTOR_ZERO_OR_FIRST_SOURCE_NORMALIZATION_ROW_4825"
DECISION = "BY5_OWNER_ZERO_UNSIGNED_FIRST_SOURCE_NORMALIZATION_ROW_STAGED_NONCLAIM"
NEXT_TARGET = "4826-Y5-R2FR-PiM-commutator-zero-or-first-Icommutator-bound-row.md"

DOC_PATH = POST / "4825-Y5-R2FR-BY5-source-functor-zero-or-first-source-normalization-row.md"
FORMAL_PATH = FORMAL / "841-PPC4161-BY5-source-functor-zero-or-first-source-normalization-row.md"
CLAIMS_PATH = FORMAL / "02-claims-register.csv"
SPINE_PATH = FORMAL / "07-unification-spine.md"
PACKET_PATH = FORMAL / "180-PPC4161-private-local-packet-integration.md"
RESUME_PATH = POST / "CURRENT_LOCAL_RESUME.md"
RUNNER = SCRIPT_DIR / "BY5_source_functor_runner.py"

SOURCE_REGISTER = SOURCE_DIR / "P8_Y5_R2FR_4825_SOURCE_REGISTER.csv"
OWNER_AUDIT = SOURCE_DIR / "P8_Y5_R2FR_4825_BY5_OWNER_ZERO_AUDIT.csv"
VALUE_CONTRACT = SOURCE_DIR / "P8_Y5_R2FR_4825_BY5_FIRST_SOURCE_NORMALIZATION_CONTRACT.csv"
RUNNER_INPUT = SOURCE_DIR / "P8_Y5_R2FR_4825_BY5_SOURCE_FUNCTOR_RUNNER_INPUT.csv"
RUNNER_OUTPUT = SOURCE_DIR / "P8_Y5_R2FR_4825_BY5_SOURCE_FUNCTOR_RUNNER_OUTPUT.csv"
DECISION_CSV = SOURCE_DIR / "P8_Y5_R2FR_4825_DECISION_LEDGER.csv"
CLAIM_GATES = SOURCE_DIR / "P8_Y5_R2FR_4825_CLAIM_GATES.csv"
STATUS_CSV = SOURCE_DIR / "P8_Y5_R2FR_4825_STATUS.csv"
NEXT_TARGET_CSV = SOURCE_DIR / "P8_Y5_R2FR_4825_NEXT_TARGET.csv"
VALIDATION_CSV = SOURCE_DIR / "P8_Y5_BRR545_4825_VALIDATION.csv"

PATHS = {
    "resume": RESUME_PATH,
    "4824_doc": POST / "4824-Y5-R2FR-Bmem-Jmem-Qboundary-component-zero-or-first-values.md",
    "4824_audit": SOURCE_DIR / "P8_Y5_R2FR_4824_BJQ_COMPONENT_ZERO_AUDIT.csv",
    "4824_contract": SOURCE_DIR / "P8_Y5_R2FR_4824_BJQ_FIRST_VALUE_CONTRACT.csv",
    "4514_Bmem": SOURCE_DIR / "P8_Y5_R2FR_4514_BMEM_EFFECTIVE_COMPONENT_VECTOR.csv",
    "4515_theorem": SOURCE_DIR / "P8_Y5_R2FR_4515_SOURCE_FUNCTOR_DESCENT_THEOREM.csv",
    "1354_doc": POST / "1354-Y5-R10-RAB-source-functional-evenness-theorem-or-Y5Y6-JZ-coefficient-fill.md",
    "1354_evenness": SOURCE_DIR / "P8_Y5_R10_1354_SOURCE_FUNCTIONAL_EVENNESS_ATTEMPT.csv",
    "1354_fill": SOURCE_DIR / "P8_Y5_R10_1354_Y5Y6_JZ_COEFFICIENT_FILL.csv",
    "1354_reject": SOURCE_DIR / "P8_Y5_R10_1354_JZ_RUNNER_REJECTION.csv",
    "1012_doc": POST / "1012-Y5-R10-Y5-source-normalization-owner-or-q_loc-bound-implementation.md",
    "1012_coeff": SOURCE_DIR / "P8_Y5_R10_1012_R11_SOURCE_NORMALIZATION_COEFFICIENT_VECTOR.csv",
    "1013_obstruction": SOURCE_DIR / "P8_Y5_R10_1013_MEASURED_GM_OBSTRUCTION_VECTOR.csv",
    "source_stack": SOURCE_DIR / "P8_SOURCE_NORMALIZATION_THEOREM_STACK.csv",
    "r11_minimum": SOURCE_DIR / "P8_R11_SOURCE_NORMALIZATION_OPERATOR_MINIMUM_FILL.csv",
    "same_frame": SOURCE_DIR / "P8_Y5_R10_683_SAME_FRAME_GM_GATE.csv",
    "newton_contract": SOURCE_DIR / "P8_Y5_R10_868_NEWTON_SOURCE_NORMALIZATION_CONTRACT.csv",
    "current_owner": SOURCE_DIR / "P8_Y5_R10_1453_CURRENT_SOURCE_NORMALIZATION_OWNER_THEOREM_ATTEMPT.csv",
    "runner": RUNNER,
}


def now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace") if path.exists() else ""


def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fieldnames = list(dict.fromkeys(field for row in rows for field in row))
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)


def md_safe(value: Any) -> str:
    return str(value).replace("\n", " ").replace("|", "\\|")


def md_table(rows: list[dict[str, Any]], fields: list[str]) -> str:
    header = "| " + " | ".join(fields) + " |"
    sep = "| " + " | ".join("---" for _ in fields) + " |"
    body = ["| " + " | ".join(md_safe(row.get(field, "")) for field in fields) + " |" for row in rows]
    return "\n".join([header, sep, *body])


def source_specs() -> list[tuple[str, Path, str, str]]:
    return [
        ("SRC4825_00_resume", PATHS["resume"], "4825-Y5-R2FR-BY5-source-functor", "4824 selected this target."),
        ("SRC4825_01_4824_doc", PATHS["4824_doc"], "B_Y5_trace", "4824 identifies BY5 as live source-normalization tail."),
        ("SRC4825_02_4824_audit", PATHS["4824_audit"], "BJQ4824_2_BY5", "4824 BY5 audit row."),
        ("SRC4825_03_4824_contract", PATHS["4824_contract"], "BVC4824_1_Bmem", "4824 Bmem feed contract."),
        ("SRC4825_04_4514_Bmem", PATHS["4514_Bmem"], "BMV4514_2_Y5_trace", "4514 BY5 component source."),
        ("SRC4825_05_4515_theorem", PATHS["4515_theorem"], "SFT4515_2_Y5_measured_GM", "4515 source-functor zero theorem."),
        ("SRC4825_06_1354_doc", PATHS["1354_doc"], "DEC1354_1_Y5_priority", "1354 marks Y5 as highest-priority coupling target."),
        ("SRC4825_07_1354_evenness", PATHS["1354_evenness"], "SFE1354_2_Y5_measured_GM_evenness", "1354 source-functional evenness blocker."),
        ("SRC4825_08_1354_fill", PATHS["1354_fill"], "JZ1354_Y5_7_calibration_offset", "1354 eight Y5 JZ coefficient rows."),
        ("SRC4825_09_1354_reject", PATHS["1354_reject"], "RUN_JZ1354_Y5_7_calibration_offset", "1354 runner rejects unfilled Y5 rows."),
        ("SRC4825_10_1012_doc", PATHS["1012_doc"], "Y5O1012_8_verdict", "1012 Y5 owner theorem verdict."),
        ("SRC4825_11_1012_coeff", PATHS["1012_coeff"], "Y5C1012_7_absolute_calibration_offset", "1012 R11 source-normalization vector."),
        ("SRC4825_12_1013_obstruction", PATHS["1013_obstruction"], "OBS1013_1_PiM_commutator", "1013 measured-GM obstruction vector."),
        ("SRC4825_13_source_stack", PATHS["source_stack"], "S5_Newton_gate", "source-normalization theorem stack."),
        ("SRC4825_14_r11_minimum", PATHS["r11_minimum"], "R11SN_7_absolute_calibration_offset", "R11 minimum fill source rows."),
        ("SRC4825_15_same_frame", PATHS["same_frame"], "SFG683_6_final", "same-frame GM gate."),
        ("SRC4825_16_newton_contract", PATHS["newton_contract"], "NS868_1_measured_GM", "Newton source-normalization contract."),
        ("SRC4825_17_current_owner", PATHS["current_owner"], "CSO1453_7_verdict", "current/source normalization owner theorem attempt."),
        ("SRC4825_18_runner", PATHS["runner"], "def evaluate_row", "4825 executable runner."),
    ]


def build_source_register(timestamp: str) -> list[dict[str, Any]]:
    rows = []
    for source_id, path, needle, role in source_specs():
        text = read_text(path)
        rows.append(
            {
                "checkpoint": CHECKPOINT,
                "source_id": source_id,
                "source_path": str(path),
                "exists": path.exists(),
                "needle": needle,
                "needle_found": needle in text,
                "role": role,
                "valid_for_claim": False,
                "timestamp_utc": timestamp,
            }
        )
    return rows


def owner_audit(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "clause_id": "BY5Z4825_0_same_frame",
            "claim_piece": "one observed coframe/source frame",
            "needed_for_zero": "matter current, rods/clocks, source mass, and orbit readout use the same e_obs before fitting",
            "current_result": "CONDITIONAL_NOT_PARENT_SIGNED",
            "finite_fallback": "epsilon_frame/source split row",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "clause_id": "BY5Z4825_1_constant_universal_coupling",
            "claim_piece": "G_eff/kappa constant and universal",
            "needed_for_zero": "no time/range/species/frame dependence in the source normalization",
            "current_result": "NOT_PARENT_DERIVED",
            "finite_fallback": "Gdot/range/species residual rows",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "clause_id": "BY5Z4825_2_PiM_parent_origin",
            "claim_piece": "Pi_M fixed before readout",
            "needed_for_zero": "Pi_M is a parent-owned charge projection, not a post-fit measured-GM mask",
            "current_result": "NOT_PARENT_DERIVED",
            "finite_fallback": "Pi_M commutator/variation obstruction",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "clause_id": "BY5Z4825_3_flux_closure",
            "claim_piece": "d(Pi_M J_H)=0 compact-exterior closure",
            "needed_for_zero": "-Pi_M dJ_extra + [d,Pi_M]J_H + A_parent vanishes or is bounded",
            "current_result": "EXACT_OBSTRUCTION_NOT_ZERO",
            "finite_fallback": "I_commutator and obstruction score rows",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "clause_id": "BY5Z4825_4_worldtube_glue",
            "claim_piece": "worldtube source measure equals exterior charge",
            "needed_for_zero": "M_source[W] = exterior parent charge before orbital fitting",
            "current_result": "CORE_MISSING",
            "finite_fallback": "worldtube M_eff residual",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "clause_id": "BY5Z4825_5_no_extra_mu_channels",
            "claim_piece": "mu_extra channels zero or bounded",
            "needed_for_zero": "boundary, bulk, domain, projector, memory, non-EH, species, time, calibration channels vanish or are scored",
            "current_result": "RETAINED_DEBT",
            "finite_fallback": "eight epsilon_Y5 rows",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "clause_id": "BY5Z4825_6_no_absorption",
            "claim_piece": "measured G cannot hide derivative hair",
            "needed_for_zero": "only common universal range/time/species/frame independent factors are calibration",
            "current_result": "GUARD_WRITTEN_NOT_SATISFIED",
            "finite_fallback": "derivative/source-normalization residual rows",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "clause_id": "BY5Z4825_7_Newton_Poisson_orbit",
            "claim_piece": "same charge sources Poisson and orbit acceleration",
            "needed_for_zero": "Gauss/Poisson/inverse-square source uses the same parent charge",
            "current_result": "CONDITIONAL_NOT_PARENT_DERIVED",
            "finite_fallback": "Newton source-normalization residual",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
    ]


def value_contract(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "contract_id": "BYS4825_0_zero",
            "quantity": "BY5_abs=0",
            "formula": "all BY5 owner clauses sign in the same branch",
            "required_inputs": "same frame, constant universal coupling, Pi_M origin, flux closure, worldtube glue, no extra channels, no absorption, Newton/Poisson/orbit",
            "status": "conditional_only",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "contract_id": "BYS4825_1_eight_channel_sum",
            "quantity": "BY5_abs",
            "formula": "sum |epsilon_radial|+|epsilon_boundary|+|epsilon_domain|+|epsilon_bulk|+|epsilon_nonEH|+|epsilon_species|+|epsilon_time|+|epsilon_calibration|",
            "required_inputs": "eight sourced epsilon rows or zero certificates",
            "status": "runner_ready_values_missing",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "contract_id": "BYS4825_2_Bmem_feed",
            "quantity": "B_mem_eff_abs",
            "formula": "BY5_abs plus B826, BWeyl, BY6, Bsrc_boundary, Bsrc_readout",
            "required_inputs": "BYS4825_1 and non-BY5 B component values",
            "status": "feed_ready_values_missing",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
    ]


def numeric_by5(row_id: str, route_type: str, timestamp: str) -> dict[str, Any]:
    return {
        "row_id": row_id,
        "route_type": route_type,
        "route": "BY5 eight-channel arithmetic smoke",
        "source_path": str(PATHS["1012_coeff"]),
        "source_signed": True,
        "units_signed": True,
        "same_branch_signed": True,
        "no_cancellation_guard": True,
        "epsilon_radial_Meff_abs": 0.01,
        "epsilon_boundary_abs": 0.02,
        "epsilon_domain_projector_abs": 0.03,
        "epsilon_bulk_X_abs": 0.04,
        "epsilon_nonEH_source_abs": 0.05,
        "epsilon_species_A_abs": 0.06,
        "epsilon_time_drift_abs": 0.07,
        "epsilon_calibration_abs": 0.08,
        "timestamp_utc": timestamp,
    }


def runner_input(timestamp: str) -> list[dict[str, Any]]:
    zero_base = {
        "route_type": "owner_zero",
        "source_path": str(PATHS["4515_theorem"]),
        "source_signed": True,
        "units_signed": True,
        "same_branch_signed": False,
        "parent_object_language_signed": False,
        "no_cancellation_guard": False,
        "same_frame_signed": False,
        "constant_universal_coupling_signed": False,
        "PiM_parent_origin_signed": False,
        "flux_closure_signed": False,
        "worldtube_glue_signed": False,
        "no_extra_mu_channels_signed": False,
        "no_absorption_guard_signed": False,
        "Newton_Poisson_orbit_signed": False,
        "source_functor_qbasic_signed": False,
    }
    missing_bound = {
        "route_type": "by5_bound",
        "source_path": str(PATHS["1012_coeff"]),
        "source_signed": False,
        "units_signed": False,
        "same_branch_signed": False,
        "no_cancellation_guard": False,
        "epsilon_radial_Meff_abs": "MISSING_RADIAL_NOHAIR_THEOREM_OR_NUMERIC_PROFILE",
        "epsilon_boundary_abs": "MISSING_BOUNDARY_NOHAIR_THEOREM_OR_NUMERIC_COEFFICIENT",
        "epsilon_domain_projector_abs": "MISSING_DOMAIN_PROJECTOR_ZERO_THEOREM_OR_NUMERIC_PRODUCTS",
        "epsilon_bulk_X_abs": "MISSING_BULK_MASS_GAP_THEOREM_OR_ALPHA_LAMBDA_CURVE",
        "epsilon_nonEH_source_abs": "MISSING_EH_ONLY_THEOREM_OR_NONEH_OPERATOR_COEFFICIENT_MAP",
        "epsilon_species_A_abs": "MISSING_SELECTOR_BLIND_SOURCE_THEOREM_OR_SPECIES_CHARGE_VECTOR",
        "epsilon_time_drift_abs": "MISSING_STATIONARITY_THEOREM_OR_TIME_DRIFT_COEFFICIENT",
        "epsilon_calibration_abs": "MISSING_PARENT_FIXED_UNIVERSAL_CALIBRATION_THEOREM_OR_RETAINED_OFFSET",
    }
    bmem_feed = numeric_by5("RUN4825_5_Bmem_feed_smoke_pass", "bmem_feed", timestamp)
    bmem_feed.update(
        {
            "B826_abs": 0.01,
            "BWeyl_abs": 0.02,
            "BY6_abs": 0.04,
            "Bsrc_boundary_abs": 0.05,
            "Bsrc_readout_abs": 0.06,
        }
    )
    forbidden_cancel = numeric_by5("RUN4825_6_forbidden_cancellation_bound", "by5_bound", timestamp)
    forbidden_cancel.update({"notes": "CANCEL_UNKNOWN_COMPONENTS control"})
    forbidden_measured_g = numeric_by5("RUN4825_7_forbidden_measured_G_absorption", "bmem_feed", timestamp)
    forbidden_measured_g.update(
        {
            "B826_abs": 0.01,
            "BWeyl_abs": 0.02,
            "BY6_abs": 0.04,
            "Bsrc_boundary_abs": 0.05,
            "Bsrc_readout_abs": 0.06,
            "notes": "MEASURED_G_ABSORPTION control",
        }
    )
    return [
        {
            "row_id": "RUN4825_0_live_owner_zero_missing",
            "route": "live BY5 owner-zero audit",
            **zero_base,
            "notes": "live BY5 owner theorem remains unsigned",
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "RUN4825_1_conditional_owner_zero_pass",
            "route": "conditional BY5 source-functor zero theorem",
            **zero_base,
            "same_branch_signed": True,
            "parent_object_language_signed": True,
            "no_cancellation_guard": True,
            "same_frame_signed": True,
            "constant_universal_coupling_signed": True,
            "PiM_parent_origin_signed": True,
            "flux_closure_signed": True,
            "worldtube_glue_signed": True,
            "no_extra_mu_channels_signed": True,
            "no_absorption_guard_signed": True,
            "Newton_Poisson_orbit_signed": True,
            "source_functor_qbasic_signed": True,
            "notes": "control only: full owner theorem signed",
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "RUN4825_2_forbidden_fitted_G_zero",
            "route": "forbidden measured-G absorption zero",
            **zero_base,
            "same_branch_signed": True,
            "parent_object_language_signed": True,
            "no_cancellation_guard": True,
            "same_frame_signed": True,
            "constant_universal_coupling_signed": True,
            "PiM_parent_origin_signed": True,
            "flux_closure_signed": True,
            "worldtube_glue_signed": True,
            "no_extra_mu_channels_signed": True,
            "no_absorption_guard_signed": True,
            "Newton_Poisson_orbit_signed": True,
            "source_functor_qbasic_signed": True,
            "notes": "MEASURED_G_ABSORPTION / ORBITAL_GM_AS_SOURCE is forbidden",
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "RUN4825_3_live_BY5_bound_missing",
            "route": "live first BY5 source-normalization row",
            **missing_bound,
            "notes": "live BY5 finite row still lacks source-backed epsilon values",
            "timestamp_utc": timestamp,
        },
        numeric_by5("RUN4825_4_BY5_bound_smoke_pass", "by5_bound", timestamp),
        bmem_feed,
        forbidden_cancel,
        forbidden_measured_g,
    ]


def decision_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "decision": DECISION,
            "meaning": "BY5 source-functor zero is not parent-signed, but the eight-channel source-normalization row is now executable and can feed B_mem_eff without fitted-G absorption.",
            "next_target": NEXT_TARGET,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
    ]


def claim_gate_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "gate_id": "G4825_0_BY5_zero",
            "claim": "B_Y5_trace=0 by source-functor owner theorem.",
            "required": "all owner-zero clauses signed in same branch",
            "current_status": "blocked_unsigned",
            "claim_allowed": False,
            "timestamp_utc": timestamp,
        },
        {
            "gate_id": "G4825_1_BY5_bound",
            "claim": "finite BY5_abs can feed B_mem_eff.",
            "required": "eight epsilon rows numeric/source-backed or theorem-zero",
            "current_status": "runner_ready_live_values_missing",
            "claim_allowed": False,
            "timestamp_utc": timestamp,
        },
        {
            "gate_id": "G4825_2_measured_G_guard",
            "claim": "measured G/GM cannot hide BY5 unless it is common, universal, range/time/species/frame independent.",
            "required": "no derivative/source-normalization hair; otherwise residual rows remain active",
            "current_status": "guard_active",
            "claim_allowed": False,
            "timestamp_utc": timestamp,
        },
    ]


def status_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "status": "PRIVATE_NONCLAIM",
            "result": "BY5/source-normalization advanced to executable owner-zero-or-eight-channel finite row",
            "missing": "same-frame/PiM/flux/worldtube owner signs or eight epsilon source-normalization values",
            "timestamp_utc": timestamp,
        }
    ]


def next_target_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "next_target": NEXT_TARGET,
            "why": "1013 identifies [d,Pi_M]J_H as the direct product-rule obstruction contaminating radial M_eff/source-normalization.",
            "first_question": "Can fixed parent Pi_M make [d,Pi_M]J_H vanish, or must I_commutator become the first BY5 obstruction value?",
            "timestamp_utc": timestamp,
        }
    ]


def append_claim(timestamp: str) -> None:
    rows = read_csv(CLAIMS_PATH)
    if any(row.get("claim_id") == CLAIM_ID for row in rows):
        return
    rows.append(
        {
            "claim_id": CLAIM_ID,
            "domain": "local_gr",
            "claim": "BY5_source_functor_zero_or_first_source_normalization_row",
            "current_evidence": "4825 converts the BY5 measured-GM/source-normalization tail into an executable owner-zero or eight-channel finite source-normalization runner.",
            "status": "BY5_source_functor_runner_private_nonclaim",
            "next_test": NEXT_TARGET,
            "key_risk": "Pi_M origin/flux closure/worldtube glue and eight epsilon rows remain unsigned or missing",
            "sector": "local_gr_Newton_source_coupling",
            "evidence": str(DOC_PATH),
            "next_action": NEXT_TARGET,
            "risk": "smoke rows pass but live BY5 values are not source-backed",
            "title": "BY5 source-functor zero or first source-normalization row",
            "notes": f"{MARKER}; {DECISION}; generated {timestamp}",
        }
    )
    write_csv(CLAIMS_PATH, rows)


def append_section(path: Path, heading: str, body: str) -> None:
    text = read_text(path)
    if MARKER in text:
        return
    suffix = "\n\n" if text and not text.endswith("\n") else "\n"
    write_text(path, text + suffix + f"## {heading}\n\n{body}\n")


def build_doc(timestamp: str, source_rows: list[dict[str, Any]], audit_rows: list[dict[str, Any]], contract_rows: list[dict[str, Any]], output_rows: list[dict[str, Any]]) -> str:
    return f"""# 4825 - BY5 Source Functor Zero Or First Source Normalization Row

Generated UTC: `{timestamp}`

Marker: `{MARKER}`

## Result

4825 isolates the Newton/source-normalization pressure point inside `B_mem_eff`:

```text
B_Y5_trace = source-normalization / measured-GM / Pi_M-J_H tail
BY5_abs = Σ_i |epsilon_i|
B_mem_eff = B_other + BY5_abs
```

The exact zero route is strong but still unsigned. It needs same-frame matter/source/orbit readout, constant universal coupling, parent-owned `Pi_M`, compact-exterior flux closure, worldtube glue, no extra `mu` channels, no measured-G absorption, and the Newton/Poisson/orbit source gate all signed in the same branch.

The finite route is now executable: eight source-normalization coefficients can produce a first `BY5_abs` row, which then feeds the 4824 `B_mem_eff` component vector. This keeps the theory honest: measured `G`/`GM` cannot be used as a broom for radial, range, time, species, frame, or calibration hair.

## Source Register

{md_table(source_rows, ["source_id", "exists", "needle_found", "role"])}

## Owner Zero Audit

{md_table(audit_rows, ["clause_id", "claim_piece", "current_result", "finite_fallback"])}

## First Source-Normalization Contract

{md_table(contract_rows, ["contract_id", "quantity", "formula", "status"])}

## Runner Output

{md_table(output_rows, ["row_id", "runner_status", "BY5_abs", "B_mem_eff_abs", "source_normalization_status", "missing_for_claim"])}

## Decision

`{DECISION}`

Next target: `{NEXT_TARGET}`
"""


def validation_rows(timestamp: str, source_rows: list[dict[str, Any]], output_rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    statuses = {row["row_id"]: row["runner_status"] for row in output_rows}
    checks = [
        ("VAL4825_00_sources_exist", all(row["exists"] for row in source_rows), "all cited source paths exist"),
        ("VAL4825_01_needles_found", all(row["needle_found"] for row in source_rows), "all source needles found"),
        ("VAL4825_02_live_zero_blocked", statuses.get("RUN4825_0_live_owner_zero_missing") == "BLOCKED_BY5_SOURCE_FUNCTOR_ZERO_CLAUSES", "live owner-zero route remains blocked"),
        ("VAL4825_03_conditional_zero_pass", statuses.get("RUN4825_1_conditional_owner_zero_pass") == "BY5_SOURCE_FUNCTOR_ZERO_PASS_NONCLAIM", "conditional owner-zero control passes"),
        ("VAL4825_04_forbidden_measured_G_zero_fails", statuses.get("RUN4825_2_forbidden_fitted_G_zero") == "FAILED_FORBIDDEN_SOURCE_OR_CIRCULAR_ROUTE", "fitted/measured-G zero shortcut fails"),
        ("VAL4825_05_live_bound_blocked", statuses.get("RUN4825_3_live_BY5_bound_missing") == "BLOCKED_BY5_SOURCE_NORMALIZATION_INPUTS", "live BY5 finite row blocked"),
        ("VAL4825_06_BY5_smoke_pass", statuses.get("RUN4825_4_BY5_bound_smoke_pass") == "BY5_SOURCE_NORMALIZATION_BOUND_PASS_NONCLAIM", "BY5 eight-channel smoke passes"),
        ("VAL4825_07_Bmem_feed_pass", statuses.get("RUN4825_5_Bmem_feed_smoke_pass") == "BY5_BMEM_FEED_PASS_NONCLAIM", "BY5 to Bmem feed smoke passes"),
        ("VAL4825_08_forbidden_cancellation_fails", statuses.get("RUN4825_6_forbidden_cancellation_bound") == "FAILED_FORBIDDEN_SOURCE_OR_CIRCULAR_ROUTE", "cancellation route fails"),
        ("VAL4825_09_forbidden_G_absorption_fails", statuses.get("RUN4825_7_forbidden_measured_G_absorption") == "FAILED_FORBIDDEN_SOURCE_OR_CIRCULAR_ROUTE", "measured-G absorption feed fails"),
        ("VAL4825_10_no_claim_allowed", all(str(row.get("claim_allowed", "")).lower() == "false" for row in output_rows), "runner never allows a claim"),
    ]
    return [
        {
            "checkpoint": CHECKPOINT,
            "check_id": check_id,
            "status": "PASS" if passed else "FAIL",
            "detail": detail,
            "timestamp_utc": timestamp,
        }
        for check_id, passed, detail in checks
    ]


def main() -> int:
    timestamp = now()
    source_rows = build_source_register(timestamp)
    audit_rows = owner_audit(timestamp)
    contract_rows = value_contract(timestamp)
    input_rows = runner_input(timestamp)
    write_csv(SOURCE_REGISTER, source_rows)
    write_csv(OWNER_AUDIT, audit_rows)
    write_csv(VALUE_CONTRACT, contract_rows)
    write_csv(RUNNER_INPUT, input_rows)

    py_compile.compile(str(RUNNER), doraise=True)
    subprocess.run(["python", str(RUNNER), str(RUNNER_INPUT), str(RUNNER_OUTPUT)], check=True)
    output_rows = read_csv(RUNNER_OUTPUT)

    write_csv(DECISION_CSV, decision_rows(timestamp))
    write_csv(CLAIM_GATES, claim_gate_rows(timestamp))
    write_csv(STATUS_CSV, status_rows(timestamp))
    write_csv(NEXT_TARGET_CSV, next_target_rows(timestamp))
    validation = validation_rows(timestamp, source_rows, output_rows)
    write_csv(VALIDATION_CSV, validation)

    doc = build_doc(timestamp, source_rows, audit_rows, contract_rows, output_rows)
    write_text(DOC_PATH, doc)
    write_text(FORMAL_PATH, doc)
    append_claim(timestamp)
    append_section(
        SPINE_PATH,
        "PPC4161 4825 BY5 source-normalization runner",
        f"`{MARKER}`. `B_Y5_trace` is now an executable owner-zero or eight-channel source-normalization bound feeding `B_mem_eff`; measured-G absorption and cancellation are rejected. Decision: `{DECISION}`.",
    )
    append_section(
        PACKET_PATH,
        "4825 BY5 source-normalization runner",
        f"`{MARKER}` sharpens the Newton/source coupling pressure point: BY5 can close only by parent-signed source-functor ownership or by explicit epsilon rows. Next: `{NEXT_TARGET}`.",
    )
    write_text(
        RESUME_PATH,
        f"""# Current local resume

Updated: `{timestamp}`
Last checkpoint: `4825-Y5-R2FR-BY5-source-functor-zero-or-first-source-normalization-row.md`
Marker: `{MARKER}`

## Where we are

4825 made the BY5/source-normalization bottleneck executable:

```text
BY5_abs = |epsilon_radial|+|epsilon_boundary|+|epsilon_domain|+|epsilon_bulk|
        + |epsilon_nonEH|+|epsilon_species|+|epsilon_time|+|epsilon_calibration|
B_mem_eff = B_other + BY5_abs
```

## Live blockers

- The BY5 owner-zero theorem is not parent-signed.
- `Pi_M` origin, `d(Pi_M J_H)` flux closure, worldtube glue, and no-extra-mu clauses remain open.
- Measured `G`/`GM` absorption is explicitly forbidden unless the factor is common, universal, range/time/species/frame independent.
- Live BY5 values still need sourced epsilon rows or componentwise theorem-zero certificates.

## Next target

`{NEXT_TARGET}`
""",
    )

    py_compile.compile(str(Path(__file__)), doraise=True)
    pycache = SCRIPT_DIR / "__pycache__"
    if pycache.exists():
        shutil.rmtree(pycache)
    failed = [row for row in validation if row["status"] != "PASS"]
    if failed:
        print(f"4825 generated with {len(failed)} validation failures")
        return 1
    print(f"4825 generated: {DOC_PATH}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

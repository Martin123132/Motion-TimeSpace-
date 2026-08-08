from __future__ import annotations

import csv
import hashlib
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


RUN_UTC = datetime.now(timezone.utc).isoformat()
ROOT = Path(__file__).resolve().parents[1]
PROJECT = ROOT.parent
RESIDUALS = ROOT / "source-intake" / "mts_residuals"
PARENT_ACTION = ROOT / "source-intake" / "parent-action"
LOCAL_BOUNDS = ROOT / "source-intake" / "local_bounds"
RAB_QUEUE = ROOT / "source-intake" / "rab-sector" / "acquisition-queue"
FORMALIZATION = PROJECT / "formalization-workbench"
PYCACHE = ROOT / "scripts" / "__pycache__"

CHECKPOINT = "3080"
BRANCH_ID = "MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428"

DOC = ROOT / "3080-Y5-R2FR-no-hypermomentum-source-readout-functor-or-DeltaGamma-bound-under-AX1090.md"
DOTG_TARGET = RESIDUALS / "P8_time_drift_residual_or_zero.csv"

SOURCE_PATHS = {
    "SRC3080_00_3079_doc": ROOT / "3079-Y5-R2FR-local-geometry-field-list-signature-or-TQ-bound-source-acquisition-under-AX1090.md",
    "SRC3080_01_3079_next": RESIDUALS / "P8_Y5_R2FR_3079_NEXT_TARGET.csv",
    "SRC3080_02_3079_current": RESIDUALS / "P8_Y5_R2FR_3079_SOURCE_READOUT_CONNECTION_CURRENT_AUDIT.csv",
    "SRC3080_03_3079_decision": RESIDUALS / "P8_Y5_R2FR_3079_DECISION_LEDGER.csv",
    "SRC3080_04_3075_nohyper": RESIDUALS / "P8_Y5_R2FR_3075_NO_HYPERMOMENTUM_AUDIT.csv",
    "SRC3080_05_1831_inventory": RESIDUALS / "P8_Y5_PARENT_QLOC_1831_FIELD_INVENTORY_CERTIFICATE_ATTEMPT.csv",
    "SRC3080_06_1832_tq": RESIDUALS / "P8_Y5_PARENT_QLOC_1832_TQ_ZERO_THEOREM_ATTEMPT.csv",
    "SRC3080_07_1833_distortion": RESIDUALS / "P8_Y5_PARENT_QLOC_1833_DISTORTION_EQUATION_OWNER_AUDIT.csv",
    "SRC3080_08_1833_hyper": RESIDUALS / "P8_Y5_PARENT_QLOC_1833_HYPERMOMENTUM_SOURCE_ROW.csv",
    "SRC3080_09_1833_decision": RESIDUALS / "P8_Y5_PARENT_QLOC_1833_DECISION_LEDGER.csv",
    "SRC3080_10_1834_bound": RESIDUALS / "P8_Y5_PARENT_QLOC_1834_DELTAGAMMA_BOUND_ROW.csv",
    "SRC3080_11_1834_decision": RESIDUALS / "P8_Y5_PARENT_QLOC_1834_DECISION_LEDGER.csv",
    "SRC3080_12_dotg_target": DOTG_TARGET,
}

OUTPUTS = {
    "sources": RESIDUALS / "P8_Y5_R2FR_3080_SOURCE_REGISTER.csv",
    "functor": RESIDUALS / "P8_Y5_R2FR_3080_NO_HYPERMOMENTUM_SOURCE_READOUT_FUNCTOR_AUDIT.csv",
    "delta_bounds": RESIDUALS / "P8_Y5_R2FR_3080_DELTAGAMMA_BOUND_COMPONENTS_NONCLAIM.csv",
    "sector_split": RESIDUALS / "P8_Y5_R2FR_3080_SOURCE_READOUT_SECTOR_SPLIT_LEDGER.csv",
    "tq_consequence": RESIDUALS / "P8_Y5_R2FR_3080_DELTAGAMMA_TO_TQ_CONSEQUENCE_LEDGER.csv",
    "arena_blockers": RESIDUALS / "P8_Y5_R2FR_3080_LOCAL_ARENA_BLOCKERS_NONCLAIM.csv",
    "historical": RESIDUALS / "P8_Y5_R2FR_3080_PRIOR_TRAIL_RECONCILIATION_LEDGER.csv",
    "decision": RESIDUALS / "P8_Y5_R2FR_3080_DECISION_LEDGER.csv",
    "claim_status": RESIDUALS / "P8_Y5_R2FR_3080_CLAIM_STATUS.csv",
    "next": RESIDUALS / "P8_Y5_R2FR_3080_NEXT_TARGET.csv",
    "branches": RESIDUALS / "P8_Y5_R2FR_3080_BRANCH_COPIES.csv",
    "validation": RESIDUALS / "P8_Y5_BRR545_3080_VALIDATION.csv",
}

BRANCH_OUTPUTS = {
    "functor_copy": PARENT_ACTION / "no_hypermomentum_source_readout_functor_3080_NOT_SIGNED.csv",
    "delta_bounds_copy": LOCAL_BOUNDS / "DeltaGamma_bound_components_3080_NONCLAIM.csv",
    "tq_consequence_copy": LOCAL_BOUNDS / "DeltaGamma_to_TQ_consequence_3080_NONCLAIM.csv",
    "arena_blockers_copy": LOCAL_BOUNDS / "DeltaGamma_local_arena_blockers_3080_NONCLAIM.csv",
    "next_copy": RAB_QUEUE / "JR3080_DeltaGamma_component_map_to_P4_observables_NEXT_NONCLAIM.csv",
}

for output_path in list(OUTPUTS.values()) + list(BRANCH_OUTPUTS.values()) + [DOC]:
    output_path.parent.mkdir(parents=True, exist_ok=True)


def remove_pycache() -> None:
    if PYCACHE.exists():
        shutil.rmtree(PYCACHE)


def file_hash(path: Path) -> str:
    if not path.exists():
        return "MISSING"
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(65536), b""):
            digest.update(chunk)
    return digest.hexdigest()


def rows(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    with path.open("r", newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def boolish(value: Any) -> bool:
    return str(value).strip().lower() in {"true", "1", "yes", "y", "pass", "passed"}


def csv_ok(path: Path) -> bool:
    try:
        if not path.exists():
            return False
        with path.open("r", newline="", encoding="utf-8") as handle:
            list(csv.DictReader(handle))
        return True
    except Exception:
        return False


def source_parse_ok(path: Path) -> bool:
    if not path.exists():
        return False
    return csv_ok(path) if path.suffix.lower() == ".csv" else True


def row_count(path: Path) -> int:
    if not path.exists():
        return 0
    if path.suffix.lower() == ".csv":
        return len(rows(path))
    return len(path.read_text(encoding="utf-8").splitlines())


def write_csv(path: Path, output_rows: list[dict[str, Any]]) -> None:
    fieldnames: list[str] = []
    for output_row in output_rows:
        for key in output_row:
            if key not in fieldnames:
                fieldnames.append(key)
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for output_row in output_rows:
            writer.writerow({key: output_row.get(key, "") for key in fieldnames})


def under(path: Path, root: Path) -> bool:
    try:
        path.resolve().relative_to(root.resolve())
        return True
    except ValueError:
        return False


def has_claim_true(input_rows: list[dict[str, Any]]) -> bool:
    claim_fields = {
        "valid_for_claim",
        "claim_allowed",
        "valid_prediction_row",
        "score_ready",
        "claim_active",
        "functor_signed",
        "current_zero_signed",
        "bound_ready",
        "numeric_ready",
        "arena_map_ready",
        "local_gr_claim",
        "tq_zero_claim",
        "delta_gamma_zero_claim",
    }
    for input_row in input_rows:
        for field in claim_fields:
            if field in input_row and boolish(input_row[field]):
                return True
    return False


def base(row: dict[str, Any]) -> dict[str, Any]:
    return {
        "checkpoint": CHECKPOINT,
        "branch_id": BRANCH_ID,
        "timestamp_utc": RUN_UTC,
        "score_ready": "false",
        "valid_prediction_row": "false",
        "valid_for_claim": "false",
        "claim_allowed": "false",
        **row,
    }


def md_escape(value: Any) -> str:
    return str(value).replace("|", "\\|").replace("\n", " ")


def md_table(table_rows: list[dict[str, Any]], columns: list[str]) -> str:
    if not table_rows:
        return "_No rows._"
    header = "| " + " | ".join(columns) + " |"
    separator = "| " + " | ".join("---" for _ in columns) + " |"
    lines = [header, separator]
    for table_row in table_rows:
        lines.append("| " + " | ".join(md_escape(table_row.get(column, "")) for column in columns) + " |")
    return "\n".join(lines)


def copy_csv(source_path: Path, destination_path: Path) -> None:
    destination_path.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(source_path, destination_path)


remove_pycache()
dotg_hash_before = file_hash(DOTG_TARGET)

source_register = [
    base(
        {
            "source_id": source_id,
            "source_path": str(source_path),
            "exists": str(source_path.exists()),
            "parse_ok": str(source_parse_ok(source_path)),
            "row_count": row_count(source_path),
            "role": "no_hypermomentum_or_DeltaGamma_bound_evidence" if source_id != "SRC3080_12_dotg_target" else "append_guard_target",
            "status": "PRESENT" if source_path.exists() else "MISSING_SOURCE",
        }
    )
    for source_id, source_path in SOURCE_PATHS.items()
]

functor_rows = [
    base(
        {
            "functor_id": "NHF3080_0_ordinary_matter",
            "sector": "ordinary matter",
            "required_functor_clause": "S_matter depends on Gamma only through omega[e_obs]/Gamma_LC[g_obs]",
            "current_status": "NOT_PARENT_SIGNED",
            "functor_signed": "false",
            "current_zero_signed": "false",
            "missing_for_claim": "MISSING_MATTER_ACTION_DOMAIN;MISSING_CONNECTION_CURRENT_EXCLUSION",
            "source_ids": "SRC3080_04_3075_nohyper;SRC3080_05_1831_inventory",
        }
    ),
    base(
        {
            "functor_id": "NHF3080_1_spin_transport",
            "sector": "spinor/spin transport",
            "required_functor_clause": "spin connection is coframe-owned and spin variation is counted through e_obs, not independent torsionful Gamma",
            "current_status": "CONDITIONAL_SPIN_GUARD_NOT_GLOBAL",
            "functor_signed": "false",
            "current_zero_signed": "false",
            "missing_for_claim": "MISSING_SPINOR_TRANSPORT_CLAUSE;MISSING_SPIN_TORSION_EXCLUSION",
            "source_ids": "SRC3080_04_3075_nohyper;SRC3080_08_1833_hyper",
        }
    ),
    base(
        {
            "functor_id": "NHF3080_2_source_support",
            "sector": "source mass/support/worldtube",
            "required_functor_clause": "source support and finite worldtube action contain no Gamma_ind, boundary torsion or source-only connection current",
            "current_status": "SOURCE_SUPPORT_CURRENT_NOT_ZEROED",
            "functor_signed": "false",
            "current_zero_signed": "false",
            "missing_for_claim": "MISSING_SOURCE_SUPPORT_DESCENT;MISSING_BOUNDARY_TORSION_SILENCE;MISSING_SOURCE_BRANCH_NORMALIZATION",
            "source_ids": "SRC3080_02_3079_current;SRC3080_08_1833_hyper;SRC3080_10_1834_bound",
        }
    ),
    base(
        {
            "functor_id": "NHF3080_3_readout",
            "sector": "clock/orbital/readout",
            "required_functor_clause": "readout maps have no independent connection-current, source-label morphism or non-Hilbert connection residue",
            "current_status": "READOUT_CONNECTION_CURRENT_NOT_ZEROED",
            "functor_signed": "false",
            "current_zero_signed": "false",
            "missing_for_claim": "MISSING_READOUT_TRANSFER_DOMAIN;MISSING_NO_SOURCE_LABEL_MORPHISM;MISSING_ORBITAL_CLOCK_MAP",
            "source_ids": "SRC3080_02_3079_current;SRC3080_08_1833_hyper;SRC3080_10_1834_bound",
        }
    ),
    base(
        {
            "functor_id": "NHF3080_4_projective_boundary",
            "sector": "projective/boundary connection channel",
            "required_functor_clause": "projective trace and boundary-supported connection modes are gauge, fixed, exact or projected silent",
            "current_status": "PROJECTIVE_BOUNDARY_NOT_FIXED",
            "functor_signed": "false",
            "current_zero_signed": "false",
            "missing_for_claim": "MISSING_PROJECTIVE_INVARIANCE;MISSING_BOUNDARY_NO_FLUX;MISSING_SOURCE_SUPPORT_MAP",
            "source_ids": "SRC3080_06_1832_tq;SRC3080_07_1833_distortion",
        }
    ),
    base(
        {
            "functor_id": "NHF3080_5_verdict",
            "sector": "all source-current sectors",
            "required_functor_clause": "all independent connection-current channels vanish in one parent branch",
            "current_status": "NO_HYPERMOMENTUM_FUNCTOR_NOT_SIGNED",
            "functor_signed": "false",
            "current_zero_signed": "false",
            "missing_for_claim": "MISSING_ALL_CURRENT_ZERO_THEOREMS_OR_BOUNDS",
            "source_ids": "SRC3080_04_3075_nohyper;SRC3080_08_1833_hyper;SRC3080_11_1834_decision",
        }
    ),
]

delta_bound_rows = [
    base(
        {
            "bound_id": "DGB3080_0_total",
            "quantity": "||Delta_Gamma_total||",
            "definition": "delta(S_matter + S_source + S_readout)/delta Gamma",
            "bound_formula": "||Delta_spin|| + ||Delta_source|| + ||Delta_readout|| + ||Delta_projective|| + ||Delta_boundary||",
            "current_status": "BOUND_ROW_STAGED_NONCLAIM",
            "bound_ready": "false",
            "numeric_ready": "false",
            "missing_for_claim": "MISSING_COMPONENT_VALUES;MISSING_COMMON_DUAL_CONNECTION_UNITS;MISSING_CONNECTION_VARIATION_NORMALIZATION;MISSING_DELTAGAMMA_TO_P4_WEP_PPN_CLOCK_MAP",
            "source_ids": "SRC3080_08_1833_hyper;SRC3080_10_1834_bound",
        }
    ),
    base(
        {
            "bound_id": "DGB3080_1_spin",
            "quantity": "||Delta_spin||",
            "definition": "spinor/tetrad connection charge beyond coframe-owned omega[e_obs]",
            "bound_formula": "spin/torsion source norm in same dual connection basis",
            "current_status": "MISSING_SPIN_BOUND",
            "bound_ready": "false",
            "numeric_ready": "false",
            "missing_for_claim": "MISSING_SPIN_CURRENT_UNITS;MISSING_SPIN_CONNECTION_NORMALIZATION;MISSING_SPIN_TO_CLOCK_LIGHTCONE_MAP",
            "source_ids": "SRC3080_08_1833_hyper;SRC3080_10_1834_bound",
        }
    ),
    base(
        {
            "bound_id": "DGB3080_2_source_readout",
            "quantity": "||Delta_source_readout||",
            "definition": "source support plus readout connection-current norm",
            "bound_formula": "source_support + clock_readout + orbital_readout + boundary_marker channels",
            "current_status": "MISSING_SOURCE_READOUT_BOUND",
            "bound_ready": "false",
            "numeric_ready": "false",
            "missing_for_claim": "MISSING_SOURCE_READOUT_UNITS;MISSING_SOURCE_BRANCH_NORMALIZATION;MISSING_R10_PPN_ORBITAL_MAP",
            "source_ids": "SRC3080_08_1833_hyper;SRC3080_10_1834_bound",
        }
    ),
    base(
        {
            "bound_id": "DGB3080_3_projective",
            "quantity": "||Delta_projective||",
            "definition": "projective trace source/current channel",
            "bound_formula": "projective current norm or zero by projective invariance",
            "current_status": "MISSING_PROJECTIVE_BOUND_OR_ZERO_THEOREM",
            "bound_ready": "false",
            "numeric_ready": "false",
            "missing_for_claim": "MISSING_PROJECTIVE_INVARIANCE;MISSING_PROJECTIVE_CURRENT_UNITS;MISSING_WEP_MAP",
            "source_ids": "SRC3080_06_1832_tq;SRC3080_07_1833_distortion",
        }
    ),
    base(
        {
            "bound_id": "DGB3080_4_boundary",
            "quantity": "||Delta_boundary||",
            "definition": "boundary/support/corner connection-current leakage",
            "bound_formula": "boundary connection-current norm or no-flux exact term",
            "current_status": "MISSING_BOUNDARY_BOUND_OR_ZERO_THEOREM",
            "bound_ready": "false",
            "numeric_ready": "false",
            "missing_for_claim": "MISSING_BOUNDARY_NO_FLUX;MISSING_SOURCE_SUPPORT_MAP;MISSING_EDGE_UNITS",
            "source_ids": "SRC3080_07_1833_distortion;SRC3080_10_1834_bound",
        }
    ),
    base(
        {
            "bound_id": "DGB3080_5_units_projection",
            "quantity": "Delta_Gamma units/projection",
            "definition": "common dual-connection units and observable projection for all Delta_Gamma components",
            "bound_formula": "component maps into P4_TQ, PPN, R10, WEP, clocks and orbital residuals",
            "current_status": "MISSING_COMPONENT_TO_OBSERVABLE_MAP",
            "bound_ready": "false",
            "numeric_ready": "false",
            "missing_for_claim": "MISSING_COMMON_UNITS;MISSING_P4_MAP;MISSING_OBSERVABLE_RESPONSE_MAP",
            "source_ids": "SRC3080_10_1834_bound;SRC3080_11_1834_decision",
        }
    ),
]

sector_split_rows = [
    base(
        {
            "sector_id": "DGS3080_0_spin",
            "component": "Delta_spin",
            "physical_channel": "spin/torsion hypermomentum",
            "blocked_tests": "clock;lightcone;spin;PPN",
            "current_status": "RETAIN_COMPONENT_NONCLAIM",
            "next_map_needed": "spin-current to torsion/clock/lightcone residual map",
        }
    ),
    base(
        {
            "sector_id": "DGS3080_1_source_support",
            "component": "Delta_source",
            "physical_channel": "finite source/worldtube/support current",
            "blocked_tests": "R10;Newton;PPN;orbital",
            "current_status": "RETAIN_COMPONENT_NONCLAIM",
            "next_map_needed": "source support current to local acceleration/force-gradient map",
        }
    ),
    base(
        {
            "sector_id": "DGS3080_2_readout",
            "component": "Delta_readout",
            "physical_channel": "clock/orbit/readout connection current",
            "blocked_tests": "clock;orbital;WEP",
            "current_status": "RETAIN_COMPONENT_NONCLAIM",
            "next_map_needed": "readout current to observed residual map",
        }
    ),
    base(
        {
            "sector_id": "DGS3080_3_projective_boundary",
            "component": "Delta_projective + Delta_boundary",
            "physical_channel": "projective trace and boundary/corner leakage",
            "blocked_tests": "WEP;R10;orbital;clock",
            "current_status": "RETAIN_COMPONENT_NONCLAIM",
            "next_map_needed": "projective/boundary gauge or no-flux map",
        }
    ),
]

tq_consequence_rows = [
    base(
        {
            "consequence_id": "DGTQ3080_0_distortion_equation",
            "statement": "If independent distortion C exists, the schematic route is M_C C = Delta_Gamma + boundary + projective.",
            "current_status": "RIGHT_HAND_SIDE_NOT_ZEROED_OR_BOUNDED",
            "tq_zero_claim": "false",
            "local_gr_claim": "false",
            "consequence": "C, T and Q cannot be set to zero from current evidence",
        }
    ),
    base(
        {
            "consequence_id": "DGTQ3080_1_metric_only_escape",
            "statement": "If the parent field list excludes C/Gamma_ind entirely, Delta_Gamma is absent by construction.",
            "current_status": "FIELD_LIST_NOT_SIGNED",
            "tq_zero_claim": "false",
            "local_gr_claim": "false",
            "consequence": "metric-only escape remains exact but conditional",
        }
    ),
    base(
        {
            "consequence_id": "DGTQ3080_2_empirical_branch",
            "statement": "If Delta_Gamma survives, the local branch becomes a residual/bound branch rather than derived local GR.",
            "current_status": "BOUND_COMPONENTS_STAGED_NO_MAP",
            "tq_zero_claim": "false",
            "local_gr_claim": "false",
            "consequence": "next task is component-to-observable mapping",
        }
    ),
]

arena_blocker_rows = [
    base(
        {
            "arena_id": "DGA3080_0_R10",
            "arena": "R10",
            "current_blocker": "Delta_source_readout and boundary/support currents lack force-gradient map",
            "arena_map_ready": "false",
            "local_gr_claim": "false",
        }
    ),
    base(
        {
            "arena_id": "DGA3080_1_PPN_orbital",
            "arena": "PPN/orbital",
            "current_blocker": "Delta_spin, Delta_source and Delta_projective lack preferred-frame/shear/orbital response map",
            "arena_map_ready": "false",
            "local_gr_claim": "false",
        }
    ),
    base(
        {
            "arena_id": "DGA3080_2_clocks_WEP",
            "arena": "clocks/WEP",
            "current_blocker": "spin, non-Hilbert readout and projective/boundary currents lack clock/rod/composition map",
            "arena_map_ready": "false",
            "local_gr_claim": "false",
        }
    ),
]

historical_rows = [
    base(
        {
            "trail_id": "HIST3080_0_1833",
            "prior_checkpoint": "1833",
            "prior_result": "distortion equation owner not proven; Delta_Gamma source row staged",
            "current_use": "confirms no C=0/T=Q=0 claim is allowed from distortion equation route",
            "status": "CONSISTENT_WITH_3080",
            "source_ids": "SRC3080_07_1833_distortion;SRC3080_08_1833_hyper;SRC3080_09_1833_decision",
        }
    ),
    base(
        {
            "trail_id": "HIST3080_1_1834",
            "prior_checkpoint": "1834",
            "prior_result": "no-hypermomentum theorem not proven; DeltaGamma bound row staged nonclaim",
            "current_use": "confirms 3080 should move to component maps, not broad proof repetition",
            "status": "CONSISTENT_WITH_3080_NEXT_TARGET",
            "source_ids": "SRC3080_10_1834_bound;SRC3080_11_1834_decision",
        }
    ),
]

decision_rows = [
    base(
        {
            "decision_id": "DEC3080_0_functor",
            "decision": "no-hypermomentum/source-readout functor not signed",
            "reason": "matter functor, spin transport, source support, readout current, projective and boundary clauses all remain unsigned",
            "consequence": "Delta_Gamma cannot be set to zero",
            "next_action": "keep Delta_Gamma components explicit",
        }
    ),
    base(
        {
            "decision_id": "DEC3080_1_bound",
            "decision": "Delta_Gamma bound components staged nonclaim",
            "reason": "component rows exist but lack values, units, normalization and observable maps",
            "consequence": "no local arena can score yet",
            "next_action": "map components to P4 observables",
        }
    ),
    base(
        {
            "decision_id": "DEC3080_2_next",
            "decision": "3081 DeltaGamma component map",
            "reason": "1834 already selected component-to-observable mapping as the next non-circular task",
            "consequence": "moves from broad theorem attempts toward testable residual channels",
            "next_action": "3081-Y5-R2FR-DeltaGamma-component-map-to-P4-observables-under-AX1090.md",
        }
    ),
]

claim_rows = [
    base(
        {
            "claim_id": "CLAIM3080_0_DeltaGamma_zero",
            "claim": "Delta_Gamma_total=0",
            "claim_active": "false",
            "status": "NOT_CLAIMED",
            "reason": "no-hypermomentum/source-readout functor is not signed",
        }
    ),
    base(
        {
            "claim_id": "CLAIM3080_1_DeltaGamma_bound",
            "claim": "Delta_Gamma has numeric source-backed bounds",
            "claim_active": "false",
            "status": "NOT_CLAIMED",
            "reason": "bound rows lack values, units, normalization and observable maps",
        }
    ),
    base(
        {
            "claim_id": "CLAIM3080_2_TQ_zero",
            "claim": "C=0, T=Q=0, K_P4_TQ=0",
            "claim_active": "false",
            "status": "NOT_CLAIMED",
            "reason": "right-hand side of distortion equation is not zeroed or bounded",
        }
    ),
    base(
        {
            "claim_id": "CLAIM3080_3_local_tests",
            "claim": "local GR/Newton/PPN/R10/clock/WEP/orbital pass",
            "claim_active": "false",
            "status": "NOT_CLAIMED",
            "reason": "Delta_Gamma, Delta_K, P4 and arena maps remain nonclaim",
        }
    ),
]

next_rows = [
    base(
        {
            "next_id": "NEXT3080_0_3081",
            "next_checkpoint": "3081-Y5-R2FR-DeltaGamma-component-map-to-P4-observables-under-AX1090.md",
            "script": "scripts/Y5_R2FR_DeltaGamma_component_map_to_P4_observables_under_AX1090_3081.py",
            "mission": "map Delta_spin, Delta_source_readout, Delta_projective and Delta_boundary into R10, PPN, clock, WEP and orbital residual channels without claiming numeric pass",
            "starting_equation": "||Delta_Gamma_total|| <= ||Delta_spin|| + ||Delta_source|| + ||Delta_readout|| + ||Delta_projective|| + ||Delta_boundary||",
            "claim_policy": "no numeric local test claim until component values, units, normalization and source-backed observable maps exist",
        }
    )
]

write_csv(OUTPUTS["sources"], source_register)
write_csv(OUTPUTS["functor"], functor_rows)
write_csv(OUTPUTS["delta_bounds"], delta_bound_rows)
write_csv(OUTPUTS["sector_split"], sector_split_rows)
write_csv(OUTPUTS["tq_consequence"], tq_consequence_rows)
write_csv(OUTPUTS["arena_blockers"], arena_blocker_rows)
write_csv(OUTPUTS["historical"], historical_rows)
write_csv(OUTPUTS["decision"], decision_rows)
write_csv(OUTPUTS["claim_status"], claim_rows)
write_csv(OUTPUTS["next"], next_rows)

copy_csv(OUTPUTS["functor"], BRANCH_OUTPUTS["functor_copy"])
copy_csv(OUTPUTS["delta_bounds"], BRANCH_OUTPUTS["delta_bounds_copy"])
copy_csv(OUTPUTS["tq_consequence"], BRANCH_OUTPUTS["tq_consequence_copy"])
copy_csv(OUTPUTS["arena_blockers"], BRANCH_OUTPUTS["arena_blockers_copy"])
copy_csv(OUTPUTS["next"], BRANCH_OUTPUTS["next_copy"])

branch_rows = [
    base(
        {
            "copy_id": copy_id,
            "source_path": str(source_path),
            "copy_path": str(destination_path),
            "copy_exists": str(destination_path.exists()),
            "copy_parse_ok": str(csv_ok(destination_path)),
            "status": "COPIED_NONCLAIM",
        }
    )
    for copy_id, source_path, destination_path in [
        ("BC3080_0_functor", OUTPUTS["functor"], BRANCH_OUTPUTS["functor_copy"]),
        ("BC3080_1_delta_bounds", OUTPUTS["delta_bounds"], BRANCH_OUTPUTS["delta_bounds_copy"]),
        ("BC3080_2_tq_consequence", OUTPUTS["tq_consequence"], BRANCH_OUTPUTS["tq_consequence_copy"]),
        ("BC3080_3_arena_blockers", OUTPUTS["arena_blockers"], BRANCH_OUTPUTS["arena_blockers_copy"]),
        ("BC3080_4_next", OUTPUTS["next"], BRANCH_OUTPUTS["next_copy"]),
    ]
]
write_csv(OUTPUTS["branches"], branch_rows)
write_csv(
    OUTPUTS["validation"],
    [
        base(
            {
                "validation_id": "VAL3080_PRE",
                "passed": "False",
                "requirement": "placeholder overwritten by final validation",
                "evidence": "generator ordering guard",
            }
        )
    ],
)
DOC.write_text("# 3080 draft\n", encoding="utf-8")

remove_pycache()
dotg_hash_after = file_hash(DOTG_TARGET)
generated_csvs = list(OUTPUTS.values()) + list(BRANCH_OUTPUTS.values())
generated_rows = (
    functor_rows
    + delta_bound_rows
    + sector_split_rows
    + tq_consequence_rows
    + arena_blocker_rows
    + historical_rows
    + decision_rows
    + claim_rows
    + next_rows
)
formalization_output_count = sum(1 for output_path in generated_csvs + [DOC] if under(output_path, FORMALIZATION))
required_delta_quantities = {
    "||Delta_Gamma_total||",
    "||Delta_spin||",
    "||Delta_source_readout||",
    "||Delta_projective||",
    "||Delta_boundary||",
    "Delta_Gamma units/projection",
}

validation_rows = [
    base(
        {
            "validation_id": "VAL3080_00_sources_exist",
            "passed": str(all(row["exists"] == "True" for row in source_register)),
            "requirement": "all cited source paths exist",
            "evidence": OUTPUTS["sources"].name,
        }
    ),
    base(
        {
            "validation_id": "VAL3080_01_sources_parse",
            "passed": str(all(row["parse_ok"] == "True" for row in source_register)),
            "requirement": "all cited CSV sources parse and markdown sources exist",
            "evidence": OUTPUTS["sources"].name,
        }
    ),
    base(
        {
            "validation_id": "VAL3080_02_csv_parse",
            "passed": str(all(csv_ok(output_path) for output_path in generated_csvs)),
            "requirement": "all generated and branch-copy CSVs parse cleanly",
            "evidence": "csv.DictReader parse check",
        }
    ),
    base(
        {
            "validation_id": "VAL3080_03_functor_not_signed",
            "passed": str(not any(boolish(row["functor_signed"]) or boolish(row["current_zero_signed"]) for row in functor_rows)),
            "requirement": "no-hypermomentum/source-readout functor remains unsigned",
            "evidence": OUTPUTS["functor"].name,
        }
    ),
    base(
        {
            "validation_id": "VAL3080_04_delta_bounds_complete_nonclaim",
            "passed": str(required_delta_quantities.issubset({row["quantity"] for row in delta_bound_rows}) and not has_claim_true(delta_bound_rows)),
            "requirement": "Delta_Gamma bound components are complete and nonclaim",
            "evidence": OUTPUTS["delta_bounds"].name,
        }
    ),
    base(
        {
            "validation_id": "VAL3080_05_sector_split_present",
            "passed": str({"Delta_spin", "Delta_source", "Delta_readout", "Delta_projective + Delta_boundary"}.issubset({row["component"] for row in sector_split_rows})),
            "requirement": "Delta_Gamma sector split includes spin, source, readout and projective/boundary components",
            "evidence": OUTPUTS["sector_split"].name,
        }
    ),
    base(
        {
            "validation_id": "VAL3080_06_TQ_not_zeroed",
            "passed": str(not any(boolish(row["tq_zero_claim"]) or boolish(row["local_gr_claim"]) for row in tq_consequence_rows)),
            "requirement": "T/Q zero route remains nonclaim while Delta_Gamma survives",
            "evidence": OUTPUTS["tq_consequence"].name,
        }
    ),
    base(
        {
            "validation_id": "VAL3080_07_arenas_blocked",
            "passed": str(not any(boolish(row["arena_map_ready"]) or boolish(row["local_gr_claim"]) for row in arena_blocker_rows)),
            "requirement": "R10, PPN/orbital and clock/WEP arenas remain blocked",
            "evidence": OUTPUTS["arena_blockers"].name,
        }
    ),
    base(
        {
            "validation_id": "VAL3080_08_prior_trail_reconciled",
            "passed": str({"1833", "1834"}.issubset({row["prior_checkpoint"] for row in historical_rows})),
            "requirement": "prior 1833/1834 source-current trail is reconciled",
            "evidence": OUTPUTS["historical"].name,
        }
    ),
    base(
        {
            "validation_id": "VAL3080_09_no_claim_promoted",
            "passed": str(not has_claim_true(claim_rows + decision_rows + tq_consequence_rows + arena_blocker_rows)),
            "requirement": "no Delta_Gamma zero, TQ zero, local-GR, PPN, R10, clock, WEP or orbital claim is promoted",
            "evidence": OUTPUTS["claim_status"].name,
        }
    ),
    base(
        {
            "validation_id": "VAL3080_10_next_target_selected",
            "passed": str(next_rows[0]["next_checkpoint"].startswith("3081-Y5-R2FR-DeltaGamma-component-map")),
            "requirement": "next target moves to DeltaGamma component map to P4 observables",
            "evidence": OUTPUTS["next"].name,
        }
    ),
    base(
        {
            "validation_id": "VAL3080_11_branch_copies_exist",
            "passed": str(all(row["copy_exists"] == "True" and row["copy_parse_ok"] == "True" for row in branch_rows)),
            "requirement": "branch copies exist and parse",
            "evidence": OUTPUTS["branches"].name,
        }
    ),
    base(
        {
            "validation_id": "VAL3080_12_dotg_unchanged",
            "passed": str(dotg_hash_before == dotg_hash_after),
            "requirement": "P8_time_drift_residual_or_zero.csv is not modified",
            "evidence": f"{dotg_hash_before}->{dotg_hash_after}",
        }
    ),
    base(
        {
            "validation_id": "VAL3080_13_outputs_under_post_checkpoint",
            "passed": str(all(under(output_path, ROOT) for output_path in generated_csvs + [DOC])),
            "requirement": "all outputs are under post-checkpoint-work",
            "evidence": "path containment check",
        }
    ),
    base(
        {
            "validation_id": "VAL3080_14_no_formalization_outputs",
            "passed": str(formalization_output_count == 0),
            "requirement": "formalization-workbench modified-file count for 3080 outputs remains zero",
            "evidence": f"formalization_3080_output_paths={formalization_output_count}",
        }
    ),
    base(
        {
            "validation_id": "VAL3080_15_pycache_absent",
            "passed": str(not PYCACHE.exists()),
            "requirement": "scripts __pycache__ is absent at generator completion",
            "evidence": str(PYCACHE),
        }
    ),
    base(
        {
            "validation_id": "VAL3080_16_doc_written",
            "passed": str(DOC.exists()),
            "requirement": "checkpoint markdown document is written",
            "evidence": str(DOC),
        }
    ),
    base(
        {
            "validation_id": "VAL3080_17_no_claim_fields_true",
            "passed": str(not has_claim_true(generated_rows)),
            "requirement": "no generated non-validation row contains a true claim/ready field",
            "evidence": "claim field scan",
        }
    ),
]

write_csv(OUTPUTS["validation"], validation_rows)

doc_text = f"""# 3080 - No-Hypermomentum Source/Readout Functor or DeltaGamma Bound

Status: `Y5_R2FR_3080_no_hypermomentum_not_signed_DeltaGamma_components_staged`

Generated: `{RUN_UTC}`

## Verdict

3080 attacked the right-hand side of the distortion equation:

`M_C C = Delta_Gamma + boundary + projective`.

If `Delta_Gamma` and the boundary/projective channels vanished, the T/Q route could move toward a real local-GR reduction. That does **not** close. Ordinary matter, spin transport, source support, readout maps, projective trace and boundary/corner channels are not parent-signed silent.

So 3080 does **not** claim `Delta_Gamma=0`, `C=0`, `T=Q=0`, `K_P4_TQ=0`, local GR, Newtonian recovery, PPN, R10, clocks, WEP, or orbital success.

The gain is that the obstruction is now componentized: `Delta_spin`, `Delta_source`, `Delta_readout`, `Delta_projective`, and `Delta_boundary`. The next useful step is not another broad theorem swing; it is mapping those components to actual observable residual channels.

## No-Hypermomentum Functor Audit

{md_table(functor_rows, ["functor_id", "sector", "current_status", "functor_signed", "missing_for_claim"])}

## DeltaGamma Bound Components

{md_table(delta_bound_rows, ["bound_id", "quantity", "current_status", "bound_ready", "missing_for_claim"])}

## Source/Readout Sector Split

{md_table(sector_split_rows, ["sector_id", "component", "physical_channel", "blocked_tests", "next_map_needed"])}

## TQ Consequence

{md_table(tq_consequence_rows, ["consequence_id", "current_status", "consequence"])}

## Local Arena Blockers

{md_table(arena_blocker_rows, ["arena_id", "arena", "current_blocker", "arena_map_ready"])}

## Prior Trail Reconciliation

{md_table(historical_rows, ["trail_id", "prior_checkpoint", "prior_result", "current_use", "status"])}

## Decision

{md_table(decision_rows, ["decision_id", "decision", "reason", "next_action"])}

## Claim Status

{md_table(claim_rows, ["claim_id", "claim", "claim_active", "status", "reason"])}

## Next Target

{md_table(next_rows, ["next_id", "next_checkpoint", "mission", "starting_equation", "claim_policy"])}

## Validation

{md_table(validation_rows, ["validation_id", "passed", "requirement", "evidence"])}

## Files

- Source register: `{OUTPUTS["sources"]}`
- No-hypermomentum functor audit: `{OUTPUTS["functor"]}`
- DeltaGamma bound components: `{OUTPUTS["delta_bounds"]}`
- Source/readout sector split: `{OUTPUTS["sector_split"]}`
- TQ consequence ledger: `{OUTPUTS["tq_consequence"]}`
- Local arena blockers: `{OUTPUTS["arena_blockers"]}`
- Prior trail reconciliation: `{OUTPUTS["historical"]}`
- Claim status: `{OUTPUTS["claim_status"]}`
- Next target: `{OUTPUTS["next"]}`
- Validation: `{OUTPUTS["validation"]}`
- Branch copy: `{BRANCH_OUTPUTS["functor_copy"]}`
- Branch copy: `{BRANCH_OUTPUTS["delta_bounds_copy"]}`
- Branch copy: `{BRANCH_OUTPUTS["tq_consequence_copy"]}`
- Branch copy: `{BRANCH_OUTPUTS["arena_blockers_copy"]}`
- Branch copy: `{BRANCH_OUTPUTS["next_copy"]}`
"""

DOC.write_text(doc_text, encoding="utf-8")
print(f"Wrote {DOC}")
print(f"Wrote {OUTPUTS['validation']}")
print(f"Validation passed {sum(1 for row in validation_rows if row['passed'] == 'True')}/{len(validation_rows)}")

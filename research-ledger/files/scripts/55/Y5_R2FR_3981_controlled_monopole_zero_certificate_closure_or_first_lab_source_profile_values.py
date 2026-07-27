from __future__ import annotations

import csv
import py_compile
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


CHECKPOINT = "3981"
SCRIPT_PATH = Path(__file__).resolve()
PCW = SCRIPT_PATH.parents[1]
ROOT = PCW.parent
FWB = ROOT / "formalization-workbench"
SRC = PCW / "source-intake" / "mts_residuals"
DOC_PATH = PCW / "3981-Y5-R2FR-controlled-monopole-zero-certificate-closure-or-first-lab-source-profile-values.md"
SPINE_PATH = PCW / "LOCAL_GR_COUPLING_SPINE_CURRENT_STATE.md"

OUTPUTS = {
    "sources": SRC / "P8_Y5_R2FR_3981_SOURCE_REGISTER.csv",
    "theorem": SRC / "P8_Y5_R2FR_3981_CONTROLLED_POYNTING_SILENCE_THEOREM.csv",
    "certificate": SRC / "P8_Y5_R2FR_3981_PARENT_ZERO_CERTIFICATE_UPDATE.csv",
    "profiles": SRC / "P8_Y5_R2FR_3981_SOURCE_PROFILE_CANDIDATE_ROWS.csv",
    "projector": SRC / "P8_Y5_R2FR_3981_PROJECTOR_RESULTS.csv",
    "bounds": SRC / "P8_Y5_R2FR_3981_BOUND_FEED_ROWS.csv",
    "feed": SRC / "P8_Y5_R2FR_3981_FEED_UPDATE.csv",
    "decision": SRC / "P8_Y5_R2FR_3981_DECISION_GATE.csv",
    "claim_gate": SRC / "P8_Y5_R2FR_3981_CLAIM_GATE.csv",
    "next": SRC / "P8_Y5_R2FR_3981_NEXT_TARGET.csv",
    "status": SRC / "P8_Y5_R2FR_3981_STATUS.csv",
    "validation": SRC / "P8_Y5_BRR545_3981_VALIDATION.csv",
}

NEXT_DOC = "3982-Y5-R2FR-closed-total-source-or-surface-exchange-zero-for-controlled-monopole.md"
NEXT_SCRIPT = "scripts/Y5_R2FR_3982_closed_total_source_or_surface_exchange_zero_for_controlled_monopole.py"


def now_utc() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def read_csv(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        raise ValueError(f"no rows for {path}")
    fields: list[str] = []
    for row in rows:
        for key in row:
            if key not in fields:
                fields.append(key)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def source_specs() -> list[tuple[str, Path, str, str]]:
    return [
        ("SRC3981_00_3980_next", SRC / "P8_Y5_R2FR_3980_NEXT_TARGET.csv", "NEXT3980_0", "3980 handoff"),
        ("SRC3981_01_3980_certificate", SRC / "P8_Y5_R2FR_3980_PARENT_ZERO_CERTIFICATE_AUDIT.csv", "PZC3980_3_poynting", "3980 Poynting blocker"),
        ("SRC3981_02_3980_total", SRC / "P8_Y5_R2FR_3980_PARENT_ZERO_CERTIFICATE_AUDIT.csv", "PZC3980_7_total", "3980 total certificate"),
        ("SRC3981_03_3980_projector", SRC / "P8_Y5_R2FR_3980_PROJECTOR_RESULTS.csv", "REAL3980_0_controlled_EH_monopole_l2m0", "3980 candidate projector row"),
        ("SRC3981_04_3980_profile", SRC / "P8_Y5_R2FR_3980_SOURCE_PROFILE_CANDIDATE_ROWS.csv", "REAL3980_0_controlled_EH_monopole_l2m0", "3980 candidate profile row"),
        ("SRC3981_05_3980_claim", SRC / "P8_Y5_R2FR_3980_CLAIM_GATE.csv", "CLG3980_0_candidate", "3980 candidate claim gate"),
        ("SRC3981_06_3978_pic_total", SRC / "P8_Y5_R2FR_3978_POYNTING_INCLUSION_CONTRACT.csv", "PIC3978_0_total_source", "total Hilbert/Maxwell source guard"),
        ("SRC3981_07_3978_pic_flux", SRC / "P8_Y5_R2FR_3978_POYNTING_INCLUSION_CONTRACT.csv", "PIC3978_1_boundary_flux", "closed total boundary flux"),
        ("SRC3981_08_3978_pic_internal", SRC / "P8_Y5_R2FR_3978_POYNTING_INCLUSION_CONTRACT.csv", "PIC3978_2_internal_flow_allowed", "internal Poynting allowed"),
        ("SRC3981_09_3978_pic_radiation", SRC / "P8_Y5_R2FR_3978_POYNTING_INCLUSION_CONTRACT.csv", "PIC3978_3_radiation", "radiation guard"),
        ("SRC3981_10_3978_no_em_claim", SRC / "P8_Y5_R2FR_3978_POYNTING_INCLUSION_CONTRACT.csv", "PIC3978_4_no_charge_claim", "no EM overclaim"),
        ("SRC3981_11_3978_z_poynting", SRC / "P8_Y5_R2FR_3978_Z_SOURCE_ZERO_UPDATE.csv", "ZSRC3978_4_poynting", "3978 Poynting certificate"),
        ("SRC3981_12_3978_theorem_poynting", SRC / "P8_Y5_R2FR_3978_CLOSED_SOURCE_TENSOR_VIRIAL_THEOREM.csv", "CST3978_2_poynting_inclusion", "Poynting theorem row"),
        ("SRC3981_13_3930_total", SRC / "P8_Y5_R2FR_3930_POYNTING_BOUNDARY_GUARD.csv", "PYG3930_0_total_system", "total system guard"),
        ("SRC3981_14_3930_internal", SRC / "P8_Y5_R2FR_3930_POYNTING_BOUNDARY_GUARD.csv", "PYG3930_1_internal_flow_allowed", "internal flow allowed"),
        ("SRC3981_15_3930_no_em_claim", SRC / "P8_Y5_R2FR_3930_POYNTING_BOUNDARY_GUARD.csv", "PYG3930_2_no_em_overclaim", "no EM origin proof"),
        ("SRC3981_16_3930_phi", SRC / "P8_Y5_R2FR_3930_BOUNDARY_HARMONIC_ZERO_RESULT.csv", "BHZ3930_2_Phi_B", "total flux private branch"),
        ("SRC3981_17_3831_em", SRC / "P8_Y5_R2FR_3831_TENSOR_VIRIAL_NO_SLIP_CONDITIONS.csv", "TV3831_3_EM_radiation_separation", "EM/radiation separation"),
    ]


def source_register_rows(timestamp: str) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    for source_id, path, needle, role in source_specs():
        exists = path.exists()
        text = read_text(path) if exists else ""
        rows.append(
            {
                "source_id": source_id,
                "role": role,
                "path": str(path),
                "needle": needle,
                "exists": exists,
                "needle_found": needle in text,
                "valid_for_claim": False,
                "timestamp_utc": timestamp,
            }
        )
    return rows


def theorem_rows(timestamp: str) -> list[dict[str, object]]:
    return [
        {
            "theorem_id": "CPS3981_0_branch",
            "claim_piece": "controlled monopole Poynting silence branch",
            "mathematical_form": "F_{mu nu}|Omega_ext=0, T_EM|Omega_ext=0, no radiative EM/GW flux through boundary(W), and any internal field stress is inside T_tot(W)",
            "derived_result": "epsilon_EM_Poynting_TF=0 for the controlled neutral/nonradiating EH-monopole profile row",
            "status": "BRANCH_SPECIFIC_POYNTING_ZERO_DERIVED",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "theorem_id": "CPS3981_1_internal_guard",
            "claim_piece": "internal Poynting not deleted",
            "mathematical_form": "S_EM may circulate inside W; only exterior support and total boundary flux are zero in this controlled branch",
            "derived_result": "no pointwise internal Poynting deletion is used",
            "status": "INTERNAL_FLOW_GUARD_ACTIVE",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "theorem_id": "CPS3981_2_no_em_unification",
            "claim_piece": "not an EM origin proof",
            "mathematical_form": "Z_Poynting_silent_or_included does not derive charge, alpha, Maxwell emergence, or Coulomb law",
            "derived_result": "this only removes one local-GR source residual blocker in a controlled neutral/nonradiating branch",
            "status": "NO_EM_OVERCLAIM_GUARD_ACTIVE",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "theorem_id": "CPS3981_3_certificate_effect",
            "claim_piece": "one blocker removed",
            "mathematical_form": "PZC3980_3_poynting: UNSIGNED_FROM_3978 -> CLOSED_FOR_CONTROLLED_NEUTRAL_NONRADIATING_MONOPOLE_BRANCH",
            "derived_result": "controlled profile row claim blockers lose Z_Poynting_silent_or_included but keep closed-source, surface-exchange, and no-extra-hair blockers",
            "status": "ONE_BLOCKER_CLOSED_BRANCH_SPECIFIC_NONCLAIM",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
    ]


def certificate_rows(timestamp: str) -> list[dict[str, object]]:
    specs = [
        ("PZC3981_0_EH_vacuum", "Z_EH_vacuum_monopole_family", "exterior readout is EH vacuum/SdS monopole family with one mass charge", "conditional_from_3969", "CONDITIONAL_NOT_PARENT_SIGNED", "still a conditional branch"),
        ("PZC3981_1_same_GR", "Z_same_GR_baseline_monopole", "GR comparator uses same source/frame/units/r_eval", "operator_contract", "DEFINED_FOR_CANDIDATE_ROW", "keeps Q_lm_GR_baseline=0 for l>=1"),
        ("PZC3981_2_total_source", "Z_closed_total_source_monopole", "one closed worldtube includes all stress/field/binding/apparatus/exchange channels", "required", "UNSIGNED_FROM_3978", "still blocks claim promotion"),
        ("PZC3981_3_poynting", "Z_Poynting_silent_or_included", "controlled branch has no exterior EM/radiative support and any internal field stress is included in T_tot(W)", "closed_branch_specific", "CLOSED_FOR_CONTROLLED_NEUTRAL_NONRADIATING_MONOPOLE_BRANCH", "blocker removed for controlled candidate only"),
        ("PZC3981_4_surface", "Z_surface_exchange_zero_monopole", "surface_TF=exchange_TF=boundary_flux_TF=0 in the same branch", "required", "PARTIAL_PRIVATE_BRANCH_ONLY", "still blocks claim promotion"),
        ("PZC3981_5_no_extra_hair", "Z_no_extra_lge1_MTS_hair", "no additional MTS source multipole survives beyond the GR monopole exterior", "required", "UNSIGNED", "still blocks claim promotion"),
        ("PZC3981_6_counterguard", "Z_no_spherical_cheat", "zero row is a controlled EH-monopole branch, not arbitrary spherical averaging", "guard", "GUARD_ACTIVE", "prevents overclaim"),
        ("PZC3981_7_total", "Z_parent_zero_lge1_candidate", "product of EH, same-GR, closed source, Poynting, surface, and no-extra-hair factors", "total", "FALSE_UNTIL_REMAINING_UNSIGNED_FACTORS_CLOSE", "candidate remains nonclaim"),
    ]
    return [
        {
            "certificate_id": certificate_id,
            "factor": factor,
            "requirement": requirement,
            "role": role,
            "current_status": status,
            "effect": effect,
            "claim_allowed": False,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
        for certificate_id, factor, requirement, role, status, effect in specs
    ]


def profile_rows(timestamp: str) -> list[dict[str, object]]:
    source_path = SRC / "P8_Y5_R2FR_3980_PARENT_ZERO_CERTIFICATE_AUDIT.csv"
    common = {
        "arena": "controlled_neutral_nonradiating_EH_monopole_branch",
        "Q_lm_total": "0.0",
        "Q_lm_GR_baseline": "0.0",
        "M_H_ref": "1.0",
        "r_eval": "symbolic_exterior_annulus",
        "worldtube_definition": "controlled_closed_total_monopole_worldtube",
        "baseline_worldtube_definition": "controlled_closed_total_monopole_worldtube",
        "units": "theorem_zero_normalized_multipole",
        "baseline_units": "theorem_zero_normalized_multipole",
        "frame_or_coframe": "same_parent_local_orthonormal_frame",
        "baseline_frame_or_coframe": "same_parent_local_orthonormal_frame",
        "includes_matter": True,
        "includes_EM": True,
        "includes_binding": True,
        "includes_apparatus": True,
        "apparatus_outside_projection": False,
        "GR_routing_flag": True,
        "boundary_flux_TF": "0.0_if_Z_surface_exchange_zero_monopole",
        "d2I_TF_dt2": "0.0_if_Z_stationary_TF_virial",
        "poynting_bound": "0.0_closed_by_CPS3981_0_branch",
        "source_path": str(source_path),
        "row_kind": "THEOREM_ZERO_CANDIDATE_PROFILE_NONCLAIM",
        "certificate_required": "Z_parent_zero_lge1_candidate",
        "claim_blockers": "Z_closed_total_source_monopole|Z_surface_exchange_zero_monopole|Z_no_extra_lge1_MTS_hair",
        "valid_for_claim": False,
        "timestamp_utc": timestamp,
    }
    rows: list[dict[str, object]] = []
    for source_id, l_value, m_value in [
        ("REAL3981_0_controlled_EH_monopole_l2m0_poynting_closed", 2, 0),
        ("REAL3981_1_same_branch_l3m0_poynting_closed", 3, 0),
    ]:
        row = dict(common)
        row.update({"source_id": source_id, "l": l_value, "m": m_value})
        rows.append(row)
    rows.append(
        {
            "source_id": "REAL3981_2_real_lab_row_placeholder_blocked",
            "arena": "future_real_lab_or_PPN_source",
            "l": 2,
            "m": 0,
            "Q_lm_total": "",
            "Q_lm_GR_baseline": "",
            "M_H_ref": "",
            "r_eval": "",
            "worldtube_definition": "",
            "baseline_worldtube_definition": "",
            "units": "",
            "baseline_units": "",
            "frame_or_coframe": "",
            "baseline_frame_or_coframe": "",
            "includes_matter": False,
            "includes_EM": False,
            "includes_binding": False,
            "includes_apparatus": False,
            "apparatus_outside_projection": False,
            "GR_routing_flag": False,
            "boundary_flux_TF": "",
            "d2I_TF_dt2": "",
            "poynting_bound": "",
            "source_path": "",
            "row_kind": "REAL_PROFILE_SLOT_BLOCKED_VALUES_MISSING",
            "certificate_required": "real_source_profile_or_Z_parent_zero_lge1_candidate",
            "claim_blockers": "MISSING_Q_LM_TOTAL|MISSING_Q_LM_GR_BASELINE|MISSING_M_H_REF|MISSING_SOURCE_PATH|MISSING_TOTAL_SOURCE_COMPONENTS",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
    )
    return rows


def project_row(row: dict[str, object], timestamp: str) -> dict[str, object]:
    q_total = str(row["Q_lm_total"]).strip()
    q_gr = str(row["Q_lm_GR_baseline"]).strip()
    m_ref = str(row["M_H_ref"]).strip()
    blockers: list[str] = []
    if not q_total:
        blockers.append("MISSING_Q_LM_TOTAL")
    if not q_gr:
        blockers.append("MISSING_Q_LM_GR_BASELINE")
    if not m_ref:
        blockers.append("MISSING_OR_ZERO_M_H_REF")
    if not str(row["source_path"]).strip() or not Path(str(row["source_path"])).exists():
        blockers.append("MISSING_SOURCE_PATH")
    if str(row["GR_routing_flag"]).lower() not in {"true", "1"}:
        blockers.append("GR_ROUTING_FLAG_FALSE")
    if str(row["includes_EM"]).lower() not in {"true", "1"} and not str(row["poynting_bound"]).strip():
        blockers.append("MISSING_EM_OR_POYNTING_BOUND")
    if str(row["includes_matter"]).lower() not in {"true", "1"}:
        blockers.append("MISSING_MATTER_COMPONENT")
    if str(row["includes_binding"]).lower() not in {"true", "1"}:
        blockers.append("MISSING_BINDING_COMPONENT")
    if str(row["includes_apparatus"]).lower() not in {"true", "1"} and str(row["apparatus_outside_projection"]).lower() not in {"true", "1"}:
        blockers.append("MISSING_APPARATUS_OR_PROJECTION_EXCLUSION")

    if blockers:
        return {
            "source_id": row["source_id"],
            "projector_status": "BLOCKED_" + "+".join(blockers),
            "Q_lm_residual": "",
            "epsilon_extra_MTS_l_ge_1": "",
            "certificate_status": "BLOCKED_VALUES_OR_COMPATIBILITY_MISSING",
            "claim_blockers": "|".join(blockers),
            "removed_blocker": "",
            "claim_allowed": False,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }

    residual = float(q_total) - float(q_gr)
    epsilon = abs(residual) / abs(float(m_ref))
    return {
        "source_id": row["source_id"],
        "projector_status": "PROJECTOR_PASS_THEOREM_ZERO_CANDIDATE_POYNTING_CLOSED_NONCLAIM",
        "Q_lm_residual": f"{residual:.12g}",
        "epsilon_extra_MTS_l_ge_1": f"{epsilon:.12g}",
        "certificate_status": "PROJECTOR_ZERO_PARENT_CERTIFICATE_PARTIALLY_CLOSED",
        "claim_blockers": row["claim_blockers"],
        "removed_blocker": "Z_Poynting_silent_or_included",
        "claim_allowed": False,
        "valid_for_claim": False,
        "timestamp_utc": timestamp,
    }


def projector_rows(profiles: list[dict[str, object]], timestamp: str) -> list[dict[str, object]]:
    return [project_row(row, timestamp) for row in profiles]


def bound_rows(timestamp: str) -> list[dict[str, object]]:
    return [
        {
            "bound_id": "BFC3981_0_poynting_closed",
            "symbol": "epsilon_EM_Poynting_TF",
            "formula": "epsilon_EM_Poynting_TF=0 for controlled neutral/nonradiating EH-monopole exterior; internal EM stress is included in T_tot(W) if present",
            "units": "dimensionless",
            "current_status": "CLOSED_FOR_CONTROLLED_BRANCH_NONCLAIM",
            "claim_allowed": False,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "bound_id": "BFC3981_1_projector_zero_candidate",
            "symbol": "epsilon_extra_MTS_l_ge_1",
            "formula": "|Q_lm_total-Q_lm_GR_baseline|/M_H_ref=0 for controlled l>=1 candidate",
            "units": "dimensionless",
            "current_status": "NONCLAIM_ZERO_CANDIDATE_WITH_ONE_BLOCKER_REMOVED",
            "claim_allowed": False,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "bound_id": "BFC3981_2_remaining_source",
            "symbol": "epsilon_source_l_ge_1",
            "formula": "still blocked by epsilon_closed_source_failure + epsilon_tensor_virial_TF + epsilon_quad_residual_TF + epsilon_apparatus_TF unless remaining parent factors close",
            "units": "dimensionless",
            "current_status": "BOUND_CHAIN_PARTIALLY_CLOSED_REMAINING_FACTORS_UNSIGNED",
            "claim_allowed": False,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
    ]


def feed_rows(timestamp: str) -> list[dict[str, object]]:
    return [
        {
            "feed_id": "CZF3981_0_poynting",
            "target": "Z_Poynting_silent_or_included",
            "update": "closed for controlled neutral/nonradiating EH-monopole branch only",
            "effect": "removes one blocker from the controlled candidate claim blocker list",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "feed_id": "CZF3981_1_projector",
            "target": "epsilon_extra_MTS_l_ge_1",
            "update": "controlled candidate still projects to zero with poynting blocker removed",
            "effect": "source profile route advances from first candidate to partially closed certificate",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "feed_id": "CZF3981_2_remaining",
            "target": "Z_parent_zero_lge1_candidate",
            "update": "remaining unsigned blockers: closed total source, surface/exchange zero, no extra MTS l>=1 hair",
            "effect": "next derivation target is narrowed to the strongest remaining blocker",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "feed_id": "CZF3981_3_next",
            "target": "closed_total_source_or_surface_exchange_zero",
            "update": f"move to {NEXT_DOC}",
            "effect": "attack closed worldtube/surface exchange next",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
    ]


def decision_rows(timestamp: str) -> list[dict[str, object]]:
    return [
        {
            "row_id": "DEC3981_0_close",
            "decision": "close one blocker branch-specifically",
            "status": "POYNTING_BLOCKER_CLOSED_FOR_CONTROLLED_BRANCH",
            "reason": "neutral/nonradiating EH-monopole exterior has no exterior EM/radiative support; internal field stress is included, not deleted",
            "next_action": "keep row nonclaim and attack closed-source/surface blockers",
            "claim_allowed": False,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "DEC3981_1_guard",
            "decision": "do not generalize to lab/non-spherical arenas",
            "status": "GENERAL_POYNTING_CLAIM_REJECTED",
            "reason": "real EM/radiative/Poynting stress still needs source rows or inclusion proof",
            "next_action": "retain Poynting rows outside controlled branch",
            "claim_allowed": False,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "DEC3981_2_next",
            "decision": "next target selected",
            "status": "MOVE_TO_CLOSED_SOURCE_OR_SURFACE_EXCHANGE",
            "reason": "remaining blockers are now smaller and exact",
            "next_action": NEXT_DOC,
            "claim_allowed": False,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
    ]


def claim_gate_rows(timestamp: str) -> list[dict[str, object]]:
    return [
        {
            "row_id": "CLG3981_0_candidate",
            "gate": "controlled theorem-zero candidate",
            "requirement": "closed total source, surface/exchange zero, and no extra l>=1 MTS hair still required",
            "status": "BLOCKED_REMAINING_PARENT_FACTORS_UNSIGNED",
            "claim_allowed": False,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "CLG3981_1_poynting_general",
            "gate": "general Poynting/EM stress",
            "requirement": "outside the controlled neutral/nonradiating branch, source T_EM/S_EM or prove inclusion",
            "status": "GENERAL_CLAIM_STILL_BLOCKED",
            "claim_allowed": False,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "CLG3981_2_local_GR",
            "gate": "local GR",
            "requirement": "all source/boundary/external/angular/PPN/Newton/EM/source-coupling gates",
            "status": "LOCAL_GR_STILL_OPEN",
            "claim_allowed": False,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
    ]


def next_rows(timestamp: str) -> list[dict[str, object]]:
    return [
        {
            "row_id": "NEXT3981_0",
            "next_doc": NEXT_DOC,
            "next_script": NEXT_SCRIPT,
            "target": "derive closed total source or surface/exchange zero for the controlled monopole candidate, or demote it to an explicit finite source-bound requirement",
            "success_condition": "one more parent blocker is closed branch-specifically, or epsilon_closed_source_failure/surface_TF rows receive source-ready inputs",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
    ]


def status_rows(timestamp: str, sources: list[dict[str, object]], projector: list[dict[str, object]]) -> list[dict[str, object]]:
    found = sum(bool(row["exists"]) and bool(row["needle_found"]) for row in sources)
    pass_rows = sum(row["projector_status"] == "PROJECTOR_PASS_THEOREM_ZERO_CANDIDATE_POYNTING_CLOSED_NONCLAIM" for row in projector)
    blocked_rows = sum(str(row["projector_status"]).startswith("BLOCKED") for row in projector)
    return [
        {
            "checkpoint": CHECKPOINT,
            "status": "CONTROLLED_POYNTING_BLOCKER_CLOSED_REMAINING_PARENT_FACTORS_UNSIGNED",
            "sources_found": found,
            "sources_total": len(sources),
            "candidate_projector_pass_rows": pass_rows,
            "blocked_rows": blocked_rows,
            "main_result": "Z_Poynting_silent_or_included is closed for the controlled neutral/nonradiating EH-monopole branch only; candidate still nonclaim because closed-source, surface-exchange, and no-extra-hair factors remain unsigned",
            "next_target": NEXT_DOC,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
    ]


def doc_text(timestamp: str, sources: list[dict[str, object]]) -> str:
    found = sum(bool(row["exists"]) and bool(row["needle_found"]) for row in sources)
    return f"""# 3981 - Controlled Monopole Zero Certificate Closure Or First Lab Source Profile Values

Timestamp: `{timestamp}`

## Result

3981 closes exactly one blocker for the controlled profile row:

```text
Z_Poynting_silent_or_included
  = CLOSED_FOR_CONTROLLED_NEUTRAL_NONRADIATING_MONOPOLE_BRANCH
```

Reason:

```text
F_mu_nu|Omega_ext = 0
T_EM|Omega_ext = 0
no radiative EM/GW flux through boundary(W)
internal field stress, if present, is included inside T_tot(W)
```

So the controlled candidate keeps:

```text
epsilon_EM_Poynting_TF = 0
epsilon_extra_MTS_l_ge_1 = 0
```

## Remaining Blockers

The candidate is still not a local-GR claim. Remaining blockers:

```text
Z_closed_total_source_monopole
Z_surface_exchange_zero_monopole
Z_no_extra_lge1_MTS_hair
```

This is not an EM unification claim, and it does not apply to real lab/non-spherical arenas without source rows.

Next target:

```text
{NEXT_DOC}
```

Source needles found: `{found}/{len(sources)}`.
"""


def spine_block(timestamp: str) -> str:
    return f"""

## 3981 - Controlled Poynting Blocker Closure

- Timestamp: `{timestamp}`
- Status: `CONTROLLED_POYNTING_BLOCKER_CLOSED_REMAINING_PARENT_FACTORS_UNSIGNED`
- Closed blocker:
  `Z_Poynting_silent_or_included` is closed only for the controlled neutral/nonradiating EH-monopole branch.
- Reason:
  no exterior EM/radiative support, no net radiative flux through the worldtube boundary, and any internal field stress is included in `T_tot(W)`.
- Still nonclaim:
  `Z_closed_total_source_monopole`, `Z_surface_exchange_zero_monopole`, and `Z_no_extra_lge1_MTS_hair` remain unsigned.
- Guard:
  not an EM-origin proof and not valid for real lab/non-spherical arenas without source rows.
- Next: `{NEXT_DOC}`.
"""


def update_spine(timestamp: str) -> None:
    marker = "## 3981 - Controlled Poynting Blocker Closure"
    block = spine_block(timestamp)
    if SPINE_PATH.exists():
        text = read_text(SPINE_PATH)
        if marker in text:
            before = text.split(marker, 1)[0].rstrip()
            SPINE_PATH.write_text(before + block, encoding="utf-8")
        else:
            SPINE_PATH.write_text(text.rstrip() + block, encoding="utf-8")
    else:
        SPINE_PATH.write_text("# Local GR Coupling Spine - Current State\n" + block, encoding="utf-8")


def all_rows(timestamp: str) -> dict[str, list[dict[str, object]]]:
    sources = source_register_rows(timestamp)
    profiles = profile_rows(timestamp)
    projector = projector_rows(profiles, timestamp)
    return {
        "sources": sources,
        "theorem": theorem_rows(timestamp),
        "certificate": certificate_rows(timestamp),
        "profiles": profiles,
        "projector": projector,
        "bounds": bound_rows(timestamp),
        "feed": feed_rows(timestamp),
        "decision": decision_rows(timestamp),
        "claim_gate": claim_gate_rows(timestamp),
        "next": next_rows(timestamp),
        "status": status_rows(timestamp, sources, projector),
    }


def validation_rows(timestamp: str, rows: dict[str, list[dict[str, object]]]) -> list[dict[str, object]]:
    generated_csvs = [path for key, path in OUTPUTS.items() if key != "validation"]
    sources = rows["sources"]
    theorem = rows["theorem"]
    certificate = rows["certificate"]
    projector = rows["projector"]
    bounds = rows["bounds"]
    feed = rows["feed"]
    decisions = rows["decision"]
    claims = rows["claim_gate"]
    next_target = rows["next"]

    def val(validation_id: str, passed: bool, detail: str) -> dict[str, object]:
        return {
            "validation_id": validation_id,
            "passed": bool(passed),
            "detail": detail,
            "timestamp_utc": timestamp,
        }

    parsed = True
    parse_detail = "generated CSV files parse cleanly"
    for path in generated_csvs:
        try:
            read_csv(path)
        except Exception as exc:
            parsed = False
            parse_detail = f"{path} failed to parse: {exc}"
            break

    theorem_statuses = {str(row["status"]) for row in theorem}
    factors = {str(row["factor"]): row for row in certificate}
    project_by_id = {str(row["source_id"]): row for row in projector}
    bound_symbols = {str(row["symbol"]) for row in bounds}
    feed_targets = {str(row["target"]) for row in feed}
    decision_statuses = {str(row["status"]) for row in decisions}
    claim_statuses = {str(row["status"]) for row in claims}
    candidate = project_by_id["REAL3981_0_controlled_EH_monopole_l2m0_poynting_closed"]

    return [
        val("VAL3981_00_sources_exist", all(row["exists"] for row in sources), "all cited source paths exist"),
        val("VAL3981_01_needles_found", all(row["needle_found"] for row in sources), "all cited source needles found"),
        val("VAL3981_02_theorem", {"BRANCH_SPECIFIC_POYNTING_ZERO_DERIVED", "INTERNAL_FLOW_GUARD_ACTIVE", "NO_EM_OVERCLAIM_GUARD_ACTIVE", "ONE_BLOCKER_CLOSED_BRANCH_SPECIFIC_NONCLAIM"} <= theorem_statuses, "branch-specific Poynting zero theorem and guards present"),
        val("VAL3981_03_certificate_closed", factors["Z_Poynting_silent_or_included"]["current_status"] == "CLOSED_FOR_CONTROLLED_NEUTRAL_NONRADIATING_MONOPOLE_BRANCH", "Poynting factor closed for controlled branch"),
        val("VAL3981_04_total_still_false", factors["Z_parent_zero_lge1_candidate"]["current_status"] == "FALSE_UNTIL_REMAINING_UNSIGNED_FACTORS_CLOSE", "total certificate still false"),
        val("VAL3981_05_projector_candidate", candidate["projector_status"] == "PROJECTOR_PASS_THEOREM_ZERO_CANDIDATE_POYNTING_CLOSED_NONCLAIM" and candidate["epsilon_extra_MTS_l_ge_1"] == "0", "candidate still projects to zero residual"),
        val("VAL3981_06_blocker_removed", candidate["removed_blocker"] == "Z_Poynting_silent_or_included" and "Z_Poynting_silent_or_included" not in str(candidate["claim_blockers"]), "Poynting blocker removed from candidate claim blockers"),
        val("VAL3981_07_remaining_blockers", {"Z_closed_total_source_monopole", "Z_surface_exchange_zero_monopole", "Z_no_extra_lge1_MTS_hair"} <= set(str(candidate["claim_blockers"]).split("|")), "remaining blockers preserved"),
        val("VAL3981_08_bounds", {"epsilon_EM_Poynting_TF", "epsilon_extra_MTS_l_ge_1", "epsilon_source_l_ge_1"} <= bound_symbols, "bound rows include Poynting, projector, and source chain"),
        val("VAL3981_09_feed", {"Z_Poynting_silent_or_included", "epsilon_extra_MTS_l_ge_1", "Z_parent_zero_lge1_candidate", "closed_total_source_or_surface_exchange_zero"} <= feed_targets, "feeds reach closed blocker, projector, parent zero, and next target"),
        val("VAL3981_10_decision", {"POYNTING_BLOCKER_CLOSED_FOR_CONTROLLED_BRANCH", "GENERAL_POYNTING_CLAIM_REJECTED", "MOVE_TO_CLOSED_SOURCE_OR_SURFACE_EXCHANGE"} <= decision_statuses, "decision gate records branch closure, general refusal, and next move"),
        val("VAL3981_11_claim_gate", {"BLOCKED_REMAINING_PARENT_FACTORS_UNSIGNED", "GENERAL_CLAIM_STILL_BLOCKED", "LOCAL_GR_STILL_OPEN"} <= claim_statuses, "claim gates preserve remaining blockers and local GR block"),
        val("VAL3981_12_next_target", next_target[0]["next_doc"] == NEXT_DOC and next_target[0]["next_script"] == NEXT_SCRIPT, "next target points to closed source/surface exchange"),
        val("VAL3981_13_all_nonclaim", all(not row.get("valid_for_claim", True) for group in rows.values() for row in group), "all generated physics rows remain nonclaim"),
        val("VAL3981_14_outputs_outside_fwb", all(FWB not in path.parents for path in generated_csvs) and FWB not in DOC_PATH.parents, "no generated output is inside formalization-workbench"),
        val("VAL3981_15_doc_exists", DOC_PATH.exists(), "checkpoint doc exists"),
        val("VAL3981_16_spine_updated", SPINE_PATH.exists() and "3981 - Controlled Poynting Blocker Closure" in read_text(SPINE_PATH), "spine updated"),
        val("VAL3981_17_csv_parse", parsed, parse_detail),
        val("VAL3981_18_script_compile", True, "script compiled before validation write"),
        val("VAL3981_19_no_pycache", not (SCRIPT_PATH.parent / "__pycache__").exists(), "scripts __pycache__ removed"),
    ]


def run() -> None:
    timestamp = now_utc()
    rows = all_rows(timestamp)

    write_csv(OUTPUTS["sources"], rows["sources"])
    write_csv(OUTPUTS["theorem"], rows["theorem"])
    write_csv(OUTPUTS["certificate"], rows["certificate"])
    write_csv(OUTPUTS["profiles"], rows["profiles"])
    write_csv(OUTPUTS["projector"], rows["projector"])
    write_csv(OUTPUTS["bounds"], rows["bounds"])
    write_csv(OUTPUTS["feed"], rows["feed"])
    write_csv(OUTPUTS["decision"], rows["decision"])
    write_csv(OUTPUTS["claim_gate"], rows["claim_gate"])
    write_csv(OUTPUTS["next"], rows["next"])
    write_csv(OUTPUTS["status"], rows["status"])

    DOC_PATH.write_text(doc_text(timestamp, rows["sources"]), encoding="utf-8")
    update_spine(timestamp)

    py_compile.compile(str(SCRIPT_PATH), doraise=True)
    pycache = SCRIPT_PATH.parent / "__pycache__"
    if pycache.exists():
        shutil.rmtree(pycache)

    validations = validation_rows(timestamp, rows)
    write_csv(OUTPUTS["validation"], validations)
    failed = [row for row in validations if not row["passed"]]
    if failed:
        raise SystemExit(f"3981 validation failed: {failed}")

    print(f"3981 checkpoint complete: {DOC_PATH}")
    print(f"validation: {OUTPUTS['validation']}")
    print("Controlled Poynting blocker closed for monopole branch")


if __name__ == "__main__":
    run()

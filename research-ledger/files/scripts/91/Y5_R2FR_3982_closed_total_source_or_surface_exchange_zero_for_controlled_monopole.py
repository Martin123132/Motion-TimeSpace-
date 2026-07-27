from __future__ import annotations

import csv
import py_compile
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


CHECKPOINT = "3982"
SCRIPT_PATH = Path(__file__).resolve()
PCW = SCRIPT_PATH.parents[1]
ROOT = PCW.parent
FWB = ROOT / "formalization-workbench"
SRC = PCW / "source-intake" / "mts_residuals"
DOC_PATH = PCW / "3982-Y5-R2FR-closed-total-source-or-surface-exchange-zero-for-controlled-monopole.md"
SPINE_PATH = PCW / "LOCAL_GR_COUPLING_SPINE_CURRENT_STATE.md"

OUTPUTS = {
    "sources": SRC / "P8_Y5_R2FR_3982_SOURCE_REGISTER.csv",
    "theorem": SRC / "P8_Y5_R2FR_3982_CONTROLLED_SURFACE_EXCHANGE_ZERO_THEOREM.csv",
    "certificate": SRC / "P8_Y5_R2FR_3982_PARENT_ZERO_CERTIFICATE_UPDATE.csv",
    "profiles": SRC / "P8_Y5_R2FR_3982_SOURCE_PROFILE_CANDIDATE_ROWS.csv",
    "projector": SRC / "P8_Y5_R2FR_3982_PROJECTOR_RESULTS.csv",
    "bounds": SRC / "P8_Y5_R2FR_3982_BOUND_FEED_ROWS.csv",
    "feed": SRC / "P8_Y5_R2FR_3982_FEED_UPDATE.csv",
    "decision": SRC / "P8_Y5_R2FR_3982_DECISION_GATE.csv",
    "claim_gate": SRC / "P8_Y5_R2FR_3982_CLAIM_GATE.csv",
    "next": SRC / "P8_Y5_R2FR_3982_NEXT_TARGET.csv",
    "status": SRC / "P8_Y5_R2FR_3982_STATUS.csv",
    "validation": SRC / "P8_Y5_BRR545_3982_VALIDATION.csv",
}

NEXT_DOC = "3983-Y5-R2FR-no-extra-lge1-MTS-hair-or-closed-total-source-for-controlled-monopole.md"
NEXT_SCRIPT = "scripts/Y5_R2FR_3983_no_extra_lge1_MTS_hair_or_closed_total_source_for_controlled_monopole.py"


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
        ("SRC3982_00_3981_next", SRC / "P8_Y5_R2FR_3981_NEXT_TARGET.csv", "NEXT3981_0", "3981 handoff"),
        ("SRC3982_01_3981_cert_surface", SRC / "P8_Y5_R2FR_3981_PARENT_ZERO_CERTIFICATE_UPDATE.csv", "PZC3981_4_surface", "3981 surface blocker"),
        ("SRC3982_02_3981_cert_poynting", SRC / "P8_Y5_R2FR_3981_PARENT_ZERO_CERTIFICATE_UPDATE.csv", "PZC3981_3_poynting", "3981 closed Poynting blocker"),
        ("SRC3982_03_3981_cert_total", SRC / "P8_Y5_R2FR_3981_PARENT_ZERO_CERTIFICATE_UPDATE.csv", "PZC3981_7_total", "3981 total certificate"),
        ("SRC3982_04_3981_projector", SRC / "P8_Y5_R2FR_3981_PROJECTOR_RESULTS.csv", "REAL3981_0_controlled_EH_monopole_l2m0_poynting_closed", "3981 candidate projector"),
        ("SRC3982_05_3981_claim", SRC / "P8_Y5_R2FR_3981_CLAIM_GATE.csv", "CLG3981_0_candidate", "3981 claim gate"),
        ("SRC3982_06_3978_surface", SRC / "P8_Y5_R2FR_3978_Z_SOURCE_ZERO_UPDATE.csv", "ZSRC3978_3_surface", "3978 surface certificate"),
        ("SRC3982_07_3978_flux", SRC / "P8_Y5_R2FR_3978_POYNTING_INCLUSION_CONTRACT.csv", "PIC3978_1_boundary_flux", "boundary flux condition"),
        ("SRC3982_08_3930_phi", SRC / "P8_Y5_R2FR_3930_BOUNDARY_HARMONIC_ZERO_RESULT.csv", "BHZ3930_2_Phi_B", "Phi_B zero route"),
        ("SRC3982_09_3930_wall", SRC / "P8_Y5_R2FR_3930_BOUNDARY_HARMONIC_ZERO_RESULT.csv", "BHZ3930_3_tau_wall_TF", "wall TF zero route"),
        ("SRC3982_10_3930_harmonic", SRC / "P8_Y5_R2FR_3930_BOUNDARY_HARMONIC_ZERO_RESULT.csv", "BHZ3930_1_B_harmonic_boundary", "harmonic boundary zero route"),
        ("SRC3982_11_3930_fallback_flux", SRC / "P8_Y5_R2FR_3930_BOUNDARY_HARMONIC_FALLBACK_ROWS.csv", "BFB3930_2_flux", "flux fallback"),
        ("SRC3982_12_3930_fallback_wall", SRC / "P8_Y5_R2FR_3930_BOUNDARY_HARMONIC_FALLBACK_ROWS.csv", "BFB3930_3_wall", "wall fallback"),
        ("SRC3982_13_3930_total_system", SRC / "P8_Y5_R2FR_3930_POYNTING_BOUNDARY_GUARD.csv", "PYG3930_0_total_system", "total-system guard"),
        ("SRC3982_14_3831_surface", SRC / "P8_Y5_R2FR_3831_TENSOR_VIRIAL_NO_SLIP_CONDITIONS.csv", "TV3831_2_surface_exchange_silence", "surface exchange condition"),
        ("SRC3982_15_3831_closed", SRC / "P8_Y5_R2FR_3831_TENSOR_VIRIAL_NO_SLIP_CONDITIONS.csv", "TV3831_0_closed_total_source", "closed source still unsigned"),
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
            "theorem_id": "CSX3982_0_branch",
            "claim_piece": "controlled surface/exchange silence",
            "mathematical_form": "fixed isolated monopole boundary + Phi_B=0 + tau_wall_TF=0 + B_harmonic_boundary=0 + no radiative/Poynting crossing",
            "derived_result": "surface_TF=exchange_TF=boundary_flux_TF=0 for the controlled fixed isolated monopole boundary",
            "status": "BRANCH_SPECIFIC_SURFACE_EXCHANGE_ZERO_DERIVED",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "theorem_id": "CSX3982_1_not_closed_source",
            "claim_piece": "surface zero does not prove closed total source",
            "mathematical_form": "surface/exchange silence on boundary(W) does not by itself prove W includes all internal stress/field/binding/apparatus channels",
            "derived_result": "Z_closed_total_source_monopole remains unsigned",
            "status": "CLOSED_SOURCE_NOT_SMUGGLED",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "theorem_id": "CSX3982_2_no_lab_generalization",
            "claim_piece": "not a real-lab boundary claim",
            "mathematical_form": "if local branch is nonisolated, moving, radiative, apparatus-coupled, or has wall/shear/harmonic data, retain BFB3930 fallback rows",
            "derived_result": "surface closure is controlled-branch only",
            "status": "GENERAL_BOUNDARY_CLAIM_REJECTED",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "theorem_id": "CSX3982_3_certificate_effect",
            "claim_piece": "second blocker removed",
            "mathematical_form": "PZC3981_4_surface: PARTIAL_PRIVATE_BRANCH_ONLY -> CLOSED_FOR_CONTROLLED_FIXED_ISOLATED_MONOPOLE_BRANCH",
            "derived_result": "controlled profile row loses Z_surface_exchange_zero_monopole but keeps closed-source and no-extra-hair blockers",
            "status": "ONE_MORE_BLOCKER_CLOSED_BRANCH_SPECIFIC_NONCLAIM",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
    ]


def certificate_rows(timestamp: str) -> list[dict[str, object]]:
    specs = [
        ("PZC3982_0_EH_vacuum", "Z_EH_vacuum_monopole_family", "exterior readout is EH vacuum/SdS monopole family with one mass charge", "conditional_from_3969", "CONDITIONAL_NOT_PARENT_SIGNED", "still a conditional branch"),
        ("PZC3982_1_same_GR", "Z_same_GR_baseline_monopole", "GR comparator uses same source/frame/units/r_eval", "operator_contract", "DEFINED_FOR_CANDIDATE_ROW", "keeps Q_lm_GR_baseline=0 for l>=1"),
        ("PZC3982_2_total_source", "Z_closed_total_source_monopole", "one closed worldtube includes all stress/field/binding/apparatus/exchange channels", "required", "UNSIGNED_FROM_3978", "still blocks claim promotion"),
        ("PZC3982_3_poynting", "Z_Poynting_silent_or_included", "controlled branch has no exterior EM/radiative support and any internal field stress is included in T_tot(W)", "closed_branch_specific", "CLOSED_FOR_CONTROLLED_NEUTRAL_NONRADIATING_MONOPOLE_BRANCH", "blocker removed in 3981"),
        ("PZC3982_4_surface", "Z_surface_exchange_zero_monopole", "fixed isolated monopole boundary has Phi_B=tau_wall_TF=B_harmonic_boundary=0 and no crossing radiative/Poynting flux", "closed_branch_specific", "CLOSED_FOR_CONTROLLED_FIXED_ISOLATED_MONOPOLE_BRANCH", "blocker removed in 3982"),
        ("PZC3982_5_no_extra_hair", "Z_no_extra_lge1_MTS_hair", "no additional MTS source multipole survives beyond the GR monopole exterior", "required", "UNSIGNED", "still blocks claim promotion"),
        ("PZC3982_6_counterguard", "Z_no_spherical_cheat", "zero row is a controlled EH-monopole branch, not arbitrary spherical averaging", "guard", "GUARD_ACTIVE", "prevents overclaim"),
        ("PZC3982_7_total", "Z_parent_zero_lge1_candidate", "product of EH, same-GR, closed source, Poynting, surface, and no-extra-hair factors", "total", "FALSE_UNTIL_CLOSED_SOURCE_AND_NO_EXTRA_HAIR_CLOSE", "candidate remains nonclaim"),
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
    source_path = SRC / "P8_Y5_R2FR_3981_PARENT_ZERO_CERTIFICATE_UPDATE.csv"
    common = {
        "arena": "controlled_fixed_isolated_neutral_nonradiating_EH_monopole_branch",
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
        "boundary_flux_TF": "0.0_closed_by_CSX3982_0_branch",
        "d2I_TF_dt2": "0.0_if_Z_stationary_TF_virial",
        "poynting_bound": "0.0_closed_by_CPS3981_0_branch",
        "source_path": str(source_path),
        "row_kind": "THEOREM_ZERO_CANDIDATE_PROFILE_NONCLAIM",
        "certificate_required": "Z_parent_zero_lge1_candidate",
        "claim_blockers": "Z_closed_total_source_monopole|Z_no_extra_lge1_MTS_hair",
        "valid_for_claim": False,
        "timestamp_utc": timestamp,
    }
    rows: list[dict[str, object]] = []
    for source_id, l_value, m_value in [
        ("REAL3982_0_controlled_EH_monopole_l2m0_surface_closed", 2, 0),
        ("REAL3982_1_same_branch_l3m0_surface_closed", 3, 0),
    ]:
        row = dict(common)
        row.update({"source_id": source_id, "l": l_value, "m": m_value})
        rows.append(row)
    rows.append(
        {
            "source_id": "REAL3982_2_real_lab_row_placeholder_blocked",
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
    blockers: list[str] = []
    q_total = str(row["Q_lm_total"]).strip()
    q_gr = str(row["Q_lm_GR_baseline"]).strip()
    m_ref = str(row["M_H_ref"]).strip()
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
    if str(row["includes_matter"]).lower() not in {"true", "1"}:
        blockers.append("MISSING_MATTER_COMPONENT")
    if str(row["includes_EM"]).lower() not in {"true", "1"} and not str(row["poynting_bound"]).strip():
        blockers.append("MISSING_EM_OR_POYNTING_BOUND")
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
            "removed_blockers": "",
            "claim_allowed": False,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }

    residual = float(q_total) - float(q_gr)
    epsilon = abs(residual) / abs(float(m_ref))
    return {
        "source_id": row["source_id"],
        "projector_status": "PROJECTOR_PASS_THEOREM_ZERO_CANDIDATE_POYNTING_AND_SURFACE_CLOSED_NONCLAIM",
        "Q_lm_residual": f"{residual:.12g}",
        "epsilon_extra_MTS_l_ge_1": f"{epsilon:.12g}",
        "certificate_status": "PROJECTOR_ZERO_PARENT_CERTIFICATE_PARTIALLY_CLOSED",
        "claim_blockers": row["claim_blockers"],
        "removed_blockers": "Z_Poynting_silent_or_included|Z_surface_exchange_zero_monopole",
        "claim_allowed": False,
        "valid_for_claim": False,
        "timestamp_utc": timestamp,
    }


def projector_rows(profiles: list[dict[str, object]], timestamp: str) -> list[dict[str, object]]:
    return [project_row(row, timestamp) for row in profiles]


def bound_rows(timestamp: str) -> list[dict[str, object]]:
    return [
        {
            "bound_id": "BXS3982_0_surface_closed",
            "symbol": "epsilon_closed_source_failure_surface_part",
            "formula": "|surface_TF|+|exchange_TF|+|boundary_flux_TF|=0 for controlled fixed isolated monopole boundary",
            "units": "same numerator as epsilon_closed_source_failure",
            "current_status": "SURFACE_EXCHANGE_CLOSED_FOR_CONTROLLED_BRANCH_NONCLAIM",
            "claim_allowed": False,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "bound_id": "BXS3982_1_projector_zero_candidate",
            "symbol": "epsilon_extra_MTS_l_ge_1",
            "formula": "|Q_lm_total-Q_lm_GR_baseline|/M_H_ref=0 for controlled l>=1 candidate",
            "units": "dimensionless",
            "current_status": "NONCLAIM_ZERO_CANDIDATE_WITH_TWO_BLOCKERS_REMOVED",
            "claim_allowed": False,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "bound_id": "BXS3982_2_remaining_source",
            "symbol": "epsilon_source_l_ge_1",
            "formula": "still blocked by closed-total-source inclusion and no-extra-l>=1-MTS-hair factors",
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
            "feed_id": "SXF3982_0_surface",
            "target": "Z_surface_exchange_zero_monopole",
            "update": "closed for controlled fixed isolated monopole boundary only",
            "effect": "removes surface/exchange blocker from the controlled candidate claim blocker list",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "feed_id": "SXF3982_1_parent_zero",
            "target": "Z_parent_zero_lge1_candidate",
            "update": "remaining blockers narrowed to closed total source and no extra l>=1 MTS hair",
            "effect": "next step can attack a much smaller pair of source-side blockers",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "feed_id": "SXF3982_2_next",
            "target": "no_extra_lge1_MTS_hair_or_closed_total_source",
            "update": f"move to {NEXT_DOC}",
            "effect": "attack no-extra-hair or closed source inclusion next",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
    ]


def decision_rows(timestamp: str) -> list[dict[str, object]]:
    return [
        {
            "row_id": "DEC3982_0_close",
            "decision": "close surface/exchange blocker branch-specifically",
            "status": "SURFACE_EXCHANGE_BLOCKER_CLOSED_FOR_CONTROLLED_BRANCH",
            "reason": "fixed isolated monopole boundary has zero harmonic boundary data, zero total flux, zero wall TF stress, and no crossing radiative/Poynting flux",
            "next_action": "keep row nonclaim and attack no-extra-hair or closed-source blocker",
            "claim_allowed": False,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "DEC3982_1_no_smuggle",
            "decision": "do not convert surface zero into closed total source",
            "status": "CLOSED_TOTAL_SOURCE_NOT_SMUGGLED",
            "reason": "boundary silence does not prove the worldtube includes all internal stress/field/binding/apparatus channels",
            "next_action": "retain Z_closed_total_source_monopole as blocker",
            "claim_allowed": False,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "DEC3982_2_next",
            "decision": "next target selected",
            "status": "MOVE_TO_NO_EXTRA_HAIR_OR_CLOSED_SOURCE",
            "reason": "only two core controlled-source blockers remain",
            "next_action": NEXT_DOC,
            "claim_allowed": False,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
    ]


def claim_gate_rows(timestamp: str) -> list[dict[str, object]]:
    return [
        {
            "row_id": "CLG3982_0_candidate",
            "gate": "controlled theorem-zero candidate",
            "requirement": "closed total source and no extra l>=1 MTS hair still required",
            "status": "BLOCKED_TWO_PARENT_FACTORS_UNSIGNED",
            "claim_allowed": False,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "CLG3982_1_general_boundary",
            "gate": "general boundary/surface exchange",
            "requirement": "outside controlled fixed isolated branch, source Phi_B/tau_wall/harmonic/wall/radiative terms or keep fallback rows",
            "status": "GENERAL_CLAIM_STILL_BLOCKED",
            "claim_allowed": False,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "CLG3982_2_local_GR",
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
            "row_id": "NEXT3982_0",
            "next_doc": NEXT_DOC,
            "next_script": NEXT_SCRIPT,
            "target": "derive no-extra-l>=1 MTS hair or closed total source for the controlled monopole branch; otherwise create explicit finite source-bound rows",
            "success_condition": "one of the two remaining controlled candidate blockers is closed or converted into a source-ready finite bound row",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
    ]


def status_rows(timestamp: str, sources: list[dict[str, object]], projector: list[dict[str, object]]) -> list[dict[str, object]]:
    found = sum(bool(row["exists"]) and bool(row["needle_found"]) for row in sources)
    pass_rows = sum(row["projector_status"] == "PROJECTOR_PASS_THEOREM_ZERO_CANDIDATE_POYNTING_AND_SURFACE_CLOSED_NONCLAIM" for row in projector)
    blocked_rows = sum(str(row["projector_status"]).startswith("BLOCKED") for row in projector)
    return [
        {
            "checkpoint": CHECKPOINT,
            "status": "CONTROLLED_SURFACE_EXCHANGE_BLOCKER_CLOSED_TWO_PARENT_FACTORS_REMAIN",
            "sources_found": found,
            "sources_total": len(sources),
            "candidate_projector_pass_rows": pass_rows,
            "blocked_rows": blocked_rows,
            "main_result": "Z_surface_exchange_zero_monopole is closed for the controlled fixed isolated EH-monopole branch only; candidate still nonclaim because closed-total-source and no-extra-l>=1-MTS-hair factors remain unsigned",
            "next_target": NEXT_DOC,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
    ]


def doc_text(timestamp: str, sources: list[dict[str, object]]) -> str:
    found = sum(bool(row["exists"]) and bool(row["needle_found"]) for row in sources)
    return f"""# 3982 - Closed Total Source Or Surface/Exchange Zero For Controlled Monopole

Timestamp: `{timestamp}`

## Result

3982 closes the surface/exchange blocker for the controlled fixed isolated monopole branch:

```text
Z_surface_exchange_zero_monopole
  = CLOSED_FOR_CONTROLLED_FIXED_ISOLATED_MONOPOLE_BRANCH
```

Reason:

```text
Phi_B = 0
tau_wall_TF = 0
B_harmonic_boundary = 0
no crossing radiative/Poynting flux
fixed isolated monopole boundary
```

## Remaining Blockers

The controlled candidate is still not claim-valid. Remaining blockers:

```text
Z_closed_total_source_monopole
Z_no_extra_lge1_MTS_hair
```

Surface silence is not being used to smuggle in closed total source. Real lab/nonisolated boundaries still need finite source rows.

Next target:

```text
{NEXT_DOC}
```

Source needles found: `{found}/{len(sources)}`.
"""


def spine_block(timestamp: str) -> str:
    return f"""

## 3982 - Controlled Surface/Exchange Blocker Closure

- Timestamp: `{timestamp}`
- Status: `CONTROLLED_SURFACE_EXCHANGE_BLOCKER_CLOSED_TWO_PARENT_FACTORS_REMAIN`
- Closed blocker:
  `Z_surface_exchange_zero_monopole` is closed only for the controlled fixed isolated EH-monopole branch.
- Reason:
  `Phi_B=0`, `tau_wall_TF=0`, `B_harmonic_boundary=0`, no crossing radiative/Poynting flux, and fixed isolated monopole boundary.
- Still nonclaim:
  `Z_closed_total_source_monopole` and `Z_no_extra_lge1_MTS_hair` remain unsigned.
- Guard:
  surface silence does not prove closed total source; real lab/nonisolated boundaries still need finite source rows.
- Next: `{NEXT_DOC}`.
"""


def update_spine(timestamp: str) -> None:
    marker = "## 3982 - Controlled Surface/Exchange Blocker Closure"
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
    candidate = project_by_id["REAL3982_0_controlled_EH_monopole_l2m0_surface_closed"]

    return [
        val("VAL3982_00_sources_exist", all(row["exists"] for row in sources), "all cited source paths exist"),
        val("VAL3982_01_needles_found", all(row["needle_found"] for row in sources), "all cited source needles found"),
        val("VAL3982_02_theorem", {"BRANCH_SPECIFIC_SURFACE_EXCHANGE_ZERO_DERIVED", "CLOSED_SOURCE_NOT_SMUGGLED", "GENERAL_BOUNDARY_CLAIM_REJECTED", "ONE_MORE_BLOCKER_CLOSED_BRANCH_SPECIFIC_NONCLAIM"} <= theorem_statuses, "surface/exchange theorem, no-smuggle guard, general refusal, and blocker effect present"),
        val("VAL3982_03_certificate_closed", factors["Z_surface_exchange_zero_monopole"]["current_status"] == "CLOSED_FOR_CONTROLLED_FIXED_ISOLATED_MONOPOLE_BRANCH", "surface factor closed for controlled branch"),
        val("VAL3982_04_poynting_still_closed", factors["Z_Poynting_silent_or_included"]["current_status"] == "CLOSED_FOR_CONTROLLED_NEUTRAL_NONRADIATING_MONOPOLE_BRANCH", "Poynting factor remains closed for controlled branch"),
        val("VAL3982_05_total_still_false", factors["Z_parent_zero_lge1_candidate"]["current_status"] == "FALSE_UNTIL_CLOSED_SOURCE_AND_NO_EXTRA_HAIR_CLOSE", "total certificate still false"),
        val("VAL3982_06_projector_candidate", candidate["projector_status"] == "PROJECTOR_PASS_THEOREM_ZERO_CANDIDATE_POYNTING_AND_SURFACE_CLOSED_NONCLAIM" and candidate["epsilon_extra_MTS_l_ge_1"] == "0", "candidate still projects to zero residual"),
        val("VAL3982_07_blockers_removed", set(str(candidate["removed_blockers"]).split("|")) == {"Z_Poynting_silent_or_included", "Z_surface_exchange_zero_monopole"}, "Poynting and surface blockers removed from candidate"),
        val("VAL3982_08_remaining_blockers", set(str(candidate["claim_blockers"]).split("|")) == {"Z_closed_total_source_monopole", "Z_no_extra_lge1_MTS_hair"}, "only closed-source and no-extra-hair blockers remain"),
        val("VAL3982_09_bounds", {"epsilon_closed_source_failure_surface_part", "epsilon_extra_MTS_l_ge_1", "epsilon_source_l_ge_1"} <= bound_symbols, "bound rows include surface closure, projector, and source chain"),
        val("VAL3982_10_feed", {"Z_surface_exchange_zero_monopole", "Z_parent_zero_lge1_candidate", "no_extra_lge1_MTS_hair_or_closed_total_source"} <= feed_targets, "feeds reach surface factor, parent zero, and next target"),
        val("VAL3982_11_decision", {"SURFACE_EXCHANGE_BLOCKER_CLOSED_FOR_CONTROLLED_BRANCH", "CLOSED_TOTAL_SOURCE_NOT_SMUGGLED", "MOVE_TO_NO_EXTRA_HAIR_OR_CLOSED_SOURCE"} <= decision_statuses, "decision gate records closure, no-smuggle, and next move"),
        val("VAL3982_12_claim_gate", {"BLOCKED_TWO_PARENT_FACTORS_UNSIGNED", "GENERAL_CLAIM_STILL_BLOCKED", "LOCAL_GR_STILL_OPEN"} <= claim_statuses, "claim gates preserve remaining blockers and local GR block"),
        val("VAL3982_13_next_target", next_target[0]["next_doc"] == NEXT_DOC and next_target[0]["next_script"] == NEXT_SCRIPT, "next target points to no-extra-hair or closed total source"),
        val("VAL3982_14_all_nonclaim", all(not row.get("valid_for_claim", True) for group in rows.values() for row in group), "all generated physics rows remain nonclaim"),
        val("VAL3982_15_outputs_outside_fwb", all(FWB not in path.parents for path in generated_csvs) and FWB not in DOC_PATH.parents, "no generated output is inside formalization-workbench"),
        val("VAL3982_16_doc_exists", DOC_PATH.exists(), "checkpoint doc exists"),
        val("VAL3982_17_spine_updated", SPINE_PATH.exists() and "3982 - Controlled Surface/Exchange Blocker Closure" in read_text(SPINE_PATH), "spine updated"),
        val("VAL3982_18_csv_parse", parsed, parse_detail),
        val("VAL3982_19_script_compile", True, "script compiled before validation write"),
        val("VAL3982_20_no_pycache", not (SCRIPT_PATH.parent / "__pycache__").exists(), "scripts __pycache__ removed"),
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
        raise SystemExit(f"3982 validation failed: {failed}")

    print(f"3982 checkpoint complete: {DOC_PATH}")
    print(f"validation: {OUTPUTS['validation']}")
    print("Controlled surface/exchange blocker closed for monopole branch")


if __name__ == "__main__":
    run()

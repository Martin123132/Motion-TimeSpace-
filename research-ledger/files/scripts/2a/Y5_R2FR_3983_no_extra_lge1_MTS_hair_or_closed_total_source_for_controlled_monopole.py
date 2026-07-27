from __future__ import annotations

import csv
import py_compile
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


CHECKPOINT = "3983"
SCRIPT_PATH = Path(__file__).resolve()
PCW = SCRIPT_PATH.parents[1]
ROOT = PCW.parent
FWB = ROOT / "formalization-workbench"
SRC = PCW / "source-intake" / "mts_residuals"
DOC_PATH = PCW / "3983-Y5-R2FR-no-extra-lge1-MTS-hair-or-closed-total-source-for-controlled-monopole.md"
SPINE_PATH = PCW / "LOCAL_GR_COUPLING_SPINE_CURRENT_STATE.md"

OUTPUTS = {
    "sources": SRC / "P8_Y5_R2FR_3983_SOURCE_REGISTER.csv",
    "theorem": SRC / "P8_Y5_R2FR_3983_CONTROLLED_NO_EXTRA_LGE1_HAIR_THEOREM.csv",
    "certificate": SRC / "P8_Y5_R2FR_3983_PARENT_ZERO_CERTIFICATE_UPDATE.csv",
    "profiles": SRC / "P8_Y5_R2FR_3983_SOURCE_PROFILE_CANDIDATE_ROWS.csv",
    "projector": SRC / "P8_Y5_R2FR_3983_PROJECTOR_RESULTS.csv",
    "bounds": SRC / "P8_Y5_R2FR_3983_BOUND_FEED_ROWS.csv",
    "feed": SRC / "P8_Y5_R2FR_3983_FEED_UPDATE.csv",
    "decision": SRC / "P8_Y5_R2FR_3983_DECISION_GATE.csv",
    "claim_gate": SRC / "P8_Y5_R2FR_3983_CLAIM_GATE.csv",
    "next": SRC / "P8_Y5_R2FR_3983_NEXT_TARGET.csv",
    "status": SRC / "P8_Y5_R2FR_3983_STATUS.csv",
    "validation": SRC / "P8_Y5_BRR545_3983_VALIDATION.csv",
}

NEXT_DOC = "3984-Y5-R2FR-closed-total-source-worldtube-ownership-or-finite-source-charge-bound.md"
NEXT_SCRIPT = "scripts/Y5_R2FR_3984_closed_total_source_worldtube_ownership_or_finite_source_charge_bound.py"


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
        ("SRC3983_00_3982_next", SRC / "P8_Y5_R2FR_3982_NEXT_TARGET.csv", "NEXT3982_0", "3982 handoff"),
        ("SRC3983_01_3982_cert_hair", SRC / "P8_Y5_R2FR_3982_PARENT_ZERO_CERTIFICATE_UPDATE.csv", "PZC3982_5_no_extra_hair", "3982 no-extra-hair blocker"),
        ("SRC3983_02_3982_cert_total", SRC / "P8_Y5_R2FR_3982_PARENT_ZERO_CERTIFICATE_UPDATE.csv", "PZC3982_7_total", "3982 total certificate"),
        ("SRC3983_03_3982_projector", SRC / "P8_Y5_R2FR_3982_PROJECTOR_RESULTS.csv", "REAL3982_0_controlled_EH_monopole_l2m0_surface_closed", "3982 candidate projector"),
        ("SRC3983_04_3982_claim", SRC / "P8_Y5_R2FR_3982_CLAIM_GATE.csv", "CLG3982_0_candidate", "3982 claim gate"),
        ("SRC3983_05_3969_EH", SRC / "P8_Y5_R2FR_3969_SINGLE_EXTERIOR_MASS_UNIQUENESS_THEOREM.csv", "UQ3969_1_conditional_uniqueness_theorem", "EH exterior uniqueness"),
        ("SRC3983_06_3969_guard", SRC / "P8_Y5_R2FR_3969_SINGLE_EXTERIOR_MASS_UNIQUENESS_THEOREM.csv", "UQ3969_4_not_current_MTS_claim", "parent signature limit"),
        ("SRC3983_07_3970_status", SRC / "P8_Y5_R2FR_3970_STATUS.csv", "NO_EXTRA_MONOPOLE_CHANNELWISE_THEOREM_AND_BOUND_VECTOR_READY", "no-extra monopole status"),
        ("SRC3983_08_mass_contract_extra", SRC / "P8_mass_current_Hamiltonian_boundary_charge_CONTRACT.csv", "HC5_no_extra_hidden_charge", "extra hidden charge blocker"),
        ("SRC3983_09_source_flux_no_extra", SRC / "P8_SOURCE_MEASURE_MEFF_FLUX_THEOREM.csv", "T509_2_no_extra_mass_channel", "no extra mass channel theorem"),
        ("SRC3983_10_source_clause_no_extra", SRC / "P8_SOURCE_MEASURE_MEFF_FLUX_CLAUSES.csv", "SM509_5_no_extra_channel", "no extra channel clause"),
        ("SRC3983_11_top_pim_no_extra", SRC / "P8_TOPOLOGICAL_PIM_PARENT_CLAUSE_ATTEMPT.csv", "TP500_4_no_extra_projection", "topological no extra projection clause"),
        ("SRC3983_12_top_pim_fail", SRC / "P8_TOPOLOGICAL_PIM_CLOSURE_CONDITIONS.csv", "TC500_4_no_extra_projection", "topological no extra projection fail-open"),
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
            "theorem_id": "NEH3983_0_branch",
            "claim_piece": "controlled no-extra l>=1 MTS hair",
            "mathematical_form": "controlled branch assumes EH-only exterior equations, DeltaE_munu=0, no extra local tensors, fixed monopole boundary class, and one exterior charge mu",
            "derived_result": "all l>=1 residual MTS source hair is zero in this controlled branch after GR-baseline subtraction",
            "status": "BRANCH_SPECIFIC_NO_EXTRA_LGE1_HAIR_DERIVED",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "theorem_id": "NEH3983_1_not_general",
            "claim_piece": "no general no-hair promotion",
            "mathematical_form": "outside the EH-only/no-extra-tensor controlled branch, retained channels Q_nonEH, Q_PiM, Q_boundary, Q_domain, Q_memory, Q_range, Q_delta_kappa remain active",
            "derived_result": "general MTS no-extra-hair is not claimed",
            "status": "GENERAL_NO_EXTRA_HAIR_CLAIM_REJECTED",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "theorem_id": "NEH3983_2_closed_source_not_smuggled",
            "claim_piece": "no-extra hair does not prove source ownership",
            "mathematical_form": "no l>=1 exterior residual hair does not prove the worldtube source measure equals the parent Hilbert/Newton source charge",
            "derived_result": "Z_closed_total_source_monopole remains unsigned",
            "status": "CLOSED_TOTAL_SOURCE_STILL_UNSIGNED",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "theorem_id": "NEH3983_3_certificate_effect",
            "claim_piece": "third blocker removed",
            "mathematical_form": "PZC3982_5_no_extra_hair: UNSIGNED -> CLOSED_FOR_CONTROLLED_EH_ONLY_MONOPOLE_BRANCH",
            "derived_result": "controlled candidate loses Z_no_extra_lge1_MTS_hair; only closed-total-source ownership remains in its direct blocker list",
            "status": "ONE_MORE_BLOCKER_CLOSED_BRANCH_SPECIFIC_NONCLAIM",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
    ]


def certificate_rows(timestamp: str) -> list[dict[str, object]]:
    specs = [
        ("PZC3983_0_EH_vacuum", "Z_EH_vacuum_monopole_family", "exterior readout is EH vacuum/SdS monopole family with one mass charge", "conditional_from_3969", "CONDITIONAL_NOT_PARENT_SIGNED", "still a conditional controlled branch"),
        ("PZC3983_1_same_GR", "Z_same_GR_baseline_monopole", "GR comparator uses same source/frame/units/r_eval", "operator_contract", "DEFINED_FOR_CANDIDATE_ROW", "keeps Q_lm_GR_baseline=0 for l>=1"),
        ("PZC3983_2_total_source", "Z_closed_total_source_monopole", "one closed worldtube includes all stress/field/binding/apparatus/exchange channels and equals parent source charge", "required", "UNSIGNED_FROM_3978", "still blocks claim promotion"),
        ("PZC3983_3_poynting", "Z_Poynting_silent_or_included", "controlled branch has no exterior EM/radiative support and any internal field stress is included in T_tot(W)", "closed_branch_specific", "CLOSED_FOR_CONTROLLED_NEUTRAL_NONRADIATING_MONOPOLE_BRANCH", "blocker removed in 3981"),
        ("PZC3983_4_surface", "Z_surface_exchange_zero_monopole", "fixed isolated monopole boundary has no flux/wall/harmonic surface exchange", "closed_branch_specific", "CLOSED_FOR_CONTROLLED_FIXED_ISOLATED_MONOPOLE_BRANCH", "blocker removed in 3982"),
        ("PZC3983_5_no_extra_hair", "Z_no_extra_lge1_MTS_hair", "EH-only/no-extra-local-tensor controlled branch has no residual l>=1 MTS hair beyond the GR monopole exterior", "closed_branch_specific", "CLOSED_FOR_CONTROLLED_EH_ONLY_MONOPOLE_BRANCH", "blocker removed in 3983"),
        ("PZC3983_6_counterguard", "Z_no_spherical_cheat", "zero row is a controlled EH-monopole branch, not arbitrary spherical averaging", "guard", "GUARD_ACTIVE", "prevents overclaim"),
        ("PZC3983_7_total", "Z_parent_zero_lge1_candidate", "product of EH, same-GR, closed source, Poynting, surface, and no-extra-hair factors", "total", "FALSE_UNTIL_CLOSED_TOTAL_SOURCE_CLOSES", "candidate remains nonclaim until source ownership closes"),
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
    source_path = SRC / "P8_Y5_R2FR_3982_PARENT_ZERO_CERTIFICATE_UPDATE.csv"
    common = {
        "arena": "controlled_EH_only_fixed_isolated_neutral_nonradiating_monopole_branch",
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
        "claim_blockers": "Z_closed_total_source_monopole",
        "valid_for_claim": False,
        "timestamp_utc": timestamp,
    }
    rows: list[dict[str, object]] = []
    for source_id, l_value, m_value in [
        ("REAL3983_0_controlled_EH_monopole_l2m0_noextra_closed", 2, 0),
        ("REAL3983_1_same_branch_l3m0_noextra_closed", 3, 0),
    ]:
        row = dict(common)
        row.update({"source_id": source_id, "l": l_value, "m": m_value})
        rows.append(row)
    rows.append(
        {
            "source_id": "REAL3983_2_real_lab_row_placeholder_blocked",
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
        "projector_status": "PROJECTOR_PASS_THEOREM_ZERO_CANDIDATE_NO_EXTRA_HAIR_CLOSED_NONCLAIM",
        "Q_lm_residual": f"{residual:.12g}",
        "epsilon_extra_MTS_l_ge_1": f"{epsilon:.12g}",
        "certificate_status": "PROJECTOR_ZERO_PARENT_CERTIFICATE_ONE_BLOCKER_REMAINS",
        "claim_blockers": row["claim_blockers"],
        "removed_blockers": "Z_Poynting_silent_or_included|Z_surface_exchange_zero_monopole|Z_no_extra_lge1_MTS_hair",
        "claim_allowed": False,
        "valid_for_claim": False,
        "timestamp_utc": timestamp,
    }


def projector_rows(profiles: list[dict[str, object]], timestamp: str) -> list[dict[str, object]]:
    return [project_row(row, timestamp) for row in profiles]


def bound_rows(timestamp: str) -> list[dict[str, object]]:
    return [
        {
            "bound_id": "BNE3983_0_no_extra_hair_closed",
            "symbol": "epsilon_extra_MTS_l_ge_1",
            "formula": "epsilon_extra_MTS_l_ge_1=0 for controlled EH-only/no-extra-tensor monopole branch after GR-baseline subtraction",
            "units": "dimensionless",
            "current_status": "NO_EXTRA_HAIR_CLOSED_FOR_CONTROLLED_BRANCH_NONCLAIM",
            "claim_allowed": False,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "bound_id": "BNE3983_1_remaining_source",
            "symbol": "epsilon_source_l_ge_1",
            "formula": "candidate still blocked by Z_closed_total_source_monopole: worldtube source ownership and parent Hilbert/Newton charge equality",
            "units": "dimensionless",
            "current_status": "ONE_PARENT_SOURCE_OWNERSHIP_BLOCKER_REMAINS",
            "claim_allowed": False,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "bound_id": "BNE3983_2_general_hair",
            "symbol": "epsilon_extra_MTS_l_ge_1_general",
            "formula": "outside controlled branch retain finite rows for Q_nonEH+Q_PiM+Q_boundary+Q_domain+Q_memory+Q_range+Q_delta_kappa",
            "units": "dimensionless",
            "current_status": "GENERAL_EXTRA_HAIR_BOUND_REQUIRED",
            "claim_allowed": False,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
    ]


def feed_rows(timestamp: str) -> list[dict[str, object]]:
    return [
        {
            "feed_id": "NEF3983_0_noextra",
            "target": "Z_no_extra_lge1_MTS_hair",
            "update": "closed for controlled EH-only/no-extra-local-tensor monopole branch only",
            "effect": "removes no-extra-hair blocker from the controlled candidate",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "feed_id": "NEF3983_1_parent_zero",
            "target": "Z_parent_zero_lge1_candidate",
            "update": "remaining direct blocker narrowed to closed total source/worldtube ownership",
            "effect": "next target becomes source-charge ownership rather than angular hair",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "feed_id": "NEF3983_2_next",
            "target": "closed_total_source_worldtube_ownership",
            "update": f"move to {NEXT_DOC}",
            "effect": "attack the final controlled-candidate source-side ownership blocker",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
    ]


def decision_rows(timestamp: str) -> list[dict[str, object]]:
    return [
        {
            "row_id": "DEC3983_0_close",
            "decision": "close no-extra-l>=1 hair branch-specifically",
            "status": "NO_EXTRA_HAIR_BLOCKER_CLOSED_FOR_CONTROLLED_BRANCH",
            "reason": "the controlled branch is EH-only, one-monopole, no-extra-local-tensor by construction; residual l>=1 MTS hair is zero after GR-baseline subtraction",
            "next_action": "keep row nonclaim and attack closed total source ownership",
            "claim_allowed": False,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "DEC3983_1_general",
            "decision": "do not generalize no-extra-hair to real arenas",
            "status": "GENERAL_NO_EXTRA_HAIR_CLAIM_REJECTED",
            "reason": "outside controlled branch, nonEH/PiM/boundary/domain/memory/range/kappa/frame channels remain active",
            "next_action": "retain general extra-hair bound rows",
            "claim_allowed": False,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "DEC3983_2_next",
            "decision": "next target selected",
            "status": "MOVE_TO_CLOSED_TOTAL_SOURCE_OWNERSHIP",
            "reason": "only direct controlled-candidate blocker left is source/worldtube charge ownership",
            "next_action": NEXT_DOC,
            "claim_allowed": False,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
    ]


def claim_gate_rows(timestamp: str) -> list[dict[str, object]]:
    return [
        {
            "row_id": "CLG3983_0_candidate",
            "gate": "controlled theorem-zero candidate",
            "requirement": "closed total source/worldtube ownership and parent Hilbert/Newton charge equality",
            "status": "BLOCKED_CLOSED_TOTAL_SOURCE_UNSIGNED",
            "claim_allowed": False,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "CLG3983_1_general_hair",
            "gate": "general no-extra-hair",
            "requirement": "source or zero all nonEH/PiM/boundary/domain/memory/range/kappa/frame extra channels",
            "status": "GENERAL_CLAIM_STILL_BLOCKED",
            "claim_allowed": False,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "CLG3983_2_local_GR",
            "gate": "local GR",
            "requirement": "controlled source ownership plus boundary/external/angular/PPN/Newton/EM/source-coupling gates",
            "status": "LOCAL_GR_STILL_OPEN",
            "claim_allowed": False,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
    ]


def next_rows(timestamp: str) -> list[dict[str, object]]:
    return [
        {
            "row_id": "NEXT3983_0",
            "next_doc": NEXT_DOC,
            "next_script": NEXT_SCRIPT,
            "target": "derive closed total source/worldtube ownership and equality to parent Hilbert/Newton charge for the controlled monopole, or emit finite source-charge bound rows",
            "success_condition": "Z_closed_total_source_monopole closes branch-specifically or is replaced by an explicit epsilon_closed_source_failure/source-charge residual row",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
    ]


def status_rows(timestamp: str, sources: list[dict[str, object]], projector: list[dict[str, object]]) -> list[dict[str, object]]:
    found = sum(bool(row["exists"]) and bool(row["needle_found"]) for row in sources)
    pass_rows = sum(row["projector_status"] == "PROJECTOR_PASS_THEOREM_ZERO_CANDIDATE_NO_EXTRA_HAIR_CLOSED_NONCLAIM" for row in projector)
    blocked_rows = sum(str(row["projector_status"]).startswith("BLOCKED") for row in projector)
    return [
        {
            "checkpoint": CHECKPOINT,
            "status": "CONTROLLED_NO_EXTRA_HAIR_BLOCKER_CLOSED_CLOSED_SOURCE_REMAINS",
            "sources_found": found,
            "sources_total": len(sources),
            "candidate_projector_pass_rows": pass_rows,
            "blocked_rows": blocked_rows,
            "main_result": "Z_no_extra_lge1_MTS_hair is closed for the controlled EH-only monopole branch only; candidate still nonclaim because closed-total-source/worldtube source ownership remains unsigned",
            "next_target": NEXT_DOC,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
    ]


def doc_text(timestamp: str, sources: list[dict[str, object]]) -> str:
    found = sum(bool(row["exists"]) and bool(row["needle_found"]) for row in sources)
    return f"""# 3983 - No Extra l>=1 MTS Hair Or Closed Total Source For Controlled Monopole

Timestamp: `{timestamp}`

## Result

3983 closes the no-extra-hair blocker only inside the controlled branch:

```text
Z_no_extra_lge1_MTS_hair
  = CLOSED_FOR_CONTROLLED_EH_ONLY_MONOPOLE_BRANCH
```

Reason:

```text
EH-only exterior equations
DeltaE_munu = 0
no extra local tensors
fixed monopole boundary class
one exterior mass charge
same-source GR baseline
```

So the controlled profile keeps:

```text
epsilon_extra_MTS_l_ge_1 = 0
```

## Remaining Blocker

The controlled candidate is still not claim-valid. Remaining direct blocker:

```text
Z_closed_total_source_monopole
```

This is not a general no-hair theorem for real arenas. Non-EH, PiM, boundary, domain, memory, range, kappa, and frame channels remain active outside the controlled branch.

Next target:

```text
{NEXT_DOC}
```

Source needles found: `{found}/{len(sources)}`.
"""


def spine_block(timestamp: str) -> str:
    return f"""

## 3983 - Controlled No-Extra-Hair Blocker Closure

- Timestamp: `{timestamp}`
- Status: `CONTROLLED_NO_EXTRA_HAIR_BLOCKER_CLOSED_CLOSED_SOURCE_REMAINS`
- Closed blocker:
  `Z_no_extra_lge1_MTS_hair` is closed only for the controlled EH-only/no-extra-local-tensor monopole branch.
- Reason:
  EH-only exterior equations, `DeltaE_munu=0`, no extra local tensors, fixed monopole boundary class, one mass charge, and same-source GR baseline.
- Still nonclaim:
  `Z_closed_total_source_monopole` remains unsigned.
- Guard:
  general no-extra-hair remains blocked for real arenas with nonEH/PiM/boundary/domain/memory/range/kappa/frame channels.
- Next: `{NEXT_DOC}`.
"""


def update_spine(timestamp: str) -> None:
    marker = "## 3983 - Controlled No-Extra-Hair Blocker Closure"
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
    candidate = project_by_id["REAL3983_0_controlled_EH_monopole_l2m0_noextra_closed"]

    return [
        val("VAL3983_00_sources_exist", all(row["exists"] for row in sources), "all cited source paths exist"),
        val("VAL3983_01_needles_found", all(row["needle_found"] for row in sources), "all cited source needles found"),
        val("VAL3983_02_theorem", {"BRANCH_SPECIFIC_NO_EXTRA_LGE1_HAIR_DERIVED", "GENERAL_NO_EXTRA_HAIR_CLAIM_REJECTED", "CLOSED_TOTAL_SOURCE_STILL_UNSIGNED", "ONE_MORE_BLOCKER_CLOSED_BRANCH_SPECIFIC_NONCLAIM"} <= theorem_statuses, "no-extra-hair theorem, general refusal, source guard, and blocker effect present"),
        val("VAL3983_03_certificate_closed", factors["Z_no_extra_lge1_MTS_hair"]["current_status"] == "CLOSED_FOR_CONTROLLED_EH_ONLY_MONOPOLE_BRANCH", "no-extra-hair factor closed for controlled branch"),
        val("VAL3983_04_closed_source_remaining", factors["Z_closed_total_source_monopole"]["current_status"] == "UNSIGNED_FROM_3978", "closed-source factor remains unsigned"),
        val("VAL3983_05_total_still_false", factors["Z_parent_zero_lge1_candidate"]["current_status"] == "FALSE_UNTIL_CLOSED_TOTAL_SOURCE_CLOSES", "total certificate still false until closed-source ownership closes"),
        val("VAL3983_06_projector_candidate", candidate["projector_status"] == "PROJECTOR_PASS_THEOREM_ZERO_CANDIDATE_NO_EXTRA_HAIR_CLOSED_NONCLAIM" and candidate["epsilon_extra_MTS_l_ge_1"] == "0", "candidate still projects to zero residual"),
        val("VAL3983_07_blockers_removed", set(str(candidate["removed_blockers"]).split("|")) == {"Z_Poynting_silent_or_included", "Z_surface_exchange_zero_monopole", "Z_no_extra_lge1_MTS_hair"}, "Poynting, surface, and no-extra-hair blockers removed"),
        val("VAL3983_08_remaining_blocker", str(candidate["claim_blockers"]) == "Z_closed_total_source_monopole", "only closed-total-source blocker remains in candidate row"),
        val("VAL3983_09_bounds", {"epsilon_extra_MTS_l_ge_1", "epsilon_source_l_ge_1", "epsilon_extra_MTS_l_ge_1_general"} <= bound_symbols, "bound rows include controlled projector, source chain, and general extra-hair fallback"),
        val("VAL3983_10_feed", {"Z_no_extra_lge1_MTS_hair", "Z_parent_zero_lge1_candidate", "closed_total_source_worldtube_ownership"} <= feed_targets, "feeds reach no-extra-hair, parent zero, and next source ownership target"),
        val("VAL3983_11_decision", {"NO_EXTRA_HAIR_BLOCKER_CLOSED_FOR_CONTROLLED_BRANCH", "GENERAL_NO_EXTRA_HAIR_CLAIM_REJECTED", "MOVE_TO_CLOSED_TOTAL_SOURCE_OWNERSHIP"} <= decision_statuses, "decision gate records closure, general refusal, and next move"),
        val("VAL3983_12_claim_gate", {"BLOCKED_CLOSED_TOTAL_SOURCE_UNSIGNED", "GENERAL_CLAIM_STILL_BLOCKED", "LOCAL_GR_STILL_OPEN"} <= claim_statuses, "claim gates preserve closed-source and local GR blocks"),
        val("VAL3983_13_next_target", next_target[0]["next_doc"] == NEXT_DOC and next_target[0]["next_script"] == NEXT_SCRIPT, "next target points to closed total source ownership"),
        val("VAL3983_14_all_nonclaim", all(not row.get("valid_for_claim", True) for group in rows.values() for row in group), "all generated physics rows remain nonclaim"),
        val("VAL3983_15_outputs_outside_fwb", all(FWB not in path.parents for path in generated_csvs) and FWB not in DOC_PATH.parents, "no generated output is inside formalization-workbench"),
        val("VAL3983_16_doc_exists", DOC_PATH.exists(), "checkpoint doc exists"),
        val("VAL3983_17_spine_updated", SPINE_PATH.exists() and "3983 - Controlled No-Extra-Hair Blocker Closure" in read_text(SPINE_PATH), "spine updated"),
        val("VAL3983_18_csv_parse", parsed, parse_detail),
        val("VAL3983_19_script_compile", True, "script compiled before validation write"),
        val("VAL3983_20_no_pycache", not (SCRIPT_PATH.parent / "__pycache__").exists(), "scripts __pycache__ removed"),
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
        raise SystemExit(f"3983 validation failed: {failed}")

    print(f"3983 checkpoint complete: {DOC_PATH}")
    print(f"validation: {OUTPUTS['validation']}")
    print("Controlled no-extra l>=1 hair blocker closed for monopole branch")


if __name__ == "__main__":
    run()

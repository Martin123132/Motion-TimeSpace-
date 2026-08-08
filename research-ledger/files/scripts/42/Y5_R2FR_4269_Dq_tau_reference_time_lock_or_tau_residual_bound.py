from __future__ import annotations

import csv
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List


ROOT = Path(__file__).resolve().parents[2]
FORMAL = ROOT / "formalization-workbench"
POST = ROOT / "post-checkpoint-work"
SOURCE_DIR = POST / "source-intake" / "mts_residuals"

CHECKPOINT = "4269"
CLAIM_ID = "L-110"
BRANCH = "MTS_R2FR_Y5_DQ_TAU_REFERENCE_TIME_LOCK_OR_TAU_RESIDUAL_BOUND_4269"
DECISION = "DQ_TAU_ADOPTED_FOR_QBASIC_OBSERVED_TAU_BRANCH_TAU_RESIDUALS_RETAINED_NONCLAIM"
MARKER = "PPC4161_DQ_TAU_REFERENCE_TIME_LOCK_OR_TAU_RESIDUAL_4269"
PACKET_MARKER = "PPC4161_PACKET_DQ_TAU_REFERENCE_TIME_LOCK_OR_TAU_RESIDUAL_4269"
NEXT_TARGET = "4270-Y5-R2FR-Dq-geom-observed-coframe-descent-or-epsilon-geom-fill.md"

FORMAL_PATH = FORMAL / "285-PPC4161-Dq-tau-reference-time-lock-or-tau-residual-bound.md"
DOC_PATH = POST / "4269-Y5-R2FR-Dq-tau-reference-time-lock-or-tau-residual-bound.md"
VALIDATION_PATH = SOURCE_DIR / "P8_Y5_BRR545_4269_VALIDATION.csv"

LIVE_COMPONENT_CANDIDATE_PATH = SOURCE_DIR / "P8_Y5_R2FR_4254_DQ_COMPONENT_VALUES_CANDIDATE.csv"
LOCAL_COMPONENT_CANDIDATE_PATH = SOURCE_DIR / "P8_Y5_R2FR_4269_DQ_COMPONENT_VALUES_CANDIDATE.csv"
REDUCED_GEOM_4270_PATH = SOURCE_DIR / "P8_Y5_R2FR_4270_DQ_GEOM_REDUCED_CANDIDATE.csv"
FORMAL_4270_PATH = FORMAL / "286-PPC4161-Dq-geom-core-coframe-shadow-or-reduced-epsilon-bound.md"
CORE_GEOM_4271_PATH = SOURCE_DIR / "P8_Y5_R2FR_4271_DQ_GEOM_CORE_FRAME_CANDIDATE.csv"
FORMAL_4271_PATH = FORMAL / "287-PPC4161-core-coframe-shadow-zero-or-first-source-backed-epsilon-row.md"
BOUND_GEOM_4272_PATH = SOURCE_DIR / "P8_Y5_R2FR_4272_DQ_GEOM_BOUND_RUNNER_CANDIDATE.csv"
FORMAL_4272_PATH = FORMAL / "288-PPC4161-parent-no-extra-frame-signature-or-cg-bdis-first-bound-runner.md"

STAMP = datetime.now(timezone.utc).replace(microsecond=0).isoformat()
PROBE_ORDER = (
    "Dq_geom",
    "Dq_tau",
    "Dq_matter",
    "Dq_source_readout",
    "Dq_theta_marker",
    "Dq_boundary_projector",
    "Dq_EM",
    "Dq_coeff",
)


@dataclass(frozen=True)
class SourceSpec:
    source_id: str
    path: Path
    required_text: str
    role: str


SOURCE_SPECS: Dict[str, SourceSpec] = {
    "SRC4269_00_4216_formal_tau_lock": SourceSpec(
        "SRC4269_00_4216_formal_tau_lock",
        FORMAL / "232-PPC4161-tau-surface-frame-lock-or-bound.md",
        "tau_source=tau_charge=tau_clock=tau_orbit=tau_PPN=tau_readout;",
        "Formal tau/surface/frame lock theorem.",
    ),
    "SRC4269_01_4215_reference": SourceSpec(
        "SRC4269_01_4215_reference",
        FORMAL / "231-PPC4161-reference-lock-curl-zero-or-bound.md",
        "fixed parent-selected functional",
        "Reference-time lock cannot be post-fit or frame-dependent.",
    ),
    "SRC4269_02_4219_dq_component": SourceSpec(
        "SRC4269_02_4219_dq_component",
        FORMAL / "235-PPC4161-Dq-source-readout-coupling-marker-zero-or-bound.md",
        "Dq_tau[v]=0",
        "Dq component norm contract names the tau leg explicitly.",
    ),
    "SRC4269_03_4216_csv_theorem": SourceSpec(
        "SRC4269_03_4216_csv_theorem",
        SOURCE_DIR / "P8_Y5_R2FR_4216_TAU_SURFACE_FRAME_THEOREM.csv",
        "TSF4216_0_one_time_generator",
        "Machine-readable one-time-generator row.",
    ),
    "SRC4269_04_4216_csv_bound": SourceSpec(
        "SRC4269_04_4216_csv_bound",
        SOURCE_DIR / "P8_Y5_R2FR_4216_TAU_SURFACE_BOUND_COMPONENTS.csv",
        "R_tau_split",
        "Machine-readable tau residual split rows.",
    ),
    "SRC4269_05_4219_matrix": SourceSpec(
        "SRC4269_05_4219_matrix",
        SOURCE_DIR / "P8_Y5_R2FR_4219_DQ_COMPONENT_MATRIX.csv",
        "DQC4219_1_tau",
        "Dq_tau is an explicit required q-component.",
    ),
    "SRC4269_06_2597_nonclaim_guard": SourceSpec(
        "SRC4269_06_2597_nonclaim_guard",
        SOURCE_DIR / "P8_Y5_TAU_IDENTITY_2597_THEOREM_AUDIT.csv",
        "TAU_IDENTITY_NOT_PARENT_SIGNED_CURRENT_CORPUS",
        "Earlier global tau identity audit stays active as a nonclaim guard.",
    ),
    "SRC4269_07_4268_next": SourceSpec(
        "SRC4269_07_4268_next",
        FORMAL / "284-PPC4161-Dq-boundary-projector-fixed-collar-or-boundary-residual-bound.md",
        "should attack `Dq_tau`",
        "4268 selected Dq_tau as the next live component.",
    ),
}


def common() -> Dict[str, str]:
    return {
        "checkpoint": CHECKPOINT,
        "branch": BRANCH,
        "generated_utc": STAMP,
        "decision": DECISION,
    }


def read_text(path: Path) -> str:
    if not path.exists():
        return ""
    return path.read_text(encoding="utf-8", errors="replace")


def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text.strip() + "\n", encoding="utf-8")


def write_csv(path: Path, rows: List[Dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        path.write_text("", encoding="utf-8")
        return
    fieldnames: List[str] = list(rows[0].keys())
    for row in rows:
        for key in row:
            if key not in fieldnames:
                fieldnames.append(key)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def csv_rows(path: Path) -> List[Dict[str, str]]:
    if not path.exists():
        return []
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def dq_geom_4270_reduced_row() -> Dict[str, str]:
    for row in csv_rows(REDUCED_GEOM_4270_PATH):
        if (
            row.get("probe_id") == "Dq_geom"
            and row.get("new_epsilon") == "MISSING_REDUCED_EPSILON_GEOM_CORE_COFRAME_SHADOW"
        ):
            return row
    return {}


def dq_geom_4271_core_row() -> Dict[str, str]:
    for row in csv_rows(CORE_GEOM_4271_PATH):
        if (
            row.get("probe_id") == "Dq_geom"
            and row.get("new_epsilon") == "MISSING_CORE_FRAME_COUPLING_ZERO_OR_NUMERIC_CG_BDIS_BOUND"
        ):
            return row
    return {}


def dq_geom_4272_bound_row() -> Dict[str, str]:
    for row in csv_rows(BOUND_GEOM_4272_PATH):
        if (
            row.get("probe_id") == "Dq_geom"
            and row.get("new_epsilon") == "MISSING_SCOREABLE_CG_BDIS_FRAME_VECTOR_INPUTS"
        ):
            return row
    return {}


def append_claim() -> None:
    path = FORMAL / "02-claims-register.csv"
    text = read_text(path)
    if CLAIM_ID in text:
        return
    with path.open(newline="", encoding="utf-8") as handle:
        fieldnames = next(csv.reader(handle))
    row = {
        "claim_id": CLAIM_ID,
        "domain": "local_gr",
        "claim": (
            "4269 adopts Dq_tau=0 and its C1 row only for the q-basic observed-tau/reference-time branch: "
            "one parent-selected local time generator defines source charge, Hamiltonian charge, clocks, orbit, PPN and readout; "
            "the linking surfaces are fixed or tau-dragged before variation; H_ref is fixed before comparison; and one observed coframe "
            "plus common units/orientation/normalization is used. Split tau choices, lapse rescaling, post-fit clock/orbit conventions, "
            "moving surfaces or private memory-time leakage reopen explicit finite tau residual rows."
        ),
        "current_evidence": (
            "4269 source register, q-basic observed-tau theorem rows, tau residual split rows, Dq_tau adoption row, "
            "updated component candidate, decision and firewall."
        ),
        "status": "private_Dq_tau_conditional_zero_adopted_for_qbasic_observed_tau_branch_nonclaim",
        "next_test": "Attack Dq_geom next; 4254 remains blocked by geometry and tomography constants.",
        "key_risk": "Confusing a branch-selected observed tau with a global parent derivation of all time notions, or using clock/orbit fits to choose tau after the fact.",
    }
    with path.open("a", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writerow(row)


def source_rows() -> List[Dict[str, str]]:
    rows: List[Dict[str, str]] = []
    for spec in SOURCE_SPECS.values():
        text = read_text(spec.path)
        rows.append(
            {
                **common(),
                "source_id": spec.source_id,
                "path": str(spec.path),
                "exists": str(spec.path.exists()),
                "required_text": spec.required_text,
                "required_text_found": str(spec.required_text in text),
                "role": spec.role,
                "valid_for_claim": "False",
            }
        )
    return rows


def tau_lock_theorem_rows() -> List[Dict[str, str]]:
    raw = [
        (
            "TAU4269_0_component_definition",
            "Dq_tau component",
            "Dq_tau measures hidden vertical drift of the observed time generator, clock branch, time readout and tau-role map, not every private process-time variable.",
            "DEFINITION_SPLIT",
            "private traversal/memory time is allowed only if it does not alter observed clock/source/orbit/readout tau",
        ),
        (
            "TAU4269_1_qbasic_observed_tau",
            "q-basic observed tau",
            "If tau_obs=tau_bar(q) is selected before variation and v is in ker(Dq), then delta_v tau_obs=0 and Dq_tau[v]=0.",
            "CONDITIONAL_ZERO_FOR_QBASIC_OBSERVED_TAU",
            "fails if tau is a hidden-field functional outside q or chosen after residuals are seen",
        ),
        (
            "TAU4269_2_role_lock",
            "same tau across roles",
            "The zero is active only when tau_source=tau_charge=tau_clock=tau_orbit=tau_PPN=tau_readout in the same local branch.",
            "CONDITIONAL_ROLE_LOCK",
            "split source, clock, orbital or PPN time choices become R_tau_split",
        ),
        (
            "TAU4269_3_surface_reference_lock",
            "fixed reference and surfaces",
            "H_ref is fixed before variation and S_link is fixed or Lie_tau-dragged, so tau drift cannot re-enter through moving surfaces or a fitted reference subtraction.",
            "CONDITIONAL_REFERENCE_SURFACE_LOCK",
            "moving surfaces and post-fit references remain residual rows",
        ),
        (
            "TAU4269_4_C1_zero",
            "fixed observed-tau C1 silence",
            "A branch-selected tau_obs(q), fixed units and fixed orientation have zero local derivative along hidden vertical directions in the compact test window.",
            "CONDITIONAL_C1_ZERO_FOR_QBASIC_TAU",
            "time-dependent readout maps, lapse rescaling or clock calibration drift reopen C1 bounds",
        ),
        (
            "TAU4269_5_global_tau_identity_not_claimed",
            "global tau theorem guard",
            "4269 does not prove all MTS private time notions are the same; it only removes the observed-tau Dq component inside the selected q-basic branch.",
            "GLOBAL_PARENT_TAU_IDENTITY_NOT_CLAIMED",
            "the 2597 audit remains active outside this local observed-tau selector",
        ),
        (
            "TAU4269_6_tau_bound_fallback",
            "tau residual fallback",
            "If any tau/source/clock/orbit/frame/readout clause fails, retain epsilon_tau <= |R_tau_lock|/M_H_ref with no cancellation against geometry or boundary rows.",
            "RETAINED_BOUND_FORK",
            "tau residuals must be scored in clock, PPN, orbital and source-charge arenas",
        ),
    ]
    return [
        {
            **common(),
            "theorem_id": theorem_id,
            "name": name,
            "statement": statement,
            "status": status,
            "guard": guard,
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
        for theorem_id, name, statement, status, guard in raw
    ]


def residual_split_rows() -> List[Dict[str, str]]:
    raw = [
        ("TRES4269_0_tau_split", "R_tau_split", "source/charge/clock/orbit/PPN/readout use different time generators", "Dq_tau", "RETAINED_IF_NONZERO"),
        ("TRES4269_1_surface_motion", "R_surface_motion", "linking surfaces move independently of the selected tau flow", "Dq_tau", "RETAINED_IF_NONZERO"),
        ("TRES4269_2_frame_coframe", "R_frame_coframe", "observed coframe or frame used by clocks/readout differs from the source-charge coframe", "Dq_tau", "RETAINED_IF_NONZERO"),
        ("TRES4269_3_clock_readout", "R_clock_readout", "clock/redshift convention is selected after comparison or drifts with hidden fields", "Dq_tau", "RETAINED_IF_NONZERO"),
        ("TRES4269_4_orbital_readout", "R_orbital_readout", "orbit/PPN coordinates are tuned after fitting rather than selected by the parent branch", "Dq_tau", "RETAINED_IF_NONZERO"),
        ("TRES4269_5_units_lapse", "R_units_lapse_rescaling", "unit, lapse, orientation or normalization rescaling changes the tau row", "Dq_tau", "RETAINED_IF_NONZERO"),
        ("TRES4269_6_private_memory_time", "R_private_memory_tau", "private process/memory time leaks into observed clock/source/orbit readout", "Dq_tau", "RETAINED_IF_NONZERO"),
        ("TRES4269_7_geometry_separation", "epsilon_geom", "coframe/metric geometry drift is not killed by the tau lock", "Dq_geom", "RETAINED_SEPARATE_GATE"),
    ]
    return [
        {
            **common(),
            "split_id": split_id,
            "coefficient_or_tail": coefficient,
            "meaning": meaning,
            "assigned_gate": gate,
            "4269_status": status,
            "deformation_requirement": "MISSING_SOURCE_BACKED_BOUND_OR_ZERO_PROOF_IF_REOPENED",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
        for split_id, coefficient, meaning, gate, status in raw
    ]


def adoption_rows() -> List[Dict[str, str]]:
    return [
        {
            **common(),
            "adoption_id": "ADOPT4269_Dq_tau",
            "component": "Dq_tau",
            "old_epsilon": "MISSING_ZERO_PROOF_OR_PROFILE_Dq_tau",
            "new_epsilon": "0.0",
            "new_epsilon_C1": "0.0",
            "adoption_status": "ADOPTED_CONDITIONAL_ZERO_FOR_QBASIC_OBSERVED_TAU_BRANCH_ONLY",
            "source_path": str(FORMAL_PATH),
            "conditions": (
                "tau_obs=tau_bar(q) is selected before variation; tau_source=tau_charge=tau_clock=tau_orbit=tau_PPN=tau_readout; "
                "S_link is fixed or tau-dragged; H_ref is fixed before comparison; one observed coframe and common units/orientation/normalization are used; "
                "split tau, lapse rescaling, moving surfaces and private memory-time leakage are routed as tau residuals"
            ),
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
    ]


def component_candidate_rows() -> List[Dict[str, str]]:
    previous = csv_rows(LIVE_COMPONENT_CANDIDATE_PATH)
    reduced_geom_4270 = dq_geom_4270_reduced_row()
    core_geom_4271 = dq_geom_4271_core_row()
    bound_geom_4272 = dq_geom_4272_bound_row()
    if not previous:
        previous = [
            {
                **common(),
                "candidate_id": "DQ_COORDINATE_SEMINORM_SMOKE_4255",
                "probe_id": probe,
                "weight": "1.0",
                "epsilon": f"MISSING_ZERO_PROOF_OR_PROFILE_{probe}",
                "epsilon_C1": f"MISSING_C1_ZERO_PROOF_OR_PROFILE_{probe}",
                "source_path": str(FORMAL_PATH),
                "valid_for_claim": "False",
            }
            for probe in PROBE_ORDER
        ]
    output: List[Dict[str, str]] = []
    seen = set()
    for row in previous:
        probe = row.get("probe_id", "")
        if not probe:
            continue
        updated = dict(row)
        updated.update(common())
        if probe == "Dq_tau":
            updated["epsilon"] = "0.0"
            updated["epsilon_C1"] = "0.0"
            updated["source_path"] = str(FORMAL_PATH)
            updated["valid_for_claim"] = "False"
        output.append(updated)
        seen.add(probe)
    for probe in PROBE_ORDER:
        if probe not in seen:
            output.append(
                {
                    **common(),
                    "candidate_id": "DQ_COORDINATE_SEMINORM_SMOKE_4255",
                    "probe_id": probe,
                    "weight": "1.0",
                    "epsilon": "0.0" if probe == "Dq_tau" else f"MISSING_ZERO_PROOF_OR_PROFILE_{probe}",
                    "epsilon_C1": "0.0" if probe == "Dq_tau" else f"MISSING_C1_ZERO_PROOF_OR_PROFILE_{probe}",
                    "source_path": str(FORMAL_PATH),
                    "valid_for_claim": "False",
                }
            )
    if reduced_geom_4270:
        for row in output:
            if row.get("probe_id") == "Dq_geom":
                row["epsilon"] = reduced_geom_4270.get("new_epsilon", "MISSING_REDUCED_EPSILON_GEOM_CORE_COFRAME_SHADOW")
                row["epsilon_C1"] = reduced_geom_4270.get("new_epsilon_C1", "MISSING_REDUCED_C1_GEOM_CORE_COFRAME_SHADOW")
                row["source_path"] = str(FORMAL_4270_PATH)
                row["valid_for_claim"] = "False"
    if core_geom_4271:
        for row in output:
            if row.get("probe_id") == "Dq_geom":
                row["epsilon"] = core_geom_4271.get("new_epsilon", "MISSING_CORE_FRAME_COUPLING_ZERO_OR_NUMERIC_CG_BDIS_BOUND")
                row["epsilon_C1"] = core_geom_4271.get("new_epsilon_C1", "MISSING_C1_CORE_FRAME_COUPLING_ZERO_OR_NUMERIC_CG_BDIS_BOUND")
                row["source_path"] = str(FORMAL_4271_PATH)
                row["valid_for_claim"] = "False"
    if bound_geom_4272:
        for row in output:
            if row.get("probe_id") == "Dq_geom":
                row["epsilon"] = bound_geom_4272.get("new_epsilon", "MISSING_SCOREABLE_CG_BDIS_FRAME_VECTOR_INPUTS")
                row["epsilon_C1"] = bound_geom_4272.get("new_epsilon_C1", "MISSING_C1_SCOREABLE_CG_BDIS_FRAME_VECTOR_INPUTS")
                row["source_path"] = str(FORMAL_4272_PATH)
                row["valid_for_claim"] = "False"
    return output


def decision_rows() -> List[Dict[str, str]]:
    raw = [
        (
            "DEC4269_0_adopt_tau",
            "Adopt Dq_tau=0 for the q-basic observed-tau/reference-time branch.",
            "The observed tau row factors through q before variation and is role-locked across source charge, clocks, orbit, PPN and readout.",
            NEXT_TARGET,
        ),
        (
            "DEC4269_1_no_global_time_claim",
            "Do not claim all MTS/private time notions are derived identical.",
            "The theorem is about the observed local time generator used by tested clocks/source/orbit/readout, not a global metaphysical time identity.",
            "Keep the 2597 nonclaim guard attached.",
        ),
        (
            "DEC4269_2_4254_progress",
            "4254 should now lose Dq_tau from the missing list while staying blocked by Dq_geom and tomography constants.",
            "This moves the local-GR ladder from tau/source-time leakage to geometry/coframe and numeric tomography gates.",
            "Rerun 4254 after 4269.",
        ),
    ]
    return [
        {
            **common(),
            "decision_id": decision_id,
            "decision": decision,
            "reason": reason,
            "next_action": next_action,
            "valid_for_claim": "False",
        }
        for decision_id, decision, reason, next_action in raw
    ]


def firewall_rows() -> List[Dict[str, str]]:
    raw = [
        ("FW4269_0_public_local_GR", "Do not claim local GR/PPN/R10/clock/orbital pass from tau closure alone.", "Dq_geom, tomography constants and empirical bounds remain live."),
        ("FW4269_1_private_time_leak", "Do not erase private process/memory time if it affects observed clocks or source charge.", "Route it as R_private_memory_tau."),
        ("FW4269_2_postfit_tau", "Do not choose tau, lapse, PPN coordinates or clock units after looking at residuals.", "Route post-fit conventions as R_clock_readout/R_orbital_readout/R_units_lapse_rescaling."),
        ("FW4269_3_geometry_smuggling", "Do not use the tau lock to kill coframe/metric geometry drift.", "Dq_geom remains separate."),
        ("FW4269_4_MHref", "Do not normalize any tau residual claim by a missing or fitted M_H_ref.", "M_H_ref remains a separate denominator gate."),
    ]
    return [
        {
            **common(),
            "firewall_id": firewall_id,
            "forbidden_move": forbidden,
            "required_gate": gate,
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
        for firewall_id, forbidden, gate in raw
    ]


def status_rows() -> List[Dict[str, str]]:
    return [
        {
            **common(),
            "status_id": "STATUS4269_0",
            "summary": (
                "4269 moves Dq_tau from missing to a conditional zero for the q-basic observed-tau/reference-time branch, "
                "while retaining split tau, lapse rescaling, post-fit clock/orbit readout, moving surfaces and private time leakage as explicit residuals."
            ),
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
    ]


def next_target_rows() -> List[Dict[str, str]]:
    return [
        {
            **common(),
            "next_target": NEXT_TARGET,
            "objective": "Attack Dq_geom: observed coframe/metric descent versus a real epsilon_geom component fill.",
            "avoid": "Do not let tau/reference-time closure substitute for the missing geometry/coframe descent theorem.",
            "valid_for_claim": "False",
        }
    ]


def formal_doc() -> str:
    return f"""
# 285 - PPC4161 Dq-tau reference-time lock or tau residual bound

Marker: `{MARKER}`

Branch: `{BRANCH}`

Decision: `{DECISION}`

## Private nonclaim

4269 does not prove public local GR, PPN, R10, WEP, clock, orbital, or global MTS time closure.

It adopts:

```text
Dq_tau = 0
```

only for the q-basic observed-tau/reference-time branch.

## What is actually proved

The observed local time generator is treated as part of the public readout structure:

```text
tau_obs = tau_bar(q).
```

For hidden vertical variations `v in ker(Dq)`:

```text
delta_v tau_obs = D tau_bar[Dq[v]] = 0.
```

The row is active only when the same observed tau is used across the tested roles:

```text
tau_source = tau_charge = tau_clock = tau_orbit = tau_PPN = tau_readout.
```

The reference and surfaces must also be fixed before comparison:

```text
H_ref fixed before variation,
S_link fixed or Lie_tau-dragged,
one e_obs(q) and common units/orientation/normalization.
```

Then:

```text
Dq_tau = 0,
Dq_tau_C1 = 0.
```

## What is not proved

This is not a global proof that every MTS/private process-time variable is identical to clock proper time. A private time variable is allowed only if it does not leak into observed clock/source/orbit/readout tau. If it does leak, it is scored.

## Tau residual tax

If any of these exist:

```text
R_tau_split,
R_surface_motion,
R_frame_coframe,
R_clock_readout,
R_orbital_readout,
R_units_lapse_rescaling,
R_private_memory_tau,
```

they are retained as:

```text
epsilon_tau <= |R_tau_lock| / M_H_ref.
```

No cancellation against geometry, boundary, EM, matter, source-readout or coefficient rows is allowed.

## 4254 feed

The live component candidate is updated:

```text
Dq_tau = 0.0,
Dq_tau_C1 = 0.0.
```

The row remains `valid_for_claim=false` because the complete 4254 source-probe/tomography gate still needs geometry and constants.

## Next target

`{NEXT_TARGET}` should attack `Dq_geom`.
"""


def checkpoint_doc() -> str:
    return f"""
# 4269 - Y5 R2FR Dq-tau reference-time lock or tau residual bound

Packet marker: `{PACKET_MARKER}`

## Result

4269 adopts:

```text
Dq_tau = 0.0,
Dq_tau_C1 = 0.0
```

for the q-basic observed-tau/reference-time branch only.

## Human translation

This says the local clock/source/orbit/readout time used in tests is one parent-selected observed time, chosen before variation and before comparison. If we secretly use one time for source charge, another for clocks, another for orbits, or a private memory time that leaks into clocks, that is not zero; it becomes a residual.

## Why this is progress

4254 had two live Dq holdouts after 4268:

```text
Dq_geom,
Dq_tau.
```

4269 removes the tau leg under a precise branch contract. That leaves the real hard piece: geometry/coframe descent plus the numeric tomography constants.

## Claim firewall

This is private and nonclaim. It does not prove public local GR and does not derive a universal theory of time. It only locks the observed tau row used by local tests.
"""


def validation_rows(paths: Dict[str, Path]) -> List[Dict[str, str]]:
    sources = csv_rows(paths["sources"])
    theorems = csv_rows(paths["theorems"])
    split = csv_rows(paths["split"])
    adoption = csv_rows(paths["adoption"])
    local_candidate = csv_rows(paths["local_candidate"])
    live_candidate = csv_rows(LIVE_COMPONENT_CANDIDATE_PATH)
    live_tau = [row for row in live_candidate if row.get("probe_id") == "Dq_tau"]
    live_geom = [row for row in live_candidate if row.get("probe_id") == "Dq_geom"]
    live_boundary = [row for row in live_candidate if row.get("probe_id") == "Dq_boundary_projector"]
    live_coeff = [row for row in live_candidate if row.get("probe_id") == "Dq_coeff"]
    live_source = [row for row in live_candidate if row.get("probe_id") == "Dq_source_readout"]
    live_matter = [row for row in live_candidate if row.get("probe_id") == "Dq_matter"]
    live_theta = [row for row in live_candidate if row.get("probe_id") == "Dq_theta_marker"]
    live_em = [row for row in live_candidate if row.get("probe_id") == "Dq_EM"]
    rows = [
        ("VAL4269_0_sources_exist", all(row["exists"] == "True" for row in sources), "all source paths exist"),
        ("VAL4269_1_needles_found", all(row["required_text_found"] == "True" for row in sources), "all source needles found"),
        (
            "VAL4269_2_qbasic_tau_theorem",
            any(row["status"] == "CONDITIONAL_ZERO_FOR_QBASIC_OBSERVED_TAU" for row in theorems),
            "q-basic observed-tau theorem emitted",
        ),
        (
            "VAL4269_3_tau_residuals_retained",
            any(row["4269_status"] == "RETAINED_IF_NONZERO" and row["coefficient_or_tail"] == "R_tau_split" for row in split)
            and any(row["coefficient_or_tail"] == "R_units_lapse_rescaling" for row in split)
            and any(row["assigned_gate"] == "Dq_geom" for row in split),
            "tau residuals and geometry separation retained",
        ),
        (
            "VAL4269_4_adoption_row",
            bool(adoption)
            and adoption[0]["new_epsilon"] == "0.0"
            and adoption[0]["adoption_status"] == "ADOPTED_CONDITIONAL_ZERO_FOR_QBASIC_OBSERVED_TAU_BRANCH_ONLY",
            "Dq_tau adoption row emitted",
        ),
        (
            "VAL4269_5_local_candidate_numeric",
            any(row.get("probe_id") == "Dq_tau" and row.get("epsilon") == "0.0" and row.get("epsilon_C1") == "0.0" for row in local_candidate),
            "local 4269 candidate has numeric tau zero",
        ),
        (
            "VAL4269_6_live_4254_updated",
            bool(live_tau)
            and live_tau[0].get("epsilon") == "0.0"
            and live_tau[0].get("epsilon_C1") == "0.0"
            and live_tau[0].get("source_path") == str(FORMAL_PATH),
            "live 4254 candidate Dq_tau updated",
        ),
        (
            "VAL4269_7_preserve_prior_adoptions",
            bool(live_em)
            and live_em[0].get("epsilon") == "0.0"
            and bool(live_theta)
            and live_theta[0].get("epsilon") == "0.0"
            and bool(live_matter)
            and live_matter[0].get("epsilon") == "0.0"
            and bool(live_source)
            and live_source[0].get("epsilon") == "0.0"
            and bool(live_coeff)
            and live_coeff[0].get("epsilon") == "0.0"
            and bool(live_boundary)
            and live_boundary[0].get("epsilon") == "0.0",
            "prior Dq_EM, Dq_theta_marker, Dq_matter, Dq_source_readout, Dq_coeff and Dq_boundary_projector adoptions preserved",
        ),
        (
            "VAL4269_8_geom_not_smuggled",
            bool(live_geom) and live_geom[0].get("epsilon") != "0.0",
            "Dq_geom remains live after tau closure",
        ),
        (
            "VAL4269_9_global_tau_nonclaim_guard",
            any(row["source_id"] == "SRC4269_06_2597_nonclaim_guard" and row["required_text_found"] == "True" for row in sources)
            and any(row["status"] == "GLOBAL_PARENT_TAU_IDENTITY_NOT_CLAIMED" for row in theorems),
            "global tau identity remains nonclaim",
        ),
        ("VAL4269_10_claim_row", CLAIM_ID in read_text(FORMAL / "02-claims-register.csv"), "claim register row added"),
        ("VAL4269_11_formal_doc", MARKER in read_text(FORMAL_PATH), "formal marker present"),
        ("VAL4269_12_checkpoint_doc", PACKET_MARKER in read_text(DOC_PATH), "checkpoint marker present"),
    ]
    return [
        {
            **common(),
            "check_id": check_id,
            "description": description,
            "passed": str(bool(passed)),
            "evidence": "generated_artifacts",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
        for check_id, passed, description in rows
    ]


def main() -> None:
    SOURCE_DIR.mkdir(parents=True, exist_ok=True)
    source_path = SOURCE_DIR / "P8_Y5_R2FR_4269_SOURCE_REGISTER.csv"
    theorem_path = SOURCE_DIR / "P8_Y5_R2FR_4269_TAU_LOCK_THEOREM.csv"
    split_path = SOURCE_DIR / "P8_Y5_R2FR_4269_TAU_RESIDUAL_SPLIT_ROWS.csv"
    adoption_path = SOURCE_DIR / "P8_Y5_R2FR_4269_DQ_TAU_ADOPTION.csv"
    decision_path = SOURCE_DIR / "P8_Y5_R2FR_4269_DECISION.csv"
    firewall_path = SOURCE_DIR / "P8_Y5_R2FR_4269_CLAIM_FIREWALL.csv"
    status_path = SOURCE_DIR / "P8_Y5_R2FR_4269_STATUS.csv"
    next_path = SOURCE_DIR / "P8_Y5_R2FR_4269_NEXT_TARGET.csv"

    component_candidate = component_candidate_rows()
    write_csv(source_path, source_rows())
    write_csv(theorem_path, tau_lock_theorem_rows())
    write_csv(split_path, residual_split_rows())
    write_csv(adoption_path, adoption_rows())
    write_csv(LOCAL_COMPONENT_CANDIDATE_PATH, component_candidate)
    write_csv(LIVE_COMPONENT_CANDIDATE_PATH, component_candidate)
    write_csv(decision_path, decision_rows())
    write_csv(firewall_path, firewall_rows())
    write_csv(status_path, status_rows())
    write_csv(next_path, next_target_rows())
    write_text(FORMAL_PATH, formal_doc())
    write_text(DOC_PATH, checkpoint_doc())
    append_claim()

    paths = {
        "sources": source_path,
        "theorems": theorem_path,
        "split": split_path,
        "adoption": adoption_path,
        "local_candidate": LOCAL_COMPONENT_CANDIDATE_PATH,
    }
    validation = validation_rows(paths)
    write_csv(VALIDATION_PATH, validation)
    failed = [row for row in validation if row["passed"] != "True"]
    print(f"{CHECKPOINT}: wrote 8 csv artifacts plus validation")
    print(f"{CHECKPOINT}: validation rows={len(validation)} failed={len(failed)}")
    print(f"{CHECKPOINT}: decision={DECISION}")


if __name__ == "__main__":
    main()

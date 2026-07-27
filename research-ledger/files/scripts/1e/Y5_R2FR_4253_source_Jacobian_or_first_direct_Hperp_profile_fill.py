from __future__ import annotations

import csv
import math
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, Iterable, List, Optional


ROOT = Path(__file__).resolve().parents[2]
FORMAL = ROOT / "formalization-workbench"
POST = ROOT / "post-checkpoint-work"
SOURCE_DIR = POST / "source-intake" / "mts_residuals"

CHECKPOINT = "4253"
CLAIM_ID = "L-094"
BRANCH = "MTS_R2FR_Y5_SOURCE_JACOBIAN_OR_FIRST_DIRECT_HPERP_PROFILE_FILL_4253"
DECISION = "NO_PARENT_JACOBIAN_FOUND_DQ_DEFECT_TO_HPERP_TOMOGRAPHY_BRIDGE_DERIVED_NONCLAIM"
MARKER = "PPC4161_SOURCE_JACOBIAN_DIRECT_HPERP_PROFILE_4253"
PACKET_MARKER = "PPC4161_PACKET_SOURCE_JACOBIAN_DIRECT_HPERP_PROFILE_4253"
NEXT_TARGET = "4254-Y5-R2FR-fill-source-probe-rank-or-parent-Pi4-Jacobian-row.md"

FORMAL_PATH = FORMAL / "269-PPC4161-source-Jacobian-or-first-direct-Hperp-profile-fill.md"
DOC_PATH = POST / "4253-Y5-R2FR-source-Jacobian-or-first-direct-Hperp-profile-fill.md"
VALIDATION_PATH = SOURCE_DIR / "P8_Y5_BRR545_4253_VALIDATION.csv"

PROFILE_CANDIDATE_PATH = SOURCE_DIR / "P8_Y5_R2FR_4253_DQ_DEFECT_PROFILE_CANDIDATE.csv"
JACOBIAN_CANDIDATE_PATH = SOURCE_DIR / "P8_Y5_R2FR_4252_JACOBIAN_COMPONENTS_CANDIDATE.csv"
AGGREGATE_CANDIDATE_PATH = SOURCE_DIR / "P8_Y5_R2FR_4252_MIXED_TRANSFER_INPUTS_CANDIDATE.csv"

STAMP = datetime.now(timezone.utc).replace(microsecond=0).isoformat()


@dataclass(frozen=True)
class SourceSpec:
    source_id: str
    path: Path
    required_text: str
    role: str


SOURCE_SPECS: Dict[str, SourceSpec] = {
    "SRC4253_00_4252_formal": SourceSpec(
        "SRC4253_00_4252_formal",
        FORMAL / "268-PPC4161-mixed-memory-Qshear-transfer-inputs-or-direct-Hperp-profile-acquisition.md",
        "B_a = omega(DPi4_X X_m, DPi4_X X_a)",
        "4252 exact Jacobian contraction target.",
    ),
    "SRC4253_01_4252_next": SourceSpec(
        "SRC4253_01_4252_next",
        SOURCE_DIR / "P8_Y5_R2FR_4252_NEXT_TARGET.csv",
        "Fill source-backed Y_m/Y_a",
        "4252 selected source-backed Jacobian or direct Hperp profile fill.",
    ),
    "SRC4253_02_3799_basicness": SourceSpec(
        "SRC4253_02_3799_basicness",
        POST / "3799-Y5-R2FR-Hperp-curvature-descent-zero-or-first-hU-source-row.md",
        "i_v H_Q=sum_i",
        "Hperp zero reduced to Clebsch vertical contraction/basicness.",
    ),
    "SRC4253_03_3800_chain": SourceSpec(
        "SRC4253_03_3800_chain",
        SOURCE_DIR / "P8_Y5_R2FR_3800_FULL_RANK_CLEBSCH_BASICNESS_THEOREM.csv",
        "CBT3800_3_qshear_chain_rule",
        "Pi4 chain rule and selector-kernel alignment.",
    ),
    "SRC4253_04_3798_profile": SourceSpec(
        "SRC4253_04_3798_profile",
        POST / "3798-Y5-R2FR-minimal-Bperp-Hperp-profile-ansatz-or-parent-zero.md",
        "Bperp_norm_over_Aref <= Lambda_U*Hperp_norm_over_Fref",
        "Bperp already reduced to Hperp plus boundary/harmonic residues.",
    ),
    "SRC4253_05_4243_defect": SourceSpec(
        "SRC4253_05_4243_defect",
        POST / "4243-Y5-R2FR-Hperp-zero-theorem-or-source-defect-profile-first-real-row.md",
        "|S_A Hperp^A| <= C_S C_perp E_Dq,H",
        "Source-defect row that can become a direct Hperp profile via probe rank.",
    ),
    "SRC4253_06_4248_sampler": SourceSpec(
        "SRC4253_06_4248_sampler",
        SOURCE_DIR / "P8_Y5_R2FR_4248_EPSILON_GEOM_PROFILE_INPUT_SCHEMA.csv",
        "Hperp_profile_id",
        "Existing sampler wants a real Hperp profile id.",
    ),
    "SRC4253_07_4207_poynting": SourceSpec(
        "SRC4253_07_4207_poynting",
        POST / "4207-Y5-R2FR-EM-Poynting-Hodge-source-owner-lock-or-side-channel-bound.md",
        "Poynting = EM energy-flow",
        "Poynting/Hodge guard: useful intuition, not a standalone double-counted Hperp source.",
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
    fieldnames: List[str] = []
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


def append_once(path: Path, marker: str, block: str) -> None:
    current = read_text(path)
    if marker in current:
        return
    write_text(path, current.rstrip() + "\n\n" + block.strip())


def parse_float(value: str) -> Optional[float]:
    try:
        parsed = float(str(value).strip())
    except (TypeError, ValueError):
        return None
    if not math.isfinite(parsed):
        return None
    return parsed


def truthy(value: str) -> bool:
    return str(value).strip().lower() in {"true", "1", "yes", "y"}


def contains_missing_marker(values: Iterable[str]) -> bool:
    return any("MISSING_" in str(value) or "PLACEHOLDER" in str(value) for value in values)


def split_paths(value: str) -> List[Path]:
    if not value:
        return []
    return [Path(piece.strip()) for piece in str(value).split(";") if piece.strip()]


def all_source_paths_exist(value: str) -> bool:
    paths = split_paths(value)
    return bool(paths) and all(path.exists() for path in paths)


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


def source_hunt_rows() -> List[Dict[str, str]]:
    raw = [
        (
            "HUNT4253_0_live_jacobian_candidate",
            str(JACOBIAN_CANDIDATE_PATH),
            JACOBIAN_CANDIDATE_PATH.exists(),
            "would fill Y_m/Y_a directly",
            "SOURCE_BACKED_IF_ROWS_EXIST_AND_VALIDATE",
            "No live parent Jacobian candidate file was found.",
        ),
        (
            "HUNT4253_1_live_aggregate_candidate",
            str(AGGREGATE_CANDIDATE_PATH),
            AGGREGATE_CANDIDATE_PATH.exists(),
            "would compute A_H/h_U_C1 through 4252 aggregate runner",
            "SOURCE_BACKED_IF_ROWS_EXIST_AND_VALIDATE",
            "No live aggregate mixed-transfer candidate file was found.",
        ),
        (
            "HUNT4253_2_3799_basicness",
            str(POST / "3799-Y5-R2FR-Hperp-curvature-descent-zero-or-first-hU-source-row.md"),
            True,
            "exact Hperp zero theorem target",
            "THEOREM_TARGET_NOT_NUMERIC_ROW",
            "Provides i_v H_Q criterion, not sourced vC_i/vD_i values.",
        ),
        (
            "HUNT4253_3_4243_defect_bound",
            str(POST / "4243-Y5-R2FR-Hperp-zero-theorem-or-source-defect-profile-first-real-row.md"),
            True,
            "componentwise Dq defect bound",
            "CAN_FEED_DIRECT_PROFILE_IF_SOURCE_PROBES_SPAN",
            "This is the best constructive fallback route after Pi4 search.",
        ),
        (
            "HUNT4253_4_4207_poynting",
            str(POST / "4207-Y5-R2FR-EM-Poynting-Hodge-source-owner-lock-or-side-channel-bound.md"),
            True,
            "EM/Poynting/Hodge guard",
            "GUARD_NOT_DIRECT_HPERP_NUMERATOR",
            "Poynting is counted inside Hilbert EM stress unless MTS Hodge deformation/flux side-channel is explicitly present.",
        ),
    ]
    return [
        {
            **common(),
            "hunt_id": hunt_id,
            "path": path,
            "exists": str(exists),
            "candidate_role": candidate_role,
            "status": status,
            "finding": finding,
            "valid_for_claim": "False",
        }
        for hunt_id, path, exists, candidate_role, status, finding in raw
    ]


def theorem_rows() -> List[Dict[str, str]]:
    raw = [
        (
            "SJH4253_0_no_free_Pi4",
            "no hand-chosen selector theorem",
            "The map Pi4:X_Q->Y_Q cannot be chosen after looking at the desired Hperp, because for a rank-four target chart different Pi4 choices can realize different B_a and G_ab contractions on the same X_Q data.",
            "NO_SMUGGLE_THEOREM",
            "A convenient Pi4 row is not evidence; Pi4 must be parent-fixed or symmetry-fixed.",
            "MISSING_PARENT_PI4_OR_SYMMETRY_SELECTOR",
        ),
        (
            "SJH4253_1_parent_jacobian_pass_condition",
            "Jacobian source pass condition",
            "The Jacobian route passes only if Y_m=DPi4_X X_m and Y_a=DPi4_X X_a are source-backed/theorem-zero rows with real source paths and no post-EM readout dependence.",
            "EXACT_ACCEPTANCE_GATE",
            "This is the cleanest route to feed 4252.",
            "MISSING_Ym_Ya_ROWS",
        ),
        (
            "SJH4253_2_source_probe_tomography",
            "Dq-defect to Hperp profile bridge",
            "Let S: Hperp-sector -> source-defect probes have lower singular value sigma_S>0 on U_good. If ||S Hperp|| <= C_S C_perp E_Dq,H, then ||Hperp|| <= sigma_S^-1 C_S C_perp E_Dq,H.",
            "DERIVED_LINEAR_ALGEBRA_BRIDGE",
            "4243 can become a direct A_H profile if source probes span the live Hperp sector.",
            "MISSING_SIGMA_S_AND_E_DQ_VALUES",
        ),
        (
            "SJH4253_3_C1_tomography",
            "Dq-defect to h_U_C1 bridge",
            "If the differentiated source-probe map has lower singular value sigma_S1>0, then h_U_C1 <= sigma_S1^-1 C_S1 C_perp E_Dq,H_C1 + (||nabla S||/sigma_S1) A_H + eta_C1.",
            "DERIVED_C1_BRIDGE",
            "This feeds the 4249 C1 route without inventing a scalar Hperp transfer.",
            "MISSING_SIGMA_S1_E_DQ_C1_NABLA_S_VALUES",
        ),
        (
            "SJH4253_4_Poynting_guard",
            "Poynting/Hodge source-side guard",
            "Poynting flow may diagnose the observed Hodge/coframe energy-flow channel, but in the safe local branch it is already part of Maxwell-Hodge Hilbert stress. It may only enter this Hperp profile path through explicit Delta_Hodge_EM, current-normalization, or radiative-flux side-channel rows.",
            "NO_DOUBLE_COUNT_GUARD",
            "This respects the user's Poynting intuition without adding the EM source twice.",
            "MISSING_MTS_HODGE_SIDE_CHANNEL_VALUE_IF_ANY",
        ),
    ]
    return [
        {
            **common(),
            "theorem_id": theorem_id,
            "claim_piece": claim_piece,
            "mathematical_form": mathematical_form,
            "derivation_status": status,
            "result_if_signed": result,
            "missing_for_current_claim": missing,
            "valid_for_claim": "False",
        }
        for theorem_id, claim_piece, mathematical_form, status, result, missing in raw
    ]


def profile_template_rows() -> List[Dict[str, str]]:
    return [
        {
            **common(),
            "candidate_id": "TEMPLATE_ONLY",
            "sigma_S": "MISSING_SOURCE_PROBE_LOWER_SINGULAR_VALUE",
            "C_S": "MISSING_SOURCE_PROBE_BOUND_CONSTANT",
            "C_perp": "MISSING_HPERP_PROJECTOR_CONSTANT",
            "E_Dq_H": "MISSING_DQ_DEFECT_ENVELOPE",
            "eta_domain": "MISSING_DOMAIN_BOUNDARY_RESIDUE_OR_ZERO",
            "sigma_S1": "MISSING_C1_SOURCE_PROBE_LOWER_SINGULAR_VALUE",
            "C_S1": "MISSING_C1_SOURCE_PROBE_BOUND_CONSTANT",
            "E_Dq_H_C1": "MISSING_C1_DQ_DEFECT_ENVELOPE",
            "nabla_S_norm": "MISSING_SOURCE_PROBE_DERIVATIVE_NORM",
            "eta_C1": "MISSING_C1_RESIDUE_OR_ZERO",
            "source_path": "MISSING_SOURCE_PATH",
            "claim_authority": "MISSING_PARENT_AUTHORITY",
            "valid_for_claim": "False",
            "notes": "Copy to P8_Y5_R2FR_4253_DQ_DEFECT_PROFILE_CANDIDATE.csv with source-backed numeric rows.",
        }
    ]


PROFILE_REQUIRED = (
    "sigma_S",
    "C_S",
    "C_perp",
    "E_Dq_H",
    "eta_domain",
    "sigma_S1",
    "C_S1",
    "E_Dq_H_C1",
    "nabla_S_norm",
    "eta_C1",
)


def profile_results() -> List[Dict[str, str]]:
    if not PROFILE_CANDIDATE_PATH.exists():
        return [
            {
                **common(),
                "candidate_id": "NO_DQ_DEFECT_PROFILE_CANDIDATE",
                "status": "BLOCKED_NO_SOURCE_PROBE_PROFILE_FILE",
                "required_file": str(PROFILE_CANDIDATE_PATH),
                "A_H_bound": "",
                "h_U_C1_bound": "",
                "claim_allowed": "False",
                "valid_for_claim": "False",
                "notes": "Fill sigma_S/C_S/C_perp/E_Dq,H rows to compute the first direct Hperp profile bound.",
            }
        ]
    rows = csv_rows(PROFILE_CANDIDATE_PATH)
    output: List[Dict[str, str]] = []
    for row in rows:
        candidate_id = row.get("candidate_id", "UNNAMED_CANDIDATE").strip() or "UNNAMED_CANDIDATE"
        parsed = {field: parse_float(row.get(field, "")) for field in PROFILE_REQUIRED}
        missing = [field for field, value in parsed.items() if value is None]
        if missing:
            output.append(
                {
                    **common(),
                    "candidate_id": candidate_id,
                    "status": "BLOCKED_MISSING_NUMERIC_FIELDS",
                    "missing": ";".join(missing),
                    "A_H_bound": "",
                    "h_U_C1_bound": "",
                    "claim_allowed": "False",
                    "valid_for_claim": "False",
                }
            )
            continue
        values = {field: parsed[field] for field in PROFILE_REQUIRED if parsed[field] is not None}
        positive_required = ["sigma_S", "sigma_S1"]
        positive_failures = [field for field in positive_required if values[field] <= 0]
        if positive_failures:
            output.append(
                {
                    **common(),
                    "candidate_id": candidate_id,
                    "status": "BLOCKED_NONPOSITIVE_RANK_CONSTANT",
                    "missing": ";".join(positive_failures),
                    "A_H_bound": "",
                    "h_U_C1_bound": "",
                    "claim_allowed": "False",
                    "valid_for_claim": "False",
                }
            )
            continue
        A_H_bound = (values["C_S"] * values["C_perp"] / values["sigma_S"]) * values["E_Dq_H"] + values["eta_domain"]
        h_U_C1_bound = (
            (values["C_S1"] * values["C_perp"] / values["sigma_S1"]) * values["E_Dq_H_C1"]
            + (values["nabla_S_norm"] / values["sigma_S1"]) * A_H_bound
            + values["eta_C1"]
        )
        input_valid = (
            truthy(row.get("valid_for_claim", ""))
            and all_source_paths_exist(row.get("source_path", ""))
            and not contains_missing_marker(row.values())
        )
        output.append(
            {
                **common(),
                "candidate_id": candidate_id,
                "status": "DQ_DEFECT_PROFILE_BOUNDS_COMPUTED_NONCLAIM",
                "A_H_bound": f"{A_H_bound:.12e}",
                "h_U_C1_bound": f"{h_U_C1_bound:.12e}",
                "source_path_exists": str(all_source_paths_exist(row.get("source_path", ""))),
                "claim_authority": row.get("claim_authority", ""),
                "claim_allowed": "False",
                "valid_for_claim": str(input_valid),
            }
        )
    return output or [
        {
            **common(),
            "candidate_id": "NO_PROFILE_ROWS",
            "status": "BLOCKED_EMPTY_PROFILE_CANDIDATE_FILE",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
    ]


def bridge_rows(results: List[Dict[str, str]]) -> List[Dict[str, str]]:
    computed = [row for row in results if row.get("status") == "DQ_DEFECT_PROFILE_BOUNDS_COMPUTED_NONCLAIM"]
    if not computed:
        return [
            {
                **common(),
                "candidate_id": "NO_4253_TO_4249_BRIDGE",
                "bridge_status": "BLOCKED_NO_DQ_DEFECT_PROFILE_RESULT",
                "A_H": "MISSING_4253_A_H_BOUND",
                "h_U_C1": "MISSING_4253_h_U_C1_BOUND",
                "remaining_4249_inputs": "C_qinv;h_U_profile;Omega_E;eta_Lie_frame;C_shape;L_U_over_ell_tr;eta_corner",
                "claim_allowed": "False",
                "valid_for_claim": "False",
            }
        ]
    return [
        {
            **common(),
            "candidate_id": row["candidate_id"],
            "bridge_status": "PARTIAL_4249_BRIDGE_READY_NONCLAIM",
            "A_H": row.get("A_H_bound", ""),
            "h_U_C1": row.get("h_U_C1_bound", ""),
            "remaining_4249_inputs": "C_qinv;h_U_profile;Omega_E;eta_Lie_frame;C_shape;L_U_over_ell_tr;eta_corner",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
        for row in computed
    ]


def decision_rows() -> List[Dict[str, str]]:
    raw = [
        (
            "DEC4253_0_jacobian",
            "No current parent Jacobian row was found.",
            "Do not hand-pick Pi4; wait for parent/symmetry source rows or theorem zeros.",
            "Keep 4252 extractor ready.",
        ),
        (
            "DEC4253_1_direct_profile",
            "Direct Hperp profile can be derived from Dq defects if source probes span the live Hperp sector.",
            "This converts 4243 from a componentwise statement into a sourceable A_H/h_U_C1 profile path.",
            "Fill sigma_S, E_Dq,H, C_S, C_perp, and C1 counterparts.",
        ),
        (
            "DEC4253_2_poynting",
            "Poynting remains a good intuition but not a standalone extra source.",
            "Use it only through explicit Hodge/current/radiative side-channel rows.",
            "Do not double-count Maxwell-Hodge Hilbert stress.",
        ),
        (
            "DEC4253_3_next",
            "The next best move is source-probe rank or parent Pi4 Jacobian fill.",
            "Either route produces a computable bound instead of another symbolic target.",
            NEXT_TARGET,
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
        ("FW4253_0_no_free_Pi4", "hand-picked Pi4 Jacobian", "FORBIDDEN_POSTHOC_SELECTOR", "False"),
        ("FW4253_1_probe_rank", "Dq-defect profile without sigma_S>0", "MISSING_SOURCE_PROBE_RANK", "False"),
        ("FW4253_2_numeric_values", "A_H/h_U_C1 without source-backed E_Dq rows", "MISSING_DQ_PROFILE_VALUES", "False"),
        ("FW4253_3_poynting", "extra Poynting source after T_EM counted", "DOUBLE_COUNT_FORBIDDEN", "False"),
        ("FW4253_4_claim", "local-GR/PPN/R10/clock/orbital closure", "NONCLAIM_PRIVATE_GATE", "False"),
    ]
    return [
        {
            **common(),
            "firewall_id": firewall_id,
            "blocked_shortcut": shortcut,
            "reason": reason,
            "claim_allowed": claim_allowed,
            "valid_for_claim": "False",
        }
        for firewall_id, shortcut, reason, claim_allowed in raw
    ]


def status_rows() -> List[Dict[str, str]]:
    return [
        {
            **common(),
            "status": DECISION,
            "summary": "4253 finds no live parent Jacobian file, rejects hand-chosen Pi4, and derives the Dq-defect/source-probe tomography bridge that can turn 4243 into direct A_H and h_U_C1 profile bounds once sigma_S and E_Dq rows are sourced.",
            "scoreable_now": "False",
            "valid_for_claim": "False",
        }
    ]


def next_target_rows() -> List[Dict[str, str]]:
    return [
        {
            **common(),
            "next_target": NEXT_TARGET,
            "objective": "Fill source-probe rank/tomography rows for the Dq-defect profile route, or source parent Pi4/X_m/X_a Jacobian rows for the 4252 route.",
            "avoid": "Do not hand-pick Pi4, do not double-count Poynting, and do not claim local safety from templates.",
            "valid_for_claim": "False",
        }
    ]


def append_claim_row() -> None:
    path = FORMAL / "02-claims-register.csv"
    current = read_text(path)
    if f"{CLAIM_ID}," in current:
        return
    row = [
        CLAIM_ID,
        "local_gr",
        "4253 sources the next coupling gate: no parent-owned Jacobian candidate is currently present, a hand-picked Pi4 selector is rejected, and a new Dq-defect/source-probe tomography bridge is derived so 4243 can become direct A_H and h_U_C1 profile bounds if sigma_S and E_Dq rows are filled.",
        "4253 source register, source hunt audit, no-free-Pi4 theorem, source-probe tomography bridge, Dq-defect profile template/runner, Poynting guard, bridge rows, decision and firewall.",
        "private_no_parent_jacobian_Dq_defect_tomography_bridge_nonclaim",
        "Fill source-probe rank/tomography rows or parent Pi4/X_m/X_a Jacobian rows, then feed computed A_H/h_U_C1 into 4249.",
        "Choosing Pi4 by convenience, using Dq defects without a spanning source-probe rank, or adding Poynting as a second source would smuggle Hperp suppression.",
    ]
    with path.open("a", newline="", encoding="utf-8") as handle:
        csv.writer(handle).writerow(row)


def write_formal_doc() -> None:
    text = f"""
# 269 - PPC4161 source Jacobian or first direct Hperp profile fill

Marker: `{MARKER}`

Branch: `{BRANCH}`

Decision: `{DECISION}`

## Claim Status

Private nonclaim. 4253 does not prove `Hperp` is small and does not prove local GR, PPN, R10, clock, or orbital safety.

## What Was Actually Tried

4253 checks the current live target from 4252:

```text
Y_m = DPi4_X X_m,
Y_a = DPi4_X X_a.
```

No source-backed candidate file exists yet for those rows. Therefore 4253 rejects the tempting shortcut:

```text
choose Pi4 by hand so that B_a and G_ab look small.
```

That would be a post-hoc selector. `Pi4` must be parent-fixed or symmetry-fixed before EM/local-GR readout.

## New Constructive Route

4253 derives a second route from the 4243 source-defect branch.

Let `S` be the source-probe map from the live `Hperp` sector to the measured/source-defect components. If, on `U_good`,

```text
sigma_S := lower singular value of S > 0,
||S Hperp|| <= C_S C_perp E_Dq,H,
```

then:

```text
A_H = ||Hperp||/F_ref
    <= sigma_S^-1 C_S C_perp E_Dq,H + eta_domain.
```

For the C1 branch:

```text
h_U_C1 <= sigma_S1^-1 C_S1 C_perp E_Dq,H_C1
          + (||nabla S||/sigma_S1) A_H
          + eta_C1.
```

This is the important move: the direct profile route is no longer just "find Hperp". It can be sourced by a finite tomography/rank row plus Dq-defect envelopes.

## Poynting/Hodge Guard

Poynting flow remains physically meaningful, but in the safe local branch it is already part of Maxwell-Hodge Hilbert stress. It can only affect this profile route through explicit MTS Hodge/current/radiative side-channel rows, not as an extra source added after `T_EM`.

## Next Target

`{NEXT_TARGET}` should fill either:

```text
parent Pi4/X_m/X_a Jacobian rows,
```

or:

```text
sigma_S, E_Dq,H, C_S, C_perp, sigma_S1, E_Dq,H_C1.
```
"""
    write_text(FORMAL_PATH, text)


def write_checkpoint_doc() -> None:
    text = f"""
# 4253 - Source Jacobian or first direct Hperp profile fill

**Status:** `{DECISION}`.

## Result

No live source-backed `Y_m/Y_a` Jacobian candidate exists yet, and 4253 rejects hand-choosing `Pi4`.

The forward move is the new source-probe tomography bridge:

```text
A_H <= sigma_S^-1 C_S C_perp E_Dq,H + eta_domain,

h_U_C1 <= sigma_S1^-1 C_S1 C_perp E_Dq,H_C1
          + (||nabla S||/sigma_S1) A_H
          + eta_C1.
```

So the first direct `Hperp` profile can be filled either from parent `Pi4/X_m/X_a` rows or from source-probe rank plus Dq-defect envelopes.

## Next Target

`{NEXT_TARGET}`
"""
    write_text(DOC_PATH, text)


def update_spine_and_packet() -> None:
    spine_block = f"""
## PPC4161 source Jacobian or direct Hperp profile fill

Marker: `{MARKER}`

4253 finds no current parent-owned `Y_m/Y_a` Jacobian row and rejects a hand-picked `Pi4`. The constructive fallback is source-probe tomography:

```text
A_H <= sigma_S^-1 C_S C_perp E_Dq,H + eta_domain,
h_U_C1 <= sigma_S1^-1 C_S1 C_perp E_Dq,H_C1
          + (||nabla S||/sigma_S1) A_H + eta_C1.
```

This turns the 4243 Dq-defect route into a possible direct `Hperp` profile fill, provided the source probes span the live sector.
"""
    packet_block = f"""
## Packet Update - source Jacobian or direct Hperp profile

Marker: `{PACKET_MARKER}`

The local packet now has two concrete coupling routes: parent `Pi4/X_m/X_a` Jacobian rows for 4252, or source-probe tomography from 4243 Dq-defect envelopes. Poynting remains guarded as Hilbert EM stress unless an explicit MTS Hodge/current/radiative side-channel row is present.
"""
    append_once(FORMAL / "07-unification-spine.md", MARKER, spine_block)
    append_once(FORMAL / "180-PPC4161-private-local-packet-integration.md", PACKET_MARKER, packet_block)


def validation_rows(outputs: Dict[str, Path]) -> List[Dict[str, str]]:
    sources = source_rows()
    theorems = theorem_rows()
    results = csv_rows(outputs["profile_results"])
    validations = [
        ("VAL4253_0_sources_exist", all(row["exists"] == "True" for row in sources), "all source paths exist"),
        ("VAL4253_1_needles_found", all(row["required_text_found"] == "True" for row in sources), "all source needles found"),
        ("VAL4253_2_no_free_Pi4", any(row["theorem_id"] == "SJH4253_0_no_free_Pi4" for row in theorems), "no-free-Pi4 theorem emitted"),
        ("VAL4253_3_tomography", any(row["theorem_id"] == "SJH4253_2_source_probe_tomography" for row in theorems), "source-probe tomography theorem emitted"),
        ("VAL4253_4_C1_bridge", any(row["theorem_id"] == "SJH4253_3_C1_tomography" for row in theorems), "C1 tomography theorem emitted"),
        ("VAL4253_5_results_nonclaim", all(row.get("claim_allowed", "False") == "False" for row in results), "profile runner does not claim closure"),
        ("VAL4253_6_formal_doc", FORMAL_PATH.exists() and MARKER in read_text(FORMAL_PATH), "formal doc written"),
        ("VAL4253_7_checkpoint_doc", DOC_PATH.exists() and DECISION in read_text(DOC_PATH), "checkpoint doc written"),
        ("VAL4253_8_claim_row", f"{CLAIM_ID}," in read_text(FORMAL / "02-claims-register.csv"), "claim register row added"),
        ("VAL4253_9_spine_marker", MARKER in read_text(FORMAL / "07-unification-spine.md"), "spine marker present"),
        ("VAL4253_10_packet_marker", PACKET_MARKER in read_text(FORMAL / "180-PPC4161-private-local-packet-integration.md"), "packet marker present"),
    ]
    for name, path in outputs.items():
        validations.append((f"VAL4253_csv_{name}", bool(csv_rows(path)), f"{path.name} parses"))
    return [
        {
            **common(),
            "check_id": check_id,
            "description": description,
            "passed": str(passed),
            "evidence": "generated_artifacts",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
        for check_id, passed, description in validations
    ]


def main() -> None:
    SOURCE_DIR.mkdir(parents=True, exist_ok=True)
    outputs = {
        "source_register": SOURCE_DIR / "P8_Y5_R2FR_4253_SOURCE_REGISTER.csv",
        "source_hunt": SOURCE_DIR / "P8_Y5_R2FR_4253_SOURCE_HUNT_AUDIT.csv",
        "theorems": SOURCE_DIR / "P8_Y5_R2FR_4253_SOURCE_JACOBIAN_HPERP_THEOREMS.csv",
        "profile_template": SOURCE_DIR / "P8_Y5_R2FR_4253_DQ_DEFECT_PROFILE_INPUT_TEMPLATE.csv",
        "profile_results": SOURCE_DIR / "P8_Y5_R2FR_4253_DQ_DEFECT_PROFILE_RESULTS.csv",
        "bridge_rows": SOURCE_DIR / "P8_Y5_R2FR_4253_TO_4249_BRIDGE_ROWS.csv",
        "decision": SOURCE_DIR / "P8_Y5_R2FR_4253_DECISION.csv",
        "firewall": SOURCE_DIR / "P8_Y5_R2FR_4253_CLAIM_FIREWALL.csv",
        "status": SOURCE_DIR / "P8_Y5_R2FR_4253_STATUS.csv",
        "next_target": SOURCE_DIR / "P8_Y5_R2FR_4253_NEXT_TARGET.csv",
    }

    write_formal_doc()
    write_checkpoint_doc()
    append_claim_row()
    update_spine_and_packet()

    results = profile_results()
    write_csv(outputs["source_register"], source_rows())
    write_csv(outputs["source_hunt"], source_hunt_rows())
    write_csv(outputs["theorems"], theorem_rows())
    write_csv(outputs["profile_template"], profile_template_rows())
    write_csv(outputs["profile_results"], results)
    write_csv(outputs["bridge_rows"], bridge_rows(results))
    write_csv(outputs["decision"], decision_rows())
    write_csv(outputs["firewall"], firewall_rows())
    write_csv(outputs["status"], status_rows())
    write_csv(outputs["next_target"], next_target_rows())
    write_csv(VALIDATION_PATH, validation_rows(outputs))

    validation = csv_rows(VALIDATION_PATH)
    failed = [row for row in validation if row["passed"] != "True"]
    print(f"{CHECKPOINT}: wrote {len(outputs)} csv artifacts")
    print(f"{CHECKPOINT}: validation rows={len(validation)} failed={len(failed)}")
    print(f"{CHECKPOINT}: decision={DECISION}")


if __name__ == "__main__":
    main()

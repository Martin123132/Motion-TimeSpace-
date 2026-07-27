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

CHECKPOINT = "4263"
CLAIM_ID = "L-104"
BRANCH = "MTS_R2FR_Y5_DQ_EM_CLOSED_COLLAR_ADOPTION_OR_RADIATIVE_BOUNDARY_ROW_4263"
DECISION = "DQ_EM_STANDARD_VISIBLE_BRANCH_ADOPTED_AS_CONDITIONAL_ZERO_FOR_CLOSED_COLLAR_OPEN_RADIATION_BOUND_ROW_RETAINED_NONCLAIM"
MARKER = "PPC4161_DQ_EM_CLOSED_COLLAR_ADOPTION_OR_RADIATIVE_BOUNDARY_ROW_4263"
PACKET_MARKER = "PPC4161_PACKET_DQ_EM_CLOSED_COLLAR_ADOPTION_OR_RADIATIVE_BOUNDARY_ROW_4263"
NEXT_TARGET = "4264-Y5-R2FR-Dq-theta-marker-or-source-readout-component-zero.md"

FORMAL_PATH = FORMAL / "279-PPC4161-Dq-EM-closed-collar-adoption-or-radiative-boundary-row.md"
DOC_PATH = POST / "4263-Y5-R2FR-Dq-EM-closed-collar-adoption-or-radiative-boundary-row.md"
VALIDATION_PATH = SOURCE_DIR / "P8_Y5_BRR545_4263_VALIDATION.csv"

LIVE_COMPONENT_CANDIDATE_PATH = SOURCE_DIR / "P8_Y5_R2FR_4254_DQ_COMPONENT_VALUES_CANDIDATE.csv"
LOCAL_COMPONENT_CANDIDATE_PATH = SOURCE_DIR / "P8_Y5_R2FR_4263_DQ_COMPONENT_VALUES_CANDIDATE.csv"

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
    "SRC4263_00_4175_poynting_owner": SourceSpec(
        "SRC4263_00_4175_poynting_owner",
        FORMAL / "191-PPC4161-Maxwell-Hodge-Poynting-stress-owner-theorem.md",
        "Radiative Boundary Guard",
        "Maxwell-Hodge owns Poynting as Hilbert flux and retains boundary guard.",
    ),
    "SRC4263_01_4207_owner_lock": SourceSpec(
        "SRC4263_01_4207_owner_lock",
        FORMAL / "223-PPC4161-EM-Poynting-Hodge-source-owner-lock.md",
        "Poynting vector is real physical flow",
        "Poynting once-only lock and retained Delta_rad_Poynting gate.",
    ),
    "SRC4263_02_4218_visible_em": SourceSpec(
        "SRC4263_02_4218_visible_em",
        FORMAL / "234-PPC4161-visible-EM-material-curl-zero-or-residual-bound.md",
        "live radiative Poynting flux is boundary-routed",
        "Visible EM residual zero theorem including radiative boundary clause.",
    ),
    "SRC4263_03_4259_component": SourceSpec(
        "SRC4263_03_4259_component",
        FORMAL / "275-PPC4161-EM-Hodge-component-zero-or-residual-vector.md",
        "radiative flux boundary-routed",
        "Dq_EM zero contract with radiative boundary clause.",
    ),
    "SRC4263_04_4262_formal": SourceSpec(
        "SRC4263_04_4262_formal",
        FORMAL / "278-PPC4161-visible-EM-readout-guard-or-charge-normalization-bound.md",
        "closed-collar radiative Poynting flux",
        "4262 leaves closed-collar and orientation as the final adoption gate.",
    ),
    "SRC4263_05_4262_reduction": SourceSpec(
        "SRC4263_05_4262_reduction",
        SOURCE_DIR / "P8_Y5_R2FR_4262_EM_COUPLING_RESIDUAL_REDUCTION.csv",
        "Delta_rad_Poynting",
        "Machine-readable 4262 residual map with open boundary rows.",
    ),
    "SRC4263_06_4262_candidate": SourceSpec(
        "SRC4263_06_4262_candidate",
        SOURCE_DIR / "P8_Y5_R2FR_4262_DQ_EM_STANDARD_BRANCH_CANDIDATE.csv",
        "NO_OVERWRITE",
        "4262 staged a Dq_EM zero candidate but did not adopt it.",
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
            "4263 adopts the 4262 Dq_EM standard-visible-branch candidate into the live component candidate only "
            "under a closed-collar/static boundary theorem: Poynting is already Maxwell-Hodge Hilbert flux, the "
            "orientation/outward-normal convention is fixed before variation, and the net radiative EM flux through "
            "the local collar is zero or routed as an explicit boundary term. The live 4254 Dq_EM epsilon and C1 "
            "epsilon are set to 0.0 as a private conditional branch input, while open radiation remains a retained "
            "finite bound row. No local-GR/PPN/R10 public pass is claimed."
        ),
        "current_evidence": (
            "4263 source register, closed-collar theorem, boundary/orientation rows, EM residual final branch map, "
            "Dq_EM adoption row, updated component candidate, decision and firewall."
        ),
        "status": "private_Dq_EM_conditional_zero_adopted_for_closed_collar_standard_visible_branch_nonclaim",
        "next_test": "Attack Dq_theta_marker or Dq_source_readout next, while 4254 remains blocked by other Dq component rows.",
        "key_risk": "Using a closed-collar EM zero outside static/quasi-static local tests or silently erasing radiative boundary flux.",
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


def closed_collar_theorem_rows() -> List[Dict[str, str]]:
    raw = [
        (
            "CCT4263_0_poynting_owner",
            "Poynting ownership",
            "For Maxwell-Hodge EM, S_i=-T_EM(n,e_i); EM flux is already in the Hilbert stress and c_Poynt_extra=0.",
            "DERIVED_IMPORTED_FROM_4175_4207",
            "forbids Poynting as a second hidden bulk source",
        ),
        (
            "CCT4263_1_closed_collar_flux",
            "closed-collar no-radiation clause",
            "On the static/quasi-static local collar used for Newton/PPN/R10/clock source tests, if Phi_EM_rad=int_boundary S dot n dA=0 over the test window, then Delta_rad_Poynting=0.",
            "CONDITIONAL_ZERO_FOR_CLOSED_COLLAR",
            "open radiative systems keep a finite boundary-flux row",
        ),
        (
            "CCT4263_2_orientation_owner",
            "orientation/outward-normal owner",
            "If the observed time orientation, volume orientation and outward boundary normal are fixed before variation, Delta_orientation_flux=0 by convention, not by fitting.",
            "CONDITIONAL_ZERO_FOR_FIXED_OBSERVED_ORIENTATION",
            "if the boundary projector/orientation varies, retain a boundary projector row",
        ),
        (
            "CCT4263_3_Dq_EM_adoption",
            "Dq_EM conditional branch zero",
            "4261 closes the action-domain/Hodge branch, 4262 closes readout/coupling leaks, and 4263 closes the closed-collar radiative/orientation guard; therefore Dq_EM=0 in this standard local branch.",
            "ADOPTED_AS_PRIVATE_COMPONENT_CANDIDATE",
            "conditional branch input only; not a public local-GR claim",
        ),
        (
            "CCT4263_4_open_boundary_bound",
            "open-boundary fallback",
            "If Phi_EM_rad != 0, use epsilon_rad_EM=|Phi_EM_rad|/(M_H c^2/Delta tau) plus any orientation/projector variation as a no-cancellation boundary bound.",
            "RETAINED_BOUND_FORK",
            "radiation is physical, not erased",
        ),
    ]
    return [
        {
            **common(),
            "theorem_id": theorem_id,
            "name": name,
            "statement": statement,
            "status": status,
            "effect": effect,
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
        for theorem_id, name, statement, status, effect in raw
    ]


def boundary_rows() -> List[Dict[str, str]]:
    raw = [
        (
            "BND4263_0_closed_static_collar",
            "Delta_rad_Poynting",
            "Phi_EM_rad=int_boundary S_Poynting dot n dA over the local test window",
            "0_if_static_or_quasistatic_closed_collar",
            "abs(Phi_EM_rad)/(M_H*c^2/Delta_tau)",
            "MISSING_OPEN_RADIATIVE_FLUX_INPUT_IF_NOT_CLOSED",
        ),
        (
            "BND4263_1_orientation_fixed",
            "Delta_orientation_flux",
            "observed time orientation, volume orientation and outward normal are fixed before variation",
            "0_if_orientation_and_normal_fixed_before_variation",
            "abs(Delta_orientation_flux)",
            "MISSING_ORIENTATION_PROJECTOR_BOUND_IF_NOT_FIXED",
        ),
        (
            "BND4263_2_boundary_projector",
            "Dq_boundary_projector",
            "boundary surface is a fixed collar/readout choice for EM radiation, not a varied hidden source projector",
            "not_closed_here_retained_for_Dq_boundary_projector_component",
            "epsilon_boundary_projector",
            "NEXT_COMPONENT_GATE",
        ),
    ]
    return [
        {
            **common(),
            "row_id": row_id,
            "coefficient": coefficient,
            "definition": definition,
            "closed_collar_status": closed_status,
            "open_collar_bound": open_bound,
            "if_not_closed": if_not_closed,
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
        for row_id, coefficient, definition, closed_status, open_bound, if_not_closed in raw
    ]


def final_residual_map_rows() -> List[Dict[str, str]]:
    raw = [
        ("delta_w_EM", "ZERO_IN_4210_STANDARD_BRANCH", "4261/4262 no visible deformation"),
        ("C_XF2", "ZERO_IN_4210_STANDARD_BRANCH", "4261 no hidden F2 operator"),
        ("C_JQ", "ZERO_IN_4210_STANDARD_BRANCH", "4262 same-action current and fixed charges"),
        ("b_alpha", "ZERO_IN_4210_STANDARD_BRANCH", "4262 fixed g_J/lambda_A before variation"),
        ("dlnlambda_derivative", "ZERO_IN_4210_STANDARD_BRANCH", "4262 lambda_A fixed before variation"),
        ("b_A/b_marker", "ZERO_IN_4210_STANDARD_BRANCH", "4262 theta_obs/material labels q-basic"),
        ("Delta_Hodge_EM", "ZERO_IN_4210_STANDARD_BRANCH_WITH_FIXED_ORIENTATION", "4261 action domain plus 4262 readout plus 4263 orientation"),
        ("Delta_rad_Poynting", "ZERO_FOR_CLOSED_COLLAR_ELSE_BOUND", "4263 closed-collar flux clause"),
        ("Delta_internal_exchange", "ZERO_IN_SINGLE_VISIBLE_ACTION_BRANCH", "4218/4262 Ward exchange ownership"),
        ("c_Poynt_extra", "ZERO_BY_POYNTING_ONCE_ONLY", "4175/4207/4259"),
    ]
    return [
        {
            **common(),
            "coefficient": coefficient,
            "standard_branch_status": status,
            "source_basis": source_basis,
            "open_branch_requirement": "retain_source_backed_bound_if_condition_fails",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
        for coefficient, status, source_basis in raw
    ]


def adoption_rows() -> List[Dict[str, str]]:
    return [
        {
            **common(),
            "adoption_id": "ADOPT4263_Dq_EM",
            "component": "Dq_EM",
            "old_epsilon": "MISSING_EPSILON_EM_VISIBLE_RESIDUAL_VECTOR",
            "new_epsilon": "0.0",
            "new_epsilon_C1": "0.0",
            "adoption_status": "ADOPTED_CONDITIONAL_ZERO_FOR_STANDARD_VISIBLE_CLOSED_COLLAR_BRANCH",
            "source_path": str(FORMAL_PATH),
            "conditions": (
                "standard visible import; no DeltaS_MTS_visible; Maxwell-Hodge on g_obs; q-basic calibrated constants; "
                "pure postprocessing readout; single visible Hilbert source; Poynting once-only; fixed orientation; "
                "closed/static collar or explicit radiative boundary route"
            ),
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
    ]


def component_candidate_rows() -> List[Dict[str, str]]:
    previous = csv_rows(LIVE_COMPONENT_CANDIDATE_PATH)
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
        if probe == "Dq_EM":
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
                    "epsilon": "0.0" if probe == "Dq_EM" else f"MISSING_ZERO_PROOF_OR_PROFILE_{probe}",
                    "epsilon_C1": "0.0" if probe == "Dq_EM" else f"MISSING_C1_ZERO_PROOF_OR_PROFILE_{probe}",
                    "source_path": str(FORMAL_PATH),
                    "valid_for_claim": "False",
                }
            )
    return output


def decision_rows() -> List[Dict[str, str]]:
    raw = [
        (
            "DEC4263_0_adopt_Dq_EM",
            "Adopt Dq_EM=0 as a live conditional component candidate for the standard visible closed-collar branch.",
            "The action-domain, readout/coupling, Poynting once-only, orientation and closed-radiation clauses are now explicitly sourced.",
            NEXT_TARGET,
        ),
        (
            "DEC4263_1_open_radiation_bound",
            "Open radiative EM systems are not closed by this theorem.",
            "Radiation crossing the collar is a boundary/Hamiltonian flux, not a hidden bulk force and not silently zero.",
            "Fill Phi_EM_rad/M_H window bound if using an open/radiative branch.",
        ),
        (
            "DEC4263_2_4254_still_blocked",
            "4254 remains blocked because other Dq components and tomography constants are still missing.",
            "This is progress: one component row is no longer the EM mystery row.",
            "Attack Dq_theta_marker, Dq_source_readout or Dq_boundary_projector next.",
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
        ("FW4263_0_radiation_erasure", "using the closed-collar zero for open radiative EM systems", "PHI_EM_RAD_BOUND_REQUIRED"),
        ("FW4263_1_poynting_double_count", "adding Poynting as a second bulk source after T_EM is included", "POYNTING_ONCE_ONLY_REQUIRED"),
        ("FW4263_2_orientation_smuggle", "changing boundary orientation or outward normal after variation", "FIXED_ORIENTATION_BEFORE_VARIATION_REQUIRED"),
        ("FW4263_3_live_claim", "treating the Dq_EM conditional row as full local-GR/PPN/R10 success", "OTHER_DQ_COMPONENTS_AND_TOMOGRAPHY_REQUIRED"),
        ("FW4263_4_old_branch_overwrite", "using a closed static collar theorem for cosmological/radiative EM backgrounds", "BRANCH_SCOPE_REQUIRED"),
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
            "status_id": "STATUS4263_0",
            "summary": (
                "4263 moves Dq_EM from a vague visible-EM residual blocker to a conditional zero in the standard "
                "visible closed-collar branch, while retaining open radiative flux as a boundary bound row."
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
            "objective": (
                "Attack one of the remaining live Dq components now that Dq_EM is conditionally adopted: "
                "Dq_theta_marker, Dq_source_readout, or Dq_boundary_projector."
            ),
            "avoid": "Do not claim 4254 has a full Hperp bound until the remaining component rows and tomography constants are numeric/source-backed.",
            "valid_for_claim": "False",
        }
    ]


def formal_doc() -> str:
    return f"""
# 279 - PPC4161 Dq-EM closed-collar adoption or radiative boundary row

Marker: `{MARKER}`

Branch: `{BRANCH}`

Decision: `{DECISION}`

## Private nonclaim

4263 does not prove public local GR, PPN, R10, clock safety, Maxwell/QED, or `alpha_EM`.

It adopts one live component row:

```text
Dq_EM = 0
```

only inside the standard visible, static/quasi-static, closed-collar local branch.

## Closed-collar theorem

From Maxwell-Hodge:

```text
S_i = -T_EM(n,e_i).
```

So Poynting is already the Hilbert flux of the EM stress, not a second source.

For the local collar:

```text
Phi_EM_rad = int_boundary S_Poynting dot n dA.
```

If:

```text
Phi_EM_rad = 0
```

over the test window, and the observed time orientation, volume orientation and outward normal are fixed before variation, then:

```text
Delta_rad_Poynting = 0,
Delta_orientation_flux = 0.
```

Combined with 4261 and 4262:

```text
action-domain/Hodge branch zero,
readout/coupling branch zero,
Poynting once-only,
closed-collar flux zero,
fixed orientation,
```

we can adopt:

```text
Dq_EM = 0,
Dq_EM_C1 = 0
```

as a private standard-branch component candidate.

## Open/radiative branch

If radiation crosses the collar:

```text
Phi_EM_rad != 0,
```

do not zero it. Use:

```text
epsilon_rad_EM = |Phi_EM_rad| / (M_H c^2 / Delta tau)
```

plus any orientation/projector variation as an explicit boundary bound.

## 4254 feed

The live component candidate is updated from:

```text
Dq_EM = MISSING_EPSILON_EM_VISIBLE_RESIDUAL_VECTOR
```

to:

```text
Dq_EM = 0.0,
Dq_EM_C1 = 0.0.
```

The row remains `valid_for_claim=false` because the full source-probe/tomography gate still needs the other Dq components and constants.

## Next target

`{NEXT_TARGET}` should attack `Dq_theta_marker`, `Dq_source_readout`, or `Dq_boundary_projector`.
"""


def checkpoint_doc() -> str:
    return f"""
# 4263 - Y5 R2FR Dq-EM closed-collar adoption or radiative boundary row

Packet marker: `{PACKET_MARKER}`

## Result

4263 adopts the standard-branch `Dq_EM=0` candidate into the live 4254 component candidate file, but only under closed-collar conditions.

Open radiative EM remains a boundary-flux bound row:

```text
epsilon_rad_EM = |Phi_EM_rad|/(M_H c^2/Delta tau).
```

## Claim status

Private nonclaim. One component is improved; the full local-GR route still needs the remaining Dq components and tomography constants.
"""


def validation_rows(paths: Dict[str, Path]) -> List[Dict[str, str]]:
    sources = csv_rows(paths["sources"])
    theorems = csv_rows(paths["theorems"])
    boundary = csv_rows(paths["boundary"])
    adoption = csv_rows(paths["adoption"])
    local_candidate = csv_rows(paths["local_candidate"])
    live_candidate = csv_rows(LIVE_COMPONENT_CANDIDATE_PATH)
    live_dq_em = [row for row in live_candidate if row.get("probe_id") == "Dq_EM"]
    rows = [
        ("VAL4263_0_sources_exist", all(row["exists"] == "True" for row in sources), "all source paths exist"),
        ("VAL4263_1_needles_found", all(row["required_text_found"] == "True" for row in sources), "all source needles found"),
        (
            "VAL4263_2_closed_collar_theorem",
            any(row["status"] == "CONDITIONAL_ZERO_FOR_CLOSED_COLLAR" for row in theorems),
            "closed-collar flux theorem emitted",
        ),
        (
            "VAL4263_3_orientation_gate",
            any(row["coefficient"] == "Delta_orientation_flux" and "0_if_orientation" in row["closed_collar_status"] for row in boundary),
            "orientation boundary gate emitted",
        ),
        (
            "VAL4263_4_adoption_row",
            bool(adoption)
            and adoption[0]["new_epsilon"] == "0.0"
            and adoption[0]["adoption_status"] == "ADOPTED_CONDITIONAL_ZERO_FOR_STANDARD_VISIBLE_CLOSED_COLLAR_BRANCH",
            "Dq_EM adoption row emitted",
        ),
        (
            "VAL4263_5_local_candidate_numeric",
            any(row.get("probe_id") == "Dq_EM" and row.get("epsilon") == "0.0" and row.get("epsilon_C1") == "0.0" for row in local_candidate),
            "local 4263 candidate has numeric Dq_EM zero",
        ),
        (
            "VAL4263_6_live_4254_updated",
            bool(live_dq_em)
            and live_dq_em[0].get("epsilon") == "0.0"
            and live_dq_em[0].get("epsilon_C1") == "0.0"
            and live_dq_em[0].get("source_path") == str(FORMAL_PATH),
            "live 4254 candidate Dq_EM updated",
        ),
        (
            "VAL4263_7_open_radiation_retained",
            any(row["coefficient"] == "Delta_rad_Poynting" and "Phi_EM_rad" in row["definition"] for row in boundary),
            "open radiative flux bound retained",
        ),
        ("VAL4263_8_claim_row", CLAIM_ID in read_text(FORMAL / "02-claims-register.csv"), "claim register row added"),
        ("VAL4263_9_formal_doc", MARKER in read_text(FORMAL_PATH), "formal marker present"),
        ("VAL4263_10_checkpoint_doc", PACKET_MARKER in read_text(DOC_PATH), "checkpoint marker present"),
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
    source_path = SOURCE_DIR / "P8_Y5_R2FR_4263_SOURCE_REGISTER.csv"
    theorem_path = SOURCE_DIR / "P8_Y5_R2FR_4263_CLOSED_COLLAR_THEOREM.csv"
    boundary_path = SOURCE_DIR / "P8_Y5_R2FR_4263_BOUNDARY_FLUX_ORIENTATION_ROWS.csv"
    residual_map_path = SOURCE_DIR / "P8_Y5_R2FR_4263_EM_RESIDUAL_FINAL_BRANCH_MAP.csv"
    adoption_path = SOURCE_DIR / "P8_Y5_R2FR_4263_DQ_EM_ADOPTION.csv"
    decision_path = SOURCE_DIR / "P8_Y5_R2FR_4263_DECISION.csv"
    firewall_path = SOURCE_DIR / "P8_Y5_R2FR_4263_CLAIM_FIREWALL.csv"
    status_path = SOURCE_DIR / "P8_Y5_R2FR_4263_STATUS.csv"
    next_path = SOURCE_DIR / "P8_Y5_R2FR_4263_NEXT_TARGET.csv"

    component_candidate = component_candidate_rows()
    write_csv(source_path, source_rows())
    write_csv(theorem_path, closed_collar_theorem_rows())
    write_csv(boundary_path, boundary_rows())
    write_csv(residual_map_path, final_residual_map_rows())
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
        "boundary": boundary_path,
        "adoption": adoption_path,
        "local_candidate": LOCAL_COMPONENT_CANDIDATE_PATH,
    }
    validation = validation_rows(paths)
    write_csv(VALIDATION_PATH, validation)
    failed = [row for row in validation if row["passed"] != "True"]
    print(f"{CHECKPOINT}: wrote 10 csv artifacts plus validation")
    print(f"{CHECKPOINT}: validation rows={len(validation)} failed={len(failed)}")
    print(f"{CHECKPOINT}: decision={DECISION}")


if __name__ == "__main__":
    main()

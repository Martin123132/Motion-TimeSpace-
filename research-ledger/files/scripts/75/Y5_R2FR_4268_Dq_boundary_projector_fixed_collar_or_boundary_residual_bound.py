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

CHECKPOINT = "4268"
CLAIM_ID = "L-109"
BRANCH = "MTS_R2FR_Y5_DQ_BOUNDARY_PROJECTOR_FIXED_COLLAR_OR_BOUNDARY_RESIDUAL_4268"
DECISION = "DQ_BOUNDARY_PROJECTOR_ADOPTED_FOR_FIXED_NOFLUX_COLLAR_BRANCH_OPEN_BOUNDARY_RETAINED_NONCLAIM"
MARKER = "PPC4161_DQ_BOUNDARY_PROJECTOR_FIXED_COLLAR_OR_BOUNDARY_RESIDUAL_4268"
PACKET_MARKER = "PPC4161_PACKET_DQ_BOUNDARY_PROJECTOR_FIXED_COLLAR_OR_BOUNDARY_RESIDUAL_4268"
NEXT_TARGET = "4269-Y5-R2FR-Dq-tau-reference-time-lock-or-tau-residual-bound.md"

FORMAL_PATH = FORMAL / "284-PPC4161-Dq-boundary-projector-fixed-collar-or-boundary-residual-bound.md"
DOC_PATH = POST / "4268-Y5-R2FR-Dq-boundary-projector-fixed-collar-or-boundary-residual-bound.md"
VALIDATION_PATH = SOURCE_DIR / "P8_Y5_BRR545_4268_VALIDATION.csv"
ADOPTION_4269_PATH = SOURCE_DIR / "P8_Y5_R2FR_4269_DQ_TAU_ADOPTION.csv"
FORMAL_4269_PATH = FORMAL / "285-PPC4161-Dq-tau-reference-time-lock-or-tau-residual-bound.md"
REDUCED_GEOM_4270_PATH = SOURCE_DIR / "P8_Y5_R2FR_4270_DQ_GEOM_REDUCED_CANDIDATE.csv"
FORMAL_4270_PATH = FORMAL / "286-PPC4161-Dq-geom-core-coframe-shadow-or-reduced-epsilon-bound.md"
CORE_GEOM_4271_PATH = SOURCE_DIR / "P8_Y5_R2FR_4271_DQ_GEOM_CORE_FRAME_CANDIDATE.csv"
FORMAL_4271_PATH = FORMAL / "287-PPC4161-core-coframe-shadow-zero-or-first-source-backed-epsilon-row.md"
BOUND_GEOM_4272_PATH = SOURCE_DIR / "P8_Y5_R2FR_4272_DQ_GEOM_BOUND_RUNNER_CANDIDATE.csv"
FORMAL_4272_PATH = FORMAL / "288-PPC4161-parent-no-extra-frame-signature-or-cg-bdis-first-bound-runner.md"

LIVE_COMPONENT_CANDIDATE_PATH = SOURCE_DIR / "P8_Y5_R2FR_4254_DQ_COMPONENT_VALUES_CANDIDATE.csv"
LOCAL_COMPONENT_CANDIDATE_PATH = SOURCE_DIR / "P8_Y5_R2FR_4268_DQ_COMPONENT_VALUES_CANDIDATE.csv"

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
    "SRC4268_00_4176_boundary": SourceSpec(
        "SRC4268_00_4176_boundary",
        FORMAL / "192-PPC4161-local-boundary-no-flux-sector-interface-theorem.md",
        "supp(T_local) subset int(W_loc)",
        "Compact local collar/worldtube no-flux theorem.",
    ),
    "SRC4268_01_4217_boundary_corner": SourceSpec(
        "SRC4268_01_4217_boundary_corner",
        FORMAL / "233-PPC4161-boundary-corner-curl-zero-or-flux-bound.md",
        "I_boundary + I_corner = 0.",
        "Boundary/corner curl zero theorem and open-flux fallback.",
    ),
    "SRC4268_02_4266_projector_tax": SourceSpec(
        "SRC4268_02_4266_projector_tax",
        FORMAL / "282-PPC4161-Dq-source-readout-Hilbert-charge-zero-or-coefficient-remainder.md",
        "changing source collar/worldtube/projector",
        "4266 explicitly assigned changing collars/projectors to this component.",
    ),
    "SRC4268_03_4267_next": SourceSpec(
        "SRC4268_03_4267_next",
        FORMAL / "283-PPC4161-Dq-coeff-fixed-parent-constant-or-Newton-calibration-bound.md",
        "Dq_boundary_projector",
        "4267 selected boundary/projector as the next live Dq component.",
    ),
    "SRC4268_04_4217_csv": SourceSpec(
        "SRC4268_04_4217_csv",
        SOURCE_DIR / "P8_Y5_R2FR_4217_BOUNDARY_CORNER_THEOREM.csv",
        "BCC4217_3_no_flux_collar",
        "Machine-readable no-flux collar theorem row.",
    ),
    "SRC4268_05_4176_decomposition": SourceSpec(
        "SRC4268_05_4176_decomposition",
        SOURCE_DIR / "P8_Y5_R2FR_4176_BOUNDARY_DOMAIN_DECOMPOSITION.csv",
        "BD4176_5_projection",
        "Boundary/domain decomposition includes the local projection/readout slot.",
    ),
    "SRC4268_06_4263_closed_collar": SourceSpec(
        "SRC4268_06_4263_closed_collar",
        SOURCE_DIR / "P8_Y5_R2FR_4263_CLOSED_COLLAR_THEOREM.csv",
        "CONDITIONAL_ZERO_FOR_CLOSED_COLLAR",
        "EM closed-collar theorem already used the same static/quasi-static collar logic.",
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


def dq_tau_4269_adoption_row() -> Dict[str, str]:
    for row in csv_rows(ADOPTION_4269_PATH):
        if (
            row.get("component") == "Dq_tau"
            and row.get("new_epsilon") == "0.0"
            and row.get("adoption_status") == "ADOPTED_CONDITIONAL_ZERO_FOR_QBASIC_OBSERVED_TAU_BRANCH_ONLY"
        ):
            return row
    return {}


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
            "4268 adopts Dq_boundary_projector=0 and its C1 row only for the fixed compact no-flux collar/worldtube branch: "
            "the local boundary, normals, orientations, caps, projector and sector interfaces are selected before variation, "
            "ordinary source support stays inside the collar, and radiative/open sector flux is absent or explicitly routed as a boundary residual. "
            "Moving boundaries, source crossing, open radiation, memory pullback or domain-selector reentry reopen finite boundary rows."
        ),
        "current_evidence": (
            "4268 source register, fixed-collar boundary projector theorem rows, open-boundary residual split rows, "
            "Dq_boundary_projector adoption row, updated component candidate, decision and firewall."
        ),
        "status": "private_Dq_boundary_projector_conditional_zero_adopted_for_fixed_noflux_collar_branch_nonclaim",
        "next_test": "Attack Dq_tau next; 4254 remains blocked by tau, geometry and tomography constants.",
        "key_risk": "Using fixed-collar silence to erase real radiative flux, moving source boundaries, domain selectors or memory-sector pullback.",
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


def boundary_projector_theorem_rows() -> List[Dict[str, str]]:
    raw = [
        (
            "BPROJ4268_0_definition_split",
            "boundary/projector component",
            "Dq_boundary_projector measures hidden vertical drift of the local collar, normals, caps, orientations, worldtube and boundary projectors, not physical radiation itself.",
            "DEFINITION_SPLIT",
            "open/radiative flux is a residual, not part of the adopted zero",
        ),
        (
            "BPROJ4268_1_fixed_collar_qbasic",
            "fixed compact collar q-basicity",
            "If W_loc, Sigma_in/out, C_side, C_rad, normals, orientations and Pi_loc are selected before variation as q-basic readout data, then delta_v boundary_projector=0.",
            "CONDITIONAL_ZERO_FOR_FIXED_COLLAR_PROJECTOR",
            "fails if the source worldtube/projector is varied by hidden fields",
        ),
        (
            "BPROJ4268_2_no_flux_support",
            "no-flux support separation",
            "If supp(T_local) is inside W_loc and n_mu T_cross^{mu nu} tau_nu vanishes on C_side and sector interfaces, the local projector has no hidden source-crossing term.",
            "CONDITIONAL_NOFLUX_ZERO",
            "fails for source crossing, open-memory/cosmology pullback or moving apparatus boundaries",
        ),
        (
            "BPROJ4268_3_C1_zero",
            "fixed collar C1 silence",
            "A fixed collar/projector with fixed normals and orientations has zero local derivative on the compact test window, so the C1 row vanishes in the standard branch.",
            "CONDITIONAL_C1_ZERO_FOR_FIXED_COLLAR_PROJECTOR",
            "fails for boundary-layer motion or time-dependent readout projectors",
        ),
        (
            "BPROJ4268_4_open_boundary_bound",
            "open boundary fallback",
            "If F_rad, R_source_crossing, R_corner_edge, R_memory_pullback or Delta_projector is nonzero, retain epsilon_boundary_projector <= |R_boundary_projector|/M_H_ref with no cancellation against other Dq rows.",
            "RETAINED_BOUND_FORK",
            "radiation and moving boundaries remain physical scored residuals",
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
        ("BRES4268_0_fixed_worldtube", "delta_v W_loc", "local source worldtube/collar selected before variation", "Dq_boundary_projector", "ZERO_IN_FIXED_COLLAR_BRANCH"),
        ("BRES4268_1_fixed_normals", "delta_v n_mu_or_orientation", "outward normal, time orientation and volume orientation fixed before variation", "Dq_boundary_projector", "ZERO_IN_FIXED_COLLAR_BRANCH"),
        ("BRES4268_2_source_crossing", "R_source_crossing", "matter/apparatus/source current crosses collar", "boundary_residual_bound", "RETAINED_IF_NONZERO"),
        ("BRES4268_3_open_radiation", "R_rad_flux", "EM/gravitational/Poynting radiation through boundary", "boundary_residual_bound", "RETAINED_IF_NONZERO"),
        ("BRES4268_4_memory_pullback", "R_memory_pullback", "open-memory/cosmology/galaxy sector pullback into local collar", "boundary_residual_bound", "RETAINED_IF_NONZERO"),
        ("BRES4268_5_domain_selector", "Delta_domain_selector_projector", "domain selector or branch-classifier moves the projector", "boundary_or_domain_residual_bound", "RETAINED_IF_NONZERO"),
        ("BRES4268_6_corner_edge", "R_corner_edge", "corner boosts, edge modes, improvements or exact terms not fixed/routed", "boundary_residual_bound", "RETAINED_IF_NONZERO"),
    ]
    return [
        {
            **common(),
            "split_id": split_id,
            "coefficient_or_tail": coefficient,
            "meaning": meaning,
            "assigned_gate": gate,
            "4268_status": status,
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
            "adoption_id": "ADOPT4268_Dq_boundary_projector",
            "component": "Dq_boundary_projector",
            "old_epsilon": "MISSING_ZERO_PROOF_OR_PROFILE_Dq_boundary_projector",
            "new_epsilon": "0.0",
            "new_epsilon_C1": "0.0",
            "adoption_status": "ADOPTED_CONDITIONAL_ZERO_FOR_FIXED_NOFLUX_COLLAR_BRANCH_ONLY",
            "source_path": str(FORMAL_PATH),
            "conditions": (
                "W_loc, source worldtube, caps, normals, orientations, Pi_loc and sector interfaces are fixed/q-basic before variation; "
                "no source crossing or open radiative/memory/cosmology pullback enters the compact local test collar; open flux is routed as a boundary residual"
            ),
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
    ]


def component_candidate_rows() -> List[Dict[str, str]]:
    previous = csv_rows(LIVE_COMPONENT_CANDIDATE_PATH)
    adoption_4269 = dq_tau_4269_adoption_row()
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
        if probe == "Dq_boundary_projector":
            updated["epsilon"] = "0.0"
            updated["epsilon_C1"] = "0.0"
            updated["source_path"] = str(FORMAL_PATH)
            updated["valid_for_claim"] = "False"
        elif probe == "Dq_tau" and adoption_4269:
            updated["epsilon"] = adoption_4269.get("new_epsilon", "0.0")
            updated["epsilon_C1"] = adoption_4269.get("new_epsilon_C1", "0.0")
            updated["source_path"] = str(FORMAL_4269_PATH)
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
                    "epsilon": "0.0" if probe == "Dq_boundary_projector" else (adoption_4269.get("new_epsilon", "0.0") if probe == "Dq_tau" and adoption_4269 else f"MISSING_ZERO_PROOF_OR_PROFILE_{probe}"),
                    "epsilon_C1": "0.0" if probe == "Dq_boundary_projector" else (adoption_4269.get("new_epsilon_C1", "0.0") if probe == "Dq_tau" and adoption_4269 else f"MISSING_C1_ZERO_PROOF_OR_PROFILE_{probe}"),
                    "source_path": str(FORMAL_PATH) if probe != "Dq_tau" or not adoption_4269 else str(FORMAL_4269_PATH),
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
            "DEC4268_0_adopt_boundary_projector",
            "Adopt Dq_boundary_projector=0 for the fixed compact no-flux collar branch.",
            "The boundary/projector is selected before variation and no hidden source-crossing flux enters the local collar.",
            NEXT_TARGET,
        ),
        (
            "DEC4268_1_retain_open_flux",
            "Do not erase radiation, source crossing, memory pullback or moving projector terms.",
            "Those are physical boundary residuals and must be scored if present.",
            "Keep open-boundary residual rows nonclaim unless source-backed.",
        ),
        (
            "DEC4268_2_4254_progress",
            "4254 should now lose Dq_boundary_projector from the missing list while staying blocked by geometry, tau and constants.",
            "This moves the local-GR ladder to the last two Dq components plus tomography constants.",
            "Rerun 4254 after 4268.",
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
        ("FW4268_0_radiation_eraser", "using fixed-collar silence to set real EM/gravity radiation flux to zero", "BOUNDARY_FLUX_BOUND_REQUIRED"),
        ("FW4268_1_moving_worldtube", "calling a hidden-field-dependent source worldtube fixed", "MOVING_PROJECTOR_BOUND_REQUIRED"),
        ("FW4268_2_domain_selector", "hiding domain selector or branch classifier motion inside a fixed boundary", "DOMAIN_PROJECTOR_GATE_REQUIRED"),
        ("FW4268_3_source_crossing", "ignoring matter/apparatus crossing the local collar", "SOURCE_CROSSING_BOUND_REQUIRED"),
        ("FW4268_4_local_GR_jump", "treating boundary/projector silence as public local-GR/PPN/R10 pass", "REMAINING_COMPONENTS_AND_TOMOGRAPHY_REQUIRED"),
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
            "status_id": "STATUS4268_0",
            "summary": (
                "4268 moves Dq_boundary_projector from missing to a conditional zero for fixed compact no-flux local collars, "
                "while retaining open radiation, source crossing, moving worldtubes and domain-selector pullbacks as explicit boundary residuals."
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
            "objective": "Attack Dq_tau: fixed local time/coframe/reference lock versus tau/readout residual bound.",
            "avoid": "Do not use fixed boundary data to hide tau/frame/readout drift or geometry transfer defects.",
            "valid_for_claim": "False",
        }
    ]


def formal_doc() -> str:
    return f"""
# 284 - PPC4161 Dq-boundary-projector fixed collar or boundary residual bound

Marker: `{MARKER}`

Branch: `{BRANCH}`

Decision: `{DECISION}`

## Private nonclaim

4268 does not prove public local GR, PPN, R10, WEP, orbital safety, or absence of physical radiation.

It adopts:

```text
Dq_boundary_projector = 0
```

only for the fixed compact no-flux local collar/worldtube branch.

## What is actually proved

The boundary/projector row is not a claim that nothing ever crosses any boundary. It is the narrow statement that the local test collar is selected before variation:

```text
W_loc, Sigma_in, Sigma_out, C_side, C_rad,
normals, orientations, caps, Pi_loc
```

are q-basic readout/domain data in the compact branch.

Then, for `v in ker(Dq)`:

```text
delta_v W_loc = 0,
delta_v Pi_loc = 0,
delta_v n_mu = 0,
delta_v orientation = 0.
```

With compact source support and no sector pullback:

```text
supp(T_local) subset int(W_loc),
n_mu T_cross^{{mu nu}} tau_nu | C_side = 0,
pullback(open sector flux) = 0,
```

the boundary/projector component has no hidden vertical variation:

```text
Dq_boundary_projector = 0,
Dq_boundary_projector_C1 = 0.
```

## Open-boundary tax

If any of these exist:

```text
F_rad[tau],
R_source_crossing,
R_memory_pullback,
R_corner_edge,
Delta_domain_selector_projector,
moving source worldtube,
```

they are not killed by 4268. They must be routed as:

```text
epsilon_boundary_projector
<= |R_boundary_projector| / M_H_ref
```

with no cancellation against geometry, tau, EM, matter, source-readout, or coefficient rows.

## 4254 feed

The live component candidate is updated:

```text
Dq_boundary_projector = 0.0,
Dq_boundary_projector_C1 = 0.0.
```

The row remains `valid_for_claim=false` because the complete 4254 source-probe/tomography gate still needs geometry, tau and constants.

## Next target

`{NEXT_TARGET}` should attack `Dq_tau`.
"""


def checkpoint_doc() -> str:
    return f"""
# 4268 - Y5 R2FR Dq-boundary-projector fixed collar or boundary residual bound

Packet marker: `{PACKET_MARKER}`

## Result

4268 adopts:

```text
Dq_boundary_projector = 0.0,
Dq_boundary_projector_C1 = 0.0
```

for fixed compact no-flux local collars/worldtubes only.

## Human translation

The local test boundary is treated like fixed apparatus/coordinate scaffolding chosen before variation. If the boundary moves, if radiation crosses, if source matter crosses, or if a domain selector changes the collar, that is not zero; it becomes an explicit residual.

## Claim status

Private nonclaim. This narrows the Dq ladder without erasing real boundary physics.
"""


def validation_rows(paths: Dict[str, Path]) -> List[Dict[str, str]]:
    sources = csv_rows(paths["sources"])
    theorems = csv_rows(paths["theorems"])
    split = csv_rows(paths["split"])
    adoption = csv_rows(paths["adoption"])
    local_candidate = csv_rows(paths["local_candidate"])
    live_candidate = csv_rows(LIVE_COMPONENT_CANDIDATE_PATH)
    live_boundary = [row for row in live_candidate if row.get("probe_id") == "Dq_boundary_projector"]
    live_coeff = [row for row in live_candidate if row.get("probe_id") == "Dq_coeff"]
    live_source = [row for row in live_candidate if row.get("probe_id") == "Dq_source_readout"]
    live_matter = [row for row in live_candidate if row.get("probe_id") == "Dq_matter"]
    live_theta = [row for row in live_candidate if row.get("probe_id") == "Dq_theta_marker"]
    live_em = [row for row in live_candidate if row.get("probe_id") == "Dq_EM"]
    live_geom = [row for row in live_candidate if row.get("probe_id") == "Dq_geom"]
    live_tau = [row for row in live_candidate if row.get("probe_id") == "Dq_tau"]
    tau_adoption = dq_tau_4269_adoption_row()
    rows = [
        ("VAL4268_0_sources_exist", all(row["exists"] == "True" for row in sources), "all source paths exist"),
        ("VAL4268_1_needles_found", all(row["required_text_found"] == "True" for row in sources), "all source needles found"),
        (
            "VAL4268_2_fixed_collar_theorem",
            any(row["status"] == "CONDITIONAL_ZERO_FOR_FIXED_COLLAR_PROJECTOR" for row in theorems),
            "fixed-collar boundary projector theorem emitted",
        ),
        (
            "VAL4268_3_open_boundary_retained",
            any(row["4268_status"] == "RETAINED_IF_NONZERO" and row["coefficient_or_tail"] == "R_rad_flux" for row in split)
            and any(row["coefficient_or_tail"] == "Delta_domain_selector_projector" for row in split),
            "open radiation and moving/domain projector residuals retained",
        ),
        (
            "VAL4268_4_adoption_row",
            bool(adoption)
            and adoption[0]["new_epsilon"] == "0.0"
            and adoption[0]["adoption_status"] == "ADOPTED_CONDITIONAL_ZERO_FOR_FIXED_NOFLUX_COLLAR_BRANCH_ONLY",
            "Dq_boundary_projector adoption row emitted",
        ),
        (
            "VAL4268_5_local_candidate_numeric",
            any(row.get("probe_id") == "Dq_boundary_projector" and row.get("epsilon") == "0.0" and row.get("epsilon_C1") == "0.0" for row in local_candidate),
            "local 4268 candidate has numeric boundary projector zero",
        ),
        (
            "VAL4268_6_live_4254_updated",
            bool(live_boundary)
            and live_boundary[0].get("epsilon") == "0.0"
            and live_boundary[0].get("epsilon_C1") == "0.0"
            and live_boundary[0].get("source_path") == str(FORMAL_PATH),
            "live 4254 candidate Dq_boundary_projector updated",
        ),
        (
            "VAL4268_7_preserve_prior_adoptions",
            bool(live_em)
            and live_em[0].get("epsilon") == "0.0"
            and bool(live_theta)
            and live_theta[0].get("epsilon") == "0.0"
            and bool(live_matter)
            and live_matter[0].get("epsilon") == "0.0"
            and bool(live_source)
            and live_source[0].get("epsilon") == "0.0"
            and bool(live_coeff)
            and live_coeff[0].get("epsilon") == "0.0",
            "prior Dq_EM, Dq_theta_marker, Dq_matter, Dq_source_readout and Dq_coeff adoptions preserved",
        ),
        (
            "VAL4268_8_geom_tau_not_smuggled_or_later_sourced",
            bool(live_geom)
            and live_geom[0].get("epsilon") != "0.0"
            and bool(live_tau)
            and (
                live_tau[0].get("epsilon") != "0.0"
                or (
                    bool(tau_adoption)
                    and live_tau[0].get("epsilon") == "0.0"
                    and live_tau[0].get("source_path") == str(FORMAL_4269_PATH)
                )
            ),
            "Dq_geom remains live; Dq_tau is either live or zero only from the later 4269 sourced tau theorem",
        ),
        ("VAL4268_9_claim_row", CLAIM_ID in read_text(FORMAL / "02-claims-register.csv"), "claim register row added"),
        ("VAL4268_10_formal_doc", MARKER in read_text(FORMAL_PATH), "formal marker present"),
        ("VAL4268_11_checkpoint_doc", PACKET_MARKER in read_text(DOC_PATH), "checkpoint marker present"),
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
    source_path = SOURCE_DIR / "P8_Y5_R2FR_4268_SOURCE_REGISTER.csv"
    theorem_path = SOURCE_DIR / "P8_Y5_R2FR_4268_BOUNDARY_PROJECTOR_THEOREM.csv"
    split_path = SOURCE_DIR / "P8_Y5_R2FR_4268_OPEN_BOUNDARY_RESIDUAL_SPLIT_ROWS.csv"
    adoption_path = SOURCE_DIR / "P8_Y5_R2FR_4268_DQ_BOUNDARY_PROJECTOR_ADOPTION.csv"
    decision_path = SOURCE_DIR / "P8_Y5_R2FR_4268_DECISION.csv"
    firewall_path = SOURCE_DIR / "P8_Y5_R2FR_4268_CLAIM_FIREWALL.csv"
    status_path = SOURCE_DIR / "P8_Y5_R2FR_4268_STATUS.csv"
    next_path = SOURCE_DIR / "P8_Y5_R2FR_4268_NEXT_TARGET.csv"

    component_candidate = component_candidate_rows()
    write_csv(source_path, source_rows())
    write_csv(theorem_path, boundary_projector_theorem_rows())
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

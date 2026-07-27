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

CHECKPOINT = "4270"
CLAIM_ID = "L-111"
BRANCH = "MTS_R2FR_Y5_DQ_GEOM_CORE_COFRAME_SHADOW_OR_REDUCED_EPSILON_BOUND_4270"
DECISION = "DQ_GEOM_FULL_ZERO_REJECTED_CORE_COFRAME_SHADOW_RESIDUAL_COMPRESSED_NONCLAIM"
MARKER = "PPC4161_DQ_GEOM_CORE_COFRAME_SHADOW_OR_REDUCED_EPSILON_BOUND_4270"
PACKET_MARKER = "PPC4161_PACKET_DQ_GEOM_CORE_COFRAME_SHADOW_OR_REDUCED_EPSILON_BOUND_4270"
NEXT_TARGET = "4271-Y5-R2FR-core-coframe-shadow-zero-or-first-source-backed-epsilon-row.md"

FORMAL_PATH = FORMAL / "286-PPC4161-Dq-geom-core-coframe-shadow-or-reduced-epsilon-bound.md"
DOC_PATH = POST / "4270-Y5-R2FR-Dq-geom-core-coframe-shadow-or-reduced-epsilon-bound.md"
VALIDATION_PATH = SOURCE_DIR / "P8_Y5_BRR545_4270_VALIDATION.csv"

LIVE_COMPONENT_CANDIDATE_PATH = SOURCE_DIR / "P8_Y5_R2FR_4254_DQ_COMPONENT_VALUES_CANDIDATE.csv"
LOCAL_COMPONENT_CANDIDATE_PATH = SOURCE_DIR / "P8_Y5_R2FR_4270_DQ_COMPONENT_VALUES_CANDIDATE.csv"
REDUCED_CANDIDATE_PATH = SOURCE_DIR / "P8_Y5_R2FR_4270_DQ_GEOM_REDUCED_CANDIDATE.csv"
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
    "SRC4270_00_274_geometry_envelope": SourceSpec(
        "SRC4270_00_274_geometry_envelope",
        FORMAL / "274-PPC4161-component-zero-closure-or-epsilon-map.md",
        "epsilon_geom",
        "Current Dq_geom envelope and blocked zero route.",
    ),
    "SRC4270_01_4246_geometry_gate": SourceSpec(
        "SRC4270_01_4246_geometry_gate",
        SOURCE_DIR / "P8_Y5_R2FR_4246_GEOMETRY_ZERO_GATES.csv",
        "GZG4246_4_no_Hperp_shadow",
        "Machine-readable no-shadow gap for Hperp geometry.",
    ),
    "SRC4270_02_4247_no_shadow": SourceSpec(
        "SRC4270_02_4247_no_shadow",
        SOURCE_DIR / "P8_Y5_R2FR_4247_NO_SHADOW_SIGNATURE_AUDIT.csv",
        "NSA4247_5_same_coframe_parent",
        "Machine-readable same-observed-coframe parent gate.",
    ),
    "SRC4270_03_4248_sampler_law": SourceSpec(
        "SRC4270_03_4248_sampler_law",
        SOURCE_DIR / "P8_Y5_R2FR_4248_SAMPLER_LAWS.csv",
        "epsilon_geom_L1 = epsilon_Oloc + epsilon_coframe + epsilon_projector + epsilon_wall + epsilon_Hodge_geom",
        "Five-piece L1 geometry envelope.",
    ),
    "SRC4270_04_3860_coframe_basicness": SourceSpec(
        "SRC4270_04_3860_coframe_basicness",
        SOURCE_DIR / "P8_Y5_R2FR_3860_COFRAME_BASICNESS_THEOREM.csv",
        "CBT3860_3_current_verdict",
        "Conditional coframe basicness theorem plus current nonclaim verdict.",
    ),
    "SRC4270_05_3861_no_shadow": SourceSpec(
        "SRC4270_05_3861_no_shadow",
        SOURCE_DIR / "P8_Y5_R2FR_3861_NO_SHADOW_COFRAME_THEOREM.csv",
        "NSC3861_4_current_verdict",
        "Conditional no-shadow coframe theorem plus current nonclaim verdict.",
    ),
    "SRC4270_06_4268_boundary": SourceSpec(
        "SRC4270_06_4268_boundary",
        FORMAL / "284-PPC4161-Dq-boundary-projector-fixed-collar-or-boundary-residual-bound.md",
        "Dq_boundary_projector = 0",
        "Fixed compact no-flux collar already owns the boundary/projector leg.",
    ),
    "SRC4270_07_4263_EM": SourceSpec(
        "SRC4270_07_4263_EM",
        FORMAL / "279-PPC4161-Dq-EM-closed-collar-adoption-or-radiative-boundary-row.md",
        "Dq_EM = 0",
        "Closed-collar standard-visible EM branch prevents double-counting Hodge/Poynting as a separate source.",
    ),
    "SRC4270_08_4269_tau": SourceSpec(
        "SRC4270_08_4269_tau",
        FORMAL / "285-PPC4161-Dq-tau-reference-time-lock-or-tau-residual-bound.md",
        "Dq_tau = 0",
        "Observed-tau branch lock is already separated from geometry.",
    ),
    "SRC4270_09_4219_component_matrix": SourceSpec(
        "SRC4270_09_4219_component_matrix",
        SOURCE_DIR / "P8_Y5_R2FR_4219_DQ_COMPONENT_MATRIX.csv",
        "DQC4219_0_geometry",
        "Dq_geom is an explicit component gate, not a hidden aggregate.",
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
            "4270 attempts the remaining Dq_geom route and rejects the current full geometry zero: 4246/4247/3860/3861 still lack a parent-signed "
            "no-shadow/same-coframe certificate for Hperp. It does, however, compress the old five-piece epsilon_geom envelope by routing boundary/projector "
            "and wall pieces to the fixed-collar branch, preventing EM/Poynting/Hodge double counting, and isolating the live blocker as the core observed-readout/"
            "coframe-shadow residual."
        ),
        "current_evidence": (
            "4270 source register, geometry zero audit, residual compression table, reduced Dq_geom candidate, updated component candidate, decision and firewall."
        ),
        "status": "private_Dq_geom_full_zero_rejected_reduced_core_coframe_shadow_residual_nonclaim",
        "next_test": "Prove core coframe-shadow silence from a parent-signed no-extra-frame/coframe action, or fill the first source-backed epsilon_core_geom row.",
        "key_risk": "Treating fixed boundary/tau/EM component zeros as a proof that the observed metric/coframe has no hidden vertical shadow.",
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


def geom_zero_audit_rows() -> List[Dict[str, str]]:
    raw = [
        (
            "GZA4270_0_exact_zero_theorem",
            "Dq_geom[Hperp]=0 follows if observed local geometry and every sector coframe/readout descend through q and Hperp has no q-independent representative shadow.",
            "EXACT_CONDITIONAL_THEOREM_RETAINED",
            "This is still the right theorem shape; it is just not parent-signed in the current corpus.",
        ),
        (
            "GZA4270_1_full_zero_rejected",
            "The current corpus does not sign A_MF/no-shadow, terminal same-coframe parent ownership, source/readout inheritance, and EM no-constitutive-Hodge exclusion together.",
            "NO_FULL_ZERO_CURRENT_CORPUS",
            "Do not set Dq_geom=0 yet.",
        ),
        (
            "GZA4270_2_tau_boundary_EM_separate",
            "4268, 4269 and 4263 remove boundary/projector, observed-tau, and standard-visible EM/Poynting legs only in their narrow branches.",
            "SEPARATION_THEOREM",
            "Those zeros prevent double-counting but do not kill core coframe/metric drift.",
        ),
        (
            "GZA4270_3_projector_wall_routing",
            "Fixed compact no-flux collars route epsilon_projector and epsilon_wall into boundary/domain/tomography tails rather than independent Dq_geom pieces.",
            "ROUTED_TO_BOUNDARY_AND_TOMOGRAPHY_CONSTANTS",
            "Open boundaries or moving domains reopen explicit finite residual rows.",
        ),
        (
            "GZA4270_4_Hodge_geom_routing",
            "After EM Hodge/Poynting ownership, epsilon_Hodge_geom is not a standalone EM source; it is a geometry/coframe response unless the constitutive branch reopens.",
            "BOUNDED_BY_COFRAME_SHADOW_NOT_EM_DOUBLE_COUNT",
            "This leaves a coframe transfer constant rather than a new force row.",
        ),
        (
            "GZA4270_5_core_live_blocker",
            "The live geometry obstruction is the observed-readout/coframe-shadow core: epsilon_Oloc plus epsilon_coframe and their C1/local-profile analogues.",
            "CORE_COFRAME_SHADOW_REMAINS_OPEN",
            "4271 should attack this core directly, not circle through already closed component legs.",
        ),
    ]
    return [
        {
            **common(),
            "audit_id": audit_id,
            "statement": statement,
            "status": status,
            "guard": guard,
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
        for audit_id, statement, status, guard in raw
    ]


def residual_compression_rows() -> List[Dict[str, str]]:
    raw = [
        (
            "GRC4270_0_original_L1",
            "epsilon_geom_L1",
            "epsilon_Oloc + epsilon_coframe + epsilon_projector + epsilon_wall + epsilon_Hodge_geom",
            "SOURCE_IMPORTED_FROM_4248",
            "Starting envelope; no cancellation is allowed.",
            "formalization-workbench/274 and 4248 sampler law",
        ),
        (
            "GRC4270_1_observed_readout_core",
            "epsilon_Oloc",
            "epsilon_core_observed_readout",
            "RETAINED_CORE",
            "Observed metric/coframe/readout may still carry hidden vertical shadow.",
            "4271 target",
        ),
        (
            "GRC4270_2_coframe_shadow_core",
            "epsilon_coframe",
            "epsilon_core_coframe_shadow",
            "RETAINED_CORE",
            "No-extra-frame/no-shadow parent action is still unsigned.",
            "3860/3861 current verdicts",
        ),
        (
            "GRC4270_3_projector_tail",
            "epsilon_projector",
            "epsilon_projector_tail -> eta_domain, nabla_S_norm, eta_C1, C_perp or explicit boundary residual",
            "ROUTED_NOT_ZERO_CLAIM",
            "Fixed-collar projector silence belongs to 4268; remaining noncompact/domain pieces are tomography constants, not hidden Dq_geom magic.",
            "4268 fixed collar plus 4254 constants",
        ),
        (
            "GRC4270_4_wall_tail",
            "epsilon_wall",
            "epsilon_wall_tail -> boundary/open-sector residual or zero only in fixed compact no-flux branch",
            "ROUTED_NOT_ZERO_CLAIM",
            "Wall/interface terms cannot be silently erased; they are boundary residuals when the fixed collar is not active.",
            "4268 open-boundary split rows",
        ),
        (
            "GRC4270_5_Hodge_geom_tail",
            "epsilon_Hodge_geom",
            "C_Hodge_geom_core * epsilon_core_coframe_shadow + epsilon_constitutive_reopen",
            "DEPENDENT_ON_CORE_COFRAME_SHADOW",
            "Once EM/Poynting is owned by the visible Maxwell-Hodge branch, the remaining Hodge geometry drift is coframe response.",
            "4263 EM branch and 3861 EM no-constitutive-Hodge guard",
        ),
        (
            "GRC4270_6_reduced_bound",
            "epsilon_geom_reduced",
            "epsilon_core_observed_readout + (1 + C_Hodge_geom_core)*epsilon_core_coframe_shadow + epsilon_projector_tail + epsilon_wall_tail + epsilon_constitutive_reopen",
            "DERIVED_REDUCED_NONNUMERIC_BOUND",
            "This is narrower than the old five independent pieces but still not numeric and not zero.",
            "4270 formal result",
        ),
    ]
    return [
        {
            **common(),
            "compression_id": compression_id,
            "old_quantity": old_quantity,
            "new_quantity_or_bound": new_quantity,
            "status": status,
            "meaning": meaning,
            "source_or_next_gate": source_or_next_gate,
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
        for compression_id, old_quantity, new_quantity, status, meaning, source_or_next_gate in raw
    ]


def reduced_candidate_rows() -> List[Dict[str, str]]:
    return [
        {
            **common(),
            "candidate_id": "DQ_GEOM_REDUCED_CORE_COFRAME_SHADOW_4270",
            "probe_id": "Dq_geom",
            "old_epsilon": "MISSING_EPSILON_GEOM_L1_COMPONENT_VALUES",
            "new_epsilon": "MISSING_REDUCED_EPSILON_GEOM_CORE_COFRAME_SHADOW",
            "new_epsilon_C1": "MISSING_REDUCED_C1_GEOM_CORE_COFRAME_SHADOW",
            "source_path": str(FORMAL_PATH),
            "status": "REDUCED_NONNUMERIC_CORE_RESIDUAL_REMAINS_OPEN",
            "conditions_to_zero": (
                "parent-signed q-basic observed geometry; no-extra-frame/no-Weyl/no-disformal matter action; source/readout inheritance; "
                "terminal public coframe certificate; EM no-constitutive-Hodge exclusion; fixed compact collar or explicit boundary tails"
            ),
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
    ]


def component_candidate_rows() -> List[Dict[str, str]]:
    previous = csv_rows(LIVE_COMPONENT_CANDIDATE_PATH)
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
        if probe == "Dq_geom":
            updated["epsilon"] = "MISSING_REDUCED_EPSILON_GEOM_CORE_COFRAME_SHADOW"
            updated["epsilon_C1"] = "MISSING_REDUCED_C1_GEOM_CORE_COFRAME_SHADOW"
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
                    "epsilon": "MISSING_REDUCED_EPSILON_GEOM_CORE_COFRAME_SHADOW"
                    if probe == "Dq_geom"
                    else f"MISSING_ZERO_PROOF_OR_PROFILE_{probe}",
                    "epsilon_C1": "MISSING_REDUCED_C1_GEOM_CORE_COFRAME_SHADOW"
                    if probe == "Dq_geom"
                    else f"MISSING_C1_ZERO_PROOF_OR_PROFILE_{probe}",
                    "source_path": str(FORMAL_PATH),
                    "valid_for_claim": "False",
                }
            )
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
            "DEC4270_0_reject_full_zero",
            "Reject Dq_geom=0 as a current adoption.",
            "The no-shadow/same-coframe parent action certificate is still unsigned in 4247/3860/3861.",
            NEXT_TARGET,
        ),
        (
            "DEC4270_1_reduce_residual",
            "Compress the Dq_geom blocker to a core observed-readout/coframe-shadow residual plus routed boundary/domain tails.",
            "This is real progress: the geometry obstacle is now smaller and better targeted, not another generic missing row.",
            NEXT_TARGET,
        ),
        (
            "DEC4270_2_keep_4254_blocked",
            "Keep 4254 blocked until the reduced core residual or source-backed profile is supplied.",
            "No public local-GR/PPN/R10 claim is allowed from a nonnumeric reduced residual.",
            "Rerun 4254 after 4270 and verify Dq_geom remains the live Dq gate.",
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
        ("FW4270_0_no_geometry_zero", "Do not set Dq_geom=0 until the parent no-shadow/same-coframe certificate is signed.", "core coframe-shadow proof or sourced epsilon row"),
        ("FW4270_1_no_component_smuggling", "Do not use tau, EM or boundary component zeros to erase metric/coframe drift.", "Dq_geom remains a separate component"),
        ("FW4270_2_no_Poynting_double_count", "Do not turn Poynting/Hodge ownership into an extra force or a fake geometry zero.", "Hodge geometry drift is routed through coframe response or constitutive reopen rows"),
        ("FW4270_3_no_public_local_GR", "Do not claim local GR/PPN/R10 safety from a reduced but nonnumeric residual.", "4254 and empirical gates remain blocked"),
        ("FW4270_4_no_cancellation", "Do not cancel projector/wall/Hodge tails against core coframe terms.", "absolute L1 envelope remains active"),
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
            "status_id": "STATUS4270_0",
            "summary": (
                "4270 does not close Dq_geom, but it narrows the live target: the remaining hard object is the core observed-readout/"
                "coframe-shadow residual, with projector/wall/Hodge tails routed to existing boundary/domain/coframe-response gates."
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
            "objective": "Attack the reduced core: prove parent no-extra-frame/coframe-shadow silence, or fill the first sourced epsilon_core_geom profile row.",
            "avoid": "Do not revisit already separated tau, EM, boundary, source-readout, matter, theta or coefficient rows unless they reopen the core coframe shadow.",
            "valid_for_claim": "False",
        }
    ]


def formal_doc() -> str:
    return f"""
# 286 - PPC4161 Dq-geom core coframe-shadow or reduced epsilon bound

Marker: `{MARKER}`

Branch: `{BRANCH}`

Decision: `{DECISION}`

## Private nonclaim

4270 does not prove:

```text
Dq_geom = 0
```

and it does not prove local GR, PPN safety, R10 safety, clock safety, orbital safety, or a public Newton/Einstein limit.

## Zero attempt

The exact zero theorem remains:

```text
observed geometry = geometry_bar(q),
sector coframes/readouts descend through q,
Hperp has no q-independent representative shadow
=> Dq_geom[Hperp] = 0.
```

But the current corpus still blocks this theorem at the same hard place:

```text
parent-signed A_MF/no-shadow,
terminal same observed-coframe ownership,
source/readout inheritance,
no independent Weyl/disformal/constitutive frame slot,
EM no-constitutive-Hodge exclusion.
```

So 4270 rejects a present full zero:

```text
Dq_geom != adopted zero.
```

## What is actually derived

The previous envelope was:

```text
epsilon_geom_L1
= epsilon_Oloc
 + epsilon_coframe
 + epsilon_projector
 + epsilon_wall
 + epsilon_Hodge_geom.
```

After 4263, 4268 and 4269, the tau, EM/Poynting/Hodge-flux and fixed-collar boundary/projector rows are separate components. They cannot be used to kill geometry, but they do stop the geometry row from double-counting them.

Thus the geometry obstruction can be compressed to:

```text
epsilon_geom_reduced
<= epsilon_core_observed_readout
 + (1 + C_Hodge_geom_core) epsilon_core_coframe_shadow
 + epsilon_projector_tail
 + epsilon_wall_tail
 + epsilon_constitutive_reopen.
```

Where:

```text
epsilon_core_observed_readout  ~ epsilon_Oloc,
epsilon_core_coframe_shadow    ~ epsilon_coframe,
epsilon_projector_tail         -> eta_domain, nabla_S_norm, eta_C1, C_perp or boundary residual,
epsilon_wall_tail              -> open-boundary/interface residual unless fixed compact no-flux collar applies,
epsilon_constitutive_reopen    -> only if the visible EM/matter branch admits an independent Hodge/constitutive frame slot.
```

This is narrower than the old five independent missing pieces, but it is not numeric and not zero.

## Live 4254 feed

The live component candidate is updated from:

```text
MISSING_EPSILON_GEOM_L1_COMPONENT_VALUES
```

to:

```text
MISSING_REDUCED_EPSILON_GEOM_CORE_COFRAME_SHADOW.
```

The C1 row becomes:

```text
MISSING_REDUCED_C1_GEOM_CORE_COFRAME_SHADOW.
```

## Next target

`{NEXT_TARGET}` should attack the core directly:

```text
prove epsilon_core_observed_readout = epsilon_core_coframe_shadow = 0
```

from a parent-signed no-extra-frame/coframe action, or fill the first source-backed local profile row for that core.
"""


def checkpoint_doc() -> str:
    return f"""
# 4270 - Y5 R2FR Dq-geom core coframe-shadow or reduced epsilon bound

Packet marker: `{PACKET_MARKER}`

## Result

Full geometry zero is still rejected. The work did move, though: the old five-piece geometry blocker has been compressed to a core observed-readout/coframe-shadow residual plus routed projector/wall/Hodge tails.

## Human translation

We are no longer saying "geometry is missing" in a vague way. The remaining dragon is now specific:

```text
Does the parent action force the public coframe/metric to be the only frame ordinary matter can see?
```

If yes, the local-GR branch has a serious shot. If not, we need a real numeric epsilon profile for the coframe shadow.

## Claim firewall

This is private and nonclaim. No local-GR/PPN/R10 pass is allowed from 4270.
"""


def validation_rows(paths: Dict[str, Path]) -> List[Dict[str, str]]:
    sources = csv_rows(paths["sources"])
    audit = csv_rows(paths["audit"])
    compression = csv_rows(paths["compression"])
    reduced = csv_rows(paths["reduced"])
    local_candidate = csv_rows(paths["local_candidate"])
    live_candidate = csv_rows(LIVE_COMPONENT_CANDIDATE_PATH)
    live_geom = [row for row in live_candidate if row.get("probe_id") == "Dq_geom"]
    live_geom_is_4270 = (
        bool(live_geom)
        and live_geom[0].get("epsilon") == "MISSING_REDUCED_EPSILON_GEOM_CORE_COFRAME_SHADOW"
        and live_geom[0].get("epsilon_C1") == "MISSING_REDUCED_C1_GEOM_CORE_COFRAME_SHADOW"
        and live_geom[0].get("source_path") == str(FORMAL_PATH)
    )
    live_geom_is_later_4271 = (
        bool(live_geom)
        and live_geom[0].get("epsilon") == "MISSING_CORE_FRAME_COUPLING_ZERO_OR_NUMERIC_CG_BDIS_BOUND"
        and live_geom[0].get("epsilon_C1") == "MISSING_C1_CORE_FRAME_COUPLING_ZERO_OR_NUMERIC_CG_BDIS_BOUND"
        and live_geom[0].get("source_path") == str(FORMAL_4271_PATH)
    )
    live_geom_is_later_4272 = (
        bool(live_geom)
        and live_geom[0].get("epsilon") == "MISSING_SCOREABLE_CG_BDIS_FRAME_VECTOR_INPUTS"
        and live_geom[0].get("epsilon_C1") == "MISSING_C1_SCOREABLE_CG_BDIS_FRAME_VECTOR_INPUTS"
        and live_geom[0].get("source_path") == str(FORMAL_4272_PATH)
    )
    prior_zero_components = {
        "Dq_tau": "285-PPC4161-Dq-tau-reference-time-lock-or-tau-residual-bound.md",
        "Dq_matter": "281-PPC4161-Dq-matter-action-domain-zero-or-source-prefactor-bound.md",
        "Dq_source_readout": "282-PPC4161-Dq-source-readout-Hilbert-charge-zero-or-coefficient-remainder.md",
        "Dq_theta_marker": "280-PPC4161-Dq-theta-marker-component-zero-or-marker-bound.md",
        "Dq_boundary_projector": "284-PPC4161-Dq-boundary-projector-fixed-collar-or-boundary-residual-bound.md",
        "Dq_EM": "279-PPC4161-Dq-EM-closed-collar-adoption-or-radiative-boundary-row.md",
        "Dq_coeff": "283-PPC4161-Dq-coeff-fixed-parent-constant-or-Newton-calibration-bound.md",
    }
    prior_zeros_preserved = True
    for probe, source_file in prior_zero_components.items():
        rows = [row for row in live_candidate if row.get("probe_id") == probe]
        if not rows or rows[0].get("epsilon") != "0.0" or source_file not in rows[0].get("source_path", ""):
            prior_zeros_preserved = False
    mapped_old_quantities = {row.get("old_quantity") for row in compression}
    rows = [
        ("VAL4270_0_sources_exist", all(row["exists"] == "True" for row in sources), "all source paths exist"),
        ("VAL4270_1_needles_found", all(row["required_text_found"] == "True" for row in sources), "all source needles found"),
        (
            "VAL4270_2_full_zero_rejected",
            any(row["status"] == "NO_FULL_ZERO_CURRENT_CORPUS" for row in audit),
            "Dq_geom full zero explicitly rejected",
        ),
        (
            "VAL4270_3_core_live_blocker",
            any(row["status"] == "CORE_COFRAME_SHADOW_REMAINS_OPEN" for row in audit),
            "core coframe-shadow blocker retained",
        ),
        (
            "VAL4270_4_all_original_pieces_mapped",
            {"epsilon_Oloc", "epsilon_coframe", "epsilon_projector", "epsilon_wall", "epsilon_Hodge_geom"}.issubset(mapped_old_quantities),
            "all five old epsilon_geom pieces mapped",
        ),
        (
            "VAL4270_5_reduced_bound_emitted",
            any(row["old_quantity"] == "epsilon_geom_reduced" and row["status"] == "DERIVED_REDUCED_NONNUMERIC_BOUND" for row in compression),
            "reduced nonnumeric geometry bound emitted",
        ),
        (
            "VAL4270_6_reduced_candidate_nonclaim",
            bool(reduced)
            and reduced[0]["new_epsilon"] == "MISSING_REDUCED_EPSILON_GEOM_CORE_COFRAME_SHADOW"
            and reduced[0]["valid_for_claim"] == "False",
            "reduced Dq_geom candidate is nonclaim",
        ),
        (
            "VAL4270_7_live_4254_updated_nonzero",
            live_geom_is_4270 or live_geom_is_later_4271 or live_geom_is_later_4272,
            "live 4254 candidate Dq_geom updated to 4270 reduced row or later refinement",
        ),
        (
            "VAL4270_8_local_candidate_matches_live",
            (
                any(row.get("probe_id") == "Dq_geom" and row.get("source_path") == str(FORMAL_PATH) for row in local_candidate)
                and live_geom_is_4270
            )
            or (
                any(row.get("probe_id") == "Dq_geom" and row.get("source_path") == str(FORMAL_4271_PATH) for row in local_candidate)
                and live_geom_is_later_4271
            )
            or (
                any(row.get("probe_id") == "Dq_geom" and row.get("source_path") == str(FORMAL_4272_PATH) for row in local_candidate)
                and live_geom_is_later_4272
            ),
            "local and live candidates carry 4270 source or later refinement source",
        ),
        (
            "VAL4270_9_prior_zero_adoptions_preserved",
            prior_zeros_preserved,
            "prior tau/matter/source/theta/boundary/EM/coefficient zero rows preserved",
        ),
        (
            "VAL4270_10_no_fake_claim",
            bool(live_geom) and live_geom[0].get("epsilon") != "0.0" and all(row.get("valid_for_claim") == "False" for row in sources + audit + compression),
            "geometry remains nonzero/nonclaim",
        ),
        ("VAL4270_11_claim_row", CLAIM_ID in read_text(FORMAL / "02-claims-register.csv"), "claim register row added"),
        ("VAL4270_12_formal_doc", MARKER in read_text(FORMAL_PATH), "formal marker present"),
        ("VAL4270_13_checkpoint_doc", PACKET_MARKER in read_text(DOC_PATH), "checkpoint marker present"),
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
    source_path = SOURCE_DIR / "P8_Y5_R2FR_4270_SOURCE_REGISTER.csv"
    audit_path = SOURCE_DIR / "P8_Y5_R2FR_4270_GEOM_ZERO_AUDIT.csv"
    compression_path = SOURCE_DIR / "P8_Y5_R2FR_4270_GEOM_RESIDUAL_COMPRESSION.csv"
    decision_path = SOURCE_DIR / "P8_Y5_R2FR_4270_DECISION.csv"
    firewall_path = SOURCE_DIR / "P8_Y5_R2FR_4270_CLAIM_FIREWALL.csv"
    status_path = SOURCE_DIR / "P8_Y5_R2FR_4270_STATUS.csv"
    next_path = SOURCE_DIR / "P8_Y5_R2FR_4270_NEXT_TARGET.csv"

    component_candidate = component_candidate_rows()
    write_csv(source_path, source_rows())
    write_csv(audit_path, geom_zero_audit_rows())
    write_csv(compression_path, residual_compression_rows())
    write_csv(REDUCED_CANDIDATE_PATH, reduced_candidate_rows())
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
        "audit": audit_path,
        "compression": compression_path,
        "reduced": REDUCED_CANDIDATE_PATH,
        "local_candidate": LOCAL_COMPONENT_CANDIDATE_PATH,
    }
    validation = validation_rows(paths)
    write_csv(VALIDATION_PATH, validation)
    failed = [row for row in validation if row["passed"] != "True"]
    print(f"{CHECKPOINT}: wrote 9 csv artifacts plus validation")
    print(f"{CHECKPOINT}: validation rows={len(validation)} failed={len(failed)}")
    print(f"{CHECKPOINT}: decision={DECISION}")


if __name__ == "__main__":
    main()

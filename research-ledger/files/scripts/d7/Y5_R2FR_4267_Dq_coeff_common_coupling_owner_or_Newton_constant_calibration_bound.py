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

CHECKPOINT = "4267"
CLAIM_ID = "L-108"
BRANCH = "MTS_R2FR_Y5_DQ_COEFF_FIXED_PARENT_CONSTANT_OR_NEWTON_CALIBRATION_BOUND_4267"
DECISION = "DQ_COEFF_ADOPTED_FOR_FIXED_PARENT_CONSTANT_BRANCH_NUMERIC_G_REMAINS_CALIBRATED_NONCLAIM"
MARKER = "PPC4161_DQ_COEFF_FIXED_PARENT_CONSTANT_OR_NEWTON_CALIBRATION_BOUND_4267"
PACKET_MARKER = "PPC4161_PACKET_DQ_COEFF_FIXED_PARENT_CONSTANT_OR_NEWTON_CALIBRATION_BOUND_4267"
NEXT_TARGET = "4268-Y5-R2FR-Dq-boundary-projector-fixed-collar-or-boundary-residual-bound.md"

FORMAL_PATH = FORMAL / "283-PPC4161-Dq-coeff-fixed-parent-constant-or-Newton-calibration-bound.md"
DOC_PATH = POST / "4267-Y5-R2FR-Dq-coeff-common-coupling-owner-or-Newton-constant-calibration-bound.md"
VALIDATION_PATH = SOURCE_DIR / "P8_Y5_BRR545_4267_VALIDATION.csv"
ADOPTION_4268_PATH = SOURCE_DIR / "P8_Y5_R2FR_4268_DQ_BOUNDARY_PROJECTOR_ADOPTION.csv"
FORMAL_4268_PATH = FORMAL / "284-PPC4161-Dq-boundary-projector-fixed-collar-or-boundary-residual-bound.md"
ADOPTION_4269_PATH = SOURCE_DIR / "P8_Y5_R2FR_4269_DQ_TAU_ADOPTION.csv"
FORMAL_4269_PATH = FORMAL / "285-PPC4161-Dq-tau-reference-time-lock-or-tau-residual-bound.md"
REDUCED_GEOM_4270_PATH = SOURCE_DIR / "P8_Y5_R2FR_4270_DQ_GEOM_REDUCED_CANDIDATE.csv"
FORMAL_4270_PATH = FORMAL / "286-PPC4161-Dq-geom-core-coframe-shadow-or-reduced-epsilon-bound.md"
CORE_GEOM_4271_PATH = SOURCE_DIR / "P8_Y5_R2FR_4271_DQ_GEOM_CORE_FRAME_CANDIDATE.csv"
FORMAL_4271_PATH = FORMAL / "287-PPC4161-core-coframe-shadow-zero-or-first-source-backed-epsilon-row.md"
BOUND_GEOM_4272_PATH = SOURCE_DIR / "P8_Y5_R2FR_4272_DQ_GEOM_BOUND_RUNNER_CANDIDATE.csv"
FORMAL_4272_PATH = FORMAL / "288-PPC4161-parent-no-extra-frame-signature-or-cg-bdis-first-bound-runner.md"

LIVE_COMPONENT_CANDIDATE_PATH = SOURCE_DIR / "P8_Y5_R2FR_4254_DQ_COMPONENT_VALUES_CANDIDATE.csv"
LOCAL_COMPONENT_CANDIDATE_PATH = SOURCE_DIR / "P8_Y5_R2FR_4267_DQ_COMPONENT_VALUES_CANDIDATE.csv"

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
    "SRC4267_00_4219_dq_contract": SourceSpec(
        "SRC4267_00_4219_dq_contract",
        FORMAL / "235-PPC4161-Dq-source-readout-coupling-marker-zero-or-bound.md",
        "Dq_coeff[v]=0",
        "Componentwise Dq zero contract names coefficient markers as their own leg.",
    ),
    "SRC4267_01_4264_constants": SourceSpec(
        "SRC4267_01_4264_constants",
        FORMAL / "280-PPC4161-Dq-theta-marker-component-zero-or-marker-bound.md",
        "alpha_EM, hbar, c",
        "Typed visible constants were already treated as fixed-before-variation markers.",
    ),
    "SRC4267_02_4265_coeff_tax": SourceSpec(
        "SRC4267_02_4265_coeff_tax",
        FORMAL / "281-PPC4161-Dq-matter-action-domain-zero-or-source-prefactor-bound.md",
        "kappa/G/ell_J coefficient drift",
        "4265 retained coefficient drift as a separate gate.",
    ),
    "SRC4267_03_4266_newton": SourceSpec(
        "SRC4267_03_4266_newton",
        FORMAL / "282-PPC4161-Dq-source-readout-Hilbert-charge-zero-or-coefficient-remainder.md",
        "This is the same reason GR uses a coupling constant",
        "4266 isolated the Newton/kappa owner from Hilbert source readout.",
    ),
    "SRC4267_04_1113_no_morphism": SourceSpec(
        "SRC4267_04_1113_no_morphism",
        POST / "1113-Y5-R10-parent-owned-readout-descent-contract-or-alpha-product-input-acquisition.md",
        "visible EM/matter coefficients cannot take hidden representatives as arguments",
        "No-hidden-visible coefficient morphism is the global coupling bottleneck.",
    ),
    "SRC4267_05_1115_counterexample": SourceSpec(
        "SRC4267_05_1115_counterexample",
        POST / "1115-Y5-R10-local-invariant-algebra-triviality-or-finite-coupling-prior-widths.md",
        "surviving scalar feeds continuous coefficients",
        "Hidden scalar coefficient dependence remains the retained counterexample if constants are not typed fixed.",
    ),
    "SRC4267_06_4266_remainder": SourceSpec(
        "SRC4267_06_4266_remainder",
        SOURCE_DIR / "P8_Y5_R2FR_4266_REMAINDER_SPLIT_ROWS.csv",
        "REM4266_0_kappa_G_owner",
        "4266 handed kappa/G ownership to Dq_coeff.",
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


def dq_boundary_projector_4268_adoption_row() -> Dict[str, str]:
    for row in csv_rows(ADOPTION_4268_PATH):
        if (
            row.get("component") == "Dq_boundary_projector"
            and row.get("new_epsilon") == "0.0"
            and row.get("adoption_status") == "ADOPTED_CONDITIONAL_ZERO_FOR_FIXED_NOFLUX_COLLAR_BRANCH_ONLY"
        ):
            return row
    return {}


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
            "4267 adopts Dq_coeff=0 and its C1 row only for the fixed parent-action constant branch: kappa, G_N, ell_J, "
            "visible charge normalizations and unit conventions are parameters/calibration constants, not hidden-field-dependent "
            "functions. This proves zero hidden vertical drift of the coupling owner, but does not derive the numerical value of G_N "
            "or forbid a future deeper parent derivation; any hidden scalar-dependent coefficient reopens a finite bound branch."
        ),
        "current_evidence": (
            "4267 source register, fixed-constant coefficient theorem rows, Newton calibration split rows, Dq_coeff adoption row, "
            "updated component candidate, decision and firewall."
        ),
        "status": "private_Dq_coeff_conditional_zero_adopted_for_fixed_parent_constant_branch_nonclaim",
        "next_test": "Attack Dq_boundary_projector next; 4254 remains blocked by boundary/projector, geometry/tau and tomography constants.",
        "key_risk": "Confusing zero coefficient drift with a derivation of the numerical Newton constant or hiding hidden scalar coefficient functions as constants.",
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


def coefficient_theorem_rows() -> List[Dict[str, str]]:
    raw = [
        (
            "COEFF4267_0_definition_split",
            "coefficient component",
            "Dq_coeff measures hidden vertical drift of coupling and normalization owners, not their numerical measured values.",
            "DEFINITION_SPLIT",
            "numeric G_N and unit conventions are not claimed derived",
        ),
        (
            "COEFF4267_1_parameter_derivative_zero",
            "fixed parameter vertical derivative",
            "If kappa, G_N, ell_J, charge normalization and unit conventions are parent action parameters or calibration constants, not fields or readout functionals, then delta_v coefficient = 0 for v in ker(Dq).",
            "CONDITIONAL_ZERO_FOR_FIXED_PARENT_CONSTANTS",
            "fails if any coefficient is promoted to c(Phi), c(I_hidden), or a reduced-action knob",
        ),
        (
            "COEFF4267_2_C1_zero",
            "constant-sector C1 silence",
            "A fixed parameter has zero local derivative on the collar, so the C1 coefficient row also vanishes in the standard fixed-constant branch.",
            "CONDITIONAL_C1_ZERO_FOR_FIXED_PARENT_CONSTANTS",
            "fails for running environment-dependent effective coefficients",
        ),
        (
            "COEFF4267_3_Newton_distinction",
            "Newton constant distinction",
            "Local GR/Newton reduction requires delta_v G_N=0, not a derivation of the numerical value of G_N. GR itself supplies G_N as a measured coupling.",
            "NO_NUMERIC_G_CLAIM",
            "a deeper MTS derivation of G_N would be a future parent-action result, not a prerequisite for this local branch",
        ),
        (
            "COEFF4267_4_hidden_scalar_counterexample",
            "hidden coefficient counterexample",
            "If a surviving hidden scalar I is allowed in c=c0+epsilon I, then Dq_coeff is nonzero unless epsilon=0 or I is proved locally constant.",
            "RETAINED_BOUND_FORK_IF_PROMOTED",
            "prevents smuggling dynamic couplings into fixed constants",
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


def calibration_split_rows() -> List[Dict[str, str]]:
    raw = [
        ("CAL4267_0_kappa", "kappa_or_8piG_over_c4", "fixed parent action coupling or calibrated common constant", "Dq_coeff", "ZERO_IN_FIXED_CONSTANT_BRANCH"),
        ("CAL4267_1_ellJ", "ell_J_or_source_current_norm", "fixed source-current normalization scale", "Dq_coeff", "ZERO_IN_FIXED_CONSTANT_BRANCH"),
        ("CAL4267_2_visible_charge", "alpha_EM_or_charge_normalization", "typed visible EM calibration constant already protected by 4262/4264", "Dq_coeff", "ZERO_IN_FIXED_CONSTANT_BRANCH"),
        ("CAL4267_3_hidden_scalar_coeff", "c0_plus_epsilon_I_hidden", "hidden scalar-dependent coefficient if promoted", "finite_bound_fork", "RETAINED_IF_ADDED"),
        ("CAL4267_4_numeric_G", "numeric_value_of_G_N", "measured/calibrated value, not derived by this local Dq gate", "future_parent_derivation_or_empirical_input", "NOT_CLAIMED"),
        ("CAL4267_5_radiative_running", "environment_or_scale_running_counterterm", "effective/radiative coefficient drift if it depends on hidden local branch", "finite_bound_fork", "RETAINED_IF_ADDED"),
    ]
    return [
        {
            **common(),
            "split_id": split_id,
            "coefficient": coefficient,
            "meaning": meaning,
            "assigned_gate": gate,
            "4267_status": status,
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
            "adoption_id": "ADOPT4267_Dq_coeff",
            "component": "Dq_coeff",
            "old_epsilon": "MISSING_ZERO_PROOF_OR_PROFILE_Dq_coeff",
            "new_epsilon": "0.0",
            "new_epsilon_C1": "0.0",
            "adoption_status": "ADOPTED_CONDITIONAL_ZERO_FOR_FIXED_PARENT_CONSTANT_BRANCH_ONLY",
            "source_path": str(FORMAL_PATH),
            "conditions": (
                "kappa/G/ell_J/visible normalization constants are fixed parent-action parameters or calibrated q-basic constants before variation; "
                "no hidden scalar-dependent coefficient c(Phi), no reduced-action readout knob, no environment-dependent running coefficient is promoted"
            ),
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
    ]


def component_candidate_rows() -> List[Dict[str, str]]:
    previous = csv_rows(LIVE_COMPONENT_CANDIDATE_PATH)
    adoption_4268 = dq_boundary_projector_4268_adoption_row()
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
        if probe == "Dq_coeff":
            updated["epsilon"] = "0.0"
            updated["epsilon_C1"] = "0.0"
            updated["source_path"] = str(FORMAL_PATH)
            updated["valid_for_claim"] = "False"
        elif probe == "Dq_boundary_projector" and adoption_4268:
            updated["epsilon"] = adoption_4268.get("new_epsilon", "0.0")
            updated["epsilon_C1"] = adoption_4268.get("new_epsilon_C1", "0.0")
            updated["source_path"] = str(FORMAL_4268_PATH)
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
                    "epsilon": "0.0" if probe == "Dq_coeff" else (adoption_4268.get("new_epsilon", "0.0") if probe == "Dq_boundary_projector" and adoption_4268 else (adoption_4269.get("new_epsilon", "0.0") if probe == "Dq_tau" and adoption_4269 else f"MISSING_ZERO_PROOF_OR_PROFILE_{probe}")),
                    "epsilon_C1": "0.0" if probe == "Dq_coeff" else (adoption_4268.get("new_epsilon_C1", "0.0") if probe == "Dq_boundary_projector" and adoption_4268 else (adoption_4269.get("new_epsilon_C1", "0.0") if probe == "Dq_tau" and adoption_4269 else f"MISSING_C1_ZERO_PROOF_OR_PROFILE_{probe}")),
                    "source_path": str(FORMAL_PATH) if (probe != "Dq_boundary_projector" or not adoption_4268) and (probe != "Dq_tau" or not adoption_4269) else (str(FORMAL_4268_PATH) if probe == "Dq_boundary_projector" else str(FORMAL_4269_PATH)),
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
            "DEC4267_0_adopt_coeff",
            "Adopt Dq_coeff=0 for the fixed parent-action/calibrated-constant branch.",
            "The variational derivative of a parameter that is not a field/readout functional is zero.",
            NEXT_TARGET,
        ),
        (
            "DEC4267_1_no_numeric_G_claim",
            "Do not claim the numerical Newton constant is derived.",
            "The local reduction needs no hidden vertical drift of the coupling, while the value can remain a calibrated action parameter as in GR.",
            "A deeper parent derivation of G_N is optional future work, not a local-GR closure shortcut.",
        ),
        (
            "DEC4267_2_4254_progress",
            "4254 should now lose Dq_coeff from the missing list while staying blocked by geometry, tau, boundary/projector and constants.",
            "This moves the local-GR ladder from source/coupling leaks to geometry/tau/boundary and tomography constants.",
            "Rerun 4254 after 4267.",
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
        ("FW4267_0_numeric_G", "claiming a numerical derivation of G_N from Dq_coeff=0", "SEPARATE_PARENT_G_DERIVATION_REQUIRED"),
        ("FW4267_1_hidden_scalar", "calling c(Phi) a constant after allowing hidden scalar dependence", "FINITE_COEFFICIENT_BOUND_REQUIRED"),
        ("FW4267_2_radiative_running", "ignoring environment or scale dependent effective coefficients", "RADIATIVE_READOUT_BOUND_REQUIRED"),
        ("FW4267_3_local_GR_jump", "treating coefficient silence as local-GR/PPN/R10 pass", "REMAINING_COMPONENTS_AND_TOMOGRAPHY_REQUIRED"),
        ("FW4267_4_species_tuning", "using fixed coefficients to tune away species/source nonuniversality", "NO_RETUNE_AND_SOURCE_FUNCTOR_GATES_REQUIRED"),
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
            "status_id": "STATUS4267_0",
            "summary": (
                "4267 moves Dq_coeff from missing to a conditional zero for fixed parent-action/calibrated constants, "
                "while explicitly retaining the numerical value of G_N and any hidden-field-dependent coefficient as separate future gates."
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
            "objective": "Attack Dq_boundary_projector: fixed closed collar/worldtube versus explicit boundary residual bound.",
            "avoid": "Do not use fixed coefficients to hide moving boundaries, domain selectors, or source projectors.",
            "valid_for_claim": "False",
        }
    ]


def formal_doc() -> str:
    return f"""
# 283 - PPC4161 Dq-coeff fixed parent constant or Newton calibration bound

Marker: `{MARKER}`

Branch: `{BRANCH}`

Decision: `{DECISION}`

## Private nonclaim

4267 does not derive the numerical value of `G_N`, `kappa`, `ell_J`, `alpha_EM`, or any particle constant.

It adopts:

```text
Dq_coeff = 0
```

only for the fixed parent-action/calibrated-constant branch.

## What is actually proved

The local variational direction `v in ker(Dq)` differentiates fields, representatives and readout functionals. It does not differentiate a parameter that is declared fixed before variation.

Thus, for a parent action parameter:

```text
delta_v kappa = 0,
delta_v G_N = 0,
delta_v ell_J = 0
```

and similarly for visible-sector calibration constants already typed by the 4262/4264 branch.

This gives:

```text
Dq_coeff = 0,
Dq_coeff_C1 = 0
```

inside the standard fixed-constant branch.

## Newton constant distinction

This does not answer:

```text
why is G_N numerically 6.67e-11 SI?
```

It answers the local-GR reduction question:

```text
does hidden vertical motion make the coupling drift locally?
```

For the fixed parent-action branch:

```text
no.
```

This is exactly the GR-style stance: `G_N` is a measured coupling in the action. A deeper MTS derivation of its value can be added later, but local GR does not require that deeper derivation to avoid a fifth-force/source-coupling leak.

## Counterexample fork

If MTS promotes any coefficient to:

```text
c(Phi), c(I_hidden), c(domain), c(memory),
```

then:

```text
delta_v c != 0
```

unless the hidden scalar is proved locally constant or the coefficient derivative is source-backed bounded. That branch is not adopted here.

## 4254 feed

The live component candidate is updated:

```text
Dq_coeff = 0.0,
Dq_coeff_C1 = 0.0.
```

The row remains `valid_for_claim=false` because the complete 4254 source-probe/tomography gate still needs geometry, tau, boundary/projector and constants.

## Next target

`{NEXT_TARGET}` should attack `Dq_boundary_projector`.
"""


def checkpoint_doc() -> str:
    return f"""
# 4267 - Y5 R2FR Dq-coeff common coupling owner or Newton constant calibration bound

Packet marker: `{PACKET_MARKER}`

## Result

4267 adopts:

```text
Dq_coeff = 0.0,
Dq_coeff_C1 = 0.0
```

for fixed parent-action/calibrated constants only.

## Human translation

This does not derive `G_N`. It proves that if `G_N/kappa` is an action parameter, hidden local representative motion does not make it drift. That is enough for this local-GR gate and matches how GR treats Newton's constant.

## Claim status

Private nonclaim. Dynamic hidden coefficients still reopen finite bound rows.
"""


def validation_rows(paths: Dict[str, Path]) -> List[Dict[str, str]]:
    sources = csv_rows(paths["sources"])
    theorems = csv_rows(paths["theorems"])
    split = csv_rows(paths["split"])
    adoption = csv_rows(paths["adoption"])
    local_candidate = csv_rows(paths["local_candidate"])
    live_candidate = csv_rows(LIVE_COMPONENT_CANDIDATE_PATH)
    live_coeff = [row for row in live_candidate if row.get("probe_id") == "Dq_coeff"]
    live_source = [row for row in live_candidate if row.get("probe_id") == "Dq_source_readout"]
    live_matter = [row for row in live_candidate if row.get("probe_id") == "Dq_matter"]
    live_theta = [row for row in live_candidate if row.get("probe_id") == "Dq_theta_marker"]
    live_em = [row for row in live_candidate if row.get("probe_id") == "Dq_EM"]
    live_boundary = [row for row in live_candidate if row.get("probe_id") == "Dq_boundary_projector"]
    boundary_adoption = dq_boundary_projector_4268_adoption_row()
    rows = [
        ("VAL4267_0_sources_exist", all(row["exists"] == "True" for row in sources), "all source paths exist"),
        ("VAL4267_1_needles_found", all(row["required_text_found"] == "True" for row in sources), "all source needles found"),
        (
            "VAL4267_2_fixed_constant_theorem",
            any(row["status"] == "CONDITIONAL_ZERO_FOR_FIXED_PARENT_CONSTANTS" for row in theorems),
            "fixed-constant coefficient zero theorem emitted",
        ),
        (
            "VAL4267_3_numeric_G_not_claimed",
            any(row["4267_status"] == "NOT_CLAIMED" and row["coefficient"] == "numeric_value_of_G_N" for row in split),
            "numeric Newton constant kept outside this gate",
        ),
        (
            "VAL4267_4_adoption_row",
            bool(adoption)
            and adoption[0]["new_epsilon"] == "0.0"
            and adoption[0]["adoption_status"] == "ADOPTED_CONDITIONAL_ZERO_FOR_FIXED_PARENT_CONSTANT_BRANCH_ONLY",
            "Dq_coeff adoption row emitted",
        ),
        (
            "VAL4267_5_local_candidate_numeric",
            any(row.get("probe_id") == "Dq_coeff" and row.get("epsilon") == "0.0" and row.get("epsilon_C1") == "0.0" for row in local_candidate),
            "local 4267 candidate has numeric coefficient zero",
        ),
        (
            "VAL4267_6_live_4254_updated",
            bool(live_coeff)
            and live_coeff[0].get("epsilon") == "0.0"
            and live_coeff[0].get("epsilon_C1") == "0.0"
            and live_coeff[0].get("source_path") == str(FORMAL_PATH),
            "live 4254 candidate Dq_coeff updated",
        ),
        (
            "VAL4267_7_preserve_prior_adoptions",
            bool(live_em)
            and live_em[0].get("epsilon") == "0.0"
            and bool(live_theta)
            and live_theta[0].get("epsilon") == "0.0"
            and bool(live_matter)
            and live_matter[0].get("epsilon") == "0.0"
            and bool(live_source)
            and live_source[0].get("epsilon") == "0.0",
            "prior Dq_EM, Dq_theta_marker, Dq_matter and Dq_source_readout adoptions preserved",
        ),
        (
            "VAL4267_8_boundary_not_smuggled_or_later_sourced",
            bool(live_boundary)
            and (
                live_boundary[0].get("epsilon") != "0.0"
                or (
                    bool(boundary_adoption)
                    and live_boundary[0].get("epsilon") == "0.0"
                    and live_boundary[0].get("source_path") == str(FORMAL_4268_PATH)
                )
            ),
            "Dq_boundary_projector is either still live or zero only from the later 4268 sourced collar theorem",
        ),
        ("VAL4267_9_claim_row", CLAIM_ID in read_text(FORMAL / "02-claims-register.csv"), "claim register row added"),
        ("VAL4267_10_formal_doc", MARKER in read_text(FORMAL_PATH), "formal marker present"),
        ("VAL4267_11_checkpoint_doc", PACKET_MARKER in read_text(DOC_PATH), "checkpoint marker present"),
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
    source_path = SOURCE_DIR / "P8_Y5_R2FR_4267_SOURCE_REGISTER.csv"
    theorem_path = SOURCE_DIR / "P8_Y5_R2FR_4267_COEFFICIENT_THEOREM.csv"
    split_path = SOURCE_DIR / "P8_Y5_R2FR_4267_NEWTON_CALIBRATION_SPLIT_ROWS.csv"
    adoption_path = SOURCE_DIR / "P8_Y5_R2FR_4267_DQ_COEFF_ADOPTION.csv"
    decision_path = SOURCE_DIR / "P8_Y5_R2FR_4267_DECISION.csv"
    firewall_path = SOURCE_DIR / "P8_Y5_R2FR_4267_CLAIM_FIREWALL.csv"
    status_path = SOURCE_DIR / "P8_Y5_R2FR_4267_STATUS.csv"
    next_path = SOURCE_DIR / "P8_Y5_R2FR_4267_NEXT_TARGET.csv"

    component_candidate = component_candidate_rows()
    write_csv(source_path, source_rows())
    write_csv(theorem_path, coefficient_theorem_rows())
    write_csv(split_path, calibration_split_rows())
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

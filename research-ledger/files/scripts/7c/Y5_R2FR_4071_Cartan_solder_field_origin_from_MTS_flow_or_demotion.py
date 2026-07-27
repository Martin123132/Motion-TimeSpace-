from __future__ import annotations

import csv
import py_compile
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, Iterable, List, Tuple


ROOT = Path(__file__).resolve().parents[1]
PROJECT = ROOT.parent
FORMALIZATION = PROJECT / "formalization-workbench"
SOURCE_DIR = ROOT / "source-intake" / "mts_residuals"
SCRIPT_PATH = Path(__file__).resolve()
DOC_PATH = ROOT / "4071-Y5-R2FR-Cartan-solder-field-origin-from-MTS-flow-or-demotion.md"

DECISION = "LOCAL_MOTION_FRAME_GAUGE_FORCES_CARTAN_FIELDS_CONDITIONALLY_CURRENT_MTS_SIGNATURE_NOT_PARENT_SIGNED"

SOURCES: Dict[str, Tuple[Path, str, str]] = {
    "SRC4071_00_4070_next": (
        SOURCE_DIR / "P8_Y5_R2FR_4070_NEXT_TARGET.csv",
        "derive B^A and omega^AB from MTS motion/flow/memory variables",
        "4070 selected Cartan solder-field origin as the next target.",
    ),
    "SRC4071_01_4070_cartan": (
        SOURCE_DIR / "P8_Y5_R2FR_4070_CARTAN_SOLDER_PARENT_ACTION.csv",
        "CSA4070_1_solder_connection",
        "4070 identifies B^A as the necessary solder repair.",
    ),
    "SRC4071_02_4070_flat": (
        SOURCE_DIR / "P8_Y5_R2FR_4070_EXACT_GRADIENT_FLATNESS_OBSTRUCTION.csv",
        "GFO4070_0_exact_scalar_coframe",
        "4070 rejects exact scalar coframes as curved-GR derivations.",
    ),
    "SRC4071_03_4070_torsion": (
        SOURCE_DIR / "P8_Y5_R2FR_4070_TORSION_EXTRA_MODE_GATE.csv",
        "TEX4070_0_torsion_zero",
        "4070 keeps torsion as an explicit gate.",
    ),
    "SRC4071_04_primitives": (
        FORMALIZATION / "03-unified-field-theory-programme.md",
        "Candidate MTS primitives:",
        "formal programme lists psi, Gamma, chi, tau, and memory primitives.",
    ),
    "SRC4071_05_spine": (
        FORMALIZATION / "07-unification-spine.md",
        "a motion/curvature-memory field theory",
        "spine frames MTS as motion/curvature-memory field theory.",
    ),
    "SRC4071_06_flow_framework": (
        PROJECT / "core-mts-framework" / "field-theory" / "geometric-field-framework.md",
        "shock-limited flow",
        "core framework contains flow and rotational attenuation clues.",
    ),
    "SRC4071_07_pgf_memory": (
        PROJECT / "core-mts-framework" / "field-theory" / "motion-timespace-research.md",
        "imperfect persistence or memory of the flow",
        "PGF draft connects memory and flow.",
    ),
    "SRC4071_08_no_absolute_frame": (
        PROJECT / "core-mts-framework" / "relativity" / "mbt-special-relativity-a-respectful-extension-of-einstein.md",
        "No Absolute Reference Frame",
        "relativity draft motivates frame covariance, but not yet local gauge ownership.",
    ),
    "SRC4071_09_owner_connection": (
        FORMALIZATION / "141-doubled-owner-connection-current-primitive.md",
        "independent_owner_connection",
        "older route identifies owner connection as useful but not projected.",
    ),
    "SRC4071_10_solder_obstruction": (
        FORMALIZATION / "142-owner-spacetime-solder-map-theorem.md",
        "owner_spacetime_solder_map_bulk_hybrid_fails_boundary_topological_backup_open",
        "older route warns that solder/projection is the obstruction.",
    ),
    "SRC4071_11_coframe_descent": (
        ROOT / "1003-Y5-R10-Bref-covariant-frame-theorem-or-Delta-ref-frame-profile-row.md",
        "CFA1003_1_quotient_coframe_descent",
        "coframe descent exists as a conditional theorem only.",
    ),
    "SRC4071_12_observed_flow": (
        SOURCE_DIR / "P8_local_GR_observed_flow_stationary_branch_status.csv",
        "STAT3538_0_flow",
        "observed flow/coframe is conditional same-stack owner.",
    ),
    "SRC4071_13_memory_double_zero": (
        SOURCE_DIR / "P8_DOUBLE_ZERO_MEMORY_ORIGIN_ATTEMPT.csv",
        "O3_determinant_current_candidate",
        "memory/current determinant route is a clue, not parent-owned.",
    ),
}

OUTPUTS = {
    "source_register": SOURCE_DIR / "P8_Y5_R2FR_4071_SOURCE_REGISTER.csv",
    "motion_frame_gauge": SOURCE_DIR / "P8_Y5_R2FR_4071_LOCAL_MOTION_FRAME_GAUGE_TEST.csv",
    "origin_theorem": SOURCE_DIR / "P8_Y5_R2FR_4071_CARTAN_ORIGIN_THEOREM_ATTEMPT.csv",
    "mts_uplift_map": SOURCE_DIR / "P8_Y5_R2FR_4071_MTS_TO_CARTAN_UPLIFT_MAP.csv",
    "demotion_tests": SOURCE_DIR / "P8_Y5_R2FR_4071_IMPORT_OR_DERIVATION_DEMOTION_TESTS.csv",
    "decision_gate": SOURCE_DIR / "P8_Y5_R2FR_4071_DECISION_GATE.csv",
    "claim_gate": SOURCE_DIR / "P8_Y5_R2FR_4071_CLAIM_GATE.csv",
    "next_target": SOURCE_DIR / "P8_Y5_R2FR_4071_NEXT_TARGET.csv",
    "status": SOURCE_DIR / "P8_Y5_R2FR_4071_STATUS.csv",
    "validation": SOURCE_DIR / "P8_Y5_BRR545_4071_VALIDATION.csv",
}


def timestamp() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def read_text(path: Path) -> str:
    if not path.exists():
        return ""
    return path.read_text(encoding="utf-8", errors="replace")


def write_csv(path: Path, rows: List[Dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        raise ValueError(f"no rows supplied for {path}")
    with path.open("w", newline="", encoding="utf-8") as output_file:
        writer = csv.DictWriter(output_file, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def source_rows(current_timestamp: str) -> List[Dict[str, object]]:
    rows: List[Dict[str, object]] = []
    for source_id, source_tuple in SOURCES.items():
        path, needle, role = source_tuple
        text = read_text(path)
        rows.append(
            {
                "source_id": source_id,
                "path": str(path),
                "exists": path.exists(),
                "needle": needle,
                "needle_found": needle in text,
                "role": role,
                "timestamp_utc": current_timestamp,
            }
        )
    return rows


def motion_frame_gauge_rows(current_timestamp: str) -> List[Dict[str, object]]:
    return [
        {
            "test_id": "MFG4071_0_global_frame",
            "principle": "global internal Lorentz/Poincare relabelling of the psi packet",
            "calculation": "constant Lambda and constant a leave dX^A covariant enough for special-relativistic tangent physics",
            "result": "INSUFFICIENT_FOR_GR",
            "derived_field": "none",
            "meaning": "global no-absolute-frame language does not by itself force curved spacetime infrastructure",
            "timestamp_utc": current_timestamp,
        },
        {
            "test_id": "MFG4071_1_local_lorentz",
            "principle": "local internal Lorentz freedom X^A -> Lambda^A_B(x) X^B",
            "calculation": "dX'^A = Lambda^A_B dX^B + dLambda^A_B X^B, so a compensating omega^A_B is required",
            "result": "FORCES_OMEGA_CONDITIONALLY",
            "derived_field": "omega^AB spin/motion-frame connection",
            "meaning": "if MTS owns local motion-frame rotations/boosts, omega is not optional decoration",
            "timestamp_utc": current_timestamp,
        },
        {
            "test_id": "MFG4071_2_local_translation",
            "principle": "local internal motion-origin freedom X^A -> X^A + a^A(x)",
            "calculation": "D X'^A = D X^A + D a^A, so B^A must transform as B^A -> B^A - D a^A to keep e^A = D X^A + B^A covariant",
            "result": "FORCES_B_CONDITIONALLY",
            "derived_field": "B^A translational/solder connection",
            "meaning": "if MTS owns local freedom to reset motion origins, B^A is the required compensator",
            "timestamp_utc": current_timestamp,
        },
        {
            "test_id": "MFG4071_3_unitary_gauge",
            "principle": "translation gauge can set X^A=0 locally",
            "calculation": "in unitary gauge e^A = B^A; without B^A the coframe vanishes or collapses to the flat exact-gradient branch",
            "result": "B_IS_PHYSICAL_SOLDER_IN_GAUGE_FIXED_BRANCH",
            "derived_field": "B^A as observed coframe carrier",
            "meaning": "the psi packet is Stueckelberg-like; the solder connection carries the physical local geometry",
            "timestamp_utc": current_timestamp,
        },
        {
            "test_id": "MFG4071_4_field_strengths",
            "principle": "nonintegrable motion-frame transport produces Cartan field strengths",
            "calculation": "T^A = D e^A = D B^A + R^A_B X^B and R^AB = d omega^AB + omega^A_C wedge omega^CB",
            "result": "CURVATURE_MEMORY_CAN_BE_CARTAN_HOLONOMY_IF_UPLIFTED",
            "derived_field": "T^A torsion/motion-closure defect and R^AB curvature/boost-rotation holonomy",
            "meaning": "Gamma/memory scalars can be invariants of Cartan field strengths, but cannot replace the full connection",
            "timestamp_utc": current_timestamp,
        },
    ]


def origin_theorem_rows(current_timestamp: str) -> List[Dict[str, object]]:
    return [
        {
            "theorem_id": "ORG4071_0_gauge_compensator",
            "statement": "If the MTS parent is invariant under local internal motion-frame Lorentz transformations and local motion-origin translations, then omega^AB and B^A are forced as gauge compensators and e^A = D_omega X^A + B^A is the covariant solder coframe.",
            "proof_sketch": "The derivative of local frame transformations generates dLambda and Da terms. A spin connection cancels dLambda; a translational connection cancels Da. The combination e^A transforms covariantly, and g_obs=eta_AB e^A e^B is invariant.",
            "status": "EXACT_CONDITIONAL_THEOREM",
            "current_MTS_status": "MTS_HAS_FLOW_MEMORY_AND_FRAME_CLUES_NOT_PARENT_SIGNED_LOCAL_POINCARE_GAUGE",
            "claim_effect": "Cartan fields are conditionally derivable from a symmetry principle, but not yet derived from current corpus alone",
            "valid_for_claim": False,
            "timestamp_utc": current_timestamp,
        },
        {
            "theorem_id": "ORG4071_1_no_import_test",
            "statement": "B^A and omega^AB are not imported GR infrastructure only if they are the connection components of the MTS motion-frame principal bundle and their action/field strengths are in S_parent before local-GR readout.",
            "proof_sketch": "A field introduced after demanding EH is a closure input. A field forced by parent symmetry and varied in the parent action is a derived infrastructure field.",
            "status": "DERIVATION_VS_IMPORT_CRITERION",
            "current_MTS_status": "CRITERION_WRITTEN_NOT_PASSED",
            "claim_effect": "4072 must either sign the symmetry/action or demote Cartan coframe to effective branch",
            "valid_for_claim": False,
            "timestamp_utc": current_timestamp,
        },
        {
            "theorem_id": "ORG4071_2_memory_uplift",
            "statement": "Scalar curvature-memory variables can be retained as invariants/projections of Cartan curvature or torsion, not as substitutes for the full connection.",
            "proof_sketch": "A scalar Gamma can encode traces, norms, or branch functionals of R^AB/T^A, but a scalar does not contain six Lorentz connection components plus four translational solder components.",
            "status": "UPLIFT_RULE_CONSTRUCTED",
            "current_MTS_status": "GAMMA_SCALAR_OVERLOADED_AND_NOT_CONNECTION_VALUED",
            "claim_effect": "prevents pretending Gamma_mem alone owns omega/B",
            "valid_for_claim": False,
            "timestamp_utc": current_timestamp,
        },
        {
            "theorem_id": "ORG4071_3_local_GR_route",
            "statement": "If ORG4071_0 is parent-signed and the 4070 torsion/nonmetricity gates close, the psi-packet route becomes a genuine candidate for MTS-to-EH rather than an adopted GR branch.",
            "proof_sketch": "The parent symmetry forces the coframe/connection, the Cartan action supplies EH after torsion resolution, and 4063 supplies the weak-field Newton/PPN readout.",
            "status": "PROMOTION_ROUTE_CONDITIONAL",
            "current_MTS_status": "OPEN",
            "claim_effect": "best next route, but no local-GR claim",
            "valid_for_claim": False,
            "timestamp_utc": current_timestamp,
        },
    ]


def mts_uplift_rows(current_timestamp: str) -> List[Dict[str, object]]:
    return [
        {
            "map_id": "UP4071_0_psi",
            "MTS_object": "psi / Psi packet",
            "Cartan_object": "X^A = L_* Psi^A Stueckelberg motion coordinates",
            "map_status": "CANONICAL_REPAIR_CANDIDATE",
            "must_prove": "rank-four packet, normalization L_*, and local motion-frame transformation law",
            "not_enough": "literal lone scalar psi",
            "timestamp_utc": current_timestamp,
        },
        {
            "map_id": "UP4071_1_flow",
            "MTS_object": "motion flow / transport / local exchange",
            "Cartan_object": "B^A translational solder one-form",
            "map_status": "BEST_ORIGIN_CANDIDATE_NOT_PARENT_SIGNED",
            "must_prove": "flow one-form transforms as B^A -> B^A - D a^A and appears in S_parent with variation",
            "not_enough": "post-readout coframe notation or fitted observer frame",
            "timestamp_utc": current_timestamp,
        },
        {
            "map_id": "UP4071_2_memory",
            "MTS_object": "Gamma_mem / curvature-memory / rotational attenuation",
            "Cartan_object": "invariants or components of R^AB[omega] and possibly T^A",
            "map_status": "SCALAR_TO_CONNECTION_UPLIFT_REQUIRED",
            "must_prove": "Gamma scalars are derived contractions/projections of a Lorentz-valued connection curvature",
            "not_enough": "single scalar Gamma as full owner of omega^AB",
            "timestamp_utc": current_timestamp,
        },
        {
            "map_id": "UP4071_3_time",
            "MTS_object": "tau / clock exchange",
            "Cartan_object": "timelike coframe leg e^0 and clock normalization",
            "map_status": "PARTIAL_COMPATIBILITY_ROUTE",
            "must_prove": "tau is the same descended coframe/clock branch used by matter, EM, and PPN readout",
            "not_enough": "independent time-flow scalar with separate matter frame",
            "timestamp_utc": current_timestamp,
        },
        {
            "map_id": "UP4071_4_chi_Qcoh",
            "MTS_object": "chi / Qcoh / transport response",
            "Cartan_object": "deformation, stationary-flow, or residual response built from e^A/omega",
            "map_status": "DOWNSTREAM_NOT_FUNDAMENTAL_GEOMETRY_OWNER",
            "must_prove": "response fields are q-basic/readout or vertical/silent in local branch",
            "not_enough": "using response fields to define geometry after fitting",
            "timestamp_utc": current_timestamp,
        },
    ]


def demotion_test_rows(current_timestamp: str) -> List[Dict[str, object]]:
    return [
        {
            "test_id": "DEM4071_0_symmetry",
            "test": "Does S_parent declare local internal motion-frame Lorentz + translation symmetry?",
            "pass_result": "B^A and omega^AB are symmetry-forced compensators",
            "fail_result": "Cartan coframe is imported effective-GR infrastructure",
            "current_status": "NOT_PARENT_SIGNED",
            "timestamp_utc": current_timestamp,
        },
        {
            "test_id": "DEM4071_1_action",
            "test": "Do B^A and omega^AB appear in the parent action before EH readout, with variations and field strengths?",
            "pass_result": "connection/coframe are parent fields",
            "fail_result": "they are closure inputs",
            "current_status": "NOT_PARENT_SIGNED",
            "timestamp_utc": current_timestamp,
        },
        {
            "test_id": "DEM4071_2_memory",
            "test": "Is Gamma_mem an invariant/projection of R^AB/T^A rather than a scalar replacing the connection?",
            "pass_result": "memory becomes Cartan holonomy/readout",
            "fail_result": "Gamma cannot own the solder route",
            "current_status": "UPLIFT_REQUIRED",
            "timestamp_utc": current_timestamp,
        },
        {
            "test_id": "DEM4071_3_torsion",
            "test": "Are torsion and nonmetricity zero, constrained, heavy, or empirically bounded?",
            "pass_result": "EH/local PPN branch can inherit 4070 route",
            "fail_result": "torsion/preferred-frame residual vector remains live",
            "current_status": "OPEN_GATE",
            "timestamp_utc": current_timestamp,
        },
        {
            "test_id": "DEM4071_4_same_coframe",
            "test": "Do matter, EM, clocks, source masses, and readouts use the same descended coframe?",
            "pass_result": "source coupling can remain universal",
            "fail_result": "frame/source residuals must be scored",
            "current_status": "CONDITIONAL_ONLY",
            "timestamp_utc": current_timestamp,
        },
    ]


def static_rows(current_timestamp: str) -> Dict[str, List[Dict[str, object]]]:
    return {
        "decision_gate": [
            {
                "decision_id": "DEC4071_0",
                "decision": DECISION,
                "summary": "4071 proves that local motion-frame gauge symmetry would force omega^AB and B^A as compensators, but current MTS sources contain flow/memory/frame clues rather than a parent-signed local Poincare/motion-frame gauge action.",
                "formalization_modified": False,
                "public_claim": False,
                "github_action": False,
                "timestamp_utc": current_timestamp,
            },
            {
                "decision_id": "DEC4071_1",
                "decision": "BEST_ROUTE_IS_LOCAL_MOTION_FRAME_GAUGE_ACTION",
                "summary": "The next work should write the actual MTS local motion-frame gauge action and decide whether B^A/omega^AB are parent-owned or demoted.",
                "formalization_modified": False,
                "public_claim": False,
                "github_action": False,
                "timestamp_utc": current_timestamp,
            },
        ],
        "claim_gate": [
            {
                "claim_id": "CLAIM4071_0",
                "claim": "MTS currently derives B^A and omega^AB from existing scalar flow/memory variables",
                "allowed_private": False,
                "allowed_public": False,
                "reason": "current corpus has clues but no parent-signed local motion-frame gauge symmetry/action",
                "timestamp_utc": current_timestamp,
            },
            {
                "claim_id": "CLAIM4071_1",
                "claim": "local motion-frame gauge symmetry would force Cartan compensators",
                "allowed_private": True,
                "allowed_public": False,
                "reason": "exact conditional gauge-compensator theorem; parent premise still unsigned",
                "timestamp_utc": current_timestamp,
            },
            {
                "claim_id": "CLAIM4071_2",
                "claim": "Gamma_mem scalar alone owns the full Cartan connection",
                "allowed_private": False,
                "allowed_public": False,
                "reason": "a scalar can be an invariant/projection, not the full Lorentz/translational connection",
                "timestamp_utc": current_timestamp,
            },
            {
                "claim_id": "CLAIM4071_3",
                "claim": "MTS has completed the local GR/Newton/PPN derivation",
                "allowed_private": False,
                "allowed_public": False,
                "reason": "motion-frame gauge action, torsion/nonmetricity gates, and same-coframe matter ownership remain open",
                "timestamp_utc": current_timestamp,
            },
        ],
        "next_target": [
            {
                "row_id": "NEXT4071_0",
                "next_doc": "4072-Y5-R2FR-local-motion-frame-gauge-action-or-effective-GR-demotion.md",
                "next_script": "scripts/Y5_R2FR_4072_local_motion_frame_gauge_action_or_effective_GR_demotion.py",
                "reason": "write the parent local motion-frame gauge action with X^A, B^A, omega^AB, R^AB, T^A, matter/EM coupling, and torsion gates; if the action cannot be sourced from MTS primitives, demote Cartan coframe to an effective-GR branch input",
                "timestamp_utc": current_timestamp,
            }
        ],
        "status": [
            {
                "status_id": "STAT4071",
                "status": DECISION,
                "formalization_modified": False,
                "public_claim": False,
                "github_action": False,
                "timestamp_utc": current_timestamp,
            }
        ],
    }


def validate_sources(source_table: List[Dict[str, object]]) -> Tuple[bool, str]:
    missing = [row["source_id"] for row in source_table if not row["exists"]]
    absent_needles = [row["source_id"] for row in source_table if not row["needle_found"]]
    if missing or absent_needles:
        return False, f"missing={missing}; absent_needles={absent_needles}"
    return True, "all cited source paths exist and needles are present"


def validate_csv_parse(paths: Iterable[Path]) -> Tuple[bool, str]:
    details: List[str] = []
    try:
        for path in paths:
            with path.open(newline="", encoding="utf-8") as input_file:
                parsed_rows = list(csv.DictReader(input_file))
            details.append(f"{path.name}:rows={len(parsed_rows)}")
    except Exception as exc:  # pragma: no cover
        return False, repr(exc)
    return True, "; ".join(details)


def validate_no_public_claim(row_groups: Iterable[List[Dict[str, object]]]) -> Tuple[bool, str]:
    offenders: List[str] = []
    for rows in row_groups:
        for row in rows:
            for key in ("valid_for_claim", "allowed_public", "public_claim", "github_action"):
                if key in row and str(row[key]).lower() == "true":
                    offenders.append(str(row))
    if offenders:
        return False, f"public/github claim flags found: {offenders}"
    return True, "all claim-bearing rows preserve public/github false"


def validate_script_compile() -> Tuple[bool, str]:
    try:
        py_compile.compile(str(SCRIPT_PATH), doraise=True)
    except py_compile.PyCompileError as exc:
        return False, str(exc)
    return True, "script compiles"


def validation_rows(
    source_table: List[Dict[str, object]],
    generated_csvs: List[Path],
    row_groups: List[List[Dict[str, object]]],
) -> List[Dict[str, object]]:
    source_ok, source_detail = validate_sources(source_table)
    csv_ok, csv_detail = validate_csv_parse(generated_csvs)
    claims_ok, claims_detail = validate_no_public_claim(row_groups)
    compile_ok, compile_detail = validate_script_compile()
    joined = str(row_groups)
    return [
        {"check_id": "VAL4071_00_sources", "passed": source_ok, "detail": source_detail},
        {"check_id": "VAL4071_01_csv_parse", "passed": csv_ok, "detail": csv_detail},
        {"check_id": "VAL4071_02_no_public_or_github_claim", "passed": claims_ok, "detail": claims_detail},
        {
            "check_id": "VAL4071_03_forces_compensators",
            "passed": "FORCES_OMEGA_CONDITIONALLY" in joined and "FORCES_B_CONDITIONALLY" in joined,
            "detail": "local motion-frame gauge tests force omega and B conditionally",
        },
        {
            "check_id": "VAL4071_04_current_status_unsigned",
            "passed": "NOT_PARENT_SIGNED" in joined and "EXACT_CONDITIONAL_THEOREM" in joined,
            "detail": "the theorem is exact-conditional but current MTS parent signature is unsigned",
        },
        {
            "check_id": "VAL4071_05_gamma_uplift",
            "passed": "SCALAR_TO_CONNECTION_UPLIFT_REQUIRED" in joined,
            "detail": "Gamma/memory scalar uplift to Cartan invariants is required",
        },
        {
            "check_id": "VAL4071_06_next_target",
            "passed": "4072-Y5-R2FR-local-motion-frame-gauge-action-or-effective-GR-demotion.md" in joined,
            "detail": "next target writes or demotes the local motion-frame gauge action",
        },
        {"check_id": "VAL4071_07_script_compiles", "passed": compile_ok, "detail": compile_detail},
    ]


def doc_text(current_timestamp: str) -> str:
    return f"""# 4071 - Cartan Solder Field Origin From MTS Flow Or Demotion

- Timestamp: `{current_timestamp}`
- Status: `private_nonclaim_checkpoint`
- Decision: `{DECISION}`
- Public GR/Newton/PPN claim: `false`
- GitHub action: `false`

## What 4071 Proves

4071 gives the exact conditional origin theorem for the Cartan fields:

```text
If MTS owns local internal motion-frame symmetry,
X^A -> Lambda^A_B(x) X^B + a^A(x),
then dX^A is not covariant by itself.
```

The `dLambda` term forces a spin/motion-frame connection `omega^AB`.
The `Da^A` term forces a translational/solder connection `B^A`.

So the covariant coframe is:

```text
e^A = D_omega X^A + B^A
g_obs = eta_AB e^A e^B.
```

This is not a vibe. It is the standard compensator logic: if the local symmetry is real, the fields are forced.

## What Is Still Not Proven

The current MTS corpus contains strong clues:

- motion/flow language;
- curvature-memory language;
- no-absolute-frame language;
- observer/coframe and same-source gates.

But it does **not** yet parent-sign a local motion-frame gauge action. That means:

```text
B^A and omega^AB are conditionally forced,
but not yet MTS-derived from the existing corpus.
```

## How MTS Could Own Them

The best mapping is:

```text
Psi^A      -> X^A = L_* Psi^A
flow       -> B^A translational solder one-form
Gamma_mem  -> invariants/projections of R^AB[omega] and T^A
tau        -> timelike coframe/clock normalization
chi/Qcoh   -> downstream transport/readout response
```

The big warning is that `Gamma_mem` as a scalar cannot own the full connection. It can only be an invariant, projection, or scalar branch of the Cartan field strengths.

## Decision

Do not demote the whole GR route yet. Demote only the claim that current scalar flow/memory variables already derive the Cartan fields.

The next step is to write the actual local motion-frame gauge action. If that action can be tied to MTS primitives, the GR bridge is alive. If not, the Cartan coframe becomes an effective-GR branch input.

## Next

`4072` should build `local-motion-frame-gauge-action-or-effective-GR-demotion`.
"""


def main() -> None:
    current_timestamp = timestamp()
    SOURCE_DIR.mkdir(parents=True, exist_ok=True)

    sources = source_rows(current_timestamp)
    motion_frame_gauge = motion_frame_gauge_rows(current_timestamp)
    origin_theorem = origin_theorem_rows(current_timestamp)
    mts_uplift = mts_uplift_rows(current_timestamp)
    demotion_tests = demotion_test_rows(current_timestamp)
    static = static_rows(current_timestamp)

    DOC_PATH.write_text(doc_text(current_timestamp), encoding="utf-8")
    write_csv(OUTPUTS["source_register"], sources)
    write_csv(OUTPUTS["motion_frame_gauge"], motion_frame_gauge)
    write_csv(OUTPUTS["origin_theorem"], origin_theorem)
    write_csv(OUTPUTS["mts_uplift_map"], mts_uplift)
    write_csv(OUTPUTS["demotion_tests"], demotion_tests)
    write_csv(OUTPUTS["decision_gate"], static["decision_gate"])
    write_csv(OUTPUTS["claim_gate"], static["claim_gate"])
    write_csv(OUTPUTS["next_target"], static["next_target"])
    write_csv(OUTPUTS["status"], static["status"])

    generated_csvs = [
        OUTPUTS["source_register"],
        OUTPUTS["motion_frame_gauge"],
        OUTPUTS["origin_theorem"],
        OUTPUTS["mts_uplift_map"],
        OUTPUTS["demotion_tests"],
        OUTPUTS["decision_gate"],
        OUTPUTS["claim_gate"],
        OUTPUTS["next_target"],
        OUTPUTS["status"],
    ]
    row_groups = [
        sources,
        motion_frame_gauge,
        origin_theorem,
        mts_uplift,
        demotion_tests,
        static["decision_gate"],
        static["claim_gate"],
        static["next_target"],
        static["status"],
    ]
    validation = validation_rows(sources, generated_csvs, row_groups)
    write_csv(OUTPUTS["validation"], validation)

    cache_dir = SCRIPT_PATH.parent / "__pycache__"
    if cache_dir.exists():
        shutil.rmtree(cache_dir)

    failures = [row for row in validation if not row["passed"]]
    print(f"wrote {DOC_PATH}")
    print(f"decision: {DECISION}")
    print(f"validation rows: {len(validation)}")
    print(f"validation failures: {len(failures)}")
    for failure in failures:
        print(f"FAIL {failure['check_id']}: {failure['detail']}")


if __name__ == "__main__":
    main()

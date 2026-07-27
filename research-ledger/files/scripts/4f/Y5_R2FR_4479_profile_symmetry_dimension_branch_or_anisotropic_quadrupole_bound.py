from __future__ import annotations

import shutil
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List, Mapping, Sequence


SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

from profile_symmetry_dimension_gate import (  # noqa: E402
    anisotropy_bound_rows,
    claim_gate_rows,
    decision_rows as gate_decision_rows,
    local_spatial_symmetry_rows,
    read_csv,
    shape_branch_input_rows,
    write_csv,
)


ROOT = Path(__file__).resolve().parents[2]
FORMAL = ROOT / "formalization-workbench"
POST = ROOT / "post-checkpoint-work"
SOURCE_DIR = POST / "source-intake" / "mts_residuals"

CHECKPOINT = "4479"
CLAIM_ID = "L-321"
MARKER = "PPC4161_PROFILE_SYMMETRY_DIMENSION_BRANCH_OR_ANISOTROPIC_QUADRUPOLE_BOUND_4479"
PACKET_MARKER = "PPC4161_PACKET_PROFILE_SYMMETRY_DIMENSION_BRANCH_OR_ANISOTROPIC_QUADRUPOLE_BOUND_4479"
DECISION = "SPATIAL_SYMMETRY_BRANCH_PARENT_UNSIGNED_TEMPORAL_DIPOLE_QUADRUPOLE_BOUNDS_DERIVED_NONCLAIM"
NEXT_TARGET = "4480-Y5-R2FR-orientation-carrier-zero-proof-or-quadrupole-residual-scorer.md"

FORMAL_PATH = FORMAL / "495-PPC4161-profile-symmetry-dimension-branch-or-anisotropic-quadrupole-bound.md"
DOC_PATH = POST / "4479-Y5-R2FR-profile-symmetry-dimension-branch-or-anisotropic-quadrupole-bound.md"
VALIDATION_PATH = SOURCE_DIR / "P8_Y5_BRR545_4479_VALIDATION.csv"
SPINE_PATH = FORMAL / "07-unification-spine.md"
PACKET_PATH = FORMAL / "180-PPC4161-private-local-packet-integration.md"
CLAIMS_PATH = FORMAL / "02-claims-register.csv"

SOURCE_REGISTER = SOURCE_DIR / "P8_Y5_R2FR_4479_SOURCE_REGISTER.csv"
THEOREM_CSV = SOURCE_DIR / "P8_Y5_R2FR_4479_LOCAL_SPATIAL_SYMMETRY_THEOREM.csv"
BOUNDS_CSV = SOURCE_DIR / "P8_Y5_R2FR_4479_ANISOTROPY_BOUND_ROWS.csv"
INPUTS_CSV = SOURCE_DIR / "P8_Y5_R2FR_4479_SHAPE_BRANCH_INPUT_ROWS.csv"
DECISION_LEDGER_CSV = SOURCE_DIR / "P8_Y5_R2FR_4479_DECISION_LEDGER.csv"
CLAIM_GATES_CSV = SOURCE_DIR / "P8_Y5_R2FR_4479_CLAIM_GATES.csv"
DECISION_CSV = SOURCE_DIR / "P8_Y5_R2FR_4479_DECISION.csv"
STATUS_CSV = SOURCE_DIR / "P8_Y5_R2FR_4479_STATUS.csv"
NEXT_CSV = SOURCE_DIR / "P8_Y5_R2FR_4479_NEXT_TARGET.csv"

GATE_PATH = SCRIPT_DIR / "profile_symmetry_dimension_gate.py"
GENERATOR_PATH = SCRIPT_DIR / "Y5_R2FR_4479_profile_symmetry_dimension_branch_or_anisotropic_quadrupole_bound.py"
STAMP = datetime.now(timezone.utc).replace(microsecond=0).isoformat()

FORMAL_494 = FORMAL / "494-PPC4161-marker-profile-support-zero-certificate-or-first-moment-input-row.md"
NEXT_4478 = SOURCE_DIR / "P8_Y5_R2FR_4478_NEXT_TARGET.csv"
SUPPORT_4478 = SOURCE_DIR / "P8_Y5_R2FR_4478_SUPPORT_ZERO_CERTIFICATE.csv"
LAWS_4478 = SOURCE_DIR / "P8_Y5_R2FR_4478_FIRST_MOMENT_INPUT_LAWS.csv"
INPUTS_4478 = SOURCE_DIR / "P8_Y5_R2FR_4478_FIRST_MOMENT_INPUT_ROWS.csv"
GATES_4478 = SOURCE_DIR / "P8_Y5_R2FR_4478_CLAIM_GATES.csv"


def text(path: Path) -> str:
    if not path.exists():
        return ""
    return path.read_text(encoding="utf-8", errors="ignore")


def write_text(path: Path, body: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(body, encoding="utf-8")


def line_of(path: Path, needle: str) -> int:
    if not path.exists() or not needle:
        return 0
    for line_number, line in enumerate(text(path).splitlines(), start=1):
        if needle in line:
            return line_number
    return 0


def md(value: object) -> str:
    return str(value).replace("\n", " ").replace("|", "\\|")


def table(rows: Sequence[Mapping[str, object]]) -> str:
    if not rows:
        return ""
    headers = list(rows[0].keys())
    output = ["| " + " | ".join(headers) + " |", "| " + " | ".join("---" for _ in headers) + " |"]
    for row in rows:
        output.append("| " + " | ".join(md(row.get(header, "")) for header in headers) + " |")
    return "\n".join(output)


def source_specs() -> List[Dict[str, object]]:
    return [
        {
            "source_id": "SRC4479_00_next4478",
            "ref": NEXT_4478,
            "needle": "4479-Y5-R2FR-profile-symmetry-dimension-branch-or-anisotropic-quadrupole-bound.md",
            "role": "4478 selected profile symmetry/dimension branch or anisotropic quadrupole bound.",
        },
        {
            "source_id": "SRC4479_01_formal494_deff",
            "ref": FORMAL_494,
            "needle": "The local support branch is conditionally `d_eff=3`",
            "role": "formal 4478 local d_eff branch.",
        },
        {
            "source_id": "SRC4479_02_formal494_quadrupole",
            "ref": FORMAL_494,
            "needle": "Q_M_TF^{ij}",
            "role": "formal 4478 anisotropic quadrupole row.",
        },
        {
            "source_id": "SRC4479_03_support4478_verdict",
            "ref": SUPPORT_4478,
            "needle": "SZC4478_5_verdict",
            "role": "4478 support zero verdict.",
        },
        {
            "source_id": "SRC4479_04_laws4478_deff",
            "ref": LAWS_4478,
            "needle": "MIL4478_2_support_dimension_branch",
            "role": "4478 local spatial support dimension law.",
        },
        {
            "source_id": "SRC4479_05_laws4478_centering",
            "ref": LAWS_4478,
            "needle": "MIL4478_4_centering_choice",
            "role": "4478 centering/dipole law.",
        },
        {
            "source_id": "SRC4479_06_laws4478_quadrupole",
            "ref": LAWS_4478,
            "needle": "MIL4478_5_isotropy_or_quadrupole",
            "role": "4478 isotropy/quadrupole law.",
        },
        {
            "source_id": "SRC4479_07_inputs4478_deff",
            "ref": INPUTS_4478,
            "needle": "FMI4478_2_d_eff",
            "role": "4478 d_eff input row.",
        },
        {
            "source_id": "SRC4479_08_inputs4478_dipole",
            "ref": INPUTS_4478,
            "needle": "FMI4478_5_dipole_or_centering",
            "role": "4478 dipole input row.",
        },
        {
            "source_id": "SRC4479_09_inputs4478_quad",
            "ref": INPUTS_4478,
            "needle": "FMI4478_6_quadrupole_TF",
            "role": "4478 quadrupole input row.",
        },
        {
            "source_id": "SRC4479_10_gates4478_support",
            "ref": GATES_4478,
            "needle": "CG4478_2_support_zero_parent_signed",
            "role": "4478 gate blocking support-zero overclaim.",
        },
        {
            "source_id": "SRC4479_11_gate",
            "ref": GATE_PATH,
            "needle": "def local_spatial_symmetry_rows",
            "role": "4479 profile symmetry/dimension gate.",
        },
        {
            "source_id": "SRC4479_12_generator",
            "ref": GENERATOR_PATH,
            "needle": 'CHECKPOINT = "4479"',
            "role": "4479 generator script.",
        },
    ]


def source_rows() -> List[Dict[str, object]]:
    rows: List[Dict[str, object]] = []
    for spec in source_specs():
        source_path = Path(spec["ref"])
        needle = str(spec["needle"])
        line_number = line_of(source_path, needle)
        rows.append(
            {
                "checkpoint": CHECKPOINT,
                "source_id": spec["source_id"],
                "source_kind": "local",
                "source_ref": str(source_path),
                "local_path_exists": source_path.exists(),
                "needle": needle,
                "needle_found": line_number > 0,
                "line_number": line_number,
                "role": spec["role"],
                "valid_for_claim": False,
            }
        )
    return rows


def decision_rows() -> List[Dict[str, object]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "marker": MARKER,
            "claim_id": CLAIM_ID,
            "decision": DECISION,
            "proof_result": "conditional d_eff=3, centering and isotropy branch written but not parent-signed",
            "fallback_result": "temporal-smearing, dipole and tracefree quadrupole residual bounds derived and staged",
            "claim_status": "private_nonclaim",
            "next_target": NEXT_TARGET,
            "valid_for_claim": False,
            "generated_utc": STAMP,
        }
    ]


def status_rows() -> List[Dict[str, object]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "marker": MARKER,
            "claim_id": CLAIM_ID,
            "decision": DECISION,
            "spatial_symmetry_branch": "written_parent_unsigned",
            "anisotropy_bounds": "derived",
            "sharpest_open_clause": "orientation_carrier_zero_or_quadrupole_residual_scorer",
            "shape_input_status": "staged_missing_values",
            "public_local_GR_claim": False,
            "next_target": NEXT_TARGET,
            "valid_for_claim": False,
            "generated_utc": STAMP,
        }
    ]


def next_rows() -> List[Dict[str, object]]:
    return [
        {
            "next_id": "NT4479_0",
            "target": NEXT_TARGET,
            "objective": "Prove no orientation/nematic/tidal carrier can source Q_M_TF, or build the quadrupole residual scorer.",
            "derive_first": "show the parent support alphabet has no vector, spin-axis, tidal, boundary-normal or nematic carrier",
            "fallback": "score Q_M_TF through R_quad into PPN, clock anisotropy and orbital precession gates",
            "risk": "assuming isotropy from scalar notation while an orientation carrier survives",
            "valid_for_claim": False,
        }
    ]


def append_section_once(path: Path, marker: str, title: str, body: str) -> None:
    current = text(path)
    if marker in current:
        return
    addition = f"\n\n## {title}\n\nMarker: `{marker}`  \n{body}\n"
    write_text(path, current.rstrip() + addition + "\n")


def update_claims_register() -> None:
    rows = read_csv(CLAIMS_PATH)
    if any(row.get("claim_id") == CLAIM_ID for row in rows):
        return
    rows.append(
        {
            "claim_id": CLAIM_ID,
            "domain": "local_gr_newton_r10_scalar_source_coupling",
            "claim": "4479 writes the conditional local d_eff=3/centering/isotropy branch and derives temporal-smearing, dipole and tracefree-quadrupole residual bounds for finite marker profiles.",
            "current_evidence": "4479 source register, local spatial symmetry theorem, anisotropy bounds, shape branch input rows, claim gates, decision/status/next CSVs and validation.",
            "status": "private_branch_theorem_and_anisotropy_bounds_nonclaim",
            "next_test": NEXT_TARGET,
            "key_risk": "assuming d_eff=3 or isotropy while temporal smearing or an orientation carrier survives.",
            "sector": "local_gr_newton_r10_scalar_source_coupling",
            "evidence": str(FORMAL_PATH),
            "next_action": NEXT_TARGET,
            "risk": "finite anisotropic marker branch remains unscored until orientation carrier or quadrupole inputs close",
        }
    )
    write_csv(CLAIMS_PATH, rows)


def formal_body(
    sources: Sequence[Mapping[str, object]],
    theorem_rows: Sequence[Mapping[str, object]],
    bound_rows: Sequence[Mapping[str, object]],
    input_rows: Sequence[Mapping[str, object]],
    ledger: Sequence[Mapping[str, object]],
    gates: Sequence[Mapping[str, object]],
    decisions: Sequence[Mapping[str, object]],
    statuses: Sequence[Mapping[str, object]],
    next_targets: Sequence[Mapping[str, object]],
) -> str:
    return f"""# 495 PPC4161 - Profile Symmetry Dimension Branch Or Anisotropic Quadrupole Bound

Private checkpoint: `{CHECKPOINT}`  
Marker: `{MARKER}`  
Decision: `{DECISION}`  
Generated UTC: `{STAMP}`

## Result

4479 closes the shape-assumption loophole.

The clean local branch is:

```text
no temporal marker kernel
+ Hamiltonian/local worldtube split
+ positive centred support
+ no orientation/nematic/tidal carrier
=> d_eff=3, D_M^i=0, Q_M_TF^ij=0.
```

Then the moment correction is the spatial one:

```text
C_a^M = lambda_M Q_M*(zeta_a + zeta_grad_a ell_rms^2/(6 L_loc^2))/N_a.
```

But none of those shape clauses are free. If temporal support, non-centering, or anisotropy survives, it becomes an explicit residual:

```text
R_shape_abs = abs(R_time)+abs(R_dip)+abs(R_quad).
```

This keeps the local-GR route honest: isotropy is not smuggled in from scalar notation.

## Local Spatial Symmetry Theorem

{table(theorem_rows)}

## Anisotropy Bound Rows

{table(bound_rows)}

## Shape Branch Input Rows

{table(input_rows)}

## Decision Ledger

{table(ledger)}

## Claim Gates

{table(gates)}

## Status

{table(statuses)}

## Next Target

{table(next_targets)}

## Source Register

{table(sources)}

## Decision Row

{table(decisions)}
"""


def post_body(
    sources: Sequence[Mapping[str, object]],
    theorem_rows: Sequence[Mapping[str, object]],
    bound_rows: Sequence[Mapping[str, object]],
    input_rows: Sequence[Mapping[str, object]],
    ledger: Sequence[Mapping[str, object]],
    gates: Sequence[Mapping[str, object]],
    decisions: Sequence[Mapping[str, object]],
    statuses: Sequence[Mapping[str, object]],
    next_targets: Sequence[Mapping[str, object]],
) -> str:
    return f"""# 4479 Y5/R2FR - Profile Symmetry Dimension Branch Or Anisotropic Quadrupole Bound

Private post-checkpoint mirror for:

`{FORMAL_PATH}`

## What Actually Moved

The `d_eff=3`, centred, isotropic branch is now conditional and explicit. If it does not sign, temporal smearing, dipole and quadrupole residuals are bounded componentwise.

## Spatial Symmetry Branch

{table(theorem_rows)}

## Bounds

{table(bound_rows)}

## Inputs

{table(input_rows)}

## Gates And Decisions

{table(gates)}

{table(ledger)}

{table(decisions)}

## Status And Next Target

{table(statuses)}

{table(next_targets)}

## Sources

{table(sources)}
"""


def validate(
    sources: Sequence[Mapping[str, object]],
    theorem_rows: Sequence[Mapping[str, object]],
    bound_rows: Sequence[Mapping[str, object]],
    input_rows: Sequence[Mapping[str, object]],
    gates: Sequence[Mapping[str, object]],
    decisions: Sequence[Mapping[str, object]],
    statuses: Sequence[Mapping[str, object]],
    next_targets: Sequence[Mapping[str, object]],
    csv_paths: Sequence[Path],
) -> List[Dict[str, object]]:
    validations: List[Dict[str, object]] = []

    def add(check_id: str, passed: bool, detail: str) -> None:
        validations.append(
            {
                "checkpoint": CHECKPOINT,
                "check_id": check_id,
                "passed": passed,
                "detail": detail,
                "valid_for_claim": False,
            }
        )

    add(
        "VAL4479_0_sources_exist_and_needles_found",
        all(row.get("local_path_exists") is True and row.get("needle_found") is True for row in sources),
        "every cited source path exists and its needle is found",
    )
    add(
        "VAL4479_1_spatial_symmetry_theorem_written",
        any(row.get("theorem_id") == "LSS4479_6_verdict" for row in theorem_rows),
        "local spatial/symmetry branch theorem verdict is written",
    )
    add(
        "VAL4479_2_spatial_symmetry_not_overclaimed",
        any(row.get("theorem_id") == "LSS4479_6_verdict" and row.get("parent_signed") is False for row in theorem_rows),
        "clean branch remains parent-unsigned",
    )
    add(
        "VAL4479_3_anisotropy_bounds_written",
        all(
            any(row.get("bound_id") == bound_id for row in bound_rows)
            for bound_id in ["AB4479_0_temporal_kernel", "AB4479_1_dipole", "AB4479_2_quadrupole", "AB4479_4_component_envelope"]
        ),
        "temporal, dipole, quadrupole and envelope bounds are written",
    )
    add(
        "VAL4479_4_shape_input_rows_staged",
        all(
            any(row.get("row_id") == row_id for row in input_rows)
            for row_id in [
                "SBI4479_0_spatial_branch_certificate",
                "SBI4479_1_tau_M",
                "SBI4479_2_centering_certificate",
                "SBI4479_3_orientation_carrier",
                "SBI4479_4_D_M_bound",
                "SBI4479_5_Q_TF_bound",
            ]
        ),
        "shape inputs include spatial branch, temporal width, centering, orientation, dipole and quadrupole",
    )
    add(
        "VAL4479_5_input_rows_remain_nonclaim",
        any("MISSING" in str(row.get("current_value")) for row in input_rows)
        and all(row.get("valid_for_claim") is False for row in input_rows),
        "input rows keep missing source values and valid_for_claim=false",
    )
    add(
        "VAL4479_6_claim_gates_block_local_GR",
        all(str(row.get("claim_allowed")).lower() == "false" for row in gates)
        and any(row.get("gate_id") == "CG4479_2_clean_branch_parent_signed" and str(row.get("gate_pass")).lower() == "false" for row in gates),
        "claim gates block local-GR/R10 promotion until clean branch or bound inputs are sourced",
    )
    add(
        "VAL4479_7_no_generated_claim_rows",
        all(
            str(row.get("valid_for_claim")).lower() == "false"
            for group in [sources, theorem_rows, bound_rows, input_rows, gates, decisions, statuses, next_targets]
            for row in group
        ),
        "all generated rows remain private/nonclaim",
    )
    csv_ok = True
    csv_detail: List[str] = []
    for csv_path in csv_paths:
        try:
            parsed_rows = read_csv(csv_path)
            csv_detail.append(f"{csv_path.name}:{len(parsed_rows)}")
        except Exception as exc:  # pragma: no cover
            csv_ok = False
            csv_detail.append(f"{csv_path.name}:ERROR:{exc}")
    add("VAL4479_8_csvs_parse", csv_ok, "; ".join(csv_detail))
    add("VAL4479_9_docs_written", FORMAL_PATH.exists() and DOC_PATH.exists(), "formal and post checkpoint docs exist")
    add(
        "VAL4479_10_claim_register_updated",
        any(row.get("claim_id") == CLAIM_ID for row in read_csv(CLAIMS_PATH)),
        "claims register contains L-321",
    )
    add(
        "VAL4479_11_spine_and_packet_updated",
        MARKER in text(SPINE_PATH) and PACKET_MARKER in text(PACKET_PATH),
        "unification spine and private packet integration contain 4479 markers",
    )
    add(
        "VAL4479_12_next_target_selected",
        bool(next_targets) and next_targets[0].get("target") == NEXT_TARGET,
        NEXT_TARGET,
    )
    add("VAL4479_13_pycache_removed", not (SCRIPT_DIR / "__pycache__").exists(), "scripts __pycache__ absent after generation")
    return validations


def main() -> None:
    sources = source_rows()
    theorem_rows = local_spatial_symmetry_rows()
    bound_rows = anisotropy_bound_rows()
    input_rows = shape_branch_input_rows()
    ledger = gate_decision_rows(NEXT_TARGET)
    gates = claim_gate_rows(sources, theorem_rows, bound_rows, input_rows)
    decisions = decision_rows()
    statuses = status_rows()
    next_targets = next_rows()

    write_csv(SOURCE_REGISTER, sources)
    write_csv(THEOREM_CSV, theorem_rows)
    write_csv(BOUNDS_CSV, bound_rows)
    write_csv(INPUTS_CSV, input_rows)
    write_csv(DECISION_LEDGER_CSV, ledger)
    write_csv(CLAIM_GATES_CSV, gates)
    write_csv(DECISION_CSV, decisions)
    write_csv(STATUS_CSV, statuses)
    write_csv(NEXT_CSV, next_targets)

    write_text(FORMAL_PATH, formal_body(sources, theorem_rows, bound_rows, input_rows, ledger, gates, decisions, statuses, next_targets))
    write_text(DOC_PATH, post_body(sources, theorem_rows, bound_rows, input_rows, ledger, gates, decisions, statuses, next_targets))
    update_claims_register()

    append_section_once(
        SPINE_PATH,
        MARKER,
        "4479 Profile Symmetry Dimension Branch",
        "4479 makes the shape assumptions explicit: local `d_eff=3`, centering and isotropy require no temporal smearing, centroid-valid support and no orientation/nematic/tidal carrier. If any clause fails, temporal, dipole and quadrupole residuals are bounded componentwise with no cancellation credit.",
    )
    append_section_once(
        PACKET_PATH,
        PACKET_MARKER,
        "4479 Packet Integration",
        "The private packet now carries fallback bounds for temporal smearing, dipole and tracefree quadrupole marker support. The next target is an orientation-carrier zero proof or a quadrupole residual scorer.",
    )

    pycache = SCRIPT_DIR / "__pycache__"
    if pycache.exists():
        shutil.rmtree(pycache)

    csv_paths = [
        SOURCE_REGISTER,
        THEOREM_CSV,
        BOUNDS_CSV,
        INPUTS_CSV,
        DECISION_LEDGER_CSV,
        CLAIM_GATES_CSV,
        DECISION_CSV,
        STATUS_CSV,
        NEXT_CSV,
    ]
    validations = validate(sources, theorem_rows, bound_rows, input_rows, gates, decisions, statuses, next_targets, csv_paths)
    write_csv(VALIDATION_PATH, validations)

    failed = [row for row in validations if str(row.get("passed")).lower() != "true"]
    if failed:
        for row in failed:
            print(f"FAILED {row['check_id']}: {row['detail']}")
        raise SystemExit(1)
    print(f"Generated {CHECKPOINT}: {FORMAL_PATH}")
    print(f"Validation: {VALIDATION_PATH}")


if __name__ == "__main__":
    main()

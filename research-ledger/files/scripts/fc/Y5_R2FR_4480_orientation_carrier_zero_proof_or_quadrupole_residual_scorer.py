from __future__ import annotations

import shutil
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List, Mapping, Sequence


SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

from orientation_carrier_quadrupole_gate import (  # noqa: E402
    claim_gate_rows,
    decision_rows as gate_decision_rows,
    orientation_zero_proof_rows,
    quadrupole_input_rows,
    quadrupole_residual_scorer_rows,
    read_csv,
    write_csv,
)


ROOT = Path(__file__).resolve().parents[2]
FORMAL = ROOT / "formalization-workbench"
POST = ROOT / "post-checkpoint-work"
SOURCE_DIR = POST / "source-intake" / "mts_residuals"

CHECKPOINT = "4480"
CLAIM_ID = "L-322"
MARKER = "PPC4161_ORIENTATION_CARRIER_ZERO_PROOF_OR_QUADRUPOLE_SCORER_4480"
PACKET_MARKER = "PPC4161_PACKET_ORIENTATION_CARRIER_ZERO_PROOF_OR_QUADRUPOLE_SCORER_4480"
DECISION = "ORIENTATION_ZERO_PARENT_UNSIGNED_QUADRUPOLE_SCORER_DERIVED_NONCLAIM"
NEXT_TARGET = "4481-Y5-R2FR-STF-carrier-inventory-source-sweep-or-l2-bound-input-pack.md"

FORMAL_PATH = FORMAL / "496-PPC4161-orientation-carrier-zero-proof-or-quadrupole-residual-scorer.md"
DOC_PATH = POST / "4480-Y5-R2FR-orientation-carrier-zero-proof-or-quadrupole-residual-scorer.md"
VALIDATION_PATH = SOURCE_DIR / "P8_Y5_BRR545_4480_VALIDATION.csv"
SPINE_PATH = FORMAL / "07-unification-spine.md"
PACKET_PATH = FORMAL / "180-PPC4161-private-local-packet-integration.md"
CLAIMS_PATH = FORMAL / "02-claims-register.csv"

SOURCE_REGISTER = SOURCE_DIR / "P8_Y5_R2FR_4480_SOURCE_REGISTER.csv"
ZERO_PROOF_CSV = SOURCE_DIR / "P8_Y5_R2FR_4480_ORIENTATION_ZERO_PROOF.csv"
SCORER_CSV = SOURCE_DIR / "P8_Y5_R2FR_4480_QUADRUPOLE_RESIDUAL_SCORER.csv"
INPUTS_CSV = SOURCE_DIR / "P8_Y5_R2FR_4480_QUADRUPOLE_INPUT_ROWS.csv"
DECISION_LEDGER_CSV = SOURCE_DIR / "P8_Y5_R2FR_4480_DECISION_LEDGER.csv"
CLAIM_GATES_CSV = SOURCE_DIR / "P8_Y5_R2FR_4480_CLAIM_GATES.csv"
DECISION_CSV = SOURCE_DIR / "P8_Y5_R2FR_4480_DECISION.csv"
STATUS_CSV = SOURCE_DIR / "P8_Y5_R2FR_4480_STATUS.csv"
NEXT_CSV = SOURCE_DIR / "P8_Y5_R2FR_4480_NEXT_TARGET.csv"

GATE_PATH = SCRIPT_DIR / "orientation_carrier_quadrupole_gate.py"
GENERATOR_PATH = SCRIPT_DIR / "Y5_R2FR_4480_orientation_carrier_zero_proof_or_quadrupole_residual_scorer.py"
STAMP = datetime.now(timezone.utc).replace(microsecond=0).isoformat()

FORMAL_495 = FORMAL / "495-PPC4161-profile-symmetry-dimension-branch-or-anisotropic-quadrupole-bound.md"
NEXT_4479 = SOURCE_DIR / "P8_Y5_R2FR_4479_NEXT_TARGET.csv"
THEOREM_4479 = SOURCE_DIR / "P8_Y5_R2FR_4479_LOCAL_SPATIAL_SYMMETRY_THEOREM.csv"
BOUNDS_4479 = SOURCE_DIR / "P8_Y5_R2FR_4479_ANISOTROPY_BOUND_ROWS.csv"
INPUTS_4479 = SOURCE_DIR / "P8_Y5_R2FR_4479_SHAPE_BRANCH_INPUT_ROWS.csv"
GATES_4479 = SOURCE_DIR / "P8_Y5_R2FR_4479_CLAIM_GATES.csv"
DOC_3168 = POST / "3168-Y5-R2FR-anisotropic-Shapiro-quadrupole-kernel-or-source-transfer-contract-under-AX1090.md"
DOC_3182 = POST / "3182-Y5-R2FR-metric-readout-of-tracefree-Hessian-carrier-or-tidal-response-coefficient-under-AX1090.md"
DOC_867 = POST / "867-Y5-R10-boundary-orientation-charge-metric-last-derivation-gate.md"
DOC_161 = POST / "161-trace-quadrupole-source-law-attempt.md"


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
            "source_id": "SRC4480_00_next4479",
            "ref": NEXT_4479,
            "needle": "4480-Y5-R2FR-orientation-carrier-zero-proof-or-quadrupole-residual-scorer.md",
            "role": "4479 selected orientation-carrier zero proof or quadrupole scorer.",
        },
        {
            "source_id": "SRC4480_01_formal495_result",
            "ref": FORMAL_495,
            "needle": "no orientation/nematic/tidal carrier",
            "role": "formal 4479 shape branch requiring orientation-carrier closure.",
        },
        {
            "source_id": "SRC4480_02_theorem4479_orientation",
            "ref": THEOREM_4479,
            "needle": "LSS4479_3_isotropy_no_orientation_carrier",
            "role": "4479 row that makes isotropy conditional on no orientation carrier.",
        },
        {
            "source_id": "SRC4480_03_bounds4479_quadrupole",
            "ref": BOUNDS_4479,
            "needle": "AB4479_2_quadrupole",
            "role": "4479 quadrupole residual bound handoff.",
        },
        {
            "source_id": "SRC4480_04_inputs4479_orientation",
            "ref": INPUTS_4479,
            "needle": "SBI4479_3_orientation_carrier",
            "role": "4479 missing orientation-carrier certificate.",
        },
        {
            "source_id": "SRC4480_05_gates4479_parent_unsigned",
            "ref": GATES_4479,
            "needle": "CG4479_2_clean_branch_parent_signed",
            "role": "4479 gate that blocks the clean branch.",
        },
        {
            "source_id": "SRC4480_06_shapiro3168_kernel",
            "ref": DOC_3168,
            "needle": "|Pi_quad_LOS| <= 1",
            "role": "prior anisotropic Shapiro line-of-sight quadrupole kernel.",
        },
        {
            "source_id": "SRC4480_07_metric3182_slip",
            "ref": DOC_3182,
            "needle": "Psi - Phi = 2 Sigma_H phi_ext",
            "role": "prior tracefree Hessian carrier enters weak-field metric readout.",
        },
        {
            "source_id": "SRC4480_08_boundary867_orientation",
            "ref": DOC_867,
            "needle": "boundary orientation sign",
            "role": "prior boundary orientation warning.",
        },
        {
            "source_id": "SRC4480_09_trace161_quadrupole",
            "ref": DOC_161,
            "needle": "quadrupole law: plausible rough clue",
            "role": "prior trace/quadrupole source-law clue, kept nonclaim.",
        },
        {
            "source_id": "SRC4480_10_gate",
            "ref": GATE_PATH,
            "needle": "def orientation_zero_proof_rows",
            "role": "4480 orientation carrier and quadrupole scorer gate.",
        },
        {
            "source_id": "SRC4480_11_generator",
            "ref": GENERATOR_PATH,
            "needle": 'CHECKPOINT = "4480"',
            "role": "4480 generator script.",
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
            "proof_result": "SO(3) scalar marker gives Q_M_TF=0 by representation theory, but parent carrier alphabet is unsigned",
            "fallback_result": "finite l=2 quadrupole branch now has canonical amplitude, compact-support bound and PPN/clock/orbital/Shapiro scorer contracts",
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
            "orientation_zero_theorem": "derived_parent_unsigned",
            "wave_Poynting_route": "kept_as_explicit_STF_carrier_counterroute",
            "quadrupole_scorer": "derived_contract_nonclaim",
            "sharpest_open_clause": "parent_STF_carrier_inventory_and_l2_arena_bounds",
            "public_local_GR_claim": False,
            "next_target": NEXT_TARGET,
            "valid_for_claim": False,
            "generated_utc": STAMP,
        }
    ]


def next_rows() -> List[Dict[str, object]]:
    return [
        {
            "next_id": "NT4480_0",
            "target": NEXT_TARGET,
            "objective": "Source the parent STF carrier inventory and l=2 empirical bound inputs, or sign Z_orientation from the parent action.",
            "derive_first": "enumerate whether vectors, spin axes, wave/Poynting fluxes, tidal tensors, nematic directors, anisotropic support metrics, or boundary normals survive in the parent marker/support alphabet",
            "fallback": "fill epsilon_Q, A_STF, tau_PPN_Q, tau_clock_Q, tau_orbital_Q and tau_Shapiro_Q as nonclaim bound rows",
            "risk": "using scalar monopole tests to hide an l=2 anisotropic residual",
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
            "claim": "4480 proves the conditional representation-theory route Q_M_TF=0 for a true SO(3)-scalar marker profile and derives a finite quadrupole residual scorer if an orientation carrier survives.",
            "current_evidence": "4480 source register, orientation zero proof rows, quadrupole scorer rows, quadrupole input rows, claim gates, decision/status/next CSVs and validation.",
            "status": "private_orientation_zero_theorem_and_quadrupole_scorer_nonclaim",
            "next_test": NEXT_TARGET,
            "key_risk": "claiming isotropy while a wave/Poynting, tidal, spin, nematic or boundary-normal carrier survives.",
            "sector": "local_gr_newton_r10_scalar_source_coupling",
            "evidence": str(FORMAL_PATH),
            "next_action": NEXT_TARGET,
            "risk": "l=2 branch remains unbounded until carrier inventory and arena tolerances are sourced",
        }
    )
    write_csv(CLAIMS_PATH, rows)


def formal_body(
    sources: Sequence[Mapping[str, object]],
    proof_rows: Sequence[Mapping[str, object]],
    scorer_rows: Sequence[Mapping[str, object]],
    input_rows: Sequence[Mapping[str, object]],
    ledger: Sequence[Mapping[str, object]],
    gates: Sequence[Mapping[str, object]],
    decisions: Sequence[Mapping[str, object]],
    statuses: Sequence[Mapping[str, object]],
    next_targets: Sequence[Mapping[str, object]],
) -> str:
    return f"""# 496 PPC4161 - Orientation Carrier Zero Proof Or Quadrupole Residual Scorer

Private checkpoint: `{CHECKPOINT}`  
Marker: `{MARKER}`  
Decision: `{DECISION}`  
Generated UTC: `{STAMP}`

## Result

4480 takes the leap that 4479 set up.

The clean zero route is now an actual representation-theory statement:

```text
F_M is a true local SO(3)-scalar profile
=> M^{{ij}}=int y^i y^j F_M d^3y = (mu2_M/3) h^{{ij}}
=> Q_M_TF^{{ij}}=0.
```

So the local isotropic branch is not magic. It is valid if the parent action really has no surviving orientation carrier.

The important catch is also now explicit:

```text
wave vector / Poynting flux / spin axis / tidal tensor / nematic director / boundary normal
```

are exactly the things that can source the tracefree `l=2` carrier. That means the user's Poynting-vector instinct is not a distraction; it is a live fork in the derivation.

If any such carrier survives, the branch is still not handwavy. It becomes:

```text
Q_M_TF^{{ij}}=epsilon_Q * mu0_abs * ell_sup^2 * A_STF^{{ij}},
0 <= epsilon_Q <= 1,
R_quad_a = lambda_M*zeta_Q_a*Q_M_TF^{{ij}}*H_a,ij^TF/(2*N_a).
```

With the compact-support envelope:

```text
|R_quad_a| <= |lambda_M| |zeta_Q_a| mu0_abs ell_sup^2 /(2 |N_a| L_loc^2).
```

That is forward motion: either sign the carrier absence, or score the quadrupole residual honestly.

## Orientation Zero Proof

{table(proof_rows)}

## Quadrupole Residual Scorer

{table(scorer_rows)}

## Quadrupole Input Rows

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
    proof_rows: Sequence[Mapping[str, object]],
    scorer_rows: Sequence[Mapping[str, object]],
    input_rows: Sequence[Mapping[str, object]],
    ledger: Sequence[Mapping[str, object]],
    gates: Sequence[Mapping[str, object]],
    decisions: Sequence[Mapping[str, object]],
    statuses: Sequence[Mapping[str, object]],
    next_targets: Sequence[Mapping[str, object]],
) -> str:
    return f"""# 4480 Y5/R2FR - Orientation Carrier Zero Proof Or Quadrupole Residual Scorer

Private post-checkpoint mirror for:

`{FORMAL_PATH}`

## What Actually Moved

The `Q_M_TF=0` route is now a clean SO(3) representation theorem, not an isotropy assumption. The same file also keeps wave/Poynting, spin, tidal, nematic and boundary-normal routes alive as explicit l=2 carriers. If the parent cannot sign carrier absence, the quadrupole branch is scoreable through componentwise PPN, clock, orbital and Shapiro contracts.

## Orientation Zero

{table(proof_rows)}

## Quadrupole Scorer

{table(scorer_rows)}

## Input Rows

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
    proof_rows: Sequence[Mapping[str, object]],
    scorer_rows: Sequence[Mapping[str, object]],
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
        "VAL4480_0_sources_exist_and_needles_found",
        all(row.get("local_path_exists") is True and row.get("needle_found") is True for row in sources),
        "every cited source path exists and its needle is found",
    )
    add(
        "VAL4480_1_SO3_zero_theorem_written",
        any(row.get("proof_id") == "OCZ4480_0_SO3_scalar_profile_theorem" for row in proof_rows),
        "SO(3) scalar marker theorem is written",
    )
    add(
        "VAL4480_2_orientation_verdict_not_overclaimed",
        any(row.get("proof_id") == "OCZ4480_5_verdict" and row.get("parent_signed") is False for row in proof_rows),
        "orientation zero remains parent-unsigned",
    )
    add(
        "VAL4480_3_wave_Poynting_counterroute_kept",
        any(row.get("proof_id") == "OCZ4480_3_wave_and_Poynting_counterroute" for row in proof_rows),
        "wave/Poynting carrier route is explicit",
    )
    add(
        "VAL4480_4_quadrupole_scorer_written",
        all(
            any(row.get("scorer_id") == scorer_id for row in scorer_rows)
            for scorer_id in [
                "QRS4480_0_canonical_STF_amplitude",
                "QRS4480_1_local_projection_bound",
                "QRS4480_3_Shapiro_LOS_kernel",
                "QRS4480_6_no_cancellation_envelope",
            ]
        ),
        "canonical amplitude, local bound, Shapiro kernel and no-cancellation envelope are written",
    )
    add(
        "VAL4480_5_input_rows_staged",
        all(
            any(row.get("row_id") == row_id for row in input_rows)
            for row_id in [
                "QRI4480_0_Z_orientation",
                "QRI4480_1_carrier_inventory",
                "QRI4480_2_epsilon_Q",
                "QRI4480_3_A_STF",
                "QRI4480_4_tau_PPN_Q",
                "QRI4480_5_tau_clock_Q",
                "QRI4480_6_tau_orbital_Q",
                "QRI4480_7_tau_Shapiro_Q",
            ]
        ),
        "input rows include carrier certificate, finite amplitude/orientation and l=2 arena bounds",
    )
    add(
        "VAL4480_6_input_rows_remain_nonclaim",
        any("MISSING" in str(row.get("current_value")) for row in input_rows)
        and all(row.get("valid_for_claim") is False for row in input_rows),
        "input rows keep missing source values and valid_for_claim=false",
    )
    add(
        "VAL4480_7_claim_gates_block_local_GR",
        all(str(row.get("claim_allowed")).lower() == "false" for row in gates)
        and any(row.get("gate_id") == "CG4480_2_orientation_zero_parent_signed" and str(row.get("gate_pass")).lower() == "false" for row in gates),
        "claim gates block local-GR/R10 promotion until orientation zero or bound inputs are sourced",
    )
    add(
        "VAL4480_8_no_generated_claim_rows",
        all(
            str(row.get("valid_for_claim")).lower() == "false"
            for group in [sources, proof_rows, scorer_rows, input_rows, gates, decisions, statuses, next_targets]
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
    add("VAL4480_9_csvs_parse", csv_ok, "; ".join(csv_detail))
    add("VAL4480_10_docs_written", FORMAL_PATH.exists() and DOC_PATH.exists(), "formal and post checkpoint docs exist")
    add(
        "VAL4480_11_claim_register_updated",
        any(row.get("claim_id") == CLAIM_ID for row in read_csv(CLAIMS_PATH)),
        "claims register contains L-322",
    )
    add(
        "VAL4480_12_spine_and_packet_updated",
        MARKER in text(SPINE_PATH) and PACKET_MARKER in text(PACKET_PATH),
        "unification spine and private packet integration contain 4480 markers",
    )
    add(
        "VAL4480_13_next_target_selected",
        bool(next_targets) and next_targets[0].get("target") == NEXT_TARGET,
        NEXT_TARGET,
    )
    add("VAL4480_14_pycache_removed", not (SCRIPT_DIR / "__pycache__").exists(), "scripts __pycache__ absent after generation")
    return validations


def main() -> None:
    sources = source_rows()
    proof_rows = orientation_zero_proof_rows()
    scorer_rows = quadrupole_residual_scorer_rows()
    input_rows = quadrupole_input_rows()
    ledger = gate_decision_rows(NEXT_TARGET)
    gates = claim_gate_rows(sources, proof_rows, scorer_rows, input_rows)
    decisions = decision_rows()
    statuses = status_rows()
    next_targets = next_rows()

    write_csv(SOURCE_REGISTER, sources)
    write_csv(ZERO_PROOF_CSV, proof_rows)
    write_csv(SCORER_CSV, scorer_rows)
    write_csv(INPUTS_CSV, input_rows)
    write_csv(DECISION_LEDGER_CSV, ledger)
    write_csv(CLAIM_GATES_CSV, gates)
    write_csv(DECISION_CSV, decisions)
    write_csv(STATUS_CSV, statuses)
    write_csv(NEXT_CSV, next_targets)

    write_text(FORMAL_PATH, formal_body(sources, proof_rows, scorer_rows, input_rows, ledger, gates, decisions, statuses, next_targets))
    write_text(DOC_PATH, post_body(sources, proof_rows, scorer_rows, input_rows, ledger, gates, decisions, statuses, next_targets))
    update_claims_register()

    append_section_once(
        SPINE_PATH,
        MARKER,
        "4480 Orientation Carrier Zero Or Quadrupole Scorer",
        "4480 proves the conditional representation-theory zero route: a true local SO(3)-scalar marker profile has no tracefree second moment, so `Q_M_TF^{ij}=0`. It also keeps wave/Poynting, spin, tidal, nematic and boundary-normal routes as explicit l=2 carriers. If any survives, the finite quadrupole branch is scored through a compact-support no-cancellation envelope.",
    )
    append_section_once(
        PACKET_PATH,
        PACKET_MARKER,
        "4480 Packet Integration",
        "The private packet now has an orientation-carrier gate. The next source job is not vague: enumerate the parent STF carrier alphabet and source or bound `epsilon_Q`, `A_STF`, `tau_PPN_Q`, `tau_clock_Q`, `tau_orbital_Q` and `tau_Shapiro_Q`.",
    )

    pycache = SCRIPT_DIR / "__pycache__"
    if pycache.exists():
        shutil.rmtree(pycache)

    csv_paths = [
        SOURCE_REGISTER,
        ZERO_PROOF_CSV,
        SCORER_CSV,
        INPUTS_CSV,
        DECISION_LEDGER_CSV,
        CLAIM_GATES_CSV,
        DECISION_CSV,
        STATUS_CSV,
        NEXT_CSV,
    ]
    validations = validate(sources, proof_rows, scorer_rows, input_rows, gates, decisions, statuses, next_targets, csv_paths)
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

from __future__ import annotations

import shutil
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List, Mapping, Sequence


SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

from parent_inventory_zero_profile_moment_gate import (  # noqa: E402
    claim_gate_rows,
    decision_rows as gate_decision_rows,
    inventory_zero_proof_rows,
    marker_profile_moment_rows,
    moment_intake_rows,
    read_csv,
    write_csv,
)


ROOT = Path(__file__).resolve().parents[2]
FORMAL = ROOT / "formalization-workbench"
POST = ROOT / "post-checkpoint-work"
SOURCE_DIR = POST / "source-intake" / "mts_residuals"

CHECKPOINT = "4477"
CLAIM_ID = "L-319"
MARKER = "PPC4161_PARENT_INVENTORY_ZERO_PROOF_OR_MARKER_PROFILE_MOMENT_DERIVATION_4477"
PACKET_MARKER = "PPC4161_PACKET_PARENT_INVENTORY_ZERO_PROOF_OR_MARKER_PROFILE_MOMENT_DERIVATION_4477"
DECISION = "PARENT_INVENTORY_ZERO_THEOREM_PARENT_UNSIGNED_MARKER_PROFILE_MOMENT_LAW_DERIVED_NONCLAIM"
NEXT_TARGET = "4478-Y5-R2FR-marker-profile-support-zero-certificate-or-first-moment-input-row.md"

FORMAL_PATH = FORMAL / "493-PPC4161-parent-inventory-zero-proof-or-marker-profile-moment-derivation.md"
DOC_PATH = POST / "4477-Y5-R2FR-parent-inventory-zero-proof-or-marker-profile-moment-derivation.md"
VALIDATION_PATH = SOURCE_DIR / "P8_Y5_BRR545_4477_VALIDATION.csv"
SPINE_PATH = FORMAL / "07-unification-spine.md"
PACKET_PATH = FORMAL / "180-PPC4161-private-local-packet-integration.md"
CLAIMS_PATH = FORMAL / "02-claims-register.csv"

SOURCE_REGISTER = SOURCE_DIR / "P8_Y5_R2FR_4477_SOURCE_REGISTER.csv"
ZERO_PROOF_CSV = SOURCE_DIR / "P8_Y5_R2FR_4477_PARENT_INVENTORY_ZERO_PROOF.csv"
MOMENT_CSV = SOURCE_DIR / "P8_Y5_R2FR_4477_MARKER_PROFILE_MOMENT_DERIVATION.csv"
INTAKE_CSV = SOURCE_DIR / "P8_Y5_R2FR_4477_MARKER_MOMENT_INTAKE_ROWS.csv"
DECISION_LEDGER_CSV = SOURCE_DIR / "P8_Y5_R2FR_4477_DECISION_LEDGER.csv"
CLAIM_GATES_CSV = SOURCE_DIR / "P8_Y5_R2FR_4477_CLAIM_GATES.csv"
DECISION_CSV = SOURCE_DIR / "P8_Y5_R2FR_4477_DECISION.csv"
STATUS_CSV = SOURCE_DIR / "P8_Y5_R2FR_4477_STATUS.csv"
NEXT_CSV = SOURCE_DIR / "P8_Y5_R2FR_4477_NEXT_TARGET.csv"

GATE_PATH = SCRIPT_DIR / "parent_inventory_zero_profile_moment_gate.py"
GENERATOR_PATH = SCRIPT_DIR / "Y5_R2FR_4477_parent_inventory_zero_proof_or_marker_profile_moment_derivation.py"
STAMP = datetime.now(timezone.utc).replace(microsecond=0).isoformat()

FORMAL_492 = FORMAL / "492-PPC4161-parent-action-inventory-signature-or-lambdaM-projection-map.md"
NEXT_4476 = SOURCE_DIR / "P8_Y5_R2FR_4476_NEXT_TARGET.csv"
INVENTORY_4476 = SOURCE_DIR / "P8_Y5_R2FR_4476_PARENT_ACTION_INVENTORY_SIGNATURE.csv"
PROJECTION_4476 = SOURCE_DIR / "P8_Y5_R2FR_4476_LAMBDAM_PROJECTION_MAP.csv"
INTAKE_4476 = SOURCE_DIR / "P8_Y5_R2FR_4476_PROJECTION_INTAKE_ROWS.csv"
GATES_4476 = SOURCE_DIR / "P8_Y5_R2FR_4476_CLAIM_GATES.csv"
THEOREM_4475 = SOURCE_DIR / "P8_Y5_R2FR_4475_MARKER_BULK_COUPLING_ZERO_THEOREM.csv"


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
            "source_id": "SRC4477_00_next4476",
            "ref": NEXT_4476,
            "needle": "4477-Y5-R2FR-parent-inventory-zero-proof-or-marker-profile-moment-derivation.md",
            "role": "4476 selected parent inventory zero proof or marker profile moment derivation.",
        },
        {
            "source_id": "SRC4477_01_formal492_Zinventory",
            "ref": FORMAL_492,
            "needle": "Z_inventory = True iff Pi_I_M(S_bulk) = 0.",
            "role": "formal 4476 inventory signature statement.",
        },
        {
            "source_id": "SRC4477_02_formal492_projection",
            "ref": FORMAL_492,
            "needle": "C_a^M = lambda_M*(zeta_a*mu0_M + zeta_grad_a*mu2_M/L_loc^2)/N_a.",
            "role": "formal 4476 finite projection formula needing moment refinement.",
        },
        {
            "source_id": "SRC4477_03_inventory4476_verdict",
            "ref": INVENTORY_4476,
            "needle": "PAI4476_5_verdict",
            "role": "4476 inventory signature verdict.",
        },
        {
            "source_id": "SRC4477_04_projection4476_universal",
            "ref": PROJECTION_4476,
            "needle": "PMAP4476_0_universal_projection",
            "role": "4476 universal lambda_M projection map.",
        },
        {
            "source_id": "SRC4477_05_projection4476_envelope",
            "ref": PROJECTION_4476,
            "needle": "PMAP4476_7_no_cancellation_envelope",
            "role": "4476 no-cancellation envelope.",
        },
        {
            "source_id": "SRC4477_06_intake4476_mu0",
            "ref": INTAKE_4476,
            "needle": "PIR4476_1_mu0_M",
            "role": "4476 mu0_M intake row.",
        },
        {
            "source_id": "SRC4477_07_intake4476_mu2",
            "ref": INTAKE_4476,
            "needle": "PIR4476_2_mu2_M",
            "role": "4476 mu2_M intake row.",
        },
        {
            "source_id": "SRC4477_08_gates4476_inventory",
            "ref": GATES_4476,
            "needle": "CG4476_2_inventory_parent_signed",
            "role": "4476 gate blocking inventory overclaim.",
        },
        {
            "source_id": "SRC4477_09_theorem4475_lambda",
            "ref": THEOREM_4475,
            "needle": "LMB4475_7_verdict",
            "role": "4475 lambda_M zero theorem verdict.",
        },
        {
            "source_id": "SRC4477_10_gate",
            "ref": GATE_PATH,
            "needle": "def inventory_zero_proof_rows",
            "role": "4477 parent inventory/profile moment gate.",
        },
        {
            "source_id": "SRC4477_11_generator",
            "ref": GENERATOR_PATH,
            "needle": 'CHECKPOINT = "4477"',
            "role": "4477 generator script.",
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
            "proof_result": "exact conditional Z_inventory zero theorem written from quotient action factorization but not parent-signed",
            "fallback_result": "finite marker profile moment expansion derived with centered/isotropic coefficient, support bound, and moment projection vector",
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
            "inventory_zero_theorem": "written_parent_unsigned",
            "moment_law": "derived",
            "sharpest_open_clause": "profile_support_zero_certificate_or_moment_inputs",
            "moment_intake_status": "staged_missing_values",
            "public_local_GR_claim": False,
            "next_target": NEXT_TARGET,
            "valid_for_claim": False,
            "generated_utc": STAMP,
        }
    ]


def next_rows() -> List[Dict[str, object]]:
    return [
        {
            "next_id": "NT4477_0",
            "target": NEXT_TARGET,
            "objective": "Prove the marker profile/support is absent on the parent branch, or derive the first non-circular support/moment input for the finite projection vector.",
            "derive_first": "show F_M is absent because the parent action alphabet has no marker support carrier",
            "fallback": "derive ell_sup, d_eff, centering/isotropy, mu0_M and mu2_M from parent geometry/support rather than fitting them",
            "risk": "using a formal moment expansion without a sourced profile/support law",
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
            "claim": "4477 writes the exact conditional parent-inventory zero theorem and derives the finite marker profile moment expansion, including the centered/isotropic mu2_M/(2 d_eff) correction and compact-support bound.",
            "current_evidence": "4477 source register, parent inventory zero proof rows, marker profile moment derivation, moment intake rows, claim gates, decision/status/next CSVs and validation.",
            "status": "private_conditional_theorem_and_moment_law_nonclaim",
            "next_test": NEXT_TARGET,
            "key_risk": "treating the moment expansion as evidence before F_M, support, d_eff, symmetry and moments are parent-sourced.",
            "sector": "local_gr_newton_r10_scalar_source_coupling",
            "evidence": str(FORMAL_PATH),
            "next_action": NEXT_TARGET,
            "risk": "finite marker branch remains unscored until profile/support inputs or Z_inventory close",
        }
    )
    write_csv(CLAIMS_PATH, rows)


def formal_body(
    sources: Sequence[Mapping[str, object]],
    proof_rows: Sequence[Mapping[str, object]],
    moment_rows: Sequence[Mapping[str, object]],
    intake_rows: Sequence[Mapping[str, object]],
    ledger: Sequence[Mapping[str, object]],
    gates: Sequence[Mapping[str, object]],
    decisions: Sequence[Mapping[str, object]],
    statuses: Sequence[Mapping[str, object]],
    next_targets: Sequence[Mapping[str, object]],
) -> str:
    return f"""# 493 PPC4161 - Parent Inventory Zero Proof Or Marker Profile Moment Derivation

Private checkpoint: `{CHECKPOINT}`
Marker: `{MARKER}`
Decision: `{DECISION}`
Generated UTC: `{STAMP}`

## Result

4477 pushes the fork instead of circling it.

The exact zero route is:

```text
S_bulk[Phi] = Sbar_bulk[q(Phi)]
I_M = <M_cell, R_obs_as_bulk, P_active, J_finite, labelled_species, M_aux>
Z_inventory = True iff Pi_I_M(S_bulk) = 0.
```

That theorem is valid if the parent action really factors through a quotient whose bulk coordinates exclude the marker ideal, with source/readout, auxiliary and boundary firewalls signed. Current MTS has not signed those parent clauses yet.

The finite route now has an actual profile moment expansion:

```text
int F_M(y) O_a(x+y) d^d y
 = mu0_M O_a(x)
 + mu1_M^i partial_i O_a(x)
 + 1/2 mu2_M^ij partial_i partial_j O_a(x)
 + ...
```

For a centred isotropic profile:

```text
int F_M O_a = mu0_M O_a + [mu2_M/(2 d_eff)] Delta_h O_a + O(mu4_M/L_loc^4).
```

So the finite branch becomes:

```text
C_a^M = lambda_M*(zeta_a mu0_M + zeta_grad_a mu2_M/(2 d_eff L_loc^2))/N_a.
```

That is the useful leap: `mu0_M` and `mu2_M` are now derived moment objects with a compact-support bound, not vague placeholders.

## Parent Inventory Zero Proof

{table(proof_rows)}

## Marker Profile Moment Derivation

{table(moment_rows)}

## Moment Intake Rows

{table(intake_rows)}

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
    moment_rows: Sequence[Mapping[str, object]],
    intake_rows: Sequence[Mapping[str, object]],
    ledger: Sequence[Mapping[str, object]],
    gates: Sequence[Mapping[str, object]],
    decisions: Sequence[Mapping[str, object]],
    statuses: Sequence[Mapping[str, object]],
    next_targets: Sequence[Mapping[str, object]],
) -> str:
    return f"""# 4477 Y5/R2FR - Parent Inventory Zero Proof Or Marker Profile Moment Derivation

Private post-checkpoint mirror for:

`{FORMAL_PATH}`

## What Actually Moved

`Z_inventory` now has an exact conditional quotient-action proof, and the finite marker branch now has a real Taylor/moment law. The claim remains blocked because the parent action alphabet and marker support/profile are not yet signed.

## Zero Proof

{table(proof_rows)}

## Moment Law

{table(moment_rows)}

## Intake Rows

{table(intake_rows)}

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
    moment_rows: Sequence[Mapping[str, object]],
    intake_rows: Sequence[Mapping[str, object]],
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
        "VAL4477_0_sources_exist_and_needles_found",
        all(row.get("local_path_exists") is True and row.get("needle_found") is True for row in sources),
        "every cited source path exists and its needle is found",
    )
    add(
        "VAL4477_1_zero_theorem_written",
        any(row.get("proof_id") == "PIZ4477_5_verdict" for row in proof_rows),
        "parent inventory zero theorem verdict is written",
    )
    add(
        "VAL4477_2_zero_theorem_not_overclaimed",
        any(row.get("proof_id") == "PIZ4477_5_verdict" and row.get("parent_signed") is False for row in proof_rows),
        "zero theorem remains parent-unsigned",
    )
    add(
        "VAL4477_3_moment_law_derived",
        all(
            any(row.get("derivation_id") == derivation_id for row in moment_rows)
            for derivation_id in [
                "MPM4477_0_distribution_expansion",
                "MPM4477_1_centered_isotropic_profile",
                "MPM4477_2_effective_marker_length",
                "MPM4477_3_compact_support_bound",
                "MPM4477_5_projection_vector_update",
            ]
        ),
        "moment expansion, centered/isotropic law, length law, compact bound and projection update are written",
    )
    add(
        "VAL4477_4_moment_intake_rows_staged",
        all(
            any(row.get("row_id") == row_id for row in intake_rows)
            for row_id in [
                "MIR4477_0_Z_inventory",
                "MIR4477_1_d_eff",
                "MIR4477_2_mu0_M",
                "MIR4477_3_mu2_M",
                "MIR4477_4_ell_sup",
                "MIR4477_5_profile_symmetry",
                "MIR4477_6_component_values",
            ]
        ),
        "moment intake rows include inventory, support dimension, moments, support radius, symmetry and component values",
    )
    add(
        "VAL4477_5_moment_rows_remain_nonclaim",
        any("MISSING" in str(row.get("current_value")) for row in intake_rows)
        and all(row.get("valid_for_claim") is False for row in intake_rows),
        "moment intake rows keep missing source values and valid_for_claim=false",
    )
    add(
        "VAL4477_6_claim_gates_block_local_GR",
        all(str(row.get("claim_allowed")).lower() == "false" for row in gates)
        and any(row.get("gate_id") == "CG4477_2_zero_theorem_parent_signed" and str(row.get("gate_pass")).lower() == "false" for row in gates),
        "claim gates block local-GR/R10 promotion until Z_inventory is signed or finite values are sourced",
    )
    add(
        "VAL4477_7_no_generated_claim_rows",
        all(
            str(row.get("valid_for_claim")).lower() == "false"
            for group in [sources, proof_rows, moment_rows, intake_rows, gates, decisions, statuses, next_targets]
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
    add("VAL4477_8_csvs_parse", csv_ok, "; ".join(csv_detail))
    add("VAL4477_9_docs_written", FORMAL_PATH.exists() and DOC_PATH.exists(), "formal and post checkpoint docs exist")
    add(
        "VAL4477_10_claim_register_updated",
        any(row.get("claim_id") == CLAIM_ID for row in read_csv(CLAIMS_PATH)),
        "claims register contains L-319",
    )
    add(
        "VAL4477_11_spine_and_packet_updated",
        MARKER in text(SPINE_PATH) and PACKET_MARKER in text(PACKET_PATH),
        "unification spine and private packet integration contain 4477 markers",
    )
    add(
        "VAL4477_12_next_target_selected",
        bool(next_targets) and next_targets[0].get("target") == NEXT_TARGET,
        NEXT_TARGET,
    )
    add("VAL4477_13_pycache_removed", not (SCRIPT_DIR / "__pycache__").exists(), "scripts __pycache__ absent after generation")
    return validations


def main() -> None:
    sources = source_rows()
    proof_rows = inventory_zero_proof_rows()
    moment_rows = marker_profile_moment_rows()
    intake_rows = moment_intake_rows()
    ledger = gate_decision_rows(NEXT_TARGET)
    gates = claim_gate_rows(sources, proof_rows, moment_rows, intake_rows)
    decisions = decision_rows()
    statuses = status_rows()
    next_targets = next_rows()

    write_csv(SOURCE_REGISTER, sources)
    write_csv(ZERO_PROOF_CSV, proof_rows)
    write_csv(MOMENT_CSV, moment_rows)
    write_csv(INTAKE_CSV, intake_rows)
    write_csv(DECISION_LEDGER_CSV, ledger)
    write_csv(CLAIM_GATES_CSV, gates)
    write_csv(DECISION_CSV, decisions)
    write_csv(STATUS_CSV, statuses)
    write_csv(NEXT_CSV, next_targets)

    write_text(FORMAL_PATH, formal_body(sources, proof_rows, moment_rows, intake_rows, ledger, gates, decisions, statuses, next_targets))
    write_text(DOC_PATH, post_body(sources, proof_rows, moment_rows, intake_rows, ledger, gates, decisions, statuses, next_targets))
    update_claims_register()

    append_section_once(
        SPINE_PATH,
        MARKER,
        "4477 Parent Inventory Zero Or Marker Profile Moments",
        "4477 proves the exact conditional `Z_inventory` theorem from quotient-action factorization and derives the finite marker profile moment law. A centred isotropic marker profile gives `int F_M O_a = mu0_M O_a + mu2_M Delta_h O_a/(2 d_eff) + ...`; compact support gives `mu2_abs <= ell_sup^2 mu0_abs`. The proof remains parent-unsigned, so the moment intake rows stay nonclaim.",
    )
    append_section_once(
        PACKET_PATH,
        PACKET_MARKER,
        "4477 Packet Integration",
        "The private packet now has the profile-moment machinery needed to turn any finite `lambda_M` into bounded local residuals: `d_eff`, `mu0_M`, `mu2_M`, `ell_sup`, centering/isotropy, projectors and normalizations must be supplied or zero-certified.",
    )

    pycache = SCRIPT_DIR / "__pycache__"
    if pycache.exists():
        shutil.rmtree(pycache)

    csv_paths = [
        SOURCE_REGISTER,
        ZERO_PROOF_CSV,
        MOMENT_CSV,
        INTAKE_CSV,
        DECISION_LEDGER_CSV,
        CLAIM_GATES_CSV,
        DECISION_CSV,
        STATUS_CSV,
        NEXT_CSV,
    ]
    validations = validate(sources, proof_rows, moment_rows, intake_rows, gates, decisions, statuses, next_targets, csv_paths)
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

from __future__ import annotations

import shutil
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List, Mapping, Sequence


SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

from marker_profile_support_gate import (  # noqa: E402
    claim_gate_rows,
    decision_rows as gate_decision_rows,
    first_moment_input_law_rows,
    first_moment_input_rows,
    read_csv,
    support_zero_certificate_rows,
    write_csv,
)


ROOT = Path(__file__).resolve().parents[2]
FORMAL = ROOT / "formalization-workbench"
POST = ROOT / "post-checkpoint-work"
SOURCE_DIR = POST / "source-intake" / "mts_residuals"

CHECKPOINT = "4478"
CLAIM_ID = "L-320"
MARKER = "PPC4161_MARKER_PROFILE_SUPPORT_ZERO_CERTIFICATE_OR_FIRST_MOMENT_INPUT_ROW_4478"
PACKET_MARKER = "PPC4161_PACKET_MARKER_PROFILE_SUPPORT_ZERO_CERTIFICATE_OR_FIRST_MOMENT_INPUT_ROW_4478"
DECISION = "MARKER_SUPPORT_ZERO_PARENT_UNSIGNED_FIRST_MOMENT_INPUT_LAWS_DERIVED_NONCLAIM"
NEXT_TARGET = "4479-Y5-R2FR-profile-symmetry-dimension-branch-or-anisotropic-quadrupole-bound.md"

FORMAL_PATH = FORMAL / "494-PPC4161-marker-profile-support-zero-certificate-or-first-moment-input-row.md"
DOC_PATH = POST / "4478-Y5-R2FR-marker-profile-support-zero-certificate-or-first-moment-input-row.md"
VALIDATION_PATH = SOURCE_DIR / "P8_Y5_BRR545_4478_VALIDATION.csv"
SPINE_PATH = FORMAL / "07-unification-spine.md"
PACKET_PATH = FORMAL / "180-PPC4161-private-local-packet-integration.md"
CLAIMS_PATH = FORMAL / "02-claims-register.csv"

SOURCE_REGISTER = SOURCE_DIR / "P8_Y5_R2FR_4478_SOURCE_REGISTER.csv"
SUPPORT_ZERO_CSV = SOURCE_DIR / "P8_Y5_R2FR_4478_SUPPORT_ZERO_CERTIFICATE.csv"
INPUT_LAW_CSV = SOURCE_DIR / "P8_Y5_R2FR_4478_FIRST_MOMENT_INPUT_LAWS.csv"
INPUT_ROWS_CSV = SOURCE_DIR / "P8_Y5_R2FR_4478_FIRST_MOMENT_INPUT_ROWS.csv"
DECISION_LEDGER_CSV = SOURCE_DIR / "P8_Y5_R2FR_4478_DECISION_LEDGER.csv"
CLAIM_GATES_CSV = SOURCE_DIR / "P8_Y5_R2FR_4478_CLAIM_GATES.csv"
DECISION_CSV = SOURCE_DIR / "P8_Y5_R2FR_4478_DECISION.csv"
STATUS_CSV = SOURCE_DIR / "P8_Y5_R2FR_4478_STATUS.csv"
NEXT_CSV = SOURCE_DIR / "P8_Y5_R2FR_4478_NEXT_TARGET.csv"

GATE_PATH = SCRIPT_DIR / "marker_profile_support_gate.py"
GENERATOR_PATH = SCRIPT_DIR / "Y5_R2FR_4478_marker_profile_support_zero_certificate_or_first_moment_input_row.py"
STAMP = datetime.now(timezone.utc).replace(microsecond=0).isoformat()

FORMAL_493 = FORMAL / "493-PPC4161-parent-inventory-zero-proof-or-marker-profile-moment-derivation.md"
NEXT_4477 = SOURCE_DIR / "P8_Y5_R2FR_4477_NEXT_TARGET.csv"
ZERO_4477 = SOURCE_DIR / "P8_Y5_R2FR_4477_PARENT_INVENTORY_ZERO_PROOF.csv"
MOMENT_4477 = SOURCE_DIR / "P8_Y5_R2FR_4477_MARKER_PROFILE_MOMENT_DERIVATION.csv"
INTAKE_4477 = SOURCE_DIR / "P8_Y5_R2FR_4477_MARKER_MOMENT_INTAKE_ROWS.csv"
GATES_4477 = SOURCE_DIR / "P8_Y5_R2FR_4477_CLAIM_GATES.csv"


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
            "source_id": "SRC4478_00_next4477",
            "ref": NEXT_4477,
            "needle": "4478-Y5-R2FR-marker-profile-support-zero-certificate-or-first-moment-input-row.md",
            "role": "4477 selected marker profile/support zero certificate or first moment input row.",
        },
        {
            "source_id": "SRC4478_01_formal493_absent",
            "ref": FORMAL_493,
            "needle": "show F_M is absent because the parent action alphabet has no marker support carrier",
            "role": "formal 4477 next target derive-first route.",
        },
        {
            "source_id": "SRC4478_02_formal493_bound",
            "ref": FORMAL_493,
            "needle": "mu2_abs <= ell_sup^2 mu0_abs",
            "role": "formal 4477 compact support bound.",
        },
        {
            "source_id": "SRC4478_03_zero4477_verdict",
            "ref": ZERO_4477,
            "needle": "PIZ4477_5_verdict",
            "role": "4477 parent inventory zero verdict.",
        },
        {
            "source_id": "SRC4478_04_moment4477_bound",
            "ref": MOMENT_4477,
            "needle": "MPM4477_3_compact_support_bound",
            "role": "4477 compact-support moment derivation.",
        },
        {
            "source_id": "SRC4478_05_moment4477_projection",
            "ref": MOMENT_4477,
            "needle": "MPM4477_5_projection_vector_update",
            "role": "4477 moment projection vector update.",
        },
        {
            "source_id": "SRC4478_06_intake4477_deff",
            "ref": INTAKE_4477,
            "needle": "MIR4477_1_d_eff",
            "role": "4477 support-dimension intake row.",
        },
        {
            "source_id": "SRC4478_07_intake4477_ellsup",
            "ref": INTAKE_4477,
            "needle": "MIR4477_4_ell_sup",
            "role": "4477 support-radius intake row.",
        },
        {
            "source_id": "SRC4478_08_intake4477_symmetry",
            "ref": INTAKE_4477,
            "needle": "MIR4477_5_profile_symmetry",
            "role": "4477 profile-symmetry intake row.",
        },
        {
            "source_id": "SRC4478_09_gates4477_zero",
            "ref": GATES_4477,
            "needle": "CG4477_2_zero_theorem_parent_signed",
            "role": "4477 gate blocking parent zero overclaim.",
        },
        {
            "source_id": "SRC4478_10_gate",
            "ref": GATE_PATH,
            "needle": "def support_zero_certificate_rows",
            "role": "4478 marker profile support gate.",
        },
        {
            "source_id": "SRC4478_11_generator",
            "ref": GENERATOR_PATH,
            "needle": 'CHECKPOINT = "4478"',
            "role": "4478 generator script.",
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
            "proof_result": "support zero certificate written but not parent-signed",
            "fallback_result": "first moment input laws derived for Q_M, d_eff, ell_rms, ell_sup, dipole and quadrupole branches",
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
            "support_zero_certificate": "written_parent_unsigned",
            "first_moment_laws": "derived",
            "sharpest_open_clause": "profile_symmetry_dimension_branch_or_anisotropic_quadrupole_bound",
            "first_input_status": "staged_missing_values",
            "public_local_GR_claim": False,
            "next_target": NEXT_TARGET,
            "valid_for_claim": False,
            "generated_utc": STAMP,
        }
    ]


def next_rows() -> List[Dict[str, object]]:
    return [
        {
            "next_id": "NT4478_0",
            "target": NEXT_TARGET,
            "objective": "Prove the local spatial support/isotropy branch or retain finite dipole and quadrupole anisotropy residual bounds.",
            "derive_first": "show local tests use d_eff=3 spatial worldtube support, centred profile and isotropic second moment",
            "fallback": "derive bounds for temporal smearing, D_M^i dipole and Q_M_TF^{ij} quadrupole residuals",
            "risk": "assuming profile symmetry or d_eff=3 without a support branch proof",
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
            "claim": "4478 writes the marker profile/support zero certificate and derives first moment input laws for finite support, including canonical normalization, d_eff branch, support-radius bound, centering/dipole and isotropy/quadrupole branches.",
            "current_evidence": "4478 source register, support zero certificate, first moment input laws, first moment input rows, claim gates, decision/status/next CSVs and validation.",
            "status": "private_support_zero_and_first_moment_laws_nonclaim",
            "next_test": NEXT_TARGET,
            "key_risk": "assuming support absence, d_eff=3 or isotropy before the parent support carrier and profile symmetry branches are signed.",
            "sector": "local_gr_newton_r10_scalar_source_coupling",
            "evidence": str(FORMAL_PATH),
            "next_action": NEXT_TARGET,
            "risk": "finite marker branch remains unscored until support zero or first moment values close",
        }
    )
    write_csv(CLAIMS_PATH, rows)


def formal_body(
    sources: Sequence[Mapping[str, object]],
    certificate_rows: Sequence[Mapping[str, object]],
    law_rows: Sequence[Mapping[str, object]],
    input_rows: Sequence[Mapping[str, object]],
    ledger: Sequence[Mapping[str, object]],
    gates: Sequence[Mapping[str, object]],
    decisions: Sequence[Mapping[str, object]],
    statuses: Sequence[Mapping[str, object]],
    next_targets: Sequence[Mapping[str, object]],
) -> str:
    return f"""# 494 PPC4161 - Marker Profile Support Zero Certificate Or First Moment Input Row

Private checkpoint: `{CHECKPOINT}`  
Marker: `{MARKER}`  
Decision: `{DECISION}`  
Generated UTC: `{STAMP}`

## Result

4478 attacks the support/profile throat.

The clean zero route is now:

```text
Z_support=True
iff no support carrier exists in S_bulk,
and readout is not support,
and ordinary Hilbert source worldtubes are not double-counted as marker support,
and boundary support is fixed/routed/no-flux.
```

If `Z_support` signs, then:

```text
F_M absent,
mu0_M = mu2_M = 0,
lambda_M*mu0_M = lambda_M*mu2_M = 0.
```

If support survives, the finite branch is canonically normalized:

```text
F_M(y)=Q_M f_M(y),  int f_M d^d y=1,
mu0_M=Q_M,
mu2_M=Q_M ell_rms^2,
ell_rms <= ell_sup.
```

The local support branch is conditionally `d_eff=3`; a covariant spacetime-smearing branch is not forbidden, but it carries clock/Lorentz/locality residual debt. Profile symmetry is also not assumed: non-centering gives a dipole row `D_M^i`, and anisotropy gives a tracefree quadrupole row `Q_M_TF^{{ij}}`.

## Support Zero Certificate

{table(certificate_rows)}

## First Moment Input Laws

{table(law_rows)}

## First Moment Input Rows

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
    certificate_rows: Sequence[Mapping[str, object]],
    law_rows: Sequence[Mapping[str, object]],
    input_rows: Sequence[Mapping[str, object]],
    ledger: Sequence[Mapping[str, object]],
    gates: Sequence[Mapping[str, object]],
    decisions: Sequence[Mapping[str, object]],
    statuses: Sequence[Mapping[str, object]],
    next_targets: Sequence[Mapping[str, object]],
) -> str:
    return f"""# 4478 Y5/R2FR - Marker Profile Support Zero Certificate Or First Moment Input Row

Private post-checkpoint mirror for:

`{FORMAL_PATH}`

## What Actually Moved

`F_M` support is now a certificate problem, not a placeholder. If support survives, the first finite inputs are `Q_M`, `d_eff`, `ell_rms`, `ell_sup`, `D_M^i` and `Q_M_TF^{{ij}}` with no hidden symmetry assumption.

## Support Zero

{table(certificate_rows)}

## Input Laws

{table(law_rows)}

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
    certificate_rows: Sequence[Mapping[str, object]],
    law_rows: Sequence[Mapping[str, object]],
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
        "VAL4478_0_sources_exist_and_needles_found",
        all(row.get("local_path_exists") is True and row.get("needle_found") is True for row in sources),
        "every cited source path exists and its needle is found",
    )
    add(
        "VAL4478_1_support_zero_certificate_written",
        any(row.get("certificate_id") == "SZC4478_5_verdict" for row in certificate_rows),
        "support zero certificate verdict is written",
    )
    add(
        "VAL4478_2_support_zero_not_overclaimed",
        any(row.get("certificate_id") == "SZC4478_5_verdict" and row.get("parent_signed") is False for row in certificate_rows),
        "support zero remains parent-unsigned",
    )
    add(
        "VAL4478_3_first_input_laws_written",
        all(
            any(row.get("law_id") == law_id for row in law_rows)
            for law_id in [
                "MIL4478_0_canonical_normalization",
                "MIL4478_1_signed_profile_guard",
                "MIL4478_2_support_dimension_branch",
                "MIL4478_4_centering_choice",
                "MIL4478_5_isotropy_or_quadrupole",
                "MIL4478_6_support_radius_bound",
            ]
        ),
        "canonical, signed, dimension, centering, quadrupole and support-bound laws are written",
    )
    add(
        "VAL4478_4_first_input_rows_staged",
        all(
            any(row.get("row_id") == row_id for row in input_rows)
            for row_id in [
                "FMI4478_0_support_zero_certificate",
                "FMI4478_1_Q_M",
                "FMI4478_2_d_eff",
                "FMI4478_3_ell_rms",
                "FMI4478_4_ell_sup",
                "FMI4478_5_dipole_or_centering",
                "FMI4478_6_quadrupole_TF",
            ]
        ),
        "first moment input rows include support zero, amplitude, dimension, radii, dipole and quadrupole",
    )
    add(
        "VAL4478_5_input_rows_remain_nonclaim",
        any("MISSING" in str(row.get("current_value")) for row in input_rows)
        and all(row.get("valid_for_claim") is False for row in input_rows),
        "input rows keep missing source values and valid_for_claim=false",
    )
    add(
        "VAL4478_6_claim_gates_block_local_GR",
        all(str(row.get("claim_allowed")).lower() == "false" for row in gates)
        and any(row.get("gate_id") == "CG4478_2_support_zero_parent_signed" and str(row.get("gate_pass")).lower() == "false" for row in gates),
        "claim gates block local-GR/R10 promotion until support zero or finite inputs are sourced",
    )
    add(
        "VAL4478_7_no_generated_claim_rows",
        all(
            str(row.get("valid_for_claim")).lower() == "false"
            for group in [sources, certificate_rows, law_rows, input_rows, gates, decisions, statuses, next_targets]
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
    add("VAL4478_8_csvs_parse", csv_ok, "; ".join(csv_detail))
    add("VAL4478_9_docs_written", FORMAL_PATH.exists() and DOC_PATH.exists(), "formal and post checkpoint docs exist")
    add(
        "VAL4478_10_claim_register_updated",
        any(row.get("claim_id") == CLAIM_ID for row in read_csv(CLAIMS_PATH)),
        "claims register contains L-320",
    )
    add(
        "VAL4478_11_spine_and_packet_updated",
        MARKER in text(SPINE_PATH) and PACKET_MARKER in text(PACKET_PATH),
        "unification spine and private packet integration contain 4478 markers",
    )
    add(
        "VAL4478_12_next_target_selected",
        bool(next_targets) and next_targets[0].get("target") == NEXT_TARGET,
        NEXT_TARGET,
    )
    add("VAL4478_13_pycache_removed", not (SCRIPT_DIR / "__pycache__").exists(), "scripts __pycache__ absent after generation")
    return validations


def main() -> None:
    sources = source_rows()
    certificate_rows = support_zero_certificate_rows()
    law_rows = first_moment_input_law_rows()
    input_rows = first_moment_input_rows()
    ledger = gate_decision_rows(NEXT_TARGET)
    gates = claim_gate_rows(sources, certificate_rows, law_rows, input_rows)
    decisions = decision_rows()
    statuses = status_rows()
    next_targets = next_rows()

    write_csv(SOURCE_REGISTER, sources)
    write_csv(SUPPORT_ZERO_CSV, certificate_rows)
    write_csv(INPUT_LAW_CSV, law_rows)
    write_csv(INPUT_ROWS_CSV, input_rows)
    write_csv(DECISION_LEDGER_CSV, ledger)
    write_csv(CLAIM_GATES_CSV, gates)
    write_csv(DECISION_CSV, decisions)
    write_csv(STATUS_CSV, statuses)
    write_csv(NEXT_CSV, next_targets)

    write_text(FORMAL_PATH, formal_body(sources, certificate_rows, law_rows, input_rows, ledger, gates, decisions, statuses, next_targets))
    write_text(DOC_PATH, post_body(sources, certificate_rows, law_rows, input_rows, ledger, gates, decisions, statuses, next_targets))
    update_claims_register()

    append_section_once(
        SPINE_PATH,
        MARKER,
        "4478 Marker Profile Support Zero Or First Inputs",
        "4478 writes the support-zero certificate: no support carrier, no readout-as-support, no Hilbert worldtube double count, and no boundary support residue. It also derives the first finite input laws for `Q_M`, `d_eff`, `ell_rms`, `ell_sup`, dipole centering and tracefree quadrupole anisotropy. The branch remains nonclaim until support zero or finite values are parent-sourced.",
    )
    append_section_once(
        PACKET_PATH,
        PACKET_MARKER,
        "4478 Packet Integration",
        "The private packet now separates profile absence from finite profile shape. If finite support survives, local projection requires `Q_M`, `d_eff`, `ell_rms`, `ell_sup`, `D_M^i` and `Q_M_TF^{ij}` rather than assuming symmetry or support scale.",
    )

    pycache = SCRIPT_DIR / "__pycache__"
    if pycache.exists():
        shutil.rmtree(pycache)

    csv_paths = [
        SOURCE_REGISTER,
        SUPPORT_ZERO_CSV,
        INPUT_LAW_CSV,
        INPUT_ROWS_CSV,
        DECISION_LEDGER_CSV,
        CLAIM_GATES_CSV,
        DECISION_CSV,
        STATUS_CSV,
        NEXT_CSV,
    ]
    validations = validate(sources, certificate_rows, law_rows, input_rows, gates, decisions, statuses, next_targets, csv_paths)
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

from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterable


ROOT = Path(__file__).resolve().parents[2]
POST = ROOT / "post-checkpoint-work"
FORMAL = ROOT / "formalization-workbench"
SOURCE_DIR = POST / "source-intake" / "mts_residuals"

CHECKPOINT = "4687"
CLAIM_ID = "L-529"
MARKER = "PPC4161_LABEL_HODGE_SUPPORT_READOUT_GATE_CURRENT_BRANCH_4687"
PACKET_MARKER = "PPC4161_PACKET_LABEL_HODGE_SUPPORT_READOUT_GATE_CURRENT_BRANCH_4687"
DECISION = "LABEL_HODGE_SUPPORT_READOUT_ZERO_OR_NORM_INSERTED_CURRENT_BRANCH_NONCLAIM"
NEXT_TARGET = "4688-Y5-R2FR-boundary-nonHilbert-zero-or-final-CXlive-norm.md"

DOC_PATH = POST / "4687-Y5-R2FR-label-Hodge-support-readout-zero-or-CXlive-next-norm.md"
FORMAL_PATH = FORMAL / "703-PPC4161-label-Hodge-support-readout-zero-or-CXlive-next-norm.md"
CLAIMS_PATH = FORMAL / "02-claims-register.csv"
SPINE_PATH = FORMAL / "07-unification-spine.md"
PACKET_PATH = FORMAL / "180-PPC4161-private-local-packet-integration.md"

CSV_4686_NEXT = SOURCE_DIR / "P8_Y5_R2FR_4686_NEXT_TARGET.csv"
CSV_4686_STATUS = SOURCE_DIR / "P8_Y5_R2FR_4686_STATUS.csv"
CSV_4599_THEOREM = SOURCE_DIR / "P8_Y5_R2FR_4599_LABEL_HODGE_SUPPORT_READOUT_ZERO_THEOREM.csv"
CSV_4599_NORM = SOURCE_DIR / "P8_Y5_R2FR_4599_CX_LABEL_HODGE_SUPPORT_READOUT_NORM.csv"
CSV_4599_BODY = SOURCE_DIR / "P8_Y5_R2FR_4599_BODY_CHARGE_ENVELOPE_LABEL_HODGE_READOUT_UPDATE.csv"
CSV_4599_NEXT_NORM = SOURCE_DIR / "P8_Y5_R2FR_4599_CXLIVE_NEXT_NORM_ROWS.csv"
CSV_4599_STATUS = SOURCE_DIR / "P8_Y5_R2FR_4599_STATUS.csv"
CSV_4599_NEXT = SOURCE_DIR / "P8_Y5_R2FR_4599_NEXT_TARGET.csv"
CSV_4599_VALIDATION = SOURCE_DIR / "P8_Y5_BRR545_4599_VALIDATION.csv"
CSV_4600_STATUS = SOURCE_DIR / "P8_Y5_R2FR_4600_STATUS.csv"
CSV_4600_NEXT = SOURCE_DIR / "P8_Y5_R2FR_4600_NEXT_TARGET.csv"
CSV_4600_VALIDATION = SOURCE_DIR / "P8_Y5_BRR545_4600_VALIDATION.csv"
FORMAL_615 = FORMAL / "615-PPC4161-label-Hodge-support-readout-zero-or-CXlive-next-norm.md"

SOURCE_REGISTER = SOURCE_DIR / "P8_Y5_R2FR_4687_SOURCE_REGISTER.csv"
THEOREM_CSV = SOURCE_DIR / "P8_Y5_R2FR_4687_LABEL_HODGE_SUPPORT_READOUT_ZERO_THEOREM.csv"
NORM_CSV = SOURCE_DIR / "P8_Y5_R2FR_4687_CX_LABEL_HODGE_SUPPORT_READOUT_NORM.csv"
BODY_CSV = SOURCE_DIR / "P8_Y5_R2FR_4687_BODY_CHARGE_ENVELOPE_LABEL_HODGE_READOUT_UPDATE.csv"
NEXT_NORM_CSV = SOURCE_DIR / "P8_Y5_R2FR_4687_CXLIVE_NEXT_NORM_ROWS.csv"
SURVIVOR_CSV = SOURCE_DIR / "P8_Y5_R2FR_4687_SURVIVOR_UPDATE.csv"
CONTROL_CSV = SOURCE_DIR / "P8_Y5_R2FR_4687_CONTROL_ROWS.csv"
DECISION_CSV = SOURCE_DIR / "P8_Y5_R2FR_4687_DECISION.csv"
STATUS_CSV = SOURCE_DIR / "P8_Y5_R2FR_4687_STATUS.csv"
NEXT_CSV = SOURCE_DIR / "P8_Y5_R2FR_4687_NEXT_TARGET.csv"
VALIDATION_CSV = SOURCE_DIR / "P8_Y5_BRR545_4687_VALIDATION.csv"


def now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace") if path.exists() else ""


def line_of(path: Path, needle: str) -> int:
    for index, line in enumerate(text(path).splitlines(), start=1):
        if needle in line:
            return index
    return 0


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fields: list[str] = []
    for row in rows:
        for field in row:
            if field not in fields:
                fields.append(field)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def table(rows: Iterable[dict[str, Any]]) -> str:
    rows = list(rows)
    if not rows:
        return ""
    headers = list(rows[0].keys())
    output = [
        "| " + " | ".join(headers) + " |",
        "| " + " | ".join("---" for _ in headers) + " |",
    ]
    for row in rows:
        output.append("| " + " | ".join(str(row.get(header, "")).replace("|", "\\|").replace("\n", " ") for header in headers) + " |")
    return "\n".join(output)


def append_once(path: Path, marker: str, body: str) -> None:
    existing = text(path)
    if marker in existing:
        return
    path.write_text(existing.rstrip() + "\n\n" + body.strip() + "\n", encoding="utf-8")


def source_rows(timestamp: str) -> list[dict[str, Any]]:
    specs = [
        ("SRC4687_00_4686_next", CSV_4686_NEXT, "4687-Y5-R2FR-label-Hodge-support-readout-zero-or-CXlive-next-norm.md", "4686 selected label/Hodge/support/readout target."),
        ("SRC4687_01_4686_status", CSV_4686_STATUS, "PPC4161_CONSTANT_STANDARD_SOURCE_WEIGHT_GATE_CURRENT_BRANCH_4686", "4686 current branch status."),
        ("SRC4687_02_4599_theorem", CSV_4599_THEOREM, "LHRS4599_4_combined", "4599 combined label/Hodge/support/readout zero theorem."),
        ("SRC4687_03_4599_norm", CSV_4599_NORM, "N4599_4_total", "4599 finite LHRS norm rows."),
        ("SRC4687_04_4599_body", CSV_4599_BODY, "BU4599_0_Csplit", "4599 body-charge envelope update."),
        ("SRC4687_05_4599_next_norm", CSV_4599_NEXT_NORM, "C4599_4_LHRS", "4599 next norm row for C_X^LHRS_live."),
        ("SRC4687_06_4599_status", CSV_4599_STATUS, "PPC4161_LABEL_HODGE_SUPPORT_READOUT_ZERO_OR_CXLIVE_NEXT_NORM_4599", "4599 status."),
        ("SRC4687_07_4599_next", CSV_4599_NEXT, "4600-Y5-R2FR-boundary-nonHilbert-zero-or-final-CXlive-norm.md", "4599 next target."),
        ("SRC4687_08_4599_validation", CSV_4599_VALIDATION, "VAL4599_OVERALL", "4599 validation passed."),
        ("SRC4687_09_4600_status", CSV_4600_STATUS, "PPC4161_BOUNDARY_NONHILBERT_ZERO_OR_FINAL_CXLIVE_NORM_4600", "4600 next rung exists."),
        ("SRC4687_10_4600_next", CSV_4600_NEXT, "4601-Y5-R2FR-CX-JX-BX-body-charge-vector-to-empirical-score-inputs.md", "4600 next target."),
        ("SRC4687_11_4600_validation", CSV_4600_VALIDATION, "VAL4600_OVERALL", "4600 validation passed."),
        ("SRC4687_12_formal615", FORMAL_615, "C_X^LHRS_live = C_X^label + C_X^Hodge + C_X^support + C_X^readout", "formal label/Hodge/support/readout gate."),
    ]
    rows = []
    for source_id, path, needle, role in specs:
        line = line_of(path, needle)
        rows.append(
            {
                "checkpoint": CHECKPOINT,
                "source_id": source_id,
                "path": str(path),
                "path_exists": path.exists(),
                "needle": needle,
                "needle_found": line > 0,
                "line_number": line,
                "role": role,
                "valid_for_claim": False,
                "timestamp_utc": timestamp,
            }
        )
    return rows


def theorem_rows(timestamp: str) -> list[dict[str, Any]]:
    data = [
        (
            "LHRS4687_0_label",
            "C_X^label",
            "source functor consumes only total variational objects T_total,J_total; source labels, constructor tags, spurions and post-readout markers are not arguments of the parent source map",
            "F_src(T_total,J_total) has no A-label or marker slot => C_X^label=0",
            "|C_X^label| <= |Delta_label_X|",
            "EXACT_CONDITIONAL_LABEL_ZERO_COUNTERMODEL_RETAINED",
        ),
        (
            "LHRS4687_1_Hodge",
            "C_X^Hodge",
            "Maxwell/current sector uses the same observed metric, coframe and orientation owner as the local source projection; no independent chi_EM, hidden constitutive tensor, readout Hodge or orientation residual is allowed",
            "Delta_Hodge_EM=0 => C_X^Hodge=0",
            "||Delta_Hodge_EM|| <= ||Delta_chi_principal||+||Delta_chi_skewon||+L||dtheta_EM||+|C_Hodge_hidden|+|C_Hodge_readout|+|Delta_orientation_flux|",
            "SAME_HODGE_ZERO_OR_NO_CANCELLATION_BOUND_READY",
        ),
        (
            "LHRS4687_2_support",
            "C_X^support",
            "source support is q-basic, regular and finite-perimeter with fixed collar, zero boundary trace, no birth/death shell, no threshold mask and no hidden side flux",
            "rho_H^tr|partial W=0 and mu_birth=0 => E_boundary_birth=0 => C_X^support=0",
            "Phi_A*(int_partialW |rho_H^tr||V_n| dSigma + ||mu_birth||_TV)/|M_H_ref| plus retained support terms",
            "REYNOLDS_ZERO_OR_SHELL_NORM_READY",
        ),
        (
            "LHRS4687_3_readout",
            "C_X^readout",
            "variation happens before readout, and readout is pure postprocessing on the solved parent quotient with no action, effective-action, coefficient or source-worldtube reentry",
            "Pi_CoeffSource([delta_parent,R_post]T_H)=0 => C_X^readout=0",
            "||C_R|| from projector/source-worldtube, EFT/prevariation, calibration feedback, material/clock response and arena kernels",
            "PURE_POSTPROCESSING_ZERO_OR_COMMUTATOR_BOUND_READY",
        ),
        (
            "LHRS4687_4_combined",
            "C_X^LHRS_live",
            "LHRS4687_0 through LHRS4687_3 all pass in the same parent branch without cancellation or fitted-calibration hiding",
            "C_X^LHRS_live=C_X^label+C_X^Hodge+C_X^support+C_X^readout=0",
            "|C_X^LHRS_live| <= |C_X^label|+|C_X^Hodge|+|C_X^support|+|C_X^readout|",
            "COMBINED_ZERO_OR_ABSOLUTE_SUM_READY",
        ),
    ]
    return [
        {
            "checkpoint": CHECKPOINT,
            "theorem_id": theorem_id,
            "target": target,
            "zero_branch": zero_branch,
            "formula": formula,
            "finite_branch": finite_branch,
            "status": status,
            "claim_allowed": False,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
        for theorem_id, target, zero_branch, formula, finite_branch, status in data
    ]


def norm_rows(timestamp: str) -> list[dict[str, Any]]:
    data = [
        ("N4687_0_label", "Delta_label_X", "source-label/constructor/spurion return norm", "WEP/R10/PPN source-label sensitivity"),
        ("N4687_1_Hodge", "Delta_Hodge_EM_X", "same-Hodge/constitutive mismatch norm", "EM/Poynting/alpha/clock source sensitivity"),
        ("N4687_2_support", "Delta_support_X", "Reynolds support-boundary/source-worldtube norm", "source mass/support/orbital/WEP kernels"),
        ("N4687_3_readout", "C_R_X", "readout/variation commutator norm", "WEP/R10/PPN/clock/orbit readout kernels"),
        ("N4687_4_total", "C_X^LHRS_live", "combined label-Hodge-support-readout live norm", "A_mem/A_h numerator input"),
    ]
    return [
        {
            "checkpoint": CHECKPOINT,
            "norm_id": norm_id,
            "symbol": symbol,
            "definition": definition,
            "finite_bound": "source-backed value or same-branch zero certificate required; no cancellation or fitted-calibration hiding",
            "observable_link": observable,
            "current_status": "ABSOLUTE_SUM_READY_VALUES_MISSING" if symbol == "C_X^LHRS_live" else "VALUE_MISSING_NONCLAIM",
            "claim_allowed": False,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
        for norm_id, symbol, definition, observable in data
    ]


def body_rows(timestamp: str) -> list[dict[str, Any]]:
    data = [
        (
            "BU4687_0_Csplit",
            "C_X live after 4687",
            "C_X^post4687 = C_X^std_weight_live + C_X^LHRS_live + C_X^boundary + C_X^nonHilbert",
            "C_X^LHRS_live=0 only if label, Hodge, support and readout zero theorems pass in the same parent branch",
            "|C_X^post4687| <= |C_X^std_weight_live|+|C_X^LHRS_live|+|C_X^boundary|+|C_X^nonHilbert|",
        ),
        (
            "BU4687_1_memory",
            "A_mem",
            "|A_mem| <= [exp(R/lambda_mem) int_body (||B_mem_eff||||R_obs|| + ||C_mem^post4687||||T|| + ||J_mem_live||) dV + ||Q_boundary_mem||]/(4*pi||Z_mem||)",
            "B_mem_eff=C_mem^post4687=J_mem_live=Q_boundary_mem=0",
            "label/Hodge/support/readout pieces now enter through C_mem^LHRS_live",
        ),
        (
            "BU4687_2_fibre",
            "A_h",
            "|A_h| <= [exp(R/lambda_h) int_body (||B_h||||R_obs|| + ||C_h^post4687||||T|| + ||J_h_live||) dV + ||Q_boundary_h||]/(4*pi||Z_h||)",
            "B_h=C_h^post4687=J_h_live=Q_boundary_h=0",
            "label/Hodge/support/readout pieces now enter through C_h^LHRS_live",
        ),
    ]
    return [
        {
            "checkpoint": CHECKPOINT,
            "update_id": update_id,
            "target": target,
            "formula": formula,
            "zero_condition": zero_condition,
            "finite_bound": finite_bound,
            "claim_allowed": False,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
        for update_id, target, formula, zero_condition, finite_bound in data
    ]


def next_norm_rows(timestamp: str) -> list[dict[str, Any]]:
    data = [
        ("C4687_0_label", "C_X^label", "source-label/constructor leakage", "prove total-source functor has no label/spurion/readout slot", "Delta_label_X"),
        ("C4687_1_Hodge", "C_X^Hodge", "Maxwell-Hodge/constitutive leakage", "prove same-Hodge visible Maxwell action and no independent chi_EM/readout/orientation residual", "Delta_Hodge_EM_X"),
        ("C4687_2_support", "C_X^support", "source-support/worldtube leakage", "prove q-basic regular zero-trace support with no shell/threshold/side flux", "Delta_support_X"),
        ("C4687_3_readout", "C_X^readout", "readout/projection commutator leakage", "prove variation-before-readout and pure postprocessing no-reentry", "C_R_X"),
        ("C4687_4_LHRS", "C_X^LHRS_live", "combined label-Hodge-support-readout live norm", "all four subrows zero in same branch", "absolute sum of C4687_0..3"),
    ]
    return [
        {
            "checkpoint": CHECKPOINT,
            "coefficient_id": coefficient_id,
            "symbol": symbol,
            "role": role,
            "derive_first": derive_first,
            "finite_fallback": finite_fallback,
            "current_status": "NEXT_NORM_ROW_READY_VALUES_MISSING" if symbol == "C_X^LHRS_live" else "MISSING_PARENT_ZERO_OR_VALUE",
            "claim_allowed": False,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
        for coefficient_id, symbol, role, derive_first, finite_fallback in data
    ]


def survivor_rows(timestamp: str) -> list[dict[str, Any]]:
    data = [
        ("SURV4687_0_LHRS", "label/Hodge/support/readout C_X rows", "zero-or-norm law imported; no numeric LHRS norms yet", NEXT_TARGET),
        ("SURV4687_1_CX_post4687", "C_X post4687 live vector", "boundary and non-Hilbert/shadow leakage remain", NEXT_TARGET),
        ("SURV4687_2_A_mem_A_h", "body-charge envelopes", "A_mem/A_h updated to use C_mem^post4687/C_h^post4687", NEXT_TARGET),
        ("SURV4687_3_standard_weight", "constant/standard/source-weight rows", "unchanged from 4686 and still explicit", "carry into final C_X vector"),
        ("SURV4687_4_global_parent", "EH/global parent/material projection", "unchanged public blockers", "keep promotion firewall active"),
    ]
    return [
        {
            "checkpoint": CHECKPOINT,
            "survivor_id": survivor_id,
            "residual_family": family,
            "status_after_4687": status,
            "next_action": action,
            "claim_allowed": False,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
        for survivor_id, family, status, action in data
    ]


def control_rows(timestamp: str) -> list[dict[str, Any]]:
    controls = [
        ("CTRL4687_0", "Do not zero label leakage unless the source functor consumes total variational objects and has no source-label, marker or spurion slot."),
        ("CTRL4687_1", "Do not zero Hodge leakage unless Maxwell, current and source projection use the same metric/coframe/orientation owner."),
        ("CTRL4687_2", "Do not zero support leakage unless source worldtubes are q-basic regular with zero trace and no birth/death shell or threshold mask."),
        ("CTRL4687_3", "Do not zero readout leakage unless variation strictly precedes pure postprocessing and the readout cannot reenter the action or source coefficient."),
        ("CTRL4687_4", "A_mem/A_h must carry C_X^LHRS_live until every LHRS branch is zeroed or source-valued."),
        ("CTRL4687_5", "Next target is boundary/non-Hilbert leakage, not public local-GR scoring."),
    ]
    return [
        {
            "checkpoint": CHECKPOINT,
            "control_id": control_id,
            "rule": rule,
            "status": "ACTIVE",
            "claim_allowed": False,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
        for control_id, rule in controls
    ]


def decision_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "decision": DECISION,
            "summary": "4687 imports the 4599 label/Hodge/support/readout gate into the current branch. These four routes vanish only if source labels are forgotten, Maxwell uses the same observed Hodge owner, support is q-basic regular with no shell or side flux, and readout is pure post-variation postprocessing in the same parent branch. Otherwise C_X^LHRS_live remains an explicit norm inside A_mem/A_h.",
            "next_target": NEXT_TARGET,
            "public_claim": False,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
    ]


def status_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "marker": MARKER,
            "claim_id": CLAIM_ID,
            "decision": DECISION,
            "derived": "source-label zero-or-norm law; same-Hodge/constitutive zero-or-norm law; support/worldtube zero-or-Reynolds norm law; readout/projection commutator zero-or-norm law; C_X^post4687 and A_mem/A_h envelope update",
            "not_derived": "parent-signed label/Hodge/support/readout zero in one branch; numeric LHRS norm values; boundary/non-Hilbert C_X rows; local-GR/R10/PPN scoring",
            "claim_status": "PRIVATE_NONCLAIM",
            "local_GR_public_claim": False,
            "next_target": NEXT_TARGET,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
    ]


def next_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "next_id": "NT4687_0",
            "target": NEXT_TARGET,
            "reason": "After label/Hodge/support/readout are isolated, the remaining C_X live family is boundary plus non-Hilbert/shadow current leakage.",
            "derive_first": "prove boundary neutrality and no non-Hilbert/shadow source covector in the same parent branch",
            "fallback": "fill final C_X boundary/non-Hilbert norm row and insert into A_mem/A_h",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
    ]


def write_documents(rows: dict[str, list[dict[str, Any]]]) -> None:
    body = f"""# 4687 - Y5/R2FR Label/Hodge/Support/Readout Zero Or C_X Live Next Norm

Marker: `{MARKER}`

Decision: `{DECISION}`

## Result

4687 imports the label/Hodge/support/readout gate:

```text
C_X^post4687 = C_X^std_weight_live + C_X^LHRS_live
             + C_X^boundary + C_X^nonHilbert.

C_X^LHRS_live = C_X^label + C_X^Hodge + C_X^support + C_X^readout.
```

The LHRS block vanishes only in one same parent branch:

```text
label-forgetting + same Maxwell-Hodge owner + q-basic regular support
+ pure post-variation readout => C_X^LHRS_live=0.
```

Otherwise `C_X^LHRS_live` enters `A_mem/A_h` as an explicit finite norm. No local-GR, R10 or PPN claim is promoted here.

## Source Register

{table(rows["sources"])}

## Label / Hodge / Support / Readout Zero Theorem

{table(rows["theorems"])}

## LHRS Norm Rows

{table(rows["norms"])}

## Body-Charge Envelope Update

{table(rows["body"])}

## C_X Live Next Norm Rows

{table(rows["next_norms"])}

## Survivor Update

{table(rows["survivors"])}

## Controls

{table(rows["controls"])}

## Decision

{table(rows["decisions"])}

## Status

{table(rows["statuses"])}

## Next Target

{table(rows["next"])}

## Validation

{table(rows.get("validations", []))}
"""
    DOC_PATH.write_text(body, encoding="utf-8")
    FORMAL_PATH.write_text(body.replace("# 4687 - Y5/R2FR", "# 703 - PPC4161"), encoding="utf-8")


def update_registers(timestamp: str) -> None:
    claims = read_csv(CLAIMS_PATH)
    if not any(row.get("claim_id") == CLAIM_ID for row in claims):
        fieldnames = list(claims[0].keys())
        row = {field: "" for field in fieldnames}
        row.update(
            {
                "claim_id": CLAIM_ID,
                "domain": "local_gr_empirical_interface",
                "claim": "4687 imports the label/Hodge/support/readout gate into the current branch. C_X^LHRS_live vanishes only when label-forgetting, same Maxwell-Hodge owner, q-basic regular support and pure post-variation readout all hold in the same parent branch; otherwise it remains an explicit norm in A_mem/A_h.",
                "current_evidence": "Generated source register, LHRS zero theorem, norm rows, body-charge envelope update, C_X live next norm rows, survivor update, controls, decision, status, next target and validation.",
                "status": DECISION.lower(),
                "next_test": NEXT_TARGET,
                "key_risk": "Hidden source-label, Hodge/constitutive, support/worldtube or readout reentry coupling can masquerade as a local-GR residual.",
                "sector": "local_gr",
                "evidence": str(DOC_PATH),
                "next_action": NEXT_TARGET,
            }
        )
        with CLAIMS_PATH.open("a", encoding="utf-8", newline="") as handle:
            writer = csv.DictWriter(handle, fieldnames=fieldnames)
            writer.writerow(row)

    append_once(
        SPINE_PATH,
        MARKER,
        f"""## Local GR Parent-Derivation Update - Current Label/Hodge/Support/Readout Gate

Marker: `{MARKER}`

4687 imports the LHRS zero-or-norm law into the current branch:

```text
C_X^post4687 = C_X^std_weight_live + C_X^LHRS_live
             + C_X^boundary + C_X^nonHilbert.
```

The remaining local-matter trace coupling cannot be called zero unless label, Hodge, support and readout reentry are all closed in the same parent branch. Otherwise `C_X^LHRS_live` remains a visible amplitude input to `A_mem/A_h`.

- claim id: `{CLAIM_ID}`
- checkpoint: `{DOC_PATH.name}`
- next: `{NEXT_TARGET}`
- timestamp_utc: `{timestamp}`
""",
    )
    append_once(
        PACKET_PATH,
        PACKET_MARKER,
        f"""## PPC4161 Packet Addendum - Current Label/Hodge/Support/Readout Gate

Marker: `{PACKET_MARKER}`

The packet now carries `C_X^LHRS_live` explicitly. Label, Hodge, support and readout terms may be removed only by a same-branch parent zero certificate; otherwise they remain finite norm rows for local tests.

- theorem csv: `{THEOREM_CSV.name}`
- norm csv: `{NORM_CSV.name}`
- next: `{NEXT_TARGET}`
""",
    )


def validation_rows(rows: dict[str, list[dict[str, Any]]], csv_paths: list[Path]) -> list[dict[str, Any]]:
    checks: list[tuple[str, bool, str]] = [
        ("VAL4687_0_sources_exist", all(row["path_exists"] for row in rows["sources"]), "all source-register paths exist"),
        ("VAL4687_1_needles_found", all(row["needle_found"] for row in rows["sources"]), "all source-register needles found"),
        ("VAL4687_2_four_zero_branches", len(rows["theorems"]) == 5 and all(row["target"] for row in rows["theorems"]), "four LHRS zero branches plus combined row present"),
        ("VAL4687_3_norm_rows", any(row["symbol"] == "C_X^LHRS_live" for row in rows["norms"]), "LHRS finite norm total present"),
        ("VAL4687_4_body_update", any("C_X^post4687" in row["formula"] for row in rows["body"]), "A_mem/A_h post4687 update present"),
        ("VAL4687_5_next_norm_rows", any(row["symbol"] == "C_X^LHRS_live" for row in rows["next_norms"]), "C_X live next norm rows present"),
        ("VAL4687_6_next_boundary_nonHilbert", rows["next"][0]["target"] == NEXT_TARGET, "next boundary/non-Hilbert target selected"),
        ("VAL4687_7_claim_row_exists", CLAIM_ID in text(CLAIMS_PATH), "claims register contains L-529"),
        ("VAL4687_8_formal_doc", FORMAL_PATH.exists() and MARKER in text(FORMAL_PATH), "formal doc exists with marker"),
        ("VAL4687_9_post_doc", DOC_PATH.exists() and MARKER in text(DOC_PATH), "post checkpoint exists with marker"),
        ("VAL4687_10_spine_marker", MARKER in text(SPINE_PATH), "spine marker written"),
        ("VAL4687_11_packet_marker", PACKET_MARKER in text(PACKET_PATH), "packet marker written"),
    ]
    for path in csv_paths:
        try:
            parsed = read_csv(path)
            checks.append((f"VAL4687_csv_{path.stem}", bool(parsed), f"{path} parses with {len(parsed)} rows"))
        except Exception as exc:
            checks.append((f"VAL4687_csv_{path.stem}", False, repr(exc)))
    checks.append(("VAL4687_12_no_claim_rows_true", all(not row.get("valid_for_claim", False) for group in rows.values() for row in group), "generated rows keep valid_for_claim false"))
    checks.append(("VAL4687_13_pycache_absent", not (POST / "scripts" / "__pycache__").exists(), "scripts __pycache__ absent"))
    overall = all(passed for _, passed, _ in checks)
    checks.append(("VAL4687_OVERALL", overall, "PASS" if overall else "FAIL"))
    return [{"checkpoint": CHECKPOINT, "check_id": check_id, "passed": passed, "detail": detail, "valid_for_claim": False} for check_id, passed, detail in checks]


def main() -> None:
    timestamp = now()
    rows = {
        "sources": source_rows(timestamp),
        "theorems": theorem_rows(timestamp),
        "norms": norm_rows(timestamp),
        "body": body_rows(timestamp),
        "next_norms": next_norm_rows(timestamp),
        "survivors": survivor_rows(timestamp),
        "controls": control_rows(timestamp),
        "decisions": decision_rows(timestamp),
        "statuses": status_rows(timestamp),
        "next": next_rows(timestamp),
    }
    csv_map = {
        SOURCE_REGISTER: rows["sources"],
        THEOREM_CSV: rows["theorems"],
        NORM_CSV: rows["norms"],
        BODY_CSV: rows["body"],
        NEXT_NORM_CSV: rows["next_norms"],
        SURVIVOR_CSV: rows["survivors"],
        CONTROL_CSV: rows["controls"],
        DECISION_CSV: rows["decisions"],
        STATUS_CSV: rows["statuses"],
        NEXT_CSV: rows["next"],
    }
    for path, data in csv_map.items():
        write_csv(path, data)
    write_documents(rows)
    update_registers(timestamp)
    cache = POST / "scripts" / "__pycache__"
    if cache.exists():
        shutil.rmtree(cache)
    rows["validations"] = validation_rows(rows, list(csv_map))
    write_csv(VALIDATION_CSV, rows["validations"])
    write_documents(rows)
    print(f"{CHECKPOINT} complete: {DOC_PATH}")
    print(f"validation: {VALIDATION_CSV}")


if __name__ == "__main__":
    main()

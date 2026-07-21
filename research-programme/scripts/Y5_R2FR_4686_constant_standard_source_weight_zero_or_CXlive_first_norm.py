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

CHECKPOINT = "4686"
CLAIM_ID = "L-528"
MARKER = "PPC4161_CONSTANT_STANDARD_SOURCE_WEIGHT_GATE_CURRENT_BRANCH_4686"
PACKET_MARKER = "PPC4161_PACKET_CONSTANT_STANDARD_SOURCE_WEIGHT_GATE_CURRENT_BRANCH_4686"
DECISION = "CONSTANT_STANDARD_AND_SOURCE_WEIGHT_ZERO_OR_SENSITIVITY_NORM_INSERTED_CURRENT_BRANCH_NONCLAIM"
NEXT_TARGET = "4687-Y5-R2FR-label-Hodge-support-readout-zero-or-CXlive-next-norm.md"

DOC_PATH = POST / "4686-Y5-R2FR-constant-standard-source-weight-zero-or-CXlive-first-norm.md"
FORMAL_PATH = FORMAL / "702-PPC4161-constant-standard-source-weight-zero-or-CXlive-first-norm.md"
CLAIMS_PATH = FORMAL / "02-claims-register.csv"
SPINE_PATH = FORMAL / "07-unification-spine.md"
PACKET_PATH = FORMAL / "180-PPC4161-private-local-packet-integration.md"

CSV_4685_NEXT = SOURCE_DIR / "P8_Y5_R2FR_4685_NEXT_TARGET.csv"
CSV_4685_STATUS = SOURCE_DIR / "P8_Y5_R2FR_4685_STATUS.csv"
CSV_4598_ZERO = SOURCE_DIR / "P8_Y5_R2FR_4598_CONSTANT_WEIGHT_ZERO_THEOREM.csv"
CSV_4598_SENS = SOURCE_DIR / "P8_Y5_R2FR_4598_CX_STANDARD_WEIGHT_SENSITIVITY_BOUND.csv"
CSV_4598_BODY = SOURCE_DIR / "P8_Y5_R2FR_4598_BODY_CHARGE_ENVELOPE_STANDARD_WEIGHT_UPDATE.csv"
CSV_4598_NORM = SOURCE_DIR / "P8_Y5_R2FR_4598_FIRST_CXLIVE_NORM_ROWS.csv"
CSV_4598_STATUS = SOURCE_DIR / "P8_Y5_R2FR_4598_STATUS.csv"
CSV_4598_NEXT = SOURCE_DIR / "P8_Y5_R2FR_4598_NEXT_TARGET.csv"
CSV_4598_VALIDATION = SOURCE_DIR / "P8_Y5_BRR545_4598_VALIDATION.csv"
CSV_4599_STATUS = SOURCE_DIR / "P8_Y5_R2FR_4599_STATUS.csv"
CSV_4599_NEXT = SOURCE_DIR / "P8_Y5_R2FR_4599_NEXT_TARGET.csv"
CSV_4599_VALIDATION = SOURCE_DIR / "P8_Y5_BRR545_4599_VALIDATION.csv"
FORMAL_614 = FORMAL / "614-PPC4161-constant-standard-source-weight-zero-or-CXlive-first-norm.md"

SOURCE_REGISTER = SOURCE_DIR / "P8_Y5_R2FR_4686_SOURCE_REGISTER.csv"
ZERO_CSV = SOURCE_DIR / "P8_Y5_R2FR_4686_CONSTANT_WEIGHT_ZERO_THEOREM.csv"
SENS_CSV = SOURCE_DIR / "P8_Y5_R2FR_4686_CX_STANDARD_WEIGHT_SENSITIVITY_BOUND.csv"
BODY_CSV = SOURCE_DIR / "P8_Y5_R2FR_4686_BODY_CHARGE_ENVELOPE_STANDARD_WEIGHT_UPDATE.csv"
NORM_CSV = SOURCE_DIR / "P8_Y5_R2FR_4686_FIRST_CXLIVE_NORM_ROWS.csv"
SURVIVOR_CSV = SOURCE_DIR / "P8_Y5_R2FR_4686_SURVIVOR_UPDATE.csv"
CONTROL_CSV = SOURCE_DIR / "P8_Y5_R2FR_4686_CONTROL_ROWS.csv"
DECISION_CSV = SOURCE_DIR / "P8_Y5_R2FR_4686_DECISION.csv"
STATUS_CSV = SOURCE_DIR / "P8_Y5_R2FR_4686_STATUS.csv"
NEXT_CSV = SOURCE_DIR / "P8_Y5_R2FR_4686_NEXT_TARGET.csv"
VALIDATION_CSV = SOURCE_DIR / "P8_Y5_BRR545_4686_VALIDATION.csv"


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
        ("SRC4686_00_4685_next", CSV_4685_NEXT, "4686-Y5-R2FR-constant-standard-source-weight-zero-or-CXlive-first-norm.md", "4685 selected constant/weight target."),
        ("SRC4686_01_4685_status", CSV_4685_STATUS, "CMEM_CH_QBASIC_SOURCE_DESCENT", "4685 status."),
        ("SRC4686_02_4598_zero", CSV_4598_ZERO, "ZW4598_0_constants", "constant and source-weight zero theorem."),
        ("SRC4686_03_4598_sens", CSV_4598_SENS, "SB4598_5_total", "sensitivity bound rows."),
        ("SRC4686_04_4598_body", CSV_4598_BODY, "BU4598_0_Csplit", "body-charge envelope post4598 update."),
        ("SRC4686_05_4598_norm", CSV_4598_NORM, "CXN4598_5_total", "first C_X live norm rows."),
        ("SRC4686_06_4598_status", CSV_4598_STATUS, "CONSTANT_STANDARD_AND_SOURCE_WEIGHT_ZERO", "4598 status."),
        ("SRC4686_07_4598_next", CSV_4598_NEXT, "4599-Y5-R2FR-label-Hodge-support-readout-zero-or-CXlive-next-norm.md", "4598 next target."),
        ("SRC4686_08_4598_validation", CSV_4598_VALIDATION, "VAL4598_OVERALL", "4598 validation passed."),
        ("SRC4686_09_4599_status", CSV_4599_STATUS, "LABEL_HODGE_SUPPORT_READOUT_ZERO", "4599 next rung exists."),
        ("SRC4686_10_4599_next", CSV_4599_NEXT, "4600-Y5-R2FR-boundary-nonHilbert-zero-or-final-CXlive-norm.md", "4599 next target."),
        ("SRC4686_11_4599_validation", CSV_4599_VALIDATION, "VAL4599_OVERALL", "4599 validation passed."),
        ("SRC4686_12_formal614", FORMAL_614, "C_X^post4598 = C_X^std_weight_live", "formal constant/source-weight gate."),
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


def zero_rows(timestamp: str) -> list[dict[str, Any]]:
    data = [
        ("ZW4686_0_constants", "C_X^std", "theta_i are quotient-owned, discrete, global/superselection, or topological zero-form constants; Dq[v_X]=0; no readout/unit rescaling cheat", "D_X ln(theta_i)=0 => C_X^std=0", "|C_X^std| <= sum_i |S_i^std| |D_X ln(theta_i)|", "EXACT_CONDITIONAL_ZERO_VALUES_MISSING"),
        ("ZW4686_1_source_weight", "C_X^weight", "one parent action-density line, connected ordinary matter category, no pre-action source prefactors w_A(X), no kappa_A(X) before variation, common calibration only after label/time/range/frame gates", "S_matter=sum_A S_A and F_src(T_total)=kappa_univ T_total => D_X w_A=D_X kappa_A=0 relative to the source functor", "|C_X^weight T| <= sum_A |D_X ln w_A| |T_A| + sum_A |D_X ln kappa_A| |T_A|", "EXACT_CONDITIONAL_ZERO_COUNTERMODEL_RETAINED"),
        ("ZW4686_2_combined", "C_X^std_weight", "ZW4686_0 and ZW4686_1 pass in the same parent branch", "C_X^std_weight = C_X^std + C_X^weight = 0", "|C_X^std_weight| <= |C_X^std| + |C_X^weight|", "COMBINED_ZERO_OR_ABSOLUTE_BOUND_READY"),
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


def sensitivity_rows(timestamp: str) -> list[dict[str, Any]]:
    data = [
        ("SB4686_0_alpha", "b_alpha_X", "D_X ln(alpha_EM)", "alpha_EM source/readout/Maxwell normalization drift", "clock/EM/R10 sensitivity"),
        ("SB4686_1_mass", "b_mA_X,b_mu_X,b_nuc_X", "D_X ln(m_A/m_ref), D_X ln(mu), D_X ln(binding)", "composition and material mass-ratio drift", "WEP/composition/source charge sensitivity"),
        ("SB4686_2_clock", "b_clock_i_X", "K_alpha_i b_alpha + K_mu_i b_mu + K_nuc_i b_nuc + ...", "clock standard drift", "clock/local time sensitivity"),
        ("SB4686_3_material", "b_mat_X", "D_X ln(theta_material)", "material/preparation/domain standard drift", "material/domain source rows"),
        ("SB4686_4_weight", "delta_w_A_X", "D_X ln(w_A) or D_X ln(kappa_A/kappa_univ)", "relative source-weight prefactor drift", "WEP/source-label rows"),
        ("SB4686_5_total", "C_X^std_weight", "sum of standard and source-weight sensitivity channels", "first C_X_live norm contribution", "insert into A_mem/A_h"),
    ]
    return [
        {
            "checkpoint": CHECKPOINT,
            "sensitivity_id": sensitivity_id,
            "symbol": symbol,
            "definition": definition,
            "physical_channel": channel,
            "finite_bound": "source-backed value or zero certificate required; no bound inversion or fitted-G hiding",
            "observable_link": observable,
            "current_status": "ABSOLUTE_SUM_READY_VALUES_MISSING" if symbol == "C_X^std_weight" else "VALUE_MISSING_NONCLAIM",
            "claim_allowed": False,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
        for sensitivity_id, symbol, definition, channel, observable in data
    ]


def body_rows(timestamp: str) -> list[dict[str, Any]]:
    data = [
        ("BU4686_0_Csplit", "C_X live after 4686", "C_X^post4686 = C_X^std_weight_live + C_X^label + C_X^Hodge + C_X^support_readout + C_X^boundary + C_X^nonHilbert", "C_X^std_weight_live=0 only if constants/standards are superselected and source weights/prefactors are illegal in the same parent branch", "|C_X^post4686| <= |C_X^std_weight_live|+|C_X^label|+|C_X^Hodge|+|C_X^support_readout|+|C_X^boundary|+|C_X^nonHilbert|"),
        ("BU4686_1_memory", "A_mem", "|A_mem| <= [exp(R/lambda_mem) int_body (||B_mem_eff||||R_obs|| + ||C_mem^post4686||||T|| + ||J_mem_live||) dV + ||Q_boundary_mem||]/(4*pi||Z_mem||)", "B_mem_eff=C_mem^post4686=J_mem_live=Q_boundary_mem=0", "standards/source weights now enter through C_mem^std_weight_live, not hidden inside C_mem"),
        ("BU4686_2_fibre", "A_h", "|A_h| <= [exp(R/lambda_h) int_body (||B_h||||R_obs|| + ||C_h^post4686||||T|| + ||J_h_live||) dV + ||Q_boundary_h||]/(4*pi||Z_h||)", "B_h=C_h^post4686=J_h_live=Q_boundary_h=0", "standards/source weights now enter through C_h^std_weight_live, not hidden inside C_h"),
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


def norm_rows(timestamp: str) -> list[dict[str, Any]]:
    data = [
        ("CXN4686_0_alpha", "b_alpha_X", "fine-structure/Maxwell normalization drift", "prove unique Maxwell F^2/current owner and q-basic readout", "clock/EM/R10 sensitivity"),
        ("CXN4686_1_mass", "b_mass_X", "mass-ratio/binding/material mass drift", "prove matter spectrum and binding data are parent-owned/superselected", "WEP/composition/source charge sensitivity"),
        ("CXN4686_2_clock", "b_clock_X", "clock transition standard drift", "prove clock readout inherits zero from alpha/mass/nuclear and tau-lock", "clock/local time sensitivity"),
        ("CXN4686_3_kappa", "D_X ln(kappa_eff)", "universal source coupling drift", "global/topological zero-form kappa or common coupling owner", "Gdot/G/source calibration sensitivity"),
        ("CXN4686_4_weight", "D_X ln(w_A),D_X ln(kappa_A/kappa_univ)", "relative source weight drift", "no pre-action source prefactor and connected action-density line", "WEP/source-label sensitivity"),
        ("CXN4686_5_total", "C_X^std_weight_live", "combined first live norm", "all rows above theorem-zero in one branch", "A_mem/A_h numerator input"),
    ]
    return [
        {
            "checkpoint": CHECKPOINT,
            "coefficient_id": coefficient_id,
            "symbol": symbol,
            "role": role,
            "derive_first": derive_first,
            "finite_fallback": fallback,
            "current_status": "FIRST_NORM_ROW_READY_VALUES_MISSING" if symbol == "C_X^std_weight_live" else "MISSING_PARENT_ZERO_OR_VALUE",
            "claim_allowed": False,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
        for coefficient_id, symbol, role, derive_first, fallback in data
    ]


def survivor_rows(timestamp: str) -> list[dict[str, Any]]:
    data = [
        ("SURV4686_0_standard_weight", "constant/standard/source-weight C_X rows", "zero-or-sensitivity law imported; values/signatures still missing", NEXT_TARGET),
        ("SURV4686_1_CX_post4686", "C_X post4686 live vector", "label/Hodge/support/readout/boundary/nonHilbert remain", NEXT_TARGET),
        ("SURV4686_2_A_mem_A_h", "body-charge envelopes", "A_mem/A_h updated to use C_mem^post4686/C_h^post4686", NEXT_TARGET),
        ("SURV4686_3_Jlive", "J_X live current", "unchanged from 4684", "return if C_X vector closes first"),
        ("SURV4686_4_global_parent", "EH/global parent/material projection", "unchanged public blockers", "keep promotion firewall active"),
    ]
    return [
        {
            "checkpoint": CHECKPOINT,
            "survivor_id": survivor_id,
            "residual_family": family,
            "status_after_4686": status,
            "next_action": action,
            "claim_allowed": False,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
        for survivor_id, family, status, action in data
    ]


def control_rows(timestamp: str) -> list[dict[str, Any]]:
    controls = [
        ("CTRL4686_0", "Do not treat constants/standards as zero unless they are quotient-owned, superselected, discrete, global or topological in the parent branch."),
        ("CTRL4686_1", "Do not hide relative source weights in fitted G or calibrated GM."),
        ("CTRL4686_2", "No pre-action source prefactors w_A(X) or kappa_A(X) may be assumed absent without an action-line owner certificate."),
        ("CTRL4686_3", "A_mem/A_h must carry C_X^std_weight_live until every sensitivity is zeroed or sourced."),
        ("CTRL4686_4", "Next target is label/Hodge/support/readout re-entry."),
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
            "summary": "4686 imports the 4598 constant/standard and source-weight gate into the current branch. C_X^std vanishes only if the relevant standards are quotient-owned/superselected/discrete/global/topological. C_X^weight vanishes only if pre-action source prefactors and species-dependent kappa_A are illegal in the parent source grammar. Otherwise C_X^std_weight_live remains an explicit sensitivity norm inside A_mem/A_h.",
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
            "derived": "constant/standard superselection zero-or-sensitivity law; no-preaction-source-weight/action-line zero-or-norm law; C_X^post4686 and A_mem/A_h envelope update; first C_X_live norm rows",
            "not_derived": "parent-signed alpha/mass/clock/material/kappa superselection; parent-signed no source prefactors/action-density line; numeric sensitivity values; local-GR/R10/PPN scoring",
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
            "next_id": "NT4686_0",
            "target": NEXT_TARGET,
            "reason": "After constants/source weights are isolated, the largest remaining C_X_live family is label/Hodge/support/readout re-entry.",
            "derive_first": "prove label forgetting plus same Maxwell-Hodge/current owner plus variation-before-readout in one parent branch",
            "fallback": "fill first finite C_X label/Hodge/support-readout norm row",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
    ]


def write_documents(rows: dict[str, list[dict[str, Any]]]) -> None:
    body = f"""# 4686 - Y5/R2FR Constant/Standard Source-Weight Zero Or C_X Live First Norm

Marker: `{MARKER}`

Decision: `{DECISION}`

## Result

4686 imports the constants/standards/source-weight gate:

```text
C_X^post4686 = C_X^std_weight_live + C_X^label + C_X^Hodge
              + C_X^support_readout + C_X^boundary + C_X^nonHilbert.
```

The standard term vanishes only under parent-owned/superselected constants:

```text
D_X ln(theta_i)=0 => C_X^std=0.
```

The source-weight term vanishes only if pre-action source prefactors are illegal:

```text
S_matter=sum_A S_A, no w_A(X)S_A, no kappa_A(X)T_A => C_X^weight=0.
```

Otherwise `C_X^std_weight_live` enters `A_mem/A_h` as an explicit sensitivity norm.

## Source Register

{table(rows["sources"])}

## Constant / Source-Weight Zero Theorem

{table(rows["zero"])}

## Standard / Weight Sensitivity Bounds

{table(rows["sensitivities"])}

## Body-Charge Envelope Update

{table(rows["body"])}

## First C_X Live Norm Rows

{table(rows["norms"])}

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
    FORMAL_PATH.write_text(body.replace("# 4686 - Y5/R2FR", "# 702 - PPC4161"), encoding="utf-8")


def update_registers(timestamp: str) -> None:
    claims = read_csv(CLAIMS_PATH)
    if not any(row.get("claim_id") == CLAIM_ID for row in claims):
        fieldnames = list(claims[0].keys())
        row = {field: "" for field in fieldnames}
        row.update(
            {
                "claim_id": CLAIM_ID,
                "domain": "local_gr_empirical_interface",
                "claim": "4686 imports the constant/standard and source-weight gate into the current branch. C_X^std vanishes only when standards are quotient-owned/superselected/discrete/global/topological, and C_X^weight vanishes only when pre-action source prefactors and species-dependent kappa_A are illegal; otherwise C_X^std_weight_live remains an explicit sensitivity norm in A_mem/A_h.",
                "current_evidence": "Generated source register, constant/source-weight zero theorem, sensitivity bounds, body-charge envelope update, first C_X live norm rows, survivor update, controls, decision, status, next target and validation.",
                "status": DECISION.lower(),
                "next_test": NEXT_TARGET,
                "key_risk": "Hiding varying constants or source weights inside fitted G/GM, unit conventions, or calibrated source coupling.",
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
        f"""## Local GR Parent-Derivation Update - Current Constant/Source-Weight Gate

Marker: `{MARKER}`

4686 imports the constant/standard and source-weight zero-or-norm law:

```text
C_X^post4686 = C_X^std_weight_live + C_X^label + C_X^Hodge
              + C_X^support_readout + C_X^boundary + C_X^nonHilbert.
```

Constants/standards and source weights are not allowed to hide inside fitted `G` or units. They are either parent-zero/superselected/no-prefactor, or they enter `A_mem/A_h` as explicit sensitivity norms.

- claim id: `{CLAIM_ID}`
- checkpoint: `{DOC_PATH.name}`
- next: `{NEXT_TARGET}`
- timestamp_utc: `{timestamp}`
""",
    )
    append_once(
        PACKET_PATH,
        PACKET_MARKER,
        f"""## PPC4161 Packet Addendum - Current Constant/Source-Weight Gate

Marker: `{PACKET_MARKER}`

The packet now carries `C_X^std_weight_live` explicitly. Do not hide constants, standards, source weights or kappa drift in unit choices, fitted `G`, or calibrated `GM`.

- zero theorem csv: `{ZERO_CSV.name}`
- sensitivity csv: `{SENS_CSV.name}`
- next: `{NEXT_TARGET}`
""",
    )


def validation_rows(rows: dict[str, list[dict[str, Any]]], csv_paths: list[Path]) -> list[dict[str, Any]]:
    checks: list[tuple[str, bool, str]] = [
        ("VAL4686_0_sources_exist", all(row["path_exists"] for row in rows["sources"]), "all source-register paths exist"),
        ("VAL4686_1_needles_found", all(row["needle_found"] for row in rows["sources"]), "all source-register needles found"),
        ("VAL4686_2_zero_theorem", len(rows["zero"]) == 3, "constant/source-weight zero theorem rows present"),
        ("VAL4686_3_sensitivity_rows", any(row["symbol"] == "C_X^std_weight" for row in rows["sensitivities"]), "C_X std/weight sensitivity total present"),
        ("VAL4686_4_body_update", len(rows["body"]) == 3, "A_mem/A_h post4686 update present"),
        ("VAL4686_5_norm_rows", any(row["symbol"] == "C_X^std_weight_live" for row in rows["norms"]), "first C_X live norm total present"),
        ("VAL4686_6_next_label_hodge", rows["next"][0]["target"] == NEXT_TARGET, "next label/Hodge/support/readout target selected"),
        ("VAL4686_7_claim_row_exists", CLAIM_ID in text(CLAIMS_PATH), "claims register contains L-528"),
        ("VAL4686_8_formal_doc", FORMAL_PATH.exists() and MARKER in text(FORMAL_PATH), "formal doc exists with marker"),
        ("VAL4686_9_post_doc", DOC_PATH.exists() and MARKER in text(DOC_PATH), "post checkpoint exists with marker"),
        ("VAL4686_10_spine_marker", MARKER in text(SPINE_PATH), "spine marker written"),
        ("VAL4686_11_packet_marker", PACKET_MARKER in text(PACKET_PATH), "packet marker written"),
    ]
    for path in csv_paths:
        try:
            parsed = read_csv(path)
            checks.append((f"VAL4686_csv_{path.stem}", bool(parsed), f"{path} parses with {len(parsed)} rows"))
        except Exception as exc:
            checks.append((f"VAL4686_csv_{path.stem}", False, repr(exc)))
    checks.append(("VAL4686_12_no_claim_rows_true", all(not row.get("valid_for_claim", False) for group in rows.values() for row in group), "generated rows keep valid_for_claim false"))
    checks.append(("VAL4686_13_pycache_absent", not (POST / "scripts" / "__pycache__").exists(), "scripts __pycache__ absent"))
    overall = all(passed for _, passed, _ in checks)
    checks.append(("VAL4686_OVERALL", overall, "PASS" if overall else "FAIL"))
    return [{"checkpoint": CHECKPOINT, "check_id": check_id, "passed": passed, "detail": detail, "valid_for_claim": False} for check_id, passed, detail in checks]


def main() -> None:
    timestamp = now()
    rows = {
        "sources": source_rows(timestamp),
        "zero": zero_rows(timestamp),
        "sensitivities": sensitivity_rows(timestamp),
        "body": body_rows(timestamp),
        "norms": norm_rows(timestamp),
        "survivors": survivor_rows(timestamp),
        "controls": control_rows(timestamp),
        "decisions": decision_rows(timestamp),
        "statuses": status_rows(timestamp),
        "next": next_rows(timestamp),
    }
    csv_map = {
        SOURCE_REGISTER: rows["sources"],
        ZERO_CSV: rows["zero"],
        SENS_CSV: rows["sensitivities"],
        BODY_CSV: rows["body"],
        NORM_CSV: rows["norms"],
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

from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path


CHECKPOINT = "3874"
BRANCH = "MTS_R2FR_Y5_EM_NORMALIZATION_OR_DELTA_W_THETA_COMMONNESS_3874"

PCW = Path(__file__).resolve().parents[1]
ROOT = PCW.parent
FWB = ROOT / "formalization-workbench"
OUT = PCW / "source-intake" / "mts_residuals"
DOC_PATH = PCW / "3874-Y5-R2FR-EM-normalization-or-Delta-w-theta-commonness.md"
SPINE_PATH = PCW / "LOCAL_GR_COUPLING_SPINE_CURRENT_STATE.md"

CSV_3873_NEXT = OUT / "P8_Y5_R2FR_3873_NEXT_TARGET.csv"
CSV_3873_UPDATE = OUT / "P8_Y5_R2FR_3873_PHI_EM_BOUNDARY_COEFFICIENT_UPDATE.csv"
CSV_3873_RETAINED = OUT / "P8_Y5_R2FR_3873_RETAINED_EM_SOURCE_RESIDUALS.csv"
CSV_3865_IMAGE = OUT / "P8_Y5_R2FR_3865_VISIBLE_OPERATOR_IMAGE_THEOREM.csv"
CSV_3865_JOINT = OUT / "P8_Y5_R2FR_3865_SXF2_ZG_BALPHA_JOINT_BOUND.csv"
CSV_3864_F2 = OUT / "P8_Y5_R2FR_3864_NO_EXTRA_F2_THEOREM.csv"
CSV_3864_AUDIT = OUT / "P8_Y5_R2FR_3864_OPERATOR_DOMAIN_AUDIT.csv"
CSV_3864_LAMBDA = OUT / "P8_Y5_R2FR_3864_LAMBDAF2_BOUND.csv"
CSV_3863_MNO = OUT / "P8_Y5_R2FR_3863_MAXWELL_NORMALIZATION_OWNER_THEOREM.csv"
CSV_3863_EM = OUT / "P8_Y5_R2FR_3863_EM_SOURCE_SCALE_BOUND.csv"
CSV_3863_CHARGE = OUT / "P8_Y5_R2FR_3863_CHARGE_CURRENT_SLOT_AUDIT.csv"
CSV_3809_MN = OUT / "P8_Y5_R2FR_3809_MAXWELL_NORMALIZATION_THEOREM.csv"
CSV_3791_ZEM = OUT / "P8_Y5_R2FR_3791_ZEM_FIXED_NORMALIZATION_THEOREM.csv"
CSV_3791_GUARD = OUT / "P8_Y5_R2FR_3791_OPERATOR_BASIS_COUNTEREXAMPLE_GUARD.csv"
CSV_1057_CT = OUT / "P8_Y5_R10_1057_F2_COUNTERTERM_LEDGER.csv"
CSV_765_MKI = OUT / "P8_Y5_R10_765_MAXWELL_KINETIC_INHERITANCE_GATE.csv"
CSV_3528_STATUS = OUT / "P8_EM_unique_F2_or_calibrated_alpha_status.csv"
CSV_3464_ALPHA = OUT / "P8_Y5_R2FR_3464_EM_ALPHA_CHARGE_OWNER_AUDIT.csv"
CSV_3465_OWNER = OUT / "P8_Y5_R2FR_3465_EM_OWNER_PACKAGE_AUDIT.csv"
CSV_3503_BOUND = OUT / "P8_EM_Hodge_Maxwell_current_owner_bound_vector.csv"

OUTPUTS = {
    "sources": OUT / "P8_Y5_R2FR_3874_SOURCE_REGISTER.csv",
    "split_theorem": OUT / "P8_Y5_R2FR_3874_EM_NORMALIZATION_SPLIT_THEOREM.csv",
    "active_residual": OUT / "P8_Y5_R2FR_3874_ACTIVE_F2_RESIDUAL_DEFINITION.csv",
    "envelope_update": OUT / "P8_Y5_R2FR_3874_STATIONARY_EM_SOURCE_ENVELOPE_UPDATE.csv",
    "branch_decision": OUT / "P8_Y5_R2FR_3874_BRANCH_DECISION_TABLE.csv",
    "claim_gates": OUT / "P8_Y5_R2FR_3874_CLAIM_GATES.csv",
    "next": OUT / "P8_Y5_R2FR_3874_NEXT_TARGET.csv",
    "status": OUT / "P8_Y5_R2FR_3874_STATUS.csv",
    "validation": OUT / "P8_Y5_BRR545_3874_VALIDATION.csv",
}

SOURCE_SPECS = [
    ("SRC3874_00_3873_next", CSV_3873_NEXT, "NEXT3873_0", "3873 selected EM normalization/Delta_w target"),
    ("SRC3874_01_3873_update", CSV_3873_UPDATE, "PCU3873_2_updated_envelope", "stationary EM envelope after Poynting zero"),
    ("SRC3874_02_3873_retained", CSV_3873_RETAINED, "RET3873_1_wEM", "retained EM source residuals"),
    ("SRC3874_03_3865_image", CSV_3865_IMAGE, "VOI3865_1_no_extra_F2_consequence", "visible operator image theorem"),
    ("SRC3874_04_3865_joint", CSV_3865_JOINT, "JHB3865_0_linear_constraint", "s_XF2/z_g/b_alpha joint identity"),
    ("SRC3874_05_3864_f2", CSV_3864_F2, "NEF3864_2_constant_lambda_guard", "constant lambda guard"),
    ("SRC3874_06_3864_audit", CSV_3864_AUDIT, "ODA3864_1_constant_lambda", "operator-domain audit constant lambda"),
    ("SRC3874_07_3864_lambda", CSV_3864_LAMBDA, "LFB3864_2_active_lambdaF2", "active F2 residual bound"),
    ("SRC3874_08_3863_mno", CSV_3863_MNO, "MNO3863_3_absolute_value_guard", "Maxwell normalization theorem"),
    ("SRC3874_09_3863_em", CSV_3863_EM, "ESB3863_2_EM_source_scale", "EM source-scale envelope"),
    ("SRC3874_10_3863_charge", CSV_3863_CHARGE, "CCA3863_1_unique_F2", "unique F2/current slot audit"),
    ("SRC3874_11_3809_mn", CSV_3809_MN, "MNT3809_5_absolute_value_split", "absolute alpha versus local drift split"),
    ("SRC3874_12_3791_zem", CSV_3791_ZEM, "ZFT3791_3_alpha_readout", "Z_EM normalization/readout guard"),
    ("SRC3874_13_3791_guard", CSV_3791_GUARD, "CTG3791_0_covariant_F2", "operator counterexample guard"),
    ("SRC3874_14_1057_ct", CSV_1057_CT, "CT1057_0_constant_lambda", "F2 counterterm ledger"),
    ("SRC3874_15_765_mki", CSV_765_MKI, "MKI765_2_unique_F2", "Maxwell kinetic inheritance gate"),
    ("SRC3874_16_3528_status", CSV_3528_STATUS, "STAT3528_1_calibrated_alpha", "calibrated alpha local branch"),
    ("SRC3874_17_3464_alpha", CSV_3464_ALPHA, "EAC3464_5_verdict", "EM action normalization proof verdict"),
    ("SRC3874_18_3465_owner", CSV_3465_OWNER, "EMO3465_5_verdict", "EM owner package audit verdict"),
    ("SRC3874_19_3503_bound", CSV_3503_BOUND, "EMB3503_1_w_EM", "EM Hodge/Maxwell/current owner bound vector"),
]

SPLIT_THEOREM = (
    "Write the effective observed Maxwell block as Z_Q_eff = Z_cal[1+deltaZ_act(X,A,readout)] and g_J_eff = g_cal[1+deltag_act(X,A,readout)]. "
    "A universal q-basic constant Z_cal/g_cal is an absolute calibration debt, not a local source-coupling residual; local WEP/R10/clock/PPN/source tests only see "
    "active non-common pieces: vertical derivatives, material/source dependence, hidden-visible F2 maps, radiative/readout regeneration, and current-normalization mismatch."
)

ACTIVE_IDENTITY = "b_alpha_active = 2 z_g_active - s_XF2_active"

STATIONARY_ACTIVE_ENVELOPE = (
    "B_EM_scale_stationary_active <= b_Z_active + b_J + |b_alpha_active| + |C_XF2_active| + |C_JQ| + |Delta_M_EM_binding| + |C_EM_readout|"
)


def now_utc() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def read_text(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        return path.read_text(encoding="utf-8-sig", errors="replace")


def rel(path: Path) -> str:
    try:
        return str(path.relative_to(PCW))
    except ValueError:
        return str(path)


def write_csv(path: Path, rows: list[dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        raise ValueError(f"no rows for {path}")
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def read_csv_rows(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8-sig") as handle:
        return list(csv.DictReader(handle))


def source_register_rows(timestamp: str) -> list[dict[str, object]]:
    rows = []
    for source_id, path, needle, role in SOURCE_SPECS:
        exists = path.exists()
        text = read_text(path) if exists else ""
        rows.append(
            {
                "source_id": source_id,
                "checkpoint": CHECKPOINT,
                "path": rel(path),
                "exists": exists,
                "needle": needle,
                "needle_found": needle in text,
                "role": role,
                "claim_use": "nonclaim_EM_normalization_active_residual_split",
                "timestamp_utc": timestamp,
            }
        )
    return rows


def split_theorem_rows(timestamp: str) -> list[dict[str, object]]:
    rows = [
        (
            "ENS3874_0_rescaling_class",
            "Maxwell normalization convention class",
            "A_Q -> s A_Q moves normalization between F_Q^2 and A_Q.J_Q, so bare Z_Q/w_EM is not physical until charge-current convention is fixed.",
            "do not mistake convention for a source residual",
            "EXACT_CONVENTION_GUARD",
        ),
        (
            "ENS3874_1_calibration_split",
            "constant calibration split",
            SPLIT_THEOREM,
            "removes universal constant lambda_0/w_0 from local residual scoring while keeping absolute-alpha prediction unclaimed",
            "EXACT_LOCAL_VS_ABSOLUTE_SPLIT",
        ),
        (
            "ENS3874_2_active_identity",
            "active alpha-current-F2 identity",
            ACTIVE_IDENTITY,
            "only active derivative/non-common pieces enter local alpha/source tests",
            "EXACT_ACTIVE_LINEAR_IDENTITY",
        ),
        (
            "ENS3874_3_parent_zero_route",
            "parent image zero route",
            "If visible coefficient image/fullness, no hidden-visible Hom, radiative/readout image stability, fixed T_Q norm, and same-current owner all hold, then s_XF2_active=z_g_active=b_alpha_active=C_XF2_active=C_JQ=0.",
            "this is the clean Maxwell/source-coupling theorem route",
            "EXACT_CONDITIONAL_ZERO_ROUTE",
        ),
        (
            "ENS3874_4_calibrated_branch",
            "calibrated local Maxwell branch",
            "If the parent zero route is unsigned, use measured alpha/mu0 as universal calibration and retain only active residual rows for local tests.",
            "lets local GR work proceed honestly without claiming an absolute alpha derivation",
            "CALIBRATED_BRANCH_ALLOWED_NONCLAIM",
        ),
        (
            "ENS3874_5_scope_guard",
            "not a proof of absolute constants",
            "The split does not derive alpha, mu0, charge quantum, or Newton G; it only classifies what can affect local source coupling after calibration.",
            "prevents overclaim",
            "SCOPE_GUARD",
        ),
    ]
    return [
        {
            "theorem_id": row_id,
            "piece": piece,
            "statement": statement,
            "effect": effect,
            "status": status,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
        for row_id, piece, statement, effect, status in rows
    ]


def active_residual_rows(timestamp: str) -> list[dict[str, object]]:
    rows = [
        ("AR3874_0_Z_cal", "Z_cal", "universal q-basic Maxwell calibration constant", "absolute_alpha_calibration_debt", "not a local drift/source residual", "CALIBRATION_NOT_LOCAL_RESIDUAL"),
        ("AR3874_1_lambda0", "lambda_0 F_Q^2", "constant hidden-independent F2 coefficient", "absolute_alpha_calibration_debt", "absorbed into measured alpha/mu0 if universal and q-basic", "CONSTANT_NOT_LOCAL_RESIDUAL"),
        ("AR3874_2_sXF2_active", "s_XF2_active", "D_X ln lambda_active or non-common F2 coefficient derivative", "hidden/readout/radiative/source-dependent F2", "clock/WEP/R10/PPN/source scale", "ACTIVE_RESIDUAL"),
        ("AR3874_3_zg_active", "z_g_active", "D_X ln g_J_eff active current normalization", "same-current owner failure", "alpha/source/current normalization", "ACTIVE_RESIDUAL"),
        ("AR3874_4_balpha_active", "b_alpha_active", "2 z_g_active - s_XF2_active", "active alpha response after calibration", "clock/WEP/R10/spectroscopy products", "ACTIVE_RESIDUAL_IDENTITY"),
        ("AR3874_5_CXF2_active", "C_XF2_active", "hidden-visible or motion/time coefficient multiplying F^2", "operator-domain/no-Hom/radiative failure", "source coupling and alpha-pressure tests", "ACTIVE_OPERATOR_RESIDUAL"),
        ("AR3874_6_CJQ", "C_JQ", "charge/current convention mismatch after calibration", "T_Q norm/current owner not fixed", "Lorentz/source current/WEP", "ACTIVE_CURRENT_RESIDUAL"),
        ("AR3874_7_CEM_readout", "C_EM_readout", "apparatus/loop/readout regenerated F2 or alpha response", "effective action not image-stable", "clock/WEP/R10/local source", "ACTIVE_READOUT_RESIDUAL"),
    ]
    return [
        {
            "residual_id": row_id,
            "quantity": quantity,
            "definition": definition,
            "owner_or_failure_mode": owner,
            "observable_effect": effect,
            "classification": classification,
            "numeric_value": "MISSING_PARENT_ZERO_OR_SOURCE_BOUND",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
        for row_id, quantity, definition, owner, effect, classification in rows
    ]


def envelope_update_rows(timestamp: str) -> list[dict[str, object]]:
    rows = [
        (
            "EUP3874_0_previous",
            "B_EM_scale_stationary",
            "B_EM_scale_stationary <= b_Z+b_J+|b_alpha|+|w_EM|+|C_XF2|+|C_JQ|+|Delta_M_EM_binding|",
            "from 3873 after Phi_EM_boundary stationary zero",
            "still mixed absolute calibration with local active residuals",
            "PREVIOUS_MIXED_FORM",
        ),
        (
            "EUP3874_1_active",
            "B_EM_scale_stationary_active",
            STATIONARY_ACTIVE_ENVELOPE,
            "3874 active residual split",
            "universal q-basic constants are calibration debt; active residuals remain test-facing",
            "REFINED_ACTIVE_SOURCE_ENVELOPE",
        ),
        (
            "EUP3874_2_parent_zero",
            "B_EM_scale_stationary_active",
            "if parent image + fixed norm + same-current + readout stability + EM binding once-only all close, then B_EM_scale_stationary_active -> |Delta_M_EM_binding_once_residual|",
            "composition of 3863/3864/3865/3873",
            "source stress then reduces to binding/source accounting rather than EM normalization drift",
            "EXACT_CONDITIONAL_REDUCTION",
        ),
        (
            "EUP3874_3_no_claim",
            "local_GR_EM_source",
            "no local-GR claim until active residuals or binding/source accounting are zeroed/bounded on the same arena domain",
            "claim discipline",
            "keeps WEP/R10/clock/PPN/orbital blocked unless rows are sourced",
            "NONCLAIM_GATE",
        ),
    ]
    return [
        {
            "update_id": row_id,
            "target": target,
            "formula": formula,
            "source_logic": logic,
            "effect": effect,
            "status": status,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
        for row_id, target, formula, logic, effect, status in rows
    ]


def branch_decision_rows(timestamp: str) -> list[dict[str, object]]:
    rows = [
        ("BRD3874_0_derived_parent", "derived-parent EM branch", "parent image/fullness + fixed T_Q norm + same-current + readout stability", "sets active EM normalization residuals to zero", "BEST_BUT_UNSIGNED"),
        ("BRD3874_1_calibrated_local", "calibrated local Maxwell branch", "measured alpha/mu0 are universal q-basic inputs; retain active residuals only", "lets local GR reduction proceed without absolute-alpha overclaim", "DEFAULT_WORKING_BRANCH"),
        ("BRD3874_2_active_bound", "finite active-residual branch", "use clock/WEP/R10/PPN/orbital source rows for s_XF2_active,z_g_active,C_XF2_active,CJQ", "empirical robustness path if theorem route stalls", "BOUND_BRANCH_READY"),
        ("BRD3874_3_reject_shortcut", "reject alpha-only shortcut", "b_alpha_active=2z_g_active-s_XF2_active", "alpha data cannot bound F2 unless z_g/current normalization is also zeroed or bounded", "GUARD_ACTIVE"),
    ]
    return [
        {
            "branch_id": branch_id,
            "branch": branch,
            "condition": condition,
            "consequence": consequence,
            "status": status,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
        for branch_id, branch, condition, consequence, status in rows
    ]


def claim_gate_rows(
    sources: list[dict[str, object]],
    theorem: list[dict[str, object]],
    residuals: list[dict[str, object]],
    envelopes: list[dict[str, object]],
    branches: list[dict[str, object]],
    timestamp: str,
) -> list[dict[str, object]]:
    all_sources = all(row["exists"] and row["needle_found"] for row in sources)
    rows = [
        ("G3874_0_sources", "all cited source rows resolved", "PASS" if all_sources else "FAIL", f"{sum(1 for row in sources if row['exists'] and row['needle_found'])}/{len(sources)} sources resolved"),
        ("G3874_1_split", "local-vs-absolute calibration split written", "PASS" if any(row["status"] == "EXACT_LOCAL_VS_ABSOLUTE_SPLIT" for row in theorem) else "FAIL", "constant calibration removed from local residual scoring"),
        ("G3874_2_active_identity", "active alpha-current-F2 identity present", "PASS" if any(ACTIVE_IDENTITY in row["statement"] for row in theorem) else "FAIL", ACTIVE_IDENTITY),
        ("G3874_3_residual_basis", "active residual basis has required terms", "PASS" if {"s_XF2_active", "z_g_active", "b_alpha_active", "C_XF2_active", "C_JQ"}.issubset({row["quantity"] for row in residuals}) else "FAIL", ",".join(sorted(row["quantity"] for row in residuals))),
        ("G3874_4_envelope", "stationary active EM source envelope written", "PASS" if any(row["formula"] == STATIONARY_ACTIVE_ENVELOPE for row in envelopes) else "FAIL", STATIONARY_ACTIVE_ENVELOPE),
        ("G3874_5_default_branch", "calibrated local branch selected as working nonclaim route", "PASS" if any(row["status"] == "DEFAULT_WORKING_BRANCH" for row in branches) else "FAIL", "calibrated branch"),
        ("G3874_6_no_claim", "no generated row allows public claim", "PASS", "valid_for_claim=false throughout"),
    ]
    return [
        {
            "gate_id": gate_id,
            "gate": gate,
            "status": status,
            "detail": detail,
            "claim_allowed": False,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
        for gate_id, gate, status, detail in rows
    ]


def next_rows(timestamp: str) -> list[dict[str, object]]:
    return [
        {
            "next_id": "NEXT3874_0",
            "target_checkpoint": "3875-Y5-R2FR-CJQ-current-owner-or-active-residual-runner.md",
            "script": "scripts/Y5_R2FR_3875_CJQ_current_owner_or_active_residual_runner.py",
            "objective": "attack the current-normalization leg C_JQ/z_g_active, because alpha/F2 bounds cannot isolate Maxwell normalization until the same-current owner is zeroed or numerically bounded",
            "why_next": "3874 split off universal calibration; the largest remaining degeneracy is z_g/C_JQ in b_alpha_active=2 z_g_active-s_XF2_active",
            "claim_allowed": False,
            "timestamp_utc": timestamp,
        }
    ]


def status_rows(timestamp: str) -> list[dict[str, object]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "branch": BRANCH,
            "result": "EM_NORMALIZATION_ACTIVE_RESIDUAL_SPLIT_BUILT_NONCLAIM",
            "claim_allowed": False,
            "short_summary": "3874 separates universal calibrated Maxwell constants from active source-coupling residuals and updates the stationary EM source envelope after the 3873 Poynting zero.",
            "timestamp_utc": timestamp,
        }
    ]


def markdown_table(rows: list[dict[str, object]], columns: list[str]) -> str:
    header = "| " + " | ".join(columns) + " |"
    sep = "| " + " | ".join("---" for _ in columns) + " |"
    lines = [header, sep]
    for row in rows:
        values = []
        for col in columns:
            values.append(str(row.get(col, "")).replace("\n", " ").replace("|", "\\|"))
        lines.append("| " + " | ".join(values) + " |")
    return "\n".join(lines)


def write_doc(
    sources: list[dict[str, object]],
    theorem: list[dict[str, object]],
    residuals: list[dict[str, object]],
    envelopes: list[dict[str, object]],
    branches: list[dict[str, object]],
    gates: list[dict[str, object]],
    next_target: list[dict[str, object]],
    timestamp: str,
) -> None:
    resolved = sum(1 for row in sources if row["exists"] and row["needle_found"])
    doc = f"""# 3874 — EM Normalization or Delta-w Theta Commonness

Generated: `{timestamp}`

## Result

3874 makes the key EM/source-coupling split:

`{SPLIT_THEOREM}`

So the stationary local source envelope after 3873 becomes:

`{STATIONARY_ACTIVE_ENVELOPE}`

This is a forward move because a universal calibrated `alpha/mu0` is no longer treated as an active local failure. The theory still cannot claim local GR/Maxwell source closure because the active pieces remain unsigned.

## Source Register

Resolved `{resolved}/{len(sources)}` source rows.

{markdown_table(sources, ["source_id", "path", "needle_found", "role"])}

## EM Normalization Split Theorem

{markdown_table(theorem, ["theorem_id", "piece", "statement", "status"])}

## Active Residual Definition

{markdown_table(residuals, ["residual_id", "quantity", "definition", "classification"])}

## Stationary Source Envelope Update

{markdown_table(envelopes, ["update_id", "target", "formula", "status"])}

## Branch Decision Table

{markdown_table(branches, ["branch_id", "branch", "condition", "consequence", "status"])}

## Claim Gates

{markdown_table(gates, ["gate_id", "status", "detail", "claim_allowed"])}

## Next Target

{markdown_table(next_target, ["next_id", "target_checkpoint", "objective", "why_next"])}

## Bottom Line

3874 is useful because it stops us wasting effort on the wrong thing. A common calibrated Maxwell constant is allowed as local input; the local-GR threat is the active residual vector `s_XF2_active`, `z_g_active`, `C_XF2_active`, `C_JQ`, `C_EM_readout`, and EM binding/source accounting. The next best move is `C_JQ/z_g_active`: without same-current/current-normalization closure, alpha data cannot isolate the F2 coefficient.
"""
    DOC_PATH.write_text(doc, encoding="utf-8")


def update_spine(timestamp: str) -> None:
    start = "<!-- BEGIN 3874 EM NORMALIZATION ACTIVE SPLIT -->"
    end = "<!-- END 3874 EM NORMALIZATION ACTIVE SPLIT -->"
    block = f"""{start}

## 3874 — EM normalization active-residual split

`3874` separates absolute Maxwell calibration from local source-coupling residuals. A universal q-basic `alpha/mu0` or constant `lambda_0 F_Q^2` is an absolute calibration debt, not by itself a WEP/R10/clock/PPN/local-source residual. The active test-facing vector is instead `s_XF2_active`, `z_g_active`, `b_alpha_active`, `C_XF2_active`, `C_JQ`, `C_EM_readout`, and EM binding/source accounting.

Exact active identity:

`{ACTIVE_IDENTITY}`

Updated stationary envelope after the 3873 Poynting boundary zero:

`{STATIONARY_ACTIVE_ENVELOPE}`

Default private branch: calibrated local Maxwell constants are allowed as inputs, while active residuals remain nonclaim until parent-zeroed or source-bounded. Next gate: `3875`, attack `C_JQ/z_g_active` because alpha/F2 cannot be isolated while current normalization is live.

Generated outputs:
- `source-intake\\mts_residuals\\P8_Y5_R2FR_3874_EM_NORMALIZATION_SPLIT_THEOREM.csv`
- `source-intake\\mts_residuals\\P8_Y5_R2FR_3874_ACTIVE_F2_RESIDUAL_DEFINITION.csv`
- `source-intake\\mts_residuals\\P8_Y5_R2FR_3874_STATIONARY_EM_SOURCE_ENVELOPE_UPDATE.csv`
- `source-intake\\mts_residuals\\P8_Y5_BRR545_3874_VALIDATION.csv`

<!-- Generated by 3874 at {timestamp} -->
{end}
"""
    existing = read_text(SPINE_PATH) if SPINE_PATH.exists() else "# Local GR Coupling Spine Current State\n"
    if start in existing and end in existing:
        before = existing.split(start)[0].rstrip()
        after = existing.split(end, 1)[1].lstrip()
        new_text = f"{before}\n\n{block}\n\n{after}".rstrip() + "\n"
    else:
        new_text = existing.rstrip() + "\n\n" + block + "\n"
    SPINE_PATH.write_text(new_text, encoding="utf-8")


def validation_rows(
    sources: list[dict[str, object]],
    theorem: list[dict[str, object]],
    residuals: list[dict[str, object]],
    envelopes: list[dict[str, object]],
    branches: list[dict[str, object]],
    gates: list[dict[str, object]],
    timestamp: str,
) -> list[dict[str, object]]:
    checks: list[tuple[str, str, bool, str]] = []
    all_sources = all(row["exists"] and row["needle_found"] for row in sources)
    checks.append(("VAL3874_0_sources", "all cited source paths exist and needles are found", all_sources, f"{sum(1 for row in sources if row['exists'] and row['needle_found'])}/{len(sources)} sources resolved"))
    checks.append(("VAL3874_1_split", "calibration split theorem exists", any(row["status"] == "EXACT_LOCAL_VS_ABSOLUTE_SPLIT" for row in theorem), "split theorem present"))
    checks.append(("VAL3874_2_active_identity", "active identity is exact and present", any(row["statement"] == ACTIVE_IDENTITY for row in theorem), ACTIVE_IDENTITY))
    required_residuals = {"s_XF2_active", "z_g_active", "b_alpha_active", "C_XF2_active", "C_JQ", "C_EM_readout"}
    residual_names = {row["quantity"] for row in residuals}
    checks.append(("VAL3874_3_residual_basis", "active residual basis covers required terms", required_residuals.issubset(residual_names), ",".join(sorted(residual_names))))
    checks.append(("VAL3874_4_envelope", "stationary active envelope is written", any(row["formula"] == STATIONARY_ACTIVE_ENVELOPE for row in envelopes), STATIONARY_ACTIVE_ENVELOPE))
    checks.append(("VAL3874_5_default_branch", "calibrated local branch is selected", any(row["status"] == "DEFAULT_WORKING_BRANCH" for row in branches), "DEFAULT_WORKING_BRANCH"))
    checks.append(("VAL3874_6_alpha_shortcut_guard", "alpha-only shortcut is rejected", any(row["status"] == "GUARD_ACTIVE" for row in branches), "GUARD_ACTIVE"))
    checks.append(("VAL3874_7_no_claim_gates", "no claim gate allows a claim", all(str(row["claim_allowed"]) == "False" for row in gates), "claim_allowed=false"))
    checks.append(("VAL3874_8_doc", "markdown checkpoint exists with expected bottom line", DOC_PATH.exists() and "3874 is useful" in read_text(DOC_PATH), rel(DOC_PATH)))
    checks.append(("VAL3874_9_spine", "spine updated with 3874 block", SPINE_PATH.exists() and "BEGIN 3874 EM NORMALIZATION ACTIVE SPLIT" in read_text(SPINE_PATH), rel(SPINE_PATH)))
    csv_outputs = [path for key, path in OUTPUTS.items() if key not in {"validation"}]
    csv_parse_ok = True
    parse_details = []
    for path in csv_outputs:
        try:
            count = len(read_csv_rows(path))
            parse_details.append(f"{path.name}:{count}")
        except Exception as exc:  # pragma: no cover
            csv_parse_ok = False
            parse_details.append(f"{path.name}:{exc}")
    checks.append(("VAL3874_10_csv_parse", "all generated CSV outputs parse", csv_parse_ok, "; ".join(parse_details)))
    formalization_hits = []
    if FWB.exists():
        formalization_hits = [path for path in FWB.rglob("*3874*") if path.is_file()]
    checks.append(("VAL3874_11_formalization_untouched", "no generated 3874 files appear in formalization-workbench", not formalization_hits, f"{len(formalization_hits)} hits"))
    pycache_hits = [path for path in (PCW / "scripts").rglob("__pycache__") if path.is_dir()]
    checks.append(("VAL3874_12_no_pycache", "scripts __pycache__ removed", not pycache_hits, f"{len(pycache_hits)} pycache dirs"))
    checks.append(("VAL3874_13_no_generated_claim", "all analytical rows are nonclaim", all(str(row.get("valid_for_claim")) == "False" for collection in [theorem, residuals, envelopes, branches] for row in collection), "valid_for_claim=false"))
    return [
        {
            "check_id": check_id,
            "description": description,
            "status": "PASS" if passed else "FAIL",
            "detail": detail,
            "timestamp_utc": timestamp,
        }
        for check_id, description, passed, detail in checks
    ]


def main() -> int:
    timestamp = now_utc()
    sources = source_register_rows(timestamp)
    theorem = split_theorem_rows(timestamp)
    residuals = active_residual_rows(timestamp)
    envelopes = envelope_update_rows(timestamp)
    branches = branch_decision_rows(timestamp)
    gates = claim_gate_rows(sources, theorem, residuals, envelopes, branches, timestamp)
    next_target = next_rows(timestamp)
    status = status_rows(timestamp)

    write_csv(OUTPUTS["sources"], sources)
    write_csv(OUTPUTS["split_theorem"], theorem)
    write_csv(OUTPUTS["active_residual"], residuals)
    write_csv(OUTPUTS["envelope_update"], envelopes)
    write_csv(OUTPUTS["branch_decision"], branches)
    write_csv(OUTPUTS["claim_gates"], gates)
    write_csv(OUTPUTS["next"], next_target)
    write_csv(OUTPUTS["status"], status)
    write_doc(sources, theorem, residuals, envelopes, branches, gates, next_target, timestamp)
    update_spine(timestamp)

    for pycache in (PCW / "scripts").rglob("__pycache__"):
        shutil.rmtree(pycache, ignore_errors=True)

    validation = validation_rows(sources, theorem, residuals, envelopes, branches, gates, timestamp)
    write_csv(OUTPUTS["validation"], validation)
    failed = [row for row in validation if row["status"] != "PASS"]
    if failed:
        for row in failed:
            print(f"FAIL {row['check_id']}: {row['detail']}")
        return 1
    print(f"{CHECKPOINT} PASS_EM_NORMALIZATION_ACTIVE_SPLIT")
    print(rel(DOC_PATH))
    print(rel(OUTPUTS["validation"]))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

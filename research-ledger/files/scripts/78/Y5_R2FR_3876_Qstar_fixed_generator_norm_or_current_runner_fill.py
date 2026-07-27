from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path


CHECKPOINT = "3876"
BRANCH = "MTS_R2FR_Y5_QSTAR_FIXED_GENERATOR_NORM_OR_CURRENT_RUNNER_FILL_3876"

PCW = Path(__file__).resolve().parents[1]
ROOT = PCW.parent
FWB = ROOT / "formalization-workbench"
OUT = PCW / "source-intake" / "mts_residuals"
DOC_PATH = PCW / "3876-Y5-R2FR-Qstar-fixed-generator-norm-or-current-runner-fill.md"
SPINE_PATH = PCW / "LOCAL_GR_COUPLING_SPINE_CURRENT_STATE.md"

CSV_3875_NEXT = OUT / "P8_Y5_R2FR_3875_NEXT_TARGET.csv"
CSV_3875_REDUCTION = OUT / "P8_Y5_R2FR_3875_ZG_ACTIVE_REDUCTION_ROWS.csv"
CSV_3868_COMPONENT = OUT / "P8_Y5_R2FR_3868_ZG_COMPONENT_LAW.csv"
CSV_3868_INPUTS = OUT / "P8_Y5_R2FR_3868_CURRENT_NORMALIZATION_BOUND_INPUT_REQUIREMENTS.csv"
CSV_3790_QSTAR = OUT / "P8_Y5_R2FR_3790_QSTAR_SUPERSELECTION_THEOREM.csv"
CSV_3790_AUDIT = OUT / "P8_Y5_R2FR_3790_CURRENT_CORPUS_QSTAR_SIGNATURE_AUDIT.csv"
CSV_3622_TQ = OUT / "P8_Y5_R2FR_3622_TQ_NQ_FIBRE_METRIC_THEOREM.csv"
CSV_3622_COUNTER = OUT / "P8_Y5_R2FR_3622_TQ_RESCALE_COUNTERMODEL_AUDIT.csv"
CSV_3623_CERT = OUT / "P8_Y5_R2FR_3623_PARENT_FIBRE_LEVEL_CERTIFICATE.csv"
CSV_3809_MN = OUT / "P8_Y5_R2FR_3809_MAXWELL_NORMALIZATION_THEOREM.csv"
CSV_3863_MNO = OUT / "P8_Y5_R2FR_3863_MAXWELL_NORMALIZATION_OWNER_THEOREM.csv"
CSV_3791_ZEM = OUT / "P8_Y5_R2FR_3791_ZEM_FIXED_NORMALIZATION_THEOREM.csv"
CSV_3781_GUARD = OUT / "P8_Y5_R2FR_3781_ZEM_ALPHA_OWNER_GUARD.csv"
CSV_765_MKI = OUT / "P8_Y5_R10_765_MAXWELL_KINETIC_INHERITANCE_GATE.csv"
CSV_3854_CELL = OUT / "P8_Y5_R2FR_3854_TOPOLOGICAL_CELL_CHARGE_AUDIT.csv"
CSV_3789_PATCH = OUT / "P8_Y5_R2FR_3789_PATCH_NORM_CONVENTION.csv"

OUTPUTS = {
    "sources": OUT / "P8_Y5_R2FR_3876_SOURCE_REGISTER.csv",
    "qstar_theorem": OUT / "P8_Y5_R2FR_3876_QSTAR_FIXED_NORM_THEOREM.csv",
    "owner_clauses": OUT / "P8_Y5_R2FR_3876_QSTAR_OWNER_CLAUSE_AUDIT.csv",
    "residual_contract": OUT / "P8_Y5_R2FR_3876_ZQSTAR_RESIDUAL_CONTRACT.csv",
    "runner_update": OUT / "P8_Y5_R2FR_3876_ACTIVE_CURRENT_RUNNER_UPDATE.csv",
    "claim_gates": OUT / "P8_Y5_R2FR_3876_CLAIM_GATES.csv",
    "next": OUT / "P8_Y5_R2FR_3876_NEXT_TARGET.csv",
    "status": OUT / "P8_Y5_R2FR_3876_STATUS.csv",
    "validation": OUT / "P8_Y5_BRR545_3876_VALIDATION.csv",
}

SOURCE_SPECS = [
    ("SRC3876_00_3875_next", CSV_3875_NEXT, "NEXT3875_0", "3875 selected z_Qstar target"),
    ("SRC3876_01_3875_reduction", CSV_3875_REDUCTION, "ZGR3875_1_z_Qstar", "z_Qstar dominant term"),
    ("SRC3876_02_3868_component", CSV_3868_COMPONENT, "ZC3868_1_base_unit", "z_Qstar component law"),
    ("SRC3876_03_3868_inputs", CSV_3868_INPUTS, "BIR3868_0_z_Qstar", "z_Qstar required evidence"),
    ("SRC3876_04_3790_qstar", CSV_3790_QSTAR, "QST3790_1_compact_lattice_route", "Qstar superselection theorem"),
    ("SRC3876_05_3790_audit", CSV_3790_AUDIT, "AUD3790_4_current_verdict", "current Qstar signature audit"),
    ("SRC3876_06_3622_tq", CSV_3622_TQ, "TNF3622_2_fixed_fibre_metric", "T_Q/N_Q fibre metric theorem"),
    ("SRC3876_07_3622_counter", CSV_3622_COUNTER, "RCM3622_1_base_charge_unit", "base charge unit countermodel"),
    ("SRC3876_08_3623_cert", CSV_3623_CERT, "PLC3623_2_charge_unit", "parent fibre level certificate"),
    ("SRC3876_09_3809_mn", CSV_3809_MN, "MNT3809_2_rescaling_countermodel", "Maxwell normalization countermodel"),
    ("SRC3876_10_3863_mno", CSV_3863_MNO, "MNO3863_2_normalization_owner_theorem", "Maxwell normalization owner theorem"),
    ("SRC3876_11_3791_zem", CSV_3791_ZEM, "ZFT3791_1_conditional_zero", "Z_EM fixed normalization theorem"),
    ("SRC3876_12_3781_guard", CSV_3781_GUARD, "ZOG3781_2_norm_owner", "Z_EM alpha owner guard"),
    ("SRC3876_13_765_mki", CSV_765_MKI, "MKI765_1_norm", "Maxwell kinetic inheritance norm gate"),
    ("SRC3876_14_3854_cell", CSV_3854_CELL, "TCA3854_3_quantized_charge", "topological cell charge limit"),
    ("SRC3876_15_3789_patch", CSV_3789_PATCH, "PATCH3789_1_positive_norm_metric", "positive norm convention"),
]

QSTAR_THEOREM = (
    "If the observed charge/current unit Qstar is a parent-owned q-basic or superselected object tied to a fixed compact T_Q lattice, "
    "a nonrescalable parent fibre metric/level/index fixes N_Q=<T_Q,T_Q>_P, the parent curvature coefficient C_P is q-basic, "
    "and readout does not redefine the charge/current unit, then z_Qstar := D_Xhat ln Qstar = 0 on ker(Dq_obs)."
)

QSTAR_COUNTERMODEL = (
    "Compact U(1) or integer representation labels fix relative n_A, but not the continuous base unit Qstar or N_Q; "
    "T_Q -> s T_Q with compensating A_Q/J_Q units leaves the observed form intact unless a nonrescalable parent norm/level/index is signed."
)

QSTAR_RESIDUAL = (
    "b_Qstar <= b_TQ_object + b_NQ_norm + b_CP_owner + b_Qunit_readout + b_level_index + b_patch_norm"
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
                "claim_use": "nonclaim_Qstar_fixed_norm_or_runner_fill",
                "timestamp_utc": timestamp,
            }
        )
    return rows


def qstar_theorem_rows(timestamp: str) -> list[dict[str, object]]:
    rows = [
        ("QNT3876_0_target", "z_Qstar zero theorem", QSTAR_THEOREM, "EXACT_CONDITIONAL_ZERO_THEOREM", "requires parent-signed fixed norm/base-unit owner"),
        ("QNT3876_1_compact_support", "compact U(1) support", "Compactness fixes the integral lattice direction and relative charge labels n_A on a fixed representation sector.", "PARTIAL_SUPPORT_RELATIVE_LABELS", "does not fix continuous Qstar/N_Q"),
        ("QNT3876_2_countermodel", "continuous normalization countermodel", QSTAR_COUNTERMODEL, "COUNTERMODEL_RETAINED", "blocks shortcut from charge quantization to alpha/current normalization"),
        ("QNT3876_3_fixed_norm_route", "fixed nonrescalable norm route", "A q-basic parent fibre metric, symplectic level, trace normalization, or lattice index fixes N_Q and gives D_X ln N_Q=0.", "EXACT_CONDITIONAL_SUBZERO", "parent object not signed"),
        ("QNT3876_4_base_unit_route", "base charge unit route", "Qstar is locally silent only if it is tied to the same parent representation/normalization data before readout.", "EXACT_CONDITIONAL_SUBZERO", "Qstar certificate missing"),
        ("QNT3876_5_absolute_guard", "absolute value guard", "Even z_Qstar=0 would not predict alpha_EM or mu0; absolute values need C_P,N_Q,Qstar,hbar/c and no-extra-F2 all parent-derived.", "SCOPE_GUARD", "local silence is not absolute prediction"),
        ("QNT3876_6_verdict", "strict current status", "Current corpus has the exact conditional theorem and support, but no parent-signed Qstar/N_Q certificate; use residual contract until signed.", "CURRENT_NONCLAIM_RESIDUAL_REQUIRED", "no current-normalization claim"),
    ]
    return [
        {
            "theorem_id": row_id,
            "piece": piece,
            "statement": statement,
            "status": status,
            "remaining_gap": gap,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
        for row_id, piece, statement, status, gap in rows
    ]


def owner_clause_rows(timestamp: str) -> list[dict[str, object]]:
    rows = [
        ("QOC3876_0_TQ_object", "parent compact visible generator T_Q exists before readout", "A_parent=A_Q T_Q+A_perp; exp(2*pi*T_Q)=1", "TEMPLATE/PARTIAL", "b_TQ_object"),
        ("QOC3876_1_lattice_labels", "relative representation labels are fixed", "n_A in Z and D_X n_A=0 on fixed sector", "DERIVED_FIXED_SECTOR_SUBZERO", "none_for_relative_labels"),
        ("QOC3876_2_NQ_norm", "nonrescalable fibre metric/level/index fixes N_Q", "N_Q=<T_Q,T_Q>_P and D_X N_Q=0", "EXACT_CONDITIONAL_NOT_SIGNED", "b_NQ_norm"),
        ("QOC3876_3_CP_owner", "parent curvature coefficient is q-basic/common", "D_X C_P=0", "CONDITIONAL_NOT_SIGNED", "b_CP_owner"),
        ("QOC3876_4_Qstar_unit", "observed base charge/current unit Qstar is tied to parent representation normalization", "q_A=n_A Qstar before readout", "MISSING_PARENT_QSTAR_CERTIFICATE", "b_Qunit_readout"),
        ("QOC3876_5_no_rescale", "continuous generator rescale is forbidden", "T_Q->sT_Q is not an allowed vertical representative once norm/level/index is fixed", "COUNTERMODEL_BLOCKER_UNSIGNED", "b_level_index"),
        ("QOC3876_6_patch_norm", "positive local norm/readout convention fixed", "same h_eff/U_good/measure convention for current and Maxwell block", "DEFINED_BUT_NUMERICALLY_MISSING", "b_patch_norm"),
    ]
    return [
        {
            "clause_id": row_id,
            "owner_clause": clause,
            "mathematical_form": form,
            "current_status": status,
            "residual_if_missing": residual,
            "passes_current_claim": False if residual != "none_for_relative_labels" else True,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
        for row_id, clause, form, status, residual in rows
    ]


def residual_contract_rows(timestamp: str) -> list[dict[str, object]]:
    rows = [
        ("ZQS3876_0_total", "b_Qstar", QSTAR_RESIDUAL, "finite nonclaim bound for z_Qstar", "COMPONENT_BOUND_CONTRACT"),
        ("ZQS3876_1_TQ_object", "b_TQ_object", "0 if parent visible T_Q object/projection is signed; otherwise bounded by projection ambiguity", "needed before Qstar can be parent-owned", "MISSING_PARENT_OBJECT_OR_BOUND"),
        ("ZQS3876_2_NQ_norm", "b_NQ_norm", "|D_X ln N_Q|", "nonrescalable fibre norm/level/index derivative", "MISSING_FIXED_NORM_OR_BOUND"),
        ("ZQS3876_3_CP_owner", "b_CP_owner", "|D_X ln C_P|", "parent curvature coefficient derivative", "MISSING_CP_OWNER_OR_BOUND"),
        ("ZQS3876_4_Qunit", "b_Qunit_readout", "|D_X ln Qstar_readout|", "base charge/current unit readout drift", "MISSING_QSTAR_CERTIFICATE_OR_BOUND"),
        ("ZQS3876_5_level_index", "b_level_index", "residual freedom in trace/level/lattice index convention", "blocks continuous rescale", "MISSING_LEVEL_INDEX_CERTIFICATE"),
        ("ZQS3876_6_patch_norm", "b_patch_norm", "norm/domain/readout mismatch contribution", "must share domain with z_g/s_XF2/b_alpha runner", "MISSING_PATCH_NORM_NUMERICS"),
        ("ZQS3876_7_active_runner", "z_g_active", "z_g_active <= b_Qstar + b_Noether + b_readout + b_source_slot + b_rad", "feeds 3875 active runner", "RUNNER_UPDATE_NONCLAIM"),
    ]
    return [
        {
            "residual_id": row_id,
            "quantity": quantity,
            "formula_or_definition": formula,
            "meaning": meaning,
            "status": status,
            "numeric_value": "MISSING_PARENT_ZERO_OR_SOURCE_BOUND",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
        for row_id, quantity, formula, meaning, status in rows
    ]


def runner_update_rows(timestamp: str) -> list[dict[str, object]]:
    rows = [
        ("RUNU3876_0_zg_previous", "z_g_active", "z_Qstar+z_Noether+z_readout+z_measure/source_slot+z_rad", "from 3875", "previous active current law"),
        ("RUNU3876_1_zqstar_insert", "z_Qstar", "z_Qstar=0 only under QNT3876_0; otherwise |z_Qstar|<=b_Qstar", "3876", "insert b_Qstar into runner"),
        ("RUNU3876_2_updated_runner", "z_g_active", "|z_g_active| <= b_Qstar+b_Noether+b_readout+b_source_slot+b_rad", "no-cancellation finite runner branch", "RUNNER_SCHEMA_REFINED"),
        ("RUNU3876_3_alpha_guard", "b_alpha_active", "b_alpha_active=2 z_g_active-s_XF2_active", "unchanged identity", "F2 cannot be isolated until b_Qstar and z_g components close"),
        ("RUNU3876_4_no_claim", "claim_allowed", "false until b_Qstar and every z_g/s_XF2/b_alpha domain row is parent-zero or source-backed", "acceptance policy", "NO_CLAIM"),
    ]
    return [
        {
            "update_id": row_id,
            "runner_field": field,
            "rule": rule,
            "source_logic": logic,
            "status": status,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
        for row_id, field, rule, logic, status in rows
    ]


def claim_gate_rows(
    sources: list[dict[str, object]],
    theorem: list[dict[str, object]],
    clauses: list[dict[str, object]],
    residuals: list[dict[str, object]],
    runner: list[dict[str, object]],
    timestamp: str,
) -> list[dict[str, object]]:
    all_sources = all(row["exists"] and row["needle_found"] for row in sources)
    rows = [
        ("G3876_0_sources", "all cited source rows resolved", "PASS" if all_sources else "FAIL", f"{sum(1 for row in sources if row['exists'] and row['needle_found'])}/{len(sources)} sources resolved"),
        ("G3876_1_theorem", "Qstar fixed norm theorem written", "PASS" if any(row["status"] == "EXACT_CONDITIONAL_ZERO_THEOREM" for row in theorem) else "FAIL", "conditional z_Qstar zero"),
        ("G3876_2_countermodel", "compact U1 shortcut blocked", "PASS" if any(row["status"] == "COUNTERMODEL_RETAINED" for row in theorem) else "FAIL", "relative labels not continuous norm"),
        ("G3876_3_clauses", "owner clauses cover norm/unit/readout", "PASS" if len(clauses) >= 7 else "FAIL", f"{len(clauses)} clauses"),
        ("G3876_4_residual_contract", "b_Qstar finite contract written", "PASS" if any(row["quantity"] == "b_Qstar" for row in residuals) else "FAIL", QSTAR_RESIDUAL),
        ("G3876_5_runner_update", "active current runner updated with b_Qstar", "PASS" if any(row["runner_field"] == "z_Qstar" for row in runner) else "FAIL", "z_Qstar runner row"),
        ("G3876_6_no_claim", "no generated row allows public claim", "PASS", "valid_for_claim=false throughout"),
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
            "next_id": "NEXT3876_0",
            "target_checkpoint": "3877-Y5-R2FR-readout-source-slot-radiative-current-tail-or-runner-fill.md",
            "script": "scripts/Y5_R2FR_3877_readout_source_slot_radiative_current_tail_or_runner_fill.py",
            "objective": "attack the remaining z_g_active tails after Qstar: readout transfer, source-slot/measure terms, and radiative/readout regeneration, or fill the active current runner with explicit nonclaim rows",
            "why_next": "3876 gives the exact Qstar theorem and finite b_Qstar contract but does not parent-sign fixed norm; the next finite tails are readout/source-slot/radiative stability",
            "claim_allowed": False,
            "timestamp_utc": timestamp,
        }
    ]


def status_rows(timestamp: str) -> list[dict[str, object]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "branch": BRANCH,
            "result": "QSTAR_FIXED_NORM_THEOREM_AND_BQSTAR_CONTRACT_BUILT_NONCLAIM",
            "claim_allowed": False,
            "short_summary": "3876 derives the exact conditional z_Qstar zero theorem, blocks the compact-U1 shortcut, and stages b_Qstar as the finite current-normalization input for the active residual runner.",
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
    clauses: list[dict[str, object]],
    residuals: list[dict[str, object]],
    runner: list[dict[str, object]],
    gates: list[dict[str, object]],
    next_target: list[dict[str, object]],
    timestamp: str,
) -> None:
    resolved = sum(1 for row in sources if row["exists"] and row["needle_found"])
    doc = f"""# 3876 — Qstar Fixed Generator Norm or Current Runner Fill

Generated: `{timestamp}`

## Result

3876 attacks the `z_Qstar` obstruction isolated by 3875:

`{QSTAR_THEOREM}`

The critical guard is:

`{QSTAR_COUNTERMODEL}`

So the finite fallback is:

`{QSTAR_RESIDUAL}`

## Source Register

Resolved `{resolved}/{len(sources)}` source rows.

{markdown_table(sources, ["source_id", "path", "needle_found", "role"])}

## Qstar Fixed-Norm Theorem

{markdown_table(theorem, ["theorem_id", "piece", "statement", "status"])}

## Owner Clause Audit

{markdown_table(clauses, ["clause_id", "owner_clause", "current_status", "residual_if_missing"])}

## z_Qstar Residual Contract

{markdown_table(residuals, ["residual_id", "quantity", "formula_or_definition", "status"])}

## Active Current Runner Update

{markdown_table(runner, ["update_id", "runner_field", "rule", "status"])}

## Claim Gates

{markdown_table(gates, ["gate_id", "status", "detail", "claim_allowed"])}

## Next Target

{markdown_table(next_target, ["next_id", "target_checkpoint", "objective", "why_next"])}

## Bottom Line

3876 is useful because it prevents a subtle overclaim: compact `U(1)` and integer charge labels do not derive the continuous current/Maxwell normalization. `z_Qstar=0` is exact only if the parent supplies a nonrescalable norm/level/base-unit owner. Since that owner is not signed in the current corpus, `b_Qstar` is now the explicit finite input feeding the active current runner. Next target: readout/source-slot/radiative current tails.
"""
    DOC_PATH.write_text(doc, encoding="utf-8")


def update_spine(timestamp: str) -> None:
    start = "<!-- BEGIN 3876 QSTAR FIXED NORM -->"
    end = "<!-- END 3876 QSTAR FIXED NORM -->"
    block = f"""{start}

## 3876 — Qstar fixed generator norm gate

`3876` attacks `z_Qstar`, the base charge/generator-norm term isolated by 3875. It records the exact conditional theorem:

`{QSTAR_THEOREM}`

It also records the guard:

`{QSTAR_COUNTERMODEL}`

Finite fallback:

`{QSTAR_RESIDUAL}`

No current-normalization or local-GR claim is made. The active runner now carries `b_Qstar` explicitly, and the next tails are readout/source-slot/radiative stability.

Generated outputs:
- `source-intake\\mts_residuals\\P8_Y5_R2FR_3876_QSTAR_FIXED_NORM_THEOREM.csv`
- `source-intake\\mts_residuals\\P8_Y5_R2FR_3876_QSTAR_OWNER_CLAUSE_AUDIT.csv`
- `source-intake\\mts_residuals\\P8_Y5_R2FR_3876_ZQSTAR_RESIDUAL_CONTRACT.csv`
- `source-intake\\mts_residuals\\P8_Y5_BRR545_3876_VALIDATION.csv`

Next gate: `3877`, readout/source-slot/radiative current tails.

<!-- Generated by 3876 at {timestamp} -->
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
    clauses: list[dict[str, object]],
    residuals: list[dict[str, object]],
    runner: list[dict[str, object]],
    gates: list[dict[str, object]],
    timestamp: str,
) -> list[dict[str, object]]:
    checks: list[tuple[str, str, bool, str]] = []
    all_sources = all(row["exists"] and row["needle_found"] for row in sources)
    checks.append(("VAL3876_0_sources", "all cited source paths exist and needles are found", all_sources, f"{sum(1 for row in sources if row['exists'] and row['needle_found'])}/{len(sources)} sources resolved"))
    checks.append(("VAL3876_1_theorem", "Qstar zero theorem exists", any(row["status"] == "EXACT_CONDITIONAL_ZERO_THEOREM" for row in theorem), "Qstar zero theorem present"))
    checks.append(("VAL3876_2_countermodel", "compact U1 shortcut is blocked", any(row["status"] == "COUNTERMODEL_RETAINED" for row in theorem), "countermodel retained"))
    required_clauses = {"b_NQ_norm", "b_Qunit_readout", "b_level_index", "b_patch_norm"}
    clause_residuals = {row["residual_if_missing"] for row in clauses}
    checks.append(("VAL3876_3_owner_clauses", "owner clauses include norm/unit/level/patch", required_clauses.issubset(clause_residuals), ",".join(sorted(clause_residuals))))
    checks.append(("VAL3876_4_residual_contract", "b_Qstar residual contract exists", any(row["quantity"] == "b_Qstar" and QSTAR_RESIDUAL in row["formula_or_definition"] for row in residuals), QSTAR_RESIDUAL))
    checks.append(("VAL3876_5_runner_update", "active runner has z_Qstar insertion row", any(row["runner_field"] == "z_Qstar" for row in runner), "z_Qstar runner update present"))
    checks.append(("VAL3876_6_no_claim_gates", "no claim gate allows a claim", all(str(row["claim_allowed"]) == "False" for row in gates), "claim_allowed=false"))
    checks.append(("VAL3876_7_doc", "markdown checkpoint exists with expected bottom line", DOC_PATH.exists() and "3876 is useful" in read_text(DOC_PATH), rel(DOC_PATH)))
    checks.append(("VAL3876_8_spine", "spine updated with 3876 block", SPINE_PATH.exists() and "BEGIN 3876 QSTAR FIXED NORM" in read_text(SPINE_PATH), rel(SPINE_PATH)))
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
    checks.append(("VAL3876_9_csv_parse", "all generated CSV outputs parse", csv_parse_ok, "; ".join(parse_details)))
    formalization_hits = []
    if FWB.exists():
        formalization_hits = [path for path in FWB.rglob("*3876*") if path.is_file()]
    checks.append(("VAL3876_10_formalization_untouched", "no generated 3876 files appear in formalization-workbench", not formalization_hits, f"{len(formalization_hits)} hits"))
    pycache_hits = [path for path in (PCW / "scripts").rglob("__pycache__") if path.is_dir()]
    checks.append(("VAL3876_11_no_pycache", "scripts __pycache__ removed", not pycache_hits, f"{len(pycache_hits)} pycache dirs"))
    checks.append(("VAL3876_12_no_generated_claim", "all analytical rows are nonclaim", all(str(row.get("valid_for_claim")) == "False" for collection in [theorem, clauses, residuals, runner] for row in collection), "valid_for_claim=false"))
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
    theorem = qstar_theorem_rows(timestamp)
    clauses = owner_clause_rows(timestamp)
    residuals = residual_contract_rows(timestamp)
    runner = runner_update_rows(timestamp)
    gates = claim_gate_rows(sources, theorem, clauses, residuals, runner, timestamp)
    next_target = next_rows(timestamp)
    status = status_rows(timestamp)

    write_csv(OUTPUTS["sources"], sources)
    write_csv(OUTPUTS["qstar_theorem"], theorem)
    write_csv(OUTPUTS["owner_clauses"], clauses)
    write_csv(OUTPUTS["residual_contract"], residuals)
    write_csv(OUTPUTS["runner_update"], runner)
    write_csv(OUTPUTS["claim_gates"], gates)
    write_csv(OUTPUTS["next"], next_target)
    write_csv(OUTPUTS["status"], status)
    write_doc(sources, theorem, clauses, residuals, runner, gates, next_target, timestamp)
    update_spine(timestamp)

    for pycache in (PCW / "scripts").rglob("__pycache__"):
        shutil.rmtree(pycache, ignore_errors=True)

    validation = validation_rows(sources, theorem, clauses, residuals, runner, gates, timestamp)
    write_csv(OUTPUTS["validation"], validation)
    failed = [row for row in validation if row["status"] != "PASS"]
    if failed:
        for row in failed:
            print(f"FAIL {row['check_id']}: {row['detail']}")
        return 1
    print(f"{CHECKPOINT} PASS_QSTAR_FIXED_NORM_CONTRACT")
    print(rel(DOC_PATH))
    print(rel(OUTPUTS["validation"]))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

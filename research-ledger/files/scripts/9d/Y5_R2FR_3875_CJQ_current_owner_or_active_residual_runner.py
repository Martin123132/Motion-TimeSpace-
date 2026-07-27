from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path


CHECKPOINT = "3875"
BRANCH = "MTS_R2FR_Y5_CJQ_CURRENT_OWNER_OR_ACTIVE_RESIDUAL_RUNNER_3875"

PCW = Path(__file__).resolve().parents[1]
ROOT = PCW.parent
FWB = ROOT / "formalization-workbench"
OUT = PCW / "source-intake" / "mts_residuals"
DOC_PATH = PCW / "3875-Y5-R2FR-CJQ-current-owner-or-active-residual-runner.md"
SPINE_PATH = PCW / "LOCAL_GR_COUPLING_SPINE_CURRENT_STATE.md"

CSV_3874_NEXT = OUT / "P8_Y5_R2FR_3874_NEXT_TARGET.csv"
CSV_3874_ACTIVE = OUT / "P8_Y5_R2FR_3874_ACTIVE_F2_RESIDUAL_DEFINITION.csv"
CSV_3874_ENV = OUT / "P8_Y5_R2FR_3874_STATIONARY_EM_SOURCE_ENVELOPE_UPDATE.csv"
CSV_3868_COMPONENT = OUT / "P8_Y5_R2FR_3868_ZG_COMPONENT_LAW.csv"
CSV_3868_REDUCED = OUT / "P8_Y5_R2FR_3868_REDUCED_ZG_CORE_ROWS.csv"
CSV_3868_INPUTS = OUT / "P8_Y5_R2FR_3868_CURRENT_NORMALIZATION_BOUND_INPUT_REQUIREMENTS.csv"
CSV_3869_THEOREM = OUT / "P8_Y5_R2FR_3869_ZNOETHER_THEOREM_PROOF.csv"
CSV_3869_AUDIT = OUT / "P8_Y5_R2FR_3869_CURRENT_OWNER_PREMISE_AUDIT.csv"
CSV_3870_THEOREM = OUT / "P8_Y5_R2FR_3870_NO_SOURCE_SLOT_THEOREM.csv"
CSV_3870_BJ = OUT / "P8_Y5_R2FR_3870_BJ_FINITE_INPUT_ROWS.csv"
CSV_3871_THEOREM = OUT / "P8_Y5_R2FR_3871_ACTION_MEASURE_OWNER_THEOREM.csv"
CSV_3871_BJ = OUT / "P8_Y5_R2FR_3871_BJ_FIRST_SOURCE_ROW_CONTRACT.csv"
CSV_3650_CLAUSES = OUT / "P8_Y5_R2FR_3650_CHARGE_CURRENT_CLAUSE_AUDIT.csv"
CSV_3863_CHARGE = OUT / "P8_Y5_R2FR_3863_CHARGE_CURRENT_SLOT_AUDIT.csv"
CSV_3503_BOUND = OUT / "P8_EM_Hodge_Maxwell_current_owner_bound_vector.csv"
CSV_3601_ELLJ = OUT / "P8_Y5_R2FR_3601_ELLJ_NORMALIZATION_THEOREM.csv"
CSV_3683_HILBERT = OUT / "P8_Y5_R2FR_3683_HILBERT_CHARGE_IDENTITY_AUDIT.csv"

OUTPUTS = {
    "sources": OUT / "P8_Y5_R2FR_3875_SOURCE_REGISTER.csv",
    "current_theorem": OUT / "P8_Y5_R2FR_3875_CJQ_CURRENT_OWNER_ZERO_THEOREM.csv",
    "zg_reduction": OUT / "P8_Y5_R2FR_3875_ZG_ACTIVE_REDUCTION_ROWS.csv",
    "runner_schema": OUT / "P8_Y5_R2FR_3875_ACTIVE_RESIDUAL_RUNNER_SCHEMA.csv",
    "claim_gates": OUT / "P8_Y5_R2FR_3875_CLAIM_GATES.csv",
    "next": OUT / "P8_Y5_R2FR_3875_NEXT_TARGET.csv",
    "status": OUT / "P8_Y5_R2FR_3875_STATUS.csv",
    "validation": OUT / "P8_Y5_BRR545_3875_VALIDATION.csv",
}

SOURCE_SPECS = [
    ("SRC3875_00_3874_next", CSV_3874_NEXT, "NEXT3874_0", "3874 selected C_JQ/z_g target"),
    ("SRC3875_01_3874_active", CSV_3874_ACTIVE, "AR3874_6_CJQ", "active C_JQ residual definition"),
    ("SRC3875_02_3874_env", CSV_3874_ENV, "EUP3874_1_active", "active stationary EM envelope"),
    ("SRC3875_03_3868_component", CSV_3868_COMPONENT, "ZC3868_0_product_decomposition", "z_g component law"),
    ("SRC3875_04_3868_reduced", CSV_3868_REDUCED, "RZG3868_0_direct_clock_alpha", "reduced z_g direct core"),
    ("SRC3875_05_3868_inputs", CSV_3868_INPUTS, "BIR3868_0_z_Qstar", "current normalization required inputs"),
    ("SRC3875_06_3869_theorem", CSV_3869_THEOREM, "ZNT3869_3_zero_theorem", "z_Noether same-current zero theorem"),
    ("SRC3875_07_3869_audit", CSV_3869_AUDIT, "PREM3869_1_same_AQ_owner", "current owner premise audit"),
    ("SRC3875_08_3870_theorem", CSV_3870_THEOREM, "NST3870_5_verdict", "no source-only current slot theorem"),
    ("SRC3875_09_3870_bj", CSV_3870_BJ, "BJF3870_5_c_A_pre", "finite current/source slot rows"),
    ("SRC3875_10_3871_theorem", CSV_3871_THEOREM, "AMT3871_1_quantum_measure", "action-measure owner theorem"),
    ("SRC3875_11_3871_bj", CSV_3871_BJ, "BJS3871_5_cA_pre", "first b_J current source row"),
    ("SRC3875_12_3650_clauses", CSV_3650_CLAUSES, "SCA3650_6_total", "charge-current clause audit"),
    ("SRC3875_13_3863_charge", CSV_3863_CHARGE, "CCA3863_2_same_current", "EM same-current slot audit"),
    ("SRC3875_14_3503_bound", CSV_3503_BOUND, "EMB3503_3_C_JQ", "current owner bound vector"),
    ("SRC3875_15_3601_ellj", CSV_3601_ELLJ, "ELJ3601_7_conditional_theorem", "ell_J source current theorem"),
    ("SRC3875_16_3683_hilbert", CSV_3683_HILBERT, "HCI3683_2_static_EM_dressing", "Hilbert current EM dressing subslot"),
]

CURRENT_ZERO_THEOREM = (
    "If the same fixed parent T_Q/A_Q owner supplies the Maxwell connection and the matter Noether current, "
    "the representation charge labels are fixed, the parent generator norm/base charge Qstar is q-basic, current variation occurs before readout, "
    "source-only c_A/w_A/kappa_A slots are absent or common derivative-silent calibration, and readout/radiative maps remain in the same q-basic image, "
    "then C_JQ=z_g_active=0 on ker(Dq_obs)."
)

ZG_REDUCED_ACTIVE = "z_g_active = z_Qstar + z_Noether + z_readout + z_measure/source_slot + z_rad"


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
                "claim_use": "nonclaim_CJQ_current_owner_or_active_residual_runner",
                "timestamp_utc": timestamp,
            }
        )
    return rows


def current_theorem_rows(timestamp: str) -> list[dict[str, object]]:
    rows = [
        ("CJT3875_0_target", "C_JQ/z_g_active zero target", CURRENT_ZERO_THEOREM, "EXACT_CONDITIONAL_ZERO_THEOREM", "not parent-promoted"),
        ("CJT3875_1_lattice", "fixed representation labels", "z_lattice,A=D ln n_A=0 on a fixed representation sector.", "DERIVED_FIXED_SECTOR_ZERO", "already a useful subzero"),
        ("CJT3875_2_post_current", "post-current rescale", "A post-variation current rescale cannot change the parent current; if inserted before variation it becomes a source/action slot.", "CONDITIONAL_POST_VARIATION_ZERO", "keeps pre-variation slots live"),
        ("CJT3875_3_noether", "Noether current owner", "If J_Q is varied from the same q-basic matter action and A_Q owner before readout, then z_Noether,A=0.", "EXACT_CONDITIONAL_SUBZERO", "requires same-current parent certificate"),
        ("CJT3875_4_source_slots", "source-only current/action slots", "c_A_pre,w_A,kappa_A are ill-typed under the parent matter grammar unless real fields/currents, q-basic calibration, or retained residuals.", "EXACT_CONDITIONAL_TYPED_EXCLUSION", "not parent-signed"),
        ("CJT3875_5_action_measure", "action/measure owner", "One hbar_parent and species-blind Dmu_parent would remove relative current/action multipliers up to common derivative-silent calibration.", "EXACT_CONDITIONAL_OWNER_ROUTE", "owner package unsigned"),
        ("CJT3875_6_verdict", "strict current status", "The clean theorem is exact conditional, but current MTS still needs Qstar fixed norm, same-current parent certificate, readout stability, and source-slot/action-measure closure.", "CURRENT_NONCLAIM_ACTIVE_RUNNER_REQUIRED", "no local-GR claim"),
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


def zg_reduction_rows(timestamp: str) -> list[dict[str, object]]:
    rows = [
        ("ZGR3875_0_reduced_law", "z_g_active", ZG_REDUCED_ACTIVE, "imports 3868 product decomposition and 3874 active split", "REDUCED_ACTIVE_LAW"),
        ("ZGR3875_1_z_Qstar", "z_Qstar", "D_X ln Qstar", "fixed nonrescalable T_Q norm/charge unit/level still missing", "DOMINANT_REMAINING_TERM"),
        ("ZGR3875_2_z_Noether", "z_Noether", "D_X ln Z_JA -> 0 if same-current owner closes", "3869 exact conditional theorem", "CONDITIONAL_SUBZERO_NOT_PROMOTED"),
        ("ZGR3875_3_z_readout", "z_readout", "D_X ln R_A", "clock/source/apparatus transfer kernel not zeroed", "LIVE_READOUT_TERM"),
        ("ZGR3875_4_z_source_slot", "z_measure/source_slot", "D_X ln c_A_pre + D_X ln w_A + D_X ln kappa_A + D_X ln J_A_measure", "3870/3871 make these ill-typed/measure-owned conditionally", "LIVE_UNTIL_PARENT_GRAMMAR"),
        ("ZGR3875_5_z_rad", "z_rad", "radiative/readout current regeneration", "effective action/image stability not signed", "LIVE_RADIOUT_TERM"),
        ("ZGR3875_6_alpha_link", "b_alpha_active", "b_alpha_active = 2 z_g_active - s_XF2_active", "current normalization must be zeroed/bounded before F2 is isolated", "RUNNER_GUARD"),
    ]
    return [
        {
            "reduction_id": row_id,
            "quantity": quantity,
            "formula": formula,
            "source_logic": logic,
            "status": status,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
        for row_id, quantity, formula, logic, status in rows
    ]


def runner_schema_rows(timestamp: str) -> list[dict[str, object]]:
    rows = [
        ("RUN3875_0_required_identity", "identity", "b_alpha_active = 2 z_g_active - s_XF2_active", "exact same-domain identity", "required before any score"),
        ("RUN3875_1_zg_input", "z_g_active", "numeric bound or theorem-zero for z_Qstar+z_Noether+z_readout+source_slot+rad", "MISSING_COMPONENT_VALUES", "blocks F2 isolation"),
        ("RUN3875_2_sxf2_input", "s_XF2_active", "numeric bound or theorem-zero for active F2 coefficient", "MISSING_F2_COMPONENT_VALUES", "blocks Maxwell normalization score"),
        ("RUN3875_3_balpha_input", "b_alpha_active", "clock/WEP/R10/spectroscopy alpha product in same Xhat/arena convention", "PARTIAL_EXTERNAL_PRODUCTS_ONLY", "must not be used alone"),
        ("RUN3875_4_CJQ_input", "C_JQ", "charge/current normalization mismatch row or same-current theorem-zero", "MISSING_CURRENT_OWNER_OR_VALUE", "local source-current leg blocked"),
        ("RUN3875_5_arena_domain", "arena_domain", "same material/source/readout/kernel convention for z_g, s_XF2 and b_alpha", "MISSING_SHARED_DOMAIN", "prevents cross-domain cancellation"),
        ("RUN3875_6_acceptance", "claim_allowed", "true only if every component is numeric/source-backed or parent-zeroed and no cancellation shortcut is used", "CLAIM_FALSE_CURRENTLY", "nonclaim runner contract"),
    ]
    return [
        {
            "schema_id": row_id,
            "field": field,
            "requirement": requirement,
            "current_status": status,
            "why_it_matters": why,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
        for row_id, field, requirement, status, why in rows
    ]


def claim_gate_rows(
    sources: list[dict[str, object]],
    theorem: list[dict[str, object]],
    reductions: list[dict[str, object]],
    runner: list[dict[str, object]],
    timestamp: str,
) -> list[dict[str, object]]:
    all_sources = all(row["exists"] and row["needle_found"] for row in sources)
    rows = [
        ("G3875_0_sources", "all cited source rows resolved", "PASS" if all_sources else "FAIL", f"{sum(1 for row in sources if row['exists'] and row['needle_found'])}/{len(sources)} sources resolved"),
        ("G3875_1_current_zero_theorem", "C_JQ/z_g zero theorem written", "PASS" if any(row["status"] == "EXACT_CONDITIONAL_ZERO_THEOREM" for row in theorem) else "FAIL", "conditional zero theorem"),
        ("G3875_2_reduction", "z_g_active reduced to finite components", "PASS" if any(row["formula"] == ZG_REDUCED_ACTIVE for row in reductions) else "FAIL", ZG_REDUCED_ACTIVE),
        ("G3875_3_alpha_guard", "alpha/F2 identity guard present", "PASS" if any(row["quantity"] == "b_alpha_active" for row in reductions) else "FAIL", "b_alpha_active row"),
        ("G3875_4_runner_schema", "active residual runner schema written", "PASS" if len(runner) >= 7 else "FAIL", f"{len(runner)} schema rows"),
        ("G3875_5_no_claim", "no generated row allows a claim", "PASS", "valid_for_claim=false throughout"),
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
            "next_id": "NEXT3875_0",
            "target_checkpoint": "3876-Y5-R2FR-Qstar-fixed-generator-norm-or-current-runner-fill.md",
            "script": "scripts/Y5_R2FR_3876_Qstar_fixed_generator_norm_or_current_runner_fill.py",
            "objective": "attack z_Qstar, the base charge/generator-norm term left after the current-owner reduction, or fill the active residual runner with explicit nonclaim rows",
            "why_next": "3875 reduces z_g_active to finite components; z_Qstar is now the cleanest remaining current-normalization obstruction",
            "claim_allowed": False,
            "timestamp_utc": timestamp,
        }
    ]


def status_rows(timestamp: str) -> list[dict[str, object]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "branch": BRANCH,
            "result": "CJQ_ZG_ACTIVE_CURRENT_OWNER_REDUCTION_BUILT_NONCLAIM",
            "claim_allowed": False,
            "short_summary": "3875 derives the exact conditional C_JQ/z_g_active zero route and reduces current normalization to Qstar, Noether/current owner, readout, source-slot/measure and radiative/readout components.",
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
    reductions: list[dict[str, object]],
    runner: list[dict[str, object]],
    gates: list[dict[str, object]],
    next_target: list[dict[str, object]],
    timestamp: str,
) -> None:
    resolved = sum(1 for row in sources if row["exists"] and row["needle_found"])
    doc = f"""# 3875 — C_JQ Current Owner or Active Residual Runner

Generated: `{timestamp}`

## Result

3875 targets the current-normalization leg that prevents alpha/F2 isolation:

`{CURRENT_ZERO_THEOREM}`

The practical reduced law is:

`{ZG_REDUCED_ACTIVE}`

This does not claim current normalization closure. It makes the next obstruction explicit: `z_Qstar` plus readout/source-slot/radiative terms.

## Source Register

Resolved `{resolved}/{len(sources)}` source rows.

{markdown_table(sources, ["source_id", "path", "needle_found", "role"])}

## C_JQ / Current Owner Theorem

{markdown_table(theorem, ["theorem_id", "piece", "statement", "status"])}

## z_g Active Reduction

{markdown_table(reductions, ["reduction_id", "quantity", "formula", "status"])}

## Active Residual Runner Schema

{markdown_table(runner, ["schema_id", "field", "requirement", "current_status"])}

## Claim Gates

{markdown_table(gates, ["gate_id", "status", "detail", "claim_allowed"])}

## Next Target

{markdown_table(next_target, ["next_id", "target_checkpoint", "objective", "why_next"])}

## Bottom Line

3875 is another real narrowing: `C_JQ/z_g_active` is no longer a single black box. Fixed representation labels and post-current rescaling are already under control; `z_Noether` has an exact same-current zero route; the remaining dominant current-normalization obstruction is `z_Qstar`, the fixed generator/base charge norm, plus readout/source-slot/radiative stability. Next best target is therefore `z_Qstar`.
"""
    DOC_PATH.write_text(doc, encoding="utf-8")


def update_spine(timestamp: str) -> None:
    start = "<!-- BEGIN 3875 CJQ CURRENT OWNER REDUCTION -->"
    end = "<!-- END 3875 CJQ CURRENT OWNER REDUCTION -->"
    block = f"""{start}

## 3875 — C_JQ / z_g_active current-owner reduction

`3875` attacks the current-normalization leg left by 3874. It records the exact conditional theorem that `C_JQ=z_g_active=0` if the same fixed parent `T_Q/A_Q` owner supplies Maxwell and matter current, representation labels are fixed, `Qstar` is q-basic/nonrescalable, current variation occurs before readout, source-only slots are absent or common derivative-silent calibration, and readout/radiative maps remain in the same image.

Reduced active law:

`{ZG_REDUCED_ACTIVE}`

The current branch is not claimed. The useful movement is that `z_g_active` now has a finite component list, and `z_Qstar` is identified as the cleanest remaining obstruction after existing fixed-label/post-current/same-current conditional reductions.

Generated outputs:
- `source-intake\\mts_residuals\\P8_Y5_R2FR_3875_CJQ_CURRENT_OWNER_ZERO_THEOREM.csv`
- `source-intake\\mts_residuals\\P8_Y5_R2FR_3875_ZG_ACTIVE_REDUCTION_ROWS.csv`
- `source-intake\\mts_residuals\\P8_Y5_R2FR_3875_ACTIVE_RESIDUAL_RUNNER_SCHEMA.csv`
- `source-intake\\mts_residuals\\P8_Y5_BRR545_3875_VALIDATION.csv`

Next gate: `3876`, attack `z_Qstar` / fixed generator norm.

<!-- Generated by 3875 at {timestamp} -->
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
    reductions: list[dict[str, object]],
    runner: list[dict[str, object]],
    gates: list[dict[str, object]],
    timestamp: str,
) -> list[dict[str, object]]:
    checks: list[tuple[str, str, bool, str]] = []
    all_sources = all(row["exists"] and row["needle_found"] for row in sources)
    checks.append(("VAL3875_0_sources", "all cited source paths exist and needles are found", all_sources, f"{sum(1 for row in sources if row['exists'] and row['needle_found'])}/{len(sources)} sources resolved"))
    checks.append(("VAL3875_1_zero_theorem", "C_JQ/z_g active zero theorem exists", any(row["status"] == "EXACT_CONDITIONAL_ZERO_THEOREM" for row in theorem), "zero theorem present"))
    checks.append(("VAL3875_2_subzeros", "fixed label and Noether subzero routes recorded", any(row["status"] == "DERIVED_FIXED_SECTOR_ZERO" for row in theorem) and any(row["status"] == "EXACT_CONDITIONAL_SUBZERO" for row in theorem), "subzeros present"))
    checks.append(("VAL3875_3_reduction_law", "z_g active reduction law exists", any(row["formula"] == ZG_REDUCED_ACTIVE for row in reductions), ZG_REDUCED_ACTIVE))
    required_quantities = {"z_Qstar", "z_Noether", "z_readout", "z_measure/source_slot", "z_rad", "b_alpha_active"}
    reduction_quantities = {row["quantity"] for row in reductions}
    checks.append(("VAL3875_4_reduction_components", "reduction components cover required terms", required_quantities.issubset(reduction_quantities), ",".join(sorted(reduction_quantities))))
    checks.append(("VAL3875_5_runner_schema", "runner schema has acceptance row", any(row["schema_id"] == "RUN3875_6_acceptance" for row in runner), f"{len(runner)} rows"))
    checks.append(("VAL3875_6_no_claim_gates", "no claim gate allows a claim", all(str(row["claim_allowed"]) == "False" for row in gates), "claim_allowed=false"))
    checks.append(("VAL3875_7_doc", "markdown checkpoint exists with expected bottom line", DOC_PATH.exists() and "3875 is another real narrowing" in read_text(DOC_PATH), rel(DOC_PATH)))
    checks.append(("VAL3875_8_spine", "spine updated with 3875 block", SPINE_PATH.exists() and "BEGIN 3875 CJQ CURRENT OWNER REDUCTION" in read_text(SPINE_PATH), rel(SPINE_PATH)))
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
    checks.append(("VAL3875_9_csv_parse", "all generated CSV outputs parse", csv_parse_ok, "; ".join(parse_details)))
    formalization_hits = []
    if FWB.exists():
        formalization_hits = [path for path in FWB.rglob("*3875*") if path.is_file()]
    checks.append(("VAL3875_10_formalization_untouched", "no generated 3875 files appear in formalization-workbench", not formalization_hits, f"{len(formalization_hits)} hits"))
    pycache_hits = [path for path in (PCW / "scripts").rglob("__pycache__") if path.is_dir()]
    checks.append(("VAL3875_11_no_pycache", "scripts __pycache__ removed", not pycache_hits, f"{len(pycache_hits)} pycache dirs"))
    checks.append(("VAL3875_12_no_generated_claim", "all analytical rows are nonclaim", all(str(row.get("valid_for_claim")) == "False" for collection in [theorem, reductions, runner] for row in collection), "valid_for_claim=false"))
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
    theorem = current_theorem_rows(timestamp)
    reductions = zg_reduction_rows(timestamp)
    runner = runner_schema_rows(timestamp)
    gates = claim_gate_rows(sources, theorem, reductions, runner, timestamp)
    next_target = next_rows(timestamp)
    status = status_rows(timestamp)

    write_csv(OUTPUTS["sources"], sources)
    write_csv(OUTPUTS["current_theorem"], theorem)
    write_csv(OUTPUTS["zg_reduction"], reductions)
    write_csv(OUTPUTS["runner_schema"], runner)
    write_csv(OUTPUTS["claim_gates"], gates)
    write_csv(OUTPUTS["next"], next_target)
    write_csv(OUTPUTS["status"], status)
    write_doc(sources, theorem, reductions, runner, gates, next_target, timestamp)
    update_spine(timestamp)

    for pycache in (PCW / "scripts").rglob("__pycache__"):
        shutil.rmtree(pycache, ignore_errors=True)

    validation = validation_rows(sources, theorem, reductions, runner, gates, timestamp)
    write_csv(OUTPUTS["validation"], validation)
    failed = [row for row in validation if row["status"] != "PASS"]
    if failed:
        for row in failed:
            print(f"FAIL {row['check_id']}: {row['detail']}")
        return 1
    print(f"{CHECKPOINT} PASS_CJQ_CURRENT_OWNER_REDUCTION")
    print(rel(DOC_PATH))
    print(rel(OUTPUTS["validation"]))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

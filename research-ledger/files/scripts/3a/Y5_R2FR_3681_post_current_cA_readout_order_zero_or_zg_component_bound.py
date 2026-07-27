from __future__ import annotations

import csv
import sys
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(r"D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work")
RESIDUALS = ROOT / "source-intake" / "mts_residuals"
FORMALIZATION = ROOT.parent / "formalization-workbench"
CHECKPOINT_ID = "3681"
BRANCH_ID = "MTS_R2FR_Y5_POST_CURRENT_CA_READOUT_ORDER_ZERO_OR_ZG_COMPONENT_BOUND_3681"
DOC = ROOT / "3681-Y5-R2FR-post-current-cA-readout-order-zero-or-zg-component-bound.md"


def stamp() -> str:
    return datetime.now(timezone.utc).isoformat()


def base(ts: str) -> dict[str, object]:
    return {
        "timestamp_utc": ts,
        "branch_id": BRANCH_ID,
        "checkpoint_id": CHECKPOINT_ID,
        "valid_for_claim": False,
    }


def read_text(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        return path.read_text(encoding="utf-8", errors="replace")


def write_csv(path: Path, rows: list[dict[str, object]]) -> None:
    if not rows:
        raise ValueError(f"no rows for {path}")
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def load_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def parse_csv(path: Path) -> tuple[bool, int]:
    try:
        rows = load_csv(path)
        return True, len(rows)
    except Exception:
        return False, 0


def source_register(ts: str) -> list[dict[str, object]]:
    specs = [
        ("handoff_3680", RESIDUALS / "P8_Y5_R2FR_3680_NEXT_TARGET.csv", "z_cA_post", "3680 selected post-current c_A/readout-order component"),
        ("component_3680", RESIDUALS / "P8_Y5_R2FR_3680_ZG_COMPONENT_DECOMPOSITION_ROWS.csv", "ZGD3680_4_post_current_term", "3680 z_g component decomposition"),
        ("arena_3680", RESIDUALS / "P8_Y5_R2FR_3680_SOURCE_ARENA_TRANSFER_ROWS.csv", "SAR3680_3_ppn_newton", "source arena transfer rows show PPN/Newton extensions"),
        ("theorem_1816", RESIDUALS / "P8_Y5_PARENT_QLOC_1816_VARIATION_BEFORE_READOUT_THEOREM.csv", "VBR1816_2_post_current_cA", "post-current c_A is conditionally not a parent source coupling"),
        ("selector_1816", RESIDUALS / "P8_Y5_PARENT_QLOC_1816_SOURCE_SELECTOR_ORDER_AUDIT.csv", "SSO1816_6_verdict", "full source-selector order remains unproved"),
        ("schema_1816", RESIDUALS / "P8_Y5_PARENT_QLOC_1816_POST_CURRENT_CA_ROW_SCHEMA.csv", "PCR1816_0_cA_post", "post-current c_A residual schema"),
        ("theorem_1454", RESIDUALS / "P8_Y5_R10_1454_VARIATION_BEFORE_READOUT_THEOREM_ATTEMPT.csv", "VBR1454_1_variational_identity", "functional derivative order identity"),
        ("readout_type_1802", RESIDUALS / "P8_Y5_PARENT_QLOC_1802_READOUT_TYPE_SPLIT.csv", "RTS1802_0_pure_postprocessing", "pure postprocessing type split"),
        ("readout_gate_1802", RESIDUALS / "P8_Y5_PARENT_QLOC_1802_MATTER_READOUT_THEOREM_GATE.csv", "MRT1802_4_pure_postprocessing", "pure readout postprocessing gate"),
        ("slot_1451", RESIDUALS / "P8_Y5_R10_1451_NO_SOURCE_ONLY_SLOT_OPERATOR_GRAMMAR_THEOREM_ATTEMPT.csv", "OG1451_6_verdict", "no source-only slot theorem remains unsigned"),
        ("slot_matrix_1451", RESIDUALS / "P8_Y5_R10_1451_SOURCE_ONLY_SLOT_REDUCTION_MATRIX.csv", "SM1451_0_wA_literal", "source-only slot countermodels"),
        ("no_rescale_1815", RESIDUALS / "P8_Y5_PARENT_QLOC_1815_NO_CURRENT_RESCALE_THEOREM.csv", "NCR1815_2_pre_variation_weight", "pre-variation weight limit remains live"),
        ("post_pre_1815", RESIDUALS / "P8_Y5_PARENT_QLOC_1815_POST_PRE_RESCALE_SPLIT_AUDIT.csv", "PPR1815_0_post_current_rescale", "post-current rescale is killed conditionally"),
    ]
    rows: list[dict[str, object]] = []
    for source_id, path, needle, relevance in specs:
        text = read_text(path) if path.exists() else ""
        rows.append(
            {
                **base(ts),
                "source_id": source_id,
                "source_path": str(path),
                "exists": path.exists(),
                "needle": needle,
                "needle_found": needle in text,
                "relevance": relevance,
            }
        )
    return rows


def theorem_rows(ts: str) -> list[dict[str, object]]:
    specs = [
        (
            "PCT3681_0_target_split",
            "split post-current c_A into parent-source and arena-transfer pieces",
            "z_cA_post,A = z_cA_parent_source,A + z_cA_transfer,A + z_cA_reentry,A",
            "SPLIT_DERIVED",
            "the target is no longer one blob; only the parent-source subpiece can be theorem-zero from variation order alone",
            False,
        ),
        (
            "PCT3681_1_variational_identity",
            "post-current c_A cannot alter a parent functional derivative",
            "If J_parent:=delta S_parent/delta A is evaluated on the parent field domain and J_eff:=c_A R_post[J_parent] is defined only after variation, then delta S_parent/delta A contains no c_A term.",
            "EXACT_TYPED_PARENT_SOURCE_LEMMA",
            "z_cA_parent_source,A = 0 by typed variation order",
            True,
        ),
        (
            "PCT3681_2_parent_source_zero",
            "parent-source part of post-current c_A is zero",
            "D_Xhat ln c_A does not enter the parent field equation if c_A is absent from S_parent and S_eff.",
            "THEOREM_ZERO_FOR_PARENT_SOURCE_SLOT",
            "parent field-equation source no longer carries this post-current coefficient",
            True,
        ),
        (
            "PCT3681_3_arena_transfer_survives",
            "empirical readout/source transfer is not killed",
            "J_eff=c_A R_post[J_parent] may still be what a clock/WEP/R10/PPN arena reports unless R_post and c_A are fixed downstream calibration with no source-normalization role.",
            "TRANSFER_RESIDUAL_RETAINED",
            "z_cA_transfer,A remains a finite component row",
            False,
        ),
        (
            "PCT3681_4_effective_reentry_survives",
            "effective/radiative/readout action reentry is not killed",
            "If c_A or a selector enters S_eff, a cutoff, a projector, a support map, or source-worldtube before variation, it is no longer post-current.",
            "REENTRY_RESIDUAL_RETAINED",
            "z_cA_reentry,A remains a finite component row",
            False,
        ),
        (
            "PCT3681_5_preaction_limit",
            "pre-action weights remain outside this theorem",
            "S_matter=sum_A w_A S_A before variation gives source currents weighted by w_A; post-current order cannot remove it.",
            "PREACTION_DELTA_W_UNTOUCHED",
            "Delta_w stays in source-arena extension, not in parent-source c_A",
            False,
        ),
        (
            "PCT3681_6_verdict",
            "z_cA_post is fully zero in the current corpus",
            "full zero would require parent-source zero plus arena transfer zero plus no effective reentry plus no source-only slot",
            "FULL_ZCA_POST_ZERO_NOT_PROVED_PARENT_SOURCE_SUBSLOT_ZERO",
            "one tooth is removed: the remaining debt is transfer/reentry, not parent-source variation",
            False,
        ),
    ]
    return [
        {
            **base(ts),
            "theorem_id": theorem_id,
            "claim": claim,
            "mathematical_statement": mathematical_statement,
            "status": status,
            "consequence": consequence,
            "theorem_zero_subslot": theorem_zero_subslot,
            "valid_for_claim": False,
            "claim_allowed": False,
            "score_ready": False,
        }
        for theorem_id, claim, mathematical_statement, status, consequence, theorem_zero_subslot in specs
    ]


def split_rows(ts: str) -> list[dict[str, object]]:
    specs = [
        (
            "CAS3681_0_parent_source",
            "z_cA_parent_source,A",
            "0",
            "post-current c_A term inside parent field equation",
            "EXACT_TYPED_PARENT_SOURCE_ZERO",
            "dimensionless current fraction",
            "PCT3681_1_variational_identity",
            "zero subslot, not an arena/local-GR claim",
        ),
        (
            "CAS3681_1_transfer",
            "z_cA_transfer,A",
            "D_Xhat ln c_A^arena or D_Xhat ln K_cA",
            "downstream empirical current/source transfer after parent source extraction",
            "MISSING_TRANSFER_KERNEL_OR_BOUND",
            "dimensionless transfer fraction",
            "PCR1816_0_cA_post;PCR1816_2_worldtube_transfer",
            "must be source-backed or theorem-zero before arena scoring",
        ),
        (
            "CAS3681_2_reentry",
            "z_cA_reentry,A",
            "||delta S_eff[c_A]/delta A||/||delta S_parent/delta A||",
            "effective/radiative/readout feedback before variation",
            "MISSING_NO_REENTRY_THEOREM_OR_BOUND",
            "dimensionless variation fraction",
            "PCR1816_3_effective_action_reentry;RTS1802_3_effective_action",
            "not post-current if it enters the action domain",
        ),
        (
            "CAS3681_3_post_current_total",
            "z_cA_post,A",
            "z_cA_transfer,A + z_cA_reentry,A",
            "remaining post-current/readout-order component after parent-source subslot removal",
            "REDUCED_COMPONENT_TRANSFER_REENTRY_ONLY",
            "dimensionless current/readout fraction",
            "CAS3681_1_transfer;CAS3681_2_reentry",
            "parent-source c_A removed from the no-cancellation vector",
        ),
        (
            "CAS3681_4_reduced_zg_core",
            "z_g_core,A",
            "z_Qstar + z_lattice,A + z_Noether,A + z_readout,A + z_cA_transfer,A + z_cA_reentry,A",
            "direct current normalization vector after the parent-source post-current c_A zero lemma",
            "UPDATED_NO_CANCELLATION_VECTOR",
            "dimensionless canonical derivative",
            "ZGD3680_1_core_decomposition",
            "still nonclaim because remaining components are unfilled",
        ),
    ]
    rows: list[dict[str, object]] = []
    for split_id, symbol, formula_or_value, meaning, status, units, source_anchor, interpretation in specs:
        rows.append(
            {
                **base(ts),
                "split_id": split_id,
                "symbol": symbol,
                "formula_or_value": formula_or_value,
                "meaning": meaning,
                "status": status,
                "units": units,
                "source_anchor": source_anchor,
                "interpretation": interpretation,
                "numeric_value": 0 if split_id == "CAS3681_0_parent_source" else "MISSING_COMPONENT_VALUE",
                "valid_for_claim": False,
                "claim_allowed": False,
                "score_ready": False,
            }
        )
    return rows


def component_bound_rows(ts: str) -> list[dict[str, object]]:
    specs = [
        (
            "ZCB3681_0_parent_source_zero",
            "z_cA_parent_source,A",
            "0",
            "theorem_zero_subslot",
            "parent-source post-current c_A is removed from field-equation source if c_A is absent from S_parent/S_eff",
            "PCT3681_1_variational_identity",
        ),
        (
            "ZCB3681_1_transfer_bound",
            "abs(z_cA_transfer,A)",
            "MISSING_TRANSFER_BOUND_VALUE",
            "dimensionless_transfer_fraction",
            "needs arena/source-worldtube transfer kernel or calibration certificate",
            "MISSING_ARENA_TRANSFER_KERNEL_SOURCE_PATH",
        ),
        (
            "ZCB3681_2_reentry_bound",
            "abs(z_cA_reentry,A)",
            "MISSING_REENTRY_BOUND_VALUE",
            "dimensionless_variation_fraction",
            "needs no-effective-action-reentry theorem or sourced coefficient",
            "MISSING_NO_REENTRY_SOURCE_PATH",
        ),
        (
            "ZCB3681_3_total_reduced",
            "abs(z_cA_post,A)",
            "abs(z_cA_transfer,A)+abs(z_cA_reentry,A)",
            "absolute_no_cancellation_envelope",
            "parent-source subslot removed, no cancellation between transfer and reentry allowed",
            "CAS3681_3_post_current_total",
        ),
    ]
    return [
        {
            **base(ts),
            "bound_id": bound_id,
            "quantity": quantity,
            "bound_or_formula": bound_or_formula,
            "units": units,
            "status": "THEOREM_ZERO_SUBSLOT_NONCLAIM" if "parent_source" in bound_id else "INPUT_REQUIRED_NONCLAIM",
            "interpretation": interpretation,
            "source_path_or_missing": source_path_or_missing,
            "valid_for_claim": False,
            "claim_allowed": False,
            "score_ready": False,
        }
        for bound_id, quantity, bound_or_formula, units, interpretation, source_path_or_missing in specs
    ]


def decision_rows(ts: str) -> list[dict[str, object]]:
    specs = [
        (
            "DEC3681_0_reduction",
            "post-current c_A parent-source subslot is theorem-zero",
            "REAL_REDUCTION",
            "a coefficient introduced only after parent variation cannot change the parent functional derivative",
            "remove z_cA_parent_source from the z_g no-cancellation vector",
        ),
        (
            "DEC3681_1_not_full_zero",
            "full z_cA_post is not theorem-zero",
            "TRANSFER_REENTRY_RETAINED",
            "arena transfer, source-worldtube kernels, and effective-action reentry can still make the observed source/current differ",
            "carry z_cA_transfer and z_cA_reentry forward",
        ),
        (
            "DEC3681_2_next_route",
            "source-worldtube/readout transfer is now the hard throat",
            "NEXT_BEST_TARGET",
            "once parent-source c_A is gone, the remaining physical piece is whether reported source current is fixed downstream or a hidden normalization map",
            "derive K_arena transfer zero or source a bound",
        ),
        (
            "DEC3681_3_claim_discipline",
            "no alpha/WEP/R10/PPN/local-GR claim",
            "PRIVATE_NONCLAIM",
            "a parent-source subslot zero is not an arena pass or a calibrated source coupling",
            "continue privately",
        ),
    ]
    return [
        {
            **base(ts),
            "decision_id": decision_id,
            "decision": decision,
            "status": status,
            "reason": reason,
            "next_action": next_action,
            "valid_for_claim": False,
            "claim_allowed": False,
            "score_ready": False,
        }
        for decision_id, decision, status, reason, next_action in specs
    ]


def claim_gate_rows(ts: str) -> list[dict[str, object]]:
    specs = [
        ("CG3681_0_parent_source_zero", "use theorem-zero subslot as local/source pass", "BLOCKED_SCOPE_LIMIT", "the zero applies only to c_A absent from the parent/effective action"),
        ("CG3681_1_full_zcA_zero", "claim z_cA_post=0", "BLOCKED_TRANSFER_REENTRY", "transfer and effective reentry rows remain missing"),
        ("CG3681_2_direct_alpha_bound", "treat alpha as direct s_XF2 bound", "BLOCKED_ZG_STILL_LIVE", "z_g still has lattice/Noether/readout/transfer/reentry components"),
        ("CG3681_3_source_universality", "claim Newton/GR source universality", "BLOCKED_SOURCE_ARENA_EXTENSION", "Delta_w, K_arena and non-Hilbert tails are outside this subslot lemma"),
        ("CG3681_4_public_or_github", "public/GitHub promotion", "BLOCKED_PRIVATE", "private derivation checkpoint only"),
    ]
    return [
        {
            **base(ts),
            "claim_gate_id": claim_gate_id,
            "gate": gate,
            "status": status,
            "reason": reason,
            "valid_for_claim": False,
            "claim_allowed": False,
            "score_ready": False,
        }
        for claim_gate_id, gate, status, reason in specs
    ]


def status_rows(ts: str) -> list[dict[str, object]]:
    return [
        {
            **base(ts),
            "status": "POST_CURRENT_CA_PARENT_SOURCE_SUBSLOT_ZERO_TRANSFER_REENTRY_RETAINED_NONCLAIM",
            "summary": "3681 proves a narrow typed lemma: a c_A introduced only after parent variation cannot alter the parent variational source. This removes the parent-source subslot from z_cA_post, but leaves arena transfer and effective-action reentry as the remaining physical component.",
            "claim_ceiling": "no full z_cA_post zero, z_g zero, direct alpha/s_XF2 bound, WEP/R10/PPN/Newton/local-GR pass, or public claim is made",
            "useful_result": "z_cA_post,A is reduced to z_cA_transfer,A + z_cA_reentry,A after z_cA_parent_source,A=0; the coupling debt is now readout/worldtube transfer, not parent-source variation",
            "next_missing_piece": "derive or source-bound z_cA_transfer,A / K_arena so reported arena current cannot hide source normalization",
        }
    ]


def next_rows(ts: str) -> list[dict[str, object]]:
    return [
        {
            **base(ts),
            "next_id": "NEXT3681_0",
            "target_doc": "3682-Y5-R2FR-source-worldtube-transfer-kernel-zero-or-zcA-transfer-bound.md",
            "target_script": "scripts/Y5_R2FR_3682_source_worldtube_transfer_kernel_zero_or_zcA_transfer_bound.py",
            "objective": "derive that the source-worldtube/readout transfer K_arena is fixed downstream and normalization-preserving, or source a finite z_cA_transfer bound row with units, normalizer, arena and source path",
            "success_gate": "z_cA_transfer is theorem-zero from a typed fixed readout kernel, or a source-backed nonclaim transfer row exists and z_cA_post has only transfer/reentry residuals",
        }
    ]


def write_doc(
    sources: list[dict[str, object]],
    theorem: list[dict[str, object]],
    split: list[dict[str, object]],
    bounds: list[dict[str, object]],
    decisions: list[dict[str, object]],
    gates: list[dict[str, object]],
    status: list[dict[str, object]],
    next_target: list[dict[str, object]],
) -> None:
    lines = [
        "# 3681 - Post-current c_A readout-order zero or z_g component bound",
        "",
        f"**Status:** {status[0]['status']}",
        "",
        "This checkpoint takes one actual bite out of the current-normalization problem. It does **not** claim `z_cA_post=0`. It proves the narrower typed result: if `c_A` appears only after parent variation, it cannot alter the parent variational source.",
        "",
        "## Main result",
        "",
        "`z_cA_parent_source,A = 0` for a strictly post-current `c_A` absent from `S_parent` and `S_eff`.",
        "",
        "The reduced post-current component is now:",
        "",
        "`z_cA_post,A = z_cA_transfer,A + z_cA_reentry,A`.",
        "",
        "So the remaining physical debt is arena transfer/effective-action reentry, not parent-source variation.",
        "",
        "## Theorem rows",
    ]
    for row in theorem:
        lines.append(f"- `{row['theorem_id']}`: {row['status']} - {row['claim']} -> {row['consequence']}")
    lines.extend(["", "## Split rows"])
    for row in split:
        lines.append(f"- `{row['split_id']}`: {row['status']} - `{row['symbol']}` -> `{row['formula_or_value']}`")
    lines.extend(["", "## Bound rows"])
    for row in bounds:
        lines.append(f"- `{row['bound_id']}`: {row['status']} - `{row['quantity']}` -> `{row['bound_or_formula']}`; {row['interpretation']}")
    lines.extend(["", "## Decisions"])
    for row in decisions:
        lines.append(f"- `{row['decision_id']}`: {row['status']} - {row['decision']} -> {row['next_action']}")
    lines.extend(["", "## Claim gates"])
    for row in gates:
        lines.append(f"- `{row['claim_gate_id']}`: {row['status']} - {row['gate']} because {row['reason']}")
    lines.extend(
        [
            "",
            "## Next target",
            f"`{next_target[0]['target_doc']}` via `{next_target[0]['target_script']}`.",
            "",
            "## Sources",
        ]
    )
    for row in sources:
        lines.append(f"- `{row['source_id']}`: `{row['source_path']}` exists={row['exists']} needle_found={row['needle_found']}")
    DOC.write_text("\n".join(lines) + "\n", encoding="utf-8")


def validate(
    ts: str,
    output_paths: list[Path],
    sources: list[dict[str, object]],
    theorem: list[dict[str, object]],
    split: list[dict[str, object]],
    bounds: list[dict[str, object]],
    decisions: list[dict[str, object]],
    gates: list[dict[str, object]],
    status: list[dict[str, object]],
    next_target: list[dict[str, object]],
) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []

    def add(validation_id: str, ok: bool, detail: str) -> None:
        rows.append(
            {
                "timestamp_utc": ts,
                "branch_id": BRANCH_ID,
                "checkpoint_id": CHECKPOINT_ID,
                "validation_id": validation_id,
                "result": "PASS" if ok else "FAIL",
                "detail": detail,
            }
        )

    csv_status = [parse_csv(path) for path in output_paths if path.suffix.lower() == ".csv"]
    generated = sources + theorem + split + bounds + decisions + gates + status + next_target
    doc_text = read_text(DOC)
    leaks: list[Path] = []
    if FORMALIZATION.exists():
        for pattern in ["*Y5_R2FR_3681*", "3681-Y5-R2FR-*", "P8_Y5*3681*"]:
            leaks.extend(FORMALIZATION.rglob(pattern))
    theorem_statuses = {str(row["status"]) for row in theorem}
    split_by_id = {str(row["split_id"]): row for row in split}
    bound_by_id = {str(row["bound_id"]): row for row in bounds}

    add("VAL3681_0_sources_exist", all(row["exists"] for row in sources), "every cited source path exists")
    add("VAL3681_1_needles_found", all(row["needle_found"] for row in sources), "every source needle found")
    add("VAL3681_2_outputs_exist", all(path.exists() for path in output_paths), "all expected 3681 outputs written")
    add("VAL3681_3_csv_parse", all(ok and count > 0 for ok, count in csv_status), "all generated CSVs parse with rows")
    add("VAL3681_4_typed_zero", "THEOREM_ZERO_FOR_PARENT_SOURCE_SLOT" in theorem_statuses and split_by_id["CAS3681_0_parent_source"]["numeric_value"] == 0, "parent-source post-current cA subslot is zero")
    add("VAL3681_5_not_full_zero", "FULL_ZCA_POST_ZERO_NOT_PROVED_PARENT_SOURCE_SUBSLOT_ZERO" in theorem_statuses, "full z_cA_post zero is not claimed")
    add("VAL3681_6_reduced_component", split_by_id["CAS3681_3_post_current_total"]["formula_or_value"] == "z_cA_transfer,A + z_cA_reentry,A", "z_cA_post reduced to transfer plus reentry")
    add("VAL3681_7_updated_zg_core", "z_cA_transfer,A + z_cA_reentry,A" in split_by_id["CAS3681_4_reduced_zg_core"]["formula_or_value"], "updated z_g core vector uses transfer/reentry only")
    add("VAL3681_8_bounds_retain_transfer", "ZCB3681_1_transfer_bound" in bound_by_id and str(bound_by_id["ZCB3681_1_transfer_bound"]["bound_or_formula"]).startswith("MISSING_"), "transfer bound remains explicit missing input")
    add("VAL3681_9_bounds_retain_reentry", "ZCB3681_2_reentry_bound" in bound_by_id and str(bound_by_id["ZCB3681_2_reentry_bound"]["bound_or_formula"]).startswith("MISSING_"), "reentry bound remains explicit missing input")
    add("VAL3681_10_claim_scope", any(row["claim_gate_id"] == "CG3681_1_full_zcA_zero" and row["status"] == "BLOCKED_TRANSFER_REENTRY" for row in gates), "full z_cA zero claim blocked by transfer/reentry")
    add("VAL3681_11_next_target", next_target[0]["target_doc"].startswith("3682-") and "z_cA_transfer" in next_target[0]["objective"], "3682 targets source-worldtube transfer")
    add("VAL3681_12_all_nonclaim", not any(str(row.get("valid_for_claim", "")).lower() == "true" or str(row.get("claim_allowed", "")).lower() == "true" or str(row.get("score_ready", "")).lower() == "true" for row in generated), "all generated rows remain nonclaim and unscoreable")
    add("VAL3681_13_doc_written", "z_cA_parent_source,A = 0" in doc_text and "z_cA_post,A = z_cA_transfer,A + z_cA_reentry,A" in doc_text and "does **not** claim" in doc_text, "doc records narrow zero and retained residual")
    add("VAL3681_14_claim_gates_blocked", all(row["claim_allowed"] is False and row["score_ready"] is False for row in gates), "claim gates remain blocked")
    add("VAL3681_15_no_formalization_leak", not leaks, "no 3681 checkpoint files in formalization-workbench")
    return rows


def main() -> int:
    ts = stamp()
    RESIDUALS.mkdir(parents=True, exist_ok=True)
    sources = source_register(ts)
    theorem = theorem_rows(ts)
    split = split_rows(ts)
    bounds = component_bound_rows(ts)
    decisions = decision_rows(ts)
    gates = claim_gate_rows(ts)
    status = status_rows(ts)
    next_target = next_rows(ts)
    outputs = {
        "sources": RESIDUALS / "P8_Y5_R2FR_3681_SOURCE_REGISTER.csv",
        "theorem": RESIDUALS / "P8_Y5_R2FR_3681_POST_CURRENT_CA_TYPED_ZERO_THEOREM.csv",
        "split": RESIDUALS / "P8_Y5_R2FR_3681_ZCA_POST_SPLIT_ROWS.csv",
        "bounds": RESIDUALS / "P8_Y5_R2FR_3681_ZCA_COMPONENT_BOUND_ROWS.csv",
        "decisions": RESIDUALS / "P8_Y5_R2FR_3681_DECISION_ROWS.csv",
        "gates": RESIDUALS / "P8_Y5_R2FR_3681_CLAIM_GATES.csv",
        "status": RESIDUALS / "P8_Y5_R2FR_3681_STATUS.csv",
        "next": RESIDUALS / "P8_Y5_R2FR_3681_NEXT_TARGET.csv",
        "validation": RESIDUALS / "P8_Y5_BRR545_3681_VALIDATION.csv",
    }
    write_csv(outputs["sources"], sources)
    write_csv(outputs["theorem"], theorem)
    write_csv(outputs["split"], split)
    write_csv(outputs["bounds"], bounds)
    write_csv(outputs["decisions"], decisions)
    write_csv(outputs["gates"], gates)
    write_csv(outputs["status"], status)
    write_csv(outputs["next"], next_target)
    write_doc(sources, theorem, split, bounds, decisions, gates, status, next_target)
    generated_paths = [path for key, path in outputs.items() if key != "validation"] + [DOC]
    validation = validate(ts, generated_paths, sources, theorem, split, bounds, decisions, gates, status, next_target)
    write_csv(outputs["validation"], validation)
    failures = [row for row in validation if row["result"] != "PASS"]
    if failures:
        print(f"3681 validation failed: {failures}", file=sys.stderr)
        return 1
    print("wrote 3681 checkpoint: parent-source post-current cA subslot zero; transfer/reentry retained")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

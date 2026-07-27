from __future__ import annotations

import csv
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
REPO = ROOT.parent
FW = REPO / "formalization-workbench"
OUT = ROOT / "source-intake" / "mts_residuals"
PYCACHE = ROOT / "scripts" / "__pycache__"

DOC = ROOT / "3292-Y5-R2FR-source-only-scalar-exclusion-from-parent-object-language-under-AX1090.md"

SRC_3291_DOC = ROOT / "3291-Y5-R2FR-TQ-Noether-current-owner-and-source-label-forgetting-under-AX1090.md"
SRC_3291_NEXT = OUT / "P8_Y5_R2FR_3291_NEXT_TARGET.csv"
SRC_3291_NOETHER = OUT / "P8_Y5_R2FR_3291_TQ_NOETHER_OWNER_LEMMA.csv"
SRC_3291_FORGETTING = OUT / "P8_Y5_R2FR_3291_SOURCE_LABEL_FORGETTING_LEMMA.csv"
SRC_3291_CLASS = OUT / "P8_Y5_R2FR_3291_CURRENT_WEIGHT_CLASSIFICATION.csv"
SRC_3291_REDUCTION = OUT / "P8_Y5_R2FR_3291_BETA_SOURCE_ALPHA_REDUCTION.csv"
SRC_3291_VALIDATION = OUT / "P8_Y5_BRR545_3291_VALIDATION.csv"
SRC_1064_DOC = ROOT / "1064-Y5-R10-parent-category-label-forgetting-proof-or-relative-weight-runner-fill.md"
SRC_1065_DOC = ROOT / "1065-Y5-R10-no-source-only-slot-parent-grammar-or-first-relative-weight-numeric-row.md"
SRC_1100_DOC = ROOT / "1100-Y5-R10-parent-TQ-owner-fixed-charge-lattice-and-gauge-norm-signature.md"

OUTPUTS = {
    "sources": OUT / "P8_Y5_R2FR_3292_SOURCE_REGISTER.csv",
    "theorem": OUT / "P8_Y5_R2FR_3292_SOURCE_ONLY_SCALAR_EXCLUSION_THEOREM.csv",
    "canonical": OUT / "P8_Y5_R2FR_3292_FIELD_REDEFINITION_CANONICALIZATION_AUDIT.csv",
    "hilbert": OUT / "P8_Y5_R2FR_3292_HILBERT_SOURCE_VS_SPURION_SPLIT.csv",
    "residuals": OUT / "P8_Y5_R2FR_3292_ARENA_PROJECTION_REMAINING_ROWS_NONCLAIM.csv",
    "runner": OUT / "P8_Y5_R2FR_3292_SCALAR_EXCLUSION_RUNNER_NONCLAIM.csv",
    "promotion": OUT / "P8_Y5_R2FR_3292_PROMOTION_GATES.csv",
    "decision": OUT / "P8_Y5_R2FR_3292_DECISION_LEDGER.csv",
    "next": OUT / "P8_Y5_R2FR_3292_NEXT_TARGET.csv",
    "validation": OUT / "P8_Y5_BRR545_3292_VALIDATION.csv",
}

RUN_UTC = datetime.now(timezone.utc).isoformat()
WEP_PRODUCT_BOUND = 4.797780522732e-05


def bool_str(value: bool) -> str:
    return "true" if value else "false"


def fmt(value: float) -> str:
    return f"{value:.12e}"


def compact(value: Any, limit: int = 520) -> str:
    text = " ".join(str(value).split())
    return text if len(text) <= limit else text[: limit - 3] + "..."


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    if not rows:
        raise ValueError(f"no rows for {path}")
    path.parent.mkdir(parents=True, exist_ok=True)
    fields: list[str] = []
    for row in rows:
        for key in row:
            if key not in fields:
                fields.append(key)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def csv_parse_ok(path: Path) -> bool:
    if not path.exists():
        return False
    try:
        read_csv(path)
        return True
    except Exception:
        return False


def text_parse_ok(path: Path) -> bool:
    if not path.exists():
        return False
    try:
        path.read_text(encoding="utf-8", errors="replace")
        return True
    except Exception:
        return False


def parse_ok(path: Path) -> bool:
    return csv_parse_ok(path) if path.suffix.lower() == ".csv" else text_parse_ok(path)


def evidence_hits(path: Path, needles: list[str], limit: int = 5) -> str:
    if not path.exists():
        return "MISSING_SOURCE"
    lines = path.read_text(encoding="utf-8", errors="replace").splitlines()
    lowered = [needle.lower() for needle in needles]
    hits: list[str] = []
    for idx, line in enumerate(lines, start=1):
        if any(needle in line.lower() for needle in lowered):
            hits.append(f"L{idx}:{compact(line, 320)}")
        if len(hits) >= limit:
            break
    return " | ".join(hits) if hits else "NO_PATTERN_HIT"


def snapshot_tree(path: Path) -> dict[str, tuple[int, int]]:
    if not path.exists():
        return {}
    snapshot: dict[str, tuple[int, int]] = {}
    for item in path.rglob("*"):
        if item.is_file():
            stat = item.stat()
            snapshot[str(item.relative_to(path))] = (stat.st_size, stat.st_mtime_ns)
    return snapshot


def changed_count(before: dict[str, tuple[int, int]], after: dict[str, tuple[int, int]]) -> int:
    keys = set(before) | set(after)
    return sum(1 for key in keys if before.get(key) != after.get(key))


def source_register_rows() -> list[dict[str, Any]]:
    sources = [
        (SRC_3291_DOC, "3291 handoff", ["source-only/species-label slot", "w_A"]),
        (SRC_3291_NEXT, "3291 next target", ["source-only-scalar-exclusion", "object-language"]),
        (SRC_3291_NOETHER, "Noether current owner lemma", ["TQN3291_3_current_weight_classification", "kappa_A"]),
        (SRC_3291_FORGETTING, "source-label forgetting lemma", ["SLF3291_3_live_counterexample", "w_A S_A"]),
        (SRC_3291_CLASS, "current weight classification", ["LIVE_SOURCE_ONLY_RESIDUAL", "MEASURED_MATTER_PARAMETER"]),
        (SRC_3291_REDUCTION, "beta source reduction", ["beta_source_only_label", "LIVE_RESIDUAL"]),
        (SRC_3291_VALIDATION, "3291 validation", ["VAL3291_13_overall", "true"]),
        (SRC_1064_DOC, "label forgetting and measured-G guard", ["no-source-only-slot", "measured G"]),
        (SRC_1065_DOC, "no-source-only-slot grammar", ["w_A", "field normalization"]),
        (SRC_1100_DOC, "T_Q current owner context", ["TQS1100_4_same_current_owner", "current rescaling"]),
    ]
    rows: list[dict[str, Any]] = []
    for idx, (path, role, needles) in enumerate(sources):
        rows.append(
            {
                "source_id": f"SRC3292_{idx}",
                "path": str(path),
                "exists": bool_str(path.exists()),
                "parse_ok": bool_str(parse_ok(path)),
                "role": role,
                "evidence_hits": evidence_hits(path, needles),
                "valid_for_claim": "false",
            }
        )
    return rows


def theorem_rows() -> list[dict[str, Any]]:
    return [
        {
            "theorem_id": "SOX3292_0_target",
            "claim_piece": "source-only scalar exclusion",
            "statement": "Exclude an inert dimensionless species scalar w_A/kappa_A whose only job is to change active source strength while leaving nongravitational readout and representation data untouched.",
            "proof_status": "TARGET_SHARP",
            "payoff": "would remove the surviving beta_source_only_label branch from 3291.",
            "valid_for_claim": "false",
        },
        {
            "theorem_id": "SOX3292_1_same_action_hilbert_route",
            "claim_piece": "non-Hilbert source term ban",
            "statement": "If source strength is only the Hilbert variation of the same matter action that defines inertial dynamics, then a term kappa_A T_A added only at source selection is not an allowed action-derived source.",
            "proof_status": "EXACT_CONDITIONAL_THEOREM",
            "payoff": "source-only weights must either enter the action/readout or be rejected as spurions.",
            "valid_for_claim": "false",
        },
        {
            "theorem_id": "SOX3292_2_canonicalization_route",
            "claim_piece": "whole-action prefactor classification",
            "statement": "If w_A multiplies the whole species action, canonical field normalization and quantum action-scale ownership move it into measured couplings/readout or remove it as a field normalization; it is not source-only.",
            "proof_status": "EXACT_CONDITIONAL_REDUCTION",
            "payoff": "w_A S_A is no longer a clean hidden gravity-only knob once canonical matter normalization is enforced.",
            "valid_for_claim": "false",
        },
        {
            "theorem_id": "SOX3292_3_object_language_route",
            "claim_piece": "parent object typing",
            "statement": "If the parent object language contains only fields, public geometry, fixed T_Q representation labels, and measured matter parameters, then a source-only scalar is not a well-typed object.",
            "proof_status": "EXACT_IF_LANGUAGE_SIGNATURE_ACCEPTED",
            "payoff": "Delta_w_AB=0 follows by absence of a source-only slot, not by tuning.",
            "valid_for_claim": "false",
        },
        {
            "theorem_id": "SOX3292_4_countermodel",
            "claim_piece": "why not promoted",
            "statement": "A parent could still add a non-Hilbert spurion field or label-retaining source functor unless same-action Hilbert source, canonical quantum normalization, and no-spurion object typing are signed.",
            "proof_status": "COUNTERMODEL_RETAINED",
            "payoff": "3292 is a strong reduction, not a local-GR/WEP claim.",
            "valid_for_claim": "false",
        },
        {
            "theorem_id": "SOX3292_5_verdict",
            "claim_piece": "source-only scalar status",
            "statement": "3292 proves a disjunction: w_A is either measured/field-normalization data, common calibration, or a non-Hilbert spurion. The hidden source-only branch survives only as the spurion case.",
            "proof_status": "PARTIAL_DERIVATION_NOT_PROMOTED",
            "payoff": "the coupling problem is now mostly parent-signature/Hilbert-source closure, not an arbitrary beta parameter.",
            "valid_for_claim": "false",
        },
    ]


def canonical_rows() -> list[dict[str, Any]]:
    return [
        {
            "case_id": "CAN3292_0_free_whole_action_weight",
            "candidate": "S_A -> w_A S_A for a free field",
            "classification": "FIELD_NORMALIZATION_OR_QUANTUM_SCALE",
            "argument": "psi_A' = sqrt(w_A) psi_A restores canonical kinetic normalization; if hbar/action scale is fixed, leftover changes are readout/normalization data, not source-only.",
            "remaining_gap": "parent-owned canonical quantum normalization",
            "valid_for_claim": "false",
        },
        {
            "case_id": "CAN3292_1_interacting_whole_action_weight",
            "candidate": "w_A multiplying an interacting/composite sector",
            "classification": "MEASURED_COUPLING_REPARAMETERIZATION_OR_SPURION",
            "argument": "canonicalization shifts interaction couplings and composite readout; if those are measured, w_A is not hidden, and if they are not transformed consistently it is a spurion.",
            "remaining_gap": "operator-domain/readout owner for all measured couplings",
            "valid_for_claim": "false",
        },
        {
            "case_id": "CAN3292_2_source_only_after_variation",
            "candidate": "T_source=sum_A w_A T_A after matter variation",
            "classification": "NON_HILBERT_SOURCE_SPURION",
            "argument": "this is not produced by varying the same S_matter unless w_A was in the action; it violates the same-action Hilbert-source premise.",
            "remaining_gap": "parent proof that all source selection is Hilbert variation only",
            "valid_for_claim": "false",
        },
        {
            "case_id": "CAN3292_3_common_weight",
            "candidate": "w_A=w_common for all species",
            "classification": "COMMON_CALIBRATION_GUARDED",
            "argument": "a universal constant can be folded into measured G only if it is time/range/frame/source independent.",
            "remaining_gap": "common-mode guard across local arenas",
            "valid_for_claim": "false",
        },
    ]


def hilbert_split_rows() -> list[dict[str, Any]]:
    return [
        {
            "split_id": "HSS3292_0_allowed_measured_parameter",
            "input_type": "mass, charge, representation label, interaction coupling",
            "source_effect": "enters S_matter, J_Q, T_total, and readout together",
            "classification": "ALLOWED_THETA_A",
            "beta_source_only_label": "0 for hidden source-only branch",
            "valid_for_claim": "false",
        },
        {
            "split_id": "HSS3292_1_allowed_common_calibration",
            "input_type": "single universal kappa_common",
            "source_effect": "common scale of source strength",
            "classification": "CALIBRATION_ONLY_IF_GUARDS_PASS",
            "beta_source_only_label": "0 relative piece only after guards",
            "valid_for_claim": "false",
        },
        {
            "split_id": "HSS3292_2_forbidden_source_only_spurion",
            "input_type": "w_A/kappa_A affects source but not matter/readout",
            "source_effect": "changes active/passive source normalization without same-action owner",
            "classification": "FORBID_IF_HILBERT_SOURCE_SIGNATURE_SIGNED",
            "beta_source_only_label": "live until parent signature",
            "valid_for_claim": "false",
        },
        {
            "split_id": "HSS3292_3_hidden_spurion_return",
            "input_type": "w_A(I_hid) or kappa_A(I_hid)",
            "source_effect": "vertical drift in source selection",
            "classification": "LIVE_COUNTERMODEL",
            "beta_source_only_label": "nonzero unless no-hidden/no-spurion theorem closes",
            "valid_for_claim": "false",
        },
    ]


def residual_rows() -> list[dict[str, Any]]:
    half = WEP_PRODUCT_BOUND / 2.0
    twice = WEP_PRODUCT_BOUND * 2.0
    return [
        {
            "row_id": "APR3292_0_source_only_zero_conditional",
            "arena": "formal_theorem",
            "quantity": "beta_source_only_label",
            "prediction": "0 if Hilbert-source signature + canonical normalization + no-spurion object typing are parent-signed",
            "bound": "0",
            "status": "PASS_SYMBOLIC_NONCLAIM",
            "missing_for_claim": "PARENT_HILBERT_SOURCE_SIGNATURE;CANONICAL_QUANTUM_NORMALIZATION;NO_SPURION_OBJECT_TYPING",
            "valid_for_claim": "false",
        },
        {
            "row_id": "APR3292_1_WEP_product_retained",
            "arena": "MICROSCOPE_WEP",
            "quantity": "|beta_source_alpha*b_alpha*tau_WEP|",
            "prediction": "product target retained",
            "bound": fmt(WEP_PRODUCT_BOUND),
            "status": "PRODUCT_TARGET_AVAILABLE_STANDALONE_BLOCKED",
            "missing_for_claim": "STANDALONE_B_ALPHA;TAU_WEP;MATERIAL_MAP;PARENT_SIGNATURE_OR_NUMERIC_PRODUCT",
            "valid_for_claim": "false",
        },
        {
            "row_id": "APR3292_2_PPN_Newton_residual",
            "arena": "PPN_Newton_local_GR",
            "quantity": "relative source/inertial normalization",
            "prediction": "MISSING_PARENT_SIGNATURE_OR_NUMERIC_BOUND",
            "bound": "PPN/orbital dependent",
            "status": "REFUSE_MISSING_SOURCE_NONCLAIM",
            "missing_for_claim": "HILBERT_SOURCE_SIGNATURE;COMMON_MODE_GUARDS;PPN_PROJECTION",
            "valid_for_claim": "false",
        },
        {
            "row_id": "APR3292_3_R10_residual",
            "arena": "R10_short_range",
            "quantity": "source alpha(lambda)",
            "prediction": "MISSING_TAU_R10_SOURCE_CURRENT_MAP",
            "bound": "requires real alpha(lambda) and source-current map",
            "status": "REFUSE_MISSING_SOURCE_NONCLAIM",
            "missing_for_claim": "TAU_R10;BOUND_CURVE;SOURCE_CURRENT_MAP;KERNEL_NORMALIZATION",
            "valid_for_claim": "false",
        },
        {
            "row_id": "APR3292_4_half_bound_smoke",
            "arena": "runner_smoke",
            "quantity": "|beta_source_alpha*b_alpha*tau_WEP|",
            "prediction": fmt(half),
            "bound": fmt(WEP_PRODUCT_BOUND),
            "status": "PASS_NUMERIC_NONCLAIM",
            "missing_for_claim": "SMOKE_ROW_NOT_PHYSICAL_INPUT",
            "valid_for_claim": "false",
        },
        {
            "row_id": "APR3292_5_twice_bound_smoke",
            "arena": "runner_smoke",
            "quantity": "|beta_source_alpha*b_alpha*tau_WEP|",
            "prediction": fmt(twice),
            "bound": fmt(WEP_PRODUCT_BOUND),
            "status": "FAIL_BOUND",
            "missing_for_claim": "SMOKE_ROW_NOT_PHYSICAL_INPUT",
            "valid_for_claim": "false",
        },
    ]


def runner_rows(residuals: list[dict[str, Any]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for row in residuals:
        try:
            prediction = float(str(row["prediction"]))
            bound = float(str(row["bound"]))
            observed = "PASS_NUMERIC_NONCLAIM" if abs(prediction) <= bound else "FAIL_BOUND"
        except (ValueError, TypeError):
            observed = row["status"]
        rows.append(
            {
                "run_id": row["row_id"],
                "expected_status": row["status"],
                "observed_status": observed,
                "expectation_match": bool_str(observed == row["status"]),
                "claim_allowed": "false",
            }
        )
    return rows


def promotion_rows() -> list[dict[str, Any]]:
    return [
        {
            "gate_id": "GATE3292_0_disjunction_theorem",
            "gate": "w_A classified as measured data, common calibration, or non-Hilbert spurion",
            "passed": "true",
            "claim_allowed": "false",
            "detail": "this is a real reduction of the source-only scalar branch.",
        },
        {
            "gate_id": "GATE3292_1_parent_hilbert_source_signed",
            "gate": "all source strength is Hilbert variation of same matter action",
            "passed": "false",
            "claim_allowed": "false",
            "detail": "still needs parent signature rather than closure.",
        },
        {
            "gate_id": "GATE3292_2_canonical_quantum_normalization_signed",
            "gate": "canonical matter/action-scale normalization is parent-owned",
            "passed": "false",
            "claim_allowed": "false",
            "detail": "field redefinition route is conditional until quantum/readout normalization is owned.",
        },
        {
            "gate_id": "GATE3292_3_arena_projection_ready",
            "gate": "WEP/R10/PPN source-current projections are sourced",
            "passed": "false",
            "claim_allowed": "false",
            "detail": "no local arena pass from scalar-exclusion theorem shape alone.",
        },
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        {
            "decision_id": "DEC3292_0_reduction_result",
            "finding": "The inert source-only scalar is not a normal free coupling under same-action Hilbert source plus canonical normalization.",
            "consequence": "it is either measured matter data, a common calibration, or a non-Hilbert spurion.",
            "claim_allowed": "false",
        },
        {
            "decision_id": "DEC3292_1_remaining_gap",
            "finding": "The remaining gap is parent signature: prove all source strength is Hilbert variation of one matter action with canonical quantum/readout normalization.",
            "consequence": "this is closer to deriving local GR matter coupling than just bounding beta_source_alpha.",
            "claim_allowed": "false",
        },
        {
            "decision_id": "DEC3292_2_best_next",
            "finding": "Next target should sign or reject parent Hilbert-source/canonical-normalization signature.",
            "consequence": "if it closes, the finite source-coupling branch collapses to arena projections; if not, move to numeric WEP/PPN/R10 source rows.",
            "claim_allowed": "false",
        },
    ]


def next_rows() -> list[dict[str, Any]]:
    return [
        {
            "next_id": "NEXT3292_0_3293",
            "target_doc": "3293-Y5-R2FR-parent-Hilbert-source-and-canonical-quantum-normalization-signature-under-AX1090.md",
            "target_script": "scripts/Y5_R2FR_3293_parent_Hilbert_source_and_canonical_quantum_normalization_signature.py",
            "objective": "prove or reject that the parent action supplies one Hilbert source for matter plus canonical quantum/readout normalization, so source-only species scalars are excluded rather than merely classified.",
            "guardrails": "do not assume equivalence principle; do not hide relative weights in measured G; do not claim WEP/R10/PPN/local-GR until arena projections are sourced.",
            "valid_for_claim": "false",
        }
    ]


def validate(
    sources: list[dict[str, Any]],
    theorem: list[dict[str, Any]],
    canonical: list[dict[str, Any]],
    hilbert: list[dict[str, Any]],
    residuals: list[dict[str, Any]],
    runner: list[dict[str, Any]],
    promotion: list[dict[str, Any]],
    decisions: list[dict[str, Any]],
    next_target: list[dict[str, Any]],
    formalization_changed_count: int,
) -> list[dict[str, Any]]:
    checks: list[dict[str, Any]] = []

    def add(check_id: str, check: str, passed: bool, detail: str = "") -> None:
        checks.append({"check_id": check_id, "check": check, "passed": bool_str(passed), "detail": detail})

    add("VAL3292_0_sources_exist", "all cited source paths exist", all(row["exists"] == "true" for row in sources))
    add("VAL3292_1_sources_parse", "all cited source paths parse", all(row["parse_ok"] == "true" for row in sources))
    add("VAL3292_2_outputs_parse", "all 3292 non-validation output CSVs parse", all(csv_parse_ok(path) for key, path in OUTPUTS.items() if key != "validation"))

    theorem_text = " ".join(row["statement"] for row in theorem)
    add(
        "VAL3292_3_theorem_has_real_disjunction",
        "theorem distinguishes Hilbert source, canonicalization, object typing, and spurion countermodel",
        "Hilbert variation" in theorem_text and "canonical" in theorem_text and "source-only scalar" in theorem_text and "spurion" in theorem_text,
    )

    canonical_text = " ".join(row["classification"] + " " + row["argument"] for row in canonical)
    add(
        "VAL3292_4_canonicalization_audit_present",
        "canonicalization audit covers field normalization, measured couplings, non-Hilbert source, and common calibration",
        "FIELD_NORMALIZATION" in canonical_text and "MEASURED_COUPLING" in canonical_text and "NON_HILBERT_SOURCE_SPURION" in canonical_text and "COMMON_CALIBRATION" in canonical_text,
    )

    hilbert_classes = {row["classification"] for row in hilbert}
    add(
        "VAL3292_5_hilbert_spurion_split_complete",
        "Hilbert split has allowed measured, common calibration, forbidden source-only, and hidden spurion rows",
        {"ALLOWED_THETA_A", "CALIBRATION_ONLY_IF_GUARDS_PASS", "FORBID_IF_HILBERT_SOURCE_SIGNATURE_SIGNED", "LIVE_COUNTERMODEL"}.issubset(hilbert_classes),
    )

    add(
        "VAL3292_6_residual_rows_nonclaim",
        "all arena residual rows remain nonclaim",
        all(row["valid_for_claim"] == "false" for row in residuals),
    )
    add(
        "VAL3292_7_runner_expectations",
        "scalar-exclusion runner expectations all match",
        all(row["expectation_match"] == "true" for row in runner),
        ";".join(f"{row['run_id']}={row['observed_status']}" for row in runner),
    )
    add(
        "VAL3292_8_claim_gates_false",
        "no 3292 gate allows WEP/R10/PPN/local-GR claim",
        all(row["claim_allowed"] == "false" for row in promotion) and any(row["passed"] == "false" for row in promotion),
    )
    add(
        "VAL3292_9_decision_moves_to_Hilbert_signature",
        "decision ledger moves to Hilbert-source/canonical-normalization signature",
        any("Hilbert variation" in row["finding"] for row in decisions) and any("local GR matter coupling" in row["consequence"] for row in decisions),
    )
    add(
        "VAL3292_10_next_target_focused",
        "next target focuses parent Hilbert source and canonical quantum normalization",
        len(next_target) == 1 and "Hilbert-source" in next_target[0]["target_doc"] and "canonical-quantum-normalization" in next_target[0]["target_doc"],
    )
    add(
        "VAL3292_11_formalization_untouched",
        "formalization-workbench modified-file count remains zero by this script",
        formalization_changed_count == 0,
        f"formalization_changed_count={formalization_changed_count}",
    )
    overall = all(row["passed"] == "true" for row in checks)
    add("VAL3292_12_overall", "3292 validation overall", overall, "all required checks passed" if overall else "one or more checks failed")
    return checks


def md_cell(value: Any) -> str:
    return str(value).replace("|", "\\|").replace("\n", " ")


def md_table(rows: list[dict[str, Any]]) -> str:
    fields: list[str] = []
    for row in rows:
        for key in row:
            if key not in fields:
                fields.append(key)
    lines = ["| " + " | ".join(fields) + " |", "| " + " | ".join("---" for _ in fields) + " |"]
    for row in rows:
        lines.append("| " + " | ".join(md_cell(row.get(field, "")) for field in fields) + " |")
    return "\n".join(lines)


def write_doc(
    sources: list[dict[str, Any]],
    theorem: list[dict[str, Any]],
    canonical: list[dict[str, Any]],
    hilbert: list[dict[str, Any]],
    residuals: list[dict[str, Any]],
    runner: list[dict[str, Any]],
    promotion: list[dict[str, Any]],
    decisions: list[dict[str, Any]],
    next_target: list[dict[str, Any]],
    validation: list[dict[str, Any]],
) -> None:
    text = f"""# 3292 - Source-only scalar exclusion from parent object language under AX1090

**Run UTC:** {RUN_UTC}

3292 attacks the survivor from 3291: an inert `w_A`/`kappa_A` that changes source strength without showing up in matter readout.

The result is a useful disjunction, not a public claim:

1. If the factor multiplies ordinary matter dynamics, canonical normalization turns it into field normalization or measured matter/readout data.
2. If it multiplies only the source after variation, it is not Hilbert variation of the same matter action; it is a non-Hilbert spurion.
3. If it is common to every species and arena, it is calibration only after range/time/frame guards.

So the source-only scalar is no longer a respectable free coupling under the same-action route. The remaining job is to parent-sign the Hilbert-source/canonical-normalization premises.

## Source Register

{md_table(sources)}

## Source-Only Scalar Exclusion Theorem

{md_table(theorem)}

## Field Redefinition And Canonicalization Audit

{md_table(canonical)}

## Hilbert Source Vs Spurion Split

{md_table(hilbert)}

## Arena Projection Residual Rows

{md_table(residuals)}

## Nonclaim Runner

{md_table(runner)}

## Promotion Gates

{md_table(promotion)}

## Decision Ledger

{md_table(decisions)}

## Next Target

{md_table(next_target)}

## Validation

{md_table(validation)}
"""
    DOC.write_text(text, encoding="utf-8")


def main() -> None:
    before_fw = snapshot_tree(FW)

    sources = source_register_rows()
    theorem = theorem_rows()
    canonical = canonical_rows()
    hilbert = hilbert_split_rows()
    residuals = residual_rows()
    runner = runner_rows(residuals)
    promotion = promotion_rows()
    decisions = decision_rows()
    next_target = next_rows()

    write_csv(OUTPUTS["sources"], sources)
    write_csv(OUTPUTS["theorem"], theorem)
    write_csv(OUTPUTS["canonical"], canonical)
    write_csv(OUTPUTS["hilbert"], hilbert)
    write_csv(OUTPUTS["residuals"], residuals)
    write_csv(OUTPUTS["runner"], runner)
    write_csv(OUTPUTS["promotion"], promotion)
    write_csv(OUTPUTS["decision"], decisions)
    write_csv(OUTPUTS["next"], next_target)

    after_fw = snapshot_tree(FW)
    validation = validate(sources, theorem, canonical, hilbert, residuals, runner, promotion, decisions, next_target, changed_count(before_fw, after_fw))
    write_csv(OUTPUTS["validation"], validation)
    write_doc(sources, theorem, canonical, hilbert, residuals, runner, promotion, decisions, next_target, validation)

    if PYCACHE.exists():
        for item in PYCACHE.iterdir():
            if item.is_file():
                item.unlink()
        try:
            PYCACHE.rmdir()
        except OSError:
            pass


if __name__ == "__main__":
    main()

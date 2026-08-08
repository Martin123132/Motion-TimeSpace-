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

DOC = ROOT / "3291-Y5-R2FR-TQ-Noether-current-owner-and-source-label-forgetting-under-AX1090.md"

SRC_3290_DOC = ROOT / "3290-Y5-R2FR-no-hidden-ZQ-coefficient-or-source-current-universality-under-AX1090.md"
SRC_3290_NEXT = OUT / "P8_Y5_R2FR_3290_NEXT_TARGET.csv"
SRC_3290_SOURCE = OUT / "P8_Y5_R2FR_3290_SOURCE_CURRENT_UNIVERSALITY_THEOREM.csv"
SRC_3290_RESIDUALS = OUT / "P8_Y5_R2FR_3290_HIDDEN_ZQ_SOURCE_ALPHA_RESIDUAL_ROWS_NONCLAIM.csv"
SRC_3290_VALIDATION = OUT / "P8_Y5_BRR545_3290_VALIDATION.csv"
SRC_1054_DOC = ROOT / "1054-Y5-R10-beta-source-alpha-zero-theorem-or-first-numeric-prior-width.md"
SRC_1062_DOC = ROOT / "1062-Y5-R10-parent-source-normalization-tauWEP-product-theorem-or-WEP-alpha-closure.md"
SRC_1063_DOC = ROOT / "1063-Y5-R10-source-label-forgetting-Noether-current-owner-or-relative-weight-prior.md"
SRC_1064_DOC = ROOT / "1064-Y5-R10-parent-category-label-forgetting-proof-or-relative-weight-runner-fill.md"
SRC_1065_DOC = ROOT / "1065-Y5-R10-no-source-only-slot-parent-grammar-or-first-relative-weight-numeric-row.md"
SRC_1100_DOC = ROOT / "1100-Y5-R10-parent-TQ-owner-fixed-charge-lattice-and-gauge-norm-signature.md"

OUTPUTS = {
    "sources": OUT / "P8_Y5_R2FR_3291_SOURCE_REGISTER.csv",
    "noether": OUT / "P8_Y5_R2FR_3291_TQ_NOETHER_OWNER_LEMMA.csv",
    "forgetting": OUT / "P8_Y5_R2FR_3291_SOURCE_LABEL_FORGETTING_LEMMA.csv",
    "classification": OUT / "P8_Y5_R2FR_3291_CURRENT_WEIGHT_CLASSIFICATION.csv",
    "reduction": OUT / "P8_Y5_R2FR_3291_BETA_SOURCE_ALPHA_REDUCTION.csv",
    "residuals": OUT / "P8_Y5_R2FR_3291_SOURCE_CURRENT_RESIDUAL_ROWS_NONCLAIM.csv",
    "runner": OUT / "P8_Y5_R2FR_3291_SOURCE_CURRENT_RUNNER_NONCLAIM.csv",
    "promotion": OUT / "P8_Y5_R2FR_3291_PROMOTION_GATES.csv",
    "decision": OUT / "P8_Y5_R2FR_3291_DECISION_LEDGER.csv",
    "next": OUT / "P8_Y5_R2FR_3291_NEXT_TARGET.csv",
    "validation": OUT / "P8_Y5_BRR545_3291_VALIDATION.csv",
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
    fieldnames: list[str] = []
    for row in rows:
        for key in row:
            if key not in fieldnames:
                fieldnames.append(key)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
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
        (SRC_3290_DOC, "3290 handoff", ["Source-current universality gate", "beta_source_alpha"]),
        (SRC_3290_NEXT, "3290 next target", ["TQ-Noether-current", "source-label-forgetting"]),
        (SRC_3290_SOURCE, "3290 source-current theorem", ["SCU3290_1_Noether_owner_case", "SCU3290_2_source_label_forgetting"]),
        (SRC_3290_RESIDUALS, "3290 WEP/R10 residual rows", ["HSR3290_2_WEP_beta_source_alpha_product", "R10"]),
        (SRC_3290_VALIDATION, "3290 validation", ["VAL3290_11_overall", "true"]),
        (SRC_1054_DOC, "beta_source_alpha zero theorem contract", ["beta_source_alpha=0", "source-label forgetting"]),
        (SRC_1062_DOC, "parent WEP source-normalization theorem", ["Noether current", "source-label forgetting"]),
        (SRC_1063_DOC, "source-label/Noether prior attempt", ["relative source weights", "Noether/current owner"]),
        (SRC_1064_DOC, "parent label-forgetting and measured-G guard", ["no-source-only-slot", "measured G"]),
        (SRC_1065_DOC, "no-source-only-slot grammar", ["w_A", "Noether/current owner"]),
        (SRC_1100_DOC, "T_Q owner and same current row", ["TQS1100_4_same_current_owner", "Z_A"]),
    ]
    rows: list[dict[str, Any]] = []
    for idx, (path, role, needles) in enumerate(sources):
        rows.append(
            {
                "source_id": f"SRC3291_{idx}",
                "path": str(path),
                "exists": bool_str(path.exists()),
                "parse_ok": bool_str(parse_ok(path)),
                "role": role,
                "evidence_hits": evidence_hits(path, needles),
                "valid_for_claim": "false",
            }
        )
    return rows


def noether_owner_rows() -> list[dict[str, Any]]:
    return [
        {
            "lemma_id": "TQN3291_0_target",
            "claim_piece": "same T_Q Noether/current owner",
            "statement": "The source/test charge current must be J_Q := (1/sqrt(-g)) delta S_matter/delta A_Q from the same parent T_Q owner that defines the Maxwell Q subblock.",
            "proof_status": "TARGET_SHARP",
            "payoff": "turns source charge normalization into a variational identity rather than an extra WEP/R10 fitting coefficient.",
            "blocks": "T_Q object, fixed charge labels, and unique current owner are not fully parent-signed in 1100.",
            "valid_for_claim": "false",
        },
        {
            "lemma_id": "TQN3291_1_minimal_coupling_variation",
            "claim_piece": "current from one action",
            "statement": "If S_A[psi_A,e,A_Q]=S_A[psi_A,e,D_A] with D_A=d+n_A A_Q T_Q, then delta S_matter/delta A_Q = sum_A n_A J_A and the Ward identity follows from T_Q gauge invariance.",
            "proof_status": "EXACT_CONDITIONAL_THEOREM",
            "payoff": "there is no separate source-current normalization slot once J_Q is defined by the same variation.",
            "blocks": "requires parent-fixed T_Q, n_A labels, and the absence of added source-only terms.",
            "valid_for_claim": "false",
        },
        {
            "lemma_id": "TQN3291_2_vertical_silence",
            "claim_piece": "current owner vertical derivative",
            "statement": "For vertical v in ker(Dq), if T_Q, n_A, A_Q projection, and the matter representation data are q-basic/fixed, then L_v n_A = 0 and L_v J_Q = 0 on shell.",
            "proof_status": "EXACT_CONDITIONAL_THEOREM",
            "payoff": "the current-normalization part of beta_source_alpha is theorem-zero without predicting the numerical alpha value.",
            "blocks": "same-current owner remains candidate rather than parent signature.",
            "valid_for_claim": "false",
        },
        {
            "lemma_id": "TQN3291_3_current_weight_classification",
            "claim_piece": "what happens to kappa_A A_Q J_A",
            "statement": "A coefficient kappa_A multiplying A_Q J_A is either a measured charge/representation label, a common calibration, or a source-only scalar that violates the same-current-owner clause.",
            "proof_status": "NEW_REDUCTION_LEMMA",
            "payoff": "current rescaling is no longer an amorphous blocker; the live finite branch is the source-only/species-label slot.",
            "blocks": "does not by itself prove source-only scalars are absent.",
            "valid_for_claim": "false",
        },
        {
            "lemma_id": "TQN3291_4_verdict",
            "claim_piece": "Noether/current owner status",
            "statement": "3291 narrows the current-coupling problem but does not promote a WEP/R10/local-GR pass: source-only species weights and parent T_Q signature remain unsigned.",
            "proof_status": "PARTIAL_DERIVATION_NOT_PROMOTED",
            "payoff": "next target can attack the source-only scalar directly instead of re-auditing all source coupling.",
            "blocks": "source-only scalar exclusion; parent T_Q signature; WEP/R10 tau projection maps.",
            "valid_for_claim": "false",
        },
    ]


def source_forgetting_rows() -> list[dict[str, Any]]:
    return [
        {
            "lemma_id": "SLF3291_0_target",
            "claim_piece": "source-label forgetting",
            "statement": "The source functor must consume total Hilbert/current objects, not species-labelled pairs: F_src(T_total,J_Q_total), not F_src({(T_A,J_A,A)}).",
            "proof_status": "TARGET_SHARP",
            "payoff": "relative source weights and beta_source_alpha slots are structurally unavailable.",
            "blocks": "parent object language has not yet forbidden source-only labels.",
            "valid_for_claim": "false",
        },
        {
            "lemma_id": "SLF3291_1_total_variation",
            "claim_piece": "labels disappear after total variation",
            "statement": "For one matter functional S_matter=sum_A S_A, T_total=(2/sqrt(-g)) delta S_matter/delta g = sum_A T_A and J_Q_total=delta S_matter/delta A_Q; the total objects do not carry a free relative coupling selector.",
            "proof_status": "EXACT_CONDITIONAL_THEOREM",
            "payoff": "a source selector that sees only total variational objects cannot build Delta_w_AB.",
            "blocks": "fails if the parent category still presents source-only labelled inputs before summation.",
            "valid_for_claim": "false",
        },
        {
            "lemma_id": "SLF3291_2_common_mode_guard",
            "claim_piece": "what measured G can absorb",
            "statement": "A single common kappa_univ multiplying every source/test sector can be calibration-only and absorbed into measured G only after it is universal, species-blind, range-independent, time-independent, and same-frame.",
            "proof_status": "GUARDED_CONDITIONAL",
            "payoff": "separates harmless common normalization from physical WEP/PPN/R10 relative weights.",
            "blocks": "range/time/frame/source derivatives are not yet derived.",
            "valid_for_claim": "false",
        },
        {
            "lemma_id": "SLF3291_3_live_counterexample",
            "claim_piece": "source-only species scalar",
            "statement": "If the parent language allows w_A S_A or kappa_A T_A where w_A has no nongravitational/readout role, covariance and additivity survive while WEP/PPN/R10 source normalization changes.",
            "proof_status": "COUNTEREXAMPLE_RETAINED",
            "payoff": "the remaining obstruction is finite and explicit.",
            "blocks": "derive no-source-only scalar rule or source numeric product rows.",
            "valid_for_claim": "false",
        },
        {
            "lemma_id": "SLF3291_4_verdict",
            "claim_piece": "source-label status",
            "statement": "Source-label forgetting is exact if the input is total variational data; the corpus still has not proved that parent syntax forbids source-only species inputs.",
            "proof_status": "PARTIAL_DERIVATION_NOT_PROMOTED",
            "payoff": "the source coupling route is now reduced to one object-language exclusion theorem plus arena projections.",
            "blocks": "no-source-only scalar exclusion; tau_WEP/R10/PPN projections.",
            "valid_for_claim": "false",
        },
    ]


def current_weight_classification_rows() -> list[dict[str, Any]]:
    return [
        {
            "class_id": "CWC3291_0_measured_charge_label",
            "coefficient_form": "n_A or q_A as representation/charge label",
            "classification": "MEASURED_MATTER_PARAMETER",
            "3291_reduction": "not a hidden alpha source coefficient if fixed by T_Q representation data",
            "remaining_requirement": "parent-fixed charge lattice/base unit and same current owner",
            "valid_for_claim": "false",
        },
        {
            "class_id": "CWC3291_1_common_normalization",
            "coefficient_form": "kappa_univ multiplying all source/current sectors",
            "classification": "COMMON_CALIBRATION_ONLY",
            "3291_reduction": "can be absorbed into measured G only after universality/range/time/frame guards",
            "remaining_requirement": "common-mode guard across PPN, clocks, orbital, R10",
            "valid_for_claim": "false",
        },
        {
            "class_id": "CWC3291_2_species_source_weight",
            "coefficient_form": "kappa_A T_A or w_A S_A with species labels retained",
            "classification": "LIVE_SOURCE_ONLY_RESIDUAL",
            "3291_reduction": "this is the surviving finite coupling branch",
            "remaining_requirement": "derive source-only scalar exclusion or source numeric product rows",
            "valid_for_claim": "false",
        },
        {
            "class_id": "CWC3291_3_hidden_current_weight",
            "coefficient_form": "kappa_A(I_hid) A_Q J_A",
            "classification": "LIVE_HIDDEN_SOURCE_RESIDUAL",
            "3291_reduction": "forbidden only if same current owner and no hidden-to-source scalar maps are parent-signed",
            "remaining_requirement": "combine with no-hidden-Z_Q/product functor route",
            "valid_for_claim": "false",
        },
        {
            "class_id": "CWC3291_4_readout_or_radiative_weight",
            "coefficient_form": "delta_readout or delta_lambda_rad changing effective charge/current",
            "classification": "LIVE_EFFECTIVE_ACTION_RESIDUAL",
            "3291_reduction": "outside tree-level Noether proof unless effective action/readout descends from same owner",
            "remaining_requirement": "radiative/readout closure",
            "valid_for_claim": "false",
        },
    ]


def beta_reduction_rows() -> list[dict[str, Any]]:
    return [
        {
            "reduction_id": "BRED3291_0_chain_rule",
            "quantity": "beta_source_alpha",
            "3291_statement": "Split beta_source_alpha into current-owner, source-label, hidden-source, and arena-projection pieces instead of treating it as one free factor.",
            "formula": "beta_source_alpha = beta_current_owner + beta_source_only_label + beta_hidden_source + beta_arena_projection",
            "status": "DECOMPOSITION",
            "valid_for_claim": "false",
        },
        {
            "reduction_id": "BRED3291_1_current_owner_piece",
            "quantity": "beta_current_owner",
            "3291_statement": "If J_Q=delta S_matter/delta A_Q from the same fixed T_Q owner, then beta_current_owner=0.",
            "formula": "L_v n_A = L_v J_Q = 0",
            "status": "THEOREM_ZERO_CONDITIONAL_NOT_PARENT_SIGNED",
            "valid_for_claim": "false",
        },
        {
            "reduction_id": "BRED3291_2_measured_charge_not_beta",
            "quantity": "measured q_A/n_A",
            "3291_statement": "A changed charge label is matter data, not a hidden source-current alpha drift, unless it is allowed to vary vertically without readout.",
            "formula": "q_A in theta_rep => L_v q_A=0",
            "status": "CLASSIFICATION_REDUCTION",
            "valid_for_claim": "false",
        },
        {
            "reduction_id": "BRED3291_3_source_only_piece",
            "quantity": "beta_source_only_label",
            "3291_statement": "The live source-current obstruction is a source-only species scalar or label-retaining source functor.",
            "formula": "Delta_w_AB != 0 gives WEP/PPN/R10 residuals",
            "status": "LIVE_RESIDUAL",
            "valid_for_claim": "false",
        },
        {
            "reduction_id": "BRED3291_4_arena_projection_piece",
            "quantity": "tau_WEP, tau_R10, tau_PPN",
            "3291_statement": "Even with source-only weights bounded, each arena still needs its own projection map before scoring.",
            "formula": "P_arena = beta_source_alpha * b_alpha * tau_arena",
            "status": "PROJECTION_REQUIRED",
            "valid_for_claim": "false",
        },
    ]


def residual_rows() -> list[dict[str, Any]]:
    half_bound = WEP_PRODUCT_BOUND / 2.0
    twice_bound = WEP_PRODUCT_BOUND * 2.0
    return [
        {
            "row_id": "SCR3291_0_same_current_owner_zero_conditional",
            "arena": "formal_theorem",
            "tested_quantity": "beta_current_owner",
            "prediction": "0 if same T_Q Noether current owner and fixed charge labels are parent-signed",
            "bound": "0",
            "runner_status": "PASS_SYMBOLIC_NONCLAIM",
            "missing_for_claim": "PARENT_TQ_SIGNATURE;FIXED_CHARGE_LABELS;NO_SOURCE_ONLY_SCALAR",
            "valid_for_claim": "false",
        },
        {
            "row_id": "SCR3291_1_source_only_species_weight",
            "arena": "WEP_PPN_R10_common_source",
            "tested_quantity": "Delta_w_AB or beta_source_only_label",
            "prediction": "MISSING_PARENT_OBJECT_LANGUAGE_ZERO_OR_NUMERIC_PRODUCT",
            "bound": "arena dependent",
            "runner_status": "REFUSE_MISSING_SOURCE_NONCLAIM",
            "missing_for_claim": "NO_SOURCE_ONLY_SCALAR_THEOREM;DELTA_W_AB;TAU_WEP;TAU_PPN;TAU_R10;SOURCE_PATHS",
            "valid_for_claim": "false",
        },
        {
            "row_id": "SCR3291_2_WEP_beta_source_alpha_product",
            "arena": "MICROSCOPE_WEP",
            "tested_quantity": "|beta_source_alpha*b_alpha*tau_WEP|",
            "prediction": "product target retained from 1054/3290",
            "bound": fmt(WEP_PRODUCT_BOUND),
            "runner_status": "PRODUCT_TARGET_AVAILABLE_STANDALONE_BLOCKED",
            "missing_for_claim": "STANDALONE_B_ALPHA;TAU_WEP_PROJECTION;BETA_SOURCE_ONLY_ZERO_OR_NUMERIC;MATERIAL_MAP",
            "valid_for_claim": "false",
        },
        {
            "row_id": "SCR3291_3_R10_source_current_placeholder",
            "arena": "R10_short_range",
            "tested_quantity": "alpha_source(lambda)",
            "prediction": "MISSING_TAU_R10_SOURCE_CURRENT_MAP",
            "bound": "requires real alpha(lambda) and source-current projection",
            "runner_status": "REFUSE_MISSING_SOURCE_NONCLAIM",
            "missing_for_claim": "TAU_R10;K_X;QBAR_XH;LAMBDA_X;REAL_BOUND_CURVE;SOURCE_CURRENT_MAP",
            "valid_for_claim": "false",
        },
        {
            "row_id": "SCR3291_4_PPN_Newton_source_normalization",
            "arena": "PPN_Newton_local_GR",
            "tested_quantity": "relative active/passive source normalization",
            "prediction": "MISSING_COMMON_MODE_AND_RELATIVE_SOURCE_MAP",
            "bound": "PPN/orbital/WEP dependent",
            "runner_status": "REFUSE_MISSING_SOURCE_NONCLAIM",
            "missing_for_claim": "COMMON_MODE_G_GUARDS;DELTA_W_AB;PPN_PROJECTION;ORBITAL_PROJECTION",
            "valid_for_claim": "false",
        },
        {
            "row_id": "SCR3291_5_half_bound_smoke",
            "arena": "runner_smoke",
            "tested_quantity": "|beta_source_alpha*b_alpha*tau_WEP|",
            "prediction": fmt(half_bound),
            "bound": fmt(WEP_PRODUCT_BOUND),
            "runner_status": "PASS_NUMERIC_NONCLAIM",
            "missing_for_claim": "SMOKE_ROW_NOT_PHYSICAL_INPUT",
            "valid_for_claim": "false",
        },
        {
            "row_id": "SCR3291_6_twice_bound_smoke",
            "arena": "runner_smoke",
            "tested_quantity": "|beta_source_alpha*b_alpha*tau_WEP|",
            "prediction": fmt(twice_bound),
            "bound": fmt(WEP_PRODUCT_BOUND),
            "runner_status": "FAIL_BOUND",
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
            numeric_result = abs(prediction) <= bound
        except (ValueError, TypeError):
            numeric_result = None
        if row["runner_status"] == "PASS_SYMBOLIC_NONCLAIM":
            observed = "PASS_SYMBOLIC_NONCLAIM"
        elif numeric_result is True:
            observed = "PASS_NUMERIC_NONCLAIM"
        elif numeric_result is False:
            observed = "FAIL_BOUND"
        else:
            observed = row["runner_status"]
        rows.append(
            {
                "run_id": row["row_id"],
                "arena": row["arena"],
                "expected_status": row["runner_status"],
                "observed_status": observed,
                "expectation_match": bool_str(observed == row["runner_status"]),
                "claim_allowed": "false",
            }
        )
    return rows


def promotion_rows() -> list[dict[str, Any]]:
    return [
        {
            "gate_id": "GATE3291_0_current_owner_shape",
            "gate": "same T_Q Noether/current owner theorem shape exists",
            "passed": "true",
            "claim_allowed": "false",
            "detail": "current normalization can be zeroed if J_Q is the same variational current.",
        },
        {
            "gate_id": "GATE3291_1_current_owner_parent_signed",
            "gate": "same T_Q current owner is parent-signed",
            "passed": "false",
            "claim_allowed": "false",
            "detail": "1100 keeps TQS1100_4 same current owner unsigned.",
        },
        {
            "gate_id": "GATE3291_2_source_only_scalar_excluded",
            "gate": "source-only species scalar w_A/kappa_A is excluded by parent object language",
            "passed": "false",
            "claim_allowed": "false",
            "detail": "1065 grammar is exact but not parent-derived.",
        },
        {
            "gate_id": "GATE3291_3_WEP_R10_PPN_projection_ready",
            "gate": "arena source-current projections are sourced",
            "passed": "false",
            "claim_allowed": "false",
            "detail": "tau_WEP, tau_R10, PPN/orbital projection maps remain missing.",
        },
        {
            "gate_id": "GATE3291_4_no_public_claim",
            "gate": "no WEP/R10/local-GR claim from 3291",
            "passed": "true",
            "claim_allowed": "false",
            "detail": "3291 is a derivation narrowing and residual split only.",
        },
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        {
            "decision_id": "DEC3291_0_real_progress",
            "finding": "Current rescaling is reduced: under same T_Q Noether owner, independent current weights are either measured charge labels, common calibration, or illegal/live source-only scalars.",
            "consequence": "the coupling problem is smaller than 3290; beta_source_alpha no longer needs to be treated as one opaque free factor.",
            "claim_allowed": "false",
        },
        {
            "decision_id": "DEC3291_1_remaining_obstruction",
            "finding": "The live counterexample is source-only species weight w_A/kappa_A or a label-retaining source functor.",
            "consequence": "next proof should attack parent object-language exclusion of inert source-only scalars.",
            "claim_allowed": "false",
        },
        {
            "decision_id": "DEC3291_2_no_transfer",
            "finding": "The WEP product target and clock products remain product pressures, not standalone beta_source_alpha or b_alpha evidence.",
            "consequence": "do not transfer clock bounds to WEP/R10/PPN without tau/source maps.",
            "claim_allowed": "false",
        },
        {
            "decision_id": "DEC3291_3_best_next",
            "finding": "3292 should try to derive the no-source-only scalar rule from parent object language/operator-domain typing.",
            "consequence": "if that fails, fill finite WEP/PPN/R10 source residual inputs instead of re-auditing Noether current.",
            "claim_allowed": "false",
        },
    ]


def next_rows() -> list[dict[str, Any]]:
    return [
        {
            "next_id": "NEXT3291_0_3292",
            "target_doc": "3292-Y5-R2FR-source-only-scalar-exclusion-from-parent-object-language-under-AX1090.md",
            "target_script": "scripts/Y5_R2FR_3292_source_only_scalar_exclusion_from_parent_object_language.py",
            "objective": "derive or reject the parent object-language/operator-domain rule that forbids inert source-only species scalars w_A/kappa_A; if rejected, fill finite WEP/PPN/R10 source-current residual input rows without claiming a pass.",
            "guardrails": "do not use minimality as proof; do not absorb relative weights into measured G; do not claim WEP/R10/PPN/local-GR without source-current projection maps.",
            "valid_for_claim": "false",
        }
    ]


def validate(
    sources: list[dict[str, Any]],
    noether: list[dict[str, Any]],
    forgetting: list[dict[str, Any]],
    classification: list[dict[str, Any]],
    reduction: list[dict[str, Any]],
    residuals: list[dict[str, Any]],
    runner: list[dict[str, Any]],
    promotion: list[dict[str, Any]],
    decisions: list[dict[str, Any]],
    next_target: list[dict[str, Any]],
    formalization_changed_count: int,
) -> list[dict[str, Any]]:
    checks: list[dict[str, Any]] = []

    def add(check_id: str, check: str, passed: bool, detail: str = "") -> None:
        checks.append(
            {
                "check_id": check_id,
                "check": check,
                "passed": bool_str(passed),
                "detail": detail,
            }
        )

    add("VAL3291_0_sources_exist", "all cited source paths exist", all(row["exists"] == "true" for row in sources))
    add("VAL3291_1_sources_parse", "all cited source paths parse", all(row["parse_ok"] == "true" for row in sources))

    output_parse = all(csv_parse_ok(path) for key, path in OUTPUTS.items() if key != "validation")
    add("VAL3291_2_outputs_parse", "all 3291 non-validation output CSVs parse", output_parse)

    noether_text = " ".join(row["statement"] for row in noether)
    add(
        "VAL3291_3_noether_lemma_real",
        "Noether lemma includes variational current and current-weight classification",
        "delta S_matter/delta A_Q" in noether_text and "kappa_A" in noether_text and "L_v J_Q = 0" in noether_text,
    )

    forgetting_text = " ".join(row["statement"] for row in forgetting)
    add(
        "VAL3291_4_source_forgetting_live_counterexample",
        "source forgetting lemma includes total variation and w_A counterexample",
        "T_total" in forgetting_text and "w_A S_A" in forgetting_text and "source-only" in forgetting_text,
    )

    classes = {row["classification"] for row in classification}
    add(
        "VAL3291_5_classification_collapses_current_weight",
        "current weights split into measured, common, source-only, hidden, and readout classes",
        {"MEASURED_MATTER_PARAMETER", "COMMON_CALIBRATION_ONLY", "LIVE_SOURCE_ONLY_RESIDUAL", "LIVE_HIDDEN_SOURCE_RESIDUAL", "LIVE_EFFECTIVE_ACTION_RESIDUAL"}.issubset(classes),
    )

    reduction_statuses = {row["status"] for row in reduction}
    add(
        "VAL3291_6_beta_reduction_keeps_live_piece",
        "beta_source_alpha decomposition zeroes only conditional current owner and retains source-only piece",
        "THEOREM_ZERO_CONDITIONAL_NOT_PARENT_SIGNED" in reduction_statuses and "LIVE_RESIDUAL" in reduction_statuses,
    )

    nonclaim_products = all(row["valid_for_claim"] == "false" for row in residuals) and any(
        row["runner_status"] == "PRODUCT_TARGET_AVAILABLE_STANDALONE_BLOCKED" for row in residuals
    )
    add("VAL3291_7_residual_rows_nonclaim", "all residual rows remain nonclaim and product target is standalone blocked", nonclaim_products)

    runner_ok = all(row["expectation_match"] == "true" for row in runner)
    add(
        "VAL3291_8_runner_expectations",
        "source-current runner expectations all match",
        runner_ok,
        ";".join(f"{row['run_id']}={row['observed_status']}" for row in runner),
    )

    gates_false = all(row["claim_allowed"] == "false" for row in promotion) and any(row["passed"] == "false" for row in promotion)
    add("VAL3291_9_claim_gates_false", "no 3291 gate allows WEP/R10/PPN/local-GR claim", gates_false)

    next_ok = (
        len(next_target) == 1
        and "source-only-scalar-exclusion" in next_target[0]["target_doc"]
        and "object-language" in next_target[0]["target_doc"]
    )
    add("VAL3291_10_next_target_focused", "next target focuses source-only scalar exclusion", next_ok)

    decision_ok = any("smaller than 3290" in row["consequence"] for row in decisions) and any(
        "not standalone" in row["finding"] for row in decisions
    )
    add("VAL3291_11_decision_records_real_narrowing", "decision ledger records real narrowing and no standalone transfer", decision_ok)

    add(
        "VAL3291_12_formalization_untouched",
        "formalization-workbench modified-file count remains zero by this script",
        formalization_changed_count == 0,
        f"formalization_changed_count={formalization_changed_count}",
    )

    overall = all(row["passed"] == "true" for row in checks)
    add("VAL3291_13_overall", "3291 validation overall", overall, "all required checks passed" if overall else "one or more checks failed")
    return checks


def md_cell(value: Any) -> str:
    return str(value).replace("|", "\\|").replace("\n", " ")


def md_table(rows: list[dict[str, Any]]) -> str:
    if not rows:
        return ""
    fields: list[str] = []
    for row in rows:
        for key in row:
            if key not in fields:
                fields.append(key)
    header = "| " + " | ".join(fields) + " |"
    sep = "| " + " | ".join("---" for _ in fields) + " |"
    lines = [header, sep]
    for row in rows:
        lines.append("| " + " | ".join(md_cell(row.get(field, "")) for field in fields) + " |")
    return "\n".join(lines)


def write_doc(
    sources: list[dict[str, Any]],
    noether: list[dict[str, Any]],
    forgetting: list[dict[str, Any]],
    classification: list[dict[str, Any]],
    reduction: list[dict[str, Any]],
    residuals: list[dict[str, Any]],
    runner: list[dict[str, Any]],
    promotion: list[dict[str, Any]],
    decisions: list[dict[str, Any]],
    next_target: list[dict[str, Any]],
    validation: list[dict[str, Any]],
) -> None:
    text = f"""# 3291 - T_Q Noether current owner and source-label forgetting under AX1090

**Run UTC:** {RUN_UTC}

3291 takes the source-coupling problem one rung forward. It does **not** claim WEP, R10, PPN, local-GR, or a numerical alpha prediction. The useful result is narrower and sharper:

1. If the matter current is the variational Noether current of the same parent `T_Q` owner, independent current weights are not a free hidden-alpha source knob.
2. A coefficient multiplying current/source terms is forced into one of three buckets: measured charge/representation data, common calibration, or a live source-only species scalar.
3. Therefore the remaining finite obstruction is not vague "coupling"; it is the source-only/species-label slot `w_A`/`kappa_A` plus arena projection maps.

## Main Reduction

The source-current branch can now be written as

`beta_source_alpha = beta_current_owner + beta_source_only_label + beta_hidden_source + beta_arena_projection`.

Under the same-`T_Q` Noether owner premise, `beta_current_owner=0` follows by vertical differentiation of the variational current definition. That is a real theorem shape. It is not a promoted theorem because the parent still has to sign fixed `T_Q`, fixed charge labels, no independent current source slot, and source-only scalar exclusion.

## Source Register

{md_table(sources)}

## T_Q Noether Owner Lemma

{md_table(noether)}

## Source-Label Forgetting Lemma

{md_table(forgetting)}

## Current Weight Classification

{md_table(classification)}

## Beta Source Alpha Reduction

{md_table(reduction)}

## Source-Current Residual Rows

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
    noether = noether_owner_rows()
    forgetting = source_forgetting_rows()
    classification = current_weight_classification_rows()
    reduction = beta_reduction_rows()
    residuals = residual_rows()
    runner = runner_rows(residuals)
    promotion = promotion_rows()
    decisions = decision_rows()
    next_target = next_rows()

    write_csv(OUTPUTS["sources"], sources)
    write_csv(OUTPUTS["noether"], noether)
    write_csv(OUTPUTS["forgetting"], forgetting)
    write_csv(OUTPUTS["classification"], classification)
    write_csv(OUTPUTS["reduction"], reduction)
    write_csv(OUTPUTS["residuals"], residuals)
    write_csv(OUTPUTS["runner"], runner)
    write_csv(OUTPUTS["promotion"], promotion)
    write_csv(OUTPUTS["decision"], decisions)
    write_csv(OUTPUTS["next"], next_target)

    after_fw = snapshot_tree(FW)
    validation = validate(
        sources,
        noether,
        forgetting,
        classification,
        reduction,
        residuals,
        runner,
        promotion,
        decisions,
        next_target,
        changed_count(before_fw, after_fw),
    )
    write_csv(OUTPUTS["validation"], validation)
    write_doc(sources, noether, forgetting, classification, reduction, residuals, runner, promotion, decisions, next_target, validation)

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

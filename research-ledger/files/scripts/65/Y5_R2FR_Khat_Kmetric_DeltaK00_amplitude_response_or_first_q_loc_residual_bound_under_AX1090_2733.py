from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


SCRIPT_START_UTC = datetime.now(timezone.utc)

ROOT = Path(__file__).resolve().parents[1]
RESIDUALS = ROOT / "source-intake" / "mts_residuals"
LOCAL_BOUNDS = ROOT / "source-intake" / "local_bounds"
SOURCE_WEIGHT = ROOT / "source-intake" / "source-weight"
RAB_QUEUE = ROOT / "source-intake" / "rab-sector" / "acquisition-queue"
FORMALIZATION = ROOT.parent / "formalization-workbench"

DOC = ROOT / "2733-Y5-R2FR-Khat-Kmetric-DeltaK00-amplitude-response-or-first-q_loc-residual-bound-under-AX1090.md"

OUTPUTS = {
    "sources": RESIDUALS / "P8_Y5_R2FR_2733_SOURCE_REGISTER.csv",
    "identity": RESIDUALS / "P8_Y5_R2FR_2733_TENSOR_IDENTITY_SPLIT.csv",
    "amplitude": RESIDUALS / "P8_Y5_R2FR_2733_DELTAK00_AMPLITUDE_LAW.csv",
    "qbound": RESIDUALS / "P8_Y5_R2FR_2733_QLOC_RESIDUAL_BOUND_INTERFACE.csv",
    "zero_gate": RESIDUALS / "P8_Y5_R2FR_2733_ZERO_THEOREM_GATE.csv",
    "residuals": RESIDUALS / "P8_Y5_R2FR_2733_RETAINED_RESIDUAL_ROWS.csv",
    "decisions": RESIDUALS / "P8_Y5_R2FR_2733_DECISION_LEDGER.csv",
    "gates": RESIDUALS / "P8_Y5_R2FR_2733_CLAIM_GATES.csv",
    "next": RESIDUALS / "P8_Y5_R2FR_2733_NEXT_TARGET.csv",
    "branches": RESIDUALS / "P8_Y5_R2FR_2733_BRANCH_COPIES.csv",
    "validation": RESIDUALS / "P8_Y5_BRR545_2733_VALIDATION.csv",
}

BRANCH_OUTPUTS = {
    "qbound": LOCAL_BOUNDS / "Khat_q_loc_residual_bound_2733_NONCLAIM.csv",
    "reopen": SOURCE_WEIGHT / "Kmetric_kernel_reopen_conditions_2733_NONCLAIM.csv",
    "next_queue": RAB_QUEUE / "JR2733_LCG_METRIC_SILENCE_OR_ML_KERNEL_NEXT.csv",
}


def ts() -> str:
    return datetime.now(timezone.utc).isoformat()


def ensure_dirs() -> None:
    for path in {p.parent for p in OUTPUTS.values()} | {p.parent for p in BRANCH_OUTPUTS.values()}:
        path.mkdir(parents=True, exist_ok=True)


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    if not rows:
        raise ValueError(f"refusing empty CSV: {path}")
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
    with path.open("r", newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def markdown_table(rows: list[dict[str, Any]], cols: list[str]) -> str:
    header = "| " + " | ".join(cols) + " |"
    sep = "| " + " | ".join("---" for _ in cols) + " |"
    body = [
        "| " + " | ".join(str(row.get(col, "")).replace("\n", " ") for col in cols) + " |"
        for row in rows
    ]
    return "\n".join([header, sep, *body])


def source_rows() -> list[dict[str, Any]]:
    specs = [
        (
            "SRC2733_0_2732_handoff",
            "2732 selects Khat/Kmetric/DeltaK/q_loc as primary next branch",
            DOC.parent / "2732-Y5-R2FR-local-GR-route-rollup-after-memory-closure-only-or-next-derivation-branch.md",
            ["NEXT2732_0_selected", "ROUTE2732_0_Khat_q_loc_tensor", "VAL2732_OVERALL"],
        ),
        (
            "SRC2733_1_2712_qloc_deltak",
            "q_loc and DeltaK status ledger",
            RESIDUALS / "P8_Y5_R2FR_2712_QLOC_DELTAK_STATUS.csv",
            ["QDK2712_2_DeltaK", "DELTAK_00_NOT_COMPUTABLE_YET"],
        ),
        (
            "SRC2733_2_1526_outcome",
            "tracefree improvement action outcome runner",
            RESIDUALS / "P8_Y5_PARENT_QLOC_1526_DELTAK_OUTCOME_RUNNER.csv",
            ["OUT1526_1_current_status", "BLOCKED_NOT_PROMOTED"],
        ),
        (
            "SRC2733_3_1527_adoption",
            "current Khat adoption row",
            RESIDUALS / "P8_Y5_PARENT_QLOC_1527_KHAT_ADOPTION_ROW.csv",
            ["KAD1527_4_verdict", "STAGED_NOT_PROMOTED"],
        ),
        (
            "SRC2733_4_1530_delta_g",
            "delta_g S_Gamma reduction to Kmetric kernels",
            RESIDUALS / "P8_Y5_PARENT_QLOC_1530_DELTA_G_SGAMMA_REDUCTION.csv",
            ["DGS1530_3_norm_envelope", "NOT_NUMERIC_REDUCED_TO_KERNELS"],
        ),
        (
            "SRC2733_5_1530_projection",
            "observable projection contract",
            RESIDUALS / "P8_Y5_PARENT_QLOC_1530_OBSERVABLE_PROJECTION_CONTRACT.csv",
            ["OBS1530_4_verdict", "NOT_SCORE_READY"],
        ),
        (
            "SRC2733_6_1531_envelope",
            "delta_g S_Gamma bound envelope",
            RESIDUALS / "P8_Y5_PARENT_QLOC_1531_DELTAG_SGAMMA_BOUND_ENVELOPE.csv",
            ["ENV1531_4_M_L_pruning", "NEXT_CRITICAL_PRUNING_TARGET"],
        ),
        (
            "SRC2733_7_1531_kernel_audit",
            "Kmetric kernel norm source audit",
            RESIDUALS / "P8_Y5_PARENT_QLOC_1531_KMETRIC_KERNEL_NORM_SOURCE_AUDIT.csv",
            ["KNA1531_5_M_L", "MISSING_PARENT_OWNERSHIP", "KNA1531_6_K_conn"],
        ),
        (
            "SRC2733_8_2714_adoption_gate",
            "Khat adoption gate",
            RESIDUALS / "P8_Y5_R2FR_2714_KHAT_ADOPTION_GATE.csv",
            ["KAG2714_2_DeltaK", "BLOCKED"],
        ),
        (
            "SRC2733_9_2714_multiplier_bound",
            "lambda_phi multiplier bound rollforward",
            RESIDUALS / "P8_Y5_R2FR_2714_MULTIPLIER_BOUND_ROLLFORWARD.csv",
            ["MBR2714_1_delta_g_SGamma", "REDUCED_TO_KMETRIC_KERNEL_NORMS"],
        ),
        (
            "SRC2733_10_2699_ward_identity",
            "Gamma/Khat/q_loc Ward identity and residual demotion",
            DOC.parent / "2699-Y5-R2FR-Gamma-Khat-q-loc-first-variation-or-official-residual-demotion.md",
            ["WID2699_0_definition", "NRD2699_0_metric_response", "PSG2699_8_all_or_nothing"],
        ),
    ]
    rows: list[dict[str, Any]] = []
    for source_id, description, path, needles in specs:
        exists = path.exists()
        text = path.read_text(encoding="utf-8", errors="ignore") if exists else ""
        missing = [needle for needle in needles if needle not in text]
        rows.append(
            {
                "source_id": source_id,
                "description": description,
                "source_path": str(path),
                "exists": exists,
                "needles_present": not missing,
                "missing_needles": ";".join(missing),
                "valid_for_claim": False,
            }
        )
    return rows


def identity_rows() -> list[dict[str, Any]]:
    return [
        {
            "identity_id": "ID2733_0_q_definition",
            "statement": "q_loc is the projected mismatch between scalar gradient and Khat divergence",
            "formula": "q_loc^nu=P_loc(nabla^nu Gamma_eff-nabla_mu Khat^{mu nu})",
            "derivation_status": "IMPORTED_EXACT_DEFINITION",
            "source_anchor": "2712 QDK2712_0; 2699 WID2699_0",
            "valid_for_claim": False,
        },
        {
            "identity_id": "ID2733_1_Khat_split",
            "statement": "split current Khat into parent metric response plus mismatch",
            "formula": "Khat^{mu nu}=Kmetric^{mu nu}[Gamma_eff]+Delta_K^{mu nu}",
            "derivation_status": "STRUCTURAL_SPLIT_WRITTEN",
            "source_anchor": "2712 QDK2712_1/QDK2712_2",
            "valid_for_claim": False,
        },
        {
            "identity_id": "ID2733_2_q_split",
            "statement": "separate Ward-owned q source from current-symbol Khat mismatch",
            "formula": "q_loc^nu=P_loc(W_metric^nu-nabla_mu Delta_K^{mu nu}), W_metric^nu:=nabla^nu Gamma_eff-nabla_mu Kmetric^{mu nu}[Gamma_eff]",
            "derivation_status": "DERIVED_ALGEBRAIC_SPLIT",
            "source_anchor": "2699 Ward identity plus 2712 DeltaK split",
            "valid_for_claim": False,
        },
        {
            "identity_id": "ID2733_3_zero_condition",
            "statement": "q_loc theorem-zero requires both parent Ward silence and DeltaK silence",
            "formula": "q_loc=0 if P_loc W_metric=0 and P_loc nabla_mu Delta_K^{mu nu}=0",
            "derivation_status": "EXACT_CONDITION_NOT_SATISFIED",
            "source_anchor": "2699 PSG2699_8; 2714 KAG2714_2",
            "valid_for_claim": False,
        },
    ]


def amplitude_rows() -> list[dict[str, Any]]:
    return [
        {
            "law_id": "DKA2733_0_component_split",
            "quantity": "Delta_K00",
            "formula_or_bound": "Delta_K00=Delta_adopt00+Delta_lambda00+Delta_kernel00+Delta_boundary00+Delta_convention00",
            "status": "DECOMPOSITION_READY_VALUES_MISSING",
            "missing_inputs": "live Khat adoption; lambda_phi zero/bound; Kmetric kernel norms; boundary convention; sign/volume convention",
            "score_ready": False,
            "valid_for_claim": False,
        },
        {
            "law_id": "DKA2733_1_adoption_mismatch",
            "quantity": "Delta_adopt00",
            "formula_or_bound": "|Delta_adopt00| <= |1-sigma_resp*c_I| |K_L00| + |K_unmatched00|",
            "status": "CONTRACT_ONLY",
            "missing_inputs": "sigma_resp*c_I live adoption; K_L00 normalization; current-MTS Khat symbol match",
            "score_ready": False,
            "valid_for_claim": False,
        },
        {
            "law_id": "DKA2733_2_multiplier_stress",
            "quantity": "Delta_lambda00",
            "formula_or_bound": "|Delta_lambda00| <= epsilon_lambda_phi",
            "status": "BOUND_FORM_ONLY",
            "missing_inputs": "C_P; C_E; C_T; R_norm; boundary_source_norm; initial/static exclusion; delta_g_SGamma_norm; observable projection",
            "score_ready": False,
            "valid_for_claim": False,
        },
        {
            "law_id": "DKA2733_3_kmetric_kernel_envelope",
            "quantity": "Delta_kernel00",
            "formula_or_bound": "||Delta_kernel|| <= (2/3)(L_cg^-2|F_prime|||M_m||+2L_cg^-3|F|||M_L||+||K_conn||+||K_domain||+||K_boundary||+||K_C||)",
            "status": "SYMBOLIC_ABSOLUTE_ENVELOPE",
            "missing_inputs": "L_cg; F; F_prime; M_m; M_L; K_conn; K_domain; K_boundary; K_C; units",
            "score_ready": False,
            "valid_for_claim": False,
        },
        {
            "law_id": "DKA2733_4_cleanest_pruning",
            "quantity": "M_L channel",
            "formula_or_bound": "M_L term vanishes only if L_cg is parent-fixed/metric-silent or F(m_*)=0 in the same branch",
            "status": "NEXT_CRITICAL_PRUNING_TARGET",
            "missing_inputs": "L_cg ownership theorem or explicit M_L norm",
            "score_ready": False,
            "valid_for_claim": False,
        },
        {
            "law_id": "DKA2733_5_no_cancellation",
            "quantity": "absolute DeltaK00 envelope",
            "formula_or_bound": "|Delta_K00| <= |Delta_adopt00|+|Delta_lambda00|+|Delta_kernel00|+|Delta_boundary00|+|Delta_convention00|",
            "status": "GUARDRAIL_PASS",
            "missing_inputs": "component values still absent; no sign cancellation allowed",
            "score_ready": False,
            "valid_for_claim": False,
        },
    ]


def qbound_rows() -> list[dict[str, Any]]:
    return [
        {
            "bound_id": "QB2733_0_vector_envelope",
            "quantity": "||q_loc||_D",
            "bound_form": "||q_loc|| <= ||P_loc|| (||W_metric|| + C_div ||Delta_K|| + ||[P_loc,nabla]Delta_K||)",
            "known_status": "DERIVED_BOUND_INTERFACE",
            "missing_inputs": "P_loc operator norm; W_metric Ward defect; divergence/domain constant C_div; Delta_K component norms; projector commutator",
            "score_ready": False,
            "valid_for_claim": False,
        },
        {
            "bound_id": "QB2733_1_00_projection",
            "quantity": "q_loc component sourced by Delta_K00",
            "bound_form": "||q_loc||_00 <= ||P_loc|| (C_0 ||partial_0 Delta_K00|| + C_i ||partial_i Delta_K00|| + component-mixing terms)",
            "known_status": "SCHEMA_ONLY_STATIC_REDUCTION_NOT_SIGNED",
            "missing_inputs": "static/stationary domain rule; component mixing; derivative scale; units; local projection",
            "score_ready": False,
            "valid_for_claim": False,
        },
        {
            "bound_id": "QB2733_2_observable_projection",
            "quantity": "PPN/R10/clock/orbital readout",
            "bound_form": "residual_arena <= K_arena ||q_loc|| or K_arena ||Delta_K||",
            "known_status": "PROJECTION_MISSING",
            "missing_inputs": "K_PPN; K_R10; K_clock; K_orbital; source normalization",
            "score_ready": False,
            "valid_for_claim": False,
        },
        {
            "bound_id": "QB2733_3_verdict",
            "quantity": "first q_loc residual bound",
            "bound_form": "symbolic envelope exists but no numeric/source-backed score row exists",
            "known_status": "NOT_SCORE_READY_REDUCED_TO_KERNELS",
            "missing_inputs": "M_L first, then M_m/K_conn/K_domain/K_boundary/lambda_phi/projections",
            "score_ready": False,
            "valid_for_claim": False,
        },
    ]


def zero_gate_rows() -> list[dict[str, Any]]:
    return [
        {
            "gate_id": "ZG2733_0_parent_metric_response",
            "required_zero_clause": "Khat equals Kmetric[Gamma_eff] in the same parent branch",
            "current_status": "BLOCKED",
            "reason": "Khat adoption row is staged/nonclaim and DeltaK remains retained",
            "zero_claim_pass": False,
            "valid_for_claim": False,
        },
        {
            "gate_id": "ZG2733_1_lambda_phi",
            "required_zero_clause": "lambda_phi stress is zero or bounded below all local channels",
            "current_status": "BLOCKED",
            "reason": "lambda_phi zero route and finite bound lack source-backed constants",
            "zero_claim_pass": False,
            "valid_for_claim": False,
        },
        {
            "gate_id": "ZG2733_2_kmetric_kernels",
            "required_zero_clause": "M_m, M_L, K_conn, K_domain, K_boundary and K_C vanish or are bounded",
            "current_status": "BLOCKED",
            "reason": "1531 reduces the problem to kernel norms, with M_L the critical next pruning target",
            "zero_claim_pass": False,
            "valid_for_claim": False,
        },
        {
            "gate_id": "ZG2733_3_Ward_silence",
            "required_zero_clause": "W_metric is a silent parent Ward term",
            "current_status": "BLOCKED",
            "reason": "Euler/source/boundary/readout/projector gates from 2699 are unsigned",
            "zero_claim_pass": False,
            "valid_for_claim": False,
        },
        {
            "gate_id": "ZG2733_4_all",
            "required_zero_clause": "all DeltaK and Ward gates close in one parent branch",
            "current_status": "THEOREM_ZERO_FALSE_CURRENT_CORPUS",
            "reason": "multiple required clauses are blocked and no score-ready bound exists",
            "zero_claim_pass": False,
            "valid_for_claim": False,
        },
    ]


def residual_rows() -> list[dict[str, Any]]:
    return [
        {
            "residual_id": "RES2733_0_DeltaK00",
            "symbol": "E_DeltaK00",
            "definition": "absolute retained 00-component mismatch between current Khat and parent Kmetric[Gamma_eff]",
            "formula": "|Delta_K00| envelope from DKA2733_5",
            "status": "ACTIVE_NONCLAIM",
            "next_input": "M_L zero theorem or norm first",
            "valid_for_claim": False,
        },
        {
            "residual_id": "RES2733_1_q_loc",
            "symbol": "E_q_loc_tensor",
            "definition": "projected Ward-plus-DeltaK residual vector",
            "formula": "||q_loc|| <= ||P_loc||(||W_metric||+C_div||Delta_K||+commutator)",
            "status": "ACTIVE_NONCLAIM",
            "next_input": "P_loc norm and DeltaK component norms",
            "valid_for_claim": False,
        },
        {
            "residual_id": "RES2733_2_lambda_phi",
            "symbol": "E_lambda_phi",
            "definition": "multiplier-stress contribution introduced by local phiR auxiliary route",
            "formula": "epsilon_lambda_phi bound from MBR2714_0",
            "status": "ACTIVE_NONCLAIM",
            "next_input": "source-backed constants and observable projection",
            "valid_for_claim": False,
        },
        {
            "residual_id": "RES2733_3_ML",
            "symbol": "E_M_Lcg",
            "definition": "metric response of L_cg inside Gamma_eff=L_cg^-2 F(m)",
            "formula": "2L_cg^-3 |F| ||M_L|| contribution",
            "status": "PRIMARY_NEXT_RESIDUAL_OR_ZERO",
            "next_input": "prove L_cg metric-silent or source ||M_L||",
            "valid_for_claim": False,
        },
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        {
            "decision_id": "DEC2733_0_zero_rejected_now",
            "decision": "NO_QLOC_OR_DELTAK_ZERO_CLAIM",
            "because": "Khat adoption, lambda_phi, Kmetric kernels and Ward silence are all unsigned",
            "effect": "retain DeltaK/q_loc residual vector",
            "valid_for_claim": False,
        },
        {
            "decision_id": "DEC2733_1_bound_interface_kept",
            "decision": "SYMBOLIC_BOUND_INTERFACE_WRITTEN",
            "because": "DeltaK00 and q_loc can be bounded as a sum of named defect channels",
            "effect": "future data/local tests must wait for source-backed coefficients",
            "valid_for_claim": False,
        },
        {
            "decision_id": "DEC2733_2_next_kernel",
            "decision": "SELECT_LCG_METRIC_SILENCE_OR_ML_KERNEL",
            "because": "1531 identifies M_L as the cleanest next algebraic pruning target; F_prime=0 does not touch L_cg response",
            "effect": "next checkpoint should prove L_cg parent-fixed/metric-silent or create first M_L norm row",
            "valid_for_claim": False,
        },
    ]


def gate_rows() -> list[dict[str, Any]]:
    claims = [
        ("CG2733_0_DeltaK_zero", "Delta_K00=0", "Khat adoption/lambda/kernel gates fail"),
        ("CG2733_1_q_loc_zero", "q_loc=0", "requires both Ward silence and DeltaK silence"),
        ("CG2733_2_q_loc_bound_score", "score-ready q_loc bound", "bound interface has symbolic missing coefficients"),
        ("CG2733_3_PPN", "PPN/local-GR pass", "observable projection and source normalization missing"),
        ("CG2733_4_Newton", "Newton/local-GR pass", "tensor residual still active"),
        ("CG2733_5_public", "public claim", "private derivation/residual checkpoint only"),
    ]
    return [
        {
            "claim_gate_id": gate_id,
            "claim": claim,
            "gate_passed": False,
            "claim_allowed": False,
            "valid_for_claim": False,
            "reason": reason,
        }
        for gate_id, claim, reason in claims
    ]


def next_rows() -> list[dict[str, Any]]:
    return [
        {
            "next_id": "NEXT2733_0_selected",
            "status": "selected_primary",
            "target_doc": "2734-Y5-R2FR-Lcg-metric-silence-or-first-ML-kernel-norm-row-under-AX1090.md",
            "target_script": "scripts/Y5_R2FR_Lcg_metric_silence_or_first_ML_kernel_norm_row_under_AX1090_2734.py",
            "mission": "attack the M_L contribution in DeltaK/q_loc: prove L_cg is parent-fixed/metric-silent in the local branch or stage a source-backed M_L norm row",
            "acceptance": "one of: L_cg metric-silence theorem; finite M_L norm/source row; or explicit blocker ledger naming missing parent L_cg ownership",
            "forbidden": "using F_prime=0 to erase L_cg response; numeric local-test score from placeholders; GitHub action; formalization-workbench edits",
            "selected": True,
            "valid_for_claim": False,
        }
    ]


def branch_rows() -> list[dict[str, Any]]:
    return [
        {
            "copy_id": "COPY2733_0_qbound",
            "source_table": str(OUTPUTS["qbound"]),
            "copy_path": str(BRANCH_OUTPUTS["qbound"]),
            "purpose": "local bounds branch receives q_loc/DeltaK bound interface",
            "exists": BRANCH_OUTPUTS["qbound"].exists(),
            "valid_for_claim": False,
        },
        {
            "copy_id": "COPY2733_1_reopen",
            "source_table": str(OUTPUTS["zero_gate"]),
            "copy_path": str(BRANCH_OUTPUTS["reopen"]),
            "purpose": "source-weight branch receives kernel zero/reopen conditions",
            "exists": BRANCH_OUTPUTS["reopen"].exists(),
            "valid_for_claim": False,
        },
        {
            "copy_id": "COPY2733_2_next_queue",
            "source_table": str(OUTPUTS["next"]),
            "copy_path": str(BRANCH_OUTPUTS["next_queue"]),
            "purpose": "queues L_cg metric-silence or M_L kernel target",
            "exists": BRANCH_OUTPUTS["next_queue"].exists(),
            "valid_for_claim": False,
        },
    ]


def formalization_recent_count() -> int:
    if not FORMALIZATION.exists():
        return 0
    count = 0
    for path in FORMALIZATION.rglob("*"):
        if path.is_file():
            modified = datetime.fromtimestamp(path.stat().st_mtime, timezone.utc)
            if modified > SCRIPT_START_UTC:
                count += 1
    return count


def validation_rows(
    sources: list[dict[str, Any]],
    identity: list[dict[str, Any]],
    amplitude: list[dict[str, Any]],
    qbound: list[dict[str, Any]],
    zero_gate: list[dict[str, Any]],
    gates: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    source_ok = all(row["exists"] is True and row["needles_present"] is True for row in sources)
    identity_ok = any(row["identity_id"] == "ID2733_2_q_split" for row in identity)
    amplitude_ok = any(row["law_id"] == "DKA2733_5_no_cancellation" for row in amplitude) and all(row["score_ready"] is False for row in amplitude)
    qbound_ok = any(row["bound_id"] == "QB2733_0_vector_envelope" for row in qbound) and all(row["score_ready"] is False for row in qbound)
    zero_false = all(row["zero_claim_pass"] is False for row in zero_gate)
    gates_false = all(row["gate_passed"] is False and row["claim_allowed"] is False for row in gates)
    branch_ok = all(path.exists() for path in BRANCH_OUTPUTS.values())
    formalization_ok = formalization_recent_count() == 0
    csv_ok = True
    csv_bits = []
    for key, path in {**OUTPUTS, **BRANCH_OUTPUTS}.items():
        if key == "validation":
            continue
        try:
            rows = read_csv(path)
            csv_bits.append(f"{path.name}:{len(rows)}:ok")
        except Exception as exc:
            csv_ok = False
            csv_bits.append(f"{path.name}:ERROR:{exc}")
    rows = [
        {"validation_id": "VAL2733_0_sources", "passed": source_ok, "detail": "all source paths exist and needles are present", "timestamp_utc": ts()},
        {"validation_id": "VAL2733_1_identity_split", "passed": identity_ok, "detail": "q_loc split into Ward and DeltaK pieces", "timestamp_utc": ts()},
        {"validation_id": "VAL2733_2_amplitude_law", "passed": amplitude_ok, "detail": "DeltaK00 no-cancellation amplitude law exists and is non-score-ready", "timestamp_utc": ts()},
        {"validation_id": "VAL2733_3_qbound_interface", "passed": qbound_ok, "detail": "q_loc residual bound interface exists and remains non-score-ready", "timestamp_utc": ts()},
        {"validation_id": "VAL2733_4_zero_claims_false", "passed": zero_false, "detail": "all zero theorem gates fail current corpus", "timestamp_utc": ts()},
        {"validation_id": "VAL2733_5_claim_gates_false", "passed": gates_false, "detail": "all local/test/public claim gates remain false", "timestamp_utc": ts()},
        {"validation_id": "VAL2733_6_branch_outputs", "passed": branch_ok, "detail": "branch copies exist", "timestamp_utc": ts()},
        {"validation_id": "VAL2733_7_csv_parse", "passed": csv_ok, "detail": "; ".join(csv_bits), "timestamp_utc": ts()},
        {"validation_id": "VAL2733_8_formalization_untouched", "passed": formalization_ok, "detail": f"formalization-workbench recent modified-file count since script start = {formalization_recent_count()}", "timestamp_utc": ts()},
    ]
    rows.append(
        {
            "validation_id": "VAL2733_OVERALL",
            "passed": all(row["passed"] is True for row in rows),
            "detail": "2733 derives the symbolic DeltaK00/q_loc residual interface, rejects zero/score claims, and selects L_cg/M_L as the next kernel target",
            "timestamp_utc": ts(),
        }
    )
    return rows


def write_doc(data: dict[str, list[dict[str, Any]]]) -> None:
    DOC.write_text(
        f"""# 2733 - Y5 R2/f(R): Khat/Kmetric DeltaK00 Amplitude Response Or First q_loc Residual Bound Under AX1090

Status: `Y5_R2FR_2733_DeltaK00_q_loc_symbolic_bound_interface_selects_Lcg_ML_next_nonclaim`

## Private Verdict

2733 gets the Khat/q_loc route out of fog and into an equation. The exact split is:

`Khat = Kmetric[Gamma_eff] + Delta_K`, so `q_loc = P_loc(W_metric - div Delta_K)`.

That is progress because it separates two different debts: parent Ward silence in `W_metric`, and current-symbol mismatch in `Delta_K`. But it is not a local-GR win. `Delta_K00` still contains staged Khat adoption, lambda_phi stress, Kmetric kernel norms, boundary/convention pieces, and no-cancellation guards. The first real q_loc bound is therefore symbolic only.

Best next punch: attack the `M_L`/`L_cg` metric-response channel. If `L_cg` is parent-fixed/metric-silent locally, a whole term in the DeltaK/q_loc envelope drops. If not, `M_L` becomes the first source-ready finite residual row.

No local-GR, Newton, PPN, R10, WEP, clock, orbital, DeltaK-zero, q_loc-zero, or public claim follows from this checkpoint.

## Source Register

{markdown_table(data["sources"], ["source_id", "description", "source_path", "exists", "needles_present", "missing_needles", "valid_for_claim"])}

## Tensor Identity Split

{markdown_table(data["identity"], ["identity_id", "statement", "formula", "derivation_status", "source_anchor", "valid_for_claim"])}

## DeltaK00 Amplitude Law

{markdown_table(data["amplitude"], ["law_id", "quantity", "formula_or_bound", "status", "missing_inputs", "score_ready", "valid_for_claim"])}

## q_loc Residual Bound Interface

{markdown_table(data["qbound"], ["bound_id", "quantity", "bound_form", "known_status", "missing_inputs", "score_ready", "valid_for_claim"])}

## Zero Theorem Gate

{markdown_table(data["zero_gate"], ["gate_id", "required_zero_clause", "current_status", "reason", "zero_claim_pass", "valid_for_claim"])}

## Retained Residual Rows

{markdown_table(data["residuals"], ["residual_id", "symbol", "definition", "formula", "status", "next_input", "valid_for_claim"])}

## Decision Ledger

{markdown_table(data["decisions"], ["decision_id", "decision", "because", "effect", "valid_for_claim"])}

## Claim Gates

{markdown_table(data["gates"], ["claim_gate_id", "claim", "gate_passed", "claim_allowed", "valid_for_claim", "reason"])}

## Next Target

{markdown_table(data["next"], ["next_id", "status", "target_doc", "target_script", "mission", "acceptance", "forbidden", "selected", "valid_for_claim"])}

## Branch Copies

{markdown_table(data["branches"], ["copy_id", "source_table", "copy_path", "purpose", "exists", "valid_for_claim"])}

## Validation

{markdown_table(data["validation"], ["validation_id", "passed", "detail", "timestamp_utc"])}

## Plain-English Read

This is a useful narrowing result. We did not get `q_loc=0`, but we did force the obstruction into named tensor channels. The cleanest next channel is not memory and not broad GR rhetoric; it is whether `L_cg` actually varies with the metric in the local Hilbert variation.
""",
        encoding="utf-8",
    )


def main() -> None:
    ensure_dirs()
    sources = source_rows()
    identity = identity_rows()
    amplitude = amplitude_rows()
    qbound = qbound_rows()
    zero_gate = zero_gate_rows()
    residuals = residual_rows()
    decisions = decision_rows()
    gates = gate_rows()
    next_target = next_rows()

    write_csv(OUTPUTS["sources"], sources)
    write_csv(OUTPUTS["identity"], identity)
    write_csv(OUTPUTS["amplitude"], amplitude)
    write_csv(OUTPUTS["qbound"], qbound)
    write_csv(OUTPUTS["zero_gate"], zero_gate)
    write_csv(OUTPUTS["residuals"], residuals)
    write_csv(OUTPUTS["decisions"], decisions)
    write_csv(OUTPUTS["gates"], gates)
    write_csv(OUTPUTS["next"], next_target)

    write_csv(BRANCH_OUTPUTS["qbound"], qbound)
    write_csv(BRANCH_OUTPUTS["reopen"], zero_gate)
    write_csv(BRANCH_OUTPUTS["next_queue"], next_target)
    branches = branch_rows()
    write_csv(OUTPUTS["branches"], branches)

    validation = validation_rows(sources, identity, amplitude, qbound, zero_gate, gates)
    write_csv(OUTPUTS["validation"], validation)

    data = {
        "sources": sources,
        "identity": identity,
        "amplitude": amplitude,
        "qbound": qbound,
        "zero_gate": zero_gate,
        "residuals": residuals,
        "decisions": decisions,
        "gates": gates,
        "next": next_target,
        "branches": branches,
        "validation": validation,
    }
    write_doc(data)

    pycache = Path(__file__).resolve().parent / "__pycache__"
    if pycache.exists():
        shutil.rmtree(pycache)

    if not all(row["passed"] is True for row in validation):
        failed = [row for row in validation if row["passed"] is not True]
        raise SystemExit(f"2733 validation failed: {failed}")
    print(f"wrote {DOC}")
    print(f"validation {OUTPUTS['validation']}")


if __name__ == "__main__":
    main()

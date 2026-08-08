from __future__ import annotations

import csv
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "source-intake" / "mts_residuals"
DOC = ROOT / "3417-Y5-R2FR-q_loc-U2-alpha-vector-and-retained-beta-stress-bound-pack-under-AX1090.md"

Q_PROXY = 7.432631961576971e-06
BETA_BOUND = 7.8e-05
KAPPAV_BOUND = 2.0 * BETA_BOUND
ALPHA3_BOUND = 3.999999999999999e-20
ALPHA3_PRODUCT_LIMIT = ALPHA3_BOUND / Q_PROXY
KAPPA_Q_BETA_IF_UNIT = 2.0 * Q_PROXY
BETA_FRACTION_IF_UNIT = Q_PROXY / BETA_BOUND
KAPPAV_FRACTION_IF_UNIT = KAPPA_Q_BETA_IF_UNIT / KAPPAV_BOUND

SOURCES = {
    "doc_3416": ROOT / "3416-Y5-R2FR-parent-normal-form-EH-selector-and-hidden-stress-exclusion-under-AX1090.md",
    "residuals_3416": OUT / "P8_Y5_R2FR_3416_RESIDUAL_DEMOTION_MATRIX.csv",
    "status_3416": OUT / "P8_Y5_R2FR_3416_LOCAL_GR_STATUS.csv",
    "next_3416": OUT / "P8_Y5_R2FR_3416_NEXT_TARGET.csv",
    "neh_3409": OUT / "P8_Y5_R2FR_3409_NON_EH_RESIDUE_CHANNELS.csv",
    "denominator_3409": OUT / "P8_Y5_R2FR_3409_GR_POLE_DENOMINATOR.csv",
    "qloc_split_3410": OUT / "P8_Y5_R2FR_3410_QLOC_DECOMPOSITION_THEOREM.csv",
    "ppn_lanes_3410": OUT / "P8_Y5_R2FR_3410_PPN_LANE_SPLIT.csv",
    "alpha_bound_3410": OUT / "P8_Y5_R2FR_3410_ALPHA_VECTOR_PRODUCT_BOUND.csv",
    "ward_3411": OUT / "P8_Y5_R2FR_3411_WARD_ZERO_THEOREM.csv",
    "stress_identity_3411": OUT / "P8_Y5_R2FR_3411_STRESS_IDENTITY_PROOF.csv",
    "symbol_audit_3411": OUT / "P8_Y5_R2FR_3411_CURRENT_SYMBOL_MATCH_AUDIT.csv",
    "double_zero_3413": OUT / "P8_Y5_R2FR_3413_DOUBLE_ZERO_PROOF.csv",
    "gates_3413": OUT / "P8_Y5_R2FR_3413_PROMOTION_GATES.csv",
    "kappav_3401": OUT / "P8_Y5_R2FR_3401_KAPPAV_COMPONENT_LEDGER.csv",
    "envelope_3403": OUT / "P8_Y5_R2FR_3403_KAPPAV_REDUCED_ENVELOPE.csv",
    "hidden_stress_3416": OUT / "P8_Y5_R2FR_3416_HIDDEN_STRESS_EXCLUSION_GATE.csv",
}

OUTPUTS = {
    "source_register": OUT / "P8_Y5_R2FR_3417_SOURCE_REGISTER.csv",
    "qloc_projection_split": OUT / "P8_Y5_R2FR_3417_QLOC_PROJECTION_SPLIT.csv",
    "qloc_numeric_pressure": OUT / "P8_Y5_R2FR_3417_QLOC_NUMERIC_PRESSURE.csv",
    "retained_beta_stress_bound_pack": OUT / "P8_Y5_R2FR_3417_RETAINED_BETA_STRESS_BOUND_PACK.csv",
    "ward_zero_rescue_gates": OUT / "P8_Y5_R2FR_3417_WARD_ZERO_RESCUE_GATES.csv",
    "promotion_gates": OUT / "P8_Y5_R2FR_3417_PROMOTION_GATES.csv",
    "decision_ledger": OUT / "P8_Y5_R2FR_3417_DECISION_LEDGER.csv",
    "next_target": OUT / "P8_Y5_R2FR_3417_NEXT_TARGET.csv",
    "runner_nonclaim": OUT / "P8_Y5_R2FR_3417_RUNNER_NONCLAIM.csv",
    "validation": OUT / "P8_Y5_BRR545_3417_VALIDATION.csv",
}


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    if not rows:
        raise ValueError(f"no rows for {path}")
    path.parent.mkdir(parents=True, exist_ok=True)
    fields = list(rows[0].keys())
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def md_table(rows: list[dict[str, Any]]) -> str:
    if not rows:
        return ""
    fields = list(rows[0].keys())

    def clean(value: Any) -> str:
        return str(value).replace("\n", " ").replace("|", "/")

    lines = [
        "| " + " | ".join(fields) + " |",
        "| " + " | ".join("---" for _ in fields) + " |",
    ]
    for row in rows:
        lines.append("| " + " | ".join(clean(row.get(field, "")) for field in fields) + " |")
    return "\n".join(lines)


def source_register() -> list[dict[str, Any]]:
    roles = {
        "doc_3416": "selector/stress gate selecting q_loc U2/alpha-vector bound pack",
        "residuals_3416": "q_loc vector and retained non-EH residual demotion rows",
        "status_3416": "local-GR status naming q_loc/full PPN gates",
        "next_3416": "declared 3417 target",
        "neh_3409": "q_loc as non-EH residue channel relative to GR pole",
        "denominator_3409": "conditional GR pole denominator D_GR",
        "qloc_split_3410": "kinematic/Hodge q_loc split",
        "ppn_lanes_3410": "PPN lane routing and current statuses",
        "alpha_bound_3410": "alpha3 product pressure bound",
        "ward_3411": "conditional q_loc Ward-zero theorem",
        "stress_identity_3411": "q_loc as projected stress divergence",
        "symbol_audit_3411": "current Gamma/Khat symbol-match failures",
        "double_zero_3413": "formal response-doublet double-zero proof and limits",
        "gates_3413": "q_loc local-GR promotion still blocked",
        "kappav_3401": "q_loc beta guard in kappa_v component ledger",
        "envelope_3403": "reduced kappa_v envelope after eta/source-square zeroes",
        "hidden_stress_3416": "hidden stress and q_loc T_GK safe-class gate",
    }
    return [
        {
            "source_id": source_id,
            "path": str(path),
            "exists": path.exists(),
            "role": roles[source_id],
            "valid_for_claim": False,
        }
        for source_id, path in SOURCES.items()
    ]


def qloc_projection_split() -> list[dict[str, Any]]:
    return [
        {
            "projection_id": "QPS3417_0_decomposition",
            "lane": "identity",
            "mathematical_form": "q_loc^nu=q_parallel u^nu + D^nu chi_q + q_T^nu + q_harmonic^nu",
            "observable": "routing identity",
            "status": "KINEMATIC_SPLIT_ONLY",
            "claim_effect": "prevents beta-only scalar number being reused as vector safety",
            "valid_for_claim": False,
        },
        {
            "projection_id": "QPS3417_1_scalar_beta",
            "lane": "scalar U2 beta",
            "mathematical_form": "delta_beta_q = W_q_beta f_beta q_proxy",
            "observable": "beta-1 and kappa_q=2 delta_beta_q",
            "status": "PROVISIONAL_SMALL_IF_UNIT_WEIGHT",
            "claim_effect": "can enter beta envelope only if U2/readout normalization is parent-signed",
            "valid_for_claim": False,
        },
        {
            "projection_id": "QPS3417_2_scalar_gamma",
            "lane": "scalar gamma/spatial slip",
            "mathematical_form": "delta_gamma_q = W_q_gamma f_gamma q_proxy",
            "observable": "gamma-1",
            "status": "UNSCORED_MISSING_W_AND_F",
            "claim_effect": "gamma cannot be inferred from beta",
            "valid_for_claim": False,
        },
        {
            "projection_id": "QPS3417_3_alpha1_alpha2",
            "lane": "transverse preferred-frame vector",
            "mathematical_form": "alpha{1,2}_q = W_q_alpha{1,2} f_qV q_proxy",
            "observable": "alpha1, alpha2",
            "status": "HIGH_RISK_UNSIGNED",
            "claim_effect": "requires theorem-zero vector projection or sourced products",
            "valid_for_claim": False,
        },
        {
            "projection_id": "QPS3417_4_alpha3",
            "lane": "momentum/preferred-frame alpha3",
            "mathematical_form": "alpha3_q = W_q_alpha3 f_qV q_proxy",
            "observable": "alpha3",
            "status": "FAIL_UNLESS_VECTOR_PRODUCT_NEAR_ZERO",
            "claim_effect": "order-one vector leakage is excluded by ~5.38e-15 product limit",
            "valid_for_claim": False,
        },
        {
            "projection_id": "QPS3417_5_xi",
            "lane": "preferred-location anisotropy",
            "mathematical_form": "xi_q = W_q_xi f_xi q_proxy",
            "observable": "xi",
            "status": "UNSCORED_DOMAIN_ANISOTROPY_MISSING",
            "claim_effect": "requires no anisotropic boundary/domain spurion or sourced xi bound",
            "valid_for_claim": False,
        },
        {
            "projection_id": "QPS3417_6_range",
            "lane": "finite-range q scalar kernel",
            "mathematical_form": "alpha_q(lambda)=W_q_R10(lambda) f_range(lambda) q_proxy",
            "observable": "R10/fifth-force alpha(lambda)",
            "status": "DEFER_UNTIL_RANGE_KERNEL_EXISTS",
            "claim_effect": "cannot score R10 without range kernel and real bound comparison",
            "valid_for_claim": False,
        },
    ]


def qloc_numeric_pressure() -> list[dict[str, Any]]:
    return [
        {
            "pressure_id": "QNP3417_0_beta_if_unit",
            "quantity": "delta_beta_q_if_Wf_eq_1",
            "formula": "delta_beta_q=q_proxy",
            "value": Q_PROXY,
            "bound_or_target": BETA_BOUND,
            "ratio_to_bound": BETA_FRACTION_IF_UNIT,
            "interpretation": "below beta target in this provisional normalization, but not claim-ready",
            "valid_for_claim": False,
        },
        {
            "pressure_id": "QNP3417_1_kappav_if_unit",
            "quantity": "kappa_q_if_Wf_eq_1",
            "formula": "kappa_q=2*q_proxy",
            "value": KAPPA_Q_BETA_IF_UNIT,
            "bound_or_target": KAPPAV_BOUND,
            "ratio_to_bound": KAPPAV_FRACTION_IF_UNIT,
            "interpretation": "uses about 9.53 percent of the kappa_v beta envelope if scalar-only and unit-weight",
            "valid_for_claim": False,
        },
        {
            "pressure_id": "QNP3417_2_alpha3_product_limit",
            "quantity": "|W_q_alpha3 f_qV|",
            "formula": "alpha3_bound/q_proxy",
            "value": ALPHA3_PRODUCT_LIMIT,
            "bound_or_target": ALPHA3_BOUND,
            "ratio_to_bound": 1.0,
            "interpretation": "vector response product must be <=5.38e-15; structural zero is the natural route",
            "valid_for_claim": False,
        },
        {
            "pressure_id": "QNP3417_3_alpha3_if_order_one",
            "quantity": "alpha3_q_if_Wf_eq_1",
            "formula": "alpha3_q=q_proxy",
            "value": Q_PROXY,
            "bound_or_target": ALPHA3_BOUND,
            "ratio_to_bound": Q_PROXY / ALPHA3_BOUND,
            "interpretation": "order-one vector leakage misses alpha3 by about 1.86e14",
            "valid_for_claim": False,
        },
        {
            "pressure_id": "QNP3417_4_verdict",
            "quantity": "q_loc_score_status",
            "formula": "scalar beta may be small; vector/preferred-frame must be zero or bounded independently",
            "value": "NOT_SCORE_READY",
            "bound_or_target": "requires U2 scalar normalization and alpha-vector projection",
            "ratio_to_bound": "n/a",
            "interpretation": "q_loc cannot be accepted as a retained local-GR pass",
            "valid_for_claim": False,
        },
    ]


def retained_beta_stress_bound_pack() -> list[dict[str, Any]]:
    return [
        {
            "bound_id": "RBP3417_0_reduced_kappav",
            "quantity": "kappa_v_reduced",
            "formula": "|kappa_v| <= |kappa_PiM|+|kappa_boundary|+|kappa_readout|+|kappa_operator|+|kappa_coupling|+|kappa_q_loc|",
            "current_input": "eta/source-square zeroes conditional; retained lanes unfilled",
            "acceptance": f"absolute envelope <= {KAPPAV_BOUND}",
            "status": "FORMULA_READY_VALUES_MISSING",
            "valid_for_claim": False,
        },
        {
            "bound_id": "RBP3417_1_q_scalar_beta",
            "quantity": "kappa_q_loc_scalar",
            "formula": "|kappa_q|=2|W_q_beta f_beta q_proxy|",
            "current_input": f"q_proxy={Q_PROXY}; unit-weight diagnostic={KAPPA_Q_BETA_IF_UNIT}",
            "acceptance": "requires physical U2/readout normalization and no vector leakage",
            "status": "PROVISIONAL_DIAGNOSTIC_NOT_SCORE_READY",
            "valid_for_claim": False,
        },
        {
            "bound_id": "RBP3417_2_q_alpha_vector",
            "quantity": "q_loc preferred-frame vector",
            "formula": "|W_q_alpha3 f_qV| <= alpha3_bound/q_proxy",
            "current_input": f"limit={ALPHA3_PRODUCT_LIMIT}",
            "acceptance": "theorem-zero f_qV=0 or sourced product below limit",
            "status": "FAIL_CURRENT_UNSIGNED",
            "valid_for_claim": False,
        },
        {
            "bound_id": "RBP3417_3_hidden_stress",
            "quantity": "T_hidden_abs",
            "formula": "absolute hidden/projector/constitutive stress projection added to beta/alpha_i/xi/zeta/source envelope",
            "current_input": "safe-class taxonomy exists; coefficients/profiles missing",
            "acceptance": "all live hidden stress safe-class, theorem-zero, or source-backed bound",
            "status": "RETAINED_VALUES_MISSING",
            "valid_for_claim": False,
        },
        {
            "bound_id": "RBP3417_4_nonEH_poles",
            "quantity": "sum_i |B_i/D_GR|",
            "formula": "absolute no-cancellation residue sum relative to conditional GR pole",
            "current_input": "3409 channel list exists; H_i/R_i/J_i/range/projection values missing",
            "acceptance": "each channel passes arena-specific beta/gamma/alpha_i/xi/R10/WEP/clock/orbital locks",
            "status": "BOUND_INTERFACE_READY_VALUES_MISSING",
            "valid_for_claim": False,
        },
        {
            "bound_id": "RBP3417_5_combined_policy",
            "quantity": "local retained residual envelope",
            "formula": "Delta_local_abs >= Delta_EH_selector_abs + sum_i|B_i/D_GR| + |T_hidden_abs| + |B_q_loc_beta_alpha_vector|",
            "current_input": "components routed but not populated",
            "acceptance": "all terms zero or bounded without cancellation",
            "status": "NO_LOCAL_GR_SCORE_YET",
            "valid_for_claim": False,
        },
    ]


def ward_zero_rescue_gates() -> list[dict[str, Any]]:
    return [
        {
            "gate_id": "WZG3417_0_stress_identity",
            "needed_clause": "T_GK^{mu nu}=Gamma_eff g^{mu nu}-K_hat^{mu nu} is the actual Hilbert stress of one parent density",
            "current_evidence": "3411 algebraic identity exists",
            "current_status": "PASS_ALGEBRA_ONLY",
            "blocks": "not enough without metric-response ownership",
            "valid_for_claim": False,
        },
        {
            "gate_id": "WZG3417_1_symbol_match",
            "needed_clause": "K_hat equals the metric response of Gamma_eff in current MTS symbols",
            "current_evidence": "3411/3413 Delta_K retained",
            "current_status": "FAIL_CURRENT_SYMBOL_MATCH",
            "blocks": "q_loc cannot be killed as Ward residual",
            "valid_for_claim": False,
        },
        {
            "gate_id": "WZG3417_2_Euler_boundary",
            "needed_clause": "local Euler equations source-free and P_loc/boundary improvements silent through O(U^2)",
            "current_evidence": "3413 source neutrality fails for Y5/Y6; boundary/projector open",
            "current_status": "FAIL_SOURCE_BOUNDARY_OPEN",
            "blocks": "bulk Ward zero could still leak into alpha-vector lanes",
            "valid_for_claim": False,
        },
        {
            "gate_id": "WZG3417_3_vector_zero",
            "needed_clause": "q_T^i and harmonic boundary/domain vector projection vanish",
            "current_evidence": "3410 alpha3 product limit demands |W f| <= 5.38e-15",
            "current_status": "NOT_PROVED_BUT_REQUIRED",
            "blocks": "preferred-frame/local-GR promotion",
            "valid_for_claim": False,
        },
        {
            "gate_id": "WZG3417_4_rescue_verdict",
            "needed_clause": "q_loc Ward-zero through O(U^2) or componentwise bound pack",
            "current_evidence": "conditional theorem exists, current gates fail",
            "current_status": "BOUND_BRANCH_ACTIVE",
            "blocks": "no q_loc local-GR pass",
            "valid_for_claim": False,
        },
    ]


def promotion_gates() -> list[dict[str, Any]]:
    return [
        {
            "gate_id": "PG3417_0_projection_split",
            "gate": "q_loc scalar/vector/Hodge lane split is explicit",
            "current_result": "PASS_ROUTING",
            "promotes_if": "not a claim gate",
            "valid_for_claim": False,
        },
        {
            "gate_id": "PG3417_1_scalar_beta",
            "gate": "q_loc scalar U2 beta lane is score-ready",
            "current_result": "FAIL_U2_NORMALIZATION_UNSIGNED",
            "promotes_if": "W_q_beta, f_beta and readout/source normalization are parent-signed",
            "valid_for_claim": False,
        },
        {
            "gate_id": "PG3417_2_alpha_vector",
            "gate": "q_loc preferred-frame alpha-vector lane is safe",
            "current_result": "FAIL_ALPHA3_PRODUCT_PRESSURE",
            "promotes_if": "f_qV=0 by theorem or |W_q_alpha3 f_qV|<=5.38e-15 with sourced rows",
            "valid_for_claim": False,
        },
        {
            "gate_id": "PG3417_3_Ward_zero",
            "gate": "q_loc Ward-zero rescue closes",
            "current_result": "BLOCKED_SYMBOL_EULER_BOUNDARY",
            "promotes_if": "metric-response symbol match, Helmholtz/Euler and boundary/projector gates pass",
            "valid_for_claim": False,
        },
        {
            "gate_id": "PG3417_4_retained_bounds",
            "gate": "retained beta/stress/nonEH bound pack is score-ready",
            "current_result": "FAIL_VALUES_MISSING",
            "promotes_if": "all retained lanes have source-backed numeric values or theorem-zeroes",
            "valid_for_claim": False,
        },
        {
            "gate_id": "PG3417_5_local_GR",
            "gate": "local GR/Newton/PPN branch is derived",
            "current_result": "BLOCKED",
            "promotes_if": "PG3417_1 through PG3417_4 and selector/source/EM stress gates pass",
            "valid_for_claim": False,
        },
    ]


def decision_ledger() -> list[dict[str, Any]]:
    return [
        {
            "decision_id": "DEC3417_0_scalar_not_enough",
            "finding": "The q_loc beta-sized diagnostic is not fatal by itself, but it is not enough.",
            "reason": "unit-weight beta uses about 9.53 percent of the beta/kappa_v target, but U2 normalization and gamma/source readout are unsigned.",
            "next_action": "do not score q_loc scalar lanes until W/f/readout rows are parent-signed",
            "valid_for_claim": False,
        },
        {
            "decision_id": "DEC3417_1_vector_is_the_dragon",
            "finding": "The alpha3 vector lane is the decisive q_loc danger.",
            "reason": "order-one vector leakage misses alpha3 by ~1.86e14; structural vector zero is the sane route.",
            "next_action": "try to prove q_T/harmonic vector zero from Ward/response/boundary gates",
            "valid_for_claim": False,
        },
        {
            "decision_id": "DEC3417_2_bound_pack",
            "finding": "The retained beta/stress residuals now have a single no-cancellation envelope.",
            "reason": "q_loc, hidden stress and non-EH pole residues are tied to the conditional GR denominator and kappa_v envelope.",
            "next_action": "populate one lane or prove it zero; avoid broad placeholder scans",
            "valid_for_claim": False,
        },
        {
            "decision_id": "DEC3417_3_best_next",
            "finding": "Next strike should be q_loc vector-zero/Ward rescue, not more scalar beta arithmetic.",
            "reason": "the scalar number is already small-ish; alpha-vector silence is the claim gate.",
            "next_action": "build 3418 q_loc vector-zero Ward/boundary proof or demote to alpha-vector bound rows",
            "valid_for_claim": False,
        },
    ]


def next_target() -> list[dict[str, Any]]:
    return [
        {
            "target_id": "3418-Y5-R2FR-q_loc-vector-zero-Ward-boundary-proof-or-alpha-bound-row-under-AX1090.md",
            "target_script": "scripts/Y5_R2FR_3418_q_loc_vector_zero_Ward_boundary_proof_or_alpha_bound_row.py",
            "objective": "try to prove q_T/harmonic vector projection of q_loc vanishes from the Ward metric-response identity plus boundary/projector silence; if not, emit explicit alpha-vector bound rows",
            "why_next": "3417 shows scalar beta is not the main q_loc danger; alpha3 requires structural zero or an extremely tiny sourced product",
            "valid_for_claim": False,
        },
        {
            "target_id": "3419-Y5-R2FR-HRJ-source-row-extraction-for-TT-only-selector-under-AX1090.md",
            "target_script": "scripts/Y5_R2FR_3419_HRJ_source_row_extraction_for_TT_only_selector.py",
            "objective": "source the missing parent H_AB/R/J rows directly from core parent-action documents to promote or reject TT-only mode rank",
            "why_next": "parallel constructive selector route after q_loc alpha-vector risk is addressed",
            "valid_for_claim": False,
        },
    ]


def runner_nonclaim() -> list[dict[str, Any]]:
    return [
        {
            "runner_id": "RUN3417_0",
            "script": str(Path(__file__).resolve()),
            "claim_status": "QLOC_SPLIT_AND_BOUND_PACK_ONLY",
            "main_result": "q_loc scalar beta diagnostic is small but not score-ready; alpha-vector lane fails unless structurally zero or product-suppressed to <=5.38e-15; local GR remains blocked.",
            "valid_for_claim": False,
        }
    ]


def validation_rows(generated: dict[str, list[dict[str, Any]]]) -> list[dict[str, Any]]:
    source_rows = generated["source_register"]
    output_paths = list(OUTPUTS.values()) + [DOC]
    source_exists = all(str(row["exists"]).lower() == "true" for row in source_rows)
    no_workbench = all("formalization-workbench" not in str(path) for path in output_paths)
    all_nonclaim = all(
        str(row.get("valid_for_claim", "False")).lower() == "false"
        for rows in generated.values()
        for row in rows
    )
    split = any(row.get("projection_id") == "QPS3417_4_alpha3" for row in generated["qloc_projection_split"])
    alpha_limit_ok = abs(ALPHA3_PRODUCT_LIMIT - 5.381673706808059e-15) < 1e-28
    beta_fraction_ok = 0.09 < BETA_FRACTION_IF_UNIT < 0.10
    alpha_fail = any(row.get("gate_id") == "PG3417_2_alpha_vector" and row.get("current_result") == "FAIL_ALPHA3_PRODUCT_PRESSURE" for row in generated["promotion_gates"])
    bound_pack = any(row.get("bound_id") == "RBP3417_5_combined_policy" for row in generated["retained_beta_stress_bound_pack"])
    local_blocked = any(row.get("gate_id") == "PG3417_5_local_GR" and row.get("current_result") == "BLOCKED" for row in generated["promotion_gates"])
    next_vector = "q_loc-vector-zero" in generated["next_target"][0]["target_id"]
    rows = [
        {
            "check_id": "VAL3417_0_sources_exist",
            "check": "every cited local source path exists",
            "passed": source_exists,
            "detail": f"{sum(str(row['exists']).lower() == 'true' for row in source_rows)}/{len(source_rows)} source paths exist",
        },
        {
            "check_id": "VAL3417_1_scope",
            "check": "no output path targets formalization-workbench",
            "passed": no_workbench,
            "detail": "all outputs are under post-checkpoint-work",
        },
        {
            "check_id": "VAL3417_2_all_nonclaim",
            "check": "all rows keep valid_for_claim=false",
            "passed": all_nonclaim,
            "detail": "3417 is a q_loc split and bound pack, not a claim",
        },
        {
            "check_id": "VAL3417_3_projection_split",
            "check": "q_loc alpha-vector split is present",
            "passed": split,
            "detail": "scalar beta/gamma and alpha-vector lanes separated",
        },
        {
            "check_id": "VAL3417_4_numeric_pressure",
            "check": "alpha3 and beta numeric pressure values are consistent",
            "passed": alpha_limit_ok and beta_fraction_ok,
            "detail": f"alpha3_product_limit={ALPHA3_PRODUCT_LIMIT}; beta_fraction={BETA_FRACTION_IF_UNIT}",
        },
        {
            "check_id": "VAL3417_5_alpha_gate",
            "check": "alpha-vector gate remains failed",
            "passed": alpha_fail,
            "detail": "structural vector zero or sourced product bound required",
        },
        {
            "check_id": "VAL3417_6_bound_pack",
            "check": "retained beta/stress bound pack exists",
            "passed": bound_pack,
            "detail": "combined no-cancellation policy row written",
        },
        {
            "check_id": "VAL3417_7_local_GR_blocked",
            "check": "local-GR promotion remains blocked",
            "passed": local_blocked,
            "detail": "q_loc, retained bounds and selector/source gates remain open",
        },
        {
            "check_id": "VAL3417_8_next_target",
            "check": "next target attacks q_loc vector zero",
            "passed": next_vector,
            "detail": generated["next_target"][0]["target_id"],
        },
    ]
    overall = all(row["passed"] for row in rows)
    rows.append(
        {
            "check_id": "VAL3417_9_overall",
            "check": "3417 q_loc split and retained bound pack is internally valid",
            "passed": overall,
            "detail": "PASS" if overall else "FAIL",
        }
    )
    return rows


def build_doc(generated: dict[str, list[dict[str, Any]]]) -> str:
    return "\n\n".join(
        [
            "# 3417 - q_loc U2 Alpha-Vector and Retained Beta/Stress Bound Pack",
            "## Summary\n"
            "- This checkpoint splits `q_loc` into scalar beta/gamma lanes and preferred-frame alpha-vector lanes.\n"
            "- The scalar beta diagnostic is not awful: with unit projection it is `7.432631961576971e-06`, about 9.53% of the beta/kappa_v target.\n"
            "- But this does not score: `W_q_beta`, `f_beta`, physical `U^2` readout and source normalization are unsigned.\n"
            "- The alpha3 lane is the dragon. If the same residual has order-one vector response, it misses the alpha3 lock by about `1.86e14`; the product `|W_q_alpha3 f_qV|` must be `<=5.38e-15`.\n"
            "- Therefore q_loc needs a structural vector-zero/Ward-boundary proof or explicit alpha-vector bound rows. Local GR remains blocked.",
            "## Source Register\n" + md_table(generated["source_register"]),
            "## q_loc Projection Split\n" + md_table(generated["qloc_projection_split"]),
            "## q_loc Numeric Pressure\n" + md_table(generated["qloc_numeric_pressure"]),
            "## Retained Beta/Stress Bound Pack\n" + md_table(generated["retained_beta_stress_bound_pack"]),
            "## Ward-Zero Rescue Gates\n" + md_table(generated["ward_zero_rescue_gates"]),
            "## Promotion Gates\n" + md_table(generated["promotion_gates"]),
            "## Decision Ledger\n" + md_table(generated["decision_ledger"]),
            "## Next Target\n" + md_table(generated["next_target"]),
            "## Runner Nonclaim\n" + md_table(generated["runner_nonclaim"]),
            "## Validation\n" + md_table(generated["validation"]),
            "## Bottom Line\n"
            "q_loc is not dead from beta alone, but beta is the wrong place to declare victory. "
            "The real gate is vector silence: either the transverse/harmonic q_loc projection is theorem-zero, or the alpha-vector product must be sourced and tiny. "
            "Until then q_loc stays as a retained local-GR blocker in the no-cancellation envelope.",
        ]
    ) + "\n"


def main() -> None:
    if "formalization-workbench" in str(ROOT):
        raise RuntimeError(f"Refusing to run from formalization-workbench: {ROOT}")

    generated: dict[str, list[dict[str, Any]]] = {
        "source_register": source_register(),
        "qloc_projection_split": qloc_projection_split(),
        "qloc_numeric_pressure": qloc_numeric_pressure(),
        "retained_beta_stress_bound_pack": retained_beta_stress_bound_pack(),
        "ward_zero_rescue_gates": ward_zero_rescue_gates(),
        "promotion_gates": promotion_gates(),
        "decision_ledger": decision_ledger(),
        "next_target": next_target(),
        "runner_nonclaim": runner_nonclaim(),
    }
    generated["validation"] = validation_rows(generated)

    for key, rows in generated.items():
        write_csv(OUTPUTS[key], rows)

    DOC.write_text(build_doc(generated), encoding="utf-8")

    if not all(str(row["passed"]).lower() == "true" for row in generated["validation"]):
        failed = [row for row in generated["validation"] if str(row["passed"]).lower() != "true"]
        raise SystemExit(f"3417 validation failed: {failed}")

    print(f"wrote {len(generated)} CSV artefacts and {DOC}")


if __name__ == "__main__":
    main()

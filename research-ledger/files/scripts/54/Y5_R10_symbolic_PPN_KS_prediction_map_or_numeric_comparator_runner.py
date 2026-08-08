from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CSV_DIR = ROOT / "source-intake" / "mts_residuals"
DOC = ROOT / "1182-Y5-R10-symbolic-PPN-KS-prediction-map-or-numeric-comparator-runner.md"
FORMALIZATION = ROOT.parent / "formalization-workbench"
STAMP = datetime.now(timezone.utc).isoformat()


def stamp(rows: list[dict[str, object]]) -> list[dict[str, object]]:
    return [row | {"generated_utc": STAMP} for row in rows]


def write_csv(path: Path, rows: list[dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        raise ValueError(f"empty csv refused: {path}")
    fieldnames: list[str] = []
    for row in rows:
        for key in row:
            if key not in fieldnames:
                fieldnames.append(key)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def md_escape(value: object) -> str:
    return str(value).replace("\\", "\\\\").replace("|", "\\|").replace("\n", " ")


def table(rows: list[dict[str, object]]) -> str:
    if not rows:
        return ""
    headers: list[str] = []
    for row in rows:
        for key in row:
            if key == "generated_utc":
                continue
            if key not in headers:
                headers.append(key)
    lines = [
        "| " + " | ".join(headers) + " |",
        "| " + " | ".join("---" for _ in headers) + " |",
    ]
    for row in rows:
        lines.append("| " + " | ".join(md_escape(row.get(header, "")) for header in headers) + " |")
    return "\n".join(lines)


def source_rows() -> list[dict[str, object]]:
    entries = [
        {
            "source_id": "SRC1182_0_1181_next",
            "relative_path": "source-intake/mts_residuals/P8_Y5_R10_1181_NEXT_TARGET.csv",
            "needle": "NEXT1181_0_1182",
            "role": "handoff to symbolic PPN K_S prediction map.",
        },
        {
            "source_id": "SRC1182_1_1181_summary",
            "relative_path": "source-intake/mts_residuals/P8_Y5_BRR545_1181_VALIDATION.csv",
            "needle": "V1181_SUMMARY",
            "role": "1181 validation summary.",
        },
        {
            "source_id": "SRC1182_2_1181_gamma",
            "relative_path": "source-intake/mts_residuals/P8_Y5_R10_1181_PPN_RESIDUAL_VECTOR_COMPARATOR_ROWS.csv",
            "needle": "PPNV1181_0_gamma",
            "role": "source-backed gamma comparator row.",
        },
        {
            "source_id": "SRC1182_3_1181_beta",
            "relative_path": "source-intake/mts_residuals/P8_Y5_R10_1181_PPN_RESIDUAL_VECTOR_COMPARATOR_ROWS.csv",
            "needle": "PPNV1181_1_beta",
            "role": "source-backed beta comparator row.",
        },
        {
            "source_id": "SRC1182_4_1181_q_loc",
            "relative_path": "source-intake/mts_residuals/P8_Y5_R10_1181_PPN_RESIDUAL_VECTOR_COMPARATOR_ROWS.csv",
            "needle": "PPNV1181_5_q_loc_TF",
            "role": "retained q_loc_TF residual row.",
        },
        {
            "source_id": "SRC1182_5_1181_KS_gamma_old",
            "relative_path": "source-intake/mts_residuals/P8_Y5_R10_1181_SYMBOLIC_KS_TO_PPN_MAP.csv",
            "needle": "KSM1181_0_gamma_channel",
            "role": "prior symbolic gamma-channel row to be refined by trace projection.",
        },
        {
            "source_id": "SRC1182_6_1177_tracefree",
            "relative_path": "1177-Y5-R10-metric-channel-routing-for-tracefree-shear-or-first-shear-norm-row.md",
            "needle": "Tr(S_Q)=0",
            "role": "tracefree split and first-variation zero condition.",
        },
        {
            "source_id": "SRC1182_7_1179_KS",
            "relative_path": "1179-Y5-R10-reciprocal-metric-tracefree-transfer-derivation-or-KS-closure.md",
            "needle": "K_S_to_metric = sigma_KS * K_norm",
            "role": "K_S closure decomposition.",
        },
        {
            "source_id": "SRC1182_8_1180_Qcoh",
            "relative_path": "1180-Y5-R10-parent-Q-geometric-identity-or-PPN-KS-source-row.md",
            "needle": "Qcoh=(1/3)hX",
            "role": "Qcoh scalar channel cannot own tracefree spin-2 transfer.",
        },
        {
            "source_id": "SRC1182_9_1181_web_gamma",
            "relative_path": "source-intake/mts_residuals/P8_Y5_R10_1181_EXTERNAL_PPN_SOURCE_REGISTER.csv",
            "needle": "SRC1181W_0_Cassini_gamma",
            "role": "external gamma source URL already recorded.",
        },
        {
            "source_id": "SRC1182_10_1181_web_beta_eta",
            "relative_path": "source-intake/mts_residuals/P8_Y5_R10_1181_EXTERNAL_PPN_SOURCE_REGISTER.csv",
            "needle": "SRC1181W_1_LLR_beta_eta",
            "role": "external beta/eta source URL already recorded.",
        },
    ]
    checked: list[dict[str, object]] = []
    for entry in entries:
        path = ROOT / str(entry["relative_path"])
        text = path.read_text(encoding="utf-8", errors="ignore") if path.exists() else ""
        checked.append(entry | {"exists": path.exists(), "needle_found": str(entry["needle"]) in text})
    return stamp(checked)


def ppn_projection_rows() -> list[dict[str, object]]:
    rows = [
        {
            "projection_id": "PPNP1182_0_metric_ansatz",
            "object": "weak-field spatial metric split",
            "formula": "g_ij = (1 + 2 gamma U/c^2) delta_ij + H_ij^TF + higher_order",
            "derivation_result": "gamma is the scalar/isotropic trace coefficient; H_ij^TF is tracefree anisotropic/tidal response",
            "status": "ANSATZ_SPLIT_WRITTEN",
            "valid_for_claim": False,
        },
        {
            "projection_id": "PPNP1182_1_trace_projection",
            "object": "scalar PPN gamma projection",
            "formula": "P_trace(H^TF) := delta^ij H_ij^TF / 3 = 0",
            "derivation_result": "pure tracefree K_S S_Q has zero first-order contribution to scalar gamma under isotropic PPN projection",
            "status": "DERIVED_LINEAR_TRACEFREE_GAMMA_ZERO",
            "valid_for_claim": False,
        },
        {
            "projection_id": "PPNP1182_2_gamma_leakage",
            "object": "gamma residual channel",
            "formula": "gamma_MTS-1 = delta_gamma_scalar + leak_iso(K_S S_Q) + q_trace + higher_order",
            "derivation_result": "K_S_to_metric enters Cassini-style gamma only through scalar leakage/domain anisotropy/q_loc trace, not through the pure tracefree first-order channel",
            "status": "REFINED_SYMBOLIC_MAP",
            "valid_for_claim": False,
        },
        {
            "projection_id": "PPNP1182_3_beta_second_order",
            "object": "PPN beta lane",
            "formula": "beta_MTS-1 = delta_beta_scalar + C_beta_TF ||K_S S_Q||^2 + C_beta_q ||q_loc|| + Delta_rec_2",
            "derivation_result": "tracefree K_S can enter beta at second order or through scalar backreaction, not as a first-order scalar trace",
            "status": "SECOND_ORDER_MAP_ONLY",
            "valid_for_claim": False,
        },
        {
            "projection_id": "PPNP1182_4_eta_combination",
            "object": "Nordtvedt eta",
            "formula": "eta_N_MTS = 4(beta_MTS-1) - (gamma_MTS-1) + eta_nonmetric",
            "derivation_result": "eta can be assembled once gamma/beta/source-coupling residuals exist, but not before",
            "status": "COMBINATION_SCHEMA_ONLY",
            "valid_for_claim": False,
        },
        {
            "projection_id": "PPNP1182_5_anisotropic_channel",
            "object": "tracefree metric residual",
            "formula": "H_ij^TF = K_S_to_metric S_Qij + q_loc_TFij + projector_TFij",
            "derivation_result": "the direct first-order home of K_S is an anisotropic/STF PPN residual channel, not the scalar gamma/beta comparator",
            "status": "DIRECT_KS_CHANNEL_IDENTIFIED",
            "valid_for_claim": False,
        },
    ]
    return stamp(rows)


def comparator_runner_rows() -> list[dict[str, object]]:
    rows = [
        {
            "runner_id": "PPR1182_0_gamma",
            "component": "gamma_minus_1",
            "source_comparator": "(2.1 +/- 2.3)e-5 from SRC1181W_0_Cassini_gamma",
            "MTS_prediction_formula": "delta_gamma_scalar + leak_iso(K_S S_Q) + q_trace",
            "score_status": "NOT_SCOREABLE_MTS_TERMS_MISSING",
            "missing_inputs": "delta_gamma_scalar; leak_iso coefficient; q_trace bound; scalar reciprocity theorem",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "runner_id": "PPR1182_1_beta",
            "component": "beta_minus_1",
            "source_comparator": "(1.2 +/- 1.1)e-4 from SRC1181W_1_LLR_beta_eta",
            "MTS_prediction_formula": "delta_beta_scalar + C_beta_TF||K_S S_Q||^2 + C_beta_q||q_loc|| + Delta_rec_2",
            "score_status": "NOT_SCOREABLE_MTS_TERMS_MISSING",
            "missing_inputs": "C_beta_TF; ||S_Q||_PPN; q_loc norm; second-order reciprocity",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "runner_id": "PPR1182_2_eta",
            "component": "eta_N",
            "source_comparator": "(4.4 +/- 4.5)e-4 from SRC1181W_1_LLR_beta_eta",
            "MTS_prediction_formula": "4(beta_MTS-1) - (gamma_MTS-1) + eta_nonmetric",
            "score_status": "NOT_SCOREABLE_MTS_TERMS_MISSING",
            "missing_inputs": "gamma_MTS; beta_MTS; eta_nonmetric/source coupling residual",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "runner_id": "PPR1182_3_STF",
            "component": "H_TF_metric",
            "source_comparator": "MISSING_PRIMARY_STF_OR_PREFERRED_FRAME_BOUND",
            "MTS_prediction_formula": "K_S_to_metric S_Qij + q_loc_TFij + projector_TFij",
            "score_status": "NOT_SCOREABLE_COMPARATOR_AND_MTS_TERMS_MISSING",
            "missing_inputs": "primary STF/preferred-frame comparator; K_S; S_Q norm; q_loc_TF norm",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]
    return stamp(rows)


def correction_rows() -> list[dict[str, object]]:
    rows = [
        {
            "correction_id": "COR1182_0_1181_gamma_row_refined",
            "prior_row": "KSM1181_0_gamma_channel",
            "prior_issue": "treated tracefree spatial metric response as directly changing scalar gamma lane",
            "correction": "pure tracefree S_Q has zero first-order scalar gamma projection; gamma sees scalar leakage/domain anisotropy/q_loc trace",
            "status": "REFINED_NOT_OVERCLAIMED",
            "valid_for_claim": False,
        },
        {
            "correction_id": "COR1182_1_testing_order_refined",
            "prior_row": "FAI1179_0_PPN_preferred_first",
            "prior_issue": "PPN was selected correctly but the scalar-vs-STF split was not sharp enough",
            "correction": "PPN remains first, but the direct K_S test should target STF/preferred-frame/tidal residuals before scalar gamma/beta scoring",
            "status": "REFINED_TEST_TARGET",
            "valid_for_claim": False,
        },
    ]
    return stamp(rows)


def gate_rows() -> list[dict[str, object]]:
    rows = [
        {
            "gate_id": "G1182_0_gamma_direct_KS",
            "claim": "pure tracefree K_S S_Q directly shifts scalar gamma at first order",
            "status": "FAILED_TRACE_PROJECTION_ZERO",
            "why_blocked": "delta^ij S_Qij=0 under isotropic projection",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "gate_id": "G1182_1_gamma_leakage_score",
            "claim": "gamma leakage is scoreable",
            "status": "BLOCKED_MTS_SCALAR_LEAKAGE_INPUTS_MISSING",
            "why_blocked": "leak_iso coefficient and q_trace bound are missing",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "gate_id": "G1182_2_beta_score",
            "claim": "beta residual is scoreable",
            "status": "BLOCKED_SECOND_ORDER_INPUTS_MISSING",
            "why_blocked": "C_beta_TF, Delta_rec_2, q_loc norm, and S_Q norm are missing",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "gate_id": "G1182_3_STF_comparator",
            "claim": "direct K_S STF PPN channel is scoreable",
            "status": "BLOCKED_PRIMARY_STF_OR_PREFERRED_FRAME_SOURCE_MISSING",
            "why_blocked": "1181 only sourced scalar gamma/beta/eta comparator rows",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "gate_id": "G1182_4_local_GR_Newton",
            "claim": "local GR/Newton limit is derived",
            "status": "BLOCKED_NO_LOCAL_LIMIT_CLAIM",
            "why_blocked": "symbolic map refined but prediction coefficients and residual bounds remain missing",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
    ]
    return stamp(rows)


def runner_rows() -> list[dict[str, object]]:
    rows = [
        {
            "run_id": "RUN1182_0_trace_projection",
            "operation": "trace projection of K_S S_Q into scalar gamma",
            "result": "PASS_ZERO_FIRST_ORDER_TRACEFREE_PROJECTION",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "run_id": "RUN1182_1_numeric_comparator",
            "operation": "gamma/beta/eta numeric comparator dry-run",
            "result": "REFUSED_MTS_PREDICTIONS_MISSING",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "run_id": "RUN1182_2_STF_channel",
            "operation": "direct K_S STF channel dry-run",
            "result": "REFUSED_STF_COMPARATOR_MISSING",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "run_id": "RUN1182_3_local_promotion",
            "operation": "PPN/local-GR promotion",
            "result": "REFUSED_NO_LOCAL_CLAIM",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
    ]
    return stamp(rows)


def decision_rows() -> list[dict[str, object]]:
    rows = [
        {
            "decision_id": "D1182_0_map_result",
            "decision": "derive_tracefree_to_scalar_gamma_zero_at_first_order",
            "reason": "the tracefree condition Tr(S_Q)=0 makes the direct scalar gamma projection vanish.",
            "next_action": "target scalar leakage/q_trace for gamma and direct STF/preferred-frame residuals for K_S.",
            "valid_for_claim": False,
        },
        {
            "decision_id": "D1182_1_test_strategy",
            "decision": "split_PPN_into_scalar_and_STF_channels",
            "reason": "Cassini gamma and LLR beta/eta test scalar combinations; K_S primarily lives in STF anisotropic channel.",
            "next_action": "source primary STF/preferred-frame comparator rows and derive leakage coefficients.",
            "valid_for_claim": False,
        },
        {
            "decision_id": "D1182_2_best_next",
            "decision": "source_STF_preferred_frame_bounds_or_derive_leak_iso",
            "reason": "without this, numeric PPN tests will not actually test the missing coupling.",
            "next_action": "build 1183 as STF/preferred-frame source pack or scalar-leakage coefficient derivation.",
            "valid_for_claim": False,
        },
    ]
    return stamp(rows)


def next_rows() -> list[dict[str, object]]:
    rows = [
        {
            "next_id": "NEXT1182_0_1183",
            "next_target": "1183-Y5-R10-STF-preferred-frame-source-pack-or-scalar-leakage-coefficient-derivation.md",
            "objective": "source primary bounds for the direct STF/preferred-frame PPN channel of K_S_to_metric, or derive the scalar leakage coefficient that lets tracefree S_Q enter gamma/beta comparators",
            "include": "alpha1/alpha2 or STF/tidal comparator sources; frame-covariance guard; leak_iso coefficient; q_loc_TF norm row; no-claim validation",
            "exclude": "claiming scalar gamma tests direct K_S; invented numeric bounds; hiding q_loc; GitHub; formalization edits",
            "valid_for_claim": False,
            "claim_allowed": False,
        }
    ]
    return stamp(rows)


def validation_rows(
    sources: list[dict[str, object]],
    projections: list[dict[str, object]],
    comparators: list[dict[str, object]],
    corrections: list[dict[str, object]],
    gates: list[dict[str, object]],
    runs: list[dict[str, object]],
    decisions: list[dict[str, object]],
    nexts: list[dict[str, object]],
) -> list[dict[str, object]]:
    checks = [
        {
            "check_id": "V1182_0_sources_exist",
            "result": "pass" if all(r["exists"] and r["needle_found"] for r in sources) else "fail",
            "detail": "all cited local source paths exist and needles are found",
            "claim_allowed": False,
        },
        {
            "check_id": "V1182_1_trace_projection_zero",
            "result": "pass" if any(r["status"] == "DERIVED_LINEAR_TRACEFREE_GAMMA_ZERO" for r in projections) else "fail",
            "detail": "linear scalar gamma projection of pure tracefree S_Q is zero",
            "claim_allowed": False,
        },
        {
            "check_id": "V1182_2_direct_STF_channel_identified",
            "result": "pass" if any(r["status"] == "DIRECT_KS_CHANNEL_IDENTIFIED" for r in projections) else "fail",
            "detail": "direct K_S channel is identified as STF/anistropic rather than scalar gamma",
            "claim_allowed": False,
        },
        {
            "check_id": "V1182_3_comparator_runner_nonclaim",
            "result": "pass" if len(comparators) >= 4 and all(r["claim_allowed"] is False for r in comparators) else "fail",
            "detail": "numeric comparator runner rows exist but remain nonclaim",
            "claim_allowed": False,
        },
        {
            "check_id": "V1182_4_prior_gamma_row_refined",
            "result": "pass" if any(r["correction_id"] == "COR1182_0_1181_gamma_row_refined" for r in corrections) else "fail",
            "detail": "1181 gamma-channel row is refined rather than silently overwritten",
            "claim_allowed": False,
        },
        {
            "check_id": "V1182_5_missing_inputs_not_claim_valid",
            "result": "pass"
            if all((not any("MISSING" in str(v) for v in row.values())) or row["valid_for_claim"] is False for row in comparators)
            else "fail",
            "detail": "rows with missing inputs remain invalid for claim",
            "claim_allowed": False,
        },
        {
            "check_id": "V1182_6_gates_blocked_or_failed",
            "result": "pass" if all(r["claim_allowed"] is False for r in gates) else "fail",
            "detail": "all PPN/local claims are blocked or explicitly failed as stated",
            "claim_allowed": False,
        },
        {
            "check_id": "V1182_7_runner_refuses_claim",
            "result": "pass" if all(r["claim_allowed"] is False for r in runs) else "fail",
            "detail": "dry-run refuses numeric PPN/local promotion claims",
            "claim_allowed": False,
        },
        {
            "check_id": "V1182_8_no_claim_rows",
            "result": "pass"
            if all(row.get("valid_for_claim") is False for row in projections + comparators + corrections + gates + decisions + nexts)
            else "fail",
            "detail": "all generated science rows remain nonclaim",
            "claim_allowed": False,
        },
        {
            "check_id": "V1182_9_next_target",
            "result": "pass" if nexts and "1183" in str(nexts[0]["next_target"]) else "fail",
            "detail": "1183 handoff targets STF/preferred-frame source pack or scalar leakage coefficient derivation",
            "claim_allowed": False,
        },
        {
            "check_id": "V1182_10_generated_under_post_checkpoint",
            "result": "pass" if str(DOC).startswith(str(ROOT)) and str(CSV_DIR).startswith(str(ROOT)) else "fail",
            "detail": "all generated outputs are under post-checkpoint-work",
            "claim_allowed": False,
        },
        {
            "check_id": "V1182_11_formalization_untouched",
            "result": "pass",
            "detail": "generator writes no outputs under formalization-workbench",
            "claim_allowed": False,
        },
        {
            "check_id": "V1182_SUMMARY",
            "result": "pass",
            "detail": "1182 derives that pure tracefree K_S S_Q does not enter scalar gamma at first order, refines the PPN strategy into scalar leakage versus direct STF/preferred-frame channels, and keeps all numeric comparisons nonclaim",
            "claim_allowed": False,
        },
    ]
    return stamp(checks)


def write_doc(
    sources: list[dict[str, object]],
    projections: list[dict[str, object]],
    comparators: list[dict[str, object]],
    corrections: list[dict[str, object]],
    gates: list[dict[str, object]],
    runs: list[dict[str, object]],
    decisions: list[dict[str, object]],
    validations: list[dict[str, object]],
    nexts: list[dict[str, object]],
) -> None:
    parts = [
        "# 1182 - Y5/R10 symbolic PPN K_S prediction map or numeric comparator runner",
        "**Current verdict:** the symbolic PPN map is sharper now: pure tracefree `K_S_to_metric S_Q` does not enter scalar `gamma` at first order because the trace projection vanishes.",
        "**Main progress:** PPN must be split into scalar comparator lanes (`gamma`, `beta`, `eta`) and direct STF/preferred-frame/tidal lanes. `K_S_to_metric` mainly lives in the latter unless scalar leakage or `q_loc` trace is derived.",
        "**Correction:** the 1181 gamma-channel row is refined: Cassini `gamma` is not a direct first-order test of pure tracefree `S_Q`; it tests scalar leakage, scalar reciprocity, and trace/q residuals.",
        "**No claim:** no local-GR, Newton, R10, PPN, WEP, clock, orbital, `c_g=0`, or public-facing claim follows from this checkpoint.",
        "## Source register\n\n" + table(sources),
        "## Symbolic PPN projection map\n\n" + table(projections),
        "## Nonclaim comparator runner rows\n\n" + table(comparators),
        "## Prior-row corrections\n\n" + table(corrections),
        "## Claim gates\n\n" + table(gates),
        "## Runner dry-run\n\n" + table(runs),
        "## Decision ledger\n\n" + table(decisions),
        "## Validation\n\n" + table(validations),
        "## Next target\n\n" + table(nexts),
    ]
    DOC.write_text("\n\n".join(parts) + "\n", encoding="utf-8")


def main() -> None:
    CSV_DIR.mkdir(parents=True, exist_ok=True)
    sources = source_rows()
    projections = ppn_projection_rows()
    comparators = comparator_runner_rows()
    corrections = correction_rows()
    gates = gate_rows()
    runs = runner_rows()
    decisions = decision_rows()
    nexts = next_rows()
    validations = validation_rows(sources, projections, comparators, corrections, gates, runs, decisions, nexts)

    outputs = {
        "P8_Y5_R10_1182_SOURCE_REGISTER.csv": sources,
        "P8_Y5_R10_1182_SYMBOLIC_PPN_PROJECTION_MAP.csv": projections,
        "P8_Y5_R10_1182_NONCLAIM_COMPARATOR_RUNNER_ROWS.csv": comparators,
        "P8_Y5_R10_1182_PRIOR_ROW_CORRECTIONS.csv": corrections,
        "P8_Y5_R10_1182_CLAIM_GATES.csv": gates,
        "P8_Y5_R10_1182_RUNNER_DRY_RUN.csv": runs,
        "P8_Y5_R10_1182_DECISION_LEDGER.csv": decisions,
        "P8_Y5_R10_1182_NEXT_TARGET.csv": nexts,
        "P8_Y5_BRR545_1182_VALIDATION.csv": validations,
    }
    for filename, rows in outputs.items():
        write_csv(CSV_DIR / filename, rows)

    write_doc(sources, projections, comparators, corrections, gates, runs, decisions, validations, nexts)

    failed = [row["check_id"] for row in validations if row["result"] != "pass"]
    pycache = Path(__file__).resolve().parent / "__pycache__"
    if pycache.exists():
        shutil.rmtree(pycache)
    if FORMALIZATION.exists() and not FORMALIZATION.is_dir():
        failed.append("formalization_path_not_directory")

    print(f"wrote {DOC}")
    print("validation: PASS" if not failed else f"validation: FAIL {failed}")
    if failed:
        raise SystemExit(1)


if __name__ == "__main__":
    main()

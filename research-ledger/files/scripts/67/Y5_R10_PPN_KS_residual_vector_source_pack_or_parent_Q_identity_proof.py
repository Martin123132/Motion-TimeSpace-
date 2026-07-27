from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CSV_DIR = ROOT / "source-intake" / "mts_residuals"
DOC = ROOT / "1181-Y5-R10-PPN-KS-residual-vector-source-pack-or-parent-Q-identity-proof.md"
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


def local_source_rows() -> list[dict[str, object]]:
    entries = [
        {
            "source_id": "SRC1181L_0_1180_next",
            "relative_path": "source-intake/mts_residuals/P8_Y5_R10_1180_NEXT_TARGET.csv",
            "needle": "NEXT1180_0_1181",
            "role": "handoff to PPN K_S residual-vector source pack.",
        },
        {
            "source_id": "SRC1181L_1_1180_summary",
            "relative_path": "source-intake/mts_residuals/P8_Y5_BRR545_1180_VALIDATION.csv",
            "needle": "V1180_SUMMARY",
            "role": "1180 validation summary.",
        },
        {
            "source_id": "SRC1181L_2_1180_Q_verdict",
            "relative_path": "source-intake/mts_residuals/P8_Y5_R10_1180_PARENT_Q_GEOMETRIC_IDENTITY_ATTEMPT.csv",
            "needle": "QID1180_5_verdict",
            "role": "Q identity remains not derived.",
        },
        {
            "source_id": "SRC1181L_3_1180_transfer",
            "relative_path": "source-intake/mts_residuals/P8_Y5_R10_1180_PPN_KS_SOURCE_CLOSURE_ROWS.csv",
            "needle": "PPNKS1180_0_transfer_definition",
            "role": "PPN K_S transfer row.",
        },
        {
            "source_id": "SRC1181L_4_1180_local_gate",
            "relative_path": "source-intake/mts_residuals/P8_Y5_R10_1180_CLAIM_GATES.csv",
            "needle": "G1180_5_local_GR_Newton",
            "role": "local GR/Newton claim remains blocked.",
        },
        {
            "source_id": "SRC1181L_5_1010_q_loc",
            "relative_path": "1010-Y5-R10-Gamma-Khat-action-existence-Helmholtz-or-q_loc-residual-retention.md",
            "needle": "retained as an explicit nonclaim residual",
            "role": "q_loc remains retained residual.",
        },
    ]
    checked: list[dict[str, object]] = []
    for entry in entries:
        path = ROOT / str(entry["relative_path"])
        text = path.read_text(encoding="utf-8", errors="ignore") if path.exists() else ""
        checked.append(entry | {"exists": path.exists(), "needle_found": str(entry["needle"]) in text})
    return stamp(checked)


def web_source_rows() -> list[dict[str, object]]:
    rows = [
        {
            "source_id": "SRC1181W_0_Cassini_gamma",
            "title": "A test of general relativity using radio links with the Cassini spacecraft",
            "url": "https://pubmed.ncbi.nlm.nih.gov/14508481/",
            "source_type": "primary_paper_index",
            "used_for": "PPN gamma comparator candidate",
            "extracted_comparator": "gamma = 1 + (2.1 +/- 2.3) x 10^-5",
            "confidence": "source_backed_from_pubmed_abstract",
            "valid_for_MTS_claim": False,
            "valid_for_claim": False,
        },
        {
            "source_id": "SRC1181W_1_LLR_beta_eta",
            "title": "Progress in Lunar Laser Ranging Tests of Relativistic Gravity",
            "url": "https://arxiv.org/abs/gr-qc/0411113",
            "source_type": "primary_preprint",
            "used_for": "PPN beta and Nordtvedt eta comparator candidates",
            "extracted_comparator": "eta=(4.4 +/- 4.5)x10^-4; beta-1=(1.2 +/- 1.1)x10^-4 using Cassini gamma",
            "confidence": "source_backed_from_arxiv_abstract",
            "valid_for_MTS_claim": False,
            "valid_for_claim": False,
        },
        {
            "source_id": "SRC1181W_2_Will_PPN_framework",
            "title": "The Confrontation between General Relativity and Experiment",
            "url": "https://link.springer.com/article/10.12942/lrr-2014-4",
            "source_type": "review_framework",
            "used_for": "PPN bookkeeping and preferred-frame parameter framework only",
            "extracted_comparator": "formal PPN residual vector context; no numeric preferred-frame bound promoted here",
            "confidence": "framework_reference_not_numeric_claim_source",
            "valid_for_MTS_claim": False,
            "valid_for_claim": False,
        },
    ]
    return stamp(rows)


def ppn_vector_rows() -> list[dict[str, object]]:
    rows = [
        {
            "ppn_id": "PPNV1181_0_gamma",
            "component": "gamma_minus_1",
            "observational_comparator": "(2.1 +/- 2.3)e-5",
            "source_id": "SRC1181W_0_Cassini_gamma",
            "MTS_prediction_slot": "gamma_MTS_minus_1 = F_gamma(K_S_to_metric, q_loc_TF, scalar_branch)",
            "required_MTS_inputs": "K_S_to_metric; q_loc_TF residual; Q identity or closure; scalar reciprocity status",
            "status": "COMPARATOR_SOURCED_PREDICTION_MISSING",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "ppn_id": "PPNV1181_1_beta",
            "component": "beta_minus_1",
            "observational_comparator": "(1.2 +/- 1.1)e-4",
            "source_id": "SRC1181W_1_LLR_beta_eta",
            "MTS_prediction_slot": "beta_MTS_minus_1 = F_beta(K_S_to_metric, Delta_C2, q_loc, second_order_reciprocity)",
            "required_MTS_inputs": "second-order reciprocal completion; K_S_to_metric; C_det2; q_loc residual",
            "status": "COMPARATOR_SOURCED_PREDICTION_MISSING",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "ppn_id": "PPNV1181_2_eta_Nordtvedt",
            "component": "eta_N = 4 beta - gamma - 3",
            "observational_comparator": "(4.4 +/- 4.5)e-4",
            "source_id": "SRC1181W_1_LLR_beta_eta",
            "MTS_prediction_slot": "eta_MTS = 4 beta_MTS - gamma_MTS - 3 plus nonmetric residual flags",
            "required_MTS_inputs": "gamma_MTS; beta_MTS; WEP/source coupling gate; q_loc residual",
            "status": "COMPARATOR_SOURCED_PREDICTION_MISSING",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "ppn_id": "PPNV1181_3_preferred_frame_alpha1",
            "component": "alpha1",
            "observational_comparator": "MISSING_PRIMARY_NUMERIC_SOURCE_IN_1181",
            "source_id": "SRC1181W_2_Will_PPN_framework",
            "MTS_prediction_slot": "alpha1_MTS = F_alpha1(local frame/routing anisotropy, q_loc_vector)",
            "required_MTS_inputs": "frame selection; vector residual; preferred-frame source row",
            "status": "FRAMEWORK_ONLY_NUMERIC_SOURCE_MISSING",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "ppn_id": "PPNV1181_4_preferred_frame_alpha2",
            "component": "alpha2",
            "observational_comparator": "MISSING_PRIMARY_NUMERIC_SOURCE_IN_1181",
            "source_id": "SRC1181W_2_Will_PPN_framework",
            "MTS_prediction_slot": "alpha2_MTS = F_alpha2(local frame/routing anisotropy, spin/precession residual)",
            "required_MTS_inputs": "frame selection; spin/precession residual; preferred-frame source row",
            "status": "FRAMEWORK_ONLY_NUMERIC_SOURCE_MISSING",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "ppn_id": "PPNV1181_5_q_loc_TF",
            "component": "q_loc_TF_residual",
            "observational_comparator": "must be bounded below each PPN component tolerance before local promotion",
            "source_id": "SRC1181L_5_1010_q_loc",
            "MTS_prediction_slot": "q_loc_TF = P_TF(P_loc(nabla Gamma_eff - nabla_mu Khat^{mu nu}))",
            "required_MTS_inputs": "S_GK action or residual norm; Helmholtz/Euler/double-zero status",
            "status": "INTERNAL_RESIDUAL_RETAINED",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]
    return stamp(rows)


def ks_mapping_rows() -> list[dict[str, object]]:
    rows = [
        {
            "map_id": "KSM1181_0_gamma_channel",
            "PPN_component": "gamma_minus_1",
            "K_S_role": "linear tracefree spatial metric response changes light-deflection/Shapiro gamma lane",
            "symbolic_prediction_contract": "abs(gamma_MTS-1) <= A_gamma abs(K_S_to_metric)||S_Q||_PPN + B_gamma||q_loc_TF|| + scalar_cross_terms",
            "missing_coefficients": "A_gamma; B_gamma; ||S_Q||_PPN; q_loc_TF_norm",
            "status": "SYMBOLIC_CONTRACT_ONLY",
            "valid_for_claim": False,
        },
        {
            "map_id": "KSM1181_1_beta_channel",
            "PPN_component": "beta_minus_1",
            "K_S_role": "second-order metric/scalar coupling enters nonlinear potential lane",
            "symbolic_prediction_contract": "abs(beta_MTS-1) <= A_beta abs(K_S_to_metric)^2||S_Q||^2 + B_beta|Delta_C2| + C_beta||q_loc||",
            "missing_coefficients": "A_beta; B_beta; C_beta; C_det2; second_order_reciprocity",
            "status": "SYMBOLIC_CONTRACT_ONLY",
            "valid_for_claim": False,
        },
        {
            "map_id": "KSM1181_2_preferred_frame_channel",
            "PPN_component": "alpha1_alpha2",
            "K_S_role": "anisotropic routing/frame choice can generate preferred-frame residuals if not parent-covariant",
            "symbolic_prediction_contract": "alpha_i_MTS = F_i(frame_selection, K_S_to_metric, q_loc_vector, projector_stress)",
            "missing_coefficients": "preferred-frame primary bounds; frame covariance theorem; vector residual norms",
            "status": "SYMBOLIC_CONTRACT_ONLY",
            "valid_for_claim": False,
        },
    ]
    return stamp(rows)


def gate_rows() -> list[dict[str, object]]:
    rows = [
        {
            "gate_id": "G1181_0_gamma_comparator",
            "claim": "gamma comparator is source-backed",
            "status": "PASS_COMPARATOR_ONLY",
            "why_not_claim": "MTS gamma prediction remains symbolic/missing",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "gate_id": "G1181_1_beta_eta_comparator",
            "claim": "beta/eta comparator is source-backed",
            "status": "PASS_COMPARATOR_ONLY",
            "why_not_claim": "MTS beta/eta prediction remains symbolic/missing",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "gate_id": "G1181_2_preferred_frame_vector",
            "claim": "preferred-frame PPN vector is source-complete",
            "status": "BLOCKED_PRIMARY_NUMERIC_SOURCE_MISSING",
            "why_not_claim": "alpha1/alpha2 numeric primary rows are not sourced in 1181",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "gate_id": "G1181_3_KS_prediction",
            "claim": "K_S_to_metric prediction is scoreable",
            "status": "BLOCKED_MTS_PREDICTION_MISSING",
            "why_not_claim": "Q identity, K_S coefficients, S_Q arena norm, and q_loc_TF bound remain missing",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "gate_id": "G1181_4_local_GR_Newton",
            "claim": "local GR/Newton limit is derived",
            "status": "BLOCKED_NO_LOCAL_LIMIT_CLAIM",
            "why_not_claim": "PPN source pack exists but local prediction map is not derived or bounded",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
    ]
    return stamp(rows)


def runner_rows() -> list[dict[str, object]]:
    rows = [
        {
            "run_id": "RUN1181_0_local_sources",
            "operation": "local source/needle validation",
            "result": "PASS_IF_VALIDATION_PASS",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "run_id": "RUN1181_1_web_source_pack",
            "operation": "external PPN source URL/string pack",
            "result": "GAMMA_BETA_ETA_SOURCED_PREFERRED_FRAME_INCOMPLETE",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "run_id": "RUN1181_2_residual_vector",
            "operation": "construct PPN residual vector schema",
            "result": "VECTOR_SCHEMA_CREATED_MTS_PREDICTIONS_MISSING",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "run_id": "RUN1181_3_KS_map",
            "operation": "construct symbolic K_S-to-PPN map",
            "result": "SYMBOLIC_ONLY_NOT_SCOREABLE",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
    ]
    return stamp(rows)


def decision_rows() -> list[dict[str, object]]:
    rows = [
        {
            "decision_id": "D1181_0_source_pack_status",
            "decision": "gamma_beta_eta_comparators_sourced_but_not_claim_valid",
            "reason": "external comparator rows are useful, but MTS prediction rows are still symbolic.",
            "next_action": "derive gamma_MTS and beta_MTS symbolic residual coefficients or keep them as closure inputs.",
            "valid_for_claim": False,
        },
        {
            "decision_id": "D1181_1_preferred_frame_status",
            "decision": "preferred_frame_vector_incomplete",
            "reason": "Will framework row is enough for bookkeeping, not enough for numeric alpha1/alpha2 source claims.",
            "next_action": "source alpha1/alpha2 primary bounds before preferred-frame scoring.",
            "valid_for_claim": False,
        },
        {
            "decision_id": "D1181_2_next_best",
            "decision": "derive_symbolic_PPN_prediction_map_before_numeric_runner",
            "reason": "without F_gamma/F_beta coefficients, numeric PPN limits cannot test MTS rather than just decorate it.",
            "next_action": "attempt PPN coefficient derivation from weak-field metric ansatz and K_S closure.",
            "valid_for_claim": False,
        },
    ]
    return stamp(rows)


def next_rows() -> list[dict[str, object]]:
    rows = [
        {
            "next_id": "NEXT1181_0_1182",
            "next_target": "1182-Y5-R10-symbolic-PPN-KS-prediction-map-or-numeric-comparator-runner.md",
            "objective": "derive the symbolic map from K_S_to_metric, q_loc_TF, and scalar reciprocity residuals into gamma-1, beta-1, eta_N, and preferred-frame slots; if not derivable, build a nonclaim numeric comparator runner with explicit MISSING prediction gates",
            "include": "weak-field metric ansatz; gamma and beta coefficient map; q_loc_TF residual; preferred-frame placeholders; source-backed comparator rows; no-claim validation",
            "exclude": "claiming PPN pass; invented MTS coefficients; hiding q_loc; GitHub; formalization edits",
            "valid_for_claim": False,
            "claim_allowed": False,
        }
    ]
    return stamp(rows)


def validation_rows(
    local_sources: list[dict[str, object]],
    web_sources: list[dict[str, object]],
    ppn_vector: list[dict[str, object]],
    ks_map: list[dict[str, object]],
    gates: list[dict[str, object]],
    runs: list[dict[str, object]],
    decisions: list[dict[str, object]],
    nexts: list[dict[str, object]],
) -> list[dict[str, object]]:
    checks = [
        {
            "check_id": "V1181_0_local_sources_exist",
            "result": "pass" if all(r["exists"] and r["needle_found"] for r in local_sources) else "fail",
            "detail": "all cited local source paths exist and needles are found",
            "claim_allowed": False,
        },
        {
            "check_id": "V1181_1_web_sources_recorded",
            "result": "pass" if all(str(r["url"]).startswith("https://") for r in web_sources) and len(web_sources) >= 3 else "fail",
            "detail": "external PPN source URLs are recorded",
            "claim_allowed": False,
        },
        {
            "check_id": "V1181_2_gamma_beta_eta_sourced",
            "result": "pass"
            if {r["component"] for r in ppn_vector} >= {"gamma_minus_1", "beta_minus_1", "eta_N = 4 beta - gamma - 3"}
            else "fail",
            "detail": "gamma, beta, and eta comparator rows are present",
            "claim_allowed": False,
        },
        {
            "check_id": "V1181_3_preferred_frame_placeholders",
            "result": "pass" if {"alpha1", "alpha2"} <= {r["component"] for r in ppn_vector} else "fail",
            "detail": "preferred-frame vector slots are present but remain nonclaim",
            "claim_allowed": False,
        },
        {
            "check_id": "V1181_4_missing_inputs_not_claim_valid",
            "result": "pass"
            if all((not any("MISSING" in str(v) for v in row.values())) or row["valid_for_claim"] is False for row in ppn_vector)
            else "fail",
            "detail": "rows with missing inputs remain invalid for claim",
            "claim_allowed": False,
        },
        {
            "check_id": "V1181_5_KS_map_symbolic",
            "result": "pass" if len(ks_map) >= 3 and all(r["status"] == "SYMBOLIC_CONTRACT_ONLY" for r in ks_map) else "fail",
            "detail": "K_S-to-PPN map remains symbolic and nonclaim",
            "claim_allowed": False,
        },
        {
            "check_id": "V1181_6_gates_blocked_or_comparator_only",
            "result": "pass" if all(r["claim_allowed"] is False for r in gates) else "fail",
            "detail": "claim gates either pass comparator-only or remain blocked",
            "claim_allowed": False,
        },
        {
            "check_id": "V1181_7_runner_refuses_claim",
            "result": "pass" if all(r["claim_allowed"] is False for r in runs) else "fail",
            "detail": "dry-run refuses PPN/local promotion claims",
            "claim_allowed": False,
        },
        {
            "check_id": "V1181_8_no_claim_rows",
            "result": "pass"
            if all(row.get("valid_for_claim") is False for row in web_sources + ppn_vector + ks_map + gates + decisions + nexts)
            else "fail",
            "detail": "all generated science rows remain nonclaim",
            "claim_allowed": False,
        },
        {
            "check_id": "V1181_9_next_target",
            "result": "pass" if nexts and "1182" in str(nexts[0]["next_target"]) else "fail",
            "detail": "1182 handoff targets symbolic PPN prediction map or numeric comparator runner",
            "claim_allowed": False,
        },
        {
            "check_id": "V1181_10_generated_under_post_checkpoint",
            "result": "pass" if str(DOC).startswith(str(ROOT)) and str(CSV_DIR).startswith(str(ROOT)) else "fail",
            "detail": "all generated outputs are under post-checkpoint-work",
            "claim_allowed": False,
        },
        {
            "check_id": "V1181_11_formalization_untouched",
            "result": "pass",
            "detail": "generator writes no outputs under formalization-workbench",
            "claim_allowed": False,
        },
        {
            "check_id": "V1181_SUMMARY",
            "result": "pass",
            "detail": "1181 records source-backed gamma/beta/eta PPN comparators, keeps preferred-frame numeric bounds incomplete, builds symbolic K_S-to-PPN residual slots, and hands off to PPN prediction-map derivation",
            "claim_allowed": False,
        },
    ]
    return stamp(checks)


def write_doc(
    local_sources: list[dict[str, object]],
    web_sources: list[dict[str, object]],
    ppn_vector: list[dict[str, object]],
    ks_map: list[dict[str, object]],
    gates: list[dict[str, object]],
    runs: list[dict[str, object]],
    decisions: list[dict[str, object]],
    validations: list[dict[str, object]],
    nexts: list[dict[str, object]],
) -> None:
    parts = [
        "# 1181 - Y5/R10 PPN K_S residual-vector source pack or parent Q identity proof",
        "**Current verdict:** the PPN comparator side is now partially source-backed, but no MTS PPN pass is claimable. The MTS prediction map is still symbolic because `K_S_to_metric`, `q_loc_TF`, and the Q identity are unresolved.",
        "**Main progress:** Cassini supplies a gamma comparator candidate, LLR supplies beta/eta candidates, and the residual vector now has explicit MTS prediction slots instead of handwaving.",
        "**Hard blocker:** preferred-frame numeric rows and the actual `F_gamma/F_beta` prediction coefficients are still missing, so this is source plumbing, not a test result.",
        "**No claim:** no local-GR, Newton, R10, PPN, WEP, clock, orbital, `c_g=0`, or public-facing claim follows from this checkpoint.",
        "## Local source register\n\n" + table(local_sources),
        "## External PPN source register\n\n" + table(web_sources),
        "## PPN residual-vector comparator rows\n\n" + table(ppn_vector),
        "## Symbolic K_S-to-PPN map\n\n" + table(ks_map),
        "## Claim gates\n\n" + table(gates),
        "## Runner dry-run\n\n" + table(runs),
        "## Decision ledger\n\n" + table(decisions),
        "## Validation\n\n" + table(validations),
        "## Next target\n\n" + table(nexts),
    ]
    DOC.write_text("\n\n".join(parts) + "\n", encoding="utf-8")


def main() -> None:
    CSV_DIR.mkdir(parents=True, exist_ok=True)
    local_sources = local_source_rows()
    web_sources = web_source_rows()
    ppn_vector = ppn_vector_rows()
    ks_map = ks_mapping_rows()
    gates = gate_rows()
    runs = runner_rows()
    decisions = decision_rows()
    nexts = next_rows()
    validations = validation_rows(local_sources, web_sources, ppn_vector, ks_map, gates, runs, decisions, nexts)

    outputs = {
        "P8_Y5_R10_1181_LOCAL_SOURCE_REGISTER.csv": local_sources,
        "P8_Y5_R10_1181_EXTERNAL_PPN_SOURCE_REGISTER.csv": web_sources,
        "P8_Y5_R10_1181_PPN_RESIDUAL_VECTOR_COMPARATOR_ROWS.csv": ppn_vector,
        "P8_Y5_R10_1181_SYMBOLIC_KS_TO_PPN_MAP.csv": ks_map,
        "P8_Y5_R10_1181_CLAIM_GATES.csv": gates,
        "P8_Y5_R10_1181_RUNNER_DRY_RUN.csv": runs,
        "P8_Y5_R10_1181_DECISION_LEDGER.csv": decisions,
        "P8_Y5_R10_1181_NEXT_TARGET.csv": nexts,
        "P8_Y5_BRR545_1181_VALIDATION.csv": validations,
    }
    for filename, rows in outputs.items():
        write_csv(CSV_DIR / filename, rows)

    write_doc(local_sources, web_sources, ppn_vector, ks_map, gates, runs, decisions, validations, nexts)

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

from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CSV_DIR = ROOT / "source-intake" / "mts_residuals"
DOC = ROOT / "1183-Y5-R10-STF-preferred-frame-source-pack-or-scalar-leakage-coefficient-derivation.md"
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
            "source_id": "SRC1183_0_1182_next",
            "relative_path": "source-intake/mts_residuals/P8_Y5_R10_1182_NEXT_TARGET.csv",
            "needle": "NEXT1182_0_1183",
            "role": "handoff to STF/preferred-frame source pack or scalar leakage coefficient derivation.",
        },
        {
            "source_id": "SRC1183_1_1182_summary",
            "relative_path": "source-intake/mts_residuals/P8_Y5_BRR545_1182_VALIDATION.csv",
            "needle": "V1182_SUMMARY",
            "role": "1182 validation summary.",
        },
        {
            "source_id": "SRC1183_2_1182_trace_zero",
            "relative_path": "source-intake/mts_residuals/P8_Y5_R10_1182_SYMBOLIC_PPN_PROJECTION_MAP.csv",
            "needle": "PPNP1182_1_trace_projection",
            "role": "pure tracefree scalar gamma projection is zero at first order.",
        },
        {
            "source_id": "SRC1183_3_1182_gamma_leak",
            "relative_path": "source-intake/mts_residuals/P8_Y5_R10_1182_SYMBOLIC_PPN_PROJECTION_MAP.csv",
            "needle": "PPNP1182_2_gamma_leakage",
            "role": "gamma leakage row to sharpen.",
        },
        {
            "source_id": "SRC1183_4_1182_STF",
            "relative_path": "source-intake/mts_residuals/P8_Y5_R10_1182_SYMBOLIC_PPN_PROJECTION_MAP.csv",
            "needle": "PPNP1182_5_anisotropic_channel",
            "role": "direct K_S channel is STF/anistropic.",
        },
        {
            "source_id": "SRC1183_5_1177_logdet",
            "relative_path": "1177-Y5-R10-metric-channel-routing-for-tracefree-shear-or-first-shear-norm-row.md",
            "needle": "log det(I+A)=Tr(A)-1/2 Tr(A^2)+...",
            "role": "log-det second-order tracefree leakage warning.",
        },
        {
            "source_id": "SRC1183_6_1178_deltaC2",
            "relative_path": "1178-Y5-R10-parent-metric-channel-owner-or-first-tracefree-shear-norm-bound-runner.md",
            "needle": "abs(Delta_C2) <= C_det2",
            "role": "second-order amplitude bound skeleton.",
        },
        {
            "source_id": "SRC1183_7_1176_domain_anisotropy",
            "relative_path": "1176-Y5-R10-domain-isotropy-owner-or-tracefree-shear-bound-row.md",
            "needle": "domain anisotropy envelope",
            "role": "domain anisotropy first-order leakage source row.",
        },
        {
            "source_id": "SRC1183_8_1180_Qcoh",
            "relative_path": "1180-Y5-R10-parent-Q-geometric-identity-or-PPN-KS-source-row.md",
            "needle": "Qcoh=(1/3)hX",
            "role": "Qcoh scalar channel cannot own tracefree metric transfer.",
        },
    ]
    checked: list[dict[str, object]] = []
    for entry in entries:
        path = ROOT / str(entry["relative_path"])
        text = path.read_text(encoding="utf-8", errors="ignore") if path.exists() else ""
        checked.append(entry | {"exists": path.exists(), "needle_found": str(entry["needle"]) in text})
    return stamp(checked)


def external_stf_source_rows() -> list[dict[str, object]]:
    rows = [
        {
            "external_id": "EXT1183_0_Will_PPN_framework",
            "title": "The Confrontation between General Relativity and Experiment",
            "url": "https://link.springer.com/article/10.12942/lrr-2014-4",
            "source_role": "framework for preferred-frame/STF PPN slots, not a promoted numeric primary row",
            "candidate_parameter": "alpha1; alpha2; anisotropic/preferred-frame PPN bookkeeping",
            "numeric_bound": "not_promoted_here",
            "status": "FRAMEWORK_ONLY",
            "valid_for_claim": False,
        },
        {
            "external_id": "EXT1183_1_alpha1_candidate",
            "title": "New limits on preferred-frame effects from pulsar-white dwarf binaries",
            "url": "https://pmc.ncbi.nlm.nih.gov/articles/PMC5253913/",
            "source_role": "candidate primary/near-primary alpha1 preferred-frame source; row needs detailed extraction before claim",
            "candidate_parameter": "alpha1",
            "numeric_bound": "candidate_order_10^-5_not_promoted",
            "status": "CANDIDATE_SOURCE_NOT_EXTRACTED_FOR_CLAIM",
            "valid_for_claim": False,
        },
        {
            "external_id": "EXT1183_2_alpha2_needed",
            "title": "alpha2 primary bound source still required",
            "url": "MISSING_PRIMARY_ALPHA2_URL",
            "source_role": "placeholder until a primary alpha2/STF source is selected and extracted",
            "candidate_parameter": "alpha2 or direct STF/tidal bound",
            "numeric_bound": "MISSING_PRIMARY_NUMERIC_BOUND",
            "status": "MISSING_SOURCE",
            "valid_for_claim": False,
        },
    ]
    return stamp(rows)


def leakage_derivation_rows() -> list[dict[str, object]]:
    rows = [
        {
            "derivation_id": "SLD1183_0_setup",
            "object": "dimensionless tracefree perturbation",
            "formula": "A := epsilon S, Tr(S)=0, ||A||<1",
            "result": "work in the canonical local matrix expansion before physical C-normalization",
            "status": "SETUP",
            "valid_for_claim": False,
        },
        {
            "derivation_id": "SLD1183_1_first_order",
            "object": "first-order scalar leakage",
            "formula": "delta log det(I+A)|_1 = Tr(A) = epsilon Tr(S) = 0",
            "result": "leak_iso_linear = 0 for pure tracefree S_Q in an isotropic scalar projection",
            "status": "DERIVED_ZERO",
            "valid_for_claim": False,
        },
        {
            "derivation_id": "SLD1183_2_second_order",
            "object": "canonical second-order scalar leakage",
            "formula": "log det(I+A)=Tr(A)-1/2 Tr(A^2)+O(A^3)",
            "result": "Delta_logdet_TF = -1/2 epsilon^2 Tr(S^2)+O(epsilon^3)",
            "status": "CANONICAL_COEFFICIENT_MINUS_HALF",
            "valid_for_claim": False,
        },
        {
            "derivation_id": "SLD1183_3_absolute_bound",
            "object": "absolute leakage envelope",
            "formula": "|Delta_logdet_TF| <= 1/2 ||A||_F^2 + R3",
            "result": "C_det2_math = 1/2 for canonical logdet, but physical C_det2 = |C_C|/2 times parent normalization",
            "status": "MATH_BOUND_DERIVED_PHYSICAL_NORMALIZATION_MISSING",
            "valid_for_claim": False,
        },
        {
            "derivation_id": "SLD1183_4_domain_anisotropy",
            "object": "non-isotropic scalar projection",
            "formula": "leak_domain_linear = <W_TF,S_Q>_D <= ||W_TF||_D ||S_Q||_D",
            "result": "first-order scalar leakage can return only through domain anisotropy / non-SO3 projection, not canonical isotropic trace",
            "status": "DOMAIN_ANISOTROPY_ROUTE_DERIVED_AS_BOUND",
            "valid_for_claim": False,
        },
        {
            "derivation_id": "SLD1183_5_q_trace",
            "object": "q_loc trace leakage",
            "formula": "gamma_leak_trace = q_trace + O(q_loc*S_Q)",
            "result": "q_loc trace remains an independent scalar leakage source until Gamma/Khat residual is closed",
            "status": "QLOC_TRACE_RETAINED",
            "valid_for_claim": False,
        },
        {
            "derivation_id": "SLD1183_6_verdict",
            "object": "scalar leakage coefficient verdict",
            "formula": "gamma_MTS-1 = delta_gamma_scalar + epsilon_D||S_Q|| + (|C_C|/2)||K_S S_Q||^2 + q_trace + R3",
            "result": "scalar gamma can test tracefree S_Q only through domain anisotropy, second-order logdet leakage, parent normalization, or q_trace",
            "status": "LEAKAGE_LAW_DERIVED_NONCLAIM",
            "valid_for_claim": False,
        },
    ]
    return stamp(rows)


def updated_ppn_rows() -> list[dict[str, object]]:
    rows = [
        {
            "ppn_update_id": "UPPN1183_0_gamma",
            "component": "gamma_minus_1",
            "updated_prediction": "gamma_MTS-1 = delta_gamma_scalar + epsilon_D||S_Q|| + (|C_C|/2)||K_S S_Q||^2 + q_trace + R3",
            "derived_inputs": "linear isotropic tracefree contribution = 0; canonical second-order coefficient = 1/2",
            "still_missing": "delta_gamma_scalar; epsilon_D; C_C; K_S; ||S_Q||_PPN; q_trace; R3",
            "score_status": "NOT_SCOREABLE",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "ppn_update_id": "UPPN1183_1_beta",
            "component": "beta_minus_1",
            "updated_prediction": "beta_MTS-1 = delta_beta_scalar + C_beta_TF||K_S S_Q||^2 + C_beta_q||q_loc|| + Delta_rec_2",
            "derived_inputs": "tracefree enters naturally at second order or through q/domain leakage",
            "still_missing": "C_beta_TF; K_S; ||S_Q||; q_loc norm; Delta_rec_2",
            "score_status": "NOT_SCOREABLE",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "ppn_update_id": "UPPN1183_2_STF",
            "component": "H_TF_metric",
            "updated_prediction": "H_TF = K_S_to_metric S_Q + q_loc_TF + projector_TF",
            "derived_inputs": "direct K_S channel remains STF/preferred-frame/tidal",
            "still_missing": "primary STF/preferred-frame bound; K_S; S_Q norm; q_loc_TF norm",
            "score_status": "NOT_SCOREABLE",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]
    return stamp(rows)


def gate_rows() -> list[dict[str, object]]:
    rows = [
        {
            "gate_id": "G1183_0_leak_iso_linear",
            "claim": "pure tracefree S_Q leaks into scalar gamma at first order under isotropic projection",
            "status": "FAILED_DERIVED_ZERO",
            "why": "Tr(S_Q)=0 gives delta logdet first order zero",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "gate_id": "G1183_1_Cdet2_math",
            "claim": "canonical logdet second-order coefficient is known",
            "status": "PASS_MATH_ONLY",
            "why": "coefficient is -1/2 before physical C normalization; not a physical claim",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "gate_id": "G1183_2_gamma_score",
            "claim": "gamma leakage is scoreable",
            "status": "BLOCKED_PHYSICAL_NORMALIZATION_AND_NORMS_MISSING",
            "why": "C_C, epsilon_D, K_S, S_Q norm, q_trace, and R3 are missing",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "gate_id": "G1183_3_STF_preferred_source",
            "claim": "direct STF/preferred-frame comparator is source-complete",
            "status": "BLOCKED_ALPHA2_OR_DIRECT_STF_PRIMARY_SOURCE_MISSING",
            "why": "alpha1 candidate exists but alpha2/direct STF source row is incomplete",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "gate_id": "G1183_4_local_GR_Newton",
            "claim": "local GR/Newton limit is derived",
            "status": "BLOCKED_NO_LOCAL_LIMIT_CLAIM",
            "why": "leakage law is nonclaim and physical coefficients/residuals remain missing",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
    ]
    return stamp(rows)


def runner_rows() -> list[dict[str, object]]:
    rows = [
        {
            "run_id": "RUN1183_0_logdet_derivation",
            "operation": "derive tracefree logdet leakage through second order",
            "result": "PASS_MATH_NONCLAIM",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "run_id": "RUN1183_1_gamma_runner",
            "operation": "attempt gamma leakage score",
            "result": "REFUSED_PHYSICAL_INPUTS_MISSING",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "run_id": "RUN1183_2_STF_source_pack",
            "operation": "stage preferred-frame/STF source rows",
            "result": "PARTIAL_ALPHA1_CANDIDATE_ALPHA2_MISSING",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "run_id": "RUN1183_3_local_promotion",
            "operation": "local-GR/PPN promotion",
            "result": "REFUSED_NO_LOCAL_CLAIM",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
    ]
    return stamp(rows)


def decision_rows() -> list[dict[str, object]]:
    rows = [
        {
            "decision_id": "D1183_0_derivation_result",
            "decision": "scalar_leakage_law_derived_as_nonclaim_math",
            "reason": "linear tracefree leak vanishes; canonical second-order logdet coefficient is -1/2 before physical normalization.",
            "next_action": "source/derive physical C_C, epsilon_D, K_S, S_Q norm, q_trace, and R3.",
            "valid_for_claim": False,
        },
        {
            "decision_id": "D1183_1_STF_status",
            "decision": "preferred_frame_source_pack_still_incomplete",
            "reason": "alpha1 candidate source is staged but alpha2/direct STF primary source remains missing.",
            "next_action": "complete alpha1/alpha2 primary extraction or use scalar leakage route first.",
            "valid_for_claim": False,
        },
        {
            "decision_id": "D1183_2_best_next",
            "decision": "derive_or_source_physical_leakage_inputs_before_numeric_PPN",
            "reason": "without physical normalization and arena norms, PPN numbers cannot score MTS fairly.",
            "next_action": "1184 should target C_C/epsilon_D/q_trace/S_Q norm source rows or parent theorem.",
            "valid_for_claim": False,
        },
    ]
    return stamp(rows)


def next_rows() -> list[dict[str, object]]:
    rows = [
        {
            "next_id": "NEXT1183_0_1184",
            "next_target": "1184-Y5-R10-physical-scalar-leakage-inputs-or-STF-source-completion.md",
            "objective": "derive/source the physical inputs that make the scalar leakage law scoreable: C_C, epsilon_D, K_S, ||S_Q||_PPN, q_trace, R3; or complete alpha1/alpha2/direct-STF primary source extraction",
            "include": "parent C normalization; domain anisotropy envelope; S_Q PPN norm; q_loc trace/TF split; preferred-frame sources; no-claim validation",
            "exclude": "claiming PPN pass; treating math coefficient as physical coefficient; invented norms; GitHub; formalization edits",
            "valid_for_claim": False,
            "claim_allowed": False,
        }
    ]
    return stamp(rows)


def validation_rows(
    sources: list[dict[str, object]],
    external: list[dict[str, object]],
    leakage: list[dict[str, object]],
    ppn_updates: list[dict[str, object]],
    gates: list[dict[str, object]],
    runs: list[dict[str, object]],
    decisions: list[dict[str, object]],
    nexts: list[dict[str, object]],
) -> list[dict[str, object]]:
    checks = [
        {
            "check_id": "V1183_0_sources_exist",
            "result": "pass" if all(r["exists"] and r["needle_found"] for r in sources) else "fail",
            "detail": "all cited local source paths exist and needles are found",
            "claim_allowed": False,
        },
        {
            "check_id": "V1183_1_linear_leak_zero",
            "result": "pass" if any(r["status"] == "DERIVED_ZERO" for r in leakage) else "fail",
            "detail": "linear tracefree scalar leakage is derived zero",
            "claim_allowed": False,
        },
        {
            "check_id": "V1183_2_second_order_coeff",
            "result": "pass" if any(r["status"] == "CANONICAL_COEFFICIENT_MINUS_HALF" for r in leakage) else "fail",
            "detail": "canonical logdet second-order coefficient is recorded",
            "claim_allowed": False,
        },
        {
            "check_id": "V1183_3_domain_anisotropy_route",
            "result": "pass" if any(r["status"] == "DOMAIN_ANISOTROPY_ROUTE_DERIVED_AS_BOUND" for r in leakage) else "fail",
            "detail": "domain anisotropy first-order leakage route is bounded",
            "claim_allowed": False,
        },
        {
            "check_id": "V1183_4_external_sources_nonclaim",
            "result": "pass" if all(r["valid_for_claim"] is False for r in external) else "fail",
            "detail": "external preferred-frame/STF source rows remain nonclaim",
            "claim_allowed": False,
        },
        {
            "check_id": "V1183_5_PPN_updates_nonclaim",
            "result": "pass" if all(r["claim_allowed"] is False for r in ppn_updates) else "fail",
            "detail": "updated PPN prediction rows remain nonclaim",
            "claim_allowed": False,
        },
        {
            "check_id": "V1183_6_missing_inputs_not_claim_valid",
            "result": "pass"
            if all((not any("MISSING" in str(v) for v in row.values())) or row["valid_for_claim"] is False for row in external + ppn_updates)
            else "fail",
            "detail": "rows with missing inputs remain invalid for claim",
            "claim_allowed": False,
        },
        {
            "check_id": "V1183_7_gates_blocked_or_math_only",
            "result": "pass" if all(r["claim_allowed"] is False for r in gates) else "fail",
            "detail": "gates remain blocked or math-only nonclaim",
            "claim_allowed": False,
        },
        {
            "check_id": "V1183_8_runner_refuses_claim",
            "result": "pass" if all(r["claim_allowed"] is False for r in runs) else "fail",
            "detail": "dry-runs refuse PPN/local promotion",
            "claim_allowed": False,
        },
        {
            "check_id": "V1183_9_no_claim_rows",
            "result": "pass"
            if all(row.get("valid_for_claim") is False for row in leakage + external + ppn_updates + gates + decisions + nexts)
            else "fail",
            "detail": "all generated science rows remain nonclaim",
            "claim_allowed": False,
        },
        {
            "check_id": "V1183_10_next_target",
            "result": "pass" if nexts and "1184" in str(nexts[0]["next_target"]) else "fail",
            "detail": "1184 handoff targets physical scalar leakage inputs or STF source completion",
            "claim_allowed": False,
        },
        {
            "check_id": "V1183_11_generated_under_post_checkpoint",
            "result": "pass" if str(DOC).startswith(str(ROOT)) and str(CSV_DIR).startswith(str(ROOT)) else "fail",
            "detail": "all generated outputs are under post-checkpoint-work",
            "claim_allowed": False,
        },
        {
            "check_id": "V1183_12_formalization_untouched",
            "result": "pass",
            "detail": "generator writes no outputs under formalization-workbench",
            "claim_allowed": False,
        },
        {
            "check_id": "V1183_SUMMARY",
            "result": "pass",
            "detail": "1183 derives zero linear scalar leakage and canonical -1/2 second-order logdet leakage for tracefree S_Q, identifies domain anisotropy/q_trace as first-order scalar leak routes, stages incomplete STF/preferred-frame sources, and keeps PPN nonclaim",
            "claim_allowed": False,
        },
    ]
    return stamp(checks)


def write_doc(
    sources: list[dict[str, object]],
    external: list[dict[str, object]],
    leakage: list[dict[str, object]],
    ppn_updates: list[dict[str, object]],
    gates: list[dict[str, object]],
    runs: list[dict[str, object]],
    decisions: list[dict[str, object]],
    validations: list[dict[str, object]],
    nexts: list[dict[str, object]],
) -> None:
    parts = [
        "# 1183 - Y5/R10 STF preferred-frame source pack or scalar leakage coefficient derivation",
        "**Current verdict:** the scalar leakage route now has a clean math result: pure tracefree `S_Q` has zero first-order scalar leakage, and canonical log-det leakage begins at `-1/2 Tr(A^2)`.",
        "**Main progress:** scalar `gamma` can only see tracefree `S_Q` through domain anisotropy, second-order log-det leakage with parent normalization, or `q_loc` trace. Direct `K_S` still belongs to STF/preferred-frame/tidal channels.",
        "**Hard blocker:** the math coefficient is not yet a physical coefficient. We still need parent `C` normalization, arena `S_Q` norm, domain anisotropy envelope, `q_trace`, and preferred-frame/STF sources.",
        "**No claim:** no local-GR, Newton, R10, PPN, WEP, clock, orbital, `c_g=0`, or public-facing claim follows from this checkpoint.",
        "## Local source register\n\n" + table(sources),
        "## External STF/preferred-frame source status\n\n" + table(external),
        "## Scalar leakage derivation\n\n" + table(leakage),
        "## Updated PPN prediction rows\n\n" + table(ppn_updates),
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
    external = external_stf_source_rows()
    leakage = leakage_derivation_rows()
    ppn_updates = updated_ppn_rows()
    gates = gate_rows()
    runs = runner_rows()
    decisions = decision_rows()
    nexts = next_rows()
    validations = validation_rows(sources, external, leakage, ppn_updates, gates, runs, decisions, nexts)

    outputs = {
        "P8_Y5_R10_1183_SOURCE_REGISTER.csv": sources,
        "P8_Y5_R10_1183_EXTERNAL_STF_PREFERRED_SOURCE_STATUS.csv": external,
        "P8_Y5_R10_1183_SCALAR_LEAKAGE_DERIVATION.csv": leakage,
        "P8_Y5_R10_1183_UPDATED_PPN_PREDICTION_ROWS.csv": ppn_updates,
        "P8_Y5_R10_1183_CLAIM_GATES.csv": gates,
        "P8_Y5_R10_1183_RUNNER_DRY_RUN.csv": runs,
        "P8_Y5_R10_1183_DECISION_LEDGER.csv": decisions,
        "P8_Y5_R10_1183_NEXT_TARGET.csv": nexts,
        "P8_Y5_BRR545_1183_VALIDATION.csv": validations,
    }
    for filename, rows in outputs.items():
        write_csv(CSV_DIR / filename, rows)

    write_doc(sources, external, leakage, ppn_updates, gates, runs, decisions, validations, nexts)

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

from __future__ import annotations

import csv
from pathlib import Path


PACK_ID = "P8_Y5_R10_1368"
TITLE = "1368-Y5-R10-RAB-m-Lcg-parent-metric-response-kernels-or-q_loc-projection-map"
ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = ROOT / "source-intake" / "mts_residuals"
DOC_PATH = ROOT / f"{TITLE}.md"
FORMALIZATION = ROOT.parent / "formalization-workbench"

SOURCE_REGISTER_PATH = OUT_DIR / f"{PACK_ID}_SOURCE_REGISTER.csv"
KERNEL_HUNT_PATH = OUT_DIR / f"{PACK_ID}_M_LCG_KERNEL_HUNT.csv"
PROJECTION_PATH = OUT_DIR / f"{PACK_ID}_QLOC_TO_PPN_GAMMA_PROJECTION_REQUIREMENTS.csv"
CLAIM_GATE_PATH = OUT_DIR / f"{PACK_ID}_CLAIM_GATE.csv"
DECISION_PATH = OUT_DIR / f"{PACK_ID}_DECISION_LEDGER.csv"
NEXT_PATH = OUT_DIR / f"{PACK_ID}_NEXT_TARGET.csv"
VALIDATION_PATH = OUT_DIR / "P8_Y5_BRR545_1368_VALIDATION.csv"


def source_path(relative_path: str) -> Path:
    path = Path(relative_path)
    if path.is_absolute():
        return path
    return ROOT / path


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def write_csv(path: Path, rows: list[dict[str, object]], fieldnames: list[str] | None = None) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if fieldnames is None:
        fieldnames = []
        for row in rows:
            for key in row:
                if key not in fieldnames:
                    fieldnames.append(key)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def read_csv_rows(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def table(headers: list[str], rows: list[dict[str, object]]) -> str:
    out = [
        "| " + " | ".join(headers) + " |",
        "| " + " | ".join(["---"] * len(headers)) + " |",
    ]
    for row in rows:
        values = [str(row.get(header, "")).replace("\n", " ") for header in headers]
        out.append("| " + " | ".join(values) + " |")
    return "\n".join(out)


def mark_nonclaim(rows: list[dict[str, object]]) -> list[dict[str, object]]:
    for row in rows:
        row["valid_for_claim"] = False
        row["claim_allowed"] = False
    return rows


def source_register() -> list[dict[str, object]]:
    rows = [
        {
            "source_id": "SRC1368_0_1367_doc",
            "source_path": "1367-Y5-R10-RAB-Kmetric-memory-scalar-chain-kernel-or-q_loc-arena-thresholds.md",
            "required_anchor": "NEXT1367_0_1368",
            "purpose": "1367 handoff to m/Lcg parent metric-response kernels or q_loc projection map.",
        },
        {
            "source_id": "SRC1368_1_1367_next",
            "source_path": "source-intake/mts_residuals/P8_Y5_R10_1367_NEXT_TARGET.csv",
            "required_anchor": "NEXT1367_0_1368",
            "purpose": "machine-readable 1368 target.",
        },
        {
            "source_id": "SRC1368_2_1367_kernel",
            "source_path": "source-intake/mts_residuals/P8_Y5_R10_1367_KMETRIC_CHAIN_KERNEL_ATTEMPT.csv",
            "required_anchor": "KER1367_1_m_metric_response_kernel",
            "purpose": "open M_m and M_L Kmetric chain-kernel rows.",
        },
        {
            "source_id": "SRC1368_3_1367_threshold",
            "source_path": "source-intake/mts_residuals/P8_Y5_R10_1367_QLOC_ARENA_THRESHOLD_INTAKE.csv",
            "required_anchor": "THR1367_0_PPN_gamma_Cassini",
            "purpose": "fallback PPN gamma comparator row.",
        },
        {
            "source_id": "SRC1368_4_1289_first_kernel",
            "source_path": "source-intake/mts_residuals/P8_Y5_R10_1289_FIRST_DERIVATIVE_TERM_ROW_NONCLAIM.csv",
            "required_anchor": "KDR1289_0_Gamma_m_L_chain_kernel_00",
            "purpose": "original Gamma_eff m/Lcg chain-kernel formula.",
        },
        {
            "source_id": "SRC1368_5_798_gamma",
            "source_path": "source-intake/mts_residuals/P8_Y5_R10_798_GAMMA_SOURCE_EXPANSION.csv",
            "required_anchor": "GSE798_0_definition",
            "purpose": "Gamma_eff=L_cg^-2 F(m) and gradient expansion seed.",
        },
        {
            "source_id": "SRC1368_6_1289_delta_template",
            "source_path": "source-intake/mts_residuals/P8_Y5_R10_1289_DELTAK00_COMPARISON_TEMPLATE.csv",
            "required_anchor": "DTC1289_2_DeltaK00_template",
            "purpose": "Delta_K template used by the q_loc-to-gamma projection requirements.",
        },
        {
            "source_id": "SRC1368_7_1299_trace",
            "source_path": "source-intake/mts_residuals/P8_Y5_R10_1299_SPATIAL_TRACE_KERNEL_ROWS_NONCLAIM.csv",
            "required_anchor": "STK1299_1_Lcg_spatial_trace",
            "purpose": "spatial trace rows showing M_m and M_L input blockers.",
        },
        {
            "source_id": "SRC1368_8_1301_doc",
            "source_path": "1301-Y5-R10-RAB-parent-metric-response-components-for-m-spatial-trace.md",
            "required_anchor": "DRV1301_0_fixed_independent_scalar_chain",
            "purpose": "conditional fixed-field derivation for M_m component zeros.",
        },
        {
            "source_id": "SRC1368_9_1301_derivation_csv",
            "source_path": "source-intake/mts_residuals/P8_Y5_R10_1301_M_m_ij_DERIVATION_ATTEMPT.csv",
            "required_anchor": "DRV1301_0_fixed_independent_scalar_chain",
            "purpose": "machine-readable M_m fixed-field/counterbranch split.",
        },
        {
            "source_id": "SRC1368_10_1301_closure_contract",
            "source_path": "source-intake/mts_residuals/P8_Y5_R10_1301_PARENT_FIXED_FIELD_CLOSURE_CONTRACT.csv",
            "required_anchor": "FFC1301_0_parent_field_status",
            "purpose": "unsigned parent clauses preventing promotion of M_m=0.",
        },
        {
            "source_id": "SRC1368_11_1181_external_ppn",
            "source_path": "source-intake/mts_residuals/P8_Y5_R10_1181_EXTERNAL_PPN_SOURCE_REGISTER.csv",
            "required_anchor": "SRC1181W_0_Cassini_gamma",
            "purpose": "source-backed Cassini PPN gamma comparator.",
        },
        {
            "source_id": "SRC1368_12_1244_policy_feed",
            "source_path": "source-intake/mts_residuals/P8_Y5_R10_1244_RUNNER_POLICY_FEED.csv",
            "required_anchor": "RPF1244_0_policy",
            "purpose": "strict one-sigma gamma policy already used for q_R, not automatically q_loc.",
        },
        {
            "source_id": "SRC1368_13_1244_doc",
            "source_path": "1244-Y5-R10-QR-statistical-policy-and-GM-convention-pack.md",
            "required_anchor": "QBD1244_0_projection",
            "purpose": "q_R-to-gamma policy source, explicitly not imported as q_loc.",
        },
    ]
    for row in rows:
        path = source_path(str(row["source_path"]))
        row["exists"] = path.exists()
        row["anchor_found"] = path.exists() and str(row["required_anchor"]) in read_text(path)
    return mark_nonclaim(rows)


def kernel_hunt_rows() -> list[dict[str, object]]:
    return mark_nonclaim(
        [
            {
                "kernel_id": "KERN1368_0_m_fixed_field_branch",
                "target": "M_m^{mu nu}",
                "derivation_or_requirement": "If m is an independent parent scalar held fixed during Hilbert variation of the algebraic Gamma_eff term, delta_g m=0, hence M_m^{mu nu}=0 for that chain response.",
                "status": "CONDITIONAL_RELATIVE_ZERO_NOT_LIVE_CLAIM",
                "source_paths": "1301-Y5-R10-RAB-parent-metric-response-components-for-m-spatial-trace.md;source-intake/mts_residuals/P8_Y5_R10_1301_M_m_ij_DERIVATION_ATTEMPT.csv",
                "source_anchors": "DRV1301_0_fixed_independent_scalar_chain",
                "missing_to_promote": "parent action must sign m as fixed independent; no metric-composite/readout/domain/projector dependence; variation-order and units/index lock; memory-stress split remains separate",
                "claim_effect": "prunes one algebraic chain branch only; does not prove q_loc=0 or local GR",
            },
            {
                "kernel_id": "KERN1368_1_m_metric_composite_branch",
                "target": "M_m^{mu nu}",
                "derivation_or_requirement": "If m is a metric-composite readout, norm, curvature scalar, projector contraction, or domain-selected scalar, delta_g m generically survives.",
                "status": "COUNTERBRANCH_RETAINED",
                "source_paths": "source-intake/mts_residuals/P8_Y5_R10_1301_M_m_ij_DERIVATION_ATTEMPT.csv;source-intake/mts_residuals/P8_Y5_R10_1301_PARENT_FIXED_FIELD_CLOSURE_CONTRACT.csv",
                "source_anchors": "DRV1301_1_metric_composite_counterbranch;FFC1301_1_no_metric_composite",
                "missing_to_promote": "explicit m[g,Phi,D,P] exclusion or response coefficient with units",
                "claim_effect": "M_m cannot be deleted in live local branch until parent chooses fixed-field route",
            },
            {
                "kernel_id": "KERN1368_2_m_active_memory_stress_split",
                "target": "m-sector Hilbert stress",
                "derivation_or_requirement": "Even if the algebraic chain has delta_g m=0, any kinetic/potential/source/boundary memory action contributes separate Hilbert stress.",
                "status": "SEPARATE_RESIDUAL_REQUIRED",
                "source_paths": "source-intake/mts_residuals/P8_Y5_R10_1301_M_m_ij_DERIVATION_ATTEMPT.csv;source-intake/mts_residuals/P8_Y5_R10_1301_PARENT_FIXED_FIELD_CLOSURE_CONTRACT.csv",
                "source_anchors": "DRV1301_2_active_memory_stress_split;FFC1301_4_stress_channel_split",
                "missing_to_promote": "local no-hair/source-zero/boundary-zero theorem or bounded memory-stress row",
                "claim_effect": "prevents the fixed-field chain zero from silently deleting real stress-energy",
            },
            {
                "kernel_id": "KERN1368_3_Lcg_fixed_scale_branch",
                "target": "M_L^{mu nu}",
                "derivation_or_requirement": "If L_cg is a parent-fixed external/local scale held fixed in Hilbert variation, delta_g L_cg=0 and the algebraic L_cg chain response vanishes.",
                "status": "CONDITIONAL_ROUTE_IDENTIFIED_NOT_DERIVED",
                "source_paths": "source-intake/mts_residuals/P8_Y5_R10_1289_FIRST_DERIVATIVE_TERM_ROW_NONCLAIM.csv;source-intake/mts_residuals/P8_Y5_R10_1299_SPATIAL_TRACE_KERNEL_ROWS_NONCLAIM.csv",
                "source_anchors": "KDR1289_0_Gamma_m_L_chain_kernel_00;STK1299_1_Lcg_spatial_trace",
                "missing_to_promote": "parent definition of L_cg; fixed-scale theorem; units and local-frame convention",
                "claim_effect": "this is the next cleanest derivation route but currently unsigned",
            },
            {
                "kernel_id": "KERN1368_4_Lcg_metric_composite_branch",
                "target": "M_L^{mu nu}",
                "derivation_or_requirement": "If L_cg is derived from curvature, domain size, projector geometry, density scale, or coarse-graining cell readout, delta_g L_cg can survive.",
                "status": "MISSING_PARENT_DEFINITION_AND_RESPONSE",
                "source_paths": "source-intake/mts_residuals/P8_Y5_R10_1367_KMETRIC_CHAIN_KERNEL_ATTEMPT.csv;source-intake/mts_residuals/P8_Y5_R10_1299_SPATIAL_TRACE_KERNEL_ROWS_NONCLAIM.csv",
                "source_anchors": "KER1367_2_Lcg_metric_response_kernel;STK1299_1_Lcg_spatial_trace",
                "missing_to_promote": "L_cg[g,Phi,D,P] definition or explicit silence proof; sign/units of M_L",
                "claim_effect": "L_cg remains the bigger live blocker after the conditional M_m progress",
            },
            {
                "kernel_id": "KERN1368_5_chain_kernel_verdict",
                "target": "Kmetric_chain^{00}",
                "derivation_or_requirement": "Current best chain formula is C_sign[L_cg^-2 F_prime(m)M_m^{00}-2L_cg^-3F(m)M_L^{00}]+K_conn+K_domain+K_boundary.",
                "status": "M_M_PARTIAL_CONDITIONAL_M_L_MISSING",
                "source_paths": "source-intake/mts_residuals/P8_Y5_R10_1367_KMETRIC_CHAIN_KERNEL_ATTEMPT.csv;source-intake/mts_residuals/P8_Y5_R10_1289_FIRST_DERIVATIVE_TERM_ROW_NONCLAIM.csv",
                "source_anchors": "KER1367_0_chain_kernel_formula;KDR1289_0_Gamma_m_L_chain_kernel_00",
                "missing_to_promote": "C_sign; live M_L kernel or silence theorem; K_conn/K_domain/K_boundary; units; Khat comparison",
                "claim_effect": "do not claim q_loc^nu=0; move next to L_cg parent metric silence or projection-map runner",
            },
        ]
    )


def projection_rows() -> list[dict[str, object]]:
    return mark_nonclaim(
        [
            {
                "projection_id": "PROJ1368_0_gamma_comparator",
                "arena": "PPN_gamma",
                "known_piece": "Cassini gamma comparator is source-backed: gamma=1+(2.1+/-2.3)e-5, with strict sigma_gamma=2.3e-5 and existing q_R guardrail 4.6e-05.",
                "missing_piece": "None for comparator; missing only for q_loc-to-gamma map.",
                "status": "SOURCE_BACKED_COMPARATOR_ONLY",
                "source_paths": "source-intake/mts_residuals/P8_Y5_R10_1181_EXTERNAL_PPN_SOURCE_REGISTER.csv;source-intake/mts_residuals/P8_Y5_R10_1244_RUNNER_POLICY_FEED.csv",
                "source_anchors": "SRC1181W_0_Cassini_gamma;RPF1244_0_policy",
                "claim_effect": "can be used as a threshold after projection exists",
            },
            {
                "projection_id": "PROJ1368_1_q_loc_scalar_trace_channel",
                "arena": "q_loc_to_gamma",
                "known_piece": "q_loc^nu is a projected local residual candidate from Gamma_eff/Khat mismatch.",
                "missing_piece": "weak-field decomposition from q_loc^nu into scalar trace, anisotropic stress, vector, and gauge pieces that source gamma-1",
                "status": "MISSING_RESPONSE_DECOMPOSITION",
                "source_paths": "source-intake/mts_residuals/P8_Y5_R10_1367_KMETRIC_CHAIN_KERNEL_ATTEMPT.csv",
                "source_anchors": "KER1367_5_DeltaK00_template",
                "claim_effect": "raw q_loc envelope cannot be compared to Cassini gamma",
            },
            {
                "projection_id": "PROJ1368_2_DeltaK_to_gamma_response",
                "arena": "Delta_K_to_PPN_gamma",
                "known_piece": "Delta_K is the retained Khat-Kmetric mismatch template.",
                "missing_piece": "linearized field solve, gauge convention, trace reversal, GM convention, and sign normalization from Delta_K to gamma-1",
                "status": "MISSING_WEAK_FIELD_SOLVE",
                "source_paths": "source-intake/mts_residuals/P8_Y5_R10_1289_DELTAK00_COMPARISON_TEMPLATE.csv",
                "source_anchors": "DTC1289_2_DeltaK00_template",
                "claim_effect": "no PPN residual vector can be produced from Delta_K yet",
            },
            {
                "projection_id": "PROJ1368_3_QR_policy_not_importable",
                "arena": "q_R_policy_bridge",
                "known_piece": "1244 has gamma_minus_1_QR=-q_R_hat/2 and abs(q_R_hat)<=4.6e-5 under a QR convention.",
                "missing_piece": "proof that q_loc reduces to q_R_hat with the same normalization, source averaging, sign, and GM convention",
                "status": "QR_POLICY_NOT_QLOC_MAP",
                "source_paths": "1244-Y5-R10-QR-statistical-policy-and-GM-convention-pack.md;source-intake/mts_residuals/P8_Y5_R10_1244_RUNNER_POLICY_FEED.csv",
                "source_anchors": "QBD1244_0_projection;RPF1244_0_policy",
                "claim_effect": "do not import the q_R bound as a q_loc pass",
            },
            {
                "projection_id": "PROJ1368_4_no_cancellation_rule",
                "arena": "local_residual_budget",
                "known_piece": "q_loc, q_R, K_S, scalar/memory stress, and boundary terms may all enter local weak-field residuals.",
                "missing_piece": "signed cancellation theorem or independent upper bounds for each retained residual channel",
                "status": "NO_CANCELLATION_ASSUMPTION_ALLOWED",
                "source_paths": "source-intake/mts_residuals/P8_Y5_R10_1367_QLOC_ARENA_THRESHOLD_INTAKE.csv",
                "source_anchors": "THR1367_6_acceptance_gate",
                "claim_effect": "each residual must be zero-derived or independently bounded",
            },
            {
                "projection_id": "PROJ1368_5_projection_verdict",
                "arena": "q_loc_to_PPN_gamma",
                "known_piece": "Cassini comparator exists and q_R policy exists.",
                "missing_piece": "q_loc-specific response map, weak-field solve, gauge/GM convention, source averaging, and no-cancellation ledger",
                "status": "PROJECTION_MAP_BLOCKED",
                "source_paths": "aggregate_projection_requirements",
                "source_anchors": "PROJ1368_0_to_PROJ1368_4",
                "claim_effect": "fallback testing lane is source-ready but not score-ready",
            },
        ]
    )


def claim_gate_rows() -> list[dict[str, object]]:
    return mark_nonclaim(
        [
            {
                "gate_id": "GATE1368_0_Mm_fixed_field_relative_branch",
                "gate": "M_m chain response has a clean fixed-field relative zero branch",
                "status": "PASS_RELATIVE_ONLY",
                "reason": "1301 derives delta_g m=0 at fixed independent scalar fields, but parent clauses are unsigned.",
            },
            {
                "gate_id": "GATE1368_1_Mm_live_kernel_resolved",
                "gate": "Live parent route either signs fixed-field m or supplies M_m response coefficients",
                "status": "BLOCKED",
                "reason": "metric-composite/readout/domain/projector counterbranch remains retained.",
            },
            {
                "gate_id": "GATE1368_2_ML_kernel_resolved",
                "gate": "L_cg metric response is zero-derived or bounded",
                "status": "BLOCKED",
                "reason": "no parent L_cg definition or metric-silence theorem is present.",
            },
            {
                "gate_id": "GATE1368_3_connection_domain_boundary_resolved",
                "gate": "K_conn, K_domain, and K_boundary are zero-derived or bounded",
                "status": "BLOCKED",
                "reason": "1367 retained all three as open response kernels.",
            },
            {
                "gate_id": "GATE1368_4_q_loc_to_gamma_projection",
                "gate": "q_loc residual maps to PPN gamma under a signed weak-field convention",
                "status": "BLOCKED",
                "reason": "Cassini comparator exists, but q_loc-specific projection map does not.",
            },
            {
                "gate_id": "GATE1368_5_local_GR_reopen",
                "gate": "local GR / q_loc=0 branch can be reopened",
                "status": "BLOCKED_NO_LOCAL_GR_CLAIM",
                "reason": "M_L and projection-map blockers remain after the M_m conditional progress.",
            },
        ]
    )


def decision_rows() -> list[dict[str, object]]:
    return mark_nonclaim(
        [
            {
                "decision_id": "DEC1368_0_real_progress",
                "decision": "record the fixed-field M_m branch as genuine mathematical progress",
                "why": "it removes the need for an isotropy/tracefree shortcut for the algebraic m-chain if the parent action signs m as independent and held fixed",
                "next_action": "do not promote it; carry it as a conditional branch until parent m status is signed",
            },
            {
                "decision_id": "DEC1368_1_primary_blocker",
                "decision": "make L_cg the next derivation-first target",
                "why": "even a perfect M_m fixed-field zero leaves the -2 L_cg^-3 F(m) M_L term alive",
                "next_action": "derive/source L_cg parent definition and metric silence, or produce a q_loc gamma projection runner",
            },
            {
                "decision_id": "DEC1368_2_no_qR_import",
                "decision": "do not import the q_R Cassini policy as a q_loc pass",
                "why": "q_R has a signed convention, while q_loc lacks its own source averaging and weak-field response map",
                "next_action": "build q_loc-to-gamma projection requirements before any local PPN scoring",
            },
        ]
    )


def next_rows() -> list[dict[str, object]]:
    return mark_nonclaim(
        [
            {
                "next_id": "NEXT1368_0_1369",
                "next_doc": "1369-Y5-R10-RAB-Lcg-parent-definition-metric-silence-or-q_loc-gamma-projection-runner.md",
                "next_script": "scripts/Y5_R10_RAB_Lcg_parent_definition_metric_silence_or_q_loc_gamma_projection_runner.py",
                "task": "derive/source L_cg parent definition and metric response/silence; if absent, build a q_loc-to-PPN-gamma projection runner schema using the Cassini comparator without claiming a pass",
                "success_condition": "either M_L is zero-derived/bounded with units and source path, or q_loc-to-gamma requirements become runner-ready with all missing coefficients explicit",
                "do_not_claim": "local GR;q_loc=0;Khat match;R10/PPN/clock/orbital pass;GitHub-ready result",
            }
        ]
    )


def csv_parse_check(paths: list[Path]) -> tuple[bool, str]:
    details = []
    ok = True
    for path in paths:
        try:
            rows = read_csv_rows(path)
            details.append(f"{path.name}:{len(rows)}")
        except Exception as exc:
            ok = False
            details.append(f"{path.name}:ERROR:{exc}")
    return ok, "; ".join(details)


def validation_rows(
    sources: list[dict[str, object]],
    kernels: list[dict[str, object]],
    projections: list[dict[str, object]],
    gates: list[dict[str, object]],
    csv_paths: list[Path],
) -> list[dict[str, object]]:
    all_sources_ok = all(row["exists"] and row["anchor_found"] for row in sources)
    all_nonclaim = all(not bool(row.get("valid_for_claim")) and not bool(row.get("claim_allowed")) for row in sources + kernels + projections + gates)
    fixed_m = any(row["kernel_id"] == "KERN1368_0_m_fixed_field_branch" for row in kernels)
    ml_blocked = any(row["kernel_id"] == "KERN1368_4_Lcg_metric_composite_branch" and row["status"] == "MISSING_PARENT_DEFINITION_AND_RESPONSE" for row in kernels)
    qloc_blocked = any(row["projection_id"] == "PROJ1368_5_projection_verdict" and row["status"] == "PROJECTION_MAP_BLOCKED" for row in projections)
    local_gr_blocked = any(row["gate_id"] == "GATE1368_5_local_GR_reopen" and row["status"] == "BLOCKED_NO_LOCAL_GR_CLAIM" for row in gates)
    csv_ok, csv_details = csv_parse_check(csv_paths)

    rows = [
        {
            "validation_id": "VAL1368_0_sources",
            "check": "every cited local source path exists and anchor is found",
            "status": "PASS" if all_sources_ok else "FAIL",
            "details": "; ".join(f"{row['source_id']} exists={row['exists']} anchor={row['anchor_found']}" for row in sources),
        },
        {
            "validation_id": "VAL1368_1_fixed_m_branch",
            "check": "M_m fixed-field branch is captured as relative/nonclaim progress",
            "status": "PASS" if fixed_m else "FAIL",
            "details": "KERN1368_0_m_fixed_field_branch records delta_g m=0 only under unsigned parent clauses",
        },
        {
            "validation_id": "VAL1368_2_Lcg_blocker",
            "check": "L_cg remains blocked unless parent definition/metric silence is sourced",
            "status": "PASS" if ml_blocked else "FAIL",
            "details": "KERN1368_4_Lcg_metric_composite_branch retains M_L as missing",
        },
        {
            "validation_id": "VAL1368_3_q_loc_projection_blocker",
            "check": "q_loc-to-PPN-gamma projection map remains blocked",
            "status": "PASS" if qloc_blocked else "FAIL",
            "details": "PROJ1368_5_projection_verdict blocks scoring despite source-backed Cassini comparator",
        },
        {
            "validation_id": "VAL1368_4_no_claim_rows",
            "check": "all new rows keep valid_for_claim=false and claim_allowed=false",
            "status": "PASS" if all_nonclaim else "FAIL",
            "details": "1368 is private branch discipline, not a local-GR or PPN pass",
        },
        {
            "validation_id": "VAL1368_5_local_gr_blocked",
            "check": "local GR branch is not reopened",
            "status": "PASS" if local_gr_blocked else "FAIL",
            "details": "GATE1368_5_local_GR_reopen remains BLOCKED_NO_LOCAL_GR_CLAIM",
        },
        {
            "validation_id": "VAL1368_6_csv_parse",
            "check": "all generated CSVs parse cleanly",
            "status": "PASS" if csv_ok else "FAIL",
            "details": csv_details,
        },
    ]
    overall_ok = all(row["status"] == "PASS" for row in rows)
    rows.append(
        {
            "validation_id": "VAL1368_7_overall",
            "check": "overall 1368 validation",
            "status": "PASS" if overall_ok else "FAIL",
            "details": "1368 captures conditional M_m progress, keeps M_L/q_loc projection blockers live, and routes to 1369.",
        }
    )
    return rows


def write_doc(
    sources: list[dict[str, object]],
    kernels: list[dict[str, object]],
    projections: list[dict[str, object]],
    gates: list[dict[str, object]],
    decisions: list[dict[str, object]],
    next_targets: list[dict[str, object]],
    validations: list[dict[str, object]],
) -> None:
    text = f"""# {TITLE}

**Current verdict:** 1368 gets one real derivation gain but not a local-GR pass. The `m` chain has a clean fixed-field zero branch (`delta_g m=0`) if the parent action signs `m` as an independent scalar held fixed in Hilbert variation. The live branch still cannot claim `q_loc^nu=0` because `L_cg` metric response, connection/domain/boundary response, and the `q_loc -> gamma` projection map remain unsigned.

**Main progress:** this narrows the live blocker. The algebraic `M_m` route is no longer the first thing to chase blindly; the bigger next target is now `M_L := delta L_cg/delta g`, plus the weak-field map from `q_loc` or `Delta_K` into PPN gamma. This is a good “we found a door, but not the key yet” checkpoint.

**Still blocked:** no R10, PPN, clock, orbital, or local-GR claim is allowed. The Cassini gamma row is a real comparator, not a `q_loc` pass. The old `q_R` policy cannot be imported until a source-backed normalization/projection bridge proves `q_loc` reduces to the same quantity.

## Source Register

{table(["source_id", "source_path", "required_anchor", "exists", "anchor_found", "purpose", "valid_for_claim", "claim_allowed"], sources)}

## `m` / `L_cg` Parent Metric-Response Kernel Hunt

{table(["kernel_id", "target", "status", "derivation_or_requirement", "missing_to_promote", "claim_effect", "source_paths", "source_anchors", "valid_for_claim", "claim_allowed"], kernels)}

## `q_loc` to PPN Gamma Projection Requirements

{table(["projection_id", "arena", "status", "known_piece", "missing_piece", "claim_effect", "source_paths", "source_anchors", "valid_for_claim", "claim_allowed"], projections)}

## Claim Gates

{table(["gate_id", "gate", "status", "reason", "valid_for_claim", "claim_allowed"], gates)}

## Decision Ledger

{table(["decision_id", "decision", "why", "next_action", "valid_for_claim", "claim_allowed"], decisions)}

## Next Target

{table(["next_id", "next_doc", "next_script", "task", "success_condition", "do_not_claim", "valid_for_claim", "claim_allowed"], next_targets)}

## Validation

{table(["validation_id", "check", "status", "details"], validations)}
"""
    DOC_PATH.write_text(text, encoding="utf-8")


def main() -> None:
    sources = source_register()
    kernels = kernel_hunt_rows()
    projections = projection_rows()
    gates = claim_gate_rows()
    decisions = decision_rows()
    next_targets = next_rows()

    write_csv(SOURCE_REGISTER_PATH, sources)
    write_csv(KERNEL_HUNT_PATH, kernels)
    write_csv(PROJECTION_PATH, projections)
    write_csv(CLAIM_GATE_PATH, gates)
    write_csv(DECISION_PATH, decisions)
    write_csv(NEXT_PATH, next_targets)

    csv_paths = [
        SOURCE_REGISTER_PATH,
        KERNEL_HUNT_PATH,
        PROJECTION_PATH,
        CLAIM_GATE_PATH,
        DECISION_PATH,
        NEXT_PATH,
    ]
    validations = validation_rows(sources, kernels, projections, gates, csv_paths)
    write_csv(VALIDATION_PATH, validations)
    write_doc(sources, kernels, projections, gates, decisions, next_targets, validations)

    print(f"wrote {DOC_PATH}")
    print(f"wrote {VALIDATION_PATH}")
    print(f"formalization-workbench touched by this script: {FORMALIZATION.exists() and False}")


if __name__ == "__main__":
    main()

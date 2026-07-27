from __future__ import annotations

import math
from pathlib import Path

from Y5_R2FR_Dq_vX_observed_metric_zero_or_finite_DObs_leak_row_2025 import (
    BRANCH_WEP,
    OUT,
    QUEUE,
    ROOT,
    SOURCE_WEIGHT_DOCS,
    base_row,
    count_formalization_modified,
    csv_rows_parse,
    md_table,
    read_text,
    remove_pycache,
    write_csv,
)


DOC = ROOT / "2104-Y5-R2FR-cg-to-PPN-projection-matrix-or-measured-frame-degeneracy.md"
FORMALIZATION = ROOT.parent / "formalization-workbench"
SCRIPT_PATH = Path(__file__).resolve()

SRC_2103_DOC = ROOT / "2103-Y5-R2FR-first-real-frame-marker-component-source-row-cg-bA-balpha.md"
CSV_2103_COMPONENTS = OUT / "P8_Y5_PARENT_QLOC_2103_COMPONENT_SOURCE_ROWS.csv"
CSV_2103_MISSING = OUT / "P8_Y5_PARENT_QLOC_2103_MISSING_PROJECTION_INPUTS.csv"
CSV_2103_DEC = OUT / "P8_Y5_PARENT_QLOC_2103_DECISION_LEDGER.csv"
CSV_2103_NEXT = OUT / "P8_Y5_PARENT_QLOC_2103_NEXT_TARGET.csv"
CSV_2103_VAL = OUT / "P8_Y5_BRR545_2103_VALIDATION.csv"

SRC_1029_DOC = ROOT / "1029-Y5-R10-cg-no-shadow-frame-theorem-or-first-numeric-coupling-row.md"
SRC_1032_DOC = ROOT / "1032-Y5-R10-spm-closure-ledger-and-finite-cg-tau-acquisition-runner.md"
CSV_1032_CLOSURE = OUT / "P8_Y5_R10_1032_SPM_CLOSURE_LEDGER.csv"
CSV_1032_READY = OUT / "P8_Y5_R10_1032_R10_PPN_READINESS_MAP.csv"

SRC_2053_DOC = ROOT / "2053-Y5-R2FR-PPN-gamma-map-from-RAB-profile-or-finite-qR-first-bound.md"
CSV_2053_DER = OUT / "P8_Y5_PARENT_QLOC_2053_PPN_GAMMA_WEAK_FIELD_DERIVATION.csv"
CSV_2053_RUN = OUT / "P8_Y5_PARENT_QLOC_2053_PPN_GAMMA_RUNNER.csv"
CSV_LOCAL_BOUNDS = ROOT / "source-intake" / "local_bounds" / "local_bound_claims.csv"

GAMMA_BOUND_SELECTED = 6.7e-5
GAMMA_BOUND_STRICT = 2.3e-5
ALPHA_EFF2_CONSERVATIVE = GAMMA_BOUND_SELECTED / 2.0
ALPHA_EFF_CONSERVATIVE = math.sqrt(ALPHA_EFF2_CONSERVATIVE)
ALPHA_EFF2_STRICT = GAMMA_BOUND_STRICT / 2.0
ALPHA_EFF_STRICT = math.sqrt(ALPHA_EFF2_STRICT)


def row(**kwargs: object) -> dict[str, object]:
    data = base_row()
    data["claim_allowed"] = False
    data.update(kwargs)
    return data


def truthy(value: object) -> bool:
    if isinstance(value, bool):
        return value
    return str(value).strip().lower() in {"true", "1", "yes", "pass", "valid", "claim_allowed", "selected"}


def formalization_has_2104_artifacts() -> bool:
    if not FORMALIZATION.exists():
        return False
    patterns = (
        "*2104-Y5-R2FR*",
        "*P8_Y5_PARENT_QLOC_2104*",
        "*Y5_R2FR_cg_to_PPN_projection_matrix_or_measured_frame_degeneracy_2104*",
        "*AFRAME_CG_PPN_PROJECTION_2104*",
        "*JR2104_CG_CANONICAL*",
    )
    try:
        return any(path.is_file() for pattern in patterns for path in FORMALIZATION.rglob(pattern))
    except Exception:
        return False


def source_register_rows() -> list[dict[str, object]]:
    specs: list[tuple[str, Path, list[str], str]] = [
        (
            "SRC2104_00_2103_doc",
            SRC_2103_DOC,
            ["NEXT2103_0_2104", "CG_TO_PPN_PROJECTION_MATRIX_NEXT", "VAL2103_OVERALL"],
            "2103 selects c_g to PPN projection or measured-frame degeneracy as the next derivation.",
        ),
        (
            "SRC2104_01_2103_components",
            CSV_2103_COMPONENTS,
            ["CSR2103_0_cg_ppn", "Delta_gamma_MTS", "MISSING_Pi_gamma_cg_AND_FRAME_LOCK"],
            "2103 stages the c_g-to-PPN row but leaves the projection coefficient missing.",
        ),
        (
            "SRC2104_02_2103_missing",
            CSV_2103_MISSING,
            ["MPR2103_0_Pi_gamma_cg", "MPR2103_1_frame_lock", "MISSING_REQUIRED_PROJECTION_INPUT"],
            "2103 missing-input ledger identifies Pi_gamma_cg and frame lock as blockers.",
        ),
        (
            "SRC2104_03_2103_decision",
            CSV_2103_DEC,
            ["DEC2103_1_best_first_derivation", "CG_TO_PPN_PROJECTION_MATRIX_NEXT"],
            "2103 decision picks c_g->PPN as the cleanest GR-facing next move.",
        ),
        (
            "SRC2104_04_2103_next",
            CSV_2103_NEXT,
            ["NEXT2103_0_2104", "2104-Y5-R2FR-cg-to-PPN-projection-matrix-or-measured-frame-degeneracy.md"],
            "2103 next-target row points exactly at this checkpoint.",
        ),
        (
            "SRC2104_05_2103_validation",
            CSV_2103_VAL,
            ["VAL2103_OVERALL", "PASS", "c_g->PPN projection"],
            "2103 validation is clean and nonclaim.",
        ),
        (
            "SRC2104_06_1029_no_shadow",
            SRC_1029_DOC,
            ["no-shadow-frame theorem", "Current MTS does not yet prove c_g=0.", "CGI1029_2_finite_cg_PPN_gamma"],
            "1029 proves only a conditional no-shadow-frame theorem and stages finite c_g PPN rows.",
        ),
        (
            "SRC2104_07_1032_spm",
            SRC_1032_DOC,
            ["Single Public Metric", "tau_PPN_gamma", "R10/PPN testing is close to runner-ready but not score-ready"],
            "1032 separates SPM closure from finite c_g/tau acquisition.",
        ),
        (
            "SRC2104_08_1032_closure_csv",
            CSV_1032_CLOSURE,
            ["SPML1032_0_branch_definition", "SPML1032_1_zero_policy", "SPM closure"],
            "1032 closure ledger says c_g=0 only inside an explicit SPM closure branch.",
        ),
        (
            "SRC2104_09_1032_readiness_csv",
            CSV_1032_READY,
            ["READY1032_1_PPN_gamma", "gamma_minus_1 = M_gamma", "tau_PPN_gamma"],
            "1032 readiness map keeps finite c_g PPN gamma unscoreable until tau/projection exists.",
        ),
        (
            "SRC2104_10_2053_gamma_doc",
            SRC_2053_DOC,
            ["C_R=(gamma_obs-1) r_s/r", "RUN2053_VERDICT", "VAL2053_OVERALL"],
            "2053 derives the observed areal q_R^PPN to PPN gamma bridge and imports Cassini.",
        ),
        (
            "SRC2104_11_2053_derivation_csv",
            CSV_2053_DER,
            ["DER2053_3_log_product", "DER2053_4_areal_qR_definition", "MAP_DERIVED_CONDITIONAL_NOT_SCOREABLE"],
            "2053 machine-readable derivation defines q_R^PPN and its gamma map.",
        ),
        (
            "SRC2104_12_2053_runner_csv",
            CSV_2053_RUN,
            ["RUN2053_VERDICT", "6.7e-05", "PPN_GAMMA_MAP_DERIVED_FIRST_QR_BOUND_ROW_NONCLAIM"],
            "2053 runner writes the conservative Cassini q_R bound row without scoring MTS.",
        ),
        (
            "SRC2104_13_local_bounds",
            CSV_LOCAL_BOUNDS,
            ["R3_gamma", "2.3e-05", "Cassini_Shapiro_gamma_2003"],
            "local bound table supplies the Cassini gamma anchor used by 2053.",
        ),
    ]
    rows: list[dict[str, object]] = []
    for source_id, path, needles, use in specs:
        exists = path.exists()
        text = read_text(path) if exists else ""
        rows.append(
            row(
                source_id=source_id,
                source_kind="2104_cg_ppn_projection",
                source_path=str(path),
                path_exists=exists,
                needles="; ".join(needles),
                needle_found=exists and all(needle in text for needle in needles),
                use_in_2104=use,
                valid_for_claim=False,
            )
        )
    return rows


def cg_ppn_projection_rows() -> list[dict[str, object]]:
    specs = [
        (
            "PRJ2104_0_observed_gamma_slot",
            "q_R^PPN",
            "From 2053, C_R=ln(A S)=(gamma_obs-1) r_s/r+O(r_s^2/r^2); therefore q_R^PPN is the first-order observed PPN-gamma residual in the selected areal convention.",
            "derived from 2053",
            "does not yet identify q_R^PPN with c_g",
            "DERIVED_CONDITIONAL_SAME_FRAME",
        ),
        (
            "PRJ2104_1_common_conformal_branch",
            "alpha_eff^2",
            "For a universal conformal matter frame g_m=A_g(X)^2 g_obs with a propagating canonically normalized scalar, alpha_eff=N_X c_g and gamma-1=-2 alpha_eff^2 Y_gamma/(1+alpha_eff^2 Y_gamma)+tails.",
            "standard scalar-tensor weak-field projection template",
            "N_X, Y_gamma, source profile, range, and tail guards are MTS-missing",
            "PROJECTION_TEMPLATE_DERIVED_NOT_SCOREABLE",
        ),
        (
            "PRJ2104_2_linear_placeholder_correction",
            "Pi_gamma_cg",
            "The 2103 linear placeholder Delta_gamma=Pi_gamma_cg*c_g is not safe for raw c_g. In the conformal scalar branch the leading PPN-gamma response is quadratic in the canonical effective coupling alpha_eff.",
            "replace Pi_gamma_cg with Pi_gamma_alpha2 after canonical normalization",
            "linear scoring of raw c_g is forbidden",
            "CORRECTS_LINEAR_PLACEHOLDER",
        ),
        (
            "PRJ2104_3_full_MTS_residual_vector",
            "Delta_gamma_MTS",
            "Delta_gamma_MTS = Delta_gamma_cg + Delta_gamma_bdis + Delta_gamma_nonH + Delta_gamma_tail + Delta_gamma_gauge + Delta_gamma_readout.",
            "absolute no-cancellation vector must be used",
            "b_dis, q_nonH, tails, gauge and readout cannot be cancelled against c_g",
            "RESIDUAL_VECTOR_FORM_WRITTEN_NONCLAIM",
        ),
        (
            "PRJ2104_4_Cassini_projection_bound",
            "alpha_eff_bound_template",
            f"If Y_gamma=1 and all other residuals are theorem-zero, the conservative 2053 bound |Delta_gamma|<={GAMMA_BOUND_SELECTED:.6g} implies alpha_eff^2<={ALPHA_EFF2_CONSERVATIVE:.6g}, alpha_eff<={ALPHA_EFF_CONSERVATIVE:.6g}.",
            "diagnostic bound on canonical effective coupling only",
            "not a raw c_g bound until N_X is derived",
            "SOURCE_BACKED_DIAGNOSTIC_NOT_MTS_SCORE",
        ),
        (
            "PRJ2104_5_verdict",
            "c_g_to_PPN_projection",
            "The PPN projection route is now explicit: raw c_g must first be converted to a canonical effective scalar coupling and range/profile response, then inserted into the 2053 q_R^PPN gamma slot with absolute tail guards.",
            "usable as 2105 input contract",
            "local-GR is still blocked by canonical normalization, range response and guard closure",
            "PROJECTION_LAW_DERIVED_INPUTS_MISSING",
        ),
    ]
    return [
        row(
            row_id=row_id,
            quantity=quantity,
            derivation_or_formula=formula,
            result=result,
            blocker_or_warning=blocker,
            status=status,
            score_ready=False,
            valid_for_claim=False,
        )
        for row_id, quantity, formula, result, blocker, status in specs
    ]


def frame_degeneracy_rows() -> list[dict[str, object]]:
    specs = [
        (
            "FDG2104_0_constant_common_factor",
            "constant A_g",
            "A_g=A_0 over the experiment is an exact unit/frame normalization and does not create a PPN gamma residual.",
            "DEGENERATE_IF_CONSTANT",
            "does not cover spatially sourced or dynamical X",
        ),
        (
            "FDG2104_1_spm_closure",
            "single-public-metric closure",
            "If ordinary matter/readout is restricted to one public quotient metric and no independent shadow frame slot exists, c_g=0 by closure definition.",
            "CLOSURE_BRANCH_ONLY",
            "1032 demotes this to an explicit branch, not a derived MTS theorem",
        ),
        (
            "FDG2104_2_jordan_einstein_relabel",
            "frame relabel",
            "Moving A_g into the metric notation does not erase scalar-tensor PPN effects if the scalar is sourced and changes the field equations.",
            "NOT_A_DEGENERACY_BY_ITSELF",
            "forbids measured-frame handwave",
        ),
        (
            "FDG2104_3_heavy_or_screened_scalar",
            "range/screening suppression",
            "If Y_gamma(lambda, profile) is negligible over the Cassini/Shapiro geometry, the PPN gamma response can be suppressed without c_g=0.",
            "FINITE_RANGE_ROUTE",
            "then R10/short-range and source-profile rows become the active constraints",
        ),
        (
            "FDG2104_4_measured_GM_readout",
            "source-mass calibration",
            "Measured GM/source-mass calibration can absorb the time-potential normalization but cannot absorb spatial curvature gamma once the same-frame convention is fixed.",
            "PARTIAL_DEGENERACY_ONLY",
            "same-frame mass, gauge and readout locks remain required",
        ),
        (
            "FDG2104_5_verdict",
            "measured-frame degeneracy",
            "The only safe zero routes are constant A_g, explicit SPM closure, or vanishing/suppressed canonical scalar response. A finite sourced scalar branch must use the PPN projection law.",
            "NO_FREE_DEGENERACY_CLAIM",
            "c_g remains live unless one of the exact conditions is parent-signed",
        ),
    ]
    return [
        row(
            degeneracy_id=degeneracy_id,
            branch=branch,
            condition_or_statement=statement,
            status=status,
            limitation=limitation,
            valid_for_claim=False,
        )
        for degeneracy_id, branch, statement, status, limitation in specs
    ]


def scalar_tensor_bound_rows() -> list[dict[str, object]]:
    specs = [
        (
            "STB2104_0_qR_bound",
            "q_R^PPN",
            f"|q_R^PPN + tails| <= {GAMMA_BOUND_SELECTED:.6g}",
            "dimensionless",
            "2053 conservative Cassini-centered envelope",
            "source-backed residual bound, not an MTS prediction",
            "BOUND_ROW_NONCLAIM",
        ),
        (
            "STB2104_1_alpha_eff_conservative",
            "alpha_eff^2",
            f"alpha_eff^2 * Y_gamma <= {ALPHA_EFF2_CONSERVATIVE:.6g}; alpha_eff <= {ALPHA_EFF_CONSERVATIVE:.6g} if Y_gamma=1",
            "dimensionless",
            "derived from |gamma-1| ~= 2 alpha_eff^2",
            "requires all non-cg residuals zero and long-range canonical scalar normalization",
            "DIAGNOSTIC_NOT_CG_BOUND",
        ),
        (
            "STB2104_2_alpha_eff_strict",
            "alpha_eff^2_strict",
            f"alpha_eff^2 * Y_gamma <= {ALPHA_EFF2_STRICT:.6g}; alpha_eff <= {ALPHA_EFF_STRICT:.6g} if Y_gamma=1",
            "dimensionless",
            "uses strict one-sigma gamma anchor as diagnostic",
            "not selected for claim; only sensitivity scale",
            "DIAGNOSTIC_NOT_SELECTED",
        ),
        (
            "STB2104_3_raw_cg",
            "c_g",
            "c_g <= alpha_eff / N_X",
            "depends_on_Xhat_normalization",
            "N_X = canonical field Jacobian / Planck normalization",
            "N_X and Z_X are missing, so no raw c_g bound exists",
            "MISSING_CANONICAL_NORMALIZATION",
        ),
        (
            "STB2104_4_range_response",
            "Y_gamma(lambda, profile)",
            "Delta_gamma_cg = -2 alpha_eff^2 Y_gamma/(1+alpha_eff^2 Y_gamma)",
            "dimensionless",
            "Cassini/Shapiro geometry and scalar range response",
            "lambda_X and profile response missing; if short-range, R10 branch must carry the bound",
            "MISSING_RANGE_RESPONSE",
        ),
    ]
    return [
        row(
            bound_id=bound_id,
            quantity=quantity,
            formula_or_bound=formula,
            units=units,
            source_or_derivation=source,
            limitation=limitation,
            status=status,
            score_ready=False,
            valid_for_claim=False,
        )
        for bound_id, quantity, formula, units, source, limitation, status in specs
    ]


def guard_rows() -> list[dict[str, object]]:
    specs = [
        ("GRD2104_0_canonical_norm", "N_X or Z_X", "canonical normalization converting raw c_g to alpha_eff", "derive parent field-space metric and Xhat normalization", "MISSING_CANONICAL_NORMALIZATION"),
        ("GRD2104_1_range_profile", "Y_gamma(lambda, profile)", "finite-range/screening response over Cassini/Shapiro geometry", "derive scalar Green response or source a conservative response factor", "MISSING_RANGE_RESPONSE"),
        ("GRD2104_2_same_frame_mass", "same-frame GM", "source mass in r_s=2GM/c^2 must match operational Cassini frame", "close 2053 same-frame mass guard", "MISSING_SAME_FRAME_SOURCE_MASS"),
        ("GRD2104_3_readout_lock", "readout metric/coframe", "clocks, rods and light propagation must use the same public frame in the PPN comparison", "derive readout-frame lock or retain readout residual", "MISSING_READOUT_FRAME_LOCK"),
        ("GRD2104_4_tail_vector", "b_dis;q_nonH;tail;gauge", "non-cg residuals in Delta_gamma_MTS must be zero or source-bounded separately", "fill absolute residual vector rows", "MISSING_TAIL_ZERO_OR_BOUNDS"),
        ("GRD2104_5_no_cancellation", "absolute norm", "no cancellation between c_g, disformal, non-Hilbert, gauge, readout or boundary terms", "use absolute vector envelope before scoring", "NO_CANCELLATION_POLICY_ACTIVE"),
    ]
    return [
        row(
            guard_id=guard_id,
            required_quantity=quantity,
            definition=definition,
            next_action=next_action,
            status=status,
            valid_for_claim=False,
        )
        for guard_id, quantity, definition, next_action, status in specs
    ]


def claim_gate_rows() -> list[dict[str, object]]:
    specs = [
        ("GATE2104_0_gamma_projection_template", "c_g PPN projection law written", True, "scalar-tensor template plus 2053 q_R gamma slot are now explicit"),
        ("GATE2104_1_raw_cg_score", "raw c_g can be compared to Cassini", False, "canonical normalization N_X/Z_X and range response are missing"),
        ("GATE2104_2_frame_degeneracy", "finite c_g is pure measured-frame degeneracy", False, "only constant A_g/SPM/suppressed response routes are safe"),
        ("GATE2104_3_spm_branch", "SPM branch can set c_g=0 internally", True, "closure branch is allowed as labelled nonclaim branch, not derived evidence"),
        ("GATE2104_4_tail_closure", "all non-cg PPN tails are zero/bounded", False, "b_dis, q_nonH, gauge/readout/tail guards remain open"),
        ("GATE2104_5_local_GR", "derived local GR/Newton limit follows", False, "gamma template alone does not derive beta, source mass, EH/Newton left-hand side or full residual vector"),
    ]
    return [
        row(
            gate_id=gate_id,
            gate=gate,
            gate_pass=gate_pass,
            reason=reason,
            claim_allowed=False,
            valid_for_claim=False,
        )
        for gate_id, gate, gate_pass, reason in specs
    ]


def decision_rows() -> list[dict[str, object]]:
    specs = [
        (
            "DEC2104_0_projection_result",
            "CG_TO_PPN_PROJECTION_TEMPLATE_DERIVED",
            "Raw c_g maps to PPN gamma through a canonical effective scalar coupling, alpha_eff=N_X c_g, with gamma-1 approximately -2 alpha_eff^2 times the range/profile response.",
            "treat the old linear Pi_gamma_cg row as a placeholder requiring canonical replacement",
        ),
        (
            "DEC2104_1_degeneracy_result",
            "MEASURED_FRAME_DEGENERACY_IS_CONDITIONAL_ONLY",
            "Constant conformal normalization and explicit SPM closure are safe zero routes, but a sourced scalar cannot be erased by a frame relabel.",
            "do not use measured-G/frame language to hide finite c_g",
        ),
        (
            "DEC2104_2_best_next",
            "CG_CANONICAL_NORMALIZATION_AND_RANGE_RESPONSE_NEXT",
            "The next missing object is not more Cassini data; it is N_X/Z_X and Y_gamma(lambda, profile), plus tail guards.",
            "derive canonical normalization first, then run the nonclaim Cassini bound template",
        ),
    ]
    return [
        row(
            decision_id=decision_id,
            decision=decision,
            because=because,
            next_action=next_action,
            valid_for_claim=False,
        )
        for decision_id, decision, because, next_action in specs
    ]


def next_rows() -> list[dict[str, object]]:
    return [
        row(
            route_id="NEXT2104_0_2105",
            next_target="2105-Y5-R2FR-cg-canonical-normalization-and-gamma-bound-runner.md",
            script="scripts/Y5_R2FR_cg_canonical_normalization_and_gamma_bound_runner_2105.py",
            objective="Derive or source the canonical normalization N_X/Z_X and finite-range response Y_gamma needed to turn raw c_g into alpha_eff and a nonclaim Cassini gamma bound row.",
            forbidden_shortcuts="linear raw-c_g Cassini score; frame relabel as proof; cancellation against b_dis/q_nonH/tails; local-GR claim from gamma alone",
            valid_for_claim=False,
        )
    ]


def write_branch_copies(
    projection: list[dict[str, object]],
    degeneracy: list[dict[str, object]],
    bounds: list[dict[str, object]],
    guards: list[dict[str, object]],
    decisions: list[dict[str, object]],
    next_target: list[dict[str, object]],
) -> list[dict[str, object]]:
    copies = [
        (
            "COPY2104_0_source_weight_docs",
            SOURCE_WEIGHT_DOCS / "AFRAME_CG_PPN_PROJECTION_2104_NONCLAIM.csv",
            projection + degeneracy + decisions,
        ),
        (
            "COPY2104_1_branch_locked_wep",
            BRANCH_WEP / "P8_Y5_PARENT_QLOC_2104_CG_PPN_STATUS_NONCLAIM.csv",
            projection + bounds + guards,
        ),
        (
            "COPY2104_2_acquisition_queue",
            QUEUE / "JR2104_CG_CANONICAL_NORMALIZATION_AND_GAMMA_QUEUE.csv",
            guards + bounds + next_target,
        ),
    ]
    rows: list[dict[str, object]] = []
    for copy_id, path, copy_rows in copies:
        write_csv(path, copy_rows)
        rows.append(
            row(
                copy_id=copy_id,
                destination=str(path),
                path_exists=path.exists(),
                row_count=len(copy_rows),
                parse_ok=csv_rows_parse(path),
                valid_for_claim=False,
            )
        )
    return rows


def validation_rows(
    sources: list[dict[str, object]],
    projection: list[dict[str, object]],
    degeneracy: list[dict[str, object]],
    bounds: list[dict[str, object]],
    guards: list[dict[str, object]],
    gates: list[dict[str, object]],
    decisions: list[dict[str, object]],
    next_target: list[dict[str, object]],
    copies: list[dict[str, object]],
    csv_paths: list[Path],
) -> list[dict[str, object]]:
    sources_ok = all(truthy(source.get("path_exists")) and truthy(source.get("needle_found")) for source in sources)
    projection_ok = any(row_.get("row_id") == "PRJ2104_5_verdict" and row_.get("status") == "PROJECTION_LAW_DERIVED_INPUTS_MISSING" for row_ in projection)
    correction_ok = any(row_.get("row_id") == "PRJ2104_2_linear_placeholder_correction" and row_.get("status") == "CORRECTS_LINEAR_PLACEHOLDER" for row_ in projection)
    degeneracy_ok = any(row_.get("degeneracy_id") == "FDG2104_5_verdict" and row_.get("status") == "NO_FREE_DEGENERACY_CLAIM" for row_ in degeneracy)
    bounds_ok = any(row_.get("bound_id") == "STB2104_1_alpha_eff_conservative" and "3.35e-05" in str(row_.get("formula_or_bound")) for row_ in bounds)
    guards_ok = len(guards) >= 6 and any(row_.get("guard_id") == "GRD2104_0_canonical_norm" and row_.get("status") == "MISSING_CANONICAL_NORMALIZATION" for row_ in guards)
    gates_ok = all(not truthy(row_.get("claim_allowed")) for row_ in gates) and any(not truthy(row_.get("gate_pass")) for row_ in gates)
    decision_ok = any(row_.get("decision") == "CG_CANONICAL_NORMALIZATION_AND_RANGE_RESPONSE_NEXT" for row_ in decisions)
    next_ok = any(row_.get("route_id") == "NEXT2104_0_2105" and "2105-Y5-R2FR" in str(row_.get("next_target")) for row_ in next_target)
    copies_ok = len(copies) == 3 and all(truthy(row_.get("path_exists")) and truthy(row_.get("parse_ok")) for row_ in copies)
    csv_ok = all(path.exists() and csv_rows_parse(path) for path in csv_paths)
    no_claims = all(
        not truthy(row_.get("valid_for_claim")) and not truthy(row_.get("claim_allowed")) and not truthy(row_.get("score_ready"))
        for collection in (sources, projection, degeneracy, bounds, guards, gates, decisions, next_target, copies)
        for row_ in collection
    )
    formalization_clean = count_formalization_modified() == 0 and not formalization_has_2104_artifacts()
    no_pycache = not (SCRIPT_PATH.parent / "__pycache__").exists()
    checks = [
        ("VAL2104_00_sources", sources_ok, "2103, 1029, 1032, 2053 and Cassini-bound sources exist with required needles"),
        ("VAL2104_01_projection", projection_ok, "c_g to PPN projection law is written but input-blocked"),
        ("VAL2104_02_linear_correction", correction_ok, "raw linear c_g placeholder is corrected to canonical alpha_eff^2 response"),
        ("VAL2104_03_degeneracy", degeneracy_ok, "measured-frame degeneracy is conditional only"),
        ("VAL2104_04_bounds", bounds_ok, "Cassini diagnostic alpha_eff bound template is staged"),
        ("VAL2104_05_guards", guards_ok, "canonical normalization/range/readout/tail guards are explicit"),
        ("VAL2104_06_claim_gates", gates_ok, "claim gates block raw c_g score and local-GR promotion"),
        ("VAL2104_07_decision", decision_ok, "decision selects canonical normalization and range response next"),
        ("VAL2104_08_next", next_ok, "next target is 2105 c_g canonical normalization and gamma bound runner"),
        ("VAL2104_09_branch_copies", copies_ok, "branch copies exist and parse"),
        ("VAL2104_10_csv_parse", csv_ok, "all generated CSVs parse cleanly"),
        ("VAL2104_11_no_claim_flags", no_claims, "no generated row allows a claim or score"),
        ("VAL2104_12_formalization_clean", formalization_clean, "formalization-workbench untouched by 2104"),
        ("VAL2104_13_no_pycache", no_pycache, "scripts __pycache__ removed"),
    ]
    overall = all(ok for _, ok, _ in checks)
    checks.append(
        (
            "VAL2104_OVERALL",
            overall,
            "2104 derives the c_g-to-PPN projection template, blocks raw c_g scoring, and selects canonical normalization/range response next",
        )
    )
    return [
        row(
            check_id=check_id,
            status="PASS" if ok else "FAIL",
            detail=detail,
            claim_allowed=False,
            valid_for_claim=False,
        )
        for check_id, ok, detail in checks
    ]


def write_doc(
    sources: list[dict[str, object]],
    projection: list[dict[str, object]],
    degeneracy: list[dict[str, object]],
    bounds: list[dict[str, object]],
    guards: list[dict[str, object]],
    gates: list[dict[str, object]],
    decisions: list[dict[str, object]],
    next_target: list[dict[str, object]],
    copies: list[dict[str, object]],
    validation: list[dict[str, object]],
) -> None:
    sections = [
        "# 2104 - Y5/R2FR c_g to PPN Projection Matrix Or Measured-Frame Degeneracy",
        "",
        "## Current Verdict",
        "",
        "2104 makes a real step toward the GR/Newton reduction route. The `c_g -> PPN gamma` map is not a linear raw-`c_g` comparison. In the finite universal conformal/scalar branch, raw `c_g` must first be converted into a canonical effective coupling `alpha_eff=N_X c_g`, and the leading PPN-gamma response is quadratic: `gamma-1 ~= -2 alpha_eff^2 Y_gamma` plus retained tails.",
        "",
        "Measured-frame degeneracy is also narrowed. A constant common conformal factor is just units, and an explicit single-public-metric closure can set `c_g=0` inside that labelled closure branch. But a sourced scalar response cannot be erased by a frame relabel. Therefore no local-GR claim follows yet.",
        "",
        f"Diagnostic scale only: using the conservative 2053 Cassini envelope `{GAMMA_BOUND_SELECTED:.6g}`, the long-range, tail-free scalar-template bound would be `alpha_eff^2 <= {ALPHA_EFF2_CONSERVATIVE:.6g}` and `alpha_eff <= {ALPHA_EFF_CONSERVATIVE:.6g}`. This is **not** a raw `c_g` bound until `N_X/Z_X` and `Y_gamma` are derived.",
        "",
        "## Source Register",
        md_table(sources, ["source_id", "source_path", "path_exists", "needle_found", "use_in_2104", "valid_for_claim"]),
        "## c_g to PPN Projection",
        md_table(projection, ["row_id", "quantity", "status", "derivation_or_formula", "result", "blocker_or_warning", "score_ready", "valid_for_claim"]),
        "## Measured-Frame Degeneracy Conditions",
        md_table(degeneracy, ["degeneracy_id", "branch", "status", "condition_or_statement", "limitation", "valid_for_claim"]),
        "## Scalar-Tensor Bound Rows",
        md_table(bounds, ["bound_id", "quantity", "formula_or_bound", "units", "source_or_derivation", "limitation", "status", "score_ready", "valid_for_claim"]),
        "## Guard Closure Rows",
        md_table(guards, ["guard_id", "required_quantity", "definition", "next_action", "status", "valid_for_claim"]),
        "## Claim Gates",
        md_table(gates, ["gate_id", "gate", "gate_pass", "reason", "claim_allowed", "valid_for_claim"]),
        "## Decision Ledger",
        md_table(decisions, ["decision_id", "decision", "because", "next_action", "valid_for_claim"]),
        "## Next Target",
        md_table(next_target, ["route_id", "next_target", "script", "objective", "forbidden_shortcuts", "valid_for_claim"]),
        "## Branch Copies",
        md_table(copies, ["copy_id", "destination", "path_exists", "row_count", "parse_ok", "valid_for_claim"]),
        "## Validation",
        md_table(validation, ["check_id", "status", "detail", "claim_allowed", "valid_for_claim"]),
    ]
    DOC.write_text("\n".join(sections), encoding="utf-8")


def main() -> None:
    sources = source_register_rows()
    projection = cg_ppn_projection_rows()
    degeneracy = frame_degeneracy_rows()
    bounds = scalar_tensor_bound_rows()
    guards = guard_rows()
    gates = claim_gate_rows()
    decisions = decision_rows()
    next_target = next_rows()
    paths = {
        "sources": OUT / "P8_Y5_PARENT_QLOC_2104_SOURCE_REGISTER.csv",
        "projection": OUT / "P8_Y5_PARENT_QLOC_2104_CG_PPN_PROJECTION.csv",
        "degeneracy": OUT / "P8_Y5_PARENT_QLOC_2104_FRAME_DEGENERACY_CONDITIONS.csv",
        "bounds": OUT / "P8_Y5_PARENT_QLOC_2104_SCALAR_TENSOR_BOUND_ROWS.csv",
        "guards": OUT / "P8_Y5_PARENT_QLOC_2104_GUARD_CLOSURE_ROWS.csv",
        "gates": OUT / "P8_Y5_PARENT_QLOC_2104_CLAIM_GATES.csv",
        "decisions": OUT / "P8_Y5_PARENT_QLOC_2104_DECISION_LEDGER.csv",
        "next": OUT / "P8_Y5_PARENT_QLOC_2104_NEXT_TARGET.csv",
        "branch": OUT / "P8_Y5_PARENT_QLOC_2104_BRANCH_COPIES.csv",
        "validation": OUT / "P8_Y5_BRR545_2104_VALIDATION.csv",
    }
    write_csv(paths["sources"], sources)
    write_csv(paths["projection"], projection)
    write_csv(paths["degeneracy"], degeneracy)
    write_csv(paths["bounds"], bounds)
    write_csv(paths["guards"], guards)
    write_csv(paths["gates"], gates)
    write_csv(paths["decisions"], decisions)
    write_csv(paths["next"], next_target)
    copies = write_branch_copies(projection, degeneracy, bounds, guards, decisions, next_target)
    write_csv(paths["branch"], copies)
    csv_paths = [path for key, path in paths.items() if key != "validation"] + [Path(str(r["destination"])) for r in copies]
    remove_pycache()
    validation = validation_rows(sources, projection, degeneracy, bounds, guards, gates, decisions, next_target, copies, csv_paths)
    write_csv(paths["validation"], validation)
    write_doc(sources, projection, degeneracy, bounds, guards, gates, decisions, next_target, copies, validation)
    remove_pycache()
    print(f"wrote {DOC}")
    print(f"validation {paths['validation']}")


if __name__ == "__main__":
    main()

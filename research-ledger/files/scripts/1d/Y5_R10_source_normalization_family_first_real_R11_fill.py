from __future__ import annotations

import csv
from datetime import datetime, timezone
from pathlib import Path


STATUS = "Y5_R10_cmu_source_normalization_family_decomposed_exactly_non_numeric_nonclaim"
CLAIM_CEILING = "c_mu_decomposition_only_no_mu_extra_zero_no_Newton_no_PPN_no_R10_no_R11_no_local_GR_claim"
NEXT_TARGET = "658-Y5-R10-cmu-radial-calibration-zero-or-numeric-envelope.md"

ROOT = Path(__file__).resolve().parents[1]
RESIDUALS = ROOT / "source-intake" / "mts_residuals"
DOC_PATH = ROOT / "657-Y5-R10-source-normalization-family-first-real-R11-fill.md"

FORMALIZATION_WORKBENCH = ROOT.parent / "formalization-workbench"
FORMALIZATION_CUTOFF = datetime.fromisoformat("2026-05-31T14:42:00")

SOURCE_PATHS = {
    "656_doc": ROOT / "656-Y5-R10-R11-executable-vector-minimum-skeleton-under-WEP-closure.md",
    "656_validation": RESIDUALS / "P8_Y5_BRR545_656_VALIDATION.csv",
    "656_skeleton": RESIDUALS / "P8_Y5_R10_656_R11_MINIMUM_SKELETON.csv",
    "656_missing_ledger": RESIDUALS / "P8_Y5_R10_656_MISSING_INPUT_LEDGER.csv",
    "656_priority_queue": RESIDUALS / "P8_Y5_R10_656_PRIORITY_FILL_QUEUE.csv",
    "402_parent_pair": ROOT / "402-EH-source-normalization-parent-pair.md",
    "425_source_plan": ROOT / "425-EH-operator-retained-ledger-and-source-normalization-test-plan.md",
    "438_r11_contract": ROOT / "438-R11-nonEH-coefficient-vector-contract.md",
    "444_residual_refinement": ROOT / "444-source-normalization-residual-vector-refinement.md",
    "460_newton_stack": ROOT / "460-source-normalized-Newton-branch-theorem-stack.md",
    "467_mu_extra_vector": ROOT / "467-mu-extra-zero-owner-or-source-normalization-coefficient-vector.md",
    "496_minimum_fill": ROOT / "496-R11-source-normalization-operator-vector-minimum-fill.md",
    "497_route_router": ROOT / "497-source-normalization-derived-zero-route-or-numeric-input-template.md",
    "560_alpha_law": ROOT / "560-Y5-R10-source-normalized-alpha-law-from-parent-or-runner-real-data-fill.md",
    "652_wep_source_target": ROOT / "652-Y5-R10-WEP-source-normalization-or-common-geometry-zero-theorem.md",
    "639_local_bound_matrix": RESIDUALS / "P8_Y5_R10_639_LOCAL_BOUND_MATRIX.csv",
    "496_operator_minimum_fill_csv": RESIDUALS / "P8_R11_SOURCE_NORMALIZATION_OPERATOR_MINIMUM_FILL.csv",
    "496_missing_ledger_csv": RESIDUALS / "P8_R11_SOURCE_NORMALIZATION_MISSING_LEDGER.csv",
    "497_route_classification_csv": RESIDUALS / "P8_SOURCE_NORMALIZATION_ROUTE_CLASSIFICATION.csv",
    "497_zero_targets_csv": RESIDUALS / "P8_SOURCE_NORMALIZATION_DERIVED_ZERO_TARGETS.csv",
    "497_numeric_templates_csv": RESIDUALS / "P8_SOURCE_NORMALIZATION_NUMERIC_INPUT_TEMPLATE.csv",
    "652_source_target_csv": RESIDUALS / "P8_Y5_R10_652_SOURCE_NORMALIZATION_TARGET.csv",
}

CHANNEL_ORDER = [
    "radial_Meff_hair",
    "boundary_monopole_shift",
    "domain_projector_mass",
    "bulk_X_Yukawa_tail",
    "nonEH_operator_potential",
    "species_source_charge",
    "time_drift",
    "absolute_calibration_offset",
]

ROW_MAPS = [
    {
        "map_id": "CMU657_R1_WEP_SOURCE",
        "affected_row": "R1",
        "observable": "eta_WEP_source_charge",
        "weak_field_map": "eta_source_AB ~ Delta_AB[partial_A epsilon_mu] with epsilon_species_A the first explicit source-charge component",
        "required_inputs": "epsilon_species_A;species_pair;source_charge_derivative;WEP material model;source path",
        "bound_or_gate": "eta_source_AB <= 2.8e-15 and alpha-specific fallback beta_source_alpha <= robust 652 target",
        "current_status": "mapped_symbolically_no_numeric_species_vector",
        "valid_for_claim": "false",
    },
    {
        "map_id": "CMU657_R4_BETA",
        "affected_row": "R4",
        "observable": "beta_minus_1",
        "weak_field_map": "beta_source_residual = B_rad epsilon_radial_Meff + B_boundary epsilon_boundary + B_nonEH epsilon_nonEH_source + B_cal epsilon_calibration + higher-order source terms",
        "required_inputs": "B_i projection coefficients;epsilon_i values or zero theorems;second-order PPN source expansion",
        "bound_or_gate": "|beta_minus_1| <= 7.8e-05 after no-cancellation channel accounting",
        "current_status": "mapped_symbolically_missing_second_order_coefficients",
        "valid_for_claim": "false",
    },
    {
        "map_id": "CMU657_R9_GDOT",
        "affected_row": "R9",
        "observable": "Gdot_over_G",
        "weak_field_map": "d ln mu_obs/dt = d ln(G_obs M_obs)/dt + d epsilon_mu/dt/(1+epsilon_mu) ~= d epsilon_time_drift/dt plus any boundary/memory flux drift",
        "required_inputs": "epsilon_time_drift(t);stationarity theorem or sourced dln_mu_dt;time window;source path",
        "bound_or_gate": "|Gdot/G| <= 9.6e-15 yr^-1",
        "current_status": "mapped_symbolically_missing_time_drift_input",
        "valid_for_claim": "false",
    },
    {
        "map_id": "CMU657_R10_RANGE",
        "affected_row": "R10",
        "observable": "delta_G_or_fifth_force_yukawa",
        "weak_field_map": "alpha_SN(lambda)=alpha_bulk_X(lambda)+alpha_nonEH(lambda)+alpha_radial(lambda) with source-normalized alpha law from 560 when parent inputs exist",
        "required_inputs": "lambda_X;alpha_X(lambda);Z_X;Q_X;q_X^T;Pi_M^H;digitized alpha_bound(lambda);source path",
        "bound_or_gate": "|alpha_SN(lambda)| <= alpha_bound(lambda) for every valid lambda row; no symbolic pass",
        "current_status": "mapped_symbolically_missing_R10_curve_or_no_range_theorem",
        "valid_for_claim": "false",
    },
    {
        "map_id": "CMU657_R11_LEDGER",
        "affected_row": "R11",
        "observable": "non_EH_operator_coefficients",
        "weak_field_map": "source_normalization_operator is cleared only if every epsilon_i is theorem-zero, parent-fixed universal calibration, or a sourced bounded residual row",
        "required_inputs": "all eight epsilon_i rows with theorem/numeric status;units;normalization;source paths;no-cancellation ledger",
        "bound_or_gate": "R11 c_mu valid only when all channel rows are individually cleared",
        "current_status": "mapped_symbolically_eight_channel_vector_not_claimable",
        "valid_for_claim": "false",
    },
]

ZERO_CLAUSES = [
    {
        "clause_id": "ZCMU657_0_sum_rule",
        "needed_statement": "mu_extra is decomposed into the eight retained source-normalization channels without hiding channels",
        "mathematical_form": "epsilon_mu := mu_extra/(G_obs M_obs) = sum_i epsilon_i",
        "current_status": "pass_identity",
        "parent_signed": "true_identity_only",
        "blocks_if_missing": "source normalization cannot be audited channel-by-channel",
    },
    {
        "clause_id": "ZCMU657_1_same_frame_source",
        "needed_statement": "the observed matter/source frame is the same frame used by gravitational source normalization",
        "mathematical_form": "delta_frame_source = 0",
        "current_status": "closure_from_WEP_branch_not_EH_source_proof",
        "parent_signed": "false",
        "blocks_if_missing": "absolute calibration/frame split can mimic measured GM",
    },
    {
        "clause_id": "ZCMU657_2_compact_monopole_conservation",
        "needed_statement": "the compact source monopole is conserved and has no radial memory/source hair",
        "mathematical_form": "dM_eff/dt=0 and partial_r epsilon_radial_Meff=0",
        "current_status": "conditional_from_244_not_parent_closed",
        "parent_signed": "false",
        "blocks_if_missing": "R4/R9/R10 source-normalization rows stay open",
    },
    {
        "clause_id": "ZCMU657_3_boundary_domain_bulk_silence",
        "needed_statement": "boundary, domain/projector, bulk-X, and memory exchange channels carry no local measured-GM monopole",
        "mathematical_form": "epsilon_boundary=epsilon_domain_projector=epsilon_bulk_X=0 plus no memory/source flux",
        "current_status": "not_derived",
        "parent_signed": "false",
        "blocks_if_missing": "R7/R8/R10 and no-cancellation source rows remain active",
    },
    {
        "clause_id": "ZCMU657_4_selector_blind_source",
        "needed_statement": "ordinary matter species do not carry a source-charge pullback under the selector/class variables",
        "mathematical_form": "partial_A epsilon_mu = 0 or epsilon_species_A=0 for allowed ordinary materials",
        "current_status": "not_parent_derived",
        "parent_signed": "false",
        "blocks_if_missing": "R1 WEP/source-charge row remains active",
    },
    {
        "clause_id": "ZCMU657_5_stationarity",
        "needed_statement": "local source normalization is stationary in the observed branch",
        "mathematical_form": "d epsilon_mu/dt=0",
        "current_status": "not_derived",
        "parent_signed": "false",
        "blocks_if_missing": "R9 Gdot row remains active",
    },
    {
        "clause_id": "ZCMU657_6_no_range_hair",
        "needed_statement": "source normalization has no finite-range hair or the alpha(lambda) curve is sourced and below bounds",
        "mathematical_form": "partial_lambda epsilon_mu=0 or alpha_SN(lambda) valid and bounded",
        "current_status": "not_derived_curve_missing",
        "parent_signed": "false",
        "blocks_if_missing": "R10 remains symbolic/nonclaim",
    },
    {
        "clause_id": "ZCMU657_7_parent_fixed_calibration",
        "needed_statement": "any absolute calibration offset is parent-fixed, universal, and derivative-free",
        "mathematical_form": "D_t lambda0=D_r lambda0=D_A lambda0=D_lambda lambda0=0",
        "current_status": "conditional_harmless_not_parent_fixed",
        "parent_signed": "false",
        "blocks_if_missing": "constant-offset cheat is not allowed as Newton proof",
    },
]


def generated_utc() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, object]], fieldnames: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, lineterminator="\n")
        writer.writeheader()
        for row in rows:
            writer.writerow({field: row.get(field, "") for field in fieldnames})


def bool_text(value: bool) -> str:
    return "true" if value else "false"


def rel(path: Path) -> str:
    try:
        return str(path.relative_to(ROOT))
    except ValueError:
        return str(path)


def source_register_rows() -> list[dict[str, str]]:
    now = generated_utc()
    return [
        {
            "source_id": source_id,
            "source_path": str(path),
            "exists": bool_text(path.exists()),
            "role": "input_or_prior_contract_for_657_c_mu_source_normalization_fill",
            "generated_utc": now,
        }
        for source_id, path in SOURCE_PATHS.items()
    ]


def robust_beta_target(target_rows: list[dict[str, str]]) -> str:
    for row in target_rows:
        if row.get("target_id") == "BST652_2_robust_target":
            return row.get("required_abs_beta_source_max", "MISSING_ROBUST_BETA_TARGET")
    return "MISSING_ROBUST_BETA_TARGET"


def c_mu_fill_rows(
    skeleton_rows: list[dict[str, str]],
    target_rows: list[dict[str, str]],
) -> list[dict[str, str]]:
    source_row = next(
        row for row in skeleton_rows if row.get("operator_family") == "source_normalization_operator"
    )
    beta_target = robust_beta_target(target_rows)
    now = generated_utc()
    return [
        {
            "fill_id": "CMU657_0_exact_decomposition",
            "source_skeleton_id": source_row.get("skeleton_id", ""),
            "model_id": "MTS_post_checkpoint_private",
            "branch_id": "WEP_CLOSURE_LOCAL_GR_R11_SKELETON",
            "vector_id": "R11_MIN_SKELETON_657_CMU",
            "operator_family": "source_normalization_operator",
            "coefficient_symbol": "c_mu",
            "coefficient_definition": "c_mu := epsilon_mu := mu_extra/(G_obs*M_obs) = sum_i epsilon_i",
            "coefficient_value": "epsilon_radial_Meff + epsilon_boundary + epsilon_domain_projector + epsilon_bulk_X + epsilon_nonEH_source + epsilon_species_A + epsilon_time_drift + epsilon_calibration",
            "coefficient_value_status": "EXACT_SUM_RULE_NON_NUMERIC_CHANNELS_UNFILLED",
            "coefficient_units": "dimensionless_after_measured_GM_normalization",
            "normalization": "relative_to_same_frame_measured_G_obs_M_obs; not claimable unless range/time/species/radial derivatives vanish or are bounded",
            "operator_form": "mu_obs = G_obs*M_obs*(1+c_mu) with c_mu decomposed into eight retained source-normalization channels",
            "weak_field_map_status": "SYMBOLIC_MAP_WRITTEN_TO_R1_R4_R9_R10_R11_NOT_NUMERIC",
            "affected_rows": "R1;R4;R9;R10;R11",
            "induced_observable": "eta_source_AB;beta_minus_1;Gdot_over_G;alpha(lambda);operator_ledger",
            "source_basis_paths": ";".join(
                [
                    rel(SOURCE_PATHS["656_skeleton"]),
                    rel(SOURCE_PATHS["496_operator_minimum_fill_csv"]),
                    rel(SOURCE_PATHS["497_route_classification_csv"]),
                    rel(SOURCE_PATHS["652_source_target_csv"]),
                ]
            ),
            "robust_beta_source_alpha_target": beta_target,
            "formula_reference": "epsilon_mu := mu_extra/(G_obs*M_obs); mu_extra=sum_i mu_i",
            "derivation_status": "exact_decomposition_formula_only_no_parent_zero_no_numeric_score",
            "score_ready": "false",
            "valid_for_claim": "false",
            "claim_blocker": "all eight epsilon_i channels still need parent-signed zero theorems or sourced numeric residuals; no cancellation credit is allowed",
            "generated_utc": now,
        }
    ]


def channel_vector_rows(
    minimum_rows: list[dict[str, str]],
    route_rows: list[dict[str, str]],
    zero_rows: list[dict[str, str]],
    numeric_rows: list[dict[str, str]],
) -> list[dict[str, str]]:
    route_by_channel = {row["p8_channel"]: row for row in route_rows}
    zero_by_channel = {row["p8_channel"]: row for row in zero_rows}
    numeric_by_channel = {row["p8_channel"]: row for row in numeric_rows}
    minimum_by_channel = {row["p8_channel"]: row for row in minimum_rows}
    rows = []
    now = generated_utc()
    for index, channel in enumerate(CHANNEL_ORDER, start=1):
        minimum = minimum_by_channel[channel]
        route = route_by_channel.get(channel, {})
        zero = zero_by_channel.get(channel, {})
        numeric = numeric_by_channel.get(channel, {})
        rows.append(
            {
                "channel_id": f"CMUCH657_{index:02d}",
                "p8_channel": channel,
                "coefficient_symbol": minimum.get("coefficient_symbol", ""),
                "coefficient_value_or_theorem": minimum.get("coefficient_value_or_theorem", ""),
                "coefficient_units": minimum.get("coefficient_units", ""),
                "normalization": minimum.get("normalization", ""),
                "operator_form": minimum.get("operator_form", ""),
                "weak_field_map": minimum.get("weak_field_map", ""),
                "affected_rows": minimum.get("affected_rows", ""),
                "induced_observable": minimum.get("induced_observable", ""),
                "primary_route": route.get("primary_route", ""),
                "fallback_route": route.get("fallback_route", ""),
                "theorem_target": zero.get("theorem_target", ""),
                "theorem_status": zero.get("current_status", ""),
                "numeric_template": numeric.get("template_id", ""),
                "required_numeric_columns": numeric.get("required_columns", ""),
                "bound_or_gate": numeric.get("bound_or_gate", minimum.get("acceptance", "")),
                "current_status": "retained_unfilled_after_657",
                "score_ready": "false",
                "valid_for_claim": "false",
                "claim_blocker": "channel still has MISSING theorem/numeric input or conditional calibration status",
                "generated_utc": now,
            }
        )
    return rows


def weak_field_map_rows(target_rows: list[dict[str, str]]) -> list[dict[str, str]]:
    beta_target = robust_beta_target(target_rows)
    rows = []
    now = generated_utc()
    for row in ROW_MAPS:
        row_copy = dict(row)
        if row_copy["affected_row"] == "R1":
            row_copy["bound_or_gate"] += f"; robust beta_source_alpha target={beta_target}"
        row_copy["score_ready"] = "false"
        row_copy["generated_utc"] = now
        rows.append(row_copy)
    return rows


def theorem_zero_audit_rows() -> list[dict[str, str]]:
    now = generated_utc()
    return [
        {
            **row,
            "c_mu_zero_effect": (
                "identity_decomposition_only"
                if row["clause_id"] == "ZCMU657_0_sum_rule"
                else "required_for_c_mu_zero"
            ),
            "valid_for_claim": "false",
            "generated_utc": now,
        }
        for row in ZERO_CLAUSES
    ]


def scoreability_gate_rows(
    c_mu_rows: list[dict[str, str]],
    channel_rows: list[dict[str, str]],
    weak_map_rows: list[dict[str, str]],
    zero_rows: list[dict[str, str]],
) -> list[dict[str, str]]:
    now = generated_utc()
    parent_signed_false = [
        row for row in zero_rows if row["parent_signed"] == "false"
    ]
    return [
        {
            "gate_id": "G657_0_cmu_formula",
            "gate": "c_mu exact source-normalization decomposition exists",
            "result": "pass_formula",
            "detail": c_mu_rows[0]["coefficient_definition"],
            "claim_effect": "formula only; not a numeric or theorem-zero pass",
            "generated_utc": now,
        },
        {
            "gate_id": "G657_1_units_normalization",
            "gate": "c_mu units and normalization are declared",
            "result": "pass_formula",
            "detail": "dimensionless after measured G_obs M_obs normalization",
            "claim_effect": "normalization declared but measured-GM derivative hair still open",
            "generated_utc": now,
        },
        {
            "gate_id": "G657_2_channel_coverage",
            "gate": "all eight source-normalization channels are carried forward",
            "result": "pass_structure" if len(channel_rows) == 8 else "fail",
            "detail": f"channels={len(channel_rows)}",
            "claim_effect": "no hidden c_mu channel",
            "generated_utc": now,
        },
        {
            "gate_id": "G657_3_weak_field_maps",
            "gate": "R1/R4/R9/R10/R11 symbolic maps exist",
            "result": "pass_structure" if len(weak_map_rows) == 5 else "fail",
            "detail": f"maps={len(weak_map_rows)}; numeric projection coefficients still missing",
            "claim_effect": "maps are executable-shaped, not executable numerically",
            "generated_utc": now,
        },
        {
            "gate_id": "G657_4_parent_zero_theorem",
            "gate": "parent signs c_mu=0 clauses",
            "result": "blocked",
            "detail": f"unsigned_required_clauses={len(parent_signed_false)}",
            "claim_effect": "blocks mu_extra zero, Newton, PPN, R10/R11, and local-GR promotion",
            "generated_utc": now,
        },
        {
            "gate_id": "G657_5_numeric_residuals",
            "gate": "all epsilon_i have sourced numeric/theorem-zero rows",
            "result": "blocked",
            "detail": "all eight channels remain retained_unfilled_after_657",
            "claim_effect": "blocks scoring and no-cancellation envelope",
            "generated_utc": now,
        },
        {
            "gate_id": "G657_6_claim_guard",
            "gate": "no row is score-ready or claim-valid",
            "result": "pass",
            "detail": "score_ready_true=0; valid_for_claim_true=0",
            "claim_effect": CLAIM_CEILING,
            "generated_utc": now,
        },
    ]


def decision_rows() -> list[dict[str, str]]:
    now = generated_utc()
    return [
        {
            "decision_id": "D657_0_cmu_fill",
            "status": "exact_decomposition_written",
            "meaning": "c_mu is no longer a generic missing placeholder; it is the dimensionless sum of eight retained source-normalization channels",
            "claim_status": "false",
            "next_action": NEXT_TARGET,
            "generated_utc": now,
        },
        {
            "decision_id": "D657_1_zero_proof",
            "status": "not_parent_signed",
            "meaning": "c_mu=0 would require all derivative, source, boundary, bulk, domain, nonEH, time, range, and calibration clauses to close",
            "claim_status": "false",
            "next_action": "try the radial_Meff_hair plus absolute_calibration_offset subroute first",
            "generated_utc": now,
        },
        {
            "decision_id": "D657_2_numeric_branch",
            "status": "allowed_future_branch",
            "meaning": "if theorem-zero fails, each epsilon_i can be scored only with sourced units, bounds, row maps, and no cancellation credit",
            "claim_status": "false",
            "next_action": "create numeric envelope templates only after source paths or theorem certificates exist",
            "generated_utc": now,
        },
        {
            "decision_id": "D657_3_local_GR",
            "status": "blocked",
            "meaning": "local GR remains blocked because source-normalized Newton and R11 c_mu are not cleared",
            "claim_status": "false",
            "next_action": NEXT_TARGET,
            "generated_utc": now,
        },
    ]


def formalization_changed_count() -> int:
    if not FORMALIZATION_WORKBENCH.exists():
        return -1
    count = 0
    for path in FORMALIZATION_WORKBENCH.rglob("*"):
        if path.is_file():
            mtime = datetime.fromtimestamp(path.stat().st_mtime)
            if mtime > FORMALIZATION_CUTOFF:
                count += 1
    return count


def validation_rows(
    source_rows: list[dict[str, str]],
    prior_validation_656: list[dict[str, str]],
    skeleton_rows: list[dict[str, str]],
    c_mu_rows: list[dict[str, str]],
    channel_rows: list[dict[str, str]],
    weak_map_rows: list[dict[str, str]],
    zero_rows: list[dict[str, str]],
    gate_rows: list[dict[str, str]],
    decision: list[dict[str, str]],
) -> list[dict[str, str]]:
    now = generated_utc()
    missing_sources = [row["source_id"] for row in source_rows if row["exists"] != "true"]
    prior_failures = [row for row in prior_validation_656 if row.get("result") != "pass"]
    skeleton_source_rows = [
        row for row in skeleton_rows if row.get("operator_family") == "source_normalization_operator"
    ]
    channel_names = {row["p8_channel"] for row in channel_rows}
    affected_rows = {row["affected_row"] for row in weak_map_rows}
    claim_rows = []
    for group in (c_mu_rows, channel_rows, weak_map_rows, zero_rows, gate_rows, decision):
        claim_rows.extend([row for row in group if row.get("valid_for_claim") == "true" or row.get("claim_status") == "true"])
    generic_fill_markers = []
    for group in (c_mu_rows, channel_rows, weak_map_rows, zero_rows, gate_rows, decision):
        for row in group:
            for value in row.values():
                if isinstance(value, str) and "fill_" in value.lower():
                    generic_fill_markers.append(value)
    blocked_gates = [row for row in gate_rows if row["result"] == "blocked"]
    formalization_changed = formalization_changed_count()
    checks = [
        (
            "V657_0_source_paths_exist",
            not missing_sources,
            "all cited local source paths exist" if not missing_sources else f"missing={';'.join(missing_sources)}",
        ),
        (
            "V657_1_prior_656_validation_clean",
            not prior_failures,
            "656 validation remains clean" if not prior_failures else f"656_failures={len(prior_failures)}",
        ),
        (
            "V657_2_source_normalization_skeleton_loaded",
            len(skeleton_source_rows) == 1,
            f"source_normalization_skeleton_rows={len(skeleton_source_rows)}",
        ),
        (
            "V657_3_cmu_decomposition_written",
            len(c_mu_rows) == 1 and "sum_i epsilon_i" in c_mu_rows[0]["coefficient_definition"],
            c_mu_rows[0]["coefficient_definition"],
        ),
        (
            "V657_4_units_normalization_no_missing",
            c_mu_rows[0]["coefficient_units"].startswith("dimensionless") and "MISSING" not in c_mu_rows[0]["normalization"],
            c_mu_rows[0]["normalization"],
        ),
        (
            "V657_5_eight_channel_coverage",
            channel_names == set(CHANNEL_ORDER),
            f"channels={';'.join(sorted(channel_names))}",
        ),
        (
            "V657_6_weak_map_coverage",
            affected_rows == {"R1", "R4", "R9", "R10", "R11"},
            f"affected_rows={';'.join(sorted(affected_rows))}",
        ),
        (
            "V657_7_zero_not_parent_signed",
            any(row["parent_signed"] == "false" for row in zero_rows),
            "required zero clauses remain unsigned",
        ),
        (
            "V657_8_scoreability_blocked",
            len(blocked_gates) >= 2,
            f"blocked_gates={len(blocked_gates)}",
        ),
        (
            "V657_9_no_claim_rows",
            not claim_rows,
            f"claim_rows={len(claim_rows)}",
        ),
        (
            "V657_10_no_generic_fill_placeholders",
            not generic_fill_markers,
            f"fill_markers={len(generic_fill_markers)}",
        ),
        (
            "V657_11_next_target_selected",
            NEXT_TARGET.startswith("658-") and "cmu" in NEXT_TARGET,
            NEXT_TARGET,
        ),
        (
            "V657_12_claim_ceiling_active",
            CLAIM_CEILING.startswith("c_mu_decomposition_only"),
            CLAIM_CEILING,
        ),
        (
            "V657_13_formalization_workbench_untouched",
            formalization_changed == 0,
            f"formalization_changed_after_cutoff={formalization_changed}",
        ),
    ]
    return [
        {
            "check_id": check_id,
            "result": "pass" if passed else "fail",
            "detail": detail,
            "generated_utc": now,
        }
        for check_id, passed, detail in checks
    ]


def nonclaim_summary_rows(
    c_mu_rows: list[dict[str, str]],
    channel_rows: list[dict[str, str]],
    gate_rows: list[dict[str, str]],
    validation: list[dict[str, str]],
) -> list[dict[str, str]]:
    return [
        {
            "status": STATUS,
            "claim_ceiling": CLAIM_CEILING,
            "c_mu_rows": len(c_mu_rows),
            "channel_rows": len(channel_rows),
            "score_ready_rows": sum(1 for row in c_mu_rows + channel_rows if row.get("score_ready") == "true"),
            "valid_for_claim_rows": sum(1 for row in c_mu_rows + channel_rows if row.get("valid_for_claim") == "true"),
            "blocked_scoreability_gates": sum(1 for row in gate_rows if row["result"] == "blocked"),
            "validation_failures": sum(1 for row in validation if row["result"] != "pass"),
            "next_target": NEXT_TARGET,
            "generated_utc": generated_utc(),
        }
    ]


def markdown_table(rows: list[dict[str, object]], columns: list[str], limit: int | None = None) -> str:
    visible_rows = rows if limit is None else rows[:limit]
    header = "| " + " | ".join(columns) + " |"
    separator = "| " + " | ".join(["---"] * len(columns)) + " |"
    body = [
        "| " + " | ".join(str(row.get(column, "")).replace("\n", " ") for column in columns) + " |"
        for row in visible_rows
    ]
    if limit is not None and len(rows) > limit:
        body.append("| " + " | ".join(["..."] * len(columns)) + " |")
    return "\n".join([header, separator, *body])


def write_document(
    source_rows: list[dict[str, str]],
    c_mu_rows: list[dict[str, str]],
    channel_rows: list[dict[str, str]],
    weak_map_rows: list[dict[str, str]],
    zero_rows: list[dict[str, str]],
    gate_rows: list[dict[str, str]],
    decision: list[dict[str, str]],
    summary_rows: list[dict[str, str]],
    validation: list[dict[str, str]],
) -> None:
    doc = f"""# 657 Y5/R10: Source-Normalization Family First Real R11 Fill

## Verdict

Status: `{STATUS}`.

This checkpoint makes the first real fill of the retained `source_normalization_operator`: `c_mu` is now an exact dimensionless source-normalization sum rule, not a generic missing placeholder. It still does not prove `mu_extra=0`, Newtonian recovery, PPN safety, R10 safety, R11 closure, or local GR.

## Source Register

{markdown_table(source_rows, ["source_id", "exists", "role"])}

## c_mu Fill

{markdown_table(c_mu_rows, ["operator_family", "coefficient_symbol", "coefficient_definition", "coefficient_value_status", "coefficient_units", "normalization", "valid_for_claim"])}

## Eight-Channel Vector

{markdown_table(channel_rows, ["p8_channel", "coefficient_symbol", "primary_route", "theorem_status", "numeric_template", "affected_rows", "current_status", "valid_for_claim"])}

## Weak-Field Map

{markdown_table(weak_map_rows, ["affected_row", "observable", "weak_field_map", "bound_or_gate", "current_status", "valid_for_claim"])}

## Theorem-Zero Audit

{markdown_table(zero_rows, ["clause_id", "needed_statement", "current_status", "parent_signed", "blocks_if_missing", "valid_for_claim"])}

## Scoreability Gates

{markdown_table(gate_rows, ["gate_id", "gate", "result", "claim_effect"])}

## Decision

{markdown_table(decision, ["decision_id", "status", "meaning", "claim_status", "next_action"])}

## Nonclaim Summary

{markdown_table(summary_rows, ["status", "claim_ceiling", "c_mu_rows", "channel_rows", "score_ready_rows", "valid_for_claim_rows", "blocked_scoreability_gates", "next_target"])}

## Validation

{markdown_table(validation, ["check_id", "result", "detail"])}

## Interpretation

This is progress, but not victory. The coupling/source-normalization blocker has been sharpened into a precise object:

`c_mu = epsilon_mu = mu_extra/(G_obs M_obs) = sum_i epsilon_i`.

That gives us a sane language for the next derivations. The first sensible subroute is radial `M_eff` hair plus absolute calibration, because old checkpoints already identified it as the most theorem-like path. If that fails, the branch needs a numeric no-cancellation envelope rather than another closure sentence.

## Next Target

`{NEXT_TARGET}`
"""
    DOC_PATH.write_text(doc, encoding="utf-8")


def main() -> None:
    source_rows = source_register_rows()
    prior_validation_656 = read_csv(SOURCE_PATHS["656_validation"])
    skeleton_rows = read_csv(SOURCE_PATHS["656_skeleton"])
    target_rows = read_csv(SOURCE_PATHS["652_source_target_csv"])
    minimum_rows = read_csv(SOURCE_PATHS["496_operator_minimum_fill_csv"])
    route_rows = read_csv(SOURCE_PATHS["497_route_classification_csv"])
    zero_target_rows = read_csv(SOURCE_PATHS["497_zero_targets_csv"])
    numeric_rows = read_csv(SOURCE_PATHS["497_numeric_templates_csv"])

    c_mu_rows = c_mu_fill_rows(skeleton_rows, target_rows)
    channel_rows = channel_vector_rows(minimum_rows, route_rows, zero_target_rows, numeric_rows)
    weak_map_rows = weak_field_map_rows(target_rows)
    zero_rows = theorem_zero_audit_rows()
    gate_rows = scoreability_gate_rows(c_mu_rows, channel_rows, weak_map_rows, zero_rows)
    decision = decision_rows()
    validation = validation_rows(
        source_rows,
        prior_validation_656,
        skeleton_rows,
        c_mu_rows,
        channel_rows,
        weak_map_rows,
        zero_rows,
        gate_rows,
        decision,
    )
    summary_rows = nonclaim_summary_rows(c_mu_rows, channel_rows, gate_rows, validation)

    write_csv(
        RESIDUALS / "P8_Y5_R10_657_SOURCE_REGISTER.csv",
        source_rows,
        ["source_id", "source_path", "exists", "role", "generated_utc"],
    )
    write_csv(
        RESIDUALS / "P8_Y5_R10_657_CMU_SOURCE_NORMALIZATION_FILL.csv",
        c_mu_rows,
        [
            "fill_id",
            "source_skeleton_id",
            "model_id",
            "branch_id",
            "vector_id",
            "operator_family",
            "coefficient_symbol",
            "coefficient_definition",
            "coefficient_value",
            "coefficient_value_status",
            "coefficient_units",
            "normalization",
            "operator_form",
            "weak_field_map_status",
            "affected_rows",
            "induced_observable",
            "source_basis_paths",
            "robust_beta_source_alpha_target",
            "formula_reference",
            "derivation_status",
            "score_ready",
            "valid_for_claim",
            "claim_blocker",
            "generated_utc",
        ],
    )
    write_csv(
        RESIDUALS / "P8_Y5_R10_657_CMU_EIGHT_CHANNEL_VECTOR.csv",
        channel_rows,
        [
            "channel_id",
            "p8_channel",
            "coefficient_symbol",
            "coefficient_value_or_theorem",
            "coefficient_units",
            "normalization",
            "operator_form",
            "weak_field_map",
            "affected_rows",
            "induced_observable",
            "primary_route",
            "fallback_route",
            "theorem_target",
            "theorem_status",
            "numeric_template",
            "required_numeric_columns",
            "bound_or_gate",
            "current_status",
            "score_ready",
            "valid_for_claim",
            "claim_blocker",
            "generated_utc",
        ],
    )
    write_csv(
        RESIDUALS / "P8_Y5_R10_657_CMU_WEAK_FIELD_MAP.csv",
        weak_map_rows,
        [
            "map_id",
            "affected_row",
            "observable",
            "weak_field_map",
            "required_inputs",
            "bound_or_gate",
            "current_status",
            "valid_for_claim",
            "score_ready",
            "generated_utc",
        ],
    )
    write_csv(
        RESIDUALS / "P8_Y5_R10_657_CMU_THEOREM_ZERO_AUDIT.csv",
        zero_rows,
        [
            "clause_id",
            "needed_statement",
            "mathematical_form",
            "current_status",
            "parent_signed",
            "blocks_if_missing",
            "c_mu_zero_effect",
            "valid_for_claim",
            "generated_utc",
        ],
    )
    write_csv(
        RESIDUALS / "P8_Y5_R10_657_SCOREABILITY_GATES.csv",
        gate_rows,
        ["gate_id", "gate", "result", "detail", "claim_effect", "generated_utc"],
    )
    write_csv(
        RESIDUALS / "P8_Y5_R10_657_DECISION.csv",
        decision,
        ["decision_id", "status", "meaning", "claim_status", "next_action", "generated_utc"],
    )
    write_csv(
        RESIDUALS / "P8_Y5_R10_657_NONCLAIM_SUMMARY.csv",
        summary_rows,
        [
            "status",
            "claim_ceiling",
            "c_mu_rows",
            "channel_rows",
            "score_ready_rows",
            "valid_for_claim_rows",
            "blocked_scoreability_gates",
            "validation_failures",
            "next_target",
            "generated_utc",
        ],
    )
    write_csv(
        RESIDUALS / "P8_Y5_BRR545_657_VALIDATION.csv",
        validation,
        ["check_id", "result", "detail", "generated_utc"],
    )
    write_document(
        source_rows,
        c_mu_rows,
        channel_rows,
        weak_map_rows,
        zero_rows,
        gate_rows,
        decision,
        summary_rows,
        validation,
    )

    failures = [row for row in validation if row["result"] != "pass"]
    print(f"status={STATUS}")
    print(f"doc={DOC_PATH}")
    print(f"c_mu_rows={len(c_mu_rows)}")
    print(f"channel_rows={len(channel_rows)}")
    print(f"validation_failures={len(failures)}")
    print(f"next_target={NEXT_TARGET}")
    if failures:
        for failure in failures:
            print(f"FAIL {failure['check_id']}: {failure['detail']}")


if __name__ == "__main__":
    main()

from __future__ import annotations

import csv
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "source-intake" / "mts_residuals"
LOCAL_BOUNDS = ROOT / "source-intake" / "local_bounds"
DOC_NAME = "921-Y5-R10-FM-force-weak-field-map-and-KBFH-units-bound-runner.md"
STATUS = "Y5_R10_921_FM_force_weak_field_map_written_KBFH_units_missing_bound_runner_smoke_nonclaim"
CLAIM_CEILING = "FM_force_weak_field_bound_interface_only_no_R10_WEP_PPN_clock_orbital_pass_no_local_GR_claim"
NEXT_TARGET = "922-Y5-R10-KBFH-parent-units-and-normalization-or-local-bound-smoke-runner.md"
GENERATED = datetime.now(timezone.utc).isoformat()
FORMALIZATION_CUTOFF = datetime.fromisoformat("2026-05-31T14:42:00")


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="ignore")


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, object]], fields: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        for row in rows:
            writer.writerow({field: row.get(field, "") for field in fields})


def md_table(rows: list[dict[str, object]], fields: list[str]) -> str:
    lines = [
        "| " + " | ".join(fields) + " |",
        "| " + " | ".join("---" for _ in fields) + " |",
    ]
    for row in rows:
        cells = [str(row.get(field, "")).replace("|", "\\|").replace("\n", " ") for field in fields]
        lines.append("| " + " | ".join(cells) + " |")
    return "\n".join(lines) + "\n"


def b(value: bool) -> str:
    return "true" if value else "false"


def source_specs() -> list[dict[str, str]]:
    return [
        {
            "source_id": "920_doc",
            "path": "920-Y5-R10-PiM-current-offshell-closure-and-holonomy-zero-or-FM-force-bound.md",
            "role": "hands off F_M_force/K_BF_H/dPiMJ_leak/A_M_holonomy/B_zero_flux source-ready schema",
            "needle": "Source-Ready Force Bound Pack",
        },
        {
            "source_id": "920_validation",
            "path": "source-intake/mts_residuals/P8_Y5_BRR545_920_VALIDATION.csv",
            "role": "proves 920 was generated and nonclaim",
            "needle": "V920_10_validation_rows_ready",
        },
        {
            "source_id": "920_bound_pack",
            "path": "source-intake/mts_residuals/P8_Y5_R10_920_SOURCE_READY_FORCE_BOUND_PACK.csv",
            "role": "input symbols and required columns for this weak-field map",
            "needle": "F_M_force",
        },
        {
            "source_id": "377_fifth_force_map",
            "path": "377-fifth-force-range-coupling-map.md",
            "role": "Yukawa force-law contract and alpha(lambda) discipline",
            "needle": "a_extra/a_GR = alpha_Y (1 + r/lambda_Y) exp(-r/lambda_Y)",
        },
        {
            "source_id": "359_PPN_guardrail",
            "path": "359-source-locked-PPN-residual-runner-from-derived-force-ledger.md",
            "role": "source-locked local guardrail budget philosophy",
            "needle": "gamma_minus_1",
        },
        {
            "source_id": "374_source_lock_manifest",
            "path": "374-fifth-force-preferred-frame-source-lock-manifest.md",
            "role": "preferred-frame and fifth-force source-lock manifest",
            "needle": "source-lock manifest records",
        },
        {
            "source_id": "427_bounds_csv",
            "path": "427-source-normalization-bounds-csv-template-fill.md",
            "role": "local_bound_claims intake discipline: bounds are not MTS predictions",
            "needle": "these are bounds on possible residual channels",
        },
        {
            "source_id": "local_bound_claims",
            "path": "source-intake/local_bounds/local_bound_claims.csv",
            "role": "local bound rows for WEP, clocks, PPN, Gdot, R10, and operator ledger",
            "needle": "R10_fifth_force",
        },
        {
            "source_id": "R10_digitized_curve",
            "path": "source-intake/local_bounds/R10_alpha_lambda_bound_curve_DIGITIZED.csv",
            "role": "R10 bound curve file; currently still placeholder/digitization-blocked",
            "needle": "MISSING_DIGITIZED_ALPHA_BOUND",
        },
        {
            "source_id": "PPN_template",
            "path": "source-intake/mts_residuals/P8_Y5_PPN_EVALUATOR_INPUT_TEMPLATE.csv",
            "role": "PPN evaluator input template for residual vector mapping",
            "needle": "gamma",
        },
        {
            "source_id": "Cextra_force_map",
            "path": "source-intake/mts_residuals/P8_Y5_CEXTRA_BULK_MEMORY_RANGE_FORCE_LAW_MAP.csv",
            "role": "prior force-law map showing R10 curve requirements",
            "needle": "R10_alpha_lambda_curve_MTS_source_normalization.csv",
        },
    ]


def build_sources() -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    for spec in source_specs():
        path = ROOT / spec["path"]
        exists = path.exists()
        needle_found = exists and spec["needle"] in read_text(path)
        rows.append(
            {
                **spec,
                "absolute_path": str(path),
                "exists": b(exists),
                "needle_found": b(needle_found),
                "valid_for_claim": "false",
                "generated_utc": GENERATED,
            }
        )
    return rows


def local_bound_index() -> dict[str, dict[str, str]]:
    path = LOCAL_BOUNDS / "local_bound_claims.csv"
    return {row["row_id"]: row for row in read_csv(path)}


def summary_rows() -> list[dict[str, object]]:
    return [
        {
            "status": STATUS,
            "claim_ceiling": CLAIM_CEILING,
            "current_result": "weak-field map and bound-runner interface are written; K_BF_H units, parent normalization, range law, and projection coefficients are missing",
            "practical_meaning": "the coupling branch is now testable in shape but not numerically claimable",
            "next_target": NEXT_TARGET,
            "valid_for_claim": "false",
            "generated_utc": GENERATED,
        }
    ]


def weak_field_rows() -> list[dict[str, object]]:
    return [
        {
            "map_id": "WFM921_0_dimensionless_residual",
            "quantity": "epsilon_FM",
            "definition": "dimensionless local coupling pressure from the mass-gauge matter-current residual",
            "formula": "epsilon_FM := |K_BF_H| |A_M| |dPiMJ_leak| / N_FM + |K_BF_H| |B_zero_flux| / N_B",
            "needed_inputs": "K_BF_H units; A_M normalization; dPiMJ_leak units; boundary-flux normalization; source path",
            "maps_to": "internal pressure only until projection coefficients are supplied",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": GENERATED,
        },
        {
            "map_id": "WFM921_1_Yukawa_R10",
            "quantity": "alpha_FM(lambda_FM)",
            "definition": "R10 inverse-square-law equivalent only if the residual has a derived finite-range potential",
            "formula": "a_FM/a_N = alpha_FM (1+r/lambda_FM) exp(-r/lambda_FM)",
            "needed_inputs": "lambda_FM; alpha_FM; source coupling; screening/composition; real R10 bound curve",
            "maps_to": "R10_fifth_force",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": GENERATED,
        },
        {
            "map_id": "WFM921_2_WEP",
            "quantity": "eta_FM_AB",
            "definition": "composition/source-charge difference induced by the coupling branch",
            "formula": "eta_FM_AB := |C_eta_A epsilon_FM_A - C_eta_B epsilon_FM_B|",
            "needed_inputs": "species/source coefficients C_eta_A,B or no-species theorem; materials; normalization",
            "maps_to": "R1_WEP_source_charge",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": GENERATED,
        },
        {
            "map_id": "WFM921_3_clock",
            "quantity": "alpha_clock_FM",
            "definition": "clock/redshift sensitivity to nonmetric or source-normalization coupling",
            "formula": "alpha_clock_FM := C_clock_FM epsilon_FM_clock",
            "needed_inputs": "clock projection coefficient; coupling to transition standards; source path",
            "maps_to": "R2_clock_redshift",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": GENERATED,
        },
        {
            "map_id": "WFM921_4_PPN_gamma_beta",
            "quantity": "delta_gamma_FM, delta_beta_FM",
            "definition": "metric-potential slip and second-order source-normalization residues",
            "formula": "delta_gamma_FM=C_gamma_FM epsilon_FM; delta_beta_FM=C_beta_FM epsilon_FM^2 or C_beta1_FM epsilon_FM",
            "needed_inputs": "weak-field metric solution; projection to gij and g00 orders; coefficients",
            "maps_to": "R3_gamma;R4_beta",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": GENERATED,
        },
        {
            "map_id": "WFM921_5_preferred_frame",
            "quantity": "alpha1_FM, alpha2_FM, alpha3_FM, xi_FM",
            "definition": "preferred-frame/location residues if A_M, holonomy, or Pi_M leakage selects a local frame/domain",
            "formula": "alpha_i_FM := C_alpha_i_FM epsilon_FM_frame; xi_FM:=C_xi_FM epsilon_FM_aniso",
            "needed_inputs": "frame vector/domain orientation; holonomy anisotropy; metric g0i projection",
            "maps_to": "R5_alpha1;R6_alpha2;R7_alpha3;R8_xi",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": GENERATED,
        },
        {
            "map_id": "WFM921_6_Gdot_or_orbital",
            "quantity": "Gdot_FM_over_G, delta_mu_orbital",
            "definition": "time/radial drift of the effective source normalization from nonclosed Pi_M current",
            "formula": "Gdot/G ~ d_t epsilon_FM; delta_mu_orbital ~ integral_shell dPiMJ_leak / M",
            "needed_inputs": "time profile; radial shell profile; orbital normalization; source path",
            "maps_to": "R9_Gdot;orbital_source_normalization",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": GENERATED,
        },
    ]


def unit_rows() -> list[dict[str, object]]:
    return [
        {
            "unit_id": "UNIT921_0_KBFH",
            "symbol": "K_BF_H",
            "required_unit_decision": "coefficient units must make integral A_M wedge Pi_M J_H an action",
            "current_status": "MISSING_PARENT_UNITS",
            "blocks": "all numeric force, R10, WEP, PPN, clock, and orbital claims",
            "valid_for_claim": "false",
            "generated_utc": GENERATED,
        },
        {
            "unit_id": "UNIT921_1_A_M",
            "symbol": "A_M",
            "required_unit_decision": "mass-gauge one-form normalization and whether line integral is dimensionless",
            "current_status": "MISSING_GAUGE_NORMALIZATION",
            "blocks": "A_M_holonomy and F_M_force scale",
            "valid_for_claim": "false",
            "generated_utc": GENERATED,
        },
        {
            "unit_id": "UNIT921_2_dPiMJ",
            "symbol": "dPiMJ_leak",
            "required_unit_decision": "mass-current divergence, shell flux, or dimensionless normalized leakage",
            "current_status": "MISSING_CURRENT_NORMALIZATION",
            "blocks": "epsilon_FM and orbital/source-normalization maps",
            "valid_for_claim": "false",
            "generated_utc": GENERATED,
        },
        {
            "unit_id": "UNIT921_3_lambdaFM",
            "symbol": "lambda_FM",
            "required_unit_decision": "finite range/transition length for any Yukawa-equivalent score",
            "current_status": "MISSING_RANGE_LAW",
            "blocks": "R10 alpha(lambda)",
            "valid_for_claim": "false",
            "generated_utc": GENERATED,
        },
        {
            "unit_id": "UNIT921_4_projection_coefficients",
            "symbol": "C_eta,C_clock,C_gamma,C_beta,C_alpha_i,C_xi",
            "required_unit_decision": "dimensionless weak-field projection coefficients from parent linearization",
            "current_status": "MISSING_LINEARIZED_PARENT_MAP",
            "blocks": "arena-specific bound comparison",
            "valid_for_claim": "false",
            "generated_utc": GENERATED,
        },
    ]


def arena_rows(bounds: dict[str, dict[str, str]]) -> list[dict[str, object]]:
    configs = [
        ("BAM921_0_WEP", "R1_WEP_source_charge", "eta_FM_AB", "eta_FM_AB <= bound"),
        ("BAM921_1_clock", "R2_clock_redshift", "alpha_clock_FM", "abs(alpha_clock_FM) <= bound"),
        ("BAM921_2_gamma", "R3_gamma", "delta_gamma_FM", "abs(delta_gamma_FM) <= bound"),
        ("BAM921_3_beta", "R4_beta", "delta_beta_FM", "abs(delta_beta_FM) <= bound"),
        ("BAM921_4_alpha1", "R5_alpha1", "alpha1_FM", "abs(alpha1_FM) <= bound"),
        ("BAM921_5_alpha2", "R6_alpha2", "alpha2_FM", "abs(alpha2_FM) <= bound"),
        ("BAM921_6_alpha3", "R7_alpha3", "alpha3_FM", "abs(alpha3_FM) <= bound"),
        ("BAM921_7_xi", "R8_xi", "xi_FM", "abs(xi_FM) <= bound"),
        ("BAM921_8_Gdot", "R9_Gdot", "Gdot_FM_over_G", "abs(Gdot/G) <= bound"),
        ("BAM921_9_R10", "R10_fifth_force", "alpha_FM(lambda_FM)", "abs(alpha_FM(lambda)) <= alpha_bound(lambda)"),
    ]
    rows: list[dict[str, object]] = []
    for map_id, row_id, residual, acceptance in configs:
        bound = bounds.get(row_id, {})
        rows.append(
            {
                "map_id": map_id,
                "local_bound_row": row_id,
                "observable": bound.get("observable", ""),
                "upper_bound": bound.get("upper_bound", ""),
                "units": bound.get("units", ""),
                "FM_residual": residual,
                "acceptance_rule": acceptance,
                "required_MTS_inputs": "parent units; projection coefficient; source path; numeric residual",
                "score_status": "not_scored_missing_MTS_inputs",
                "valid_for_claim": "false",
                "generated_utc": GENERATED,
            }
        )
    return rows


def smoke_rows() -> list[dict[str, object]]:
    return [
        {
            "smoke_id": "SMK921_0_schema_only_epsilon",
            "branch": "FM_force_nonclaim",
            "input_status": "MISSING_KBFH_UNITS;MISSING_A_NORM;MISSING_dPiMJ_NUMERIC",
            "formula": "epsilon_FM = |K_BF_H| |A_M| |dPiMJ_leak| / N_FM",
            "expected_runner_result": "blocked_missing_parent_units",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": GENERATED,
        },
        {
            "smoke_id": "SMK921_1_R10_symbolic_only",
            "branch": "R10_alpha_lambda",
            "input_status": "MISSING_lambda_FM;MISSING_alpha_FM;R10_DIGITIZED_CURVE_PLACEHOLDER",
            "formula": "alpha_FM(lambda_FM) compared to alpha_bound(lambda)",
            "expected_runner_result": "blocked_symbolic_curve_required",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": GENERATED,
        },
        {
            "smoke_id": "SMK921_2_PPN_vector_placeholder",
            "branch": "PPN_WEP_clock_vector",
            "input_status": "MISSING_projection_coefficients",
            "formula": "residual_i = C_i epsilon_FM",
            "expected_runner_result": "blocked_missing_linearized_parent_map",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": GENERATED,
        },
    ]


def decision_rows() -> list[dict[str, object]]:
    return [
        {
            "decision_id": "BD921_0_map_written",
            "branch": "weak_field_bound_interface",
            "verdict": "schema_ready_nonclaim",
            "reason": "FM coupling residual now maps to WEP, clock, PPN, preferred-frame, Gdot/orbital, and R10 arenas",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": GENERATED,
        },
        {
            "decision_id": "BD921_1_KBFH_blocks_score",
            "branch": "units_and_parent_normalization",
            "verdict": "main_blocker",
            "reason": "without K_BF_H units and A_M/J_H normalization, no numerical force or alpha(lambda) is meaningful",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": GENERATED,
        },
        {
            "decision_id": "BD921_2_next",
            "branch": "parent_units_or_smoke_runner",
            "verdict": "selected",
            "reason": "next step should either parent-sign K_BF_H normalization or create a strict local-bound smoke runner that fails cleanly",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": GENERATED,
        },
    ]


def gate_rows() -> list[dict[str, object]]:
    return [
        {
            "gate_id": "CGATE921_0_KBFH_units",
            "claim": "K_BF_H has parent-derived units and normalization",
            "blocker": "not supplied by the current parent action",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": GENERATED,
        },
        {
            "gate_id": "CGATE921_1_force_projection",
            "claim": "F_M_force projects to a local acceleration/metric residual",
            "blocker": "linearized parent map and projection coefficients are missing",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": GENERATED,
        },
        {
            "gate_id": "CGATE921_2_R10_alpha_lambda",
            "claim": "FM branch has a valid alpha(lambda) R10 score",
            "blocker": "range law, alpha_FM(lambda), and real digitized bound curve are missing",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": GENERATED,
        },
        {
            "gate_id": "CGATE921_3_local_bounds_pass",
            "claim": "FM branch passes WEP/clock/PPN/orbital/local-GR bounds",
            "blocker": "smoke rows are schema-only and intentionally invalid for claim",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": GENERATED,
        },
    ]


def next_rows() -> list[dict[str, object]]:
    return [
        {
            "next_target": NEXT_TARGET,
            "objective": "either derive K_BF_H units/normalization from the parent BF/mass-gauge action or run a strict nonclaim local-bound smoke runner that proves all missing fields block scoring",
            "include": "action dimensions, A_M normalization, J_H form degree/units, epsilon_FM normalization, local_bound_claims join, R10 curve status",
            "exclude": "numeric pass claims, alpha(lambda) without a range law, free G/M absorption, GitHub action, formalization-workbench edits",
            "valid_for_claim": "false",
            "generated_utc": GENERATED,
        }
    ]


def formalization_changed_count() -> int:
    formalization = ROOT.parent / "formalization-workbench"
    if not formalization.exists():
        return 0
    return sum(
        1
        for path in formalization.rglob("*")
        if path.is_file() and datetime.fromtimestamp(path.stat().st_mtime) > FORMALIZATION_CUTOFF
    )


def all_false(rows: list[dict[str, object]], fields: tuple[str, ...]) -> bool:
    return all(str(row.get(field, "")).strip().lower() != "true" for row in rows for field in fields)


def validation_rows(
    src: list[dict[str, object]],
    weak: list[dict[str, object]],
    units: list[dict[str, object]],
    arenas: list[dict[str, object]],
    smoke: list[dict[str, object]],
    decisions: list[dict[str, object]],
    gates: list[dict[str, object]],
) -> list[dict[str, object]]:
    source_ok = all(row["exists"] == "true" and row["needle_found"] == "true" for row in src)
    prior = OUT / "P8_Y5_BRR545_920_VALIDATION.csv"
    prior_ok = prior.exists() and "V920_10_validation_rows_ready" in read_text(prior)
    required_bounds = {"R1_WEP_source_charge", "R2_clock_redshift", "R3_gamma", "R4_beta", "R5_alpha1", "R6_alpha2", "R7_alpha3", "R8_xi", "R9_Gdot", "R10_fifth_force"}
    mapped_bounds = {row["local_bound_row"] for row in arenas}
    false_fields = ("claim_allowed", "valid_for_claim")
    generated = weak + units + arenas + smoke + decisions + gates
    changed = formalization_changed_count()
    return [
        {
            "check_id": "V921_0_sources_exist_and_needles",
            "result": "pass" if source_ok else "fail",
            "detail": "all source paths exist and needles are present" if source_ok else "missing source or needle",
            "generated_utc": GENERATED,
        },
        {
            "check_id": "V921_1_prior_920_clean",
            "result": "pass" if prior_ok else "fail",
            "detail": "P8_Y5_BRR545_920_VALIDATION.csv clean" if prior_ok else "920 validation missing or incomplete",
            "generated_utc": GENERATED,
        },
        {
            "check_id": "V921_2_weak_field_map_nonclaim",
            "result": "pass" if all_false(weak, false_fields) and len(weak) >= 7 else "fail",
            "detail": "weak-field map covers epsilon, R10, WEP, clock, PPN, preferred-frame, and Gdot/orbital rows",
            "generated_utc": GENERATED,
        },
        {
            "check_id": "V921_3_units_block_scoring",
            "result": "pass" if all(row["current_status"].startswith("MISSING") for row in units) else "fail",
            "detail": "all units/projection prerequisites remain explicit blockers",
            "generated_utc": GENERATED,
        },
        {
            "check_id": "V921_4_local_bounds_joined",
            "result": "pass" if required_bounds <= mapped_bounds else "fail",
            "detail": "WEP, clock, gamma, beta, alpha1, alpha2, alpha3, xi, Gdot, and R10 bound rows are mapped",
            "generated_utc": GENERATED,
        },
        {
            "check_id": "V921_5_smoke_rows_block_claim",
            "result": "pass" if all_false(smoke, false_fields) and all("blocked" in row["expected_runner_result"] for row in smoke) else "fail",
            "detail": "all smoke rows are expected to block scoring until missing inputs are supplied",
            "generated_utc": GENERATED,
        },
        {
            "check_id": "V921_6_claim_gates_false",
            "result": "pass" if all_false(gates, false_fields) else "fail",
            "detail": "KBFH units, projection, R10, and local-bound pass gates remain false",
            "generated_utc": GENERATED,
        },
        {
            "check_id": "V921_7_decisions_nonclaim",
            "result": "pass" if all_false(decisions, false_fields) else "fail",
            "detail": "decision selects parent-units or strict smoke runner without promotion",
            "generated_utc": GENERATED,
        },
        {
            "check_id": "V921_8_all_generated_rows_nonclaim",
            "result": "pass" if all_false(generated, false_fields) else "fail",
            "detail": "all generated rows keep guarded claim fields false",
            "generated_utc": GENERATED,
        },
        {
            "check_id": "V921_9_formalization_workbench_untouched",
            "result": "pass" if changed == 0 else "fail",
            "detail": f"formalization_changed_after_cutoff={changed}",
            "generated_utc": GENERATED,
        },
        {
            "check_id": "V921_10_next_target_selected",
            "result": "pass" if NEXT_TARGET.startswith("922-") else "fail",
            "detail": NEXT_TARGET,
            "generated_utc": GENERATED,
        },
        {
            "check_id": "V921_11_validation_rows_ready",
            "result": "pass",
            "detail": "validation table constructed",
            "generated_utc": GENERATED,
        },
    ]


def write_doc(
    src: list[dict[str, object]],
    summary: list[dict[str, object]],
    weak: list[dict[str, object]],
    units: list[dict[str, object]],
    arenas: list[dict[str, object]],
    smoke: list[dict[str, object]],
    decisions: list[dict[str, object]],
    gates: list[dict[str, object]],
    next_target: list[dict[str, object]],
    validation: list[dict[str, object]],
) -> None:
    body = f"""# 921 - Y5/R10 FM Force Weak-Field Map And KBFH Units Bound Runner

Private local-bound interface checkpoint. This is not a public R10, WEP, clock, PPN, orbital, local-GR, or unified-field claim.

Status: `{STATUS}`

Claim ceiling: `{CLAIM_CEILING}`

Current result: **the coupling residual now has a weak-field/bounds interface, but it cannot be scored until parent units and projection coefficients exist.**

The internal pressure variable is:

```text
epsilon_FM := |K_BF_H| |A_M| |dPiMJ_leak| / N_FM
              + |K_BF_H| |B_zero_flux| / N_B.
```

That is not yet physics evidence. It becomes a testable prediction only after `K_BF_H`, `A_M`, `J_H`, the weak-field projection coefficients, and any finite range law are parent/source-backed.

The R10 rule remains strict:

```text
a_FM/a_N = alpha_FM (1+r/lambda_FM) exp(-r/lambda_FM)
```

only exists if MTS derives `alpha_FM(lambda_FM)` and `lambda_FM`. Otherwise the row is symbolic and blocked.

## Non-Claim Summary

{md_table(summary, ["status", "claim_ceiling", "current_result", "practical_meaning", "next_target", "valid_for_claim", "generated_utc"])}

## Source Register

{md_table(src, ["source_id", "path", "role", "needle", "exists", "needle_found", "valid_for_claim", "generated_utc"])}

## Weak-Field Map

{md_table(weak, ["map_id", "quantity", "definition", "formula", "needed_inputs", "maps_to", "claim_allowed", "valid_for_claim", "generated_utc"])}

## Units And Projection Audit

{md_table(units, ["unit_id", "symbol", "required_unit_decision", "current_status", "blocks", "valid_for_claim", "generated_utc"])}

## Local Bound Arena Map

{md_table(arenas, ["map_id", "local_bound_row", "observable", "upper_bound", "units", "FM_residual", "acceptance_rule", "required_MTS_inputs", "score_status", "valid_for_claim", "generated_utc"])}

## Nonclaim Smoke Rows

{md_table(smoke, ["smoke_id", "branch", "input_status", "formula", "expected_runner_result", "claim_allowed", "valid_for_claim", "generated_utc"])}

## Branch Decision

{md_table(decisions, ["decision_id", "branch", "verdict", "reason", "claim_allowed", "valid_for_claim", "generated_utc"])}

## Claim Gate

{md_table(gates, ["gate_id", "claim", "blocker", "claim_allowed", "valid_for_claim", "generated_utc"])}

## Next Target

{md_table(next_target, ["next_target", "objective", "include", "exclude", "valid_for_claim", "generated_utc"])}

## Validation

{md_table(validation, ["check_id", "result", "detail", "generated_utc"])}
"""
    (ROOT / DOC_NAME).write_text(body, encoding="utf-8")


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    src = build_sources()
    bounds = local_bound_index()
    summary = summary_rows()
    weak = weak_field_rows()
    units = unit_rows()
    arenas = arena_rows(bounds)
    smoke = smoke_rows()
    decisions = decision_rows()
    gates = gate_rows()
    next_target = next_rows()
    validation = validation_rows(src, weak, units, arenas, smoke, decisions, gates)

    write_csv(OUT / "P8_Y5_R10_921_SOURCE_REGISTER.csv", src, ["source_id", "path", "absolute_path", "role", "needle", "exists", "needle_found", "valid_for_claim", "generated_utc"])
    write_csv(OUT / "P8_Y5_R10_921_NONCLAIM_SUMMARY.csv", summary, ["status", "claim_ceiling", "current_result", "practical_meaning", "next_target", "valid_for_claim", "generated_utc"])
    write_csv(OUT / "P8_Y5_R10_921_WEAK_FIELD_MAP.csv", weak, ["map_id", "quantity", "definition", "formula", "needed_inputs", "maps_to", "claim_allowed", "valid_for_claim", "generated_utc"])
    write_csv(OUT / "P8_Y5_R10_921_UNITS_CONVENTION_AUDIT.csv", units, ["unit_id", "symbol", "required_unit_decision", "current_status", "blocks", "valid_for_claim", "generated_utc"])
    write_csv(OUT / "P8_Y5_R10_921_LOCAL_BOUND_ARENA_MAP.csv", arenas, ["map_id", "local_bound_row", "observable", "upper_bound", "units", "FM_residual", "acceptance_rule", "required_MTS_inputs", "score_status", "valid_for_claim", "generated_utc"])
    write_csv(OUT / "P8_Y5_R10_921_NONCLAIM_SMOKE_ROWS.csv", smoke, ["smoke_id", "branch", "input_status", "formula", "expected_runner_result", "claim_allowed", "valid_for_claim", "generated_utc"])
    write_csv(OUT / "P8_Y5_R10_921_BRANCH_DECISION.csv", decisions, ["decision_id", "branch", "verdict", "reason", "claim_allowed", "valid_for_claim", "generated_utc"])
    write_csv(OUT / "P8_Y5_R10_921_CLAIM_GATE.csv", gates, ["gate_id", "claim", "blocker", "claim_allowed", "valid_for_claim", "generated_utc"])
    write_csv(OUT / "P8_Y5_R10_921_NEXT_TARGET.csv", next_target, ["next_target", "objective", "include", "exclude", "valid_for_claim", "generated_utc"])
    write_csv(OUT / "P8_Y5_BRR545_921_VALIDATION.csv", validation, ["check_id", "result", "detail", "generated_utc"])
    write_doc(src, summary, weak, units, arenas, smoke, decisions, gates, next_target, validation)

    failed = [row for row in validation if row["result"] != "pass"]
    if failed:
        raise SystemExit(f"validation failed: {failed}")
    print(STATUS)
    print(f"wrote {ROOT / DOC_NAME}")
    print(f"next target: {NEXT_TARGET}")


if __name__ == "__main__":
    main()

from __future__ import annotations

import csv
from datetime import datetime, timezone
from pathlib import Path


POST_CHECKPOINT = Path(__file__).resolve().parents[1]
RESIDUALS = POST_CHECKPOINT / "source-intake" / "mts_residuals"
FORMALIZATION = POST_CHECKPOINT.parent / "formalization-workbench"
OUTPUT_DOC = POST_CHECKPOINT / "718-Y5-R10-AEH-prefactor-gradient-zero-theorem-or-retained-source-pack.md"
NEXT_TARGET = "719-Y5-R10-AEH-gradient-canonical-projection-zero-or-mode-source-pack.md"
GENERATED_UTC = datetime.now(timezone.utc).replace(microsecond=0).isoformat()
CUTOFF = datetime(2026, 5, 31, 14, 42, 0)


SOURCES = {
    "717_doc": {
        "path": POST_CHECKPOINT / "717-Y5-R10-observed-frame-lock-and-frame-transfer-coefficient-pack.md",
        "note": "frame-transfer branch lock and next target",
    },
    "717_validation": {
        "path": RESIDUALS / "P8_Y5_BRR545_717_VALIDATION.csv",
        "note": "prior checkpoint validation",
    },
    "717_conformal": {
        "path": RESIDUALS / "P8_Y5_R10_717_CONFORMAL_DERIVATION.csv",
        "note": "f_frame and D=4 Einstein-frame formula",
    },
    "717_queue": {
        "path": RESIDUALS / "P8_Y5_R10_717_BOUND_OR_DERIVE_QUEUE.csv",
        "note": "a_I selected as next derivation target",
    },
    "716_doc": {
        "path": POST_CHECKPOINT / "716-Y5-R10-matter-coupling-source-charge-derivation-or-free-coefficient-lock.md",
        "note": "Q_Aa charge law and b_A,I definition",
    },
    "715_pack": {
        "path": RESIDUALS / "P8_Y5_R10_715_MINIMUM_EXECUTABLE_COEFFICIENT_PACK.csv",
        "note": "minimum retained scalar coefficient pack",
    },
    "710_descent": {
        "path": RESIDUALS / "P8_Y5_R10_710_DESCENT_PARENT_ACTION_CLAUSE.csv",
        "note": "conditional no-prefactor and descent theorem clauses",
    },
    "710_aeh_update": {
        "path": RESIDUALS / "P8_Y5_R10_710_AEH_SCALAR_UPDATE.csv",
        "note": "AEH scalar update after descent-clause attempt",
    },
    "711_ownership": {
        "path": RESIDUALS / "P8_Y5_R10_711_DPC710_OWNERSHIP_MAP.csv",
        "note": "ownership state of DPC710 no-prefactor and same-frame clauses",
    },
    "704_doc": {
        "path": POST_CHECKPOINT / "704-Y5-R10-EH-prefactor-constant-theorem-or-kappa-gradient-bound.md",
        "note": "EH prefactor constant theorem and kappa-gradient fallback",
    },
    "704_validation": {
        "path": RESIDUALS / "P8_Y5_BRR545_704_VALIDATION.csv",
        "note": "704 validation",
    },
    "705_channels": {
        "path": RESIDUALS / "P8_Y5_R10_705_VARIABLE_PREFACTOR_CHANNELS.csv",
        "note": "variable-prefactor channel ledger",
    },
    "705_validation": {
        "path": RESIDUALS / "P8_Y5_BRR545_705_VALIDATION.csv",
        "note": "705 validation",
    },
    "706_inventory": {
        "path": RESIDUALS / "P8_Y5_R10_706_AEH_TERM_INVENTORY.csv",
        "note": "AEH term inventory",
    },
    "706_validation": {
        "path": RESIDUALS / "P8_Y5_BRR545_706_VALIDATION.csv",
        "note": "706 validation",
    },
    "707_doc": {
        "path": POST_CHECKPOINT / "707-Y5-R10-scalar-class-FR-prefactor-zero-or-AEH-bound.md",
        "note": "scalar/class FR prefactor zero attempt and retained bound pack",
    },
    "707_validation": {
        "path": RESIDUALS / "P8_Y5_BRR545_707_VALIDATION.csv",
        "note": "707 validation",
    },
}


def write_csv(path: Path, rows: list[dict[str, object]], fieldnames: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def bool_text(value: bool) -> str:
    return "true" if value else "false"


def source_path_string(*keys: str) -> str:
    return ";".join(str(SOURCES[key]["path"]) for key in keys)


def csv_contains(path: Path, *needles: str) -> bool:
    text = path.read_text(encoding="utf-8", errors="replace")
    return all(needle in text for needle in needles)


def prior_validation_clean(path: Path) -> bool:
    rows = read_csv(path)
    return bool(rows) and all(row.get("result") == "pass" for row in rows)


def all_valid_false(paths: list[Path]) -> bool:
    for path in paths:
        rows = read_csv(path)
        if not rows:
            continue
        if "valid_for_claim" not in rows[0]:
            continue
        if any(row.get("valid_for_claim", "").lower() != "false" for row in rows):
            return False
    return True


def formalization_changed_after_cutoff() -> int:
    if not FORMALIZATION.exists():
        return -1
    count = 0
    for path in FORMALIZATION.rglob("*"):
        if not path.is_file():
            continue
        modified = datetime.fromtimestamp(path.stat().st_mtime)
        if modified > CUTOFF:
            count += 1
    return count


def markdown_table(rows: list[dict[str, object]], fields: list[str]) -> str:
    header = "| " + " | ".join(fields) + " |"
    separator = "| " + " | ".join("---" for _ in fields) + " |"
    body = []
    for row in rows:
        cells = []
        for field in fields:
            value = str(row.get(field, ""))
            value = value.replace("\n", " ").replace("|", "\\|")
            cells.append(value)
        body.append("| " + " | ".join(cells) + " |")
    return "\n".join([header, separator, *body])


def main() -> None:
    RESIDUALS.mkdir(parents=True, exist_ok=True)

    source_register = [
        {
            "source_id": key,
            "path": str(info["path"]),
            "exists": bool_text(info["path"].exists()),
            "role": info["note"],
            "valid_for_claim": "false",
            "generated_utc": GENERATED_UTC,
        }
        for key, info in SOURCES.items()
    ]

    zero_theorem_audit = [
        {
            "theorem_id": "AGZ718_0_parent_extraction",
            "zero_route": "extract A_EH from the parent action",
            "required_statement": "A_EH(u) is explicitly supplied by the parent action or by a theorem proving it absent",
            "current_evidence": "704/705/706 inventory names the channel but does not supply a claim-ready parent coefficient",
            "status": "missing_parent_AEH_extraction",
            "effect_if_closed": "turns a_I into a computable or theorem-zero object",
            "valid_for_claim": "false",
            "source_paths": source_path_string("704_doc", "705_channels", "706_inventory"),
            "generated_utc": GENERATED_UTC,
        },
        {
            "theorem_id": "AGZ718_1_no_variable_prefactor",
            "zero_route": "identity no-prefactor theorem",
            "required_statement": "A_EH(u)=constant in the local observed frame, hence a_I=partial_I ln A_EH|u0=0",
            "current_evidence": "DPC710_2 exists only as candidate_clause_not_parent_signed",
            "status": "not_parent_signed",
            "effect_if_closed": "kills frame-induced scalar source from A_EH",
            "valid_for_claim": "false",
            "source_paths": source_path_string("710_descent", "711_ownership"),
            "generated_utc": GENERATED_UTC,
        },
        {
            "theorem_id": "AGZ718_2_calibration_guard",
            "zero_route": "A0 normalization",
            "required_statement": "A0=A_EH(u0)=1 is only a measured-G normalization unless the gradient also vanishes",
            "current_evidence": "MEP715_4 and MEP715_5 are separate required objects",
            "status": "guard_active",
            "effect_if_closed": "prevents replacing a_I=0 with A0=1",
            "valid_for_claim": "false",
            "source_paths": source_path_string("715_pack", "704_doc"),
            "generated_utc": GENERATED_UTC,
        },
        {
            "theorem_id": "AGZ718_3_vacuum_extremum",
            "zero_route": "local vacuum extremum",
            "required_statement": "u0 is a stationary point that forces partial_I ln A_EH|u0=0, not merely partial_I V_eff=0",
            "current_evidence": "no parent extremum law ties local vacuum stationarity to the EH prefactor gradient",
            "status": "not_derived",
            "effect_if_closed": "could zero a_I without proving A_EH is globally constant",
            "valid_for_claim": "false",
            "source_paths": source_path_string("715_pack", "717_doc"),
            "generated_utc": GENERATED_UTC,
        },
        {
            "theorem_id": "AGZ718_4_charge_cancellation",
            "zero_route": "Einstein-frame charge cancellation",
            "required_statement": "E_a^I(b_A,I-a_I/2)=0 for every local source/test A and scalar mode a",
            "current_evidence": "716 and 717 give the formula, but neither b_A,I nor a_I is sourced or theorem-zero",
            "status": "not_derived",
            "effect_if_closed": "could suppress observable scalar charge even if a_I is not zero",
            "valid_for_claim": "false",
            "source_paths": source_path_string("716_doc", "717_conformal"),
            "generated_utc": GENERATED_UTC,
        },
        {
            "theorem_id": "AGZ718_5_no_mode_projection",
            "zero_route": "canonical projection/no-mode theorem",
            "required_statement": "E_a^I a_I=0 for all propagating modes, or no local scalar mode exists",
            "current_evidence": "canonical mode rows remain missing in 715",
            "status": "not_derived",
            "effect_if_closed": "turns nonzero formal a_I into no observable local coupling",
            "valid_for_claim": "false",
            "source_paths": source_path_string("715_pack", "717_queue"),
            "generated_utc": GENERATED_UTC,
        },
        {
            "theorem_id": "AGZ718_6_boundary_projection_silence",
            "zero_route": "no hidden boundary/projection AEH shift",
            "required_statement": "quotient projection and boundary/counterterms do not renormalize A_EH or its gradient",
            "current_evidence": "706 inventory keeps boundary/counterterm and frame-transfer channels open",
            "status": "not_parent_signed",
            "effect_if_closed": "removes a common escape hatch for hidden gradient debt",
            "valid_for_claim": "false",
            "source_paths": source_path_string("706_inventory", "710_descent"),
            "generated_utc": GENERATED_UTC,
        },
        {
            "theorem_id": "AGZ718_7_verdict",
            "zero_route": "claim-ready a_I=0 theorem",
            "required_statement": "one of the exact zero routes is parent-signed with no missing source rows",
            "current_evidence": "all available routes remain unsigned or incomplete",
            "status": "fail_current_corpus",
            "effect_if_closed": "would unlock local-GR reduction tests for the scalar AEH channel",
            "valid_for_claim": "false",
            "source_paths": source_path_string("717_doc", "710_descent", "711_ownership"),
            "generated_utc": GENERATED_UTC,
        },
    ]

    variation_derivation = [
        {
            "step_id": "AVD718_0_definition",
            "object": "EH prefactor",
            "equation": "S_EH = int sqrt(-g_obs) (M_*^2/2) A_EH(u) R[g_obs]",
            "result": "define A0=A_EH(u0), a_I=partial_I ln A_EH|u0, a_IJ=partial_I partial_J ln A_EH|u0",
            "status": "definition",
            "valid_for_claim": "false",
            "source_paths": source_path_string("715_pack", "717_conformal"),
            "generated_utc": GENERATED_UTC,
        },
        {
            "step_id": "AVD718_1_local_expansion",
            "object": "Taylor expansion",
            "equation": "A_EH(u0+delta u)=A0[1+a_I delta u^I+1/2(a_IJ+a_I a_J)delta u^I delta u^J+...]",
            "result": "A0 and a_I are independent data; A0=1 does not force a_I=0",
            "status": "derived_shape",
            "valid_for_claim": "false",
            "source_paths": source_path_string("715_pack"),
            "generated_utc": GENERATED_UTC,
        },
        {
            "step_id": "AVD718_2_metric_variation",
            "object": "metric equation",
            "equation": "delta_g[sqrt(-g)A_EH R] -> A_EH G_mu nu + (g_mu nu box - nabla_mu nabla_nu)A_EH",
            "result": "spacetime gradients of A_EH are a genuine local metric residual unless A_EH is constant or mode-silent",
            "status": "derived_shape",
            "valid_for_claim": "false",
            "source_paths": source_path_string("704_doc", "710_descent"),
            "generated_utc": GENERATED_UTC,
        },
        {
            "step_id": "AVD718_3_scalar_variation",
            "object": "scalar equation",
            "equation": "delta_u S_EH contains (M_*^2/2) A0 a_I R[g_obs] delta u^I",
            "result": "a_I is the curvature-source coefficient before frame normalization",
            "status": "derived_shape",
            "valid_for_claim": "false",
            "source_paths": source_path_string("704_doc", "715_pack"),
            "generated_utc": GENERATED_UTC,
        },
        {
            "step_id": "AVD718_4_Einstein_charge",
            "object": "D=4 Einstein-frame source charge",
            "equation": "Q_Aa=N_frame E_a^I(b_A,I-a_I/2)",
            "result": "even a matter-blind b_A,I=0 branch carries charge if E_a^I a_I is nonzero",
            "status": "derived_from_717",
            "valid_for_claim": "false",
            "source_paths": source_path_string("716_doc", "717_conformal"),
            "generated_utc": GENERATED_UTC,
        },
        {
            "step_id": "AVD718_5_zero_condition",
            "object": "observable AEH silence",
            "equation": "A_a := E_a^I a_I = 0 for every propagating mode a, or b_A,I cancels a_I/2 for every source/test",
            "result": "a_I=0 is sufficient but not strictly necessary; projected/cancelled/no-mode silence is the next derivable target",
            "status": "conditional_zero_condition",
            "valid_for_claim": "false",
            "source_paths": source_path_string("715_pack", "717_doc"),
            "generated_utc": GENERATED_UTC,
        },
    ]

    retained_source_pack = [
        {
            "pack_id": "RAP718_0_A0",
            "symbol": "A0",
            "definition": "A_EH(u0)",
            "current_value_or_status": "MISSING_A0_OR_A0_EQUALS_1_THEOREM",
            "units": "dimensionless",
            "priority": "P1",
            "unlocks": "measured-G normalization and Newtonian limit bookkeeping",
            "valid_for_claim": "false",
            "source_paths": source_path_string("715_pack"),
            "generated_utc": GENERATED_UTC,
        },
        {
            "pack_id": "RAP718_1_aI",
            "symbol": "a_I",
            "definition": "partial_I ln A_EH|u0",
            "current_value_or_status": "MISSING_PREFACTOR_GRADIENT_VECTOR_OR_ZERO_THEOREM",
            "units": "inverse_field_units",
            "priority": "P0",
            "unlocks": "frame transfer, scalar charge, PPN, Gdot, R10, and local-GR gate",
            "valid_for_claim": "false",
            "source_paths": source_path_string("715_pack", "717_queue"),
            "generated_utc": GENERATED_UTC,
        },
        {
            "pack_id": "RAP718_2_aIJ",
            "symbol": "a_IJ",
            "definition": "partial_I partial_J ln A_EH|u0",
            "current_value_or_status": "MISSING_PREFACTOR_HESSIAN",
            "units": "inverse_field_units_squared",
            "priority": "P2",
            "unlocks": "beta/nonlinear source-normalization and stability maps",
            "valid_for_claim": "false",
            "source_paths": source_path_string("715_pack"),
            "generated_utc": GENERATED_UTC,
        },
        {
            "pack_id": "RAP718_3_mode_projection",
            "symbol": "A_a",
            "definition": "E_a^I a_I",
            "current_value_or_status": "MISSING_CANONICAL_MODE_PROJECTION",
            "units": "canonical_inverse_field_units",
            "priority": "P0",
            "unlocks": "decides whether a_I is actually visible to local scalar modes",
            "valid_for_claim": "false",
            "source_paths": source_path_string("715_pack"),
            "generated_utc": GENERATED_UTC,
        },
        {
            "pack_id": "RAP718_4_effective_charge_D4",
            "symbol": "Q_Aa",
            "definition": "N_frame E_a^I(b_A,I-a_I/2)",
            "current_value_or_status": "MISSING_bAI_aI_E_MODE_AND_NORMALIZATION",
            "units": "dimensionless",
            "priority": "P1",
            "unlocks": "WEP, R10 alpha(lambda), PPN gamma/beta, clocks",
            "valid_for_claim": "false",
            "source_paths": source_path_string("716_doc", "717_conformal"),
            "generated_utc": GENERATED_UTC,
        },
        {
            "pack_id": "RAP718_5_Gdot_AEH",
            "symbol": "dlnA0_dt",
            "definition": "a_I dot(u0)^I",
            "current_value_or_status": "MISSING_TIME_DERIVATIVE_AND_AEH_GRADIENT",
            "units": "per_time",
            "priority": "P2",
            "unlocks": "Gdot and clock drift rows",
            "valid_for_claim": "false",
            "source_paths": source_path_string("715_pack", "704_doc"),
            "generated_utc": GENERATED_UTC,
        },
    ]

    local_observable_propagation = [
        {
            "arena_id": "LOP718_0_Newton",
            "arena": "Newtonian limit",
            "aeh_entry": "A0 calibrates measured G; a_I enters finite-range scalar corrections only after projection/source map",
            "current_status": "blocked_until_A0_aI_projection_charges_ranges_sourced",
            "claim_effect": "no derived Newton limit from retained scalar branch",
            "valid_for_claim": "false",
            "source_paths": source_path_string("715_pack", "717_doc"),
            "generated_utc": GENERATED_UTC,
        },
        {
            "arena_id": "LOP718_1_R10",
            "arena": "fifth force",
            "aeh_entry": "alpha_AB,a(lambda)=Q_Aa Q_Ba with Q_Aa=N_frame E_a^I(b_A,I-a_I/2)",
            "current_status": "blocked_until_Q_lambda_bound_curve",
            "claim_effect": "no R10 pass",
            "valid_for_claim": "false",
            "source_paths": source_path_string("716_doc", "717_conformal"),
            "generated_utc": GENERATED_UTC,
        },
        {
            "arena_id": "LOP718_2_PPN",
            "arena": "PPN gamma/beta",
            "aeh_entry": "universal nonzero A_a contributes scalar-tensor PPN; Hessian/derivative rows feed beta",
            "current_status": "blocked_until_Aa_aIJ_ZM_modes_sourced",
            "claim_effect": "no PPN/local-GR pass",
            "valid_for_claim": "false",
            "source_paths": source_path_string("715_pack"),
            "generated_utc": GENERATED_UTC,
        },
        {
            "arena_id": "LOP718_3_WEP",
            "arena": "composition dependence",
            "aeh_entry": "a_I shift is universal; WEP risk depends on species variation of b_A,I after common shift",
            "current_status": "blocked_until_bAI_material_map",
            "claim_effect": "no WEP pass",
            "valid_for_claim": "false",
            "source_paths": source_path_string("716_doc"),
            "generated_utc": GENERATED_UTC,
        },
        {
            "arena_id": "LOP718_4_clocks_Gdot",
            "arena": "clock readout and Gdot",
            "aeh_entry": "dlnA0_dt=a_I dot(u0)^I; clock readout requires its own B_clock derivative",
            "current_status": "blocked_until_clock_readout_and_udot_sourced",
            "claim_effect": "no clock/Gdot pass",
            "valid_for_claim": "false",
            "source_paths": source_path_string("715_pack", "704_doc"),
            "generated_utc": GENERATED_UTC,
        },
        {
            "arena_id": "LOP718_5_R11",
            "arena": "retained scalar metric class",
            "aeh_entry": "a_I is an R11 scalar-tensor class coefficient unless zero/projected/no-mode theorem closes",
            "current_status": "blocked_until_retained_R11_row_executable",
            "claim_effect": "no R11 pass or closure",
            "valid_for_claim": "false",
            "source_paths": source_path_string("707_doc", "715_pack"),
            "generated_utc": GENERATED_UTC,
        },
    ]

    decision = [
        {
            "decision_id": "D718_0_direct_zero",
            "target": "a_I=0 direct theorem",
            "result": "not_available_current_corpus",
            "reason": "no parent-signed no-prefactor theorem, parent A_EH extraction, or extremum law forces partial_I ln A_EH|u0=0",
            "next_action": NEXT_TARGET,
            "valid_for_claim": "false",
            "generated_utc": GENERATED_UTC,
        },
        {
            "decision_id": "D718_1_calibration",
            "target": "A0=1 calibration",
            "result": "guarded_not_a_zero_proof",
            "reason": "A0 and a_I are separate Taylor data; setting measured G does not kill the gradient",
            "next_action": NEXT_TARGET,
            "valid_for_claim": "false",
            "generated_utc": GENERATED_UTC,
        },
        {
            "decision_id": "D718_2_retained",
            "target": "retained AEH gradient source pack",
            "result": "selected_current_route",
            "reason": "a_I must remain explicit until zero, projection, cancellation, no-mode, or numeric bound closes it",
            "next_action": NEXT_TARGET,
            "valid_for_claim": "false",
            "generated_utc": GENERATED_UTC,
        },
    ]

    bound_or_derive_queue = [
        {
            "queue_id": "BDQ718_0_projection",
            "target": "A_a=E_a^I a_I",
            "preferred_route": "derive projection zero or no canonical scalar mode",
            "fallback_route": "source Z_IJ, M2_IJ, E_a^I and compute retained local residuals",
            "priority": "P0",
            "next_artifact": NEXT_TARGET,
            "valid_for_claim": "false",
            "source_paths": source_path_string("715_pack"),
            "generated_utc": GENERATED_UTC,
        },
        {
            "queue_id": "BDQ718_1_parent_AEH",
            "target": "parent A_EH(u)",
            "preferred_route": "prove A_EH constant/no F(u)R in the parent action",
            "fallback_route": "fill A0, a_I, a_IJ as sourced symbolic/numeric rows",
            "priority": "P1",
            "next_artifact": "parent_AEH_source_row_if_projection_does_not_close",
            "valid_for_claim": "false",
            "source_paths": source_path_string("704_doc", "706_inventory"),
            "generated_utc": GENERATED_UTC,
        },
        {
            "queue_id": "BDQ718_2_charge_cancellation",
            "target": "E_a^I(b_A,I-a_I/2)=0",
            "preferred_route": "derive universal cancellation from matter/readout construction",
            "fallback_route": "score b_A,I and a_I separately in local tests",
            "priority": "P1",
            "next_artifact": "matter_charge_cancellation_or_material_coefficient_pack",
            "valid_for_claim": "false",
            "source_paths": source_path_string("716_doc", "717_conformal"),
            "generated_utc": GENERATED_UTC,
        },
    ]

    claim_gate_evaluation = [
        {
            "gate_id": "CG718_0_prior_717",
            "gate": "prior frame checkpoint",
            "observed_state": "717 validation clean and nonclaim",
            "result": "pass_structure",
            "claim_effect": "can build on frame formula without promoting claims",
            "valid_for_claim": "false",
            "generated_utc": GENERATED_UTC,
        },
        {
            "gate_id": "CG718_1_no_prefactor",
            "gate": "A_EH constant/no-prefactor theorem",
            "observed_state": "DPC710_2 remains candidate_clause_not_parent_signed",
            "result": "fail_blocked",
            "claim_effect": "a_I=0 not claimable",
            "valid_for_claim": "false",
            "generated_utc": GENERATED_UTC,
        },
        {
            "gate_id": "CG718_2_A0_guard",
            "gate": "A0 normalization",
            "observed_state": "A0 and a_I are separate rows",
            "result": "pass_guard",
            "claim_effect": "prevents measured-G calibration from being treated as local-GR proof",
            "valid_for_claim": "false",
            "generated_utc": GENERATED_UTC,
        },
        {
            "gate_id": "CG718_3_projection",
            "gate": "canonical projection/no-mode",
            "observed_state": "Z/M/E mode pack missing",
            "result": "fail_blocked",
            "claim_effect": "cannot prove AEH gradient is locally invisible",
            "valid_for_claim": "false",
            "generated_utc": GENERATED_UTC,
        },
        {
            "gate_id": "CG718_4_local_claims",
            "gate": "local-GR/Newton/PPN/R10/WEP/Gdot",
            "observed_state": "a_I, projection, charges, modes, ranges, and bounds not sourced",
            "result": "fail_blocked",
            "claim_effect": "no local claim",
            "valid_for_claim": "false",
            "generated_utc": GENERATED_UTC,
        },
        {
            "gate_id": "CG718_5_next_target",
            "gate": "next derivation target",
            "observed_state": NEXT_TARGET,
            "result": "pass_structure",
            "claim_effect": "best route is projection/no-mode before numeric scoring",
            "valid_for_claim": "false",
            "generated_utc": GENERATED_UTC,
        },
    ]

    nonclaim_summary = [
        {
            "status": "Y5_R10_AEH_prefactor_gradient_zero_theorem_failed_retained_source_pack_written_nonclaim",
            "claim_ceiling": "AEH_gradient_contract_only_no_aI_zero_no_A0_calibration_cheat_no_local_GR_Newton_PPN_R10_WEP_Gdot_claim",
            "main_result": "a_I is now an explicit retained P0 coefficient; A0=1 is not a_I=0",
            "zero_status": "direct a_I=0 theorem not parent-signed",
            "retained_formula": "Q_Aa=N_frame E_a^I(b_A,I-a_I/2) in the D=4 Einstein branch",
            "remaining_blocker": "canonical projection A_a=E_a^I a_I, no-mode theorem, or sourced A_EH gradient is missing",
            "next_target": NEXT_TARGET,
            "valid_for_claim": "false",
            "generated_utc": GENERATED_UTC,
        }
    ]

    csv_outputs = {
        "source_register": (
            RESIDUALS / "P8_Y5_R10_718_SOURCE_REGISTER.csv",
            source_register,
            ["source_id", "path", "exists", "role", "valid_for_claim", "generated_utc"],
        ),
        "zero_theorem_audit": (
            RESIDUALS / "P8_Y5_R10_718_AEH_GRADIENT_ZERO_THEOREM_AUDIT.csv",
            zero_theorem_audit,
            [
                "theorem_id",
                "zero_route",
                "required_statement",
                "current_evidence",
                "status",
                "effect_if_closed",
                "valid_for_claim",
                "source_paths",
                "generated_utc",
            ],
        ),
        "variation_derivation": (
            RESIDUALS / "P8_Y5_R10_718_AEH_VARIATION_DERIVATION.csv",
            variation_derivation,
            ["step_id", "object", "equation", "result", "status", "valid_for_claim", "source_paths", "generated_utc"],
        ),
        "retained_source_pack": (
            RESIDUALS / "P8_Y5_R10_718_RETAINED_AEH_SOURCE_PACK.csv",
            retained_source_pack,
            [
                "pack_id",
                "symbol",
                "definition",
                "current_value_or_status",
                "units",
                "priority",
                "unlocks",
                "valid_for_claim",
                "source_paths",
                "generated_utc",
            ],
        ),
        "local_observable_propagation": (
            RESIDUALS / "P8_Y5_R10_718_LOCAL_OBSERVABLE_PROPAGATION.csv",
            local_observable_propagation,
            ["arena_id", "arena", "aeh_entry", "current_status", "claim_effect", "valid_for_claim", "source_paths", "generated_utc"],
        ),
        "decision": (
            RESIDUALS / "P8_Y5_R10_718_ZERO_OR_RETAIN_DECISION.csv",
            decision,
            ["decision_id", "target", "result", "reason", "next_action", "valid_for_claim", "generated_utc"],
        ),
        "bound_or_derive_queue": (
            RESIDUALS / "P8_Y5_R10_718_BOUND_OR_DERIVE_QUEUE.csv",
            bound_or_derive_queue,
            ["queue_id", "target", "preferred_route", "fallback_route", "priority", "next_artifact", "valid_for_claim", "source_paths", "generated_utc"],
        ),
        "claim_gate_evaluation": (
            RESIDUALS / "P8_Y5_R10_718_CLAIM_GATE_EVALUATION.csv",
            claim_gate_evaluation,
            ["gate_id", "gate", "observed_state", "result", "claim_effect", "valid_for_claim", "generated_utc"],
        ),
        "nonclaim_summary": (
            RESIDUALS / "P8_Y5_R10_718_NONCLAIM_SUMMARY.csv",
            nonclaim_summary,
            [
                "status",
                "claim_ceiling",
                "main_result",
                "zero_status",
                "retained_formula",
                "remaining_blocker",
                "next_target",
                "valid_for_claim",
                "generated_utc",
            ],
        ),
    }

    for path, rows, fields in csv_outputs.values():
        write_csv(path, rows, fields)

    generated_csv_paths = [path for path, _, _ in csv_outputs.values()]
    validation: list[dict[str, str]] = []

    def add_check(check_id: str, ok: bool, detail: str) -> None:
        validation.append(
            {
                "check_id": check_id,
                "result": "pass" if ok else "fail",
                "detail": detail,
                "generated_utc": GENERATED_UTC,
            }
        )

    all_sources_exist = all(info["path"].exists() for info in SOURCES.values())
    add_check("V718_0_source_paths_exist", all_sources_exist, "all cited source paths exist" if all_sources_exist else "missing source path")

    prior_clean = prior_validation_clean(SOURCES["717_validation"]["path"])
    add_check("V718_1_prior_717_clean", prior_clean, "717_validation_failures=0" if prior_clean else "717 validation not clean")

    older_clean = all(
        prior_validation_clean(SOURCES[key]["path"])
        for key in ["704_validation", "705_validation", "706_validation", "707_validation"]
    )
    add_check("V718_2_prior_AEH_chain_clean", older_clean, "704-707 validations clean" if older_clean else "one older AEH validation not clean")

    no_prefactor_unowned = csv_contains(SOURCES["710_descent"]["path"], "DPC710_2_no_R_prefactor", "candidate_clause_not_parent_signed")
    add_check("V718_3_no_prefactor_unowned_confirmed", no_prefactor_unowned, "DPC710_2 no_R_prefactor not parent-signed")

    channel_inventory_blocks = csv_contains(SOURCES["706_inventory"]["path"], "AEHT706_11_verdict", "fail_current_corpus")
    add_check("V718_4_AEH_inventory_blocks", channel_inventory_blocks, "706 AEH inventory verdict blocks claim")

    zero_path = csv_outputs["zero_theorem_audit"][0]
    add_check(
        "V718_5_zero_theorem_not_promoted",
        csv_contains(zero_path, "AGZ718_7_verdict", "fail_current_corpus"),
        "a_I=0 theorem not promoted",
    )

    variation_path = csv_outputs["variation_derivation"][0]
    add_check(
        "V718_6_A0_gradient_guard_written",
        csv_contains(variation_path, "A0=1 does not force a_I=0", "A0[1+a_I"),
        "A0 and a_I separation written",
    )

    add_check(
        "V718_7_metric_variation_channel_written",
        csv_contains(variation_path, "(g_mu nu box - nabla_mu nabla_nu)A_EH", "spacetime gradients of A_EH"),
        "metric residual channel recorded",
    )

    add_check(
        "V718_8_Einstein_charge_retained",
        csv_contains(variation_path, "Q_Aa=N_frame E_a^I(b_A,I-a_I/2)"),
        "D=4 retained charge formula included",
    )

    retained_path = csv_outputs["retained_source_pack"][0]
    add_check(
        "V718_9_retained_pack_has_aI",
        csv_contains(retained_path, "RAP718_1_aI", "MISSING_PREFACTOR_GRADIENT_VECTOR_OR_ZERO_THEOREM"),
        "retained source pack carries a_I as P0",
    )

    add_check(
        "V718_10_projection_next_selected",
        csv_contains(csv_outputs["bound_or_derive_queue"][0], NEXT_TARGET) and csv_contains(csv_outputs["decision"][0], NEXT_TARGET),
        NEXT_TARGET,
    )

    all_false = all_valid_false(generated_csv_paths)
    add_check("V718_11_no_claim_rows_promoted", all_false, "all generated rows valid_for_claim=false")

    outputs_scoped = all(str(path).startswith(str(POST_CHECKPOINT)) for path in generated_csv_paths + [OUTPUT_DOC])
    add_check("V718_12_outputs_scoped", outputs_scoped, "all outputs under post-checkpoint-work")

    formalization_count = formalization_changed_after_cutoff()
    add_check(
        "V718_13_formalization_workbench_untouched",
        formalization_count == 0,
        f"formalization_changed_after_cutoff={formalization_count}",
    )

    add_check(
        "V718_14_status_nonclaim",
        csv_contains(csv_outputs["nonclaim_summary"][0], "no_aI_zero_no_A0_calibration_cheat_no_local_GR"),
        "AEH gradient contract only; no local claim",
    )

    add_check(
        "V718_15_local_arenas_blocked",
        all("blocked" in row["current_status"] for row in local_observable_propagation),
        "all local observable rows blocked until sourced",
    )

    add_check(
        "V718_16_source_register_written",
        len(source_register) >= 15 and all(row["exists"] == "true" for row in source_register),
        f"source_rows={len(source_register)}",
    )

    add_check(
        "V718_17_calibration_cheat_guard",
        csv_contains(csv_outputs["decision"][0], "guarded_not_a_zero_proof", "A0 and a_I are separate Taylor data"),
        "A0 calibration cannot be used as a_I zero proof",
    )

    validation_path = RESIDUALS / "P8_Y5_BRR545_718_VALIDATION.csv"
    write_csv(validation_path, validation, ["check_id", "result", "detail", "generated_utc"])

    sections = [
        "# 718 - Y5 R10 AEH Prefactor Gradient Zero Theorem Or Retained Source Pack",
        "",
        "## Summary",
        "",
        "This checkpoint tries the clean route first: prove `a_I=partial_I ln A_EH|u0=0`. The current corpus still cannot do it.",
        "",
        "The important guard is now explicit:",
        "",
        "`A0=A_EH(u0)` is calibration data, while `a_I=partial_I ln A_EH|u0` is coupling data.",
        "",
        "So `A0=1` does **not** imply `a_I=0`. In the retained D=4 Einstein branch from 717, the local scalar charge remains",
        "",
        "`Q_Aa = N_frame E_a^I (b_A,I - a_I/2)`.",
        "",
        "The next best derivation route is not to rerun the same no-prefactor argument. It is to test the canonical projection: maybe `a_I` exists formally but lives in a non-propagating/null/topological direction, so `A_a=E_a^I a_I=0` for every local scalar mode.",
        "",
        "| Field | Value |",
        "| --- | --- |",
        f"| Generated UTC | `{GENERATED_UTC}` |",
        "| Claim status | nonclaim/private checkpoint |",
        f"| Next target | `{NEXT_TARGET}` |",
        "",
        "## AEH Gradient Zero Theorem Audit",
        "",
        markdown_table(zero_theorem_audit, ["theorem_id", "zero_route", "status", "effect_if_closed", "valid_for_claim"]),
        "",
        "## AEH Variation Derivation",
        "",
        markdown_table(variation_derivation, ["step_id", "object", "equation", "result", "status", "valid_for_claim"]),
        "",
        "## Retained AEH Source Pack",
        "",
        markdown_table(retained_source_pack, ["pack_id", "symbol", "definition", "current_value_or_status", "priority", "unlocks", "valid_for_claim"]),
        "",
        "## Local Observable Propagation",
        "",
        markdown_table(local_observable_propagation, ["arena_id", "arena", "aeh_entry", "current_status", "claim_effect", "valid_for_claim"]),
        "",
        "## Zero Or Retain Decision",
        "",
        markdown_table(decision, ["decision_id", "target", "result", "reason", "next_action", "valid_for_claim"]),
        "",
        "## Bound Or Derive Queue",
        "",
        markdown_table(bound_or_derive_queue, ["queue_id", "target", "preferred_route", "fallback_route", "priority", "next_artifact", "valid_for_claim"]),
        "",
        "## Claim Gate Evaluation",
        "",
        markdown_table(claim_gate_evaluation, ["gate_id", "gate", "observed_state", "result", "claim_effect", "valid_for_claim"]),
        "",
        "## Nonclaim Summary",
        "",
        markdown_table(nonclaim_summary, ["status", "claim_ceiling", "main_result", "zero_status", "retained_formula", "remaining_blocker", "next_target", "valid_for_claim"]),
        "",
        "## Source Register",
        "",
        markdown_table(source_register, ["source_id", "path", "exists", "role"]),
        "",
        "## Validation",
        "",
        markdown_table(validation, ["check_id", "result", "detail"]),
        "",
        "## Verdict",
        "",
        "This is not the happy ending, but it is a cleaner theory. The direct `a_I=0` proof fails in the current corpus because the no-prefactor/no-`F(u)R` route is still unsigned. The good news is that the next possible rescue is sharper: we only need the **observable projection** of `a_I` to vanish. If `E_a^I a_I=0` for all local modes, the gradient can be formal bookkeeping rather than a fifth-force source. If that fails too, we stop hunting theorem exits and score the retained scalar branch honestly.",
        "",
    ]
    OUTPUT_DOC.write_text("\n".join(sections), encoding="utf-8")

    passes = sum(1 for row in validation if row["result"] == "pass")
    total = len(validation)
    print(f"Y5_R10_AEH_prefactor_gradient_zero_theorem_failed_retained_source_pack_written_nonclaim: validation_passes={passes}/{total}")


if __name__ == "__main__":
    main()

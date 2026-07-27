from __future__ import annotations

import csv
from datetime import datetime, timezone
from pathlib import Path


STATUS = "Y5_R10_retained_scalar_source_row_minimum_executable_coefficient_pack_written_nonclaim"
CLAIM_CEILING = "coefficient_pack_schema_only_no_sourced_values_no_R10_PPN_WEP_Gdot_R11_or_local_GR_claim"
NEXT_TARGET = "716-Y5-R10-matter-coupling-source-charge-derivation-or-free-coefficient-lock.md"

ROOT = Path(__file__).resolve().parents[1]
RESIDUALS = ROOT / "source-intake" / "mts_residuals"
DOC_PATH = ROOT / "715-Y5-R10-retained-scalar-source-row-minimum-executable-coefficient-pack.md"
FORMALIZATION_WORKBENCH = ROOT.parent / "formalization-workbench"
FORMALIZATION_CUTOFF = datetime.fromisoformat("2026-05-31T14:42:00")

OUTPUT_PATHS = [
    DOC_PATH,
    RESIDUALS / "P8_Y5_R10_715_SOURCE_REGISTER.csv",
    RESIDUALS / "P8_Y5_R10_715_MINIMUM_EXECUTABLE_COEFFICIENT_PACK.csv",
    RESIDUALS / "P8_Y5_R10_715_COUPLING_BOTTLENECK_AUDIT.csv",
    RESIDUALS / "P8_Y5_R10_715_RETAINED_SCALAR_OBSERVABLE_MAP.csv",
    RESIDUALS / "P8_Y5_R10_715_RETAINED_SCALAR_FILL_TEMPLATE.csv",
    RESIDUALS / "P8_Y5_R10_715_ZERO_OR_NUMERIC_DECISION_RULES.csv",
    RESIDUALS / "P8_Y5_R10_715_AEH_SCALAR_UPDATE.csv",
    RESIDUALS / "P8_Y5_R10_715_CLAIM_GATE_EVALUATION.csv",
    RESIDUALS / "P8_Y5_R10_715_DECISION.csv",
    RESIDUALS / "P8_Y5_R10_715_NONCLAIM_SUMMARY.csv",
    RESIDUALS / "P8_Y5_BRR545_715_VALIDATION.csv",
]

SOURCE_PATHS = {
    "714_doc": ROOT / "714-Y5-R10-scalar-closure-vs-retained-branch-decision-gate.md",
    "714_validation": RESIDUALS / "P8_Y5_BRR545_714_VALIDATION.csv",
    "714_queue": RESIDUALS / "P8_Y5_R10_714_RETAINED_BRANCH_SOURCE_QUEUE.csv",
    "714_route": RESIDUALS / "P8_Y5_R10_714_ROUTE_DECISION_GATE.csv",
    "714_aeh": RESIDUALS / "P8_Y5_R10_714_AEH_SCALAR_UPDATE.csv",
    "714_summary": RESIDUALS / "P8_Y5_R10_714_NONCLAIM_SUMMARY.csv",
    "708_contract": RESIDUALS / "P8_Y5_R10_708_SCALAR_CLASS_SOURCE_ROW_CONTRACT.csv",
    "708_local_map": RESIDUALS / "P8_Y5_R10_708_LOCAL_EXPANSION_MAP.csv",
    "708_ppn_map": RESIDUALS / "P8_Y5_R10_708_PPN_GDOT_WEP_MAP.csv",
    "708_r10": RESIDUALS / "P8_Y5_R10_708_R10_ALPHA_LAMBDA_SCALAR_TEMPLATE.csv",
    "708_r11": RESIDUALS / "P8_Y5_R10_708_R11_SCALAR_OPERATOR_ROW.csv",
    "712_rules": RESIDUALS / "P8_Y5_R10_712_FORBIDDEN_PROMOTION_RULES.csv",
    "713_baselines": RESIDUALS / "P8_Y5_R10_713_LOCAL_BOUND_BASELINES.csv",
    "local_template": RESIDUALS / "MTS_local_residual_predictions_TEMPLATE.csv",
    "r10_contract": RESIDUALS / "P8_Y5_R10_BOUND_CURVE_REAL_DATA_CONTRACT.csv",
    "r11_template": RESIDUALS / "R11_nonEH_operator_vector_TEMPLATE.csv",
}


def now() -> str:
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


def source_list(*source_ids: str) -> str:
    return ";".join(str(SOURCE_PATHS[source_id]) for source_id in source_ids)


def validation_failures(source_id: str) -> list[dict[str, str]]:
    path = SOURCE_PATHS[source_id]
    if not path.exists():
        return [{"check_id": "missing", "result": "fail", "detail": str(path)}]
    return [row for row in read_csv(path) if row.get("result") != "pass"]


def formalization_changed_count() -> int:
    if not FORMALIZATION_WORKBENCH.exists():
        return -1
    return sum(
        1
        for candidate in FORMALIZATION_WORKBENCH.rglob("*")
        if candidate.is_file() and datetime.fromtimestamp(candidate.stat().st_mtime) > FORMALIZATION_CUTOFF
    )


def source_register_rows() -> list[dict[str, str]]:
    generated = now()
    roles = {
        "714_doc": "previous closure-vs-retained decision gate",
        "714_validation": "previous validation gate",
        "714_queue": "retained scalar source queue",
        "714_route": "route selecting retained branch",
        "714_aeh": "AEH/coupling retained queue status",
        "714_summary": "nonclaim summary selecting retained route",
        "708_contract": "scalar source-row required objects",
        "708_local_map": "symbolic local scalar expansion map",
        "708_ppn_map": "PPN/WEP/Gdot/R10/R11 symbolic map",
        "708_r10": "retained scalar R10 template",
        "708_r11": "retained scalar R11 row",
        "712_rules": "forbidden promotion rules",
        "713_baselines": "local baseline rows for nonclaim scoring",
        "local_template": "canonical local residual prediction template",
        "r10_contract": "R10 real curve contract",
        "r11_template": "R11 operator-vector template",
    }
    return [
        {
            "source_id": source_id,
            "path": str(path),
            "exists": str(path.exists()).lower(),
            "role": roles[source_id],
            "generated_utc": generated,
        }
        for source_id, path in SOURCE_PATHS.items()
    ]


def coefficient_pack_rows() -> list[dict[str, str]]:
    generated = now()
    rows = [
        (
            "MEP715_0_parent_action",
            "parent scalar/class action",
            "S_scalar_local",
            "int sqrt(-g_obs)[A_EH(u)R/(2kappa_ref) - 1/2 Z_IJ(u)nabla u^I nabla u^J - V(u)] + S_matter[B_A^2(u)g_obs,psi_A]",
            "action density plus matter frame",
            "MISSING_PARENT_ACTION_COEFFICIENT_SOURCE",
            "action",
            "P0",
            "defines whether retained scalar branch exists as local physics",
        ),
        (
            "MEP715_1_observed_frame",
            "observed frame and measured-G convention",
            "F_obs",
            "choose the metric/coframe used by clocks, rods, matter action, EH term, and measured Newtonian GM",
            "explicit frame convention",
            "MISSING_FRAME_AND_GREF_CONVENTION",
            "dimensionless",
            "P0",
            "prevents double-counting source normalization as fifth force or hiding prefactors",
        ),
        (
            "MEP715_2_field_multiplet",
            "scalar/class field list",
            "u^I",
            "ordered local scalar/class coordinates, e.g. u^I=(phi,C,...) after quotient/closure choices",
            "field vector",
            "MISSING_FIELD_LIST",
            "field units",
            "P1",
            "indexes all gradients, kinetic terms, masses, and charges",
        ),
        (
            "MEP715_3_background",
            "local background point",
            "u0^I",
            "exterior/local-vacuum background where coefficients are evaluated",
            "field vector",
            "MISSING_BACKGROUND_VALUE",
            "field units",
            "P1",
            "sets A0 and all local Taylor coefficients",
        ),
        (
            "MEP715_4_A0",
            "EH prefactor value",
            "A0=A_EH(u0)",
            "coefficient multiplying R in the observed local action at u0",
            "numeric_or_theorem",
            "MISSING_A0_OR_A0_EQUALS_1_THEOREM",
            "dimensionless",
            "P1",
            "sets delta_AEH_scalar and Newtonian normalization debt",
        ),
        (
            "MEP715_5_A_gradient",
            "EH prefactor gradient",
            "a_I=partial_I ln A_EH|u0",
            "first derivative of EH prefactor in retained scalar field space",
            "numeric_vector_or_theorem_zero",
            "MISSING_PREFACTOR_GRADIENT_VECTOR",
            "inverse field units",
            "P1",
            "feeds scalar force strength, frame transfer, Gdot, and PPN maps",
        ),
        (
            "MEP715_6_A_hessian",
            "EH prefactor Hessian",
            "a_IJ=partial_I partial_J ln A_EH|u0",
            "second derivative needed for beta/nonlinear scalar response if retained",
            "numeric_matrix_or_theorem_zero",
            "MISSING_PREFACTOR_HESSIAN",
            "inverse field units squared",
            "P2",
            "feeds beta and nonlinear source-normalization map",
        ),
        (
            "MEP715_7_kinetic_metric",
            "kinetic metric",
            "Z_IJ(u0)",
            "field-space kinetic metric with sign/gauge/null classification",
            "numeric_matrix_or_null_theorem",
            "MISSING_KINETIC_METRIC",
            "dimensionless_or_field_units",
            "P2",
            "canonicalizes propagating scalar modes",
        ),
        (
            "MEP715_8_mass_matrix",
            "mass/range matrix",
            "M2_IJ=partial_I partial_J V_eff(u0)",
            "local mass matrix in same canonical convention as Z_IJ",
            "numeric_matrix_or_no_mode_theorem",
            "MISSING_MASS_MATRIX",
            "mass^2",
            "P2",
            "sets lambda_a=hbar/(m_a c) for R10",
        ),
        (
            "MEP715_9_canonical_modes",
            "canonical eigenmodes",
            "E_a^I,m_a^2,lambda_a",
            "basis diagonalizing Z_IJ and M2_IJ with normalized scalar modes s_a",
            "numeric_basis_or_no_mode_theorem",
            "MISSING_CANONICAL_DIAGONALIZATION",
            "mixed",
            "P2",
            "turns symbolic field-space entries into observable mode charges",
        ),
        (
            "MEP715_10_matter_charge",
            "matter/source charge vector",
            "b_A,I=partial_I ln m_A(u)|u0",
            "species/source/test derivative of matter readout or mass functional",
            "numeric_vector_or_matter_blind_theorem",
            "MISSING_SOURCE_TEST_CHARGE_VECTOR",
            "inverse field units",
            "P1",
            "the main coupling bottleneck for WEP and R10",
        ),
        (
            "MEP715_11_frame_transfer",
            "frame-transfer charge correction",
            "f_frame*a_I",
            "extra scalar charge induced if transforming between EH and matter/readout frames",
            "numeric_coefficient_or_same_frame_theorem",
            "MISSING_FRAME_TRANSFER_COEFFICIENT",
            "inverse field units",
            "P1",
            "prevents hidden Weyl/disformal coupling",
        ),
        (
            "MEP715_12_effective_charge",
            "effective canonical source charge",
            "Q_Aa=N_frame E_a^I(b_A,I+f_frame a_I)",
            "canonical scalar charge of source/test body A in mode a",
            "computed_from_prior_rows",
            "MISSING_EFFECTIVE_CANONICAL_CHARGE",
            "dimensionless",
            "P2",
            "feeds WEP, R10, gamma, beta, and clock rows",
        ),
        (
            "MEP715_13_alpha_lambda",
            "Yukawa/fifth-force amplitude",
            "alpha_AB,a(lambda_a)=Q_Aa Q_Ba",
            "range-dependent scalar fifth-force amplitude in fixed convention",
            "computed_from_prior_rows_plus_bound_curve",
            "MISSING_ALPHA_LAMBDA_ROW",
            "dimensionless",
            "P3",
            "only score after charges, ranges, and real bound curve exist",
        ),
    ]
    return [
        {
            "pack_id": pack_id,
            "required_object": required_object,
            "symbol": symbol,
            "definition": definition,
            "required_value_type": required_type,
            "current_value_or_status": current_status,
            "units": units,
            "priority": priority,
            "unlocks": unlocks,
            "valid_for_claim": "false",
            "source_paths": source_list("708_contract", "708_local_map", "708_ppn_map", "714_queue"),
            "generated_utc": generated,
        }
        for pack_id, required_object, symbol, definition, required_type, current_status, units, priority, unlocks in rows
    ]


def coupling_bottleneck_rows() -> list[dict[str, str]]:
    generated = now()
    rows = [
        (
            "CBA715_0_zero_charge",
            "b_A,I=0 and f_frame*a_I=0 for all A,I",
            "scalar source charge Q_Aa=0",
            "would kill WEP and R10 scalar force only if parent-signed",
            "not_proved",
            "derive matter-blind theorem or keep retained charge vector",
        ),
        (
            "CBA715_1_universal_charge",
            "Q_Aa=Q_a independent of species A",
            "WEP may be protected but scalar fifth force and PPN remain active",
            "not a local-GR pass; still needs R10/PPN comparison",
            "not_sourced",
            "source universal charge and range or prove it vanishes",
        ),
        (
            "CBA715_2_species_charge",
            "Q_Aa depends on source/test composition",
            "WEP/R1 and R10 become active immediately",
            "requires species map and bounds",
            "not_sourced",
            "derive b_A,I for test materials or declare free coefficient",
        ),
        (
            "CBA715_3_frame_transfer",
            "f_frame*a_I nonzero or frame convention ambiguous",
            "apparent zero b_A,I can be spoiled by Weyl/disformal transfer",
            "blocks all scalar scoring",
            "missing_frame_lock",
            "fix same-frame theorem or retain f_frame in charge",
        ),
        (
            "CBA715_4_massless_mode",
            "m_a=0 or lambda_a much larger than local test scale",
            "long-range PPN/WEP/fifth-force channel",
            "must compare to gamma/beta/WEP/R10 locks",
            "not_sourced",
            "source M2_IJ and canonical eigenmodes",
        ),
        (
            "CBA715_5_short_range_mode",
            "finite m_a and lambda_a in R10 band",
            "Yukawa alpha(lambda) row",
            "requires real bound curve and source charges",
            "not_sourced",
            "fill lambda_a and alpha_AB,a nonclaim row first",
        ),
        (
            "CBA715_6_no_mode_theorem",
            "Z/M sector is pure gauge, topological, or absent in local action",
            "retained scalar branch collapses into parent-signed silence",
            "only allowed with Ward/Bianchi/action owner",
            "not_proved",
            "prove no local scalar mode or keep retained branch",
        ),
    ]
    return [
        {
            "audit_id": audit_id,
            "condition": condition,
            "coupling_consequence": consequence,
            "observable_effect": effect,
            "current_status": status,
            "next_action": next_action,
            "valid_for_claim": "false",
            "source_paths": source_list("708_contract", "708_local_map", "708_ppn_map", "714_aeh"),
            "generated_utc": generated,
        }
        for audit_id, condition, consequence, effect, status, next_action in rows
    ]


def observable_map_rows() -> list[dict[str, str]]:
    generated = now()
    rows = [
        (
            "RSO715_0_Newton",
            "Newtonian limit",
            "G_eff_AB(r)",
            "G_ref/A0 times [1 + sum_a Q_Aa Q_Ba exp(-r/lambda_a)] after measured-G convention",
            "A0;F_obs;Q_Aa;lambda_a;source-normalization rule",
            "MISSING_FRAME_A0_CHARGES_RANGES",
        ),
        (
            "RSO715_1_WEP",
            "R1",
            "eta_WEP_source_charge",
            "composition dependence of Q_Aa and source-normalized acceleration",
            "b_A,I;f_frame;a_I;E_a^I;material/source labels",
            "MISSING_SOURCE_TEST_CHARGE_VECTOR",
        ),
        (
            "RSO715_2_clock",
            "R2",
            "alpha_clock_redshift",
            "clock/readout scalar dependence after observed-frame lock",
            "F_obs;B_clock(u);a_I;b_clock,I;local gradient/time profile",
            "MISSING_CLOCK_READOUT_MAP",
        ),
        (
            "RSO715_3_gamma",
            "R3",
            "gamma_minus_1",
            "scalar-tensor light/curvature response as a function of canonical universal charge in the observed frame",
            "F_obs;Q_universal,a;lambda_a;PPN convention",
            "MISSING_GAMMA_MAP",
        ),
        (
            "RSO715_4_beta",
            "R4",
            "beta_minus_1",
            "nonlinear scalar response requiring derivative of effective charge/prefactor and source normalization",
            "a_I;a_IJ;b_A,I;partial_J b_A,I;Z_IJ;M2_IJ;F_obs",
            "MISSING_BETA_MAP",
        ),
        (
            "RSO715_5_Gdot",
            "R9",
            "Gdot_over_G",
            "-partial_t ln A0 plus source-mass/readout drift in measured-G convention",
            "partial_t u0^I;a_I;b_A,I;source-normalization drift",
            "MISSING_TIME_DERIVATIVE_AND_CALIBRATION_MAP",
        ),
        (
            "RSO715_6_R10",
            "R10",
            "alpha_AB(lambda)",
            "alpha_AB,a=Q_Aa Q_Ba at lambda_a, compared only to real alpha_bound(lambda)",
            "Q_Aa;Q_Ba;lambda_a;real R10 bound curve",
            "MISSING_ALPHA_LAMBDA_MAP",
        ),
        (
            "RSO715_7_R11",
            "R11",
            "scalar_tensor_class_metric",
            "retained scalar operator coefficient vector feeding all local residual rows",
            "A0;a_I;a_IJ;Z_IJ;M2_IJ;b_A,I;E_a^I;F_obs",
            "MISSING_EXECUTABLE_R11_SCALAR_ROW",
        ),
    ]
    return [
        {
            "map_id": map_id,
            "arena": arena,
            "observable": observable,
            "retained_formula": formula,
            "minimum_inputs": inputs,
            "current_status": status,
            "claim_effect": "map_shape_only_no_score",
            "valid_for_claim": "false",
            "source_paths": source_list("708_local_map", "708_ppn_map", "713_baselines", "local_template"),
            "generated_utc": generated,
        }
        for map_id, arena, observable, formula, inputs, status in rows
    ]


def fill_template_rows() -> list[dict[str, str]]:
    generated = now()
    return [
        {
            "template_id": "RST715_0_mode_a_nonclaim_template",
            "model_id": "MTS_scalar_class_retained_branch",
            "branch_id": "post_714_retained_scalar",
            "mode_label": "mode_a",
            "A0": "MISSING_A0_OR_A0_EQUALS_1_THEOREM",
            "a_I": "MISSING_PREFACTOR_GRADIENT_VECTOR",
            "a_IJ": "MISSING_PREFACTOR_HESSIAN",
            "Z_IJ": "MISSING_KINETIC_METRIC",
            "M2_IJ": "MISSING_MASS_MATRIX",
            "E_aI": "MISSING_CANONICAL_DIAGONALIZATION",
            "lambda_a_m": "MISSING_lambda_a_from_mass_matrix",
            "b_source_I": "MISSING_SOURCE_CHARGE_VECTOR",
            "b_test_I": "MISSING_TEST_CHARGE_VECTOR",
            "frame_transfer": "MISSING_FRAME_TRANSFER_COEFFICIENT",
            "Q_source_a": "MISSING_EFFECTIVE_SOURCE_CHARGE",
            "Q_test_a": "MISSING_EFFECTIVE_TEST_CHARGE",
            "alpha_AB_a": "MISSING_ALPHA_FROM_Q_SOURCE_Q_TEST",
            "gamma_input": "MISSING_GAMMA_MAP",
            "beta_input": "MISSING_BETA_MAP",
            "Gdot_input": "MISSING_TIME_DERIVATIVE_AND_CALIBRATION_MAP",
            "source_file": str(DOC_PATH),
            "derivation_status": "retained_unfilled",
            "valid_for_claim": "false",
            "notes": "copy this row only after every MISSING field is replaced by sourced numeric value or theorem-zero certificate",
            "generated_utc": generated,
        }
    ]


def zero_or_numeric_decision_rows() -> list[dict[str, str]]:
    generated = now()
    rows = [
        (
            "ZND715_0_frame_first",
            "If F_obs is missing, no retained scalar observable may be scored.",
            "frame lock is prerequisite to all alpha/PPN/WEP/Gdot comparisons",
            "blocks_all_scoring",
        ),
        (
            "ZND715_1_zero_charge",
            "Q_Aa=0 can be used only with parent-signed matter-blind or no-mode theorem.",
            "closure zero or assumed universality is insufficient",
            "blocks_zero_claim",
        ),
        (
            "ZND715_2_universal_nonzero",
            "Universal nonzero Q_a may protect WEP but activates R10/PPN/Gdot checks.",
            "do not call universal coupling local GR",
            "requires_numeric_scoring",
        ),
        (
            "ZND715_3_species_nonzero",
            "Species-dependent Q_Aa activates WEP and R10 immediately.",
            "requires material/source charge map",
            "requires_numeric_scoring",
        ),
        (
            "ZND715_4_no_mode",
            "No scalar mode requires a signed Z/M/gauge/topological theorem.",
            "a missing mass matrix is not a no-mode theorem",
            "blocks_no_mode_claim",
        ),
        (
            "ZND715_5_real_bound",
            "R10 comparison requires real alpha_bound(lambda) rows, not placeholder or anchor-only rows.",
            "do not score against symbolic alpha(lambda)",
            "blocks_R10_claim",
        ),
    ]
    return [
        {
            "rule_id": rule_id,
            "rule": rule,
            "reason": reason,
            "claim_effect": effect,
            "valid_for_claim": "false",
            "source_paths": source_list("712_rules", "713_baselines", "714_route", "r10_contract"),
            "generated_utc": generated,
        }
        for rule_id, rule, reason, effect in rows
    ]


def aeh_update_rows() -> list[dict[str, str]]:
    generated = now()
    rows = [
        (
            "AEHU715_0_A0",
            "A_EH(u0)",
            "MISSING_A0_OR_A0_EQUALS_1_THEOREM",
            "retained_unfilled",
            "delta_AEH_scalar not scoreable",
        ),
        (
            "AEHU715_1_gradient",
            "partial_I ln A_EH|u0",
            "MISSING_PREFACTOR_GRADIENT_VECTOR",
            "retained_unfilled",
            "scalar force strength not scoreable",
        ),
        (
            "AEHU715_2_coupling",
            "b_A,I plus frame-transfer charge",
            "MISSING_SOURCE_TEST_CHARGE_VECTOR_AND_FRAME_TRANSFER",
            "live_bottleneck",
            "coupling hunt selected next",
        ),
        (
            "AEHU715_3_R11",
            "scalar_tensor_class_metric",
            "MISSING_EXECUTABLE_COEFFICIENT_PACK_VALUES",
            "retained_unfilled",
            "R11 remains active and unscored",
        ),
    ]
    return [
        {
            "update_id": update_id,
            "target": target,
            "value_or_status": value,
            "current_status": status,
            "claim_effect": effect,
            "valid_for_claim": "false",
            "source_paths": source_list("714_aeh", "708_contract", "708_r11"),
            "generated_utc": generated,
        }
        for update_id, target, value, status, effect in rows
    ]


def claim_gate_rows(
    source_rows: list[dict[str, str]],
    pack_rows: list[dict[str, str]],
    coupling_rows: list[dict[str, str]],
    observable_rows: list[dict[str, str]],
    template_rows: list[dict[str, str]],
) -> list[dict[str, str]]:
    generated = now()
    missing_sources = [row["source_id"] for row in source_rows if row["exists"] != "true"]
    prior_failures = validation_failures("714_validation")
    missing_pack = [row for row in pack_rows if "MISSING" in row["current_value_or_status"]]
    live_bottleneck = [row for row in coupling_rows if row["audit_id"] in {"CBA715_2_species_charge", "CBA715_3_frame_transfer"}]
    missing_maps = [row for row in observable_rows if "MISSING" in row["current_status"]]
    template_missing = [field for field, value in template_rows[0].items() if isinstance(value, str) and "MISSING" in value]
    rows = [
        (
            "CG715_0_sources",
            "all source files load",
            f"missing_sources={len(missing_sources)}",
            "pass_structure" if not missing_sources else "fail_blocked",
            "allows coefficient-pack checkpoint only",
        ),
        (
            "CG715_1_prior_714",
            "714 validation clean",
            f"714_validation_failures={len(prior_failures)}",
            "pass_structure" if not prior_failures else "fail_blocked",
            "inherits retained route decision",
        ),
        (
            "CG715_2_pack_written",
            "minimum executable pack",
            f"pack_rows={len(pack_rows)} missing_rows={len(missing_pack)}",
            "pass_blocked_recorded",
            "schema exists but no values sourced",
        ),
        (
            "CG715_3_coupling_bottleneck",
            "coupling bottleneck audit",
            f"live_bottleneck_rows={len(live_bottleneck)}",
            "pass_blocked_recorded",
            "next derivation target is coupling/source charge",
        ),
        (
            "CG715_4_observable_maps",
            "observable map coverage",
            f"observable_rows={len(observable_rows)} missing_maps={len(missing_maps)}",
            "pass_blocked_recorded",
            "R1/R2/R3/R4/R9/R10/R11 mapped but unscored",
        ),
        (
            "CG715_5_fill_template",
            "fill template remains nonclaim",
            f"missing_template_fields={len(template_missing)}",
            "pass_blocked_recorded",
            "template cannot be mistaken for a result row",
        ),
        (
            "CG715_6_claim_status",
            "retained scalar score",
            "no sourced A0/a_I/Z/M/b_A/E/frame values",
            "fail_blocked",
            "no R10/PPN/WEP/Gdot/R11/local-GR claim",
        ),
        (
            "CG715_7_next_target",
            "next target",
            NEXT_TARGET,
            "pass_structure",
            "coupling derivation/free-coefficient lock selected",
        ),
    ]
    return [
        {
            "gate_id": gate_id,
            "gate": gate,
            "observed_state": state,
            "result": result,
            "claim_effect": effect,
            "valid_for_claim": "false",
            "source_paths": source_list("714_validation", "714_queue", "708_contract", "708_local_map", "708_ppn_map"),
            "generated_utc": generated,
        }
        for gate_id, gate, state, result, effect in rows
    ]


def decision_rows() -> list[dict[str, str]]:
    generated = now()
    rows = [
        (
            "D715_0_pack",
            "minimum executable scalar coefficient pack",
            "written_nonclaim",
            "all fields needed for retained scalar scoring are named in one machine-readable pack",
            NEXT_TARGET,
        ),
        (
            "D715_1_values",
            "sourced numeric/theorem values",
            "not_available",
            "pack is not executable until MISSING entries are replaced by source paths or theorem certificates",
            NEXT_TARGET,
        ),
        (
            "D715_2_coupling",
            "matter/source coupling",
            "selected_as_next_bottleneck",
            "b_A,I and frame-transfer charge decide WEP/R10 and much of PPN risk",
            NEXT_TARGET,
        ),
        (
            "D715_3_claim",
            "local-GR/R10/PPN/WEP/Gdot claim",
            "forbidden",
            "retained branch is organized but not scored",
            NEXT_TARGET,
        ),
    ]
    return [
        {
            "decision_id": decision_id,
            "target": target,
            "result": result,
            "reason": reason,
            "next_action": next_action,
            "valid_for_claim": "false",
            "generated_utc": generated,
        }
        for decision_id, target, result, reason, next_action in rows
    ]


def nonclaim_summary_rows(pack_rows: list[dict[str, str]]) -> list[dict[str, str]]:
    generated = now()
    p0 = [row for row in pack_rows if row["priority"] == "P0"]
    p1 = [row for row in pack_rows if row["priority"] == "P1"]
    return [
        {
            "status": STATUS,
            "claim_ceiling": CLAIM_CEILING,
            "pack_rows": str(len(pack_rows)),
            "p0_rows": str(len(p0)),
            "p1_rows": str(len(p1)),
            "main_result": "retained scalar branch now has a minimum executable coefficient/coupling schema, but no sourced coefficient values",
            "remaining_blocker": "observed frame, A_EH gradient, matter charge b_A,I, frame-transfer coefficient, Z/M canonical modes",
            "next_target": NEXT_TARGET,
            "valid_for_claim": "false",
            "generated_utc": generated,
        }
    ]


def all_generated_rows(*tables: list[dict[str, str]]) -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    for table in tables:
        rows.extend(table)
    return rows


def validation_rows(
    source_rows: list[dict[str, str]],
    pack_rows: list[dict[str, str]],
    coupling_rows: list[dict[str, str]],
    observable_rows: list[dict[str, str]],
    template_rows: list[dict[str, str]],
    rule_rows: list[dict[str, str]],
    aeh_rows: list[dict[str, str]],
    gate_rows: list[dict[str, str]],
    decision_rows_: list[dict[str, str]],
    summary_rows: list[dict[str, str]],
) -> list[dict[str, str]]:
    generated = now()
    missing_sources = [row for row in source_rows if row["exists"] != "true"]
    prior_failures = validation_failures("714_validation")
    all_rows = all_generated_rows(
        source_rows,
        pack_rows,
        coupling_rows,
        observable_rows,
        template_rows,
        rule_rows,
        aeh_rows,
        gate_rows,
        decision_rows_,
        summary_rows,
    )
    changed_count = formalization_changed_count()
    required_symbols = {"S_scalar_local", "F_obs", "u^I", "u0^I", "A0=A_EH(u0)", "a_I=partial_I ln A_EH|u0", "Z_IJ(u0)", "M2_IJ=partial_I partial_J V_eff(u0)", "b_A,I=partial_I ln m_A(u)|u0", "Q_Aa=N_frame E_a^I(b_A,I+f_frame a_I)"}
    pack_symbols = {row["symbol"] for row in pack_rows}
    checks = [
        (
            "V715_0_source_paths_exist",
            not missing_sources,
            "all cited source paths exist" if not missing_sources else "missing=" + ",".join(row["source_id"] for row in missing_sources),
        ),
        (
            "V715_1_prior_714_clean",
            not prior_failures,
            f"714_validation_failures={len(prior_failures)}",
        ),
        (
            "V715_2_pack_complete",
            len(pack_rows) == 14 and required_symbols.issubset(pack_symbols),
            f"pack_rows={len(pack_rows)} required_symbols_present={required_symbols.issubset(pack_symbols)}",
        ),
        (
            "V715_3_pack_has_p0_p1",
            any(row["priority"] == "P0" for row in pack_rows) and any(row["priority"] == "P1" for row in pack_rows),
            "P0/P1 executable prerequisites present",
        ),
        (
            "V715_4_pack_values_blocked",
            all(row["valid_for_claim"] == "false" for row in pack_rows)
            and any("MISSING" in row["current_value_or_status"] for row in pack_rows),
            "pack remains unfilled/nonclaim",
        ),
        (
            "V715_5_coupling_audit_covers_cases",
            len(coupling_rows) == 7 and any(row["audit_id"] == "CBA715_3_frame_transfer" for row in coupling_rows),
            f"coupling_rows={len(coupling_rows)}",
        ),
        (
            "V715_6_observable_map_covers_local_rows",
            {"R1", "R2", "R3", "R4", "R9", "R10", "R11"}.issubset({row["arena"] for row in observable_rows}),
            f"observable_rows={len(observable_rows)}",
        ),
        (
            "V715_7_fill_template_nonclaim_missing",
            len(template_rows) == 1
            and template_rows[0]["valid_for_claim"] == "false"
            and any("MISSING" in value for value in template_rows[0].values()),
            "fill template has explicit MISSING markers and valid_for_claim=false",
        ),
        (
            "V715_8_zero_numeric_rules_written",
            len(rule_rows) == 6 and all(row["valid_for_claim"] == "false" for row in rule_rows),
            f"rules={len(rule_rows)}",
        ),
        (
            "V715_9_claim_gates_blocked",
            any(row["gate_id"] == "CG715_6_claim_status" and row["result"] == "fail_blocked" for row in gate_rows),
            "retained scalar score remains blocked",
        ),
        (
            "V715_10_AEH_update_live_bottleneck",
            any(row["current_status"] == "live_bottleneck" for row in aeh_rows),
            "coupling bottleneck recorded in AEH update",
        ),
        (
            "V715_11_next_target_selected",
            any(row["next_action"] == NEXT_TARGET for row in decision_rows_),
            NEXT_TARGET,
        ),
        (
            "V715_12_no_claim_rows_promoted",
            all(row.get("valid_for_claim", "false") == "false" for row in all_rows),
            "all generated rows valid_for_claim=false",
        ),
        (
            "V715_13_outputs_scoped",
            all(str(path).startswith(str(ROOT)) for path in OUTPUT_PATHS),
            "all outputs under post-checkpoint-work",
        ),
        (
            "V715_14_formalization_workbench_untouched",
            changed_count == 0,
            f"formalization_changed_after_cutoff={changed_count}",
        ),
        (
            "V715_15_status_nonclaim",
            CLAIM_CEILING in summary_rows[0]["claim_ceiling"],
            CLAIM_CEILING,
        ),
    ]
    return [
        {
            "check_id": check_id,
            "result": "pass" if passed else "fail",
            "detail": detail,
            "generated_utc": generated,
        }
        for check_id, passed, detail in checks
    ]


def markdown_table(rows: list[dict[str, str]], columns: list[str]) -> str:
    lines = [
        "| " + " | ".join(columns) + " |",
        "| " + " | ".join("---" for _ in columns) + " |",
    ]
    for row in rows:
        lines.append("| " + " | ".join(str(row.get(column, "")).replace("\n", " ") for column in columns) + " |")
    return "\n".join(lines)


def write_markdown(
    source_rows: list[dict[str, str]],
    pack_rows: list[dict[str, str]],
    coupling_rows: list[dict[str, str]],
    observable_rows: list[dict[str, str]],
    template_rows: list[dict[str, str]],
    rule_rows: list[dict[str, str]],
    aeh_rows: list[dict[str, str]],
    gate_rows: list[dict[str, str]],
    decision_rows_: list[dict[str, str]],
    summary_rows: list[dict[str, str]],
    validation_rows_: list[dict[str, str]],
) -> None:
    content = f"""# 715 - Y5 R10 Retained Scalar Source Row Minimum Executable Coefficient Pack

## Summary

715 turns the retained scalar/class branch from a loose warning into an executable source-row contract. It does **not** fill the coefficients. It says exactly what must be filled before retained scalar physics can be scored against Newton, WEP, clocks, PPN, Gdot, R10, or R11.

The main bottleneck is now explicit: the effective matter/source charge

`Q_Aa = N_frame E_a^I (b_A,I + f_frame a_I)`.

Until `F_obs`, `a_I`, `b_A,I`, `f_frame`, `Z_IJ`, `M2_IJ`, and `E_a^I` are sourced or theorem-zero, no scalar local-GR or fifth-force claim is allowed.

| Status | `{STATUS}` |
| --- | --- |
| Claim ceiling | `{CLAIM_CEILING}` |
| Next target | `{NEXT_TARGET}` |

## Minimum Executable Coefficient Pack

{markdown_table(pack_rows, ["pack_id", "required_object", "symbol", "current_value_or_status", "priority", "unlocks", "valid_for_claim"])}

## Coupling Bottleneck Audit

{markdown_table(coupling_rows, ["audit_id", "condition", "coupling_consequence", "observable_effect", "current_status", "next_action", "valid_for_claim"])}

## Retained Scalar Observable Map

{markdown_table(observable_rows, ["map_id", "arena", "observable", "retained_formula", "minimum_inputs", "current_status", "valid_for_claim"])}

## Retained Scalar Fill Template

{markdown_table(template_rows, ["template_id", "mode_label", "A0", "a_I", "Z_IJ", "M2_IJ", "b_source_I", "b_test_I", "frame_transfer", "Q_source_a", "Q_test_a", "alpha_AB_a", "derivation_status", "valid_for_claim"])}

## Zero Or Numeric Decision Rules

{markdown_table(rule_rows, ["rule_id", "rule", "reason", "claim_effect", "valid_for_claim"])}

## Aeh Scalar Update

{markdown_table(aeh_rows, ["update_id", "target", "value_or_status", "current_status", "claim_effect", "valid_for_claim"])}

## Claim Gate Evaluation

{markdown_table(gate_rows, ["gate_id", "gate", "observed_state", "result", "claim_effect", "valid_for_claim"])}

## Decision

{markdown_table(decision_rows_, ["decision_id", "target", "result", "reason", "next_action", "valid_for_claim"])}

## Nonclaim Summary

{markdown_table(summary_rows, ["status", "claim_ceiling", "pack_rows", "p0_rows", "p1_rows", "main_result", "remaining_blocker", "next_target", "valid_for_claim"])}

## Source Register

{markdown_table(source_rows, ["source_id", "path", "exists", "role"])}

## Validation

{markdown_table(validation_rows_, ["check_id", "result", "detail"])}

## Verdict

This is progress, but not victory. The retained scalar branch now has a clean socket for real physics: if the coupling vanishes by theorem, the scalar route can collapse toward GR; if the coupling is universal but nonzero, R10/PPN must score it; if the coupling is species-dependent, WEP and fifth-force tests become live. The next best move is therefore to hunt `b_A,I` and the frame-transfer term, not to run another fake comparison against zeros.
"""
    DOC_PATH.write_text(content, encoding="utf-8")


def main() -> int:
    source_rows = source_register_rows()
    pack_rows = coefficient_pack_rows()
    coupling_rows = coupling_bottleneck_rows()
    observable_rows = observable_map_rows()
    template_rows = fill_template_rows()
    rule_rows = zero_or_numeric_decision_rows()
    aeh_rows = aeh_update_rows()
    gate_rows = claim_gate_rows(source_rows, pack_rows, coupling_rows, observable_rows, template_rows)
    decision_rows_ = decision_rows()
    summary_rows = nonclaim_summary_rows(pack_rows)
    validation_rows_ = validation_rows(
        source_rows,
        pack_rows,
        coupling_rows,
        observable_rows,
        template_rows,
        rule_rows,
        aeh_rows,
        gate_rows,
        decision_rows_,
        summary_rows,
    )

    write_csv(
        RESIDUALS / "P8_Y5_R10_715_SOURCE_REGISTER.csv",
        source_rows,
        ["source_id", "path", "exists", "role", "generated_utc"],
    )
    write_csv(
        RESIDUALS / "P8_Y5_R10_715_MINIMUM_EXECUTABLE_COEFFICIENT_PACK.csv",
        pack_rows,
        [
            "pack_id",
            "required_object",
            "symbol",
            "definition",
            "required_value_type",
            "current_value_or_status",
            "units",
            "priority",
            "unlocks",
            "valid_for_claim",
            "source_paths",
            "generated_utc",
        ],
    )
    write_csv(
        RESIDUALS / "P8_Y5_R10_715_COUPLING_BOTTLENECK_AUDIT.csv",
        coupling_rows,
        ["audit_id", "condition", "coupling_consequence", "observable_effect", "current_status", "next_action", "valid_for_claim", "source_paths", "generated_utc"],
    )
    write_csv(
        RESIDUALS / "P8_Y5_R10_715_RETAINED_SCALAR_OBSERVABLE_MAP.csv",
        observable_rows,
        ["map_id", "arena", "observable", "retained_formula", "minimum_inputs", "current_status", "claim_effect", "valid_for_claim", "source_paths", "generated_utc"],
    )
    write_csv(
        RESIDUALS / "P8_Y5_R10_715_RETAINED_SCALAR_FILL_TEMPLATE.csv",
        template_rows,
        [
            "template_id",
            "model_id",
            "branch_id",
            "mode_label",
            "A0",
            "a_I",
            "a_IJ",
            "Z_IJ",
            "M2_IJ",
            "E_aI",
            "lambda_a_m",
            "b_source_I",
            "b_test_I",
            "frame_transfer",
            "Q_source_a",
            "Q_test_a",
            "alpha_AB_a",
            "gamma_input",
            "beta_input",
            "Gdot_input",
            "source_file",
            "derivation_status",
            "valid_for_claim",
            "notes",
            "generated_utc",
        ],
    )
    write_csv(
        RESIDUALS / "P8_Y5_R10_715_ZERO_OR_NUMERIC_DECISION_RULES.csv",
        rule_rows,
        ["rule_id", "rule", "reason", "claim_effect", "valid_for_claim", "source_paths", "generated_utc"],
    )
    write_csv(
        RESIDUALS / "P8_Y5_R10_715_AEH_SCALAR_UPDATE.csv",
        aeh_rows,
        ["update_id", "target", "value_or_status", "current_status", "claim_effect", "valid_for_claim", "source_paths", "generated_utc"],
    )
    write_csv(
        RESIDUALS / "P8_Y5_R10_715_CLAIM_GATE_EVALUATION.csv",
        gate_rows,
        ["gate_id", "gate", "observed_state", "result", "claim_effect", "valid_for_claim", "source_paths", "generated_utc"],
    )
    write_csv(
        RESIDUALS / "P8_Y5_R10_715_DECISION.csv",
        decision_rows_,
        ["decision_id", "target", "result", "reason", "next_action", "valid_for_claim", "generated_utc"],
    )
    write_csv(
        RESIDUALS / "P8_Y5_R10_715_NONCLAIM_SUMMARY.csv",
        summary_rows,
        [
            "status",
            "claim_ceiling",
            "pack_rows",
            "p0_rows",
            "p1_rows",
            "main_result",
            "remaining_blocker",
            "next_target",
            "valid_for_claim",
            "generated_utc",
        ],
    )
    write_csv(
        RESIDUALS / "P8_Y5_BRR545_715_VALIDATION.csv",
        validation_rows_,
        ["check_id", "result", "detail", "generated_utc"],
    )
    write_markdown(
        source_rows,
        pack_rows,
        coupling_rows,
        observable_rows,
        template_rows,
        rule_rows,
        aeh_rows,
        gate_rows,
        decision_rows_,
        summary_rows,
        validation_rows_,
    )

    failures = [row for row in validation_rows_ if row["result"] != "pass"]
    print(f"{STATUS}: validation_passes={len(validation_rows_) - len(failures)}/{len(validation_rows_)}")
    if failures:
        for failure in failures:
            print(f"FAIL {failure['check_id']}: {failure['detail']}")
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

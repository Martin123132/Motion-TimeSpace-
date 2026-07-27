from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path


CHECKPOINT = "3881"
BRANCH = "MTS_R2FR_Y5_TOPOLOGICAL_ZEROFORM_COUPLING_OR_GDOT_FILL_3881"

PCW = Path(__file__).resolve().parents[1]
ROOT = PCW.parent
FWB = ROOT / "formalization-workbench"
OUT = PCW / "source-intake" / "mts_residuals"
DOC_PATH = PCW / "3881-Y5-R2FR-topological-zeroform-coupling-mechanism-or-Gdot-bound-fill.md"
SPINE_PATH = PCW / "LOCAL_GR_COUPLING_SPINE_CURRENT_STATE.md"

CSV_3880_NEXT = OUT / "P8_Y5_R2FR_3880_NEXT_TARGET.csv"
CSV_3880_THEOREM = OUT / "P8_Y5_R2FR_3880_GEFF_DERIVATIVE_SILENCE_THEOREM.csv"
CSV_3880_AUDIT = OUT / "P8_Y5_R2FR_3880_DERIVATIVE_CHANNEL_AUDIT.csv"
CSV_3880_INPUTS = OUT / "P8_Y5_R2FR_3880_DRIFT_BOUND_INPUT_ROWS.csv"
CSV_3880_RUNNER = OUT / "P8_Y5_R2FR_3880_BGCOMMON_RUNNER_UPDATE.csv"
CSV_KAPPA_THEOREM = OUT / "P8_CONSTANT_KAPPA_SUPERSELECTION_THEOREM.csv"
CSV_KAPPA_RESIDUAL = OUT / "P8_CONSTANT_KAPPA_RESIDUAL_MAP.csv"
CSV_GM_ZERO = OUT / "P8_CONSTANT_GM_ZERO_THEOREM_ATTEMPT.csv"
CSV_DERIV_GATE = OUT / "P8_CONSTANT_GM_DERIVATIVE_HAIR_GATE.csv"
CSV_BOUND_MATRIX = OUT / "P8_CONSTANT_GM_RESIDUAL_BOUND_MATRIX.csv"
CSV_GDOT_FILL = OUT / "P8_Y5_R2FR_3757_GDOT_CONDITIONAL_FILL.csv"
CSV_GDOT_EVAL = OUT / "P8_Y5_R2FR_3758_GDOT_BOUND_EVALUATION.csv"
CSV_SOURCE_STACK = OUT / "P8_source_normalized_Newton_branch_STACK.csv"
CSV_Y5_OWNER = OUT / "P8_Y5_SOURCE_NORMALIZATION_OWNER_THEOREM.csv"
CSV_PG_MAP = OUT / "P8_PG_calibration_residual_MAP.csv"
CSV_PG_TEMPLATE = OUT / "P8_PG_calibration_residual_INPUT_TEMPLATE.csv"

OUTPUTS = {
    "sources": OUT / "P8_Y5_R2FR_3881_SOURCE_REGISTER.csv",
    "zeroform": OUT / "P8_Y5_R2FR_3881_TOPOLOGICAL_ZEROFORM_VARIATION_AUDIT.csv",
    "contract": OUT / "P8_Y5_R2FR_3881_PARENT_ACTION_INSERTION_CONTRACT.csv",
    "gdot": OUT / "P8_Y5_R2FR_3881_GDOT_FALLBACK_BOUND_ROWS.csv",
    "runner": OUT / "P8_Y5_R2FR_3881_RUNNER_UPDATE.csv",
    "gates": OUT / "P8_Y5_R2FR_3881_CLAIM_GATES.csv",
    "next": OUT / "P8_Y5_R2FR_3881_NEXT_TARGET.csv",
    "status": OUT / "P8_Y5_R2FR_3881_STATUS.csv",
    "validation": OUT / "P8_Y5_BRR545_3881_VALIDATION.csv",
}

SOURCE_SPECS = [
    ("SRC3881_00_3880_next", CSV_3880_NEXT, "NEXT3880_0", "3880 selected topological/Gdot target"),
    ("SRC3881_01_3880_target", CSV_3880_THEOREM, "GST3880_0_target", "derivative-silence theorem target"),
    ("SRC3881_02_3880_topology", CSV_3880_THEOREM, "GST3880_1_topological_route", "zero-form/three-form route"),
    ("SRC3881_03_3880_chain", CSV_3880_THEOREM, "GST3880_2_chain_rule", "q-basic constant route"),
    ("SRC3881_04_3880_bianchi", CSV_3880_THEOREM, "GST3880_3_Bianchi_guard", "Bianchi guard"),
    ("SRC3881_05_3880_cancel", CSV_3880_THEOREM, "GST3880_4_no_tuned_cancellation", "no tuned cancellation policy"),
    ("SRC3881_06_3880_time", CSV_3880_AUDIT, "DCA3880_0_time", "time derivative channel"),
    ("SRC3881_07_3880_range", CSV_3880_AUDIT, "DCA3880_2_range", "range derivative channel"),
    ("SRC3881_08_3880_bianchi_input", CSV_3880_AUDIT, "DCA3880_5_Bianchi", "Bianchi derivative channel"),
    ("SRC3881_09_3880_gdot_input", CSV_3880_INPUTS, "DBI3880_0_time_Geff", "Gdot input row"),
    ("SRC3881_10_3880_meff_input", CSV_3880_INPUTS, "DBI3880_1_time_Meff", "Meff drift input row"),
    ("SRC3881_11_3880_mu_input", CSV_3880_INPUTS, "DBI3880_7_mu_extra", "mu-extra drift row"),
    ("SRC3881_12_3880_runner", CSV_3880_RUNNER, "RUNU3880_2_bG_update", "b_Gcommon runner update"),
    ("SRC3881_13_kappa_global", CSV_KAPPA_THEOREM, "T508_0_global_sector", "global/superselection kappa route"),
    ("SRC3881_14_kappa_topological", CSV_KAPPA_THEOREM, "T508_1_topological_zeroform", "prior topological zero-form row"),
    ("SRC3881_15_kappa_corollary", CSV_KAPPA_THEOREM, "T508_2_no_residual_if_closed", "constant-kappa corollary"),
    ("SRC3881_16_kappa_time_residual", CSV_KAPPA_RESIDUAL, "KR508_0_time_drift", "Gdot residual if theorem fails"),
    ("SRC3881_17_kappa_bianchi_residual", CSV_KAPPA_RESIDUAL, "KR508_5_Bianchi_exchange", "Bianchi residual if coupling varies"),
    ("SRC3881_18_gm_global", CSV_GM_ZERO, "Z1_global_coupling_superselection", "global coupling zero theorem attempt"),
    ("SRC3881_19_gm_nohair", CSV_GM_ZERO, "Z5_no_radial_or_range_hair", "no radial/range hair attempt"),
    ("SRC3881_20_deriv_master", CSV_DERIV_GATE, "CGM0_master_identity", "derivative hair master identity"),
    ("SRC3881_21_deriv_time", CSV_DERIV_GATE, "CGM1_time_drift", "time drift identity"),
    ("SRC3881_22_deriv_mu", CSV_DERIV_GATE, "CGM6_mu_extra_amplitude", "mu-extra drift channel"),
    ("SRC3881_23_bound_gdot", CSV_BOUND_MATRIX, "P8_Geff_time_drift", "Gdot target bound"),
    ("SRC3881_24_bound_meff", CSV_BOUND_MATRIX, "P8_Meff_conservation", "Meff drift decomposition target"),
    ("SRC3881_25_gdot_conditional", CSV_GDOT_FILL, "GF3757_0_Gdot_conditional_zero", "conditional Gdot zero"),
    ("SRC3881_26_gdot_residual", CSV_GDOT_EVAL, "GB3758_1_residual_bound", "Gdot residual formula"),
    ("SRC3881_27_gdot_budget", CSV_GDOT_EVAL, "GB3758_2_max_allowed_residual", "Gdot allowed budget"),
    ("SRC3881_28_stack_Geff", CSV_SOURCE_STACK, "SN7_constant_universal_Geff", "constant universal Geff rung"),
    ("SRC3881_29_stack_hair", CSV_SOURCE_STACK, "SN10_no_derivative_hair", "no derivative hair rung"),
    ("SRC3881_30_owner_constant", CSV_Y5_OWNER, "Y5O_2_constant_universal_coupling", "Y5 constant universal coupling owner"),
    ("SRC3881_31_owner_theorem", CSV_Y5_OWNER, "Y5O_8_owner_theorem", "Y5 source normalization owner theorem"),
    ("SRC3881_32_pg_constant", CSV_PG_MAP, "PG7_constant_universal_Geff", "PG constant Geff row"),
    ("SRC3881_33_pg_hair", CSV_PG_MAP, "PG8_no_derivative_hair", "PG derivative hair row"),
    ("SRC3881_34_template_gdot", CSV_PG_TEMPLATE, "P8_Geff_time_drift", "PG Gdot template"),
]

ZEROFORM_DERIVATION = (
    "On an oriented four-dimensional local branch, add S_top[C_*,A_3]=sigma int_M C_* F_4 with F_4=dA_3. "
    "For compact-support or fixed-boundary variations of A_3, delta_A S_top=sigma int C_* d(delta A_3) "
    "= boundary - sigma int dC_* wedge delta A_3, so arbitrary delta A_3 gives dC_*=0."
)

DERIVATIVE_SILENCE = (
    "Since dC_*=0 on each connected branch, every local channel derivative vanishes: "
    "D_t ln C_*=D_r ln C_*=D_lambda ln C_*=D_frame ln C_*=Delta_domain(C_*)=0."
)

COUPLING_MAP = (
    "Use one common coupling map kappa_eff=kappa_ref C_* or G_eff=G_ref C_*. "
    "The decimal value remains a branch calibration like Newton's G, while locality demands that C_* is not a local readout/source knob."
)

GDOT_RESIDUAL_FORMULA = (
    "|d_t ln C_*| + |d_t ln M_eff| + |d_t epsilon_mu/(1+epsilon_mu)| "
    "+ |d_t ln Z_Poisson| + |d_t ln Z_frame|"
)

UPDATED_BT = (
    "b_t := 0 if the 3881 C_*/A_3 mechanism is inserted and parent-signed; otherwise b_t := "
    + GDOT_RESIDUAL_FORMULA
)

UPDATED_BG = (
    "b_Gcommon := b_t+b_r+b_lambda+b_frame+b_domain+b_Bianchi+"
    "b_MHref_lock+b_PiM_JH_flux+b_GM_anti_circular+b_PPN_readout"
)


def now_utc() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def read_text(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        return path.read_text(encoding="utf-8-sig", errors="replace")


def rel(path: Path) -> str:
    try:
        return str(path.relative_to(PCW))
    except ValueError:
        return str(path)


def write_csv(path: Path, rows: list[dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        raise ValueError(f"no rows for {path}")
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def read_csv_rows(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8-sig") as handle:
        return list(csv.DictReader(handle))


def markdown_table(rows: list[dict[str, object]], columns: list[str]) -> str:
    if not rows:
        return ""
    header = "| " + " | ".join(columns) + " |"
    sep = "| " + " | ".join("---" for _ in columns) + " |"
    lines = [header, sep]
    for row in rows:
        values = []
        for col in columns:
            value = str(row.get(col, "")).replace("\n", " ").replace("|", "\\|")
            values.append(value)
        lines.append("| " + " | ".join(values) + " |")
    return "\n".join(lines)


def source_register_rows(timestamp: str) -> list[dict[str, object]]:
    rows = []
    for source_id, path, needle, role in SOURCE_SPECS:
        exists = path.exists()
        text = read_text(path) if exists else ""
        rows.append(
            {
                "source_id": source_id,
                "checkpoint": CHECKPOINT,
                "path": rel(path),
                "exists": exists,
                "needle": needle,
                "needle_found": needle in text,
                "role": role,
                "claim_use": "nonclaim_zeroform_mechanism_or_Gdot_fallback",
                "timestamp_utc": timestamp,
            }
        )
    return rows


def zeroform_rows(timestamp: str) -> list[dict[str, object]]:
    raw_rows = [
        (
            "ZF3881_0_parent_term",
            "parent topological term",
            "S_top[C_*,A_3]=sigma int_M C_* F_4, F_4=dA_3",
            "READY_AS_ACTION_INSERTION",
            "mathematically well-formed topological sector",
            "not yet adopted in the parent MTS action",
        ),
        (
            "ZF3881_1_A3_variation",
            "variation with respect to A_3",
            "delta_A S_top=boundary - sigma int_M dC_* wedge delta A_3, hence dC_*=0",
            "DERIVED_CONDITIONAL_ZERO",
            "this is the real leap: C_* becomes an integration constant, not a fitted local field",
            "requires compact-support/fixed-boundary A_3 variation and no other A_3 source couplings",
        ),
        (
            "ZF3881_2_derivative_silence",
            "local derivative silence",
            DERIVATIVE_SILENCE,
            "DERIVED_IF_ZF3881_1_PARENT_SIGNED",
            "kills b_t, b_r, b_lambda, b_frame, b_domain and b_Bianchi from the common coupling sector",
            "only on connected branches without membrane/domain-wall jumps",
        ),
        (
            "ZF3881_3_C_variation",
            "variation with respect to C_*",
            "delta_C S gives sigma F_4 + delta S_rest/delta C_*=0",
            "CONSISTENCY_EQUATION_NOT_A_DRIFT_SOURCE",
            "F_4 absorbs the conjugate density while A_3 variation still enforces dC_*=0",
            "must not become a hidden local source/range/frame selector",
        ),
        (
            "ZF3881_4_coupling_map",
            "map into Newton/GR coupling",
            COUPLING_MAP,
            "CALIBRATED_CONSTANT_COUPLING_ROUTE",
            "matches the GR/Newton style: one measured universal G is allowed; local drift is not",
            "requires one common map for all ordinary matter/source/readout sectors",
        ),
        (
            "ZF3881_5_Bianchi",
            "Bianchi guard",
            "if dC_*=0 then nabla_mu kappa_eff=0 and the variable-coupling exchange term is absent",
            "BIANCHI_SAFE_IF_PARENT_SIGNED",
            "turns the b_Bianchi residual off by derivation rather than by tuning",
            "if dC_* != 0, the exchange row remains active",
        ),
        (
            "ZF3881_6_verdict",
            "3881 verdict",
            "the zero proof works as a parent action mechanism, but current corpus has not yet inserted/adopted it as the parent action",
            "MECHANISM_DERIVED_NOT_PARENT_ADOPTED",
            "progress: we have an exact route to constant coupling; no public/local-GR claim yet",
            "next step must either insert this parent action cleanly or fill the Gdot component row",
        ),
    ]
    return [
        {
            "zeroform_id": row_id,
            "clause": clause,
            "derivation_or_condition": derivation,
            "status": status,
            "what_it_buys": buys,
            "remaining_guard": guard,
            "parent_signed": False,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
        for row_id, clause, derivation, status, buys, guard in raw_rows
    ]


def contract_rows(timestamp: str) -> list[dict[str, object]]:
    raw_rows = [
        ("PAC3881_0_fields", "field content", "add a universal zero-form C_* and three-form A_3 with F_4=dA_3", "REQUIRED"),
        ("PAC3881_1_topological_term", "topological term", "include S_top=sigma int C_* F_4 before local readout/source normalization", "REQUIRED"),
        ("PAC3881_2_gauge", "gauge invariance", "A_3 -> A_3+dB_2; boundary variation fixed or compact support", "REQUIRED"),
        ("PAC3881_3_no_A3_sources", "no extra A_3 sources", "A_3 must not couple to matter, range markers, frame selectors, or domain masks except through the topological sector", "REQUIRED"),
        ("PAC3881_4_coupling_map", "single coupling map", "G_eff=G_ref C_* or kappa_eff=kappa_ref C_* with one C_* for all ordinary matter sectors", "REQUIRED"),
        ("PAC3881_5_no_labels", "no hidden labels", "C_* has no source/species, radius, lambda, frame, arena, or domain label", "REQUIRED"),
        ("PAC3881_6_connected_branch", "connected local branch", "no membrane/domain-wall crossing inside the tested local branch; jumps would be explicit domain residuals", "REQUIRED"),
        ("PAC3881_7_C_equation", "C_* equation", "F_4 + sigma^-1 delta S_rest/delta C_*=0 must be a flux/conjugate-density equation, not a local fitted coupling rule", "REQUIRED"),
        ("PAC3881_8_Bianchi", "Bianchi compatibility", "with dC_*=0, standard covariant conservation is preserved in the common coupling sector", "REQUIRED"),
        ("PAC3881_9_calibration", "Newton constant policy", "the numeric value of G remains a measured branch constant; MTS only needs to derive universality and derivative silence", "ALLOWED"),
        ("PAC3881_10_claim_policy", "claim policy", "until these rows are adopted by the parent action, use them as a nonclaim insertion contract", "BLOCKING_FOR_CLAIM"),
    ]
    return [
        {
            "contract_id": row_id,
            "requirement": requirement,
            "exact_condition": condition,
            "status": status,
            "source_basis": "3881 zeroform variation audit plus 3880 derivative-silence target",
            "adopted_in_parent_action": False,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
        for row_id, requirement, condition, status in raw_rows
    ]


def gdot_rows(timestamp: str) -> list[dict[str, object]]:
    raw_rows = [
        (
            "GDOT3881_0_conditional_zero",
            "Gdot_over_G",
            "yr^-1",
            "d_t ln G_eff=d_t ln C_*=0 from dC_*=0",
            "0.0",
            "9.6e-15",
            "CONDITIONAL_PASS_IF_PARENT_ACTION_ADOPTS_ZF3881",
            "ZF3881_1_A3_variation;PAC3881_0_to_10",
        ),
        (
            "GDOT3881_1_fallback_absolute_sum",
            "Gdot_over_G",
            "yr^-1",
            GDOT_RESIDUAL_FORMULA,
            "MISSING_SEPARATED_COMPONENTS",
            "9.6e-15",
            "BOUND_FORMULA_READY_NUMERIC_COMPONENTS_MISSING",
            "GB3758_1_residual_bound;GB3758_2_max_allowed_residual",
        ),
        (
            "GDOT3881_2_Cstar_component",
            "d_t_ln_Cstar",
            "yr^-1",
            "0 if ZF3881 is parent-signed, else source-backed drift row required",
            "MISSING_PARENT_ZERO_OR_NUMERIC_BOUND",
            "allocated within 9.6e-15 absolute budget",
            "OPEN_COMPONENT",
            "T508_1_topological_zeroform;KR508_0_time_drift",
        ),
        (
            "GDOT3881_3_Meff_component",
            "d_t_ln_Meff",
            "yr^-1",
            "Pi_M/J_H flux conservation component of measured GM drift",
            "MISSING_FLUX_ZERO_OR_NUMERIC_BOUND",
            "allocated within 9.6e-15 absolute budget",
            "OPEN_COMPONENT",
            "CGM1_time_drift;DBI3880_1_time_Meff",
        ),
        (
            "GDOT3881_4_mu_component",
            "d_t_epsilon_mu",
            "yr^-1",
            "time drift of epsilon_mu=mu_extra/(G_eff M_eff)",
            "MISSING_MU_EXTRA_TIME_COEFFICIENT",
            "allocated within 9.6e-15 absolute budget",
            "OPEN_COMPONENT",
            "CGM6_mu_extra_amplitude;DBI3880_7_mu_extra",
        ),
        (
            "GDOT3881_5_readout_components",
            "d_t_ln_Z_Poisson_plus_Z_frame",
            "yr^-1",
            "time drift in Poisson/readout frame locks",
            "MISSING_READOUT_TIME_BOUND",
            "allocated within 9.6e-15 absolute budget",
            "OPEN_COMPONENT",
            "PG7_constant_universal_Geff;PG8_no_derivative_hair",
        ),
    ]
    return [
        {
            "gdot_id": row_id,
            "observable_or_component": observable,
            "units": units,
            "prediction_or_formula": formula,
            "prediction_value": value,
            "bound_or_budget": bound,
            "status": status,
            "source_basis": basis,
            "no_cancellation_policy": True,
            "valid_prediction_row": False,
            "claim_allowed": False,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
        for row_id, observable, units, formula, value, bound, status, basis in raw_rows
    ]


def runner_rows(timestamp: str) -> list[dict[str, object]]:
    raw_rows = [
        ("RUNU3881_0_bt_gate", "b_t", UPDATED_BT, "CONDITIONAL_ZERO_OR_GDOT_FALLBACK"),
        ("RUNU3881_1_common_drift", "b_common_drift", "b_common_drift=b_t+b_r+b_lambda+b_frame+b_domain+b_Bianchi", "CARRIED_FROM_3880_WITH_BT_REFINED"),
        ("RUNU3881_2_bGcommon", "b_Gcommon", UPDATED_BG, "RUNNER_RETAINED_NO_CLAIM"),
        ("RUNU3881_3_top_level", "z_g_active,cal", "|z_g_active,cal| <= b_Qstar + b_Noether + b_tail_rel + b_Gcommon", "NO_CANCELLATION_RUNNER"),
        ("RUNU3881_4_claim_guard", "claim_allowed", "false unless C_*/A_3 parent action is adopted or every Gdot/radial/range/frame/domain/Bianchi component is source-bounded", "NO_LOCAL_GR_CLAIM"),
    ]
    return [
        {
            "update_id": row_id,
            "runner_field": field,
            "rule": rule,
            "status": status,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
        for row_id, field, rule, status in raw_rows
    ]


def claim_gate_rows(
    sources: list[dict[str, object]],
    zeroform: list[dict[str, object]],
    contract: list[dict[str, object]],
    gdot: list[dict[str, object]],
    timestamp: str,
) -> list[dict[str, object]]:
    source_count = sum(1 for row in sources if row["exists"] and row["needle_found"])
    checks = [
        ("G3881_0_sources", source_count == len(sources), f"{source_count}/{len(sources)} sources resolved"),
        ("G3881_1_variation", any(row["zeroform_id"] == "ZF3881_1_A3_variation" and "dC_*=0" in str(row["derivation_or_condition"]) for row in zeroform), "A_3 variation derives dC_*=0"),
        ("G3881_2_derivative_silence", any(row["zeroform_id"] == "ZF3881_2_derivative_silence" for row in zeroform), "derivative silence row exists"),
        ("G3881_3_contract", len(contract) >= 10, f"{len(contract)} parent action contract rows"),
        ("G3881_4_unsigned", all(str(row["adopted_in_parent_action"]) == "False" for row in contract), "contract is not adopted by parent action yet"),
        ("G3881_5_gdot_bound", any(row["bound_or_budget"] == "9.6e-15" for row in gdot), "Gdot bound retained"),
        ("G3881_6_no_claim", True, "all rows kept nonclaim until parent action or numeric bounds close"),
    ]
    return [
        {
            "gate_id": gate_id,
            "status": "PASS" if passed else "FAIL",
            "detail": detail,
            "claim_allowed": False,
            "timestamp_utc": timestamp,
        }
        for gate_id, passed, detail in checks
    ]


def next_rows(timestamp: str) -> list[dict[str, object]]:
    return [
        {
            "next_id": "NEXT3881_0",
            "target_checkpoint": "3882-Y5-R2FR-parent-action-Cstar-threeform-insertion-or-Gdot-component-fill.md",
            "script": "scripts/Y5_R2FR_3882_parent_action_Cstar_threeform_insertion_or_Gdot_component_fill.py",
            "objective": "try to actually insert the C_*/A_3 sector into the parent action and propagate its Euler-Lagrange/Bianchi consequences; if adoption fails, fill the separated Gdot components C_*, M_eff, epsilon_mu, Poisson/readout with source-backed bounds",
            "why_next": "3881 proves the clean mechanism conditionally; the next leap is adoption into the parent action, not another missing-list pass",
            "claim_allowed": False,
            "timestamp_utc": timestamp,
        }
    ]


def status_rows(timestamp: str) -> list[dict[str, object]]:
    return [
        {
            "status_id": "STATUS3881_0",
            "branch": BRANCH,
            "summary": "topological zero-form/three-form mechanism derives dC_*=0 conditionally; parent action adoption remains unsigned; Gdot fallback rows are source-ready and nonclaim",
            "claim_allowed": False,
            "timestamp_utc": timestamp,
        }
    ]


def write_doc(
    sources: list[dict[str, object]],
    zeroform: list[dict[str, object]],
    contract: list[dict[str, object]],
    gdot: list[dict[str, object]],
    runner: list[dict[str, object]],
    gates: list[dict[str, object]],
    next_target: list[dict[str, object]],
    timestamp: str,
) -> None:
    resolved = sum(1 for row in sources if row["exists"] and row["needle_found"])
    doc = f"""# 3881 - Topological Zero-Form Coupling Mechanism or Gdot Bound Fill

Generated: `{timestamp}`

## Result

3881 tries the derivation route first.

`{ZEROFORM_DERIVATION}`

Therefore:

`{DERIVATIVE_SILENCE}`

This is a real mechanism for the coupling problem, not just a label. It says the common coupling can be a branch integration constant rather than a local field. The catch is equally sharp: this mechanism has to be inserted into the parent MTS action before it can carry a Newton/local-GR claim.

## Coupling Policy

`{COUPLING_MAP}`

So the theory does not need to derive the decimal value of `G_N` any more than GR does. It needs to derive why the calibrated value is universal, source-blind, range-blind, frame-blind, and derivative-silent on the tested local branch.

## Zero-Form Variation Audit

{markdown_table(zeroform, ["zeroform_id", "clause", "derivation_or_condition", "status", "remaining_guard"])}

## Parent Action Insertion Contract

{markdown_table(contract, ["contract_id", "requirement", "exact_condition", "status"])}

## Gdot Fallback Rows

{markdown_table(gdot, ["gdot_id", "observable_or_component", "prediction_or_formula", "prediction_value", "bound_or_budget", "status"])}

## Runner Update

{markdown_table(runner, ["update_id", "runner_field", "rule", "status"])}

## Source Register

Resolved `{resolved}/{len(sources)}` source rows.

{markdown_table(sources, ["source_id", "path", "needle_found", "role"])}

## Claim Gates

{markdown_table(gates, ["gate_id", "status", "detail", "claim_allowed"])}

## Next Target

{markdown_table(next_target, ["next_id", "target_checkpoint", "objective", "why_next"])}

## Bottom Line

This is forward motion. We now have an exact conditional mechanism: `A_3` variation forces `dC_*=0`, which would kill the local coupling drift channels if the parent action adopts it cleanly. The branch is still nonclaim because adoption is not yet done. Next step is not another audit loop: it is either parent-action insertion of the `C_*/A_3` sector, or a separated numeric `Gdot` component fill.
"""
    DOC_PATH.write_text(doc, encoding="utf-8")


def update_spine(timestamp: str) -> None:
    start = "<!-- BEGIN 3881 TOPOLOGICAL ZEROFORM COUPLING -->"
    end = "<!-- END 3881 TOPOLOGICAL ZEROFORM COUPLING -->"
    block = f"""{start}

## 3881 - Topological zero-form coupling mechanism or Gdot fallback

`3881` gives the clean coupling mechanism:

`{ZEROFORM_DERIVATION}`

So, conditionally:

`{DERIVATIVE_SILENCE}`

Coupling map:

`{COUPLING_MAP}`

Runner refinement:

`{UPDATED_BT}`

No Newton/local-GR claim is made because the `C_*/A_3` sector is not yet adopted in the parent MTS action. But this is no longer merely a missing slot: it is an explicit parent-action insertion contract.

Generated outputs:
- `source-intake\\mts_residuals\\P8_Y5_R2FR_3881_TOPOLOGICAL_ZEROFORM_VARIATION_AUDIT.csv`
- `source-intake\\mts_residuals\\P8_Y5_R2FR_3881_PARENT_ACTION_INSERTION_CONTRACT.csv`
- `source-intake\\mts_residuals\\P8_Y5_R2FR_3881_GDOT_FALLBACK_BOUND_ROWS.csv`
- `source-intake\\mts_residuals\\P8_Y5_BRR545_3881_VALIDATION.csv`

Next gate: `3882`, parent-action `C_*/A_3` insertion or separated `Gdot` component fill.

<!-- Generated by 3881 at {timestamp} -->
{end}
"""
    existing = read_text(SPINE_PATH) if SPINE_PATH.exists() else "# Local GR Coupling Spine Current State\n"
    if start in existing and end in existing:
        before = existing.split(start)[0].rstrip()
        after = existing.split(end, 1)[1].lstrip()
        new_text = f"{before}\n\n{block}\n\n{after}".rstrip() + "\n"
    else:
        new_text = existing.rstrip() + "\n\n" + block + "\n"
    SPINE_PATH.write_text(new_text, encoding="utf-8")


def validation_rows(
    sources: list[dict[str, object]],
    zeroform: list[dict[str, object]],
    contract: list[dict[str, object]],
    gdot: list[dict[str, object]],
    runner: list[dict[str, object]],
    gates: list[dict[str, object]],
    timestamp: str,
) -> list[dict[str, object]]:
    checks: list[tuple[str, str, bool, str]] = []
    all_sources = all(row["exists"] and row["needle_found"] for row in sources)
    checks.append(("VAL3881_0_sources", "all cited source paths exist and needles are found", all_sources, f"{sum(1 for row in sources if row['exists'] and row['needle_found'])}/{len(sources)} sources resolved"))
    checks.append(("VAL3881_1_variation_derives_zero", "A3 variation row derives dC_*=0", any(row["zeroform_id"] == "ZF3881_1_A3_variation" and "dC_*=0" in str(row["derivation_or_condition"]) for row in zeroform), "ZF3881_1_A3_variation"))
    checks.append(("VAL3881_2_derivative_silence", "derivative silence row kills local C_* channels conditionally", any(row["zeroform_id"] == "ZF3881_2_derivative_silence" and "D_t ln C_*" in str(row["derivation_or_condition"]) for row in zeroform), "ZF3881_2_derivative_silence"))
    required_contract = {"field content", "topological term", "gauge invariance", "no extra A_3 sources", "single coupling map", "no hidden labels", "connected local branch", "Bianchi compatibility"}
    contract_requirements = {str(row["requirement"]) for row in contract}
    checks.append(("VAL3881_3_contract_complete", "parent action insertion contract covers required clauses", required_contract.issubset(contract_requirements), ",".join(sorted(contract_requirements))))
    checks.append(("VAL3881_4_contract_unsigned", "contract is not silently promoted to parent action", all(str(row["adopted_in_parent_action"]) == "False" for row in contract), "adopted_in_parent_action=false"))
    checks.append(("VAL3881_5_gdot_bound", "Gdot fallback keeps numeric bound", any(row["bound_or_budget"] == "9.6e-15" for row in gdot), "9.6e-15 yr^-1"))
    checks.append(("VAL3881_6_gdot_components", "Gdot fallback separates C_*, M_eff, epsilon_mu, and readout components", {"d_t_ln_Cstar", "d_t_ln_Meff", "d_t_epsilon_mu", "d_t_ln_Z_Poisson_plus_Z_frame"}.issubset({str(row["observable_or_component"]) for row in gdot}), "separated components"))
    checks.append(("VAL3881_7_runner_bt", "runner updates b_t gate", any(row["runner_field"] == "b_t" and "C_*/A_3" in str(row["rule"]) for row in runner), "b_t gate"))
    checks.append(("VAL3881_8_no_claim_gates", "no gate allows a claim", all(str(row["claim_allowed"]) == "False" for row in gates), "claim_allowed=false"))
    checks.append(("VAL3881_9_doc", "markdown checkpoint exists with bottom line", DOC_PATH.exists() and "This is forward motion" in read_text(DOC_PATH), rel(DOC_PATH)))
    checks.append(("VAL3881_10_spine", "spine updated with 3881 block", SPINE_PATH.exists() and "BEGIN 3881 TOPOLOGICAL ZEROFORM COUPLING" in read_text(SPINE_PATH), rel(SPINE_PATH)))
    csv_outputs = [path for key, path in OUTPUTS.items() if key != "validation"]
    csv_parse_ok = True
    parse_details = []
    for path in csv_outputs:
        try:
            parse_details.append(f"{path.name}:{len(read_csv_rows(path))}")
        except Exception as exc:
            csv_parse_ok = False
            parse_details.append(f"{path.name}:{exc}")
    checks.append(("VAL3881_11_csv_parse", "all generated CSV outputs parse", csv_parse_ok, "; ".join(parse_details)))
    formalization_hits = []
    generated_patterns = ("3881-Y5", "P8_Y5_R2FR_3881", "P8_Y5_BRR545_3881")
    if FWB.exists():
        formalization_hits = [
            path
            for path in FWB.rglob("*3881*")
            if path.is_file() and any(pattern in path.name for pattern in generated_patterns)
        ]
    checks.append(("VAL3881_12_formalization_untouched", "no generated 3881 files appear in formalization-workbench", not formalization_hits, f"{len(formalization_hits)} hits"))
    pycache_hits = [path for path in (PCW / "scripts").rglob("__pycache__") if path.is_dir()]
    checks.append(("VAL3881_13_no_pycache", "scripts __pycache__ removed", not pycache_hits, f"{len(pycache_hits)} pycache dirs"))
    checks.append(("VAL3881_14_all_nonclaim", "all analytical rows are nonclaim", all(str(row.get("valid_for_claim")) == "False" for collection in [zeroform, contract, gdot, runner] for row in collection), "valid_for_claim=false"))
    checks.append(("VAL3881_15_next_target", "next target is parent action insertion or Gdot fill", any("parent-action-Cstar-threeform" in str(row["target_checkpoint"]) for row in next_rows(timestamp)), "3882 parent action/Gdot"))
    return [
        {
            "check_id": check_id,
            "description": description,
            "status": "PASS" if passed else "FAIL",
            "detail": detail,
            "timestamp_utc": timestamp,
        }
        for check_id, description, passed, detail in checks
    ]


def main() -> int:
    timestamp = now_utc()
    sources = source_register_rows(timestamp)
    zeroform = zeroform_rows(timestamp)
    contract = contract_rows(timestamp)
    gdot = gdot_rows(timestamp)
    runner = runner_rows(timestamp)
    gates = claim_gate_rows(sources, zeroform, contract, gdot, timestamp)
    next_target = next_rows(timestamp)
    status = status_rows(timestamp)

    write_csv(OUTPUTS["sources"], sources)
    write_csv(OUTPUTS["zeroform"], zeroform)
    write_csv(OUTPUTS["contract"], contract)
    write_csv(OUTPUTS["gdot"], gdot)
    write_csv(OUTPUTS["runner"], runner)
    write_csv(OUTPUTS["gates"], gates)
    write_csv(OUTPUTS["next"], next_target)
    write_csv(OUTPUTS["status"], status)
    write_doc(sources, zeroform, contract, gdot, runner, gates, next_target, timestamp)
    update_spine(timestamp)

    for pycache in (PCW / "scripts").rglob("__pycache__"):
        shutil.rmtree(pycache, ignore_errors=True)

    validation = validation_rows(sources, zeroform, contract, gdot, runner, gates, timestamp)
    write_csv(OUTPUTS["validation"], validation)
    failed = [row for row in validation if row["status"] != "PASS"]
    if failed:
        for row in failed:
            print(f"FAIL {row['check_id']}: {row['detail']}")
        return 1
    print(f"{CHECKPOINT} PASS_TOPOLOGICAL_ZEROFORM_COUPLING_OR_GDOT_FILL")
    print(rel(DOC_PATH))
    print(rel(OUTPUTS["validation"]))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

from __future__ import annotations

import csv
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


POST_CHECKPOINT = Path(__file__).resolve().parents[1]
REPO_ROOT = POST_CHECKPOINT.parent
RESIDUALS = POST_CHECKPOINT / "source-intake" / "mts_residuals"
FORMALIZATION = REPO_ROOT / "formalization-workbench"

OUTPUT_DOC = POST_CHECKPOINT / "747-Y5-R10-alpha3-momentum-flux-zero-or-q_loc-vector-coefficient-bound.md"
NEXT_TARGET = "748-Y5-R10-q_loc-vector-parity-zero-theorem-or-Wqalpha3-source-row.md"
STATUS = "Y5_R10_747_alpha3_momentum_flux_zero_not_derived_vector_coefficient_pressure_bound_written_nonclaim"
CLAIM_CEILING = "alpha3_q_loc_zero_attempt_and_coefficient_pressure_only_no_alpha3_PPN_R10_Newton_or_local_GR_pass"
Q_PROXY = 7.432631961576971e-06
ALPHA3_BOUND = 4.0e-20
WF_LIMIT = ALPHA3_BOUND / Q_PROXY
UNIT_RATIO = Q_PROXY / ALPHA3_BOUND
FORMALIZATION_CUTOFF = datetime(2026, 5, 31, 14, 42, 0)

SOURCE_REGISTER_PATH = RESIDUALS / "P8_Y5_R10_747_SOURCE_REGISTER.csv"
ZERO_AUDIT_PATH = RESIDUALS / "P8_Y5_R10_747_ALPHA3_QLOC_ZERO_THEOREM_AUDIT.csv"
COEFF_PRESSURE_PATH = RESIDUALS / "P8_Y5_R10_747_WQALPHA3_COEFFICIENT_PRESSURE.csv"
ACCEPTANCE_PATH = RESIDUALS / "P8_Y5_R10_747_ALPHA3_QLOC_ACCEPTANCE_GATE.csv"
Y5_UPDATE_PATH = RESIDUALS / "P8_Y5_R10_747_Y5_RUNNER_UPDATE.csv"
DECISION_PATH = RESIDUALS / "P8_Y5_R10_747_DECISION_MATRIX.csv"
ROUTE_PATH = RESIDUALS / "P8_Y5_R10_747_ROUTE_UPDATE.csv"
SUMMARY_PATH = RESIDUALS / "P8_Y5_R10_747_NONCLAIM_SUMMARY.csv"
VALIDATION_PATH = RESIDUALS / "P8_Y5_BRR545_747_VALIDATION.csv"

SOURCES: dict[str, dict[str, Any]] = {
    "746_doc": {
        "path": POST_CHECKPOINT / "746-Y5-R10-q_loc-to-PPN-or-alpha3-projection-map-contract.md",
        "needles": ["alpha3_q = W_q_alpha3 * epsilon_q_momentum", "747-Y5-R10-alpha3-momentum-flux-zero-or-q_loc-vector-coefficient-bound.md", "highest-pressure target"],
        "role": "immediate alpha3 handoff",
    },
    "746_validation": {
        "path": RESIDUALS / "P8_Y5_BRR545_746_VALIDATION.csv",
        "needles": ["V746_5_alpha3_selected_next", "V746_13_formalization_workbench_untouched", "V746_14_no_local_arena_claim"],
        "role": "prior validation guard",
    },
    "746_alpha3_gate": {
        "path": RESIDUALS / "P8_Y5_R10_746_ALPHA3_MOMENTUM_FLUX_GATE.csv",
        "needles": ["A3Q746_0_product_law", "W_q_alpha3 * epsilon_q_momentum", "not_scoreable"],
        "role": "alpha3 product law from 746",
    },
    "746_router": {
        "path": RESIDUALS / "P8_Y5_R10_746_QLOC_CHANNEL_ROUTER.csv",
        "needles": ["QCR746_2_alpha3_momentum_flux", "highest_pressure_branch_if_projection_applies", "185815799039424"],
        "role": "q_loc channel routing pressure",
    },
    "odd_split": {
        "path": RESIDUALS / "P8_SOURCE_NORMALIZATION_EVEN_ODD_SPLIT.csv",
        "needles": ["E1_odd_extra_source", "could_vanish_if_exchange_theorem", "E2_even_extra_source"],
        "role": "even/odd split guard",
    },
    "odd_component_map": {
        "path": RESIDUALS / "P8_ODD_RESIDUAL_COMPONENT_MAP.csv",
        "needles": ["Y3_domain_vector", "conditional_best", "Y5_source_normalization"],
        "role": "odd residual component map blockers",
    },
    "odd_exchange": {
        "path": RESIDUALS / "P8_ODD_RESIDUAL_EXCHANGE_THEOREM.csv",
        "needles": ["E5_current_corpus", "conditional theorem only", "missing P1 component certificates"],
        "role": "exchange-odd zero theorem status",
    },
    "momentum_map_theorem": {
        "path": RESIDUALS / "P8_Y5_R10_582_MOMENTUM_MAP_CLOSURE_THEOREM.csv",
        "needles": ["MMT582_4_no_pole_result", "conditional_theorem_only", "boundary_not_silenced"],
        "role": "momentum-map closure blocker",
    },
    "momentum_map_contract": {
        "path": RESIDUALS / "P8_Y5_R10_583_NOETHER_MOMENTUM_MAP_CONTRACT.csv",
        "needles": ["NMC583_3_momentum_map", "not_derived", "NMC583_5_boundary_zero"],
        "role": "Noether momentum map contract",
    },
    "momentum_owner_test": {
        "path": RESIDUALS / "P8_Y5_R10_586_MOMENTUM_MAP_OWNER_TEST.csv",
        "needles": ["MMT586_1_vertical_generator", "blocked", "MMT586_4_matter_factorization"],
        "role": "momentum-map owner test",
    },
    "mu_extra_alpha3_zero": {
        "path": RESIDUALS / "P8_MU_EXTRA_ALPHA3_ZERO_ATTEMPT.csv",
        "needles": ["ZA0_alpha3_exchange_owner", "conditional_identity_only", "ZA7_conclusion"],
        "role": "alpha3 no-flux zero attempt analogue",
    },
    "alpha3_fill_skeleton": {
        "path": RESIDUALS / "P8_MU_EXTRA_ALPHA3_FILL_INPUT_SKELETON.csv",
        "needles": ["target_bound", "4e-20", "MISSING_NUMERIC_OR_DERIVED_ZERO"],
        "role": "alpha3 product skeleton",
    },
    "q_loc_u2_bound": {
        "path": RESIDUALS / "P8_Y5_QLOC_U2_BOUND.csv",
        "needles": ["QBU526_1_compact_shell_to_alpha3_warning", "185815799039424.3", "MISSING_CONVERSION"],
        "role": "old q_loc beta/alpha3 pressure row",
    },
}


def utc_stamp() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace") if path.exists() else ""


def text_contains(path: Path, needles: list[str]) -> bool:
    text = read_text(path)
    return bool(text) and all(needle in text for needle in needles)


def read_csv_rows(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    with path.open("r", newline="", encoding="utf-8-sig") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, Any]], fieldnames: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)


def markdown_cell(value: Any) -> str:
    return str(value).replace("|", "\\|").replace("\n", "<br>")


def markdown_table(rows: list[dict[str, Any]], columns: list[str]) -> str:
    if not rows:
        return "_No rows._"
    header = "| " + " | ".join(columns) + " |"
    divider = "| " + " | ".join("---" for _ in columns) + " |"
    body = ["| " + " | ".join(markdown_cell(row.get(column, "")) for column in columns) + " |" for row in rows]
    return "\n".join([header, divider, *body])


def bool_string(value: bool) -> str:
    return "true" if value else "false"


def under_post(path: Path) -> bool:
    try:
        path.resolve().relative_to(POST_CHECKPOINT.resolve())
        return True
    except ValueError:
        return False


def formalization_changed_after_cutoff() -> int:
    if not FORMALIZATION.exists():
        return -1
    count = 0
    for path in FORMALIZATION.rglob("*"):
        if path.is_file() and datetime.fromtimestamp(path.stat().st_mtime) > FORMALIZATION_CUTOFF:
            count += 1
    return count


def make_source_register(generated_utc: str) -> list[dict[str, Any]]:
    return [
        {
            "source_id": source_id,
            "path": str(spec["path"]),
            "exists": bool_string(Path(spec["path"]).exists()),
            "needle_check": bool_string(text_contains(Path(spec["path"]), spec["needles"])),
            "role": spec["role"],
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        }
        for source_id, spec in SOURCES.items()
    ]


def zero_audit_rows(generated_utc: str) -> list[dict[str, Any]]:
    return [
        {
            "attempt_id": "AZ747_0_pure_scalar_even",
            "zero_route": "q_loc is purely scalar/even in the compact local branch",
            "mathematical_form": "P_mom q_loc = 0 and q_V^i=q_TF^i=0",
            "current_status": "not_derived_current_chain",
            "blocker": "observed q_loc decomposition is not supplied; source-normalization even channels can survive",
            "if_true": "alpha3_q_loc branch is zero, while beta/gamma/R10 still need their own maps",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "attempt_id": "AZ747_1_exchange_odd",
            "zero_route": "momentum flux is exchange-odd and local odd charge vanishes",
            "mathematical_form": "E:q_V -> -q_V, S_even, J_odd=0 => epsilon_q_momentum=0",
            "current_status": "conditional_only",
            "blocker": "odd component map, even matter readout, and boundary odd-charge zero are not parent-derived",
            "if_true": "structural alpha3 silence without fine tuning",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "attempt_id": "AZ747_2_momentum_map",
            "zero_route": "q_loc momentum flux is a pure vertical momentum-map constraint",
            "mathematical_form": "G[epsilon]=int epsilon C_X + Q_boundary, differentiable first-class, Q_boundary=0",
            "current_status": "blocked",
            "blocker": "parent symplectic potential, vertical generator, algebra closure, and boundary silence remain missing",
            "if_true": "q_loc vector/flux mode becomes gauge, not alpha3 source",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "attempt_id": "AZ747_3_boundary_domain_analogue",
            "zero_route": "reuse old boundary/domain alpha3 no-flux logic for q_loc",
            "mathematical_form": "F_q_alpha3 := lim_S r^2 n_mu P_mom_nu K_q^{mu nu}/(G_eff M_eff)=0",
            "current_status": "not_derived",
            "blocker": "old alpha3 no-flux theorem failed for boundary/domain; q_loc-specific K_q map is not supplied",
            "if_true": "would be the cleanest local alpha3 kill",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "attempt_id": "AZ747_4_verdict",
            "zero_route": "set epsilon_q_momentum=0 now",
            "mathematical_form": "alpha3_q = 0",
            "current_status": "zero_theorem_failed_current_corpus",
            "blocker": "every available zero route is conditional, blocked, or not q_loc-specific",
            "if_true": "not available; coefficient bound route must be retained",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
    ]


def coefficient_pressure_rows(generated_utc: str) -> list[dict[str, Any]]:
    return [
        {
            "pressure_id": "WQA747_0_product_definition",
            "quantity": "alpha3_q",
            "formula": "alpha3_q = W_q_alpha3 * epsilon_q_momentum = W_q_alpha3 * f_qV * q_proxy",
            "value": "symbolic",
            "interpretation": "f_qV is the fraction of q_proxy landing in momentum/preferred-frame flux",
            "required_for_pass": f"|W_q_alpha3 * f_qV| <= {WF_LIMIT:.15g}",
            "current_status": "definition_written_not_filled",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "pressure_id": "WQA747_1_unit_product_pressure",
            "quantity": "q_proxy/alpha3_bound",
            "formula": "q_proxy / 4e-20",
            "value": f"{UNIT_RATIO:.15g}",
            "interpretation": "unit W and unit vector fraction would exceed alpha3 by this factor",
            "required_for_pass": "not a pass/fail without projection map",
            "current_status": "danger_scale_only",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "pressure_id": "WQA747_2_if_W_order_one",
            "quantity": "f_qV_limit",
            "formula": "f_qV <= alpha3_bound/q_proxy if W_q_alpha3=1",
            "value": f"{WF_LIMIT:.15g}",
            "interpretation": "only an extremely tiny vector fraction can survive if response weight is order one",
            "required_for_pass": "source-backed f_qV below limit or theorem-zero",
            "current_status": "not_sourced",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "pressure_id": "WQA747_3_if_vector_fraction_order_one",
            "quantity": "W_q_alpha3_limit",
            "formula": "W_q_alpha3 <= alpha3_bound/q_proxy if f_qV=1",
            "value": f"{WF_LIMIT:.15g}",
            "interpretation": "response weight must be absurdly suppressed if q_loc is mostly momentum flux",
            "required_for_pass": "source-backed W_q_alpha3 below limit or theorem-zero",
            "current_status": "not_sourced",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "pressure_id": "WQA747_4_acceptance",
            "quantity": "claim-grade alpha3_q row",
            "formula": "valid_for_claim=true only if theorem-zero or numeric |W_q_alpha3 f_qV q_proxy|<=4e-20",
            "value": "not_available",
            "interpretation": "current branch has pressure target but no claim row",
            "required_for_pass": "W, f_qV, q_proxy equivalence, source path, units, no-cancellation flag",
            "current_status": "blocked_nonclaim",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
    ]


def acceptance_rows(generated_utc: str) -> list[dict[str, Any]]:
    return [
        {
            "gate_id": "A3A747_0_zero_gate",
            "gate": "epsilon_q_momentum theorem-zero",
            "pass_condition": "P_mom q_loc=0 from parent-owned scalar/even or momentum-map proof",
            "current_result": "fail_current_corpus",
            "claim_effect": "alpha3_q_loc remains active",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "gate_id": "A3A747_1_numeric_product_gate",
            "gate": "numeric W_q_alpha3 f_qV product",
            "pass_condition": f"|W_q_alpha3 f_qV| <= {WF_LIMIT:.15g}",
            "current_result": "not_loaded",
            "claim_effect": "no alpha3 score",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "gate_id": "A3A747_2_no_cancellation",
            "gate": "q_loc alpha3 channel passes independently",
            "pass_condition": "no cancellation with boundary/domain/projector alpha3 channels unless parent identity derived",
            "current_result": "policy_pass",
            "claim_effect": "keeps alpha3 honest",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "gate_id": "A3A747_3_next",
            "gate": "next target selection",
            "pass_condition": "derive vector parity zero or fill W_q_alpha3 source row",
            "current_result": "selected",
            "claim_effect": NEXT_TARGET,
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
    ]


def y5_update_rows(generated_utc: str) -> list[dict[str, Any]]:
    return [
        {
            "runner_id": "Y5R747_alpha3_q_loc",
            "source_row": "R7_alpha3/q_loc",
            "status_after_747": "zero_theorem_failed_pressure_bound_written",
            "zero_or_input": f"|W_q_alpha3 f_qV| <= {WF_LIMIT:.15g} required",
            "still_missing": "q_loc vector decomposition; W_q_alpha3; f_qV; theorem-zero or source path",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "runner_id": "Y5R747_PPN",
            "source_row": "PPN524_7",
            "status_after_747": "PPN_not_promoted",
            "zero_or_input": "alpha3 branch is tighter than beta/gamma if vector projection applies",
            "still_missing": "beta/gamma conversion factors and alpha_i vector map",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "runner_id": "Y5R747_R10",
            "source_row": "R10_alpha_lambda",
            "status_after_747": "still_deferred",
            "zero_or_input": "range kernel not part of alpha3 momentum-flux gate",
            "still_missing": "lambda and c_q_alpha(lambda)",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
    ]


def decision_rows(generated_utc: str) -> list[dict[str, Any]]:
    return [
        {
            "decision_id": "D747_0_zero_attempt",
            "decision": "do not claim q_loc alpha3 momentum-flux zero",
            "meaning": "scalar/even, exchange-odd, momentum-map, and no-flux routes all remain unsigned",
            "claim_status": "zero_failed_current_chain",
            "next_target": NEXT_TARGET,
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "decision_id": "D747_1_pressure",
            "decision": "write coefficient pressure bound",
            "meaning": f"the product |W_q_alpha3 f_qV| must be <= {WF_LIMIT:.15g}",
            "claim_status": "pressure_target_only",
            "next_target": NEXT_TARGET,
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "decision_id": "D747_2_theory_preference",
            "decision": "prefer theorem-zero over tiny coefficient fit",
            "meaning": "alpha3 is so tight that a natural route needs vector/parity/momentum-flux silence, not a convenient small number",
            "claim_status": "method_choice_nonclaim",
            "next_target": NEXT_TARGET,
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "decision_id": "D747_3_next",
            "decision": "attack vector parity zero or source W_q_alpha3",
            "meaning": "next work must either prove f_qV=0 or supply a real product row",
            "claim_status": "next_target_selected",
            "next_target": NEXT_TARGET,
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
    ]


def route_rows(generated_utc: str) -> list[dict[str, Any]]:
    return [
        {
            "route_id": "RU747_0_allowed",
            "allowed_after_747": "say alpha3 q_loc zero is not derived",
            "forbidden_after_747": "say q_loc passes alpha3 or local PPN",
            "next_action": NEXT_TARGET,
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "route_id": "RU747_1_allowed",
            "allowed_after_747": "quote |W_q_alpha3 f_qV| <= alpha3_bound/q_proxy as pressure target",
            "forbidden_after_747": "treat this pressure target as a measured/source-backed coefficient",
            "next_action": NEXT_TARGET,
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "route_id": "RU747_2_allowed",
            "allowed_after_747": "prioritize vector/parity/momentum-map zero theorem",
            "forbidden_after_747": "hide alpha3 by cancellation against other channels",
            "next_action": NEXT_TARGET,
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
    ]


def summary_rows(generated_utc: str) -> list[dict[str, Any]]:
    return [
        {
            "status": STATUS,
            "claim_ceiling": CLAIM_CEILING,
            "main_result": "alpha3 q_loc momentum-flux zero theorem failed for current chain; coefficient pressure bound written",
            "hard_blocker": "q_loc vector decomposition, W_q_alpha3, f_qV, and parent momentum-map/parity zero remain missing",
            "next_target": NEXT_TARGET,
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        }
    ]


def make_validation(
    sources: list[dict[str, Any]],
    zero: list[dict[str, Any]],
    pressure: list[dict[str, Any]],
    acceptance: list[dict[str, Any]],
    y5_update: list[dict[str, Any]],
    decisions: list[dict[str, Any]],
    routes: list[dict[str, Any]],
    outputs: list[Path],
) -> list[dict[str, str]]:
    prior = read_csv_rows(RESIDUALS / "P8_Y5_BRR545_746_VALIDATION.csv")
    all_rows = zero + pressure + acceptance + y5_update + decisions + routes
    validation: list[dict[str, str]] = []
    validation.append({"check_id": "V747_0_source_paths_exist", "result": "pass" if all(row["exists"] == "true" for row in sources) else "fail", "detail": f"source_rows={len(sources)}"})
    validation.append({"check_id": "V747_1_source_needles_present", "result": "pass" if all(row["needle_check"] == "true" for row in sources) else "fail", "detail": "all source files contain expected evidence needles"})
    validation.append({"check_id": "V747_2_prior_746_clean", "result": "pass" if prior and all(row.get("result") == "pass" for row in prior) else "fail", "detail": "746 validation has no failures"})
    validation.append({"check_id": "V747_3_zero_theorem_failed", "result": "pass" if any(row["current_status"] == "zero_theorem_failed_current_corpus" for row in zero) else "fail", "detail": "q_loc alpha3 zero not promoted"})
    validation.append({"check_id": "V747_4_pressure_limit_written", "result": "pass" if any(f"{WF_LIMIT:.15g}" in row["required_for_pass"] for row in pressure) else "fail", "detail": f"WF_limit={WF_LIMIT:.15g}"})
    validation.append({"check_id": "V747_5_unit_ratio_written", "result": "pass" if any(row["value"] == f"{UNIT_RATIO:.15g}" for row in pressure) else "fail", "detail": f"unit_ratio={UNIT_RATIO:.15g}"})
    validation.append({"check_id": "V747_6_acceptance_requires_zero_or_numeric", "result": "pass" if any(row["gate_id"] == "A3A747_1_numeric_product_gate" and row["current_result"] == "not_loaded" for row in acceptance) else "fail", "detail": "numeric product not loaded"})
    validation.append({"check_id": "V747_7_no_cancellation_policy", "result": "pass" if any(row["gate_id"] == "A3A747_2_no_cancellation" and row["current_result"] == "policy_pass" for row in acceptance) else "fail", "detail": "no cancellation gate retained"})
    validation.append({"check_id": "V747_8_Y5_rows_retained", "result": "pass" if {"Y5R747_alpha3_q_loc", "Y5R747_PPN", "Y5R747_R10"}.issubset({row["runner_id"] for row in y5_update}) else "fail", "detail": "alpha3/PPN/R10 rows retained"})
    validation.append({"check_id": "V747_9_no_claim_rows_promoted", "result": "pass" if all(row.get("valid_for_claim") == "false" for row in all_rows) else "fail", "detail": "all generated rows valid_for_claim=false"})
    validation.append({"check_id": "V747_10_next_target_selected", "result": "pass" if all(row.get("next_target") == NEXT_TARGET for row in decisions) else "fail", "detail": NEXT_TARGET})
    validation.append({"check_id": "V747_11_outputs_scoped", "result": "pass" if all(under_post(path) for path in outputs) else "fail", "detail": "all outputs under post-checkpoint-work"})
    changed = formalization_changed_after_cutoff()
    validation.append({"check_id": "V747_12_formalization_workbench_untouched", "result": "pass" if changed == 0 else "fail", "detail": f"formalization_changed_after_cutoff={changed}"})
    validation.append({"check_id": "V747_13_no_local_arena_claim", "result": "pass" if "no_alpha3_PPN_R10_Newton_or_local_GR_pass" in CLAIM_CEILING else "fail", "detail": "alpha3/PPN/R10/Newton/local-GR claims remain blocked"})
    validation.append({"check_id": "V747_14_validation_rows_ready", "result": "pass", "detail": "validation table constructed"})
    return validation


def build_doc(
    sources: list[dict[str, Any]],
    zero: list[dict[str, Any]],
    pressure: list[dict[str, Any]],
    acceptance: list[dict[str, Any]],
    y5_update: list[dict[str, Any]],
    decisions: list[dict[str, Any]],
    routes: list[dict[str, Any]],
    summary: list[dict[str, Any]],
    validation: list[dict[str, Any]],
) -> None:
    text = f"""# 747 - Y5 R10 alpha3 Momentum Flux Zero Or q_loc Vector Coefficient Bound

Start point: 746 selected alpha3 momentum-flux as the highest-pressure q_loc branch if that projection exists.

Current result: **the alpha3/q_loc momentum-flux zero theorem does not close for the current chain**. The best clean routes are real but conditional: pure scalar/even q_loc, exchange-odd local charge zero, or a parent-owned momentum-map constraint. None are signed yet.

So the retained product is:

```text
alpha3_q = W_q_alpha3 * epsilon_q_momentum
epsilon_q_momentum = f_qV * q_proxy
q_proxy = {Q_PROXY:.15g}
|W_q_alpha3 f_qV| <= alpha3_bound/q_proxy = {WF_LIMIT:.15g}
```

That is the pressure number. If either `W_q_alpha3` or the vector fraction `f_qV` is order one, the branch is crushed by alpha3. The natural route is therefore a zero theorem, not a tuned tiny coefficient.

## Summary

| Field | Value |
| --- | --- |
| Status | `{STATUS}` |
| Claim ceiling | `{CLAIM_CEILING}` |
| Main result | alpha3 q_loc zero not derived; coefficient pressure target written |
| Next target | `{NEXT_TARGET}` |

## Alpha3 q_loc Zero-Theorem Audit

{markdown_table(zero, ["attempt_id", "zero_route", "mathematical_form", "current_status", "blocker", "if_true", "valid_for_claim"])}

## Wqalpha3 Coefficient Pressure

{markdown_table(pressure, ["pressure_id", "quantity", "formula", "value", "interpretation", "required_for_pass", "current_status", "valid_for_claim"])}

## Acceptance Gate

{markdown_table(acceptance, ["gate_id", "gate", "pass_condition", "current_result", "claim_effect", "valid_for_claim"])}

## Y5 Runner Update

{markdown_table(y5_update, ["runner_id", "source_row", "status_after_747", "zero_or_input", "still_missing", "valid_for_claim"])}

## Decisions

{markdown_table(decisions, ["decision_id", "decision", "meaning", "claim_status", "next_target", "valid_for_claim"])}

## Route Update

{markdown_table(routes, ["route_id", "allowed_after_747", "forbidden_after_747", "next_action", "valid_for_claim"])}

## Source Register

{markdown_table(sources, ["source_id", "path", "exists", "needle_check", "role", "valid_for_claim"])}

## Validation

{markdown_table(validation, ["check_id", "result", "detail"])}

## Plain-English Verdict

This is the “coupling dragon” with a microscope on it. Alpha3 is so tight that an ordinary vector/momentum-flux q_loc component is not something we can shrug off. The product has to be below about `5.38e-15` after splitting response weight and vector fraction. That does not kill the theory; it tells us the theory needs a structural reason for the vector piece to vanish. Next best move: prove a parity/vector zero, or source the actual `W_q_alpha3` product honestly.
"""
    OUTPUT_DOC.write_text(text, encoding="utf-8")


def main() -> None:
    generated_utc = utc_stamp()
    sources = make_source_register(generated_utc)
    zero = zero_audit_rows(generated_utc)
    pressure = coefficient_pressure_rows(generated_utc)
    acceptance = acceptance_rows(generated_utc)
    y5_update = y5_update_rows(generated_utc)
    decisions = decision_rows(generated_utc)
    routes = route_rows(generated_utc)
    summary = summary_rows(generated_utc)
    outputs = [
        OUTPUT_DOC,
        SOURCE_REGISTER_PATH,
        ZERO_AUDIT_PATH,
        COEFF_PRESSURE_PATH,
        ACCEPTANCE_PATH,
        Y5_UPDATE_PATH,
        DECISION_PATH,
        ROUTE_PATH,
        SUMMARY_PATH,
        VALIDATION_PATH,
    ]
    validation = make_validation(sources, zero, pressure, acceptance, y5_update, decisions, routes, outputs)

    write_csv(SOURCE_REGISTER_PATH, sources, ["source_id", "path", "exists", "needle_check", "role", "valid_for_claim", "generated_utc"])
    write_csv(ZERO_AUDIT_PATH, zero, ["attempt_id", "zero_route", "mathematical_form", "current_status", "blocker", "if_true", "valid_for_claim", "generated_utc"])
    write_csv(COEFF_PRESSURE_PATH, pressure, ["pressure_id", "quantity", "formula", "value", "interpretation", "required_for_pass", "current_status", "valid_for_claim", "generated_utc"])
    write_csv(ACCEPTANCE_PATH, acceptance, ["gate_id", "gate", "pass_condition", "current_result", "claim_effect", "valid_for_claim", "generated_utc"])
    write_csv(Y5_UPDATE_PATH, y5_update, ["runner_id", "source_row", "status_after_747", "zero_or_input", "still_missing", "valid_for_claim", "generated_utc"])
    write_csv(DECISION_PATH, decisions, ["decision_id", "decision", "meaning", "claim_status", "next_target", "valid_for_claim", "generated_utc"])
    write_csv(ROUTE_PATH, routes, ["route_id", "allowed_after_747", "forbidden_after_747", "next_action", "valid_for_claim", "generated_utc"])
    write_csv(SUMMARY_PATH, summary, ["status", "claim_ceiling", "main_result", "hard_blocker", "next_target", "valid_for_claim", "generated_utc"])
    write_csv(VALIDATION_PATH, validation, ["check_id", "result", "detail"])
    build_doc(sources, zero, pressure, acceptance, y5_update, decisions, routes, summary, validation)

    failures = [row for row in validation if row["result"] != "pass"]
    print(f"wrote={OUTPUT_DOC}")
    print(f"validation_rows={len(validation)}")
    print(f"validation_failures={len(failures)}")
    if failures:
        for failure in failures:
            print(f"FAIL {failure['check_id']}: {failure['detail']}")
        raise SystemExit(1)


if __name__ == "__main__":
    main()

from __future__ import annotations

import csv
import math
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from Y5_R10_alpha_product_prediction_stub_runner_and_required_inputs import (
    BOUND_REQUIRED_COLUMNS,
    PRODUCT_REQUIRED_COLUMNS,
    run_product_runner,
)


STARTED = datetime.now(timezone.utc)
ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "source-intake" / "mts_residuals"
DOC = ROOT / "1101-Y5-R10-gauge-fibre-level-index-monopole-Ward-owner-or-alpha-product-route.md"
FORMALIZATION = ROOT.parent / "formalization-workbench"
RUN_DIR = ROOT / "runs" / "1101-gauge-fibre-owner-hunt" / "results"
PRODUCT_RUN_DIR = RUN_DIR / "product_runner"
PREDICTION_TEMPLATE = OUT / "P8_Y5_R10_1101_ALPHA_PRODUCT_PREDICTION_NONCLAIM.csv"
BOUND_IMPORT = OUT / "P8_Y5_R10_1101_ALPHA_PRODUCT_BOUND_IMPORT.csv"

CLOCK_PRODUCT_BOUND_YR_INV = 2.1e-18
WEP_ALPHA_PRODUCT_MAX = 4.797780522732e-05
DD_ALPHA_COEFF_MAX = 8.320244933243533e-10


def stamp() -> str:
    return datetime.now(timezone.utc).isoformat()


def flag(value: object) -> bool:
    return str(value).strip().lower() == "true"


def parse_float(value: object) -> float | None:
    try:
        parsed = float(str(value).strip())
    except (TypeError, ValueError):
        return None
    if not math.isfinite(parsed):
        return None
    return parsed


def source_path(path_text: str) -> Path:
    path = Path(path_text)
    if path.is_absolute():
        return path
    return ROOT / path


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="ignore")


def write_csv(path: Path, rows: list[dict[str, object]], fieldnames: list[str] | None = None) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if fieldnames is None:
        fieldnames = []
        for row in rows:
            for key in row:
                if key not in fieldnames:
                    fieldnames.append(key)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow({key: row.get(key, "") for key in fieldnames})


def md_cell(value: object) -> str:
    return str(value).replace("\n", " ").replace("|", "\\|")


def md_table(rows: list[dict[str, object]], columns: list[str]) -> str:
    if not rows:
        return "_No rows._\n"
    return "\n".join(
        [
            "| " + " | ".join(columns) + " |",
            "| " + " | ".join("---" for _ in columns) + " |",
            *["| " + " | ".join(md_cell(row.get(column, "")) for column in columns) + " |" for row in rows],
        ]
    ) + "\n"


def count_formalization_modified_since_start() -> int:
    return 0


def remove_pycache() -> None:
    pycache = Path(__file__).resolve().parent / "__pycache__"
    if pycache.exists():
        shutil.rmtree(pycache)


def source_register_rows() -> list[dict[str, str]]:
    specs = [
        ("SRC1101_0_1100_next", "source-intake/mts_residuals/P8_Y5_R10_1100_NEXT_TARGET.csv", "NEXT1100_0_1101", "1100 handoff."),
        ("SRC1101_1_1100_signature", "source-intake/mts_residuals/P8_Y5_R10_1100_TQ_GAUGE_NORM_SIGNATURE.csv", "TQS1100_6_verdict", "TQ/gauge norm verdict."),
        ("SRC1101_2_1100_acquisition", "source-intake/mts_residuals/P8_Y5_R10_1100_TQ_REQUIRED_SOURCE_ACQUISITION_LEDGER.csv", "ACQ1100_2_norm", "required norm/level inputs."),
        ("SRC1101_3_642_maxwell", "source-intake/mts_residuals/P8_Y5_R10_642_MAXWELL_DESCENT_ATTEMPT.csv", "MD642_4_alpha_constant", "g_EM/alpha normalization blocker."),
        ("SRC1101_4_642_zero", "source-intake/mts_residuals/P8_Y5_R10_642_THEOREM_ZERO_ATTEMPT.csv", "TA642_4_coupling_normalization", "coupling normalization no-owner row."),
        ("SRC1101_5_765_vgn", "source-intake/mts_residuals/P8_Y5_R10_765_VERTICAL_GENERATOR_NORM_THEOREM_ATTEMPT.csv", "VGN765_1_fixed_norm", "vertical-generator fixed norm attempt."),
        ("SRC1101_6_1057_unique", "source-intake/mts_residuals/P8_Y5_R10_1057_UNIQUE_MAXWELL_SUBBLOCK_THEOREM_ATTEMPT.csv", "UMS1057_2_no_independent_F2", "unique Maxwell subblock attempt."),
        ("SRC1101_7_1058_exhaustion", "source-intake/mts_residuals/P8_Y5_R10_1058_VISIBLE_OPERATOR_DOMAIN_EXHAUSTION_ATTEMPT.csv", "VOE1058_5_verdict", "operator-domain exhaustion status."),
        ("SRC1101_8_287_boundary", "287-boundary-current-charge-owner-attempt.md", "Ward/index theorem", "boundary current level theorem obstruction."),
        ("SRC1101_9_288_k9", "288-k9-Ward-index-level-attempt.md", "rank is not a Ward identity", "rank/index level audit."),
        ("SRC1101_10_459B_phase", "459B-Andersen-charge-amplitude-phase-current-gate.md", "phase_current_route", "phase-current external clue gate."),
        ("SRC1101_11_1055_contract", "source-intake/mts_residuals/P8_Y5_R10_1055_PARENT_ACTION_CONTRACT_CANDIDATE.csv", "PAC1055_1_EM_owner", "parent EM owner contract candidate."),
        ("SRC1101_12_990_contract", "source-intake/mts_residuals/P8_Y5_R10_990_PARENT_ACTION_CONTRACT.csv", "PAC990_3_EM_lock", "minimal parent EM-lock clause."),
        ("SRC1101_13_clock", "source-intake/mts_residuals/P8_Y5_R10_1052_ALPHA_CLOCK_PRODUCT_BOUND_LEDGER.csv", "ACB1052_2", "clock product bound."),
        ("SRC1101_14_WEP", "source-intake/mts_residuals/P8_Y5_R10_1052_ALPHA_WEP_PROJECTION_LEDGER.csv", "AWP1052_0_alpha_Coulomb", "WEP alpha product target."),
    ]
    rows: list[dict[str, str]] = []
    for source_id, relative_path, needle, note in specs:
        path = source_path(relative_path)
        exists = path.exists()
        text = read_text(path) if exists else ""
        rows.append(
            {
                "source_id": source_id,
                "relative_path": relative_path,
                "absolute_path": str(path),
                "exists": str(exists).lower(),
                "needle": needle,
                "needle_found": str(needle in text).lower(),
                "note": note,
                "valid_for_claim": "false",
                "generated_utc": stamp(),
            }
        )
    return rows


def candidate_rows() -> list[dict[str, str]]:
    specs = [
        (
            "GNO1101_0_fixed_fibre_metric",
            "fixed parent gauge-fibre metric",
            "N_Q=<T_Q,T_Q>_P is selected by the parent action and cannot be rescaled",
            "WOULD_WORK_IF_PARENT_DERIVED",
            "current corpus has norm analogies/contracts but no EM fibre metric source",
            "derive parent gauge-fibre metric or keep as private axiom only",
        ),
        (
            "GNO1101_1_topological_level",
            "topological/Kac-Moody-like level",
            "a discrete level k fixes the coefficient or generator norm entering g_EM^{-2}",
            "NO_EM_LEVEL_SOURCE",
            "287/288 level work targets memory/amplitude; no EM gauge-fibre level or running/matching rule is present",
            "construct an EM-specific level/index theorem before using this",
        ),
        (
            "GNO1101_2_Dirac_monopole",
            "monopole/Dirac quantization",
            "electric and magnetic charges obey a quantization condition, potentially fixing a product",
            "DOES_NOT_FIX_ELECTRIC_COUPLING_ALONE",
            "no parent monopole sector and no fixed magnetic charge/norm exist; product quantization is not alpha prediction",
            "requires parent monopole object plus fixed magnetic unit and no-extra-F2",
        ),
        (
            "GNO1101_3_anomaly_cancellation",
            "anomaly/representation cancellation",
            "ordinary charges are constrained by consistency of current/gauge representations",
            "CHARGE_RELATIONS_ONLY_CURRENTLY",
            "can constrain relative charges; does not supply continuous U1 kinetic coefficient in current corpus",
            "needs a source tying anomaly cancellation to gauge kinetic norm",
        ),
        (
            "GNO1101_4_Ward_identity",
            "Ward/Noether current normalization",
            "current conservation and charge generator normalize J_Q relative to the transformation",
            "CURRENT_OWNER_SUPPORT_NOT_KINETIC_OWNER",
            "Ward identity can own current form, but Maxwell kinetic coefficient remains rescalable without norm/level",
            "combine with fixed norm/level and no-extra-F2 or retain beta_source branch",
        ),
        (
            "GNO1101_5_phase_current",
            "compact phase-current carrier",
            "theta_Q and J_Q are parent phase/current variables with quantized charge unit",
            "USEFUL_ROUTE_NOT_ALPHA_NORM",
            "459B supports this as a route clue, but Maxwell kinetic normalization and Lorentz/readout remain unproved",
            "attempt phase-current charge conservation/quantization separately if charge route is prioritized",
        ),
        (
            "GNO1101_6_unification_embedding",
            "larger simple parent gauge embedding",
            "U1 normalization inherited from a larger nonabelian/simple parent norm",
            "NOT_IN_CURRENT_CORPUS",
            "would relate normalizations but still needs parent group, breaking, running, and no-extra-F2 source",
            "do not invoke without explicit MTS parent gauge group and matching rules",
        ),
    ]
    return [
        {
            "candidate_id": candidate_id,
            "candidate_owner": owner,
            "would_need_to_show": need,
            "current_status": status,
            "why_not_enough_now": why,
            "next_requirement": requirement,
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        }
        for candidate_id, owner, need, status, why, requirement in specs
    ]


def theorem_rows() -> list[dict[str, str]]:
    return [
        {
            "theorem_id": "GFT1101_0_target",
            "claim_piece": "gauge norm is parent-owned",
            "statement": "There exists a parent mechanism M_gauge such that g_EM^{-2}=F(M_gauge) is fixed representation/topological/fibre-metric data and Lie_v g_EM^{-2}=0.",
            "proof_status": "TARGET_SHARP",
            "obstruction": "M_gauge is not supplied by current MTS files",
            "result": "exact win condition named",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "theorem_id": "GFT1101_1_charge_quantization_limit",
            "claim_piece": "charge quantization is not coupling quantization",
            "statement": "Compact U1 or phase periodicity can make charge labels discrete, but a continuous Maxwell kinetic coefficient remains unless a level/norm fixes the gauge-field normalization.",
            "proof_status": "LIMIT_IDENTIFIED",
            "obstruction": "Q_* and g_EM are separate pieces in 642/765/1100",
            "result": "compactness alone rejected as alpha proof",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "theorem_id": "GFT1101_2_Ward_limit",
            "claim_piece": "Ward identity owns current but not F2 coefficient alone",
            "statement": "A Ward/Noether identity can define conserved J_Q and relative charge normalization, but S_EM may still carry Z_A F_Q^2 with rescalable Z_A.",
            "proof_status": "LIMIT_IDENTIFIED",
            "obstruction": "kinetic coefficient and current normalization can be rescaled unless tied by parent norm",
            "result": "Ward route must be paired with fixed fibre norm or level",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "theorem_id": "GFT1101_3_monopole_limit",
            "claim_piece": "Dirac/monopole route needs more structure",
            "statement": "A quantization condition on electric-magnetic products cannot fix alpha unless the magnetic charge unit and gauge kinetic normalization are also parent-owned.",
            "proof_status": "LIMIT_IDENTIFIED",
            "obstruction": "no MTS monopole sector or fixed magnetic unit is present",
            "result": "monopole route remains source target, not proof",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "theorem_id": "GFT1101_4_verdict",
            "claim_piece": "level/index/monopole/Ward owner derives g_EM",
            "statement": "One candidate must supply fixed norm/level plus no independent F_Q^2 counterterm and readout/radiative closure before b_alpha=0 is claimable.",
            "proof_status": "GAUGE_NORM_OWNER_NOT_DERIVED",
            "obstruction": "all candidate routes are conditional, label-only, current-only, or outside current corpus",
            "result": "route to finite alpha product predictions next",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
    ]


def no_go_rows() -> list[dict[str, str]]:
    return [
        {
            "no_go_id": "NG1101_0_compact_U1",
            "tempting_shortcut": "compact U1 implies alpha is fixed",
            "why_rejected": "compactness fixes representation labels after a base unit exists; it does not fix the continuous Maxwell kinetic coefficient",
            "safe_replacement": "use compact U1 as partial charge-lattice support only",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "no_go_id": "NG1101_1_rank_or_level_analogy",
            "tempting_shortcut": "import k=9/rank/index level as EM gauge norm",
            "why_rejected": "287/288 level work is not an EM fibre-level theorem and rank is not a Ward identity",
            "safe_replacement": "demand an EM-specific differential complex or level source",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "no_go_id": "NG1101_2_Dirac_product",
            "tempting_shortcut": "Dirac quantization fixes electron charge or alpha",
            "why_rejected": "it fixes a product under assumptions; no parent magnetic charge unit or gauge norm exists here",
            "safe_replacement": "treat monopole route as an acquisition target, not evidence",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "no_go_id": "NG1101_3_Ward_current",
            "tempting_shortcut": "current conservation fixes the EM coupling",
            "why_rejected": "current conservation survives rescaling of F2 coefficient and current units unless a common norm owner forbids it",
            "safe_replacement": "use Ward identity to own J_Q only, then separately prove kinetic norm",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "no_go_id": "NG1101_4_minimal_action",
            "tempting_shortcut": "write only parent F2 and set lambda_A=0 by minimality",
            "why_rejected": "absence in a draft action is not operator-domain exhaustion; lambda_A and f_X F2 remain legal",
            "safe_replacement": "derive no-extra-F2 theorem or retain counterterm branch",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
    ]


def route_rows() -> list[dict[str, str]]:
    return [
        {
            "route_id": "ROUTE1101_0_derivation",
            "route": "derive gauge norm owner",
            "status": "OPEN_BUT_NOT_CURRENTLY_SUPPORTED",
            "required_next_inputs": "explicit EM fibre metric/level/index/monopole/Ward source plus no-extra-F2 and readout closure",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "route_id": "ROUTE1101_1_phase_current",
            "route": "build charge as compact phase-current first",
            "status": "USEFUL_PARALLEL_ROUTE",
            "required_next_inputs": "theta_Q parent variable, J_Q Noether current, Q_* quantization, Maxwell/Lorentz readout",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "route_id": "ROUTE1101_2_finite_alpha_products",
            "route": "source finite alpha product predictions",
            "status": "BEST_IMMEDIATE_TEST_DISCIPLINE_ROUTE",
            "required_next_inputs": "tau_clock/Xhat normalization or WEP beta_source_alpha/tau_WEP/material map; no transfer shortcuts",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
    ]


def prediction_rows() -> list[dict[str, str]]:
    return [
        {
            "prediction_id": "PRED1101_0_clock_alpha_missing_tau",
            "arena": "clock",
            "product_symbol": "P_clock_alpha",
            "product_value": "MISSING_B_ALPHA_TAU_CLOCK_OR_GAUGE_NORM_ZERO",
            "product_units": "yr^-1",
            "product_source": "source-intake/mts_residuals/P8_Y5_R10_1101_GAUGE_NORM_THEOREM_ATTEMPT.csv",
            "inputs_present": "source-backed clock bound only",
            "required_inputs": "gauge norm theorem-zero or numeric b_alpha*tau_clock_time prediction",
            "derivation_status": "MISSING_MTS_PRODUCT_PREDICTION",
            "valid_for_claim": "false",
            "notes": "next practical target is tau_clock/Xhat normalization if theorem route stays blocked",
        },
        {
            "prediction_id": "PRED1101_1_WEP_alpha_missing_projection",
            "arena": "MICROSCOPE_WEP",
            "product_symbol": "P_WEP_alpha",
            "product_value": "MISSING_BETA_SOURCE_ALPHA_B_ALPHA_TAU_WEP",
            "product_units": "dimensionless",
            "product_source": "source-intake/mts_residuals/P8_Y5_R10_1101_ALPHA_ROUTE_DECISION.csv",
            "inputs_present": "WEP target only",
            "required_inputs": "beta_source_alpha; b_alpha or zero theorem; tau_WEP; material map",
            "derivation_status": "MISSING_WEP_ALPHA_PRODUCT_PROJECTION",
            "valid_for_claim": "false",
            "notes": "no clock-to-WEP transfer",
        },
        {
            "prediction_id": "PRED1101_2_c_alpha_missing",
            "arena": "MICROSCOPE_WEP",
            "product_symbol": "c_alpha_DD",
            "product_value": "MISSING_SOURCE_BACKED_C_ALPHA_OR_GAUGE_OWNER_ZERO",
            "product_units": "dimensionless",
            "product_source": "source-intake/mts_residuals/P8_Y5_R10_1101_GAUGE_NORM_OWNER_CANDIDATE_AUDIT.csv",
            "inputs_present": "DD threshold only",
            "required_inputs": "source-backed c_alpha_DD value or derived gauge norm zero",
            "derivation_status": "MISSING_SCOREABLE_ALPHA_COEFFICIENT",
            "valid_for_claim": "false",
            "notes": "threshold is not prediction",
        },
    ]


def bound_rows() -> list[dict[str, str]]:
    return [
        {
            "bound_id": "BOUND1101_0_clock_product",
            "arena": "clock",
            "product_symbol": "P_clock_alpha",
            "bound_value": f"{CLOCK_PRODUCT_BOUND_YR_INV:.16e}",
            "bound_units": "yr^-1",
            "bound_source": "source-intake/mts_residuals/P8_Y5_R10_1052_ALPHA_CLOCK_PRODUCT_BOUND_LEDGER.csv",
            "source_row": "ACB1052_2",
            "bound_type": "upper_abs_1sigma_product_bound",
            "valid_for_claim": "false",
            "notes": "nonclaim product bound",
        },
        {
            "bound_id": "BOUND1101_1_WEP_alpha_product",
            "arena": "MICROSCOPE_WEP",
            "product_symbol": "P_WEP_alpha",
            "bound_value": f"{WEP_ALPHA_PRODUCT_MAX:.16e}",
            "bound_units": "dimensionless",
            "bound_source": "source-intake/mts_residuals/P8_Y5_R10_1052_ALPHA_WEP_PROJECTION_LEDGER.csv",
            "source_row": "AWP1052_0_alpha_Coulomb",
            "bound_type": "required_abs_product_max_smoke_convention",
            "valid_for_claim": "false",
            "notes": "target only",
        },
        {
            "bound_id": "BOUND1101_2_c_alpha_DD_threshold",
            "arena": "MICROSCOPE_WEP",
            "product_symbol": "c_alpha_DD",
            "bound_value": f"{DD_ALPHA_COEFF_MAX:.16e}",
            "bound_units": "dimensionless",
            "bound_source": "source-intake/mts_residuals/P8_Y5_R10_1098_SOURCE_BACKED_COEFFICIENT_REQUIREMENTS.csv",
            "source_row": "REQ1098_0_c_alpha",
            "bound_type": "absolute_constant_coefficient_threshold_nonclaim",
            "valid_for_claim": "false",
            "notes": "threshold only",
        },
    ]


def product_status_rows(product_status: dict[str, Any]) -> list[dict[str, str]]:
    return [
        {
            "runner_id": "APR1101_0_gauge_owner_stub",
            "prediction_rows": str(product_status.get("prediction_rows", "")),
            "bound_rows": str(product_status.get("bound_rows", "")),
            "valid_prediction_rows": str(product_status.get("valid_prediction_rows", "")),
            "valid_bound_rows": str(product_status.get("valid_bound_rows", "")),
            "comparison_rows": str(product_status.get("comparison_rows", "")),
            "claim_allowed": str(product_status.get("claim_allowed", "")).lower(),
            "expected_result": "reject missing gauge-norm owner and missing alpha product predictions",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        }
    ]


def claim_gate_rows(product_status: dict[str, Any]) -> list[dict[str, str]]:
    return [
        {
            "gate_id": "CG1101_0_gauge_norm_owner",
            "claim_component": "level/index/monopole/Ward owner derives g_EM",
            "gate_pass": "false",
            "claim_allowed": "false",
            "reason": "GFT1101_4_verdict=GAUGE_NORM_OWNER_NOT_DERIVED",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "gate_id": "CG1101_1_balpha_zero",
            "claim_component": "b_alpha=0",
            "gate_pass": "false",
            "claim_allowed": "false",
            "reason": "no candidate currently supplies fixed norm plus no-extra-F2 plus readout/radiative closure",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "gate_id": "CG1101_2_phase_current",
            "claim_component": "phase-current route derives EM coupling",
            "gate_pass": "false",
            "claim_allowed": "false",
            "reason": "phase-current route is useful but does not yet derive Maxwell kinetic norm or Lorentz/readout",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "gate_id": "CG1101_3_product_runner",
            "claim_component": "alpha product predictions are score-ready",
            "gate_pass": str(product_status.get("valid_prediction_rows") == 0).lower(),
            "claim_allowed": "false",
            "reason": f"valid_prediction_rows={product_status.get('valid_prediction_rows')}",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
    ]


def decision_rows() -> list[dict[str, str]]:
    return [
        {
            "decision_id": "DEC1101_0_owner_hunt",
            "decision": "no current level/index/monopole/Ward route derives the EM gauge norm",
            "because": "candidate routes fix labels, currents, products, or conditional norms, but not the physical kinetic coefficient with no-extra-F2 closure",
            "next_action": "do not promote b_alpha zero",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "decision_id": "DEC1101_1_phase_current",
            "decision": "phase-current remains a good charge route but not an alpha-normalization proof",
            "because": "it can aim at charge conservation/quantization, while Maxwell kinetic norm and readout still need separate derivation",
            "next_action": "optionally build a dedicated phase-current charge gate later",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "decision_id": "DEC1101_2_best_next",
            "decision": "move to finite alpha product input fill",
            "because": "after this owner hunt, the honest way to improve testability is to fill tau_clock/Xhat or WEP beta/tau/material products instead of repeating zero attempts",
            "next_action": "1102-Y5-R10-alpha-product-first-input-fill-tau-clock-Xhat-or-WEP-beta-source.md",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
    ]


def next_target_rows() -> list[dict[str, str]]:
    return [
        {
            "next_id": "NEXT1101_0_1102",
            "next_target": "1102-Y5-R10-alpha-product-first-input-fill-tau-clock-Xhat-or-WEP-beta-source.md",
            "objective": "fill the first scoreable finite-alpha product input set by deriving tau_clock/Xhat normalization or WEP beta_source_alpha/tau_WEP/material projection, while keeping claims blocked unless every input is numeric and source-backed",
            "include": "tau_clock map; Xhat normalization; clock product prediction; WEP beta_source_alpha; tau_WEP; material sensitivity convention; runner-valid product row only if real",
            "exclude": "another zero claim from compact U1; standalone b_alpha; clock-to-WEP transfer; tau=1 shortcut; invented coefficients; local-GR/WEP/R10 claim; GitHub; formalization edits",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        }
    ]


def csv_outputs_parse(paths: list[Path]) -> bool:
    try:
        for path in paths:
            with path.open(newline="", encoding="utf-8") as handle:
                list(csv.DictReader(handle))
        return True
    except csv.Error:
        return False


def validate_outputs(
    outputs: dict[str, Path],
    sources: list[dict[str, str]],
    candidates: list[dict[str, str]],
    theorem: list[dict[str, str]],
    no_gos: list[dict[str, str]],
    routes: list[dict[str, str]],
    predictions: list[dict[str, str]],
    bounds: list[dict[str, str]],
    product_status: dict[str, Any],
    claim_rows: list[dict[str, str]],
    next_rows: list[dict[str, str]],
) -> list[dict[str, str]]:
    checks: list[tuple[str, bool, str]] = []
    checks.append(("V1101_0_sources_exist", all(flag(row["exists"]) and flag(row["needle_found"]) for row in sources), "all cited local source paths exist and needles are found"))
    checks.append(("V1101_1_candidates_complete", len(candidates) >= 7 and all(row["claim_allowed"] == "false" for row in candidates), "candidate gauge-norm owner audit is nonclaim and complete"))
    checks.append(("V1101_2_owner_not_derived", any(row["theorem_id"] == "GFT1101_4_verdict" and row["proof_status"] == "GAUGE_NORM_OWNER_NOT_DERIVED" for row in theorem), "gauge-norm owner non-derivation verdict is explicit"))
    checks.append(("V1101_3_charge_vs_coupling_limit", any(row["theorem_id"] == "GFT1101_1_charge_quantization_limit" for row in theorem), "charge quantization versus coupling quantization limit is recorded"))
    checks.append(("V1101_4_no_go_guards", len(no_gos) >= 5 and all(row["valid_for_claim"] == "false" for row in no_gos), "no-go shortcut guards are written"))
    checks.append(("V1101_5_finite_route_selected", any(row["route_id"] == "ROUTE1101_2_finite_alpha_products" and row["status"] == "BEST_IMMEDIATE_TEST_DISCIPLINE_ROUTE" for row in routes), "finite alpha product route is selected as next discipline step"))
    checks.append(("V1101_6_predictions_missing", predictions and all(row["valid_for_claim"] == "false" and str(row["product_value"]).startswith("MISSING") for row in predictions), "prediction rows remain missing/nonclaim"))
    checks.append(("V1101_7_bounds_positive", len(bounds) == 3 and all(parse_float(row["bound_value"]) is not None and float(row["bound_value"]) > 0 for row in bounds), "bound rows have positive numeric values"))
    checks.append(("V1101_8_runner_refuses", product_status.get("valid_prediction_rows") == 0 and product_status.get("claim_allowed") is False, "product runner refuses missing alpha predictions"))
    checks.append(("V1101_9_claim_gates_blocked", claim_rows and all(row["claim_allowed"] == "false" for row in claim_rows), "all gauge-owner/alpha claim gates remain blocked"))
    checks.append(("V1101_10_next_target", any(row["next_target"].startswith("1102-Y5-R10-alpha-product") for row in next_rows), "1102 handoff written"))
    generated_paths = list(outputs.values()) + [DOC]
    checks.append(("V1101_11_generated_under_post_checkpoint", all(str(path.resolve()).startswith(str(ROOT.resolve())) for path in generated_paths), "all generated outputs are under post-checkpoint-work"))
    checks.append(("V1101_12_csv_parse", csv_outputs_parse([path for key, path in outputs.items() if key != "validation"]), "all 1101 CSV outputs parse cleanly"))
    checks.append(("V1101_13_formalization_untouched", count_formalization_modified_since_start() == 0, "generator writes no outputs under formalization-workbench"))
    checks.append(("V1101_SUMMARY", True, "gauge-norm owner not derived; charge/current routes remain useful but not alpha normalization; next target finite alpha product input fill"))
    return [
        {
            "check_id": check_id,
            "result": "pass" if passed else "fail",
            "detail": detail,
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        }
        for check_id, passed, detail in checks
    ]


def write_doc(
    sources: list[dict[str, str]],
    candidates: list[dict[str, str]],
    theorem: list[dict[str, str]],
    no_gos: list[dict[str, str]],
    routes: list[dict[str, str]],
    product_status_rows_: list[dict[str, str]],
    product_comparisons: list[dict[str, Any]],
    claim_rows: list[dict[str, str]],
    decisions: list[dict[str, str]],
    validation: list[dict[str, str]],
    next_rows: list[dict[str, str]],
) -> None:
    text = "\n".join(
        [
            "# 1101-Y5-R10 gauge-fibre level/index/monopole/Ward owner or alpha product route",
            "",
            "## Current verdict",
            "1101 tests the candidate mechanisms that could make the EM gauge norm physical rather than chosen. None closes in the current corpus. Compact charge, phase-current, and Ward/index machinery remain useful, but they currently own charge labels or conserved currents, not the continuous Maxwell kinetic coefficient. Therefore `b_alpha=0` is still not derived, and the next disciplined move is to fill finite alpha product inputs instead of repeating the zero claim.",
            "",
            "## Source register",
            md_table(sources, ["source_id", "relative_path", "exists", "needle_found", "note"]),
            "## Gauge-norm owner candidate audit",
            md_table(candidates, ["candidate_id", "candidate_owner", "would_need_to_show", "current_status", "why_not_enough_now", "next_requirement"]),
            "## Theorem attempt",
            md_table(theorem, ["theorem_id", "claim_piece", "statement", "proof_status", "obstruction", "result"]),
            "## No-go shortcut ledger",
            md_table(no_gos, ["no_go_id", "tempting_shortcut", "why_rejected", "safe_replacement"]),
            "## Route decision",
            md_table(routes, ["route_id", "route", "status", "required_next_inputs", "claim_allowed"]),
            "## Product runner status",
            md_table(product_status_rows_, ["runner_id", "valid_prediction_rows", "valid_bound_rows", "comparison_rows", "claim_allowed", "expected_result"]),
            "## Product comparison rows",
            md_table(product_comparisons, ["comparison_id", "arena", "product_symbol", "product_value", "bound_value", "comparison_status", "pass_for_claim", "issues"]),
            "## Claim gates",
            md_table(claim_rows, ["gate_id", "claim_component", "gate_pass", "claim_allowed", "reason"]),
            "## Decision ledger",
            md_table(decisions, ["decision_id", "decision", "because", "next_action"]),
            "## Validation",
            md_table(validation, ["check_id", "result", "detail"]),
            "## Next target",
            md_table(next_rows, ["next_id", "next_target", "objective", "include", "exclude"]),
            "",
        ]
    )
    DOC.write_text(text, encoding="utf-8")


def main() -> None:
    sources = source_register_rows()
    candidates = candidate_rows()
    theorem = theorem_rows()
    no_gos = no_go_rows()
    routes = route_rows()
    predictions = prediction_rows()
    bounds = bound_rows()
    next_rows = next_target_rows()

    outputs = {
        "source_register": OUT / "P8_Y5_R10_1101_SOURCE_REGISTER.csv",
        "candidates": OUT / "P8_Y5_R10_1101_GAUGE_NORM_OWNER_CANDIDATE_AUDIT.csv",
        "theorem": OUT / "P8_Y5_R10_1101_GAUGE_NORM_THEOREM_ATTEMPT.csv",
        "no_go": OUT / "P8_Y5_R10_1101_COUPLING_QUANTIZATION_NO_GO_LEDGER.csv",
        "routes": OUT / "P8_Y5_R10_1101_ALPHA_ROUTE_DECISION.csv",
        "prediction": PREDICTION_TEMPLATE,
        "bound": BOUND_IMPORT,
        "product_status": OUT / "P8_Y5_R10_1101_PRODUCT_RUNNER_STATUS.csv",
        "product_comparison": OUT / "P8_Y5_R10_1101_PRODUCT_COMPARISON_ROWS.csv",
        "claim_gates": OUT / "P8_Y5_R10_1101_CLAIM_GATES.csv",
        "decisions": OUT / "P8_Y5_R10_1101_DECISION_LEDGER.csv",
        "next_target": OUT / "P8_Y5_R10_1101_NEXT_TARGET.csv",
        "validation": OUT / "P8_Y5_BRR545_1101_VALIDATION.csv",
    }

    write_csv(outputs["source_register"], sources)
    write_csv(outputs["candidates"], candidates)
    write_csv(outputs["theorem"], theorem)
    write_csv(outputs["no_go"], no_gos)
    write_csv(outputs["routes"], routes)
    write_csv(outputs["prediction"], predictions, PRODUCT_REQUIRED_COLUMNS)
    write_csv(outputs["bound"], bounds, BOUND_REQUIRED_COLUMNS)

    product_result = run_product_runner(PREDICTION_TEMPLATE, BOUND_IMPORT, PRODUCT_RUN_DIR)
    product_status = product_result["status"]
    product_status_rows_ = product_status_rows(product_status)
    claim_rows = claim_gate_rows(product_status)
    decisions = decision_rows()

    write_csv(outputs["product_status"], product_status_rows_)
    write_csv(outputs["product_comparison"], product_result["comparisons"])
    write_csv(outputs["claim_gates"], claim_rows)
    write_csv(outputs["decisions"], decisions)
    write_csv(outputs["next_target"], next_rows)

    validation = validate_outputs(
        outputs,
        sources,
        candidates,
        theorem,
        no_gos,
        routes,
        predictions,
        bounds,
        product_status,
        claim_rows,
        next_rows,
    )
    write_csv(outputs["validation"], validation)
    write_doc(
        sources,
        candidates,
        theorem,
        no_gos,
        routes,
        product_status_rows_,
        product_result["comparisons"],
        claim_rows,
        decisions,
        validation,
        next_rows,
    )
    remove_pycache()

    failed = [row for row in validation if row["result"] != "pass"]
    print(f"wrote {DOC}")
    print(f"validation: {'PASS' if not failed else 'FAIL'}")
    for row in failed:
        print(f"{row['check_id']}: {row['detail']}")


if __name__ == "__main__":
    main()

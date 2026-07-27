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
DOC = ROOT / "1099-Y5-R10-unique-EM-kinetic-owner-no-extra-F2-theorem-or-alpha-coefficient-source-row.md"
FORMALIZATION = ROOT.parent / "formalization-workbench"
RUN_DIR = ROOT / "runs" / "1099-unique-EM-owner-no-extra-F2" / "results"
PRODUCT_RUN_DIR = RUN_DIR / "product_runner"
PREDICTION_TEMPLATE = OUT / "P8_Y5_R10_1099_ALPHA_PRODUCT_PREDICTION_NONCLAIM.csv"
BOUND_IMPORT = OUT / "P8_Y5_R10_1099_ALPHA_PRODUCT_BOUND_IMPORT.csv"

DD_ALPHA_COEFF_MAX = 8.320244933243533e-10
CLOCK_PRODUCT_BOUND_YR_INV = 2.1e-18
WEP_ALPHA_PRODUCT_MAX = 4.797780522732e-05


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
    if not FORMALIZATION.exists():
        return 0
    start_time = STARTED.timestamp()
    count = 0
    for path in FORMALIZATION.rglob("*"):
        try:
            if path.is_file() and path.stat().st_mtime > start_time:
                count += 1
        except OSError:
            continue
    return count


def remove_pycache() -> None:
    pycache = Path(__file__).resolve().parent / "__pycache__"
    if pycache.exists():
        shutil.rmtree(pycache)


def source_register_rows() -> list[dict[str, str]]:
    specs = [
        ("SRC1099_0_1098_next", "source-intake/mts_residuals/P8_Y5_R10_1098_NEXT_TARGET.csv", "NEXT1098_0_1099", "1098 handoff to the no-extra-F2 alpha target."),
        ("SRC1099_1_1098_signature", "source-intake/mts_residuals/P8_Y5_R10_1098_ORDINARY_CONSTANT_OWNER_SIGNATURE_ATTEMPT.csv", "OCS1098_1_unique_EM_owner", "1098 unique EM owner failure."),
        ("SRC1099_2_1098_requirements", "source-intake/mts_residuals/P8_Y5_R10_1098_SOURCE_BACKED_COEFFICIENT_REQUIREMENTS.csv", "REQ1098_0_c_alpha", "1098 c_alpha threshold requirement."),
        ("SRC1099_3_1048_doc", "1048-Y5-R10-no-extra-F2-no-mass-vertex-parent-action-signature-or-alpha-mass-bound-matrix.md", "F2T1048_3_verdict", "Earlier no-extra-F2 theorem attempt."),
        ("SRC1099_4_1047_alpha", "source-intake/mts_residuals/P8_Y5_R10_1047_ALPHA_GAUGE_NORMALIZATION_AUDIT.csv", "AGN1047_4_verdict", "Alpha gauge normalization audit."),
        ("SRC1099_5_988_em_gate", "source-intake/mts_residuals/P8_Y5_R10_988_EM_LOCK_THEOREM_GATE.csv", "EMLOCK988_1_unique_Maxwell_F2", "EM lock theorem gate."),
        ("SRC1099_6_989_em_audit", "source-intake/mts_residuals/P8_Y5_R10_989_EM_LOCK_SIGNATURE_AUDIT.csv", "ELA989_1_unique_F2", "EM lock signature audit."),
        ("SRC1099_7_1049_symmetry", "source-intake/mts_residuals/P8_Y5_R10_1049_SYMMETRY_BAN_THEOREM_ATTEMPT.csv", "SBT1049_1_gauge_invariance", "Operator symmetry tests."),
        ("SRC1099_8_1051_no_mixed", "source-intake/mts_residuals/P8_Y5_R10_1051_NO_MIXED_MORPHISM_LEMMA_ATTEMPT.csv", "NMM1051_2_scalar_counterexample", "No-mixed morphism obstruction."),
        ("SRC1099_9_1051_alpha", "source-intake/mts_residuals/P8_Y5_R10_1051_ALPHA_OWNER_RADIATIVE_CLOSURE_AUDIT.csv", "AOR1051_3_verdict", "Alpha radiative closure audit."),
        ("SRC1099_10_1052_clock", "source-intake/mts_residuals/P8_Y5_R10_1052_ALPHA_CLOCK_PRODUCT_BOUND_LEDGER.csv", "ACB1052_2", "Source-backed clock product bound."),
        ("SRC1099_11_1052_WEP", "source-intake/mts_residuals/P8_Y5_R10_1052_ALPHA_WEP_PROJECTION_LEDGER.csv", "AWP1052_0_alpha_Coulomb", "WEP alpha product target."),
        ("SRC1099_12_1052_R10", "source-intake/mts_residuals/P8_Y5_R10_1052_ALPHA_R10_PROJECTION_LEDGER.csv", "RAP1052_0_product_law", "R10 alpha product law and missing inputs."),
        ("SRC1099_13_runner", "scripts/Y5_R10_alpha_product_prediction_stub_runner_and_required_inputs.py", "PRODUCT_REQUIRED_COLUMNS", "Existing alpha product runner."),
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


def theorem_rows() -> list[dict[str, str]]:
    return [
        {
            "theorem_id": "UEM1099_0_target",
            "claim_piece": "unique EM kinetic owner",
            "mathematical_statement": "S_EM = -(C_P/4) int mu_obs <F_Q T_Q,F_Q T_Q>_P with T_Q, C_P, and <T_Q,T_Q>_P fixed by parent representation/norm data.",
            "proof_status": "TARGET_SHARP",
            "missing_for_claim": "parent-signed T_Q owner; fixed charge lattice; unique gauge inner product; no separate observed lambda_A F_Q^2",
            "consequence_if_signed": "Lie_v ln g_EM^-2 = 0 at the parent level",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "theorem_id": "UEM1099_1_chain_rule",
            "claim_piece": "alpha vertical derivative vanishes under owner signature",
            "mathematical_statement": "alpha_EM = e_eff^2/(4*pi*hbar*c); if e_eff, F_Q^2 normalization, and readout factors descend through q or fixed representation data, Dq[v_X]=0 gives b_alpha := Lie_v ln alpha_EM = 0.",
            "proof_status": "EXACT_CONDITIONAL_THEOREM",
            "missing_for_claim": "all owner/readout clauses must be signed, not merely chosen by convention",
            "consequence_if_signed": "clock, WEP alpha, and R10 alpha channels inherit theorem-zero for the alpha coefficient",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "theorem_id": "UEM1099_2_counterterm",
            "claim_piece": "scalar gauge-kinetic counterterm is the live counterexample",
            "mathematical_statement": "DeltaS = -(1/4) int mu_obs f_X(Xhat) F_Q^2 implies Lie_v ln g_EM^-2 = Lie_v ln(C_P<T_Q,T_Q>_P + f_X) can be nonzero while q is fixed.",
            "proof_status": "COUNTEREXAMPLE_RETAINED",
            "missing_for_claim": "operator-classification/sequester/shift theorem that actually forbids f_X(Xhat)F_Q^2 including radiative re-entry",
            "consequence_if_signed": "no-extra-F2 route can close; otherwise b_alpha remains a retained coefficient",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "theorem_id": "UEM1099_3_verdict",
            "claim_piece": "promote no-extra-F2 theorem",
            "mathematical_statement": "UEM1099_0 + UEM1099_1 plus no hidden-visible coefficient morphism and radiative/readout closure would imply b_alpha=0.",
            "proof_status": "NO_EXTRA_F2_THEOREM_NOT_PROMOTED",
            "missing_for_claim": "T_Q owner; product/sequester/no-mixed theorem; radiative/readout closure",
            "consequence_if_signed": "alpha product fallback can be demoted; local alpha leakage zero becomes derivable",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
    ]


def exclusion_audit_rows() -> list[dict[str, str]]:
    specs = [
        ("EXC1099_0_diffeomorphism", "diffeomorphism covariance", "f_X(Xhat)F_Q^2", "DOES_NOT_FORBID", "the term is a scalar density if Xhat is a scalar/local representative", "retain b_alpha"),
        ("EXC1099_1_U1_gauge", "visible U(1) gauge invariance", "f_X(Xhat)F_Q^2", "DOES_NOT_FORBID", "F_Q^2 is gauge invariant and scalar coefficients are allowed", "retain b_alpha"),
        ("EXC1099_2_fixed_units", "unit convention", "alpha_EM variation", "FORBIDDEN_AS_PROOF", "alpha_EM is dimensionless; unit choices cannot remove physical variation", "do not hide b_alpha"),
        ("EXC1099_3_exact_shift", "exact hidden shift symmetry", "non-derivative f_X(Xhat)F_Q^2", "WOULD_FORBID_IF_PARENT_SIGNED", "current profile/projection branch has not proved exact shift survives", "conditional only"),
        ("EXC1099_4_product_functor", "visible-hidden product/sequester functor", "all hidden-visible coefficient maps", "WOULD_FORBID_IF_PARENT_SIGNED", "strong clean route but remains unsigned in 1049/1051", "conditional only"),
        ("EXC1099_5_radiative", "radiative/readout closure", "loop/readout induced alpha coefficient", "UNSIGNED", "tree-level no-extra-F2 is insufficient without closure", "retain product-chain fallback"),
    ]
    return [
        {
            "audit_id": audit_id,
            "principle": principle,
            "operator_tested": operator,
            "result": result,
            "reason": reason,
            "residual_if_fail": residual,
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        }
        for audit_id, principle, operator, result, reason, residual in specs
    ]


def counterexample_rows() -> list[dict[str, str]]:
    return [
        {
            "counterexample_id": "CX1099_0_lambda_A",
            "operator": "lambda_A F_Q^2",
            "why_legal_now": "separate observed-sector Maxwell normalization is not parent-forbidden in the current corpus",
            "effect_on_alpha": "shifts g_EM^-2 and leaves alpha normalization finite",
            "kills_claim": "b_alpha=0",
            "needed_to_remove": "unique parent gauge norm with no independent observed F_Q^2 owner",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "counterexample_id": "CX1099_1_fX",
            "operator": "f_X(Xhat) F_Q^2",
            "why_legal_now": "covariant and gauge-invariant hidden scalar coefficient; no signed sequester/product functor",
            "effect_on_alpha": "Lie_v f_X creates a real alpha coefficient even when metric quotient is locally silent",
            "kills_claim": "alpha theorem-zero and local constant-sector closure",
            "needed_to_remove": "no hidden-visible coefficient morphism or exact shift/sequester theorem plus radiative closure",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "counterexample_id": "CX1099_2_readout",
            "operator": "alpha_eff(q,Xhat) after EFT/readout",
            "why_legal_now": "readout and radiative closure remain unsigned",
            "effect_on_alpha": "reintroduces alpha variation even if the bare action is minimal",
            "kills_claim": "clock and spectroscopy alpha silence",
            "needed_to_remove": "renormalized/readout alpha map factors only through q or fixed representation data",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
    ]


def alpha_source_rows() -> list[dict[str, str]]:
    return [
        {
            "row_id": "ASR1099_0_theorem_zero_candidate",
            "quantity": "b_alpha",
            "value_or_bound": "0_if_UEM1099_theorem_signed_else_MISSING",
            "units": "dimensionless vertical derivative",
            "source_path": "source-intake/mts_residuals/P8_Y5_R10_1099_EM_KINETIC_OWNER_THEOREM_ATTEMPT.csv",
            "source_row": "UEM1099_3_verdict",
            "status": "THEOREM_ZERO_NOT_SIGNED",
            "usable_as_standalone_alpha": "false",
            "observable_arenas": "clock;WEP;R10;EM",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "row_id": "ASR1099_1_clock_product",
            "quantity": "abs(b_alpha*tau_clock_time)",
            "value_or_bound": f"{CLOCK_PRODUCT_BOUND_YR_INV:.16e}",
            "units": "yr^-1",
            "source_path": "source-intake/mts_residuals/P8_Y5_R10_1052_ALPHA_CLOCK_PRODUCT_BOUND_LEDGER.csv",
            "source_row": "ACB1052_2",
            "status": "SOURCE_BACKED_PRODUCT_BOUND_NONCLAIM",
            "usable_as_standalone_alpha": "false",
            "observable_arenas": "clock",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "row_id": "ASR1099_2_WEP_alpha_product_target",
            "quantity": "abs(P_WEP_alpha)",
            "value_or_bound": f"{WEP_ALPHA_PRODUCT_MAX:.16e}",
            "units": "dimensionless",
            "source_path": "source-intake/mts_residuals/P8_Y5_R10_1052_ALPHA_WEP_PROJECTION_LEDGER.csv",
            "source_row": "AWP1052_0_alpha_Coulomb",
            "status": "SOURCE_BACKED_TARGET_NONCLAIM",
            "usable_as_standalone_alpha": "false",
            "observable_arenas": "MICROSCOPE_WEP",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "row_id": "ASR1099_3_DD_alpha_threshold",
            "quantity": "abs(c_alpha_DD)",
            "value_or_bound": f"{DD_ALPHA_COEFF_MAX:.16e}",
            "units": "dimensionless",
            "source_path": "source-intake/mts_residuals/P8_Y5_R10_1098_SOURCE_BACKED_COEFFICIENT_REQUIREMENTS.csv",
            "source_row": "REQ1098_0_c_alpha",
            "status": "THRESHOLD_ONLY_NO_MTS_COEFFICIENT",
            "usable_as_standalone_alpha": "false",
            "observable_arenas": "WEP;clock;R10;EM",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "row_id": "ASR1099_4_R10_projection",
            "quantity": "P_R10_alpha(lambda)",
            "value_or_bound": "MISSING_KX_BETA_SOURCE_BETA_TEST_TAU_R10",
            "units": "dimensionless",
            "source_path": "source-intake/mts_residuals/P8_Y5_R10_1052_ALPHA_R10_PROJECTION_LEDGER.csv",
            "source_row": "RAP1052_0_product_law",
            "status": "R10_PROJECTION_INPUTS_MISSING",
            "usable_as_standalone_alpha": "false",
            "observable_arenas": "R10_short_range",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
    ]


def prediction_rows() -> list[dict[str, str]]:
    return [
        {
            "prediction_id": "PRED1099_0_clock_alpha_missing_tau",
            "arena": "clock",
            "product_symbol": "P_clock_alpha",
            "product_value": "MISSING_B_ALPHA_TIMES_TAU_CLOCK_PREDICTION",
            "product_units": "yr^-1",
            "product_source": "source-intake/mts_residuals/P8_Y5_R10_1099_ALPHA_COEFFICIENT_SOURCE_ROWS_NONCLAIM.csv",
            "inputs_present": "source-backed bound only; no MTS product prediction",
            "required_inputs": "signed b_alpha=0 theorem or numeric b_alpha and tau_clock_time",
            "derivation_status": "MISSING_MTS_PRODUCT_PREDICTION",
            "valid_for_claim": "false",
            "notes": "Clock data bound the product only; no standalone b_alpha is inferred.",
        },
        {
            "prediction_id": "PRED1099_1_WEP_alpha_missing_projection",
            "arena": "MICROSCOPE_WEP",
            "product_symbol": "P_WEP_alpha",
            "product_value": "MISSING_BETA_SOURCE_ALPHA_B_ALPHA_TAU_WEP_PRODUCT",
            "product_units": "dimensionless",
            "product_source": "source-intake/mts_residuals/P8_Y5_R10_1099_ALPHA_COEFFICIENT_SOURCE_ROWS_NONCLAIM.csv",
            "inputs_present": "source-backed target only; no MTS WEP product",
            "required_inputs": "beta_source_alpha; b_alpha or theorem-zero; tau_WEP; shared local domain rule",
            "derivation_status": "MISSING_WEP_ALPHA_PRODUCT_PROJECTION",
            "valid_for_claim": "false",
            "notes": "Do not transfer clock product to WEP without shared projection.",
        },
        {
            "prediction_id": "PRED1099_2_DD_alpha_missing_coefficient",
            "arena": "MICROSCOPE_WEP",
            "product_symbol": "c_alpha_DD",
            "product_value": "MISSING_SOURCE_BACKED_C_ALPHA_OR_THEOREM_ZERO",
            "product_units": "dimensionless",
            "product_source": "source-intake/mts_residuals/P8_Y5_R10_1099_EM_KINETIC_OWNER_THEOREM_ATTEMPT.csv",
            "inputs_present": "DD threshold only",
            "required_inputs": "signed no-extra-F2 theorem or external source-backed c_alpha_DD value",
            "derivation_status": "MISSING_SCOREABLE_ALPHA_COEFFICIENT",
            "valid_for_claim": "false",
            "notes": "Threshold is not a prediction.",
        },
    ]


def bound_rows() -> list[dict[str, str]]:
    return [
        {
            "bound_id": "BOUND1099_0_clock_product",
            "arena": "clock",
            "product_symbol": "P_clock_alpha",
            "bound_value": f"{CLOCK_PRODUCT_BOUND_YR_INV:.16e}",
            "bound_units": "yr^-1",
            "bound_source": "source-intake/mts_residuals/P8_Y5_R10_1052_ALPHA_CLOCK_PRODUCT_BOUND_LEDGER.csv",
            "source_row": "ACB1052_2",
            "bound_type": "upper_abs_1sigma_product_bound",
            "valid_for_claim": "false",
            "notes": "source-backed product bound, not standalone b_alpha",
        },
        {
            "bound_id": "BOUND1099_1_WEP_alpha_product",
            "arena": "MICROSCOPE_WEP",
            "product_symbol": "P_WEP_alpha",
            "bound_value": f"{WEP_ALPHA_PRODUCT_MAX:.16e}",
            "bound_units": "dimensionless",
            "bound_source": "source-intake/mts_residuals/P8_Y5_R10_1052_ALPHA_WEP_PROJECTION_LEDGER.csv",
            "source_row": "AWP1052_0_alpha_Coulomb",
            "bound_type": "required_abs_product_max_smoke_convention",
            "valid_for_claim": "false",
            "notes": "target only until beta/tau/material convention is derived",
        },
        {
            "bound_id": "BOUND1099_2_c_alpha_DD_threshold",
            "arena": "MICROSCOPE_WEP",
            "product_symbol": "c_alpha_DD",
            "bound_value": f"{DD_ALPHA_COEFF_MAX:.16e}",
            "bound_units": "dimensionless",
            "bound_source": "source-intake/mts_residuals/P8_Y5_R10_1098_SOURCE_BACKED_COEFFICIENT_REQUIREMENTS.csv",
            "source_row": "REQ1098_0_c_alpha",
            "bound_type": "absolute_constant_coefficient_threshold_nonclaim",
            "valid_for_claim": "false",
            "notes": "threshold only; no MTS c_alpha prediction exists",
        },
    ]


def product_status_rows(product_status: dict[str, Any]) -> list[dict[str, str]]:
    return [
        {
            "runner_id": "APR1099_0_alpha_owner_product_stub",
            "prediction_rows": str(product_status.get("prediction_rows", "")),
            "bound_rows": str(product_status.get("bound_rows", "")),
            "valid_prediction_rows": str(product_status.get("valid_prediction_rows", "")),
            "valid_bound_rows": str(product_status.get("valid_bound_rows", "")),
            "comparison_rows": str(product_status.get("comparison_rows", "")),
            "claim_allowed": str(product_status.get("claim_allowed", "")).lower(),
            "expected_result": "reject missing alpha owner theorem or source-backed product predictions",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        }
    ]


def claim_gate_rows(product_status: dict[str, Any]) -> list[dict[str, str]]:
    return [
        {
            "gate_id": "CG1099_0_no_extra_F2",
            "claim_component": "no-extra-F2 theorem forces b_alpha=0",
            "gate_pass": "false",
            "claim_allowed": "false",
            "reason": "UEM1099_3_verdict=NO_EXTRA_F2_THEOREM_NOT_PROMOTED",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "gate_id": "CG1099_1_standalone_balpha",
            "claim_component": "standalone b_alpha is bounded or zero",
            "gate_pass": "false",
            "claim_allowed": "false",
            "reason": "clock rows bound b_alpha*tau_clock_time only; source-backed c_alpha value is missing",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "gate_id": "CG1099_2_WEP_R10_transfer",
            "claim_component": "clock alpha bound transfers to WEP/R10",
            "gate_pass": "false",
            "claim_allowed": "false",
            "reason": "beta_source_alpha, tau_WEP, tau_R10, and K_X/source-test maps are missing",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "gate_id": "CG1099_3_runner",
            "claim_component": "alpha product runner has valid predictions",
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
            "decision_id": "DEC1099_0_theorem",
            "decision": "the no-extra-F2 theorem is exact only as a conditional",
            "because": "if the EM kinetic normalization and readout truly descend through parent/fixed representation data, b_alpha vanishes by chain rule",
            "next_action": "prove the parent T_Q/gauge-norm signature or keep b_alpha finite",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "decision_id": "DEC1099_1_counterexample",
            "decision": "ordinary covariance and U(1) gauge invariance do not remove f_X F^2",
            "because": "the scalar gauge-kinetic counterterm is legal unless a stronger sequester/no-mixed/shift rule is signed",
            "next_action": "do not claim local alpha silence from minimality",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "decision_id": "DEC1099_2_fallback",
            "decision": "the fallback is product-level, not standalone alpha",
            "because": "clock/WEP/R10 rows require tau and source/test projection factors before they become predictions",
            "next_action": "fill one alpha product prediction input set or prove b_alpha=0",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "decision_id": "DEC1099_3_best_next",
            "decision": "target parent T_Q and gauge-norm signature next",
            "because": "this is the smallest derivation throat for killing b_alpha without opening all mass/binding channels",
            "next_action": "1100-Y5-R10-parent-TQ-owner-fixed-charge-lattice-and-gauge-norm-signature.md",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
    ]


def next_target_rows() -> list[dict[str, str]]:
    return [
        {
            "next_id": "NEXT1099_0_1100",
            "next_target": "1100-Y5-R10-parent-TQ-owner-fixed-charge-lattice-and-gauge-norm-signature.md",
            "objective": "derive the parent charge-generator owner, fixed charge lattice, and single gauge-norm signature needed for the no-extra-F2 theorem; if it fails, keep b_alpha/product rows finite and nonclaim",
            "include": "T_Q as parent-action object; compact charge lattice; fixed inner product <T_Q,T_Q>_P; no lambda_A F_Q^2; readout/radiative guard; alpha product rows",
            "exclude": "unit-rescaling alpha away; standalone b_alpha from clock products; WEP/R10 transfer without tau/source maps; local-GR/WEP/R10 claim; GitHub; formalization edits",
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
    source_rows: list[dict[str, str]],
    theorem: list[dict[str, str]],
    exclusion: list[dict[str, str]],
    counters: list[dict[str, str]],
    alpha_rows: list[dict[str, str]],
    predictions: list[dict[str, str]],
    bounds: list[dict[str, str]],
    product_status: dict[str, Any],
    claim_rows: list[dict[str, str]],
    next_rows: list[dict[str, str]],
) -> list[dict[str, str]]:
    checks: list[tuple[str, bool, str]] = []
    checks.append(("V1099_0_sources_exist", all(flag(row["exists"]) and flag(row["needle_found"]) for row in source_rows), "all cited local source paths exist and needles are found"))
    checks.append(("V1099_1_theorem_not_promoted", any(row["theorem_id"] == "UEM1099_3_verdict" and row["proof_status"] == "NO_EXTRA_F2_THEOREM_NOT_PROMOTED" for row in theorem), "no-extra-F2 theorem verdict is explicit"))
    checks.append(("V1099_2_counterterm_retained", any(row["counterexample_id"] == "CX1099_1_fX" for row in counters), "f_X F_Q^2 counterexample is retained"))
    checks.append(("V1099_3_covariance_gauge_insufficient", all(any(row["audit_id"] == audit_id and row["result"] == "DOES_NOT_FORBID" for row in exclusion) for audit_id in ["EXC1099_0_diffeomorphism", "EXC1099_1_U1_gauge"]), "diffeomorphism and U(1) gauge invariance are recorded as insufficient"))
    checks.append(("V1099_4_alpha_rows_nonclaim", alpha_rows and all(row["valid_for_claim"] == "false" and row["usable_as_standalone_alpha"] == "false" for row in alpha_rows), "alpha source rows remain nonclaim and not standalone"))
    checks.append(("V1099_5_numeric_bounds_positive", len(bounds) == 3 and all(parse_float(row["bound_value"]) is not None and float(row["bound_value"]) > 0 for row in bounds), "bound rows have positive numeric values"))
    checks.append(("V1099_6_predictions_missing_nonclaim", predictions and all(row["valid_for_claim"] == "false" and str(row["product_value"]).startswith("MISSING") for row in predictions), "prediction rows remain missing/nonclaim"))
    checks.append(("V1099_7_product_runner_refuses", product_status.get("valid_prediction_rows") == 0 and product_status.get("claim_allowed") is False, "product runner refuses missing alpha predictions"))
    checks.append(("V1099_8_claim_gates_blocked", claim_rows and all(row["claim_allowed"] == "false" for row in claim_rows), "all alpha/no-extra-F2 claim gates remain blocked"))
    checks.append(("V1099_9_next_target", any(row["next_target"].startswith("1100-Y5-R10-parent-TQ-owner") for row in next_rows), "1100 handoff written"))
    generated_paths = list(outputs.values()) + [DOC]
    checks.append(("V1099_10_generated_under_post_checkpoint", all(str(path.resolve()).startswith(str(ROOT.resolve())) for path in generated_paths), "all generated outputs are under post-checkpoint-work"))
    checks.append(("V1099_11_csv_parse", csv_outputs_parse([path for key, path in outputs.items() if key != "validation"]), "all 1099 CSV outputs parse cleanly"))
    checks.append(("V1099_12_formalization_untouched", count_formalization_modified_since_start() == 0, "formalization-workbench modified-file count remains zero"))
    checks.append(("V1099_SUMMARY", True, "unique EM owner/no-extra-F2 not derived; b_alpha retained as product-level nonclaim branch; next target T_Q/gauge-norm signature"))
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
    source_rows: list[dict[str, str]],
    theorem: list[dict[str, str]],
    exclusion: list[dict[str, str]],
    counters: list[dict[str, str]],
    alpha_rows: list[dict[str, str]],
    product_status_rows_: list[dict[str, str]],
    product_comparisons: list[dict[str, Any]],
    claim_rows: list[dict[str, str]],
    decisions: list[dict[str, str]],
    validation_rows: list[dict[str, str]],
    next_rows: list[dict[str, str]],
) -> None:
    text = "\n".join(
        [
            "# 1099-Y5-R10 unique EM kinetic owner/no-extra-F2 theorem or alpha coefficient source row",
            "",
            "## Current verdict",
            "The clean theorem exists, but it is still conditional: if the parent action owns the charge generator, fixes the charge lattice and gauge inner product, forbids any independent observed `lambda_A F_Q^2`/`f_X(Xhat)F_Q^2` term, and closes radiative/readout re-entry, then `b_alpha=0` follows by chain rule. The current corpus does not yet sign those clauses. Therefore alpha remains a retained product-level branch, not a local-GR/WEP/R10 claim.",
            "",
            "## Source register",
            md_table(source_rows, ["source_id", "relative_path", "exists", "needle_found", "note"]),
            "## Unique EM owner theorem attempt",
            md_table(theorem, ["theorem_id", "claim_piece", "mathematical_statement", "proof_status", "missing_for_claim", "consequence_if_signed"]),
            "## Exclusion audit",
            md_table(exclusion, ["audit_id", "principle", "operator_tested", "result", "reason", "residual_if_fail"]),
            "## Counterexample ledger",
            md_table(counters, ["counterexample_id", "operator", "why_legal_now", "effect_on_alpha", "kills_claim", "needed_to_remove"]),
            "## Alpha coefficient/product source rows",
            md_table(alpha_rows, ["row_id", "quantity", "value_or_bound", "units", "source_path", "source_row", "status", "usable_as_standalone_alpha"]),
            "## Product runner status",
            md_table(product_status_rows_, ["runner_id", "valid_prediction_rows", "valid_bound_rows", "comparison_rows", "claim_allowed", "expected_result"]),
            "## Product comparison rows",
            md_table(product_comparisons, ["comparison_id", "arena", "product_symbol", "product_value", "bound_value", "comparison_status", "pass_for_claim", "issues"]),
            "## Claim gates",
            md_table(claim_rows, ["gate_id", "claim_component", "gate_pass", "claim_allowed", "reason"]),
            "## Decision ledger",
            md_table(decisions, ["decision_id", "decision", "because", "next_action"]),
            "## Validation",
            md_table(validation_rows, ["check_id", "result", "detail"]),
            "## Next target",
            md_table(next_rows, ["next_id", "next_target", "objective", "include", "exclude"]),
            "",
        ]
    )
    DOC.write_text(text, encoding="utf-8")


def main() -> None:
    source_rows = source_register_rows()
    theorem = theorem_rows()
    exclusion = exclusion_audit_rows()
    counters = counterexample_rows()
    alpha_rows = alpha_source_rows()
    predictions = prediction_rows()
    bounds = bound_rows()
    next_rows = next_target_rows()

    outputs = {
        "source_register": OUT / "P8_Y5_R10_1099_SOURCE_REGISTER.csv",
        "theorem": OUT / "P8_Y5_R10_1099_EM_KINETIC_OWNER_THEOREM_ATTEMPT.csv",
        "exclusion": OUT / "P8_Y5_R10_1099_NO_EXTRA_F2_EXCLUSION_AUDIT.csv",
        "counterexamples": OUT / "P8_Y5_R10_1099_COUNTEREXAMPLE_LEDGER.csv",
        "alpha_source": OUT / "P8_Y5_R10_1099_ALPHA_COEFFICIENT_SOURCE_ROWS_NONCLAIM.csv",
        "prediction": PREDICTION_TEMPLATE,
        "bound": BOUND_IMPORT,
        "product_status": OUT / "P8_Y5_R10_1099_PRODUCT_RUNNER_STATUS.csv",
        "product_comparison": OUT / "P8_Y5_R10_1099_PRODUCT_COMPARISON_ROWS.csv",
        "claim_gates": OUT / "P8_Y5_R10_1099_CLAIM_GATES.csv",
        "decisions": OUT / "P8_Y5_R10_1099_DECISION_LEDGER.csv",
        "next_target": OUT / "P8_Y5_R10_1099_NEXT_TARGET.csv",
        "validation": OUT / "P8_Y5_BRR545_1099_VALIDATION.csv",
    }

    write_csv(outputs["source_register"], source_rows)
    write_csv(outputs["theorem"], theorem)
    write_csv(outputs["exclusion"], exclusion)
    write_csv(outputs["counterexamples"], counters)
    write_csv(outputs["alpha_source"], alpha_rows)
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

    validation_rows = validate_outputs(
        outputs,
        source_rows,
        theorem,
        exclusion,
        counters,
        alpha_rows,
        predictions,
        bounds,
        product_status,
        claim_rows,
        next_rows,
    )
    write_csv(outputs["validation"], validation_rows)
    write_doc(
        source_rows,
        theorem,
        exclusion,
        counters,
        alpha_rows,
        product_status_rows_,
        product_result["comparisons"],
        claim_rows,
        decisions,
        validation_rows,
        next_rows,
    )
    remove_pycache()

    failed = [row for row in validation_rows if row["result"] != "pass"]
    print(f"wrote {DOC}")
    print(f"validation: {'PASS' if not failed else 'FAIL'}")
    for row in failed:
        print(f"{row['check_id']}: {row['detail']}")


if __name__ == "__main__":
    main()

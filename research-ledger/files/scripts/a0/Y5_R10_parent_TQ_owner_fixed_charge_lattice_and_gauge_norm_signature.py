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
DOC = ROOT / "1100-Y5-R10-parent-TQ-owner-fixed-charge-lattice-and-gauge-norm-signature.md"
FORMALIZATION = ROOT.parent / "formalization-workbench"
RUN_DIR = ROOT / "runs" / "1100-parent-TQ-owner-gauge-norm-signature" / "results"
PRODUCT_RUN_DIR = RUN_DIR / "product_runner"
PREDICTION_TEMPLATE = OUT / "P8_Y5_R10_1100_ALPHA_PRODUCT_PREDICTION_NONCLAIM.csv"
BOUND_IMPORT = OUT / "P8_Y5_R10_1100_ALPHA_PRODUCT_BOUND_IMPORT.csv"

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
        ("SRC1100_0_1099_next", "source-intake/mts_residuals/P8_Y5_R10_1099_NEXT_TARGET.csv", "NEXT1099_0_1100", "1099 handoff."),
        ("SRC1100_1_1099_theorem", "source-intake/mts_residuals/P8_Y5_R10_1099_EM_KINETIC_OWNER_THEOREM_ATTEMPT.csv", "UEM1099_3_verdict", "no-extra-F2 theorem status."),
        ("SRC1100_2_765_vgn", "source-intake/mts_residuals/P8_Y5_R10_765_VERTICAL_GENERATOR_NORM_THEOREM_ATTEMPT.csv", "VGN765_6_verdict", "vertical-generator norm theorem attempt."),
        ("SRC1100_3_765_mki", "source-intake/mts_residuals/P8_Y5_R10_765_MAXWELL_KINETIC_INHERITANCE_GATE.csv", "MKI765_5_total", "Maxwell kinetic inheritance gate."),
        ("SRC1100_4_765_rescale", "source-intake/mts_residuals/P8_Y5_R10_765_RESCALING_COUNTEREXAMPLE_LEDGER.csv", "RCE765_1_generator_rescale", "generator/current/readout counterexamples."),
        ("SRC1100_5_642_maxwell", "source-intake/mts_residuals/P8_Y5_R10_642_MAXWELL_DESCENT_ATTEMPT.csv", "MD642_4_alpha_constant", "compact U1/Maxwell descent partial result."),
        ("SRC1100_6_642_zero", "source-intake/mts_residuals/P8_Y5_R10_642_THEOREM_ZERO_ATTEMPT.csv", "TA642_4_coupling_normalization", "coupling normalization blocker."),
        ("SRC1100_7_1057_unique", "source-intake/mts_residuals/P8_Y5_R10_1057_UNIQUE_MAXWELL_SUBBLOCK_THEOREM_ATTEMPT.csv", "UMS1057_5_verdict", "unique Maxwell subblock attempt."),
        ("SRC1100_8_1057_counter", "source-intake/mts_residuals/P8_Y5_R10_1057_F2_COUNTERTERM_LEDGER.csv", "CT1057_0_constant_lambda", "independent F2 counterterm ledger."),
        ("SRC1100_9_1058_exhaustion", "source-intake/mts_residuals/P8_Y5_R10_1058_VISIBLE_OPERATOR_DOMAIN_EXHAUSTION_ATTEMPT.csv", "VOE1058_5_verdict", "visible operator-domain exhaustion status."),
        ("SRC1100_10_1055_contract", "source-intake/mts_residuals/P8_Y5_R10_1055_PARENT_ACTION_CONTRACT_CANDIDATE.csv", "PAC1055_1_EM_owner", "parent EM owner contract candidate."),
        ("SRC1100_11_990_contract", "source-intake/mts_residuals/P8_Y5_R10_990_PARENT_ACTION_CONTRACT.csv", "PAC990_3_EM_lock", "minimal parent-action EM-lock clause."),
        ("SRC1100_12_1091_operator", "1091-Y5-R10-parent-operator-domain-no-hidden-visible-hom-theorem-or-MOMS-closure.md", "OBS1091_1_alpha_owner", "operator-domain/no-hidden-visible hom blocker."),
        ("SRC1100_13_clock_bound", "source-intake/mts_residuals/P8_Y5_R10_1052_ALPHA_CLOCK_PRODUCT_BOUND_LEDGER.csv", "ACB1052_2", "clock alpha product bound."),
        ("SRC1100_14_WEP_target", "source-intake/mts_residuals/P8_Y5_R10_1052_ALPHA_WEP_PROJECTION_LEDGER.csv", "AWP1052_0_alpha_Coulomb", "WEP alpha product target."),
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


def signature_rows() -> list[dict[str, str]]:
    return [
        {
            "clause_id": "TQS1100_0_parent_TQ_object",
            "signature_clause": "T_Q is a parent-action object, not a post-readout EM label",
            "mathematical_form": "T_Q in Lie(G_parent) or an integral lattice L_Q with exp(2*pi*T_Q)=1; A_parent = A_Q T_Q + A_perp before observed readout",
            "current_status": "PARTIAL_TEMPLATE_ONLY",
            "evidence": "642 gives compact U1 support; 765 says T_Q is not supplied as a varied parent-action object",
            "if_signed": "observed EM connection has a parent projection rather than appended closure status",
            "if_missing": "A_Q can be appended after the parent action; alpha owner remains unsigned",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "clause_id": "TQS1100_1_fixed_charge_lattice",
            "signature_clause": "charge labels live in a fixed compact representation lattice",
            "mathematical_form": "matter charges n_A are fixed representation/winding data with Lie_v n_A=0 and a nonrescalable base unit Q_*",
            "current_status": "PARTIAL_INTEGER_LABELS_BASE_UNIT_UNSIGNED",
            "evidence": "compact U1 gives integer relative labels, but 642/765 do not derive Q_* or its equality to observed charge",
            "if_signed": "current/source charge labels cannot be hidden Xhat functions",
            "if_missing": "source/test charge normalization can float in WEP/R10 and EM readout",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "clause_id": "TQS1100_2_fixed_generator_norm",
            "signature_clause": "the fibre norm of T_Q is fixed and cannot be rescaled",
            "mathematical_form": "N_Q=<T_Q,T_Q>_P is selected by a parent metric/symplectic/level/lattice form; T_Q -> sT_Q is not an allowed representative transformation",
            "current_status": "NOT_PARENT_SIGNED",
            "evidence": "765 records norm analogies but no parent-fixed EM charge-generator norm",
            "if_signed": "g_EM^{-2}=C_P N_Q can be inherited from parent data",
            "if_missing": "T_Q/A_Q/current rescaling keeps alpha normalization conventional/free",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "clause_id": "TQS1100_3_unique_curvature_norm",
            "signature_clause": "observed F_Q^2 is the only allowed Maxwell kinetic subblock",
            "mathematical_form": "S_parent contains -C_P/4 int <F,F>_P and the Q subblock gives -C_P N_Q/4 int F_Q^2 with no independent lambda_A F_Q^2 or f_X F_Q^2",
            "current_status": "FAIL_CURRENT_CORPUS_COUNTERTERM_LEGAL",
            "evidence": "1057 and 1099 retain lambda_A and f_X F_Q^2 as legal unless operator-domain exhaustion is derived",
            "if_signed": "alpha owner closes at tree level",
            "if_missing": "Z_A=C_P N_Q + lambda_A + f_X + radiative/readout terms",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "clause_id": "TQS1100_4_same_current_owner",
            "signature_clause": "matter current normalization is the Noether current of the same T_Q owner",
            "mathematical_form": "S_int=sum_A n_A int A_Q J_A, with J_Q=delta S_m/delta A_Q and no q_A(Xhat) or c_A current weights",
            "current_status": "NOT_PARENT_SIGNED",
            "evidence": "765 current owner and 990 EM-lock both keep current normalization unsigned",
            "if_signed": "source/test alpha charge does not float independently of Maxwell kinetic owner",
            "if_missing": "WEP/R10 beta_source_alpha and current rescaling remain live",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "clause_id": "TQS1100_5_readout_radiative_guard",
            "signature_clause": "readout and effective action preserve the same parent owner",
            "mathematical_form": "S_vis^eff and alpha readout remain in Alg[q_loc, T_Q, N_Q, theta_rep] with Lie_v(*_obs)=Lie_v ln(hbar*c)=0 or quotient-fixed cancellation",
            "current_status": "UNSIGNED",
            "evidence": "1058 and 1099 retain radiative/readout counterterms",
            "if_signed": "tree-level alpha silence survives clocks/spectra",
            "if_missing": "clock/readout can reintroduce b_alpha",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "clause_id": "TQS1100_6_verdict",
            "signature_clause": "parent T_Q/gauge-norm signature is derived",
            "mathematical_form": "TQS1100_0 through TQS1100_5 all parent-signed",
            "current_status": "TQ_GAUGE_NORM_SIGNATURE_NOT_DERIVED",
            "evidence": "fixed lattice partial support exists, but norm, no-extra-F2, current owner, and readout/radiative guard remain unsigned",
            "if_signed": "b_alpha=0 becomes a promoted theorem instead of a closure",
            "if_missing": "alpha branch stays product-level nonclaim",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
    ]


def theorem_rows() -> list[dict[str, str]]:
    return [
        {
            "theorem_id": "TQT1100_0_exact_conditional",
            "claim_piece": "T_Q signature implies vertical alpha silence",
            "proof_sketch": "If T_Q, N_Q, C_P, the charge lattice, current owner, and readout factors are fixed parent/representation data, then D_v(C_P N_Q)=D_v n_A=D_v readout=0 and Dq[v]=0 gives b_alpha=0.",
            "proof_status": "EXACT_CONDITIONAL_THEOREM",
            "obstruction": "signature clauses are not all parent-signed",
            "result": "useful theorem shape, not a claim",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "theorem_id": "TQT1100_1_compact_U1_limit",
            "claim_piece": "compact U1 fixes only relative integer labels",
            "proof_sketch": "single-valued representations give integer weights n_A, but the base normalization Q_* and kinetic coefficient g_EM are continuous data unless a level/norm owner fixes them.",
            "proof_status": "PARTIAL_SUCCESS_WITH_COUPLING_GAP",
            "obstruction": "Q_* and g_EM are not fixed by compactness alone",
            "result": "charge lattice support, not alpha value",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "theorem_id": "TQT1100_2_rescaling_countermodel",
            "claim_piece": "missing norm owner makes generator normalization conventional",
            "proof_sketch": "When N_Q is not parent-fixed, T_Q -> sT_Q can be compensated by A_Q/current/charge-label normalizations, leaving observed form but not a unique alpha owner.",
            "proof_status": "COUNTERMODEL_RETAINED",
            "obstruction": "nonrescalable parent fibre norm is absent",
            "result": "cannot infer g_EM^{-2}=C_P N_Q as a physical prediction",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "theorem_id": "TQT1100_3_lambda_countermodel",
            "claim_piece": "fixed norm alone is still insufficient without domain exhaustion",
            "proof_sketch": "Even if C_P N_Q exists, S -> S - lambda_A/4 int F_Q^2 gives Z_A=C_P N_Q+lambda_A unless the parent visible-operator domain forbids independent F_Q^2.",
            "proof_status": "COUNTEREXAMPLE_RETAINED",
            "obstruction": "operator-domain exhaustion/no-extra-F2 not derived",
            "result": "b_alpha and finite alpha product branch remain live",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "theorem_id": "TQT1100_4_verdict",
            "claim_piece": "T_Q/gauge-norm route closes alpha owner",
            "proof_sketch": "TQT1100_0 would promote only after fixed T_Q object, fixed norm/level, unique F2 subblock, same current owner, and readout/radiative closure are signed.",
            "proof_status": "NOT_PROMOTED",
            "obstruction": "norm, no-extra-F2, current, and readout clauses remain open",
            "result": "retain alpha products and hunt a level/index/monopole/Ward owner next",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
    ]


def acquisition_rows() -> list[dict[str, str]]:
    specs = [
        ("ACQ1100_0_TQ_object", "T_Q_parent_object", "parent connection projection and charge generator are varied/owned before readout", "MISSING_PARENT_ACTION_OBJECT", "source path or theorem row showing T_Q in parent action"),
        ("ACQ1100_1_compact_lattice", "charge_lattice_LQ", "integral representation lattice plus observed base unit convention", "PARTIAL_INTEGER_LABELS_QSTAR_MISSING", "lattice/period/level source and Q_* normalization"),
        ("ACQ1100_2_norm", "N_Q=<T_Q,T_Q>_P", "fixed nonrescalable norm or level/index value", "MISSING_PARENT_NORM_OR_LEVEL", "parent fibre metric/symplectic form/Kac-Moody-like level/monopole quantization/Ward index"),
        ("ACQ1100_3_Cp", "C_P", "single parent gauge curvature coefficient", "MISSING_PARENT_COEFFICIENT_SOURCE", "source tying C_P to parent action scale rather than observed EM fit"),
        ("ACQ1100_4_no_lambda", "lambda_A_absent", "independent F_Q^2 counterterm forbidden", "MISSING_OPERATOR_DOMAIN_EXHAUSTION", "visible operator-domain theorem or no-hidden-visible coefficient hom"),
        ("ACQ1100_5_current", "J_Q_owner", "same T_Q Noether/Ward owner for current and charge labels", "MISSING_CURRENT_OWNER", "source/current variation contract"),
        ("ACQ1100_6_readout", "alpha_readout_guard", "Hodge/hbar/c/readout quotient-fixed or closed by theorem", "MISSING_RADIOUT_CLOSURE", "effective-action/readout functor closure"),
    ]
    return [
        {
            "input_id": input_id,
            "symbol_or_object": symbol,
            "needed_evidence": evidence,
            "current_status": status,
            "required_source_or_derivation": required,
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        }
        for input_id, symbol, evidence, status, required in specs
    ]


def decomposition_rows() -> list[dict[str, str]]:
    return [
        {
            "decomposition_id": "Z1100_0_parent_piece",
            "term": "C_P N_Q",
            "meaning": "parent curvature-norm contribution to g_EM^{-2}",
            "current_status": "CONDITIONAL_SYMBOLIC_ONLY",
            "vertical_derivative_status": "zero only if C_P and N_Q are parent-fixed",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "decomposition_id": "Z1100_1_constant_counterterm",
            "term": "lambda_A",
            "meaning": "independent visible Maxwell kinetic counterterm",
            "current_status": "LEGAL_UNLESS_OPERATOR_DOMAIN_EXCLUDES",
            "vertical_derivative_status": "constant lambda changes alpha value; hidden-dependent lambda reopens b_alpha",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "decomposition_id": "Z1100_2_hidden_counterterm",
            "term": "f_X(Xhat) or f(I_hid)",
            "meaning": "hidden scalar coefficient multiplying F_Q^2",
            "current_status": "LEGAL_IF_HIDDEN_INVARIANT_SURVIVES",
            "vertical_derivative_status": "direct b_alpha source",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "decomposition_id": "Z1100_3_radiative_readout",
            "term": "delta_lambda_rad + readout terms",
            "meaning": "loop/threshold/readout regeneration of alpha coefficient",
            "current_status": "RETAINED_UNTIL_CLOSURE",
            "vertical_derivative_status": "can reintroduce clock/spectroscopy alpha pressure",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "decomposition_id": "Z1100_4_total",
            "term": "Z_A = C_P N_Q + lambda_A + f_X + delta_lambda_rad + readout",
            "meaning": "honest current alpha normalization ledger",
            "current_status": "FINITE_BRANCH_RETAINED",
            "vertical_derivative_status": "b_alpha not theorem-zero unless all nonparent terms vanish and parent piece fixed",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
    ]


def prediction_rows() -> list[dict[str, str]]:
    return [
        {
            "prediction_id": "PRED1100_0_missing_TQ_signature_or_balpha",
            "arena": "clock",
            "product_symbol": "P_clock_alpha",
            "product_value": "MISSING_TQ_SIGNATURE_OR_B_ALPHA_TAU_CLOCK",
            "product_units": "yr^-1",
            "product_source": "source-intake/mts_residuals/P8_Y5_R10_1100_TQ_GAUGE_NORM_SIGNATURE.csv",
            "inputs_present": "clock bound only; T_Q signature not derived",
            "required_inputs": "signed TQ/gauge-norm theorem or numeric b_alpha*tau_clock prediction",
            "derivation_status": "MISSING_MTS_PRODUCT_PREDICTION",
            "valid_for_claim": "false",
            "notes": "no standalone b_alpha from clock product",
        },
        {
            "prediction_id": "PRED1100_1_missing_WEP_alpha_projection",
            "arena": "MICROSCOPE_WEP",
            "product_symbol": "P_WEP_alpha",
            "product_value": "MISSING_TQ_SIGNATURE_OR_BETA_SOURCE_ALPHA_B_ALPHA_TAU_WEP",
            "product_units": "dimensionless",
            "product_source": "source-intake/mts_residuals/P8_Y5_R10_1100_TQ_GAUGE_NORM_SIGNATURE.csv",
            "inputs_present": "WEP target only; source/test alpha projection missing",
            "required_inputs": "signed TQ/current/source owner or beta_source_alpha;b_alpha;tau_WEP",
            "derivation_status": "MISSING_WEP_ALPHA_PRODUCT_PROJECTION",
            "valid_for_claim": "false",
            "notes": "no clock-to-WEP transfer",
        },
        {
            "prediction_id": "PRED1100_2_missing_c_alpha_DD",
            "arena": "MICROSCOPE_WEP",
            "product_symbol": "c_alpha_DD",
            "product_value": "MISSING_SOURCE_BACKED_C_ALPHA_OR_TQ_THEOREM_ZERO",
            "product_units": "dimensionless",
            "product_source": "source-intake/mts_residuals/P8_Y5_R10_1100_TQ_THEOREM_ATTEMPT.csv",
            "inputs_present": "DD threshold only",
            "required_inputs": "signed TQ/no-extra-F2 theorem or external c_alpha_DD source row",
            "derivation_status": "MISSING_SCOREABLE_ALPHA_COEFFICIENT",
            "valid_for_claim": "false",
            "notes": "threshold is not an MTS prediction",
        },
    ]


def bound_rows() -> list[dict[str, str]]:
    return [
        {
            "bound_id": "BOUND1100_0_clock_product",
            "arena": "clock",
            "product_symbol": "P_clock_alpha",
            "bound_value": f"{CLOCK_PRODUCT_BOUND_YR_INV:.16e}",
            "bound_units": "yr^-1",
            "bound_source": "source-intake/mts_residuals/P8_Y5_R10_1052_ALPHA_CLOCK_PRODUCT_BOUND_LEDGER.csv",
            "source_row": "ACB1052_2",
            "bound_type": "upper_abs_1sigma_product_bound",
            "valid_for_claim": "false",
            "notes": "source-backed product bound only",
        },
        {
            "bound_id": "BOUND1100_1_WEP_alpha_product",
            "arena": "MICROSCOPE_WEP",
            "product_symbol": "P_WEP_alpha",
            "bound_value": f"{WEP_ALPHA_PRODUCT_MAX:.16e}",
            "bound_units": "dimensionless",
            "bound_source": "source-intake/mts_residuals/P8_Y5_R10_1052_ALPHA_WEP_PROJECTION_LEDGER.csv",
            "source_row": "AWP1052_0_alpha_Coulomb",
            "bound_type": "required_abs_product_max_smoke_convention",
            "valid_for_claim": "false",
            "notes": "projection target only",
        },
        {
            "bound_id": "BOUND1100_2_c_alpha_DD_threshold",
            "arena": "MICROSCOPE_WEP",
            "product_symbol": "c_alpha_DD",
            "bound_value": f"{DD_ALPHA_COEFF_MAX:.16e}",
            "bound_units": "dimensionless",
            "bound_source": "source-intake/mts_residuals/P8_Y5_R10_1098_SOURCE_BACKED_COEFFICIENT_REQUIREMENTS.csv",
            "source_row": "REQ1098_0_c_alpha",
            "bound_type": "absolute_constant_coefficient_threshold_nonclaim",
            "valid_for_claim": "false",
            "notes": "threshold only; no MTS c_alpha prediction",
        },
    ]


def product_status_rows(product_status: dict[str, Any]) -> list[dict[str, str]]:
    return [
        {
            "runner_id": "APR1100_0_TQ_signature_stub",
            "prediction_rows": str(product_status.get("prediction_rows", "")),
            "bound_rows": str(product_status.get("bound_rows", "")),
            "valid_prediction_rows": str(product_status.get("valid_prediction_rows", "")),
            "valid_bound_rows": str(product_status.get("valid_bound_rows", "")),
            "comparison_rows": str(product_status.get("comparison_rows", "")),
            "claim_allowed": str(product_status.get("claim_allowed", "")).lower(),
            "expected_result": "reject missing TQ signature and missing finite alpha products",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        }
    ]


def claim_gate_rows(product_status: dict[str, Any]) -> list[dict[str, str]]:
    return [
        {
            "gate_id": "CG1100_0_TQ_signature",
            "claim_component": "parent T_Q/gauge-norm signature is derived",
            "gate_pass": "false",
            "claim_allowed": "false",
            "reason": "TQS1100_6_verdict=TQ_GAUGE_NORM_SIGNATURE_NOT_DERIVED",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "gate_id": "CG1100_1_balpha_zero",
            "claim_component": "b_alpha=0 follows",
            "gate_pass": "false",
            "claim_allowed": "false",
            "reason": "fixed norm, no-extra-F2, current owner, and readout/radiative closure are not all signed",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "gate_id": "CG1100_2_finite_products",
            "claim_component": "finite alpha product predictions are score-ready",
            "gate_pass": "false",
            "claim_allowed": "false",
            "reason": "prediction rows contain missing TQ theorem or missing tau/source product inputs",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "gate_id": "CG1100_3_runner",
            "claim_component": "product runner has claim-valid predictions",
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
            "decision_id": "DEC1100_0_partial_win",
            "decision": "compact U1 and integer charge labels remain useful partial support",
            "because": "they organize relative charges and Bianchi/Maxwell form, but do not fix Q_* or g_EM",
            "next_action": "do not discard the route; sharpen the missing owner",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "decision_id": "DEC1100_1_signature_result",
            "decision": "parent T_Q/gauge-norm signature is not derived",
            "because": "fixed nonrescalable norm, unique F2 subblock, current owner, and readout/radiative guard are unsigned",
            "next_action": "retain alpha as finite product-level branch",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "decision_id": "DEC1100_2_best_theory_next",
            "decision": "hunt a level/index/monopole/Ward owner for the gauge norm",
            "because": "only a real parent quantization/norm mechanism can turn C_P N_Q from notation into a physical alpha owner",
            "next_action": "1101-Y5-R10-gauge-fibre-level-index-monopole-Ward-owner-or-alpha-product-route.md",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
    ]


def next_target_rows() -> list[dict[str, str]]:
    return [
        {
            "next_id": "NEXT1100_0_1101",
            "next_target": "1101-Y5-R10-gauge-fibre-level-index-monopole-Ward-owner-or-alpha-product-route.md",
            "objective": "try to derive a real parent owner for the EM gauge norm from a level, index, monopole/Dirac quantization, anomaly/Ward identity, or fixed fibre metric; if no owner exists, keep alpha on the finite product route",
            "include": "level/index candidates; fixed fibre metric; charge quantization versus coupling quantization; Ward current normalization; no-extra-F2 guard; product fallback rows",
            "exclude": "compact U1 alone as alpha proof; unit rescaling; invented alpha value; standalone b_alpha from clock products; WEP/R10 transfer without tau/source maps; local-GR claim; GitHub; formalization edits",
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
    signature: list[dict[str, str]],
    theorem: list[dict[str, str]],
    acquisition: list[dict[str, str]],
    decomposition: list[dict[str, str]],
    predictions: list[dict[str, str]],
    bounds: list[dict[str, str]],
    product_status: dict[str, Any],
    claim_rows: list[dict[str, str]],
    next_rows: list[dict[str, str]],
) -> list[dict[str, str]]:
    checks: list[tuple[str, bool, str]] = []
    checks.append(("V1100_0_sources_exist", all(flag(row["exists"]) and flag(row["needle_found"]) for row in sources), "all cited local source paths exist and needles are found"))
    checks.append(("V1100_1_signature_not_derived", any(row["clause_id"] == "TQS1100_6_verdict" and row["current_status"] == "TQ_GAUGE_NORM_SIGNATURE_NOT_DERIVED" for row in signature), "TQ/gauge-norm signature verdict is explicit"))
    checks.append(("V1100_2_partial_U1_recorded", any(row["theorem_id"] == "TQT1100_1_compact_U1_limit" and row["proof_status"] == "PARTIAL_SUCCESS_WITH_COUPLING_GAP" for row in theorem), "compact U1 partial support and coupling gap are recorded"))
    checks.append(("V1100_3_countermodels_retained", all(any(row["theorem_id"] == theorem_id for row in theorem) for theorem_id in ["TQT1100_2_rescaling_countermodel", "TQT1100_3_lambda_countermodel"]), "generator rescaling and lambda countermodels are retained"))
    checks.append(("V1100_4_acquisition_nonclaim", acquisition and all(row["claim_allowed"] == "false" and row["valid_for_claim"] == "false" for row in acquisition), "acquisition ledger is nonclaim"))
    checks.append(("V1100_5_ZA_decomposition_retained", any(row["decomposition_id"] == "Z1100_4_total" and row["current_status"] == "FINITE_BRANCH_RETAINED" for row in decomposition), "honest Z_A decomposition retains finite branch"))
    checks.append(("V1100_6_predictions_missing", predictions and all(row["valid_for_claim"] == "false" and str(row["product_value"]).startswith("MISSING") for row in predictions), "prediction rows remain missing/nonclaim"))
    checks.append(("V1100_7_bounds_positive", len(bounds) == 3 and all(parse_float(row["bound_value"]) is not None and float(row["bound_value"]) > 0 for row in bounds), "bound rows have positive numeric values"))
    checks.append(("V1100_8_runner_refuses", product_status.get("valid_prediction_rows") == 0 and product_status.get("claim_allowed") is False, "product runner refuses missing alpha predictions"))
    checks.append(("V1100_9_claim_gates_blocked", claim_rows and all(row["claim_allowed"] == "false" for row in claim_rows), "all TQ/alpha claim gates remain blocked"))
    checks.append(("V1100_10_next_target", any(row["next_target"].startswith("1101-Y5-R10-gauge-fibre") for row in next_rows), "1101 handoff written"))
    generated_paths = list(outputs.values()) + [DOC]
    checks.append(("V1100_11_generated_under_post_checkpoint", all(str(path.resolve()).startswith(str(ROOT.resolve())) for path in generated_paths), "all generated outputs are under post-checkpoint-work"))
    checks.append(("V1100_12_csv_parse", csv_outputs_parse([path for key, path in outputs.items() if key != "validation"]), "all 1100 CSV outputs parse cleanly"))
    checks.append(("V1100_13_formalization_untouched", count_formalization_modified_since_start() == 0, "formalization-workbench modified-file count remains zero"))
    checks.append(("V1100_SUMMARY", True, "TQ/gauge-norm signature not derived; compact U1 partial support retained; alpha finite product branch remains nonclaim; next target level/index/monopole/Ward owner hunt"))
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
    signature: list[dict[str, str]],
    theorem: list[dict[str, str]],
    acquisition: list[dict[str, str]],
    decomposition: list[dict[str, str]],
    product_status_rows_: list[dict[str, str]],
    product_comparisons: list[dict[str, Any]],
    claim_rows: list[dict[str, str]],
    decisions: list[dict[str, str]],
    validation: list[dict[str, str]],
    next_rows: list[dict[str, str]],
) -> None:
    text = "\n".join(
        [
            "# 1100-Y5-R10 parent T_Q owner, fixed charge lattice, and gauge-norm signature",
            "",
            "## Current verdict",
            "1100 keeps the useful partial result and names the exact failure. Compact `U(1)` can organize integer charge labels and Maxwell form, but it does not by itself fix the continuous EM coupling. To derive `b_alpha=0`, MTS still needs a parent-owned `T_Q`, a nonrescalable charge lattice/base unit, a fixed gauge-fibre norm or level, no independent `lambda_A F_Q^2`/`f_X F_Q^2`, the same current owner, and radiative/readout closure. Those clauses are not all signed, so alpha remains a finite product-level nonclaim branch.",
            "",
            "## Source register",
            md_table(sources, ["source_id", "relative_path", "exists", "needle_found", "note"]),
            "## T_Q/gauge-norm signature",
            md_table(signature, ["clause_id", "signature_clause", "mathematical_form", "current_status", "evidence", "if_signed", "if_missing"]),
            "## Theorem attempt",
            md_table(theorem, ["theorem_id", "claim_piece", "proof_sketch", "proof_status", "obstruction", "result"]),
            "## Required source/acquisition ledger",
            md_table(acquisition, ["input_id", "symbol_or_object", "needed_evidence", "current_status", "required_source_or_derivation"]),
            "## Alpha normalization decomposition",
            md_table(decomposition, ["decomposition_id", "term", "meaning", "current_status", "vertical_derivative_status"]),
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
    signature = signature_rows()
    theorem = theorem_rows()
    acquisition = acquisition_rows()
    decomposition = decomposition_rows()
    predictions = prediction_rows()
    bounds = bound_rows()
    next_rows = next_target_rows()

    outputs = {
        "source_register": OUT / "P8_Y5_R10_1100_SOURCE_REGISTER.csv",
        "signature": OUT / "P8_Y5_R10_1100_TQ_GAUGE_NORM_SIGNATURE.csv",
        "theorem": OUT / "P8_Y5_R10_1100_TQ_THEOREM_ATTEMPT.csv",
        "acquisition": OUT / "P8_Y5_R10_1100_TQ_REQUIRED_SOURCE_ACQUISITION_LEDGER.csv",
        "decomposition": OUT / "P8_Y5_R10_1100_ALPHA_NORMALIZATION_DECOMPOSITION.csv",
        "prediction": PREDICTION_TEMPLATE,
        "bound": BOUND_IMPORT,
        "product_status": OUT / "P8_Y5_R10_1100_PRODUCT_RUNNER_STATUS.csv",
        "product_comparison": OUT / "P8_Y5_R10_1100_PRODUCT_COMPARISON_ROWS.csv",
        "claim_gates": OUT / "P8_Y5_R10_1100_CLAIM_GATES.csv",
        "decisions": OUT / "P8_Y5_R10_1100_DECISION_LEDGER.csv",
        "next_target": OUT / "P8_Y5_R10_1100_NEXT_TARGET.csv",
        "validation": OUT / "P8_Y5_BRR545_1100_VALIDATION.csv",
    }

    write_csv(outputs["source_register"], sources)
    write_csv(outputs["signature"], signature)
    write_csv(outputs["theorem"], theorem)
    write_csv(outputs["acquisition"], acquisition)
    write_csv(outputs["decomposition"], decomposition)
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
        signature,
        theorem,
        acquisition,
        decomposition,
        predictions,
        bounds,
        product_status,
        claim_rows,
        next_rows,
    )
    write_csv(outputs["validation"], validation)
    write_doc(
        sources,
        signature,
        theorem,
        acquisition,
        decomposition,
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

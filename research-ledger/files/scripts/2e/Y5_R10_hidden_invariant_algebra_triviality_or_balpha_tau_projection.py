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
DOC = ROOT / "1092-Y5-R10-hidden-invariant-algebra-triviality-or-balpha-tau-projection.md"
FORMALIZATION = ROOT.parent / "formalization-workbench"
RUN_DIR = ROOT / "runs" / "1092-hidden-invariant-algebra-triviality" / "results"
PRODUCT_RUN_DIR = RUN_DIR / "product_runner"
PREDICTION_TEMPLATE = OUT / "P8_Y5_R10_1092_WEP_PRODUCT_CANDIDATE_NONCLAIM.csv"
BOUND_IMPORT = OUT / "P8_Y5_R10_1092_WEP_BOUND_IMPORT.csv"
ETA_BOUND = 2.8e-15
BEST_CLOCK_PRODUCT_BOUND = 2.1e-18
REQUIRED_BETA_SOURCE_ALPHA_MAX = 4.797780522732e-05


def stamp() -> str:
    return datetime.now(timezone.utc).isoformat()


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


def parse_float(value: object) -> float | None:
    try:
        parsed = float(str(value).strip())
    except (TypeError, ValueError):
        return None
    if not math.isfinite(parsed):
        return None
    return parsed


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
    return sum(
        1
        for path in FORMALIZATION.rglob("*")
        if path.is_file() and datetime.fromtimestamp(path.stat().st_mtime, timezone.utc) >= STARTED
    )


def remove_pycache() -> None:
    pycache = Path(__file__).resolve().parent / "__pycache__"
    if pycache.exists():
        shutil.rmtree(pycache)


def source_register_rows() -> list[dict[str, str]]:
    specs = [
        ("SRC1092_0_1091_next", "source-intake/mts_residuals/P8_Y5_R10_1091_NEXT_TARGET.csv", "NEXT1091_0_1092", "1091 handoff to hidden-invariant algebra or b_alpha tau projection."),
        ("SRC1092_1_1091_theorem", "source-intake/mts_residuals/P8_Y5_R10_1091_OPERATOR_DOMAIN_THEOREM_ATTEMPT.csv", "ODH1091_6_verdict", "operator-domain theorem failure and scalar obstruction."),
        ("SRC1092_2_414_triviality", "414-local-quotient-invariant-algebra-triviality-gate.md", "local_invariant_algebra_triviality_derived", "local invariant algebra triviality gate."),
        ("SRC1092_3_573_chain", "source-intake/mts_residuals/P8_Y5_R10_573_NO_MARKER_REDUCTION_CHAIN.csv", "RC573_1_invariant_algebra", "no-marker reduction chain."),
        ("SRC1092_4_573_debt", "source-intake/mts_residuals/P8_Y5_R10_573_INVARIANT_GENERATOR_DEBT.csv", "IG573_3_memory_scalar", "surviving invariant-generator debt."),
        ("SRC1092_5_965_audit", "source-intake/mts_residuals/P8_Y5_R10_965_LOCAL_INVARIANT_ALGEBRA_AUDIT.csv", "ALG965_9_verdict", "latest local invariant algebra audit."),
        ("SRC1092_6_980_functor", "980-Y5-R10-no-marker-sector-functor-theorem-or-first-qbar-source-acquisition.md", "NMF980_2_scalar_obstruction_lemma", "scalar obstruction to no-marker functor."),
        ("SRC1092_7_1052_clock", "1052-Y5-R10-tau-clock-Xhat-normalization-or-alpha-WEP-R10-projection-source.md", "TCN1052_4_verdict", "tau_clock/Xhat normalization failure."),
        ("SRC1092_8_1052_clock_bound", "source-intake/mts_residuals/P8_Y5_R10_1052_ALPHA_CLOCK_PRODUCT_BOUND_LEDGER.csv", "ACB1052_2", "best source-backed b_alpha tau clock product row."),
        ("SRC1092_9_1052_WEP", "source-intake/mts_residuals/P8_Y5_R10_1052_ALPHA_WEP_PROJECTION_LEDGER.csv", "AWP1052_0_alpha_Coulomb", "alpha WEP projection pressure row."),
        ("SRC1092_10_1052_R10", "source-intake/mts_residuals/P8_Y5_R10_1052_ALPHA_R10_PROJECTION_LEDGER.csv", "RAP1052_0_product_law", "R10 alpha product-law projection row."),
        ("SRC1092_11_local_bounds", "source-intake/local_bounds/local_bound_claims.csv", "R1_WEP_source_charge", "MICROSCOPE WEP source-charge bound anchor."),
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


def hidden_invariant_attempt_rows() -> list[dict[str, str]]:
    return [
        {
            "attempt_id": "HIT1092_0_target",
            "claim_piece": "hidden invariant algebra triviality",
            "mathematical_statement": "O(C_hid)^inv = R on the local/MOMS branch",
            "status": "TARGET_SHARP",
            "proof_or_obstruction": "would remove local scalar labels that feed visible coefficients",
            "claim_effect": "would support no-hidden-visible-hom and ordinary matter constants",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "attempt_id": "HIT1092_1_sufficiency",
            "claim_piece": "triviality implies constant visible coefficients",
            "mathematical_statement": "if O(C_hid)^inv=R, then any invariant coefficient c:C_hid->R is constant",
            "status": "EXACT_CONDITIONAL_THEOREM",
            "proof_or_obstruction": "invariant coefficient maps factor through the invariant algebra",
            "claim_effect": "would kill b_alpha(I), b_mA(I), clock(I), and source-weight(I) at this level",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "attempt_id": "HIT1092_2_current_corpus",
            "claim_piece": "current source audit eliminates all hidden invariant generators",
            "mathematical_statement": "finite_cell_spectrum, domain class, chi_D, memory scalar, species constants, readout, and time-arrow are constants/gauge",
            "status": "FAIL_CURRENT_CORPUS",
            "proof_or_obstruction": "414, 573, and 965 all retain generator debts",
            "claim_effect": "triviality cannot be promoted from the present corpus",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "attempt_id": "HIT1092_3_scalar_counterexample",
            "claim_piece": "surviving scalar obstruction",
            "mathematical_statement": "if I in O(C_hid)^inv and dI != 0, then b_alpha(I)=b0+epsilon I is a legal nonconstant coefficient map",
            "status": "COUNTEREXAMPLE_PROVED",
            "proof_or_obstruction": "diffeomorphism/gauge symmetry alone does not forbid f(I)F^2 or m_A(I)psi_bar psi",
            "claim_effect": "hidden-invariant triviality is false unless I is removed, no-haired, or bounded",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "attempt_id": "HIT1092_4_quotient_shift_nohair",
            "claim_piece": "quotient/shift/nohair closure",
            "mathematical_statement": "Dq[v_X]=0 plus exact shift or positive nohair forces I=constant and grad I=0 locally",
            "status": "CONDITIONAL_ONLY",
            "proof_or_obstruction": "needs parent-owned operator, sign, source-free equation, boundary flux zero, and self-adjoint domain",
            "claim_effect": "route remains promising but unsigned",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "attempt_id": "HIT1092_5_verdict",
            "claim_piece": "derive O(C_hid)^inv=R now",
            "mathematical_statement": "all local hidden invariant generators are trivial on the physical local branch",
            "status": "TRIVIALITY_NOT_DERIVED",
            "proof_or_obstruction": "multiple generator debts survive and scalar counterexample remains legal",
            "claim_effect": "do not promote local-GR/WEP/R10 safety; continue finite residual route or prove scalar nohair inputs",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
    ]


def surviving_generator_rows() -> list[dict[str, str]]:
    specs = [
        ("GEN1092_0_finite_cell_spectrum", "finite_cell_fibre_spectrum", "not_trivialized", "can act as mass gap, scalar charge, or fifth-force scale", "integrate out universally or prove pure basis/gauge relabeling"),
        ("GEN1092_1_relative_domain_class", "relative_boundary_domain_class", "not_derived", "can select local branch or domain-dependent coupling", "derive physical local trivial class or fixed-class stress-free nohair"),
        ("GEN1092_2_domain_selector", "domain_selector_chi_D", "not_derived", "can become active projector/source switch", "derive selector theorem separating local vacuum from cosmology"),
        ("GEN1092_3_memory_scalar", "memory_or_class_scalar", "not_silenced_as_theorem", "can drive clock drift, gamma shift, or fifth-force channel", "prove local value and gradient silence or retain bounded residual"),
        ("GEN1092_4_orientation_time_arrow", "orientation_time_arrow", "not_classified", "can create preferred-frame or time-asymmetry residual", "show contained in observed coframe, constant, or pure gauge"),
        ("GEN1092_5_species_constants", "species_charge_constants", "not_universalized", "can create WEP/source-charge/clock nonuniversality", "derive constant-sector universality theorem"),
        ("GEN1092_6_readout_projector", "readout_projector", "no_cheat_rule_only", "can re-enter as reduced action term if varied too early", "prove readout-after-variation theorem"),
    ]
    return [
        {
            "generator_id": generator_id,
            "generator": generator,
            "current_status": current_status,
            "blocks_triviality": "true",
            "risk": risk,
            "required_elimination": required_elimination,
            "source_basis": "414;573;965",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        }
        for generator_id, generator, current_status, risk, required_elimination in specs
    ]


def scalar_nohair_rows() -> list[dict[str, str]]:
    return [
        {
            "audit_id": "SNH1092_0_operator_owner",
            "input_needed": "parent-owned scalar/operator variable Xhat or I",
            "mathematical_need": "the same parent field must control the dangerous visible coefficient and obey the nohair equation",
            "status": "MISSING_PARENT_OWNER",
            "effect": "cannot apply nohair to an arbitrary closure coordinate",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "audit_id": "SNH1092_1_positive_operator",
            "input_needed": "Z_X>0 and M_X^2>=0 with self-adjoint local domain",
            "mathematical_need": "integral identity int(Z_X|grad X|^2+M_X^2 X^2)=boundary+source",
            "status": "MISSING_SIGNED_OPERATOR",
            "effect": "positive identity cannot be used as a theorem",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "audit_id": "SNH1092_2_source_silence",
            "input_needed": "J_X=0 for ordinary local matter/readout",
            "mathematical_need": "source-free local equation rather than a forced finite residual",
            "status": "MISSING_SOURCE_SILENCE",
            "effect": "ordinary matter can still excite the scalar channel",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "audit_id": "SNH1092_3_boundary_flux",
            "input_needed": "boundary/local projection flux vanishes or is bounded",
            "mathematical_need": "boundary term must not carry the hidden invariant into the lab region",
            "status": "MISSING_BOUNDARY_CONDITION",
            "effect": "closed/gapped local plateau remains conditional",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "audit_id": "SNH1092_4_verdict",
            "input_needed": "complete scalar nohair input pack",
            "mathematical_need": "parent owner + positive operator + J_X=0 + zero flux + local projection",
            "status": "NOHAIR_ROUTE_UNSIGNED",
            "effect": "do not assert O(C_hid)^inv=R; use nonclaim b_alpha*tau fallback",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
    ]


def balpha_tau_rows() -> list[dict[str, str]]:
    return [
        {
            "fallback_id": "BTP1092_0_best_clock_product",
            "product": "b_alpha*tau_clock_time",
            "best_bound": f"|b_alpha*tau_clock_time| <= {BEST_CLOCK_PRODUCT_BOUND:.12e} yr^-1",
            "source_basis": "1051/1052 Yb E3/E2 clock row",
            "usable_now": "source-backed nonclaim product bound",
            "missing_for_claim": "tau_clock_time parent derivation and standalone b_alpha",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "fallback_id": "BTP1092_1_no_standalone",
            "product": "b_alpha",
            "best_bound": "not available",
            "source_basis": "TCN1052_4_verdict",
            "usable_now": "none as standalone",
            "missing_for_claim": "Xhat/chi_X normalization and tau_clock_time",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "fallback_id": "BTP1092_2_WEP_pressure",
            "product": "beta_source_alpha or equivalent WEP alpha source coefficient",
            "best_bound": f"|beta_source_alpha| <= {REQUIRED_BETA_SOURCE_ALPHA_MAX:.12e} required by 1052 alpha/Coulomb stress row",
            "source_basis": "AWP1052_0_alpha_Coulomb",
            "usable_now": "target threshold only",
            "missing_for_claim": "beta_source_alpha theorem/prior, tau_WEP, and material charge model",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "fallback_id": "BTP1092_3_R10_pressure",
            "product": "beta_s beta_t K_X/Z_X tau_R10",
            "best_bound": "not scoreable",
            "source_basis": "RAP1052_0_product_law",
            "usable_now": "schema and refusal test only",
            "missing_for_claim": "lambda_X, K_X(lambda), Z_X, beta_s, beta_t, tau_R10, promoted R10 bound curve",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "fallback_id": "BTP1092_4_verdict",
            "product": "finite residual branch",
            "best_bound": "clock product retained; WEP/R10 transfers blocked",
            "source_basis": "1052 transfer gates plus 1092 hidden-triviality failure",
            "usable_now": "private discipline ledger",
            "missing_for_claim": "scalar nohair input pack or sourced projection products",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
    ]


def transfer_gate_rows() -> list[dict[str, str]]:
    return [
        {
            "gate_id": "TRG1092_0_clock_product",
            "arena": "clock",
            "transfer_claim": "clock product bound is usable",
            "gate_status": "true_nonclaim_only",
            "reason": "source-backed product bound exists but is not standalone b_alpha",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "gate_id": "TRG1092_1_standalone_balpha",
            "arena": "clock_to_theory",
            "transfer_claim": "derive standalone b_alpha",
            "gate_status": "false",
            "reason": "tau_clock_time and Xhat/chi_X normalization are not parent-derived",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "gate_id": "TRG1092_2_clock_to_WEP",
            "arena": "MICROSCOPE_WEP",
            "transfer_claim": "clock product transfers to WEP alpha source charge",
            "gate_status": "false",
            "reason": "requires beta_source_alpha, tau_WEP, composition charges, and shared domain rule",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "gate_id": "TRG1092_3_clock_to_R10",
            "arena": "R10_short_range",
            "transfer_claim": "clock product transfers to alpha(lambda)",
            "gate_status": "false",
            "reason": "requires beta_s beta_t K_X/Z_X tau_R10, lambda_X, and promoted bound curve",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "gate_id": "TRG1092_4_local_GR",
            "arena": "local_GR_PPN_R10_WEP",
            "transfer_claim": "hidden-invariant triviality gives local-GR safety",
            "gate_status": "false",
            "reason": "O(C_hid)^inv=R and scalar nohair inputs are not derived",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
    ]


def prediction_rows() -> list[dict[str, str]]:
    return [
        {
            "prediction_id": "PRED1092_0_WEP_alpha_projection_missing",
            "arena": "MICROSCOPE_WEP",
            "product_symbol": "P_WEP_alpha",
            "product_value": "MISSING_BETA_SOURCE_ALPHA_TAU_WEP_AND_MATERIAL_CHARGES",
            "product_units": "dimensionless",
            "product_source": "source-intake/mts_residuals/P8_Y5_R10_1092_BALPHA_TAU_PROJECTION_FALLBACK.csv",
            "inputs_present": "clock product bound only",
            "required_inputs": "beta_source_alpha;tau_WEP;composition charge matrix;shared domain rule OR theorem-zero",
            "derivation_status": "MISSING_WEP_PROJECTION_INPUTS",
            "valid_for_claim": "false",
            "notes": "generic product runner must refuse; this is not a WEP prediction",
        }
    ]


def bound_import_rows() -> list[dict[str, str]]:
    return [
        {
            "bound_id": "BOUND1092_0_MICROSCOPE_WEP",
            "arena": "MICROSCOPE_WEP",
            "product_symbol": "P_WEP_alpha",
            "bound_value": f"{ETA_BOUND:.16e}",
            "bound_units": "dimensionless",
            "bound_source": "source-intake/local_bounds/local_bound_claims.csv",
            "source_row": "R1_WEP_source_charge",
            "bound_type": "absolute_eta_upper_bound",
            "valid_for_claim": "true",
            "notes": "source-backed comparator bound; MTS prediction row remains invalid",
        }
    ]


def product_status_rows(product_status: dict[str, Any]) -> list[dict[str, str]]:
    return [
        {
            "runner_id": "APR1092_0_WEP_projection_stub",
            "prediction_rows": str(product_status.get("prediction_rows", "")),
            "bound_rows": str(product_status.get("bound_rows", "")),
            "valid_prediction_rows": str(product_status.get("valid_prediction_rows", "")),
            "valid_bound_rows": str(product_status.get("valid_bound_rows", "")),
            "comparison_rows": str(product_status.get("comparison_rows", "")),
            "claim_allowed": str(product_status.get("claim_allowed", "")).lower(),
            "expected_result": "reject missing WEP projection product and keep claim false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        }
    ]


def claim_gate_rows(product_status: dict[str, Any]) -> list[dict[str, str]]:
    return [
        {
            "gate_id": "CG1092_0_hidden_triviality",
            "claim_component": "O(C_hid)^inv=R local branch",
            "gate_pass": "false",
            "claim_allowed": "false",
            "reason": "HIT1092_5_verdict=TRIVIALITY_NOT_DERIVED",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "gate_id": "CG1092_1_scalar_nohair",
            "claim_component": "positive/source-free scalar nohair identity",
            "gate_pass": "false",
            "claim_allowed": "false",
            "reason": "parent owner, signs, source silence, boundary flux, and domain are unsigned",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "gate_id": "CG1092_2_clock_product",
            "claim_component": "standalone b_alpha from clock product",
            "gate_pass": "false",
            "claim_allowed": "false",
            "reason": "clock product is bounded but tau_clock_time is not parent-derived",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "gate_id": "CG1092_3_WEP_R10_transfer",
            "claim_component": "clock product transfer to WEP/R10",
            "gate_pass": "false",
            "claim_allowed": "false",
            "reason": "projection factors and source/test products are missing",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "gate_id": "CG1092_4_product_runner",
            "claim_component": "WEP product runner",
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
            "decision_id": "DEC1092_0_triviality_result",
            "decision": "hidden invariant algebra triviality is not derived",
            "because": "current generator debts survive and any nonconstant invariant scalar creates the forbidden coefficient map",
            "next_action": "try to assign a parent owner and nohair input pack to the scalar channel",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "decision_id": "DEC1092_1_fallback_result",
            "decision": "retain the b_alpha*tau_clock product as a nonclaim constraint",
            "because": "clock evidence is real but only constrains the product, not b_alpha or WEP/R10 transfer",
            "next_action": "source or derive tau_clock/tau_WEP/tau_R10 and beta_source_alpha consistently",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "decision_id": "DEC1092_2_best_next",
            "decision": "derive-first route should attack scalar nohair input ownership before fitting priors",
            "because": "if parent owner, signs, J_X=0, and boundary silence close, the clean local-GR route reopens",
            "next_action": "1093-Y5-R10-scalar-nohair-input-owner-or-balpha-tau-projection-source.md",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
    ]


def next_target_rows() -> list[dict[str, str]]:
    return [
        {
            "next_id": "NEXT1092_0_1093",
            "next_target": "1093-Y5-R10-scalar-nohair-input-owner-or-balpha-tau-projection-source.md",
            "objective": "try to parent-own the dangerous scalar and derive the positive/source-free local nohair input pack; if that fails, source the finite b_alpha/tau_WEP/tau_R10 projection products",
            "include": "parent Xhat/I owner; Z_X and M_X^2 sign; J_X=0 source silence; zero/bounded boundary flux; self-adjoint local domain; b_alpha tau fallback rows",
            "exclude": "assuming hidden invariant algebra triviality; clock-to-WEP/R10 transfer without projection; pair cancellations; local-GR/WEP/R10 claim; GitHub; formalization edits",
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
    hidden_rows: list[dict[str, str]],
    generator_rows: list[dict[str, str]],
    nohair_rows: list[dict[str, str]],
    fallback_rows: list[dict[str, str]],
    transfer_rows: list[dict[str, str]],
    prediction_rows_: list[dict[str, str]],
    bound_rows_: list[dict[str, str]],
    product_status: dict[str, Any],
    claim_rows: list[dict[str, str]],
    next_rows: list[dict[str, str]],
) -> list[dict[str, str]]:
    checks: list[tuple[str, bool, str]] = []
    checks.append(("V1092_0_local_sources_exist", all(row["exists"] == "true" and row["needle_found"] == "true" for row in source_rows), "all cited source paths and needles are present"))
    checks.append(("V1092_1_triviality_not_derived", any(row["attempt_id"] == "HIT1092_5_verdict" and row["status"] == "TRIVIALITY_NOT_DERIVED" for row in hidden_rows), "hidden invariant algebra triviality ends in explicit non-derivation verdict"))
    checks.append(("V1092_2_scalar_counterexample_retained", any(row["attempt_id"] == "HIT1092_3_scalar_counterexample" and row["status"] == "COUNTEREXAMPLE_PROVED" for row in hidden_rows), "scalar counterexample remains retained"))
    checks.append(("V1092_3_generator_debt_complete", len(generator_rows) >= 7 and all(row["blocks_triviality"] == "true" and row["valid_for_claim"] == "false" for row in generator_rows), "surviving generator ledger blocks triviality and is nonclaim"))
    checks.append(("V1092_4_nohair_unsigned", any(row["audit_id"] == "SNH1092_4_verdict" and row["status"] == "NOHAIR_ROUTE_UNSIGNED" for row in nohair_rows), "scalar nohair route remains unsigned"))
    checks.append(("V1092_5_clock_product_numeric_nonclaim", any(parse_float(row["best_bound"].split("<=")[-1].split()[0]) == BEST_CLOCK_PRODUCT_BOUND and row["valid_for_claim"] == "false" for row in fallback_rows if row["fallback_id"] == "BTP1092_0_best_clock_product"), "best b_alpha*tau clock product is numeric and nonclaim"))
    checks.append(("V1092_6_transfer_gates_blocked", transfer_rows and all(row["claim_allowed"] == "false" for row in transfer_rows), "all clock/WEP/R10/local-GR transfer gates deny claims"))
    checks.append(("V1092_7_prediction_missing_nonclaim", any("MISSING_BETA_SOURCE_ALPHA" in row["product_value"] and row["valid_for_claim"] == "false" for row in prediction_rows_), "WEP prediction row remains missing projection inputs"))
    checks.append(("V1092_8_bound_numeric", bool(bound_rows_) and parse_float(bound_rows_[0]["bound_value"]) is not None and float(bound_rows_[0]["bound_value"]) > 0 and bound_rows_[0]["valid_for_claim"] == "true", "MICROSCOPE bound import is positive numeric"))
    checks.append(("V1092_9_product_runner_refuses", product_status.get("valid_prediction_rows") == 0 and product_status.get("claim_allowed") is False, "generic product runner reports no valid prediction rows and claim false"))
    checks.append(("V1092_10_claim_gates_safe", claim_rows and all(row["claim_allowed"] == "false" for row in claim_rows), "all claim gates deny local-GR/WEP/R10 claims"))
    checks.append(("V1092_11_next_target", any(row["next_target"].startswith("1093-Y5-R10-scalar-nohair-input-owner") for row in next_rows), "1093 handoff written"))
    generated_paths = list(outputs.values()) + [DOC]
    checks.append(("V1092_12_generated_under_post_checkpoint", all(str(path.resolve()).startswith(str(ROOT.resolve())) for path in generated_paths), "all generated outputs are under post-checkpoint-work"))
    checks.append(("V1092_13_csv_parse", csv_outputs_parse([path for key, path in outputs.items() if key != "validation"]), "all 1092 CSV outputs parse cleanly"))
    checks.append(("V1092_14_formalization_untouched", count_formalization_modified_since_start() == 0, "formalization-workbench modified-file count remains zero"))
    checks.append(("V1092_SUMMARY", True, "hidden invariant triviality not derived; scalar nohair input pack unsigned; b_alpha*tau retained as nonclaim fallback"))
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
    hidden_rows: list[dict[str, str]],
    generator_rows: list[dict[str, str]],
    nohair_rows: list[dict[str, str]],
    fallback_rows: list[dict[str, str]],
    transfer_rows: list[dict[str, str]],
    product_status_rows_: list[dict[str, str]],
    product_comparisons: list[dict[str, Any]],
    claim_rows: list[dict[str, str]],
    decisions: list[dict[str, str]],
    validation_rows: list[dict[str, str]],
    next_rows: list[dict[str, str]],
) -> None:
    text = "\n".join(
        [
            "# 1092-Y5-R10 hidden-invariant algebra triviality or b_alpha tau projection",
            "",
            "## Current verdict",
            "1092 tries the cleanest remaining route: prove the local hidden invariant algebra is trivial so hidden motion cannot feed ordinary alpha, matter, clock, source, or readout coefficients. The sufficiency theorem is sharp, but the present corpus does not prove its premise. The surviving generator ledger still contains finite-cell, domain, selector, memory/class, species, readout, and time-arrow markers, and any nonconstant hidden invariant scalar builds the forbidden coefficient map. So local-GR/WEP/R10 safety remains blocked. The only usable empirical object here is the source-backed nonclaim clock product bound `|b_alpha*tau_clock_time| <= 2.1e-18 yr^-1`.",
            "",
            "## Source register",
            md_table(source_rows, ["source_id", "relative_path", "exists", "needle_found", "note"]),
            "## Hidden-invariant triviality attempt",
            md_table(hidden_rows, ["attempt_id", "claim_piece", "mathematical_statement", "status", "proof_or_obstruction", "claim_effect"]),
            "## Surviving generator ledger",
            md_table(generator_rows, ["generator_id", "generator", "current_status", "blocks_triviality", "risk", "required_elimination"]),
            "## Scalar nohair route audit",
            md_table(nohair_rows, ["audit_id", "input_needed", "mathematical_need", "status", "effect"]),
            "## b_alpha tau projection fallback",
            md_table(fallback_rows, ["fallback_id", "product", "best_bound", "source_basis", "usable_now", "missing_for_claim"]),
            "## WEP/R10 transfer gates",
            md_table(transfer_rows, ["gate_id", "arena", "transfer_claim", "gate_status", "reason", "claim_allowed"]),
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
    hidden_rows = hidden_invariant_attempt_rows()
    generator_rows = surviving_generator_rows()
    nohair_rows = scalar_nohair_rows()
    fallback_rows = balpha_tau_rows()
    transfer_rows = transfer_gate_rows()
    prediction_rows_ = prediction_rows()
    bound_rows_ = bound_import_rows()
    next_rows = next_target_rows()

    outputs = {
        "source_register": OUT / "P8_Y5_R10_1092_SOURCE_REGISTER.csv",
        "hidden_attempt": OUT / "P8_Y5_R10_1092_HIDDEN_INVARIANT_TRIVIALITY_ATTEMPT.csv",
        "surviving_generators": OUT / "P8_Y5_R10_1092_SURVIVING_GENERATOR_LEDGER.csv",
        "scalar_nohair": OUT / "P8_Y5_R10_1092_SCALAR_NOHAIR_ROUTE_AUDIT.csv",
        "fallback": OUT / "P8_Y5_R10_1092_BALPHA_TAU_PROJECTION_FALLBACK.csv",
        "transfer_gates": OUT / "P8_Y5_R10_1092_WEP_R10_TRANSFER_GATES.csv",
        "prediction": PREDICTION_TEMPLATE,
        "bound": BOUND_IMPORT,
        "product_status": OUT / "P8_Y5_R10_1092_PRODUCT_RUNNER_STATUS.csv",
        "product_comparison": OUT / "P8_Y5_R10_1092_PRODUCT_COMPARISON_ROWS.csv",
        "claim_gates": OUT / "P8_Y5_R10_1092_CLAIM_GATES.csv",
        "decisions": OUT / "P8_Y5_R10_1092_DECISION_LEDGER.csv",
        "next_target": OUT / "P8_Y5_R10_1092_NEXT_TARGET.csv",
        "validation": OUT / "P8_Y5_BRR545_1092_VALIDATION.csv",
    }

    write_csv(outputs["source_register"], source_rows)
    write_csv(outputs["hidden_attempt"], hidden_rows)
    write_csv(outputs["surviving_generators"], generator_rows)
    write_csv(outputs["scalar_nohair"], nohair_rows)
    write_csv(outputs["fallback"], fallback_rows)
    write_csv(outputs["transfer_gates"], transfer_rows)
    write_csv(outputs["prediction"], prediction_rows_, PRODUCT_REQUIRED_COLUMNS)
    write_csv(outputs["bound"], bound_rows_, BOUND_REQUIRED_COLUMNS)

    product_result = run_product_runner(PREDICTION_TEMPLATE, BOUND_IMPORT, PRODUCT_RUN_DIR)
    product_status = product_result["status"]
    product_status_rows_ = product_status_rows(product_status)
    product_comparisons = product_result["comparisons"]
    claim_rows = claim_gate_rows(product_status)
    decisions = decision_rows()

    write_csv(outputs["product_status"], product_status_rows_)
    write_csv(outputs["product_comparison"], product_comparisons)
    write_csv(outputs["claim_gates"], claim_rows)
    write_csv(outputs["decisions"], decisions)
    write_csv(outputs["next_target"], next_rows)

    validation_rows = validate_outputs(
        outputs,
        source_rows,
        hidden_rows,
        generator_rows,
        nohair_rows,
        fallback_rows,
        transfer_rows,
        prediction_rows_,
        bound_rows_,
        product_status,
        claim_rows,
        next_rows,
    )
    write_csv(outputs["validation"], validation_rows)
    write_doc(
        source_rows,
        hidden_rows,
        generator_rows,
        nohair_rows,
        fallback_rows,
        transfer_rows,
        product_status_rows_,
        product_comparisons,
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

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
DOC = ROOT / "1093-Y5-R10-scalar-nohair-input-owner-or-balpha-tau-projection-source.md"
FORMALIZATION = ROOT.parent / "formalization-workbench"
RUN_DIR = ROOT / "runs" / "1093-scalar-nohair-input-owner" / "results"
PRODUCT_RUN_DIR = RUN_DIR / "product_runner"
PREDICTION_TEMPLATE = OUT / "P8_Y5_R10_1093_WEP_PRODUCT_CANDIDATE_NONCLAIM.csv"
BOUND_IMPORT = OUT / "P8_Y5_R10_1093_WEP_BOUND_IMPORT.csv"
BEST_CLOCK_PRODUCT_BOUND = 2.1e-18
ETA_BOUND = 2.8e-15


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
        ("SRC1093_0_1092_next", "source-intake/mts_residuals/P8_Y5_R10_1092_NEXT_TARGET.csv", "NEXT1092_0_1093", "1092 handoff."),
        ("SRC1093_1_1092_nohair", "source-intake/mts_residuals/P8_Y5_R10_1092_SCALAR_NOHAIR_ROUTE_AUDIT.csv", "SNH1092_4_verdict", "latest nohair route audit."),
        ("SRC1093_2_1022_nohair", "source-intake/mts_residuals/P8_Y5_R10_1022_SCALAR_NOHAIR_CONSTRUCTION.csv", "SNH1022_6_verdict", "scalar nohair construction clauses."),
        ("SRC1093_3_1042_identity", "source-intake/mts_residuals/P8_Y5_R10_1042_POSITIVE_X_NOHAIR_IDENTITY.csv", "NH1042_5_verdict", "positive X nohair identity."),
        ("SRC1093_4_1042_gate", "source-intake/mts_residuals/P8_Y5_R10_1042_NOHAIR_PREMISE_GATE.csv", "NHP1042_6_verdict", "nohair premise gate."),
        ("SRC1093_5_647_chix", "source-intake/mts_residuals/P8_Y5_R10_647_CHIX_DEFINITION_ATTEMPT.csv", "CHX647_1_finite_alpha_pressure_coordinate", "chi_X definition attempt."),
        ("SRC1093_6_647_tau", "source-intake/mts_residuals/P8_Y5_R10_647_TAU_CLOCK_MAP.csv", "TAU647_0_time_drift", "tau_clock product map."),
        ("SRC1093_7_648_local", "source-intake/mts_residuals/P8_Y5_R10_648_LOCAL_CHIX_DYNAMICS_ATTEMPT.csv", "LCD648_1_closed_gapped_boundary_state", "local chi_X dynamics attempt."),
        ("SRC1093_8_1052_tau", "source-intake/mts_residuals/P8_Y5_R10_1052_TAU_CLOCK_XHAT_NORMALIZATION_AUDIT.csv", "TCN1052_4_verdict", "tau_clock/Xhat normalization audit."),
        ("SRC1093_9_1052_clock_bound", "source-intake/mts_residuals/P8_Y5_R10_1052_ALPHA_CLOCK_PRODUCT_BOUND_LEDGER.csv", "ACB1052_2", "best clock product row."),
        ("SRC1093_10_1053_tau_projection", "source-intake/mts_residuals/P8_Y5_R10_1053_TAU_WEP_R10_PROJECTION_AUDIT.csv", "TPR1053_4_verdict", "clock/WEP/R10 projection audit."),
        ("SRC1093_11_1061_beta_tau", "source-intake/mts_residuals/P8_Y5_R10_1061_BETA_TAU_DERIVATION_ATTEMPT.csv", "DER1061_2_tau_WEP", "beta_source_alpha/tau_WEP derivation attempt."),
        ("SRC1093_12_1067_tau_functional", "source-intake/mts_residuals/P8_Y5_R10_1067_TAU_WEP_FUNCTIONAL_DECOMPOSITION.csv", "TWF1067_6_verdict", "tau_WEP functional decomposition."),
        ("SRC1093_13_1069_tau_source", "source-intake/mts_residuals/P8_Y5_R10_1069_FIRST_REAL_TAU_SOURCE_ROW.csv", "WTS1069_0_MICROSCOPE_eta_source_charge_proxy", "first real WEP tau source/readout row."),
        ("SRC1093_14_1072_numeric_tau", "source-intake/mts_residuals/P8_Y5_R10_1072_NUMERIC_TAU_STATUS.csv", "NTS1072_2_tau_WEP", "numeric tau acquisition status."),
        ("SRC1093_15_local_bounds", "source-intake/local_bounds/local_bound_claims.csv", "R1_WEP_source_charge", "MICROSCOPE WEP bound anchor."),
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


def parent_owner_rows() -> list[dict[str, str]]:
    return [
        {
            "owner_id": "OWN1093_0_target",
            "candidate_owner": "parent scalar Xhat/I controlling visible coefficients",
            "needed_identity": "d ln(alpha_EM)=b_alpha dXhat and the same Xhat enters L_X Xhat=J_X",
            "current_status": "TARGET_SHARP",
            "why_not_closed": "not yet identified as a parent field rather than a closure coordinate",
            "if_closed": "clock, WEP, and R10 can share one normalization instead of separate placeholders",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "owner_id": "OWN1093_1_chiX",
            "candidate_owner": "chi_X finite alpha-pressure coordinate",
            "needed_identity": "chi_X is a parent-owned local field with units and action normalization",
            "current_status": "CLOSURE_COORDINATE_ONLY",
            "why_not_closed": "CHX647_1 defines d ln(alpha_EM)=b_alpha dchi_X, but not the parent state variable",
            "if_closed": "could turn the clock product into a theory-normalized alpha branch",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "owner_id": "OWN1093_2_vertical_norm",
            "candidate_owner": "parent vertical norm C_P N_Q hbar c",
            "needed_identity": "alpha_EM quotient-fixed or alpha pressure equals a vertical norm response",
            "current_status": "NOT_DERIVED",
            "why_not_closed": "C_P, N_Q, coframe descent, and no-extra-F2 remain unsigned in the prior chain",
            "if_closed": "could force b_alpha=0 or make alpha response parent-owned",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "owner_id": "OWN1093_3_clock_coframe",
            "candidate_owner": "clock/coframe scalar C_clock[Q_coh,D]",
            "needed_identity": "chi_X is the same signed clock scalar used by observed clock/redshift maps",
            "current_status": "THEOREM_TARGET_NOT_DERIVED",
            "why_not_closed": "clock scalar is not parent-derived and may be gauge/closure if not action-owned",
            "if_closed": "could connect alpha drift to the observer/coframe sector",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "owner_id": "OWN1093_4_verdict",
            "candidate_owner": "unique parent owner for dangerous scalar coefficient",
            "needed_identity": "one parent-normalized Xhat controls b_alpha and obeys the nohair operator",
            "current_status": "PARENT_OWNER_NOT_DERIVED",
            "why_not_closed": "all candidates are either closure coordinates or unsigned theorem targets",
            "if_closed": "would unlock the positive nohair identity as a local-GR route",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
    ]


def operator_input_rows() -> list[dict[str, str]]:
    return [
        {
            "input_id": "OP1093_0_LX_owner",
            "required_input": "parent L_X selected from second variation",
            "mathematical_role": "defines the self-adjoint operator acting on the same Xhat that controls visible coefficients",
            "current_status": "MISSING_PARENT_LX",
            "source_basis": "NHP1042_0_LX_owner; SNH1022_0_operator",
            "blocks_claim": "true",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "input_id": "OP1093_1_Z_positive",
            "required_input": "Z_X positive kinetic matrix",
            "mathematical_role": "makes int Z_X |grad X|^2 nonnegative",
            "current_status": "FORMULA_ONLY_NOT_PARENT_SIGNED",
            "source_basis": "NHP1042_1_Z_positive; SNH1022_1_positive_kinetic",
            "blocks_claim": "true",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "input_id": "OP1093_2_mass_gap",
            "required_input": "M_X^2 positive gap or justified zero-mode handling",
            "mathematical_role": "removes long-range scalar zero mode from local exterior",
            "current_status": "FORMULA_ONLY_NOT_PARENT_SIGNED",
            "source_basis": "NHP1042_2_mass_gap; SNH1022_2_positive_mass_gap",
            "blocks_claim": "true",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "input_id": "OP1093_3_self_adjoint_domain",
            "required_input": "self-adjoint local domain and boundary class",
            "mathematical_role": "permits integration by parts without hidden leakage",
            "current_status": "MISSING_DOMAIN_SIGNATURE",
            "source_basis": "SNH1022_0_operator; NHP1042_0_LX_owner",
            "blocks_claim": "true",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "input_id": "OP1093_4_verdict",
            "required_input": "claim-grade positive operator pack",
            "mathematical_role": "supports positive nohair identity for MTS rather than generic math",
            "current_status": "OPERATOR_PACK_UNSIGNED",
            "source_basis": "NH1042_5_verdict",
            "blocks_claim": "true",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
    ]


def source_silence_rows() -> list[dict[str, str]]:
    return [
        {
            "silence_id": "JX1093_0_target",
            "channel": "ordinary matter/source current",
            "needed_zero": "J_X^matter=0",
            "current_status": "CONDITIONAL_ON_MOMS",
            "obstruction": "MOMS1088 zero theorem exists only if the parent ordinary-matter signature is signed",
            "finite_fallback": "retain beta_source_alpha or qbar source coefficients",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "silence_id": "JX1093_1_alpha",
            "channel": "alpha/EM coefficient",
            "needed_zero": "partial_X ln(alpha_EM)=0 or parent-owned b_alpha with no local source",
            "current_status": "NOT_DERIVED",
            "obstruction": "alpha owner and no-extra-F2 theorem remain unsigned",
            "finite_fallback": f"|b_alpha*tau_clock_time| <= {BEST_CLOCK_PRODUCT_BOUND:.12e} yr^-1",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "silence_id": "JX1093_2_WEP_source",
            "channel": "WEP source/test material projection",
            "needed_zero": "beta_source_alpha*tau_WEP=0 or bounded numeric product",
            "current_status": "PROJECTION_NOT_DERIVED",
            "obstruction": "tau_WEP source worldtube, orbit average, force readout, material tensor, and Xhat normalization are incomplete",
            "finite_fallback": "source/readout bound anchor exists but no scoreable MTS product",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "silence_id": "JX1093_3_R10_source",
            "channel": "R10 source/test Yukawa projection",
            "needed_zero": "beta_s beta_t K_X/Z_X tau_R10=0 or bounded alpha(lambda)",
            "current_status": "PROJECTION_NOT_DERIVED",
            "obstruction": "tau_R10 and K_X/Z_X/lambda_X remain definition/template rows",
            "finite_fallback": "R10 remains smoke/schema only",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "silence_id": "JX1093_4_verdict",
            "channel": "source-free nohair premise",
            "needed_zero": "J_X=0 channelwise",
            "current_status": "SOURCE_SILENCE_NOT_DERIVED",
            "obstruction": "ordinary matter, alpha, WEP, R10, boundary, and readout channels are not all parent-silenced",
            "finite_fallback": "continue finite product/source acquisition",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
    ]


def boundary_domain_rows() -> list[dict[str, str]]:
    return [
        {
            "boundary_id": "BD1093_0_boundary_flux",
            "needed_clause": "Phi_boundary_local=0 or explicit upper bound",
            "current_status": "BOUNDARY_FLUX_ZERO_NOT_DERIVED",
            "risk_if_missing": "hidden scalar can enter through the boundary even with bulk source silence",
            "source_basis": "NHP1042_4_boundary_flux_zero; SNH1022_4_boundary_flux_zero",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "boundary_id": "BD1093_1_zero_mode",
            "needed_clause": "no topological/gauge zero mode outside quotient kernel",
            "current_status": "TOPOLOGY_KERNEL_GATE_OPEN",
            "risk_if_missing": "positive norm may fail to kill an allowed flat/local mode",
            "source_basis": "NHP1042_5_no_zero_mode",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "boundary_id": "BD1093_2_local_silence",
            "needed_clause": "closed/gapped local coframe/boundary state parent-selected",
            "current_status": "CONDITIONAL_ONLY_NOT_ACTIVE",
            "risk_if_missing": "tau_clock_local=0 remains a plateau axiom, not a derivation",
            "source_basis": "LCD648_0_strict_local_coframe; LCD648_1_closed_gapped_boundary_state",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "boundary_id": "BD1093_3_domain_selector",
            "needed_clause": "domain selector/readout is after-variation and cannot source X",
            "current_status": "NO_CHEAT_RULE_ONLY",
            "risk_if_missing": "post-readout projector re-enters as an effective source",
            "source_basis": "GEN1092_6_readout_projector",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
    ]


def conditional_nohair_rows() -> list[dict[str, str]]:
    return [
        {
            "theorem_id": "THM1093_0_assumptions",
            "step": "assume parent-owned Xhat",
            "mathematical_statement": "Xhat is the same field in the visible coefficient c(Xhat) and in L_X Xhat=J_X",
            "status": "ASSUMPTION_NOT_SIGNED",
            "consequence": "without this, nohair may silence the wrong variable",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "theorem_id": "THM1093_1_energy_identity",
            "step": "multiply by Xhat and integrate over local exterior A",
            "mathematical_statement": "int_A[Z_X|grad Xhat|^2+M_X^2 Xhat^2+positive_mix] = int_A Xhat J_X + Phi_boundary",
            "status": "CONDITIONAL_MATH_VALID",
            "consequence": "matches 1042 identity once operator/domain signs exist",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "theorem_id": "THM1093_2_zero_result",
            "step": "set J_X=0 and Phi_boundary=0 with positive gap/no zero mode",
            "mathematical_statement": "positive integral equals zero, hence grad Xhat=0 and Xhat=0 or constant reference on A",
            "status": "EXACT_CONDITIONAL_THEOREM",
            "consequence": "would silence c(Xhat) locally and reopen local-GR route",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "theorem_id": "THM1093_3_failure_mode",
            "step": "drop any one premise",
            "mathematical_statement": "missing owner, sign, source silence, boundary zero, or domain permits finite profile/residual",
            "status": "FINITE_BRANCH_REQUIRED",
            "consequence": "must score b_alpha*tau, tau_WEP, tau_R10, K_X/Z_X products instead",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "theorem_id": "THM1093_4_verdict",
            "step": "apply theorem to MTS current corpus",
            "mathematical_statement": "all nohair premises are required together; current source audit does not sign them",
            "status": "CONDITIONAL_THEOREM_NOT_PROMOTED",
            "consequence": "no local-GR/WEP/R10 claim; keep nohair as exact contract for parent action",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
    ]


def projection_source_rows() -> list[dict[str, str]]:
    return [
        {
            "projection_id": "PS1093_0_clock",
            "arena": "clock",
            "object": "b_alpha*tau_clock_time",
            "current_evidence": f"source-backed product bound <= {BEST_CLOCK_PRODUCT_BOUND:.12e} yr^-1",
            "status": "USABLE_NONCLAIM_PRODUCT_BOUND",
            "missing_for_claim": "parent tau_clock_time and standalone b_alpha",
            "next_source_need": "derive Xhat/chi_X normalization or keep product-only scoring",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "projection_id": "PS1093_1_tau_WEP",
            "arena": "MICROSCOPE_WEP",
            "object": "tau_WEP",
            "current_evidence": "real eta/readout bound anchor exists from 1069; numeric tau not acquired in 1072",
            "status": "PARTIAL_SOURCE_CONTEXT_NO_NUMERIC_TAU",
            "missing_for_claim": "source worldtube, orbit kernel, force readout, material tensor, Xhat normalization",
            "next_source_need": "build direct product row or acquire CMSM/orbit/attitude arrays",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "projection_id": "PS1093_2_beta_source_alpha",
            "arena": "MICROSCOPE_WEP",
            "object": "beta_source_alpha",
            "current_evidence": "1061 defines product target but not source coefficient",
            "status": "NOT_DERIVED",
            "missing_for_claim": "alpha-channel source/force normalization or theorem-zero",
            "next_source_need": "use Damour-Donoghue/material model only as sourced finite product, not a hidden cancellation",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "projection_id": "PS1093_3_tau_R10",
            "arena": "R10_short_range",
            "object": "tau_R10",
            "current_evidence": "definition/template rows only",
            "status": "DEFINITION_ONLY",
            "missing_for_claim": "profile convention, material/readout trace, K_X/Z_X, lambda_X, promoted bound curve",
            "next_source_need": "source real R10 alpha(lambda) curve and one real projected MTS product row",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
    ]


def prediction_rows() -> list[dict[str, str]]:
    return [
        {
            "prediction_id": "PRED1093_0_WEP_direct_product_missing",
            "arena": "MICROSCOPE_WEP",
            "product_symbol": "P_WEP_alpha",
            "product_value": "MISSING_DIRECT_PRODUCT_OR_BETA_SOURCE_ALPHA_TIMES_TAU_WEP",
            "product_units": "dimensionless",
            "product_source": "source-intake/mts_residuals/P8_Y5_R10_1093_BALPHA_TAU_PROJECTION_SOURCE_LEDGER.csv",
            "inputs_present": "clock product bound; MICROSCOPE bound anchor; partial tau_WEP source context",
            "required_inputs": "direct P_WEP_alpha from parent/source projection OR beta_source_alpha and tau_WEP with material/readout normalization",
            "derivation_status": "MISSING_SCOREABLE_WEP_PRODUCT",
            "valid_for_claim": "false",
            "notes": "no transfer from clock branch; no tau=1 shortcut; runner must refuse",
        }
    ]


def bound_import_rows() -> list[dict[str, str]]:
    return [
        {
            "bound_id": "BOUND1093_0_MICROSCOPE_WEP",
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
            "runner_id": "APR1093_0_WEP_product_stub",
            "prediction_rows": str(product_status.get("prediction_rows", "")),
            "bound_rows": str(product_status.get("bound_rows", "")),
            "valid_prediction_rows": str(product_status.get("valid_prediction_rows", "")),
            "valid_bound_rows": str(product_status.get("valid_bound_rows", "")),
            "comparison_rows": str(product_status.get("comparison_rows", "")),
            "claim_allowed": str(product_status.get("claim_allowed", "")).lower(),
            "expected_result": "reject missing direct WEP product or beta_source_alpha*tau_WEP",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        }
    ]


def claim_gate_rows(product_status: dict[str, Any]) -> list[dict[str, str]]:
    return [
        {
            "gate_id": "CG1093_0_parent_owner",
            "claim_component": "dangerous scalar is parent-owned",
            "gate_pass": "false",
            "claim_allowed": "false",
            "reason": "OWN1093_4_verdict=PARENT_OWNER_NOT_DERIVED",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "gate_id": "CG1093_1_positive_nohair",
            "claim_component": "positive source-free nohair theorem applies to MTS",
            "gate_pass": "false",
            "claim_allowed": "false",
            "reason": "operator pack, source silence, boundary flux, and zero-mode gates remain unsigned",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "gate_id": "CG1093_2_clock_to_WEP",
            "claim_component": "clock product transfers to WEP",
            "gate_pass": "false",
            "claim_allowed": "false",
            "reason": "tau_WEP/beta_source_alpha/direct product is missing",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "gate_id": "CG1093_3_R10_transfer",
            "claim_component": "clock product transfers to R10 alpha(lambda)",
            "gate_pass": "false",
            "claim_allowed": "false",
            "reason": "tau_R10, K_X/Z_X, lambda_X, and promoted bound curve are missing",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "gate_id": "CG1093_4_product_runner",
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
            "decision_id": "DEC1093_0_nohair_contract",
            "decision": "positive nohair is now an exact parent-action contract, not an active MTS claim",
            "because": "the energy identity is valid, but parent owner, signs, source silence, boundary, and zero-mode gates are unsigned",
            "next_action": "either derive the parent Xhat action clauses or test finite products",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "decision_id": "DEC1093_1_best_finite_path",
            "decision": "finite route should target a direct WEP product before standalone factors",
            "because": "tau_WEP and beta_source_alpha are individually hard, but a direct P_WEP_alpha row can be source-scored without fake division",
            "next_action": "build direct WEP product source-pack from material/readout/source conventions",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "decision_id": "DEC1093_2_best_next",
            "decision": "go after the direct WEP product source pack while preserving the nohair contract",
            "because": "this is less scrutiny-prone than asserting tau=1 or standalone b_alpha",
            "next_action": "1094-Y5-R10-direct-WEP-product-source-pack-or-parent-Xhat-action-clause.md",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
    ]


def next_target_rows() -> list[dict[str, str]]:
    return [
        {
            "next_id": "NEXT1093_0_1094",
            "next_target": "1094-Y5-R10-direct-WEP-product-source-pack-or-parent-Xhat-action-clause.md",
            "objective": "construct a source-backed direct P_WEP_alpha product row or derive the parent Xhat action clause that makes the scalar nohair contract active",
            "include": "direct product scoring convention; MICROSCOPE eta/readout map; Ti/Pt material response; source worldtube convention; Xhat normalization; nohair parent-action clause attempt",
            "exclude": "tau_WEP=1 shortcut; clock-to-WEP transfer; factor division without sources; cancellation arguments; local-GR/WEP/R10 claim; GitHub; formalization edits",
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
    owner_rows: list[dict[str, str]],
    operator_rows: list[dict[str, str]],
    silence_rows: list[dict[str, str]],
    boundary_rows: list[dict[str, str]],
    theorem_rows: list[dict[str, str]],
    projection_rows: list[dict[str, str]],
    prediction_rows_: list[dict[str, str]],
    bound_rows_: list[dict[str, str]],
    product_status: dict[str, Any],
    claim_rows: list[dict[str, str]],
    next_rows: list[dict[str, str]],
) -> list[dict[str, str]]:
    checks: list[tuple[str, bool, str]] = []
    checks.append(("V1093_0_local_sources_exist", all(row["exists"] == "true" and row["needle_found"] == "true" for row in source_rows), "all cited source paths and needles are present"))
    checks.append(("V1093_1_parent_owner_not_derived", any(row["owner_id"] == "OWN1093_4_verdict" and row["current_status"] == "PARENT_OWNER_NOT_DERIVED" for row in owner_rows), "parent owner verdict is explicit"))
    checks.append(("V1093_2_operator_pack_unsigned", any(row["input_id"] == "OP1093_4_verdict" and row["current_status"] == "OPERATOR_PACK_UNSIGNED" for row in operator_rows), "positive operator pack remains unsigned"))
    checks.append(("V1093_3_source_silence_blocked", any(row["silence_id"] == "JX1093_4_verdict" and row["current_status"] == "SOURCE_SILENCE_NOT_DERIVED" for row in silence_rows), "source-silence verdict is explicit"))
    checks.append(("V1093_4_boundary_domain_blocked", boundary_rows and all(row["valid_for_claim"] == "false" for row in boundary_rows), "boundary/domain clauses are nonclaim and blocked"))
    checks.append(("V1093_5_conditional_theorem_only", any(row["theorem_id"] == "THM1093_4_verdict" and row["status"] == "CONDITIONAL_THEOREM_NOT_PROMOTED" for row in theorem_rows), "conditional nohair theorem is not promoted"))
    checks.append(("V1093_6_projection_status_nonclaim", projection_rows and all(row["valid_for_claim"] == "false" for row in projection_rows), "projection source ledger remains nonclaim"))
    checks.append(("V1093_7_clock_product_numeric", any(str(BEST_CLOCK_PRODUCT_BOUND) in row["current_evidence"] or "2.100000000000e-18" in row["current_evidence"] for row in projection_rows if row["projection_id"] == "PS1093_0_clock"), "clock product bound retained numerically"))
    checks.append(("V1093_8_prediction_missing_nonclaim", any("MISSING_DIRECT_PRODUCT" in row["product_value"] and row["valid_for_claim"] == "false" for row in prediction_rows_), "WEP prediction row remains missing direct product"))
    checks.append(("V1093_9_bound_numeric", bool(bound_rows_) and parse_float(bound_rows_[0]["bound_value"]) is not None and float(bound_rows_[0]["bound_value"]) > 0 and bound_rows_[0]["valid_for_claim"] == "true", "MICROSCOPE bound import is positive numeric"))
    checks.append(("V1093_10_product_runner_refuses", product_status.get("valid_prediction_rows") == 0 and product_status.get("claim_allowed") is False, "generic product runner reports no valid prediction rows and claim false"))
    checks.append(("V1093_11_claim_gates_safe", claim_rows and all(row["claim_allowed"] == "false" for row in claim_rows), "all claim gates deny local-GR/WEP/R10 claims"))
    checks.append(("V1093_12_next_target", any(row["next_target"].startswith("1094-Y5-R10-direct-WEP-product-source-pack") for row in next_rows), "1094 handoff written"))
    generated_paths = list(outputs.values()) + [DOC]
    checks.append(("V1093_13_generated_under_post_checkpoint", all(str(path.resolve()).startswith(str(ROOT.resolve())) for path in generated_paths), "all generated outputs are under post-checkpoint-work"))
    checks.append(("V1093_14_csv_parse", csv_outputs_parse([path for key, path in outputs.items() if key != "validation"]), "all 1093 CSV outputs parse cleanly"))
    checks.append(("V1093_15_formalization_untouched", count_formalization_modified_since_start() == 0, "formalization-workbench modified-file count remains zero"))
    checks.append(("V1093_SUMMARY", True, "scalar nohair theorem remains exact but conditional; parent owner unsigned; direct WEP product pack is best next route"))
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
    owner_rows: list[dict[str, str]],
    operator_rows: list[dict[str, str]],
    silence_rows: list[dict[str, str]],
    boundary_rows: list[dict[str, str]],
    theorem_rows: list[dict[str, str]],
    projection_rows: list[dict[str, str]],
    product_status_rows_: list[dict[str, str]],
    product_comparisons: list[dict[str, Any]],
    claim_rows: list[dict[str, str]],
    decisions: list[dict[str, str]],
    validation_rows: list[dict[str, str]],
    next_rows: list[dict[str, str]],
) -> None:
    text = "\n".join(
        [
            "# 1093-Y5-R10 scalar nohair input owner or b_alpha tau projection source",
            "",
            "## Current verdict",
            "1093 sharpens the local-GR route into an exact contract: if the dangerous scalar is parent-owned, has a positive self-adjoint local operator, has channelwise `J_X=0`, has zero/bounded boundary flux, and has no zero-mode leakage, the standard energy identity forces the local scalar profile to vanish. That is real math, but it is still conditional for MTS. The current corpus does not yet identify `chi_X`/`Xhat` as the parent-owned operator variable, and the sign/source/boundary clauses remain unsigned. So we should not claim local-GR/WEP/R10 safety. The best next empirical move is a direct `P_WEP_alpha` product source pack rather than dividing clock bounds by guessed tau factors.",
            "",
            "## Source register",
            md_table(source_rows, ["source_id", "relative_path", "exists", "needle_found", "note"]),
            "## Parent scalar owner attempt",
            md_table(owner_rows, ["owner_id", "candidate_owner", "needed_identity", "current_status", "why_not_closed", "if_closed"]),
            "## Positive operator input pack",
            md_table(operator_rows, ["input_id", "required_input", "mathematical_role", "current_status", "source_basis", "blocks_claim"]),
            "## Source silence audit",
            md_table(silence_rows, ["silence_id", "channel", "needed_zero", "current_status", "obstruction", "finite_fallback"]),
            "## Boundary/domain audit",
            md_table(boundary_rows, ["boundary_id", "needed_clause", "current_status", "risk_if_missing", "source_basis"]),
            "## Conditional nohair theorem",
            md_table(theorem_rows, ["theorem_id", "step", "mathematical_statement", "status", "consequence"]),
            "## b_alpha tau projection source ledger",
            md_table(projection_rows, ["projection_id", "arena", "object", "current_evidence", "status", "missing_for_claim", "next_source_need"]),
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
    owner_rows = parent_owner_rows()
    operator_rows = operator_input_rows()
    silence_rows = source_silence_rows()
    boundary_rows = boundary_domain_rows()
    theorem_rows = conditional_nohair_rows()
    projection_rows = projection_source_rows()
    prediction_rows_ = prediction_rows()
    bound_rows_ = bound_import_rows()
    next_rows = next_target_rows()

    outputs = {
        "source_register": OUT / "P8_Y5_R10_1093_SOURCE_REGISTER.csv",
        "parent_owner": OUT / "P8_Y5_R10_1093_PARENT_SCALAR_OWNER_ATTEMPT.csv",
        "operator_inputs": OUT / "P8_Y5_R10_1093_POSITIVE_OPERATOR_INPUT_PACK.csv",
        "source_silence": OUT / "P8_Y5_R10_1093_SOURCE_SILENCE_AUDIT.csv",
        "boundary_domain": OUT / "P8_Y5_R10_1093_BOUNDARY_DOMAIN_AUDIT.csv",
        "conditional_theorem": OUT / "P8_Y5_R10_1093_CONDITIONAL_NOHAIR_THEOREM.csv",
        "projection_sources": OUT / "P8_Y5_R10_1093_BALPHA_TAU_PROJECTION_SOURCE_LEDGER.csv",
        "prediction": PREDICTION_TEMPLATE,
        "bound": BOUND_IMPORT,
        "product_status": OUT / "P8_Y5_R10_1093_PRODUCT_RUNNER_STATUS.csv",
        "product_comparison": OUT / "P8_Y5_R10_1093_PRODUCT_COMPARISON_ROWS.csv",
        "claim_gates": OUT / "P8_Y5_R10_1093_CLAIM_GATES.csv",
        "decisions": OUT / "P8_Y5_R10_1093_DECISION_LEDGER.csv",
        "next_target": OUT / "P8_Y5_R10_1093_NEXT_TARGET.csv",
        "validation": OUT / "P8_Y5_BRR545_1093_VALIDATION.csv",
    }

    write_csv(outputs["source_register"], source_rows)
    write_csv(outputs["parent_owner"], owner_rows)
    write_csv(outputs["operator_inputs"], operator_rows)
    write_csv(outputs["source_silence"], silence_rows)
    write_csv(outputs["boundary_domain"], boundary_rows)
    write_csv(outputs["conditional_theorem"], theorem_rows)
    write_csv(outputs["projection_sources"], projection_rows)
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
        owner_rows,
        operator_rows,
        silence_rows,
        boundary_rows,
        theorem_rows,
        projection_rows,
        prediction_rows_,
        bound_rows_,
        product_status,
        claim_rows,
        next_rows,
    )
    write_csv(outputs["validation"], validation_rows)
    write_doc(
        source_rows,
        owner_rows,
        operator_rows,
        silence_rows,
        boundary_rows,
        theorem_rows,
        projection_rows,
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

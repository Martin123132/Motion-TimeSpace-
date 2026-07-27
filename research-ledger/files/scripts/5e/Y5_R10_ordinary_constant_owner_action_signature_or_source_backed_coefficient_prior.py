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
DOC = ROOT / "1098-Y5-R10-ordinary-constant-owner-action-signature-or-source-backed-coefficient-prior.md"
FORMALIZATION = ROOT.parent / "formalization-workbench"
RUN_DIR = ROOT / "runs" / "1098-ordinary-constant-owner-action-signature" / "results"
PRODUCT_RUN_DIR = RUN_DIR / "product_runner"
PREDICTION_TEMPLATE = OUT / "P8_Y5_R10_1098_CONSTANT_COEFFICIENT_CANDIDATE_NONCLAIM.csv"
BOUND_IMPORT = OUT / "P8_Y5_R10_1098_CONSTANT_COEFFICIENT_BOUND_IMPORT.csv"
DD_ALPHA_COEFF_MAX = 8.320244933243533e-10
DD_SURFACE_COEFF_MAX = 6.987501646143863e-11
DD_COMMON_COEFF_MAX = 6.446142229433907e-11


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
        ("SRC1098_0_1097_next", "source-intake/mts_residuals/P8_Y5_R10_1097_NEXT_TARGET.csv", "NEXT1097_0_1098", "1097 handoff."),
        ("SRC1098_1_1097_theorem", "source-intake/mts_residuals/P8_Y5_R10_1097_CONSTANT_SECTOR_UNIVERSALITY_THEOREM_ATTEMPT.csv", "CSU1097_5_verdict", "constant-sector universality failure."),
        ("SRC1098_2_1097_prior", "source-intake/mts_residuals/P8_Y5_R10_1097_FINITE_COEFFICIENT_SOURCE_PRIOR_LEDGER.csv", "FSP1097_0_c_alpha_DD", "finite coefficient threshold ledger."),
        ("SRC1098_3_1048_doc", "1048-Y5-R10-no-extra-F2-no-mass-vertex-parent-action-signature-or-alpha-mass-bound-matrix.md", "PVS1048_5_verdict", "old parent vertex signature attempt."),
        ("SRC1098_4_1047_alpha", "source-intake/mts_residuals/P8_Y5_R10_1047_ALPHA_GAUGE_NORMALIZATION_AUDIT.csv", "AGN1047_4_verdict", "alpha owner audit."),
        ("SRC1098_5_988_em_gate", "source-intake/mts_residuals/P8_Y5_R10_988_EM_LOCK_THEOREM_GATE.csv", "EMLOCK988_5_theorem_verdict", "EM lock theorem gate."),
        ("SRC1098_6_989_em_audit", "source-intake/mts_residuals/P8_Y5_R10_989_EM_LOCK_SIGNATURE_AUDIT.csv", "ELA989_5_total", "EM lock signature audit."),
        ("SRC1098_7_990_parent_contract", "source-intake/mts_residuals/P8_Y5_R10_990_PARENT_ACTION_CONTRACT.csv", "PAC990_2_matter_functor", "parent action contract."),
        ("SRC1098_8_638_zero", "source-intake/mts_residuals/P8_Y5_R10_638_CONSTANT_ZERO_ROUTE_ATTEMPT.csv", "ZR638_2_particle_masses", "constant zero route attempt."),
        ("SRC1098_9_1048_matrix", "source-intake/mts_residuals/P8_Y5_R10_1048_ALPHA_MASS_CLOCK_BOUND_MATRIX.csv", "BM1048_2_WEP_alpha_mass", "alpha/mass/clock bound matrix."),
        ("SRC1098_10_1051_alpha", "source-intake/mts_residuals/P8_Y5_R10_1051_ALPHA_OWNER_RADIATIVE_CLOSURE_AUDIT.csv", "AOR1051_3_verdict", "alpha radiative closure audit."),
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


def owner_signature_rows() -> list[dict[str, str]]:
    return [
        {
            "clause_id": "OCS1098_0_parent_domain",
            "signature_clause": "parent action declares all constant-sector slots before local tests are fitted",
            "required_form": "S_parent[Phi,Psi]=S_geom[q(Phi)]+S_gauge[A,T_Q,q(Phi)]+S_matter[Psi,e_obs(q),theta_rep]",
            "current_status": "CONTRACT_NEEDED_NOT_PARENT_SIGNED",
            "if_signed": "prevents adding arena-specific hidden constant/source vertices",
            "if_missing": "coefficient priors remain live",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "clause_id": "OCS1098_1_unique_EM_owner",
            "signature_clause": "unique EM kinetic owner and no independent f_X F^2",
            "required_form": "Allowed: -C_P/4 int <F,F>_P; Forbidden: -1/4 int f_X(Xhat) F_Q^2 or lambda_A F_Q^2",
            "current_status": "FAIL_CURRENT_CORPUS_COUNTERTERM_LEGAL",
            "if_signed": "b_alpha theorem-zero from fixed parent gauge norm",
            "if_missing": "alpha, clock, WEP, and R10 branches retain b_alpha/c_alpha",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "clause_id": "OCS1098_2_matter_spectrum_owner",
            "signature_clause": "no Xhat-dependent masses, Yukawas, Higgs/QCD, or binding response",
            "required_form": "Forbidden: m_A(Xhat), y_A(Xhat), Lambda_QCD(Xhat), B_A(Xhat), material response slots depending on Xhat",
            "current_status": "NOT_PARENT_SIGNED",
            "if_signed": "b_mu, b_mA, b_nuc, and composition/binding WEP terms can be theorem-zero",
            "if_missing": "mass/binding/clock/WEP material channels stay live",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "clause_id": "OCS1098_3_clock_readout_owner",
            "signature_clause": "clock/spectral readout descends from quotient-owned coframe plus owned constants",
            "required_form": "nu_i(Phi)=nu_bar_i(q(Phi),theta_rep) with no nu_i(Xhat), Hodge/readout, or shadow-clock slot",
            "current_status": "UNSIGNED",
            "if_signed": "clock residuals inherit zero upstream constants",
            "if_missing": "clock rows remain separate readout residuals",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "clause_id": "OCS1098_4_source_weight_exclusion",
            "signature_clause": "no species/source-only gravitational weights",
            "required_form": "Forbidden: w_A(Xhat)S_A, kappa_A(Xhat)T_A, source-only material multiplier before variation",
            "current_status": "UNSIGNED",
            "if_signed": "WEP/source charge route can close with common Hilbert current",
            "if_missing": "WEP/Newton-GM/R10 source normalization remains retained",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "clause_id": "OCS1098_5_radiative_readout_closure",
            "signature_clause": "forbidden vertices do not re-enter in S_eff or post-variation readout",
            "required_form": "renormalized alpha/mass/readout maps factor through q or fixed theta_rep; readout-after-variation theorem holds",
            "current_status": "RADIATIVE_READOUT_UNSIGNED",
            "if_signed": "bare action signature survives observed tests",
            "if_missing": "b_alpha, b_clock_i, and readout/source coefficients remain live",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "clause_id": "OCS1098_6_verdict",
            "signature_clause": "ordinary-constant owner action signature is derived",
            "required_form": "OCS1098_0 through OCS1098_5 all parent-signed",
            "current_status": "OWNER_ACTION_SIGNATURE_NOT_DERIVED",
            "if_signed": "constant-sector universality and c_I=0 theorem can be promoted",
            "if_missing": "external source-backed coefficient priors required",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
    ]


def forbidden_vertex_rows() -> list[dict[str, str]]:
    specs = [
        ("FV1098_0_parent_F2", "EM", "<F_Q T_Q,F_Q T_Q>_P", "allowed_if_parent_owned", "C_P<T_Q,T_Q>_P", "conditional"),
        ("FV1098_1_scalar_F2", "EM", "f_X(Xhat)F_Q^2 or lambda_A F_Q^2", "forbidden_required_but_currently_legal", "b_alpha,c_alpha", "blocks_claim"),
        ("FV1098_2_mass_X", "matter", "m_A(Xhat) psi_bar_A psi_A", "forbidden_required_but_currently_legal", "b_mA", "blocks_claim"),
        ("FV1098_3_yukawa_X", "matter", "y_A(Xhat) psi_A H psi_B", "forbidden_required_but_currently_legal", "b_mu,b_mA", "blocks_claim"),
        ("FV1098_4_binding_X", "nuclear/binding", "Lambda_QCD(Xhat), B_A(Xhat), nuclear response slot", "forbidden_required_but_currently_legal", "b_nuc,c_surface", "blocks_claim"),
        ("FV1098_5_clock_readout_X", "clock/readout", "nu_i(Xhat), readout_X, Hodge/readout leakage", "forbidden_required_but_currently_legal", "b_clock_i", "blocks_claim"),
        ("FV1098_6_source_weight_X", "source/WEP", "w_A(Xhat), kappa_A(Xhat), source-only material multiplier", "forbidden_required_but_currently_legal", "qbar_source,c_WEP", "blocks_claim"),
    ]
    return [
        {
            "vertex_id": vertex_id,
            "sector": sector,
            "operator_or_slot": slot,
            "classification": classification,
            "coefficient": coefficient,
            "current_status": status,
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        }
        for vertex_id, sector, slot, classification, coefficient, status in specs
    ]


def theorem_rows() -> list[dict[str, str]]:
    return [
        {
            "theorem_id": "OCT1098_0_assumption",
            "claim_piece": "ordinary constants are parent-owned",
            "mathematical_statement": "S_parent has no independent hidden-visible constant vertices beyond quotient-owned or fixed representation data",
            "status": "ASSUMPTION_NOT_SIGNED",
            "consequence": "starts exact theorem route",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "theorem_id": "OCT1098_1_chain_rule",
            "claim_piece": "constant derivatives vanish",
            "mathematical_statement": "theta_A=theta_bar_A(q(Phi)) or theta_rep and Dq[v_X]=0 imply Lie_v theta_A=0",
            "status": "EXACT_CONDITIONAL_THEOREM",
            "consequence": "b_alpha,b_mu,b_mA,b_nuc,b_clock_i,c_I vanish if the signature is signed",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "theorem_id": "OCT1098_2_vertex_counterexample",
            "claim_piece": "any forbidden vertex kills the theorem",
            "mathematical_statement": "DeltaS=-1/4 int f_X(Xhat)F^2 or int m_A(Xhat)psi_bar psi gives nonzero Lie_v theta_A while q is fixed",
            "status": "COUNTEREXAMPLE_RETAINED",
            "consequence": "metric descent alone is insufficient",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "theorem_id": "OCT1098_3_verdict",
            "claim_piece": "promote ordinary-constant owner theorem",
            "mathematical_statement": "all alpha/mass/binding/clock/source-weight vertices are forbidden by the parent action and closure survives readout",
            "status": "OWNER_THEOREM_NOT_PROMOTED",
            "consequence": "finite coefficient/source prior route remains required",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
    ]


def coefficient_source_rows() -> list[dict[str, str]]:
    specs = [
        ("REQ1098_0_c_alpha", "c_alpha_DD or b_alpha", DD_ALPHA_COEFF_MAX, "source-backed alpha coefficient value or no-extra-F2 theorem", "clock;WEP;R10;EM"),
        ("REQ1098_1_c_surface", "c_surface_DD or b_binding", DD_SURFACE_COEFF_MAX, "source-backed surface/binding coefficient value or no-binding-vertex theorem", "WEP;clock;nuclear"),
        ("REQ1098_2_c_common", "common absolute DD scale", DD_COMMON_COEFF_MAX, "source-backed coefficient-vector norm or all-channel theorem-zero", "WEP material vector"),
    ]
    return [
        {
            "requirement_id": requirement_id,
            "coefficient": coefficient,
            "threshold_abs": f"{threshold:.16e}",
            "required_evidence": evidence,
            "observable_arenas": arenas,
            "current_status": "MISSING_SOURCE_BACKED_COEFFICIENT_OR_THEOREM_ZERO",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        }
        for requirement_id, coefficient, threshold, evidence, arenas in specs
    ]


def prediction_rows() -> list[dict[str, str]]:
    return [
        {
            "prediction_id": "PRED1098_0_missing_constant_owner_or_c_alpha_source",
            "arena": "MICROSCOPE_WEP",
            "product_symbol": "c_alpha_DD",
            "product_value": "MISSING_OWNER_SIGNATURE_OR_SOURCE_BACKED_C_ALPHA",
            "product_units": "dimensionless",
            "product_source": "source-intake/mts_residuals/P8_Y5_R10_1098_ORDINARY_CONSTANT_OWNER_SIGNATURE_ATTEMPT.csv",
            "inputs_present": "1097 constant-sector theorem attempt; 1048 vertex audit; 1097 coefficient threshold",
            "required_inputs": "signed ordinary-constant owner signature or external source-backed c_alpha_DD value",
            "derivation_status": "MISSING_SCOREABLE_CONSTANT_COEFFICIENT",
            "valid_for_claim": "false",
            "notes": "unit rescaling, clock transfer, and unsourced priors are forbidden",
        }
    ]


def bound_import_rows() -> list[dict[str, str]]:
    return [
        {
            "bound_id": "BOUND1098_0_c_alpha_DD_threshold",
            "arena": "MICROSCOPE_WEP",
            "product_symbol": "c_alpha_DD",
            "bound_value": f"{DD_ALPHA_COEFF_MAX:.16e}",
            "bound_units": "dimensionless",
            "bound_source": "source-intake/mts_residuals/P8_Y5_R10_1097_FINITE_COEFFICIENT_SOURCE_PRIOR_LEDGER.csv",
            "source_row": "FSP1097_0_c_alpha_DD",
            "bound_type": "absolute_constant_coefficient_threshold_nonclaim",
            "valid_for_claim": "false",
            "notes": "threshold only; no source-backed MTS coefficient value",
        }
    ]


def product_status_rows(product_status: dict[str, Any]) -> list[dict[str, str]]:
    return [
        {
            "runner_id": "APR1098_0_owner_signature_stub",
            "prediction_rows": str(product_status.get("prediction_rows", "")),
            "bound_rows": str(product_status.get("bound_rows", "")),
            "valid_prediction_rows": str(product_status.get("valid_prediction_rows", "")),
            "valid_bound_rows": str(product_status.get("valid_bound_rows", "")),
            "comparison_rows": str(product_status.get("comparison_rows", "")),
            "claim_allowed": str(product_status.get("claim_allowed", "")).lower(),
            "expected_result": "reject missing owner signature or source-backed coefficient",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        }
    ]


def claim_gate_rows(product_status: dict[str, Any]) -> list[dict[str, str]]:
    return [
        {
            "gate_id": "CG1098_0_owner_signature",
            "claim_component": "ordinary-constant owner action signature",
            "gate_pass": "false",
            "claim_allowed": "false",
            "reason": "OCS1098_6_verdict=OWNER_ACTION_SIGNATURE_NOT_DERIVED",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "gate_id": "CG1098_1_source_prior",
            "claim_component": "source-backed coefficient prior",
            "gate_pass": "false",
            "claim_allowed": "false",
            "reason": "threshold exists but no external coefficient value/source exists",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "gate_id": "CG1098_2_product_runner",
            "claim_component": "constant coefficient runner",
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
            "decision_id": "DEC1098_0_signature",
            "decision": "ordinary-constant owner action signature is not derived",
            "because": "unique EM owner, no mass/binding vertices, clock/readout owner, source-weight exclusion, and radiative closure are not all signed",
            "next_action": "attack the unique EM kinetic owner first, because it is the explicit failed clause",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "decision_id": "DEC1098_1_finite_route",
            "decision": "source-backed coefficient priors remain required for any finite branch",
            "because": "thresholds constrain allowed values but do not provide MTS coefficient values",
            "next_action": "do not score WEP/clock/R10 until coefficients or theorem-zero exist",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "decision_id": "DEC1098_2_best_next",
            "decision": "target unique EM kinetic owner/no-extra-F2 next",
            "because": "alpha is the sharpest shared pressure channel across clocks, WEP, R10, and EM",
            "next_action": "1099-Y5-R10-unique-EM-kinetic-owner-no-extra-F2-theorem-or-alpha-coefficient-source-row.md",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
    ]


def next_target_rows() -> list[dict[str, str]]:
    return [
        {
            "next_id": "NEXT1098_0_1099",
            "next_target": "1099-Y5-R10-unique-EM-kinetic-owner-no-extra-F2-theorem-or-alpha-coefficient-source-row.md",
            "objective": "derive the unique EM kinetic owner/no-extra-F2 theorem that forces b_alpha=0, or stage an external source-backed alpha coefficient row against clock/WEP/R10 thresholds",
            "include": "T_Q owner; fixed charge lattice; unique Maxwell F2 norm; no f_X F^2 counterterm; readout/radiative closure; alpha coefficient thresholds",
            "exclude": "unit rescaling of alpha; clock-only screening; tau_WEP=1; unsourced alpha priors; WEP/local-GR claim; GitHub; formalization edits",
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
    signature_rows: list[dict[str, str]],
    vertex_rows: list[dict[str, str]],
    theorem_rows_: list[dict[str, str]],
    coefficient_rows: list[dict[str, str]],
    prediction_rows_: list[dict[str, str]],
    bound_rows_: list[dict[str, str]],
    product_status: dict[str, Any],
    claim_rows: list[dict[str, str]],
    next_rows: list[dict[str, str]],
) -> list[dict[str, str]]:
    checks: list[tuple[str, bool, str]] = []
    checks.append(("V1098_0_local_sources_exist", all(row["exists"] == "true" and row["needle_found"] == "true" for row in source_rows), "all cited source paths and needles are present"))
    checks.append(("V1098_1_owner_signature_not_derived", any(row["clause_id"] == "OCS1098_6_verdict" and row["current_status"] == "OWNER_ACTION_SIGNATURE_NOT_DERIVED" for row in signature_rows), "owner action signature verdict is explicit"))
    checks.append(("V1098_2_scalar_F2_legal", any(row["vertex_id"] == "FV1098_1_scalar_F2" and row["classification"] == "forbidden_required_but_currently_legal" for row in vertex_rows), "scalar F2 counterterm remains legal"))
    checks.append(("V1098_3_mass_binding_legal", any(row["vertex_id"] == "FV1098_4_binding_X" and row["current_status"] == "blocks_claim" for row in vertex_rows), "mass/binding vertices remain live"))
    checks.append(("V1098_4_theorem_not_promoted", any(row["theorem_id"] == "OCT1098_3_verdict" and row["status"] == "OWNER_THEOREM_NOT_PROMOTED" for row in theorem_rows_), "ordinary-constant owner theorem is not promoted"))
    checks.append(("V1098_5_coefficient_requirements_numeric", len(coefficient_rows) == 3 and all(parse_float(row["threshold_abs"]) is not None and float(row["threshold_abs"]) > 0 for row in coefficient_rows), "source-backed coefficient requirements carry positive thresholds"))
    checks.append(("V1098_6_prediction_missing_nonclaim", any("MISSING_OWNER_SIGNATURE" in row["product_value"] and row["valid_for_claim"] == "false" for row in prediction_rows_), "prediction row remains missing owner signature/source coefficient"))
    checks.append(("V1098_7_bound_threshold_positive", bool(bound_rows_) and parse_float(bound_rows_[0]["bound_value"]) is not None and float(bound_rows_[0]["bound_value"]) > 0, "coefficient threshold bound is positive numeric"))
    checks.append(("V1098_8_product_runner_refuses", product_status.get("valid_prediction_rows") == 0 and product_status.get("claim_allowed") is False, "generic product runner reports no valid prediction rows and claim false"))
    checks.append(("V1098_9_claim_gates_safe", claim_rows and all(row["claim_allowed"] == "false" for row in claim_rows), "all claim gates deny WEP/local claim"))
    checks.append(("V1098_10_next_target", any(row["next_target"].startswith("1099-Y5-R10-unique-EM-kinetic-owner") for row in next_rows), "1099 handoff written"))
    generated_paths = list(outputs.values()) + [DOC]
    checks.append(("V1098_11_generated_under_post_checkpoint", all(str(path.resolve()).startswith(str(ROOT.resolve())) for path in generated_paths), "all generated outputs are under post-checkpoint-work"))
    checks.append(("V1098_12_csv_parse", csv_outputs_parse([path for key, path in outputs.items() if key != "validation"]), "all 1098 CSV outputs parse cleanly"))
    checks.append(("V1098_13_formalization_untouched", count_formalization_modified_since_start() == 0, "formalization-workbench modified-file count remains zero"))
    checks.append(("V1098_SUMMARY", True, "ordinary-constant owner signature not derived; no-extra-F2 is the sharp next target; finite coefficients remain explicit"))
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
    signature_rows: list[dict[str, str]],
    vertex_rows: list[dict[str, str]],
    theorem_rows_: list[dict[str, str]],
    coefficient_rows: list[dict[str, str]],
    product_status_rows_: list[dict[str, str]],
    product_comparisons: list[dict[str, Any]],
    claim_rows: list[dict[str, str]],
    decisions: list[dict[str, str]],
    validation_rows: list[dict[str, str]],
    next_rows: list[dict[str, str]],
) -> None:
    text = "\n".join(
        [
            "# 1098-Y5-R10 ordinary-constant owner action signature or source-backed coefficient prior",
            "",
            "## Current verdict",
            "1098 turns constant-sector universality into a concrete parent-action signature. If the parent action signs one field domain, one EM kinetic owner, no hidden mass/binding/clock/source-weight vertices, and radiative/readout closure, then ordinary constant coefficients vanish by chain rule. The current corpus does not sign this. The explicit failure is useful: an independent scalar `f_X F^2` counterterm is still legal, and mass/binding/source-weight vertices are still not parent-forbidden. Therefore finite coefficient rows stay live, and the sharp next derivation target is the unique EM kinetic owner/no-extra-F2 theorem.",
            "",
            "## Source register",
            md_table(source_rows, ["source_id", "relative_path", "exists", "needle_found", "note"]),
            "## Ordinary-constant owner signature",
            md_table(signature_rows, ["clause_id", "signature_clause", "required_form", "current_status", "if_signed", "if_missing"]),
            "## Allowed/forbidden vertex audit",
            md_table(vertex_rows, ["vertex_id", "sector", "operator_or_slot", "classification", "coefficient", "current_status"]),
            "## Action-signature theorem",
            md_table(theorem_rows_, ["theorem_id", "claim_piece", "mathematical_statement", "status", "consequence"]),
            "## Source-backed coefficient requirements",
            md_table(coefficient_rows, ["requirement_id", "coefficient", "threshold_abs", "required_evidence", "observable_arenas", "current_status"]),
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
    signature_rows = owner_signature_rows()
    vertex_rows = forbidden_vertex_rows()
    theorem_rows_ = theorem_rows()
    coefficient_rows = coefficient_source_rows()
    prediction_rows_ = prediction_rows()
    bound_rows_ = bound_import_rows()
    next_rows = next_target_rows()

    outputs = {
        "source_register": OUT / "P8_Y5_R10_1098_SOURCE_REGISTER.csv",
        "signature": OUT / "P8_Y5_R10_1098_ORDINARY_CONSTANT_OWNER_SIGNATURE_ATTEMPT.csv",
        "vertices": OUT / "P8_Y5_R10_1098_FORBIDDEN_VERTEX_AUDIT.csv",
        "theorem": OUT / "P8_Y5_R10_1098_ACTION_SIGNATURE_THEOREM.csv",
        "coefficient_requirements": OUT / "P8_Y5_R10_1098_SOURCE_BACKED_COEFFICIENT_REQUIREMENTS.csv",
        "prediction": PREDICTION_TEMPLATE,
        "bound": BOUND_IMPORT,
        "product_status": OUT / "P8_Y5_R10_1098_PRODUCT_RUNNER_STATUS.csv",
        "product_comparison": OUT / "P8_Y5_R10_1098_PRODUCT_COMPARISON_ROWS.csv",
        "claim_gates": OUT / "P8_Y5_R10_1098_CLAIM_GATES.csv",
        "decisions": OUT / "P8_Y5_R10_1098_DECISION_LEDGER.csv",
        "next_target": OUT / "P8_Y5_R10_1098_NEXT_TARGET.csv",
        "validation": OUT / "P8_Y5_BRR545_1098_VALIDATION.csv",
    }

    write_csv(outputs["source_register"], source_rows)
    write_csv(outputs["signature"], signature_rows)
    write_csv(outputs["vertices"], vertex_rows)
    write_csv(outputs["theorem"], theorem_rows_)
    write_csv(outputs["coefficient_requirements"], coefficient_rows)
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
        signature_rows,
        vertex_rows,
        theorem_rows_,
        coefficient_rows,
        prediction_rows_,
        bound_rows_,
        product_status,
        claim_rows,
        next_rows,
    )
    write_csv(outputs["validation"], validation_rows)
    write_doc(
        source_rows,
        signature_rows,
        vertex_rows,
        theorem_rows_,
        coefficient_rows,
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

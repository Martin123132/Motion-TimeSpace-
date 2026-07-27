from __future__ import annotations

import csv
import importlib.util
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "source-intake" / "mts_residuals"
R10 = ROOT / "source-intake" / "r10"
MICROSCOPE = ROOT / "source-intake" / "microscope"
BRANCH_RESIDUALS = MICROSCOPE / "branch_locked_wep" / "residuals"
BRANCH_COEFF = MICROSCOPE / "branch_locked_wep" / "coefficients"
FORMALIZATION = ROOT.parent / "formalization-workbench"
BRANCH_ID = "MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428"
DOC = ROOT / "1507-Y5-R10-RAB-positive-nohair-charge-zero-or-source-backed-alpha-priors.md"
START_TS = datetime.now(timezone.utc).timestamp()

RUNNER_SCRIPT = ROOT / "scripts" / "R10_alpha_lambda_bound_prediction_runner.py"
RUNNER_OUT = ROOT / "runs" / "1507-R10-positive-nohair-alpha-prior-template-runner" / "results"
BOUND_TEMPLATE = OUT / "R10_alpha_lambda_bound_curve_1506_VISUAL_RUNNER_SHAPE_NONCLAIM.csv"

SOURCE_FILES = {
    "1506_validation": OUT / "P8_Y5_BRR545_1506_VALIDATION.csv",
    "1506_charge_audit": OUT / "P8_Y5_R10_1506_SOURCE_TEST_CHARGE_ZERO_AUDIT.csv",
    "1506_theorem": OUT / "P8_Y5_R10_1506_SOURCE_TEST_CHARGE_THEOREM_LEDGER.csv",
    "1506_alpha_template": OUT / "R10_alpha_lambda_curve_MTS_1506_SOURCE_TEST_CHARGE_TEMPLATE_NONCLAIM.csv",
    "energy_identity": OUT / "P8_EXTRA_SECTOR_SILENCE_ENERGY_IDENTITY.csv",
    "hamiltonian_silence": ROOT / "runs" / "20260605-141500-Y5-extra-sector-Hamiltonian-charge-silence-or-channel-fill" / "results" / "P8_Y5_HAMILTONIAN_EXTRA_CHARGE_SILENCE_ATTEMPT.csv",
    "hamiltonian_channel_map": ROOT / "runs" / "20260605-141500-Y5-extra-sector-Hamiltonian-charge-silence-or-channel-fill" / "results" / "P8_Y5_HAMILTONIAN_EXTRA_CHARGE_CHANNEL_MAP.csv",
    "positive_operator_attempt": ROOT / "runs" / "20260605-142500-Y5-Cextra-bulk-memory-range-positive-operator-zero-or-Yukawa-bound-fill" / "results" / "P8_Y5_CEXTRA_BULK_MEMORY_RANGE_POSITIVE_OPERATOR_ATTEMPT.csv",
    "force_law_map": ROOT / "runs" / "20260605-142500-Y5-Cextra-bulk-memory-range-positive-operator-zero-or-Yukawa-bound-fill" / "results" / "P8_Y5_CEXTRA_BULK_MEMORY_RANGE_FORCE_LAW_MAP.csv",
    "r10_curve_contract": ROOT / "runs" / "20260605-142500-Y5-Cextra-bulk-memory-range-positive-operator-zero-or-Yukawa-bound-fill" / "results" / "P8_Y5_CEXTRA_BULK_MEMORY_RANGE_R10_CURVE_CONTRACT.csv",
    "decision_557": ROOT / "runs" / "20260605-142500-Y5-Cextra-bulk-memory-range-positive-operator-zero-or-Yukawa-bound-fill" / "results" / "P8_Y5_BRR545_557_DECISION.csv",
    "runner_script": RUNNER_SCRIPT,
    "bound_template": BOUND_TEMPLATE,
}

CURVE_TARGET = R10 / "derived" / "R10_alpha_lambda_bound_curve_DIGITIZED.csv"
KERNEL_TARGET = R10 / "derived" / "R10_delta_w_kernel_lambda.csv"
C_PARENT_IMPORT = BRANCH_COEFF / "C_parent_WEP_slot_import.csv"

NOHAIR_AUDIT = OUT / "P8_Y5_R10_1507_POSITIVE_NOHAIR_CHARGE_ZERO_AUDIT.csv"
NOHAIR_THEOREM = OUT / "P8_Y5_R10_1507_NOHAIR_THEOREM_LEDGER.csv"
CERT_REQUIREMENTS = OUT / "P8_Y5_R10_1507_THEOREM_ZERO_CERTIFICATE_REQUIREMENTS.csv"
ALPHA_PRIOR_REQUIREMENTS = OUT / "P8_Y5_R10_1507_SOURCE_BACKED_ALPHA_PRIOR_REQUIREMENTS.csv"
ALPHA_PRIOR_TEMPLATE = OUT / "R10_alpha_lambda_curve_MTS_1507_ALPHA_PRIOR_TEMPLATE_NONCLAIM.csv"
RUNNER_LEDGER = OUT / "P8_Y5_R10_1507_RUNNER_LEDGER.csv"
TARGET_BLOCKERS = OUT / "P8_Y5_R10_1507_TARGET_PROMOTION_BLOCKERS.csv"
SCORE_READINESS = OUT / "P8_Y5_R10_1507_DELTA_W_SCORE_READINESS.csv"
C_PARENT_REFUSAL = OUT / "P8_Y5_R10_1507_C_PARENT_IMPORT_REFUSAL.csv"
LOCAL_STATUS = OUT / "P8_Y5_R10_1507_LOCAL_GR_NEWTON_STATUS.csv"
REJECTION_LEDGER = OUT / "P8_Y5_R10_1507_REJECTION_LEDGER.csv"
DECISION_LEDGER = OUT / "P8_Y5_R10_1507_DECISION_LEDGER.csv"
NEXT_TARGET = OUT / "P8_Y5_R10_1507_NEXT_TARGET.csv"
VALIDATION = OUT / "P8_Y5_BRR545_1507_VALIDATION.csv"

QUARANTINE = MICROSCOPE / "quarantine" / "1507"
QUAR_AUDIT = QUARANTINE / "POSITIVE_NOHAIR_CHARGE_ZERO_AUDIT_NONCLAIM.csv"
QUAR_THEOREM = QUARANTINE / "NOHAIR_THEOREM_LEDGER_NONCLAIM.csv"
QUAR_CERT = QUARANTINE / "THEOREM_ZERO_CERTIFICATE_REQUIREMENTS_NONCLAIM.csv"
QUAR_ALPHA = QUARANTINE / "ALPHA_PRIOR_TEMPLATE_NONCLAIM.csv"
BRANCH_AUDIT = BRANCH_RESIDUALS / "r10_positive_nohair_charge_zero_audit_nonclaim_1507.csv"
BRANCH_THEOREM = BRANCH_RESIDUALS / "r10_nohair_theorem_ledger_nonclaim_1507.csv"
BRANCH_CERT = BRANCH_RESIDUALS / "r10_theorem_zero_certificate_requirements_nonclaim_1507.csv"
BRANCH_ALPHA = BRANCH_RESIDUALS / "r10_alpha_prior_template_nonclaim_1507.csv"

MTS_REQUIRED_COLUMNS = [
    "model_id",
    "branch_id",
    "curve_id",
    "lambda_value",
    "lambda_units",
    "alpha_predicted",
    "alpha_bound",
    "alpha_bound_source",
    "force_law_form",
    "derivation_status",
    "formula_reference",
    "source_file",
    "assumptions",
    "valid_for_claim",
    "notes",
]


def flags() -> dict[str, bool]:
    return {"score_ready": False, "valid_prediction_row": False, "valid_for_claim": False, "claim_allowed": False}


def rel(path: Path) -> str:
    try:
        return str(path.relative_to(ROOT)).replace("\\", "/")
    except ValueError:
        return str(path)


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def parse_csv(path: Path) -> bool:
    read_csv(path)
    return True


def nohair_audit_rows() -> list[dict[str, Any]]:
    rows = [
        ("NH1507_0_energy_identity", "positive operator identity", "int_A <X,L_X X>=norm_positive[X]+boundary_flux", "CONDITIONAL_REFERENCE", "sufficient only after field-specific L_X and boundary/source premises are parent-owned"),
        ("NH1507_1_operator_sign", "L_X positive/self-adjoint", "Z_X>0 and M_X^2>0 or positive constrained operator", "MISSING_FIELD_SPECIFIC_PARENT_OPERATOR", "mass gap/sign not owned for the R10-active field"),
        ("NH1507_2_source_silence", "no local source", "J_X=0 or Q_X_source=0 in compact annulus", "MISSING_SOURCE_CHARGE_ZERO", "source charge could still generate a Yukawa tail"),
        ("NH1507_3_test_silence", "no test charge", "q_test_X=0 for R10 apparatus/readout", "MISSING_TEST_CHARGE_ZERO", "test body could still respond even if source sector is subtle"),
        ("NH1507_4_boundary_silence", "zero boundary/history injection", "boundary_flux=0 and no memory-history tail", "MISSING_BOUNDARY_MEMORY_ZERO", "positive operator identity has a boundary side term"),
        ("NH1507_5_hamiltonian_projection", "zero mass-charge projection", "PiM_H Q_X=0", "MISSING_HAMILTONIAN_PROJECTION_ZERO", "source-normalized local GR/R10 pass still blocked"),
        ("NH1507_6_mass_gap_guardrail", "mass gap alone", "M_X^2>0 => lambda_X finite", "INVALID_SHORTCUT", "finite lambda is not alpha=0; coupling normalization still determines force strength"),
        ("NH1507_7_verdict", "positive no-hair route", "operator+source+test+boundary+projection zero certificate", "NOT_PARENT_DERIVED", "emit certificate requirements and nonclaim alpha priors"),
    ]
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "audit_id": audit_id,
            "object": obj,
            "mathematical_form": form,
            "current_status": status,
            "effect": effect,
            **flags(),
        }
        for audit_id, obj, form, status, effect in rows
    ]


def theorem_rows() -> list[dict[str, Any]]:
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "theorem_id": "THM1507_0_positive_nohair_zero",
            "statement": "If L_X is positive/self-adjoint on the compact exterior annulus, J_X=0, q_test_X=0, boundary/history injection is zero, and PiM_H projection is zero, then X has no R10-active local hair and alpha_X(lambda)=0.",
            "proof_status": "EXACT_CONDITIONAL_THEOREM",
            "proof_sketch": "Integrate the source-free field equation against X. Positivity forces X=0 modulo pure gauge/topological constants when boundary flux is zero; zero test/source/projection clauses prevent hidden force readout.",
            "current_claim_status": "CONDITIONAL_NOT_PARENT_SIGNED",
            **flags(),
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "theorem_id": "THM1507_1_mass_gap_not_enough",
            "statement": "A positive mass gap or finite range does not by itself prove alpha_X(lambda)=0; the source/test coupling product and measured-G normalization set the fifth-force amplitude.",
            "proof_status": "COUNTERMODEL_ACTIVE",
            "proof_sketch": "A massive field with nonzero source and test charges produces a Yukawa force. The mass fixes lambda, not the amplitude.",
            "current_claim_status": "BLOCKS_MASS_GAP_SHORTCUT",
            **flags(),
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "theorem_id": "THM1507_2_current_branch_verdict",
            "statement": "The current corpus has the positive no-hair theorem shape, but not the field-specific signed operator, zero source/test charge, boundary silence, Hamiltonian projection, or source-backed alpha priors.",
            "proof_status": "DERIVED_AS_GATE_LOGIC",
            "proof_sketch": "The cited 556/557 ledgers explicitly retain those inputs as missing and forbid cancellation or mass-gap shortcuts.",
            "current_claim_status": "KEEP_R10_NONCLAIM_ALPHA_PRIOR_TEMPLATE",
            **flags(),
        },
    ]


def certificate_rows() -> list[dict[str, Any]]:
    rows = [
        ("CERT1507_0_field", "R10-active X_a field", "declared parent field/component", "MISSING_R10_FIELD_MAP"),
        ("CERT1507_1_operator", "L_X", "positive self-adjoint local operator with units/sign", "MISSING"),
        ("CERT1507_2_source", "J_X or Q_X_source", "derived zero in compact local annulus", "MISSING"),
        ("CERT1507_3_test", "q_test_X", "derived zero for R10 material/readout", "MISSING"),
        ("CERT1507_4_boundary", "boundary_flux", "zero boundary/history injection", "MISSING"),
        ("CERT1507_5_projection", "PiM_H Q_X", "zero Hamiltonian mass-charge projection", "MISSING"),
        ("CERT1507_6_gauge", "pure gauge/topological constants", "shown not to affect R10 force/readout", "MISSING"),
        ("CERT1507_7_acceptance", "alpha_X(lambda)=0", "allowed only after CERT1507_0 through CERT1507_6 close", "BLOCKED"),
    ]
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "certificate_id": certificate_id,
            "symbol": symbol,
            "requirement": requirement,
            "current_status": status,
            **flags(),
        }
        for certificate_id, symbol, requirement, status in rows
    ]


def alpha_prior_requirement_rows() -> list[dict[str, Any]]:
    rows = [
        ("APR1507_0_lambda", "lambda_X", "positive numeric range with units and source path", "MISSING"),
        ("APR1507_1_alpha", "alpha_predicted(lambda)", "numeric or DERIVED_ZERO value from source/test/normalization product", "MISSING"),
        ("APR1507_2_source", "Q_X_source", "source charge or zero proof", "MISSING"),
        ("APR1507_3_test", "q_test_X", "test charge or zero proof", "MISSING"),
        ("APR1507_4_normalization", "G_measured/M_source/m_test", "same-frame source normalization", "MISSING"),
        ("APR1507_5_tau", "tau_R10(lambda)", "finite-source response", "MISSING"),
        ("APR1507_6_bound", "alpha_bound(lambda)", "reviewed source-backed bound curve", "VISUAL_NONCLAIM_ONLY"),
        ("APR1507_7_claim", "valid_for_claim", "true only after every coefficient is source-backed or derived zero", "FALSE"),
    ]
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "requirement_id": requirement_id,
            "symbol": symbol,
            "requirement": requirement,
            "current_status": status,
            **flags(),
        }
        for requirement_id, symbol, requirement, status in rows
    ]


def alpha_prior_rows() -> list[dict[str, Any]]:
    anchors = [
        ("3.86000000e-05", "1.00000000e+00", "mass_gap_guardrail_anchor"),
        ("5.60000000e-05", "1.00000000e-01", "source_charge_prior_anchor"),
        ("1.00000000e-04", "2.00000000e-02", "boundary_projection_prior_anchor"),
    ]
    return [
        {
            "model_id": "MTS_1507_POSITIVE_NOHAIR_OR_ALPHA_PRIOR_NONCLAIM",
            "branch_id": BRANCH_ID,
            "curve_id": f"MTS_1507_POSITIVE_NOHAIR_PRIOR_{label}",
            "lambda_value": lambda_value,
            "lambda_units": "m",
            "alpha_predicted": "MISSING_POSITIVE_NOHAIR_CERTIFICATE_OR_SOURCE_BACKED_ALPHA",
            "alpha_bound": alpha_bound,
            "alpha_bound_source": rel(BOUND_TEMPLATE),
            "force_law_form": "alpha_X(lambda)=0 if nohair certificate closes; otherwise source-backed numeric prior required",
            "derivation_status": "template_invalid_missing_nohair_certificate_and_alpha_prior",
            "formula_reference": "positive nohair theorem OR alpha_X(lambda) from Q_X q_test tau_R10 /(G_N M m)",
            "source_file": "MISSING_SOURCE_FILE",
            "assumptions": "nonclaim row; mass gap alone cannot set alpha=0; replace MISSING markers before scoring",
            "valid_for_claim": "false",
            "notes": f"1507 nonclaim prior row for {label}",
        }
        for lambda_value, alpha_bound, label in anchors
    ]


def run_runner() -> dict[str, Any]:
    spec = importlib.util.spec_from_file_location("r10_runner_1507", RUNNER_SCRIPT)
    if spec is None or spec.loader is None:
        raise RuntimeError("could not load R10 runner")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    result = module.run_runner(ALPHA_PRIOR_TEMPLATE, BOUND_TEMPLATE, RUNNER_OUT)
    return result["status"]


def runner_rows(status: dict[str, Any]) -> list[dict[str, Any]]:
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "runner_id": "RUN1507_0_alpha_prior_template",
            "mts_curve": status.get("mts_curve", ""),
            "bound_curve": status.get("bound_curve", ""),
            "output_dir": status.get("output_dir", ""),
            "valid_mts_rows": status.get("valid_mts_rows", ""),
            "valid_bound_rows": status.get("valid_bound_rows", ""),
            "R10_pass_for_claim": status.get("R10_pass_for_claim", False),
            "claim_allowed": status.get("claim_allowed", False),
            "interpretation": "expected block: nohair certificate and source-backed alpha priors are missing",
            **flags(),
        }
    ]


def blocker_rows() -> list[dict[str, Any]]:
    blockers = [
        ("BLK1507_0_operator", "MISSING_FIELD_SPECIFIC_POSITIVE_OPERATOR", "no parent-signed L_X/Z_X/M_X^2 for the R10-active field", "parent_action"),
        ("BLK1507_1_source", "MISSING_SOURCE_CHARGE_ZERO_OR_VALUE", "Q_X_source remains unowned", "parent_action"),
        ("BLK1507_2_test", "MISSING_TEST_CHARGE_ZERO_OR_VALUE", "q_test_X remains unowned", "parent_action"),
        ("BLK1507_3_boundary", "MISSING_BOUNDARY_HISTORY_ZERO", "boundary/history injection remains open", "parent_action"),
        ("BLK1507_4_projection", "MISSING_HAMILTONIAN_PROJECTION_ZERO", "PiM_H projection remains open", "parent_action"),
        ("BLK1507_5_alpha_prior", "MISSING_SOURCE_BACKED_ALPHA_PRIOR", "no finite alpha prior has source-backed coefficients", rel(ALPHA_PRIOR_TEMPLATE)),
        ("BLK1507_6_kernel", "MISSING_R10_KERNEL", "R10 finite-source tau/kernel remains absent", rel(KERNEL_TARGET)),
        ("BLK1507_7_curve", "MISSING_REVIEWED_R10_CURVE", "live reviewed R10 curve remains absent", rel(CURVE_TARGET)),
        ("BLK1507_8_import", "MISSING_C_PARENT_IMPORT", "no live coefficient import exists", rel(C_PARENT_IMPORT)),
    ]
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "blocker_id": blocker_id,
            "blocking_marker": marker,
            "reason": reason,
            "target_path": target,
            **flags(),
        }
        for blocker_id, marker, reason, target in blockers
    ]


def simple_rows_from_blockers(blockers: list[dict[str, Any]], prefix: str) -> list[dict[str, Any]]:
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            f"{prefix}_id": f"{prefix.upper()}1507_{index}",
            "object": row["blocking_marker"],
            "path": row["target_path"],
            "status": "BLOCKED",
            "effect": row["reason"],
            **flags(),
        }
        for index, row in enumerate(blockers)
    ]


def c_parent_refusal_rows() -> list[dict[str, Any]]:
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "refusal_id": "CP1507_0_no_import",
            "path": rel(C_PARENT_IMPORT),
            "path_exists": C_PARENT_IMPORT.exists(),
            "imported_now": False,
            "reason": "1507 has no nohair certificate or source-backed alpha coefficient pack",
            "claim_effect": "R10/local-GR claim remains blocked",
            **flags(),
        }
    ]


def decision_rows() -> list[dict[str, Any]]:
    decisions = [
        ("DEC1507_0_nohair_route", "keep positive no-hair as theorem-zero target", "it is the cleanest local-GR/R10 route if parent-owned"),
        ("DEC1507_1_mass_gap_guardrail", "reject mass-gap-only R10 pass", "lambda without alpha/source/test normalization is not a bound comparison"),
        ("DEC1507_2_next", "derive the field-specific operator/source certificate or acquire real coefficient priors", "that is the next fork"),
    ]
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "decision_id": decision_id,
            "decision": decision,
            "rationale": rationale,
            **flags(),
        }
        for decision_id, decision, rationale in decisions
    ]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "next_id": "NEXT1507_0_1508",
            "next_target": "1508-Y5-R10-RAB-field-specific-LX-operator-certificate-or-alpha-prior-source-pack.md",
            "script": "scripts/Y5_R10_RAB_field_specific_LX_operator_certificate_or_alpha_prior_source_pack.py",
            "objective": "try to instantiate a field-specific positive operator certificate for X_a; if not, build a coefficient-source acquisition pack for finite alpha priors",
            **flags(),
        }
    ]


def generated_flags_false(paths: list[Path]) -> bool:
    for path in paths:
        for row in read_csv(path):
            for column in ["score_ready", "valid_prediction_row", "valid_for_claim", "claim_allowed"]:
                value = row.get(column)
                if value not in (None, "", "False", "false", False):
                    return False
    return True


def copy_outputs() -> None:
    QUARANTINE.mkdir(parents=True, exist_ok=True)
    BRANCH_RESIDUALS.mkdir(parents=True, exist_ok=True)
    for src, dst in [
        (NOHAIR_AUDIT, QUAR_AUDIT),
        (NOHAIR_THEOREM, QUAR_THEOREM),
        (CERT_REQUIREMENTS, QUAR_CERT),
        (ALPHA_PRIOR_TEMPLATE, QUAR_ALPHA),
        (NOHAIR_AUDIT, BRANCH_AUDIT),
        (NOHAIR_THEOREM, BRANCH_THEOREM),
        (CERT_REQUIREMENTS, BRANCH_CERT),
        (ALPHA_PRIOR_TEMPLATE, BRANCH_ALPHA),
    ]:
        shutil.copyfile(src, dst)


def validation_rows(generated_csvs: list[Path], status: dict[str, Any], theorem: list[dict[str, Any]], audit: list[dict[str, Any]]) -> list[dict[str, Any]]:
    source_paths_exist = all(path.exists() for path in SOURCE_FILES.values())
    exact_nohair = any(row["theorem_id"] == "THM1507_0_positive_nohair_zero" and row["proof_status"] == "EXACT_CONDITIONAL_THEOREM" for row in theorem)
    mass_gap_guardrail = any(row["theorem_id"] == "THM1507_1_mass_gap_not_enough" and row["proof_status"] == "COUNTERMODEL_ACTIVE" for row in theorem)
    not_parent_derived = any(row["audit_id"] == "NH1507_7_verdict" and row["current_status"] == "NOT_PARENT_DERIVED" for row in audit)
    alpha_schema_ok = set(read_csv(ALPHA_PRIOR_TEMPLATE)[0].keys()) >= set(MTS_REQUIRED_COLUMNS)
    runner_blocked = status.get("R10_pass_for_claim") is False and status.get("claim_allowed") is False
    live_targets_absent = not CURVE_TARGET.exists() and not KERNEL_TARGET.exists()
    c_parent_refused = read_csv(C_PARENT_REFUSAL)[0]["imported_now"] == "False"
    csv_parse_ok = all(parse_csv(path) for path in generated_csvs)
    flags_false = generated_flags_false(generated_csvs)
    branch_copies = all(path.exists() for path in [QUAR_AUDIT, QUAR_THEOREM, QUAR_CERT, QUAR_ALPHA, BRANCH_AUDIT, BRANCH_THEOREM, BRANCH_CERT, BRANCH_ALPHA])
    pycache = ROOT / "scripts" / "__pycache__"
    if pycache.exists():
        shutil.rmtree(pycache)
    pycache_absent = not pycache.exists()
    formalization_modified = 0
    if FORMALIZATION.exists():
        formalization_modified = sum(1 for path in FORMALIZATION.rglob("*") if path.is_file() and path.stat().st_mtime > START_TS)
    checks = [
        ("VAL1507_0_local_sources", source_paths_exist, "all cited nohair/R10 source paths exist"),
        ("VAL1507_1_exact_nohair", exact_nohair, "conditional positive nohair theorem recorded"),
        ("VAL1507_2_mass_gap_guardrail", mass_gap_guardrail, "mass-gap-only shortcut rejected"),
        ("VAL1507_3_not_parent_derived", not_parent_derived, "current branch does not claim nohair certificate"),
        ("VAL1507_4_alpha_schema", alpha_schema_ok, "alpha prior template has runner-required columns"),
        ("VAL1507_5_runner_blocked", runner_blocked, "runner blocks nonclaim alpha-prior template"),
        ("VAL1507_6_live_targets_absent", live_targets_absent, "live R10 curve/kernel targets remain absent"),
        ("VAL1507_7_Cparent_refused", c_parent_refused, "C_parent import was not performed"),
        ("VAL1507_8_csv_parse", csv_parse_ok, "all generated 1507 CSVs parse cleanly"),
        ("VAL1507_9_branch_copies", branch_copies, "branch/quarantine nonclaim copies written"),
        ("VAL1507_10_pycache_absent", pycache_absent, "scripts __pycache__ absent after run"),
        ("VAL1507_11_formalization_untouched", formalization_modified == 0, f"formalization modified-file count since start={formalization_modified}"),
        ("VAL1507_12_claim_flags_false", flags_false, "all generated prediction/claim flags remain false"),
    ]
    overall = all(result for _, result, _ in checks)
    rows = [
        {"same_parent_branch_id": BRANCH_ID, "check_id": check_id, "result": "PASS" if result else "FAIL", "detail": detail}
        for check_id, result, detail in checks
    ]
    rows.append(
        {
            "same_parent_branch_id": BRANCH_ID,
            "check_id": "VAL1507_13_overall",
            "result": "PASS" if overall else "FAIL",
            "detail": "1507 kept positive nohair as a conditional theorem and blocked mass-gap/alpha-prior overclaim"
            if overall
            else "1507 validation failed; inspect failed rows before continuing",
        }
    )
    return rows


def md_table(rows: list[dict[str, Any]], columns: list[str]) -> str:
    output = ["| " + " | ".join(columns) + " |", "| " + " | ".join("---" for _ in columns) + " |"]
    for row in rows:
        output.append("| " + " | ".join(str(row.get(column, "")).replace("\n", " ") for column in columns) + " |")
    return "\n".join(output)


def write_doc(
    audit: list[dict[str, Any]],
    theorem: list[dict[str, Any]],
    certs: list[dict[str, Any]],
    priors: list[dict[str, Any]],
    runner: list[dict[str, Any]],
    validation: list[dict[str, Any]],
    next_rows: list[dict[str, Any]],
) -> None:
    DOC.write_text(
        "\n".join(
            [
                "# 1507 - Positive Nohair Charge Zero or Source-Backed Alpha Priors",
                "",
                "## Verdict",
                "- Positive nohair is a real theorem shape: a signed positive operator with zero source, test charge, boundary/history flux, and Hamiltonian projection would give alpha_X(lambda)=0.",
                "- The current branch does not own the field-specific operator or charge-zero certificate, and mass gap alone is explicitly rejected.",
                "- A nonclaim alpha-prior template was emitted and the runner correctly blocks it until the certificate or source-backed coefficients exist.",
                "",
                "## Positive Nohair Audit",
                md_table(audit, ["audit_id", "object", "current_status", "effect"]),
                "",
                "## Nohair Theorem Ledger",
                md_table(theorem, ["theorem_id", "proof_status", "current_claim_status"]),
                "",
                "## Certificate Requirements",
                md_table(certs, ["certificate_id", "symbol", "requirement", "current_status"]),
                "",
                "## Alpha Prior Requirements",
                md_table(priors, ["requirement_id", "symbol", "requirement", "current_status"]),
                "",
                "## Runner Ledger",
                md_table(runner, ["runner_id", "valid_mts_rows", "valid_bound_rows", "R10_pass_for_claim", "interpretation"]),
                "",
                "## Validation",
                md_table(validation, ["check_id", "result", "detail"]),
                "",
                "## Next Target",
                md_table(next_rows, ["next_id", "next_target", "script", "objective"]),
                "",
            ]
        ),
        encoding="utf-8",
    )


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    audit = nohair_audit_rows()
    theorem = theorem_rows()
    certs = certificate_rows()
    prior_requirements = alpha_prior_requirement_rows()
    alpha_template = alpha_prior_rows()
    blockers = blocker_rows()
    readiness = simple_rows_from_blockers(blockers, "ready")
    c_parent = c_parent_refusal_rows()
    local_rows = [
        {
            "same_parent_branch_id": BRANCH_ID,
            "local_status_id": "LRS1507_0",
            "object": "R10 positive nohair / alpha-prior branch",
            "status": "FIELD_SPECIFIC_NOHAIR_CERT_OR_ALPHA_PRIOR_REQUIRED",
            "effect": "no local-GR/Newton/R10 claim",
            **flags(),
        }
    ]
    rejections = simple_rows_from_blockers(blockers, "rejection")
    decisions = decision_rows()
    next_rows = next_target_rows()

    write_csv(NOHAIR_AUDIT, audit)
    write_csv(NOHAIR_THEOREM, theorem)
    write_csv(CERT_REQUIREMENTS, certs)
    write_csv(ALPHA_PRIOR_REQUIREMENTS, prior_requirements)
    write_csv(ALPHA_PRIOR_TEMPLATE, alpha_template)
    write_csv(TARGET_BLOCKERS, blockers)
    write_csv(SCORE_READINESS, readiness)
    write_csv(C_PARENT_REFUSAL, c_parent)
    write_csv(LOCAL_STATUS, local_rows)
    write_csv(REJECTION_LEDGER, rejections)
    write_csv(DECISION_LEDGER, decisions)
    write_csv(NEXT_TARGET, next_rows)
    status = run_runner()
    runner = runner_rows(status)
    write_csv(RUNNER_LEDGER, runner)
    copy_outputs()

    generated_csvs = [
        NOHAIR_AUDIT,
        NOHAIR_THEOREM,
        CERT_REQUIREMENTS,
        ALPHA_PRIOR_REQUIREMENTS,
        ALPHA_PRIOR_TEMPLATE,
        RUNNER_LEDGER,
        TARGET_BLOCKERS,
        SCORE_READINESS,
        C_PARENT_REFUSAL,
        LOCAL_STATUS,
        REJECTION_LEDGER,
        DECISION_LEDGER,
        NEXT_TARGET,
    ]
    validation = validation_rows(generated_csvs, status, theorem, audit)
    write_csv(VALIDATION, validation)
    write_doc(audit, theorem, certs, prior_requirements, runner, validation, next_rows)
    pycache = ROOT / "scripts" / "__pycache__"
    if pycache.exists():
        shutil.rmtree(pycache)


if __name__ == "__main__":
    main()

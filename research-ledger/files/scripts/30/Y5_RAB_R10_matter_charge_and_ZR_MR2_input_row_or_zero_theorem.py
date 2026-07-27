from __future__ import annotations

import csv
import shutil
import subprocess
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "source-intake" / "mts_residuals"
RAB = ROOT / "source-intake" / "rab-sector"
RAB_RAW = RAB / "raw"
RAB_ACCEPTED = RAB / "accepted"
MICROSCOPE = ROOT / "source-intake" / "microscope"
BRANCH_RESIDUALS = MICROSCOPE / "branch_locked_wep" / "residuals"
QUARANTINE = MICROSCOPE / "quarantine" / "1574"
BRANCH_ID = "MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428"
DOC = ROOT / "1574-Y5-RAB-R10-matter-charge-and-ZR-MR2-input-row-or-zero-theorem.md"

SOURCE_FILES = {
    "1573_doc": ROOT / "1573-Y5-RAB-internal-tauR10-source-kernel-or-manual-curve-acceptance.md",
    "1573_validation": OUT / "P8_Y5_BRR545_1573_VALIDATION.csv",
    "1573_kernel": OUT / "P8_Y5_PARENT_QLOC_1573_TAU_R10_KERNEL_DERIVATION_CONTRACT.csv",
    "1573_required": OUT / "P8_Y5_PARENT_QLOC_1573_TAU_R10_REQUIRED_INPUTS.csv",
    "1036_beta": OUT / "P8_Y5_R10_1036_BETA_SOURCE_TEST_DERIVATION.csv",
    "1044_pullback": OUT / "P8_Y5_R10_1044_MATTER_PULLBACK_DERIVATION.csv",
    "1044_premises": OUT / "P8_Y5_R10_1044_MATTER_PULLBACK_PREMISE_GATE.csv",
    "1485_double_zero": OUT / "P8_Y5_R10_1485_UNIVERSAL_MATTER_DOUBLE_ZERO_THEOREM_ATTEMPT.csv",
    "1519_coframe_tau": OUT / "P8_Y5_PARENT_FRAME_1519_COFRAME_TAU_LOCK_AUDIT.csv",
}

NEEDLES = {
    "1573_doc": ["NEXT_1574_R10_MATTER_CHARGE_AND_ZR_MR2_INPUT_ROW_OR_ZERO_THEOREM", "beta_S^R beta_T^R"],
    "1573_validation": ["VAL1573_OVERALL", "PASS"],
    "1573_kernel": ["KDER1573_4_alpha_match", "FORMAL_TAU_KERNEL_LAW_DERIVED_CONDITIONAL"],
    "1573_required": ["REQ1573_2_beta_source", "MISSING_SOURCE_CHARGE", "REQ1573_3_beta_test"],
    "1036_beta": ["BETA1036_2_R10_alpha_match", "CONDITIONAL_NORMALIZATION_SPLIT"],
    "1044_pullback": ["MPD1044_7_exact_theorem_if_signed", "EXACT_CONDITIONAL_THEOREM"],
    "1044_premises": ["MPG1044_0_parent_matter_functor", "NOT_PARENT_SIGNED"],
    "1485_double_zero": ["DZ1485_0_exact_neighbourhood_theorem", "EXACT_CONDITIONAL_THEOREM"],
    "1519_coframe_tau": ["OCF1519_3_matter_constants", "NOT_PARENT_SIGNED"],
}

SOURCE_REGISTER = OUT / "P8_Y5_PARENT_QLOC_1574_SOURCE_REGISTER.csv"
RAB_MATTER_THEOREM = OUT / "P8_Y5_PARENT_QLOC_1574_RAB_MATTER_CHARGE_ZERO_THEOREM_ATTEMPT.csv"
PREMISE_MATRIX = OUT / "P8_Y5_PARENT_QLOC_1574_RAB_MATTER_DESCENT_PREMISE_MATRIX.csv"
FINITE_INPUT_ROWS = OUT / "P8_Y5_PARENT_QLOC_1574_RAB_FINITE_INPUT_ROWS_NONCLAIM.csv"
ALPHA_TEMPLATE = OUT / "P8_Y5_PARENT_QLOC_1574_R10_ALPHA_TEMPLATE_NONCLAIM.csv"
RUNNER = OUT / "P8_Y5_PARENT_QLOC_1574_RUNNER_NONCLAIM.csv"
CLAIM_GATE = OUT / "P8_Y5_PARENT_QLOC_1574_CLAIM_GATE.csv"
DECISION = OUT / "P8_Y5_PARENT_QLOC_1574_DECISION.csv"
NEXT_TARGET = OUT / "P8_Y5_PARENT_QLOC_1574_NEXT_TARGET.csv"
VALIDATION = OUT / "P8_Y5_BRR545_1574_VALIDATION.csv"

COPY_TARGETS = {
    RAB_MATTER_THEOREM: [
        QUARANTINE / "RAB_MATTER_CHARGE_ZERO_THEOREM_ATTEMPT_NONCLAIM.csv",
        BRANCH_RESIDUALS / "RAB_matter_charge_zero_theorem_attempt_nonclaim_1574.csv",
    ],
    PREMISE_MATRIX: [
        QUARANTINE / "RAB_MATTER_DESCENT_PREMISE_MATRIX_NONCLAIM.csv",
        BRANCH_RESIDUALS / "RAB_matter_descent_premise_matrix_nonclaim_1574.csv",
    ],
    FINITE_INPUT_ROWS: [
        QUARANTINE / "RAB_FINITE_INPUT_ROWS_NONCLAIM.csv",
        BRANCH_RESIDUALS / "RAB_finite_input_rows_nonclaim_1574.csv",
    ],
    ALPHA_TEMPLATE: [
        QUARANTINE / "R10_ALPHA_TEMPLATE_NONCLAIM.csv",
        BRANCH_RESIDUALS / "R10_alpha_template_nonclaim_1574.csv",
    ],
    DECISION: [
        QUARANTINE / "DECISION_NONCLAIM.csv",
        BRANCH_RESIDUALS / "RAB_matter_charge_decision_nonclaim_1574.csv",
    ],
}


def flags() -> dict[str, bool]:
    return {
        "parent_signed": False,
        "numeric_value_present": False,
        "source_backed": False,
        "score_ready": False,
        "valid_prediction_row": False,
        "valid_for_claim": False,
        "claim_allowed": False,
    }


def rel(path: Path) -> str:
    try:
        return str(path.relative_to(ROOT)).replace("\\", "/")
    except ValueError:
        return str(path)


def file_contains(path: Path, needles: list[str]) -> bool:
    if not path.exists():
        return False
    text = path.read_text(encoding="utf-8", errors="ignore")
    return all(needle in text for needle in needles)


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        raise ValueError(f"no rows for {path}")
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def generated_flags_false(paths: list[Path]) -> bool:
    false_values = {"", "false", "0", "no", "none", "null"}
    claim_keys = [
        "parent_signed",
        "numeric_value_present",
        "source_backed",
        "score_ready",
        "valid_prediction_row",
        "valid_for_claim",
        "claim_allowed",
        "accepted_for_scoring",
        "passes_for_claim",
    ]
    for path in paths:
        for row in read_csv(path):
            for key in claim_keys:
                if key in row and str(row[key]).strip().lower() not in false_values:
                    return False
    return True


def source_register_rows() -> list[dict[str, Any]]:
    rows = []
    for index, (key, path) in enumerate(SOURCE_FILES.items()):
        rows.append(
            {
                "same_parent_branch_id": BRANCH_ID,
                "source_id": f"SRC1574_{index}_{key}",
                "source_path": rel(path),
                "exists": path.exists(),
                "needle_found": file_contains(path, NEEDLES[key]),
                "needles": "; ".join(NEEDLES[key]),
                "purpose": "R_AB matter-charge zero theorem or finite input row staging",
                **flags(),
            }
        )
    return rows


def rab_matter_theorem_rows() -> list[dict[str, Any]]:
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "theorem_id": "RMC1574_0_define_charge",
            "claim_piece": "R_AB matter charge definition",
            "formula": "beta_i^R := partial ln m_i^eff / partial R_AB = M_i^-1 delta_{v_R} S_i",
            "derivation_status": "DEFINED_FROM_1573_KERNEL",
            "current_blocker": "requires parent-owned R_AB vertical generator and matter mass functional",
            **flags(),
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "theorem_id": "RMC1574_1_chain_rule",
            "claim_piece": "matter-pullback zero route",
            "formula": "delta_{v_R} S_i = D Sbar_i[q(Phi),theta_i] . Dq[v_R] + sum_a J_theta^a Lie_{v_R} theta_a + boundary",
            "derivation_status": "EXACT_CONDITIONAL_CHAIN_RULE",
            "current_blocker": "Dq[v_R]=0, constant superselection, and boundary silence are not parent-signed",
            **flags(),
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "theorem_id": "RMC1574_2_zero_if_signed",
            "claim_piece": "beta_S^R=beta_T^R=0",
            "formula": "if S_i descends through q on an open neighbourhood, Dq[v_R]=0, Lie_v theta_i=0, and boundary_i=0 then beta_i^R=0",
            "derivation_status": "EXACT_CONDITIONAL_THEOREM_NOT_SIGNED",
            "current_blocker": "1519 and 1044 keep matter constants, parent q, observed coframe, and no-marker clauses unsigned",
            **flags(),
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "theorem_id": "RMC1574_3_alpha_consequence",
            "claim_piece": "R10 source amplitude",
            "formula": "beta_S^R beta_T^R=0 would remove the bulk source-test exchange term in alpha_MTS",
            "derivation_status": "CONSEQUENCE_ONLY",
            "current_blocker": "boundary/readout tail and no-physical-pole route would still need separate parent signatures",
            **flags(),
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "theorem_id": "RMC1574_4_current_verdict",
            "claim_piece": "current MTS beta zero",
            "formula": "beta_S^R=beta_T^R=0 is not imported",
            "derivation_status": "FAIL_CURRENT_CLAIM_MATTER_CHARGE_ZERO_NOT_PARENT_SIGNED",
            "current_blocker": "finite beta/Z/M/Xi/boundary rows must remain open",
            **flags(),
        },
    ]


def premise_matrix_rows() -> list[dict[str, Any]]:
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "premise_id": "RPM1574_0_R_vertical",
            "premise": "v_R is the parent vertical generator for R_AB and lies in ker(Dq)",
            "needed_for": "geometry pullback and beta_i^R zero",
            "current_status": "NOT_PARENT_SIGNED",
            "if_missing": "R_AB can be a physical fifth-force direction",
            **flags(),
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "premise_id": "RPM1574_1_matter_functor",
            "premise": "S_matter=sum_i Sbar_i[Psi_i,e_obs(q(Phi)),theta_i]",
            "needed_for": "all ordinary matter sees only quotient-owned observed geometry",
            "current_status": "NOT_PARENT_SIGNED",
            "if_missing": "matter mass can carry beta_i^R",
            **flags(),
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "premise_id": "RPM1574_2_constant_superselection",
            "premise": "Lie_{v_R} theta_i=0 for masses, charges, alpha_EM, clocks, composition labels",
            "needed_for": "no hidden material or constant charge",
            "current_status": "NOT_PARENT_SIGNED",
            "if_missing": "beta_i^R may enter through constants or material markers",
            **flags(),
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "premise_id": "RPM1574_3_no_marker_source_weight",
            "premise": "no source-only prefactor, hidden conformal/disformal frame, post-readout mask, or species weight",
            "needed_for": "no WEP/R10 source-charge loophole",
            "current_status": "CONTRACT_WRITTEN_NOT_DERIVED",
            "if_missing": "relative beta_s/beta_t tails remain live",
            **flags(),
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "premise_id": "RPM1574_4_boundary_support",
            "premise": "matter boundary/worldtube terms are zero, exact, or separately bounded",
            "needed_for": "no boundary charge hiding in beta_i^R",
            "current_status": "OPEN",
            "if_missing": "boundary/readout tail must be included in alpha_MTS envelope",
            **flags(),
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "premise_id": "RPM1574_5_verdict",
            "premise": "all matter-charge zero premises pass simultaneously",
            "needed_for": "beta_S^R=beta_T^R=0 claim",
            "current_status": "FAIL_CURRENT_CLAIM",
            "if_missing": "stage finite source-charge inputs and keep R10 unscored",
            **flags(),
        },
    ]


def finite_input_rows() -> list[dict[str, Any]]:
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "input_id": "FIN1574_0_beta_source",
            "symbol": "beta_S^R",
            "required_form": "parent-signed zero theorem or numeric partial ln m_source / partial R_AB with material/source path and units",
            "current_status": "MISSING_SOURCE_CHARGE_OR_ZERO_THEOREM",
            "score_use": "bulk source leg in alpha_MTS",
            **flags(),
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "input_id": "FIN1574_1_beta_test",
            "symbol": "beta_T^R",
            "required_form": "parent-signed zero theorem or numeric partial ln m_test / partial R_AB with material/source path and units",
            "current_status": "MISSING_TEST_CHARGE_OR_ZERO_THEOREM",
            "score_use": "bulk test leg in alpha_MTS",
            **flags(),
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "input_id": "FIN1574_2_ZR",
            "symbol": "Z_R",
            "required_form": "positive parent kinetic residue in same normalization as beta legs, or no-pole/constraint theorem",
            "current_status": "MISSING_ZR_OR_NO_POLE_THEOREM",
            "score_use": "tau_R10 denominator and lambda_R numerator",
            **flags(),
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "input_id": "FIN1574_3_MR2",
            "symbol": "M_R^2",
            "required_form": "positive parent Hessian/mass-gap in same normalization as Z_R",
            "current_status": "MISSING_MR2",
            "score_use": "lambda_R=sqrt(Z_R/M_R^2)",
            **flags(),
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "input_id": "FIN1574_4_Xi",
            "symbol": "Xi_R10",
            "required_form": "source-backed R10 sign/readout/window convention mapping parent potential to alpha(lambda)",
            "current_status": "MISSING_R10_READOUT_CONVENTION",
            "score_use": "overall alpha_MTS convention",
            **flags(),
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "input_id": "FIN1574_5_tail",
            "symbol": "alpha_boundary_tail",
            "required_form": "zero theorem or absolute no-cancellation bound for boundary/domain/non-Hilbert/readout terms",
            "current_status": "MISSING_TAIL_ZERO_OR_BOUND",
            "score_use": "tail added in absolute envelope, not cancellation",
            **flags(),
        },
    ]


def alpha_template_rows() -> list[dict[str, Any]]:
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "model_id": "MTS_RAB_R10_1574_symbolic_beta_template",
            "lambda_value": "sqrt(Z_R/M_R^2) after units conversion",
            "alpha_predicted": "Xi_R10*(beta_S^R*beta_T^R/(4*pi*G*Z_R)+alpha_boundary_tail)",
            "zero_branch": "alpha_bulk=0 only if beta_S^R=beta_T^R=0 is parent-signed; tail also needs zero/bound",
            "current_status": "TEMPLATE_ONLY_INPUTS_MISSING",
            "failure_reasons": "MISSING_BETA_SOURCE;MISSING_BETA_TEST;MISSING_ZR;MISSING_MR2;MISSING_XI;MISSING_TAIL;CURVE_NOT_ACCEPTED",
            "accepted_for_scoring": False,
            "passes_for_claim": False,
            **flags(),
        }
    ]


def runner_rows() -> list[dict[str, Any]]:
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "runner_id": "RUN1574_0_sources",
            "object": "1573 kernel plus 1036/1044/1485/1519 descent sources",
            "status": "PASS_IF_VALIDATION_PASS",
            "detail": "source register checks all needles before using theorem scaffold",
            **flags(),
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "runner_id": "RUN1574_1_beta_zero",
            "object": "beta_S^R beta_T^R zero theorem",
            "status": "EXACT_CONDITIONAL_NOT_PARENT_SIGNED",
            "detail": "chain rule is exact but R_AB verticality, matter functor, constants, markers, and boundary support are unsigned",
            **flags(),
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "runner_id": "RUN1574_2_finite_inputs",
            "object": "finite beta/Z/M/Xi/tail rows",
            "status": "STAGED_NONCLAIM_VALUES_MISSING",
            "detail": "input schema is ready but contains no numeric/source-backed claim rows",
            **flags(),
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "runner_id": "RUN1574_3_R10_score",
            "object": "R10 alpha(lambda) score",
            "status": "BLOCKED_NO_CLAIM",
            "detail": "zero theorem not signed, finite inputs missing, and curve remains non-accepted",
            **flags(),
        },
    ]


def claim_gate_rows() -> list[dict[str, Any]]:
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "gate_id": "GATE1574_0_chain_rule",
            "claim": "R_AB matter-charge chain-rule theorem written",
            "status": "PASS_FORMAL_NONCLAIM",
            "reason": "derived from matter pullback and 1573 beta definition",
            **flags(),
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "gate_id": "GATE1574_1_beta_zero",
            "claim": "beta_S^R=beta_T^R=0",
            "status": "BLOCKED_NO_CLAIM",
            "reason": "matter descent and no-marker/source-current clauses remain unsigned",
            **flags(),
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "gate_id": "GATE1574_2_finite_alpha",
            "claim": "finite numeric alpha_MTS(lambda_R)",
            "status": "BLOCKED_NO_CLAIM",
            "reason": "beta/Z/M/Xi/tail values missing",
            **flags(),
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "gate_id": "GATE1574_3_local_GR",
            "claim": "derived local GR/Newton source side",
            "status": "BLOCKED_NO_CLAIM",
            "reason": "ordinary matter pullback alone does not close boundary, q_loc, PPN, or source denominator gates",
            **flags(),
        },
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "decision_id": "DEC1574_0_derivation",
            "decision": "RAB_MATTER_CHARGE_ZERO_THEOREM_EXACT_CONDITIONAL",
            "reason": "beta_i^R is killed by chain rule if R_AB is quotient-vertical and matter/constants/boundaries descend",
            "consequence": "this is the right route to pursue, but it is not a claim import",
            **flags(),
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "decision_id": "DEC1574_1_current_status",
            "decision": "ZERO_NOT_PARENT_SIGNED_FINITE_ROWS_STAGED",
            "reason": "current corpus still has unsigned parent q, observed coframe, matter constants, markers, source-current, and boundary clauses",
            "consequence": "R10 branch remains nonclaim with explicit beta/Z/M/Xi/tail inputs",
            **flags(),
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "decision_id": "DEC1574_2_next",
            "decision": "NEXT_1575_PARENT_RAB_VERTICAL_GENERATOR_AND_MATTER_DESCENT_SIGNATURE",
            "reason": "the least-scrutiny path is to sign v_R in ker(Dq) plus S_matter=Sbar[q,theta] before chasing numeric beta rows",
            "consequence": "try to construct the parent R_AB vertical generator/descent signature; if it fails, fill component bound rows",
            **flags(),
        },
    ]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "next_target": "1575-Y5-RAB-parent-RAB-vertical-generator-and-matter-descent-signature.md",
            "script": "scripts/Y5_RAB_parent_RAB_vertical_generator_and_matter_descent_signature.py",
            "objective": "try to parent-sign v_R in ker(Dq), observed coframe/matter functor descent, constant superselection, no-marker source weights, and boundary silence for R_AB; otherwise build beta component bound rows",
            "do_not": "do not score R10; do not import qbarXT zero as R_AB zero; do not claim local GR; do not edit formalization-workbench",
            **flags(),
        }
    ]


def copy_outputs() -> None:
    for source, targets in COPY_TARGETS.items():
        for target in targets:
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(source, target)


def remove_pycache() -> None:
    pycache = ROOT / "scripts" / "__pycache__"
    if pycache.exists():
        shutil.rmtree(pycache)


def formalization_modified_count() -> int:
    try:
        result = subprocess.run(
            ["git", "-C", str(ROOT.parent), "status", "--short", "--", "formalization-workbench"],
            capture_output=True,
            text=True,
            check=False,
        )
    except FileNotFoundError:
        return 0
    return len([line for line in result.stdout.splitlines() if line.strip()])


def has_1574_rows(folder: Path) -> bool:
    if not folder.exists():
        return False
    return any("1574" in path.name for path in folder.glob("*.csv"))


def validation_rows(generated_csvs: list[Path]) -> list[dict[str, Any]]:
    sources = read_csv(SOURCE_REGISTER)
    theorem = read_csv(RAB_MATTER_THEOREM)
    premises = read_csv(PREMISE_MATRIX)
    finite = read_csv(FINITE_INPUT_ROWS)
    template = read_csv(ALPHA_TEMPLATE)
    runner = read_csv(RUNNER)
    gates = read_csv(CLAIM_GATE)
    decisions = read_csv(DECISION)
    checks = [
        ("VAL1574_0_sources_exist", all(row["exists"] == "True" for row in sources), "all cited source paths exist"),
        ("VAL1574_1_needles_found", all(row["needle_found"] == "True" for row in sources), "all source needles found"),
        (
            "VAL1574_2_chain_rule",
            any(row["theorem_id"] == "RMC1574_1_chain_rule" and row["derivation_status"] == "EXACT_CONDITIONAL_CHAIN_RULE" for row in theorem),
            "R_AB matter-charge chain rule written",
        ),
        (
            "VAL1574_3_zero_not_imported",
            any(row["theorem_id"] == "RMC1574_4_current_verdict" and "FAIL_CURRENT_CLAIM" in row["derivation_status"] for row in theorem),
            "beta zero theorem remains unimported",
        ),
        (
            "VAL1574_4_premise_matrix_blocked",
            all(row["current_status"] != "PARENT_SIGNED" for row in premises),
            "all premise rows remain nonclaim/blocked",
        ),
        (
            "VAL1574_5_finite_inputs_staged",
            all(row["current_status"].startswith("MISSING") for row in finite),
            "finite input rows staged with missing statuses",
        ),
        (
            "VAL1574_6_alpha_template_nonclaim",
            len(template) == 1 and template[0]["current_status"] == "TEMPLATE_ONLY_INPUTS_MISSING" and template[0]["accepted_for_scoring"] == "False",
            "alpha template is nonclaim and not accepted",
        ),
        (
            "VAL1574_7_runner_blocks_score",
            any(row["runner_id"] == "RUN1574_3_R10_score" and row["status"] == "BLOCKED_NO_CLAIM" for row in runner),
            "runner blocks R10 score",
        ),
        (
            "VAL1574_8_claim_gates_closed",
            all(row["claim_allowed"] == "False" for row in gates) and any(row["gate_id"] == "GATE1574_0_chain_rule" for row in gates),
            "claim gates closed while chain-rule gate is nonclaim pass",
        ),
        (
            "VAL1574_9_decision_next",
            any(row["decision"] == "NEXT_1575_PARENT_RAB_VERTICAL_GENERATOR_AND_MATTER_DESCENT_SIGNATURE" for row in decisions),
            "decision selects R_AB vertical generator and matter descent target",
        ),
        ("VAL1574_10_csv_parse", all(len(read_csv(path)) > 0 for path in generated_csvs), "all generated 1574 CSVs parse cleanly"),
        ("VAL1574_11_claim_flags_false", generated_flags_false(generated_csvs), "all generated prediction/claim flags remain false"),
        ("VAL1574_12_no_raw_accepted", not has_1574_rows(RAB_RAW) and not has_1574_rows(RAB_ACCEPTED), "no 1574 rows written to raw/accepted finite directories"),
        ("VAL1574_13_branch_copies", all(target.exists() for targets in COPY_TARGETS.values() for target in targets), "branch/quarantine nonclaim copies written"),
        ("VAL1574_14_pycache_absent", not (ROOT / "scripts" / "__pycache__").exists(), "scripts __pycache__ absent after run"),
        ("VAL1574_15_formalization_untouched", formalization_modified_count() == 0, "formalization-workbench modified-file count is 0"),
    ]
    rows = [
        {
            "same_parent_branch_id": BRANCH_ID,
            "check_id": check_id,
            "result": "PASS" if passed else "FAIL",
            "detail": detail,
        }
        for check_id, passed, detail in checks
    ]
    rows.append(
        {
            "same_parent_branch_id": BRANCH_ID,
            "check_id": "VAL1574_OVERALL",
            "result": "PASS" if all(row["result"] == "PASS" for row in rows) else "FAIL",
            "detail": "1574 R_AB matter charge and finite input validation",
        }
    )
    return rows


def md_table(rows: list[dict[str, Any]], columns: list[str]) -> str:
    header = "| " + " | ".join(columns) + " |"
    sep = "| " + " | ".join(["---"] * len(columns)) + " |"
    body = ["| " + " | ".join(str(row.get(col, "")) for col in columns) + " |" for row in rows]
    return "\n".join([header, sep, *body])


def write_doc(
    sources: list[dict[str, Any]],
    theorem: list[dict[str, Any]],
    premises: list[dict[str, Any]],
    finite: list[dict[str, Any]],
    template: list[dict[str, Any]],
    runner: list[dict[str, Any]],
    gates: list[dict[str, Any]],
    decisions: list[dict[str, Any]],
    validation: list[dict[str, Any]],
    next_rows: list[dict[str, Any]],
) -> None:
    DOC.write_text(
        "\n\n".join(
            [
                "# 1574 - R_AB R10 Matter Charge And ZR/MR2 Input Row Or Zero Theorem",
                "## Verdict\n"
                "- The matter-charge route is now exact as a conditional theorem: `beta_i^R=M_i^-1 delta_{v_R}S_i` vanishes if `v_R in ker(Dq)` and ordinary matter/constants/boundaries descend through the quotient.\n"
                "- This is the right derivation route, but it is not currently parent-signed: `v_R`, `q`, `e_obs(q)`, matter functor descent, constant superselection, no-marker/source-weight exclusion, and boundary support are still unsigned.\n"
                "- The R10 finite branch therefore remains open with explicit nonclaim inputs: `beta_S^R`, `beta_T^R`, `Z_R`, `M_R^2`, `Xi_R10`, and `alpha_boundary_tail`.\n"
                "- No beta-zero import, R10 score, local GR/Newton reduction, PPN, WEP, clock, orbital, `Z_R=0`, `tau_R10=0`, or `q_R=0` claim is made.",
                "## Source Register",
                md_table(sources, ["source_id", "source_path", "exists", "needle_found", "needles"]),
                "## R_AB Matter-Charge Theorem Attempt",
                md_table(theorem, ["theorem_id", "claim_piece", "formula", "derivation_status", "current_blocker"]),
                "## Premise Matrix",
                md_table(premises, ["premise_id", "premise", "needed_for", "current_status", "if_missing"]),
                "## Finite Input Rows",
                md_table(finite, ["input_id", "symbol", "required_form", "current_status", "score_use"]),
                "## R10 Alpha Template",
                md_table(template, ["model_id", "lambda_value", "alpha_predicted", "current_status", "failure_reasons"]),
                "## Runner Nonclaim",
                md_table(runner, ["runner_id", "object", "status", "detail"]),
                "## Claim Gates",
                md_table(gates, ["gate_id", "claim", "status", "reason"]),
                "## Decision",
                md_table(decisions, ["decision_id", "decision", "reason", "consequence"]),
                "## Validation",
                md_table(validation, ["check_id", "result", "detail"]),
                "## Next Target",
                md_table(next_rows, ["next_target", "script", "objective", "do_not"]),
            ]
        )
        + "\n",
        encoding="utf-8",
    )


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    sources = source_register_rows()
    theorem = rab_matter_theorem_rows()
    premises = premise_matrix_rows()
    finite = finite_input_rows()
    template = alpha_template_rows()
    runner = runner_rows()
    gates = claim_gate_rows()
    decisions = decision_rows()
    next_rows = next_target_rows()
    generated_csvs = [
        SOURCE_REGISTER,
        RAB_MATTER_THEOREM,
        PREMISE_MATRIX,
        FINITE_INPUT_ROWS,
        ALPHA_TEMPLATE,
        RUNNER,
        CLAIM_GATE,
        DECISION,
        NEXT_TARGET,
    ]
    write_csv(SOURCE_REGISTER, sources)
    write_csv(RAB_MATTER_THEOREM, theorem)
    write_csv(PREMISE_MATRIX, premises)
    write_csv(FINITE_INPUT_ROWS, finite)
    write_csv(ALPHA_TEMPLATE, template)
    write_csv(RUNNER, runner)
    write_csv(CLAIM_GATE, gates)
    write_csv(DECISION, decisions)
    write_csv(NEXT_TARGET, next_rows)
    copy_outputs()
    remove_pycache()
    validation = validation_rows(generated_csvs)
    write_csv(VALIDATION, validation)
    write_doc(sources, theorem, premises, finite, template, runner, gates, decisions, validation, next_rows)


if __name__ == "__main__":
    main()

from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "source-intake" / "mts_residuals"
MICROSCOPE = ROOT / "source-intake" / "microscope"
BRANCH_RESIDUALS = MICROSCOPE / "branch_locked_wep" / "residuals"
FORMALIZATION = ROOT.parent / "formalization-workbench"
BRANCH_ID = "MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428"
DOC = ROOT / "1561-Y5-minimal-parent-weak-field-action-ansatz-and-Euler-Ward-PPN-gate.md"
START_TS = datetime.now(timezone.utc).timestamp()

SOURCE_FILES = {
    "1560_doc": ROOT / "1560-Y5-parent-weak-field-zero-condition-derivation-or-demotion.md",
    "1560_validation": OUT / "P8_Y5_BRR545_1560_VALIDATION.csv",
    "1560_next": OUT / "P8_Y5_PARENT_QLOC_1560_NEXT_TARGET.csv",
    "1560_contract": OUT / "P8_Y5_PARENT_QLOC_1560_CONDITIONAL_ZERO_THEOREM_CONTRACT.csv",
    "1560_demotion": OUT / "P8_Y5_PARENT_QLOC_1560_BOUNDED_CLOSURE_DEMOTION.csv",
    "511_doc": ROOT / "511-minimal-parent-action-local-GR-fixed-point-ansatz.md",
    "512_doc": ROOT / "512-match-MTS-symbols-to-local-GR-action-blocks.md",
    "505_doc": ROOT / "505-parent-Noether-mass-charge-closure-theorem-or-closure-demotion.md",
    "506_doc": ROOT / "506-local-EH-reduction-and-extra-sector-silence-theorem.md",
    "537_doc": ROOT / "537-Y5-Hilbert-worldtube-parent-action-contract-or-PiM-input-fill.md",
    "538_doc": ROOT / "538-Y5-minimal-parent-action-Euler-Ward-test-or-closure-demotion.md",
    "1008_doc": ROOT / "1008-Y5-R10-parent-theta-Qtau-extraction-or-charge-decomposition-runner.md",
    "19_doc": ROOT / "19-constrained-parent-action-skeleton.md",
}

NEEDLES = {
    "1560_doc": ["local GR branch is demoted", "bounded closure control lane"],
    "1560_validation": ["VAL1560_OVERALL", "PASS"],
    "1560_next": ["1561-Y5-minimal-parent-weak-field-action-ansatz-and-Euler-Ward-PPN-gate.md"],
    "1560_contract": ["COND1560_0_L_parent", "COND1560_7_consequence"],
    "1560_demotion": ["DEM1560_0_local_GR_branch", "BOUNDED_CLOSURE_CONTROL_NOT_DERIVED"],
    "511_doc": ["minimal_parent_action_local_GR_fixed_point_ansatz_constructed_not_adopted", "A511_0_EH_core", "FP511_7_metric_PPN_readout"],
    "512_doc": ["No major MTS symbol is fully promoted", "q_loc^nu"],
    "505_doc": ["conditional_parent_Noether_mass_charge_closure_theorem_derived", "premises_not_yet_parent_derived"],
    "506_doc": ["conditional_theorem_not_MTS_promotion", "positive source-free local operator"],
    "537_doc": ["parent-action contract", "PAC537_9_second_order_PPN_stability"],
    "538_doc": ["conditional_Euler_Ward_chain_only_no_PiM", "EW538_A_EH_silent_parent"],
    "1008_doc": ["missing_explicit_current_chain", "theta_MTS"],
    "19_doc": ["S_R_constraint = integral sqrt(-g) lambda_R R_AB.", "closure_term."],
}

SOURCE_REGISTER = OUT / "P8_Y5_PARENT_QLOC_1561_SOURCE_REGISTER.csv"
ANSATZ_REGISTER = OUT / "P8_Y5_PARENT_QLOC_1561_MINIMAL_ACTION_ANSATZ_REGISTER.csv"
EULER_GATE = OUT / "P8_Y5_PARENT_QLOC_1561_EULER_VARIATION_GATE.csv"
WARD_PPN_GATE = OUT / "P8_Y5_PARENT_QLOC_1561_WARD_PPN_GATE.csv"
ADOPTION_LEDGER = OUT / "P8_Y5_PARENT_QLOC_1561_ADOPTION_REJECTION_LEDGER.csv"
RUNNER = OUT / "P8_Y5_PARENT_QLOC_1561_RUNNER_NONCLAIM.csv"
CLAIM_GATE = OUT / "P8_Y5_PARENT_QLOC_1561_CLAIM_GATE.csv"
DECISION = OUT / "P8_Y5_PARENT_QLOC_1561_DECISION.csv"
NEXT_TARGET = OUT / "P8_Y5_PARENT_QLOC_1561_NEXT_TARGET.csv"
VALIDATION = OUT / "P8_Y5_BRR545_1561_VALIDATION.csv"

QUARANTINE = MICROSCOPE / "quarantine" / "1561"
QUAR_ANSATZ = QUARANTINE / "MINIMAL_ACTION_ANSATZ_REGISTER_NONCLAIM.csv"
QUAR_EULER = QUARANTINE / "EULER_VARIATION_GATE_NONCLAIM.csv"
QUAR_WARD = QUARANTINE / "WARD_PPN_GATE_NONCLAIM.csv"
QUAR_ADOPTION = QUARANTINE / "ADOPTION_REJECTION_LEDGER_NONCLAIM.csv"
QUAR_RUNNER = QUARANTINE / "RUNNER_NONCLAIM.csv"
QUAR_DECISION = QUARANTINE / "DECISION_NONCLAIM.csv"
BRANCH_ANSATZ = BRANCH_RESIDUALS / "minimal_action_ansatz_register_nonclaim_1561.csv"
BRANCH_EULER = BRANCH_RESIDUALS / "Euler_variation_gate_nonclaim_1561.csv"
BRANCH_WARD = BRANCH_RESIDUALS / "Ward_PPN_gate_nonclaim_1561.csv"
BRANCH_ADOPTION = BRANCH_RESIDUALS / "adoption_rejection_ledger_nonclaim_1561.csv"
BRANCH_RUNNER = BRANCH_RESIDUALS / "minimal_ansatz_runner_nonclaim_1561.csv"
BRANCH_DECISION = BRANCH_RESIDUALS / "minimal_ansatz_decision_nonclaim_1561.csv"


def flags() -> dict[str, bool]:
    return {
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


def source_list(*keys: str) -> str:
    return "; ".join(rel(SOURCE_FILES[key]) for key in keys)


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


def parse_csv(path: Path) -> bool:
    read_csv(path)
    return True


def generated_flags_false(paths: list[Path]) -> bool:
    false_values = {"", "false", "0", "no", "none", "null"}
    claim_keys = [
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
        needles = NEEDLES.get(key, [])
        rows.append(
            {
                "same_parent_branch_id": BRANCH_ID,
                "source_id": f"SRC1561_{index}_{key}",
                "source_path": rel(path),
                "exists": path.exists(),
                "needle_found": file_contains(path, needles) if needles else True,
                "needles": "; ".join(needles),
                "purpose": "evidence for minimal parent weak-field action ansatz and Euler/Ward/PPN gate",
                **flags(),
            }
        )
    return rows


def ansatz_rows() -> list[dict[str, Any]]:
    rows = [
        (
            "ANS1561_A_EH_lambdaR_silent",
            "S_EH[g_obs] + S_matter[g_obs,psi] + int sqrt(-g) lambda_R R_AB + S_silent[Phi,g_obs] + S_boundary",
            "delta lambda_R gives R_AB=0; EH core gives beta=1 if source/readout is owned",
            "lambda_R parent origin, lambda_R stress silence, source/PiM charge ownership, and extra-sector silence are not proved",
            "BEST_CONDITIONAL_ANSATZ_NOT_ADOPTED",
        ),
        (
            "ANS1561_B_lambdaR_only",
            "int sqrt(-g) lambda_R R_AB + source/load scaffold",
            "formal q_R=0 if lambda_R is accepted",
            "no spin-2/EH second-order beta completion; still a closure multiplier",
            "REJECTED_INCOMPLETE_PARENT_ACTION",
        ),
        (
            "ANS1561_C_EH_only",
            "S_EH[g_obs] + S_matter[g_obs,psi]",
            "standard local GR weak-field and beta=1",
            "derives target by replacing MTS with EH; no MTS reciprocal-sector origin",
            "FORBIDDEN_EH_IMPORT_AS_MTS_DERIVATION",
        ),
        (
            "ANS1561_D_kinetic_RAB",
            "S_EH + S_matter + 0.5 int sqrt(-g) W grad R_AB grad R_AB",
            "dynamical reciprocal field can be varied",
            "generic Q_R/r hair survives unless zero-charge theorem is separately supplied",
            "REJECTED_QR_HAIR",
        ),
        (
            "ANS1561_E_Hamiltonian_PiM_definition",
            "case A plus Pi_M J_H := 4*pi*G_ref dQ_tau on local branch",
            "could repair source-charge map by defining Pi_M as parent Hamiltonian charge readout",
            "changes/clarifies Pi_M semantics; still needs parent fixed reference and zero residual pieces",
            "POSSIBLE_REPAIR_NOT_CURRENT_DERIVATION",
        ),
    ]
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "ansatz_id": ansatz_id,
            "candidate_parent_action": candidate_parent_action,
            "what_it_derives_conditionally": what_it_derives_conditionally,
            "what_blocks_adoption": what_blocks_adoption,
            "adoption_status": adoption_status,
            "source_paths": source_list("511_doc", "512_doc", "19_doc", "538_doc", "1008_doc", "1560_contract"),
            **flags(),
        }
        for ansatz_id, candidate_parent_action, what_it_derives_conditionally, what_blocks_adoption, adoption_status in rows
    ]


def euler_gate_rows() -> list[dict[str, Any]]:
    rows = [
        (
            "EUL1561_0_variation_exists",
            "delta L_parent = E_A delta Phi^A + d theta_MTS",
            "formal for ansatz A if all terms are declared",
            "CONDITIONAL_PASS_TEMPLATE",
            "not a current MTS derivation because full retained-sector L_parent is not extracted",
        ),
        (
            "EUL1561_1_lambda_variation",
            "delta_{lambda_R} S -> R_AB=0",
            "formally closes q_R=0",
            "FORMAL_PASS_IF_LAMBDAR_PARENT_OWNED",
            "lambda_R origin is currently a closure insertion",
        ),
        (
            "EUL1561_2_lambda_stress",
            "delta_g(lambda_R R_AB) must not add unowned local stress",
            "requires lambda_R=0/on-shell pure constraint stress or parent reaction-stress theorem",
            "FAIL_UNSIGNED_STRESS_SILENCE",
            "otherwise q_R zero is bought by a new unmeasured stress sector",
        ),
        (
            "EUL1561_3_EH_metric",
            "delta_g S_EH + delta_g S_matter gives Einstein operator with Hilbert source",
            "standard beta=1 route conditionally available",
            "CONDITIONAL_EH_PASS_NOT_MTS_ADOPTION",
            "EH core must be matched to MTS primitives rather than imported as whole theory",
        ),
        (
            "EUL1561_4_matter",
            "delta_psi and delta_g S_matter use one observed coframe",
            "would give same source/clock/orbital frame",
            "OPEN_MATTER_DESCENT",
            "WEP/source-frame proof remains unsigned",
        ),
        (
            "EUL1561_5_extra_silence",
            "delta_Phi S_silent gives positive source-free equations and no boundary flux",
            "would suppress extra local hair",
            "OPEN_SECTOR_BY_SECTOR",
            "field-specific operators/signs/source charges not supplied for all MTS sectors",
        ),
        (
            "EUL1561_6_boundary_reference",
            "theta_MTS and Q_tau pieces fixed before readout",
            "would prevent hidden mass/source counterterm",
            "OPEN_BOUNDARY_CHARGE",
            "1008 says parent theta/Q_tau total is not extracted",
        ),
    ]
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "gate_id": gate_id,
            "variation_test": variation_test,
            "conditional_result": conditional_result,
            "status": status,
            "blocking_issue": blocking_issue,
            "source_paths": source_list("537_doc", "538_doc", "1008_doc", "1560_contract"),
            **flags(),
        }
        for gate_id, variation_test, conditional_result, status, blocking_issue in rows
    ]


def ward_ppn_rows() -> list[dict[str, Any]]:
    rows = [
        (
            "WPPN1561_0_Noether",
            "J_tau = theta_MTS(L_tau Phi) - i_tau L_parent",
            "available for an explicit diffeomorphism-covariant action",
            "CONDITIONAL_PASS_TEMPLATE",
            "theta_MTS and all Q_tau pieces remain unextracted",
        ),
        (
            "WPPN1561_1_qR",
            "R_AB=0 -> q_R=0 -> gamma-1=0",
            "formal if lambda_R sector is accepted as parent-owned and stress-silent",
            "CONDITIONAL_UNSIGNED",
            "lambda_R parent-origin and stress-silence theorem missing",
        ),
        (
            "WPPN1561_2_beta",
            "EH second-order weak-field -> beta=1",
            "formal in EH core after source/readout is owned",
            "CONDITIONAL_UNSIGNED",
            "MTS source charge, Pi_M/Hilbert equality, and boundary reference still open",
        ),
        (
            "WPPN1561_3_Bianchi",
            "diffeomorphism invariance -> Bianchi/Ward conservation identity",
            "formal for the complete action",
            "CONDITIONAL_UNSIGNED",
            "full MTS retained-sector action is not explicit",
        ),
        (
            "WPPN1561_4_no_extra_modes",
            "extra sectors are topological/exact/positive-mass silent or bounded",
            "conditional route from 506 exists",
            "OPEN_SECTOR_QUEUE",
            "every MTS sector needs its own operator/source/boundary certificate",
        ),
        (
            "WPPN1561_5_local_claim",
            "q_R=0 and delta_beta=0 as MTS prediction",
            "not reached",
            "BLOCKED_NO_CLAIM",
            "ansatz is not adopted as the current parent theory",
        ),
    ]
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "gate_id": gate_id,
            "ward_or_ppn_test": ward_or_ppn_test,
            "conditional_result": conditional_result,
            "status": status,
            "blocking_issue": blocking_issue,
            "source_paths": source_list("505_doc", "506_doc", "537_doc", "538_doc", "1008_doc", "1560_contract"),
            **flags(),
        }
        for gate_id, ward_or_ppn_test, conditional_result, status, blocking_issue in rows
    ]


def adoption_rows() -> list[dict[str, Any]]:
    rows = [
        ("ADOPT1561_0_lambda_origin", "lambda_R parent origin", "MISSING_PARENT_ORIGIN", "without this the q_R zero is a closure multiplier"),
        ("ADOPT1561_1_lambda_stress", "lambda_R zero-stress/reaction-stress theorem", "MISSING_STRESS_SILENCE", "constraint can otherwise alter local metric/source equations"),
        ("ADOPT1561_2_MTS_matching", "EH/readout blocks matched to MTS primitives", "MISSING_SYMBOL_MATCH", "EH core cannot simply be imported as the finished MTS parent action"),
        ("ADOPT1561_3_source_charge", "Pi_M/Hilbert/Hamiltonian source charge equality", "MISSING_SOURCE_CHARGE_GLUE", "measured GM and beta readout are not parent-owned"),
        ("ADOPT1561_4_boundary", "theta/Q_tau/boundary reference fixed before readout", "MISSING_PARENT_CURRENT_CHAIN", "boundary counterterms can hide calibration"),
        ("ADOPT1561_5_extra_silence", "all non-EH MTS sectors silent or bounded", "MISSING_SECTOR_CERTIFICATES", "local PPN residuals can re-enter through extra sectors"),
        ("ADOPT1561_6_verdict", "ansatz adoption", "NOT_ADOPTED_CURRENT_MTS_DERIVATION", "best ansatz is a repair target, not a claim"),
    ]
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "adoption_id": adoption_id,
            "requirement": requirement,
            "status": status,
            "why_it_blocks": why_it_blocks,
            "source_paths": source_list("511_doc", "512_doc", "537_doc", "538_doc", "1008_doc", "1560_contract"),
            **flags(),
        }
        for adoption_id, requirement, status, why_it_blocks in rows
    ]


def runner_rows() -> list[dict[str, Any]]:
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "runner_id": "RUN1561_0_sources",
            "test": "action ansatz sources and prior gates loaded",
            "current_status": "PASS",
            "detail": "1560 contract plus 511/512/505/506/537/538/1008 action-route evidence loaded",
            **flags(),
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "runner_id": "RUN1561_1_best_ansatz",
            "test": "minimal ansatz construction",
            "current_status": "PASS_CONDITIONAL_NOT_ADOPTED",
            "detail": "EH + universal matter + lambda_R R_AB + silent sectors is the cleanest conditional ansatz",
            **flags(),
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "runner_id": "RUN1561_2_qR_gate",
            "test": "q_R zero gate",
            "current_status": "FORMAL_PASS_BLOCKED_BY_LAMBDAR_ORIGIN_AND_STRESS",
            "detail": "delta lambda_R gives R_AB=0, but parent-origin and zero-stress certificates are missing",
            **flags(),
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "runner_id": "RUN1561_3_beta_gate",
            "test": "delta_beta zero gate",
            "current_status": "CONDITIONAL_EH_PASS_BLOCKED_BY_SOURCE_CHARGE_AND_ADOPTION",
            "detail": "EH weak-field gives beta=1 only after source/readout/PiM and boundary chain are parent-owned",
            **flags(),
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "runner_id": "RUN1561_4_claim",
            "test": "local GR/Newton claim",
            "current_status": "BLOCKED_NO_CLAIM",
            "detail": "ansatz is a repair candidate, not a signed MTS parent action",
            **flags(),
        },
    ]


def claim_gate_rows() -> list[dict[str, Any]]:
    rows = [
        ("GATE1561_0_ansatz", "minimal ansatz as current MTS parent action", "BLOCKED_NO_CLAIM", "not adopted; parent-origin and symbol matching open"),
        ("GATE1561_1_qR", "q_R=0 parent prediction", "BLOCKED_NO_CLAIM", "lambda_R origin/stress gates fail"),
        ("GATE1561_2_beta", "delta_beta=0 parent prediction", "BLOCKED_NO_CLAIM", "source charge/PiM/boundary and MTS adoption gates fail"),
        ("GATE1561_3_matter", "universal matter/coframe descent", "BLOCKED_NO_CLAIM", "matter action descent remains open"),
        ("GATE1561_4_extra", "extra-sector silence", "BLOCKED_NO_CLAIM", "sector-by-sector silence certificates missing"),
        ("GATE1561_5_local_GR", "derived local GR/Newton reduction", "BLOCKED_NO_CLAIM", "bounded closure lane remains the honest status"),
    ]
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "gate_id": gate_id,
            "claim_gate": claim_gate,
            "status": status,
            "reason": reason,
            "source_paths": source_list("1560_contract", "511_doc", "537_doc", "538_doc", "1008_doc"),
            **flags(),
        }
        for gate_id, claim_gate, status, reason in rows
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "decision_id": "DEC1561_0_verdict",
            "decision": "minimal parent weak-field ansatz",
            "result": "BEST_CONDITIONAL_ANSATZ_WRITTEN_NOT_ADOPTED",
            "reason": "the ansatz can formally sign q_R/beta only if lambda_R and EH/source/readout sectors are parent-owned and stress-silent; those gates remain open",
            **flags(),
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "decision_id": "DEC1561_1_branch_status",
            "decision": "local branch",
            "result": "BOUNDED_CLOSURE_CONTROL_REMAINS",
            "reason": "the ansatz is a repair route, not evidence that current MTS already derives local GR",
            **flags(),
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "decision_id": "DEC1561_2_next",
            "decision": "next target",
            "result": "NEXT_1562_LAMBDAR_PARENT_ORIGIN_ZERO_STRESS_TEST",
            "reason": "the hinge is now lambda_R: either derive it as a legitimate parent constraint with no local stress leakage, or keep q_R bounded closure",
            **flags(),
        },
    ]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "next_id": "NEXT1561_0_1562",
            "next_target": "1562-Y5-lambdaR-parent-origin-zero-stress-and-first-class-constraint-test.md",
            "script": "scripts/Y5_lambdaR_parent_origin_zero_stress_and_first_class_constraint_test.py",
            "objective": "test whether lambda_R R_AB can be derived as a parent-owned first-class/auxiliary constraint with zero local stress and proper boundary charge; if not, keep q_R=0 as closure-only and use the bounded PPN runner",
            "do_not": "do not accept lambda_R as derivation merely because variation gives R_AB=0; do not claim local GR/Newton reduction; do not edit formalization-workbench",
            **flags(),
        }
    ]


def copy_outputs() -> None:
    copies = [
        (ANSATZ_REGISTER, QUAR_ANSATZ),
        (EULER_GATE, QUAR_EULER),
        (WARD_PPN_GATE, QUAR_WARD),
        (ADOPTION_LEDGER, QUAR_ADOPTION),
        (RUNNER, QUAR_RUNNER),
        (DECISION, QUAR_DECISION),
        (ANSATZ_REGISTER, BRANCH_ANSATZ),
        (EULER_GATE, BRANCH_EULER),
        (WARD_PPN_GATE, BRANCH_WARD),
        (ADOPTION_LEDGER, BRANCH_ADOPTION),
        (RUNNER, BRANCH_RUNNER),
        (DECISION, BRANCH_DECISION),
    ]
    for source, destination in copies:
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(source, destination)


def remove_pycache() -> None:
    pycache = ROOT / "scripts" / "__pycache__"
    if pycache.exists():
        shutil.rmtree(pycache)


def formalization_modified_count_since_start() -> int:
    if not FORMALIZATION.exists():
        return 0
    return sum(1 for path in FORMALIZATION.rglob("*") if path.is_file() and path.stat().st_mtime >= START_TS)


def validation_rows(generated_csvs: list[Path]) -> list[dict[str, Any]]:
    sources = read_csv(SOURCE_REGISTER)
    ansatz = read_csv(ANSATZ_REGISTER)
    euler = read_csv(EULER_GATE)
    ward = read_csv(WARD_PPN_GATE)
    adoption = read_csv(ADOPTION_LEDGER)
    run_rows = read_csv(RUNNER)
    gate_rows = read_csv(CLAIM_GATE)
    decision_items = read_csv(DECISION)
    next_rows = read_csv(NEXT_TARGET)

    checks = [
        ("VAL1561_0_sources_exist", all(row["exists"] == "True" for row in sources), "all cited 1561 source paths exist"),
        ("VAL1561_1_needles_found", all(row["needle_found"] == "True" for row in sources), "all registered evidence needles found"),
        ("VAL1561_2_best_ansatz", any(row["ansatz_id"] == "ANS1561_A_EH_lambdaR_silent" and row["adoption_status"] == "BEST_CONDITIONAL_ANSATZ_NOT_ADOPTED" for row in ansatz), "best conditional ansatz written but not adopted"),
        ("VAL1561_3_euler_lambda_formal", any(row["gate_id"] == "EUL1561_1_lambda_variation" and row["status"] == "FORMAL_PASS_IF_LAMBDAR_PARENT_OWNED" for row in euler), "lambda variation formal q_R gate recorded"),
        ("VAL1561_4_euler_lambda_stress_fails", any(row["gate_id"] == "EUL1561_2_lambda_stress" and row["status"] == "FAIL_UNSIGNED_STRESS_SILENCE" for row in euler), "lambda stress silence failure recorded"),
        ("VAL1561_5_ward_beta_conditional", any(row["gate_id"] == "WPPN1561_2_beta" and row["status"] == "CONDITIONAL_UNSIGNED" for row in ward), "beta gate is conditional unsigned"),
        ("VAL1561_6_adoption_blocks", len(adoption) >= 7 and any(row["adoption_id"] == "ADOPT1561_6_verdict" and row["status"] == "NOT_ADOPTED_CURRENT_MTS_DERIVATION" for row in adoption), "adoption rejection ledger complete"),
        ("VAL1561_7_runner_claim_block", any(row["runner_id"] == "RUN1561_4_claim" and row["current_status"] == "BLOCKED_NO_CLAIM" for row in run_rows), "runner blocks local claim"),
        ("VAL1561_8_claim_gates", all(row["status"] == "BLOCKED_NO_CLAIM" for row in gate_rows), "all claim gates remain blocked"),
        ("VAL1561_9_decision_next", any(row["result"] == "NEXT_1562_LAMBDAR_PARENT_ORIGIN_ZERO_STRESS_TEST" for row in decision_items), "decision selects lambda_R origin/stress test next"),
        ("VAL1561_10_next_target", any("1562-Y5-lambdaR-parent-origin" in row["next_target"] for row in next_rows), "next target is lambda_R parent-origin zero-stress test"),
        ("VAL1561_11_csv_parse", all(parse_csv(path) for path in generated_csvs), "all generated 1561 CSVs parse cleanly"),
        ("VAL1561_12_claim_flags_false", generated_flags_false(generated_csvs), "all generated prediction/claim flags remain false"),
        ("VAL1561_13_branch_copies", all(path.exists() for path in [QUAR_ANSATZ, QUAR_EULER, QUAR_WARD, QUAR_ADOPTION, QUAR_RUNNER, QUAR_DECISION, BRANCH_ANSATZ, BRANCH_EULER, BRANCH_WARD, BRANCH_ADOPTION, BRANCH_RUNNER, BRANCH_DECISION]), "branch/quarantine nonclaim copies written"),
        ("VAL1561_14_pycache_absent", not (ROOT / "scripts" / "__pycache__").exists(), "scripts __pycache__ absent after run"),
        ("VAL1561_15_formalization_untouched", formalization_modified_count_since_start() == 0, "formalization modified-file count since start=0"),
    ]
    overall = all(result for _, result, _ in checks)
    rows = [
        {
            "same_parent_branch_id": BRANCH_ID,
            "check_id": check_id,
            "result": "PASS" if result else "FAIL",
            "detail": detail,
        }
        for check_id, result, detail in checks
    ]
    rows.append(
        {
            "same_parent_branch_id": BRANCH_ID,
            "check_id": "VAL1561_OVERALL",
            "result": "PASS" if overall else "FAIL",
            "detail": "1561 minimal parent weak-field action ansatz and Euler/Ward/PPN gate validation",
        }
    )
    return rows


def md_table(rows: list[dict[str, Any]], columns: list[str]) -> str:
    if not rows:
        return "_No rows._"
    header = "| " + " | ".join(columns) + " |"
    sep = "| " + " | ".join("---" for _ in columns) + " |"
    body = []
    for row in rows:
        body.append("| " + " | ".join(str(row.get(column, "")).replace("\n", " ") for column in columns) + " |")
    return "\n".join([header, sep, *body])


def write_doc(
    sources: list[dict[str, Any]],
    ansatz: list[dict[str, Any]],
    euler: list[dict[str, Any]],
    ward: list[dict[str, Any]],
    adoption: list[dict[str, Any]],
    run_rows: list[dict[str, Any]],
    gate_rows: list[dict[str, Any]],
    decision_items: list[dict[str, Any]],
    validation: list[dict[str, Any]],
    next_rows: list[dict[str, Any]],
) -> None:
    DOC.write_text(
        "\n".join(
            [
                "# 1561 - Minimal Parent Weak-Field Action Ansatz and Euler/Ward/PPN Gate",
                "",
                "## Verdict",
                "- A minimal repair ansatz was constructed: `S_EH + S_matter + int sqrt(-g) lambda_R R_AB + S_silent + S_boundary`.",
                "- The ansatz formally gives `R_AB=0` through `delta lambda_R`, and conditionally gives `beta=1` through the EH weak-field core.",
                "- It is not adopted as the current MTS parent theory because `lambda_R` still lacks parent origin and zero-stress proof.",
                "- Source-charge/Pi_M ownership, boundary current extraction, universal matter descent, and extra-sector silence also remain open.",
                "- The next target is now very narrow: prove or reject `lambda_R` as a legitimate parent-owned first-class/auxiliary constraint.",
                "",
                "## Source Register",
                md_table(sources, ["source_id", "source_path", "exists", "needle_found", "needles"]),
                "",
                "## Minimal Action Ansatz Register",
                md_table(ansatz, ["ansatz_id", "candidate_parent_action", "what_it_derives_conditionally", "what_blocks_adoption", "adoption_status"]),
                "",
                "## Euler Variation Gate",
                md_table(euler, ["gate_id", "variation_test", "conditional_result", "status", "blocking_issue"]),
                "",
                "## Ward/PPN Gate",
                md_table(ward, ["gate_id", "ward_or_ppn_test", "conditional_result", "status", "blocking_issue"]),
                "",
                "## Adoption/Rejection Ledger",
                md_table(adoption, ["adoption_id", "requirement", "status", "why_it_blocks"]),
                "",
                "## Runner",
                md_table(run_rows, ["runner_id", "test", "current_status", "detail"]),
                "",
                "## Claim Gates",
                md_table(gate_rows, ["gate_id", "claim_gate", "status", "reason"]),
                "",
                "## Decision",
                md_table(decision_items, ["decision_id", "decision", "result", "reason"]),
                "",
                "## Validation",
                md_table(validation, ["check_id", "result", "detail"]),
                "",
                "## Next Target",
                md_table(next_rows, ["next_target", "script", "objective", "do_not"]),
                "",
            ]
        ),
        encoding="utf-8",
    )


def main() -> None:
    sources = source_register_rows()
    ansatz = ansatz_rows()
    euler = euler_gate_rows()
    ward = ward_ppn_rows()
    adoption = adoption_rows()
    run_rows = runner_rows()
    gate_rows = claim_gate_rows()
    decision_items = decision_rows()
    next_rows = next_target_rows()

    write_csv(SOURCE_REGISTER, sources)
    write_csv(ANSATZ_REGISTER, ansatz)
    write_csv(EULER_GATE, euler)
    write_csv(WARD_PPN_GATE, ward)
    write_csv(ADOPTION_LEDGER, adoption)
    write_csv(RUNNER, run_rows)
    write_csv(CLAIM_GATE, gate_rows)
    write_csv(DECISION, decision_items)
    write_csv(NEXT_TARGET, next_rows)
    copy_outputs()
    remove_pycache()

    generated_csvs = [
        SOURCE_REGISTER,
        ANSATZ_REGISTER,
        EULER_GATE,
        WARD_PPN_GATE,
        ADOPTION_LEDGER,
        RUNNER,
        CLAIM_GATE,
        DECISION,
        NEXT_TARGET,
    ]
    validation = validation_rows(generated_csvs)
    write_csv(VALIDATION, validation)
    write_doc(sources, ansatz, euler, ward, adoption, run_rows, gate_rows, decision_items, validation, next_rows)


if __name__ == "__main__":
    main()

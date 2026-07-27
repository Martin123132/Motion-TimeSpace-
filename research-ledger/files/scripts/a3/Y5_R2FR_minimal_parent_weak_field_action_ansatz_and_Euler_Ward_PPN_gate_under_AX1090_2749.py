from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


SCRIPT_START_UTC = datetime.now(timezone.utc)

ROOT = Path(__file__).resolve().parents[1]
RESIDUALS = ROOT / "source-intake" / "mts_residuals"
LOCAL_BOUNDS = ROOT / "source-intake" / "local_bounds"
SOURCE_WEIGHT = ROOT / "source-intake" / "source-weight"
RAB_QUEUE = ROOT / "source-intake" / "rab-sector" / "acquisition-queue"
FORMALIZATION = ROOT.parent / "formalization-workbench"

DOC = ROOT / "2749-Y5-R2FR-minimal-parent-weak-field-action-ansatz-and-Euler-Ward-PPN-gate-under-AX1090.md"

OUTPUTS = {
    "sources": RESIDUALS / "P8_Y5_R2FR_2749_SOURCE_REGISTER.csv",
    "ansatz": RESIDUALS / "P8_Y5_R2FR_2749_MINIMAL_ACTION_ANSATZ_REGISTER.csv",
    "euler": RESIDUALS / "P8_Y5_R2FR_2749_EULER_VARIATION_GATE.csv",
    "ward": RESIDUALS / "P8_Y5_R2FR_2749_WARD_PPN_GATE.csv",
    "adoption": RESIDUALS / "P8_Y5_R2FR_2749_ADOPTION_REJECTION_LEDGER.csv",
    "runner": RESIDUALS / "P8_Y5_R2FR_2749_RUNNER_NONCLAIM.csv",
    "gates": RESIDUALS / "P8_Y5_R2FR_2749_CLAIM_GATES.csv",
    "decisions": RESIDUALS / "P8_Y5_R2FR_2749_DECISION_LEDGER.csv",
    "next": RESIDUALS / "P8_Y5_R2FR_2749_NEXT_TARGET.csv",
    "branches": RESIDUALS / "P8_Y5_R2FR_2749_BRANCH_COPIES.csv",
    "validation": RESIDUALS / "P8_Y5_BRR545_2749_VALIDATION.csv",
}

BRANCH_OUTPUTS = {
    "ansatz": SOURCE_WEIGHT / "minimal_weak_field_action_ansatz_2749_NONCLAIM.csv",
    "ward": LOCAL_BOUNDS / "euler_ward_ppn_gate_2749_NONCLAIM.csv",
    "next_queue": RAB_QUEUE / "JR2749_LAMBDAR_ORIGIN_ZERO_STRESS_NEXT.csv",
}

BRANCH_ID = "MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428"


def ts() -> str:
    return datetime.now(timezone.utc).isoformat()


def ensure_dirs() -> None:
    for path in {p.parent for p in OUTPUTS.values()} | {p.parent for p in BRANCH_OUTPUTS.values()}:
        path.mkdir(parents=True, exist_ok=True)


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    if not rows:
        raise ValueError(f"refusing empty CSV: {path}")
    fieldnames: list[str] = []
    for row in rows:
        for key in row:
            if key not in fieldnames:
                fieldnames.append(key)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def md(value: Any) -> str:
    return str(value).replace("\n", " ").replace("|", "\\|")


def markdown_table(rows: list[dict[str, Any]], cols: list[str]) -> str:
    header = "| " + " | ".join(cols) + " |"
    sep = "| " + " | ".join("---" for _ in cols) + " |"
    body = ["| " + " | ".join(md(row.get(col, "")) for col in cols) + " |" for row in rows]
    return "\n".join([header, sep, *body])


def rel(path: Path) -> str:
    try:
        return str(path.relative_to(ROOT)).replace("\\", "/")
    except ValueError:
        return str(path)


def local_path(path_text: str) -> Path:
    path = Path(path_text)
    if path.is_absolute():
        return path
    return ROOT / path


def nonclaim(row: dict[str, Any]) -> dict[str, Any]:
    row["numeric_value_present"] = False
    row["source_backed"] = False
    row["score_ready"] = False
    row["valid_prediction_row"] = False
    row["valid_for_claim"] = False
    row["claim_allowed"] = False
    return row


def source_rows() -> list[dict[str, Any]]:
    rows = [
        {
            "source_id": "SRC2749_0_2748_doc",
            "description": "2748 selects minimal parent weak-field action ansatz.",
            "source_path": "2748-Y5-R2FR-parent-weak-field-zero-condition-derivation-or-demotion-under-AX1090.md",
            "required_needles": "NEXT2748_0_2749;COND2748_7_consequence;VAL2748_OVERALL",
        },
        {
            "source_id": "SRC2749_1_2748_validation",
            "description": "2748 validation output.",
            "source_path": "source-intake/mts_residuals/P8_Y5_BRR545_2748_VALIDATION.csv",
            "required_needles": "VAL2748_OVERALL;True;minimal parent weak-field action ansatz",
        },
        {
            "source_id": "SRC2749_2_2748_contract",
            "description": "live conditional zero theorem contract.",
            "source_path": "source-intake/mts_residuals/P8_Y5_R2FR_2748_CONDITIONAL_ZERO_THEOREM_CONTRACT.csv",
            "required_needles": "COND2748_0_L_parent;COND2748_7_consequence",
        },
        {
            "source_id": "SRC2749_3_2748_demotion",
            "description": "live bounded closure demotion ledger.",
            "source_path": "source-intake/mts_residuals/P8_Y5_R2FR_2748_BOUNDED_CLOSURE_DEMOTION.csv",
            "required_needles": "DEM2748_0_local_GR_branch;BOUNDED_CLOSURE_CONTROL_NOT_DERIVED",
        },
        {
            "source_id": "SRC2749_4_1561_doc",
            "description": "prior minimal parent weak-field action ansatz gate.",
            "source_path": "1561-Y5-minimal-parent-weak-field-action-ansatz-and-Euler-Ward-PPN-gate.md",
            "required_needles": "ANS1561_A_EH_lambdaR_silent;EUL1561_2_lambda_stress;NEXT_1562_LAMBDAR_PARENT_ORIGIN_ZERO_STRESS_TEST",
        },
        {
            "source_id": "SRC2749_5_511_doc",
            "description": "minimal parent local-GR fixed-point ansatz.",
            "source_path": "511-minimal-parent-action-local-GR-fixed-point-ansatz.md",
            "required_needles": "minimal_parent_action_local_GR_fixed_point_ansatz_constructed_not_adopted;A511_0_EH_core;FP511_7_metric_PPN_readout",
        },
        {
            "source_id": "SRC2749_6_512_doc",
            "description": "MTS symbol matching to local GR action blocks.",
            "source_path": "512-match-MTS-symbols-to-local-GR-action-blocks.md",
            "required_needles": "No major MTS symbol is fully promoted;q_loc^nu",
        },
        {
            "source_id": "SRC2749_7_505_doc",
            "description": "parent Noether mass-charge closure theorem attempt.",
            "source_path": "505-parent-Noether-mass-charge-closure-theorem-or-closure-demotion.md",
            "required_needles": "conditional_parent_Noether_mass_charge_closure_theorem_derived;premises_not_yet_parent_derived",
        },
        {
            "source_id": "SRC2749_8_506_doc",
            "description": "local EH reduction and extra-sector silence theorem.",
            "source_path": "506-local-EH-reduction-and-extra-sector-silence-theorem.md",
            "required_needles": "conditional_theorem_not_MTS_promotion;positive source-free local operator",
        },
        {
            "source_id": "SRC2749_9_537_doc",
            "description": "Hilbert worldtube parent action contract.",
            "source_path": "537-Y5-Hilbert-worldtube-parent-action-contract-or-PiM-input-fill.md",
            "required_needles": "parent-action contract;PAC537_9_second_order_PPN_stability",
        },
        {
            "source_id": "SRC2749_10_538_doc",
            "description": "minimal parent Euler/Ward test.",
            "source_path": "538-Y5-minimal-parent-action-Euler-Ward-test-or-closure-demotion.md",
            "required_needles": "conditional_Euler_Ward_chain_only_no_PiM;EW538_A_EH_silent_parent",
        },
        {
            "source_id": "SRC2749_11_1008_doc",
            "description": "parent theta/current-chain extraction attempt.",
            "source_path": "1008-Y5-R10-parent-theta-Qtau-extraction-or-charge-decomposition-runner.md",
            "required_needles": "missing_explicit_current_chain;theta_MTS",
        },
        {
            "source_id": "SRC2749_12_19_doc",
            "description": "constrained parent action skeleton.",
            "source_path": "19-constrained-parent-action-skeleton.md",
            "required_needles": "S_R_constraint = integral sqrt(-g) lambda_R R_AB.;closure_term.",
        },
        {
            "source_id": "SRC2749_13_2748_queue",
            "description": "live queue into this checkpoint.",
            "source_path": "source-intake/rab-sector/acquisition-queue/JR2748_MINIMAL_PARENT_WEAK_FIELD_ACTION_NEXT.csv",
            "required_needles": "NEXT2748_0_2749;minimal parent weak-field action ansatz",
        },
    ]
    for row in rows:
        path = local_path(row["source_path"])
        text = path.read_text(encoding="utf-8", errors="replace") if path.exists() else ""
        needles = [needle for needle in row["required_needles"].split(";") if needle]
        missing = [needle for needle in needles if needle not in text]
        row["exists"] = path.exists()
        row["needles_present"] = len(missing) == 0
        row["missing_needles"] = ";".join(missing)
        nonclaim(row)
    return rows


def ansatz_rows() -> list[dict[str, Any]]:
    specs = [
        ("ANS2749_A_EH_lambdaR_silent", "S_EH[g_obs] + S_matter[g_obs,psi] + int sqrt(-g) lambda_R R_AB + S_silent[Phi,g_obs] + S_boundary", "delta lambda_R gives R_AB=0; EH core gives beta=1 if source/readout is owned", "lambda_R parent origin, lambda_R stress silence, source/PiM charge ownership, and extra-sector silence are not proved", "BEST_CONDITIONAL_ANSATZ_NOT_ADOPTED"),
        ("ANS2749_B_lambdaR_only", "int sqrt(-g) lambda_R R_AB + source/load scaffold", "formal q_R=0 if lambda_R is accepted", "no spin-2/EH second-order beta completion; still a closure multiplier", "REJECTED_INCOMPLETE_PARENT_ACTION"),
        ("ANS2749_C_EH_only", "S_EH[g_obs] + S_matter[g_obs,psi]", "standard local GR weak-field and beta=1", "derives target by replacing MTS with EH; no MTS reciprocal-sector origin", "FORBIDDEN_EH_IMPORT_AS_MTS_DERIVATION"),
        ("ANS2749_D_kinetic_RAB", "S_EH + S_matter + 0.5 int sqrt(-g) W grad R_AB grad R_AB", "dynamical reciprocal field can be varied", "generic Q_R/r hair survives unless zero-charge theorem is separately supplied", "REJECTED_QR_HAIR"),
        ("ANS2749_E_Hamiltonian_PiM_definition", "case A plus Pi_M J_H := 4*pi*G_ref dQ_tau on local branch", "could repair source-charge map by defining Pi_M as parent Hamiltonian charge readout", "changes/clarifies Pi_M semantics; still needs parent fixed reference and zero residual pieces", "POSSIBLE_REPAIR_NOT_CURRENT_DERIVATION"),
    ]
    return [nonclaim({"same_parent_branch_id": BRANCH_ID, "ansatz_id": aid, "candidate_parent_action": action, "what_it_derives_conditionally": derives, "what_blocks_adoption": blocks, "adoption_status": status, "source_paths": "511-minimal-parent-action-local-GR-fixed-point-ansatz.md; 19-constrained-parent-action-skeleton.md; 538-Y5-minimal-parent-action-Euler-Ward-test-or-closure-demotion.md; 1008-Y5-R10-parent-theta-Qtau-extraction-or-charge-decomposition-runner.md; source-intake/mts_residuals/P8_Y5_R2FR_2748_CONDITIONAL_ZERO_THEOREM_CONTRACT.csv"}) for aid, action, derives, blocks, status in specs]


def euler_rows() -> list[dict[str, Any]]:
    specs = [
        ("EUL2749_0_variation_exists", "delta L_parent = E_A delta Phi^A + d theta_MTS", "formal for ansatz A if all terms are declared", "CONDITIONAL_PASS_TEMPLATE", "not a current MTS derivation because full retained-sector L_parent is not extracted"),
        ("EUL2749_1_lambda_variation", "delta_{lambda_R} S -> R_AB=0", "formally closes q_R=0", "FORMAL_PASS_IF_LAMBDAR_PARENT_OWNED", "lambda_R origin is currently a closure insertion"),
        ("EUL2749_2_lambda_stress", "delta_g(lambda_R R_AB) must not add unowned local stress", "requires lambda_R=0/on-shell pure constraint stress or parent reaction-stress theorem", "FAIL_UNSIGNED_STRESS_SILENCE", "otherwise q_R zero is bought by a new unmeasured stress sector"),
        ("EUL2749_3_EH_metric", "delta_g S_EH + delta_g S_matter gives Einstein operator with Hilbert source", "standard beta=1 route conditionally available", "CONDITIONAL_EH_PASS_NOT_MTS_ADOPTION", "EH core must be matched to MTS primitives rather than imported as whole theory"),
        ("EUL2749_4_matter", "delta_psi and delta_g S_matter use one observed coframe", "would give same source/clock/orbital frame", "OPEN_MATTER_DESCENT", "WEP/source-frame proof remains unsigned"),
        ("EUL2749_5_extra_silence", "delta_Phi S_silent gives positive source-free equations and no boundary flux", "would suppress extra local hair", "OPEN_SECTOR_BY_SECTOR", "field-specific operators/signs/source charges not supplied for all MTS sectors"),
        ("EUL2749_6_boundary_reference", "theta_MTS and Q_tau pieces fixed before readout", "would prevent hidden mass/source counterterm", "OPEN_BOUNDARY_CHARGE", "1008 says parent theta/Q_tau total is not extracted"),
    ]
    return [nonclaim({"same_parent_branch_id": BRANCH_ID, "gate_id": gid, "variation_test": test, "conditional_result": result, "status": status, "blocking_issue": block}) for gid, test, result, status, block in specs]


def ward_rows() -> list[dict[str, Any]]:
    specs = [
        ("WPPN2749_0_Noether", "J_tau = theta_MTS(L_tau Phi) - i_tau L_parent", "available for an explicit diffeomorphism-covariant action", "CONDITIONAL_PASS_TEMPLATE", "theta_MTS and all Q_tau pieces remain unextracted"),
        ("WPPN2749_1_qR", "R_AB=0 -> q_R=0 -> gamma-1=0", "formal if lambda_R sector is accepted as parent-owned and stress-silent", "CONDITIONAL_UNSIGNED", "lambda_R parent-origin and stress-silence theorem missing"),
        ("WPPN2749_2_beta", "EH second-order weak-field -> beta=1", "formal in EH core after source/readout is owned", "CONDITIONAL_UNSIGNED", "MTS source charge, Pi_M/Hilbert equality, and boundary reference still open"),
        ("WPPN2749_3_Bianchi", "diffeomorphism invariance -> Bianchi/Ward conservation identity", "formal for the complete action", "CONDITIONAL_UNSIGNED", "full MTS retained-sector action is not explicit"),
        ("WPPN2749_4_no_extra_modes", "extra sectors are topological/exact/positive-mass silent or bounded", "conditional route from 506 exists", "OPEN_SECTOR_QUEUE", "every MTS sector needs its own operator/source/boundary certificate"),
        ("WPPN2749_5_local_claim", "q_R=0 and delta_beta=0 as MTS prediction", "not reached", "BLOCKED_NO_CLAIM", "ansatz is not adopted as the current parent theory"),
    ]
    return [nonclaim({"same_parent_branch_id": BRANCH_ID, "gate_id": gid, "ward_or_ppn_test": test, "conditional_result": result, "status": status, "blocking_issue": block}) for gid, test, result, status, block in specs]


def adoption_rows() -> list[dict[str, Any]]:
    specs = [
        ("ADOPT2749_0_lambda_origin", "lambda_R parent origin", "MISSING_PARENT_ORIGIN", "without this the q_R zero is a closure multiplier"),
        ("ADOPT2749_1_lambda_stress", "lambda_R zero-stress/reaction-stress theorem", "MISSING_STRESS_SILENCE", "constraint can otherwise alter local metric/source equations"),
        ("ADOPT2749_2_MTS_matching", "EH/readout blocks matched to MTS primitives", "MISSING_SYMBOL_MATCH", "EH core cannot simply be imported as the finished MTS parent action"),
        ("ADOPT2749_3_source_charge", "Pi_M/Hilbert/Hamiltonian source charge equality", "MISSING_SOURCE_CHARGE_GLUE", "measured GM and beta readout are not parent-owned"),
        ("ADOPT2749_4_boundary", "theta/Q_tau/boundary reference fixed before readout", "MISSING_PARENT_CURRENT_CHAIN", "boundary counterterms can hide calibration"),
        ("ADOPT2749_5_extra_silence", "all non-EH MTS sectors silent or bounded", "MISSING_SECTOR_CERTIFICATES", "local PPN residuals can re-enter through extra sectors"),
        ("ADOPT2749_6_verdict", "ansatz adoption", "NOT_ADOPTED_CURRENT_MTS_DERIVATION", "best ansatz is a repair target, not a claim"),
    ]
    return [nonclaim({"same_parent_branch_id": BRANCH_ID, "adoption_id": aid, "requirement": req, "status": status, "why_it_blocks": why}) for aid, req, status, why in specs]


def runner_rows() -> list[dict[str, Any]]:
    specs = [
        ("RUN2749_0_sources", "action ansatz sources and prior gates loaded", "PASS", "2748 contract plus 511/512/505/506/537/538/1008 action-route evidence loaded"),
        ("RUN2749_1_best_ansatz", "minimal ansatz construction", "PASS_CONDITIONAL_NOT_ADOPTED", "EH + universal matter + lambda_R R_AB + silent sectors is the cleanest conditional ansatz"),
        ("RUN2749_2_qR_gate", "q_R zero gate", "FORMAL_PASS_BLOCKED_BY_LAMBDAR_ORIGIN_AND_STRESS", "delta lambda_R gives R_AB=0, but parent-origin and zero-stress certificates are missing"),
        ("RUN2749_3_beta_gate", "delta_beta zero gate", "CONDITIONAL_EH_PASS_BLOCKED_BY_SOURCE_CHARGE_AND_ADOPTION", "EH weak-field gives beta=1 only after source/readout/PiM and boundary chain are parent-owned"),
        ("RUN2749_4_claim", "local GR/Newton claim", "BLOCKED_NO_CLAIM", "ansatz is a repair candidate, not a signed MTS parent action"),
    ]
    return [nonclaim({"same_parent_branch_id": BRANCH_ID, "runner_id": rid, "test": test, "current_status": status, "detail": detail}) for rid, test, status, detail in specs]


def gate_rows() -> list[dict[str, Any]]:
    specs = [
        ("GATE2749_0_ansatz", "minimal ansatz as current MTS parent action", "BLOCKED_NO_CLAIM", "not adopted; parent-origin and symbol matching open"),
        ("GATE2749_1_qR", "q_R=0 parent prediction", "BLOCKED_NO_CLAIM", "lambda_R origin/stress gates fail"),
        ("GATE2749_2_beta", "delta_beta=0 parent prediction", "BLOCKED_NO_CLAIM", "source charge/PiM/boundary and MTS adoption gates fail"),
        ("GATE2749_3_matter", "universal matter/coframe descent", "BLOCKED_NO_CLAIM", "matter action descent remains open"),
        ("GATE2749_4_extra", "extra-sector silence", "BLOCKED_NO_CLAIM", "sector-by-sector silence certificates missing"),
        ("GATE2749_5_local_GR", "derived local GR/Newton reduction", "BLOCKED_NO_CLAIM", "bounded closure lane remains the honest status"),
    ]
    return [nonclaim({"claim_gate_id": gid, "claim_gate": gate, "status": status, "reason": reason}) for gid, gate, status, reason in specs]


def decision_rows() -> list[dict[str, Any]]:
    specs = [
        ("DEC2749_0_verdict", "minimal parent weak-field ansatz", "BEST_CONDITIONAL_ANSATZ_WRITTEN_NOT_ADOPTED", "the ansatz can formally sign q_R/beta only if lambda_R and EH/source/readout sectors are parent-owned and stress-silent; those gates remain open"),
        ("DEC2749_1_branch_status", "local branch", "BOUNDED_CLOSURE_CONTROL_REMAINS", "the ansatz is a repair route, not evidence that current MTS already derives local GR"),
        ("DEC2749_2_next", "next target", "NEXT_2750_LAMBDAR_PARENT_ORIGIN_ZERO_STRESS_TEST", "the hinge is now lambda_R: either derive it as a legitimate parent constraint with no local stress leakage, or keep q_R bounded closure"),
    ]
    return [nonclaim({"decision_id": did, "decision": decision, "result": result, "reason": reason}) for did, decision, result, reason in specs]


def next_rows() -> list[dict[str, Any]]:
    return [
        nonclaim(
            {
                "next_id": "NEXT2749_0_2750",
                "status": "selected_primary",
                "target_doc": "2750-Y5-R2FR-lambdaR-parent-origin-zero-stress-and-first-class-constraint-test-under-AX1090.md",
                "target_script": "scripts/Y5_R2FR_lambdaR_parent_origin_zero_stress_and_first_class_constraint_test_under_AX1090_2750.py",
                "mission": "test whether lambda_R R_AB can be derived as a parent-owned first-class/auxiliary constraint with zero local stress and proper boundary charge; if not, keep q_R=0 as closure-only and use the bounded PPN runner",
                "acceptance": "accept lambda_R only with parent-origin, zero-stress/reaction-stress, boundary charge, degree-count, and matter-readout clauses; otherwise reject as closure-only",
                "forbidden": "do not accept lambda_R as derivation merely because variation gives R_AB=0; do not claim local GR/Newton reduction; do not edit formalization-workbench",
                "selected": True,
            }
        )
    ]


def branch_rows() -> list[dict[str, Any]]:
    return [
        nonclaim({"copy_id": "BR2749_0_ansatz", "source_table": rel(OUTPUTS["ansatz"]), "copy_path": rel(BRANCH_OUTPUTS["ansatz"]), "purpose": "source-weight minimal weak-field action ansatz", "exists": BRANCH_OUTPUTS["ansatz"].exists()}),
        nonclaim({"copy_id": "BR2749_1_ward", "source_table": rel(OUTPUTS["ward"]), "copy_path": rel(BRANCH_OUTPUTS["ward"]), "purpose": "local-bound Euler/Ward/PPN gate", "exists": BRANCH_OUTPUTS["ward"].exists()}),
        nonclaim({"copy_id": "BR2749_2_next_queue", "source_table": rel(OUTPUTS["next"]), "copy_path": rel(BRANCH_OUTPUTS["next_queue"]), "purpose": "RAB acquisition queue for lambda_R origin/stress test", "exists": BRANCH_OUTPUTS["next_queue"].exists()}),
    ]


def formalization_recent_count() -> int:
    if not FORMALIZATION.exists():
        return 0
    start = SCRIPT_START_UTC.timestamp()
    return sum(1 for path in FORMALIZATION.rglob("*") if path.is_file() and path.stat().st_mtime >= start)


def pycache_path() -> Path:
    return Path(__file__).resolve().parent / "__pycache__"


def remove_pycache() -> None:
    pycache = pycache_path()
    if pycache.exists():
        shutil.rmtree(pycache)


def validation_rows(
    sources: list[dict[str, Any]],
    ansatz: list[dict[str, Any]],
    euler: list[dict[str, Any]],
    ward: list[dict[str, Any]],
    adoption: list[dict[str, Any]],
    runner: list[dict[str, Any]],
    gates: list[dict[str, Any]],
    next_target: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    source_ok = all(row["exists"] is True and row["needles_present"] is True for row in sources)
    ansatz_ok = any(row["ansatz_id"] == "ANS2749_A_EH_lambdaR_silent" and row["adoption_status"] == "BEST_CONDITIONAL_ANSATZ_NOT_ADOPTED" for row in ansatz)
    euler_ok = any(row["gate_id"] == "EUL2749_1_lambda_variation" and row["status"] == "FORMAL_PASS_IF_LAMBDAR_PARENT_OWNED" for row in euler) and any(row["gate_id"] == "EUL2749_2_lambda_stress" and row["status"] == "FAIL_UNSIGNED_STRESS_SILENCE" for row in euler)
    ward_ok = any(row["gate_id"] == "WPPN2749_1_qR" and row["status"] == "CONDITIONAL_UNSIGNED" for row in ward) and any(row["gate_id"] == "WPPN2749_5_local_claim" and row["status"] == "BLOCKED_NO_CLAIM" for row in ward)
    adoption_ok = any(row["adoption_id"] == "ADOPT2749_6_verdict" and row["status"] == "NOT_ADOPTED_CURRENT_MTS_DERIVATION" for row in adoption)
    runner_ok = any(row["runner_id"] == "RUN2749_2_qR_gate" and "BLOCKED_BY_LAMBDAR" in row["current_status"] for row in runner)
    gates_ok = len(gates) == 6 and all(row["status"] == "BLOCKED_NO_CLAIM" for row in gates)
    no_claim_flags_ok = all(row.get("valid_for_claim") is False and row.get("claim_allowed") is False for block in [ansatz, euler, ward, adoption, runner, gates] for row in block)
    next_ok = next_target[0]["selected"] is True and "2750" in next_target[0]["target_doc"] and "lambdaR" in next_target[0]["target_doc"]
    branch_ok = all(path.exists() for path in BRANCH_OUTPUTS.values())
    pycache_ok = not pycache_path().exists()
    formalization_count = formalization_recent_count()
    formalization_ok = formalization_count == 0
    csv_ok = True
    csv_bits: list[str] = []
    for key, path in {**OUTPUTS, **BRANCH_OUTPUTS}.items():
        if key == "validation":
            continue
        try:
            rows = read_csv(path)
            csv_bits.append(f"{path.name}:{len(rows)}:ok")
        except Exception as exc:
            csv_ok = False
            csv_bits.append(f"{path.name}:ERROR:{exc}")
    rows = [
        {"validation_id": "VAL2749_0_sources", "passed": source_ok, "detail": "all source paths exist and required anchors/needles are present", "timestamp_utc": ts()},
        {"validation_id": "VAL2749_1_best_ansatz", "passed": ansatz_ok, "detail": "best conditional ansatz written but not adopted", "timestamp_utc": ts()},
        {"validation_id": "VAL2749_2_euler_lambda", "passed": euler_ok, "detail": "lambda variation formal q_R gate and stress failure recorded", "timestamp_utc": ts()},
        {"validation_id": "VAL2749_3_ward_ppn", "passed": ward_ok, "detail": "q_R/beta gate is conditional unsigned and local claim blocked", "timestamp_utc": ts()},
        {"validation_id": "VAL2749_4_adoption_blocks", "passed": adoption_ok, "detail": "adoption rejection ledger complete", "timestamp_utc": ts()},
        {"validation_id": "VAL2749_5_runner_claim_block", "passed": runner_ok, "detail": "runner blocks local claim through lambda_R origin/stress gates", "timestamp_utc": ts()},
        {"validation_id": "VAL2749_6_claim_gates", "passed": gates_ok and no_claim_flags_ok, "detail": "all claim gates remain blocked and flags false", "timestamp_utc": ts()},
        {"validation_id": "VAL2749_7_next_target", "passed": next_ok, "detail": "next target is lambda_R parent-origin zero-stress test", "timestamp_utc": ts()},
        {"validation_id": "VAL2749_8_branch_outputs", "passed": branch_ok, "detail": "branch copies exist", "timestamp_utc": ts()},
        {"validation_id": "VAL2749_9_csv_parse", "passed": csv_ok, "detail": "; ".join(csv_bits), "timestamp_utc": ts()},
        {"validation_id": "VAL2749_10_pycache_absent", "passed": pycache_ok, "detail": f"scripts __pycache__ absent={pycache_ok}", "timestamp_utc": ts()},
        {"validation_id": "VAL2749_11_formalization_untouched", "passed": formalization_ok, "detail": f"formalization-workbench recent modified-file count since script start = {formalization_count}", "timestamp_utc": ts()},
    ]
    rows.append(
        {
            "validation_id": "VAL2749_OVERALL",
            "passed": all(row["passed"] is True for row in rows),
            "detail": "2749 writes the minimal parent weak-field action ansatz, gates Euler/Ward/PPN conditions, and selects lambda_R origin/stress next",
            "timestamp_utc": ts(),
        }
    )
    return rows


def write_doc(data: dict[str, list[dict[str, Any]]]) -> None:
    DOC.write_text(
        f"""# 2749 - Y5 R2/f(R): Minimal Parent Weak-Field Action Ansatz And Euler/Ward/PPN Gate Under AX1090

Status: `Y5_R2FR_2749_best_conditional_ansatz_written_not_adopted_lambdar_gate_next`

## Private Verdict

2749 writes the minimal repair ansatz:

`S_parent = S_EH[g_obs] + S_matter[g_obs,psi] + int sqrt(-g) lambda_R R_AB + S_silent[Phi,g_obs] + S_boundary`.

It formally gives `R_AB=0` through `delta lambda_R`, and conditionally gives `beta=1` through the EH weak-field core.

But it is not adopted as the current MTS parent theory. `lambda_R` still lacks parent origin and zero-stress/reaction-stress proof. Source/Pi_M charge ownership, boundary current extraction, universal matter descent, and extra-sector silence also remain open.

The next hinge is narrow and sharp: can `lambda_R R_AB` be a legitimate parent-owned first-class/auxiliary constraint, or is it just the closure axiom wearing a better coat?

## Source Register

{markdown_table(data["sources"], ["source_id", "description", "source_path", "exists", "needles_present", "missing_needles", "valid_for_claim"])}

## Minimal Action Ansatz Register

{markdown_table(data["ansatz"], ["ansatz_id", "candidate_parent_action", "what_it_derives_conditionally", "what_blocks_adoption", "adoption_status", "valid_for_claim"])}

## Euler Variation Gate

{markdown_table(data["euler"], ["gate_id", "variation_test", "conditional_result", "status", "blocking_issue", "valid_for_claim"])}

## Ward/PPN Gate

{markdown_table(data["ward"], ["gate_id", "ward_or_ppn_test", "conditional_result", "status", "blocking_issue", "valid_for_claim"])}

## Adoption/Rejection Ledger

{markdown_table(data["adoption"], ["adoption_id", "requirement", "status", "why_it_blocks", "valid_for_claim"])}

## Runner

{markdown_table(data["runner"], ["runner_id", "test", "current_status", "detail", "valid_for_claim"])}

## Claim Gates

{markdown_table(data["gates"], ["claim_gate_id", "claim_gate", "status", "reason", "valid_for_claim"])}

## Decision Ledger

{markdown_table(data["decisions"], ["decision_id", "decision", "result", "reason", "valid_for_claim"])}

## Next Target

{markdown_table(data["next"], ["next_id", "status", "target_doc", "target_script", "mission", "acceptance", "forbidden", "selected", "valid_for_claim"])}

## Branch Copies

{markdown_table(data["branches"], ["copy_id", "source_table", "copy_path", "purpose", "exists", "valid_for_claim"])}

## Validation

{markdown_table(data["validation"], ["validation_id", "passed", "detail", "timestamp_utc"])}

## Plain-English Read

This is progress with teeth. We now know the cleanest minimal action that would make the local GR lane work. We also know exactly why it is not yet a win: the `lambda_R` constraint has to be derived as a real parent object with no hidden stress or boundary cheat. That is the next lock to pick.
""",
        encoding="utf-8",
    )


def main() -> None:
    ensure_dirs()
    sources = source_rows()
    ansatz = ansatz_rows()
    euler = euler_rows()
    ward = ward_rows()
    adoption = adoption_rows()
    runner = runner_rows()
    gates = gate_rows()
    decisions = decision_rows()
    next_target = next_rows()

    write_csv(OUTPUTS["sources"], sources)
    write_csv(OUTPUTS["ansatz"], ansatz)
    write_csv(OUTPUTS["euler"], euler)
    write_csv(OUTPUTS["ward"], ward)
    write_csv(OUTPUTS["adoption"], adoption)
    write_csv(OUTPUTS["runner"], runner)
    write_csv(OUTPUTS["gates"], gates)
    write_csv(OUTPUTS["decisions"], decisions)
    write_csv(OUTPUTS["next"], next_target)

    write_csv(BRANCH_OUTPUTS["ansatz"], ansatz)
    write_csv(BRANCH_OUTPUTS["ward"], ward)
    write_csv(BRANCH_OUTPUTS["next_queue"], next_target)
    branches = branch_rows()
    write_csv(OUTPUTS["branches"], branches)

    remove_pycache()
    validation = validation_rows(sources, ansatz, euler, ward, adoption, runner, gates, next_target)
    write_csv(OUTPUTS["validation"], validation)

    data = {
        "sources": sources,
        "ansatz": ansatz,
        "euler": euler,
        "ward": ward,
        "adoption": adoption,
        "runner": runner,
        "gates": gates,
        "decisions": decisions,
        "next": next_target,
        "branches": branches,
        "validation": validation,
    }
    write_doc(data)

    remove_pycache()

    if not all(row["passed"] is True for row in validation):
        failed = [row for row in validation if row["passed"] is not True]
        raise SystemExit(f"2749 validation failed: {failed}")
    print(f"wrote {DOC}")
    print(f"validation {OUTPUTS['validation']}")


if __name__ == "__main__":
    main()

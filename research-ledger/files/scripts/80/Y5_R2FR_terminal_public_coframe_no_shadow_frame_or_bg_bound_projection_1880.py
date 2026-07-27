from __future__ import annotations

import csv
import shutil
from pathlib import Path
from typing import Any


BRANCH_ID = "MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428"
CHECKPOINT_ID = "1880"

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "source-intake" / "mts_residuals"
MICROSCOPE_RESIDUALS = ROOT / "source-intake" / "microscope" / "branch_locked_wep" / "residuals"
QUARANTINE = ROOT / "source-intake" / "microscope" / "quarantine" / CHECKPOINT_ID
QUEUE = ROOT / "source-intake" / "rab-sector" / "acquisition-queue"
FORMALIZATION = ROOT.parent / "formalization-workbench"

DOC = ROOT / "1880-Y5-R2FR-terminal-public-coframe-no-shadow-frame-or-bg-bound-projection.md"

INPUTS = {
    "1879_doc": ROOT / "1879-Y5-R2FR-parent-coframe-ownership-or-common-frame-leak-bound.md",
    "1879_validation": OUT / "P8_Y5_BRR545_1879_VALIDATION.csv",
    "1879_next": OUT / "P8_Y5_PARENT_QLOC_1879_NEXT_TARGET.csv",
    "1879_no_shadow": OUT / "P8_Y5_PARENT_QLOC_1879_NO_SHADOW_FRAME_TESTS.csv",
    "1879_leak_rows": OUT / "P8_Y5_PARENT_QLOC_1879_COMMON_FRAME_LEAK_BOUND_ROWS.csv",
    "1879_arena_interface": OUT / "P8_Y5_PARENT_QLOC_1879_ARENA_BOUND_INTERFACE.csv",
    "1740_doc": ROOT / "1740-Y5-R2FR-no-shadow-frame-zero-or-bg-bound-projection-map.md",
    "1030_spm_gate": ROOT / "1030-Y5-R10-single-public-metric-parent-action-derivation-or-cg-provenance-gate.md",
}

SOURCE_NEEDLES = {
    "1879_doc": [
        "b_R, d_R, w_R, epsilon_endpoint_R, epsilon_common_frame_abs",
        "NO_SHADOW_TERMINAL_PUBLIC_METRIC_OR_BG_PROJECTION_SELECTED_NEXT",
    ],
    "1879_validation": [
        "VAL1879_OVERALL,PASS",
    ],
    "1879_next": [
        "1880-Y5-R2FR-terminal-public-coframe-no-shadow-frame-or-bg-bound-projection.md",
        "selected",
    ],
    "1879_no_shadow": [
        "NO_SHADOW_FRAME_NOT_DERIVED_CURRENT_CORPUS",
        "FAILS_UNCONDITIONAL_DERIVATION",
    ],
    "1879_leak_rows": [
        "CFL1879_0_bR",
        "MISSING_ABSOLUTE_ENVELOPE",
    ],
    "1879_arena_interface": [
        "BLOCKED_NONCLAIM_WRONG_ROUTE_GUARD",
        "R10 finite range",
    ],
    "1740_doc": [
        "NO_SHADOW_FRAME_THEOREM_NOT_SIGNED",
        "BOUND_PROJECTION_MAP_STAGED_NONCLAIM",
    ],
    "1030_spm_gate": [
        "EXACT_CLOSURE_CLAUSE_NOT_DERIVED",
        "Covariance, WEP, and Ward identities do not derive the single public metric",
    ],
}

OUTPUTS = {
    "source_register": OUT / "P8_Y5_PARENT_QLOC_1880_SOURCE_REGISTER.csv",
    "terminal_coframe_gate": OUT / "P8_Y5_PARENT_QLOC_1880_TERMINAL_PUBLIC_COFRAME_GATE.csv",
    "zero_theorem_attempt": OUT / "P8_Y5_PARENT_QLOC_1880_NO_SHADOW_ZERO_THEOREM_ATTEMPT.csv",
    "projection_contracts": OUT / "P8_Y5_PARENT_QLOC_1880_COMMON_FRAME_PROJECTION_CONTRACTS.csv",
    "bound_input_rows": OUT / "P8_Y5_PARENT_QLOC_1880_BOUND_INPUT_ROWS_NONCLAIM.csv",
    "runner_refusal": OUT / "P8_Y5_PARENT_QLOC_1880_RUNNER_REFUSAL.csv",
    "claim_gate": OUT / "P8_Y5_PARENT_QLOC_1880_CLAIM_GATE.csv",
    "decision": OUT / "P8_Y5_PARENT_QLOC_1880_DECISION_LEDGER.csv",
    "next_target": OUT / "P8_Y5_PARENT_QLOC_1880_NEXT_TARGET.csv",
    "validation": OUT / "P8_Y5_BRR545_1880_VALIDATION.csv",
}


def ensure_dirs() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    MICROSCOPE_RESIDUALS.mkdir(parents=True, exist_ok=True)
    QUARANTINE.mkdir(parents=True, exist_ok=True)
    QUEUE.mkdir(parents=True, exist_ok=True)


def bool_string(value: Any) -> str:
    return str(value).strip().lower()


def path_has_needles(path: Path, needles: list[str]) -> tuple[bool, str]:
    if not path.exists():
        return False, "MISSING_SOURCE_PATH"
    text = path.read_text(encoding="utf-8", errors="ignore")
    missing = [needle for needle in needles if needle not in text]
    if missing:
        return False, "MISSING_NEEDLES=" + ";".join(missing)
    return True, "OK"


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    if not rows:
        raise ValueError(f"no rows for {path}")
    path.parent.mkdir(parents=True, exist_ok=True)
    fieldnames: list[str] = []
    for row in rows:
        for key in row:
            if key not in fieldnames:
                fieldnames.append(key)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()
        for row in rows:
            writer.writerow(row)


def csv_rows(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def source_register_rows() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for source_id, path in INPUTS.items():
        ok, detail = path_has_needles(path, SOURCE_NEEDLES[source_id])
        rows.append(
            {
                "branch_id": BRANCH_ID,
                "checkpoint_id": CHECKPOINT_ID,
                "source_id": source_id,
                "source_path": str(path),
                "required_needles": " ; ".join(SOURCE_NEEDLES[source_id]),
                "source_exists": path.exists(),
                "needle_check": detail,
                "usable_for_1880": ok,
                "valid_for_claim": False,
                "claim_allowed": False,
            }
        )
    return rows


def terminal_coframe_gate_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "gate_id": "TPC1880_0_terminal_object",
            "clause": "ordinary observables have a terminal public coframe object",
            "mathematical_requirement": "all ordinary matter/readout maps factor through e_pub=E(Q_vis), with no extra matter-frame argument",
            "current_status": "TERMINAL_PUBLIC_COFRAME_NOT_PARENT_DERIVED",
            "if_closed": "no independent A_R(C_R) or B_R(C_R) slot exists",
            "proof_closed": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "gate_id": "TPC1880_1_no_C_argument",
            "clause": "C_R/J_q is not a readout or matter-domain argument",
            "mathematical_requirement": "Allowed[S_matter] excludes A_R(C_R), B_R(C_R), w_A(C_R), and E(Q_vis,C_R)",
            "current_status": "NO_EXTRA_FRAME_SLOT_CLOSURE_ONLY",
            "if_closed": "b_R=d_R=w_R=0 by action-domain exclusion",
            "proof_closed": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "gate_id": "TPC1880_2_connection_source",
            "clause": "connection/source/tau/boundary are inherited from the same public coframe domain",
            "mathematical_requirement": "omega[e_pub], source support, tau, endpoint and boundary maps cannot choose a different frame",
            "current_status": "INHERITANCE_STACK_UNSIGNED",
            "if_closed": "prevents no-shadow theorem from being reopened after metric readout",
            "proof_closed": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "gate_id": "TPC1880_3_verdict",
            "clause": "terminal public coframe excludes shadow frame",
            "mathematical_requirement": "TPC1880_0 through TPC1880_2 parent-signed in the same action branch",
            "current_status": "TERMINAL_PUBLIC_COFRAME_NO_SHADOW_NOT_DERIVED",
            "if_closed": "return b_R/d_R/w_R to theorem-zero route",
            "proof_closed": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]


def zero_theorem_attempt_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "theorem_id": "ZTH1880_0_exact_conditional",
            "statement": "If ordinary matter/readout has terminal public coframe e_pub=E(Q_vis), and the parent action domain has no C_R/J_q Weyl, disformal, source-prefactor, endpoint, or post-readout frame slot, then b_R=d_R=w_R=epsilon_endpoint_R=0.",
            "proof_status": "EXACT_CONDITIONAL_THEOREM",
            "missing_for_current_claim": "parent terminal-object derivation; no-extra-frame action-domain proof; connection/source/tau/boundary inheritance",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "theorem_id": "ZTH1880_1_shortcut_rejection",
            "statement": "Covariance, WEP, and Ward conservation do not by themselves exclude a universal hidden frame or source-weight current.",
            "proof_status": "SHORTCUTS_REJECTED",
            "missing_for_current_claim": "actual parent action domain exclusion, not symmetry slogans",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "theorem_id": "ZTH1880_2_current_verdict",
            "statement": "Current MTS proves terminal public coframe/no-shadow-frame zero.",
            "proof_status": "NO_SHADOW_ZERO_NOT_DERIVED_CURRENT_CORPUS",
            "missing_for_current_claim": "TPC1880_0;TPC1880_1;TPC1880_2",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "theorem_id": "ZTH1880_3_fallback",
            "statement": "If no-shadow zero is unsigned, common-frame coefficients must be projected into local empirical arenas before any score.",
            "proof_status": "BOUND_PROJECTION_REQUIRED_NONCLAIM",
            "missing_for_current_claim": "numeric coefficients, units, source paths, response kernels and accepted arena bounds",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]


def projection_contract_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "projection_id": "PRC1880_0_PPN_metric",
            "arena": "PPN_metric",
            "observable": "gamma_minus_1; beta_minus_1",
            "mapping_contract": "|Delta_PPN_metric| <= K_gamma_bR |b_R| + K_gamma_wR |w_R| + K_gamma_endpoint |epsilon_endpoint_R| plus massless tail terms",
            "required_inputs": "b_R;w_R;epsilon_endpoint_R;q_R_hat;tau_PPN;source denominator;no-cancellation envelope",
            "current_status": "MISSING_RESPONSE_KERNEL_AND_COEFFICIENTS",
            "score_ready": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "projection_id": "PRC1880_1_PPN_preferred",
            "arena": "PPN_preferred_frame",
            "observable": "alpha1; alpha2; alpha3; xi",
            "mapping_contract": "|alpha_i| <= K_i_dR |d_R| + K_i_tau |Delta tau| + K_i_boundary |epsilon_endpoint_R|",
            "required_inputs": "d_R;tau_pushforward;boundary endpoint;preferred-frame response kernels",
            "current_status": "MISSING_RESPONSE_KERNEL_AND_COEFFICIENTS",
            "score_ready": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "projection_id": "PRC1880_2_clock_WEP",
            "arena": "clock_WEP_material",
            "observable": "Delta nu/nu; eta_AB; material differential residual",
            "mapping_contract": "|clock/WEP| <= K_clock_bR |b_R| + K_clock_wR |w_R| + K_material |Delta theta|",
            "required_inputs": "b_R;w_R;material sensitivities;constant-marker rows;tau_clock;tau_WEP",
            "current_status": "MISSING_RESPONSE_KERNEL_AND_COEFFICIENTS",
            "score_ready": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "projection_id": "PRC1880_3_orbital",
            "arena": "orbital_light_time",
            "observable": "precession;acceleration;light-time residual",
            "mapping_contract": "|Delta_orbit| <= K_orb_bR |b_R| + K_orb_dR |d_R| + K_orb_endpoint |epsilon_endpoint_R|",
            "required_inputs": "b_R;d_R;epsilon_endpoint_R;tau_orbital;same-frame mass/source denominator",
            "current_status": "MISSING_RESPONSE_KERNEL_AND_COEFFICIENTS",
            "score_ready": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "projection_id": "PRC1880_4_R10_guarded",
            "arena": "R10_finite_range",
            "observable": "alpha(lambda)",
            "mapping_contract": "alpha_R(lambda) may include w_R or source-leg factors only after Z_R,M_R^2,lambda_R,beta_source,beta_test,tau_R10 and accepted bound curve exist",
            "required_inputs": "finite operator/range/source/test/projection rows first; common-frame leak is not a range substitute",
            "current_status": "MISSING_FINITE_ROUTE_INPUTS_WRONG_ROUTE_GUARD_ACTIVE",
            "score_ready": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]


def bound_input_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "row_id": "BIN1880_0_coefficients",
            "quantity": "b_R,d_R,w_R,epsilon_endpoint_R,epsilon_common_frame_abs",
            "needed_before_score": "numeric value or theorem-zero certificate, units, source_path, normalization frame",
            "current_status": "MISSING_NUMERIC_COEFFICIENTS_OR_THEOREM_ZERO",
            "valid_for_claim": False,
            "claim_allowed": False,
            "score_ready": False,
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "BIN1880_1_response_kernels",
            "quantity": "K_gamma,K_preferred,K_clock,K_WEP,K_orbital,K_R10",
            "needed_before_score": "source-backed arena response matrix with no cross-arena transfer by assertion",
            "current_status": "MISSING_RESPONSE_KERNELS",
            "valid_for_claim": False,
            "claim_allowed": False,
            "score_ready": False,
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "BIN1880_2_bounds",
            "quantity": "accepted PPN/WEP/clock/orbital/R10 bound rows",
            "needed_before_score": "source-backed bounds and declared comparison convention",
            "current_status": "MISSING_ACCEPTED_BOUND_SET_FOR_THIS_BRANCH",
            "valid_for_claim": False,
            "claim_allowed": False,
            "score_ready": False,
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "BIN1880_3_baseline",
            "quantity": "GR/PPN baseline under same readout assumptions",
            "needed_before_score": "same pipeline baseline and no-cancellation envelope",
            "current_status": "MISSING_BASELINE_AND_NO_CANCELLATION_GUARD",
            "valid_for_claim": False,
            "claim_allowed": False,
            "score_ready": False,
        },
    ]


def runner_refusal_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "runner_id": "RUN1880_0_local_bound_runner",
            "runner": "future common-frame local bound runner",
            "current_status": "REFUSE_CLAIM_RUN",
            "reason": "coefficients, response kernels, accepted bounds, baseline and no-cancellation envelope are missing",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "runner_id": "RUN1880_1_R10_runner",
            "runner": "future R10 alpha(lambda) runner",
            "current_status": "REFUSE_CLAIM_RUN_WRONG_ROUTE_GUARD",
            "reason": "R10 still requires finite Z_R/M_R^2/lambda/source/test/projection rows; common-frame leak cannot be routed into alpha(lambda) alone",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]


def claim_gate_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "claim_id": "CG1880_0_internal",
            "claim": "1880 no-shadow theorem/projection contract may guide next work",
            "status": "ALLOW_INTERNAL_NONCLAIM_CONTRACT",
            "reason": "the theorem is conditional and projection contracts are blocked",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "claim_id": "CG1880_1_zero",
            "claim": "b_R=d_R=w_R=epsilon_endpoint_R=0 by terminal public coframe",
            "status": "BLOCKED",
            "reason": "terminal public coframe/no-extra-frame clause is not parent-derived",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "claim_id": "CG1880_2_projection_score",
            "claim": "finite common-frame leak is below local bounds",
            "status": "BLOCKED",
            "reason": "coefficients, response kernels, accepted bounds and baselines are missing",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "claim_id": "CG1880_3_local_GR",
            "claim": "local GR/Newton is derived from no-shadow coframe",
            "status": "BLOCKED",
            "reason": "no-shadow is not derived and is not sufficient without beta/conservation/source closure",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "decision_id": "DEC1880_0_zero",
            "decision": "TERMINAL_PUBLIC_COFRAME_NO_SHADOW_NOT_DERIVED",
            "basis": "the exclusion clause is exact as a contract but not parent-derived in the current corpus",
            "consequence": "do not promote b_R/d_R/w_R zero theorem",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "decision_id": "DEC1880_1_projection",
            "decision": "COMMON_FRAME_PROJECTION_CONTRACTS_READY_NONCLAIM",
            "basis": "PPN, WEP/clock, orbital and R10 guard formulas now name required kernels and missing inputs",
            "consequence": "next empirical work can source one response kernel without pretending a score",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "decision_id": "DEC1880_2_next",
            "decision": "FIRST_RESPONSE_KERNEL_OR_PARENT_ACTION_CLAUSE_SELECTED_NEXT",
            "basis": "either find a parent action clause that excludes shadow slots, or fill the first source-backed projection kernel",
            "consequence": "1881 should target one concrete PPN/WEP/clock response map or the missing parent action clause",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "route_id": "NEXT1880_0_primary",
            "target_doc": "1881-Y5-R2FR-first-common-frame-response-kernel-or-parent-action-clause.md",
            "target_script": "scripts/Y5_R2FR_first_common_frame_response_kernel_or_parent_action_clause_1881.py",
            "objective": "source or derive one concrete response kernel for b_R/d_R/w_R into PPN, WEP, clock, or orbital bounds; alternatively find the parent action clause that excludes shadow-frame slots.",
            "selection_status": "selected",
            "success_condition": "one source-backed response-kernel row or a parent action no-shadow clause; no scores unless coefficients and bounds also exist.",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "route_id": "NEXT1880_1_R10_later",
            "target_doc": "1881b-Y5-R2FR-R10-common-frame-source-leg-after-finite-range-inputs.md",
            "target_script": "scripts/Y5_R2FR_R10_common_frame_source_leg_after_finite_range_inputs_1881b.py",
            "objective": "only after finite range/operator rows exist, map common-frame source-leg terms into R10 alpha(lambda).",
            "selection_status": "held_later",
            "success_condition": "R10 route remains blocked until Z_R/M_R^2/lambda/source/test/tau rows are sourced.",
            "valid_for_claim": False,
        },
    ]


def all_output_rows() -> dict[str, list[dict[str, Any]]]:
    return {
        "source_register": source_register_rows(),
        "terminal_coframe_gate": terminal_coframe_gate_rows(),
        "zero_theorem_attempt": zero_theorem_attempt_rows(),
        "projection_contracts": projection_contract_rows(),
        "bound_input_rows": bound_input_rows(),
        "runner_refusal": runner_refusal_rows(),
        "claim_gate": claim_gate_rows(),
        "decision": decision_rows(),
        "next_target": next_target_rows(),
    }


def all_claim_flags_false(paths: list[Path]) -> tuple[bool, str]:
    checked = 0
    for path in paths:
        for row_index, row in enumerate(csv_rows(path), start=2):
            for column in [
                "valid_for_claim",
                "claim_allowed",
                "proof_closed",
                "score_ready",
            ]:
                if column in row:
                    checked += 1
                    if bool_string(row[column]) == "true":
                        return False, f"{path.name}:{row_index}:{column}=true"
    return checked > 0, f"checked={checked}"


def missing_rows_not_ready(paths: list[Path]) -> tuple[bool, str]:
    checked = 0
    for path in paths:
        for row_index, row in enumerate(csv_rows(path), start=2):
            joined = " ".join(row.values())
            if "MISSING_" in joined:
                checked += 1
                for column in ["score_ready", "valid_for_claim", "claim_allowed"]:
                    if column in row and bool_string(row[column]) == "true":
                        return False, f"{path.name}:{row_index}:{column}=true_on_missing_row"
    return checked > 0, f"checked_missing_rows={checked}"


def csv_parse_check(paths: list[Path]) -> tuple[bool, str]:
    details: list[str] = []
    for path in paths:
        rows = csv_rows(path)
        if not rows:
            return False, f"EMPTY_CSV={path.name}"
        details.append(f"{path.name}:{len(rows)}")
    return True, ";".join(details)


def copy_branch_artifacts() -> None:
    for path in OUTPUTS.values():
        if path.name.endswith("_VALIDATION.csv"):
            continue
        shutil.copy2(path, MICROSCOPE_RESIDUALS / path.name)
        shutil.copy2(path, QUARANTINE / path.name)
    shutil.copy2(OUTPUTS["projection_contracts"], QUEUE / "JR1880_COMMON_FRAME_PROJECTION_CONTRACTS_NONCLAIM.csv")
    shutil.copy2(OUTPUTS["bound_input_rows"], QUEUE / "JR1880_BOUND_INPUT_ROWS_NONCLAIM.csv")
    shutil.copy2(OUTPUTS["next_target"], QUEUE / "JR1880_NEXT_TARGET_NONCLAIM.csv")


def remove_pycache() -> None:
    pycache = Path(__file__).resolve().parent / "__pycache__"
    if pycache.exists():
        shutil.rmtree(pycache)


def validation_rows() -> list[dict[str, Any]]:
    generated_without_validation = [path for key, path in OUTPUTS.items() if key != "validation"]
    rows_by_name = {key: csv_rows(path) for key, path in OUTPUTS.items() if key != "validation"}
    checks: list[dict[str, Any]] = []

    sources = rows_by_name["source_register"]
    checks.append(
        {
            "validation_id": "VAL1880_0_sources",
            "status": "PASS" if all(bool_string(row["usable_for_1880"]) == "true" for row in sources) else "FAIL",
            "detail": "1879/1740/1030 sources are available",
            "valid_for_claim": False,
        }
    )

    terminal = rows_by_name["terminal_coframe_gate"]
    checks.append(
        {
            "validation_id": "VAL1880_1_terminal_gate",
            "status": "PASS"
            if len(terminal) == 4
            and any(row["current_status"] == "TERMINAL_PUBLIC_COFRAME_NO_SHADOW_NOT_DERIVED" for row in terminal)
            and all(bool_string(row["proof_closed"]) == "false" for row in terminal)
            else "FAIL",
            "detail": "terminal public coframe gate remains unsigned",
            "valid_for_claim": False,
        }
    )

    theorem = rows_by_name["zero_theorem_attempt"]
    proof_statuses = {row["proof_status"] for row in theorem}
    checks.append(
        {
            "validation_id": "VAL1880_2_zero_theorem",
            "status": "PASS"
            if {
                "EXACT_CONDITIONAL_THEOREM",
                "SHORTCUTS_REJECTED",
                "NO_SHADOW_ZERO_NOT_DERIVED_CURRENT_CORPUS",
                "BOUND_PROJECTION_REQUIRED_NONCLAIM",
            }.issubset(proof_statuses)
            else "FAIL",
            "detail": "no-shadow zero theorem is exact conditional, shortcuts rejected, and fallback retained",
            "valid_for_claim": False,
        }
    )

    projections = rows_by_name["projection_contracts"]
    checks.append(
        {
            "validation_id": "VAL1880_3_projection_contracts",
            "status": "PASS"
            if len(projections) == 5
            and all(bool_string(row["score_ready"]) == "false" for row in projections)
            and any("WRONG_ROUTE_GUARD" in row["current_status"] for row in projections)
            else "FAIL",
            "detail": "projection contracts cover PPN, WEP/clock, orbital and guarded R10 routes",
            "valid_for_claim": False,
        }
    )

    bound_inputs = rows_by_name["bound_input_rows"]
    checks.append(
        {
            "validation_id": "VAL1880_4_bound_inputs",
            "status": "PASS"
            if len(bound_inputs) == 4
            and all("MISSING_" in row["current_status"] for row in bound_inputs)
            else "FAIL",
            "detail": "coefficients, kernels, bounds and baselines remain missing nonclaim inputs",
            "valid_for_claim": False,
        }
    )

    runners = rows_by_name["runner_refusal"]
    checks.append(
        {
            "validation_id": "VAL1880_5_runner_refusal",
            "status": "PASS"
            if all(row["current_status"].startswith("REFUSE_CLAIM_RUN") for row in runners)
            else "FAIL",
            "detail": "local and R10 runners refuse claim runs",
            "valid_for_claim": False,
        }
    )

    claims = rows_by_name["claim_gate"]
    checks.append(
        {
            "validation_id": "VAL1880_6_claim_gate",
            "status": "PASS"
            if any(row["status"] == "ALLOW_INTERNAL_NONCLAIM_CONTRACT" for row in claims)
            and all(bool_string(row["claim_allowed"]) == "false" for row in claims)
            else "FAIL",
            "detail": "only internal nonclaim contract is allowed",
            "valid_for_claim": False,
        }
    )

    decisions = rows_by_name["decision"]
    checks.append(
        {
            "validation_id": "VAL1880_7_decision",
            "status": "PASS"
            if any(row["decision"] == "TERMINAL_PUBLIC_COFRAME_NO_SHADOW_NOT_DERIVED" for row in decisions)
            and any(row["decision"] == "FIRST_RESPONSE_KERNEL_OR_PARENT_ACTION_CLAUSE_SELECTED_NEXT" for row in decisions)
            else "FAIL",
            "detail": "decision ledger selects first response kernel or parent action clause next",
            "valid_for_claim": False,
        }
    )

    next_targets = rows_by_name["next_target"]
    checks.append(
        {
            "validation_id": "VAL1880_8_next_target",
            "status": "PASS"
            if any(row["route_id"] == "NEXT1880_0_primary" and row["selection_status"] == "selected" for row in next_targets)
            else "FAIL",
            "detail": "1881 first response kernel or parent action clause target selected",
            "valid_for_claim": False,
        }
    )

    flags_ok, flags_detail = all_claim_flags_false(generated_without_validation)
    checks.append(
        {
            "validation_id": "VAL1880_9_claim_flags_false",
            "status": "PASS" if flags_ok else "FAIL",
            "detail": flags_detail,
            "valid_for_claim": False,
        }
    )

    missing_ok, missing_detail = missing_rows_not_ready(generated_without_validation)
    checks.append(
        {
            "validation_id": "VAL1880_10_missing_not_ready",
            "status": "PASS" if missing_ok else "FAIL",
            "detail": missing_detail,
            "valid_for_claim": False,
        }
    )

    parse_ok, parse_detail = csv_parse_check(generated_without_validation)
    checks.append(
        {
            "validation_id": "VAL1880_11_csv_parse",
            "status": "PASS" if parse_ok else "FAIL",
            "detail": parse_detail,
            "valid_for_claim": False,
        }
    )

    copied_paths = [
        MICROSCOPE_RESIDUALS / OUTPUTS["projection_contracts"].name,
        QUARANTINE / OUTPUTS["bound_input_rows"].name,
        QUEUE / "JR1880_COMMON_FRAME_PROJECTION_CONTRACTS_NONCLAIM.csv",
        QUEUE / "JR1880_BOUND_INPUT_ROWS_NONCLAIM.csv",
    ]
    checks.append(
        {
            "validation_id": "VAL1880_12_branch_copies",
            "status": "PASS" if all(path.exists() for path in copied_paths) else "FAIL",
            "detail": ";".join(str(path) for path in copied_paths),
            "valid_for_claim": False,
        }
    )

    pycache = Path(__file__).resolve().parent / "__pycache__"
    checks.append(
        {
            "validation_id": "VAL1880_13_pycache_absent",
            "status": "PASS" if not pycache.exists() else "FAIL",
            "detail": str(pycache),
            "valid_for_claim": False,
        }
    )

    formalization_hits = list(FORMALIZATION.rglob("*1880*")) if FORMALIZATION.exists() else []
    checks.append(
        {
            "validation_id": "VAL1880_14_formalization_untouched",
            "status": "PASS" if not formalization_hits else "FAIL",
            "detail": f"formalization_1880_count={len(formalization_hits)}",
            "valid_for_claim": False,
        }
    )

    fail_count = sum(1 for row in checks if row["status"] != "PASS")
    checks.append(
        {
            "validation_id": "VAL1880_OVERALL",
            "status": "PASS" if fail_count == 0 else "FAIL",
            "detail": "1880 terminal public coframe no-shadow frame or bound projection",
            "valid_for_claim": False,
        }
    )
    return checks


def markdown_table(rows: list[dict[str, Any]]) -> str:
    if not rows:
        return ""
    headers: list[str] = []
    for row in rows:
        for key in row:
            if key not in headers:
                headers.append(key)
    lines = [
        "| " + " | ".join(headers) + " |",
        "| " + " | ".join("---" for _ in headers) + " |",
    ]
    for row in rows:
        values = [str(row.get(header, "")).replace("\n", " ") for header in headers]
        lines.append("| " + " | ".join(values) + " |")
    return "\n".join(lines)


def write_doc(rows_by_name: dict[str, list[dict[str, Any]]]) -> None:
    validation = csv_rows(OUTPUTS["validation"])
    content = f"""# 1880 - Terminal Public Coframe No-Shadow Frame Or Bound Projection

**Private status:** nonclaim theorem/projection checkpoint.

## Result

The no-shadow-frame theorem remains exact but conditional:

```text
ordinary matter/readout has terminal public coframe e_pub = E(Q_vis)
no C_R/J_q Weyl, disformal, source-prefactor, endpoint, or post-readout slot exists
=> b_R = d_R = w_R = epsilon_endpoint_R = 0
```

Current MTS does not yet derive the terminal public coframe/action-domain exclusion. So the theorem is not promoted.

The useful progress is that the finite fallback is now projection-shaped rather than vague: PPN, preferred-frame PPN, clock/WEP, orbital, and guarded R10 each have a response-kernel contract and explicit missing inputs.

## Terminal Public Coframe Gate

{markdown_table(rows_by_name["terminal_coframe_gate"])}

## No-Shadow Zero Theorem Attempt

{markdown_table(rows_by_name["zero_theorem_attempt"])}

## Projection Contracts

{markdown_table(rows_by_name["projection_contracts"])}

## Bound Input Rows

{markdown_table(rows_by_name["bound_input_rows"])}

## Runner Refusal

{markdown_table(rows_by_name["runner_refusal"])}

## Source Register

{markdown_table(rows_by_name["source_register"])}

## Claim Gate

{markdown_table(rows_by_name["claim_gate"])}

## Decision Ledger

{markdown_table(rows_by_name["decision"])}

## Next Target

{markdown_table(rows_by_name["next_target"])}

## Validation

{markdown_table(validation)}
"""
    DOC.write_text(content, encoding="utf-8")


def main() -> None:
    ensure_dirs()
    rows_by_name = all_output_rows()
    for key, rows in rows_by_name.items():
        write_csv(OUTPUTS[key], rows)
    copy_branch_artifacts()
    remove_pycache()
    write_csv(OUTPUTS["validation"], validation_rows())
    write_doc(rows_by_name)


if __name__ == "__main__":
    main()

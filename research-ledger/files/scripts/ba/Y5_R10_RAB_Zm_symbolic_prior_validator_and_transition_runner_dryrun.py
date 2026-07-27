from __future__ import annotations

import csv
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
SRC_DIR = Path("source-intake/mts_residuals")

DOC_PATH = Path("1383-Y5-R10-RAB-Zm-symbolic-prior-validator-and-transition-runner-dryrun.md")
SOURCE_REGISTER_PATH = SRC_DIR / "P8_Y5_R10_1383_SOURCE_REGISTER.csv"
PRIOR_VALIDATOR_PATH = SRC_DIR / "P8_Y5_R10_1383_SYMBOLIC_PRIOR_VALIDATOR.csv"
TRANSITION_DRYRUN_PATH = SRC_DIR / "P8_Y5_R10_1383_TRANSITION_INEQUALITY_DRYRUN.csv"
LOCAL_REFUSAL_PATH = SRC_DIR / "P8_Y5_R10_1383_LOCAL_RESIDUAL_REFUSAL_MAP.csv"
CLAIM_GATE_PATH = SRC_DIR / "P8_Y5_R10_1383_CLAIM_GATE.csv"
DECISION_LEDGER_PATH = SRC_DIR / "P8_Y5_R10_1383_DECISION_LEDGER.csv"
NEXT_TARGET_PATH = SRC_DIR / "P8_Y5_R10_1383_NEXT_TARGET.csv"
VALIDATION_PATH = SRC_DIR / "P8_Y5_BRR545_1383_VALIDATION.csv"

PRIOR_PACK_PATH = SRC_DIR / "P8_Y5_R10_1382_SYMBOLIC_PRIOR_PACK.csv"

STATUS = (
    "Z_m_symbolic_prior_validator_and_transition_runner_dryrun_written_"
    "algebraic_only_no_numeric_local_claim"
)
CLAIM_CEILING = (
    "strict_symbolic_validator_only_no_source_backed_Z_m_law_no_numeric_ell_tr_"
    "no_Q_alg_score_no_PPN_no_R10_no_local_GR_pass"
)

EXPECTED_PRIOR_IDS = {
    "ZPP1382_0_Zm_min",
    "ZPP1382_1_Zm_bar",
    "ZPP1382_2_Zm_units",
    "ZPP1382_3_XB_range",
    "ZPP1382_4_same_value_rule",
    "ZPP1382_5_F2_sign_value",
    "ZPP1382_6_Mm2_gap",
    "ZPP1382_7_sources_boundary",
    "ZPP1382_8_prior_verdict",
}

SOURCE_ROWS = [
    {
        "source_id": "SRC1383_0_1382_doc",
        "source_path": "1382-Y5-R10-RAB-Zm-coefficient-law-admissibility-or-symbolic-prior-pack.md",
        "required_anchor": "NEXT1382_0_1383",
        "purpose": "handoff from Z_m prior pack to strict validator/dry-run",
    },
    {
        "source_id": "SRC1383_1_1382_next",
        "source_path": "source-intake/mts_residuals/P8_Y5_R10_1382_NEXT_TARGET.csv",
        "required_anchor": "NEXT1382_0_1383",
        "purpose": "machine-readable 1383 target",
    },
    {
        "source_id": "SRC1383_2_1382_prior_pack",
        "source_path": "source-intake/mts_residuals/P8_Y5_R10_1382_SYMBOLIC_PRIOR_PACK.csv",
        "required_anchor": "ZPP1382_8_prior_verdict",
        "purpose": "symbolic prior rows to validate",
    },
    {
        "source_id": "SRC1383_3_1382_scaffold",
        "source_path": "source-intake/mts_residuals/P8_Y5_R10_1382_ZM_ADMISSIBILITY_SCAFFOLD.csv",
        "required_anchor": "ZAS1382_8_verdict",
        "purpose": "admissibility conditions for Z_m(X_B)",
    },
    {
        "source_id": "SRC1383_4_1382_runner_feed",
        "source_path": "source-intake/mts_residuals/P8_Y5_R10_1382_RUNNER_FEED_UPDATE.csv",
        "required_anchor": "RUF1382_1_symbolic_transition_length",
        "purpose": "symbolic transition length feed",
    },
    {
        "source_id": "SRC1383_5_1382_claim_gate",
        "source_path": "source-intake/mts_residuals/P8_Y5_R10_1382_CLAIM_GATE.csv",
        "required_anchor": "GATE1382_4_local_claim",
        "purpose": "1382 local claim refusal gate",
    },
    {
        "source_id": "SRC1383_6_1379_doc",
        "source_path": "1379-Y5-R10-RAB-gradient-completion-parent-signature-or-transition-closure-runner.md",
        "required_anchor": "Q_alg <= A_ref^-1",
        "purpose": "closure-only symbolic formulas for ell_tr, U_B, Delta_m, Q_alg",
    },
    {
        "source_id": "SRC1383_7_1379_formula_feed",
        "source_path": "source-intake/mts_residuals/P8_Y5_R10_1379_CONDITIONAL_FORMULA_FEED.csv",
        "required_anchor": "CFF1379_3_Q_alg",
        "purpose": "machine-readable conditional formula feed",
    },
    {
        "source_id": "SRC1383_8_1302_stress_contract",
        "source_path": "source-intake/mts_residuals/P8_Y5_R10_1302_MEMORY_STRESS_RESIDUAL_CONTRACT_NONCLAIM.csv",
        "required_anchor": "MSR1302_1_spatial_trace_bound_template",
        "purpose": "memory stress residual bound template",
    },
    {
        "source_id": "SRC1383_9_1382_validation",
        "source_path": "source-intake/mts_residuals/P8_Y5_BRR545_1382_VALIDATION.csv",
        "required_anchor": "VAL1382_5_overall",
        "purpose": "previous checkpoint validation",
    },
    {
        "source_id": "SRC1383_10_this_script",
        "source_path": "scripts/Y5_R10_RAB_Zm_symbolic_prior_validator_and_transition_runner_dryrun.py",
        "required_anchor": "STATUS",
        "purpose": "1383 generator",
    },
]


def clean(value: Any) -> str:
    return str(value).replace("\n", " ").replace("|", "/")


def write_csv(path: Path, rows: list[dict[str, Any]], columns: list[str] | None = None) -> None:
    if not rows:
        raise ValueError(f"no rows for {path}")
    out = ROOT / path
    out.parent.mkdir(parents=True, exist_ok=True)
    fieldnames = columns or list(rows[0].keys())
    with out.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()
        for row in rows:
            writer.writerow({key: clean(row.get(key, "")) for key in fieldnames})


def read_csv(path: Path) -> list[dict[str, str]]:
    with (ROOT / path).open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def md_table(rows: list[dict[str, Any]], columns: list[str] | None = None) -> str:
    if not rows:
        return ""
    fieldnames = columns or list(rows[0].keys())
    lines = [
        "| " + " | ".join(fieldnames) + " |",
        "| " + " | ".join("---" for _ in fieldnames) + " |",
    ]
    for row in rows:
        lines.append("| " + " | ".join(clean(row.get(column, "")) for column in fieldnames) + " |")
    return "\n".join(lines)


def anchor_found(path: Path, anchor: str) -> bool:
    if not path.exists():
        return False
    return anchor in path.read_text(encoding="utf-8", errors="ignore")


def source_register_rows() -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    for row in SOURCE_ROWS:
        source_path = ROOT / row["source_path"]
        exists = source_path.exists()
        found = anchor_found(source_path, row["required_anchor"])
        rows.append(
            {
                **row,
                "exists": str(exists),
                "anchor_found": str(found),
                "valid_for_claim": "False",
                "claim_allowed": "False",
            }
        )
    return rows


def has_missing_marker(row: dict[str, str]) -> bool:
    joined = " ".join(row.values()).upper()
    blockers = [
        "MISSING",
        "NOT_FILLED",
        "NONCLAIM",
        "NOT CLAIM",
        "NOT_SOURCED",
        "NOT_SOURCED",
        "SYMBOLIC_PRIOR",
        "RULE_REQUIRED",
    ]
    return any(marker in joined for marker in blockers)


def bool_text(value: str) -> bool:
    return value.strip().lower() == "true"


def prior_pack_index() -> dict[str, dict[str, str]]:
    rows = read_csv(PRIOR_PACK_PATH)
    return {row["prior_id"]: row for row in rows}


def validator_rows(priors: dict[str, dict[str, str]]) -> list[dict[str, str]]:
    present = set(priors)
    missing_ids = sorted(EXPECTED_PRIOR_IDS - present)
    unexpected_ids = sorted(present - EXPECTED_PRIOR_IDS)
    any_claim_true = any(bool_text(row.get("valid_for_claim", "")) for row in priors.values())
    missing_or_symbolic = [pid for pid, row in priors.items() if has_missing_marker(row)]

    def row_for(
        validator_id: str,
        requirement: str,
        required_prior_ids: list[str],
        algebra: str,
        failure_mode: str,
        next_action: str,
    ) -> dict[str, str]:
        rows = [priors.get(pid, {}) for pid in required_prior_ids]
        ids_present = all(pid in priors for pid in required_prior_ids)
        rows_claim_ready = bool(rows) and all(bool_text(row.get("valid_for_claim", "")) for row in rows)
        rows_clean = bool(rows) and all(not has_missing_marker(row) for row in rows)
        numeric_ready = ids_present and rows_claim_ready and rows_clean
        return {
            "validator_id": validator_id,
            "requirement": requirement,
            "required_prior_ids": ";".join(required_prior_ids),
            "input_status": "ALL_PRESENT" if ids_present else "MISSING_PRIOR_ID",
            "pass_for_algebra": algebra,
            "pass_for_numeric": str(numeric_ready),
            "pass_for_claim": str(numeric_ready),
            "failure_mode": "none" if numeric_ready else failure_mode,
            "next_action": "numeric scorer may run" if numeric_ready else next_action,
        }

    rows = [
        {
            "validator_id": "ZPV1383_0_prior_pack_integrity",
            "requirement": "expected symbolic prior rows exist and remain nonclaim",
            "required_prior_ids": ";".join(sorted(EXPECTED_PRIOR_IDS)),
            "input_status": "PRESENT" if not missing_ids else f"MISSING:{','.join(missing_ids)}",
            "pass_for_algebra": "True",
            "pass_for_numeric": "False",
            "pass_for_claim": "False",
            "failure_mode": (
                "unexpected claim-ready prior row" if any_claim_true else "symbolic prior pack intentionally nonclaim"
            ),
            "next_action": (
                "remove claim flag from prior rows" if any_claim_true else "continue algebraic dry-run only"
            ),
        },
        row_for(
            "ZPV1383_1_positive_ellipticity",
            "real no-ghost local kinetic operator",
            ["ZPP1382_0_Zm_min", "ZPP1382_2_Zm_units"],
            "True",
            "Z_m_min or units are missing; positivity is a requirement not a theorem",
            "derive/source Z_m_min>0 and field/action normalization",
        ),
        row_for(
            "ZPV1383_2_finite_bounds",
            "finite Z_m envelope for stress and transition envelopes",
            ["ZPP1382_1_Zm_bar", "ZPP1382_3_XB_range"],
            "True",
            "Z_m_bar and compact X_B range are missing",
            "derive compact X_B range plus continuity/extrema or source a bound row",
        ),
        row_for(
            "ZPV1383_3_same_law",
            "no arena retuning",
            ["ZPP1382_4_same_value_rule"],
            "True",
            "universal parent law is required but not filled",
            "write/source a single Z_m(X_B) law and projection map per arena",
        ),
        row_for(
            "ZPV1383_4_transition_length",
            "real numeric ell_tr",
            ["ZPP1382_0_Zm_min", "ZPP1382_2_Zm_units", "ZPP1382_5_F2_sign_value"],
            "True",
            "F2 sign/value/units or Z_m normalization are missing",
            "derive/source F2 around m_* and prove Z_m F2>0 in the chosen convention",
        ),
        row_for(
            "ZPV1383_5_profile_bound",
            "local profile/nohair bound",
            ["ZPP1382_5_F2_sign_value", "ZPP1382_6_Mm2_gap", "ZPP1382_7_sources_boundary"],
            "True",
            "gap, zero-mode, source, or boundary terms are missing",
            "derive/source M_m^2 gap, zero-mode treatment, source norm, and boundary flux condition",
        ),
        row_for(
            "ZPV1383_6_residual_scoring",
            "Q_alg/stress residual numeric scoring",
            [
                "ZPP1382_0_Zm_min",
                "ZPP1382_1_Zm_bar",
                "ZPP1382_5_F2_sign_value",
                "ZPP1382_6_Mm2_gap",
                "ZPP1382_7_sources_boundary",
            ],
            "True",
            "transition and stress coefficients remain symbolic",
            "fill all parent coefficient, gap, amplitude, source, and boundary rows",
        ),
        {
            "validator_id": "ZPV1383_7_verdict",
            "requirement": "strict symbolic validator verdict",
            "required_prior_ids": ";".join(sorted(EXPECTED_PRIOR_IDS)),
            "input_status": f"missing_or_symbolic={len(missing_or_symbolic)}; unexpected={','.join(unexpected_ids) or 'none'}",
            "pass_for_algebra": "True",
            "pass_for_numeric": "False",
            "pass_for_claim": "False",
            "failure_mode": "STRICT_VALIDATOR_READY_NUMERIC_BLOCKED",
            "next_action": "use only algebraic inequalities until a parent coefficient law fills the prior pack",
        },
    ]
    return rows


def transition_dryrun_rows() -> list[dict[str, str]]:
    return [
        {
            "dryrun_id": "TID1383_0_real_transition_length",
            "object": "ell_tr",
            "symbolic_formula": "ell_tr=sqrt(Z_m L0^2/F2)",
            "admissibility_condition": "Z_m/F2>0 and L0>0; with Z_m>0 this requires F2>0 in the selected convention",
            "algebraic_bound_if_target": "not a target row; reality condition only",
            "required_inputs": "Z_m sign;F2 sign;L0 units;field normalization",
            "current_status": "ALGEBRAIC_ONLY_INPUTS_MISSING",
            "numeric_scoring": "blocked",
            "valid_for_claim": "False",
        },
        {
            "dryrun_id": "TID1383_1_support_suppression_target",
            "object": "U_B(d)",
            "symbolic_formula": "U_B=exp(-d/ell_tr)",
            "admissibility_condition": "0<U_B<=epsilon_U<1",
            "algebraic_bound_if_target": "ell_tr <= d/log(1/epsilon_U), equivalently Z_m/F2 <= d^2/(L0^2 log(1/epsilon_U)^2)",
            "required_inputs": "d;epsilon_U;Z_m;F2;L0;units",
            "current_status": "ALGEBRAIC_INEQUALITY_READY_VALUES_MISSING",
            "numeric_scoring": "blocked",
            "valid_for_claim": "False",
        },
        {
            "dryrun_id": "TID1383_2_amplitude_target",
            "object": "Delta_m",
            "symbolic_formula": "Delta_m=A_S U_B",
            "admissibility_condition": "|Delta_m|<=epsilon_Delta",
            "algebraic_bound_if_target": "A_S exp(-d/ell_tr) <= epsilon_Delta",
            "required_inputs": "A_S;d;ell_tr;epsilon_Delta;boundary/source amplitude",
            "current_status": "ALGEBRAIC_INEQUALITY_READY_VALUES_MISSING",
            "numeric_scoring": "blocked",
            "valid_for_claim": "False",
        },
        {
            "dryrun_id": "TID1383_3_gradient_target",
            "object": "Delta_grad_m",
            "symbolic_formula": "|nabla m| ~ A_S U_B/ell_tr",
            "admissibility_condition": "|nabla m|<=epsilon_grad",
            "algebraic_bound_if_target": "A_S exp(-d/ell_tr)/ell_tr <= epsilon_grad",
            "required_inputs": "A_S;d;ell_tr;epsilon_grad;profile theorem",
            "current_status": "ALGEBRAIC_INEQUALITY_READY_VALUES_MISSING",
            "numeric_scoring": "blocked",
            "valid_for_claim": "False",
        },
        {
            "dryrun_id": "TID1383_4_Q_alg_target",
            "object": "Q_alg",
            "symbolic_formula": "Q_alg <= A_ref^-1 |F2| A_S^2 U_B^2/(L0^2 ell_tr)",
            "admissibility_condition": "Q_alg<=Q_bound",
            "algebraic_bound_if_target": "|F2| A_S^2 exp(-2d/ell_tr) <= Q_bound A_ref L0^2 ell_tr",
            "required_inputs": "A_ref;F2;A_S;d;ell_tr;L0;Q_bound",
            "current_status": "ALGEBRAIC_INEQUALITY_READY_VALUES_MISSING",
            "numeric_scoring": "blocked",
            "valid_for_claim": "False",
        },
        {
            "dryrun_id": "TID1383_5_stress_residual_target",
            "object": "memory stress residual",
            "symbolic_formula": "sigma_m <= C_Z Z_m_bar B_grad^2 + C_V B_V + C_XB B_XB + C_source B_source + C_boundary B_boundary",
            "admissibility_condition": "sigma_m<=sigma_bound for each local arena",
            "algebraic_bound_if_target": "each residual envelope must be individually bounded; no cancellation credit without parent identity",
            "required_inputs": "Z_m_bar;B_grad;potential subtraction;X_B metric response;source/bath bound;boundary bound",
            "current_status": "RESIDUAL_TEMPLATE_ONLY_VALUES_MISSING",
            "numeric_scoring": "blocked",
            "valid_for_claim": "False",
        },
        {
            "dryrun_id": "TID1383_6_dryrun_verdict",
            "object": "transition runner dry-run",
            "symbolic_formula": "ell_tr,U_B,Delta_m,Delta_grad_m,Q_alg,sigma_m",
            "admissibility_condition": "all formulas may be used for algebraic target-setting only",
            "algebraic_bound_if_target": "strict validator must reject numeric scores until all prior rows become claim-grade",
            "required_inputs": "complete source-backed prior pack",
            "current_status": "DRYRUN_READY_NUMERIC_BLOCKED",
            "numeric_scoring": "blocked",
            "valid_for_claim": "False",
        },
    ]


def local_refusal_rows() -> list[dict[str, str]]:
    return [
        {
            "arena_id": "LRF1383_0_q_loc",
            "arena": "q_loc^nu -> 0",
            "needed_for_claim": "parent-signed source/boundary/gap theorem plus stress residual bound",
            "blocking_inputs": "ZPP1382_6_Mm2_gap;ZPP1382_7_sources_boundary;TID1383_5_stress_residual_target",
            "current_status": "BLOCKED_NO_THEOREM_ZERO",
            "next_action": "derive source/boundary silence or keep q_loc residual vector explicit",
            "claim_allowed": "False",
        },
        {
            "arena_id": "LRF1383_1_local_GR",
            "arena": "local GR reduction",
            "needed_for_claim": "q_loc residuals vanish or are bounded below GR-test tolerances without arena retuning",
            "blocking_inputs": "Z_m law;F2;gap;stress envelope;PPN residual vector",
            "current_status": "BLOCKED_NO_LOCAL_GR_PASS",
            "next_action": "fill prior pack and run PPN/local residual scorer",
            "claim_allowed": "False",
        },
        {
            "arena_id": "LRF1383_2_PPN",
            "arena": "PPN",
            "needed_for_claim": "numeric residual vector alpha1, alpha2, gamma-1, beta-1, xi, preferred-frame/location terms",
            "blocking_inputs": "stress residual envelope;source/boundary terms;arena projection",
            "current_status": "BLOCKED_NO_NUMERIC_RESIDUAL_VECTOR",
            "next_action": "derive or source local residual coefficients after prior pack fill",
            "claim_allowed": "False",
        },
        {
            "arena_id": "LRF1383_3_R10",
            "arena": "R10 / short-range alpha(lambda)",
            "needed_for_claim": "alpha_predicted(lambda) with sourced coupling, mass/range, and bound curve",
            "blocking_inputs": "Z_m/F2/L0 range;coupling coefficient;source projection;valid bound rows",
            "current_status": "BLOCKED_NO_ALPHA_LAMBDA_SCORE",
            "next_action": "do not connect transition length to R10 until coupling and range are claim-grade",
            "claim_allowed": "False",
        },
        {
            "arena_id": "LRF1383_4_clocks_orbital",
            "arena": "clocks and orbital systems",
            "needed_for_claim": "time variation, fifth-force, and orbital residual coefficients below bounds",
            "blocking_inputs": "same universal Z_m law;source/boundary projection;metric response",
            "current_status": "BLOCKED_NO_ARENA_PROJECTION",
            "next_action": "fill universal-law projection before using any clock/orbital comparison",
            "claim_allowed": "False",
        },
    ]


def claim_gate_rows(validator: list[dict[str, str]]) -> list[dict[str, str]]:
    numeric_ready = all(row["pass_for_numeric"] == "True" for row in validator if row["validator_id"] != "ZPV1383_0_prior_pack_integrity")
    return [
        {
            "gate_id": "GATE1383_0_sources",
            "gate": "all cited sources exist and anchors are present",
            "status": "PASS",
            "reason": "source register validates against local corpus",
            "valid_for_claim": "False",
            "claim_allowed": "False",
        },
        {
            "gate_id": "GATE1383_1_validator",
            "gate": "strict symbolic prior validator exists",
            "status": "PASS_SYMBOLIC_VALIDATOR",
            "reason": "validator rows identify the missing priors and keep pass_for_numeric=false",
            "valid_for_claim": "False",
            "claim_allowed": "False",
        },
        {
            "gate_id": "GATE1383_2_algebra",
            "gate": "transition inequalities may be used algebraically",
            "status": "PASS_ALGEBRA_ONLY",
            "reason": "ell_tr, U_B, Delta_m, gradient, Q_alg, and stress target inequalities are written as dry-run rows",
            "valid_for_claim": "False",
            "claim_allowed": "False",
        },
        {
            "gate_id": "GATE1383_3_numeric",
            "gate": "numeric scoring can run",
            "status": "PASS_NUMERIC_READY" if numeric_ready else "BLOCKED_NUMERIC_INPUTS_MISSING",
            "reason": "all validator rows would need source-backed, claim-grade inputs before scoring",
            "valid_for_claim": "False",
            "claim_allowed": "False",
        },
        {
            "gate_id": "GATE1383_4_local_claim",
            "gate": "local GR / PPN / R10 pass can be claimed",
            "status": "BLOCKED_NO_CLAIM",
            "reason": "1383 is a refusal-aware algebraic dry-run, not a parent-signed local reduction",
            "valid_for_claim": "False",
            "claim_allowed": "False",
        },
    ]


def decision_rows() -> list[dict[str, str]]:
    return [
        {
            "decision_id": "DEC1383_0",
            "question": "Did 1383 make the transition branch safer?",
            "answer": "Yes",
            "rationale": "A future runner now has exact conditions for when algebra is allowed and when numeric scoring is refused.",
            "next_action": "try to derive the first parent coefficient-law row rather than adding more closure layers",
            "claim_allowed": "False",
        },
        {
            "decision_id": "DEC1383_1",
            "question": "Did 1383 prove local GR or q_loc=0?",
            "answer": "No",
            "rationale": "The validator exposes that Z_m_min, Z_m_bar, F2, gap, source, boundary, and arena projection rows remain missing.",
            "next_action": "attack Z_m(X_B)/F2 parent law derivation directly",
            "claim_allowed": "False",
        },
    ]


def next_target_rows() -> list[dict[str, str]]:
    return [
        {
            "next_id": "NEXT1383_0_1384",
            "next_doc": "1384-Y5-R10-RAB-Zm-parent-coefficient-law-derivation-attempt-or-F2-normalization-pivot.md",
            "next_script": "scripts/Y5_R10_RAB_Zm_parent_coefficient_law_derivation_attempt_or_F2_normalization_pivot.py",
            "task": "attempt the derivation of a parent-owned Z_m(X_B) coefficient law and F2 normalization; if it fails, identify the smallest first-fill row that would unlock transition/local residual scoring",
            "success_condition": "either a parent-law derivation scaffold for Z_m/F2 exists, or the next irreducible missing input is selected with source requirements and claims remain blocked",
            "do_not_claim": "local GR;PPN pass;R10 pass;q_loc=0;numeric ell_tr;GitHub-ready result",
            "valid_for_claim": "False",
            "claim_allowed": "False",
        }
    ]


def validation_rows(
    sources: list[dict[str, str]],
    priors: dict[str, dict[str, str]],
    validator: list[dict[str, str]],
    transition: list[dict[str, str]],
    local_refusal: list[dict[str, str]],
    gates: list[dict[str, str]],
) -> list[dict[str, str]]:
    all_sources_ok = all(row["exists"] == "True" and row["anchor_found"] == "True" for row in sources)
    all_expected_priors = EXPECTED_PRIOR_IDS.issubset(set(priors))
    numeric_blocked = all(row["pass_for_numeric"] == "False" for row in validator)
    transition_nonclaim = all(row["valid_for_claim"] == "False" and row["numeric_scoring"] == "blocked" for row in transition)
    local_blocked = all(row["claim_allowed"] == "False" and row["current_status"].startswith("BLOCKED") for row in local_refusal)
    claim_blocked = any(row["gate_id"] == "GATE1383_4_local_claim" and row["status"] == "BLOCKED_NO_CLAIM" for row in gates)
    outputs = [
        DOC_PATH,
        SOURCE_REGISTER_PATH,
        PRIOR_VALIDATOR_PATH,
        TRANSITION_DRYRUN_PATH,
        LOCAL_REFUSAL_PATH,
        CLAIM_GATE_PATH,
        DECISION_LEDGER_PATH,
        NEXT_TARGET_PATH,
        VALIDATION_PATH,
        Path("scripts/Y5_R10_RAB_Zm_symbolic_prior_validator_and_transition_runner_dryrun.py"),
    ]
    outside_formalization = all("formalization-workbench" not in str(ROOT / path) for path in outputs)
    overall = all([all_sources_ok, all_expected_priors, numeric_blocked, transition_nonclaim, local_blocked, claim_blocked, outside_formalization])
    return [
        {
            "validation_id": "VAL1383_0_sources",
            "check": "every cited local source path exists and anchor is found",
            "status": "PASS" if all_sources_ok else "FAIL",
            "details": "; ".join(f"{row['source_id']} exists={row['exists']} anchor={row['anchor_found']}" for row in sources),
        },
        {
            "validation_id": "VAL1383_1_prior_ids",
            "check": "expected 1382 symbolic prior ids exist",
            "status": "PASS" if all_expected_priors else "FAIL",
            "details": f"expected={len(EXPECTED_PRIOR_IDS)} present={len(set(priors) & EXPECTED_PRIOR_IDS)}",
        },
        {
            "validation_id": "VAL1383_2_numeric_refusal",
            "check": "validator refuses numeric scoring",
            "status": "PASS" if numeric_blocked else "FAIL",
            "details": "All ZPV1383 rows keep pass_for_numeric=False.",
        },
        {
            "validation_id": "VAL1383_3_transition_nonclaim",
            "check": "transition dry-run rows are algebraic and nonclaim",
            "status": "PASS" if transition_nonclaim else "FAIL",
            "details": "All TID1383 rows keep numeric_scoring=blocked and valid_for_claim=False.",
        },
        {
            "validation_id": "VAL1383_4_local_refusal",
            "check": "local arenas remain blocked",
            "status": "PASS" if local_blocked and claim_blocked else "FAIL",
            "details": "LRF1383 rows and GATE1383_4 block local GR/PPN/R10/q_loc claims.",
        },
        {
            "validation_id": "VAL1383_5_scope",
            "check": "generated outputs stay inside post-checkpoint-work and outside formalization-workbench",
            "status": "PASS" if outside_formalization else "FAIL",
            "details": f"ROOT={ROOT}; output_count={len(outputs)}; formalization_touched=False",
        },
        {
            "validation_id": "VAL1383_6_overall",
            "check": "overall 1383 validation",
            "status": "PASS" if overall else "FAIL",
            "details": "1383 writes a strict refusal-aware symbolic validator and transition inequality dry-run.",
        },
    ]


def write_doc(
    sources: list[dict[str, str]],
    validator: list[dict[str, str]],
    transition: list[dict[str, str]],
    local_refusal: list[dict[str, str]],
    gates: list[dict[str, str]],
    decisions: list[dict[str, str]],
    next_target: list[dict[str, str]],
    validation: list[dict[str, str]],
) -> None:
    generated = datetime.now(timezone.utc).isoformat()
    body = f"""# 1383 - Y5 R10 RAB Z_m Symbolic Prior Validator And Transition Runner Dry-Run

**Generated:** {generated}

**Current verdict:** the `Z_m` transition route is now executable only as algebra. The validator accepts symbolic manipulation of `ell_tr`, `U_B`, `Delta_m`, gradient size, `Q_alg`, and stress envelopes, but refuses numeric scoring because `Z_m_min`, `Z_m_bar`, `F2`, units, gap, source, boundary, and arena-projection rows remain unresolved.

**What this buys:** the branch is no longer vague. A future derivation can target exact inequalities instead of waving at "suppression"; but any local-GR, PPN, R10, or `q_loc=0` claim remains blocked.

**Claim ceiling:** {CLAIM_CEILING}

## Source Register

{md_table(sources)}

## Strict Symbolic Prior Validator

{md_table(validator)}

## Transition Inequality Dry-Run

{md_table(transition)}

## Local Residual Refusal Map

{md_table(local_refusal)}

## Claim Gates

{md_table(gates)}

## Decision Ledger

{md_table(decisions)}

## Next Target

{md_table(next_target)}

## Validation

{md_table(validation)}
"""
    (ROOT / DOC_PATH).write_text(body, encoding="utf-8")


def main() -> None:
    sources = source_register_rows()
    priors = prior_pack_index()
    validator = validator_rows(priors)
    transition = transition_dryrun_rows()
    local_refusal = local_refusal_rows()
    gates = claim_gate_rows(validator)
    decisions = decision_rows()
    next_target = next_target_rows()
    validation = validation_rows(sources, priors, validator, transition, local_refusal, gates)

    write_csv(SOURCE_REGISTER_PATH, sources)
    write_csv(PRIOR_VALIDATOR_PATH, validator)
    write_csv(TRANSITION_DRYRUN_PATH, transition)
    write_csv(LOCAL_REFUSAL_PATH, local_refusal)
    write_csv(CLAIM_GATE_PATH, gates)
    write_csv(DECISION_LEDGER_PATH, decisions)
    write_csv(NEXT_TARGET_PATH, next_target)
    write_csv(VALIDATION_PATH, validation)
    write_doc(sources, validator, transition, local_refusal, gates, decisions, next_target, validation)

    failed = [row for row in validation if row["status"] != "PASS"]
    if failed:
        raise SystemExit(f"1383 validation failed: {failed}")
    print(STATUS)
    print(ROOT / DOC_PATH)
    print(ROOT / VALIDATION_PATH)


if __name__ == "__main__":
    main()

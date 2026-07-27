from __future__ import annotations

import csv
from datetime import datetime, timezone
from pathlib import Path


PACK_ID = "P8_Y5_R10_1312"
TITLE = "1312-Y5-R10-RAB-b-alpha-no-vertex-or-source-backed-coefficient"
ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = ROOT / "source-intake" / "mts_residuals"
DOC_PATH = ROOT / f"{TITLE}.md"
FORMALIZATION = ROOT.parent / "formalization-workbench"

SOURCE_REGISTER_PATH = OUT_DIR / f"{PACK_ID}_SOURCE_REGISTER.csv"
NO_F2_PROOF_AUDIT_PATH = OUT_DIR / f"{PACK_ID}_B_ALPHA_NO_F2_PROOF_AUDIT.csv"
ZQEFF_DRIFT_AUDIT_PATH = OUT_DIR / f"{PACK_ID}_ZQEFF_DRIFT_CLAUSE_AUDIT.csv"
COEFFICIENT_ACQUISITION_PATH = OUT_DIR / f"{PACK_ID}_B_ALPHA_COEFFICIENT_ACQUISITION_NONCLAIM.csv"
PRODUCT_RUNNER_GATE_PATH = OUT_DIR / f"{PACK_ID}_ALPHA_PRODUCT_RUNNER_GATE.csv"
THRESHOLD_POLICY_PATH = OUT_DIR / f"{PACK_ID}_THRESHOLD_POLICY.csv"
CLAIM_GATES_PATH = OUT_DIR / f"{PACK_ID}_CLAIM_GATES.csv"
DECISION_PATH = OUT_DIR / f"{PACK_ID}_DECISION_LEDGER.csv"
NEXT_PATH = OUT_DIR / f"{PACK_ID}_NEXT_TARGET.csv"
VALIDATION_PATH = OUT_DIR / "P8_Y5_BRR545_1312_VALIDATION.csv"


def source_path(relative_path: str) -> Path:
    path = Path(relative_path)
    if path.is_absolute():
        return path
    return ROOT / path


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, object]], fieldnames: list[str] | None = None) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if fieldnames is None:
        fieldnames = []
        for row in rows:
            for key in row:
                if key not in fieldnames:
                    fieldnames.append(key)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()
        for row in rows:
            writer.writerow({field: row.get(field, "") for field in fieldnames})


def md_escape(value: object) -> str:
    return str(value).replace("|", "\\|").replace("\n", " ")


def markdown_table(rows: list[dict[str, object]], fields: list[str]) -> str:
    if not rows:
        return "_No rows._\n"
    return "\n".join(
        [
            "| " + " | ".join(fields) + " |",
            "| " + " | ".join(["---"] * len(fields)) + " |",
            *["| " + " | ".join(md_escape(row.get(field, "")) for field in fields) + " |" for row in rows],
        ]
    )


def exists_and_contains(relative_path: str, needle: str) -> tuple[bool, bool]:
    path = source_path(relative_path)
    if not path.exists():
        return False, False
    if not needle:
        return True, True
    return True, needle in read_text(path)


def validation_row(check_id: str, check: str, passed: bool, details: str) -> dict[str, object]:
    return {"check_id": check_id, "check": check, "status": "PASS" if passed else "FAIL", "details": details}


def is_false(value: object) -> bool:
    return str(value).strip().lower() in {"false", "0", "no"}


def all_nonclaim(tables: list[list[dict[str, object]]]) -> bool:
    return all(
        is_false(row.get("valid_for_claim", False)) and is_false(row.get("claim_allowed", False))
        for rows in tables
        for row in rows
    )


def generated_inside_formalization() -> list[Path]:
    generated_paths = [
        SOURCE_REGISTER_PATH,
        NO_F2_PROOF_AUDIT_PATH,
        ZQEFF_DRIFT_AUDIT_PATH,
        COEFFICIENT_ACQUISITION_PATH,
        PRODUCT_RUNNER_GATE_PATH,
        THRESHOLD_POLICY_PATH,
        CLAIM_GATES_PATH,
        DECISION_PATH,
        NEXT_PATH,
        VALIDATION_PATH,
        DOC_PATH,
    ]
    return [path for path in generated_paths if FORMALIZATION in path.parents]


def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)

    source_register = [
        {
            "source_id": "SRC1312_0_1311_next",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1311_NEXT_TARGET.csv",
            "needle": "NEXT1311_0_1312",
            "role": "handoff into b_alpha/c_alpha no-vertex or source-backed coefficient gate",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "source_id": "SRC1312_1_1311_balpha",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1311_COEFFICIENT_SOURCE_AUDIT.csv",
            "needle": "QCSA1311_0_b_alpha",
            "role": "1311 says b_alpha has no theorem-zero or source-backed value",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "source_id": "SRC1312_2_1048_noF2",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1048_NO_EXTRA_F2_THEOREM_ATTEMPT.csv",
            "needle": "FAIL_CURRENT_CORPUS_COUNTERTERM_NOT_FORBIDDEN",
            "role": "earlier no-extra-F2 theorem attempt and live scalar counterterm",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "source_id": "SRC1312_3_1099_owner",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1099_EM_KINETIC_OWNER_THEOREM_ATTEMPT.csv",
            "needle": "NO_EXTRA_F2_THEOREM_NOT_PROMOTED",
            "role": "unique EM kinetic owner theorem remains conditional",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "source_id": "SRC1312_4_1100_signature",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1100_TQ_GAUGE_NORM_SIGNATURE.csv",
            "needle": "TQ_GAUGE_NORM_SIGNATURE_NOT_DERIVED",
            "role": "T_Q/gauge-norm signature does not close coupling owner",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "source_id": "SRC1312_5_1100_Z",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1100_ALPHA_NORMALIZATION_DECOMPOSITION.csv",
            "needle": "Z1100_4_total",
            "role": "Z_A decomposition names parent, lambda, hidden, radiative, and readout pieces",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "source_id": "SRC1312_6_1108_acq",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1108_EM_ALPHA_ACQUISITION_LEDGER.csv",
            "needle": "ACQ1108_5_external_alpha_coefficient",
            "role": "EM alpha acquisition ledger names missing source-backed coefficient",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "source_id": "SRC1312_7_1111_drift",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1111_ALPHA_DRIFT_ZERO_THEOREM_ATTEMPT.csv",
            "needle": "ALPHA_DRIFT_ZERO_NOT_DERIVED",
            "role": "alpha drift zero chain-rule theorem is exact but unsigned",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "source_id": "SRC1312_8_1112_contract",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1112_ALPHA_PRODUCT_RUNNER_CONTRACT_NONCLAIM.csv",
            "needle": "APC1112_2_R10_alpha_product",
            "role": "strict alpha product runner contract",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "source_id": "SRC1312_9_1113_acq",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1113_ALPHA_PRODUCT_INPUT_ACQUISITION_LEDGER.csv",
            "needle": "AQ1113_0_balpha_or_zero",
            "role": "finite alpha product input acquisition ledger",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "source_id": "SRC1312_10_1114_nohom",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1114_NO_HIDDEN_VISIBLE_MORPHISM_THEOREM_ATTEMPT.csv",
            "needle": "NHV1114_6_verdict",
            "role": "no-hidden-visible coefficient morphism attempt",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "source_id": "SRC1312_11_1115_invariant",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1115_LOCAL_INVARIANT_ALGEBRA_TRIVIALITY_ATTEMPT.csv",
            "needle": "LIA1115_6_verdict",
            "role": "local invariant algebra triviality attempt",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "source_id": "SRC1312_12_1218_alpha_owner",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1218_ALPHA_SURFACE_OPERATOR_OWNER_AUDIT.csv",
            "needle": "PARENT_ALPHA_SURFACE_OPERATOR_OWNER_NOT_DERIVED",
            "role": "later alpha/surface owner audit retains alpha counterterm obstruction",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]
    for row in source_register:
        exists, needle_found = exists_and_contains(str(row["local_path"]), str(row["needle"]))
        row["exists"] = exists
        row["needle_found"] = needle_found

    no_f2_proof = [
        {
            "clause_id": "BA1312_0_parent_TQ_object",
            "clause": "T_Q is a parent-action object before observed EM readout",
            "mathematical_requirement": "T_Q in Lie(G_parent) or integral lattice L_Q, varied/owned in S_parent before projection to A_Q",
            "current_evidence": "1100 marks parent T_Q object partial template only",
            "result": "UNSIGNED",
            "if_signed": "observed EM connection is not appended after the fact",
            "if_missing": "A_Q and its normalization can remain readout-side data",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "clause_id": "BA1312_1_fixed_norm_level",
            "clause": "fixed nonrescalable gauge-fibre norm or level",
            "mathematical_requirement": "N_Q=<T_Q,T_Q>_P or a discrete level/index fixes the Maxwell kinetic normalization",
            "current_evidence": "1100/1101 retain the continuous coupling gap",
            "result": "UNSIGNED",
            "if_signed": "parent Maxwell coefficient can be vertically silent",
            "if_missing": "T_Q rescaling leaves g_EM/alpha owner conventional",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "clause_id": "BA1312_2_no_lambda_F2",
            "clause": "no independent visible lambda_A F_Q^2 term",
            "mathematical_requirement": "operator-domain exhaustion excludes any standalone visible Maxwell kinetic counterterm",
            "current_evidence": "1048, 1099, 1107, and 1218 keep lambda_A F_Q^2 legal",
            "result": "COUNTERTERM_RETAINED",
            "if_signed": "fixed parent norm is the unique tree-level EM kinetic owner",
            "if_missing": "constant lambda changes alpha calibration and hidden-dependent lambda reopens b_alpha",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "clause_id": "BA1312_3_no_hidden_fF2",
            "clause": "no hidden-visible coefficient map f(I_hid)F_Q^2",
            "mathematical_requirement": "Hom(C_hid,Coeff(F_Q^2)) is constant/absent or O(C_hid)^inv=R",
            "current_evidence": "1114 no-hom and 1115 invariant-triviality routes are not promoted",
            "result": "COUNTEREXAMPLE_RETAINED",
            "if_signed": "hidden local representatives cannot generate alpha drift",
            "if_missing": "a surviving scalar invariant can define b_alpha(I)=b0+epsilon I",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "clause_id": "BA1312_4_same_current_owner",
            "clause": "same T_Q owner fixes current/source normalization",
            "mathematical_requirement": "J_Q=delta S_m/delta A_Q with no q_A(Xhat), beta_source_alpha, or species current weights",
            "current_evidence": "1100 and 1113 keep source normalization and beta_source_alpha missing",
            "result": "UNSIGNED",
            "if_signed": "WEP/R10 alpha source products cannot float independently",
            "if_missing": "beta_source_alpha remains a real source-normalization debt",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "clause_id": "BA1312_5_radiative_readout",
            "clause": "radiative/readout closure preserves alpha owner",
            "mathematical_requirement": "S_vis^eff and observed alpha/readout maps factor only through q, T_Q, N_Q, and fixed representation data",
            "current_evidence": "1051, 1058, 1112, and 1113 keep radiative/readout closure unsigned",
            "result": "UNSIGNED_CRITICAL",
            "if_signed": "tree-level no-F2 result survives clocks/spectra",
            "if_missing": "loop, threshold, or readout terms regenerate b_alpha",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "clause_id": "BA1312_6_verdict",
            "clause": "b_alpha theorem-zero by no-F2/EM-owner route",
            "mathematical_requirement": "BA1312_0 through BA1312_5 all signed",
            "current_evidence": "multiple critical clauses fail or remain unsigned",
            "result": "B_ALPHA_THEOREM_ZERO_NOT_DERIVED",
            "if_signed": "b_alpha/c_alpha can be demoted to theorem-zero",
            "if_missing": "retain finite alpha coefficient/product acquisition",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    zqeff_drift = [
        {
            "term_id": "ZBA1312_0_parent_piece",
            "term": "C_P N_Q",
            "drift_condition": "D_v(C_P N_Q)=0",
            "current_status": "NOT_DERIVED",
            "source_anchor": "Z1100_0_parent_piece; ADZ1111_3_parent_norm",
            "effect_if_open": "parent normalization itself can contribute to b_alpha",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "term_id": "ZBA1312_1_lambda",
            "term": "lambda_A",
            "drift_condition": "lambda_A absent or universal constant with no local vertical branch",
            "current_status": "CONSTANT_CALIBRATION_ONLY_HIDDEN_BRANCH_OPEN",
            "source_anchor": "Z1100_1_constant_counterterm; ALP1107_1_constant_counterterm",
            "effect_if_open": "absolute alpha value is calibrated, not predicted; hidden lambda can drift",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "term_id": "ZBA1312_2_hidden_f",
            "term": "f(I_hid)",
            "drift_condition": "D_v f(I_hid)=0 by no-hidden-visible morphism or invariant-triviality theorem",
            "current_status": "COUNTEREXAMPLE_RETAINED",
            "source_anchor": "OWNER1218_2_alpha_counterterm_obstruction; NHV1114_6_verdict; LIA1115_6_verdict",
            "effect_if_open": "direct local alpha drift/source coupling",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "term_id": "ZBA1312_3_radiative",
            "term": "Delta_lambda_rad(mu,X)",
            "drift_condition": "EFT threshold/running terms descend through q and fixed representation data",
            "current_status": "UNSIGNED",
            "source_anchor": "ZQD1112_3_radiative; RCG1058_1_loop_threshold",
            "effect_if_open": "bare zero does not survive effective observed alpha",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "term_id": "ZBA1312_4_readout",
            "term": "Delta_readout",
            "drift_condition": "clock/spectroscopy/readout maps are post-solution quotient functors",
            "current_status": "CONDITIONAL_NOT_GLOBAL",
            "source_anchor": "ZQD1112_4_readout; POC1113_6_radiative_closure",
            "effect_if_open": "spectroscopy/clocks can see alpha pressure even if bare action is clean",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "term_id": "ZBA1312_5_total",
            "term": "b_alpha=-D_v ln Z_Q_eff",
            "drift_condition": "all terms above are vertically silent and Z_Q_eff finite",
            "current_status": "ALPHA_DRIFT_ZERO_NOT_DERIVED",
            "source_anchor": "ADZ1111_5_verdict; ZQD1112_6_verdict",
            "effect_if_open": "standalone b_alpha/c_alpha remains missing, not zero",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    coefficient_acquisition = [
        {
            "acq_id": "BAC1312_0_theorem_zero",
            "quantity": "b_alpha or c_alpha_DD",
            "available_value": "NONE",
            "available_bound_or_pressure": "8.3202449332435330e-10 dimensionless DD threshold",
            "units": "dimensionless vertical coefficient",
            "current_status": "MISSING_THEOREM_ZERO_OR_SOURCE_BACKED_COEFFICIENT",
            "why_not_claim": "threshold is a private acceptance fence, not an MTS coefficient prediction",
            "required_next_input": "signed EM-F2/no-hidden/radiative-readout theorem or numeric source-backed coefficient",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "acq_id": "BAC1312_1_clock_product",
            "quantity": "b_alpha*tau_clock_time",
            "available_value": "2.1000000000000000e-18",
            "available_bound_or_pressure": "source-backed clock product bound",
            "units": "yr^-1",
            "current_status": "PRODUCT_BOUND_AVAILABLE_NOT_STANDALONE",
            "why_not_claim": "tau_clock_time and Xhat/readout normalization are not derived",
            "required_next_input": "tau_clock/Xhat map or direct MTS clock product prediction",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "acq_id": "BAC1312_2_wep_product",
            "quantity": "beta_source_alpha*b_alpha*tau_WEP",
            "available_value": "NONE",
            "available_bound_or_pressure": "4.7977805227320001e-05 WEP alpha/Coulomb pressure target",
            "units": "dimensionless",
            "current_status": "PRODUCT_TARGET_ONLY",
            "why_not_claim": "beta_source_alpha, tau_WEP, and full material/source map are missing",
            "required_next_input": "source normalization theorem or direct numeric WEP alpha product",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "acq_id": "BAC1312_3_r10_product",
            "quantity": "P_R10_alpha(lambda)",
            "available_value": "NONE",
            "available_bound_or_pressure": "claim-valid alpha_bound(lambda) curve still required",
            "units": "dimensionless Yukawa alpha(lambda)",
            "current_status": "R10_PRODUCT_VECTOR_MISSING",
            "why_not_claim": "lambda_X, Z_X, K_X, beta_source, beta_test, tau_R10, and promoted bound curve are not all sourced",
            "required_next_input": "finite numeric R10 product vector plus real bound curve",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "acq_id": "BAC1312_4_cross_arena",
            "quantity": "shared alpha branch classifier",
            "available_value": "NONE",
            "available_bound_or_pressure": "clock/WEP/R10 pressure rows exist separately",
            "units": "branch/readout identity",
            "current_status": "MISSING_CROSS_ARENA_PARENT_MAP",
            "why_not_claim": "same symbol alpha does not prove same parent-owned local product in every arena",
            "required_next_input": "global readout/domain functor or explicit arena product rows",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    product_runner_gate = [
        {
            "gate_id": "APG1312_0_balpha",
            "runner_requirement": "b_alpha theorem-zero or numeric coefficient",
            "current_status": "MISSING",
            "runner_effect": "all alpha product rows remain non-executable",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "gate_id": "APG1312_1_clock",
            "runner_requirement": "tau_clock_time or direct clock product",
            "current_status": "MISSING_PARENT_TAU_CLOCK_XHAT_MAP",
            "runner_effect": "clock product bound cannot be divided into standalone b_alpha",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "gate_id": "APG1312_2_wep",
            "runner_requirement": "beta_source_alpha, tau_WEP, and material map or direct product",
            "current_status": "MISSING_SOURCE_NORMALIZATION_AND_TAU_WEP",
            "runner_effect": "WEP alpha product cannot score",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "gate_id": "APG1312_3_r10",
            "runner_requirement": "lambda_X, Z_X, K_X, source/test beta factors, tau_R10, promoted alpha_bound(lambda)",
            "current_status": "MISSING_R10_FINITE_BRANCH_INPUTS",
            "runner_effect": "R10 alpha product cannot score",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "gate_id": "APG1312_4_cross_arena",
            "runner_requirement": "same parent Z_Q_eff branch and readout/domain map across clock/WEP/R10",
            "current_status": "MISSING_CROSS_ARENA_PARENT_MAP",
            "runner_effect": "no transfer shortcut between arenas",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    threshold_policy = [
        {
            "policy_id": "TP1312_0_DD_alpha",
            "threshold": "abs(c_alpha_DD) <= 8.3202449332435330e-10",
            "source_family": "1096/1097/1098/1110/1218 threshold rows",
            "allowed_use": "private acceptance fence after MTS coefficient exists",
            "forbidden_use": "do not treat as b_alpha/c_alpha prediction or prior selected by theory",
            "status": "THRESHOLD_ONLY_NONCLAIM",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "policy_id": "TP1312_1_clock_product",
            "threshold": "abs(b_alpha*tau_clock_time) <= 2.1e-18 yr^-1",
            "source_family": "1051/1052/1102 clock product rows",
            "allowed_use": "nonclaim product pressure on a future clock product prediction",
            "forbidden_use": "do not divide by guessed tau_clock or transfer to WEP/R10",
            "status": "PRODUCT_BOUND_NONCLAIM",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "policy_id": "TP1312_2_WEP_product",
            "threshold": "abs(P_WEP_alpha) <= 4.7977805227320001e-05",
            "source_family": "1052/1102 WEP alpha/Coulomb target rows",
            "allowed_use": "nonclaim pressure target for future source-backed WEP product",
            "forbidden_use": "do not set beta_source_alpha=1, tau_WEP=1, or use pair tuning",
            "status": "PRODUCT_TARGET_NONCLAIM",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    claim_gates = [
        {
            "gate_id": "CG1312_0_no_F2",
            "claim": "b_alpha=0 follows from no-extra-F2/EM-owner theorem",
            "current_status": "BLOCKED",
            "reason": "fixed norm, no lambda, no hidden f, same current owner, and radiative/readout clauses are not all signed",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "gate_id": "CG1312_1_source_backed",
            "claim": "b_alpha/c_alpha has a source-backed numeric value",
            "current_status": "BLOCKED",
            "reason": "no numeric coefficient value exists; thresholds are fences only",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "gate_id": "CG1312_2_products",
            "claim": "clock/WEP/R10 alpha products are score-ready",
            "current_status": "BLOCKED",
            "reason": "tau, source normalization, material maps, R10 product vector, and promoted bound curve are missing",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "gate_id": "CG1312_3_local_GR",
            "claim": "local GR/Newton recovery is secured by alpha branch",
            "current_status": "BLOCKED",
            "reason": "alpha is one retained coupling branch, and source/test charge plus PPN gates remain separate",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    decision = [
        {
            "decision_id": "DEC1312_0_result",
            "decision": "b_alpha no-vertex route is exact as a conditional but not derived",
            "because": "the live legal operators are lambda_A F_Q^2, f(I_hid)F_Q^2, and radiative/readout F2 terms",
            "next_action": "attack the typed no-hidden-visible coefficient morphism clause, because it would also hit mass, clocks, WEP, R10, and source weights",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "decision_id": "DEC1312_1_acquisition",
            "decision": "finite alpha rows remain nonclaim acquisition rows",
            "because": "available numerical rows are thresholds or product bounds, not MTS predictions",
            "next_action": "keep threshold/product rows as fences while seeking a theorem-zero or real coefficient/product input",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    next_target = [
        {
            "next_id": "NEXT1312_0_1313",
            "target_file": "1313-Y5-R10-RAB-typed-no-hidden-visible-coefficient-morphism-or-alpha-product-input.md",
            "target_script": "scripts/Y5_R10_RAB_typed_no_hidden_visible_coefficient_morphism_or_alpha_product_input.py",
            "task": "try to prove the typed no-hidden-visible coefficient morphism theorem; if it fails, begin strict finite alpha product input acquisition under the 1112 contract",
            "success_condition": "hidden representatives cannot be arguments of visible F2/mass/clock/source coefficients, or every alpha product input remains explicit and nonclaim",
            "do_not": "do not use minimality, unit choices, thresholds, or clock products as standalone b_alpha predictions",
            "valid_for_claim": False,
            "claim_allowed": False,
        }
    ]

    validations: list[dict[str, object]] = []
    validations.append(
        validation_row(
            "VAL1312_0_sources_exist",
            "registered source paths exist and anchors are found",
            all(row["exists"] and row["needle_found"] for row in source_register),
            f"{sum(1 for row in source_register if row['exists'] and row['needle_found'])}/{len(source_register)} source anchors found",
        )
    )
    validations.append(
        validation_row(
            "VAL1312_1_no_F2_not_derived",
            "b_alpha no-F2 theorem is not promoted",
            no_f2_proof[-1]["result"] == "B_ALPHA_THEOREM_ZERO_NOT_DERIVED",
            ";".join(f"{row['clause_id']}={row['result']}" for row in no_f2_proof),
        )
    )
    validations.append(
        validation_row(
            "VAL1312_2_zqeff_open_terms",
            "Z_Q_eff drift audit retains open parent/hidden/radiative/readout terms",
            any(row["current_status"] in {"NOT_DERIVED", "COUNTEREXAMPLE_RETAINED", "UNSIGNED"} for row in zqeff_drift),
            ";".join(f"{row['term_id']}={row['current_status']}" for row in zqeff_drift),
        )
    )
    validations.append(
        validation_row(
            "VAL1312_3_no_source_backed_balpha",
            "no standalone source-backed b_alpha/c_alpha value is acquired",
            coefficient_acquisition[0]["available_value"] == "NONE"
            and coefficient_acquisition[0]["current_status"] == "MISSING_THEOREM_ZERO_OR_SOURCE_BACKED_COEFFICIENT",
            f"{coefficient_acquisition[0]['acq_id']}={coefficient_acquisition[0]['current_status']}",
        )
    )
    validations.append(
        validation_row(
            "VAL1312_4_product_gates_block",
            "alpha product runner gates block all arena transfers",
            all("MISSING" in row["current_status"] for row in product_runner_gate),
            ";".join(f"{row['gate_id']}={row['current_status']}" for row in product_runner_gate),
        )
    )
    validations.append(
        validation_row(
            "VAL1312_5_thresholds_nonclaim",
            "threshold and product pressure rows remain nonclaim",
            all(row["status"].endswith("NONCLAIM") for row in threshold_policy),
            ";".join(f"{row['policy_id']}={row['status']}" for row in threshold_policy),
        )
    )
    validations.append(
        validation_row(
            "VAL1312_6_claim_gates_block",
            "claim gates block b_alpha, products, and local-GR promotion",
            all(row["current_status"] == "BLOCKED" for row in claim_gates),
            ";".join(f"{row['gate_id']}={row['current_status']}" for row in claim_gates),
        )
    )

    tables = [
        source_register,
        no_f2_proof,
        zqeff_drift,
        coefficient_acquisition,
        product_runner_gate,
        threshold_policy,
        claim_gates,
        decision,
        next_target,
    ]
    output_specs = [
        (SOURCE_REGISTER_PATH, source_register),
        (NO_F2_PROOF_AUDIT_PATH, no_f2_proof),
        (ZQEFF_DRIFT_AUDIT_PATH, zqeff_drift),
        (COEFFICIENT_ACQUISITION_PATH, coefficient_acquisition),
        (PRODUCT_RUNNER_GATE_PATH, product_runner_gate),
        (THRESHOLD_POLICY_PATH, threshold_policy),
        (CLAIM_GATES_PATH, claim_gates),
        (DECISION_PATH, decision),
        (NEXT_PATH, next_target),
    ]
    for path, rows in output_specs:
        write_csv(path, rows)

    parsed_details = []
    csv_parse_ok = True
    for path, _rows in output_specs:
        try:
            parsed_rows = read_csv(path)
            parsed_details.append(f"{path.name}:{len(parsed_rows)}")
        except Exception as exc:  # pragma: no cover - validation ledger path
            csv_parse_ok = False
            parsed_details.append(f"{path.name}:ERROR:{exc}")
    validations.append(
        validation_row(
            "VAL1312_7_csv_parse",
            "all generated CSVs parse cleanly",
            csv_parse_ok,
            "; ".join(parsed_details),
        )
    )
    formalization_outputs = generated_inside_formalization()
    validations.append(
        validation_row(
            "VAL1312_8_formalization_untouched",
            "formalization-workbench untouched by generated outputs",
            len(formalization_outputs) == 0,
            f"formalization_generated_output_count={len(formalization_outputs)}",
        )
    )
    validations.append(
        validation_row(
            "VAL1312_9_nonclaim_policy",
            "all generated rows remain nonclaim",
            all_nonclaim(tables),
            "valid_for_claim=false and claim_allowed=false throughout generated tables",
        )
    )
    validations.append(
        validation_row(
            "VAL1312_10_next_target_1313",
            "next target routes to typed no-hidden-visible coefficient morphism",
            next_target[0]["next_id"] == "NEXT1312_0_1313",
            str(next_target[0]["target_file"]),
        )
    )

    overall_pass = all(row["status"] == "PASS" for row in validations)
    validations.append(
        validation_row(
            "VAL1312_11_overall",
            "overall 1312 validation",
            overall_pass,
            "1312 does not derive b_alpha=0 or source a standalone alpha coefficient; thresholds/products remain nonclaim; next target is typed no-hidden-visible coefficient morphism",
        )
    )
    write_csv(VALIDATION_PATH, validations)

    doc = f"""# {TITLE}

**Current verdict:** `b_alpha/c_alpha` is not theorem-zero and not source-backed. The no-extra-`F_Q^2` route is mathematically clean, but the current corpus still allows `lambda_A F_Q^2`, `f(I_hid)F_Q^2`, and radiative/readout re-entry.

**Main progress:** 1312 compresses the alpha branch into a strict proof/acquisition gate: parent `T_Q`, fixed gauge norm/level, no visible/hidden `F^2` counterterms, same-current owner, and radiative/readout closure must all sign before `b_alpha=0` is claimable.

**Decision:** the next derivation target is the typed no-hidden-visible coefficient morphism theorem. If that fails, alpha must proceed only through finite product inputs under the 1112 runner contract.

## Source Register

{markdown_table(source_register, ["source_id", "local_path", "needle", "exists", "needle_found", "role", "valid_for_claim", "claim_allowed"])}

## b_alpha No-F2 Proof Audit

{markdown_table(no_f2_proof, ["clause_id", "clause", "mathematical_requirement", "current_evidence", "result", "if_signed", "if_missing", "valid_for_claim", "claim_allowed"])}

## ZQeff Drift Clause Audit

{markdown_table(zqeff_drift, ["term_id", "term", "drift_condition", "current_status", "source_anchor", "effect_if_open", "valid_for_claim", "claim_allowed"])}

## Coefficient Acquisition

{markdown_table(coefficient_acquisition, ["acq_id", "quantity", "available_value", "available_bound_or_pressure", "units", "current_status", "why_not_claim", "required_next_input", "valid_for_claim", "claim_allowed"])}

## Product Runner Gate

{markdown_table(product_runner_gate, ["gate_id", "runner_requirement", "current_status", "runner_effect", "valid_for_claim", "claim_allowed"])}

## Threshold Policy

{markdown_table(threshold_policy, ["policy_id", "threshold", "source_family", "allowed_use", "forbidden_use", "status", "valid_for_claim", "claim_allowed"])}

## Claim Gates

{markdown_table(claim_gates, ["gate_id", "claim", "current_status", "reason", "valid_for_claim", "claim_allowed"])}

## Decision Ledger

{markdown_table(decision, ["decision_id", "decision", "because", "next_action", "valid_for_claim", "claim_allowed"])}

## Next Target

{markdown_table(next_target, ["next_id", "target_file", "target_script", "task", "success_condition", "do_not", "valid_for_claim", "claim_allowed"])}

## Validation

{markdown_table(validations, ["check_id", "check", "status", "details"])}
"""
    DOC_PATH.write_text(doc, encoding="utf-8")


if __name__ == "__main__":
    main()

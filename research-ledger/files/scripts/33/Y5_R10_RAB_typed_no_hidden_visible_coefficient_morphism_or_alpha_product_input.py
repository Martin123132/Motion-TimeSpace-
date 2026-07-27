from __future__ import annotations

import csv
from pathlib import Path


PACK_ID = "P8_Y5_R10_1313"
TITLE = "1313-Y5-R10-RAB-typed-no-hidden-visible-coefficient-morphism-or-alpha-product-input"
ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = ROOT / "source-intake" / "mts_residuals"
DOC_PATH = ROOT / f"{TITLE}.md"
FORMALIZATION = ROOT.parent / "formalization-workbench"

SOURCE_REGISTER_PATH = OUT_DIR / f"{PACK_ID}_SOURCE_REGISTER.csv"
TYPED_MORPHISM_AUDIT_PATH = OUT_DIR / f"{PACK_ID}_TYPED_MORPHISM_PROOF_AUDIT.csv"
COUNTEREXAMPLE_LOCK_PATH = OUT_DIR / f"{PACK_ID}_HIDDEN_SCALAR_COUNTEREXAMPLE_LOCK_UPDATE.csv"
ALPHA_PRODUCT_INPUT_PATH = OUT_DIR / f"{PACK_ID}_ALPHA_PRODUCT_INPUT_BRIDGE_NONCLAIM.csv"
CLOSURE_SCOREPACK_PATH = OUT_DIR / f"{PACK_ID}_FINITE_COUPLING_SCOREPACK_QUEUE.csv"
ROUTE_DEMOTION_PATH = OUT_DIR / f"{PACK_ID}_NO_HIDDEN_VISIBLE_ROUTE_DEMOTION.csv"
CLAIM_GATES_PATH = OUT_DIR / f"{PACK_ID}_CLAIM_GATES.csv"
DECISION_PATH = OUT_DIR / f"{PACK_ID}_DECISION_LEDGER.csv"
NEXT_PATH = OUT_DIR / f"{PACK_ID}_NEXT_TARGET.csv"
VALIDATION_PATH = OUT_DIR / "P8_Y5_BRR545_1313_VALIDATION.csv"


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
        TYPED_MORPHISM_AUDIT_PATH,
        COUNTEREXAMPLE_LOCK_PATH,
        ALPHA_PRODUCT_INPUT_PATH,
        CLOSURE_SCOREPACK_PATH,
        ROUTE_DEMOTION_PATH,
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
            "source_id": "SRC1313_0_1312_next",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1312_NEXT_TARGET.csv",
            "needle": "NEXT1312_0_1313",
            "role": "handoff from b_alpha no-vertex gate",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "source_id": "SRC1313_1_1312_balpha",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1312_B_ALPHA_NO_F2_PROOF_AUDIT.csv",
            "needle": "B_ALPHA_THEOREM_ZERO_NOT_DERIVED",
            "role": "b_alpha theorem-zero was not derived",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "source_id": "SRC1313_2_1312_product_gate",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1312_ALPHA_PRODUCT_RUNNER_GATE.csv",
            "needle": "MISSING_R10_FINITE_BRANCH_INPUTS",
            "role": "RAB alpha product gates remain missing",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "source_id": "SRC1313_3_1114_nohom",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1114_NO_HIDDEN_VISIBLE_MORPHISM_THEOREM_ATTEMPT.csv",
            "needle": "NO_HIDDEN_VISIBLE_MORPHISM_NOT_DERIVED",
            "role": "typed/product no-hidden-visible theorem not promoted",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "source_id": "SRC1313_4_1114_obstructions",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1114_COUPLING_OBSTRUCTION_LEDGER.csv",
            "needle": "OBS1114_1_scalar_invariant",
            "role": "surviving scalar obstruction ledger",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "source_id": "SRC1313_5_1114_finite",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1114_FINITE_COUPLING_INPUTS_NONCLAIM.csv",
            "needle": "FCI1114_0_alpha_F2",
            "role": "finite coupling inputs if no-morphism theorem fails",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "source_id": "SRC1313_6_1115_invariant",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1115_LOCAL_INVARIANT_ALGEBRA_TRIVIALITY_ATTEMPT.csv",
            "needle": "LOCAL_INVARIANT_ALGEBRA_TRIVIALITY_NOT_DERIVED",
            "role": "hidden invariant algebra triviality not derived",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "source_id": "SRC1313_7_1115_generators",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1115_GENERATOR_KILL_LIST.csv",
            "needle": "KILL1115_3_memory_scalar",
            "role": "generator kill list retains memory scalar and related debts",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "source_id": "SRC1313_8_1219_functor",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1219_TYPED_VISIBLE_COEFFICIENT_FUNCTOR_ATTEMPT.csv",
            "needle": "TYPED_VISIBLE_COEFFICIENT_FUNCTOR_NOT_DERIVED",
            "role": "later typed visible coefficient functor attempt",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "source_id": "SRC1313_9_1219_counterexamples",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1219_HIDDEN_SCALAR_COUNTEREXAMPLE_LOCK.csv",
            "needle": "HSC1219_1_alpha",
            "role": "hidden scalar counterexample lock",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "source_id": "SRC1313_10_1219_debts",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1219_FINITE_COUPLING_CLOSURE_DEBT_ROWS.csv",
            "needle": "FC1219_0_alpha",
            "role": "finite coupling closure debts",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "source_id": "SRC1313_11_1220_signature",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1220_PARENT_TYPED_SIGNATURE_ATTEMPT.csv",
            "needle": "PARENT_TYPED_OBJECT_LANGUAGE_SIGNATURE_NOT_DERIVED",
            "role": "parent typed object-language certificate attempt",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "source_id": "SRC1313_12_1220_demotion",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1220_NO_HIDDEN_VISIBLE_ROUTE_DEMOTION.csv",
            "needle": "DEM1220_0_route_status",
            "role": "no-hidden-visible route demotion",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "source_id": "SRC1313_13_1220_closure",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1220_FINITE_COUPLING_CLOSURE_REGISTER.csv",
            "needle": "FCCR1220_0_alpha",
            "role": "finite coupling closure register",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "source_id": "SRC1313_14_1113_acq",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1113_ALPHA_PRODUCT_INPUT_ACQUISITION_LEDGER.csv",
            "needle": "AQ1113_4_r10_branch",
            "role": "alpha product input acquisition rows",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]
    for row in source_register:
        exists, needle_found = exists_and_contains(str(row["local_path"]), str(row["needle"]))
        row["exists"] = exists
        row["needle_found"] = needle_found

    typed_morphism_audit = [
        {
            "audit_id": "TMC1313_0_target",
            "claim_piece": "typed no-hidden-visible coefficient morphism",
            "formal_statement": "Coeff_vis(O_vis) has no hidden/local representative argument slot; Hom(C_hid, Coeff(O_vis)) is constant or absent",
            "result": "TARGET_SHARP",
            "proof_or_blocker": "would kill alpha F2, mass/binding, clock/readout, source-weight, and R10 source/test coefficient drift",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "audit_id": "TMC1313_1_type_rule",
            "claim_piece": "syntax forbids hidden arguments",
            "formal_statement": "If parent syntax supplies no morphism C_hid -> Arg(Coeff_vis), terms c(I_hid)O_vis are ill-typed",
            "result": "EXACT_CONDITIONAL_THEOREM",
            "proof_or_blocker": "formal grammar works if parent object language is signed",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "audit_id": "TMC1313_2_product_projection",
            "claim_piece": "visible coefficients factor through visible projection",
            "formal_statement": "C_parent=C_vis x C_hid and coeff_vis=coeff_bar o pi_vis implies Lie_v_hid coeff_vis=0",
            "result": "EXACT_CONDITIONAL_THEOREM",
            "proof_or_blocker": "chain rule closes hidden tangent directions only after product/sequester is parent-derived",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "audit_id": "TMC1313_3_invariant_triviality",
            "claim_piece": "no hidden scalar inputs exist",
            "formal_statement": "O(C_hid)^inv=R so every continuous visible coefficient map from hidden data is constant",
            "result": "EXACT_CONDITIONAL_NOT_DERIVED",
            "proof_or_blocker": "1115 retains surviving generators and scalar counterexamples",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "audit_id": "TMC1313_4_parent_signature",
            "claim_piece": "current corpus signs parent grammar/action domain",
            "formal_statement": "one parent typed object-language certificate signs visible coefficient domains, source weights, no-extension, and measure/readout owners",
            "result": "NOT_DERIVED",
            "proof_or_blocker": "1220 says parent typed object-language signature certificate is not derived",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "audit_id": "TMC1313_5_radiative_readout",
            "claim_piece": "no-morphism survives observed EFT/readout",
            "formal_statement": "S_eff and clock/WEP/R10 readout maps preserve the same typed coefficient domain",
            "result": "UNSIGNED_CRITICAL",
            "proof_or_blocker": "bare grammar, even if clean, does not automatically survive loops, thresholds, spectroscopy, or reduced readout",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "audit_id": "TMC1313_6_verdict",
            "claim_piece": "derive typed no-hidden-visible theorem now",
            "formal_statement": "visible F2/mass/clock/source coefficients cannot take hidden representatives or hidden invariants as arguments",
            "result": "TYPED_NO_HIDDEN_VISIBLE_MORPHISM_NOT_DERIVED_RAB",
            "proof_or_blocker": "1219/1220 already demote this route without a new parent grammar primitive",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    counterexample_lock = [
        {
            "counterexample_id": "HSC1313_0_generic",
            "hidden_input": "I_hid in O(C_hid)^inv with dI_hid != 0",
            "visible_map": "c_vis=c0+epsilon I_hid",
            "visible_operator": "generic visible scalar-density operator",
            "status": "LOCKED_ACTIVE",
            "blocks": "global typed no-hidden-visible theorem",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "counterexample_id": "HSC1313_1_alpha",
            "hidden_input": "I_hid or Xhat",
            "visible_map": "f(I_hid)F_Q^2",
            "visible_operator": "EM kinetic / alpha",
            "status": "LOCKED_ACTIVE",
            "blocks": "b_alpha/c_alpha theorem-zero",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "counterexample_id": "HSC1313_2_mass_surface",
            "hidden_input": "I_hid, marker, or domain scalar",
            "visible_map": "m_A(I_hid), B_A(I_hid), a_surface(I_hid)",
            "visible_operator": "matter mass/binding/surface response",
            "status": "LOCKED_ACTIVE",
            "blocks": "mass/clock/WEP surface coefficient silence",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "counterexample_id": "HSC1313_3_clock_readout",
            "hidden_input": "I_hid after EFT/readout",
            "visible_map": "nu_i(I_hid) or alpha_eff(I_hid)",
            "visible_operator": "clock/spectroscopy readout",
            "status": "LOCKED_ACTIVE",
            "blocks": "clock product transfer and observed alpha silence",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "counterexample_id": "HSC1313_4_source_weight",
            "hidden_input": "marker/domain/source scalar",
            "visible_map": "w_A(I_hid)S_A or kappa_A(I_hid)T_A",
            "visible_operator": "WEP/source-weight/local source coupling",
            "status": "LOCKED_ACTIVE",
            "blocks": "WEP/R10 source-side theorem-zero and local-GR source branch",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    alpha_product_input = [
        {
            "input_id": "API1313_0_balpha_or_zero",
            "product_row": "APC1112_0/APC1112_1/APC1112_2",
            "needed_input": "b_alpha theorem-zero or numeric source-backed coefficient",
            "current_status": "MISSING_THEOREM_ZERO_OR_NUMERIC_COEFFICIENT",
            "best_available_pressure": "abs(c_alpha_DD) <= 8.3202449332435330e-10 threshold only",
            "claim_effect": "all alpha product claims blocked",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "input_id": "API1313_1_clock",
            "product_row": "P_clock_alpha=b_alpha*tau_clock_time",
            "needed_input": "tau_clock_time/Xhat map or direct MTS clock product prediction",
            "current_status": "MISSING_CLOCK_READOUT_MAP",
            "best_available_pressure": "source-backed product bound 2.1e-18 yr^-1",
            "claim_effect": "clock bound cannot become standalone b_alpha",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "input_id": "API1313_2_wep",
            "product_row": "P_WEP_alpha=beta_source_alpha*b_alpha*tau_WEP",
            "needed_input": "beta_source_alpha, tau_WEP, material/readout map, or direct eta product theorem",
            "current_status": "MISSING_SOURCE_NORMALIZATION_AND_TAU_WEP",
            "best_available_pressure": "WEP alpha/Coulomb pressure target 4.7977805227320001e-05",
            "claim_effect": "WEP alpha product cannot score",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "input_id": "API1313_3_r10",
            "product_row": "P_R10_alpha(lambda)",
            "needed_input": "lambda_X, Z_X, K_X, beta_source, beta_test, tau_R10, epsilon_tail, promoted alpha_bound(lambda)",
            "current_status": "MISSING_R10_FINITE_BRANCH_INPUTS",
            "best_available_pressure": "symbolic/anchor-only rows are not claim-valid",
            "claim_effect": "R10 alpha product cannot score",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "input_id": "API1313_4_cross_arena",
            "product_row": "shared alpha descent/product consistency",
            "needed_input": "same Z_Q_eff branch and readout/domain classifier across clock/WEP/R10",
            "current_status": "MISSING_CROSS_ARENA_PARENT_MAP",
            "best_available_pressure": "separate clock/WEP/R10 pressure rows only",
            "claim_effect": "no transfer shortcut between arenas",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    closure_scorepack = [
        {
            "queue_id": "FSQ1313_0_alpha",
            "closure_debt": "c_alpha_DD / b_alpha",
            "retained_counterexample": "HSC1313_1_alpha",
            "scorepack_schema": "coefficient_value;units;branch_id;source_path;normalization;arena_projection;valid_for_claim",
            "current_status": "SOURCE_ACQUISITION_NEEDED",
            "do_not": "do not use threshold as coefficient value",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "queue_id": "FSQ1313_1_clock",
            "closure_debt": "b_alpha*tau_clock_time or direct readout product",
            "retained_counterexample": "HSC1313_3_clock_readout",
            "scorepack_schema": "direct_product_or_tau_map;clock_pair;readout_model;units;source_path;valid_for_claim",
            "current_status": "SOURCE_ACQUISITION_NEEDED",
            "do_not": "do not divide by assumed tau_clock",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "queue_id": "FSQ1313_2_wep",
            "closure_debt": "beta_source_alpha*tau_WEP/material map",
            "retained_counterexample": "HSC1313_4_source_weight",
            "scorepack_schema": "beta_source_alpha;tau_WEP;material_pair;DeltaQ_alpha;source_path;valid_for_claim",
            "current_status": "SOURCE_ACQUISITION_NEEDED",
            "do_not": "do not set beta_source_alpha or tau_WEP to unity",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "queue_id": "FSQ1313_3_r10",
            "closure_debt": "finite R10 alpha product vector",
            "retained_counterexample": "HSC1313_1_alpha;HSC1313_4_source_weight",
            "scorepack_schema": "lambda_X;Z_X;K_X;beta_source;beta_test;tau_R10;alpha_bound_lambda;source_path;valid_for_claim",
            "current_status": "SOURCE_ACQUISITION_NEEDED",
            "do_not": "do not run symbolic R10 rows as claims",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "queue_id": "FSQ1313_4_parent_primitive",
            "closure_debt": "new parent grammar primitive source",
            "retained_counterexample": "all HSC1313 rows",
            "scorepack_schema": "primitive_statement;parent_action_clause;typed_domain_rule;readout_closure;source_path;valid_for_claim",
            "current_status": "NEW_PRIMITIVE_SOURCE_REQUIRED_TO_REOPEN_THEOREM_ROUTE",
            "do_not": "do not re-argue aesthetic minimality as proof",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    route_demotion = [
        {
            "demotion_id": "DEM1313_0_route",
            "route": "typed no-hidden-visible coefficient morphism",
            "status": "DEMOTED_TO_FINITE_CLOSURE_UNLESS_NEW_PARENT_PRIMITIVE",
            "because": "1219/1220 prove only conditional grammar theorems and retain active hidden-scalar counterexamples",
            "effect": "RAB alpha branch must use theorem-zero only if new primitive appears; otherwise finite product/acquisition rows",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "demotion_id": "DEM1313_1_hidden_scalar",
            "route": "hidden scalar obstruction",
            "status": "COUNTEREXAMPLE_LOCKED",
            "because": "surviving invariant scalar can feed continuous visible coefficients",
            "effect": "alpha, mass/surface, clock, and source-weight rows carry explicit finite closure debts",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "demotion_id": "DEM1313_2_local_GR",
            "route": "local GR/Newton source-side closure",
            "status": "STILL_SEPARATE_BLOCKED_BRANCH",
            "because": "typed grammar would help source coupling but does not replace EH/source Hamiltonian/PPN gates",
            "effect": "no local-GR claim follows from 1313",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    claim_gates = [
        {
            "gate_id": "CG1313_0_typed_morphism",
            "claim": "typed no-hidden-visible morphism is derived",
            "status": "BLOCKED",
            "reason": "TMC1313_6_verdict=TYPED_NO_HIDDEN_VISIBLE_MORPHISM_NOT_DERIVED_RAB",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "gate_id": "CG1313_1_counterexamples",
            "claim": "hidden scalar counterexamples are removed",
            "status": "BLOCKED",
            "reason": "HSC1313 rows remain active",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "gate_id": "CG1313_2_alpha_products",
            "claim": "alpha product rows are score-ready",
            "status": "BLOCKED",
            "reason": "API1313 rows keep b_alpha/tau/source/R10/cross-arena inputs missing",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "gate_id": "CG1313_3_local_GR",
            "claim": "local GR/Newton is closed from typed grammar",
            "status": "BLOCKED",
            "reason": "typed grammar is not signed and independent EH/source Hamiltonian/PPN gates remain",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    decision = [
        {
            "decision_id": "DEC1313_0_no_relitigation",
            "decision": "do not re-argue the same unsigned typed grammar as proof",
            "because": "1219/1220 already show the theorem is exact conditionally but not parent-signed",
            "next_action": "either find a genuinely new parent grammar primitive source or move to finite coupling scorepack acquisition",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "decision_id": "DEC1313_1_RAB_alpha",
            "decision": "RAB alpha branch inherits the hidden-scalar counterexample lock",
            "because": "f(I_hid)F_Q^2 remains legal without the typed grammar/invariant-triviality/radiative closure package",
            "next_action": "build alpha/clock/WEP/R10 scorepack rows without using thresholds as predictions",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    next_target = [
        {
            "next_id": "NEXT1313_0_1314",
            "target_file": "1314-Y5-R10-RAB-finite-alpha-coupling-scorepack-or-parent-primitive-source.md",
            "target_script": "scripts/Y5_R10_RAB_finite_alpha_coupling_scorepack_or_parent_primitive_source.py",
            "task": "turn alpha/clock/WEP/R10 finite coupling closure debts into source-acquisition scorepack rows, while preserving an escape hatch for a genuinely new parent grammar primitive",
            "success_condition": "each retained coupling debt has a source-ready schema and claim gate, or a new parent primitive source reopens the theorem route",
            "do_not": "do not claim local GR/R10/WEP; do not use thresholds or absence in a clean action as predictions",
            "valid_for_claim": False,
            "claim_allowed": False,
        }
    ]

    output_specs = [
        (SOURCE_REGISTER_PATH, source_register),
        (TYPED_MORPHISM_AUDIT_PATH, typed_morphism_audit),
        (COUNTEREXAMPLE_LOCK_PATH, counterexample_lock),
        (ALPHA_PRODUCT_INPUT_PATH, alpha_product_input),
        (CLOSURE_SCOREPACK_PATH, closure_scorepack),
        (ROUTE_DEMOTION_PATH, route_demotion),
        (CLAIM_GATES_PATH, claim_gates),
        (DECISION_PATH, decision),
        (NEXT_PATH, next_target),
    ]
    for path, rows in output_specs:
        write_csv(path, rows)

    validations: list[dict[str, object]] = []
    validations.append(
        validation_row(
            "VAL1313_0_sources_exist",
            "registered source paths exist and anchors are found",
            all(row["exists"] and row["needle_found"] for row in source_register),
            f"{sum(1 for row in source_register if row['exists'] and row['needle_found'])}/{len(source_register)} source anchors found",
        )
    )
    validations.append(
        validation_row(
            "VAL1313_1_typed_not_derived",
            "typed no-hidden-visible morphism is not promoted",
            typed_morphism_audit[-1]["result"] == "TYPED_NO_HIDDEN_VISIBLE_MORPHISM_NOT_DERIVED_RAB",
            ";".join(f"{row['audit_id']}={row['result']}" for row in typed_morphism_audit),
        )
    )
    validations.append(
        validation_row(
            "VAL1313_2_counterexamples_locked",
            "hidden scalar counterexamples remain locked active",
            all(row["status"] == "LOCKED_ACTIVE" for row in counterexample_lock),
            ";".join(row["counterexample_id"] for row in counterexample_lock),
        )
    )
    validations.append(
        validation_row(
            "VAL1313_3_alpha_inputs_missing",
            "alpha product bridge keeps required inputs missing",
            all("MISSING" in row["current_status"] for row in alpha_product_input),
            ";".join(f"{row['input_id']}={row['current_status']}" for row in alpha_product_input),
        )
    )
    validations.append(
        validation_row(
            "VAL1313_4_scorepack_queue_nonclaim",
            "finite coupling scorepack queue is source-acquisition only",
            all(row["current_status"].endswith("NEEDED") or row["current_status"].startswith("NEW_PRIMITIVE") for row in closure_scorepack),
            ";".join(f"{row['queue_id']}={row['current_status']}" for row in closure_scorepack),
        )
    )
    validations.append(
        validation_row(
            "VAL1313_5_route_demoted",
            "no-hidden-visible route demoted unless new primitive source appears",
            route_demotion[0]["status"] == "DEMOTED_TO_FINITE_CLOSURE_UNLESS_NEW_PARENT_PRIMITIVE",
            ";".join(f"{row['demotion_id']}={row['status']}" for row in route_demotion),
        )
    )
    validations.append(
        validation_row(
            "VAL1313_6_claim_gates_block",
            "claim gates block typed theorem, products, and local-GR promotion",
            all(row["status"] == "BLOCKED" for row in claim_gates),
            ";".join(f"{row['gate_id']}={row['status']}" for row in claim_gates),
        )
    )

    parsed_details = []
    csv_parse_ok = True
    for path, _rows in output_specs:
        try:
            parsed_rows = read_csv(path)
            parsed_details.append(f"{path.name}:{len(parsed_rows)}")
        except Exception as exc:  # pragma: no cover
            csv_parse_ok = False
            parsed_details.append(f"{path.name}:ERROR:{exc}")
    validations.append(
        validation_row(
            "VAL1313_7_csv_parse",
            "all generated CSVs parse cleanly",
            csv_parse_ok,
            "; ".join(parsed_details),
        )
    )
    formalization_outputs = generated_inside_formalization()
    validations.append(
        validation_row(
            "VAL1313_8_formalization_untouched",
            "formalization-workbench untouched by generated outputs",
            len(formalization_outputs) == 0,
            f"formalization_generated_output_count={len(formalization_outputs)}",
        )
    )
    tables = [
        source_register,
        typed_morphism_audit,
        counterexample_lock,
        alpha_product_input,
        closure_scorepack,
        route_demotion,
        claim_gates,
        decision,
        next_target,
    ]
    validations.append(
        validation_row(
            "VAL1313_9_nonclaim_policy",
            "all generated rows remain nonclaim",
            all_nonclaim(tables),
            "valid_for_claim=false and claim_allowed=false throughout generated tables",
        )
    )
    validations.append(
        validation_row(
            "VAL1313_10_next_target_1314",
            "next target routes to finite alpha coupling scorepack or parent primitive source",
            next_target[0]["next_id"] == "NEXT1313_0_1314",
            str(next_target[0]["target_file"]),
        )
    )
    overall_pass = all(row["status"] == "PASS" for row in validations)
    validations.append(
        validation_row(
            "VAL1313_11_overall",
            "overall 1313 validation",
            overall_pass,
            "1313 bridges the typed-morphism route into RAB: theorem remains unsigned, counterexamples stay locked, and next work is finite alpha coupling scorepack or new parent primitive source",
        )
    )
    write_csv(VALIDATION_PATH, validations)

    doc = f"""# {TITLE}

**Current verdict:** 1313 does not derive the typed no-hidden-visible coefficient morphism theorem. It imports the stronger 1219/1220 result into the RAB branch: the typed theorem is exact if signed, but the current corpus lacks the parent grammar/action-domain certificate and keeps hidden-scalar counterexamples active.

**Main progress:** the RAB alpha/coupling branch now has a clean fork. Either a genuinely new parent grammar primitive signs the no-hidden-argument rule, or alpha/clock/WEP/R10 coupling debts move into finite source-acquisition scorepack rows.

**Decision:** stop re-litigating aesthetic minimality. `f(I_hid)F_Q^2`, clock/readout drift, and source-weight maps remain live until killed by a parent primitive or replaced by source-backed finite products.

## Source Register

{markdown_table(source_register, ["source_id", "local_path", "needle", "exists", "needle_found", "role", "valid_for_claim", "claim_allowed"])}

## Typed Morphism Proof Audit

{markdown_table(typed_morphism_audit, ["audit_id", "claim_piece", "formal_statement", "result", "proof_or_blocker", "valid_for_claim", "claim_allowed"])}

## Counterexample Lock

{markdown_table(counterexample_lock, ["counterexample_id", "hidden_input", "visible_map", "visible_operator", "status", "blocks", "valid_for_claim", "claim_allowed"])}

## Alpha Product Input Bridge

{markdown_table(alpha_product_input, ["input_id", "product_row", "needed_input", "current_status", "best_available_pressure", "claim_effect", "valid_for_claim", "claim_allowed"])}

## Finite Coupling Scorepack Queue

{markdown_table(closure_scorepack, ["queue_id", "closure_debt", "retained_counterexample", "scorepack_schema", "current_status", "do_not", "valid_for_claim", "claim_allowed"])}

## Route Demotion

{markdown_table(route_demotion, ["demotion_id", "route", "status", "because", "effect", "valid_for_claim", "claim_allowed"])}

## Claim Gates

{markdown_table(claim_gates, ["gate_id", "claim", "status", "reason", "valid_for_claim", "claim_allowed"])}

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

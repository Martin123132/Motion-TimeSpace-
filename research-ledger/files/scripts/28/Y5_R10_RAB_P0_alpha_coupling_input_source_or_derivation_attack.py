from __future__ import annotations

import csv
from pathlib import Path


PACK_ID = "P8_Y5_R10_1316"
TITLE = "1316-Y5-R10-RAB-P0-alpha-coupling-input-source-or-derivation-attack"
ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = ROOT / "source-intake" / "mts_residuals"
DOC_PATH = ROOT / f"{TITLE}.md"
FORMALIZATION = ROOT.parent / "formalization-workbench"

SOURCE_REGISTER_PATH = OUT_DIR / f"{PACK_ID}_SOURCE_REGISTER.csv"
BLOCKER_IMPORT_PATH = OUT_DIR / f"{PACK_ID}_P0_BLOCKER_IMPORT.csv"
DERIVATION_ATTACK_PATH = OUT_DIR / f"{PACK_ID}_P0_DERIVATION_ATTACK_LEDGER.csv"
PRODUCT_FORMULA_PATH = OUT_DIR / f"{PACK_ID}_P0_PRODUCT_FORMULA_REQUIREMENTS.csv"
SOURCE_REQUIREMENT_PATH = OUT_DIR / f"{PACK_ID}_P0_SOURCE_REQUIREMENT_LEDGER.csv"
COUNTEREXAMPLE_PATH = OUT_DIR / f"{PACK_ID}_COUNTEREXAMPLE_DISPOSITION.csv"
PROMOTION_GATES_PATH = OUT_DIR / f"{PACK_ID}_PROMOTION_GATES.csv"
DECISION_PATH = OUT_DIR / f"{PACK_ID}_DECISION_LEDGER.csv"
NEXT_PATH = OUT_DIR / f"{PACK_ID}_NEXT_TARGET.csv"
VALIDATION_PATH = OUT_DIR / "P8_Y5_BRR545_1316_VALIDATION.csv"


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
        BLOCKER_IMPORT_PATH,
        DERIVATION_ATTACK_PATH,
        PRODUCT_FORMULA_PATH,
        SOURCE_REQUIREMENT_PATH,
        COUNTEREXAMPLE_PATH,
        PROMOTION_GATES_PATH,
        DECISION_PATH,
        NEXT_PATH,
        VALIDATION_PATH,
        DOC_PATH,
    ]
    return [path for path in generated_paths if FORMALIZATION in path.parents]


def compact_bool(value: object) -> bool:
    return str(value).strip().lower() == "true"


def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)

    source_register = [
        {
            "source_id": "SRC1316_0_1315_next",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1315_NEXT_TARGET.csv",
            "needle": "NEXT1315_0_1316",
            "role": "handoff into P0 alpha coupling derivation/source attack",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "source_id": "SRC1316_1_1315_blockers",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1315_MISSING_INPUT_BLOCKER_LEDGER.csv",
            "needle": "BLK1315_3_0",
            "role": "P0 blocker inventory",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "source_id": "SRC1316_2_1315_score",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1315_FIRST_NONCLAIM_SCORE_TABLE.csv",
            "needle": "NCS1315_3_3_r10",
            "role": "current nonclaim score table",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "source_id": "SRC1316_3_1315_shortcuts",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1315_ANTI_SHORTCUT_GATES.csv",
            "needle": "SHORT1315_1_no_threshold_prediction",
            "role": "anti-shortcut policy",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "source_id": "SRC1316_4_1315_r10",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1315_R10_REFUSAL_DETAIL.csv",
            "needle": "R10REF1315_3_decision",
            "role": "R10 refusal detail",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "source_id": "SRC1316_5_1314_parent",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1314_PARENT_PRIMITIVE_ESCAPE_HATCH.csv",
            "needle": "PESC1314_1_alpha_F2",
            "role": "parent primitive escape hatch state",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "source_id": "SRC1316_6_1314_schema",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1314_ALPHA_SCOREPACK_INPUT_SCHEMA.csv",
            "needle": "AS1314_3_r10_vector",
            "role": "scorepack input schema",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "source_id": "SRC1316_7_1313_hsc",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1313_HIDDEN_SCALAR_COUNTEREXAMPLE_LOCK_UPDATE.csv",
            "needle": "HSC1313_1_alpha",
            "role": "hidden scalar and source/readout counterexamples",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "source_id": "SRC1316_8_1312_balpha",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1312_B_ALPHA_NO_F2_PROOF_AUDIT.csv",
            "needle": "B_ALPHA_THEOREM_ZERO_NOT_DERIVED",
            "role": "b_alpha theorem-zero failure state",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]
    for row in source_register:
        exists, needle_found = exists_and_contains(str(row["local_path"]), str(row["needle"]))
        row["exists"] = exists
        row["needle_found"] = needle_found

    prior_blockers = read_csv(source_path("source-intake/mts_residuals/P8_Y5_R10_1315_MISSING_INPUT_BLOCKER_LEDGER.csv"))
    blocker_import = []
    p0_blockers = []
    for row in prior_blockers:
        imported = {
            "import_id": f"IMP1316_{len(blocker_import)}",
            "source_blocker_id": row.get("blocker_id", ""),
            "runner_row_id": row.get("runner_row_id", ""),
            "blocker_token": row.get("blocker_token", ""),
            "blocker_source": row.get("blocker_source", ""),
            "priority": "P0" if row.get("runner_row_id", "") in {"RUN1314_0_alpha", "RUN1314_1_clock", "RUN1314_2_wep", "RUN1314_3_r10"} else "P1",
            "current_disposition": "ATTACKED_IN_1316",
            "valid_for_claim": False,
            "claim_allowed": False,
        }
        blocker_import.append(imported)
        if imported["priority"] == "P0":
            p0_blockers.append(imported)

    derivation_attack = [
        {
            "attack_id": "DVA1316_0_alpha_F2",
            "target": "b_alpha/c_alpha theorem-zero",
            "p0_blockers": "BLK1315_0_0;BLK1315_0_counterexample",
            "attempted_derivation": "If the EM kinetic coefficient Z_Q_eff descends through the visible quotient and hidden vertical generators act trivially, then L_v Z_Q_eff=0 and the hidden-branch alpha coefficient vanishes after fixed current normalization.",
            "conditional_result": "EXACT_IF_PARENT_SIGNED",
            "obstruction": "PESC1314_1_alpha_F2 is counterexample-active; HSC1313_1_alpha permits f(I_hid)F_Q^2; radiative/readout closure is not signed.",
            "output_formula_if_not_zero": "P_alpha=abs(b_alpha or c_alpha_DD)",
            "required_source_fill": "numeric b_alpha/c_alpha with units, branch, normalization, source path, or a signed parent primitive killing f(I_hid)F_Q^2 and readout regeneration",
            "promotion_status": "NOT_PROMOTED",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "attack_id": "DVA1316_1_clock_readout",
            "target": "clock alpha product",
            "p0_blockers": "BLK1315_1_0;BLK1315_1_counterexample",
            "attempted_derivation": "A clock row is derivable only after a readout functor maps the parent alpha branch into the measured transition frequencies and fixes the sensitivity/readout kernel.",
            "conditional_result": "EXACT_IF_READOUT_SIGNED",
            "obstruction": "HSC1313_3_clock_readout remains active; the source-backed clock product bound is not a standalone b_alpha value.",
            "output_formula_if_not_zero": "P_clock_alpha=abs(b_alpha*tau_clock_time) or direct sourced P_clock_alpha",
            "required_source_fill": "tau_clock_time or direct P_clock_alpha with clock pair, alpha sensitivity/readout model, time units, branch, and source path",
            "promotion_status": "NOT_PROMOTED",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "attack_id": "DVA1316_2_wep_source",
            "target": "WEP alpha/source product",
            "p0_blockers": "BLK1315_2_0;BLK1315_2_counterexample",
            "attempted_derivation": "A WEP row is derivable only if the same parent alpha branch fixes source normalization, test-body material response, and readout kernel rather than setting any factor to unity.",
            "conditional_result": "EXACT_IF_SOURCE_MAP_SIGNED",
            "obstruction": "HSC1313_4_source_weight remains active; beta_source_alpha, tau_WEP, material DeltaQ_alpha, readout kernel, and source profile are not parent-signed.",
            "output_formula_if_not_zero": "P_WEP_alpha=abs(beta_source_alpha*b_alpha*tau_WEP*DeltaQ_alpha_AB) or direct sourced P_WEP_alpha",
            "required_source_fill": "beta_source_alpha, b_alpha/theorem-zero, tau_WEP, material pair, DeltaQ_alpha_AB, source/worldtube profile, readout kernel, and source paths",
            "promotion_status": "NOT_PROMOTED",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "attack_id": "DVA1316_3_r10_product",
            "target": "R10 alpha(lambda) product",
            "p0_blockers": "BLK1315_3_0;BLK1315_3_counterexample",
            "attempted_derivation": "A short-range row is derivable only if the parent branch supplies a finite Yukawa/profile vector and a promoted empirical alpha_bound(lambda) curve exists for comparison.",
            "conditional_result": "EXACT_IF_BRANCH_VECTOR_AND_BOUND_SIGNED",
            "obstruction": "R10REF1315 keeps numeric product, promoted bound curve, and source/test projection missing; HSC1313_1_alpha and HSC1313_4_source_weight stay active.",
            "output_formula_if_not_zero": "P_R10_alpha(lambda)=abs(Z_X*K_X(lambda)*beta_source(lambda)*beta_test(lambda)*tau_R10*epsilon_tail)",
            "required_source_fill": "lambda_X, Z_X, K_X(lambda), beta_source(lambda), beta_test(lambda), tau_R10, epsilon_tail, promoted alpha_bound(lambda), and source paths",
            "promotion_status": "NOT_PROMOTED",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "attack_id": "DVA1316_4_cross_arena",
            "target": "shared alpha branch transfer",
            "p0_blockers": "BLK1315_4_0;BLK1315_4_counterexample",
            "attempted_derivation": "Cross-arena transfer is derivable only if one parent branch classifier and readout functor generate the clock, WEP, R10, and local products with stated arena projections.",
            "conditional_result": "EXACT_IF_PARENT_BRANCH_FUNCTOR_SIGNED",
            "obstruction": "The current rows are separate pressure/threshold rows; no same-branch readout functor is signed.",
            "output_formula_if_not_zero": "same_branch_id plus arena maps F_clock,F_WEP,F_R10,F_local with no threshold transfer",
            "required_source_fill": "branch classifier, readout functor, arena product maps, and explicit statement of which products can and cannot transfer",
            "promotion_status": "NOT_PROMOTED",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "attack_id": "DVA1316_5_parent_primitive",
            "target": "new parent grammar primitive",
            "p0_blockers": "PESC1314_0_parent_primitive;PROM1315_5_parent_primitive",
            "attempted_derivation": "A new primitive would close P0 if it signs typed visible coefficient domains, forbids hidden scalar arguments, and proves radiative/readout preservation under descent.",
            "conditional_result": "EXACT_CONTRACT_WRITTEN_NOT_SOURCE_SIGNED",
            "obstruction": "No source-backed primitive clause is present in the current corpus.",
            "output_formula_if_not_zero": "not a numeric product; theorem-zero route only if parent object-language certificate exists",
            "required_source_fill": "primitive statement, parent action clause, typed coefficient-domain rule, no-hidden-argument rule, radiative closure, readout closure, source path",
            "promotion_status": "NOT_PROMOTED",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    product_formula = [
        {
            "formula_id": "FORM1316_0_alpha",
            "runner_row_id": "RUN1314_0_alpha",
            "canonical_product": "P_alpha=abs(b_alpha or c_alpha_DD)",
            "minimum_inputs": "b_alpha_or_c_alpha;units;branch_id;normalization;source_path;or theorem_zero_certificate",
            "current_available": "threshold_abs_only",
            "why_not_numeric": "threshold is a comparison fence, not a prediction",
            "promotion_rule": "numeric source-backed coefficient or signed theorem-zero",
            "score_ready": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "formula_id": "FORM1316_1_clock",
            "runner_row_id": "RUN1314_1_clock",
            "canonical_product": "P_clock_alpha=abs(b_alpha*tau_clock_time) or direct P_clock_alpha",
            "minimum_inputs": "b_alpha_or_zero;tau_clock_time;clock_pair;readout_model;units;source_path",
            "current_available": "clock_bound_only",
            "why_not_numeric": "tau/readout map missing; product bound cannot be divided by assumed tau",
            "promotion_rule": "direct numeric product or signed tau/readout map",
            "score_ready": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "formula_id": "FORM1316_2_wep",
            "runner_row_id": "RUN1314_2_wep",
            "canonical_product": "P_WEP_alpha=abs(beta_source_alpha*b_alpha*tau_WEP*DeltaQ_alpha_AB) or direct P_WEP_alpha",
            "minimum_inputs": "beta_source_alpha;b_alpha_or_zero;tau_WEP;DeltaQ_alpha_AB;material_pair;source_profile;readout_kernel;source_path",
            "current_available": "pressure_target_only",
            "why_not_numeric": "source normalization, material response, and tau/readout are missing",
            "promotion_rule": "direct numeric WEP product or every factor sourced/derived",
            "score_ready": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "formula_id": "FORM1316_3_r10",
            "runner_row_id": "RUN1314_3_r10",
            "canonical_product": "P_R10_alpha(lambda)=abs(Z_X*K_X(lambda)*beta_source(lambda)*beta_test(lambda)*tau_R10*epsilon_tail)",
            "minimum_inputs": "lambda_X;Z_X;K_X(lambda);beta_source(lambda);beta_test(lambda);tau_R10;epsilon_tail;alpha_bound_lambda;source_path",
            "current_available": "review_candidate_or_anchor_only_nonclaim",
            "why_not_numeric": "finite product vector and promoted claim-valid alpha_bound(lambda) curve are missing",
            "promotion_rule": "numeric source-backed product and promoted bound curve",
            "score_ready": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "formula_id": "FORM1316_4_cross_arena",
            "runner_row_id": "RUN1314_4_cross_arena",
            "canonical_product": "same_branch_id plus arena maps F_clock,F_WEP,F_R10,F_local",
            "minimum_inputs": "parent_branch_classifier;readout_functor;arena_product_maps;nontransfer_statement",
            "current_available": "separate_pressure_rows_only",
            "why_not_numeric": "no signed common branch map; arena thresholds cannot be transferred",
            "promotion_rule": "one signed parent branch/readout map or explicit separate-product declaration",
            "score_ready": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    source_requirements = [
        ("REQ1316_0_balpha", "b_alpha/c_alpha", "alpha;clock;WEP;R10", "numeric coefficient or theorem-zero certificate", "MISSING_SOURCE_BACKED_COEFFICIENT_OR_PARENT_PRIMITIVE"),
        ("REQ1316_1_norm", "fixed EM current normalization", "alpha", "normalization convention and branch id", "MISSING_NORMALIZATION_SOURCE"),
        ("REQ1316_2_no_hidden", "no-hidden visible coefficient primitive", "alpha;WEP;R10", "typed parent object-language rule", "MISSING_PARENT_PRIMITIVE"),
        ("REQ1316_3_radiative", "radiative/readout closure", "alpha;clock", "closure proof that loops/readout do not regenerate F_Q^2 coefficient", "MISSING_RADIATIVE_READOUT_CLOSURE"),
        ("REQ1316_4_tau_clock", "tau_clock_time", "clock", "clock readout projection or direct product", "MISSING_CLOCK_READOUT_MAP"),
        ("REQ1316_5_clock_model", "clock sensitivity/readout model", "clock", "clock pair, sensitivity vector, units, source path", "MISSING_CLOCK_MODEL"),
        ("REQ1316_6_beta_source", "beta_source_alpha", "WEP;R10", "source normalization coefficient as function of parent branch", "MISSING_SOURCE_NORMALIZATION"),
        ("REQ1316_7_tau_wep", "tau_WEP", "WEP", "WEP branch projection/readout factor", "MISSING_TAU_WEP"),
        ("REQ1316_8_material", "DeltaQ_alpha_AB/material map", "WEP", "material pair response and readout kernel", "MISSING_MATERIAL_RESPONSE"),
        ("REQ1316_9_source_profile", "source/worldtube profile", "WEP;R10;local", "finite source profile and domain", "MISSING_SOURCE_PROFILE"),
        ("REQ1316_10_lambda", "lambda_X", "R10", "range scale with units and branch id", "MISSING_LAMBDA_X"),
        ("REQ1316_11_ZX", "Z_X", "R10", "branch amplitude/normalization", "MISSING_Z_X"),
        ("REQ1316_12_KX", "K_X(lambda)", "R10", "kernel or profile factor as lambda function", "MISSING_K_X"),
        ("REQ1316_13_beta_test", "beta_test(lambda)", "R10", "test-body coupling/readout factor", "MISSING_BETA_TEST"),
        ("REQ1316_14_tail", "epsilon_tail", "R10", "finite-size/tail correction convention", "MISSING_EPSILON_TAIL"),
        ("REQ1316_15_bound", "alpha_bound(lambda)", "R10", "digitized/source-backed promoted bound curve", "MISSING_PROMOTED_BOUND_CURVE"),
        ("REQ1316_16_branch", "parent branch classifier", "cross_arena", "shared branch id and arena maps", "MISSING_CROSS_ARENA_PARENT_MAP"),
    ]
    source_requirement_rows = [
        {
            "requirement_id": req_id,
            "needed_object": needed_object,
            "arena": arena,
            "minimum_usable_form": minimum_usable_form,
            "current_status": status,
            "resolution_type": "derive_or_source",
            "valid_for_claim": False,
            "claim_allowed": False,
        }
        for req_id, needed_object, arena, minimum_usable_form, status in source_requirements
    ]

    counterexample_disposition = [
        {
            "counterexample_id": "HSC1313_1_alpha",
            "blocks": "b_alpha/c_alpha theorem-zero and R10 alpha product",
            "1316_disposition": "ACTIVE",
            "reason": "f(I_hid)F_Q^2 remains legal without parent no-hidden/radiative/readout primitive",
            "required_to_close": "signed typed coefficient-domain primitive or source-backed finite coefficient",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "counterexample_id": "HSC1313_3_clock_readout",
            "blocks": "clock product transfer",
            "1316_disposition": "ACTIVE",
            "reason": "readout can reintroduce alpha dependence after EFT/spectroscopy",
            "required_to_close": "signed readout functor or direct P_clock_alpha source",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "counterexample_id": "HSC1313_4_source_weight",
            "blocks": "WEP/R10 source-side theorem-zero and local source branch",
            "1316_disposition": "ACTIVE",
            "reason": "source-only species weights remain syntactically possible",
            "required_to_close": "signed source-normalization theorem or source-backed beta/tau/material rows",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "counterexample_id": "R10REF1315_product_bound_source",
            "blocks": "R10 claim row",
            "1316_disposition": "ACTIVE",
            "reason": "numeric R10 product, promoted alpha_bound(lambda), and source/test projection are all missing",
            "required_to_close": "complete R10 product vector plus promoted bound curve",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    promotion_gates = [
        {
            "gate_id": "GATE1316_0_parent_theorem",
            "gate": "parent theorem-zero route",
            "must_have": "typed visible coefficient domain, no hidden scalar arguments, fixed normalization, radiative/readout closure",
            "current_status": "BLOCKED",
            "claim_rule": "theorem-zero cannot be claimed from minimality or absence in a chosen effective action",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "gate_id": "GATE1316_1_numeric_prediction",
            "gate": "finite numeric product route",
            "must_have": "numeric predicted_abs_value with units, branch, source path, and no MISSING tokens",
            "current_status": "BLOCKED",
            "claim_rule": "thresholds and bounds are comparison fences, never predictions",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "gate_id": "GATE1316_2_clock",
            "gate": "clock row",
            "must_have": "tau_clock_time/readout map or direct clock product",
            "current_status": "BLOCKED",
            "claim_rule": "clock product bound cannot be divided by assumed tau",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "gate_id": "GATE1316_3_wep_source",
            "gate": "WEP/source row",
            "must_have": "source normalization, tau_WEP, material response, source profile, readout kernel",
            "current_status": "BLOCKED",
            "claim_rule": "beta_source_alpha and tau_WEP cannot be set to unity",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "gate_id": "GATE1316_4_r10",
            "gate": "R10 row",
            "must_have": "finite R10 product vector and promoted alpha_bound(lambda) curve",
            "current_status": "BLOCKED",
            "claim_rule": "review-candidate or anchor-only bounds remain nonclaim",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "gate_id": "GATE1316_5_cross_arena",
            "gate": "cross-arena transfer",
            "must_have": "same parent branch classifier and arena readout maps",
            "current_status": "BLOCKED",
            "claim_rule": "clock/WEP/R10 products do not transfer without signed functor",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    decisions = [
        {
            "decision_id": "DEC1316_0_derivation",
            "decision": "P0 coupling derivation attempted but not promoted",
            "because": "all theorem-zero routes remain exact conditionals with active hidden-scalar/readout/source counterexamples",
            "next_action": "use the product formulas and source ledger as the exact intake contract",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "decision_id": "DEC1316_1_contract",
            "decision": "P0 coupling is now equation-shaped",
            "because": "alpha, clock, WEP, R10, and cross-arena rows have explicit product forms and minimum input lists",
            "next_action": "build a source-intake template/runner that can accept real coefficients or theorem-zero certificates without hand edits",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "decision_id": "DEC1316_2_no_claim",
            "decision": "no R10/WEP/clock/local-GR claim",
            "because": "no P0 blocker was closed by proof or sourced numeric input",
            "next_action": "1317 should turn this into a fillable input template and priority runner",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    next_target = [
        {
            "next_id": "NEXT1316_0_1317",
            "target_file": "1317-Y5-R10-RAB-P0-alpha-source-intake-template-and-priority-runner.md",
            "target_script": "scripts/Y5_R10_RAB_P0_alpha_source_intake_template_and_priority_runner.py",
            "task": "convert the 1316 exact product/source contract into fillable nonclaim source-intake templates and a runner that refuses rows until numeric/provenanced inputs or signed theorem-zero certificates exist",
            "success_condition": "every P0 required input has a template field, validation rule, provenance field, and refusal reason; no row can become claim-valid from thresholds or unity assumptions",
            "do_not": "do not invent coefficient values; do not transfer clock bounds into WEP/R10; do not claim local-GR/R10",
            "valid_for_claim": False,
            "claim_allowed": False,
        }
    ]

    validation = []
    sources_ok = all(compact_bool(row["exists"]) and compact_bool(row["needle_found"]) for row in source_register)
    validation.append(
        validation_row(
            "VAL1316_0_sources_exist",
            "registered source paths exist and anchors are found",
            sources_ok,
            f"{sum(compact_bool(row['exists']) and compact_bool(row['needle_found']) for row in source_register)}/{len(source_register)} source anchors found",
        )
    )
    validation.append(
        validation_row(
            "VAL1316_1_blockers_imported",
            "1315 blockers imported and P0 subset identified",
            len(blocker_import) == 15 and len(p0_blockers) == 12,
            f"blocker_rows={len(blocker_import)} p0_rows={len(p0_blockers)}",
        )
    )
    validation.append(
        validation_row(
            "VAL1316_2_derivation_attempts_cover_p0",
            "derivation attacks cover alpha, clock, WEP, R10, cross-arena, and parent primitive",
            {row["attack_id"] for row in derivation_attack}
            == {
                "DVA1316_0_alpha_F2",
                "DVA1316_1_clock_readout",
                "DVA1316_2_wep_source",
                "DVA1316_3_r10_product",
                "DVA1316_4_cross_arena",
                "DVA1316_5_parent_primitive",
            },
            ";".join(row["promotion_status"] for row in derivation_attack),
        )
    )
    validation.append(
        validation_row(
            "VAL1316_3_no_derivation_promoted",
            "no P0 derivation is promoted as a claim",
            all(row["promotion_status"] == "NOT_PROMOTED" for row in derivation_attack),
            "all derivation rows remain exact conditionals or source requirements",
        )
    )
    validation.append(
        validation_row(
            "VAL1316_4_product_formulas_written",
            "canonical product formulas exist for all scorepack rows",
            len(product_formula) == 5 and all("P_" in row["canonical_product"] or "same_branch_id" in row["canonical_product"] for row in product_formula),
            ";".join(row["formula_id"] for row in product_formula),
        )
    )
    validation.append(
        validation_row(
            "VAL1316_5_source_requirements_exact",
            "source requirements enumerate P0 missing inputs",
            len(source_requirement_rows) >= 17
            and all(str(row["current_status"]).startswith("MISSING") for row in source_requirement_rows),
            f"requirements={len(source_requirement_rows)}",
        )
    )
    validation.append(
        validation_row(
            "VAL1316_6_counterexamples_active",
            "counterexample locks remain active",
            all(row["1316_disposition"] == "ACTIVE" for row in counterexample_disposition),
            ";".join(row["counterexample_id"] for row in counterexample_disposition),
        )
    )
    validation.append(
        validation_row(
            "VAL1316_7_promotion_gates_block",
            "promotion gates block claims until proof/source inputs exist",
            all(row["current_status"] == "BLOCKED" for row in promotion_gates),
            ";".join(row["gate_id"] for row in promotion_gates),
        )
    )
    csv_tables = [
        ("source", source_register),
        ("blockers", blocker_import),
        ("derivation", derivation_attack),
        ("formula", product_formula),
        ("requirements", source_requirement_rows),
        ("counterexamples", counterexample_disposition),
        ("gates", promotion_gates),
        ("decisions", decisions),
        ("next", next_target),
    ]
    validation.append(
        validation_row(
            "VAL1316_8_nonclaim_policy",
            "all generated rows remain nonclaim",
            all_nonclaim([rows for _, rows in csv_tables]),
            "valid_for_claim=false and claim_allowed=false throughout generated tables",
        )
    )
    validation.append(
        validation_row(
            "VAL1316_9_formalization_untouched",
            "formalization-workbench untouched by generated outputs",
            not generated_inside_formalization(),
            f"formalization_generated_output_count={len(generated_inside_formalization())}",
        )
    )
    validation.append(
        validation_row(
            "VAL1316_10_next_target_1317",
            "next target routes to source-intake template and priority runner",
            next_target[0]["target_file"].startswith("1317-Y5-R10-RAB-P0-alpha-source-intake"),
            str(next_target[0]["target_file"]),
        )
    )
    validation.append(
        validation_row(
            "VAL1316_11_overall",
            "overall 1316 validation",
            all(row["status"] == "PASS" for row in validation),
            "1316 attacks P0 coupling derivations, promotes none, writes exact product/source contract, and routes to fillable source-intake runner",
        )
    )

    write_csv(SOURCE_REGISTER_PATH, source_register)
    write_csv(BLOCKER_IMPORT_PATH, blocker_import)
    write_csv(DERIVATION_ATTACK_PATH, derivation_attack)
    write_csv(PRODUCT_FORMULA_PATH, product_formula)
    write_csv(SOURCE_REQUIREMENT_PATH, source_requirement_rows)
    write_csv(COUNTEREXAMPLE_PATH, counterexample_disposition)
    write_csv(PROMOTION_GATES_PATH, promotion_gates)
    write_csv(DECISION_PATH, decisions)
    write_csv(NEXT_PATH, next_target)
    write_csv(VALIDATION_PATH, validation)

    doc = f"""# 1316: RAB P0 Alpha Coupling Input Source Or Derivation Attack

**Current verdict:** 1316 tries the derivation route first. It does not promote `b_alpha=0`, clock silence, WEP/source silence, R10 silence, or cross-arena transfer. Every route remains either an exact conditional theorem or a finite source-input requirement.

**Main progress:** the coupling bottleneck is now equation-shaped. The work no longer says merely "missing coupling"; it states the product forms and exact inputs that must be derived or sourced before any P0 alpha row can score.

**Decision:** build a fillable source-intake template/runner next. If a parent primitive appears, it can enter as a theorem-zero certificate; otherwise each product must be numeric, sourced, and provenance-checked.

## Source Register
{markdown_table(source_register, ["source_id", "local_path", "needle", "exists", "needle_found", "role", "valid_for_claim", "claim_allowed"])}

## P0 Blocker Import
{markdown_table(blocker_import, ["import_id", "source_blocker_id", "runner_row_id", "blocker_token", "blocker_source", "priority", "current_disposition", "valid_for_claim", "claim_allowed"])}

## Derivation Attack Ledger
{markdown_table(derivation_attack, ["attack_id", "target", "conditional_result", "obstruction", "output_formula_if_not_zero", "required_source_fill", "promotion_status", "valid_for_claim", "claim_allowed"])}

## Product Formula Requirements
{markdown_table(product_formula, ["formula_id", "runner_row_id", "canonical_product", "minimum_inputs", "current_available", "why_not_numeric", "promotion_rule", "score_ready", "valid_for_claim", "claim_allowed"])}

## P0 Source Requirement Ledger
{markdown_table(source_requirement_rows, ["requirement_id", "needed_object", "arena", "minimum_usable_form", "current_status", "resolution_type", "valid_for_claim", "claim_allowed"])}

## Counterexample Disposition
{markdown_table(counterexample_disposition, ["counterexample_id", "blocks", "1316_disposition", "reason", "required_to_close", "valid_for_claim", "claim_allowed"])}

## Promotion Gates
{markdown_table(promotion_gates, ["gate_id", "gate", "must_have", "current_status", "claim_rule", "valid_for_claim", "claim_allowed"])}

## Decision Ledger
{markdown_table(decisions, ["decision_id", "decision", "because", "next_action", "valid_for_claim", "claim_allowed"])}

## Next Target
{markdown_table(next_target, ["next_id", "target_file", "target_script", "task", "success_condition", "do_not", "valid_for_claim", "claim_allowed"])}

## Validation
{markdown_table(validation, ["check_id", "check", "status", "details"])}
"""
    DOC_PATH.write_text(doc, encoding="utf-8")


if __name__ == "__main__":
    main()

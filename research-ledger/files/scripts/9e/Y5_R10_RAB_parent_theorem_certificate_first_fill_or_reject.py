from __future__ import annotations

import csv
from pathlib import Path


PACK_ID = "P8_Y5_R10_1318"
TITLE = "1318-Y5-R10-RAB-parent-theorem-certificate-first-fill-or-reject"
ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = ROOT / "source-intake" / "mts_residuals"
DOC_PATH = ROOT / f"{TITLE}.md"
FORMALIZATION = ROOT.parent / "formalization-workbench"

SOURCE_REGISTER_PATH = OUT_DIR / f"{PACK_ID}_SOURCE_REGISTER.csv"
CERTIFICATE_IMPORT_PATH = OUT_DIR / f"{PACK_ID}_CERTIFICATE_IMPORT.csv"
CLAUSE_AUDIT_PATH = OUT_DIR / f"{PACK_ID}_CERTIFICATE_CLAUSE_AUDIT.csv"
CERTIFICATE_VERDICT_PATH = OUT_DIR / f"{PACK_ID}_CERTIFICATE_VERDICT.csv"
NUMERIC_FALLBACK_PATH = OUT_DIR / f"{PACK_ID}_NUMERIC_SOURCE_FALLBACK_ACTIVE.csv"
COUNTEREXAMPLE_CHECK_PATH = OUT_DIR / f"{PACK_ID}_COUNTEREXAMPLE_CHECK.csv"
ANTI_OVERCLAIM_PATH = OUT_DIR / f"{PACK_ID}_ANTI_OVERCLAIM_GATES.csv"
DECISION_PATH = OUT_DIR / f"{PACK_ID}_DECISION_LEDGER.csv"
NEXT_PATH = OUT_DIR / f"{PACK_ID}_NEXT_TARGET.csv"
VALIDATION_PATH = OUT_DIR / "P8_Y5_BRR545_1318_VALIDATION.csv"


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
        CERTIFICATE_IMPORT_PATH,
        CLAUSE_AUDIT_PATH,
        CERTIFICATE_VERDICT_PATH,
        NUMERIC_FALLBACK_PATH,
        COUNTEREXAMPLE_CHECK_PATH,
        ANTI_OVERCLAIM_PATH,
        DECISION_PATH,
        NEXT_PATH,
        VALIDATION_PATH,
        DOC_PATH,
    ]
    return [path for path in generated_paths if FORMALIZATION in path.parents]


def compact_bool(value: object) -> bool:
    return str(value).strip().lower() == "true"


def clause_evidence(certificate_id: str, clause: str) -> tuple[str, str, str, str]:
    exact_conditional = "CONDITIONAL_ONLY_NOT_PARENT_SIGNED"
    if certificate_id == "CERT1317_0_parent_object_language":
        return {
            "parent_action_clause": (
                "PTOL1220_0_parent_domain",
                "P8_Y5_R10_1220_PARENT_TYPED_SIGNATURE_ATTEMPT.csv",
                "SCHEMA_WRITTEN_NOT_DERIVED",
                "parent object language is a discipline contract, not derived from MTS primitives",
            ),
            "typed_visible_coefficient_domain": (
                "PTOL1220_1_visible_coefficient_domain",
                "P8_Y5_R10_1220_PARENT_TYPED_SIGNATURE_ATTEMPT.csv",
                "POWERFUL_RULE_NOT_DERIVED",
                "Hom(C_hid,Coeff(O_vis)) exclusion remains assumed/conditional",
            ),
            "no_hidden_argument_rule": (
                "TVC1219_1_typed_domain_theorem;PTOL1220_1_visible_coefficient_domain",
                "P8_Y5_R10_1219_TYPED_VISIBLE_COEFFICIENT_FUNCTOR_ATTEMPT.csv;P8_Y5_R10_1220_PARENT_TYPED_SIGNATURE_ATTEMPT.csv",
                exact_conditional,
                "typed rule is exact if grammar is signed, but current parent signature is not derived",
            ),
            "radiative_closure": (
                "PTOL1220_5_radiative_readout_closure",
                "P8_Y5_R10_1220_PARENT_TYPED_SIGNATURE_ATTEMPT.csv",
                "UNSIGNED",
                "S_eff, loops, spectroscopy, and readout preservation are not proven",
            ),
            "readout_closure": (
                "PTOL1220_5_radiative_readout_closure;HSC1313_3_clock_readout",
                "P8_Y5_R10_1220_PARENT_TYPED_SIGNATURE_ATTEMPT.csv;P8_Y5_R10_1316_COUNTEREXAMPLE_DISPOSITION.csv",
                "UNSIGNED_WITH_COUNTEREXAMPLE_ACTIVE",
                "clock/readout regeneration remains live",
            ),
            "source_path": (
                "SRC1318_2_1220_signature",
                "P8_Y5_R10_1220_PARENT_TYPED_SIGNATURE_ATTEMPT.csv",
                "SOURCE_PATH_EXISTS_NOT_CERTIFICATE",
                "source path exists but records failure, not a signed certificate",
            ),
        }[clause]
    if certificate_id == "CERT1317_1_alpha_F2_zero":
        return {
            "fixed_EM_current_normalization": (
                "BA1312_1_fixed_norm_level",
                "P8_Y5_R10_1312_B_ALPHA_NO_F2_PROOF_AUDIT.csv",
                "UNSIGNED",
                "fixed norm/level is not parent-signed",
            ),
            "no_lambda_F2": (
                "BA1312_2_no_lambda_F2",
                "P8_Y5_R10_1312_B_ALPHA_NO_F2_PROOF_AUDIT.csv",
                "COUNTERTERM_RETAINED",
                "lambda_A F_Q^2 remains legal unless parent excludes it",
            ),
            "no_f_Ihid_F2": (
                "BA1312_3_no_hidden_fF2;HSC1313_1_alpha",
                "P8_Y5_R10_1312_B_ALPHA_NO_F2_PROOF_AUDIT.csv;P8_Y5_R10_1316_COUNTEREXAMPLE_DISPOSITION.csv",
                "COUNTEREXAMPLE_ACTIVE",
                "f(I_hid)F_Q^2 remains legal without no-hidden primitive",
            ),
            "same_current_owner": (
                "BA1312_4_same_current_owner",
                "P8_Y5_R10_1312_B_ALPHA_NO_F2_PROOF_AUDIT.csv",
                "UNSIGNED",
                "same-current owner is not signed across readout/effective action",
            ),
            "radiative_readout_closure": (
                "BA1312_5_radiative_readout;PTOL1220_5_radiative_readout_closure",
                "P8_Y5_R10_1312_B_ALPHA_NO_F2_PROOF_AUDIT.csv;P8_Y5_R10_1220_PARENT_TYPED_SIGNATURE_ATTEMPT.csv",
                "UNSIGNED_CRITICAL",
                "radiative/readout re-entry blocks b_alpha=0 promotion",
            ),
            "source_path": (
                "SRC1318_7_1312_balpha",
                "P8_Y5_R10_1312_B_ALPHA_NO_F2_PROOF_AUDIT.csv",
                "SOURCE_PATH_EXISTS_NOT_CERTIFICATE",
                "source path exists but records b_alpha theorem-zero failure",
            ),
        }[clause]
    if certificate_id == "CERT1317_2_clock_readout":
        return {
            "clock_pair": (
                "CERT1317_2_clock_readout",
                "P8_Y5_R10_1317_THEOREM_ZERO_CERTIFICATE_TEMPLATE.csv",
                "MISSING_CLOCK_MODEL",
                "clock pair is a required template field, not filled",
            ),
            "transition_sensitivity": (
                "REQ1316_5_clock_model",
                "P8_Y5_R10_1316_P0_SOURCE_REQUIREMENT_LEDGER.csv",
                "MISSING_CLOCK_MODEL",
                "transition sensitivity/readout model is missing",
            ),
            "readout_functor": (
                "HSC1313_3_clock_readout;DVA1316_1_clock_readout",
                "P8_Y5_R10_1316_COUNTEREXAMPLE_DISPOSITION.csv;P8_Y5_R10_1316_P0_DERIVATION_ATTACK_LEDGER.csv",
                "UNSIGNED_WITH_COUNTEREXAMPLE_ACTIVE",
                "readout can regenerate alpha dependence",
            ),
            "tau_clock_time_or_direct_product": (
                "REQ1316_4_tau_clock",
                "P8_Y5_R10_1316_P0_SOURCE_REQUIREMENT_LEDGER.csv",
                "MISSING_CLOCK_READOUT_MAP",
                "tau_clock_time/direct product is missing",
            ),
            "units": (
                "TPL1317_4_tau_clock_time",
                "P8_Y5_R10_1317_P0_SOURCE_INTAKE_TEMPLATE.csv",
                "MISSING_UNITS_OR_DIMENSIONLESS_DECLARATION",
                "units field exists but is empty",
            ),
            "source_path": (
                "TPL1317_4_tau_clock_time",
                "P8_Y5_R10_1317_P0_SOURCE_INTAKE_TEMPLATE.csv",
                "MISSING_SOURCE_PATH",
                "source path field exists but is empty",
            ),
        }[clause]
    if certificate_id == "CERT1317_3_source_weight_zero":
        return {
            "source_weight_domain": (
                "PTOL1220_3_source_weight_exclusion;HSC1313_4_source_weight",
                "P8_Y5_R10_1220_PARENT_TYPED_SIGNATURE_ATTEMPT.csv;P8_Y5_R10_1316_COUNTEREXAMPLE_DISPOSITION.csv",
                "EXACT_CONDITIONAL_NOT_PARENT_SIGNED",
                "source weights are removable only if syntactically impossible, not merely absent",
            ),
            "species_weight_rule": (
                "PTOL1220_4_action_scale_measure_owner",
                "P8_Y5_R10_1220_PARENT_TYPED_SIGNATURE_ATTEMPT.csv",
                "NOT_PARENT_SIGNED",
                "species-dependent action multipliers remain live",
            ),
            "material_response": (
                "REQ1316_8_material",
                "P8_Y5_R10_1316_P0_SOURCE_REQUIREMENT_LEDGER.csv",
                "MISSING_MATERIAL_RESPONSE",
                "material map is not derived or sourced",
            ),
            "worldtube_profile": (
                "REQ1316_9_source_profile",
                "P8_Y5_R10_1316_P0_SOURCE_REQUIREMENT_LEDGER.csv",
                "MISSING_SOURCE_PROFILE",
                "finite source/worldtube profile is missing",
            ),
            "readout_kernel": (
                "REQ1316_8_material;REQ1316_9_source_profile",
                "P8_Y5_R10_1316_P0_SOURCE_REQUIREMENT_LEDGER.csv",
                "MISSING_READOUT_KERNEL",
                "WEP/R10 readout kernel is not signed",
            ),
            "source_path": (
                "TPL1317_6_beta_source_alpha",
                "P8_Y5_R10_1317_P0_SOURCE_INTAKE_TEMPLATE.csv",
                "MISSING_SOURCE_PATH",
                "source path field exists but is empty",
            ),
        }[clause]
    if certificate_id == "CERT1317_4_r10_product_vector":
        return {
            "lambda_X": ("REQ1316_10_lambda", "P8_Y5_R10_1316_P0_SOURCE_REQUIREMENT_LEDGER.csv", "MISSING_LAMBDA_X", "R10 range scale missing"),
            "Z_X": ("REQ1316_11_ZX", "P8_Y5_R10_1316_P0_SOURCE_REQUIREMENT_LEDGER.csv", "MISSING_Z_X", "R10 branch amplitude missing"),
            "K_X(lambda)": ("REQ1316_12_KX", "P8_Y5_R10_1316_P0_SOURCE_REQUIREMENT_LEDGER.csv", "MISSING_K_X", "R10 kernel/profile function missing"),
            "beta_source(lambda)": ("REQ1316_6_beta_source", "P8_Y5_R10_1316_P0_SOURCE_REQUIREMENT_LEDGER.csv", "MISSING_SOURCE_NORMALIZATION", "R10 source beta missing"),
            "beta_test(lambda)": ("REQ1316_13_beta_test", "P8_Y5_R10_1316_P0_SOURCE_REQUIREMENT_LEDGER.csv", "MISSING_BETA_TEST", "R10 test-body beta missing"),
            "tau_R10": ("CERT1317_4_r10_product_vector", "P8_Y5_R10_1317_THEOREM_ZERO_CERTIFICATE_TEMPLATE.csv", "MISSING_TAU_R10", "R10 branch/readout tau missing"),
            "epsilon_tail": ("REQ1316_14_tail", "P8_Y5_R10_1316_P0_SOURCE_REQUIREMENT_LEDGER.csv", "MISSING_EPSILON_TAIL", "finite-tail correction missing"),
            "promoted_alpha_bound_curve": ("REQ1316_15_bound", "P8_Y5_R10_1316_P0_SOURCE_REQUIREMENT_LEDGER.csv", "MISSING_PROMOTED_BOUND_CURVE", "R10 bound curve not promoted"),
            "source_path": ("RUN1317_3_run1314_3_r10", "P8_Y5_R10_1317_PRIORITY_RUNNER_REFUSAL_TABLE.csv", "MISSING_SOURCE_PATH", "R10 product row has no source-backed vector"),
        }[clause]
    if certificate_id == "CERT1317_5_cross_arena_functor":
        return {
            "same_parent_branch_id": ("REQ1316_16_branch", "P8_Y5_R10_1316_P0_SOURCE_REQUIREMENT_LEDGER.csv", "MISSING_CROSS_ARENA_PARENT_MAP", "shared parent branch id missing"),
            "readout_functor": ("DVA1316_4_cross_arena", "P8_Y5_R10_1316_P0_DERIVATION_ATTACK_LEDGER.csv", "UNSIGNED", "arena readout functor not signed"),
            "F_clock": ("CERT1317_2_clock_readout", "P8_Y5_R10_1317_THEOREM_ZERO_CERTIFICATE_TEMPLATE.csv", "MISSING_CLOCK_READOUT_CERTIFICATE", "clock arena map missing"),
            "F_WEP": ("CERT1317_3_source_weight_zero", "P8_Y5_R10_1317_THEOREM_ZERO_CERTIFICATE_TEMPLATE.csv", "MISSING_SOURCE_WEIGHT_CERTIFICATE", "WEP arena map missing"),
            "F_R10": ("CERT1317_4_r10_product_vector", "P8_Y5_R10_1317_THEOREM_ZERO_CERTIFICATE_TEMPLATE.csv", "MISSING_R10_VECTOR_OR_BOUND_CURVE", "R10 arena map missing"),
            "F_local": ("REQ1316_16_branch", "P8_Y5_R10_1316_P0_SOURCE_REQUIREMENT_LEDGER.csv", "MISSING_LOCAL_ARENA_MAP", "local arena map not supplied"),
            "nontransfer_exceptions": ("SHORT1317_5_no_cross_arena_transfer", "P8_Y5_R10_1317_ANTI_SHORTCUT_AUDIT.csv", "NONTRANSFER_RULE_ENFORCED_NOT_FUNCTOR", "anti-shortcut exists but not a transfer proof"),
            "source_path": ("TPL1317_16_parent_branch_classifier", "P8_Y5_R10_1317_P0_SOURCE_INTAKE_TEMPLATE.csv", "MISSING_SOURCE_PATH", "cross-arena source path field is empty"),
        }[clause]
    raise KeyError(f"Unhandled clause {certificate_id}:{clause}")


def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)

    source_register = [
        {
            "source_id": "SRC1318_0_1317_next",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1317_NEXT_TARGET.csv",
            "needle": "NEXT1317_0_1318",
            "role": "handoff into parent certificate fill/reject",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "source_id": "SRC1318_1_1317_certs",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1317_THEOREM_ZERO_CERTIFICATE_TEMPLATE.csv",
            "needle": "CERT1317_0_parent_object_language",
            "role": "certificate template to fill or reject",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "source_id": "SRC1318_2_1220_signature",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1220_PARENT_TYPED_SIGNATURE_ATTEMPT.csv",
            "needle": "PARENT_TYPED_OBJECT_LANGUAGE_SIGNATURE_NOT_DERIVED",
            "role": "strongest parent typed signature audit",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "source_id": "SRC1318_3_1219_functor",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1219_TYPED_VISIBLE_COEFFICIENT_FUNCTOR_ATTEMPT.csv",
            "needle": "TYPED_VISIBLE_COEFFICIENT_FUNCTOR_NOT_DERIVED",
            "role": "typed visible coefficient functor attempt",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "source_id": "SRC1318_4_1114_nohidden",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1114_NO_HIDDEN_VISIBLE_MORPHISM_THEOREM_ATTEMPT.csv",
            "needle": "NO_HIDDEN_VISIBLE_MORPHISM_NOT_DERIVED",
            "role": "no-hidden-visible morphism theorem attempt",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "source_id": "SRC1318_5_1115_invariant",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1115_LOCAL_INVARIANT_ALGEBRA_TRIVIALITY_ATTEMPT.csv",
            "needle": "LOCAL_INVARIANT_ALGEBRA_TRIVIALITY_NOT_DERIVED",
            "role": "invariant algebra triviality attempt",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "source_id": "SRC1318_6_1316_attack",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1316_P0_DERIVATION_ATTACK_LEDGER.csv",
            "needle": "DVA1316_5_parent_primitive",
            "role": "P0 derivation attack ledger",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "source_id": "SRC1318_7_1312_balpha",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1312_B_ALPHA_NO_F2_PROOF_AUDIT.csv",
            "needle": "B_ALPHA_THEOREM_ZERO_NOT_DERIVED",
            "role": "b_alpha no-F2 proof audit",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "source_id": "SRC1318_8_1316_counterexamples",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1316_COUNTEREXAMPLE_DISPOSITION.csv",
            "needle": "HSC1313_1_alpha",
            "role": "active counterexample disposition",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "source_id": "SRC1318_9_1317_runner",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1317_PRIORITY_RUNNER_REFUSAL_TABLE.csv",
            "needle": "RUN1317_3_run1314_3_r10",
            "role": "numeric source fallback runner state",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]
    for row in source_register:
        exists, needle_found = exists_and_contains(str(row["local_path"]), str(row["needle"]))
        row["exists"] = exists
        row["needle_found"] = needle_found

    certificates = read_csv(source_path("source-intake/mts_residuals/P8_Y5_R10_1317_THEOREM_ZERO_CERTIFICATE_TEMPLATE.csv"))
    runner_rows = read_csv(source_path("source-intake/mts_residuals/P8_Y5_R10_1317_PRIORITY_RUNNER_REFUSAL_TABLE.csv"))
    counterexamples = read_csv(source_path("source-intake/mts_residuals/P8_Y5_R10_1316_COUNTEREXAMPLE_DISPOSITION.csv"))

    certificate_import = []
    clause_audit = []
    certificate_verdict = []
    for certificate in certificates:
        certificate_id = certificate["certificate_id"]
        required_clauses = [clause.strip() for clause in certificate["required_clauses"].split(";") if clause.strip()]
        certificate_import.append(
            {
                "import_id": f"IMP1318_{len(certificate_import)}",
                "certificate_id": certificate_id,
                "route": certificate["route"],
                "required_clause_count": len(required_clauses),
                "current_certificate_status": certificate["current_certificate_status"],
                "fill_attempt_status": "AUDITED",
                "valid_for_claim": False,
                "claim_allowed": False,
            }
        )
        failed_clauses = []
        for index, clause in enumerate(required_clauses):
            evidence_id, evidence_path, clause_status, blocker = clause_evidence(certificate_id, clause)
            passes_certificate = clause_status == "SIGNED_AS_PARENT_CERTIFICATE"
            if not passes_certificate:
                failed_clauses.append(clause)
            clause_audit.append(
                {
                    "clause_id": f"CLAUSE1318_{certificate_id}_{index}",
                    "certificate_id": certificate_id,
                    "route": certificate["route"],
                    "required_clause": clause,
                    "evidence_id": evidence_id,
                    "evidence_path": evidence_path,
                    "clause_status": clause_status,
                    "passes_certificate": passes_certificate,
                    "blocker": blocker,
                    "valid_for_claim": False,
                    "claim_allowed": False,
                }
            )
        certificate_verdict.append(
            {
                "verdict_id": f"VERDICT1318_{len(certificate_verdict)}",
                "certificate_id": certificate_id,
                "route": certificate["route"],
                "required_clause_count": len(required_clauses),
                "signed_clause_count": len(required_clauses) - len(failed_clauses),
                "failed_clause_count": len(failed_clauses),
                "failed_clauses": ";".join(failed_clauses),
                "certificate_status": "REJECTED_FOR_NOW",
                "why": "at least one required clause is missing, conditional-only, unsigned, or counterexample-active",
                "effect": "theorem-zero route not promoted; finite source rows remain active",
                "valid_for_claim": False,
                "claim_allowed": False,
            }
        )

    numeric_fallback = []
    for row in runner_rows:
        numeric_fallback.append(
            {
                "fallback_id": f"FALL1318_{len(numeric_fallback)}",
                "source_runner_row_id": row["source_runner_row_id"],
                "canonical_product": row["canonical_product"],
                "missing_requirement_count": row["missing_requirement_count"],
                "missing_requirement_ids": row["missing_requirement_ids"],
                "fallback_status": "ACTIVE_NONCLAIM",
                "why_active": "parent certificate was not signed; product row still needs numeric/provenanced inputs or a later theorem-zero certificate",
                "valid_for_claim": False,
                "claim_allowed": False,
            }
        )

    counterexample_check = [
        {
            "check_id": f"CEX1318_{index}",
            "counterexample_id": row["counterexample_id"],
            "blocks": row["blocks"],
            "status_after_certificate_attempt": "ACTIVE",
            "reason": row["reason"],
            "required_to_close": row["required_to_close"],
            "valid_for_claim": False,
            "claim_allowed": False,
        }
        for index, row in enumerate(counterexamples)
    ]

    anti_overclaim = [
        {
            "gate_id": "AOC1318_0_no_conditional_to_certificate",
            "overclaim": "promote exact conditional theorem to signed parent certificate",
            "enforcement": "requires parent object-language/action-domain source path and all clauses signed",
            "status": "ENFORCED",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "gate_id": "AOC1318_1_no_absence_to_zero",
            "overclaim": "treat absence of a term in a chosen action as b_alpha=0 theorem",
            "enforcement": "lambda_A F_Q^2 and f(I_hid)F_Q^2 counterterms remain blockers",
            "status": "ENFORCED",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "gate_id": "AOC1318_2_no_readout_silence",
            "overclaim": "assume bare theorem-zero survives clocks, WEP, R10, or local readout",
            "enforcement": "radiative/readout closure must be signed separately",
            "status": "ENFORCED",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "gate_id": "AOC1318_3_no_numeric_shortcut",
            "overclaim": "fill source rows from thresholds, unity defaults, or review-candidate bounds",
            "enforcement": "numeric fallback rows remain active but nonclaim",
            "status": "ENFORCED",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    decisions = [
        {
            "decision_id": "DEC1318_0_certificate_rejected",
            "decision": "parent theorem-zero certificate rejected for now",
            "because": "the strongest corpus rows prove conditional routes but do not sign the parent object-language, no-hidden, source-weight, or readout clauses",
            "next_action": "try to construct the missing parent object-language signature rather than invent finite coefficients",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "decision_id": "DEC1318_1_numeric_rows_active",
            "decision": "numeric source fallback rows remain active and nonclaim",
            "because": "without a signed certificate, alpha/clock/WEP/R10/cross-arena products still need source-backed inputs",
            "next_action": "keep 1317 templates as the intake contract",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "decision_id": "DEC1318_2_best_next_route",
            "decision": "attack parent object-language construction next",
            "because": "derivability is the higher-value route; a signed parent grammar would close more debts than coefficient sourcing",
            "next_action": "1319 should attempt a minimal parent object-language signature construction or explicitly demote it to closure-only",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    next_target = [
        {
            "next_id": "NEXT1318_0_1319",
            "target_file": "1319-Y5-R10-RAB-minimal-parent-object-language-signature-construction-or-closure.md",
            "target_script": "scripts/Y5_R10_RAB_minimal_parent_object_language_signature_construction_or_closure.py",
            "task": "try to construct the missing parent object-language signature from the parent action/quotient/descent ingredients; if it cannot be derived, demote theorem-zero route to explicit closure-only and keep finite source rows active",
            "success_condition": "either a signed clause package is produced for parent action domain, visible coefficient domain, no-hidden argument rule, source-weight exclusion, and radiative/readout closure, or every missing clause is marked closure-only with exact consequences",
            "do_not": "do not use conditional grammar as signed proof; do not claim b_alpha=0, WEP/R10, or local-GR; do not fill numeric rows by assumption",
            "valid_for_claim": False,
            "claim_allowed": False,
        }
    ]

    validation = []
    sources_ok = all(compact_bool(row["exists"]) and compact_bool(row["needle_found"]) for row in source_register)
    validation.append(
        validation_row(
            "VAL1318_0_sources_exist",
            "registered source paths exist and anchors are found",
            sources_ok,
            f"{sum(compact_bool(row['exists']) and compact_bool(row['needle_found']) for row in source_register)}/{len(source_register)} source anchors found",
        )
    )
    expected_clause_count = sum(len(row["required_clauses"].split(";")) for row in certificates)
    validation.append(
        validation_row(
            "VAL1318_1_certificates_imported",
            "all 1317 certificates imported",
            len(certificate_import) == 6 and expected_clause_count == 41,
            f"certificates={len(certificate_import)} expected_clauses={expected_clause_count}",
        )
    )
    validation.append(
        validation_row(
            "VAL1318_2_clause_audit_complete",
            "every required certificate clause is audited",
            len(clause_audit) == expected_clause_count
            and all(row["passes_certificate"] is False for row in clause_audit),
            f"audited_clauses={len(clause_audit)} signed={sum(row['passes_certificate'] is True for row in clause_audit)}",
        )
    )
    validation.append(
        validation_row(
            "VAL1318_3_all_certificates_rejected",
            "no theorem-zero certificate is promoted",
            all(row["certificate_status"] == "REJECTED_FOR_NOW" for row in certificate_verdict),
            ";".join(f"{row['certificate_id']}:{row['failed_clause_count']}" for row in certificate_verdict),
        )
    )
    validation.append(
        validation_row(
            "VAL1318_4_numeric_fallback_active",
            "numeric source fallback remains active and nonclaim",
            len(numeric_fallback) == 5 and all(row["fallback_status"] == "ACTIVE_NONCLAIM" for row in numeric_fallback),
            ";".join(row["source_runner_row_id"] for row in numeric_fallback),
        )
    )
    validation.append(
        validation_row(
            "VAL1318_5_counterexamples_active",
            "counterexamples remain active after certificate attempt",
            len(counterexample_check) == 4
            and all(row["status_after_certificate_attempt"] == "ACTIVE" for row in counterexample_check),
            ";".join(row["counterexample_id"] for row in counterexample_check),
        )
    )
    validation.append(
        validation_row(
            "VAL1318_6_anti_overclaim_enforced",
            "anti-overclaim gates are enforced",
            all(row["status"] == "ENFORCED" for row in anti_overclaim),
            ";".join(row["gate_id"] for row in anti_overclaim),
        )
    )
    csv_tables = [
        ("source", source_register),
        ("cert_import", certificate_import),
        ("clause", clause_audit),
        ("verdict", certificate_verdict),
        ("fallback", numeric_fallback),
        ("counterexamples", counterexample_check),
        ("anti", anti_overclaim),
        ("decisions", decisions),
        ("next", next_target),
    ]
    validation.append(
        validation_row(
            "VAL1318_7_nonclaim_policy",
            "all generated rows remain nonclaim",
            all_nonclaim([rows for _, rows in csv_tables]),
            "valid_for_claim=false and claim_allowed=false throughout generated tables",
        )
    )
    validation.append(
        validation_row(
            "VAL1318_8_formalization_untouched",
            "formalization-workbench untouched by generated outputs",
            not generated_inside_formalization(),
            f"formalization_generated_output_count={len(generated_inside_formalization())}",
        )
    )
    validation.append(
        validation_row(
            "VAL1318_9_next_target_1319",
            "next target routes to minimal parent object-language construction",
            next_target[0]["target_file"].startswith("1319-Y5-R10-RAB-minimal-parent-object-language"),
            str(next_target[0]["target_file"]),
        )
    )
    validation.append(
        validation_row(
            "VAL1318_10_overall",
            "overall 1318 validation",
            all(row["status"] == "PASS" for row in validation),
            "1318 rejects current parent theorem-zero certificates clause-by-clause and routes to parent object-language construction attempt",
        )
    )

    write_csv(SOURCE_REGISTER_PATH, source_register)
    write_csv(CERTIFICATE_IMPORT_PATH, certificate_import)
    write_csv(CLAUSE_AUDIT_PATH, clause_audit)
    write_csv(CERTIFICATE_VERDICT_PATH, certificate_verdict)
    write_csv(NUMERIC_FALLBACK_PATH, numeric_fallback)
    write_csv(COUNTEREXAMPLE_CHECK_PATH, counterexample_check)
    write_csv(ANTI_OVERCLAIM_PATH, anti_overclaim)
    write_csv(DECISION_PATH, decisions)
    write_csv(NEXT_PATH, next_target)
    write_csv(VALIDATION_PATH, validation)

    doc = f"""# 1318: RAB Parent Theorem Certificate First Fill Or Reject

**Current verdict:** 1318 tries to fill the 1317 parent theorem-zero certificates from the strongest existing corpus rows and rejects every certificate for now. The useful theorem pieces are exact conditionals, but the parent object-language/signature package is still not signed.

**Main progress:** the rejection is now clause-by-clause rather than vague. We know exactly which parent clauses fail: action-domain derivation, visible coefficient-domain ownership, no-hidden argument rule, source-weight exclusion, R10 product vector, and radiative/readout closure.

**Decision:** do not source-hunt first. The best next route is to attempt a minimal parent object-language signature construction; if that fails, the theorem-zero path becomes explicit closure-only and the 1317 finite source rows remain the honest intake path.

## Source Register
{markdown_table(source_register, ["source_id", "local_path", "needle", "exists", "needle_found", "role", "valid_for_claim", "claim_allowed"])}

## Certificate Import
{markdown_table(certificate_import, ["import_id", "certificate_id", "route", "required_clause_count", "current_certificate_status", "fill_attempt_status", "valid_for_claim", "claim_allowed"])}

## Certificate Clause Audit
{markdown_table(clause_audit, ["clause_id", "certificate_id", "route", "required_clause", "evidence_id", "evidence_path", "clause_status", "passes_certificate", "blocker", "valid_for_claim", "claim_allowed"])}

## Certificate Verdict
{markdown_table(certificate_verdict, ["verdict_id", "certificate_id", "route", "required_clause_count", "signed_clause_count", "failed_clause_count", "failed_clauses", "certificate_status", "why", "effect", "valid_for_claim", "claim_allowed"])}

## Numeric Source Fallback Active
{markdown_table(numeric_fallback, ["fallback_id", "source_runner_row_id", "canonical_product", "missing_requirement_count", "missing_requirement_ids", "fallback_status", "why_active", "valid_for_claim", "claim_allowed"])}

## Counterexample Check
{markdown_table(counterexample_check, ["check_id", "counterexample_id", "blocks", "status_after_certificate_attempt", "reason", "required_to_close", "valid_for_claim", "claim_allowed"])}

## Anti-Overclaim Gates
{markdown_table(anti_overclaim, ["gate_id", "overclaim", "enforcement", "status", "valid_for_claim", "claim_allowed"])}

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

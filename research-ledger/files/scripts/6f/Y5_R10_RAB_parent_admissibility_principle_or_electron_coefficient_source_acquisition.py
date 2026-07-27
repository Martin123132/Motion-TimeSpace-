from __future__ import annotations

import csv
import math
from pathlib import Path


PACK_ID = "P8_Y5_R10_1334"
TITLE = "1334-Y5-R10-RAB-parent-admissibility-principle-or-electron-coefficient-source-acquisition"
ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = ROOT / "source-intake" / "mts_residuals"
DOC_PATH = ROOT / f"{TITLE}.md"
FORMALIZATION = ROOT.parent / "formalization-workbench"

SOURCE_REGISTER_PATH = OUT_DIR / f"{PACK_ID}_SOURCE_REGISTER.csv"
ADMISSIBILITY_PATH = OUT_DIR / f"{PACK_ID}_PARENT_ADMISSIBILITY_PRINCIPLE_AUDIT.csv"
EPSILON_SOURCE_PATH = OUT_DIR / f"{PACK_ID}_ELECTRON_COEFFICIENT_SOURCE_ACQUISITION.csv"
SAME_BRANCH_PATH = OUT_DIR / f"{PACK_ID}_SAME_BRANCH_WEP_PRODUCT_REQUIREMENTS.csv"
RUNNER_PATH = OUT_DIR / f"{PACK_ID}_RUNNER_UPDATE.csv"
ANTI_SHORTCUT_PATH = OUT_DIR / f"{PACK_ID}_ANTI_SHORTCUT_GATES.csv"
DECISION_PATH = OUT_DIR / f"{PACK_ID}_DECISION_LEDGER.csv"
NEXT_PATH = OUT_DIR / f"{PACK_ID}_NEXT_TARGET.csv"
VALIDATION_PATH = OUT_DIR / "P8_Y5_BRR545_1334_VALIDATION.csv"


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
    return str(value).strip().lower() == "false"


def all_nonclaim(tables: list[list[dict[str, object]]]) -> bool:
    for table in tables:
        for row in table:
            if "valid_for_claim" in row and not is_false(row.get("valid_for_claim", False)):
                return False
            if "claim_allowed" in row and not is_false(row.get("claim_allowed", False)):
                return False
    return True


def finite_positive(value: object) -> bool:
    try:
        number = float(value)
    except (TypeError, ValueError):
        return False
    return math.isfinite(number) and number > 0.0


def generated_inside_formalization() -> list[Path]:
    if not FORMALIZATION.exists():
        return []
    return [path for path in FORMALIZATION.rglob("*1334*") if path.is_file()]


def fmt(value: float) -> str:
    return f"{value:.12e}"


def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)

    source_specs = [
        {
            "source_id": "SRC1334_0_1333_next",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1333_NEXT_TARGET.csv",
            "needle": "NEXT1333_0_1334",
            "role": "selected 1334 target",
        },
        {
            "source_id": "SRC1334_1_1333_derivation",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1333_NO_SOURCE_PREFACTOR_DERIVATION_ATTEMPT.csv",
            "needle": "NSP1333_5_verdict",
            "role": "no-prefactor derivation verdict",
        },
        {
            "source_id": "SRC1334_2_1333_bound",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1333_ELECTRON_RESIDUAL_BOUND_CONTRACT.csv",
            "needle": "EB1333_0_unit_kernel_electron_prefactor",
            "role": "electron coefficient proxy bound",
        },
        {
            "source_id": "SRC1334_3_1214_no_slot",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1214_NO_SOURCE_ONLY_SLOT_SIGNATURE_AUDIT.csv",
            "needle": "NSS1214_5_verdict",
            "role": "no source-only slot signature audit",
        },
        {
            "source_id": "SRC1334_4_1319_minimal_signature",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1319_MINIMAL_SIGNATURE_CANDIDATE.csv",
            "needle": "SIG1319_4_source_weight_exclusion",
            "role": "minimal parent signature candidate",
        },
        {
            "source_id": "SRC1334_5_1088_minimal_signature",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1088_MINIMAL_SIGNATURE_CLAUSE.csv",
            "needle": "MOMS1088_4_no_species_weights",
            "role": "minimal ordinary matter signature",
        },
        {
            "source_id": "SRC1334_6_1104_signature",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1104_PARENT_SIGNATURE_LEDGER.csv",
            "needle": "SIG1104_4_source_weight_exclusion",
            "role": "ordinary-sector parent signature ledger",
        },
        {
            "source_id": "SRC1334_7_1236_meta",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1236_NO_HIDDEN_VISIBLE_COEFFICIENT_META_THEOREM.csv",
            "needle": "META1236_2_local_GR_consequence",
            "role": "typed coefficient meta-theorem",
        },
        {
            "source_id": "SRC1334_8_1219_no_hidden",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1219_NO_HIDDEN_ARGUMENT_CONDITIONAL_THEOREM.csv",
            "needle": "NHA1219_0_type_rule",
            "role": "typed domain no-hidden argument theorem",
        },
        {
            "source_id": "SRC1334_9_1046_forbidden",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1046_FORBIDDEN_VERTEX_CATALOG.csv",
            "needle": "FV1046_6_source_only_weight",
            "role": "source-only forbidden vertex catalog",
        },
        {
            "source_id": "SRC1334_10_1098_forbidden",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1098_FORBIDDEN_VERTEX_AUDIT.csv",
            "needle": "FV1098_6_source_weight_X",
            "role": "forbidden source-weight vertex audit",
        },
        {
            "source_id": "SRC1334_11_1225_tau",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1225_TAU_WEP_SOURCE_ACQUISITION_TABLE.csv",
            "needle": "ACQ1225_1_product_convention",
            "role": "WEP product/readout blocker",
        },
        {
            "source_id": "SRC1334_12_1333_validation",
            "local_path": "source-intake/mts_residuals/P8_Y5_BRR545_1333_VALIDATION.csv",
            "needle": "VAL1333_10_overall",
            "role": "1333 pass gate",
        },
    ]
    source_register: list[dict[str, object]] = []
    for spec in source_specs:
        exists, needle_found = exists_and_contains(spec["local_path"], spec["needle"])
        source_register.append(
            {
                **spec,
                "exists": exists,
                "needle_found": needle_found,
                "valid_for_claim": False,
                "claim_allowed": False,
            }
        )

    bound_row = read_csv(source_path("source-intake/mts_residuals/P8_Y5_R10_1333_ELECTRON_RESIDUAL_BOUND_CONTRACT.csv"))[0]
    epsilon_bound = float(bound_row["required_abs_coefficient_max"])

    admissibility = [
        {
            "audit_id": "ADM1334_0_target",
            "principle": "active-source-only prefactors w_A are not admissible parent objects",
            "candidate_rule": "Coeff(source-visible operators) has typed domain Q_obs x Rep_vis x Top_vis; no species-only active-source scalar argument exists",
            "result": "TARGET_SHARPENED",
            "missing_for_claim": "derive the object language and coefficient domain from MTS primitives",
            "parent_signed": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "audit_id": "ADM1334_1_typed_domain_route",
            "principle": "typed coefficient domain excludes hidden/source-only arguments",
            "candidate_rule": "Hom(SourceOnlySpeciesLabel, Coeff(T_A)) is absent; w_A S_A is ill-typed",
            "result": "EXACT_CONDITIONAL_META_THEOREM",
            "missing_for_claim": "META1236/NHA1219 premises are not parent-derived",
            "parent_signed": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "audit_id": "ADM1334_2_minimal_signature_route",
            "principle": "minimal ordinary matter signature has no w_A slot",
            "candidate_rule": "MOMS1088/SIG1319 excludes source-only species weights in the matter language",
            "result": "CLOSURE_SCHEMA_ONLY",
            "missing_for_claim": "single parent action source does not derive MOMS/SIG1319",
            "parent_signed": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "audit_id": "ADM1334_3_action_measure_owner",
            "principle": "one action-scale/measure/hbar owner makes relative w_A non-admissible",
            "candidate_rule": "species-dependent action scales are forbidden unless they are measured nongravitational constants theta_A",
            "result": "NOT_PARENT_SIGNED",
            "missing_for_claim": "action measure owner and radiative/readout stability remain unsigned",
            "parent_signed": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "audit_id": "ADM1334_4_forbidden_vertex_route",
            "principle": "w_A is a forbidden visible source-weight vertex",
            "candidate_rule": "FV1046_6/FV1098_6 list source-only weights as forbidden-required-but-currently-legal",
            "result": "FORBIDDEN_REQUIRED_NOT_FORBIDDEN_DERIVED",
            "missing_for_claim": "forbidden-vertex catalog is a gate, not a parent proof",
            "parent_signed": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "audit_id": "ADM1334_5_verdict",
            "principle": "primitive parent admissibility principle excludes w_A",
            "candidate_rule": "combine typed domain, minimal signature, action-measure owner, and forbidden-vertex catalog",
            "result": "NOT_DERIVED_CURRENT_CORPUS",
            "missing_for_claim": "all routes are exact conditionals or closure schemas; none is a derived parent theorem",
            "parent_signed": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    epsilon_source = [
        {
            "source_id": "EPS1334_0_existing_proxy_bound",
            "coefficient": "epsilon_e_or_delta_w_e",
            "value_or_bound": fmt(epsilon_bound),
            "units": "dimensionless",
            "source_basis": "EB1333_0_unit_kernel_electron_prefactor",
            "status": "SOURCE_BACKED_PROXY_BOUND_NONCLAIM",
            "same_branch_status": "UNIT_KERNEL_ONLY",
            "missing_for_claim": "tau_WEP product convention; source worldtube; readout kernel; parent coefficient units/sign",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "source_id": "EPS1334_1_parent_coefficient_source",
            "coefficient": "epsilon_e_or_delta_w_e",
            "value_or_bound": "MISSING_PARENT_COEFFICIENT",
            "units": "MISSING_UNITS",
            "source_basis": "no parent action term yet",
            "status": "MISSING_SOURCE_ROW",
            "same_branch_status": "MISSING",
            "missing_for_claim": "action term or theorem-zero certificate for electron source-only prefactor",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "source_id": "EPS1334_2_no_prefactor_zero_certificate",
            "coefficient": "epsilon_e_or_delta_w_e",
            "value_or_bound": "ZERO_ONLY_IF_ADM1334_PREMISES_SIGNED",
            "units": "dimensionless",
            "source_basis": "ADM1334_1 plus ADM1334_2 plus ADM1334_3",
            "status": "ZERO_CERTIFICATE_NOT_SIGNED",
            "same_branch_status": "CONDITIONAL_ONLY",
            "missing_for_claim": "parent admissibility theorem excluding w_A",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    same_branch = [
        {
            "requirement_id": "SBR1334_0_tau_WEP",
            "needed_object": "tau_WEP/readout product convention",
            "current_status": "NORMALIZATION_NOT_FILLED",
            "source": "ACQ1225_1_product_convention",
            "effect": "unit-kernel proxy cannot become claim-grade bound",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "requirement_id": "SBR1334_1_source_worldtube",
            "needed_object": "Earth/source stress worldtube in observed frame",
            "current_status": "MISSING_SOURCE_PROFILE_WEIGHTING",
            "source": "ACQ1225_2_source_worldtube",
            "effect": "source leg cannot be multiplied into WEP prediction",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "requirement_id": "SBR1334_2_orbit_average",
            "needed_object": "MICROSCOPE orbit/session average and masks",
            "current_status": "MISSING_ORBIT_AVERAGE_ARRAYS",
            "source": "ACQ1225_3_orbit_average",
            "effect": "reported eta channel not reproduced",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "requirement_id": "SBR1334_3_parent_branch",
            "needed_object": "same parent branch id for epsilon_e, material response, source, and readout",
            "current_status": "MISSING_BRANCH_CLASSIFIER",
            "source": "P8_Y5_R10_1317_P0_SOURCE_INTAKE_TEMPLATE.csv:TPL1317_16",
            "effect": "cannot mix electron bound with unrelated source/readout assumptions",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    runner = [
        {
            "runner_id": "RUN1334_0_admissibility_principle",
            "target": "derive primitive parent admissibility principle excluding w_A",
            "input_status": "CONDITIONAL_META_THEOREM_NOT_PARENT_SIGNED",
            "runner_status": "REFUSED_ZERO_PROMOTION",
            "reason": "typed-domain and minimal-signature routes are powerful but not derived from MTS primitives",
            "score_ready": False,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "runner_id": "RUN1334_1_epsilon_e_bound",
            "target": "finite electron coefficient epsilon_e",
            "input_status": "PROXY_BOUND_AVAILABLE_PARENT_SOURCE_MISSING",
            "runner_status": "BOUND_CONTRACT_STAGED_NOT_SCOREABLE",
            "reason": "epsilon_e <= proxy bound is useful pressure, but same-branch WEP/readout normalization is absent",
            "score_ready": False,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    anti_shortcut = [
        {
            "gate_id": "SHORT1334_0_no_typed_rule_as_parent_proof",
            "shortcut": "treat typed-language conditionals as derived parent action",
            "enforcement": "REFUSED",
            "status": "ENFORCED",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "gate_id": "SHORT1334_1_no_forbidden_catalog_as_proof",
            "shortcut": "treat forbidden-vertex catalog as proof the vertex is absent",
            "enforcement": "REFUSED",
            "status": "ENFORCED",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "gate_id": "SHORT1334_2_no_proxy_bound_as_score",
            "shortcut": "score WEP from unit-kernel epsilon_e bound",
            "enforcement": "REFUSED",
            "status": "ENFORCED",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "gate_id": "SHORT1334_3_no_local_GR_claim",
            "shortcut": "claim local GR/Newton reduction from source-prefactor work",
            "enforcement": "REFUSED",
            "status": "ENFORCED",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    decision = [
        {
            "decision_id": "DEC1334_0_admissibility_result",
            "decision": "primitive admissibility principle is not derived yet",
            "because": "the best rules are conditional grammar/signature gates, not parent-action consequences",
            "effect": "no-source-prefactor zero remains closure-only; finite epsilon_e branch remains live",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "decision_id": "DEC1334_1_next_empirical_step",
            "decision": "make the epsilon_e bound same-branch before any scoring",
            "because": "the unit-kernel bound is numerically sharp but not tied to tau_WEP/source/readout product convention",
            "effect": "next target should fill WEP product normalization/readout inputs or keep coefficient source missing",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    next_target = [
        {
            "next_id": "NEXT1334_0_1335",
            "target_file": "1335-Y5-R10-RAB-WEP-product-normalization-for-electron-residual-or-readout-waitstate.md",
            "target_script": "scripts/Y5_R10_RAB_WEP_product_normalization_for_electron_residual_or_readout_waitstate.py",
            "task": "try to put the epsilon_e electron residual bound into the same WEP/readout/source-worldtube convention; if unavailable, create a precise readout/source waitstate",
            "success_condition": "epsilon_e bound gets a same-branch tau/source/readout normalization contract, or the missing official MICROSCOPE/readout/source inputs are listed as blockers",
            "do_not": "do not score WEP from unit kernel, do not claim local GR, do not mix branches, and do not tune Ti/Pt",
            "valid_for_claim": False,
            "claim_allowed": False,
        }
    ]

    tables_for_nonclaim = [
        source_register,
        admissibility,
        epsilon_source,
        same_branch,
        runner,
        anti_shortcut,
        decision,
        next_target,
    ]

    source_anchor_count = sum(1 for row in source_register if row["exists"] and row["needle_found"])
    admissibility_not_derived = any(row["audit_id"] == "ADM1334_5_verdict" and row["result"] == "NOT_DERIVED_CURRENT_CORPUS" for row in admissibility)
    proxy_bound_finite = finite_positive(epsilon_source[0]["value_or_bound"])
    zero_not_signed = any(row["source_id"] == "EPS1334_2_no_prefactor_zero_certificate" and row["status"] == "ZERO_CERTIFICATE_NOT_SIGNED" for row in epsilon_source)
    same_branch_blocked = all(row["current_status"].startswith(("NORMALIZATION", "MISSING")) for row in same_branch)
    runner_refuses = all(row["score_ready"] is False and row["valid_prediction_row"] is False for row in runner)
    shortcuts_enforced = all(row["status"] == "ENFORCED" for row in anti_shortcut)
    nonclaim = all_nonclaim(tables_for_nonclaim)
    formal_clean = len(generated_inside_formalization()) == 0
    next_is_1335 = next_target[0]["target_file"].startswith("1335-")

    validations = [
        validation_row(
            "VAL1334_0_sources_exist",
            "registered source paths exist and anchors are found",
            source_anchor_count == len(source_register),
            f"{source_anchor_count}/{len(source_register)} source anchors found",
        ),
        validation_row(
            "VAL1334_1_admissibility_not_derived",
            "primitive admissibility principle is not promoted",
            admissibility_not_derived,
            "ADM1334_5_verdict=NOT_DERIVED_CURRENT_CORPUS",
        ),
        validation_row(
            "VAL1334_2_proxy_bound_finite",
            "epsilon_e proxy bound is finite positive",
            proxy_bound_finite,
            f"epsilon_e_proxy_bound={fmt(epsilon_bound)}",
        ),
        validation_row(
            "VAL1334_3_zero_not_signed",
            "epsilon_e zero certificate remains unsigned",
            zero_not_signed,
            "EPS1334_2_no_prefactor_zero_certificate=ZERO_CERTIFICATE_NOT_SIGNED",
        ),
        validation_row(
            "VAL1334_4_same_branch_blocked",
            "same-branch WEP product requirements remain blocked",
            same_branch_blocked,
            ";".join(f"{row['requirement_id']}={row['current_status']}" for row in same_branch),
        ),
        validation_row(
            "VAL1334_5_runners_refuse_claims",
            "runners refuse zero/WEP/local-GR promotion",
            runner_refuses,
            ";".join(f"{row['runner_id']}={row['runner_status']}" for row in runner),
        ),
        validation_row(
            "VAL1334_6_shortcuts_enforced",
            "anti-shortcut gates are enforced",
            shortcuts_enforced,
            ";".join(row["gate_id"] for row in anti_shortcut),
        ),
        validation_row(
            "VAL1334_7_nonclaim_policy",
            "all generated rows remain nonclaim",
            nonclaim,
            "valid_for_claim=false and claim_allowed=false where present",
        ),
        validation_row(
            "VAL1334_8_formalization_untouched",
            "formalization-workbench untouched by generated outputs",
            formal_clean,
            f"formalization_generated_output_count={len(generated_inside_formalization())}",
        ),
        validation_row(
            "VAL1334_9_next_target_1335",
            "next target routes to WEP product normalization/readout waitstate",
            next_is_1335,
            str(next_target[0]["target_file"]),
        ),
    ]
    validations.append(
        validation_row(
            "VAL1334_10_overall",
            "overall 1334 validation",
            all(row["status"] == "PASS" for row in validations),
            "1334 keeps admissibility conditional and carries epsilon_e into a same-branch WEP normalization target",
        )
    )

    write_csv(SOURCE_REGISTER_PATH, source_register)
    write_csv(ADMISSIBILITY_PATH, admissibility)
    write_csv(EPSILON_SOURCE_PATH, epsilon_source)
    write_csv(SAME_BRANCH_PATH, same_branch)
    write_csv(RUNNER_PATH, runner)
    write_csv(ANTI_SHORTCUT_PATH, anti_shortcut)
    write_csv(DECISION_PATH, decision)
    write_csv(NEXT_PATH, next_target)
    write_csv(VALIDATION_PATH, validations)

    doc = f"""# {TITLE}

**Current verdict:** 1334 does not derive a primitive parent admissibility principle. The typed-language/no-hidden/source-weight exclusion route is powerful, but still conditional on adopting a parent grammar that has not been derived from MTS primitives.

**Main progress:** the finite electron branch is now a source-acquisition object: `epsilon_e` has a nonclaim proxy upper scale `{fmt(epsilon_bound)}`, a missing zero certificate, and explicit same-branch WEP/readout blockers.

**Decision:** no `epsilon_e=0`, WEP, or local-GR claim. Next work should try to normalize the electron residual bound into the same MICROSCOPE/source-worldtube/readout convention, or mark the branch as readout-waitstate.

## Source Register
{markdown_table(source_register, ["source_id", "local_path", "needle", "exists", "needle_found", "role", "valid_for_claim", "claim_allowed"])}

## Parent Admissibility Principle Audit
{markdown_table(admissibility, ["audit_id", "principle", "candidate_rule", "result", "missing_for_claim", "parent_signed", "valid_for_claim", "claim_allowed"])}

## Electron Coefficient Source Acquisition
{markdown_table(epsilon_source, ["source_id", "coefficient", "value_or_bound", "units", "source_basis", "status", "same_branch_status", "missing_for_claim", "valid_for_claim", "claim_allowed"])}

## Same-Branch WEP Product Requirements
{markdown_table(same_branch, ["requirement_id", "needed_object", "current_status", "source", "effect", "valid_for_claim", "claim_allowed"])}

## Runner Update
{markdown_table(runner, ["runner_id", "target", "input_status", "runner_status", "reason", "score_ready", "valid_prediction_row", "valid_for_claim", "claim_allowed"])}

## Anti-Shortcut Gates
{markdown_table(anti_shortcut, ["gate_id", "shortcut", "enforcement", "status", "valid_for_claim", "claim_allowed"])}

## Decision Ledger
{markdown_table(decision, ["decision_id", "decision", "because", "effect", "valid_for_claim", "claim_allowed"])}

## Next Target
{markdown_table(next_target, ["next_id", "target_file", "target_script", "task", "success_condition", "do_not", "valid_for_claim", "claim_allowed"])}

## Validation
{markdown_table(validations, ["check_id", "check", "status", "details"])}
"""
    DOC_PATH.write_text(doc, encoding="utf-8")

    print(f"Wrote {DOC_PATH}")
    print(f"Wrote validation {VALIDATION_PATH}")


if __name__ == "__main__":
    main()

from __future__ import annotations

import csv
import math
from pathlib import Path


PACK_ID = "P8_Y5_R10_1333"
TITLE = "1333-Y5-R10-RAB-no-source-prefactor-parent-schema-or-electron-residual-bound"
ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = ROOT / "source-intake" / "mts_residuals"
DOC_PATH = ROOT / f"{TITLE}.md"
FORMALIZATION = ROOT.parent / "formalization-workbench"

SOURCE_REGISTER_PATH = OUT_DIR / f"{PACK_ID}_SOURCE_REGISTER.csv"
DERIVATION_PATH = OUT_DIR / f"{PACK_ID}_NO_SOURCE_PREFACTOR_DERIVATION_ATTEMPT.csv"
COUNTERMODEL_PATH = OUT_DIR / f"{PACK_ID}_SOURCE_PREFACTOR_COUNTERMODEL_LEDGER.csv"
SCHEMA_OPTIONS_PATH = OUT_DIR / f"{PACK_ID}_PARENT_SCHEMA_OPTIONS.csv"
ELECTRON_BOUND_PATH = OUT_DIR / f"{PACK_ID}_ELECTRON_RESIDUAL_BOUND_CONTRACT.csv"
RUNNER_PATH = OUT_DIR / f"{PACK_ID}_WEP_RUNNER_UPDATE.csv"
ANTI_SHORTCUT_PATH = OUT_DIR / f"{PACK_ID}_ANTI_SHORTCUT_GATES.csv"
DECISION_PATH = OUT_DIR / f"{PACK_ID}_DECISION_LEDGER.csv"
NEXT_PATH = OUT_DIR / f"{PACK_ID}_NEXT_TARGET.csv"
VALIDATION_PATH = OUT_DIR / "P8_Y5_BRR545_1333_VALIDATION.csv"


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
    return [path for path in FORMALIZATION.rglob("*1333*") if path.is_file()]


def fmt(value: float) -> str:
    return f"{value:.12e}"


def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)

    source_specs = [
        {
            "source_id": "SRC1333_0_1332_next",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1332_NEXT_TARGET.csv",
            "needle": "NEXT1332_0_1333",
            "role": "selected 1333 target",
        },
        {
            "source_id": "SRC1333_1_1332_common_mode",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1332_COMMON_MODE_SOURCE_THEOREM.csv",
            "needle": "CMT1332_0_common_mode_source_coupling",
            "role": "common-mode theorem target",
        },
        {
            "source_id": "SRC1333_2_1332_premises",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1332_COMMON_MODE_PREMISE_AUDIT.csv",
            "needle": "PREM1332_3_no_relative_source_prefactors",
            "role": "no-prefactor premise blocker",
        },
        {
            "source_id": "SRC1333_3_1330_delta",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1330_AUDITED_ELECTRON_DELTA_VECTOR.csv",
            "needle": "DELTA1330_0_TA6V_minus_PtRh10_electron",
            "role": "audited electron material contrast",
        },
        {
            "source_id": "SRC1333_4_1080_wep_bound",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1080_WEP_BOUND_IMPORT.csv",
            "needle": "BOUND1080_0_MICROSCOPE_WEP_source_charge",
            "role": "MICROSCOPE proxy WEP bound",
        },
        {
            "source_id": "SRC1333_5_954_action_clause",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_954_PARENT_ACTION_CLAUSE.csv",
            "needle": "PAC954_1_no_source_prefactors",
            "role": "parent action no-prefactor clause",
        },
        {
            "source_id": "SRC1333_6_954_label_forgetting",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_954_PARENT_LABEL_FORGETTING_ATTEMPT.csv",
            "needle": "PLF954_2_prefactor_obstruction",
            "role": "relative prefactor countermodel",
        },
        {
            "source_id": "SRC1333_7_955_minimal_lemma",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_955_MINIMAL_MATTER_ACTION_LEMMA.csv",
            "needle": "MMA955_6_verdict",
            "role": "minimal matter action lemma",
        },
        {
            "source_id": "SRC1333_8_955_prefactor_class",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_955_SOURCE_PREFACTOR_CLASSIFICATION.csv",
            "needle": "SPC955_2_relative_species_weight",
            "role": "prefactor classification",
        },
        {
            "source_id": "SRC1333_9_653_theorem_audit",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_653_THEOREM_ATTEMPT_AUDIT.csv",
            "needle": "TA653_0_diffeomorphism_invariance",
            "role": "symmetry routes that fail to derive common matter",
        },
        {
            "source_id": "SRC1333_10_1225_tau",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1225_TAU_WEP_SOURCE_ACQUISITION_TABLE.csv",
            "needle": "ACQ1225_1_product_convention",
            "role": "tau/source/readout normalization blocker",
        },
        {
            "source_id": "SRC1333_11_1332_validation",
            "local_path": "source-intake/mts_residuals/P8_Y5_BRR545_1332_VALIDATION.csv",
            "needle": "VAL1332_10_overall",
            "role": "1332 pass gate",
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

    electron_delta = read_csv(source_path("source-intake/mts_residuals/P8_Y5_R10_1330_AUDITED_ELECTRON_DELTA_VECTOR.csv"))[0]
    wep_bound = read_csv(source_path("source-intake/mts_residuals/P8_Y5_R10_1080_WEP_BOUND_IMPORT.csv"))[0]
    delta_f_e = float(electron_delta["abs_delta_fraction"])
    delta_f_e_unc = float(electron_delta["delta_uncertainty"])
    eta_bound = float(wep_bound["bound_value"])
    unit_kernel_beta_bound = eta_bound / delta_f_e
    unit_kernel_beta_bound_unc = unit_kernel_beta_bound * (delta_f_e_unc / delta_f_e)

    derivation = [
        {
            "attempt_id": "NSP1333_0_target",
            "claim": "derive no independent source-only species prefactors w_A from the parent action",
            "formal_move": "Allowed[S_matter] excludes terms sum_A w_A S_A where w_A is an active-source coefficient not fixed by nongravitational matter normalization",
            "result": "TARGET_SHARPENED",
            "gap": "must be parent schema theorem, not minimality taste",
            "parent_signed": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "attempt_id": "NSP1333_1_covariance",
            "claim": "diffeomorphism covariance forbids w_A",
            "formal_move": "S_matter=sum_A w_A S_A remains a scalar action if w_A are constant scalars",
            "result": "FAIL_COUNTERMODEL_SURVIVES",
            "gap": "covariance controls tensor form, not relative active-source normalization",
            "parent_signed": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "attempt_id": "NSP1333_2_same_action",
            "claim": "same matter action for dynamics and source forbids w_A",
            "formal_move": "E_Psi=delta S_matter/delta Psi and T=delta S_matter/delta g both come from the same S_matter",
            "result": "FAIL_COUNTERMODEL_SURVIVES",
            "gap": "a constant w_A inside S_A scales both dynamics and source; interactions/normalization can make it physical",
            "parent_signed": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "attempt_id": "NSP1333_3_field_rescaling",
            "claim": "field redefinitions remove all w_A",
            "formal_move": "Psi_A -> sqrt(w_A) Psi_A can absorb a free quadratic prefactor",
            "result": "FAIL_NOT_GENERAL",
            "gap": "interactions, charges, masses, quantum normalization, and clock standards can move the prefactor into observable theta_A",
            "parent_signed": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "attempt_id": "NSP1333_4_minimal_schema",
            "claim": "parent schema excludes source-only prefactors by construction",
            "formal_move": "theta_A may contain measured nongravitational constants; active-source multipliers w_A are not admissible parent fields",
            "result": "EXACT_SCHEMA_CONDITIONAL_NOT_DERIVED",
            "gap": "needs primitive parent admissibility principle or explicit action signature",
            "parent_signed": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "attempt_id": "NSP1333_5_verdict",
            "claim": "no-source-prefactor theorem is derived",
            "formal_move": "combine covariance, same-action principle, field rescaling, and minimal schema",
            "result": "NOT_DERIVED_CURRENT_CORPUS",
            "gap": "relative w_A countermodel remains legal unless the parent schema forbids it",
            "parent_signed": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    countermodels = [
        {
            "countermodel_id": "CM1333_0_relative_species_weight",
            "form": "S_matter = sum_A w_A S_A[Psi_A,e_obs,theta_A]",
            "survives": "diffeomorphism covariance; additivity; same Hilbert variation",
            "breaks": "component/common-mode collapse if w_A/w_B differs",
            "required_response": "forbid by parent schema or bound epsilon_A",
            "status": "LIVE_COUNTERMODEL",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "countermodel_id": "CM1333_1_hidden_marker_weight",
            "form": "w_A = w_common(1 + epsilon marker_A)",
            "survives": "if marker is quotient-owned or post-readout and not forbidden",
            "breaks": "no-shadow/no-marker source theorem",
            "required_response": "no-spurion theorem or retained residual vector",
            "status": "LIVE_COUNTERMODEL",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "countermodel_id": "CM1333_2_nonHilbert_current_weight",
            "form": "J_source = kappa T_Hilbert + zeta_A J_NH,A",
            "survives": "unless non-Hilbert currents are absent/exact/projected silent",
            "breaks": "source-current uniqueness",
            "required_response": "non-Hilbert current gate or finite source row",
            "status": "LIVE_COUNTERMODEL",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    schema_options = [
        {
            "schema_id": "SCHEMA1333_0_strict_minimal_matter",
            "admissible_action": "S_matter[Psi,e_obs,theta] with no source-only w_A slots",
            "derivation_status": "CLOSURE_SCHEMA_NOT_DERIVED",
            "benefit": "common-mode source coupling and GR-like source side become conditionally available",
            "risk": "must be justified as primitive parent action rule, not retrofitted to WEP",
            "selected": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "schema_id": "SCHEMA1333_1_finite_prefactor_branch",
            "admissible_action": "S_matter=sum_A w_A S_A with epsilon_A retained as finite source residual",
            "derivation_status": "COUNTERMODEL_COMPATIBLE",
            "benefit": "honest finite-bound programme if no-prefactor theorem fails",
            "risk": "less GR-like; must survive WEP/clock/PPN bounds",
            "selected": True,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    electron_bound = [
        {
            "bound_id": "EB1333_0_unit_kernel_electron_prefactor",
            "coefficient": "epsilon_e_or_delta_w_e",
            "assumption": "single electron residual component, unit source/readout kernel, no cancellation with other components",
            "eta_bound": fmt(eta_bound),
            "eta_bound_source": wep_bound["bound_source"],
            "delta_F_e_abs": fmt(delta_f_e),
            "delta_F_e_uncertainty": fmt(delta_f_e_unc),
            "required_abs_coefficient_max": fmt(unit_kernel_beta_bound),
            "coefficient_uncertainty_from_delta_only": fmt(unit_kernel_beta_bound_unc),
            "status": "FINITE_PROXY_BOUND_CONTRACT_NONCLAIM",
            "blocks_claim": "tau_WEP/source/readout normalization missing; other components unresolved; no parent coefficient source",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "bound_id": "EB1333_1_claim_grade_requirements",
            "coefficient": "epsilon_e_or_delta_w_e",
            "assumption": "claim-grade finite electron residual",
            "eta_bound": fmt(eta_bound),
            "eta_bound_source": wep_bound["bound_source"],
            "delta_F_e_abs": fmt(delta_f_e),
            "delta_F_e_uncertainty": fmt(delta_f_e_unc),
            "required_abs_coefficient_max": fmt(unit_kernel_beta_bound),
            "coefficient_uncertainty_from_delta_only": fmt(unit_kernel_beta_bound_unc),
            "status": "MISSING_PARENT_INPUTS",
            "blocks_claim": "needs source-worldtube profile, readout kernel, same-branch product convention, and parent coefficient units/sign",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    runner = [
        {
            "runner_id": "RUN1333_0_no_prefactor_derivation",
            "target": "derive common-mode source coupling from no-source-prefactor parent schema",
            "input_status": "DERIVATION_ATTEMPT_FAILED_COUNTERMODEL_SURVIVES",
            "runner_status": "REFUSED_NO_ZERO_PROMOTION",
            "reason": "no-prefactor clause remains a parent schema condition, not a derived theorem",
            "score_ready": False,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "runner_id": "RUN1333_1_electron_bound_contract",
            "target": "finite electron source-prefactor residual",
            "input_status": "PROXY_BOUND_CONTRACT_AVAILABLE_NONCLAIM",
            "runner_status": "BOUND_STAGED_NOT_SCOREABLE",
            "reason": "unit-kernel bound exists, but tau/source/readout and parent coefficient map are missing",
            "score_ready": False,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    anti_shortcut = [
        {
            "gate_id": "SHORT1333_0_no_minimality_as_derivation",
            "shortcut": "treat aesthetic minimal matter action as proof",
            "enforcement": "REFUSED",
            "status": "ENFORCED",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "gate_id": "SHORT1333_1_no_covariance_overclaim",
            "shortcut": "claim covariance forbids relative w_A",
            "enforcement": "REFUSED by CM1333_0",
            "status": "ENFORCED",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "gate_id": "SHORT1333_2_no_unit_kernel_claim",
            "shortcut": "treat unit-kernel electron coefficient bound as WEP pass",
            "enforcement": "REFUSED",
            "status": "ENFORCED",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "gate_id": "SHORT1333_3_no_local_GR_claim",
            "shortcut": "promote source-side work to full local GR/Newton derivation",
            "enforcement": "REFUSED",
            "status": "ENFORCED",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    decision = [
        {
            "decision_id": "DEC1333_0_derivation_result",
            "decision": "no-source-prefactor clause is not derived from current premises",
            "because": "relative constant w_A countermodel survives covariance, additivity, and same-action variation",
            "effect": "common-mode/local-GR source route remains conditional rather than promoted",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "decision_id": "DEC1333_1_fallback_bound",
            "decision": "stage finite electron residual coefficient bound as nonclaim",
            "because": "audited electron contrast plus MICROSCOPE proxy bound gives a useful pressure scale",
            "effect": "epsilon_e must be below the unit-kernel proxy scale before any electron-only residual branch could survive",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    next_target = [
        {
            "next_id": "NEXT1333_0_1334",
            "target_file": "1334-Y5-R10-RAB-parent-admissibility-principle-or-electron-coefficient-source-acquisition.md",
            "target_script": "scripts/Y5_R10_RAB_parent_admissibility_principle_or_electron_coefficient_source_acquisition.py",
            "task": "try to derive a primitive parent admissibility principle that excludes active-source prefactors w_A; if it fails, source or bound the electron coefficient epsilon_e in the same WEP/readout convention",
            "success_condition": "either source-only prefactors are forbidden by a parent action admissibility theorem, or epsilon_e gets a source-backed nonclaim coefficient prior/bound contract",
            "do_not": "do not use minimality taste as proof, do not claim WEP/local GR, do not tune Ti/Pt, and do not mix branches",
            "valid_for_claim": False,
            "claim_allowed": False,
        }
    ]

    tables_for_nonclaim = [
        source_register,
        derivation,
        countermodels,
        schema_options,
        electron_bound,
        runner,
        anti_shortcut,
        decision,
        next_target,
    ]

    source_anchor_count = sum(1 for row in source_register if row["exists"] and row["needle_found"])
    derivation_not_promoted = any(row["attempt_id"] == "NSP1333_5_verdict" and row["result"] == "NOT_DERIVED_CURRENT_CORPUS" for row in derivation)
    countermodels_live = len(countermodels) == 3 and all(row["status"] == "LIVE_COUNTERMODEL" for row in countermodels)
    bound_finite = all(finite_positive(row["required_abs_coefficient_max"]) for row in electron_bound)
    bound_nonclaim = all(is_false(row["valid_for_claim"]) and is_false(row["claim_allowed"]) for row in electron_bound)
    runner_refuses = all(row["score_ready"] is False and row["valid_prediction_row"] is False for row in runner)
    shortcuts_enforced = all(row["status"] == "ENFORCED" for row in anti_shortcut)
    nonclaim = all_nonclaim(tables_for_nonclaim)
    formal_clean = len(generated_inside_formalization()) == 0
    next_is_1334 = next_target[0]["target_file"].startswith("1334-")

    validations = [
        validation_row(
            "VAL1333_0_sources_exist",
            "registered source paths exist and anchors are found",
            source_anchor_count == len(source_register),
            f"{source_anchor_count}/{len(source_register)} source anchors found",
        ),
        validation_row(
            "VAL1333_1_derivation_not_promoted",
            "no-source-prefactor derivation is not promoted without parent schema theorem",
            derivation_not_promoted,
            "NSP1333_5_verdict=NOT_DERIVED_CURRENT_CORPUS",
        ),
        validation_row(
            "VAL1333_2_countermodels_live",
            "relative source-prefactor countermodels remain live",
            countermodels_live,
            ";".join(f"{row['countermodel_id']}={row['status']}" for row in countermodels),
        ),
        validation_row(
            "VAL1333_3_electron_bound_finite",
            "finite electron residual bound contract has positive numeric coefficient targets",
            bound_finite,
            f"unit_kernel_bound={fmt(unit_kernel_beta_bound)};delta_F_e={fmt(delta_f_e)};eta_bound={fmt(eta_bound)}",
        ),
        validation_row(
            "VAL1333_4_electron_bound_nonclaim",
            "electron bound rows remain nonclaim",
            bound_nonclaim,
            ";".join(f"{row['bound_id']}={row['status']}" for row in electron_bound),
        ),
        validation_row(
            "VAL1333_5_runners_refuse_claims",
            "runners refuse WEP/full Delta_w/local-GR scoring",
            runner_refuses,
            ";".join(f"{row['runner_id']}={row['runner_status']}" for row in runner),
        ),
        validation_row(
            "VAL1333_6_shortcuts_enforced",
            "anti-shortcut gates are enforced",
            shortcuts_enforced,
            ";".join(row["gate_id"] for row in anti_shortcut),
        ),
        validation_row(
            "VAL1333_7_nonclaim_policy",
            "all generated rows remain nonclaim",
            nonclaim,
            "valid_for_claim=false and claim_allowed=false where present",
        ),
        validation_row(
            "VAL1333_8_formalization_untouched",
            "formalization-workbench untouched by generated outputs",
            formal_clean,
            f"formalization_generated_output_count={len(generated_inside_formalization())}",
        ),
        validation_row(
            "VAL1333_9_next_target_1334",
            "next target routes to parent admissibility principle or electron coefficient acquisition",
            next_is_1334,
            str(next_target[0]["target_file"]),
        ),
    ]
    validations.append(
        validation_row(
            "VAL1333_10_overall",
            "overall 1333 validation",
            all(row["status"] == "PASS" for row in validations),
            "1333 rejects no-prefactor derivation from current premises and stages a finite electron residual bound contract",
        )
    )

    write_csv(SOURCE_REGISTER_PATH, source_register)
    write_csv(DERIVATION_PATH, derivation)
    write_csv(COUNTERMODEL_PATH, countermodels)
    write_csv(SCHEMA_OPTIONS_PATH, schema_options)
    write_csv(ELECTRON_BOUND_PATH, electron_bound)
    write_csv(RUNNER_PATH, runner)
    write_csv(ANTI_SHORTCUT_PATH, anti_shortcut)
    write_csv(DECISION_PATH, decision)
    write_csv(NEXT_PATH, next_target)
    write_csv(VALIDATION_PATH, validations)

    doc = f"""# {TITLE}

**Current verdict:** 1333 does not derive the no-source-prefactor parent theorem. A relative constant source prefactor `w_A` remains a legal countermodel under covariance, additivity, and same-action variation unless the parent schema explicitly forbids it.

**Main progress:** the failure is bounded. The audited electron contrast plus the MICROSCOPE proxy bound gives a nonclaim unit-kernel pressure scale: `|epsilon_e| <= {fmt(unit_kernel_beta_bound)}` for an electron-only residual branch.

**Decision:** the clean GR-like source route remains conditional. The next step must either derive a primitive parent admissibility principle excluding active-source prefactors, or source/bound the finite electron coefficient in the same WEP/readout convention.

## Source Register
{markdown_table(source_register, ["source_id", "local_path", "needle", "exists", "needle_found", "role", "valid_for_claim", "claim_allowed"])}

## No-Source-Prefactor Derivation Attempt
{markdown_table(derivation, ["attempt_id", "claim", "formal_move", "result", "gap", "parent_signed", "valid_for_claim", "claim_allowed"])}

## Source Prefactor Countermodel Ledger
{markdown_table(countermodels, ["countermodel_id", "form", "survives", "breaks", "required_response", "status", "valid_for_claim", "claim_allowed"])}

## Parent Schema Options
{markdown_table(schema_options, ["schema_id", "admissible_action", "derivation_status", "benefit", "risk", "selected", "valid_for_claim", "claim_allowed"])}

## Electron Residual Bound Contract
{markdown_table(electron_bound, ["bound_id", "coefficient", "assumption", "eta_bound", "eta_bound_source", "delta_F_e_abs", "delta_F_e_uncertainty", "required_abs_coefficient_max", "coefficient_uncertainty_from_delta_only", "status", "blocks_claim", "valid_for_claim", "claim_allowed"])}

## WEP Runner Update
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

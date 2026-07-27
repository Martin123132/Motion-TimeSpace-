from __future__ import annotations

import csv
from pathlib import Path


PACK_ID = "P8_Y5_R10_1322"
TITLE = "1322-Y5-R10-RAB-clock-tau-readout-map-derivation-or-source-rejection"
ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = ROOT / "source-intake" / "mts_residuals"
DOC_PATH = ROOT / f"{TITLE}.md"
FORMALIZATION = ROOT.parent / "formalization-workbench"

SOURCE_REGISTER_PATH = OUT_DIR / f"{PACK_ID}_SOURCE_REGISTER.csv"
DERIVATION_ATTEMPT_PATH = OUT_DIR / f"{PACK_ID}_TAU_READOUT_DERIVATION_ATTEMPT.csv"
GAP_LEDGER_PATH = OUT_DIR / f"{PACK_ID}_CLOCK_READOUT_GAP_LEDGER.csv"
DIRECT_REQUIREMENTS_PATH = OUT_DIR / f"{PACK_ID}_DIRECT_PRODUCT_SOURCE_REQUIREMENTS.csv"
RUNNER_UPDATE_PATH = OUT_DIR / f"{PACK_ID}_CLOCK_RUNNER_UPDATE.csv"
ANTI_SHORTCUT_PATH = OUT_DIR / f"{PACK_ID}_ANTI_SHORTCUT_GATES.csv"
DECISION_PATH = OUT_DIR / f"{PACK_ID}_DECISION_LEDGER.csv"
NEXT_PATH = OUT_DIR / f"{PACK_ID}_NEXT_TARGET.csv"
VALIDATION_PATH = OUT_DIR / "P8_Y5_BRR545_1322_VALIDATION.csv"


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
        DERIVATION_ATTEMPT_PATH,
        GAP_LEDGER_PATH,
        DIRECT_REQUIREMENTS_PATH,
        RUNNER_UPDATE_PATH,
        ANTI_SHORTCUT_PATH,
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
            "source_id": "SRC1322_0_1321_next",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1321_NEXT_TARGET.csv",
            "needle": "NEXT1321_0_1322",
            "role": "handoff into clock tau/readout derivation attempt",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "source_id": "SRC1322_1_1321_runner",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1321_CLOCK_FIRST_FILL_RUNNER.csv",
            "needle": "CLKRUN1321_0_best_clock_bound",
            "role": "current refused clock runner",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "source_id": "SRC1322_2_1052_tau",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1052_TAU_CLOCK_XHAT_NORMALIZATION_AUDIT.csv",
            "needle": "TCN1052_4_verdict",
            "role": "latest tau_clock/Xhat normalization audit",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "source_id": "SRC1322_3_647_tau",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_647_TAU_CLOCK_MAP.csv",
            "needle": "TAU647_0_time_drift",
            "role": "tau clock map definitions",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "source_id": "SRC1322_4_646_projection",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_646_CLOCK_PROJECTION_LEDGER.csv",
            "needle": "CPL646_1_time_drift",
            "role": "clock projection law",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "source_id": "SRC1322_5_646_sensitivity",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_646_CLOCK_ALPHA_SENSITIVITY_SOURCE.csv",
            "needle": "CAS646_1_YbE3E2",
            "role": "source-backed clock alpha sensitivities",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "source_id": "SRC1322_6_1002_time",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1002_TIME_PROFILE_RUNNER.csv",
            "needle": "REFUSED_MISSING_STATIONARY_TAU_PROVENANCE",
            "role": "time profile runner rejecting missing stationary tau provenance",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "source_id": "SRC1322_7_685_killing",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_685_KILLING_CLOCK_GATE.csv",
            "needle": "KCG685_7_total",
            "role": "Killing/clock/tau gate",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "source_id": "SRC1322_8_766_lock",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_766_CLOCK_ALPHA_SOURCE_LOCK.csv",
            "needle": "CAS646_1_YbE3E2",
            "role": "clock alpha source lock",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "source_id": "SRC1322_9_948_runner",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_948_CLOCK_PRODUCT_BOUND_RUNNER.csv",
            "needle": "CLK948_1_CAS646_1_YbE3E2",
            "role": "prior clock product bound runner",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]
    for row in source_register:
        exists, needle_found = exists_and_contains(str(row["local_path"]), str(row["needle"]))
        row["exists"] = exists
        row["needle_found"] = needle_found

    current_runner = read_csv(source_path("source-intake/mts_residuals/P8_Y5_R10_1321_CLOCK_FIRST_FILL_RUNNER.csv"))[0]

    derivation_attempt = [
        {
            "attempt_id": "TAU1322_0_product_definition",
            "target": "tau_clock_time definition",
            "candidate_law": "tau_clock_time := d chi_X / dt and d ln(alpha_EM)/dt = b_alpha*tau_clock_time",
            "source_evidence": "TCN1052_0_product_definition;TAU647_0_time_drift;CPL646_1_time_drift",
            "attempt_result": "DEFINED_PRODUCT_MAP_NOT_PARENT_DERIVED",
            "blocker": "chi_X parent state and local time projection are not derived",
            "claim_effect": "clock product bound can be imported, but no MTS predicted product is scored",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "attempt_id": "TAU1322_1_h0_diagnostic",
            "target": "H0-normalized tau route",
            "candidate_law": "tau_clock_time = H0*d chi_X/dN",
            "source_evidence": "TCN1052_1_H0_diagnostic;TAU647_1_H0_normalized_drift",
            "attempt_result": "DIAGNOSTIC_ONLY_NOT_READOUT_DERIVATION",
            "blocker": "no parent proof that lab clock tau equals cosmological H0*dchi_X/dN",
            "claim_effect": "H0-normalized number remains diagnostic and cannot define tau",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "attempt_id": "TAU1322_2_chix_coordinate",
            "target": "chi_X normalization",
            "candidate_law": "d ln(alpha_EM)=b_alpha*d chi_X",
            "source_evidence": "TCN1052_2_chix_closure_coordinate;TAU647_0_time_drift",
            "attempt_result": "CLOSURE_COORDINATE_ONLY",
            "blocker": "chi_X is not identified with a parent-owned local field or normalized vertical norm",
            "claim_effect": "factorized product remains a coordinate convention unless b_alpha and tau are sourced",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "attempt_id": "TAU1322_3_local_silence",
            "target": "tau_clock_time=0 local silence branch",
            "candidate_law": "tau_clock_time=0 in strict local coframe or closed/gapped local boundary state",
            "source_evidence": "TCN1052_3_local_silence;TAU647_3_local_silence;KCG685_7_total",
            "attempt_result": "CONDITIONAL_ONLY_NOT_ACTIVE",
            "blocker": "strict-local representative, closed/gapped split, stationary tau, and clock normalization are not parent-proved",
            "claim_effect": "cannot use local silence to evade clock bounds",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "attempt_id": "TAU1322_4_clock_model",
            "target": "clock sensitivity/readout model",
            "candidate_law": "d ln R_ab = DeltaK_alpha*d ln(alpha_EM)",
            "source_evidence": "CAS646_1_YbE3E2;CPL646_0_pair_ratio;CLK1047_1_CAS646_1_YbE3E2",
            "attempt_result": "SOURCE_SENSITIVITY_PRESENT_MTS_READOUT_MISSING",
            "blocker": "ordinary clock sensitivity exists, but MTS readout kernel and tau map are missing",
            "claim_effect": "clock pair and DeltaK can be used in a future direct product row only",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "attempt_id": "TAU1322_5_time_profile",
            "target": "stationary tau/time profile proof",
            "candidate_law": "parent-signed stationary tau or finite same-frame time profile",
            "source_evidence": "TPR1002_*;KCG685_0_through_7",
            "attempt_result": "REFUSED_MISSING_STATIONARY_TAU_PROVENANCE",
            "blocker": "time parameter, tau definition, clock lock, Hamiltonian integrability, fixed reference, and no-exchange certificates are missing",
            "claim_effect": "no stationary tau zero switch and no time-profile fallback can be used for clocks",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    gap_ledger = [
        {
            "gap_id": "GAP1322_0_chix_parent",
            "missing_object": "parent-owned chi_X state or vertical norm",
            "blocks": "tau_clock_time as physical readout",
            "current_best": "closure coordinate d ln(alpha_EM)=b_alpha*d chi_X",
            "required_resolution": "derive chi_X from parent fields and normalization, or source a direct clock product without chi_X",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "gap_id": "GAP1322_1_local_time_projection",
            "missing_object": "local time projection dt or tau_obs",
            "blocks": "d chi_X/dt as lab clock observable",
            "current_best": "tau_clock_time := d chi_X/dt definition",
            "required_resolution": "parent-selected observed time vector and clock normalization theorem",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "gap_id": "GAP1322_2_clock_readout_kernel",
            "missing_object": "MTS clock readout kernel",
            "blocks": "direct P_clock_alpha prediction",
            "current_best": "source-backed DeltaK_alpha sensitivities",
            "required_resolution": "map MTS alpha/time state into the Yb E3/E2 ratio convention with source path and units",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "gap_id": "GAP1322_3_balpha",
            "missing_object": "b_alpha/c_alpha source-backed coefficient or theorem-zero",
            "blocks": "factorized b_alpha*tau_clock_time product",
            "current_best": "parent signature route demoted to closure-only",
            "required_resolution": "source-backed coefficient or signed alpha F2 owner certificate",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "gap_id": "GAP1322_4_stationary_tau",
            "missing_object": "parent-signed stationary/local silence tau certificate",
            "blocks": "tau_clock_time=0 branch",
            "current_best": "conditional local silence row",
            "required_resolution": "strict local coframe/closed-gapped branch with clock lock and no-exchange certificate",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "gap_id": "GAP1322_5_cross_arena",
            "missing_object": "shared parent branch/readout functor",
            "blocks": "clock-to-WEP/R10 transfer",
            "current_best": "cross-arena row deferred by 1320/1321 gates",
            "required_resolution": "same-branch classifier and arena maps after at least one arena product is filled",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    direct_requirements = [
        {
            "requirement_id": "DCP1322_0_clock_pair",
            "needed_object": "clock pair and DeltaK_alpha",
            "current_status": "SOURCE_BACKED_FOR_YB_E3_E2",
            "minimum_usable_form": "171Yb+ E3 / 171Yb+ E2; DeltaK_alpha=-6.95; source path/anchor",
            "source_hint": "P8_Y5_R10_646_CLOCK_ALPHA_SENSITIVITY_SOURCE.csv:CAS646_1_YbE3E2",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "requirement_id": "DCP1322_1_direct_product",
            "needed_object": "numeric P_clock_alpha_direct",
            "current_status": "MISSING_DIRECT_P_CLOCK_ALPHA",
            "minimum_usable_form": "yr^-1 value with sign/absolute convention, model definition, source path, and source anchor",
            "source_hint": "future direct MTS clock product source or derivation",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "requirement_id": "DCP1322_2_readout_kernel",
            "needed_object": "MTS clock readout kernel",
            "current_status": "MISSING_MTS_CLOCK_READOUT_MODEL",
            "minimum_usable_form": "functional mapping MTS alpha/time state to d ln R_YbE3E2/dt with units",
            "source_hint": "future clock readout derivation/source",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "requirement_id": "DCP1322_3_tau_clock",
            "needed_object": "tau_clock_time",
            "current_status": "DEFINED_NOT_PARENT_DERIVED",
            "minimum_usable_form": "d chi_X/dt with parent-owned chi_X and lab time projection, or source-backed direct product bypass",
            "source_hint": "P8_Y5_R10_1052_TAU_CLOCK_XHAT_NORMALIZATION_AUDIT.csv:TCN1052_0_product_definition",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "requirement_id": "DCP1322_4_balpha",
            "needed_object": "b_alpha/c_alpha",
            "current_status": "MISSING_SOURCE_BACKED_COEFFICIENT_OR_THEOREM_ZERO",
            "minimum_usable_form": "numeric coefficient with source path or signed alpha F2 theorem-zero certificate",
            "source_hint": "parent theorem-zero route currently closure-only",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "requirement_id": "DCP1322_5_units_provenance",
            "needed_object": "units/provenance/source anchor",
            "current_status": "MISSING_FOR_MTS_PRODUCT",
            "minimum_usable_form": "yr^-1 units, source path, equation reference, clock convention, and no-cross-arena-transfer statement",
            "source_hint": "required for any future direct or factorized product row",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    runner_update = [
        {
            "runner_id": "CLKRUN1322_0_tau_derivation_attempt",
            "source_runner_id": current_runner["runner_id"],
            "clock_pair": current_runner["clock_pair"],
            "comparison_bound_1sigma_yr_inv": current_runner["comparison_bound_1sigma_yr_inv"],
            "tau_derivation_status": "NOT_DERIVED",
            "direct_product_status": "MISSING_DIRECT_P_CLOCK_ALPHA",
            "factorized_product_status": "MISSING_B_ALPHA_AND_TAU_CLOCK_TIME",
            "standalone_balpha_status": "FORBIDDEN_SHORTCUT",
            "runner_status": "REFUSED",
            "refusal_reason": "tau_clock_time_defined_not_parent_derived;missing_direct_product;missing_readout_kernel;missing_balpha;standalone_balpha_forbidden",
            "score_ready": False,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        }
    ]

    anti_shortcut = [
        {
            "gate_id": "SHORT1322_0_no_definition_as_derivation",
            "shortcut": "treat tau_clock_time := d chi_X/dt as a parent-derived lab readout",
            "enforcement": "REFUSED until chi_X and local time projection are parent-owned",
            "status": "ENFORCED",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "gate_id": "SHORT1322_1_no_h0_tau",
            "shortcut": "use H0*dchi_X/dN diagnostic as tau_clock_time",
            "enforcement": "REFUSED; diagnostic only",
            "status": "ENFORCED",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "gate_id": "SHORT1322_2_no_local_silence",
            "shortcut": "set tau_clock_time=0 by local silence",
            "enforcement": "REFUSED until strict local/closed-gapped branch is parent-signed",
            "status": "ENFORCED",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "gate_id": "SHORT1322_3_no_standalone_balpha",
            "shortcut": "divide clock bound by guessed tau to infer b_alpha",
            "enforcement": "REFUSED; clock row scores products only",
            "status": "ENFORCED",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "gate_id": "SHORT1322_4_no_transfer",
            "shortcut": "transfer clock product to WEP/R10/local rows",
            "enforcement": "REFUSED until shared branch/readout functor is signed",
            "status": "ENFORCED",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    decisions = [
        {
            "decision_id": "DEC1322_0_tau_not_derived",
            "decision": "tau_clock_time/readout map is not derived",
            "because": "the corpus defines a product coordinate but does not parent-sign chi_X, lab time projection, or readout kernel",
            "next_action": "use direct-product source requirements rather than standalone b_alpha",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "decision_id": "DEC1322_1_clock_remains_best_first_fill",
            "decision": "clock row remains the first feasible finite row",
            "because": "the empirical bound and DeltaK are sourced, even though MTS product is still missing",
            "next_action": "build a direct clock product source pack / first-fill row that can accept real P_clock_alpha if derived later",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "decision_id": "DEC1322_2_no_claim",
            "decision": "no clock, alpha, WEP, R10, or local-GR claim",
            "because": "no numeric MTS product or signed readout theorem exists",
            "next_action": "1323 should instantiate the direct product source pack and optional placeholder-free acceptance runner",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    next_target = [
        {
            "next_id": "NEXT1322_0_1323",
            "target_file": "1323-Y5-R10-RAB-clock-direct-product-source-pack-and-acceptance-runner.md",
            "target_script": "scripts/Y5_R10_RAB_clock_direct_product_source_pack_and_acceptance_runner.py",
            "task": "build a source-pack and acceptance runner for direct P_clock_alpha rows using the Yb bound, while preserving refusal for missing MTS product and standalone b_alpha",
            "success_condition": "direct clock product rows have required source/provenance/units fields and the runner blocks all placeholder, H0-tau, standalone-balpha, and cross-arena shortcuts",
            "do_not": "do not claim clock pass; do not infer b_alpha; do not transfer clock row to WEP/R10/local-GR",
            "valid_for_claim": False,
            "claim_allowed": False,
        }
    ]

    validation = []
    sources_ok = all(compact_bool(row["exists"]) and compact_bool(row["needle_found"]) for row in source_register)
    validation.append(
        validation_row(
            "VAL1322_0_sources_exist",
            "registered source paths exist and anchors are found",
            sources_ok,
            f"{sum(compact_bool(row['exists']) and compact_bool(row['needle_found']) for row in source_register)}/{len(source_register)} source anchors found",
        )
    )
    validation.append(
        validation_row(
            "VAL1322_1_derivation_attempts_cover_routes",
            "tau/readout derivation attempts cover definition, H0, chi_X, local silence, clock model, and time profile",
            len(derivation_attempt) == 6
            and all(row["attempt_result"] != "DERIVED" for row in derivation_attempt),
            ";".join(row["attempt_id"] + ":" + row["attempt_result"] for row in derivation_attempt),
        )
    )
    validation.append(
        validation_row(
            "VAL1322_2_tau_not_promoted",
            "tau_clock_time is not promoted as a parent-derived readout",
            runner_update[0]["tau_derivation_status"] == "NOT_DERIVED",
            runner_update[0]["refusal_reason"],
        )
    )
    validation.append(
        validation_row(
            "VAL1322_3_direct_requirements_written",
            "direct clock product source requirements are explicit",
            len(direct_requirements) == 6
            and any(row["requirement_id"] == "DCP1322_1_direct_product" for row in direct_requirements),
            ";".join(row["requirement_id"] for row in direct_requirements),
        )
    )
    validation.append(
        validation_row(
            "VAL1322_4_runner_refuses",
            "clock runner remains refused after tau attempt",
            runner_update[0]["runner_status"] == "REFUSED",
            runner_update[0]["refusal_reason"],
        )
    )
    validation.append(
        validation_row(
            "VAL1322_5_shortcuts_enforced",
            "anti-shortcut gates are enforced",
            all(row["status"] == "ENFORCED" for row in anti_shortcut),
            ";".join(row["gate_id"] for row in anti_shortcut),
        )
    )
    csv_tables = [
        ("source", source_register),
        ("derivation", derivation_attempt),
        ("gaps", gap_ledger),
        ("requirements", direct_requirements),
        ("runner", runner_update),
        ("shortcuts", anti_shortcut),
        ("decisions", decisions),
        ("next", next_target),
    ]
    validation.append(
        validation_row(
            "VAL1322_6_nonclaim_policy",
            "all generated rows remain nonclaim",
            all_nonclaim([rows for _, rows in csv_tables]),
            "valid_for_claim=false and claim_allowed=false throughout generated tables",
        )
    )
    validation.append(
        validation_row(
            "VAL1322_7_formalization_untouched",
            "formalization-workbench untouched by generated outputs",
            not generated_inside_formalization(),
            f"formalization_generated_output_count={len(generated_inside_formalization())}",
        )
    )
    validation.append(
        validation_row(
            "VAL1322_8_next_target_1323",
            "next target routes to clock direct product source pack and acceptance runner",
            next_target[0]["target_file"].startswith("1323-Y5-R10-RAB-clock-direct-product"),
            str(next_target[0]["target_file"]),
        )
    )
    validation.append(
        validation_row(
            "VAL1322_9_overall",
            "overall 1322 validation",
            all(row["status"] == "PASS" for row in validation),
            "1322 rejects tau/readout derivation for now, writes direct product source requirements, and keeps standalone b_alpha refused",
        )
    )

    write_csv(SOURCE_REGISTER_PATH, source_register)
    write_csv(DERIVATION_ATTEMPT_PATH, derivation_attempt)
    write_csv(GAP_LEDGER_PATH, gap_ledger)
    write_csv(DIRECT_REQUIREMENTS_PATH, direct_requirements)
    write_csv(RUNNER_UPDATE_PATH, runner_update)
    write_csv(ANTI_SHORTCUT_PATH, anti_shortcut)
    write_csv(DECISION_PATH, decisions)
    write_csv(NEXT_PATH, next_target)
    write_csv(VALIDATION_PATH, validation)

    doc = f"""# 1322: RAB Clock Tau Readout Map Derivation Or Source Rejection

**Current verdict:** 1322 tries to derive `tau_clock_time`/clock readout and does not promote it. The corpus has a useful product definition, but not a parent-derived lab clock readout map.

**Main progress:** the clock route is now split cleanly: `tau_clock_time := d chi_X/dt` is a defined product coordinate, H0 normalization is diagnostic only, local silence is conditional/inactive, and the honest fallback is a direct sourced `P_clock_alpha` row.

**Decision:** build the direct clock product source pack next. The clock row remains the best first finite fill, but it still cannot claim standalone `b_alpha` or transfer to WEP/R10.

## Source Register
{markdown_table(source_register, ["source_id", "local_path", "needle", "exists", "needle_found", "role", "valid_for_claim", "claim_allowed"])}

## Tau Readout Derivation Attempt
{markdown_table(derivation_attempt, ["attempt_id", "target", "candidate_law", "source_evidence", "attempt_result", "blocker", "claim_effect", "valid_for_claim", "claim_allowed"])}

## Clock Readout Gap Ledger
{markdown_table(gap_ledger, ["gap_id", "missing_object", "blocks", "current_best", "required_resolution", "valid_for_claim", "claim_allowed"])}

## Direct Product Source Requirements
{markdown_table(direct_requirements, ["requirement_id", "needed_object", "current_status", "minimum_usable_form", "source_hint", "valid_for_claim", "claim_allowed"])}

## Clock Runner Update
{markdown_table(runner_update, ["runner_id", "source_runner_id", "clock_pair", "comparison_bound_1sigma_yr_inv", "tau_derivation_status", "direct_product_status", "factorized_product_status", "standalone_balpha_status", "runner_status", "refusal_reason", "score_ready", "valid_prediction_row", "valid_for_claim", "claim_allowed"])}

## Anti-Shortcut Gates
{markdown_table(anti_shortcut, ["gate_id", "shortcut", "enforcement", "status", "valid_for_claim", "claim_allowed"])}

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

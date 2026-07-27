from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path


BRANCH = "MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428"
ROOT = Path(__file__).resolve().parents[1]
REPO = ROOT.parent
FORMALIZATION = REPO / "formalization-workbench"
MTS_RESIDUALS = ROOT / "source-intake" / "mts_residuals"
SOURCE_WEIGHT_DOCS = ROOT / "source-intake" / "source-weight" / "docs"
RAB_QUEUE = ROOT / "source-intake" / "rab-sector" / "acquisition-queue"
MICROSCOPE_COEFFS = ROOT / "source-intake" / "microscope" / "branch_locked_wep" / "coefficients"

DOC_PATH = ROOT / "1989-Y5-R2FR-WEP-source-weight-projection-denominator-or-Hilbert-signature.md"
VALIDATION_PATH = MTS_RESIDUALS / "P8_Y5_BRR545_1989_VALIDATION.csv"

SOURCES = {
    "1988_doc": {
        "path": ROOT / "1988-Y5-R2FR-action-weight-source-beta-theorem-or-finite-row-fill.md",
        "needles": ["NEXT1988_0_primary", "FIN1988_0_WEP_TiPt_inequality"],
    },
    "1988_validation": {
        "path": MTS_RESIDUALS / "P8_Y5_BRR545_1988_VALIDATION.csv",
        "needles": ["VAL1988_OVERALL", "PASS"],
    },
    "1935_doc": {
        "path": ROOT / "1935-Y5-R2FR-MTS-WEP-eta-projection-map-or-material-charge-ledger.md",
        "needles": ["ETA1935_4_mts_source_weight_form", "PB1935_1_exact_WEP_product_contract"],
    },
    "1935_contract": {
        "path": MTS_RESIDUALS / "P8_Y5_PARENT_QLOC_1935_MTS_WEP_PROJECTION_CONTRACT.csv",
        "needles": ["CON1935_2_universal_weight_sum", "MISSING_DENOMINATOR_CONTROL"],
    },
    "1935_product": {
        "path": MTS_RESIDUALS / "P8_Y5_PARENT_QLOC_1935_WEP_PRODUCT_BOUND_TARGET.csv",
        "needles": ["PB1935_0_linear_WEP_product_target", "EXACT_SCHEMA_READY_INPUTS_MISSING"],
    },
    "1934_bound": {
        "path": ROOT / "1934-Y5-R2FR-WEP-source-weight-first-finite-row-acquisition-nonclaim.md",
        "needles": ["WEP1934_0_MICROSCOPE_TiPt_eta", "2.7e-15"],
    },
    "1936_universality": {
        "path": ROOT / "1936-Y5-R2FR-source-weight-universality-theorem-or-TiPt-material-charge-ledger.md",
        "needles": ["UNIV1936_1_hilbert_source_theorem", "TIPT1936_5_eta_target"],
    },
    "1596_tau_law": {
        "path": ROOT / "1596-Y5-R2FR-tau-WEP-source-projection-or-action-measure-owner-last-gate.md",
        "needles": ["TCL1596_2_delta_w_amplitude_law", "NO_TAU_MIN_SOURCE"],
    },
    "1437_pwep_inputs": {
        "path": ROOT / "1437-Y5-R10-RAB-P-WEP-first-row-or-source-input-acquisition-ledger.md",
        "needles": ["IRA1437_0_C_parent", "DEC1437_0_first_row_refused"],
    },
}

OUTPUTS = {
    "source_register": MTS_RESIDUALS / "P8_Y5_PARENT_QLOC_1989_SOURCE_REGISTER.csv",
    "exact_projection": MTS_RESIDUALS / "P8_Y5_PARENT_QLOC_1989_EXACT_WEP_PROJECTION_INVERSION.csv",
    "denominator_gate": MTS_RESIDUALS / "P8_Y5_PARENT_QLOC_1989_DENOMINATOR_CONTROL_GATE.csv",
    "product_bound": MTS_RESIDUALS / "P8_Y5_PARENT_QLOC_1989_PRODUCT_BOUND_LEDGER.csv",
    "hilbert_route": MTS_RESIDUALS / "P8_Y5_PARENT_QLOC_1989_HILBERT_SIGNATURE_ROUTE.csv",
    "runner_dryrun": MTS_RESIDUALS / "P8_Y5_PARENT_QLOC_1989_RUNNER_DRYRUN.csv",
    "claim_gate": MTS_RESIDUALS / "P8_Y5_PARENT_QLOC_1989_CLAIM_GATE.csv",
    "decision": MTS_RESIDUALS / "P8_Y5_PARENT_QLOC_1989_DECISION_LEDGER.csv",
    "next": MTS_RESIDUALS / "P8_Y5_PARENT_QLOC_1989_NEXT_TARGET.csv",
    "source_weight": SOURCE_WEIGHT_DOCS / "WEP_SOURCE_WEIGHT_DENOMINATOR_GATE_1989_NONCLAIM.csv",
    "wep_coeffs": MICROSCOPE_COEFFS / "P8_Y5_PARENT_QLOC_1989_PRODUCT_DENOMINATOR_GATE_NONCLAIM.csv",
    "queue": RAB_QUEUE / "JR1989_DENOMINATOR_CONTROL_OR_TAU_MIN_QUEUE.csv",
}


def now() -> str:
    return datetime.now(timezone.utc).isoformat()


def ensure_dirs() -> None:
    for path in OUTPUTS.values():
        path.parent.mkdir(parents=True, exist_ok=True)
    VALIDATION_PATH.parent.mkdir(parents=True, exist_ok=True)


def base_row(stamp: str) -> dict[str, str]:
    return {
        "branch_id": BRANCH,
        "valid_for_claim": "false",
        "claim_allowed": "false",
        "generated_utc": stamp,
    }


def write_csv(path: Path, rows: list[dict[str, str]]) -> None:
    if not rows:
        raise ValueError(f"no rows for {path}")
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def source_register(stamp: str) -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    for source_id, spec in SOURCES.items():
        path = spec["path"]
        exists = path.exists()
        text = read_text(path) if exists else ""
        missing = [needle for needle in spec["needles"] if needle not in text]
        row = base_row(stamp)
        row.update(
            {
                "source_id": source_id,
                "source_path": str(path),
                "needed_for": "1989 WEP source-weight projection denominator gate",
                "needles": ";".join(spec["needles"]),
                "exists": str(exists),
                "anchor_found": str(exists and not missing),
                "missing_needles": ";".join(missing),
                "status": "EXISTS_NEEDLES_CONFIRMED" if exists and not missing else "MISSING_SOURCE_OR_ANCHOR",
            }
        )
        rows.append(row)
    return rows


def build_tables() -> dict[str, list[dict[str, str]]]:
    stamp = now()

    def row(data: dict[str, str]) -> dict[str, str]:
        merged = base_row(stamp)
        merged.update(data)
        return merged

    exact_projection = [
        row(
            {
                "projection_id": "PROJ1989_0_definitions",
                "symbols": "epsilon_A=P_WEP W_A; D=P_WEP DeltaW_TiPt; U=P_WEP SigmaW_TiPt",
                "formula": "eta_TiPt = 2D/(2+U)",
                "derivation_status": "EXACT_ALGEBRA_FROM_ETA_DEFINITION",
                "meaning": "D is the differential source-weight product; U is the common/sum denominator correction",
            }
        ),
        row(
            {
                "projection_id": "PROJ1989_1_inversion",
                "symbols": "D;U;eta_TiPt",
                "formula": "D = eta_TiPt*(2+U)/2",
                "derivation_status": "EXACT_INVERSION_IF_DENOMINATOR_NONZERO",
                "meaning": "the experiment bounds the aggregate product D only after denominator control, not DeltaW_TiPt alone",
            }
        ),
        row(
            {
                "projection_id": "PROJ1989_2_linear_limit",
                "symbols": "|U|<=u_max",
                "formula": "|D| <= eta_bound_abs*(1+u_max/2)",
                "derivation_status": "EXACT_ABSOLUTE_BOUND_UNDER_DENOMINATOR_ENVELOPE",
                "meaning": "the common shortcut |D|<=eta_bound_abs is only the u_max=0 or negligible-denominator limit",
            }
        ),
        row(
            {
                "projection_id": "PROJ1989_3_individual_weight_bound",
                "symbols": "DeltaW_TiPt;P_WEP",
                "formula": "if |P_WEP|>=P_min>0 then |DeltaW_TiPt| <= eta_bound_abs*(1+u_max/2)/P_min",
                "derivation_status": "CONDITIONAL_AMPLITUDE_LAW",
                "meaning": "without a sourced nonzero lower bound on P_WEP or tau_WEP*S_Earth, MICROSCOPE does not bound DeltaW_TiPt individually",
            }
        ),
    ]

    denominator_gate = [
        row(
            {
                "gate_id": "DEN1989_0_denominator_nonzero",
                "needed_input": "2+P_WEP SigmaW_TiPt is nonzero in the MICROSCOPE branch",
                "acceptable_evidence": "parent theorem, finite envelope |P_WEP SigmaW_TiPt|<2, or sourced denominator floor",
                "current_status": "MISSING_DENOMINATOR_CONTROL",
                "effect": "exact eta formula cannot be used as a claim-grade inversion without this",
            }
        ),
        row(
            {
                "gate_id": "DEN1989_1_linear_regime",
                "needed_input": "u_max for |P_WEP SigmaW_TiPt|",
                "acceptable_evidence": "sourced small-residual envelope with units/convention, or theorem U=0",
                "current_status": "MISSING_U_MAX",
                "effect": "linear product bound |P_WEP DeltaW|<=2.7e-15 is not claim-grade",
            }
        ),
        row(
            {
                "gate_id": "DEN1989_2_tau_lower_bound",
                "needed_input": "P_min or tau_min such that |P_WEP|>=P_min>0",
                "acceptable_evidence": "tau_WEP/source-worldtube/readout derivation or source-backed lower-bound row",
                "current_status": "NO_TAU_MIN_SOURCE",
                "effect": "no individual DeltaW_TiPt amplitude bound follows from the product bound",
            }
        ),
        row(
            {
                "gate_id": "DEN1989_3_material_charges",
                "needed_input": "W_Ti, W_Pt, DeltaW_TiPt, SigmaW_TiPt in one MTS basis",
                "acceptable_evidence": "parent zero theorem or source-backed material response tensor",
                "current_status": "MISSING_MATERIAL_CHARGES",
                "effect": "no numeric eta_pred can be computed",
            }
        ),
        row(
            {
                "gate_id": "DEN1989_4_readout_sign",
                "needed_input": "MICROSCOPE body order, sensitive-axis sign, and readout/orbit convention",
                "acceptable_evidence": "official source extraction or reproducible local manifest",
                "current_status": "SOURCE_CANDIDATE_NOT_EXTRACTED",
                "effect": "numeric comparison remains blocked even with symbolic product bound",
            }
        ),
    ]

    product_bound = [
        row(
            {
                "bound_id": "PB1989_0_exact_product_target",
                "quantity": "D=P_WEP*DeltaW_TiPt",
                "bound_formula": "|D| <= eta_bound_abs*|2+U|/2",
                "bound_value_if_U_controlled": "2.7e-15*(1+u_max/2)",
                "required_inputs": "eta_bound_abs=2.7e-15; U envelope u_max or exact U; sign/readout convention",
                "status": "EXACT_FORMULA_READY_DENOMINATOR_MISSING",
            }
        ),
        row(
            {
                "bound_id": "PB1989_1_linear_anchor",
                "quantity": "D=P_WEP*DeltaW_TiPt",
                "bound_formula": "|D| <= 2.7e-15",
                "bound_value_if_U_controlled": "2.7e-15",
                "required_inputs": "prove |U| negligible or U=0; source/environment convention fixed",
                "status": "LINEAR_LIMIT_NOT_CLAIM_GRADE",
            }
        ),
        row(
            {
                "bound_id": "PB1989_2_deltaW_amplitude",
                "quantity": "DeltaW_TiPt",
                "bound_formula": "|DeltaW_TiPt| <= 2.7e-15*(1+u_max/2)/P_min",
                "bound_value_if_U_controlled": "symbolic only",
                "required_inputs": "P_min>0, u_max, material/source convention",
                "status": "NO_TAU_OR_P_MIN_SOURCE",
            }
        ),
        row(
            {
                "bound_id": "PB1989_3_zero_route",
                "quantity": "DeltaW_TiPt",
                "bound_formula": "DeltaW_TiPt=0 implies eta_TiPt=0 for finite nonzero denominator",
                "bound_value_if_U_controlled": "0",
                "required_inputs": "parent-signed universal Hilbert source coupling and no source-weight slot",
                "status": "CONDITIONAL_THEOREM_NOT_PARENT_SIGNED",
            }
        ),
    ]

    hilbert_route = [
        row(
            {
                "route_id": "HIL1989_0_clean_GR_route",
                "claim_if_signed": "ordinary matter has one universal Hilbert source and no species/source multiplier",
                "result": "DeltaW_TiPt=0 and eta_TiPt=0 exactly",
                "current_status": "NOT_PARENT_SIGNED",
                "why_not_closed": "no-source-weight, common current, and readout preservation clauses remain unsigned",
            }
        ),
        row(
            {
                "route_id": "HIL1989_1_finite_route",
                "claim_if_signed": "not applicable; source-weight residual survives",
                "result": "use exact product/denominator bound instead of a GR-like zero claim",
                "current_status": "FINITE_NONCLAIM_ROUTE_ACTIVE",
                "why_not_closed": "P_WEP, material charges, denominator envelope, and sign/readout rows missing",
            }
        ),
    ]

    runner_dryrun = [
        row(
            {
                "run_id": "RUN1989_0_exact_formula",
                "check": "exact eta projection inversion",
                "result": "PASS_SYMBOLIC",
                "reason": "eta=2D/(2+U) and D=eta(2+U)/2 are algebraic consequences of 1935",
            }
        ),
        row(
            {
                "run_id": "RUN1989_1_linear_bound",
                "check": "claim |P_WEP DeltaW|<=2.7e-15",
                "result": "FAIL_DENOMINATOR_MISSING",
                "reason": "u_max or U=0 has not been sourced/derived",
            }
        ),
        row(
            {
                "run_id": "RUN1989_2_deltaW_bound",
                "check": "claim individual DeltaW_TiPt bound",
                "result": "FAIL_P_MIN_MISSING",
                "reason": "P_WEP/tau_WEP lower bound is missing and tau=1 shortcut is forbidden",
            }
        ),
        row(
            {
                "run_id": "RUN1989_3_hilbert_zero",
                "check": "claim DeltaW_TiPt=0 from Hilbert source coupling",
                "result": "FAIL_PARENT_SIGNATURE_UNSIGNED",
                "reason": "conditional theorem remains exact but not parent-signed",
            }
        ),
        row(
            {
                "run_id": "RUN1989_4_verdict",
                "check": "1989 WEP denominator gate",
                "result": "DENOMINATOR_GATE_WRITTEN_NONCLAIM",
                "reason": "we have the exact product law and the exact missing inputs; no WEP/local-GR score",
            }
        ),
    ]

    claim_gate = [
        row(
            {
                "claim_id": "CG1989_0_exact_projection",
                "claim": "exact symbolic WEP product projection is derived",
                "status": "PASS_NONCLAIM_SYMBOLIC",
                "reason": "algebra is exact, but contains unsourced U, P_WEP, and material charges",
            }
        ),
        row(
            {
                "claim_id": "CG1989_1_linear_product_bound",
                "claim": "|P_WEP DeltaW_TiPt| <= 2.7e-15",
                "status": "FAIL_BLOCKED",
                "reason": "requires U=0/negligible or a sourced u_max denominator envelope",
            }
        ),
        row(
            {
                "claim_id": "CG1989_2_deltaW_bound",
                "claim": "DeltaW_TiPt individually bounded",
                "status": "FAIL_BLOCKED",
                "reason": "requires sourced P_min or tau_min; otherwise P_WEP can be arbitrarily small",
            }
        ),
        row(
            {
                "claim_id": "CG1989_3_wep_pass",
                "claim": "MTS passes MICROSCOPE/WEP",
                "status": "FAIL_BLOCKED",
                "reason": "no numeric eta_pred and no source-weight zero theorem",
            }
        ),
        row(
            {
                "claim_id": "CG1989_4_local_GR_Newton",
                "claim": "local GR/Newton source universality derived",
                "status": "FAIL_BLOCKED",
                "reason": "Hilbert signature route remains conditional",
            }
        ),
    ]

    decision = [
        row(
            {
                "decision_id": "DEC1989_0_exact_gain",
                "decision": "PRODUCT_DENOMINATOR_LAW_DERIVED",
                "because": "the WEP branch now has exact D=eta(2+U)/2 bookkeeping and no longer relies on a hidden linear shortcut",
                "next_action": "source or derive U envelope and P_min/tau_min, or close Hilbert source signature",
            }
        ),
        row(
            {
                "decision_id": "DEC1989_1_no_individual_bound",
                "decision": "NO_DELTAW_BOUND_WITHOUT_P_MIN",
                "because": "the experiment constrains P_WEP*DeltaW, not DeltaW alone; tau/P may vanish unless bounded away from zero",
                "next_action": "build tau/P lower-bound gate before any individual coefficient claim",
            }
        ),
        row(
            {
                "decision_id": "DEC1989_2_best_next",
                "decision": "TAU_OR_HILBERT_SIGNATURE_NEXT",
                "because": "the root fork is now clear: either universal source coupling kills DeltaW, or finite testing needs P_min and U_max",
                "next_action": "1990-Y5-R2FR-tau-WEP-lower-bound-or-Hilbert-source-signature.md",
            }
        ),
    ]

    next_target = [
        row(
            {
                "next_id": "NEXT1989_0_primary",
                "selection_status": "selected",
                "target_doc": "1990-Y5-R2FR-tau-WEP-lower-bound-or-Hilbert-source-signature.md",
                "target_script": "scripts/Y5_R2FR_tau_WEP_lower_bound_or_Hilbert_source_signature_1990.py",
                "task": "try to derive a nonzero P_WEP/tau_WEP lower bound and U denominator envelope, while keeping the parent Hilbert source signature route alive",
                "success_condition": "either P_min/u_max rows are sourced/derived for a finite nonclaim WEP product comparison, or DeltaW_TiPt is theorem-zero from a parent-signed Hilbert source clause",
                "do_not": "do not set tau_WEP=1, assume U=0, invent Ti/Pt charges, absorb relative weights into measured G, claim WEP/local-GR pass, or modify formalization-workbench",
            }
        )
    ]

    source_weight = [
        row(
            {
                "artifact_id": "SW1989_0_denominator_gate",
                "artifact_type": "WEP_source_weight_product_denominator_gate",
                "exact_law": "D=P_WEP*DeltaW_TiPt=eta_TiPt*(2+P_WEP*SigmaW_TiPt)/2",
                "claim_status": "NONCLAIM_DENOMINATOR_AND_PMIN_MISSING",
                "source_path": str(DOC_PATH),
            }
        )
    ]

    wep_coeffs = [
        row(
            {
                "coefficient_id": "WEP1989_0_product_bound_gate",
                "observable": "eta_TiPt",
                "eta_bound_abs": "2.7e-15",
                "aggregate_product": "D=P_WEP*DeltaW_TiPt",
                "denominator_term": "U=P_WEP*SigmaW_TiPt",
                "exact_bound": "|D| <= 2.7e-15*|2+U|/2",
                "missing_for_claim": "U envelope or U=0 theorem; P_min/tau_min for DeltaW; W_Ti/W_Pt; sign/readout convention",
                "status": "NONCLAIM_EXACT_GATE",
            }
        )
    ]

    queue = [
        row(
            {
                "queue_id": "JR1989_0_tau_denominator_gate",
                "priority": "1",
                "needed_input": "P_min/tau_min and U_max denominator envelope",
                "route": "derive from source-worldtube/readout projection or parent Hilbert source signature",
                "required_fields": "P_min;tau_min;u_max;confidence;basis;units;source_path;assumptions;valid_for_claim",
                "blocked_claims": "DeltaW bound;WEP pass;local_GR;Newton;PPN;R10",
            }
        )
    ]

    return {
        "source_register": source_register(stamp),
        "exact_projection": exact_projection,
        "denominator_gate": denominator_gate,
        "product_bound": product_bound,
        "hilbert_route": hilbert_route,
        "runner_dryrun": runner_dryrun,
        "claim_gate": claim_gate,
        "decision": decision,
        "next": next_target,
        "source_weight": source_weight,
        "wep_coeffs": wep_coeffs,
        "queue": queue,
    }


def validate(tables: dict[str, list[dict[str, str]]]) -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []

    def val(validation_id: str, status: str, detail: str) -> None:
        rows.append(
            {
                "validation_id": validation_id,
                "status": status,
                "detail": detail,
                "valid_for_claim": "false",
                "claim_allowed": "false",
            }
        )

    source_failures = [row for row in tables["source_register"] if row["status"] != "EXISTS_NEEDLES_CONFIRMED"]
    val("VAL1989_00_sources", "PASS" if not source_failures else "FAIL", "all source paths exist and needles found" if not source_failures else ";".join(row["source_id"] for row in source_failures))

    exact_formula = any(row["formula"] == "D = eta_TiPt*(2+U)/2" for row in tables["exact_projection"])
    linear_guard = any("u_max" in row["formula"] and "eta_bound_abs" in row["formula"] for row in tables["exact_projection"])
    val("VAL1989_01_exact_projection", "PASS" if exact_formula and linear_guard else "FAIL", "exact inversion and denominator-envelope law written")

    denom_missing = any(row["current_status"] == "MISSING_DENOMINATOR_CONTROL" for row in tables["denominator_gate"])
    tau_missing = any(row["current_status"] == "NO_TAU_MIN_SOURCE" for row in tables["denominator_gate"])
    val("VAL1989_02_missing_inputs_visible", "PASS" if denom_missing and tau_missing else "FAIL", "denominator and tau/P lower-bound blockers visible")

    exact_product = next((row for row in tables["product_bound"] if row["bound_id"] == "PB1989_0_exact_product_target"), None)
    product_ok = bool(exact_product and "2.7e-15*(1+u_max/2)" in exact_product["bound_value_if_U_controlled"])
    val("VAL1989_03_product_bound", "PASS" if product_ok else "FAIL", "product bound is exact/nonclaim with denominator control")

    runner_blocks = tables["runner_dryrun"][1]["result"] == "FAIL_DENOMINATOR_MISSING" and tables["runner_dryrun"][2]["result"] == "FAIL_P_MIN_MISSING"
    val("VAL1989_04_runner_blocks", "PASS" if runner_blocks else "FAIL", "runner refuses linear and individual DeltaW claims")

    gates_safe = all(row["status"] in {"PASS_NONCLAIM_SYMBOLIC", "FAIL_BLOCKED"} for row in tables["claim_gate"])
    val("VAL1989_05_claim_gates", "PASS" if gates_safe else "FAIL", "claim gates safe; symbolic pass only")

    next_ok = tables["next"][0]["target_doc"] == "1990-Y5-R2FR-tau-WEP-lower-bound-or-Hilbert-source-signature.md"
    val("VAL1989_06_next_target", "PASS" if next_ok else "FAIL", "1990 tau lower-bound/Hilbert signature target selected")

    all_rows = [row for rows_for_table in tables.values() for row in rows_for_table]
    flags_safe = all(row.get("valid_for_claim") == "false" and row.get("claim_allowed") == "false" for row in all_rows)
    val("VAL1989_07_claim_flags_safe", "PASS" if flags_safe else "FAIL", "claim flags all false")

    parse_failures = []
    for output_name, path in OUTPUTS.items():
        if not path.exists():
            parse_failures.append(f"{output_name}:missing")
            continue
        with path.open(newline="", encoding="utf-8") as handle:
            parsed = list(csv.DictReader(handle))
        if not parsed:
            parse_failures.append(f"{output_name}:empty")
    val("VAL1989_08_csv_parse", "PASS" if not parse_failures else "FAIL", "all generated CSVs parse with rows" if not parse_failures else ";".join(parse_failures))

    pycache_exists = (ROOT / "scripts" / "__pycache__").exists()
    val("VAL1989_09_pycache_absent", "PASS" if not pycache_exists else "FAIL", "scripts __pycache__ absent")

    formalization_artifacts = []
    if FORMALIZATION.exists():
        formalization_artifacts = [path for path in FORMALIZATION.rglob("*1989*")]
    val("VAL1989_10_formalization_untouched", "PASS" if not formalization_artifacts else "FAIL", f"formalization_1989_artifact_count={len(formalization_artifacts)}")

    overall = "PASS" if all(row["status"] == "PASS" for row in rows) else "FAIL"
    val("VAL1989_OVERALL", overall, "1989 WEP source-weight projection denominator gate")
    return rows


def markdown_table(rows: list[dict[str, str]]) -> str:
    if not rows:
        return ""
    headers = list(rows[0].keys())
    lines = [
        "| " + " | ".join(headers) + " |",
        "| " + " | ".join("---" for _ in headers) + " |",
    ]
    for row in rows:
        lines.append("| " + " | ".join(str(row.get(header, "")).replace("\n", " ") for header in headers) + " |")
    return "\n".join(lines)


def write_markdown(tables: dict[str, list[dict[str, str]]], validation_rows: list[dict[str, str]]) -> None:
    sections = [
        ("Source Register", tables["source_register"]),
        ("Exact Projection Inversion", tables["exact_projection"]),
        ("Denominator Control Gate", tables["denominator_gate"]),
        ("Product Bound Ledger", tables["product_bound"]),
        ("Hilbert Signature Route", tables["hilbert_route"]),
        ("Runner Dryrun", tables["runner_dryrun"]),
        ("Claim Gate", tables["claim_gate"]),
        ("Decision Ledger", tables["decision"]),
        ("Next Target", tables["next"]),
        ("Validation", validation_rows),
    ]
    lines = [
        "# 1989 Y5 R2FR: WEP Source-Weight Projection Denominator Or Hilbert Signature",
        "",
        "Private checkpoint. This sharpens the 1988 coupling result by separating the exact MICROSCOPE product law from the tempting but unsafe linear shortcut.",
        "",
        "Verdict: the exact WEP source-weight projection is now `D=P_WEP*DeltaW_TiPt=eta_TiPt*(2+U)/2`, where `U=P_WEP*SigmaW_TiPt`. The commonly useful bound `|P_WEP*DeltaW_TiPt| <= 2.7e-15` is only claim-grade if `U=0`, negligible, or source-bounded. An individual `DeltaW_TiPt` bound additionally needs a nonzero lower bound `|P_WEP|>=P_min>0`.",
        "",
        "So the project has moved forward, but not by claiming a WEP pass: the next missing object is either `P_min/u_max` from the WEP source/readout projection or the stronger parent Hilbert source signature that sets `DeltaW_TiPt=0` directly.",
        "",
        "No WEP, local-GR, Newton, R10, PPN, clock, orbital, or public claim follows from 1989.",
        "",
    ]
    for title, rows in sections:
        lines.extend([f"## {title}", "", markdown_table(rows), ""])
    DOC_PATH.write_text("\n".join(lines), encoding="utf-8")


def main() -> int:
    ensure_dirs()
    pycache_path = ROOT / "scripts" / "__pycache__"
    if pycache_path.exists():
        shutil.rmtree(pycache_path)
    tables = build_tables()
    for output_name, path in OUTPUTS.items():
        write_csv(path, tables[output_name])
    validation_rows = validate(tables)
    write_csv(VALIDATION_PATH, validation_rows)
    write_markdown(tables, validation_rows)
    if pycache_path.exists():
        shutil.rmtree(pycache_path)
    overall = validation_rows[-1]["status"]
    print(f"wrote {DOC_PATH}")
    print(f"wrote {VALIDATION_PATH}")
    print(f"VAL1989_OVERALL={overall}")
    return 0 if overall == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())

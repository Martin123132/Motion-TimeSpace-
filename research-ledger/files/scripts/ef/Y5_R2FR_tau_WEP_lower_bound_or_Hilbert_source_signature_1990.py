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

DOC_PATH = ROOT / "1990-Y5-R2FR-tau-WEP-lower-bound-or-Hilbert-source-signature.md"
VALIDATION_PATH = MTS_RESIDUALS / "P8_Y5_BRR545_1990_VALIDATION.csv"

SOURCES = {
    "1989_doc": {
        "path": ROOT / "1989-Y5-R2FR-WEP-source-weight-projection-denominator-or-Hilbert-signature.md",
        "needles": ["NEXT1989_0_primary", "DEN1989_2_tau_lower_bound"],
    },
    "1989_validation": {
        "path": MTS_RESIDUALS / "P8_Y5_BRR545_1989_VALIDATION.csv",
        "needles": ["VAL1989_OVERALL", "PASS"],
    },
    "1225_tau_contract": {
        "path": ROOT / "1225-Y5-R10-tau-WEP-source-worldtube-readout-projection.md",
        "needles": ["FORM1225_0_tau_WEP_functional", "TAU1225_6_verdict"],
    },
    "1596_tau_lower": {
        "path": ROOT / "1596-Y5-R2FR-tau-WEP-source-projection-or-action-measure-owner-last-gate.md",
        "needles": ["TCL1596_3_tau_null_escape", "TSA1596_3_tau_min"],
    },
    "1437_pwep_refusal": {
        "path": ROOT / "1437-Y5-R10-RAB-P-WEP-first-row-or-source-input-acquisition-ledger.md",
        "needles": ["PWA1437_0_first_row", "REFUSED_FIRST_ROW_MISSING_INPUTS"],
    },
    "1936_hilbert": {
        "path": ROOT / "1936-Y5-R2FR-source-weight-universality-theorem-or-TiPt-material-charge-ledger.md",
        "needles": ["UNIV1936_1_hilbert_source_theorem", "UNIVERSALITY_NOT_DERIVED"],
    },
    "1988_hilbert": {
        "path": ROOT / "1988-Y5-R2FR-action-weight-source-beta-theorem-or-finite-row-fill.md",
        "needles": ["THM1988_0_parent_form", "THEOREM_NOT_CLOSED_CURRENT_CORPUS"],
    },
    "1935_eta": {
        "path": ROOT / "1935-Y5-R2FR-MTS-WEP-eta-projection-map-or-material-charge-ledger.md",
        "needles": ["ETA1935_4_mts_source_weight_form", "CON1935_3_transfer_factor"],
    },
}

OUTPUTS = {
    "source_register": MTS_RESIDUALS / "P8_Y5_PARENT_QLOC_1990_SOURCE_REGISTER.csv",
    "tau_attempt": MTS_RESIDUALS / "P8_Y5_PARENT_QLOC_1990_TAU_LOWER_BOUND_THEOREM_ATTEMPT.csv",
    "no_go": MTS_RESIDUALS / "P8_Y5_PARENT_QLOC_1990_TAU_NONZERO_NO_GO_LEDGER.csv",
    "certificate": MTS_RESIDUALS / "P8_Y5_PARENT_QLOC_1990_NONDEGENERACY_CERTIFICATE_CONTRACT.csv",
    "u_envelope": MTS_RESIDUALS / "P8_Y5_PARENT_QLOC_1990_U_DENOMINATOR_ENVELOPE_CONTRACT.csv",
    "hilbert_route": MTS_RESIDUALS / "P8_Y5_PARENT_QLOC_1990_HILBERT_SOURCE_SIGNATURE_GATE.csv",
    "runner_dryrun": MTS_RESIDUALS / "P8_Y5_PARENT_QLOC_1990_RUNNER_DRYRUN.csv",
    "claim_gate": MTS_RESIDUALS / "P8_Y5_PARENT_QLOC_1990_CLAIM_GATE.csv",
    "decision": MTS_RESIDUALS / "P8_Y5_PARENT_QLOC_1990_DECISION_LEDGER.csv",
    "next": MTS_RESIDUALS / "P8_Y5_PARENT_QLOC_1990_NEXT_TARGET.csv",
    "source_weight": SOURCE_WEIGHT_DOCS / "TAU_WEP_LOWER_BOUND_OR_HILBERT_SIGNATURE_1990_NONCLAIM.csv",
    "wep_coeffs": MICROSCOPE_COEFFS / "P8_Y5_PARENT_QLOC_1990_TAU_NONDEGENERACY_CONTRACT_NONCLAIM.csv",
    "queue": RAB_QUEUE / "JR1990_TAU_NONDEGENERACY_OR_HILBERT_SIGNATURE_QUEUE.csv",
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
                "needed_for": "1990 tau_WEP lower-bound or Hilbert-source signature gate",
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

    tau_attempt = [
        row(
            {
                "attempt_id": "TAU1990_0_functional_shape",
                "statement": "tau_WEP is a dimensionless source-worldtube/orbit/readout/material functional, not a convention-free unity factor.",
                "formula": "tau_WEP = N_eta^{-1}<K_eta[e_obs,orbit,masks] · Integral_Earth K_source(x;orbit) R_source(x) dV · R_material(TiPt)>_orbit",
                "result": "SYMBOLIC_FUNCTIONAL_CONFIRMED",
                "claim_status": "NONCLAIM",
            }
        ),
        row(
            {
                "attempt_id": "TAU1990_1_upper_bound_easy",
                "statement": "norm data can give an upper envelope on |tau_WEP|",
                "formula": "|tau| <= |N_eta|^{-1} ||K_eta|| ||K_source R_source|| ||R_material||",
                "result": "UPPER_BOUND_SHAPE_ONLY",
                "claim_status": "NOT_ENOUGH_FOR_DELTAW_BOUND",
            }
        ),
        row(
            {
                "attempt_id": "TAU1990_2_lower_bound_hard",
                "statement": "a lower bound needs nonzero aligned projection, not merely nonzero ingredients",
                "formula": "|tau_WEP| >= tau_min>0 requires sign/alignment/coercivity or official arrays proving nonzero orbit-readout projection",
                "result": "LOWER_BOUND_NOT_DERIVED",
                "claim_status": "CURRENT_CORPUS_HAS_NO_TAU_MIN",
            }
        ),
        row(
            {
                "attempt_id": "TAU1990_3_current_verdict",
                "statement": "Does current MTS derive |P_WEP|>=P_min>0 or |tau_WEP|>=tau_min>0?",
                "formula": "P_WEP=tau_WEP*S_Earth; need |tau_WEP*S_Earth|>=P_min",
                "result": "FAIL_CURRENT_PROOF",
                "claim_status": "P_MIN_NOT_DERIVED_OR_SOURCED",
            }
        ),
    ]

    no_go = [
        row(
            {
                "no_go_id": "NG1990_0_orthogonality",
                "premise": "K_eta and source/material response are each nonzero",
                "counterexample": "choose K_eta orthogonal to the source/material response over the orbit average",
                "consequence": "tau_WEP=0 even though every named factor is nonzero",
                "lesson": "nonzero factors do not imply nonzero projected transfer",
            }
        ),
        row(
            {
                "no_go_id": "NG1990_1_mask_cancellation",
                "premise": "source response has positive and negative orbit segments or readout masks",
                "counterexample": "equal weighted positive/negative segments cancel in the reported eta channel",
                "consequence": "tau_WEP can vanish by averaging without a source-weight theorem",
                "lesson": "official readout/orbit convention is required for any lower bound",
            }
        ),
        row(
            {
                "no_go_id": "NG1990_2_common_mode",
                "premise": "source coupling is universal/common but not composition-differential",
                "counterexample": "common response enters SigmaW or measured calibration but not DeltaW_TiPt",
                "consequence": "P_WEP for the differential channel can be zero while common source response exists",
                "lesson": "measured-G/common-mode strength is not a WEP differential lower bound",
            }
        ),
        row(
            {
                "no_go_id": "NG1990_3_normalization",
                "premise": "symbolic tau functional exists",
                "counterexample": "without N_eta/product convention, rescale tau and DeltaW inversely",
                "consequence": "tau_min is convention-dependent unless normalization is fixed",
                "lesson": "tau_WEP=1 is a forbidden gauge choice, not a derivation",
            }
        ),
    ]

    certificate = [
        row(
            {
                "cert_id": "CERT1990_0_official_readout",
                "required_clause": "official or exactly equivalent MICROSCOPE readout/orbit kernel K_eta",
                "acceptance": "source path, units, masks, body order, sensitive-axis sign, and reproducible extraction",
                "current_status": "OFFICIAL_ARRAYS_NOT_IMPORTED",
                "if_missing": "no tau numeric value or tau_min",
            }
        ),
        row(
            {
                "cert_id": "CERT1990_1_source_worldtube",
                "required_clause": "Earth/source worldtube vector in same parent basis",
                "acceptance": "finite-size/source profile, orbit weighting, basis convention, and uncertainty/source path",
                "current_status": "MISSING_SOURCE_PROFILE_WEIGHTING",
                "if_missing": "source side of P_WEP is not evaluable",
            }
        ),
        row(
            {
                "cert_id": "CERT1990_2_material_tensor",
                "required_clause": "TA6V-minus-PtRh10 material response tensor in same basis",
                "acceptance": "composition/model/source path and no double-counting rule",
                "current_status": "MATERIAL_PAIR_ONLY_OR_PARTIAL_SMOKE",
                "if_missing": "DeltaW_TiPt cannot be linked to the readout product",
            }
        ),
        row(
            {
                "cert_id": "CERT1990_3_alignment_floor",
                "required_clause": "nonzero aligned projection certificate",
                "acceptance": "explicit positive floor I_min for the orbit/readout/source/material inner product, or theorem ruling out orthogonality",
                "current_status": "MISSING_ALIGNMENT_COERCIVITY",
                "if_missing": "tau_WEP may vanish by orthogonality/cancellation",
            }
        ),
        row(
            {
                "cert_id": "CERT1990_4_normalization_floor",
                "required_clause": "eta product normalization N_eta and bounded convention",
                "acceptance": "N_eta nonzero with source path and sign/units convention",
                "current_status": "NORMALIZATION_NOT_FILLED",
                "if_missing": "tau_min is convention-dependent",
            }
        ),
    ]

    u_envelope = [
        row(
            {
                "u_id": "U1990_0_definition",
                "quantity": "U=P_WEP*SigmaW_TiPt",
                "needed_for": "denominator control in eta=2D/(2+U)",
                "current_status": "SYMBOL_DEFINED_VALUES_MISSING",
                "required_input": "P_WEP envelope and SigmaW_TiPt envelope or theorem U=0",
            }
        ),
        row(
            {
                "u_id": "U1990_1_zero_route",
                "quantity": "U",
                "needed_for": "linear product bound with u_max=0",
                "current_status": "CONDITIONAL_ONLY",
                "required_input": "parent Hilbert source universality or common-mode cancellation theorem",
            }
        ),
        row(
            {
                "u_id": "U1990_2_finite_route",
                "quantity": "u_max",
                "needed_for": "|D| <= eta_bound_abs*(1+u_max/2)",
                "current_status": "MISSING_U_MAX",
                "required_input": "upper bounds for |P_WEP| and |SigmaW_TiPt| in same convention",
            }
        ),
    ]

    hilbert_route = [
        row(
            {
                "route_id": "HIL1990_0_strong_route",
                "target": "parent-signed universal Hilbert source coupling",
                "if_success": "DeltaW_TiPt=0 and beta_w=0, so WEP source-weight residual vanishes without tau_min",
                "current_status": "CONDITIONAL_THEOREM_EXACT_PARENT_UNSIGNED",
                "remaining_gap": "no-source-weight object-language clause, common measure/current owner, and readout preservation",
            }
        ),
        row(
            {
                "route_id": "HIL1990_1_finite_route",
                "target": "tau/P nondegeneracy and denominator finite envelopes",
                "if_success": "finite nonclaim WEP product comparison becomes scoreable",
                "current_status": "SOURCE_READOUT_NONDEGENERACY_MISSING",
                "remaining_gap": "official MICROSCOPE/readout/source/material/sign rows and alignment floor",
            }
        ),
    ]

    runner_dryrun = [
        row(
            {
                "run_id": "RUN1990_0_tau_functional",
                "check": "tau_WEP functional shape",
                "result": "PASS_SYMBOLIC",
                "reason": "1225 formula gives the source-worldtube/orbit/readout/material functional shape",
            }
        ),
        row(
            {
                "run_id": "RUN1990_1_tau_lower_bound",
                "check": "derive tau_min>0 from current corpus",
                "result": "FAIL_ORTHOGONALITY_COUNTEREXAMPLE",
                "reason": "nonzero factors can project to zero without an alignment/coercivity certificate",
            }
        ),
        row(
            {
                "run_id": "RUN1990_2_u_envelope",
                "check": "derive u_max for denominator control",
                "result": "FAIL_VALUES_MISSING",
                "reason": "P_WEP and SigmaW_TiPt envelopes are not sourced/derived",
            }
        ),
        row(
            {
                "run_id": "RUN1990_3_hilbert_signature",
                "check": "close DeltaW_TiPt=0 by parent Hilbert source signature",
                "result": "FAIL_PARENT_SIGNATURE_UNSIGNED",
                "reason": "conditional theorem exists but parent object language still permits countermodels unless signed",
            }
        ),
        row(
            {
                "run_id": "RUN1990_4_verdict",
                "check": "1990 tau/Hilbert fork",
                "result": "TAU_LOWER_BOUND_NOT_DERIVED_CERTIFICATE_CONTRACT_WRITTEN",
                "reason": "progress is the exact nondegeneracy certificate contract, not a WEP/local-GR score",
            }
        ),
    ]

    claim_gate = [
        row(
            {
                "gate_id": "CG1990_0_symbolic_tau",
                "claim": "tau_WEP functional shape is defined",
                "status": "PASS_NONCLAIM_SYMBOLIC",
                "reason": "functional shape is inherited from 1225 and kept nonclaim",
            }
        ),
        row(
            {
                "gate_id": "CG1990_1_tau_min",
                "claim": "|tau_WEP|>=tau_min>0",
                "status": "FAIL_BLOCKED",
                "reason": "no alignment/coercivity/readout certificate; orthogonality counterexample survives",
            }
        ),
        row(
            {
                "gate_id": "CG1990_2_P_min",
                "claim": "|P_WEP|>=P_min>0",
                "status": "FAIL_BLOCKED",
                "reason": "tau_min and source-environment floor missing",
            }
        ),
        row(
            {
                "gate_id": "CG1990_3_u_max",
                "claim": "denominator envelope u_max is known",
                "status": "FAIL_BLOCKED",
                "reason": "P_WEP and SigmaW_TiPt envelopes missing",
            }
        ),
        row(
            {
                "gate_id": "CG1990_4_hilbert_zero",
                "claim": "DeltaW_TiPt=0 parent-signed",
                "status": "FAIL_BLOCKED",
                "reason": "Hilbert source route remains conditional",
            }
        ),
        row(
            {
                "gate_id": "CG1990_5_local_GR_Newton",
                "claim": "local GR/Newton source universality derived",
                "status": "FAIL_BLOCKED",
                "reason": "neither tau finite route nor Hilbert zero route is closed",
            }
        ),
    ]

    decision = [
        row(
            {
                "decision_id": "DEC1990_0_tau_result",
                "decision": "TAU_MIN_NOT_DERIVED",
                "because": "tau_WEP is an inner-product/readout functional; current corpus lacks the alignment certificate needed to rule out zero projection",
                "next_action": "build nondegeneracy certificate or source official readout arrays",
            }
        ),
        row(
            {
                "decision_id": "DEC1990_1_hilbert_status",
                "decision": "HILBERT_ZERO_ROUTE_REMAINS_BEST_CLEAN_GR_ROUTE",
                "because": "if universal Hilbert source coupling is parent-signed, DeltaW_TiPt=0 and tau_min becomes unnecessary for WEP zero",
                "next_action": "try to close source-signature/readout-preservation theorem in parallel with finite data route",
            }
        ),
        row(
            {
                "decision_id": "DEC1990_2_best_next",
                "decision": "NONDEGENERACY_CERTIFICATE_OR_HILBERT_OWNER_NEXT",
                "because": "the finite route needs official readout/source/material alignment; the derivation route needs no-source-weight parent ownership",
                "next_action": "1991-Y5-R2FR-WEP-nondegeneracy-certificate-or-parent-Hilbert-owner.md",
            }
        ),
    ]

    next_target = [
        row(
            {
                "next_id": "NEXT1990_0_primary",
                "selection_status": "selected",
                "target_doc": "1991-Y5-R2FR-WEP-nondegeneracy-certificate-or-parent-Hilbert-owner.md",
                "target_script": "scripts/Y5_R2FR_WEP_nondegeneracy_certificate_or_parent_Hilbert_owner_1991.py",
                "task": "either construct a nonzero WEP projection certificate from readout/source/material alignment, or close the parent Hilbert source owner/no-species-weight theorem",
                "success_condition": "tau/P lower-bound certificate with source paths, or parent-signed DeltaW_TiPt=0; otherwise retain finite nonclaim route",
                "do_not": "do not set tau_WEP=1, use nonzero factors as nonzero projection, assume U=0, invent material/source rows, claim WEP/local-GR pass, or modify formalization-workbench",
            }
        )
    ]

    source_weight = [
        row(
            {
                "artifact_id": "SW1990_0_tau_lower_bound_record",
                "artifact_type": "tau_lower_bound_no_go_and_certificate_contract",
                "status": "NONCLAIM_TAU_MIN_NOT_DERIVED",
                "source_path": str(DOC_PATH),
                "next_target": "1991-Y5-R2FR-WEP-nondegeneracy-certificate-or-parent-Hilbert-owner.md",
            }
        )
    ]

    wep_coeffs = [
        row(
            {
                "coefficient_id": "WEP1990_0_tau_min_certificate_slot",
                "quantity": "tau_min or P_min",
                "required_formula": "|tau_WEP|>=tau_min>0; |P_WEP|>=P_min>0",
                "required_evidence": "official readout/source/material alignment floor or parent theorem",
                "current_status": "MISSING_NONDEGENERACY_CERTIFICATE",
                "status": "NONCLAIM_SLOT_ONLY",
            }
        )
    ]

    queue = [
        row(
            {
                "queue_id": "JR1990_0_nondegeneracy_certificate",
                "priority": "1",
                "needed_input": "WEP projection nondegeneracy certificate",
                "route": "official MICROSCOPE readout/source/material/sign rows or parent Hilbert owner theorem",
                "required_fields": "K_eta;R_source;R_material;N_eta;orbit_masks;body_order;sign;basis;I_min_or_zero_theorem;source_path",
                "blocked_claims": "tau_min;P_min;DeltaW bound;WEP pass;local_GR;Newton",
            }
        )
    ]

    return {
        "source_register": source_register(stamp),
        "tau_attempt": tau_attempt,
        "no_go": no_go,
        "certificate": certificate,
        "u_envelope": u_envelope,
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
    val("VAL1990_00_sources", "PASS" if not source_failures else "FAIL", "all source paths exist and needles found" if not source_failures else ";".join(row["source_id"] for row in source_failures))

    symbolic_tau = any(row["result"] == "SYMBOLIC_FUNCTIONAL_CONFIRMED" for row in tables["tau_attempt"])
    lower_fail = any(row["result"] == "LOWER_BOUND_NOT_DERIVED" for row in tables["tau_attempt"])
    val("VAL1990_01_tau_attempt", "PASS" if symbolic_tau and lower_fail else "FAIL", "tau functional retained; lower bound not promoted")

    no_go_ok = any(row["no_go_id"] == "NG1990_0_orthogonality" for row in tables["no_go"])
    val("VAL1990_02_no_go", "PASS" if no_go_ok else "FAIL", "orthogonality/cancellation no-go recorded")

    cert_ok = any(row["cert_id"] == "CERT1990_3_alignment_floor" and row["current_status"] == "MISSING_ALIGNMENT_COERCIVITY" for row in tables["certificate"])
    val("VAL1990_03_certificate_contract", "PASS" if cert_ok else "FAIL", "alignment/coercivity certificate required")

    u_ok = any(row["u_id"] == "U1990_2_finite_route" and row["current_status"] == "MISSING_U_MAX" for row in tables["u_envelope"])
    val("VAL1990_04_u_envelope", "PASS" if u_ok else "FAIL", "U denominator envelope remains explicit and missing")

    runner_blocks = tables["runner_dryrun"][1]["result"] == "FAIL_ORTHOGONALITY_COUNTEREXAMPLE" and tables["runner_dryrun"][3]["result"] == "FAIL_PARENT_SIGNATURE_UNSIGNED"
    val("VAL1990_05_runner_blocks", "PASS" if runner_blocks else "FAIL", "runner blocks tau-min and Hilbert-zero claims")

    gates_safe = all(row["status"] in {"PASS_NONCLAIM_SYMBOLIC", "FAIL_BLOCKED"} for row in tables["claim_gate"])
    val("VAL1990_06_claim_gates", "PASS" if gates_safe else "FAIL", "claim gates safe; symbolic tau only")

    next_ok = tables["next"][0]["target_doc"] == "1991-Y5-R2FR-WEP-nondegeneracy-certificate-or-parent-Hilbert-owner.md"
    val("VAL1990_07_next_target", "PASS" if next_ok else "FAIL", "1991 nondegeneracy/Hilbert owner target selected")

    all_rows = [row for rows_for_table in tables.values() for row in rows_for_table]
    flags_safe = all(row.get("valid_for_claim") == "false" and row.get("claim_allowed") == "false" for row in all_rows)
    val("VAL1990_08_claim_flags_safe", "PASS" if flags_safe else "FAIL", "claim flags all false")

    parse_failures = []
    for output_name, path in OUTPUTS.items():
        if not path.exists():
            parse_failures.append(f"{output_name}:missing")
            continue
        with path.open(newline="", encoding="utf-8") as handle:
            parsed = list(csv.DictReader(handle))
        if not parsed:
            parse_failures.append(f"{output_name}:empty")
    val("VAL1990_09_csv_parse", "PASS" if not parse_failures else "FAIL", "all generated CSVs parse with rows" if not parse_failures else ";".join(parse_failures))

    pycache_exists = (ROOT / "scripts" / "__pycache__").exists()
    val("VAL1990_10_pycache_absent", "PASS" if not pycache_exists else "FAIL", "scripts __pycache__ absent")

    formalization_artifacts = []
    if FORMALIZATION.exists():
        formalization_artifacts = [path for path in FORMALIZATION.rglob("*1990*")]
    val("VAL1990_11_formalization_untouched", "PASS" if not formalization_artifacts else "FAIL", f"formalization_1990_artifact_count={len(formalization_artifacts)}")

    overall = "PASS" if all(row["status"] == "PASS" for row in rows) else "FAIL"
    val("VAL1990_OVERALL", overall, "1990 tau WEP lower-bound or Hilbert source signature gate")
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
        ("Tau Lower-Bound Theorem Attempt", tables["tau_attempt"]),
        ("Tau Nonzero No-Go Ledger", tables["no_go"]),
        ("Nondegeneracy Certificate Contract", tables["certificate"]),
        ("U Denominator Envelope Contract", tables["u_envelope"]),
        ("Hilbert Source Signature Gate", tables["hilbert_route"]),
        ("Runner Dryrun", tables["runner_dryrun"]),
        ("Claim Gate", tables["claim_gate"]),
        ("Decision Ledger", tables["decision"]),
        ("Next Target", tables["next"]),
        ("Validation", validation_rows),
    ]
    lines = [
        "# 1990 Y5 R2FR: Tau WEP Lower Bound Or Hilbert Source Signature",
        "",
        "Private checkpoint. This tries the 1989 fork honestly: can `tau_WEP` or `P_WEP` be bounded away from zero, or must the branch lean harder on the parent Hilbert-source zero theorem?",
        "",
        "Verdict: the symbolic `tau_WEP` functional is retained, but no lower bound is derived. The obstruction is mathematical, not cosmetic: `tau_WEP` is an orbit/readout/source/material inner product, and such a projection can vanish by orthogonality or mask cancellation even when every named factor is nonzero.",
        "",
        "Therefore the finite WEP route needs a real nondegeneracy certificate: official/readout-equivalent `K_eta`, Earth/source worldtube, Ti/Pt material tensor, product normalization, sign convention, and an alignment floor. The clean GR/Newton route remains the parent Hilbert-source theorem: if ordinary matter has one universal Hilbert source and no species/source-weight slot, then `DeltaW_TiPt=0` and tau lower bounds are unnecessary for the WEP zero.",
        "",
        "No WEP, local-GR, Newton, R10, PPN, clock, orbital, or public claim follows from 1990.",
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
    print(f"VAL1990_OVERALL={overall}")
    return 0 if overall == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())

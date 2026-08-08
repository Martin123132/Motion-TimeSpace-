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

DOC_PATH = ROOT / "1996-Y5-R2FR-parent-action-scale-normalization-or-WEP-tau-projection.md"
VALIDATION_PATH = MTS_RESIDUALS / "P8_Y5_BRR545_1996_VALIDATION.csv"

SOURCES = {
    "1995_doc": {
        "path": ROOT / "1995-Y5-R2FR-matter-interface-label-forgetting-or-first-material-charge-source.md",
        "needles": ["MIB1995_1_action_scale_owner", "NEXT1995_0_primary"],
    },
    "1995_validation": {
        "path": MTS_RESIDUALS / "P8_Y5_BRR545_1995_VALIDATION.csv",
        "needles": ["VAL1995_OVERALL", "PASS"],
    },
    "1067_action_scale": {
        "path": ROOT / "1067-Y5-R10-parent-quantum-action-scale-normalization-or-WEP-tau-projection.md",
        "needles": ["ASO1067_5_verdict", "TWF1067_6_verdict"],
    },
    "1067_validation": {
        "path": MTS_RESIDUALS / "P8_Y5_BRR545_1067_VALIDATION.csv",
        "needles": ["V1067_SUMMARY", "pass"],
    },
    "1068_tau_pack": {
        "path": ROOT / "1068-Y5-R10-WEP-tau-source-worldtube-orbit-readout-acquisition-pack.md",
        "needles": ["TAP1068_0_source_worldtube", "DEC1068_2_best_next"],
    },
    "1068_validation": {
        "path": MTS_RESIDUALS / "P8_Y5_BRR545_1068_VALIDATION.csv",
        "needles": ["V1068_SUMMARY", "pass"],
    },
    "1066_source_scalar": {
        "path": ROOT / "1066-Y5-R10-parent-action-syntax-source-scalar-exclusion-or-WEP-Delta-w-prior-width.md",
        "needles": ["SSE1066_5_verdict", "DWP1066_5_product"],
    },
}

OUTPUTS = {
    "source_register": MTS_RESIDUALS / "P8_Y5_PARENT_QLOC_1996_SOURCE_REGISTER.csv",
    "action_scale": MTS_RESIDUALS / "P8_Y5_PARENT_QLOC_1996_ACTION_SCALE_NORMALIZATION_THEOREM.csv",
    "obstruction": MTS_RESIDUALS / "P8_Y5_PARENT_QLOC_1996_ACTION_SCALE_OBSTRUCTION_AUDIT.csv",
    "tau_pack": MTS_RESIDUALS / "P8_Y5_PARENT_QLOC_1996_TAU_WEP_PROJECTION_PACK.csv",
    "direct_product": MTS_RESIDUALS / "P8_Y5_PARENT_QLOC_1996_DIRECT_WEP_PRODUCT_ROUTE.csv",
    "runner_dryrun": MTS_RESIDUALS / "P8_Y5_PARENT_QLOC_1996_RUNNER_DRYRUN.csv",
    "claim_gate": MTS_RESIDUALS / "P8_Y5_PARENT_QLOC_1996_CLAIM_GATE.csv",
    "decision": MTS_RESIDUALS / "P8_Y5_PARENT_QLOC_1996_DECISION_LEDGER.csv",
    "next": MTS_RESIDUALS / "P8_Y5_PARENT_QLOC_1996_NEXT_TARGET.csv",
    "source_weight": SOURCE_WEIGHT_DOCS / "ACTION_SCALE_NORMALIZATION_1996_NONCLAIM.csv",
    "wep_coeffs": MICROSCOPE_COEFFS / "P8_Y5_PARENT_QLOC_1996_TAU_WEP_PROJECTION_PACK_NONCLAIM.csv",
    "queue": RAB_QUEUE / "JR1996_DIRECT_WEP_PRODUCT_OR_REAL_TAU_QUEUE.csv",
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
                "needed_for": "1996 parent action-scale normalization or WEP tau projection",
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

    action_scale = [
        row(
            {
                "theorem_id": "ASN1996_0_statement",
                "statement": "If the parent theory owns one species-blind action quantum/measure normalization for all ordinary matter, then species-dependent source-only multipliers w_A S_A are inadmissible or quotient-equivalent to a common calibration.",
                "formal_condition": "S_parent/hbar_parent uses sum_A S_A with one hbar_parent, one measure class, one public coframe measure, and no species-indexed action-scale slot",
                "consequence": "Delta_w_AB=0 for ordinary source-only relative weights; the clean C_EP_direct source-weight channel vanishes",
                "status": "EXACT_CONDITIONAL_THEOREM",
            }
        ),
        row(
            {
                "theorem_id": "ASN1996_1_hilbert_source_effect",
                "statement": "A species multiplier is not harmless unless the parent measure quotients it, because Hilbert stress varies with the coefficient.",
                "formal_condition": "delta(w_A S_A)/delta e_pub = w_A T_A unless w_A is absent, common, or gauge-quotiented before variation",
                "consequence": "classical EOM similarity does not prove source universality",
                "status": "EXACT_OBSTRUCTION_IDENTITY",
            }
        ),
        row(
            {
                "theorem_id": "ASN1996_2_measure_owner",
                "statement": "Path-integral/statistical/action-scale ownership must be common, otherwise w_A can reappear as a species-dependent phase/measure weight.",
                "formal_condition": "Dmu_parent and hbar_parent have no source-only species component or Jacobian spurion",
                "consequence": "no hidden source-weight return through quantum/statistical normalization",
                "status": "MISSING_PARENT_MEASURE_OWNER",
            }
        ),
        row(
            {
                "theorem_id": "ASN1996_3_current_verdict",
                "statement": "Can 1996 promote Delta_w_TiPt=0 from action-scale normalization?",
                "formal_condition": "ASN1996_0 through ASN1996_2 parent-signed plus current owner/readout descent",
                "consequence": "would close the relative source-weight route toward C_EP_direct=0",
                "status": "NOT_PARENT_SIGNED_DO_NOT_PROMOTE",
            }
        ),
    ]

    obstruction = [
        row(
            {
                "audit_id": "ASO1996_0_classical_EOM_trap",
                "obstruction": "w_A can leave isolated Euler-Lagrange equations looking scaled while changing Hilbert source and action weight",
                "needed_to_close": "prove w_A is quotient/gauge redundancy before variation, not just dynamically invisible after equations of motion",
                "status": "ACTIVE_OBSTRUCTION",
            }
        ),
        row(
            {
                "audit_id": "ASO1996_1_field_rescaling_limit",
                "obstruction": "field normalization can remove one factor only if interactions, charges, composite parameters, source, readout, and measure transform with no residual source-only scalar",
                "needed_to_close": "parent field-redefinition quotient plus measured-coupling/current owner",
                "status": "ACTIVE_OBSTRUCTION",
            }
        ),
        row(
            {
                "audit_id": "ASO1996_2_measure_jacobian",
                "obstruction": "species-dependent measure/coframe/boundary Jacobian can mimic w_A even when explicit w_A is absent",
                "needed_to_close": "species-blind measure/coframe descent and no hidden spurion return",
                "status": "ACTIVE_OBSTRUCTION",
            }
        ),
        row(
            {
                "audit_id": "ASO1996_3_current_status",
                "obstruction": "current corpus does not yet derive hbar/action-measure owner",
                "needed_to_close": "parent primitive or quotient rule that removes action-scale species labels",
                "status": "BLOCKS_THEOREM_ZERO",
            }
        ),
    ]

    tau_pack = [
        row(
            {
                "pack_id": "TAU1996_0_source_worldtube",
                "component": "Earth/source worldtube",
                "required_for": "source leg of tau_WEP or direct P_WEP product",
                "accepted_form": "source stress/profile/composition convention in observed local frame, or theorem-reduced point-source convention with error bound",
                "current_status": "MISSING_SOURCE_WORLDTUBE",
            }
        ),
        row(
            {
                "pack_id": "TAU1996_1_orbit_readout_kernel",
                "component": "MICROSCOPE orbit/readout kernel",
                "required_for": "projection from source residual to measured eta_AB channel",
                "accepted_form": "orbit/attitude/time averaging kernel and eta readout convention with source path",
                "current_status": "MISSING_ORBIT_READOUT_KERNEL",
            }
        ),
        row(
            {
                "pack_id": "TAU1996_2_material_tensor",
                "component": "Ti/Pt material response tensor",
                "required_for": "test-body leg of relative source-weight or material-charge response",
                "accepted_form": "full material/source response tensor or parent theorem reducing response to Delta_w_TiPt",
                "current_status": "MISSING_FULL_MATERIAL_TENSOR",
            }
        ),
        row(
            {
                "pack_id": "TAU1996_3_force_map",
                "component": "observed-frame force/readout map",
                "required_for": "same-frame acceleration residual and eta_AB comparison",
                "accepted_form": "force law in e_obs with units, calibration, no measured-G relative absorption",
                "current_status": "MISSING_FORCE_READOUT_MAP",
            }
        ),
        row(
            {
                "pack_id": "TAU1996_4_Xhat_normalization",
                "component": "Xhat/chi_X normalization",
                "required_for": "compatibility across WEP, R10, clocks, and finite branch coefficients",
                "accepted_form": "shared parent normalization or explicit branch separation convention",
                "current_status": "MISSING_XHAT_NORMALIZATION",
            }
        ),
    ]

    direct_product = [
        row(
            {
                "route_id": "DWP1996_0_preferred_direct_theorem",
                "route": "derive P_WEP_relative_source_weight directly from parent variation into eta_AB",
                "why_preferred": "avoids arbitrary split into Delta_w_TiPt and tau_WEP",
                "required_evidence": "parent variation, source/readout map, material response, units, source path or theorem-zero",
                "status": "MISSING_DIRECT_PARENT_PRODUCT",
            }
        ),
        row(
            {
                "route_id": "DWP1996_1_split_route",
                "route": "P_WEP = abs(Delta_w_TiPt*tau_WEP)",
                "why_preferred": "usable finite branch if direct theorem fails",
                "required_evidence": "numeric or theorem-zero Delta_w_TiPt and numeric/theorem-zero tau_WEP, no unity shortcut",
                "status": "MISSING_BOTH_FACTORS",
            }
        ),
        row(
            {
                "route_id": "DWP1996_2_zero_route",
                "route": "P_WEP=0",
                "why_preferred": "cleanest local-GR-safe source branch",
                "required_evidence": "parent action-scale/source-scalar theorem or WEP projection silence theorem",
                "status": "THEOREM_ZERO_UNSIGNED",
            }
        ),
        row(
            {
                "route_id": "DWP1996_3_refusal",
                "route": "reject fake products",
                "why_preferred": "keeps the branch testable rather than decorative",
                "required_evidence": "no tau=1, no Delta_w=0 by convention, no measured-G absorption, no cancellation argument",
                "status": "REFUSAL_ACTIVE",
            }
        ),
    ]

    runner_dryrun = [
        row(
            {
                "run_id": "RUN1996_0_action_scale",
                "check": "derive species-blind parent action-scale normalization",
                "result": "FAIL_PARENT_OWNER_MISSING",
                "reason": "1067 and current audit retain hbar/action-measure/current/readout owner gaps",
            }
        ),
        row(
            {
                "run_id": "RUN1996_1_Delta_w_zero",
                "check": "claim Delta_w_TiPt=0",
                "result": "FAIL_THEOREM_ZERO_UNSIGNED",
                "reason": "action-scale theorem is exact but conditional",
            }
        ),
        row(
            {
                "run_id": "RUN1996_2_tau_pack",
                "check": "construct scoreable tau_WEP",
                "result": "FAIL_PACK_COMPONENTS_MISSING",
                "reason": "source worldtube, orbit/readout, material tensor, force map, and Xhat normalization are missing",
            }
        ),
        row(
            {
                "run_id": "RUN1996_3_direct_product",
                "check": "derive direct P_WEP product",
                "result": "FAIL_NOT_DERIVED",
                "reason": "parent variation has not yet produced eta_AB residual directly",
            }
        ),
        row(
            {
                "run_id": "RUN1996_4_verdict",
                "check": "1996 next-step decision",
                "result": "NEXT_1997_DIRECT_WEP_PRODUCT_THEOREM_OR_FIRST_REAL_TAU_SOURCE_ROW",
                "reason": "if action-scale owner is not immediately signed, direct P_WEP or first tau source row is the honest finite branch",
            }
        ),
    ]

    claim_gate = [
        row(
            {
                "gate_id": "CG1996_0_action_scale_contract",
                "claim": "action-scale theorem exists as a conditional contract",
                "status": "PASS_NONCLAIM_CONTRACT",
                "reason": "one parent action/measure owner would remove w_A",
            }
        ),
        row(
            {
                "gate_id": "CG1996_1_action_scale_derived",
                "claim": "action-scale owner is parent-derived",
                "status": "FAIL_BLOCKED",
                "reason": "hbar/action-measure/current/readout ownership is missing",
            }
        ),
        row(
            {
                "gate_id": "CG1996_2_Delta_w_zero",
                "claim": "Delta_w_TiPt=0",
                "status": "FAIL_BLOCKED",
                "reason": "theorem-zero route remains unsigned",
            }
        ),
        row(
            {
                "gate_id": "CG1996_3_tau_WEP",
                "claim": "tau_WEP is numeric or theorem-zero",
                "status": "FAIL_BLOCKED",
                "reason": "tau pack components are missing",
            }
        ),
        row(
            {
                "gate_id": "CG1996_4_local_GR_Newton",
                "claim": "local GR/Newton source coupling is derived",
                "status": "FAIL_BLOCKED",
                "reason": "source-side product/projection and C_EP/C_corr gates remain open",
            }
        ),
    ]

    decision = [
        row(
            {
                "decision_id": "DEC1996_0_theory_status",
                "decision": "ACTION_SCALE_OWNER_IS_THE_CLEAN_THEOREM_PATH_BUT_NOT_SIGNED",
                "because": "species action-scale factors alter Hilbert source and measure unless one parent owner forbids or quotients them",
                "next_action": "do not use Delta_w=0 until hbar/action-measure owner is derived",
            }
        ),
        row(
            {
                "decision_id": "DEC1996_1_finite_status",
                "decision": "TAU_WEP_PACK_IS_EXPLICIT_BUT EMPTY",
                "because": "1068 names the source worldtube, orbit/readout, material tensor, force map, and Xhat normalization gaps",
                "next_action": "derive direct P_WEP product or acquire the first real tau source row",
            }
        ),
        row(
            {
                "decision_id": "DEC1996_2_best_next",
                "decision": "DIRECT_WEP_PRODUCT_THEOREM_BEFORE_DATA_FILL",
                "because": "a direct eta_AB product avoids arbitrary split-factor priors; if it fails, source tau rows one by one",
                "next_action": "1997-Y5-R2FR-direct-WEP-product-theorem-or-first-real-tau-source-row.md",
            }
        ),
    ]

    next_target = [
        row(
            {
                "next_id": "NEXT1996_0_primary",
                "selection_status": "selected",
                "target_doc": "1997-Y5-R2FR-direct-WEP-product-theorem-or-first-real-tau-source-row.md",
                "target_script": "scripts/Y5_R2FR_direct_WEP_product_theorem_or_first_real_tau_source_row_1997.py",
                "task": "derive a direct parent variation theorem for P_WEP_relative_source_weight, or acquire the first real tau_WEP component row with source path and units",
                "success_condition": "direct eta_AB product theorem-zero/numeric row, or first real tau source-worldtube/orbit/readout/material row while keeping WEP/local-GR nonclaim",
                "do_not": "do not set tau_WEP=1, set Delta_w=0 by convention, absorb relative weights into measured G, use cancellation arguments, push GitHub, or edit formalization-workbench",
            }
        )
    ]

    source_weight = [
        row(
            {
                "artifact_id": "SW1996_0_action_scale_contract",
                "artifact_type": "action_scale_normalization_or_tau_projection_nonclaim",
                "status": "ACTION_SCALE_UNSIGNED_TAU_PACK_MISSING",
                "source_path": str(DOC_PATH),
                "next_target": "1997-Y5-R2FR-direct-WEP-product-theorem-or-first-real-tau-source-row.md",
            }
        )
    ]

    wep_coeffs = [
        row(
            {
                "coefficient_id": "WEP1996_0_tau_pack_contract",
                "quantity": "P_WEP_relative_source_weight or Delta_w_TiPt*tau_WEP",
                "required_formula": "P_WEP direct parent product, or abs(Delta_w_TiPt*tau_WEP)",
                "required_evidence": "direct parent variation; or Delta_w theorem/value plus tau source worldtube, orbit/readout, material tensor, force map, Xhat normalization",
                "current_status": "MISSING_DIRECT_PRODUCT_AND_MISSING_TAU_PACK",
                "status": "NONCLAIM_REQUIREMENTS_ONLY",
            }
        )
    ]

    queue = [
        row(
            {
                "queue_id": "JR1996_0_direct_wep_or_tau",
                "priority": "1",
                "needed_input": "direct WEP product theorem or first real tau source row",
                "route": "try parent variation into eta_AB first; if not, acquire/source tau_WEP pack components beginning with eta/readout convention or Earth source worldtube",
                "required_fields": "P_WEP_formula;source_worldtube;orbit_kernel;eta_readout;material_tensor;force_map;Xhat_normalization;source_path;units",
                "blocked_claims": "WEP_product_score;Delta_w_zero;C_EP_zero;local_GR;Newton",
            }
        )
    ]

    return {
        "source_register": source_register(stamp),
        "action_scale": action_scale,
        "obstruction": obstruction,
        "tau_pack": tau_pack,
        "direct_product": direct_product,
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
    val("VAL1996_00_sources", "PASS" if not source_failures else "FAIL", "all source paths exist and needles found" if not source_failures else ";".join(row["source_id"] for row in source_failures))

    theorem_ready = any(row["theorem_id"] == "ASN1996_0_statement" and row["status"] == "EXACT_CONDITIONAL_THEOREM" for row in tables["action_scale"])
    theorem_blocked = any(row["theorem_id"] == "ASN1996_3_current_verdict" and row["status"] == "NOT_PARENT_SIGNED_DO_NOT_PROMOTE" for row in tables["action_scale"])
    val("VAL1996_01_action_scale", "PASS" if theorem_ready and theorem_blocked else "FAIL", "action-scale theorem exact but not promoted")

    obstructions_active = all(row["status"] in {"ACTIVE_OBSTRUCTION", "BLOCKS_THEOREM_ZERO"} for row in tables["obstruction"])
    val("VAL1996_02_obstructions", "PASS" if obstructions_active else "FAIL", "action-scale obstructions retained")

    tau_missing = all(row["current_status"].startswith("MISSING") for row in tables["tau_pack"])
    val("VAL1996_03_tau_pack", "PASS" if tau_missing else "FAIL", "tau_WEP pack components remain explicitly missing")

    direct_blocked = all(row["status"] in {"MISSING_DIRECT_PARENT_PRODUCT", "MISSING_BOTH_FACTORS", "THEOREM_ZERO_UNSIGNED", "REFUSAL_ACTIVE"} for row in tables["direct_product"])
    val("VAL1996_04_direct_product", "PASS" if direct_blocked else "FAIL", "direct/split/zero WEP product routes are blocked or guarded")

    runner_selects = tables["runner_dryrun"][-1]["result"] == "NEXT_1997_DIRECT_WEP_PRODUCT_THEOREM_OR_FIRST_REAL_TAU_SOURCE_ROW"
    val("VAL1996_05_runner_decision", "PASS" if runner_selects else "FAIL", "runner selects direct WEP/tau source target")

    gates_safe = all(row["status"] in {"FAIL_BLOCKED", "PASS_NONCLAIM_CONTRACT"} for row in tables["claim_gate"])
    no_physics_claim = all(row["status"] == "FAIL_BLOCKED" for row in tables["claim_gate"] if row["gate_id"] != "CG1996_0_action_scale_contract")
    val("VAL1996_06_claim_gates", "PASS" if gates_safe and no_physics_claim else "FAIL", "only conditional contract passes; physics claims blocked")

    next_ok = tables["next"][0]["target_doc"] == "1997-Y5-R2FR-direct-WEP-product-theorem-or-first-real-tau-source-row.md"
    val("VAL1996_07_next_target", "PASS" if next_ok else "FAIL", "1997 direct WEP/tau target selected")

    all_rows = [row for rows_for_table in tables.values() for row in rows_for_table]
    flags_safe = all(row.get("valid_for_claim") == "false" and row.get("claim_allowed") == "false" for row in all_rows)
    val("VAL1996_08_claim_flags_safe", "PASS" if flags_safe else "FAIL", "claim flags all false")

    parse_failures = []
    for output_name, path in OUTPUTS.items():
        if not path.exists():
            parse_failures.append(f"{output_name}:missing")
            continue
        with path.open(newline="", encoding="utf-8") as handle:
            parsed = list(csv.DictReader(handle))
        if not parsed:
            parse_failures.append(f"{output_name}:empty")
    val("VAL1996_09_csv_parse", "PASS" if not parse_failures else "FAIL", "all generated CSVs parse with rows" if not parse_failures else ";".join(parse_failures))

    pycache_exists = (ROOT / "scripts" / "__pycache__").exists()
    val("VAL1996_10_pycache_absent", "PASS" if not pycache_exists else "FAIL", "scripts __pycache__ absent")

    formalization_artifacts = []
    checkpoint_markers = ("Y5_R2FR", "P8_Y5", "JR1996", "ASN1996", "TAU1996", "WEP")
    if FORMALIZATION.exists():
        formalization_artifacts = [
            path
            for path in FORMALIZATION.rglob("*")
            if "1996" in path.name and any(marker in path.name for marker in checkpoint_markers)
        ]
    val("VAL1996_11_formalization_untouched", "PASS" if not formalization_artifacts else "FAIL", f"formalization_1996_artifact_count={len(formalization_artifacts)}")

    overall = "PASS" if all(row["status"] == "PASS" for row in rows) else "FAIL"
    val("VAL1996_OVERALL", overall, "1996 parent action-scale normalization or WEP tau projection")
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
        cells = [str(row.get(header, "")).replace("\n", " ").replace("|", "\\|") for header in headers]
        lines.append("| " + " | ".join(cells) + " |")
    return "\n".join(lines)


def write_markdown(tables: dict[str, list[dict[str, str]]], validation_rows: list[dict[str, str]]) -> None:
    sections = [
        ("Source Register", tables["source_register"]),
        ("Action-Scale Normalization Theorem", tables["action_scale"]),
        ("Action-Scale Obstruction Audit", tables["obstruction"]),
        ("tau_WEP Projection Pack", tables["tau_pack"]),
        ("Direct WEP Product Route", tables["direct_product"]),
        ("Runner Dryrun", tables["runner_dryrun"]),
        ("Claim Gate", tables["claim_gate"]),
        ("Decision Ledger", tables["decision"]),
        ("Next Target", tables["next"]),
        ("Validation", validation_rows),
    ]
    lines = [
        "# 1996 Y5 R2FR: Parent Action-Scale Normalization Or WEP tau Projection",
        "",
        "Private checkpoint. This imports the 1067/1068 action-scale and tau work into the current `C_EP`/local-GR branch.",
        "",
        "Verdict: the action-scale theorem is exact but conditional. If the parent owns one species-blind action quantum/measure normalization, then inert source-only `w_A S_A` terms are absent or common-calibration only, so `Delta_w_TiPt=0` and the cleanest `C_EP_direct` source-weight channel vanishes. Current corpus does not yet sign that owner.",
        "",
        "Finite branch: `tau_WEP` is not a number. It is a projection pack needing source worldtube, orbit/readout kernel, Ti/Pt material tensor, observed-frame force map, and `Xhat` normalization. Setting `tau_WEP=1` remains forbidden.",
        "",
        "Next honest move: try a direct parent variation theorem for `P_WEP_relative_source_weight`; if that fails, acquire the first real tau component row.",
        "",
        "No WEP, local-GR, Newton, R10, PPN, clock, orbital, or public claim follows from 1996.",
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
    print(f"VAL1996_OVERALL={overall}")
    return 0 if overall == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())

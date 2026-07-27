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

DOC_PATH = ROOT / "1995-Y5-R2FR-matter-interface-label-forgetting-or-first-material-charge-source.md"
VALIDATION_PATH = MTS_RESIDUALS / "P8_Y5_BRR545_1995_VALIDATION.csv"

SOURCES = {
    "1994_doc": {
        "path": ROOT / "1994-Y5-R2FR-parent-charge-basis-exclusion-or-material-charge-row.md",
        "needles": ["PFA1994_2_label_forgetting", "NEXT1994_0_primary"],
    },
    "1994_validation": {
        "path": MTS_RESIDUALS / "P8_Y5_BRR545_1994_VALIDATION.csv",
        "needles": ["VAL1994_OVERALL", "PASS"],
    },
    "1063_source_forgetting": {
        "path": ROOT / "1063-Y5-R10-source-label-forgetting-Noether-current-owner-or-relative-weight-prior.md",
        "needles": ["THM1063_5_verdict", "DEC1063_2_best_next"],
    },
    "1064_category_label": {
        "path": ROOT / "1064-Y5-R10-parent-category-label-forgetting-proof-or-relative-weight-runner-fill.md",
        "needles": ["PLF1064_5_verdict", "DEC1064_2_best_next"],
    },
    "1065_no_source_slot": {
        "path": ROOT / "1065-Y5-R10-no-source-only-slot-parent-grammar-or-first-relative-weight-numeric-row.md",
        "needles": ["PGG1065_5_verdict", "DEC1065_2_best_next"],
    },
    "1066_source_scalar": {
        "path": ROOT / "1066-Y5-R10-parent-action-syntax-source-scalar-exclusion-or-WEP-Delta-w-prior-width.md",
        "needles": ["SSE1066_5_verdict", "DEC1066_2_best_next"],
    },
    "1055_parent_contract": {
        "path": ROOT / "1055-Y5-R10-alpha-owner-and-matter-functor-parent-action-contract.md",
        "needles": ["PAC1055_4_source_label_forgetting", "DEC1055_1_not_derivation_yet"],
    },
}

OUTPUTS = {
    "source_register": MTS_RESIDUALS / "P8_Y5_PARENT_QLOC_1995_SOURCE_REGISTER.csv",
    "label_chain": MTS_RESIDUALS / "P8_Y5_PARENT_QLOC_1995_LABEL_FORGETTING_CHAIN_IMPORT.csv",
    "theorem_bridge": MTS_RESIDUALS / "P8_Y5_PARENT_QLOC_1995_MATTER_INTERFACE_THEOREM_BRIDGE.csv",
    "blocker": MTS_RESIDUALS / "P8_Y5_PARENT_QLOC_1995_ACTION_SCALE_BLOCKER.csv",
    "finite_source": MTS_RESIDUALS / "P8_Y5_PARENT_QLOC_1995_FIRST_MATERIAL_CHARGE_SOURCE_REQUIREMENTS.csv",
    "runner_dryrun": MTS_RESIDUALS / "P8_Y5_PARENT_QLOC_1995_RUNNER_DRYRUN.csv",
    "claim_gate": MTS_RESIDUALS / "P8_Y5_PARENT_QLOC_1995_CLAIM_GATE.csv",
    "decision": MTS_RESIDUALS / "P8_Y5_PARENT_QLOC_1995_DECISION_LEDGER.csv",
    "next": MTS_RESIDUALS / "P8_Y5_PARENT_QLOC_1995_NEXT_TARGET.csv",
    "source_weight": SOURCE_WEIGHT_DOCS / "MATTER_INTERFACE_LABEL_FORGETTING_1995_NONCLAIM.csv",
    "wep_coeffs": MICROSCOPE_COEFFS / "P8_Y5_PARENT_QLOC_1995_FIRST_MATERIAL_CHARGE_SOURCE_REQUIREMENTS_NONCLAIM.csv",
    "queue": RAB_QUEUE / "JR1995_ACTION_SCALE_NORMALIZATION_OR_WEP_TAU_QUEUE.csv",
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
                "needed_for": "1995 matter-interface label-forgetting bridge",
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

    label_chain = [
        row(
            {
                "chain_id": "LFC1995_0_1063_source_forgetting",
                "imported_result": "label-forgotten source functor plus same-action Hilbert source gives one universal source normalization",
                "old_status": "CONDITIONAL_THEOREM_NOT_PARENT_DERIVED",
                "current_branch_use": "shows what must be true for source labels not to generate Delta_w or C_EP_direct",
                "verdict": "IMPORTED_AS_CONDITIONAL_CONTRACT",
            }
        ),
        row(
            {
                "chain_id": "LFC1995_1_1064_category_forgetting",
                "imported_result": "parent category label-forgetting remains conditional; relative w_A runner fills if not proved",
                "old_status": "CONDITIONAL_CONTRACT_NOT_PARENT_DERIVED",
                "current_branch_use": "connects matter labels to source-coupling selection",
                "verdict": "NO_PROMOTION",
            }
        ),
        row(
            {
                "chain_id": "LFC1995_2_1065_no_source_only_slot",
                "imported_result": "if parent grammar excludes an inert source-only species scalar w_A, then Delta_w_AB=0 follows",
                "old_status": "CONDITIONAL_GRAMMAR_NOT_PARENT_SIGNED",
                "current_branch_use": "reduces label-forgetting to a grammar/source-scalar theorem",
                "verdict": "ROOT_OBJECT_SHARPENED",
            }
        ),
        row(
            {
                "chain_id": "LFC1995_3_1066_action_scale_obstruction",
                "imported_result": "source-scalar exclusion is exact conditionally, but action-scale/measure ownership blocks promotion",
                "old_status": "CONDITIONAL_SOURCE_SCALAR_EXCLUSION_NOT_PARENT_DERIVED",
                "current_branch_use": "identifies the next parent action clause: one action-scale/measure owner",
                "verdict": "NEXT_BLOCKER_IDENTIFIED",
            }
        ),
    ]

    theorem_bridge = [
        row(
            {
                "bridge_id": "MIB1995_0_label_forgetting_law",
                "statement": "Matter-interface label-forgetting holds if the source-coupling functor receives T_total and public quotient data, not labelled pairs (T_A,A) or inert source scalars w_A.",
                "consequence": "relative source weights Delta_w_AB cannot be formed",
                "effect_on_CEP": "lambda_source_weight_i=0 and C_EP_direct loses the relative-source-weight channel",
                "status": "EXACT_CONDITIONAL_BRIDGE",
            }
        ),
        row(
            {
                "bridge_id": "MIB1995_1_action_scale_owner",
                "statement": "The parent action must own a single species-blind action-scale/measure normalization, so multiplying S_A by w_A is either a common calibration or inadmissible syntax.",
                "consequence": "w_A S_A cannot rescale Hilbert stress species-by-species",
                "effect_on_CEP": "Delta_w_TiPt=0 if parent-signed",
                "status": "MISSING_PARENT_ACTION_SCALE_OWNER",
            }
        ),
        row(
            {
                "bridge_id": "MIB1995_2_constants_split",
                "statement": "Measured masses, charges, representation data, and clock constants belong in theta_A with the same dynamics/source/readout owner; unobservable source-only weights are not theta_A.",
                "consequence": "ordinary material differences are physical matter content, not a hidden gravitational charge multiplier",
                "effect_on_CEP": "prevents hiding lambda_i inside mass/unit conventions",
                "status": "CONDITIONAL_NOT_SIGNED",
            }
        ),
        row(
            {
                "bridge_id": "MIB1995_3_full_branch_status",
                "statement": "Label-forgetting can kill the direct relative-source-weight/material-charge channel, but full C_EP also needs tau/projection and C_corr channels handled.",
                "consequence": "local-GR source side is closer but not claimed",
                "effect_on_CEP": "C_EP_direct may vanish under theorem; C_corr and projection debts remain",
                "status": "LOCAL_GR_SOURCE_SIDE_NOT_CLOSED",
            }
        ),
    ]

    blocker = [
        row(
            {
                "blocker_id": "ASB1995_0_classical_scale_trap",
                "blocker": "A species multiplier w_A S_A can leave isolated classical EOM shape unchanged while rescaling Hilbert stress.",
                "why_it_matters": "dismissing w_A as convention is not enough for a variational source theory",
                "needed_resolution": "prove w_A is a gauge/quotient redundancy for action, source, and measure, or forbid it by parent syntax",
                "status": "ACTIVE_BLOCKER",
            }
        ),
        row(
            {
                "blocker_id": "ASB1995_1_quantum_measure_owner",
                "blocker": "Path-integral/statistical/action normalization can make an overall action-scale coefficient physical.",
                "why_it_matters": "the parent theory must own the action scale, not leave one per matter species",
                "needed_resolution": "single hbar/action-measure owner or species-blind normalization theorem",
                "status": "ACTIVE_BLOCKER",
            }
        ),
        row(
            {
                "blocker_id": "ASB1995_2_measure_coframe_spurion",
                "blocker": "measure/coframe/boundary factors can reintroduce species labels without an explicit w_A term.",
                "why_it_matters": "a hidden spurion returns the same source-charge problem under a different name",
                "needed_resolution": "species-blind measure/coframe descent plus no hidden spurion return",
                "status": "ACTIVE_BLOCKER",
            }
        ),
    ]

    finite_source = [
        row(
            {
                "source_id": "FMS1995_0_Delta_w_TiPt",
                "quantity": "Delta_w_TiPt",
                "formula_role": "relative source-weight material contrast in C_EP_direct and MICROSCOPE WEP product",
                "units": "dimensionless",
                "source_requirement": "parent theorem zero from action-scale owner OR numeric prior/source row",
                "status": "MISSING_THEOREM_ZERO_OR_NUMERIC_PRIOR",
            }
        ),
        row(
            {
                "source_id": "FMS1995_1_tau_WEP",
                "quantity": "tau_WEP",
                "formula_role": "projection from Delta_w_TiPt into the MICROSCOPE/readout WEP channel",
                "units": "dimensionless",
                "source_requirement": "source worldtube, orbit/readout kernel, material tensor, sign convention, and normalization",
                "status": "MISSING_ARENA_PROJECTION",
            }
        ),
        row(
            {
                "source_id": "FMS1995_2_WEP_product",
                "quantity": "P_WEP_relative_source_weight",
                "formula_role": "abs(Delta_w_TiPt*tau_WEP) compared to eta bound; no cancellation or unity shortcut",
                "units": "dimensionless",
                "source_requirement": "both Delta_w_TiPt and tau_WEP real, sourced, numeric, and valid_for_claim=true before scoring",
                "status": "NOT_SCOREABLE",
            }
        ),
        row(
            {
                "source_id": "FMS1995_3_generic_lambda_i",
                "quantity": "lambda_i material/source charge",
                "formula_role": "fallback material-charge row if label-forgetting fails outside source-weight channel",
                "units": "parent_defined",
                "source_requirement": "parent action term, charge basis, units, test arenas, and source path",
                "status": "TEMPLATE_ONLY",
            }
        ),
    ]

    runner_dryrun = [
        row(
            {
                "run_id": "RUN1995_0_import_prior_chain",
                "check": "import 1063-1066 label-forgetting chain into current C_EP branch",
                "result": "PASS_IMPORTED",
                "reason": "older work already reduces label-forgetting to source-scalar exclusion and action-scale ownership",
            }
        ),
        row(
            {
                "run_id": "RUN1995_1_label_forgetting_proof",
                "check": "claim matter-interface label-forgetting as parent theorem",
                "result": "FAIL_ACTION_SCALE_OWNER_MISSING",
                "reason": "w_A S_A obstruction remains unless parent action-scale/measure normalization is signed",
            }
        ),
        row(
            {
                "run_id": "RUN1995_2_first_material_charge_source",
                "check": "score first finite material/source charge row",
                "result": "FAIL_DELTAW_AND_TAU_MISSING",
                "reason": "Delta_w_TiPt and tau_WEP are both missing or nonclaim",
            }
        ),
        row(
            {
                "run_id": "RUN1995_3_CEP_status",
                "check": "close C_EP direct/zero branch",
                "result": "FAIL_CONDITIONAL_ONLY",
                "reason": "direct channel has an exact theorem target but no parent signature; C_corr still retained",
            }
        ),
        row(
            {
                "run_id": "RUN1995_4_verdict",
                "check": "1995 next-step decision",
                "result": "NEXT_1996_PARENT_ACTION_SCALE_NORMALIZATION_OR_WEP_TAU_PROJECTION",
                "reason": "action-scale normalization is the clean theorem path; tau_WEP is the finite branch bottleneck",
            }
        ),
    ]

    claim_gate = [
        row(
            {
                "gate_id": "CG1995_0_label_chain_import",
                "claim": "1063-1066 chain is correctly imported as current-branch evidence",
                "status": "PASS_NONCLAIM_IMPORT",
                "reason": "all source paths and validation anchors exist",
            }
        ),
        row(
            {
                "gate_id": "CG1995_1_label_forgetting",
                "claim": "matter-interface label-forgetting is derived",
                "status": "FAIL_BLOCKED",
                "reason": "action-scale/measure owner is missing",
            }
        ),
        row(
            {
                "gate_id": "CG1995_2_source_scalar_zero",
                "claim": "Delta_w_TiPt=0 by theorem",
                "status": "FAIL_BLOCKED",
                "reason": "source-scalar exclusion is conditional only",
            }
        ),
        row(
            {
                "gate_id": "CG1995_3_finite_WEP_product",
                "claim": "finite WEP product can be scored",
                "status": "FAIL_BLOCKED",
                "reason": "Delta_w_TiPt and tau_WEP are missing",
            }
        ),
        row(
            {
                "gate_id": "CG1995_4_local_GR_Newton",
                "claim": "local GR/Newton source side is derived",
                "status": "FAIL_BLOCKED",
                "reason": "source-side action-scale/current/projection and C_corr gates remain open",
            }
        ),
    ]

    decision = [
        row(
            {
                "decision_id": "DEC1995_0_not_circling",
                "decision": "LABEL_FORGETTING_HAS_COLLAPSED_TO_ACTION_SCALE_OWNERSHIP",
                "because": "the prior chain shows no-source-only w_A is the root object; 1066 shows the remaining obstruction is action-scale/measure ownership",
                "next_action": "attack action-scale normalization before another WEP data row",
            }
        ),
        row(
            {
                "decision_id": "DEC1995_1_clean_route",
                "decision": "BEST_THEORY_ROUTE_IS_PARENT_ACTION_SCALE_NORMALIZATION",
                "because": "a species-blind action/measure owner forbids inert source scalars and pushes C_EP_direct toward zero",
                "next_action": "derive one hbar/action-measure owner or prove species multipliers are quotient redundancy",
            }
        ),
        row(
            {
                "decision_id": "DEC1995_2_finite_route",
                "decision": "IF_THE_CLEAN_ROUTE_FAILS_USE_TAU_WEP_NOT_HANDWAVING",
                "because": "a finite Delta_w prior is meaningless without the arena projection tau_WEP",
                "next_action": "fill tau_WEP from source worldtube, orbit/readout kernel, and material tensor",
            }
        ),
    ]

    next_target = [
        row(
            {
                "next_id": "NEXT1995_0_primary",
                "selection_status": "selected",
                "target_doc": "1996-Y5-R2FR-parent-action-scale-normalization-or-WEP-tau-projection.md",
                "target_script": "scripts/Y5_R2FR_parent_action_scale_normalization_or_WEP_tau_projection_1996.py",
                "task": "derive a single species-blind parent action-scale/measure owner that forbids w_A, or construct the real tau_WEP projection contract for the finite branch",
                "success_condition": "parent-signed action-scale normalization giving Delta_w_TiPt=0, or nonclaim tau_WEP projection rows with source worldtube, readout kernel, material tensor, units, and source paths",
                "do_not": "do not set w_A=1 by convention, set tau_WEP=1, absorb relative weights into measured G, claim local GR/WEP, push GitHub, or edit formalization-workbench",
            }
        )
    ]

    source_weight = [
        row(
            {
                "artifact_id": "SW1995_0_label_forgetting_bridge",
                "artifact_type": "matter_interface_label_forgetting_nonclaim_bridge",
                "status": "REDUCED_TO_ACTION_SCALE_OWNER",
                "source_path": str(DOC_PATH),
                "next_target": "1996-Y5-R2FR-parent-action-scale-normalization-or-WEP-tau-projection.md",
            }
        )
    ]

    wep_coeffs = [
        row(
            {
                "coefficient_id": "WEP1995_0_Delta_w_tau_requirements",
                "quantity": "Delta_w_TiPt and tau_WEP",
                "required_formula": "P_WEP_relative_source_weight = abs(Delta_w_TiPt*tau_WEP)",
                "required_evidence": "action-scale theorem-zero or numeric Delta_w prior; source/readout/material tau_WEP projection",
                "current_status": "MISSING_THEOREM_ZERO_AND_MISSING_TAU",
                "status": "NONCLAIM_REQUIREMENTS_ONLY",
            }
        )
    ]

    queue = [
        row(
            {
                "queue_id": "JR1995_0_action_scale_or_tau",
                "priority": "1",
                "needed_input": "parent action-scale normalization theorem or tau_WEP projection",
                "route": "derive one species-blind action/measure owner; if that fails, build tau_WEP from source worldtube, orbit/readout kernel, and Ti/Pt material tensor",
                "required_fields": "action_scale_owner;measure_owner;field_rescaling_guard;Delta_w_TiPt;tau_WEP;source_path;units",
                "blocked_claims": "Delta_w_zero;finite_WEP_product;C_EP_zero;local_GR;Newton",
            }
        )
    ]

    return {
        "source_register": source_register(stamp),
        "label_chain": label_chain,
        "theorem_bridge": theorem_bridge,
        "blocker": blocker,
        "finite_source": finite_source,
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
    val("VAL1995_00_sources", "PASS" if not source_failures else "FAIL", "all source paths exist and needles found" if not source_failures else ";".join(row["source_id"] for row in source_failures))

    chain_imported = any(row["chain_id"] == "LFC1995_3_1066_action_scale_obstruction" and row["verdict"] == "NEXT_BLOCKER_IDENTIFIED" for row in tables["label_chain"])
    val("VAL1995_01_label_chain", "PASS" if chain_imported else "FAIL", "label-forgetting chain reduces to action-scale obstruction")

    bridge_ready = any(row["bridge_id"] == "MIB1995_0_label_forgetting_law" and row["status"] == "EXACT_CONDITIONAL_BRIDGE" for row in tables["theorem_bridge"])
    bridge_blocked = any(row["bridge_id"] == "MIB1995_1_action_scale_owner" and row["status"] == "MISSING_PARENT_ACTION_SCALE_OWNER" for row in tables["theorem_bridge"])
    val("VAL1995_02_theorem_bridge", "PASS" if bridge_ready and bridge_blocked else "FAIL", "conditional bridge ready but parent action-scale owner missing")

    blockers_active = all(row["status"] == "ACTIVE_BLOCKER" for row in tables["blocker"])
    val("VAL1995_03_blockers", "PASS" if blockers_active else "FAIL", "action-scale/measure blockers retained")

    finite_missing = all(row["status"] in {"MISSING_THEOREM_ZERO_OR_NUMERIC_PRIOR", "MISSING_ARENA_PROJECTION", "NOT_SCOREABLE", "TEMPLATE_ONLY"} for row in tables["finite_source"])
    val("VAL1995_04_finite_source", "PASS" if finite_missing else "FAIL", "finite material/source rows remain missing-input nonclaim")

    runner_selects = tables["runner_dryrun"][-1]["result"] == "NEXT_1996_PARENT_ACTION_SCALE_NORMALIZATION_OR_WEP_TAU_PROJECTION"
    val("VAL1995_05_runner_decision", "PASS" if runner_selects else "FAIL", "runner selects action-scale/tau target")

    gates_safe = all(row["status"] in {"FAIL_BLOCKED", "PASS_NONCLAIM_IMPORT"} for row in tables["claim_gate"])
    no_physics_claim = all(row["status"] == "FAIL_BLOCKED" for row in tables["claim_gate"] if row["gate_id"] != "CG1995_0_label_chain_import")
    val("VAL1995_06_claim_gates", "PASS" if gates_safe and no_physics_claim else "FAIL", "only nonclaim import passes; physics claims blocked")

    next_ok = tables["next"][0]["target_doc"] == "1996-Y5-R2FR-parent-action-scale-normalization-or-WEP-tau-projection.md"
    val("VAL1995_07_next_target", "PASS" if next_ok else "FAIL", "1996 action-scale/tau target selected")

    all_rows = [row for rows_for_table in tables.values() for row in rows_for_table]
    flags_safe = all(row.get("valid_for_claim") == "false" and row.get("claim_allowed") == "false" for row in all_rows)
    val("VAL1995_08_claim_flags_safe", "PASS" if flags_safe else "FAIL", "claim flags all false")

    parse_failures = []
    for output_name, path in OUTPUTS.items():
        if not path.exists():
            parse_failures.append(f"{output_name}:missing")
            continue
        with path.open(newline="", encoding="utf-8") as handle:
            parsed = list(csv.DictReader(handle))
        if not parsed:
            parse_failures.append(f"{output_name}:empty")
    val("VAL1995_09_csv_parse", "PASS" if not parse_failures else "FAIL", "all generated CSVs parse with rows" if not parse_failures else ";".join(parse_failures))

    pycache_exists = (ROOT / "scripts" / "__pycache__").exists()
    val("VAL1995_10_pycache_absent", "PASS" if not pycache_exists else "FAIL", "scripts __pycache__ absent")

    formalization_artifacts = []
    checkpoint_markers = ("Y5_R2FR", "P8_Y5", "JR1995", "LFC1995", "MIB1995", "Delta_w", "tau_WEP")
    if FORMALIZATION.exists():
        formalization_artifacts = [
            path
            for path in FORMALIZATION.rglob("*")
            if "1995" in path.name and any(marker in path.name for marker in checkpoint_markers)
        ]
    val("VAL1995_11_formalization_untouched", "PASS" if not formalization_artifacts else "FAIL", f"formalization_1995_artifact_count={len(formalization_artifacts)}")

    overall = "PASS" if all(row["status"] == "PASS" for row in rows) else "FAIL"
    val("VAL1995_OVERALL", overall, "1995 matter-interface label-forgetting bridge")
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
        ("Label-Forgetting Chain Import", tables["label_chain"]),
        ("Matter-Interface Theorem Bridge", tables["theorem_bridge"]),
        ("Action-Scale Blocker", tables["blocker"]),
        ("First Material-Charge Source Requirements", tables["finite_source"]),
        ("Runner Dryrun", tables["runner_dryrun"]),
        ("Claim Gate", tables["claim_gate"]),
        ("Decision Ledger", tables["decision"]),
        ("Next Target", tables["next"]),
        ("Validation", validation_rows),
    ]
    lines = [
        "# 1995 Y5 R2FR: Matter-Interface Label-Forgetting Or First Material-Charge Source",
        "",
        "Private checkpoint. This folds the older 1063-1066 label-forgetting work into the current `C_EP` branch instead of circling the same coupling problem.",
        "",
        "Verdict: label-forgetting reduces to a sharper root clause: the parent action must forbid an inert source-only species scalar `w_A`, or prove it is a pure quotient/gauge redundancy for action, source, and measure. The old chain already shows this is exact conditionally but not parent-derived.",
        "",
        "Best current target: parent action-scale/measure normalization. If one species-blind action-scale owner is derived, the relative source-weight channel gives `Delta_w_TiPt=0` and removes the cleanest route to `C_EP_direct`. If it fails, the finite branch needs real `Delta_w_TiPt` and `tau_WEP` rows, not unity shortcuts.",
        "",
        "No WEP, local-GR, Newton, R10, PPN, clock, orbital, or public claim follows from 1995.",
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
    print(f"VAL1995_OVERALL={overall}")
    return 0 if overall == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())

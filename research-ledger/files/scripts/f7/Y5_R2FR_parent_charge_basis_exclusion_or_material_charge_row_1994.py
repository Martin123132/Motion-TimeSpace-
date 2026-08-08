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

DOC_PATH = ROOT / "1994-Y5-R2FR-parent-charge-basis-exclusion-or-material-charge-row.md"
VALIDATION_PATH = MTS_RESIDUALS / "P8_Y5_BRR545_1994_VALIDATION.csv"

SOURCES = {
    "1993_doc": {
        "path": ROOT / "1993-Y5-R2FR-C-EP-source-coefficient-or-common-mode-zero-theorem.md",
        "needles": ["CFL1993_0_basis_expansion", "NEXT1993_0_primary"],
    },
    "1993_validation": {
        "path": MTS_RESIDUALS / "P8_Y5_BRR545_1993_VALIDATION.csv",
        "needles": ["VAL1993_OVERALL", "PASS"],
    },
    "1030_single_public_metric": {
        "path": ROOT / "1030-Y5-R10-single-public-metric-parent-action-derivation-or-cg-provenance-gate.md",
        "needles": ["SPM1030_1_matter_functor_domain", "SPM1030_6_contract_verdict"],
    },
    "1030_validation": {
        "path": MTS_RESIDUALS / "P8_Y5_BRR545_1030_VALIDATION.csv",
        "needles": ["V1030_SUMMARY", "pass"],
    },
    "1031_terminal_metric": {
        "path": ROOT / "1031-Y5-R10-quotient-naturality-terminal-public-metric-proof-or-spm-closure.md",
        "needles": ["TPM1031_2_matter_interface_functor", "TPM1031_5_terminality_insufficiency"],
    },
    "1031_validation": {
        "path": MTS_RESIDUALS / "P8_Y5_BRR545_1031_VALIDATION.csv",
        "needles": ["V1031_SUMMARY", "pass"],
    },
    "1032_closure_ledger": {
        "path": ROOT / "1032-Y5-R10-spm-closure-ledger-and-finite-cg-tau-acquisition-runner.md",
        "needles": ["SPML1032_0_branch_definition", "ACQ1032_1_finite_cg_value"],
    },
    "1988_hilbert_source": {
        "path": ROOT / "1988-Y5-R2FR-action-weight-source-beta-theorem-or-finite-row-fill.md",
        "needles": ["THM1988_0_parent_form", "THEOREM_NOT_CLOSED_CURRENT_CORPUS"],
    },
}

OUTPUTS = {
    "source_register": MTS_RESIDUALS / "P8_Y5_PARENT_QLOC_1994_SOURCE_REGISTER.csv",
    "exclusion_theorem": MTS_RESIDUALS / "P8_Y5_PARENT_QLOC_1994_CHARGE_BASIS_EXCLUSION_THEOREM.csv",
    "proof_audit": MTS_RESIDUALS / "P8_Y5_PARENT_QLOC_1994_PROOF_AUDIT.csv",
    "countermodels": MTS_RESIDUALS / "P8_Y5_PARENT_QLOC_1994_COUNTERMODEL_LEDGER.csv",
    "material_charge": MTS_RESIDUALS / "P8_Y5_PARENT_QLOC_1994_MATERIAL_CHARGE_ROW_TEMPLATE.csv",
    "runner_dryrun": MTS_RESIDUALS / "P8_Y5_PARENT_QLOC_1994_RUNNER_DRYRUN.csv",
    "claim_gate": MTS_RESIDUALS / "P8_Y5_PARENT_QLOC_1994_CLAIM_GATE.csv",
    "decision": MTS_RESIDUALS / "P8_Y5_PARENT_QLOC_1994_DECISION_LEDGER.csv",
    "next": MTS_RESIDUALS / "P8_Y5_PARENT_QLOC_1994_NEXT_TARGET.csv",
    "source_weight": SOURCE_WEIGHT_DOCS / "PARENT_CHARGE_BASIS_EXCLUSION_1994_NONCLAIM.csv",
    "wep_coeffs": MICROSCOPE_COEFFS / "P8_Y5_PARENT_QLOC_1994_MATERIAL_CHARGE_ROW_TEMPLATE_NONCLAIM.csv",
    "queue": RAB_QUEUE / "JR1994_MATTER_INTERFACE_LABEL_FORGETTING_QUEUE.csv",
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
                "needed_for": "1994 parent charge-basis exclusion or first material-charge row",
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

    exclusion_theorem = [
        row(
            {
                "theorem_id": "CBX1994_0_statement",
                "statement": "If ordinary matter actions factor only through the public quotient coframe/metric and quotient-owned ordinary constants, with no extra material/source charge argument, then all direct nonmetric WEP charge-basis coefficients lambda_i vanish.",
                "formal_condition": "S_matter=sum_A S_A[Psi_A,e_pub(q(Phi)),omega(e_pub),theta_A(q)] and no term lambda_i X Q_i[A,material,source] or source-only current J_i is in the parent object language",
                "consequence_for_C_EP": "C_EP_direct=sum_i lambda_i*DeltaQ_i_TiPt*I_i_Earth_EP = 0",
                "status": "EXACT_CONDITIONAL_EXCLUSION_THEOREM",
            }
        ),
        row(
            {
                "theorem_id": "CBX1994_1_vertical_silence",
                "statement": "For v_X in ker(Dq), Lie_vX e_pub(q(Phi))=0 and Lie_vX theta_A(q)=0, so representative/memory vertical motion cannot create a material charge if the matter functor has no pre-quotient argument.",
                "formal_condition": "Dq[v_X]=0 plus matter-domain factorization through q",
                "consequence_for_C_EP": "no vertical source-weight beta or lambda_i is generated from ordinary matter variation",
                "status": "EXACT_CONDITIONAL_CHAIN_RULE",
            }
        ),
        row(
            {
                "theorem_id": "CBX1994_2_hilbert_source_owner",
                "statement": "The active gravitational source is the Hilbert/coframe variation of the same public matter action, not a species-weighted post-variation source sum.",
                "formal_condition": "T_total := delta S_matter/delta e_pub with one universal source normalization; no kappa_A, w_A, or J_nonH species/source multiplier",
                "consequence_for_C_EP": "ordinary composition changes inertial/internal stress, not a separate free-fall charge",
                "status": "EXACT_CONDITIONAL_SOURCE_OWNER",
            }
        ),
        row(
            {
                "theorem_id": "CBX1994_3_full_zero_clause",
                "statement": "Full C_EP=0 needs both direct charge-basis exclusion and silence/bounds for correction channels C_corr: hidden currents, support shifts, frame renames, calibration, and readout-domain leakage.",
                "formal_condition": "C_EP = C_EP_direct + C_corr and C_EP_direct=0 plus C_corr=0 or source-backed bound",
                "consequence_for_C_EP": "local-GR-safe WEP branch only after correction channels are also handled",
                "status": "FULL_ZERO_NOT_CLOSED",
            }
        ),
    ]

    proof_audit = [
        row(
            {
                "audit_id": "PFA1994_0_domain_exclusivity",
                "needed_clause": "matter action has terminal/public quotient domain only",
                "available_evidence": "1030 writes the single-public-metric contract; 1031 shows terminality alone is insufficient",
                "verdict": "NOT_PARENT_SIGNED",
                "next_gap": "derive matter-interface label-forgetting from the parent object language",
            }
        ),
        row(
            {
                "audit_id": "PFA1994_1_no_extra_charge_argument",
                "needed_clause": "no Q_i[A,material,source] argument can enter S_matter or source current before quotient evaluation",
                "available_evidence": "1988/1936 provide exact conditional Hilbert-source theorems but retain the w_A countermodel",
                "verdict": "NOT_PARENT_SIGNED",
                "next_gap": "exclude label/source multipliers rather than merely setting them small",
            }
        ),
        row(
            {
                "audit_id": "PFA1994_2_label_forgetting",
                "needed_clause": "ordinary species labels select Standard Model fields/parameters only, not MTS source charges",
                "available_evidence": "no current parent file proves the label-forgetting rule",
                "verdict": "MISSING_ROOT_CLAUSE",
                "next_gap": "state and prove the matter-interface label-forgetting theorem",
            }
        ),
        row(
            {
                "audit_id": "PFA1994_3_hidden_current_silence",
                "needed_clause": "no non-Hilbert/support/boundary current reintroduces C_corr",
                "available_evidence": "1030/1032 explicitly retain hidden-current and no-cancellation guards",
                "verdict": "RETAINED_RESIDUAL",
                "next_gap": "do not claim full C_EP=0 until C_corr is zero or bounded",
            }
        ),
        row(
            {
                "audit_id": "PFA1994_4_current_result",
                "needed_clause": "parent-signed charge-basis exclusion",
                "available_evidence": "conditional theorem exists; necessary clauses are isolated",
                "verdict": "THEOREM_READY_NOT_DERIVED",
                "next_gap": "1995 label-forgetting/domain proof or first material-charge row",
            }
        ),
    ]

    countermodels = [
        row(
            {
                "countermodel_id": "CM1994_0_terminal_but_labelled_functor",
                "model": "Q_obs has terminal e_pub, but S_A[Psi_A,E_A(q),theta_A] is evaluated on a labelled non-terminal ordinary frame before the terminal map.",
                "why_it_survives": "terminality is a morphism property, not an action-domain exclusion",
                "damage": "species/readout frame dependence can mimic a material charge slot",
                "status": "SURVIVES_UNLESS_LABEL_FORGETTING_PROVED",
            }
        ),
        row(
            {
                "countermodel_id": "CM1994_1_species_weighted_source",
                "model": "S_matter is public-metric, but the active source equation uses sum_A kappa_A delta S_A/delta e_pub.",
                "why_it_survives": "Ward conservation and covariance do not force all kappa_A equal",
                "damage": "creates DeltaQ_TiPt and a nonzero C_EP_direct",
                "status": "SURVIVES_UNLESS_HILBERT_OWNER_PROVED",
            }
        ),
        row(
            {
                "countermodel_id": "CM1994_2_hidden_material_constant",
                "model": "theta_A(q) contains an MTS-sensitive material marker m_A(q,X) or alpha_A(q,X) while the visible coframe remains public.",
                "why_it_survives": "single public metric alone does not control constants and material parameters",
                "damage": "moves lambda_i from the frame slot into a material-charge slot",
                "status": "SURVIVES_UNLESS_CONSTANT_LEDGER_SILENT",
            }
        ),
        row(
            {
                "countermodel_id": "CM1994_3_nonHilbert_support_current",
                "model": "ordinary matter is public-metric, but source support/boundary/domain terms carry a non-Hilbert current into the local projection.",
                "why_it_survives": "C_corr was separated in 1993 and is not killed by direct charge-basis exclusion",
                "damage": "direct lambda_i vanish but full C_EP can remain nonzero",
                "status": "SURVIVES_AS_CORRECTION_CHANNEL",
            }
        ),
    ]

    material_charge = [
        row(
            {
                "row_id": "MCR1994_0_generic_material_charge",
                "coefficient": "lambda_material_i",
                "formula_slot": "C_EP_direct += lambda_material_i*DeltaQ_i_TiPt*I_i_Earth_EP",
                "units": "dimensionless_or_parent_defined",
                "source_path": "MISSING_PARENT_SOURCE",
                "required_fields": "parent_action_term;charge_basis_i;lambda_i_units;DeltaQ_i_TiPt;I_i_Earth_EP;sign_convention;test_arenas;source_path",
                "status": "MISSING_PARENT_INPUT_NONCLAIM_ROW_ONLY",
            }
        ),
        row(
            {
                "row_id": "MCR1994_1_species_source_weight",
                "coefficient": "Delta_kappa_TiPt_or_Delta_w_TiPt",
                "formula_slot": "C_EP_direct += Delta_kappa_TiPt*I_Hilbert_Earth_EP",
                "units": "dimensionless",
                "source_path": "MISSING_PARENT_SOURCE",
                "required_fields": "species/source multiplier theorem-or-value;TiPt contrast;Earth source projection;WEP/R10/PPN links",
                "status": "BLOCKED_BY_1988_COUNTERMODEL",
            }
        ),
        row(
            {
                "row_id": "MCR1994_2_hidden_constant_charge",
                "coefficient": "lambda_theta_i",
                "formula_slot": "C_EP_direct += lambda_theta_i*Delta(partial ln theta_A/partial X)_TiPt*I_i",
                "units": "dimensionless_or_per_field_unit",
                "source_path": "MISSING_CONSTANT_LEDGER_SOURCE",
                "required_fields": "which theta_A;vertical derivative;material contrast;arena projection;source path",
                "status": "RETAINED_IF_LABEL_FORGETTING_FAILS",
            }
        ),
    ]

    runner_dryrun = [
        row(
            {
                "run_id": "RUN1994_0_conditional_exclusion",
                "check": "derive direct charge-basis exclusion from a parent-domain hypothesis",
                "result": "PASS_CONDITIONAL_THEOREM",
                "reason": "if matter only sees quotient public structures and one Hilbert source owner, direct lambda_i material/source charge slots are absent",
            }
        ),
        row(
            {
                "run_id": "RUN1994_1_parent_signature",
                "check": "promote exclusion theorem to derived MTS",
                "result": "FAIL_NOT_PARENT_SIGNED",
                "reason": "domain exclusivity, no extra charge argument, and label-forgetting remain missing",
            }
        ),
        row(
            {
                "run_id": "RUN1994_2_full_CEP_zero",
                "check": "claim C_EP=0",
                "result": "FAIL_CCORR_RETAINED",
                "reason": "even direct charge exclusion does not kill hidden current/support/frame/constant correction channels",
            }
        ),
        row(
            {
                "run_id": "RUN1994_3_material_charge_row",
                "check": "stage first material-charge row if exclusion fails",
                "result": "PASS_NONCLAIM_TEMPLATE_ONLY",
                "reason": "explicit lambda_i row schema exists but no value or source path is inserted",
            }
        ),
        row(
            {
                "run_id": "RUN1994_4_verdict",
                "check": "1994 next-step decision",
                "result": "NEXT_1995_MATTER_INTERFACE_LABEL_FORGETTING_OR_FIRST_MATERIAL_CHARGE_SOURCE",
                "reason": "label-forgetting is the root clause that would exclude the charge basis; otherwise the first material-charge row must be sourced",
            }
        ),
    ]

    claim_gate = [
        row(
            {
                "gate_id": "CG1994_0_conditional_theorem",
                "claim": "charge-basis exclusion theorem exists as a conditional contract",
                "status": "PASS_NONCLAIM_CONTRACT",
                "reason": "the theorem is exact under explicit parent-domain hypotheses",
            }
        ),
        row(
            {
                "gate_id": "CG1994_1_parent_derived_exclusion",
                "claim": "parent action excludes all material/source charge slots",
                "status": "FAIL_BLOCKED",
                "reason": "matter-interface label-forgetting and no-extra-charge argument are missing",
            }
        ),
        row(
            {
                "gate_id": "CG1994_2_CEP_zero",
                "claim": "C_EP=0",
                "status": "FAIL_BLOCKED",
                "reason": "direct charge exclusion is not parent-derived and C_corr remains retained",
            }
        ),
        row(
            {
                "gate_id": "CG1994_3_material_charge_value",
                "claim": "finite material-charge coefficient exists with value",
                "status": "FAIL_BLOCKED",
                "reason": "only a nonclaim row template exists; no parent source/value/units",
            }
        ),
        row(
            {
                "gate_id": "CG1994_4_local_GR_Newton",
                "claim": "local GR/Newton source side is derived",
                "status": "FAIL_BLOCKED",
                "reason": "needs parent charge-basis exclusion plus C_corr/left-hand field-equation gates",
            }
        ),
    ]

    decision = [
        row(
            {
                "decision_id": "DEC1994_0_progress",
                "decision": "DIRECT_CHARGE_EXCLUSION_THEOREM_IS_EXACT_BUT_CONDITIONAL",
                "because": "once ordinary matter can only see the public quotient coframe and one Hilbert source owner, no lambda_i material/source charge basis is available",
                "next_action": "prove that matter-interface/domain restriction from the parent corpus",
            }
        ),
        row(
            {
                "decision_id": "DEC1994_1_not_enough",
                "decision": "TERMINAL_PUBLIC_METRIC_OR_WEP_IS_NOT_ENOUGH",
                "because": "a labelled functor or source multiplier can survive terminality and covariance",
                "next_action": "attack label-forgetting/no-extra-charge argument directly",
            }
        ),
        row(
            {
                "decision_id": "DEC1994_2_fallback",
                "decision": "IF_LABEL_FORGETTING_FAILS_THE_THEORY_HAS_A_TESTABLE_MATERIAL_CHARGE",
                "because": "the surviving lambda_i row is not embarrassing if sourced; it becomes a fifth-force/WEP/clock/PPN object to bound",
                "next_action": "stage first material-charge row only with parent source path, units, and arena projections",
            }
        ),
    ]

    next_target = [
        row(
            {
                "next_id": "NEXT1994_0_primary",
                "selection_status": "selected",
                "target_doc": "1995-Y5-R2FR-matter-interface-label-forgetting-or-first-material-charge-source.md",
                "target_script": "scripts/Y5_R2FR_matter_interface_label_forgetting_or_first_material_charge_source_1995.py",
                "task": "prove ordinary matter labels cannot act as MTS source/material charge arguments, or source the first explicit material-charge coefficient row",
                "success_condition": "parent-signed label-forgetting theorem closing lambda_i slots, or a nonclaim material-charge row with source path, units, sign convention, and WEP/R10/PPN/clock/orbital test links",
                "do_not": "do not claim C_EP=0 from terminality, WEP quietness, covariance, or notation; do not invent lambda values; do not push GitHub",
            }
        )
    ]

    source_weight = [
        row(
            {
                "artifact_id": "SW1994_0_charge_basis_exclusion",
                "artifact_type": "parent_charge_basis_exclusion_nonclaim_contract",
                "status": "CONDITIONAL_THEOREM_READY_LABEL_FORGETTING_MISSING",
                "source_path": str(DOC_PATH),
                "next_target": "1995-Y5-R2FR-matter-interface-label-forgetting-or-first-material-charge-source.md",
            }
        )
    ]

    wep_coeffs = [
        row(
            {
                "coefficient_id": "WEP1994_0_material_charge_template",
                "quantity": "lambda_i material/source charge slot",
                "required_formula": "C_EP_direct = sum_i lambda_i*DeltaQ_i_TiPt*I_i_Earth_EP",
                "required_evidence": "parent action term or exclusion theorem; units; material contrast; source/readout projection; correction envelope",
                "current_status": "TEMPLATE_ONLY_NO_VALUE",
                "status": "NONCLAIM_SLOT_ONLY",
            }
        )
    ]

    queue = [
        row(
            {
                "queue_id": "JR1994_0_label_forgetting_or_charge_row",
                "priority": "1",
                "needed_input": "matter-interface label-forgetting theorem or first material-charge coefficient source",
                "route": "prove ordinary species labels select only ordinary fields/constants and cannot act as MTS source-charge arguments; if false, source lambda_i and test projections",
                "required_fields": "matter_interface_domain;label_forgetting_clause;no_extra_Q_i_argument;Hilbert_source_owner;C_corr_policy;source_path",
                "blocked_claims": "C_EP_zero;C_EP_nonzero;WEP_pass;local_GR;Newton",
            }
        )
    ]

    return {
        "source_register": source_register(stamp),
        "exclusion_theorem": exclusion_theorem,
        "proof_audit": proof_audit,
        "countermodels": countermodels,
        "material_charge": material_charge,
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
    val("VAL1994_00_sources", "PASS" if not source_failures else "FAIL", "all source paths exist and needles found" if not source_failures else ";".join(row["source_id"] for row in source_failures))

    theorem_ready = any(row["theorem_id"] == "CBX1994_0_statement" and row["status"] == "EXACT_CONDITIONAL_EXCLUSION_THEOREM" for row in tables["exclusion_theorem"])
    full_not_closed = any(row["theorem_id"] == "CBX1994_3_full_zero_clause" and row["status"] == "FULL_ZERO_NOT_CLOSED" for row in tables["exclusion_theorem"])
    val("VAL1994_01_exclusion_theorem", "PASS" if theorem_ready and full_not_closed else "FAIL", "conditional charge-basis exclusion written without full C_EP zero claim")

    root_gap = any(row["audit_id"] == "PFA1994_2_label_forgetting" and row["verdict"] == "MISSING_ROOT_CLAUSE" for row in tables["proof_audit"])
    val("VAL1994_02_proof_audit", "PASS" if root_gap else "FAIL", "label-forgetting is isolated as root missing clause")

    countermodels_live = all(row["status"].startswith("SURVIVES") for row in tables["countermodels"])
    val("VAL1994_03_countermodels", "PASS" if countermodels_live else "FAIL", "all countermodels remain live unless named clauses are proved")

    template_only = all("MISSING" in row["status"] or "BLOCKED" in row["status"] or "RETAINED" in row["status"] for row in tables["material_charge"])
    val("VAL1994_04_material_charge_template", "PASS" if template_only else "FAIL", "material-charge rows are template-only and nonclaim")

    runner_selects = tables["runner_dryrun"][-1]["result"] == "NEXT_1995_MATTER_INTERFACE_LABEL_FORGETTING_OR_FIRST_MATERIAL_CHARGE_SOURCE"
    val("VAL1994_05_runner_decision", "PASS" if runner_selects else "FAIL", "runner selects label-forgetting/material-charge target")

    gates_safe = all(row["status"] in {"FAIL_BLOCKED", "PASS_NONCLAIM_CONTRACT"} for row in tables["claim_gate"])
    no_physics_claim = all(row["status"] == "FAIL_BLOCKED" for row in tables["claim_gate"] if row["gate_id"] != "CG1994_0_conditional_theorem")
    val("VAL1994_06_claim_gates", "PASS" if gates_safe and no_physics_claim else "FAIL", "only conditional contract passes; physics claims blocked")

    next_ok = tables["next"][0]["target_doc"] == "1995-Y5-R2FR-matter-interface-label-forgetting-or-first-material-charge-source.md"
    val("VAL1994_07_next_target", "PASS" if next_ok else "FAIL", "1995 label-forgetting/material-charge target selected")

    all_rows = [row for rows_for_table in tables.values() for row in rows_for_table]
    flags_safe = all(row.get("valid_for_claim") == "false" and row.get("claim_allowed") == "false" for row in all_rows)
    val("VAL1994_08_claim_flags_safe", "PASS" if flags_safe else "FAIL", "claim flags all false")

    parse_failures = []
    for output_name, path in OUTPUTS.items():
        if not path.exists():
            parse_failures.append(f"{output_name}:missing")
            continue
        with path.open(newline="", encoding="utf-8") as handle:
            parsed = list(csv.DictReader(handle))
        if not parsed:
            parse_failures.append(f"{output_name}:empty")
    val("VAL1994_09_csv_parse", "PASS" if not parse_failures else "FAIL", "all generated CSVs parse with rows" if not parse_failures else ";".join(parse_failures))

    pycache_exists = (ROOT / "scripts" / "__pycache__").exists()
    val("VAL1994_10_pycache_absent", "PASS" if not pycache_exists else "FAIL", "scripts __pycache__ absent")

    formalization_artifacts = []
    checkpoint_markers = ("Y5_R2FR", "P8_Y5", "JR1994", "MCR1994", "CBX1994", "C_EP")
    if FORMALIZATION.exists():
        formalization_artifacts = [
            path
            for path in FORMALIZATION.rglob("*")
            if "1994" in path.name and any(marker in path.name for marker in checkpoint_markers)
        ]
    val("VAL1994_11_formalization_untouched", "PASS" if not formalization_artifacts else "FAIL", f"formalization_1994_artifact_count={len(formalization_artifacts)}")

    overall = "PASS" if all(row["status"] == "PASS" for row in rows) else "FAIL"
    val("VAL1994_OVERALL", overall, "1994 parent charge-basis exclusion or material-charge row")
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
        ("Charge-Basis Exclusion Theorem", tables["exclusion_theorem"]),
        ("Proof Audit", tables["proof_audit"]),
        ("Countermodel Ledger", tables["countermodels"]),
        ("Material-Charge Row Template", tables["material_charge"]),
        ("Runner Dryrun", tables["runner_dryrun"]),
        ("Claim Gate", tables["claim_gate"]),
        ("Decision Ledger", tables["decision"]),
        ("Next Target", tables["next"]),
        ("Validation", validation_rows),
    ]
    lines = [
        "# 1994 Y5 R2FR: Parent Charge-Basis Exclusion Or Material-Charge Row",
        "",
        "Private checkpoint. This attacks the cleanest route after the 1993 `C_EP` factor law: can the parent action forbid every nonmetric material/source charge slot?",
        "",
        "Verdict: the direct charge-basis exclusion theorem is exact as a conditional theorem. If ordinary matter only sees the public quotient coframe/metric and one Hilbert source owner, with no extra `Q_i` material/source argument, then the direct coefficients `lambda_i` vanish and `C_EP_direct=0`.",
        "",
        "But it is not yet a derived MTS theorem. Terminal public metric, covariance, WEP quietness, and notation are not enough; the missing root clause is matter-interface label-forgetting: ordinary species labels must select Standard Model fields/parameters only, not MTS source charges.",
        "",
        "The useful fork is now sharp. Either prove label-forgetting and push toward the clean local-GR source side, or admit the first explicit material-charge row and test it like a fifth-force/WEP coefficient.",
        "",
        "No WEP, local-GR, Newton, R10, PPN, clock, orbital, or public claim follows from 1994.",
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
    print(f"VAL1994_OVERALL={overall}")
    return 0 if overall == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())

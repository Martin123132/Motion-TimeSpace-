from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "source-intake" / "mts_residuals"
MICROSCOPE = ROOT / "source-intake" / "microscope"
BRANCH_RESIDUALS = MICROSCOPE / "branch_locked_wep" / "residuals"
FORMALIZATION = ROOT.parent / "formalization-workbench"
BRANCH_ID = "MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428"
DOC = ROOT / "1518-Y5-parent-PiM-commutator-zero-theorem-or-R_eq-I_commutator-source-acquisition.md"
START_TS = datetime.now(timezone.utc).timestamp()

SOURCE_FILES = {
    "1517_validation": OUT / "P8_Y5_BRR545_1517_VALIDATION.csv",
    "1517_next": OUT / "P8_Y5_PARENT_PIM_1517_NEXT_TARGET.csv",
    "1517_import": OUT / "P8_Y5_PARENT_PIM_1517_THEOREM_IMPORT_GATE.csv",
    "1152_audit": OUT / "P8_Y5_R10_1152_COMMUTATOR_ZERO_THEOREM_AUDIT.csv",
    "1152_acq": OUT / "P8_Y5_R10_1152_R_EQ_I_COMMUTATOR_SOURCE_ACQUISITION_ROWS.csv",
    "1152_guards": OUT / "P8_Y5_R10_1152_PROJECTOR_ROUTE_GUARDS.csv",
    "1357_zero": OUT / "P8_Y5_R10_1357_PIM_COMMUTATOR_ZERO_ATTEMPT.csv",
    "1357_profiles": OUT / "P8_Y5_R10_1357_ICOMMUTATOR_SOURCE_PROFILE_ROWS.csv",
    "1357_guards": OUT / "P8_Y5_R10_1357_CHAINMAP_GUARDRAILS.csv",
    "1358_signature": OUT / "P8_Y5_R10_1358_FIXED_CHAINMAP_PARENT_SIGNATURE_ATTEMPT.csv",
    "1358_contract": OUT / "P8_Y5_R10_1358_PARENT_CHAINMAP_CONTRACT.csv",
    "1358_schema": OUT / "P8_Y5_R10_1358_ICOMMUTATOR_FIRST_PROFILE_ROW_SCHEMA.csv",
    "1359_selector": OUT / "P8_Y5_R10_1359_PARENT_SELECTOR_ACTION_ATTEMPT.csv",
    "1359_obstructions": OUT / "P8_Y5_R10_1359_SELECTOR_ACTION_OBSTRUCTION_LEDGER.csv",
    "1359_intake": OUT / "P8_Y5_R10_1359_ICOMMUTATOR_SOURCE_INTAKE_LEDGER.csv",
    "1360_locality": OUT / "P8_Y5_R10_1360_SELECTOR_LOCALITY_DIFFERENTIABILITY_ATTEMPT.csv",
    "1360_stress": OUT / "P8_Y5_R10_1360_SELECTOR_STRESS_LEDGER.csv",
    "1360_intake": OUT / "P8_Y5_R10_1360_MHREF_SURFACE_INTAKE_ROWS.csv",
    "1360_next": OUT / "P8_Y5_R10_1360_NEXT_TARGET.csv",
}

COMMUTATOR_AUDIT = OUT / "P8_Y5_PARENT_PIM_1518_COMMUTATOR_ZERO_AUDIT.csv"
CHAINMAP_CONTRACT = OUT / "P8_Y5_PARENT_PIM_1518_FIXED_CHAINMAP_CONTRACT.csv"
SOURCE_ACQUISITION = OUT / "P8_Y5_PARENT_PIM_1518_SOURCE_ACQUISITION_ROWS.csv"
SELECTOR_OBSTRUCTION = OUT / "P8_Y5_PARENT_PIM_1518_SELECTOR_OBSTRUCTION_LEDGER.csv"
MHREF_SURFACE_LOCK = OUT / "P8_Y5_PARENT_PIM_1518_MHREF_SURFACE_LOCK.csv"
REJECTION_LEDGER = OUT / "P8_Y5_PARENT_PIM_1518_REJECTION_LEDGER.csv"
DECISION = OUT / "P8_Y5_PARENT_PIM_1518_DECISION.csv"
LOCAL_STATUS = OUT / "P8_Y5_PARENT_PIM_1518_LOCAL_GR_NEWTON_STATUS.csv"
NEXT_TARGET = OUT / "P8_Y5_PARENT_PIM_1518_NEXT_TARGET.csv"
VALIDATION = OUT / "P8_Y5_BRR545_1518_VALIDATION.csv"

QUARANTINE = MICROSCOPE / "quarantine" / "1518"
QUAR_AUDIT = QUARANTINE / "PIM_COMMUTATOR_ZERO_AUDIT_NONCLAIM.csv"
QUAR_SOURCE = QUARANTINE / "PIM_SOURCE_ACQUISITION_ROWS_NONCLAIM.csv"
QUAR_MHREF = QUARANTINE / "PIM_MHREF_SURFACE_LOCK_NONCLAIM.csv"
QUAR_DECISION = QUARANTINE / "PIM_DECISION_NONCLAIM.csv"
BRANCH_AUDIT = BRANCH_RESIDUALS / "pim_commutator_zero_audit_nonclaim_1518.csv"
BRANCH_SOURCE = BRANCH_RESIDUALS / "pim_source_acquisition_rows_nonclaim_1518.csv"
BRANCH_MHREF = BRANCH_RESIDUALS / "pim_mhref_surface_lock_nonclaim_1518.csv"
BRANCH_DECISION_COPY = BRANCH_RESIDUALS / "pim_decision_nonclaim_1518.csv"


def flags() -> dict[str, bool]:
    return {"score_ready": False, "valid_prediction_row": False, "valid_for_claim": False, "claim_allowed": False}


def rel(path: Path) -> str:
    try:
        return str(path.relative_to(ROOT)).replace("\\", "/")
    except ValueError:
        return str(path)


def source_list(*keys: str) -> str:
    return "; ".join(rel(SOURCE_FILES[key]) for key in keys)


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        raise ValueError(f"no rows for {path}")
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def parse_csv(path: Path) -> bool:
    read_csv(path)
    return True


def generated_flags_false(paths: list[Path]) -> bool:
    false_values = {"", "false", "0", "no", "none", "null"}
    claim_keys = ["score_ready", "valid_prediction_row", "valid_for_claim", "claim_allowed", "accepted_for_scoring", "passes_for_claim"]
    for path in paths:
        for row in read_csv(path):
            for key in claim_keys:
                if key in row and str(row[key]).strip().lower() not in false_values:
                    return False
    return True


def commutator_audit_rows() -> list[dict[str, Any]]:
    rows = [
        ("COM1518_0_product_rule", "d(Pi_M J_H)=Pi_M dJ_H+[d,Pi_M]J_H", "IDENTITY_RETAINED", "dropping the commutator would be algebraic handwaving", source_list("1517_import", "1152_audit")),
        ("COM1518_1_conditional_chainmap", "fixed topological chain-map implies [d,Pi_M]J_H=0", "VALID_CONDITIONAL_MATH_ONLY", "conditional theorem has no claim credit until parent ownership is signed", source_list("1357_zero", "1358_contract")),
        ("COM1518_2_parent_fixed_domain", "source worldtube/exterior annulus/linking class fixed before readout", "NOT_PARENT_SIGNED", "domain derivative feeds I_commutator", source_list("1358_signature", "1360_locality")),
        ("COM1518_3_metric_independent_PiM", "Pi_M is topological not Hodge/DeWitt/Green metric machinery", "CONDITIONAL_NOT_DERIVED", "Hodge route keeps projector stress and PPN/R11 residuals", source_list("1357_guards", "1360_stress")),
        ("COM1518_4_physical_current_domain", "physical Hilbert current lies in the fixed chain-map complex", "SOURCE_DOMAIN_NOT_LOCKED", "commutator-zero proof can target a surrogate current", source_list("1357_zero", "1358_contract")),
        ("COM1518_5_exterior_silence", "no source/anomaly/boundary support in compact exterior annulus", "NOT_DERIVED", "finite-shell I_commutator profile can be nonzero", source_list("1357_profiles", "1359_intake")),
        ("COM1518_6_tau_MHref", "same tau/source/charge/readout frame and M_H_ref denominator", "MISSING_TAU_MHREF_LOCK", "I_commutator cannot be normalized claim-safely", source_list("1360_intake", "1360_next")),
        ("COM1518_7_selector_action", "parent selector action owns chi_M,W_M,omega_M_top,ell_M,Pi_M", "PARENT_SELECTOR_ACTION_NOT_DERIVED", "candidate selector sector is closure machinery unless parent-derived", source_list("1359_selector", "1359_obstructions")),
        ("COM1518_8_verdict", "current MTS proves [d,Pi_M]J_H=0", "PIM_COMMUTATOR_ZERO_NOT_PROVED", "retain source-acquisition rows and keep Newton/local-GR blocked", source_list("1152_audit", "1360_locality")),
    ]
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "audit_id": audit_id,
            "claim_piece": piece,
            "current_status": status,
            "failure_if_missing": failure,
            "source_paths": sources,
            **flags(),
        }
        for audit_id, piece, status, failure, sources in rows
    ]


def chainmap_contract_rows() -> list[dict[str, Any]]:
    rows = [
        ("FCM1518_0_selector", "parent action selects mass/topology channel before observations", "MISSING_PARENT_SELECTOR", "chi_M or ell_M source in existing parent action"),
        ("FCM1518_1_worldtube", "source worldtube and exterior linking class are fixed", "MISSING_DOMAIN_LOCK", "worldtube support theorem or parent boundary condition"),
        ("FCM1518_2_representative", "closed normalized topological representative is supplied", "CONDITIONAL_TEMPLATE_ONLY", "omega_M_top tied to physical source, not arbitrary topology"),
        ("FCM1518_3_chainmap", "Pi_M is a chain-map on the Hilbert-current complex", "CONDITIONAL_LEMMA_ONLY", "proof Pi_M maps physical source complex to fixed de Rham class"),
        ("FCM1518_4_current", "physical J_H belongs to the same fixed complex", "MISSING_CURRENT_DOMAIN_LOCK", "same-frame Hilbert current including extra/source/species channels"),
        ("FCM1518_5_exterior", "finite annulus contains no commutator source", "MISSING_EXTERIOR_SILENCE_THEOREM", "support and boundary theorem for A_parent, B_flux, extra current"),
        ("FCM1518_6_tau_MHref", "same time generator and denominator are parent-owned", "MISSING_TAU_MHREF_LOCK", "Hamiltonian charge/reference theorem and source denominator row"),
    ]
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "contract_id": contract_id,
            "parent_requirement": requirement,
            "current_status": status,
            "evidence_needed": evidence,
            "source_paths": source_list("1358_contract", "1360_intake"),
            **flags(),
        }
        for contract_id, requirement, status, evidence in rows
    ]


def source_acquisition_rows() -> list[dict[str, Any]]:
    rows = [
        ("ACQ1518_0_R_eq", "R_eq_integral", "int_A_ext abs(Pi_M J_H - J_M_top - dB_zero)", "MISSING_R_EQ_INTEGRAL", "R_eq source/theorem row for same source worldtube", source_list("1152_acq", "1517_import")),
        ("ACQ1518_1_I_commutator", "I_commutator", "int_A_ext abs([d,Pi_M]J_H)", "MISSING_I_COMMUTATOR", "commutator source profile or chain-map theorem on physical J_H", source_list("1152_acq", "1357_profiles")),
        ("ACQ1518_2_projector_stress", "epsilon_projector_stress", "projector stress beta/source-normalized equivalent", "MISSING_PROJECTOR_STRESS_MAP", "stress theorem or finite local residual calculation", source_list("1152_acq", "1360_stress")),
        ("ACQ1518_3_MHref", "M_H_ref", "same-frame Hilbert/Hamiltonian source mass denominator", "MISSING_M_H_REF", "Q_tau/H_ref/tau-frame source-backed row, not orbital GM", source_list("1360_intake")),
        ("ACQ1518_4_surfaces", "S1/S2/A_ext", "fixed linked surfaces and annulus homology before readout", "MISSING_SURFACE_AND_HOMOLOGY_INPUTS", "inner/outer surfaces, homology class, source-free exterior source path", source_list("1360_intake")),
        ("ACQ1518_5_total", "epsilon_PiM_total_abs", "absolute runner envelope", "BLOCKED_MISSING_COMPONENTS", "all component rows source-backed or theorem-zeroed", source_list("1517_import", "1517_validation")),
    ]
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "row_id": row_id,
            "quantity": quantity,
            "definition": definition,
            "current_status": status,
            "required_input": required,
            "source_paths": sources,
            **flags(),
        }
        for row_id, quantity, definition, status, required, sources in rows
    ]


def selector_obstruction_rows() -> list[dict[str, Any]]:
    rows = [
        ("OBS1518_0_auxiliary_sector", "selector action may add new variables", "OPEN", "derive chi_M/omega_M_top/ell_M from existing parent variables or mark as extension"),
        ("OBS1518_1_nonlocal_support", "W_M=supp(J_H) is nonlocal and nonsmooth", "OPEN", "prove compact regular support and differentiable worldtube class"),
        ("OBS1518_2_wrong_charge", "closed omega_M_top may conserve wrong object", "OPEN", "prove ell_M is same-frame Hamiltonian source charge"),
        ("OBS1518_3_chainmap_functional", "d ell_M[J]=ell_M[dJ] not automatic", "OPEN", "derive Hamiltonian/source-measure lock or keep numerator row"),
        ("OBS1518_4_selector_stress", "selector constraints can generate stress", "OPEN", "compute delta_g S_selector or prove topological metric independence"),
        ("OBS1518_5_denominator", "M_H_ref missing", "OPEN", "source or derive same-frame Hamiltonian denominator"),
    ]
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "obstruction_id": obstruction_id,
            "obstruction": obstruction,
            "current_status": status,
            "repair": repair,
            "source_paths": source_list("1359_obstructions", "1360_stress"),
            **flags(),
        }
        for obstruction_id, obstruction, status, repair in rows
    ]


def mhref_surface_rows() -> list[dict[str, Any]]:
    rows = [
        ("MH1518_0_M_H_ref", "M_H_ref", "MISSING_M_H_REF", "system_id;tau_id;surface_outer;Q_tau_integral;G_ref;H_ref;units;source_path;source_anchor"),
        ("MH1518_1_S1", "inner linking surface S1/r1", "MISSING_INNER_RADIUS_OR_SURFACE", "surface_inner_id;r1;links_W_M;fixed_before_readout;source_path"),
        ("MH1518_2_S2", "outer linking surface S2/r2", "MISSING_OUTER_RADIUS_OR_SURFACE", "surface_outer_id;r2;homology_class;fixed_before_readout;source_path"),
        ("MH1518_3_annulus", "A_ext and homology class", "MISSING_ANNULUS_HOMOLOGY_SOURCE", "boundary_relation;S1_homology;S2_homology;exterior_source_free;source_path"),
        ("MH1518_4_tau_frame", "tau/source/charge/readout lock", "MISSING_TAU_FRAME_LOCK", "e_obs_id;tau_source;tau_charge;tau_clock;tau_readout;lock_certificate"),
        ("MH1518_5_Qtau_ref", "Q_tau integrability and H_ref", "MISSING_QTAU_INTEGRABILITY_REFERENCE", "delta_H_tau_curl;Q_tau_integral;H_ref;Delta_ref;B_zero_flux;Delta_symp"),
        ("MH1518_6_domain_num", "int_A dPiM_domain J_H", "MISSING_INT_A_DPiM_DOMAIN_JH", "annulus_A;dPiM_domain;J_H_source;integral_value;M_H_ref;normalization"),
        ("MH1518_7_acceptance", "first-profile acceptance gate", "CLAIM_BLOCKED", "all_required_items_present;no_MISSING;units_compatible;sources_verified;anti_cheat_flags_true"),
    ]
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "lock_id": lock_id,
            "quantity": quantity,
            "current_status": status,
            "required_columns": required_columns,
            "source_paths": source_list("1360_intake"),
            **flags(),
        }
        for lock_id, quantity, status, required_columns in rows
    ]


def rejection_rows() -> list[dict[str, Any]]:
    rows = [
        ("REJ1518_0_idempotence", "Pi_M^2=Pi_M as commutator proof", "REJECTED", "projector algebra is not chain-map ownership"),
        ("REJ1518_1_hodge_silence", "Hodge/metric projector with no stress row", "REJECTED", "metric dependence requires projector-stress accounting"),
        ("REJ1518_2_readout_mask", "choose Pi_M after orbital/readout residuals", "REJECTED", "post-readout mask is not a parent theorem"),
        ("REJ1518_3_orbital_denominator", "normalize I_commutator by orbital GM", "REJECTED", "orbital GM is what the source transfer must derive"),
        ("REJ1518_4_auxiliary_closure", "add selector multipliers as if already derived", "REJECTED", "candidate selector action is closure unless parent-owned"),
    ]
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "rejection_id": rejection_id,
            "shortcut": shortcut,
            "status": status,
            "reason": reason,
            **flags(),
        }
        for rejection_id, shortcut, status, reason in rows
    ]


def decision_rows() -> list[dict[str, Any]]:
    rows = [
        ("DEC1518_0_commutator", "PiM commutator zero", "NOT_PROVED", "fixed-chainmap route is clean but not parent-signed"),
        ("DEC1518_1_source_rows", "R_eq/I_commutator acquisition", "ACTIVE_NONCLAIM", "rows exist but remain missing/source-unfilled"),
        ("DEC1518_2_selector", "selector action route", "CONTRACT_ONLY_NOT_DERIVED", "local proxy exists but auxiliary/stress/MHref debts remain"),
        ("DEC1518_3_next", "observed coframe/tau/MHref lock", "NEXT_1519_MHREF", "same-frame tau/source denominator is now the sharpest denominator blocker"),
    ]
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "decision_id": decision_id,
            "decision": decision,
            "result": result,
            "rationale": rationale,
            **flags(),
        }
        for decision_id, decision, result, rationale in rows
    ]


def local_status_rows() -> list[dict[str, Any]]:
    rows = [
        ("LOCAL1518_0_Newton", "source-normalized Newtonian limit", "NOT_CLAIMED", "PiM commutator/equality and M_H_ref denominator remain open"),
        ("LOCAL1518_1_GR", "derived local GR", "NOT_CLAIMED", "Newton denominator plus PPN followthrough still missing"),
        ("LOCAL1518_2_GM", "measured-GM transfer", "NOT_CLAIMED", "M_H_ref cannot be replaced by orbital GM"),
        ("LOCAL1518_3_R11", "R11 source-normalization", "ACTIVE_NONCLAIM", "source-normalization vector remains unbounded/unzeroed"),
        ("LOCAL1518_4_PPN", "PPN source stability", "NOT_CLAIMED", "selector stress and projector/Hodge rows remain open"),
    ]
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "status_id": status_id,
            "claim": claim,
            "current_status": status,
            "reason": reason,
            **flags(),
        }
        for status_id, claim, status, reason in rows
    ]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "next_id": "NEXT1518_0_1519",
            "next_target": "1519-Y5-parent-observed-coframe-tau-source-frame-lock-or-MHref-first-row.md",
            "script": "scripts/Y5_parent_observed_coframe_tau_source_frame_lock_or_MHref_first_row.py",
            "objective": "try to parent-sign one observed coframe and tau/source/charge/readout lock needed for M_H_ref; if not, write the first nonclaim M_H_ref source-row schema with Q_tau/H_ref/surface/source requirements",
            **flags(),
        }
    ]


def copy_outputs() -> None:
    copies = [
        (COMMUTATOR_AUDIT, QUAR_AUDIT),
        (SOURCE_ACQUISITION, QUAR_SOURCE),
        (MHREF_SURFACE_LOCK, QUAR_MHREF),
        (DECISION, QUAR_DECISION),
        (COMMUTATOR_AUDIT, BRANCH_AUDIT),
        (SOURCE_ACQUISITION, BRANCH_SOURCE),
        (MHREF_SURFACE_LOCK, BRANCH_MHREF),
        (DECISION, BRANCH_DECISION_COPY),
    ]
    for source, destination in copies:
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(source, destination)


def remove_pycache() -> None:
    pycache = ROOT / "scripts" / "__pycache__"
    if pycache.exists():
        shutil.rmtree(pycache)


def formalization_modified_count_since_start() -> int:
    if not FORMALIZATION.exists():
        return 0
    return sum(1 for path in FORMALIZATION.rglob("*") if path.is_file() and path.stat().st_mtime >= START_TS)


def validation_rows(generated_csvs: list[Path]) -> list[dict[str, Any]]:
    audit = read_csv(COMMUTATOR_AUDIT)
    contract = read_csv(CHAINMAP_CONTRACT)
    source_rows = read_csv(SOURCE_ACQUISITION)
    obstructions = read_csv(SELECTOR_OBSTRUCTION)
    mhref = read_csv(MHREF_SURFACE_LOCK)
    decisions = read_csv(DECISION)
    next_rows = read_csv(NEXT_TARGET)

    checks = [
        ("VAL1518_0_sources", all(path.exists() for path in SOURCE_FILES.values()), "all cited 1518 input source paths exist"),
        ("VAL1518_1_commutator_not_proved", any(row["audit_id"] == "COM1518_8_verdict" and "NOT_PROVED" in row["current_status"] for row in audit), "PiM commutator zero remains unproved"),
        ("VAL1518_2_chainmap_contract_complete", len(contract) >= 7 and any(row["contract_id"] == "FCM1518_6_tau_MHref" for row in contract), "fixed-chainmap contract includes selector/domain/current/exterior/tau clauses"),
        ("VAL1518_3_source_rows_missing", any(row["quantity"] == "R_eq_integral" and "MISSING" in row["current_status"] for row in source_rows) and any(row["quantity"] == "I_commutator" and "MISSING" in row["current_status"] for row in source_rows), "R_eq and I_commutator acquisition rows remain explicit and missing"),
        ("VAL1518_4_selector_obstructions_open", all(row["current_status"] == "OPEN" for row in obstructions), "selector action obstructions remain open"),
        ("VAL1518_5_mhref_surface_lock", any(row["quantity"] == "M_H_ref" and "MISSING" in row["current_status"] for row in mhref) and any("S1" in row["quantity"] for row in mhref), "M_H_ref and surface intake locks are staged"),
        ("VAL1518_6_decision_next", any(row["result"] == "NEXT_1519_MHREF" for row in decisions), "decision selects observed coframe/tau/MHref next"),
        ("VAL1518_7_next_target", any("observed-coframe-tau" in row["next_target"] for row in next_rows), "next target is observed coframe/tau/source-frame lock"),
        ("VAL1518_8_csv_parse", all(parse_csv(path) for path in generated_csvs), "all generated 1518 CSVs parse cleanly"),
        ("VAL1518_9_claim_flags_false", generated_flags_false(generated_csvs), "all generated prediction/claim flags remain false"),
        ("VAL1518_10_branch_copies", all(path.exists() for path in [QUAR_AUDIT, QUAR_SOURCE, QUAR_MHREF, QUAR_DECISION, BRANCH_AUDIT, BRANCH_SOURCE, BRANCH_MHREF, BRANCH_DECISION_COPY]), "branch/quarantine nonclaim copies written"),
        ("VAL1518_11_pycache_absent", not (ROOT / "scripts" / "__pycache__").exists(), "scripts __pycache__ absent after run"),
        ("VAL1518_12_formalization_untouched", formalization_modified_count_since_start() == 0, "formalization modified-file count since start=0"),
    ]
    overall = all(result for _, result, _ in checks)
    rows = [
        {"same_parent_branch_id": BRANCH_ID, "check_id": check_id, "result": "PASS" if result else "FAIL", "detail": detail}
        for check_id, result, detail in checks
    ]
    rows.append(
        {
            "same_parent_branch_id": BRANCH_ID,
            "check_id": "VAL1518_13_overall",
            "result": "PASS" if overall else "FAIL",
            "detail": "1518 keeps PiM commutator zero unproved, stages R_eq/I_commutator/MHref intake rows, and selects observed coframe/tau lock"
            if overall
            else "1518 validation failed; inspect failed rows before continuing",
        }
    )
    return rows


def md_table(rows: list[dict[str, Any]], columns: list[str]) -> str:
    output = ["| " + " | ".join(columns) + " |", "| " + " | ".join("---" for _ in columns) + " |"]
    for row in rows:
        output.append("| " + " | ".join(str(row.get(column, "")).replace("\n", " ").replace("|", "\\|") for column in columns) + " |")
    return "\n".join(output)


def write_doc(
    audit: list[dict[str, Any]],
    contract: list[dict[str, Any]],
    source_rows: list[dict[str, Any]],
    obstructions: list[dict[str, Any]],
    mhref: list[dict[str, Any]],
    rejections: list[dict[str, Any]],
    decisions: list[dict[str, Any]],
    local_rows: list[dict[str, Any]],
    validation: list[dict[str, Any]],
    next_rows: list[dict[str, Any]],
) -> None:
    DOC.write_text(
        "\n".join(
            [
                "# 1518 - Parent PiM Commutator Zero Theorem or R_eq/I_commutator Source Acquisition",
                "",
                "## Verdict",
                "- The fixed-topological chain-map route is mathematically real, but current MTS does not parent-sign the selector, fixed domain, physical-current membership, exterior silence, or tau/M_H_ref clauses.",
                "- Therefore [d,Pi_M]J_H=0 is not claimed; R_eq_integral and I_commutator stay as explicit nonclaim source-acquisition rows.",
                "- The parent selector action can be written as a contract, but it remains auxiliary closure machinery unless derived from the parent theory and shown no-stress.",
                "- The next sharp target is one observed coframe plus tau/source/charge/readout lock, because M_H_ref is now the denominator bottleneck for the commutator runner.",
                "",
                "## Commutator Zero Audit",
                md_table(audit, ["audit_id", "claim_piece", "current_status", "failure_if_missing"]),
                "",
                "## Fixed Chainmap Contract",
                md_table(contract, ["contract_id", "parent_requirement", "current_status", "evidence_needed"]),
                "",
                "## Source Acquisition Rows",
                md_table(source_rows, ["row_id", "quantity", "current_status", "required_input"]),
                "",
                "## Selector Obstruction Ledger",
                md_table(obstructions, ["obstruction_id", "obstruction", "current_status", "repair"]),
                "",
                "## MHref / Surface Lock",
                md_table(mhref, ["lock_id", "quantity", "current_status", "required_columns"]),
                "",
                "## Rejection Ledger",
                md_table(rejections, ["rejection_id", "shortcut", "status", "reason"]),
                "",
                "## Decision",
                md_table(decisions, ["decision_id", "decision", "result"]),
                "",
                "## Local GR / Newton Status",
                md_table(local_rows, ["status_id", "claim", "current_status", "reason"]),
                "",
                "## Validation",
                md_table(validation, ["check_id", "result", "detail"]),
                "",
                "## Next Target",
                md_table(next_rows, ["next_id", "next_target", "script", "objective"]),
                "",
            ]
        ),
        encoding="utf-8",
    )


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    audit = commutator_audit_rows()
    contract = chainmap_contract_rows()
    source_rows = source_acquisition_rows()
    obstructions = selector_obstruction_rows()
    mhref = mhref_surface_rows()
    rejections = rejection_rows()
    decisions = decision_rows()
    local_rows = local_status_rows()
    next_rows = next_target_rows()

    write_csv(COMMUTATOR_AUDIT, audit)
    write_csv(CHAINMAP_CONTRACT, contract)
    write_csv(SOURCE_ACQUISITION, source_rows)
    write_csv(SELECTOR_OBSTRUCTION, obstructions)
    write_csv(MHREF_SURFACE_LOCK, mhref)
    write_csv(REJECTION_LEDGER, rejections)
    write_csv(DECISION, decisions)
    write_csv(LOCAL_STATUS, local_rows)
    write_csv(NEXT_TARGET, next_rows)
    copy_outputs()
    remove_pycache()

    generated_csvs = [
        COMMUTATOR_AUDIT,
        CHAINMAP_CONTRACT,
        SOURCE_ACQUISITION,
        SELECTOR_OBSTRUCTION,
        MHREF_SURFACE_LOCK,
        REJECTION_LEDGER,
        DECISION,
        LOCAL_STATUS,
        NEXT_TARGET,
    ]
    validation = validation_rows(generated_csvs)
    write_csv(VALIDATION, validation)
    write_doc(audit, contract, source_rows, obstructions, mhref, rejections, decisions, local_rows, validation, next_rows)


if __name__ == "__main__":
    main()

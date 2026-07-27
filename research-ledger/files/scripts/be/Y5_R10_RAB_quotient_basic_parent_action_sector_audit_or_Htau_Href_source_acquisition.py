from __future__ import annotations

import csv
from pathlib import Path


PACK_ID = "P8_Y5_R10_1364"
TITLE = "1364-Y5-R10-RAB-quotient-basic-parent-action-sector-audit-or-Htau-Href-source-acquisition"
ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = ROOT / "source-intake" / "mts_residuals"
DOC_PATH = ROOT / f"{TITLE}.md"
FORMALIZATION = ROOT.parent / "formalization-workbench"

SOURCE_REGISTER_PATH = OUT_DIR / f"{PACK_ID}_SOURCE_REGISTER.csv"
SECTOR_AUDIT_PATH = OUT_DIR / f"{PACK_ID}_QUOTIENT_BASIC_SECTOR_AUDIT.csv"
ACQUISITION_PATH = OUT_DIR / f"{PACK_ID}_HTAU_HREF_SOURCE_ACQUISITION_LEDGER.csv"
CLAIM_GATE_PATH = OUT_DIR / f"{PACK_ID}_CLAIM_GATE.csv"
DECISION_PATH = OUT_DIR / f"{PACK_ID}_DECISION_LEDGER.csv"
NEXT_PATH = OUT_DIR / f"{PACK_ID}_NEXT_TARGET.csv"
VALIDATION_PATH = OUT_DIR / "P8_Y5_BRR545_1364_VALIDATION.csv"


def source_path(relative_path: str) -> Path:
    path = Path(relative_path)
    if path.is_absolute():
        return path
    return ROOT / path


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def write_csv(path: Path, rows: list[dict[str, object]], fieldnames: list[str] | None = None) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if fieldnames is None:
        fieldnames = []
        for row in rows:
            for key in row:
                if key not in fieldnames:
                    fieldnames.append(key)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def table(headers: list[str], rows: list[dict[str, object]]) -> str:
    out = [
        "| " + " | ".join(headers) + " |",
        "| " + " | ".join(["---"] * len(headers)) + " |",
    ]
    for row in rows:
        out.append("| " + " | ".join(str(row.get(header, "")).replace("\n", " ") for header in headers) + " |")
    return "\n".join(out)


def mark_nonclaim(rows: list[dict[str, object]]) -> list[dict[str, object]]:
    for row in rows:
        row["valid_for_claim"] = False
        row["claim_allowed"] = False
    return rows


def source_register() -> list[dict[str, object]]:
    rows = [
        {
            "source_id": "SRC1364_0_1363_doc",
            "source_path": "1363-Y5-R10-RAB-parent-qObs-current-chain-bridge-or-Htau-Href-first-source-row.md",
            "required_anchor": "NEXT1363_0_1364",
            "purpose": "1363 handoff to quotient-basic parent-action sector audit.",
        },
        {
            "source_id": "SRC1364_1_1363_next",
            "source_path": "source-intake/mts_residuals/P8_Y5_R10_1363_NEXT_TARGET.csv",
            "required_anchor": "NEXT1363_0_1364",
            "purpose": "machine-readable 1364 target.",
        },
        {
            "source_id": "SRC1364_2_1363_bridge",
            "source_path": "source-intake/mts_residuals/P8_Y5_R10_1363_QOBS_CURRENT_CHAIN_BRIDGE_ATTEMPT.csv",
            "required_anchor": "BTA1363_7_verdict",
            "purpose": "bridge theorem remains conditional, not promoted.",
        },
        {
            "source_id": "SRC1364_3_1363_first_source_row",
            "source_path": "source-intake/mts_residuals/P8_Y5_R10_1363_HTAU_HREF_FIRST_SOURCE_ROW.csv",
            "required_anchor": "HFR1363_0_first_source_row",
            "purpose": "guarded H_tau/H_ref first source row template.",
        },
        {
            "source_id": "SRC1364_4_1009_doc",
            "source_path": "1009-Y5-R10-parent-current-chain-action-contract-or-sector-variation-runner.md",
            "required_anchor": "PCS1009_9_total_parent_contract",
            "purpose": "parent current-chain sector contract.",
        },
        {
            "source_id": "SRC1364_5_1009_sector_contract",
            "source_path": "source-intake/mts_residuals/P8_Y5_R10_1009_PARENT_SECTOR_CONTRACT.csv",
            "required_anchor": "PCS1009_9_total_parent_contract",
            "purpose": "all retained sector statuses.",
        },
        {
            "source_id": "SRC1364_6_1009_runner",
            "source_path": "source-intake/mts_residuals/P8_Y5_R10_1009_SECTOR_VARIATION_RUNNER.csv",
            "required_anchor": "SVR1009_6_total_parent_switch_unsigned",
            "purpose": "runner refusals for sector/current-chain shortcuts.",
        },
        {
            "source_id": "SRC1364_7_1009_claim_gate",
            "source_path": "source-intake/mts_residuals/P8_Y5_R10_1009_CLAIM_GATE.csv",
            "required_anchor": "CG1009_0_total_parent_action",
            "purpose": "current-chain claim gates stay blocked.",
        },
        {
            "source_id": "SRC1364_8_1010_doc",
            "source_path": "1010-Y5-R10-Gamma-Khat-action-existence-Helmholtz-or-q_loc-residual-retention.md",
            "required_anchor": "GKT1010_6_verdict",
            "purpose": "Gamma/Khat action-existence route not closed.",
        },
        {
            "source_id": "SRC1364_9_1010_residuals",
            "source_path": "source-intake/mts_residuals/P8_Y5_R10_1010_RESIDUAL_RETENTION_LEDGER.csv",
            "required_anchor": "QRES1010_0_q_loc_vector",
            "purpose": "q_loc retained residual and observable map.",
        },
        {
            "source_id": "SRC1364_10_1008_variation",
            "source_path": "source-intake/mts_residuals/P8_Y5_R10_1008_PARENT_VARIATION_AUDIT.csv",
            "required_anchor": "PVA1008_6_verdict",
            "purpose": "theta/Q_tau parent variation extraction not accepted.",
        },
        {
            "source_id": "SRC1364_11_1008_piece_ledger",
            "source_path": "source-intake/mts_residuals/P8_Y5_R10_1008_CHARGE_PIECE_LEDGER.csv",
            "required_anchor": "QTA1008_8_Q_total",
            "purpose": "charge piece total is not promoted.",
        },
        {
            "source_id": "SRC1364_12_1007_symplectic_schema",
            "source_path": "source-intake/mts_residuals/P8_Y5_R10_1007_SYMPLECTIC_RESIDUAL_SCHEMA.csv",
            "required_anchor": "SRS1007_0_integrability_formula",
            "purpose": "H_tau integrability source requirements.",
        },
    ]
    for row in rows:
        path = source_path(str(row["source_path"]))
        row["exists"] = path.exists()
        row["anchor_found"] = path.exists() and str(row["required_anchor"]) in read_text(path)
    return mark_nonclaim(rows)


def sector_audit_rows() -> list[dict[str, object]]:
    return mark_nonclaim(
        [
            {
                "audit_id": "QBA1364_0_EH_core",
                "sector_id": "PCS1009_0_EH_core",
                "sector": "EH reference geometry",
                "q_basic_L": "CONDITIONAL_IF_g_obs_EQUALS_Obs_e(q)",
                "theta_owned": "REFERENCE_ONLY_theta_EH",
                "Q_tau_owned": "REFERENCE_ONLY_Q_EH",
                "tau_owned": "NOT_FULL_PARENT_TAU",
                "boundary_reference_owned": "FIXED_LAMBDA_KAPPA_SUBTRACTION_MISSING",
                "source_glue_owned": "NOT_TOTAL_SOURCE_GLUE",
                "status": "REFERENCE_ANCHOR_ONLY",
                "blocker": "EH can set the GR comparison shape, but cannot stand in for total MTS parent action.",
                "next_evidence": "parent reduction showing all non-EH sectors are zero/topological/bounded, not absent by assumption",
            },
            {
                "audit_id": "QBA1364_1_kappa_topological",
                "sector_id": "PCS1009_1_kappa_topological",
                "sector": "kappa/topological branch",
                "q_basic_L": "NOT_ADOPTED",
                "theta_owned": "MISSING_A3_KAPPA_VARIATION",
                "Q_tau_owned": "MISSING_TOPOLOGICAL_CHARGE_LEVEL",
                "tau_owned": "MISSING",
                "boundary_reference_owned": "BOUNDARY_LEVEL_CONVENTION_MISSING",
                "source_glue_owned": "NO_SOURCE_SPECIES_DOMAIN_CERTIFICATE",
                "status": "CANDIDATE_NOT_ADOPTED",
                "blocker": "topological kappa candidate has not been accepted as a parent sector.",
                "next_evidence": "adoption decision plus A_3/kappa_eff variation and boundary level source",
            },
            {
                "audit_id": "QBA1364_2_universal_matter",
                "sector_id": "PCS1009_2_universal_matter",
                "sector": "ordinary matter / universal coupling",
                "q_basic_L": "CONDITIONAL_IF_COFRAME_AND_CONSTANTS_DESCEND",
                "theta_owned": "MATTER_THETA_NOT_PARENT_SIGNED",
                "Q_tau_owned": "MATTER_SOURCE_CHARGE_NOT_GLUED",
                "tau_owned": "CLOCK_SOURCE_TAU_LOCK_MISSING",
                "boundary_reference_owned": "NA_OR_SOURCE_BOUNDARY_UNSIGNED",
                "source_glue_owned": "HILBERT_CURRENT_EQUALITY_UNSIGNED",
                "status": "CONDITIONAL_SOURCE_INPUT",
                "blocker": "masses, charges, clocks, material labels, and Hilbert/source equality can still leak representative dependence.",
                "next_evidence": "quotient-owned theta_A/constants and worldtube Hilbert-source equality source",
            },
            {
                "audit_id": "QBA1364_3_boundary_reference",
                "sector_id": "PCS1009_3_boundary_reference",
                "sector": "boundary/reference/counterterm",
                "q_basic_L": "MISSING_FIXED_BASIC_BOUNDARY_TERM",
                "theta_owned": "THETA_BOUNDARY_NOT_FIXED",
                "Q_tau_owned": "Q_BOUNDARY_NOT_PARENT_FIXED",
                "tau_owned": "BOUNDARY_TAU_ACTION_MISSING",
                "boundary_reference_owned": "FIXED_BEFORE_READOUT_MISSING",
                "source_glue_owned": "REFERENCE_CAN_ABSORB_NORMALIZATION",
                "status": "FIXED_REFERENCE_MISSING",
                "blocker": "H_ref is not yet fixed before readout; counterterm ambiguity can hide residuals.",
                "next_evidence": "source-backed fixed reference selector and no-fitted-counterterm certificate",
            },
            {
                "audit_id": "QBA1364_4_Gamma_Khat_extra",
                "sector_id": "PCS1009_4_Gamma_Khat_extra",
                "sector": "Gamma_eff/K_hat/q_loc extra sector",
                "q_basic_L": "MISSING_S_GK",
                "theta_owned": "MISSING_THETA_GK",
                "Q_tau_owned": "MISSING_Q_GK",
                "tau_owned": "MISSING_TAU_ACTION_ON_GK_FIELDS",
                "boundary_reference_owned": "NO_FLUX_BOUNDARY_MISSING",
                "source_glue_owned": "Q_LOC_RETAINED",
                "status": "HARD_FAIL_ACTION_NOT_PROVED",
                "blocker": "q_loc remains retained because S_GK, metric-response identity, Helmholtz symmetry, Euler double-zero, and no-flux are not proved.",
                "next_evidence": "derive q-basic S_GK or source q_loc bound row",
            },
            {
                "audit_id": "QBA1364_5_domain_projector_selector",
                "sector_id": "PCS1009_5_domain_projector_selector",
                "sector": "domain/projector selector",
                "q_basic_L": "PARTIAL_SELECTOR_CLAUSE_ONLY",
                "theta_owned": "MISSING_SELECTOR_THETA",
                "Q_tau_owned": "MISSING_SELECTOR_Q",
                "tau_owned": "MISSING",
                "boundary_reference_owned": "BOUNDARY_NO_FLUX_MISSING",
                "source_glue_owned": "LOCAL_FLRW_BRANCH_RULE_UNSIGNED",
                "status": "PARTIAL_NOT_PARENT_CLOSED",
                "blocker": "selector stress and boundary/domain dependence are not eliminated by parent equations.",
                "next_evidence": "Euler/topological selector action with stress/no-flux accounting",
            },
            {
                "audit_id": "QBA1364_6_mass_projector_PiM",
                "sector_id": "PCS1009_6_mass_projector_PiM",
                "sector": "mass projector Pi_M / source measure",
                "q_basic_L": "MISSING_PARENT_PROJECTOR_ACTION",
                "theta_owned": "MISSING_PROJECTOR_THETA",
                "Q_tau_owned": "MISSING_PROJECTOR_Q",
                "tau_owned": "MISSING",
                "boundary_reference_owned": "SYMPLECTIC_BOUNDARY_METRIC_UNSIGNED",
                "source_glue_owned": "I_COMMUTATOR_RETAINED",
                "status": "NOT_PARENT_DERIVED",
                "blocker": "Pi_M chain map, commutator, variation, and measured-GM calibration are not parent-derived.",
                "next_evidence": "parent symplectic projector derivation or explicit I_commutator source profile",
            },
            {
                "audit_id": "QBA1364_7_memory_response_doublet",
                "sector_id": "PCS1009_7_memory_response_doublet",
                "sector": "memory/response doublet",
                "q_basic_L": "PARTIAL_RESPONSE_CANDIDATE",
                "theta_owned": "MISSING_RESPONSE_THETA",
                "Q_tau_owned": "MISSING_RESPONSE_Q",
                "tau_owned": "MISSING",
                "boundary_reference_owned": "NO_FLUX_MISSING",
                "source_glue_owned": "LOCAL_DOUBLE_ZERO_NOT_PARENT_SIGNED",
                "status": "PARTIAL_NOT_MATCHED",
                "blocker": "response doublet does not yet produce a parent-signed local double-zero with cosmological activation.",
                "next_evidence": "complete component map, positive operator, odd-source zero, PPN lock, and boundary no-flux",
            },
            {
                "audit_id": "QBA1364_8_worldtube_source_glue",
                "sector_id": "PCS1009_8_worldtube_source_glue",
                "sector": "worldtube/source matching",
                "q_basic_L": "MISSING_SOURCE_GLUE_ACTION",
                "theta_owned": "MISSING_SOURCE_GLUE_THETA",
                "Q_tau_owned": "CONDITIONAL_SOURCE_Q_NOT_GLUED",
                "tau_owned": "SOURCE_TAU_LOCK_MISSING",
                "boundary_reference_owned": "EXTERIOR_CLOSURE_MISSING",
                "source_glue_owned": "R_EQ_RETAINED",
                "status": "CORE_MISSING_PIECE",
                "blocker": "M_source[W] = int_S Q_M[tau] is not proved before orbital fitting.",
                "next_evidence": "parent Noether identity, exterior closure, worldtube matching, and Poisson/Newton calibration",
            },
            {
                "audit_id": "QBA1364_9_total_parent_contract",
                "sector_id": "PCS1009_9_total_parent_contract",
                "sector": "total parent action",
                "q_basic_L": "NOT_PROMOTED",
                "theta_owned": "NOT_EXTRACTED",
                "Q_tau_owned": "NOT_EXTRACTED",
                "tau_owned": "NOT_OWNED",
                "boundary_reference_owned": "NOT_FIXED",
                "source_glue_owned": "NOT_GLUED",
                "status": "TOTAL_NOT_PROMOTED",
                "blocker": "every retained sector must pass before S_parent can be claimed.",
                "next_evidence": "complete sector table with source paths, variation equations, theta/Q contributions, boundary/tau certificates",
            },
        ]
    )


def acquisition_rows() -> list[dict[str, object]]:
    return mark_nonclaim(
        [
            {
                "acquisition_id": "ACQ1364_0_q_basic_sector_table",
                "target": "q-basic parent sector table",
                "needed_for": "BTA1363_0;QBA1364_9_total_parent_contract",
                "required_fields": "sector_id;L_sector_source;parent_fields;q_map;equivalence_relation;L_sector=Lbar(q)+dB_basic proof;source_path;source_anchor",
                "current_value": "MISSING_Q_BASIC_SECTOR_PROOFS",
                "anti_shortcut": "no total-parent switch without every retained sector row",
                "status": "MISSING_SOURCE_EQUATION",
            },
            {
                "acquisition_id": "ACQ1364_1_theta_Qtau_piece_table",
                "target": "theta_MTS/Q_tau^MTS piece table",
                "needed_for": "H_tau;M_H_ref;local_GR",
                "required_fields": "sector_id;theta_sector;Q_tau_sector;constraint_C_tau;boundary_improvement;units;source_path;source_anchor",
                "current_value": "MISSING_THETA_QTAU_PIECES",
                "anti_shortcut": "EH theta/Q_tau is reference-only until MTS reduction signs silent sectors",
                "status": "MISSING_SOURCE_EQUATION",
            },
            {
                "acquisition_id": "ACQ1364_2_tau_generator_lock",
                "target": "tau_obs(q) generator",
                "needed_for": "H_tau same-frame charge;clock/source/orbit consistency",
                "required_fields": "tau_id;definition_on_Q_obs;Lie_tau_on_each_sector;clock_source_orbit_boundary_lock;source_path;source_anchor",
                "current_value": "MISSING_TAU_OBS_Q",
                "anti_shortcut": "no post-readout frame/tau choice",
                "status": "MISSING_SOURCE_EQUATION",
            },
            {
                "acquisition_id": "ACQ1364_3_fixed_Href_reference",
                "target": "H_ref fixed reference/counterterm",
                "needed_for": "M_H_ref denominator",
                "required_fields": "reference_selector;counterterm_policy;fixed_before_readout_certificate;H_ref;units;source_path;source_anchor",
                "current_value": "MISSING_FIXED_H_REF",
                "anti_shortcut": "no fitted counterterm; no reference-only 1",
                "status": "MISSING_SOURCE_INPUT",
            },
            {
                "acquisition_id": "ACQ1364_4_Htau_surface_charge",
                "target": "H_tau surface charge",
                "needed_for": "M_H_ref denominator",
                "required_fields": "surface_outer;coframe_id;tau_id;theta_source;Q_tau_source;H_tau;units;integrability_certificate;source_path;source_anchor",
                "current_value": "MISSING_H_TAU",
                "anti_shortcut": "no orbital GM; no bare mass; no EH-only import",
                "status": "MISSING_SOURCE_INPUT",
            },
            {
                "acquisition_id": "ACQ1364_5_GK_q_loc_source_or_zero",
                "target": "Gamma/Khat q_loc sector",
                "needed_for": "local PPN/local GR",
                "required_fields": "S_GK_source_or_q_loc_profile;Gamma_formula;Khat_formula;Helmholtz_check;Euler_double_zero;boundary_no_flux;units;observable_map",
                "current_value": "QRES1010_0_q_loc_vector_RETAINED",
                "anti_shortcut": "no plateau axiom; no bookkeeping stress",
                "status": "MISSING_DERIVATION_OR_BOUND",
            },
            {
                "acquisition_id": "ACQ1364_6_PiM_worldtube_source_glue",
                "target": "Pi_M/worldtube/source equality",
                "needed_for": "source mass denominator and Poisson/Newton bridge",
                "required_fields": "Pi_M_parent_origin;commutator_profile;R_eq_integral;B_zero_flux;worldtube_matching;source_path;source_anchor",
                "current_value": "MISSING_CHAINMAP_SOURCE_EQUALITY",
                "anti_shortcut": "no measured orbital GM until Poisson/Gauss bridge is derived",
                "status": "MISSING_SOURCE_EQUATION",
            },
            {
                "acquisition_id": "ACQ1364_7_matter_constant_coupling_descent",
                "target": "matter constants and coupling quotient ownership",
                "needed_for": "WEP/clock/source normalization",
                "required_fields": "theta_A_constants;mass_charge_clock_descent;material_label_rule;no_species_extra_coupling;source_path;source_anchor",
                "current_value": "MISSING_MATTER_CONSTANT_DESCENT",
                "anti_shortcut": "no assumption that metric coframe descent alone proves universal coupling",
                "status": "MISSING_SOURCE_EQUATION",
            },
            {
                "acquisition_id": "ACQ1364_8_acceptance_gate",
                "target": "H_tau/H_ref acquisition promotion",
                "needed_for": "reopen M_H_ref/local GR gates",
                "required_fields": "ACQ1364_0 through ACQ1364_7 all source-backed with no MISSING markers and compatible units",
                "current_value": "CLAIM_BLOCKED",
                "anti_shortcut": "all anti-circularity flags must remain true",
                "status": "CLAIM_BLOCKED",
            },
        ]
    )


def claim_gates() -> list[dict[str, object]]:
    return mark_nonclaim(
        [
            {
                "gate_id": "GATE1364_0_all_sectors_q_basic",
                "claim": "every retained parent sector is q-basic and current-chain owned",
                "gate_pass": False,
                "reason": "no audited sector reaches claimable q-basic/current-owned status; total parent contract is not promoted.",
            },
            {
                "gate_id": "GATE1364_1_EH_total_action_shortcut",
                "claim": "EH reference geometry can stand in for total MTS parent action",
                "gate_pass": False,
                "reason": "EH is only a reference anchor unless all non-EH sectors are reduced, zero, topological, or source-bounded.",
            },
            {
                "gate_id": "GATE1364_2_Htau_Href_acquisition_ready",
                "claim": "H_tau/H_ref source-acquisition rows are ready to score",
                "gate_pass": False,
                "reason": "all source/equation rows remain missing or blocked.",
            },
            {
                "gate_id": "GATE1364_3_GK_next_priority",
                "claim": "Gamma/Khat q_loc local sector is the next hard local-GR blocker",
                "gate_pass": True,
                "reason": "it is the first hard-fail sector with direct PPN/local force observable map.",
            },
            {
                "gate_id": "GATE1364_4_local_GR_reopen",
                "claim": "local-GR/PPN/Newton gates can reopen",
                "gate_pass": False,
                "reason": "q-basic sector ownership, H_tau/H_ref, q_loc, Pi_M/source equality, and matter coupling remain open.",
            },
        ]
    )


def decision_rows() -> list[dict[str, object]]:
    return mark_nonclaim(
        [
            {
                "decision_id": "DEC1364_0_sector_audit_blocks_total_parent_action",
                "decision": "Do not promote S_parent or the qObs-current-chain bridge.",
                "why": "sector audit shows every retained nontrivial sector still lacks q-basic/current-chain ownership.",
                "next_action": "repair one hard sector at a time, beginning with the local-force Gamma/Khat branch.",
            },
            {
                "decision_id": "DEC1364_1_EH_anchor_is_useful_not_sufficient",
                "decision": "Keep EH as comparison shape only.",
                "why": "this protects the GR limit from circular import while preserving the right target form.",
                "next_action": "require explicit MTS reduction/silence/bound rows before using EH charge as H_tau evidence.",
            },
            {
                "decision_id": "DEC1364_2_acquisition_ledger_replaces_handwaving",
                "decision": "Use acquisition rows as the only route to H_tau/H_ref scoring.",
                "why": "they name the exact missing equations, source paths, units, and anti-circularity certificates.",
                "next_action": "source or derive the highest-impact missing row rather than broadening claims.",
            },
        ]
    )


def next_rows() -> list[dict[str, object]]:
    return mark_nonclaim(
        [
            {
                "next_id": "NEXT1364_0_1365",
                "target_file": "1365-Y5-R10-RAB-Gamma-Khat-qbasic-sector-repair-or-q_loc-bound-source-row.md",
                "target_script": "scripts/Y5_R10_RAB_Gamma_Khat_qbasic_sector_repair_or_q_loc_bound_source_row.py",
                "task": "attempt the Gamma/Khat q-basic sector repair: construct S_GK on Q_obs with metric response, Helmholtz, Euler double-zero, and boundary no-flux; if not, fill a nonclaim q_loc bound/source row",
                "success_condition": "either S_GK is q-basic/current-owned with theta/Q_tau contribution, or q_loc has a source-ready bound row with units, observable map, and missing inputs explicit",
                "do_not": "do not use plateau axiom, bookkeeping stress, EH-only import, fitted cancellation, local-GR claim, formalization-workbench edits, or GitHub action",
            }
        ]
    )


def validate_outputs(
    sources: list[dict[str, object]],
    sectors: list[dict[str, object]],
    acquisitions: list[dict[str, object]],
    gates: list[dict[str, object]],
    decisions: list[dict[str, object]],
    next_target: list[dict[str, object]],
) -> list[dict[str, object]]:
    validations: list[dict[str, object]] = []

    def add(check_id: str, check: str, passed: bool, details: str) -> None:
        validations.append(
            {
                "check_id": check_id,
                "check": check,
                "status": "PASS" if passed else "FAIL",
                "details": details,
            }
        )

    add(
        "VAL1364_0_sources_exist",
        "registered source paths exist and anchors are found",
        all(bool(row["exists"]) and bool(row["anchor_found"]) for row in sources),
        ";".join(f"{row['source_id']}={row['exists']}/{row['anchor_found']}" for row in sources),
    )

    required_sector_ids = {
        "PCS1009_0_EH_core",
        "PCS1009_1_kappa_topological",
        "PCS1009_2_universal_matter",
        "PCS1009_3_boundary_reference",
        "PCS1009_4_Gamma_Khat_extra",
        "PCS1009_5_domain_projector_selector",
        "PCS1009_6_mass_projector_PiM",
        "PCS1009_7_memory_response_doublet",
        "PCS1009_8_worldtube_source_glue",
        "PCS1009_9_total_parent_contract",
    }
    add(
        "VAL1364_1_sector_audit_complete",
        "sector audit covers all retained parent-action sectors",
        required_sector_ids.issubset({str(row["sector_id"]) for row in sectors}),
        f"sector_rows={len(sectors)}",
    )

    add(
        "VAL1364_2_no_sector_promoted",
        "no sector is promoted as q-basic/current-owned claim evidence",
        all(not row["claim_allowed"] and str(row["status"]) not in {"PASS", "CLAIM_READY", "Q_BASIC_CURRENT_OWNED"} for row in sectors),
        ";".join(f"{row['sector_id']}={row['status']}" for row in sectors),
    )

    gk = next(row for row in sectors if row["sector_id"] == "PCS1009_4_Gamma_Khat_extra")
    add(
        "VAL1364_3_GK_hard_blocker_identified",
        "Gamma/Khat q_loc sector is identified as hard local-force blocker",
        str(gk["status"]) == "HARD_FAIL_ACTION_NOT_PROVED" and "q_loc" in str(gk["blocker"]),
        str(gk["next_evidence"]),
    )

    required_acq = {f"ACQ1364_{idx}_{suffix}" for idx, suffix in [
        (0, "q_basic_sector_table"),
        (1, "theta_Qtau_piece_table"),
        (2, "tau_generator_lock"),
        (3, "fixed_Href_reference"),
        (4, "Htau_surface_charge"),
        (5, "GK_q_loc_source_or_zero"),
        (6, "PiM_worldtube_source_glue"),
        (7, "matter_constant_coupling_descent"),
        (8, "acceptance_gate"),
    ]}
    add(
        "VAL1364_4_acquisition_ledger_complete",
        "H_tau/H_ref source-acquisition ledger covers sector proofs, charge pieces, tau, reference, surface charge, q_loc, PiM/source, and matter coupling",
        required_acq.issubset({str(row["acquisition_id"]) for row in acquisitions}),
        f"acquisition_rows={len(acquisitions)}",
    )

    add(
        "VAL1364_5_acquisitions_nonclaim_missing",
        "acquisition rows remain missing or blocked rather than scored",
        all(not row["claim_allowed"] and str(row["status"]) in {"MISSING_SOURCE_EQUATION", "MISSING_SOURCE_INPUT", "MISSING_DERIVATION_OR_BOUND", "CLAIM_BLOCKED"} for row in acquisitions),
        ";".join(f"{row['acquisition_id']}={row['status']}" for row in acquisitions),
    )

    add(
        "VAL1364_6_claim_gates_block_claim",
        "claim gates block q-basic action, EH shortcut, acquisition scoring, and local-GR claims",
        all((row["gate_pass"] is False or row["gate_id"] == "GATE1364_3_GK_next_priority") and not row["claim_allowed"] for row in gates),
        ";".join(f"{row['gate_id']}={row['gate_pass']}" for row in gates),
    )

    all_rows = sources + sectors + acquisitions + gates + decisions + next_target
    add(
        "VAL1364_7_nonclaim_policy",
        "all generated rows remain nonclaim",
        all(not row.get("valid_for_claim", False) and not row.get("claim_allowed", False) for row in all_rows),
        "valid_for_claim=false and claim_allowed=false across generated rows",
    )

    formalization_hits: list[Path] = []
    if FORMALIZATION.exists():
        for pattern in ("*P8_Y5_R10_1364*", "*1364-Y5-R10-RAB-quotient-basic-parent-action*", "*Y5_R10_RAB_quotient_basic_parent_action*"):
            formalization_hits.extend(FORMALIZATION.rglob(pattern))
    add(
        "VAL1364_8_formalization_untouched",
        "formalization-workbench untouched by generated outputs",
        len(formalization_hits) == 0,
        f"formalization_generated_output_count={len(formalization_hits)}",
    )

    add(
        "VAL1364_9_next_target_1365",
        "next target routes to Gamma/Khat q-basic repair or q_loc bound row",
        bool(next_target) and str(next_target[0]["target_file"]).startswith("1365-Y5-R10-RAB-Gamma-Khat-qbasic-sector-repair"),
        str(next_target[0]["target_file"]) if next_target else "missing",
    )

    add(
        "VAL1364_10_overall",
        "overall 1364 validation",
        all(row["status"] == "PASS" for row in validations),
        "1364 blocks total parent action promotion and selects Gamma/Khat q_loc repair as next hard local-GR target",
    )

    return validations


def build_doc(
    sources: list[dict[str, object]],
    sectors: list[dict[str, object]],
    acquisitions: list[dict[str, object]],
    gates: list[dict[str, object]],
    decisions: list[dict[str, object]],
    next_target: list[dict[str, object]],
    validations: list[dict[str, object]],
) -> str:
    return "\n\n".join(
        [
            f"# {TITLE}",
            "**Current verdict:** 1364 does not find a claimable q-basic total parent action. EH remains a useful GR reference anchor, but the retained MTS sectors are not yet jointly quotient-basic, current-chain owned, tau-locked, and reference-fixed.",
            "**Main progress:** the local-GR bridge is now decomposed by sector. The first hard local blocker is the `Gamma_eff/K_hat/q_loc` sector because it has a direct PPN/local-force observable map and no accepted `S_GK`, metric-response identity, Helmholtz proof, Euler double-zero, or no-flux certificate.",
            "## Source register",
            table(["source_id", "source_path", "exists", "anchor_found", "purpose"], sources),
            "## Quotient-basic sector audit",
            table(
                [
                    "audit_id",
                    "sector_id",
                    "sector",
                    "q_basic_L",
                    "theta_owned",
                    "Q_tau_owned",
                    "tau_owned",
                    "boundary_reference_owned",
                    "source_glue_owned",
                    "status",
                    "blocker",
                    "next_evidence",
                ],
                sectors,
            ),
            "## Htau/Href source-acquisition ledger",
            table(["acquisition_id", "target", "needed_for", "required_fields", "current_value", "anti_shortcut", "status"], acquisitions),
            "## Claim gates",
            table(["gate_id", "claim", "gate_pass", "reason", "claim_allowed"], gates),
            "## Decision ledger",
            table(["decision_id", "decision", "why", "next_action"], decisions),
            "## Next target",
            table(["next_id", "target_file", "target_script", "task", "success_condition", "do_not"], next_target),
            "## Validation",
            table(["check_id", "check", "status", "details"], validations),
        ]
    ) + "\n"


def main() -> None:
    sources = source_register()
    sectors = sector_audit_rows()
    acquisitions = acquisition_rows()
    gates = claim_gates()
    decisions = decision_rows()
    next_target = next_rows()
    validations = validate_outputs(sources, sectors, acquisitions, gates, decisions, next_target)

    write_csv(SOURCE_REGISTER_PATH, sources)
    write_csv(SECTOR_AUDIT_PATH, sectors)
    write_csv(ACQUISITION_PATH, acquisitions)
    write_csv(CLAIM_GATE_PATH, gates)
    write_csv(DECISION_PATH, decisions)
    write_csv(NEXT_PATH, next_target)
    write_csv(VALIDATION_PATH, validations)
    DOC_PATH.write_text(
        build_doc(sources, sectors, acquisitions, gates, decisions, next_target, validations),
        encoding="utf-8",
    )


if __name__ == "__main__":
    main()

from __future__ import annotations

import csv
from pathlib import Path


PACK_ID = "P8_Y5_R10_1363"
TITLE = "1363-Y5-R10-RAB-parent-qObs-current-chain-bridge-or-Htau-Href-first-source-row"
ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = ROOT / "source-intake" / "mts_residuals"
DOC_PATH = ROOT / f"{TITLE}.md"
FORMALIZATION = ROOT.parent / "formalization-workbench"

SOURCE_REGISTER_PATH = OUT_DIR / f"{PACK_ID}_SOURCE_REGISTER.csv"
BRIDGE_ATTEMPT_PATH = OUT_DIR / f"{PACK_ID}_QOBS_CURRENT_CHAIN_BRIDGE_ATTEMPT.csv"
OBSTRUCTION_PATH = OUT_DIR / f"{PACK_ID}_BRIDGE_OBSTRUCTION_LEDGER.csv"
FIRST_SOURCE_ROW_PATH = OUT_DIR / f"{PACK_ID}_HTAU_HREF_FIRST_SOURCE_ROW.csv"
CLAIM_GATE_PATH = OUT_DIR / f"{PACK_ID}_CLAIM_GATE.csv"
DECISION_PATH = OUT_DIR / f"{PACK_ID}_DECISION_LEDGER.csv"
NEXT_PATH = OUT_DIR / f"{PACK_ID}_NEXT_TARGET.csv"
VALIDATION_PATH = OUT_DIR / "P8_Y5_BRR545_1363_VALIDATION.csv"


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
            "source_id": "SRC1363_0_1362_doc",
            "source_path": "1362-Y5-R10-RAB-quotient-observed-coframe-parent-qObs-or-MHref-denominator-source-pack.md",
            "required_anchor": "NEXT1362_0_1363",
            "purpose": "1362 handoff to qObs-current-chain bridge or H_tau/H_ref row.",
        },
        {
            "source_id": "SRC1363_1_1362_next",
            "source_path": "source-intake/mts_residuals/P8_Y5_R10_1362_NEXT_TARGET.csv",
            "required_anchor": "NEXT1362_0_1363",
            "purpose": "machine-readable 1363 target.",
        },
        {
            "source_id": "SRC1363_2_1362_qobs",
            "source_path": "source-intake/mts_residuals/P8_Y5_R10_1362_QOBS_PARENT_CONSTRUCTION_ATTEMPT.csv",
            "required_anchor": "QOA1362_3_chain_rule_zero",
            "purpose": "conditional q/Obs_e vertical-blindness lemma.",
        },
        {
            "source_id": "SRC1363_3_1362_denominator_pack",
            "source_path": "source-intake/mts_residuals/P8_Y5_R10_1362_MHREF_DENOMINATOR_SOURCE_PACK.csv",
            "required_anchor": "DSP1362_0_H_tau",
            "purpose": "strict H_tau/H_ref/M_H_ref denominator requirements.",
        },
        {
            "source_id": "SRC1363_4_1008_doc",
            "source_path": "1008-Y5-R10-parent-theta-Qtau-extraction-or-charge-decomposition-runner.md",
            "required_anchor": "QTA1008_8_Q_total",
            "purpose": "parent theta/Q_tau extraction remains blocked.",
        },
        {
            "source_id": "SRC1363_5_1008_variation",
            "source_path": "source-intake/mts_residuals/P8_Y5_R10_1008_PARENT_VARIATION_AUDIT.csv",
            "required_anchor": "PVA1008_0_parent_action",
            "purpose": "explicit current-chain parent action audit.",
        },
        {
            "source_id": "SRC1363_6_1008_piece_ledger",
            "source_path": "source-intake/mts_residuals/P8_Y5_R10_1008_CHARGE_PIECE_LEDGER.csv",
            "required_anchor": "QTA1008_8_Q_total",
            "purpose": "Q_tau pieces and total charge nonpromotion.",
        },
        {
            "source_id": "SRC1363_7_1009_doc",
            "source_path": "1009-Y5-R10-parent-current-chain-action-contract-or-sector-variation-runner.md",
            "required_anchor": "PCS1009_9_total_parent_contract",
            "purpose": "sector contract for total parent action.",
        },
        {
            "source_id": "SRC1363_8_1009_contract",
            "source_path": "source-intake/mts_residuals/P8_Y5_R10_1009_PARENT_SECTOR_CONTRACT.csv",
            "required_anchor": "PCS1009_9_total_parent_contract",
            "purpose": "retained sector-by-sector parent action status.",
        },
        {
            "source_id": "SRC1363_9_1010_doc",
            "source_path": "1010-Y5-R10-Gamma-Khat-action-existence-Helmholtz-or-q_loc-residual-retention.md",
            "required_anchor": "GKT1010_6_verdict",
            "purpose": "Gamma/Khat/q_loc action route remains retained residual.",
        },
        {
            "source_id": "SRC1363_10_1007_doc",
            "source_path": "1007-Y5-R10-Htau-integrability-fixed-reference-theorem-or-symplectic-residual-row.md",
            "required_anchor": "HTA1007_6_integrability_verdict",
            "purpose": "H_tau integrability and fixed-reference theorem remains blocked.",
        },
        {
            "source_id": "SRC1363_11_1007_symplectic_schema",
            "source_path": "source-intake/mts_residuals/P8_Y5_R10_1007_SYMPLECTIC_RESIDUAL_SCHEMA.csv",
            "required_anchor": "SRS1007_0_integrability_formula",
            "purpose": "strict symplectic/integrability row requirements.",
        },
        {
            "source_id": "SRC1363_12_771_owner_audit",
            "source_path": "source-intake/mts_residuals/P8_Y5_R10_771_THETA_QTAU_CURRENT_OWNER_AUDIT.csv",
            "required_anchor": "TQ771_6_owner_verdict",
            "purpose": "older theta/Q_tau current-owner audit.",
        },
        {
            "source_id": "SRC1363_13_993_decomposition",
            "source_path": "source-intake/mts_residuals/P8_Y5_R10_993_QTAU_DECOMPOSITION_LEDGER.csv",
            "required_anchor": "QDEC993_5_total",
            "purpose": "older Q_tau decomposition ledger.",
        },
    ]
    for row in rows:
        path = source_path(str(row["source_path"]))
        row["exists"] = path.exists()
        row["anchor_found"] = path.exists() and str(row["required_anchor"]) in read_text(path)
    return mark_nonclaim(rows)


def bridge_attempt() -> list[dict[str, object]]:
    return mark_nonclaim(
        [
            {
                "attempt_id": "BTA1363_0_quotient_basic_parent_action",
                "claim_piece": "parent action is quotient-basic",
                "required_form": "S_parent[Phi,psi] = Sbar_parent[q(Phi),psi,theta(q)] + int dB_basic[q]",
                "result": "CONDITIONAL_ROUTE_ONLY",
                "what_would_follow": "vertical representative directions cannot change the bulk parent action or its basic boundary term.",
                "why_not_claim": "1008/1009 show the full current-chain parent action is still a sector contract, not an extracted action.",
            },
            {
                "attempt_id": "BTA1363_1_tau_generator_descends",
                "claim_piece": "observed time generator is quotient-owned",
                "required_form": "tau = tau_obs(q(Phi)) and Lie_tau acts on all metric, matter, representative, boundary, and reference fields before readout",
                "result": "NOT_PARENT_SIGNED",
                "what_would_follow": "the Hamiltonian current is computed in the same frame used by clocks, source, orbit, and boundary.",
                "why_not_claim": "tau/source/charge/clock/boundary roles remain split in 1362 and 771.",
            },
            {
                "attempt_id": "BTA1363_2_symplectic_potential_descends",
                "claim_piece": "theta_MTS descends through q",
                "required_form": "theta_MTS(Phi;delta Phi) = theta_bar(q;Dq delta Phi) + dY_basic(q;delta q)",
                "result": "VALID_CONDITIONAL_LEMMA",
                "what_would_follow": "for v in ker Dq, theta_MTS(Phi;v) is exact/basic and cannot source a local bulk force.",
                "why_not_claim": "theta_extra, theta_projector, theta_boundary, and theta_matter/source are not extracted.",
            },
            {
                "attempt_id": "BTA1363_3_Noether_current_descends",
                "claim_piece": "J_tau descends through q",
                "required_form": "J_tau = theta_MTS(L_tau Phi) - i_tau L_parent = Jbar_tau(q) + dY_tau + C_tau_basic",
                "result": "VALID_CONDITIONAL_LEMMA",
                "what_would_follow": "the current-chain source of H_tau would be quotient-owned rather than representative-owned.",
                "why_not_claim": "J_tau is currently formal-shape only and tau action over all sectors is not owned.",
            },
            {
                "attempt_id": "BTA1363_4_Qtau_charge_descends",
                "claim_piece": "Q_tau^MTS and fixed reference descend through q",
                "required_form": "J_tau = dQ_tau^MTS + C_tau, with Q_tau^MTS = Qbar_tau(q) + Q_ref_fixed(q) + exact",
                "result": "CONDITIONAL_NOT_EXTRACTED",
                "what_would_follow": "H_tau and H_ref could be assigned to one observed coframe/tau frame without EH-only import.",
                "why_not_claim": "Q_boundary, Q_extra, Q_projector, and Q_matter/source remain unowned or conditional.",
            },
            {
                "attempt_id": "BTA1363_5_vertical_Htau_variation_zero",
                "claim_piece": "vertical representative motion cannot change H_tau",
                "required_form": "delta_v H_tau = int_S(delta_v Q_tau^MTS - i_tau theta_MTS(v)) = 0 for all v in ker Dq",
                "result": "VALID_IF_BTA1363_0_TO_4_PASS",
                "what_would_follow": "the local denominator/current chain would not hide a representative coupling leak.",
                "why_not_claim": "the required parent action, tau, theta, Q_tau, and fixed reference clauses are not jointly signed.",
            },
            {
                "attempt_id": "BTA1363_6_sector_failure_map",
                "claim_piece": "all retained MTS sectors are q-basic and current-owned",
                "required_form": "EH, matter, boundary, Gamma/Khat, Pi_M, memory/response, and worldtube/source sectors all supply basic L, theta, Q, and constraints",
                "result": "CURRENT_CORPUS_FAILS",
                "what_would_follow": "the bridge would become a parent current-chain proof instead of a closure template.",
                "why_not_claim": "Gamma/Khat/q_loc, Pi_M commutator, worldtube source glue, boundary reference, and matter constants remain open.",
            },
            {
                "attempt_id": "BTA1363_7_verdict",
                "claim_piece": "parent qObs-current-chain bridge for current MTS",
                "required_form": "BTA1363_0 through BTA1363_6 all parent-signed with source paths and equations",
                "result": "QOBS_CURRENT_CHAIN_BRIDGE_NOT_PROVED",
                "what_would_follow": "H_tau/H_ref/M_H_ref denominator scoring and local-GR gates could reopen.",
                "why_not_claim": "the bridge theorem is exact as a conditional route, but current MTS lacks the parent current-chain construction.",
            },
        ]
    )


def obstruction_rows() -> list[dict[str, object]]:
    return mark_nonclaim(
        [
            {
                "obstruction_id": "BOB1363_0_missing_q_basic_L_parent",
                "obstruction": "no explicit L_parent proved basic with respect to q",
                "blocks": "BTA1363_0",
                "risk": "representative variables can still enter physics through the action.",
                "repair": "write each sector Lagrangian as a function of q(Phi) plus exact/basic terms.",
                "status": "OPEN",
            },
            {
                "obstruction_id": "BOB1363_1_tau_not_quotient_owned",
                "obstruction": "observed tau is not constructed as tau_obs(q)",
                "blocks": "BTA1363_1",
                "risk": "Hamiltonian charge, clocks, source support, and orbit can use different time readouts.",
                "repair": "define tau on Q_obs and prove all sector Lie_tau variations use that tau before readout.",
                "status": "OPEN",
            },
            {
                "obstruction_id": "BOB1363_2_theta_Q_split_missing",
                "obstruction": "theta_MTS and Q_tau^MTS are not extracted for all sectors",
                "blocks": "BTA1363_2;BTA1363_3;BTA1363_4",
                "risk": "EH charge can be accidentally imported as the whole MTS source charge.",
                "repair": "extract theta and Q pieces for boundary, extra, projector, memory, and matter/source sectors.",
                "status": "OPEN",
            },
            {
                "obstruction_id": "BOB1363_3_reference_boundary_not_fixed",
                "obstruction": "H_ref/counterterm policy is not fixed before readout",
                "blocks": "BTA1363_4;HFR1363_0_first_source_row",
                "risk": "reference subtraction could absorb a source normalization residual.",
                "repair": "source a fixed reference selector and counterterm convention independent of fitted residuals.",
                "status": "OPEN",
            },
            {
                "obstruction_id": "BOB1363_4_Gamma_Khat_q_loc_retained",
                "obstruction": "Gamma/Khat/q_loc sector is retained as a residual",
                "blocks": "BTA1363_6",
                "risk": "local force/current leakage survives the current-chain proof.",
                "repair": "derive S_GK with Helmholtz, metric response, Euler double zero, and no-flux clauses, or source q_loc bounds.",
                "status": "OPEN",
            },
            {
                "obstruction_id": "BOB1363_5_PiM_worldtube_source_unsigned",
                "obstruction": "Pi_M commutator and worldtube Hilbert-source equality are not parent-signed",
                "blocks": "BTA1363_6",
                "risk": "the source mass denominator may not equal the parent current charge.",
                "repair": "prove chain-map/source equality or keep I_commutator and R_eq residuals in the denominator pack.",
                "status": "OPEN",
            },
            {
                "obstruction_id": "BOB1363_6_matter_constants_not_q_owned",
                "obstruction": "masses, charge normalization, clock constants, and material labels are not shown to descend through q",
                "blocks": "BTA1363_0;BTA1363_6",
                "risk": "ordinary-coupling leaks can remain even if the metric coframe descends.",
                "repair": "derive quotient-owned theta_A/constants or source explicit WEP/clock/coupling residual rows.",
                "status": "OPEN",
            },
        ]
    )


def first_source_rows() -> list[dict[str, object]]:
    return mark_nonclaim(
        [
            {
                "row_id": "HFR1363_0_first_source_row",
                "row_kind": "H_tau_H_ref_denominator_template",
                "system_id": "LOCAL_SOURCE_TEMPLATE_001",
                "surface_outer": "MISSING_SURFACE_OUTER",
                "surface_reference": "MISSING_REFERENCE_SURFACE_OR_BACKGROUND",
                "coframe_id": "MISSING_COFRAME_ID",
                "tau_id": "MISSING_TAU_ID",
                "boundary_domain_id": "MISSING_BOUNDARY_DOMAIN_ID",
                "theta_source": "MISSING_THETA_MTS_SOURCE",
                "Q_tau_source": "MISSING_Q_TAU_MTS_SOURCE",
                "H_tau": "MISSING_H_TAU",
                "H_tau_units": "MISSING_UNITS",
                "H_ref": "MISSING_H_REF",
                "H_ref_units": "MISSING_UNITS",
                "M_H_ref": "MISSING_M_H_REF",
                "M_H_ref_units": "MISSING_UNITS",
                "reference_policy": "MISSING_FIXED_BEFORE_READOUT_POLICY",
                "fixed_before_readout_certificate": "MISSING_CERTIFICATE",
                "not_orbital_GM": True,
                "not_bare_mass": True,
                "not_reference_only_one": True,
                "not_EH_only_import": True,
                "source_path": "MISSING_SOURCE_PATH",
                "source_anchor": "MISSING_SOURCE_ANCHOR",
                "missing_fields": "surface_outer;surface_reference;coframe_id;tau_id;boundary_domain_id;theta_source;Q_tau_source;H_tau;H_ref;M_H_ref;units;reference_policy;source_path;source_anchor",
                "status": "CLAIM_BLOCKED_SOURCE_ROW_TEMPLATE",
            },
            {
                "row_id": "HFR1363_1_Htau_component",
                "row_kind": "H_tau_component_requirement",
                "system_id": "LOCAL_SOURCE_TEMPLATE_001",
                "surface_outer": "REQUIRED",
                "surface_reference": "NA",
                "coframe_id": "REQUIRED",
                "tau_id": "REQUIRED",
                "boundary_domain_id": "REQUIRED",
                "theta_source": "REQUIRED_PARENT_THETA_MTS",
                "Q_tau_source": "REQUIRED_PARENT_Q_TAU_MTS",
                "H_tau": "FINITE_NUMERIC_REQUIRED",
                "H_tau_units": "ENERGY_OR_MASS_UNITS_REQUIRED",
                "H_ref": "NA",
                "H_ref_units": "NA",
                "M_H_ref": "NA",
                "M_H_ref_units": "NA",
                "reference_policy": "NA",
                "fixed_before_readout_certificate": "NA",
                "not_orbital_GM": True,
                "not_bare_mass": True,
                "not_reference_only_one": True,
                "not_EH_only_import": True,
                "source_path": "MISSING_SOURCE_PATH",
                "source_anchor": "MISSING_SOURCE_ANCHOR",
                "missing_fields": "theta_source;Q_tau_source;H_tau;units;frame/tau/source paths",
                "status": "MISSING_SOURCE_INPUT",
            },
            {
                "row_id": "HFR1363_2_Href_component",
                "row_kind": "H_ref_component_requirement",
                "system_id": "LOCAL_SOURCE_TEMPLATE_001",
                "surface_outer": "NA",
                "surface_reference": "REQUIRED_FIXED_REFERENCE",
                "coframe_id": "REQUIRED",
                "tau_id": "REQUIRED",
                "boundary_domain_id": "REQUIRED",
                "theta_source": "REQUIRED_PARENT_THETA_MTS_OR_FIXED_COUNTERTERM_SOURCE",
                "Q_tau_source": "REQUIRED_PARENT_Q_TAU_MTS_OR_FIXED_COUNTERTERM_SOURCE",
                "H_tau": "NA",
                "H_tau_units": "NA",
                "H_ref": "FINITE_NUMERIC_REQUIRED",
                "H_ref_units": "ENERGY_OR_MASS_UNITS_REQUIRED",
                "M_H_ref": "NA",
                "M_H_ref_units": "NA",
                "reference_policy": "FIXED_BEFORE_READOUT_REQUIRED",
                "fixed_before_readout_certificate": "MISSING_CERTIFICATE",
                "not_orbital_GM": True,
                "not_bare_mass": True,
                "not_reference_only_one": True,
                "not_EH_only_import": True,
                "source_path": "MISSING_SOURCE_PATH",
                "source_anchor": "MISSING_SOURCE_ANCHOR",
                "missing_fields": "H_ref;units;reference_policy;fixed_before_readout_certificate;source_path",
                "status": "MISSING_SOURCE_INPUT",
            },
            {
                "row_id": "HFR1363_3_acceptance_gate",
                "row_kind": "promotion_gate",
                "system_id": "LOCAL_SOURCE_TEMPLATE_001",
                "surface_outer": "REQUIRED",
                "surface_reference": "REQUIRED",
                "coframe_id": "REQUIRED",
                "tau_id": "REQUIRED",
                "boundary_domain_id": "REQUIRED",
                "theta_source": "REQUIRED",
                "Q_tau_source": "REQUIRED",
                "H_tau": "FINITE_NUMERIC_REQUIRED",
                "H_tau_units": "MATCH_H_REF_UNITS_REQUIRED",
                "H_ref": "FINITE_NUMERIC_REQUIRED",
                "H_ref_units": "MATCH_H_TAU_UNITS_REQUIRED",
                "M_H_ref": "H_TAU_MINUS_H_REF_POSITIVE_REQUIRED",
                "M_H_ref_units": "MATCHED_UNITS_REQUIRED",
                "reference_policy": "FIXED_BEFORE_READOUT_REQUIRED",
                "fixed_before_readout_certificate": "REQUIRED",
                "not_orbital_GM": True,
                "not_bare_mass": True,
                "not_reference_only_one": True,
                "not_EH_only_import": True,
                "source_path": "REQUIRED_REAL_LOCAL_SOURCE_PATH",
                "source_anchor": "REQUIRED_REAL_SOURCE_ANCHOR",
                "missing_fields": "all finite numeric/source/certificate fields still missing in live row",
                "status": "CLAIM_BLOCKED",
            },
        ]
    )


def claim_gates() -> list[dict[str, object]]:
    return mark_nonclaim(
        [
            {
                "gate_id": "GATE1363_0_conditional_bridge",
                "claim": "if parent L, tau, theta, Q_tau, and reference are quotient-basic, then vertical H_tau leakage vanishes",
                "gate_pass": True,
                "reason": "Noether/covariant-phase-space chain rule is mathematically valid under the stated strong hypotheses.",
            },
            {
                "gate_id": "GATE1363_1_parent_current_chain_bridge",
                "claim": "current MTS parent action satisfies the qObs-current-chain bridge",
                "gate_pass": False,
                "reason": "sector parent action, theta, Q_tau, tau, boundary/reference, Gamma/Khat, Pi_M, and matter/source clauses are not jointly signed.",
            },
            {
                "gate_id": "GATE1363_2_Htau_Href_source_row_ready",
                "claim": "H_tau/H_ref first source row can be scored",
                "gate_pass": False,
                "reason": "first source row is a strict missing-field template with real source path, units, and coefficients absent.",
            },
            {
                "gate_id": "GATE1363_3_EH_or_orbital_shortcut_allowed",
                "claim": "EH-only charge, orbital GM, bare mass, or reference-only 1 may fill M_H_ref",
                "gate_pass": False,
                "reason": "anti-circularity guard remains active.",
            },
            {
                "gate_id": "GATE1363_4_local_GR_reopen",
                "claim": "local-GR/PPN/Newton gates can reopen",
                "gate_pass": False,
                "reason": "qObs current-chain, H_tau/H_ref/M_H_ref, q_loc, Pi_M/source equality, and frame/tau locks remain blocked.",
            },
        ]
    )


def decision_rows() -> list[dict[str, object]]:
    return mark_nonclaim(
        [
            {
                "decision_id": "DEC1363_0_bridge_is_exact_but_conditional",
                "decision": "Keep the qObs-current-chain bridge as the clean theorem route.",
                "why": "It would derive local denominator frame blindness rather than assert it.",
                "next_action": "audit whether each retained parent sector is quotient-basic and current-chain owned.",
            },
            {
                "decision_id": "DEC1363_1_current_corpus_does_not_close_bridge",
                "decision": "Do not claim the bridge for current MTS.",
                "why": "1008/1009/1010 leave theta, Q_tau, Gamma/Khat, Pi_M, boundary/reference, and source glue unsigned.",
                "next_action": "keep all bridge failures explicit as residual/source rows.",
            },
            {
                "decision_id": "DEC1363_2_first_Htau_Href_row_staged",
                "decision": "Use the new first-row template for future denominator evidence.",
                "why": "It blocks the dangerous shortcuts: EH-only import, orbital GM, bare mass, and reference-only 1.",
                "next_action": "fill the row only from parent theta/Q_tau sources or a documented source acquisition path.",
            },
        ]
    )


def next_rows() -> list[dict[str, object]]:
    return mark_nonclaim(
        [
            {
                "next_id": "NEXT1363_0_1364",
                "target_file": "1364-Y5-R10-RAB-quotient-basic-parent-action-sector-audit-or-Htau-Href-source-acquisition.md",
                "target_script": "scripts/Y5_R10_RAB_quotient_basic_parent_action_sector_audit_or_Htau_Href_source_acquisition.py",
                "task": "audit each retained parent-action sector for quotient-basic Lagrangian, theta, Q_tau, tau, boundary/reference, and source-glue ownership; if any fail, make concrete H_tau/H_ref source-acquisition rows",
                "success_condition": "either every retained sector is q-basic/current-owned with source paths, or the denominator acquisition ledger says exactly which source/equation is missing",
                "do_not": "do not claim local GR; do not import EH-only charge; do not use orbital GM, bare mass, reference-only 1, fitted reference, post-readout frame choice, formalization-workbench edits, or GitHub action",
            }
        ]
    )


def validate_outputs(
    sources: list[dict[str, object]],
    bridge: list[dict[str, object]],
    obstructions: list[dict[str, object]],
    first_rows: list[dict[str, object]],
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
        "VAL1363_0_sources_exist",
        "registered source paths exist and anchors are found",
        all(bool(row["exists"]) and bool(row["anchor_found"]) for row in sources),
        ";".join(f"{row['source_id']}={row['exists']}/{row['anchor_found']}" for row in sources),
    )

    verdict = next(row for row in bridge if row["attempt_id"] == "BTA1363_7_verdict")
    add(
        "VAL1363_1_bridge_not_promoted",
        "qObs-current-chain bridge is not promoted for current MTS",
        str(verdict["result"]) == "QOBS_CURRENT_CHAIN_BRIDGE_NOT_PROVED" and not bool(verdict["claim_allowed"]),
        str(verdict["why_not_claim"]),
    )

    add(
        "VAL1363_2_conditional_math_is_separated",
        "conditional bridge lemmas are separated from current claims",
        any(row["result"].startswith("VALID") for row in bridge) and str(verdict["result"]).endswith("NOT_PROVED"),
        "conditional rows present while verdict blocks claim",
    )

    add(
        "VAL1363_3_obstructions_open",
        "bridge obstruction ledger covers parent action, tau, theta/Q, reference, q_loc, Pi_M/worldtube, and matter constants",
        len(obstructions) == 7 and all(row["status"] == "OPEN" for row in obstructions),
        f"open_obstructions={len(obstructions)}",
    )

    anti_flags = ("not_orbital_GM", "not_bare_mass", "not_reference_only_one", "not_EH_only_import")
    add(
        "VAL1363_4_first_source_row_guarded",
        "H_tau/H_ref first source row has strict anti-circularity fields",
        all(flag in first_rows[0] and bool(first_rows[0][flag]) for flag in anti_flags)
        and all(not row["claim_allowed"] for row in first_rows),
        ";".join(f"{flag}={first_rows[0][flag]}" for flag in anti_flags),
    )

    add(
        "VAL1363_5_first_source_row_missing_fields_explicit",
        "H_tau/H_ref source rows keep missing fields explicit and nonclaim",
        "MISSING_H_TAU" in str(first_rows[0]["H_tau"])
        and "MISSING_H_REF" in str(first_rows[0]["H_ref"])
        and "MISSING_M_H_REF" in str(first_rows[0]["M_H_ref"])
        and str(first_rows[0]["status"]).startswith("CLAIM_BLOCKED"),
        str(first_rows[0]["missing_fields"]),
    )

    add(
        "VAL1363_6_claim_gates_block_claim",
        "claim gates block current MTS bridge, denominator, shortcut, and local-GR claims",
        all((row["gate_pass"] is False or row["gate_id"] == "GATE1363_0_conditional_bridge") and not row["claim_allowed"] for row in gates),
        ";".join(f"{row['gate_id']}={row['gate_pass']}" for row in gates),
    )

    all_rows = sources + bridge + obstructions + first_rows + gates + decisions + next_target
    add(
        "VAL1363_7_nonclaim_policy",
        "all generated rows remain nonclaim",
        all(not row.get("valid_for_claim", False) and not row.get("claim_allowed", False) for row in all_rows),
        "valid_for_claim=false and claim_allowed=false across generated rows",
    )

    formalization_hits: list[Path] = []
    if FORMALIZATION.exists():
        for pattern in ("*P8_Y5_R10_1363*", "*1363-Y5-R10-RAB-parent-qObs-current-chain*", "*Y5_R10_RAB_parent_qObs_current_chain*"):
            formalization_hits.extend(FORMALIZATION.rglob(pattern))
    add(
        "VAL1363_8_formalization_untouched",
        "formalization-workbench untouched by generated outputs",
        len(formalization_hits) == 0,
        f"formalization_generated_output_count={len(formalization_hits)}",
    )

    add(
        "VAL1363_9_next_target_1364",
        "next target routes to quotient-basic sector audit or H_tau/H_ref acquisition",
        bool(next_target) and str(next_target[0]["target_file"]).startswith("1364-Y5-R10-RAB-quotient-basic-parent-action-sector-audit"),
        str(next_target[0]["target_file"]) if next_target else "missing",
    )

    add(
        "VAL1363_10_overall",
        "overall 1363 validation",
        all(row["status"] == "PASS" for row in validations),
        "1363 keeps the exact bridge conditional and stages guarded H_tau/H_ref source rows",
    )

    return validations


def build_doc(
    sources: list[dict[str, object]],
    bridge: list[dict[str, object]],
    obstructions: list[dict[str, object]],
    first_rows: list[dict[str, object]],
    gates: list[dict[str, object]],
    decisions: list[dict[str, object]],
    next_target: list[dict[str, object]],
    validations: list[dict[str, object]],
) -> str:
    return "\n\n".join(
        [
            f"# {TITLE}",
            "**Current verdict:** 1363 writes the exact conditional bridge from `q/Obs_e` descent to the parent `theta_MTS/Q_tau^MTS/H_tau` current chain, but current MTS does not satisfy the bridge. The route is derivable in principle only if the full parent action, tau generator, symplectic potential, Noether charge, fixed reference, and retained sectors are quotient-basic.",
            "**Main progress:** this checkpoint removes a possible smuggle. We are no longer allowed to say the coframe descends and then quietly borrow an EH Hamiltonian mass. The bridge now demands a q-basic parent current chain, or else the denominator must be filled by explicit nonclaim `H_tau/H_ref` source rows with anti-circularity guards.",
            "## Source register",
            table(["source_id", "source_path", "exists", "anchor_found", "purpose"], sources),
            "## qObs-current-chain bridge attempt",
            table(["attempt_id", "claim_piece", "required_form", "result", "what_would_follow", "why_not_claim"], bridge),
            "## Bridge obstruction ledger",
            table(["obstruction_id", "obstruction", "blocks", "risk", "repair", "status"], obstructions),
            "## Htau/Href first source row",
            table(
                [
                    "row_id",
                    "row_kind",
                    "system_id",
                    "theta_source",
                    "Q_tau_source",
                    "H_tau",
                    "H_ref",
                    "M_H_ref",
                    "not_orbital_GM",
                    "not_bare_mass",
                    "not_reference_only_one",
                    "not_EH_only_import",
                    "source_path",
                    "missing_fields",
                    "status",
                ],
                first_rows,
            ),
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
    bridge = bridge_attempt()
    obstructions = obstruction_rows()
    first_rows = first_source_rows()
    gates = claim_gates()
    decisions = decision_rows()
    next_target = next_rows()
    validations = validate_outputs(sources, bridge, obstructions, first_rows, gates, decisions, next_target)

    write_csv(SOURCE_REGISTER_PATH, sources)
    write_csv(BRIDGE_ATTEMPT_PATH, bridge)
    write_csv(OBSTRUCTION_PATH, obstructions)
    write_csv(FIRST_SOURCE_ROW_PATH, first_rows)
    write_csv(CLAIM_GATE_PATH, gates)
    write_csv(DECISION_PATH, decisions)
    write_csv(NEXT_PATH, next_target)
    write_csv(VALIDATION_PATH, validations)
    DOC_PATH.write_text(
        build_doc(sources, bridge, obstructions, first_rows, gates, decisions, next_target, validations),
        encoding="utf-8",
    )


if __name__ == "__main__":
    main()

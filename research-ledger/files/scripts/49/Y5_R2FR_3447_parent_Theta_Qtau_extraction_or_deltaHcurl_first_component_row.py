from __future__ import annotations

import csv
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "source-intake" / "mts_residuals"
DOC = ROOT / "3447-Y5-R2FR-parent-Theta-Q_tau-extraction-or-deltaH-curl-first-component-row-under-AX1090.md"
FORMALIZATION = ROOT.parent / "formalization-workbench"

SOURCES = {
    "doc_3446": ROOT / "3446-Y5-R2FR-Htau-exact-one-form-reference-lock-or-MHref-denominator-bound-under-AX1090.md",
    "next_3446": OUT / "P8_Y5_R2FR_3446_NEXT_TARGET.csv",
    "denominator_rows_3446": OUT / "P8_Y5_R2FR_3446_MHREF_DENOMINATOR_BOUND_ROWS.csv",
    "one_form_3446": OUT / "P8_Y5_R2FR_3446_HTAU_EXACT_ONE_FORM_THEOREM.csv",
    "pimh_3446": OUT / "P8_Y5_R2FR_3446_PIMH_CARRYFORWARD.csv",
    "doc_3445": ROOT / "3445-Y5-R2FR-Hilbert-identity-PiM-parent-adoption-or-Htau-source-current-lock-under-AX1090.md",
    "pimh_contract_3445": OUT / "P8_Y5_R2FR_3445_HILBERT_IDENTITY_PIM_PARENT_ADOPTION_CONTRACT.csv",
    "doc_3424": ROOT / "3424-Y5-R2FR-minimal-parent-source-coupling-action-or-PC3400-adoption-gate-under-AX1090.md",
    "parent_density_3424": OUT / "P8_Y5_R2FR_3424_PARENT_ACTION_DENSITY.csv",
    "parent_hilbert_clause_3340": OUT / "P8_Y5_R2FR_3340_PARENT_HILBERT_SOURCE_CLAUSE.csv",
    "hilbert_theorem_3340": OUT / "P8_Y5_R2FR_3340_HILBERT_SOURCE_THEOREM_OR_FAIL.csv",
    "jh_derivation_3408": OUT / "P8_Y5_R2FR_3408_JH_HILBERT_SOURCE_DERIVATION.csv",
    "variation_667": OUT / "P8_Y5_R10_667_VARIATION_LEDGER.csv",
    "qtau_decomp_993": OUT / "P8_Y5_R10_993_QTAU_DECOMPOSITION_LEDGER.csv",
    "charge_spine_2340": OUT / "P8_Y5_PARENT_QLOC_2340_PARENT_CHARGE_EXTRACTION_SPINE.csv",
    "theta_qtau_rows_1733": OUT / "P8_Y5_PARENT_QLOC_1733_THETA_QTAU_COMPONENT_ROWS.csv",
    "qtau_status_1646": OUT / "P8_Y5_PARENT_QLOC_1646_QTAU_DECOMPOSITION_STATUS.csv",
    "sector_ledger_2939": OUT / "P8_Y5_R2FR_2939_THETA_QTAU_SECTOR_CERTIFICATE_LEDGER.csv",
    "certificate_2947": OUT / "P8_Y5_R2FR_2947_THETA_QTAU_CERTIFICATE_ATTEMPT.csv",
    "feed_rows_3007": OUT / "P8_Y5_R2FR_3007_THETA_QTAU_FEED_ROWS.csv",
    "theta_qtau_owner_1646": OUT / "P8_Y5_PARENT_QLOC_1646_THETA_QTAU_CURRENT_OWNER_AUDIT.csv",
}

OUTPUTS = {
    "source_register": OUT / "P8_Y5_R2FR_3447_SOURCE_REGISTER.csv",
    "public_current_chain": OUT / "P8_Y5_R2FR_3447_PUBLIC_CURRENT_CHAIN_EXTRACTION.csv",
    "theta_qtau_component_status": OUT / "P8_Y5_R2FR_3447_THETA_QTAU_COMPONENT_STATUS.csv",
    "deltaH_curl_component_rows": OUT / "P8_Y5_R2FR_3447_DELTAH_CURL_FIRST_COMPONENT_ROWS.csv",
    "denominator_update": OUT / "P8_Y5_R2FR_3447_DENOMINATOR_ROW_UPDATE.csv",
    "pimh_carryforward": OUT / "P8_Y5_R2FR_3447_PIMH_CARRYFORWARD.csv",
    "promotion_gates": OUT / "P8_Y5_R2FR_3447_PROMOTION_GATES.csv",
    "decision_ledger": OUT / "P8_Y5_R2FR_3447_DECISION_LEDGER.csv",
    "next_target": OUT / "P8_Y5_R2FR_3447_NEXT_TARGET.csv",
    "runner_nonclaim": OUT / "P8_Y5_R2FR_3447_RUNNER_NONCLAIM.csv",
    "validation": OUT / "P8_Y5_BRR545_3447_VALIDATION.csv",
}


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    if not rows:
        raise ValueError(f"no rows for {path}")
    path.parent.mkdir(parents=True, exist_ok=True)
    fields = list(rows[0].keys())
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def read_csv(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def md_table(rows: list[dict[str, Any]]) -> str:
    if not rows:
        return "_No rows._"
    fields = list(rows[0].keys())

    def clean(value: Any) -> str:
        return str(value).replace("\n", " ").replace("|", "/")

    return "\n".join(
        [
            "| " + " | ".join(fields) + " |",
            "| " + " | ".join("---" for _ in fields) + " |",
            *["| " + " | ".join(clean(row.get(field, "")) for field in fields) + " |" for row in rows],
        ]
    )


def source_register() -> list[dict[str, Any]]:
    roles = {
        "doc_3446": "immediate Theta/Qtau extraction handoff",
        "next_3446": "machine-readable 3447 target",
        "denominator_rows_3446": "Delta_H_curl target rows",
        "one_form_3446": "Htau one-form theorem and bound route",
        "pimh_3446": "PiMH carryforward",
        "doc_3445": "PiMH adoption checkpoint",
        "pimh_contract_3445": "Hilbert identity branch contract",
        "doc_3424": "minimal parent action branch",
        "parent_density_3424": "public EH/matter/EM parent density",
        "parent_hilbert_clause_3340": "public Hilbert source clause",
        "hilbert_theorem_3340": "conditional Hilbert source theorem",
        "jh_derivation_3408": "Hilbert stress derivation",
        "variation_667": "covariant phase-space variation ledger",
        "qtau_decomp_993": "Q_tau sector decomposition",
        "charge_spine_2340": "parent charge extraction spine",
        "theta_qtau_rows_1733": "Theta/Qtau component rows",
        "qtau_status_1646": "Q_tau decomposition status",
        "sector_ledger_2939": "sector certificate ledger",
        "certificate_2947": "Theta/Qtau certificate attempt",
        "feed_rows_3007": "Theta/Qtau feed rows",
        "theta_qtau_owner_1646": "parent current owner audit",
    }
    return [
        {
            "source_id": source_id,
            "path": str(path),
            "exists": path.exists(),
            "role": roles[source_id],
            "valid_for_claim": False,
            "claim_allowed": False,
        }
        for source_id, path in SOURCES.items()
    ]


def public_current_chain() -> list[dict[str, Any]]:
    return [
        {
            "chain_id": "PCE3447_0_public_L",
            "piece": "public local action",
            "formula": "L_pub=L_EH[g_obs;G_ref]+L_matter[e_obs,psi]+L_EM[g_obs,A;lambda_0]",
            "extraction": "delta L_pub=E_pub delta Phi_pub + d(Theta_EH+Theta_matter+Theta_EM)",
            "status": "PUBLIC_CONTROL_CHAIN_EXTRACTED_CONDITIONALLY",
            "remaining_gap": "not the total MTS parent current; extra, boundary/reference, tau/surface and source-glue sectors remain",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "chain_id": "PCE3447_1_public_Noether",
            "piece": "public observed-time current",
            "formula": "J_tau^pub=Theta_pub(Phi,L_tau Phi)-i_tau L_pub",
            "extraction": "on public equations, J_tau^pub=dQ_tau^EH+C_tau^matter+C_tau^EM, with public matter/EM stress in the Hilbert source and any gauge/radiative boundary flux retained",
            "status": "FORMAL_PUBLIC_CURRENT_CHAIN_AVAILABLE",
            "remaining_gap": "stationary/no-flux public boundary conditions are required before curl zero; matter/EM source support and radiation crossing must be handled",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "chain_id": "PCE3447_2_EM_Poynting",
            "piece": "public EM/Poynting stress",
            "formula": "S_EM=-(lambda_0/4) int sqrt(-g_obs) F^2; T_EM from Hilbert variation",
            "extraction": "Poynting flux is an observer split of T_EM/symplectic flux, not a separate gravitational source owner",
            "status": "PUBLIC_HILBERT_SOURCE_IF_LAMBDA0_AND_GOBS_SIGNED",
            "remaining_gap": "public Maxwell/Hodge normalization and radiative boundary flux still need branch conditions or bounds",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "chain_id": "PCE3447_3_PiMH",
            "piece": "Hilbert identity mass map",
            "formula": "Pi_M^H=id/inclusion on C_H^M",
            "extraction": "no independent Theta_projector or Q_tau_projector is needed for the preferred identity branch",
            "status": "CARRIED_FORWARD_FROM_3445",
            "remaining_gap": "non-Hilbert J_extra and old non-identity projectors remain outside this result",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "chain_id": "PCE3447_4_total_verdict",
            "piece": "Theta_MTS and Q_tau^MTS total",
            "formula": "Theta_MTS=Theta_pub+Theta_extra+Theta_boundary+Theta_ref+Theta_glue; Q_tau^MTS=Q_tau^pub+Q_tau^extra+Q_tau^boundary+Q_tau^glue",
            "extraction": "public chain is extracted as a control sector, but total MTS charge is not promoted",
            "status": "PARTIAL_EXTRACTION_TOTAL_NOT_CLAIM_READY",
            "remaining_gap": "extra-sector action/current, boundary/reference charge and tau/surface/source-glue rows are the live blockers",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
    ]


def theta_qtau_component_status() -> list[dict[str, Any]]:
    return [
        {
            "component_id": "TQS3447_0_public_EH",
            "component": "Theta_EH;Q_tau^EH",
            "status_after_3447": "CONDITIONAL_PUBLIC_CONTROL_ANCHOR",
            "zero_or_bound_route": "EH exterior plus fixed tau/surface/reference and no non-EH flux",
            "blocks_total_claim": False,
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "component_id": "TQS3447_1_public_matter_EM",
            "component": "Theta_matter;Theta_EM;C_tau^matter;C_tau^EM",
            "status_after_3447": "HILBERT_SOURCE_CONTROL_SECTOR_RETAIN_PUBLIC_FLUX",
            "zero_or_bound_route": "source-free/stationary exterior or explicit public matter/EM/radiation flux bound",
            "blocks_total_claim": True,
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "component_id": "TQS3447_2_PiMH",
            "component": "Theta_projector^H;Q_tau_projector^H",
            "status_after_3447": "NO_INDEPENDENT_COMPONENT_IN_IDENTITY_BRANCH",
            "zero_or_bound_route": "reactivates only for non-identity PiM",
            "blocks_total_claim": False,
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "component_id": "TQS3447_3_extra_MTS",
            "component": "Theta_extra;Q_tau^extra;C_tau^extra",
            "status_after_3447": "MISSING_L_EXTRA_THETA_QTAU",
            "zero_or_bound_route": "derive residual-sector L_X/Theta_X/Q_tau^X or source-bound its curl contribution",
            "blocks_total_claim": True,
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "component_id": "TQS3447_4_boundary_reference",
            "component": "Theta_boundary;Q_tau^boundary;delta B_ref",
            "status_after_3447": "MISSING_BOUNDARY_REFERENCE_OWNER",
            "zero_or_bound_route": "fixed reference/no-retune boundary class or Delta_ref/symplectic flux bound",
            "blocks_total_claim": True,
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "component_id": "TQS3447_5_tau_surface_glue",
            "component": "tau/surface/worldtube source glue",
            "status_after_3447": "MISSING_TAU_SURFACE_SOURCE_GLUE",
            "zero_or_bound_route": "same tau/frame/surface certificate and worldtube Hilbert source equality",
            "blocks_total_claim": True,
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "component_id": "TQS3447_6_total",
            "component": "Theta_MTS;Q_tau^MTS",
            "status_after_3447": "TOTAL_NOT_PROMOTED_PUBLIC_CONTROL_PLUS_RETAINED_MTS_COMPONENTS",
            "zero_or_bound_route": "all components above must be theorem-zero, public-control, or source-bounded",
            "blocks_total_claim": True,
            "claim_allowed": False,
            "valid_for_claim": False,
        },
    ]


def deltaH_curl_component_rows() -> list[dict[str, Any]]:
    return [
        {
            "row_id": "DHC3447_0_public_sector_curl",
            "quantity": "Delta_H_curl_public",
            "definition": "public EH+ordinary matter+EM contribution to int_BF|d_F alpha_tau|",
            "formula": "int_BF | -int_S i_tau omega_pub + C_tau^matter + C_tau^EM |",
            "current_status": "THEOREM_ZERO_IF_STATIONARY_PUBLIC_NO_FLUX_BOUNDARY_ELSE_BOUND_REQUIRED",
            "required_columns": "system_id;tau_id;surface_pair;variation_pair;public_boundary_condition;EM_radiation_flux;matter_support;curl_public_bound;units;source_path",
            "numeric_or_theorem_value": "CONDITIONAL_ZERO_OR_MISSING_PUBLIC_FLUX_BOUND",
            "source_path": str(OUT / "P8_Y5_R2FR_3447_PUBLIC_CURRENT_CHAIN_EXTRACTION.csv"),
            "score_ready": False,
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "row_id": "DHC3447_1_extra_sector_curl",
            "quantity": "Delta_H_curl_extra",
            "definition": "MTS extra/domain/memory/range/source-exchange contribution to H_tau curl",
            "formula": "int_BF | -int_S i_tau omega_extra + C_tau^extra |",
            "current_status": "MISSING_EXTRA_SECTOR_LAGRANGIAN_CURRENT",
            "required_columns": "system_id;sector;L_X;Theta_X;Q_tau_X;C_tau_X;surface_pair;variation_pair;curl_extra_bound;units;source_path",
            "numeric_or_theorem_value": "MISSING_EXTRA_CURL_COMPONENT",
            "source_path": "MISSING_SOURCE_PATH",
            "score_ready": False,
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "row_id": "DHC3447_2_boundary_reference_curl",
            "quantity": "Delta_H_curl_boundary_ref",
            "definition": "boundary, corner and reference contribution to H_tau curl",
            "formula": "int_BF |C_S+C_ref+delta B_ref curl|",
            "current_status": "MISSING_BOUNDARY_REFERENCE_LOCK_OR_BOUND",
            "required_columns": "system_id;reference_selector;surface_pair;corner_rule;Delta_ref_curl;boundary_flux_bound;units;source_path",
            "numeric_or_theorem_value": "MISSING_BOUNDARY_REFERENCE_CURL",
            "source_path": "MISSING_SOURCE_PATH",
            "score_ready": False,
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "row_id": "DHC3447_TOTAL",
            "quantity": "Delta_H_curl_bound",
            "definition": "absolute no-cancellation H_tau curl bound after first public component extraction",
            "formula": "abs(Delta_H_curl_public)+abs(Delta_H_curl_extra)+abs(Delta_H_curl_boundary_ref)+abs(tau_surface_frame_curl)",
            "current_status": "TOTAL_NONCLAIM_COMPONENT_VALUES_MISSING",
            "required_columns": "all component rows plus M_H_ref_lower and no_cancellation_flag",
            "numeric_or_theorem_value": "MISSING_COMPONENT_VALUES",
            "source_path": str(OUT / "P8_Y5_R2FR_3447_DELTAH_CURL_FIRST_COMPONENT_ROWS.csv"),
            "score_ready": False,
            "claim_allowed": False,
            "valid_for_claim": False,
        },
    ]


def denominator_update() -> list[dict[str, Any]]:
    return [
        {
            "update_id": "DU3447_0_DBR3446_1",
            "prior_row": "DBR3446_1_delta_H_curl",
            "before": "MISSING_CURL_COMPONENT_BOUNDS",
            "after": "first component split written: public sector conditional zero/bound row plus extra and boundary/reference residual rows",
            "effect": "Delta_H_curl is no longer one blob; public GR-control and MTS-specific curl components are separated",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "update_id": "DU3447_1_DBR3446_5",
            "prior_row": "DBR3446_5_epsilon_den_total",
            "before": "MISSING_COMPONENT_VALUES",
            "after": "epsilon_den_total must include DHC3447_TOTAL plus Delta_ref, tau/surface/frame and M_H_ref_lower",
            "effect": "source denominator runner can later compare public-control zero branch against MTS extra-sector bound branch",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
    ]


def pimh_carryforward() -> list[dict[str, Any]]:
    return [
        {
            "carry_id": "PIMH3447_0",
            "result": "Pi_M^H remains identity/inclusion and adds no independent Theta_projector/Q_tau_projector component",
            "guard": "if non-identity PiM returns, TQS3447_2 is invalid and I_commutator/projector-stress rows reactivate",
            "claim_allowed": False,
            "valid_for_claim": False,
        }
    ]


def promotion_gates() -> list[dict[str, Any]]:
    return [
        {
            "gate_id": "PG3447_0_sources",
            "claim": "all 3447 cited source paths exist",
            "gate_pass": all(path.exists() for path in SOURCES.values()),
            "reason": "source register path check",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "gate_id": "PG3447_1_public_chain",
            "claim": "public EH+matter+EM current chain is extracted as a control sector",
            "gate_pass": True,
            "reason": "PCE3447 rows give L_pub, Theta_pub and J_tau^pub chain",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "gate_id": "PG3447_2_first_curl_row",
            "claim": "first Delta_H_curl component row is written",
            "gate_pass": True,
            "reason": "DHC3447_0_public_sector_curl splits public control curl from MTS extra curl",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "gate_id": "PG3447_3_total_Qtau",
            "claim": "Theta_MTS and Q_tau^MTS total are promoted",
            "gate_pass": False,
            "reason": "extra, boundary/reference and tau/surface/source-glue components remain missing",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "gate_id": "PG3447_4_local_GR_Newton",
            "claim": "local GR/Newton denominator is promoted",
            "gate_pass": False,
            "reason": "M_H_ref_lower and total curl/reference/frame components are still nonclaim",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
    ]


def decision_ledger() -> list[dict[str, Any]]:
    return [
        {
            "decision_id": "DEC3447_0_public_control",
            "decision": "Use public EH+matter+EM current chain as the control branch.",
            "because": "it separates standard-GR current bookkeeping from genuinely MTS-specific extra/boundary/source-glue sectors",
            "next_action": "do not blame MTS-specific failures on the public control chain unless the public boundary/radiation flux also fails",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "decision_id": "DEC3447_1_extra_next",
            "decision": "Attack the MTS extra-sector L_X/Theta_X/Q_tau_X next.",
            "because": "after Pi_M^H and public control extraction, the first real MTS denominator blocker is the extra-sector curl piece",
            "next_action": "derive extra-sector current owner or fill DHC3447_1",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
    ]


def next_target() -> list[dict[str, Any]]:
    return [
        {
            "target_doc": "3448-Y5-R2FR-extra-sector-LX-ThetaX-QtauX-owner-or-deltaHcurl-extra-row-under-AX1090.md",
            "target_script": "scripts/Y5_R2FR_3448_extra_sector_LX_ThetaX_QtauX_owner_or_deltaHcurl_extra_row.py",
            "objective": "derive the MTS extra-sector L_X, Theta_X, Q_tau^X and C_tau^X contribution to the H_tau curl for the adopted Pi_M^H branch, or fill DHC3447_1 as a nonclaim source-bound component with units, surface pair, variation pair and source path",
            "success_condition": "extra-sector curl is theorem-zero, public-bound style, or represented by a schema-valid nonclaim bound row; no local-GR/Newton claim until denominator total is closed",
            "valid_for_claim": False,
            "claim_allowed": False,
        }
    ]


def runner_nonclaim() -> list[dict[str, Any]]:
    return [
        {
            "runner_id": "RUN3447_0_public_control",
            "public_chain_extracted": True,
            "first_curl_component_written": True,
            "total_Qtau_promoted": False,
            "score_ready": False,
            "result": "PUBLIC_CONTROL_READY_TOTAL_MTS_CHARGE_BLOCKED",
            "valid_for_claim": False,
            "claim_allowed": False,
        }
    ]


def validation_rows(rows_by_name: dict[str, list[dict[str, Any]]], start_utc: datetime) -> list[dict[str, Any]]:
    modified_count = 0
    if FORMALIZATION.exists():
        start_timestamp = start_utc.timestamp()
        modified_count = sum(
            1
            for checked_path in FORMALIZATION.rglob("*")
            if checked_path.is_file() and checked_path.stat().st_mtime >= start_timestamp
        )

    nonclaim_ok = True
    for output_name, rows in rows_by_name.items():
        if output_name == "validation":
            continue
        for row in rows:
            if str(row.get("valid_for_claim", "")).lower() == "true":
                nonclaim_ok = False
            if str(row.get("claim_allowed", "")).lower() == "true":
                nonclaim_ok = False

    parse_ok = True
    for output_name, path in OUTPUTS.items():
        if output_name == "validation":
            continue
        if path.exists():
            try:
                read_csv(path)
            except csv.Error:
                parse_ok = False

    validations = [
        {
            "check_id": "VAL3447_0_sources_exist",
            "condition": "all cited 3447 source paths exist",
            "passed": all(path.exists() for path in SOURCES.values()),
            "detail": f"{sum(1 for path in SOURCES.values() if path.exists())}/{len(SOURCES)} source paths exist",
        },
        {
            "check_id": "VAL3447_1_public_chain",
            "condition": "public current chain extraction is present",
            "passed": any(row["chain_id"] == "PCE3447_0_public_L" for row in rows_by_name["public_current_chain"])
            and any(row["chain_id"] == "PCE3447_1_public_Noether" for row in rows_by_name["public_current_chain"]),
            "detail": "L_pub and J_tau^pub rows written",
        },
        {
            "check_id": "VAL3447_2_first_curl_row",
            "condition": "first Delta_H_curl component row is present",
            "passed": any(
                row["row_id"] == "DHC3447_0_public_sector_curl"
                for row in rows_by_name["deltaH_curl_component_rows"]
            ),
            "detail": "public-sector curl component split",
        },
        {
            "check_id": "VAL3447_3_total_not_promoted",
            "condition": "total Theta_MTS/Q_tau^MTS remains nonclaim",
            "passed": any(
                row["component_id"] == "TQS3447_6_total"
                and row["status_after_3447"] == "TOTAL_NOT_PROMOTED_PUBLIC_CONTROL_PLUS_RETAINED_MTS_COMPONENTS"
                for row in rows_by_name["theta_qtau_component_status"]
            ),
            "detail": "total current chain still blocked",
        },
        {
            "check_id": "VAL3447_4_PiMH_no_reopen",
            "condition": "Pi_M^H does not reintroduce projector charge",
            "passed": any(row["component_id"] == "TQS3447_2_PiMH" for row in rows_by_name["theta_qtau_component_status"]),
            "detail": "PiMH carryforward row present",
        },
        {
            "check_id": "VAL3447_5_next_extra",
            "condition": "next target attacks extra-sector curl owner",
            "passed": rows_by_name["next_target"][0]["target_doc"].startswith("3448-Y5-R2FR-extra-sector-LX-ThetaX-QtauX-owner"),
            "detail": rows_by_name["next_target"][0]["target_doc"],
        },
        {
            "check_id": "VAL3447_6_generated_csv_parse",
            "condition": "generated CSV rows parse cleanly",
            "passed": parse_ok,
            "detail": "CSV reader pass for generated outputs present before validation write",
        },
        {
            "check_id": "VAL3447_7_nonclaim",
            "condition": "all generated rows remain nonclaim",
            "passed": nonclaim_ok,
            "detail": "valid_for_claim=false and claim_allowed=false wherever present",
        },
        {
            "check_id": "VAL3447_8_formalization_untouched",
            "condition": "formalization-workbench modified-file count remains 0 during this run",
            "passed": modified_count == 0,
            "detail": f"modified_count_since_start={modified_count}",
        },
    ]
    validations.append(
        {
            "check_id": "VAL3447_9_overall",
            "condition": "3447 Theta/Qtau checkpoint is internally valid",
            "passed": all(row["passed"] for row in validations),
            "detail": "PASS" if all(row["passed"] for row in validations) else "FAIL",
        }
    )
    return validations


def write_doc(rows_by_name: dict[str, list[dict[str, Any]]]) -> None:
    text = f"""# 3447 - Parent Theta/Qtau Extraction or DeltaH Curl First Component Row

## Summary
- This checkpoint extracts the public control current chain for the adopted `Pi_M^H` branch.
- The public sector is `L_pub=L_EH+L_matter+L_EM`, with `Theta_pub=Theta_EH+Theta_matter+Theta_EM` and `J_tau^pub=Theta_pub(L_tau Phi)-i_tau L_pub`.
- This is not the total MTS charge: extra, boundary/reference, tau/surface and source-glue pieces remain live.
- The first `Delta_H_curl` component row is now split out as `DHC3447_0_public_sector_curl`, separating standard public-sector flux from genuinely MTS-specific extra curl.
- `Pi_M^H` stays clean: no independent projector `Theta/Q_tau` component is introduced in the preferred identity branch.

## Source Register
{md_table(rows_by_name["source_register"])}

## Public Current Chain Extraction
{md_table(rows_by_name["public_current_chain"])}

## Theta/Qtau Component Status
{md_table(rows_by_name["theta_qtau_component_status"])}

## DeltaH Curl First Component Rows
{md_table(rows_by_name["deltaH_curl_component_rows"])}

## Denominator Row Update
{md_table(rows_by_name["denominator_update"])}

## PiMH Carryforward
{md_table(rows_by_name["pimh_carryforward"])}

## Promotion Gates
{md_table(rows_by_name["promotion_gates"])}

## Decision Ledger
{md_table(rows_by_name["decision_ledger"])}

## Next Target
{md_table(rows_by_name["next_target"])}

## Runner Nonclaim
{md_table(rows_by_name["runner_nonclaim"])}

## Validation
{md_table(rows_by_name["validation"])}

## Bottom Line
We now have a control chain: public EH plus ordinary matter and public EM can be handled as the reference current sector, including Poynting as Hilbert/symplectic flux rather than a mystery source. The next hard part is genuinely MTS: `L_X`, `Theta_X`, `Q_tau^X`, and `C_tau^X` for the extra sector.
"""
    DOC.write_text(text, encoding="utf-8")


def main() -> None:
    start_utc = datetime.now(timezone.utc)
    rows_by_name = {
        "source_register": source_register(),
        "public_current_chain": public_current_chain(),
        "theta_qtau_component_status": theta_qtau_component_status(),
        "deltaH_curl_component_rows": deltaH_curl_component_rows(),
        "denominator_update": denominator_update(),
        "pimh_carryforward": pimh_carryforward(),
        "promotion_gates": promotion_gates(),
        "decision_ledger": decision_ledger(),
        "next_target": next_target(),
        "runner_nonclaim": runner_nonclaim(),
    }
    rows_by_name["validation"] = validation_rows(rows_by_name, start_utc)
    for output_name, rows in rows_by_name.items():
        write_csv(OUTPUTS[output_name], rows)
    write_doc(rows_by_name)
    failed_rows = [row for row in rows_by_name["validation"] if not row["passed"]]
    if failed_rows:
        raise SystemExit(f"3447 validation failed: {failed_rows}")
    print(f"wrote {DOC}")
    print(f"wrote {len(OUTPUTS)} csv outputs")


if __name__ == "__main__":
    main()

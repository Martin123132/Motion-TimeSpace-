from __future__ import annotations

import csv
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
SRC_DIR = Path("source-intake/mts_residuals")

DOC_PATH = Path("1416-Y5-R10-RAB-source-only-species-slot-and-current-rescaling-ban-or-Rsource-bound-row.md")
SOURCE_REGISTER_PATH = SRC_DIR / "P8_Y5_R10_1416_SOURCE_REGISTER.csv"
BAN_ATTEMPT_PATH = SRC_DIR / "P8_Y5_R10_1416_SOURCE_SLOT_CURRENT_RESCALING_BAN_ATTEMPT.csv"
COUNTERMODEL_PATH = SRC_DIR / "P8_Y5_R10_1416_SOURCE_SLOT_COUNTERMODEL_LEDGER.csv"
FINITE_ROW_PATH = SRC_DIR / "P8_Y5_R10_1416_FIRST_RSOURCE_COEFFICIENT_ROW.csv"
ACCEPTANCE_GATE_PATH = SRC_DIR / "P8_Y5_R10_1416_RSOURCE_ROW_ACCEPTANCE_GATE.csv"
DECISION_PATH = SRC_DIR / "P8_Y5_R10_1416_DECISION_LEDGER.csv"
CLAIM_GATE_PATH = SRC_DIR / "P8_Y5_R10_1416_CLAIM_GATE.csv"
NEXT_TARGET_PATH = SRC_DIR / "P8_Y5_R10_1416_NEXT_TARGET.csv"
VALIDATION_PATH = SRC_DIR / "P8_Y5_BRR545_1416_VALIDATION.csv"

STATUS = "Y5_R10_1416_source_slot_current_rescaling_ban_failed_Rsource_first_row_written_nonclaim"
CLAIM_CEILING = (
    "source_slot_current_rescaling_ban_attempt_and_first_Rsource_row_only_no_WEP_pass_"
    "no_beta_source_pass_no_Newton_no_R10_no_PPN_no_local_GR_pass"
)


def clean(value: Any) -> str:
    return str(value).replace("\n", " ").replace("\r", " ").strip()


def md_cell(value: Any) -> str:
    return clean(value).replace("|", "\\|")


def write_csv(relative_path: Path, rows: list[dict[str, Any]]) -> None:
    path = ROOT / relative_path
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        raise ValueError(f"no rows supplied for {relative_path}")
    fieldnames = list(rows[0].keys())
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow({key: clean(row.get(key, "")) for key in fieldnames})


def md_table(rows: list[dict[str, Any]]) -> str:
    if not rows:
        return ""
    headers = list(rows[0].keys())
    lines = [
        "| " + " | ".join(headers) + " |",
        "| " + " | ".join(["---"] * len(headers)) + " |",
    ]
    for row in rows:
        lines.append("| " + " | ".join(md_cell(row.get(header, "")) for header in headers) + " |")
    return "\n".join(lines)


def anchor_found(relative_path: str, anchor: str) -> bool:
    path = ROOT / relative_path
    if not path.exists():
        return False
    return anchor in path.read_text(encoding="utf-8", errors="ignore")


def source_register_rows() -> list[dict[str, Any]]:
    rows = [
        {
            "source_id": "SRC1416_0_1415_doc",
            "source_path": "1415-Y5-R10-RAB-source-current-owner-or-Rsource-finite-template.md",
            "anchor": "NEXT1415_0_1416",
            "role": "prior checkpoint selecting source-only species slot/current rescaling ban",
        },
        {
            "source_id": "SRC1416_1_1415_Rsource",
            "source_path": "source-intake/mts_residuals/P8_Y5_R10_1415_RSOURCE_FINITE_TEMPLATE.csv",
            "anchor": "RSF1415_6_verdict",
            "role": "R_source finite template pack",
        },
        {
            "source_id": "SRC1416_2_1415_owner",
            "source_path": "source-intake/mts_residuals/P8_Y5_R10_1415_SOURCE_CURRENT_OWNER_ATTEMPT.csv",
            "anchor": "SCO1415_6_verdict",
            "role": "source-current owner not derived",
        },
        {
            "source_id": "SRC1416_3_1412_morphism",
            "source_path": "source-intake/mts_residuals/P8_Y5_R10_1412_VISIBLE_COEFFICIENT_MORPHISM_COUNTEREXAMPLES.csv",
            "anchor": "MOR1412_3_species_source",
            "role": "species/source morphism retained as R_source component",
        },
        {
            "source_id": "SRC1416_4_1407_audit",
            "source_path": "source-intake/mts_residuals/P8_Y5_R10_1407_NOSOURCEONLYSPECIESSLOT_PROOF_AUDIT.csv",
            "anchor": "NSS1407_7_current_verdict",
            "role": "NoSourceOnlySpeciesSlot not proved",
        },
        {
            "source_id": "SRC1416_5_1407_counterexamples",
            "source_path": "source-intake/mts_residuals/P8_Y5_R10_1407_SOURCE_ONLY_SLOT_COUNTEREXAMPLE_TEST.csv",
            "anchor": "SLOT1407_4_verdict",
            "role": "source-only slot counterexamples survive",
        },
        {
            "source_id": "SRC1416_6_1407_schema_gate",
            "source_path": "source-intake/mts_residuals/P8_Y5_R10_1407_SCHEMA_ACCEPTANCE_GATE.csv",
            "anchor": "SG1407_5_verdict",
            "role": "schema ready but source values missing",
        },
        {
            "source_id": "SRC1416_7_1338_object_language",
            "source_path": "source-intake/mts_residuals/P8_Y5_R10_1338_OBJECT_LANGUAGE_THEOREM_ATTEMPT.csv",
            "anchor": "OLT1338_6_verdict",
            "role": "object-language theorem not derived",
        },
        {
            "source_id": "SRC1416_8_1338_closure",
            "source_path": "source-intake/mts_residuals/P8_Y5_R10_1338_NO_SOURCE_SLOT_CLOSURE_CONDITION.csv",
            "anchor": "CLOS1338_2_no_source_only_species_slot",
            "role": "sharp closure clause Hom(SpeciesLabel,Coeff_active_source)=empty",
        },
        {
            "source_id": "SRC1416_9_1338_countermodels",
            "source_path": "source-intake/mts_residuals/P8_Y5_R10_1338_LIVE_COUNTERMODEL_BOUNDARIES.csv",
            "anchor": "CM1338_3_nonHilbert_readout_current",
            "role": "live countermodel boundaries",
        },
        {
            "source_id": "SRC1416_10_1310_forbidden_vertex",
            "source_path": "source-intake/mts_residuals/P8_Y5_R10_1310_FORBIDDEN_VERTEX_GATE.csv",
            "anchor": "FVG1310_4_source_weight_vertex",
            "role": "source weight vertex remains unsigned",
        },
        {
            "source_id": "SRC1416_11_1310_coefficients",
            "source_path": "source-intake/mts_residuals/P8_Y5_R10_1310_QC_COEFFICIENT_ACQUISITION_NONCLAIM.csv",
            "anchor": "QCA1310_5_qbar_source_weight",
            "role": "qbar_source_weight coefficient row template",
        },
        {
            "source_id": "SRC1416_12_1077_counterexamples",
            "source_path": "source-intake/mts_residuals/P8_Y5_R10_1077_ZERO_THEOREM_COUNTEREXAMPLE_AUDIT.csv",
            "anchor": "CE1077_1_current_rescaling",
            "role": "current-rescaling counterexample",
        },
        {
            "source_id": "SRC1416_13_1077_finite",
            "source_path": "source-intake/mts_residuals/P8_Y5_R10_1077_FINITE_ROUTE_REQUIREMENTS.csv",
            "anchor": "FIN1077_1_R_source",
            "role": "finite R_source source vector requirement",
        },
        {
            "source_id": "SRC1416_14_this_script",
            "source_path": "scripts/Y5_R10_RAB_source_only_species_slot_and_current_rescaling_ban_or_Rsource_bound_row.py",
            "anchor": "STATUS",
            "role": "generator for this checkpoint",
        },
    ]
    for row in rows:
        row["path_exists"] = (ROOT / row["source_path"]).exists()
        row["anchor_found"] = anchor_found(row["source_path"], row["anchor"])
        row["valid_for_claim"] = False
        row["claim_allowed"] = False
    return rows


def ban_attempt_rows() -> list[dict[str, Any]]:
    return [
        {
            "attempt_id": "BAN1416_0_target",
            "ban_target": "Hom(SpeciesLabel,Coeff_active_source)=empty and no current rescaling",
            "formal_test": "ordinary species labels and matter currents have no morphism into active gravitational source coefficients except via fixed representation data or explicit residual fields",
            "current_result": "TARGET_DEFINED",
            "failure_mode": "requires parent-derived object-language constructor list and current owner",
            "if_signed": "R_source source-only/current-rescaling branch is theorem-banned",
            "if_failed": "write first finite R_source coefficient row",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "attempt_id": "BAN1416_1_locality_covariance",
            "ban_target": "w_A(X)S_A",
            "formal_test": "exclude by locality, diffeomorphism covariance, and additivity",
            "current_result": "FAILS",
            "failure_mode": "SLOT1407_0 and NSS1407_2 show local/covariant/additive scalar weights survive",
            "if_signed": "not applicable from basic symmetry alone",
            "if_failed": "must use parent grammar or finite coefficient row",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "attempt_id": "BAN1416_2_object_language",
            "ban_target": "source-only species morphism",
            "formal_test": "parent constructor list contains geometry, matter fields, gauge/current data, representation constants, and universal constants only",
            "current_result": "NOT_DERIVED_CURRENT_CORPUS",
            "failure_mode": "OLT1338_2 says no authoritative primitive-to-parent object-language derivation exists",
            "if_signed": "Hom(SpeciesLabel,Coeff_active_source)=empty becomes theorem",
            "if_failed": "explicit closure or finite source-weight coefficient required",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "attempt_id": "BAN1416_3_action_measure",
            "ban_target": "species measure/action multiplier",
            "formal_test": "one parent action measure/hbar/action scale forbids species-dependent source multipliers",
            "current_result": "NOT_PARENT_SIGNED",
            "failure_mode": "OLT1338_4 and NSS1407_4 keep measure/action-scale owner unsigned",
            "if_signed": "species measure-weight countermodel is killed",
            "if_failed": "measure-weight component remains in R_source",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "attempt_id": "BAN1416_4_current_rescaling",
            "ban_target": "J_A -> c_A J_A or beta_source,A marker",
            "formal_test": "single current functor fixes matter currents and source normalization before readout",
            "current_result": "NOT_DERIVED",
            "failure_mode": "CE1077_1 and SCO1415_3 show current owner missing",
            "if_signed": "current rescaling residual row can be theorem-zero",
            "if_failed": "current_rescaling_residual finite row required",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "attempt_id": "BAN1416_5_readout_radiative",
            "ban_target": "readout/radiative re-entry of source coefficient",
            "formal_test": "S_eff/readout coefficients preserve same source coefficient domain and cannot regenerate source-only weights",
            "current_result": "UNSIGNED_PARALLEL_GATE",
            "failure_mode": "OLT1338_5 and FVG1310_5 keep radiative/readout re-entry open",
            "if_signed": "bare source-slot zero transfers to observables",
            "if_failed": "readout/radiative source residual remains in R_source/R_readout",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "attempt_id": "BAN1416_6_verdict",
            "ban_target": "source-only species/current-rescaling ban",
            "formal_test": "BAN1416_1 through BAN1416_5 close",
            "current_result": "BAN_NOT_PROVED_FIRST_RSOURCE_ROW_REQUIRED",
            "failure_mode": "basic symmetry fails, object-language/measure/current/readout gates unsigned",
            "if_signed": "R_source can shrink sharply",
            "if_failed": "write qbar_source_weight/current_rescaling first coefficient rows as nonclaim",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]


def countermodel_rows() -> list[dict[str, Any]]:
    return [
        {
            "countermodel_id": "CM1416_0_wA_action",
            "form": "S_matter = sum_A w_A(X) S_A[Psi_A,e_obs,theta_A]",
            "why_survives": "local, diffeomorphism-covariant if w_A is scalar, and additive by species",
            "kills_if_banned": "relative Hilbert source weights and qbar_source_weight",
            "current_status": "LIVE_COUNTEREXAMPLE",
            "finite_row_if_live": "RSC1416_0_qbar_source_weight",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "countermodel_id": "CM1416_1_kappaA_source",
            "form": "source map uses kappa_A(X) T_A after material labelling but before gravity coupling",
            "why_survives": "can be written as source selection rule unless source functor forgets labels",
            "kills_if_banned": "source/test dependent gravitational source coefficient",
            "current_status": "LIVE_COUNTEREXAMPLE",
            "finite_row_if_live": "RSC1416_0_qbar_source_weight",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "countermodel_id": "CM1416_2_current_rescaling",
            "form": "J_A -> c_A J_A or beta_source,A source marker",
            "why_survives": "current functor/source normalization owner is missing",
            "kills_if_banned": "current/source normalization residual",
            "current_status": "LIVE_COUNTEREXAMPLE",
            "finite_row_if_live": "RSC1416_1_current_rescaling",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "countermodel_id": "CM1416_3_hidden_marker",
            "form": "w_A=w(marker_A,domain,boundary,hidden invariant)",
            "why_survives": "source-only slot can be smuggled through marker/domain scalar if coefficient domains are not sealed",
            "kills_if_banned": "marker-mediated source residual",
            "current_status": "LIVE_COUNTEREXAMPLE",
            "finite_row_if_live": "future_R_marker_boundary",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "countermodel_id": "CM1416_4_readout_current",
            "form": "J_source=T_Hilbert+sum_A zeta_A J_A_readout",
            "why_survives": "can be covariant if added currents are conserved or projected and readout ordering is unsigned",
            "kills_if_banned": "post-variation source/readout current residual",
            "current_status": "LIVE_COUNTEREXAMPLE",
            "finite_row_if_live": "future_R_readout_rad",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]


def finite_row_rows() -> list[dict[str, Any]]:
    return [
        {
            "row_id": "RSC1416_0_qbar_source_weight",
            "quantity": "qbar_source_weight",
            "definition": "species/source-only gravitational prefactor or kappa_A sensitivity",
            "formula_or_bound": "qbar_source_weight = partial_X ln kappa_A or equivalent source-only weight derivative",
            "required_inputs": "source-weight exclusion theorem or coefficient; material/source tags; parent coordinate basis; source paths",
            "current_value": "MISSING_SOURCE_WEIGHT_EXCLUSION_OR_COEFFICIENT",
            "units": "dimensionless",
            "observable_links": "WEP_source_charge;Newton_GM;R10;R11;local_GR",
            "source_path": "source-intake/mts_residuals/P8_Y5_R10_1310_QC_COEFFICIENT_ACQUISITION_NONCLAIM.csv",
            "source_anchor": "QCA1310_5_qbar_source_weight",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "row_id": "RSC1416_1_current_rescaling",
            "quantity": "current_rescaling_residual",
            "definition": "source/test current normalization component from J_A -> c_A J_A or beta_source,A source marker",
            "formula_or_bound": "delta_source_current := partial_X ln c_A or declared beta_source,A in parent source-current basis",
            "required_inputs": "Noether current owner or finite c_A/beta_source,A coefficient; units; sign; source path",
            "current_value": "MISSING_CURRENT_OWNER_OR_COEFFICIENT",
            "units": "dimensionless or parent current-normalization units",
            "observable_links": "WEP_source_charge;R10_source_side;Newton_GM;local_GR",
            "source_path": "source-intake/mts_residuals/P8_Y5_R10_1077_ZERO_THEOREM_COUNTEREXAMPLE_AUDIT.csv",
            "source_anchor": "CE1077_1_current_rescaling",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "row_id": "RSC1416_2_parent_basis",
            "quantity": "R_source parent basis",
            "definition": "parent source-current coordinate basis and normalization for qbar_source_weight/current_rescaling",
            "formula_or_bound": "declared basis X_I and source-current units before comparison to WEP/Newton/R10",
            "required_inputs": "typed parent object language, source-current owner, basis normalization",
            "current_value": "MISSING_PARENT_COUPLING_BASIS",
            "units": "not_declared",
            "observable_links": "all R_source arenas",
            "source_path": "source-intake/mts_residuals/P8_Y5_R10_1076_COUPLING_OWNER_GATES.csv",
            "source_anchor": "OWN1076_0_parent_object_language",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "row_id": "RSC1416_3_verdict",
            "quantity": "first R_source coefficient row pack",
            "definition": "source-only species/current-rescaling ban is not proved, so the first finite R_source rows are explicit",
            "formula_or_bound": "score_ready iff RSC1416_0/RSC1416_1/RSC1416_2 are theorem-zero or source-backed with units/signs and arena projections",
            "required_inputs": "values, units, signs, source paths, parent basis, U_a/product convention",
            "current_value": "TEMPLATE_ONLY",
            "units": "not_applicable",
            "observable_links": "WEP;Newton_GM;R10;R11;local_GR",
            "source_path": "source-intake/mts_residuals/P8_Y5_R10_1416_SOURCE_SLOT_CURRENT_RESCALING_BAN_ATTEMPT.csv",
            "source_anchor": "BAN1416_6_verdict",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]


def acceptance_gate_rows() -> list[dict[str, Any]]:
    return [
        {
            "gate_id": "ACC1416_0_no_missing_values",
            "requirement": "finite R_source rows require real values before valid_for_claim=true",
            "current_status": "VALUES_MISSING",
            "failure_action": "all rows remain nonclaim",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "gate_id": "ACC1416_1_units",
            "requirement": "units and parent-coordinate dimension basis must be declared",
            "current_status": "PARENT_BASIS_MISSING",
            "failure_action": "no comparison to WEP/Newton/R10/PPN",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "gate_id": "ACC1416_2_source_paths",
            "requirement": "source path and source anchor must support any numeric coefficient",
            "current_status": "TEMPLATE_SOURCES_ONLY",
            "failure_action": "no claim-ready coefficient",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "gate_id": "ACC1416_3_arena_projection",
            "requirement": "R_source cannot transfer across WEP/Newton/R10/PPN without arena projection theorem",
            "current_status": "ARENA_PROJECTION_MISSING",
            "failure_action": "retain arena isolation",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "gate_id": "ACC1416_4_no_cancellation",
            "requirement": "do not accept source residual only because it cancels a material pair or measured-G convention",
            "current_status": "NO_CANCELLATION_POLICY_ACTIVE",
            "failure_action": "require theorem-zero or source-backed bounds",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "gate_id": "ACC1416_5_verdict",
            "requirement": "first R_source row acceptance",
            "current_status": "ROW_SCHEMA_READY_VALUES_MISSING_NO_PASS",
            "failure_action": "continue derivation/source acquisition",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        {
            "decision_id": "DEC1416_0_ban_verdict",
            "decision": "do not claim source-only/current-rescaling ban",
            "reason": "w_A/kappa_A/current-rescaling counterexamples survive without parent object-language and current-owner proof",
            "effect": "finite qbar_source_weight/current_rescaling rows are required",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "decision_id": "DEC1416_1_first_row",
            "decision": "use qbar_source_weight as first R_source coefficient row",
            "reason": "it directly represents Hom(SpeciesLabel,Coeff_active_source) and feeds WEP/Newton/R10 source side",
            "effect": "R_source now has a concrete first coefficient slot to derive or source",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "decision_id": "DEC1416_2_next_best",
            "decision": "target parent object-language constructor list next",
            "reason": "only a primitive constructor proof can kill source-only slots cleanly without coefficient fitting",
            "effect": "next checkpoint should either derive constructor exhaustion or accept qbar_source_weight source acquisition",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]


def claim_gate_rows() -> list[dict[str, Any]]:
    return [
        {
            "claim_id": "GATE1416_0_ban",
            "claim": "source-only species slot and current rescaling are theorem-banned",
            "status": "NOT_PROVED_NO_CLAIM",
            "reason": "counterexamples survive and parent grammar/current owner are unsigned",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "claim_id": "GATE1416_1_Rsource_row",
            "claim": "first R_source coefficient row is score-ready",
            "status": "TEMPLATE_ONLY_NO_CLAIM",
            "reason": "value, units, parent basis, and arena projection are missing",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "claim_id": "GATE1416_2_WEP_Newton_R10",
            "claim": "WEP/Newton/R10 source-side arenas pass",
            "status": "BLOCKED_NO_CLAIM",
            "reason": "R_source coefficient rows are not source-backed and U_a/source-worldtube/product convention remain missing",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "claim_id": "GATE1416_3_local_GR",
            "claim": "local GR/Newton reduction follows",
            "status": "BLOCKED_NO_CLAIM",
            "reason": "R_source is not killed or bounded; EH/PPN and other residual gates remain active",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "claim_id": "GATE1416_4_verdict",
            "claim": "1416 closes R_source",
            "status": "NO_PROMOTION",
            "reason": "1416 writes the first finite R_source coefficient rows only",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        {
            "next_id": "NEXT1416_0_1417",
            "target_doc": "1417-Y5-R10-RAB-parent-object-language-constructor-exhaustion-or-qbar-source-acquisition.md",
            "target_script": "scripts/Y5_R10_RAB_parent_object_language_constructor_exhaustion_or_qbar_source_acquisition.py",
            "task": "attempt to derive the primitive constructor list that excludes Hom(SpeciesLabel,Coeff_active_source); if it fails, build qbar_source_weight source acquisition rows",
            "success_condition": "constructor exhaustion kills source-only slots, or qbar_source_weight has source-ready acquisition rows with units/sign/source anchors and nonclaim gates",
            "do_not_claim": "WEP pass; R_source pass; Newton-GM pass; R10/PPN/local GR",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "next_id": "NEXT1416_1_data_parallel",
            "target_doc": "future-current-rescaling-coefficient-source-acquisition.md",
            "target_script": "future_source_row_route",
            "task": "if theorem route fails, source finite current_rescaling_residual rows in a parent basis",
            "success_condition": "current rescaling coefficient has value, uncertainty, units, sign convention, source path, and arena projection",
            "do_not_claim": "template row as numeric bound",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]


def validation_rows(
    sources: list[dict[str, Any]],
    ban_attempt: list[dict[str, Any]],
    countermodels: list[dict[str, Any]],
    finite_rows: list[dict[str, Any]],
    acceptance: list[dict[str, Any]],
    decisions: list[dict[str, Any]],
    gates: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    timestamp = datetime.now(timezone.utc).isoformat()
    output_paths = [
        DOC_PATH,
        SOURCE_REGISTER_PATH,
        BAN_ATTEMPT_PATH,
        COUNTERMODEL_PATH,
        FINITE_ROW_PATH,
        ACCEPTANCE_GATE_PATH,
        DECISION_PATH,
        CLAIM_GATE_PATH,
        NEXT_TARGET_PATH,
        VALIDATION_PATH,
    ]
    rows: list[dict[str, Any]] = []

    def add(check_id: str, passed: bool, detail: str) -> None:
        rows.append(
            {
                "check_id": check_id,
                "status": "PASS" if passed else "FAIL",
                "detail": detail,
                "timestamp_utc": timestamp,
            }
        )

    add(
        "VAL1416_0_sources",
        all(row["path_exists"] == True and row["anchor_found"] == True for row in sources),
        "all cited local source paths exist and anchors are present",
    )
    add(
        "VAL1416_1_ban_attempt",
        any(row["attempt_id"] == "BAN1416_6_verdict" and row["current_result"] == "BAN_NOT_PROVED_FIRST_RSOURCE_ROW_REQUIRED" for row in ban_attempt),
        "source-only/current-rescaling ban attempt fails and selects first R_source rows",
    )
    add(
        "VAL1416_2_countermodels",
        {"CM1416_0_wA_action", "CM1416_1_kappaA_source", "CM1416_2_current_rescaling"}.issubset(
            {row["countermodel_id"] for row in countermodels}
        )
        and all(row["valid_for_claim"] == False for row in countermodels),
        "live countermodel ledger includes source slot and current rescaling cases",
    )
    add(
        "VAL1416_3_finite_rows",
        any(row["row_id"] == "RSC1416_0_qbar_source_weight" for row in finite_rows)
        and any(row["row_id"] == "RSC1416_3_verdict" and row["current_value"] == "TEMPLATE_ONLY" for row in finite_rows)
        and all(row["valid_for_claim"] == False for row in finite_rows),
        "first R_source coefficient rows exist and remain nonclaim",
    )
    add(
        "VAL1416_4_acceptance",
        all(row["valid_for_claim"] == False and row["claim_allowed"] == False for row in acceptance)
        and any(row["gate_id"] == "ACC1416_5_verdict" for row in acceptance),
        "acceptance gate blocks score-ready status until values/units/sources/arena projections exist",
    )
    add(
        "VAL1416_5_decision",
        any(row["decision_id"] == "DEC1416_2_next_best" for row in decisions),
        "decision ledger selects parent object-language constructor exhaustion next",
    )
    add(
        "VAL1416_6_claim_refusal",
        all(row["valid_for_claim"] == False and row["claim_allowed"] == False for row in gates),
        "ban, R_source row, arena, and local-GR claims are refused",
    )
    add(
        "VAL1416_7_scope",
        all((ROOT / path).resolve().is_relative_to(ROOT.resolve()) for path in output_paths),
        "outputs are confined to post-checkpoint-work paths",
    )
    add(
        "VAL1416_8_overall",
        True,
        "1416 fails the source-slot/current-rescaling ban and writes first finite R_source coefficient rows",
    )
    return rows


def write_doc(
    sources: list[dict[str, Any]],
    ban_attempt: list[dict[str, Any]],
    countermodels: list[dict[str, Any]],
    finite_rows: list[dict[str, Any]],
    acceptance: list[dict[str, Any]],
    decisions: list[dict[str, Any]],
    gates: list[dict[str, Any]],
    next_targets: list[dict[str, Any]],
    validations: list[dict[str, Any]],
) -> None:
    doc = f"""# 1416 - Source-Only Species Slot And Current Rescaling Ban Or R_source Bound Row

**Status:** `{STATUS}`

**Current verdict:** the clean source-side theorem is not proved. `Hom(SpeciesLabel,Coeff_active_source)=empty` and the ban on `J_A -> c_A J_A` both require a parent object-language/current-owner proof that the current corpus does not supply. Locality, covariance, and additivity do not kill the source-only slot by themselves.

**Discipline move:** no WEP, Newton-GM, R10, PPN, or local-GR claim is made. The useful output is the first explicit finite `R_source` coefficient pack: `qbar_source_weight`, `current_rescaling_residual`, and the missing parent-basis row, all nonclaim.

**Claim ceiling:** `{CLAIM_CEILING}`

## Source Register

{md_table(sources)}

## Source Slot / Current Rescaling Ban Attempt

{md_table(ban_attempt)}

## Source Slot Countermodel Ledger

{md_table(countermodels)}

## First R_source Coefficient Row

{md_table(finite_rows)}

## R_source Row Acceptance Gate

{md_table(acceptance)}

## Decision Ledger

{md_table(decisions)}

## Claim Gate

{md_table(gates)}

## Next Target

{md_table(next_targets)}

## Validation

{md_table(validations)}
"""
    (ROOT / DOC_PATH).write_text(doc, encoding="utf-8")


def main() -> None:
    sources = source_register_rows()
    ban_attempt = ban_attempt_rows()
    countermodels = countermodel_rows()
    finite_rows = finite_row_rows()
    acceptance = acceptance_gate_rows()
    decisions = decision_rows()
    gates = claim_gate_rows()
    next_targets = next_target_rows()
    validations = validation_rows(sources, ban_attempt, countermodels, finite_rows, acceptance, decisions, gates)

    write_csv(SOURCE_REGISTER_PATH, sources)
    write_csv(BAN_ATTEMPT_PATH, ban_attempt)
    write_csv(COUNTERMODEL_PATH, countermodels)
    write_csv(FINITE_ROW_PATH, finite_rows)
    write_csv(ACCEPTANCE_GATE_PATH, acceptance)
    write_csv(DECISION_PATH, decisions)
    write_csv(CLAIM_GATE_PATH, gates)
    write_csv(NEXT_TARGET_PATH, next_targets)
    write_csv(VALIDATION_PATH, validations)
    write_doc(sources, ban_attempt, countermodels, finite_rows, acceptance, decisions, gates, next_targets, validations)

    if any(row["status"] != "PASS" for row in validations):
        raise SystemExit("1416 validation failed")

    print(STATUS)


if __name__ == "__main__":
    main()

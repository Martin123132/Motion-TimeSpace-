from __future__ import annotations

import csv
import shutil
import subprocess
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


BRANCH_ID = "MTS_R2FR_CURRENT_OWNER_NORMAL_FORM_OR_SOURCEGM_RESIDUAL_FIRST_ROW_2345"

ROOT = Path(__file__).resolve().parents[1]
PROJECT = ROOT.parent
FORMALIZATION = PROJECT / "formalization-workbench"
OUT = ROOT / "source-intake" / "mts_residuals"
RAB_QUEUE = ROOT / "source-intake" / "rab-sector" / "acquisition-queue"
MICRO_RESIDUALS = ROOT / "source-intake" / "microscope" / "branch_locked_wep" / "residuals"
BETA_DOCS = ROOT / "source-intake" / "beta-source" / "docs"

DOC = ROOT / "2345-Y5-R2FR-current-owner-normal-form-from-parent-variation-or-sourceGM-residual-first-row.md"

PATHS = {
    "2344_doc": ROOT / "2344-Y5-R2FR-parent-source-blind-matter-functor-current-owner-or-sourceGM-bound.md",
    "2344_validation": OUT / "P8_Y5_BRR545_2344_VALIDATION.csv",
    "2344_next": OUT / "P8_Y5_PARENT_QLOC_2344_NEXT_TARGET.csv",
    "2344_bounds": OUT / "P8_Y5_PARENT_QLOC_2344_SOURCEGM_BOUND_ACQUISITION_SCHEMA.csv",
    "2344_countermodels": OUT / "P8_Y5_PARENT_QLOC_2344_COUNTERMODEL_KILL_MATRIX.csv",
    "1798_parent_current": OUT / "P8_Y5_PARENT_QLOC_1798_PARENT_CURRENT_OWNER_ATTEMPT.csv",
    "1889_ward_owner": OUT / "P8_Y5_PARENT_QLOC_1889_SOURCE_CURRENT_WARD_OWNER_ATTEMPT.csv",
    "1899_action_current": OUT / "P8_Y5_PARENT_QLOC_1899_ACTION_CURRENT_OWNER_LEMMA_ATTEMPT.csv",
    "1958_nonhilbert": OUT / "P8_Y5_PARENT_QLOC_1958_CURRENT_OWNER_NONHILBERT_ATTEMPT.csv",
    "1687_common_owner": OUT / "P8_Y5_PARENT_QLOC_1687_COMMON_ACTION_MEASURE_CURRENT_OWNER_PROOF_ATTEMPT.csv",
    "1677_source_owner": OUT / "P8_Y5_PARENT_QLOC_1677_SOURCE_CURRENT_OWNER_ATTEMPT.csv",
    "1680_zero_clauses": OUT / "P8_Y5_PARENT_QLOC_1680_SOURCE_CURRENT_OWNER_ZERO_THEOREM_CLAUSES.csv",
    "2097_current_owner": OUT / "P8_Y5_PARENT_QLOC_2097_CURRENT_OWNER_ATTEMPT.csv",
    "1079_narrow_owner": OUT / "P8_Y5_R10_1079_NARROW_CURRENT_OWNER_THEOREM_ATTEMPT.csv",
    "1079_premises": OUT / "P8_Y5_R10_1079_CURRENT_OWNER_PREMISE_LEDGER.csv",
    "1453_source_norm": OUT / "P8_Y5_R10_1453_CURRENT_SOURCE_NORMALIZATION_OWNER_THEOREM_ATTEMPT.csv",
    "1425_synthesis": OUT / "P8_Y5_R10_1425_CURRENT_OWNER_SYNTHESIS.csv",
    "990_contract": OUT / "P8_Y5_R10_990_PARENT_ACTION_CONTRACT.csv",
}

SOURCES = [
    ("SRC2345_00_2344_doc", "2344_doc", ["CO2344_5_verdict", "NEXT2344_0"], "2344 handoff to current-owner normal form"),
    ("SRC2345_01_2344_validation", "2344_validation", ["VAL2344_OVERALL", "PASS"], "2344 validation"),
    ("SRC2345_02_2344_next", "2344_next", ["NEXT2344_0", "current-owner-normal-form"], "machine-readable 2345 target"),
    ("SRC2345_03_2344_bounds", "2344_bounds", ["SGB2344_1_current_owner", "epsilon_current_owner_NH_abs"], "2344 current-owner residual schema"),
    ("SRC2345_04_2344_countermodels", "2344_countermodels", ["CKM2344_4_nonhilbert_current", "SURVIVES_CURRENT_OWNER_UNSIGNED"], "2344 non-Hilbert current countermodel"),
    ("SRC2345_05_1798_parent_current", "1798_parent_current", ["PCO1798_0_parent_action_current", "PCO1798_6_verdict"], "parent Theta/Qtau current owner attempt"),
    ("SRC2345_06_1889_ward_owner", "1889_ward_owner", ["SWO1889_4_total_variation_route", "SWO1889_7_verdict"], "Ward owner and pre-action weight limit"),
    ("SRC2345_07_1899_action_current", "1899_action_current", ["ACO1899_3_classical_rescale_obstruction", "ACO1899_6_verdict"], "action/current owner lemma attempt"),
    ("SRC2345_08_1958_nonhilbert", "1958_nonhilbert", ["OWN1958_2_canonical_to_Hilbert_improvement", "OWN1958_6_verdict"], "non-Hilbert current owner obstruction"),
    ("SRC2345_09_1687_common_owner", "1687_common_owner", ["COM1687_3_action_scale", "COM1687_6_verdict"], "common action-measure-current owner attempt"),
    ("SRC2345_10_1677_source_owner", "1677_source_owner", ["SCO1677_5_verdict", "SOURCE_CURRENT_OWNER_NOT_DERIVED"], "source-current owner status"),
    ("SRC2345_11_1680_zero_clauses", "1680_zero_clauses", ["single_source_current_owner", "variation_before_readout"], "source-current zero theorem clauses"),
    ("SRC2345_12_2097_current_owner", "2097_current_owner", ["CUR2097_7_verdict", "current owner/non-Hilbert/readout silence"], "latest current-owner non-Hilbert/readout failure"),
    ("SRC2345_13_1079_narrow_owner", "1079_narrow_owner", ["NCO1079_5_species_action_weight", "NCO1079_6_verdict"], "narrow current-owner theorem attempt"),
    ("SRC2345_14_1079_premises", "1079_premises", ["PR1079_4_no_pre_action_species_weight", "NOT_SIGNED"], "current-owner premise ledger"),
    ("SRC2345_15_1453_source_norm", "1453_source_norm", ["CSO1453_5_pre_variation_weight", "CSO1453_7_verdict"], "source-normalization current owner theorem attempt"),
    ("SRC2345_16_1425_synthesis", "1425_synthesis", ["CUR1425_1_pre_variation_wall", "LIVE_COUNTERMODEL"], "current-owner synthesis"),
    ("SRC2345_17_990_contract", "990_contract", ["PAC990_2_matter_functor", "PAC990_5_Ward_Bianchi"], "parent action contract"),
]

OUTPUTS = {
    "sources": OUT / "P8_Y5_PARENT_QLOC_2345_SOURCE_REGISTER.csv",
    "normal_form": OUT / "P8_Y5_PARENT_QLOC_2345_CURRENT_OWNER_NORMAL_FORM_AUDIT.csv",
    "variation": OUT / "P8_Y5_PARENT_QLOC_2345_PARENT_VARIATION_SPLIT_AUDIT.csv",
    "residual": OUT / "P8_Y5_PARENT_QLOC_2345_SOURCEGM_CURRENT_OWNER_RESIDUAL_FIRST_ROW.csv",
    "countermodels": OUT / "P8_Y5_PARENT_QLOC_2345_COUNTERMODEL_STATUS.csv",
    "decision": OUT / "P8_Y5_PARENT_QLOC_2345_DECISION_LEDGER.csv",
    "claims": OUT / "P8_Y5_PARENT_QLOC_2345_CLAIM_GATES.csv",
    "refusal": OUT / "P8_Y5_PARENT_QLOC_2345_REFUSAL_RUNNER.csv",
    "next": OUT / "P8_Y5_PARENT_QLOC_2345_NEXT_TARGET.csv",
    "copies": OUT / "P8_Y5_PARENT_QLOC_2345_BRANCH_COPIES.csv",
    "validation": OUT / "P8_Y5_BRR545_2345_VALIDATION.csv",
}

BRANCH_COPY_SPECS = [
    ("COPY2345_0_normal_form", OUTPUTS["normal_form"], BETA_DOCS / "CURRENT_OWNER_NORMAL_FORM_AUDIT_2345_NONCLAIM.csv"),
    ("COPY2345_1_residual", OUTPUTS["residual"], MICRO_RESIDUALS / "SOURCEGM_CURRENT_OWNER_RESIDUAL_FIRST_ROW_2345_NONCLAIM.csv"),
    ("COPY2345_2_decision", OUTPUTS["decision"], RAB_QUEUE / "JR2345_CURRENT_OWNER_DECISION_LEDGER_NONCLAIM.csv"),
]


def timestamp() -> str:
    return datetime.now(timezone.utc).isoformat()


def bool_text(value: bool) -> str:
    return "true" if value else "false"


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def read_csv_rows(path: Path) -> list[dict[str, str]]:
    with path.open("r", newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, Any]], fieldnames: list[str] | None = None) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if fieldnames is None:
        fieldnames = []
        for row in rows:
            for key in row:
                if key not in fieldnames:
                    fieldnames.append(key)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def markdown_table(rows: list[dict[str, Any]], columns: list[str]) -> str:
    header = "| " + " | ".join(columns) + " |"
    separator = "| " + " | ".join("---" for _ in columns) + " |"
    body = []
    for row in rows:
        values = []
        for column in columns:
            value = str(row.get(column, "")).replace("|", "\\|").replace("\n", " ")
            values.append(value)
        body.append("| " + " | ".join(values) + " |")
    return "\n".join([header, separator, *body])


def build_sources() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for row_id, source_key, needles, role in SOURCES:
        path = PATHS[source_key]
        exists = path.exists()
        text = read_text(path) if exists else ""
        missing = [needle for needle in needles if needle not in text]
        rows.append(
            {
                "timestamp_utc": timestamp(),
                "branch_id": BRANCH_ID,
                "row_id": row_id,
                "source_key": source_key,
                "source_path": str(path),
                "exists": bool_text(exists),
                "required": "true",
                "needles": ";".join(needles),
                "needles_found": bool_text(exists and not missing),
                "missing_needles": ";".join(missing),
                "source_role": role,
                "valid_for_claim": "false",
            }
        )
    return rows


def build_normal_form_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "row_id": "CNF2345_0_target",
            "normal_form_piece": "current-owner normal form",
            "formal_statement": "S_parent=S_geom[g_obs]+S_matter[Psi,e_obs,theta_rep]+S_res, with J_active := delta S_matter/delta e_obs plus explicitly retained residual currents before readout.",
            "status": "TARGET_SHARPENED",
            "derived_content": "separates the exact Hilbert-owner subtheorem from residual channels",
            "remaining_gap": "prove S_res has no local source projection or bound it",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "CNF2345_1_hilbert_owner",
            "normal_form_piece": "Hilbert/coframe source owner",
            "formal_statement": "If ordinary matter couples only through e_obs/g_obs and variation is performed before readout, T_H := delta S_matter/delta e_obs is the unique source contributed by S_matter.",
            "status": "EXACT_CONDITIONAL_SUBTHEOREM",
            "derived_content": "post-variation source rescaling cannot redefine the field equation",
            "remaining_gap": "common action/domain and variation-before-readout must be parent-signed",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "CNF2345_2_ward_bianchi",
            "normal_form_piece": "Ward/Bianchi compatibility",
            "formal_statement": "Diffeomorphism invariance gives covariant conservation of the Hilbert source on matter shell.",
            "status": "VALID_COMPATIBILITY_NOT_UNIVERSALITY",
            "derived_content": "the source can be conserved in the observed geometry",
            "remaining_gap": "conservation permits weighted sums if weights are admitted before variation",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "CNF2345_3_pre_action_wall",
            "normal_form_piece": "pre-action species weights",
            "formal_statement": "S_matter=sum_A w_A S_A yields T_H=sum_A w_A T_A; current ownership after action selection does not erase w_A.",
            "status": "LIVE_OBSTRUCTION",
            "derived_content": "proves why current-owner alone cannot close source universality",
            "remaining_gap": "requires source-blind parent syntax / NoSourceOnlySpeciesSlot",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "CNF2345_4_nonhilbert_split",
            "normal_form_piece": "active current residual split",
            "formal_statement": "J_active = J_Hilbert + J_spin/torsion + J_boundary + J_readout + J_improvement + J_shadow_connection.",
            "status": "RETAIN_SPLIT",
            "derived_content": "all non-Hilbert channels are visible as residuals instead of hidden inside GM",
            "remaining_gap": "prove each projected channel zero or source-bound it",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "CNF2345_5_readout_order",
            "normal_form_piece": "variation before readout",
            "formal_statement": "Readout/projection maps may measure or bound J_active but cannot retroactively define the parent source that varied the metric.",
            "status": "EXACT_IF_PARENT_READOUT_ORDER_SIGNED",
            "derived_content": "kills post-variation source selector cheats",
            "remaining_gap": "radiative/readout stability and arena kernel ownership remain unsigned",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "CNF2345_6_verdict",
            "normal_form_piece": "derive current-owner normal form from current corpus",
            "formal_statement": "Current MTS gives a strong partial theorem: Hilbert owner after action selection is exact, but pre-action weights and non-Hilbert/readout tails remain live.",
            "status": "PARTIAL_THEOREM_NOT_CLOSED",
            "derived_content": "post-variation current rescaling route is pruned; residual channels are now explicit",
            "remaining_gap": "source-blind parent syntax plus non-Hilbert/readout zero or finite residual rows",
            "valid_for_claim": "false",
        },
    ]


def build_variation_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "row_id": "PVS2345_0_total_variation",
            "variation_clause": "total parent variation",
            "normal_form": "delta S_parent = E_g delta g_obs + E_Psi delta Psi + E_X delta X + dTheta_total",
            "status": "FORM_REQUIRED_NOT_FULLY_SOURCE_WRITTEN",
            "if_missing": "cannot prove all local source terms are owned by the same variation",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "PVS2345_1_matter_variation",
            "variation_clause": "ordinary matter variation",
            "normal_form": "delta S_matter = E_Psi delta Psi + T_H dot delta e_obs + dTheta_matter",
            "status": "EXACT_GIVEN_COMMON_ACTION",
            "if_missing": "source tensor remains undefined or arena-selected",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "PVS2345_2_connection_channel",
            "variation_clause": "connection/hypermomentum channel",
            "normal_form": "omega=omega[e_obs] or P_source[J_spin/torsion/nonmetricity]=0/bounded",
            "status": "UNSIGNED",
            "if_missing": "spin/torsion/nonmetricity can carry active local source",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "PVS2345_3_boundary_channel",
            "variation_clause": "boundary/improvement source channel",
            "normal_form": "integral_boundary B_improvement has zero local source projection or explicit bound",
            "status": "UNSIGNED",
            "if_missing": "improvement or worldtube flux shifts measured active mass",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "PVS2345_4_readout_channel",
            "variation_clause": "readout no-reentry",
            "normal_form": "K_readout acts after J_active and cannot introduce source/species labels into the parent current",
            "status": "UNSIGNED",
            "if_missing": "readout selector can manufacture or hide apparent source residuals",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "PVS2345_5_common_action_scale",
            "variation_clause": "common action scale",
            "normal_form": "one common matter-action scale is absorbed into kappa/G; relative species scales are forbidden or residualized",
            "status": "COMMON_MODE_EXACT_RELATIVE_MODE_UNSIGNED",
            "if_missing": "measured GM absorbs too much and hides WEP/PPN/R10 leakage",
            "valid_for_claim": "false",
        },
    ]


def build_residual_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "row_id": "RCO2345_0_schema",
            "quantity": "epsilon_current_owner_NH_abs",
            "component": "total_nonhilbert_current_owner_residual",
            "formula": "||P_source[J_spin/torsion + J_boundary + J_readout + J_improvement + J_shadow_connection]|| / ||P_source[J_Hilbert]||",
            "units": "dimensionless",
            "current_value": "MISSING_COMPONENT_VALUES",
            "required_source_or_zero": "parent current-owner zero theorem or numeric component rows",
            "observable_links": "local_GR;Newton_GM;PPN;WEP;R10;orbital",
            "score_ready": "false",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "RCO2345_1_spin_torsion",
            "quantity": "epsilon_spin_torsion_abs",
            "component": "spin/torsion/nonmetricity source projection",
            "formula": "||P_source[J_spin/torsion/nonmetricity]|| / ||P_source[J_Hilbert]||",
            "units": "dimensionless",
            "current_value": "MISSING_TORSION_CONNECTION_PROJECTION",
            "required_source_or_zero": "Levi-Civita/torsionless parent proof or hypermomentum projection bound",
            "observable_links": "PPN;local_GR;spin_source_tests",
            "score_ready": "false",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "RCO2345_2_boundary",
            "quantity": "epsilon_boundary_source_abs",
            "component": "boundary/worldtube/improvement flux",
            "formula": "||P_source[J_boundary + J_improvement]|| / ||P_source[J_Hilbert]||",
            "units": "dimensionless",
            "current_value": "MISSING_BOUNDARY_FLUX_PROJECTION",
            "required_source_or_zero": "zero local boundary flux theorem or finite source-worldtube flux bound",
            "observable_links": "Newton_GM;orbital;PPN",
            "score_ready": "false",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "RCO2345_3_readout",
            "quantity": "epsilon_readout_current_reentry_abs",
            "component": "readout/source-label reentry",
            "formula": "||P_source[K_readout(J_H,A,marker)-K_readout(J_H)]|| / ||P_source[J_Hilbert]||",
            "units": "dimensionless",
            "current_value": "MISSING_READOUT_SELECTOR_LEAKAGE",
            "required_source_or_zero": "variation-before-readout/radiative stability theorem or leakage coefficient",
            "observable_links": "WEP;R10;clock;PPN",
            "score_ready": "false",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "RCO2345_4_shadow_connection",
            "quantity": "epsilon_shadow_connection_abs",
            "component": "independent shadow connection/coframe source",
            "formula": "||P_source[J_shadow_connection]|| / ||P_source[J_Hilbert]||",
            "units": "dimensionless",
            "current_value": "MISSING_SHADOW_CONNECTION_PROJECTION",
            "required_source_or_zero": "single observed coframe/connection descent theorem or finite c_g/b_dis/q_nonH row",
            "observable_links": "R10;PPN;clocks;local_GR",
            "score_ready": "false",
            "valid_for_claim": "false",
        },
    ]


def build_countermodel_rows() -> list[dict[str, Any]]:
    return [
        {"branch_id": BRANCH_ID, "row_id": "CM2345_0_post_variation_rescale", "countermodel": "J_A -> c_A J_A after T_H is extracted", "status": "CONDITIONALLY_KILLED", "why": "post-variation maps cannot redefine the source in the parent field equation if readout order is signed", "residual_if_unsigned": "epsilon_readout_current_reentry_abs", "valid_for_claim": "false"},
        {"branch_id": BRANCH_ID, "row_id": "CM2345_1_pre_action_weight", "countermodel": "S_matter=sum_A w_A S_A before variation", "status": "SURVIVES_CURRENT_OWNER_ALONE", "why": "Hilbert variation inherits weights already inside S_matter", "residual_if_unsigned": "epsilon_source_GM_rel_abs", "valid_for_claim": "false"},
        {"branch_id": BRANCH_ID, "row_id": "CM2345_2_nonhilbert_tail", "countermodel": "J_NH contributes to active local source", "status": "SURVIVES_NONHILBERT_SILENCE_UNSIGNED", "why": "current owner of S_matter does not automatically erase spin/torsion/boundary/readout tails", "residual_if_unsigned": "epsilon_current_owner_NH_abs", "valid_for_claim": "false"},
        {"branch_id": BRANCH_ID, "row_id": "CM2345_3_bianchi_weighted_total", "countermodel": "weighted total source is conserved", "status": "SURVIVES_WARD_ONLY", "why": "Bianchi/Ward conservation is compatible with separately conserved weighted sectors", "residual_if_unsigned": "epsilon_kappaA_source_abs", "valid_for_claim": "false"},
        {"branch_id": BRANCH_ID, "row_id": "CM2345_4_verdict", "countermodel": "current-owner shortcut closes local GR/Newton source side", "status": "REJECTED", "why": "only post-variation rescale is conditionally killed; pre-action and non-Hilbert residuals remain", "residual_if_unsigned": "sourceGM_total_residual_required", "valid_for_claim": "false"},
    ]


def build_decision_rows() -> list[dict[str, Any]]:
    return [
        {"branch_id": BRANCH_ID, "row_id": "DEC2345_0_result", "decision": "do not claim current-owner normal form as parent-derived", "reason": "Hilbert owner is exact after common action selection, but the common action syntax, non-Hilbert silence and readout stability are unsigned", "consequence": "local GR/Newton source side remains blocked", "status": "PARTIAL_THEOREM_RETAIN_RESIDUAL", "valid_for_claim": "false"},
        {"branch_id": BRANCH_ID, "row_id": "DEC2345_1_real_win", "decision": "treat post-variation rescaling as conditionally killed", "reason": "once the field equation is varied, downstream source selectors cannot redefine its source", "consequence": "one class of coupling cheat is pruned from future routes", "status": "POST_VARIATION_ROUTE_PRUNED", "valid_for_claim": "false"},
        {"branch_id": BRANCH_ID, "row_id": "DEC2345_2_first_residual", "decision": "install epsilon_current_owner_NH_abs as first strict sourceGM residual row", "reason": "non-Hilbert/boundary/readout/shadow-connection tails must be zero-proved or bounded", "consequence": "future empirical branches get a single current-owner residual input rather than vague caveats", "status": "RESIDUAL_SCHEMA_INSTALLED_NONCLAIM", "valid_for_claim": "false"},
        {"branch_id": BRANCH_ID, "row_id": "DEC2345_3_next", "decision": "attack non-Hilbert source projection zero before more public or empirical claims", "reason": "this is the remaining local-GR source-current obstruction after the partial Hilbert-owner win", "consequence": "next target is a zero-proof or component-bound pack for J_NH", "status": "SELECT_NONHILBERT_SOURCE_ZERO_NEXT", "valid_for_claim": "false"},
        {"branch_id": BRANCH_ID, "row_id": "DEC2345_4_public_policy", "decision": "no GitHub update from 2345", "reason": "private derivation triage and residual schema, not public claim material", "consequence": "continue private goal work", "status": "NO_GITHUB_EVIDENCE_UPDATE", "valid_for_claim": "false"},
    ]


def build_claim_rows() -> list[dict[str, Any]]:
    return [
        {"branch_id": BRANCH_ID, "row_id": "CG2345_0_common_action", "gate": "one common matter action parent-signed", "passed": "false", "claim_effect": "pre-action weights remain possible", "valid_for_claim": "false"},
        {"branch_id": BRANCH_ID, "row_id": "CG2345_1_hilbert_owner", "gate": "Hilbert owner after action selection", "passed": "true", "claim_effect": "partial theorem only; not enough for local GR/Newton", "valid_for_claim": "false"},
        {"branch_id": BRANCH_ID, "row_id": "CG2345_2_nonhilbert_zero", "gate": "non-Hilbert/boundary/readout source projection zero", "passed": "false", "claim_effect": "epsilon_current_owner_NH_abs remains live", "valid_for_claim": "false"},
        {"branch_id": BRANCH_ID, "row_id": "CG2345_3_readout_stability", "gate": "variation-before-readout stability parent-signed", "passed": "false", "claim_effect": "readout reentry remains live", "valid_for_claim": "false"},
        {"branch_id": BRANCH_ID, "row_id": "CG2345_4_residual_score_ready", "gate": "current-owner residual row score-ready", "passed": "false", "claim_effect": "component values/source paths missing", "valid_for_claim": "false"},
        {"branch_id": BRANCH_ID, "row_id": "CG2345_5_local_GR_Newton", "gate": "local GR/Newton source recovery derived", "passed": "false", "claim_effect": "source-current residual still blocks claim", "valid_for_claim": "false"},
        {"branch_id": BRANCH_ID, "row_id": "CG2345_6_github", "gate": "safe public GitHub update", "passed": "false", "claim_effect": "private checkpoint only", "valid_for_claim": "false"},
    ]


def build_refusal_rows() -> list[dict[str, Any]]:
    return [
        {"branch_id": BRANCH_ID, "row_id": "REF2345_0_hilbert_to_full", "claim": "Hilbert owner subtheorem proves full current-owner normal form", "allowed": "false", "reason": "pre-action weights and non-Hilbert/readout tails survive", "blocking_rows": "CNF2345_3_pre_action_wall;CNF2345_4_nonhilbert_split", "valid_for_claim": "false"},
        {"branch_id": BRANCH_ID, "row_id": "REF2345_1_ward_to_universal", "claim": "Ward/Bianchi identity proves universal source coupling", "allowed": "false", "reason": "weighted conserved sums are still compatible with conservation", "blocking_rows": "CNF2345_2_ward_bianchi;CM2345_3_bianchi_weighted_total", "valid_for_claim": "false"},
        {"branch_id": BRANCH_ID, "row_id": "REF2345_2_rescale", "claim": "field/action rescaling removes w_A source weights", "allowed": "false", "reason": "variation with respect to geometry still sees w_A unless the parent language forbids it", "blocking_rows": "CNF2345_3_pre_action_wall;CM2345_1_pre_action_weight", "valid_for_claim": "false"},
        {"branch_id": BRANCH_ID, "row_id": "REF2345_3_hide_in_GM", "claim": "current-owner residual can be absorbed into measured GM", "allowed": "false", "reason": "structured non-Hilbert/readout/source-label pieces are not one common calibration mode", "blocking_rows": "RCO2345_0_schema;CG2345_4_residual_score_ready", "valid_for_claim": "false"},
        {"branch_id": BRANCH_ID, "row_id": "REF2345_4_local_claim", "claim": "2345 proves local GR/Newton source recovery", "allowed": "false", "reason": "2345 records a partial theorem and first residual row, not a closed source-side reduction", "blocking_rows": "DEC2345_0_result;CG2345_5_local_GR_Newton", "valid_for_claim": "false"},
    ]


def build_next_rows() -> list[dict[str, Any]]:
    return [
        {"branch_id": BRANCH_ID, "row_id": "NEXT2345_0", "next_target": "2346-Y5-R2FR-nonHilbert-source-projection-zero-or-component-bound-pack.md", "why": "the post-variation current-owner win leaves the non-Hilbert/boundary/readout source projection as the sharpest local-GR source obstruction", "route_type": "private_derivation_next_step", "valid_for_claim": "false"},
        {"branch_id": BRANCH_ID, "row_id": "NEXT2345_1", "next_target": "2346b-Y5-R2FR-current-owner-residual-component-acquisition.md", "why": "fallback if the non-Hilbert source projection cannot be theorem-zeroed", "route_type": "fallback_nonclaim", "valid_for_claim": "false"},
        {"branch_id": BRANCH_ID, "row_id": "NEXT2345_2", "next_target": "2346c-Y5-R2FR-source-blind-parent-action-adoption-decision.md", "why": "decision route for whether the exact normal form becomes the minimal parent action definition if deeper derivation stalls", "route_type": "closure_or_adoption_decision", "valid_for_claim": "false"},
    ]


def copy_branch_outputs() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for row_id, source, destination in BRANCH_COPY_SPECS:
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(source, destination)
        rows.append(
            {
                "timestamp_utc": timestamp(),
                "branch_id": BRANCH_ID,
                "row_id": row_id,
                "source_csv": str(source.relative_to(ROOT)),
                "branch_copy_path": str(destination),
                "copy_exists": bool_text(destination.exists()),
                "row_count": len(read_csv_rows(destination)),
                "valid_for_claim": "false",
            }
        )
    return rows


def build_validation(
    sources: list[dict[str, Any]],
    normal_rows: list[dict[str, Any]],
    variation_rows: list[dict[str, Any]],
    residual_rows: list[dict[str, Any]],
    counter_rows: list[dict[str, Any]],
    decision_rows: list[dict[str, Any]],
    claim_rows: list[dict[str, Any]],
    refusal_rows: list[dict[str, Any]],
    next_rows: list[dict[str, Any]],
    copy_rows: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []

    def add(row_id: str, passed: bool, detail: str) -> None:
        rows.append({"timestamp_utc": timestamp(), "branch_id": BRANCH_ID, "row_id": row_id, "status": "PASS" if passed else "FAIL", "detail": detail, "valid_for_claim": "false"})

    add("VAL2345_00_required_sources_exist", all(row["exists"] == "true" for row in sources), "every required source path exists")
    add("VAL2345_01_required_needles_found", all(row["needles_found"] == "true" for row in sources), "all required source needles were found")
    add("VAL2345_02_partial_theorem_recorded", any(row["row_id"] == "CNF2345_1_hilbert_owner" and row["status"] == "EXACT_CONDITIONAL_SUBTHEOREM" for row in normal_rows), "Hilbert-owner partial theorem recorded")
    add("VAL2345_03_not_promoted", any(row["row_id"] == "CNF2345_6_verdict" and row["status"] == "PARTIAL_THEOREM_NOT_CLOSED" for row in normal_rows), "current-owner theorem not promoted")
    add("VAL2345_04_variation_split_has_open_channels", any(row["status"] == "UNSIGNED" for row in variation_rows), "variation split retains unsigned channels")
    add("VAL2345_05_residual_schema_nonclaim", all(row["score_ready"] == "false" and row["valid_for_claim"] == "false" for row in residual_rows), "current-owner residual first row remains non-score-ready")
    add("VAL2345_06_countermodels_statused", any(row["status"] == "CONDITIONALLY_KILLED" for row in counter_rows) and any("SURVIVES" in row["status"] for row in counter_rows), "countermodel matrix separates partial win from live obstructions")
    partial_gate = [row for row in claim_rows if row["row_id"] == "CG2345_1_hilbert_owner"]
    other_gates = [row for row in claim_rows if row["row_id"] != "CG2345_1_hilbert_owner"]
    add("VAL2345_07_claim_gates_blocked_except_partial", bool(partial_gate and partial_gate[0]["passed"] == "true") and all(row["passed"] == "false" for row in other_gates) and all(row["valid_for_claim"] == "false" for row in claim_rows), "only the explicitly partial Hilbert-owner gate passes; no claim gate is valid_for_claim")
    add("VAL2345_08_refusals_block_shortcuts", all(row["allowed"] == "false" for row in refusal_rows), "shortcut claims refused")
    add("VAL2345_09_next_selected", any(row["row_id"] == "NEXT2345_0" and "nonHilbert-source-projection" in row["next_target"] for row in next_rows), "2346 non-Hilbert source projection target recorded")
    add("VAL2345_10_branch_copies_parse", all(row["copy_exists"] == "true" and int(row["row_count"]) > 0 for row in copy_rows), "branch copies exist and parse")
    generated_groups = [sources, normal_rows, variation_rows, residual_rows, counter_rows, decision_rows, claim_rows, refusal_rows, next_rows, copy_rows]
    add("VAL2345_11_no_claim_flags", all(row.get("valid_for_claim") == "false" for group in generated_groups for row in group), "no generated row is valid_for_claim=true")
    checkpoint_needles = [
        "CURRENT_OWNER_NORMAL_FORM_AUDIT_2345",
        "SOURCEGM_CURRENT_OWNER_RESIDUAL_FIRST_ROW_2345",
        "JR2345_CURRENT_OWNER",
        "Y5_R2FR_current_owner_normal_form",
    ]
    formalization_hits: list[str] = []
    if FORMALIZATION.exists():
        for needle in checkpoint_needles:
            try:
                result = subprocess.run(["rg", "-n", "--fixed-strings", needle, str(FORMALIZATION)], capture_output=True, text=True, timeout=30, check=False)
            except (OSError, subprocess.TimeoutExpired):
                result = subprocess.CompletedProcess(args=[], returncode=1, stdout="", stderr="")
            if result.returncode == 0 and result.stdout.strip():
                formalization_hits.extend(result.stdout.strip().splitlines())
    add("VAL2345_12_formalization_untouched_by_2345", not formalization_hits, "no 2345 checkpoint output appears in formalization-workbench")
    add("VAL2345_13_no_github_policy", any(row["row_id"] == "DEC2345_4_public_policy" and row["status"] == "NO_GITHUB_EVIDENCE_UPDATE" for row in decision_rows), "public GitHub update not recommended from 2345")

    add("VAL2345_OVERALL", all(row["status"] == "PASS" for row in rows), "2345 derives the partial Hilbert-owner subtheorem, refuses full current-owner promotion, installs the first current-owner sourceGM residual row, and selects non-Hilbert source projection as 2346.")
    return rows


def write_doc(
    sources: list[dict[str, Any]],
    normal_rows: list[dict[str, Any]],
    variation_rows: list[dict[str, Any]],
    residual_rows: list[dict[str, Any]],
    counter_rows: list[dict[str, Any]],
    decision_rows: list[dict[str, Any]],
    claim_rows: list[dict[str, Any]],
    refusal_rows: list[dict[str, Any]],
    next_rows: list[dict[str, Any]],
    copy_rows: list[dict[str, Any]],
    validation_rows: list[dict[str, Any]],
) -> None:
    sections = [
        "# 2345 - Current Owner Normal Form From Parent Variation Or SourceGM Residual First Row",
        "",
        "## Summary",
        "",
        "2345 gets one clean win without pretending it is the whole fight.",
        "",
        "If a common ordinary matter action is already fixed and varied before readout, the active source contributed by",
        "ordinary matter is the Hilbert/coframe derivative. That conditionally kills post-variation source rescaling:",
        "a downstream readout map cannot rewrite the source that already varied the metric.",
        "",
        "But this does not kill source weights inserted before variation, and it does not silence non-Hilbert, boundary,",
        "shadow-connection, or readout-reentry source currents. So 2345 refuses a local GR/Newton claim and installs",
        "the first strict `epsilon_current_owner_NH_abs` residual row.",
        "",
        "## Source Register",
        "",
        markdown_table(sources, ["row_id", "source_key", "source_path", "exists", "required", "needles_found", "source_role", "valid_for_claim"]),
        "",
        "## Current Owner Normal Form Audit",
        "",
        markdown_table(normal_rows, ["row_id", "normal_form_piece", "formal_statement", "status", "derived_content", "remaining_gap", "valid_for_claim"]),
        "",
        "## Parent Variation Split Audit",
        "",
        markdown_table(variation_rows, ["row_id", "variation_clause", "normal_form", "status", "if_missing", "valid_for_claim"]),
        "",
        "## SourceGM Current Owner Residual First Row",
        "",
        markdown_table(residual_rows, ["row_id", "quantity", "component", "formula", "units", "current_value", "required_source_or_zero", "observable_links", "score_ready", "valid_for_claim"]),
        "",
        "## Countermodel Status",
        "",
        markdown_table(counter_rows, ["row_id", "countermodel", "status", "why", "residual_if_unsigned", "valid_for_claim"]),
        "",
        "## Decision Ledger",
        "",
        markdown_table(decision_rows, ["row_id", "decision", "reason", "consequence", "status", "valid_for_claim"]),
        "",
        "## Claim Gates",
        "",
        markdown_table(claim_rows, ["row_id", "gate", "passed", "claim_effect", "valid_for_claim"]),
        "",
        "## Refusal Runner",
        "",
        markdown_table(refusal_rows, ["row_id", "claim", "allowed", "reason", "blocking_rows", "valid_for_claim"]),
        "",
        "## Next Target",
        "",
        markdown_table(next_rows, ["row_id", "next_target", "why", "route_type", "valid_for_claim"]),
        "",
        "## Branch Copies",
        "",
        markdown_table(copy_rows, ["row_id", "source_csv", "branch_copy_path", "copy_exists", "row_count", "valid_for_claim"]),
        "",
        "## Validation",
        "",
        markdown_table(validation_rows, ["row_id", "status", "detail", "valid_for_claim"]),
        "",
    ]
    DOC.write_text("\n".join(sections), encoding="utf-8")


def main() -> None:
    sources = build_sources()
    normal_rows = build_normal_form_rows()
    variation_rows = build_variation_rows()
    residual_rows = build_residual_rows()
    counter_rows = build_countermodel_rows()
    decision_rows = build_decision_rows()
    claim_rows = build_claim_rows()
    refusal_rows = build_refusal_rows()
    next_rows = build_next_rows()

    write_csv(OUTPUTS["sources"], sources)
    write_csv(OUTPUTS["normal_form"], normal_rows)
    write_csv(OUTPUTS["variation"], variation_rows)
    write_csv(OUTPUTS["residual"], residual_rows)
    write_csv(OUTPUTS["countermodels"], counter_rows)
    write_csv(OUTPUTS["decision"], decision_rows)
    write_csv(OUTPUTS["claims"], claim_rows)
    write_csv(OUTPUTS["refusal"], refusal_rows)
    write_csv(OUTPUTS["next"], next_rows)

    copy_rows = copy_branch_outputs()
    write_csv(OUTPUTS["copies"], copy_rows)

    validation_rows = build_validation(
        sources,
        normal_rows,
        variation_rows,
        residual_rows,
        counter_rows,
        decision_rows,
        claim_rows,
        refusal_rows,
        next_rows,
        copy_rows,
    )
    write_csv(OUTPUTS["validation"], validation_rows)
    write_doc(
        sources,
        normal_rows,
        variation_rows,
        residual_rows,
        counter_rows,
        decision_rows,
        claim_rows,
        refusal_rows,
        next_rows,
        copy_rows,
        validation_rows,
    )
    print(f"2345 checkpoint generated: {DOC}")
    print(f"Validation: {OUTPUTS['validation']}")


if __name__ == "__main__":
    main()

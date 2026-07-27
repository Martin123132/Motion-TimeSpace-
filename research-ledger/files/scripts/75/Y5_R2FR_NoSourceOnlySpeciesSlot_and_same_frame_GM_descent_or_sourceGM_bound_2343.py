from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


BRANCH_ID = "MTS_R2FR_NOSOURCEONLYSPECIES_AND_SAME_FRAME_GM_DESCENT_OR_SOURCEGM_BOUND_2343"

ROOT = Path(__file__).resolve().parents[1]
PROJECT = ROOT.parent
FORMALIZATION = PROJECT / "formalization-workbench"
OUT = ROOT / "source-intake" / "mts_residuals"
RAB_QUEUE = ROOT / "source-intake" / "rab-sector" / "acquisition-queue"
MICRO_RESIDUALS = ROOT / "source-intake" / "microscope" / "branch_locked_wep" / "residuals"
BETA_DOCS = ROOT / "source-intake" / "beta-source" / "docs"

DOC = ROOT / "2343-Y5-R2FR-NoSourceOnlySpeciesSlot-and-same-frame-GM-descent-or-sourceGM-bound.md"

PATHS = {
    "2342_doc": ROOT / "2342-Y5-R2FR-source-charge-equals-measured-GM-or-selector-bound.md",
    "2342_validation": OUT / "P8_Y5_BRR545_2342_VALIDATION.csv",
    "2342_next": OUT / "P8_Y5_PARENT_QLOC_2342_NEXT_TARGET.csv",
    "2342_bridge": OUT / "P8_Y5_PARENT_QLOC_2342_SOURCE_GM_BRIDGE_AUDIT.csv",
    "2342_contract": OUT / "P8_Y5_PARENT_QLOC_2342_SELECTOR_SOURCE_MEASURE_CONTRACT.csv",
    "2328_nospecies": OUT / "P8_Y5_PARENT_QLOC_2328_NO_SOURCE_ONLY_SPECIES_SLOT_DERIVATION_ATTEMPT.csv",
    "2124_gm_guard": OUT / "P8_Y5_PARENT_QLOC_2124_GM_GUARD_DESCENT_AUDIT.csv",
    "2125_refusal": OUT / "P8_Y5_PARENT_QLOC_2125_GM_ABSORPTION_REFUSAL.csv",
    "1902_label_forget": OUT / "P8_Y5_PARENT_QLOC_1902_SOURCE_LABEL_FORGETTING_BEFORE_GM_ATTEMPT.csv",
    "no_species_contract": OUT / "P8_no_species_source_charge_CONTRACT.csv",
    "1425_common_guard": OUT / "P8_Y5_R10_1425_MEASURED_G_COMMON_MODE_GUARD.csv",
    "1425_premises": OUT / "P8_Y5_R10_1425_COMMON_MODE_PREMISE_AUDIT.csv",
    "1461_countermodels": OUT / "P8_Y5_R10_1461_SOURCE_LABEL_COUNTERMODEL_AUDIT.csv",
    "1476_premises": OUT / "P8_Y5_R10_1476_SOURCE_LABEL_PREMISE_AUDIT.csv",
    "683_same_frame": OUT / "P8_Y5_R10_683_SAME_FRAME_GM_GATE.csv",
}

SOURCES = [
    ("SRC2343_00_2342_doc", "2342_doc", PATHS["2342_doc"], ["DEC2342_2_next", "NoSourceOnlySpeciesSlot"], "2342 handoff to coupling/source-GM descent"),
    ("SRC2343_01_2342_validation", "2342_validation", PATHS["2342_validation"], ["VAL2342_OVERALL", "PASS"], "2342 validation"),
    ("SRC2343_02_2342_next", "2342_next", PATHS["2342_next"], ["NEXT2342_0", "NoSourceOnlySpeciesSlot"], "machine-readable 2343 target"),
    ("SRC2343_03_2342_bridge", "2342_bridge", PATHS["2342_bridge"], ["SGM2342_5_constant_G", "MISSING_UNIVERSAL_COUPLING_DESCENT"], "source-GM bridge constant-G blocker"),
    ("SRC2343_04_2342_contract", "2342_contract", PATHS["2342_contract"], ["SSC2342_4_universal_G", "MISSING_NO_SOURCE_ONLY_SPECIES_SLOT"], "universal coupling contract"),
    ("SRC2343_05_2328_nospecies", "2328_nospecies", PATHS["2328_nospecies"], ["NSOS2328_6_verdict", "NOT_DERIVED_PARENT_CONTRACT_READY"], "NoSourceOnlySpeciesSlot derivation attempt"),
    ("SRC2343_06_2124_gm_guard", "2124_gm_guard", PATHS["2124_gm_guard"], ["GM2124_0_common_mode_rule", "GUARD_NORMAL_FORM_CLOSED_DATA_OPEN"], "measured-G common-mode guard"),
    ("SRC2343_07_2125_refusal", "2125_refusal", PATHS["2125_refusal"], ["REF2125_1_measured_G_hiding", "REFUSED"], "GM absorption shortcut refusals"),
    ("SRC2343_08_1902_label_forget", "1902_label_forget", PATHS["1902_label_forget"], ["SLG1902_6_verdict", "SOURCE_LABEL_FORGETTING_BEFORE_GM_NOT_PARENT_DERIVED"], "source-label forgetting before GM attempt"),
    ("SRC2343_09_no_species_contract", "no_species_contract", PATHS["no_species_contract"], ["S4_source_normalization_species_blind", "not_parent_derived"], "no species source charge contract"),
    ("SRC2343_10_1425_common_guard", "1425_common_guard", PATHS["1425_common_guard"], ["GCG1425_0_common_scale", "GCG1425_1_relative_residual"], "common-mode measured-G guard"),
    ("SRC2343_11_1425_premises", "1425_premises", PATHS["1425_premises"], ["PREM1425_3_no_relative_source_prefactors", "EXACT_HIGH_PRESSURE_MISSING_CLAUSE"], "common-mode zero premises"),
    ("SRC2343_12_1461_countermodels", "1461_countermodels", PATHS["1461_countermodels"], ["CM1461_0_relative_wA", "RETAIN_LIVE_NONCLAIM"], "relative source-label countermodels"),
    ("SRC2343_13_1476_premises", "1476_premises", PATHS["1476_premises"], ["SLP1476_2_action_measure_owner", "SLP1476_5_readout_no_reentry"], "source-label premise audit"),
    ("SRC2343_14_683_same_frame", "683_same_frame", PATHS["683_same_frame"], ["SFG683_6_final", "fail_blocked"], "same-frame GM gate"),
]

OUTPUTS = {
    "sources": OUT / "P8_Y5_PARENT_QLOC_2343_SOURCE_REGISTER.csv",
    "nospecies_audit": OUT / "P8_Y5_PARENT_QLOC_2343_NOSOURCEONLYSPECIES_AUDIT.csv",
    "same_frame": OUT / "P8_Y5_PARENT_QLOC_2343_SAME_FRAME_GM_DESCENT_AUDIT.csv",
    "countermodels": OUT / "P8_Y5_PARENT_QLOC_2343_SOURCEGM_COUNTERMODEL_LEDGER.csv",
    "bound_rows": OUT / "P8_Y5_PARENT_QLOC_2343_SOURCEGM_BOUND_ROWS.csv",
    "decision": OUT / "P8_Y5_PARENT_QLOC_2343_DECISION_LEDGER.csv",
    "claims": OUT / "P8_Y5_PARENT_QLOC_2343_CLAIM_GATES.csv",
    "refusal": OUT / "P8_Y5_PARENT_QLOC_2343_REFUSAL_RUNNER.csv",
    "next": OUT / "P8_Y5_PARENT_QLOC_2343_NEXT_TARGET.csv",
    "copies": OUT / "P8_Y5_PARENT_QLOC_2343_BRANCH_COPIES.csv",
    "validation": OUT / "P8_Y5_BRR545_2343_VALIDATION.csv",
}

BRANCH_COPY_SPECS = [
    ("COPY2343_0_nospecies", OUTPUTS["nospecies_audit"], BETA_DOCS / "NOSOURCEONLYSPECIES_AUDIT_2343_NONCLAIM.csv"),
    ("COPY2343_1_bounds", OUTPUTS["bound_rows"], MICRO_RESIDUALS / "SOURCEGM_BOUND_ROWS_2343_NONCLAIM.csv"),
    ("COPY2343_2_decision", OUTPUTS["decision"], RAB_QUEUE / "JR2343_SOURCEGM_DECISION_LEDGER_NONCLAIM.csv"),
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


def relative_path(path: Path) -> str:
    try:
        return str(path.relative_to(ROOT))
    except ValueError:
        return str(path)


def markdown_table(rows: list[dict[str, Any]], columns: list[str]) -> str:
    header = "| " + " | ".join(columns) + " |"
    separator = "| " + " | ".join("---" for _ in columns) + " |"
    body = []
    for row in rows:
        values = []
        for column in columns:
            value = str(row.get(column, ""))
            value = value.replace("|", "\\|").replace("\n", " ")
            values.append(value)
        body.append("| " + " | ".join(values) + " |")
    return "\n".join([header, separator, *body])


def build_sources() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for row_id, source_key, path, needles, role in SOURCES:
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


def build_nospecies_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "row_id": "NSS2343_0_target",
            "claim_piece": "NoSourceOnlySpeciesSlot",
            "formal_statement": "Hom_parent(SpeciesLabel, Coeff_active_source)=empty; no w_A S_A source-only prefactor can multiply gravitational source strength independently of matter normalization.",
            "status": "TARGET_SHARPENED",
            "proof_or_obstruction": "this is the exact clause needed before measured GM can be used as derived source readout",
            "fallback": "finite relative source-GM vector",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "NSS2343_1_covariance",
            "claim_piece": "covariance forbids relative source weights",
            "formal_statement": "Diffeomorphism covariance alone excludes constant scalar w_A prefactors.",
            "status": "FAIL_COUNTERMODEL_SURVIVES",
            "proof_or_obstruction": "S_matter=sum_A w_A S_A is covariant and additive unless parent grammar excludes it",
            "fallback": "retain relative_wA countermodel",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "NSS2343_2_Hilbert",
            "claim_piece": "Hilbert current ownership",
            "formal_statement": "Once S_matter is fixed, source is Hilbert variation with respect to e_obs/g_obs before readout.",
            "status": "EXACT_SUBTHEOREM_BUT_NOT_ENOUGH",
            "proof_or_obstruction": "pre-variation w_A inside the action is inherited by Hilbert stress",
            "fallback": "require no-source-only parent slot, not just Hilbert variation",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "NSS2343_3_source_blind_functor",
            "claim_piece": "source-blind matter functor theorem",
            "formal_statement": "If ordinary matter is one source-blind descended functor with one observed measure and no independent species-to-source coefficient object, relative w_A is inadmissible.",
            "status": "EXACT_CONDITIONAL_THEOREM",
            "proof_or_obstruction": "current corpus has not parent-signed the functor/admissibility clauses",
            "fallback": "finite source-profile row remains live",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "NSS2343_4_common_scale",
            "claim_piece": "single common source scale",
            "formal_statement": "A single common factor multiplying total T_matter may be absorbed once into kappa/G_N/GM calibration.",
            "status": "EXACT_IF_SINGLE_SCALE",
            "proof_or_obstruction": "relative source/species coefficients are not common scale",
            "fallback": "common-mode removed relative residual vector",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "NSS2343_5_verdict",
            "claim_piece": "promote NoSourceOnlySpeciesSlot now",
            "formal_statement": "Current MTS derives no source-only species/source slot strongly enough to set epsilon_source_GM_rel=0.",
            "status": "NOT_DERIVED_RETAIN_SOURCEGM_BOUND",
            "proof_or_obstruction": "the clean theorem is isolated but needs parent-signed action/functor grammar, common measure/current owner and readout no-reentry",
            "fallback": "stage epsilon_source_GM_rel_abs",
            "valid_for_claim": "false",
        },
    ]


def build_same_frame_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "row_id": "SFGD2343_0_tau",
            "descent_clause": "same observed time generator",
            "formal_statement": "tau_source=tau_charge=tau_clock=tau_orbit and delta tau=0 in charge variation.",
            "status": "MISSING_SAME_OBSERVED_TIME_GENERATOR",
            "residual_if_missing": "Delta_tau_source_GM",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "SFGD2343_1_coframe",
            "descent_clause": "same observed coframe/source frame",
            "formal_statement": "S_matter uses one e_obs for source current, rods, clocks, metric perturbation and orbital readout.",
            "status": "MISSING_SAME_FRAME_MEASURE_PROOF",
            "residual_if_missing": "Delta_frame_source",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "SFGD2343_2_common_measure",
            "descent_clause": "common action measure/current owner",
            "formal_statement": "one action measure, one hbar/Jacobian and one Hilbert/coframe current owner for ordinary matter sectors.",
            "status": "COMMON_MEASURE_CURRENT_OWNER_UNSIGNED",
            "residual_if_missing": "Delta_species_measure_jacobian",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "SFGD2343_3_no_reentry",
            "descent_clause": "readout no-reentry",
            "formal_statement": "source-worldtube/readout kernels cannot recreate species labels after variation.",
            "status": "READOUT_NO_REENTRY_UNSIGNED",
            "residual_if_missing": "Delta_readout_selector_reentry",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "SFGD2343_4_final",
            "descent_clause": "same-frame GM descent",
            "formal_statement": "all same-frame/source-label descent clauses pass before GM calibration is used as source evidence.",
            "status": "DESCENT_NOT_DERIVED",
            "residual_if_missing": "epsilon_same_frame_source_GM_abs",
            "valid_for_claim": "false",
        },
    ]


def build_countermodel_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "row_id": "CM2343_0_relative_wA",
            "countermodel": "S_matter=sum_A w_A S_A",
            "why_survives": "covariant/additive and not excluded by current parent grammar",
            "effect": "source charge becomes composition/source-profile dependent",
            "retention": "RETAIN_LIVE_NONCLAIM",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "CM2343_1_species_measure_jacobian",
            "countermodel": "species-dependent measure/current normalization J_A",
            "why_survives": "common measure/current owner not parent-derived",
            "effect": "bypasses Hilbert total-source uniqueness",
            "retention": "RETAIN_LIVE_NONCLAIM",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "CM2343_2_hidden_marker_source_weight",
            "countermodel": "w_A(Xhat, marker, material) source coefficient",
            "why_survives": "no-hidden-visible-hom and no-marker extension are unsigned",
            "effect": "source charge varies with hidden/material profile",
            "retention": "RETAIN_LIVE_NONCLAIM",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "CM2343_3_nonHilbert_current",
            "countermodel": "J_src=kappa T_Hilbert + J_NH",
            "why_survives": "non-Hilbert current silence is not proven",
            "effect": "source residual can survive without appearing as species stress label",
            "retention": "RETAIN_LIVE_NONCLAIM",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "CM2343_4_readout_selector_reentry",
            "countermodel": "source-worldtube/readout kernel selects material/source profile after variation",
            "why_survives": "readout no-reentry not source-signed",
            "effect": "pipeline can manufacture or hide an apparent source residual",
            "retention": "RETAIN_LIVE_NONCLAIM",
            "valid_for_claim": "false",
        },
    ]


def build_bound_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "row_id": "SGB2343_0_relative_source",
            "quantity": "epsilon_source_GM_rel_abs",
            "formula": "norm((I-P_common) source_GM_weight_vector)",
            "required_columns": "system_id;source_weight_basis;common_mode_projector;relative_weights;norm;source_path;equation_ref;valid_for_claim",
            "current_value": "MISSING_SOURCE_WEIGHT_BASIS;MISSING_RELATIVE_WEIGHTS",
            "score_ready": "false",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "SGB2343_1_same_frame",
            "quantity": "epsilon_same_frame_source_GM_abs",
            "formula": "abs(Delta_tau_source_GM)+abs(Delta_frame_source)+abs(Delta_species_measure_jacobian)+abs(Delta_readout_selector_reentry)",
            "required_columns": "system_id;tau_id;coframe_id;current_owner;readout_kernel;component_values;source_path;equation_ref;valid_for_claim",
            "current_value": "MISSING_SAME_FRAME_COMPONENTS",
            "score_ready": "false",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "SGB2343_2_countermodel",
            "quantity": "epsilon_countermodel_source_GM_abs",
            "formula": "max allowed impact from retained countermodels CM2343_0..4 after common GM calibration",
            "required_columns": "countermodel_id;coefficient_value;observable_projection;bound_source;units;valid_for_claim",
            "current_value": "MISSING_COUNTERMODEL_COEFFICIENTS",
            "score_ready": "false",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "SGB2343_3_total",
            "quantity": "epsilon_sourceGM_descent_abs",
            "formula": "epsilon_source_GM_rel_abs + epsilon_same_frame_source_GM_abs + epsilon_countermodel_source_GM_abs",
            "required_columns": "system_id;component_values;component_sources;no_cancellation_guard;valid_for_claim",
            "current_value": "MISSING_COMPONENT_INPUTS",
            "score_ready": "false",
            "valid_for_claim": "false",
        },
    ]


def build_decision_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "row_id": "DEC2343_0_theorem_result",
            "decision": "do not claim NoSourceOnlySpeciesSlot or same-frame GM descent",
            "reason": "relative w_A, species Jacobian, hidden marker, non-Hilbert current and readout re-entry countermodels remain live",
            "consequence": "source-GM equality and local Newton recovery remain blocked",
            "status": "THEOREM_NOT_DERIVED_RETAIN_BOUNDS",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "DEC2343_1_clean_route",
            "decision": "keep the clean conditional theorem as the target",
            "reason": "if parent grammar signs source-blind matter functor, common measure/current owner and no re-entry, the relative source residual collapses",
            "consequence": "future derivation can still close this without data fitting",
            "status": "CONDITIONAL_THEOREM_ROUTE_RETAINED",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "DEC2343_2_bound_route",
            "decision": "stage sourceGM descent bound rows",
            "reason": "if the theorem does not close, the relative source-GM vector must be source-backed and bounded",
            "consequence": "no hidden calibration pass; one common mode only",
            "status": "SOURCEGM_BOUND_ROWS_STAGED_NONCLAIM",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "DEC2343_3_next",
            "decision": "attack parent source-blind matter functor/current-owner proof next",
            "reason": "this is the least empirical and least circular route to kill relative source weights",
            "consequence": "next target should derive the parent grammar/current-owner condition or demote to bound acquisition",
            "status": "SELECT_PARENT_SOURCE_BLIND_FUNCTOR_NEXT",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "DEC2343_4_public_policy",
            "decision": "no GitHub update from 2343",
            "reason": "this is private coupling theorem triage, not public claim material",
            "consequence": "continue private derivation sequence",
            "status": "NO_GITHUB_EVIDENCE_UPDATE",
            "valid_for_claim": "false",
        },
    ]


def build_claim_rows() -> list[dict[str, Any]]:
    gates = [
        ("CG2343_0_NoSourceOnlySpeciesSlot", "NoSourceOnlySpeciesSlot parent-signed", "false", "parent action/functor grammar still unsigned"),
        ("CG2343_1_common_measure", "common action measure/current owner signed", "false", "species Jacobian/current owner countermodel survives"),
        ("CG2343_2_same_frame", "same-frame GM descent signed", "false", "tau/coframe/readout no-reentry remain blocked"),
        ("CG2343_3_relative_zero", "relative source-GM residual theorem-zero", "false", "relative weights cannot be calibrated away"),
        ("CG2343_4_bound_score", "sourceGM bound rows score-ready", "false", "component values and source paths missing"),
        ("CG2343_5_local_GR_Newton", "local GR/Newton recovery derived", "false", "source-GM descent remains open"),
        ("CG2343_6_github", "safe public GitHub update", "false", "private checkpoint only"),
    ]
    return [
        {
            "branch_id": BRANCH_ID,
            "row_id": row_id,
            "gate": gate,
            "passed": passed,
            "claim_effect": effect,
            "valid_for_claim": "false",
        }
        for row_id, gate, passed, effect in gates
    ]


def build_refusal_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "row_id": "REF2343_0_covariance_zero",
            "claim": "covariance alone forbids relative source weights",
            "allowed": "false",
            "reason": "constant scalar w_A countermodel is covariant and additive",
            "blocking_rows": "NSS2343_1_covariance;CM2343_0_relative_wA",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "REF2343_1_Hilbert_zero",
            "claim": "Hilbert variation alone forbids pre-action w_A",
            "allowed": "false",
            "reason": "Hilbert variation inherits prefactors already inside S_matter",
            "blocking_rows": "NSS2343_2_Hilbert;CM2343_0_relative_wA",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "REF2343_2_GM_absorb_relative",
            "claim": "fit measured GM to absorb relative source/species weights",
            "allowed": "false",
            "reason": "GM calibration absorbs only one common-mode factor",
            "blocking_rows": "NSS2343_4_common_scale;SGB2343_0_relative_source",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "REF2343_3_readout_hide",
            "claim": "let source-worldtube/readout kernel hide species labels",
            "allowed": "false",
            "reason": "readout no-reentry must be parent-signed or residualized",
            "blocking_rows": "SFGD2343_3_no_reentry;CM2343_4_readout_selector_reentry",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "REF2343_4_local_claim",
            "claim": "2343 proves local GR/Newton recovery",
            "allowed": "false",
            "reason": "2343 stages a nonclaim coupling theorem audit and sourceGM bound rows",
            "blocking_rows": "DEC2343_0_theorem_result;CG2343_5_local_GR_Newton",
            "valid_for_claim": "false",
        },
    ]


def build_next_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "row_id": "NEXT2343_0",
            "next_target": "2344-Y5-R2FR-parent-source-blind-matter-functor-current-owner-or-sourceGM-bound.md",
            "why": "the clean theorem route needs parent grammar/current owner to remove species/source-only coefficients before GM calibration.",
            "claim_status": "private_derivation_next_step",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "NEXT2343_1",
            "next_target": "2344b-Y5-R2FR-sourceGM-relative-vector-acquisition.md",
            "why": "fallback route: if parent proof stalls, fill relative source/profile/species vector rows with units and source paths.",
            "claim_status": "fallback_nonclaim",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "NEXT2343_2",
            "next_target": "2344c-Y5-R2FR-Poisson-Gauss-orbital-bridge-or-DeltaPG-row.md",
            "why": "parallel route: even after coupling descent, the same charge must still generate the observed orbital field.",
            "claim_status": "parallel_nonclaim",
            "valid_for_claim": "false",
        },
    ]


def copy_branch_outputs() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for row_id, source, destination in BRANCH_COPY_SPECS:
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(source, destination)
        copied_rows = read_csv_rows(destination)
        rows.append(
            {
                "branch_id": BRANCH_ID,
                "row_id": row_id,
                "source_csv": relative_path(source),
                "branch_copy_path": str(destination),
                "copy_exists": bool_text(destination.exists()),
                "row_count": str(len(copied_rows)),
                "valid_for_claim": "false",
            }
        )
    return rows


def build_validation(
    sources: list[dict[str, Any]],
    nospecies: list[dict[str, Any]],
    same_frame: list[dict[str, Any]],
    countermodels: list[dict[str, Any]],
    bound_rows: list[dict[str, Any]],
    decision: list[dict[str, Any]],
    claims: list[dict[str, Any]],
    refusal: list[dict[str, Any]],
    next_rows: list[dict[str, Any]],
    copies: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    validations: list[tuple[str, bool, str]] = []
    validations.append(("VAL2343_00_required_sources_exist", all(row["exists"] == "true" for row in sources), "every required source path exists"))
    validations.append(("VAL2343_01_required_needles_found", all(row["needles_found"] == "true" for row in sources), "all required source needles were found"))
    validations.append(("VAL2343_02_theorem_not_promoted", any(row["status"] == "NOT_DERIVED_RETAIN_SOURCEGM_BOUND" for row in nospecies), "NoSourceOnlySpeciesSlot theorem not promoted"))
    validations.append(("VAL2343_03_same_frame_not_promoted", any(row["status"] == "DESCENT_NOT_DERIVED" for row in same_frame), "same-frame GM descent not promoted"))
    validations.append(("VAL2343_04_countermodels_retained", len(countermodels) >= 5 and all(row["retention"] == "RETAIN_LIVE_NONCLAIM" for row in countermodels), "live countermodels retained"))
    validations.append(("VAL2343_05_bound_rows_nonready", len(bound_rows) >= 4 and all(row["score_ready"] == "false" for row in bound_rows), "sourceGM bound rows remain non-score-ready"))
    validations.append(("VAL2343_06_claim_gates_blocked", all(row["passed"] == "false" for row in claims), "all claim gates remain blocked"))
    validations.append(("VAL2343_07_refusals_block_shortcuts", all(row["allowed"] == "false" for row in refusal), "shortcut claims refused"))
    validations.append(("VAL2343_08_next_selected", any("parent-source-blind-matter-functor" in row["next_target"] for row in next_rows), "2344 parent source-blind matter functor next target recorded"))
    validations.append(("VAL2343_09_github_blocked", any(row["status"] == "NO_GITHUB_EVIDENCE_UPDATE" for row in decision), "public GitHub update not recommended from 2343"))
    validations.append(("VAL2343_10_branch_copies_parse", all(row["copy_exists"] == "true" and int(row["row_count"]) > 0 for row in copies), "branch copies exist and parse"))

    generated_paths = [path for key, path in OUTPUTS.items() if key != "validation"]
    generated_paths.extend(destination for _, _, destination in BRANCH_COPY_SPECS)
    validations.append(("VAL2343_11_outputs_exist", all(path.exists() for path in generated_paths), "CSV outputs and branch copies exist before doc render"))

    no_claim_flags = True
    for path in [*OUTPUTS.values(), *(destination for _, _, destination in BRANCH_COPY_SPECS)]:
        if path.exists() and path.suffix == ".csv":
            rows = read_csv_rows(path)
            if any(row.get("valid_for_claim", "").lower() == "true" for row in rows):
                no_claim_flags = False
                break
    validations.append(("VAL2343_12_no_claim_flags", no_claim_flags, "no generated row is valid_for_claim=true"))

    checkpoint_needles = (
        "NOSOURCEONLYSPECIES_AUDIT_2343",
        "SOURCEGM_BOUND_ROWS_2343",
        "JR2343_SOURCEGM",
        "Y5_R2FR_NoSourceOnlySpeciesSlot",
    )
    if FORMALIZATION.exists():
        formalization_clean = not any(
            any(needle in str(path) for needle in checkpoint_needles)
            for path in FORMALIZATION.rglob("*")
        )
    else:
        formalization_clean = True
    validations.append(("VAL2343_13_formalization_untouched_by_2343", formalization_clean, "no 2343 checkpoint output appears in formalization-workbench"))

    rows = [
        {
            "branch_id": BRANCH_ID,
            "row_id": row_id,
            "status": "PASS" if passed else "FAIL",
            "detail": detail,
            "valid_for_claim": "false",
        }
        for row_id, passed, detail in validations
    ]
    overall = all(row["status"] == "PASS" for row in rows)
    rows.append(
        {
            "branch_id": BRANCH_ID,
            "row_id": "VAL2343_OVERALL",
            "status": "PASS" if overall else "FAIL",
            "detail": "2343 tests NoSourceOnlySpeciesSlot and same-frame GM descent, rejects shortcut promotion, retains countermodels, stages sourceGM bounds, and selects parent source-blind matter functor/current-owner next.",
            "valid_for_claim": "false",
        }
    )
    return rows


def write_doc(
    sources: list[dict[str, Any]],
    nospecies: list[dict[str, Any]],
    same_frame: list[dict[str, Any]],
    countermodels: list[dict[str, Any]],
    bound_rows: list[dict[str, Any]],
    decision: list[dict[str, Any]],
    claims: list[dict[str, Any]],
    refusal: list[dict[str, Any]],
    next_rows: list[dict[str, Any]],
    copies: list[dict[str, Any]],
    validation: list[dict[str, Any]],
) -> None:
    text = f"""# 2343 - NoSourceOnlySpeciesSlot and same-frame GM descent or sourceGM bound

## Summary

2343 attacks the coupling nerve selected by 2342.

The desired theorem is:

`Hom_parent(SpeciesLabel, Coeff_active_source)=empty`,

plus same-frame descent for the source current, clocks, rods, orbital readout and measured `GM`.

It does not close yet. Covariance and Hilbert variation are useful but insufficient: a pre-action
`S_matter=sum_A w_A S_A` countermodel remains covariant unless the parent grammar forbids source-only species
coefficients. A fitted `GM` can absorb one common source scale, but it cannot hide relative source/species/profile
weights.

So 2343 keeps the clean conditional theorem as the target and stages explicit sourceGM residual bounds.

## Source Register

{markdown_table(sources, ["row_id", "source_key", "source_path", "exists", "required", "needles_found", "source_role", "valid_for_claim"])}

## NoSourceOnlySpeciesSlot Audit

{markdown_table(nospecies, ["row_id", "claim_piece", "formal_statement", "status", "proof_or_obstruction", "fallback", "valid_for_claim"])}

## Same-Frame GM Descent Audit

{markdown_table(same_frame, ["row_id", "descent_clause", "formal_statement", "status", "residual_if_missing", "valid_for_claim"])}

## SourceGM Countermodel Ledger

{markdown_table(countermodels, ["row_id", "countermodel", "why_survives", "effect", "retention", "valid_for_claim"])}

## SourceGM Bound Rows

{markdown_table(bound_rows, ["row_id", "quantity", "formula", "current_value", "score_ready", "valid_for_claim"])}

## Decision Ledger

{markdown_table(decision, ["row_id", "decision", "reason", "consequence", "status", "valid_for_claim"])}

## Claim Gates

{markdown_table(claims, ["row_id", "gate", "passed", "claim_effect", "valid_for_claim"])}

## Refusal Runner

{markdown_table(refusal, ["row_id", "claim", "allowed", "reason", "blocking_rows", "valid_for_claim"])}

## Next Target

{markdown_table(next_rows, ["row_id", "next_target", "why", "claim_status", "valid_for_claim"])}

## Branch Copies

{markdown_table(copies, ["row_id", "source_csv", "branch_copy_path", "copy_exists", "row_count", "valid_for_claim"])}

## Validation

{markdown_table(validation, ["row_id", "status", "detail", "valid_for_claim"])}
"""
    DOC.write_text(text, encoding="utf-8")


def main() -> int:
    sources = build_sources()
    nospecies = build_nospecies_rows()
    same_frame = build_same_frame_rows()
    countermodels = build_countermodel_rows()
    bound_rows = build_bound_rows()
    decision = build_decision_rows()
    claims = build_claim_rows()
    refusal = build_refusal_rows()
    next_rows = build_next_rows()

    write_csv(OUTPUTS["sources"], sources)
    write_csv(OUTPUTS["nospecies_audit"], nospecies)
    write_csv(OUTPUTS["same_frame"], same_frame)
    write_csv(OUTPUTS["countermodels"], countermodels)
    write_csv(OUTPUTS["bound_rows"], bound_rows)
    write_csv(OUTPUTS["decision"], decision)
    write_csv(OUTPUTS["claims"], claims)
    write_csv(OUTPUTS["refusal"], refusal)
    write_csv(OUTPUTS["next"], next_rows)

    copies = copy_branch_outputs()
    write_csv(OUTPUTS["copies"], copies)

    validation = build_validation(sources, nospecies, same_frame, countermodels, bound_rows, decision, claims, refusal, next_rows, copies)
    write_csv(OUTPUTS["validation"], validation)

    write_doc(sources, nospecies, same_frame, countermodels, bound_rows, decision, claims, refusal, next_rows, copies, validation)

    failed = [row for row in validation if row["status"] != "PASS"]
    if failed:
        print(f"2343 validation failed: {len(failed)} failed rows")
        for row in failed:
            print(f"{row['row_id']}: {row['detail']}")
        return 1

    print(f"2343 checkpoint generated: {DOC}")
    print(f"Validation: {OUTPUTS['validation']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

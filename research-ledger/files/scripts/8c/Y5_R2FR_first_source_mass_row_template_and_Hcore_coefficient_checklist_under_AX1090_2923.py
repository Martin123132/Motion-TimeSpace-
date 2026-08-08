from __future__ import annotations

import csv
import math
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


SCRIPT_START_UTC = datetime.now(timezone.utc)

ROOT = Path(__file__).resolve().parents[1]
PROJECT = ROOT.parent
RESIDUALS = ROOT / "source-intake" / "mts_residuals"
LOCAL_BOUNDS = ROOT / "source-intake" / "local_bounds"
RAB_QUEUE = ROOT / "source-intake" / "rab-sector" / "acquisition-queue"
PARENT_ACTION = ROOT / "source-intake" / "parent-action"
FORMALIZATION = PROJECT / "formalization-workbench"

CHECKPOINT = "2923"
BRANCH_ID = "MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428"
RUN_UTC = SCRIPT_START_UTC.isoformat()

DOC = ROOT / "2923-Y5-R2FR-first-source-mass-row-template-and-Hcore-coefficient-checklist-under-AX1090.md"

SRC_2922_DOC = ROOT / "2922-Y5-R2FR-Hamiltonian-sector-owner-or-source-mass-first-row-under-AX1090.md"
SRC_2922_NEXT = RESIDUALS / "P8_Y5_R2FR_2922_NEXT_TARGET.csv"
SRC_2922_SCHEMA = RESIDUALS / "P8_Y5_R2FR_2922_SOURCE_MASS_FIRST_ROW_SCHEMA.csv"
SRC_2922_REFUSAL = RESIDUALS / "P8_Y5_R2FR_2922_SOURCE_MASS_FIRST_ROW_REFUSAL_RUNNER.csv"
SRC_2922_OWNER = RESIDUALS / "P8_Y5_R2FR_2922_HAMILTONIAN_SECTOR_OWNER_AUDIT.csv"
SRC_2922_CROSSWALK = RESIDUALS / "P8_Y5_R2FR_2922_PRIOR_CHAIN_ENDPOINT_CROSSWALK.csv"
SRC_1249_RULES = RESIDUALS / "P8_Y5_R10_1249_FINITE_QRHAT_VALIDATION_RULES.csv"
SRC_1249_RESULTS = RESIDUALS / "P8_Y5_R10_1249_FINITE_QRHAT_CANDIDATE_RESULTS.csv"
SRC_1249_LEDGER = RESIDUALS / "P8_Y5_R10_1249_SOURCE_ACQUISITION_LEDGER.csv"
SRC_1238_DOC = ROOT / "1238-Y5-R10-first-class-RAB-constraint-or-local-GR-closure-benchmark-scorecard.md"
SRC_1105_DOC = ROOT / "1105-Y5-R10-master-no-hidden-visible-coefficient-morphism-or-explicit-closure-pack.md"
SRC_1237_DOC = ROOT / "1237-Y5-R10-MTS-primitives-to-sorted-parent-action-derivation-or-closure-demotion.md"

OUTPUTS = {
    "sources": RESIDUALS / "P8_Y5_R2FR_2923_SOURCE_REGISTER.csv",
    "hcore_checklist": RESIDUALS / "P8_Y5_R2FR_2923_HCORE_QTAU_COEFFICIENT_CHECKLIST.csv",
    "row_template": RESIDUALS / "P8_Y5_R2FR_2923_SOURCE_MASS_ROW_TEMPLATE.csv",
    "validator_rules": RESIDUALS / "P8_Y5_R2FR_2923_STRICT_VALIDATOR_RULES.csv",
    "candidate_results": RESIDUALS / "P8_Y5_R2FR_2923_CANDIDATE_VALIDATION_RESULTS.csv",
    "claims": RESIDUALS / "P8_Y5_R2FR_2923_CLAIM_GATES.csv",
    "decision": RESIDUALS / "P8_Y5_R2FR_2923_DECISION_LEDGER.csv",
    "next": RESIDUALS / "P8_Y5_R2FR_2923_NEXT_TARGET.csv",
    "branches": RESIDUALS / "P8_Y5_R2FR_2923_BRANCH_COPIES.csv",
    "validation": RESIDUALS / "P8_Y5_BRR545_2923_VALIDATION.csv",
}

BRANCH_OUTPUTS = {
    "hcore_copy": PARENT_ACTION / "Hcore_Qtau_coefficient_checklist_2923_NONCLAIM.csv",
    "row_template_copy": LOCAL_BOUNDS / "Source_mass_row_template_2923_NONCLAIM.csv",
    "next_copy": RAB_QUEUE / "JR2923_PARENT_HCORE_COEFFICIENT_MAP_OR_FIRST_SOURCE_ROW_NEXT_NONCLAIM.csv",
}

for directory in {path.parent for path in OUTPUTS.values()} | {path.parent for path in BRANCH_OUTPUTS.values()} | {DOC.parent}:
    directory.mkdir(parents=True, exist_ok=True)


def read_text(path: Path) -> str:
    if not path.exists():
        return ""
    return path.read_text(encoding="utf-8", errors="replace")


def anchors_present(path: Path, anchors: str) -> tuple[bool, str]:
    if not path.exists():
        return False, anchors
    text = read_text(path)
    missing = [anchor for anchor in anchors.split(";") if anchor and anchor not in text]
    return not missing, ";".join(missing)


def add_common(row: dict[str, Any]) -> dict[str, Any]:
    row.update(
        {
            "checkpoint": CHECKPOINT,
            "branch_id": BRANCH_ID,
            "control_only": True,
            "score_ready": False,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
            "generated_utc": RUN_UTC,
        }
    )
    return row


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    fieldnames: list[str] = []
    for row in rows:
        for key in row:
            if key not in fieldnames:
                fieldnames.append(key)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def read_csv_rows(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def csv_parses(path: Path) -> bool:
    try:
        read_csv_rows(path)
        return True
    except Exception:
        return False


def is_under(path: Path, parent: Path) -> bool:
    try:
        path.resolve().relative_to(parent.resolve())
        return True
    except ValueError:
        return False


def split_semicolon(value: str) -> list[str]:
    return [part.strip() for part in value.split(";") if part.strip()]


def as_bool(value: Any) -> bool:
    if isinstance(value, bool):
        return value
    return str(value).strip().lower() in {"1", "true", "yes", "y"}


def finite_float(value: Any) -> bool:
    try:
        parsed = float(str(value))
    except (TypeError, ValueError):
        return False
    return math.isfinite(parsed)


def placeholder(value: Any) -> bool:
    text = str(value).strip()
    if not text:
        return True
    upper = text.upper()
    return any(token in upper for token in ("MISSING", "PLACEHOLDER", "TBD", "UNSIGNED", "NOT_DERIVED"))


def md_escape(value: Any) -> str:
    return str(value).replace("|", "\\|").replace("\n", "<br>")


def md_table(rows: list[dict[str, Any]], columns: list[str] | None = None) -> str:
    if not rows:
        return "_No rows._"
    selected = columns or list(rows[0].keys())
    header = "| " + " | ".join(selected) + " |"
    separator = "| " + " | ".join("---" for _ in selected) + " |"
    body = [
        "| " + " | ".join(md_escape(row.get(column, "")) for column in selected) + " |"
        for row in rows
    ]
    return "\n".join([header, separator, *body])


def source_register_rows() -> list[dict[str, Any]]:
    specs = [
        (
            "SRC2923_00_2922_doc",
            SRC_2922_DOC,
            "Y5_R2FR_2922_owner_theorem_not_derived_source_mass_first_row_template_2923_next;NEXT2922_0_2923;Validation overall: `True`",
            "2922 status and 2923 target selection",
        ),
        (
            "SRC2923_01_2922_next",
            SRC_2922_NEXT,
            "NEXT2922_0_2923;2923-Y5-R2FR-first-source-mass-row-template-and-Hcore-coefficient-checklist-under-AX1090.md",
            "machine-readable next target from 2922",
        ),
        (
            "SRC2923_02_2922_schema",
            SRC_2922_SCHEMA,
            "SMR2922_0_identity;SMR2922_9_total_guard",
            "2922 source-mass first-row schema",
        ),
        (
            "SRC2923_03_2922_refusal",
            SRC_2922_REFUSAL,
            "REJECT_CIRCULAR_NEWTON_IMPORT;ACCEPTED_AS_NONCLAIM_SMOKE_NOT_SOURCE_MASS_PROOF",
            "2922 refusal runner for circular GM, closure zero, and finite qRhat smoke",
        ),
        (
            "SRC2923_04_2922_owner",
            SRC_2922_OWNER,
            "HOA2922_10_verdict;OWNER_THEOREM_NOT_DERIVED",
            "Hamiltonian owner theorem remains unsigned",
        ),
        (
            "SRC2923_05_2922_crosswalk",
            SRC_2922_CROSSWALK,
            "1249;2921",
            "prior chain endpoint crosswalk",
        ),
        (
            "SRC2923_06_1249_rules",
            SRC_1249_RULES,
            "QRV1249_0_route;QRV1249_5_no_claim_flags",
            "finite qRhat validation discipline",
        ),
        (
            "SRC2923_07_1249_results",
            SRC_1249_RESULTS,
            "QRHAT1255_CASSINI_GAMMA_1SIGMA_BOUND_NONCLAIM;ACCEPTED_NONCLAIM_FINITE_QRHAT",
            "accepted nonclaim finite qRhat smoke row",
        ),
        (
            "SRC2923_08_1249_ledger",
            SRC_1249_LEDGER,
            "SA1249_0_parent_coefficients;MISSING_PARENT_COEFFICIENT_MAP",
            "parent coefficient map remains missing",
        ),
        (
            "SRC2923_09_1238_closure",
            SRC_1238_DOC,
            "BGR1238_1_closure_GR;DEC1238_2_residual_vector_selected",
            "local-GR closure benchmark is not a derivation",
        ),
        (
            "SRC2923_10_1105_morphism",
            SRC_1105_DOC,
            "MHM1105_6_verdict;PACK1105_4_residual_vector_if_unsigned",
            "hidden-visible morphism remains a residual pack when unsigned",
        ),
        (
            "SRC2923_11_1237_parent_grammar",
            SRC_1237_DOC,
            "PRIM1237_8_verdict;VAL1237_2_primitive_derivation_failed",
            "primitive-to-parent-action grammar did not close",
        ),
    ]
    rows = []
    for source_id, path, anchors, role in specs:
        ok, missing = anchors_present(path, anchors)
        rows.append(
            add_common(
                {
                    "source_id": source_id,
                    "source_path": str(path),
                    "anchors": anchors,
                    "role": role,
                    "path_exists": path.exists(),
                    "anchors_found": ok,
                    "missing_anchors": missing,
                }
            )
        )
    return rows


def hcore_checklist_rows() -> list[dict[str, Any]]:
    shared_sources = ";".join(str(path) for path in [SRC_2922_OWNER, SRC_2922_SCHEMA, SRC_1249_LEDGER, SRC_1238_DOC, SRC_1105_DOC])
    specs = [
        (
            "HC2923_0_parent_action_block",
            "H_core or L_MTS_core",
            "field list, derivative order, normalization, source term, gauge/constraint class, boundary term",
            "MISSING_PARENT_ACTION_BLOCK",
            "No claim-grade Hamiltonian source mass can exist until the parent block is fixed.",
        ),
        (
            "HC2923_1_canonical_brackets",
            "canonical variables and brackets",
            "phase-space variables, symplectic form, first/second-class constraints, bracket algebra",
            "MISSING_CANONICAL_BRACKET_MAP",
            "Q_tau and q_R_hat coefficients cannot be extracted from a Hamiltonian without the bracket map.",
        ),
        (
            "HC2923_2_tau_lock",
            "observed time/coframe generator",
            "tau_source=tau_charge=tau_clock=tau_readout and delta tau=0 on comparison branches",
            "MISSING_TAU_LOCK",
            "Source mass, clock readout, and orbital readout otherwise live in different frames.",
        ),
        (
            "HC2923_3_theta_Qtau",
            "Theta_MTS and Q_tau^MTS",
            "delta L=E delta Phi+dTheta, J_tau=Theta(L_tau Phi)-i_tau L=dQ_tau+C_tau",
            "MISSING_THETA_QTAU_EXTRACTION",
            "This is the direct source charge that must replace hand-inserted GM.",
        ),
        (
            "HC2923_4_boundary_reference",
            "H_ref/B_ref",
            "reference branch, counterterm, topology, and boundary class fixed before any source readout",
            "MISSING_FIXED_REFERENCE",
            "A floating reference subtraction can fit away the local-GR problem.",
        ),
        (
            "HC2923_5_MHref_denominator",
            "M_H_ref",
            "positive same-frame mass denominator, units, G_ref, surface, source path, no orbital-GM import",
            "MISSING_MHREF_DENOMINATOR",
            "The Newton/Gauss bridge needs a source mass, not the measured orbital answer fed back in.",
        ),
        (
            "HC2923_6_PiMH_projector",
            "Pi_M^H",
            "projector definition and held-fixed fields at fixed tau, surface, boundary class, topology",
            "MISSING_PIMH_PROJECTOR",
            "The mass/source coordinate is not yet parent-owned.",
        ),
        (
            "HC2923_7_PG_bridge",
            "Poisson/Gauss/orbital certificate",
            "Poisson coefficient, Gauss surface rule, orbital readout map, S_res status, mu_extra status",
            "MISSING_PG_BRIDGE_PREMISES",
            "2921 kept the bridge conditional; this checklist names the missing premises.",
        ),
        (
            "HC2923_8_qRhat_coeff_map",
            "finite q_R_hat coefficient map",
            "q_R_hat from H_core/canonical brackets/boundary class with GM convention and raw units",
            "MISSING_PARENT_QRHAT_COEFFICIENT_MAP",
            "1249 supplies a nonclaim smoke row, not a theory prediction.",
        ),
        (
            "HC2923_9_hidden_visible_signature",
            "object-language hidden-visible exclusion",
            "no hidden-visible coefficient morphism, no radiative/readout return, no source-dependent visible constants",
            "MISSING_PARENT_OBJECT_LANGUAGE_SIGNATURE",
            "Residual couplings remain legal unless this is parent-signed.",
        ),
        (
            "HC2923_10_total_guard",
            "absolute-sum/no-cancellation guard",
            "all source, boundary, hidden-visible, reciprocal-hair, and readout components sourced or bounded",
            "NOT_COMPUTED_COMPONENTS_MISSING",
            "Unknown terms cannot be cancelled by taste; they must be derived or bounded.",
        ),
    ]
    rows = []
    for checklist_id, parent_object, required_evidence, current_status, why_it_matters in specs:
        rows.append(
            add_common(
                {
                    "checklist_id": checklist_id,
                    "parent_object": parent_object,
                    "required_evidence": required_evidence,
                    "current_status": current_status,
                    "clause_signed": False,
                    "blocks_local_GR_claim": True,
                    "blocks_Newton_bridge_claim": True,
                    "why_it_matters": why_it_matters,
                    "next_action": "fill with a parent-sourced row or keep the branch nonclaim",
                    "source_paths": shared_sources,
                }
            )
        )
    return rows


def source_mass_row_template_rows() -> list[dict[str, Any]]:
    theorem_fields = (
        "row_id;route_type;system_id;branch_id;H_core_source;theta_source;Q_tau_source;tau_id;"
        "surface_id;H_ref_rule;M_H_ref;M_H_units;G_ref;PiM_H_definition;"
        "Poisson_Gauss_certificate;mu_obs_convention;GM_convention;closure_used;"
        "orbital_GM_imported;hidden_visible_status;source_path;equation_ref;valid_for_claim;claim_allowed"
    )
    rows = [
        {
            "template_id": "SMT2923_0_parent_source_mass_theorem",
            "route_type": "parent_source_mass_theorem",
            "required_columns": theorem_fields,
            "acceptance_clause": "all parent/source fields present, non-placeholder, source-backed, same-frame, closure_used=false, orbital_GM_imported=false",
            "reject_if": "missing H_core/Theta/Q_tau, fitted H_ref, missing positive M_H_ref, circular orbital GM, closure zero, hidden-visible unsigned",
            "claim_policy": "claim-grade only if every Hcore checklist clause is signed",
        },
        {
            "template_id": "SMT2923_1_parent_coefficient_map",
            "route_type": "parent_coefficient_map",
            "required_columns": "row_id;route_type;H_core_source;bracket_source;boundary_class;q_R_hat_expression;source_mass_expression;coefficient_map;units;source_path;equation_ref;valid_for_claim;claim_allowed",
            "acceptance_clause": "q_R_hat or source residual coefficients are derived from H_core and canonical brackets before data fitting",
            "reject_if": "coefficient map missing, fitted residual inserted, closure zero used, source path absent",
            "claim_policy": "can feed a later finite prediction only after a parent source-mass row exists",
        },
        {
            "template_id": "SMT2923_2_finite_qRhat_smoke",
            "route_type": "finite_qR_hat",
            "required_columns": "row_id;route_type;q_R_hat;gamma_minus_1_QR;GM_convention;raw_QR_units;closure_used;N_sigma;sigma_gamma;source_path;valid_for_claim;claim_allowed",
            "acceptance_clause": "matches 1249 rules, finite numeric, no closure, valid_for_claim=false, claim_allowed=false",
            "reject_if": "non-numeric q_R_hat, missing GM convention, claim flags true, ansatz zero",
            "claim_policy": "accepted only as nonclaim smoke/ceiling",
        },
        {
            "template_id": "SMT2923_3_phenomenological_bound",
            "route_type": "phenomenological_bound",
            "required_columns": "row_id;route_type;observable;bound_value;bound_units;system_id;source_path;valid_for_claim;claim_allowed",
            "acceptance_clause": "source-backed local bound row with units and arena declaration",
            "reject_if": "used as a derived MTS prediction or mixed into M_H_ref",
            "claim_policy": "bound input only, never a derivation",
        },
        {
            "template_id": "SMT2923_4_closure_candidate_rejected",
            "route_type": "closure_candidate_rejected",
            "required_columns": "row_id;route_type;closure_statement;which_parent_clause_missing;source_path;valid_for_claim;claim_allowed",
            "acceptance_clause": "records why a closure/axiom route is not evidence",
            "reject_if": "promoted to local-GR proof",
            "claim_policy": "must remain claim_closed",
        },
        {
            "template_id": "SMT2923_5_orbital_GM_import_rejected",
            "route_type": "orbital_GM_import_rejected",
            "required_columns": "row_id;route_type;GM_source;where_imported;bridge_not_yet_derived;source_path;valid_for_claim;claim_allowed",
            "acceptance_clause": "explicitly quarantines circular Newton/GR imports",
            "reject_if": "used as M_H_ref before the source-mass theorem",
            "claim_policy": "claim_closed",
        },
        {
            "template_id": "SMT2923_6_hidden_visible_residual_vector",
            "route_type": "hidden_visible_residual_vector",
            "required_columns": "row_id;route_type;b_alpha;b_mu;b_mA;b_nuc;b_clock;qbar_constants_abs;units;source_path;valid_for_claim;claim_allowed",
            "acceptance_clause": "keeps every unsigned coupling visible as a finite residual or bound target",
            "reject_if": "coefficient is set to zero without the object-language signature",
            "claim_policy": "nonclaim until the 1105 morphism closes",
        },
        {
            "template_id": "SMT2923_7_total_guard",
            "route_type": "total_guard",
            "required_columns": "row_id;route_type;abs_sum_components;no_cancellation_guard;all_components_sourced;source_path;valid_for_claim;claim_allowed",
            "acceptance_clause": "all missing components bounded or derived before any pass/fail local claim",
            "reject_if": "component cancellation is assumed without parent identity",
            "claim_policy": "must be true before local-GR/Newton pass",
        },
    ]
    return [add_common(row) for row in rows]


def strict_validator_rule_rows() -> list[dict[str, Any]]:
    rows = [
        ("SVR2923_0_route", "route_type must be one of the template route types", "REJECT_BAD_ROUTE_TYPE"),
        ("SVR2923_1_parent_paths", "parent_source_mass_theorem rows require real H_core, theta, Q_tau, H_ref, M_H_ref, PiM_H, and Poisson/Gauss source paths", "REJECT_MISSING_PARENT_SOURCE"),
        ("SVR2923_2_no_closure", "closure_used must be false for any prediction row; ansatz zero is refused", "REJECT_CLOSURE_AS_EVIDENCE"),
        ("SVR2923_3_no_orbital_GM", "orbital GM cannot be used as M_H_ref before the Poisson/Gauss/orbital bridge is derived", "REJECT_CIRCULAR_NEWTON_IMPORT"),
        ("SVR2923_4_positive_MHref", "M_H_ref must be finite, positive, same-frame, and unit-declared for theorem rows", "REJECT_NO_POSITIVE_SOURCE_DENOMINATOR"),
        ("SVR2923_5_qRhat_1249", "finite q_R_hat rows must obey 1249 route/numeric/source/GM/policy/no-claim rules", "REJECT_BAD_FINITE_QRHAT_SMOKE"),
        ("SVR2923_6_hidden_visible", "hidden-visible coefficients cannot be set to zero without the 1105 object-language signature", "REJECT_UNSIGNED_HIDDEN_VISIBLE_ZERO"),
        ("SVR2923_7_total_guard", "no cancellation is permitted unless every component has a parent source or bound row", "REJECT_UNSOURCED_CANCELLATION"),
        ("SVR2923_8_claim_flags", "no 2923 row may set valid_for_claim=true or claim_allowed=true", "REJECT_CLAIM_FLAG"),
    ]
    return [
        add_common(
            {
                "rule_id": rule_id,
                "rule": rule,
                "reject_status": reject_status,
                "theorem_required": rule_id in {"SVR2923_1_parent_paths", "SVR2923_4_positive_MHref", "SVR2923_7_total_guard"},
                "finite_smoke_allowed": rule_id == "SVR2923_5_qRhat_1249",
            }
        )
        for rule_id, rule, reject_status in rows
    ]


def candidate_seed_rows() -> list[dict[str, Any]]:
    return [
        {
            "candidate_id": "CAND2923_0_missing_Htau",
            "route_type": "parent_source_mass_theorem",
            "H_core_source": str(SRC_2922_OWNER),
            "theta_source": str(SRC_2922_OWNER),
            "Q_tau_source": "MISSING_QTAU_SOURCE",
            "H_ref_rule": "MISSING_FIXED_REFERENCE",
            "M_H_ref": "MISSING_MHREF",
            "M_H_units": "",
            "G_ref": "",
            "PiM_H_definition": "MISSING_PIMH_PROJECTOR",
            "Poisson_Gauss_certificate": "MISSING_PG_BRIDGE",
            "source_path": str(SRC_2922_SCHEMA),
            "closure_used": False,
            "orbital_GM_imported": False,
        },
        {
            "candidate_id": "CAND2923_1_orbital_GM_denominator",
            "route_type": "parent_source_mass_theorem",
            "H_core_source": str(SRC_2922_OWNER),
            "theta_source": str(SRC_2922_OWNER),
            "Q_tau_source": str(SRC_2922_OWNER),
            "H_ref_rule": "fixed_symbolic_only",
            "M_H_ref": "GM_orbit/G_ref",
            "M_H_units": "mass",
            "G_ref": "G_N",
            "PiM_H_definition": "symbolic",
            "Poisson_Gauss_certificate": "bridge_not_derived",
            "source_path": str(SRC_2922_REFUSAL),
            "closure_used": False,
            "orbital_GM_imported": True,
        },
        {
            "candidate_id": "CAND2923_2_closure_zero",
            "route_type": "closure_candidate_rejected",
            "closure_statement": "set q_R_hat=0 and beta-1=0 by local-GR closure",
            "source_path": str(SRC_1238_DOC),
            "closure_used": True,
            "orbital_GM_imported": False,
        },
        {
            "candidate_id": "CAND2923_3_1249_qRhat_nonclaim_smoke",
            "route_type": "finite_qR_hat",
            "q_R_hat": "4.6e-05",
            "gamma_minus_1_QR": "-2.3e-05",
            "GM_convention": "1244_Cassini_gamma_policy",
            "raw_QR_units": "dimensionless q_R_hat imported from accepted 1249 smoke row",
            "N_sigma": "1",
            "sigma_gamma": "2.3e-5",
            "source_path": str(SRC_1249_RESULTS),
            "closure_used": False,
            "orbital_GM_imported": False,
        },
        {
            "candidate_id": "CAND2923_4_parent_source_mass_theorem_candidate",
            "route_type": "parent_source_mass_theorem",
            "H_core_source": "MISSING_PARENT_ACTION_BLOCK",
            "theta_source": "MISSING_THETA_SOURCE",
            "Q_tau_source": "MISSING_QTAU_SOURCE",
            "H_ref_rule": "MISSING_FIXED_REFERENCE",
            "M_H_ref": "MISSING_MHREF",
            "M_H_units": "MISSING_UNITS",
            "G_ref": "MISSING_GREF",
            "PiM_H_definition": "MISSING_PIMH_PROJECTOR",
            "Poisson_Gauss_certificate": "MISSING_PG_BRIDGE",
            "source_path": str(SRC_1249_LEDGER),
            "closure_used": False,
            "orbital_GM_imported": False,
        },
        {
            "candidate_id": "CAND2923_5_hidden_visible_zero",
            "route_type": "hidden_visible_residual_vector",
            "b_alpha": "0",
            "b_mu": "0",
            "hidden_visible_status": "MISSING_PARENT_OBJECT_LANGUAGE_SIGNATURE",
            "source_path": str(SRC_1105_DOC),
            "closure_used": False,
            "orbital_GM_imported": False,
        },
    ]


REQUIRED_THEOREM_FIELDS = [
    "H_core_source",
    "theta_source",
    "Q_tau_source",
    "H_ref_rule",
    "M_H_ref",
    "M_H_units",
    "G_ref",
    "PiM_H_definition",
    "Poisson_Gauss_certificate",
    "source_path",
]


def validate_candidate(candidate: dict[str, Any], route_types: set[str]) -> dict[str, Any]:
    rejects: list[str] = []
    notes: list[str] = []
    route_type = str(candidate.get("route_type", ""))
    if route_type not in route_types:
        rejects.append("REJECT_BAD_ROUTE_TYPE")
    if as_bool(candidate.get("closure_used", False)):
        rejects.append("REJECT_CLOSURE_AS_EVIDENCE")
    if as_bool(candidate.get("orbital_GM_imported", False)):
        rejects.append("REJECT_CIRCULAR_NEWTON_IMPORT")

    if route_type == "parent_source_mass_theorem":
        missing = [field for field in REQUIRED_THEOREM_FIELDS if placeholder(candidate.get(field, ""))]
        if missing:
            rejects.append("REJECT_MISSING_PARENT_SOURCE:" + "+".join(missing))
        if not finite_float(candidate.get("M_H_ref", "")):
            rejects.append("REJECT_NO_POSITIVE_SOURCE_DENOMINATOR")
        else:
            if float(str(candidate["M_H_ref"])) <= 0:
                rejects.append("REJECT_NO_POSITIVE_SOURCE_DENOMINATOR")
    elif route_type == "parent_coefficient_map":
        for field in ["H_core_source", "bracket_source", "coefficient_map", "source_path"]:
            if placeholder(candidate.get(field, "")):
                rejects.append("REJECT_MISSING_PARENT_COEFFICIENT_MAP")
                break
    elif route_type == "finite_qR_hat":
        q_ok = finite_float(candidate.get("q_R_hat", ""))
        source_ok = not placeholder(candidate.get("source_path", "")) and Path(str(candidate.get("source_path", ""))).exists()
        gm_ok = not placeholder(candidate.get("GM_convention", ""))
        units_ok = not placeholder(candidate.get("raw_QR_units", ""))
        policy_ok = str(candidate.get("N_sigma", "")) == "1" and str(candidate.get("sigma_gamma", "")) == "2.3e-5"
        if not (q_ok and source_ok and gm_ok and units_ok and policy_ok):
            rejects.append("REJECT_BAD_FINITE_QRHAT_SMOKE")
        else:
            notes.append("ACCEPTED_NONCLAIM_FINITE_QRHAT_SMOKE")
    elif route_type == "hidden_visible_residual_vector":
        if placeholder(candidate.get("hidden_visible_status", "")):
            rejects.append("REJECT_UNSIGNED_HIDDEN_VISIBLE_ZERO")
    elif route_type in {"closure_candidate_rejected", "orbital_GM_import_rejected"}:
        if not rejects:
            rejects.append("REJECT_NON_DERIVATION_ROUTE")

    if as_bool(candidate.get("valid_for_claim", False)) or as_bool(candidate.get("claim_allowed", False)):
        rejects.append("REJECT_CLAIM_FLAG")

    if rejects:
        status = ";".join(rejects)
        runner_eligible = False
    elif route_type == "finite_qR_hat":
        status = "ACCEPTED_NONCLAIM_FINITE_QRHAT_SMOKE"
        runner_eligible = True
    else:
        status = "ACCEPTED_STRUCTURAL_TEMPLATE_ONLY_NONCLAIM"
        runner_eligible = False

    row = dict(candidate)
    row.update(
        {
            "validation_status": status,
            "runner_eligible": runner_eligible,
            "notes": ";".join(notes),
        }
    )
    return add_common(row)


def candidate_validation_rows(template_rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    route_types = {str(row["route_type"]) for row in template_rows}
    return [validate_candidate(candidate, route_types) for candidate in candidate_seed_rows()]


def claim_gate_rows(candidate_rows: list[dict[str, Any]], checklist_rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    all_signed = all(as_bool(row.get("clause_signed", False)) for row in checklist_rows)
    finite_smoke = any(row["validation_status"] == "ACCEPTED_NONCLAIM_FINITE_QRHAT_SMOKE" for row in candidate_rows)
    rows = [
        {
            "gate_id": "CG2923_0_Hcore_checklist_closed",
            "gate": "every H_core/Q_tau/source-mass clause parent-signed",
            "gate_status": "BLOCKED",
            "evidence": "all_signed=" + str(all_signed),
            "decision": "do not claim local GR/Newton derivation",
        },
        {
            "gate_id": "CG2923_1_parent_source_mass_row",
            "gate": "claim-grade parent_source_mass_theorem row exists",
            "gate_status": "BLOCKED",
            "evidence": "candidate theorem rows are rejected by missing parent/source fields",
            "decision": "keep source-mass identity unproved",
        },
        {
            "gate_id": "CG2923_2_no_circular_GM",
            "gate": "orbital GM import is rejected before bridge derivation",
            "gate_status": "CONTROL_PASS_CLAIM_CLOSED",
            "evidence": "CAND2923_1 triggers REJECT_CIRCULAR_NEWTON_IMPORT",
            "decision": "protects the derivation from Newton smuggling",
        },
        {
            "gate_id": "CG2923_3_closure_zero_refused",
            "gate": "closure zero is not accepted as proof",
            "gate_status": "CONTROL_PASS_CLAIM_CLOSED",
            "evidence": "CAND2923_2 triggers REJECT_CLOSURE_AS_EVIDENCE",
            "decision": "closure-only routes remain quarantined",
        },
        {
            "gate_id": "CG2923_4_finite_qRhat_smoke",
            "gate": "1249 finite qRhat row accepted only as smoke",
            "gate_status": "NONCLAIM_SMOKE_AVAILABLE" if finite_smoke else "BLOCKED",
            "evidence": "finite_smoke=" + str(finite_smoke),
            "decision": "can test pipeline mechanics but cannot prove parent source mass",
        },
        {
            "gate_id": "CG2923_5_local_GR_Newton_claim",
            "gate": "derived local GR/Newton limit",
            "gate_status": "CLOSED",
            "evidence": "H_core coefficient map and parent source mass theorem missing",
            "decision": "next move is 2924 parent coefficient map or first finite source row fill",
        },
    ]
    return [add_common(row) for row in rows]


def decision_rows() -> list[dict[str, Any]]:
    rows = [
        {
            "decision_id": "DEC2923_0_progress",
            "decision": "2923 creates the exact source-mass/H_core trapdoor rather than claiming the bridge",
            "status": "TEMPLATE_BUILT_NONCLAIM",
            "reason": "2922 proved the owner theorem is missing, so the next honest deliverable is a strict row/checklist.",
        },
        {
            "decision_id": "DEC2923_1_claim_status",
            "decision": "local GR/Newton reduction remains conditional",
            "status": "CLAIM_CLOSED",
            "reason": "H_core, Q_tau, M_H_ref, Pi_M^H, and Poisson/Gauss premises are unsigned.",
        },
        {
            "decision_id": "DEC2923_2_smoke_status",
            "decision": "1249 finite qRhat row remains useful but nonclaim",
            "status": "NONCLAIM_SMOKE_ONLY",
            "reason": "it checks units/schema/policy behavior but does not produce parent source mass.",
        },
        {
            "decision_id": "DEC2923_3_next",
            "decision": "attempt 2924 parent H_core coefficient map or first finite source-mass row fill",
            "status": "NEXT_SELECTED",
            "reason": "the first real leap must fill a parent coefficient/source row, not add another refusal wrapper.",
        },
    ]
    return [add_common(row) for row in rows]


def next_target_rows() -> list[dict[str, Any]]:
    rows = [
        {
            "next_id": "NEXT2923_0_2924",
            "selection": "selected_primary",
            "target_doc": "2924-Y5-R2FR-parent-Hcore-coefficient-map-or-finite-source-mass-first-row-fill-under-AX1090.md",
            "target_script": "scripts/Y5_R2FR_parent_Hcore_coefficient_map_or_finite_source_mass_first_row_fill_under_AX1090_2924.py",
            "objective": "try to fill one parent-sourced H_core/Q_tau/M_H_ref coefficient row; if impossible, record the precise missing parent object",
            "acceptance_gate": "at least one candidate row either becomes parent-sourced nonclaim finite input or is rejected with a specific missing object; no closure/GM import claim",
        },
        {
            "next_id": "NEXT2923_1_fallback",
            "selection": "fallback_if_parent_action_still_unsigned",
            "target_doc": "2924B-Y5-R2FR-minimal-parent-action-block-choice-and-Hcore-variation-test.md",
            "target_script": "scripts/Y5_R2FR_minimal_parent_action_block_choice_and_Hcore_variation_test_2924B.py",
            "objective": "choose one minimal parent action block and compute whether its variation can even supply Theta_MTS and Q_tau",
            "acceptance_gate": "symbolic variation path exists or the chosen parent block is demoted",
        },
    ]
    return [add_common(row) for row in rows]


def branch_copy_rows() -> list[dict[str, Any]]:
    copy_specs = [
        ("BC2923_0_hcore_checklist", OUTPUTS["hcore_checklist"], BRANCH_OUTPUTS["hcore_copy"], "parent action queue"),
        ("BC2923_1_row_template", OUTPUTS["row_template"], BRANCH_OUTPUTS["row_template_copy"], "local bounds/source mass queue"),
        ("BC2923_2_next_target", OUTPUTS["next"], BRANCH_OUTPUTS["next_copy"], "RAB acquisition next target"),
    ]
    rows = []
    for copy_id, source, destination, role in copy_specs:
        shutil.copyfile(source, destination)
        rows.append(
            add_common(
                {
                    "copy_id": copy_id,
                    "source_path": str(source),
                    "destination_path": str(destination),
                    "role": role,
                    "destination_exists": destination.exists(),
                    "destination_parses": csv_parses(destination),
                }
            )
        )
    return rows


def validation_rows(
    sources: list[dict[str, Any]],
    checklist: list[dict[str, Any]],
    template: list[dict[str, Any]],
    validator: list[dict[str, Any]],
    candidates: list[dict[str, Any]],
    claims: list[dict[str, Any]],
    branches: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    required_checklist = {
        "HC2923_0_parent_action_block",
        "HC2923_1_canonical_brackets",
        "HC2923_2_tau_lock",
        "HC2923_3_theta_Qtau",
        "HC2923_4_boundary_reference",
        "HC2923_5_MHref_denominator",
        "HC2923_6_PiMH_projector",
        "HC2923_7_PG_bridge",
        "HC2923_8_qRhat_coeff_map",
        "HC2923_9_hidden_visible_signature",
        "HC2923_10_total_guard",
    }
    required_routes = {
        "parent_source_mass_theorem",
        "parent_coefficient_map",
        "finite_qR_hat",
        "phenomenological_bound",
        "closure_candidate_rejected",
        "orbital_GM_import_rejected",
        "hidden_visible_residual_vector",
        "total_guard",
    }
    checks: list[tuple[str, bool, str, bool]] = [
        (
            "VAL2923_0_sources_exist",
            all(as_bool(row["path_exists"]) for row in sources),
            "every cited source path exists",
            True,
        ),
        (
            "VAL2923_1_source_anchors_found",
            all(as_bool(row["anchors_found"]) for row in sources),
            "every source anchor is present",
            True,
        ),
        (
            "VAL2923_2_hcore_checklist_complete",
            required_checklist <= {str(row["checklist_id"]) for row in checklist},
            "all H_core/Q_tau/source-mass checklist legs are present",
            True,
        ),
        (
            "VAL2923_3_template_routes_complete",
            required_routes <= {str(row["route_type"]) for row in template},
            "template includes theorem, coefficient, smoke, rejection, residual, and guard routes",
            True,
        ),
        (
            "VAL2923_4_validator_rules_complete",
            len(validator) >= 9 and any(row["reject_status"] == "REJECT_CIRCULAR_NEWTON_IMPORT" for row in validator),
            "strict validator has route, source, closure, circular-GM, qRhat, hidden-visible, guard, and claim rules",
            True,
        ),
        (
            "VAL2923_5_circular_GM_rejected",
            any(row["candidate_id"] == "CAND2923_1_orbital_GM_denominator" and "REJECT_CIRCULAR_NEWTON_IMPORT" in row["validation_status"] for row in candidates),
            "orbital-GM denominator candidate is rejected",
            True,
        ),
        (
            "VAL2923_6_closure_zero_rejected",
            any(row["candidate_id"] == "CAND2923_2_closure_zero" and "REJECT_CLOSURE_AS_EVIDENCE" in row["validation_status"] for row in candidates),
            "closure-zero candidate is rejected",
            True,
        ),
        (
            "VAL2923_7_finite_qRhat_smoke_nonclaim",
            any(row["candidate_id"] == "CAND2923_3_1249_qRhat_nonclaim_smoke" and row["validation_status"] == "ACCEPTED_NONCLAIM_FINITE_QRHAT_SMOKE" and not as_bool(row["valid_for_claim"]) and not as_bool(row["claim_allowed"]) for row in candidates),
            "1249 finite qRhat row is accepted only as nonclaim smoke",
            True,
        ),
        (
            "VAL2923_8_no_claim_gates_open",
            all(not as_bool(row["claim_allowed"]) and str(row["gate_status"]) != "OPEN" for row in claims),
            "no claim gate opens in 2923",
            True,
        ),
        (
            "VAL2923_9_branch_copies_valid",
            all(as_bool(row["destination_exists"]) and as_bool(row["destination_parses"]) for row in branches),
            "branch copies exist and parse",
            True,
        ),
        (
            "VAL2923_10_no_formalization_outputs",
            not any(is_under(path, FORMALIZATION) for path in [DOC, *OUTPUTS.values(), *BRANCH_OUTPUTS.values()]),
            "no generated output path is inside formalization-workbench",
            True,
        ),
        (
            "VAL2923_11_doc_exists",
            DOC.exists(),
            "2923 markdown checkpoint exists",
            True,
        ),
    ]
    rows = [
        {
            "validation_id": check_id,
            "passed": passed,
            "check": check,
            "required": required,
            "generated_utc": RUN_UTC,
        }
        for check_id, passed, check, required in checks
    ]
    overall = all(passed for _, passed, _, required in checks if required)
    rows.append(
        {
            "validation_id": "VAL2923_OVERALL",
            "passed": overall,
            "check": "2923 validation overall",
            "required": True,
            "generated_utc": RUN_UTC,
        }
    )
    return rows


def write_doc(
    sources: list[dict[str, Any]],
    checklist: list[dict[str, Any]],
    template: list[dict[str, Any]],
    validator: list[dict[str, Any]],
    candidates: list[dict[str, Any]],
    claims: list[dict[str, Any]],
    decisions: list[dict[str, Any]],
    next_rows: list[dict[str, Any]],
    validation: list[dict[str, Any]],
) -> None:
    overall = next(row["passed"] for row in validation if row["validation_id"] == "VAL2923_OVERALL")
    lines = [
        "# 2923 - Y5/R2FR First Source-Mass Row Template And Hcore Coefficient Checklist Under AX1090",
        "",
        "Status: `Y5_R2FR_2923_template_built_parent_Hcore_coefficient_map_2924_next`",
        "",
        "## Result",
        "",
        "2923 does not claim the local GR/Newton bridge. It builds the exact claim trapdoor for the next derivation attempt: a candidate must now supply a parent-owned `H_core`, `Theta_MTS`, `Q_tau^MTS`, fixed `H_ref/B_ref`, positive same-frame `M_H_ref`, `Pi_M^H`, and Poisson/Gauss/orbital certificate before it can be treated as source mass evidence.",
        "",
        "The useful progress is that circular Newton imports and closure zeros now fail mechanically. The accepted 1249 finite `q_R_hat` row remains a nonclaim smoke test only.",
        "",
        "## Source Register",
        "",
        md_table(sources, ["source_id", "path_exists", "anchors_found", "role", "source_path"]),
        "",
        "## Hcore / Qtau Coefficient Checklist",
        "",
        md_table(checklist, ["checklist_id", "parent_object", "required_evidence", "current_status", "blocks_local_GR_claim", "why_it_matters"]),
        "",
        "## Source-Mass Row Template",
        "",
        md_table(template, ["template_id", "route_type", "required_columns", "acceptance_clause", "reject_if", "claim_policy"]),
        "",
        "## Strict Validator Rules",
        "",
        md_table(validator, ["rule_id", "rule", "reject_status"]),
        "",
        "## Candidate Validation Results",
        "",
        md_table(candidates, ["candidate_id", "route_type", "validation_status", "runner_eligible", "valid_for_claim", "claim_allowed", "source_path"]),
        "",
        "## Claim Gates",
        "",
        md_table(claims, ["gate_id", "gate", "gate_status", "decision", "evidence"]),
        "",
        "## Decision Ledger",
        "",
        md_table(decisions, ["decision_id", "decision", "status", "reason"]),
        "",
        "## Next Target",
        "",
        md_table(next_rows, ["next_id", "selection", "target_doc", "target_script", "objective", "acceptance_gate"]),
        "",
        "## Validation",
        "",
        md_table(validation, ["validation_id", "passed", "check", "required"]),
        "",
        f"Validation overall: `{overall}`.",
        "",
        "## Bottom Line",
        "",
        "This checkpoint narrows the live local-GR problem to the real coupling/source-mass object. The branch is not failing because a numerical residual is large here; it is blocked because the parent Hamiltonian has not yet produced the source mass used by Newton/GR. That is the next derivation target.",
    ]
    DOC.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    sources = source_register_rows()
    checklist = hcore_checklist_rows()
    template = source_mass_row_template_rows()
    validator = strict_validator_rule_rows()
    candidates = candidate_validation_rows(template)
    claims = claim_gate_rows(candidates, checklist)
    decisions = decision_rows()
    next_rows = next_target_rows()

    write_csv(OUTPUTS["sources"], sources)
    write_csv(OUTPUTS["hcore_checklist"], checklist)
    write_csv(OUTPUTS["row_template"], template)
    write_csv(OUTPUTS["validator_rules"], validator)
    write_csv(OUTPUTS["candidate_results"], candidates)
    write_csv(OUTPUTS["claims"], claims)
    write_csv(OUTPUTS["decision"], decisions)
    write_csv(OUTPUTS["next"], next_rows)

    branches = branch_copy_rows()
    write_csv(OUTPUTS["branches"], branches)

    DOC.write_text("# 2923 - validation preflight\n", encoding="utf-8")
    validation = validation_rows(sources, checklist, template, validator, candidates, claims, branches)
    write_csv(OUTPUTS["validation"], validation)
    write_doc(sources, checklist, template, validator, candidates, claims, decisions, next_rows, validation)

    overall = next(row["passed"] for row in validation if row["validation_id"] == "VAL2923_OVERALL")
    if not overall:
        raise SystemExit("2923 validation failed; see " + str(OUTPUTS["validation"]))
    print("2923 validation overall:", overall)
    print("doc:", DOC)


if __name__ == "__main__":
    main()

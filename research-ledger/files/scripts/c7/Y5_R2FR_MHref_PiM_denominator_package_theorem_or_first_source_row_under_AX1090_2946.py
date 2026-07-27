from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


SCRIPT_START_UTC = datetime.now(timezone.utc)

ROOT = Path(__file__).resolve().parents[1]
PROJECT = ROOT.parent
RESIDUALS = ROOT / "source-intake" / "mts_residuals"
LOCAL_BOUNDS = ROOT / "source-intake" / "local_bounds"
PARENT_ACTION = ROOT / "source-intake" / "parent-action"
RAB_QUEUE = ROOT / "source-intake" / "rab-sector" / "acquisition-queue"
FORMALIZATION = PROJECT / "formalization-workbench"

CHECKPOINT = "2946"
BRANCH_ID = "MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428"
RUN_UTC = SCRIPT_START_UTC.isoformat()

DOC = ROOT / "2946-Y5-R2FR-MHref-PiM-denominator-package-theorem-or-first-source-row-under-AX1090.md"

SRC_2945_DOC = ROOT / "2945-Y5-R2FR-source-normalized-stationary-q_loc-current-scale-or-denominator-blocker-under-AX1090.md"
SRC_2945_DENOM = RESIDUALS / "P8_Y5_R2FR_2945_DENOMINATOR_BLOCKER_ROWS.csv"
SRC_2945_SCALE = RESIDUALS / "P8_Y5_R2FR_2945_SOURCE_SCALE_RESIDUAL_ROWS.csv"
SRC_2945_NEXT = RESIDUALS / "P8_Y5_R2FR_2945_NEXT_TARGET.csv"
SRC_2945_STATIONARY = RESIDUALS / "P8_Y5_R2FR_2945_STATIONARY_COLLAR_DERIVATION_ATTEMPT.csv"
SRC_2339_MHREF = RESIDUALS / "P8_Y5_PARENT_QLOC_2339_MHREF_FIRST_ROW.csv"
SRC_1518_MHREF = RESIDUALS / "P8_Y5_PARENT_PIM_1518_MHREF_SURFACE_LOCK.csv"
SRC_1774_MHREF_GATE = RESIDUALS / "P8_Y5_PARENT_QLOC_1774_MHREF_DENOMINATOR_GATE.csv"
SRC_2938_REFLOCK = RESIDUALS / "P8_Y5_R2FR_2938_MHREF_ELLJ_REFERENCE_LOCK_CONTRACT.csv"
SRC_2938_WORLD = RESIDUALS / "P8_Y5_R2FR_2938_HTAU_WORLDTUBE_SOURCE_MEASURE_THEOREM_ATTEMPT.csv"
SRC_WORLD_THEOREM = RESIDUALS / "P8_WORLDTUBE_SOURCE_MEASURE_THEOREM.csv"
SRC_PIM_FLUX = RESIDUALS / "P8_PiM_flux_closure_Ward_topological_CONTRACT.csv"
SRC_PIM_ALGEBRA = RESIDUALS / "P8_PiM_parent_symplectic_projector_algebra_CONTRACT.csv"
SRC_KAPPA_CONTRACT = RESIDUALS / "P8_constant_universal_Geff_kappa_CONTRACT.csv"
SRC_KAPPA_SUPER = RESIDUALS / "P8_CONSTANT_KAPPA_SUPERSELECTION_THEOREM.csv"
SRC_2932_KAPPA_ELLJ = RESIDUALS / "P8_Y5_R2FR_2932_KAPPA_ELLJ_CONSTANT_PROOF_AUDIT.csv"
SRC_2934_ELLJ = RESIDUALS / "P8_Y5_R2FR_2934_ELLJ_OWNER_SOURCE_CURRENT_AUDIT.csv"
SRC_2577_SELECTOR = RESIDUALS / "P8_Y5_SOURCE_SELECTOR_COUPLING_2577_RESIDUAL_INPUT_LEDGER.csv"
SRC_2615_ZERO = RESIDUALS / "P8_Y5_TOTAL_HILBERT_SOURCE_GATE_2615_SOURCE_ZERO_STATUS.csv"

OUTPUTS = {
    "sources": RESIDUALS / "P8_Y5_R2FR_2946_SOURCE_REGISTER.csv",
    "theorem": RESIDUALS / "P8_Y5_R2FR_2946_DENOMINATOR_PACKAGE_THEOREM_ATTEMPT.csv",
    "schemas": RESIDUALS / "P8_Y5_R2FR_2946_FIRST_ROW_ACQUISITION_SCHEMAS.csv",
    "envelope": RESIDUALS / "P8_Y5_R2FR_2946_DENOMINATOR_RESIDUAL_ENVELOPE.csv",
    "anti_circularity": RESIDUALS / "P8_Y5_R2FR_2946_ANTI_CIRCULARITY_GUARDS.csv",
    "arenas": RESIDUALS / "P8_Y5_R2FR_2946_ARENA_READINESS_GATE.csv",
    "claims": RESIDUALS / "P8_Y5_R2FR_2946_CLAIM_GATES.csv",
    "decision": RESIDUALS / "P8_Y5_R2FR_2946_DECISION_LEDGER.csv",
    "next": RESIDUALS / "P8_Y5_R2FR_2946_NEXT_TARGET.csv",
    "branches": RESIDUALS / "P8_Y5_R2FR_2946_BRANCH_COPIES.csv",
    "validation": RESIDUALS / "P8_Y5_BRR545_2946_VALIDATION.csv",
}

BRANCH_OUTPUTS = {
    "theorem_copy": PARENT_ACTION / "MHref_PiM_denominator_package_theorem_attempt_2946_NONCLAIM.csv",
    "schema_copy": LOCAL_BOUNDS / "MHref_PiM_denominator_first_row_schemas_2946_NONCLAIM.csv",
    "envelope_copy": LOCAL_BOUNDS / "MHref_PiM_denominator_residual_envelope_2946_NONCLAIM.csv",
    "anti_circularity_copy": LOCAL_BOUNDS / "MHref_PiM_anti_circularity_guards_2946_NONCLAIM.csv",
    "next_copy": RAB_QUEUE / "JR2946_THETA_QTAU_MHREF_DENOMINATOR_NEXT_NONCLAIM.csv",
}

for directory in {path.parent for path in OUTPUTS.values()} | {path.parent for path in BRANCH_OUTPUTS.values()} | {DOC.parent}:
    directory.mkdir(parents=True, exist_ok=True)


def read_text(path: Path) -> str:
    if not path.exists():
        return ""
    return path.read_text(encoding="utf-8", errors="replace")


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


def is_under(path: Path, parent: Path) -> bool:
    try:
        path.resolve().relative_to(parent.resolve())
        return True
    except ValueError:
        return False


def md_escape(value: Any) -> str:
    return str(value).replace("|", "\\|").replace("\n", "<br>")


def md_table(rows: list[dict[str, Any]], columns: list[str] | None = None) -> str:
    if not rows:
        return "_No rows._"
    selected = columns or list(rows[0].keys())
    header = "| " + " | ".join(selected) + " |"
    separator = "| " + " | ".join("---" for _ in selected) + " |"
    body = ["| " + " | ".join(md_escape(row.get(column, "")) for column in selected) + " |" for row in rows]
    return "\n".join([header, separator, *body])


def source_register_rows() -> list[dict[str, Any]]:
    specs = [
        ("SRC2946_00_2945_doc", SRC_2945_DOC, "NEXT2945_0_2946;Validation overall: `True`", "2945 handoff to denominator package"),
        ("SRC2946_01_2945_denom", SRC_2945_DENOM, "DEN2945_0_MHref_value;DEN2945_7_selector_shadow", "denominator blocker rows"),
        ("SRC2946_02_2945_scale", SRC_2945_SCALE, "SSR2945_1_DellJ;SSR2945_4_side_flux", "source-scale residual rows"),
        ("SRC2946_03_2945_next", SRC_2945_NEXT, "NEXT2945_0_2946", "machine-readable 2946 target"),
        ("SRC2946_04_2945_stationary", SRC_2945_STATIONARY, "ST2945_4_source_normalization;ST2945_5_verdict", "stationary route denominator failure"),
        ("SRC2946_05_2339_mhref", SRC_2339_MHREF, "MHR2339_0_first_row;MHR2339_3_zero_switch", "M_H_ref first-row schema"),
        ("SRC2946_06_1518_mhref", SRC_1518_MHREF, "MH1518_0_M_H_ref;MH1518_7_acceptance", "M_H_ref surface lock"),
        ("SRC2946_07_1774_gate", SRC_1774_MHREF_GATE, "MHG1774_0_definition;MHG1774_4_verdict", "denominator acceptance gate"),
        ("SRC2946_08_2938_reflock", SRC_2938_REFLOCK, "REF2938_0_MHref_definition;REF2938_4_no_laundering", "reference/ellJ lock contract"),
        ("SRC2946_09_2938_world", SRC_2938_WORLD, "HWS2938_0_master_identity;HWS2938_6_verdict", "Hamiltonian worldtube source measure attempt"),
        ("SRC2946_10_world_theorem", SRC_WORLD_THEOREM, "T510_1_worldtube_source_measure;T510_3_Newton_PPN_readout", "worldtube source measure conditional theorem"),
        ("SRC2946_11_pim_flux", SRC_PIM_FLUX, "FC1_stationary_or_Hamiltonian_time_generator;FC7_absolute_calibration_after_closure", "Pi_M flux closure contract"),
        ("SRC2946_12_pim_algebra", SRC_PIM_ALGEBRA, "PM5_projector_variation_owned;PM7_absolute_calibration_deferred", "Pi_M algebra and calibration"),
        ("SRC2946_13_kappa_contract", SRC_KAPPA_CONTRACT, "CU1_global_coupling_status;CU8_retained_residual_fallback", "constant kappa contract"),
        ("SRC2946_14_kappa_super", SRC_KAPPA_SUPER, "T508_0_global_sector;T508_2_no_residual_if_closed", "conditional kappa superselection theorem"),
        ("SRC2946_15_2932_kappa_ellj", SRC_2932_KAPPA_ELLJ, "KLC2932_0_kappa_route;KLC2932_6_verdict", "kappa/ellJ proof audit"),
        ("SRC2946_16_2934_ellj", SRC_2934_ELLJ, "EJO2934_0_definition;EJO2934_5_verdict", "ellJ owner audit"),
        ("SRC2946_17_2577_selector", SRC_2577_SELECTOR, "SRR2577_0_W_selector;SRR2577_6_delta_ellJ", "source selector/coupling residuals"),
        ("SRC2946_18_2615_zero", SRC_2615_ZERO, "SZ2615_0_derivation_gain;SZ2615_6_next", "source-zero status"),
    ]
    rows: list[dict[str, Any]] = []
    for source_id, source_path, anchors, role in specs:
        found, missing = anchors_present(source_path, anchors)
        rows.append(
            add_common(
                {
                    "source_id": source_id,
                    "source_type": "local_file",
                    "source_path": str(source_path),
                    "anchors": anchors,
                    "role": role,
                    "path_exists": source_path.exists(),
                    "anchors_found": found,
                    "missing_anchors": missing,
                }
            )
        )
    return rows


def theorem_rows() -> list[dict[str, Any]]:
    rows = [
        ("THM2946_0_definition", "M_H_ref definition", "M_H_ref = H_tau[S_outer] - H_ref in same tau/coframe/source frame", "definition exists", "values and parent certificates missing", False),
        ("THM2946_1_theta_Qtau", "parent Noether charge", "theta_MTS and Q_tau_MTS extracted from a single parent variation with all sectors", "required first premise", "MISSING_PARENT_THETA_QTAU", False),
        ("THM2946_2_integrability_reference", "integrability and fixed reference", "delta H_tau is path-independent and H_ref is source-blind before readout", "conditional criterion exists", "INTEGRABILITY_BLOCKED_REFERENCE_UNSIGNED", False),
        ("THM2946_3_worldtube_measure", "worldtube source measure", "Hamiltonian source charge equals dressed worldtube Hilbert measure up to retained residuals", "exact conditional identity exists", "SOURCE_MEASURE_GLUE_NOT_DERIVED", False),
        ("THM2946_4_PiM_equality", "Pi_M J_H equality", "(4*pi*G_ref)^-1 int_S Pi_M J_H = M_H_ref on linked surfaces", "required denominator bridge", "MISSING_HILBERT_TO_HTAU_MAP", False),
        ("THM2946_5_coupling_scales", "kappa/ellJ/G_ref lock", "kappa and ell_J fixed before readout with no source/range/frame/domain labels", "kappa has conditional route; ellJ named", "KAPPA_NOT_ADOPTED_ELLJ_OWNER_OPEN", False),
        ("THM2946_6_anti_circularity", "no orbital-GM laundering", "orbital GM can test but cannot define M_H_ref, Pi_M, kappa or ell_J", "guardrail exact", "passes as guard only, not denominator proof", True),
        ("THM2946_7_verdict", "denominator package theorem", "all clauses close in one same-frame parent package", "attempted", "DENOMINATOR_PACKAGE_NOT_DERIVED", False),
    ]
    return [
        add_common(
            {
                "theorem_step_id": step_id,
                "clause": clause,
                "required_statement": required,
                "current_evidence": evidence,
                "blocking_gap": gap,
                "condition_passed": passed,
            }
        )
        for step_id, clause, required, evidence, gap, passed in rows
    ]


def schema_rows() -> list[dict[str, Any]]:
    rows = [
        ("SCHEMA2946_0_MHref_value", "M_H_ref", "system_id;tau_id;coframe_id;surface_outer;H_tau;H_tau_units;H_ref;H_ref_units;M_H_ref;M_H_ref_units;reference_rule;theta_Qtau_certificate;integrability_certificate;source_path;equation_ref;not_orbital_GM_imported;valid_for_claim", "MISSING_H_TAU;MISSING_H_REF;MISSING_M_H_REF", "positive same-frame parent source charge"),
        ("SCHEMA2946_1_theta_Qtau", "theta_MTS/Q_tau", "L_parent;sector_list;theta_MTS;Q_tau_MTS;boundary_terms;reference_terms;variation_variables;source_path;equation_ref;parent_signed;valid_for_claim", "MISSING_PARENT_THETA_QTAU", "single parent Noether charge certificate"),
        ("SCHEMA2946_2_integrability", "H_tau integrability", "omega_total;i_tau_omega;curl_delta_H_tau;reference_curl;projector_stress;boundary_flux;absolute_residual;source_path;valid_for_claim", "INTEGRABILITY_BLOCKED", "Hamiltonian path-independence or finite curl bound"),
        ("SCHEMA2946_3_Href_selector", "H_ref/Sigma_ref", "selector_equation;source_blind_derivative;topology_rule;stationarity_rule;no_GM_label;no_material_label;source_path;valid_for_claim", "REFERENCE_SELECTOR_UNSIGNED", "fixed source-blind reference"),
        ("SCHEMA2946_4_PiM_Hilbert", "Pi_M J_H", "PiM_definition;J_H_definition;linked_surface;homology_class;integral_value;normalization;M_H_ref_link;G_ref_link;source_path;valid_for_claim", "MISSING_HILBERT_TO_HTAU_MAP", "same-frame Hilbert/Hamiltonian equality"),
        ("SCHEMA2946_5_kappa", "kappa_MTS/G_ref", "parent_sector;global_or_topological_certificate;D_t_kappa;D_A_kappa;D_lambda_kappa;frame_blind;source_blind;G_ref_match;source_path;valid_for_claim", "KAPPA_ROUTE_CONDITIONAL_NOT_ADOPTED", "constant universal coupling"),
        ("SCHEMA2946_6_ellJ", "ell_J", "source_current_owner;ell_J_definition;D_t_ellJ;D_A_ellJ;D_lambda_ellJ;not_absorbed_into_MHref;not_absorbed_into_GM;source_path;valid_for_claim", "SOURCE_SCALE_OWNER_OPEN", "source-current scale lock"),
        ("SCHEMA2946_7_worldtube_selector", "W_source/source-shadow", "W_source_definition;support_lock;same_frame_JH;connected_exchange_graph;source_shadow_absent;nonHilbert_bypass_absent;source_path;valid_for_claim", "SOURCE_SHADOW_NOT_EXCLUDED", "source selector/source-shadow ban"),
        ("SCHEMA2946_8_side_flux", "side/boundary/projector flux", "annulus_id;side_flux;B_zero_flux;projector_commutator;PiM_chainmap;units;normalization_by_MHref;source_path;valid_for_claim", "MISSING_FLUX_ZERO_OR_BOUND", "no compact exterior leakage"),
    ]
    return [
        add_common(
            {
                "schema_id": schema_id,
                "quantity": quantity,
                "required_columns": columns,
                "current_status": status,
                "acceptance_condition": acceptance,
            }
        )
        for schema_id, quantity, columns, status, acceptance in rows
    ]


def envelope_rows() -> list[dict[str, Any]]:
    rows = [
        ("ENV2946_0_denominator_total", "epsilon_denominator_abs", "abs(epsilon_MHref)+abs(epsilon_PiM)+abs(delta_kappa)+abs(delta_ellJ)+abs(epsilon_selector)+abs(epsilon_flux)+abs(epsilon_calibration)", "NO_CANCELLATION_ENVELOPE", "all arenas"),
        ("ENV2946_1_MHref", "epsilon_MHref", "absolute residual from missing/uncertain H_tau-H_ref denominator", "MISSING_FIRST_ROW", "Newton;R10;PPN;clock;orbital"),
        ("ENV2946_2_PiM", "epsilon_PiM", "failure of Pi_M J_H to equal Hamiltonian/worldtube source charge", "MISSING_EQUALITY_OR_BOUND", "Newton;R10;PPN;WEP"),
        ("ENV2946_3_kappa", "delta_kappa", "Dln(kappa_MTS) or same-frame coupling mismatch", "CONDITIONAL_ROUTE_NOT_ADOPTED", "Newton;R10;PPN;clock;orbital"),
        ("ENV2946_4_ellJ", "delta_ellJ", "Dln(ell_J) or source-current normalization mismatch", "SOURCE_SCALE_OWNER_OPEN", "Newton;R10;PPN;clock;orbital;WEP"),
        ("ENV2946_5_selector_shadow", "epsilon_selector_shadow", "source selector/source-shadow/non-Hilbert bypass residual", "SOURCE_SHADOW_NOT_EXCLUDED", "WEP;R10;Newton;PPN"),
        ("ENV2946_6_flux", "epsilon_flux", "side/boundary/projector compact exterior flux over M_H_ref", "MISSING_FLUX_ZERO_OR_BOUND", "Newton;PPN;orbital"),
    ]
    return [
        add_common(
            {
                "envelope_id": envelope_id,
                "residual": residual,
                "definition": definition,
                "status": status,
                "arenas": arenas,
            }
        )
        for envelope_id, residual, definition, status, arenas in rows
    ]


def anti_circularity_rows() -> list[dict[str, Any]]:
    rows = [
        ("AC2946_0_orbital_GM", "measured orbital GM cannot define M_H_ref", "M_H_ref must precede Poisson/orbital readout", True),
        ("AC2946_1_bare_mass", "bare rest mass cannot replace dressed Hamiltonian source charge", "binding/boundary/field dressing may be part of source charge", True),
        ("AC2946_2_EH_import", "EH-only Q_tau cannot be imported as MTS Q_tau", "all retained MTS sectors must be included or bounded", True),
        ("AC2946_3_reference_laundering", "H_ref cannot absorb source/coupling residuals", "reference selector must be source-blind and fixed before readout", True),
        ("AC2946_4_constant_calibration", "a common constant can be calibration only after derivatives and source labels vanish", "do not absorb range/time/species/frame dependence", True),
    ]
    return [
        add_common(
            {
                "guard_id": guard_id,
                "guard": guard,
                "reason": reason,
                "guard_passed": passed,
            }
        )
        for guard_id, guard, reason, passed in rows
    ]


def arena_rows() -> list[dict[str, Any]]:
    rows = [
        ("AR2946_0_Newton", "Newton/Poisson", "M_H_ref, Pi_M equality, kappa/G_ref, no compact flux", "BLOCKED_DENOMINATOR"),
        ("AR2946_1_R10", "R10 alpha(lambda)", "same denominator, ell_J/source selector, lambda source map", "BLOCKED_SOURCE_SCALE"),
        ("AR2946_2_PPN", "PPN gamma beta alpha_i", "same source charge plus Pi_M/projector/flux silence", "BLOCKED_PIM_AND_FLUX"),
        ("AR2946_3_clocks", "clock tests", "tau frame, kappa drift and ell_J drift fixed before readout", "BLOCKED_SCALE_DRIFT"),
        ("AR2946_4_orbital", "orbital systems", "parent source mass before downstream orbital GM comparison", "BLOCKED_ANTI_CIRCULARITY"),
        ("AR2946_5_WEP", "WEP/source composition", "no source-shadow and connected ordinary matter exchange graph", "BLOCKED_SOURCE_SHADOW"),
    ]
    return [
        add_common(
            {
                "arena_id": arena_id,
                "arena": arena,
                "needed_denominator_package": needed,
                "status": status,
            }
        )
        for arena_id, arena, needed, status in rows
    ]


def claim_rows() -> list[dict[str, Any]]:
    rows = [
        ("CG2946_0_denominator_theorem", "M_H_ref/Pi_M denominator package derived", False, "DENOMINATOR_PACKAGE_NOT_DERIVED", False),
        ("CG2946_1_first_rows_claim_ready", "first-row schemas are valid prediction rows", False, "SCHEMAS_ONLY_VALUES_MISSING", False),
        ("CG2946_2_source_scale_zero", "kappa/ellJ/source selector residuals vanish", False, "SOURCE_SCALE_OWNER_OPEN", False),
        ("CG2946_3_q_loc_score_ready", "source-normalized q_loc bound score-ready", False, "DENOMINATOR_AND_NUMERATORS_OPEN", False),
        ("CG2946_4_Newton_GR", "Newton/local-GR reduction derived", False, "NO_DENOMINATOR_PACKAGE", False),
        ("CG2946_5_public_claim", "public claim allowed from 2946", False, "PRIVATE_NONCLAIM_CHECKPOINT", False),
    ]
    return [
        add_common(
            {
                "claim_gate_id": gate_id,
                "claim": claim,
                "condition_passed": passed,
                "status": status,
                "claim_allowed": allowed,
            }
        )
        for gate_id, claim, passed, status, allowed in rows
    ]


def decision_rows() -> list[dict[str, Any]]:
    rows = [
        ("DEC2946_0_theorem_failed", "denominator package theorem not closed", "theta/Qtau, H_tau, H_ref, Pi_M equality, kappa, ellJ and selector clauses are not signed together", "do not claim local-GR or source-normalized q_loc"),
        ("DEC2946_1_schema_success", "first-row schemas are now explicit", "every denominator component has required columns and acceptance condition", "use schemas for 2947 acquisition/certificate work"),
        ("DEC2946_2_earliest_root", "theta_MTS/Q_tau extraction is the first formal root", "without parent charge, M_H_ref and Pi_M equality cannot be theorem-grade", "attack theta/Qtau certificate next"),
        ("DEC2946_3_parallel_root", "ell_J/kappa/source-shadow remain parallel roots", "even a Hamiltonian charge cannot score local arenas if source scale can drift or hide", "carry residual envelope"),
        ("DEC2946_4_guardrail", "anti-circularity guard remains hard", "measured orbital GM is downstream evidence only", "refuse laundering shortcuts"),
    ]
    return [
        add_common(
            {
                "decision_id": decision_id,
                "decision": decision,
                "reason": reason,
                "next_action": next_action,
            }
        )
        for decision_id, decision, reason, next_action in rows
    ]


def next_rows() -> list[dict[str, Any]]:
    return [
        add_common(
            {
                "next_id": "NEXT2946_0_2947",
                "priority": "selected_primary",
                "next_doc": "2947-Y5-R2FR-parent-theta-Qtau-MHref-certificate-or-denominator-first-row-runner-under-AX1090.md",
                "next_script": "scripts/Y5_R2FR_parent_theta_Qtau_MHref_certificate_or_denominator_first_row_runner_under_AX1090_2947.py",
                "objective": "Attack the earliest formal denominator root: try to extract or certify parent theta_MTS and Q_tau_MTS for the current parent spine, including boundary/reference/projector/extra sectors. If it cannot close, instantiate the M_H_ref/Pi_M denominator first-row runner with explicit missing certificates.",
                "include": "theta_MTS;Q_tau_MTS;H_tau;H_ref;integrability;Pi_M J_H;boundary terms;projector stress;extra-sector silence;anti-circularity",
                "exclude": "EH-only charge import; measured orbital GM denominator; Gamma zero axiom; public claim; GitHub action; formalization-workbench edits",
            }
        )
    ]


def branch_rows() -> list[dict[str, Any]]:
    copies = [
        ("theorem_copy", OUTPUTS["theorem"], BRANCH_OUTPUTS["theorem_copy"]),
        ("schema_copy", OUTPUTS["schemas"], BRANCH_OUTPUTS["schema_copy"]),
        ("envelope_copy", OUTPUTS["envelope"], BRANCH_OUTPUTS["envelope_copy"]),
        ("anti_circularity_copy", OUTPUTS["anti_circularity"], BRANCH_OUTPUTS["anti_circularity_copy"]),
        ("next_copy", OUTPUTS["next"], BRANCH_OUTPUTS["next_copy"]),
    ]
    rows: list[dict[str, Any]] = []
    for copy_id, source_path, copy_path in copies:
        if source_path.exists():
            shutil.copyfile(source_path, copy_path)
        rows.append(
            add_common(
                {
                    "copy_id": copy_id,
                    "source_path": str(source_path),
                    "copy_path": str(copy_path),
                    "source_exists": source_path.exists(),
                    "copy_exists": copy_path.exists(),
                }
            )
        )
    return rows


def validation_rows(source_rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    generated_csvs = [path for key, path in OUTPUTS.items() if key != "validation"]
    formalization_has_2946 = False
    if FORMALIZATION.exists():
        formalization_has_2946 = any(FORMALIZATION.rglob("*2946*"))
    theorem = read_csv_rows(OUTPUTS["theorem"])
    schemas = read_csv_rows(OUTPUTS["schemas"])
    guards = read_csv_rows(OUTPUTS["anti_circularity"])
    claims = read_csv_rows(OUTPUTS["claims"])
    next_target = read_csv_rows(OUTPUTS["next"])
    checks = [
        ("VAL2946_0_sources_exist", all(row["path_exists"] for row in source_rows), "all cited local source paths exist", True),
        ("VAL2946_1_anchors_found", all(row["anchors_found"] for row in source_rows), "all source anchors found", True),
        ("VAL2946_2_theorem_attempted", any(row.get("theorem_step_id") == "THM2946_7_verdict" for row in theorem), "denominator theorem verdict row exists", True),
        ("VAL2946_3_theorem_not_claimed", any(row.get("theorem_step_id") == "THM2946_7_verdict" and row.get("condition_passed") == "False" for row in theorem), "denominator theorem remains nonclaim", True),
        ("VAL2946_4_schemas_emitted", len(schemas) >= 9, "first-row acquisition schemas emitted", True),
        ("VAL2946_5_anti_circularity_passed", all(row.get("guard_passed") == "True" for row in guards), "anti-circularity guards pass", True),
        ("VAL2946_6_claims_blocked", all(row.get("claim_allowed") == "False" for row in claims), "all claims blocked", True),
        ("VAL2946_7_next_target_selected", any(row.get("next_id") == "NEXT2946_0_2947" for row in next_target), "2947 theta/Qtau denominator target selected", True),
        ("VAL2946_8_branches_exist", all(path.exists() for path in BRANCH_OUTPUTS.values()), "branch copy files exist", True),
        ("VAL2946_9_csvs_parse", all(csv_parses(path) for path in generated_csvs), "all generated CSV files parse", True),
        ("VAL2946_10_outputs_under_post_checkpoint", all(is_under(path, ROOT) for path in [DOC, *OUTPUTS.values(), *BRANCH_OUTPUTS.values()]), "all generated outputs are under post-checkpoint-work", True),
        ("VAL2946_11_formalization_clean", not formalization_has_2946, "no 2946 outputs were written to formalization-workbench", True),
    ]
    overall = all(passed == required for _, passed, _, required in checks)
    rows = [{"validation_id": validation_id, "passed": passed, "check": check, "required": required} for validation_id, passed, check, required in checks]
    rows.append({"validation_id": "VAL2946_OVERALL", "passed": overall, "check": "2946 validation overall", "required": True})
    return rows


def write_doc(
    source_rows: list[dict[str, Any]],
    theorem: list[dict[str, Any]],
    schemas: list[dict[str, Any]],
    envelope: list[dict[str, Any]],
    guards: list[dict[str, Any]],
    arenas: list[dict[str, Any]],
    claims: list[dict[str, Any]],
    decisions: list[dict[str, Any]],
    next_target: list[dict[str, Any]],
    branches: list[dict[str, Any]],
    validation: list[dict[str, Any]],
) -> None:
    overall = next(row for row in validation if row["validation_id"] == "VAL2946_OVERALL")["passed"]
    text = f"""# 2946 - Y5 R2FR: MHref/PiM denominator package theorem or first source row under AX1090

Status: `Y5_R2FR_2946_denominator_package_theorem_not_closed_first_row_schemas_emitted`

Claim ceiling: `no_source_normalized_q_loc_bound_no_Newton_no_local_GR_no_R10_no_PPN_no_public_claim`

2946 tries to close the denominator package instead of merely naming it. The required bridge is:

`M_H_ref = H_tau[S_outer] - H_ref`

with `theta_MTS`, `Q_tau_MTS`, `Pi_M J_H`, `G_ref`, `kappa`, `ell_J`, source selector, reference, boundary and projector terms all fixed in the same parent frame before readout.

The theorem does not close in the current corpus. The anti-circularity guard is strong, but it is only a guard: it refuses orbital-GM laundering without supplying `H_tau`, `H_ref` or `Pi_M J_H`. The useful output is therefore a first-row acquisition schema for every denominator component and a no-cancellation residual envelope.

## Source Register

{md_table(source_rows, ["source_id", "source_path", "path_exists", "anchors_found", "role"])}

## Denominator Package Theorem Attempt

{md_table(theorem, ["theorem_step_id", "clause", "required_statement", "current_evidence", "blocking_gap", "condition_passed"])}

## First-Row Acquisition Schemas

{md_table(schemas, ["schema_id", "quantity", "required_columns", "current_status", "acceptance_condition"])}

## Denominator Residual Envelope

{md_table(envelope, ["envelope_id", "residual", "definition", "status", "arenas"])}

## Anti-Circularity Guards

{md_table(guards, ["guard_id", "guard", "reason", "guard_passed"])}

## Arena Readiness Gate

{md_table(arenas, ["arena_id", "arena", "needed_denominator_package", "status"])}

## Claim Gates

{md_table(claims, ["claim_gate_id", "claim", "condition_passed", "status", "claim_allowed"])}

## Decision Ledger

{md_table(decisions, ["decision_id", "decision", "reason", "next_action"])}

## Next Target

{md_table(next_target, ["next_id", "priority", "next_doc", "next_script", "objective", "exclude"])}

## Branch Copies

{md_table(branches, ["copy_id", "source_path", "copy_path", "source_exists", "copy_exists", "valid_for_claim"])}

## Validation

{md_table(validation, ["validation_id", "passed", "check", "required"])}

Validation overall: `{overall}`.
"""
    DOC.write_text(text, encoding="utf-8")


def main() -> None:
    source_rows = source_register_rows()
    write_csv(OUTPUTS["sources"], source_rows)

    theorem = theorem_rows()
    schemas = schema_rows()
    envelope = envelope_rows()
    guards = anti_circularity_rows()
    arenas = arena_rows()
    claims = claim_rows()
    decisions = decision_rows()
    next_target = next_rows()

    write_csv(OUTPUTS["theorem"], theorem)
    write_csv(OUTPUTS["schemas"], schemas)
    write_csv(OUTPUTS["envelope"], envelope)
    write_csv(OUTPUTS["anti_circularity"], guards)
    write_csv(OUTPUTS["arenas"], arenas)
    write_csv(OUTPUTS["claims"], claims)
    write_csv(OUTPUTS["decision"], decisions)
    write_csv(OUTPUTS["next"], next_target)

    branches = branch_rows()
    write_csv(OUTPUTS["branches"], branches)

    validation = validation_rows(source_rows)
    write_csv(OUTPUTS["validation"], validation)

    write_doc(source_rows, theorem, schemas, envelope, guards, arenas, claims, decisions, next_target, branches, validation)

    overall = next(row for row in validation if row["validation_id"] == "VAL2946_OVERALL")["passed"]
    print(f"2946 validation overall: {overall}")
    print(DOC)


if __name__ == "__main__":
    main()

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
SOURCE_WEIGHT = ROOT / "source-intake" / "source-weight"
RAB_QUEUE = ROOT / "source-intake" / "rab-sector" / "acquisition-queue"
BETA_DOCS = ROOT / "source-intake" / "beta-source" / "docs"
FORMALIZATION = PROJECT / "formalization-workbench"

BRANCH_ID = "MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428"

DOC = ROOT / "2881-Y5-R2FR-JR-matter-source-current-or-matter-descent-zero-under-AX1090.md"

SRC_2880_DOC = ROOT / "2880-Y5-R2FR-ZR-MR2-operator-normalization-or-range-source-row-under-AX1090.md"
SRC_2880_NEXT = RESIDUALS / "P8_Y5_R2FR_2880_NEXT_TARGET.csv"
SRC_2880_VALIDATION = RESIDUALS / "P8_Y5_BRR545_2880_VALIDATION.csv"
SRC_2880_QUEUE = RESIDUALS / "P8_Y5_R2FR_2880_OPERATOR_COEFFICIENT_ACQUISITION_QUEUE.csv"
SRC_2879_ZERO = RESIDUALS / "P8_Y5_R2FR_2879_SOURCE_ZERO_THEOREM_AUDIT.csv"
SRC_2879_DECOMP = RESIDUALS / "P8_Y5_R2FR_2879_SRZR_SOURCE_MAP_DECOMPOSITION.csv"
SRC_1625_BUILDER = RESIDUALS / "P8_Y5_PARENT_QLOC_1625_FINITE_ZR_PRIOR_ROW_BUILDER.csv"

SRC_2356_DESCENT = RESIDUALS / "P8_Y5_PARENT_QLOC_2356_SOURCE_CURRENT_DESCENT_THEOREM_AUDIT.csv"
SRC_2356_DOMAIN_ROWS = RESIDUALS / "P8_Y5_PARENT_QLOC_2356_DOMAIN_MOTION_BOUND_ROWS.csv"
SRC_2419_CHAINMAP = RESIDUALS / "P8_Y5_PARENT_QLOC_2419_CHAINMAP_ZERO_GATE.csv"
SRC_2466_HILBERT = RESIDUALS / "P8_Y5_SOURCE_BRIDGE_2466_HILBERT_CURRENT_DESCENT.csv"
SRC_2525_WORLDTUBE = RESIDUALS / "P8_Y5_NO_SHADOW_2525_WORLDTUBE_DESCENT_AUDIT.csv"
SRC_2525_GATE = RESIDUALS / "P8_Y5_NO_SHADOW_2525_FIXED_DOMAIN_GATE.csv"
SRC_2525_DRYRUN = RESIDUALS / "P8_Y5_NO_SHADOW_2525_DRYRUN_RESULTS.csv"
SRC_2525_DOMAIN_ROWS = RESIDUALS / "P8_Y5_NO_SHADOW_2525_JDOMAIN_BOUND_ROWS.csv"
SRC_2526_COUPLING = RESIDUALS / "P8_Y5_NO_SHADOW_2526_MINIMAL_COUPLING_ACTION_CANDIDATE.csv"
SRC_2526_TESTS = RESIDUALS / "P8_Y5_NO_SHADOW_2526_ACTION_SIGNING_TESTS.csv"
SRC_2526_GATES = RESIDUALS / "P8_Y5_NO_SHADOW_2526_CLAIM_GATES.csv"
SRC_2526_COUNTER = RESIDUALS / "P8_Y5_NO_SHADOW_2526_COUNTERMODEL_TESTS.csv"
SRC_2526_DRYRUN = RESIDUALS / "P8_Y5_NO_SHADOW_2526_DRYRUN_RESULTS.csv"
SRC_2526_DECISION = RESIDUALS / "P8_Y5_NO_SHADOW_2526_DECISION_LEDGER.csv"
SRC_CURRENT_CONTRACT = RESIDUALS / "P8_source_current_Ward_universality_CONTRACT.csv"
SRC_OWNER_CONTRACT = RESIDUALS / "P8_source_owner_parent_action_terms_CONTRACT.csv"
SRC_CONSTANT_CONTRACT = RESIDUALS / "P8_constant_sector_universality_CONTRACT.csv"

OUTPUTS = {
    "sources": RESIDUALS / "P8_Y5_R2FR_2881_SOURCE_REGISTER.csv",
    "normal_form": RESIDUALS / "P8_Y5_R2FR_2881_JR_DESCENT_NORMAL_FORM.csv",
    "zero_audit": RESIDUALS / "P8_Y5_R2FR_2881_JR_ZERO_GATE_AUDIT.csv",
    "countermodels": RESIDUALS / "P8_Y5_R2FR_2881_JR_COUNTERMODEL_LEDGER.csv",
    "fill": RESIDUALS / "P8_Y5_R2FR_2881_JR_FILL_ATTEMPT.csv",
    "queue": RESIDUALS / "P8_Y5_R2FR_2881_SOURCE_CURRENT_ACQUISITION_QUEUE.csv",
    "gates": RESIDUALS / "P8_Y5_R2FR_2881_ACCEPTANCE_GATES.csv",
    "runner": RESIDUALS / "P8_Y5_R2FR_2881_RUNNER_STATUS.csv",
    "decision": RESIDUALS / "P8_Y5_R2FR_2881_DECISION_LEDGER.csv",
    "next": RESIDUALS / "P8_Y5_R2FR_2881_NEXT_TARGET.csv",
    "branches": RESIDUALS / "P8_Y5_R2FR_2881_BRANCH_COPIES.csv",
    "validation": RESIDUALS / "P8_Y5_BRR545_2881_VALIDATION.csv",
}

BRANCH_OUTPUTS = {
    "normal_form_copy": LOCAL_BOUNDS / "RAB_JR_DESCENT_NORMAL_FORM_2881_NONCLAIM.csv",
    "zero_audit_copy": SOURCE_WEIGHT / "RAB_JR_ZERO_GATE_AUDIT_2881_NONCLAIM.csv",
    "fill_copy": BETA_DOCS / "RAB_JR_FILL_ATTEMPT_2881_NONCLAIM.csv",
    "next_queue": RAB_QUEUE / "JR2881_q_object_vertical_generator_certificate_NEXT.csv",
}


for directory in {path.parent for path in OUTPUTS.values()} | {path.parent for path in BRANCH_OUTPUTS.values()} | {DOC.parent}:
    directory.mkdir(parents=True, exist_ok=True)


def now() -> str:
    return datetime.now(timezone.utc).isoformat()


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
            "control_only": True,
            "score_ready": False,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
            "generated_utc": now(),
        }
    )
    return row


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fieldnames: list[str] = []
    for row in rows:
        for key in row:
            if key not in fieldnames:
                fieldnames.append(key)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def csv_parses(path: Path) -> bool:
    try:
        with path.open(newline="", encoding="utf-8") as handle:
            list(csv.DictReader(handle))
        return True
    except Exception:
        return False


def source_register_rows() -> list[dict[str, Any]]:
    specs = [
        ("SRC2881_0_2880_doc", SRC_2880_DOC, "Status: `Y5_R2FR_2880_operator_range_law_installed_ZR_MR2_ellR_not_filled_JR_2881_next`;J_R", "2880 handoff doc"),
        ("SRC2881_1_2880_next", SRC_2880_NEXT, "NEXT2880_0_2881", "2880 selected this target"),
        ("SRC2881_2_2880_validation", SRC_2880_VALIDATION, "VAL2880_OVERALL", "2880 validation"),
        ("SRC2881_3_2880_queue", SRC_2880_QUEUE, "Q2880_4_JR", "J_R selected source-current queue row"),
        ("SRC2881_4_2879_zero", SRC_2879_ZERO, "ZERO2879_0_JR_matter_silence", "J_R zero theorem previously unsigned"),
        ("SRC2881_5_2879_decomp", SRC_2879_DECOMP, "MAP2879_1_matter_current", "J_R/Z_R source-map component"),
        ("SRC2881_6_1625_builder", SRC_1625_BUILDER, "PB1625_2_JR", "older J_R source-current builder"),
        ("SRC2881_7_2356_descent", SRC_2356_DESCENT, "SCD2356_0_chain_rule_identity;SCD2356_1_descent_theorem;SCD2356_6_current_corpus_verdict", "exact conditional source-current theorem"),
        ("SRC2881_8_2356_rows", SRC_2356_DOMAIN_ROWS, "DMB2356_0_total;DMB2356_1_J_qdesc;DMB2356_4_J_slot", "fallback finite source-current rows"),
        ("SRC2881_9_2419_chainmap", SRC_2419_CHAINMAP, "CMG2419_4_source_descent;CMG2419_6_verdict", "source descent blocks chain-map zero"),
        ("SRC2881_10_2466_hilbert", SRC_2466_HILBERT, "HIL2466_0_define_T;HIL2466_1_define_current;HIL2466_2_parent_scale", "Hilbert current candidate and scale blocker"),
        ("SRC2881_11_2525_worldtube", SRC_2525_WORLDTUBE, "WTD2525_2_source_current_descent;WTD2525_8_verdict", "worldtube/source-current descent audit"),
        ("SRC2881_12_2525_gate", SRC_2525_GATE, "FDG2525_0_parent_q;FDG2525_1_vertical_generator;FDG2525_2_JH_descent;FDG2525_10_theorem", "fixed-domain gate blockers"),
        ("SRC2881_13_2525_dryrun", SRC_2525_DRYRUN, "DRY2525_1_noether_only;DRY2525_4_observed_GM_backfill", "shortcut rejection"),
        ("SRC2881_14_2525_domain_rows", SRC_2525_DOMAIN_ROWS, "JDOM2525_1_current_descent;JDOM2525_7_current_escape", "nonclaim current/domain rows"),
        ("SRC2881_15_2526_coupling", SRC_2526_COUPLING, "MCA2526_2_minimal_matter_terms;MCA2526_6_descent_output;MCA2526_7_current_verdict", "minimal coupling candidate"),
        ("SRC2881_16_2526_tests", SRC_2526_TESTS, "AST2526_0_q_object;AST2526_1_vertical_generator;AST2526_9_adoption", "action signing tests"),
        ("SRC2881_17_2526_gates", SRC_2526_GATES, "CG2526_1_source_current_descent;CG2526_3_local_GR_Newton", "claim gates blocked"),
        ("SRC2881_18_2526_counter", SRC_2526_COUNTER, "CMT2526_0_species_weight;CMT2526_5_q_missing", "countermodel ledger"),
        ("SRC2881_19_2526_dryrun", SRC_2526_DRYRUN, "DRY2526_0_ansatz_as_derivation;DRY2526_1_minimal_coupling_hides_q", "candidate-action shortcut rejection"),
        ("SRC2881_20_2526_decision", SRC_2526_DECISION, "DEC2526_0_contract_status;DEC2526_2_next", "least-scrutiny coupling contract decision"),
        ("SRC2881_21_current_contract", SRC_CURRENT_CONTRACT, "SC1_Hilbert_source_definition;SC3_universal_kappa_coupling;SC4_no_nonHilbert_source_current", "source-current Ward contract"),
        ("SRC2881_22_owner_contract", SRC_OWNER_CONTRACT, "A1_source_owner_decomposition;A6_selector_blind_source_action", "source-owner action terms"),
        ("SRC2881_23_constant_contract", SRC_CONSTANT_CONTRACT, "C3_universal_source_variation;C6_measured_GM_absolute_calibration", "constant/source universality contract"),
    ]
    rows: list[dict[str, Any]] = []
    for source_id, path, anchors, role in specs:
        found, missing = anchors_present(path, anchors)
        rows.append(
            add_common(
                {
                    "source_id": source_id,
                    "source_path": str(path),
                    "anchors": anchors,
                    "role": role,
                    "path_exists": path.exists(),
                    "anchors_found": found,
                    "missing_anchors": missing,
                }
            )
        )
    return rows


def normal_form_rows() -> list[dict[str, Any]]:
    rows = [
        {
            "form_id": "JR2881_0_chain_rule",
            "statement": "For vertical v, delta_v S_matter=DSbar[Dq(v)]+E_psi delta_v psi+J_theta L_v theta+J_direct[v]+delta_v B.",
            "role": "turns source-current zero into checkable premises instead of vibes",
            "current_status": "EXACT_IDENTITY_OR_NORMAL_FORM",
            "source_path": str(SRC_2356_DESCENT),
            "source_anchor": "SCD2356_0_chain_rule_identity",
            "accepted_current_theorem": False,
            "parent_signed": False,
        },
        {
            "form_id": "JR2881_1_Hilbert_current",
            "statement": "T_H^{mu nu}=-(2/sqrt(-g))delta S_matter/delta g_mu_nu and J_M^nu=ell_J T_H^{nu rho} tau_rho define the least-circular source object if ell_J/tau are parent-owned.",
            "role": "defines the candidate ordinary matter source before readout",
            "current_status": "PASS_AS_CANDIDATE_CONTRACT_SCALE_UNSIGNED",
            "source_path": str(SRC_2466_HILBERT),
            "source_anchor": "HIL2466_1_define_current",
            "accepted_current_theorem": False,
            "parent_signed": False,
        },
        {
            "form_id": "JR2881_2_descent_theorem",
            "statement": "If S_matter factors through q and all vertical lifts are gauge/Euler/boundary-only, then J_v^matter=0 modulo owned boundary/gauge terms.",
            "role": "exact conditional route to J_R=0",
            "current_status": "EXACT_CONDITIONAL_THEOREM",
            "source_path": str(SRC_2356_DESCENT),
            "source_anchor": "SCD2356_1_descent_theorem",
            "accepted_current_theorem": False,
            "parent_signed": False,
        },
        {
            "form_id": "JR2881_3_minimal_coupling_candidate",
            "statement": "MCA2526 gives S_A[psi_A;q(Phi),theta_A], forbids source-only slots, and extracts T_H/J_H before readout.",
            "role": "least-scrutiny coupling contract if later adopted by parent action",
            "current_status": "CANDIDATE_CONTRACT_NOT_PARENT_DERIVED",
            "source_path": str(SRC_2526_COUPLING),
            "source_anchor": "MCA2526_2_minimal_matter_terms;MCA2526_6_descent_output",
            "accepted_current_theorem": False,
            "parent_signed": False,
        },
        {
            "form_id": "JR2881_4_current_corpus_verdict",
            "statement": "Current corpus has the exact conditional theorem and a clean candidate coupling grammar, but not the parent q object, open-branch verticality, action adoption, boundary/support, tau/ell_J or M_H_ref clauses.",
            "role": "prevents using the coupling theorem as a current-MTS claim",
            "current_status": "APPLICATION_BLOCKED_CURRENT_CORPUS",
            "source_path": str(SRC_2526_GATES),
            "source_anchor": "CG2526_1_source_current_descent",
            "accepted_current_theorem": False,
            "parent_signed": False,
        },
    ]
    return [add_common(row) for row in rows]


def zero_audit_rows() -> list[dict[str, Any]]:
    rows = [
        ("ZG2881_0_parent_q", "parent q object exists before matter/readout", "q: Phi_parent -> Q_obs is parent kinematics/action data", "BLOCKED_Q_OBJECT_NOT_PARENT_SIGNED", SRC_2525_GATE, "FDG2525_0_parent_q"),
        ("ZG2881_1_verticality", "local residual direction is quotient-vertical", "v in ker(Dq) on an open local branch", "BLOCKED_VERTICALITY_NOT_SIGNED", SRC_2525_GATE, "FDG2525_1_vertical_generator"),
        ("ZG2881_2_action_adoption", "minimal coupling action is derived from MTS core", "MCA2526 is unique/parent-adopted, not just a clean ansatz", "NOT_SIGNED_BY_CURRENT_CORPUS", SRC_2526_TESTS, "AST2526_9_adoption"),
        ("ZG2881_3_matter_factorization", "ordinary matter factors through q", "S_matter=Sbar[q(Phi),psi,theta]+dB", "CONDITIONALLY_SIGNED_BY_CANDIDATE_ONLY", SRC_2526_TESTS, "AST2526_2_matter_factorization"),
        ("ZG2881_4_matter_lift", "vertical matter lift is gauge/Euler/boundary-only", "E_psi delta_v psi vanishes or is owned", "PARTIAL_CONDITIONAL_SIGNING", SRC_2526_TESTS, "AST2526_3_matter_lift"),
        ("ZG2881_5_constants", "ordinary constants are fixed representation/superselection data", "L_v theta=0 for clock/EM/mass constants", "CONDITIONALLY_SIGNED_BY_CANDIDATE_ONLY", SRC_2526_TESTS, "AST2526_4_constants"),
        ("ZG2881_6_no_source_slot", "no source-only weights/current rescalings/shadow frames", "w_A(X), c_A(X), A_A(X)^2 g_obs and source markers are excluded by parent grammar", "CONTRACT_NOT_PARENT_UNIQUENESS", SRC_2526_DRYRUN, "DRY2526_2_no_source_slot_by_decree"),
        ("ZG2881_7_boundary_support", "boundary/support tail is zero/proper/q-owned or explicit", "delta_v B and support flux vanish or are finite rows", "MISSING_BOUNDARY_SUPPORT_SILENCE_OR_BOUND", SRC_2356_DOMAIN_ROWS, "DMB2356_5_J_boundary"),
        ("ZG2881_8_tau_ellJ_MHref", "tau, ell_J and M_H_ref are parent-owned before scoring", "source current denominator and clock/coframe scale are noncircular", "MISSING_PARENT_SCALE_AND_MHREF", SRC_2466_HILBERT, "HIL2466_2_parent_scale"),
        ("ZG2881_9_variation_before_readout", "current extracted before material projection/orbital calibration", "T_H and J_H are functional derivatives before arena readout", "CONDITIONALLY_SIGNED_BY_CANDIDATE_ONLY", SRC_2526_TESTS, "AST2526_6_variation_order"),
        ("ZG2881_10_no_escape_current", "no non-Hilbert source current escapes", "bulk/boundary/domain/memory/range/connection do not add unowned source current", "MISSING_EXTRA_CURRENT_SILENCE_OR_BOUND", SRC_2525_DOMAIN_ROWS, "JDOM2525_7_current_escape"),
        ("ZG2881_11_joint_JR_zero", "J_R=0 as current MTS theorem", "all clauses above close with source paths", "NOT_CLOSED", SRC_2879_ZERO, "ZERO2879_0_JR_matter_silence"),
    ]
    return [
        add_common(
            {
                "zero_gate_id": gate_id,
                "required_clause": clause,
                "formal_condition": condition,
                "current_status": status,
                "source_path": str(path),
                "source_anchor": anchor,
                "gate_pass": False,
                "theorem_zero": False,
                "parent_signed": False,
            }
        )
        for gate_id, clause, condition, status, path, anchor in rows
    ]


def countermodel_rows() -> list[dict[str, Any]]:
    rows = [
        ("CM2881_0_noether_shortcut", "dJ=0 or Noether conservation alone", "conserved wrong-object currents need not descend through q", "ACTIVE_GUARD", SRC_2525_DRYRUN, "DRY2525_1_noether_only"),
        ("CM2881_1_species_weight", "S_matter -> sum_A w_A(X) S_A", "creates source-only species/current weights", "EXCLUDED_ONLY_IF_PARENT_ADOPTS_MCA2526", SRC_2526_COUNTER, "CMT2526_0_species_weight"),
        ("CM2881_2_variable_constants", "theta_A(X) varies with MTS invariants", "creates clock/EM/mass source current", "EXCLUDED_ONLY_IF_SUPERSELECTION_DERIVED", SRC_2526_COUNTER, "CMT2526_1_variable_constants"),
        ("CM2881_3_shadow_frame", "ordinary matter sees A_A(X)^2 g_obs or disformal source-only frame", "creates frame/source current despite visible geometry", "EXCLUDED_ONLY_IF_PARENT_ADOPTS_MCA2526", SRC_2526_COUNTER, "CMT2526_2_shadow_frame"),
        ("CM2881_4_post_readout_selector", "material/readout projection after variation changes source current", "post-variation source masks can fake descent", "EXCLUDED_ONLY_IF_VARIATION_ORDER_PARENT_SIGNED", SRC_2526_COUNTER, "CMT2526_3_post_variation_selector"),
        ("CM2881_5_boundary_domain_marker", "support/domain/boundary marker shifts under v", "bulk descent can still leave boundary/source tail", "RETAINED_UNTIL_BOUNDARY_ROW_EXISTS", SRC_2526_COUNTER, "CMT2526_4_boundary_domain_marker"),
        ("CM2881_6_q_missing", "candidate coupling uses q that is not parent-derived", "minimal coupling cannot prove its own quotient map or verticality", "RETAINED_AS_NEXT_GEOMETRY_GATE", SRC_2526_COUNTER, "CMT2526_5_q_missing"),
        ("CM2881_7_GM_backfill", "observed orbital GM normalizes source current", "launders empirical readout into source denominator", "ACTIVE_GUARD", SRC_2526_DRYRUN, "DRY2526_4_observed_GM_normalization"),
    ]
    return [
        add_common(
            {
                "countermodel_id": countermodel_id,
                "countermodel": countermodel,
                "why_dangerous": danger,
                "current_status": status,
                "source_path": str(path),
                "source_anchor": anchor,
                "excluded_now": False,
                "claim_safe": False,
            }
        )
        for countermodel_id, countermodel, danger, status, path, anchor in rows
    ]


def fill_rows() -> list[dict[str, Any]]:
    rows = [
        {
            "fill_id": "FILL2881_0_JR_live_row_attempt",
            "quantity": "J_R",
            "candidate_formula": "bulk vertical matter/source current from delta_v S_matter",
            "candidate_value": "MISSING_J_R",
            "units": "MISSING_SOURCE_CURRENT_UNITS",
            "source_path": "MISSING_PARENT_MATTER_ACTION_PATH",
            "equation_anchor": "MISSING_JR_ANCHOR",
            "status": "FAILED_TO_FILL_FROM_CURRENT_CORPUS",
            "failure_mode": "conditional theorem exists, but q object, verticality, action adoption, constants, boundary/support, tau/ell_J and M_H_ref are not parent-signed together",
            "accepted_live_input": False,
            "parent_signed": False,
        },
        {
            "fill_id": "FILL2881_1_JR_zero_attempt",
            "quantity": "J_R=0",
            "candidate_formula": "Dq(v)=0 plus S_matter=Sbar[q(Phi),psi,theta]+dB plus owned lifts/boundary",
            "candidate_value": "THEOREM_ZERO_NOT_AVAILABLE_CURRENT_CORPUS",
            "units": "n/a",
            "source_path": "MISSING_JOINT_PARENT_DESCENT_THEOREM",
            "equation_anchor": "MISSING_ZERO_THEOREM_ANCHOR",
            "status": "SOURCE_ZERO_REJECTED_CURRENT_CORPUS",
            "failure_mode": "MCA2526 is a contract/ansatz, not a derived MTS parent action; q/v gate remains upstream",
            "accepted_live_input": False,
            "parent_signed": False,
        },
        {
            "fill_id": "FILL2881_2_JR_finite_fallback",
            "quantity": "finite J_R residual pack",
            "candidate_formula": "epsilon_source_domain_motion_abs=abs(J_qdesc+J_lift+J_theta+J_slot+J_boundary+I_domain_mask+I_boundary_crossing)/M_H_ref",
            "candidate_value": "MISSING_COMPONENT_VALUES",
            "units": "dimensionless after parent source-current and M_H_ref normalization",
            "source_path": str(SRC_2356_DOMAIN_ROWS),
            "equation_anchor": "DMB2356_0_total",
            "status": "FALLBACK_SCHEMA_ONLY",
            "failure_mode": "component values, units, M_H_ref and source paths are missing",
            "accepted_live_input": False,
            "parent_signed": False,
        },
    ]
    return [add_common(row) for row in rows]


def queue_rows() -> list[dict[str, Any]]:
    rows = [
        ("Q2881_0_q_v_certificate", "q,Dq,v_X", "geometry_gate", "derive parent q object and prove v_X in ker(Dq) on an open local branch, or retain Dq_vertical_leak/J_vertical_physical rows", "MISSING_Q_OBJECT_AND_VERTICALITY", 1, True),
        ("Q2881_1_action_adoption", "MCA2526 adoption", "parent_action_gate", "derive minimal matter coupling from MTS core/object language or keep it as contract only", "MISSING_ACTION_ADOPTION_CERTIFICATE", 2, False),
        ("Q2881_2_J_qdesc", "J_qdesc", "finite_source_row", "source or zero failure of S_matter to factor through q", "MISSING_MATTER_DESCENT_PROOF_OR_NUMERIC_BOUND", 3, False),
        ("Q2881_3_J_lift", "J_matter_lift", "finite_source_row", "prove matter lift is Euler/gauge/boundary or source coefficient", "MISSING_MATTER_LIFT_OWNER", 4, False),
        ("Q2881_4_J_theta", "J_theta", "constant_source_row", "derive constant superselection or source clock/EM/mass sensitivity coefficients", "MISSING_CONSTANT_SUPERSELECTION_OR_COEFFICIENTS", 5, False),
        ("Q2881_5_J_slot", "J_source_only_slot", "source_only_slot_row", "prove no-source-only grammar/selector-blind source action or source finite weights", "MISSING_NO_SOURCE_ONLY_SLOT_OR_COEFFICIENTS", 6, False),
        ("Q2881_6_J_boundary", "J_boundary_support", "boundary_support_row", "prove boundary/support tail zero or source finite boundary flux", "MISSING_BOUNDARY_SUPPORT_SILENCE_OR_BOUND", 7, False),
        ("Q2881_7_MHref", "M_H_ref/tau/ell_J", "normalization_row", "derive same-frame source denominator and scale before empirical scoring", "MISSING_MHREF_TAU_ELLJ_LOCK", 8, False),
    ]
    return [
        add_common(
            {
                "queue_id": queue_id,
                "symbol": symbol,
                "row_type": row_type,
                "needed_action": action,
                "current_marker": marker,
                "priority": priority,
                "accepted_live_input": False,
                "selected_for_next": selected,
            }
        )
        for queue_id, symbol, row_type, action, marker, priority, selected in rows
    ]


def gate_rows() -> list[dict[str, Any]]:
    rows = [
        ("GATE2881_0_normal_form", "source-current normal form exists", "PASS_CONTROL_ONLY", "chain-rule identity and conditional theorem are exact but not current-MTS proof", False),
        ("GATE2881_1_Hilbert_current", "Hilbert current source object is parent-owned", "FAIL", "ell_J, tau and parent scale/current exchange are unsigned", False),
        ("GATE2881_2_JR_zero", "J_R=0 matter-descent theorem applies to current MTS", "FAIL", "q object, verticality, action adoption and boundary/support clauses are missing", False),
        ("GATE2881_3_MCA_adoption", "minimal coupling action is derived from MTS core", "FAIL", "MCA2526 is retained as least-scrutiny contract, not theorem", False),
        ("GATE2881_4_countermodels", "source-only/shadow/readout countermodels are excluded", "FAIL", "exclusion is conditional on parent adoption/object-language proof", False),
        ("GATE2881_5_finite_JR", "finite J_R residual row can be scored", "FAIL", "component values, units, M_H_ref and source paths are missing", False),
        ("GATE2881_6_local_claim", "local GR/Newton source-current reduction can be claimed", "FAIL_CLOSED", "source current descent and source normalization remain nonclaim", False),
    ]
    return [
        add_common(
            {
                "gate_id": gate_id,
                "criterion": criterion,
                "result": result,
                "reason": reason,
                "gate_passed": passed,
            }
        )
        for gate_id, criterion, result, reason, passed in rows
    ]


def runner_rows() -> list[dict[str, Any]]:
    return [
        add_common(
            {
                "runner_id": "RUN2881_0_JR_import",
                "status": "REFUSED_JR_SOURCE_CURRENT_NOT_LIVE",
                "accepted_JR_rows": 0,
                "required_JR_rows": 1,
                "reason": "J_R has an exact conditional descent theorem but no parent-signed q/v/action/boundary/normalization bundle and no finite sourced residual row",
                "runner_ready": False,
                "claim_unlocked": False,
                "score_allowed": False,
            }
        )
    ]


def decision_rows() -> list[dict[str, Any]]:
    rows = [
        ("DEC2881_0_theorem", "Record exact J_R descent normal form.", "COMPLETE_CONTROL_ONLY", "coupling zero is now a premise bundle, not a vibe"),
        ("DEC2881_1_contract", "Retain MCA2526 minimal coupling as least-scrutiny contract.", "RETAINED_NOT_PROMOTED", "it forbids dangerous source-only slots but is not derived from MTS core"),
        ("DEC2881_2_zero", "Try to prove J_R=0.", "REJECTED_CURRENT_CORPUS", "q object, verticality, action adoption and boundary/support/normalization clauses remain unsigned"),
        ("DEC2881_3_finite", "Stage finite J_R residual fallback.", "SCHEMA_ONLY", "component values and M_H_ref are missing"),
        ("DEC2881_4_next", "Route next to q-object/vertical-generator certificate.", "SELECTED_2882", "matter coupling can use q but cannot derive q or prove v_X in ker(Dq)"),
    ]
    return [
        add_common(
            {
                "decision_id": decision_id,
                "decision": decision,
                "result": result,
                "because": because,
            }
        )
        for decision_id, decision, result, because in rows
    ]


def next_rows() -> list[dict[str, Any]]:
    return [
        add_common(
            {
                "next_id": "NEXT2881_0_2882",
                "status": "selected_primary",
                "target_doc": "2882-Y5-R2FR-q-object-vertical-generator-certificate-or-Dq-leak-row-under-AX1090.md",
                "target_script": "scripts/Y5_R2FR_q_object_vertical_generator_certificate_or_Dq_leak_row_under_AX1090_2882.py",
                "mission": "derive the parent q object and prove the local residual generator v_X lies in ker(Dq) on an open local branch; if not, retain Dq_vertical_leak/J_vertical_physical finite rows and keep J_R blocked",
                "selected": True,
            }
        )
    ]


def copy_branch_outputs() -> list[dict[str, Any]]:
    pairs = [
        ("COPY2881_0_normal_form", OUTPUTS["normal_form"], BRANCH_OUTPUTS["normal_form_copy"], "J_R descent normal form nonclaim copy"),
        ("COPY2881_1_zero_audit", OUTPUTS["zero_audit"], BRANCH_OUTPUTS["zero_audit_copy"], "J_R zero gate audit nonclaim copy"),
        ("COPY2881_2_fill", OUTPUTS["fill"], BRANCH_OUTPUTS["fill_copy"], "failed J_R fill attempt nonclaim copy"),
        ("COPY2881_3_next_queue", OUTPUTS["next"], BRANCH_OUTPUTS["next_queue"], "RAB queue handoff to q/v certificate target"),
    ]
    rows: list[dict[str, Any]] = []
    for copy_id, source, destination, purpose in pairs:
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(source, destination)
        rows.append(
            add_common(
                {
                    "copy_id": copy_id,
                    "source_table": str(source),
                    "copy_path": str(destination),
                    "purpose": purpose,
                    "exists": destination.exists(),
                }
            )
        )
    return rows


def remove_pycache() -> None:
    pycache = Path(__file__).resolve().parent / "__pycache__"
    if pycache.exists():
        shutil.rmtree(pycache)


def formalization_untouched() -> bool:
    if not FORMALIZATION.exists():
        return True
    for path in FORMALIZATION.rglob("*"):
        if path.is_file():
            modified = datetime.fromtimestamp(path.stat().st_mtime, timezone.utc)
            if modified > SCRIPT_START_UTC:
                return False
    return True


def generated_under_root(paths: list[Path]) -> bool:
    root_resolved = ROOT.resolve()
    for path in paths:
        try:
            path.resolve().relative_to(root_resolved)
        except ValueError:
            return False
    return True


def no_claim_flags(rows_by_name: dict[str, list[dict[str, Any]]]) -> bool:
    claim_keys = {
        "score_ready",
        "valid_prediction_row",
        "valid_for_claim",
        "claim_allowed",
        "accepted_current_theorem",
        "parent_signed",
        "gate_pass",
        "theorem_zero",
        "excluded_now",
        "claim_safe",
        "accepted_live_input",
        "gate_passed",
        "runner_ready",
        "claim_unlocked",
        "score_allowed",
    }
    for rows in rows_by_name.values():
        for row in rows:
            for key in claim_keys:
                if row.get(key) is True:
                    return False
    return True


def validation_rows(rows_by_name: dict[str, list[dict[str, Any]]], branch_rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    sources = rows_by_name["sources"]
    normal_form = rows_by_name["normal_form"]
    zero_audit = rows_by_name["zero_audit"]
    countermodels = rows_by_name["countermodels"]
    fill = rows_by_name["fill"]
    queue = rows_by_name["queue"]
    gates = rows_by_name["gates"]
    runner = rows_by_name["runner"]
    next_target = rows_by_name["next"]

    output_paths_without_validation = [path for key, path in OUTPUTS.items() if key != "validation"]
    branch_paths = list(BRANCH_OUTPUTS.values())
    all_generated_paths = output_paths_without_validation + branch_paths + [DOC, OUTPUTS["validation"]]

    checks = [
        ("VAL2881_0_sources_exist", all(row["path_exists"] for row in sources), "all registered source paths exist"),
        ("VAL2881_1_source_anchors", all(row["anchors_found"] for row in sources), "all registered source anchors were found"),
        ("VAL2881_2_normal_form_complete", len(normal_form) == 5 and any(row["form_id"] == "JR2881_2_descent_theorem" for row in normal_form), "J_R normal form and exact conditional theorem recorded"),
        ("VAL2881_3_no_theorem_promotion", not any(row["accepted_current_theorem"] for row in normal_form), "conditional theorem not promoted to current-MTS claim"),
        ("VAL2881_4_zero_gate_blocked", any(row["zero_gate_id"] == "ZG2881_11_joint_JR_zero" and row["current_status"] == "NOT_CLOSED" for row in zero_audit) and not any(row["theorem_zero"] for row in zero_audit), "J_R zero theorem not closed"),
        ("VAL2881_5_countermodels_retained", len(countermodels) >= 8 and not any(row["excluded_now"] for row in countermodels), "dangerous source-current countermodels retained"),
        ("VAL2881_6_fill_refused", not any(row["accepted_live_input"] for row in fill), "J_R live/zero/finite fill attempts refused"),
        ("VAL2881_7_queue_selects_qv", any(row["queue_id"] == "Q2881_0_q_v_certificate" and row["selected_for_next"] is True for row in queue), "q/Dq/v_X certificate selected next"),
        ("VAL2881_8_gates_fail_closed", all(row["gate_passed"] is False for row in gates), "all J_R claim gates fail closed"),
        ("VAL2881_9_runner_refused", runner[0]["status"] == "REFUSED_JR_SOURCE_CURRENT_NOT_LIVE" and runner[0]["runner_ready"] is False, "runner remains refused"),
        ("VAL2881_10_next_target_2882", next_target[0]["next_id"] == "NEXT2881_0_2882" and next_target[0]["selected"] is True, "2882 q/v target selected"),
        ("VAL2881_11_outputs_exist", all(path.exists() for path in output_paths_without_validation), "all generated CSV outputs exist before validation write"),
        ("VAL2881_12_branch_outputs_exist", all(path.exists() for path in branch_paths) and all(row["exists"] for row in branch_rows), "branch copies were written"),
        ("VAL2881_13_csv_parse", all(csv_parses(path) for path in output_paths_without_validation + branch_paths), "all generated CSV outputs parse"),
        ("VAL2881_14_no_claim_flags", no_claim_flags(rows_by_name | {"branches": branch_rows}), "no claim/score/prediction flags are true"),
        ("VAL2881_15_generated_under_post_checkpoint", generated_under_root(all_generated_paths), "all generated artifacts remain under post-checkpoint-work"),
        ("VAL2881_16_formalization_untouched", formalization_untouched(), "formalization-workbench was not modified during this run"),
        ("VAL2881_17_pycache_absent", not (Path(__file__).resolve().parent / "__pycache__").exists(), "scripts __pycache__ absent during validation"),
    ]
    rows = [
        {
            "validation_id": validation_id,
            "passed": passed,
            "detail": detail,
            "timestamp_utc": now(),
        }
        for validation_id, passed, detail in checks
    ]
    rows.append(
        {
            "validation_id": "VAL2881_OVERALL",
            "passed": all(row["passed"] for row in rows),
            "detail": "2881 recorded the exact conditional J_R descent theorem, refused matter-source zero/live-row promotion, retained coupling countermodels, and selected q-object/vertical-generator certification for 2882.",
            "timestamp_utc": now(),
        }
    )
    return rows


def md_table(rows: list[dict[str, Any]], columns: list[str]) -> str:
    header = "| " + " | ".join(columns) + " |"
    separator = "| " + " | ".join("---" for _ in columns) + " |"
    body = []
    for row in rows:
        cells = []
        for column in columns:
            value = str(row.get(column, ""))
            value = value.replace("\n", " ").replace("|", "\\|")
            cells.append(value)
        body.append("| " + " | ".join(cells) + " |")
    return "\n".join([header, separator, *body])


def write_doc(rows_by_name: dict[str, list[dict[str, Any]]], branch_rows: list[dict[str, Any]], validation: list[dict[str, Any]]) -> None:
    text = f"""# 2881 - Y5 R2FR J_R Matter-Source Current Or Matter-Descent Zero Under AX1090

Status: `Y5_R2FR_2881_JR_descent_theorem_conditional_zero_not_signed_qv_2882_next`

## Private Verdict

2881 hits the coupling nerve properly.

There is a real conditional theorem:

`delta_v S_m = DSbar[Dq(v)] + E_psi delta_v psi + J_theta L_v theta + J_direct[v] + delta_v B`.

So if the parent supplies `S_matter=Sbar[q(Phi),psi,theta]+dB`, `Dq(v)=0`, vertical matter lifts are gauge/Euler/boundary-only, constants are fixed, source-only slots are forbidden, and boundary/support terms are zero or explicit, then the bulk matter-source current vanishes: `J_R=0` for that residual direction.

But current MTS does not yet sign those antecedents. The clean minimal matter-coupling action from 2526 is a good contract, not a derived parent theorem. The upstream missing key is now sharp: derive the parent `q` object and prove the local generator `v_X` is truly in `ker(Dq)` on an open local branch.

No local-GR/Newton/R10/PPN claim is unlocked here. This checkpoint keeps the coupling route alive without letting it become handwaving.

## Source Register

{md_table(rows_by_name["sources"], ["source_id", "role", "path_exists", "anchors_found", "missing_anchors", "valid_for_claim"])}

## J_R Descent Normal Form

{md_table(rows_by_name["normal_form"], ["form_id", "statement", "role", "current_status", "accepted_current_theorem", "parent_signed", "valid_for_claim"])}

## J_R Zero Gate Audit

{md_table(rows_by_name["zero_audit"], ["zero_gate_id", "required_clause", "formal_condition", "current_status", "gate_pass", "theorem_zero", "valid_for_claim"])}

## Countermodel Ledger

{md_table(rows_by_name["countermodels"], ["countermodel_id", "countermodel", "why_dangerous", "current_status", "excluded_now", "claim_safe", "valid_for_claim"])}

## J_R Fill Attempt

{md_table(rows_by_name["fill"], ["fill_id", "quantity", "candidate_formula", "candidate_value", "status", "failure_mode", "accepted_live_input", "valid_for_claim"])}

## Source-Current Acquisition Queue

{md_table(rows_by_name["queue"], ["queue_id", "symbol", "row_type", "needed_action", "current_marker", "priority", "selected_for_next", "valid_for_claim"])}

## Acceptance Gates

{md_table(rows_by_name["gates"], ["gate_id", "criterion", "result", "reason", "gate_passed", "valid_for_claim"])}

## Runner Status

{md_table(rows_by_name["runner"], ["runner_id", "status", "accepted_JR_rows", "required_JR_rows", "reason", "runner_ready", "valid_for_claim"])}

## Decision Ledger

{md_table(rows_by_name["decision"], ["decision_id", "decision", "result", "because", "valid_for_claim"])}

## Next Target

{md_table(rows_by_name["next"], ["next_id", "status", "target_doc", "target_script", "mission", "selected", "valid_for_claim"])}

## Branch Copies

{md_table(branch_rows, ["copy_id", "source_table", "copy_path", "purpose", "exists", "valid_for_claim"])}

## Validation

{md_table(validation, ["validation_id", "passed", "detail", "timestamp_utc"])}
"""
    DOC.write_text(text, encoding="utf-8")


def main() -> None:
    remove_pycache()

    rows_by_name = {
        "sources": source_register_rows(),
        "normal_form": normal_form_rows(),
        "zero_audit": zero_audit_rows(),
        "countermodels": countermodel_rows(),
        "fill": fill_rows(),
        "queue": queue_rows(),
        "gates": gate_rows(),
        "runner": runner_rows(),
        "decision": decision_rows(),
        "next": next_rows(),
    }

    for name, rows in rows_by_name.items():
        write_csv(OUTPUTS[name], rows)

    branch_rows = copy_branch_outputs()
    write_csv(OUTPUTS["branches"], branch_rows)
    rows_by_name["branches"] = branch_rows

    remove_pycache()
    validation = validation_rows(rows_by_name, branch_rows)
    write_csv(OUTPUTS["validation"], validation)
    write_doc(rows_by_name, branch_rows, validation)
    remove_pycache()

    print(f"Wrote {DOC}")
    print(f"Wrote {OUTPUTS['validation']}")
    overall = next(row for row in validation if row["validation_id"] == "VAL2881_OVERALL")
    print(f"VAL2881_OVERALL={overall['passed']}")


if __name__ == "__main__":
    main()

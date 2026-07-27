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
RAB_QUEUE = ROOT / "source-intake" / "rab-sector" / "acquisition-queue"
PARENT_ACTION = ROOT / "source-intake" / "parent-action"
FORMALIZATION = PROJECT / "formalization-workbench"

CHECKPOINT = "2922"
BRANCH_ID = "MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428"
RUN_UTC = SCRIPT_START_UTC.isoformat()

DOC = ROOT / "2922-Y5-R2FR-Hamiltonian-sector-owner-or-source-mass-first-row-under-AX1090.md"

SRC_2921_DOC = ROOT / "2921-Y5-R2FR-source-normalized-Newton-Gauss-orbital-scorecard-or-parent-source-mass-identity-under-AX1090.md"
SRC_2921_NEXT = RESIDUALS / "P8_Y5_R2FR_2921_NEXT_TARGET.csv"
SRC_2921_IDENTITY = RESIDUALS / "P8_Y5_R2FR_2921_PARENT_SOURCE_MASS_IDENTITY_AUDIT.csv"
SRC_1018_DOC = ROOT / "1018-Y5-R10-sector-Lagrangian-boundary-owner-or-FB5540-source-row.md"
SRC_1018_OWNER = RESIDUALS / "P8_Y5_R10_1018_OWNER_CLAUSES.csv"
SRC_1018_SCHEMA = RESIDUALS / "P8_Y5_R10_1018_SOURCE_ROW_SCHEMA.csv"
SRC_1019_SCHEMA = RESIDUALS / "P8_Y5_R10_1019_SOURCE_PACK_SCHEMA.csv"
SRC_1021_DOC = ROOT / "1021-Y5-R10-BX-primitive-from-parent-variation-or-edge-bound-term-fill.md"
SRC_1024_DOC = ROOT / "1024-Y5-R10-scalar-nohair-input-pack-or-residual-alpha-coefficient-runner.md"
SRC_1105_DOC = ROOT / "1105-Y5-R10-master-no-hidden-visible-coefficient-morphism-or-explicit-closure-pack.md"
SRC_1237_DOC = ROOT / "1237-Y5-R10-MTS-primitives-to-sorted-parent-action-derivation-or-closure-demotion.md"
SRC_1238_DOC = ROOT / "1238-Y5-R10-first-class-RAB-constraint-or-local-GR-closure-benchmark-scorecard.md"
SRC_1249_DOC = ROOT / "1249-Y5-R10-finite-qRhat-source-acquisition-and-policy-runner.md"
SRC_1249_RESULTS = RESIDUALS / "P8_Y5_R10_1249_FINITE_QRHAT_CANDIDATE_RESULTS.csv"
SRC_1249_VALIDATION = RESIDUALS / "P8_Y5_BRR545_1249_VALIDATION.csv"

OUTPUTS = {
    "sources": RESIDUALS / "P8_Y5_R2FR_2922_SOURCE_REGISTER.csv",
    "owner_audit": RESIDUALS / "P8_Y5_R2FR_2922_HAMILTONIAN_SECTOR_OWNER_AUDIT.csv",
    "first_row_schema": RESIDUALS / "P8_Y5_R2FR_2922_SOURCE_MASS_FIRST_ROW_SCHEMA.csv",
    "refusal_runner": RESIDUALS / "P8_Y5_R2FR_2922_SOURCE_MASS_FIRST_ROW_REFUSAL_RUNNER.csv",
    "endpoint_crosswalk": RESIDUALS / "P8_Y5_R2FR_2922_PRIOR_CHAIN_ENDPOINT_CROSSWALK.csv",
    "claims": RESIDUALS / "P8_Y5_R2FR_2922_CLAIM_GATES.csv",
    "decision": RESIDUALS / "P8_Y5_R2FR_2922_DECISION_LEDGER.csv",
    "next": RESIDUALS / "P8_Y5_R2FR_2922_NEXT_TARGET.csv",
    "branches": RESIDUALS / "P8_Y5_R2FR_2922_BRANCH_COPIES.csv",
    "validation": RESIDUALS / "P8_Y5_BRR545_2922_VALIDATION.csv",
}

BRANCH_OUTPUTS = {
    "owner_copy": PARENT_ACTION / "Hamiltonian_sector_owner_audit_2922_NONCLAIM.csv",
    "first_row_copy": LOCAL_BOUNDS / "Source_mass_first_row_schema_2922_NONCLAIM.csv",
    "next_copy": RAB_QUEUE / "JR2922_HCORE_COEFFICIENT_OR_SOURCE_MASS_TEMPLATE_NEXT_NONCLAIM.csv",
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


def csv_parses(path: Path) -> bool:
    try:
        with path.open(newline="", encoding="utf-8") as handle:
            list(csv.DictReader(handle))
        return True
    except Exception:
        return False


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
    body = [
        "| " + " | ".join(md_escape(row.get(column, "")) for column in selected) + " |"
        for row in rows
    ]
    return "\n".join([header, separator, *body])


def source_register_rows() -> list[dict[str, Any]]:
    specs = [
        ("SRC2922_00_2921_doc", SRC_2921_DOC, "NEXT2921_0_2922;source-mass first-row", "2921 selected Hamiltonian sector owner/source-mass first-row gate"),
        ("SRC2922_01_2921_next", SRC_2921_NEXT, "NEXT2921_0_2922;L_X/Theta_X/Q_X", "machine-readable 2922 target"),
        ("SRC2922_02_2921_identity", SRC_2921_IDENTITY, "PSM2921_6_MHref_reference_lock;PSM2921_10_verdict", "2921 parent source-mass identity audit"),
        ("SRC2922_03_1018_doc", SRC_1018_DOC, "LOC1018_8_verdict;DEC1018_0_owner_result", "1018 sector owner map"),
        ("SRC2922_04_1018_owner", SRC_1018_OWNER, "LOC1018_0_LX_owner;LOC1018_8_verdict", "owner clauses for L_X/Theta/Q/B_ref/B_class/tau/MHref"),
        ("SRC2922_05_1018_schema", SRC_1018_SCHEMA, "FSR1018_0_M_H_ref;FSR1018_7_total_guard", "source-row schema for Hamiltonian denominator and no-cancellation guard"),
        ("SRC2922_06_1019_schema", SRC_1019_SCHEMA, "SP1019_0_M_H_ref;SP1019_7_total_guard", "source-pack schema for M_H_ref/bulk/edge/R11 rows"),
        ("SRC2922_07_1021_doc", SRC_1021_DOC, "DEC1021_0_primitive_result;DEC1021_2_best_next", "B_X primitive route failure and branch split"),
        ("SRC2922_08_1024_doc", SRC_1024_DOC, "BV1024_2_coupling_status;DEC1024_3_next_target", "scalar no-hair input/alpha runner refusal"),
        ("SRC2922_09_1105_doc", SRC_1105_DOC, "MHM1105_6_verdict;PACK1105_4_residual_vector_if_unsigned", "master no-hidden-visible morphism demotion"),
        ("SRC2922_10_1237_doc", SRC_1237_DOC, "PRIM1237_8_verdict;DERIVATION_FAILS_CLOSURE_DEMOTION_REQUIRED", "MTS primitive route to sorted parent action fails"),
        ("SRC2922_11_1238_doc", SRC_1238_DOC, "BGR1238_1_closure_GR;DEC1238_2_residual_vector_selected", "local-GR closure benchmark and residual vector selection"),
        ("SRC2922_12_1249_doc", SRC_1249_DOC, "DEC1249_2_local_status;NEXT1249_0_1250", "finite qRhat source intake endpoint"),
        ("SRC2922_13_1249_results", SRC_1249_RESULTS, "QRHAT1255_CASSINI_GAMMA_1SIGMA_BOUND_NONCLAIM;ACCEPTED_NONCLAIM_FINITE_QRHAT", "accepted finite qRhat nonclaim smoke row"),
        ("SRC2922_14_1249_validation", SRC_1249_VALIDATION, "VAL1249_12_overall;PASS", "1249 validation summary"),
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


def owner_audit_rows() -> list[dict[str, Any]]:
    specs = [
        (
            "HOA2922_0_target",
            "same-frame Hamiltonian source mass",
            "M_H := G_ref^-1[H_tau - H_ref] = G_ref^-1 integral_S Q_tau^MTS in the observed source/orbit frame",
            "TARGET_DEFINED_NOT_DERIVED",
            "this is the denominator/source object needed before Newton and beta can be physically scored",
            False,
        ),
        (
            "HOA2922_1_LX_owner",
            "parent-owned sector Lagrangian",
            "L_X[g,X,nabla X] with explicit field content, normalization, source term, derivative order, and boundary convention",
            "NOT_SIGNED",
            "without L_X, Theta_X/Q_X/P_X/B_X and Hessian signs are menus, not derivations",
            False,
        ),
        (
            "HOA2922_2_Theta_Q_owner",
            "sector symplectic potential and Hamiltonian charge",
            "delta L_X=E_X delta X+dTheta_X and J_tau^X=Theta_X(L_tau X)-i_tau L_X=dQ_tau^X+C_tau^X",
            "FORMULA_WRITTEN_NOT_OWNED",
            "Hamiltonian integrability and source charge cannot be certified from a symbolic current alone",
            False,
        ),
        (
            "HOA2922_3_Bref_owner",
            "fixed reference/counterterm before readout",
            "B_ref[gamma_ref,tau_ref,C_top] with no source/radius/time/frame/range retuning",
            "NOT_SIGNED",
            "reference subtraction can otherwise absorb the source-mass answer",
            False,
        ),
        (
            "HOA2922_4_Bclass_owner",
            "boundary class, cohomology, and projector silence",
            "B_class and C_top fix exact/harmonic/corner sectors and Pi_M^H[Q_edge]=0 or a finite bound",
            "NOT_SIGNED",
            "edge/source leakage remains active in R10, alpha3, and source-normalization rows",
            False,
        ),
        (
            "HOA2922_5_tau_lock",
            "one observed time/coframe generator",
            "tau_source=tau_charge=tau_clock=tau_readout and delta tau=0 on the comparison branch",
            "NOT_SIGNED",
            "same-frame Hamiltonian mass is not fixed if charge time and orbital/readout time differ",
            False,
        ),
        (
            "HOA2922_6_MHref_positive",
            "positive same-frame source denominator",
            "M_H_ref > 0 with declared units, surface, reference, G_ref, and source path",
            "MISSING_M_H_REF",
            "no finite local residual row is scoreable without a denominator that does not borrow orbital GM",
            False,
        ),
        (
            "HOA2922_7_PiM_H_projector",
            "Hamiltonian mass/source projector",
            "Pi_M^H[f]=partial f/partial M_H_ref at fixed tau, surface, reference, boundary class, and topological sector",
            "FORMAL_DEFINITION_ONLY",
            "projector can silently absorb reference or edge variation unless the source coordinate is parent-owned",
            False,
        ),
        (
            "HOA2922_8_no_hidden_visible_morphism",
            "visible coefficients cannot depend on hidden/source scalars",
            "S_vis=S_vis[q(Phi),theta_rep] with no hidden-visible coefficient morphism or radiative/readout return",
            "CLOSURE_PACK_NOT_DERIVED",
            "otherwise alpha/mass/source/clock constants remain legal residual coefficients",
            False,
        ),
        (
            "HOA2922_9_RAB_or_qRhat",
            "reciprocal hair/local metric residual branch",
            "R_AB=0 as first-class parent constraint, or finite q_R_hat source row with policy/GM convention",
            "FIRST_CLASS_NOT_CONSTRUCTED_FINITE_SMOKE_ONLY",
            "1249 provides nonclaim finite intake discipline, not a parent coefficient prediction",
            False,
        ),
        (
            "HOA2922_10_verdict",
            "current Hamiltonian sector-owner theorem",
            "HOA2922_0 through HOA2922_9 parent-signed together",
            "OWNER_THEOREM_NOT_DERIVED_FIRST_ROW_TEMPLATE_REQUIRED",
            "stage source-mass rows and move to H_core/parent coefficient checklist rather than claiming local GR",
            False,
        ),
    ]
    return [
        add_common(
            {
                "audit_id": audit_id,
                "owner_clause": clause,
                "math_form": math_form,
                "current_status": status,
                "why_it_matters": why,
                "clause_passed": passed,
                "source_paths": f"{SRC_2921_DOC};{SRC_1018_OWNER};{SRC_1105_DOC};{SRC_1238_DOC};{SRC_1249_DOC}",
            }
        )
        for audit_id, clause, math_form, status, why, passed in specs
    ]


def first_row_schema_rows() -> list[dict[str, Any]]:
    specs = [
        ("SMR2922_0_identity", "source_mass_identity_row", "system_id;branch_id;claim_type;mu_obs_convention;G_ref;M_H;M_H_units;source_path;equation_ref;valid_for_claim", "MISSING_PARENT_SOURCE_MASS_ROW", "defines whether this is a theorem row, finite residual row, or nonclaim smoke row"),
        ("SMR2922_1_Htau", "H_tau_or_Q_tau_integral", "tau_id;surface_id;Q_tau_integral;H_tau;H_tau_units;Theta_source;Q_source;source_path;equation_ref", "MISSING_HTAU_QTAU_SOURCE", "observed-time Hamiltonian charge input"),
        ("SMR2922_2_reference", "H_ref_Bref_rule", "reference_branch;B_ref_rule;H_ref;Delta_ref;counterterm_convention;fixed_before_readout_certificate;source_path", "MISSING_FIXED_REFERENCE_RULE", "blocks fitted subtraction from becoming a fake mass proof"),
        ("SMR2922_3_MHref", "M_H_ref_denominator", "M_H_ref;M_H_ref_units;positive_certificate;same_frame_certificate;no_orbital_GM_import;source_path", "MISSING_POSITIVE_SAME_FRAME_MHREF", "denominator for normalized source-mass and residual rows"),
        ("SMR2922_4_PiM", "Pi_M_H_projector", "projector_definition;held_fixed_fields;surface_class;topological_class;PiM_variation_status;source_path", "MISSING_PARENT_PIMH_PROJECTOR", "prevents source projector from being chosen after orbit/readout"),
        ("SMR2922_5_PG_bridge", "Poisson_Gauss_orbital_bridge_certificate", "Poisson_coefficient;Gauss_surface_rule;orbital_readout_rule;S_res_status;mu_extra_status;source_path", "MISSING_PG_BRIDGE_PREMISES", "connects Hamiltonian charge to measured orbital GM"),
        ("SMR2922_6_flux_obstruction", "flux_R_eq_Icommutator_pack", "R_eq_integral;I_commutator;dln_Meff_dt;radial_hair;units;normalization;source_path", "MISSING_FLUX_OBSTRUCTION_VALUES", "turns failed Pi_M flux closure into finite source rows"),
        ("SMR2922_7_extra_channels", "mu_extra_and_hidden_visible_coefficients", "mu_extra_vector;b_alpha;b_mu;b_mA;b_nuc;b_clock;qbar_constants_abs;units;source_path", "MISSING_EXTRA_CHANNEL_VECTOR", "keeps hidden-visible/source coefficients explicit"),
        ("SMR2922_8_qRhat", "finite_q_R_hat_optional", "route_type;q_R_hat;gamma_minus_1_QR;GM_convention;closure_used;uncertainty_policy;source_path;valid_for_claim", "NONCLAIM_SMOKE_ONLY_IF_PRESENT", "finite qRhat can test policy but does not prove parent source mass"),
        ("SMR2922_9_total_guard", "source_mass_total_guard", "abs_sum_components;bound_or_policy;no_cancellation_guard;all_components_sourced;valid_for_claim", "NOT_COMPUTED_COMPONENTS_MISSING", "no cancellation between unknown owner/source components"),
    ]
    return [
        add_common(
            {
                "schema_id": schema_id,
                "row_object": row_object,
                "required_columns": columns,
                "current_status": status,
                "purpose": purpose,
                "source_paths": f"{SRC_1018_SCHEMA};{SRC_1019_SCHEMA};{SRC_1249_RESULTS}",
            }
        )
        for schema_id, row_object, columns, status, purpose in specs
    ]


def refusal_runner_rows() -> list[dict[str, Any]]:
    specs = [
        ("FRR2922_0_missing_Htau", "candidate_source_mass_row", "MISSING_HTAU_QTAU_SOURCE", "REJECT_MISSING_PARENT_CHARGE", False),
        ("FRR2922_1_missing_reference", "candidate_source_mass_row", "MISSING_FIXED_REFERENCE_RULE", "REJECT_REFERENCE_CAN_BE_FITTED", False),
        ("FRR2922_2_missing_MHref", "candidate_source_mass_row", "MISSING_POSITIVE_SAME_FRAME_MHREF", "REJECT_NO_DENOMINATOR", False),
        ("FRR2922_3_orbital_GM_import", "candidate_source_mass_row", "GM_orbit used as M_H_ref before bridge", "REJECT_CIRCULAR_NEWTON_IMPORT", False),
        ("FRR2922_4_closure_zero", "candidate_source_mass_row", "closure_used=true or q_R_hat=0 from ansatz", "REJECT_CLOSURE_AS_EVIDENCE", False),
        ("FRR2922_5_finite_qRhat_smoke", "QRHAT1255_CASSINI_GAMMA_1SIGMA_BOUND_NONCLAIM", "finite nonclaim q_R_hat row accepted by 1249 policy", "ACCEPTED_AS_NONCLAIM_SMOKE_NOT_SOURCE_MASS_PROOF", True),
        ("FRR2922_6_total_verdict", "2922 source-mass first row", "no candidate row contains all required owner/source fields", "FIRST_ROW_NOT_SCORE_READY", False),
    ]
    return [
        add_common(
            {
                "runner_id": runner_id,
                "candidate_id": candidate_id,
                "trigger": trigger,
                "runner_status": status,
                "runner_eligible": eligible,
                "source_paths": f"{OUTPUTS['first_row_schema']};{SRC_1249_RESULTS}",
            }
        )
        for runner_id, candidate_id, trigger, status, eligible in specs
    ]


def endpoint_crosswalk_rows() -> list[dict[str, Any]]:
    specs = [
        ("XW2922_0_1018", "1018", "owner map for L_X/Theta/Q/B_ref/B_class/tau/MHref", "all owner clauses explicit", "no owner route signed", "2922 keeps owner theorem nonclaim"),
        ("XW2922_1_1021", "1021", "B_X primitive map and scalar/edge route split", "primitive route separated from scalar no-hair", "parent L_X/Theta/Q/P_X/B_ct not signed", "2922 does not claim boundary exactness"),
        ("XW2922_2_1024", "1024", "scalar no-hair input and alpha runner refusal", "J_X/qbar/Qbar coupling gap made concrete", "Z_X/M_X2/J_X/boundary_flux missing", "2922 treats scalar route as finite residual unless sourced"),
        ("XW2922_3_1105", "1105", "master no-hidden-visible morphism compressed to closure pack", "minimum closure pack written", "pack not derived from parent object language", "2922 refuses hidden-visible coefficient zeroes"),
        ("XW2922_4_1237", "1237", "MTS primitives to sorted parent action attempted", "motion-load local GR scaffold isolated", "sorted grammar remains closure-only", "2922 does not use closure grammar as derivation"),
        ("XW2922_5_1238", "1238", "local-GR closure benchmark and residual vector selected", "private benchmark available", "first-class R_AB constraint not constructed", "2922 separates benchmark from proof"),
        ("XW2922_6_1249", "1249", "finite q_R_hat policy runner validates nonclaim smoke row", "finite runner ready", "parent coefficient map missing", "2922 can inherit row discipline but not a theory claim"),
        ("XW2922_7_2921", "2921", "Newton bridge retained as conditional theorem", "source-mass identity target sharpened", "Hamiltonian owner/source row missing", "2922 stages exact first-row schema"),
    ]
    return [
        add_common(
            {
                "crosswalk_id": crosswalk_id,
                "prior_checkpoint": checkpoint,
                "resolved": resolved,
                "usable_gain": gain,
                "remaining_blocker": blocker,
                "2922_use": use,
            }
        )
        for crosswalk_id, checkpoint, resolved, gain, blocker, use in specs
    ]


def claim_rows() -> list[dict[str, Any]]:
    specs = [
        ("CG2922_0_owner_theorem", "Hamiltonian sector-owner theorem is derived", "BLOCKED_NONCLAIM", "L_X/Theta/Q/B_ref/B_class/tau/MHref/PiM^H are not parent-signed", False),
        ("CG2922_1_source_mass_row", "claim-grade source-mass first row exists", "BLOCKED_NONCLAIM", "required H_tau, reference, MHref, PiM^H, PG bridge, and residual fields are missing", False),
        ("CG2922_2_finite_qRhat_claim", "finite q_R_hat row is an MTS prediction", "BLOCKED_NONCLAIM", "1249 row is accepted only as nonclaim phenomenological smoke", False),
        ("CG2922_3_newton_beta_reopen", "source-normalized Newton/beta gates reopen", "BLOCKED_NONCLAIM", "parent source mass remains unproved and scorecard rows remain missing", False),
        ("CG2922_4_local_GR", "local GR/Newton reduction follows", "BLOCKED_NONCLAIM", "owner theorem and residual vector are still open", False),
        ("CG2922_5_no_circling", "prior chain endpoint is imported", "PASS_GUARDRAIL", "1018-1249 endpoint lessons are crosswalked into the current branch", False),
        ("CG2922_6_public_or_github", "public/GitHub claim can be made from 2922", "BLOCKED_NONCLAIM", "private checkpoint only", False),
    ]
    return [
        add_common(
            {
                "gate_id": gate_id,
                "claim": claim,
                "gate_status": status,
                "reason": reason,
                "gate_pass": gate_pass,
            }
        )
        for gate_id, claim, status, reason, gate_pass in specs
    ]


def decision_rows() -> list[dict[str, Any]]:
    specs = [
        (
            "DEC2922_0_owner_result",
            "do not claim the Hamiltonian sector-owner theorem",
            "the owner map is precise but the actual parent L_X/Theta/Q/B_ref/B_class/tau/MHref/PiM^H package is unsigned",
            "keep source-normalized Newton and beta blocked",
        ),
        (
            "DEC2922_1_first_row_result",
            "stage the exact source-mass first-row schema instead of a placeholder prediction",
            "no candidate row currently has the full parent charge, reference, denominator, projector, bridge, and residual fields",
            "use the refusal runner to reject circular GM import and closure-zero rows",
        ),
        (
            "DEC2922_2_prior_endpoint",
            "import the 1018-1249 endpoint rather than restarting the source hunt",
            "the old chain already shows closure benchmarks and finite qRhat smoke are useful but not derivations",
            "next work should build the H_core coefficient checklist or source-backed first row",
        ),
        (
            "DEC2922_3_next",
            "select first finite source-mass/H_core coefficient template",
            "the next useful deliverable is a row that a real parent coefficient or finite phenomenological source can fill without ambiguity",
            "2923 should create the H_core coefficient checklist and strict source-mass row validator",
        ),
    ]
    return [
        add_common(
            {
                "decision_id": decision_id,
                "decision": decision,
                "because": because,
                "next_action": action,
            }
        )
        for decision_id, decision, because, action in specs
    ]


def next_rows() -> list[dict[str, Any]]:
    return [
        add_common(
            {
                "route_id": "NEXT2922_0_2923",
                "selection_status": "selected_primary",
                "target_file": "2923-Y5-R2FR-first-source-mass-row-template-and-Hcore-coefficient-checklist-under-AX1090.md",
                "target_script": "scripts/Y5_R2FR_first_source_mass_row_template_and_Hcore_coefficient_checklist_under_AX1090_2923.py",
                "task": "create the exact claim-safe source-mass first-row template and H_core/Q_tau coefficient checklist, rejecting closure zeros, orbital-GM denominators, and placeholder owner rows",
                "success_condition": "template contains all parent charge/reference/MHref/PiM/Poisson-Gauss/residual fields and strict validator rejects every incomplete or circular row while accepting only nonclaim finite smoke rows",
                "fallback_condition": "keep owner theorem blocked and route to finite residual acquisition rows with no cancellation credit",
            }
        )
    ]


def branch_rows() -> list[dict[str, Any]]:
    copies = [
        ("owner_copy", OUTPUTS["owner_audit"], BRANCH_OUTPUTS["owner_copy"]),
        ("first_row_copy", OUTPUTS["first_row_schema"], BRANCH_OUTPUTS["first_row_copy"]),
        ("next_copy", OUTPUTS["next"], BRANCH_OUTPUTS["next_copy"]),
    ]
    rows = []
    for copy_id, source_path, destination_path in copies:
        shutil.copyfile(source_path, destination_path)
        rows.append(
            add_common(
                {
                    "copy_id": copy_id,
                    "source_path": str(source_path),
                    "destination_path": str(destination_path),
                    "source_exists": source_path.exists(),
                    "destination_exists": destination_path.exists(),
                    "destination_parses": csv_parses(destination_path),
                }
            )
        )
    return rows


def validation_rows(
    source_rows: list[dict[str, Any]],
    owner_rows: list[dict[str, Any]],
    schema_rows: list[dict[str, Any]],
    refusal_rows: list[dict[str, Any]],
    crosswalk_rows: list[dict[str, Any]],
    claim_rows_: list[dict[str, Any]],
    next_rows_: list[dict[str, Any]],
    branch_rows_: list[dict[str, Any]],
    include_doc_check: bool,
) -> list[dict[str, Any]]:
    generated_csvs = list(OUTPUTS.values())
    if not include_doc_check:
        generated_csvs = [path for key, path in OUTPUTS.items() if key != "validation"]

    rows = [
        {
            "validation_id": "VAL2922_0_source_paths_exist",
            "status": all(bool(row["path_exists"]) for row in source_rows),
            "detail": "all cited source paths exist",
            "valid_for_claim": False,
            "generated_utc": RUN_UTC,
        },
        {
            "validation_id": "VAL2922_1_source_anchors_found",
            "status": all(bool(row["anchors_found"]) for row in source_rows),
            "detail": "all source anchors found",
            "valid_for_claim": False,
            "generated_utc": RUN_UTC,
        },
        {
            "validation_id": "VAL2922_2_csv_outputs_parse",
            "status": all(csv_parses(path) for path in generated_csvs),
            "detail": "generated CSV outputs parse cleanly",
            "valid_for_claim": False,
            "generated_utc": RUN_UTC,
        },
        {
            "validation_id": "VAL2922_3_owner_verdict_blocks_claim",
            "status": any(row["audit_id"] == "HOA2922_10_verdict" and "NOT_DERIVED" in row["current_status"] for row in owner_rows),
            "detail": "Hamiltonian owner theorem remains unproved",
            "valid_for_claim": False,
            "generated_utc": RUN_UTC,
        },
        {
            "validation_id": "VAL2922_4_first_row_schema_complete",
            "status": {row["row_object"] for row in schema_rows}
            == {
                "source_mass_identity_row",
                "H_tau_or_Q_tau_integral",
                "H_ref_Bref_rule",
                "M_H_ref_denominator",
                "Pi_M_H_projector",
                "Poisson_Gauss_orbital_bridge_certificate",
                "flux_R_eq_Icommutator_pack",
                "mu_extra_and_hidden_visible_coefficients",
                "finite_q_R_hat_optional",
                "source_mass_total_guard",
            },
            "detail": "first-row schema covers owner, bridge, residual, and guard fields",
            "valid_for_claim": False,
            "generated_utc": RUN_UTC,
        },
        {
            "validation_id": "VAL2922_5_refusal_runner_safe",
            "status": any(row["runner_status"] == "REJECT_CIRCULAR_NEWTON_IMPORT" for row in refusal_rows)
            and any(row["runner_status"] == "ACCEPTED_AS_NONCLAIM_SMOKE_NOT_SOURCE_MASS_PROOF" for row in refusal_rows)
            and all(not bool(row["valid_for_claim"]) for row in refusal_rows),
            "detail": "runner rejects circular/closure rows and keeps finite smoke nonclaim",
            "valid_for_claim": False,
            "generated_utc": RUN_UTC,
        },
        {
            "validation_id": "VAL2922_6_prior_endpoint_imported",
            "status": {"1018", "1021", "1024", "1105", "1237", "1238", "1249", "2921"}.issubset({row["prior_checkpoint"] for row in crosswalk_rows}),
            "detail": "prior endpoint crosswalk imported to avoid re-circling",
            "valid_for_claim": False,
            "generated_utc": RUN_UTC,
        },
        {
            "validation_id": "VAL2922_7_claim_gates_safe",
            "status": all(not bool(row["gate_pass"]) or row["gate_id"] == "CG2922_5_no_circling" for row in claim_rows_)
            and all(not bool(row["valid_for_claim"]) for row in claim_rows_),
            "detail": "no physics claim gate is open",
            "valid_for_claim": False,
            "generated_utc": RUN_UTC,
        },
        {
            "validation_id": "VAL2922_8_next_target_selected",
            "status": any(row["route_id"] == "NEXT2922_0_2923" for row in next_rows_),
            "detail": "2923 first source-mass row/Hcore checklist target selected",
            "valid_for_claim": False,
            "generated_utc": RUN_UTC,
        },
        {
            "validation_id": "VAL2922_9_branch_copies_parse",
            "status": all(bool(row["destination_exists"]) and bool(row["destination_parses"]) for row in branch_rows_),
            "detail": "branch copies exist and parse",
            "valid_for_claim": False,
            "generated_utc": RUN_UTC,
        },
        {
            "validation_id": "VAL2922_10_no_formalization_outputs",
            "status": not any(is_under(path, FORMALIZATION) for path in list(OUTPUTS.values()) + list(BRANCH_OUTPUTS.values()) + [DOC]),
            "detail": "no generated output path is inside formalization-workbench",
            "valid_for_claim": False,
            "generated_utc": RUN_UTC,
        },
        {
            "validation_id": "VAL2922_11_doc_written",
            "status": DOC.exists() if include_doc_check else True,
            "detail": "markdown checkpoint exists",
            "valid_for_claim": False,
            "generated_utc": RUN_UTC,
        },
    ]
    rows.append(
        {
            "validation_id": "VAL2922_OVERALL",
            "status": all(bool(row["status"]) for row in rows),
            "detail": "2922 validation overall",
            "valid_for_claim": False,
            "generated_utc": RUN_UTC,
        }
    )
    return rows


def write_doc(
    source_rows: list[dict[str, Any]],
    owner_rows: list[dict[str, Any]],
    schema_rows: list[dict[str, Any]],
    refusal_rows: list[dict[str, Any]],
    crosswalk_rows: list[dict[str, Any]],
    claim_rows_: list[dict[str, Any]],
    decision_rows_: list[dict[str, Any]],
    next_rows_: list[dict[str, Any]],
    branch_rows_: list[dict[str, Any]],
    validation_rows_: list[dict[str, Any]],
) -> None:
    overall = next(row for row in validation_rows_ if row["validation_id"] == "VAL2922_OVERALL")
    text = f"""# 2922 - Y5/R2FR Hamiltonian Sector Owner Or Source-Mass First Row Under AX1090

Status: `Y5_R2FR_2922_owner_theorem_not_derived_source_mass_first_row_template_2923_next`

Claim ceiling: `owner_map_yes_parent_owner_no_first_row_schema_yes_no_source_mass_no_Newton_no_beta_no_local_GR_no_GitHub_claim`

Generated UTC: `{RUN_UTC}`

## Summary

2922 attacks the owner/source-row bottleneck identified by 2921. The target object is:

`M_H := G_ref^-1[H_tau - H_ref] = G_ref^-1 integral_S Q_tau^MTS`

in the same observed source/orbit frame, with a fixed reference, positive `M_H_ref`, parent-owned `Pi_M^H`, and a Poisson/Gauss/orbital bridge that does not import orbital `GM` as the denominator.

The result is disciplined but not promotional. The owner theorem is not derived. The current corpus has a sharp owner map, a deep prior source hunt, and nonclaim finite-runner discipline, but it does not supply one parent-signed package containing `L_X`, `Theta_X`, `Q_X`, `B_ref`, `B_class`, `tau`, `M_H_ref`, `Pi_M^H`, and hidden-visible coefficient exclusion.

So 2922 stages the exact source-mass first-row schema and a refusal runner. Circular rows, closure-zero rows, and rows that use orbital `GM` before the bridge are rejected. The 1249 finite `q_R_hat` row is allowed only as nonclaim smoke, not as a theory prediction or source-mass proof.

## Source Register

{md_table(source_rows, ["source_id", "source_path", "anchors_found", "role", "missing_anchors"])}

## Hamiltonian Sector-Owner Audit

{md_table(owner_rows, ["audit_id", "owner_clause", "math_form", "current_status", "why_it_matters", "clause_passed", "valid_for_claim"])}

## Source-Mass First-Row Schema

{md_table(schema_rows, ["schema_id", "row_object", "required_columns", "current_status", "purpose", "valid_for_claim"])}

## First-Row Refusal Runner

{md_table(refusal_rows, ["runner_id", "candidate_id", "trigger", "runner_status", "runner_eligible", "valid_for_claim"])}

## Prior Chain Endpoint Crosswalk

{md_table(crosswalk_rows, ["crosswalk_id", "prior_checkpoint", "resolved", "usable_gain", "remaining_blocker", "2922_use", "valid_for_claim"])}

## Claim Gates

{md_table(claim_rows_, ["gate_id", "claim", "gate_status", "reason", "gate_pass", "valid_for_claim"])}

## Decision Ledger

{md_table(decision_rows_, ["decision_id", "decision", "because", "next_action", "valid_for_claim"])}

## Next Target

{md_table(next_rows_, ["route_id", "selection_status", "target_file", "target_script", "task", "success_condition", "fallback_condition", "valid_for_claim"])}

## Branch Copies

{md_table(branch_rows_, ["copy_id", "source_path", "destination_path", "destination_exists", "destination_parses", "valid_for_claim"])}

## Validation

{md_table(validation_rows_, ["validation_id", "status", "detail", "valid_for_claim"])}

Validation overall: `{overall["status"]}`.

## Interpretation

This is the honest local-GR position after the source-mass audit: the bridge from Hamiltonian charge to Newtonian `GM` is usable, but the parent object that should sit inside the bridge is still not owned. That means local GR is not dead; it is bottlenecked on a concrete parent-action row.

The useful next move is not another verbal theorem attempt. It is a strict row/checklist that can accept a real `H_core/Q_tau/M_H_ref` coefficient if one is derived, or a finite nonclaim source row if the theory must go empirical at this gate.

## Not Claimed

- no Hamiltonian sector-owner theorem is claimed;
- no source-mass first row is claim-grade;
- no finite `q_R_hat` row is promoted beyond nonclaim smoke;
- no source-normalized Newton, beta, PPN, R10, WEP, clock, orbital, or local-GR pass is claimed;
- no closure benchmark is treated as derivation;
- no file in `formalization-workbench` is modified by this checkpoint;
- no public/GitHub action is implied.
"""
    DOC.write_text(text, encoding="utf-8")


def main() -> None:
    source_rows = source_register_rows()
    owner_rows = owner_audit_rows()
    schema_rows = first_row_schema_rows()
    refusal_rows = refusal_runner_rows()
    crosswalk_rows = endpoint_crosswalk_rows()
    claim_rows_ = claim_rows()
    decision_rows_ = decision_rows()
    next_rows_ = next_rows()

    write_csv(OUTPUTS["sources"], source_rows)
    write_csv(OUTPUTS["owner_audit"], owner_rows)
    write_csv(OUTPUTS["first_row_schema"], schema_rows)
    write_csv(OUTPUTS["refusal_runner"], refusal_rows)
    write_csv(OUTPUTS["endpoint_crosswalk"], crosswalk_rows)
    write_csv(OUTPUTS["claims"], claim_rows_)
    write_csv(OUTPUTS["decision"], decision_rows_)
    write_csv(OUTPUTS["next"], next_rows_)

    branch_rows_ = branch_rows()
    write_csv(OUTPUTS["branches"], branch_rows_)

    validation_rows_ = validation_rows(
        source_rows,
        owner_rows,
        schema_rows,
        refusal_rows,
        crosswalk_rows,
        claim_rows_,
        next_rows_,
        branch_rows_,
        include_doc_check=False,
    )
    write_csv(OUTPUTS["validation"], validation_rows_)
    write_doc(
        source_rows,
        owner_rows,
        schema_rows,
        refusal_rows,
        crosswalk_rows,
        claim_rows_,
        decision_rows_,
        next_rows_,
        branch_rows_,
        validation_rows_,
    )

    validation_rows_ = validation_rows(
        source_rows,
        owner_rows,
        schema_rows,
        refusal_rows,
        crosswalk_rows,
        claim_rows_,
        next_rows_,
        branch_rows_,
        include_doc_check=True,
    )
    write_csv(OUTPUTS["validation"], validation_rows_)
    write_doc(
        source_rows,
        owner_rows,
        schema_rows,
        refusal_rows,
        crosswalk_rows,
        claim_rows_,
        decision_rows_,
        next_rows_,
        branch_rows_,
        validation_rows_,
    )

    overall = next(row for row in validation_rows_ if row["validation_id"] == "VAL2922_OVERALL")
    if not bool(overall["status"]):
        raise SystemExit(1)


if __name__ == "__main__":
    main()

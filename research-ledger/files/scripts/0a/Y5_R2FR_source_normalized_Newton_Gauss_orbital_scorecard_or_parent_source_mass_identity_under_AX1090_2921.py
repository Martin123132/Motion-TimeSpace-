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

CHECKPOINT = "2921"
BRANCH_ID = "MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428"
RUN_UTC = SCRIPT_START_UTC.isoformat()

DOC = ROOT / "2921-Y5-R2FR-source-normalized-Newton-Gauss-orbital-scorecard-or-parent-source-mass-identity-under-AX1090.md"

SRC_2920_DOC = ROOT / "2920-Y5-R2FR-beta-source-normalization-second-order-kernel-or-parent-square-law-under-AX1090.md"
SRC_2920_NEXT = RESIDUALS / "P8_Y5_R2FR_2920_NEXT_TARGET.csv"
SRC_2920_QUEUE = RESIDUALS / "P8_Y5_R2FR_2920_SOURCE_NORMALIZED_NEWTON_GAUSS_ORBITAL_SCORECARD_QUEUE.csv"
SRC_458_DOC = ROOT / "458-Hamiltonian-charge-to-Poisson-Gauss-calibration-gate.md"
SRC_PG_CONTRACT = RESIDUALS / "P8_Hamiltonian_charge_Poisson_Gauss_calibration_CONTRACT.csv"
SRC_CC_DIRECT = RESIDUALS / "P8_charge_current_equality_DIRECT_ATTEMPT.csv"
SRC_CC_RESIDUAL = RESIDUALS / "P8_charge_current_equality_RESIDUAL_DECOMPOSITION.csv"
SRC_MEFF_FLUX = RESIDUALS / "P8_SOURCE_MEASURE_MEFF_FLUX_THEOREM.csv"
SRC_PIM_ALGEBRA = RESIDUALS / "P8_PiM_parent_symplectic_projector_algebra_CONTRACT.csv"
SRC_PIM_FLUX = RESIDUALS / "P8_PiM_flux_closure_Ward_topological_CONTRACT.csv"
SRC_CONSTANT_GM = RESIDUALS / "P8_CONSTANT_GM_ZERO_THEOREM_ATTEMPT.csv"
SRC_BOUND_MATRIX = RESIDUALS / "P8_CONSTANT_GM_RESIDUAL_BOUND_MATRIX.csv"
SRC_PG_MAP = RESIDUALS / "P8_PG_calibration_residual_MAP.csv"
SRC_PG_TEMPLATE = RESIDUALS / "P8_PG_calibration_residual_INPUT_TEMPLATE.csv"
SRC_1012_DOC = ROOT / "1012-Y5-R10-Y5-source-normalization-owner-or-q_loc-bound-implementation.md"
SRC_1013_DOC = ROOT / "1013-Y5-R10-PiM-JH-flux-closure-or-measured-GM-obstruction-score.md"
SRC_1015_DOC = ROOT / "1015-Y5-R10-topological-Hilbert-equality-or-R_eq-bound-runner.md"
SRC_1016_DOC = ROOT / "1016-Y5-R10-parent-worldtube-source-measure-selector-or-R_eq-first-input.md"
SRC_1017_DOC = ROOT / "1017-Y5-R10-Hamiltonian-PiM-reference-lock-or-MHref-first-row.md"
SRC_1018_DOC = ROOT / "1018-Y5-R10-sector-Lagrangian-boundary-owner-or-FB5540-source-row.md"
SRC_1019_DOC = ROOT / "1019-Y5-R10-boundary-exactness-projector-orthogonality-or-source-pack.md"
SRC_1020_DOC = ROOT / "1020-Y5-R10-boundary-cohomology-domain-certificate-or-source-pack-first-row.md"

OUTPUTS = {
    "sources": RESIDUALS / "P8_Y5_R2FR_2921_SOURCE_REGISTER.csv",
    "identity_audit": RESIDUALS / "P8_Y5_R2FR_2921_PARENT_SOURCE_MASS_IDENTITY_AUDIT.csv",
    "pg_bridge": RESIDUALS / "P8_Y5_R2FR_2921_POISSON_GAUSS_ORBITAL_BRIDGE_AUDIT.csv",
    "scorecard": RESIDUALS / "P8_Y5_R2FR_2921_SOURCE_NORMALIZED_NEWTON_SCORECARD_ROWS.csv",
    "crosswalk": RESIDUALS / "P8_Y5_R2FR_2921_PRIOR_HUNT_CROSSWALK.csv",
    "claims": RESIDUALS / "P8_Y5_R2FR_2921_CLAIM_GATES.csv",
    "decision": RESIDUALS / "P8_Y5_R2FR_2921_DECISION_LEDGER.csv",
    "next": RESIDUALS / "P8_Y5_R2FR_2921_NEXT_TARGET.csv",
    "branches": RESIDUALS / "P8_Y5_R2FR_2921_BRANCH_COPIES.csv",
    "validation": RESIDUALS / "P8_Y5_BRR545_2921_VALIDATION.csv",
}

BRANCH_OUTPUTS = {
    "identity_copy": PARENT_ACTION / "Parent_source_mass_identity_audit_2921_NONCLAIM.csv",
    "scorecard_copy": LOCAL_BOUNDS / "Source_normalized_Newton_scorecard_2921_NONCLAIM.csv",
    "next_copy": RAB_QUEUE / "JR2921_HAMILTONIAN_SECTOR_OWNER_OR_SOURCE_MASS_FIRST_ROW_NEXT_NONCLAIM.csv",
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
        ("SRC2921_00_2920_doc", SRC_2920_DOC, "mu_obs = G0 M_H;Validation overall", "2920 selected source-normalized Newton/Gauss/orbital identity as beta prerequisite"),
        ("SRC2921_01_2920_next", SRC_2920_NEXT, "NEXT2920_0_2921;mu_obs=G0 M_H", "machine-readable 2921 target"),
        ("SRC2921_02_2920_queue", SRC_2920_QUEUE, "NGQ2920_0_parent_source_mass_identity;NGQ2920_5_scorecard_verdict", "2920 Newton/Gauss/orbital queue"),
        ("SRC2921_03_458_doc", SRC_458_DOC, "conditional_Poisson_Gauss_calibration_theorem;current_corpus_status", "earlier Hamiltonian to Poisson/Gauss calibration gate"),
        ("SRC2921_04_PG_contract", SRC_PG_CONTRACT, "PG0_Hamiltonian_charge_input;PG10_retained_residual_fallback", "Poisson/Gauss contract rows"),
        ("SRC2921_05_CC_direct", SRC_CC_DIRECT, "CC7_closed_flux_and_Gauss_calibration;CC8_second_order_limit", "direct charge-current equality attempt"),
        ("SRC2921_06_CC_residual", SRC_CC_RESIDUAL, "Delta_cal;Delta_PPN", "charge-current residual decomposition"),
        ("SRC2921_07_Meff_flux", SRC_MEFF_FLUX, "T509_0_charge_identity_needed;T509_2_no_extra_mass_channel", "M_eff/source-measure flux theorem attempt"),
        ("SRC2921_08_PiM_algebra", SRC_PIM_ALGEBRA, "PM6_flux_closure_requires_Ward_or_Euler;PM7_absolute_calibration_deferred", "Pi_M parent symplectic projector algebra contract"),
        ("SRC2921_09_PiM_flux", SRC_PIM_FLUX, "FC2_closed_mass_current_equation;FC7_absolute_calibration_after_closure", "Pi_M flux closure/Ward/topological contract"),
        ("SRC2921_10_constant_GM", SRC_CONSTANT_GM, "Z0_decomposition_identity;Z8_second_order_source_stability", "constant measured-GM theorem attempt"),
        ("SRC2921_11_bound_matrix", SRC_BOUND_MATRIX, "P8_Meff_conservation;P8_nonlinear_beta_source_residue", "source-normalization residual bound matrix"),
        ("SRC2921_12_PG_map", SRC_PG_MAP, "PG4_Gauss_surface_integral;PG10_retained_residual_fallback", "Poisson/Gauss residual map"),
        ("SRC2921_13_PG_template", SRC_PG_TEMPLATE, "P8_Geff_time_drift;R11_EH_operator_ledger", "Poisson/Gauss scorecard input template"),
        ("SRC2921_14_1012_doc", SRC_1012_DOC, "DEC1012_0_owner_not_proved;DEC1012_2_next_root", "prior source-normalization owner checkpoint"),
        ("SRC2921_15_1013_doc", SRC_1013_DOC, "PFC1013_8_verdict;DEC1013_0_exact_obstruction_is_best_object", "prior Pi_M flux obstruction checkpoint"),
        ("SRC2921_16_1015_doc", SRC_1015_DOC, "SOL1015_6_verdict;DEC1015_0_conditional_lemma", "prior topological-Hilbert same-object lemma"),
        ("SRC2921_17_1016_doc", SRC_1016_DOC, "PSC1016_6_PiM_Hamiltonian_map;PST1016_5_verdict", "prior parent worldtube/source-measure selector checkpoint"),
        ("SRC2921_18_1017_doc", SRC_1017_DOC, "HRL1017_5_MHref_denominator;DEC1017_0_reference_lock", "prior Hamiltonian reference/MHref lock checkpoint"),
        ("SRC2921_19_1018_doc", SRC_1018_DOC, "LOC1018_8_verdict;DEC1018_0_owner_result", "prior sector Lagrangian/boundary owner checkpoint"),
        ("SRC2921_20_1019_doc", SRC_1019_DOC, "BE1019_1_BX_exact;PO1019_5_verdict", "prior boundary exactness/projector orthogonality checkpoint"),
        ("SRC2921_21_1020_doc", SRC_1020_DOC, "BDC1020_0_surface_manifold;DEC1020_1_best_next_route", "prior boundary cohomology/weighted-Stokes checkpoint"),
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


def identity_audit_rows() -> list[dict[str, Any]]:
    specs = [
        (
            "PSM2921_0_target_identity",
            "target local Newton source-mass identity",
            "mu_obs = G0 M_H = G_eff M_source_parent",
            "TARGET_DEFINED_NOT_PROVED",
            "this is the first-order identity needed before beta/source-normalization can be scored",
            False,
        ),
        (
            "PSM2921_1_conditional_bridge",
            "Hamiltonian charge to Poisson/Gauss/orbital bridge",
            "if B_xi=G_eff M_H, nabla^2 Phi=4 pi G_eff rho_H, surface_integral grad Phi dS=4 pi G_eff M_H, and a=-grad Phi, then mu_obs=G_eff M_H",
            "VALID_CONDITIONAL_THEOREM_FROM_458",
            "the algebraic bridge is clean, but its premises are not parent-signed",
            True,
        ),
        (
            "PSM2921_2_observed_time_charge",
            "well-defined observed-time Hamiltonian/boundary charge",
            "H_xi=B_xi on shell with xi=partial_t_obs and fixed normalization",
            "CONDITIONAL_NOT_PARENT_DERIVED",
            "without this, the charge can be a formal diffeomorphism charge, not measured mass",
            False,
        ),
        (
            "PSM2921_3_projected_Hilbert_source",
            "charge equals parent projected Hilbert mass current",
            "B_xi/G_eff = M_eff[Pi_M J_H]",
            "NOT_PARENT_DERIVED",
            "old Pi_M may be a readout mask unless Pi_M^H is parent-owned before orbital fitting",
            False,
        ),
        (
            "PSM2921_4_flux_closure",
            "projected Hilbert mass flux closed in compact exterior",
            "d(Pi_M J_H)=0 or exact obstruction -Pi_M dJ_extra + [d,Pi_M]J_H + A_parent is zero/bounded",
            "EXACT_OBSTRUCTION_ACTIVE",
            "1013 shows the product-rule obstruction; closure is not delivered by projector algebra alone",
            False,
        ),
        (
            "PSM2921_5_same_object_lemma",
            "topological/Hilbert current represents the same compact source worldtube class",
            "Pi_M J_H = J_M_top + dB_zero + R_eq with R_eq=0 only after same-class source-worldtube clauses",
            "CONDITIONAL_LEMMA_ONLY",
            "topology can conserve the wrong object unless the source worldtube/class is parent-signed",
            False,
        ),
        (
            "PSM2921_6_MHref_reference_lock",
            "positive same-frame Hamiltonian source denominator and fixed reference",
            "M_H_ref = G_ref^-1 integral_S Q_tau^MTS with same tau, surface, and observed frame",
            "FAIL_CURRENT_CLAIM",
            "1017 keeps H_tau integrability, fixed H_ref, tau lock, and M_H_ref open",
            False,
        ),
        (
            "PSM2921_7_zero_extra_source_channels",
            "no boundary/bulk/domain/memory/range/frame/non-EH mass channel",
            "mu_obs = G_eff M_eff + mu_extra with mu_extra=0 and S_res=0",
            "MISSING_COMPONENT_VALUES_OR_THEOREM_ZERO",
            "unowned mass-channel charge would become real measured-GM correction",
            False,
        ),
        (
            "PSM2921_8_derivative_silence",
            "measured source strength has no time/range/radial/species/frame/domain derivative",
            "partial_t,r,A,lambda,frame,domain mu_obs = 0",
            "MISSING_DERIVATIVE_HAIR_ZERO",
            "constant-GM residual rows remain unfilled",
            False,
        ),
        (
            "PSM2921_9_second_order_stability",
            "first-order source identity survives PPN beta/gamma order",
            "delta_beta_source=0 and gamma-1=0 after measured-GM normalization",
            "DEFERRED_UNTIL_FIRST_ORDER_SCORECARD_CLOSES",
            "2920 beta square-law cannot be scored before the source identity is owned",
            False,
        ),
        (
            "PSM2921_10_verdict",
            "current parent source-mass identity",
            "mu_obs = G0 M_H from current corpus",
            "PARENT_SOURCE_MASS_IDENTITY_NOT_DERIVED_SCORECARD_STAGED",
            "use the prior source hunt; do not re-circle the same gate as if new",
            False,
        ),
    ]
    return [
        add_common(
            {
                "audit_id": audit_id,
                "clause": clause,
                "math_form": math_form,
                "current_status": status,
                "meaning": meaning,
                "clause_passed": passed,
                "source_paths": f"{SRC_458_DOC};{SRC_CC_DIRECT};{SRC_1013_DOC};{SRC_1017_DOC};{SRC_2920_DOC}",
            }
        )
        for audit_id, clause, math_form, status, meaning, passed in specs
    ]


def pg_bridge_rows() -> list[dict[str, Any]]:
    specs = [
        ("PG2921_0_Hamiltonian_charge_input", "PG0", "H_xi=B_xi on shell with observed-time normalization", "CONDITIONAL_FROM_PRIOR_NOT_PARENT_DERIVED", "derive observed-time Hamiltonian charge or retain charge residuals"),
        ("PG2921_1_charge_equals_projected_source", "PG1", "B_xi/G_eff = M_eff[Pi_M J_H]", "NOT_PARENT_DERIVED", "parent-own Pi_M^H and source-current equality"),
        ("PG2921_2_same_frame_potential", "PG2", "g_00=-1+2 Phi/c^2 and a=-grad Phi in observed matter frame", "CONDITIONAL_NOT_PARENT_DERIVED", "same-frame metric/matter/coframe theorem tied to source variation"),
        ("PG2921_3_Poisson_coefficient", "PG3", "nabla^2 Phi = (kappa_eff c^4/2) rho_H = 4 pi G_eff rho_H", "CONDITIONAL_FROM_EH_ONLY_PREMISES", "EH/no-hair or R11 coefficient vector"),
        ("PG2921_4_Gauss_surface", "PG4", "surface_integral grad Phi dot dS = 4 pi G_eff M_eff", "NOT_PARENT_DERIVED", "closed Pi_M flux plus zero boundary/source residuals"),
        ("PG2921_5_orbital_readout", "PG5", "a_r=-G_eff M_eff/r^2 and v^2 r=G_eff M_eff", "NOT_PARENT_DERIVED", "slow-particle geodesic plus no fifth-force/source/radial/frame hair"),
        ("PG2921_6_zero_residual_source", "PG6", "mu_extra=0 and S_res=0", "MISSING_COMPONENT_VALUES_OR_THEOREM_ZERO", "component coefficient rows or parent no-extra-source theorem"),
        ("PG2921_7_constant_Geff", "PG7", "partial_t,r,A,lambda,frame G_eff=0", "NOT_PARENT_DERIVED", "constant universal coupling theorem or drift rows"),
        ("PG2921_8_no_derivative_hair", "PG8", "partial_t,r,A,lambda,frame mu_obs=0", "NOT_PARENT_DERIVED", "Gdot/Mdot/WEP/R10/radial/frame rows"),
        ("PG2921_9_second_order_stability", "PG9", "delta_beta_source=0 and gamma-1=0", "DEFERRED_UNTIL_SOURCE_IDENTITY", "return to beta square-law after first-order source identity"),
        ("PG2921_10_residual_fallback", "PG10", "failed PG row maps to executable residual data", "PASS_GUARDRAIL", "keep all failed premises as scorecard rows, not prose debt"),
    ]
    return [
        add_common(
            {
                "bridge_id": bridge_id,
                "contract_row": contract_row,
                "required_identity": identity,
                "current_status": status,
                "next_requirement": requirement,
                "source_paths": f"{SRC_PG_CONTRACT};{SRC_PG_MAP};{SRC_458_DOC}",
            }
        )
        for bridge_id, contract_row, identity, status, requirement in specs
    ]


def scorecard_rows() -> list[dict[str, Any]]:
    specs = [
        ("SN2921_0_dln_Geff_dt", "P8_Geff_time_drift", "dln_Geff_dt", "yr^-1", "Gdot_over_G", "9.6e-15 yr^-1 or derived zero", "MISSING_NUMERIC_OR_THEOREM_ZERO"),
        ("SN2921_1_dln_Meff_dt", "P8_Meff_conservation", "dln_Meff_dt", "yr^-1", "beta_minus_1;Gdot_over_G", "derived conservation or decomposed bound", "MISSING_MASS_FLUX_CLOSURE_OR_DRIFT_ROW"),
        ("SN2921_2_eta_source_AB", "P8_species_source_charge", "eta_source_AB", "dimensionless", "eta_WEP_source_charge", "2.8e-15 or derived universal source charge", "MISSING_SOURCE_CHARGE_UNIVERSALITY"),
        ("SN2921_3_alpha_lambda", "P8_range_dependence", "alpha(lambda)", "range-dependent", "delta_G_or_fifth_force_yukawa", "verified alpha(lambda) curve or derived zero", "MISSING_RANGE_CURVE_OR_NO_RANGE_THEOREM"),
        ("SN2921_4_radial_hair", "P8_radial_source_hair", "partial_r_ln_mu_obs", "inverse_length_or_dimensionless_envelope", "gamma_minus_1;beta_minus_1;alpha(lambda)", "zero radial hair or mapped bound", "MISSING_RADIAL_PROFILE_OR_THEOREM_ZERO"),
        ("SN2921_5_mu_extra", "P8_boundary_bulk_domain_mu_extra", "mu_extra_boundary_bulk_domain", "dimensionless_or_GM_units_after_normalization", "gamma;beta;alpha3;xi;Gdot", "zero owned exchange or component locks", "MISSING_MU_EXTRA_COMPONENT_VECTOR"),
        ("SN2921_6_frame_split", "P8_frame_calibration_split", "delta_frame_source", "dimensionless", "eta_WEP_direct_geometry;clock;orbital", "one observed frame or row locks", "MISSING_SOURCE_FRAME_PULLBACK"),
        ("SN2921_7_delta_beta_source", "P8_nonlinear_beta_source_residue", "delta_beta_source", "dimensionless", "beta_minus_1", "7.8e-05 or derived zero", "MISSING_B_SOURCE_A_SOURCE_SQUARE_LAW"),
        ("SN2921_8_R11_operator", "R11_EH_operator_ledger", "c_nonEH_operator_vector", "operator family", "operator_ledger;gamma;beta;preferred_frame;fifth_force", "EH-only theorem-zero or executable coefficient vector", "MISSING_R11_OPERATOR_VECTOR_OR_EH_NOHAIR"),
        ("SN2921_9_total_guard", "source_normalized_Newton_total", "Delta_SN_total_abs", "dimensionless_or_component_units", "Newton;PPN;R10;WEP;Gdot", "all components theorem-zero or source-backed under their locks", "TOTAL_SOURCE_NORMALIZED_NEWTON_NOT_SCORE_READY"),
    ]
    return [
        add_common(
            {
                "scorecard_id": scorecard_id,
                "component_id": component_id,
                "symbol": symbol,
                "units": units,
                "observable_link": observable_link,
                "bound_or_target": bound,
                "current_status": status,
                "source_paths": f"{SRC_BOUND_MATRIX};{SRC_PG_TEMPLATE};{SRC_PG_MAP};{SRC_CC_RESIDUAL}",
                "next_requirement": "derive theorem-zero or fill numeric/source-backed row with normalization and units",
            }
        )
        for scorecard_id, component_id, symbol, units, observable_link, bound, status in specs
    ]


def crosswalk_rows() -> list[dict[str, Any]]:
    specs = [
        ("XW2921_0_458", "458", "conditional Poisson/Gauss/orbital bridge written", "algebra clean but parent premises not derived", "do not use orbital GM to prove source mass"),
        ("XW2921_1_1012", "1012", "source-normalization owner theorem failed", "Pi_M origin, flux closure, worldtube glue, universal G, and mu_extra channels open", "route moved to Pi_M J_H flux"),
        ("XW2921_2_1013", "1013", "exact Pi_M J_H flux obstruction written", "-Pi_M dJ_extra + [d,Pi_M]J_H + A_parent remains active", "commutator/projector variation became root"),
        ("XW2921_3_1015", "1015", "de Rham same-object lemma written", "conditional only; same compact source-worldtube class not parent-signed", "worldtube/source-measure selector became root"),
        ("XW2921_4_1016", "1016", "parent worldtube/source-measure selector contract written", "Pi_M^H candidate not adopted; coupling/readout descent unsigned", "Hamiltonian reference/MHref lock became root"),
        ("XW2921_5_1017", "1017", "H_tau reference/MHref lock split", "M_H_ref denominator fails without integrability/reference/tau/source readout", "sector Lagrangian/boundary owners became root"),
        ("XW2921_6_1018", "1018", "L_X/Theta_X/Q_X owner map explicit", "owner route sharp but no L_X/no-pole/source-row closure", "boundary exactness/projector/source pack became root"),
        ("XW2921_7_1019", "1019", "boundary exactness and projector orthogonality fork written", "neither fork parent-signed; source pack missing", "boundary cohomology/domain certificate became root"),
        ("XW2921_8_1020", "1020", "weighted-Stokes boundary route sharpened", "explicit B_X primitive/cohomology/kernel terms missing", "B_X primitive or first source row remains live"),
        ("XW2921_9_2920", "2920", "beta square-law needs source-normalized Newton first", "B_source=A_source^2 cannot be scored until mu_obs=G0 M_H branch is owned", "do not circle; jump to Hamiltonian sector owner/source row"),
    ]
    return [
        add_common(
            {
                "crosswalk_id": crosswalk_id,
                "prior_checkpoint": prior,
                "what_it_resolved": resolved,
                "what_remains": remains,
                "2921_use": use,
            }
        )
        for crosswalk_id, prior, resolved, remains, use in specs
    ]


def claim_rows() -> list[dict[str, Any]]:
    specs = [
        ("CG2921_0_parent_source_mass", "mu_obs=G0 M_H is parent-derived", "BLOCKED_NONCLAIM", "conditional bridge exists but source-current/Hamiltonian/PiM/reference premises are unsigned", False),
        ("CG2921_1_source_normalized_Newton", "source-normalized Newton/Gauss/orbital precondition passes", "BLOCKED_NONCLAIM", "PG0-PG9 are not all closed and scorecard rows remain missing", False),
        ("CG2921_2_beta_reopen", "beta square-law can now be scored", "BLOCKED_NONCLAIM", "first-order source identity and derivative silence are not owned", False),
        ("CG2921_3_local_GR", "local GR/Newton reduction follows", "BLOCKED_NONCLAIM", "source mass, beta, R11, boundary/domain/readout, and alpha3 heads remain open", False),
        ("CG2921_4_anti_circling", "2921 repeats old work without advancing", "PASS_GUARDRAIL", "prior 458/1012-1020 hunt is imported and deepest unresolved owner row is selected", False),
        ("CG2921_5_public_or_github", "public/GitHub claim can be made from 2921", "BLOCKED_NONCLAIM", "private checkpoint only", False),
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
            "DEC2921_0_bridge_result",
            "retain the Hamiltonian-to-Poisson/Gauss/orbital bridge as conditional theorem",
            "the algebra is clean: if the same parent source charge feeds Poisson and orbits with no residuals, then mu_obs=G_eff M_H",
            "do not count it as current MTS proof until the premises close",
        ),
        (
            "DEC2921_1_identity_result",
            "do not claim parent source-mass identity",
            "Pi_M/Hamiltonian source measure, flux closure, M_H_ref/reference lock, and residual-source silence remain unsigned",
            "keep source-normalized Newton as nonclaim scorecard",
        ),
        (
            "DEC2921_2_no_circling",
            "reuse the old deep source hunt instead of restarting it",
            "458 and 1012-1020 already show the live root is sector Hamiltonian/boundary ownership and first source rows",
            "next target should attack owner/source-row input, not restate PG0-PG10",
        ),
        (
            "DEC2921_3_next",
            "select Hamiltonian sector owner or source-mass first-row target",
            "without L_X/Theta_X/Q_X/B_ref/B_class/tau/M_H_ref ownership, source-mass rows cannot become scoreable",
            "2922 should derive the missing owners or stage the first source-backed nonclaim row",
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
                "route_id": "NEXT2921_0_2922",
                "selection_status": "selected_primary",
                "target_file": "2922-Y5-R2FR-Hamiltonian-sector-owner-or-source-mass-first-row-under-AX1090.md",
                "target_script": "scripts/Y5_R2FR_Hamiltonian_sector_owner_or_source_mass_first_row_under_AX1090_2922.py",
                "task": "derive L_X/Theta_X/Q_X/B_ref/B_class/tau/M_H_ref ownership enough to define the same-frame parent source mass, or stage the first source-backed nonclaim source-mass row",
                "success_condition": "observed-time Hamiltonian charge, fixed reference, positive M_H_ref, Pi_M^H source projector, and Poisson/Gauss/orbital denominator are parent-signed; otherwise first row has units/source path and valid_for_claim=false",
                "fallback_condition": "keep source-normalized Newton nonclaim and fill FB5540/boundary/source-pack component rows with no cancellation credit",
            }
        )
    ]


def branch_rows() -> list[dict[str, Any]]:
    copies = [
        ("identity_copy", OUTPUTS["identity_audit"], BRANCH_OUTPUTS["identity_copy"]),
        ("scorecard_copy", OUTPUTS["scorecard"], BRANCH_OUTPUTS["scorecard_copy"]),
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
    identity_rows: list[dict[str, Any]],
    pg_rows: list[dict[str, Any]],
    scorecard_rows_: list[dict[str, Any]],
    crosswalk_rows_: list[dict[str, Any]],
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
            "validation_id": "VAL2921_0_source_paths_exist",
            "status": all(bool(row["path_exists"]) for row in source_rows),
            "detail": "all cited source paths exist",
            "valid_for_claim": False,
            "generated_utc": RUN_UTC,
        },
        {
            "validation_id": "VAL2921_1_source_anchors_found",
            "status": all(bool(row["anchors_found"]) for row in source_rows),
            "detail": "all source anchors found",
            "valid_for_claim": False,
            "generated_utc": RUN_UTC,
        },
        {
            "validation_id": "VAL2921_2_csv_outputs_parse",
            "status": all(csv_parses(path) for path in generated_csvs),
            "detail": "generated CSV outputs parse cleanly",
            "valid_for_claim": False,
            "generated_utc": RUN_UTC,
        },
        {
            "validation_id": "VAL2921_3_conditional_bridge_retained",
            "status": any(row["audit_id"] == "PSM2921_1_conditional_bridge" and bool(row["clause_passed"]) for row in identity_rows),
            "detail": "conditional Hamiltonian-to-Poisson/Gauss bridge retained",
            "valid_for_claim": False,
            "generated_utc": RUN_UTC,
        },
        {
            "validation_id": "VAL2921_4_identity_not_claimed",
            "status": any(row["audit_id"] == "PSM2921_10_verdict" and "NOT_DERIVED" in row["current_status"] for row in identity_rows),
            "detail": "parent source-mass identity remains unproved",
            "valid_for_claim": False,
            "generated_utc": RUN_UTC,
        },
        {
            "validation_id": "VAL2921_5_pg_contract_complete",
            "status": {row["contract_row"] for row in pg_rows} == {f"PG{i}" for i in range(11)},
            "detail": "PG0-PG10 bridge rows are represented",
            "valid_for_claim": False,
            "generated_utc": RUN_UTC,
        },
        {
            "validation_id": "VAL2921_6_scorecard_complete",
            "status": {row["component_id"] for row in scorecard_rows_}
            == {
                "P8_Geff_time_drift",
                "P8_Meff_conservation",
                "P8_species_source_charge",
                "P8_range_dependence",
                "P8_radial_source_hair",
                "P8_boundary_bulk_domain_mu_extra",
                "P8_frame_calibration_split",
                "P8_nonlinear_beta_source_residue",
                "R11_EH_operator_ledger",
                "source_normalized_Newton_total",
            },
            "detail": "source-normalized Newton scorecard rows are complete",
            "valid_for_claim": False,
            "generated_utc": RUN_UTC,
        },
        {
            "validation_id": "VAL2921_7_prior_hunt_imported",
            "status": len(crosswalk_rows_) >= 10 and any(row["prior_checkpoint"] == "1020" for row in crosswalk_rows_),
            "detail": "prior 458/1012-1020 source hunt is imported to avoid circling",
            "valid_for_claim": False,
            "generated_utc": RUN_UTC,
        },
        {
            "validation_id": "VAL2921_8_claim_gates_safe",
            "status": all(not bool(row["gate_pass"]) or row["gate_id"] == "CG2921_4_anti_circling" for row in claim_rows_)
            and all(not bool(row["valid_for_claim"]) for row in claim_rows_),
            "detail": "no physics claim gate is open",
            "valid_for_claim": False,
            "generated_utc": RUN_UTC,
        },
        {
            "validation_id": "VAL2921_9_next_target_selected",
            "status": any(row["route_id"] == "NEXT2921_0_2922" for row in next_rows_),
            "detail": "2922 Hamiltonian sector-owner/source-row target selected",
            "valid_for_claim": False,
            "generated_utc": RUN_UTC,
        },
        {
            "validation_id": "VAL2921_10_branch_copies_parse",
            "status": all(bool(row["destination_exists"]) and bool(row["destination_parses"]) for row in branch_rows_),
            "detail": "branch copies exist and parse",
            "valid_for_claim": False,
            "generated_utc": RUN_UTC,
        },
        {
            "validation_id": "VAL2921_11_no_formalization_outputs",
            "status": not any(is_under(path, FORMALIZATION) for path in list(OUTPUTS.values()) + list(BRANCH_OUTPUTS.values()) + [DOC]),
            "detail": "no generated output path is inside formalization-workbench",
            "valid_for_claim": False,
            "generated_utc": RUN_UTC,
        },
        {
            "validation_id": "VAL2921_12_doc_written",
            "status": DOC.exists() if include_doc_check else True,
            "detail": "markdown checkpoint exists",
            "valid_for_claim": False,
            "generated_utc": RUN_UTC,
        },
    ]
    rows.append(
        {
            "validation_id": "VAL2921_OVERALL",
            "status": all(bool(row["status"]) for row in rows),
            "detail": "2921 validation overall",
            "valid_for_claim": False,
            "generated_utc": RUN_UTC,
        }
    )
    return rows


def write_doc(
    source_rows: list[dict[str, Any]],
    identity_rows: list[dict[str, Any]],
    pg_rows: list[dict[str, Any]],
    scorecard_rows_: list[dict[str, Any]],
    crosswalk_rows_: list[dict[str, Any]],
    claim_rows_: list[dict[str, Any]],
    decision_rows_: list[dict[str, Any]],
    next_rows_: list[dict[str, Any]],
    branch_rows_: list[dict[str, Any]],
    validation_rows_: list[dict[str, Any]],
) -> None:
    overall = next(row for row in validation_rows_ if row["validation_id"] == "VAL2921_OVERALL")
    text = f"""# 2921 - Y5/R2FR Source-Normalized Newton/Gauss/Orbital Scorecard Or Parent Source-Mass Identity Under AX1090

Status: `Y5_R2FR_2921_conditional_PG_bridge_parent_source_mass_identity_not_derived_2922_owner_row_next`

Claim ceiling: `conditional_Newton_bridge_yes_parent_source_mass_no_beta_reopen_no_local_GR_no_PPN_no_R10_no_GitHub_claim`

Generated UTC: `{RUN_UTC}`

## Summary

2921 attacks the identity underneath the beta square-law:

`mu_obs = G0 M_H = G_eff M_source_parent`.

The clean result is conditional, not promotional. The Hamiltonian-to-Poisson/Gauss/orbital bridge is mathematically usable:

`B_xi = G_eff M_H`, `nabla^2 Phi = 4 pi G_eff rho_H`, `surface_integral grad Phi dot dS = 4 pi G_eff M_H`, and `a=-grad Phi` imply the measured orbital source strength `mu_obs=G_eff M_H`.

But the current MTS corpus does not yet prove the parent premises. The same source charge must be owned before readout, the projected Hilbert current must close, the Hamiltonian reference and `M_H_ref` denominator must be fixed, extra mass-channel charges must vanish or be bounded, and derivative/source/frame/range hair must be absent.

So this checkpoint keeps the bridge, refuses the claim, and imports the older 458/1012-1020 source-mass hunt so we do not circle. The deepest live obstruction is not "write Poisson again"; it is owner/source-row input for the Hamiltonian sector: `L_X/Theta_X/Q_X`, `B_ref`, `B_class`, `tau`, `M_H_ref`, and `Pi_M^H`.

## Source Register

{md_table(source_rows, ["source_id", "source_path", "anchors_found", "role", "missing_anchors"])}

## Parent Source-Mass Identity Audit

{md_table(identity_rows, ["audit_id", "clause", "math_form", "current_status", "meaning", "clause_passed", "valid_for_claim"])}

## Poisson/Gauss/Orbital Bridge Audit

{md_table(pg_rows, ["bridge_id", "contract_row", "required_identity", "current_status", "next_requirement", "valid_for_claim"])}

## Source-Normalized Newton Scorecard Rows

{md_table(scorecard_rows_, ["scorecard_id", "component_id", "symbol", "units", "observable_link", "bound_or_target", "current_status", "valid_for_claim"])}

## Prior Source-Mass Hunt Crosswalk

{md_table(crosswalk_rows_, ["crosswalk_id", "prior_checkpoint", "what_it_resolved", "what_remains", "2921_use", "valid_for_claim"])}

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

This is progress because it separates a true theorem from a missing parent certificate. The Newton bridge itself is not the weak point; the weak point is proving that the charge in the bridge is the same parent source charge that the observed orbit reads.

In other words: the route to GR reduction is now bottlenecked on source ownership, not on algebra. If the next owner/source-row target closes, beta can be reopened with a much cleaner denominator. If it fails, the source-normalized Newton branch remains an explicit residual vector instead of a hidden calibration assumption.

## Not Claimed

- no parent source-mass identity is claimed;
- no source-normalized Newton/Gauss/orbital pass is claimed;
- no beta square-law or PPN beta pass is claimed;
- no local-GR/Newton/PPN/R10/WEP/clock/orbital pass is claimed;
- no old 458/1012-1020 obstruction is erased by restating the bridge;
- no file in `formalization-workbench` is modified by this checkpoint;
- no public/GitHub action is implied.
"""
    DOC.write_text(text, encoding="utf-8")


def main() -> None:
    source_rows = source_register_rows()
    identity_rows = identity_audit_rows()
    pg_rows = pg_bridge_rows()
    scorecard_rows_ = scorecard_rows()
    crosswalk_rows_ = crosswalk_rows()
    claim_rows_ = claim_rows()
    decision_rows_ = decision_rows()
    next_rows_ = next_rows()

    write_csv(OUTPUTS["sources"], source_rows)
    write_csv(OUTPUTS["identity_audit"], identity_rows)
    write_csv(OUTPUTS["pg_bridge"], pg_rows)
    write_csv(OUTPUTS["scorecard"], scorecard_rows_)
    write_csv(OUTPUTS["crosswalk"], crosswalk_rows_)
    write_csv(OUTPUTS["claims"], claim_rows_)
    write_csv(OUTPUTS["decision"], decision_rows_)
    write_csv(OUTPUTS["next"], next_rows_)

    branch_rows_ = branch_rows()
    write_csv(OUTPUTS["branches"], branch_rows_)

    validation_rows_ = validation_rows(
        source_rows,
        identity_rows,
        pg_rows,
        scorecard_rows_,
        crosswalk_rows_,
        claim_rows_,
        next_rows_,
        branch_rows_,
        include_doc_check=False,
    )
    write_csv(OUTPUTS["validation"], validation_rows_)
    write_doc(
        source_rows,
        identity_rows,
        pg_rows,
        scorecard_rows_,
        crosswalk_rows_,
        claim_rows_,
        decision_rows_,
        next_rows_,
        branch_rows_,
        validation_rows_,
    )

    validation_rows_ = validation_rows(
        source_rows,
        identity_rows,
        pg_rows,
        scorecard_rows_,
        crosswalk_rows_,
        claim_rows_,
        next_rows_,
        branch_rows_,
        include_doc_check=True,
    )
    write_csv(OUTPUTS["validation"], validation_rows_)
    write_doc(
        source_rows,
        identity_rows,
        pg_rows,
        scorecard_rows_,
        crosswalk_rows_,
        claim_rows_,
        decision_rows_,
        next_rows_,
        branch_rows_,
        validation_rows_,
    )

    overall = next(row for row in validation_rows_ if row["validation_id"] == "VAL2921_OVERALL")
    if not bool(overall["status"]):
        raise SystemExit(1)


if __name__ == "__main__":
    main()

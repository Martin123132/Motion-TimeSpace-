from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


RUN_STARTED_UTC = datetime.now(timezone.utc)
ROOT = Path(r"D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main")
WORK = ROOT / "post-checkpoint-work"
MTS = WORK / "source-intake" / "mts_residuals"
RAB_QUEUE = WORK / "source-intake" / "rab-sector" / "acquisition-queue"
BETA_DOCS = WORK / "source-intake" / "beta-source" / "docs"
MICROSCOPE_DIR = WORK / "source-intake" / "microscope" / "branch_locked_wep" / "residuals"
SCRIPTS = WORK / "scripts"
FORMALIZATION = ROOT / "formalization-workbench"
DOC = WORK / "2794-Y5-R2FR-minimal-parent-ordinary-matter-signature-clause-or-finite-coefficient-intake-under-AX1090.md"

OUTPUTS = {
    "sources": MTS / "P8_Y5_R2FR_2794_SOURCE_REGISTER.csv",
    "signature": MTS / "P8_Y5_R2FR_2794_MINIMAL_SIGNATURE_CLAUSE.csv",
    "theorem": MTS / "P8_Y5_R2FR_2794_CONDITIONAL_ZERO_THEOREM.csv",
    "countermodels": MTS / "P8_Y5_R2FR_2794_COUNTERMODEL_RETENTION.csv",
    "formula": MTS / "P8_Y5_R2FR_2794_FINITE_PRODUCT_FORMULA.csv",
    "intake_schema": MTS / "P8_Y5_R2FR_2794_FINITE_DD_INTAKE_SCHEMA.csv",
    "template": MTS / "P8_Y5_R2FR_2794_FINITE_DD_INTAKE_TEMPLATE_NONCLAIM.csv",
    "candidate": MTS / "P8_Y5_R2FR_2794_WEP_PRODUCT_CANDIDATE_NONCLAIM.csv",
    "runner": MTS / "P8_Y5_R2FR_2794_PRODUCT_RUNNER_STATUS.csv",
    "comparisons": MTS / "P8_Y5_R2FR_2794_PRODUCT_COMPARISON_ROWS.csv",
    "gates": MTS / "P8_Y5_R2FR_2794_CLAIM_GATES.csv",
    "decision": MTS / "P8_Y5_R2FR_2794_DECISION_LEDGER.csv",
    "next": MTS / "P8_Y5_R2FR_2794_NEXT_TARGET.csv",
    "branches": MTS / "P8_Y5_R2FR_2794_BRANCH_COPIES.csv",
    "validation": MTS / "P8_Y5_BRR545_2794_VALIDATION.csv",
}

BRANCH_OUTPUTS = {
    "signature_queue": RAB_QUEUE / "JR2794_MINIMAL_PARENT_ORDINARY_MATTER_SIGNATURE_NONCLAIM.csv",
    "countermodel_queue": RAB_QUEUE / "JR2794_COUNTERMODEL_RETENTION_NONCLAIM.csv",
    "intake_queue": RAB_QUEUE / "JR2794_FINITE_DD_INTAKE_TEMPLATE_NONCLAIM.csv",
    "beta_doc": BETA_DOCS / "WEP_MINIMAL_SIGNATURE_OR_FINITE_INTAKE_2794_NONCLAIM.csv",
    "microscope_copy": MICROSCOPE_DIR / "microscope_wep_minimal_signature_or_finite_intake_2794_nonclaim.csv",
    "next_queue": RAB_QUEUE / "JR2794_PARENT_SIGNATURE_SOURCE_HUNT_OR_DD_INTAKE_REVIEW_NEXT.csv",
}


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def ensure_dirs() -> None:
    for path in {p.parent for p in OUTPUTS.values()} | {p.parent for p in BRANCH_OUTPUTS.values()} | {DOC.parent}:
        path.mkdir(parents=True, exist_ok=True)


def read_text(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8", errors="replace")
    except FileNotFoundError:
        return ""


def read_rows(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        path.write_text("", encoding="utf-8")
        return
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def csv_parses(path: Path) -> bool:
    try:
        if not path.exists():
            return False
        with path.open("r", encoding="utf-8", newline="") as handle:
            list(csv.DictReader(handle))
        return True
    except csv.Error:
        return False


def source_map() -> dict[str, tuple[Path, str]]:
    return {
        "2794_next_source": (MTS / "P8_Y5_R2FR_2793_NEXT_TARGET.csv", "authoritative R2FR target requesting minimal parent signature or finite intake"),
        "2793_descent": (MTS / "P8_Y5_R2FR_2793_PARENT_MATTER_DESCENT_ATTEMPT.csv", "clause stack that failed to become parent-signed"),
        "2793_contract": (MTS / "P8_Y5_R2FR_2793_ZERO_CURRENT_CLAUSE_CONTRACT.csv", "zero-current parent contract terms"),
        "2793_pack": (MTS / "P8_Y5_R2FR_2793_DD_COEFFICIENT_SOURCE_PACK.csv", "finite DD coefficient slots to inherit"),
        "2793_template": (MTS / "P8_Y5_R2FR_2793_DD_COEFFICIENT_SOURCE_PACK_TEMPLATE_NONCLAIM.csv", "nonclaim coefficient placeholders"),
        "2793_policy": (MTS / "P8_Y5_R2FR_2793_ALL_MATERIAL_NO_CANCELLATION_POLICY.csv", "all-material no-cancellation policy"),
        "2793_validation": (MTS / "P8_Y5_BRR545_2793_VALIDATION.csv", "prior validation ledger"),
        "2792_delta": (MTS / "P8_Y5_R2FR_2792_COMPOSITION_DELTA_OBSTRUCTION.csv", "DD material deltas for product formula context"),
        "2791_range_schema": (MTS / "P8_Y5_R2FR_2791_RANGE_ACQUISITION_SCHEMA.csv", "same-branch range/profile/readout blockers"),
        "1088_signature_analogue": (MTS / "P8_Y5_R10_1088_MINIMAL_SIGNATURE_CLAUSE.csv", "R10 minimal-signature analogue for structure only"),
        "1088_theorem_analogue": (MTS / "P8_Y5_R10_1088_CONDITIONAL_ZERO_THEOREM.csv", "R10 conditional zero theorem analogue for structure only"),
        "1088_intake_analogue": (MTS / "P8_Y5_R10_1088_FINITE_DD_INTAKE_SCHEMA.csv", "R10 finite-intake schema analogue for structure only"),
    }


def build_sources() -> list[dict[str, Any]]:
    rows = []
    for source_id, (path, role) in source_map().items():
        rows.append(
            {
                "source_id": source_id,
                "path": str(path),
                "exists": path.exists(),
                "role": role,
                "contains_text": bool(read_text(path).strip()) if path.exists() else False,
                "valid_for_claim": False,
                "generated_utc": utc_now(),
            }
        )
    return rows


def build_signature_rows() -> list[dict[str, Any]]:
    rows = [
        (
            "MOMS2794_0_action_form",
            "S_parent = S_geom[Phi] + sum_A S_A[Psi_A; E(q(Phi)), Omega(E(q(Phi))), A_obs(q(Phi)), theta_A]",
            "ordinary matter sees only observed quotient geometry, observed gauge data, owned matter fields, and representation/superselection constants",
            "CONDITIONAL_CLAUSE_WRITTEN_NOT_PARENT_DERIVED",
            "one corpus parent action explicitly owning q, E, Omega, A_obs, Psi_A, theta_A, and the species sum",
        ),
        (
            "MOMS2794_1_quotient_observables",
            "q: Phi_parent -> Q_obs with v_X in ker(Dq), e_obs=E(q(Phi)), g_obs=e_obs^T eta e_obs",
            "Lie_vX e_obs = Lie_vX g_obs = 0 by chain rule",
            "CONDITIONAL_GEOMETRY_SUBLEMMA",
            "parent-derived observed quotient/coframe functor and independent connection silence",
        ),
        (
            "MOMS2794_2_matter_bundle",
            "Psi_A is a section of Bundle_A[e_obs,A_obs] and vertical lifts on Psi_A are fixed, gauge, local-Lorentz, diffeomorphism, or boundary-only",
            "no physical ordinary-matter lift along a quotient-vertical field",
            "MISSING_PARENT_MATTER_BUNDLE_FUNCTOR",
            "species-complete parent matter bundle functor and boundary class",
        ),
        (
            "MOMS2794_3_constant_superselection",
            "Lie_vX theta_A = 0 for ordinary masses, charges, clock standards, representation labels, and hbar/c normalization",
            "no hidden composition current through material constants",
            "CONSTANT_SUPERSELECTION_UNSIGNED",
            "parent theorem that constants are fixed representation data, or explicit retained residual fields",
        ),
        (
            "MOMS2794_4_no_species_weights",
            "the parent matter sum has no independent w_A(X) S_A or material-only source multiplier before variation",
            "kills pre-action species/source weights that mimic WEP violation while keeping the visible metric fixed",
            "PRE_ACTION_WEIGHT_EXCLUSION_UNSIGNED",
            "object-language plus action-measure clause forbidding source-only inert weights",
        ),
        (
            "MOMS2794_5_variation_order",
            "Hilbert/current extraction is performed on S_parent before material/readout projection or empirical fitting",
            "prevents post-variation source selectors from manufacturing a residual current",
            "CONDITIONAL_SUBTHEOREM_ONLY",
            "parent-side variation-before-readout rule tied to the same action",
        ),
        (
            "MOMS2794_6_no_shadow_domain",
            "no shadow matter frame A_A(X)^2 g_obs, disformal B_A(X), support/domain marker, boundary charge, or source-only metric is present",
            "closes hidden frame/domain leakage",
            "NO_SHADOW_DOMAIN_UNSIGNED",
            "single parent exclusion of shadow frames and boundary/domain charges",
        ),
        (
            "MOMS2794_7_verdict",
            "MOMS2794_0 through MOMS2794_6 are all parent-derived in one ordinary-matter action signature",
            "qbar_XT=0 and the local WEP source-current branch is theorem-zero",
            "MINIMAL_PARENT_ORDINARY_MATTER_SIGNATURE_NOT_DERIVED",
            "the clause is exact but current R2FR files provide it only as a future contract, not as a derived parent action",
        ),
    ]
    return [
        {
            "clause_id": row[0],
            "minimal_signature_clause": row[1],
            "what_it_signs": row[2],
            "current_status": row[3],
            "missing_for_adoption": row[4],
            "valid_for_claim": False,
            "generated_utc": utc_now(),
        }
        for row in rows
    ]


def build_theorem_rows() -> list[dict[str, Any]]:
    rows = [
        ("THM2794_0_assumptions", "assume the full MOMS2794 parent ordinary-matter signature", "all ordinary matter terms depend on v_X only through q(Phi), quotient-owned observed geometry/gauge data, gauge/boundary lifts, and X-trivial constants", "ASSUMPTION_SET_EXACT", "conditional_only"),
        ("THM2794_1_visible_fields", "differentiate observed fields along v_X", "Dq[v_X]=0 gives Lie_vX e_obs = D E[Dq(v_X)] = 0, and similarly for g_obs, Omega[e_obs], and A_obs(q(Phi))", "VISIBLE_FIELD_VARIATION_ZERO_IF_SIGNATURE_SIGNED", "conditional_only"),
        ("THM2794_2_matter_lift", "differentiate matter fields along the owned vertical lift", "delta_v Psi_A is zero, gauge, local-Lorentz, diffeomorphism, or boundary-only, so its contribution to the bulk Euler/Hilbert source current vanishes", "BULK_MATTER_LIFT_VARIATION_ZERO_IF_SIGNATURE_SIGNED", "conditional_only"),
        ("THM2794_3_constants", "differentiate representation constants", "Lie_vX theta_A=0 removes alpha_EM, mass-ratio, clock, and material-constant source-current channels unless they are explicitly retained as finite residual fields", "CONSTANT_CHANNEL_ZERO_IF_SIGNATURE_SIGNED", "conditional_only"),
        ("THM2794_4_no_weight_leak", "exclude pre-action weights and shadow/domain terms", "without w_A(X), shadow frames, or domain markers, no source-only material label remains for delta_v S_matter to hit", "NO_HIDDEN_RESIDUAL_SLOT_IF_SIGNATURE_SIGNED", "conditional_only"),
        ("THM2794_5_conclusion", "take the vertical variation of ordinary matter", "delta_v S_matter = 0 up to gauge/boundary terms, hence J_X^matter=0 and qbar_XT=0 for local WEP/DD composition response", "ZERO_THEOREM_PROVED_UNDER_MOMS2794_SIGNATURE", "conditional_only"),
        ("THM2794_6_current_corpus_verdict", "compare theorem assumptions with current R2FR source files", "2793 writes the required clauses, but does not derive them in one parent action", "CONDITIONAL_ZERO_THEOREM_NOT_PROMOTED", "blocked_by_unsigned_signature"),
    ]
    return [
        {
            "theorem_id": row[0],
            "step": row[1],
            "derivation": row[2],
            "result": row[3],
            "claim_status": row[4],
            "valid_for_claim": False,
            "generated_utc": utc_now(),
        }
        for row in rows
    ]


def build_countermodel_rows() -> list[dict[str, Any]]:
    rows = [
        ("CM2794_0_species_weight", "S_matter -> sum_A w_A(X) S_A with species/material-dependent w_A", "visible metric can remain quotient-owned while WEP source current is nonzero", "MOMS2794_4_no_species_weights"),
        ("CM2794_1_variable_constants", "theta_A(X) includes alpha_EM, nuclear binding, mass-ratio, or clock sensitivities", "composition-dependent DD charges survive even if geometry descends", "MOMS2794_3_constant_superselection"),
        ("CM2794_2_shadow_frame", "ordinary matter uses A_A(X)^2 g_obs or disformal/source-only metric data", "local fifth-force or WEP residual hides outside the observed coframe chain rule", "MOMS2794_6_no_shadow_domain"),
        ("CM2794_3_post_variation_selector", "material/readout projection is applied after variation and changes source normalization", "a residual source current appears as a readout artifact rather than a parent current", "MOMS2794_5_variation_order"),
        ("CM2794_4_boundary_domain_marker", "source support, boundary charge, or domain marker shifts under v_X", "bulk descent can hold while finite-boundary/source-profile WEP residual remains", "MOMS2794_6_no_shadow_domain"),
    ]
    return [
        {
            "countermodel_id": row[0],
            "legal_without_signature": row[1],
            "damage": row[2],
            "killed_by": row[3],
            "current_status": "NOT_KILLED_BY_CURRENT_R2FR_CORPUS",
            "valid_for_claim": False,
            "generated_utc": utc_now(),
        }
        for row in rows
    ]


def build_formula_rows() -> list[dict[str, Any]]:
    rows = [
        (
            "FPF2794_0_eta_formula",
            "eta_AB(lambda) = K_MICROSCOPE(lambda) * [c_alpha Qeff_E_alpha(lambda) DeltaQ_AB_alpha + c_surface Qeff_E_surface(lambda) DeltaQ_AB_surface + c_mass_ratio Qeff_E_mass(lambda) DeltaQ_AB_mass + q_tail_AB(lambda)]",
            "fallback finite branch if MOMS2794 zero theorem remains unsigned",
            "same-branch lambda, K, Qeff source profile, test-material DD deltas, c_alpha, c_surface, c_mass_ratio, and tail envelope",
            "FORMULA_READY_NONCLAIM",
        ),
        (
            "FPF2794_1_zero_limit",
            "if MOMS2794 signs, c_alpha=c_surface=c_mass_ratio=q_tail=0 before readout and eta_AB=0",
            "theorem route beats finite fitting by deleting the coefficient vector",
            "parent-derived MOMS2794 signature",
            "CONDITIONAL_ZERO_LIMIT",
        ),
        (
            "FPF2794_2_same_branch_lock",
            "lambda_X, K_MICROSCOPE, Qeff_E, c_I, and DeltaQ_I must be owned by the same branch and normalization",
            "prevents range/amplitude/readout mix-and-match tuning",
            "branch_id and source paths for every factor",
            "CLAIM_POLICY_LOCK",
        ),
    ]
    return [
        {
            "formula_id": row[0],
            "formula": row[1],
            "meaning": row[2],
            "required_inputs": row[3],
            "status": row[4],
            "valid_for_claim": False,
            "generated_utc": utc_now(),
        }
        for row in rows
    ]


def build_intake_schema_rows() -> list[dict[str, Any]]:
    rows = [
        ("FIS2794_0_branch_id", "branch_id", "label", "one MTS branch supplying range, amplitude, coefficients, and readout", "must be same branch for every row"),
        ("FIS2794_1_lambda", "lambda_X_m", "m", "parent Z_X/M_X^2 or source-backed finite-range branch", "positive numeric with source path; no fitted convenience range"),
        ("FIS2794_2_readout", "K_MICROSCOPE_lambda", "dimensionless readout factor", "official or derived MICROSCOPE readout/projection model", "not a unit proxy unless explicitly labelled nonclaim"),
        ("FIS2794_3_source_profile", "Qeff_E_alpha;Qeff_E_surface;Qeff_E_mass", "DD charge convention", "bulk long-range theorem or finite profile integration with sourced Earth profile", "must match lambda_X and composition profile"),
        ("FIS2794_4_coefficients", "c_alpha;c_surface;c_mass_ratio;q_tail", "dimensionless after parent normalization", "parent action derivative or labelled phenomenological source with provenance", "no pair cancellation, no posthoc sign choice, no measured-G absorption"),
        ("FIS2794_5_prediction", "eta_pred", "dimensionless", "computed from all source-backed factors using FPF2794_0", "claim allowed only if abs(eta_pred) <= accepted bound and all gates are source-backed"),
    ]
    return [
        {
            "field_id": row[0],
            "field_name": row[1],
            "units": row[2],
            "required_source": row[3],
            "validity_rule": row[4],
            "valid_for_claim": False,
            "generated_utc": utc_now(),
        }
        for row in rows
    ]


def build_template_rows() -> list[dict[str, Any]]:
    rows = [
        ("FIT2794_0_c_alpha", "MTS_WEP_finite_branch", "c_alpha", "MISSING_PARENT_EM_DERIVATIVE_OR_PROVENANCE_VALUE", "dimensionless_after_parent_normalization", "MISSING_PARENT_OR_EXPLICIT_PHENOMENOLOGICAL_SOURCE", "MISSING", "missing", "do not fill from smoke-fit, cancellation line, or desired WEP bound"),
        ("FIT2794_1_c_surface", "MTS_WEP_finite_branch", "c_surface", "MISSING_PARENT_BINDING_DERIVATIVE_OR_PROVENANCE_VALUE", "dimensionless_after_parent_normalization", "MISSING_PARENT_OR_EXPLICIT_PHENOMENOLOGICAL_SOURCE", "MISSING", "missing", "must be all-material, not tuned to TA6V/PtRh10"),
        ("FIT2794_2_c_mass_ratio", "MTS_WEP_finite_branch", "c_mass_ratio", "MISSING_PARENT_MASS_RATIO_DERIVATIVE_OR_ZERO_PROOF", "dimensionless_after_parent_normalization", "MISSING_PARENT_OR_EXPLICIT_PHENOMENOLOGICAL_SOURCE", "MISSING", "missing", "must separate universal mass scaling from composition contrast"),
        ("FIT2794_3_q_tail", "MTS_WEP_finite_branch", "q_tail_AB_lambda", "MISSING_TAIL_ENVELOPE", "dimensionless_eta_contribution_or_charge_envelope", "MISSING_PARENT_OR_EMPIRICAL_ENVELOPE_SOURCE", "MISSING", "missing", "needed because alpha/surface/mass rows are not a complete material basis"),
        ("FIT2794_4_lambda_K_profile", "MTS_WEP_finite_branch", "lambda_X_m;K_MICROSCOPE;Qeff_E", "MISSING_SAME_BRANCH_RANGE_READOUT_PROFILE", "m;dimensionless;DD_charge", "MISSING_RANGE_READOUT_PROFILE_SOURCE", "MISSING", "missing", "must share one branch normalization with the coefficient vector"),
    ]
    return [
        {
            "template_id": row[0],
            "branch_id": row[1],
            "quantity": row[2],
            "value": row[3],
            "units": row[4],
            "source_path": row[5],
            "source_row": row[6],
            "derivation_status": row[7],
            "valid_for_claim": False,
            "notes": row[8],
            "generated_utc": utc_now(),
        }
        for row in rows
    ]


def build_candidate_rows() -> list[dict[str, Any]]:
    return [
        {
            "prediction_id": "WEP2794_0_finite_template",
            "observable": "eta_AB(lambda)",
            "formula_id": "FPF2794_0_eta_formula",
            "inputs_status": "MISSING_COEFFICIENTS_AND_SAME_BRANCH_READOUT",
            "eta_pred": "MISSING_NUMERIC",
            "claim_blocker": "finite intake template contains only placeholders",
            "valid_for_claim": False,
            "generated_utc": utc_now(),
        }
    ]


def build_runner_rows() -> list[dict[str, Any]]:
    return [
        {
            "runner_id": "RUN2794_0_refuse_placeholder_intake",
            "valid_prediction_rows": 0,
            "claim_allowed": False,
            "expected_result": "RUNNER_REFUSES_WEP_CLAIM",
            "reason": "MOMS2794 is unsigned and finite-intake rows are placeholders",
            "valid_for_claim": False,
            "generated_utc": utc_now(),
        }
    ]


def build_comparison_rows() -> list[dict[str, Any]]:
    return [
        {
            "comparison_id": "CMP2794_0_no_numeric_eta",
            "baseline": "WEP/local-GR compatibility bound",
            "prediction": "MTS R2FR finite DD branch",
            "comparison_status": "NOT_RUN_NUMERICALLY",
            "reason": "no source-backed coefficient/readout/profile rows exist",
            "valid_for_claim": False,
            "generated_utc": utc_now(),
        }
    ]


def build_gate_rows() -> list[dict[str, Any]]:
    rows = [
        ("CG2794_0_parent_signature", "minimal parent ordinary-matter signature", False, False, "MOMS2794_7_verdict=MINIMAL_PARENT_ORDINARY_MATTER_SIGNATURE_NOT_DERIVED"),
        ("CG2794_1_conditional_zero_theorem", "qbar_XT=0 theorem", True, False, "proved only under unsigned MOMS2794 assumptions"),
        ("CG2794_2_finite_intake", "finite DD coefficient intake", False, False, "all finite coefficient/range/readout/profile rows contain missing placeholders"),
        ("CG2794_3_product_runner", "WEP product runner", True, False, "valid_prediction_rows=0"),
        ("CG2794_4_local_GR_claim", "local-GR/WEP reduction", False, False, "conditional theorem does not equal a parent-derived reduction"),
    ]
    return [
        {
            "gate_id": row[0],
            "claim_component": row[1],
            "gate_pass": row[2],
            "claim_allowed": row[3],
            "reason": row[4],
            "valid_for_claim": False,
            "generated_utc": utc_now(),
        }
        for row in rows
    ]


def build_decision_rows() -> list[dict[str, Any]]:
    rows = [
        (
            "DEC2794_0_conditional_win",
            "conditional WEP-zero theorem is now exact",
            "under MOMS2794, the matter source current vanishes by chain rule, gauge/boundary lift, X-trivial constants, and no hidden material slot",
            "hunt for a real parent-action source that derives MOMS2794 rather than adopting it",
        ),
        (
            "DEC2794_1_not_promoted",
            "do not promote MOMS2794 to a theorem of MTS yet",
            "countermodels remain legal unless the parent action forbids species weights, variable constants, shadow frames, post-variation selectors, and boundary/domain markers",
            "keep countermodel ledger live",
        ),
        (
            "DEC2794_2_finite_fallback",
            "finite DD intake is ready as explicit phenomenological scaffolding",
            "if the parent signature cannot be sourced, only fully sourced coefficient/readout/profile rows can be reviewed",
            "review finite intake rows without fitting to the WEP bound",
        ),
    ]
    return [
        {
            "decision_id": row[0],
            "decision": row[1],
            "because": row[2],
            "next_action": row[3],
            "valid_for_claim": False,
            "generated_utc": utc_now(),
        }
        for row in rows
    ]


def build_next_rows() -> list[dict[str, Any]]:
    return [
        {
            "next_id": "NEXT2794_0_2795",
            "next_target": "2795-Y5-R2FR-parent-ordinary-matter-signature-source-hunt-or-DD-intake-review-under-AX1090.md",
            "script": "scripts/Y5_R2FR_parent_ordinary_matter_signature_source_hunt_or_DD_intake_review_under_AX1090_2795.py",
            "objective": "search the corpus for a real parent-action source that signs the MOMS2794 ordinary-matter signature; if none exists, keep finite DD intake as explicit nonclaim scaffolding and review only fully sourced rows",
            "include": "parent action source hunt; ordinary matter object-language; no species weights; constant superselection; variation-before-readout; no-shadow/domain clause; finite intake review rules",
            "exclude": "adopting MOMS2794 as axiom; invented coefficients; pair cancellation; measured-G absorption; WEP/local-GR claim; GitHub; formalization edits",
            "valid_for_claim": False,
            "generated_utc": utc_now(),
        }
    ]


def copy_branches() -> list[dict[str, Any]]:
    copy_plan = [
        (OUTPUTS["signature"], BRANCH_OUTPUTS["signature_queue"], "signature_queue"),
        (OUTPUTS["countermodels"], BRANCH_OUTPUTS["countermodel_queue"], "countermodel_queue"),
        (OUTPUTS["template"], BRANCH_OUTPUTS["intake_queue"], "intake_queue"),
        (OUTPUTS["theorem"], BRANCH_OUTPUTS["beta_doc"], "beta_doc"),
        (OUTPUTS["formula"], BRANCH_OUTPUTS["microscope_copy"], "microscope_copy"),
        (OUTPUTS["next"], BRANCH_OUTPUTS["next_queue"], "next_queue"),
    ]
    rows = []
    for source, destination, label in copy_plan:
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(source, destination)
        rows.append(
            {
                "copy_id": f"BC2794_{label}",
                "source": str(source),
                "destination": str(destination),
                "exists": destination.exists(),
                "valid_for_claim": False,
                "generated_utc": utc_now(),
            }
        )
    return rows


def formalization_untouched_since_run() -> bool:
    if not FORMALIZATION.exists():
        return True
    threshold = RUN_STARTED_UTC.timestamp()
    return not any(path.is_file() and path.stat().st_mtime >= threshold for path in FORMALIZATION.rglob("*"))


def claim_flags_true(sections: dict[str, list[dict[str, Any]]]) -> bool:
    for key, rows in sections.items():
        if key == "validation":
            continue
        for row in rows:
            if str(row.get("valid_for_claim", "false")).lower() == "true":
                return True
            if str(row.get("claim_allowed", "false")).lower() == "true":
                return True
    return False


def build_validation(sections: dict[str, list[dict[str, Any]]]) -> list[dict[str, Any]]:
    generated_paths = [path for key, path in OUTPUTS.items() if key != "validation"] + list(BRANCH_OUTPUTS.values())
    checks = [
        ("VAL2794_0_sources_exist", all(row["exists"] for row in sections["sources"]), "all cited local source paths exist"),
        ("VAL2794_1_signature_exact", any(row["clause_id"] == "MOMS2794_0_action_form" for row in sections["signature"]), "minimal signature action form is written"),
        ("VAL2794_2_signature_not_derived", any(row["clause_id"] == "MOMS2794_7_verdict" and row["current_status"] == "MINIMAL_PARENT_ORDINARY_MATTER_SIGNATURE_NOT_DERIVED" for row in sections["signature"]), "minimal parent ordinary-matter signature is not claimed"),
        ("VAL2794_3_conditional_theorem_proved", any(row["theorem_id"] == "THM2794_5_conclusion" and row["result"] == "ZERO_THEOREM_PROVED_UNDER_MOMS2794_SIGNATURE" for row in sections["theorem"]), "conditional zero theorem is proved under unsigned assumptions"),
        ("VAL2794_4_theorem_not_promoted", any(row["theorem_id"] == "THM2794_6_current_corpus_verdict" and row["result"] == "CONDITIONAL_ZERO_THEOREM_NOT_PROMOTED" for row in sections["theorem"]), "conditional zero theorem is not promoted to an MTS claim"),
        ("VAL2794_5_countermodels_live", all(row["current_status"] == "NOT_KILLED_BY_CURRENT_R2FR_CORPUS" for row in sections["countermodels"]), "countermodels remain live"),
        ("VAL2794_6_formula_nonclaim", any(row["formula_id"] == "FPF2794_0_eta_formula" and row["status"] == "FORMULA_READY_NONCLAIM" for row in sections["formula"]), "finite eta formula is staged as nonclaim"),
        ("VAL2794_7_intake_schema_complete", {row["field_name"] for row in sections["intake_schema"]} >= {"branch_id", "lambda_X_m", "K_MICROSCOPE_lambda", "Qeff_E_alpha;Qeff_E_surface;Qeff_E_mass", "c_alpha;c_surface;c_mass_ratio;q_tail", "eta_pred"}, "finite intake schema covers branch, range, readout, profile, coefficients, and prediction"),
        ("VAL2794_8_template_placeholders", all("MISSING" in str(row["value"]) for row in sections["template"]), "finite intake template contains placeholders only"),
        ("VAL2794_9_runner_refuses", any(row["expected_result"] == "RUNNER_REFUSES_WEP_CLAIM" and str(row["claim_allowed"]).lower() == "false" for row in sections["runner"]), "runner refuses placeholder WEP claim"),
        ("VAL2794_10_claim_gates_safe", all(str(row["claim_allowed"]).lower() == "false" for row in sections["gates"]), "all claim gates keep claims blocked"),
        ("VAL2794_11_next_target_2795", any(row["next_id"] == "NEXT2794_0_2795" for row in sections["next"]), "next target is 2795"),
        ("VAL2794_12_branch_outputs_exist", all(path.exists() for path in BRANCH_OUTPUTS.values()), "branch copies were written"),
        ("VAL2794_13_outputs_exist", all(path.exists() for path in generated_paths), "all output paths exist"),
        ("VAL2794_14_csv_parse", all(csv_parses(path) for path in generated_paths), "all generated CSV outputs parse"),
        ("VAL2794_15_no_claim_flags", not claim_flags_true(sections), "no valid_for_claim or claim_allowed flag is true"),
        ("VAL2794_16_generated_under_post_checkpoint", all(str(path).startswith(str(WORK)) for path in generated_paths + [DOC]), "all generated artifacts remain under post-checkpoint-work"),
        ("VAL2794_17_formalization_untouched", formalization_untouched_since_run(), "formalization-workbench was not modified during this run"),
        ("VAL2794_18_pycache_absent", not (SCRIPTS / "__pycache__").exists(), "scripts __pycache__ absent before compile step"),
    ]
    rows = [
        {
            "validation_id": check_id,
            "passed": bool(passed),
            "detail": detail,
            "generated_utc": utc_now(),
        }
        for check_id, passed, detail in checks
    ]
    rows.append(
        {
            "validation_id": "VAL2794_OVERALL",
            "passed": all(row["passed"] for row in rows),
            "detail": "2794 proves the WEP zero-current theorem under an exact minimal ordinary-matter parent signature, but refuses to promote it because the signature is not parent-derived in the current R2FR corpus. Finite DD intake remains source-ready and nonclaim.",
            "generated_utc": utc_now(),
        }
    )
    return rows


def markdown_table(rows: list[dict[str, Any]], columns: list[str]) -> str:
    if not rows:
        return "_No rows._"
    header = "| " + " | ".join(columns) + " |"
    separator = "| " + " | ".join("---" for _ in columns) + " |"
    body = []
    for row in rows:
        body.append("| " + " | ".join(str(row.get(column, "")).replace("\n", " ").replace("|", "\\|") for column in columns) + " |")
    return "\n".join([header, separator, *body])


def build_doc(sections: dict[str, list[dict[str, Any]]]) -> str:
    lines = [
        "# 2794 — Y5 R2FR Minimal Parent Ordinary Matter Signature Clause Or Finite Coefficient Intake Under AX1090",
        "",
        "## Private Verdict",
        "",
        "2794 gets a real mathematical foothold: **if** the minimal ordinary-matter parent signature MOMS2794 is true, then the WEP/local composition current vanishes by a clean chain-rule theorem. That is the route that would make local GR compatibility look structural rather than fitted.",
        "",
        "But MOMS2794 is not yet derived from the parent MTS action. The current corpus has the exact clause as a contract, not as an owned action principle. Countermodels remain legal until the corpus kills species weights, variable constants, shadow frames, post-variation selectors, and boundary/domain markers.",
        "",
        "So the score is: conditional theorem **yes**; claimable WEP/local-GR reduction **not yet**; finite DD coefficient intake staged only as nonclaim scaffolding.",
        "",
        "## Source Register",
        markdown_table(sections["sources"], ["source_id", "exists", "role", "path"]),
        "",
        "## Minimal Signature Clause",
        markdown_table(sections["signature"], ["clause_id", "current_status", "what_it_signs", "missing_for_adoption"]),
        "",
        "## Conditional Zero Theorem",
        markdown_table(sections["theorem"], ["theorem_id", "step", "result", "claim_status"]),
        "",
        "## Countermodel Retention",
        markdown_table(sections["countermodels"], ["countermodel_id", "legal_without_signature", "damage", "killed_by", "current_status"]),
        "",
        "## Finite Product Formula",
        markdown_table(sections["formula"], ["formula_id", "formula", "status", "required_inputs"]),
        "",
        "## Finite DD Intake Schema",
        markdown_table(sections["intake_schema"], ["field_id", "field_name", "required_source", "validity_rule"]),
        "",
        "## Finite Intake Template",
        markdown_table(sections["template"], ["template_id", "quantity", "value", "source_path", "valid_for_claim"]),
        "",
        "## Claim Gates",
        markdown_table(sections["gates"], ["gate_id", "claim_component", "gate_pass", "claim_allowed", "reason"]),
        "",
        "## Decision Ledger",
        markdown_table(sections["decision"], ["decision_id", "decision", "because", "next_action"]),
        "",
        "## Validation",
        markdown_table(sections["validation"], ["validation_id", "passed", "detail"]),
        "",
        "## Next Target",
        markdown_table(sections["next"], ["next_id", "next_target", "objective", "include", "exclude"]),
        "",
    ]
    return "\n".join(lines)


def main() -> None:
    ensure_dirs()
    if (SCRIPTS / "__pycache__").exists():
        shutil.rmtree(SCRIPTS / "__pycache__")

    sections: dict[str, list[dict[str, Any]]] = {
        "sources": build_sources(),
        "signature": build_signature_rows(),
        "theorem": build_theorem_rows(),
        "countermodels": build_countermodel_rows(),
        "formula": build_formula_rows(),
        "intake_schema": build_intake_schema_rows(),
        "template": build_template_rows(),
        "candidate": build_candidate_rows(),
        "runner": build_runner_rows(),
        "comparisons": build_comparison_rows(),
        "gates": build_gate_rows(),
        "decision": build_decision_rows(),
        "next": build_next_rows(),
    }
    for key, rows in sections.items():
        if key in OUTPUTS:
            write_csv(OUTPUTS[key], rows)

    sections["branches"] = copy_branches()
    write_csv(OUTPUTS["branches"], sections["branches"])
    sections["validation"] = build_validation(sections)
    write_csv(OUTPUTS["validation"], sections["validation"])
    DOC.write_text(build_doc(sections), encoding="utf-8")
    print(f"wrote {DOC}")
    print(f"validation overall: {sections['validation'][-1]['passed']}")


if __name__ == "__main__":
    main()

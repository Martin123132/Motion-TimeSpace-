from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "source-intake" / "mts_residuals"
SOURCE_WEIGHT_DOCS = ROOT / "source-intake" / "source-weight" / "docs"
MICROSCOPE_COEFFS = ROOT / "source-intake" / "microscope" / "branch_locked_wep" / "coefficients"
QUEUE = ROOT / "source-intake" / "rab-sector" / "acquisition-queue"
QUARANTINE = ROOT / "source-intake" / "microscope" / "quarantine" / "1931"
FORMALIZATION = ROOT.parent / "formalization-workbench"

DOC = ROOT / "1931-Y5-R2FR-parent-ordinary-sector-action-signature-or-explicit-closure-ledger.md"
BRANCH_ID = "MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428"
GENERATED_UTC = datetime.now(timezone.utc).isoformat()

SOURCES = {
    "1930_next": OUT / "P8_Y5_PARENT_QLOC_1930_NEXT_TARGET.csv",
    "1930_doc": ROOT / "1930-Y5-R2FR-alpha-product-first-input-fill-tau-clock-Xhat-or-WEP-beta-source.md",
    "1930_live_debts": OUT / "P8_Y5_PARENT_QLOC_1930_LIVE_DEBT_MATRIX.csv",
    "1930_validation": OUT / "P8_Y5_BRR545_1930_VALIDATION.csv",
    "1104_signature": OUT / "P8_Y5_R10_1104_PARENT_SIGNATURE_LEDGER.csv",
    "1104_theorem": OUT / "P8_Y5_R10_1104_CONDITIONAL_THEOREM.csv",
    "1104_closure": OUT / "P8_Y5_R10_1104_EXPLICIT_CLOSURE_LEDGER.csv",
    "1104_claims": OUT / "P8_Y5_R10_1104_CLAIM_GATES.csv",
    "1104_validation": OUT / "P8_Y5_BRR545_1104_VALIDATION.csv",
    "1104_next": OUT / "P8_Y5_R10_1104_NEXT_TARGET.csv",
    "1105_master": OUT / "P8_Y5_R10_1105_MASTER_MORPHISM_THEOREM_ATTEMPT.csv",
    "1105_closure_pack": OUT / "P8_Y5_R10_1105_EXPLICIT_CLOSURE_PACK.csv",
    "1105_finite_requirements": OUT / "P8_Y5_R10_1105_FINITE_SOURCE_REQUIREMENTS.csv",
    "1105_claims": OUT / "P8_Y5_R10_1105_CLAIM_GATES.csv",
    "1105_validation": OUT / "P8_Y5_BRR545_1105_VALIDATION.csv",
    "1105_next": OUT / "P8_Y5_R10_1105_NEXT_TARGET.csv",
}

NEEDLES = {
    "1930_next": ["NEXT1930_0_primary", "parent-ordinary-sector-action-signature"],
    "1930_doc": ["DEBT1930_0_parent_ordinary_sector_signature", "VAL1930_OVERALL"],
    "1930_live_debts": ["DEBT1930_0_parent_ordinary_sector_signature", "DEBT1930_5_hidden_invariants"],
    "1930_validation": ["VAL1930_OVERALL", "PASS"],
    "1104_signature": ["SIG1104_0_parent_domain", "SIG1104_10_verdict"],
    "1104_theorem": ["THM1104_1_chain_rule_if_signature_signed", "THM1104_4_verdict"],
    "1104_closure": ["CLOS1104_1_master_closure_candidate", "CLOS1104_5_finite_branch"],
    "1104_claims": ["CG1104_0_parent_signature", "CG1104_4_local_GR_Newton"],
    "1104_validation": ["V1104_SUMMARY", "pass"],
    "1104_next": ["NEXT1104_0_1105", "master-no-hidden-visible"],
    "1105_master": ["MHM1105_6_verdict", "MASTER_THEOREM_NOT_DERIVED"],
    "1105_closure_pack": ["PACK1105_0_parent_object_language", "PACK1105_4_residual_vector_if_unsigned"],
    "1105_finite_requirements": ["FIN1105_0_alpha_coefficient", "FIN1105_5_mass_binding"],
    "1105_claims": ["CG1105_0_master_theorem", "CG1105_3_finite_rows"],
    "1105_validation": ["V1105_SUMMARY", "pass"],
    "1105_next": ["NEXT1105_0_1106", "closure pack"],
}

OUTPUTS = {
    "source_register": OUT / "P8_Y5_PARENT_QLOC_1931_SOURCE_REGISTER.csv",
    "signature": OUT / "P8_Y5_PARENT_QLOC_1931_PARENT_SIGNATURE_LEDGER.csv",
    "theorem": OUT / "P8_Y5_PARENT_QLOC_1931_CONDITIONAL_THEOREM.csv",
    "closure": OUT / "P8_Y5_PARENT_QLOC_1931_EXPLICIT_CLOSURE_LEDGER.csv",
    "finite_requirements": OUT / "P8_Y5_PARENT_QLOC_1931_FINITE_SOURCE_REQUIREMENTS.csv",
    "claim_gate": OUT / "P8_Y5_PARENT_QLOC_1931_CLAIM_GATE.csv",
    "decision": OUT / "P8_Y5_PARENT_QLOC_1931_DECISION_LEDGER.csv",
    "next_target": OUT / "P8_Y5_PARENT_QLOC_1931_NEXT_TARGET.csv",
    "snapshot": OUT / "P8_Y5_PARENT_QLOC_1931_PROJECT_STATUS_SNAPSHOT.csv",
    "validation": OUT / "P8_Y5_BRR545_1931_VALIDATION.csv",
}

BRANCH_COPIES = [
    (OUTPUTS["signature"], SOURCE_WEIGHT_DOCS / "ORDINARY_SECTOR_PARENT_SIGNATURE_LEDGER_1931_NONCLAIM.csv"),
    (OUTPUTS["finite_requirements"], MICROSCOPE_COEFFS / "P8_Y5_PARENT_QLOC_1931_FINITE_SOURCE_REQUIREMENTS_NONCLAIM.csv"),
    (OUTPUTS["finite_requirements"], QUEUE / "JR1931_FIRST_SOURCE_BACKED_COEFFICIENT_ROW_QUEUE.csv"),
    (OUTPUTS["claim_gate"], QUARANTINE / "P8_Y5_PARENT_QLOC_1931_CLAIM_GATE.csv"),
]


def ensure_dirs() -> None:
    for path in [OUT, SOURCE_WEIGHT_DOCS, MICROSCOPE_COEFFS, QUEUE, QUARANTINE]:
        path.mkdir(parents=True, exist_ok=True)


def remove_pycache() -> None:
    pycache = ROOT / "scripts" / "__pycache__"
    if pycache.exists():
        shutil.rmtree(pycache)


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    if not rows:
        raise ValueError(f"no rows for {path}")
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def parse_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def source_register_rows() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for key, path in SOURCES.items():
        text = read_text(path) if path.exists() else ""
        missing = [needle for needle in NEEDLES[key] if needle not in text]
        rows.append(
            {
                "branch_id": BRANCH_ID,
                "source_key": key,
                "source_path": str(path),
                "needed_for": "1931 parent ordinary-sector action signature or explicit closure ledger",
                "needles": ";".join(NEEDLES[key]),
                "status": "EXISTS_NEEDLES_CONFIRMED" if path.exists() and not missing else "MISSING_OR_NEEDLE_FAILED",
                "missing_needles": ";".join(missing),
                "valid_for_claim": False,
                "claim_allowed": False,
                "generated_utc": GENERATED_UTC,
            }
        )
    return rows


def signature_rows() -> list[dict[str, Any]]:
    specs = [
        ("SIG1931_0_parent_domain", "declare parent ordinary-sector object language before local tests", "S_parent = S_geom[q(Phi)] + S_EM[A,T_Q,q(Phi)] + S_matter[Psi,e_obs(q),theta_rep] + allowed residual operators", "CONTRACT_NEEDED_NOT_PARENT_SIGNED", "prevents arena-by-arena hidden constant/source vertices", "finite coefficient priors remain live", "parent_object_language"),
        ("SIG1931_1_EH_or_R11_operator", "local gravitational operator is EH/GR in observed frame or explicit retained R11 operator", "E[g_obs]=kappa_ref T_total plus retained residual vector with weak-field maps", "EH_UNSIGNED_R11_TEMPLATE_ONLY", "opens actual GR/Newton/PPN reduction route", "no honest local-GR/Newton/PPN claim", "gravity_operator"),
        ("SIG1931_2_matter_spectrum_owner", "matter masses, Yukawas, QCD/binding fractions, and material responses are fixed representation/readout data", "theta_A=theta_rep or theta_bar(q); forbid m_A(Xhat), y_A(Xhat), Lambda_QCD(Xhat), B_A(Xhat)", "NOT_PARENT_SIGNED", "zeros mass/binding/composition coefficients by chain rule", "mass, binding, clock, and WEP material channels remain physical branches", "ordinary_constants"),
        ("SIG1931_3_unique_EM_owner", "unique EM kinetic owner, fixed charge generator, and no independent scalar F2 term", "Allowed -C_P/4 <F,F>_P with fixed T_Q; forbid f_X(Xhat)F_Q^2 and lambda_A F_Q^2", "FAIL_CURRENT_CORPUS_COUNTERTERM_LEGAL", "b_alpha and c_alpha theorem-zero", "alpha remains finite product-level debt", "EM_gauge_norm"),
        ("SIG1931_4_source_weight_exclusion", "no source-only species/material gravitational weights", "forbid w_A(Xhat)S_A, kappa_A(Xhat)T_A, and source-only material multipliers before variation", "CONDITIONAL_SOURCE_SCALAR_EXCLUSION_NOT_PARENT_DERIVED", "source-label forgetting and beta_source_alpha closure", "WEP/Newton-GM/R10 source normalization remains retained", "source_coupling"),
        ("SIG1931_5_no_hidden_visible_hom", "hidden invariant algebra cannot feed visible continuous coefficient spaces", "Hom(C_hid,Coeff(O_vis))=Const/0 for visible F2, mass, binding, clock, and source operators", "SCALAR_INVARIANT_COUNTEREXAMPLE_ACTIVE", "subsumes many forbidden-vertex clauses as one master no-leak theorem", "one surviving invariant scalar can generate coefficient drift", "operator_domain_master_clause"),
        ("SIG1931_6_clock_readout_owner", "clock/spectral readout descends from quotient-owned coframe plus owned constants", "nu_i(Phi)=nu_bar_i(q(Phi),theta_rep) with no nu_i(Xhat), Hodge, shadow-clock, or post-readout slot", "UNSIGNED", "clock residuals inherit upstream zero constants", "clock bound remains |b_alpha*tau_clock| product only", "readout"),
        ("SIG1931_7_radiative_readout_closure", "forbidden bare vertices do not re-enter through S_eff, loops, Hodge/readout, or post-variation projectors", "renormalized visible coefficients factor through q or theta_rep; variation precedes readout/projection", "RADIATIVE_READOUT_UNSIGNED", "bare parent signature survives observed tests", "alpha, clock, source, and readout coefficients can regenerate", "effective_readout_stability"),
        ("SIG1931_8_projection_maps", "tau_clock, tau_WEP, tau_R10, and source/test kernels are derived arena projections, not unity knobs", "tau_arena=functional[parent local state, observed frame, source worldtube, material/readout tensor, orbit/range averaging]", "PROJECTION_CONTRACTS_WRITTEN_NOT_DERIVED", "finite product branches become scoreable predictions", "runners keep valid_prediction_rows=0", "arena_projection"),
        ("SIG1931_9_Ward_Bianchi_conservation", "selectors, boundaries, hidden variables, and matter/source currents obey Bianchi/Ward compatibility or are retained residuals", "nabla_mu T_total^{mu nu}=0 in observed frame, with no silent Euler/domain/boundary leaks", "OPEN_PARALLEL_GATE", "protects GR/Newton reduction from hidden source leakage", "retained R11/local residual vector remains necessary", "conservation"),
        ("SIG1931_10_verdict", "ordinary-sector parent action signature is fully signed", "SIG1931_0 through SIG1931_9 all parent-derived or explicitly retained as residuals with runners", "NOT_DERIVED", "constant-sector universality and source coupling may be promoted to a GR-style reduction branch", "local-GR/WEP/R10/clock/alpha claims remain blocked", "summary_gate"),
    ]
    return [
        {
            "branch_id": BRANCH_ID,
            "clause_id": clause_id,
            "ordinary_sector_clause": clause,
            "minimal_form": form,
            "current_status": status,
            "derived_if_signed": derived,
            "if_unsigned": unsigned,
            "closure_kind": closure_kind,
            "valid_for_claim": False,
            "claim_allowed": False,
            "generated_utc": GENERATED_UTC,
        }
        for clause_id, clause, form, status, derived, unsigned, closure_kind in specs
    ]


def theorem_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "theorem_id": "THM1931_0_target",
            "claim": "ordinary-sector constants/source couplings are parent-owned and vertically silent",
            "formal_statement": "For every vertical v in ker(Dq), Lie_v theta_vis=0 and no source-only coefficient exists for theta_vis in {alpha, masses, binding, clocks, source weights}.",
            "status": "TARGET_NOT_PROMOTED",
            "proof_or_gap": "requires the full signature ledger, not just metric descent",
            "valid_for_claim": False,
            "claim_allowed": False,
            "generated_utc": GENERATED_UTC,
        },
        {
            "branch_id": BRANCH_ID,
            "theorem_id": "THM1931_1_chain_rule_if_signature_signed",
            "claim": "chain rule gives zero visible coefficient drift",
            "formal_statement": "theta_vis(Phi)=theta_bar(q(Phi),theta_rep) and Dq[v]=0 imply Lie_v theta_vis=0.",
            "status": "EXACT_CONDITIONAL_THEOREM",
            "proof_or_gap": "valid only after parent object language excludes direct hidden-visible coefficient maps",
            "valid_for_claim": False,
            "claim_allowed": False,
            "generated_utc": GENERATED_UTC,
        },
        {
            "branch_id": BRANCH_ID,
            "theorem_id": "THM1931_2_counterexample_if_any_clause_missing",
            "claim": "one missing clause reopens finite coefficients",
            "formal_statement": "DeltaS=c(I_hid)O_vis, f_X(Xhat)F^2, m_A(Xhat)bar(psi)psi, or w_A T_A gives Lie_v theta_vis != 0 while q is fixed.",
            "status": "COUNTEREXAMPLES_ACTIVE",
            "proof_or_gap": "current corpus explicitly retains scalar F2, hidden invariant, mass/binding, and source-weight counterexamples",
            "valid_for_claim": False,
            "claim_allowed": False,
            "generated_utc": GENERATED_UTC,
        },
        {
            "branch_id": BRANCH_ID,
            "theorem_id": "THM1931_3_GR_reduction_condition",
            "claim": "local GR/Newton reduction needs source side plus field-operator side",
            "formal_statement": "EH/R11 operator + universal Hilbert source + Ward/Bianchi compatibility + PPN/readout maps are required before gamma=beta=1 or Newtonian GM is claimed.",
            "status": "CONDITIONAL_REDUCTION_CONTRACT",
            "proof_or_gap": "ordinary-sector signature is necessary but not sufficient for local GR",
            "valid_for_claim": False,
            "claim_allowed": False,
            "generated_utc": GENERATED_UTC,
        },
        {
            "branch_id": BRANCH_ID,
            "theorem_id": "THM1931_4_verdict",
            "claim": "current MTS ordinary-sector signature is derived",
            "formal_statement": "All required ordinary-sector clauses are parent-signed and stable under readout/EFT.",
            "status": "NOT_DERIVED",
            "proof_or_gap": "several clauses are exact contracts or closures but not parent derivations",
            "valid_for_claim": False,
            "claim_allowed": False,
            "generated_utc": GENERATED_UTC,
        },
    ]


def closure_rows() -> list[dict[str, Any]]:
    specs = [
        ("CLOS1931_0_derive_now", "chain_rule_descent", "derivable_conditional", "If visible constants factor through q or fixed representation data, vertical derivatives vanish.", "use as theorem ingredient only, not final claim"),
        ("CLOS1931_1_master_closure_candidate", "no_hidden_visible_coefficient_morphism", "best_single_master_clause_but_unsigned", "Forbid hidden invariant scalars from entering visible coefficient spaces.", "next derivation target; if it fails, label as explicit closure"),
        ("CLOS1931_2_EM_specific_closure", "no_extra_F2", "needed_specific_clause", "Forbid independent f_X F_Q^2 and lambda_A F_Q^2 terms.", "cannot promote b_alpha=0 until signed"),
        ("CLOS1931_3_source_specific_closure", "no_wA_source_scalar", "needed_specific_clause", "Forbid source-only species/material weights and prevent measured-G absorption shortcuts.", "cannot promote WEP/source normalization until signed"),
        ("CLOS1931_4_readout_closure", "radiative_EFT_readout", "needed_stability_clause", "Ensure forbidden bare vertices do not reappear in effective/readout maps.", "all zero-theorem claims remain nonclaim without it"),
        ("CLOS1931_5_finite_branch", "source_backed_products", "fallback_if_theorem_fails", "Provide actual coefficient/product values, not just bounds, for clock/WEP/R10 comparisons.", "strict runners must reject placeholders"),
    ]
    return [
        {
            "branch_id": BRANCH_ID,
            "closure_id": closure_id,
            "clause_family": family,
            "classification": classification,
            "content": content,
            "claim_policy": policy,
            "valid_for_claim": False,
            "claim_allowed": False,
            "generated_utc": GENERATED_UTC,
        }
        for closure_id, family, classification, content, policy in specs
    ]


def finite_requirement_rows() -> list[dict[str, Any]]:
    specs = [
        ("FIN1931_0_alpha_coefficient", "alpha/EM", "source-backed b_alpha, c_alpha_DD, or theorem-zero no-extra-F2", "abs(c_alpha_DD or b_alpha) <= 8.320244933243533e-10 for DD/WEP pressure; clock product bound exists separately", "coefficient value/source or parent no-extra-F2 theorem"),
        ("FIN1931_1_clock_product", "clock", "numeric MTS prediction for b_alpha*tau_clock_time or tau_clock/Xhat map", "abs(b_alpha*tau_clock_time) <= 2.1e-18 yr^-1", "tau_clock_time; Xhat normalization; standalone alpha owner"),
        ("FIN1931_2_WEP_alpha_product", "WEP alpha/material", "numeric P_WEP_alpha or beta_source_alpha*tau_WEP*material response product", "direct alpha product target 4.797780522732e-05", "beta_source_alpha; tau_WEP; direct product theorem/value"),
        ("FIN1931_3_WEP_relative_source_weight", "source/WEP", "numeric abs(Delta_w_TiPt*tau_WEP) or theorem-zero no-w_A", "eta_TiPt/source-charge proxy <= 2.8e-15", "Delta_w_TiPt theorem-zero or numeric prior; tau_WEP projection"),
        ("FIN1931_4_R10_product", "R10 short range", "numeric alpha(lambda) or relative-weight product with lambda, K(lambda), source/test weights, tau_R10, and promoted bound curve", "alpha(lambda) curve required; anchor-only rows are nonclaim", "lambda/K/tau_R10/source-test product and claim-valid bound curve"),
        ("FIN1931_5_mass_binding", "mass/binding/material", "source-backed b_mu, b_mA, b_nuc, c_surface, or theorem-zero matter-spectrum owner", "abs(c_surface_DD or b_binding) <= 6.9875016461438634e-11; common DD scale <= 6.4461422294339073e-11", "coefficient value/source or parent no-mass/no-binding theorem"),
    ]
    return [
        {
            "branch_id": BRANCH_ID,
            "requirement_id": requirement_id,
            "channel": channel,
            "needed_row": needed,
            "current_bound_or_threshold": threshold,
            "missing": missing,
            "status": "SOURCE_REQUIRED_OR_THEOREM_ZERO_REQUIRED",
            "valid_for_claim": False,
            "claim_allowed": False,
            "generated_utc": GENERATED_UTC,
        }
        for requirement_id, channel, needed, threshold, missing in specs
    ]


def claim_gate_rows() -> list[dict[str, Any]]:
    return [
        ("CG1931_0_parent_signature", "ordinary-sector parent action signature is derived", "FAIL_SIGNATURE_UNSIGNED", "signature ledger contains multiple unsigned clauses and active counterexamples"),
        ("CG1931_1_alpha_zero", "b_alpha or c_alpha is theorem-zero", "FAIL_EM_OWNER_UNSIGNED", "unique EM kinetic owner/no-extra-F2 clause remains unsigned"),
        ("CG1931_2_source_weight_zero", "relative source weights vanish", "FAIL_SOURCE_WEIGHT_UNSIGNED", "source-scalar exclusion remains conditional and not parent-derived"),
        ("CG1931_3_constant_universality", "alpha, masses, binding, clocks, and source constants are vertically silent", "FAIL_MASTER_MORPHISM_AND_READOUT_OPEN", "hidden-visible coefficient morphism and radiative/readout closure remain open"),
        ("CG1931_4_local_GR_Newton", "local GR/Newton is derived", "FAIL_LOCAL_GR_NEEDS_MORE_GATES", "ordinary-sector signature is only one gate; EH/R11 operator, source charge, Ward/Bianchi, and PPN readout remain required"),
        ("CG1931_5_finite_product_claims", "clock/WEP/R10 finite products are scoreable", "FAIL_PRODUCTS_PLACEHOLDER_OR_BOUND_ONLY", "tau/projection and product values remain missing; bounds alone are not predictions"),
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "decision_id": "DEC1931_0_signature_status",
            "decision": "PARENT_ORDINARY_SECTOR_SIGNATURE_EXPLICIT_NOT_DERIVED",
            "because": "1931 combines source-weight, EM, hidden-invariant, mass/binding, clock/readout, projection, radiative, and conservation clauses into one ledger",
            "next_action": "do not claim local GR/WEP/R10/clock silence from this checkpoint",
            "valid_for_claim": False,
            "claim_allowed": False,
            "generated_utc": GENERATED_UTC,
        },
        {
            "branch_id": BRANCH_ID,
            "decision_id": "DEC1931_1_best_derivation_target",
            "decision": "ATTACK_MASTER_NO_HIDDEN_VISIBLE_COEFFICIENT_MORPHISM_NEXT",
            "because": "it is the smallest clause that could subsume no-extra-F2, mass/binding vertices, source weights, and readout coefficient leaks",
            "next_action": "derive it from parent object-language typing or demote it to explicit closure pack",
            "valid_for_claim": False,
            "claim_allowed": False,
            "generated_utc": GENERATED_UTC,
        },
        {
            "branch_id": BRANCH_ID,
            "decision_id": "DEC1931_2_finite_branch_policy",
            "decision": "FINITE_BRANCHES_REMAIN_PRESSURE_TESTS_ONLY",
            "because": "current rows contain bounds and thresholds, not MTS coefficient/product predictions",
            "next_action": "strict runners continue to reject placeholders and unity shortcuts",
            "valid_for_claim": False,
            "claim_allowed": False,
            "generated_utc": GENERATED_UTC,
        },
    ]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "route_id": "NEXT1931_0_primary",
            "selection_status": "selected",
            "target_doc": "1932-Y5-R2FR-master-no-hidden-visible-coefficient-morphism-or-explicit-closure-pack.md",
            "target_script": "scripts/Y5_R2FR_master_no_hidden_visible_coefficient_morphism_or_explicit_closure_pack_1932.py",
            "objective": "derive the master no-hidden-visible coefficient morphism from parent object-language typing and quotient/category structure; otherwise demote it to an explicit closure pack and list finite source rows required for alpha, WEP/source weights, clocks, R10, and mass/binding",
            "success_condition": "a signed master morphism theorem, or an explicit closure pack with finite source requirements and all local-GR/WEP/R10/clock claims blocked",
            "do_not": "do not claim local GR, set coefficients to zero by taste, set tau=1, use standalone b_alpha, absorb relative weights into measured G, or modify formalization-workbench",
            "valid_for_claim": False,
            "claim_allowed": False,
            "generated_utc": GENERATED_UTC,
        }
    ]


def snapshot_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "snapshot_id": "STAT1931_0_gain",
            "area": "ordinary-sector synthesis",
            "summary": "1931 turns the coupling leaks into one parent-action signature ledger instead of separate alpha/WEP/clock/R10 loops.",
            "status": "SIGNATURE_EXPLICIT_NOT_DERIVED",
            "what_it_means": "the framework now has a clear contract for what must be parent-derived versus retained as residuals",
            "next": "master no-hidden-visible coefficient morphism",
            "valid_for_claim": False,
            "claim_allowed": False,
            "generated_utc": GENERATED_UTC,
        },
        {
            "branch_id": BRANCH_ID,
            "snapshot_id": "STAT1931_1_GR_reduction",
            "area": "GR/Newton route",
            "summary": "ordinary-sector closure is necessary but not sufficient for local GR/Newton; EH/R11 operator, universal source, Ward/Bianchi, and PPN/readout gates remain required.",
            "status": "LOCAL_GR_NOT_CLAIMED",
            "what_it_means": "we keep the reduction ambition alive without smuggling it through coupling cleanup",
            "next": "master morphism or explicit closure pack",
            "valid_for_claim": False,
            "claim_allowed": False,
            "generated_utc": GENERATED_UTC,
        },
    ]


def build_rows() -> dict[str, list[dict[str, Any]]]:
    claim_rows = [
        {
            "branch_id": BRANCH_ID,
            "gate_id": gate_id,
            "claim": claim,
            "status": status,
            "reason": reason,
            "valid_for_claim": False,
            "claim_allowed": False,
            "generated_utc": GENERATED_UTC,
        }
        for gate_id, claim, status, reason in claim_gate_rows()
    ]
    return {
        "source_register": source_register_rows(),
        "signature": signature_rows(),
        "theorem": theorem_rows(),
        "closure": closure_rows(),
        "finite_requirements": finite_requirement_rows(),
        "claim_gate": claim_rows,
        "decision": decision_rows(),
        "next_target": next_target_rows(),
        "snapshot": snapshot_rows(),
    }


def copy_branch_artifacts() -> None:
    for source, destination in BRANCH_COPIES:
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(source, destination)


def validation_rows() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    sources = parse_csv(OUTPUTS["source_register"])
    rows.append({"validation_id": "VAL1931_00_sources", "status": "PASS" if all(row["status"] == "EXISTS_NEEDLES_CONFIRMED" for row in sources) else "FAIL", "detail": "all local source paths exist and needles found", "valid_for_claim": False, "claim_allowed": False})
    signature = parse_csv(OUTPUTS["signature"])
    rows.append({"validation_id": "VAL1931_01_signature_complete", "status": "PASS" if len(signature) == 11 and any(row["clause_id"] == "SIG1931_10_verdict" and row["current_status"] == "NOT_DERIVED" for row in signature) else "FAIL", "detail": "signature ledger covers parent domain, gravity, matter, EM, source, hidden morphism, readout, projection, conservation, and verdict", "valid_for_claim": False, "claim_allowed": False})
    theorem = parse_csv(OUTPUTS["theorem"])
    rows.append({"validation_id": "VAL1931_02_theorem_conditional", "status": "PASS" if any(row["status"] == "EXACT_CONDITIONAL_THEOREM" for row in theorem) and any(row["status"] == "NOT_DERIVED" for row in theorem) else "FAIL", "detail": "chain-rule theorem retained as conditional and not promoted", "valid_for_claim": False, "claim_allowed": False})
    closure = parse_csv(OUTPUTS["closure"])
    rows.append({"validation_id": "VAL1931_03_closure_separation", "status": "PASS" if len(closure) == 6 and any(row["classification"] == "best_single_master_clause_but_unsigned" for row in closure) and any(row["classification"] == "fallback_if_theorem_fails" for row in closure) else "FAIL", "detail": "explicit closure ledger separates derivable, master, specific, readout, and finite branches", "valid_for_claim": False, "claim_allowed": False})
    finite = parse_csv(OUTPUTS["finite_requirements"])
    rows.append({"validation_id": "VAL1931_04_finite_requirements", "status": "PASS" if len(finite) == 6 and all(row["status"] == "SOURCE_REQUIRED_OR_THEOREM_ZERO_REQUIRED" for row in finite) else "FAIL", "detail": "finite source requirements staged for alpha, clock, WEP, source, R10, and mass/binding", "valid_for_claim": False, "claim_allowed": False})
    gates = parse_csv(OUTPUTS["claim_gate"])
    rows.append({"validation_id": "VAL1931_05_claim_gates_blocked", "status": "PASS" if len(gates) == 6 and all(row["status"].startswith("FAIL") for row in gates) else "FAIL", "detail": "all local GR/WEP/R10/clock/alpha claim gates remain blocked", "valid_for_claim": False, "claim_allowed": False})
    decisions = parse_csv(OUTPUTS["decision"])
    rows.append({"validation_id": "VAL1931_06_decision", "status": "PASS" if any(row["decision"] == "ATTACK_MASTER_NO_HIDDEN_VISIBLE_COEFFICIENT_MORPHISM_NEXT" for row in decisions) else "FAIL", "detail": "master morphism selected as next target", "valid_for_claim": False, "claim_allowed": False})
    next_rows = parse_csv(OUTPUTS["next_target"])
    rows.append({"validation_id": "VAL1931_07_next_target", "status": "PASS" if next_rows[0]["target_doc"].startswith("1932-Y5-R2FR-master-no-hidden-visible") else "FAIL", "detail": "1932 master morphism target selected", "valid_for_claim": False, "claim_allowed": False})
    generated = [path for key, path in OUTPUTS.items() if key != "validation"]
    csv_ok = True
    claim_safe = True
    for path in generated:
        try:
            parsed = parse_csv(path)
            csv_ok = csv_ok and bool(parsed)
            for row in parsed:
                if row.get("valid_for_claim", "False") != "False" or row.get("claim_allowed", "False") != "False":
                    claim_safe = False
        except Exception:
            csv_ok = False
    rows.append({"validation_id": "VAL1931_08_claim_flags_safe", "status": "PASS" if claim_safe else "FAIL", "detail": "claim flags all false", "valid_for_claim": False, "claim_allowed": False})
    rows.append({"validation_id": "VAL1931_09_csv_parse", "status": "PASS" if csv_ok else "FAIL", "detail": "all generated CSVs parse with rows", "valid_for_claim": False, "claim_allowed": False})
    rows.append({"validation_id": "VAL1931_10_branch_copies", "status": "PASS" if all(destination.exists() for _, destination in BRANCH_COPIES) else "FAIL", "detail": "; ".join(str(destination) for _, destination in BRANCH_COPIES), "valid_for_claim": False, "claim_allowed": False})
    pycache = ROOT / "scripts" / "__pycache__"
    rows.append({"validation_id": "VAL1931_11_pycache_absent", "status": "PASS" if not pycache.exists() else "FAIL", "detail": str(pycache), "valid_for_claim": False, "claim_allowed": False})
    formalization_count = 0
    if FORMALIZATION.exists():
        formalization_count = sum(1 for path in FORMALIZATION.rglob("*") if path.name.startswith("1931-") or "_1931" in path.name or "1931_" in path.name or "Y5_R2FR_parent_ordinary" in path.name)
    rows.append({"validation_id": "VAL1931_12_formalization_untouched", "status": "PASS" if formalization_count == 0 else "FAIL", "detail": f"formalization_1931_artifact_count={formalization_count}", "valid_for_claim": False, "claim_allowed": False})
    overall = all(row["status"] == "PASS" for row in rows)
    rows.append({"validation_id": "VAL1931_OVERALL", "status": "PASS" if overall else "FAIL", "detail": "1931 parent ordinary-sector action signature or explicit closure ledger", "valid_for_claim": False, "claim_allowed": False})
    return rows


def markdown_table(rows: list[dict[str, Any]]) -> str:
    headers = list(rows[0].keys())
    lines = ["| " + " | ".join(headers) + " |", "| " + " | ".join("---" for _ in headers) + " |"]
    for row in rows:
        lines.append("| " + " | ".join(str(row.get(header, "")).replace("\n", " ").replace("|", "\\|") for header in headers) + " |")
    return "\n".join(lines)


def write_doc(rows_by_name: dict[str, list[dict[str, Any]]]) -> None:
    validation = validation_rows()
    content = f"""# 1931 - Parent Ordinary-Sector Action Signature Or Explicit Closure Ledger

## Purpose

This checkpoint synthesizes the repeated coupling leaks into one ordinary-sector parent action signature. It separates what is an exact conditional theorem, what is an explicit closure candidate, and what remains a finite source-backed product requirement.

## Result

- The ordinary-sector signature is explicit but not derived.
- The chain-rule/descent theorem is valid only after parent object language excludes hidden-visible coefficient maps.
- The master no-hidden-visible coefficient morphism is the smallest next derivation target.
- Local GR/Newton still needs additional gates: EH/R11 operator, universal Hilbert source, Ward/Bianchi compatibility, and PPN/readout maps.
- Finite product branches remain internal pressure tests until actual sourced predictions exist.

## Source Register

{markdown_table(rows_by_name["source_register"])}

## Parent Signature Ledger

{markdown_table(rows_by_name["signature"])}

## Conditional Theorem

{markdown_table(rows_by_name["theorem"])}

## Explicit Closure Ledger

{markdown_table(rows_by_name["closure"])}

## Finite Source Requirements

{markdown_table(rows_by_name["finite_requirements"])}

## Claim Gate

{markdown_table(rows_by_name["claim_gate"])}

## Decision Ledger

{markdown_table(rows_by_name["decision"])}

## Next Target

{markdown_table(rows_by_name["next_target"])}

## Project Status Snapshot

{markdown_table(rows_by_name["snapshot"])}

## Validation

{markdown_table(validation)}
"""
    DOC.write_text(content, encoding="utf-8")


def main() -> None:
    ensure_dirs()
    remove_pycache()
    rows_by_name = build_rows()
    for key, rows in rows_by_name.items():
        write_csv(OUTPUTS[key], rows)
    copy_branch_artifacts()
    remove_pycache()
    write_csv(OUTPUTS["validation"], validation_rows())
    write_doc(rows_by_name)


if __name__ == "__main__":
    main()

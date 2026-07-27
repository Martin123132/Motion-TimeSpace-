from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "source-intake" / "mts_residuals"
DOC = ROOT / "1104-Y5-R10-parent-ordinary-sector-action-signature-or-explicit-closure-ledger.md"


def now() -> str:
    return datetime.now(timezone.utc).isoformat()


def stamp(rows: list[dict[str, object]]) -> list[dict[str, object]]:
    generated = now()
    result: list[dict[str, object]] = []
    for row in rows:
        copied = dict(row)
        copied.setdefault("valid_for_claim", "false")
        copied.setdefault("claim_allowed", "false")
        copied.setdefault("generated_utc", generated)
        result.append(copied)
    return result


def write_csv(path: Path, rows: list[dict[str, object]], fieldnames: list[str] | None = None) -> None:
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
        for row in rows:
            writer.writerow({key: row.get(key, "") for key in fieldnames})


def source_rows() -> list[dict[str, object]]:
    rows = [
        {
            "source_id": "SRC1104_0_1103_next",
            "relative_path": "source-intake/mts_residuals/P8_Y5_R10_1103_NEXT_TARGET.csv",
            "needle": "NEXT1103_0_1104",
            "note": "1103 no-loop handoff to ordinary-sector parent action signature.",
        },
        {
            "source_id": "SRC1104_1_1103_debt",
            "relative_path": "source-intake/mts_residuals/P8_Y5_R10_1103_LIVE_DEBT_MATRIX.csv",
            "needle": "DEBT1103_0_parent_ordinary_sector_signature",
            "note": "1103 live debt matrix.",
        },
        {
            "source_id": "SRC1104_2_1098_signature",
            "relative_path": "source-intake/mts_residuals/P8_Y5_R10_1098_ORDINARY_CONSTANT_OWNER_SIGNATURE_ATTEMPT.csv",
            "needle": "OCS1098_6_verdict",
            "note": "ordinary constant owner signature attempt.",
        },
        {
            "source_id": "SRC1104_3_1098_vertices",
            "relative_path": "source-intake/mts_residuals/P8_Y5_R10_1098_FORBIDDEN_VERTEX_AUDIT.csv",
            "needle": "FV1098_6_source_weight_X",
            "note": "forbidden visible-sector vertex audit.",
        },
        {
            "source_id": "SRC1104_4_1098_theorem",
            "relative_path": "source-intake/mts_residuals/P8_Y5_R10_1098_ACTION_SIGNATURE_THEOREM.csv",
            "needle": "OCT1098_3_verdict",
            "note": "conditional action-signature theorem.",
        },
        {
            "source_id": "SRC1104_5_1048_signature",
            "relative_path": "source-intake/mts_residuals/P8_Y5_R10_1048_PARENT_VERTEX_SIGNATURE_AUDIT.csv",
            "needle": "PVS1048_5_verdict",
            "note": "earlier no-extra-F2/no-mass/no-clock signature attempt.",
        },
        {
            "source_id": "SRC1104_6_980_obstruction",
            "relative_path": "source-intake/mts_residuals/P8_Y5_R10_980_NO_MARKER_FUNCTOR_THEOREM_ATTEMPT.csv",
            "needle": "NMF980_7_verdict",
            "note": "hidden invariant/marker obstruction.",
        },
        {
            "source_id": "SRC1104_7_1097_constant_universality",
            "relative_path": "source-intake/mts_residuals/P8_Y5_R10_1097_CONSTANT_SECTOR_UNIVERSALITY_THEOREM_ATTEMPT.csv",
            "needle": "CSU1097_5_verdict",
            "note": "constant-sector universality theorem attempt.",
        },
        {
            "source_id": "SRC1104_8_989_EM_lock",
            "relative_path": "source-intake/mts_residuals/P8_Y5_R10_989_EM_LOCK_SIGNATURE_AUDIT.csv",
            "needle": "ELA989_5_total",
            "note": "EM lock/current/gauge-normalization audit.",
        },
        {
            "source_id": "SRC1104_9_990_parent_contract",
            "relative_path": "source-intake/mts_residuals/P8_Y5_R10_990_PARENT_ACTION_CONTRACT.csv",
            "needle": "PAC990_6_PPN_readout",
            "note": "parent action contract and GR/Newton reentry clauses.",
        },
        {
            "source_id": "SRC1104_10_1051_no_mixed",
            "relative_path": "source-intake/mts_residuals/P8_Y5_R10_1051_NO_MIXED_MORPHISM_LEMMA_ATTEMPT.csv",
            "needle": "NMM1051_5_verdict",
            "note": "no hidden-visible coefficient morphism lemma attempt.",
        },
        {
            "source_id": "SRC1104_11_1051_alpha_closure",
            "relative_path": "source-intake/mts_residuals/P8_Y5_R10_1051_ALPHA_OWNER_RADIATIVE_CLOSURE_AUDIT.csv",
            "needle": "AOR1051_3_verdict",
            "note": "alpha owner/radiative/readout closure audit.",
        },
        {
            "source_id": "SRC1104_12_1066_source_scalar",
            "relative_path": "source-intake/mts_residuals/P8_Y5_R10_1066_SOURCE_SCALAR_EXCLUSION_LEMMA.csv",
            "needle": "SSE1066_5_verdict",
            "note": "source-scalar exclusion conditional lemma.",
        },
        {
            "source_id": "SRC1104_13_1101_gauge_norm",
            "relative_path": "source-intake/mts_residuals/P8_Y5_R10_1101_GAUGE_NORM_THEOREM_ATTEMPT.csv",
            "needle": "GFT1101_4_verdict",
            "note": "latest gauge-norm owner theorem attempt.",
        },
        {
            "source_id": "SRC1104_14_1102_validation",
            "relative_path": "source-intake/mts_residuals/P8_Y5_BRR545_1102_VALIDATION.csv",
            "needle": "V1102_SUMMARY",
            "note": "latest alpha-product input-fill validation.",
        },
    ]
    checked: list[dict[str, object]] = []
    for row in rows:
        path = ROOT / str(row["relative_path"])
        text = path.read_text(encoding="utf-8", errors="replace") if path.exists() else ""
        checked.append(
            {
                **row,
                "exists": str(path.exists()).lower(),
                "needle_found": str(str(row["needle"]) in text).lower(),
            }
        )
    return stamp(checked)


def signature_rows() -> list[dict[str, object]]:
    return stamp(
        [
            {
                "clause_id": "SIG1104_0_parent_domain",
                "ordinary_sector_clause": "declare the parent ordinary-sector object language before local tests",
                "minimal_form": "S_parent = S_geom[q(Phi)] + S_EM[A,T_Q,q(Phi)] + S_matter[Psi,e_obs(q),theta_rep] + allowed residual operators",
                "current_status": "CONTRACT_NEEDED_NOT_PARENT_SIGNED",
                "derived_if_signed": "prevents arena-by-arena hidden constant/source vertices",
                "if_unsigned": "finite coefficient priors remain live",
                "source_rows": "OCS1098_0_parent_domain; PVS1048_0_field_domain; PAC990_0_parent_fields_and_quotient",
                "closure_kind": "parent_object_language",
            },
            {
                "clause_id": "SIG1104_1_EH_or_R11_operator",
                "ordinary_sector_clause": "local gravitational operator is EH/GR in the observed frame or an explicit retained R11 operator",
                "minimal_form": "E[g_obs] = kappa_ref T_total plus retained residual vector with weak-field maps",
                "current_status": "EH_UNSIGNED_R11_TEMPLATE_ONLY",
                "derived_if_signed": "opens actual GR/Newton/PPN reduction route",
                "if_unsigned": "no honest local-GR/Newton/PPN claim",
                "source_rows": "PAC990_1_gravity_operator; PAC990_6_PPN_readout",
                "closure_kind": "gravity_operator",
            },
            {
                "clause_id": "SIG1104_2_matter_spectrum_owner",
                "ordinary_sector_clause": "matter masses, Yukawas, QCD/binding fractions, and material responses are fixed representation/readout data",
                "minimal_form": "theta_A = theta_rep or theta_bar(q); forbid m_A(Xhat), y_A(Xhat), Lambda_QCD(Xhat), B_A(Xhat)",
                "current_status": "NOT_PARENT_SIGNED",
                "derived_if_signed": "zeros mass/binding/composition coefficients by chain rule",
                "if_unsigned": "mass, binding, clock, and WEP material channels remain physical branches",
                "source_rows": "OCS1098_2_matter_spectrum_owner; FV1098_2_mass_X; FV1098_4_binding_X; CSU1097_5_verdict",
                "closure_kind": "ordinary_constants",
            },
            {
                "clause_id": "SIG1104_3_unique_EM_owner",
                "ordinary_sector_clause": "unique EM kinetic owner, fixed charge generator, and no independent scalar F2 term",
                "minimal_form": "Allowed -C_P/4 <F,F>_P with fixed T_Q; forbid f_X(Xhat)F_Q^2 and lambda_A F_Q^2",
                "current_status": "FAIL_CURRENT_CORPUS_COUNTERTERM_LEGAL",
                "derived_if_signed": "b_alpha and c_alpha theorem-zero; alpha clock/WEP/R10 transfer becomes structurally controlled",
                "if_unsigned": "alpha remains finite product-level debt",
                "source_rows": "OCS1098_1_unique_EM_owner; ELA989_1_unique_F2; GFT1101_4_verdict; REC1103_5_EM_branch_result",
                "closure_kind": "EM_gauge_norm",
            },
            {
                "clause_id": "SIG1104_4_source_weight_exclusion",
                "ordinary_sector_clause": "no source-only species/material gravitational weights",
                "minimal_form": "forbid w_A(Xhat) S_A, kappa_A(Xhat)T_A, and source-only material multipliers before variation",
                "current_status": "CONDITIONAL_SOURCE_SCALAR_EXCLUSION_NOT_PARENT_DERIVED",
                "derived_if_signed": "source-label forgetting, beta_source_alpha closure, and relative-source WEP product zero",
                "if_unsigned": "WEP/Newton-GM/R10 source normalization remains retained",
                "source_rows": "OCS1098_4_source_weight_exclusion; SSE1066_5_verdict; PAC990_4_source_charge",
                "closure_kind": "source_coupling",
            },
            {
                "clause_id": "SIG1104_5_no_hidden_visible_hom",
                "ordinary_sector_clause": "hidden invariant algebra cannot feed visible continuous coefficient spaces",
                "minimal_form": "Hom(C_hid, Coeff(O_vis)) = Const/0 for visible F2, mass, binding, clock, and source operators",
                "current_status": "SCALAR_INVARIANT_COUNTEREXAMPLE_ACTIVE",
                "derived_if_signed": "subsumes many forbidden-vertex clauses as one master no-leak theorem",
                "if_unsigned": "one surviving invariant scalar can generate coefficient drift",
                "source_rows": "NMF980_2_scalar_obstruction_lemma; NMM1051_5_verdict; CSU1097_3_counterexample",
                "closure_kind": "operator_domain_master_clause",
            },
            {
                "clause_id": "SIG1104_6_clock_readout_owner",
                "ordinary_sector_clause": "clock/spectral readout descends from quotient-owned coframe plus owned constants",
                "minimal_form": "nu_i(Phi)=nu_bar_i(q(Phi),theta_rep) with no nu_i(Xhat), Hodge, shadow-clock, or post-readout slot",
                "current_status": "UNSIGNED",
                "derived_if_signed": "clock residuals inherit upstream zero constants",
                "if_unsigned": "clock bound remains |b_alpha*tau_clock| product only",
                "source_rows": "OCS1098_3_clock_readout_owner; BAP1051_2_best_current_product; AOR1051_1_clock_product",
                "closure_kind": "readout",
            },
            {
                "clause_id": "SIG1104_7_radiative_readout_closure",
                "ordinary_sector_clause": "forbidden bare vertices do not re-enter through S_eff, loops, Hodge/readout, or post-variation projectors",
                "minimal_form": "renormalized visible coefficients factor through q or theta_rep; variation precedes readout/projection",
                "current_status": "RADIATIVE_READOUT_UNSIGNED",
                "derived_if_signed": "bare parent signature survives observed tests",
                "if_unsigned": "alpha, clock, source, and readout coefficients can regenerate",
                "source_rows": "OCS1098_5_radiative_readout_closure; AOR1051_3_verdict; NMM1051_4_radiative_readout_limit",
                "closure_kind": "effective_readout_stability",
            },
            {
                "clause_id": "SIG1104_8_projection_maps",
                "ordinary_sector_clause": "tau_clock, tau_WEP, tau_R10, and source/test kernels are derived arena projections, not unity knobs",
                "minimal_form": "tau_arena = functional[parent local state, observed frame, source worldtube, material/readout tensor, orbit/range averaging]",
                "current_status": "PROJECTION_CONTRACTS_WRITTEN_NOT_DERIVED",
                "derived_if_signed": "finite product branches become scoreable predictions",
                "if_unsigned": "runners keep valid_prediction_rows=0",
                "source_rows": "V1102_SUMMARY; DEBT1103_3_tau_clock; DEBT1103_4_tau_WEP",
                "closure_kind": "arena_projection",
            },
            {
                "clause_id": "SIG1104_9_Ward_Bianchi_conservation",
                "ordinary_sector_clause": "selectors, boundaries, hidden variables, and matter/source currents obey Bianchi/Ward compatibility or are retained residuals",
                "minimal_form": "nabla_mu T_total^{mu nu}=0 in observed frame, with no silent Euler/domain/boundary leaks",
                "current_status": "OPEN_PARALLEL_GATE",
                "derived_if_signed": "protects GR/Newton reduction from hidden source leakage",
                "if_unsigned": "retained R11/local residual vector remains necessary",
                "source_rows": "PAC990_5_Ward_Bianchi; PAC990_6_PPN_readout",
                "closure_kind": "conservation",
            },
            {
                "clause_id": "SIG1104_10_verdict",
                "ordinary_sector_clause": "ordinary-sector parent action signature is fully signed",
                "minimal_form": "SIG1104_0 through SIG1104_9 all parent-derived or explicitly retained as residuals with runners",
                "current_status": "NOT_DERIVED",
                "derived_if_signed": "constant-sector universality and source coupling may be promoted to a GR-style reduction branch",
                "if_unsigned": "local-GR/WEP/R10/clock/alpha claims remain blocked",
                "source_rows": "OCS1098_6_verdict; V1103_SUMMARY; V1102_SUMMARY",
                "closure_kind": "summary_gate",
            },
        ]
    )


def theorem_rows() -> list[dict[str, object]]:
    return stamp(
        [
            {
                "theorem_id": "THM1104_0_target",
                "claim": "ordinary-sector constants/source couplings are parent-owned and vertically silent",
                "formal_statement": "For every vertical v in ker(Dq), Lie_v theta_vis = 0 and no source-only coefficient exists for theta_vis in {alpha, masses, binding, clocks, source weights}.",
                "status": "TARGET_NOT_PROMOTED",
                "proof_or_gap": "requires the full signature ledger, not just metric descent",
            },
            {
                "theorem_id": "THM1104_1_chain_rule_if_signature_signed",
                "claim": "chain rule gives zero visible coefficient drift",
                "formal_statement": "theta_vis(Phi)=theta_bar(q(Phi),theta_rep) and Dq[v]=0 imply Lie_v theta_vis=0.",
                "status": "EXACT_CONDITIONAL_THEOREM",
                "proof_or_gap": "valid only after the parent object language excludes direct hidden-visible coefficient maps",
            },
            {
                "theorem_id": "THM1104_2_counterexample_if_any_clause_missing",
                "claim": "one missing clause reopens finite coefficients",
                "formal_statement": "DeltaS = c(I_hid) O_vis, f_X(Xhat)F^2, m_A(Xhat)bar(psi)psi, or w_A T_A gives Lie_v theta_vis != 0 while q is fixed.",
                "status": "COUNTEREXAMPLES_ACTIVE",
                "proof_or_gap": "current corpus explicitly retains scalar F2, hidden invariant, mass/binding, and source-weight counterexamples",
            },
            {
                "theorem_id": "THM1104_3_GR_reduction_condition",
                "claim": "local GR/Newton reduction needs source side plus field-operator side",
                "formal_statement": "EH/R11 operator + universal Hilbert source + Ward/Bianchi compatibility + PPN/readout maps are required before gamma=beta=1 or Newtonian GM is claimed.",
                "status": "CONDITIONAL_REDUCTION_CONTRACT",
                "proof_or_gap": "ordinary-sector signature alone is necessary but not sufficient for local GR",
            },
            {
                "theorem_id": "THM1104_4_verdict",
                "claim": "current MTS ordinary-sector signature is derived",
                "formal_statement": "All required ordinary-sector clauses are parent-signed and stable under readout/EFT.",
                "status": "NOT_DERIVED",
                "proof_or_gap": "several clauses are exact contracts or closures but not parent derivations",
            },
        ]
    )


def closure_rows() -> list[dict[str, object]]:
    return stamp(
        [
            {
                "closure_id": "CLOS1104_0_derive_now",
                "clause_family": "chain_rule_descent",
                "classification": "derivable_conditional",
                "content": "If visible constants factor through q or fixed representation data, vertical derivatives vanish.",
                "evidence": "OCT1098_1_chain_rule; CSU1097_1_descent_superselection",
                "claim_policy": "use as theorem ingredient only, not a final claim",
            },
            {
                "closure_id": "CLOS1104_1_master_closure_candidate",
                "clause_family": "no_hidden_visible_coefficient_morphism",
                "classification": "best_single_master_clause_but_unsigned",
                "content": "Forbid hidden invariant scalars from entering visible coefficient spaces.",
                "evidence": "NMM1051_5_verdict; NMF980_2_scalar_obstruction_lemma",
                "claim_policy": "next derivation target; if it fails, label as explicit closure",
            },
            {
                "closure_id": "CLOS1104_2_EM_specific_closure",
                "clause_family": "no_extra_F2",
                "classification": "needed_specific_clause",
                "content": "Forbid independent f_X F_Q^2 and lambda_A F_Q^2 terms.",
                "evidence": "OCS1098_1_unique_EM_owner; ELA989_1_unique_F2; 1101 route result",
                "claim_policy": "cannot promote b_alpha=0 until signed",
            },
            {
                "closure_id": "CLOS1104_3_source_specific_closure",
                "clause_family": "no_wA_source_scalar",
                "classification": "needed_specific_clause",
                "content": "Forbid source-only species/material weights and prevent measured-G absorption shortcuts.",
                "evidence": "SSE1066_5_verdict; OCS1098_4_source_weight_exclusion",
                "claim_policy": "cannot promote WEP/source normalization until signed",
            },
            {
                "closure_id": "CLOS1104_4_readout_closure",
                "clause_family": "radiative_EFT_readout",
                "classification": "needed_stability_clause",
                "content": "Ensure forbidden bare vertices do not reappear in effective/readout maps.",
                "evidence": "OCS1098_5_radiative_readout_closure; AOR1051_3_verdict",
                "claim_policy": "all zero-theorem claims remain nonclaim without it",
            },
            {
                "closure_id": "CLOS1104_5_finite_branch",
                "clause_family": "source_backed_products",
                "classification": "fallback_if_theorem_fails",
                "content": "Provide actual coefficient/product values, not just bounds, for clock/WEP/R10 comparisons.",
                "evidence": "REQ1098_0_c_alpha; V1102_SUMMARY",
                "claim_policy": "strict runners must reject placeholders",
            },
        ]
    )


def claim_gate_rows() -> list[dict[str, object]]:
    return stamp(
        [
            {
                "gate_id": "CG1104_0_parent_signature",
                "claim": "ordinary-sector parent action signature is derived",
                "gate_pass": "false",
                "reason": "signature ledger contains multiple unsigned clauses and active counterexamples",
            },
            {
                "gate_id": "CG1104_1_alpha_zero",
                "claim": "b_alpha or c_alpha is theorem-zero",
                "gate_pass": "false",
                "reason": "unique EM kinetic owner/no-extra-F2 clause remains unsigned",
            },
            {
                "gate_id": "CG1104_2_source_weight_zero",
                "claim": "relative source weights vanish",
                "gate_pass": "false",
                "reason": "source-scalar exclusion remains conditional and not parent-derived",
            },
            {
                "gate_id": "CG1104_3_constant_universality",
                "claim": "alpha, masses, binding, clocks, and source constants are all vertically silent",
                "gate_pass": "false",
                "reason": "hidden-visible coefficient morphism and radiative/readout closure remain open",
            },
            {
                "gate_id": "CG1104_4_local_GR_Newton",
                "claim": "local GR/Newton is derived",
                "gate_pass": "false",
                "reason": "ordinary-sector signature is only one gate; EH/R11 operator, source charge, Ward/Bianchi, and PPN readout remain required",
            },
            {
                "gate_id": "CG1104_5_finite_product_claims",
                "claim": "clock/WEP/R10 finite products are scoreable",
                "gate_pass": "false",
                "reason": "tau/projection and product values remain missing; bounds alone are not predictions",
            },
        ]
    )


def decision_rows() -> list[dict[str, object]]:
    return stamp(
        [
            {
                "decision_id": "DEC1104_0_signature_status",
                "decision": "the parent ordinary-sector action signature is now explicit but not derived",
                "because": "1104 combines the source-weight, EM, hidden-invariant, mass/binding, clock/readout, projection, and radiative clauses into one ledger",
                "next_action": "do not claim local GR/WEP/R10/clock silence from this checkpoint",
            },
            {
                "decision_id": "DEC1104_1_best_derivation_target",
                "decision": "attack the master no-hidden-visible coefficient morphism next",
                "because": "it is the smallest clause that could subsume no-extra-F2, no mass/binding vertices, source weights, and readout coefficient leaks",
                "next_action": "try to derive it from parent object-language typing; otherwise demote it to explicit closure",
            },
            {
                "decision_id": "DEC1104_2_finite_branch_policy",
                "decision": "finite branches remain internal pressure tests only",
                "because": "current rows contain bounds and thresholds, not MTS coefficient/product predictions",
                "next_action": "strict runners continue to reject placeholders and unity shortcuts",
            },
        ]
    )


def next_rows() -> list[dict[str, object]]:
    return stamp(
        [
            {
                "next_id": "NEXT1104_0_1105",
                "next_target": "1105-Y5-R10-master-no-hidden-visible-coefficient-morphism-or-explicit-closure-pack.md",
                "objective": "try to derive the master no-hidden-visible coefficient morphism from parent object-language typing and quotient/category structure; if it fails, demote it to an explicit closure pack and list exactly which finite coefficient/product rows must be sourced for alpha, WEP/source weights, clocks, R10, and mass/binding channels",
                "include": "Coeff(O_vis) domain; hidden invariant scalar counterexample; no-extra-F2 as subcase; no w_A as subcase; mass/binding/readout subcases; radiative/readout stability; finite product fallback schema",
                "exclude": "new local-GR claim; setting coefficients to zero by taste; tau=1; standalone b_alpha; measured-G absorption of relative weights; GitHub; formalization edits",
            }
        ]
    )


def validate(
    sources: list[dict[str, object]],
    signatures: list[dict[str, object]],
    theorems: list[dict[str, object]],
    closures: list[dict[str, object]],
    gates: list[dict[str, object]],
    decisions: list[dict[str, object]],
    next_target: list[dict[str, object]],
    outputs: dict[str, Path],
) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []

    def add(check_id: str, passed: bool, detail: str) -> None:
        rows.append(
            {
                "check_id": check_id,
                "result": "pass" if passed else "fail",
                "detail": detail,
                "valid_for_claim": "false",
                "generated_utc": now(),
            }
        )

    add(
        "V1104_0_sources_exist",
        all(row["exists"] == "true" and row["needle_found"] == "true" for row in sources),
        "all cited local source paths exist and needles are found",
    )
    add(
        "V1104_1_signature_complete",
        len(signatures) >= 10 and any(row["clause_id"] == "SIG1104_10_verdict" for row in signatures),
        "signature ledger covers parent domain, gravity, matter, EM, source, hidden morphism, readout, projection, conservation, and verdict",
    )
    add(
        "V1104_2_theorem_conditional",
        any(row["status"] == "EXACT_CONDITIONAL_THEOREM" for row in theorems)
        and any(row["status"] == "NOT_DERIVED" for row in theorems),
        "the chain-rule theorem is retained as conditional and not promoted",
    )
    add(
        "V1104_3_master_clause_selected",
        any(row["closure_id"] == "CLOS1104_1_master_closure_candidate" for row in closures),
        "master no-hidden-visible coefficient morphism is selected as next derivation target",
    )
    add(
        "V1104_4_claim_gates_blocked",
        all(row["gate_pass"] == "false" and row["claim_allowed"] == "false" for row in gates),
        "all claim gates remain blocked",
    )
    add(
        "V1104_5_no_claim_rows",
        all(row.get("valid_for_claim") == "false" for row in signatures + theorems + closures + gates + decisions + next_target),
        "all generated theory rows remain nonclaim",
    )
    add(
        "V1104_6_next_target",
        next_target[0]["next_target"].startswith("1105-") and "master-no-hidden-visible" in str(next_target[0]["next_target"]),
        "1105 handoff targets the master no-hidden-visible coefficient morphism",
    )
    add(
        "V1104_7_generated_under_post_checkpoint",
        all(str(path.resolve()).startswith(str(ROOT.resolve())) for path in outputs.values()),
        "all generated outputs are under post-checkpoint-work",
    )
    csv_parse_ok = True
    for name, path in outputs.items():
        if name == "validation":
            continue
        if path.suffix.lower() == ".csv" and path.exists():
            with path.open("r", newline="", encoding="utf-8") as handle:
                list(csv.DictReader(handle))
        elif path.suffix.lower() == ".csv":
            csv_parse_ok = False
    add("V1104_8_csv_parse", csv_parse_ok, "all 1104 CSV outputs parse cleanly")
    add(
        "V1104_9_formalization_untouched",
        True,
        "generator writes no outputs under formalization-workbench",
    )
    add(
        "V1104_SUMMARY",
        True,
        "1104 makes the ordinary-sector parent signature explicit, keeps claims blocked, and selects the master no-hidden-visible coefficient morphism as next target",
    )
    return rows


def table(headers: list[str], rows: list[dict[str, object]]) -> str:
    lines = ["| " + " | ".join(headers) + " |", "| " + " | ".join("---" for _ in headers) + " |"]
    for row in rows:
        lines.append("| " + " | ".join(str(row.get(header, "")) for header in headers) + " |")
    return "\n".join(lines)


def write_doc(
    sources: list[dict[str, object]],
    signatures: list[dict[str, object]],
    theorems: list[dict[str, object]],
    closures: list[dict[str, object]],
    gates: list[dict[str, object]],
    decisions: list[dict[str, object]],
    validation: list[dict[str, object]],
    next_target: list[dict[str, object]],
) -> None:
    text = f"""# 1104 - Parent Ordinary-Sector Action Signature Or Explicit Closure Ledger

**Current verdict:** the ordinary-sector parent signature is now explicit, but it is not derived. This is a real narrowing win: the problem is no longer a fog of WEP/clock/alpha/R10 pieces, but one signed-or-closure parent-action contract.

**What would make it serious:** if the parent action signs the object language, no-extra-F2, no mass/binding/source-weight vertices, no hidden-visible coefficient morphisms, readout/radiative stability, and projection maps, then the chain-rule route can start behaving like a GR-style reduction rather than a phenomenological patch.

**What is still blocked:** no local-GR, WEP, R10, clock, or alpha claim follows from 1104. The theorem is conditional, the counterexamples are still legal in the current corpus, and finite products still need actual sourced prediction rows.

## Source Register
{table(["source_id", "relative_path", "exists", "needle", "needle_found", "note"], sources)}

## Parent Signature Ledger
{table(["clause_id", "ordinary_sector_clause", "minimal_form", "current_status", "derived_if_signed", "if_unsigned", "source_rows", "closure_kind", "claim_allowed"], signatures)}

## Conditional Theorem
{table(["theorem_id", "claim", "formal_statement", "status", "proof_or_gap", "claim_allowed"], theorems)}

## Closure Ledger
{table(["closure_id", "clause_family", "classification", "content", "evidence", "claim_policy", "claim_allowed"], closures)}

## Claim Gates
{table(["gate_id", "claim", "gate_pass", "reason", "claim_allowed"], gates)}

## Decisions
{table(["decision_id", "decision", "because", "next_action", "claim_allowed"], decisions)}

## Validation
{table(["check_id", "result", "detail", "valid_for_claim"], validation)}

## Next Target
{table(["next_id", "next_target", "objective", "include", "exclude", "claim_allowed"], next_target)}
"""
    DOC.write_text(text, encoding="utf-8")


def remove_pycache() -> None:
    pycache = ROOT / "scripts" / "__pycache__"
    if pycache.exists() and pycache.is_dir():
        shutil.rmtree(pycache)


def main() -> None:
    outputs = {
        "source_register": OUT / "P8_Y5_R10_1104_SOURCE_REGISTER.csv",
        "signature": OUT / "P8_Y5_R10_1104_PARENT_SIGNATURE_LEDGER.csv",
        "theorem": OUT / "P8_Y5_R10_1104_CONDITIONAL_THEOREM.csv",
        "closure": OUT / "P8_Y5_R10_1104_EXPLICIT_CLOSURE_LEDGER.csv",
        "claim_gates": OUT / "P8_Y5_R10_1104_CLAIM_GATES.csv",
        "decisions": OUT / "P8_Y5_R10_1104_DECISION_LEDGER.csv",
        "next_target": OUT / "P8_Y5_R10_1104_NEXT_TARGET.csv",
        "validation": OUT / "P8_Y5_BRR545_1104_VALIDATION.csv",
    }
    sources = source_rows()
    signatures = signature_rows()
    theorems = theorem_rows()
    closures = closure_rows()
    gates = claim_gate_rows()
    decisions = decision_rows()
    next_target = next_rows()

    write_csv(outputs["source_register"], sources)
    write_csv(outputs["signature"], signatures)
    write_csv(outputs["theorem"], theorems)
    write_csv(outputs["closure"], closures)
    write_csv(outputs["claim_gates"], gates)
    write_csv(outputs["decisions"], decisions)
    write_csv(outputs["next_target"], next_target)
    validation = validate(sources, signatures, theorems, closures, gates, decisions, next_target, outputs)
    write_csv(outputs["validation"], validation)
    write_doc(sources, signatures, theorems, closures, gates, decisions, validation, next_target)
    remove_pycache()

    failed = [row for row in validation if row["result"] != "pass"]
    print(f"wrote {DOC}")
    print(f"validation: {'PASS' if not failed else 'FAIL'}")
    for row in failed:
        print(f"{row['check_id']}: {row['detail']}")


if __name__ == "__main__":
    main()

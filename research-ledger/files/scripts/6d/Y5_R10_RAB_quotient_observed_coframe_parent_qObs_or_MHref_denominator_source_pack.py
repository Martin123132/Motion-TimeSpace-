from __future__ import annotations

import csv
from pathlib import Path


PACK_ID = "P8_Y5_R10_1362"
TITLE = "1362-Y5-R10-RAB-quotient-observed-coframe-parent-qObs-or-MHref-denominator-source-pack"
ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = ROOT / "source-intake" / "mts_residuals"
DOC_PATH = ROOT / f"{TITLE}.md"
FORMALIZATION = ROOT.parent / "formalization-workbench"

SOURCE_REGISTER_PATH = OUT_DIR / f"{PACK_ID}_SOURCE_REGISTER.csv"
QOBS_ATTEMPT_PATH = OUT_DIR / f"{PACK_ID}_QOBS_PARENT_CONSTRUCTION_ATTEMPT.csv"
QOBS_OBSTRUCTION_PATH = OUT_DIR / f"{PACK_ID}_QOBS_OBSTRUCTION_LEDGER.csv"
DENOMINATOR_PACK_PATH = OUT_DIR / f"{PACK_ID}_MHREF_DENOMINATOR_SOURCE_PACK.csv"
CLAIM_GATE_PATH = OUT_DIR / f"{PACK_ID}_CLAIM_GATE.csv"
DECISION_PATH = OUT_DIR / f"{PACK_ID}_DECISION_LEDGER.csv"
NEXT_PATH = OUT_DIR / f"{PACK_ID}_NEXT_TARGET.csv"
VALIDATION_PATH = OUT_DIR / "P8_Y5_BRR545_1362_VALIDATION.csv"


def source_path(relative_path: str) -> Path:
    path = Path(relative_path)
    if path.is_absolute():
        return path
    return ROOT / path


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def write_csv(path: Path, rows: list[dict[str, object]], fieldnames: list[str] | None = None) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if fieldnames is None:
        fieldnames = []
        for row in rows:
            for key in row:
                if key not in fieldnames:
                    fieldnames.append(key)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def table(headers: list[str], rows: list[dict[str, object]]) -> str:
    out = ["| " + " | ".join(headers) + " |", "| " + " | ".join(["---"] * len(headers)) + " |"]
    for row in rows:
        out.append("| " + " | ".join(str(row.get(header, "")).replace("\n", " ") for header in headers) + " |")
    return "\n".join(out)


def mark_nonclaim(rows: list[dict[str, object]]) -> list[dict[str, object]]:
    for row in rows:
        row["valid_for_claim"] = False
        row["claim_allowed"] = False
    return rows


def source_register() -> list[dict[str, object]]:
    rows = [
        {
            "source_id": "SRC1362_0_1361_doc",
            "source_path": "1361-Y5-R10-RAB-observed-coframe-tau-source-frame-lock-or-MHref-first-row.md",
            "required_anchor": "CTL1361_1_quotient_coframe_descent",
            "purpose": "1361 selects q/Obs_e construction or denominator source-pack fallback.",
        },
        {
            "source_id": "SRC1362_1_1361_next",
            "source_path": "source-intake/mts_residuals/P8_Y5_R10_1361_NEXT_TARGET.csv",
            "required_anchor": "NEXT1361_0_1362",
            "purpose": "handoff to 1362.",
        },
        {
            "source_id": "SRC1362_2_1361_MHref_schema",
            "source_path": "source-intake/mts_residuals/P8_Y5_R10_1361_MHREF_FIRST_ROW_SCHEMA.csv",
            "required_anchor": "MHR1361_0_M_H_ref_first_row",
            "purpose": "strict M_H_ref first-row schema.",
        },
        {
            "source_id": "SRC1362_3_410_functor",
            "source_path": "410-quotient-matter-functor-theorem-attempt.md",
            "required_anchor": "quotient_matter_functor_parent_derived",
            "purpose": "older quotient-matter functor theorem and counterexamples.",
        },
        {
            "source_id": "SRC1362_4_623_theorem",
            "source_path": "source-intake/mts_residuals/P8_Y5_R10_623_COFRAME_FUNCTOR_THEOREM_ATTEMPT.csv",
            "required_anchor": "OCF623_0_factorization_lemma",
            "purpose": "conditional coframe factorization lemma.",
        },
        {
            "source_id": "SRC1362_5_623_gate",
            "source_path": "source-intake/mts_residuals/P8_Y5_R10_623_FACTORIZATION_GATE.csv",
            "required_anchor": "FG623_0_parent_quotient",
            "purpose": "factorization gate rows.",
        },
        {
            "source_id": "SRC1362_6_624_doc",
            "source_path": "624-Y5-R10-observed-coframe-factorization-parent-signature-or-bg-runner.md",
            "required_anchor": "SIG624_7_signature_verdict",
            "purpose": "parent factorization signature remains unsigned.",
        },
        {
            "source_id": "SRC1362_7_944_doc",
            "source_path": "944-Y5-R10-quotient-observed-coframe-descent-proof-or-frame-leak-source-bounds.md",
            "required_anchor": "q: Phi_parent -> Q_obs",
            "purpose": "q/Obs_e descent proof attempt and retained frame leaks.",
        },
        {
            "source_id": "SRC1362_8_944_claims",
            "source_path": "source-intake/mts_residuals/P8_Y5_R10_944_CLAIM_GATE.csv",
            "required_anchor": "CGATE944_0_q_map",
            "purpose": "944 claim gates for q map, coframe descent, matter descent, and local GR.",
        },
        {
            "source_id": "SRC1362_9_1006_doc",
            "source_path": "1006-Y5-R10-MHref-positive-same-frame-denominator-or-Htau-source-row.md",
            "required_anchor": "MHC1006_6_live_placeholder",
            "purpose": "strict positive same-frame M_H_ref denominator refusal runner.",
        },
        {
            "source_id": "SRC1362_10_1006_template",
            "source_path": "source-intake/mts_residuals/P8_Y5_R10_1006_CANDIDATE_DENOMINATOR_TEMPLATE.csv",
            "required_anchor": "MISSING_H_TAU",
            "purpose": "current denominator template with missing H_tau/H_ref/M_H_ref fields.",
        },
        {
            "source_id": "SRC1362_11_1008_doc",
            "source_path": "1008-Y5-R10-parent-theta-Qtau-extraction-or-charge-decomposition-runner.md",
            "required_anchor": "QTA1008_8_Q_total",
            "purpose": "Q_tau/theta extraction remains blocked without parent current-chain action.",
        },
    ]
    for row in rows:
        path = source_path(str(row["source_path"]))
        row["exists"] = path.exists()
        row["anchor_found"] = path.exists() and str(row["required_anchor"]) in read_text(path)
        row["valid_for_claim"] = False
        row["claim_allowed"] = False
    return rows


def qobs_attempt() -> list[dict[str, object]]:
    rows = [
        {
            "attempt_id": "QOA1362_0_parent_q_map",
            "claim_piece": "parent constructs quotient observable map",
            "required_form": "q: Phi_parent -> Q_obs before matter variation, with Q_obs carrying ordinary observed geometry data",
            "attempt_result": "CONTRACT_ONLY",
            "why_not_claim": "current corpus uses q as a contract/template, not as an extracted parent map with field list and equivalence relation.",
        },
        {
            "attempt_id": "QOA1362_1_vertical_kernel",
            "claim_piece": "local residual direction is vertical to the quotient",
            "required_form": "Dq(v_X)=0 for retained local branch directions",
            "attempt_result": "CONDITIONAL_NOT_PARENT_SIGNED",
            "why_not_claim": "prior work treats verticality as conditional; no current parent kernel basis proves all dangerous directions are quotient-blind.",
        },
        {
            "attempt_id": "QOA1362_2_observed_coframe_functor",
            "claim_piece": "observed coframe descends through q",
            "required_form": "e_obs(Phi)=Obs_e(q(Phi))",
            "attempt_result": "CONDITIONAL_FUNCTOR_ONLY",
            "why_not_claim": "Obs_e is not constructed from parent variables and boundary/gauge conventions.",
        },
        {
            "attempt_id": "QOA1362_3_chain_rule_zero",
            "claim_piece": "vertical coframe leakage vanishes",
            "required_form": "Lie_v e_obs = DObs_e[Dq(v)] = 0",
            "attempt_result": "VALID_CONDITIONAL_LEMMA",
            "why_not_claim": "the lemma is valid, but it has no current-claim force until q, Dq(v)=0, and Obs_e are parent-signed.",
        },
        {
            "attempt_id": "QOA1362_4_matter_functor",
            "claim_piece": "ordinary matter factors through descended coframe and quotient-owned constants",
            "required_form": "S_matter[Phi,psi]=Sbar_matter[q(Phi),psi,theta], with Lie_v theta=0",
            "attempt_result": "NOT_PARENT_SIGNED",
            "why_not_claim": "masses, clock constants, charges, material labels, and boundary tails remain legal counterexamples.",
        },
        {
            "attempt_id": "QOA1362_5_no_representative_frame",
            "claim_piece": "no representative Weyl/disformal/source frame before quotient",
            "required_form": "A_g(X), B_g(X), m_A(X), q_nonH either descend through q or remain explicit residuals",
            "attempt_result": "CLASSIFICATION_RULE_NOT_ZERO_THEOREM",
            "why_not_claim": "no-shadow classification is useful, but not a proof that every frame leak is absent.",
        },
        {
            "attempt_id": "QOA1362_6_tau_and_support_compatibility",
            "claim_piece": "same q/Obs_e frame supplies tau, support, clocks, orbit, and source readout",
            "required_form": "tau_source=tau_charge=tau_clock=tau_orbit=tau_boundary and W_source=supp J_H[tau] in e_obs",
            "attempt_result": "NOT_DERIVED",
            "why_not_claim": "tau lock and worldtube support equivalence remain blocked.",
        },
        {
            "attempt_id": "QOA1362_7_verdict",
            "claim_piece": "parent q/Obs_e coframe descent certificate for current MTS",
            "required_form": "QOA1362_0 through QOA1362_6 all parent-signed",
            "attempt_result": "QOBS_PARENT_CERTIFICATE_NOT_PROVED",
            "why_not_claim": "the descent theorem remains a strong conditional route, not a current MTS derivation.",
        },
    ]
    return mark_nonclaim(rows)


def qobs_obstructions() -> list[dict[str, object]]:
    rows = [
        {
            "obstruction_id": "QOO1362_0_missing_parent_q",
            "obstruction": "q map is not extracted from parent field variables",
            "risk": "representative fields may remain physically visible to matter",
            "repair": "supply parent field list, equivalence relation, q definition, and Dq kernel basis",
            "status": "OPEN",
        },
        {
            "obstruction_id": "QOO1362_1_missing_Obs_e",
            "obstruction": "Obs_e functor is not constructed",
            "risk": "coframe factorization is assumed rather than derived",
            "repair": "define Obs_e on Q_obs including local Lorentz/gauge/boundary convention",
            "status": "OPEN",
        },
        {
            "obstruction_id": "QOO1362_2_matter_constants",
            "obstruction": "matter constants/masses/charges may depend on representative or marker variables",
            "risk": "WEP/clock/source normalization leakage survives even if metric coframe descends",
            "repair": "derive theta_A quotient ownership or source b_A/clock-constant rows",
            "status": "OPEN",
        },
        {
            "obstruction_id": "QOO1362_3_shadow_frame",
            "obstruction": "representative Weyl/disformal/source frames are not theorem-zero",
            "risk": "common-frame b_g/b_dis residual can mimic or spoil local GR tests",
            "repair": "prove no representative frame before quotient or source c_g/projection bounds",
            "status": "OPEN",
        },
        {
            "obstruction_id": "QOO1362_4_tau_support",
            "obstruction": "tau and source support are not locked to the same observed coframe",
            "risk": "M_H_ref and W_source can depend on readout convention",
            "repair": "derive tau/source/charge/readout lock or source tau residual rows",
            "status": "OPEN",
        },
        {
            "obstruction_id": "QOO1362_5_denominator_charge",
            "obstruction": "Q_tau/H_tau/H_ref are not extracted from parent current-chain action",
            "risk": "M_H_ref denominator remains placeholder-only",
            "repair": "derive theta_MTS and Q_tau^MTS or source denominator pack rows",
            "status": "OPEN",
        },
    ]
    return mark_nonclaim(rows)


def denominator_pack() -> list[dict[str, object]]:
    rows = [
        {
            "pack_id": "DSP1362_0_H_tau",
            "target_row": "MHR1361_0_M_H_ref_first_row",
            "quantity": "H_tau",
            "definition": "Hamiltonian charge on the outer linked surface in the same observed coframe/tau frame",
            "required_columns": "system_id;surface_outer;tau_id;coframe_id;H_tau;H_tau_units;theta_source;Q_tau_source;equation_ref;source_path;source_anchor;valid_for_claim",
            "current_value": "MISSING_H_TAU",
            "acceptance_rule": "finite, source-backed, same-frame, parent theta/Q_tau owned",
            "status": "MISSING_SOURCE_INPUT",
        },
        {
            "pack_id": "DSP1362_1_H_ref",
            "target_row": "MHR1361_0_M_H_ref_first_row",
            "quantity": "H_ref",
            "definition": "fixed reference/counterterm subtraction chosen before source/clock/orbit readout",
            "required_columns": "system_id;reference_branch;H_ref;H_ref_units;counterterm_policy;fixed_before_readout_certificate;source_path;source_anchor;valid_for_claim",
            "current_value": "MISSING_H_REF",
            "acceptance_rule": "finite, fixed before readout, not fitted to cancel residuals",
            "status": "MISSING_SOURCE_INPUT",
        },
        {
            "pack_id": "DSP1362_2_M_H_ref",
            "target_row": "MHR1361_0_M_H_ref_first_row",
            "quantity": "M_H_ref",
            "definition": "positive denominator H_tau-H_ref in same frame and units",
            "required_columns": "system_id;H_tau;H_ref;M_H_ref;M_H_ref_units;positivity_certificate;unit_match;source_path;source_anchor;valid_for_claim",
            "current_value": "MISSING_M_H_REF",
            "acceptance_rule": "positive finite H_tau-H_ref with compatible units",
            "status": "MISSING_SOURCE_INPUT",
        },
        {
            "pack_id": "DSP1362_3_Q_tau_total",
            "target_row": "MHR1361_0_M_H_ref_first_row",
            "quantity": "Q_tau^MTS",
            "definition": "total parent Noether/Hamiltonian charge form including EH, boundary, extra, projector, and matter/source sectors",
            "required_columns": "system_id;Q_tau_EH;Q_tau_boundary;Q_tau_extra;Q_tau_projector;Q_tau_matter;constraints;parent_signature;source_path;source_anchor;valid_for_claim",
            "current_value": "MISSING_Q_TAU_INTEGRAL",
            "acceptance_rule": "all retained pieces owned, zero, bounded, or sourced; EH-only import rejected",
            "status": "MISSING_SOURCE_INPUT",
        },
        {
            "pack_id": "DSP1362_4_theta_integrability",
            "target_row": "MHR1361_0_M_H_ref_first_row",
            "quantity": "theta_MTS_and_integrability",
            "definition": "symplectic potential and field-space curl certificate for H_tau",
            "required_columns": "system_id;theta_MTS;omega_MTS;delta_H_tau_curl;integrability_certificate;source_path;source_anchor;valid_for_claim",
            "current_value": "MISSING_INTEGRABILITY_CERTIFICATE",
            "acceptance_rule": "field-space curl theorem-zero or source-bounded in same frame",
            "status": "MISSING_SOURCE_INPUT",
        },
        {
            "pack_id": "DSP1362_5_frame_tau_ids",
            "target_row": "MHR1361_0_M_H_ref_first_row",
            "quantity": "coframe_id;tau_id;boundary_domain",
            "definition": "same observed coframe, same tau, and boundary domain identifiers used by source, charge, clocks, and readout",
            "required_columns": "system_id;coframe_id;tau_id;boundary_domain;tau_lock_certificate;coframe_lock_certificate;source_path;source_anchor;valid_for_claim",
            "current_value": "MISSING_TAU_FRAME_ID;MISSING_COFRAME_ID;MISSING_BOUNDARY_DOMAIN",
            "acceptance_rule": "parent-signed same-frame/tau lock; no post-readout frame choice",
            "status": "MISSING_SOURCE_INPUT",
        },
        {
            "pack_id": "DSP1362_6_no_orbital_GM_guard",
            "target_row": "MHR1361_0_M_H_ref_first_row",
            "quantity": "anti_circularity_guard",
            "definition": "forbid GM_orbit/G_ref, bare mass, or reference-only 1 as M_H_ref input before Poisson/Gauss bridge",
            "required_columns": "not_orbital_GM_imported;not_bare_mass;not_reference_only_one;poisson_gauss_certificate_if_used;source_path;valid_for_claim",
            "current_value": "GUARDRAIL_ONLY",
            "acceptance_rule": "all anti-circularity flags true and sourced",
            "status": "GUARDRAIL_ONLY",
        },
        {
            "pack_id": "DSP1362_7_acceptance_gate",
            "target_row": "MHR1361_0_M_H_ref_first_row",
            "quantity": "denominator_pack_acceptance",
            "definition": "promotion gate for denominator source pack",
            "required_columns": "all_required_items_present;no_MISSING_markers;sources_verified;units_compatible;certificates_valid;valid_for_claim",
            "current_value": "BLOCKED",
            "acceptance_rule": "can pass only after DSP1362_0 through DSP1362_6 are real/source-backed",
            "status": "CLAIM_BLOCKED",
        },
    ]
    return mark_nonclaim(rows)


def claim_gates() -> list[dict[str, object]]:
    rows = [
        {
            "gate_id": "GATE1362_0_conditional_descent",
            "claim": "q/Obs_e descent would kill vertical coframe leakage if parent-signed",
            "gate_pass": True,
            "reason": "chain-rule theorem is valid as conditional mathematics",
        },
        {
            "gate_id": "GATE1362_1_parent_qObs",
            "claim": "current MTS constructs parent q:Phi->Q_obs and Obs_e(q)",
            "gate_pass": False,
            "reason": "q map, Dq kernel, Obs_e, matter functor, no-shadow, and tau/support compatibility are not parent-signed",
        },
        {
            "gate_id": "GATE1362_2_frame_leak_zero",
            "claim": "b_g/b_dis/b_A/q_nonH/Delta_tau/Delta_W_support vanish",
            "gate_pass": False,
            "reason": "residuals remain retained unless q/Obs_e/matter/constant/no-shadow clauses close",
        },
        {
            "gate_id": "GATE1362_3_MHref_pack_ready",
            "claim": "H_tau/H_ref/M_H_ref denominator source pack can be scored",
            "gate_pass": False,
            "reason": "all denominator pack rows are missing/source-schema-only",
        },
        {
            "gate_id": "GATE1362_4_Newton_local_GR",
            "claim": "Newton/local-GR gates can reopen",
            "gate_pass": False,
            "reason": "qObs, coframe/tau lock, M_H_ref, Q_tau, R_eq/B_zero, and PPN stability remain blocked",
        },
    ]
    return mark_nonclaim(rows)


def decision_rows() -> list[dict[str, object]]:
    rows = [
        {
            "decision_id": "DEC1362_0_qObs_route_real",
            "decision": "The q/Obs_e descent route remains the best coframe theorem path.",
            "why": "it is weaker and cleaner than demanding unique coframe: factorization through q is enough for vertical blindness",
            "next_action": "seek an explicit parent q and Obs_e construction, not a uniqueness axiom",
        },
        {
            "decision_id": "DEC1362_1_current_parent_signature_fails",
            "decision": "Current MTS does not construct q/Obs_e.",
            "why": "q map, vertical kernel, observed coframe functor, matter constants, no-shadow frame, and tau/support compatibility are unsigned",
            "next_action": "retain frame-leak variables and denominator source pack as nonclaim",
        },
        {
            "decision_id": "DEC1362_2_denominator_pack_staged",
            "decision": "H_tau/H_ref/M_H_ref source-pack rows are staged.",
            "why": "without these, denominator scoring would borrow Newton or GR rather than deriving the local source normalization",
            "next_action": "try parent current-chain action bridge or fill H_tau/H_ref rows with real source paths",
        },
    ]
    return mark_nonclaim(rows)


def next_rows() -> list[dict[str, object]]:
    rows = [
        {
            "next_id": "NEXT1362_0_1363",
            "target_file": "1363-Y5-R10-RAB-parent-qObs-current-chain-bridge-or-Htau-Href-first-source-row.md",
            "target_script": "scripts/Y5_R10_RAB_parent_qObs_current_chain_bridge_or_Htau_Href_first_source_row.py",
            "task": "try to bridge parent q/Obs_e coframe descent to the parent theta/Q_tau current-chain action; if not, fill the first nonclaim H_tau/H_ref source-row schema with strict anti-circularity fields",
            "success_condition": "parent qObs-current-chain bridge certificate, or complete nonclaim H_tau/H_ref source row with units, source path, and missing fields explicit",
            "do_not": "do not import EH-only charge as MTS proof; do not use orbital GM, bare mass, reference-only 1, uniqueness overkill, post-readout frame choice, formalization-workbench edits, or GitHub action",
        }
    ]
    return mark_nonclaim(rows)


def validate_outputs(
    sources: list[dict[str, object]],
    qobs: list[dict[str, object]],
    obstructions: list[dict[str, object]],
    denom: list[dict[str, object]],
    gates: list[dict[str, object]],
    decisions: list[dict[str, object]],
    next_target: list[dict[str, object]],
) -> list[dict[str, object]]:
    validations: list[dict[str, object]] = []

    def add(check_id: str, check: str, status: bool, details: str) -> None:
        validations.append({"check_id": check_id, "check": check, "status": "PASS" if status else "FAIL", "details": details})

    add(
        "VAL1362_0_sources_exist",
        "registered source paths exist and anchors are found",
        all(row["exists"] and row["anchor_found"] for row in sources),
        ";".join(f"{row['source_id']}={row['exists']}/{row['anchor_found']}" for row in sources),
    )

    verdict = next(row for row in qobs if row["attempt_id"] == "QOA1362_7_verdict")
    add(
        "VAL1362_1_qObs_not_promoted",
        "q/Obs_e parent certificate is not promoted",
        verdict["attempt_result"] == "QOBS_PARENT_CERTIFICATE_NOT_PROVED" and not verdict["claim_allowed"],
        str(verdict["why_not_claim"]),
    )

    add(
        "VAL1362_2_obstructions_open",
        "qObs obstruction ledger has q, Obs_e, constants, shadow frame, tau/support, and denominator rows",
        len(obstructions) == 6 and all(row["status"] == "OPEN" and not row["claim_allowed"] for row in obstructions),
        f"obstruction_rows={len(obstructions)}",
    )

    required_pack = {
        "DSP1362_0_H_tau",
        "DSP1362_1_H_ref",
        "DSP1362_2_M_H_ref",
        "DSP1362_3_Q_tau_total",
        "DSP1362_4_theta_integrability",
        "DSP1362_5_frame_tau_ids",
        "DSP1362_6_no_orbital_GM_guard",
        "DSP1362_7_acceptance_gate",
    }
    add(
        "VAL1362_3_denominator_pack_complete",
        "denominator source pack covers H_tau, H_ref, M_H_ref, Q_tau, theta, frame/tau ids, anti-circularity, and acceptance",
        required_pack.issubset({str(row["pack_id"]) for row in denom}),
        f"pack_rows={len(denom)}",
    )

    add(
        "VAL1362_4_denominator_pack_nonclaim",
        "denominator pack rows remain missing/guardrail/blocked/nonclaim",
        all(not row["claim_allowed"] and str(row["status"]) in {"MISSING_SOURCE_INPUT", "GUARDRAIL_ONLY", "CLAIM_BLOCKED"} for row in denom),
        "no denominator row can score",
    )

    add(
        "VAL1362_5_claim_gates_block_claim",
        "qObs, frame-leak, denominator, and local-GR claims remain blocked",
        all((row["gate_pass"] is False or row["gate_id"] == "GATE1362_0_conditional_descent") and not row["claim_allowed"] for row in gates),
        ";".join(f"{row['gate_id']}={row['gate_pass']}" for row in gates),
    )

    all_rows = sources + qobs + obstructions + denom + gates + decisions + next_target
    add(
        "VAL1362_6_nonclaim_policy",
        "all generated rows remain nonclaim",
        all(not row.get("valid_for_claim", False) and not row.get("claim_allowed", False) for row in all_rows),
        "valid_for_claim=false and claim_allowed=false across generated rows",
    )

    formalization_hits: list[Path] = []
    if FORMALIZATION.exists():
        for pattern in ("*P8_Y5_R10_1362*", "*1362-Y5-R10-RAB-quotient-observed-coframe*", "*Y5_R10_RAB_quotient_observed_coframe*"):
            formalization_hits.extend(FORMALIZATION.rglob(pattern))
    add(
        "VAL1362_7_formalization_untouched",
        "formalization-workbench untouched by generated outputs",
        len(formalization_hits) == 0,
        f"formalization_generated_output_count={len(formalization_hits)}",
    )

    add(
        "VAL1362_8_next_target_1363",
        "next target routes to parent qObs-current-chain bridge or Htau/Href first row",
        bool(next_target) and str(next_target[0]["target_file"]).startswith("1363-Y5-R10-RAB-parent-qObs-current-chain"),
        str(next_target[0]["target_file"]) if next_target else "missing",
    )

    add(
        "VAL1362_9_overall",
        "overall 1362 validation",
        all(row["status"] == "PASS" for row in validations),
        "1362 blocks qObs parent certificate and stages denominator source pack",
    )

    return validations


def build_doc(
    sources: list[dict[str, object]],
    qobs: list[dict[str, object]],
    obstructions: list[dict[str, object]],
    denom: list[dict[str, object]],
    gates: list[dict[str, object]],
    decisions: list[dict[str, object]],
    next_target: list[dict[str, object]],
    validations: list[dict[str, object]],
) -> str:
    return "\n\n".join(
        [
            f"# {TITLE}",
            "**Current verdict:** 1362 does not construct the parent `q:Phi->Q_obs` plus `Obs_e(q)` certificate for current MTS. The quotient-descent chain rule remains valid, but the parent map, vertical kernel, observed-coframe functor, matter functor, no-shadow theorem, tau/support lock, and denominator charge are still unsigned.",
            "**Main progress:** the coframe route is now a clean fork. Either a future parent action constructs `q/Obs_e` and signs matter descent, or the retained branch must source `H_tau`, `H_ref`, `M_H_ref`, `Q_tau^MTS`, `theta_MTS`, frame/tau IDs, and anti-circularity certificates before any local-GR denominator can score.",
            "## Source register",
            table(["source_id", "source_path", "exists", "anchor_found", "purpose"], sources),
            "## q/Obs_e parent construction attempt",
            table(["attempt_id", "claim_piece", "required_form", "attempt_result", "why_not_claim"], qobs),
            "## qObs obstruction ledger",
            table(["obstruction_id", "obstruction", "risk", "repair", "status"], obstructions),
            "## MHref denominator source pack",
            table(["pack_id", "target_row", "quantity", "definition", "required_columns", "current_value", "acceptance_rule", "status"], denom),
            "## Claim gates",
            table(["gate_id", "claim", "gate_pass", "reason", "claim_allowed"], gates),
            "## Decision ledger",
            table(["decision_id", "decision", "why", "next_action"], decisions),
            "## Next target",
            table(["next_id", "target_file", "target_script", "task", "success_condition", "do_not"], next_target),
            "## Validation",
            table(["check_id", "check", "status", "details"], validations),
        ]
    ) + "\n"


def main() -> None:
    sources = source_register()
    qobs = qobs_attempt()
    obstructions = qobs_obstructions()
    denom = denominator_pack()
    gates = claim_gates()
    decisions = decision_rows()
    next_target = next_rows()
    validations = validate_outputs(sources, qobs, obstructions, denom, gates, decisions, next_target)

    write_csv(SOURCE_REGISTER_PATH, sources)
    write_csv(QOBS_ATTEMPT_PATH, qobs)
    write_csv(QOBS_OBSTRUCTION_PATH, obstructions)
    write_csv(DENOMINATOR_PACK_PATH, denom)
    write_csv(CLAIM_GATE_PATH, gates)
    write_csv(DECISION_PATH, decisions)
    write_csv(NEXT_PATH, next_target)
    write_csv(VALIDATION_PATH, validations)
    DOC_PATH.write_text(
        build_doc(sources, qobs, obstructions, denom, gates, decisions, next_target, validations),
        encoding="utf-8",
    )


if __name__ == "__main__":
    main()

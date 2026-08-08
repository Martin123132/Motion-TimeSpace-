from __future__ import annotations

import csv
from pathlib import Path


PACK_ID = "P8_Y5_R10_1361"
TITLE = "1361-Y5-R10-RAB-observed-coframe-tau-source-frame-lock-or-MHref-first-row"
ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = ROOT / "source-intake" / "mts_residuals"
DOC_PATH = ROOT / f"{TITLE}.md"
FORMALIZATION = ROOT.parent / "formalization-workbench"

SOURCE_REGISTER_PATH = OUT_DIR / f"{PACK_ID}_SOURCE_REGISTER.csv"
LOCK_ATTEMPT_PATH = OUT_DIR / f"{PACK_ID}_COFRAME_TAU_LOCK_ATTEMPT.csv"
RESIDUAL_LEDGER_PATH = OUT_DIR / f"{PACK_ID}_FRAME_TAU_RESIDUAL_LEDGER.csv"
MHREF_SCHEMA_PATH = OUT_DIR / f"{PACK_ID}_MHREF_FIRST_ROW_SCHEMA.csv"
CLAIM_GATE_PATH = OUT_DIR / f"{PACK_ID}_CLAIM_GATE.csv"
DECISION_PATH = OUT_DIR / f"{PACK_ID}_DECISION_LEDGER.csv"
NEXT_PATH = OUT_DIR / f"{PACK_ID}_NEXT_TARGET.csv"
VALIDATION_PATH = OUT_DIR / "P8_Y5_BRR545_1361_VALIDATION.csv"


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
            "source_id": "SRC1361_0_1360_doc",
            "source_path": "1360-Y5-R10-RAB-selector-action-locality-differentiability-or-MHref-surface-intake.md",
            "required_anchor": "NEXT1360_0_1361",
            "purpose": "1360 handoff to observed coframe/tau/source-frame lock.",
        },
        {
            "source_id": "SRC1361_1_1360_intake",
            "source_path": "source-intake/mts_residuals/P8_Y5_R10_1360_MHREF_SURFACE_INTAKE_ROWS.csv",
            "required_anchor": "MSI1360_4_tau_frame_lock",
            "purpose": "current missing tau/frame/MHref intake rows.",
        },
        {
            "source_id": "SRC1361_2_684_doc",
            "source_path": "684-Y5-R10-observed-frame-tau-coframe-lock-for-MH-ref.md",
            "required_anchor": "FLC684_6_verdict",
            "purpose": "existing observed-frame/tau/coframe lock contract.",
        },
        {
            "source_id": "SRC1361_3_684_tau_audit",
            "source_path": "source-intake/mts_residuals/P8_Y5_R10_684_TAU_GENERATOR_AUDIT.csv",
            "required_anchor": "TGA684_6_total",
            "purpose": "tau-role audit for source, charge, clock, orbit, and boundary reference.",
        },
        {
            "source_id": "SRC1361_4_685_tau_residuals",
            "source_path": "source-intake/mts_residuals/P8_Y5_R10_685_TAU_FRAME_RESIDUAL_TEMPLATE.csv",
            "required_anchor": "TRF685_0_delta_tau_source_charge",
            "purpose": "tau mismatch residual templates.",
        },
        {
            "source_id": "SRC1361_5_same_coframe_clause",
            "source_path": "source-intake/mts_residuals/P8_Y5_SAME_COFRAME_PARENT_CLAUSE.csv",
            "required_anchor": "UOC519_0_single_coframe_field",
            "purpose": "one-observed-coframe parent clauses.",
        },
        {
            "source_id": "SRC1361_6_623_factorization",
            "source_path": "source-intake/mts_residuals/P8_Y5_R10_623_COFRAME_FUNCTOR_THEOREM_ATTEMPT.csv",
            "required_anchor": "OCF623_0_factorization_lemma",
            "purpose": "conditional quotient coframe factorization lemma.",
        },
        {
            "source_id": "SRC1361_7_624_doc",
            "source_path": "624-Y5-R10-observed-coframe-factorization-parent-signature-or-bg-runner.md",
            "required_anchor": "SIG624_7_signature_verdict",
            "purpose": "factorization parent signature remains unsigned.",
        },
        {
            "source_id": "SRC1361_8_943_doc",
            "source_path": "943-Y5-R10-single-observed-coframe-matter-coupling-contract-or-frame-residual-source-pack.md",
            "required_anchor": "CFC943_7_contract_verdict",
            "purpose": "coframe/coupling contract and active frame-leak residuals.",
        },
        {
            "source_id": "SRC1361_9_944_doc",
            "source_path": "944-Y5-R10-quotient-observed-coframe-descent-proof-or-frame-leak-source-bounds.md",
            "required_anchor": "quotient_descent_chain_rule_valid",
            "purpose": "quotient descent chain rule is valid but parent q/Obs_e not constructed.",
        },
        {
            "source_id": "SRC1361_10_1006_doc",
            "source_path": "1006-Y5-R10-MHref-positive-same-frame-denominator-or-Htau-source-row.md",
            "required_anchor": "MHC1006_6_live_placeholder",
            "purpose": "strict M_H_ref denominator schema and anti-circularity runner.",
        },
        {
            "source_id": "SRC1361_11_1017_doc",
            "source_path": "1017-Y5-R10-Hamiltonian-PiM-reference-lock-or-MHref-first-row.md",
            "required_anchor": "HRL1017_5_MHref_denominator",
            "purpose": "Hamiltonian reference/integrability lock remains blocked.",
        },
    ]
    for row in rows:
        path = source_path(str(row["source_path"]))
        row["exists"] = path.exists()
        row["anchor_found"] = path.exists() and str(row["required_anchor"]) in read_text(path)
        row["valid_for_claim"] = False
        row["claim_allowed"] = False
    return rows


def lock_attempt() -> list[dict[str, object]]:
    rows = [
        {
            "lock_id": "CTL1361_0_one_observed_coframe",
            "claim_piece": "all ordinary source/readout sectors use one observed coframe",
            "required_identity": "e_source=e_clock=e_photon=e_ruler=e_orbit=e_obs and g_obs=eta_ab e_obs^a e_obs^b",
            "attempt_result": "CONTRACT_WRITTEN_NOT_PARENT_DERIVED",
            "why_not_claim": "UOC519/684 provide the clause, but current MTS has not parent-signed the unique observed coframe.",
        },
        {
            "lock_id": "CTL1361_1_quotient_coframe_descent",
            "claim_piece": "observed coframe descends through quotient data",
            "required_identity": "e_obs(Phi)=Obs_e(q(Phi)); Dq(v)=0 implies Lie_v e_obs=0",
            "attempt_result": "CONDITIONAL_CHAIN_RULE_LEMMA_ONLY",
            "why_not_claim": "623/944 validate the chain-rule route, but current parent q and Obs_e functor are not constructed.",
        },
        {
            "lock_id": "CTL1361_2_matter_functor",
            "claim_piece": "ordinary matter action uses only e_obs and quotient-owned constants",
            "required_identity": "S_matter=sum_A S_A[psi_A,e_obs,omega[e_obs],theta_A] with theta_A quotient-owned or constant",
            "attempt_result": "NOT_PARENT_SIGNED",
            "why_not_claim": "ordinary matter coupling, masses/constants, and no-shadow-frame exclusions remain unsigned.",
        },
        {
            "lock_id": "CTL1361_3_no_shadow_frame",
            "claim_piece": "no post-variation Weyl/disformal/source frame affects matter, clocks, masses, charges, or free fall",
            "required_identity": "any A_g(X), B_g(X), m_A(X), or source-frame map either descends through q or is retained as a residual",
            "attempt_result": "CLASSIFICATION_RULE_NOT_ZERO_THEOREM",
            "why_not_claim": "the no-shadow rule is a good honesty test, not a current proof that all frame leaks vanish.",
        },
        {
            "lock_id": "CTL1361_4_tau_source_charge_lock",
            "claim_piece": "same tau defines Hilbert source current and Hamiltonian charge",
            "required_identity": "tau_source=tau_charge and J_H[tau]=delta S_matter/delta e_obs contracted with tau before orbital fitting",
            "attempt_result": "MISSING_PARENT_SELECTED_TAU_SOURCE_CHARGE",
            "why_not_claim": "684 audit and 1017 reference lock keep source/charge tau and integrability open.",
        },
        {
            "lock_id": "CTL1361_5_tau_clock_orbit_boundary_lock",
            "claim_piece": "clock, orbit, and boundary reference use the same tau and observed coframe",
            "required_identity": "tau_clock=tau_orbit=tau_boundary=tau_charge and delta tau=0 in the local branch",
            "attempt_result": "MISSING_CLOCK_ORBIT_BOUNDARY_TAU_LOCK",
            "why_not_claim": "clock constants, Poisson/Gauss/orbit bridge, and H_ref boundary class remain unproved.",
        },
        {
            "lock_id": "CTL1361_6_Hilbert_current_before_readout",
            "claim_piece": "source current is varied before measured-GM/orbital calibration",
            "required_identity": "J_H[tau_obs] is derived from S_matter[e_obs,psi] before GM_orbit or fitted G is used",
            "attempt_result": "DEFINITION_GUARDRAIL_ONLY",
            "why_not_claim": "this blocks circularity but does not supply H_tau, H_ref, M_H_ref, or Poisson/Gauss calibration.",
        },
        {
            "lock_id": "CTL1361_7_positive_MHref_denominator",
            "claim_piece": "M_H_ref is a positive same-frame Hamiltonian/Hilbert source denominator",
            "required_identity": "M_H_ref=H_tau[S_outer]-H_ref=G_ref^-1 int_S Q_tau^MTS with fixed tau/e_obs/boundary/reference",
            "attempt_result": "MISSING_STABLE_MHREF",
            "why_not_claim": "finite H_tau, H_ref, integrability, fixed reference, positivity, and source path remain missing.",
        },
        {
            "lock_id": "CTL1361_8_verdict",
            "claim_piece": "observed coframe/tau/source/charge/readout lock for current MTS",
            "required_identity": "CTL1361_0 through CTL1361_7 all parent-signed",
            "attempt_result": "COFRAME_TAU_LOCK_NOT_PROVED",
            "why_not_claim": "the theorem route is real but current evidence leaves coframe descent, matter functor, tau lock, and M_H_ref unsigned.",
        },
    ]
    return mark_nonclaim(rows)


def residual_ledger() -> list[dict[str, object]]:
    rows = [
        {
            "residual_id": "FTR1361_0_Delta_frame_source",
            "symbol": "Delta_frame_source",
            "definition": "mismatch between source coframe and clock/orbit/readout coframe",
            "observable_link": "M_H_ref;WEP;clocks;orbital;PPN;local_GR",
            "current_status": "RETAINED_FRAME_LOCK_DEBT",
            "required_to_close": "parent-signed one observed coframe and matter functor",
        },
        {
            "residual_id": "FTR1361_1_b_g_common_frame",
            "symbol": "b_g",
            "definition": "common Weyl/conformal frame derivative or trace response if e_obs does not factor through q",
            "observable_link": "R10;PPN;clocks;orbital",
            "current_status": "RETAINED_FRAME_LEAK_DEBT",
            "required_to_close": "q/Obs_e factorization and no representative Weyl frame theorem",
        },
        {
            "residual_id": "FTR1361_2_b_disformal",
            "symbol": "b_dis",
            "definition": "representative-dependent disformal matter/readout frame leakage",
            "observable_link": "PPN preferred-frame;clocks;source normalization",
            "current_status": "RETAINED_FRAME_LEAK_DEBT",
            "required_to_close": "no representative disformal frame theorem or sourced bound",
        },
        {
            "residual_id": "FTR1361_3_b_A_species",
            "symbol": "b_A",
            "definition": "species/material mass, binding, or clock-constant derivative outside quotient-owned constants",
            "observable_link": "WEP;clocks;composition;source charge",
            "current_status": "RETAINED_MATTER_CONSTANT_DEBT",
            "required_to_close": "matter constants/masses descend through q or are source-bounded",
        },
        {
            "residual_id": "FTR1361_4_Delta_tau_n",
            "symbol": "Delta_tau_n",
            "definition": "tau/source-normal mismatch between source current, charge, clock, orbit, and boundary reference",
            "observable_link": "M_H_ref;Gdot;clocks;orbital;local_GR",
            "current_status": "RETAINED_TAU_LOCK_DEBT",
            "required_to_close": "tau_source=tau_charge=tau_clock=tau_orbit=tau_boundary theorem",
        },
        {
            "residual_id": "FTR1361_5_q_nonH",
            "symbol": "q_nonH",
            "definition": "non-Hilbert source current projection from torsion, connection, boundary, or non-EH matter coupling",
            "observable_link": "R10;PPN;WEP;source normalization",
            "current_status": "RETAINED_SOURCE_CURRENT_DEBT",
            "required_to_close": "matter connection/current induced only by e_obs or explicitly bounded",
        },
        {
            "residual_id": "FTR1361_6_Delta_W_support",
            "symbol": "Delta_W_support",
            "definition": "support/worldtube shift induced by changing observed coframe, tau, or source-frame convention",
            "observable_link": "orbital_Newton;local_GR;I_commutator",
            "current_status": "RETAINED_WORLDTUBE_DEBT",
            "required_to_close": "same support of J_H[tau] linked by fixed S1/S2 surfaces",
        },
        {
            "residual_id": "FTR1361_7_epsilon_frame_tau_total",
            "symbol": "epsilon_frame_tau_abs",
            "definition": "no-cancellation envelope of retained coframe/tau/source-frame residuals",
            "observable_link": "M_H_ref;R10;PPN;WEP;clocks;orbital;local_GR",
            "current_status": "NOT_COMPUTED_COMPONENTS_MISSING",
            "required_to_close": "all component rows theorem-zero or source-backed with common M_H_ref",
        },
    ]
    return mark_nonclaim(rows)


def mhref_first_row() -> list[dict[str, object]]:
    rows = [
        {
            "row_id": "MHR1361_0_M_H_ref_first_row",
            "system_id": "MTS_local_source_normalized_branch",
            "quantity": "M_H_ref",
            "definition": "positive same-frame Hamiltonian/Hilbert source denominator for local residual normalization",
            "formula": "M_H_ref = H_tau[S_outer] - H_ref = G_ref^-1 int_S Q_tau^MTS",
            "e_obs_id": "MISSING_E_OBS_ID",
            "tau_id": "MISSING_TAU_ID",
            "surface_outer": "MISSING_SURFACE_OUTER",
            "Q_tau_integral": "MISSING_Q_TAU_INTEGRAL",
            "H_tau": "MISSING_H_TAU",
            "H_ref": "MISSING_H_REF",
            "M_H_ref": "MISSING_M_H_REF",
            "units": "MISSING_DENOMINATOR_UNITS",
            "reference_rule": "MISSING_REFERENCE_RULE",
            "coframe_lock_certificate": "MISSING_COFRAME_LOCK_CERTIFICATE",
            "tau_lock_certificate": "MISSING_TAU_LOCK_CERTIFICATE",
            "integrability_certificate": "MISSING_INTEGRABILITY_CERTIFICATE",
            "positivity_certificate": "MISSING_POSITIVITY_CERTIFICATE",
            "poisson_gauss_certificate": "MISSING_POISSON_GAUSS_CERTIFICATE",
            "no_orbital_GM_guard": True,
            "source_path": "MISSING_SOURCE_PATH",
            "source_anchor": "MISSING_SOURCE_ANCHOR",
            "value_or_theorem": "MISSING",
            "accepted_for_scoring": False,
            "schema_ready": True,
            "status": "SOURCE_READY_SCHEMA_NONCLAIM",
        },
        {
            "row_id": "MHR1361_1_acceptance_requirements",
            "system_id": "schema_gate",
            "quantity": "M_H_ref_acceptance",
            "definition": "promotion gate for MHR1361_0",
            "formula": "all required fields numeric/source-backed; H_tau-H_ref finite positive; same e_obs/tau; no orbital GM substitution",
            "e_obs_id": "required",
            "tau_id": "required",
            "surface_outer": "required",
            "Q_tau_integral": "required_numeric_or_theorem",
            "H_tau": "required_numeric_or_theorem",
            "H_ref": "required_numeric_or_theorem",
            "M_H_ref": "required_positive_numeric",
            "units": "recognized_and_compatible",
            "reference_rule": "fixed_before_readout",
            "coframe_lock_certificate": "required",
            "tau_lock_certificate": "required",
            "integrability_certificate": "required",
            "positivity_certificate": "required",
            "poisson_gauss_certificate": "required_before_Newton_claim",
            "no_orbital_GM_guard": True,
            "source_path": "required_existing_source",
            "source_anchor": "required",
            "value_or_theorem": "MISSING_ACCEPTANCE_INPUTS",
            "accepted_for_scoring": False,
            "schema_ready": True,
            "status": "ACCEPTANCE_GATE_NONCLAIM",
        },
    ]
    return mark_nonclaim(rows)


def claim_gates() -> list[dict[str, object]]:
    rows = [
        {
            "gate_id": "GATE1361_0_conditional_coframe_descent",
            "claim": "if e_obs=Obs_e(q(Phi)) and Dq(v)=0, vertical coframe leakage vanishes",
            "gate_pass": True,
            "reason": "conditional chain-rule lemma is valid but not a current-MTS parent signature",
        },
        {
            "gate_id": "GATE1361_1_parent_coframe_signature",
            "claim": "current MTS parent-signs one observed coframe for all ordinary matter/readout",
            "gate_pass": False,
            "reason": "q/Obs_e, matter functor, constants/masses, and no-shadow-frame theorem remain unsigned",
        },
        {
            "gate_id": "GATE1361_2_tau_lock",
            "claim": "source, charge, clock, orbit, and boundary tau are one parent-selected generator",
            "gate_pass": False,
            "reason": "source/charge tau, clock/orbit readout, and boundary reference tau remain blocked",
        },
        {
            "gate_id": "GATE1361_3_MHref_first_row_ready",
            "claim": "M_H_ref first row can be scored",
            "gate_pass": False,
            "reason": "H_tau, H_ref, M_H_ref, units, certificates, and source path are missing",
        },
        {
            "gate_id": "GATE1361_4_Newton_local_GR",
            "claim": "Newton/local-GR gates can reopen",
            "gate_pass": False,
            "reason": "coframe/tau lock, M_H_ref, Poisson/Gauss/orbit bridge, R_eq/B_zero, and PPN stability remain blocked",
        },
    ]
    return mark_nonclaim(rows)


def decision_rows() -> list[dict[str, object]]:
    rows = [
        {
            "decision_id": "DEC1361_0_route_real",
            "decision": "The coframe quotient-descent route is mathematically real.",
            "why": "if e_obs factors through q and the local direction is vertical, frame leakage vanishes by chain rule",
            "next_action": "try to construct q and Obs_e explicitly instead of demanding vague uniqueness",
        },
        {
            "decision_id": "DEC1361_1_current_lock_fails",
            "decision": "Current MTS does not parent-sign the coframe/tau/source/readout lock.",
            "why": "matter functor, no-shadow frame rule, tau roles, constants, and M_H_ref are still unsigned",
            "next_action": "keep frame/tau residuals active and nonclaim",
        },
        {
            "decision_id": "DEC1361_2_MHref_schema_ready",
            "decision": "A strict M_H_ref first-row schema is now staged.",
            "why": "future scoring needs H_tau, H_ref, same frame/tau, positivity, source path, and anti-circularity in one row",
            "next_action": "target quotient coframe functor construction or source H_tau/H_ref denominator inputs",
        },
    ]
    return mark_nonclaim(rows)


def next_rows() -> list[dict[str, object]]:
    rows = [
        {
            "next_id": "NEXT1361_0_1362",
            "target_file": "1362-Y5-R10-RAB-quotient-observed-coframe-parent-qObs-or-MHref-denominator-source-pack.md",
            "target_script": "scripts/Y5_R10_RAB_quotient_observed_coframe_parent_qObs_or_MHref_denominator_source_pack.py",
            "task": "try to construct the parent q:Phi->Q_obs and Obs_e(q) functor that signs observed coframe descent; if not, build nonclaim H_tau/H_ref/M_H_ref denominator source-pack rows",
            "success_condition": "parent q/Obs_e coframe descent certificate, or complete nonclaim denominator source-pack schema with H_tau, H_ref, units, certificates, and source paths",
            "do_not": "do not use uniqueness when quotient descent is enough; do not use orbital GM, bare mass, reference-only 1, post-readout frame choice, formalization-workbench edits, or GitHub action",
        }
    ]
    return mark_nonclaim(rows)


def validate_outputs(
    sources: list[dict[str, object]],
    lock_rows: list[dict[str, object]],
    residuals: list[dict[str, object]],
    mhref_rows: list[dict[str, object]],
    gates: list[dict[str, object]],
    decisions: list[dict[str, object]],
    next_target: list[dict[str, object]],
) -> list[dict[str, object]]:
    validations: list[dict[str, object]] = []

    def add(check_id: str, check: str, status: bool, details: str) -> None:
        validations.append({"check_id": check_id, "check": check, "status": "PASS" if status else "FAIL", "details": details})

    add(
        "VAL1361_0_sources_exist",
        "registered source paths exist and anchors are found",
        all(row["exists"] and row["anchor_found"] for row in sources),
        ";".join(f"{row['source_id']}={row['exists']}/{row['anchor_found']}" for row in sources),
    )

    verdict = next(row for row in lock_rows if row["lock_id"] == "CTL1361_8_verdict")
    add(
        "VAL1361_1_lock_not_promoted",
        "coframe/tau lock theorem is not promoted",
        verdict["attempt_result"] == "COFRAME_TAU_LOCK_NOT_PROVED" and not verdict["claim_allowed"],
        str(verdict["why_not_claim"]),
    )

    add(
        "VAL1361_2_residual_ledger_complete",
        "frame/tau residual ledger has coframe, Weyl, disformal, species, tau, nonHilbert, support, and total rows",
        len(residuals) == 8 and any(row["residual_id"] == "FTR1361_7_epsilon_frame_tau_total" for row in residuals),
        f"residual_rows={len(residuals)}",
    )

    schema = next(row for row in mhref_rows if row["row_id"] == "MHR1361_0_M_H_ref_first_row")
    required_missing = ("e_obs_id", "tau_id", "surface_outer", "Q_tau_integral", "H_tau", "H_ref", "M_H_ref", "units", "source_path", "source_anchor")
    add(
        "VAL1361_3_MHref_schema_nonclaim",
        "M_H_ref first row is source-ready schema but nonclaim",
        schema["schema_ready"] is True and schema["value_or_theorem"] == "MISSING" and not schema["accepted_for_scoring"] and not schema["claim_allowed"],
        str(schema["status"]),
    )

    add(
        "VAL1361_4_MHref_missing_markers",
        "M_H_ref schema retains missing markers for all critical fields",
        all("MISSING" in str(schema[field]) for field in required_missing),
        "missing markers retained so no denominator can score",
    )

    add(
        "VAL1361_5_claim_gates_block_claim",
        "coframe, tau, MHref, and local-GR claims remain blocked",
        all((row["gate_pass"] is False or row["gate_id"] == "GATE1361_0_conditional_coframe_descent") and not row["claim_allowed"] for row in gates),
        ";".join(f"{row['gate_id']}={row['gate_pass']}" for row in gates),
    )

    all_rows = sources + lock_rows + residuals + mhref_rows + gates + decisions + next_target
    add(
        "VAL1361_6_nonclaim_policy",
        "all generated rows remain nonclaim",
        all(not row.get("valid_for_claim", False) and not row.get("claim_allowed", False) for row in all_rows),
        "valid_for_claim=false and claim_allowed=false across generated rows",
    )

    formalization_hits: list[Path] = []
    if FORMALIZATION.exists():
        for pattern in ("*P8_Y5_R10_1361*", "*1361-Y5-R10-RAB-observed-coframe*", "*Y5_R10_RAB_observed_coframe*"):
            formalization_hits.extend(FORMALIZATION.rglob(pattern))
    add(
        "VAL1361_7_formalization_untouched",
        "formalization-workbench untouched by generated outputs",
        len(formalization_hits) == 0,
        f"formalization_generated_output_count={len(formalization_hits)}",
    )

    add(
        "VAL1361_8_next_target_1362",
        "next target routes to quotient observed coframe parent q/Obs or denominator source pack",
        bool(next_target) and str(next_target[0]["target_file"]).startswith("1362-Y5-R10-RAB-quotient-observed-coframe"),
        str(next_target[0]["target_file"]) if next_target else "missing",
    )

    add(
        "VAL1361_9_overall",
        "overall 1361 validation",
        all(row["status"] == "PASS" for row in validations),
        "1361 blocks coframe/tau lock claim and stages strict M_H_ref first-row schema",
    )

    return validations


def build_doc(
    sources: list[dict[str, object]],
    lock_rows: list[dict[str, object]],
    residuals: list[dict[str, object]],
    mhref_rows: list[dict[str, object]],
    gates: list[dict[str, object]],
    decisions: list[dict[str, object]],
    next_target: list[dict[str, object]],
    validations: list[dict[str, object]],
) -> str:
    return "\n\n".join(
        [
            f"# {TITLE}",
            "**Current verdict:** 1361 does not parent-sign the one-observed-coframe plus tau/source/charge/readout lock. The quotient coframe descent theorem is real, but current MTS has not constructed the parent `q`, `Obs_e`, universal matter functor, no-shadow-frame theorem, tau lock, or positive `M_H_ref`.",
            "**Main progress:** the local-GR denominator obstruction is now less foggy. `M_H_ref` has a strict first-row schema requiring `e_obs`, `tau`, `H_tau`, `H_ref`, `Q_tau`, fixed reference, integrability, positivity, source path, and an explicit no-orbital-GM guard.",
            "## Source register",
            table(["source_id", "source_path", "exists", "anchor_found", "purpose"], sources),
            "## Coframe/tau lock attempt",
            table(["lock_id", "claim_piece", "required_identity", "attempt_result", "why_not_claim"], lock_rows),
            "## Frame/tau residual ledger",
            table(["residual_id", "symbol", "definition", "observable_link", "current_status", "required_to_close"], residuals),
            "## MHref first-row schema",
            table(["row_id", "system_id", "quantity", "definition", "formula", "e_obs_id", "tau_id", "surface_outer", "Q_tau_integral", "H_tau", "H_ref", "M_H_ref", "units", "reference_rule", "source_path", "source_anchor", "value_or_theorem", "accepted_for_scoring", "schema_ready", "status"], mhref_rows),
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
    lock_rows = lock_attempt()
    residuals = residual_ledger()
    mhref_rows = mhref_first_row()
    gates = claim_gates()
    decisions = decision_rows()
    next_target = next_rows()
    validations = validate_outputs(sources, lock_rows, residuals, mhref_rows, gates, decisions, next_target)

    write_csv(SOURCE_REGISTER_PATH, sources)
    write_csv(LOCK_ATTEMPT_PATH, lock_rows)
    write_csv(RESIDUAL_LEDGER_PATH, residuals)
    write_csv(MHREF_SCHEMA_PATH, mhref_rows)
    write_csv(CLAIM_GATE_PATH, gates)
    write_csv(DECISION_PATH, decisions)
    write_csv(NEXT_PATH, next_target)
    write_csv(VALIDATION_PATH, validations)
    DOC_PATH.write_text(
        build_doc(sources, lock_rows, residuals, mhref_rows, gates, decisions, next_target, validations),
        encoding="utf-8",
    )


if __name__ == "__main__":
    main()

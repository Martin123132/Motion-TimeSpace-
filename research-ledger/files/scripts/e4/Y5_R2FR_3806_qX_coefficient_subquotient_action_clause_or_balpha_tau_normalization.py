import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path


CHECKPOINT = "3806"
BRANCH = "MTS_R2FR_Y5_QX_COEFFICIENT_SUBQUOTIENT_ACTION_OR_BALPHA_TAU_3806"
ROOT = Path(
    r"D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework"
    r"\Motion-TimeSpace--main"
)
PCW = ROOT / "post-checkpoint-work"
FWB = ROOT / "formalization-workbench"
RESIDUALS = PCW / "source-intake" / "mts_residuals"
DOC_PATH = PCW / "3806-Y5-R2FR-qX-coefficient-subquotient-action-clause-or-balpha-tau-normalization.md"
SCRIPT_PATH = PCW / "scripts" / "Y5_R2FR_3806_qX_coefficient_subquotient_action_clause_or_balpha_tau_normalization.py"

P_3805 = PCW / "3805-Y5-R2FR-no-XQ-visible-coefficient-sequester-theorem-or-component-bound-acquisition.md"
P_3804 = PCW / "3804-Y5-R2FR-qX-calibration-companion-closure-or-local-bound-runner.md"
P_1052 = PCW / "1052-Y5-R10-tau-clock-Xhat-normalization-or-alpha-WEP-R10-projection-source.md"
P_1057 = PCW / "1057-Y5-R10-unique-Maxwell-subblock-no-independent-F2-ban-or-balpha-retention.md"
P_1091 = PCW / "1091-Y5-R10-parent-operator-domain-no-hidden-visible-hom-theorem-or-MOMS-closure.md"
P_SPINE = PCW / "LOCAL_GR_COUPLING_SPINE_CURRENT_STATE.md"

C_3805_THEOREM = RESIDUALS / "P8_Y5_R2FR_3805_SEQUESTER_THEOREM_ATTEMPT.csv"
C_3805_ALPHA = RESIDUALS / "P8_Y5_R2FR_3805_B_ALPHA_PRODUCT_IMPORT_NONCLAIM.csv"
C_1052_TAU = RESIDUALS / "P8_Y5_R10_1052_TAU_CLOCK_XHAT_NORMALIZATION_AUDIT.csv"
C_1052_CLOCK = RESIDUALS / "P8_Y5_R10_1052_ALPHA_CLOCK_PRODUCT_BOUND_LEDGER.csv"
C_1057_GATES = RESIDUALS / "P8_Y5_R10_1057_CLAIM_GATES.csv"

OUTPUTS = {
    "sources": RESIDUALS / "P8_Y5_R2FR_3806_SOURCE_REGISTER.csv",
    "action": RESIDUALS / "P8_Y5_R2FR_3806_COEFFICIENT_SUBQUOTIENT_ACTION_CLAUSE.csv",
    "zero": RESIDUALS / "P8_Y5_R2FR_3806_VARIATIONAL_ZERO_THEOREM.csv",
    "audit": RESIDUALS / "P8_Y5_R2FR_3806_CURRENT_SIGNATURE_AUDIT.csv",
    "tau": RESIDUALS / "P8_Y5_R2FR_3806_B_ALPHA_TAU_NORMALIZATION_AUDIT.csv",
    "components": RESIDUALS / "P8_Y5_R2FR_3806_COMPONENT_BOUND_STATUS.csv",
    "refusal": RESIDUALS / "P8_Y5_R2FR_3806_REFUSAL_RUNNER.csv",
    "gates": RESIDUALS / "P8_Y5_R2FR_3806_CLAIM_GATES.csv",
    "decisions": RESIDUALS / "P8_Y5_R2FR_3806_DECISION_ROWS.csv",
    "next_target": RESIDUALS / "P8_Y5_R2FR_3806_NEXT_TARGET.csv",
    "status": RESIDUALS / "P8_Y5_R2FR_3806_STATUS.csv",
    "validation": RESIDUALS / "P8_Y5_BRR545_3806_VALIDATION.csv",
}

SOURCE_SPECS = [
    ("SRC3806_0_3805_handoff", P_3805, "Coeff_vis", "3805 typed sequester target"),
    ("SRC3806_1_3804_runner", P_3804, "C_qX_companion_abs", "3804 companion vector"),
    ("SRC3806_2_1052_tau_doc", P_1052, "tau_clock_time := d chi_X / dt", "tau-clock/Xhat normalization audit"),
    ("SRC3806_3_1057_F2_doc", P_1057, "UMS1057_2_no_independent_F2", "no-independent-F2 counterterm gate"),
    ("SRC3806_4_1091_hom_doc", P_1091, "no hidden-visible coefficient homomorphisms", "operator-domain/no-hidden-visible-hom theorem attempt"),
    ("SRC3806_5_3805_theorem_csv", C_3805_THEOREM, "SQT3805_0_typed_subquotient_sequester", "3805 sequester theorem rows"),
    ("SRC3806_6_3805_alpha_csv", C_3805_ALPHA, "BAP3805_0_import_1051_best_balpha_tau", "3805 imported b_alpha tau product"),
    ("SRC3806_7_1052_tau_csv", C_1052_TAU, "TCN1052_4_verdict", "1052 tau-clock normalization verdict"),
    ("SRC3806_8_1052_clock_csv", C_1052_CLOCK, "ACB1052_2", "1052 best clock product row"),
    ("SRC3806_9_1057_gates_csv", C_1057_GATES, "CG1057_0_unique_F2", "1057 unique F2 claim gate"),
    ("SRC3806_10_spine", P_SPINE, "3806-Y5-R2FR-qX-coefficient-subquotient-action-clause-or-balpha-tau-normalization.md", "live spine target"),
]


def read_text(path):
    return path.read_text(encoding="utf-8", errors="replace")


def load_csv(path):
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def write_csv(path, rows):
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        raise ValueError(f"no rows for {path}")
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()), lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def csv_parses(path):
    try:
        load_csv(path)
        return True
    except Exception:
        return False


def bool_text(value):
    return "true" if value else "false"


def source_rows(timestamp):
    rows = []
    for source_id, path, needle, role in SOURCE_SPECS:
        exists = path.exists()
        needle_found = exists and needle in read_text(path)
        rows.append(
            {
                "timestamp_utc": timestamp,
                "branch_id": BRANCH,
                "checkpoint_id": CHECKPOINT,
                "source_id": source_id,
                "source_path": str(path),
                "exists": bool_text(exists),
                "needle": needle,
                "needle_found": bool_text(needle_found),
                "role": role,
                "valid_for_claim": "false",
            }
        )
    return rows


def action_rows(timestamp):
    specs = [
        (
            "CSA3806_0_field_space",
            "typed q_X field space",
            "Use q_X=(q_obs,X_Q), pi_obs:q_X->q_obs, Y_Q=Pi4(X_Q), B_Q=B_Q[Y_Q], and visible coefficient fields c_J in C_vis={Z_EM,m_A,y_A,kappa_eff,w_A,nu_i,D_boundary,...}.",
            "Defines the typed split: X_Q may own B_Q/EM geometry, while ordinary visible coefficients are separate objects.",
            "MISSING_PARENT_TYPED_FIELD_SPACE_SIGNATURE",
        ),
        (
            "CSA3806_1_action_clause",
            "coefficient-subquotient action grammar",
            "S_parent^qX = S_Qspec[X_Q,Y_Q,lambda] + S_BQ[X_Q,Y_Q,theta_Q] + S_vis[psi,g_obs(pi_obs(q_X)),A_Q(B_Q[Y_Q]),c_J] + int sqrt(-g_obs) sum_J Lambda_J (c_J-cbar_J(pi_obs(q_X),theta_rep)) O_J^0.",
            "The Lagrange/constraint sector forces c_J to be pullbacks from pi_obs(q_X)=q_obs and representation data, not arbitrary functions of full q_X.",
            "CLAUSE_WRITTEN_HERE_NOT_STRICT_CORPUS_SIGNED",
        ),
        (
            "CSA3806_2_allowed_XQ_path",
            "only B_Q reads X_Q",
            "The only visible-sector path allowed to read X_Q is X_Q -> Y_Q -> B_Q[Y_Q] -> A_Q,F_Q. Coefficient functors Coeff_vis may read pi_obs(q_X), theta_rep, and fixed topological/representation labels only.",
            "This keeps the EM geometry route while forbidding f(X_Q)F^2, m_A(X_Q), kappa(X_Q), source weights, and marker coefficients.",
            "MISSING_PARENT_NO_MIXED_COEFFICIENT_FUNCTOR_SIGNATURE",
        ),
        (
            "CSA3806_3_no_mixed_ideal",
            "excluded mixed coefficient ideal",
            "The parent operator domain quotients out or forbids I_mix={<nonconstant function of X_Q>*O_vis} for O_vis in {F^2, psi_bar psi, R, S_A, clock/readout, boundary flux}, except for the declared B_Q connection construction.",
            "This is the action-level repair of the 3805 q_X-basic counterexample.",
            "MISSING_OPERATOR_DOMAIN_EXHAUSTION_AND_RADIOACTIVE_READOUT_CLOSURE",
        ),
        (
            "CSA3806_4_effective_closure",
            "radiative/readout closure clause",
            "The same subquotient rule must hold for renormalized coefficients c_J^eff and readout maps: c_J^eff=cbar_J^eff(pi_obs(q_X),theta_rep) unless a sourced finite residual is declared.",
            "Bare sequester is insufficient unless loops/effective reductions/readout cannot reintroduce X_Q-visible coefficients.",
            "MISSING_EFFECTIVE_ACTION_AND_READOUT_CLOSURE",
        ),
    ]
    return [
        {
            "timestamp_utc": timestamp,
            "branch_id": BRANCH,
            "checkpoint_id": CHECKPOINT,
            "clause_id": clause_id,
            "clause": clause,
            "mathematical_form": form,
            "result_if_signed": result,
            "missing_for_current_claim": missing,
            "valid_for_claim": "false",
        }
        for clause_id, clause, form, result, missing in specs
    ]


def zero_rows(timestamp):
    specs = [
        (
            "VZT3806_0_chain_rule",
            "visible coefficient derivative zero",
            "If c_J=cbar_J(pi_obs(q_X),theta_rep), then partial_XQ c_J|_{q_obs,theta_rep}=0. Therefore partial_XQ Z_EM=partial_XQ m_A=partial_XQ kappa_eff=partial_XQ w_A=partial_XQ nu_i=partial_XQ D_boundary=0 outside B_Q.",
            "EXACT_CONDITIONAL_CHAIN_RULE_ZERO",
            "Sets the visible-coefficient pieces of epsilon_ZEM_XQ, epsilon_theta_XQ, epsilon_kappa_XQ, epsilon_source_XQ, and epsilon_boundary_XQ to zero.",
            "requires CSA3806 action clause parent-signed",
        ),
        (
            "VZT3806_1_variation_split",
            "q_X variation of S_vis",
            "delta_XQ S_vis = (delta S_vis/delta A_Q).delta_XQ A_Q[B_Q] + sum_J (partial S_vis/partial c_J).delta_XQ c_J. Under CSA3806, the second term vanishes and the first is the declared same-source EM path.",
            "EXACT_CONDITIONAL_VARIATION_SPLIT",
            "No visible coefficient fifth-force remains; B_Q/EM exchange still needs same-current/Hilbert handling from 3792/3803.",
            "same-current and B_Q calibration companions remain separate gates",
        ),
        (
            "VZT3806_2_no_lambda_F2",
            "independent F2 exclusion",
            "An independent DeltaS=-1/4 int sqrt(-g) lambda_A(X_Q)F_Q^2 is illegal only inside the CSA3806 operator domain. If this domain is not parent-signed, 1057/3791 counterexamples remain active.",
            "COUNTEREXAMPLE_GUARD",
            "Explains why the written clause is the needed repair and why ordinary symmetry is not enough.",
            "operator-domain exhaustion not strict-current derived",
        ),
        (
            "VZT3806_3_strict_current_verdict",
            "strict current claim",
            "The clause is a coherent parent action extension/contract, not a strict-current derivation. Current files support the syntax but do not prove that MTS already uses this typed coefficient subquotient.",
            "PASS_CONDITIONAL_CLAUSE_FAIL_STRICT_CLAIM",
            "Use the clause as the next candidate parent signature; retain finite component rows until signed.",
            "no current parent source contains CSA3806 syntax",
        ),
    ]
    return [
        {
            "timestamp_utc": timestamp,
            "branch_id": BRANCH,
            "checkpoint_id": CHECKPOINT,
            "theorem_id": theorem_id,
            "claim_piece": claim,
            "mathematical_form": form,
            "derivation_status": status,
            "result_if_signed": result,
            "missing_for_current_claim": missing,
            "valid_for_claim": "false",
        }
        for theorem_id, claim, form, status, result, missing in specs
    ]


def audit_rows(timestamp):
    specs = [
        ("AUD3806_0_clause_written", "subquotient action clause", "3806 writes explicit CSA3806 syntax.", "CONDITIONAL_PARENT_EXTENSION_READY", "not found in strict corpus"),
        ("AUD3806_1_no_F2", "independent F2", "1057/3791 show F2 slots are legal unless operator-domain exhausted.", "ACTIVE_COUNTEREXAMPLE_WITHOUT_CLAUSE", "operator-domain exhaustion unsigned"),
        ("AUD3806_2_no_hom", "no hidden-visible coefficient hom", "1091/1051 show scalar obstruction survives.", "ACTIVE_COUNTEREXAMPLE_WITHOUT_CLAUSE", "hidden invariant triviality/no-mixed hom unsigned"),
        ("AUD3806_3_tau", "b_alpha tau product", "1052 says tau_clock_time is product-defined, not parent-derived.", "PRODUCT_BOUND_ONLY", "standalone b_alpha blocked"),
        ("AUD3806_4_runner", "3804 local runner", "C_qX_companion_abs waits on component values or theorem-zero clauses.", "RUNNER_STILL_BLOCKED", "CSA3806 not signed and tau not normalized"),
    ]
    return [
        {
            "timestamp_utc": timestamp,
            "branch_id": BRANCH,
            "checkpoint_id": CHECKPOINT,
            "audit_id": audit_id,
            "item": item,
            "current_evidence": evidence,
            "status": status,
            "missing_for_claim": missing,
            "valid_for_claim": "false",
        }
        for audit_id, item, evidence, status, missing in specs
    ]


def tau_rows(timestamp):
    best_1sigma = "2.1e-18"
    best_2sigma = "3.2e-18"
    diagnostic = "2.93296e-08"
    if C_1052_CLOCK.exists():
        for row in load_csv(C_1052_CLOCK):
            if row.get("bound_id") == "ACB1052_2" or row.get("chain_id") == "ACB1052_2":
                best_1sigma = row.get("product_bound_1sigma_yr_inv", best_1sigma)
                best_2sigma = row.get("product_bound_2sigma_yr_inv", best_2sigma)
                diagnostic = row.get("H0_normalized_diagnostic", diagnostic)
    specs = [
        ("BTN3806_0_product_bound", "best clock product", f"|b_alpha*tau_clock_time| <= {best_1sigma} yr^-1 at 1sigma and {best_2sigma} yr^-1 at 2sigma", "SOURCE_BACKED_NONCLAIM_PRODUCT", "standalone b_alpha not ready"),
        ("BTN3806_1_tau_definition", "tau_clock_time", "tau_clock_time := d chi_X/dt and d ln alpha_EM/dt=b_alpha*tau_clock_time", "DEFINED_PRODUCT_MAP_NOT_PARENT_DERIVED", "chi_X parent state/local time projection missing"),
        ("BTN3806_2_H0_diagnostic", "H0 diagnostic", f"if tau_clock_time=H0*dchi_X/dN were assumed, |b_alpha*dchi_X/dN| <= {diagnostic}", "DIAGNOSTIC_ONLY", "not a theory prediction"),
        ("BTN3806_3_standalone_refusal", "standalone b_alpha", "b_alpha=(d ln R/dt)/(DeltaK_alpha*tau_clock_time)", "REFUSED", "tau_clock_time and X_Q/chi_X normalization not derived"),
        ("BTN3806_4_CSA_zero_branch", "if CSA3806 signed", "visible coefficient sequester would set b_alpha coefficient leakage to zero before needing clock product promotion", "CONDITIONAL_ONLY", "CSA3806 not parent-signed"),
    ]
    return [
        {
            "timestamp_utc": timestamp,
            "branch_id": BRANCH,
            "checkpoint_id": CHECKPOINT,
            "row_id": row_id,
            "object": obj,
            "formula_or_bound": formula,
            "status": status,
            "missing_for_claim": missing,
            "valid_for_claim": "false",
        }
        for row_id, obj, formula, status, missing in specs
    ]


def component_rows(timestamp):
    specs = [
        ("CBS3806_0_epsilon_ZEM_XQ", "epsilon_ZEM_XQ", "zero if CSA3806 and no independent F2/effective readout re-entry are signed; otherwise retain beta_Z/lambda/b_alpha product branch", "MISSING_CSA3806_SIGNATURE_OR_ZEM_BOUND", "highest"),
        ("CBS3806_1_epsilon_theta_XQ", "epsilon_theta_XQ", "zero if masses/material/clock/source markers are CSA3806 coefficient fields over pi_obs(q_X); otherwise sensitivity bounds required", "MISSING_THETA_SUBQUOTIENT_OR_SENSITIVITIES", "high"),
        ("CBS3806_2_epsilon_source_XQ", "epsilon_source_XQ", "zero if source weights w_A are excluded from X_Q coefficient functors and direct source derivative certificate holds", "MISSING_SOURCE_WEIGHT_EXCLUSION", "high"),
        ("CBS3806_3_epsilon_kappa_XQ", "epsilon_kappa_XQ", "zero if kappa_eff=cbar_kappa(pi_obs(q_X)) or global/superselected; otherwise Gdot/PPN bound row required", "MISSING_KAPPA_SUBQUOTIENT_OR_BOUND", "medium"),
        ("CBS3806_4_epsilon_boundary_XQ", "epsilon_boundary_XQ", "zero if boundary weights factor through pi_obs(q_X) and no-flux/domain clauses hold; otherwise flux bound required", "MISSING_BOUNDARY_SUBQUOTIENT_OR_FLUX_BOUND", "medium"),
    ]
    return [
        {
            "timestamp_utc": timestamp,
            "branch_id": BRANCH,
            "checkpoint_id": CHECKPOINT,
            "row_id": row_id,
            "symbol": symbol,
            "conditional_resolution": resolution,
            "current_value": current,
            "priority": priority,
            "valid_for_claim": "false",
            "blocks_claim": "true",
        }
        for row_id, symbol, resolution, current, priority in specs
    ]


def refusal_rows(timestamp):
    specs = [
        ("REF3806_0_CSA_claim", "CSA3806 is current MTS theorem", "REFUSED_STRICT_CURRENT", "clause written here but not parent-signed in current corpus"),
        ("REF3806_1_local_GR", "q_X local-GR closure", "REFUSED", "CSA3806, same-current, Qspec stress, and component values not all closed"),
        ("REF3806_2_balpha", "standalone b_alpha from clocks", "REFUSED", "tau_clock_time and X_Q/chi_X normalization not derived"),
        ("REF3806_3_R10_WEP_transfer", "clock product transfers to WEP/R10", "REFUSED", "tau_WEP/tau_R10, source/test charges, K_X/Z_X, and shared projection missing"),
    ]
    return [
        {
            "timestamp_utc": timestamp,
            "branch_id": BRANCH,
            "checkpoint_id": CHECKPOINT,
            "refusal_id": rid,
            "object": obj,
            "refusal_status": status,
            "failure_reasons": reason,
            "claim_allowed": "false",
            "valid_for_claim": "false",
        }
        for rid, obj, status, reason in specs
    ]


def gates(timestamp, grouped):
    sources_ok = all(row["exists"] == "true" for row in grouped["sources"])
    needles_ok = all(row["needle_found"] == "true" for row in grouped["sources"])
    comp_nonclaim = all(row["blocks_claim"] == "true" for row in grouped["components"])
    specs = [
        ("CG3806_0_sources", sources_ok and needles_ok, "all sources and needles found"),
        ("CG3806_1_action_clause_written", True, "CSA3806 coefficient-subquotient action grammar emitted"),
        ("CG3806_2_chain_rule_zero", True, "conditional visible coefficient derivative zero theorem emitted"),
        ("CG3806_3_current_parent_signed", False, "CSA3806 is not strict-current parent-signed"),
        ("CG3806_4_tau_normalized", False, "tau_clock_time remains product-defined, not parent-derived"),
        ("CG3806_5_components_nonclaim", comp_nonclaim, "component rows remain blockers"),
        ("CG3806_6_claims_closed", False, "no local-GR/EM/Newton/clock/R10/WEP claim allowed"),
    ]
    return [
        {
            "timestamp_utc": timestamp,
            "branch_id": BRANCH,
            "checkpoint_id": CHECKPOINT,
            "gate_id": gid,
            "pass": bool_text(passed),
            "claim_allowed": "false",
            "details": detail,
            "valid_for_claim": "false",
        }
        for gid, passed, detail in specs
    ]


def decision_rows(timestamp):
    specs = [
        ("DEC3806_0_progress", "The exact parent action syntax now exists.", "CSA3806 makes visible coefficients pull back from pi_obs(q_X), while only B_Q reads X_Q.", "Use CSA3806 as the parent-signature target."),
        ("DEC3806_1_nonclaim", "CSA3806 is not yet a strict-current derivation.", "The source corpus has contracts and counterexamples, not a signed action-domain theorem.", "Keep component rows and runner blocks active."),
        ("DEC3806_2_tau", "The clock product remains product-only.", "1052 blocks standalone b_alpha because tau_clock_time is not parent-derived.", "Do not transfer the 2.1e-18 row to WEP/R10 without tau/projection maps."),
        ("DEC3806_3_next", "Next target should try to parent-sign CSA3806 from MTS primitives or derive the effective-action closure.", "The bare grammar is now written; the risk is whether it survives readout/radiative closure and is actually owned by MTS.", "Move to 3807 parent-signature/effective closure audit."),
    ]
    return [
        {
            "timestamp_utc": timestamp,
            "branch_id": BRANCH,
            "checkpoint_id": CHECKPOINT,
            "decision_id": did,
            "decision": decision,
            "rationale": rationale,
            "action": action,
            "valid_for_claim": "false",
        }
        for did, decision, rationale, action in specs
    ]


def next_rows(timestamp):
    return [
        {
            "timestamp_utc": timestamp,
            "branch_id": BRANCH,
            "checkpoint_id": CHECKPOINT,
            "target_doc": "3807-Y5-R2FR-CSA3806-parent-signature-or-effective-readout-closure-audit.md",
            "target_script": "scripts/Y5_R2FR_3807_CSA3806_parent_signature_or_effective_readout_closure_audit.py",
            "objective": "Search the MTS parent corpus for a signed action-domain/effective-readout rule equivalent to CSA3806; if absent, keep CSA3806 as an explicit closure axiom candidate and route to source-backed component bounds.",
            "avoid": "do not treat the newly written action grammar as already present in the strict corpus",
            "valid_for_claim": "false",
        }
    ]


def status_rows(timestamp):
    return [
        {
            "timestamp_utc": timestamp,
            "branch_id": BRANCH,
            "checkpoint_id": CHECKPOINT,
            "status": "PASS_NONCLAIM_CSA3806_ACTION_CLAUSE_WRITTEN_TAU_PRODUCT_RETAINED",
            "headline": "The q_X coefficient-subquotient action grammar is written and gives a conditional chain-rule zero; strict-current parent signature and tau-clock normalization remain unsigned.",
            "claim_allowed": "false",
            "next_target": "3807 CSA3806 parent signature or effective readout closure audit",
        }
    ]


def validation_rows(timestamp, grouped):
    sources_ok = all(row["exists"] == "true" for row in grouped["sources"])
    needles_ok = all(row["needle_found"] == "true" for row in grouped["sources"])
    csv_ok = all(csv_parses(path) for key, path in OUTPUTS.items() if key != "validation")
    action_text = "\n".join(row["mathematical_form"] for row in grouped["action"])
    zero_text = "\n".join(row["mathematical_form"] for row in grouped["zero"])
    tau_text = "\n".join(row["formula_or_bound"] for row in grouped["tau"])
    all_gates_closed = all(row["claim_allowed"] == "false" for row in grouped["gates"])
    fwb_hits = []
    if FWB.exists():
        for pattern in ("*Y5_R2FR_3806*", "*3806-Y5*", "*P8_Y5*3806*"):
            fwb_hits.extend(FWB.rglob(pattern))
    pycache_clean = not (PCW / "scripts" / "__pycache__").exists()
    doc_text = read_text(DOC_PATH) if DOC_PATH.exists() else ""
    script_text = read_text(SCRIPT_PATH) if SCRIPT_PATH.exists() else ""
    bad_chars_clean = chr(0x00C2) not in doc_text + script_text and chr(0xFFFD) not in doc_text + script_text
    checks = [
        ("sources_exist", sources_ok, "every cited source path exists"),
        ("needles_found", needles_ok, "every cited source needle was found"),
        ("csv_outputs_parse", csv_ok, "all generated CSV outputs exist and parse"),
        ("doc_written", DOC_PATH.exists(), "3806 markdown document written"),
        ("action_clause_present", "S_parent^qX" in action_text and "c_J-cbar_J(pi_obs(q_X),theta_rep)" in action_text, "CSA3806 action grammar emitted"),
        ("chain_rule_zero_present", "partial_XQ c_J" in zero_text and "delta_XQ S_vis" in zero_text, "variation split and chain-rule zero emitted"),
        ("tau_product_retained", "2.1e-18" in tau_text and "REFUSED" in "\n".join(row["status"] for row in grouped["tau"]), "b_alpha tau product retained but standalone refused"),
        ("claims_closed", all_gates_closed, "no claim gate allows a claim"),
        ("formalization_clean", not fwb_hits, "no 3806 files written under formalization-workbench"),
        ("pycache_removed", pycache_clean, "scripts __pycache__ removed"),
        ("bad_chars_clean", bad_chars_clean, "new doc/script contain no mojibake replacement characters"),
    ]
    return [
        {
            "timestamp_utc": timestamp,
            "branch_id": BRANCH,
            "checkpoint_id": CHECKPOINT,
            "check_id": cid,
            "result": "PASS" if passed else "FAIL",
            "detail": detail,
        }
        for cid, passed, detail in checks
    ]


def row_bullet(row, key_fields):
    label = " ".join(f"`{row[field]}`" for field in key_fields if field in row and row[field])
    rest = "; ".join(
        f"{key}: {value}"
        for key, value in row.items()
        if key not in key_fields and key not in {"timestamp_utc", "branch_id", "checkpoint_id"}
    )
    return f"- {label}: {rest}"


def write_markdown(grouped):
    lines = [
        "# 3806 - qX Coefficient Subquotient Action Clause or b_alpha tau Normalization",
        "",
        "## Status",
        "",
        "`PASS_NONCLAIM_CSA3806_ACTION_CLAUSE_WRITTEN_TAU_PRODUCT_RETAINED`.",
        "",
        "3806 writes the action-level repair that 3805 demanded. The parent grammar is now explicit:",
        "",
        "`S_parent^qX = S_Qspec + S_BQ[X_Q,Y_Q] + S_vis[psi,g_obs(pi_obs(q_X)),A_Q(B_Q[Y_Q]),c_J] + int sqrt(-g_obs) sum_J Lambda_J (c_J-cbar_J(pi_obs(q_X),theta_rep)) O_J^0`.",
        "",
        "So visible coefficients `c_J={Z_EM,m_A,y_A,kappa_eff,w_A,nu_i,D_boundary,...}` see `pi_obs(q_X)=q_obs`, not full `q_X`. The only allowed `X_Q` route into visible physics is `X_Q -> Y_Q -> B_Q -> A_Q,F_Q`.",
        "",
        "This gives the exact chain-rule zero for visible coefficient leakage if parent-signed. It is not yet a strict-current claim.",
        "",
        "## Result In Plain Terms",
        "",
        "We now have the actual clause a future parent action must contain. This is better than saying 'no coupling please': it is syntax-level separation of EM geometry from visible coefficients.",
        "",
        "The fallback did not promote: the clock row still only says `|b_alpha*tau_clock_time| <= 2.1e-18 yr^-1`. `tau_clock_time` is not parent-derived, so no standalone `b_alpha` and no WEP/R10 transfer.",
        "",
        "## Compact Result",
        "",
        "`CSA3806` is the candidate action-domain closure.",
        "",
        "If signed, `partial_XQ c_J=0` for visible coefficients.",
        "",
        "Strict-current MTS has not signed it yet.",
        "",
        "The alpha clock bound remains product-only.",
        "",
    ]
    sections = [
        ("Source Register", "sources", ["source_id"]),
        ("Coefficient Subquotient Action Clause", "action", ["clause_id", "clause"]),
        ("Variational Zero Theorem", "zero", ["theorem_id", "claim_piece"]),
        ("Current Signature Audit", "audit", ["audit_id", "item"]),
        ("b_alpha tau Normalization Audit", "tau", ["row_id", "object"]),
        ("Component Bound Status", "components", ["row_id", "symbol"]),
        ("Refusal Runner", "refusal", ["refusal_id", "object"]),
        ("Claim Gates", "gates", ["gate_id"]),
        ("Decisions", "decisions", ["decision_id"]),
        ("Next Target", "next_target", ["target_doc"]),
        ("Validation", "validation", ["check_id", "result"]),
    ]
    for title, key, key_fields in sections:
        lines.append(f"## {title}")
        for row in grouped[key]:
            lines.append(row_bullet(row, key_fields))
    DOC_PATH.write_text("\n".join(lines) + "\n", encoding="utf-8")


def cleanup_pycache():
    pycache = PCW / "scripts" / "__pycache__"
    if pycache.exists():
        shutil.rmtree(pycache)


def main():
    timestamp = datetime.now(timezone.utc).isoformat(timespec="seconds")
    grouped = {
        "sources": source_rows(timestamp),
        "action": action_rows(timestamp),
        "zero": zero_rows(timestamp),
        "audit": audit_rows(timestamp),
        "tau": tau_rows(timestamp),
        "components": component_rows(timestamp),
        "refusal": refusal_rows(timestamp),
        "decisions": decision_rows(timestamp),
        "next_target": next_rows(timestamp),
        "status": status_rows(timestamp),
    }
    grouped["gates"] = gates(timestamp, grouped)
    for key, path in OUTPUTS.items():
        if key not in {"validation"}:
            write_csv(path, grouped[key])
    grouped["validation"] = [{"timestamp_utc": timestamp, "branch_id": BRANCH, "checkpoint_id": CHECKPOINT, "check_id": "pending", "result": "PASS", "detail": "placeholder before final validation"}]
    write_markdown(grouped)
    cleanup_pycache()
    grouped["validation"] = validation_rows(timestamp, grouped)
    write_csv(OUTPUTS["validation"], grouped["validation"])
    write_markdown(grouped)
    cleanup_pycache()
    failed = [row for row in grouped["validation"] if row["result"] != "PASS"]
    print(grouped["status"][0]["status"])
    print(f"wrote {DOC_PATH}")
    if failed:
        raise SystemExit(f"validation failed: {failed}")


if __name__ == "__main__":
    main()

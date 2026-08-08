from __future__ import annotations

import csv
import sys
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(r"D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work")
RESIDUALS = ROOT / "source-intake" / "mts_residuals"
FORMALIZATION = ROOT.parent / "formalization-workbench"
CHECKPOINT_ID = "3691"
BRANCH_ID = "MTS_R2FR_Y5_VERTICAL_Q_MAP_SOURCE_CURRENT_ORTHOGONALITY_OR_JA_COEFFICIENT_ACQUISITION_3691"
DOC = ROOT / "3691-Y5-R2FR-vertical-q-map-source-current-orthogonality-or-JA-coefficient-acquisition.md"


def stamp() -> str:
    return datetime.now(timezone.utc).isoformat()


def base(ts: str) -> dict[str, object]:
    return {"timestamp_utc": ts, "branch_id": BRANCH_ID, "checkpoint_id": CHECKPOINT_ID, "valid_for_claim": False}


def read_text(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        return path.read_text(encoding="utf-8", errors="replace")


def write_csv(path: Path, rows: list[dict[str, object]]) -> None:
    if not rows:
        raise ValueError(f"no rows for {path}")
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def load_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def parse_csv(path: Path) -> tuple[bool, int]:
    try:
        return True, len(load_csv(path))
    except Exception:
        return False, 0


def source_register(ts: str) -> list[dict[str, object]]:
    specs = [
        ("handoff_3690", RESIDUALS / "P8_Y5_R2FR_3690_NEXT_TARGET.csv", "vertical/source orthogonality", "3690 selected vertical q-map/source-current target"),
        ("ja_gates_3690", RESIDUALS / "P8_Y5_R2FR_3690_JA_ZERO_GATE_ROWS.csv", "JZG3690_3_source_orthogonality", "open J_A zero gates"),
        ("ja_decomp_3690", RESIDUALS / "P8_Y5_R2FR_3690_JA_DECOMPOSITION_ROWS.csv", "JAD3690_3_source_norm", "matter/source decomposition"),
        ("arena_3690", RESIDUALS / "P8_Y5_R2FR_3690_JA_ARENA_TEMPLATE_ROWS.csv", "JAR3690_3_Newton_source", "J_A arena templates"),
        ("vertical_3631", RESIDUALS / "P8_Y5_R2FR_3631_VERTICAL_GENERATOR_TEST.csv", "VGT3631_4_verdict", "vertical generator test already formulated"),
        ("dcdagger_3631", RESIDUALS / "P8_Y5_R2FR_3631_DCDAGGER_VERTICAL_GENERATOR_MAP.csv", "DVG3631_1_verticality_gate", "DCdagger-to-vertical contract"),
        ("dq_leak_3631", RESIDUALS / "P8_Y5_R2FR_3631_DQ_Z_LEAK_AND_JZ_COEFFICIENTS.csv", "DQL3631_0_Dq_Z", "Dq leak and J_Z coefficient rows"),
        ("zmap_3631", RESIDUALS / "P8_Y5_R2FR_3631_Z_OBSERVABLE_MAP.csv", "ZOM3631_7_verdict", "Z observable map not claimed"),
        ("source_2642", RESIDUALS / "P8_Y5_SOURCE_CURRENT_IDENTITY_2642_PROOF_ATTEMPT.csv", "SCI2642_1_JH_descent", "Hilbert source descent conditional lemma"),
        ("bounds_2642", RESIDUALS / "P8_Y5_SOURCE_CURRENT_IDENTITY_2642_COMPONENT_BOUND_PACK.csv", "SCB2642_0_master", "source-current component bound pack"),
        ("leak_2643", RESIDUALS / "P8_Y5_COMMON_DESCENT_DQZ_2643_DQZ_JH_LEAK_BOUND_ROWS.csv", "LEAK2643_1_Dq_Z_norm", "DqZ/common matter leak bounds"),
        ("em_current_3650", RESIDUALS / "P8_Y5_R2FR_3650_SOURCE_CURRENT_THEOREM_ATTEMPT.csv", "SCT3650_2_beta_zero_law", "EM/source-current normalization theorem"),
        ("pim_lock_2579", RESIDUALS / "P8_Y5_EH_DESCENT_COUPLING_PIM_2579_COUPLING_PIM_LOCK_GATE.csv", "CPG2579_6_verdict", "Pi_M/source coupling lock remains open"),
    ]
    rows = []
    for source_id, path, needle, relevance in specs:
        text = read_text(path) if path.exists() else ""
        rows.append({**base(ts), "source_id": source_id, "source_path": str(path), "exists": path.exists(), "needle": needle, "needle_found": needle in text, "relevance": relevance})
    return rows


def vertical_gate_rows(ts: str) -> list[dict[str, object]]:
    specs = [
        ("VQ3691_0_parent_q", "parent quotient map", "q:Phi_parent->Q_MTS is written before readout and includes observed metric/coframe/source/readout/boundary data", "MISSING_PARENT_Q_MAP", "R_qmap"),
        ("VQ3691_1_generator", "vertical generator", "e_A belongs to ker(Dq): Dq[e_A]=0 for every observed matter/source/readout/boundary component", "MISSING_DQ_VERTICAL_GENERATOR_MAP", "R_Zvertical"),
        ("VQ3691_2_naive_Z", "naive partial_Z generator", "partial_Z q=0 in a product chart", "NOT_PROVED_RETAIN_DQ_Z_LEAK", "Dq_Z_norm"),
        ("VQ3691_3_compensated", "compensated generator", "e_A=partial_ZA-C_A^I partial_QI with D_Q q[C_A]=D_ZA q", "FORMAL_REPAIR_NOT_PARENT_ADMISSIBLE", "Dq_comp_residual"),
        ("VQ3691_4_DCd", "DCdagger generator test", "Omega_flat(e_X)=DCdagger[X] then Dq[e_X]=0 and boundary charge proper", "TEST_WRITTEN_NOT_RUNNABLE_WITHOUT_Q_OMEGA_BOUNDARY", "R_DCd_vertical"),
        ("VQ3691_5_constraint_first", "constraint-first route", "S_parent=S_obs[q]+int Lambda^A C_A, e_epsilon={Phi,G[epsilon]}, Dq[e_epsilon]=0, Q_boundary=0/proper", "BEST_ROUTE_SELECTED_NOT_CLOSED", "R_constraint_owner"),
        ("VQ3691_6_verdict", "verticality for canonical Z", "VQ3691_0..5 pass in one parent branch", "VERTICAL_Q_MAP_NOT_CLAIMED", "R_qmap+R_Zvertical+Dq_Z_norm"),
    ]
    return [{**base(ts), "gate_id": gate_id, "gate": gate, "requirement": requirement, "status": status, "residual_if_failed": residual, "claim_allowed": False, "score_ready": False} for gate_id, gate, requirement, status, residual in specs]


def source_orthogonality_rows(ts: str) -> list[dict[str, object]]:
    specs = [
        ("SO3691_0_matter", "ordinary Hilbert matter leg", "delta_Z S_matter=(delta Sbar_matter/delta q)Dq[e_A]delta Z^A", "J_A^matter=0 if matter descends through q and e_A is vertical", "CONDITIONAL_ZERO_NOT_PARENT_SIGNED", "eps_JH_Z_abs"),
        ("SO3691_1_source_current", "source current leg", "Pi_M,J_H,M_eff,G_eff are q-owned/fixed or orthogonal to vertical charges", "J_A^source=0 if Pi_M/J_H do not vary along e_A", "CONDITIONAL_ZERO_SOURCE_LOCK_UNSIGNED", "eps_source_current"),
        ("SO3691_2_EM_charge", "EM/source normalization leg", "beta_source_alpha,A = Lie_vX ln n_A + Lie_vX ln Z_JA + Lie_vX ln N_A + Lie_vX ln chi_material,A", "zero if charge lattice/current renormalization/source measure/material labels descend through q/fixed reps", "CONDITIONAL_ZERO_COUNTERMODEL_LIVE", "beta_source_alpha"),
        ("SO3691_3_projector_PiM", "Pi_M projector derivative", "partial_A Pi_M(Phi0)=0 and [d,Pi_M]J_H=0", "zero if Pi_M is q-owned and same-domain with J_H", "PIM_DERIVATIVE_COMMUTATOR_OPEN", "epsilon_DPiM+I_commutator"),
        ("SO3691_4_readout_marker", "theta/material/source marker", "no representative marker theta(Z), no source-only weight, no readout re-entry", "zero only if parent object language forbids marker/readout source slots", "MARKER_SOURCE_SLOT_UNSIGNED", "eps_theta_marker+Delta_w_abs"),
        ("SO3691_5_boundary", "boundary/source-worldtube leg", "B_A=0 or source boundary contribution is fixed/exact/proper", "zero only with boundary class and source-worldtube owner", "BOUNDARY_SOURCE_OPEN", "eps_B_abs"),
        ("SO3691_6_verdict", "matter/source orthogonality for J_A", "all SO3691_0..5 pass in one parent branch", "zero only if matter/source/projector/readout/boundary legs are signed in the same parent branch", "MATTER_SOURCE_ORTHOGONALITY_NOT_CLAIMED", "R_Jmatter+R_Jsource"),
    ]
    return [{**base(ts), "orthogonality_id": oid, "piece": piece, "formula": formula, "zero_condition": zero, "status": status, "residual_if_failed": residual, "claim_allowed": False, "score_ready": False} for oid, piece, formula, zero, status, residual in specs]


def coefficient_acquisition_rows(ts: str) -> list[dict[str, object]]:
    specs = [
        ("JAC3691_0_Dq", "Dq_Z_norm", "Dq_Z_norm := ||Dq[v_Z]||_q/||v_Z||_Z", "all observed arenas", "q map, Z basis, q/Z norms, source/readout descent", "MISSING_NUMERIC_OR_THEOREM_ZERO"),
        ("JAC3691_1_JH", "eps_JH_Z_abs", "eps_JH_Z_abs <= C_matter*Dq_Z_norm + eps_theta_marker + eps_direct_Z + eps_source_weight + eps_matter_boundary", "Newton;PPN;R10;WEP;clock;orbital;EM", "C_matter, Dq_Z value, theta/no-marker, source-weight, matter-boundary rows", "BOUND_FORM_READY_VALUES_MISSING"),
        ("JAC3691_2_master", "Delta_A source-current residual", "Delta_A <= ||L_A M^-1||*(eps_JH_Z_abs+eps_JNH_abs+eps_B_abs+Delta_readout_abs_A+Q_cdb_abs+eps_projector_abs)+E_DqZ_A", "Newton;PPN;R10;WEP;clock;orbital;EM", "M_AB, L_A, source components, DqZ map, units", "MASTER_BOUND_FORM_READY_VALUES_MISSING"),
        ("JAC3691_3_Newton", "K_mu_JA", "delta_mu_JA = K_mu_JA * Pi_M(L^{-1}J_A)", "Newton;R10;R11", "source mass/range profile, Pi_M, L inverse, worldtube source", "MISSING_SOURCE_MASS_AND_RANGE_PROFILE"),
        ("JAC3691_4_PPN", "K_gamma_JA,K_beta_JA,P_PF", "Delta PPN_JA from K_AJ * ||L^{-1}J_A|| plus boundary flux", "PPN gamma,beta,alpha_i,xi", "PPN projection, L inverse, boundary/source profile", "MISSING_PPN_PROJECTIONS"),
        ("JAC3691_5_clock_WEP_Gdot", "K_clock_JA,Delta_AB ln mu_obs,partial_t ln mu_obs", "clock/WEP/Gdot response to L^{-1}J_A", "clocks;WEP;ephemeris", "frame/species/source/time projection", "MISSING_CLOCK_WEP_TIME_PROJECTION"),
        ("JAC3691_6_EM", "beta_source_alpha,K_EM_JA", "qbar_A^EM = beta_source_alpha,A*b_alpha + B_A^EM*f_EM + r_A^Hodge*b_Hodge + r_A^opt*b_optical + q_A^rad", "EM;WEP;clock;orbital", "charge/source representation, material sensitivities, EM flux normalization", "MISSING_EM_SOURCE_NORMALIZATION"),
        ("JAC3691_7_R11", "c_JA_operator_vector", "operator-family projection of retained L^{-1}J_A terms", "R11/non-EH operators", "executable operator coefficients and domain norms", "MISSING_EXECUTABLE_OPERATOR_VECTOR"),
    ]
    return [{**base(ts), "acquisition_id": aid, "quantity": quantity, "formula": formula, "arenas": arenas, "minimum_inputs": inputs, "status": status, "claim_allowed": False, "score_ready": False} for aid, quantity, formula, arenas, inputs, status in specs]


def decision_rows(ts: str) -> list[dict[str, object]]:
    specs = [
        ("DEC3691_0_vertical", "VERTICAL_TEST_EXACT_NOT_SIGNED", "Dq[e_A]=0 is the correct test, but q/Omega/boundary parent ownership is missing", "do not claim J_A matter/source zero"),
        ("DEC3691_1_source", "SOURCE_ORTHOGONALITY_CONDITIONAL", "matter/source/EM current zero laws are exact only under quotient/source-current descent", "retain eps_JH_Z_abs, beta_source_alpha and PiM derivative residuals"),
        ("DEC3691_2_coefficients", "COEFFICIENT_ACQUISITION_ROWS_INSTALLED", "if the zero theorem fails, required J_A coefficients are now named by arena", "source K_mu_JA, K_gamma_JA, beta_source_alpha and L inverse profiles"),
        ("DEC3691_3_next", "NEXT_BEST_TARGET", "constraint-first Omega owner is the only route that can truly sign verticality", "run 3692 Omega-owner constraint generator or Dq/J_A coefficient runner"),
        ("DEC3691_4_private", "PRIVATE_NONCLAIM", "no local-GR/Newton/GitHub/public claim", "continue private derivation"),
    ]
    return [{**base(ts), "decision_id": did, "status": status, "decision": decision, "next_action": next_action, "claim_allowed": False, "score_ready": False} for did, status, decision, next_action in specs]


def claim_gate_rows(ts: str) -> list[dict[str, object]]:
    specs = [
        ("CG3691_0_vertical", "claim Dq[e_A]=0", "BLOCKED_Q_OMEGA_BOUNDARY_OWNER", "q, Omega/DCdagger, and boundary charge are not parent-signed"),
        ("CG3691_1_JA_matter_source", "claim J_A^matter=J_A^source=0", "BLOCKED_DESCENT_ORTHOGONALITY", "matter/source/PiM/JH descent is conditional only"),
        ("CG3691_2_JA_total", "claim J_A=0", "BLOCKED_BOUNDARY_SELECTOR_FLUX_ZMAP", "boundary, selector, flux and Z observable map remain open"),
        ("CG3691_3_score", "score PPN/R10/WEP/clock/EM", "BLOCKED_COEFFICIENTS", "arena coefficients and L inverse/source profiles are missing"),
        ("CG3691_4_public", "public/GitHub promotion", "BLOCKED_PRIVATE", "private checkpoint only"),
    ]
    return [{**base(ts), "claim_gate_id": gid, "gate": gate, "status": status, "reason": reason, "claim_allowed": False, "score_ready": False} for gid, gate, status, reason in specs]


def status_rows(ts: str) -> list[dict[str, object]]:
    return [{**base(ts), "status_id": "STATUS3691_0", "status": "VERTICAL_SOURCE_ORTHOGONALITY_CONDITIONAL_NOT_SIGNED_JA_COEFFICIENT_ACQUISITION_ROWS_INSTALLED", "summary": "3691 confirms the exact vertical q-map and matter/source-current zero tests, refuses J_A=0 because parent q/Omega/source/boundary signatures are unsigned, and installs precise J_A coefficient acquisition rows for PPN, Newton/R10, clocks, WEP, EM and R11.", "claim_allowed": False, "score_ready": False}]


def next_rows(ts: str) -> list[dict[str, object]]:
    return [{**base(ts), "next_id": "NEXT3691_0", "target_doc": "3692-Y5-R2FR-Omega-owner-constraint-generator-or-DqJA-coefficient-runner.md", "target_script": "scripts/Y5_R2FR_3692_Omega_owner_constraint_generator_or_DqJA_coefficient_runner.py", "objective": "try the constraint-first route: source or construct parent Omega, q, P, J and boundary charge so e_X=Omega^-1 DCdagger[X] is a proper vertical generator with Dq[e_X]=0; if not, run Dq/J_A coefficient acquisition rows", "success_gate": "proper parent vertical generator closes Dq[e_X]=0 and matter/source components of J_A, or Dq/J_A coefficients remain as explicit nonclaim runner inputs", "claim_allowed": False, "score_ready": False}]


def write_doc(sources, vertical, orthogonality, acquisitions, decisions, claim_gates, status, next_target) -> None:
    lines = [
        "# 3691 - Vertical q-map source-current orthogonality or J_A coefficient acquisition",
        "",
        f"**Status:** {status[0]['status']}",
        "",
        "This checkpoint tests the exact route for killing the matter/source part of the canonical coupling `J_A`. The algebra is clean: if the canonical `Z` directions are truly vertical and matter/source currents descend through the quotient, the corresponding source terms vanish. The current corpus does not yet sign those parent premises, so coefficient acquisition rows remain live.",
        "",
        "## Main result",
        "",
        "`Dq[e_A]=0` is the verticality test.",
        "",
        "`delta_Z S_matter=(delta Sbar_matter/delta q)Dq[e_A]delta Z^A`, so `J_A^matter=0` only after verticality plus matter q-descent.",
        "",
        "`delta_Z S_source=0` only if `Pi_M,J_H,M_eff,G_eff` are q-owned or orthogonal to vertical charges.",
        "",
        "`eps_JH_Z_abs <= C_matter*Dq_Z_norm + eps_theta_marker + eps_direct_Z + eps_source_weight + eps_matter_boundary`.",
        "",
        "## Vertical gates",
    ]
    for row in vertical:
        lines.append(f"- `{row['gate_id']}`: {row['status']} - {row['gate']} -> {row['residual_if_failed']}")
    lines.extend(["", "## Source orthogonality"])
    for row in orthogonality:
        lines.append(f"- `{row['orthogonality_id']}`: {row['status']} - {row['piece']} -> {row['residual_if_failed']}")
    lines.extend(["", "## Coefficient acquisition"])
    for row in acquisitions:
        lines.append(f"- `{row['acquisition_id']}`: {row['status']} - `{row['quantity']}` in {row['arenas']} -> {row['minimum_inputs']}")
    lines.extend(["", "## Decisions"])
    for row in decisions:
        lines.append(f"- `{row['decision_id']}`: {row['status']} - {row['decision']} -> {row['next_action']}")
    lines.extend(["", "## Claim gates"])
    for row in claim_gates:
        lines.append(f"- `{row['claim_gate_id']}`: {row['status']} - {row['gate']} because {row['reason']}")
    lines.extend(["", "## Next target", f"`{next_target[0]['target_doc']}` via `{next_target[0]['target_script']}`.", "", "## Sources"])
    for row in sources:
        lines.append(f"- `{row['source_id']}`: `{row['source_path']}` exists={row['exists']} needle_found={row['needle_found']}")
    DOC.write_text("\n".join(lines) + "\n", encoding="utf-8")


def validate(ts, output_paths, sources, vertical, orthogonality, acquisitions, decisions, claim_gates, status, next_target):
    rows = []

    def add(vid, ok, detail):
        rows.append({"timestamp_utc": ts, "branch_id": BRANCH_ID, "checkpoint_id": CHECKPOINT_ID, "validation_id": vid, "result": "PASS" if ok else "FAIL", "detail": detail})

    csv_status = [parse_csv(path) for path in output_paths if path.suffix.lower() == ".csv"]
    generated = sources + vertical + orthogonality + acquisitions + decisions + claim_gates + status + next_target
    doc_text = read_text(DOC)
    leaks = []
    if FORMALIZATION.exists():
        for pattern in ["*Y5_R2FR_3691*", "3691-Y5-R2FR-*", "P8_Y5*3691*"]:
            leaks.extend(FORMALIZATION.rglob(pattern))
    vertical_by_id = {str(row["gate_id"]): row for row in vertical}
    ortho_by_id = {str(row["orthogonality_id"]): row for row in orthogonality}
    acq_ids = {str(row["acquisition_id"]) for row in acquisitions}

    add("VAL3691_0_sources_exist", all(row["exists"] for row in sources), "every cited source path exists")
    add("VAL3691_1_needles_found", all(row["needle_found"] for row in sources), "every source needle found")
    add("VAL3691_2_outputs_exist", all(path.exists() for path in output_paths), "all expected 3691 outputs written")
    add("VAL3691_3_csv_parse", all(ok and count > 0 for ok, count in csv_status), "all generated CSVs parse with rows")
    add("VAL3691_4_vertical_test", "Dq[e_A]=0" in vertical_by_id["VQ3691_1_generator"]["requirement"], "vertical Dq test recorded")
    add("VAL3691_5_vertical_not_claimed", vertical_by_id["VQ3691_6_verdict"]["status"] == "VERTICAL_Q_MAP_NOT_CLAIMED", "verticality not claimed")
    add("VAL3691_6_matter_source_conditional", ortho_by_id["SO3691_0_matter"]["status"].startswith("CONDITIONAL") and ortho_by_id["SO3691_1_source_current"]["status"].startswith("CONDITIONAL"), "matter/source zero conditional only")
    add("VAL3691_7_coeff_rows", {"JAC3691_0_Dq", "JAC3691_3_Newton", "JAC3691_6_EM", "JAC3691_7_R11"}.issubset(acq_ids), "key coefficient rows present")
    add("VAL3691_8_next_target", next_target[0]["target_doc"].startswith("3692-") and "Omega" in next_target[0]["target_doc"], "3692 targets Omega owner")
    add("VAL3691_9_claim_gates_blocked", all(row["claim_allowed"] is False and row["score_ready"] is False for row in claim_gates), "claim gates remain blocked")
    add("VAL3691_10_all_nonclaim", not any(str(row.get("valid_for_claim", "")).lower() == "true" or str(row.get("claim_allowed", "")).lower() == "true" or str(row.get("score_ready", "")).lower() == "true" for row in generated), "all generated rows remain nonclaim and unscoreable")
    add("VAL3691_11_doc_written", "Dq[e_A]=0" in doc_text and "eps_JH_Z_abs" in doc_text and "Coefficient acquisition" in doc_text, "doc records vertical test and acquisition rows")
    add("VAL3691_12_no_formalization_leak", not leaks, "no 3691 checkpoint files in formalization-workbench")
    return rows


def main() -> int:
    ts = stamp()
    RESIDUALS.mkdir(parents=True, exist_ok=True)
    sources = source_register(ts)
    vertical = vertical_gate_rows(ts)
    orthogonality = source_orthogonality_rows(ts)
    acquisitions = coefficient_acquisition_rows(ts)
    decisions = decision_rows(ts)
    claim_gates = claim_gate_rows(ts)
    status = status_rows(ts)
    next_target = next_rows(ts)
    outputs = {
        "sources": RESIDUALS / "P8_Y5_R2FR_3691_SOURCE_REGISTER.csv",
        "vertical": RESIDUALS / "P8_Y5_R2FR_3691_VERTICAL_QMAP_GATE_ROWS.csv",
        "orthogonality": RESIDUALS / "P8_Y5_R2FR_3691_SOURCE_ORTHOGONALITY_ROWS.csv",
        "acquisitions": RESIDUALS / "P8_Y5_R2FR_3691_JA_COEFFICIENT_ACQUISITION_ROWS.csv",
        "decisions": RESIDUALS / "P8_Y5_R2FR_3691_DECISION_ROWS.csv",
        "claim_gates": RESIDUALS / "P8_Y5_R2FR_3691_CLAIM_GATES.csv",
        "status": RESIDUALS / "P8_Y5_R2FR_3691_STATUS.csv",
        "next": RESIDUALS / "P8_Y5_R2FR_3691_NEXT_TARGET.csv",
        "validation": RESIDUALS / "P8_Y5_BRR545_3691_VALIDATION.csv",
    }
    write_csv(outputs["sources"], sources)
    write_csv(outputs["vertical"], vertical)
    write_csv(outputs["orthogonality"], orthogonality)
    write_csv(outputs["acquisitions"], acquisitions)
    write_csv(outputs["decisions"], decisions)
    write_csv(outputs["claim_gates"], claim_gates)
    write_csv(outputs["status"], status)
    write_csv(outputs["next"], next_target)
    write_doc(sources, vertical, orthogonality, acquisitions, decisions, claim_gates, status, next_target)
    generated_paths = [path for key, path in outputs.items() if key != "validation"] + [DOC]
    validation = validate(ts, generated_paths, sources, vertical, orthogonality, acquisitions, decisions, claim_gates, status, next_target)
    write_csv(outputs["validation"], validation)
    failures = [row for row in validation if row["result"] != "PASS"]
    if failures:
        print(f"3691 validation failed: {failures}", file=sys.stderr)
        return 1
    print("wrote 3691 checkpoint: vertical/source orthogonality conditional; J_A coefficient acquisition rows installed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

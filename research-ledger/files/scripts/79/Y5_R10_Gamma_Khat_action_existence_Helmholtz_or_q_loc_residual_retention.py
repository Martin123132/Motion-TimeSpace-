from __future__ import annotations

import csv
from datetime import datetime, timezone
from pathlib import Path


STARTED = datetime.now(timezone.utc)
ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "source-intake" / "mts_residuals"
DOC = ROOT / "1010-Y5-R10-Gamma-Khat-action-existence-Helmholtz-or-q_loc-residual-retention.md"
FORMALIZATION = ROOT.parent / "formalization-workbench"


def stamp() -> str:
    return datetime.now(timezone.utc).isoformat()


def flag(value: object) -> bool:
    return str(value).strip().lower() == "true"


def missing(value: object) -> bool:
    text = str(value or "").strip()
    return text == "" or text.upper().startswith("MISSING")


def source_path(path_text: str) -> Path:
    path = Path(path_text)
    if path.is_absolute():
        return path
    return ROOT / path


def path_exists(path_text: str) -> bool:
    text = str(path_text or "").strip()
    if missing(text):
        return False
    if text in {"BOOKKEEPING_ONLY", "NOT_REQUIRED_FOR_RESIDUAL", "CANDIDATE_NOT_MATCHED", "PLATEAU_AXIOM"}:
        return False
    return source_path(text).exists()


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


def md_cell(value: object) -> str:
    return str(value).replace("\n", " ").replace("|", "\\|")


def md_table(rows: list[dict[str, object]], columns: list[str]) -> str:
    if not rows:
        return "_No rows._\n"
    return "\n".join(
        [
            "| " + " | ".join(columns) + " |",
            "| " + " | ".join("---" for _ in columns) + " |",
            *["| " + " | ".join(md_cell(row.get(col, "")) for col in columns) + " |" for row in rows],
        ]
    ) + "\n"


def source_register_rows() -> list[dict[str, str]]:
    specs = [
        ("SRC1010_0_1009_next", "source-intake/mts_residuals/P8_Y5_R10_1009_NEXT_TARGET.csv", "Gamma-Khat-action-existence", "1009 handoff target."),
        ("SRC1010_1_1009_contract", "source-intake/mts_residuals/P8_Y5_R10_1009_PARENT_SECTOR_CONTRACT.csv", "PCS1009_4_Gamma_Khat_extra", "1009 identifies Gamma/Khat as hard fail."),
        ("SRC1010_2_1009_claim_gate", "source-intake/mts_residuals/P8_Y5_R10_1009_CLAIM_GATE.csv", "CG1009_3_GK_q_loc_zero", "prior gate keeps q_loc zero blocked."),
        ("SRC1010_3_GK_contract", "source-intake/mts_residuals/P8_GAMMA_KHAT_QLOC_FIRST_VARIATION_CONTRACT.csv", "GK513_0_action_existence", "first variation contract."),
        ("SRC1010_4_GK_source_register", "source-intake/mts_residuals/P8_GAMMA_KHAT_QLOC_SOURCE_REGISTER.csv", "Gamma-Khat-q_loc first-variation target", "prior source register."),
        ("SRC1010_5_GK_candidates", "source-intake/mts_residuals/P8_GK_STRESS_ACTION_CANDIDATES.csv", "GK514_A_metric_response_scalar_density", "candidate S_GK action routes."),
        ("SRC1010_6_GK_gate_tests", "source-intake/mts_residuals/P8_GK_STRESS_ACTION_GATE_TESTS.csv", "G514_2_current_MTS_match", "current match failure gate."),
        ("SRC1010_7_GK_decision", "source-intake/mts_residuals/P8_GK_STRESS_ACTION_DECISION.csv", "D514_1", "prior decision: current MTS not matched."),
        ("SRC1010_8_Gamma_owner", "source-intake/mts_residuals/P8_GAMMA_OWNER_CANDIDATE_ACTION.csv", "GO516_A_response_doublet_quadratic_density", "Gamma owner candidate action routes."),
        ("SRC1010_9_metric_response_evidence", "source-intake/mts_residuals/P8_GK_METRIC_RESPONSE_SOURCE_EVIDENCE.csv", "E515_4_source_current_audit", "metric response clue and limitations."),
        ("SRC1010_10_symbol_gate", "source-intake/mts_residuals/P8_MTS_SYMBOL_FIRST_VARIATION_GATES.csv", "FV512_2_Gamma_Khat_q", "symbol first-variation gate."),
        ("SRC1010_11_symbol_map", "source-intake/mts_residuals/P8_MTS_SYMBOL_TO_LOCAL_GR_ACTION_MAP.csv", "q_loc^nu", "q_loc is derived residual, not fundamental field."),
        ("SRC1010_12_Noether_audit", "source-intake/mts_residuals/P8_YLOC_SOURCE_CURRENT_NOETHER_AUDIT.csv", "N5_verdict", "Noether alone does not prove zero."),
        ("SRC1010_13_response_doublet", "source-intake/mts_residuals/P8_RESPONSE_DOUBLET_ACTION_CONTRACT.csv", "RD516_2_metric_response", "response doublet contract."),
        ("SRC1010_14_response_variation", "source-intake/mts_residuals/P8_RESPONSE_DOUBLET_ACTION_VARIATION.csv", "AV517_4_Euler_equation", "response doublet variation obstruction."),
        ("SRC1010_15_local_residual_vector", "source-intake/mts_residuals/P8_LOCAL_GR_RESIDUAL_VECTOR_FROM_DOMAIN_SOURCE.csv", "LRV_TOTAL_ALPHA3_GUARD", "residual retention observable map."),
    ]
    rows = []
    for source_id, path_text, needle, role in specs:
        path = source_path(path_text)
        text = path.read_text(encoding="utf-8", errors="replace") if path.exists() else ""
        rows.append(
            {
                "source_id": source_id,
                "source_path": path_text,
                "exists": str(path.exists()).lower(),
                "needle": needle,
                "needle_found": str(needle in text).lower(),
                "role": role,
                "generated_utc": stamp(),
            }
        )
    return rows


def theorem_attempt_rows() -> list[dict[str, str]]:
    rows = [
        {
            "theorem_id": "GKT1010_0_variational_route",
            "claim_piece": "metric-response action route",
            "mathematical_form": "S_GK = - integral sqrt(-g) Gamma_eff(g,Phi,nabla Phi,D,...)",
            "what_would_follow": "K_hat is the metric response of Gamma_eff and q_loc becomes a Ward/Euler residual",
            "current_evidence": "GK514_A is best candidate, but G514_2 says current MTS match fails.",
            "status": "candidate_contract_not_claim",
            "valid_for_claim": "false",
        },
        {
            "theorem_id": "GKT1010_1_metric_response_identity",
            "claim_piece": "K_hat^{mu nu} = K_metric^{mu nu}",
            "mathematical_form": "K_metric^{mu nu}:=2/sqrt(-g) delta[sqrt(-g) Gamma_eff]/delta g_{mu nu} minus volume/sign convention",
            "what_would_follow": "nabla_mu(Gamma_eff g^{mu nu}-K_hat^{mu nu}) is the variational stress divergence",
            "current_evidence": "P8_GK_METRIC_RESPONSE_SOURCE_EVIDENCE calls this a required gate, not a match.",
            "status": "not_matched_to_current_symbols",
            "valid_for_claim": "false",
        },
        {
            "theorem_id": "GKT1010_2_Helmholtz_integrability",
            "claim_piece": "stress tensor is variational",
            "mathematical_form": "delta(sqrt(-g)T_GK^{mu nu})/delta g_{alpha beta} is symmetric under exchange of metric variations up to boundary terms",
            "what_would_follow": "there exists an S_GK whose metric variation gives the proposed stress",
            "current_evidence": "GK513_1 says not_checked; no second-variation symmetry calculation exists.",
            "status": "not_checked_current_claim",
            "valid_for_claim": "false",
        },
        {
            "theorem_id": "GKT1010_3_Euler_closure",
            "claim_piece": "q_loc vanishes on local compact vacuum equations",
            "mathematical_form": "nabla_mu T_GK^{mu nu}=sum_A E_A nabla^nu Phi^A + boundary; E_A=0 and boundary=0 imply q_loc^nu=0",
            "what_would_follow": "local force residual is derived zero rather than plateau-axiom zero",
            "current_evidence": "GK513_2 not_derived; response-doublet Euler equation blocked by source-current rows.",
            "status": "not_derived",
            "valid_for_claim": "false",
        },
        {
            "theorem_id": "GKT1010_4_double_zero",
            "claim_piece": "local fixed point has zero amplitude and zero first variation",
            "mathematical_form": "T_GK(Phi0)=0 and partial_A T_GK(Phi0)=0, equivalently Gamma0 subtracted and K_hat response matched",
            "what_would_follow": "PPN/source-normalization hair starts only at bounded second order",
            "current_evidence": "GK513_3 not_matched; response-doublet double-zero is conditional but not MTS promotion.",
            "status": "not_matched",
            "valid_for_claim": "false",
        },
        {
            "theorem_id": "GKT1010_5_projector_boundary",
            "claim_piece": "P_loc and boundary/symplectic no-flux are parent-owned",
            "mathematical_form": "P_loc=P_parent(Phi0), partial_A P_loc(Phi0)=0, integral_boundary Delta(theta_GK,Q_GK,tau)=0",
            "what_would_follow": "projection and boundary cannot hide/tune force components",
            "current_evidence": "GK513_4 and GK513_5 remain open.",
            "status": "open",
            "valid_for_claim": "false",
        },
        {
            "theorem_id": "GKT1010_6_verdict",
            "claim_piece": "derive q_loc^nu=0 from S_GK",
            "mathematical_form": "all GKT1010_0 through GKT1010_5 pass with source/equation paths and parent signatures",
            "what_would_follow": "local PPN branch can reopen at the residual-vector gate",
            "current_evidence": "route is precise but current corpus lacks match, Helmholtz check, Euler closure, double-zero, projector, and boundary certificates.",
            "status": "fail_current_claim",
            "valid_for_claim": "false",
        },
    ]
    for row in rows:
        row["generated_utc"] = stamp()
    return rows


def Helmholtz_schema_rows() -> list[dict[str, str]]:
    rows = [
        {
            "schema_id": "HGS1010_0_candidate_action",
            "target": "S_GK",
            "required_fields": "action_source; scalar_density; field_content; boundary_terms; variation_variables; sign_convention",
            "pass_condition": "S_GK is explicit and diffeomorphism-invariant on local compact branch",
            "valid_for_claim": "false",
        },
        {
            "schema_id": "HGS1010_1_metric_response",
            "target": "K_hat",
            "required_fields": "K_metric_formula; Gamma_eff_formula; volume_convention; derivative_term_accounting; source_path",
            "pass_condition": "existing K_hat equals metric response of sqrt(-g) Gamma_eff, including derivative/boundary terms",
            "valid_for_claim": "false",
        },
        {
            "schema_id": "HGS1010_2_Helmholtz",
            "target": "variational stress",
            "required_fields": "second_variation_symmetry; boundary_symmetry; variable_domain; gauge_constraints",
            "pass_condition": "stress satisfies Helmholtz integrability, not merely Ward bookkeeping",
            "valid_for_claim": "false",
        },
        {
            "schema_id": "HGS1010_3_Euler_double_zero",
            "target": "q_loc zero",
            "required_fields": "Euler_equations; local_fixed_point; source_zero; boundary_zero; T_zero; dT_zero",
            "pass_condition": "q_loc^nu vanishes on shell and first variation vanishes at local fixed point",
            "valid_for_claim": "false",
        },
        {
            "schema_id": "HGS1010_4_residual_retention",
            "target": "q_loc residual",
            "required_fields": "q_loc_profile; units; normalization; observable_map; bound_or_gate; source_path; valid_for_claim",
            "pass_condition": "if derivation fails, q_loc is retained as explicit local residual instead of claimed zero",
            "valid_for_claim": "false",
        },
    ]
    for row in rows:
        row["generated_utc"] = stamp()
    return rows


def candidate_rows() -> list[dict[str, str]]:
    base = {
        "target": "Gamma_Khat_q_loc_action_existence",
        "action_source": "MISSING_ACTION_SOURCE",
        "Gamma_formula_source": "MISSING_GAMMA_FORMULA_SOURCE",
        "Khat_formula_source": "MISSING_KHAT_FORMULA_SOURCE",
        "metric_response_certificate": "MISSING_METRIC_RESPONSE_CERTIFICATE",
        "Helmholtz_certificate": "MISSING_HELMHOLTZ_CERTIFICATE",
        "Euler_closure_certificate": "MISSING_EULER_CLOSURE_CERTIFICATE",
        "double_zero_certificate": "MISSING_DOUBLE_ZERO_CERTIFICATE",
        "P_loc_certificate": "MISSING_P_LOC_CERTIFICATE",
        "boundary_no_flux_certificate": "MISSING_BOUNDARY_NO_FLUX_CERTIFICATE",
        "source_current_zero_certificate": "MISSING_SOURCE_CURRENT_ZERO_CERTIFICATE",
        "q_loc_profile_source": "MISSING_Q_LOC_PROFILE_SOURCE",
        "observable_map_source": "MISSING_OBSERVABLE_MAP_SOURCE",
        "residual_policy": "MISSING_RESIDUAL_POLICY",
        "claim_type": "derivation",
        "valid_for_claim": "false",
    }
    rows: list[dict[str, str]] = []

    def add(candidate_id: str, candidate: str, **updates: str) -> None:
        row = dict(base)
        row.update({"candidate_id": candidate_id, "candidate": candidate, "generated_utc": stamp()})
        row.update(updates)
        rows.append(row)

    add(
        "GKC1010_0_metric_response_scalar_density",
        "S_GK=-int sqrt(-g) Gamma_eff with K_hat as metric response",
        action_source="source-intake/mts_residuals/P8_GK_STRESS_ACTION_CANDIDATES.csv",
        Gamma_formula_source="source-intake/mts_residuals/P8_GK_STRESS_ACTION_CANDIDATES.csv",
        Khat_formula_source="source-intake/mts_residuals/P8_GK_METRIC_RESPONSE_SOURCE_EVIDENCE.csv",
        observable_map_source="source-intake/mts_residuals/P8_LOCAL_GR_RESIDUAL_VECTOR_FROM_DOMAIN_SOURCE.csv",
        residual_policy="DERIVE_OR_RETAIN",
    )
    add(
        "GKC1010_1_response_doublet_even_density",
        "exchange-response doublet makes Gamma_eff even and locally double-zero",
        action_source="source-intake/mts_residuals/P8_GAMMA_OWNER_CANDIDATE_ACTION.csv",
        Gamma_formula_source="source-intake/mts_residuals/P8_RESPONSE_DOUBLET_ACTION_VARIATION.csv",
        Khat_formula_source="source-intake/mts_residuals/P8_RESPONSE_DOUBLET_ACTION_CONTRACT.csv",
        observable_map_source="source-intake/mts_residuals/P8_LOCAL_GR_RESIDUAL_VECTOR_FROM_DOMAIN_SOURCE.csv",
        residual_policy="DERIVE_OR_RETAIN",
    )
    add(
        "GKC1010_2_positive_auxiliary_fields",
        "positive auxiliary operator forces Phi=Phi0 on compact source-free collars",
        action_source="source-intake/mts_residuals/P8_GK_STRESS_ACTION_CANDIDATES.csv",
        Gamma_formula_source="source-intake/mts_residuals/P8_GAMMA_OWNER_CANDIDATE_ACTION.csv",
        Khat_formula_source="source-intake/mts_residuals/P8_GK_STRESS_ACTION_CANDIDATES.csv",
        observable_map_source="source-intake/mts_residuals/P8_LOCAL_GR_RESIDUAL_VECTOR_FROM_DOMAIN_SOURCE.csv",
        residual_policy="DERIVE_OR_RETAIN",
    )
    add(
        "GKC1010_3_topological_exact_sector",
        "Gamma/Khat contribution is exact/topological and bulk force-free",
        action_source="source-intake/mts_residuals/P8_GK_STRESS_ACTION_CANDIDATES.csv",
        Gamma_formula_source="source-intake/mts_residuals/P8_GAMMA_OWNER_CANDIDATE_ACTION.csv",
        Khat_formula_source="source-intake/mts_residuals/P8_GK_STRESS_ACTION_CANDIDATES.csv",
        boundary_no_flux_certificate="MISSING_TOPOLOGICAL_BOUNDARY_NO_FLUX_CERTIFICATE",
        residual_policy="DERIVE_OR_RETAIN",
    )
    add(
        "GKC1010_4_plateau_axiom_attempt",
        "q_loc is set to zero by local plateau assumption",
        action_source="PLATEAU_AXIOM",
        residual_policy="FORBIDDEN_PLATEAU_AXIOM",
    )
    add(
        "GKC1010_5_bookkeeping_stress_attempt",
        "Gamma_eff and K_hat are treated as stress pieces without variational action",
        action_source="BOOKKEEPING_ONLY",
        residual_policy="FORBIDDEN_BOOKKEEPING_STRESS",
    )
    add(
        "GKC1010_6_residual_retention",
        "q_loc retained as explicit residual profile for local tests",
        action_source="NOT_REQUIRED_FOR_RESIDUAL",
        q_loc_profile_source="source-intake/mts_residuals/P8_LOCAL_GR_RESIDUAL_VECTOR_FROM_DOMAIN_SOURCE.csv",
        observable_map_source="source-intake/mts_residuals/P8_LOCAL_GR_RESIDUAL_VECTOR_FROM_DOMAIN_SOURCE.csv",
        residual_policy="RETAIN_Q_LOC_AS_EXPLICIT_RESIDUAL",
        claim_type="residual_retention",
    )
    return rows


def evaluate_candidate(row: dict[str, str]) -> dict[str, str]:
    reasons: list[str] = []
    if row["claim_type"] == "derivation":
        for field in ["action_source", "Gamma_formula_source", "Khat_formula_source", "observable_map_source"]:
            if not path_exists(row.get(field, "")):
                reasons.append(f"MISSING_EXISTING_{field.upper()}")
        for field in [
            "metric_response_certificate",
            "Helmholtz_certificate",
            "Euler_closure_certificate",
            "double_zero_certificate",
            "P_loc_certificate",
            "boundary_no_flux_certificate",
            "source_current_zero_certificate",
        ]:
            if not str(row.get(field, "")).startswith("PARENT_SIGNED_"):
                reasons.append(f"MISSING_PARENT_SIGNED_{field.upper()}")
        if row["candidate_id"] == "GKC1010_4_plateau_axiom_attempt":
            reasons.append("PLATEAU_AXIOM_REJECTED")
        if row["candidate_id"] == "GKC1010_5_bookkeeping_stress_attempt":
            reasons.append("BOOKKEEPING_STRESS_REJECTED")
        if not flag(row.get("valid_for_claim")):
            reasons.append("VALID_FOR_CLAIM_FALSE")
        verdict = "PASS_DERIVED_Q_LOC_ZERO" if not reasons else "REFUSED_DERIVED_Q_LOC_ZERO"
        claim_allowed = not reasons and flag(row.get("valid_for_claim"))
        score_ready = not reasons
    else:
        for field in ["q_loc_profile_source", "observable_map_source"]:
            if not path_exists(row.get(field, "")):
                reasons.append(f"MISSING_EXISTING_{field.upper()}")
        if row.get("residual_policy") != "RETAIN_Q_LOC_AS_EXPLICIT_RESIDUAL":
            reasons.append("MISSING_EXPLICIT_RESIDUAL_RETENTION_POLICY")
        if not flag(row.get("valid_for_claim")):
            reasons.append("VALID_FOR_CLAIM_FALSE")
        retained = "VALID_FOR_CLAIM_FALSE" in reasons and len([r for r in reasons if r != "VALID_FOR_CLAIM_FALSE"]) == 0
        verdict = "RETAINED_NONCLAIM_Q_LOC_RESIDUAL" if retained else "REFUSED_RESIDUAL_ROW"
        claim_allowed = False
        score_ready = retained
    return {
        "runner_id": row["candidate_id"].replace("GKC", "GKR"),
        "candidate_id": row["candidate_id"],
        "claim_type": row["claim_type"],
        "verdict": verdict,
        "score_ready": str(score_ready).lower(),
        "q_loc_zero_derived": str(verdict == "PASS_DERIVED_Q_LOC_ZERO").lower(),
        "residual_retained": str(verdict == "RETAINED_NONCLAIM_Q_LOC_RESIDUAL").lower(),
        "claim_allowed": str(claim_allowed).lower(),
        "valid_for_claim": str(claim_allowed).lower(),
        "failure_reasons": ";".join(reasons),
        "generated_utc": stamp(),
    }


def runner_rows(candidates: list[dict[str, str]]) -> list[dict[str, str]]:
    return [evaluate_candidate(row) for row in candidates]


def residual_retention_rows() -> list[dict[str, str]]:
    rows = [
        {
            "residual_id": "QRES1010_0_q_loc_vector",
            "residual_symbol": "q_loc^nu",
            "definition": "P_loc(nabla^nu Gamma_eff - nabla_mu K_hat^{mu nu})",
            "status": "retained_until_S_GK_proved",
            "observable_map": "PPN alpha_i/xi, source-normalization R11, local force/fifth-force, clock/orbital residuals",
            "required_to_claim_zero": "PARENT_SIGNED_S_GK_METRIC_RESPONSE_HELMHOLTZ_EULER_DOUBLE_ZERO_BOUNDARY_TRUE",
            "valid_for_claim": "false",
        },
        {
            "residual_id": "QRES1010_1_Gamma_metric_response_gap",
            "residual_symbol": "Delta_K",
            "definition": "K_hat - K_metric[Gamma_eff]",
            "status": "retained_symbolic_gap",
            "observable_map": "if nonzero, enters q_loc and PPN/source-normalization rows",
            "required_to_claim_zero": "explicit metric-response match including derivative/boundary terms",
            "valid_for_claim": "false",
        },
        {
            "residual_id": "QRES1010_2_Helmholtz_gap",
            "residual_symbol": "H_GK",
            "definition": "antisymmetric second-variation obstruction for proposed T_GK",
            "status": "retained_symbolic_gap",
            "observable_map": "if nonzero, no action exists for the claimed stress",
            "required_to_claim_zero": "Helmholtz symmetry calculation",
            "valid_for_claim": "false",
        },
        {
            "residual_id": "QRES1010_3_source_boundary_gap",
            "residual_symbol": "J_GK + B_GK",
            "definition": "source-current and boundary work in response doublet/Euler identity",
            "status": "retained_symbolic_gap",
            "observable_map": "PPN preferred-frame/source hair and local boundary flux",
            "required_to_claim_zero": "zero source-current and no-flux theorem",
            "valid_for_claim": "false",
        },
    ]
    for row in rows:
        row["generated_utc"] = stamp()
    return rows


def claim_gate_rows(theorem: list[dict[str, str]], runner: list[dict[str, str]]) -> list[dict[str, str]]:
    derivations_refused = all(row["verdict"] != "PASS_DERIVED_Q_LOC_ZERO" for row in runner)
    residual_retained = any(row["verdict"] == "RETAINED_NONCLAIM_Q_LOC_RESIDUAL" for row in runner)
    theorem_failed = any(row["theorem_id"] == "GKT1010_6_verdict" and row["status"] == "fail_current_claim" for row in theorem)
    gates = [
        ("CG1010_0_S_GK_action", "S_GK exists as accepted MTS parent sector", "false", "candidate routes are contracts but not matched to current symbols"),
        ("CG1010_1_metric_response", "K_hat is the metric response of Gamma_eff", "false", "metric-response identity is not matched including derivative/boundary terms"),
        ("CG1010_2_Helmholtz", "T_GK satisfies Helmholtz integrability", "false", "second variation symmetry is not checked"),
        ("CG1010_3_Euler_double_zero", "q_loc vanishes by Euler closure and double-zero", "false", "source-current, boundary, and local fixed-point certificates are missing"),
        ("CG1010_4_plateau_guard", "local plateau axiom may set q_loc=0", "false", "plateau axiom is rejected"),
        ("CG1010_5_Htau_MHref_local_GR", "H_tau/M_H_ref/local-GR gates can reopen", "false", "q_loc remains retained residual"),
        ("CG1010_6_residual_retention", "q_loc residual is retained rather than hidden", str(residual_retained).lower(), "explicit nonclaim residual row is installed"),
        ("CG1010_7_guardrail", "Gamma/Khat action-existence guardrail is installed", str(derivations_refused and residual_retained and theorem_failed).lower(), "derivation shortcuts are refused and q_loc is retained"),
    ]
    return [
        {
            "gate_id": gate_id,
            "claim": claim,
            "gate_pass": gate_pass,
            "reason": reason,
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        }
        for gate_id, claim, gate_pass, reason in gates
    ]


def decision_rows() -> list[dict[str, str]]:
    rows = [
        {
            "decision_id": "DEC1010_0_derivation_route_precise",
            "decision": "The derivation route is precise: S_GK plus metric-response K_hat plus Helmholtz plus Euler/double-zero would derive q_loc=0.",
            "because": "Ward identity then turns q_loc into an on-shell variational residual rather than an axiom.",
            "next_action": "try the response-doublet source-current zero theorem, because it is the most concrete route to Gamma double-zero",
            "valid_for_claim": "false",
        },
        {
            "decision_id": "DEC1010_1_not_currently_proved",
            "decision": "Current MTS corpus does not yet prove the route.",
            "because": "metric-response match, Helmholtz symmetry, source-current zero, P_loc ownership, and boundary no-flux are missing.",
            "next_action": "do not reopen H_tau/M_H_ref/local-GR until these are sourced or residual-bounded",
            "valid_for_claim": "false",
        },
        {
            "decision_id": "DEC1010_2_residual_kept_honest",
            "decision": "q_loc is retained as an explicit residual instead of being hidden.",
            "because": "this keeps PPN/source-normalization testing honest if derivation fails.",
            "next_action": "either prove response-doublet zero-source/boundary theorem or fill q_loc observable coefficients",
            "valid_for_claim": "false",
        },
    ]
    for row in rows:
        row["generated_utc"] = stamp()
    return rows


def next_target_rows() -> list[dict[str, str]]:
    return [
        {
            "next_target": "1011-Y5-R10-response-doublet-source-current-zero-or-q_loc-bound-fill.md",
            "objective": "try to prove the response-doublet source-current and boundary terms vanish for the local compact branch; if not, produce q_loc residual bound-fill rows",
            "include": "R_+^A, R_-^A, Z^A, exchange symmetry, Gamma_eff even density, L_AB positive operator, J_Z=0, B_Z=0, PPN/source-normalization map, q_loc units and bounds",
            "exclude": "plateau axiom, bookkeeping stress, fitted cancellation, H_tau pass, M_H_ref pass, local-GR claim, GitHub action",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        }
    ]


def formalization_changed_after_start() -> list[Path]:
    if not FORMALIZATION.exists():
        return []
    changed = []
    for path in FORMALIZATION.rglob("*"):
        if path.is_file() and datetime.fromtimestamp(path.stat().st_mtime, timezone.utc) >= STARTED:
            changed.append(path)
    return changed


def validation_rows(
    sources: list[dict[str, str]],
    theorem: list[dict[str, str]],
    schema: list[dict[str, str]],
    candidates: list[dict[str, str]],
    runner: list[dict[str, str]],
    residuals: list[dict[str, str]],
    claims: list[dict[str, str]],
    decisions: list[dict[str, str]],
    next_target: list[dict[str, str]],
) -> list[dict[str, str]]:
    changed = formalization_changed_after_start()
    derivation_rows = [row for row in runner if row["claim_type"] == "derivation"]
    validations = [
        ("V1010_0_sources_exist", all(flag(row["exists"]) and flag(row["needle_found"]) for row in sources), "all source paths exist and needles are present"),
        ("V1010_1_theorem_blocks_claim", any(row["theorem_id"] == "GKT1010_6_verdict" and row["status"] == "fail_current_claim" for row in theorem) and all(not flag(row["valid_for_claim"]) for row in theorem), "theorem attempt keeps q_loc zero nonclaim"),
        ("V1010_2_schema_ready", {"HGS1010_0_candidate_action", "HGS1010_1_metric_response", "HGS1010_2_Helmholtz", "HGS1010_4_residual_retention"}.issubset({row["schema_id"] for row in schema}), "action, metric-response, Helmholtz, and residual schemas are present"),
        ("V1010_3_candidates_nonclaim", len(candidates) >= 7 and all(not flag(row["valid_for_claim"]) for row in candidates), "candidate rows remain nonclaim"),
        ("V1010_4_derivation_shortcuts_refused", len(derivation_rows) >= 6 and all(row["verdict"] == "REFUSED_DERIVED_Q_LOC_ZERO" for row in derivation_rows), "every q_loc zero derivation shortcut is refused"),
        ("V1010_5_residual_retained", any(row["verdict"] == "RETAINED_NONCLAIM_Q_LOC_RESIDUAL" and flag(row["residual_retained"]) for row in runner), "q_loc residual retention row is active and nonclaim"),
        ("V1010_6_plateau_guard", any(row["candidate_id"] == "GKC1010_4_plateau_axiom_attempt" and "PLATEAU_AXIOM_REJECTED" in row["failure_reasons"] for row in runner), "plateau axiom is refused"),
        ("V1010_7_bookkeeping_guard", any(row["candidate_id"] == "GKC1010_5_bookkeeping_stress_attempt" and "BOOKKEEPING_STRESS_REJECTED" in row["failure_reasons"] for row in runner), "bookkeeping stress is refused"),
        ("V1010_8_residual_ledger_written", len(residuals) >= 4 and all(not flag(row["valid_for_claim"]) for row in residuals), "residual ledger maps retained q_loc gaps"),
        ("V1010_9_claim_gates_blocked", all(not flag(row["claim_allowed"]) and not flag(row["valid_for_claim"]) for row in claims), "S_GK, q_loc zero, H_tau, M_H_ref, and local-GR claims stay blocked"),
        ("V1010_10_guardrail_written", any(row["gate_id"] == "CG1010_7_guardrail" and flag(row["gate_pass"]) for row in claims), "Gamma/Khat action-existence guardrail is installed"),
        ("V1010_11_decision_written", any(row["decision_id"] == "DEC1010_0_derivation_route_precise" for row in decisions), "derivation route and residual fallback decisions are written"),
        ("V1010_12_next_target_written", len(next_target) == 1 and "1011-Y5-R10-response-doublet-source-current-zero" in next_target[0]["next_target"], "1011 target row is present and nonclaim"),
        ("V1010_13_formalization_untouched", len(changed) == 0, f"formalization-workbench modified-file count since script start is {len(changed)}"),
    ]
    rows = [{"check_id": cid, "result": "pass" if passed else "fail", "detail": detail, "generated_utc": stamp()} for cid, passed, detail in validations]
    rows.insert(0, {"check_id": "V1010_SUMMARY", "result": "pass" if all(row["result"] == "pass" for row in rows) else "fail", "detail": "1010 Gamma/Khat action-existence validation summary", "generated_utc": stamp()})
    return rows


def write_doc(
    sources: list[dict[str, str]],
    theorem: list[dict[str, str]],
    schema: list[dict[str, str]],
    candidates: list[dict[str, str]],
    runner: list[dict[str, str]],
    residuals: list[dict[str, str]],
    claims: list[dict[str, str]],
    decisions: list[dict[str, str]],
    next_target: list[dict[str, str]],
    validations: list[dict[str, str]],
) -> None:
    text = "\n".join(
        [
            "# 1010 Y5 R10 Gamma/Khat action existence, Helmholtz, or q_loc residual retention",
            "",
            "**Status:** the exact derivation route for `q_loc^nu -> 0` is now written, but not closed. `q_loc` is retained as an explicit nonclaim residual until `S_GK`, metric response, Helmholtz, Euler/double-zero, projector, and boundary clauses are signed.",
            "",
            "**Claim ceiling:** no `q_loc=0`, local PPN/local-GR, `H_tau`, `M_H_ref`, `RC994_0`, or `FB554_0` claim is allowed from 1010.",
            "",
            "## Source register",
            md_table(sources, ["source_id", "source_path", "exists", "needle_found", "role"]),
            "## Theorem attempt",
            md_table(theorem, ["theorem_id", "claim_piece", "mathematical_form", "what_would_follow", "status", "valid_for_claim"]),
            "## Helmholtz/action schema",
            md_table(schema, ["schema_id", "target", "required_fields", "pass_condition", "valid_for_claim"]),
            "## Candidate rows",
            md_table(candidates, ["candidate_id", "candidate", "claim_type", "action_source", "Gamma_formula_source", "Khat_formula_source", "residual_policy", "valid_for_claim"]),
            "## Runner",
            md_table(runner, ["runner_id", "candidate_id", "claim_type", "verdict", "score_ready", "q_loc_zero_derived", "residual_retained", "failure_reasons"]),
            "## Residual retention ledger",
            md_table(residuals, ["residual_id", "residual_symbol", "definition", "status", "observable_map", "required_to_claim_zero", "valid_for_claim"]),
            "## Claim gate",
            md_table(claims, ["gate_id", "claim", "gate_pass", "reason", "claim_allowed", "valid_for_claim"]),
            "## Decision ledger",
            md_table(decisions, ["decision_id", "decision", "because", "next_action", "valid_for_claim"]),
            "## Validation",
            md_table(validations, ["check_id", "result", "detail", "generated_utc"]),
            "## Next target",
            md_table(next_target, ["next_target", "objective", "include", "exclude", "valid_for_claim"]),
            "",
        ]
    )
    DOC.write_text(text, encoding="utf-8")


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    sources = source_register_rows()
    theorem = theorem_attempt_rows()
    schema = Helmholtz_schema_rows()
    candidates = candidate_rows()
    runner = runner_rows(candidates)
    residuals = residual_retention_rows()
    claims = claim_gate_rows(theorem, runner)
    decisions = decision_rows()
    next_target = next_target_rows()
    validations = validation_rows(sources, theorem, schema, candidates, runner, residuals, claims, decisions, next_target)

    write_csv(OUT / "P8_Y5_R10_1010_SOURCE_REGISTER.csv", sources)
    write_csv(OUT / "P8_Y5_R10_1010_THEOREM_ATTEMPT.csv", theorem)
    write_csv(OUT / "P8_Y5_R10_1010_HELMHOLTZ_ACTION_SCHEMA.csv", schema)
    write_csv(OUT / "P8_Y5_R10_1010_CANDIDATE_ROWS.csv", candidates)
    write_csv(OUT / "P8_Y5_R10_1010_RUNNER.csv", runner)
    write_csv(OUT / "P8_Y5_R10_1010_RESIDUAL_RETENTION_LEDGER.csv", residuals)
    write_csv(OUT / "P8_Y5_R10_1010_CLAIM_GATE.csv", claims)
    write_csv(OUT / "P8_Y5_R10_1010_DECISION_LEDGER.csv", decisions)
    write_csv(OUT / "P8_Y5_R10_1010_NEXT_TARGET.csv", next_target)
    write_csv(OUT / "P8_Y5_BRR545_1010_VALIDATION.csv", validations)
    write_doc(sources, theorem, schema, candidates, runner, residuals, claims, decisions, next_target, validations)


if __name__ == "__main__":
    main()

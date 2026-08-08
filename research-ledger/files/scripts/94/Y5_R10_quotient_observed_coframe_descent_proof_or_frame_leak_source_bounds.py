from __future__ import annotations

import csv
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "source-intake" / "mts_residuals"
DOC = ROOT / "944-Y5-R10-quotient-observed-coframe-descent-proof-or-frame-leak-source-bounds.md"
FORMALIZATION = ROOT.parent / "formalization-workbench"
SCRIPT_START_UTC = datetime.now(timezone.utc)


def stamp() -> str:
    return datetime.now(timezone.utc).isoformat()


def flag(value: bool) -> str:
    return "true" if value else "false"


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, object]], fieldnames: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()
        for row in rows:
            writer.writerow({field: row.get(field, "") for field in fieldnames})


def md_cell(value: object) -> str:
    return str(value).replace("\n", " ").replace("|", "\\|")


def md_table(rows: list[dict[str, object]], fields: list[str]) -> str:
    if not rows:
        return "_No rows._"
    header = "| " + " | ".join(fields) + " |"
    separator = "| " + " | ".join("---" for _field in fields) + " |"
    body = []
    for row in rows:
        body.append("| " + " | ".join(md_cell(row.get(field, "")) for field in fields) + " |")
    return "\n".join([header, separator, *body])


def source_register() -> list[dict[str, str]]:
    specs = [
        {
            "source_id": "943_doc",
            "path": "943-Y5-R10-single-observed-coframe-matter-coupling-contract-or-frame-residual-source-pack.md",
            "role": "handoff selecting quotient observed-coframe descent",
            "needle": "quotient descent",
        },
        {
            "source_id": "943_validation",
            "path": "source-intake/mts_residuals/P8_Y5_BRR545_943_VALIDATION.csv",
            "role": "previous checkpoint validation",
            "needle": "V943_12_validation_rows_ready",
        },
        {
            "source_id": "943_next_target",
            "path": "source-intake/mts_residuals/P8_Y5_R10_943_NEXT_TARGET.csv",
            "role": "944 target contract",
            "needle": "944-Y5-R10-quotient-observed-coframe-descent-proof-or-frame-leak-source-bounds.md",
        },
        {
            "source_id": "410_functor_attempt",
            "path": "410-quotient-matter-functor-theorem-attempt.md",
            "role": "older quotient-matter functor theorem and counterexamples",
            "needle": "Conditional Functor Theorem",
        },
        {
            "source_id": "626_descent_signature",
            "path": "626-Y5-R10-quotient-invariant-matter-action-signature-or-cg-bound-input.md",
            "role": "quotient-invariant matter action signature and c_g bound schema",
            "needle": "Descent Criterion",
        },
        {
            "source_id": "OCF623_theorem",
            "path": "source-intake/mts_residuals/P8_Y5_R10_623_COFRAME_FUNCTOR_THEOREM_ATTEMPT.csv",
            "role": "conditional coframe factorization lemma",
            "needle": "OCF623_0_factorization_lemma",
        },
        {
            "source_id": "PMC622_contract",
            "path": "source-intake/mts_residuals/P8_Y5_R10_622_PARENT_MATTER_CONTRACT.csv",
            "role": "parent matter functor contract",
            "needle": "PMC622_2_unique_observed_geometry",
        },
        {
            "source_id": "QDA711_audit",
            "path": "source-intake/mts_residuals/P8_Y5_R10_711_QUOTIENT_DESCENT_DERIVATION_AUDIT.csv",
            "role": "quotient descent derivation audit",
            "needle": "QDA711_9_verdict",
        },
        {
            "source_id": "CDT778_gate",
            "path": "source-intake/mts_residuals/P8_Y5_R10_778_COUPLING_DESCENT_THEOREM_GATE.csv",
            "role": "coupling descent theorem gate",
            "needle": "CDT778_7_theorem_result",
        },
        {
            "source_id": "SIG779_audit",
            "path": "source-intake/mts_residuals/P8_Y5_R10_779_PARENT_COUPLING_SIGNATURE_AUDIT.csv",
            "role": "parent coupling signature audit",
            "needle": "SIG779_0_coupling_descent",
        },
        {
            "source_id": "NS636_gate",
            "path": "source-intake/mts_residuals/P8_Y5_R10_636_NO_SHADOW_FRAME_GATE.csv",
            "role": "no-shadow-frame rule for observable frame leakage",
            "needle": "NS636_0_observable_completeness",
        },
        {
            "source_id": "MCD716_derivation",
            "path": "source-intake/mts_residuals/P8_Y5_R10_716_MATTER_COUPLING_DERIVATION.csv",
            "role": "finite matter coupling/source charge fallback",
            "needle": "MCD716_6_current_corpus_verdict",
        },
        {
            "source_id": "MDS898_signature",
            "path": "source-intake/mts_residuals/P8_Y5_R10_898_MATTER_DESCENT_SIGNATURE.csv",
            "role": "latest matter descent/source-cokernel signature",
            "needle": "MDS898_5_verdict",
        },
        {
            "source_id": "KD930_chain",
            "path": "source-intake/mts_residuals/P8_Y5_R10_930_COUPLING_DERIVATION_CHAIN.csv",
            "role": "coupling derivation chain tying BF source charge to observed worldtube",
            "needle": "KD930_3_same_worldtube",
        },
    ]
    rows = []
    for spec in specs:
        path = ROOT / spec["path"]
        exists = path.exists()
        needle_found = exists and spec["needle"] in read_text(path)
        rows.append(
            {
                **spec,
                "absolute_path": str(path),
                "exists": flag(exists),
                "needle_found": flag(needle_found),
                "valid_for_claim": "false",
                "generated_utc": stamp(),
            }
        )
    return rows


def descent_proof_gate() -> list[dict[str, str]]:
    specs = [
        (
            "QDG944_0_parent_q_map",
            "parent defines q:Phi_parent -> Q_obs before matter coupling and readout",
            "q is part of the parent configuration/action data, not a post-fit equivalence",
            "unsigned",
            "without q, Dq(v)=0 is only notation",
        ),
        (
            "QDG944_1_vertical_generator",
            "representative/frame leak direction v lies in ker(Dq)",
            "Dq(v)=0 for local representative Weyl/disformal/mass-frame variations",
            "unsigned",
            "without verticality, chain-rule blindness does not apply",
        ),
        (
            "QDG944_2_observed_coframe_functor",
            "observed coframe is a functor on quotient data",
            "e_obs(Phi)=Obs_e(q(Phi)); Lie_v e_obs=DObs_e[Dq(v)]=0",
            "conditional_lemma_not_parent_signed",
            "current corpus has the theorem shape but not the parent map",
        ),
        (
            "QDG944_3_matter_action_factorization",
            "ordinary matter depends on parent fields only through e_obs and quotient-owned constants",
            "S_matter[Phi,Psi]=Sbar_matter[q(Phi),Psi,theta], Lie_v theta=0",
            "not_parent_signed",
            "representative A_g/B_g/m_A channels remain legal",
        ),
        (
            "QDG944_4_geometry_stack_descent",
            "measure, metric/coframe, connection, and derivative operator all descend",
            "mu_m,e_m,g_m,omega_m,D_m = functions of q(Phi) or owned gauge/exact data",
            "not_parent_signed",
            "connection/torsion/nonmetricity can re-enter source force",
        ),
        (
            "QDG944_5_no_marker_constants",
            "species constants, masses, charges, and clock standards are quotient-owned/superselected",
            "Lie_v theta_A=Lie_v m_A=Lie_v alpha_EM=0 or finite coefficients retained",
            "not_parent_signed",
            "WEP/clock/source-charge residuals remain active",
        ),
        (
            "QDG944_6_boundary_no_tail",
            "vertical variation has no local boundary/source-measure tail",
            "Lie_v S_matter=0 up to dB with Pi_local dB=0 and zero compact flux",
            "not_parent_signed",
            "boundary/EFT terms can carry local source work",
        ),
        (
            "QDG944_7_total",
            "quotient observed-coframe descent proof",
            "QDG944_0..QDG944_6 all parent-signed",
            "not_proved_current_corpus",
            "descent route remains conditional; source-bound fallback stays active",
        ),
    ]
    return [
        {
            "gate_id": gate_id,
            "required_clause": required_clause,
            "mathematical_requirement": mathematical_requirement,
            "current_status": current_status,
            "failure_if_missing": failure_if_missing,
            "parent_signed": "false",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        }
        for gate_id, required_clause, mathematical_requirement, current_status, failure_if_missing in specs
    ]


def proof_attempt_rows() -> list[dict[str, str]]:
    specs = [
        (
            "P944_0_assume_signed_q",
            "Assume q and v are parent-owned with Dq(v)=0.",
            "Then v is a representative direction, not an ordinary observable variation.",
            "conditional_step",
            "q and v not extracted from current parent action",
        ),
        (
            "P944_1_chain_rule_coframe",
            "If e_obs=Obs_e(q(Phi)), then Lie_v e_obs=0.",
            "Lie_v e_obs = DObs_e[Dq(v)] = 0.",
            "valid_conditional_proof",
            "does not prove e_obs descends",
        ),
        (
            "P944_2_chain_rule_matter",
            "If S_matter=Sbar[q(Phi),Psi,theta] and Lie_v theta=0, then Lie_v S_matter=0.",
            "Lie_v S_matter = delta Sbar/delta q Dq(v) + partial_theta Sbar Lie_v theta = 0.",
            "valid_conditional_proof",
            "does not prove constants/masses are quotient-owned",
        ),
        (
            "P944_3_source_zero",
            "The representative matter source J_v vanishes only under P944_0..P944_2.",
            "J_v := delta S_matter/delta v = 0.",
            "conditional_zero_only",
            "cannot promote c_g/b_A/q_nonH zero",
        ),
        (
            "P944_4_worldtube_support",
            "If the observed Hilbert current is unique, W_source is fixed by its support.",
            "W_source=closure supp T_obs(n,tau).",
            "conditional_support_only",
            "tau/n and positivity/readout locks remain unsigned",
        ),
        (
            "P944_5_counterexample_common_frame",
            "A representative frame factor breaks the theorem.",
            "e_m=A_g(X)e_obs gives Lie_v e_m=(Lie_v ln A_g)e_m.",
            "legal_counterexample_until_forbidden",
            "requires b_g source bound or no-shadow proof",
        ),
        (
            "P944_6_counterexample_material_marker",
            "A material constant/mass marker breaks the theorem.",
            "m_A=m_A(X,theta) gives b_A=Lie_v ln m_A.",
            "legal_counterexample_until_forbidden",
            "requires b_A source bound or constants descent proof",
        ),
        (
            "P944_7_verdict",
            "944 cannot prove the current MTS parent descent.",
            "conditional theorem true; parent ownership certificate missing.",
            "proof_not_closed",
            "next target must either construct q/Obs_e explicitly or source first frame-leak bounds",
        ),
    ]
    return [
        {
            "proof_id": proof_id,
            "step": step,
            "mathematical_form": mathematical_form,
            "status": status,
            "gap": gap,
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        }
        for proof_id, step, mathematical_form, status, gap in specs
    ]


def frame_leak_bound_pack() -> list[dict[str, str]]:
    specs = [
        (
            "FLB944_0_cg_weyl",
            "c_g or b_g",
            "c_g := d ln A_g/dXhat for representative Weyl/common matter frame",
            "dimensionless",
            "R10;PPN;WEP;clock",
            "alpha_R10 ~ K_X(lambda) Qbar_XH tau_R10 c_g",
            "MISSING_PARENT_ZERO_OR_NUMERIC_CG",
        ),
        (
            "FLB944_1_disformal",
            "b_dis",
            "b_dis := dB_g/dXhat for representative disformal matter frame",
            "model_dependent",
            "PPN;preferred_frame;clock;orbital",
            "r_dis ~ M_dis(lambda,profile) tau_dis b_dis",
            "MISSING_DISFORMAL_ZERO_OR_NUMERIC_BOUND",
        ),
        (
            "FLB944_2_species_mass",
            "b_A",
            "b_A := d ln m_A^obs/dXhat for species/material standard A",
            "dimensionless",
            "WEP;clock;composition",
            "eta_AB ~ (b_A-b_B) q_test profile",
            "MISSING_MASS_CONSTANT_DESCENT_OR_NUMERIC_BA",
        ),
        (
            "FLB944_3_charge_clock_constants",
            "b_alpha;b_clock",
            "vertical derivative of EM/frequency/binding constants",
            "dimensionless",
            "clock;EM;composition",
            "delta ln nu ~ S_alpha b_alpha + S_mass b_A",
            "MISSING_CONSTANT_DESCENT_OR_CLOCK_BOUND",
        ),
        (
            "FLB944_4_nonHilbert_current",
            "q_nonH",
            "source projection carried by torsion/nonmetricity/boundary/non-Hilbert currents",
            "same_as_source_current",
            "R10;PPN;source_normalization",
            "r_nonH ~ Pi_local q_nonH / M_ref",
            "MISSING_NONHILBERT_ZERO_FLUX_OR_NUMERIC_SOURCE",
        ),
        (
            "FLB944_5_tau_normal_shift",
            "Delta_tau_n",
            "mismatch of source tau/n frame and readout tau/n frame",
            "dimensionless",
            "clock;orbital;source_support",
            "Delta M/M ~ Delta_tau_n + Delta_frame_source",
            "MISSING_TAU_NORMAL_LOCK_OR_NUMERIC_BOUND",
        ),
        (
            "FLB944_6_support_shift",
            "Delta_W_support",
            "change in Hilbert source support under allowed observed-frame choices",
            "dimensionless",
            "orbital;local_GR",
            "Delta Q_H/M_ref under support-rule variation",
            "MISSING_SUPPORT_EQUIVALENCE_OR_NUMERIC_BOUND",
        ),
        (
            "FLB944_7_epsilon_frame_leak",
            "epsilon_frame_leak",
            "component-sum absolute normalized frame/coupling leak residual",
            "dimensionless",
            "all_local_arenas",
            "sum_abs(components)/normalization",
            "MISSING_COMPONENT_INPUTS",
        ),
    ]
    return [
        {
            "bound_id": bound_id,
            "symbol": symbol,
            "definition": definition,
            "units": units,
            "observable_link": observable_link,
            "score_formula": score_formula,
            "current_status": current_status,
            "required_columns": "mode_or_system_id;value;units;arena_projection;source_path;zero_theorem_path;normalization;valid_for_claim",
            "score_ready": "false",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        }
        for bound_id, symbol, definition, units, observable_link, score_formula, current_status in specs
    ]


def route_comparison() -> list[dict[str, str]]:
    specs = [
        (
            "ROUTE944_0_parent_q_construction",
            "construct explicit q:Phi->Q_obs and Obs_e(q)",
            "highest derivation value; would convert chain-rule lemma into a real parent theorem",
            "hardest but best aligned with GR-reduction goal",
            "selected_next",
        ),
        (
            "ROUTE944_1_matter_functor_axiom",
            "declare S_matter=Sbar[q,Psi,theta] as a parent axiom",
            "short route to consistency but looks axiomatic unless tied to parent construction",
            "allowed only as labelled closure/contract, not proof",
            "not_selected",
        ),
        (
            "ROUTE944_2_no_shadow_theorem",
            "prove any experiment-affecting frame must be quotient-owned",
            "would forbid hidden A_g/B_g/m_A channels by observability definition",
            "useful support, still needs q/Obs_e object",
            "supporting_route",
        ),
        (
            "ROUTE944_3_source_bound_pack",
            "source b_g,b_A,b_dis,q_nonH numeric bounds",
            "fastest path to empirical scoring if derivation stalls",
            "less fundamental than proof; still needed for retained branch",
            "fallback_ready",
        ),
    ]
    return [
        {
            "route_id": route_id,
            "route": route,
            "benefit": benefit,
            "risk": risk,
            "decision": decision,
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        }
        for route_id, route, benefit, risk, decision in specs
    ]


def decisions() -> list[dict[str, str]]:
    return [
        {
            "decision_id": "DEC944_0_descent",
            "decision": "quotient_descent_theorem_conditional_not_parent_proved",
            "reason": "chain-rule proof is valid if q, v in ker(Dq), Obs_e(q), and matter factorization are parent-signed, but source hierarchy keeps those clauses unsigned",
            "consequence": "no frame-leak zero, W_source selector, beta, R10, WEP, clock, orbital, or local-GR claim",
            "next_action": "construct explicit parent q/Obs_e map or keep source-bound fallback",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "decision_id": "DEC944_1_best_next",
            "decision": "parent_q_map_and_Obs_e_functor_selected_next",
            "reason": "without an explicit parent q map, every later matter descent proof is only a chain-rule conditional",
            "consequence": "945 should attack q:Phi->Q_obs and Obs_e(q) directly before numeric bound acquisition",
            "next_action": "945-Y5-R10-parent-q-map-Obs-e-functor-construction-or-first-frame-leak-bound-pack.md",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "decision_id": "DEC944_2_bound_fallback",
            "decision": "frame_leak_bound_pack_ready_but_nonclaim",
            "reason": "if q/Obs_e cannot be parent-constructed, b_g,b_dis,b_A,q_nonH must be sourced before empirical local scoring",
            "consequence": "retained branch has a concrete data interface but no placeholders count as evidence",
            "next_action": "use FLB944 rows only after source paths and numeric/theorem-zero inputs exist",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
    ]


def claim_gates() -> list[dict[str, str]]:
    return [
        {
            "gate_id": "CGATE944_0_q_map",
            "claim": "parent q:Phi->Q_obs is defined and owns local representative verticality",
            "blocker": "explicit current-MTS q map and Dq kernel not extracted",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "gate_id": "CGATE944_1_coframe_descent",
            "claim": "e_obs=Obs_e(q(Phi)) parent-signed",
            "blocker": "observed coframe functor remains conditional template",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "gate_id": "CGATE944_2_matter_descent",
            "claim": "S_matter descends to quotient for all ordinary matter",
            "blocker": "matter action, constants/masses, geometry stack, and boundary tails are unsigned",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "gate_id": "CGATE944_3_frame_leak_bounds",
            "claim": "retained frame leaks are numerically scoreable",
            "blocker": "FLB944 rows are schemas only with missing parent zero or numeric sources",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "gate_id": "CGATE944_4_local_GR",
            "claim": "local GR/Newton/PPN reduction is derived",
            "blocker": "q/Obs_e descent, same-worldtube source glue, measured-GM normalization, and PPN stability remain open",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
    ]


def next_target() -> list[dict[str, str]]:
    return [
        {
            "next_target": "945-Y5-R10-parent-q-map-Obs-e-functor-construction-or-first-frame-leak-bound-pack.md",
            "objective": "try to construct the parent quotient map q:Phi->Q_obs and observed coframe functor Obs_e(q) explicitly enough to sign descent; if not, promote FLB944 schemas into first source-bound rows",
            "include": "parent fields Phi, quotient variables Q_obs, vertical generator basis, Dq kernel test, Obs_e construction, local Lorentz gauge separation, Weyl/disformal/mass counterexamples, b_g/b_A first-bound fallback",
            "exclude": "assuming q exists by notation, declaring matter descent from chain rule alone, hiding frame leaks, local-GR claim, beta pass claim, GitHub action, formalization-workbench edits",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        }
    ]


def formalization_changed_after_start() -> int:
    if not FORMALIZATION.exists():
        return -1
    changed = 0
    for path in FORMALIZATION.rglob("*"):
        if not path.is_file():
            continue
        modified = datetime.fromtimestamp(path.stat().st_mtime, timezone.utc)
        if modified > SCRIPT_START_UTC:
            changed += 1
    return changed


def validation(
    sources: list[dict[str, str]],
    gate_rows: list[dict[str, str]],
    proof_rows: list[dict[str, str]],
    bound_rows: list[dict[str, str]],
    route_rows: list[dict[str, str]],
    decision_rows: list[dict[str, str]],
    claim_rows: list[dict[str, str]],
    target_rows: list[dict[str, str]],
) -> list[dict[str, str]]:
    rows = []

    def add(check_id: str, passed: bool, detail: str) -> None:
        rows.append({"check_id": check_id, "result": "pass" if passed else "fail", "detail": detail, "generated_utc": stamp()})

    prior = read_csv(OUT / "P8_Y5_BRR545_943_VALIDATION.csv")
    prior_clean = prior and all(row.get("result") == "pass" for row in prior)
    sources_ok = all(row["exists"] == "true" and row["needle_found"] == "true" for row in sources)
    not_proved = any(row["gate_id"] == "QDG944_7_total" and row["current_status"] == "not_proved_current_corpus" for row in gate_rows)
    proof_conditional = any(row["proof_id"] == "P944_7_verdict" and row["status"] == "proof_not_closed" for row in proof_rows)
    counterexamples_retained = any(row["proof_id"] == "P944_5_counterexample_common_frame" and row["status"] == "legal_counterexample_until_forbidden" for row in proof_rows) and any(row["proof_id"] == "P944_6_counterexample_material_marker" and row["status"] == "legal_counterexample_until_forbidden" for row in proof_rows)
    bounds_blocked = bound_rows and all(row["score_ready"] == "false" and row["claim_allowed"] == "false" for row in bound_rows)
    q_route_selected = any(row["route_id"] == "ROUTE944_0_parent_q_construction" and row["decision"] == "selected_next" for row in route_rows)
    decisions_nonclaim = all(row["valid_for_claim"] == "false" for row in decision_rows)
    claims_false = all(row["claim_allowed"] == "false" and row["valid_for_claim"] == "false" for row in claim_rows)
    next_selected = any(row["next_target"].startswith("945-Y5-R10-parent-q-map") for row in target_rows)
    no_claims = all(
        row.get("valid_for_claim") == "false"
        for row in sources + gate_rows + proof_rows + bound_rows + route_rows + decision_rows + claim_rows + target_rows
    )
    formalization_changed = formalization_changed_after_start()

    add("V944_0_sources_exist_and_needles", sources_ok, "all 944 source paths exist and needles are present" if sources_ok else "missing source path or needle")
    add("V944_1_prior_943_clean", prior_clean, "P8_Y5_BRR545_943_VALIDATION.csv clean")
    add("V944_2_descent_not_proved", not_proved, "quotient descent proof not promoted")
    add("V944_3_proof_conditional", proof_conditional, "chain-rule proof retained as conditional only")
    add("V944_4_counterexamples_retained", counterexamples_retained, "Weyl/disformal/mass-marker counterexamples retained")
    add("V944_5_bound_rows_blocked", bounds_blocked, "frame-leak bound rows are schemas only")
    add("V944_6_parent_q_route_selected", q_route_selected, "parent q/Obs_e construction selected before numeric fallback")
    add("V944_7_decisions_nonclaim", decisions_nonclaim, "decision ledger remains nonclaim")
    add("V944_8_claim_gates_false", claims_false, "all claim gates remain false")
    add("V944_9_next_target_selected", next_selected, "945 parent q-map/Obs_e target selected")
    add("V944_10_no_claims_promoted", no_claims, "all generated rows are valid_for_claim=false")
    add("V944_11_formalization_workbench_untouched", formalization_changed == 0, f"formalization_changed_after_start={formalization_changed}")
    add("V944_12_validation_rows_ready", True, "validation table constructed")
    return rows


def write_doc(
    sources: list[dict[str, str]],
    gate_rows: list[dict[str, str]],
    proof_rows: list[dict[str, str]],
    bound_rows: list[dict[str, str]],
    route_rows: list[dict[str, str]],
    decision_rows: list[dict[str, str]],
    claim_rows: list[dict[str, str]],
    target_rows: list[dict[str, str]],
    validation_rows: list[dict[str, str]],
) -> None:
    text = f"""# 944 - Y5/R10 Quotient Observed-Coframe Descent Proof Or Frame-Leak Source Bounds

Generated: `{stamp()}`

Status: `Y5_R10_944_quotient_descent_chain_rule_valid_but_parent_q_Obs_e_not_constructed_frame_leak_bounds_ready_nonclaim`

Claim ceiling: `descent_gate_only_no_frame_leak_zero_no_R10_WEP_PPN_clock_or_local_GR_pass`

## Result

944 confirms the exact mathematical situation:

```text
q: Phi_parent -> Q_obs,
v in ker(Dq),
e_obs(Phi)=Obs_e(q(Phi)),
S_matter[Phi,Psi]=Sbar_matter[q(Phi),Psi,theta],
Lie_v theta=0
```

would imply:

```text
Lie_v e_obs = DObs_e[Dq(v)] = 0,
Lie_v S_matter = 0,
J_v = delta S_matter/delta v = 0.
```

So the descent theorem is real. It is not a fake route. But 944 does **not** prove the current MTS parent has the required `q` map, vertical generator basis, `Obs_e` functor, matter factorization, constants/mass descent, or boundary no-tail certificate.

That means `c_g/b_g`, `b_dis`, `b_A`, `q_nonH`, `Delta_tau_n`, and `Delta_W_support` remain retained frame-leak variables. They are not allowed to vanish by vibes. They need either a parent-signed zero theorem or real source/bound rows.

The best next derivation route is narrower than before: construct `q:Phi->Q_obs` and `Obs_e(q)` explicitly. If that cannot be done, the retained branch should switch to the first frame-leak bound pack.

## Source Register

{md_table(sources, ["source_id", "path", "role", "needle_found", "valid_for_claim"])}

## Descent Proof Gate

{md_table(gate_rows, ["gate_id", "required_clause", "mathematical_requirement", "current_status", "failure_if_missing"])}

## Proof Attempt

{md_table(proof_rows, ["proof_id", "step", "mathematical_form", "status", "gap"])}

## Frame-Leak Bound Pack

{md_table(bound_rows, ["bound_id", "symbol", "definition", "observable_link", "score_formula", "current_status", "score_ready"])}

## Route Comparison

{md_table(route_rows, ["route_id", "route", "benefit", "risk", "decision"])}

## Decision Ledger

{md_table(decision_rows, ["decision_id", "decision", "reason", "consequence", "next_action", "valid_for_claim"])}

## Claim Gates

{md_table(claim_rows, ["gate_id", "claim", "blocker", "claim_allowed", "valid_for_claim"])}

## Validation

{md_table(validation_rows, ["check_id", "result", "detail", "generated_utc"])}

## Next Target

{md_table(target_rows, ["next_target", "objective", "include", "exclude", "valid_for_claim"])}
"""
    DOC.write_text(text, encoding="utf-8")


def ensure_csv_roundtrip(paths: list[Path]) -> None:
    for path in paths:
        rows = read_csv(path)
        if rows and any(None in row for row in rows):
            raise SystemExit(f"malformed CSV row in {path}")


def main() -> None:
    sources = source_register()
    gate_rows = descent_proof_gate()
    proof_rows = proof_attempt_rows()
    bound_rows = frame_leak_bound_pack()
    route_rows = route_comparison()
    decision_rows = decisions()
    claim_rows = claim_gates()
    target_rows = next_target()
    validation_rows = validation(sources, gate_rows, proof_rows, bound_rows, route_rows, decision_rows, claim_rows, target_rows)

    output_specs = [
        (
            OUT / "P8_Y5_R10_944_SOURCE_REGISTER.csv",
            sources,
            ["source_id", "path", "absolute_path", "role", "needle", "exists", "needle_found", "valid_for_claim", "generated_utc"],
        ),
        (
            OUT / "P8_Y5_R10_944_DESCENT_PROOF_GATE.csv",
            gate_rows,
            ["gate_id", "required_clause", "mathematical_requirement", "current_status", "failure_if_missing", "parent_signed", "claim_allowed", "valid_for_claim", "generated_utc"],
        ),
        (
            OUT / "P8_Y5_R10_944_PROOF_ATTEMPT.csv",
            proof_rows,
            ["proof_id", "step", "mathematical_form", "status", "gap", "claim_allowed", "valid_for_claim", "generated_utc"],
        ),
        (
            OUT / "P8_Y5_R10_944_FRAME_LEAK_BOUND_PACK.csv",
            bound_rows,
            ["bound_id", "symbol", "definition", "units", "observable_link", "score_formula", "current_status", "required_columns", "score_ready", "claim_allowed", "valid_for_claim", "generated_utc"],
        ),
        (
            OUT / "P8_Y5_R10_944_ROUTE_COMPARISON.csv",
            route_rows,
            ["route_id", "route", "benefit", "risk", "decision", "valid_for_claim", "generated_utc"],
        ),
        (
            OUT / "P8_Y5_R10_944_DECISION_LEDGER.csv",
            decision_rows,
            ["decision_id", "decision", "reason", "consequence", "next_action", "valid_for_claim", "generated_utc"],
        ),
        (
            OUT / "P8_Y5_R10_944_CLAIM_GATE.csv",
            claim_rows,
            ["gate_id", "claim", "blocker", "claim_allowed", "valid_for_claim", "generated_utc"],
        ),
        (
            OUT / "P8_Y5_R10_944_NEXT_TARGET.csv",
            target_rows,
            ["next_target", "objective", "include", "exclude", "valid_for_claim", "generated_utc"],
        ),
        (
            OUT / "P8_Y5_BRR545_944_VALIDATION.csv",
            validation_rows,
            ["check_id", "result", "detail", "generated_utc"],
        ),
    ]

    for path, rows, fieldnames in output_specs:
        write_csv(path, rows, fieldnames)

    ensure_csv_roundtrip([path for path, _rows, _fieldnames in output_specs])
    write_doc(sources, gate_rows, proof_rows, bound_rows, route_rows, decision_rows, claim_rows, target_rows, validation_rows)

    failures = [row for row in validation_rows if row["result"] != "pass"]
    if failures:
        raise SystemExit(f"validation failed: {failures}")

    print("Y5_R10_944_quotient_descent_chain_rule_valid_but_parent_q_Obs_e_not_constructed_frame_leak_bounds_ready_nonclaim")
    print(f"wrote {DOC}")
    print("next target: 945-Y5-R10-parent-q-map-Obs-e-functor-construction-or-first-frame-leak-bound-pack.md")


if __name__ == "__main__":
    main()

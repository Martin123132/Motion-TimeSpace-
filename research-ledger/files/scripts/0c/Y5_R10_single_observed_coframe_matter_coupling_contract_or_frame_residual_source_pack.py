from __future__ import annotations

import csv
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "source-intake" / "mts_residuals"
DOC = ROOT / "943-Y5-R10-single-observed-coframe-matter-coupling-contract-or-frame-residual-source-pack.md"
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
            "source_id": "942_doc",
            "path": "942-Y5-R10-parent-worldtube-selector-source-frame-or-CbetaN5-kernel-fill.md",
            "role": "handoff selecting single observed coframe and coupling clause",
            "needle": "The good news is that the missing object is no longer vague",
        },
        {
            "source_id": "942_validation",
            "path": "source-intake/mts_residuals/P8_Y5_BRR545_942_VALIDATION.csv",
            "role": "previous checkpoint validation",
            "needle": "V942_13_validation_rows_ready",
        },
        {
            "source_id": "942_next_target",
            "path": "source-intake/mts_residuals/P8_Y5_R10_942_NEXT_TARGET.csv",
            "role": "943 target contract",
            "needle": "943-Y5-R10-single-observed-coframe-matter-coupling-contract-or-frame-residual-source-pack.md",
        },
        {
            "source_id": "PAC537_contract",
            "path": "source-intake/mts_residuals/P8_Y5_HILBERT_WORLDTUBE_PARENT_ACTION_CONTRACT.csv",
            "role": "open same-frame and fixed-worldtube parent clauses",
            "needle": "PAC537_1_single_observed_source_frame",
        },
        {
            "source_id": "WT510_clauses",
            "path": "source-intake/mts_residuals/P8_WORLDTUBE_SOURCE_MEASURE_CLAUSES.csv",
            "role": "open minimal observed matter coupling and tau lock",
            "needle": "WG510_1_minimal_observed_matter_coupling",
        },
        {
            "source_id": "SC_contract",
            "path": "source-intake/mts_residuals/P8_source_current_Ward_universality_CONTRACT.csv",
            "role": "source-current Ward/universality contract",
            "needle": "SC0_single_observed_coframe_input",
        },
        {
            "source_id": "PMC622_contract",
            "path": "source-intake/mts_residuals/P8_Y5_R10_622_PARENT_MATTER_CONTRACT.csv",
            "role": "parent matter functor and quotient geometry contract",
            "needle": "PMC622_2_unique_observed_geometry",
        },
        {
            "source_id": "OCF623_theorem",
            "path": "source-intake/mts_residuals/P8_Y5_R10_623_COFRAME_FUNCTOR_THEOREM_ATTEMPT.csv",
            "role": "quotient coframe factorization lemma",
            "needle": "OCF623_0_factorization_lemma",
        },
        {
            "source_id": "MF631_cases",
            "path": "source-intake/mts_residuals/P8_Y5_R10_631_MATTER_FRAME_CASES.csv",
            "role": "quotient, conformal, disformal, and mass-dependence matter-frame cases",
            "needle": "MF631_0_quotient_only",
        },
        {
            "source_id": "NS636_gate",
            "path": "source-intake/mts_residuals/P8_Y5_R10_636_NO_SHADOW_FRAME_GATE.csv",
            "role": "no-shadow-frame classification gate",
            "needle": "NS636_0_observable_completeness",
        },
        {
            "source_id": "PAL703_audit",
            "path": "source-intake/mts_residuals/P8_Y5_R10_703_PARENT_ACTION_COUPLING_LOCK_AUDIT.csv",
            "role": "parent action coupling-lock audit",
            "needle": "PAL703_2_matter_functor",
        },
        {
            "source_id": "MCD716_derivation",
            "path": "source-intake/mts_residuals/P8_Y5_R10_716_MATTER_COUPLING_DERIVATION.csv",
            "role": "retained matter coupling and scalar/source charge derivation",
            "needle": "MCD716_6_current_corpus_verdict",
        },
        {
            "source_id": "JHH927_clauses",
            "path": "source-intake/mts_residuals/P8_Y5_R10_927_JHH_SOURCE_PROOF_CLAUSES.csv",
            "role": "same observed frame and worldtube source proof clauses",
            "needle": "JHH927_0_single_observed_frame",
        },
        {
            "source_id": "KD930_chain",
            "path": "source-intake/mts_residuals/P8_Y5_R10_930_COUPLING_DERIVATION_CHAIN.csv",
            "role": "coupling derivation chain requiring same observed worldtube",
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


def coframe_contract() -> list[dict[str, str]]:
    specs = [
        (
            "CFC943_0_parent_quotient_map",
            "parent provides a quotient map q:Phi -> Q_obs before readout",
            "q(Phi) is fixed by the parent kinematics; vertical v has Dq(v)=0",
            "defines what ordinary matter is allowed to see",
            "not_parent_signed_currently",
        ),
        (
            "CFC943_1_observed_coframe_descent",
            "observed coframe descends through the quotient, not representative coordinates",
            "e_obs(Phi)=Obs_e(q(Phi)); therefore Lie_v e_obs = D Obs_e[Dq(v)] = 0",
            "kills representative-frame leakage by chain rule",
            "conditional_lemma_available_not_parent_signed",
        ),
        (
            "CFC943_2_matter_functor",
            "ordinary matter action is a functor of the descended observed coframe",
            "S_m=sum_A S_A[psi_A,e_obs,omega[e_obs],theta_A]",
            "makes Hilbert source, clocks, rods, and orbital readout use one frame",
            "not_parent_signed",
        ),
        (
            "CFC943_3_constants_and_masses",
            "material constants and masses are quotient-owned/superselected, not vertical fields",
            "Lie_v theta_A=0 and Lie_v m_A=0, or finite b_A retained",
            "prevents mass-ratio or clock coupling from bypassing metric descent",
            "not_parent_signed",
        ),
        (
            "CFC943_4_connection_lock",
            "matter connection is induced by e_obs unless an extra current is explicitly retained",
            "omega_m=omega[e_obs] and non-Hilbert source current is absent/exact/zero-flux/retained",
            "prevents torsion/nonmetricity from becoming a hidden source force",
            "not_parent_signed",
        ),
        (
            "CFC943_5_tau_normal_lock",
            "tau and the source normal n are defined in the same observed frame",
            "rho_H=T_obs(n,tau), W_source=closure supp rho_H",
            "turns source support into an observed-current support rather than a fit domain",
            "open_from_WG510_2",
        ),
        (
            "CFC943_6_no_shadow_frame_rule",
            "any frame that affects rods, clocks, masses, charges, or free fall is observable",
            "if A(X), B(X), or m_A(X) affects an experiment, it must descend through Q_obs or be retained",
            "forbids invisible representative-frame cheating",
            "candidate_repair_contract_not_theorem",
        ),
        (
            "CFC943_7_contract_verdict",
            "CFC943_0 through CFC943_6 would sign the coupling/frame branch",
            "then Delta_frame_source=Delta_worldtube_domain=0 at the selector level",
            "would unblock same-worldtube proof target upstream of R_glue and PPN",
            "contract_exact_but_unsigned",
        ),
    ]
    return [
        {
            "contract_id": contract_id,
            "required_clause": required_clause,
            "mathematical_form": mathematical_form,
            "why_needed": why_needed,
            "current_status": current_status,
            "parent_signed": "false",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        }
        for contract_id, required_clause, mathematical_form, why_needed, current_status in specs
    ]


def derivation_attempt() -> list[dict[str, str]]:
    specs = [
        (
            "DER943_0_vertical_blindness",
            "If e_obs=Obs_e(q(Phi)) and Dq(v)=0, then Lie_v e_obs=0.",
            "Lie_v e_obs = D Obs_e[Dq(v)] = 0",
            "valid conditional chain-rule lemma from OCF623",
            "does_not_prove_parent_factorization",
        ),
        (
            "DER943_1_matter_action_blindness",
            "If S_m depends on Phi only through e_obs and quotient-owned theta_A, then Lie_v S_m=0.",
            "Lie_v S_m = (delta S_m/delta e_obs) Lie_v e_obs + sum_A (partial S_m/partial theta_A) Lie_v theta_A = 0",
            "valid conditional theorem",
            "theta_A and e_obs descent not parent-signed",
        ),
        (
            "DER943_2_source_current_blindness",
            "Vertical/source-frame current vanishes only after the matter action blindness theorem.",
            "J_v := delta S_m/delta v = 0",
            "conditional zero of representative matter charge",
            "not a current claim",
        ),
        (
            "DER943_3_one_Hilbert_current",
            "The active ordinary source is the observed Hilbert/coframe current if the matter functor is signed.",
            "T_obs^{mu nu}=2/sqrt(-g_obs) delta S_m/delta g_obs_munu",
            "conditional definition",
            "full parent source-current definition still open",
        ),
        (
            "DER943_4_support_selector",
            "The source worldtube follows from the support of the observed Hilbert energy density.",
            "W_source=closure supp T_obs(n,tau)",
            "conditional support theorem",
            "tau/n lock and positivity/support conditions unsigned",
        ),
        (
            "DER943_5_shadow_counterexample",
            "A representative Weyl/disformal/mass channel evades the zero theorem unless forbidden or retained.",
            "g_A=A_A(X)^2 g_obs + B_A(X)U_mu U_nu; m_A=m_A(X,theta)",
            "counterexample class retained",
            "must source b_A,c_g,b_g or prove no-shadow frame theorem",
        ),
        (
            "DER943_6_verdict",
            "The derivation path is real but conditional; the project has not yet derived the parent matter functor.",
            "signed quotient descent => frame/source leakage zero; unsigned descent => retained residuals",
            "selected_as_next_derivation_target",
            "no local_GR_or_beta_promotion",
        ),
    ]
    return [
        {
            "derivation_id": derivation_id,
            "statement": statement,
            "mathematical_form": mathematical_form,
            "derivation_status": derivation_status,
            "gap": gap,
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        }
        for derivation_id, statement, mathematical_form, derivation_status, gap in specs
    ]


def frame_residual_source_pack() -> list[dict[str, str]]:
    specs = [
        (
            "FRS943_0_common_frame_log_derivative",
            "b_g",
            "b_g := Lie_v ln A_g at local point for any representative Weyl frame g_m=A_g^2 g_obs",
            "mode_id;A_g_definition;b_g;units;source_path;zero_theorem_path;valid_for_claim",
            "MISSING_QUOTIENT_DESCENT_OR_NUMERIC_BOUND",
            "R10;PPN;WEP;clock",
        ),
        (
            "FRS943_1_disformal_frame_derivative",
            "b_dis",
            "b_dis := Lie_v B_g for representative disformal matter frame",
            "mode_id;B_g_definition;b_dis;units;source_path;zero_theorem_path;valid_for_claim",
            "MISSING_DISFORMAL_ABSENCE_OR_BOUND",
            "PPN;preferred_frame;clock",
        ),
        (
            "FRS943_2_species_mass_derivative",
            "b_A",
            "b_A := Lie_v ln m_A^obs for species or material standard A",
            "species_id;material_class;b_A;units;source_path;zero_theorem_path;valid_for_claim",
            "MISSING_MASS_CONSTANT_DESCENT_OR_BOUND",
            "WEP;clock;composition",
        ),
        (
            "FRS943_3_universal_coupling_derivative",
            "partial_v kappa",
            "vertical/source derivative of the universal Hilbert coupling",
            "mode_id;kappa_definition;partial_v_kappa;units;source_path;zero_theorem_path;valid_for_claim",
            "MISSING_CONSTANT_KAPPA_THEOREM",
            "Gdot;source_normalization;orbital",
        ),
        (
            "FRS943_4_tau_normal_frame_shift",
            "Delta_tau_n",
            "mismatch between source tau/n and exterior/readout tau/n",
            "system_id;tau_source;tau_readout;n_source;n_readout;Delta_tau_n;source_path;valid_for_claim",
            "MISSING_TAU_NORMAL_LOCK",
            "clock;orbital;source_support",
        ),
        (
            "FRS943_5_worldtube_support_shift",
            "Delta_W_support",
            "support-domain shift induced by changing observed coframe or matter frame",
            "system_id;support_rule_A;support_rule_B;Delta_W_support;source_path;valid_for_claim",
            "MISSING_SUPPORT_FRAME_EQUIVALENCE",
            "local_GR;orbital",
        ),
        (
            "FRS943_6_nonHilbert_current_projection",
            "q_nonH",
            "ordinary-matter-source projection carried by non-Hilbert torsion/connection/boundary currents",
            "channel_id;current_definition;q_nonH;units;source_path;zero_flux_path;valid_for_claim",
            "MISSING_NONHILBERT_CURRENT_SILENCE",
            "R10;PPN;WEP",
        ),
        (
            "FRS943_7_epsilon_frame_coupling",
            "epsilon_frame_coupling",
            "component-sum absolute normalized frame/coupling residual",
            "system_id;epsilon_frame_coupling;component_sum_abs;normalization;source_path;valid_for_claim",
            "MISSING_COMPONENT_INPUTS",
            "all_local_arenas",
        ),
    ]
    return [
        {
            "row_id": row_id,
            "symbol": symbol,
            "definition": definition,
            "required_columns": required_columns,
            "current_status": current_status,
            "observable_link": observable_link,
            "score_ready": "false",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        }
        for row_id, symbol, definition, required_columns, current_status, observable_link in specs
    ]


def arena_gate_map() -> list[dict[str, str]]:
    specs = [
        (
            "ARENA943_0_R10",
            "short-range/fifth-force",
            "b_g,b_dis,b_A,q_nonH",
            "zero only if quotient descent/no-shadow frame is signed; otherwise source alpha(lambda) rows",
            "blocked",
        ),
        (
            "ARENA943_1_WEP",
            "composition universality",
            "b_A species spread, eta_AB, q_nonH",
            "zero only if all matter constants/masses descend to quotient or are universal",
            "blocked",
        ),
        (
            "ARENA943_2_PPN",
            "gamma/beta/preferred-frame",
            "b_g,b_dis,Delta_tau_n,nonHilbert current",
            "zero only after same observed frame and second-order readout stability",
            "blocked",
        ),
        (
            "ARENA943_3_clocks",
            "clock/frequency standards",
            "b_A for constants and masses, Delta_tau_n",
            "zero only if material standards and time generator share e_obs",
            "blocked",
        ),
        (
            "ARENA943_4_orbital_Newton",
            "Newton/source normalization",
            "Delta_W_support,partial_v kappa,Delta_tau_n",
            "zero only if source support and orbital readout are the same Hilbert object",
            "blocked",
        ),
        (
            "ARENA943_5_local_GR",
            "full local GR reduction",
            "all frame/coupling residuals plus R_glue and PPN stability",
            "not claimable until selector/frame/coupling, same-worldtube, and PPN gates all close",
            "blocked",
        ),
    ]
    return [
        {
            "arena_id": arena_id,
            "arena": arena,
            "active_residuals": active_residuals,
            "pass_condition": pass_condition,
            "current_status": current_status,
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        }
        for arena_id, arena, active_residuals, pass_condition, current_status in specs
    ]


def decisions() -> list[dict[str, str]]:
    return [
        {
            "decision_id": "DEC943_0_best_route",
            "decision": "quotient_observed_coframe_descent_selected",
            "reason": "OCF623 shows uniqueness is overkill; if e_obs factors through q, vertical frame leakage vanishes by chain rule",
            "consequence": "next proof should target e_obs=Obs_e(q(Phi)) and S_matter[e_obs,psi_i,theta_A] as parent-owned",
            "next_action": "944-Y5-R10-quotient-observed-coframe-descent-proof-or-frame-leak-source-bounds.md",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "decision_id": "DEC943_1_current_verdict",
            "decision": "single_observed_coframe_not_parent_signed",
            "reason": "PAC537_1, WG510_1, SC0, PMC622_2, PAL703_2, and MCD716_6 remain conditional/not signed",
            "consequence": "Delta_frame_source, Delta_worldtube_domain, b_g, b_dis, b_A, and q_nonH remain active",
            "next_action": "build quotient-descent proof attempt before numeric local bound rows",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "decision_id": "DEC943_2_residual_policy",
            "decision": "finite_frame_leaks_must_be_retained_not_hidden",
            "reason": "no-shadow-frame gate says anything that changes rods, clocks, masses, charges, or free fall is observable",
            "consequence": "representative Weyl/disformal/mass channels are either quotient-owned, theorem-zero, or source-backed residuals",
            "next_action": "if 944 fails, source first b_g/b_A residual bound pack",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
    ]


def claim_gates() -> list[dict[str, str]]:
    return [
        {
            "gate_id": "CGATE943_0_coframe_descent",
            "claim": "ordinary matter sees only e_obs=Obs_e(q(Phi))",
            "blocker": "parent quotient/coframe functor not signed in current corpus",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "gate_id": "CGATE943_1_matter_coupling",
            "claim": "S_matter=S_matter[e_obs,psi_i,theta_A] for all ordinary matter",
            "blocker": "universal matter functor and constants/mass descent remain unsigned",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "gate_id": "CGATE943_2_frame_leak_zero",
            "claim": "Delta_frame_source=b_g=b_dis=b_A=q_nonH=0",
            "blocker": "conditional zero theorem lacks parent-owned descent/no-shadow signature",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "gate_id": "CGATE943_3_worldtube_selector",
            "claim": "W_source=supp(J_H[tau]) is parent-owned",
            "blocker": "same observed coframe, tau/n lock, and support-frame equivalence remain unsigned",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "gate_id": "CGATE943_4_local_GR",
            "claim": "Newton/local-GR/PPN branch is derived",
            "blocker": "coframe/coupling gate, same-worldtube glue, measured-GM calibration, and PPN stability remain open",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
    ]


def next_target() -> list[dict[str, str]]:
    return [
        {
            "next_target": "944-Y5-R10-quotient-observed-coframe-descent-proof-or-frame-leak-source-bounds.md",
            "objective": "prove e_obs=Obs_e(q(Phi)) and S_matter[e_obs,psi_i,theta_A] from the parent quotient/matter functor, or demote frame leaks to source-backed b_g/b_dis/b_A/q_nonH rows",
            "include": "q:Phi->Q_obs, Dq(v)=0, Obs_e functor, local Lorentz gauge separation, constants/mass descent, no-shadow-frame rule, first frame-leak residual rows",
            "exclude": "assuming uniqueness when quotient descent is enough, hiding representative Weyl/disformal channels, declaring local GR, beta pass claim, GitHub action, formalization-workbench edits",
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
    contract_rows: list[dict[str, str]],
    derivation_rows: list[dict[str, str]],
    residual_rows: list[dict[str, str]],
    arena_rows: list[dict[str, str]],
    decision_rows: list[dict[str, str]],
    claim_rows: list[dict[str, str]],
    target_rows: list[dict[str, str]],
) -> list[dict[str, str]]:
    rows = []

    def add(check_id: str, passed: bool, detail: str) -> None:
        rows.append({"check_id": check_id, "result": "pass" if passed else "fail", "detail": detail, "generated_utc": stamp()})

    prior = read_csv(OUT / "P8_Y5_BRR545_942_VALIDATION.csv")
    prior_clean = prior and all(row.get("result") == "pass" for row in prior)
    sources_ok = all(row["exists"] == "true" and row["needle_found"] == "true" for row in sources)
    descent_selected = any(row["decision_id"] == "DEC943_0_best_route" and row["decision"] == "quotient_observed_coframe_descent_selected" for row in decision_rows)
    contract_unsigned = any(row["contract_id"] == "CFC943_7_contract_verdict" and row["current_status"] == "contract_exact_but_unsigned" for row in contract_rows)
    conditional_derivation = any(row["derivation_id"] == "DER943_6_verdict" and row["derivation_status"] == "selected_as_next_derivation_target" for row in derivation_rows)
    residuals_blocked = residual_rows and all(row["score_ready"] == "false" and row["claim_allowed"] == "false" for row in residual_rows)
    arenas_blocked = arena_rows and all(row["current_status"] == "blocked" and row["claim_allowed"] == "false" for row in arena_rows)
    decisions_nonclaim = all(row["valid_for_claim"] == "false" for row in decision_rows)
    claims_false = all(row["claim_allowed"] == "false" and row["valid_for_claim"] == "false" for row in claim_rows)
    next_selected = any(row["next_target"].startswith("944-Y5-R10-quotient-observed-coframe") for row in target_rows)
    no_claims = all(
        row.get("valid_for_claim") == "false"
        for row in sources + contract_rows + derivation_rows + residual_rows + arena_rows + decision_rows + claim_rows + target_rows
    )
    formalization_changed = formalization_changed_after_start()

    add("V943_0_sources_exist_and_needles", sources_ok, "all 943 source paths exist and needles are present" if sources_ok else "missing source path or needle")
    add("V943_1_prior_942_clean", prior_clean, "P8_Y5_BRR545_942_VALIDATION.csv clean")
    add("V943_2_quotient_descent_selected", descent_selected, "quotient observed-coframe descent selected as best route")
    add("V943_3_contract_unsigned", contract_unsigned, "exact coframe/coupling contract remains unsigned")
    add("V943_4_derivation_conditional", conditional_derivation, "conditional derivation path retained without promotion")
    add("V943_5_residual_rows_blocked", residuals_blocked, "frame/coupling residual rows remain non-scoreable")
    add("V943_6_local_arenas_blocked", arenas_blocked, "all local arenas remain blocked until descent or residuals are sourced")
    add("V943_7_decisions_nonclaim", decisions_nonclaim, "decision ledger remains nonclaim")
    add("V943_8_claim_gates_false", claims_false, "all claim gates remain false")
    add("V943_9_next_target_selected", next_selected, "944 quotient-descent target selected")
    add("V943_10_no_claims_promoted", no_claims, "all generated rows are valid_for_claim=false")
    add("V943_11_formalization_workbench_untouched", formalization_changed == 0, f"formalization_changed_after_start={formalization_changed}")
    add("V943_12_validation_rows_ready", True, "validation table constructed")
    return rows


def write_doc(
    sources: list[dict[str, str]],
    contract_rows: list[dict[str, str]],
    derivation_rows: list[dict[str, str]],
    residual_rows: list[dict[str, str]],
    arena_rows: list[dict[str, str]],
    decision_rows: list[dict[str, str]],
    claim_rows: list[dict[str, str]],
    target_rows: list[dict[str, str]],
    validation_rows: list[dict[str, str]],
) -> None:
    text = f"""# 943 - Y5/R10 Single Observed Coframe Matter Coupling Contract Or Frame Residual Source Pack

Generated: `{stamp()}`

Status: `Y5_R10_943_quotient_observed_coframe_descent_selected_contract_exact_but_unsigned_frame_residual_pack_built_nonclaim`

Claim ceiling: `coframe_coupling_gate_only_no_frame_leak_zero_no_worldtube_selector_claim_no_local_GR_pass`

## Result

943 sharpens the coupling problem. The clean route is not to demand a mystical unique metric. The cleaner, less fragile route is quotient descent:

```text
q: Phi -> Q_obs,
Dq(v) = 0,
e_obs(Phi) = Obs_e(q(Phi)),
S_matter = sum_A S_A[psi_A, e_obs, omega[e_obs], theta_A].
```

Then for any vertical/representative direction `v`,

```text
Lie_v e_obs = D Obs_e[Dq(v)] = 0,
Lie_v S_matter = 0,
J_v = delta S_matter/delta v = 0.
```

That would make ordinary matter blind to representative-frame leakage, fix the Hilbert source current in one observed coframe, and support the 942 selector theorem `W_source=supp(J_H[tau])`.

But the current corpus does **not** parent-sign that descent. Existing rows say the right contract is written, not proved: `PAC537_1`, `WG510_1`, `SC0`, `PMC622_2`, `PAL703_2`, and `MCD716_6` are still conditional/not signed. So no local-GR, beta, R10, WEP, clock, or orbital claim is promoted.

The honest fallback is to retain every possible frame/coupling leak:

```text
b_g, b_dis, b_A, partial_v kappa, Delta_tau_n, Delta_W_support, q_nonH.
```

Those are now the source-ready residual rows if the next quotient-descent proof attempt fails.

## Source Register

{md_table(sources, ["source_id", "path", "role", "needle_found", "valid_for_claim"])}

## Coframe Coupling Contract

{md_table(contract_rows, ["contract_id", "required_clause", "mathematical_form", "current_status", "claim_allowed"])}

## Derivation Attempt

{md_table(derivation_rows, ["derivation_id", "statement", "mathematical_form", "derivation_status", "gap"])}

## Frame Residual Source Pack

{md_table(residual_rows, ["row_id", "symbol", "definition", "current_status", "observable_link", "score_ready"])}

## Arena Gate Map

{md_table(arena_rows, ["arena_id", "arena", "active_residuals", "pass_condition", "current_status"])}

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
    contract_rows = coframe_contract()
    derivation_rows = derivation_attempt()
    residual_rows = frame_residual_source_pack()
    arena_rows = arena_gate_map()
    decision_rows = decisions()
    claim_rows = claim_gates()
    target_rows = next_target()
    validation_rows = validation(sources, contract_rows, derivation_rows, residual_rows, arena_rows, decision_rows, claim_rows, target_rows)

    output_specs = [
        (
            OUT / "P8_Y5_R10_943_SOURCE_REGISTER.csv",
            sources,
            ["source_id", "path", "absolute_path", "role", "needle", "exists", "needle_found", "valid_for_claim", "generated_utc"],
        ),
        (
            OUT / "P8_Y5_R10_943_COFRAME_COUPLING_CONTRACT.csv",
            contract_rows,
            ["contract_id", "required_clause", "mathematical_form", "why_needed", "current_status", "parent_signed", "claim_allowed", "valid_for_claim", "generated_utc"],
        ),
        (
            OUT / "P8_Y5_R10_943_DERIVATION_ATTEMPT.csv",
            derivation_rows,
            ["derivation_id", "statement", "mathematical_form", "derivation_status", "gap", "claim_allowed", "valid_for_claim", "generated_utc"],
        ),
        (
            OUT / "P8_Y5_R10_943_FRAME_RESIDUAL_SOURCE_PACK.csv",
            residual_rows,
            ["row_id", "symbol", "definition", "required_columns", "current_status", "observable_link", "score_ready", "claim_allowed", "valid_for_claim", "generated_utc"],
        ),
        (
            OUT / "P8_Y5_R10_943_ARENA_GATE_MAP.csv",
            arena_rows,
            ["arena_id", "arena", "active_residuals", "pass_condition", "current_status", "claim_allowed", "valid_for_claim", "generated_utc"],
        ),
        (
            OUT / "P8_Y5_R10_943_DECISION_LEDGER.csv",
            decision_rows,
            ["decision_id", "decision", "reason", "consequence", "next_action", "valid_for_claim", "generated_utc"],
        ),
        (
            OUT / "P8_Y5_R10_943_CLAIM_GATE.csv",
            claim_rows,
            ["gate_id", "claim", "blocker", "claim_allowed", "valid_for_claim", "generated_utc"],
        ),
        (
            OUT / "P8_Y5_R10_943_NEXT_TARGET.csv",
            target_rows,
            ["next_target", "objective", "include", "exclude", "valid_for_claim", "generated_utc"],
        ),
        (
            OUT / "P8_Y5_BRR545_943_VALIDATION.csv",
            validation_rows,
            ["check_id", "result", "detail", "generated_utc"],
        ),
    ]

    for path, rows, fieldnames in output_specs:
        write_csv(path, rows, fieldnames)

    ensure_csv_roundtrip([path for path, _rows, _fieldnames in output_specs])
    write_doc(sources, contract_rows, derivation_rows, residual_rows, arena_rows, decision_rows, claim_rows, target_rows, validation_rows)

    failures = [row for row in validation_rows if row["result"] != "pass"]
    if failures:
        raise SystemExit(f"validation failed: {failures}")

    print("Y5_R10_943_quotient_observed_coframe_descent_selected_contract_exact_but_unsigned_frame_residual_pack_built_nonclaim")
    print(f"wrote {DOC}")
    print("next target: 944-Y5-R10-quotient-observed-coframe-descent-proof-or-frame-leak-source-bounds.md")


if __name__ == "__main__":
    main()

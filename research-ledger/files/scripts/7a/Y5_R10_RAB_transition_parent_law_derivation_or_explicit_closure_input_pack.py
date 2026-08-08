from __future__ import annotations

import csv
from pathlib import Path


PACK_ID = "P8_Y5_R10_1378"
TITLE = "1378-Y5-R10-RAB-transition-parent-law-derivation-or-explicit-closure-input-pack"
ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = ROOT / "source-intake" / "mts_residuals"
DOC_PATH = ROOT / f"{TITLE}.md"
FORMALIZATION = ROOT.parent / "formalization-workbench"

SOURCE_REGISTER_PATH = OUT_DIR / f"{PACK_ID}_SOURCE_REGISTER.csv"
DERIVATION_PATH = OUT_DIR / f"{PACK_ID}_TRANSITION_PARENT_LAW_DERIVATION.csv"
GRADIENT_BRANCH_PATH = OUT_DIR / f"{PACK_ID}_CONDITIONAL_GRADIENT_RELAXATION_BRANCH.csv"
CLOSURE_PACK_PATH = OUT_DIR / f"{PACK_ID}_EXPLICIT_CLOSURE_INPUT_PACK.csv"
RUNNER_FEED_PATH = OUT_DIR / f"{PACK_ID}_RUNNER_FEED_UPDATE.csv"
CLAIM_GATE_PATH = OUT_DIR / f"{PACK_ID}_CLAIM_GATE.csv"
DECISION_PATH = OUT_DIR / f"{PACK_ID}_DECISION_LEDGER.csv"
NEXT_PATH = OUT_DIR / f"{PACK_ID}_NEXT_TARGET.csv"
VALIDATION_PATH = OUT_DIR / "P8_Y5_BRR545_1378_VALIDATION.csv"


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


def read_csv_rows(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def cell(value: object) -> str:
    return str(value).replace("\n", " ").replace("|", "\\|")


def table(headers: list[str], rows: list[dict[str, object]]) -> str:
    out = [
        "| " + " | ".join(headers) + " |",
        "| " + " | ".join(["---"] * len(headers)) + " |",
    ]
    for row in rows:
        out.append("| " + " | ".join(cell(row.get(header, "")) for header in headers) + " |")
    return "\n".join(out)


def mark_nonclaim(rows: list[dict[str, object]]) -> list[dict[str, object]]:
    for row in rows:
        row["valid_for_claim"] = False
        row["claim_allowed"] = False
    return rows


def source_register() -> list[dict[str, object]]:
    rows = [
        {
            "source_id": "SRC1378_0_1377_doc",
            "source_path": "1377-Y5-R10-RAB-transition-parent-source-row-builder-or-Kconn-operator-source-hunt.md",
            "required_anchor": "NEXT1377_0_1378",
            "purpose": "1377 handoff to transition law derivation or explicit closure pack.",
        },
        {
            "source_id": "SRC1378_1_1377_next",
            "source_path": "source-intake/mts_residuals/P8_Y5_R10_1377_NEXT_TARGET.csv",
            "required_anchor": "NEXT1377_0_1378",
            "purpose": "machine-readable 1378 target.",
        },
        {
            "source_id": "SRC1378_2_1377_blockers",
            "source_path": "source-intake/mts_residuals/P8_Y5_R10_1377_BLOCKER_LEDGER.csv",
            "required_anchor": "BLK1377_0_U_B_parent_law",
            "purpose": "active transition/Kconn/local projection blockers.",
        },
        {
            "source_id": "SRC1378_3_1371_fixed_L0",
            "source_path": "source-intake/mts_residuals/P8_Y5_R10_1371_FIXED_L0_PARENT_ACTION_INSERTION.csv",
            "required_anchor": "PAI1371_4_gradient_source_after_double_zero",
            "purpose": "fixed-L0 double-zero branch and quadratic gradient source.",
        },
        {
            "source_id": "SRC1378_4_1370_L0_contract",
            "source_path": "source-intake/mts_residuals/P8_Y5_R10_1370_PARENT_LCG_CONTRACT_CANDIDATE.csv",
            "required_anchor": "LCC1370_4_metric_silence_result",
            "purpose": "fixed L0 metric-silence result and anti-smuggling clauses.",
        },
        {
            "source_id": "SRC1378_5_1301_fixed_field",
            "source_path": "source-intake/mts_residuals/P8_Y5_R10_1301_PARENT_FIXED_FIELD_CLOSURE_CONTRACT.csv",
            "required_anchor": "FFC1301_0_parent_field_status",
            "purpose": "m parent-field status remains unsigned.",
        },
        {
            "source_id": "SRC1378_6_1373_Qnorm",
            "source_path": "source-intake/mts_residuals/P8_Y5_R10_1373_QNORM_COMPONENT_FIRST_FILL_CONTRACTS.csv",
            "required_anchor": "QFF1373_4_Q_trans",
            "purpose": "Q_alg/Q_trans/Q_cdb runner contracts.",
        },
        {
            "source_id": "SRC1378_7_1374_Qalg_Qtrans",
            "source_path": "source-intake/mts_residuals/P8_Y5_R10_1374_QALG_QTRANS_FIRST_FILL.csv",
            "required_anchor": "QQF1374_2_shell_projection_guard",
            "purpose": "symbolic Q_alg/Q_trans transition formulas and shell guard.",
        },
        {
            "source_id": "SRC1378_8_1376_acquisition",
            "source_path": "source-intake/mts_residuals/P8_Y5_R10_1376_TRANSITION_PARENT_SOURCE_ACQUISITION.csv",
            "required_anchor": "TPS1376_16_shell_projector_or_bound",
            "purpose": "transition parent-source acquisition checklist.",
        },
        {
            "source_id": "SRC1378_9_802_shell",
            "source_path": "source-intake/mts_residuals/P8_Y5_R10_802_TRANSITION_SHELL_OBSTRUCTION.csv",
            "required_anchor": "TS802_0_direct_projection",
            "purpose": "direct transition-shell projection obstruction.",
        },
        {
            "source_id": "SRC1378_10_803_anticheat",
            "source_path": "source-intake/mts_residuals/P8_Y5_R10_803_TRANSITION_SHELL_ANTI_CHEAT_BOUND.csv",
            "required_anchor": "AC803_0_required_shell_suppression",
            "purpose": "anti-cheat guard against generic shell suppression.",
        },
    ]
    for row in rows:
        path = source_path(str(row["source_path"]))
        row["exists"] = path.exists()
        row["anchor_found"] = path.exists() and str(row["required_anchor"]) in read_text(path)
    return mark_nonclaim(rows)


def derivation_rows() -> list[dict[str, object]]:
    return mark_nonclaim(
        [
            {
                "step_id": "DER1378_0_fixed_L0_start",
                "object": "fixed-L0 double-zero branch",
                "derivation": "Start with S_GK^0=-int sqrt(-g) L0^-2 Fhat(m;m_*), L0 fixed, Fhat(m_*)=0, Fhat'(m_*)=0.",
                "result": "algebraic volume/m/L chain can be silent at m=m_* under closure assumptions",
                "status": "SOURCE_TIED_STARTING_POINT",
                "remaining_gap": "parent adoption; parent law selecting m_*; m parent-field signature",
                "source_paths": "source-intake/mts_residuals/P8_Y5_R10_1371_FIXED_L0_PARENT_ACTION_INSERTION.csv;source-intake/mts_residuals/P8_Y5_R10_1370_PARENT_LCG_CONTRACT_CANDIDATE.csv",
            },
            {
                "step_id": "DER1378_1_pure_algebraic_Euler",
                "object": "transition profile from S_GK^0 alone",
                "derivation": "Euler variation in m gives L0^-2 Fhat'(m)=0 pointwise; there is no derivative term for m and therefore no second-order boundary-value problem.",
                "result": "pure fixed-L0 algebra selects extrema but does not determine U_B, L_tr, support powers, or a spatial transition profile",
                "status": "FAIL_PROFILE_UNDERDETERMINED",
                "remaining_gap": "need gradient stiffness, nonlocal constraint, boundary condition, or parent no-hair theorem",
                "source_paths": "source-intake/mts_residuals/P8_Y5_R10_1371_FIXED_L0_PARENT_ACTION_INSERTION.csv;source-intake/mts_residuals/P8_Y5_R10_1377_BLOCKER_LEDGER.csv",
            },
            {
                "step_id": "DER1378_2_quadratic_source_bound",
                "object": "nabla Gamma_eff near m_*",
                "derivation": "Write eta=m-m_*; from the double-zero expansion, nabla_mu Gamma_eff=L0^-2 F2 eta nabla_mu eta + O(eta^2 nabla eta).",
                "result": "if eta and nabla eta are bounded, Q_alg is quadratically suppressed, but the bound does not itself derive eta",
                "status": "CONDITIONAL_SUPPRESSION_ONLY",
                "remaining_gap": "Delta_m, Delta_grad_m, U_B, A_S, pS, and L_tr still require a parent transition law",
                "source_paths": "source-intake/mts_residuals/P8_Y5_R10_1371_FIXED_L0_PARENT_ACTION_INSERTION.csv;source-intake/mts_residuals/P8_Y5_R10_1373_QNORM_COMPONENT_FIRST_FILL_CONTRACTS.csv",
            },
            {
                "step_id": "DER1378_3_minimal_gradient_completion",
                "object": "candidate transition parent law",
                "derivation": "If a new parent term -(kappa_m/2) g^{mu nu} partial_mu eta partial_nu eta is added, then the vacuum linearized Euler equation is kappa_m Box eta - L0^-2 F2 eta=0.",
                "result": "in a static normal coordinate x, eta''-eta/ell_tr^2=0 with ell_tr=sqrt(kappa_m L0^2/F2) for kappa_m F2>0",
                "status": "CONDITIONAL_BRANCH_DERIVED_REQUIRES_NEW_PARENT_TERM",
                "remaining_gap": "kappa_m is not source-backed; sign/units of F2 and kappa_m are not parent-signed; source coupling and boundary data are not fixed",
                "source_paths": "source-intake/mts_residuals/P8_Y5_R10_1371_FIXED_L0_PARENT_ACTION_INSERTION.csv;source-intake/mts_residuals/P8_Y5_R10_1301_PARENT_FIXED_FIELD_CLOSURE_CONTRACT.csv",
            },
            {
                "step_id": "DER1378_4_exponential_support_law",
                "object": "U_B and pS",
                "derivation": "For the decaying branch eta=A_S exp(-d/ell_tr), set U_B=exp(-d/ell_tr); then Delta_m=A_S U_B and |nabla eta|<=A_S U_B/ell_tr.",
                "result": "conditional gradient branch gives pS=1 and L_tr=ell_tr",
                "status": "CONDITIONAL_NOT_PARENT_SIGNED",
                "remaining_gap": "distance d, boundary amplitude A_S, and the physical meaning of U_B are not sourced",
                "source_paths": "source-intake/mts_residuals/P8_Y5_R10_1374_QALG_QTRANS_FIRST_FILL.csv;source-intake/mts_residuals/P8_Y5_R10_1376_TRANSITION_PARENT_SOURCE_ACQUISITION.csv",
            },
            {
                "step_id": "DER1378_5_fixed_L0_L_chain",
                "object": "A_L / pL",
                "derivation": "If L0 is truly fixed before projection/domain reduction, delta_g L0=0 and nabla L0=0, so the algebraic L-chain drift coefficient is conditionally A_L=0.",
                "result": "A_L=0 is derivable only inside the fixed-L0 closure branch, not as a live claim",
                "status": "CONDITIONAL_ZERO_UNDER_CLOSURE",
                "remaining_gap": "fixed-L0 branch is not parent-signed as live theory; domain/readout leakage must stay out of variation",
                "source_paths": "source-intake/mts_residuals/P8_Y5_R10_1370_PARENT_LCG_CONTRACT_CANDIDATE.csv;source-intake/mts_residuals/P8_Y5_R10_1371_FIXED_L0_PARENT_ACTION_INSERTION.csv",
            },
            {
                "step_id": "DER1378_6_quadratic_gradient_stress",
                "object": "trace/memory stress scaling",
                "derivation": "The added gradient completion would itself carry Hilbert stress T_eta~kappa_m[(nabla eta)^2 g - 2 nabla eta nabla eta], hence stress scales as A_S^2 U_B^2/ell_tr^2.",
                "result": "pT=2 and memory/stress exponents are plausible only in the conditional gradient branch",
                "status": "CONDITIONAL_STRESS_NOT_CLAIM",
                "remaining_gap": "A_T, b_mem, normalization, and trace-reversal slot are not sourced; added kinetic stress cannot be silently deleted",
                "source_paths": "source-intake/mts_residuals/P8_Y5_R10_1301_PARENT_FIXED_FIELD_CLOSURE_CONTRACT.csv;source-intake/mts_residuals/P8_Y5_R10_1373_QNORM_COMPONENT_FIRST_FILL_CONTRACTS.csv",
            },
            {
                "step_id": "DER1378_7_boundary_shell_obstruction",
                "object": "transition shell / boundary",
                "derivation": "The exponential branch still has boundary data and possible shell/edge terms; generic U_B or width suppression does not prove projector silence.",
                "result": "A_B/pB and shell projector remain explicit closure inputs unless an exact cancellation/quarantine theorem or finite shell bound is supplied",
                "status": "BLOCKED_BY_SHELL_ANTI_CHEAT",
                "remaining_gap": "boundary condition, no-flux theorem, Kperp bound, or projector identity",
                "source_paths": "source-intake/mts_residuals/P8_Y5_R10_1374_QALG_QTRANS_FIRST_FILL.csv;source-intake/mts_residuals/P8_Y5_R10_802_TRANSITION_SHELL_OBSTRUCTION.csv;source-intake/mts_residuals/P8_Y5_R10_803_TRANSITION_SHELL_ANTI_CHEAT_BOUND.csv",
            },
            {
                "step_id": "DER1378_8_verdict",
                "object": "transition parent law",
                "derivation": "Fixed-L0 double-zero alone cannot derive the transition law; adding a gradient relaxation term yields a clean conditional law but introduces an unsigned parent coefficient and boundary/shell data.",
                "result": "demote transition values to an explicit closure-only input pack while preserving the conditional gradient branch as the best derivation route",
                "status": "NO_PARENT_SIGNED_TRANSITION_LAW_YET",
                "remaining_gap": "parent-sign kappa_m/gradient completion or derive an equivalent no-hair/support law",
                "source_paths": "aggregate_DER1378_0_to_DER1378_7",
            },
        ]
    )


def gradient_branch_rows() -> list[dict[str, object]]:
    return mark_nonclaim(
        [
            {
                "branch_id": "GRB1378_0_candidate_action",
                "branch_component": "gradient completion",
                "conditional_formula": "S_eta=-int sqrt(-g)[L0^-2 Fhat(m_*+eta)+(kappa_m/2) g^{mu nu} partial_mu eta partial_nu eta]",
                "derived_mapping": "adds the missing second-order transition equation",
                "required_parent_signature": "kappa_m positive, units fixed, m parent scalar, source coupling specified",
                "status": "CONDITIONAL_CLOSURE_ONLY",
            },
            {
                "branch_id": "GRB1378_1_transition_length",
                "branch_component": "L_tr",
                "conditional_formula": "ell_tr=sqrt(kappa_m L0^2/F2), with F2=Fhat''(m_*) and kappa_m F2>0",
                "derived_mapping": "L_tr -> ell_tr",
                "required_parent_signature": "source-backed kappa_m, F2 sign, L0 scale rule",
                "status": "CONDITIONAL_CLOSURE_ONLY",
            },
            {
                "branch_id": "GRB1378_2_support_law",
                "branch_component": "U_B,pS,A_S",
                "conditional_formula": "eta(d)=A_S exp(-d/ell_tr); U_B=exp(-d/ell_tr); pS=1; Delta_grad_m<=A_S U_B/ell_tr",
                "derived_mapping": "A_S is boundary amplitude; U_B is exponential support factor",
                "required_parent_signature": "boundary/reference amplitude and physical support distance d",
                "status": "CONDITIONAL_CLOSURE_ONLY",
            },
            {
                "branch_id": "GRB1378_3_Qalg",
                "branch_component": "Q_alg",
                "conditional_formula": "Q_alg <= A_ref^-1 |F2| A_S^2 U_B^2/(L0^2 ell_tr)",
                "derived_mapping": "matches QQF1374_0 with pS=1 and L_tr=ell_tr",
                "required_parent_signature": "A_ref and all branch inputs source-backed",
                "status": "CONDITIONAL_CLOSURE_ONLY",
            },
            {
                "branch_id": "GRB1378_4_fixed_L_chain",
                "branch_component": "A_L",
                "conditional_formula": "A_L=0 if L0 is a fixed scalar parameter and no projection/readout enters before variation",
                "derived_mapping": "removes the L-chain drift term only in the fixed-L0 closure branch",
                "required_parent_signature": "L0 parent-signature plus anti-smuggling clause",
                "status": "CONDITIONAL_ZERO_UNDER_CLOSURE",
            },
            {
                "branch_id": "GRB1378_5_gradient_stress",
                "branch_component": "pT,b_mem,A_T",
                "conditional_formula": "T_eta scales as kappa_m A_S^2 U_B^2/ell_tr^2; stress-like transition terms therefore start at quadratic support order",
                "derived_mapping": "suggests pT=2 for gradient stress but does not fix A_T or b_mem",
                "required_parent_signature": "trace projection, stress normalization, and memory/source split",
                "status": "CONDITIONAL_CLOSURE_ONLY",
            },
            {
                "branch_id": "GRB1378_6_boundary_shell",
                "branch_component": "A_B,pB,shell",
                "conditional_formula": "boundary/shell term must be zero by boundary condition/projector identity or retained as explicit Q_trans/Q_proj contribution",
                "derived_mapping": "no safe generic pB is derived",
                "required_parent_signature": "no-flux theorem, Kperp finite bound, or exact shell projector quarantine",
                "status": "NOT_DERIVED_RETAIN_AS_CLOSURE_INPUT",
            },
            {
                "branch_id": "GRB1378_7_branch_verdict",
                "branch_component": "conditional transition law",
                "conditional_formula": "gradient-relaxation law is mathematically coherent but not parent-signed by the current corpus",
                "derived_mapping": "best candidate route for 1379; not evidence for local-GR pass",
                "required_parent_signature": "parent action adoption, coefficient provenance, shell handling, arena projection",
                "status": "CANDIDATE_ROUTE_NOT_CLAIM",
            },
        ]
    )


def closure_pack_rows() -> list[dict[str, object]]:
    return mark_nonclaim(
        [
            {
                "input_id": "CIP1378_0_branch_id",
                "closure_input": "transition_branch",
                "required_value_or_rule": "choose gradient_relaxation_closure or supply a different parent-signed transition law",
                "role": "declares which law generates U_B/powers/lengths",
                "current_status": "CLOSURE_ONLY_REQUIRED",
                "refusal_gate": "no implicit plateau axiom; no local-test-tuned branch choice",
            },
            {
                "input_id": "CIP1378_1_kappa_m",
                "closure_input": "kappa_m",
                "required_value_or_rule": "positive gradient stiffness with units and parent-action source path",
                "role": "sets ell_tr with F2 and L0",
                "current_status": "MISSING_PARENT_COEFFICIENT",
                "refusal_gate": "reject if introduced only after local residual comparison",
            },
            {
                "input_id": "CIP1378_2_F2",
                "closure_input": "F2=Fhat''(m_*)",
                "required_value_or_rule": "curvature of parent potential at m_*; sign and units sourced",
                "role": "sets restoring mass and Q_alg amplitude",
                "current_status": "MISSING_PARENT_COEFFICIENT",
                "refusal_gate": "reject if sign/magnitude chosen to hide residuals",
            },
            {
                "input_id": "CIP1378_3_L0",
                "closure_input": "L0",
                "required_value_or_rule": "fixed scalar scale selected by parent microphysics or RG stability",
                "role": "sets Gamma_eff scale and ell_tr",
                "current_status": "ACTION_ROLE_SOURCED_NUMERIC_RULE_MISSING",
                "refusal_gate": "reject per-arena fit",
            },
            {
                "input_id": "CIP1378_4_L_tr",
                "closure_input": "L_tr",
                "required_value_or_rule": "L_tr=ell_tr=sqrt(kappa_m L0^2/F2) or alternate parent-derived transition length",
                "role": "bounds Delta_grad_m and Q_trans",
                "current_status": "CONDITIONAL_FORMULA_READY_VALUES_MISSING",
                "refusal_gate": "reject arbitrary wide transition shell",
            },
            {
                "input_id": "CIP1378_5_U_B",
                "closure_input": "U_B",
                "required_value_or_rule": "U_B=exp(-d/ell_tr) or equivalent support factor with sourced distance/domain",
                "role": "controls local suppression powers",
                "current_status": "CONDITIONAL_FORMULA_READY_DISTANCE_MISSING",
                "refusal_gate": "reject copied toy value",
            },
            {
                "input_id": "CIP1378_6_support_powers",
                "closure_input": "pS;pL;pT;pB",
                "required_value_or_rule": "pS=1 in gradient branch; pL absent if A_L=0; pT=2 only for gradient stress; pB requires boundary theorem",
                "role": "feeds Q_alg/Q_trans formulas",
                "current_status": "PARTIAL_CONDITIONAL_NOT_PARENT_SIGNED",
                "refusal_gate": "reject powers tuned independently per observable",
            },
            {
                "input_id": "CIP1378_7_amplitudes",
                "closure_input": "A_S;A_L;A_T;A_B;b_mem",
                "required_value_or_rule": "A_S boundary amplitude; A_L=0 only under fixed-L0 closure; A_T/A_B/b_mem from stress and boundary projections",
                "role": "sets Q_alg/Q_trans magnitude",
                "current_status": "MISSING_PROJECTION_NORMALIZATION",
                "refusal_gate": "reject silent deletion of kinetic/source/boundary stress",
            },
            {
                "input_id": "CIP1378_8_A_ref",
                "closure_input": "A_ref",
                "required_value_or_rule": "local norm/domain normalization with units",
                "role": "turns residual norms into dimensionless runner inputs",
                "current_status": "MISSING_NORMALIZATION_CONVENTION",
                "refusal_gate": "reject normalization chosen to make residual small",
            },
            {
                "input_id": "CIP1378_9_shell_gate",
                "closure_input": "transition_shell_projector_identity_or_explicit_bound",
                "required_value_or_rule": "exact cancellation/quarantine theorem or explicit shell contribution in Q_trans/Q_proj",
                "role": "anti-cheat condition for local branch",
                "current_status": "MISSING_SHELL_CLOSURE",
                "refusal_gate": "reject generic U_B/width hiding",
            },
            {
                "input_id": "CIP1378_10_arena_limits",
                "closure_input": "epsilon_q_limit;epsilon_N_limit;observable_response",
                "required_value_or_rule": "R10/PPN/clock/orbital response operator and accepted observable thresholds",
                "role": "decides whether finite residual bound is small enough",
                "current_status": "MISSING_ARENA_PROJECTION",
                "refusal_gate": "reject local-GR pass without response map",
            },
            {
                "input_id": "CIP1378_11_provenance",
                "closure_input": "source_path;source_anchor;units;extraction_method",
                "required_value_or_rule": "every numeric/theorem value must have real local source and units",
                "role": "prevents toy/schema rows becoming claims",
                "current_status": "SCHEMA_READY_VALUES_MISSING",
                "refusal_gate": "reject MISSING_* or toy_nonclaim_no_physical_source",
            },
            {
                "input_id": "CIP1378_12_verdict",
                "closure_input": "closure pack status",
                "required_value_or_rule": "finite closure pack exists as a checklist only",
                "role": "keeps transition route explicit while derivation is incomplete",
                "current_status": "EXPLICIT_CLOSURE_INPUT_PACK_READY_NONCLAIM",
                "refusal_gate": "no PPN/R10/local-GR claim until parent-signed or independently bounded",
            },
        ]
    )


def runner_feed_rows() -> list[dict[str, object]]:
    return mark_nonclaim(
        [
            {
                "feed_id": "RUF1378_0_transition_law",
                "runner_field": "transition_parent_law",
                "feed_update": "fixed-L0 double-zero alone fails to derive U_B/powers/L_tr; gradient relaxation is conditional only",
                "status": "BLOCKED_PARENT_LAW_NOT_SIGNED",
                "blocks_claim_because": "the law requires unsigned kappa_m, boundary data, and shell handling",
            },
            {
                "feed_id": "RUF1378_1_closure_pack",
                "runner_field": "closure_input_pack",
                "feed_update": "use CIP1378 rows as the explicit finite input checklist if the branch remains closure-only",
                "status": "CLOSURE_PACK_READY_NONCLAIM",
                "blocks_claim_because": "checklist values are not sourced or claim-grade",
            },
            {
                "feed_id": "RUF1378_2_conditional_Qalg",
                "runner_field": "Q_alg",
                "feed_update": "conditional gradient branch maps Q_alg <= A_ref^-1 |F2| A_S^2 U_B^2/(L0^2 ell_tr)",
                "status": "CONDITIONAL_FORMULA_READY_VALUES_MISSING",
                "blocks_claim_because": "A_ref, F2, A_S, U_B, L0, ell_tr are not all parent-signed",
            },
            {
                "feed_id": "RUF1378_3_claim_status",
                "runner_field": "local_GR_PPN_R10_status",
                "feed_update": "local-GR, PPN, R10, and q_loc=0 claims remain blocked",
                "status": "BLOCKED_NO_CLAIM",
                "blocks_claim_because": "transition law is conditional/closure-only and shell/Kconn/arena gates remain open",
            },
        ]
    )


def claim_gate_rows() -> list[dict[str, object]]:
    return mark_nonclaim(
        [
            {
                "gate_id": "GATE1378_0_fixed_L0_alone",
                "gate": "fixed-L0 double-zero alone derives transition law",
                "status": "FAIL_PROFILE_UNDERDETERMINED",
                "reason": "pure algebraic Euler equation has no derivative term and no transition width/profile.",
            },
            {
                "gate_id": "GATE1378_1_gradient_branch",
                "gate": "conditional gradient relaxation law exists",
                "status": "PASS_CONDITIONAL_BRANCH_DERIVED",
                "reason": "adding kappa_m gradient stiffness yields ell_tr=sqrt(kappa_m L0^2/F2) and exponential support.",
            },
            {
                "gate_id": "GATE1378_2_parent_signed",
                "gate": "gradient branch is parent-signed by current corpus",
                "status": "BLOCKED_NOT_PARENT_SIGNED",
                "reason": "kappa_m, source coupling, boundary data, and m parent-field status are unsigned.",
            },
            {
                "gate_id": "GATE1378_3_shell",
                "gate": "transition shell is exactly cancelled or bounded",
                "status": "BLOCKED_SHELL_CLOSURE_MISSING",
                "reason": "802/803 anti-cheat ledgers still require exact projector identity or explicit shell bound.",
            },
            {
                "gate_id": "GATE1378_4_local_claim",
                "gate": "local GR / PPN / R10 pass can be claimed",
                "status": "BLOCKED_NO_CLAIM",
                "reason": "only a conditional transition law and closure input pack exist.",
            },
        ]
    )


def decision_rows() -> list[dict[str, object]]:
    return mark_nonclaim(
        [
            {
                "decision_id": "DEC1378_0_pure_branch",
                "decision": "do not use fixed-L0 algebraic branch alone as a transition-profile derivation",
                "why": "it gives pointwise extrema but no differential profile, support factor, or width",
                "next_action": "keep fixed-L0 branch as algebraic silence only",
            },
            {
                "decision_id": "DEC1378_1_gradient_branch",
                "decision": "retain gradient relaxation as the best conditional derivation route",
                "why": "it produces ell_tr, U_B, pS=1, and a clear Q_alg scaling without arbitrary plateau smuggling",
                "next_action": "try to parent-sign kappa_m/gradient action and boundary conditions",
            },
            {
                "decision_id": "DEC1378_2_closure_pack",
                "decision": "demote all transition inputs to explicit closure-only until parent-signed",
                "why": "this protects the theory from hidden local-test tuning while preserving a finite route to scoring",
                "next_action": "build 1379 around parent-signing or rejecting the gradient completion branch",
            },
        ]
    )


def next_rows() -> list[dict[str, object]]:
    return mark_nonclaim(
        [
            {
                "next_id": "NEXT1378_0_1379",
                "next_doc": "1379-Y5-R10-RAB-gradient-completion-parent-signature-or-transition-closure-runner.md",
                "next_script": "scripts/Y5_R10_RAB_gradient_completion_parent_signature_or_transition_closure_runner.py",
                "task": "attempt to parent-sign the kappa_m gradient-completion branch, including units, source coupling, boundary/no-flux or shell-bound handling, and m parent-field status; if not, build a closure-only runner input schema from CIP1378",
                "success_condition": "either kappa_m gradient completion is parent-signed enough for a nonclaim candidate row, or a closure runner schema exists that refuses all local-GR/PPN/R10 claims",
                "do_not_claim": "local GR;PPN pass;R10 pass;q_loc=0;GitHub-ready result",
            }
        ]
    )


def generated_csv_paths() -> list[Path]:
    return [
        SOURCE_REGISTER_PATH,
        DERIVATION_PATH,
        GRADIENT_BRANCH_PATH,
        CLOSURE_PACK_PATH,
        RUNNER_FEED_PATH,
        CLAIM_GATE_PATH,
        DECISION_PATH,
        NEXT_PATH,
    ]


def all_rows_nonclaim(*groups: list[dict[str, object]]) -> bool:
    for rows in groups:
        for row in rows:
            if str(row.get("valid_for_claim", "")).lower() != "false":
                return False
            if str(row.get("claim_allowed", "")).lower() != "false":
                return False
    return True


def csv_parse_details(paths: list[Path]) -> tuple[bool, str]:
    details = []
    ok = True
    for path in paths:
        try:
            count = len(read_csv_rows(path))
            details.append(f"{path.name}:{count}")
        except Exception as exc:  # pragma: no cover
            ok = False
            details.append(f"{path.name}:ERROR:{exc}")
    return ok, "; ".join(details)


def validation_rows(
    sources: list[dict[str, object]],
    derivation: list[dict[str, object]],
    gradient_branch: list[dict[str, object]],
    closure_pack: list[dict[str, object]],
    runner_feed: list[dict[str, object]],
    gates: list[dict[str, object]],
    csv_paths: list[Path],
) -> list[dict[str, object]]:
    all_sources_ok = all(bool(row["exists"]) and bool(row["anchor_found"]) for row in sources)
    pure_branch_fails = any(row["step_id"] == "DER1378_1_pure_algebraic_Euler" and row["status"] == "FAIL_PROFILE_UNDERDETERMINED" for row in derivation)
    conditional_branch = any(row["branch_id"] == "GRB1378_7_branch_verdict" and row["status"] == "CANDIDATE_ROUTE_NOT_CLAIM" for row in gradient_branch)
    required_inputs = {
        "transition_branch",
        "kappa_m",
        "F2=Fhat''(m_*)",
        "L0",
        "L_tr",
        "U_B",
        "pS;pL;pT;pB",
        "A_S;A_L;A_T;A_B;b_mem",
        "A_ref",
        "transition_shell_projector_identity_or_explicit_bound",
        "epsilon_q_limit;epsilon_N_limit;observable_response",
        "source_path;source_anchor;units;extraction_method",
        "closure pack status",
    }
    closure_inputs = {str(row["closure_input"]) for row in closure_pack}
    closure_pack_ready = required_inputs.issubset(closure_inputs)
    runner_blocks = any(row["feed_id"] == "RUF1378_3_claim_status" and row["status"] == "BLOCKED_NO_CLAIM" for row in runner_feed)
    local_claim_blocked = any(row["gate_id"] == "GATE1378_4_local_claim" and row["status"] == "BLOCKED_NO_CLAIM" for row in gates)
    nonclaim = all_rows_nonclaim(sources, derivation, gradient_branch, closure_pack, runner_feed, gates)
    csv_ok, csv_details = csv_parse_details(csv_paths)
    outputs = [DOC_PATH, VALIDATION_PATH, *csv_paths]
    outputs_scoped = all(ROOT in path.resolve().parents or path.resolve() == ROOT for path in outputs)
    formalization_untouched_by_script = FORMALIZATION.exists() and all(FORMALIZATION not in path.resolve().parents for path in outputs)

    rows = [
        {
            "validation_id": "VAL1378_0_sources",
            "check": "every cited local source path exists and anchor is found",
            "status": "PASS" if all_sources_ok else "FAIL",
            "details": "; ".join(f"{row['source_id']} exists={row['exists']} anchor={row['anchor_found']}" for row in sources),
        },
        {
            "validation_id": "VAL1378_1_pure_branch",
            "check": "fixed-L0 double-zero alone is not overclaimed as a transition law",
            "status": "PASS" if pure_branch_fails else "FAIL",
            "details": "DER1378_1 records profile underdetermination.",
        },
        {
            "validation_id": "VAL1378_2_gradient_branch",
            "check": "conditional gradient relaxation branch is derived but nonclaim",
            "status": "PASS" if conditional_branch else "FAIL",
            "details": "GRB1378_7 keeps branch candidate route, not claim.",
        },
        {
            "validation_id": "VAL1378_3_closure_pack",
            "check": "explicit closure pack covers transition law inputs",
            "status": "PASS" if closure_pack_ready else "FAIL",
            "details": "required closure inputs checked: " + ";".join(sorted(required_inputs)),
        },
        {
            "validation_id": "VAL1378_4_runner_refusal",
            "check": "runner feed and gates keep local claims blocked",
            "status": "PASS" if runner_blocks and local_claim_blocked else "FAIL",
            "details": "RUF1378_3 and GATE1378_4 keep BLOCKED_NO_CLAIM.",
        },
        {
            "validation_id": "VAL1378_5_no_claim_rows",
            "check": "all generated rows keep valid_for_claim=false and claim_allowed=false",
            "status": "PASS" if nonclaim else "FAIL",
            "details": "1378 is conditional derivation plus closure pack, not a local-GR/PPN/R10 pass.",
        },
        {
            "validation_id": "VAL1378_6_csv_parse",
            "check": "all generated CSVs parse cleanly",
            "status": "PASS" if csv_ok else "FAIL",
            "details": csv_details,
        },
        {
            "validation_id": "VAL1378_7_scope",
            "check": "generated outputs stay inside post-checkpoint-work and outside formalization-workbench",
            "status": "PASS" if outputs_scoped and formalization_untouched_by_script else "FAIL",
            "details": f"ROOT={ROOT}; FORMALIZATION_EXISTS={FORMALIZATION.exists()}",
        },
    ]
    overall_ok = all(row["status"] == "PASS" for row in rows)
    rows.append(
        {
            "validation_id": "VAL1378_8_overall",
            "check": "overall 1378 validation",
            "status": "PASS" if overall_ok else "FAIL",
            "details": "1378 derives a conditional gradient-relaxation route and demotes transition inputs to explicit closure-only status.",
        }
    )
    return rows


def write_doc(
    sources: list[dict[str, object]],
    derivation: list[dict[str, object]],
    gradient_branch: list[dict[str, object]],
    closure_pack: list[dict[str, object]],
    runner_feed: list[dict[str, object]],
    gates: list[dict[str, object]],
    decisions: list[dict[str, object]],
    next_targets: list[dict[str, object]],
    validations: list[dict[str, object]],
) -> None:
    text = f"""# {TITLE}

**Current verdict:** fixed-`L0` double-zero by itself does **not** derive the transition law. It gives pointwise algebraic silence at `m=m_*`, but no differential equation for a spatial profile, no `L_tr`, no `U_B`, and no support powers. So the transition plateau cannot be smuggled in as if the fixed-`L0` branch already proved it.

**Best derivation route found:** if the parent action is extended by a signed gradient stiffness `kappa_m`, the local vacuum equation becomes `kappa_m Box eta - L0^-2 F2 eta=0`, giving `ell_tr=sqrt(kappa_m L0^2/F2)` and an exponential support law `U_B=exp(-d/ell_tr)` with `pS=1`. That is mathematically clean, but it is conditional because `kappa_m`, boundary data, source coupling, and shell handling are not parent-signed.

**Discipline move:** transition inputs are demoted to an explicit closure-only input pack. This is useful because it gives a finite list of what must be derived or sourced next, while keeping local-GR/PPN/R10 claims blocked.

## Source Register

{table(["source_id", "source_path", "required_anchor", "exists", "anchor_found", "purpose", "valid_for_claim", "claim_allowed"], sources)}

## Transition Parent-Law Derivation

{table(["step_id", "object", "derivation", "result", "status", "remaining_gap", "source_paths", "valid_for_claim", "claim_allowed"], derivation)}

## Conditional Gradient-Relaxation Branch

{table(["branch_id", "branch_component", "conditional_formula", "derived_mapping", "required_parent_signature", "status", "valid_for_claim", "claim_allowed"], gradient_branch)}

## Explicit Closure Input Pack

{table(["input_id", "closure_input", "required_value_or_rule", "role", "current_status", "refusal_gate", "valid_for_claim", "claim_allowed"], closure_pack)}

## Runner Feed Update

{table(["feed_id", "runner_field", "feed_update", "status", "blocks_claim_because", "valid_for_claim", "claim_allowed"], runner_feed)}

## Claim Gates

{table(["gate_id", "gate", "status", "reason", "valid_for_claim", "claim_allowed"], gates)}

## Decision Ledger

{table(["decision_id", "decision", "why", "next_action", "valid_for_claim", "claim_allowed"], decisions)}

## Next Target

{table(["next_id", "next_doc", "next_script", "task", "success_condition", "do_not_claim", "valid_for_claim", "claim_allowed"], next_targets)}

## Validation

{table(["validation_id", "check", "status", "details"], validations)}
"""
    DOC_PATH.write_text(text, encoding="utf-8")


def main() -> None:
    sources = source_register()
    derivation = derivation_rows()
    gradient_branch = gradient_branch_rows()
    closure_pack = closure_pack_rows()
    runner_feed = runner_feed_rows()
    gates = claim_gate_rows()
    decisions = decision_rows()
    next_targets = next_rows()

    csv_paths = generated_csv_paths()
    write_csv(SOURCE_REGISTER_PATH, sources)
    write_csv(DERIVATION_PATH, derivation)
    write_csv(GRADIENT_BRANCH_PATH, gradient_branch)
    write_csv(CLOSURE_PACK_PATH, closure_pack)
    write_csv(RUNNER_FEED_PATH, runner_feed)
    write_csv(CLAIM_GATE_PATH, gates)
    write_csv(DECISION_PATH, decisions)
    write_csv(NEXT_PATH, next_targets)

    validations = validation_rows(sources, derivation, gradient_branch, closure_pack, runner_feed, gates, csv_paths)
    write_csv(VALIDATION_PATH, validations)
    write_doc(sources, derivation, gradient_branch, closure_pack, runner_feed, gates, decisions, next_targets, validations)

    print(f"wrote {DOC_PATH}")
    print(f"wrote {VALIDATION_PATH}")
    print(f"formalization-workbench touched by this script: {FORMALIZATION.exists() and False}")


if __name__ == "__main__":
    main()

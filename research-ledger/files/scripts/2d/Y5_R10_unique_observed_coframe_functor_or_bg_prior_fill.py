from __future__ import annotations

import csv
import json
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "source-intake" / "mts_residuals"
DOC = ROOT / "623-Y5-R10-unique-observed-coframe-functor-or-bg-prior-fill.md"
SCRIPT_REL = "scripts/Y5_R10_unique_observed_coframe_functor_or_bg_prior_fill.py"
STATUS = "Y5_R10_observed_coframe_factorization_lemma_written_uniqueness_not_needed_bg_prior_still_open"
CLAIM_CEILING = "private_geometry_functor_gate_only_no_bg_zero_R10_WEP_PPN_or_local_GR_pass"
NEXT_TARGET = "624-Y5-R10-observed-coframe-factorization-parent-signature-or-bg-runner.md"


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def write_csv(path: Path, rows: list[dict[str, object]], fieldnames: list[str] | None = None) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fields = fieldnames or (list(rows[0].keys()) if rows else [])
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        for row in rows:
            writer.writerow(row)


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def parse_bool(value: object) -> bool:
    return str(value).strip().lower() == "true"


def md_table(rows: list[dict[str, object]], fieldnames: list[str] | None = None) -> str:
    if not rows:
        return "_No rows._"
    fields = fieldnames or list(rows[0].keys())

    def cell(value: object) -> str:
        return str(value).replace("|", "\\|").replace("\n", " ")

    lines = [
        "| " + " | ".join(cell(field) for field in fields) + " |",
        "| " + " | ".join("---" for _ in fields) + " |",
    ]
    for row in rows:
        lines.append("| " + " | ".join(cell(row.get(field, "")) for field in fields) + " |")
    return "\n".join(lines)


def build_source_register() -> list[dict[str, object]]:
    sources = [
        ("622-Y5-R10-parent-matter-sector-contract-or-residual-prior-runner.md", "immediate handoff: b_g chosen first"),
        ("source-intake/mts_residuals/P8_Y5_BRR545_622_VALIDATION.csv", "prior validation gate"),
        ("source-intake/mts_residuals/P8_Y5_R10_622_PARENT_MATTER_CONTRACT.csv", "parent matter contract"),
        ("source-intake/mts_residuals/P8_Y5_R10_622_CONTRACT_TO_PRIOR_MAP.csv", "b_g to prior map"),
        ("source-intake/mts_residuals/P8_Y5_R10_622_PRIOR_RUNNER_SMOKE_RESULTS.csv", "prior smoke blocker rows"),
        ("620-Y5-R10-qbarXT-residual-envelope-after-no-marker-failure.md", "b_g residual definition"),
        ("source-intake/mts_residuals/P8_Y5_R10_620_RESIDUAL_BASIS.csv", "six-component residual basis"),
        ("621-Y5-R10-matter-coupling-normal-form-theorem-or-residual-coefficient-priors.md", "normal-form contract"),
        ("source-intake/mts_residuals/P8_Y5_R10_621_COMPONENT_STATUS_MATRIX.csv", "component status matrix"),
        ("565-Y5-R10-coframe-pullback-zero-or-finite-alpha-coefficient.md", "conditional coframe pullback theorem"),
        ("410-quotient-matter-functor-theorem-attempt.md", "quotient matter functor attempt"),
        ("613-Y5-R10-parent-matter-selector-theorem-or-finite-CX-envelope-lock.md", "selector theorem audit"),
        ("423-parent-action-minimality-no-extension-theorem-attempt.md", "no-extension/marker loopholes"),
        (SCRIPT_REL, "this checkpoint generator"),
    ]
    return [
        {"source_file": source_file, "exists": (ROOT / source_file).exists(), "role": role}
        for source_file, role in sources
    ]


def build_functor_theorem_rows() -> list[dict[str, object]]:
    return [
        {
            "theorem_id": "OCF623_0_factorization_lemma",
            "claim_attempted": "derive b_g=0 from quotient-factorized matter coframe",
            "mathematical_statement": "If e_m(Phi)=E(q(Phi)) and dq(v_X)=0, then Lie_vX e_m = DE[dq(v_X)] = 0.",
            "proof_status": "valid_conditional_lemma",
            "parent_status": "factorization_not_signed",
            "what_it_buys": "kills b_g without needing strict uniqueness of E",
            "what_it_does_not_buy": "does not exclude matter seeing e_m(Phi,X) before q, and does not prove local GR",
            "promote_bg_zero": "false",
            "valid_for_claim": "false",
        },
        {
            "theorem_id": "OCF623_1_uniqueness_overkill",
            "claim_attempted": "require unique observed coframe functor",
            "mathematical_statement": "Uniqueness E=Obs_e is stronger than needed for vertical blindness; any E:Q_MTS->Coframe is v_X-blind.",
            "proof_status": "clarified",
            "parent_status": "unique functor_not_derived",
            "what_it_buys": "shifts next proof target from uniqueness to parent factorization through Q_MTS",
            "what_it_does_not_buy": "multiple Q-only frames may still affect baseline interpretation but not b_g along vertical X",
            "promote_bg_zero": "false",
            "valid_for_claim": "false",
        },
        {
            "theorem_id": "OCF623_2_common_X_frame_counterterm",
            "claim_attempted": "exclude hat_g_ab=A_g(X)^2 g_ab",
            "mathematical_statement": "A_g(X) is not a well-defined Q_MTS functor if X is a representative fibre coordinate, but it remains legal unless parent matter factorization is signed.",
            "proof_status": "counterexample_routed",
            "parent_status": "not_excluded_by_current_parent",
            "what_it_buys": "defines common_frame_log_derivative as the exact b_g prior",
            "what_it_does_not_buy": "does not bound or zero A_g'(X)",
            "promote_bg_zero": "false",
            "valid_for_claim": "false",
        },
        {
            "theorem_id": "OCF623_3_local_lorentz_gauge",
            "claim_attempted": "separate harmless coframe gauge from physical common frame",
            "mathematical_statement": "e'_obs=Lambda(x)e_obs is safe only when Lambda is ordinary local Lorentz gauge and matter action is gauge-invariant; Weyl/disformal factors are not gauge by default.",
            "proof_status": "classification_rule_written",
            "parent_status": "gauge_handling_conditional",
            "what_it_buys": "prevents counting tetrad gauge as b_g",
            "what_it_does_not_buy": "does not remove conformal/disformal X-sensitive metric modes",
            "promote_bg_zero": "false",
            "valid_for_claim": "false",
        },
        {
            "theorem_id": "OCF623_4_bg_verdict",
            "claim_attempted": "close b_g",
            "mathematical_statement": "b_g=0 follows only after parent signs matter-visible geometry factorization through Q_MTS, or after a sourced bound sets common_frame_log_derivative below arena thresholds.",
            "proof_status": "not_closed",
            "parent_status": "contract_only",
            "what_it_buys": "keeps b_g as the next targeted derivation/prior row",
            "what_it_does_not_buy": "no R10, PPN, clock, orbital, or local-GR pass",
            "promote_bg_zero": "false",
            "valid_for_claim": "false",
        },
    ]


def build_factorization_gate_rows() -> list[dict[str, object]]:
    return [
        {
            "gate_id": "FG623_0_parent_quotient",
            "required_clause": "q:Phi_parent -> Q_MTS exists before matter variation",
            "status": "contract_only",
            "if_pass": "coframe factorization can be stated cleanly",
            "if_fail": "X may be physical geometry data rather than a vertical fibre",
            "blocks_bg_zero": "true",
            "valid_for_claim": "false",
        },
        {
            "gate_id": "FG623_1_X_vertical",
            "required_clause": "dq(v_X)=0 on the local matter branch",
            "status": "conditional_from_prior_work_not_parent_signed",
            "if_pass": "any Q-factorized coframe is v_X-blind",
            "if_fail": "b_g can be physical and must be scored",
            "blocks_bg_zero": "true",
            "valid_for_claim": "false",
        },
        {
            "gate_id": "FG623_2_matter_geometry_factorization",
            "required_clause": "e_matter(Phi)=E(q(Phi)) for all ordinary matter species",
            "status": "not_parent_signed",
            "if_pass": "Lie_vX e_matter=0",
            "if_fail": "common_frame_log_derivative remains open",
            "blocks_bg_zero": "true",
            "valid_for_claim": "false",
        },
        {
            "gate_id": "FG623_3_no_representative_Weyl_or_disformal",
            "required_clause": "no matter-visible A_g(X), B_g(X), or disformal representative-field factor before quotient",
            "status": "not_parent_signed",
            "if_pass": "universal common-frame leakage is excluded",
            "if_fail": "b_g prior required even if WEP is protected",
            "blocks_bg_zero": "true",
            "valid_for_claim": "false",
        },
        {
            "gate_id": "FG623_4_gauge_vs_physical_frame",
            "required_clause": "local Lorentz/tetrad gauge separated from conformal/disformal physical frame",
            "status": "classification_rule_written_not_full_parent_theorem",
            "if_pass": "pure gauge coframe rotations do not enter b_g",
            "if_fail": "runner could confuse gauge with physical common-frame coupling",
            "blocks_bg_zero": "true",
            "valid_for_claim": "false",
        },
        {
            "gate_id": "FG623_5_uniqueness_scope",
            "required_clause": "strict uniqueness of E is required only for single-frame public interpretation, not for vertical b_g zero",
            "status": "scope_clarified",
            "if_pass": "next target can focus on factorization rather than over-strong uniqueness",
            "if_fail": "proof target remains unnecessarily hard",
            "blocks_bg_zero": "false",
            "valid_for_claim": "false",
        },
        {
            "gate_id": "FG623_6_total",
            "required_clause": "FG623_0..FG623_4 parent-signed",
            "status": "not_passed",
            "if_pass": "b_g=0 for ordinary matter geometry coupling",
            "if_fail": "common_frame_log_derivative prior remains active",
            "blocks_bg_zero": "true",
            "valid_for_claim": "false",
        },
    ]


def build_counterexample_rows() -> list[dict[str, object]]:
    return [
        {
            "counterexample_id": "CE623_0_universal_Weyl_X",
            "geometry": "hat_g_ab=A_g(X)^2 g_ab",
            "why_legal_if_unsigned": "universal coupling can preserve WEP while still giving nonzero trace coupling",
            "b_g_projection": "b_g ~ tau_g*d_ln_A_g_dXhat",
            "zero_route": "prove A_g descends to Q_MTS and dq(v_X)=0, or prove d_ln_A_g_dXhat=0",
            "prior_route": "common_frame_log_derivative",
            "valid_for_claim": "false",
        },
        {
            "counterexample_id": "CE623_1_disformal_X",
            "geometry": "hat_g_ab=g_ab+B_g(X)u_a u_b or equivalent disformal readout",
            "why_legal_if_unsigned": "covariant representative-dependent readout can be written unless parent factorization forbids it",
            "b_g_projection": "b_g depends on stress anisotropy and environment vector/tensor choice",
            "zero_route": "derive no representative-dependent disformal geometry",
            "prior_route": "common_frame_disformal_projection",
            "valid_for_claim": "false",
        },
        {
            "counterexample_id": "CE623_2_second_Q_frame",
            "geometry": "e_2=E_2(Q_MTS) with no X representative dependence",
            "why_legal_if_unsigned": "multiple Q-only frames may exist as definitions",
            "b_g_projection": "zero along v_X if E_2 depends only on Q_MTS",
            "zero_route": "vertical blindness already enough for b_g; uniqueness needed only for interpretation",
            "prior_route": "not_a_bg_prior_if_Q_only",
            "valid_for_claim": "false",
        },
        {
            "counterexample_id": "CE623_3_local_Lorentz_rotation",
            "geometry": "e'_obs=Lambda(x)e_obs",
            "why_legal_if_unsigned": "ordinary tetrad gauge freedom",
            "b_g_projection": "zero for gauge-invariant matter action",
            "zero_route": "prove Lambda is local Lorentz gauge and matter action is invariant",
            "prior_route": "no_prior_if_pure_gauge",
            "valid_for_claim": "false",
        },
        {
            "counterexample_id": "CE623_4_marker_dependent_frame",
            "geometry": "hat_g_ab=A(m,X)^2 g_ab",
            "why_legal_if_unsigned": "material marker loophole and geometry loophole combine",
            "b_g_projection": "b_g mixes common-frame and marker channels",
            "zero_route": "derive marker taxonomy plus geometry factorization",
            "prior_route": "common_frame_log_derivative + marker_coupling_projection",
            "valid_for_claim": "false",
        },
    ]


def build_bg_prior_rows() -> list[dict[str, object]]:
    return [
        {
            "prior_id": "BG623_0_common_frame_log_derivative",
            "parameter": "common_frame_log_derivative",
            "symbol": "c_g",
            "definition": "c_g := d ln A_g/dXhat for hat_g_ab=A_g(X)^2 g_ab",
            "component": "b_g",
            "units": "dimensionless",
            "current_value": "MISSING_PARENT_INPUT",
            "source_path": "MISSING_PARENT_SOURCE",
            "claim_gate": "blocked_until_derive_zero_or_numeric_bound",
            "valid_for_claim": "false",
        },
        {
            "prior_id": "BG623_1_trace_response",
            "parameter": "geometry_trace_response",
            "symbol": "tau_g",
            "definition": "tau_g := projected T^ab hat_g_ab/rho_ref, sign and normalization fixed by arena convention",
            "component": "b_g",
            "units": "dimensionless",
            "current_value": "MISSING_ARENA_PROJECTION",
            "source_path": "MISSING_ARENA_SOURCE",
            "claim_gate": "blocked_until_projection_defined",
            "valid_for_claim": "false",
        },
        {
            "prior_id": "BG623_2_effective_bg",
            "parameter": "b_g_effective",
            "symbol": "b_g",
            "definition": "b_g := tau_g*c_g for pure conformal common-frame mode; generalized by a projection matrix for disformal modes",
            "component": "b_g",
            "units": "dimensionless",
            "current_value": "MISSING_PARENT_INPUT",
            "source_path": "MISSING_PARENT_SOURCE",
            "claim_gate": "blocked_until_c_g_and_tau_g_sourced_or_zero_derived",
            "valid_for_claim": "false",
        },
        {
            "prior_id": "BG623_3_zero_certificate",
            "parameter": "b_g_zero_certificate",
            "symbol": "Z_bg",
            "definition": "Z_bg=true only if parent signs q, X verticality, matter geometry factorization, and no representative-dependent frame",
            "component": "b_g",
            "units": "boolean",
            "current_value": "false",
            "source_path": "this_checkpoint",
            "claim_gate": "not_signed",
            "valid_for_claim": "false",
        },
    ]


def build_arena_impact_rows() -> list[dict[str, object]]:
    return [
        {
            "arena_id": "AI623_0_R10",
            "arena": "R10 inverse-square",
            "how_bg_enters": "alpha_X(lambda) contains K_X Qbar_XH P_R10(b_g plus material channels)",
            "if_bg_zero": "removes universal common-frame matter contribution from R10 source/test projection",
            "if_bg_open": "R10 remains blocked until c_g, tau_g, K_X, Qbar_XH, lambda_X, and bound curve are sourced",
            "claim_allowed": "false",
        },
        {
            "arena_id": "AI623_1_PPN",
            "arena": "PPN/local gravity",
            "how_bg_enters": "common metric coupling can shift effective scalar-tensor/PPN residual unless short-range suppressed",
            "if_bg_zero": "removes the highest-leverage metric-sector PPN leakage",
            "if_bg_open": "must compute range suppression and PPN projection",
            "claim_allowed": "false",
        },
        {
            "arena_id": "AI623_2_clocks",
            "arena": "clocks/redshift",
            "how_bg_enters": "common frame affects gravitational redshift/environmental frequency comparisons",
            "if_bg_zero": "clock branch can focus on constants b_theta",
            "if_bg_open": "clock projection needs c_g and environment profile",
            "claim_allowed": "false",
        },
        {
            "arena_id": "AI623_3_orbital",
            "arena": "orbital/binary systems",
            "how_bg_enters": "common metric coupling affects orbital residuals unless local range/profile suppression kills it",
            "if_bg_zero": "orbital branch can focus on source/current/radiation channels",
            "if_bg_open": "orbital scoring needs c_g, lambda_X, and profile model",
            "claim_allowed": "false",
        },
    ]


def build_decision_rows() -> list[dict[str, object]]:
    return [
        {
            "decision_id": "D623_0_main_verdict",
            "status": STATUS,
            "decision": "derive quotient-factorized coframe lemma but do not promote b_g=0",
            "meaning": "if matter geometry factors through Q_MTS, b_g is zero along v_X; the current parent action has not signed that factorization",
            "next_target": NEXT_TARGET,
            "valid_for_claim": "false",
        },
        {
            "decision_id": "D623_1_uniqueness_scope",
            "status": "uniqueness_not_needed_for_vertical_bg_zero",
            "decision": "weaken proof target from strict uniqueness to factorization through Q_MTS",
            "meaning": "multiple Q-only frames do not by themselves source b_g along vertical X",
            "next_target": NEXT_TARGET,
            "valid_for_claim": "false",
        },
        {
            "decision_id": "D623_2_prior_fill",
            "status": "common_frame_prior_retained",
            "decision": "retain common_frame_log_derivative prior",
            "meaning": "representative-dependent Weyl/disformal matter geometry remains legal until parent factorization is signed",
            "next_target": NEXT_TARGET,
            "valid_for_claim": "false",
        },
        {
            "decision_id": "D623_3_claim_ceiling",
            "status": CLAIM_CEILING,
            "decision": "no local test pass",
            "meaning": "b_g zero is not signed; R10/PPN/clock/orbital claims remain blocked",
            "next_target": NEXT_TARGET,
            "valid_for_claim": "false",
        },
    ]


def build_route_rows() -> list[dict[str, object]]:
    return [
        {
            "route_id": "RU623_0_allowed",
            "allowed_after_623": "cite the factorization lemma: e_m=E(q(Phi)) and dq(v_X)=0 imply Lie_vX e_m=0",
            "forbidden_after_623": "say the parent action has proved e_m=E(q(Phi))",
            "next_action": NEXT_TARGET,
        },
        {
            "route_id": "RU623_1_allowed",
            "allowed_after_623": "treat uniqueness as interpretive, not required for b_g vertical zero",
            "forbidden_after_623": "force an over-strong uniqueness theorem before proving factorization",
            "next_action": "try parent signature for observed coframe factorization",
        },
        {
            "route_id": "RU623_2_allowed",
            "allowed_after_623": "fill c_g/tau_g priors only if factorization cannot be signed",
            "forbidden_after_623": "score b_g while c_g or tau_g has MISSING markers",
            "next_action": NEXT_TARGET,
        },
    ]


def build_nonclaim_summary() -> list[dict[str, object]]:
    return [
        {
            "status": STATUS,
            "claim_ceiling": CLAIM_CEILING,
            "factorization_lemma_derived": "true",
            "unique_functor_derived": "false",
            "uniqueness_required_for_bg_zero": "false",
            "parent_factorization_signed": "false",
            "b_g_zero_promoted": "false",
            "common_frame_prior_retained": "true",
            "R10_pass": "false",
            "WEP_pass": "false",
            "PPN_pass": "false",
            "local_GR_pass": "false",
            "next_target": NEXT_TARGET,
        }
    ]


def build_validation_rows(
    source_register: list[dict[str, object]],
    theorem_rows: list[dict[str, object]],
    gate_rows: list[dict[str, object]],
    counterexample_rows: list[dict[str, object]],
    bg_prior_rows: list[dict[str, object]],
    arena_rows: list[dict[str, object]],
    decision_rows: list[dict[str, object]],
    nonclaim_rows: list[dict[str, object]],
) -> list[dict[str, object]]:
    missing_sources = [row["source_file"] for row in source_register if not parse_bool(row["exists"])]
    prior_path = OUT / "P8_Y5_BRR545_622_VALIDATION.csv"
    prior_rows = read_csv(prior_path) if prior_path.exists() else []
    prior_failures = [row for row in prior_rows if row.get("result") != "pass"]
    lemma_present = any(row["theorem_id"] == "OCF623_0_factorization_lemma" and row["proof_status"] == "valid_conditional_lemma" for row in theorem_rows)
    no_bg_zero_promoted = all(not parse_bool(row["promote_bg_zero"]) for row in theorem_rows)
    total_gate = [row for row in gate_rows if row["gate_id"] == "FG623_6_total"]
    total_gate_blocks = bool(total_gate) and total_gate[0]["status"] == "not_passed" and parse_bool(total_gate[0]["blocks_bg_zero"])
    counterexamples_routed = len(counterexample_rows) >= 5 and all(row["prior_route"] for row in counterexample_rows)
    required_prior_parameters = {"common_frame_log_derivative", "geometry_trace_response", "b_g_effective", "b_g_zero_certificate"}
    prior_parameters = {row["parameter"] for row in bg_prior_rows}
    bg_priors_safe = required_prior_parameters.issubset(prior_parameters) and all(not parse_bool(row["valid_for_claim"]) for row in bg_prior_rows)
    missing_prior_markers = any("MISSING_" in str(value) for row in bg_prior_rows for value in row.values())
    arenas_blocked = all(row["claim_allowed"] == "false" for row in arena_rows)
    all_nonclaim = all(
        not parse_bool(row.get("valid_for_claim", "false"))
        for row in theorem_rows + gate_rows + counterexample_rows + bg_prior_rows + decision_rows
    )
    nonclaim = nonclaim_rows[0]

    return [
        {
            "check_id": "V623_0_source_paths_exist",
            "result": "pass" if not missing_sources else "fail",
            "detail": "missing=" + str(len(missing_sources)) + ("; " + json.dumps(missing_sources) if missing_sources else ""),
        },
        {
            "check_id": "V623_1_prior_622_clean",
            "result": "pass" if prior_path.exists() and not prior_failures else "fail",
            "detail": f"prior_exists={prior_path.exists()};prior_rows={len(prior_rows)};prior_failures={len(prior_failures)}",
        },
        {
            "check_id": "V623_2_factorization_lemma_present",
            "result": "pass" if lemma_present else "fail",
            "detail": "e_m=E(q(Phi)) and dq(v_X)=0 implies Lie_vX e_m=0",
        },
        {
            "check_id": "V623_3_no_bg_zero_promotion",
            "result": "pass" if no_bg_zero_promoted else "fail",
            "detail": f"no_bg_zero_promoted={no_bg_zero_promoted}",
        },
        {
            "check_id": "V623_4_total_gate_blocks_bg",
            "result": "pass" if total_gate_blocks else "fail",
            "detail": f"total_gate_blocks={total_gate_blocks}",
        },
        {
            "check_id": "V623_5_counterexamples_routed",
            "result": "pass" if counterexamples_routed else "fail",
            "detail": f"counterexample_rows={len(counterexample_rows)}",
        },
        {
            "check_id": "V623_6_bg_priors_safe",
            "result": "pass" if bg_priors_safe and missing_prior_markers else "fail",
            "detail": f"prior_parameters={','.join(sorted(prior_parameters))};missing_markers={missing_prior_markers}",
        },
        {
            "check_id": "V623_7_arenas_blocked",
            "result": "pass" if arenas_blocked else "fail",
            "detail": f"arena_rows={len(arena_rows)};all_claim_allowed_false={arenas_blocked}",
        },
        {
            "check_id": "V623_8_all_claim_flags_false",
            "result": "pass" if all_nonclaim else "fail",
            "detail": f"all_valid_for_claim_false={all_nonclaim}",
        },
        {
            "check_id": "V623_9_no_local_claim",
            "result": "pass"
            if nonclaim["R10_pass"] == "false"
            and nonclaim["WEP_pass"] == "false"
            and nonclaim["PPN_pass"] == "false"
            and nonclaim["local_GR_pass"] == "false"
            and nonclaim["b_g_zero_promoted"] == "false"
            else "fail",
            "detail": "b_g_zero=false;R10=false;WEP=false;PPN=false;local_GR=false",
        },
    ]


def write_doc(
    source_register: list[dict[str, object]],
    theorem_rows: list[dict[str, object]],
    gate_rows: list[dict[str, object]],
    counterexample_rows: list[dict[str, object]],
    bg_prior_rows: list[dict[str, object]],
    arena_rows: list[dict[str, object]],
    decision_rows: list[dict[str, object]],
    route_rows: list[dict[str, object]],
    nonclaim_rows: list[dict[str, object]],
    validation_rows: list[dict[str, object]],
) -> None:
    generated = utc_now()
    content = f"""# 623 Y5 R10 unique observed coframe functor or bg prior fill

Generated: {generated}  
Status: `{STATUS}`  
Claim ceiling: `{CLAIM_CEILING}`  
Next target: `{NEXT_TARGET}`

## Verdict
- I attacked the `b_g` geometry branch first, as planned.
- The useful derivation is slightly different from the title: strict uniqueness of the observed coframe functor is not required to kill `b_g`. The sufficient condition is factorization through the quotient.
- Conditional lemma: if `e_matter(Phi)=E(q(Phi))` and `dq(v_X)=0`, then `Lie_vX(e_matter)=0`, so the common metric/coframe contribution `b_g` vanishes.
- The current parent action has not signed `e_matter(Phi)=E(q(Phi))` for all ordinary matter. Therefore `b_g=0` is not promoted, and `common_frame_log_derivative` remains the honest prior.

## Coframe Factorization Lemma

```text
q: Phi_parent -> Q_MTS
v_X vertical: dq(v_X)=0
e_matter(Phi)=E(q(Phi))
```

Then:

```text
Lie_vX e_matter = D(E o q)[v_X] = DE[dq(v_X)] = 0
```

For a pure common conformal frame,

```text
hat_g_ab = A_g(X)^2 g_ab
c_g = d ln A_g/dXhat
b_g ~= tau_g c_g
```

So either the parent signs the factorization lemma and `b_g=0`, or `c_g` and the arena trace/projection `tau_g` must be supplied before local tests can score it.

## Source Register
{md_table(source_register)}

## Functor Theorem Attempt
{md_table(theorem_rows)}

## Factorization Gate
{md_table(gate_rows)}

## Counterexample Router
{md_table(counterexample_rows)}

## b_g Prior Fill
{md_table(bg_prior_rows)}

## Arena Impact
{md_table(arena_rows)}

## Decision
{md_table(decision_rows)}

## Route Update
{md_table(route_rows)}

## Nonclaim Summary
{md_table(nonclaim_rows)}

## Validation
{md_table(validation_rows)}

## Practical Read
This narrows the geometry problem nicely. We do not need to prove a grand unique-frame theorem before making progress. We need the parent to sign one sharper clause: ordinary matter-visible geometry factors through `Q_MTS`. If it signs, `b_g` dies. If it does not, `c_g` becomes the first common-frame prior for R10/PPN/clock/orbital scoring.
"""
    DOC.write_text(content, encoding="utf-8")


def main() -> None:
    source_register = build_source_register()
    theorem_rows = build_functor_theorem_rows()
    gate_rows = build_factorization_gate_rows()
    counterexample_rows = build_counterexample_rows()
    bg_prior_rows = build_bg_prior_rows()
    arena_rows = build_arena_impact_rows()
    decision_rows = build_decision_rows()
    route_rows = build_route_rows()
    nonclaim_rows = build_nonclaim_summary()
    validation_rows = build_validation_rows(
        source_register,
        theorem_rows,
        gate_rows,
        counterexample_rows,
        bg_prior_rows,
        arena_rows,
        decision_rows,
        nonclaim_rows,
    )

    outputs = [
        ("P8_Y5_R10_623_SOURCE_REGISTER.csv", source_register),
        ("P8_Y5_R10_623_COFRAME_FUNCTOR_THEOREM_ATTEMPT.csv", theorem_rows),
        ("P8_Y5_R10_623_FACTORIZATION_GATE.csv", gate_rows),
        ("P8_Y5_R10_623_COUNTEREXAMPLE_ROUTER.csv", counterexample_rows),
        ("P8_Y5_R10_623_BG_PRIOR_FILL.csv", bg_prior_rows),
        ("P8_Y5_R10_623_ARENA_IMPACT.csv", arena_rows),
        ("P8_Y5_BRR545_623_DECISION.csv", decision_rows),
        ("P8_Y5_BRR545_623_ROUTE_UPDATE.csv", route_rows),
        ("P8_Y5_R10_623_NONCLAIM_SUMMARY.csv", nonclaim_rows),
        ("P8_Y5_BRR545_623_VALIDATION.csv", validation_rows),
    ]
    for filename, rows in outputs:
        write_csv(OUT / filename, rows)

    write_doc(
        source_register,
        theorem_rows,
        gate_rows,
        counterexample_rows,
        bg_prior_rows,
        arena_rows,
        decision_rows,
        route_rows,
        nonclaim_rows,
        validation_rows,
    )

    failed = [row for row in validation_rows if row["result"] != "pass"]
    print(json.dumps({"status": STATUS, "doc": str(DOC), "failed_checks": failed}, indent=2))
    if failed:
        raise SystemExit(1)


if __name__ == "__main__":
    main()

from __future__ import annotations

import csv
import json
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "source-intake" / "mts_residuals"
DOC = ROOT / "619-Y5-R10-no-marker-minimal-quotient-theorem-or-qbarXT-residual-fill.md"
SCRIPT_REL = "scripts/Y5_R10_no_marker_minimal_quotient_theorem_or_qbarXT_residual_fill.py"
STATUS = "Y5_R10_no_marker_minimal_quotient_theorem_conditional_only_qbarXT_residual_fill_selected"
CLAIM_CEILING = "private_derivation_gate_only_no_qbarXT_zero_R10_WEP_PPN_or_local_GR_claim"
NEXT_TARGET = "620-Y5-R10-qbarXT-residual-envelope-after-no-marker-failure.md"


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
        ("618-Y5-R10-no-pole-source-zero-certificate-after-finite-branch-demotion.md", "immediate handoff: no-marker/qbarXT route selected"),
        ("source-intake/mts_residuals/P8_Y5_BRR545_618_VALIDATION.csv", "prior validation gate"),
        ("source-intake/mts_residuals/P8_Y5_R10_618_SOURCE_ZERO_CERTIFICATE_AUDIT.csv", "source-zero certificate audit"),
        ("613-Y5-R10-parent-matter-selector-theorem-or-finite-CX-envelope-lock.md", "selector theorem and finite envelope lock"),
        ("source-intake/mts_residuals/P8_Y5_R10_613_SELECTOR_CERTIFICATE_TEMPLATE.csv", "matter-selector certificate obligations"),
        ("source-intake/mts_residuals/P8_Y5_R10_613_COUNTERMODEL_STRESS_TEST.csv", "legal countermodels against qbarXT zero"),
        ("576-Y5-R10-constant-source-current-universality-or-qbar-envelope.md", "constant/source-current universality attempt"),
        ("source-intake/mts_residuals/P8_Y5_R10_576_UNIVERSALITY_PREMISE_LEDGER.csv", "constant/source-current premise ledger"),
        ("565-Y5-R10-coframe-pullback-zero-or-finite-alpha-coefficient.md", "coframe pullback zero theorem"),
        ("410-quotient-matter-functor-theorem-attempt.md", "quotient matter functor theorem attempt"),
        ("404-selector-blind-matter-axiom-origin.md", "selector-blind matter axiom origin"),
        ("423-parent-action-minimality-no-extension-theorem-attempt.md", "minimality/no-extension theorem attempt"),
        (SCRIPT_REL, "this checkpoint generator"),
    ]
    return [
        {"source_file": source_file, "exists": (ROOT / source_file).exists(), "role": role}
        for source_file, role in sources
    ]


def build_theorem_attempt_rows() -> list[dict[str, object]]:
    return [
        {
            "theorem_row": "NMT619_0_chain_rule_zero",
            "claim_attempted": "qbar_XT=0 from selector-blind matter factorization",
            "mathematical_statement": "If S_m=S_m[Psi,Obs(Q_MTS),theta] with Lie_vX Obs(Q_MTS)=0 and Lie_vX theta=0, then Lie_vX S_m=0.",
            "proof_status": "valid_conditional_chain_rule",
            "missing_parent_clause": "parent must prove all ordinary matter actions factor only through Obs(Q_MTS)",
            "failure_mode": "extra marker or X-dependent constants add nonzero chain-rule terms",
            "promote_to_theorem_zero": "false",
            "valid_for_claim": "false",
        },
        {
            "theorem_row": "NMT619_1_primitive_minimal_quotient",
            "claim_attempted": "Q_MTS is the primitive/free/minimal object for ordinary matter readouts",
            "mathematical_statement": "For every natural ordinary-matter readout R, there exists a unique factorization R=Rbar∘Obs∘q.",
            "proof_status": "not_constructed",
            "missing_parent_clause": "category of allowed readouts, naturality rule, and universal property are not defined from parent action",
            "failure_mode": "a nonconstant natural marker can be adjoined without contradiction",
            "promote_to_theorem_zero": "false",
            "valid_for_claim": "false",
        },
        {
            "theorem_row": "NMT619_2_no_natural_marker",
            "claim_attempted": "no material marker m can couple to ordinary matter",
            "mathematical_statement": "Any m with Lie_vX m != 0 is pure gauge, a source-independent universal auxiliary, or a retained physical field.",
            "proof_status": "policy_shape_only",
            "missing_parent_clause": "parent variation must classify every marker instead of excluding it by preference",
            "failure_mode": "transforming material marker extension Q_tilde=(Q,m)/G_rel remains legal",
            "promote_to_theorem_zero": "false",
            "valid_for_claim": "false",
        },
        {
            "theorem_row": "NMT619_3_constant_triviality",
            "claim_attempted": "ordinary constants are selector-trivial representation data",
            "mathematical_statement": "Lie_vX theta_A=0 and no theta_A(X,class,species) terms exist in parent matter sector.",
            "proof_status": "not_parent_derived",
            "missing_parent_clause": "superselection/representation theorem for constants",
            "failure_mode": "class-dependent or species-dependent constants source qbar_constants",
            "promote_to_theorem_zero": "false",
            "valid_for_claim": "false",
        },
        {
            "theorem_row": "NMT619_4_universal_source_current",
            "claim_attempted": "only one Hilbert/coframe source with one universal kappa is permitted",
            "mathematical_statement": "J_XT = kappa*T_Hilbert[Obs(Q)] and no species-weighted or non-Hilbert currents contribute.",
            "proof_status": "not_parent_derived",
            "missing_parent_clause": "source-current ownership theorem from parent action",
            "failure_mode": "species-weighted source or non-Hilbert current survives",
            "promote_to_theorem_zero": "false",
            "valid_for_claim": "false",
        },
        {
            "theorem_row": "NMT619_5_no_marker_theorem_verdict",
            "claim_attempted": "primitive-minimal no-marker theorem closes qbar_XT",
            "mathematical_statement": "NMT619_0..NMT619_4 jointly imply qbar_XT=0.",
            "proof_status": "not_closed",
            "missing_parent_clause": "primitive quotient, no-marker, constant-triviality, and source-current premises remain independent assumptions",
            "failure_mode": "qbar_XT must be filled as a residual envelope",
            "promote_to_theorem_zero": "false",
            "valid_for_claim": "false",
        },
    ]


def build_minimal_quotient_gate_rows() -> list[dict[str, object]]:
    return [
        {
            "gate_id": "MQ619_0_fixed_spurion",
            "candidate_extension": "fixed active spurion s(x) inserted into matter action",
            "strict_minimal_action_result": "excluded_conditionally",
            "reason": "a fixed non-varied active object violates the strict parent-variation contract",
            "safe_zero_condition": "parent action explicitly forbids nondynamical active matter selectors",
            "residual_if_not_safe": "qbar_marker_fixed",
            "valid_for_claim": "false",
        },
        {
            "gate_id": "MQ619_1_transforming_material_marker",
            "candidate_extension": "dynamical or transforming marker m with matter coupling",
            "strict_minimal_action_result": "not_excluded_by_current_corpus",
            "reason": "it can be made covariant/natural and varied as a real field",
            "safe_zero_condition": "prove m is pure gauge or a unique source-independent auxiliary",
            "residual_if_not_safe": "qbar_marker_dynamic",
            "valid_for_claim": "false",
        },
        {
            "gate_id": "MQ619_2_common_conformal_frame",
            "candidate_extension": "hat_g_ab=exp(2F(X))g_ab seen universally by matter",
            "strict_minimal_action_result": "not_excluded_by_current_corpus",
            "reason": "universality protects WEP but does not make the X derivative vanish",
            "safe_zero_condition": "prove F'(X)=0 or that X is gauge before matter readout",
            "residual_if_not_safe": "qbar_metric_common",
            "valid_for_claim": "false",
        },
        {
            "gate_id": "MQ619_3_selector_dependent_constants",
            "candidate_extension": "theta_A=theta_A0[1+epsilon_A X] or class-dependent constants",
            "strict_minimal_action_result": "not_excluded_by_current_corpus",
            "reason": "constant triviality is not yet a parent theorem",
            "safe_zero_condition": "prove constants are representation/superselection data with Lie_vX theta_A=0",
            "residual_if_not_safe": "qbar_constants",
            "valid_for_claim": "false",
        },
        {
            "gate_id": "MQ619_4_species_weighted_source",
            "candidate_extension": "sum_A kappa_A T_A instead of one universal kappa*T",
            "strict_minimal_action_result": "not_excluded_by_current_corpus",
            "reason": "universal source-current ownership has not been parent-derived",
            "safe_zero_condition": "derive one source current and one universal coupling from parent symmetry",
            "residual_if_not_safe": "qbar_source_weight",
            "valid_for_claim": "false",
        },
        {
            "gate_id": "MQ619_5_post_readout_EFT",
            "candidate_extension": "phenomenological matter counterterm added after quotient readout",
            "strict_minimal_action_result": "forbidden_for_theorem_credit",
            "reason": "it cannot be used to claim parent derivation",
            "safe_zero_condition": "discard from derivation branch or rederive as parent term",
            "residual_if_not_safe": "qbar_readout_counterterm",
            "valid_for_claim": "false",
        },
        {
            "gate_id": "MQ619_6_gate_verdict",
            "candidate_extension": "all material marker routes",
            "strict_minimal_action_result": "no_marker_theorem_not_closed",
            "reason": "only fixed active spurions are conditionally excluded; transforming markers and constants remain legal",
            "safe_zero_condition": "construct parent minimal quotient universal property",
            "residual_if_not_safe": "qbar_XT_residual_envelope",
            "valid_for_claim": "false",
        },
    ]


def build_counterexample_router_rows() -> list[dict[str, object]]:
    return [
        {
            "counterexample_id": "CER619_0_common_metric_mode",
            "legal_counterexample": "universal conformal/common metric frame hat_g=exp(2F(X))g",
            "evades_which_zero": "qbar_XT=0 via matter factorization",
            "residual_channel": "qbar_metric_common",
            "required_fill": "bound Fprime_X or derive Fprime_X=0 from parent quotient",
            "next_runner_action": "include as symbolic residual coefficient",
            "valid_for_claim": "false",
        },
        {
            "counterexample_id": "CER619_1_selector_constants",
            "legal_counterexample": "theta_A depends on X, class, or species label",
            "evades_which_zero": "Lie_vX theta_A=0",
            "residual_channel": "qbar_constants",
            "required_fill": "source or bound dtheta_A/dX for clock, EM, mass, or composition channels",
            "next_runner_action": "add constant-derivative input slots",
            "valid_for_claim": "false",
        },
        {
            "counterexample_id": "CER619_2_material_marker",
            "legal_counterexample": "Q_tilde=(Q,m)/G_rel with m varied or transforming naturally",
            "evades_which_zero": "no material marker extension",
            "residual_channel": "qbar_marker_dynamic",
            "required_fill": "classify m as gauge/auxiliary or retain its coupling derivative",
            "next_runner_action": "add marker residual slot",
            "valid_for_claim": "false",
        },
        {
            "counterexample_id": "CER619_3_species_source_weight",
            "legal_counterexample": "source current sum_A kappa_A T_A with species weights",
            "evades_which_zero": "one universal Hilbert current",
            "residual_channel": "qbar_source_weight",
            "required_fill": "derive universal kappa or bound species splittings",
            "next_runner_action": "add composition residual slot",
            "valid_for_claim": "false",
        },
        {
            "counterexample_id": "CER619_4_nonHilbert_current",
            "legal_counterexample": "spin/torsion/topological/non-Hilbert current coupled to X channel",
            "evades_which_zero": "source equals Hilbert/coframe stress only",
            "residual_channel": "qbar_nonHilbert",
            "required_fill": "prove exact/zero-flux/nonlocal-only or provide coefficient",
            "next_runner_action": "add non-Hilbert current slot",
            "valid_for_claim": "false",
        },
        {
            "counterexample_id": "CER619_5_post_readout_counterterm",
            "legal_counterexample": "effective counterterm inserted after quotient readout",
            "evades_which_zero": "parent-derived matter sector",
            "residual_channel": "qbar_readout_counterterm",
            "required_fill": "ban for theorem branch; retain only as phenomenological residual if used",
            "next_runner_action": "flag as no theorem credit",
            "valid_for_claim": "false",
        },
    ]


def build_qbarxt_residual_rows() -> list[dict[str, object]]:
    return [
        {
            "residual_id": "QXT619_0_metric_common",
            "source_channel": "common observed metric/coframe X-dependence",
            "symbolic_qbar_component": "qbar_metric_common ~ (delta S_m/d hat_g_ab) Lie_vX hat_g_ab",
            "required_parent_input": "Obs(Q) theorem with Lie_vX hat_g=0, or sourced Fprime_X bound",
            "current_status": "open_residual",
            "next_action": "create input slot for Fprime_X or theorem-zero certificate",
            "valid_for_claim": "false",
        },
        {
            "residual_id": "QXT619_1_constants",
            "source_channel": "ordinary constants and representation data",
            "symbolic_qbar_component": "qbar_constants ~ sum_A (partial S_m/partial theta_A) Lie_vX theta_A",
            "required_parent_input": "constant-triviality theorem or dtheta_A/dX coefficients",
            "current_status": "open_residual",
            "next_action": "create constant derivative ledger for EM, clocks, masses, composition",
            "valid_for_claim": "false",
        },
        {
            "residual_id": "QXT619_2_marker",
            "source_channel": "material marker fields",
            "symbolic_qbar_component": "qbar_marker ~ (partial S_m/partial m) Lie_vX m",
            "required_parent_input": "marker classified as gauge/auxiliary/retained field plus coupling derivative",
            "current_status": "open_residual",
            "next_action": "add marker classification gate before any zero promotion",
            "valid_for_claim": "false",
        },
        {
            "residual_id": "QXT619_3_source_weight",
            "source_channel": "species-weighted or class-weighted source current",
            "symbolic_qbar_component": "qbar_source_weight ~ sum_A (kappa_A-kappa) T_A",
            "required_parent_input": "one universal kappa theorem or bounded species splittings",
            "current_status": "open_residual",
            "next_action": "map to WEP/composition and R10 source-test rows",
            "valid_for_claim": "false",
        },
        {
            "residual_id": "QXT619_4_nonHilbert",
            "source_channel": "non-Hilbert/coframe currents",
            "symbolic_qbar_component": "qbar_nonHilbert ~ J_XT^nonHilbert",
            "required_parent_input": "exactness/zero-flux theorem or numerical coefficient",
            "current_status": "open_residual",
            "next_action": "route torsion/spin/topological currents to separate slots",
            "valid_for_claim": "false",
        },
        {
            "residual_id": "QXT619_5_readout_counterterm",
            "source_channel": "post-readout EFT or phenomenological term",
            "symbolic_qbar_component": "qbar_readout_counterterm ~ delta_X S_EFT_after_readout",
            "required_parent_input": "parent derivation or explicit demotion to phenomenology",
            "current_status": "forbidden_for_theorem_credit_retained_as_residual_if_used",
            "next_action": "block theorem credit and label nonfundamental",
            "valid_for_claim": "false",
        },
        {
            "residual_id": "QXT619_6_total",
            "source_channel": "qbar_XT residual sum",
            "symbolic_qbar_component": "qbar_XT = qbar_metric_common + qbar_constants + qbar_marker + qbar_source_weight + qbar_nonHilbert + qbar_readout_counterterm",
            "required_parent_input": "each component zero-derived or coefficient-filled",
            "current_status": "residual_fill_selected",
            "next_action": NEXT_TARGET,
            "valid_for_claim": "false",
        },
    ]


def build_decision_rows() -> list[dict[str, object]]:
    return [
        {
            "decision_id": "D619_0_main_verdict",
            "status": STATUS,
            "decision": "do not promote no-marker/minimal-quotient theorem",
            "meaning": "the conditional chain-rule proof is useful, but the parent has not excluded transforming markers, constant dependence, or source-current variants",
            "next_target": NEXT_TARGET,
            "valid_for_claim": "false",
        },
        {
            "decision_id": "D619_1_conditional_theorem_retained",
            "status": "conditional_theorem_retained",
            "decision": "retain exact qbarXT zero conditions as future parent-action contract",
            "meaning": "if primitive quotient, no-marker, constant-triviality, and source-current universality are later proven, qbar_XT can be closed cleanly",
            "next_target": NEXT_TARGET,
            "valid_for_claim": "false",
        },
        {
            "decision_id": "D619_2_residual_fill",
            "status": "qbarXT_residual_fill_selected",
            "decision": "fill qbar_XT as a residual envelope instead of smuggling qbar_XT=0",
            "meaning": "the next runner should expose metric, constants, marker, source-weight, non-Hilbert, and readout-counterterm components",
            "next_target": NEXT_TARGET,
            "valid_for_claim": "false",
        },
        {
            "decision_id": "D619_3_claim_ceiling",
            "status": CLAIM_CEILING,
            "decision": "no local-GR/R10/WEP/PPN claim",
            "meaning": "this checkpoint is theorem hygiene and residual routing only",
            "next_target": NEXT_TARGET,
            "valid_for_claim": "false",
        },
    ]


def build_route_rows() -> list[dict[str, object]]:
    return [
        {
            "route_id": "RU619_0_allowed",
            "allowed_after_619": "quote the qbar_XT=0 chain-rule theorem only with all parent premises visible",
            "forbidden_after_619": "state qbar_XT=0 as already derived",
            "next_action": "use residual envelope unless parent no-marker proof is supplied",
        },
        {
            "route_id": "RU619_1_allowed",
            "allowed_after_619": "exclude fixed active spurions under strict parent variation",
            "forbidden_after_619": "exclude transforming material markers without classifying them",
            "next_action": "route legal marker extensions into qbar_marker",
        },
        {
            "route_id": "RU619_2_allowed",
            "allowed_after_619": "treat constants and source weights as explicit residual channels",
            "forbidden_after_619": "hide constant/source-current assumptions inside matter factorization",
            "next_action": NEXT_TARGET,
        },
    ]


def build_nonclaim_summary() -> list[dict[str, object]]:
    return [
        {
            "status": STATUS,
            "claim_ceiling": CLAIM_CEILING,
            "conditional_qbarXT_zero_theorem": "true",
            "primitive_minimal_quotient_proven": "false",
            "no_marker_theorem_proven": "false",
            "constant_triviality_proven": "false",
            "source_current_universality_proven": "false",
            "qbar_XT_zero_promoted": "false",
            "qbar_XT_residual_fill_selected": "true",
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
    minimal_gate_rows: list[dict[str, object]],
    counterexample_rows: list[dict[str, object]],
    qbar_rows: list[dict[str, object]],
    decision_rows: list[dict[str, object]],
    nonclaim_rows: list[dict[str, object]],
) -> list[dict[str, object]]:
    missing_sources = [row["source_file"] for row in source_register if not parse_bool(row["exists"])]

    prior_path = OUT / "P8_Y5_BRR545_618_VALIDATION.csv"
    prior_rows = read_csv(prior_path) if prior_path.exists() else []
    prior_failures = [row for row in prior_rows if row.get("result") != "pass"]

    theorem_zero_promoted = any(parse_bool(row["promote_to_theorem_zero"]) for row in theorem_rows)
    all_gate_nonclaim = all(not parse_bool(row["valid_for_claim"]) for row in minimal_gate_rows)
    all_counterexamples_routed = all(str(row["residual_channel"]).startswith("qbar_") for row in counterexample_rows)
    total_residual_row = [row for row in qbar_rows if row["residual_id"] == "QXT619_6_total"]
    all_qbar_nonclaim = all(not parse_bool(row["valid_for_claim"]) for row in qbar_rows)
    next_target_set = all(row["next_target"] == NEXT_TARGET for row in decision_rows)
    nonclaim = nonclaim_rows[0]

    checks = [
        {
            "check_id": "V619_0_source_paths_exist",
            "result": "pass" if not missing_sources else "fail",
            "detail": "missing=" + str(len(missing_sources)) + ("; " + json.dumps(missing_sources) if missing_sources else ""),
        },
        {
            "check_id": "V619_1_prior_618_clean",
            "result": "pass" if prior_path.exists() and not prior_failures else "fail",
            "detail": f"prior_exists={prior_path.exists()};prior_rows={len(prior_rows)};prior_failures={len(prior_failures)}",
        },
        {
            "check_id": "V619_2_conditional_chain_rule_written",
            "result": "pass" if theorem_rows[0]["proof_status"] == "valid_conditional_chain_rule" else "fail",
            "detail": "qbar_XT zero theorem retained only with visible premises",
        },
        {
            "check_id": "V619_3_no_theorem_zero_promotion",
            "result": "pass" if not theorem_zero_promoted else "fail",
            "detail": f"theorem_zero_promoted={theorem_zero_promoted}",
        },
        {
            "check_id": "V619_4_minimal_gate_nonclaim",
            "result": "pass" if all_gate_nonclaim else "fail",
            "detail": f"gate_rows={len(minimal_gate_rows)};all_valid_for_claim_false={all_gate_nonclaim}",
        },
        {
            "check_id": "V619_5_counterexamples_routed",
            "result": "pass" if all_counterexamples_routed else "fail",
            "detail": f"counterexample_rows={len(counterexample_rows)};all_have_qbar_residual_channel={all_counterexamples_routed}",
        },
        {
            "check_id": "V619_6_qbarXT_residual_template_written",
            "result": "pass" if total_residual_row and all_qbar_nonclaim else "fail",
            "detail": f"qbar_rows={len(qbar_rows)};has_total_row={bool(total_residual_row)};all_valid_for_claim_false={all_qbar_nonclaim}",
        },
        {
            "check_id": "V619_7_next_target_set",
            "result": "pass" if next_target_set else "fail",
            "detail": NEXT_TARGET,
        },
        {
            "check_id": "V619_8_no_R10_or_local_GR_claim",
            "result": "pass"
            if nonclaim["R10_pass"] == "false"
            and nonclaim["WEP_pass"] == "false"
            and nonclaim["PPN_pass"] == "false"
            and nonclaim["local_GR_pass"] == "false"
            else "fail",
            "detail": "R10_pass=false;WEP=false;PPN=false;local_GR=false",
        },
    ]
    return checks


def write_doc(
    source_register: list[dict[str, object]],
    theorem_rows: list[dict[str, object]],
    minimal_gate_rows: list[dict[str, object]],
    counterexample_rows: list[dict[str, object]],
    qbar_rows: list[dict[str, object]],
    decision_rows: list[dict[str, object]],
    route_rows: list[dict[str, object]],
    nonclaim_rows: list[dict[str, object]],
    validation_rows: list[dict[str, object]],
) -> None:
    generated = utc_now()
    content = f"""# 619 Y5 R10 no-marker minimal quotient theorem or qbarXT residual fill

Generated: {generated}  
Status: `{STATUS}`  
Claim ceiling: `{CLAIM_CEILING}`  
Next target: `{NEXT_TARGET}`

## Verdict
- I tried the derivation route first: the clean chain-rule theorem exists, but it only closes `qbar_XT=0` if the parent action already proves primitive quotient minimality, no material marker, constant triviality, and one universal source current.
- The current corpus does **not** prove those parent clauses. It excludes fixed active spurions only under a strict parent-variation contract; transforming material markers, common metric modes, selector-dependent constants, and species-weighted sources remain legal counterexamples.
- Therefore `qbar_XT=0` is not promoted. The honest next move is to fill `qbar_XT` as a residual envelope with explicit channels instead of hiding it behind a plateau/no-marker axiom.
- This is a useful fail: it turns the vague missing assumption into a short list of exact parent-action obligations.

## Conditional Theorem
If

```text
q: Phi_parent -> Q_MTS
v_X is vertical: dq(v_X)=0
S_matter = S_matter[Psi, Obs(Q_MTS), theta]
Lie_vX Obs(Q_MTS)=0
Lie_vX theta=0
```

then

```text
Lie_vX S_matter = 0
qbar_XT = 0
```

by the chain rule. This theorem is mathematically fine. The problem is not the local proof; the problem is ownership of the premises.

## Missing Parent Ownership
The theorem becomes a real local-GR route only if the parent action proves something close to:

```text
Q_MTS is the primitive/minimal ordinary-matter quotient.
Every natural ordinary-matter readout uniquely factors through Obs(Q_MTS).
Every additional material marker is pure gauge, a source-independent universal auxiliary, or a retained physical field.
Ordinary constants are selector-trivial representation data.
The source current is one universal Hilbert/coframe current.
```

That exact contract is now written, but not derived.

## Source Register
{md_table(source_register)}

## No-Marker Theorem Attempt
{md_table(theorem_rows)}

## Minimal Quotient Gate
{md_table(minimal_gate_rows)}

## Counterexample Router
{md_table(counterexample_rows)}

## qbarXT Residual Fill Template
{md_table(qbar_rows)}

## Decision
{md_table(decision_rows)}

## Route Update
{md_table(route_rows)}

## Nonclaim Summary
{md_table(nonclaim_rows)}

## Validation
{md_table(validation_rows)}

## Practical Read
This keeps the local branch alive, but not by magic. The clean theorem says exactly what a future parent action must own. Until it owns it, the boxer stays on points: `qbar_XT` becomes a scored residual vector, not a knockout zero. Next checkpoint should build the residual envelope so local tests can punish or tolerate each missing clause separately.
"""
    DOC.write_text(content, encoding="utf-8")


def main() -> None:
    source_register = build_source_register()
    theorem_rows = build_theorem_attempt_rows()
    minimal_gate_rows = build_minimal_quotient_gate_rows()
    counterexample_rows = build_counterexample_router_rows()
    qbar_rows = build_qbarxt_residual_rows()
    decision_rows = build_decision_rows()
    route_rows = build_route_rows()
    nonclaim_rows = build_nonclaim_summary()
    validation_rows = build_validation_rows(
        source_register,
        theorem_rows,
        minimal_gate_rows,
        counterexample_rows,
        qbar_rows,
        decision_rows,
        nonclaim_rows,
    )

    outputs = [
        ("P8_Y5_R10_619_SOURCE_REGISTER.csv", source_register),
        ("P8_Y5_R10_619_NO_MARKER_THEOREM_ATTEMPT.csv", theorem_rows),
        ("P8_Y5_R10_619_MINIMAL_QUOTIENT_GATE.csv", minimal_gate_rows),
        ("P8_Y5_R10_619_COUNTEREXAMPLE_ROUTER.csv", counterexample_rows),
        ("P8_Y5_R10_619_QBARXT_RESIDUAL_FILL_TEMPLATE.csv", qbar_rows),
        ("P8_Y5_BRR545_619_DECISION.csv", decision_rows),
        ("P8_Y5_BRR545_619_ROUTE_UPDATE.csv", route_rows),
        ("P8_Y5_R10_619_NONCLAIM_SUMMARY.csv", nonclaim_rows),
        ("P8_Y5_BRR545_619_VALIDATION.csv", validation_rows),
    ]
    for filename, rows in outputs:
        write_csv(OUT / filename, rows)

    write_doc(
        source_register,
        theorem_rows,
        minimal_gate_rows,
        counterexample_rows,
        qbar_rows,
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

from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
REPO = ROOT.parent
FW = REPO / "formalization-workbench"
OUT = ROOT / "source-intake" / "mts_residuals"
PYCACHE = ROOT / "scripts" / "__pycache__"
DOC = ROOT / "3369-Y5-R2FR-extra-response-Y5-source-zero-or-qbarXT-bound-row-under-AX1090.md"
RUN_UTC = datetime.now(timezone.utc).isoformat()

OUTPUTS = {
    "source_register": OUT / "P8_Y5_R2FR_3369_SOURCE_REGISTER.csv",
    "zero_theorem": OUT / "P8_Y5_R2FR_3369_QBARXT_SOURCE_ZERO_THEOREM.csv",
    "premise_audit": OUT / "P8_Y5_R2FR_3369_QBARXT_PARENT_PREMISE_AUDIT.csv",
    "counterexamples": OUT / "P8_Y5_R2FR_3369_QBARXT_COUNTEREXAMPLES.csv",
    "bound_law": OUT / "P8_Y5_R2FR_3369_QBARXT_BOUND_LAW.csv",
    "component_rows": OUT / "P8_Y5_R2FR_3369_QBARXT_COMPONENT_ROWS_NONCLAIM.csv",
    "runner": OUT / "P8_Y5_R2FR_3369_QBARXT_RUNNER_NONCLAIM.csv",
    "gates": OUT / "P8_Y5_R2FR_3369_PROMOTION_GATES.csv",
    "decision": OUT / "P8_Y5_R2FR_3369_DECISION_LEDGER.csv",
    "next": OUT / "P8_Y5_R2FR_3369_NEXT_TARGET.csv",
    "validation": OUT / "P8_Y5_BRR545_3369_VALIDATION.csv",
}

LOCAL_SOURCES = [
    ("SRC3369_0_3368_doc", ROOT / "3368-Y5-R2FR-parent-nonEH-operator-classification-or-source-coefficient-first-row-under-AX1090.md", "3368 classified extra-response Y5 source leg as top priority"),
    ("SRC3369_1_3368_next", OUT / "P8_Y5_R2FR_3368_NEXT_TARGET.csv", "3368 next target naming 3369"),
    ("SRC3369_2_3368_priority", OUT / "P8_Y5_R2FR_3368_OPERATOR_PRIORITY_RANKING.csv", "extra-response Y5 priority row"),
    ("SRC3369_3_3368_coeff", OUT / "P8_Y5_R2FR_3368_FIRST_SOURCE_COEFFICIENT_ROWS_NONCLAIM.csv", "qbar_XT/J_X missing coefficient row"),
    ("SRC3369_4_1027_doc", ROOT / "1027-Y5-R10-qbarXT-source-zero-or-bounded-coupling-row.md", "older qbarXT chain-rule theorem and bounded schema"),
    ("SRC3369_5_1027_proof", OUT / "P8_Y5_R10_1027_SOURCE_ZERO_PROOF_AUDIT.csv", "qbarXT source-zero proof audit"),
    ("SRC3369_6_1027_schema", OUT / "P8_Y5_R10_1027_BOUNDED_QBARXT_ROW_SCHEMA.csv", "bounded qbarXT row schema"),
    ("SRC3369_7_1027_counter", OUT / "P8_Y5_R10_1027_COUNTEREXAMPLE_GUARD.csv", "qbarXT counterexample guard"),
    ("SRC3369_8_2594_channels", OUT / "P8_Y5_SOURCE_NORM_2594_CHANNEL_VECTOR.csv", "Y5 source-normalization eight-channel vector"),
    ("SRC3369_9_2594_stack", OUT / "P8_Y5_SOURCE_NORM_2594_THEOREM_STACK.csv", "Y5 source-normalization theorem stack"),
    ("SRC3369_10_2905_cert", OUT / "P8_Y5_R2FR_2905_EXTRA_RESPONSE_SILENCE_CERTIFICATE.csv", "extra-response Y5/Y6 source silence certificate"),
    ("SRC3369_11_2906_split", OUT / "P8_Y5_R2FR_2906_EPSILON_EXTRA_SOURCE_SPLIT.csv", "Y5/Y6 source split"),
    ("SRC3369_12_3339_residual", OUT / "P8_Y5_R2FR_3339_RESIDUAL_CHANNEL_VECTOR.csv", "source-coupling residual vector"),
    ("SRC3369_13_3340_clause", OUT / "P8_Y5_R2FR_3340_PARENT_HILBERT_SOURCE_CLAUSE.csv", "parent Hilbert source clause"),
]


def bool_text(value: bool) -> str:
    return "true" if value else "false"


def parse_csv(path: Path) -> tuple[bool, str]:
    try:
        with path.open("r", encoding="utf-8-sig", newline="") as handle:
            list(csv.DictReader(handle))
        return True, ""
    except Exception as exc:  # noqa: BLE001
        return False, f"{type(exc).__name__}: {exc}"


def parse_text(path: Path) -> tuple[bool, str]:
    try:
        path.read_text(encoding="utf-8", errors="replace")
        return True, ""
    except Exception as exc:  # noqa: BLE001
        return False, f"{type(exc).__name__}: {exc}"


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    headers: list[str] = []
    for row in rows:
        for key in row:
            if key not in headers:
                headers.append(key)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=headers)
        writer.writeheader()
        writer.writerows(rows)


def source_rows() -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    for source_id, path, role in LOCAL_SOURCES:
        exists = path.exists()
        parse_ok = False
        parse_error = ""
        if exists:
            parse_ok, parse_error = parse_csv(path) if path.suffix.lower() == ".csv" else parse_text(path)
        rows.append(
            {
                "source_id": source_id,
                "source_path": str(path),
                "exists": bool_text(exists),
                "parse_ok": bool_text(parse_ok),
                "role": role,
                "parse_error": parse_error,
                "valid_for_claim": "false",
            }
        )
    return rows


def zero_theorem_rows() -> list[dict[str, str]]:
    return [
        {
            "theorem_id": "QZT3369_0_chain_rule_source_zero",
            "statement": "If X is vertical to the parent quotient q, the observed coframe is e_obs=Obs_e(q(Phi)), ordinary matter descends as S_matter=Sbar[Psi,e_obs,theta(q)], and Lie_X theta=0, then J_X=-delta S_matter/delta X=0 and qbar_XT=0.",
            "derivation": "Lie_X S_matter = (delta Sbar/delta e_obs) Lie_X e_obs + (partial Sbar/partial theta) Lie_X theta. Since Lie_X q=0, Lie_X e_obs=0. Since Lie_X theta=0, the remaining term vanishes. Therefore the extra-response source leg receives no ordinary matter source.",
            "current_result": "VALID_CONDITIONAL_THEOREM",
            "blocks_current_claim": "parent q-kernel, observed-coframe descent, matter functor, no-marker constants, and hidden-tail silence are not all parent-signed",
            "valid_for_claim": "false",
        },
        {
            "theorem_id": "QZT3369_1_Y5_extra_response_link",
            "statement": "For the extra-response Y5 channel, qbar_XT=0 implies the matter/test source factor in alpha_X~K_X Qbar_XH qbar_XT and in the Y5 non-EH source leg vanishes.",
            "derivation": "The source/test leg is the pullback derivative of the ordinary matter/readout functional along X. If the chain-rule zero theorem holds, that leg is identically zero before empirical readout.",
            "current_result": "CONDITIONAL_LINK_TO_RNONEH_AND_Y5",
            "blocks_current_claim": "K_X, Qbar_XH, lambda_X and parent operator classification remain needed for any nonzero/bound route",
            "valid_for_claim": "false",
        },
        {
            "theorem_id": "QZT3369_2_no_WEP_only_shortcut",
            "statement": "WEP/species-blindness is not enough to prove qbar_XT=0.",
            "derivation": "A universal Weyl or source-frame coupling can be composition-blind while still creating common fifth-force/source-normalization charge; measured G absorbs only constant common modes, not derivative X couplings.",
            "current_result": "SHORTCUT_REJECTED",
            "blocks_current_claim": "requires no-shadow-frame/no-marker/no-hidden-source theorem or finite bounds",
            "valid_for_claim": "false",
        },
    ]


def premise_rows() -> list[dict[str, str]]:
    return [
        {
            "premise_id": "PRE3369_0_q_verticality",
            "required_premise": "Lie_X q = 0 and X lies in the parent quotient kernel before variation",
            "current_status": "CONDITIONAL_NOT_PARENT_SIGNED",
            "failure_mode": "X changes observed geometry/source channel and qbar_XT can be nonzero",
            "source_hint": "QZ1027_1_q_verticality",
            "valid_for_claim": "false",
        },
        {
            "premise_id": "PRE3369_1_observed_coframe",
            "required_premise": "e_obs=Obs_e(q(Phi)) with no representative Weyl/disformal matter frame",
            "current_status": "MISSING_OBS_E_DESCENT_OR_FRAME_LEAK_ZERO",
            "failure_mode": "common c_g or b_dis frame coupling re-enters source normalization",
            "source_hint": "QZ1027_2_observed_coframe",
            "valid_for_claim": "false",
        },
        {
            "premise_id": "PRE3369_2_matter_functor",
            "required_premise": "ordinary matter/readout action has no direct X argument outside e_obs and quotient-owned constants",
            "current_status": "EXACT_CONTRACT_NOT_PARENT_SIGNED",
            "failure_mode": "matter action can contain direct X-sensitive source slot",
            "source_hint": "QZ1027_3_matter_functor;HSC3340_0_parent_action_form",
            "valid_for_claim": "false",
        },
        {
            "premise_id": "PRE3369_3_no_marker_constants",
            "required_premise": "Lie_X masses, material constants, clock constants, EM constants and markers vanish",
            "current_status": "MISSING_NO_MARKER_THEOREM",
            "failure_mode": "b_A or b_alpha marker coupling creates qbar_marker",
            "source_hint": "QZ1027_4_no_marker_constants",
            "valid_for_claim": "false",
        },
        {
            "premise_id": "PRE3369_4_hidden_tail_silence",
            "required_premise": "non-Hilbert current, support shift, domain/projector and boundary tails are theorem-zero or bounded",
            "current_status": "MISSING_HIDDEN_SOURCE_ZERO_OR_BOUND",
            "failure_mode": "visible qbar_XT may be zero while total source normalization still leaks",
            "source_hint": "QZ1027_5_hidden_source_tail;YSN2594_3_mu_extra_zero",
            "valid_for_claim": "false",
        },
        {
            "premise_id": "PRE3369_5_same_branch",
            "required_premise": "all zero clauses hold in one q/e_obs/tau/M_ref branch",
            "current_status": "MISSING_SAME_BRANCH_CERTIFICATE",
            "failure_mode": "sector-by-sector zeroes use incompatible normalizations",
            "source_hint": "XRS2905_8_same_branch",
            "valid_for_claim": "false",
        },
    ]


def counterexample_rows() -> list[dict[str, str]]:
    return [
        {
            "counterexample_id": "CE3369_0_universal_Weyl",
            "weak_premise": "WEP/species-blindness",
            "construction": "g_matter=exp(2 c_g X) g_obs for every species",
            "why_it_blocks": "composition WEP can pass while common source charge qbar_geom is nonzero",
            "repair": "prove c_g=0/no-shadow-frame or bound c_g with arena projection",
            "valid_for_claim": "false",
        },
        {
            "counterexample_id": "CE3369_1_material_marker",
            "weak_premise": "observed coframe is X-blind",
            "construction": "m_A(X), alpha_EM(X), or material/readout marker theta_A(X)",
            "why_it_blocks": "Lie_X theta_A term survives in Lie_X S_matter",
            "repair": "no-marker theorem or numeric b_A/b_alpha component bounds",
            "valid_for_claim": "false",
        },
        {
            "counterexample_id": "CE3369_2_hidden_nonHilbert_tail",
            "weak_premise": "ordinary Hilbert matter source is zero",
            "construction": "hidden non-Hilbert source current, support shift, boundary/contact tail, or domain projector source",
            "why_it_blocks": "qbar_XT for visible matter can vanish while total Y5 source-normalization residual remains",
            "repair": "q_nonH/support/domain/boundary zero theorem or bound rows",
            "valid_for_claim": "false",
        },
        {
            "counterexample_id": "CE3369_3_field_rename",
            "weak_premise": "choose e_obs notation as the matter frame",
            "construction": "move X-dependence into constants, G_eff, boundary reference, or source normalization by field redefinition",
            "why_it_blocks": "same coupling reappears in another residual channel",
            "repair": "single parent branch ledger across matter, clocks, EM, source mass and boundary/reference",
            "valid_for_claim": "false",
        },
    ]


def bound_law_rows() -> list[dict[str, str]]:
    return [
        {
            "law_id": "BQL3369_0_total_abs_guard",
            "quantity": "qbar_XT_bound_abs",
            "law": "|qbar_XT| <= |qbar_geom| + |qbar_marker| + |qbar_nonH| + |qbar_support| + |qbar_boundary| + |qbar_domain|",
            "derivation": "decompose Lie_X S_source into observed-frame, marker-constant, non-Hilbert current, support/worldtube, boundary/contact and domain/projector variations; use triangle inequality because no parent cancellation theorem is signed",
            "claim_condition": "every component is theorem-zero or has numeric/source-backed value with units and source path",
            "current_status": "BOUND_LAW_DERIVED_VALUES_MISSING",
            "valid_for_claim": "false",
        },
        {
            "law_id": "BQL3369_1_RnonEH_dependency",
            "quantity": "R_nonEH_extra_Y5",
            "law": "|R_nonEH_extra_Y5| <= |K_X Qbar_XH| |qbar_XT_bound_abs| in the selected arena plus boundary/source terms",
            "derivation": "the extra-response source leg enters the non-EH sourced operator product; zero qbar_XT kills this leg, while finite qbar_XT requires K_X and Qbar_XH response factors",
            "claim_condition": "K_X, Qbar_XH, lambda_X/arena kernel and qbar_XT components all sourced",
            "current_status": "DEPENDENCY_LAW_DERIVED_INPUTS_MISSING",
            "valid_for_claim": "false",
        },
    ]


def component_rows() -> list[dict[str, str]]:
    return [
        {
            "component_id": "QBC3369_0_geom",
            "symbol": "qbar_geom",
            "definition": "ordinary test/source X charge from Weyl/disformal observed-frame leakage",
            "zero_route": "no-shadow-frame theorem: Lie_X e_matter=0 in the ordinary matter functor",
            "bound_formula": "|qbar_geom| <= |tau_g c_g| + |tau_dis b_dis|",
            "current_status": "MISSING_FRAME_LEAK_ZERO_OR_NUMERIC_BOUND",
            "observable_links": "R10;PPN;clock;WEP-common",
            "valid_for_claim": "false",
        },
        {
            "component_id": "QBC3369_1_marker",
            "symbol": "qbar_marker",
            "definition": "X charge from masses, material constants, EM constants, clock/readout markers",
            "zero_route": "quotient-owned constants/no-marker theorem: Lie_X theta_A=0",
            "bound_formula": "|qbar_marker| <= sum_A |s_A b_A| + |s_alpha b_alpha|",
            "current_status": "MISSING_NO_MARKER_THEOREM_OR_NUMERIC_BOUNDS",
            "observable_links": "WEP;composition clocks;alpha;R10 materials",
            "valid_for_claim": "false",
        },
        {
            "component_id": "QBC3369_2_nonHilbert",
            "symbol": "qbar_nonH",
            "definition": "non-Hilbert/source-shadow current contribution to the extra-response source leg",
            "zero_route": "parent Hilbert source clause plus no direct source slot",
            "bound_formula": "|qbar_nonH| <= |q_nonH| + |J_shadow|/|J_H|",
            "current_status": "MISSING_NO_DIRECT_SOURCE_SLOT_OR_NUMERIC_BOUND",
            "observable_links": "source_mass;WEP;Newton;local_GR",
            "valid_for_claim": "false",
        },
        {
            "component_id": "QBC3369_3_support",
            "symbol": "qbar_support",
            "definition": "source worldtube/support shift under X variation",
            "zero_route": "support fixed by Hilbert source before readout",
            "bound_formula": "|qbar_support| <= |Delta_W_support|",
            "current_status": "MISSING_FIXED_SUPPORT_THEOREM_OR_NUMERIC_BOUND",
            "observable_links": "orbital GM;source_mass;PPN",
            "valid_for_claim": "false",
        },
        {
            "component_id": "QBC3369_4_boundary",
            "symbol": "qbar_boundary",
            "definition": "boundary/contact/interface source contribution to qbar_XT",
            "zero_route": "compact interior collar plus no contact/interface support",
            "bound_formula": "|qbar_boundary| <= |epsilon_boundary_contact| + |B_X_flux|",
            "current_status": "CONTACT_SURVIVOR_OPEN",
            "observable_links": "PPN;R10;orbital;WEP material",
            "valid_for_claim": "false",
        },
        {
            "component_id": "QBC3369_5_domain",
            "symbol": "qbar_domain",
            "definition": "domain/projector/source-measure contribution to qbar_XT",
            "zero_route": "Pi_M/source measure is parent-fixed q-basic chain map",
            "bound_formula": "|qbar_domain| <= |epsilon_Qv_projector_piece| + |epsilon_Cv_constraint_missing|",
            "current_status": "MISSING_PROJECTOR_VARIATION_AND_WARD_CLOSURE",
            "observable_links": "Newton;orbital;PPN;source_mass",
            "valid_for_claim": "false",
        },
        {
            "component_id": "QBC3369_TOTAL",
            "symbol": "qbar_XT_bound_abs",
            "definition": "absolute no-cancellation envelope for extra-response Y5 source leg",
            "zero_route": "all components theorem-zero in same parent branch",
            "bound_formula": "sum_abs(QBC3369_0..QBC3369_5)",
            "current_status": "SCHEMA_READY_VALUES_MISSING",
            "observable_links": "R_nonEH;Newton;local_GR;WEP;R10;PPN;clock;orbital",
            "valid_for_claim": "false",
        },
    ]


def runner_rows() -> list[dict[str, str]]:
    return [
        {
            "run_id": "RUN3369_0_chain_rule_theorem",
            "test": "prove qbar_XT=0 under strict descent premises",
            "result": "PASS_CONDITIONAL_THEOREM",
            "detail": "Lie_X q=0, e_obs(q), S_matter descent and Lie_X theta=0 imply Lie_X S_matter=0",
            "valid_for_claim": "false",
        },
        {
            "run_id": "RUN3369_1_current_corpus_zero",
            "test": "claim qbar_XT=0 for current corpus",
            "result": "BLOCKED_NOT_PARENT_SIGNED",
            "detail": "q-kernel/coframe/matter/no-marker/hidden-tail/same-branch premises are not all signed",
            "valid_for_claim": "false",
        },
        {
            "run_id": "RUN3369_2_bound_law",
            "test": "construct qbar_XT absolute bound law",
            "result": "PASS_BOUND_LAW_NONCLAIM",
            "detail": "component envelope written with no-cancellation guard; values missing",
            "valid_for_claim": "false",
        },
        {
            "run_id": "RUN3369_3_WEP_shortcut",
            "test": "use WEP/species-blindness alone as source-zero proof",
            "result": "REJECT_SHORTCUT",
            "detail": "universal Weyl/common source coupling can be WEP-clean and still qbar_XT-nonzero",
            "valid_for_claim": "false",
        },
        {
            "run_id": "RUN3369_4_RnonEH_promotion",
            "test": "promote R_nonEH/source-normalized Newton from qbar_XT route",
            "result": "BLOCKED",
            "detail": "zero theorem conditional; bound law has no numeric/source-backed component values",
            "valid_for_claim": "false",
        },
    ]


def gate_rows() -> list[dict[str, str]]:
    return [
        {"gate_id": "GATE3369_0_chain_rule_zero_shape", "claim": "chain-rule source-zero theorem is derived", "passed": "true", "reason": "explicit Lie_X S_matter derivation written", "valid_for_claim": "false"},
        {"gate_id": "GATE3369_1_bound_law_written", "claim": "qbar_XT no-cancellation bound law is written", "passed": "true", "reason": "geom/marker/nonH/support/boundary/domain components sum absolutely", "valid_for_claim": "false"},
        {"gate_id": "GATE3369_2_parent_premises_closed", "claim": "all qbar_XT parent premises close in one branch", "passed": "false", "reason": "q-kernel, coframe, matter functor, no-marker, hidden tail and same-branch premises remain unsigned", "valid_for_claim": "false"},
        {"gate_id": "GATE3369_3_numeric_bound_ready", "claim": "qbar_XT bound row is numerically score-ready", "passed": "false", "reason": "component values and source paths are missing", "valid_for_claim": "false"},
        {"gate_id": "GATE3369_4_local_GR_Newton", "claim": "local GR/Newton source coupling promoted", "passed": "false", "reason": "qbar_XT is narrowed but neither zero-claimed nor bounded", "valid_for_claim": "false"},
    ]


def decision_rows() -> list[dict[str, str]]:
    return [
        {
            "decision_id": "DEC3369_0_derivation_result",
            "question": "Can qbar_XT/J_X be derived zero?",
            "answer": "yes conditionally, not as current corpus claim",
            "reason": "chain-rule proof is exact if X is quotient-vertical and ordinary matter/constants descend through q",
            "next_action": "attack the missing parent premise most likely to close several components: no-shadow-frame/no-marker matter functor",
            "valid_for_claim": "false",
        },
        {
            "decision_id": "DEC3369_1_bound_result",
            "question": "Can qbar_XT be bounded now?",
            "answer": "bound law yes, numeric bound no",
            "reason": "absolute envelope is derived but qbar_geom/qbar_marker/qbar_nonH/qbar_support/qbar_boundary/qbar_domain lack values",
            "next_action": "fill the first component row, probably qbar_geom via c_g/no-shadow-frame or qbar_marker via no-marker theorem",
            "valid_for_claim": "false",
        },
        {
            "decision_id": "DEC3369_2_best_next",
            "question": "What is the best next strike?",
            "answer": "try no-shadow-frame/no-marker matter-functor closure before numeric fishing",
            "reason": "one parent-domain theorem could zero qbar_geom and qbar_marker together and materially improve the local-GR route",
            "next_action": "3370 should target the ordinary matter functor: no A_g(X), no b_A/b_alpha markers, no direct source slot",
            "valid_for_claim": "false",
        },
    ]


def next_rows() -> list[dict[str, str]]:
    return [
        {
            "target_id": "3370-Y5-R2FR-no-shadow-frame-no-marker-matter-functor-or-first-qbar-component-bound-under-AX1090.md",
            "target_script": "scripts/Y5_R2FR_3370_no_shadow_frame_no_marker_matter_functor_or_first_qbar_component_bound.py",
            "objective": "derive that ordinary matter has only the quotient-owned observed coframe and quotient-owned constants, with no A_g(X), disformal frame, b_A, b_alpha or direct source marker; if not, emit the first qbar_geom/qbar_marker bound row",
            "why_next": "3369 shows qbar_XT zero hinges on coframe/no-marker matter descent; closing it would remove two largest counterexample families",
            "valid_for_claim": "false",
        },
        {
            "target_id": "3371-Y5-R2FR-hidden-source-support-tail-zero-or-qbar-nonH-bound-under-AX1090.md",
            "target_script": "scripts/Y5_R2FR_3371_hidden_source_support_tail_zero_or_qbar_nonH_bound.py",
            "objective": "prove no hidden non-Hilbert/source-support/domain tail contributes to qbar_XT, or write qbar_nonH/qbar_support/qbar_domain bound rows",
            "why_next": "even visible matter source-zero does not silence total Y5 source normalization until hidden/support/domain tails are zero or bounded",
            "valid_for_claim": "false",
        },
    ]


def validate_rows(
    sources: list[dict[str, str]],
    zero_theorem: list[dict[str, str]],
    premises: list[dict[str, str]],
    counterexamples: list[dict[str, str]],
    bound_law: list[dict[str, str]],
    components: list[dict[str, str]],
    runner: list[dict[str, str]],
    gates: list[dict[str, str]],
    next_rows_in: list[dict[str, str]],
) -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []

    def add(check_id: str, check: str, passed: bool, detail: str = "") -> None:
        rows.append({"check_id": check_id, "check": check, "passed": bool_text(passed), "detail": detail})

    add("VAL3369_0_sources_exist", "all cited local source paths exist", all(row["exists"] == "true" for row in sources))
    add("VAL3369_1_sources_parse", "all cited local source paths parse", all(row["parse_ok"] == "true" for row in sources))
    add("VAL3369_2_chain_rule_theorem", "chain-rule source-zero theorem present", any(row["theorem_id"] == "QZT3369_0_chain_rule_source_zero" for row in zero_theorem))
    add("VAL3369_3_premise_audit_complete", "premise audit covers q, coframe, matter, markers, hidden tail and same branch", {row["premise_id"] for row in premises} == {"PRE3369_0_q_verticality", "PRE3369_1_observed_coframe", "PRE3369_2_matter_functor", "PRE3369_3_no_marker_constants", "PRE3369_4_hidden_tail_silence", "PRE3369_5_same_branch"})
    add("VAL3369_4_counterexamples_block_shortcuts", "counterexamples block WEP/covariance/rename shortcuts", len(counterexamples) >= 4 and all(row["valid_for_claim"] == "false" for row in counterexamples))
    add("VAL3369_5_bound_law_written", "qbar_XT absolute no-cancellation bound law is written", any(row["law_id"] == "BQL3369_0_total_abs_guard" and "qbar_geom" in row["law"] for row in bound_law))
    add("VAL3369_6_component_rows_complete", "component rows cover geom, marker, nonH, support, boundary, domain and total", {row["symbol"] for row in components} == {"qbar_geom", "qbar_marker", "qbar_nonH", "qbar_support", "qbar_boundary", "qbar_domain", "qbar_XT_bound_abs"})
    add("VAL3369_7_runner_blocks_current_claim", "runner blocks current qbarXT/local-GR claim", any(row["run_id"] == "RUN3369_4_RnonEH_promotion" and row["result"] == "BLOCKED" for row in runner))
    add("VAL3369_8_no_promotion_gates", "local GR/Newton gate remains false", any(row["gate_id"] == "GATE3369_4_local_GR_Newton" and row["passed"] == "false" for row in gates))
    add("VAL3369_9_next_target_matter_functor", "next target attacks no-shadow-frame/no-marker matter functor", any(row["target_id"].startswith("3370-") for row in next_rows_in))
    write_targets = list(OUTPUTS.values()) + [DOC]
    add("VAL3369_10_write_scope_outside_formalization", "all 3369 write targets are outside formalization-workbench", all(not str(path).lower().startswith(str(FW).lower()) for path in write_targets), f"write_targets={len(write_targets)}")
    passed_so_far = all(row["passed"] == "true" for row in rows)
    add("VAL3369_11_overall", "3369 validation overall", passed_so_far, "all required checks passed" if passed_so_far else "one or more checks failed")
    return rows


def markdown_table(rows: list[dict[str, Any]]) -> str:
    if not rows:
        return ""
    headers: list[str] = []
    for row in rows:
        for key in row:
            if key not in headers:
                headers.append(key)
    lines = ["| " + " | ".join(headers) + " |", "| " + " | ".join(["---"] * len(headers)) + " |"]
    for row in rows:
        vals = [str(row.get(header, "")).replace("\n", " ").replace("|", "\\|") for header in headers]
        lines.append("| " + " | ".join(vals) + " |")
    return "\n".join(lines)


def write_doc(
    sources: list[dict[str, str]],
    zero_theorem: list[dict[str, str]],
    premises: list[dict[str, str]],
    counterexamples: list[dict[str, str]],
    bound_law: list[dict[str, str]],
    components: list[dict[str, str]],
    runner: list[dict[str, str]],
    gates: list[dict[str, str]],
    decisions: list[dict[str, str]],
    next_rows_in: list[dict[str, str]],
    validations: list[dict[str, str]],
) -> None:
    content = f"""# 3369 - Y5/R2FR extra-response Y5 source-zero or qbarXT bound row under AX1090

## Summary
- 3369 attacks the highest-priority extra/response source leg: `J_X/qbar_XT`.
- Derivation result: the source-zero theorem is real as a chain-rule theorem. If `X` is quotient-vertical, `e_obs` descends through `q`, ordinary matter has no direct `X` slot, and material/EM/clock constants are quotient-owned, then `Lie_X S_matter=0`, so `J_X=qbar_XT=0`.
- Current-corpus result: the zero theorem is not claimable yet because q-kernel, observed coframe, matter functor, no-marker constants, hidden source tails, and same-branch closure are not all parent-signed.
- Bound result: a no-cancellation envelope is now explicit: `|qbar_XT| <= |qbar_geom|+|qbar_marker|+|qbar_nonH|+|qbar_support|+|qbar_boundary|+|qbar_domain|`.
- Best next strike is no-shadow-frame/no-marker matter-functor closure, because that could kill `qbar_geom` and `qbar_marker` together.

Generated UTC: `{RUN_UTC}`

## Source Register
{markdown_table(sources)}

## Source-Zero Theorem
{markdown_table(zero_theorem)}

## Parent Premise Audit
{markdown_table(premises)}

## Counterexamples
{markdown_table(counterexamples)}

## Bound Law
{markdown_table(bound_law)}

## Component Rows
{markdown_table(components)}

## Runner
{markdown_table(runner)}

## Promotion Gates
{markdown_table(gates)}

## Decision Ledger
{markdown_table(decisions)}

## Next Target
{markdown_table(next_rows_in)}

## Validation
{markdown_table(validations)}
"""
    DOC.write_text(content, encoding="utf-8")


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    sources = source_rows()
    zero = zero_theorem_rows()
    premises = premise_rows()
    counters = counterexample_rows()
    laws = bound_law_rows()
    components = component_rows()
    runs = runner_rows()
    gates = gate_rows()
    decisions = decision_rows()
    next_rows_in = next_rows()
    validations = validate_rows(sources, zero, premises, counters, laws, components, runs, gates, next_rows_in)

    write_csv(OUTPUTS["source_register"], sources)
    write_csv(OUTPUTS["zero_theorem"], zero)
    write_csv(OUTPUTS["premise_audit"], premises)
    write_csv(OUTPUTS["counterexamples"], counters)
    write_csv(OUTPUTS["bound_law"], laws)
    write_csv(OUTPUTS["component_rows"], components)
    write_csv(OUTPUTS["runner"], runs)
    write_csv(OUTPUTS["gates"], gates)
    write_csv(OUTPUTS["decision"], decisions)
    write_csv(OUTPUTS["next"], next_rows_in)
    write_csv(OUTPUTS["validation"], validations)
    write_doc(sources, zero, premises, counters, laws, components, runs, gates, decisions, next_rows_in, validations)
    if PYCACHE.exists():
        shutil.rmtree(PYCACHE)


if __name__ == "__main__":
    main()

from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path


CHECKPOINT = "3889"
BRANCH = "MTS_R2FR_Y5_PARENT_OBJECT_LANGUAGE_NO_DIRECT_SOURCE_OR_PREDICTION_COEFFICIENT_FILL_3889"

PCW = Path(__file__).resolve().parents[1]
ROOT = PCW.parent
FWB = ROOT / "formalization-workbench"
OUT = PCW / "source-intake" / "mts_residuals"
DOC_PATH = PCW / "3889-Y5-R2FR-parent-object-language-no-direct-source-or-prediction-coefficient-fill.md"
SPINE_PATH = PCW / "LOCAL_GR_COUPLING_SPINE_CURRENT_STATE.md"

CSV_3888_NEXT = OUT / "P8_Y5_R2FR_3888_NEXT_TARGET.csv"
CSV_3888_DERIVATION = OUT / "P8_Y5_R2FR_3888_QUOTIENT_NO_LINEAR_SOURCE_DERIVATION.csv"
CSV_3888_CHANNELS = OUT / "P8_Y5_R2FR_3888_SOURCE_CHANNEL_SPLIT.csv"
CSV_3888_LOCK = OUT / "P8_Y5_R2FR_3888_RESIDUAL_LOCK_ATTEMPT.csv"
CSV_3888_BOUNDS = OUT / "P8_Y5_R2FR_3888_FIRST_COEFFICIENT_BOUND_INTERFACE.csv"
CSV_3888_VALIDATION = OUT / "P8_Y5_BRR545_3888_VALIDATION.csv"
CSV_2612_GRAMMAR = OUT / "P8_Y5_DIRECT_MATTER_GRAMMAR_GATE_2612_NO_DIRECT_MATTER_X_VERTEX_GRAMMAR_ATTEMPT.csv"
CSV_2612_PREF = OUT / "P8_Y5_DIRECT_MATTER_GRAMMAR_GATE_2612_SOURCE_PREFACTOR_CLASSIFICATION.csv"
CSV_2612_VERTEX = OUT / "P8_Y5_DIRECT_MATTER_GRAMMAR_GATE_2612_DIRECT_VERTEX_AND_NO_MARKER_AUDIT.csv"
CSV_2612_DECISION = OUT / "P8_Y5_DIRECT_MATTER_GRAMMAR_GATE_2612_DECISION_LEDGER.csv"
CSV_2612_COEF = OUT / "P8_Y5_DIRECT_MATTER_GRAMMAR_GATE_2612_AMATTER_COEFFICIENT_PACK.csv"
CSV_2612_GATES = OUT / "P8_Y5_DIRECT_MATTER_GRAMMAR_GATE_2612_CLAIM_GATES.csv"
CSV_2611_AMATTER = OUT / "P8_Y5_MATTER_DESCENT_GATE_2611_AMATTER_BOUND_INTERFACE.csv"
CSV_2570_MATTER = OUT / "P8_Y5_FIELD_QUOTIENT_2570_MATTER_DESCENT_GATE.csv"
CSV_3883_HILBERT = OUT / "P8_Y5_R2FR_3883_SAME_HILBERT_SOURCE_LOCK.csv"
CSV_LOCAL_LOCK = OUT / "P8_Y5_BRR545_LOCAL_LOCK_MAP.csv"

OUTPUTS = {
    "sources": OUT / "P8_Y5_R2FR_3889_SOURCE_REGISTER.csv",
    "theorem": OUT / "P8_Y5_R2FR_3889_PARENT_OBJECT_LANGUAGE_NO_DIRECT_SOURCE_THEOREM.csv",
    "grammar": OUT / "P8_Y5_R2FR_3889_DIRECT_SLOT_EXCLUSION_MATRIX.csv",
    "predictions": OUT / "P8_Y5_R2FR_3889_PREDICTION_SIDE_COEFFICIENT_ROWS.csv",
    "decision": OUT / "P8_Y5_R2FR_3889_ROUTE_DECISION_GATE.csv",
    "runner": OUT / "P8_Y5_R2FR_3889_RUNNER_UPDATE.csv",
    "next": OUT / "P8_Y5_R2FR_3889_NEXT_TARGET.csv",
    "status": OUT / "P8_Y5_R2FR_3889_STATUS.csv",
    "validation": OUT / "P8_Y5_BRR545_3889_VALIDATION.csv",
}

SOURCE_SPECS = [
    ("SRC3889_00_next", CSV_3888_NEXT, "NEXT3888_0", "3888 selected object-language source exclusion target"),
    ("SRC3889_01_derivation", CSV_3888_DERIVATION, "NLS3888_5_verdict", "quotient no-linear-source verdict"),
    ("SRC3889_02_channels", CSV_3888_CHANNELS, "SRCCH3888_1_direct_hidden", "direct hidden source channel"),
    ("SRC3889_03_lock", CSV_3888_LOCK, "RL3888_5_lock_verdict", "residual-lock nonclaim status"),
    ("SRC3889_04_bounds", CSV_3888_BOUNDS, "BND3888_0_boundary_alpha3", "first bound-side interface"),
    ("SRC3889_05_valid", CSV_3888_VALIDATION, "VAL3888_14_next_target", "3888 validation"),
    ("SRC3889_06_grammar", CSV_2612_GRAMMAR, "NDV2612_1_allowed_syntax", "minimal matter syntax"),
    ("SRC3889_07_pref", CSV_2612_PREF, "SP2612_2_relative_species", "relative source prefactor countermodel"),
    ("SRC3889_08_vertex", CSV_2612_VERTEX, "DV2612_5_verdict", "direct vertex audit verdict"),
    ("SRC3889_09_decision", CSV_2612_DECISION, "DEC2612_4_best_next", "2612 next route decision"),
    ("SRC3889_10_coef", CSV_2612_COEF, "CP2612_6_A_direct_matter", "direct matter coefficient pack"),
    ("SRC3889_11_gates", CSV_2612_GATES, "GATE2612_0_no_direct_vertex", "direct grammar claim gate"),
    ("SRC3889_12_Amatter", CSV_2611_AMATTER, "AM2611_8_A_matter", "A_matter bound interface"),
    ("SRC3889_13_2570", CSV_2570_MATTER, "MD2570_0_chain_rule", "quotient matter descent chain rule"),
    ("SRC3889_14_hilbert", CSV_3883_HILBERT, "HSL3883_2_same_source", "same Hilbert source support"),
    ("SRC3889_15_local_lock", CSV_LOCAL_LOCK, "BRL547_7_denominator_WEP", "WEP/source lock bound row"),
]

OBJECT_LANGUAGE_RULE = (
    "Allowed[S_ord] = {sum_A S_A[Psi_A,e_obs(q(Phi)),omega[e_obs],theta_A]} with common measure, "
    "q-basic constants, and no Hom(H_hidden,M_source) generator"
)
HOM_ZERO = "Hom_parent(H_hidden, M_source)=0; therefore V_m[X,rho_A,W], w_A(y), hidden frames g_A(y), alpha_EM(y), m_A(y), and post-readout source masks are not well-typed matter terms"
DIRECT_ZERO = "If the Hom/no-marker grammar is parent-signed, then delta_y V_m|_0=0, delta_y w_A=0, delta_y g_A=0, delta_y alpha_EM=0, and J_A^direct=0"


def now_utc() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def read_text(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        return path.read_text(encoding="utf-8-sig", errors="replace")


def rel(path: Path) -> str:
    try:
        return str(path.relative_to(PCW))
    except ValueError:
        return str(path)


def write_csv(path: Path, rows: list[dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        raise ValueError(f"no rows for {path}")
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def read_csv_rows(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8-sig") as handle:
        return list(csv.DictReader(handle))


def markdown_table(rows: list[dict[str, object]], columns: list[str]) -> str:
    if not rows:
        return ""
    header = "| " + " | ".join(columns) + " |"
    sep = "| " + " | ".join("---" for _ in columns) + " |"
    lines = [header, sep]
    for row in rows:
        cells = [str(row.get(col, "")).replace("\n", " ").replace("|", "\\|") for col in columns]
        lines.append("| " + " | ".join(cells) + " |")
    return "\n".join(lines)


def source_register_rows(timestamp: str) -> list[dict[str, object]]:
    rows = []
    for source_id, path, needle, role in SOURCE_SPECS:
        exists = path.exists()
        text = read_text(path) if exists else ""
        rows.append(
            {
                "source_id": source_id,
                "checkpoint": CHECKPOINT,
                "path": rel(path),
                "exists": exists,
                "needle": needle,
                "needle_found": needle in text,
                "role": role,
                "claim_use": "nonclaim_parent_object_language_or_prediction_fill",
                "timestamp_utc": timestamp,
            }
        )
    return rows


def theorem_rows(timestamp: str) -> list[dict[str, object]]:
    raw_rows = [
        ("OLT3889_0_objects", "Define the parent object language.", "Objects: Q_obs for quotient-observed geometry, H_hidden for quotient-vertical local silence variables, M_source for ordinary matter/source functor.", "FORMAL_LANGUAGE_DECLARED", "declaration must be adopted by parent action"),
        ("OLT3889_1_allowed_syntax", "Allowed ordinary matter syntax.", OBJECT_LANGUAGE_RULE, "EXACT_GRAMMAR_SCHEMA", "not yet parent-signed as the only admissible syntax"),
        ("OLT3889_2_no_Hom", "No source-only hidden arrow.", HOM_ZERO, "EXACT_IF_PARENT_OBJECT_LANGUAGE_SIGNED", "current corpus treats this as contract, not theorem"),
        ("OLT3889_3_derivative_zero", "Direct hidden/source derivative vanishes because the slot is absent, not because a coefficient is tuned.", DIRECT_ZERO, "CONDITIONAL_DIRECT_SOURCE_ZERO", "fails if hidden/source prefactor slots are allowed as extensions"),
        ("OLT3889_4_common_mode", "Universal common prefactor is calibration-only.", "S_ord -> w_* S_ord can be absorbed into kappa/G calibration; relative delta_w_A remains forbidden-or-bounded.", "CALIBRATION_SPLIT_EXACT", "does not zero relative species/source weights by itself"),
        ("OLT3889_5_no_marker", "No-marker/minimality rule.", "ordinary matter labels are representation data over q-basic geometry, not functions of hidden marker/domain/boundary variables.", "CONDITIONAL_MARKER_EXCLUSION", "primitive minimality/invariant-algebra triviality remains unsigned"),
        ("OLT3889_6_verdict", "3889 route verdict.", "The direct-source theorem is mathematically clean if the parent object language signs Hom_parent(H_hidden,M_source)=0; otherwise the surviving direct coefficients must be predicted and bounded.", "THEOREM_READY_PARENT_UNSIGNED", "local GR remains nonclaim"),
    ]
    return [
        {
            "theorem_id": row_id,
            "step": step,
            "statement_or_math": statement,
            "result": result,
            "remaining_failure": failure,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
        for row_id, step, statement, result, failure in raw_rows
    ]


def grammar_rows(timestamp: str) -> list[dict[str, object]]:
    raw_rows = [
        ("GEX3889_0_Vm", "V_m[X,rho_A,W_source]", "not a morphism from Q_obs to M_source if X is hidden vertical", "A_direct_matter", "delta_y V_m|_0=0", "OPEN_PARENT_GRAMMAR_UNSIGNED"),
        ("GEX3889_1_relative_w", "w_A(y,m,D,W) S_A", "source-only Hom from hidden/domain marker to species weight is forbidden", "delta_w_A;delta_w_species;delta_w_hidden", "delta_y w_A=0 and relative w_A/w_B absent", "OPEN_COUNTERMODEL_IF_GRAMMAR_NOT_SIGNED"),
        ("GEX3889_2_hidden_marker", "theta_A(m), kappa_A(m), material/domain marker", "ordinary material constants are representation data, not hidden-field functions", "delta_w_marker;A_theta_matter", "delta_y theta_A=0 for hidden y", "OPEN_MINIMALITY_UNSIGNED"),
        ("GEX3889_3_shadow_frame", "g_A(y)=A_A(y)^2 g_obs + disformal terms", "one observed matter coframe before readout; no species hidden frame", "A_shadow_frame;c_g_like", "delta_y g_A=0 because g_A slot absent", "OPEN_EXTENSION_IF_ALLOWED"),
        ("GEX3889_4_alpha_mass", "alpha_EM(y)F^2, m_A(y), q_A y_mu J_A^mu", "constants/charges are q-basic representation parameters", "A_alpha_mass;b_theta", "delta_y alpha_EM=delta_y m_A=0", "OPEN_CONSTANT_VERTEX_UNSIGNED"),
        ("GEX3889_5_readout_worldtube", "w(W_source,Pi_M,readout,domain)", "source support/readout may not be selected after variation outside q", "A_worldtube_matter;delta_w_readout", "delta_y W_source=0 if support descends through q", "OPEN_SUPPORT_OWNER_UNSIGNED"),
        ("GEX3889_6_boundary_source", "Pi_local delta_y B_A or corner source term", "boundary/source terms must be q-basic, topological, or retained", "A_boundary_matter;epsilon_B_flux_abs", "boundary source zero only with no-flux/topological clause", "OPEN_BOUNDARY_RETAINED"),
    ]
    return [
        {
            "slot_id": row_id,
            "forbidden_or_controlled_slot": slot,
            "object_language_rule": rule,
            "fallback_quantity": fallback,
            "zero_if_signed": zero,
            "current_status": status,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
        for row_id, slot, rule, fallback, zero, status in raw_rows
    ]


def prediction_rows(timestamp: str) -> list[dict[str, object]]:
    raw_rows = [
        ("PRED3889_0_A_direct", "A_direct_matter", "E_star_norm", "A_direct_matter = ||delta_y V_m[X,rho_A,W_source]|_{X=0}||_{E*}", "R_source_direct <= U_B A_direct_matter", "MISSING_ESTAR_NORM_AND_COMPONENT_VALUE", "A_matter;WEP;source-normalization"),
        ("PRED3889_1_delta_w", "delta_w_A", "dimensionless", "delta_w_A = w_A/w_* - 1; delta_w_rel=max_AB|delta_w_A-delta_w_B|", "eta_source <= C_eta delta_w_rel; delta_beta_source includes C_beta^w delta_w_rel", "MISSING_SPECIES_BASIS_AND_CETA_CBETA", "WEP;beta;source calibration"),
        ("PRED3889_2_alpha3_boundary", "alpha3_pred", "dimensionless", "alpha3_pred = c_B_flux_to_alpha3 epsilon_B_flux_abs + c_proj_to_alpha3 ||T_extra|| + c_mem_to_alpha3 ||K_history||", "abs(alpha3_pred) <= 4e-20", "MISSING_PREDICTION_COEFFICIENTS_AND_INPUTS", "alpha3"),
        ("PRED3889_3_gamma_R11", "delta_gamma_R11", "dimensionless", "delta_gamma_R11 = sum_F C_gamma^F c_F + C_gamma^proj ||T_extra|| + C_gamma^readout epsilon_readout", "abs(delta_gamma_R11) <= 2.3e-05", "MISSING_WEAK_FIELD_MAP_COEFFICIENTS", "gamma_minus_1"),
        ("PRED3889_4_beta_source", "delta_beta_source", "dimensionless", "delta_beta_source = B_source/A_source^2 - 1 + C_beta^w delta_w_rel + C_beta^WT A_worldtube", "abs(delta_beta_source) <= 7.8e-05", "MISSING_A_SOURCE_B_SOURCE_AND_COUPLINGS", "beta_minus_1"),
        ("PRED3889_5_R10_alpha", "alpha_pred(lambda)", "range_dependent", "alpha_pred(lambda)=sum_X K_X(lambda) Q_X^H q_X^test / G_N + alpha_direct(lambda)", "abs(alpha_pred(lambda)) <= alpha_bound(lambda)", "MISSING_SOURCE_CHARGES_AND_REAL_BOUND_CURVE", "R10 fifth-force"),
        ("PRED3889_6_Gdot", "Gdot_over_G_pred", "yr^-1", "Gdot/G_pred = d_t ln(C_* Pi_M M_H) + d_t K_history + d_t epsilon_B_flux", "abs(Gdot/G_pred) <= 9.6e-15 yr^-1", "MISSING_TIME_PROFILE_AND_FRAME_LOCK", "Gdot"),
        ("PRED3889_7_projector", "Delta_PPN_projector", "dimensionless_vector", "Delta_PPN_projector = P_PPN[T_extra_munu] with components {delta_gamma,delta_beta,alpha_i,xi,zeta_i}", "each component below its row bound with no cancellation credit", "MISSING_PROJECTOR_VARIATION_AND_COMPONENT_MAP", "PPN;Bianchi"),
    ]
    return [
        {
            "prediction_id": row_id,
            "symbol": symbol,
            "units": units,
            "prediction_formula": formula,
            "pass_rule": pass_rule,
            "current_input_status": status,
            "observable_link": observable,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
        for row_id, symbol, units, formula, pass_rule, status, observable in raw_rows
    ]


def decision_rows(timestamp: str) -> list[dict[str, object]]:
    raw_rows = [
        ("DEC3889_0_observed_source", "observed q-basic matter source", "J_A^obs=0 remains conditionally derived from 3888", "PASS_CONDITIONAL"),
        ("DEC3889_1_object_language", "Hom_parent(H_hidden,M_source)=0", "would zero direct hidden/source slots without tuning", "THEOREM_READY_PARENT_UNSIGNED"),
        ("DEC3889_2_direct_slots", "direct matter/source slots", "all slot-specific exclusions have fallback quantities and prediction formulas", "PREDICTION_ROWS_READY_NONCLAIM"),
        ("DEC3889_3_bounds", "prediction side vs bound side", "prediction formulas exist but numeric coefficients/inputs are still missing", "BOUND_TEST_NOT_RUN"),
        ("DEC3889_4_local_GR", "local GR promotion", "blocked until object-language theorem is parent-signed or prediction coefficients pass bounds", "BLOCKED_NO_CLAIM"),
    ]
    return [
        {
            "decision_id": row_id,
            "gate": gate,
            "meaning": meaning,
            "status": status,
            "claim_allowed": False,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
        for row_id, gate, meaning, status in raw_rows
    ]


def runner_rows(timestamp: str) -> list[dict[str, object]]:
    raw_rows = [
        ("RUNU3889_0_Hom", "object_language_gate", "if Hom_parent(H_hidden,M_source)=0 and allowed syntax is parent-signed, set A_direct_matter=delta_w_A=A_alpha_mass=A_shadow_frame=0", "CONDITIONAL_ZERO_RULE"),
        ("RUNU3889_1_no_tuning", "slot_absence_guard", "zero is allowed only by absence of a typed slot, not by setting a free coefficient to zero after the fact", "NO_TUNED_ZERO"),
        ("RUNU3889_2_prediction", "coefficient_prediction_gate", "if a slot remains legal, evaluate its prediction formula against the bound row with no cancellation credit", "PREDICTION_SIDE_READY"),
        ("RUNU3889_3_claim", "local_GR_claim", "false until either all direct slots are parent-forbidden and residual-lock/R11 close, or all surviving coefficients are numeric and bounded", "NO_LOCAL_GR_CLAIM"),
        ("RUNU3889_4_next", "next_attack", "try to sign the parent grammar inside the candidate action; otherwise begin filling numerical coefficient inputs in priority order", "NEXT_3890"),
    ]
    return [
        {
            "update_id": row_id,
            "runner_field": field,
            "rule": rule,
            "status": status,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
        for row_id, field, rule, status in raw_rows
    ]


def next_rows(timestamp: str) -> list[dict[str, object]]:
    return [
        {
            "next_id": "NEXT3889_0",
            "target_checkpoint": "3890-Y5-R2FR-sign-parent-grammar-in-action-or-fill-numeric-coefficient-inputs.md",
            "script": "scripts/Y5_R2FR_3890_sign_parent_grammar_in_action_or_fill_numeric_coefficient_inputs.py",
            "objective": "attempt to insert/sign the Hom/no-marker object-language rule inside the candidate parent action; if not defensible, start numeric coefficient input fill in priority order: delta_w, A_direct, alpha3 boundary, beta source, gamma R11, R10 alpha(lambda), Gdot and projector stress",
            "why_next": "3889 makes the direct-source problem binary: parent grammar forbids the hidden source arrows, or the surviving arrows must be scored as prediction coefficients",
            "claim_allowed": False,
            "timestamp_utc": timestamp,
        }
    ]


def status_rows(timestamp: str) -> list[dict[str, object]]:
    return [
        {
            "status_id": "STATUS3889_0",
            "branch": BRANCH,
            "summary": "parent object-language Hom/no-marker exclusion theorem written as exact conditional route; direct-source slots mapped to fallback quantities; prediction-side coefficient formulas filled for the first local arenas; no local-GR claim",
            "claim_allowed": False,
            "timestamp_utc": timestamp,
        }
    ]


def write_doc(
    sources: list[dict[str, object]],
    theorem: list[dict[str, object]],
    grammar: list[dict[str, object]],
    predictions: list[dict[str, object]],
    decision: list[dict[str, object]],
    runner: list[dict[str, object]],
    next_target: list[dict[str, object]],
    timestamp: str,
) -> None:
    resolved = sum(1 for row in sources if row["exists"] and row["needle_found"])
    doc = f"""# 3889 - Parent Object-Language No-Direct-Source or Prediction Coefficient Fill

Generated: `{timestamp}`

## Result

3889 turns the direct-source problem into a sharp either/or.

Parent grammar candidate:

`{OBJECT_LANGUAGE_RULE}`

No-hidden-source arrow:

`{HOM_ZERO}`

Direct zero consequence:

`{DIRECT_ZERO}`

This is a useful theorem route because it does not say "the coupling is small"; it says the dangerous coupling is not a legal parent-language term. If the parent action signs that grammar, direct hidden matter/source terms vanish by absence of a slot. If not, 3889 now supplies prediction-side coefficient formulas so the surviving slots can be bounded rather than waved away.

## Object-Language Theorem Attempt

{markdown_table(theorem, ["theorem_id", "step", "statement_or_math", "result", "remaining_failure"])}

## Direct Slot Exclusion Matrix

{markdown_table(grammar, ["slot_id", "forbidden_or_controlled_slot", "object_language_rule", "fallback_quantity", "zero_if_signed", "current_status"])}

## Prediction-Side Coefficient Rows

{markdown_table(predictions, ["prediction_id", "symbol", "units", "prediction_formula", "pass_rule", "current_input_status"])}

## Route Decision Gate

{markdown_table(decision, ["decision_id", "gate", "meaning", "status", "claim_allowed"])}

## Runner Update

{markdown_table(runner, ["update_id", "runner_field", "rule", "status"])}

## Source Register

Resolved `{resolved}/{len(sources)}` source rows.

{markdown_table(sources, ["source_id", "path", "needle_found", "role"])}

## Next Target

{markdown_table(next_target, ["next_id", "target_checkpoint", "objective", "why_next"])}

## Bottom Line

This is the right kind of fork. Either MTS has a parent grammar where ordinary matter is a quotient-observed functor and hidden source arrows simply do not exist, or those arrows are physical residuals and must be scored. 3889 puts both paths in executable form instead of letting the theory hover between them.
"""
    DOC_PATH.write_text(doc, encoding="utf-8")


def update_spine(timestamp: str) -> None:
    start = "<!-- BEGIN 3889 OBJECT LANGUAGE NO DIRECT SOURCE -->"
    end = "<!-- END 3889 OBJECT LANGUAGE NO DIRECT SOURCE -->"
    block = f"""{start}

## 3889 - Parent object-language no-direct-source fork

Parent grammar:

`{OBJECT_LANGUAGE_RULE}`

No-hidden-source arrow:

`{HOM_ZERO}`

Direct zero consequence:

`{DIRECT_ZERO}`

Status: exact conditional route written. If parent-signed, direct hidden matter/source couplings vanish because they are not legal terms. If not signed, 3889 provides prediction-side coefficient formulas for delta_w, A_direct, alpha3 boundary, gamma_R11, beta_source, R10 alpha(lambda), Gdot and projector stress. Local GR remains nonclaim.

Generated outputs:
- `source-intake\\mts_residuals\\P8_Y5_R2FR_3889_PARENT_OBJECT_LANGUAGE_NO_DIRECT_SOURCE_THEOREM.csv`
- `source-intake\\mts_residuals\\P8_Y5_R2FR_3889_DIRECT_SLOT_EXCLUSION_MATRIX.csv`
- `source-intake\\mts_residuals\\P8_Y5_R2FR_3889_PREDICTION_SIDE_COEFFICIENT_ROWS.csv`
- `source-intake\\mts_residuals\\P8_Y5_BRR545_3889_VALIDATION.csv`

Next gate: `3890`, sign the parent grammar inside the candidate action or fill numeric coefficient inputs.

<!-- Generated by 3889 at {timestamp} -->
{end}
"""
    existing = read_text(SPINE_PATH) if SPINE_PATH.exists() else "# Local GR Coupling Spine Current State\n"
    if start in existing and end in existing:
        before = existing.split(start)[0].rstrip()
        after = existing.split(end, 1)[1].lstrip()
        new_text = f"{before}\n\n{block}\n\n{after}".rstrip() + "\n"
    else:
        new_text = existing.rstrip() + "\n\n" + block + "\n"
    SPINE_PATH.write_text(new_text, encoding="utf-8")


def validation_rows(
    sources: list[dict[str, object]],
    theorem: list[dict[str, object]],
    grammar: list[dict[str, object]],
    predictions: list[dict[str, object]],
    decision: list[dict[str, object]],
    runner: list[dict[str, object]],
    timestamp: str,
) -> list[dict[str, object]]:
    checks: list[tuple[str, str, bool, str]] = []
    resolved = sum(1 for row in sources if row["exists"] and row["needle_found"])
    checks.append(("VAL3889_0_sources", "all cited source paths exist and needles are found", resolved == len(sources), f"{resolved}/{len(sources)} sources resolved"))
    checks.append(("VAL3889_1_Hom_zero", "Hom no-hidden-source rule is explicit", any("Hom_parent(H_hidden,M_source)=0" in str(row["statement_or_math"]) for row in theorem), "OLT3889_2"))
    checks.append(("VAL3889_2_direct_zero", "direct derivative zero consequence is explicit", any("J_A^direct=0" in str(row["statement_or_math"]) for row in theorem), "OLT3889_3"))
    required_slots = {"V_m[X,rho_A,W_source]", "w_A(y,m,D,W) S_A", "theta_A(m), kappa_A(m), material/domain marker", "g_A(y)=A_A(y)^2 g_obs + disformal terms", "alpha_EM(y)F^2, m_A(y), q_A y_mu J_A^mu", "w(W_source,Pi_M,readout,domain)", "Pi_local delta_y B_A or corner source term"}
    found_slots = {str(row["forbidden_or_controlled_slot"]) for row in grammar}
    checks.append(("VAL3889_3_slot_coverage", "direct slot matrix covers hidden vertex/prefactor/marker/frame/constants/worldtube/boundary", required_slots.issubset(found_slots), f"{len(found_slots)} slots"))
    required_preds = {"A_direct_matter", "delta_w_A", "alpha3_pred", "delta_gamma_R11", "delta_beta_source", "alpha_pred(lambda)", "Gdot_over_G_pred", "Delta_PPN_projector"}
    found_preds = {str(row["symbol"]) for row in predictions}
    checks.append(("VAL3889_4_prediction_coverage", "prediction-side rows cover priority coefficient inputs", required_preds.issubset(found_preds), f"{len(found_preds)} predictions"))
    checks.append(("VAL3889_5_prediction_formulas", "every prediction row has a formula and pass rule", all(str(row["prediction_formula"]).strip() and str(row["pass_rule"]).strip() for row in predictions), "formulas present"))
    checks.append(("VAL3889_6_local_gr_no_claim", "route decision keeps local GR blocked", any(row["decision_id"] == "DEC3889_4_local_GR" and "BLOCKED" in str(row["status"]) for row in decision), "DEC3889_4"))
    checks.append(("VAL3889_7_all_nonclaim", "all generated analytic rows are nonclaim", all(str(row.get("valid_for_claim")) == "False" for collection in [theorem, grammar, predictions, decision, runner] for row in collection), "valid_for_claim=false"))
    checks.append(("VAL3889_8_runner", "runner distinguishes slot absence from tuned zero", any(row["runner_field"] == "slot_absence_guard" and "free coefficient" in str(row["rule"]) for row in runner), "RUNU3889_1"))
    checks.append(("VAL3889_9_doc", "markdown checkpoint exists with bottom line", DOC_PATH.exists() and "both paths in executable form" in read_text(DOC_PATH), rel(DOC_PATH)))
    checks.append(("VAL3889_10_spine", "spine updated with 3889 block", SPINE_PATH.exists() and "BEGIN 3889 OBJECT LANGUAGE NO DIRECT SOURCE" in read_text(SPINE_PATH), rel(SPINE_PATH)))
    csv_outputs = [path for key, path in OUTPUTS.items() if key != "validation"]
    csv_parse_ok = True
    parse_details = []
    for path in csv_outputs:
        try:
            parse_details.append(f"{path.name}:{len(read_csv_rows(path))}")
        except Exception as exc:
            csv_parse_ok = False
            parse_details.append(f"{path.name}:{exc}")
    checks.append(("VAL3889_11_csv_parse", "all generated CSV outputs parse", csv_parse_ok, "; ".join(parse_details)))
    formalization_hits = []
    if FWB.exists():
        formalization_hits = [path for path in FWB.rglob("*3889*") if path.is_file() and ("3889-Y5" in path.name or "P8_Y5_R2FR_3889" in path.name or "P8_Y5_BRR545_3889" in path.name)]
    checks.append(("VAL3889_12_formalization_untouched", "no generated 3889 files appear in formalization-workbench", not formalization_hits, f"{len(formalization_hits)} hits"))
    pycache_hits = [path for path in (PCW / "scripts").rglob("__pycache__") if path.is_dir()]
    checks.append(("VAL3889_13_no_pycache", "scripts __pycache__ removed", not pycache_hits, f"{len(pycache_hits)} pycache dirs"))
    checks.append(("VAL3889_14_next_target", "next target signs parent grammar or fills numeric coefficient inputs", any("sign-parent-grammar" in str(row["target_checkpoint"]) for row in next_rows(timestamp)), "3890 sign-parent-grammar"))
    return [
        {
            "check_id": check_id,
            "description": description,
            "status": "PASS" if passed else "FAIL",
            "detail": detail,
            "timestamp_utc": timestamp,
        }
        for check_id, description, passed, detail in checks
    ]


def main() -> int:
    timestamp = now_utc()
    sources = source_register_rows(timestamp)
    theorem = theorem_rows(timestamp)
    grammar = grammar_rows(timestamp)
    predictions = prediction_rows(timestamp)
    decision = decision_rows(timestamp)
    runner = runner_rows(timestamp)
    next_target = next_rows(timestamp)
    status = status_rows(timestamp)

    write_csv(OUTPUTS["sources"], sources)
    write_csv(OUTPUTS["theorem"], theorem)
    write_csv(OUTPUTS["grammar"], grammar)
    write_csv(OUTPUTS["predictions"], predictions)
    write_csv(OUTPUTS["decision"], decision)
    write_csv(OUTPUTS["runner"], runner)
    write_csv(OUTPUTS["next"], next_target)
    write_csv(OUTPUTS["status"], status)
    write_doc(sources, theorem, grammar, predictions, decision, runner, next_target, timestamp)
    update_spine(timestamp)

    for pycache in (PCW / "scripts").rglob("__pycache__"):
        shutil.rmtree(pycache, ignore_errors=True)

    validation = validation_rows(sources, theorem, grammar, predictions, decision, runner, timestamp)
    write_csv(OUTPUTS["validation"], validation)
    failed = [row for row in validation if row["status"] != "PASS"]
    if failed:
        for row in failed:
            print(f"FAIL {row['check_id']}: {row['detail']}")
        return 1
    print(f"{CHECKPOINT} PASS_OBJECT_LANGUAGE_OR_PREDICTION_FILL_FORK")
    print(rel(DOC_PATH))
    print(rel(OUTPUTS["validation"]))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

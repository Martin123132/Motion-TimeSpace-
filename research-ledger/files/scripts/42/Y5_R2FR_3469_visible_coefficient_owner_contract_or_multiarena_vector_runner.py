from __future__ import annotations

import csv
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "source-intake" / "mts_residuals"
DOC = ROOT / "3469-Y5-R2FR-visible-coefficient-owner-contract-or-multiarena-vector-runner.md"
FORMALIZATION = ROOT.parent / "formalization-workbench"
ETA_TIPT_BOUND = 2.8e-15

SOURCES: dict[str, dict[str, Any]] = {
    "script_3469": {"type": "local", "path": Path(__file__).resolve(), "role": "generator for this checkpoint"},
    "doc_3468": {"type": "local", "path": ROOT / "3468-Y5-R2FR-constant-sector-universality-or-hidden-SM-coefficient-morphism.md", "role": "3468 handoff"},
    "next_3468": {"type": "local", "path": OUT / "P8_Y5_R2FR_3468_NEXT_TARGET.csv", "role": "3469 target statement"},
    "theorem_3468": {"type": "local", "path": OUT / "P8_Y5_R2FR_3468_CONSTANT_SECTOR_THEOREM_ATTEMPT.csv", "role": "constant-sector theorem attempt"},
    "morphism_3468": {"type": "local", "path": OUT / "P8_Y5_R2FR_3468_HIDDEN_TO_SM_COEFFICIENT_MORPHISM_GATES.csv", "role": "hidden-to-SM coefficient morphism gates"},
    "vector_3468": {"type": "local", "path": OUT / "P8_Y5_R2FR_3468_RETAINED_COEFFICIENT_VECTOR.csv", "role": "retained coefficient vector"},
    "envelope_3468": {"type": "local", "path": OUT / "P8_Y5_R2FR_3468_NO_CANCELLATION_VECTOR_ENVELOPE.csv", "role": "no-cancellation vector envelope"},
    "arena_3468": {"type": "local", "path": OUT / "P8_Y5_R2FR_3468_ARENA_CROSSWALK.csv", "role": "arena crosswalk"},
    "no_species_contract": {"type": "local", "path": OUT / "P8_no_species_source_charge_CONTRACT.csv", "role": "constant-sector/source-charge contract"},
    "source_ward_contract": {"type": "local", "path": OUT / "P8_source_current_Ward_universality_CONTRACT.csv", "role": "source-current Ward contract"},
    "source_owner_contract": {"type": "local", "path": OUT / "P8_source_owner_parent_action_terms_CONTRACT.csv", "role": "source owner parent action terms"},
    "typing_2650": {"type": "local", "path": OUT / "P8_Y5_SOURCE_PREF_OBJECTLANG_2650_SOURCE_PREFACTOR_TYPING_GATE.csv", "role": "source-prefactor typing gate"},
    "direct_matter_2612": {"type": "local", "path": OUT / "P8_Y5_DIRECT_MATTER_GRAMMAR_GATE_2612_SOURCE_PREFACTOR_CLASSIFICATION.csv", "role": "direct alpha/mass vertex classification"},
    "alpha_bound_3465": {"type": "local", "path": OUT / "P8_Y5_R2FR_3465_ALPHA_ONLY_BOUND_CALCULATION.csv", "role": "alpha WEP bound"},
    "mass_product_3467": {"type": "local", "path": OUT / "P8_Y5_R2FR_3467_SOURCE_PRODUCT_COUPLING_ROWS.csv", "role": "mass product bound"},
    "local_bounds": {"type": "local", "path": ROOT / "source-intake" / "local_bounds" / "local_bound_claims.csv", "role": "local empirical bounds"},
    "damour_donoghue_arxiv": {"type": "external", "url": "https://arxiv.org/abs/1007.2792", "role": "DD coefficient charge framework"},
    "microscope_final": {"type": "external", "url": "https://arxiv.org/abs/2209.15487", "role": "MICROSCOPE WEP bound"},
}


def now() -> str:
    return datetime.now(timezone.utc).isoformat()


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    if not rows:
        raise ValueError(f"no rows for {path}")
    path.parent.mkdir(parents=True, exist_ok=True)
    fields: list[str] = []
    for row in rows:
        for key in row:
            if key not in fields:
                fields.append(key)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def md_table(rows: list[dict[str, Any]]) -> str:
    if not rows:
        return "_No rows._"
    fields: list[str] = []
    for row in rows:
        for key in row:
            if key not in fields:
                fields.append(key)
    header = "| " + " | ".join(fields) + " |"
    sep = "| " + " | ".join(["---"] * len(fields)) + " |"
    body: list[str] = []
    for row in rows:
        values = [str(row.get(field, "")).replace("\n", "<br>").replace("|", "/") for field in fields]
        body.append("| " + " | ".join(values) + " |")
    return "\n".join([header, sep, *body])


def parse_float(value: Any) -> float | None:
    if value is None:
        return None
    text = str(value).strip()
    if not text or text.lower() in {"n/a", "missing", "not_applicable"} or "MISSING" in text or "FOLDED" in text:
        return None
    try:
        return float(text)
    except ValueError:
        return None


def source_register() -> list[dict[str, Any]]:
    stamp = now()
    rows: list[dict[str, Any]] = []
    for source_id, meta in SOURCES.items():
        path = meta.get("path")
        url = meta.get("url", "")
        rows.append({
            "timestamp_utc": stamp,
            "source_id": source_id,
            "source_type": meta["type"],
            "source_path": str(path) if path else "",
            "source_url": url,
            "exists_or_url_present": bool(path.exists()) if isinstance(path, Path) else bool(url),
            "role": meta["role"],
            "valid_for_claim": False,
        })
    return rows


def vector_values() -> dict[str, dict[str, str]]:
    return {row["coefficient_id"]: row for row in read_csv(SOURCES["vector_3468"]["path"])}


def owner_contract() -> list[dict[str, Any]]:
    return [
        {
            "contract_id": "VCO3469_0_visible_coeff_sort",
            "required_clause": "Coeff_visible is a parent sort, not an arena/readout afterthought.",
            "mathematical_form": "Theta_vis in RepData_fixed union q^*C^\u221e(B_vis)",
            "if_signed": "visible coefficients have only fixed or quotient-basic dependence",
            "current_status": "CONTRACT_EXACT_PARENT_SORT_UNSIGNED",
            "source_path": str(SOURCES["theorem_3468"]["path"]),
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "contract_id": "VCO3469_1_no_hidden_to_visible_hom",
            "required_clause": "Hom(HiddenInvariant, Coeff_visible)=empty except constants.",
            "mathematical_form": "not exists f:I_hid -> {Z_EM,y_f,v_H/Lambda_QCD,mhat/Lambda_QCD,B_nuc,readout_coeff}",
            "if_signed": "hidden scalar morphisms cannot generate b_alpha, b_mhat, b_me, b_bind or b_readout",
            "current_status": "EXACT_CONDITIONAL_NOT_PARENT_SIGNED",
            "source_path": str(SOURCES["morphism_3468"]["path"]),
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "contract_id": "VCO3469_2_qbasic_chain_rule",
            "required_clause": "Theta_vis descends through q or is superselected.",
            "mathematical_form": "D_v Theta_vis = D(q^*Theta_bar)[v]=0 for v in ker(Dq)",
            "if_signed": "all visible coefficient slopes vanish in the local vertical branch",
            "current_status": "EXACT_CONDITIONAL_THEOREM",
            "source_path": str(SOURCES["theorem_3468"]["path"]),
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "contract_id": "VCO3469_3_variation_before_readout",
            "required_clause": "Hilbert/source and coefficient extraction happen before WEP/clock/R10 readout.",
            "mathematical_form": "delta S_parent -> owned currents/coefficients -> Pi_arena, not Pi_arena -> coefficients",
            "if_signed": "material/readout labels cannot create new active coefficients",
            "current_status": "CONDITIONAL_MATH_CLEAN_PARENT_INCOMPLETE",
            "source_path": str(SOURCES["typing_2650"]["path"]),
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "contract_id": "VCO3469_4_radiative_readout_preservation",
            "required_clause": "RG thresholds, Hodge maps, clocks and spectra are functorial in q-basic visible data.",
            "mathematical_form": "Theta_eff = R(Theta_vis,q-basic readout data) => D_v Theta_eff=0",
            "if_signed": "tree-level coefficient silence survives effective/readout reductions",
            "current_status": "UNSIGNED_PRESERVATION_REQUIREMENT",
            "source_path": str(SOURCES["theorem_3468"]["path"]),
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "contract_id": "VCO3469_5_common_calibration_guard",
            "required_clause": "Only a universal dimensionful scale may be absorbed into measured G/units.",
            "mathematical_form": "Delta_AB L_v ln C_common=0; dimensionless coefficient drifts remain residuals",
            "if_signed": "Newton/G calibration cannot hide alpha or mass-ratio drift",
            "current_status": "EXACT_COMMON_MODE_GUARD",
            "source_path": str(SOURCES["source_owner_contract"]["path"]),
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "contract_id": "VCO3469_6_contract_verdict",
            "required_clause": "VCO3469_0 through VCO3469_5 all parent-signed.",
            "mathematical_form": "VisibleCoefficientOwner => D_v Theta_vis=0 and retained vector theorem-zero",
            "if_signed": "b_alpha,b_mhat,b_me,b_bind,b_readout become structural zeros",
            "current_status": "CONTRACT_READY_NOT_PARENT_SIGNED_USE_RUNNER_SCHEMA",
            "source_path": str(SOURCES["theorem_3468"]["path"]),
            "claim_allowed": False,
            "valid_for_claim": False,
        },
    ]


def runner_schema() -> list[dict[str, Any]]:
    return [
        {
            "schema_id": "MAV3469_0_WEP_TiPt",
            "arena": "WEP_MICROSCOPE_TiPt",
            "observable": "eta_TiPt_abs",
            "formula": "sum_i abs(S_i^WEP * D_i_eff) + abs(direct/shadow/projector/readout) <= eta_bound",
            "required_inputs": "coefficient vector; material sensitivities; tau_WEP(lambda); source leg; no-cancellation policy",
            "currently_numeric": "b_alpha and b_mhat one-channel pieces only",
            "runner_status": "EXECUTABLE_DRYRUN_BLOCKED_BY_MISSING_VECTOR_ROWS",
            "source_path": str(SOURCES["envelope_3468"]["path"]),
            "valid_for_claim": False,
        },
        {
            "schema_id": "MAV3469_1_clocks",
            "arena": "CLOCKS_SPECTRA",
            "observable": "delta_ln_frequency_or_alpha_mass_ratio",
            "formula": "delta ln nu_A/nu_B = sum_i K_clock_i D_i_eff + readout_tail",
            "required_inputs": "clock sensitivity vector K_alpha,K_me,K_mhat,K_bind; source/time kernel; readout closure",
            "currently_numeric": "none in 3469",
            "runner_status": "SCHEMA_READY_INPUTS_MISSING",
            "source_path": str(SOURCES["source_ward_contract"]["path"]),
            "valid_for_claim": False,
        },
        {
            "schema_id": "MAV3469_2_R10",
            "arena": "R10_SHORT_RANGE",
            "observable": "alpha_lambda_prediction",
            "formula": "abs(alpha_pred(lambda)) <= alpha_bound(lambda); alpha_pred requires source/test numerator from b_alpha/current normalization",
            "required_inputs": "lambda; R10 bound curve; b_alpha numerator; source/test charge normalization; range kernel",
            "currently_numeric": "external bound curve exists elsewhere; MTS numerator missing",
            "runner_status": "SCHEMA_READY_NUMERATOR_MISSING",
            "source_path": str(SOURCES["theorem_3468"]["path"]),
            "valid_for_claim": False,
        },
        {
            "schema_id": "MAV3469_3_local_GR_Newton",
            "arena": "LOCAL_GR_NEWTON_SOURCE",
            "observable": "source_residual_vector",
            "formula": "J_source = kappa_common T_H + sum_i D_i_eff Q_i + q_retained; require differential terms zero/bounded",
            "required_inputs": "common calibration; Hilbert source owner; coefficient vector; q_retained/source residual rows; PPN second order",
            "currently_numeric": "common calibration guard only",
            "runner_status": "SCHEMA_READY_LOCAL_GR_CLAIM_BLOCKED",
            "source_path": str(SOURCES["source_owner_contract"]["path"]),
            "valid_for_claim": False,
        },
    ]


def wep_dryrun_rows(values: dict[str, dict[str, str]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for coeff_id in ("RCV3468_0_b_alpha", "RCV3468_1_b_mhat"):
        row = values[coeff_id]
        factor_text = row["material_or_readout_factor"].split("=")[-1]
        sensitivity = parse_float(factor_text)
        bound = parse_float(row["current_bound"])
        contribution = (sensitivity or 0.0) * (bound or 0.0)
        rows.append({
            "dryrun_id": f"WDR3469_{len(rows)}_{row['symbol']}",
            "arena": "WEP_MICROSCOPE_TiPt",
            "coefficient": row["symbol"],
            "sensitivity": f"{sensitivity:.12e}" if sensitivity is not None else "MISSING",
            "product_bound": f"{bound:.12e}" if bound is not None else "MISSING",
            "abs_contribution_if_saturated": f"{contribution:.12e}",
            "units": "dimensionless",
            "status": "NUMERIC_SINGLE_CHANNEL_ONLY",
            "source_path": row["source_path"],
            "valid_for_claim": False,
        })
    missing = [
        ("b_me", "MISSING_Delta_Q_me_or_clock_sensitivity", "MISSING_NUMERIC_BOUND"),
        ("b_bind", "MISSING_exact_binding_material_tensor", "FOLDED_ONLY_IN_PROXY_MASS_CHANNEL"),
        ("b_readout", "MISSING_arena_readout_sensitivity", "MISSING_NUMERIC_BOUND"),
        ("direct_shadow_projector", "MISSING_projection_sensitivities", "MISSING_NUMERIC_BOUND"),
    ]
    for symbol, sensitivity, bound in missing:
        rows.append({
            "dryrun_id": f"WDR3469_{len(rows)}_{symbol}",
            "arena": "WEP_MICROSCOPE_TiPt",
            "coefficient": symbol,
            "sensitivity": sensitivity,
            "product_bound": bound,
            "abs_contribution_if_saturated": "MISSING",
            "units": "dimensionless",
            "status": "BLOCKING_MISSING_VECTOR_INPUT",
            "source_path": str(SOURCES["vector_3468"]["path"]),
            "valid_for_claim": False,
        })
    known_sum = sum(parse_float(row["abs_contribution_if_saturated"]) or 0.0 for row in rows)
    rows.append({
        "dryrun_id": "WDR3469_SUMMARY",
        "arena": "WEP_MICROSCOPE_TiPt",
        "coefficient": "known_numeric_single_channel_sum",
        "sensitivity": "not_a_joint_fit",
        "product_bound": f"eta_bound={ETA_TIPT_BOUND:.12e}",
        "abs_contribution_if_saturated": f"{known_sum:.12e}",
        "units": "dimensionless",
        "status": "BLOCKED_NO_VECTOR_PASS_SINGLE_CHANNEL_CEILINGS_SATURATE_SEPARATELY",
        "source_path": str(SOURCES["envelope_3468"]["path"]),
        "valid_for_claim": False,
    })
    return rows


def blocker_ledger() -> list[dict[str, Any]]:
    return [
        {"blocker_id": "BLK3469_0_contract_signature", "arena": "all", "missing_input": "parent-signed no HiddenInvariant -> Coeff_visible theorem", "why_needed": "would zero b_alpha,b_mhat,b_me,b_bind,b_readout structurally", "fallback": "retain coefficient vector", "valid_for_claim": False},
        {"blocker_id": "BLK3469_1_tau_source_leg", "arena": "WEP/local", "missing_input": "tau_WEP(lambda) and S_E^q source leg", "why_needed": "splits product bounds into theory coefficients", "fallback": "bound products only", "valid_for_claim": False},
        {"blocker_id": "BLK3469_2_clock_sensitivities", "arena": "clocks", "missing_input": "K_clock_i for alpha, me, mhat, binding, readout", "why_needed": "turn retained vector into clock predictions", "fallback": "clock schema only", "valid_for_claim": False},
        {"blocker_id": "BLK3469_3_R10_numerator", "arena": "R10", "missing_input": "MTS alpha numerator/source-test normalization", "why_needed": "compare predicted alpha(lambda) to short-range bound curve", "fallback": "R10 schema blocked", "valid_for_claim": False},
        {"blocker_id": "BLK3469_4_exact_material_tensor", "arena": "WEP/nuclear", "missing_input": "exact b_me/b_bind isotope/alloy material tensor", "why_needed": "complete no-cancellation vector", "fallback": "proxy mhat-only row remains", "valid_for_claim": False},
        {"blocker_id": "BLK3469_5_local_source_second_order", "arena": "local_GR_Newton", "missing_input": "PPN/source-normalization second-order closure", "why_needed": "local GR claim requires more than first-order coefficient bounds", "fallback": "local source claim blocked", "valid_for_claim": False},
    ]


def claim_gates(contract_rows: list[dict[str, Any]], schema_rows: list[dict[str, Any]], dryrun_rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    contract_ready = any(row["contract_id"] == "VCO3469_6_contract_verdict" for row in contract_rows)
    schema_all = {row["arena"] for row in schema_rows} >= {"WEP_MICROSCOPE_TiPt", "CLOCKS_SPECTRA", "R10_SHORT_RANGE", "LOCAL_GR_NEWTON_SOURCE"}
    dryrun_summary = next(row for row in dryrun_rows if row["dryrun_id"] == "WDR3469_SUMMARY")
    return [
        {"gate_id": "CG3469_0_owner_contract_exact", "gate": "visible coefficient owner contract is explicit", "pass": contract_ready, "detail": "contract written, not parent-signed", "claim_allowed": False, "valid_for_claim": False},
        {"gate_id": "CG3469_1_owner_contract_signed", "gate": "visible coefficient owner theorem is signed", "pass": False, "detail": "parent proof still missing", "claim_allowed": False, "valid_for_claim": False},
        {"gate_id": "CG3469_2_runner_schema_multiarena", "gate": "WEP/clocks/R10/local source schema rows exist", "pass": schema_all, "detail": "multi-arena schema written", "claim_allowed": False, "valid_for_claim": False},
        {"gate_id": "CG3469_3_WEP_dryrun_honest_fail", "gate": "WEP dryrun blocks cancellation/pass claim", "pass": dryrun_summary["status"].startswith("BLOCKED"), "detail": dryrun_summary["status"], "claim_allowed": False, "valid_for_claim": False},
        {"gate_id": "CG3469_4_local_GR_claim", "gate": "local GR/Newton/Maxwell source coupling derived", "pass": False, "detail": "blocked by unsigned owner contract and missing vector inputs", "claim_allowed": False, "valid_for_claim": False},
    ]


def decision_ledger() -> list[dict[str, Any]]:
    return [
        {"decision_id": "DEC3469_0_contract", "decision": "Keep the visible-coefficient owner as an exact parent contract, not a claim.", "reason": "The clauses are now sharp but current evidence does not sign them.", "next_action": "Use as the proof target for future derivation attempts.", "claim_allowed": False, "valid_for_claim": False},
        {"decision_id": "DEC3469_1_runner", "decision": "Use the multi-arena vector schema as the empirical discipline tool.", "reason": "It shows exactly why WEP, clocks, R10 and local source coupling remain blocked without pretending the missing rows are harmless.", "next_action": "Fill the first missing vector input or turn schema into a standalone runner.", "claim_allowed": False, "valid_for_claim": False},
        {"decision_id": "DEC3469_2_next", "decision": "Next best step is a standalone vector runner with explicit input templates.", "reason": "3469 proves the schema shape; the next step should make it reusable for WEP first, then clocks/R10.", "next_action": "3470 should generate executable vector input templates and a dry-run runner that refuses claims until every retained row is numeric or theorem-zero.", "claim_allowed": False, "valid_for_claim": False},
    ]


def next_target() -> list[dict[str, Any]]:
    return [{
        "next_doc": "3470-Y5-R2FR-executable-coefficient-vector-runner-and-input-templates.md",
        "next_script": "scripts/Y5_R2FR_3470_executable_coefficient_vector_runner_and_input_templates.py",
        "objective": "Create reusable WEP-first coefficient-vector input templates and a runner that evaluates the no-cancellation envelope, then extend the schema hooks for clocks and R10.",
        "success_gate": "Runner reads coefficient products, sensitivities, theorem-zero flags and missing markers; it outputs pass only when every live component is numeric/theorem-zero and the absolute envelope is below bound.",
        "exclude": "GitHub action; formalization-workbench edits; public WEP/local-GR claim; cancellation pass; hiding dimensionless drifts in G_N.",
        "claim_allowed": False,
        "valid_for_claim": False,
    }]


def validate(outputs: dict[str, Path], source_rows: list[dict[str, Any]], contract_rows: list[dict[str, Any]], schema_rows: list[dict[str, Any]], dryrun_rows: list[dict[str, Any]], blocker_rows: list[dict[str, Any]], gate_rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    stamp = now()
    local_sources_ok = all(row["exists_or_url_present"] for row in source_rows if row["source_type"] == "local")
    contract_verdict = any(row["contract_id"] == "VCO3469_6_contract_verdict" and row["current_status"] == "CONTRACT_READY_NOT_PARENT_SIGNED_USE_RUNNER_SCHEMA" for row in contract_rows)
    schema_arenas = {row["arena"] for row in schema_rows}
    schema_ok = {"WEP_MICROSCOPE_TiPt", "CLOCKS_SPECTRA", "R10_SHORT_RANGE", "LOCAL_GR_NEWTON_SOURCE"}.issubset(schema_arenas)
    numeric_components = [row for row in dryrun_rows if row["status"] == "NUMERIC_SINGLE_CHANNEL_ONLY"]
    dryrun_summary = next(row for row in dryrun_rows if row["dryrun_id"] == "WDR3469_SUMMARY")
    dryrun_blocks = dryrun_summary["status"].startswith("BLOCKED") and len(numeric_components) == 2
    blockers_ok = len(blocker_rows) >= 5
    local_gr_blocked = any(row["gate_id"] == "CG3469_4_local_GR_claim" and row["pass"] is False for row in gate_rows)
    no_claim_rows = not any(
        str(value).lower() == "true"
        for rows in (contract_rows, schema_rows, dryrun_rows, blocker_rows, gate_rows)
        for row in rows
        for key, value in row.items()
        if key in {"claim_allowed", "valid_for_claim"}
    )
    parse_counts: list[str] = []
    csv_parse_ok = True
    for label, path in outputs.items():
        if label == "validation":
            continue
        try:
            parse_counts.append(f"{path.name}:{len(read_csv(path))}")
        except Exception as exc:
            parse_counts.append(f"{path.name}:ERROR:{exc}")
            csv_parse_ok = False
    formalization_ok = True
    formalization_detail = "formalization_exists=False"
    if FORMALIZATION.exists():
        matches = list(FORMALIZATION.rglob("*3469*"))
        formalization_ok = not matches
        formalization_detail = f"formalization_exists=True; 3469_outputs_in_formalization={len(matches)}"
    rows = [
        {"validation_id": "VAL3469_0_local_sources_exist", "pass": local_sources_ok, "detail": "all local sources exist", "timestamp_utc": stamp},
        {"validation_id": "VAL3469_1_contract_ready_unsigned", "pass": contract_verdict, "detail": "visible coefficient owner contract written and explicitly unsigned", "timestamp_utc": stamp},
        {"validation_id": "VAL3469_2_multiarena_schema", "pass": schema_ok, "detail": ";".join(sorted(schema_arenas)), "timestamp_utc": stamp},
        {"validation_id": "VAL3469_3_WEP_dryrun_blocks_claim", "pass": dryrun_blocks, "detail": dryrun_summary["status"], "timestamp_utc": stamp},
        {"validation_id": "VAL3469_4_blocker_ledger_present", "pass": blockers_ok, "detail": f"blockers={len(blocker_rows)}", "timestamp_utc": stamp},
        {"validation_id": "VAL3469_5_local_GR_claim_blocked", "pass": local_gr_blocked, "detail": "local source coupling remains false", "timestamp_utc": stamp},
        {"validation_id": "VAL3469_6_no_claim_rows", "pass": no_claim_rows, "detail": "all claim_allowed and valid_for_claim flags remain false", "timestamp_utc": stamp},
        {"validation_id": "VAL3469_7_csv_parse", "pass": csv_parse_ok, "detail": ";".join(parse_counts), "timestamp_utc": stamp},
        {"validation_id": "VAL3469_8_formalization_untouched_by_3469", "pass": formalization_ok, "detail": formalization_detail, "timestamp_utc": stamp},
    ]
    rows.append({"validation_id": "VAL3469_SUMMARY", "pass": all(str(row["pass"]).lower() == "true" for row in rows), "detail": "PASS" if all(str(row["pass"]).lower() == "true" for row in rows) else "FAIL", "timestamp_utc": stamp})
    return rows


def write_doc(source_rows: list[dict[str, Any]], contract_rows: list[dict[str, Any]], schema_rows: list[dict[str, Any]], dryrun_rows: list[dict[str, Any]], blocker_rows: list[dict[str, Any]], gate_rows: list[dict[str, Any]], decision_rows: list[dict[str, Any]], validation_rows: list[dict[str, Any]], next_rows: list[dict[str, Any]]) -> None:
    dryrun_summary = next(row for row in dryrun_rows if row["dryrun_id"] == "WDR3469_SUMMARY")
    doc = f"""# 3469 - Visible Coefficient Owner Contract Or Multi-Arena Vector Runner

**Current verdict:** the exact visible-coefficient owner contract is now written, but it is not parent-signed. The fallback is no longer prose: the retained vector has WEP, clocks, R10 and local-source runner schema rows.

**Concrete progress:** WEP dry-run now fails honestly. Alpha and mass have numeric one-channel components, but their saturated absolute sum is `{dryrun_summary['abs_contribution_if_saturated']}`, so no vector pass or cancellation claim is allowed.

## Source Register
{md_table(source_rows)}

## Visible Coefficient Owner Contract
{md_table(contract_rows)}

## Multi-Arena Runner Schema
{md_table(schema_rows)}

## WEP Vector Dry-Run
{md_table(dryrun_rows)}

## Blocker Ledger
{md_table(blocker_rows)}

## Claim Gates
{md_table(gate_rows)}

## Decision Ledger
{md_table(decision_rows)}

## Validation
{md_table(validation_rows)}

## Next Target
{md_table(next_rows)}

## Short Readout
- Contract: exact, sharp, and unsigned.
- Runner schema: WEP, clocks, R10 and local source coupling are all represented.
- WEP dry-run: alpha and mass components are numeric, but single-channel ceilings cannot be combined as a pass.
- Next: make a reusable input-template runner that refuses claims until every live vector component is numeric or theorem-zero.
"""
    DOC.write_text(doc, encoding="utf-8")


def main() -> None:
    source_rows = source_register()
    values = vector_values()
    contract_rows = owner_contract()
    schema_rows = runner_schema()
    dryrun_rows = wep_dryrun_rows(values)
    blocker_rows = blocker_ledger()
    gate_rows = claim_gates(contract_rows, schema_rows, dryrun_rows)
    decision_rows = decision_ledger()
    next_rows = next_target()
    outputs = {
        "source_register": OUT / "P8_Y5_R2FR_3469_SOURCE_REGISTER.csv",
        "contract": OUT / "P8_Y5_R2FR_3469_VISIBLE_COEFFICIENT_OWNER_CONTRACT.csv",
        "schema": OUT / "P8_Y5_R2FR_3469_MULTIARENA_VECTOR_RUNNER_SCHEMA.csv",
        "dryrun": OUT / "P8_Y5_R2FR_3469_WEP_VECTOR_DRYRUN.csv",
        "blockers": OUT / "P8_Y5_R2FR_3469_BLOCKER_LEDGER.csv",
        "claim_gates": OUT / "P8_Y5_R2FR_3469_CLAIM_GATES.csv",
        "decision": OUT / "P8_Y5_R2FR_3469_DECISION_LEDGER.csv",
        "next": OUT / "P8_Y5_R2FR_3469_NEXT_TARGET.csv",
        "validation": OUT / "P8_Y5_BRR545_3469_VALIDATION.csv",
    }
    write_csv(outputs["source_register"], source_rows)
    write_csv(outputs["contract"], contract_rows)
    write_csv(outputs["schema"], schema_rows)
    write_csv(outputs["dryrun"], dryrun_rows)
    write_csv(outputs["blockers"], blocker_rows)
    write_csv(outputs["claim_gates"], gate_rows)
    write_csv(outputs["decision"], decision_rows)
    write_csv(outputs["next"], next_rows)
    validation_rows = validate(outputs, source_rows, contract_rows, schema_rows, dryrun_rows, blocker_rows, gate_rows)
    write_csv(outputs["validation"], validation_rows)
    write_doc(source_rows, contract_rows, schema_rows, dryrun_rows, blocker_rows, gate_rows, decision_rows, validation_rows, next_rows)
    summary = next(row for row in validation_rows if row["validation_id"] == "VAL3469_SUMMARY")
    print(summary["detail"])
    print(DOC)


if __name__ == "__main__":
    main()

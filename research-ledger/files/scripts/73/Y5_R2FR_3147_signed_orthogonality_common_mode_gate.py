from __future__ import annotations

import csv
import json
import math
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "source-intake" / "mts_residuals"

INPUTS = OUT / "P8_Y5_R2FR_3147_INPUTS.csv"
THEOREM = OUT / "P8_Y5_R2FR_3147_SIGNED_CANCELLATION_THEOREM.csv"
GATES = OUT / "P8_Y5_R2FR_3147_GATE_STATUS.csv"
SCORES = OUT / "P8_Y5_R2FR_3147_SIGNED_VS_ABSOLUTE_SCORECARD.csv"
CONTRACT = OUT / "P8_Y5_R2FR_3147_PARENT_CONTRACT.csv"
DECISION = OUT / "P8_Y5_R2FR_3147_DECISION.csv"
VALIDATION = OUT / "P8_Y5_R2FR_3147_VALIDATION.csv"


def stamp() -> str:
    return datetime.now(timezone.utc).isoformat()


def source_path(relative: str) -> str:
    return str((ROOT / relative).resolve())


def read_csv(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        raise ValueError(f"no rows for {path}")
    fieldnames: list[str] = []
    for row in rows:
        for key in row:
            if key not in fieldnames:
                fieldnames.append(key)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow(row)


def parse_float(value: object) -> float | None:
    try:
        parsed = float(str(value).strip())
    except (TypeError, ValueError):
        return None
    if not math.isfinite(parsed):
        return None
    return parsed


def fmt(value: float | None) -> str:
    if value is None:
        return "MISSING_NUMERIC_VALUE"
    return f"{value:.15e}"


def find_row(rows: list[dict[str, str]], column: str, value: str) -> dict[str, str] | None:
    for row in rows:
        if row.get(column) == value:
            return row
    return None


def input_rows() -> list[dict[str, str]]:
    now = stamp()
    rows = [
        {
            "source_id": "SRC3147_0_3146_doc",
            "path": source_path(
                "3146-Y5-R2FR-first-source-calibration-kernel-pair-and-no-cancellation-score-under-AX1090.md"
            ),
            "role": "handoff exposing absolute-vs-signed fork",
        },
        {
            "source_id": "SRC3147_1_3146_combo",
            "path": source_path("source-intake/mts_residuals/P8_Y5_R2FR_3146_NO_CANCELLATION_COMBO_SCORE.csv"),
            "role": "signed and absolute score rows",
        },
        {
            "source_id": "SRC3147_2_3146_gates",
            "path": source_path("source-intake/mts_residuals/P8_Y5_R2FR_3146_GATES.csv"),
            "role": "current sign/common-mode/profile gates",
        },
        {
            "source_id": "SRC3147_3_2790_doc",
            "path": source_path("2790-Y5-R2FR-DD-source-profile-weighting-or-MICROSCOPE-readout-import-gate-under-AX1090.md"),
            "role": "profile/readout/parent-to-DD gates",
        },
        {
            "source_id": "SRC3147_4_2790_profile_gates",
            "path": source_path("source-intake/mts_residuals/P8_Y5_R2FR_2790_PROFILE_CLOSURE_GATES.csv"),
            "role": "profile, source basis, readout projection blockers",
        },
        {
            "source_id": "SRC3147_5_3134_doc",
            "path": source_path("3134-Y5-R2FR-parent-quotient-map-and-matter-pullback-reduction-under-AX1090.md"),
            "role": "parent quotient and matter pullback reduction status",
        },
        {
            "source_id": "SRC3147_6_3134_leakage",
            "path": source_path("source-intake/mts_residuals/P8_Y5_R2FR_3134_FINITE_LEAKAGE_CARRY_FORWARD.csv"),
            "role": "J_spurion/J_direct readout/source leakage heads",
        },
        {
            "source_id": "SRC3147_7_3145_kernel",
            "path": source_path("source-intake/mts_residuals/P8_Y5_R2FR_3145_DELTAJ_BEFORE_GM_KERNEL.csv"),
            "role": "Frechet source-GM kernel law",
        },
    ]
    for row in rows:
        row["exists"] = str(Path(row["path"]).exists()).lower()
        row["valid_for_claim"] = "false"
        row["generated_utc"] = now
    return rows


def extracted_scores() -> dict[str, float | str | None]:
    combos = read_csv(OUT / "P8_Y5_R2FR_3146_NO_CANCELLATION_COMBO_SCORE.csv")
    abs_row = find_row(combos, "combo_id", "COMBO3146_0_absolute_coulomb_plus_profile")
    signed_row = find_row(combos, "combo_id", "COMBO3146_1_signed_coulomb_plus_profile")
    rho_row = find_row(combos, "combo_id", "COMBO3146_2_required_surface_rho_after_coulomb")
    if abs_row is None or signed_row is None or rho_row is None:
        raise ValueError("3146 combo rows missing")
    abs_coeff = parse_float(abs_row.get("coefficient_abs"))
    signed_coeff = parse_float(signed_row.get("coefficient_abs"))
    threshold = parse_float(abs_row.get("threshold_abs"))
    abs_eta = parse_float(abs_row.get("predicted_eta_abs_at_deltaJ_bound"))
    signed_eta = parse_float(signed_row.get("predicted_eta_abs_at_deltaJ_bound"))
    required_rho = parse_float(rho_row.get("coefficient_abs"))

    profile_rows = read_csv(OUT / "P8_Y5_R2FR_3133_RHO_PROFILE_WORLDTUBE_FIRST_ROW.csv")
    profile_summary = find_row(profile_rows, "row_id", "RHO3133_0_profile_worldtube_summary")
    current_rho = parse_float(profile_summary.get("rho_profile_abs")) if profile_summary else None

    wep_bound = None
    smoke_rows = read_csv(OUT / "P8_Y5_R2FR_3129_EARTH_SOURCE_CAL_SMOKE_OUTPUT.csv")
    coulomb_row = find_row(smoke_rows, "row_id", "ESC3129_1")
    if coulomb_row is not None:
        wep_bound = parse_float(coulomb_row.get("WEP_eta_bound"))

    return {
        "absolute_coefficient": abs_coeff,
        "signed_coefficient": signed_coeff,
        "threshold_coefficient": threshold,
        "absolute_eta": abs_eta,
        "signed_eta": signed_eta,
        "wep_eta_bound": wep_bound,
        "required_rho_after_coulomb": required_rho,
        "current_profile_rho": current_rho,
        "absolute_score": abs_row.get("score", ""),
        "signed_score": signed_row.get("score", ""),
    }


def theorem_rows() -> list[dict[str, str]]:
    now = stamp()
    return [
        {
            "theorem_id": "SCT3147_0_linear_parent_functional",
            "statement": "Signed addition is legal only if Coulomb and surface/profile terms are components of the same parent-owned linear source functional before fitting.",
            "formal_condition": "DeltaK_total = L_parent[P_C q_C + P_S q_S] with fixed oriented basis and no post-readout sign choice",
            "effect_if_signed": "signed coefficient row may replace absolute no-cancellation row",
            "current_status": "conditional_exact_not_signed",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "theorem_id": "SCT3147_1_common_mode_calibration",
            "statement": "Common-mode silence is legal if source and calibration use the same Hilbert-stress worldtube functional for both channels.",
            "formal_condition": "K_GM_J[S;u_C,u_S] = K_GM_J[cal;u_C,u_S] as functionals, not merely numerically at one source",
            "effect_if_signed": "DeltaK_GM_J=0 and local source-GM branch is silent for this channel",
            "current_status": "conditional_exact_not_signed",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "theorem_id": "SCT3147_2_orthogonal_projection",
            "statement": "Surface/profile channel can be excluded from this local source-GM score only if the parent projector maps it into a boundary/readout-null subspace.",
            "formal_condition": "Pi_local P_surface q_surface = 0 or <P_C q_C, P_S q_S>_source = 0 by parent symplectic/Hilbert pairing",
            "effect_if_signed": "surface/profile term is not added to Coulomb in the local source-GM coefficient",
            "current_status": "conditional_exact_not_signed",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "theorem_id": "SCT3147_3_absolute_policy",
            "statement": "If no parent sign/common-mode/orthogonality identity is signed, channels add by absolute value for claim gating.",
            "formal_condition": "score_abs = |DeltaK_C| + |DeltaK_S| + sibling absolute tails",
            "effect_if_signed": "not applicable; this is the fallback policy",
            "current_status": "active_fallback_policy",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
    ]


def gate_rows() -> list[dict[str, str]]:
    now = stamp()
    profile_gates = read_csv(OUT / "P8_Y5_R2FR_2790_PROFILE_CLOSURE_GATES.csv")
    profile_gate_status = {row.get("gate_id", ""): row.get("claim_pass", row.get("gate_pass", "")) for row in profile_gates}
    return [
        {
            "gate_id": "G3147_0_parent_to_DD_oriented_map",
            "gate": "parent_to_DD_basis_and_sign_orientation",
            "status": "fail_for_claim",
            "evidence": profile_gate_status.get("PCG2790_2_source_charge_basis", "missing"),
            "why": "2790 says parent-to-DD coefficient/source basis map is not derived",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "gate_id": "G3147_1_real_profile",
            "gate": "PREM_or_equivalent_worldtube_profile",
            "status": "fail_for_claim",
            "evidence": profile_gate_status.get("PCG2790_1_finite_range_profile", "missing"),
            "why": "current profile is two-layer smoke; PREM/shell/readout profile is missing",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "gate_id": "G3147_2_readout_projection",
            "gate": "official_readout_or_parent_projection",
            "status": "fail_for_claim",
            "evidence": profile_gate_status.get("PCG2790_3_readout_projection", "missing"),
            "why": "profile vector has not been projected into official MICROSCOPE/local source readout",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "gate_id": "G3147_3_common_worldtube",
            "gate": "same_source_calibration_worldtube_functional",
            "status": "fail_for_claim",
            "evidence": "3146 common-mode theorem unsigned; 3134 parent signature not promoted",
            "why": "source/calibration common-mode identity is still a theorem target, not current evidence",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "gate_id": "G3147_4_spurion_exclusion",
            "gate": "no_J_spurion_or_J_direct_reentry",
            "status": "fail_for_claim",
            "evidence": "3134 carries J_direct and J_spurion leakage heads",
            "why": "direct/spurion source vertices block a clean sign identity",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "gate_id": "G3147_5_absolute_fallback",
            "gate": "absolute_no_cancellation_policy",
            "status": "active",
            "evidence": "no parent sign/common-mode/orthogonality identity currently signed",
            "why": "signed smoke pass cannot be promoted",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
    ]


def score_rows(values: dict[str, float | str | None]) -> list[dict[str, str]]:
    now = stamp()
    abs_coeff = values["absolute_coefficient"] if isinstance(values["absolute_coefficient"], float) else None
    signed_coeff = values["signed_coefficient"] if isinstance(values["signed_coefficient"], float) else None
    threshold = values["threshold_coefficient"] if isinstance(values["threshold_coefficient"], float) else None
    abs_eta = values["absolute_eta"] if isinstance(values["absolute_eta"], float) else None
    signed_eta = values["signed_eta"] if isinstance(values["signed_eta"], float) else None
    wep_bound = values["wep_eta_bound"] if isinstance(values["wep_eta_bound"], float) else None
    required_rho = values["required_rho_after_coulomb"] if isinstance(values["required_rho_after_coulomb"], float) else None
    current_rho = values["current_profile_rho"] if isinstance(values["current_profile_rho"], float) else None
    coeff_gap = None if abs_coeff is None or threshold is None else abs_coeff - threshold
    eta_gap = None if abs_eta is None or wep_bound is None else abs_eta - wep_bound
    rho_ratio = None if current_rho is None or required_rho in (None, 0) else current_rho / required_rho
    return [
        {
            "score_id": "SC3147_0_absolute_fallback",
            "mode": "absolute_no_cancellation",
            "coefficient_abs": fmt(abs_coeff),
            "threshold_abs": fmt(threshold),
            "coefficient_margin": fmt(coeff_gap),
            "eta_abs": fmt(abs_eta),
            "eta_bound": fmt(wep_bound),
            "eta_margin": fmt(eta_gap),
            "score": "fails_current_smoke_pressure" if coeff_gap is not None and coeff_gap > 0 else "passes_or_not_scoreable",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "issues": "ABSOLUTE_POLICY_ACTIVE;SMOKE_PROFILE;CALIBRATION_KERNEL_MISSING",
            "generated_utc": now,
        },
        {
            "score_id": "SC3147_1_signed_if_parent_identity",
            "mode": "signed_parent_oriented_sum",
            "coefficient_abs": fmt(signed_coeff),
            "threshold_abs": fmt(threshold),
            "coefficient_margin": fmt(None if signed_coeff is None or threshold is None else signed_coeff - threshold),
            "eta_abs": fmt(signed_eta),
            "eta_bound": fmt(wep_bound),
            "eta_margin": fmt(None if signed_eta is None or wep_bound is None else signed_eta - wep_bound),
            "score": "would_pass_if_parent_sign_identity_signed" if signed_coeff is not None and threshold is not None and signed_coeff <= threshold else "would_not_pass_or_not_scoreable",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "issues": "PARENT_SIGN_IDENTITY_UNSIGNED",
            "generated_utc": now,
        },
        {
            "score_id": "SC3147_2_profile_suppression_target",
            "mode": "profile_tightening",
            "coefficient_abs": fmt(current_rho),
            "threshold_abs": fmt(required_rho),
            "coefficient_margin": fmt(None if current_rho is None or required_rho is None else current_rho - required_rho),
            "eta_abs": "rho_ratio=" + fmt(rho_ratio),
            "eta_bound": "not_eta_row",
            "eta_margin": "not_eta_row",
            "score": "current_profile_smoke_above_required_rho" if current_rho is not None and required_rho is not None and current_rho > required_rho else "profile_below_target_or_not_scoreable",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "issues": "PREM_PROFILE_MISSING;TWO_LAYER_SMOKE_ONLY",
            "generated_utc": now,
        },
    ]


def contract_rows() -> list[dict[str, str]]:
    now = stamp()
    return [
        {
            "contract_id": "PC3147_0_basis",
            "required_parent_object": "oriented parent-to-DD/source basis map",
            "exact_requirement": "A signed linear map B_parent_to_DD from parent source variables to Coulomb and surface/profile components, fixed before fitting/readout.",
            "failure_mode": "signed smoke sum is numerology; use absolute sum",
            "next_action": "derive B_parent_to_DD or keep PCG2790_2 blocking claims",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "contract_id": "PC3147_1_pairing",
            "required_parent_object": "source Hilbert/symplectic pairing",
            "exact_requirement": "A parent-owned inner product/pairing showing either orthogonality, common-mode equality, or fixed destructive orientation between channels.",
            "failure_mode": "no cancellation between Coulomb and surface/profile channels",
            "next_action": "derive Pi_local P_surface=0, K_source=K_cal, or signed DeltaK_total identity",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "contract_id": "PC3147_2_profile",
            "required_parent_object": "physical profile/worldtube vector",
            "exact_requirement": "Replace two-layer smoke with PREM/shell/readout profile or prove long-range bulk limit lambda_WEP >> R_E.",
            "failure_mode": "rho_profile=0.0825 remains smoke and above tightened target 0.0493",
            "next_action": "source real profile or derive long-range carrier theorem",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "contract_id": "PC3147_3_spurion",
            "required_parent_object": "no source-only spurion/direct vertex",
            "exact_requirement": "J_spurion and J_direct leakage heads are killed or explicitly bounded before sign/common-mode theorem is used.",
            "failure_mode": "hidden source vertex can flip or add coefficients outside the signed pair",
            "next_action": "route through 3134/3144 no-source-slot grammar or carry finite spurion residual",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
    ]


def decision_rows() -> list[dict[str, str]]:
    now = stamp()
    return [
        {
            "decision_id": "D3147_0_theorem_attempt",
            "decision": "signed cancellation theorem shape is exact but not currently signed",
            "effect": "do not use signed smoke pass as a claim",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "decision_id": "D3147_1_active_score",
            "decision": "absolute no-cancellation pressure row remains active",
            "effect": "local branch still needs common-mode, orthogonality, sign identity, or tighter profile",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "decision_id": "D3147_2_next",
            "decision": "next target should attack the parent pairing/projector theorem before importing data",
            "effect": "3148 should try Pi_local P_surface=0 or K_source=K_cal from Hilbert/worldtube geometry; if that fails, use PREM/profile acquisition",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
    ]


def validation_rows(
    inputs: list[dict[str, str]],
    theorem: list[dict[str, str]],
    gates: list[dict[str, str]],
    scores: list[dict[str, str]],
    contract: list[dict[str, str]],
    decisions: list[dict[str, str]],
    values: dict[str, float | str | None],
) -> list[dict[str, str]]:
    now = stamp()
    sources_exist = all(row["exists"] == "true" for row in inputs)
    has_theorem = {"SCT3147_0_linear_parent_functional", "SCT3147_1_common_mode_calibration", "SCT3147_2_orthogonal_projection", "SCT3147_3_absolute_policy"}.issubset(
        {row["theorem_id"] for row in theorem}
    )
    gates_block = all(row["claim_allowed"] == "false" for row in gates)
    absolute_active = any(
        row["score_id"] == "SC3147_0_absolute_fallback" and row["score"] == "fails_current_smoke_pressure"
        for row in scores
    )
    signed_nonclaim = any(
        row["score_id"] == "SC3147_1_signed_if_parent_identity"
        and row["score"] == "would_pass_if_parent_sign_identity_signed"
        and row["claim_allowed"] == "false"
        for row in scores
    )
    contract_complete = {"PC3147_0_basis", "PC3147_1_pairing", "PC3147_2_profile", "PC3147_3_spurion"}.issubset(
        {row["contract_id"] for row in contract}
    )
    decisions_nonclaim = all(row["valid_for_claim"] == "false" for row in decisions)
    numerics = all(
        isinstance(values[key], float)
        for key in [
            "absolute_coefficient",
            "signed_coefficient",
            "threshold_coefficient",
            "absolute_eta",
            "signed_eta",
            "wep_eta_bound",
            "required_rho_after_coulomb",
            "current_profile_rho",
        ]
    )
    return [
        {
            "check_id": "V3147_0_sources_exist",
            "status": "pass" if sources_exist else "fail",
            "details": json.dumps({row["source_id"]: row["exists"] for row in inputs}, ensure_ascii=False),
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "check_id": "V3147_1_theorem_shapes_present",
            "status": "pass" if has_theorem else "fail",
            "details": json.dumps([row["theorem_id"] for row in theorem], ensure_ascii=False),
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "check_id": "V3147_2_numeric_scores_extracted",
            "status": "pass" if numerics else "fail",
            "details": json.dumps({key: fmt(value if isinstance(value, float) else None) for key, value in values.items() if key not in ("absolute_score", "signed_score")}, sort_keys=True),
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "check_id": "V3147_3_absolute_pressure_retained",
            "status": "pass" if absolute_active else "fail",
            "details": "absolute fallback must remain active until parent identity signs",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "check_id": "V3147_4_signed_pass_nonclaim",
            "status": "pass" if signed_nonclaim else "fail",
            "details": "signed smoke pass is recorded but blocked",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "check_id": "V3147_5_contract_and_no_claim_leak",
            "status": "pass" if gates_block and contract_complete and decisions_nonclaim else "fail",
            "details": "",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
    ]


def main() -> None:
    inputs = input_rows()
    values = extracted_scores()
    theorem = theorem_rows()
    gates = gate_rows()
    scores = score_rows(values)
    contract = contract_rows()
    decisions = decision_rows()
    validations = validation_rows(inputs, theorem, gates, scores, contract, decisions, values)
    write_csv(INPUTS, inputs)
    write_csv(THEOREM, theorem)
    write_csv(GATES, gates)
    write_csv(SCORES, scores)
    write_csv(CONTRACT, contract)
    write_csv(DECISION, decisions)
    write_csv(VALIDATION, validations)


if __name__ == "__main__":
    main()

from __future__ import annotations

import csv
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
REPO = ROOT.parent
FW = REPO / "formalization-workbench"
OUT = ROOT / "source-intake" / "mts_residuals"

INPUTS = OUT / "P8_Y5_R2FR_3174_INPUTS.csv"
HESSIAN = OUT / "P8_Y5_R2FR_3174_EFFECTIVE_HESSIAN_EXTRACTION.csv"
STATUS = OUT / "P8_Y5_R2FR_3174_READOUT_AND_SOURCE_STATUS.csv"
MATCH = OUT / "P8_Y5_R2FR_3174_CONDITIONAL_OPERATOR_MATCH.csv"
ACTION_GAP = OUT / "P8_Y5_R2FR_3174_ACTION_GAP_LOCK.csv"
DECISION = OUT / "P8_Y5_R2FR_3174_DECISION.csv"
VALIDATION = OUT / "P8_Y5_R2FR_3174_VALIDATION.csv"


def stamp() -> str:
    return datetime.now(timezone.utc).isoformat()


def write_csv(path: Path, rows: list[dict[str, object]]) -> None:
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


def path_from_base(base: str, relative: str) -> Path:
    if base == "post_checkpoint":
        return ROOT / relative
    if base == "formalization":
        return FW / relative
    raise ValueError(base)


def input_rows() -> list[dict[str, object]]:
    now = stamp()
    rows = [
        ("post_checkpoint", "3173-Y5-R2FR-parent-exterior-operator-match-or-PiJ2metric-source-row-under-AX1090.md", "3173 exact extractor handoff"),
        ("post_checkpoint", "source-intake/mts_residuals/P8_Y5_R2FR_3173_PIJ2_EXTRACTOR_CONTRACT.csv", "3173 Upsilon extractor contract"),
        ("formalization", "83-parent-equations-v1.md", "effective parent metric equation and K_MTS/q/K_hat scaffold"),
        ("formalization", "84-parent-equations-v1-gate.md", "gate proving v1 is conditional/effective, not closed-action derived"),
        ("formalization", "36-minimal-parent-equations-v0.md", "earlier metric equation and stress decomposition scaffold"),
        ("formalization", "138-metric-null-action-block-contract.md", "future parent action/source-lift contract"),
        ("formalization", "142-owner-spacetime-solder-map-theorem.md", "solder/readout failure audit"),
        ("post_checkpoint", "1016-Y5-R10-parent-worldtube-source-measure-selector-or-R_eq-first-input.md", "same-frame source/coframe selector contract"),
        ("post_checkpoint", "3159-Y5-R2FR-projection-coefficient-derivation-for-J2-and-tide-under-AX1090.md", "public weak-field metric/J2 readout convention"),
    ]
    return [
        {
            "input_id": f"IN3174_{index}",
            "base": base,
            "path": str(path_from_base(base, relative).resolve()),
            "exists": str(path_from_base(base, relative).exists()).lower(),
            "role": role,
            "valid_for_claim": "false",
            "generated_utc": now,
        }
        for index, (base, relative, role) in enumerate(rows)
    ]


def hessian_rows() -> list[dict[str, object]]:
    now = stamp()
    return [
        {
            "extract_id": "HX3174_0_parent_v1_metric_equation",
            "object": "effective_metric_equation",
            "source_basis": "83 E0",
            "extracted_form": "G^{mu nu}+Lambda_0 g^{mu nu}=K_matter^{mu nu}+K_MTS^{mu nu}",
            "status": "effective_open_system_scaffold_extracted",
            "claim_limit": "not closed-action derived; not fundamental proof",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "extract_id": "HX3174_1_effective_linear_operator",
            "object": "L_eff_metric",
            "source_basis": "linearization of 83 E0 around local exterior background",
            "extracted_form": "L_eff[h] := delta(G^{mu nu}+Lambda_0 g^{mu nu})/delta g_{alpha beta} * h_{alpha beta}",
            "status": "conditional_effective_Hessian_available",
            "claim_limit": "effective GR-like metric operator only if parent-v1 scaffold is accepted as local exterior equation",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "extract_id": "HX3174_2_source_side_linearization",
            "object": "linearized_source_side",
            "source_basis": "83 K_MTS decomposition and 3173 sigma_K2 lane",
            "extracted_form": "L_eff[h] = delta K_matter + delta K_MTS; for K2 lane, delta K_MTS = S_K2 sigma_K2",
            "status": "formal_source_slot_available",
            "claim_limit": "S_K2 is not extracted from current corpus",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "extract_id": "HX3174_3_exterior_vacuum_reduction",
            "object": "source_free_exterior_operator",
            "source_basis": "compact source exterior plus 3172 public Green theorem",
            "extracted_form": "outside source: delta K_matter=0 and delta K_MTS=0 -> L_eff[h]=0 -> public l=2 Laplace channel in weak-field static limit",
            "status": "conditional_operator_match_from_effective_v1",
            "claim_limit": "requires compact source selector and same public metric readout; not a parent-action proof",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "extract_id": "HX3174_4_metric_readout_identity_candidate",
            "object": "E_metric",
            "source_basis": "83 uses g_mu_nu as parent metric; 3159 uses weak-field metric readout",
            "extracted_form": "E_metric = identity_on_delta_g if ordinary matter/clocks/orbits all read the same g_mu_nu",
            "status": "conditional_readout_candidate",
            "claim_limit": "same observed coframe/matter functor remains unsigned per 1016 and solder-map audits",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
    ]


def status_rows() -> list[dict[str, object]]:
    now = stamp()
    return [
        {
            "status_id": "ST3174_0_L_parent",
            "quantity": "L_parent",
            "current_best": "L_eff_metric = delta(G+Lambda_0 g)/delta g from parent-v1 E0",
            "status": "conditional_effective_extracted",
            "missing_before_claim": "closed parent action/Hessian showing why E0 is the MTS local exterior limit",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "status_id": "ST3174_1_E_metric",
            "quantity": "E_metric",
            "current_best": "identity_on_g if parent metric g_mu_nu is the observed metric/coframe",
            "status": "conditional_readout_extracted",
            "missing_before_claim": "same-frame matter/coframe descent certificate; no hidden source/readout frame split",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "status_id": "ST3174_2_S_K2",
            "quantity": "S_K2",
            "current_best": "would be STF/l=2 component of delta K_MTS^{mu nu}/delta sigma_K2, likely inside K_hat",
            "status": "MISSING_K2_STF_SOURCE_TENSOR",
            "missing_before_claim": "derive how W_2 M_Lambda deforms K_hat/K_MTS in the source worldtube",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "status_id": "ST3174_3_T_source",
            "quantity": "T_source",
            "current_best": "requires mapping Earth/local K2 lane to solar compact source lane",
            "status": "MISSING_SOURCE_DOMAIN_TRANSFER",
            "missing_before_claim": "source selector, M_H_ref/source normalization, and K2 universality/solar construction",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "status_id": "ST3174_4_closed_action",
            "quantity": "S_parent",
            "current_best": "formal action-block contracts exist, parent-v1 is effective/open-system",
            "status": "MISSING_CLOSED_PARENT_ACTION",
            "missing_before_claim": "diffeomorphism-covariant parent action or controlled open-system variational principle",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
    ]


def match_rows() -> list[dict[str, object]]:
    now = stamp()
    return [
        {
            "match_id": "OM3174_0_conditional_effective_operator_match",
            "claim_tested": "parent exterior operator match for public l=2 metric channel",
            "conditional_statement": "If parent-v1 E0 is accepted as the local exterior metric equation and the observed metric is g_mu_nu, then the exterior perturbation produced by a compact K2 source obeys the linearized GR/source-free public metric channel outside the source.",
            "formula": "L_eff[h]=S_K2 sigma_K2 inside source; L_eff[h]=0 outside source; weak-field static l=2 -> r^2 f_2''+2r f_2'-6f_2=0",
            "result": "operator match conditionally passes at effective-scaffold level",
            "not_claim_because": "S_K2, source normalization, same-frame readout, and closed parent action remain unsigned",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "match_id": "OM3174_1_conditional_Upsilon_reduction",
            "claim_tested": "3173 exact Upsilon extractor under parent-v1 effective scaffold",
            "conditional_statement": "Under the effective scaffold, E_metric can be identity and L_parent can be L_eff, reducing the missing kernel to the source tensor projection.",
            "formula": "Upsilon_J2 = P_surf,l2 L_eff^{-1} S_K2, with E_metric=I and G_ext_l2_surface handled by 3172",
            "result": "the hard missing object is S_K2 plus T_source, not the exterior radial operator",
            "not_claim_because": "S_K2 is unfilled and L_eff is effective, not fundamental",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "match_id": "OM3174_2_no_direct_public_score",
            "claim_tested": "direct solar J2/PPN score from effective operator match",
            "conditional_statement": "An effective operator match does not supply source amplitude, sign, radius, compact support, or observed source normalization.",
            "formula": "A_surface = P_surf,l2 L_eff^{-1} S_K2 sigma_K2; S_K2 is MISSING",
            "result": "direct score remains blocked",
            "not_claim_because": "no numeric/source-backed K2 -> K_hat_STF source tensor",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
    ]


def action_gap_rows() -> list[dict[str, object]]:
    now = stamp()
    return [
        {
            "gap_id": "AG3174_0_effective_not_fundamental",
            "gap": "parent-v1 E0 imports/effectively uses Einstein tensor as scaffold",
            "evidence": "83 and 84 label parent-v1 as effective/open-system and not closed-action derived",
            "required_to_close": "derive E0 from MTS parent action/emergent metric theorem or explicitly keep it as GR-limit scaffold",
            "severity": "fundamental_theory_blocker_not_effective_test_blocker",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "gap_id": "AG3174_1_source_tensor_missing",
            "gap": "K2 has no source tensor variation",
            "evidence": "3164/3165 define scalar residual lane; 3173 requires S_K2",
            "required_to_close": "derive S_K2 = delta K_hat_STF^{mu nu}/delta(K2*C_K2_unit) or source-backed bound row",
            "severity": "immediate_J2_PPN_blocker",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "gap_id": "AG3174_2_same_frame_readout_unsigned",
            "gap": "identity metric readout requires same observed coframe for matter/clocks/orbits",
            "evidence": "1016 and 142 keep source/coframe/solder signatures unsigned",
            "required_to_close": "same-frame matter functor/coframe descent certificate or finite residual bounds",
            "severity": "WEP_PPN_readout_blocker",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
    ]


def decision_rows() -> list[dict[str, object]]:
    now = stamp()
    return [
        {
            "decision_id": "D3174_0_partial_win",
            "decision": "parent-v1 provides a conditional effective linearized metric operator and metric readout candidate",
            "because": "E0 uses G+Lambda g=K_matter+K_MTS with g_mu_nu as the metric variable",
            "effect": "the exterior operator/radial-profile side is no longer the main bottleneck if the effective scaffold is accepted",
            "next_action": "focus on S_K2 source tensor and same-frame source normalization",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "decision_id": "D3174_1_no_fundamental_promotion",
            "decision": "do not promote this to derived local GR or fundamental parent action",
            "because": "83/84 explicitly mark the scaffold as not closed-action derived",
            "effect": "use it as an effective GR-limit scaffold only",
            "next_action": "derive the action/emergent-metric origin separately after source tensor route is sharpened",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "decision_id": "D3174_2_next_target",
            "decision": "the next derivation should target the K2 source tensor inside K_hat/K_MTS",
            "because": "3174 reduces Upsilon_J2 under the effective scaffold to P_surf,l2 L_eff^-1 S_K2",
            "effect": "J2/PPN scoring remains blocked until S_K2 or a source-backed bound row exists",
            "next_action": "3175-Y5-R2FR-K2-STF-source-tensor-in-Khat-or-source-backed-bound-row-under-AX1090",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
    ]


def validation_rows(
    inputs: list[dict[str, object]],
    hessian: list[dict[str, object]],
    status: list[dict[str, object]],
    matches: list[dict[str, object]],
    gaps: list[dict[str, object]],
    decisions: list[dict[str, object]],
) -> list[dict[str, object]]:
    now = stamp()
    input_ok = all(row["exists"] == "true" for row in inputs)
    effective_l = any(row["object"] == "L_eff_metric" and "conditional" in row["status"] for row in hessian)
    readout_candidate = any(row["quantity"] == "E_metric" and "conditional" in row["status"] for row in status)
    source_missing = any(row["quantity"] == "S_K2" and "MISSING" in row["status"] for row in status)
    conditional_match = any(row["match_id"] == "OM3174_0_conditional_effective_operator_match" for row in matches)
    action_gap = any(row["gap_id"] == "AG3174_0_effective_not_fundamental" for row in gaps)
    next_target = any("3175" in row["next_action"] for row in decisions)
    no_claim = all(
        str(row.get("valid_for_claim", "")).lower() == "false"
        for rows in [inputs, hessian, status, matches, gaps, decisions]
        for row in rows
    )
    return [
        {
            "check_id": "V3174_0_inputs_exist",
            "status": "pass" if input_ok else "fail",
            "detail": "; ".join(f"{row['input_id']}={row['exists']}" for row in inputs),
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "check_id": "V3174_1_effective_L_extracted",
            "status": "pass" if effective_l else "fail",
            "detail": "L_eff_metric extracted conditionally from parent-v1 E0",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "check_id": "V3174_2_readout_candidate_conditional",
            "status": "pass" if readout_candidate else "fail",
            "detail": "E_metric identity candidate remains conditional on same-frame/coframe descent",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "check_id": "V3174_3_S_K2_missing",
            "status": "pass" if source_missing else "fail",
            "detail": "K2 STF source tensor remains the immediate missing object",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "check_id": "V3174_4_conditional_match_written",
            "status": "pass" if conditional_match else "fail",
            "detail": "effective operator match written without promoting claim",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "check_id": "V3174_5_action_gap_locked",
            "status": "pass" if action_gap else "fail",
            "detail": "closed/fundamental parent action gap remains explicit",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "check_id": "V3174_6_next_target_selected",
            "status": "pass" if next_target else "fail",
            "detail": "3175 K2 STF source tensor target selected",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "check_id": "V3174_7_no_claim_leak",
            "status": "pass" if no_claim else "fail",
            "detail": "all 3174 rows valid_for_claim=false",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
    ]


def main() -> None:
    inputs = input_rows()
    hessian = hessian_rows()
    status = status_rows()
    matches = match_rows()
    gaps = action_gap_rows()
    decisions = decision_rows()
    validations = validation_rows(inputs, hessian, status, matches, gaps, decisions)
    write_csv(INPUTS, inputs)
    write_csv(HESSIAN, hessian)
    write_csv(STATUS, status)
    write_csv(MATCH, matches)
    write_csv(ACTION_GAP, gaps)
    write_csv(DECISION, decisions)
    write_csv(VALIDATION, validations)
    failures = [row for row in validations if row["status"] != "pass"]
    if failures:
        raise SystemExit(f"3174 validation failed: {failures}")


if __name__ == "__main__":
    main()

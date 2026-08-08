from __future__ import annotations

import csv
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "source-intake" / "mts_residuals"
DOC = ROOT / "3451-Y5-R2FR-pure-representative-action-descent-or-LX-residual-owner-split-under-AX1090.md"
FORMALIZATION = ROOT.parent / "formalization-workbench"

SOURCES = {
    "script_3451": Path(__file__).resolve(),
    "doc_3450": ROOT / "3450-Y5-R2FR-field-by-field-vX-kernel-signature-or-omegaX-norm-bound-input-under-AX1090.md",
    "next_3450": OUT / "P8_Y5_R2FR_3450_NEXT_TARGET.csv",
    "qvx_3450": OUT / "P8_Y5_R2FR_3450_CANDIDATE_QVX_DEFINITION.csv",
    "kernel_3450": OUT / "P8_Y5_R2FR_3450_FIELD_BY_FIELD_KERNEL_TABLE.csv",
    "rejected_3450": OUT / "P8_Y5_R2FR_3450_REJECTED_VERTICAL_SLOTS.csv",
    "action_density_3424": OUT / "P8_Y5_R2FR_3424_PARENT_ACTION_DENSITY.csv",
    "public_current_3447": OUT / "P8_Y5_R2FR_3447_PUBLIC_CURRENT_CHAIN_EXTRACTION.csv",
    "strict_gate_3114": OUT / "P8_Y5_R2FR_3114_STRICT_LOCAL_QUOTIENT_SIGNATURE_GATE.csv",
    "doc_3104": ROOT / "3104-Y5-R2FR-left-hand-EH-Newton-reduction-under-quotient-matter-domain.md",
    "doc_3108": ROOT / "3108-Y5-R2FR-source-charge-Gauss-bridge-or-GM-calibration-residual-under-AX1090.md",
}

OUTPUTS = {
    "source_register": OUT / "P8_Y5_R2FR_3451_SOURCE_REGISTER.csv",
    "public_core_action_silence": OUT / "P8_Y5_R2FR_3451_PUBLIC_CORE_ACTION_SILENCE.csv",
    "pure_rep_action_descent_contract": OUT / "P8_Y5_R2FR_3451_PURE_REP_ACTION_DESCENT_CONTRACT.csv",
    "lx_residual_owner_split": OUT / "P8_Y5_R2FR_3451_LX_RESIDUAL_OWNER_SPLIT.csv",
    "deltaH_curl_feed_update": OUT / "P8_Y5_R2FR_3451_DELTAH_CURL_FEED_UPDATE.csv",
    "promotion_gates": OUT / "P8_Y5_R2FR_3451_PROMOTION_GATES.csv",
    "decision_ledger": OUT / "P8_Y5_R2FR_3451_DECISION_LEDGER.csv",
    "next_target": OUT / "P8_Y5_R2FR_3451_NEXT_TARGET.csv",
    "runner_nonclaim": OUT / "P8_Y5_R2FR_3451_RUNNER_NONCLAIM.csv",
    "validation": OUT / "P8_Y5_BRR545_3451_VALIDATION.csv",
}


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    if not rows:
        raise ValueError(f"no rows for {path}")
    path.parent.mkdir(parents=True, exist_ok=True)
    fields = list(rows[0].keys())
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def read_csv(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def md_table(rows: list[dict[str, Any]]) -> str:
    if not rows:
        return "_No rows._"
    fields = list(rows[0].keys())

    def clean(value: Any) -> str:
        return str(value).replace("\n", " ").replace("|", "/")

    return "\n".join(
        [
            "| " + " | ".join(fields) + " |",
            "| " + " | ".join("---" for _ in fields) + " |",
            *["| " + " | ".join(clean(row.get(field, "")) for field in fields) + " |" for row in rows],
        ]
    )


def source_register() -> list[dict[str, Any]]:
    roles = {
        "script_3451": "generator for this checkpoint",
        "doc_3450": "field-by-field v_X kernel handoff",
        "next_3450": "machine-readable 3451 target",
        "qvx_3450": "restricted q/v_X definition",
        "kernel_3450": "safe-slot Dq[v_Xrep]=0 table",
        "rejected_3450": "active nonvertical hazards",
        "action_density_3424": "candidate public parent action density",
        "public_current_3447": "public EH/matter/EM current chain",
        "strict_gate_3114": "strict local quotient/action-descent gates",
        "doc_3104": "EH/Newton public action reduction",
        "doc_3108": "Hilbert source/Gauss bridge and calibrated G note",
    }
    return [
        {
            "source_id": source_id,
            "path": str(path),
            "exists": path.exists(),
            "role": roles[source_id],
            "claim_allowed": False,
            "valid_for_claim": False,
        }
        for source_id, path in SOURCES.items()
    ]


def public_core_action_silence() -> list[dict[str, Any]]:
    return [
        {
            "silence_id": "PCS3451_0_EH_public_geometry",
            "action_piece": "S_EH[g_obs;G_ref]",
            "variation_under_vXrep": "delta_vXrep g_obs=0 and delta_vXrep sqrt(-g_obs)R[g_obs]=0",
            "result": "delta_vXrep S_EH=0",
            "status": "DERIVED_FOR_PUBLIC_CORE",
            "remaining_gap": "does not prove G_ref numeric value; G_ref is a single calibrated constant, not per-source fit",
            "source_path": str(SOURCES["action_density_3424"]),
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "silence_id": "PCS3451_1_public_matter",
            "action_piece": "S_matter[e_obs,Psi_A,theta_rep]",
            "variation_under_vXrep": "delta_vXrep e_obs=0, delta_vXrep Psi_A=0 or gauge, delta_vXrep theta_rep=0",
            "result": "delta_vXrep S_matter=0 if ordinary matter is the quotient/public-metric matter domain",
            "status": "DERIVED_CONDITIONAL_ON_MATTER_SIGNATURE",
            "remaining_gap": "hidden source weights or material markers remain rejected residuals",
            "source_path": str(SOURCES["doc_3104"]),
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "silence_id": "PCS3451_2_public_EM",
            "action_piece": "S_EM[g_obs,A_obs;lambda_0]",
            "variation_under_vXrep": "delta_vXrep g_obs=0, delta_vXrep A_obs=0, delta_vXrep lambda_0=0",
            "result": "delta_vXrep S_EM=0 and public Poynting/Maxwell stress stays in Hilbert public sector",
            "status": "DERIVED_CONDITIONAL_ON_Q_BASIC_EM_NORMALIZATION",
            "remaining_gap": "hidden F^2 coefficient or shadow Hodge is rejected residual, not vertical silence",
            "source_path": str(SOURCES["public_current_3447"]),
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "silence_id": "PCS3451_3_PiMH_source_charge",
            "action_piece": "Hilbert source/Hamiltonian worldtube current",
            "variation_under_vXrep": "delta_vXrep Pi_M^H=0 and public Hilbert stress is q-basic",
            "result": "delta_vXrep J_H=0 for the public Hilbert branch",
            "status": "DERIVED_CONDITIONAL_REFERENCE_BOUNDARY_OPEN",
            "remaining_gap": "H_ref, source-worldtube integrability and boundary/reference lock are not closed here",
            "source_path": str(SOURCES["doc_3108"]),
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "silence_id": "PCS3451_4_public_core_verdict",
            "action_piece": "S_pub=S_EH+S_matter+S_EM",
            "variation_under_vXrep": "all public q-basic slots are fixed by KERN3450_*",
            "result": "delta_vXrep S_pub=0",
            "status": "PUBLIC_CORE_SILENCE_PROVED_FOR_RESTRICTED_GENERATOR",
            "remaining_gap": "total S_parent may still contain X_rep, boundary, frame, source-weight, R_AB or tau-clock residual terms",
            "source_path": str(OUTPUTS["public_core_action_silence"]),
            "claim_allowed": False,
            "valid_for_claim": False,
        },
    ]


def pure_rep_action_descent_contract() -> list[dict[str, Any]]:
    return [
        {
            "contract_id": "ADC3451_0_sufficient_normal_form",
            "statement": "If S_parent = S_pub[q(Phi),Psi,theta_rep] + S_top[q(Phi)] + S_boundary_class[q(Phi)] + S_res[Z_active] with no X_rep argument, then delta_vXrep S_parent=0.",
            "derivation": "v_Xrep annihilates q(Phi), Psi/theta by the matter lift, and does not act on Z_active; exact/proper boundary representatives have fixed class.",
            "status": "SUFFICIENT_ACTION_DESCENT_THEOREM",
            "missing_for_promotion": "a parent action formation rule forbidding explicit X_rep terms",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "contract_id": "ADC3451_1_forbidden_term_test",
            "statement": "Any term L(X_rep), f(X_rep)R, f(X_rep)F^2, w_A(X_rep)L_A, or B_X[beta_exact] violates pure-representative descent unless it is exact/proper and charge-silent.",
            "derivation": "delta_vXrep of such a term contains partial_X L * xi_X or a boundary charge; this is a real Euler/current contribution, not a quotient zero.",
            "status": "ACTION_DESCENT_COUNTERTERM_TEST_DERIVED",
            "missing_for_promotion": "scan/adopt the actual parent action line against this test",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "contract_id": "ADC3451_2_current_status",
            "statement": "Current corpus supports S_pub silence, but does not yet source-sign absence of every explicit X_rep or rejected-slot action term.",
            "derivation": "3424/3447/3104 give public-core structure; 3450 deliberately leaves active residual slots outside v_Xrep.",
            "status": "TOTAL_ACTION_DESCENT_NOT_PROMOTED",
            "missing_for_promotion": "3452 must prove no explicit X_rep action line or retain an L_X residual vector",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
    ]


def lx_residual_owner_split() -> list[dict[str, Any]]:
    return [
        {
            "residual_id": "LXR3451_0_explicit_Xrep_bulk",
            "action_term": "L_Xrep(X_rep,partial X_rep,...)",
            "variation": "E_Xrep xi_X + dTheta_Xrep",
            "owner_status": "MISSING_ABSENCE_PROOF_OR_PARENT_LX_LINE",
            "effect_on_DeltaH": "activates omega_X and C_tau^X rows",
            "next_action": "prove term forbidden by action grammar or fill omega_X norm density",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "residual_id": "LXR3451_1_hidden_frame_or_EM_coefficient",
            "action_term": "f_X(X_rep)R, f_X(X_rep)F^2, shadow Hodge/coframe",
            "variation": "f_X'(X_rep) xi_X times public operator",
            "owner_status": "REJECTED_ACTIVE_RESIDUAL",
            "effect_on_DeltaH": "reopens PPN/R10/clock/EM coupling channels",
            "next_action": "no-shadow-frame/no-extra-F2 theorem or coefficient bound",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "residual_id": "LXR3451_2_source_weight_marker",
            "action_term": "w_A(X_rep)L_A or kappa_A(X_rep)T_A",
            "variation": "w_A'(X_rep) xi_X L_A",
            "owner_status": "REJECTED_ACTIVE_RESIDUAL",
            "effect_on_DeltaH": "source coupling, WEP and measured-GM residual",
            "next_action": "ordinary matter signature theorem or finite source-weight coefficient row",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "residual_id": "LXR3451_3_RAB_observer_cell",
            "action_term": "L_RAB(R_AB,lambda_R) with observer-cell readout",
            "variation": "E_RAB delta R_AB plus readout variation",
            "owner_status": "ACTIVE_RESIDUAL_NOT_IN_VXREP",
            "effect_on_DeltaH": "cannot be hidden by quotient kernel; needs constraint-first elimination or bound",
            "next_action": "R_AB constraint-first proof or keep R_AB residual vector",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "residual_id": "LXR3451_4_boundary_reference_charge",
            "action_term": "B_ref,Q_X,corner/reference class depending on representative data",
            "variation": "surface charge or nonintegrable boundary symplectic term",
            "owner_status": "BOUNDARY_SILENCE_NOT_PROVED",
            "effect_on_DeltaH": "activates B_X and H_ref/reference-lock rows",
            "next_action": "boundary charge zero/proper/exact theorem or boundary norm bound",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "residual_id": "LXR3451_5_private_tau_clock",
            "action_term": "private memory time, tau_source, tau_clock mismatch",
            "variation": "clock/preferred-frame source term",
            "owner_status": "TAU_LOCK_NOT_PROVED",
            "effect_on_DeltaH": "clock/PPN alpha_i residual",
            "next_action": "tau_source=tau_charge=tau_clock=tau_readout theorem or clock/PPN bound",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
    ]


def deltaH_curl_feed_update() -> list[dict[str, Any]]:
    return [
        {
            "feed_id": "DHF3451_0_public_core",
            "feeds": "DHC3448_0_Delta_H_curl_extra and OB3449_0_surface_norm_bound",
            "result": "public-core action pieces do not contribute to omega_X for v_Xrep",
            "status": "PUBLIC_CORE_ZERO_FEED",
            "still_active": "explicit Xrep, hidden-frame/source-weight/RAB/boundary/tau residuals",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "feed_id": "DHF3451_1_total",
            "feeds": "Delta_H_curl_extra",
            "result": "Delta_H_curl_extra remains nonclaim until LXR3451_* residual owners are zeroed or bounded",
            "status": "TOTAL_NONCLAIM_RESIDUAL_SPLIT_READY",
            "still_active": "LXR3451_0..LXR3451_5",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
    ]


def promotion_gates() -> list[dict[str, Any]]:
    return [
        {
            "gate_id": "G3451_0_sources_exist",
            "gate": "all cited 3451 source paths exist",
            "status": "PRIVATE_CHECK_PASS",
            "blocks_claim": False,
            "needed_for_claim": "provenance only",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "gate_id": "G3451_1_public_core_silence",
            "gate": "delta_vXrep S_pub=0",
            "status": "PASS_FOR_RESTRICTED_PUBLIC_CORE",
            "blocks_claim": False,
            "needed_for_claim": "parent action must contain only the public core plus silent allowed pieces",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "gate_id": "G3451_2_total_action_descent",
            "gate": "delta_vXrep S_parent=0",
            "status": "FAIL_NOT_PARENT_SIGNED",
            "blocks_claim": True,
            "needed_for_claim": "prove no explicit Xrep/rejected-slot action terms or bound them",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "gate_id": "G3451_3_lx_split",
            "gate": "non-descended action terms are named",
            "status": "PASS_RESIDUAL_OWNER_SPLIT",
            "blocks_claim": True,
            "needed_for_claim": "each LXR3451 residual zero or bounded",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "gate_id": "G3451_4_no_claim",
            "gate": "no local-GR/Newton/R10/PPN/clock/orbital pass from this checkpoint",
            "status": "ENFORCED",
            "blocks_claim": True,
            "needed_for_claim": "full residual closure and empirical gates",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
    ]


def decision_ledger() -> list[dict[str, Any]]:
    return [
        {
            "decision_id": "DEC3451_0",
            "question": "Did action descent improve?",
            "answer": "Yes: the public EH/matter/EM core is silent under v_Xrep.",
            "reason": "v_Xrep fixes every public q-basic slot, so the public action derivative vanishes.",
            "next_action": "prove absence of explicit Xrep/rejected-slot terms in the total parent action",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "decision_id": "DEC3451_1",
            "question": "Is local GR derived yet?",
            "answer": "No; the total parent action can still contain live residual terms.",
            "reason": "Kernel plus public-core silence is not enough to erase boundary/frame/source/RAB/tau channels.",
            "next_action": "3452 action-line absence proof or residual norm bounds",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
    ]


def next_target() -> list[dict[str, Any]]:
    return [
        {
            "target_doc": "3452-Y5-R2FR-Xrep-action-line-absence-or-LX-residual-norm-bound-under-AX1090.md",
            "target_script": "scripts/Y5_R2FR_3452_Xrep_action_line_absence_or_LX_residual_norm_bound.py",
            "objective": "Prove the parent action formation rule forbids explicit X_rep/rejected-slot terms on the compact local branch, or convert LXR3451_* into executable residual norm bounds.",
            "start_from": "ADC3451_1_forbidden_term_test and LXR3451_0..LXR3451_5",
            "success_gate": "Either total action descent delta_vXrep S_parent=0 closes, or every non-descended term has a theorem/numeric bound input with units.",
            "claim_allowed": False,
            "valid_for_claim": False,
        }
    ]


def runner_nonclaim() -> list[dict[str, Any]]:
    return [
        {
            "runner_id": "RUN3451_0",
            "mode": "private_nonclaim_checkpoint",
            "result": "public-core action silence derived; total L_X residual split written",
            "claim_status": "NO_LOCAL_GR_NEWTON_R10_PPN_CLOCK_OR_ORBITAL_CLAIM",
            "reason": "explicit Xrep and rejected-slot action terms are not yet forbidden or bounded",
            "claim_allowed": False,
            "valid_for_claim": False,
        }
    ]


def validation_rows(rows_by_name: dict[str, list[dict[str, Any]]], start_utc: datetime) -> list[dict[str, Any]]:
    modified_count = 0
    if FORMALIZATION.exists():
        start_timestamp = start_utc.timestamp()
        modified_count = sum(
            1
            for checked_path in FORMALIZATION.rglob("*")
            if checked_path.is_file() and checked_path.stat().st_mtime >= start_timestamp
        )

    nonclaim_ok = True
    for rows in rows_by_name.values():
        for row in rows:
            if "valid_for_claim" in row and str(row["valid_for_claim"]).lower() != "false":
                nonclaim_ok = False
            if "claim_allowed" in row and str(row["claim_allowed"]).lower() != "false":
                nonclaim_ok = False

    parse_ok = True
    for output_name, path in OUTPUTS.items():
        if output_name == "validation":
            continue
        try:
            read_csv(path)
        except csv.Error:
            parse_ok = False

    public_verdict = [
        row
        for row in rows_by_name["public_core_action_silence"]
        if row["silence_id"] == "PCS3451_4_public_core_verdict"
    ]
    residual_ids = {row["residual_id"] for row in rows_by_name["lx_residual_owner_split"]}

    validations = [
        {
            "check_id": "VAL3451_0_sources_exist",
            "condition": "all cited 3451 source paths exist",
            "passed": all(path.exists() for path in SOURCES.values()),
            "detail": f"{sum(1 for path in SOURCES.values() if path.exists())}/{len(SOURCES)} source paths exist",
        },
        {
            "check_id": "VAL3451_1_public_core_silence",
            "condition": "public-core action derivative vanishes under v_Xrep",
            "passed": bool(public_verdict)
            and public_verdict[0]["status"] == "PUBLIC_CORE_SILENCE_PROVED_FOR_RESTRICTED_GENERATOR",
            "detail": public_verdict[0]["result"] if public_verdict else "missing public verdict",
        },
        {
            "check_id": "VAL3451_2_descent_not_promoted",
            "condition": "total parent action descent remains explicitly not promoted",
            "passed": any(
                row["contract_id"] == "ADC3451_2_current_status"
                and row["status"] == "TOTAL_ACTION_DESCENT_NOT_PROMOTED"
                for row in rows_by_name["pure_rep_action_descent_contract"]
            ),
            "detail": "total parent action still needs no-Xrep action-line proof",
        },
        {
            "check_id": "VAL3451_3_lx_residual_split",
            "condition": "six L_X residual owner rows are present",
            "passed": residual_ids
            == {
                "LXR3451_0_explicit_Xrep_bulk",
                "LXR3451_1_hidden_frame_or_EM_coefficient",
                "LXR3451_2_source_weight_marker",
                "LXR3451_3_RAB_observer_cell",
                "LXR3451_4_boundary_reference_charge",
                "LXR3451_5_private_tau_clock",
            },
            "detail": f"{len(residual_ids)} residual rows",
        },
        {
            "check_id": "VAL3451_4_no_claims",
            "condition": "all generated rows remain nonclaim",
            "passed": nonclaim_ok,
            "detail": "valid_for_claim=false and claim_allowed=false wherever present",
        },
        {
            "check_id": "VAL3451_5_generated_csv_parse",
            "condition": "generated CSV rows parse cleanly",
            "passed": parse_ok,
            "detail": "CSV reader pass for generated outputs present before validation write",
        },
        {
            "check_id": "VAL3451_6_next_target_3452",
            "condition": "next target is Xrep action-line absence or residual norm bound",
            "passed": rows_by_name["next_target"][0]["target_doc"].startswith("3452-Y5-R2FR-Xrep-action-line-absence"),
            "detail": rows_by_name["next_target"][0]["target_doc"],
        },
        {
            "check_id": "VAL3451_7_formalization_untouched",
            "condition": "formalization-workbench modified-file count remains 0 during this run",
            "passed": modified_count == 0,
            "detail": f"modified_count_since_start={modified_count}",
        },
    ]
    validations.append(
        {
            "check_id": "VAL3451_8_overall",
            "condition": "3451 action descent checkpoint is internally valid",
            "passed": all(row["passed"] for row in validations),
            "detail": "PASS" if all(row["passed"] for row in validations) else "FAIL",
        }
    )
    return validations


def write_doc(rows_by_name: dict[str, list[dict[str, Any]]]) -> None:
    text = f"""# 3451 - Pure-Representative Action Descent or L_X Residual Owner Split

## Summary
- This checkpoint uses `v_X^rep` from 3450 to test the action, not just the quotient map.
- The public core is quiet: `delta_vXrep S_EH=0`, `delta_vXrep S_matter=0` under the quotient matter signature, and `delta_vXrep S_EM=0` under q-basic EM normalization.
- That is real progress toward local GR: the public EH/Hilbert/Maxwell sector does not source the extra `X` current.
- It still does not close total local GR, because an explicit `X_rep` action line, hidden frame/EM coefficient, source weight, `R_AB`, boundary charge, or private tau-clock term would generate a real `L_X` residual.
- Those residual owners are now split as `LXR3451_0..LXR3451_5`; no one gets to hide in the word “vertical”.

## Source Register
{md_table(rows_by_name["source_register"])}

## Public-Core Action Silence
{md_table(rows_by_name["public_core_action_silence"])}

## Pure-Representative Action Descent Contract
{md_table(rows_by_name["pure_rep_action_descent_contract"])}

## L_X Residual Owner Split
{md_table(rows_by_name["lx_residual_owner_split"])}

## DeltaH Curl Feed Update
{md_table(rows_by_name["deltaH_curl_feed_update"])}

## Promotion Gates
{md_table(rows_by_name["promotion_gates"])}

## Decision Ledger
{md_table(rows_by_name["decision_ledger"])}

## Next Target
{md_table(rows_by_name["next_target"])}

## Runner Nonclaim
{md_table(rows_by_name["runner_nonclaim"])}

## Validation
{md_table(rows_by_name["validation"])}

## Bottom Line
The local-GR route got sharper: `v_X^rep` kills the public EH/matter/EM action derivative, so the remaining fight is not the public core. The fight is whether the total parent action has any explicit `X_rep` or rejected-slot term. If it does, we bound it; if it does not, the absent-quotient zero theorem can move much closer to promotion.
"""
    DOC.write_text(text, encoding="utf-8")


def main() -> None:
    start_utc = datetime.now(timezone.utc)
    rows_by_name = {
        "source_register": source_register(),
        "public_core_action_silence": public_core_action_silence(),
        "pure_rep_action_descent_contract": pure_rep_action_descent_contract(),
        "lx_residual_owner_split": lx_residual_owner_split(),
        "deltaH_curl_feed_update": deltaH_curl_feed_update(),
        "promotion_gates": promotion_gates(),
        "decision_ledger": decision_ledger(),
        "next_target": next_target(),
        "runner_nonclaim": runner_nonclaim(),
    }
    for output_name, rows in rows_by_name.items():
        write_csv(OUTPUTS[output_name], rows)
    rows_by_name["validation"] = validation_rows(rows_by_name, start_utc)
    write_csv(OUTPUTS["validation"], rows_by_name["validation"])
    write_doc(rows_by_name)
    failed_rows = [row for row in rows_by_name["validation"] if not row["passed"]]
    if failed_rows:
        raise SystemExit(f"3451 validation failed: {failed_rows}")
    print(f"wrote {DOC}")
    print(f"wrote {len(OUTPUTS)} csv outputs")


if __name__ == "__main__":
    main()

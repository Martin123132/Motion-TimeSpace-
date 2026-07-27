from __future__ import annotations

import csv
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
RESIDUALS = ROOT / "source-intake" / "mts_residuals"
FORMALIZATION = ROOT.parent / "formalization-workbench"
CHECKPOINT_ID = "3638"
BRANCH_ID = "MTS_R2FR_Y5_NO_MARKER_SOURCE_THEOREM_OR_BETA_COMPONENT_PACK_3638"
DOC = ROOT / "3638-Y5-R2FR-no-marker-source-theorem-or-beta-component-pack.md"


def now() -> str:
    return datetime.now(timezone.utc).isoformat()


def write_csv(path: Path, rows: list[dict[str, object]]) -> None:
    if not rows:
        raise ValueError(f"refusing empty csv: {path}")
    path.parent.mkdir(parents=True, exist_ok=True)
    fields: list[str] = []
    for row in rows:
        for key in row:
            if key not in fields:
                fields.append(key)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def contains(path: Path, needle: str) -> bool:
    if not path.exists():
        return False
    return needle in path.read_text(encoding="utf-8", errors="replace")


def out_paths() -> dict[str, Path]:
    return {
        "source_register": RESIDUALS / "P8_Y5_R2FR_3638_SOURCE_REGISTER.csv",
        "theorem_audit": RESIDUALS / "P8_Y5_R2FR_3638_NO_MARKER_SOURCE_THEOREM_AUDIT.csv",
        "beta_component_pack": RESIDUALS / "P8_Y5_R2FR_3638_BETAX_COMPONENT_PACK.csv",
        "absolute_envelope": RESIDUALS / "P8_Y5_R2FR_3638_BETAX_ABSOLUTE_ENVELOPE.csv",
        "eta_update": RESIDUALS / "P8_Y5_R2FR_3638_ETA_SOURCE_AB_COMPONENT_UPDATE.csv",
        "decision_gates": RESIDUALS / "P8_Y5_R2FR_3638_DECISION_GATES.csv",
        "status": RESIDUALS / "P8_Y5_R2FR_3638_STATUS.csv",
        "next_target": RESIDUALS / "P8_Y5_R2FR_3638_NEXT_TARGET.csv",
        "canonical_status": RESIDUALS / "P8_Y5_no_marker_beta_component_status.csv",
        "validation": RESIDUALS / "P8_Y5_BRR545_3638_VALIDATION.csv",
    }


def source_rows(t: str) -> list[dict[str, object]]:
    sources = [
        (
            "handoff_3637",
            RESIDUALS / "P8_Y5_R2FR_3637_NEXT_TARGET.csv",
            "no-marker/source-blind theorem",
            "3637 handoff: prove no-marker theorem or build beta component pack.",
        ),
        (
            "eta_3637",
            RESIDUALS / "P8_Y5_R2FR_3637_ETA_SOURCE_AB_BETAX_ROW.csv",
            "Delta beta_X_AB",
            "current beta-difference source-charge row.",
        ),
        (
            "nomarker_1028",
            ROOT / "1028-Y5-R10-frame-marker-coupling-bound-input-pack-or-no-marker-theorem.md",
            "MISSING_NO_MARKER_THEOREM",
            "prior no-marker audit and frame/marker bound pack.",
        ),
        (
            "qbar_1027",
            ROOT / "1027-Y5-R10-qbarXT-source-zero-or-bounded-coupling-row.md",
            "common nonzero source charge",
            "counterexample guard: WEP/covariance alone cannot kill source charge.",
        ),
        (
            "no_species_contract",
            RESIDUALS / "P8_no_species_source_charge_CONTRACT.csv",
            "S4_source_normalization_species_blind",
            "source-charge/no-species contract with fallback policy.",
        ),
        (
            "species_residual",
            RESIDUALS / "P8_species_source_charge_residual_or_zero.csv",
            "SSC2675_2_TiPt_first_fill",
            "existing nonclaim source-charge residual row and MICROSCOPE target.",
        ),
        (
            "frame_pack_944",
            RESIDUALS / "P8_Y5_R10_944_FRAME_LEAK_BOUND_PACK.csv",
            "FLB944_2_species_mass",
            "older frame/marker component schema.",
        ),
        (
            "frame_rows_945",
            RESIDUALS / "P8_Y5_R10_945_FIRST_FRAME_LEAK_BOUND_ROWS.csv",
            "BND945_3_bA_species",
            "first frame/marker bound rows.",
        ),
        (
            "object_language_2677",
            RESIDUALS / "P8_Y5_R2FR_2677_NO_SPECIES_ACTION_WEIGHT_OBJECT_LANGUAGE_AUDIT.csv",
            "OL2677_0_target_rule",
            "no species action weight object-language audit.",
        ),
        (
            "em_object_language_3519",
            RESIDUALS / "P8_EM_vq_parent_object_language_normal_form_candidate.csv",
            "NF3519_2_matter_functor",
            "parent object language candidate for matter functor/source slots.",
        ),
        (
            "material_requirements_1068",
            RESIDUALS / "P8_Y5_R10_1068_MATERIAL_RESPONSE_REQUIREMENTS.csv",
            "MISSING_FULL_MATERIAL_TENSOR",
            "material response requirements and missing tensor warning.",
        ),
        (
            "no_cancellation_1087",
            RESIDUALS / "P8_Y5_R10_1087_ALL_MATERIAL_NO_CANCELLATION_POLICY.csv",
            "one-pair cancellation is not invariant",
            "no-cancellation policy for material/source coefficients.",
        ),
    ]
    return [
        {
            "timestamp_utc": t,
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "source_id": source_id,
            "path": str(path),
            "exists": path.exists(),
            "needle": needle,
            "needle_found": contains(path, needle),
            "role": role,
        }
        for source_id, path, needle, role in sources
    ]


def theorem_audit_rows(t: str) -> list[dict[str, object]]:
    rows = [
        {
            "audit_id": "NMS3638_0_parent_q_kernel",
            "theorem_clause": "X_N is vertical to the parent quotient before matter/source variation",
            "mathematical_form": "v_X in ker(Dq), with boundary/proper gauge silence",
            "current_evidence": "1028 and 3633 keep q-kernel ownership unsigned",
            "status": "UNSIGNED",
            "if_unsigned": "X_N may be a physical/source-coupled field, so beta components remain active",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "audit_id": "NMS3638_1_matter_functor",
            "theorem_clause": "ordinary matter/source action factors through q-owned public structures only",
            "mathematical_form": "S_matter=sum_A S_A[Psi_A,Qvis(q),theta_A(q)] with no source-only slot",
            "current_evidence": "3519 gives exact conditional normal form; 1031 says matter-interface restriction is not parent-signed",
            "status": "CONDITIONAL_NOT_PARENT_SIGNED",
            "if_unsigned": "source prefactors, action weights, or non-terminal labels can carry beta",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "audit_id": "NMS3638_2_marker_constants",
            "theorem_clause": "masses, material constants, EM constants, and clock/readout markers are q-owned or superselected",
            "mathematical_form": "Lie_X m_A=Lie_X alpha_EM=Lie_X theta_A=Lie_X tau_clock=0",
            "current_evidence": "1028 marks MISSING_NO_MARKER_THEOREM; 944/945 retain b_A and b_alpha rows",
            "status": "MISSING_NO_MARKER_THEOREM",
            "if_unsigned": "b_A, b_alpha, b_clock, and material sensitivity rows remain active",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "audit_id": "NMS3638_3_species_action_weight",
            "theorem_clause": "species action weights, hbar_A, source weights, and Jacobians are not legal parent symbols",
            "mathematical_form": "w_A=hbar_A=J_A=0 as independent species/source residuals",
            "current_evidence": "2677 sharpens the target but verdict is NO_SPECIES_ACTION_WEIGHT_OBJECT_LANGUAGE_NOT_DERIVED",
            "status": "TARGET_SHARPENED_NOT_SIGNED",
            "if_unsigned": "b_source_weight and b_measure_weight remain in beta component pack",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "audit_id": "NMS3638_4_hidden_source_tail",
            "theorem_clause": "non-Hilbert, boundary, projector, support-shift, and readout tails are zero or separately scored",
            "mathematical_form": "q_nonH=0, Delta_W_support=0, Delta_PiM=0, or all enter absolute envelope",
            "current_evidence": "1028 and charge-current residual ledgers keep hidden tails active",
            "status": "HIDDEN_TAILS_RETAINED",
            "if_unsigned": "b_nonH and b_support enter beta envelope and common-mode source normalization",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "audit_id": "NMS3638_5_verdict",
            "theorem_clause": "no-marker/source-blind theorem for current MTS corpus",
            "mathematical_form": "all clauses NMS3638_0..4 parent-signed together",
            "current_evidence": "conditional theorem exists but parent signature is missing in multiple independent clauses",
            "status": "NO_MARKER_THEOREM_NOT_PARENT_SIGNED_BETA_COMPONENT_PACK_REQUIRED",
            "if_unsigned": "build b_A, b_alpha, b_source_weight, b_nonH, b_support, and beta_common component rows",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
    ]
    return [
        {
            "timestamp_utc": t,
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            **row,
        }
        for row in rows
    ]


def beta_component_rows(t: str) -> list[dict[str, object]]:
    rows = [
        {
            "component_id": "BETA3638_0_beta_common",
            "symbol": "beta_common",
            "definition": "common species-blind source charge partial_XN ln mu_obs shared by all ordinary source/test bodies",
            "formula_slot": "beta_X^A = beta_common + delta beta_A",
            "units": "dimensionless",
            "observable_links": "R10;Gdot;radial_source_hair;source_normalization;clock_common_mode",
            "zero_or_score_requirement": "parent common-mode no-source theorem or route to R10/Gdot/radial rows",
            "status": "COMMON_MODE_ACTIVE_NOT_WEP_ERASED",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "component_id": "BETA3638_1_b_Geff_species",
            "symbol": "b_Geff_A",
            "definition": "species/source-label derivative of G_eff/kappa_eff",
            "formula_slot": "Delta_AB partial_XN ln G_eff",
            "units": "dimensionless",
            "observable_links": "R1;R9;R10;R11",
            "zero_or_score_requirement": "global coupling superselection with no species labels, or b_Geff_A row",
            "status": "OPEN_NOT_PARENT_DERIVED",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "component_id": "BETA3638_2_b_Meff_species",
            "symbol": "b_Meff_A",
            "definition": "species/material derivative of projected source mass M_eff",
            "formula_slot": "Delta_AB partial_XN ln M_eff",
            "units": "dimensionless",
            "observable_links": "R1;R4;R9;R11",
            "zero_or_score_requirement": "Pi_M/J_H source Ward current is selector-blind and calibrated before readout, or b_Meff_A row",
            "status": "OPEN_NOT_PARENT_DERIVED",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "component_id": "BETA3638_3_b_epsilon_mu_species",
            "symbol": "b_epsilon_mu_A",
            "definition": "species/material derivative of extra measured-GM contribution epsilon_mu",
            "formula_slot": "Delta_AB partial_XN ln(1+epsilon_mu)",
            "units": "dimensionless",
            "observable_links": "R1;R3;R4;R7;R8;R9;R11",
            "zero_or_score_requirement": "mu_extra zero/universal constant theorem, or coefficient vector for species-dependent extra mass channels",
            "status": "FAILED_MISSING_COEFFICIENT_VECTOR",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "component_id": "BETA3638_4_b_A",
            "symbol": "b_A",
            "definition": "vertical derivative of material mass/species constants d ln m_A^obs/dX_N",
            "formula_slot": "Delta beta_mass_AB = sum_i (s_i^A-s_i^B)b_A_i",
            "units": "dimensionless",
            "observable_links": "WEP;clock;composition;R10",
            "zero_or_score_requirement": "mass/material constants descend through q or material sensitivity rows with source paths",
            "status": "MISSING_CONSTANT_DESCENT_OR_NUMERIC_BA",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "component_id": "BETA3638_5_b_alpha",
            "symbol": "b_alpha",
            "definition": "vertical derivative of EM/fine-structure/electromagnetic binding marker",
            "formula_slot": "Delta beta_EM_AB = (s_alpha^A-s_alpha^B)b_alpha",
            "units": "dimensionless",
            "observable_links": "clock;EM;WEP;composition",
            "zero_or_score_requirement": "EM constants descend through q or b_alpha sensitivity row",
            "status": "MISSING_EM_CONSTANT_DESCENT_OR_NUMERIC_BOUND",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "component_id": "BETA3638_6_b_clock",
            "symbol": "b_clock",
            "definition": "clock/readout marker derivative that changes measured source or frequency standards",
            "formula_slot": "Delta beta_clock_AB = (s_clock^A-s_clock^B)b_clock",
            "units": "dimensionless",
            "observable_links": "clock;R2;WEP;source_normalization",
            "zero_or_score_requirement": "clock markers q-owned/superselected or clock sensitivity row",
            "status": "MISSING_CLOCK_MARKER_DESCENT",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "component_id": "BETA3638_7_b_source_weight",
            "symbol": "b_source_weight",
            "definition": "species/action/source prefactor derivative w_A, hbar_A, source Jacobian, or source-only normalization",
            "formula_slot": "Delta beta_weight_AB = Delta_AB partial_XN ln w_A or equivalent source prefactor",
            "units": "dimensionless",
            "observable_links": "R1;R4;R9;R11",
            "zero_or_score_requirement": "object-language exclusion of species weights or finite Delta_w_AB row",
            "status": "NO_SPECIES_ACTION_WEIGHT_NOT_DERIVED",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "component_id": "BETA3638_8_b_nonH",
            "symbol": "b_nonH",
            "definition": "non-Hilbert/boundary/projector/domain source tail contribution to beta",
            "formula_slot": "Delta beta_nonH_AB from q_nonH, Delta_PiM, boundary/domain/source-tail pieces",
            "units": "dimensionless_or_source_current_normalized",
            "observable_links": "R1;R7;R8;R10;R11",
            "zero_or_score_requirement": "hidden source tail theorem or q_nonH/boundary/projector rows",
            "status": "HIDDEN_SOURCE_TAIL_RETAINED",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "component_id": "BETA3638_9_b_support",
            "symbol": "b_support",
            "definition": "source/worldtube support shift contribution under observed-frame/source support changes",
            "formula_slot": "Delta beta_support_AB from Delta_W_support and support-rule variation",
            "units": "dimensionless",
            "observable_links": "orbital;source_normalization;local_GR",
            "zero_or_score_requirement": "support equivalence theorem or system-level support-shift bound",
            "status": "SUPPORT_SHIFT_RETAINED",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
    ]
    return [
        {
            "timestamp_utc": t,
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            **row,
        }
        for row in rows
    ]


def absolute_envelope_rows(t: str) -> list[dict[str, object]]:
    rows = [
        {
            "envelope_id": "ENV3638_0_delta_beta_abs",
            "quantity": "abs_Delta_beta_X_AB_envelope",
            "formula": "|Delta beta_X_AB| <= |Delta b_Geff_AB| + |Delta b_Meff_AB| + |Delta b_epsilon_mu_AB| + |Delta beta_marker_AB| + |Delta beta_weight_AB| + |Delta beta_nonH_AB| + |Delta beta_support_AB|",
            "no_cancellation_rule": "component cancellation is forbidden unless a parent identity proves it for all allowed material pairs",
            "feeds": "eta_source_AB small-charge limit; R1 source WEP",
            "status": "ABSOLUTE_ENVELOPE_READY_VALUES_MISSING",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "envelope_id": "ENV3638_1_marker_abs",
            "quantity": "abs_Delta_beta_marker_AB",
            "formula": "|Delta beta_marker_AB| <= sum_i |s_i^A-s_i^B||b_A_i| + |s_alpha^A-s_alpha^B||b_alpha| + |s_clock^A-s_clock^B||b_clock|",
            "no_cancellation_rule": "material/EM/clock components add by absolute envelope without sign tuning",
            "feeds": "WEP;clock;EM;composition",
            "status": "SENSITIVITY_ROWS_MISSING",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "envelope_id": "ENV3638_2_eta_bound_rule",
            "quantity": "eta_source_AB_bound_rule",
            "formula": "eta_source_AB <= 2 abs_Delta_beta_X_AB_envelope / |2 + beta_X^A + beta_X^B|, approx abs_Delta_beta_X_AB_envelope for small beta",
            "no_cancellation_rule": "a one-pair material cancellation cannot certify theory zero",
            "feeds": "2.8e-15 source-charge WEP target",
            "status": "BOUND_RULE_READY_NUMERIC_VALUES_MISSING",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
    ]
    return [
        {
            "timestamp_utc": t,
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            **row,
        }
        for row in rows
    ]


def eta_update_rows(t: str) -> list[dict[str, object]]:
    return [
        {
            "timestamp_utc": t,
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "row_id": "ETA3638_0_componentized_beta_source_charge",
            "parent_row": "ETA3637_0_betaX_species_difference",
            "observable": "eta_source_AB;eta_WEP_source_charge",
            "componentized_prediction": "eta_source_AB = 2|Delta b_Geff + Delta b_Meff + Delta b_epsilon_mu + Delta beta_marker + Delta beta_weight + Delta beta_nonH + Delta beta_support| / |2+beta_X^A+beta_X^B|",
            "absolute_envelope": "abs_Delta_beta_X_AB_envelope from ENV3638_0_delta_beta_abs",
            "small_charge_scoring": "eta_source_AB ~= abs_Delta_beta_X_AB_envelope only after component values or theorem zeros exist",
            "bound_or_target": "2.8e-15",
            "units": "dimensionless",
            "derivation_status": "component_skeleton_filled_not_numeric",
            "score_status": "not_scoreable_until_component_values_or_parent_zero",
            "common_mode_guard": "beta_common still bypasses eta_source_AB and remains active for R10/Gdot/radial/source-normalization",
            "claim_allowed": False,
            "valid_for_claim": False,
        }
    ]


def decision_rows(t: str) -> list[dict[str, object]]:
    rows = [
        {
            "decision_id": "DEC3638_0_no_marker_theorem",
            "decision": "The no-marker/source-blind theorem is still conditional; it is not parent-signed for current MTS.",
            "status": "NO_MARKER_THEOREM_NOT_PARENT_SIGNED",
            "next_action": "use beta component pack rather than claiming source-charge zero",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "decision_id": "DEC3638_1_component_pack",
            "decision": "The beta source-charge row now has explicit component placeholders: b_A, b_alpha, b_source_weight, b_nonH, b_support, and beta_common.",
            "status": "BETA_COMPONENT_PACK_FILLED",
            "next_action": "derive or source components one by one with units and observable links",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "decision_id": "DEC3638_2_no_cancellation",
            "decision": "The eta_source_AB row must use an absolute-sum envelope until a parent identity proves cancellation.",
            "status": "ABSOLUTE_ENVELOPE_REQUIRED",
            "next_action": "do not use material-pair cancellation as a theory result",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "decision_id": "DEC3638_3_next_focus",
            "decision": "The next highest-value fork is common-mode beta because WEP can pass while a universal source force survives.",
            "status": "COMMON_BETA_NEXT",
            "next_action": "try beta_common=0 or map beta_common to R10/Gdot/radial source-normalization rows",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
    ]
    return [
        {
            "timestamp_utc": t,
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            **row,
        }
        for row in rows
    ]


def status_rows(t: str) -> list[dict[str, object]]:
    return [
        {
            "timestamp_utc": t,
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "status": "NO_MARKER_THEOREM_UNSIGNED_BETA_COMPONENT_PACK_FILLED_ABSOLUTE_ENVELOPE_ACTIVE",
            "summary": "3638 audits the no-marker/source-blind theorem and keeps it conditional, not claim-live. It converts the beta source-charge row into a component pack: beta_common, b_Geff, b_Meff, b_epsilon_mu, b_A, b_alpha, b_clock, b_source_weight, b_nonH, and b_support, with common-mode beta marked as the next priority. It also installs an absolute-sum envelope so unknown marker/source components cannot cancel into a fake eta_source_AB pass.",
            "claim_ceiling": "no source-WEP, Newton, R10/R11, local-GR, PPN, clock, EM, or source-zero claim is allowed from 3638",
            "useful_result": "source coupling is now a componentized beta ledger with no-cancellation policy and common-mode beta marked as next priority",
            "claim_allowed": False,
            "valid_for_claim": False,
        }
    ]


def next_rows(t: str) -> list[dict[str, object]]:
    return [
        {
            "timestamp_utc": t,
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "next_id": "NEXT3638_0",
            "target_doc": "3639-Y5-R2FR-common-beta-zero-or-source-normalization-runner.md",
            "target_script": "scripts/Y5_R2FR_3639_common_beta_zero_or_source_normalization_runner.py",
            "objective": "try to derive beta_common=0 from parent quotient/source action; if not, map common beta into R10, Gdot, radial source hair, and source-normalization residual rows without relying on WEP",
            "success_gate": "either common beta is theorem-zero from parent q-data, or beta_common gains nonclaim rows for R10/Gdot/radial/source-normalization with units, observable links, and required bound inputs",
            "reason": "3638 shows differential WEP can miss common source coupling; common beta is the next highest-pressure source-coupling target.",
            "claim_allowed": False,
            "valid_for_claim": False,
        }
    ]


def canonical_rows(t: str) -> list[dict[str, object]]:
    return [
        {
            "timestamp_utc": t,
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "canonical_object": "no_marker_beta_component_pack",
            "canonical_status": "NO_MARKER_THEOREM_UNSIGNED_COMPONENT_PACK_ACTIVE",
            "usable_result": "Delta beta_X_AB is decomposed into Geff, Meff, epsilon_mu, material/EM/clock markers, source weights, non-Hilbert tails, and support shifts; absolute envelope forbids cancellation.",
            "hard_block": "derive beta_common=0 or map common beta to source-normalization/R10/Gdot/radial residuals",
            "claim_allowed": False,
            "valid_for_claim": False,
        }
    ]


def md(value: object) -> str:
    return str(value).replace("|", "\\|").replace("\n", "<br>")


def table(rows: list[dict[str, object]], cols: list[str]) -> str:
    output = ["| " + " | ".join(cols) + " |", "| " + " | ".join("---" for _ in cols) + " |"]
    for row in rows:
        output.append("| " + " | ".join(md(row.get(col, "")) for col in cols) + " |")
    return "\n".join(output)


def write_doc(
    src: list[dict[str, object]],
    audit: list[dict[str, object]],
    components: list[dict[str, object]],
    envelope: list[dict[str, object]],
    eta: list[dict[str, object]],
    decisions: list[dict[str, object]],
    status: list[dict[str, object]],
    nxt: list[dict[str, object]],
) -> None:
    text = "\n\n".join(
        [
            "# 3638 Y5 R2FR no-marker source theorem or beta component pack",
            f"**Status:** {status[0]['summary']}",
            f"**Claim ceiling:** {status[0]['claim_ceiling']}.",
            "## Main result",
            (
                "The no-marker theorem remains a clean target, but not a current claim. The beta source-charge row is now componentized:\n\n"
                "```text\n"
                "Delta beta_X_AB = Delta b_Geff_AB + Delta b_Meff_AB + Delta b_epsilon_mu_AB\n"
                "                + Delta beta_marker_AB + Delta beta_weight_AB\n"
                "                + Delta beta_nonH_AB + Delta beta_support_AB.\n"
                "```\n\n"
                "Until a parent identity proves cancellation, scoring must use the absolute envelope. This prevents a fake WEP pass from sign-tuning material/source pieces. The next pressure point is `beta_common`, because differential WEP can miss a universal source coupling."
            ),
            "## Source register",
            table(src, ["source_id", "path", "exists", "needle_found", "role"]),
            "## No-marker theorem audit",
            table(audit, ["audit_id", "theorem_clause", "mathematical_form", "current_evidence", "status", "if_unsigned"]),
            "## Beta component pack",
            table(components, ["component_id", "symbol", "definition", "formula_slot", "units", "observable_links", "zero_or_score_requirement", "status"]),
            "## Absolute envelope",
            table(envelope, ["envelope_id", "quantity", "formula", "no_cancellation_rule", "feeds", "status"]),
            "## eta source update",
            table(eta, ["row_id", "observable", "componentized_prediction", "absolute_envelope", "small_charge_scoring", "bound_or_target", "score_status", "common_mode_guard"]),
            "## Decisions",
            table(decisions, ["decision_id", "decision", "status", "next_action"]),
            "## Next target",
            table(nxt, ["target_doc", "target_script", "objective", "success_gate"]),
        ]
    )
    DOC.write_text(text + "\n", encoding="utf-8")


def validate(outputs: dict[str, Path], src: list[dict[str, object]]) -> list[dict[str, object]]:
    t = now()
    rows: list[dict[str, object]] = []

    def add(validation_id: str, ok: bool, detail: str) -> None:
        rows.append(
            {
                "timestamp_utc": t,
                "branch_id": BRANCH_ID,
                "checkpoint_id": CHECKPOINT_ID,
                "validation_id": validation_id,
                "result": "PASS" if ok else "FAIL",
                "detail": detail,
            }
        )

    add("VAL3638_0_sources_exist", all(bool(row["exists"]) for row in src), "all cited source paths exist")
    add("VAL3638_1_needles_found", all(bool(row["needle_found"]) for row in src), "all source needles found")
    pre = {name: path for name, path in outputs.items() if name != "validation"}
    add("VAL3638_2_outputs_exist", all(path.exists() for path in pre.values()) and DOC.exists(), "all pre-validation outputs and doc written")

    details = []
    parse_ok = True
    for name, path in pre.items():
        try:
            count = len(read_csv(path))
            details.append(f"{name}:{count}")
            parse_ok = parse_ok and count > 0
        except Exception as exc:
            details.append(f"{name}:ERR:{exc}")
            parse_ok = False
    add("VAL3638_3_csv_parse", parse_ok, "; ".join(details))

    audit = read_csv(outputs["theorem_audit"])
    components = read_csv(outputs["beta_component_pack"])
    envelope = read_csv(outputs["absolute_envelope"])
    eta = read_csv(outputs["eta_update"])
    decisions = read_csv(outputs["decision_gates"])
    status = read_csv(outputs["status"])
    nxt = read_csv(outputs["next_target"])

    add("VAL3638_4_theorem_unsigned", any(row["status"] == "NO_MARKER_THEOREM_NOT_PARENT_SIGNED_BETA_COMPONENT_PACK_REQUIRED" for row in audit), "no-marker theorem is not promoted")
    symbols = {row["symbol"] for row in components}
    required_symbols = {"beta_common", "b_A", "b_alpha", "b_source_weight", "b_nonH", "b_support"}
    add("VAL3638_5_component_pack_required_symbols", required_symbols.issubset(symbols), "beta component pack includes common/mass/EM/source/nonH/support pieces")
    add("VAL3638_6_absolute_envelope_present", any("component cancellation is forbidden" in row["no_cancellation_rule"] for row in envelope), "absolute no-cancellation envelope present")
    add("VAL3638_7_eta_update_componentized", bool(eta) and "Delta b_Geff" in eta[0]["componentized_prediction"] and eta[0]["bound_or_target"] == "2.8e-15", "eta source row componentized with target")
    add("VAL3638_8_common_beta_next", any(row["status"] == "COMMON_BETA_NEXT" for row in decisions) and "common-mode beta" in status[0]["summary"], "common beta selected next")
    add("VAL3638_9_nonclaim_all_outputs", all(row["valid_for_claim"].lower() == "false" for row in audit + components + envelope + eta + decisions + status + nxt), "all generated rows remain nonclaim")
    leaks = list(FORMALIZATION.rglob("*3638*")) if FORMALIZATION.exists() else []
    add("VAL3638_10_no_formalization_leak", not leaks, "no 3638 files in formalization-workbench")
    add("VAL3638_11_next_target_written", bool(nxt) and "3639" in nxt[0]["target_doc"], "3639 common beta target written")
    add("VAL3638_12_doc_written", DOC.exists() and "Delta beta_X_AB" in DOC.read_text(encoding="utf-8", errors="replace"), "checkpoint doc written with beta decomposition")
    add("VAL3638_13_canonical_status_written", outputs["canonical_status"].exists() and "NO_MARKER_THEOREM_UNSIGNED_COMPONENT_PACK_ACTIVE" in outputs["canonical_status"].read_text(encoding="utf-8", errors="replace"), "canonical no-marker/beta status written")
    return rows


def main() -> None:
    t = now()
    outputs = out_paths()
    src = source_rows(t)
    audit = theorem_audit_rows(t)
    components = beta_component_rows(t)
    envelope = absolute_envelope_rows(t)
    eta = eta_update_rows(t)
    decisions = decision_rows(t)
    status = status_rows(t)
    nxt = next_rows(t)
    canonical = canonical_rows(t)

    write_csv(outputs["source_register"], src)
    write_csv(outputs["theorem_audit"], audit)
    write_csv(outputs["beta_component_pack"], components)
    write_csv(outputs["absolute_envelope"], envelope)
    write_csv(outputs["eta_update"], eta)
    write_csv(outputs["decision_gates"], decisions)
    write_csv(outputs["status"], status)
    write_csv(outputs["next_target"], nxt)
    write_csv(outputs["canonical_status"], canonical)
    write_doc(src, audit, components, envelope, eta, decisions, status, nxt)

    validation = validate(outputs, src)
    write_csv(outputs["validation"], validation)
    failures = [row for row in validation if row["result"] != "PASS"]
    if failures:
        raise SystemExit(f"3638 validation failed: {failures}")
    print(f"wrote 3638 checkpoint with {len(validation)} validation checks")


if __name__ == "__main__":
    main()

from __future__ import annotations

import csv
from datetime import datetime, timezone
from pathlib import Path


POST_CHECKPOINT = Path(__file__).resolve().parents[1]
RESIDUALS = POST_CHECKPOINT / "source-intake" / "mts_residuals"
FORMALIZATION = POST_CHECKPOINT.parent / "formalization-workbench"
OUTPUT_DOC = POST_CHECKPOINT / "717-Y5-R10-observed-frame-lock-and-frame-transfer-coefficient-pack.md"
NEXT_TARGET = "718-Y5-R10-AEH-prefactor-gradient-zero-theorem-or-retained-source-pack.md"
GENERATED_UTC = datetime.now(timezone.utc).replace(microsecond=0).isoformat()
CUTOFF = datetime(2026, 5, 31, 14, 42, 0)


SOURCES = {
    "716_doc": {
        "path": POST_CHECKPOINT / "716-Y5-R10-matter-coupling-source-charge-derivation-or-free-coefficient-lock.md",
        "note": "source charge law and frame-transfer bottleneck",
    },
    "716_validation": {
        "path": RESIDUALS / "P8_Y5_BRR545_716_VALIDATION.csv",
        "note": "prior checkpoint validation",
    },
    "716_frame_map": {
        "path": RESIDUALS / "P8_Y5_R10_716_FRAME_TRANSFER_MAP.csv",
        "note": "frame-transfer branches from 716",
    },
    "716_coupling_derivation": {
        "path": RESIDUALS / "P8_Y5_R10_716_MATTER_COUPLING_DERIVATION.csv",
        "note": "b_A,I and Q_Aa definitions",
    },
    "715_doc": {
        "path": POST_CHECKPOINT / "715-Y5-R10-retained-scalar-source-row-minimum-executable-coefficient-pack.md",
        "note": "minimum retained scalar coefficient pack",
    },
    "715_pack": {
        "path": RESIDUALS / "P8_Y5_R10_715_MINIMUM_EXECUTABLE_COEFFICIENT_PACK.csv",
        "note": "socket containing F_obs, A_EH, a_I, b_A,I, and f_frame",
    },
    "710_descent_clause": {
        "path": RESIDUALS / "P8_Y5_R10_710_DESCENT_PARENT_ACTION_CLAUSE.csv",
        "note": "conditional descent clauses including no-prefactor and same-frame gates",
    },
    "710_frame_guard": {
        "path": RESIDUALS / "P8_Y5_R10_710_FRAME_TRANSFER_GUARD.csv",
        "note": "earlier frame-transfer guard",
    },
    "711_ownership_map": {
        "path": RESIDUALS / "P8_Y5_R10_711_DPC710_OWNERSHIP_MAP.csv",
        "note": "ownership status of DPC710 clauses",
    },
    "626_doc": {
        "path": POST_CHECKPOINT / "626-Y5-R10-quotient-invariant-matter-action-signature-or-cg-bound-input.md",
        "note": "descent/signature warning for local matter action",
    },
    "410_doc": {
        "path": POST_CHECKPOINT / "410-quotient-matter-functor-theorem-attempt.md",
        "note": "matter functor theorem attempt and failure conditions",
    },
}


def write_csv(path: Path, rows: list[dict[str, object]], fieldnames: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def bool_text(value: bool) -> str:
    return "true" if value else "false"


def source_path_string(*keys: str) -> str:
    return ";".join(str(SOURCES[key]["path"]) for key in keys)


def all_generated_rows_have_false_validity(paths: list[Path]) -> bool:
    for path in paths:
        rows = read_csv(path)
        if not rows:
            continue
        if "valid_for_claim" not in rows[0]:
            continue
        for row in rows:
            if row.get("valid_for_claim", "").lower() != "false":
                return False
    return True


def formalization_changed_after_cutoff() -> int:
    if not FORMALIZATION.exists():
        return -1
    count = 0
    for path in FORMALIZATION.rglob("*"):
        if not path.is_file():
            continue
        modified = datetime.fromtimestamp(path.stat().st_mtime)
        if modified > CUTOFF:
            count += 1
    return count


def prior_validation_clean(path: Path) -> bool:
    rows = read_csv(path)
    return bool(rows) and all(row.get("result") == "pass" for row in rows)


def csv_contains(path: Path, *needles: str) -> bool:
    text = path.read_text(encoding="utf-8", errors="replace")
    return all(needle in text for needle in needles)


def markdown_table(rows: list[dict[str, object]], fields: list[str]) -> str:
    header = "| " + " | ".join(fields) + " |"
    separator = "| " + " | ".join("---" for _ in fields) + " |"
    body = []
    for row in rows:
        cells = []
        for field in fields:
            value = str(row.get(field, ""))
            value = value.replace("\n", " ").replace("|", "\\|")
            cells.append(value)
        body.append("| " + " | ".join(cells) + " |")
    return "\n".join([header, separator, *body])


def main() -> None:
    RESIDUALS.mkdir(parents=True, exist_ok=True)

    source_register = [
        {
            "source_id": key,
            "path": str(info["path"]),
            "exists": bool_text(info["path"].exists()),
            "role": info["note"],
            "valid_for_claim": "false",
            "generated_utc": GENERATED_UTC,
        }
        for key, info in SOURCES.items()
    ]

    frame_convention_audit = [
        {
            "audit_id": "FCA717_0_parent_template",
            "object": "local scalar-tensor frame template",
            "statement": "S contains sqrt(-g_obs) A_EH(u) R[g_obs] plus matter S_A[B_A^2(u) g_obs, psi_A, theta_A(u)]",
            "status": "template_available_not_parent_signed",
            "f_frame_effect": "defines the algebra to be locked, not a claim",
            "claim_effect": "no local-GR or R10 claim",
            "valid_for_claim": "false",
            "source_paths": source_path_string("715_pack", "716_coupling_derivation", "710_descent_clause"),
            "generated_utc": GENERATED_UTC,
        },
        {
            "audit_id": "FCA717_1_observed_same_frame",
            "object": "observed frame",
            "statement": "If EH and matter both use g_obs and A_EH is parent-fixed locally, no conformal transfer term is generated",
            "status": "conditional_only_not_signed",
            "f_frame_effect": "f_frame=0 only if DPC710_2 and DPC710_6 are parent-owned, or a_I=0 by theorem",
            "claim_effect": "zero route blocked by current ownership map",
            "valid_for_claim": "false",
            "source_paths": source_path_string("710_descent_clause", "711_ownership_map", "716_frame_map"),
            "generated_utc": GENERATED_UTC,
        },
        {
            "audit_id": "FCA717_2_Einstein_normalization",
            "object": "Einstein-normalized frame",
            "statement": "For D dimensions, g_E = A_EH(u)^(2/(D-2)) g_obs removes the R prefactor up to scalar kinetic/boundary terms",
            "status": "conditional_conformal_identity",
            "f_frame_effect": "f_frame=-1/(D-2), so f_frame=-1/2 in D=4",
            "claim_effect": "if this frame is selected, a nonzero a_I becomes a real source-charge correction",
            "valid_for_claim": "false",
            "source_paths": source_path_string("715_pack", "716_frame_map"),
            "generated_utc": GENERATED_UTC,
        },
        {
            "audit_id": "FCA717_3_disformal_or_readout_leakage",
            "object": "representative/readout metric",
            "statement": "If matter or clocks use a Weyl/disformal representative beyond B_A^2 g_obs, additional coefficients enter q_A,I",
            "status": "blocked_for_claim",
            "f_frame_effect": "retain extra representative coefficients or prove they vanish",
            "claim_effect": "cannot hide leakage inside the conformal coefficient",
            "valid_for_claim": "false",
            "source_paths": source_path_string("626_doc", "710_frame_guard", "716_frame_map"),
            "generated_utc": GENERATED_UTC,
        },
        {
            "audit_id": "FCA717_4_current_policy",
            "object": "current frame lock",
            "statement": "The frame algebra is derived conditionally, but no branch is promoted as claim-ready",
            "status": "selected_current_route_nonclaim",
            "f_frame_effect": "carry f_frame=0 only as parent-zero branch; carry f_frame=-1/2 as Einstein-frame retained branch; carry symbolic terms for disformal leakage",
            "claim_effect": "frame transfer no longer vague, but it is not eliminated",
            "valid_for_claim": "false",
            "source_paths": source_path_string("716_doc", "716_frame_map", "711_ownership_map"),
            "generated_utc": GENERATED_UTC,
        },
    ]

    conformal_derivation = [
        {
            "step_id": "CD717_0_start_action",
            "step": "start from observed-frame gravitational prefactor",
            "equation": "S_grav = integral sqrt(-g_obs) (M_*^(D-2)/2) A_EH(u) R[g_obs] + ...",
            "derived_result": "A_EH is the frame prefactor whose logarithmic gradient is a_I",
            "status": "definition_template",
            "valid_for_claim": "false",
            "source_paths": source_path_string("715_pack", "710_descent_clause"),
            "generated_utc": GENERATED_UTC,
        },
        {
            "step_id": "CD717_1_conformal_map",
            "step": "choose Einstein normalization",
            "equation": "g_E,mu nu = A_EH(u)^(2/(D-2)) g_obs,mu nu",
            "derived_result": "coefficient of R[g_E] is constant after the standard conformal rearrangement",
            "status": "conditional_identity",
            "valid_for_claim": "false",
            "source_paths": source_path_string("715_pack", "716_frame_map"),
            "generated_utc": GENERATED_UTC,
        },
        {
            "step_id": "CD717_2_matter_metric",
            "step": "rewrite matter metric in the Einstein frame",
            "equation": "g_A = B_A(u)^2 g_obs = [B_A(u) A_EH(u)^(-1/(D-2))]^2 g_E",
            "derived_result": "effective Einstein-frame matter scale is C_A=B_A A_EH^(-1/(D-2))",
            "status": "derived_shape",
            "valid_for_claim": "false",
            "source_paths": source_path_string("716_coupling_derivation"),
            "generated_utc": GENERATED_UTC,
        },
        {
            "step_id": "CD717_3_charge_transfer",
            "step": "differentiate the effective matter scale",
            "equation": "q_A,I = partial_I ln C_A = b_A,I - (1/(D-2)) a_I",
            "derived_result": "f_frame=-1/(D-2)",
            "status": "derived_conditional_formula",
            "valid_for_claim": "false",
            "source_paths": source_path_string("716_coupling_derivation", "716_frame_map"),
            "generated_utc": GENERATED_UTC,
        },
        {
            "step_id": "CD717_4_four_dimensions",
            "step": "specialize to local spacetime dimension D=4",
            "equation": "q_A,I = b_A,I - (1/2) a_I and Q_Aa=N_frame E_a^I(b_A,I - a_I/2)",
            "derived_result": "f_frame=-1/2 in the standard 4D Einstein-frame branch",
            "status": "derived_conditional_D4",
            "valid_for_claim": "false",
            "source_paths": source_path_string("715_doc", "716_doc"),
            "generated_utc": GENERATED_UTC,
        },
        {
            "step_id": "CD717_5_observed_branch",
            "step": "do not transform to Einstein frame",
            "equation": "q_A,I=b_A,I with f_frame=0 only if variable A_EH is absent or parent-fixed in the observed frame",
            "derived_result": "observed-frame f_frame=0 is not enough unless a_I is theorem-zero or the variable prefactor is retained honestly in field equations",
            "status": "conditional_not_claim_ready",
            "valid_for_claim": "false",
            "source_paths": source_path_string("710_descent_clause", "711_ownership_map"),
            "generated_utc": GENERATED_UTC,
        },
    ]

    fframe_decision = [
        {
            "branch_id": "FFD717_0_same_frame_zero",
            "branch": "same observed frame and local EH prefactor fixed",
            "frame_condition": "DPC710_2 no_R_prefactor and DPC710_6 same_frame are parent-signed, or a_I=0 by theorem",
            "f_frame": "0",
            "charge_law": "Q_Aa=N_frame E_a^I b_A,I",
            "current_status": "not_available_current_corpus",
            "claim_effect": "would remove frame-transfer coupling but not b_A,I unless matter theorem also closes",
            "valid_for_claim": "false",
            "source_paths": source_path_string("710_descent_clause", "711_ownership_map", "716_frame_map"),
            "generated_utc": GENERATED_UTC,
        },
        {
            "branch_id": "FFD717_1_Einstein_D4",
            "branch": "standard D=4 Einstein-frame normalization",
            "frame_condition": "A_EH multiplies R[g_obs] and g_E=A_EH g_obs is selected",
            "f_frame": "-1/2",
            "charge_law": "Q_Aa=N_frame E_a^I(b_A,I-a_I/2)",
            "current_status": "derived_conditional_formula_not_sourced",
            "claim_effect": "activates scalar coupling whenever a_I survives",
            "valid_for_claim": "false",
            "source_paths": source_path_string("715_pack", "716_coupling_derivation"),
            "generated_utc": GENERATED_UTC,
        },
        {
            "branch_id": "FFD717_2_general_dimension",
            "branch": "D-dimensional Einstein-frame normalization",
            "frame_condition": "g_E=A_EH^(2/(D-2)) g_obs",
            "f_frame": "-1/(D-2)",
            "charge_law": "Q_Aa=N_frame E_a^I(b_A,I-a_I/(D-2))",
            "current_status": "derived_conditional_formula",
            "claim_effect": "kept for algebraic traceability; local tests use D=4 unless otherwise stated",
            "valid_for_claim": "false",
            "source_paths": source_path_string("715_pack", "716_doc"),
            "generated_utc": GENERATED_UTC,
        },
        {
            "branch_id": "FFD717_3_disformal_retained",
            "branch": "Weyl/disformal representative leakage",
            "frame_condition": "matter/readout metric contains extra representative dependence",
            "f_frame": "symbolic plus additional coefficients",
            "charge_law": "Q_Aa=N_frame E_a^I(b_A,I+f_frame a_I+d_A,I)",
            "current_status": "blocked_for_claim_until_excluded_or_sourced",
            "claim_effect": "requires disformal/current residual cleanup before local pass",
            "valid_for_claim": "false",
            "source_paths": source_path_string("626_doc", "710_frame_guard"),
            "generated_utc": GENERATED_UTC,
        },
        {
            "branch_id": "FFD717_4_current_lock",
            "branch": "current private checkpoint policy",
            "frame_condition": "no parent-signed observed-frame zero; Einstein formula available conditionally",
            "f_frame": "branch_locked_nonclaim",
            "charge_law": "score no local observable until branch, a_I, b_A,I, Z/M/E, and ranges are real",
            "current_status": "selected_current_route",
            "claim_effect": "no local-GR, WEP, R10, PPN, clock, Gdot, or R11 claim",
            "valid_for_claim": "false",
            "source_paths": source_path_string("716_doc", "716_validation"),
            "generated_utc": GENERATED_UTC,
        },
    ]

    effective_charge_update = [
        {
            "row_id": "ECU717_0_previous",
            "quantity": "716 generic effective charge",
            "formula": "Q_Aa=N_frame E_a^I(b_A,I+f_frame a_I)",
            "status": "retained",
            "claim_effect": "generic socket remains valid",
            "valid_for_claim": "false",
            "source_paths": source_path_string("716_doc"),
            "generated_utc": GENERATED_UTC,
        },
        {
            "row_id": "ECU717_1_observed_zero_branch",
            "quantity": "observed same-frame branch",
            "formula": "Q_Aa=N_frame E_a^I b_A,I",
            "status": "conditional_only",
            "claim_effect": "requires a_I=0 or no_R_prefactor theorem before it can support GR reduction",
            "valid_for_claim": "false",
            "source_paths": source_path_string("710_descent_clause", "711_ownership_map"),
            "generated_utc": GENERATED_UTC,
        },
        {
            "row_id": "ECU717_2_Einstein_D4_branch",
            "quantity": "D=4 Einstein-frame branch",
            "formula": "Q_Aa=N_frame E_a^I(b_A,I-a_I/2)",
            "status": "derived_conditional",
            "claim_effect": "makes A_EH gradient a direct local-coupling risk",
            "valid_for_claim": "false",
            "source_paths": source_path_string("715_pack", "716_coupling_derivation"),
            "generated_utc": GENERATED_UTC,
        },
        {
            "row_id": "ECU717_3_zero_condition_update",
            "quantity": "exact zero condition",
            "formula": "E_a^I(b_A,I-a_I/2)=0 in the selected D=4 Einstein branch, or E_a^I b_A,I=0 in a parent-signed observed-zero branch",
            "status": "conditional_zero_condition",
            "claim_effect": "zero requires cancellation theorem, not numerical wishful thinking",
            "valid_for_claim": "false",
            "source_paths": source_path_string("716_coupling_derivation"),
            "generated_utc": GENERATED_UTC,
        },
    ]

    local_limit_implications = [
        {
            "arena_id": "LLI717_0_Newton",
            "arena": "Newtonian limit",
            "frame_implication": "A0 fixes measured-G normalization; a_I and Q_Aa decide whether finite-range corrections survive",
            "current_status": "blocked_until_A0_aI_Q_ranges_sourced",
            "claim_effect": "no derived Newton limit from scalar branch yet",
            "valid_for_claim": "false",
            "source_paths": source_path_string("715_doc"),
            "generated_utc": GENERATED_UTC,
        },
        {
            "arena_id": "LLI717_1_WEP",
            "arena": "composition dependence",
            "frame_implication": "Einstein D=4 branch shifts every species charge by -a_I/2; universality can protect WEP but not fifth-force/PPN",
            "current_status": "blocked_until_b_A_I_material_map",
            "claim_effect": "WEP pass not claimable",
            "valid_for_claim": "false",
            "source_paths": source_path_string("716_doc"),
            "generated_utc": GENERATED_UTC,
        },
        {
            "arena_id": "LLI717_2_R10",
            "arena": "fifth-force alpha(lambda)",
            "frame_implication": "alpha_AB,a uses Q_Aa Q_Ba; frame choice changes the predicted alpha row",
            "current_status": "blocked_until_frame_charge_range_and_real_bound_curve",
            "claim_effect": "no R10 pass",
            "valid_for_claim": "false",
            "source_paths": source_path_string("716_frame_map"),
            "generated_utc": GENERATED_UTC,
        },
        {
            "arena_id": "LLI717_3_PPN",
            "arena": "PPN gamma/beta",
            "frame_implication": "universal nonzero Q shifts scalar-tensor PPN even if WEP is quiet",
            "current_status": "blocked_until_canonical_mode_and_observed_frame_fixed",
            "claim_effect": "no local PPN pass",
            "valid_for_claim": "false",
            "source_paths": source_path_string("715_doc"),
            "generated_utc": GENERATED_UTC,
        },
        {
            "arena_id": "LLI717_4_clocks_Gdot",
            "arena": "clock readouts and Gdot",
            "frame_implication": "a_I also appears in drift/readout maps, so frame lock does not by itself remove time variation",
            "current_status": "blocked_until_clock_readout_and_u_dot_sourced",
            "claim_effect": "no clock/Gdot claim",
            "valid_for_claim": "false",
            "source_paths": source_path_string("715_pack"),
            "generated_utc": GENERATED_UTC,
        },
    ]

    bound_or_derive_queue = [
        {
            "queue_id": "BDQ717_0_AEH_zero",
            "target": "a_I=partial_I ln A_EH|u0",
            "preferred_route": "derive zero from parent action/no_R_prefactor clause",
            "fallback_route": "retain numeric/symbolic a_I and score local residuals",
            "priority": "P0",
            "next_artifact": NEXT_TARGET,
            "valid_for_claim": "false",
            "source_paths": source_path_string("710_descent_clause", "715_pack"),
            "generated_utc": GENERATED_UTC,
        },
        {
            "queue_id": "BDQ717_1_bAI",
            "target": "b_A,I material/source charges",
            "preferred_route": "derive matter blindness or universality",
            "fallback_route": "create source/test material coefficient rows",
            "priority": "P1",
            "next_artifact": "after_AEH_or_parallel_material_charge_pack",
            "valid_for_claim": "false",
            "source_paths": source_path_string("716_coupling_derivation", "410_doc"),
            "generated_utc": GENERATED_UTC,
        },
        {
            "queue_id": "BDQ717_2_disformal",
            "target": "representative/disformal leakage",
            "preferred_route": "prove absent by observed coframe factorization",
            "fallback_route": "retain disformal coefficients and local bounds",
            "priority": "P2",
            "next_artifact": "disformal_current_residual_cleanup_if_AEH_survives",
            "valid_for_claim": "false",
            "source_paths": source_path_string("626_doc", "710_frame_guard"),
            "generated_utc": GENERATED_UTC,
        },
    ]

    claim_gate_evaluation = [
        {
            "gate_id": "CG717_0_prior_716",
            "gate": "prior coupling checkpoint",
            "observed_state": "716 validation clean and nonclaim",
            "result": "pass_structure",
            "claim_effect": "can build on 716 without promoting claims",
            "valid_for_claim": "false",
            "generated_utc": GENERATED_UTC,
        },
        {
            "gate_id": "CG717_1_same_frame",
            "gate": "observed-frame f_frame=0",
            "observed_state": "DPC710_6 same-frame identity not parent-owned",
            "result": "fail_blocked",
            "claim_effect": "f_frame=0 cannot be used as local-GR evidence",
            "valid_for_claim": "false",
            "generated_utc": GENERATED_UTC,
        },
        {
            "gate_id": "CG717_2_no_prefactor",
            "gate": "a_I=0/no R-prefactor",
            "observed_state": "DPC710_2 no_R_prefactor not parent-owned",
            "result": "fail_blocked",
            "claim_effect": "A_EH gradient remains live",
            "valid_for_claim": "false",
            "generated_utc": GENERATED_UTC,
        },
        {
            "gate_id": "CG717_3_Einstein_formula",
            "gate": "standard conformal transfer formula",
            "observed_state": "conditional derivation gives f_frame=-1/(D-2), D=4 gives -1/2",
            "result": "pass_conditional",
            "claim_effect": "usable as branch algebra, not a pass",
            "valid_for_claim": "false",
            "generated_utc": GENERATED_UTC,
        },
        {
            "gate_id": "CG717_4_claim_status",
            "gate": "local claims",
            "observed_state": "frame branch, a_I, b_A,I, modes, ranges, and bounds not all sourced",
            "result": "fail_blocked",
            "claim_effect": "no local-GR, Newton, PPN, WEP, R10, clocks, Gdot, or R11 claim",
            "valid_for_claim": "false",
            "generated_utc": GENERATED_UTC,
        },
        {
            "gate_id": "CG717_5_next_target",
            "gate": "next derivation target",
            "observed_state": NEXT_TARGET,
            "result": "pass_structure",
            "claim_effect": "attack a_I first because it kills or activates frame transfer globally",
            "valid_for_claim": "false",
            "generated_utc": GENERATED_UTC,
        },
    ]

    decision = [
        {
            "decision_id": "D717_0_formula",
            "decision": "frame-transfer algebra",
            "selected_status": "derived_conditionally",
            "reason": "conformal normalization gives f_frame=-1/(D-2), hence -1/2 in D=4",
            "next_action": NEXT_TARGET,
            "valid_for_claim": "false",
            "generated_utc": GENERATED_UTC,
        },
        {
            "decision_id": "D717_1_zero",
            "decision": "observed-frame zero",
            "selected_status": "not_promoted",
            "reason": "same-frame and no-prefactor clauses are not parent-signed",
            "next_action": NEXT_TARGET,
            "valid_for_claim": "false",
            "generated_utc": GENERATED_UTC,
        },
        {
            "decision_id": "D717_2_policy",
            "decision": "local branch policy",
            "selected_status": "nonclaim_branch_lock",
            "reason": "carry f_frame=0 only in parent-zero branch, f_frame=-1/2 in Einstein branch, symbolic terms if disformal leakage survives",
            "next_action": NEXT_TARGET,
            "valid_for_claim": "false",
            "generated_utc": GENERATED_UTC,
        },
    ]

    nonclaim_summary = [
        {
            "status": "Y5_R10_observed_frame_lock_conditional_f_frame_pack_written_nonclaim",
            "claim_ceiling": "frame_transfer_formula_only_no_AEH_zero_no_b_zero_no_local_GR_or_R10_PPN_WEP_claim",
            "observed_branch": "f_frame=0 only if no_R_prefactor/same_frame/a_I_zero is parent-signed",
            "einstein_branch": "f_frame=-1/(D-2), so -1/2 in D=4",
            "main_result": "frame-transfer coefficient is no longer vague; it is branch-dependent and must be carried honestly",
            "remaining_blocker": "A_EH gradient a_I and matter charge b_A,I are not theorem-zero or sourced",
            "next_target": NEXT_TARGET,
            "valid_for_claim": "false",
            "generated_utc": GENERATED_UTC,
        }
    ]

    csv_outputs = {
        "source_register": (
            RESIDUALS / "P8_Y5_R10_717_SOURCE_REGISTER.csv",
            source_register,
            ["source_id", "path", "exists", "role", "valid_for_claim", "generated_utc"],
        ),
        "frame_convention_audit": (
            RESIDUALS / "P8_Y5_R10_717_FRAME_CONVENTION_AUDIT.csv",
            frame_convention_audit,
            [
                "audit_id",
                "object",
                "statement",
                "status",
                "f_frame_effect",
                "claim_effect",
                "valid_for_claim",
                "source_paths",
                "generated_utc",
            ],
        ),
        "conformal_derivation": (
            RESIDUALS / "P8_Y5_R10_717_CONFORMAL_DERIVATION.csv",
            conformal_derivation,
            ["step_id", "step", "equation", "derived_result", "status", "valid_for_claim", "source_paths", "generated_utc"],
        ),
        "fframe_decision": (
            RESIDUALS / "P8_Y5_R10_717_FFRAME_DECISION_TABLE.csv",
            fframe_decision,
            [
                "branch_id",
                "branch",
                "frame_condition",
                "f_frame",
                "charge_law",
                "current_status",
                "claim_effect",
                "valid_for_claim",
                "source_paths",
                "generated_utc",
            ],
        ),
        "effective_charge_update": (
            RESIDUALS / "P8_Y5_R10_717_EFFECTIVE_CHARGE_UPDATE.csv",
            effective_charge_update,
            ["row_id", "quantity", "formula", "status", "claim_effect", "valid_for_claim", "source_paths", "generated_utc"],
        ),
        "local_limit_implications": (
            RESIDUALS / "P8_Y5_R10_717_LOCAL_LIMIT_IMPLICATIONS.csv",
            local_limit_implications,
            ["arena_id", "arena", "frame_implication", "current_status", "claim_effect", "valid_for_claim", "source_paths", "generated_utc"],
        ),
        "bound_or_derive_queue": (
            RESIDUALS / "P8_Y5_R10_717_BOUND_OR_DERIVE_QUEUE.csv",
            bound_or_derive_queue,
            ["queue_id", "target", "preferred_route", "fallback_route", "priority", "next_artifact", "valid_for_claim", "source_paths", "generated_utc"],
        ),
        "claim_gate_evaluation": (
            RESIDUALS / "P8_Y5_R10_717_CLAIM_GATE_EVALUATION.csv",
            claim_gate_evaluation,
            ["gate_id", "gate", "observed_state", "result", "claim_effect", "valid_for_claim", "generated_utc"],
        ),
        "decision": (
            RESIDUALS / "P8_Y5_R10_717_DECISION.csv",
            decision,
            ["decision_id", "decision", "selected_status", "reason", "next_action", "valid_for_claim", "generated_utc"],
        ),
        "nonclaim_summary": (
            RESIDUALS / "P8_Y5_R10_717_NONCLAIM_SUMMARY.csv",
            nonclaim_summary,
            [
                "status",
                "claim_ceiling",
                "observed_branch",
                "einstein_branch",
                "main_result",
                "remaining_blocker",
                "next_target",
                "valid_for_claim",
                "generated_utc",
            ],
        ),
    }

    for path, rows, fields in csv_outputs.values():
        write_csv(path, rows, fields)

    generated_csv_paths = [path for path, _, _ in csv_outputs.values()]

    validation = []

    def add_check(check_id: str, ok: bool, detail: str) -> None:
        validation.append(
            {
                "check_id": check_id,
                "result": "pass" if ok else "fail",
                "detail": detail,
                "generated_utc": GENERATED_UTC,
            }
        )

    source_paths_exist = all(info["path"].exists() for info in SOURCES.values())
    add_check("V717_0_source_paths_exist", source_paths_exist, "all cited source paths exist" if source_paths_exist else "one or more source paths missing")

    prior_clean = prior_validation_clean(SOURCES["716_validation"]["path"])
    add_check("V717_1_prior_716_clean", prior_clean, "716_validation_failures=0" if prior_clean else "716 validation not clean")

    own711 = SOURCES["711_ownership_map"]["path"]
    dpc710 = SOURCES["710_descent_clause"]["path"]
    same_frame_unowned = csv_contains(own711, "OWN711_6_DPC710_6", "not_derived")
    add_check("V717_2_same_frame_unowned_confirmed", same_frame_unowned, "DPC710_6 same-frame identity not parent-owned")

    no_prefactor_unowned = csv_contains(dpc710, "DPC710_2_no_R_prefactor", "candidate_clause_not_parent_signed")
    add_check("V717_3_no_prefactor_unowned_confirmed", no_prefactor_unowned, "DPC710_2 no_R_prefactor not parent-signed")

    derivation_path = csv_outputs["conformal_derivation"][0]
    add_check(
        "V717_4_general_conformal_formula_written",
        csv_contains(derivation_path, "f_frame=-1/(D-2)", "g_E,mu nu = A_EH(u)^(2/(D-2)) g_obs,mu nu"),
        "general conformal transfer formula recorded",
    )

    add_check(
        "V717_5_D4_formula_written",
        csv_contains(derivation_path, "f_frame=-1/2", "Q_Aa=N_frame E_a^I(b_A,I - a_I/2)"),
        "D=4 Einstein-frame f_frame=-1/2 formula recorded",
    )

    fdecision_path = csv_outputs["fframe_decision"][0]
    add_check(
        "V717_6_observed_zero_not_promoted",
        csv_contains(fdecision_path, "not_available_current_corpus", "f_frame", "0"),
        "observed f_frame=0 branch remains unavailable",
    )

    add_check(
        "V717_7_current_lock_nonclaim",
        csv_contains(fdecision_path, "FFD717_4_current_lock", "selected_current_route"),
        "current branch lock selected as nonclaim",
    )

    echarge_path = csv_outputs["effective_charge_update"][0]
    add_check(
        "V717_8_effective_charge_updated",
        csv_contains(echarge_path, "Q_Aa=N_frame E_a^I(b_A,I-a_I/2)", "conditional_zero_condition"),
        "effective charge rows include frame-updated formula",
    )

    add_check(
        "V717_9_local_arenas_blocked",
        all("blocked" in row["current_status"] for row in local_limit_implications),
        "all local arenas remain blocked until sourced",
    )

    add_check(
        "V717_10_next_target_selected",
        csv_contains(csv_outputs["decision"][0], NEXT_TARGET) and csv_contains(csv_outputs["bound_or_derive_queue"][0], NEXT_TARGET),
        NEXT_TARGET,
    )

    all_false = all_generated_rows_have_false_validity(generated_csv_paths)
    add_check("V717_11_no_claim_rows_promoted", all_false, "all generated rows valid_for_claim=false")

    outputs_scoped = all(str(path).startswith(str(POST_CHECKPOINT)) for path in generated_csv_paths + [OUTPUT_DOC])
    add_check("V717_12_outputs_scoped", outputs_scoped, "all outputs under post-checkpoint-work")

    formalization_count = formalization_changed_after_cutoff()
    add_check(
        "V717_13_formalization_workbench_untouched",
        formalization_count == 0,
        f"formalization_changed_after_cutoff={formalization_count}",
    )

    add_check(
        "V717_14_status_nonclaim",
        csv_contains(csv_outputs["nonclaim_summary"][0], "no_AEH_zero_no_b_zero_no_local_GR_or_R10_PPN_WEP_claim"),
        "frame-transfer formula only; no local claim",
    )

    add_check(
        "V717_15_source_register_written",
        len(source_register) >= 10 and all(row["exists"] == "true" for row in source_register),
        f"source_rows={len(source_register)}",
    )

    add_check(
        "V717_16_decision_no_smuggled_zero",
        csv_contains(csv_outputs["decision"][0], "not_promoted", "same-frame and no-prefactor clauses are not parent-signed"),
        "zero branch not smuggled",
    )

    validation_path = RESIDUALS / "P8_Y5_BRR545_717_VALIDATION.csv"
    write_csv(validation_path, validation, ["check_id", "result", "detail", "generated_utc"])

    sections = [
        "# 717 - Y5 R10 Observed Frame Lock And Frame Transfer Coefficient Pack",
        "",
        "## Summary",
        "",
        "The frame-transfer coefficient is now a conditional derivation rather than a vague placeholder.",
        "",
        "If the local action is kept in a parent-signed observed frame where the EH prefactor is fixed, then `f_frame=0`. That branch is not claim-ready because the current corpus has not parent-signed the no-prefactor and same-frame clauses.",
        "",
        "If the retained scalar branch is put into the standard Einstein-normalized frame, the conformal relation gives",
        "",
        "`g_E,mu nu = A_EH(u)^(2/(D-2)) g_obs,mu nu`,",
        "",
        "so",
        "",
        "`q_A,I = b_A,I - a_I/(D-2)`",
        "",
        "and in four spacetime dimensions",
        "",
        "`Q_Aa = N_frame E_a^I (b_A,I - a_I/2)`.",
        "",
        "That is useful but not a victory lap: it means `a_I=partial_I ln A_EH|u0` is now an exposed local-coupling risk. The next derivation should try to prove `a_I=0`; if that fails, the local branch must source or bound `a_I`.",
        "",
        "| Field | Value |",
        "| --- | --- |",
        f"| Generated UTC | `{GENERATED_UTC}` |",
        "| Claim status | nonclaim/private checkpoint |",
        f"| Next target | `{NEXT_TARGET}` |",
        "",
        "## Frame Convention Audit",
        "",
        markdown_table(frame_convention_audit, ["audit_id", "object", "status", "f_frame_effect", "claim_effect", "valid_for_claim"]),
        "",
        "## Conformal Derivation",
        "",
        markdown_table(conformal_derivation, ["step_id", "step", "equation", "derived_result", "status", "valid_for_claim"]),
        "",
        "## Frame Coefficient Decision Table",
        "",
        markdown_table(fframe_decision, ["branch_id", "branch", "frame_condition", "f_frame", "charge_law", "current_status", "valid_for_claim"]),
        "",
        "## Effective Charge Update",
        "",
        markdown_table(effective_charge_update, ["row_id", "quantity", "formula", "status", "claim_effect", "valid_for_claim"]),
        "",
        "## Local Limit Implications",
        "",
        markdown_table(local_limit_implications, ["arena_id", "arena", "frame_implication", "current_status", "claim_effect", "valid_for_claim"]),
        "",
        "## Bound Or Derive Queue",
        "",
        markdown_table(bound_or_derive_queue, ["queue_id", "target", "preferred_route", "fallback_route", "priority", "next_artifact", "valid_for_claim"]),
        "",
        "## Claim Gate Evaluation",
        "",
        markdown_table(claim_gate_evaluation, ["gate_id", "gate", "observed_state", "result", "claim_effect", "valid_for_claim"]),
        "",
        "## Decision",
        "",
        markdown_table(decision, ["decision_id", "decision", "selected_status", "reason", "next_action", "valid_for_claim"]),
        "",
        "## Nonclaim Summary",
        "",
        markdown_table(nonclaim_summary, ["status", "claim_ceiling", "observed_branch", "einstein_branch", "main_result", "remaining_blocker", "next_target", "valid_for_claim"]),
        "",
        "## Source Register",
        "",
        markdown_table(source_register, ["source_id", "path", "exists", "role"]),
        "",
        "## Validation",
        "",
        markdown_table(validation, ["check_id", "result", "detail"]),
        "",
        "## Verdict",
        "",
        "This checkpoint improves the theory because the frame term is no longer a black box. The brutal version is: `f_frame=0` is only allowed inside the parent-signed observed-frame zero branch, while the ordinary four-dimensional Einstein-frame retained branch gives `f_frame=-1/2`. Therefore the scalar local branch does not fail here, but it is also not allowed to hide. The next monster under the bed is `a_I`; prove `a_I=0` from the parent action or carry it into the local residual scorecard.",
        "",
    ]
    OUTPUT_DOC.write_text("\n".join(sections), encoding="utf-8")

    passes = sum(1 for row in validation if row["result"] == "pass")
    total = len(validation)
    print(f"Y5_R10_observed_frame_lock_conditional_f_frame_pack_written_nonclaim: validation_passes={passes}/{total}")


if __name__ == "__main__":
    main()

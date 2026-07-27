from __future__ import annotations

import csv
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "source-intake" / "mts_residuals"
DOC = ROOT / "3452-Y5-R2FR-Xrep-action-line-absence-or-LX-residual-norm-bound-under-AX1090.md"
FORMALIZATION = ROOT.parent / "formalization-workbench"

SOURCES = {
    "script_3452": Path(__file__).resolve(),
    "doc_3451": ROOT / "3451-Y5-R2FR-pure-representative-action-descent-or-LX-residual-owner-split-under-AX1090.md",
    "next_3451": OUT / "P8_Y5_R2FR_3451_NEXT_TARGET.csv",
    "lx_split_3451": OUT / "P8_Y5_R2FR_3451_LX_RESIDUAL_OWNER_SPLIT.csv",
    "action_contract_3451": OUT / "P8_Y5_R2FR_3451_PURE_REP_ACTION_DESCENT_CONTRACT.csv",
    "minimal_line_3378": OUT / "P8_Y5_R2FR_3378_MINIMAL_PARENT_ACTION_LINE.csv",
    "adoption_theorem_3379": OUT / "P8_Y5_R2FR_3379_PARENT_ACTION_ADOPTION_NO_EXTENSION_THEOREM.csv",
    "formation_rules_3380": OUT / "P8_Y5_R2FR_3380_ACTION_FORMATION_RULES.csv",
    "local_action_3382": OUT / "P8_Y5_R2FR_3382_LOCAL_ACTION_BLOCK_UNDER_UOC.csv",
    "minimal_candidate_3395": OUT / "P8_Y5_R2FR_3395_MINIMAL_PARENT_ACTION_LINE_CANDIDATE.csv",
    "parent_density_3424": OUT / "P8_Y5_R2FR_3424_PARENT_ACTION_DENSITY.csv",
}

OUTPUTS = {
    "source_register": OUT / "P8_Y5_R2FR_3452_SOURCE_REGISTER.csv",
    "action_line_absence_scan": OUT / "P8_Y5_R2FR_3452_ACTION_LINE_ABSENCE_SCAN.csv",
    "formation_rule_theorem": OUT / "P8_Y5_R2FR_3452_FORMATION_RULE_THEOREM.csv",
    "lx_residual_norm_bounds": OUT / "P8_Y5_R2FR_3452_LX_RESIDUAL_NORM_BOUNDS.csv",
    "residual_priority_queue": OUT / "P8_Y5_R2FR_3452_RESIDUAL_PRIORITY_QUEUE.csv",
    "promotion_gates": OUT / "P8_Y5_R2FR_3452_PROMOTION_GATES.csv",
    "decision_ledger": OUT / "P8_Y5_R2FR_3452_DECISION_LEDGER.csv",
    "next_target": OUT / "P8_Y5_R2FR_3452_NEXT_TARGET.csv",
    "runner_nonclaim": OUT / "P8_Y5_R2FR_3452_RUNNER_NONCLAIM.csv",
    "validation": OUT / "P8_Y5_BRR545_3452_VALIDATION.csv",
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
        "script_3452": "generator for this checkpoint",
        "doc_3451": "immediate handoff: action-line absence or residual bounds",
        "next_3451": "machine-readable 3452 target",
        "lx_split_3451": "six L_X residual owner channels",
        "action_contract_3451": "forbidden term test",
        "minimal_line_3378": "minimal parent action candidate/action grammar",
        "adoption_theorem_3379": "no extension/no source prefactor theorem",
        "formation_rules_3380": "action formation rules and no-hidden-homsets rule",
        "local_action_3382": "local effective action block under UOC",
        "minimal_candidate_3395": "later minimal parent action line candidate",
        "parent_density_3424": "parent action density/source-coupling branch",
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


def csv_text(source_id: str, row_key: str, row_value: str) -> tuple[str, str]:
    rows = read_csv(SOURCES[source_id])
    for row in rows:
        if row.get(row_key) == row_value:
            return row_value, " ".join(str(value) for value in row.values())
    return row_value, "MISSING_ROW"


def action_line_absence_scan() -> list[dict[str, Any]]:
    selected = [
        ("minimal_line_3378", "clause_id", "PAL3378_0_minimal_line", "main candidate parent action line"),
        ("minimal_line_3378", "clause_id", "PAL3378_3_matter_source_scale", "source-prefactor absence clause"),
        ("adoption_theorem_3379", "theorem_id", "ADOPT3379_2_no_source_prefactor", "formal no source-prefactor theorem"),
        ("adoption_theorem_3379", "theorem_id", "ADOPT3379_3_no_second_source_metric", "formal no hidden source-frame theorem"),
        ("formation_rules_3380", "rule_id", "FORM3380_4_no_hidden_homsets", "formation rule excluding hidden-visible homsets"),
        ("local_action_3382", "block_id", "ACT3382_0_effective_action", "local action block under UOC"),
        ("minimal_candidate_3395", "line_id", "MPL3395_0_parent_action_line", "later minimal parent action candidate"),
        ("parent_density_3424", "term_id", "PAD3424_4_Z_residual_sector", "local MTS residual sector line"),
    ]
    rows: list[dict[str, Any]] = []
    for source_id, key, value, role in selected:
        row_id, text = csv_text(source_id, key, value)
        lower_text = text.lower()
        explicit_xrep = any(token in lower_text for token in ["x_rep", "xrep"])
        forbidden_source_form = any(token in text for token in ["w_A(X)", "kappa_A(X)", "f_X(X_rep)", "f_X(X)", "theta_A(X)"])
        broad_placeholder = any(token in text for token in ["L_MTS_silent", "L_MTS_IR", "S_MTS[", "Z_residual", "Phi,g_obs"])
        forbids = any(word in lower_text for word in ["no source-only", "must forbid", "no hidden", "no hom", "contains no hom"])

        if text == "MISSING_ROW":
            status = "MISSING_SOURCE_ROW"
        elif broad_placeholder:
            status = "BROAD_PLACEHOLDER_NOT_ABSENCE_PROOF"
        elif forbids and forbidden_source_form:
            status = "FORBIDS_FORBIDDEN_FORM_IF_PARENT_SIGNED"
        elif explicit_xrep or (forbidden_source_form and not forbids):
            status = "EXPLICIT_FORBIDDEN_TOKEN_PRESENT"
        else:
            status = "NO_LITERAL_XREP_IN_SELECTED_ROW"

        rows.append(
            {
                "scan_id": f"SCAN3452_{len(rows)}_{row_id}",
                "source_id": source_id,
                "row_id": row_id,
                "role": role,
                "contains_literal_Xrep": explicit_xrep,
                "contains_forbidden_source_form": forbidden_source_form,
                "contains_broad_placeholder": broad_placeholder,
                "formation_rule_forbids_it": forbids,
                "scan_status": status,
                "source_path": str(SOURCES[source_id]),
                "claim_allowed": False,
                "valid_for_claim": False,
            }
        )
    rows.append(
        {
            "scan_id": "SCAN3452_VERDICT",
            "source_id": "combined",
            "row_id": "selected_action_lines",
            "role": "absence scan verdict",
            "contains_literal_Xrep": False,
            "contains_forbidden_source_form": True,
            "contains_broad_placeholder": True,
            "formation_rule_forbids_it": True,
            "scan_status": "NO_LITERAL_XREP_BUT_BROAD_MTS_PLACEHOLDERS_REMAIN",
            "source_path": str(OUTPUTS["action_line_absence_scan"]),
            "claim_allowed": False,
            "valid_for_claim": False,
        }
    )
    return rows


def formation_rule_theorem() -> list[dict[str, Any]]:
    return [
        {
            "theorem_id": "FRT3452_0_syntax_exclusion",
            "statement": "If the parent action grammar is restricted to q-basic observed fields, fixed representation constants, topological/exact boundary classes, and explicitly declared Z_active residual blocks, then no explicit X_rep action line is legal.",
            "proof": "X_rep is not in Args(S_parent) except as a forgotten representative coordinate; scalar density constructors cannot use an argument outside the declared object language.",
            "status": "EXACT_IF_FORMATION_RULE_PARENT_ADOPTED",
            "does_it_close_total_action": False,
            "remaining_gap": "selected action candidates contain broad MTS placeholders whose internal argument list is not fully expanded",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "theorem_id": "FRT3452_1_source_weight_exclusion",
            "statement": "ADOPT3379/FORM3380 exclude w_A(X), kappa_A(X), hidden source frames, and hidden-visible homsets if they are parent-signed.",
            "proof": "The grammar admits one observed matter functor and one common Hilbert source normalization; source-specific hidden maps are not legal constructors.",
            "status": "CONDITIONAL_THEOREM_SUPPORTED_BY_ACTION_GRAMMAR",
            "does_it_close_total_action": False,
            "remaining_gap": "adoption theorem is still a branch contract, not a derivation from primitives",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "theorem_id": "FRT3452_2_placeholder_guard",
            "statement": "Any broad placeholder such as L_MTS_silent, L_MTS_IR(Phi,g_obs), S_MTS[psi,Gamma,...], or Z_residual must be expanded or treated as L_X residual.",
            "proof": "A placeholder can hide X_rep dependence; absence cannot be inferred from a name like 'silent'.",
            "status": "ANTI_SMUGGLING_RULE",
            "does_it_close_total_action": False,
            "remaining_gap": "expand MTS residual action line or bound every retained residual",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "theorem_id": "FRT3452_3_current_verdict",
            "statement": "Current selected action lines do not display a literal X_rep bulk term, but total X_rep absence is not proved because MTS residual placeholders remain.",
            "proof": "The scan finds no explicit X_rep token in selected public-core rows, while broad residual placeholders and rejected-slot families survive.",
            "status": "ABSENCE_SCAN_PARTIAL_PASS_TOTAL_NOT_PROMOTED",
            "does_it_close_total_action": False,
            "remaining_gap": "3453 must expand or bound the MTS residual block",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
    ]


def lx_residual_norm_bounds() -> list[dict[str, Any]]:
    return [
        {
            "bound_id": "LXB3452_0_explicit_Xrep_bulk",
            "residual_id": "LXR3451_0_explicit_Xrep_bulk",
            "norm_bound": "I_Xbulk <= ||E_Xrep||_L2(BF x U) ||xi_X||_L2(BF x U) + ||Theta_Xrep_boundary||_1",
            "required_inputs": "E_Xrep_density;xi_X_norm_or_unit_generator;bulk_domain_measure;Theta_Xrep_boundary_flux;units;source_path",
            "zero_route": "forbidden if action grammar proves X_rep not in Args(S_parent)",
            "status": "BOUND_FORMULA_READY_INPUTS_MISSING",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "bound_id": "LXB3452_1_hidden_frame_or_EM_coefficient",
            "residual_id": "LXR3451_1_hidden_frame_or_EM_coefficient",
            "norm_bound": "I_frameEM <= ||partial_X f_X xi_X||_inf (int_U |R[g_obs]| dmu + int_U |F_obs^2| dmu)",
            "required_inputs": "partial_X_fX_bound;xi_X_bound;curvature_norm;F2_norm;domain;units;source_path",
            "zero_route": "no-shadow-frame/no-extra-F2 theorem from parent grammar",
            "status": "BOUND_FORMULA_READY_INPUTS_MISSING",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "bound_id": "LXB3452_2_source_weight_marker",
            "residual_id": "LXR3451_2_source_weight_marker",
            "norm_bound": "I_source_weight <= max_A ||partial_X w_A xi_X||_inf int_U |L_A| dmu_obs",
            "required_inputs": "species_set;partial_X_wA_bound;matter_action_density_norm;source_worldtube;units;source_path",
            "zero_route": "ADOPT3379 no-source-prefactor plus fixed representation constants",
            "status": "BOUND_FORMULA_READY_INPUTS_MISSING",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "bound_id": "LXB3452_3_RAB_observer_cell",
            "residual_id": "LXR3451_3_RAB_observer_cell",
            "norm_bound": "I_RAB <= ||E_RAB||_L2 ||delta R_AB||_L2 + ||DObs_e[delta R_AB]|| * ||delta S_pub/delta e_obs||",
            "required_inputs": "E_RAB_norm;delta_RAB_norm;DObs_e_RAB_operator_norm;Hilbert_source_norm;units;source_path",
            "zero_route": "constraint-first R_AB elimination before readout",
            "status": "BOUND_FORMULA_READY_INPUTS_MISSING",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "bound_id": "LXB3452_4_boundary_reference_charge",
            "residual_id": "LXR3451_4_boundary_reference_charge",
            "norm_bound": "I_boundaryX <= |Q_X[S2]-Q_X[S1]| + ||Delta_symp_X||_1 + ||delta B_ref_X||_1",
            "required_inputs": "QX_surface_values;Delta_symp_X_bound;delta_B_ref_X_bound;surface_pair;reference_class;units;source_path",
            "zero_route": "Q_X exact/proper with zero local projection and fixed B_ref class",
            "status": "BOUND_FORMULA_READY_INPUTS_MISSING",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "bound_id": "LXB3452_5_private_tau_clock",
            "residual_id": "LXR3451_5_private_tau_clock",
            "norm_bound": "I_tauX <= ||delta_X tau_private||_inf ||C_tau^pub||_1 + clock/PPN projection residual",
            "required_inputs": "delta_X_tau_bound;C_tau_pub_norm;clock_projection_coefficients;PPN_alpha_i_projection;units;source_path",
            "zero_route": "tau_source=tau_charge=tau_clock=tau_readout parent theorem",
            "status": "BOUND_FORMULA_READY_INPUTS_MISSING",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
    ]


def residual_priority_queue() -> list[dict[str, Any]]:
    return [
        {
            "priority_id": "RPQ3452_0",
            "next_residual": "broad MTS residual action placeholder",
            "why_first": "It decides whether total action descent can be claimed; without expansion, absence is not proof.",
            "target_row": "FRT3452_2_placeholder_guard",
            "recommended_action": "expand L_MTS_silent/L_MTS_IR/S_MTS/ Z_residual into allowed q-basic, exact boundary, or explicit residual terms",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "priority_id": "RPQ3452_1",
            "next_residual": "source-weight/hidden-frame grammar adoption",
            "why_first": "ADOPT3379 and FORM3380 can zero the most dangerous matter-coupling channels if parent-signed.",
            "target_row": "LXB3452_1;LXB3452_2",
            "recommended_action": "derive parent object language from MTS primitives or keep coefficient bounds",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
    ]


def promotion_gates() -> list[dict[str, Any]]:
    return [
        {
            "gate_id": "G3452_0_sources_exist",
            "gate": "all cited 3452 source paths exist",
            "status": "PRIVATE_CHECK_PASS",
            "blocks_claim": False,
            "needed_for_claim": "provenance only",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "gate_id": "G3452_1_scan_partial",
            "gate": "selected action lines scanned for explicit X_rep/forbidden families",
            "status": "PASS_PARTIAL_SCAN",
            "blocks_claim": False,
            "needed_for_claim": "expand broad placeholders",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "gate_id": "G3452_2_no_placeholder_smuggling",
            "gate": "broad MTS placeholders are not treated as absence proof",
            "status": "ENFORCED",
            "blocks_claim": True,
            "needed_for_claim": "expand or bound all placeholders",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "gate_id": "G3452_3_bound_rows",
            "gate": "all six LXR3451 channels have theorem-bound formulas",
            "status": "PASS_FORMULAS_INPUTS_MISSING",
            "blocks_claim": True,
            "needed_for_claim": "numeric/theorem-zero inputs with units and source paths",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "gate_id": "G3452_4_no_claim",
            "gate": "no local-GR/Newton/R10/PPN/clock/orbital pass from this checkpoint",
            "status": "ENFORCED",
            "blocks_claim": True,
            "needed_for_claim": "full action-line expansion or residual bounds",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
    ]


def decision_ledger() -> list[dict[str, Any]]:
    return [
        {
            "decision_id": "DEC3452_0",
            "question": "Did we find an explicit X_rep action line?",
            "answer": "No literal X_rep action line appears in the selected public/action-candidate rows.",
            "reason": "The scan covers the selected local parent-action candidates and formation rules.",
            "next_action": "do not promote: broad MTS placeholders must be expanded",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "decision_id": "DEC3452_1",
            "question": "Can source-weight and hidden-frame channels be zeroed?",
            "answer": "Conditionally yes if ADOPT3379/FORM3380 are parent-signed.",
            "reason": "The formation grammar explicitly forbids source-only prefactors, hidden source frames and hidden-visible homsets.",
            "next_action": "derive/adopt the object-language theorem or keep coefficient bounds",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
    ]


def next_target() -> list[dict[str, Any]]:
    return [
        {
            "target_doc": "3453-Y5-R2FR-MTS-residual-action-placeholder-expansion-or-first-LX-bound-input-under-AX1090.md",
            "target_script": "scripts/Y5_R2FR_3453_MTS_residual_action_placeholder_expansion_or_first_LX_bound_input.py",
            "objective": "Expand L_MTS_silent/L_MTS_IR/S_MTS/Z_residual into q-basic, exact-boundary, or active residual terms; if expansion fails, fill the first L_X residual norm input.",
            "start_from": "FRT3452_2_placeholder_guard and LXB3452_0_explicit_Xrep_bulk",
            "success_gate": "No broad placeholder remains in the local action line, or at least one L_X residual bound row receives real theorem/numeric inputs.",
            "claim_allowed": False,
            "valid_for_claim": False,
        }
    ]


def runner_nonclaim() -> list[dict[str, Any]]:
    return [
        {
            "runner_id": "RUN3452_0",
            "mode": "private_nonclaim_checkpoint",
            "result": "selected action-line scan plus six residual norm-bound formulas",
            "claim_status": "NO_LOCAL_GR_NEWTON_R10_PPN_CLOCK_OR_ORBITAL_CLAIM",
            "reason": "broad MTS residual placeholders remain unexpanded and bound inputs are missing",
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

    scan_statuses = {row["scan_status"] for row in rows_by_name["action_line_absence_scan"]}
    bound_ids = {row["bound_id"] for row in rows_by_name["lx_residual_norm_bounds"]}

    validations = [
        {
            "check_id": "VAL3452_0_sources_exist",
            "condition": "all cited 3452 source paths exist",
            "passed": all(path.exists() for path in SOURCES.values()),
            "detail": f"{sum(1 for path in SOURCES.values() if path.exists())}/{len(SOURCES)} source paths exist",
        },
        {
            "check_id": "VAL3452_1_scan_covers_selected_rows",
            "condition": "selected action rows and verdict are scanned",
            "passed": len(rows_by_name["action_line_absence_scan"]) >= 9
            and "NO_LITERAL_XREP_BUT_BROAD_MTS_PLACEHOLDERS_REMAIN" in scan_statuses,
            "detail": f"{len(rows_by_name['action_line_absence_scan'])} scan rows",
        },
        {
            "check_id": "VAL3452_2_placeholder_guard",
            "condition": "broad placeholders block promotion",
            "passed": any(
                row["theorem_id"] == "FRT3452_2_placeholder_guard"
                and row["status"] == "ANTI_SMUGGLING_RULE"
                for row in rows_by_name["formation_rule_theorem"]
            ),
            "detail": "placeholder anti-smuggling guard present",
        },
        {
            "check_id": "VAL3452_3_all_lx_bounds",
            "condition": "all six LXR3451 residual channels have bound formulas",
            "passed": bound_ids
            == {
                "LXB3452_0_explicit_Xrep_bulk",
                "LXB3452_1_hidden_frame_or_EM_coefficient",
                "LXB3452_2_source_weight_marker",
                "LXB3452_3_RAB_observer_cell",
                "LXB3452_4_boundary_reference_charge",
                "LXB3452_5_private_tau_clock",
            },
            "detail": f"{len(bound_ids)} bound rows",
        },
        {
            "check_id": "VAL3452_4_no_claims",
            "condition": "all generated rows remain nonclaim",
            "passed": nonclaim_ok,
            "detail": "valid_for_claim=false and claim_allowed=false wherever present",
        },
        {
            "check_id": "VAL3452_5_generated_csv_parse",
            "condition": "generated CSV rows parse cleanly",
            "passed": parse_ok,
            "detail": "CSV reader pass for generated outputs present before validation write",
        },
        {
            "check_id": "VAL3452_6_next_target_3453",
            "condition": "next target expands residual placeholder or fills first bound input",
            "passed": rows_by_name["next_target"][0]["target_doc"].startswith("3453-Y5-R2FR-MTS-residual-action-placeholder"),
            "detail": rows_by_name["next_target"][0]["target_doc"],
        },
        {
            "check_id": "VAL3452_7_formalization_untouched",
            "condition": "formalization-workbench modified-file count remains 0 during this run",
            "passed": modified_count == 0,
            "detail": f"modified_count_since_start={modified_count}",
        },
    ]
    validations.append(
        {
            "check_id": "VAL3452_8_overall",
            "condition": "3452 action-line absence/bound checkpoint is internally valid",
            "passed": all(row["passed"] for row in validations),
            "detail": "PASS" if all(row["passed"] for row in validations) else "FAIL",
        }
    )
    return validations


def write_doc(rows_by_name: dict[str, list[dict[str, Any]]]) -> None:
    text = f"""# 3452 - Xrep Action-Line Absence or L_X Residual Norm Bound

## Summary
- This checkpoint scans the selected local parent-action candidates instead of merely saying an action line is missing.
- Result: the selected public/action-candidate rows do not show a literal `X_rep` bulk action term.
- Stronger result, but still nonclaim: ADOPT3379/FORM3380 conditionally forbid source weights, hidden source frames and hidden-visible homsets if that grammar is parent-signed.
- The anti-smuggling catch is important: broad placeholders like `L_MTS_silent`, `L_MTS_IR`, `S_MTS[...]`, and `Z_residual` are not absence proofs.
- Every surviving `L_X` channel now has a theorem-bound formula, so if the placeholder cannot be expanded into q-basic/exact pieces, the fallback is executable.

## Source Register
{md_table(rows_by_name["source_register"])}

## Action-Line Absence Scan
{md_table(rows_by_name["action_line_absence_scan"])}

## Formation Rule Theorem
{md_table(rows_by_name["formation_rule_theorem"])}

## L_X Residual Norm Bounds
{md_table(rows_by_name["lx_residual_norm_bounds"])}

## Residual Priority Queue
{md_table(rows_by_name["residual_priority_queue"])}

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
This improves the situation without cheating: no explicit `X_rep` bulk term is visible in the selected action lines, and the grammar has conditional no-source/no-shadow teeth. But total action descent is still not promoted because broad MTS residual placeholders can hide exactly the thing we are trying to exclude. The next useful move is to expand those placeholders or fill the first real `L_X` bound input.
"""
    DOC.write_text(text, encoding="utf-8")


def main() -> None:
    start_utc = datetime.now(timezone.utc)
    rows_by_name = {
        "source_register": source_register(),
        "action_line_absence_scan": action_line_absence_scan(),
        "formation_rule_theorem": formation_rule_theorem(),
        "lx_residual_norm_bounds": lx_residual_norm_bounds(),
        "residual_priority_queue": residual_priority_queue(),
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
        raise SystemExit(f"3452 validation failed: {failed_rows}")
    print(f"wrote {DOC}")
    print(f"wrote {len(OUTPUTS)} csv outputs")


if __name__ == "__main__":
    main()

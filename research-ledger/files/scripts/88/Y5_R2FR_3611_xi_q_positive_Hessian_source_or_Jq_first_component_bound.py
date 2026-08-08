from __future__ import annotations

import csv
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
RESIDUALS = ROOT / "source-intake" / "mts_residuals"
FORMALIZATION = ROOT.parent / "formalization-workbench"
CHECKPOINT_ID = "3611"
BRANCH_ID = "MTS_R2FR_Y5_XI_Q_POSITIVE_HESSIAN_OR_JQ_FIRST_COMPONENT_BOUND_3611"
DOC = ROOT / "3611-Y5-R2FR-xi-q-positive-Hessian-source-or-Jq-first-component-bound.md"


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as csv_handle:
        return list(csv.DictReader(csv_handle))


def write_csv(path: Path, rows: list[dict[str, object]]) -> None:
    if not rows:
        raise ValueError(f"refusing to write empty csv: {path}")
    path.parent.mkdir(parents=True, exist_ok=True)
    fieldnames: list[str] = []
    for row in rows:
        for fieldname in row:
            if fieldname not in fieldnames:
                fieldnames.append(fieldname)
    with path.open("w", encoding="utf-8", newline="") as csv_handle:
        writer = csv.DictWriter(csv_handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def source_contains(path: Path, needle: str) -> bool:
    return needle in path.read_text(encoding="utf-8-sig", errors="replace")


def source_map() -> dict[str, tuple[Path, str]]:
    return {
        "handoff_3610": (
            RESIDUALS / "P8_Y5_R2FR_3610_NEXT_TARGET.csv",
            "3611-Y5-R2FR-xi-q-positive-Hessian-source-or-Jq-first-component-bound.md",
        ),
        "zq_jq_3610": (
            RESIDUALS / "P8_Y5_R2FR_3610_ZQ_JQ_EXTRACTION_ROWS.csv",
            "lambda_q = sqrt(Z_q/M_q^2) = xi_q",
        ),
        "hessian_hunt_2314": (
            RESIDUALS / "P8_Y5_PARENT_QLOC_2314_HESSIAN_SOURCE_HUNT.csv",
            "lambda_q=xi_q",
        ),
        "positive_nohair_3092": (
            RESIDUALS / "P8_Y5_R2FR_3092_POSITIVE_NOHAIR_CONTRACT.csv",
            "Z_X>=Z_min>0",
        ),
        "positive_operator_3429": (
            RESIDUALS / "P8_Y5_R2FR_3429_POSITIVE_OPERATOR_NOHAIR_THEOREM.csv",
            "BOUND_FORMULA_READY_VALUES_MISSING",
        ),
        "yloc_euler_3535": (
            RESIDUALS / "P8_Y5_R2FR_3535_YLOC_EULER_THEOREM.csv",
            "Positive Hessian/mass gap",
        ),
        "jq_zero_2431": (
            RESIDUALS / "P8_Y5_PARENT_QLOC_2431_JQ_DESCENT_ZERO_THEOREM.csv",
            "J_q=0 is not proved",
        ),
        "jq_components_2431": (
            RESIDUALS / "P8_Y5_PARENT_QLOC_2431_JQ_COMPONENT_BOUND_VECTOR.csv",
            "J_q^matter_bulk",
        ),
        "matter_pullback_3095": (
            RESIDUALS / "P8_Y5_R2FR_3095_MATTER_PULLBACK_DERIVATION.csv",
            "delta_v S_T",
        ),
        "matter_source_functor_3235": (
            RESIDUALS / "P8_Y5_R2FR_3235_MATTER_SOURCE_FUNCTOR_DERIVATION.csv",
            "delta_v S_A",
        ),
        "matter_bound_3235": (
            RESIDUALS / "P8_Y5_R2FR_3235_JMATTER_COMPONENT_BOUND.csv",
            "J_matter_bound",
        ),
        "no_source_only_3509": (
            RESIDUALS / "P8_Y5_R2FR_3509_NO_SOURCE_ONLY_MATTER_FUNCTOR_THEOREM.csv",
            "no source-only matter coefficient slot",
        ),
        "xi_overlap_3304": (
            RESIDUALS / "P8_Y5_R2FR_3304_XI_OVERLAP_DEFINITION.csv",
            "Xi_0[A]",
        ),
        "alpha_xi_3311": (
            RESIDUALS / "P8_Y5_R2FR_3311_ALPHA_XI_FACTOR_LAW.csv",
            "A_i is a finite-mode relative source factor",
        ),
    }


def output_paths() -> dict[str, Path]:
    return {
        "source_register": RESIDUALS / "P8_Y5_R2FR_3611_SOURCE_REGISTER.csv",
        "xi_q_audit": RESIDUALS / "P8_Y5_R2FR_3611_XI_Q_POSITIVE_HESSIAN_AUDIT.csv",
        "jq_matter_bound": RESIDUALS / "P8_Y5_R2FR_3611_JQ_FIRST_COMPONENT_BOUND.csv",
        "decision_gates": RESIDUALS / "P8_Y5_R2FR_3611_DECISION_GATES.csv",
        "status": RESIDUALS / "P8_Y5_R2FR_3611_STATUS.csv",
        "next_target": RESIDUALS / "P8_Y5_R2FR_3611_NEXT_TARGET.csv",
        "canonical_status": RESIDUALS / "P8_Y5_xi_q_positive_Hessian_or_Jq_first_bound_status.csv",
        "validation": RESIDUALS / "P8_Y5_BRR545_3611_VALIDATION.csv",
    }


def source_register_rows(sources: dict[str, tuple[Path, str]]) -> list[dict[str, object]]:
    timestamp = utc_now()
    rows: list[dict[str, object]] = []
    for source_id, source_tuple in sources.items():
        source_path, needle = source_tuple
        exists = source_path.exists()
        rows.append(
            {
                "timestamp_utc": timestamp,
                "branch_id": BRANCH_ID,
                "checkpoint_id": CHECKPOINT_ID,
                "source_id": source_id,
                "source_path": str(source_path),
                "exists": exists,
                "needle": needle,
                "needle_found": exists and source_contains(source_path, needle),
                "valid_for_claim": False,
            }
        )
    return rows


def xi_q_audit_rows(sources: dict[str, tuple[Path, str]]) -> list[dict[str, object]]:
    source_paths = {source_id: str(source_tuple[0]) for source_id, source_tuple in sources.items()}
    timestamp = utc_now()
    row_specs = [
        (
            "XIH3611_0_notation_guard",
            "xi_q versus Xi_i[A]",
            "lowercase xi_q is the q smoothing/correlation length; uppercase Xi_i[A] is a normalized finite-mode source-overlap charge",
            "xi_q != Xi_i[A]; xi_q sets lambda_q in the positive-Hessian branch, Xi_i[A] multiplies finite-mode source strength",
            "DERIVED_GUARDRAIL",
            "Prevents the source-composition factor from being falsely used as a range/source for q.",
            "xi_overlap_3304",
            False,
        ),
        (
            "XIH3611_1_ratio_theorem",
            "lambda_q=xi_q conditional ratio",
            "if M_q^2=n_q^A H_AB n_q^B and Z_q=xi_q^2 n_q^A H_AB n_q^B with the same normalization, then lambda_q=sqrt(Z_q/M_q^2)=xi_q",
            "M_q^2>0 and same n_q normalization in the kinetic and mass terms",
            "EXACT_CONDITIONAL_RATIO_RETAINED",
            "This is a real simplification: a physical q branch has one range owner, not independent Z_q and M_q knobs.",
            "zq_jq_3610",
            False,
        ),
        (
            "XIH3611_2_positive_Hessian_requirement",
            "H_AB positivity",
            "H_AB must be parent-owned and positive on the q-transverse quotient after gauge/representative modes are removed",
            "n_q^A H_AB n_q^B >= h_min ||n_q||^2 > 0 on the physical q slot",
            "OWNER_MISSING_NOT_CLAIMED",
            "Without this, xi_q does not define a stable local range and q could be tachyonic, gauge, or representative noise.",
            "positive_operator_3429",
            False,
        ),
        (
            "XIH3611_3_xi_q_owner_requirement",
            "xi_q owner",
            "xi_q must come from a parent smoothing/correlation length, quotient-cell scale, or Hessian gradient/mass normalization; it cannot be fitted after seeing R10/PPN",
            "Z_q = xi_q^2 M_q^2 after parent normalization",
            "SOURCE_MISSING_NOT_NUMERIC",
            "This is the current hard missing object for a claim-grade q residual calculation.",
            "hessian_hunt_2314",
            False,
        ),
        (
            "XIH3611_4_domain_boundary_requirement",
            "self-adjoint local operator",
            "L_q=-Z_q Delta_branch+M_q^2+B_q^bdry must have a fixed domain, boundary condition, and no unsilenced exterior flux",
            "<q,L_q q> >= lambda_gap ||q||^2 plus Phi_boundary=0",
            "DOMAIN_BOUNDARY_UNSIGNED",
            "This is what stops a formal positive Hessian from leaking through the worldtube or projector edge.",
            "positive_nohair_3092",
            False,
        ),
        (
            "XIH3611_5_local_silence_bridge",
            "Y_loc double-zero compatibility",
            "The xi_q/Hessian route is compatible with the older local-silence mechanism only if q is a physical Y_loc component, not a deleted representative coordinate",
            "operator couplings factor through Sigma_loc=G_AB Y^A Y^B and first variation vanishes at Y=0",
            "BRIDGE_IDENTIFIED_CONDITIONAL",
            "This connects the local-GR route to the double-zero mechanism without declaring them identical.",
            "yloc_euler_3535",
            False,
        ),
        (
            "XIH3611_6_current_verdict",
            "xi_q/H_AB claim status",
            "No parent-owned numeric xi_q, n_q, H_AB positivity certificate, self-adjoint domain, or boundary silence row exists yet",
            "owned_xi_q=false; owned_H_AB=false; local_q_range_claim=false",
            "FAIL_CURRENT_CLAIM_BUT_EXACT_CONTRACT_WRITTEN",
            "The derivation path is alive but not claim-grade; proceed by filling source/current bounds so local tests can still score the branch.",
            "handoff_3610",
            False,
        ),
    ]
    return [
        {
            "timestamp_utc": timestamp,
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "audit_id": audit_id,
            "target": target,
            "statement": statement,
            "mathematical_form": mathematical_form,
            "current_status": current_status,
            "effect_or_guard": effect_or_guard,
            "source_path": source_paths[source_id],
            "parent_signed": parent_signed,
            "claim_allowed": False,
            "valid_for_claim": False,
        }
        for (
            audit_id,
            target,
            statement,
            mathematical_form,
            current_status,
            effect_or_guard,
            source_id,
            parent_signed,
        ) in row_specs
    ]


def jq_matter_bound_rows(sources: dict[str, tuple[Path, str]]) -> list[dict[str, object]]:
    source_paths = {source_id: str(source_tuple[0]) for source_id, source_tuple in sources.items()}
    timestamp = utc_now()
    row_specs = [
        (
            "JQM3611_0_component_selected",
            "J_q^matter_bulk",
            "ordinary matter vertical source in the q equation",
            "J_q^matter_bulk[eta] := delta_eta S_matter|bulk projected onto the q slot",
            "FIRST_COMPONENT_SELECTED",
            "matter_pullback_3095",
            "This is the most dangerous local-GR coupling component because it feeds WEP, R10, PPN, clocks and Newtonian source calibration.",
        ),
        (
            "JQM3611_1_exact_chain_rule",
            "matter variation identity",
            "bulk matter q-source decomposes into observed-geometry, constants, matter-lift, source-weight and boundary/support terms",
            "delta_v S_A = 1/2 int sqrt(-g_obs) T_A^{mu nu} L_v g_obs_munu + sum_a int J_theta,A^a L_v theta_A^a + E_A delta_v Psi_A + B_A[v]",
            "EXACT_CHAIN_RULE_IMPORTED",
            "matter_source_functor_3235",
            "This is not a vibe: it is the local algebraic decomposition of the coupling problem.",
        ),
        (
            "JQM3611_2_zero_theorem",
            "matter descent zero",
            "J_q^matter_bulk=0 follows only if observed geometry, constants, matter lift, source-current weights and boundary/support all descend through q-blind data",
            "D_{v_q}e_obs=0; D_{v_q}theta_a=0; delta_{v_q}Psi_A pure gauge/on-shell; D_{v_q}kappa_A=0; B_A[v_q]=0",
            "EXACT_IF_PARENT_SIGNED_NOT_ACTIVE",
            "jq_zero_2431",
            "This is the clean route, but it is not signed, so the branch must keep a finite absolute bound.",
        ),
        (
            "JQM3611_3_no_cancellation_bound",
            "J_q^matter_bulk absolute bound",
            "the first J_q component is now bounded by named subcomponents instead of an unnamed missing coupling",
            "||J_q^matter_bulk||_* <= C_e||D_{v_q}e_obs|| + sum_a C_theta,a||D_{v_q}theta_a|| + C_Psi||delta_{v_q}Psi||_nongauge + C_B||B_A[v_q]|| + C_kappa max_A|D_{v_q}ln kappa_A| + C_NH||J_NH||",
            "BOUND_LAW_FILLED_VALUES_MISSING",
            "matter_bound_3235",
            "This is the requested forward movement: one leading component has a source-backed bound law, even though the numerical inputs are still missing.",
        ),
        (
            "JQM3611_4_source_only_slot_reduction",
            "species/source-only weights",
            "source-only matter coefficients are conditionally excluded by a typed matter constructor, connected density line, and no-Hom theorem",
            "parent domain + connected density line + no-Hom => delta_w_species=0, beta_source_alpha=0, z_g source-spurion part=0",
            "THEOREM_STACK_READY_NOT_PARENT_SIGNED",
            "no_source_only_3509",
            "This converts part of the coupling worry into three crisp parent signatures rather than a free parameter.",
        ),
        (
            "JQM3611_5_subcomponent_map",
            "J_q^matter_bulk subcomponents",
            "the matter bulk component splits into geometry, constants, marker, source-weight, boundary/support, readout/non-Hilbert and matter-lift rows",
            "J_matter_bound = J_geom + J_constants + J_marker + J_source_weight + J_boundary + J_readout_nonH + J_matter_lift",
            "SUBCOMPONENT_MAP_IMPORTED",
            "matter_bound_3235",
            "3612 should attack these rows one by one rather than returning to a generic coupling complaint.",
        ),
        (
            "JQM3611_6_current_verdict",
            "first J_q component status",
            "J_q^matter_bulk is not zero and not numeric, but it now has a precise no-cancellation bound law with source paths and named missing inputs",
            "valid_for_claim=false until every subcomponent is theorem-zero or source-backed numeric in common units",
            "SUCCESS_GATE_FILLED_NONCLAIM_BOUND",
            "jq_components_2431",
            "This satisfies the 3611 fallback gate without making a false local-GR/R10/PPN claim.",
        ),
    ]
    return [
        {
            "timestamp_utc": timestamp,
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "bound_id": bound_id,
            "quantity": quantity,
            "definition": definition,
            "formula": formula,
            "status": status,
            "source_path": source_paths[source_id],
            "effect_or_guard": effect_or_guard,
            "numeric_value_owned": False,
            "parent_zero_signed": False,
            "claim_allowed": False,
            "valid_for_claim": False,
        }
        for bound_id, quantity, definition, formula, status, source_id, effect_or_guard in row_specs
    ]


def decision_gate_rows(sources: dict[str, tuple[Path, str]]) -> list[dict[str, object]]:
    source_paths = {source_id: str(source_tuple[0]) for source_id, source_tuple in sources.items()}
    timestamp = utc_now()
    row_specs = [
        (
            "DEC3611_0_xi_q",
            "xi_q/H_AB route",
            "NOT_CLOSED",
            "The lambda_q=xi_q ratio is exact conditional math, but xi_q, H_AB positivity, q normal, domain and boundary are still not parent-owned.",
            "hessian_hunt_2314",
        ),
        (
            "DEC3611_1_jq_matter",
            "J_q^matter_bulk fallback",
            "ADVANCED",
            "The first leading J_q component now has a source-backed chain-rule/no-cancellation bound law.",
            "matter_bound_3235",
        ),
        (
            "DEC3611_2_claim_guard",
            "local-GR/R10/PPN claim",
            "BLOCKED",
            "No claim is allowed from this checkpoint because the xi/Hessian route is unsigned and the J_q matter bound has no numeric/theorem-zero subcomponent closures.",
            "zq_jq_3610",
        ),
        (
            "DEC3611_3_next",
            "next best attack",
            "SELECT_JQ_MATTER_SUBCOMPONENT_OR_XI_SOURCE_INPUT",
            "Attack the matter constants/source-weight/EM-binding subcomponents first, while keeping xi_q/H_AB as a parallel parent-signature target.",
            "matter_source_functor_3235",
        ),
    ]
    return [
        {
            "timestamp_utc": timestamp,
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "decision_id": decision_id,
            "target": target,
            "decision": decision,
            "rationale": rationale,
            "source_path": source_paths[source_id],
            "claim_allowed": False,
            "valid_for_claim": False,
        }
        for decision_id, target, decision, rationale, source_id in row_specs
    ]


def status_rows() -> list[dict[str, object]]:
    return [
        {
            "timestamp_utc": utc_now(),
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "status": "XI_Q_NOT_OWNED_JQ_MATTER_BULK_BOUND_LAW_FILLED",
            "summary": (
                "3611 separates xi_q from Xi_i[A], preserves the exact conditional lambda_q=xi_q ratio, "
                "rejects a current xi_q/H_AB claim, and fills the first J_q component bound for ordinary matter "
                "as an absolute no-cancellation chain-rule envelope."
            ),
            "claim_allowed": False,
            "valid_for_claim": False,
        }
    ]


def next_target_rows() -> list[dict[str, object]]:
    return [
        {
            "timestamp_utc": utc_now(),
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "next_id": "NEXT3611_0",
            "target_doc": "3612-Y5-R2FR-Jq-matter-subcomponent-zero-or-xi-q-source-input.md",
            "target_script": "scripts/Y5_R2FR_3612_Jq_matter_subcomponent_zero_or_xi_q_source_input.py",
            "objective": (
                "try to theorem-zero or source-bound the J_q^matter_bulk subcomponents "
                "(constants, source weights, EM/binding/Poynting, and boundary/support); in parallel, search for a parent-owned xi_q/H_AB source row"
            ),
            "success_gate": (
                "must close at least one named J_q^matter_bulk subcomponent as theorem-zero or numeric/source-backed nonclaim, "
                "or produce an owned xi_q/H_AB parent-signature row"
            ),
            "reason": "3611 converted the coupling bottleneck into named subcomponent rows; 3612 should take one of those rows off the board.",
            "claim_allowed": False,
            "valid_for_claim": False,
        }
    ]


def csv_parse_summary(outputs: dict[str, Path]) -> str:
    summaries: list[str] = []
    for output_name, output_path in outputs.items():
        if output_name == "validation":
            continue
        rows = read_csv(output_path)
        summaries.append(f"{output_name}:{len(rows)}")
    return "; ".join(summaries)


def formalization_leaks() -> list[Path]:
    if not FORMALIZATION.exists():
        return []
    leaks: list[Path] = []
    for candidate in FORMALIZATION.rglob("*3611*"):
        parts = set(candidate.parts)
        if "__pycache__" in parts or ".venv" in parts or "package" in parts:
            continue
        leaks.append(candidate)
    return leaks


def validation_rows(sources: dict[str, tuple[Path, str]], outputs: dict[str, Path]) -> list[dict[str, object]]:
    source_register = read_csv(outputs["source_register"])
    xi_rows = read_csv(outputs["xi_q_audit"])
    jq_rows = read_csv(outputs["jq_matter_bound"])
    decision_rows = read_csv(outputs["decision_gates"])
    status = read_csv(outputs["status"])
    existing_outputs = all(path.exists() for output_name, path in outputs.items() if output_name != "validation")
    parsed_summary = csv_parse_summary(outputs)
    no_claim_flags = True
    for output_name, output_path in outputs.items():
        if output_name == "validation":
            continue
        for row in read_csv(output_path):
            if row.get("valid_for_claim", "False").lower() == "true" or row.get("claim_allowed", "False").lower() == "true":
                no_claim_flags = False
    source_paths_all_exist = all(row["exists"].lower() == "true" for row in source_register)
    source_needles_found = all(row["needle_found"].lower() == "true" for row in source_register)
    notation_guard = any("xi_q != Xi_i[A]" in row["mathematical_form"] for row in xi_rows)
    xi_not_claimed = any(row["audit_id"] == "XIH3611_6_current_verdict" and row["current_status"].startswith("FAIL_CURRENT_CLAIM") for row in xi_rows)
    jq_bound_filled = any(row["bound_id"] == "JQM3611_3_no_cancellation_bound" and "<=" in row["formula"] for row in jq_rows)
    next_selected = any(row["decision_id"] == "DEC3611_3_next" and "SELECT_JQ_MATTER" in row["decision"] for row in decision_rows)
    status_ok = bool(status) and status[0]["status"] == "XI_Q_NOT_OWNED_JQ_MATTER_BULK_BOUND_LAW_FILLED"
    leaks = formalization_leaks()
    validation_specs = [
        ("VAL3611_0_sources_exist", source_paths_all_exist, "all required 3611 source paths exist"),
        ("VAL3611_1_needles_found", source_needles_found, "all selected 3611 source anchors found"),
        ("VAL3611_2_outputs_exist", existing_outputs, "all pre-validation 3611 csv outputs written"),
        ("VAL3611_3_csv_parse", True, parsed_summary),
        ("VAL3611_4_xi_not_Xi_guard", notation_guard, "lowercase xi_q range and uppercase Xi_i[A] source-overlap kept separate"),
        ("VAL3611_5_xi_claim_not_falsely_signed", xi_not_claimed, "xi_q/H_AB branch remains nonclaim"),
        ("VAL3611_6_jq_matter_bound_filled", jq_bound_filled, "first J_q component has an explicit absolute bound law"),
        ("VAL3611_7_no_claim_flags", no_claim_flags, "all generated physics rows remain nonclaim"),
        ("VAL3611_8_next_target_selected", next_selected, "3612 target selected from the new componentized bottleneck"),
        ("VAL3611_9_status_ok", status_ok, "canonical status matches 3611 verdict"),
        (
            "VAL3611_10_formalization_workbench_untouched",
            len(leaks) == 0,
            "no 3611 checkpoint output appears in formalization-workbench outside package/venv noise",
        ),
    ]
    return [
        {
            "timestamp_utc": utc_now(),
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "validation_id": validation_id,
            "result": "PASS" if passed else "FAIL",
            "detail": detail if passed else f"{detail}; leaks={[str(leak) for leak in leaks]}",
        }
        for validation_id, passed, detail in validation_specs
    ]


def write_doc(outputs: dict[str, Path]) -> None:
    xi_rows = read_csv(outputs["xi_q_audit"])
    jq_rows = read_csv(outputs["jq_matter_bound"])
    decision_rows = read_csv(outputs["decision_gates"])
    status = read_csv(outputs["status"])[0]
    next_target = read_csv(outputs["next_target"])[0]
    validation = read_csv(outputs["validation"])
    lines: list[str] = [
        "# 3611 - xi_q positive-Hessian source or Jq first-component bound",
        "",
        "## Verdict",
        "3611 does not close the `xi_q/H_AB` route.  The exact conditional simplification remains valuable:",
        "",
        "`M_q^2 = n_q^A H_AB n_q^B`, `Z_q = xi_q^2 n_q^A H_AB n_q^B`, therefore `lambda_q = xi_q`.",
        "",
        "But `xi_q`, `H_AB`, the q-normal, domain, and boundary/no-flux data are not parent-owned yet.  So no local-GR, R10, PPN, clock, or orbital claim is allowed from this branch.",
        "",
        "The forward movement is the fallback: the first dangerous `J_q` component is now filled as an ordinary-matter chain-rule bound, not a generic missing coupling.",
        "",
        "Important notation guard: lowercase `xi_q` is the q range/correlation length.  Uppercase `Xi_i[A]` is a finite-mode body/source-overlap factor.  They are not interchangeable.",
        "",
        "## xi_q / Positive Hessian Audit",
    ]
    for row in xi_rows:
        lines.append(f"- `{row['audit_id']}` / `{row['target']}`: {row['current_status']} - {row['statement']}")
    lines.extend(["", "## J_q Matter-Bulk Bound"])
    for row in jq_rows:
        lines.append(f"- `{row['bound_id']}` / `{row['quantity']}`: {row['status']} - `{row['formula']}`")
    lines.extend(["", "## Decision Gates"])
    for row in decision_rows:
        lines.append(f"- `{row['decision_id']}` / `{row['target']}`: {row['decision']} - {row['rationale']}")
    lines.extend(
        [
            "",
            "## Status",
            f"- `{status['status']}`: {status['summary']}",
            "",
            "## Validation",
        ]
    )
    for row in validation:
        lines.append(f"- `{row['validation_id']}`: {row['result']} ({row['detail']})")
    lines.extend(
        [
            "",
            "## Next Target",
            f"- `{next_target['next_id']}` -> `{next_target['target_doc']}`",
            f"- Objective: {next_target['objective']}",
            f"- Success gate: {next_target['success_gate']}",
            f"- Reason: {next_target['reason']}",
            "",
        ]
    )
    DOC.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    sources = source_map()
    outputs = output_paths()
    write_csv(outputs["source_register"], source_register_rows(sources))
    write_csv(outputs["xi_q_audit"], xi_q_audit_rows(sources))
    write_csv(outputs["jq_matter_bound"], jq_matter_bound_rows(sources))
    write_csv(outputs["decision_gates"], decision_gate_rows(sources))
    write_csv(outputs["status"], status_rows())
    write_csv(outputs["next_target"], next_target_rows())
    write_csv(outputs["canonical_status"], status_rows())
    write_csv(outputs["validation"], validation_rows(sources, outputs))
    write_doc(outputs)
    print(f"wrote {DOC}")
    print(f"wrote {outputs['validation']}")


if __name__ == "__main__":
    main()

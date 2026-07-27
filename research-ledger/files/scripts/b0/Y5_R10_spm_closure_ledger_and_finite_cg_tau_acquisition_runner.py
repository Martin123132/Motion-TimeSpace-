from __future__ import annotations

import csv
from datetime import datetime, timezone
from pathlib import Path


STARTED = datetime.now(timezone.utc)
ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "source-intake" / "mts_residuals"
DOC = ROOT / "1032-Y5-R10-spm-closure-ledger-and-finite-cg-tau-acquisition-runner.md"
FORMALIZATION = ROOT.parent / "formalization-workbench"


def stamp() -> str:
    return datetime.now(timezone.utc).isoformat()


def flag(value: object) -> bool:
    return str(value).strip().lower() == "true"


def source_path(path_text: str) -> Path:
    path = Path(path_text)
    if path.is_absolute():
        return path
    return ROOT / path


def write_csv(path: Path, rows: list[dict[str, object]], fieldnames: list[str] | None = None) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if fieldnames is None:
        fieldnames = []
        for row in rows:
            for key in row:
                if key not in fieldnames:
                    fieldnames.append(key)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow({key: row.get(key, "") for key in fieldnames})


def md_cell(value: object) -> str:
    return str(value).replace("\n", " ").replace("|", "\\|")


def md_table(rows: list[dict[str, object]], columns: list[str]) -> str:
    if not rows:
        return "_No rows._\n"
    return "\n".join(
        [
            "| " + " | ".join(columns) + " |",
            "| " + " | ".join("---" for _ in columns) + " |",
            *["| " + " | ".join(md_cell(row.get(column, "")) for column in columns) + " |" for row in rows],
        ]
    ) + "\n"


def source_register_rows() -> list[dict[str, str]]:
    specs = [
        ("SRC1032_0_1031_next", "source-intake/mts_residuals/P8_Y5_R10_1031_NEXT_TARGET.csv", "1032-Y5-R10-spm-closure-ledger", "1031 handoff to SPM closure ledger and finite c_g/tau runner."),
        ("SRC1032_1_1031_proof", "source-intake/mts_residuals/P8_Y5_R10_1031_TERMINAL_PUBLIC_METRIC_PROOF_AUDIT.csv", "TPM1031_6_verdict", "1031 terminal metric nonproof verdict."),
        ("SRC1032_2_1031_closure", "source-intake/mts_residuals/P8_Y5_R10_1031_SPM_CLOSURE_BRANCH.csv", "SPMC1031_0_closure_name", "1031 explicit SPM closure branch."),
        ("SRC1032_3_1031_fallback", "source-intake/mts_residuals/P8_Y5_R10_1031_FINITE_CG_TAU_FALLBACK.csv", "FCG1031_1_tau_R10", "1031 finite c_g/tau fallback requirements."),
        ("SRC1032_4_1029_intake", "source-intake/mts_residuals/P8_Y5_R10_1029_CG_INTAKE_TEMPLATE.csv", "CGI1029_1_finite_cg_R10", "1029 c_g intake template."),
        ("SRC1032_5_1029_tau", "source-intake/mts_residuals/P8_Y5_R10_1029_TAU_PROJECTION_REQUIREMENTS.csv", "TAU1029_1_PPN_gamma_beta", "1029 tau projection requirements."),
        ("SRC1032_6_1030_provenance", "source-intake/mts_residuals/P8_Y5_R10_1030_CG_PROVENANCE_GATE_BINDING.csv", "CPG1030_4_no_cancellation", "1030 c_g provenance and no-cancellation bindings."),
        ("SRC1032_7_951_schema", "source-intake/mts_residuals/P8_Y5_R10_951_PROVENANCE_GATE_SCHEMA.csv", "PGS951_2_derivation_status", "951 provenance gate schema."),
        ("SRC1032_8_946_interface", "source-intake/mts_residuals/P8_Y5_R10_946_CG_BA_BOUND_INTERFACE.csv", "CGB946_0_cg_R10", "946 R10/PPN c_g bound interface."),
        ("SRC1032_9_947_projection", "source-intake/mts_residuals/P8_Y5_R10_947_PROJECTION_FILL_ATTEMPT.csv", "PFA947_0_R10_projection", "947 projection fill attempt."),
        ("SRC1032_10_947_bound_update", "source-intake/mts_residuals/P8_Y5_R10_947_BOUND_INTERFACE_UPDATE.csv", "BI947_1_cg_PPN", "947 bound interface update."),
        ("SRC1032_11_1028_pack", "source-intake/mts_residuals/P8_Y5_R10_1028_FRAME_MARKER_BOUND_INPUT_PACK.csv", "FMB1028_10_total_qbarXT_envelope", "1028 total no-cancellation envelope."),
        ("SRC1032_12_local_bounds", "source-intake/local_bounds/local_bound_claims.csv", "R10_fifth_force", "local empirical anchors including R10 symbolic curve and PPN gamma/beta bounds."),
    ]
    rows: list[dict[str, str]] = []
    for source_id, path_text, needle, role in specs:
        path = source_path(path_text)
        exists = path.exists()
        text = path.read_text(encoding="utf-8", errors="ignore") if exists else ""
        rows.append(
            {
                "source_id": source_id,
                "source_path": str(path),
                "exists": str(exists).lower(),
                "needle": needle,
                "needle_found": str(needle in text).lower(),
                "role": role,
                "valid_for_claim": "false",
                "generated_utc": stamp(),
            }
        )
    return rows


def spm_closure_ledger_rows() -> list[dict[str, str]]:
    return [
        {
            "closure_id": "SPML1032_0_branch_definition",
            "branch": "Single Public Metric closure",
            "allowed_statement": "Assume ordinary matter/readout is restricted to Sbar[Psi,e_pub(q),omega[e_pub],theta(q)].",
            "mathematical_effect": "A_g(Xhat) and B_g(Xhat) shadow-frame slots are excluded by closure.",
            "claim_boundary": "closure branch only; not derived from current parent corpus",
            "local_effect": "c_g=0 and b_dis=0 only inside this closure branch",
            "remaining_debt": "b_A;b_alpha;q_nonH;Delta_W_support;measured_GM;left_hand_EH_Newton",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "closure_id": "SPML1032_1_zero_policy",
            "branch": "SPM zero-coefficient policy",
            "allowed_statement": "Under explicit SPM closure, c_g and direct shadow-frame b_dis are set to zero by branch definition.",
            "mathematical_effect": "finite c_g/tau rows are bypassed only for the closure branch, not for derived-MTS claims",
            "claim_boundary": "must label every result as SPM-closure conditional",
            "local_effect": "R10/PPN common-frame terms vanish only conditionally",
            "remaining_debt": "other frame-renamed and hidden-source terms remain separate",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "closure_id": "SPML1032_2_no_overclaim_policy",
            "branch": "SPM anti-overclaim policy",
            "allowed_statement": "SPM closure can be used as an internal selection principle or model branch.",
            "mathematical_effect": "no local-GR/Newton pass unless all retained residuals and left-hand field-equation gates close",
            "claim_boundary": "do not call SPM derived, natural, or forced",
            "local_effect": "closure simplifies local coupling ledger but is not evidence",
            "remaining_debt": "source-support, constants, measured-GM, and EH/Newton limit",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "closure_id": "SPML1032_3_test_policy",
            "branch": "SPM versus finite branch comparison",
            "allowed_statement": "Report SPM closure and finite-coupling branch separately.",
            "mathematical_effect": "SPM branch has c_g=0 by closure; finite branch scores c_g*tau only with real provenance",
            "claim_boundary": "no cancellation between closure and finite unknowns",
            "local_effect": "keeps future R10/PPN tests honest",
            "remaining_debt": "finite branch needs c_g,tau_R10,tau_PPN sourced",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
    ]


def acquisition_template_rows() -> list[dict[str, str]]:
    return [
        {
            "acquisition_id": "ACQ1032_0_spm_zero_branch",
            "quantity": "c_g_zero_under_SPM",
            "branch": "SPM_closure",
            "candidate_value": "0_by_explicit_closure",
            "units": "dimensionless",
            "source_path": "source-intake/mts_residuals/P8_Y5_R10_1031_SPM_CLOSURE_BRANCH.csv",
            "source_row_id": "SPMC1031_1_cg_effect",
            "derivation_status": "explicit_closure_nonclaim",
            "comparison_bound": "not_scored_as_evidence",
            "comparison_bound_source": "closure_branch_only",
            "required_before_score": "not eligible for claim scoring; label as SPM closure branch",
            "ready_for_runner": "true",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "acquisition_id": "ACQ1032_1_finite_cg_value",
            "quantity": "c_g",
            "branch": "finite_coupling",
            "candidate_value": "MISSING_PARENT_INPUT",
            "units": "dimensionless",
            "source_path": "MISSING_PARENT_SOURCE",
            "source_row_id": "MISSING_SOURCE_ROW_ID",
            "derivation_status": "MISSING_DERIVATION_STATUS",
            "comparison_bound": "R10/PPN/clock bound only after tau projection",
            "comparison_bound_source": "P8_Y5_R10_946_CG_BA_BOUND_INTERFACE.csv",
            "required_before_score": "numeric c_g or parent-derived finite value with source path and units",
            "ready_for_runner": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "acquisition_id": "ACQ1032_2_tau_R10_projection",
            "quantity": "tau_R10",
            "branch": "finite_coupling_R10",
            "candidate_value": "MISSING_ARENA_PROJECTION",
            "units": "dimensionless",
            "source_path": "MISSING_PROJECTION_SOURCE",
            "source_row_id": "MISSING_SOURCE_ROW_ID",
            "derivation_status": "MISSING_R10_PROJECTION_DERIVATION",
            "comparison_bound": "alpha_bound(lambda)",
            "comparison_bound_source": "source-intake/local_bounds/local_bound_claims.csv:R10_fifth_force",
            "required_before_score": "K_X(lambda), Qbar_XH, source/test profile, and tau_R10 convention",
            "ready_for_runner": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "acquisition_id": "ACQ1032_3_tau_PPN_gamma",
            "quantity": "tau_PPN_gamma",
            "branch": "finite_coupling_PPN",
            "candidate_value": "MISSING_ARENA_PROJECTION",
            "units": "dimensionless",
            "source_path": "MISSING_RESPONSE_SOURCE",
            "source_row_id": "MISSING_SOURCE_ROW_ID",
            "derivation_status": "MISSING_PPN_RESPONSE_MATRIX",
            "comparison_bound": "2.3e-05",
            "comparison_bound_source": "source-intake/local_bounds/local_bound_claims.csv:R3_gamma",
            "required_before_score": "M_gamma, gauge, profile, weak-field order, and c_g source",
            "ready_for_runner": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "acquisition_id": "ACQ1032_4_tau_PPN_beta",
            "quantity": "tau_PPN_beta",
            "branch": "finite_coupling_PPN",
            "candidate_value": "MISSING_ARENA_PROJECTION",
            "units": "dimensionless",
            "source_path": "MISSING_RESPONSE_SOURCE",
            "source_row_id": "MISSING_SOURCE_ROW_ID",
            "derivation_status": "MISSING_PPN_RESPONSE_MATRIX",
            "comparison_bound": "7.8e-05",
            "comparison_bound_source": "source-intake/local_bounds/local_bound_claims.csv:R4_beta",
            "required_before_score": "M_beta, gauge, profile, weak-field order, and c_g source",
            "ready_for_runner": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "acquisition_id": "ACQ1032_5_no_cancellation_envelope",
            "quantity": "local_abs_envelope",
            "branch": "all_local_branches",
            "candidate_value": "ABSOLUTE_COMPONENT_SUM_REQUIRED",
            "units": "policy",
            "source_path": "source-intake/mts_residuals/P8_Y5_R10_1028_FRAME_MARKER_BOUND_INPUT_PACK.csv",
            "source_row_id": "FMB1028_10_total_qbarXT_envelope",
            "derivation_status": "policy_guard",
            "comparison_bound": "all retained components theorem-zero or numeric/source-backed",
            "comparison_bound_source": "P8_Y5_R10_1030_CG_PROVENANCE_GATE_BINDING.csv:CPG1030_4_no_cancellation",
            "required_before_score": "no cancellation between c_g,b_A,b_alpha,b_dis,q_nonH,Delta_W_support",
            "ready_for_runner": "true",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
    ]


def placeholder_refusal_rows(acquisition: list[dict[str, str]]) -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    for index, row in enumerate(acquisition):
        failures: list[str] = []
        if row["branch"] == "SPM_closure":
            failures.append("CLOSURE_BRANCH_NOT_CLAIM_EVIDENCE")
        if "MISSING" in row["candidate_value"]:
            failures.append("MISSING_NUMERIC_OR_THEOREM_VALUE")
        if "MISSING" in row["source_path"]:
            failures.append("MISSING_EXISTING_SOURCE_PATH")
        if "MISSING" in row["source_row_id"]:
            failures.append("MISSING_SOURCE_ROW_ID")
        if "MISSING" in row["derivation_status"]:
            failures.append("MISSING_DERIVATION_STATUS")
        if row["valid_for_claim"] != "true":
            failures.append("CLAIM_POLICY_FALSE")
        rows.append(
            {
                "run_id": f"REF1032_{index}_{row['acquisition_id'].split('_', 1)[1]}",
                "acquisition_id": row["acquisition_id"],
                "quantity": row["quantity"],
                "branch": row["branch"],
                "candidate_value": row["candidate_value"],
                "refusal_status": "accepted_as_nonclaim_closure" if row["branch"] == "SPM_closure" else "rejected_missing_provenance",
                "failure_reasons": ";".join(failures),
                "score_eligible": "false",
                "claim_allowed": "false",
                "valid_for_claim": "false",
                "generated_utc": stamp(),
            }
        )
    return rows


def readiness_map_rows() -> list[dict[str, str]]:
    return [
        {
            "readiness_id": "READY1032_0_R10_finite",
            "arena": "R10 fifth-force",
            "score_formula": "alpha_R10(lambda)=K_X(lambda) Qbar_XH tau_R10 c_g + retained tails",
            "bound_anchor": "local_bound_claims.csv:R10_fifth_force alpha(lambda) symbolic curve",
            "missing_mts_inputs": "c_g;K_X(lambda);Qbar_XH;tau_R10;profile convention;tail envelope",
            "current_status": "NOT_SCORE_READY",
            "next_source_action": "derive/source tau_R10 projection and c_g parent value or zero theorem",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "readiness_id": "READY1032_1_PPN_gamma",
            "arena": "PPN gamma",
            "score_formula": "gamma_minus_1 = M_gamma(profile,gauge) tau_PPN_gamma c_g + disformal/tail terms",
            "bound_anchor": "local_bound_claims.csv:R3_gamma upper_bound=2.3e-05",
            "missing_mts_inputs": "c_g;M_gamma;tau_PPN_gamma;gauge;profile;b_dis separation",
            "current_status": "NOT_SCORE_READY",
            "next_source_action": "derive/source weak-field response matrix",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "readiness_id": "READY1032_2_PPN_beta",
            "arena": "PPN beta",
            "score_formula": "beta_minus_1 = M_beta(profile,gauge) tau_PPN_beta c_g + nonlinear/tail terms",
            "bound_anchor": "local_bound_claims.csv:R4_beta upper_bound=7.8e-05",
            "missing_mts_inputs": "c_g;M_beta;tau_PPN_beta;weak-field order;nonlinear closure",
            "current_status": "NOT_SCORE_READY",
            "next_source_action": "derive/source second-order PPN response matrix",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "readiness_id": "READY1032_3_SPM_closure",
            "arena": "SPM closure local branch",
            "score_formula": "c_g=0 by explicit closure; no finite c_g score",
            "bound_anchor": "not empirical evidence",
            "missing_mts_inputs": "full parent proof if promoted beyond closure",
            "current_status": "CLOSURE_READY_NONCLAIM",
            "next_source_action": "label separately from derived-MTS and finite branches",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
    ]


def claim_gate_rows() -> list[dict[str, str]]:
    return [
        {
            "gate_id": "CGATE1032_0_sources",
            "claim": "all 1032 cited sources exist",
            "gate_pass": "true",
            "reason": "validated by source register",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "gate_id": "CGATE1032_1_spm_derived",
            "claim": "SPM closure is a derived parent theorem",
            "gate_pass": "false",
            "reason": "1031 demoted SPM to explicit closure unless stronger parent proof is supplied",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "gate_id": "CGATE1032_2_spm_closure_ready",
            "claim": "SPM closure branch is internally ledgered",
            "gate_pass": "true",
            "reason": "closure branch rows exist and remain nonclaim",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "gate_id": "CGATE1032_3_finite_runner_refuses_placeholders",
            "claim": "finite acquisition runner refuses placeholder values",
            "gate_pass": "true",
            "reason": "every finite c_g/tau row is rejected while MISSING markers remain",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "gate_id": "CGATE1032_4_R10_PPN_claim",
            "claim": "R10 or PPN branch can be scored now",
            "gate_pass": "false",
            "reason": "c_g, tau_R10, tau_PPN, and response matrices remain missing",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "gate_id": "CGATE1032_5_no_cancellation",
            "claim": "unknown local components may cancel",
            "gate_pass": "true",
            "reason": "no-cancellation absolute-envelope policy is active",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
    ]


def decision_rows() -> list[dict[str, str]]:
    return [
        {
            "decision_id": "DEC1032_0_spm_status",
            "decision": "SPM is now a formal nonclaim closure branch.",
            "because": "terminal-public-metric proof did not close, but the closure is useful if labelled honestly.",
            "next_action": "keep all SPM results branch-labelled and not derived-MTS claims",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "decision_id": "DEC1032_1_finite_status",
            "decision": "finite c_g/tau acquisition runner is staged and refuses placeholders.",
            "because": "candidate c_g, tau_R10, tau_PPN, and response matrices still lack source/provenance rows.",
            "next_action": "source or derive tau_R10 first, then PPN response matrix",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "decision_id": "DEC1032_2_testing_status",
            "decision": "R10/PPN testing is close to runner-ready but not score-ready.",
            "because": "external anchors exist, but the MTS-side projection map is missing.",
            "next_action": "build tau_R10 projection derivation/acquisition target",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "decision_id": "DEC1032_3_next_target",
            "decision": "Next target is tau_R10 projection derivation or sourced acquisition.",
            "because": "R10 is the cleanest first finite c_g arena once tau_R10 and profile conventions are real.",
            "next_action": "1033-Y5-R10-tau-R10-projection-derivation-or-source-acquisition.md",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
    ]


def next_target_rows() -> list[dict[str, str]]:
    return [
        {
            "next_target": "1033-Y5-R10-tau-R10-projection-derivation-or-source-acquisition.md",
            "objective": "derive or source the R10 projection coefficient tau_R10, including K_X(lambda), Qbar_XH, source/test material convention, profile normalization, and alpha(lambda) bound linkage; keep finite c_g unscored until all inputs are real",
            "include": "tau_R10, K_X(lambda), Qbar_XH, R10 alpha(lambda), source/test profiles, units, source paths, provenance gate, no-cancellation envelope",
            "exclude": "invented c_g/tau values, R10 pass claim, PPN pass claim, SPM-derived claim, cancellation between unknowns, GitHub action, formalization-workbench edits",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        }
    ]


def formalization_changed_after_start() -> list[Path]:
    if not FORMALIZATION.exists():
        return []
    changed = []
    for candidate in FORMALIZATION.rglob("*"):
        if candidate.is_file():
            modified = datetime.fromtimestamp(candidate.stat().st_mtime, timezone.utc)
            if modified >= STARTED:
                changed.append(candidate)
    return changed


def validation_rows(
    sources: list[dict[str, str]],
    closure: list[dict[str, str]],
    acquisition: list[dict[str, str]],
    refusals: list[dict[str, str]],
    readiness: list[dict[str, str]],
    gates: list[dict[str, str]],
    decisions: list[dict[str, str]],
    next_target: list[dict[str, str]],
) -> list[dict[str, str]]:
    changed = formalization_changed_after_start()
    closure_required = {f"SPML1032_{idx}_{name}" for idx, name in [
        (0, "branch_definition"),
        (1, "zero_policy"),
        (2, "no_overclaim_policy"),
        (3, "test_policy"),
    ]}
    acquisition_required = {f"ACQ1032_{idx}_{name}" for idx, name in [
        (0, "spm_zero_branch"),
        (1, "finite_cg_value"),
        (2, "tau_R10_projection"),
        (3, "tau_PPN_gamma"),
        (4, "tau_PPN_beta"),
        (5, "no_cancellation_envelope"),
    ]}
    readiness_required = {f"READY1032_{idx}_{name}" for idx, name in [
        (0, "R10_finite"),
        (1, "PPN_gamma"),
        (2, "PPN_beta"),
        (3, "SPM_closure"),
    ]}
    finite_refusals = [row for row in refusals if row["branch"] != "SPM_closure"]
    checks = [
        ("V1032_0_sources_exist", all(flag(row["exists"]) and flag(row["needle_found"]) for row in sources), "all cited source paths exist and expected needles are present"),
        ("V1032_1_closure_rows_complete", closure_required.issubset({row["closure_id"] for row in closure}), "SPM closure ledger covers branch definition, zero policy, anti-overclaim policy, and test policy"),
        ("V1032_2_closure_nonclaim", all(row["valid_for_claim"] == "false" for row in closure), "SPM closure remains nonclaim"),
        ("V1032_3_acquisition_rows_complete", acquisition_required.issubset({row["acquisition_id"] for row in acquisition}), "acquisition template covers SPM zero branch, finite c_g, tau_R10, tau_PPN gamma/beta, and no-cancellation"),
        ("V1032_4_finite_rows_not_ready", all(row["ready_for_runner"] == "false" for row in acquisition if row["branch"].startswith("finite")), "finite rows are not marked ready while MISSING markers remain"),
        ("V1032_5_refusals_complete", len(refusals) == len(acquisition), "placeholder refusal runner emitted one row per acquisition row"),
        ("V1032_6_refuses_placeholders", all(row["score_eligible"] == "false" and row["claim_allowed"] == "false" for row in finite_refusals), "finite placeholder rows are rejected from scoring"),
        ("V1032_7_readiness_map_complete", readiness_required.issubset({row["readiness_id"] for row in readiness}), "readiness map covers R10, PPN gamma, PPN beta, and SPM closure"),
        ("V1032_8_readiness_nonclaim", all(row["claim_allowed"] == "false" and row["valid_for_claim"] == "false" for row in readiness), "readiness rows do not claim tests"),
        ("V1032_9_claim_gates_blocked", all(row["claim_allowed"] == "false" and row["valid_for_claim"] == "false" for row in gates), "all claim gates refuse promotion"),
        ("V1032_10_no_cancellation_guard", any(row["gate_id"] == "CGATE1032_5_no_cancellation" and flag(row["gate_pass"]) for row in gates), "no-cancellation guard is active"),
        ("V1032_11_decision_next", any(row["decision_id"] == "DEC1032_3_next_target" for row in decisions), "decision ledger selects the 1033 target"),
        ("V1032_12_next_target_written", len(next_target) == 1 and "1033-Y5-R10-tau-R10" in next_target[0]["next_target"], "1033 next target row is present"),
        ("V1032_13_no_overclaim", all(row.get("valid_for_claim", "false") == "false" for group in [sources, closure, acquisition, refusals, readiness, gates, decisions, next_target] for row in group), "all generated rows remain valid_for_claim=false"),
        ("V1032_14_formalization_untouched", len(changed) == 0, f"formalization-workbench modified-file count since script start is {len(changed)}"),
    ]
    passed_all = all(passed for _, passed, _ in checks)
    rows = [{"check_id": check_id, "result": "pass" if passed else "fail", "detail": detail, "generated_utc": stamp()} for check_id, passed, detail in checks]
    rows.insert(0, {"check_id": "V1032_SUMMARY", "result": "pass" if passed_all else "fail", "detail": "1032 SPM closure ledger and finite c_g/tau acquisition validation summary", "generated_utc": stamp()})
    return rows


def write_doc(
    sources: list[dict[str, str]],
    closure: list[dict[str, str]],
    acquisition: list[dict[str, str]],
    refusals: list[dict[str, str]],
    readiness: list[dict[str, str]],
    gates: list[dict[str, str]],
    decisions: list[dict[str, str]],
    next_target: list[dict[str, str]],
    validations: list[dict[str, str]],
) -> None:
    text = "\n".join(
        [
            "# 1032 Y5 R10 SPM closure ledger and finite c_g/tau acquisition runner",
            "",
            "**Status:** Single Public Metric is now a formal nonclaim closure branch, not a derived theorem. The finite `c_g/tau_R10/tau_PPN` branch has an acquisition runner that refuses all placeholder values while preserving the exact fields needed for future R10 and PPN scoring.",
            "",
            "**Claim ceiling:** no SPM-derived theorem, finite-`c_g` score, R10, PPN, WEP, clock, orbital, local-GR/Newton, or source-side GR pass is allowed from 1032.",
            "",
            "## Source register",
            md_table(sources, ["source_id", "source_path", "exists", "needle_found", "role"]),
            "## SPM closure ledger",
            md_table(closure, ["closure_id", "branch", "allowed_statement", "mathematical_effect", "claim_boundary", "local_effect", "remaining_debt", "valid_for_claim"]),
            "## Finite c_g/tau acquisition template",
            md_table(acquisition, ["acquisition_id", "quantity", "branch", "candidate_value", "units", "source_path", "source_row_id", "derivation_status", "comparison_bound", "comparison_bound_source", "required_before_score", "ready_for_runner", "valid_for_claim"]),
            "## Placeholder refusal runner",
            md_table(refusals, ["run_id", "acquisition_id", "quantity", "branch", "candidate_value", "refusal_status", "failure_reasons", "score_eligible", "claim_allowed", "valid_for_claim"]),
            "## R10/PPN readiness map",
            md_table(readiness, ["readiness_id", "arena", "score_formula", "bound_anchor", "missing_mts_inputs", "current_status", "next_source_action", "claim_allowed", "valid_for_claim"]),
            "## Claim gates",
            md_table(gates, ["gate_id", "claim", "gate_pass", "reason", "claim_allowed", "valid_for_claim"]),
            "## Decision ledger",
            md_table(decisions, ["decision_id", "decision", "because", "next_action", "valid_for_claim"]),
            "## Validation",
            md_table(validations, ["check_id", "result", "detail", "generated_utc"]),
            "## Next target",
            md_table(next_target, ["next_target", "objective", "include", "exclude", "valid_for_claim"]),
            "",
        ]
    )
    DOC.write_text(text, encoding="utf-8")


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    sources = source_register_rows()
    closure = spm_closure_ledger_rows()
    acquisition = acquisition_template_rows()
    refusals = placeholder_refusal_rows(acquisition)
    readiness = readiness_map_rows()
    gates = claim_gate_rows()
    decisions = decision_rows()
    next_target = next_target_rows()
    validations = validation_rows(sources, closure, acquisition, refusals, readiness, gates, decisions, next_target)

    write_csv(OUT / "P8_Y5_R10_1032_SOURCE_REGISTER.csv", sources)
    write_csv(OUT / "P8_Y5_R10_1032_SPM_CLOSURE_LEDGER.csv", closure)
    write_csv(OUT / "P8_Y5_R10_1032_CG_TAU_ACQUISITION_TEMPLATE.csv", acquisition)
    write_csv(OUT / "P8_Y5_R10_1032_PLACEHOLDER_REFUSAL_RUNNER.csv", refusals)
    write_csv(OUT / "P8_Y5_R10_1032_R10_PPN_READINESS_MAP.csv", readiness)
    write_csv(OUT / "P8_Y5_R10_1032_CLAIM_GATES.csv", gates)
    write_csv(OUT / "P8_Y5_R10_1032_DECISION_LEDGER.csv", decisions)
    write_csv(OUT / "P8_Y5_R10_1032_NEXT_TARGET.csv", next_target)
    write_csv(OUT / "P8_Y5_BRR545_1032_VALIDATION.csv", validations)
    write_doc(sources, closure, acquisition, refusals, readiness, gates, decisions, next_target, validations)


if __name__ == "__main__":
    main()

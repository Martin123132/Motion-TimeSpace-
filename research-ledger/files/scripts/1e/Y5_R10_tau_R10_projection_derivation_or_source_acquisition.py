from __future__ import annotations

import csv
from datetime import datetime, timezone
from pathlib import Path


STARTED = datetime.now(timezone.utc)
ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "source-intake" / "mts_residuals"
LOCAL_BOUNDS = ROOT / "source-intake" / "local_bounds"
DOC = ROOT / "1033-Y5-R10-tau-R10-projection-derivation-or-source-acquisition.md"
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
        ("SRC1033_0_1032_next", "source-intake/mts_residuals/P8_Y5_R10_1032_NEXT_TARGET.csv", "1033-Y5-R10-tau-R10", "1032 handoff to tau_R10 projection."),
        ("SRC1033_1_1032_acquisition", "source-intake/mts_residuals/P8_Y5_R10_1032_CG_TAU_ACQUISITION_TEMPLATE.csv", "ACQ1032_2_tau_R10_projection", "1032 tau_R10 acquisition slot."),
        ("SRC1033_2_1032_readiness", "source-intake/mts_residuals/P8_Y5_R10_1032_R10_PPN_READINESS_MAP.csv", "READY1032_0_R10_finite", "1032 R10 readiness map."),
        ("SRC1033_3_1032_refusal", "source-intake/mts_residuals/P8_Y5_R10_1032_PLACEHOLDER_REFUSAL_RUNNER.csv", "REF1032_2_2_tau_R10_projection", "1032 placeholder refusal evidence."),
        ("SRC1033_4_1029_tau", "source-intake/mts_residuals/P8_Y5_R10_1029_TAU_PROJECTION_REQUIREMENTS.csv", "TAU1029_0_R10", "1029 tau projection requirements."),
        ("SRC1033_5_1030_provenance", "source-intake/mts_residuals/P8_Y5_R10_1030_CG_PROVENANCE_GATE_BINDING.csv", "CPG1030_2_tau_R10", "1030 c_g/tau provenance binding."),
        ("SRC1033_6_946_interface", "source-intake/mts_residuals/P8_Y5_R10_946_CG_BA_BOUND_INTERFACE.csv", "CGB946_0_cg_R10", "946 R10 c_g bound interface."),
        ("SRC1033_7_947_projection", "source-intake/mts_residuals/P8_Y5_R10_947_PROJECTION_FILL_ATTEMPT.csv", "PFA947_0_R10_projection", "947 R10 projection missing row."),
        ("SRC1033_8_947_update", "source-intake/mts_residuals/P8_Y5_R10_947_BOUND_INTERFACE_UPDATE.csv", "BI947_0_cg_R10", "947 R10 bound interface update."),
        ("SRC1033_9_631_charge_law", "source-intake/mts_residuals/P8_Y5_R10_631_SOURCE_TEST_CHARGE_LAW.csv", "Q631_0_universal_weyl_charge", "631 source/test charge law."),
        ("SRC1033_10_633_frame", "source-intake/mts_residuals/P8_Y5_R10_633_MATTER_FRAME_CANDIDATE_CLASSIFICATION.csv", "MFC633_7_631_variation", "633 matter-frame candidate classification."),
        ("SRC1033_11_mts_curve", "source-intake/mts_residuals/R10_alpha_lambda_curve_MTS_source_normalization.csv", "MISSING_SOURCE_NORMALIZED_ALPHA_PREDICTION", "current MTS R10 prediction placeholder."),
        ("SRC1033_12_bound_curve", "source-intake/local_bounds/R10_alpha_lambda_bound_curve_DIGITIZED.csv", "R10_BOUND_PLACEHOLDER_0", "current R10 bound curve placeholder."),
        ("SRC1033_13_local_bounds", "source-intake/local_bounds/local_bound_claims.csv", "R10_fifth_force", "local R10 symbolic bound anchor."),
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


def derivation_audit_rows() -> list[dict[str, str]]:
    return [
        {
            "audit_id": "TAUR1033_0_R10_observable",
            "target": "map MTS finite X response to the R10 Yukawa alpha(lambda) convention",
            "mathematical_form": "V(r)=-G m_s m_t/r [1 + alpha(lambda) exp(-r/lambda)]",
            "result": "OBSERVABLE_CONVENTION_IDENTIFIED",
            "missing_for_claim": "digitized/source-backed alpha_bound(lambda) curve",
            "if_missing": "no R10 scoring, only schema work",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "audit_id": "TAUR1033_1_factorization",
            "target": "factor finite MTS prediction into source, test, Green-kernel, and projection factors",
            "mathematical_form": "alpha_R10(lambda)=K_X(lambda) Qbar_XH(source,lambda) [tau_R10(test,lambda)c_g + retained tails]",
            "result": "PROJECTION_CONTRACT_WRITTEN",
            "missing_for_claim": "K_X(lambda), Qbar_XH, tau_R10, c_g, source/test profile, tail envelope",
            "if_missing": "finite branch remains unscoreable",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "audit_id": "TAUR1033_2_tau_definition",
            "target": "define tau_R10 without inventing a value",
            "mathematical_form": "tau_R10 := normalized test-leg/material/readout projection that converts c_g into the R10 test charge under the selected Yukawa profile convention",
            "result": "DEFINITION_ONLY",
            "missing_for_claim": "material/readout trace convention, Xhat normalization, finite-source correction, and profile integral",
            "if_missing": "tau_R10 cannot be assumed unity",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "audit_id": "TAUR1033_3_KX_definition",
            "target": "separate the propagator/normalization factor from material projection",
            "mathematical_form": "K_X(lambda) contains static Green-function normalization, X kinetic normalization, 4pi/G conversion, and range/profile factors",
            "result": "DEFINITION_ONLY",
            "missing_for_claim": "parent kinetic normalization, X mass/range relation, and Newtonian comparison convention",
            "if_missing": "K_X cannot be absorbed into tau_R10 without losing units/provenance",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "audit_id": "TAUR1033_4_Qbar_source",
            "target": "separate source-leg charge from test-leg tau_R10",
            "mathematical_form": "Qbar_XH(source,lambda) := source-normalized Hilbert/trace/source charge entering the Yukawa field solution",
            "result": "DEFINITION_ONLY",
            "missing_for_claim": "same-worldtube Hilbert source, measured-GM calibration, source support, and hidden-current silence",
            "if_missing": "source leg may hide q_nonH or support terms",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "audit_id": "TAUR1033_5_universal_cg_limit",
            "target": "check whether universal conformal coupling makes tau_R10=1",
            "mathematical_form": "if beta_source=beta_test=c_g in a fully normalized scalar-tensor convention, alpha is proportional to c_g^2, not a free tau_R10=1 claim",
            "result": "UNITY_SHORTCUT_REJECTED",
            "missing_for_claim": "full convention proving beta_source, beta_test, K_X, and Newton normalization",
            "if_missing": "do not set tau_R10=1 by intuition",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "audit_id": "TAUR1033_6_verdict",
            "target": "derive or source tau_R10 for current MTS finite branch",
            "mathematical_form": "tau_R10 is score-ready only with sourced profile/material/projection convention and all companion factors",
            "result": "NOT_DERIVED_CURRENT_CORPUS",
            "missing_for_claim": "tau_R10, K_X(lambda), Qbar_XH, c_g, digitized alpha_bound(lambda), and tail envelope",
            "if_missing": "write acquisition rows and refuse R10 scoring",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
    ]


def profile_contract_rows() -> list[dict[str, str]]:
    return [
        {
            "contract_id": "R10PC1033_0_force_law",
            "required_input": "Yukawa force law convention",
            "mathematical_form": "alpha(lambda) multiplies exp(-r/lambda) correction to Newtonian potential",
            "current_status": "SYMBOLIC_ANCHOR_ONLY",
            "needed_source": "digitized/source-backed alpha_bound(lambda) curve",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "contract_id": "R10PC1033_1_range_relation",
            "required_input": "lambda_X relation",
            "mathematical_form": "lambda_X is the static range of the finite X mode in metres under the selected kinetic/mass normalization",
            "current_status": "MISSING_PARENT_RANGE_NORMALIZATION",
            "needed_source": "parent X kinetic/mass row or sourced finite range",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "contract_id": "R10PC1033_2_KX",
            "required_input": "K_X(lambda)",
            "mathematical_form": "static Green-kernel and Newton-normalized conversion between MTS charges and alpha(lambda)",
            "current_status": "MISSING_KERNEL_NORMALIZATION",
            "needed_source": "derived propagator normalization and G comparison",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "contract_id": "R10PC1033_3_Qbar_XH",
            "required_input": "Qbar_XH",
            "mathematical_form": "source-normalized Hilbert/source charge for the source body under R10 support convention",
            "current_status": "MISSING_SOURCE_CHARGE",
            "needed_source": "same-worldtube source measure and measured-GM calibration",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "contract_id": "R10PC1033_4_tau_R10",
            "required_input": "tau_R10",
            "mathematical_form": "test-leg/material projection converting c_g into R10 test charge under selected profile convention",
            "current_status": "MISSING_ARENA_PROJECTION",
            "needed_source": "test-body trace/readout convention and finite-size/material correction",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "contract_id": "R10PC1033_5_tail_envelope",
            "required_input": "retained tails",
            "mathematical_form": "absolute envelope for b_A,b_alpha,b_dis,q_nonH,Delta_W_support and hidden components",
            "current_status": "ABSOLUTE_ENVELOPE_REQUIRED",
            "needed_source": "theorem-zero or numeric/source-backed rows for every retained component",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "contract_id": "R10PC1033_6_score_gate",
            "required_input": "R10 score gate",
            "mathematical_form": "score only if alpha_predicted(lambda) and alpha_bound(lambda) are numeric, unit-matched, sourced, and valid_for_claim=true",
            "current_status": "CLAIM_BLOCKED",
            "needed_source": "all R10PC1033_0 through R10PC1033_5 closed",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
    ]


def acquisition_rows() -> list[dict[str, str]]:
    return [
        {
            "acquisition_id": "R10ACQ1033_0_alpha_bound_curve",
            "quantity": "alpha_bound(lambda)",
            "candidate_value": "MISSING_DIGITIZED_ALPHA_BOUND",
            "units": "range-dependent",
            "source_path": "source-intake/local_bounds/R10_alpha_lambda_bound_curve_DIGITIZED.csv",
            "source_row_id": "R10_BOUND_PLACEHOLDER_0",
            "derivation_status": "MISSING_DIGITIZED_BOUND_CURVE",
            "required_columns": "lambda_value;lambda_units;alpha_bound;alpha_bound_source;digitization_method;valid_for_claim",
            "ready_for_score": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "acquisition_id": "R10ACQ1033_1_KX_lambda",
            "quantity": "K_X(lambda)",
            "candidate_value": "MISSING_KERNEL_NORMALIZATION",
            "units": "model_dependent",
            "source_path": "MISSING_PARENT_SOURCE",
            "source_row_id": "MISSING_SOURCE_ROW_ID",
            "derivation_status": "MISSING_GREEN_FUNCTION_DERIVATION",
            "required_columns": "lambda_value;K_X;normalization;kinetic_term;G_conversion;source_path",
            "ready_for_score": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "acquisition_id": "R10ACQ1033_2_Qbar_XH",
            "quantity": "Qbar_XH",
            "candidate_value": "MISSING_SOURCE_CHARGE",
            "units": "dimensionless_or_declared",
            "source_path": "MISSING_PARENT_SOURCE",
            "source_row_id": "MISSING_SOURCE_ROW_ID",
            "derivation_status": "MISSING_SOURCE_NORMALIZATION",
            "required_columns": "source_body;support_rule;Qbar_XH;units;measured_GM_calibration;source_path",
            "ready_for_score": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "acquisition_id": "R10ACQ1033_3_tau_R10",
            "quantity": "tau_R10",
            "candidate_value": "MISSING_ARENA_PROJECTION",
            "units": "dimensionless",
            "source_path": "MISSING_PROJECTION_SOURCE",
            "source_row_id": "MISSING_SOURCE_ROW_ID",
            "derivation_status": "MISSING_R10_PROJECTION_DERIVATION",
            "required_columns": "test_body;material;profile;tau_R10;units;trace_convention;source_path",
            "ready_for_score": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "acquisition_id": "R10ACQ1033_4_cg",
            "quantity": "c_g",
            "candidate_value": "MISSING_PARENT_INPUT",
            "units": "dimensionless",
            "source_path": "MISSING_PARENT_SOURCE",
            "source_row_id": "MISSING_SOURCE_ROW_ID",
            "derivation_status": "MISSING_PARENT_CG_OR_ZERO_THEOREM",
            "required_columns": "branch;c_g;units;source_path;derivation_status;claim_policy",
            "ready_for_score": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "acquisition_id": "R10ACQ1033_5_alpha_predicted",
            "quantity": "alpha_predicted(lambda)",
            "candidate_value": "MISSING_SOURCE_NORMALIZED_ALPHA_PREDICTION",
            "units": "dimensionless",
            "source_path": "source-intake/mts_residuals/R10_alpha_lambda_curve_MTS_source_normalization.csv",
            "source_row_id": "bulk_memory_range_template",
            "derivation_status": "MISSING_MTS_PREDICTION",
            "required_columns": "lambda_value;alpha_predicted;K_X;Qbar_XH;tau_R10;c_g;tail_envelope;source_paths",
            "ready_for_score": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
    ]


def refusal_rows(acquisition: list[dict[str, str]]) -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    for index, row in enumerate(acquisition):
        failures = []
        for field, label in [
            ("candidate_value", "MISSING_VALUE"),
            ("source_path", "MISSING_SOURCE_PATH"),
            ("source_row_id", "MISSING_SOURCE_ROW_ID"),
            ("derivation_status", "MISSING_DERIVATION_STATUS"),
        ]:
            if "MISSING" in row[field]:
                failures.append(label)
        if row["ready_for_score"] != "true":
            failures.append("NOT_READY_FOR_SCORE")
        if row["valid_for_claim"] != "true":
            failures.append("CLAIM_POLICY_FALSE")
        rows.append(
            {
                "run_id": f"R10REF1033_{index}_{row['quantity'].replace('(', '').replace(')', '').replace('/', '_').replace(' ', '_')}",
                "acquisition_id": row["acquisition_id"],
                "quantity": row["quantity"],
                "candidate_value": row["candidate_value"],
                "refusal_status": "rejected_missing_R10_inputs",
                "failure_reasons": ";".join(failures),
                "score_eligible": "false",
                "claim_allowed": "false",
                "valid_for_claim": "false",
                "generated_utc": stamp(),
            }
        )
    return rows


def claim_gate_rows() -> list[dict[str, str]]:
    return [
        {
            "gate_id": "CGATE1033_0_sources",
            "claim": "all 1033 cited sources exist",
            "gate_pass": "true",
            "reason": "validated by source register",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "gate_id": "CGATE1033_1_tau_derived",
            "claim": "tau_R10 is derived or sourced",
            "gate_pass": "false",
            "reason": "tau_R10 remains MISSING_ARENA_PROJECTION",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "gate_id": "CGATE1033_2_alpha_bound_curve",
            "claim": "R10 alpha(lambda) bound curve is score-ready",
            "gate_pass": "false",
            "reason": "bound curve file contains placeholder rows, not digitized alpha_bound(lambda)",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "gate_id": "CGATE1033_3_alpha_prediction",
            "claim": "MTS alpha_predicted(lambda) is score-ready",
            "gate_pass": "false",
            "reason": "K_X, Qbar_XH, tau_R10, c_g, and tail envelope are missing",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "gate_id": "CGATE1033_4_R10_pass",
            "claim": "R10 passes finite c_g branch",
            "gate_pass": "false",
            "reason": "both bound and prediction rows are unscoreable placeholders",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "gate_id": "CGATE1033_5_no_cancellation",
            "claim": "unknown local terms may cancel",
            "gate_pass": "true",
            "reason": "absolute no-cancellation envelope remains required",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
    ]


def decision_rows() -> list[dict[str, str]]:
    return [
        {
            "decision_id": "DEC1033_0_tau_status",
            "decision": "tau_R10 is not a free constant and is not derived yet.",
            "because": "it bundles the R10 material/test projection, trace convention, source-test profile, and Xhat normalization.",
            "next_action": "derive/source tau_R10 as a projection row rather than setting it to unity",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "decision_id": "DEC1033_1_factor_status",
            "decision": "R10 finite branch needs K_X(lambda), Qbar_XH, tau_R10, c_g, and the tail envelope.",
            "because": "without separating these factors, alpha(lambda) cannot be compared to the external bound curve.",
            "next_action": "acquire/derive K_X and Qbar_XH alongside tau_R10",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "decision_id": "DEC1033_2_bound_status",
            "decision": "R10 bound data is still symbolic/placeholder.",
            "because": "local bound claims name the source but do not provide a digitized alpha_bound(lambda) curve.",
            "next_action": "digitize/source the R10 alpha(lambda) bound curve before any score",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "decision_id": "DEC1033_3_next_target",
            "decision": "Next target is R10 bound curve digitization plus projection input pack.",
            "because": "the theory-side tau row and external alpha(lambda) bound are both required before finite-branch scoring.",
            "next_action": "1034-Y5-R10-alpha-bound-curve-digitization-and-projection-input-pack.md",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
    ]


def next_target_rows() -> list[dict[str, str]]:
    return [
        {
            "next_target": "1034-Y5-R10-alpha-bound-curve-digitization-and-projection-input-pack.md",
            "objective": "obtain/source a real R10 alpha_bound(lambda) curve and build a projection input pack for K_X(lambda), Qbar_XH, tau_R10, c_g, and retained tails without scoring placeholders",
            "include": "R10 alpha_bound(lambda), digitization provenance, lambda units, K_X(lambda), Qbar_XH, tau_R10, c_g provenance, source/test profile convention, no-cancellation envelope",
            "exclude": "R10 pass claim, invented bound rows, invented tau/c_g/K_X values, unity tau shortcut, PPN/local-GR claim, GitHub action, formalization-workbench edits",
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
    derivation: list[dict[str, str]],
    profile: list[dict[str, str]],
    acquisition: list[dict[str, str]],
    refusals: list[dict[str, str]],
    gates: list[dict[str, str]],
    decisions: list[dict[str, str]],
    next_target: list[dict[str, str]],
) -> list[dict[str, str]]:
    changed = formalization_changed_after_start()
    derivation_required = {f"TAUR1033_{idx}_{name}" for idx, name in [
        (0, "R10_observable"),
        (1, "factorization"),
        (2, "tau_definition"),
        (3, "KX_definition"),
        (4, "Qbar_source"),
        (5, "universal_cg_limit"),
        (6, "verdict"),
    ]}
    profile_required = {f"R10PC1033_{idx}_{name}" for idx, name in [
        (0, "force_law"),
        (1, "range_relation"),
        (2, "KX"),
        (3, "Qbar_XH"),
        (4, "tau_R10"),
        (5, "tail_envelope"),
        (6, "score_gate"),
    ]}
    acquisition_required = {f"R10ACQ1033_{idx}_{name}" for idx, name in [
        (0, "alpha_bound_curve"),
        (1, "KX_lambda"),
        (2, "Qbar_XH"),
        (3, "tau_R10"),
        (4, "cg"),
        (5, "alpha_predicted"),
    ]}
    checks = [
        ("V1033_0_sources_exist", all(flag(row["exists"]) and flag(row["needle_found"]) for row in sources), "all cited source paths exist and expected needles are present"),
        ("V1033_1_derivation_rows_complete", derivation_required.issubset({row["audit_id"] for row in derivation}), "derivation audit covers observable, factorization, tau, K_X, Qbar, unity shortcut, and verdict"),
        ("V1033_2_tau_not_claimed", any(row["audit_id"] == "TAUR1033_6_verdict" and row["result"] == "NOT_DERIVED_CURRENT_CORPUS" for row in derivation), "tau_R10 remains nonclaim"),
        ("V1033_3_unity_shortcut_rejected", any(row["audit_id"] == "TAUR1033_5_universal_cg_limit" and row["result"] == "UNITY_SHORTCUT_REJECTED" for row in derivation), "tau_R10=1 shortcut is rejected"),
        ("V1033_4_profile_contract_complete", profile_required.issubset({row["contract_id"] for row in profile}), "profile contract covers force law, range, K_X, Qbar, tau, tails, and score gate"),
        ("V1033_5_profile_nonclaim", all(row["claim_allowed"] == "false" and row["valid_for_claim"] == "false" for row in profile), "profile contract rows remain nonclaim"),
        ("V1033_6_acquisition_complete", acquisition_required.issubset({row["acquisition_id"] for row in acquisition}), "acquisition rows cover bound curve, K_X, Qbar, tau_R10, c_g, and alpha prediction"),
        ("V1033_7_acquisition_not_ready", all(row["ready_for_score"] == "false" and row["valid_for_claim"] == "false" for row in acquisition), "acquisition rows refuse scoring"),
        ("V1033_8_refusals_complete", len(refusals) == len(acquisition) and all(row["score_eligible"] == "false" for row in refusals), "refusal runner rejects every placeholder acquisition row"),
        ("V1033_9_claim_gates_blocked", all(row["claim_allowed"] == "false" and row["valid_for_claim"] == "false" for row in gates), "all claim gates refuse promotion"),
        ("V1033_10_no_cancellation_guard", any(row["gate_id"] == "CGATE1033_5_no_cancellation" and flag(row["gate_pass"]) for row in gates), "no-cancellation guard is active"),
        ("V1033_11_decision_next", any(row["decision_id"] == "DEC1033_3_next_target" for row in decisions), "decision ledger selects the 1034 target"),
        ("V1033_12_next_target_written", len(next_target) == 1 and "1034-Y5-R10-alpha-bound-curve" in next_target[0]["next_target"], "1034 next target row is present"),
        ("V1033_13_no_overclaim", all(row.get("valid_for_claim", "false") == "false" for group in [sources, derivation, profile, acquisition, refusals, gates, decisions, next_target] for row in group), "all generated rows remain valid_for_claim=false"),
        ("V1033_14_formalization_untouched", len(changed) == 0, f"formalization-workbench modified-file count since script start is {len(changed)}"),
    ]
    passed_all = all(passed for _, passed, _ in checks)
    rows = [{"check_id": check_id, "result": "pass" if passed else "fail", "detail": detail, "generated_utc": stamp()} for check_id, passed, detail in checks]
    rows.insert(0, {"check_id": "V1033_SUMMARY", "result": "pass" if passed_all else "fail", "detail": "1033 tau_R10 projection derivation/acquisition validation summary", "generated_utc": stamp()})
    return rows


def write_doc(
    sources: list[dict[str, str]],
    derivation: list[dict[str, str]],
    profile: list[dict[str, str]],
    acquisition: list[dict[str, str]],
    refusals: list[dict[str, str]],
    gates: list[dict[str, str]],
    decisions: list[dict[str, str]],
    next_target: list[dict[str, str]],
    validations: list[dict[str, str]],
) -> None:
    text = "\n".join(
        [
            "# 1033 Y5 R10 tau_R10 projection derivation or source acquisition",
            "",
            "**Status:** `tau_R10` is now defined as an R10 arena projection, not a magic constant. It cannot be set to one or scored until the full finite-branch factorization is sourced: `K_X(lambda)`, `Qbar_XH`, `tau_R10`, `c_g`, a digitized/source-backed `alpha_bound(lambda)` curve, and the retained-tail absolute envelope.",
            "",
            "**Claim ceiling:** no `tau_R10` derivation claim, finite-`c_g` score, R10 pass, PPN pass, SPM-derived claim, local-GR/Newton pass, or source-side GR pass is allowed from 1033.",
            "",
            "## Source register",
            md_table(sources, ["source_id", "source_path", "exists", "needle_found", "role"]),
            "## tau_R10 derivation audit",
            md_table(derivation, ["audit_id", "target", "mathematical_form", "result", "missing_for_claim", "if_missing", "valid_for_claim"]),
            "## R10 profile-normalization contract",
            md_table(profile, ["contract_id", "required_input", "mathematical_form", "current_status", "needed_source", "claim_allowed", "valid_for_claim"]),
            "## R10 acquisition template",
            md_table(acquisition, ["acquisition_id", "quantity", "candidate_value", "units", "source_path", "source_row_id", "derivation_status", "required_columns", "ready_for_score", "valid_for_claim"]),
            "## Placeholder refusal runner",
            md_table(refusals, ["run_id", "acquisition_id", "quantity", "candidate_value", "refusal_status", "failure_reasons", "score_eligible", "claim_allowed", "valid_for_claim"]),
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
    derivation = derivation_audit_rows()
    profile = profile_contract_rows()
    acquisition = acquisition_rows()
    refusals = refusal_rows(acquisition)
    gates = claim_gate_rows()
    decisions = decision_rows()
    next_target = next_target_rows()
    validations = validation_rows(sources, derivation, profile, acquisition, refusals, gates, decisions, next_target)

    write_csv(OUT / "P8_Y5_R10_1033_SOURCE_REGISTER.csv", sources)
    write_csv(OUT / "P8_Y5_R10_1033_TAU_R10_DERIVATION_AUDIT.csv", derivation)
    write_csv(OUT / "P8_Y5_R10_1033_R10_PROFILE_NORMALIZATION_CONTRACT.csv", profile)
    write_csv(OUT / "P8_Y5_R10_1033_R10_ACQUISITION_TEMPLATE.csv", acquisition)
    write_csv(OUT / "P8_Y5_R10_1033_PLACEHOLDER_REFUSAL_RUNNER.csv", refusals)
    write_csv(OUT / "P8_Y5_R10_1033_CLAIM_GATES.csv", gates)
    write_csv(OUT / "P8_Y5_R10_1033_DECISION_LEDGER.csv", decisions)
    write_csv(OUT / "P8_Y5_R10_1033_NEXT_TARGET.csv", next_target)
    write_csv(OUT / "P8_Y5_BRR545_1033_VALIDATION.csv", validations)
    write_doc(sources, derivation, profile, acquisition, refusals, gates, decisions, next_target, validations)


if __name__ == "__main__":
    main()

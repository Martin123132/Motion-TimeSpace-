from __future__ import annotations

import csv
from datetime import datetime, timezone
from pathlib import Path


STARTED = datetime.now(timezone.utc)
ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "source-intake" / "mts_residuals"
DOC = ROOT / "1024-Y5-R10-scalar-nohair-input-pack-or-residual-alpha-coefficient-runner.md"
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
        ("SRC1024_0_1023_next", "source-intake/mts_residuals/P8_Y5_R10_1023_NEXT_TARGET.csv", "scalar no-hair", "1023 handoff to scalar no-hair input pack."),
        ("SRC1024_1_1023_inputs", "source-intake/mts_residuals/P8_Y5_R10_1023_SCALAR_SOURCE_INPUT_PACK.csv", "SNH1023_0_Z_X", "1023 scalar/source input pack."),
        ("SRC1024_2_1023_demotion", "source-intake/mts_residuals/P8_Y5_R10_1023_DEMOTION_LEDGER.csv", "DEM1023_1_scalar_operator", "1023 scalar route promoted to work target, not claim."),
        ("SRC1024_3_1022_scalar", "source-intake/mts_residuals/P8_Y5_R10_1022_SCALAR_NOHAIR_CONSTRUCTION.csv", "SNH1022_6_verdict", "1022 scalar no-hair clauses."),
        ("SRC1024_4_670_sourcefree", "source-intake/mts_residuals/P8_Y5_R10_670_POSITIVE_SOURCEFREE_PROOF_CHAIN.csv", "PSF670_6_zero_profile_result", "670 positive source-free theorem chain."),
        ("SRC1024_5_669_residual", "source-intake/mts_residuals/P8_Y5_R10_669_R10_R11_RESIDUAL_VECTOR.csv", "RV669_0_Z_X", "669 residual coefficient vector."),
        ("SRC1024_6_669_gates", "source-intake/mts_residuals/P8_Y5_R10_669_LX_OWNER_GATE_TESTS.csv", "G669_1_positive_kinetic", "669 scalar input gates."),
        ("SRC1024_7_669_candidates", "source-intake/mts_residuals/P8_Y5_R10_669_MINIMAL_LX_OPERATOR_CANDIDATES.csv", "LX669_2_positive_sourcefree_massive", "669 scalar/source-free candidate."),
        ("SRC1024_8_579_contract", "source-intake/mts_residuals/P8_Y5_R10_579_EXPLICIT_PARENT_X_BLOCK_CONTRACT.csv", "PXC579_1_positive_kinetic_residue", "579 parent X block contract."),
        ("SRC1024_9_580_candidates", "source-intake/mts_residuals/P8_Y5_R10_580_PARENT_BLOCK_CANDIDATES.csv", "PB580_2_positive_sourcefree_massive_X", "580 parent block candidate."),
        ("SRC1024_10_618_source_zero", "source-intake/mts_residuals/P8_Y5_R10_618_SOURCE_ZERO_CERTIFICATE_AUDIT.csv", "SZ618_0_qbar_XT_chain_rule", "618 source-zero certificate audit."),
        ("SRC1024_11_energy_identity", "source-intake/mts_residuals/P8_EXTRA_SECTOR_SILENCE_ENERGY_IDENTITY.csv", "E506_scalar_positive_operator", "extra-sector positive energy identity template."),
        ("SRC1024_12_1019_schema", "source-intake/mts_residuals/P8_Y5_R10_1019_SOURCE_PACK_SCHEMA.csv", "SP1019_2_bulk_X_coefficients", "1019 source-pack schema for bulk X and alpha rows."),
    ]
    rows = []
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


def scalar_input_assessment_rows() -> list[dict[str, str]]:
    rows = [
        {
            "input_id": "SIA1024_0_operator_domain",
            "quantity": "O_X self-adjoint positive operator",
            "required_condition": "O_X=-nabla_i(Z_X nabla^i)+M_X^2 on a compact source-free exterior with owned domain",
            "current_evidence": "PSF670_0 and SNH1022_0 give template only",
            "current_status": "TEMPLATE_ONLY",
            "missing_for_claim": "parent operator, field units, self-adjoint boundary conditions, compact exterior domain",
            "if_missing": "energy identity cannot be used as theorem-zero",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "input_id": "SIA1024_1_Z_X",
            "quantity": "Z_X>0",
            "required_condition": "second variation fixes positive kinetic residue with normalization and units",
            "current_evidence": "PXC579_1 and RV669_0 say formula/input missing",
            "current_status": "MISSING_PARENT_INPUT",
            "missing_for_claim": "parent Hessian, sign convention, field normalization, units",
            "if_missing": "ghost/anti-elliptic/indefinite residual must be retained",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "input_id": "SIA1024_2_M_X2_lambda",
            "quantity": "M_X^2>0 and lambda_X",
            "required_condition": "mass gap is positive and lambda_X=sqrt(Z_X/M_X^2) has source-backed length units",
            "current_evidence": "PXC579_2 and RV669_1/RV669_6 are missing",
            "current_status": "MISSING_PARENT_INPUT",
            "missing_for_claim": "parent Hessian curvature, range derivation, unit convention",
            "if_missing": "long-range/tachyonic/zero-mode branch remains possible",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "input_id": "SIA1024_3_J_X_zero",
            "quantity": "J_X=0",
            "required_condition": "ordinary matter plus hidden/source/domain terms are X-blind channel-by-channel",
            "current_evidence": "PSF670_4, G669_3, and SZ618_0 are conditional/not signed",
            "current_status": "MISSING_SOURCE_ZERO_PROOF",
            "missing_for_claim": "matter quotient/no-marker theorem or explicit source-current zero/bound",
            "if_missing": "qbar_XT and source-coupling rows remain live",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "input_id": "SIA1024_4_boundary_flux_zero",
            "quantity": "boundary_flux_X=0",
            "required_condition": "boundary flux is zero/proper/exact or source-backed bounded",
            "current_evidence": "PSF670_5 and RV669_7 remain boundary-lock missing",
            "current_status": "MISSING_BOUNDARY_LOCK",
            "missing_for_claim": "boundary class/no-hair/projector silence or boundary flux bound",
            "if_missing": "EDGEBOUND, Qbar_edge_XH, and FB5540 boundary rows remain live",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "input_id": "SIA1024_5_energy_identity",
            "quantity": "positive energy identity",
            "required_condition": "int_A(Z_X|grad X|^2+M_X^2 X^2)=int_A XJ_X+boundary_flux_X",
            "current_evidence": "PSF670_1 says the math identity is conditional",
            "current_status": "CONDITIONAL_MATH_ONLY",
            "missing_for_claim": "SIA1024_0 through SIA1024_4 all close together",
            "if_missing": "no scalar no-hair/local-GR claim",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "input_id": "SIA1024_6_verdict",
            "quantity": "scalar no-hair theorem",
            "required_condition": "all scalar input rows parent-signed or source-bounded with zero RHS",
            "current_evidence": "all required input rows remain missing/conditional",
            "current_status": "FAIL_CURRENT_CLAIM",
            "missing_for_claim": "operator, Z_X, M_X^2, J_X=0, boundary_flux_X=0, units",
            "if_missing": "run residual alpha coefficient refusal",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
    ]
    return rows


def alpha_coefficient_rows() -> list[dict[str, str]]:
    rows = [
        {
            "row_id": "ALPHA1024_0_bulk_operator",
            "quantity": "Z_X;M_X2;lambda_X",
            "formula": "lambda_X=sqrt(Z_X/M_X2)",
            "required_columns": "system_id;field_id;Z_X;M_X2;lambda_X;Z_units;M_units;lambda_units;source_path;valid_for_claim",
            "current_status": "MISSING_PARENT_INPUT",
            "source_path": "source-intake/mts_residuals/P8_Y5_R10_669_R10_R11_RESIDUAL_VECTOR.csv",
            "runner_status": "blocked_missing_operator_inputs",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "row_id": "ALPHA1024_1_source_current",
            "quantity": "J_X or J_X_bound",
            "formula": "O_X X=J_X",
            "required_columns": "system_id;J_X;J_X_bound;source_channel;units;source_path;valid_for_claim",
            "current_status": "MISSING_SOURCE_ZERO_PROOF",
            "source_path": "source-intake/mts_residuals/P8_Y5_R10_618_SOURCE_ZERO_CERTIFICATE_AUDIT.csv",
            "runner_status": "blocked_missing_source_zero_or_bound",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "row_id": "ALPHA1024_2_boundary_flux",
            "quantity": "boundary_flux_X or boundary_flux_bound",
            "formula": "boundary_flux_X=int_boundary X Z_X n.grad X plus edge/projector terms",
            "required_columns": "system_id;boundary_flux_X;boundary_flux_bound;boundary_rule;units;source_path;valid_for_claim",
            "current_status": "MISSING_BOUNDARY_LOCK",
            "source_path": "source-intake/mts_residuals/P8_Y5_R10_669_R10_R11_RESIDUAL_VECTOR.csv",
            "runner_status": "blocked_missing_boundary_flux_zero_or_bound",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "row_id": "ALPHA1024_3_bulk_R10_projection",
            "quantity": "K_X;Qbar_XH;qbar_XT",
            "formula": "alpha_bulk(lambda_X)=K_X Qbar_XH qbar_XT",
            "required_columns": "system_id;lambda_X;K_X;Qbar_XH;qbar_XT;alpha_bulk;normalization;units;source_path;valid_for_claim",
            "current_status": "MISSING_ARENA_PROJECTION",
            "source_path": "source-intake/mts_residuals/P8_Y5_R10_1019_SOURCE_PACK_SCHEMA.csv",
            "runner_status": "blocked_missing_alpha_projection_inputs",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "row_id": "ALPHA1024_4_edge_projection",
            "quantity": "lambda_edge;K_edge;Qbar_edge_XH;qbar_XT",
            "formula": "alpha_edge(lambda_edge)=K_edge Qbar_edge_XH qbar_XT",
            "required_columns": "system_id;lambda_edge;K_edge;Qbar_edge_XH;qbar_XT;alpha_edge;units;source_path;valid_for_claim",
            "current_status": "MISSING_EDGE_PROJECTION",
            "source_path": "source-intake/mts_residuals/P8_Y5_R10_1019_SOURCE_PACK_SCHEMA.csv",
            "runner_status": "blocked_missing_edge_projection_inputs",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "row_id": "ALPHA1024_5_no_cancellation_guard",
            "quantity": "alpha_total_guard",
            "formula": "abs_alpha_total=|alpha_bulk|+|alpha_edge|+|epsilon_FB5540|+|alpha_R11|",
            "required_columns": "system_id;lambda;abs_alpha_bulk;abs_alpha_edge;abs_FB5540;abs_alpha_R11;component_sum_abs;bound;source_path;valid_for_claim",
            "current_status": "NOT_COMPUTED_COMPONENTS_MISSING",
            "source_path": "source-intake/mts_residuals/P8_Y5_R10_1019_SOURCE_PACK_SCHEMA.csv",
            "runner_status": "blocked_missing_no_cancellation_components",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
    ]
    return rows


def runner_rows(alpha_rows: list[dict[str, str]]) -> list[dict[str, str]]:
    rows = []
    for row in alpha_rows:
        reasons = []
        if "MISSING" in row["current_status"] or "NOT_COMPUTED" in row["current_status"]:
            reasons.append(row["current_status"])
        if row["valid_for_claim"] != "true":
            reasons.append("VALID_FOR_CLAIM_FALSE")
        rows.append(
            {
                "runner_id": row["row_id"].replace("ALPHA", "RUN"),
                "row_id": row["row_id"],
                "quantity": row["quantity"],
                "computed_status": row["runner_status"],
                "claim_allowed": "false",
                "failure_reasons": ";".join(reasons),
                "valid_for_claim": "false",
                "generated_utc": stamp(),
            }
        )
    rows.append(
        {
            "runner_id": "RUN1024_6_verdict",
            "row_id": "ALPHA1024_VERDICT",
            "quantity": "scalar_nohair_or_alpha_runner",
            "computed_status": "refused_no_claim",
            "claim_allowed": "false",
            "failure_reasons": "SCALAR_NOHAIR_INPUTS_MISSING;ALPHA_COMPONENTS_MISSING;VALID_FOR_CLAIM_FALSE",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        }
    )
    return rows


def branch_verdict_rows() -> list[dict[str, str]]:
    rows = [
        {
            "verdict_id": "BV1024_0_scalar_zero",
            "branch": "scalar no-hair theorem",
            "status": "fail_current_claim",
            "because": "Z_X, M_X2, J_X=0, boundary_flux_X=0, and units are not parent-signed",
            "allowed_statement": "positive energy identity is a conditional theorem target only",
            "next_action": "try parent Hessian/sign extraction before coefficient scoring",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "verdict_id": "BV1024_1_residual_alpha",
            "branch": "residual alpha scorer",
            "status": "schema_ready_runner_refuses",
            "because": "K_X, Qbar_XH, qbar_XT, lambda_X, edge terms, and total guard are missing",
            "allowed_statement": "alpha rows are ready as nonclaim placeholders only",
            "next_action": "source first operator/range row or first projection row",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "verdict_id": "BV1024_2_coupling_status",
            "branch": "coupling suspicion",
            "status": "confirmed_as_live_gap",
            "because": "J_X/qbar_XT/Qbar_XH channels are exactly the unowned coupling/source inputs",
            "allowed_statement": "coupling is the next concrete input class, not a vague problem",
            "next_action": "fill J_X=0 theorem or qbar_XT coefficient row after Hessian signs",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "verdict_id": "BV1024_3_next_target",
            "branch": "next target",
            "status": "parent_hessian_first",
            "because": "without Z_X and M_X2, neither no-hair nor alpha(lambda) can be normalized",
            "allowed_statement": "first attack the operator/range owner before source projection",
            "next_action": "1025-Y5-R10-parent-Hessian-ZX-MX2-range-or-alpha-source-row.md",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
    ]
    return rows


def claim_gate_rows() -> list[dict[str, str]]:
    rows = [
        ("CG1024_0_sources_registered", "1024 source chain exists", True, "all scalar/no-hair/residual source ledgers are found", False),
        ("CG1024_1_scalar_operator_owned", "scalar operator owned", False, "operator/domain/field units are template only", False),
        ("CG1024_2_ZX_MX2_positive", "Z_X>0 and M_X2>0", False, "parent Hessian signs and units are missing", False),
        ("CG1024_3_sourcefree", "J_X=0", False, "matter/source/hidden channel zero is not parent-signed", False),
        ("CG1024_4_boundary_flux_zero", "boundary_flux_X=0", False, "boundary class/no-hair/projector silence is missing", False),
        ("CG1024_5_scalar_nohair_claim", "scalar no-hair theorem", False, "positive energy identity lacks required inputs", False),
        ("CG1024_6_alpha_runner_claim", "residual alpha scorer pass", False, "alpha coefficient rows are missing and nonclaim", False),
        ("CG1024_7_no_cancellation_guard", "absolute no-cancellation guard", True, "unknown components may not cancel each other into a fake pass", False),
        ("CG1024_8_local_GR_claim", "local GR/Newton reduction", False, "neither theorem-zero nor source-bound local branch closes", False),
    ]
    return [
        {
            "gate_id": gate_id,
            "claim": claim,
            "gate_pass": str(gate_pass).lower(),
            "reason": reason,
            "claim_allowed": str(claim_allowed).lower(),
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        }
        for gate_id, claim, gate_pass, reason, claim_allowed in rows
    ]


def decision_rows() -> list[dict[str, str]]:
    rows = [
        {
            "decision_id": "DEC1024_0_scalar_result",
            "decision": "Scalar no-hair cannot be claimed from current inputs.",
            "because": "the energy identity is conditional and all physical inputs are missing or unsigned.",
            "next_action": "keep no-hair as theorem target, not evidence",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "decision_id": "DEC1024_1_runner_result",
            "decision": "Residual alpha runner is staged but refuses all claims.",
            "because": "operator/range, source, projection, edge, and total guard rows are missing.",
            "next_action": "fill the first parent Hessian/range row before alpha scoring",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "decision_id": "DEC1024_2_coupling",
            "decision": "The coupling gap is now concrete.",
            "because": "J_X, qbar_XT, Qbar_XH, and edge projection are the exact coupling/source places where local tests bite.",
            "next_action": "after Z_X/M_X2, attack J_X=0 or qbar_XT with source paths",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "decision_id": "DEC1024_3_next_target",
            "decision": "Next target is parent Hessian signs and range.",
            "because": "Z_X and M_X2 are the first shared inputs for both scalar no-hair and alpha(lambda).",
            "next_action": "1025-Y5-R10-parent-Hessian-ZX-MX2-range-or-alpha-source-row.md",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
    ]
    return rows


def next_target_rows() -> list[dict[str, str]]:
    return [
        {
            "next_target": "1025-Y5-R10-parent-Hessian-ZX-MX2-range-or-alpha-source-row.md",
            "objective": "derive or source the parent Hessian signs and range: Z_X, M_X^2, field units, lambda_X, and the first fallback alpha source row if the Hessian cannot be owned",
            "include": "second variation, field normalization, kinetic sign, mass-gap sign, units, lambda_X, source paths, no-cancellation guard, fallback K_X/Qbar/qbar row schema",
            "exclude": "source-free by assertion, fitted range as theory input, placeholder alpha pass, quotient no-pole credit, local-GR claim, R10/R11 pass, GitHub action",
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
    inputs: list[dict[str, str]],
    alpha_rows: list[dict[str, str]],
    runner: list[dict[str, str]],
    verdicts: list[dict[str, str]],
    gates: list[dict[str, str]],
    decisions: list[dict[str, str]],
    next_target: list[dict[str, str]],
) -> list[dict[str, str]]:
    changed = formalization_changed_after_start()
    input_required = {"SIA1024_0_operator_domain", "SIA1024_1_Z_X", "SIA1024_2_M_X2_lambda", "SIA1024_3_J_X_zero", "SIA1024_4_boundary_flux_zero", "SIA1024_5_energy_identity", "SIA1024_6_verdict"}
    alpha_required = {"ALPHA1024_0_bulk_operator", "ALPHA1024_1_source_current", "ALPHA1024_2_boundary_flux", "ALPHA1024_3_bulk_R10_projection", "ALPHA1024_4_edge_projection", "ALPHA1024_5_no_cancellation_guard"}
    checks = [
        ("V1024_0_sources_exist", all(flag(row["exists"]) and flag(row["needle_found"]) for row in sources), "all source paths exist and expected needles are present"),
        ("V1024_1_scalar_inputs_complete", input_required.issubset({row["input_id"] for row in inputs}), "scalar input assessment covers operator, Z_X, M_X2, J_X, boundary flux, identity, and verdict"),
        ("V1024_2_scalar_inputs_nonclaim", all(row["valid_for_claim"] == "false" for row in inputs) and any(row["input_id"] == "SIA1024_6_verdict" and row["current_status"] == "FAIL_CURRENT_CLAIM" for row in inputs), "scalar no-hair remains nonclaim"),
        ("V1024_3_alpha_rows_complete", alpha_required.issubset({row["row_id"] for row in alpha_rows}), "alpha coefficient rows cover bulk, source, boundary, projection, edge, and guard"),
        ("V1024_4_alpha_rows_nonclaim", all(row["valid_for_claim"] == "false" and ("MISSING" in row["current_status"] or "NOT_COMPUTED" in row["current_status"]) for row in alpha_rows), "alpha rows remain missing and nonclaim"),
        ("V1024_5_runner_refuses", any(row["runner_id"] == "RUN1024_6_verdict" and row["computed_status"] == "refused_no_claim" for row in runner) and all(row["claim_allowed"] == "false" for row in runner), "runner refuses all claims"),
        ("V1024_6_verdicts_complete", {"BV1024_0_scalar_zero", "BV1024_1_residual_alpha", "BV1024_2_coupling_status", "BV1024_3_next_target"}.issubset({row["verdict_id"] for row in verdicts}), "branch verdicts are complete"),
        ("V1024_7_claim_gates_blocked", all(not flag(row["claim_allowed"]) and not flag(row["valid_for_claim"]) for row in gates), "all claim gates are nonclaim"),
        ("V1024_8_no_cancellation_guard", any(row["gate_id"] == "CG1024_7_no_cancellation_guard" and flag(row["gate_pass"]) for row in gates), "no-cancellation guard is active"),
        ("V1024_9_decision_written", any(row["decision_id"] == "DEC1024_3_next_target" for row in decisions), "1025 decision row is written"),
        ("V1024_10_next_target_written", len(next_target) == 1 and "1025-Y5-R10-parent-Hessian" in next_target[0]["next_target"], "1025 next target row is present"),
        ("V1024_11_formalization_untouched", len(changed) == 0, f"formalization-workbench modified-file count since script start is {len(changed)}"),
    ]
    rows = [{"check_id": check_id, "result": "pass" if passed else "fail", "detail": detail, "generated_utc": stamp()} for check_id, passed, detail in checks]
    rows.insert(0, {"check_id": "V1024_SUMMARY", "result": "pass" if all(row["result"] == "pass" for row in rows) else "fail", "detail": "1024 scalar no-hair input pack and residual alpha runner validation summary", "generated_utc": stamp()})
    return rows


def write_doc(
    sources: list[dict[str, str]],
    inputs: list[dict[str, str]],
    alpha_rows: list[dict[str, str]],
    runner: list[dict[str, str]],
    verdicts: list[dict[str, str]],
    gates: list[dict[str, str]],
    decisions: list[dict[str, str]],
    next_target: list[dict[str, str]],
    validations: list[dict[str, str]],
) -> None:
    text = "\n".join(
        [
            "# 1024 Y5 R10 scalar nohair input pack or residual alpha coefficient runner",
            "",
            "**Status:** The scalar no-hair route is executable as a conditional energy identity only. Current MTS does not yet own `Z_X`, `M_X^2`, `J_X=0`, `boundary_flux_X=0`, `lambda_X`, or the source-normalized alpha coefficients. The residual alpha runner is staged and refuses all claims.",
            "",
            "**Claim ceiling:** no scalar no-hair theorem, no residual alpha pass, no R10/R11 pass, no PPN pass, and no local-GR/Newton reduction is allowed from 1024.",
            "",
            "## Source register",
            md_table(sources, ["source_id", "source_path", "exists", "needle_found", "role"]),
            "## Scalar input assessment",
            md_table(inputs, ["input_id", "quantity", "required_condition", "current_evidence", "current_status", "missing_for_claim", "if_missing", "valid_for_claim"]),
            "## Alpha coefficient rows",
            md_table(alpha_rows, ["row_id", "quantity", "formula", "required_columns", "current_status", "runner_status", "valid_for_claim"]),
            "## Runner refusal",
            md_table(runner, ["runner_id", "row_id", "quantity", "computed_status", "claim_allowed", "failure_reasons", "valid_for_claim"]),
            "## Branch verdicts",
            md_table(verdicts, ["verdict_id", "branch", "status", "because", "allowed_statement", "next_action", "valid_for_claim"]),
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
    inputs = scalar_input_assessment_rows()
    alpha_rows = alpha_coefficient_rows()
    runner = runner_rows(alpha_rows)
    verdicts = branch_verdict_rows()
    gates = claim_gate_rows()
    decisions = decision_rows()
    next_target = next_target_rows()
    validations = validation_rows(sources, inputs, alpha_rows, runner, verdicts, gates, decisions, next_target)

    write_csv(OUT / "P8_Y5_R10_1024_SOURCE_REGISTER.csv", sources)
    write_csv(OUT / "P8_Y5_R10_1024_SCALAR_INPUT_ASSESSMENT.csv", inputs)
    write_csv(OUT / "P8_Y5_R10_1024_ALPHA_COEFFICIENT_ROWS.csv", alpha_rows)
    write_csv(OUT / "P8_Y5_R10_1024_ALPHA_RUNNER_REFUSAL.csv", runner)
    write_csv(OUT / "P8_Y5_R10_1024_BRANCH_VERDICTS.csv", verdicts)
    write_csv(OUT / "P8_Y5_R10_1024_CLAIM_GATES.csv", gates)
    write_csv(OUT / "P8_Y5_R10_1024_DECISION_LEDGER.csv", decisions)
    write_csv(OUT / "P8_Y5_R10_1024_NEXT_TARGET.csv", next_target)
    write_csv(OUT / "P8_Y5_BRR545_1024_VALIDATION.csv", validations)
    write_doc(sources, inputs, alpha_rows, runner, verdicts, gates, decisions, next_target, validations)


if __name__ == "__main__":
    main()

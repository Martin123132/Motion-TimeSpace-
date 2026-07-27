from __future__ import annotations

import csv
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


CHECKPOINT = "2700"
BRANCH_ID = "Y5_R2FR_GAMMA_EFF_CANDIDATE_METRIC_RESPONSE_OR_FIRST_Q_LOC_RESPONSE_ROW_2700"

ROOT = Path(__file__).resolve().parents[1]
SOURCE_INTAKE = ROOT / "source-intake"
RESIDUALS = SOURCE_INTAKE / "mts_residuals"
LOCAL_BOUNDS = SOURCE_INTAKE / "local_bounds"
WEP_RESIDUALS = SOURCE_INTAKE / "microscope" / "branch_locked_wep" / "residuals"
SOURCE_WEIGHT = SOURCE_INTAKE / "source-weight"
RAB_QUEUE = SOURCE_INTAKE / "rab-sector" / "acquisition-queue"

DOC_PATH = ROOT / "2700-Y5-R2FR-Gamma-eff-candidate-metric-response-or-first-q-loc-response-row.md"

OUTPUTS = {
    "source_register": RESIDUALS / "P8_Y5_R2FR_2700_SOURCE_REGISTER.csv",
    "candidate_audit": RESIDUALS / "P8_Y5_R2FR_2700_GAMMA_EFF_CANDIDATE_AUDIT.csv",
    "metric_response_comparison": RESIDUALS / "P8_Y5_R2FR_2700_KHAT_METRIC_RESPONSE_COMPARISON_NONCLAIM.csv",
    "first_response_operator": RESIDUALS / "P8_Y5_R2FR_2700_FIRST_QLOC_RESPONSE_OPERATOR_ROW_NONCLAIM.csv",
    "missing_inputs": RESIDUALS / "P8_Y5_R2FR_2700_RESPONSE_ROW_MISSING_INPUTS.csv",
    "claim_gates": RESIDUALS / "P8_Y5_R2FR_2700_CLAIM_GATES.csv",
    "decision_ledger": RESIDUALS / "P8_Y5_R2FR_2700_DECISION_LEDGER.csv",
    "next_target": RESIDUALS / "P8_Y5_R2FR_2700_NEXT_TARGET.csv",
    "project_status": RESIDUALS / "P8_Y5_R2FR_2700_PROJECT_STATUS_SNAPSHOT.csv",
    "branch_copies": RESIDUALS / "P8_Y5_R2FR_2700_BRANCH_COPIES.csv",
    "validation": RESIDUALS / f"P8_Y5_BRR545_{CHECKPOINT}_VALIDATION.csv",
}

BRANCH_OUTPUTS = {
    "local_response_operator": LOCAL_BOUNDS / "q_loc_first_PPN_response_operator_2700_NONCLAIM.csv",
    "local_metric_comparison": LOCAL_BOUNDS / "GammaKhat_metric_response_comparison_2700_NONCLAIM.csv",
    "wep_response_operator": WEP_RESIDUALS / "q_loc_first_PPN_response_operator_2700_NONCLAIM.csv",
    "source_weight_response_operator": SOURCE_WEIGHT / "QLOC_FIRST_PPN_RESPONSE_OPERATOR_2700_NONCLAIM.csv",
    "rab_next": RAB_QUEUE / "JR2700_QLOC_RESPONSE_COEFFICIENTS_OR_KHAT_SOURCE_MATCH_NEXT.csv",
}

SOURCE_SPECS: list[dict[str, Any]] = [
    {
        "source_id": "SRC2700_2699_NEXT",
        "relative_path": "2699-Y5-R2FR-Gamma-Khat-q-loc-first-variation-or-official-residual-demotion.md",
        "required_needles": ["NEXT2699_0_selected", "QLOC2699_1_metric_response", "VAL2699_OVERALL"],
        "purpose": "imports the selected metric-response or response-row target",
    },
    {
        "source_id": "SRC2700_GK_CANDIDATES",
        "relative_path": "source-intake/mts_residuals/P8_GK_STRESS_ACTION_CANDIDATES.csv",
        "required_needles": ["GK514_A_metric_response_scalar_density", "GK514_D_residual_branch"],
        "purpose": "imports candidate S_GK action shapes",
    },
    {
        "source_id": "SRC2700_GAMMA_OWNER",
        "relative_path": "source-intake/mts_residuals/P8_GAMMA_OWNER_CANDIDATE_ACTION.csv",
        "required_needles": ["GO516_A_response_doublet_quadratic_density", "GO516_D_residual_bound_runner"],
        "purpose": "imports candidate Gamma_eff owner densities",
    },
    {
        "source_id": "SRC2700_RESPONSE_DOUBLET",
        "relative_path": "source-intake/mts_residuals/P8_RESPONSE_DOUBLET_ACTION_CONTRACT.csv",
        "required_needles": ["RD516_2_metric_response", "RD516_5_PPN_lock"],
        "purpose": "imports response-doublet metric-response and PPN-lock clauses",
    },
    {
        "source_id": "SRC2700_METRIC_EVIDENCE",
        "relative_path": "source-intake/mts_residuals/P8_GK_METRIC_RESPONSE_SOURCE_EVIDENCE.csv",
        "required_needles": ["E515_4_source_current_audit", "E515_5_current_contract"],
        "purpose": "imports source evidence showing the metric-response contract exists but is not matched",
    },
    {
        "source_id": "SRC2700_2581_LOCK",
        "relative_path": "2581-Y5-R2FR-GammaKhat-q_loc-coupling-double-zero-or-residual-lock.md",
        "required_needles": ["TEST2581_0_PPN_alpha", "QLOC2581_TOTAL", "VAL2581_OVERALL"],
        "purpose": "imports local-test queue and PPN missing projection status",
    },
    {
        "source_id": "SRC2700_2206_DEMOTION",
        "relative_path": "2206-Y5-R2FR-GammaKhat-q-loc-parent-action-signature-or-official-residual-demotion.md",
        "required_needles": ["APQ2206_0_PPN", "QDEM2206_9_total", "VAL2206_OVERALL"],
        "purpose": "imports q_loc residual demotion and PPN response-operator need",
    },
]


def stamp() -> str:
    return datetime.now(timezone.utc).isoformat()


def as_bool(value: bool) -> str:
    return "true" if value else "false"


def path_for(relative_path: str) -> Path:
    return ROOT / relative_path


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace") if path.exists() else ""


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        raise ValueError(f"Refusing to write empty CSV: {path}")
    fieldnames = list(rows[0].keys())
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def parse_csv(path: Path) -> tuple[bool, int, str]:
    try:
        with path.open(newline="", encoding="utf-8") as handle:
            reader = csv.DictReader(handle)
            rows = list(reader)
            if not reader.fieldnames:
                return False, 0, "missing_header"
            return True, len(rows), "parsed"
    except Exception as exc:  # pragma: no cover
        return False, 0, f"{type(exc).__name__}: {exc}"


def markdown_table(rows: list[dict[str, Any]]) -> str:
    if not rows:
        return "_No rows._"
    headers = list(rows[0].keys())
    lines = ["| " + " | ".join(headers) + " |", "| " + " | ".join("---" for _ in headers) + " |"]
    for row in rows:
        cells = [str(row.get(header, "")).replace("|", "\\|").replace("\n", "<br>") for header in headers]
        lines.append("| " + " | ".join(cells) + " |")
    return "\n".join(lines)


def source_register_rows() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for spec in SOURCE_SPECS:
        path = path_for(spec["relative_path"])
        text = read_text(path)
        needles = list(spec["required_needles"])
        found = [needle for needle in needles if needle in text]
        missing = [needle for needle in needles if needle not in text]
        rows.append(
            {
                "source_id": spec["source_id"],
                "relative_path": spec["relative_path"],
                "absolute_path": str(path),
                "exists": as_bool(path.exists()),
                "required_needles": ";".join(needles),
                "found_needles": ";".join(found),
                "missing_needles": ";".join(missing),
                "purpose": spec["purpose"],
                "valid_for_claim": "false",
                "timestamp_utc": stamp(),
            }
        )
    return rows


def candidate_audit_rows() -> list[dict[str, Any]]:
    rows = [
        (
            "GCA2700_0_GK514_A",
            "metric_response_scalar_density",
            "S_GK=-int sqrt(-g) Gamma_eff(g,Phi,nabla Phi,D,...)",
            "K_hat^{mu nu}=K_metric^{mu nu}[Gamma_eff]",
            "best_candidate_not_matched_to_existing_MTS",
            "no explicit source-signed Gamma_eff formula; no live K_hat tensor term list; no derivative/boundary convention",
            "REJECT_FOR_CLAIM_USE_AS_TEMPLATE",
        ),
        (
            "GCA2700_1_GO516_A",
            "response_doublet_quadratic_density",
            "Gamma_eff=Gamma0+1/2 M_AB(g,R_even,D,...) Z^A Z^B+O(Z^4)",
            "K_hat is the metric response of sqrt(-g)Gamma_eff and F1 vanishes at Z=0",
            "best_candidate_not_current_MTS_derived",
            "Z^A component lock, M_AB source, live K_hat comparison, and PPN/source-normalization lock are absent",
            "REJECT_FOR_CLAIM_USE_AS_SCHEMATIC_COMPARISON",
        ),
        (
            "GCA2700_2_GO516_B",
            "positive_auxiliary_energy_density",
            "Gamma_eff=V(Phi)+1/2 G_AB(Phi)nabla Phi^A nabla Phi^B",
            "K_hat is the kinetic/elastic metric response",
            "candidate_but_source_current_zero_not_derived",
            "source-current zero, boundary no-flux, and physical residual map are missing",
            "REJECT_FOR_CLAIM_KEEP_AS_FUTURE_MODEL",
        ),
        (
            "GCA2700_3_GO516_C",
            "topological_boundary_density",
            "Gamma_eff from normalized boundary/topological density or exact form",
            "K_hat is boundary/improvement stress response",
            "candidate_but_charge_unit_and_boundary_flux_open",
            "charge units and no-flux boundary theorem are not signed",
            "REJECT_FOR_CLAIM_KEEP_AS_BOUNDARY_ROUTE",
        ),
        (
            "GCA2700_4_verdict",
            "candidate audit verdict",
            "no current candidate is source-signed enough to compute a live K_metric=K_hat pass",
            "metric-response branch cannot promote q_loc zero",
            "NO_SOURCE_SIGNED_GAMMA_EFF_CANDIDATE",
            "fall back to strict first response-operator row",
            "RESPONSE_ROW_ROUTE_SELECTED",
        ),
    ]
    return [
        {
            "candidate_id": candidate_id,
            "candidate_type": candidate_type,
            "candidate_formula": formula,
            "metric_response_target": target,
            "source_status": status,
            "blocking_gap": gap,
            "decision": decision,
            "source_signed": "false",
            "metric_comparison_possible": "false",
            "valid_for_claim": "false",
            "claim_allowed": "false",
            "timestamp_utc": stamp(),
        }
        for candidate_id, candidate_type, formula, target, status, gap, decision in rows
    ]


def metric_response_comparison_rows() -> list[dict[str, Any]]:
    rows = [
        (
            "MRC2700_0_schematic_response_doublet",
            "GO516_A_response_doublet_quadratic_density",
            "Gamma_eff=Gamma0+1/2 M_AB Z^A Z^B+O(Z^4)",
            "K_metric^{mu nu}=2/sqrt(-g) delta[sqrt(-g)Gamma_eff]/delta g_{mu nu} minus convention",
            "at Z=0 after Gamma0 subtraction, K_metric and partial_Z K_metric can be zero if M_AB is finite/even",
            "not a live comparison: M_AB, Z^A component lock and K_hat tensor components are missing",
            "SCHEMATIC_ONLY_NOT_MATCHED",
        ),
        (
            "MRC2700_1_live_Khat_match",
            "live_MTS_Khat",
            "K_hat^{mu nu} from current corpus",
            "term-by-term compare to K_metric[Gamma_eff]",
            "cannot compute",
            "no source-signed live K_hat component list and no source-signed Gamma_eff density",
            "NOT_COMPUTABLE_CURRENT_CORPUS",
        ),
        (
            "MRC2700_2_metric_response_defect",
            "q_metric_response_defect",
            "Delta_K^{mu nu}=K_hat^{mu nu}-K_metric^{mu nu}[Gamma_eff]",
            "Delta_K must be zero by theorem or projected into q_loc residuals",
            "retained as symbolic residual",
            "requires source-backed Gamma_eff, K_hat, derivative convention, boundary/improvement convention",
            "OFFICIAL_RETAINED_GAP",
        ),
    ]
    return [
        {
            "comparison_id": comparison_id,
            "object": obj,
            "input_formula": formula,
            "metric_response_formula": response,
            "comparison_result": result,
            "reason": reason,
            "status": status,
            "valid_for_claim": "false",
            "claim_allowed": "false",
            "timestamp_utc": stamp(),
        }
        for comparison_id, obj, formula, response, result, reason, status in rows
    ]


def first_response_operator_rows() -> list[dict[str, Any]]:
    source_paths = ";".join(
        str(path_for(path))
        for path in [
            "2699-Y5-R2FR-Gamma-Khat-q-loc-first-variation-or-official-residual-demotion.md",
            "2581-Y5-R2FR-GammaKhat-q_loc-coupling-double-zero-or-residual-lock.md",
            "2206-Y5-R2FR-GammaKhat-q-loc-parent-action-signature-or-official-residual-demotion.md",
        ]
    )
    return [
        {
            "operator_id": "QOP2700_0_PPN_GK_q_loc_response_operator",
            "arena": "PPN",
            "input_residual": "q_loc_residual_vector_abs",
            "operator_symbol": "R_PPN_GK[q_loc;g_obs,source_frame,radial_profile]",
            "projected_quantity": "Delta_PPN_GK=(gamma-1,beta-1,alpha_1,alpha_2,alpha_3,zeta_1,zeta_2,zeta_3,zeta_4,xi)_GK",
            "input_units": "force_density_or_arena_normalized_q_loc_vector",
            "output_units": "dimensionless_PPN_coefficients",
            "source_paths": source_paths,
            "known_formula": "Delta_PPN_GK^a = integral K_PPN^a{}_nu(r,source,frame) q_loc^nu(r) dV after source normalization",
            "required_missing_inputs": "K_PPN_kernel;q_loc_radial_profile;source_normalization_map;metric_response_matrix;frame_choice;boundary_condition;threshold_table",
            "score_ready": "false",
            "valid_for_claim": "false",
            "claim_allowed": "false",
            "next_action": "fill K_PPN kernel or fallback to R10 alpha(lambda) operator if PPN kernel remains unavailable",
            "timestamp_utc": stamp(),
        }
    ]


def missing_input_rows() -> list[dict[str, Any]]:
    rows = [
        ("MISS2700_0_K_PPN_kernel", "K_PPN^a{}_nu", "response kernel from q_loc force/stress residual to PPN coefficients", "PPN", "MISSING_OPERATOR_DERIVATION"),
        ("MISS2700_1_qloc_profile", "q_loc^nu(r)", "radial/source/frame profile or theorem-zero certificate", "PPN;R10;orbital", "MISSING_PROFILE"),
        ("MISS2700_2_source_normalization", "source_normalization_map", "same source measure used before PPN readout", "PPN;R11;Newton", "MISSING_PIM_HTAU_LOCK"),
        ("MISS2700_3_metric_response_matrix", "metric_response_matrix", "how q_metric_response_defect changes g_obs coefficients", "PPN;clock;orbital", "MISSING_KHAT_METRIC_RESPONSE"),
        ("MISS2700_4_frame_boundary", "frame_choice;boundary_condition", "observed frame and no-flux/reference class fixed before projection", "PPN;WEP;local_GR", "MISSING_FRAME_BOUNDARY_LOCK"),
        ("MISS2700_5_thresholds", "PPN_threshold_table", "which experimental bounds to compare to after prediction exists", "PPN", "MISSING_COMPARISON_TABLE"),
    ]
    return [
        {
            "missing_id": missing_id,
            "input": input_name,
            "purpose": purpose,
            "affected_arenas": arenas,
            "status": status,
            "source_backed": "false",
            "score_ready": "false",
            "valid_for_claim": "false",
            "timestamp_utc": stamp(),
        }
        for missing_id, input_name, purpose, arenas, status in rows
    ]


def claim_gate_rows() -> list[dict[str, Any]]:
    rows = [
        ("CG2700_0_source_candidate", "source-signed Gamma_eff candidate exists", "BLOCKED_NONCLAIM", "false", "false", "all candidates are templates or conditional"),
        ("CG2700_1_metric_match", "K_hat=K_metric[Gamma_eff] term-by-term", "NOT_COMPUTABLE_NONCLAIM", "false", "false", "no live source-signed tensors"),
        ("CG2700_2_response_row", "first PPN q_loc response row exists", "PASS_NONCLAIM_SCHEMA", "true", "false", "row has units and source paths but missing kernels/profile"),
        ("CG2700_3_score_ready", "PPN score can be run", "BLOCKED_NONCLAIM", "false", "false", "operator kernel and profile missing"),
        ("CG2700_4_local_GR", "local GR/Newton can be claimed", "BLOCKED_NONCLAIM", "false", "false", "q_loc is neither zero nor bounded"),
        ("CG2700_5_public", "public/GitHub readiness", "BLOCKED_PRIVATE_WORK", "false", "false", "private derivation plumbing only"),
    ]
    return [
        {
            "claim_gate_id": gate_id,
            "gate": gate,
            "status": status,
            "gate_passed": passed,
            "claim_allowed": allowed,
            "reason": reason,
            "timestamp_utc": stamp(),
        }
        for gate_id, gate, status, passed, allowed, reason in rows
    ]


def decision_ledger_rows() -> list[dict[str, Any]]:
    rows = [
        ("DEC2700_0_candidate_result", "NO_SOURCE_SIGNED_GAMMA_EFF_FOUND", "candidate shapes are useful but remain templates, so no live K_hat metric-response pass is available", "do not claim q_loc zero"),
        ("DEC2700_1_schematic_gain", "RESPONSE_DOUBLET_SCHEMATIC_RECORDED", "the quadratic-even Gamma route would kill first variation at Z=0 if component lock and metric response are later signed", "keep as future derivation route"),
        ("DEC2700_2_response_row", "FIRST_PPN_QLOC_RESPONSE_OPERATOR_ROW_CREATED", "the q_loc branch now has a concrete nonclaim PPN operator row with units and source paths", "fill kernel/profile inputs next"),
        ("DEC2700_3_next", "PPN_KERNEL_OR_R10_OPERATOR_NEXT", "progress now requires a real response kernel or an easier R10 alpha(lambda) conversion row", "run 2701"),
    ]
    return [
        {
            "decision_id": decision_id,
            "decision": decision,
            "rationale": rationale,
            "next_action": next_action,
            "valid_for_claim": "false",
            "timestamp_utc": stamp(),
        }
        for decision_id, decision, rationale, next_action in rows
    ]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        {
            "next_id": "NEXT2700_0_selected",
            "selection": "selected_primary",
            "target_doc": "2701-Y5-R2FR-q-loc-PPN-kernel-or-R10-alpha-response-operator-fill.md",
            "target_script": "scripts/Y5_R2FR_q_loc_PPN_kernel_or_R10_alpha_response_operator_fill_2701.py",
            "task": "try to derive the PPN response kernel K_PPN from q_loc to PPN coefficients; if too underdetermined, create the first R10 alpha(lambda) response-operator row with units and missing-input ledger",
            "success_condition": "one response operator is either derived enough for a dry-run schema, or staged as a strict nonclaim row with source paths, units, and explicit missing inputs",
            "forbidden_shortcuts": "score placeholders; claim local GR; hide q_loc in measured G; use cancellation-only budgets; GitHub action; formalization-workbench edits",
            "valid_for_claim": "false",
            "timestamp_utc": stamp(),
        }
    ]


def project_status_rows() -> list[dict[str, Any]]:
    rows = [
        ("STATUS2700_0_metric_response", "Gamma/Khat metric response", "NO_LIVE_MATCH_YET", "candidate formulas are not source-signed current MTS tensors", "fill kernel/profile or source-sign Gamma_eff later"),
        ("STATUS2700_1_q_loc_testing", "q_loc empirical residual path", "FIRST_PPN_OPERATOR_ROW_STAGED", "not score-ready, but no longer abstract", "derive K_PPN or switch to R10 alpha row"),
        ("STATUS2700_2_local_GR", "local GR/Newton", "STILL_BLOCKED_BUT_MORE_EXECUTABLE", "q_loc residual now has a concrete response-row scaffold", "make one projection calculable"),
        ("STATUS2700_3_public", "public/GitHub", "NO_ACTION_PRIVATE", "checkpoint is private and nonclaim", "keep private"),
    ]
    return [
        {
            "status_id": status_id,
            "topic": topic,
            "status": status,
            "meaning": meaning,
            "next_action": next_action,
            "claim_allowed": "false",
            "timestamp_utc": stamp(),
        }
        for status_id, topic, status, meaning, next_action in rows
    ]


def branch_copy_rows() -> list[dict[str, Any]]:
    return [
        {
            "copy_id": "BC2700_0_local_operator",
            "source_csv": str(OUTPUTS["first_response_operator"]),
            "branch_csv": str(BRANCH_OUTPUTS["local_response_operator"]),
            "purpose": "local-bound branch receives first PPN q_loc response-operator row",
            "valid_for_claim": "false",
            "timestamp_utc": stamp(),
        },
        {
            "copy_id": "BC2700_1_local_metric",
            "source_csv": str(OUTPUTS["metric_response_comparison"]),
            "branch_csv": str(BRANCH_OUTPUTS["local_metric_comparison"]),
            "purpose": "local-bound branch receives Khat metric-response nonclaim comparison",
            "valid_for_claim": "false",
            "timestamp_utc": stamp(),
        },
        {
            "copy_id": "BC2700_2_wep",
            "source_csv": str(OUTPUTS["first_response_operator"]),
            "branch_csv": str(BRANCH_OUTPUTS["wep_response_operator"]),
            "purpose": "WEP residual branch receives q_loc operator scaffold",
            "valid_for_claim": "false",
            "timestamp_utc": stamp(),
        },
        {
            "copy_id": "BC2700_3_source_weight",
            "source_csv": str(OUTPUTS["first_response_operator"]),
            "branch_csv": str(BRANCH_OUTPUTS["source_weight_response_operator"]),
            "purpose": "source-weight branch receives q_loc/source-normalization operator scaffold",
            "valid_for_claim": "false",
            "timestamp_utc": stamp(),
        },
        {
            "copy_id": "BC2700_4_rab_next",
            "source_csv": str(OUTPUTS["next_target"]),
            "branch_csv": str(BRANCH_OUTPUTS["rab_next"]),
            "purpose": "RAB queue receives PPN-kernel or R10-operator next target",
            "valid_for_claim": "false",
            "timestamp_utc": stamp(),
        },
    ]


def validation_rows(rows_by_name: dict[str, list[dict[str, Any]]]) -> list[dict[str, Any]]:
    source_rows = rows_by_name["source_register"]
    all_sources_exist = all(row["exists"] == "true" for row in source_rows)
    all_needles_found = all(row["missing_needles"] == "" for row in source_rows)

    parse_targets = {key: path for key, path in OUTPUTS.items() if key != "validation"}
    parse_targets.update(BRANCH_OUTPUTS)
    parse_results = {key: parse_csv(path) for key, path in parse_targets.items()}
    all_csv_parse = all(ok and count > 0 for ok, count, _ in parse_results.values())

    candidates = rows_by_name["candidate_audit"]
    comparisons = rows_by_name["metric_response_comparison"]
    operators = rows_by_name["first_response_operator"]
    missing_inputs = rows_by_name["missing_inputs"]
    claim_gates = rows_by_name["claim_gates"]
    next_targets = rows_by_name["next_target"]

    no_source_signed_candidate = all(row["source_signed"] == "false" for row in candidates)
    metric_not_claimed = all(row["claim_allowed"] == "false" and row["valid_for_claim"] == "false" for row in comparisons)
    response_row_present = any(
        row["operator_id"] == "QOP2700_0_PPN_GK_q_loc_response_operator"
        and row["source_paths"] != ""
        and row["input_units"] != ""
        and row["output_units"] == "dimensionless_PPN_coefficients"
        and row["valid_for_claim"] == "false"
        for row in operators
    )
    missing_inputs_recorded = len(missing_inputs) >= 5 and all(row["valid_for_claim"] == "false" for row in missing_inputs)
    no_claims = all(row["claim_allowed"] == "false" for row in claim_gates)
    next_2701 = any(row["next_id"] == "NEXT2700_0_selected" and "2701-" in row["target_doc"] for row in next_targets)
    no_formalization_outputs = all("formalization-workbench" not in str(path).lower() for path in parse_targets.values())
    no_github_outputs = all(".git" not in str(path).lower() and "github" not in path.name.lower() for path in parse_targets.values())

    checks = [
        ("VAL2700_0_sources_exist", all_sources_exist, "all cited source paths exist"),
        ("VAL2700_1_needles_found", all_needles_found, "all required source needles were found"),
        ("VAL2700_2_csv_parse", all_csv_parse, "all generated CSVs and branch copies parse with at least one row"),
        ("VAL2700_3_no_source_signed_candidate", no_source_signed_candidate, "no candidate is falsely marked source-signed"),
        ("VAL2700_4_metric_not_claimed", metric_not_claimed, "metric-response comparison stays nonclaim"),
        ("VAL2700_5_response_row_present", response_row_present, "first PPN q_loc response row has units, source paths, and valid_for_claim=false"),
        ("VAL2700_6_missing_inputs_recorded", missing_inputs_recorded, "missing kernel/profile/source inputs are explicit"),
        ("VAL2700_7_no_claims", no_claims, "all claim gates keep claim_allowed=false"),
        ("VAL2700_8_next_2701", next_2701, "2701 PPN-kernel or R10 operator target selected"),
        ("VAL2700_9_no_formalization_outputs", no_formalization_outputs, "no output path points into formalization-workbench"),
        ("VAL2700_10_no_github_outputs", no_github_outputs, "no GitHub/public-output path was written"),
    ]

    rows: list[dict[str, Any]] = []
    for check_id, passed, detail in checks:
        rows.append(
            {
                "check_id": check_id,
                "passed": as_bool(passed),
                "detail": detail,
                "timestamp_utc": stamp(),
            }
        )
    for key, (ok, count, message) in parse_results.items():
        rows.append(
            {
                "check_id": f"VAL2700_PARSE_{key}",
                "passed": as_bool(ok and count > 0),
                "detail": f"{message}; rows={count}",
                "timestamp_utc": stamp(),
            }
        )
    overall = all(row["passed"] == "true" for row in rows)
    rows.append(
        {
            "check_id": "VAL2700_OVERALL",
            "passed": as_bool(overall),
            "detail": "2700 rejects unsourced Gamma_eff metric-response promotion, records a schematic comparison, creates the first nonclaim PPN q_loc response row, and selects 2701 kernel/operator fill",
            "timestamp_utc": stamp(),
        }
    )
    return rows


def write_doc(rows_by_name: dict[str, list[dict[str, Any]]]) -> None:
    verdict = (
        "2700 checks the concrete route and does not fake it: the response-doublet Gamma_eff shape is mathematically useful, "
        "but it is not source-signed as the live MTS Gamma_eff/K_hat pair. Therefore K_hat=K_metric[Gamma_eff] cannot be claimed. "
        "The useful forward move is executable plumbing: the first nonclaim PPN q_loc response-operator row is now staged with units, "
        "source paths, and explicit missing kernels/profile inputs."
    )
    text = f"""# 2700: Gamma_eff Candidate Metric Response Or First q_loc Response Row

**Branch:** `{BRANCH_ID}`

## Private Verdict

{verdict}

## Candidate Audit

{markdown_table(rows_by_name["candidate_audit"])}

## Metric-Response Comparison

{markdown_table(rows_by_name["metric_response_comparison"])}

## First q_loc Response Operator

{markdown_table(rows_by_name["first_response_operator"])}

## Missing Inputs

{markdown_table(rows_by_name["missing_inputs"])}

## Source Register

{markdown_table(rows_by_name["source_register"])}

## Claim Gates

{markdown_table(rows_by_name["claim_gates"])}

## Decisions

{markdown_table(rows_by_name["decision_ledger"])}

## Next Target

{markdown_table(rows_by_name["next_target"])}

## Project Status

{markdown_table(rows_by_name["project_status"])}

## Validation

{markdown_table(rows_by_name["validation"])}
"""
    DOC_PATH.write_text(text, encoding="utf-8")


def main() -> None:
    source_rows = source_register_rows()
    candidate_rows = candidate_audit_rows()
    comparison_rows = metric_response_comparison_rows()
    operator_rows = first_response_operator_rows()
    missing_rows = missing_input_rows()
    claim_rows = claim_gate_rows()
    decision_rows = decision_ledger_rows()
    next_rows = next_target_rows()
    status_rows = project_status_rows()
    branch_rows = branch_copy_rows()

    rows_by_name: dict[str, list[dict[str, Any]]] = {
        "source_register": source_rows,
        "candidate_audit": candidate_rows,
        "metric_response_comparison": comparison_rows,
        "first_response_operator": operator_rows,
        "missing_inputs": missing_rows,
        "claim_gates": claim_rows,
        "decision_ledger": decision_rows,
        "next_target": next_rows,
        "project_status": status_rows,
        "branch_copies": branch_rows,
    }

    for key, rows in rows_by_name.items():
        write_csv(OUTPUTS[key], rows)

    write_csv(BRANCH_OUTPUTS["local_response_operator"], operator_rows)
    write_csv(BRANCH_OUTPUTS["local_metric_comparison"], comparison_rows)
    write_csv(BRANCH_OUTPUTS["wep_response_operator"], operator_rows)
    write_csv(BRANCH_OUTPUTS["source_weight_response_operator"], operator_rows)
    write_csv(BRANCH_OUTPUTS["rab_next"], next_rows)

    validation = validation_rows(rows_by_name)
    rows_by_name["validation"] = validation
    write_csv(OUTPUTS["validation"], validation)
    write_doc(rows_by_name)

    print(f"wrote {DOC_PATH}")
    print(f"wrote {OUTPUTS['validation']}")


if __name__ == "__main__":
    main()

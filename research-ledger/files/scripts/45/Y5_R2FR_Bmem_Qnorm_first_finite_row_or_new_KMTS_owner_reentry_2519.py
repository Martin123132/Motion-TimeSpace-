from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
BRANCH_ID = "MTS_R2FR_BMEM_QNORM_FIRST_FINITE_ROW_2519"
CHECKPOINT_ID = "2519"
DOC = ROOT / "2519-Y5-R2FR-Bmem-Qnorm-first-finite-row-or-new-KMTS-owner-reentry.md"
MTS_RESIDUALS = ROOT / "source-intake" / "mts_residuals"

OUTPUTS = {
    "source_register": MTS_RESIDUALS / "P8_Y5_NO_SHADOW_2519_SOURCE_REGISTER.csv",
    "bmem_reentry_audit": MTS_RESIDUALS / "P8_Y5_NO_SHADOW_2519_BMEM_REENTRY_AUDIT.csv",
    "bmem_finite_row": MTS_RESIDUALS / "P8_Y5_NO_SHADOW_2519_BMEM_FINITE_ROW.csv",
    "qnorm_link_rows": MTS_RESIDUALS / "P8_Y5_NO_SHADOW_2519_QNORM_LINK_ROWS.csv",
    "observable_gate": MTS_RESIDUALS / "P8_Y5_NO_SHADOW_2519_OBSERVABLE_GATE.csv",
    "dryrun_results": MTS_RESIDUALS / "P8_Y5_NO_SHADOW_2519_DRYRUN_RESULTS.csv",
    "decision_ledger": MTS_RESIDUALS / "P8_Y5_NO_SHADOW_2519_DECISION_LEDGER.csv",
    "next_target": MTS_RESIDUALS / "P8_Y5_NO_SHADOW_2519_NEXT_TARGET.csv",
    "branch_copies": MTS_RESIDUALS / "P8_Y5_NO_SHADOW_2519_BRANCH_COPIES.csv",
    "validation": MTS_RESIDUALS / "P8_Y5_BRR545_2519_VALIDATION.csv",
}

BRANCH_COPIES = {
    "bmem_reentry_audit": ROOT
    / "source-intake"
    / "local_bounds"
    / "Bmem_reentry_audit_2519_NONCLAIM.csv",
    "qnorm_link_rows": ROOT
    / "source-intake"
    / "beta-source"
    / "docs"
    / "Bmem_Qnorm_link_rows_2519_NONCLAIM.csv",
    "bmem_finite_row": ROOT
    / "source-intake"
    / "rab-sector"
    / "acquisition-queue"
    / "JR2519_BMEM_FINITE_ROW_NONCLAIM.csv",
    "next_target": ROOT
    / "source-intake"
    / "rab-sector"
    / "acquisition-queue"
    / "JR2519_QMEM_QNORM_COMPONENT_NEXT_NONCLAIM.csv",
}

SOURCE_SPECS = [
    {
        "source_id": "SRC2519_0_2518_next",
        "path": "source-intake/mts_residuals/P8_Y5_NO_SHADOW_2518_NEXT_TARGET.csv",
        "needles": ["NEXT2518_0_selected", "B_mem/Qnorm"],
        "role": "authoritative 2518 handoff selecting finite B_mem/Qnorm first-fill",
    },
    {
        "source_id": "SRC2519_1_2518_finite_rows",
        "path": "source-intake/mts_residuals/P8_Y5_NO_SHADOW_2518_FINITE_VERTEX_INPUT_ROWS.csv",
        "needles": ["HVIN2518_0_Bmem", "MISSING_NO_XR_VERTEX_OR_VALUE"],
        "role": "current finite memory vertex input gap",
    },
    {
        "source_id": "SRC2519_2_2518_validation",
        "path": "source-intake/mts_residuals/P8_Y5_BRR545_2518_VALIDATION.csv",
        "needles": ["VAL2518_OVERALL", "PASS"],
        "role": "previous checkpoint validation gate",
    },
    {
        "source_id": "SRC2519_3_1349_kmts",
        "path": "1349-Y5-R10-RAB-KMTS-trace-projection-owner-or-memory-closure-declaration.md",
        "needles": ["KMTS_TRACE_PROJECTION_OWNER_NOT_DERIVED", "SYMBOLIC_NONCLAIM_RETAINED"],
        "role": "best current K_MTS owner result and finite residual default",
    },
    {
        "source_id": "SRC2519_4_1350_runner",
        "path": "1350-Y5-R10-RAB-finite-Bmem-and-qloc-residual-runner-contract.md",
        "needles": ["REQ1350_0_Bmem", "WOULD_ACCEPT_IF_REAL_FILES_AND_VALUES_EXIST"],
        "role": "strict finite B_mem/q_loc runner contract",
    },
    {
        "source_id": "SRC2519_5_1372_qnorm",
        "path": "1372-Y5-R10-RAB-fixed-L0-double-zero-local-residual-theorem-or-Qnorm-bound.md",
        "needles": ["Q_norm <= Q_alg + Q_cdb + Q_mem + Q_bdy + Q_trans + Q_proj", "QGF1372_1_gamma_bound"],
        "role": "Q_norm component decomposition and PPN gamma feed",
    },
    {
        "source_id": "SRC2519_6_1590_coupling",
        "path": "1590-Y5-R2FR-Gamma-Khat-Ploc-owner-bundle-or-cR2-finite-coefficient-row.md",
        "needles": ["COUPLING_AND_RESPONSE_REMAIN_THE_BOTTLENECK", "QGAMMA_QNORM_IS_THE_TESTING_LANE"],
        "role": "newer R2FR summary naming coupling/response as the active bottleneck",
    },
]


def timestamp() -> str:
    return datetime.now(timezone.utc).isoformat()


def base_row(**kwargs: Any) -> dict[str, Any]:
    row: dict[str, Any] = {
        "timestamp_utc": timestamp(),
        "branch_id": BRANCH_ID,
        "checkpoint_id": CHECKPOINT_ID,
        "valid_for_claim": False,
        "claim_allowed": False,
    }
    row.update(kwargs)
    return row


def read_text(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8", errors="replace")
    except FileNotFoundError:
        return ""


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fieldnames: list[str] = []
    for row in rows:
        for fieldname in row:
            if fieldname not in fieldnames:
                fieldnames.append(fieldname)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def csv_rows_parse(path: Path) -> tuple[bool, int, str]:
    try:
        with path.open(newline="", encoding="utf-8") as handle:
            parsed_rows = list(csv.DictReader(handle))
        return bool(parsed_rows), len(parsed_rows), "OK"
    except Exception as exc:
        return False, 0, f"{type(exc).__name__}: {exc}"


def md_table(rows: list[dict[str, Any]], columns: list[str]) -> str:
    lines = [
        "| " + " | ".join(columns) + " |",
        "| " + " | ".join("---" for _ in columns) + " |",
    ]
    for row in rows:
        cells: list[str] = []
        for column in columns:
            value = str(row.get(column, "")).replace("\n", "<br>").replace("|", "\\|")
            cells.append(value)
        lines.append("| " + " | ".join(cells) + " |")
    return "\n".join(lines)


def remove_pycache() -> None:
    pycache = Path(__file__).resolve().parent / "__pycache__"
    if pycache.exists():
        shutil.rmtree(pycache)


def source_register_rows() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for spec in SOURCE_SPECS:
        source_path = ROOT / spec["path"]
        source_text = read_text(source_path)
        found_needles = [needle for needle in spec["needles"] if needle in source_text]
        rows.append(
            base_row(
                source_id=spec["source_id"],
                source_path=spec["path"],
                path_exists=source_path.exists(),
                required_needles=";".join(spec["needles"]),
                found_needles=";".join(found_needles),
                role=spec["role"],
                source_pass=source_path.exists() and len(found_needles) == len(spec["needles"]),
            )
        )
    return rows


def bmem_reentry_audit_rows() -> list[dict[str, Any]]:
    entries = [
        {
            "audit_id": "BRE2519_0_target",
            "test": "can B_mem=0 theorem be re-entered instead of finite-row staging",
            "required_new_evidence": "new K_MTS trace-projection owner source after 1349 plus parent variation of Gamma_eff/K_hat/P_loc",
            "current_evidence": "2518 handoff names finite B_mem/Qnorm first-fill; no new K_MTS owner row is registered",
            "result_status": "REENTRY_ALLOWED_ONLY_IF_NEW_KMTS_OWNER_SOURCE_APPEARS",
            "blocking_marker": "MISSING_NEW_KMTS_OWNER_SOURCE",
        },
        {
            "audit_id": "BRE2519_1_current_source_check",
            "test": "check current source chain for new owner evidence",
            "required_new_evidence": "source path and theorem clause stronger than 1349 private closure",
            "current_evidence": "1349 says KMTS_TRACE_PROJECTION_OWNER_NOT_DERIVED; 2518 keeps HVIN2518_0_Bmem missing",
            "result_status": "NO_REENTRY_CURRENT_CORPUS",
            "blocking_marker": "OLD_FAILURE_STILL_AUTHORITY",
        },
        {
            "audit_id": "BRE2519_2_private_closure_guard",
            "test": "prevent private closure from becoming public theorem",
            "required_new_evidence": "parent-signed zero theorem, not a branch convenience",
            "current_evidence": "B_mem=0 remains PRIVATE_CLOSURE_ONLY in the 1349 lane",
            "result_status": "PRIVATE_CLOSURE_REJECTED_AS_THEOREM",
            "blocking_marker": "PRIVATE_CLOSURE_NOT_THEOREM",
        },
        {
            "audit_id": "BRE2519_3_finite_default",
            "test": "select default if no new owner evidence exists",
            "required_new_evidence": "none for nonclaim staging; finite row must preserve blockers",
            "current_evidence": "1350 runner contract rejects symbolic scoring but accepts future fully sourced schema",
            "result_status": "FINITE_BMEM_ROW_REQUIRED",
            "blocking_marker": "SYMBOLIC_NONCLAIM_ONLY",
        },
        {
            "audit_id": "BRE2519_4_verdict",
            "test": "checkpoint verdict",
            "required_new_evidence": "new K_MTS owner source for theorem route",
            "current_evidence": "no new owner evidence found in current source register",
            "result_status": "DO_NOT_REENTER_ZERO_THEOREM_STAGE_FINITE_ROW",
            "blocking_marker": "MISSING_NEW_KMTS_OWNER_SOURCE",
        },
    ]
    return [base_row(**entry) for entry in entries]


def bmem_finite_rows() -> list[dict[str, Any]]:
    entries = [
        {
            "row_id": "BMEM2519_0_Bmem",
            "quantity": "B_mem",
            "row_role": "primary finite memory curvature vertex row",
            "numeric_value_or_theorem_zero": "MISSING_NO_XR_VERTEX_OR_VALUE",
            "units": "parent_action_units_for_delta_m_R_vertex",
            "parent_owner_source": "MISSING_NEW_KMTS_OR_PARENT_MEMORY_VERTEX_SOURCE",
            "normalization_and_sign": "MISSING_BRANCH_CONVENTION_AND_SIGN",
            "observable_map": "R10;PPN_gamma;Qnorm",
            "bound_source": "MISSING_R10_PPN_QNORM_PROJECTION",
            "current_status": "REJECT_CURRENT_ROW",
            "accepted_for_scoring": False,
            "claim_pass": False,
        },
        {
            "row_id": "BMEM2519_1_Zmem",
            "quantity": "Z_mem",
            "row_role": "memory kinetic normalization",
            "numeric_value_or_theorem_zero": "MISSING_PARENT_INPUT",
            "units": "kinetic_norm_or_parent_action_equivalent",
            "parent_owner_source": "MISSING_MEMORY_OPERATOR_SOURCE",
            "normalization_and_sign": "MISSING_POSITIVITY_CONVENTION",
            "observable_map": "lambda_mem;Qmem",
            "bound_source": "MISSING_OPERATOR_BOUND",
            "current_status": "REJECT_CURRENT_ROW",
            "accepted_for_scoring": False,
            "claim_pass": False,
        },
        {
            "row_id": "BMEM2519_2_M2mem",
            "quantity": "M2_mem",
            "row_role": "memory gap or inverse range",
            "numeric_value_or_theorem_zero": "MISSING_PARENT_INPUT",
            "units": "inverse_length_squared_or_parent_equivalent",
            "parent_owner_source": "MISSING_MEMORY_GAP_SOURCE",
            "normalization_and_sign": "MISSING_STABILITY_DOMAIN",
            "observable_map": "lambda_mem=sqrt(Z_mem/M2_mem);R10",
            "bound_source": "MISSING_RANGE_BOUND",
            "current_status": "REJECT_CURRENT_ROW",
            "accepted_for_scoring": False,
            "claim_pass": False,
        },
        {
            "row_id": "BMEM2519_3_Lmem_inverse",
            "quantity": "L_mem^-1",
            "row_role": "memory response Green operator",
            "numeric_value_or_theorem_zero": "MISSING_DOMAIN_OPERATOR",
            "units": "operator_inverse_units",
            "parent_owner_source": "MISSING_DOMAIN_AND_BOUNDARY_SOURCE",
            "normalization_and_sign": "MISSING_SELF_ADJOINT_POSITIVE_GAP_CONVENTION",
            "observable_map": "Q_mem;Delta_cR2_hidden",
            "bound_source": "MISSING_OPERATOR_NORM_BOUND",
            "current_status": "REJECT_CURRENT_ROW",
            "accepted_for_scoring": False,
            "claim_pass": False,
        },
        {
            "row_id": "BMEM2519_4_Cmem",
            "quantity": "C_mem",
            "row_role": "matter/source coupling into memory branch",
            "numeric_value_or_theorem_zero": "MISSING_SOURCE_RESPONSE_MAP",
            "units": "source_charge_units",
            "parent_owner_source": "MISSING_MATTER_DESCENT_SOURCE",
            "normalization_and_sign": "MISSING_TEST_BODY_NORMALIZATION",
            "observable_map": "WEP;PPN;clock;orbit",
            "bound_source": "MISSING_SOURCE_CHARGE_BOUND",
            "current_status": "REJECT_CURRENT_ROW",
            "accepted_for_scoring": False,
            "claim_pass": False,
        },
        {
            "row_id": "BMEM2519_5_Jmem",
            "quantity": "J_mem",
            "row_role": "independent memory source or bath drive",
            "numeric_value_or_theorem_zero": "MISSING_SOURCE_SILENCE_THEOREM_OR_BOUND",
            "units": "memory_source_units",
            "parent_owner_source": "MISSING_SOURCE_SILENCE_SOURCE",
            "normalization_and_sign": "MISSING_NO_HAIR_CONVENTION",
            "observable_map": "Q_mem;local_residual",
            "bound_source": "MISSING_SOURCE_DRIVE_BOUND",
            "current_status": "REJECT_CURRENT_ROW",
            "accepted_for_scoring": False,
            "claim_pass": False,
        },
        {
            "row_id": "BMEM2519_6_Qboundary_mem",
            "quantity": "Q_boundary_mem",
            "row_role": "memory boundary/domain leakage",
            "numeric_value_or_theorem_zero": "MISSING_BOUNDARY_FLUX_THEOREM_OR_BOUND",
            "units": "boundary_flux_units",
            "parent_owner_source": "MISSING_BOUNDARY_CONDITION_SOURCE",
            "normalization_and_sign": "MISSING_SURFACE_OR_DOMAIN_CONVENTION",
            "observable_map": "Q_bdy;Q_mem;clock;orbit",
            "bound_source": "MISSING_BOUNDARY_BOUND",
            "current_status": "REJECT_CURRENT_ROW",
            "accepted_for_scoring": False,
            "claim_pass": False,
        },
        {
            "row_id": "BMEM2519_7_provenance",
            "quantity": "source_file;normalization;assumptions",
            "row_role": "future scoring provenance lock",
            "numeric_value_or_theorem_zero": "REQUIRED_FOR_FUTURE_SCORING",
            "units": "path_or_url_and_convention",
            "parent_owner_source": "MISSING_FULL_SOURCE_BUNDLE",
            "normalization_and_sign": "MISSING_CONVENTION_LEDGER",
            "observable_map": "all_future_runners",
            "bound_source": "MISSING_BOUND_LEDGER",
            "current_status": "REJECT_CURRENT_ROW",
            "accepted_for_scoring": False,
            "claim_pass": False,
        },
    ]
    return [base_row(score_ready=False, valid_prediction_row=False, **entry) for entry in entries]


def qnorm_link_rows() -> list[dict[str, Any]]:
    entries = [
        {
            "link_id": "QMEM2519_0_Qmem",
            "quantity": "Q_mem",
            "formula": "Q_mem <= A_ref^-1 (N_kin K_mem_kin + N_pot K_mem_drift + N_src J_mem + N_bath B_mem)",
            "required_inputs": "A_ref;N_kin;K_mem_kin;N_pot;K_mem_drift;N_src;J_mem;N_bath;B_mem",
            "status": "SYMBOLIC_BOUND_FORM_DERIVED_INPUTS_MISSING",
            "claim_use": "nonclaim component fill only",
            "blocking_marker": "MISSING_QMEM_COMPONENT_VALUES",
        },
        {
            "link_id": "QMEM2519_1_Qnorm",
            "quantity": "Q_norm",
            "formula": "Q_norm <= Q_alg + Q_cdb + Q_mem + Q_bdy + Q_trans + Q_proj",
            "required_inputs": "Q_alg;Q_cdb;Q_mem;Q_bdy;Q_trans;Q_proj;common norm/domain convention",
            "status": "SYMBOLIC_DECOMPOSITION_READY_COMPONENTS_MISSING",
            "claim_use": "no-cancellation residual budget",
            "blocking_marker": "MISSING_QNORM_COMPONENT_VALUES",
        },
        {
            "link_id": "QMEM2519_2_Cqgamma",
            "quantity": "B_gamma",
            "formula": "B_gamma <= (c^2/(2U_min)) N_G N_D Q_norm",
            "required_inputs": "U_min;N_G;N_D;Q_norm;Cassini gamma policy convention",
            "status": "SYMBOLIC_PPN_FEED_READY_INPUTS_MISSING",
            "claim_use": "PPN gamma residual vector only after numeric source-backed inputs",
            "blocking_marker": "MISSING_CQGAMMA_INPUTS",
        },
        {
            "link_id": "QMEM2519_3_acceptance",
            "quantity": "Qnorm_acceptance_threshold",
            "formula": "Q_alg+Q_cdb+Q_mem+Q_bdy+Q_trans+Q_proj <= 2 U_min sigma_gamma/(c^2 N_G N_D)",
            "required_inputs": "sigma_gamma;U_min;N_G;N_D;all Q_i values",
            "status": "POLICY_FORM_READY_INPUTS_MISSING",
            "claim_use": "future PPN gamma gate only",
            "blocking_marker": "MISSING_THRESHOLD_INPUTS",
        },
        {
            "link_id": "QMEM2519_4_proxy_guard",
            "quantity": "old_compact_shell_or_closure_proxy",
            "formula": "not imported",
            "required_inputs": "source-backed component values only",
            "status": "OLD_PROXY_REJECTED",
            "claim_use": "guardrail",
            "blocking_marker": "DO_NOT_USE_PROXY_SCORING",
        },
    ]
    return [base_row(score_ready=False, accepted_for_scoring=False, claim_pass=False, **entry) for entry in entries]


def observable_gate_rows() -> list[dict[str, Any]]:
    entries = [
        {
            "gate_id": "OG2519_0_R10",
            "arena": "R10 short-range gravity",
            "map_formula": "B_mem,Z_mem,M2_mem,L_mem^-1,C_mem,J_mem,Q_boundary_mem -> alpha(lambda)",
            "required_bundle": "finite coefficient; units; range; source charge; bound curve; projection convention",
            "status": "BLOCKED_MISSING_COEFFICIENT_MAP_AND_BOUND_SOURCE",
            "claim_pass": False,
        },
        {
            "gate_id": "OG2519_1_PPN_gamma",
            "arena": "PPN gamma",
            "map_formula": "Q_norm -> B_gamma <= (c^2/(2U_min)) N_G N_D Q_norm",
            "required_bundle": "Q_i components; U_min;N_G;N_D;sigma_gamma;fixed observed-GM convention",
            "status": "BLOCKED_MISSING_CQGAMMA_INPUTS",
            "claim_pass": False,
        },
        {
            "gate_id": "OG2519_2_PPN_beta",
            "arena": "PPN beta",
            "map_formula": "memory/source second-order response -> delta_beta",
            "required_bundle": "second-order response map and coefficient normalization",
            "status": "BLOCKED_MISSING_SECOND_ORDER_BETA_MAP",
            "claim_pass": False,
        },
        {
            "gate_id": "OG2519_3_clocks",
            "arena": "clock/time tests",
            "map_formula": "Q_mem,Q_bdy,Q_trans -> clock residual vector",
            "required_bundle": "clock projection, coupling to time-rate readout, bound source",
            "status": "BLOCKED_MISSING_CLOCK_PROJECTION",
            "claim_pass": False,
        },
        {
            "gate_id": "OG2519_4_orbits",
            "arena": "orbital systems",
            "map_formula": "Q_norm and source response -> perihelion/range residual vector",
            "required_bundle": "orbital projection, body normalization, observational bound",
            "status": "BLOCKED_MISSING_ORBITAL_PROJECTION",
            "claim_pass": False,
        },
        {
            "gate_id": "OG2519_5_local_GR",
            "arena": "local GR/Newton recovery",
            "map_formula": "B_mem/Q_mem/Q_norm silence plus cdb/boundary/projection closure",
            "required_bundle": "zero theorem or bounded residual vector below all local gates",
            "status": "BLOCKED_NO_LOCAL_GR_CLAIM",
            "claim_pass": False,
        },
    ]
    return [base_row(score_ready=False, accepted_for_scoring=False, **entry) for entry in entries]


def dryrun_rows() -> list[dict[str, Any]]:
    entries = [
        {
            "case_id": "DRY2519_0_Bmem_zero_private_closure",
            "case_description": "reuse B_mem=0 private closure as theorem",
            "missing_requirements": "new K_MTS owner source; parent variation; Gamma_eff/Khat/P_loc response",
            "result_status": "REJECT",
            "blocking_markers": "PRIVATE_CLOSURE_NOT_THEOREM;MISSING_NEW_KMTS_OWNER_SOURCE",
            "pass_fail": "BLOCKED_NONCLAIM",
            "claim_pass": False,
        },
        {
            "case_id": "DRY2519_1_symbolic_Bmem",
            "case_description": "score symbolic B_mem row against R10/PPN",
            "missing_requirements": "numeric/theorem-zero value; units; source path; observable map; bound source",
            "result_status": "REJECT",
            "blocking_markers": "SYMBOLIC_NONCLAIM_ONLY",
            "pass_fail": "BLOCKED_NONCLAIM",
            "claim_pass": False,
        },
        {
            "case_id": "DRY2519_2_numeric_without_parent",
            "case_description": "use numeric B_mem with no parent/source normalization",
            "missing_requirements": "parent_owner_source; normalization_and_sign; source/test convention",
            "result_status": "REJECT",
            "blocking_markers": "MISSING_PARENT_OWNER_SOURCE",
            "pass_fail": "BLOCKED_NONCLAIM",
            "claim_pass": False,
        },
        {
            "case_id": "DRY2519_3_qloc_zero_axiom",
            "case_description": "set q_loc or Q_mem to zero by local vacuum/plateau axiom",
            "missing_requirements": "derived zero theorem for each residual channel",
            "result_status": "REJECT",
            "blocking_markers": "AXIOMATIC_LOCAL_SILENCE_REJECTED",
            "pass_fail": "BLOCKED_NONCLAIM",
            "claim_pass": False,
        },
        {
            "case_id": "DRY2519_4_Qnorm_proxy",
            "case_description": "import old compact-shell or closure proxy as Q_norm value",
            "missing_requirements": "componentwise no-cancellation Q_i values with common norm/domain convention",
            "result_status": "REJECT",
            "blocking_markers": "DO_NOT_USE_PROXY_SCORING",
            "pass_fail": "BLOCKED_NONCLAIM",
            "claim_pass": False,
        },
        {
            "case_id": "DRY2519_5_future_complete_template",
            "case_description": "future B_mem/Q_mem/Qnorm row with real values, source paths, units and maps",
            "missing_requirements": "none in schema, but still future evidence",
            "result_status": "WOULD_ACCEPT_SCHEMA_IF_REAL_FILES_AND_VALUES_EXIST",
            "blocking_markers": "FUTURE_EVIDENCE_ONLY",
            "pass_fail": "TEMPLATE_NONCLAIM",
            "claim_pass": False,
        },
    ]
    return [base_row(score_ready=False, accepted_for_scoring=False, **entry) for entry in entries]


def decision_rows() -> list[dict[str, Any]]:
    entries = [
        {
            "decision_id": "DEC2519_0_no_reentry",
            "decision": "do not re-enter B_mem=0 theorem route in 2519",
            "rationale": "1349 remains the current authority and no new K_MTS owner source is registered",
            "next_action": "retain finite B_mem nonclaim row with missing-value blockers",
            "status": "ACTIVE",
        },
        {
            "decision_id": "DEC2519_1_finite_row",
            "decision": "stage first strict finite B_mem row",
            "rationale": "2518 selected memory before fibre and 1350 requires units/source/map fields before scoring",
            "next_action": "fill B_mem,Z_mem,M2_mem,L_mem^-1,C/J/boundary provenance before any runner claim",
            "status": "ACTIVE",
        },
        {
            "decision_id": "DEC2519_2_qnorm_link",
            "decision": "attach B_mem to Q_mem/Q_norm residual lane",
            "rationale": "1372 converts local theorem failure into a componentwise no-cancellation norm budget",
            "next_action": "attack Q_mem component values or source-silence theorem next",
            "status": "ACTIVE",
        },
        {
            "decision_id": "DEC2519_3_empirical_guard",
            "decision": "keep R10/PPN/clocks/orbits blocked",
            "rationale": "symbolic rows and private closures cannot beat empirical constraints honestly",
            "next_action": "future runs must consume only real finite rows or theorem-zero certificates",
            "status": "ACTIVE",
        },
    ]
    return [base_row(valid_for_claim=False, claim_allowed=False, **entry) for entry in entries]


def next_target_rows() -> list[dict[str, Any]]:
    entries = [
        {
            "route_id": "NEXT2519_0_selected",
            "selection_status": "selected",
            "target_file": "2520-Y5-R2FR-Qmem-component-first-fill-or-memory-source-silence-theorem.md",
            "target_script": "scripts/Y5_R2FR_Qmem_component_first_fill_or_memory_source_silence_theorem_2520.py",
            "objective": "try to prove memory source/stress silence; if not, fill Q_mem component rows with units, source paths, operator norms, and no-cancellation links",
            "success_condition": "Q_mem is either theorem-zero from parent-owned memory/source silence or remains a finite nonclaim component with declared missing inputs and arena projections",
            "do_not_do": "do not score symbolic B_mem; do not use private closure; do not claim local GR/PPN/R10 from Qnorm formula alone",
        },
        {
            "route_id": "NEXT2519_1_fibre_queue",
            "selection_status": "queued_after_memory_Qmem",
            "target_file": "2521-Y5-R2FR-fibre-Bh-finite-row-or-hidden-visible-grammar-reentry.md",
            "target_script": "scripts/Y5_R2FR_fibre_Bh_finite_row_or_hidden_visible_grammar_reentry_2521.py",
            "objective": "classify fibre B_h with hidden-visible grammar reentry or finite fibre coefficient rows after memory/Qmem lane is staged",
            "success_condition": "B_h has theorem-zero evidence or finite nonclaim Z_h/M2_h/B_h/C_h/source-charge rows",
            "do_not_do": "do not let memory closure erase fibre residuals",
        },
    ]
    return [base_row(valid_for_claim=False, claim_allowed=False, **entry) for entry in entries]


def branch_copy_rows() -> list[dict[str, Any]]:
    copy_specs = [
        ("bmem_reentry_audit", OUTPUTS["bmem_reentry_audit"], BRANCH_COPIES["bmem_reentry_audit"]),
        ("qnorm_link_rows", OUTPUTS["qnorm_link_rows"], BRANCH_COPIES["qnorm_link_rows"]),
        ("bmem_finite_row", OUTPUTS["bmem_finite_row"], BRANCH_COPIES["bmem_finite_row"]),
        ("next_target", OUTPUTS["next_target"], BRANCH_COPIES["next_target"]),
    ]
    rows: list[dict[str, Any]] = []
    for copy_id, source_path, destination_path in copy_specs:
        destination_path.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(source_path, destination_path)
        parse_ok, row_count, parse_message = csv_rows_parse(destination_path)
        rows.append(
            base_row(
                copy_id=copy_id,
                source=str(source_path.relative_to(ROOT)),
                destination=str(destination_path.relative_to(ROOT)),
                copied=destination_path.exists(),
                parse_ok=parse_ok,
                row_count=row_count,
                parse_message=parse_message,
            )
        )
    return rows


def falsey(value: Any) -> bool:
    return str(value).strip().lower() in {"false", "0", "no", "not_computed", ""}


def no_claim_flags(rows_by_name: dict[str, list[dict[str, Any]]]) -> bool:
    for name, rows in rows_by_name.items():
        if name in {"source_register", "validation"}:
            continue
        for row in rows:
            for fieldname in (
                "valid_for_claim",
                "claim_allowed",
                "score_ready",
                "valid_prediction_row",
                "accepted_for_scoring",
                "claim_pass",
            ):
                if fieldname in row and not falsey(row[fieldname]):
                    return False
    return True


def validation_rows(rows_by_name: dict[str, list[dict[str, Any]]]) -> list[dict[str, Any]]:
    checks: list[dict[str, Any]] = []

    def add(check_id: str, status: bool, detail: str = "") -> None:
        checks.append(
            base_row(
                check_id=check_id,
                status="PASS" if status else "FAIL",
                detail=detail,
                valid_for_claim=False,
                claim_allowed=False,
            )
        )

    source_rows = rows_by_name["source_register"]
    bmem_rows = rows_by_name["bmem_finite_row"]
    qnorm_rows = rows_by_name["qnorm_link_rows"]
    dryrun_rows_local = rows_by_name["dryrun_results"]
    next_rows = rows_by_name["next_target"]

    add("VAL2519_00_sources_exist", all(str(row["path_exists"]) == "True" for row in source_rows))
    add("VAL2519_01_source_needles", all(str(row["source_pass"]) == "True" for row in source_rows))
    add(
        "VAL2519_02_no_KMTS_reentry",
        any(
            row["audit_id"] == "BRE2519_4_verdict"
            and row["result_status"] == "DO_NOT_REENTER_ZERO_THEOREM_STAGE_FINITE_ROW"
            for row in rows_by_name["bmem_reentry_audit"]
        ),
        "no new K_MTS owner source is accepted",
    )
    add(
        "VAL2519_03_Bmem_primary_row",
        any(
            row["row_id"] == "BMEM2519_0_Bmem"
            and row["quantity"] == "B_mem"
            and row["current_status"] == "REJECT_CURRENT_ROW"
            and str(row["accepted_for_scoring"]) == "False"
            for row in bmem_rows
        ),
        "primary B_mem finite row is present and blocked",
    )
    add(
        "VAL2519_04_Bmem_support_bundle",
        all(
            any(row["quantity"] == required_quantity for row in bmem_rows)
            for required_quantity in ["Z_mem", "M2_mem", "L_mem^-1", "C_mem", "J_mem", "Q_boundary_mem"]
        ),
        "operator/source/boundary support rows are staged",
    )
    add(
        "VAL2519_05_Qmem_Qnorm_links",
        all(
            any(row["link_id"] == required_link for row in qnorm_rows)
            for required_link in ["QMEM2519_0_Qmem", "QMEM2519_1_Qnorm", "QMEM2519_2_Cqgamma", "QMEM2519_3_acceptance"]
        ),
        "Q_mem, Q_norm and C_qgamma formulas are linked",
    )
    add(
        "VAL2519_06_observable_gates_blocked",
        all(str(row["claim_pass"]) == "False" and str(row["status"]).startswith("BLOCKED") for row in rows_by_name["observable_gate"]),
        "R10/PPN/clock/orbit/local-GR gates remain blocked",
    )
    add(
        "VAL2519_07_dryruns_block_bad_rows",
        all(str(row["claim_pass"]) == "False" for row in dryrun_rows_local)
        and all(str(row["result_status"]) in {"REJECT", "WOULD_ACCEPT_SCHEMA_IF_REAL_FILES_AND_VALUES_EXIST"} for row in dryrun_rows_local),
        "closure, symbolic, no-parent, axiom and proxy cases do not score",
    )
    add(
        "VAL2519_08_next_target_Qmem",
        any(row["route_id"] == "NEXT2519_0_selected" and "Qmem-component" in row["target_file"] for row in next_rows),
        "Qmem component first-fill selected next",
    )
    add("VAL2519_09_no_claim_flags", no_claim_flags(rows_by_name))
    add(
        "VAL2519_10_branch_copies",
        all(str(row["copied"]) == "True" and str(row["parse_ok"]) == "True" for row in rows_by_name["branch_copies"]),
    )
    formalization = ROOT.parent / "formalization-workbench"
    formalization_hits = list(formalization.rglob("*2519*")) if formalization.exists() else []
    add(
        "VAL2519_11_no_formalization_artifacts",
        len(formalization_hits) == 0,
        ";".join(str(path) for path in formalization_hits),
    )
    add("VAL2519_12_pycache_absent", not (Path(__file__).resolve().parent / "__pycache__").exists())

    for name, path in OUTPUTS.items():
        if name == "validation":
            continue
        parse_ok, row_count, parse_message = csv_rows_parse(path)
        add(f"VAL2519_CSV_{path.stem}", parse_ok, f"{parse_message}; rows={row_count}")
    for copy_key, copy_path in BRANCH_COPIES.items():
        parse_ok, row_count, parse_message = csv_rows_parse(copy_path)
        add(f"VAL2519_COPY_CSV_{copy_key}", parse_ok, f"{parse_message}; rows={row_count}")

    overall = all(row["status"] == "PASS" for row in checks)
    checks.append(
        base_row(
            check_id="VAL2519_OVERALL",
            status="PASS" if overall else "FAIL",
            detail="2519 refuses B_mem=0 theorem reentry without new K_MTS owner evidence, stages strict finite B_mem rows, links Q_mem/Q_norm/C_qgamma, and selects Qmem first-fill next.",
            valid_for_claim=False,
            claim_allowed=False,
        )
    )
    return checks


def write_doc(rows_by_name: dict[str, list[dict[str, Any]]]) -> None:
    DOC.write_text(
        "\n".join(
            [
                "# 2519 - Bmem Qnorm First Finite Row or New KMTS Owner Reentry",
                "",
                "**Current verdict:** no new `K_MTS` owner evidence is present, so 2519 does not re-enter the `B_mem=0` theorem route. The checkpoint stages the first strict finite `B_mem/Qnorm` nonclaim row instead.",
                "",
                "**Main gain:** the coupling bottleneck is now in runner language. `B_mem`, its operator support, source/boundary charges, and `Q_mem -> Q_norm -> B_gamma` links are explicit rows with units/source/projection blockers rather than hand-waved closure.",
                "",
                "**Claim discipline:** no local-GR, R10, PPN, clock, orbit, scalaron, beta, gamma, Newton, GR-limit, or public evidence claim is made. Private closure remains private closure.",
                "",
                "## Source Register",
                md_table(rows_by_name["source_register"], ["source_id", "source_path", "path_exists", "found_needles", "source_pass", "role"]),
                "",
                "## Bmem Reentry Audit",
                md_table(rows_by_name["bmem_reentry_audit"], ["audit_id", "test", "required_new_evidence", "current_evidence", "result_status", "blocking_marker"]),
                "",
                "## Bmem Finite Row",
                md_table(rows_by_name["bmem_finite_row"], ["row_id", "quantity", "row_role", "numeric_value_or_theorem_zero", "units", "parent_owner_source", "observable_map", "current_status"]),
                "",
                "## Qnorm Link Rows",
                md_table(rows_by_name["qnorm_link_rows"], ["link_id", "quantity", "formula", "required_inputs", "status", "blocking_marker"]),
                "",
                "## Observable Gate",
                md_table(rows_by_name["observable_gate"], ["gate_id", "arena", "map_formula", "required_bundle", "status", "claim_pass"]),
                "",
                "## Dry Run",
                md_table(rows_by_name["dryrun_results"], ["case_id", "case_description", "missing_requirements", "result_status", "blocking_markers", "pass_fail"]),
                "",
                "## Decision Ledger",
                md_table(rows_by_name["decision_ledger"], ["decision_id", "decision", "rationale", "next_action", "status"]),
                "",
                "## Next Target",
                md_table(rows_by_name["next_target"], ["route_id", "selection_status", "target_file", "target_script", "objective", "success_condition", "do_not_do"]),
                "",
                "## Validation",
                md_table(rows_by_name["validation"], ["check_id", "status", "detail"]),
                "",
            ]
        ),
        encoding="utf-8",
    )


def main() -> None:
    remove_pycache()
    rows_by_name: dict[str, list[dict[str, Any]]] = {
        "source_register": source_register_rows(),
        "bmem_reentry_audit": bmem_reentry_audit_rows(),
        "bmem_finite_row": bmem_finite_rows(),
        "qnorm_link_rows": qnorm_link_rows(),
        "observable_gate": observable_gate_rows(),
        "dryrun_results": dryrun_rows(),
        "decision_ledger": decision_rows(),
        "next_target": next_target_rows(),
    }

    for name, rows in rows_by_name.items():
        write_csv(OUTPUTS[name], rows)

    rows_by_name["branch_copies"] = branch_copy_rows()
    write_csv(OUTPUTS["branch_copies"], rows_by_name["branch_copies"])

    rows_by_name["validation"] = validation_rows(rows_by_name)
    write_csv(OUTPUTS["validation"], rows_by_name["validation"])
    write_doc(rows_by_name)
    remove_pycache()

    print(f"wrote {DOC}")
    for name, path in OUTPUTS.items():
        print(f"wrote {name}: {path}")
    for copy_key, copy_path in BRANCH_COPIES.items():
        print(f"copied {copy_key}: {copy_path}")


if __name__ == "__main__":
    main()

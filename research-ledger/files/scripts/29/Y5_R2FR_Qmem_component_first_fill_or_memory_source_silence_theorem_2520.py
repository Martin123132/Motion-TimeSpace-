from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
BRANCH_ID = "MTS_R2FR_QMEM_COMPONENT_FIRST_FILL_2520"
CHECKPOINT_ID = "2520"
DOC = ROOT / "2520-Y5-R2FR-Qmem-component-first-fill-or-memory-source-silence-theorem.md"
MTS_RESIDUALS = ROOT / "source-intake" / "mts_residuals"

OUTPUTS = {
    "source_register": MTS_RESIDUALS / "P8_Y5_NO_SHADOW_2520_SOURCE_REGISTER.csv",
    "qmem_zero_attempt": MTS_RESIDUALS / "P8_Y5_NO_SHADOW_2520_QMEM_ZERO_THEOREM_ATTEMPT.csv",
    "qmem_component_rows": MTS_RESIDUALS / "P8_Y5_NO_SHADOW_2520_QMEM_COMPONENT_ROWS.csv",
    "qmem_runner_schema": MTS_RESIDUALS / "P8_Y5_NO_SHADOW_2520_QMEM_RUNNER_SCHEMA.csv",
    "observable_gate": MTS_RESIDUALS / "P8_Y5_NO_SHADOW_2520_OBSERVABLE_GATE.csv",
    "dryrun_results": MTS_RESIDUALS / "P8_Y5_NO_SHADOW_2520_DRYRUN_RESULTS.csv",
    "decision_ledger": MTS_RESIDUALS / "P8_Y5_NO_SHADOW_2520_DECISION_LEDGER.csv",
    "next_target": MTS_RESIDUALS / "P8_Y5_NO_SHADOW_2520_NEXT_TARGET.csv",
    "branch_copies": MTS_RESIDUALS / "P8_Y5_NO_SHADOW_2520_BRANCH_COPIES.csv",
    "validation": MTS_RESIDUALS / "P8_Y5_BRR545_2520_VALIDATION.csv",
}

BRANCH_COPIES = {
    "qmem_zero_attempt": ROOT
    / "source-intake"
    / "local_bounds"
    / "Qmem_zero_theorem_attempt_2520_NONCLAIM.csv",
    "qmem_component_rows": ROOT
    / "source-intake"
    / "beta-source"
    / "docs"
    / "Qmem_component_rows_2520_NONCLAIM.csv",
    "qmem_runner_schema": ROOT
    / "source-intake"
    / "rab-sector"
    / "acquisition-queue"
    / "JR2520_QMEM_RUNNER_SCHEMA_NONCLAIM.csv",
    "next_target": ROOT
    / "source-intake"
    / "rab-sector"
    / "acquisition-queue"
    / "JR2520_NEXT_TARGET_NONCLAIM.csv",
}

SOURCE_SPECS = [
    {
        "source_id": "SRC2520_0_2519_next",
        "path": "source-intake/mts_residuals/P8_Y5_NO_SHADOW_2519_NEXT_TARGET.csv",
        "needles": ["NEXT2519_0_selected", "Q_mem"],
        "role": "authoritative handoff to Q_mem theorem or component fill",
    },
    {
        "source_id": "SRC2520_1_2519_qnorm_link",
        "path": "source-intake/mts_residuals/P8_Y5_NO_SHADOW_2519_QNORM_LINK_ROWS.csv",
        "needles": ["QMEM2519_0_Qmem", "MISSING_QMEM_COMPONENT_VALUES"],
        "role": "current symbolic Q_mem feed and missing component marker",
    },
    {
        "source_id": "SRC2520_2_2519_bmem_row",
        "path": "source-intake/mts_residuals/P8_Y5_NO_SHADOW_2519_BMEM_FINITE_ROW.csv",
        "needles": ["BMEM2519_0_Bmem", "MISSING_NO_XR_VERTEX_OR_VALUE"],
        "role": "B_mem limb of Q_mem remains finite blocked input",
    },
    {
        "source_id": "SRC2520_3_2519_validation",
        "path": "source-intake/mts_residuals/P8_Y5_BRR545_2519_VALIDATION.csv",
        "needles": ["VAL2519_OVERALL", "PASS"],
        "role": "previous checkpoint validation gate",
    },
    {
        "source_id": "SRC2520_4_1348_memory_operator",
        "path": "1348-Y5-R10-RAB-memory-branch-extremum-and-operator-signature-or-closure.md",
        "needles": ["BEXT1348_5_verdict", "OPS1348_5_verdict"],
        "role": "conditional B_mem/operator route and current parent-ownership failure",
    },
    {
        "source_id": "SRC2520_5_1301_stress_split",
        "path": "source-intake/mts_residuals/P8_Y5_R10_1301_MEMORY_STRESS_SPLIT_LEDGER.csv",
        "needles": ["MSS1301_1_memory_kinetic_stress", "MSS1301_3_boundary_source_bath"],
        "role": "memory kinetic/potential/source/bath stress split",
    },
    {
        "source_id": "SRC2520_6_1302_nohair_requirements",
        "path": "source-intake/mts_residuals/P8_Y5_R10_1302_MEMORY_STRESS_NOHAIR_REQUIREMENTS.csv",
        "needles": ["NHM1302_0_operator_owner", "NHM1302_5_observable_projection"],
        "role": "no-hair theorem required premises",
    },
    {
        "source_id": "SRC2520_7_1303_nohair_attempt",
        "path": "source-intake/mts_residuals/P8_Y5_R10_1303_MEMORY_STRESS_NOHAIR_ATTEMPT.csv",
        "needles": ["NHA1303_5_verdict", "FAIL_CURRENT_CORPUS_STAGE_BOUND_INPUTS"],
        "role": "best current memory no-hair attempt fails to claim",
    },
    {
        "source_id": "SRC2520_8_1372_qnorm",
        "path": "1372-Y5-R10-RAB-fixed-L0-double-zero-local-residual-theorem-or-Qnorm-bound.md",
        "needles": ["QNB1372_3_memory_stress", "QGF1372_1_gamma_bound"],
        "role": "Q_mem as component of Q_norm and PPN gamma feed",
    },
    {
        "source_id": "SRC2520_9_1373_qnorm_contracts",
        "path": "source-intake/mts_residuals/P8_Y5_R10_1373_QNORM_COMPONENT_FIRST_FILL_CONTRACTS.csv",
        "needles": ["QFF1373_2_Q_mem", "FILL_CONTRACT_READY_VALUES_MISSING"],
        "role": "older Q_mem fill contract used as guardrail",
    },
    {
        "source_id": "SRC2520_10_1591_theorem_attempt",
        "path": "source-intake/mts_residuals/P8_Y5_PARENT_QLOC_1591_CDB_MEMORY_THEOREM_ATTEMPT.csv",
        "needles": ["CMA1591_5_memory_source_stress", "MEMORY_STRESS_RETAINED"],
        "role": "fixed-L0 branch keeps memory/source stress active",
    },
    {
        "source_id": "SRC2520_11_1969_memory_mixing",
        "path": "source-intake/mts_residuals/P8_Y5_PARENT_QLOC_1969_MEMORY_DERIVATION.csv",
        "needles": ["MEM1969_2_written_branch_direct_mixing", "PARTIAL_ZERO_TOTAL_MIXING_NOT_CLOSED"],
        "role": "direct memory Ricci mixing partial-zero and remaining indirect channels",
    },
    {
        "source_id": "SRC2520_12_1978_mass_gap",
        "path": "source-intake/mts_residuals/P8_Y5_PARENT_QLOC_1978_MEMORY_MASS_GAP_PACK.csv",
        "needles": ["MG1978_5_inverse_bound", "MASS_GAP_PACK_NOT_CLAIMABLE"],
        "role": "memory Hessian inverse and missing mass-gap values",
    },
    {
        "source_id": "SRC2520_13_1980_positivity",
        "path": "source-intake/mts_residuals/P8_Y5_PARENT_QLOC_1980_MEMORY_POSITIVITY_LEMMA.csv",
        "needles": ["LEM1980_3_Gm", "CLOSURE_FORK_REQUIRED_IF_UNSIGNED"],
        "role": "conditional positivity theorem and closure fork if parent signs remain unsigned",
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
        for key in row:
            if key not in fieldnames:
                fieldnames.append(key)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def csv_rows_parse(path: Path) -> tuple[bool, int, str]:
    try:
        with path.open(newline="", encoding="utf-8") as handle:
            rows = list(csv.DictReader(handle))
        return bool(rows), len(rows), "OK"
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
        path = ROOT / spec["path"]
        text = read_text(path)
        found = [needle for needle in spec["needles"] if needle in text]
        rows.append(
            base_row(
                source_id=spec["source_id"],
                source_path=spec["path"],
                path_exists=path.exists(),
                required_needles=";".join(spec["needles"]),
                found_needles=";".join(found),
                role=spec["role"],
                source_pass=path.exists() and len(found) == len(spec["needles"]),
            )
        )
    return rows


def qmem_zero_attempt_rows() -> list[dict[str, Any]]:
    entries = [
        {
            "attempt_id": "QZ2520_0_conditional_theorem",
            "theorem_piece": "conditional Q_mem zero theorem skeleton",
            "statement": "If H_m is parent-owned/coercive, m is constant at the selected local branch, B_mem=J_mem=Q_boundary_mem=0, and potential drift is pure background subtraction, then Q_mem=0.",
            "status": "CONDITIONAL_THEOREM_FORMULATED",
            "blocking_gap": "premises are not all parent-signed in current corpus",
            "evidence_path": "source-intake/mts_residuals/P8_Y5_R10_1302_MEMORY_STRESS_NOHAIR_REQUIREMENTS.csv;source-intake/mts_residuals/P8_Y5_PARENT_QLOC_1980_MEMORY_POSITIVITY_LEMMA.csv",
            "effect": "useful target, not a claim",
        },
        {
            "attempt_id": "QZ2520_1_operator_owner",
            "theorem_piece": "H_m parent-owned self-adjoint operator",
            "statement": "memory Euler/Hessian operator must come from the parent action with domain and boundary conditions",
            "status": "NOT_DERIVED",
            "blocking_gap": "1348/1303 retain parent owner/domain/sign gaps",
            "evidence_path": "1348-Y5-R10-RAB-memory-branch-extremum-and-operator-signature-or-closure.md;source-intake/mts_residuals/P8_Y5_R10_1303_MEMORY_STRESS_NOHAIR_ATTEMPT.csv",
            "effect": "positive no-hair cannot activate",
        },
        {
            "attempt_id": "QZ2520_2_positive_gap",
            "theorem_piece": "coercive memory spectral floor",
            "statement": "G_m := Z_min lambda_1(D_loc)+M2_min-Eta_H > 0 gives ||H_m^-1|| <= 1/G_m",
            "status": "CONDITIONAL_READY_VALUES_MISSING",
            "blocking_gap": "Z_min, M2_min, lambda_1(D_loc), Eta_H and source/boundary correction norms are missing",
            "evidence_path": "source-intake/mts_residuals/P8_Y5_PARENT_QLOC_1978_MEMORY_MASS_GAP_PACK.csv;source-intake/mts_residuals/P8_Y5_PARENT_QLOC_1980_MEMORY_POSITIVITY_LEMMA.csv",
            "effect": "turns sign debt into a concrete bound row",
        },
        {
            "attempt_id": "QZ2520_3_source_current_silence",
            "theorem_piece": "J_mem source/current zero",
            "statement": "ordinary local exterior must not source the memory branch through matter, bath, readout, history, or domain wall terms",
            "status": "NOT_DERIVED",
            "blocking_gap": "1302/1303 keep source silence missing; 1011 response doublet source-current zero fails current corpus",
            "evidence_path": "source-intake/mts_residuals/P8_Y5_R10_1302_MEMORY_STRESS_NOHAIR_REQUIREMENTS.csv;source-intake/mts_residuals/P8_Y5_R10_1011_RESPONSED_DOUBLET_THEOREM_ATTEMPT.csv",
            "effect": "J_mem must remain finite or bounded",
        },
        {
            "attempt_id": "QZ2520_4_boundary_silence",
            "theorem_piece": "Q_boundary_mem boundary/no-flux zero",
            "statement": "boundary flux, zero mode, and topological memory charge vanish or reduce to source-independent background",
            "status": "NOT_DERIVED",
            "blocking_gap": "boundary primitive and local no-flux conditions are still unsigned",
            "evidence_path": "source-intake/mts_residuals/P8_Y5_R10_1302_MEMORY_STRESS_NOHAIR_REQUIREMENTS.csv;source-intake/mts_residuals/P8_Y5_R10_1303_MEMORY_STRESS_NOHAIR_ATTEMPT.csv",
            "effect": "boundary contribution must remain explicit in Q_mem/Q_bdy",
        },
        {
            "attempt_id": "QZ2520_5_potential_drift",
            "theorem_piece": "memory potential/background subtraction",
            "statement": "constant V_R(m_*) is harmless only if it is EH/Lambda-compatible subtraction and X_B/m drift is killed or bounded",
            "status": "NOT_DERIVED",
            "blocking_gap": "subtraction owner and drift-zero clauses are missing",
            "evidence_path": "source-intake/mts_residuals/P8_Y5_R10_1301_MEMORY_STRESS_SPLIT_LEDGER.csv;source-intake/mts_residuals/P8_Y5_R10_1302_MEMORY_STRESS_NOHAIR_REQUIREMENTS.csv",
            "effect": "K_mem_drift remains a Q_mem component",
        },
        {
            "attempt_id": "QZ2520_6_Bmem_vertex",
            "theorem_piece": "B_mem curvature/memory vertex zero",
            "statement": "direct displayed Ricci mixing is conditionally absent, but total B_mem includes indirect X_B/source/bath/boundary channels",
            "status": "PARTIAL_DIRECT_ZERO_TOTAL_OPEN",
            "blocking_gap": "2519 keeps B_mem finite blocked; 1969 says total mixing not closed",
            "evidence_path": "source-intake/mts_residuals/P8_Y5_NO_SHADOW_2519_BMEM_FINITE_ROW.csv;source-intake/mts_residuals/P8_Y5_PARENT_QLOC_1969_MEMORY_DERIVATION.csv",
            "effect": "B_mem remains in Q_mem runner rows",
        },
        {
            "attempt_id": "QZ2520_7_verdict",
            "theorem_piece": "Q_mem=0 local memory/source-stress theorem",
            "statement": "QZ2520_1 through QZ2520_6 must close together",
            "status": "QMEM_ZERO_THEOREM_NOT_DERIVED_STAGE_COMPONENT_ROWS",
            "blocking_gap": "operator owner, source current, boundary, drift, total B_mem and arena projection gaps remain",
            "evidence_path": "aggregate_QZ2520_0_to_QZ2520_6",
            "effect": "finite Q_mem component rows become the honest default",
        },
    ]
    return [base_row(score_ready=False, valid_prediction_row=False, **entry) for entry in entries]


def qmem_component_rows() -> list[dict[str, Any]]:
    entries = [
        {
            "component_id": "QMC2520_0_Aref_norm",
            "quantity": "A_ref;norm_domain",
            "component_role": "normalization and local domain measure",
            "formula_or_bound": "Q_mem is dimensionless only after A_ref and the local norm/domain are fixed",
            "units": "area/action_normalization_or_declared_dimensionless_convention",
            "required_inputs": "A_ref;D_loc;measure;norm;frame/readout convention",
            "current_status": "MISSING_NORM_DOMAIN_CONVENTION",
            "observable_links": "Q_norm;PPN_gamma",
        },
        {
            "component_id": "QMC2520_1_Nkin",
            "quantity": "N_kin",
            "component_role": "kinetic stress operator multiplier",
            "formula_or_bound": "Kinetic contribution <= A_ref^-1 N_kin K_mem_kin",
            "units": "dimensionless_or_operator_norm_units",
            "required_inputs": "stress-to-Qnorm operator norm; local frame; trace/readout convention",
            "current_status": "MISSING_OPERATOR_NORM",
            "observable_links": "Q_mem;Q_norm",
        },
        {
            "component_id": "QMC2520_2_Kmem_kin",
            "quantity": "K_mem_kin",
            "component_role": "memory kinetic stress magnitude",
            "formula_or_bound": "K_mem_kin ~ ||Z_m h^{ij} partial_i m partial_j m||_D or theorem-zero if constant m no-hair closes",
            "units": "stress_or_action_density_units",
            "required_inputs": "Z_m bounds; gradient amplitude; H_m inverse/nohair theorem; source path",
            "current_status": "MISSING_ZM_GRADIENT_OR_NOHAIR",
            "observable_links": "Q_mem;clock;orbit",
        },
        {
            "component_id": "QMC2520_3_Npot",
            "quantity": "N_pot",
            "component_role": "potential/drift stress operator multiplier",
            "formula_or_bound": "Potential contribution <= A_ref^-1 N_pot K_mem_drift",
            "units": "dimensionless_or_operator_norm_units",
            "required_inputs": "volume-to-residual map; background subtraction convention",
            "current_status": "MISSING_POTENTIAL_OPERATOR_NORM",
            "observable_links": "Q_mem;PPN_gamma",
        },
        {
            "component_id": "QMC2520_4_Kmem_drift",
            "quantity": "K_mem_drift",
            "component_role": "nonconstant memory potential/background drift",
            "formula_or_bound": "K_mem_drift <= ||V_R(m;X_B)-V_ref||_D plus X_B/m branch drift corrections",
            "units": "stress_or_action_density_units",
            "required_inputs": "V_R functional; V_ref owner; Delta_m;X_B drift bound; subtraction source",
            "current_status": "MISSING_VR_SUBTRACTION_AND_DRIFT_BOUND",
            "observable_links": "Q_mem;local_GR",
        },
        {
            "component_id": "QMC2520_5_Nsrc",
            "quantity": "N_src",
            "component_role": "source-current operator multiplier",
            "formula_or_bound": "Source drive contribution <= A_ref^-1 N_src J_mem",
            "units": "dimensionless_or_operator_norm_units",
            "required_inputs": "source-to-residual map; body/readout normalization",
            "current_status": "MISSING_SOURCE_OPERATOR_NORM",
            "observable_links": "Q_mem;WEP;clock",
        },
        {
            "component_id": "QMC2520_6_Jmem",
            "quantity": "J_mem",
            "component_role": "memory source/current drive",
            "formula_or_bound": "J_mem=0 only if matter/bath/readout/history/domain-wall source silence is parent-derived; otherwise finite bound needed",
            "units": "memory_source_units",
            "required_inputs": "source-current zero theorem or finite body/source bound; source path",
            "current_status": "MISSING_SOURCE_SILENCE_THEOREM_OR_BOUND",
            "observable_links": "Q_mem;local_residual;WEP",
        },
        {
            "component_id": "QMC2520_7_Nbath",
            "quantity": "N_bath",
            "component_role": "curvature/bath drive operator multiplier",
            "formula_or_bound": "Curvature/bath contribution <= A_ref^-1 N_bath B_mem",
            "units": "dimensionless_or_operator_norm_units",
            "required_inputs": "B_mem-to-residual operator norm; range/source convention",
            "current_status": "MISSING_BMEM_OPERATOR_NORM",
            "observable_links": "Q_mem;R10;PPN_gamma",
        },
        {
            "component_id": "QMC2520_8_Bmem",
            "quantity": "B_mem",
            "component_role": "memory curvature/source bath vertex",
            "formula_or_bound": "B_mem remains finite unless new K_MTS owner or total mixing zero certificate appears",
            "units": "parent_action_units_for_delta_m_R_vertex",
            "required_inputs": "value/theorem-zero; units; parent source; normalization; R10/PPN/Qnorm map",
            "current_status": "MISSING_NO_XR_VERTEX_OR_VALUE",
            "observable_links": "Q_mem;R10;PPN_gamma",
        },
        {
            "component_id": "QMC2520_9_boundary",
            "quantity": "Q_boundary_mem",
            "component_role": "memory boundary/source leakage",
            "formula_or_bound": "boundary memory leakage must be theorem-zero or bounded and assigned to Q_mem/Q_bdy without double counting",
            "units": "boundary_flux_units",
            "required_inputs": "boundary primitive; domain; surface measure; no-flux theorem or finite bound",
            "current_status": "MISSING_BOUNDARY_FLUX_THEOREM_OR_BOUND",
            "observable_links": "Q_mem;Q_bdy;clock;orbit",
        },
        {
            "component_id": "QMC2520_10_Hm_inverse",
            "quantity": "H_m^-1;G_m",
            "component_role": "optional response amplitude envelope",
            "formula_or_bound": "If G_m=Z_min lambda_1(D_loc)+M2_min-Eta_H>0 then ||H_m^-1||<=1/G_m",
            "units": "operator_inverse_units",
            "required_inputs": "Z_min;lambda_1;M2_min;Eta_H;domain/source/boundary correction norms",
            "current_status": "FORMULA_READY_VALUES_MISSING",
            "observable_links": "Q_mem;B_mem amplitude;R10",
        },
        {
            "component_id": "QMC2520_11_Qmem_total",
            "quantity": "Q_mem",
            "component_role": "componentwise no-cancellation memory residual",
            "formula_or_bound": "Q_mem <= A_ref^-1 (N_kin K_mem_kin + N_pot K_mem_drift + N_src J_mem + N_bath B_mem) plus boundary allocation ledger",
            "units": "dimensionless_after_A_ref_normalization",
            "required_inputs": "all QMC2520_0 through QMC2520_10 with source paths and no double counting",
            "current_status": "FILL_CONTRACT_READY_VALUES_MISSING",
            "observable_links": "Q_norm;PPN_gamma;local_GR",
        },
    ]
    return [
        base_row(
            score_ready=False,
            valid_prediction_row=False,
            accepted_for_scoring=False,
            claim_pass=False,
            **entry,
        )
        for entry in entries
    ]


def qmem_runner_schema_rows() -> list[dict[str, Any]]:
    entries = [
        {
            "field_id": "QMS2520_0_quantity",
            "field_name": "quantity",
            "required_for": "all rows",
            "acceptance_rule": "must be one of A_ref,N_kin,K_mem_kin,N_pot,K_mem_drift,N_src,J_mem,N_bath,B_mem,Q_boundary_mem,H_m_inverse,Q_mem",
            "current_status": "SCHEMA_READY",
        },
        {
            "field_id": "QMS2520_1_value",
            "field_name": "numeric_value_or_theorem_zero",
            "required_for": "scored rows",
            "acceptance_rule": "finite numeric value with units or theorem-zero certificate with source path; symbolic-only rejects",
            "current_status": "MISSING_FOR_CURRENT_ROWS",
        },
        {
            "field_id": "QMS2520_2_units",
            "field_name": "units",
            "required_for": "scored rows",
            "acceptance_rule": "declared units must match Q_mem dimensionless normalization after A_ref",
            "current_status": "MISSING_OR_PLACEHOLDER_FOR_CURRENT_ROWS",
        },
        {
            "field_id": "QMS2520_3_source_path",
            "field_name": "parent_owner_source",
            "required_for": "all scored/theorem rows",
            "acceptance_rule": "local file path or external source string plus branch convention; missing source rejects",
            "current_status": "MISSING_FOR_CURRENT_ROWS",
        },
        {
            "field_id": "QMS2520_4_no_cancellation",
            "field_name": "component_allocation",
            "required_for": "Q_mem and Q_norm rows",
            "acceptance_rule": "each component bounded independently; boundary/source terms assigned once only",
            "current_status": "GUARD_READY_VALUES_MISSING",
        },
        {
            "field_id": "QMS2520_5_arena_map",
            "field_name": "observable_map",
            "required_for": "claim or comparator rows",
            "acceptance_rule": "Q_mem must map into Q_norm and then declared PPN/R10/clock/orbital residual lanes",
            "current_status": "MISSING_ARENA_PROJECTION_VALUES",
        },
    ]
    return [base_row(valid_for_claim=False, claim_allowed=False, **entry) for entry in entries]


def observable_gate_rows() -> list[dict[str, Any]]:
    entries = [
        {
            "gate_id": "QOG2520_0_Qnorm",
            "arena": "Q_norm residual budget",
            "map_formula": "Q_norm <= Q_alg + Q_cdb + Q_mem + Q_bdy + Q_trans + Q_proj",
            "required_bundle": "source-backed Q_mem plus other Q_i components with common norm/domain convention",
            "status": "BLOCKED_MISSING_QMEM_AND_OTHER_COMPONENT_VALUES",
            "claim_pass": False,
        },
        {
            "gate_id": "QOG2520_1_PPN_gamma",
            "arena": "PPN gamma/Cassini",
            "map_formula": "B_gamma <= (c^2/(2U_min)) N_G N_D Q_norm",
            "required_bundle": "U_min;N_G;N_D;sigma_gamma;all Q_i values",
            "status": "BLOCKED_MISSING_CQGAMMA_INPUTS",
            "claim_pass": False,
        },
        {
            "gate_id": "QOG2520_2_R10",
            "arena": "R10 short-range gravity",
            "map_formula": "B_mem,H_m_inverse,source charge -> alpha(lambda)",
            "required_bundle": "B_mem value/theorem; H_m range; source/test normalization; bound curve",
            "status": "BLOCKED_MISSING_BMEM_RANGE_AND_SOURCE_MAP",
            "claim_pass": False,
        },
        {
            "gate_id": "QOG2520_3_clocks",
            "arena": "clock/time residuals",
            "map_formula": "J_mem,K_mem_drift,boundary/readout -> clock residual vector",
            "required_bundle": "clock readout coupling; local source current; bounds",
            "status": "BLOCKED_MISSING_CLOCK_READOUT_PROJECTION",
            "claim_pass": False,
        },
        {
            "gate_id": "QOG2520_4_orbits",
            "arena": "orbital/Newtonian systems",
            "map_formula": "Q_mem/source/boundary stress -> orbital residual vector",
            "required_bundle": "body normalization; orbital projection; observed-GM convention",
            "status": "BLOCKED_MISSING_ORBITAL_PROJECTION",
            "claim_pass": False,
        },
        {
            "gate_id": "QOG2520_5_local_GR",
            "arena": "local GR/Newton recovery",
            "map_formula": "Q_mem=0 or Q_mem bounded plus other Q_i below all local gates",
            "required_bundle": "Q_mem theorem-zero or component bounds; CDB/boundary/transition/projector closure",
            "status": "BLOCKED_NO_LOCAL_GR_CLAIM",
            "claim_pass": False,
        },
    ]
    return [base_row(score_ready=False, accepted_for_scoring=False, **entry) for entry in entries]


def dryrun_rows() -> list[dict[str, Any]]:
    entries = [
        {
            "case_id": "DRY2520_0_positive_operator_only",
            "case_description": "claim Q_mem=0 from positive H_m without source/boundary silence",
            "missing_requirements": "J_mem=0;B_mem=0;Q_boundary_mem=0;potential drift subtraction;parent owner",
            "result_status": "REJECT",
            "blocking_markers": "NOHAIR_PREMISES_UNSIGNED",
            "pass_fail": "BLOCKED_NONCLAIM",
            "claim_pass": False,
        },
        {
            "case_id": "DRY2520_1_exterior_vacuum_source_zero",
            "case_description": "set J_mem=0 because ordinary matter is outside local vacuum",
            "missing_requirements": "matter/bath/readout/history/domain-wall source-current theorem",
            "result_status": "REJECT",
            "blocking_markers": "MISSING_SOURCE_SILENCE_THEOREM",
            "pass_fail": "BLOCKED_NONCLAIM",
            "claim_pass": False,
        },
        {
            "case_id": "DRY2520_2_direct_mixing_zero_as_total_Bmem_zero",
            "case_description": "use 1969 direct Ricci-mixing absence as total B_mem=0",
            "missing_requirements": "indirect X_B/source/bath/boundary/metric-composite channel closure",
            "result_status": "REJECT",
            "blocking_markers": "PARTIAL_DIRECT_ZERO_TOTAL_OPEN",
            "pass_fail": "BLOCKED_NONCLAIM",
            "claim_pass": False,
        },
        {
            "case_id": "DRY2520_3_numeric_Kmem_without_domain",
            "case_description": "score finite K_mem_kin without units/domain/A_ref",
            "missing_requirements": "units;A_ref;local norm;source path;operator map",
            "result_status": "REJECT",
            "blocking_markers": "MISSING_NORM_DOMAIN_CONVENTION",
            "pass_fail": "BLOCKED_NONCLAIM",
            "claim_pass": False,
        },
        {
            "case_id": "DRY2520_4_old_proxy_as_Qmem",
            "case_description": "use old compact-shell proxy or closure smoke as Q_mem value",
            "missing_requirements": "mapping to Q_mem units and source-normalization",
            "result_status": "REJECT",
            "blocking_markers": "DO_NOT_USE_PROXY_SCORING",
            "pass_fail": "BLOCKED_NONCLAIM",
            "claim_pass": False,
        },
        {
            "case_id": "DRY2520_5_future_complete_Qmem",
            "case_description": "future Q_mem row with all component values/theorem-zero certificates and source paths",
            "missing_requirements": "none in schema; evidence remains future",
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
            "decision_id": "DEC2520_0_theorem_status",
            "decision": "do not claim Q_mem=0",
            "rationale": "the no-hair theorem skeleton is clean, but source current, boundary, drift, B_mem and parent operator premises remain unsigned",
            "next_action": "stage component rows instead of using closure",
            "status": "ACTIVE",
        },
        {
            "decision_id": "DEC2520_1_partial_gain",
            "decision": "retain 1969 direct-mixing simplification as partial progress only",
            "rationale": "the displayed branch lacks direct m R_geom mixing, but indirect channels keep total B_mem open",
            "next_action": "separate direct-zero evidence from total B_mem runner rows",
            "status": "ACTIVE",
        },
        {
            "decision_id": "DEC2520_2_component_default",
            "decision": "Q_mem componentwise no-cancellation fill is now the default",
            "rationale": "Q_mem enters Q_norm and PPN gamma only through independently bounded pieces",
            "next_action": "attack J_mem/source-current silence first because it gates memory no-hair and source coupling",
            "status": "ACTIVE",
        },
        {
            "decision_id": "DEC2520_3_fibre_queue",
            "decision": "keep fibre B_h queued but do not jump there yet",
            "rationale": "Q_mem still has a live source-current coupling blocker after 2520",
            "next_action": "renumber fibre queue after the J_mem/source-current target",
            "status": "ACTIVE",
        },
    ]
    return [base_row(valid_for_claim=False, claim_allowed=False, **entry) for entry in entries]


def next_target_rows() -> list[dict[str, Any]]:
    entries = [
        {
            "route_id": "NEXT2520_0_selected",
            "selection_status": "selected",
            "target_file": "2521-Y5-R2FR-Jmem-source-current-zero-or-memory-drive-bound.md",
            "target_script": "scripts/Y5_R2FR_Jmem_source_current_zero_or_memory_drive_bound_2521.py",
            "objective": "try to derive J_mem=0 from parent matter/source descent and local exterior conditions; if not, create a finite memory-drive bound row with source normalization and arena projections",
            "success_condition": "J_mem is either theorem-zero with parent source-current evidence or remains a finite nonclaim drive with units, source paths, and Q_mem/PPN/clock/orbit links",
            "do_not_do": "do not set source current to zero by vacuum wording; do not use response-doublet symmetry unless parent-signed; do not claim local GR or PPN",
        },
        {
            "route_id": "NEXT2520_1_fibre_queue",
            "selection_status": "queued_after_Jmem",
            "target_file": "2522-Y5-R2FR-fibre-Bh-finite-row-or-hidden-visible-grammar-reentry.md",
            "target_script": "scripts/Y5_R2FR_fibre_Bh_finite_row_or_hidden_visible_grammar_reentry_2522.py",
            "objective": "classify fibre B_h with hidden-visible grammar reentry or finite fibre coefficient rows after the active memory source-current blocker is handled",
            "success_condition": "B_h has theorem-zero evidence or finite nonclaim Z_h/M2_h/B_h/C_h/source-charge rows",
            "do_not_do": "do not let memory closure erase fibre residuals",
        },
    ]
    return [base_row(valid_for_claim=False, claim_allowed=False, **entry) for entry in entries]


def branch_copy_rows() -> list[dict[str, Any]]:
    copy_specs = [
        ("qmem_zero_attempt", OUTPUTS["qmem_zero_attempt"], BRANCH_COPIES["qmem_zero_attempt"]),
        ("qmem_component_rows", OUTPUTS["qmem_component_rows"], BRANCH_COPIES["qmem_component_rows"]),
        ("qmem_runner_schema", OUTPUTS["qmem_runner_schema"], BRANCH_COPIES["qmem_runner_schema"]),
        ("next_target", OUTPUTS["next_target"], BRANCH_COPIES["next_target"]),
    ]
    rows: list[dict[str, Any]] = []
    for copy_id, source, destination in copy_specs:
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(source, destination)
        ok, count, message = csv_rows_parse(destination)
        rows.append(
            base_row(
                copy_id=copy_id,
                source=str(source.relative_to(ROOT)),
                destination=str(destination.relative_to(ROOT)),
                copied=destination.exists(),
                parse_ok=ok,
                row_count=count,
                parse_message=message,
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
            for key in (
                "valid_for_claim",
                "claim_allowed",
                "score_ready",
                "valid_prediction_row",
                "accepted_for_scoring",
                "claim_pass",
            ):
                if key in row and not falsey(row[key]):
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
    zero_rows = rows_by_name["qmem_zero_attempt"]
    component_rows = rows_by_name["qmem_component_rows"]

    add("VAL2520_00_sources_exist", all(str(row["path_exists"]) == "True" for row in source_rows))
    add("VAL2520_01_source_needles", all(str(row["source_pass"]) == "True" for row in source_rows))
    add(
        "VAL2520_02_conditional_theorem_written",
        any(row["attempt_id"] == "QZ2520_0_conditional_theorem" for row in zero_rows),
        "conditional Q_mem zero theorem skeleton is recorded",
    )
    add(
        "VAL2520_03_zero_theorem_not_promoted",
        any(
            row["attempt_id"] == "QZ2520_7_verdict"
            and row["status"] == "QMEM_ZERO_THEOREM_NOT_DERIVED_STAGE_COMPONENT_ROWS"
            for row in zero_rows
        ),
        "Q_mem zero remains unclaimed",
    )
    add(
        "VAL2520_04_component_bundle_complete",
        all(
            any(row["component_id"] == required for row in component_rows)
            for required in [
                "QMC2520_0_Aref_norm",
                "QMC2520_2_Kmem_kin",
                "QMC2520_4_Kmem_drift",
                "QMC2520_6_Jmem",
                "QMC2520_8_Bmem",
                "QMC2520_11_Qmem_total",
            ]
        ),
        "Q_mem component rows include norm, kinetic, drift, source, B_mem and total rows",
    )
    add(
        "VAL2520_05_component_rows_nonclaim",
        all(str(row["accepted_for_scoring"]) == "False" and str(row["claim_pass"]) == "False" for row in component_rows),
        "all Q_mem component rows are blocked for scoring",
    )
    add(
        "VAL2520_06_runner_schema_ready",
        len(rows_by_name["qmem_runner_schema"]) == 6
        and any(row["field_id"] == "QMS2520_4_no_cancellation" for row in rows_by_name["qmem_runner_schema"]),
        "runner schema includes no-cancellation guard",
    )
    add(
        "VAL2520_07_observable_gates_blocked",
        all(str(row["claim_pass"]) == "False" and str(row["status"]).startswith("BLOCKED") for row in rows_by_name["observable_gate"]),
        "Qnorm/PPN/R10/clock/orbit/local-GR gates remain blocked",
    )
    add(
        "VAL2520_08_dryruns_block_bad_rows",
        all(str(row["claim_pass"]) == "False" for row in rows_by_name["dryrun_results"])
        and all(str(row["result_status"]) in {"REJECT", "WOULD_ACCEPT_SCHEMA_IF_REAL_FILES_AND_VALUES_EXIST"} for row in rows_by_name["dryrun_results"]),
        "positive-operator-only, source-vacuum, direct-zero, proxy and incomplete numeric cases do not score",
    )
    add(
        "VAL2520_09_next_target_Jmem",
        any(row["route_id"] == "NEXT2520_0_selected" and "Jmem-source-current" in row["target_file"] for row in rows_by_name["next_target"]),
        "J_mem source-current zero or bound selected next",
    )
    add("VAL2520_10_no_claim_flags", no_claim_flags(rows_by_name))
    add(
        "VAL2520_11_branch_copies",
        all(str(row["copied"]) == "True" and str(row["parse_ok"]) == "True" for row in rows_by_name["branch_copies"]),
    )
    formalization = ROOT.parent / "formalization-workbench"
    formalization_hits = list(formalization.rglob("*2520*")) if formalization.exists() else []
    add(
        "VAL2520_12_no_formalization_artifacts",
        len(formalization_hits) == 0,
        ";".join(str(path) for path in formalization_hits),
    )
    add("VAL2520_13_pycache_absent", not (Path(__file__).resolve().parent / "__pycache__").exists())

    for name, path in OUTPUTS.items():
        if name == "validation":
            continue
        ok, count, message = csv_rows_parse(path)
        add(f"VAL2520_CSV_{path.stem}", ok, f"{message}; rows={count}")
    for key, path in BRANCH_COPIES.items():
        ok, count, message = csv_rows_parse(path)
        add(f"VAL2520_COPY_CSV_{key}", ok, f"{message}; rows={count}")

    overall = all(row["status"] == "PASS" for row in checks)
    checks.append(
        base_row(
            check_id="VAL2520_OVERALL",
            status="PASS" if overall else "FAIL",
            detail="2520 formulates the conditional Q_mem zero theorem, refuses to promote it, stages componentwise Q_mem rows, and selects J_mem source-current zero/bound next.",
            valid_for_claim=False,
            claim_allowed=False,
        )
    )
    return checks


def write_doc(rows_by_name: dict[str, list[dict[str, Any]]]) -> None:
    DOC.write_text(
        "\n".join(
            [
                "# 2520 - Qmem Component First Fill or Memory Source Silence Theorem",
                "",
                "**Current verdict:** the clean theorem route exists only conditionally: `Q_mem=0` follows if the memory operator is parent-owned/coercive and all source, boundary, drift, and `B_mem` drives are killed. Current MTS does not yet own those clauses.",
                "",
                "**Main gain:** `Q_mem` is no longer a foggy word. It is now split into concrete rows for `A_ref`, `N_kin`, `K_mem_kin`, `N_pot`, `K_mem_drift`, `N_src`, `J_mem`, `N_bath`, `B_mem`, boundary allocation, `H_m^-1`, and total `Q_mem`.",
                "",
                "**Claim discipline:** no local-GR, Newton, PPN, R10, clock, orbit, source-current, memory no-hair, or public evidence claim is made. The partial direct-mixing zero from 1969 is retained only as partial progress.",
                "",
                "## Source Register",
                md_table(rows_by_name["source_register"], ["source_id", "source_path", "path_exists", "found_needles", "source_pass", "role"]),
                "",
                "## Qmem Zero Theorem Attempt",
                md_table(rows_by_name["qmem_zero_attempt"], ["attempt_id", "theorem_piece", "statement", "status", "blocking_gap", "effect"]),
                "",
                "## Qmem Component Rows",
                md_table(rows_by_name["qmem_component_rows"], ["component_id", "quantity", "component_role", "formula_or_bound", "required_inputs", "current_status", "observable_links"]),
                "",
                "## Runner Schema",
                md_table(rows_by_name["qmem_runner_schema"], ["field_id", "field_name", "required_for", "acceptance_rule", "current_status"]),
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
        "qmem_zero_attempt": qmem_zero_attempt_rows(),
        "qmem_component_rows": qmem_component_rows(),
        "qmem_runner_schema": qmem_runner_schema_rows(),
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
    for key, path in BRANCH_COPIES.items():
        print(f"copied {key}: {path}")


if __name__ == "__main__":
    main()

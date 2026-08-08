from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
BRANCH_ID = "MTS_R2FR_MATTER_MEMORY_DIRECT_COUPLING_2522"
CHECKPOINT_ID = "2522"
DOC = ROOT / "2522-Y5-R2FR-matter-memory-direct-coupling-zero-or-Jdirect-bound.md"
MTS_RESIDUALS = ROOT / "source-intake" / "mts_residuals"

OUTPUTS = {
    "source_register": MTS_RESIDUALS / "P8_Y5_NO_SHADOW_2522_SOURCE_REGISTER.csv",
    "direct_zero_audit": MTS_RESIDUALS / "P8_Y5_NO_SHADOW_2522_MATTER_MEMORY_DIRECT_ZERO_AUDIT.csv",
    "argument_list_gate": MTS_RESIDUALS / "P8_Y5_NO_SHADOW_2522_MATTER_ARGUMENT_LIST_GATE.csv",
    "jdirect_bound_rows": MTS_RESIDUALS / "P8_Y5_NO_SHADOW_2522_JDIRECT_BOUND_ROWS.csv",
    "observable_gate": MTS_RESIDUALS / "P8_Y5_NO_SHADOW_2522_OBSERVABLE_GATE.csv",
    "dryrun_results": MTS_RESIDUALS / "P8_Y5_NO_SHADOW_2522_DRYRUN_RESULTS.csv",
    "decision_ledger": MTS_RESIDUALS / "P8_Y5_NO_SHADOW_2522_DECISION_LEDGER.csv",
    "next_target": MTS_RESIDUALS / "P8_Y5_NO_SHADOW_2522_NEXT_TARGET.csv",
    "branch_copies": MTS_RESIDUALS / "P8_Y5_NO_SHADOW_2522_BRANCH_COPIES.csv",
    "validation": MTS_RESIDUALS / "P8_Y5_BRR545_2522_VALIDATION.csv",
}

BRANCH_COPIES = {
    "direct_zero_audit": ROOT
    / "source-intake"
    / "local_bounds"
    / "Matter_memory_direct_zero_audit_2522_NONCLAIM.csv",
    "jdirect_bound_rows": ROOT
    / "source-intake"
    / "beta-source"
    / "docs"
    / "Jdirect_matter_bound_rows_2522_NONCLAIM.csv",
    "argument_list_gate": ROOT
    / "source-intake"
    / "rab-sector"
    / "acquisition-queue"
    / "JR2522_MATTER_ARGUMENT_LIST_GATE_NONCLAIM.csv",
    "next_target": ROOT
    / "source-intake"
    / "rab-sector"
    / "acquisition-queue"
    / "JR2522_NEXT_TARGET_NONCLAIM.csv",
}

SOURCE_SPECS = [
    {
        "source_id": "SRC2522_0_2521_next",
        "path": "source-intake/mts_residuals/P8_Y5_NO_SHADOW_2521_NEXT_TARGET.csv",
        "needles": ["NEXT2521_0_selected", "Jdirect"],
        "role": "authoritative 2521 handoff to direct matter-memory coupling gate",
    },
    {
        "source_id": "SRC2522_1_2521_drive_rows",
        "path": "source-intake/mts_residuals/P8_Y5_NO_SHADOW_2521_JMEM_DRIVE_BOUND_ROWS.csv",
        "needles": ["JDRV2521_1_direct_matter", "MISSING_MATTER_MBLIND_DESCENT"],
        "role": "current direct matter-to-memory drive blocker",
    },
    {
        "source_id": "SRC2522_2_2521_contract",
        "path": "source-intake/mts_residuals/P8_Y5_NO_SHADOW_2521_SOURCE_CURRENT_DESCENT_CONTRACT.csv",
        "needles": ["SCC2521_0_define_direct_Jmem", "DEFINITION_READY_ZERO_UNSIGNED"],
        "role": "direct J_mem definition and zero condition from 2521",
    },
    {
        "source_id": "SRC2522_3_2521_validation",
        "path": "source-intake/mts_residuals/P8_Y5_BRR545_2521_VALIDATION.csv",
        "needles": ["VAL2521_OVERALL", "PASS"],
        "role": "previous checkpoint validation gate",
    },
    {
        "source_id": "SRC2522_4_2486_matter_descent",
        "path": "source-intake/mts_residuals/P8_Y5_FIELD_QUOTIENT_2486_MATTER_DESCENT_GATE.csv",
        "needles": ["MD2486_0_chain_rule", "EXACT_CONDITIONAL"],
        "role": "conditional matter descent theorem shape",
    },
    {
        "source_id": "SRC2522_5_2486_doc",
        "path": "2486-Y5-R2FR-parent-field-sort-and-quotient-map-signature-or-residual-owner-split.md",
        "needles": ["THM2486_1_matter_blindness", "GATE2486_3_matter_descent"],
        "role": "matter blindness conditional theorem and blocked claim gate",
    },
    {
        "source_id": "SRC2522_6_2487_doc",
        "path": "2487-Y5-R2FR-observed-coframe-functor-and-vertical-generator-certificate-or-DObs-leak-row.md",
        "needles": ["NS2487_3_current_verdict", "NO_SHADOW_ZERO_NOT_DERIVED_CURRENT_CORPUS"],
        "role": "observed coframe/no-shadow readout remains unsigned",
    },
    {
        "source_id": "SRC2522_7_1427_signature",
        "path": "1427-Y5-R10-RAB-parent-action-signature-or-branch-locked-WEP-input-manifest.md",
        "needles": ["SIG1427_0_action_shape", "DECLARED_CLOSURE_CANDIDATE_NOT_DERIVED"],
        "role": "ordinary matter action signature closure candidate only",
    },
    {
        "source_id": "SRC2522_8_2508_no_slot",
        "path": "source-intake/mts_residuals/P8_Y5_NO_SHADOW_2508_NO_SOURCE_ONLY_SLOT_PROOF_ATTEMPT.csv",
        "needles": ["NSP2508_7_verdict", "NO_SOURCE_ONLY_SLOT_PROOF_NOT_PARENT_DERIVED"],
        "role": "no source-only slot theorem not parent-derived",
    },
    {
        "source_id": "SRC2522_9_2508_gates",
        "path": "source-intake/mts_residuals/P8_Y5_NO_SHADOW_2508_NO_SOURCE_SLOT_THEOREM_GATES.csv",
        "needles": ["GATE2508_6_theorem", "CLAIM_BLOCKED"],
        "role": "theorem gates blocking source-slot promotion",
    },
    {
        "source_id": "SRC2522_10_2509_runner",
        "path": "source-intake/mts_residuals/P8_Y5_NO_SHADOW_2509_SOURCE_WEIGHT_RESIDUAL_RUNNER_STATUS.csv",
        "needles": ["SWR2509_0_core_vector", "RUNNER_STATUS_NONEXECUTABLE_NEXT_TARGET"],
        "role": "source-weight residual runner remains nonexecutable",
    },
    {
        "source_id": "SRC2522_11_2503_selector",
        "path": "2503-Y5-R2FR-worldtube-Hilbert-source-selector-and-zero-boundary-flux-or-R-eq-fill.md",
        "needles": ["SCA2503_4_extra_channels", "EXTRA_CHANNEL_SILENCE_NOT_DERIVED"],
        "role": "extra/memory/source channels not silenced by Hilbert selector",
    },
    {
        "source_id": "SRC2522_12_2466_hilbert_current",
        "path": "source-intake/mts_residuals/P8_Y5_SOURCE_BRIDGE_2466_HILBERT_CURRENT_DESCENT.csv",
        "needles": ["HIL2466_4_matter_A_coupling", "MISSING_UNIFICATION_OF_COUPLINGS"],
        "role": "Hilbert current bridge warns direct A/matter coupling must reduce universally",
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


def direct_zero_audit_rows() -> list[dict[str, Any]]:
    entries = [
        {
            "audit_id": "JDZ2522_0_definition",
            "claim_piece": "direct matter-memory source definition",
            "formal_statement": "J_direct_matter := ||delta S_matter/delta m|| at fixed public metric/coframe, matter fields, and pre-readout variation order",
            "result": "DEFINITION_LOCKED",
            "blocking_gap": "definition does not by itself prove zero",
            "effect": "separates direct matter coupling from Hilbert source mass and readout re-entry",
        },
        {
            "audit_id": "JDZ2522_1_chain_rule_zero",
            "claim_piece": "q-basic matter descent",
            "formal_statement": "If S_matter=Sbar[psi,e_obs(q(Phi)),theta_obs(q(Phi)),c_vis(q)] and v_m in ker(Dq), then delta_v_m S_matter=0",
            "result": "EXACT_CONDITIONAL_THEOREM",
            "blocking_gap": "q_parent, v_m, q-basic e_obs/theta_obs and visible coefficient descent are not simultaneously parent-signed",
            "effect": "direct zero route remains mathematically clean",
        },
        {
            "audit_id": "JDZ2522_2_parent_argument_list",
            "claim_piece": "matter action has no m or hidden-memory argument",
            "formal_statement": "Arg(S_matter) excludes m, X_B, R_AB, hidden markers, domain walls, source labels, and memory-specific coefficients before variation",
            "result": "NOT_PARENT_DERIVED",
            "blocking_gap": "1427 records this as a closure candidate and 2508 blocks no-source-slot promotion",
            "effect": "direct m-blind descent cannot be claimed",
        },
        {
            "audit_id": "JDZ2522_3_source_prefactor",
            "claim_piece": "no m-dependent source/action prefactor",
            "formal_statement": "No term w_A(m,hidden) S_A or kappa_A(m,hidden) T_A exists in ordinary matter before variation",
            "result": "NOT_DERIVED_COUNTERMODEL_SURVIVES",
            "blocking_gap": "constructor exhaustion, no-Hom, single action-scale and readout stability are unsigned",
            "effect": "source-weight residual interface remains live",
        },
        {
            "audit_id": "JDZ2522_4_variation_order",
            "claim_piece": "variation before readout/projector",
            "formal_statement": "delta_m acts on the parent action before Pi_M, P_loc, material projection, worldtube selection, or fitted orbital source maps",
            "result": "GUARD_READY_NOT_GENERAL_ZERO",
            "blocking_gap": "readout variation commutator remains open and is not part of direct zero",
            "effect": "move readout re-entry to next target instead of hiding it in J_direct",
        },
        {
            "audit_id": "JDZ2522_5_radiative_or_effective_reentry",
            "claim_piece": "no effective m psi psi coupling after integrating hidden/source sectors",
            "formal_statement": "EFT, bath, boundary, domain and source-worldtube reduction does not generate an effective direct m-matter term",
            "result": "NOT_DERIVED",
            "blocking_gap": "no-shadow/source-only slot and extra-channel silence remain unsigned",
            "effect": "finite effective direct coupling row required",
        },
        {
            "audit_id": "JDZ2522_6_Hilbert_separation",
            "claim_piece": "Hilbert source current does not equal direct memory silence",
            "formal_statement": "T_matter and J_M define source mass; they do not imply delta S_matter/delta m=0 unless the matter action argument list is m-blind",
            "result": "PASS_GUARDRAIL",
            "blocking_gap": "none; this prevents an overclaim",
            "effect": "source mass bridge remains usable without erasing coupling debt",
        },
        {
            "audit_id": "JDZ2522_7_verdict",
            "claim_piece": "J_direct_matter=0 theorem",
            "formal_statement": "JDZ2522_1 through JDZ2522_5 must close together",
            "result": "JDIRECT_ZERO_THEOREM_NOT_DERIVED_STAGE_BOUND_ROWS",
            "blocking_gap": "parent matter argument list, no source-prefactor, no marker/reentry and coefficient descent are unsigned",
            "effect": "finite J_direct_matter row is retained; next target is readout/projector re-entry",
        },
    ]
    return [base_row(score_ready=False, valid_prediction_row=False, **entry) for entry in entries]


def argument_list_gate_rows() -> list[dict[str, Any]]:
    entries = [
        {
            "gate_id": "ARG2522_0_public_carrier",
            "required_clause": "ordinary matter factors only through public metric/coframe",
            "formal_condition": "S_matter=Sbar[psi,e_pub,theta_pub,c_vis] with e_pub=E(q_parent(Phi))",
            "current_status": "CONDITIONAL_FROM_2486_2487_NOT_PARENT_SIGNED",
            "if_fail": "m can enter through the carrier/readout leg",
            "gate_pass": False,
        },
        {
            "gate_id": "ARG2522_1_no_m_argument",
            "required_clause": "m and memory variables absent from matter argument list",
            "formal_condition": "partial Arg(S_matter)/partial m=0 before readout and before source projection",
            "current_status": "DECLARED_CLOSURE_CANDIDATE_NOT_DERIVED",
            "if_fail": "direct J_direct_matter survives",
            "gate_pass": False,
        },
        {
            "gate_id": "ARG2522_2_no_hidden_marker",
            "required_clause": "no hidden/domain/boundary/material marker targets matter/source coefficients",
            "formal_condition": "Hom(HiddenMarker,Coeff_matter_source)=empty and no marker re-entry through EFT/readout",
            "current_status": "FAIL_NO_MARKER_REENTRY_NOT_PROVED",
            "if_fail": "hidden memory marker can become direct source coefficient",
            "gate_pass": False,
        },
        {
            "gate_id": "ARG2522_3_no_source_prefactor",
            "required_clause": "no source-only action/coupling prefactors",
            "formal_condition": "No w_A(m)S_A, kappa_A(m)T_A, or species-indexed action-scale line before variation",
            "current_status": "FAIL_NO_SOURCE_ONLY_SLOT_NOT_PARENT_DERIVED",
            "if_fail": "relative source weights and WEP/R10/PPN residuals survive",
            "gate_pass": False,
        },
        {
            "gate_id": "ARG2522_4_visible_constants",
            "required_clause": "visible constants are q-basic and m-independent",
            "formal_condition": "dc_vis(v_m)=0 for matter masses, clock constants, couplings and material coefficients",
            "current_status": "UNSIGNED_HARD_BLOCKER",
            "if_fail": "direct coupling can hide in material/constant response",
            "gate_pass": False,
        },
        {
            "gate_id": "ARG2522_5_variation_order",
            "required_clause": "variation before readout/projection/source selection",
            "formal_condition": "[delta_m,Pi_M]=[delta_m,P_loc]=[delta_m,Readout]=0 or those terms are assigned outside J_direct",
            "current_status": "GUARD_ACTIVE_REENTRY_NOT_ZEROED",
            "if_fail": "direct/readout coupling double-counting risk",
            "gate_pass": False,
        },
        {
            "gate_id": "ARG2522_6_theorem",
            "required_clause": "J_direct_matter zero theorem",
            "formal_condition": "ARG2522_0 through ARG2522_5 all pass with source paths",
            "current_status": "CLAIM_BLOCKED",
            "if_fail": "retain finite J_direct_matter bound rows",
            "gate_pass": False,
        },
    ]
    return [base_row(valid_for_claim=False, claim_allowed=False, **entry) for entry in entries]


def jdirect_bound_rows() -> list[dict[str, Any]]:
    entries = [
        {
            "row_id": "JDIR2522_0_total",
            "quantity": "J_direct_matter",
            "row_role": "total direct explicit matter-to-memory source",
            "formula_or_bound": "J_direct_matter <= J_arg_m + J_prefactor_m + J_coeff_m + J_measure_m + J_marker_m + J_effective_m",
            "units": "memory_source_units",
            "required_inputs": "component values/theorem-zero certificates; units; source paths; no-cancellation allocation",
            "current_status": "MISSING_DIRECT_ZERO_CERTIFICATE_OR_COMPONENT_VALUES",
            "observable_links": "J_mem;Q_mem;WEP;R10;PPN",
        },
        {
            "row_id": "JDIR2522_1_arg_m",
            "quantity": "J_arg_m",
            "row_role": "explicit m argument in matter action",
            "formula_or_bound": "J_arg_m := ||partial S_matter/partial m|| at fixed e_pub,psi",
            "units": "memory_source_units",
            "required_inputs": "parent matter argument list or finite coupling coefficient",
            "current_status": "MISSING_PARENT_MATTER_ARGUMENT_LIST",
            "observable_links": "J_mem;WEP;R10",
        },
        {
            "row_id": "JDIR2522_2_prefactor_m",
            "quantity": "J_prefactor_m",
            "row_role": "m-dependent source/action prefactor",
            "formula_or_bound": "J_prefactor_m <= ||partial_m w_A|| ||S_A|| + ||partial_m kappa_A|| ||T_A||",
            "units": "memory_source_units",
            "required_inputs": "no-source-only-slot theorem or prefactor derivative bound",
            "current_status": "MISSING_NO_SOURCE_ONLY_SLOT_THEOREM",
            "observable_links": "WEP;PPN;R10;J_mem",
        },
        {
            "row_id": "JDIR2522_3_coeff_m",
            "quantity": "J_coeff_m",
            "row_role": "m-dependence of visible constants/material coefficients",
            "formula_or_bound": "J_coeff_m <= sum_i ||partial_m c_i|| ||partial S_matter/partial c_i||",
            "units": "memory_source_units",
            "required_inputs": "coefficient descent theorem or source-backed material sensitivity row",
            "current_status": "MISSING_VISIBLE_COEFFICIENT_DESCENT",
            "observable_links": "clock;WEP;particle;PPN",
        },
        {
            "row_id": "JDIR2522_4_measure_scale_m",
            "quantity": "J_measure_m",
            "row_role": "m-dependence of action measure/normalization",
            "formula_or_bound": "J_measure_m <= ||partial_m ln mu_action|| |S_matter|",
            "units": "memory_source_units",
            "required_inputs": "single action-scale/measure owner or finite derivative bound",
            "current_status": "MISSING_SINGLE_ACTION_SCALE_OWNER",
            "observable_links": "WEP;clock;source_normalization",
        },
        {
            "row_id": "JDIR2522_5_marker_m",
            "quantity": "J_marker_m",
            "row_role": "hidden/domain/boundary marker direct source leg",
            "formula_or_bound": "J_marker_m <= K_marker |epsilon_hidden_marker|",
            "units": "memory_source_units",
            "required_inputs": "no-marker/no-Hom theorem or finite marker kernel",
            "current_status": "MISSING_NO_MARKER_REENTRY_THEOREM",
            "observable_links": "R10;WEP;PPN",
        },
        {
            "row_id": "JDIR2522_6_effective_m",
            "quantity": "J_effective_m",
            "row_role": "effective direct coupling generated by hidden/source-worldtube reduction",
            "formula_or_bound": "J_effective_m <= ||partial_m S_eff,matter|| after integrating non-observed sectors",
            "units": "memory_source_units",
            "required_inputs": "EFT/readout/source-worldtube no-reentry theorem or finite kernel",
            "current_status": "MISSING_EFFECTIVE_REENTRY_ZERO_OR_BOUND",
            "observable_links": "J_mem;Q_mem;clock;orbit",
        },
        {
            "row_id": "JDIR2522_7_Qmem_insertion",
            "quantity": "N_src J_direct_matter",
            "row_role": "direct matter drive insertion into Q_mem",
            "formula_or_bound": "Q_mem_direct <= A_ref^-1 N_src J_direct_matter",
            "units": "dimensionless_after_Aref",
            "required_inputs": "A_ref;N_src;J_direct_matter value/theorem-zero; source path",
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


def observable_gate_rows() -> list[dict[str, Any]]:
    entries = [
        {
            "gate_id": "JDG2522_0_Jmem",
            "arena": "J_mem total drive",
            "map_formula": "J_mem includes J_direct_matter plus exchange/bath/readout/domain/worldtube/shadow channels",
            "required_bundle": "J_direct zero certificate or component bounds plus no double counting",
            "status": "BLOCKED_MISSING_JDIRECT_VALUE_OR_THEOREM",
            "claim_pass": False,
        },
        {
            "gate_id": "JDG2522_1_Qmem",
            "arena": "Q_mem residual",
            "map_formula": "Q_mem_direct <= A_ref^-1 N_src J_direct_matter",
            "required_bundle": "A_ref;N_src;J_direct units/value/source",
            "status": "BLOCKED_MISSING_QMEM_INSERTION_VALUES",
            "claim_pass": False,
        },
        {
            "gate_id": "JDG2522_2_WEP",
            "arena": "WEP/material source universality",
            "map_formula": "J_prefactor_m,J_coeff_m,J_marker_m -> Delta_w_eff -> eta",
            "required_bundle": "source-weight/material kernels and no-source-slot theorem or values",
            "status": "BLOCKED_MISSING_WEP_KERNELS_AND_PARENT_VALUES",
            "claim_pass": False,
        },
        {
            "gate_id": "JDG2522_3_R10",
            "arena": "R10 short-range/source coupling",
            "map_formula": "J_direct_matter and B_mem/H_m range -> alpha(lambda) or source-normalization residual",
            "required_bundle": "range;source/test charge;bound curve;direct coupling coefficient",
            "status": "BLOCKED_MISSING_R10_PROJECTION",
            "claim_pass": False,
        },
        {
            "gate_id": "JDG2522_4_clock_orbit",
            "arena": "clock/orbital readout",
            "map_formula": "J_coeff_m,J_measure_m,J_effective_m -> clock/orbital residual",
            "required_bundle": "material sensitivities, readout kernels, units",
            "status": "BLOCKED_MISSING_CLOCK_ORBIT_KERNELS",
            "claim_pass": False,
        },
        {
            "gate_id": "JDG2522_5_local_GR",
            "arena": "local GR/Newton recovery",
            "map_formula": "direct source zero or bound plus all other J_mem/Qmem/CDB/source-normalization gates",
            "required_bundle": "full residual vector below local gates",
            "status": "BLOCKED_NO_LOCAL_GR_CLAIM",
            "claim_pass": False,
        },
    ]
    return [base_row(score_ready=False, accepted_for_scoring=False, **entry) for entry in entries]


def dryrun_rows() -> list[dict[str, Any]]:
    entries = [
        {
            "case_id": "DRY2522_0_declared_matter_signature",
            "case_description": "claim J_direct=0 from declared matter action signature",
            "missing_requirements": "parent-derived argument list, no-source-slot, no-marker, coefficient descent",
            "result_status": "REJECT",
            "blocking_markers": "CLOSURE_CANDIDATE_NOT_DERIVED",
            "pass_fail": "BLOCKED_NONCLAIM",
            "claim_pass": False,
        },
        {
            "case_id": "DRY2522_1_chain_rule_without_qbasic_readout",
            "case_description": "use quotient chain rule while e_obs/theta/readout are not q-basic",
            "missing_requirements": "q_parent, v_m, E(q), theta(q), visible coefficient descent",
            "result_status": "REJECT",
            "blocking_markers": "Q_BASIC_READOUT_UNSIGNED",
            "pass_fail": "BLOCKED_NONCLAIM",
            "claim_pass": False,
        },
        {
            "case_id": "DRY2522_2_no_source_slot_repeat",
            "case_description": "repeat no-source-only-slot theorem as if new",
            "missing_requirements": "new constructor exhaustion source; no-Hom; action scale owner",
            "result_status": "REJECT",
            "blocking_markers": "2508_LOOP_GUARD",
            "pass_fail": "BLOCKED_NONCLAIM",
            "claim_pass": False,
        },
        {
            "case_id": "DRY2522_3_Hilbert_current_as_matter_blindness",
            "case_description": "use Hilbert source current to infer delta S_matter/delta m=0",
            "missing_requirements": "m-blind matter argument list and no effective reentry",
            "result_status": "REJECT",
            "blocking_markers": "SOURCE_MASS_NOT_DIRECT_ZERO",
            "pass_fail": "BLOCKED_NONCLAIM",
            "claim_pass": False,
        },
        {
            "case_id": "DRY2522_4_numeric_Jdirect_without_bundle",
            "case_description": "score finite J_direct without component values, units, source paths, A_ref/N_src",
            "missing_requirements": "units;component allocation;source path;arena map",
            "result_status": "REJECT",
            "blocking_markers": "MISSING_JDIRECT_RUNNER_BUNDLE",
            "pass_fail": "BLOCKED_NONCLAIM",
            "claim_pass": False,
        },
        {
            "case_id": "DRY2522_5_future_complete_Jdirect",
            "case_description": "future J_direct row with real zero certificate or finite component bounds",
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
            "decision_id": "DEC2522_0_direct_status",
            "decision": "do not claim direct matter-memory zero",
            "rationale": "chain-rule matter blindness is exact only after q-basic matter/readout and parent action argument-list clauses are signed",
            "next_action": "retain finite J_direct_matter bound rows",
            "status": "ACTIVE",
        },
        {
            "decision_id": "DEC2522_1_partial_gain",
            "decision": "keep direct coupling separated from readout re-entry",
            "rationale": "direct delta S_matter/delta m and post-variation readout/projector commutators are different mechanisms",
            "next_action": "attack readout/projector memory re-entry next",
            "status": "ACTIVE",
        },
        {
            "decision_id": "DEC2522_2_loop_guard",
            "decision": "do not repeat no-source-slot proof loop",
            "rationale": "2508 already proved the theorem is clean but not parent-derived without constructor exhaustion",
            "next_action": "use residual rows unless genuinely new constructor evidence appears",
            "status": "ACTIVE",
        },
        {
            "decision_id": "DEC2522_3_fibre_queue",
            "decision": "keep fibre B_h queued after readout re-entry",
            "rationale": "memory-source direct and readout channels remain upstream of Qmem scoring",
            "next_action": "renumber fibre queue after readout/projector target",
            "status": "ACTIVE",
        },
    ]
    return [base_row(valid_for_claim=False, claim_allowed=False, **entry) for entry in entries]


def next_target_rows() -> list[dict[str, Any]]:
    entries = [
        {
            "route_id": "NEXT2522_0_selected",
            "selection_status": "selected",
            "target_file": "2523-Y5-R2FR-readout-projector-memory-reentry-zero-or-Jreadout-bound.md",
            "target_script": "scripts/Y5_R2FR_readout_projector_memory_reentry_zero_or_Jreadout_bound_2523.py",
            "objective": "prove post-variation readout/projector/worldtube maps do not reintroduce memory-source dependence, or stage finite J_readout commutator rows with units and source paths",
            "success_condition": "J_readout is theorem-zero from fixed readout/projector variation order or retained as a finite nonclaim component feeding J_mem and Q_mem",
            "do_not_do": "do not repeat no-source-slot proof; do not treat Hilbert source mass as readout silence; do not claim WEP/Newton/local GR",
        },
        {
            "route_id": "NEXT2522_1_fibre_queue",
            "selection_status": "queued_after_readout_reentry",
            "target_file": "2524-Y5-R2FR-fibre-Bh-finite-row-or-hidden-visible-grammar-reentry.md",
            "target_script": "scripts/Y5_R2FR_fibre_Bh_finite_row_or_hidden_visible_grammar_reentry_2524.py",
            "objective": "classify fibre B_h with hidden-visible grammar reentry or finite fibre coefficient rows after memory readout-source lane is handled",
            "success_condition": "B_h has theorem-zero evidence or finite nonclaim Z_h/M2_h/B_h/C_h/source-charge rows",
            "do_not_do": "do not let memory closure erase fibre residuals",
        },
    ]
    return [base_row(valid_for_claim=False, claim_allowed=False, **entry) for entry in entries]


def branch_copy_rows() -> list[dict[str, Any]]:
    copy_specs = [
        ("direct_zero_audit", OUTPUTS["direct_zero_audit"], BRANCH_COPIES["direct_zero_audit"]),
        ("jdirect_bound_rows", OUTPUTS["jdirect_bound_rows"], BRANCH_COPIES["jdirect_bound_rows"]),
        ("argument_list_gate", OUTPUTS["argument_list_gate"], BRANCH_COPIES["argument_list_gate"]),
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
    audit_rows = rows_by_name["direct_zero_audit"]
    bound_rows = rows_by_name["jdirect_bound_rows"]
    argument_rows = rows_by_name["argument_list_gate"]

    add("VAL2522_00_sources_exist", all(str(row["path_exists"]) == "True" for row in source_rows))
    add("VAL2522_01_source_needles", all(str(row["source_pass"]) == "True" for row in source_rows))
    add(
        "VAL2522_02_conditional_theorem_written",
        any(row["audit_id"] == "JDZ2522_1_chain_rule_zero" and row["result"] == "EXACT_CONDITIONAL_THEOREM" for row in audit_rows),
        "conditional q-basic matter descent theorem is recorded",
    )
    add(
        "VAL2522_03_direct_zero_not_promoted",
        any(
            row["audit_id"] == "JDZ2522_7_verdict"
            and row["result"] == "JDIRECT_ZERO_THEOREM_NOT_DERIVED_STAGE_BOUND_ROWS"
            for row in audit_rows
        ),
        "J_direct_matter zero remains unclaimed",
    )
    add(
        "VAL2522_04_argument_gates_blocked",
        len(argument_rows) == 7 and all(str(row["gate_pass"]) == "False" for row in argument_rows),
        "matter argument-list gates block promotion",
    )
    add(
        "VAL2522_05_bound_rows_complete",
        all(
            any(row["row_id"] == required for row in bound_rows)
            for required in [
                "JDIR2522_0_total",
                "JDIR2522_1_arg_m",
                "JDIR2522_2_prefactor_m",
                "JDIR2522_3_coeff_m",
                "JDIR2522_7_Qmem_insertion",
            ]
        ),
        "direct bound rows include total, argument, prefactor, coefficient and Qmem insertion",
    )
    add(
        "VAL2522_06_bound_rows_nonclaim",
        all(str(row["accepted_for_scoring"]) == "False" and str(row["claim_pass"]) == "False" for row in bound_rows),
        "all direct bound rows are blocked for scoring",
    )
    add(
        "VAL2522_07_observable_gates_blocked",
        all(str(row["claim_pass"]) == "False" and str(row["status"]).startswith("BLOCKED") for row in rows_by_name["observable_gate"]),
        "Jmem/Qmem/WEP/R10/clock/orbit/local-GR gates remain blocked",
    )
    add(
        "VAL2522_08_dryruns_block_bad_rows",
        all(str(row["claim_pass"]) == "False" for row in rows_by_name["dryrun_results"])
        and all(str(row["result_status"]) in {"REJECT", "WOULD_ACCEPT_SCHEMA_IF_REAL_FILES_AND_VALUES_EXIST"} for row in rows_by_name["dryrun_results"]),
        "declared signature, q-basic shortcut, no-slot repeat, Hilbert-as-silence and incomplete numeric rows do not score",
    )
    add(
        "VAL2522_09_next_target_readout",
        any(row["route_id"] == "NEXT2522_0_selected" and "readout-projector" in row["target_file"] for row in rows_by_name["next_target"]),
        "readout/projector memory re-entry selected next",
    )
    add("VAL2522_10_no_claim_flags", no_claim_flags(rows_by_name))
    add(
        "VAL2522_11_branch_copies",
        all(str(row["copied"]) == "True" and str(row["parse_ok"]) == "True" for row in rows_by_name["branch_copies"]),
    )
    formalization = ROOT.parent / "formalization-workbench"
    formalization_hits = [
        path
        for path in formalization.rglob("*2522*")
        if ".venv" not in path.parts and "site-packages" not in path.parts
    ] if formalization.exists() else []
    add(
        "VAL2522_12_no_formalization_artifacts",
        len(formalization_hits) == 0,
        ";".join(str(path) for path in formalization_hits),
    )
    add("VAL2522_13_pycache_absent", not (Path(__file__).resolve().parent / "__pycache__").exists())

    for name, path in OUTPUTS.items():
        if name == "validation":
            continue
        ok, count, message = csv_rows_parse(path)
        add(f"VAL2522_CSV_{path.stem}", ok, f"{message}; rows={count}")
    for key, path in BRANCH_COPIES.items():
        ok, count, message = csv_rows_parse(path)
        add(f"VAL2522_COPY_CSV_{key}", ok, f"{message}; rows={count}")

    overall = all(row["status"] == "PASS" for row in checks)
    checks.append(
        base_row(
            check_id="VAL2522_OVERALL",
            status="PASS" if overall else "FAIL",
            detail="2522 formulates exact conditional matter-memory direct zero, refuses to promote unsigned matter signature/no-slot clauses, stages J_direct rows, and selects readout/projector re-entry next.",
            valid_for_claim=False,
            claim_allowed=False,
        )
    )
    return checks


def write_doc(rows_by_name: dict[str, list[dict[str, Any]]]) -> None:
    DOC.write_text(
        "\n".join(
            [
                "# 2522 - Matter-Memory Direct Coupling Zero or Jdirect Bound",
                "",
                "**Current verdict:** `J_direct_matter=0` is exact only as a conditional chain-rule theorem. Current MTS does not parent-sign the matter argument list, no-source-prefactor grammar, no-marker clause, visible coefficient descent, or readout-order stability needed to promote it.",
                "",
                "**Main gain:** direct matter-memory coupling is now separated from Hilbert source mass and from post-variation readout/projector re-entry. The finite direct row is split into argument, source-prefactor, coefficient, action-measure, hidden-marker, effective-reentry, and `Q_mem` insertion pieces.",
                "",
                "**Claim discipline:** no direct-source zero, WEP, Newton, PPN, R10, clock, orbit, local-GR, no-source-slot, or public/GitHub claim is made.",
                "",
                "## Source Register",
                md_table(rows_by_name["source_register"], ["source_id", "source_path", "path_exists", "found_needles", "source_pass", "role"]),
                "",
                "## Direct Zero Audit",
                md_table(rows_by_name["direct_zero_audit"], ["audit_id", "claim_piece", "formal_statement", "result", "blocking_gap", "effect"]),
                "",
                "## Matter Argument List Gate",
                md_table(rows_by_name["argument_list_gate"], ["gate_id", "required_clause", "formal_condition", "current_status", "if_fail", "gate_pass"]),
                "",
                "## Jdirect Bound Rows",
                md_table(rows_by_name["jdirect_bound_rows"], ["row_id", "quantity", "row_role", "formula_or_bound", "required_inputs", "current_status", "observable_links"]),
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
        "direct_zero_audit": direct_zero_audit_rows(),
        "argument_list_gate": argument_list_gate_rows(),
        "jdirect_bound_rows": jdirect_bound_rows(),
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

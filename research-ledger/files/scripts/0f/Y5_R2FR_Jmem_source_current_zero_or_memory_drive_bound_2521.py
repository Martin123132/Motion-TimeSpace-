from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
BRANCH_ID = "MTS_R2FR_JMEM_SOURCE_CURRENT_ZERO_2521"
CHECKPOINT_ID = "2521"
DOC = ROOT / "2521-Y5-R2FR-Jmem-source-current-zero-or-memory-drive-bound.md"
MTS_RESIDUALS = ROOT / "source-intake" / "mts_residuals"

OUTPUTS = {
    "source_register": MTS_RESIDUALS / "P8_Y5_NO_SHADOW_2521_SOURCE_REGISTER.csv",
    "jmem_zero_audit": MTS_RESIDUALS / "P8_Y5_NO_SHADOW_2521_JMEM_ZERO_AUDIT.csv",
    "source_current_contract": MTS_RESIDUALS / "P8_Y5_NO_SHADOW_2521_SOURCE_CURRENT_DESCENT_CONTRACT.csv",
    "jmem_drive_bound_rows": MTS_RESIDUALS / "P8_Y5_NO_SHADOW_2521_JMEM_DRIVE_BOUND_ROWS.csv",
    "observable_gate": MTS_RESIDUALS / "P8_Y5_NO_SHADOW_2521_OBSERVABLE_GATE.csv",
    "dryrun_results": MTS_RESIDUALS / "P8_Y5_NO_SHADOW_2521_DRYRUN_RESULTS.csv",
    "decision_ledger": MTS_RESIDUALS / "P8_Y5_NO_SHADOW_2521_DECISION_LEDGER.csv",
    "next_target": MTS_RESIDUALS / "P8_Y5_NO_SHADOW_2521_NEXT_TARGET.csv",
    "branch_copies": MTS_RESIDUALS / "P8_Y5_NO_SHADOW_2521_BRANCH_COPIES.csv",
    "validation": MTS_RESIDUALS / "P8_Y5_BRR545_2521_VALIDATION.csv",
}

BRANCH_COPIES = {
    "jmem_zero_audit": ROOT
    / "source-intake"
    / "local_bounds"
    / "Jmem_zero_audit_2521_NONCLAIM.csv",
    "jmem_drive_bound_rows": ROOT
    / "source-intake"
    / "beta-source"
    / "docs"
    / "Jmem_drive_bound_rows_2521_NONCLAIM.csv",
    "source_current_contract": ROOT
    / "source-intake"
    / "rab-sector"
    / "acquisition-queue"
    / "JR2521_SOURCE_CURRENT_DESCENT_CONTRACT_NONCLAIM.csv",
    "next_target": ROOT
    / "source-intake"
    / "rab-sector"
    / "acquisition-queue"
    / "JR2521_NEXT_TARGET_NONCLAIM.csv",
}

SOURCE_SPECS = [
    {
        "source_id": "SRC2521_0_2520_next",
        "path": "source-intake/mts_residuals/P8_Y5_NO_SHADOW_2520_NEXT_TARGET.csv",
        "needles": ["NEXT2520_0_selected", "J_mem"],
        "role": "authoritative 2520 handoff to source-current zero or memory-drive bound",
    },
    {
        "source_id": "SRC2521_1_2520_qmem_components",
        "path": "source-intake/mts_residuals/P8_Y5_NO_SHADOW_2520_QMEM_COMPONENT_ROWS.csv",
        "needles": ["QMC2520_6_Jmem", "MISSING_SOURCE_SILENCE_THEOREM_OR_BOUND"],
        "role": "current J_mem component row and blocker",
    },
    {
        "source_id": "SRC2521_2_2520_validation",
        "path": "source-intake/mts_residuals/P8_Y5_BRR545_2520_VALIDATION.csv",
        "needles": ["VAL2520_OVERALL", "PASS"],
        "role": "previous checkpoint validation gate",
    },
    {
        "source_id": "SRC2521_3_1302_nohair_requirements",
        "path": "source-intake/mts_residuals/P8_Y5_R10_1302_MEMORY_STRESS_NOHAIR_REQUIREMENTS.csv",
        "needles": ["NHM1302_2_source_silence", "MISSING_ZERO_SOURCE_THEOREM"],
        "role": "memory no-hair source-silence requirement",
    },
    {
        "source_id": "SRC2521_4_1303_nohair_attempt",
        "path": "source-intake/mts_residuals/P8_Y5_R10_1303_MEMORY_STRESS_NOHAIR_ATTEMPT.csv",
        "needles": ["NHA1303_2_source_silence", "NOT_DERIVED"],
        "role": "best current memory source-silence attempt",
    },
    {
        "source_id": "SRC2521_5_1011_response_doublet",
        "path": "source-intake/mts_residuals/P8_Y5_R10_1011_RESPONSED_DOUBLET_THEOREM_ATTEMPT.csv",
        "needles": ["RDT1011_3_source_current_zero", "fail_current_claim"],
        "role": "response-doublet source-current theorem fails current corpus",
    },
    {
        "source_id": "SRC2521_6_2466_hilbert_current",
        "path": "source-intake/mts_residuals/P8_Y5_SOURCE_BRIDGE_2466_HILBERT_CURRENT_DESCENT.csv",
        "needles": ["HIL2466_0_define_T", "MISSING_UNIFICATION_OF_COUPLINGS"],
        "role": "Hilbert energy current source bridge and direct-coupling warning",
    },
    {
        "source_id": "SRC2521_7_2466_verdict",
        "path": "source-intake/mts_residuals/P8_Y5_SOURCE_BRIDGE_2466_PROMOTION_VERDICT.csv",
        "needles": ["PV2466_4_overall", "SOURCE_BRIDGE_SHARPENED_NOT_CLOSED"],
        "role": "source bridge sharpened but not closed",
    },
    {
        "source_id": "SRC2521_8_2467_verdict",
        "path": "source-intake/mts_residuals/P8_Y5_HILBERT_CURRENT_2467_PROMOTION_VERDICT.csv",
        "needles": ["PV2467_4_overall", "LOCAL_STATIONARY_CONTRACT_SHARPENED_DYNAMIC_CLOSURE_BLOCKED"],
        "role": "Hilbert current conservation/scale/clock gate",
    },
    {
        "source_id": "SRC2521_9_2468_stationary",
        "path": "source-intake/mts_residuals/P8_Y5_STATIONARY_SOURCE_2468_EXTERIOR_QLOC_RESULT.csv",
        "needles": ["EXT2468_0_stationary_q_zero", "EXT2468_4_claim_limit"],
        "role": "stationary exterior q_loc theorem contract and claim limit",
    },
    {
        "source_id": "SRC2521_10_2481_source_norm",
        "path": "source-intake/mts_residuals/P8_Y5_SOURCE_NORM_2481_THEOREM_ATTEMPT.csv",
        "needles": ["THM2481_0_define_current", "ZERO_NOT_PROMOTED_RETAIN_E_NORM"],
        "role": "Hilbert source normalization theorem attempt and retained gap",
    },
    {
        "source_id": "SRC2521_11_2508_no_source_slot",
        "path": "source-intake/mts_residuals/P8_Y5_NO_SHADOW_2508_NO_SOURCE_ONLY_SLOT_PROOF_ATTEMPT.csv",
        "needles": ["NSP2508_7_verdict", "NO_SOURCE_ONLY_SLOT_PROOF_NOT_PARENT_DERIVED"],
        "role": "no source-only slot theorem not parent-derived",
    },
    {
        "source_id": "SRC2521_12_2508_residual_rows",
        "path": "source-intake/mts_residuals/P8_Y5_NO_SHADOW_2508_SOURCE_WEIGHT_RESIDUAL_ROWS.csv",
        "needles": ["RSW2508_0", "MISSING_NO_SOURCE_ONLY_SLOT_THEOREM"],
        "role": "source-weight/shadow residual rows retained",
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


def jmem_zero_audit_rows() -> list[dict[str, Any]]:
    entries = [
        {
            "audit_id": "JZ2521_0_conditional_zero_theorem",
            "claim_piece": "J_mem=0 theorem skeleton",
            "formal_statement": "If S_matter has no explicit memory-coordinate dependence, source/readout/bath/history/domain maps do not re-enter the m-Euler equation, and the exterior worldtube has no memory flux, then the direct memory source current J_mem vanishes.",
            "result": "CONDITIONAL_THEOREM_FORMULATED",
            "blocking_gap": "the parent m-blind matter action, no re-entry, and worldtube/bath/readout clauses are not all signed",
            "effect": "usable theorem target, not evidence",
        },
        {
            "audit_id": "JZ2521_1_Hilbert_current",
            "claim_piece": "Hilbert energy current as source object",
            "formal_statement": "J_M^nu=ell_J T_matter^{nu rho} tau_rho is the least-circular source-current route for mass/charge",
            "result": "PASS_AS_SOURCE_BRIDGE_NOT_JMEM_ZERO",
            "blocking_gap": "Hilbert current defines source mass; it does not by itself prove memory-source silence",
            "effect": "separates source mass derivation from memory drive zero",
        },
        {
            "audit_id": "JZ2521_2_stationary_exterior",
            "claim_piece": "stationary compact exterior source silence",
            "formal_statement": "q_loc -> 0 and surface mass is constant under stationary compact-source hypotheses",
            "result": "CONDITIONAL_LOCAL_BRANCH_ONLY",
            "blocking_gap": "dynamic exchange, parent scale, metric stress, and source-shadow equivalence remain open",
            "effect": "cannot be promoted to global J_mem=0 or full local GR",
        },
        {
            "audit_id": "JZ2521_3_response_doublet",
            "claim_piece": "response-doublet source-current zero",
            "formal_statement": "exchange symmetry forbids odd source current if all physical residuals live in parent doublets and matter/readout is even",
            "result": "FAIL_CURRENT_CORPUS",
            "blocking_gap": "source-current zero, boundary zero, Y5/Y6, and PPN lock are not derived",
            "effect": "do not use response-doublet symmetry as J_mem zero certificate",
        },
        {
            "audit_id": "JZ2521_4_no_source_only_slot",
            "claim_piece": "no independent source-only coefficient slot",
            "formal_statement": "parent grammar forbids w_A, kappa_A, hidden markers or source-only material multipliers before variation",
            "result": "NOT_PARENT_DERIVED",
            "blocking_gap": "constructor exhaustion, no-Hom, single action-scale owner, and readout no-reentry are unsigned",
            "effect": "source-shadow/source-weight residuals remain live",
        },
        {
            "audit_id": "JZ2521_5_direct_matter_blindness",
            "claim_piece": "direct matter-to-memory coupling absence",
            "formal_statement": "delta S_matter/delta m=0 at fixed g,psi if matter action depends only on metric/coframe and not m, X_B, hidden marker, domain wall, or source readout",
            "result": "PLAUSIBLE_BEST_NEXT_TARGET_NOT_SIGNED",
            "blocking_gap": "parent matter action descent and no marker/readout re-entry have not been certified",
            "effect": "select direct matter m-blind descent as next derivation target",
        },
        {
            "audit_id": "JZ2521_6_boundary_bath_history",
            "claim_piece": "bath/history/boundary memory drive silence",
            "formal_statement": "J_bath=J_history=J_boundary_feed=0 in ordinary local exterior",
            "result": "NOT_DERIVED",
            "blocking_gap": "boundary/source/bath terms were retained in 1302/1303 and are not theorem-zero",
            "effect": "finite drive rows must include these channels",
        },
        {
            "audit_id": "JZ2521_7_verdict",
            "claim_piece": "J_mem=0 theorem",
            "formal_statement": "JZ2521_0 through JZ2521_6 must close together",
            "result": "JMEM_ZERO_THEOREM_NOT_DERIVED_STAGE_DRIVE_BOUND_ROWS",
            "blocking_gap": "direct m-blind matter descent, no-source-slot, readout, bath/history, boundary and dynamic exchange clauses remain unsigned",
            "effect": "finite J_mem drive row is the honest default",
        },
    ]
    return [base_row(score_ready=False, valid_prediction_row=False, **entry) for entry in entries]


def source_current_contract_rows() -> list[dict[str, Any]]:
    entries = [
        {
            "contract_id": "SCC2521_0_define_direct_Jmem",
            "object": "J_mem_direct",
            "contract": "J_mem_direct := delta S_source/delta m at fixed metric/coframe/matter fields and fixed variation order",
            "zero_condition": "S_source is m-blind before variation and readout/projector maps do not re-enter the Euler equation",
            "current_status": "DEFINITION_READY_ZERO_UNSIGNED",
            "missing": "parent matter action descent; fixed variation order; no readout re-entry",
        },
        {
            "contract_id": "SCC2521_1_hilbert_source_separation",
            "object": "J_M^nu",
            "contract": "J_M^nu := ell_J T_matter^{nu rho} tau_rho defines source mass current, not memory drive",
            "zero_condition": "none; this is the source object for Newton branch, not a silence theorem",
            "current_status": "PASS_AS_CONTRACT_NONCLAIM",
            "missing": "ell_J parent scale; tau conservation; coupling unification",
        },
        {
            "contract_id": "SCC2521_2_stationary_subbranch",
            "object": "J_mem_stationary_exterior",
            "contract": "stationary compact-source exterior may set exterior q_loc leakage to zero under explicit hypotheses",
            "zero_condition": "stationary tau; compact support; side flux zero; residual source-shadow silent",
            "current_status": "CONDITIONAL_SUBBRANCH_ONLY",
            "missing": "dynamic exchange and source-shadow equivalence",
        },
        {
            "contract_id": "SCC2521_3_source_shadow",
            "object": "J_mem_shadow",
            "contract": "hidden/source-weight/readout coefficients must not project into memory/source drive",
            "zero_condition": "NoSourceOnlySpeciesSlot and no marker/readout re-entry are parent-derived",
            "current_status": "BLOCKED_BY_2508",
            "missing": "constructor exhaustion; no-Hom; single action-scale owner",
        },
        {
            "contract_id": "SCC2521_4_bound_default",
            "object": "J_mem_bound",
            "contract": "If any zero clause fails, use |J_mem| <= sum of direct/source/bath/readout/history/domain/worldtube/shadow pieces with no cancellation",
            "zero_condition": "all channel bounds zero independently",
            "current_status": "FINITE_BOUND_ROUTE_ACTIVE_NONCLAIM",
            "missing": "channel values/theorems, units, source paths, arena maps",
        },
    ]
    return [base_row(valid_for_claim=False, claim_allowed=False, **entry) for entry in entries]


def jmem_drive_bound_rows() -> list[dict[str, Any]]:
    entries = [
        {
            "row_id": "JDRV2521_0_Jmem_total",
            "quantity": "J_mem",
            "row_role": "total memory source-current drive",
            "formula_or_bound": "|J_mem| <= J_direct_matter + J_Hilbert_exchange + J_bath + J_readout + J_history + J_domain + J_worldtube + J_shadow",
            "units": "memory_source_units",
            "required_inputs": "all component drives; units; source paths; no-cancellation allocation; Q_mem normalization",
            "current_status": "MISSING_TOTAL_ZERO_CERTIFICATE_OR_COMPONENT_VALUES",
            "observable_links": "Q_mem;PPN_gamma;clock;orbit;WEP",
        },
        {
            "row_id": "JDRV2521_1_direct_matter",
            "quantity": "J_direct_matter",
            "row_role": "direct explicit matter-to-memory source",
            "formula_or_bound": "J_direct_matter := ||delta S_matter/delta m|| at fixed g,psi,variation order",
            "units": "memory_source_units",
            "required_inputs": "m-blind parent matter action or finite direct coupling bound",
            "current_status": "MISSING_MATTER_MBLIND_DESCENT",
            "observable_links": "Q_mem;WEP;R10",
        },
        {
            "row_id": "JDRV2521_2_Hilbert_exchange",
            "quantity": "J_Hilbert_exchange",
            "row_role": "dynamic exchange induced by non-stationary Hilbert current/clock strain",
            "formula_or_bound": "J_Hilbert_exchange <= C_tau ||T^{mu nu} nabla_mu tau_nu|| plus exchange-current residual",
            "units": "memory_source_units",
            "required_inputs": "tau conservation/exchange theorem; C_tau; dynamic support bound",
            "current_status": "MISSING_DYNAMIC_EXCHANGE_CURRENT",
            "observable_links": "Q_mem;clock;Gdot;orbit",
        },
        {
            "row_id": "JDRV2521_3_bath",
            "quantity": "J_bath",
            "row_role": "environment/history/bath memory drive",
            "formula_or_bound": "J_bath := ||delta S_bath_history/delta m||",
            "units": "memory_source_units",
            "required_inputs": "bath/history absence theorem or finite source-bound row",
            "current_status": "MISSING_BATH_HISTORY_ZERO_OR_BOUND",
            "observable_links": "Q_mem;clock",
        },
        {
            "row_id": "JDRV2521_4_readout_projector",
            "quantity": "J_readout",
            "row_role": "post-variation readout/projector re-entry into memory drive",
            "formula_or_bound": "J_readout <= ||[delta_m, Readout/P_loc/Pi_M] S_source||",
            "units": "memory_source_units",
            "required_inputs": "readout variation commutator zero theorem or finite commutator norm",
            "current_status": "MISSING_READOUT_COMMUTATOR_ZERO_OR_BOUND",
            "observable_links": "Q_mem;PPN;orbital;clock",
        },
        {
            "row_id": "JDRV2521_5_domain_wall",
            "quantity": "J_domain",
            "row_role": "domain/wall/source support leakage",
            "formula_or_bound": "J_domain <= ||delta_m chi_D|| ||source current|| plus wall/support terms",
            "units": "memory_source_units",
            "required_inputs": "domain fixed theorem; support/jump condition; wall coefficient",
            "current_status": "MISSING_DOMAIN_SUPPORT_ZERO_OR_BOUND",
            "observable_links": "Q_mem;R10;WEP",
        },
        {
            "row_id": "JDRV2521_6_worldtube",
            "quantity": "J_worldtube",
            "row_role": "worldtube side-flux and jump/source support residual",
            "formula_or_bound": "J_worldtube <= epsilon_surface_drift + epsilon_jump_support contributions in memory-source units",
            "units": "memory_source_units",
            "required_inputs": "surface independence theorem or finite jump/support bound",
            "current_status": "MISSING_WORLDTUBE_JUMP_SUPPORT_BOUND",
            "observable_links": "Q_mem;Newton;orbit",
        },
        {
            "row_id": "JDRV2521_7_shadow_weight",
            "quantity": "J_shadow",
            "row_role": "source-only weight/hidden marker/source-normalization shadow",
            "formula_or_bound": "J_shadow <= K_shadow |Delta_w_eff| or theorem-zero from NoSourceOnlySpeciesSlot",
            "units": "memory_source_units",
            "required_inputs": "source-weight vector; no-source-slot theorem; arena kernel",
            "current_status": "MISSING_NO_SOURCE_ONLY_SLOT_THEOREM",
            "observable_links": "Q_mem;WEP;PPN;R10",
        },
        {
            "row_id": "JDRV2521_8_scale_units",
            "quantity": "ell_J;tau;source_normalization",
            "row_role": "source-current scale and clock normalization",
            "formula_or_bound": "J_M^nu=ell_J T^{nu rho} tau_rho with ell_J constant and tau parent-owned",
            "units": "scale_and_clock_convention",
            "required_inputs": "ell_J parent source; tau conservation; units; no hidden fitted GM",
            "current_status": "MISSING_PARENT_SCALE_AND_CLOCK_CONVENTION",
            "observable_links": "Newton;Q_mem;clock;orbit",
        },
        {
            "row_id": "JDRV2521_9_Qmem_insertion",
            "quantity": "N_src J_mem",
            "row_role": "Q_mem source-drive insertion",
            "formula_or_bound": "Q_mem_source <= A_ref^-1 N_src J_mem",
            "units": "dimensionless_after_Aref",
            "required_inputs": "A_ref;N_src;J_mem value or theorem-zero; source paths",
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
            "gate_id": "JOG2521_0_Qmem",
            "arena": "Q_mem component budget",
            "map_formula": "Q_mem_source <= A_ref^-1 N_src J_mem",
            "required_bundle": "A_ref;N_src;J_mem component values or zero certificates",
            "status": "BLOCKED_MISSING_JMEM_VALUE_OR_THEOREM",
            "claim_pass": False,
        },
        {
            "gate_id": "JOG2521_1_PPN_gamma",
            "arena": "PPN gamma",
            "map_formula": "J_mem -> Q_mem -> Q_norm -> B_gamma",
            "required_bundle": "Q_mem source drive plus all Q_i and C_qgamma inputs",
            "status": "BLOCKED_MISSING_QNORM_CHAIN_VALUES",
            "claim_pass": False,
        },
        {
            "gate_id": "JOG2521_2_WEP",
            "arena": "WEP/material composition",
            "map_formula": "J_shadow/direct source weights -> Delta_w_eff -> eta",
            "required_bundle": "no-source-slot theorem or material kernel and source-weight vector",
            "status": "BLOCKED_MISSING_SOURCE_WEIGHT_KERNEL",
            "claim_pass": False,
        },
        {
            "gate_id": "JOG2521_3_clocks",
            "arena": "clock/time tests",
            "map_formula": "J_Hilbert_exchange,J_readout,J_bath -> clock residual",
            "required_bundle": "tau strain/exchange-current bound and clock readout map",
            "status": "BLOCKED_MISSING_CLOCK_EXCHANGE_MAP",
            "claim_pass": False,
        },
        {
            "gate_id": "JOG2521_4_orbits_Newton",
            "arena": "Newton/orbital source normalization",
            "map_formula": "Hilbert source mass plus source-normalization gap -> measured GM/orbital residual",
            "required_bundle": "ell_J/tau/worldtube closure and Poisson/Gauss calibration",
            "status": "BLOCKED_MISSING_NEWTON_SOURCE_NORMALIZATION_CERTIFICATE",
            "claim_pass": False,
        },
        {
            "gate_id": "JOG2521_5_local_GR",
            "arena": "local GR/Newton recovery",
            "map_formula": "J_mem=0 or bounded plus B_mem/Q_mem/CDB/boundary/projection residual gates",
            "required_bundle": "full local residual vector below bounds",
            "status": "BLOCKED_NO_LOCAL_GR_CLAIM",
            "claim_pass": False,
        },
    ]
    return [base_row(score_ready=False, accepted_for_scoring=False, **entry) for entry in entries]


def dryrun_rows() -> list[dict[str, Any]]:
    entries = [
        {
            "case_id": "DRY2521_0_vacuum_wording",
            "case_description": "set J_mem=0 because local exterior is called vacuum",
            "missing_requirements": "m-blind matter action; no bath/readout/history/domain/worldtube drive; no source-shadow",
            "result_status": "REJECT",
            "blocking_markers": "VACUUM_WORDING_NOT_SOURCE_CURRENT_THEOREM",
            "pass_fail": "BLOCKED_NONCLAIM",
            "claim_pass": False,
        },
        {
            "case_id": "DRY2521_1_Hilbert_current_as_silence",
            "case_description": "use Hilbert current definition as proof that memory current is zero",
            "missing_requirements": "orthogonality/no direct memory coupling/no re-entry theorem",
            "result_status": "REJECT",
            "blocking_markers": "SOURCE_MASS_ROUTE_NOT_JMEM_ZERO",
            "pass_fail": "BLOCKED_NONCLAIM",
            "claim_pass": False,
        },
        {
            "case_id": "DRY2521_2_response_doublet_symmetry",
            "case_description": "set J_mem=0 by response-doublet exchange symmetry",
            "missing_requirements": "parent doublets; even matter readout; boundary zero; PPN lock",
            "result_status": "REJECT",
            "blocking_markers": "RDT1011_FAIL_CURRENT_CLAIM",
            "pass_fail": "BLOCKED_NONCLAIM",
            "claim_pass": False,
        },
        {
            "case_id": "DRY2521_3_stationary_subbranch_as_global",
            "case_description": "promote stationary compact exterior q_loc theorem to full dynamic J_mem silence",
            "missing_requirements": "dynamic exchange current; parent scale; source-shadow; metric stress closure",
            "result_status": "REJECT",
            "blocking_markers": "STATIONARY_BRANCH_ONLY",
            "pass_fail": "BLOCKED_NONCLAIM",
            "claim_pass": False,
        },
        {
            "case_id": "DRY2521_4_numeric_Jmem_without_units",
            "case_description": "score finite J_mem without units/source path/A_ref/N_src",
            "missing_requirements": "units;parent source;normalization;Q_mem insertion",
            "result_status": "REJECT",
            "blocking_markers": "MISSING_JMEM_RUNNER_BUNDLE",
            "pass_fail": "BLOCKED_NONCLAIM",
            "claim_pass": False,
        },
        {
            "case_id": "DRY2521_5_future_complete_Jmem",
            "case_description": "future J_mem row with zero certificates or sourced component bounds and arena maps",
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
            "decision_id": "DEC2521_0_zero_status",
            "decision": "do not claim J_mem=0",
            "rationale": "Hilbert source bridge and stationary exterior route are useful but do not close direct memory source, readout, bath, shadow, or dynamic exchange clauses",
            "next_action": "retain finite J_mem drive row",
            "status": "ACTIVE",
        },
        {
            "decision_id": "DEC2521_1_best_subtarget",
            "decision": "attack direct matter m-blind descent next",
            "rationale": "the most defensible first zero is delta S_matter/delta m=0 before readout; it is narrower than full source-current silence",
            "next_action": "prove direct matter-to-memory coupling absent or bound J_direct_matter",
            "status": "ACTIVE",
        },
        {
            "decision_id": "DEC2521_2_hilbert_route",
            "decision": "keep Hilbert current as Newton/source-mass bridge, not J_mem eraser",
            "rationale": "conflating source mass with memory-drive silence would hide the coupling problem",
            "next_action": "reuse Hilbert route only for source normalization once residual drives are handled",
            "status": "ACTIVE",
        },
        {
            "decision_id": "DEC2521_3_fibre_queue",
            "decision": "keep fibre B_h queued after direct Jmem subtarget",
            "rationale": "memory source-current blocker is now sharper and still upstream of Qmem scoring",
            "next_action": "renumber fibre queue after matter-memory direct coupling target",
            "status": "ACTIVE",
        },
    ]
    return [base_row(valid_for_claim=False, claim_allowed=False, **entry) for entry in entries]


def next_target_rows() -> list[dict[str, Any]]:
    entries = [
        {
            "route_id": "NEXT2521_0_selected",
            "selection_status": "selected",
            "target_file": "2522-Y5-R2FR-matter-memory-direct-coupling-zero-or-Jdirect-bound.md",
            "target_script": "scripts/Y5_R2FR_matter_memory_direct_coupling_zero_or_Jdirect_bound_2522.py",
            "objective": "prove delta S_matter/delta m=0 from parent matter m-blind descent before readout, or stage a finite J_direct_matter bound row with units and source paths",
            "success_condition": "direct matter-to-memory source is theorem-zero or retained as a finite nonclaim component feeding J_mem and Q_mem",
            "do_not_do": "do not use exterior vacuum wording; do not import Hilbert source mass as silence; do not claim WEP/Newton/local GR",
        },
        {
            "route_id": "NEXT2521_1_fibre_queue",
            "selection_status": "queued_after_direct_Jmem",
            "target_file": "2523-Y5-R2FR-fibre-Bh-finite-row-or-hidden-visible-grammar-reentry.md",
            "target_script": "scripts/Y5_R2FR_fibre_Bh_finite_row_or_hidden_visible_grammar_reentry_2523.py",
            "objective": "classify fibre B_h with hidden-visible grammar reentry or finite fibre coefficient rows after direct memory source-current lane is handled",
            "success_condition": "B_h has theorem-zero evidence or finite nonclaim Z_h/M2_h/B_h/C_h/source-charge rows",
            "do_not_do": "do not let memory closure erase fibre residuals",
        },
    ]
    return [base_row(valid_for_claim=False, claim_allowed=False, **entry) for entry in entries]


def branch_copy_rows() -> list[dict[str, Any]]:
    copy_specs = [
        ("jmem_zero_audit", OUTPUTS["jmem_zero_audit"], BRANCH_COPIES["jmem_zero_audit"]),
        ("jmem_drive_bound_rows", OUTPUTS["jmem_drive_bound_rows"], BRANCH_COPIES["jmem_drive_bound_rows"]),
        ("source_current_contract", OUTPUTS["source_current_contract"], BRANCH_COPIES["source_current_contract"]),
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
    zero_rows = rows_by_name["jmem_zero_audit"]
    drive_rows = rows_by_name["jmem_drive_bound_rows"]

    add("VAL2521_00_sources_exist", all(str(row["path_exists"]) == "True" for row in source_rows))
    add("VAL2521_01_source_needles", all(str(row["source_pass"]) == "True" for row in source_rows))
    add(
        "VAL2521_02_conditional_zero_written",
        any(row["audit_id"] == "JZ2521_0_conditional_zero_theorem" for row in zero_rows),
        "conditional J_mem zero theorem skeleton is recorded",
    )
    add(
        "VAL2521_03_zero_not_promoted",
        any(
            row["audit_id"] == "JZ2521_7_verdict"
            and row["result"] == "JMEM_ZERO_THEOREM_NOT_DERIVED_STAGE_DRIVE_BOUND_ROWS"
            for row in zero_rows
        ),
        "J_mem zero remains unclaimed",
    )
    add(
        "VAL2521_04_bound_rows_complete",
        all(
            any(row["row_id"] == required for row in drive_rows)
            for required in [
                "JDRV2521_0_Jmem_total",
                "JDRV2521_1_direct_matter",
                "JDRV2521_2_Hilbert_exchange",
                "JDRV2521_4_readout_projector",
                "JDRV2521_7_shadow_weight",
                "JDRV2521_9_Qmem_insertion",
            ]
        ),
        "drive rows include total, direct matter, exchange, readout, shadow and Qmem insertion",
    )
    add(
        "VAL2521_05_bound_rows_nonclaim",
        all(str(row["accepted_for_scoring"]) == "False" and str(row["claim_pass"]) == "False" for row in drive_rows),
        "all J_mem drive rows are blocked for scoring",
    )
    add(
        "VAL2521_06_contract_separates_Hilbert",
        any(
            row["contract_id"] == "SCC2521_1_hilbert_source_separation"
            and row["current_status"] == "PASS_AS_CONTRACT_NONCLAIM"
            for row in rows_by_name["source_current_contract"]
        ),
        "Hilbert source mass route is separated from J_mem silence",
    )
    add(
        "VAL2521_07_observable_gates_blocked",
        all(str(row["claim_pass"]) == "False" and str(row["status"]).startswith("BLOCKED") for row in rows_by_name["observable_gate"]),
        "Qmem/PPN/WEP/clock/orbit/local-GR gates remain blocked",
    )
    add(
        "VAL2521_08_dryruns_block_bad_rows",
        all(str(row["claim_pass"]) == "False" for row in rows_by_name["dryrun_results"])
        and all(str(row["result_status"]) in {"REJECT", "WOULD_ACCEPT_SCHEMA_IF_REAL_FILES_AND_VALUES_EXIST"} for row in rows_by_name["dryrun_results"]),
        "vacuum wording, Hilbert-as-silence, doublet symmetry, stationary overpromotion and incomplete numeric rows do not score",
    )
    add(
        "VAL2521_09_next_target_direct_J",
        any(row["route_id"] == "NEXT2521_0_selected" and "Jdirect" in row["target_file"] for row in rows_by_name["next_target"]),
        "direct matter-memory coupling selected next",
    )
    add("VAL2521_10_no_claim_flags", no_claim_flags(rows_by_name))
    add(
        "VAL2521_11_branch_copies",
        all(str(row["copied"]) == "True" and str(row["parse_ok"]) == "True" for row in rows_by_name["branch_copies"]),
    )
    formalization = ROOT.parent / "formalization-workbench"
    formalization_hits = [
        path
        for path in formalization.rglob("*2521*")
        if ".venv" not in path.parts and "site-packages" not in path.parts
    ] if formalization.exists() else []
    add(
        "VAL2521_12_no_formalization_artifacts",
        len(formalization_hits) == 0,
        ";".join(str(path) for path in formalization_hits),
    )
    add("VAL2521_13_pycache_absent", not (Path(__file__).resolve().parent / "__pycache__").exists())

    for name, path in OUTPUTS.items():
        if name == "validation":
            continue
        ok, count, message = csv_rows_parse(path)
        add(f"VAL2521_CSV_{path.stem}", ok, f"{message}; rows={count}")
    for key, path in BRANCH_COPIES.items():
        ok, count, message = csv_rows_parse(path)
        add(f"VAL2521_COPY_CSV_{key}", ok, f"{message}; rows={count}")

    overall = all(row["status"] == "PASS" for row in checks)
    checks.append(
        base_row(
            check_id="VAL2521_OVERALL",
            status="PASS" if overall else "FAIL",
            detail="2521 formulates the conditional J_mem source-current zero theorem, refuses vacuum/Hilbert/doublet/stationary shortcuts, stages finite drive rows, and selects direct matter-memory coupling next.",
            valid_for_claim=False,
            claim_allowed=False,
        )
    )
    return checks


def write_doc(rows_by_name: dict[str, list[dict[str, Any]]]) -> None:
    DOC.write_text(
        "\n".join(
            [
                "# 2521 - Jmem Source-Current Zero or Memory Drive Bound",
                "",
                "**Current verdict:** `J_mem=0` is not derived. The clean route is now explicit: prove the parent matter/source sector is memory-blind before readout and that bath, history, domain, worldtube, and source-shadow channels do not re-enter the memory Euler equation.",
                "",
                "**Main gain:** the Hilbert current route is separated from the memory-source route. `J_M^nu=ell_J T^{nu rho} tau_rho` is a good source-mass bridge, but it does not erase `J_mem`. The finite `J_mem` drive is now split into direct matter, Hilbert exchange, bath, readout, history, domain, worldtube, shadow, scale, and `Q_mem` insertion rows.",
                "",
                "**Claim discipline:** no source-current zero, WEP, Newton, PPN, R10, clock, orbit, local-GR, memory no-hair, or GitHub/public claim is made.",
                "",
                "## Source Register",
                md_table(rows_by_name["source_register"], ["source_id", "source_path", "path_exists", "found_needles", "source_pass", "role"]),
                "",
                "## Jmem Zero Audit",
                md_table(rows_by_name["jmem_zero_audit"], ["audit_id", "claim_piece", "formal_statement", "result", "blocking_gap", "effect"]),
                "",
                "## Source Current Descent Contract",
                md_table(rows_by_name["source_current_contract"], ["contract_id", "object", "contract", "zero_condition", "current_status", "missing"]),
                "",
                "## Jmem Drive Bound Rows",
                md_table(rows_by_name["jmem_drive_bound_rows"], ["row_id", "quantity", "row_role", "formula_or_bound", "required_inputs", "current_status", "observable_links"]),
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
        "jmem_zero_audit": jmem_zero_audit_rows(),
        "source_current_contract": source_current_contract_rows(),
        "jmem_drive_bound_rows": jmem_drive_bound_rows(),
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

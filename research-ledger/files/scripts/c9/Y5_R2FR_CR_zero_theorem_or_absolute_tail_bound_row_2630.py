from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
PROJECT = ROOT.parent
RESIDUALS = ROOT / "source-intake" / "mts_residuals"
LOCAL_BOUNDS = ROOT / "source-intake" / "local_bounds"
RAB_QUEUE = ROOT / "source-intake" / "rab-sector" / "acquisition-queue"
FORMALIZATION = PROJECT / "formalization-workbench"
DOC_PATH = ROOT / "2630-Y5-R2FR-CR-zero-theorem-or-absolute-tail-bound-row.md"

PREFIX = "P8_Y5_CR_ZERO_ROLLFORWARD_2630"

OUTPUTS = {
    "source_register": RESIDUALS / f"{PREFIX}_SOURCE_REGISTER.csv",
    "rollforward": RESIDUALS / f"{PREFIX}_ZERO_THEOREM_ROLLFORWARD.csv",
    "tail_bound": RESIDUALS / f"{PREFIX}_ABSOLUTE_TAIL_BOUND_IMPORT.csv",
    "residual_vector": RESIDUALS / f"{PREFIX}_RAB_RESIDUAL_VECTOR_IMPORT.csv",
    "arena_blocks": RESIDUALS / f"{PREFIX}_ARENA_BLOCK_IMPORT.csv",
    "claim_gates": RESIDUALS / f"{PREFIX}_CLAIM_GATES.csv",
    "decision": RESIDUALS / f"{PREFIX}_DECISION_LEDGER.csv",
    "next_target": RESIDUALS / f"{PREFIX}_NEXT_TARGET.csv",
    "branch_copies": RESIDUALS / f"{PREFIX}_BRANCH_COPIES.csv",
    "validation": RESIDUALS / "P8_Y5_BRR545_2630_VALIDATION.csv",
}

SOURCES = [
    {
        "source_id": "SRC2630_00_2629_frontier",
        "role": "current 2629 frontier selecting C_R zero or absolute tail bound",
        "path": ROOT / "2629-Y5-R2FR-reciprocity-selector-operator-or-Hcore-source-equation.md",
        "needles": [
            "CR_ZERO_THEOREM_OR_ABSOLUTE_TAIL_BOUND_SELECTED_NEXT",
            "RECIPROCITY_SELECTOR_OR_HCORE_NOT_DERIVED_CURRENT_CORPUS",
            "C_R theorem-zero versus absolute tail bound",
        ],
    },
    {
        "source_id": "SRC2630_01_2629_validation",
        "role": "2629 validation pass",
        "path": RESIDUALS / "P8_Y5_BRR545_2629_VALIDATION.csv",
        "needles": ["VAL2629_OVERALL", "PASS"],
    },
    {
        "source_id": "SRC2630_02_1872_zero_bound",
        "role": "prior C_R zero/tail-bound target already executed",
        "path": ROOT / "1872-Y5-R2FR-CR-zero-theorem-or-absolute-tail-bound-row.md",
        "needles": [
            "CR_ZERO_NOT_PROVED_CURRENT_CORPUS",
            "ABSOLUTE_CR_TAIL_BOUND_LEDGER_READY_NONCLAIM",
            "BOUNDARY_SILENCE_PARENT_CONTRACT_SELECTED_NEXT",
        ],
    },
    {
        "source_id": "SRC2630_03_1873_boundary_contract",
        "role": "boundary silence parent contract and closure demotion",
        "path": ROOT / "1873-Y5-R2FR-boundary-silence-parent-contract-for-CR-zero-or-residual-closure.md",
        "needles": [
            "BOUNDARY_SILENCE_PARENT_CONTRACT_EXACTLY_STATED",
            "CURRENT_LOCAL_CR_ZERO_ROUTE_DEMOTED_TO_RESIDUAL_CLOSURE",
            "PARENT_DOMAIN_VERTICALITY_OR_EXPLICIT_RESIDUAL_FIELD_SELECTED_NEXT",
        ],
    },
    {
        "source_id": "SRC2630_04_1874_verticality",
        "role": "R_AB verticality rejected under available observer map",
        "path": ROOT / "1874-Y5-R2FR-parent-domain-verticality-for-RAB-or-explicit-residual-field.md",
        "needles": [
            "PARENT_DOMAIN_VERTICALITY_NOT_DERIVED",
            "RAB_CLASSIFIED_AS_EXPLICIT_RESIDUAL_FIELD_CURRENTLY",
            "RAB_RESIDUAL_OPERATOR_SOURCE_VECTOR_SELECTED_NEXT",
        ],
    },
    {
        "source_id": "SRC2630_05_1875_vector",
        "role": "explicit R_AB residual vector and routing matrix",
        "path": ROOT / "1875-Y5-R2FR-RAB-residual-operator-source-vector-and-test-routing.md",
        "needles": [
            "RAB_RESIDUAL_VECTOR_READY_NONCLAIM",
            "MASSLESS_AND_FINITE_ROUTES_SEPARATED",
            "BLOCKING_RUNNER_DRYRUN_SELECTED_NEXT",
        ],
    },
    {
        "source_id": "SRC2630_06_1876_runner",
        "role": "machine-readable all-arena blocking dry-run",
        "path": ROOT / "1876-Y5-R2FR-RAB-residual-vector-blocking-runner-dryrun.md",
        "needles": [
            "BLOCKING_RUNNER_DRYRUN_PASS_ALL_ARENAS_BLOCKED",
            "R10_MASSLESS_ROUTE_FORBIDDEN_MACHINE_READABLE",
            "DERIVATION_PRIORITY_RETURNS_TO_QSHAPE_OR_LAMBDAR",
        ],
    },
    {
        "source_id": "SRC2630_07_1878_dobs",
        "role": "q_shape readout/coframe kernel not derived",
        "path": ROOT / "1878-Y5-R2FR-qshape-readout-functor-kernel-or-parent-category-principle.md",
        "needles": [
            "DOBS_E_KERNEL_NOT_DERIVED_CURRENT_CORPUS",
            "RADIAL_CELL_VARIATION_HAS_VISIBLE_COFAME_PROJECTION_UNLESS_PARENT_SILENCED",
            "PARENT_COFRAME_OWNERSHIP_OR_BG_BOUND_SELECTED_NEXT",
        ],
    },
    {
        "source_id": "SRC2630_08_2489_ppn_vector",
        "role": "current no-shadow/PPN vector gate remains unsigned",
        "path": ROOT / "2489-Y5-R2FR-first-common-frame-PPN-response-kernel-or-parent-no-shadow-clause.md",
        "needles": [
            "PARENT_NO_SHADOW_CLAUSE_STILL_UNSIGNED",
            "GAMMA_ONLY_PASS_FORBIDDEN",
            "DELTA_P_BETA_DISFORMAL_VECTOR_OR_NO_SHADOW_SELECTED",
        ],
    },
]


def ensure_dirs() -> None:
    for directory in (RESIDUALS, LOCAL_BOUNDS, RAB_QUEUE):
        directory.mkdir(parents=True, exist_ok=True)


def read_text(path: Path) -> str:
    if not path.exists():
        return ""
    return path.read_text(encoding="utf-8", errors="ignore")


def bool_text(value: bool) -> str:
    return "True" if value else "False"


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    if not rows:
        raise ValueError(f"empty rows for {path}")
    path.parent.mkdir(parents=True, exist_ok=True)
    fieldnames: list[str] = []
    for row in rows:
        for key in row:
            if key not in fieldnames:
                fieldnames.append(key)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def csv_parses(path: Path) -> bool:
    try:
        return bool(read_csv(path))
    except Exception:
        return False


def source_register_rows() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for source in SOURCES:
        path = source["path"]
        text = read_text(path)
        exists = path.exists()
        needles_present = exists and all(needle in text for needle in source["needles"])
        rows.append(
            {
                "source_id": source["source_id"],
                "role": source["role"],
                "source_path": str(path),
                "exists": bool_text(exists),
                "needles_present": bool_text(needles_present),
                "needles": "; ".join(source["needles"]),
                "valid_for_claim": "False",
            }
        )
    return rows


def rollforward_rows() -> list[dict[str, Any]]:
    return [
        {
            "roll_id": "CRR2630_0_2629_frontier",
            "target": "C_R=0/Pi_R=0 theorem versus absolute tail bound",
            "imported_status": "TARGET_SELECTED_BY_2629",
            "current_verdict": "resolved_by_existing_1872_to_1878_chain_as_nonclaim",
            "reason": "2629 stopped at the fork; older executed checkpoints already attacked the fork and recorded the failure modes.",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            "roll_id": "CRR2630_1_zero_theorem",
            "target": "C_R=0 or Pi_R=0",
            "imported_status": "CR_ZERO_NOT_PROVED_CURRENT_CORPUS",
            "current_verdict": "not_derived",
            "reason": "asymptotic flatness does not kill C_R/r; boundary variation/source neutrality/no-marker routes remain parent-unsigned.",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            "roll_id": "CRR2630_2_boundary_contract",
            "target": "parent boundary silence contract",
            "imported_status": "BOUNDARY_SILENCE_PARENT_CONTRACT_EXACTLY_STATED",
            "current_verdict": "exact_conditional_not_parent_signed",
            "reason": "if all clauses close, Pi_R=0 follows; current corpus leaves verticality, matter descent, boundary silence, hidden tails, and no-cancellation unsigned.",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            "roll_id": "CRR2630_3_verticality",
            "target": "R_AB as q-vertical representative",
            "imported_status": "PARENT_DOMAIN_VERTICALITY_NOT_DERIVED",
            "current_verdict": "explicit_residual_field_currently",
            "reason": "R_AB=ln(T^2 S)=2 ln(J_q) is visible under the available observer-cell map unless a q_shape or constraint-first parent theorem is supplied.",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            "roll_id": "CRR2630_4_qshape_category",
            "target": "q_shape readout functor or category principle",
            "imported_status": "DOBS_E_KERNEL_NOT_DERIVED_CURRENT_CORPUS",
            "current_verdict": "coframe_readout_leak_rows_retained",
            "reason": "Dq_shape[v_R]=0 is weaker than DObs_e[v_R]=0; common coframe/Weyl/disformal/endpoint leaks remain possible.",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            "roll_id": "CRR2630_5_no_shadow_ppn",
            "target": "parent no-shadow/full PPN vector gate",
            "imported_status": "PARENT_NO_SHADOW_CLAUSE_STILL_UNSIGNED",
            "current_verdict": "gamma_only_pass_forbidden",
            "reason": "Cassini gamma kernel exists as a constraint, but beta, disformal/preferred-frame, source-prefactor, endpoint and readout tails remain open.",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
    ]


def tail_bound_rows() -> list[dict[str, Any]]:
    return [
        {
            "bound_id": "ATB2630_0_CR_abs",
            "quantity": "C_R_abs",
            "formula_or_contract": "|q_R| = |C_R| c^2/(2 G M_*)",
            "existing_source": str(RESIDUALS / "P8_Y5_PARENT_QLOC_1872_CR_PIR_DELTAGAMMA_BOUND_ROWS_NONCLAIM.csv"),
            "current_status": "MISSING_C_R_VALUE_OR_ZERO_THEOREM",
            "blocks": "PPN;orbital;local_GR",
            "valid_prediction_row": "False",
            "valid_for_claim": "False",
            "claim_allowed": "False",
        },
        {
            "bound_id": "ATB2630_1_PiR_abs",
            "quantity": "Pi_R_abs",
            "formula_or_contract": "|C_R|=|Pi_R|/|kappa_W| only after signed boundary orientation",
            "existing_source": str(RESIDUALS / "P8_Y5_PARENT_QLOC_1872_CR_PIR_DELTAGAMMA_BOUND_ROWS_NONCLAIM.csv"),
            "current_status": "MISSING_Pi_R_BOUND_OR_ZERO_THEOREM;MISSING_BOUNDARY_SIGN_ORIENTATION;MISSING_KAPPA_W",
            "blocks": "PPN;orbital;local_GR",
            "valid_prediction_row": "False",
            "valid_for_claim": "False",
            "claim_allowed": "False",
        },
        {
            "bound_id": "ATB2630_2_Mstar",
            "quantity": "M_star_same_frame",
            "formula_or_contract": "|C_R| <= (2 G M_*/c^2) |Delta gamma|_max",
            "existing_source": str(RESIDUALS / "P8_Y5_PARENT_QLOC_1644_NONCIRCULAR_DENOMINATOR_BLOCKERS.csv"),
            "current_status": "MISSING_SAME_FRAME_PARENT_SOURCE_MASS;ORBITAL_GM_IMPORT_REJECTED_AS_CIRCULAR",
            "blocks": "PPN;orbital;Newton_source_normalization",
            "valid_prediction_row": "False",
            "valid_for_claim": "False",
            "claim_allowed": "False",
        },
        {
            "bound_id": "ATB2630_3_gamma_bound",
            "quantity": "Delta_gamma_abs_max",
            "formula_or_contract": "|Delta gamma|_max=6.7e-05 conservative Cassini input row",
            "existing_source": str(RESIDUALS / "P8_Y5_PARENT_QLOC_1852_PPN_OBSERVABLE_BOUND.csv"),
            "current_status": "SOURCE_BACKED_BOUND_INPUT_ONLY_NONCLAIM",
            "blocks": "does_not_block_as_external_bound;MTS_inputs_still_block",
            "valid_prediction_row": "False",
            "valid_for_claim": "False",
            "claim_allowed": "False",
        },
        {
            "bound_id": "ATB2630_4_absolute_vector",
            "quantity": "absolute_local_residual_vector",
            "formula_or_contract": "all local residual components must be zero or bounded with no cancellation credit",
            "existing_source": str(RESIDUALS / "P8_Y5_PARENT_QLOC_1875_RAB_RESIDUAL_OPERATOR_SOURCE_VECTOR.csv"),
            "current_status": "MISSING_NO_CANCELLATION_GUARD",
            "blocks": "all_local_arenas",
            "valid_prediction_row": "False",
            "valid_for_claim": "False",
            "claim_allowed": "False",
        },
    ]


def residual_vector_rows() -> list[dict[str, Any]]:
    return [
        {
            "vector_id": "RVI2630_0_RAB_status",
            "component": "R_AB branch status",
            "imported_result": "R_AB explicit residual field until q_shape/constraint/no-pole theorem is signed",
            "current_status": "RESIDUAL_VECTOR_READY_NONCLAIM",
            "required_to_promote": "parent verticality or constraint/no-pole, plus matter/boundary/readout/no-cancellation closure",
            "valid_for_claim": "False",
            "claim_allowed": "False",
        },
        {
            "vector_id": "RVI2630_1_massless_route",
            "component": "C_R/r massless tail",
            "imported_result": "routes to PPN/orbital/light-time, not R10 alpha(lambda)",
            "current_status": "MISSING_C_R_PIR_KAPPA_MSTAR_OR_ZERO_THEOREM",
            "required_to_promote": "C_R/Pi_R/kappa_W/M_* row, tau_PPN/tau_orbital, boundary/readout tails, no-cancellation",
            "valid_for_claim": "False",
            "claim_allowed": "False",
        },
        {
            "vector_id": "RVI2630_2_finite_route",
            "component": "finite Z_R/M_R^2/lambda_range branch",
            "imported_result": "finite R10/clock/orbital route only after same-normalized operator/source rows",
            "current_status": "MISSING_PARENT_OPERATOR_ZR;MISSING_PARENT_OPERATOR_MR2_OR_RANGE_RELATION;MISSING_SOURCE_CHARGE_RESOLUTION",
            "required_to_promote": "Z_R, M_R^2, lambda_range, beta_source/test, tau_R10 and accepted bound curve",
            "valid_for_claim": "False",
            "claim_allowed": "False",
        },
        {
            "vector_id": "RVI2630_3_common_frame",
            "component": "DObs_e/common-frame leak",
            "imported_result": "q_shape alone does not imply observed coframe invisibility",
            "current_status": "MISSING_QSHAPE_READOUT_FUNCTOR;MISSING_PARENT_NO_SHADOW_CLAUSE",
            "required_to_promote": "DObs_e[v_R]=0 theorem or finite b_R/d_R/endpoint/readout kernel rows",
            "valid_for_claim": "False",
            "claim_allowed": "False",
        },
        {
            "vector_id": "RVI2630_4_ppn_full_vector",
            "component": "full PPN residual vector",
            "imported_result": "gamma-only pass forbidden; beta/disformal/source-prefactor/endpoint/readout rows remain",
            "current_status": "MISSING_BETA_RESPONSE_KERNEL;MISSING_DISFORMAL_PPN_PROJECTION;MISSING_ENDPOINT_READOUT_KERNEL",
            "required_to_promote": "delta_p/beta/disformal/source/readout vector filled or theorem-zero in source-normalized gauge",
            "valid_for_claim": "False",
            "claim_allowed": "False",
        },
    ]


def arena_block_rows() -> list[dict[str, Any]]:
    return [
        {
            "arena_id": "ABI2630_0_local_GR",
            "arena": "local_GR/Newton",
            "imported_runner_status": "BLOCKED_NONCLAIM",
            "missing_rows": "verticality_or_constraint;C_R/Pi_R_zero_or_bound;boundary_readout_tail;no_cancellation;source_normalization",
            "forbidden_shortcut": "closure-only R_AB=0 or GR plateau premise",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            "arena_id": "ABI2630_1_PPN_light_time",
            "arena": "PPN/light-time",
            "imported_runner_status": "BLOCKED_NONCLAIM",
            "missing_rows": "C_R/Pi_R/kappa_W/M_*;tau_PPN;beta/disformal/readout vector;no_cancellation",
            "forbidden_shortcut": "gamma-only pass or cancellation against other tails",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            "arena_id": "ABI2630_2_R10",
            "arena": "R10 alpha(lambda)",
            "imported_runner_status": "BLOCKED_NONCLAIM_MASSLESS_ROUTE_FORBIDDEN",
            "missing_rows": "Z_R;M_R^2;lambda_range;source/test charges;tau_R10;accepted bound curve",
            "forbidden_shortcut": "massless C_R/r tail as finite-range Yukawa alpha(lambda)",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            "arena_id": "ABI2630_3_clock_WEP",
            "arena": "clock/WEP/material",
            "imported_runner_status": "BLOCKED_NONCLAIM",
            "missing_rows": "constant/marker theorem;source weight vector;tau_clock;tau_WEP;material tensors;no_cancellation",
            "forbidden_shortcut": "assuming matter blindness from unsigned quotient descent",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            "arena_id": "ABI2630_4_orbital",
            "arena": "orbital massless and finite branches",
            "imported_runner_status": "BLOCKED_NONCLAIM",
            "missing_rows": "C_R/Pi_R tail or finite operator;M_*;tau_orbital;worldtube/Gauss closure;baseline comparison",
            "forbidden_shortcut": "observed orbital GM as noncircular source denominator",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
    ]


def claim_gate_rows() -> list[dict[str, Any]]:
    return [
        {
            "gate_id": "GATE2630_0_CR_zero",
            "claim": "C_R=0/Pi_R=0 is derived",
            "evidence_status": "CR_ZERO_NOT_PROVED_CURRENT_CORPUS",
            "gate_pass": "False",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            "gate_id": "GATE2630_1_tail_bound",
            "claim": "absolute C_R/Pi_R tail bound is score-ready",
            "evidence_status": "BOUND_TEMPLATE_READY_NONCLAIM;MTS_NUMERATOR_DENOMINATOR_NO_CANCELLATION_MISSING",
            "gate_pass": "False",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            "gate_id": "GATE2630_2_residual_vector",
            "claim": "R_AB residual vector is claim-ready",
            "evidence_status": "INTERNAL_NONCLAIM_VECTOR_ONLY",
            "gate_pass": "False",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            "gate_id": "GATE2630_3_local_tests",
            "claim": "local_GR/PPN/R10/clock/WEP/orbital pass",
            "evidence_status": "ALL_ARENAS_BLOCKED_BY_1876_AND_FULL_PPN_VECTOR_OPEN_BY_2489",
            "gate_pass": "False",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            "gate_id": "GATE2630_4_current_progress",
            "claim": "2630 may supersede the 2629 next target",
            "evidence_status": "PASS_AS_PRIVATE_NONCLAIM_ROLLFORWARD_ONLY",
            "gate_pass": "True",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        {
            "decision_id": "DEC2630_0_rollforward",
            "decision": "CR_ZERO_TARGET_ALREADY_EXECUTED_AND_IMPORTED",
            "reason": "1872 through 1878 already attempted the zero theorem, boundary contract, verticality, q_shape/category and DObs_e routes; 2630 imports that status into the current 2629 chain.",
            "next_action": "do not duplicate 1872; use its failure/ledger as current branch evidence",
            "valid_for_claim": "False",
        },
        {
            "decision_id": "DEC2630_1_zero_status",
            "decision": "CR_ZERO_NOT_DERIVED_AND_RAB_REMAINS_EXPLICIT_RESIDUAL",
            "reason": "boundary/source neutrality and q_shape/category routes remain parent-unsigned; observer coframe can see radial-cell variation.",
            "next_action": "keep local-GR/Newton blocked unless parent no-shadow/coframe or constraint/no-pole theorem closes",
            "valid_for_claim": "False",
        },
        {
            "decision_id": "DEC2630_2_bound_status",
            "decision": "ABSOLUTE_TAIL_BOUND_LEDGER_READY_NONCLAIM_NOT_SCORE_READY",
            "reason": "Cassini/gamma bound can constrain a completed prediction, but C_R/Pi_R, kappa_W, M_*, tau projections and no-cancellation rows are missing.",
            "next_action": "do not score PPN/orbital; retain rows as acquisition targets",
            "valid_for_claim": "False",
        },
        {
            "decision_id": "DEC2630_3_next",
            "decision": "CURRENT_BRANCH_NO_SHADOW_FULL_PPN_VECTOR_SELECTED_NEXT",
            "reason": "the live bottleneck after CR-zero failure is observed-coframe/no-shadow plus full PPN vector closure, not another gamma-only or R10 shortcut.",
            "next_action": "2631 should consolidate DObs_e/no-shadow/delta_p/beta/disformal/source/readout kernels for the current branch, or keep finite residual rows blocked",
            "valid_for_claim": "False",
        },
    ]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        {
            "next_target": "2631-Y5-R2FR-current-branch-no-shadow-full-PPN-vector-or-residual-kernel-fill.md",
            "script": "scripts/Y5_R2FR_current_branch_no_shadow_full_PPN_vector_or_residual_kernel_fill_2631.py",
            "objective": "consolidate the parent no-shadow/DObs_e gate and full PPN residual vector for the current 2629+ branch: delta_p/q_R, b_R, beta, d_R, w_R, endpoint/readout tails, source normalization, and no-cancellation.",
            "include": "1878 DObs_e kernel failure; 2489 gamma kernel and full vector blockers; 1875/1876 residual vector/block runner; beta/disformal/source/readout rows where already staged",
            "exclude": "gamma-only pass, fitted GM denominator, massless C_R/r into R10, closure-only local GR, cancellation-only scoring, GitHub action, formalization-workbench edits",
            "selected": "True",
            "valid_for_claim": "False",
        },
        {
            "next_target": "2631b-Y5-R2FR-CR-PiR-Mstar-source-row-acquisition.md",
            "script": "scripts/Y5_R2FR_CR_PiR_Mstar_source_row_acquisition_2631b.py",
            "objective": "fallback only: stage CR/PiR/kappa_W/Mstar source-acquisition rows for massless PPN/orbital branch with every claim blocked until source-backed.",
            "include": "C_R_abs;Pi_R_abs;kappa_W;M_star_same_frame;tau_PPN;tau_orbital;absolute residual vector",
            "exclude": "public PPN score, orbital-GM backfill, no-cancellation shortcut",
            "selected": "False",
            "valid_for_claim": "False",
        },
    ]


def copy_branch_outputs() -> list[dict[str, Any]]:
    copy_specs = [
        ("COPY2630_rollforward", "CR_zero_rollforward", OUTPUTS["rollforward"], LOCAL_BOUNDS / "CR_zero_rollforward_2630_NONCLAIM.csv"),
        ("COPY2630_tail_bound", "absolute_tail_bound_import", OUTPUTS["tail_bound"], LOCAL_BOUNDS / "CR_absolute_tail_bound_import_2630_NONCLAIM.csv"),
        ("COPY2630_arena_blocks", "arena_block_import", OUTPUTS["arena_blocks"], LOCAL_BOUNDS / "RAB_arena_block_import_2630_NONCLAIM.csv"),
        ("COPY2630_next", "next_target", OUTPUTS["next_target"], RAB_QUEUE / "JR2630_NO_SHADOW_FULL_PPN_VECTOR_NEXT.csv"),
    ]
    rows: list[dict[str, Any]] = []
    for copy_id, label, source_path, destination_path in copy_specs:
        destination_path.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(source_path, destination_path)
        rows.append(
            {
                "copy_id": copy_id,
                "label": label,
                "source_path": str(source_path),
                "destination_path": str(destination_path),
                "destination_exists": bool_text(destination_path.exists()),
                "csv_parses": bool_text(csv_parses(destination_path)),
                "row_count": len(read_csv(destination_path)) if destination_path.exists() else 0,
            }
        )
    return rows


def any_claim_promoted(rows_by_name: dict[str, list[dict[str, Any]]]) -> bool:
    for rows in rows_by_name.values():
        for row in rows:
            if row.get("valid_for_claim") == "True" or row.get("claim_allowed") == "True":
                return True
    return False


def missing_row_promoted(rows_by_name: dict[str, list[dict[str, Any]]]) -> bool:
    for rows in rows_by_name.values():
        for row in rows:
            row_text = " ".join(str(value) for value in row.values())
            promoted = row.get("valid_for_claim") == "True" or row.get("claim_allowed") == "True"
            if "MISSING_" in row_text and promoted:
                return True
    return False


def validation_rows(rows_by_name: dict[str, list[dict[str, Any]]]) -> list[dict[str, Any]]:
    generated_paths = [path for name, path in OUTPUTS.items() if name != "validation"]
    source_rows = rows_by_name["source_register"]
    roll_rows = rows_by_name["rollforward"]
    tail_rows = rows_by_name["tail_bound"]
    arena_rows = rows_by_name["arena_blocks"]
    gate_rows = rows_by_name["claim_gates"]
    next_rows = rows_by_name["next_target"]
    branch_rows = rows_by_name["branch_copies"]

    checks: list[tuple[str, bool, str]] = [
        (
            "VAL2630_00_sources",
            all(row["exists"] == "True" and row["needles_present"] == "True" for row in source_rows),
            "all cited source paths exist and needles are present",
        ),
        (
            "VAL2630_01_rollforward_import",
            any(row["imported_status"] == "CR_ZERO_NOT_PROVED_CURRENT_CORPUS" for row in roll_rows)
            and any(row["imported_status"] == "DOBS_E_KERNEL_NOT_DERIVED_CURRENT_CORPUS" for row in roll_rows),
            "CR-zero failure and DObs_e kernel failure are imported",
        ),
        (
            "VAL2630_02_tail_bound_nonclaim",
            all(row["valid_for_claim"] == "False" and row["claim_allowed"] == "False" for row in tail_rows),
            "absolute tail bound rows remain nonclaim",
        ),
        (
            "VAL2630_03_arena_blocks",
            all(row["claim_allowed"] == "False" and "BLOCKED" in row["imported_runner_status"] for row in arena_rows),
            "all imported arena statuses are blocked/nonclaim",
        ),
        (
            "VAL2630_04_R10_guard",
            any("massless C_R/r tail" in row["forbidden_shortcut"] for row in arena_rows),
            "massless C_R/r route is forbidden for R10",
        ),
        (
            "VAL2630_05_claim_gates",
            all(row["claim_allowed"] == "False" for row in gate_rows),
            "claim gates do not promote physics claims",
        ),
        (
            "VAL2630_06_no_claim_flags",
            not any_claim_promoted(rows_by_name),
            "no generated claim-sensitive row is promoted",
        ),
        (
            "VAL2630_07_missing_not_ready",
            not missing_row_promoted(rows_by_name),
            "no MISSING_* row is marked claim-ready",
        ),
        (
            "VAL2630_08_next_target",
            any(row["selected"] == "True" and "2631" in row["next_target"] for row in next_rows),
            "2631 current-branch no-shadow/full PPN vector target selected",
        ),
        (
            "VAL2630_09_branch_copies",
            all(row["destination_exists"] == "True" and row["csv_parses"] == "True" for row in branch_rows),
            "branch/local/queue copies exist and parse",
        ),
        (
            "VAL2630_10_formalization_untouched",
            not any(str(path).startswith(str(FORMALIZATION)) for path in generated_paths + [DOC_PATH]),
            "no 2630 outputs are written under formalization-workbench",
        ),
        (
            "VAL2630_11_csv_parse",
            all(csv_parses(path) for path in generated_paths),
            "all generated 2630 CSVs parse",
        ),
        (
            "VAL2630_12_pycache_absent",
            not (ROOT / "scripts" / "__pycache__").exists(),
            "scripts __pycache__ absent",
        ),
    ]
    rows = [
        {
            "check_id": check_id,
            "status": "PASS" if passed else "FAIL",
            "detail": detail,
            "valid_for_claim": "False",
        }
        for check_id, passed, detail in checks
    ]
    rows.append(
        {
            "check_id": "VAL2630_OVERALL",
            "status": "PASS" if all(row["status"] == "PASS" for row in rows) else "FAIL",
            "detail": "2630 CR-zero theorem roll-forward and absolute tail-bound import",
            "valid_for_claim": "False",
        }
    )
    return rows


def markdown_table(rows: list[dict[str, Any]]) -> str:
    if not rows:
        return ""
    headers = list(rows[0].keys())
    lines = [
        "| " + " | ".join(headers) + " |",
        "| " + " | ".join("---" for _ in headers) + " |",
    ]
    for row in rows:
        values = [str(row.get(header, "")).replace("\n", " ").replace("|", "\\|") for header in headers]
        lines.append("| " + " | ".join(values) + " |")
    return "\n".join(lines)


def write_doc(rows_by_name: dict[str, list[dict[str, Any]]]) -> None:
    generated_at = datetime.now(timezone.utc).isoformat()
    sections = [
        ("Source Register", rows_by_name["source_register"]),
        ("Zero Theorem Rollforward", rows_by_name["rollforward"]),
        ("Absolute Tail Bound Import", rows_by_name["tail_bound"]),
        ("R_AB Residual Vector Import", rows_by_name["residual_vector"]),
        ("Arena Block Import", rows_by_name["arena_blocks"]),
        ("Claim Gates", rows_by_name["claim_gates"]),
        ("Decision Ledger", rows_by_name["decision"]),
        ("Next Target", rows_by_name["next_target"]),
        ("Branch Copies", rows_by_name["branch_copies"]),
        ("Validation", rows_by_name["validation"]),
    ]
    body = [
        "# 2630 - Y5 R2/f(R) C_R Zero Theorem Or Absolute Tail-Bound Row",
        "",
        f"Generated: `{generated_at}`",
        "",
        "Status: `Y5_R2FR_2630_CR_zero_not_derived_existing_tail_bound_imported_RAB_residual_vector_current_branch_nonclaim`",
        "",
        "Claim ceiling: no `C_R=0`, no `Pi_R=0`, no `R_AB` verticality theorem, no parent no-shadow theorem, no local-GR/Newton reduction, no PPN/R10/WEP/clock/orbital pass, no GitHub action, and no `formalization-workbench` edit is made.",
        "",
        "## Summary",
        "",
        "2630 does not repeat the old `C_R=0` attempt. It imports the already-executed 1872-1878 chain into the current 2629 frontier.",
        "",
        "The consolidated verdict is sharp: `C_R=0/Pi_R=0` is not derived. Boundary silence is an exact conditional contract, but verticality, q_shape readout, category/no-shadow, same-frame mass, and no-cancellation remain unsigned.",
        "",
        "The practical consequence is also sharp: `R_AB` is an explicit residual field in the current branch. Massless `C_R/r` can only route to PPN/orbital/light-time, finite `Z_R/M_R^2` can only route to R10/finite-range tests, and every arena remains blocked until real theorem-zero or source-backed rows exist.",
        "",
    ]
    for title, rows in sections:
        body.extend([f"## {title}", "", markdown_table(rows), ""])
    body.extend(
        [
            "## Plain-English Verdict",
            "",
            "This is progress by refusing a fake win. The theory cannot currently say local GR follows because `C_R` vanishes; it can only say the exact theorem is known and the missing premises are now named.",
            "",
            "The next useful derivation target is not another `C_R` loop. It is the no-shadow/full-PPN vector gate: either prove the observed coframe/readout cannot see the radial-cell variable, or keep every PPN component as an explicit residual kernel.",
            "",
        ]
    )
    DOC_PATH.write_text("\n".join(body), encoding="utf-8")


def main() -> None:
    ensure_dirs()
    rows_by_name: dict[str, list[dict[str, Any]]] = {
        "source_register": source_register_rows(),
        "rollforward": rollforward_rows(),
        "tail_bound": tail_bound_rows(),
        "residual_vector": residual_vector_rows(),
        "arena_blocks": arena_block_rows(),
        "claim_gates": claim_gate_rows(),
        "decision": decision_rows(),
        "next_target": next_target_rows(),
    }

    for name, rows in rows_by_name.items():
        write_csv(OUTPUTS[name], rows)

    rows_by_name["branch_copies"] = copy_branch_outputs()
    write_csv(OUTPUTS["branch_copies"], rows_by_name["branch_copies"])

    rows_by_name["validation"] = validation_rows(rows_by_name)
    write_csv(OUTPUTS["validation"], rows_by_name["validation"])
    write_doc(rows_by_name)

    print(f"wrote {DOC_PATH}")
    print(f"validation {OUTPUTS['validation']}")


if __name__ == "__main__":
    main()

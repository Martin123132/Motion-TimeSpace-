from __future__ import annotations

import csv
import shutil
from pathlib import Path
from typing import Any


BRANCH_ID = "MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428"
CHECKPOINT_ID = "1878"

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "source-intake" / "mts_residuals"
MICROSCOPE_RESIDUALS = ROOT / "source-intake" / "microscope" / "branch_locked_wep" / "residuals"
QUARANTINE = ROOT / "source-intake" / "microscope" / "quarantine" / CHECKPOINT_ID
QUEUE = ROOT / "source-intake" / "rab-sector" / "acquisition-queue"
FORMALIZATION = ROOT.parent / "formalization-workbench"

DOC = ROOT / "1878-Y5-R2FR-qshape-readout-functor-kernel-or-parent-category-principle.md"

INPUTS = {
    "1877_doc": ROOT / "1877-Y5-R2FR-qshape-or-lambdaR-parent-origin-source-hunt.md",
    "1877_validation": OUT / "P8_Y5_BRR545_1877_VALIDATION.csv",
    "1877_equivalence": OUT / "P8_Y5_PARENT_QLOC_1877_QSHAPE_LAMBDAR_EQUIVALENCE_NO_GO.csv",
    "1877_contract": OUT / "P8_Y5_PARENT_QLOC_1877_PARENT_CONTRACT_REQUIREMENTS.csv",
    "1738_doc": ROOT / "1738-Y5-R2FR-observed-coframe-kernel-zero-or-first-finite-DObs-e-row.md",
    "1738_finite_rows": OUT / "P8_Y5_PARENT_QLOC_1738_FINITE_DOBS_E_SOURCE_ROWS.csv",
    "10_observer_contract": ROOT / "10-observer-map-symplectic-contract.md",
    "1868_typed_grammar": ROOT / "1868-Y5-R2FR-typed-parent-grammar-for-radial-cell-or-coefficient-bound-branch.md",
    "1875_vector": OUT / "P8_Y5_PARENT_QLOC_1875_RAB_RESIDUAL_OPERATOR_SOURCE_VECTOR.csv",
}

SOURCE_NEEDLES = {
    "1877_doc": [
        "QSHAPE_IS_NOT_INDEPENDENT_ESCAPE",
        "DObs_e[v_R] = 0",
    ],
    "1877_validation": [
        "VAL1877_OVERALL,PASS",
    ],
    "1877_equivalence": [
        "QSHAPE_LAMBDAR_EQUIVALENCE_FOR_CURRENT_CORPUS",
        "DOBS_E_BURDEN_REMAINS",
    ],
    "1877_contract": [
        "MISSING_DOBS_E_ZERO",
        "MISSING_PARENT_CATEGORY_PRINCIPLE",
    ],
    "1738_doc": [
        "DOBS_E_KERNEL_ZERO_NOT_SIGNED",
        "SAME_COFRAME_IS_NOT_ENOUGH",
    ],
    "1738_finite_rows": [
        "DOE1738_2_vRAB_Jq",
        "RETAINED_NONCLAIM_DOBS_E_ROW",
    ],
    "10_observer_contract": [
        "theta_0 = T c dt",
        "theta_1 = sqrt(S) dr",
    ],
    "1868_typed_grammar": [
        "TYPED_PARENT_GRAMMAR_NOT_DERIVED_CURRENT_CORPUS",
        "COFRAME_DERIVATIVE_COUNTERMODEL",
    ],
    "1875_vector": [
        "RV1875_0_domain_visibility",
        "MISSING_VERTICALITY_CERTIFICATE_OR_BOUND",
    ],
}

OUTPUTS = {
    "source_register": OUT / "P8_Y5_PARENT_QLOC_1878_SOURCE_REGISTER.csv",
    "coframe_kernel_test": OUT / "P8_Y5_PARENT_QLOC_1878_QSHAPE_COFRAME_KERNEL_TEST.csv",
    "finite_dobs_rows": OUT / "P8_Y5_PARENT_QLOC_1878_FINITE_DOBS_E_LEAK_ROWS.csv",
    "category_principle_audit": OUT / "P8_Y5_PARENT_QLOC_1878_PARENT_CATEGORY_PRINCIPLE_AUDIT.csv",
    "local_gate_map": OUT / "P8_Y5_PARENT_QLOC_1878_LOCAL_GATE_MAP.csv",
    "claim_gate": OUT / "P8_Y5_PARENT_QLOC_1878_CLAIM_GATE.csv",
    "decision": OUT / "P8_Y5_PARENT_QLOC_1878_DECISION_LEDGER.csv",
    "next_target": OUT / "P8_Y5_PARENT_QLOC_1878_NEXT_TARGET.csv",
    "validation": OUT / "P8_Y5_BRR545_1878_VALIDATION.csv",
}


def ensure_dirs() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    MICROSCOPE_RESIDUALS.mkdir(parents=True, exist_ok=True)
    QUARANTINE.mkdir(parents=True, exist_ok=True)
    QUEUE.mkdir(parents=True, exist_ok=True)


def bool_string(value: Any) -> str:
    return str(value).strip().lower()


def path_has_needles(path: Path, needles: list[str]) -> tuple[bool, str]:
    if not path.exists():
        return False, "MISSING_SOURCE_PATH"
    text = path.read_text(encoding="utf-8", errors="ignore")
    missing = [needle for needle in needles if needle not in text]
    if missing:
        return False, "MISSING_NEEDLES=" + ";".join(missing)
    return True, "OK"


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    if not rows:
        raise ValueError(f"no rows for {path}")
    path.parent.mkdir(parents=True, exist_ok=True)
    fieldnames: list[str] = []
    for row in rows:
        for key in row:
            if key not in fieldnames:
                fieldnames.append(key)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()
        for row in rows:
            writer.writerow(row)


def csv_rows(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def source_register_rows() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for source_id, path in INPUTS.items():
        ok, detail = path_has_needles(path, SOURCE_NEEDLES[source_id])
        rows.append(
            {
                "branch_id": BRANCH_ID,
                "checkpoint_id": CHECKPOINT_ID,
                "source_id": source_id,
                "source_path": str(path),
                "required_needles": " ; ".join(SOURCE_NEEDLES[source_id]),
                "source_exists": path.exists(),
                "needle_check": detail,
                "usable_for_1878": ok,
                "valid_for_claim": False,
                "claim_allowed": False,
            }
        )
    return rows


def coframe_kernel_test_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "test_id": "CKT1878_0_chain_rule",
            "claim_piece": "q-basic observed coframe theorem",
            "mathematical_test": "if e_obs=E(q_shape(Phi)) and Dq_shape[v_R]=0, then DObs_e[v_R]=0",
            "result": "EXACT_CONDITIONAL",
            "blocker": "q_shape and E(q_shape) are not parent-signed",
            "proof_closed": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "test_id": "CKT1878_1_component_lemma",
            "claim_piece": "radial-cell variation invisible to observed coframe",
            "mathematical_test": "theta_0=T cdt, theta_1=sqrt(S)dr, C_R=2(ln T+ln sqrt(S)); DObs_e=0 requires the observed T and sqrt(S) variations to vanish unless a new readout gauge is proved",
            "result": "FAIL_CURRENT_CORPUS",
            "blocker": "a nonzero delta C_R has visible coframe projection in the current observed-coframe map",
            "proof_closed": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "test_id": "CKT1878_2_qshape_not_enough",
            "claim_piece": "Dq_shape[v_R]=0 suffices for local GR",
            "mathematical_test": "forget J_q in q_shape and ask whether clocks, rulers, photons, orbits and sources still descend through q_shape",
            "result": "FAIL_CURRENT_CORPUS",
            "blocker": "readout functor proof is missing; Dq_shape kernel is weaker than DObs_e kernel",
            "proof_closed": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "test_id": "CKT1878_3_common_frame_countermodel",
            "claim_piece": "single common coframe implies zero local residual",
            "mathematical_test": "e_obs=exp(b_R C_R)e0 is a universal coframe but DObs_e[partial_C_R]=b_R e_obs",
            "result": "COUNTERMODEL_SURVIVES",
            "blocker": "b_R=0 theorem or numeric bound is missing",
            "proof_closed": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "test_id": "CKT1878_4_category_principle",
            "claim_piece": "parent category makes C_R compatibility-only",
            "mathematical_test": "forbid C_R as independent field, derivative target, source slot, boundary charge, and readout argument",
            "result": "CONTRACT_ONLY",
            "blocker": "parent primitive/constructor category principle not derived",
            "proof_closed": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "test_id": "CKT1878_5_verdict",
            "claim_piece": "q_shape readout kernel or category principle closes",
            "mathematical_test": "CKT1878_0 through CKT1878_4 all parent-signed",
            "result": "DOBS_E_KERNEL_NOT_DERIVED_CURRENT_CORPUS",
            "blocker": "retain finite DObs_e/C_R leak rows",
            "proof_closed": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]


def finite_dobs_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "row_id": "FDOBS1878_0_radial_cell_coframe",
            "symbol": "epsilon_R_cell",
            "direction": "v_RAB/J_q",
            "formula": "epsilon_R_cell := ||(delta ln T, delta ln sqrt(S))|| for fixed q_shape under v_R",
            "needed_for": "local_GR;PPN;WEP;clock;orbital",
            "status": "MISSING_NUMERIC_OR_THEOREM_ZERO",
            "numeric_value": "MISSING_NUMERIC_VALUE",
            "units": "dimensionless_coframe_log_derivative",
            "source_path": "MISSING_SOURCE_PATH",
            "score_ready": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "FDOBS1878_1_common_weyl",
            "symbol": "b_R",
            "direction": "common Weyl dependence on C_R",
            "formula": "e_obs=exp(b_R C_R)e0",
            "needed_for": "PPN;clock;WEP;local_GR",
            "status": "MISSING_B_R_ZERO_THEOREM_OR_BOUND",
            "numeric_value": "MISSING_NUMERIC_VALUE",
            "units": "dimensionless",
            "source_path": "MISSING_SOURCE_PATH",
            "score_ready": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "FDOBS1878_2_common_disformal",
            "symbol": "d_R",
            "direction": "common disformal/current residual",
            "formula": "g_obs=C(C_R)g0+D(C_R)u_mu u_nu",
            "needed_for": "PPN;clock;orbital;local_GR",
            "status": "MISSING_DISFORMAL_ZERO_THEOREM_OR_BOUND",
            "numeric_value": "MISSING_NUMERIC_VALUE",
            "units": "dimensionless_or_declared_disformal_scale",
            "source_path": "MISSING_SOURCE_PATH",
            "score_ready": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "FDOBS1878_3_boundary_endpoint",
            "symbol": "epsilon_endpoint_R",
            "direction": "boundary/endpoint coframe leak",
            "formula": "P_loc partial_{Q_endpoint} E(q_shape,Q_endpoint)",
            "needed_for": "PPN;clock;orbital;local_GR",
            "status": "MISSING_BOUNDARY_ENDPOINT_SILENCE_OR_BOUND",
            "numeric_value": "MISSING_NUMERIC_VALUE",
            "units": "dimensionless_projection_norm",
            "source_path": "MISSING_SOURCE_PATH",
            "score_ready": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "FDOBS1878_4_total",
            "symbol": "epsilon_DObs_R_abs",
            "direction": "absolute observed-coframe leak envelope",
            "formula": "epsilon_R_cell+|b_R|+|d_R|+|epsilon_endpoint_R| with no cancellation credit",
            "needed_for": "all_local_arenas",
            "status": "MISSING_ABSOLUTE_DOBS_ENVELOPE",
            "numeric_value": "MISSING_NUMERIC_VALUE",
            "units": "dimensionless",
            "source_path": "MISSING_SOURCE_PATH",
            "score_ready": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]


def category_principle_audit_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "audit_id": "CPA1878_0_primitives",
            "principle_clause": "motion/time/space primitives are declared before metric readout",
            "current_status": "MISSING_PARENT_PRIMITIVE_LIST",
            "if_closed": "C_R can be typed as compatibility data rather than an ordinary scalar",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "audit_id": "CPA1878_1_no_readout_argument",
            "principle_clause": "observed coframe/readout does not accept C_R/J_q as an independent argument",
            "current_status": "MISSING_QSHAPE_READOUT_FUNCTOR",
            "if_closed": "DObs_e[v_R]=0 follows by q-basicity",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "audit_id": "CPA1878_2_no_derivatives",
            "principle_clause": "no derivative operator may act on C_R as a scalar",
            "current_status": "MISSING_PARENT_CATEGORY_PRINCIPLE",
            "if_closed": "Z_R kinetic residue becomes illegal",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "audit_id": "CPA1878_3_auxiliary",
            "principle_clause": "Lambda_R C_R is parent-owned and Dirac/auxiliary chain closes",
            "current_status": "MISSING_LAMBDAR_ORIGIN_DIRAC_CHAIN",
            "if_closed": "C_R=0 before readout without closure smuggling",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "audit_id": "CPA1878_4_matter_boundary",
            "principle_clause": "matter, source, boundary and endpoint maps are q-basic or proper/exact",
            "current_status": "MISSING_MATTER_BOUNDARY_READOUT_SILENCE",
            "if_closed": "J_R, Q_R and endpoint tails cannot revive the radial-cell residual",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "audit_id": "CPA1878_5_verdict",
            "principle_clause": "parent category principle closes local radial-cell invisibility",
            "current_status": "CATEGORY_PRINCIPLE_NOT_DERIVED_CURRENT_CORPUS",
            "if_closed": "return to local-GR derivation; otherwise finite DObs/Q_R rows remain",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]


def local_gate_map_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "gate_id": "LGM1878_0_local_GR",
            "arena": "local_GR/Newton",
            "needs": "epsilon_DObs_R_abs=0 or bounded plus source/conservation/beta gates",
            "current_status": "BLOCKED_BY_DOBS_E_KERNEL",
            "blocking_rows": "FDOBS1878_0_radial_cell_coframe;FDOBS1878_4_total",
            "score_ready": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "gate_id": "LGM1878_1_PPN",
            "arena": "PPN_gamma_beta_light_time",
            "needs": "coframe leak, q_R_hat, boundary/readout and beta/conservation residuals",
            "current_status": "BLOCKED_BY_COFAME_AND_QR_ROWS",
            "blocking_rows": "FDOBS1878_0_radial_cell_coframe;RV1875_5_massless_tail;RV1875_9_no_cancellation",
            "score_ready": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "gate_id": "LGM1878_2_WEP_clock",
            "arena": "WEP_clock_material",
            "needs": "common coframe derivative zero/bound plus marker/source/readout descent",
            "current_status": "BLOCKED_BY_COMMON_FRAME_COUNTERMODEL",
            "blocking_rows": "FDOBS1878_1_common_weyl;FDOBS1878_2_common_disformal;RV1875_7_constants_markers",
            "score_ready": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "gate_id": "LGM1878_3_orbital",
            "arena": "orbital_light_time",
            "needs": "coframe leak and orbital projection in same source frame",
            "current_status": "BLOCKED_BY_DOBS_AND_TAU_ORBITAL",
            "blocking_rows": "FDOBS1878_4_total;RV1875_8_projection_kernels",
            "score_ready": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "gate_id": "LGM1878_4_R10",
            "arena": "R10_finite_range",
            "needs": "finite operator/source/projection route; massless/coframe rows cannot be routed into alpha(lambda)",
            "current_status": "SEPARATE_FINITE_ROUTE_BLOCKED_NONCLAIM",
            "blocking_rows": "RV1875_2_operator_ZR;RV1875_3_operator_MR2_lambda;RV1875_4_bulk_source_charges",
            "score_ready": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]


def claim_gate_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "claim_id": "CG1878_0_internal",
            "claim": "1878 coframe kernel test may guide next derivation",
            "status": "ALLOW_INTERNAL_NONCLAIM_TEST",
            "reason": "it records an exact conditional theorem and finite leak rows without promoting claims",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "claim_id": "CG1878_1_DObs",
            "claim": "DObs_e[v_R]=0 is derived",
            "status": "BLOCKED",
            "reason": "q_shape readout functor and parent coframe ownership are missing",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "claim_id": "CG1878_2_category",
            "claim": "parent category principle makes C_R compatibility-only",
            "status": "BLOCKED",
            "reason": "primitive list, operator permissions, auxiliary origin, matter descent, and boundary silence are unsigned",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "claim_id": "CG1878_3_local_GR",
            "claim": "local GR/Newton limit follows from q_shape readout",
            "status": "BLOCKED",
            "reason": "coframe kernel is necessary but not sufficient; beta/conservation/source gates remain open",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "decision_id": "DEC1878_0_result",
            "decision": "DOBS_E_KERNEL_NOT_DERIVED_CURRENT_CORPUS",
            "basis": "q_shape can forget J_q, but observed coframe invisibility requires DObs_e[v_R]=0 and that kernel is unsigned",
            "consequence": "finite DObs_e/C_R leak rows are now staged for local runners",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "decision_id": "DEC1878_1_component_trapdoor",
            "decision": "RADIAL_CELL_VARIATION_HAS_VISIBLE_COFAME_PROJECTION_UNLESS_PARENT_SILENCED",
            "basis": "theta_0 and theta_1 depend on T and sqrt(S), while C_R=2(lnT+lnsqrtS)",
            "consequence": "future proof must derive parent coframe ownership or bound common-frame leakage",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "decision_id": "DEC1878_2_next",
            "decision": "PARENT_COFRAME_OWNERSHIP_OR_BG_BOUND_SELECTED_NEXT",
            "basis": "the smallest remaining upstream theorem is e_obs=E(Q_vis) with no C_R/J_q argument; fallback is b_R/epsilon_DObs bound row",
            "consequence": "1879 targets parent coframe ownership before broader finite local tests",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "route_id": "NEXT1878_0_primary",
            "target_doc": "1879-Y5-R2FR-parent-coframe-ownership-or-common-frame-leak-bound.md",
            "target_script": "scripts/Y5_R2FR_parent_coframe_ownership_or_common_frame_leak_bound_1879.py",
            "objective": "derive e_obs=E(Q_vis) with no C_R/J_q argument and no common Weyl/disformal residual, or stage b_R/epsilon_DObs source-ready bound rows.",
            "selection_status": "selected",
            "success_condition": "parent coframe ownership theorem, or nonclaim finite common-frame leak rows with local_GR/PPN/WEP/clock/orbital gates blocked.",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "route_id": "NEXT1878_1_later",
            "target_doc": "1879b-Y5-R2FR-source-readout-marker-boundary-qbasicity.md",
            "target_script": "scripts/Y5_R2FR_source_readout_marker_boundary_qbasicity_1879b.py",
            "objective": "after coframe ownership, test source/readout/marker/boundary q-basicity so C_R does not reenter through matter or endpoints.",
            "selection_status": "held_later",
            "success_condition": "source/readout q-basic theorem or finite leak rows for each channel.",
            "valid_for_claim": False,
        },
    ]


def all_output_rows() -> dict[str, list[dict[str, Any]]]:
    return {
        "source_register": source_register_rows(),
        "coframe_kernel_test": coframe_kernel_test_rows(),
        "finite_dobs_rows": finite_dobs_rows(),
        "category_principle_audit": category_principle_audit_rows(),
        "local_gate_map": local_gate_map_rows(),
        "claim_gate": claim_gate_rows(),
        "decision": decision_rows(),
        "next_target": next_target_rows(),
    }


def all_claim_flags_false(paths: list[Path]) -> tuple[bool, str]:
    checked = 0
    for path in paths:
        for row_index, row in enumerate(csv_rows(path), start=2):
            for column in [
                "valid_for_claim",
                "claim_allowed",
                "proof_closed",
                "score_ready",
            ]:
                if column in row:
                    checked += 1
                    if bool_string(row[column]) == "true":
                        return False, f"{path.name}:{row_index}:{column}=true"
    return checked > 0, f"checked={checked}"


def missing_rows_not_ready(paths: list[Path]) -> tuple[bool, str]:
    checked = 0
    for path in paths:
        for row_index, row in enumerate(csv_rows(path), start=2):
            joined = " ".join(row.values())
            if "MISSING_" in joined:
                checked += 1
                for column in ["score_ready", "valid_for_claim", "claim_allowed"]:
                    if column in row and bool_string(row[column]) == "true":
                        return False, f"{path.name}:{row_index}:{column}=true_on_missing_row"
    return checked > 0, f"checked_missing_rows={checked}"


def csv_parse_check(paths: list[Path]) -> tuple[bool, str]:
    details: list[str] = []
    for path in paths:
        rows = csv_rows(path)
        if not rows:
            return False, f"EMPTY_CSV={path.name}"
        details.append(f"{path.name}:{len(rows)}")
    return True, ";".join(details)


def copy_branch_artifacts() -> None:
    for path in OUTPUTS.values():
        if path.name.endswith("_VALIDATION.csv"):
            continue
        shutil.copy2(path, MICROSCOPE_RESIDUALS / path.name)
        shutil.copy2(path, QUARANTINE / path.name)
    shutil.copy2(OUTPUTS["coframe_kernel_test"], QUEUE / "JR1878_QSHAPE_COFRAME_KERNEL_TEST_NONCLAIM.csv")
    shutil.copy2(OUTPUTS["finite_dobs_rows"], QUEUE / "JR1878_FINITE_DOBS_E_LEAK_ROWS_NONCLAIM.csv")
    shutil.copy2(OUTPUTS["next_target"], QUEUE / "JR1878_NEXT_TARGET_NONCLAIM.csv")


def remove_pycache() -> None:
    pycache = Path(__file__).resolve().parent / "__pycache__"
    if pycache.exists():
        shutil.rmtree(pycache)


def validation_rows() -> list[dict[str, Any]]:
    generated_without_validation = [path for key, path in OUTPUTS.items() if key != "validation"]
    rows_by_name = {key: csv_rows(path) for key, path in OUTPUTS.items() if key != "validation"}
    checks: list[dict[str, Any]] = []

    sources = rows_by_name["source_register"]
    checks.append(
        {
            "validation_id": "VAL1878_0_sources",
            "status": "PASS" if all(bool_string(row["usable_for_1878"]) == "true" for row in sources) else "FAIL",
            "detail": "1877, 1738, observer-contract, typed-grammar and residual-vector sources are available",
            "valid_for_claim": False,
        }
    )

    tests = rows_by_name["coframe_kernel_test"]
    results = {row["result"] for row in tests}
    checks.append(
        {
            "validation_id": "VAL1878_1_kernel_test",
            "status": "PASS"
            if "EXACT_CONDITIONAL" in results
            and "COUNTERMODEL_SURVIVES" in results
            and "DOBS_E_KERNEL_NOT_DERIVED_CURRENT_CORPUS" in results
            else "FAIL",
            "detail": "coframe kernel test records conditional theorem, countermodel, and current no-derivation verdict",
            "valid_for_claim": False,
        }
    )

    finite = rows_by_name["finite_dobs_rows"]
    checks.append(
        {
            "validation_id": "VAL1878_2_finite_rows",
            "status": "PASS"
            if len(finite) == 5
            and any(row["row_id"] == "FDOBS1878_0_radial_cell_coframe" for row in finite)
            and all("MISSING_" in row["status"] for row in finite)
            else "FAIL",
            "detail": "finite DObs/coframe leak rows are staged as missing nonclaim rows",
            "valid_for_claim": False,
        }
    )

    category = rows_by_name["category_principle_audit"]
    checks.append(
        {
            "validation_id": "VAL1878_3_category_audit",
            "status": "PASS"
            if any(row["current_status"] == "CATEGORY_PRINCIPLE_NOT_DERIVED_CURRENT_CORPUS" for row in category)
            and any(row["current_status"] == "MISSING_QSHAPE_READOUT_FUNCTOR" for row in category)
            else "FAIL",
            "detail": "parent category principle and q_shape readout functor remain unsigned",
            "valid_for_claim": False,
        }
    )

    local_gates = rows_by_name["local_gate_map"]
    checks.append(
        {
            "validation_id": "VAL1878_4_local_gates",
            "status": "PASS"
            if len(local_gates) == 5
            and all(row["current_status"].startswith("BLOCKED") or "BLOCKED" in row["current_status"] for row in local_gates)
            and all(bool_string(row["claim_allowed"]) == "false" for row in local_gates)
            else "FAIL",
            "detail": "local_GR, PPN, WEP/clock, orbital, and R10 gates remain blocked",
            "valid_for_claim": False,
        }
    )

    claims = rows_by_name["claim_gate"]
    checks.append(
        {
            "validation_id": "VAL1878_5_claim_gate",
            "status": "PASS"
            if any(row["status"] == "ALLOW_INTERNAL_NONCLAIM_TEST" for row in claims)
            and all(bool_string(row["claim_allowed"]) == "false" for row in claims)
            else "FAIL",
            "detail": "only internal nonclaim test is allowed",
            "valid_for_claim": False,
        }
    )

    decisions = rows_by_name["decision"]
    checks.append(
        {
            "validation_id": "VAL1878_6_decision",
            "status": "PASS"
            if any(row["decision"] == "DOBS_E_KERNEL_NOT_DERIVED_CURRENT_CORPUS" for row in decisions)
            and any(row["decision"] == "PARENT_COFRAME_OWNERSHIP_OR_BG_BOUND_SELECTED_NEXT" for row in decisions)
            else "FAIL",
            "detail": "decision ledger records failed DObs theorem and selects parent-coframe ownership next",
            "valid_for_claim": False,
        }
    )

    next_targets = rows_by_name["next_target"]
    checks.append(
        {
            "validation_id": "VAL1878_7_next_target",
            "status": "PASS"
            if any(row["route_id"] == "NEXT1878_0_primary" and row["selection_status"] == "selected" for row in next_targets)
            else "FAIL",
            "detail": "1879 parent coframe ownership/common-frame leak target selected",
            "valid_for_claim": False,
        }
    )

    flags_ok, flags_detail = all_claim_flags_false(generated_without_validation)
    checks.append(
        {
            "validation_id": "VAL1878_8_claim_flags_false",
            "status": "PASS" if flags_ok else "FAIL",
            "detail": flags_detail,
            "valid_for_claim": False,
        }
    )

    missing_ok, missing_detail = missing_rows_not_ready(generated_without_validation)
    checks.append(
        {
            "validation_id": "VAL1878_9_missing_not_ready",
            "status": "PASS" if missing_ok else "FAIL",
            "detail": missing_detail,
            "valid_for_claim": False,
        }
    )

    parse_ok, parse_detail = csv_parse_check(generated_without_validation)
    checks.append(
        {
            "validation_id": "VAL1878_10_csv_parse",
            "status": "PASS" if parse_ok else "FAIL",
            "detail": parse_detail,
            "valid_for_claim": False,
        }
    )

    copied_paths = [
        MICROSCOPE_RESIDUALS / OUTPUTS["coframe_kernel_test"].name,
        QUARANTINE / OUTPUTS["finite_dobs_rows"].name,
        QUEUE / "JR1878_QSHAPE_COFRAME_KERNEL_TEST_NONCLAIM.csv",
        QUEUE / "JR1878_FINITE_DOBS_E_LEAK_ROWS_NONCLAIM.csv",
    ]
    checks.append(
        {
            "validation_id": "VAL1878_11_branch_copies",
            "status": "PASS" if all(path.exists() for path in copied_paths) else "FAIL",
            "detail": ";".join(str(path) for path in copied_paths),
            "valid_for_claim": False,
        }
    )

    pycache = Path(__file__).resolve().parent / "__pycache__"
    checks.append(
        {
            "validation_id": "VAL1878_12_pycache_absent",
            "status": "PASS" if not pycache.exists() else "FAIL",
            "detail": str(pycache),
            "valid_for_claim": False,
        }
    )

    formalization_hits = list(FORMALIZATION.rglob("*1878*")) if FORMALIZATION.exists() else []
    checks.append(
        {
            "validation_id": "VAL1878_13_formalization_untouched",
            "status": "PASS" if not formalization_hits else "FAIL",
            "detail": f"formalization_1878_count={len(formalization_hits)}",
            "valid_for_claim": False,
        }
    )

    fail_count = sum(1 for row in checks if row["status"] != "PASS")
    checks.append(
        {
            "validation_id": "VAL1878_OVERALL",
            "status": "PASS" if fail_count == 0 else "FAIL",
            "detail": "1878 q_shape readout functor kernel or parent category principle",
            "valid_for_claim": False,
        }
    )
    return checks


def markdown_table(rows: list[dict[str, Any]]) -> str:
    if not rows:
        return ""
    headers: list[str] = []
    for row in rows:
        for key in row:
            if key not in headers:
                headers.append(key)
    lines = [
        "| " + " | ".join(headers) + " |",
        "| " + " | ".join("---" for _ in headers) + " |",
    ]
    for row in rows:
        values = [str(row.get(header, "")).replace("\n", " ") for header in headers]
        lines.append("| " + " | ".join(values) + " |")
    return "\n".join(lines)


def write_doc(rows_by_name: dict[str, list[dict[str, Any]]]) -> None:
    validation = csv_rows(OUTPUTS["validation"])
    content = f"""# 1878 - q_shape Readout Functor Kernel Or Parent Category Principle

**Private status:** nonclaim derivation checkpoint. No local-GR, PPN, WEP, clock, orbital, R10, or public claim is made.

## Result

The chain-rule theorem is still exact:

```text
e_obs = E(q_shape(Phi)) and Dq_shape[v_R] = 0  =>  DObs_e[v_R] = 0.
```

But the current corpus does not prove the premise. In the current observed-coframe map:

```text
theta_0 = T c dt
theta_1 = sqrt(S) dr
C_R = R_AB = 2(ln T + ln sqrt(S))
```

So a radial-cell variation that changes `C_R` has a visible coframe projection unless a parent readout functor, category principle, or constraint-first mechanism silences it before readout.

In plain language: `q_shape` can forget the radial cell, but physics cannot forget what clocks and rulers actually read unless the parent theory proves that forgetfulness.

## Coframe Kernel Test

{markdown_table(rows_by_name["coframe_kernel_test"])}

## Finite DObs_e Leak Rows

{markdown_table(rows_by_name["finite_dobs_rows"])}

## Parent Category Principle Audit

{markdown_table(rows_by_name["category_principle_audit"])}

## Local Gate Map

{markdown_table(rows_by_name["local_gate_map"])}

## Source Register

{markdown_table(rows_by_name["source_register"])}

## Claim Gate

{markdown_table(rows_by_name["claim_gate"])}

## Decision Ledger

{markdown_table(rows_by_name["decision"])}

## Next Target

{markdown_table(rows_by_name["next_target"])}

## Validation

{markdown_table(validation)}
"""
    DOC.write_text(content, encoding="utf-8")


def main() -> None:
    ensure_dirs()
    rows_by_name = all_output_rows()
    for key, rows in rows_by_name.items():
        write_csv(OUTPUTS[key], rows)
    copy_branch_artifacts()
    remove_pycache()
    write_csv(OUTPUTS["validation"], validation_rows())
    write_doc(rows_by_name)


if __name__ == "__main__":
    main()

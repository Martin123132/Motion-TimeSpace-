from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "source-intake" / "mts_residuals"
LOCAL_BOUNDS = ROOT / "source-intake" / "local_bounds"
QUEUE = ROOT / "source-intake" / "rab-sector" / "acquisition-queue"
MICROSCOPE = ROOT / "source-intake" / "microscope" / "branch_locked_wep" / "residuals"
BETA_DOCS = ROOT / "source-intake" / "beta-source" / "docs"
FORMALIZATION = ROOT.parent / "formalization-workbench"
DOC = ROOT / "2244-Y5-R2FR-RAB-no-physical-pole-theorem-or-bounded-beta-runner.md"
BRANCH_ID = "MTS_R2FR_PARENT_QLOC_RAB_NO_PHYSICAL_POLE_OR_BETA_RUNNER_2244"
START_TS = datetime.now(timezone.utc).timestamp()


SOURCE_FILES = {
    "2243_doc": ROOT / "2243-Y5-R2FR-RAB-parent-finite-quadratic-row-and-source-test-beta-split.md",
    "2243_validation": OUT / "P8_Y5_BRR545_2243_VALIDATION.csv",
    "2243_next": OUT / "P8_Y5_PARENT_QLOC_2243_NEXT_TARGET.csv",
    "2243_branch": OUT / "P8_Y5_PARENT_QLOC_2243_BRANCH_CLASSIFICATION.csv",
    "2243_parent_audit": OUT / "P8_Y5_PARENT_QLOC_2243_PARENT_RAB_ACTION_AUDIT.csv",
    "2243_beta": OUT / "P8_Y5_PARENT_QLOC_2243_BETA_SOURCE_TEST_DERIVATION.csv",
    "1037_doc": ROOT / "1037-Y5-R10-no-physical-X-pole-theorem-or-bounded-beta-runner.md",
    "1037_validation": OUT / "P8_Y5_BRR545_1037_VALIDATION.csv",
    "1037_no_pole": OUT / "P8_Y5_R10_1037_NO_PHYSICAL_X_POLE_AUDIT.csv",
    "1037_beta": OUT / "P8_Y5_R10_1037_BOUNDED_BETA_SOURCE_TEST_TEMPLATE.csv",
    "1038_doc": ROOT / "1038-Y5-R10-parent-Omega-DCX-vertical-generator-closure-or-beta-bound-acquisition.md",
    "1038_validation": OUT / "P8_Y5_BRR545_1038_VALIDATION.csv",
    "1038_omega_dcx": OUT / "P8_Y5_R10_1038_OMEGA_DCX_CLOSURE_AUDIT.csv",
    "1038_vertical_map": OUT / "P8_Y5_R10_1038_VERTICAL_GENERATOR_FIELD_MAP.csv",
    "1038_beta_acq": OUT / "P8_Y5_R10_1038_BETA_BOUND_SOURCE_ACQUISITION.csv",
    "581_certificate": OUT / "P8_Y5_R10_581_NO_POLE_CERTIFICATE_TEMPLATE.csv",
    "582_momentum": OUT / "P8_Y5_R10_582_MOMENTUM_MAP_CLOSURE_THEOREM.csv",
    "590_gate": OUT / "P8_Y5_R10_590_MAPPING_CLOSURE_GATE.csv",
    "590_field_map": OUT / "P8_Y5_R10_590_FIELD_BY_FIELD_VERTICAL_ACTION_MAP.csv",
    "670_chain": OUT / "P8_Y5_R10_670_NO_POLE_QUOTIENT_PROOF_CHAIN.csv",
    "local_bounds": LOCAL_BOUNDS / "local_bound_claims.csv",
    "r10_candidate": LOCAL_BOUNDS / "R10_alpha_lambda_bound_curve_1034_REVIEW_CANDIDATE_NONCLAIM.csv",
}


SOURCE_REGISTER = OUT / "P8_Y5_PARENT_QLOC_2244_SOURCE_REGISTER.csv"
NO_POLE_AUDIT = OUT / "P8_Y5_PARENT_QLOC_2244_NO_PHYSICAL_RAB_POLE_AUDIT.csv"
POLE_COUNTERMODELS = OUT / "P8_Y5_PARENT_QLOC_2244_POLE_COUNTERMODEL_LEDGER.csv"
OMEGA_DCR_CLOSURE = OUT / "P8_Y5_PARENT_QLOC_2244_OMEGA_DCR_CLOSURE_AUDIT.csv"
VERTICAL_GENERATOR_MAP = OUT / "P8_Y5_PARENT_QLOC_2244_VERTICAL_GENERATOR_FIELD_MAP.csv"
BOUNDED_BETA_TEMPLATE = OUT / "P8_Y5_PARENT_QLOC_2244_BOUNDED_BETA_SOURCE_TEST_TEMPLATE.csv"
ABSOLUTE_TAIL_ENVELOPE = OUT / "P8_Y5_PARENT_QLOC_2244_ABSOLUTE_TAIL_ENVELOPE.csv"
ARENA_ROUTING = OUT / "P8_Y5_PARENT_QLOC_2244_ARENA_ROUTING_MAP.csv"
MTS_ALPHA_TEMPLATE = OUT / "R10_alpha_lambda_curve_MTS_2244_NO_POLE_OR_BETA_TEMPLATE_NONCLAIM.csv"
RUNNER_SMOKE = OUT / "P8_Y5_PARENT_QLOC_2244_RUNNER_SMOKE_STATUS.csv"
PLACEHOLDER_REFUSAL = OUT / "P8_Y5_PARENT_QLOC_2244_PLACEHOLDER_REFUSAL_RUNNER.csv"
CLAIM_GATES = OUT / "P8_Y5_PARENT_QLOC_2244_CLAIM_GATES.csv"
DECISION = OUT / "P8_Y5_PARENT_QLOC_2244_DECISION_LEDGER.csv"
NEXT_TARGET = OUT / "P8_Y5_PARENT_QLOC_2244_NEXT_TARGET.csv"
BRANCH_COPIES = OUT / "P8_Y5_PARENT_QLOC_2244_BRANCH_COPIES.csv"
VALIDATION = OUT / "P8_Y5_BRR545_2244_VALIDATION.csv"


COPY_TARGETS = {
    "queue_beta": QUEUE / "JR2244_BOUNDED_BETA_SOURCE_TEST_TEMPLATE_NONCLAIM.csv",
    "queue_nopole": QUEUE / "JR2244_NO_PHYSICAL_RAB_POLE_AUDIT_NONCLAIM.csv",
    "branch_wep": MICROSCOPE / "no_physical_RAB_pole_or_beta_runner_nonclaim_2244.csv",
    "beta_docs": BETA_DOCS / "NO_PHYSICAL_RAB_POLE_OR_BETA_RUNNER_2244_NONCLAIM.csv",
}


GENERATED = [
    SOURCE_REGISTER,
    NO_POLE_AUDIT,
    POLE_COUNTERMODELS,
    OMEGA_DCR_CLOSURE,
    VERTICAL_GENERATOR_MAP,
    BOUNDED_BETA_TEMPLATE,
    ABSOLUTE_TAIL_ENVELOPE,
    ARENA_ROUTING,
    MTS_ALPHA_TEMPLATE,
    RUNNER_SMOKE,
    PLACEHOLDER_REFUSAL,
    CLAIM_GATES,
    DECISION,
    NEXT_TARGET,
    BRANCH_COPIES,
    VALIDATION,
]


def flags() -> dict[str, bool]:
    return {
        "numeric_value_present": False,
        "source_backed": False,
        "score_ready": False,
        "valid_prediction_row": False,
        "valid_for_claim": False,
        "claim_allowed": False,
    }


def rel(path: Path) -> str:
    try:
        return str(path.relative_to(ROOT)).replace("\\", "/")
    except ValueError:
        return str(path)


def resolve_project_path(path_text: str) -> Path:
    path = Path(path_text.strip())
    if path.is_absolute():
        return path
    return ROOT / path


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        raise ValueError(f"no rows for {path}")
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def parse_csv(path: Path) -> bool:
    read_csv(path)
    return True


def validation_pass(path: Path) -> bool:
    if not path.exists():
        return False
    rows = read_csv(path)
    if not rows:
        return False
    id_key = "check_id" if "check_id" in rows[0] else "validation_id"
    result_key = "result" if "result" in rows[0] else "status"
    overall_rows = [row for row in rows if "overall" in row.get(id_key, "").lower() or "summary" in row.get(id_key, "").lower()]
    if overall_rows:
        return all(row.get(result_key, "").lower() == "pass" for row in overall_rows)
    return all(row.get(result_key, "").lower() == "pass" for row in rows)


def source_rows() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for index, (key, path) in enumerate(SOURCE_FILES.items()):
        if key.startswith("2243"):
            role = "current R2FR finite-row/no-pole handoff"
        elif key.startswith("1037") or key.startswith("1038"):
            role = "older no-pole/bounded-beta proof scaffold"
        elif key.startswith(("581", "582", "590", "670")):
            role = "parent quotient/symplectic/vertical-generator obstruction evidence"
        else:
            role = "external local bound anchor ledger"
        rows.append(
            {
                "branch_id": BRANCH_ID,
                "source_id": f"SRC2244_{index}_{key}",
                "source_path": rel(path),
                "path_exists": path.exists(),
                "validation_overall_pass": validation_pass(path) if key.endswith("validation") else "",
                "role": role,
                **flags(),
            }
        )
    return rows


def source_register_paths_exist() -> bool:
    return all(resolve_project_path(row["source_path"]).exists() for row in read_csv(SOURCE_REGISTER))


def no_pole_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "audit_id": "NPR2244_0_q_kernel",
            "criterion": "vertical R_AB is in the kernel of the parent quotient",
            "mathematical_test": "Dq[v_R]=0 and q is parent-defined before variation",
            "current_evidence": "670 gives conditional kernel transfer; 2243 says the finite R_AB row is not owned",
            "result": "PARTIAL_MATH_ONLY_NOT_PARENT_SIGNED",
            "if_missing": "R_AB can still be a physical residual rather than a representative choice",
            **flags(),
        },
        {
            "branch_id": BRANCH_ID,
            "audit_id": "NPR2244_1_action_descent",
            "criterion": "bulk action descends through q",
            "mathematical_test": "S_bulk[Phi]=S_red[q(Phi)] so H(v_R,.)=0 and no vertical Green operator exists",
            "current_evidence": "581/670 keep action factorization conditional; 2243 says parent R_AB row is not owned",
            "result": "CONDITIONAL_DESCENT_NOT_SIGNED",
            "if_missing": "a physical finite R_AB Hessian block can survive",
            **flags(),
        },
        {
            "branch_id": BRANCH_ID,
            "audit_id": "NPR2244_2_constraint_generator",
            "criterion": "vertical R_AB is generated by a first-class differentiable constraint",
            "mathematical_test": "delta G_R=Omega(delta Phi,v_R), G_R=int epsilon_AB C_R^AB + Q_R, and brackets close",
            "current_evidence": "582 writes theorem schema; 590/1038 show Omega, D C, v, boundary differentiability missing",
            "result": "MISSING_PARENT_OMEGA_DCR_VERTICAL_GENERATOR",
            "if_missing": "zero Hessian is not enough; second-class or edge remnants can remain",
            **flags(),
        },
        {
            "branch_id": BRANCH_ID,
            "audit_id": "NPR2244_3_boundary_silence",
            "criterion": "vertical transformations carry no local boundary charge",
            "mathematical_test": "Q_R=0/exact/proper and K_boundary=0 for compact local vertical transformations",
            "current_evidence": "1038 identifies Q_X/K_boundary as sharp obstruction; no R_AB boundary charge is computed",
            "result": "MISSING_BOUNDARY_CHARGE_ZERO",
            "if_missing": "R_AB can reappear as edge hair or source charge",
            **flags(),
        },
        {
            "branch_id": BRANCH_ID,
            "audit_id": "NPR2244_4_degree_count",
            "criterion": "constraints remove the local R_AB pair",
            "mathematical_test": "primary/secondary first-class pair removes R_AB and reduced Omega has no proper R_AB stabilizer",
            "current_evidence": "581/582/590 all leave rank/degree count incomplete",
            "result": "MISSING_DEGREE_COUNT",
            "if_missing": "no-pole cannot be distinguished from under-specified dynamics",
            **flags(),
        },
        {
            "branch_id": BRANCH_ID,
            "audit_id": "NPR2244_5_matter_readout",
            "criterion": "ordinary matter/readout descends through q and no marker sees R_AB",
            "mathematical_test": "S_matter=Sbar[Obs(q(Phi)),psi,theta] and Lie_vR theta=0",
            "current_evidence": "1027/1028/955 write contracts; 2243 says beta source/test rows remain unowned",
            "result": "MISSING_MATTER_NO_MARKER_SIGNATURE",
            "if_missing": "beta_source/beta_test rows remain live even if the bulk pole is controlled",
            **flags(),
        },
        {
            "branch_id": BRANCH_ID,
            "audit_id": "NPR2244_6_verdict",
            "criterion": "no physical local R_AB pole in the GR/Newton branch",
            "mathematical_test": "NPR2244_0 through NPR2244_5 all close from one parent action and boundary prescription",
            "current_evidence": "route is sharp, but the parent certificate is incomplete",
            "result": "FAIL_CURRENT_CLAIM_NO_POLE_NOT_PROVED",
            "if_missing": "build bounded beta_source/beta_test runner and retain no-cancellation tails",
            **flags(),
        },
    ]


def countermodel_rows() -> list[dict[str, Any]]:
    rows = [
        ("PCM2244_0_second_class_RAB", "R_AB has a degenerate-looking Hessian but constraints are second class or incomplete", "no Green kernel cannot be claimed without first-class closure and degree count", "parent Omega, D C_R, bracket, degree-count proof"),
        ("PCM2244_1_edge_mode", "bulk vertical variation is pure gauge, but boundary charge Q_R survives", "R10/source charge can be carried by edge hair", "boundary differentiability, Q_R=0/proper/exact, K_boundary=0"),
        ("PCM2244_2_shadow_matter_frame", "ordinary matter uses a universal R_AB-dependent Weyl/disformal frame", "WEP may look fine while beta_source=beta_test=c_g and R10 sees c_g^2", "no-shadow-frame theorem or numeric c_g/b_dis bound"),
        ("PCM2244_3_marker_constants", "masses, EM constants, or material markers carry R_AB-dependence", "clock/WEP/composition constraints become tied to R10 beta rows", "no-marker theorem or b_A/b_alpha bounds"),
        ("PCM2244_4_hidden_support", "non-Hilbert current, source support, or domain/boundary tail sources R_AB", "alpha_R can survive even if visible Hilbert matter descends", "q_nonH, Delta_W_support, q_domain, and q_boundary zero/bound rows"),
    ]
    return [
        {
            "branch_id": BRANCH_ID,
            "countermodel_id": countermodel_id,
            "countermodel": countermodel,
            "why_it_matters": why,
            "blocked_by": blocked_by,
            **flags(),
        }
        for countermodel_id, countermodel, why, blocked_by in rows
    ]


def omega_dcr_rows() -> list[dict[str, Any]]:
    rows = [
        ("ODR2244_0_parent_Omega", "parent symplectic form", "Omega_Y=delta Theta_Y on the full parent variable set before quotient/gauge fixing", "cannot reconstruct Theta_Y from current R_AB ledgers; existing rows only name the missing object", "MISSING_PARENT_OMEGA", "D C_R^dagger cannot be identified with an Omega-flat vertical vector"),
        ("ODR2244_1_DCR_operator", "linearized R_AB constraint/source operator D C_R", "C_R^AB[Phi]=0 is parent-owned and D C_R maps field variations into the R_AB constraint covector", "candidate C_R is only schematic; no parent-owned operator/domain is written", "MISSING_DCR_OPERATOR", "D C_R^dagger is pairing-dependent bookkeeping, not a generator proof"),
        ("ODR2244_2_Omega_flat_map", "Omega-flat vertical generator identity", "i_{v_R} Omega_Y = delta C_R[epsilon] or D C_R^dagger epsilon = Omega_Y^flat(v_R[epsilon])", "identity cannot be checked without both Omega_Y and D C_R", "NOT_COMPARABLE_WITHOUT_OMEGA_AND_DCR", "rank-zero/null directions do not prove gauge; a physical or edge mode can remain"),
        ("ODR2244_3_vertical_generator_fields", "field-by-field vertical generator", "v_R is specified on metric/coframe, momenta, R_AB, domain/memory/projector, matter/readout, and boundary fields", "standard diffeo/local-Lorentz candidates exist only for metric/coframe; MTS extra sectors are unmapped", "FIELD_MAP_INCOMPLETE", "the putative gauge direction can leak into source/test charges"),
        ("ODR2244_4_boundary_differentiability", "boundary charge Q_R", "delta Q_R cancels all boundary variation and Q_R is zero, exact, or proper on the local branch", "no current file computes Q_R=0 for R_AB", "MISSING_BOUNDARY_CHARGE_ZERO", "source charge can be hidden in edge hair"),
        ("ODR2244_5_bracket_closure", "first-class bracket and boundary cocycle", "{G_R[epsilon],G_R[eta]} = G_R[[epsilon,eta]] + K_boundary and K_boundary=0 locally", "algebra is only a target; K_boundary is not computed", "MISSING_BRACKET_KBOUNDARY", "the R_AB direction may be second-class, anomalous, or edge-charged"),
        ("ODR2244_6_degree_count", "reduced phase-space degree count", "primary/secondary first-class pair removes the local R_AB pair and reduced Omega is nondegenerate without an R_AB stabilizer", "rank/constraint count remains a named obligation", "MISSING_DEGREE_COUNT", "no-pole can be confused with under-specified dynamics"),
        ("ODR2244_7_matter_readout", "matter/no-marker descent", "S_matter=Sbar[q(Phi),psi,theta] and ordinary constants/readouts carry no representative-R_AB marker", "existing contracts isolate the requirement but do not parent-sign it", "MISSING_MATTER_QUOTIENT", "beta_source and beta_test remain live"),
        ("ODR2244_8_verdict", "exact no-physical-R_AB-pole certificate", "ODR2244_0 through ODR2244_7 close from one parent action and boundary prescription", "2244 sharpens the obstruction but does not close it", "FAIL_CURRENT_CLAIM_NO_POLE_NOT_CLOSED", "start bounded beta source/test acquisition while keeping derivation route open"),
    ]
    return [
        {
            "branch_id": BRANCH_ID,
            "audit_id": audit_id,
            "object": obj,
            "needed_statement": needed,
            "derivation_attempt": attempt,
            "current_status": status,
            "if_missing": if_missing,
            **flags(),
        }
        for audit_id, obj, needed, attempt, status, if_missing in rows
    ]


def vertical_map_rows() -> list[dict[str, Any]]:
    rows = [
        ("metric_or_coframe", "v_R[g]=Lie_epsilon g or v_R[e]=Lie_epsilon e plus local Lorentz compensation if R_AB is pure representative", "metric/coframe component of Omega_Y^flat(v_R)", "metric/coframe component of D C_R^dagger epsilon", "STANDARD_CANDIDATE_NOT_PARENT_DECLARED", "observed metric/coframe ownership and parent symplectic potential"),
        ("R_AB_residual_block", "v_R[R_AB] is either a pure vertical representative shift, algebraic constraint response, or no action if R_AB is absent", "R_AB component of Omega_Y^flat(v_R)", "R_AB component of D C_R^dagger epsilon", "CORE_BLOCK_UNWRITTEN", "explicit R_AB parent variable status and transformation law"),
        ("canonical_momenta_or_boundary_charge", "v_R[pi]=Lie_epsilon pi plus density and boundary improvements", "momentum and boundary component of Omega_Y^flat(v_R)", "integration-by-parts boundary term in delta C_R[epsilon]", "NOT_WRITTEN_FOR_MTS", "canonical variables or covariant phase-space charge split"),
        ("domain_memory_projector_fields", "v_R[Phi^A]=Lie_epsilon Phi^A or quotient-vertical representative shift", "domain/memory/projector component of Omega_Y^flat(v_R)", "extra-sector component of D C_R^dagger", "UNMAPPED", "transformation law for chi_D, Q_coh, memory, projector, and boundary variables"),
        ("matter_readout_constants", "v_R[psi]=0 and v_R[theta_A]=0 only if matter descends through q", "matter component should vanish or be quotient-pullback only", "no source/test marker covector", "NOT_DERIVED", "matter action descent and no-marker theorem"),
        ("boundary_edge_modes", "proper compact transformation or exact boundary representative shift", "no residual boundary charge in Omega_Y^flat(v_R)", "Q_R=0/exact/proper and K_boundary=0", "NOT_DERIVED", "boundary differentiability, Q_R, and cocycle computation"),
    ]
    return [
        {
            "branch_id": BRANCH_ID,
            "field_block": block,
            "candidate_vertical_action": action,
            "Omega_flat_target": omega,
            "DCR_target": dcr,
            "status": status,
            "missing_input": missing,
            **flags(),
        }
        for block, action, omega, dcr, status, missing in rows
    ]


def beta_rows() -> list[dict[str, Any]]:
    rows = [
        ("BB2244_0_beta_source_geom", "source", "beta_s_geom", "source-body R_AB charge from common Weyl/disformal observed-frame leakage", "|beta_s_geom| <= |profile_s^W c_g| + |profile_s^dis b_dis|", "profile_s^W;profile_s^dis;c_g;b_dis;source support;units;source_path", "MISSING_FRAME_LEAK_ZERO_OR_NUMERIC_BOUND", "R10;PPN;WEP;clock"),
        ("BB2244_1_beta_test_geom", "test", "beta_t_geom", "test/readout R_AB charge from common Weyl/disformal observed-frame leakage", "|beta_t_geom| <= |tau_R10 c_g| + |tau_dis b_dis|", "tau_R10;tau_dis;c_g;b_dis;test material/readout profile;units;source_path", "MISSING_ARENA_PROJECTION", "R10;PPN;WEP;clock"),
        ("BB2244_2_beta_source_marker", "source", "beta_s_marker", "source composition/material/EM marker R_AB charge", "|beta_s_marker| <= sum_A |S_sA b_A| + |S_salpha b_alpha|", "source material sensitivities;b_A;b_alpha;EM/binding convention;source_path", "MISSING_NO_MARKER_THEOREM_OR_NUMERIC_BOUNDS", "WEP;clock;composition;R10"),
        ("BB2244_3_beta_test_marker", "test", "beta_t_marker", "test material/readout marker R_AB charge", "|beta_t_marker| <= sum_A |S_tA b_A| + |S_talpha b_alpha|", "test material sensitivities;b_A;b_alpha;readout convention;source_path", "MISSING_MARKER_READOUT_PROJECTION", "WEP;clock;composition;R10"),
        ("BB2244_4_beta_source_nonH", "source", "beta_s_nonH", "source-side non-Hilbert/boundary/domain/support R_AB current", "|beta_s_nonH| <= |q_nonH_s| + |Delta_W_support_s| + |q_domain_s| + |q_boundary_s|", "non-Hilbert current;support shift;domain current;boundary charge;units;source_path", "MISSING_HIDDEN_SOURCE_ZERO_OR_NUMERIC_BOUND", "R10;orbital;source_normalization;local_GR"),
        ("BB2244_5_beta_test_nonH", "test", "beta_t_nonH", "test/readout-side non-Hilbert/boundary/domain/support R_AB current", "|beta_t_nonH| <= |q_nonH_t| + |Delta_W_support_t| + |q_domain_t| + |q_boundary_t|", "readout support;non-Hilbert current;domain/boundary tail;units;source_path", "MISSING_HIDDEN_TEST_ZERO_OR_NUMERIC_BOUND", "R10;orbital;source_normalization;local_GR"),
        ("BB2244_6_beta_abs_totals", "source_and_test", "beta_s_abs;beta_t_abs", "absolute no-cancellation source/test beta envelopes", "beta_s_abs=sum_i |beta_s_i|; beta_t_abs=sum_i |beta_t_i|", "all component rows BB2244_0 through BB2244_5 theorem-zero or numeric/source-backed", "SCHEMA_READY_VALUES_MISSING", "all_local_arenas"),
        ("BB2244_7_beta_product_guard", "source_times_test", "abs_beta_product", "claim-safe source-test product for finite exchange", "|beta_s beta_t| <= beta_s_abs beta_t_abs; universal Weyl gives c_g^2 contribution", "beta_s_abs;beta_t_abs;declaration whether Qbar already contains source leg", "CLAIM_BLOCKED", "R10;PPN;WEP;clock;orbital"),
    ]
    return [
        {
            "branch_id": BRANCH_ID,
            "beta_id": beta_id,
            "leg": leg,
            "symbol": symbol,
            "definition": definition,
            "formula_or_bound": formula,
            "required_inputs": required,
            "current_status": status,
            "observable_links": links,
            **flags(),
        }
        for beta_id, leg, symbol, definition, formula, required, status, links in rows
    ]


def tail_rows() -> list[dict[str, Any]]:
    rows = [
        ("TAIL2244_0_alpha_envelope", "abs_alpha_R(lambda)", "|alpha_R| <= |K_R^R10(lambda)| * [beta_s_abs beta_t_abs + abs_tail_source_test(lambda)]", "K_R^R10;beta_s_abs;beta_t_abs;tail rows;promoted alpha_bound(lambda)", "MISSING_NUMERIC_ENVELOPE"),
        ("TAIL2244_1_no_cancellation_policy", "tail addition rule", "unknown components add in absolute value; no cancellation credit between c_g,b_dis,b_A,b_alpha,q_nonH,boundary/support", "component theorem-zero or numeric/source-backed bounds", "POLICY_ACTIVE"),
        ("TAIL2244_2_R10_score_gate", "R10 comparison gate", "score only if abs_alpha_R(lambda) and alpha_bound(lambda) are numeric, sourced, unit-matched, and valid_for_claim=true", "MTS prediction and promoted bound curve", "CLAIM_BLOCKED"),
    ]
    return [
        {
            "branch_id": BRANCH_ID,
            "tail_id": tail_id,
            "quantity": quantity,
            "formula": formula,
            "missing_inputs": missing,
            "current_status": status,
            **flags(),
        }
        for tail_id, quantity, formula, missing, status in rows
    ]


def arena_rows() -> list[dict[str, Any]]:
    rows = [
        ("ARENA2244_0_R10", "short-range fifth force", "K_R^R10 beta_s beta_t plus absolute tails", "lambda profile, source/test support, tau_R10, bound curve", "BLOCKED_BY_BETA_KR_BOUND"),
        ("ARENA2244_1_PPN", "PPN/local weak field", "common frame c_g, disformal b_dis, non-Hilbert/support tails", "gauge-fixed response matrix for gamma,beta,preferred-frame rows", "BLOCKED_ARENA_PROJECTION_MISSING"),
        ("ARENA2244_2_WEP_clock", "WEP, clocks, EM/material markers", "b_A,b_alpha,c_g marker/readout sensitivities", "material sensitivities, clock coefficients, composition pairs", "BLOCKED_MARKER_DESCENT_OR_NUMERIC_BOUNDS_MISSING"),
        ("ARENA2244_3_orbital_source", "orbital/source normalization/local GR", "q_nonH, Delta_W_support, boundary/domain support tails", "worldtube/source support and orbital observable map", "BLOCKED_SUPPORT_THEOREM_OR_BOUND_MISSING"),
    ]
    return [
        {
            "branch_id": BRANCH_ID,
            "arena_id": arena_id,
            "arena": arena,
            "receives": receives,
            "required_projection": required,
            "current_status": status,
            **flags(),
        }
        for arena_id, arena, receives, required, status in rows
    ]


def alpha_template_rows() -> list[dict[str, Any]]:
    rows = [
        ("MTS_source_normalized_Newton_branch", "no_physical_RAB_pole_template", "ALL_LOCAL_R10_RANGE", "MISSING_NO_PHYSICAL_RAB_POLE_CERTIFICATE", "no active finite Yukawa pole only if quotient/constraint/boundary/matter certificate closes", "template_invalid_no_pole_not_parent_signed"),
        ("MTS_source_normalized_Newton_branch", "bounded_beta_product_template", "MISSING_PARENT_LAMBDA_R", "MISSING_KR_TIMES_BETA_S_ABS_BETA_T_ABS_TAILS", "|alpha_R| <= |K_R^R10| [beta_s_abs beta_t_abs + abs_tail]", "template_invalid_bounded_beta_inputs_missing"),
        ("MTS_source_normalized_Newton_branch", "universal_weyl_cg_squared_template", "MISSING_PARENT_LAMBDA_R", "MISSING_KR_PROFILE_CG_SQUARED", "universal Weyl source/test branch: alpha_R proportional to K_R^R10 c_g^2", "template_invalid_cg_and_KR_missing"),
    ]
    return [
        {
            "branch_id": BRANCH_ID,
            "model_id": model,
            "template_branch": template,
            "lambda_value": lambda_value,
            "alpha_predicted": alpha,
            "force_law_form": law,
            "derivation_status": status,
            **flags(),
        }
        for model, template, lambda_value, alpha, law, status in rows
    ]


def runner_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "smoke_id": "SMOKE2244_0_runner_status",
            "valid_mts_rows": 0,
            "valid_bound_rows": 0,
            "comparison_rows": 1,
            "R10_pass_for_claim": False,
            "expected_result": "blocked_nonclaim",
            **flags(),
        }
    ]


def refusal_rows() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for row in no_pole_rows():
        rows.append(
            {
                "branch_id": BRANCH_ID,
                "refusal_id": row["audit_id"].replace("NPR2244", "REF2244_NOPOLE"),
                "object": row["criterion"],
                "current_status": row["result"],
                "refusal_status": "no_pole_claim_rejected_current_corpus",
                "failure_reasons": f"{row['result']};CLAIM_POLICY_FALSE",
                "score_eligible": False,
                **flags(),
            }
        )
    for row in beta_rows():
        rows.append(
            {
                "branch_id": BRANCH_ID,
                "refusal_id": row["beta_id"].replace("BB2244", "REF2244_BETA"),
                "object": row["symbol"],
                "current_status": row["current_status"],
                "refusal_status": "bounded_beta_row_rejected_missing_inputs",
                "failure_reasons": f"{row['current_status']};SCORE_READY_FALSE;CLAIM_POLICY_FALSE",
                "score_eligible": False,
                **flags(),
            }
        )
    for row in omega_dcr_rows():
        rows.append(
            {
                "branch_id": BRANCH_ID,
                "refusal_id": row["audit_id"].replace("ODR2244", "REF2244_ODR"),
                "object": row["object"],
                "current_status": row["current_status"],
                "refusal_status": "omega_dcr_claim_rejected_current_corpus",
                "failure_reasons": f"{row['current_status']};CLAIM_POLICY_FALSE",
                "score_eligible": False,
                **flags(),
            }
        )
    return rows


def claim_rows() -> list[dict[str, Any]]:
    rows = [
        ("CGATE2244_0_no_pole", "finite local R_AB mode has no physical pole", "parent Omega, D C_R, vertical action, boundary charge, degree count, and matter/no-marker signature remain incomplete"),
        ("CGATE2244_1_alpha_zero", "R10 alpha_R=0 locally", "no-pole and hidden-tail clauses are not parent-signed"),
        ("CGATE2244_2_bounded_beta", "bounded beta_source/beta_test rows are score-ready", "all beta component rows still contain missing theorem-zero or numeric/source-backed inputs"),
        ("CGATE2244_3_linear_cg", "linear c_g can be scored against R10", "universal Weyl source/test branch contributes c_g squared"),
        ("CGATE2244_4_R10_local_GR_pass", "R10/local-GR pass is established", "MTS rows and external bound curve remain nonclaim/unscoreable"),
    ]
    return [
        {
            "branch_id": BRANCH_ID,
            "gate_id": gate_id,
            "claim": claim,
            "gate_pass": False,
            "reason": reason,
            **flags(),
        }
        for gate_id, claim, reason in rows
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "decision_id": "DEC2244_0_no_pole_status",
            "decision": "No-pole remains the cleanest GR-reduction route, but it fails current-claim status.",
            "because": "the route requires parent Omega, D C_R, field-by-field vertical generator, boundary charge silence, degree count, and matter/no-marker descent together",
            "next_action": "attack the missing parent Omega/D C_R/vertical-generator closure directly",
            **flags(),
        },
        {
            "branch_id": BRANCH_ID,
            "decision_id": "DEC2244_1_beta_fallback_status",
            "decision": "The fallback is a bounded beta_source/beta_test acquisition problem.",
            "because": "if a physical finite pole survives, local tests see beta_source beta_test plus absolute tails, not a single coupling",
            "next_action": "fill theorem-zero or numeric/source-backed beta component rows one by one",
            **flags(),
        },
        {
            "branch_id": BRANCH_ID,
            "decision_id": "DEC2244_2_linear_cg_status",
            "decision": "Legacy linear c_g shorthand remains quarantined.",
            "because": "a source-test interaction needs both legs; universal frame leakage is quadratic unless Qbar owns one leg",
            "next_action": "make future candidate rows declare beta_source beta_test or an explicit source leg inside Qbar with source path and units",
            **flags(),
        },
        {
            "branch_id": BRANCH_ID,
            "decision_id": "DEC2244_3_next_target",
            "decision": "Next target should attack boundary charge/cocycle first while keeping beta acquisition ready.",
            "because": "Q_R=0 and K_boundary=0 are the sharpest single remaining no-pole obstruction and decide whether edge charge becomes a beta source",
            "next_action": "2245-Y5-R2FR-RAB-boundary-charge-QR-Kboundary-zero-or-beta-bound-first-row.md",
            **flags(),
        },
    ]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "next_target": "2245-Y5-R2FR-RAB-boundary-charge-QR-Kboundary-zero-or-beta-bound-first-row.md",
            "script": "scripts/Y5_R2FR_RAB_boundary_charge_QR_Kboundary_zero_or_beta_bound_first_row_2245.py",
            "objective": "try to compute or prove silence of Q_R and K_boundary for the local R_AB vertical branch; if this fails, fill the first source-backed beta projection row without claiming a pass",
            "include": "boundary variation of G_R, Q_R exact/proper/zero tests, K_boundary cocycle, compact-support local transformation limit, first beta source row schema",
            "exclude": "invented parent action terms, naked linear c_g scoring, cancellation between beta tails, R10/local-GR pass claim, formalization-workbench edits, GitHub action",
            **flags(),
        }
    ]


def copy_rows() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    copy_sources = {
        "queue_beta": BOUNDED_BETA_TEMPLATE,
        "queue_nopole": NO_POLE_AUDIT,
        "branch_wep": BOUNDED_BETA_TEMPLATE,
        "beta_docs": BOUNDED_BETA_TEMPLATE,
    }
    for copy_id, source in copy_sources.items():
        target = COPY_TARGETS[copy_id]
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(source, target)
        rows.append(
            {
                "branch_id": BRANCH_ID,
                "copy_id": copy_id,
                "source_path": rel(source),
                "target_path": rel(target),
                "copied": target.exists(),
                "parse_ok": parse_csv(target),
                **flags(),
            }
        )
    return rows


def generated_flags_false(paths: list[Path]) -> bool:
    false_values = {"", "false", "0", "no", "none", "null"}
    keys = ["numeric_value_present", "source_backed", "score_ready", "valid_prediction_row", "valid_for_claim", "claim_allowed"]
    for path in paths:
        for row in read_csv(path):
            for key in keys:
                if key in row and str(row[key]).strip().lower() not in false_values:
                    return False
    return True


def no_pole_audit_blocks_claim() -> bool:
    return any(row.get("result") == "FAIL_CURRENT_CLAIM_NO_POLE_NOT_PROVED" for row in read_csv(NO_POLE_AUDIT))


def omega_dcr_blocks_claim() -> bool:
    return any(row.get("current_status") == "FAIL_CURRENT_CLAIM_NO_POLE_NOT_CLOSED" for row in read_csv(OMEGA_DCR_CLOSURE))


def beta_rows_nonclaim() -> bool:
    return all(row.get("score_ready", "").lower() == "false" and row.get("valid_for_claim", "").lower() == "false" for row in read_csv(BOUNDED_BETA_TEMPLATE))


def tail_policy_active() -> bool:
    text = " ".join(" ".join(row.values()) for row in read_csv(ABSOLUTE_TAIL_ENVELOPE))
    return "no cancellation" in text.lower() and "CLAIM_BLOCKED" in text


def claim_gates_blocked() -> bool:
    return all(row.get("gate_pass", "").lower() == "false" and row.get("claim_allowed", "").lower() == "false" for row in read_csv(CLAIM_GATES))


def remove_pycache() -> None:
    pycache = ROOT / "scripts" / "__pycache__"
    if pycache.exists():
        shutil.rmtree(pycache)


def formalization_2244_artifacts_absent() -> bool:
    if not FORMALIZATION.exists():
        return True
    return not any(
        path.is_file()
        and "2244" in path.name
        and ".venv" not in path.relative_to(FORMALIZATION).parts
        for path in FORMALIZATION.rglob("*")
    )


def formalization_untouched_since_start() -> bool:
    if not FORMALIZATION.exists():
        return True
    return not any(path.is_file() and path.stat().st_mtime >= START_TS for path in FORMALIZATION.rglob("*"))


def validation_rows(generated_paths: list[Path]) -> list[dict[str, Any]]:
    rows = [
        {
            "branch_id": BRANCH_ID,
            "check_id": "VAL2244_00_sources_exist",
            "result": "PASS" if all(path.exists() for path in SOURCE_FILES.values()) and source_register_paths_exist() else "FAIL",
            "detail": "all direct and registered 2244 source paths exist",
        },
        {
            "branch_id": BRANCH_ID,
            "check_id": "VAL2244_01_prior_validations",
            "result": "PASS" if validation_pass(SOURCE_FILES["2243_validation"]) and validation_pass(SOURCE_FILES["1037_validation"]) and validation_pass(SOURCE_FILES["1038_validation"]) else "FAIL",
            "detail": "2243, 1037, and 1038 validations pass overall",
        },
        {
            "branch_id": BRANCH_ID,
            "check_id": "VAL2244_02_no_pole_audit_blocks_claim",
            "result": "PASS" if no_pole_audit_blocks_claim() else "FAIL",
            "detail": "no-pole audit reaches blocked verdict",
        },
        {
            "branch_id": BRANCH_ID,
            "check_id": "VAL2244_03_countermodels_complete",
            "result": "PASS" if len(read_csv(POLE_COUNTERMODELS)) == 5 else "FAIL",
            "detail": "countermodel ledger blocks weak no-pole shortcuts",
        },
        {
            "branch_id": BRANCH_ID,
            "check_id": "VAL2244_04_omega_dcr_blocks_claim",
            "result": "PASS" if omega_dcr_blocks_claim() else "FAIL",
            "detail": "Omega/D C_R closure audit ends in blocked no-pole verdict",
        },
        {
            "branch_id": BRANCH_ID,
            "check_id": "VAL2244_05_vertical_map_complete_nonclaim",
            "result": "PASS" if len(read_csv(VERTICAL_GENERATOR_MAP)) == 6 else "FAIL",
            "detail": "vertical generator map covers core, R_AB, extra, matter, and boundary blocks without promotion",
        },
        {
            "branch_id": BRANCH_ID,
            "check_id": "VAL2244_06_beta_rows_nonclaim",
            "result": "PASS" if beta_rows_nonclaim() else "FAIL",
            "detail": "bounded beta schema includes source/test legs and remains nonclaim",
        },
        {
            "branch_id": BRANCH_ID,
            "check_id": "VAL2244_07_tail_policy_active",
            "result": "PASS" if tail_policy_active() else "FAIL",
            "detail": "absolute no-cancellation tail policy is active",
        },
        {
            "branch_id": BRANCH_ID,
            "check_id": "VAL2244_08_arena_routing_complete",
            "result": "PASS" if len(read_csv(ARENA_ROUTING)) == 4 else "FAIL",
            "detail": "arena routing covers R10, PPN, WEP/clock, and orbital/source channels",
        },
        {
            "branch_id": BRANCH_ID,
            "check_id": "VAL2244_09_mts_template_nonclaim",
            "result": "PASS" if all(row.get("valid_for_claim", "").lower() == "false" for row in read_csv(MTS_ALPHA_TEMPLATE)) else "FAIL",
            "detail": "MTS alpha template has no claim-valid rows",
        },
        {
            "branch_id": BRANCH_ID,
            "check_id": "VAL2244_10_runner_smoke_refuses_claim",
            "result": "PASS" if read_csv(RUNNER_SMOKE)[0].get("expected_result") == "blocked_nonclaim" else "FAIL",
            "detail": "runner smoke status refuses a claim",
        },
        {
            "branch_id": BRANCH_ID,
            "check_id": "VAL2244_11_claim_gates_blocked",
            "result": "PASS" if claim_gates_blocked() else "FAIL",
            "detail": "all claim gates remain blocked",
        },
        {
            "branch_id": BRANCH_ID,
            "check_id": "VAL2244_12_next_target_written",
            "result": "PASS" if read_csv(NEXT_TARGET)[0]["next_target"].startswith("2245-Y5-R2FR-RAB-boundary-charge") else "FAIL",
            "detail": "next target row is present",
        },
        {
            "branch_id": BRANCH_ID,
            "check_id": "VAL2244_13_csv_parse",
            "result": "PASS" if all(parse_csv(path) for path in generated_paths) else "FAIL",
            "detail": "all generated 2244 CSVs parse cleanly",
        },
        {
            "branch_id": BRANCH_ID,
            "check_id": "VAL2244_14_claim_flags_false",
            "result": "PASS" if generated_flags_false(generated_paths) else "FAIL",
            "detail": "all generated prediction/claim flags remain false",
        },
        {
            "branch_id": BRANCH_ID,
            "check_id": "VAL2244_15_branch_copies",
            "result": "PASS" if all(row["copied"] == "True" and row["parse_ok"] == "True" for row in read_csv(BRANCH_COPIES)) else "FAIL",
            "detail": "branch/quarantine nonclaim copies written",
        },
        {
            "branch_id": BRANCH_ID,
            "check_id": "VAL2244_16_pycache_absent",
            "result": "PASS" if not (ROOT / "scripts" / "__pycache__").exists() else "FAIL",
            "detail": "scripts __pycache__ absent after run",
        },
        {
            "branch_id": BRANCH_ID,
            "check_id": "VAL2244_17_formalization_no_2244",
            "result": "PASS" if formalization_2244_artifacts_absent() else "FAIL",
            "detail": "formalization-workbench has no non-venv 2244 artifacts",
        },
        {
            "branch_id": BRANCH_ID,
            "check_id": "VAL2244_18_formalization_untouched",
            "result": "PASS" if formalization_untouched_since_start() else "FAIL",
            "detail": "formalization-workbench untouched during 2244 run",
        },
    ]
    rows.append(
        {
            "branch_id": BRANCH_ID,
            "check_id": "VAL2244_OVERALL",
            "result": "PASS" if all(row["result"] == "PASS" for row in rows) else "FAIL",
            "detail": "2244 attempts the no-physical-R_AB-pole theorem, blocks the claim on Omega/D C_R/boundary/degree/matter gaps, stages bounded beta rows, and selects Q_R/K_boundary next",
        }
    )
    return rows


def md_table(rows: list[dict[str, Any]], columns: list[str]) -> str:
    lines = [
        "| " + " | ".join(columns) + " |",
        "| " + " | ".join("---" for _ in columns) + " |",
    ]
    for row in rows:
        values = [str(row.get(column, "")).replace("\n", " ").replace("|", "\\|") for column in columns]
        lines.append("| " + " | ".join(values) + " |")
    return "\n".join(lines)


def build_doc(
    source: list[dict[str, Any]],
    no_pole: list[dict[str, Any]],
    countermodels: list[dict[str, Any]],
    omega_dcr: list[dict[str, Any]],
    vertical_map: list[dict[str, Any]],
    beta: list[dict[str, Any]],
    tails: list[dict[str, Any]],
    arena: list[dict[str, Any]],
    alpha_template: list[dict[str, Any]],
    runner: list[dict[str, Any]],
    refusal: list[dict[str, Any]],
    claim: list[dict[str, Any]],
    decision: list[dict[str, Any]],
    next_target: list[dict[str, Any]],
    copies: list[dict[str, Any]],
    validation: list[dict[str, Any]],
) -> str:
    return "\n\n".join(
        [
            "# 2244 - Y5/R2FR R_AB No Physical Pole Theorem or Bounded Beta Runner",
            "## Verdict\n"
            "- 2244 attacks the cleanest local-GR route: prove the finite local `R_AB` residual has no physical exchange pole in the GR/Newton branch.\n"
            "- The route is not proved by the current corpus. It needs parent `Omega_Y`, parent-owned `D C_R`, all-field `v_R`, boundary `Q_R`, cocycle `K_boundary`, degree count, and matter/no-marker descent to close together.\n"
            "- This does not kill the framework; it prevents an unsafe `alpha_R=0` claim and keeps the finite branch as a bounded `beta_source beta_test` problem with absolute no-cancellation tails.\n"
            "- The old naked linear `c_g` route remains quarantined: universal source/test leakage enters as `c_g^2` unless the source leg is explicitly source-backed inside `Qbar`.\n"
            "- No R10, PPN, WEP, clock, orbital, local-GR, or Newton claim is made.",
            "## Source Register\n"
            + md_table(source, ["source_id", "source_path", "path_exists", "validation_overall_pass", "role"]),
            "## No Physical R_AB Pole Audit\n"
            + md_table(no_pole, ["audit_id", "criterion", "mathematical_test", "current_evidence", "result", "if_missing"]),
            "## Pole Countermodel Ledger\n"
            + md_table(countermodels, ["countermodel_id", "countermodel", "why_it_matters", "blocked_by"]),
            "## Omega/D C_R Closure Audit\n"
            + md_table(omega_dcr, ["audit_id", "object", "needed_statement", "derivation_attempt", "current_status", "if_missing"]),
            "## Vertical Generator Field Map\n"
            + md_table(vertical_map, ["field_block", "candidate_vertical_action", "Omega_flat_target", "DCR_target", "status", "missing_input"]),
            "## Bounded Beta Source/Test Template\n"
            + md_table(beta, ["beta_id", "leg", "symbol", "definition", "formula_or_bound", "required_inputs", "current_status", "observable_links"]),
            "## Absolute Tail Envelope\n"
            + md_table(tails, ["tail_id", "quantity", "formula", "missing_inputs", "current_status"]),
            "## Arena Routing Map\n"
            + md_table(arena, ["arena_id", "arena", "receives", "required_projection", "current_status"]),
            "## MTS Alpha Template Update\n"
            + md_table(alpha_template, ["model_id", "template_branch", "lambda_value", "alpha_predicted", "force_law_form", "derivation_status"]),
            "## Runner Smoke Status\n"
            + md_table(runner, ["smoke_id", "valid_mts_rows", "valid_bound_rows", "comparison_rows", "R10_pass_for_claim", "claim_allowed", "expected_result"]),
            "## Placeholder Refusal Runner\n"
            + md_table(refusal, ["refusal_id", "object", "current_status", "refusal_status", "failure_reasons", "score_eligible", "claim_allowed"]),
            "## Claim Gates\n"
            + md_table(claim, ["gate_id", "claim", "gate_pass", "reason", "claim_allowed"]),
            "## Decision Ledger\n"
            + md_table(decision, ["decision_id", "decision", "because", "next_action"]),
            "## Next Target\n"
            + md_table(next_target, ["next_target", "script", "objective", "include", "exclude"]),
            "## Branch Copies\n"
            + md_table(copies, ["copy_id", "source_path", "target_path", "copied", "parse_ok"]),
            "## Validation\n"
            + md_table(validation, ["check_id", "result", "detail"]),
            "## Working Interpretation\n\n"
            "This is the exact place where the theory either earns derived local GR or admits a bounded residual. "
            "The no-pole route is still the best route because it removes the finite local exchange structurally, but the missing object is not a vibe: it is `Q_R/K_boundary` plus the parent `Omega/D C_R` certificate. "
            "So the next strike should be boundary charge/cocycle first, because if edge charge survives it becomes a beta source; if it vanishes cleanly, the no-pole theorem gets materially closer.",
            "",
        ]
    )


def main() -> None:
    source = source_rows()
    no_pole = no_pole_rows()
    countermodels = countermodel_rows()
    omega_dcr = omega_dcr_rows()
    vertical_map = vertical_map_rows()
    beta = beta_rows()
    tails = tail_rows()
    arena = arena_rows()
    alpha_template = alpha_template_rows()
    runner = runner_rows()
    refusal = refusal_rows()
    claim = claim_rows()
    decision = decision_rows()
    next_target = next_target_rows()

    write_csv(SOURCE_REGISTER, source)
    write_csv(NO_POLE_AUDIT, no_pole)
    write_csv(POLE_COUNTERMODELS, countermodels)
    write_csv(OMEGA_DCR_CLOSURE, omega_dcr)
    write_csv(VERTICAL_GENERATOR_MAP, vertical_map)
    write_csv(BOUNDED_BETA_TEMPLATE, beta)
    write_csv(ABSOLUTE_TAIL_ENVELOPE, tails)
    write_csv(ARENA_ROUTING, arena)
    write_csv(MTS_ALPHA_TEMPLATE, alpha_template)
    write_csv(RUNNER_SMOKE, runner)
    write_csv(PLACEHOLDER_REFUSAL, refusal)
    write_csv(CLAIM_GATES, claim)
    write_csv(DECISION, decision)
    write_csv(NEXT_TARGET, next_target)
    copies = copy_rows()
    write_csv(BRANCH_COPIES, copies)

    remove_pycache()
    generated_before_validation = [path for path in GENERATED if path != VALIDATION]
    validation = validation_rows(generated_before_validation)
    write_csv(VALIDATION, validation)
    remove_pycache()

    DOC.write_text(
        build_doc(
            source,
            no_pole,
            countermodels,
            omega_dcr,
            vertical_map,
            beta,
            tails,
            arena,
            alpha_template,
            runner,
            refusal,
            claim,
            decision,
            next_target,
            copies,
            validation,
        ),
        encoding="utf-8",
    )

    if not validation_pass(VALIDATION):
        raise SystemExit(f"2244 validation failed: {VALIDATION}")


if __name__ == "__main__":
    main()

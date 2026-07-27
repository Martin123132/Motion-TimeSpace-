from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


SCRIPT_START_UTC = datetime.now(timezone.utc)

ROOT = Path(__file__).resolve().parents[1]
PROJECT = ROOT.parent
RESIDUALS = ROOT / "source-intake" / "mts_residuals"
LOCAL_BOUNDS = ROOT / "source-intake" / "local_bounds"
SOURCE_WEIGHT = ROOT / "source-intake" / "source-weight"
RAB_QUEUE = ROOT / "source-intake" / "rab-sector" / "acquisition-queue"
BETA_DOCS = ROOT / "source-intake" / "beta-source" / "docs"
FORMALIZATION = PROJECT / "formalization-workbench"

BRANCH_ID = "MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428"

DOC = ROOT / "2882-Y5-R2FR-q-object-vertical-generator-certificate-or-Dq-leak-row-under-AX1090.md"

SRC_2881_DOC = ROOT / "2881-Y5-R2FR-JR-matter-source-current-or-matter-descent-zero-under-AX1090.md"
SRC_2881_NEXT = RESIDUALS / "P8_Y5_R2FR_2881_NEXT_TARGET.csv"
SRC_2881_QUEUE = RESIDUALS / "P8_Y5_R2FR_2881_SOURCE_CURRENT_ACQUISITION_QUEUE.csv"
SRC_2881_ZERO = RESIDUALS / "P8_Y5_R2FR_2881_JR_ZERO_GATE_AUDIT.csv"
SRC_2881_VALIDATION = RESIDUALS / "P8_Y5_BRR545_2881_VALIDATION.csv"

SRC_1023_QVX = RESIDUALS / "P8_Y5_R10_1023_QVX_CERTIFICATE.csv"
SRC_1023_VALIDATION = RESIDUALS / "P8_Y5_BRR545_1023_VALIDATION.csv"
SRC_1505_DQ_TESTS = RESIDUALS / "P8_Y5_R10_1505_DQ_VERTICALITY_TESTS.csv"
SRC_1505_THEOREM = RESIDUALS / "P8_Y5_R10_1505_QUOTIENT_VERTICAL_THEOREM_LEDGER.csv"
SRC_1575_VERTICAL = RESIDUALS / "P8_Y5_PARENT_QLOC_1575_RAB_VERTICAL_GENERATOR_SIGNATURE_ATTEMPT.csv"
SRC_1620_QVM = RESIDUALS / "P8_Y5_PARENT_QLOC_1620_QUOTIENT_VERTICALITY_MAP_AUDIT.csv"
SRC_1270_DQ = RESIDUALS / "P8_Y5_R10_1270_DQ_KERNEL_TEST_MATRIX.csv"
SRC_1270_QSORT = RESIDUALS / "P8_Y5_R10_1270_RAB_QUOTIENT_SORT_DERIVATION_ATTEMPT.csv"
SRC_1540_CHAIN = RESIDUALS / "P8_Y5_PARENT_QLOC_1540_VARIATION_CHAIN_AUDIT.csv"
SRC_1541_QMAP = RESIDUALS / "P8_Y5_PARENT_QLOC_1541_QMAP_CANDIDATE_LEDGER.csv"
SRC_1541_VGEN = RESIDUALS / "P8_Y5_PARENT_QLOC_1541_VERTICAL_GENERATOR_AUDIT.csv"
SRC_1541_KERNEL = RESIDUALS / "P8_Y5_PARENT_QLOC_1541_KERNEL_TEST.csv"
SRC_1541_COUPLING = RESIDUALS / "P8_Y5_PARENT_QLOC_1541_DQVM_FINITE_COUPLING_ROW_NONCLAIM.csv"
SRC_1541_VALIDATION = RESIDUALS / "P8_Y5_BRR545_1541_VALIDATION.csv"
SRC_1667_QAUDIT = RESIDUALS / "P8_Y5_PARENT_QLOC_1667_QUOTIENT_MAP_AUDIT.csv"
SRC_1667_DQ_TESTS = RESIDUALS / "P8_Y5_PARENT_QLOC_1667_DQ_ON_ZPHI_TESTS.csv"
SRC_1667_LEAKS = RESIDUALS / "P8_Y5_PARENT_QLOC_1667_RETAINED_DQ_LEAK_ROWS.csv"
SRC_1667_CONSTRAINT = RESIDUALS / "P8_Y5_PARENT_QLOC_1667_CONSTRAINT_FIRST_BRANCH_AUDIT.csv"
SRC_1667_VALIDATION = RESIDUALS / "P8_Y5_BRR545_1667_VALIDATION.csv"
SRC_1808_NOMIXED = RESIDUALS / "P8_Y5_PARENT_QLOC_1808_NO_MIXED_MORPHISM_LEMMA_ATTEMPT.csv"
SRC_2355_DOMAIN = RESIDUALS / "P8_Y5_PARENT_QLOC_2355_FIXED_DOMAIN_THEOREM_AUDIT.csv"
SRC_2356_DESCENT = RESIDUALS / "P8_Y5_PARENT_QLOC_2356_SOURCE_CURRENT_DESCENT_THEOREM_AUDIT.csv"
SRC_2525_GATE = RESIDUALS / "P8_Y5_NO_SHADOW_2525_FIXED_DOMAIN_GATE.csv"
SRC_2526_TESTS = RESIDUALS / "P8_Y5_NO_SHADOW_2526_ACTION_SIGNING_TESTS.csv"
SRC_2526_COUNTER = RESIDUALS / "P8_Y5_NO_SHADOW_2526_COUNTERMODEL_TESTS.csv"

OUTPUTS = {
    "sources": RESIDUALS / "P8_Y5_R2FR_2882_SOURCE_REGISTER.csv",
    "certificate": RESIDUALS / "P8_Y5_R2FR_2882_Q_OBJECT_VERTICALITY_CERTIFICATE.csv",
    "countermodels": RESIDUALS / "P8_Y5_R2FR_2882_DQ_KERNEL_COUNTERMODEL_REVIEW.csv",
    "fill": RESIDUALS / "P8_Y5_R2FR_2882_DQ_LEAK_FILL_ATTEMPT.csv",
    "queue": RESIDUALS / "P8_Y5_R2FR_2882_QV_ACQUISITION_QUEUE.csv",
    "gates": RESIDUALS / "P8_Y5_R2FR_2882_ACCEPTANCE_GATES.csv",
    "runner": RESIDUALS / "P8_Y5_R2FR_2882_RUNNER_STATUS.csv",
    "decision": RESIDUALS / "P8_Y5_R2FR_2882_DECISION_LEDGER.csv",
    "next": RESIDUALS / "P8_Y5_R2FR_2882_NEXT_TARGET.csv",
    "branches": RESIDUALS / "P8_Y5_R2FR_2882_BRANCH_COPIES.csv",
    "validation": RESIDUALS / "P8_Y5_BRR545_2882_VALIDATION.csv",
}

BRANCH_OUTPUTS = {
    "certificate_copy": LOCAL_BOUNDS / "RAB_Q_OBJECT_VERTICALITY_CERTIFICATE_2882_NONCLAIM.csv",
    "countermodel_copy": BETA_DOCS / "RAB_DQ_KERNEL_COUNTERMODEL_REVIEW_2882_NONCLAIM.csv",
    "fill_copy": SOURCE_WEIGHT / "RAB_DQ_LEAK_FILL_ATTEMPT_2882_NONCLAIM.csv",
    "next_queue": RAB_QUEUE / "JR2882_constraint_first_q_or_Dq_leak_source_pack_NEXT.csv",
}


for directory in {path.parent for path in OUTPUTS.values()} | {path.parent for path in BRANCH_OUTPUTS.values()} | {DOC.parent}:
    directory.mkdir(parents=True, exist_ok=True)


def now() -> str:
    return datetime.now(timezone.utc).isoformat()


def read_text(path: Path) -> str:
    if not path.exists():
        return ""
    return path.read_text(encoding="utf-8", errors="replace")


def anchors_present(path: Path, anchors: str) -> tuple[bool, str]:
    if not path.exists():
        return False, anchors
    text = read_text(path)
    missing = [anchor for anchor in anchors.split(";") if anchor and anchor not in text]
    return not missing, ";".join(missing)


def add_common(row: dict[str, Any]) -> dict[str, Any]:
    row.update(
        {
            "control_only": True,
            "score_ready": False,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
            "generated_utc": now(),
        }
    )
    return row


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


def csv_parses(path: Path) -> bool:
    try:
        with path.open(newline="", encoding="utf-8") as handle:
            list(csv.DictReader(handle))
        return True
    except Exception:
        return False


def source_register_rows() -> list[dict[str, Any]]:
    specs = [
        ("SRC2882_0_2881_doc", SRC_2881_DOC, "Status: `Y5_R2FR_2881_JR_descent_theorem_conditional_zero_not_signed_qv_2882_next`;derive the parent `q` object", "2881 handoff"),
        ("SRC2882_1_2881_next", SRC_2881_NEXT, "NEXT2881_0_2882", "explicit 2882 target"),
        ("SRC2882_2_2881_queue", SRC_2881_QUEUE, "Q2881_0_q_v_certificate", "q/v acquisition row"),
        ("SRC2882_3_2881_zero", SRC_2881_ZERO, "ZG2881_0_parent_q;ZG2881_1_verticality;ZG2881_11_joint_JR_zero", "J_R blocker rows"),
        ("SRC2882_4_2881_validation", SRC_2881_VALIDATION, "VAL2881_OVERALL", "2881 validation"),
        ("SRC2882_5_1023_qvx", SRC_1023_QVX, "QVC1023_0_parent_q;QVC1023_4_vertical_action;QVC1023_8_verdict", "single q/v/action certificate failure"),
        ("SRC2882_6_1023_validation", SRC_1023_VALIDATION, "V1023_2_certificate_fails;V1023_4_coupling_nonzero_open", "q/v certificate validation"),
        ("SRC2882_7_1505_dq_tests", SRC_1505_DQ_TESTS, "DQT1505_0_define_q;DQT1505_2_apply_Dq;DQT1505_8_acceptance", "Dq verticality acceptance tests"),
        ("SRC2882_8_1505_theorem", SRC_1505_THEOREM, "THM1505_0_vertical_residual_safe;THM1505_1_vertical_to_coframe_not_enough;THM1505_2_current_branch_verdict", "exact conditional theorem plus countermodel"),
        ("SRC2882_9_1575_vertical", SRC_1575_VERTICAL, "VERT1575_1_generator;VERT1575_3_constraint_escape;VERT1575_5_verdict", "R_AB vertical generator attempt"),
        ("SRC2882_10_1620_qvm", SRC_1620_QVM, "QVM1620_0_observer_jacobian;QVM1620_2_constraint_first;QVM1620_5_verdict", "quotient verticality map audit"),
        ("SRC2882_11_1270_dq", SRC_1270_DQ, "DQ1270_0_full_metric_readout;DQ1270_2_representative_class_readout;DQ1270_3_generic_hidden_X", "Dq kernel counterexamples"),
        ("SRC2882_12_1270_qsort", SRC_1270_QSORT, "QSR1270_1_observed_full_metric;QSR1270_3_auxiliary_before_q;QSR1270_5_verdict", "R_AB quotient sort verdict"),
        ("SRC2882_13_1540_chain", SRC_1540_CHAIN, "VAR1540_0_matter_variation;VAR1540_1_stress_not_zero;VAR1540_4_payoff_identity", "stress-mediated Dq chain"),
        ("SRC2882_14_1541_qmap", SRC_1541_QMAP, "QMAP1541_0_parent_quotient;QMAP1541_4_current_verdict", "q-map candidate ledger"),
        ("SRC2882_15_1541_vgen", SRC_1541_VGEN, "VGEN1541_0_target;VGEN1541_3_current_verdict", "vertical generator field-by-field gap"),
        ("SRC2882_16_1541_kernel", SRC_1541_KERNEL, "KTEST1541_0_Dq_kernel;KTEST1541_4_kernel_verdict", "Dq kernel test"),
        ("SRC2882_17_1541_coupling", SRC_1541_COUPLING, "DQC1541_0_C_qm_definition;DQC1541_4_Scg_envelope", "finite Dq coupling fallback"),
        ("SRC2882_18_1541_validation", SRC_1541_VALIDATION, "VAL1541_3_kernel_not_proved;VAL1541_14_overall", "1541 validation"),
        ("SRC2882_19_1667_qaudit", SRC_1667_QAUDIT, "QMA1667_0_q_prior;QMA1667_6_verdict", "current q not computable"),
        ("SRC2882_20_1667_dq_tests", SRC_1667_DQ_TESTS, "DQT1667_0_test_definition;DQT1667_6_verdict", "Dq on Z/phi tests"),
        ("SRC2882_21_1667_leaks", SRC_1667_LEAKS, "DQL1667_0_Dq_Z;DQL1667_7_Scg_envelope", "retained Dq leak rows"),
        ("SRC2882_22_1667_constraint", SRC_1667_CONSTRAINT, "CFB1667_2_RAB_constraint;CFB1667_5_verdict", "constraint-first route"),
        ("SRC2882_23_1667_validation", SRC_1667_VALIDATION, "VAL1667_2_q_not_computable;VAL1667_3_Dq_not_closed;VAL1667_OVERALL", "1667 validation"),
        ("SRC2882_24_1808_nomixed", SRC_1808_NOMIXED, "NMM1808_2_scalar_counterexample;NMM1808_3_quotient_kernel_limit;NMM1808_5_verdict", "hidden-to-visible coefficient morphism obstruction"),
        ("SRC2882_25_2355_domain", SRC_2355_DOMAIN, "FDT2355_1_vertical_support_descent;FDT2355_6_current_corpus_verdict", "support/domain descent conditional"),
        ("SRC2882_26_2356_descent", SRC_2356_DESCENT, "SCD2356_1_descent_theorem;SCD2356_5_countermodel_retained", "source-current descent conditional and countermodel"),
        ("SRC2882_27_2525_gate", SRC_2525_GATE, "FDG2525_0_parent_q;FDG2525_1_vertical_generator;FDG2525_10_theorem", "fixed-domain q/v gate"),
        ("SRC2882_28_2526_tests", SRC_2526_TESTS, "AST2526_0_q_object;AST2526_1_vertical_generator;AST2526_9_adoption", "minimal coupling cannot derive q/v"),
        ("SRC2882_29_2526_counter", SRC_2526_COUNTER, "CMT2526_5_q_missing", "q missing countermodel"),
    ]
    rows: list[dict[str, Any]] = []
    for source_id, path, anchors, role in specs:
        found, missing = anchors_present(path, anchors)
        rows.append(
            add_common(
                {
                    "source_id": source_id,
                    "source_path": str(path),
                    "anchors": anchors,
                    "role": role,
                    "path_exists": path.exists(),
                    "anchors_found": found,
                    "missing_anchors": missing,
                }
            )
        )
    return rows


def certificate_rows() -> list[dict[str, Any]]:
    rows = [
        {
            "cert_id": "CERT2882_0_exact_kernel_contract",
            "required_clause": "exact q-kernel criterion",
            "formal_statement": "If q is a parent-owned quotient/readout map and v_X is a field-space generator with Dq[v_X]=0 on an open local branch, then q-visible geometry is silent under v_X.",
            "current_evidence": "THM1505_0 and SCD2356_1 give exact conditional theorems.",
            "current_status": "EXACT_CONDITIONAL_THEOREM_ONLY",
            "source_path": str(SRC_1505_THEOREM),
            "source_anchor": "THM1505_0_vertical_residual_safe",
            "certificate_signed": False,
            "theorem_zero": False,
        },
        {
            "cert_id": "CERT2882_1_parent_q_object",
            "required_clause": "q exists before matter/readout",
            "formal_statement": "q: Phi_parent -> Q_obs must be computable from parent kinematics/action data, not chosen after a failed local test.",
            "current_evidence": "QMA1667_6 says q is not computable; FDG2525_0 blocks parent q.",
            "current_status": "BLOCKED_Q_OBJECT_NOT_PARENT_SIGNED",
            "source_path": str(SRC_1667_QAUDIT),
            "source_anchor": "QMA1667_6_verdict",
            "certificate_signed": False,
            "theorem_zero": False,
        },
        {
            "cert_id": "CERT2882_2_field_by_field_vX",
            "required_clause": "v_X is a real parent tangent generator",
            "formal_statement": "v_X must declare variations of metric/coframe, memory/projector/domain, matter lift, constants, source normalization, and boundary data.",
            "current_evidence": "QVC1023_4 and VGEN1541_0 record the missing transformation law.",
            "current_status": "BLOCKED_VERTICAL_GENERATOR_FIELD_ACTION_MISSING",
            "source_path": str(SRC_1541_VGEN),
            "source_anchor": "VGEN1541_0_target",
            "certificate_signed": False,
            "theorem_zero": False,
        },
        {
            "cert_id": "CERT2882_3_Dq_computation",
            "required_clause": "Dq[v_X] computed, not named",
            "formal_statement": "The quotient derivative must be computed against the actual observed stack, source/readout data, constants and boundary/projector maps.",
            "current_evidence": "DQT1505_2 and DQT1667_0 say the live Dq computation is missing/not runnable.",
            "current_status": "BLOCKED_DQ_OPERATOR_NOT_COMPUTABLE",
            "source_path": str(SRC_1505_DQ_TESTS),
            "source_anchor": "DQT1505_2_apply_Dq",
            "certificate_signed": False,
            "theorem_zero": False,
        },
        {
            "cert_id": "CERT2882_4_open_branch_kernel",
            "required_clause": "kernel holds on an open branch",
            "formal_statement": "Dq[v_X]=0 must hold as a branch identity, not at a point, not by symbol choice, and not by post-readout deletion.",
            "current_evidence": "FDG2525_1 and QVM1620_3 refuse pointwise/posthoc verticality.",
            "current_status": "BLOCKED_OPEN_BRANCH_KERNEL_NOT_SIGNED",
            "source_path": str(SRC_2525_GATE),
            "source_anchor": "FDG2525_1_vertical_generator",
            "certificate_signed": False,
            "theorem_zero": False,
        },
        {
            "cert_id": "CERT2882_5_full_metric_countermodel",
            "required_clause": "q does not include the residual as visible metric/coframe data",
            "formal_statement": "If q observes A=T^2 and B=S separately, then delta R_AB=delta ln(AB) changes q and the direction is not vertical.",
            "current_evidence": "DQ1270_0 and QSR1270_1 give the full-metric readout countermodel.",
            "current_status": "COUNTERMODEL_ACTIVE",
            "source_path": str(SRC_1270_DQ),
            "source_anchor": "DQ1270_0_full_metric_readout",
            "certificate_signed": False,
            "theorem_zero": False,
        },
        {
            "cert_id": "CERT2882_6_constraint_first_escape",
            "required_clause": "visible residual removed before matter/readout if not vertical",
            "formal_statement": "A parent constraint/no-pole equation may eliminate R_AB/Z/phi before q sees it, but the multiplier/action origin must be parent-signed.",
            "current_evidence": "QVM1620_2, VERT1575_3 and CFB1667_2 mark this as the cleanest unsigned route.",
            "current_status": "BEST_ROUTE_BUT_PARENT_ORIGIN_UNSIGNED",
            "source_path": str(SRC_1667_CONSTRAINT),
            "source_anchor": "CFB1667_2_RAB_constraint",
            "certificate_signed": False,
            "theorem_zero": False,
        },
        {
            "cert_id": "CERT2882_7_source_charge_extension",
            "required_clause": "Dq=0 must also silence source/test/marker/boundary channels",
            "formal_statement": "Even Dq[v_X]=0 for the observed coframe is insufficient if source/test charge, marker readout, boundary flux, or finite operator response survives.",
            "current_evidence": "THM1505_1, SCD2356_5 and FDT2355_6 retain these channels.",
            "current_status": "BLOCKED_EXTENSION_CHANNELS_OPEN",
            "source_path": str(SRC_1505_THEOREM),
            "source_anchor": "THM1505_1_vertical_to_coframe_not_enough",
            "certificate_signed": False,
            "theorem_zero": False,
        },
        {
            "cert_id": "CERT2882_8_hidden_morphism_extension",
            "required_clause": "hidden invariants cannot feed visible coefficients",
            "formal_statement": "Dq[v]=0 does not kill hidden-to-visible coefficient maps unless the coefficient functor domain excludes hidden invariants or proves them trivial.",
            "current_evidence": "NMM1808_3 and NMM1808_5 keep the no-mixed morphism lemma unsigned.",
            "current_status": "BLOCKED_NO_MIXED_MORPHISM_NOT_PROVED",
            "source_path": str(SRC_1808_NOMIXED),
            "source_anchor": "NMM1808_3_quotient_kernel_limit",
            "certificate_signed": False,
            "theorem_zero": False,
        },
        {
            "cert_id": "CERT2882_9_joint_certificate",
            "required_clause": "single q/v/action/matter/boundary certificate",
            "formal_statement": "q object, v_X, Dq-kernel, matter descent, constants, boundary/support, no hidden morphism, and open-branch degree/rank must close together.",
            "current_evidence": "QVC1023_8, KTEST1541_4, VAL1667_OVERALL and ZG2881_11 all fail current promotion.",
            "current_status": "NOT_CLOSED_KEEP_DQ_LEAK_ROWS",
            "source_path": str(SRC_1023_QVX),
            "source_anchor": "QVC1023_8_verdict",
            "certificate_signed": False,
            "theorem_zero": False,
        },
    ]
    return [add_common(row) for row in rows]


def countermodel_rows() -> list[dict[str, Any]]:
    specs = [
        ("CM2882_0_full_metric_readout", "q observes A=T^2 and B=S", "delta R_AB changes q for generic variations; visible metric/coframe data cannot be called vertical.", SRC_1270_DQ, "DQ1270_0_full_metric_readout", "ACTIVE"),
        ("CM2882_1_representative_class_circularity", "define q=[A,B]/R_AB after seeing the problem", "verticality by definition is closure-smuggling unless the parent primitive action proves the equivalence first.", SRC_1270_DQ, "DQ1270_2_representative_class_readout", "ACTIVE"),
        ("CM2882_2_observer_cell_visibility", "q includes radial phase-cell/J_q data", "R_AB=ln(T^2 S)=2 ln(J_q) can be coframe/cell-visible unless constraint-eliminated.", SRC_1620_QVM, "QVM1620_0_observer_jacobian", "ACTIVE"),
        ("CM2882_3_q_missing_from_matter_action", "minimal matter coupling uses q but does not derive q", "the clean matter action cannot prove its own quotient map or vertical generator.", SRC_2526_COUNTER, "CMT2526_5_q_missing", "ACTIVE"),
        ("CM2882_4_stress_mediated_Dq", "ordinary matter Hilbert stress is nonzero", "delta_v S_matter contains <delta S/delta q,Dq[v]>; stress cannot be killed by matter EOM.", SRC_1540_CHAIN, "VAR1540_1_stress_not_zero", "ACTIVE"),
        ("CM2882_5_source_test_charge_survives", "Dq=0 for coframe but source/test charge remains", "beta-style coframe silence does not imply alpha/Yukawa/source-force silence.", SRC_1505_THEOREM, "THM1505_1_vertical_to_coframe_not_enough", "ACTIVE"),
        ("CM2882_6_hidden_scalar_coefficient", "surviving hidden invariant feeds visible coefficient", "c(Phi)=c0+epsilon I_hid is natural/covariant unless the invariant algebra is killed.", SRC_1808_NOMIXED, "NMM1808_2_scalar_counterexample", "ACTIVE"),
        ("CM2882_7_boundary_support_motion", "support/domain/boundary marker shifts under v_X", "even if bulk geometry descends, boundary/support tails can generate the first local residual row.", SRC_2355_DOMAIN, "FDT2355_6_current_corpus_verdict", "ACTIVE"),
        ("CM2882_8_posthoc_delete", "delete residual after readout", "forbidden because it hides a real source charge and violates the derivation-first rule.", SRC_1620_QVM, "QVM1620_3_posthoc_delete", "ACTIVE"),
    ]
    return [
        add_common(
            {
                "countermodel_id": countermodel_id,
                "countermodel": countermodel,
                "why_dangerous": why,
                "source_path": str(path),
                "source_anchor": anchor,
                "current_status": status,
                "countermodel_active": True,
                "excluded_now": False,
                "claim_safe": False,
            }
        )
        for countermodel_id, countermodel, why, path, anchor, status in specs
    ]


def fill_rows() -> list[dict[str, Any]]:
    rows = [
        {
            "fill_id": "FILL2882_0_Dq_vertical_leak",
            "quantity": "Dq_vertical_leak",
            "candidate_formula": "||Dq[v_X]||_arena over observed coframe, source/readout, constants and boundary/projector components",
            "candidate_value": "MISSING_NUMERIC_OR_THEOREM_ZERO",
            "units": "arena-dependent quotient norm",
            "source_path": str(SRC_1667_LEAKS),
            "source_anchor": "DQL1667_4_Dsource_readout",
            "status": "RETAINED_NONCLAIM_INPUT",
            "failure_mode": "q is not computable and v_X field action is not parent-signed",
            "accepted_live_input": False,
            "parent_signed": False,
        },
        {
            "fill_id": "FILL2882_1_Dq_RAB_or_Jq_norm",
            "quantity": "Dq_RAB_or_Jq_norm",
            "candidate_formula": "Dq[v_R] for R_AB/J_q cell-visible residual",
            "candidate_value": "MISSING_NUMERIC_OR_THEOREM_ZERO",
            "units": "cell/coframe norm",
            "source_path": str(SRC_1667_LEAKS),
            "source_anchor": "DQL1667_2_Dq_RAB_Jq",
            "status": "RETAINED_NONCLAIM_INPUT",
            "failure_mode": "full metric/readout countermodel remains active; constraint-first route unsigned",
            "accepted_live_input": False,
            "parent_signed": False,
        },
        {
            "fill_id": "FILL2882_2_C_qm",
            "quantity": "C_qm",
            "candidate_formula": "C_qm := ||DObs_e[Dq[v_m]]|| in local weak-field/source norm",
            "candidate_value": "MISSING_QMAP_DERIVATIVE",
            "units": "depends on v_X normalization",
            "source_path": str(SRC_1541_COUPLING),
            "source_anchor": "DQC1541_0_C_qm_definition",
            "status": "SCHEMA_ONLY_INPUTS_MISSING",
            "failure_mode": "observed coframe functor and q derivative are not available",
            "accepted_live_input": False,
            "parent_signed": False,
        },
        {
            "fill_id": "FILL2882_3_J_vertical_physical",
            "quantity": "J_vertical_physical",
            "candidate_formula": "DSbar[Dq(v_X)]+J_direct[v_X]+J_theta L_v theta+delta_v B plus source/readout escape terms",
            "candidate_value": "MISSING_COMPONENT_VALUES",
            "units": "source-current units after ell_J/tau/M_H_ref lock",
            "source_path": str(SRC_2356_DESCENT),
            "source_anchor": "SCD2356_3_domain_motion_normal_form",
            "status": "FALLBACK_SCHEMA_ONLY",
            "failure_mode": "Dq leak, direct source slot, constants, boundary and normalization values are missing",
            "accepted_live_input": False,
            "parent_signed": False,
        },
        {
            "fill_id": "FILL2882_4_Scg_norm_envelope",
            "quantity": "S_cg_norm",
            "candidate_formula": "S_cg_norm <= 1/2||T||_source C_qm + S_direct_m + S_source_norm_extra + S_boundary_m",
            "candidate_value": "FORMULA_ONLY_INPUTS_MISSING",
            "units": "E* forcing units",
            "source_path": str(SRC_1541_COUPLING),
            "source_anchor": "DQC1541_4_Scg_envelope",
            "status": "RETAINED_NONCLAIM_ENVELOPE",
            "failure_mode": "T norm, C_qm, direct/source/boundary terms and units are not source-backed",
            "accepted_live_input": False,
            "parent_signed": False,
        },
        {
            "fill_id": "FILL2882_5_constraint_zero_attempt",
            "quantity": "Dq_vertical_leak=0 by constraint/no-pole",
            "candidate_formula": "lambda_R R_AB=0 or no independent Green/source pole before matter coupling",
            "candidate_value": "THEOREM_ZERO_NOT_AVAILABLE_CURRENT_CORPUS",
            "units": "n/a",
            "source_path": str(SRC_1667_CONSTRAINT),
            "source_anchor": "CFB1667_2_RAB_constraint",
            "status": "ZERO_ROUTE_UNSIGNED",
            "failure_mode": "constraint/multiplier origin, stress silence and boundary certificate are not parent-signed",
            "accepted_live_input": False,
            "parent_signed": False,
        },
    ]
    return [add_common(row) for row in rows]


def queue_rows() -> list[dict[str, Any]]:
    specs = [
        ("Q2882_0_constraint_first_or_leak_pack", "q,Dq,v_X,Dq_vertical_leak,J_vertical_physical", "primary_next", "try parent constraint/no-pole q construction for R_AB/Z/phi; if not derived, source finite Dq/J leak pack", "MISSING_PARENT_Q_AND_DQ_LEAK_VALUES", 1, True),
        ("Q2882_1_parent_q_object", "q: Phi_parent -> Q_obs", "geometry_certificate", "construct q from parent fields before matter/readout and show it is computable", "Q_NOT_COMPUTABLE_CURRENT_CORPUS", 2, False),
        ("Q2882_2_vertical_generator", "v_X", "generator_certificate", "write field-by-field parent transformation law including coframe, matter lift, constants, source normalization and boundary", "FIELD_BY_FIELD_ACTION_MISSING", 3, False),
        ("Q2882_3_Dq_operator", "Dq[v_X]", "operator_certificate", "compute the quotient derivative against the actual observed/source/readout stack", "MISSING_DQ_COMPUTATION", 4, False),
        ("Q2882_4_source_channel_extension", "q_source/q_test/q_marker/q_boundary", "extension_certificate", "prove source/test/marker/boundary silence or retain finite rows", "Dq_COFRAME_NOT_ENOUGH", 5, False),
        ("Q2882_5_no_mixed_morphism", "hidden coefficient maps", "coefficient_certificate", "forbid hidden invariants feeding visible coefficients or keep priors", "NO_MIXED_MORPHISM_NOT_PROVED", 6, False),
        ("Q2882_6_arena_projection", "R10/PPN/clock/orbit Dq leak projection", "bound_source_pack", "map any retained leak into arena observables with units and source paths", "MISSING_ARENA_PROJECTION", 7, False),
    ]
    return [
        add_common(
            {
                "queue_id": queue_id,
                "symbol": symbol,
                "row_type": row_type,
                "needed_action": action,
                "current_marker": marker,
                "priority": priority,
                "selected_for_next": selected,
                "accepted_live_input": False,
            }
        )
        for queue_id, symbol, row_type, action, marker, priority, selected in specs
    ]


def gate_rows() -> list[dict[str, Any]]:
    specs = [
        ("GATE2882_0_exact_contract", "conditional q-kernel theorem recorded", "PASS_CONTROL_ONLY", "the mathematical contract is exact but not signed by current MTS", False),
        ("GATE2882_1_parent_q", "parent q object is computable before matter/readout", "FAIL", "q remains a partial prior/candidate contract", False),
        ("GATE2882_2_vertical_generator", "v_X has field-by-field parent action", "FAIL", "current branch has symbols and candidate directions, not a transformation law", False),
        ("GATE2882_3_Dq_kernel", "Dq[v_X]=0 on an open local branch", "FAIL", "Dq is missing/nonzero in active countermodels", False),
        ("GATE2882_4_constraint_zero", "constraint/no-pole eliminates visible residual before q", "FAIL", "best route exists but parent origin is unsigned", False),
        ("GATE2882_5_extension_channels", "source/test/marker/boundary/hidden coefficient channels are silent", "FAIL", "Dq coframe silence would not be enough even if obtained", False),
        ("GATE2882_6_finite_leak_rows", "retained Dq/J leak rows can be scored", "FAIL", "values, units, source paths and arena projections are missing", False),
        ("GATE2882_7_local_claim", "local GR/Newton/PPN/R10/clock/orbit claim unlocked", "FAIL_CLOSED", "q/v certificate fails and finite leak bounds are nonclaim schema only", False),
    ]
    return [
        add_common(
            {
                "gate_id": gate_id,
                "criterion": criterion,
                "result": result,
                "reason": reason,
                "gate_passed": passed,
            }
        )
        for gate_id, criterion, result, reason, passed in specs
    ]


def runner_rows() -> list[dict[str, Any]]:
    return [
        add_common(
            {
                "runner_id": "RUN2882_0_geometry_gate_import",
                "status": "REFUSED_QV_CERTIFICATE_NOT_LIVE",
                "accepted_qv_certificates": 0,
                "required_qv_certificates": 1,
                "accepted_leak_rows": 0,
                "required_leak_rows_if_no_zero": 1,
                "reason": "q is not computable, v_X is not field-by-field parent-signed, Dq[v_X]=0 is not proved, and finite Dq/J leak rows have no numeric/source-backed inputs",
                "runner_ready": False,
                "claim_unlocked": False,
                "score_allowed": False,
            }
        )
    ]


def decision_rows() -> list[dict[str, Any]]:
    specs = [
        ("DEC2882_0_contract", "Write the exact q-kernel contract.", "COMPLETE_CONTROL_ONLY", "Dq[v]=0 is a valid route only after q and v_X are parent objects."),
        ("DEC2882_1_certificate", "Attempt to certify q/v_X on the live local branch.", "FAILED_CURRENT_CORPUS", "q object, field-by-field v_X and Dq computation remain unsigned."),
        ("DEC2882_2_countermodels", "Retain Dq countermodels.", "ACTIVE", "full metric/readout, source charge, hidden scalar morphism and boundary support can all re-open coupling."),
        ("DEC2882_3_leaks", "Stage Dq_vertical_leak and J_vertical_physical fallback rows.", "SCHEMA_ONLY", "finite rows exist as nonclaim placeholders until values, units and source paths are real."),
        ("DEC2882_4_JR", "Keep J_R/source-current zero blocked.", "BLOCKED", "the 2881 descent theorem cannot apply without the 2882 q/v certificate or finite leak bound."),
        ("DEC2882_5_next", "Select constraint-first q construction or Dq leak source-pack.", "SELECTED_2883", "cleaner route is to eliminate visible residuals before q; failing that, make the leak measurable."),
    ]
    return [
        add_common(
            {
                "decision_id": decision_id,
                "decision": decision,
                "result": result,
                "because": because,
            }
        )
        for decision_id, decision, result, because in specs
    ]


def next_rows() -> list[dict[str, Any]]:
    return [
        add_common(
            {
                "next_id": "NEXT2882_0_2883",
                "status": "selected_primary",
                "target_doc": "2883-Y5-R2FR-constraint-first-q-construction-or-Dq-leak-source-pack-under-AX1090.md",
                "target_script": "scripts/Y5_R2FR_constraint_first_q_construction_or_Dq_leak_source_pack_under_AX1090_2883.py",
                "mission": "try to derive a parent constraint/no-pole q construction that removes R_AB/Z/phi before matter/readout sees them; if it fails, source finite Dq_vertical_leak and J_vertical_physical rows with units, paths and arena projections",
                "forbidden_shortcuts": "no visible-residual-as-gauge naming; no post-readout deletion; no local GR/Newton/PPN/R10/WEP/clock/orbit claim without a signed theorem or source-backed leak bounds",
                "selected": True,
            }
        )
    ]


def copy_branch_outputs() -> list[dict[str, Any]]:
    pairs = [
        ("COPY2882_0_certificate", OUTPUTS["certificate"], BRANCH_OUTPUTS["certificate_copy"], "q/v object verticality certificate nonclaim copy"),
        ("COPY2882_1_countermodels", OUTPUTS["countermodels"], BRANCH_OUTPUTS["countermodel_copy"], "Dq countermodel review nonclaim copy"),
        ("COPY2882_2_fill", OUTPUTS["fill"], BRANCH_OUTPUTS["fill_copy"], "Dq leak fill attempt nonclaim copy"),
        ("COPY2882_3_next_queue", OUTPUTS["next"], BRANCH_OUTPUTS["next_queue"], "RAB queue handoff to constraint-first or Dq leak source-pack"),
    ]
    rows: list[dict[str, Any]] = []
    for copy_id, source, destination, purpose in pairs:
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(source, destination)
        rows.append(
            add_common(
                {
                    "copy_id": copy_id,
                    "source_table": str(source),
                    "copy_path": str(destination),
                    "purpose": purpose,
                    "exists": destination.exists(),
                }
            )
        )
    return rows


def remove_pycache() -> None:
    pycache = Path(__file__).resolve().parent / "__pycache__"
    if pycache.exists():
        shutil.rmtree(pycache)


def formalization_untouched() -> bool:
    if not FORMALIZATION.exists():
        return True
    for path in FORMALIZATION.rglob("*"):
        if path.is_file():
            modified = datetime.fromtimestamp(path.stat().st_mtime, timezone.utc)
            if modified > SCRIPT_START_UTC:
                return False
    return True


def generated_under_root(paths: list[Path]) -> bool:
    root_resolved = ROOT.resolve()
    for path in paths:
        try:
            path.resolve().relative_to(root_resolved)
        except ValueError:
            return False
    return True


def no_claim_flags(rows_by_name: dict[str, list[dict[str, Any]]]) -> bool:
    claim_keys = {
        "score_ready",
        "valid_prediction_row",
        "valid_for_claim",
        "claim_allowed",
        "certificate_signed",
        "theorem_zero",
        "excluded_now",
        "claim_safe",
        "accepted_live_input",
        "parent_signed",
        "gate_passed",
        "runner_ready",
        "claim_unlocked",
        "score_allowed",
    }
    for rows in rows_by_name.values():
        for row in rows:
            for key in claim_keys:
                if row.get(key) is True:
                    return False
    return True


def validation_rows(rows_by_name: dict[str, list[dict[str, Any]]], branch_rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    sources = rows_by_name["sources"]
    certificate = rows_by_name["certificate"]
    countermodels = rows_by_name["countermodels"]
    fill = rows_by_name["fill"]
    queue = rows_by_name["queue"]
    gates = rows_by_name["gates"]
    runner = rows_by_name["runner"]
    next_target = rows_by_name["next"]

    output_paths_without_validation = [path for key, path in OUTPUTS.items() if key != "validation"]
    branch_paths = list(BRANCH_OUTPUTS.values())
    all_generated_paths = output_paths_without_validation + branch_paths + [DOC, OUTPUTS["validation"]]

    checks = [
        ("VAL2882_0_sources_exist", all(row["path_exists"] for row in sources), "all registered source paths exist"),
        ("VAL2882_1_source_anchors", all(row["anchors_found"] for row in sources), "all registered source anchors were found"),
        ("VAL2882_2_exact_contract_recorded", any(row["cert_id"] == "CERT2882_0_exact_kernel_contract" for row in certificate), "exact q-kernel contract recorded"),
        ("VAL2882_3_certificate_not_promoted", not any(row["certificate_signed"] for row in certificate) and not any(row["theorem_zero"] for row in certificate), "no unsigned q/v theorem promoted"),
        ("VAL2882_4_joint_certificate_blocked", any(row["cert_id"] == "CERT2882_9_joint_certificate" and row["current_status"] == "NOT_CLOSED_KEEP_DQ_LEAK_ROWS" for row in certificate), "joint q/v certificate remains blocked"),
        ("VAL2882_5_countermodels_retained", len(countermodels) >= 8 and all(row["countermodel_active"] for row in countermodels) and not any(row["excluded_now"] for row in countermodels), "Dq countermodels retained"),
        ("VAL2882_6_fill_refused", not any(row["accepted_live_input"] for row in fill) and any("MISSING" in row["candidate_value"] for row in fill), "Dq/J leak rows remain nonclaim placeholders"),
        ("VAL2882_7_queue_selects_2883", any(row["queue_id"] == "Q2882_0_constraint_first_or_leak_pack" and row["selected_for_next"] is True for row in queue), "constraint-first or Dq leak pack selected next"),
        ("VAL2882_8_gates_fail_closed", all(row["gate_passed"] is False for row in gates), "all q/v claim gates fail closed"),
        ("VAL2882_9_runner_refused", runner[0]["status"] == "REFUSED_QV_CERTIFICATE_NOT_LIVE" and runner[0]["runner_ready"] is False, "runner remains refused"),
        ("VAL2882_10_next_target_2883", next_target[0]["next_id"] == "NEXT2882_0_2883" and next_target[0]["selected"] is True, "2883 target selected"),
        ("VAL2882_11_outputs_exist", all(path.exists() for path in output_paths_without_validation), "all generated CSV outputs exist before validation write"),
        ("VAL2882_12_branch_outputs_exist", all(path.exists() for path in branch_paths) and all(row["exists"] for row in branch_rows), "branch copies were written"),
        ("VAL2882_13_csv_parse", all(csv_parses(path) for path in output_paths_without_validation + branch_paths), "all generated CSV outputs parse"),
        ("VAL2882_14_no_claim_flags", no_claim_flags(rows_by_name | {"branches": branch_rows}), "no claim/score/prediction flags are true"),
        ("VAL2882_15_generated_under_post_checkpoint", generated_under_root(all_generated_paths), "all generated artifacts remain under post-checkpoint-work"),
        ("VAL2882_16_formalization_untouched", formalization_untouched(), "formalization-workbench was not modified during this run"),
        ("VAL2882_17_pycache_absent", not (Path(__file__).resolve().parent / "__pycache__").exists(), "scripts __pycache__ absent during validation"),
    ]
    rows = [
        {
            "validation_id": validation_id,
            "passed": passed,
            "detail": detail,
            "timestamp_utc": now(),
        }
        for validation_id, passed, detail in checks
    ]
    rows.append(
        {
            "validation_id": "VAL2882_OVERALL",
            "passed": all(row["passed"] for row in rows),
            "detail": "2882 wrote the q-object/vertical-generator certificate, rejected current q/v promotion, retained Dq/J leak placeholders, and selected constraint-first q construction or Dq leak source-pack for 2883.",
            "timestamp_utc": now(),
        }
    )
    return rows


def md_table(rows: list[dict[str, Any]], columns: list[str]) -> str:
    header = "| " + " | ".join(columns) + " |"
    separator = "| " + " | ".join("---" for _ in columns) + " |"
    body = []
    for row in rows:
        cells = []
        for column in columns:
            value = str(row.get(column, ""))
            value = value.replace("\n", " ").replace("|", "\\|")
            cells.append(value)
        body.append("| " + " | ".join(cells) + " |")
    return "\n".join([header, separator, *body])


def write_doc(rows_by_name: dict[str, list[dict[str, Any]]], branch_rows: list[dict[str, Any]], validation: list[dict[str, Any]]) -> None:
    text = f"""# 2882 - Y5 R2FR q Object Vertical Generator Certificate Or Dq Leak Row Under AX1090

Status: `Y5_R2FR_2882_qv_certificate_rejected_Dq_leaks_retained_2883_next`

## Private Verdict

2882 does the geometry gate cleanly.

The exact route is real: if a parent quotient map `q` exists before matter/readout, if the local residual generator `v_X` is a real field-space transformation, and if `Dq[v_X]=0` on an open local branch, then the q-visible part of the local residual is silent. That would let the 2881 matter-descent theorem bite.

But current MTS does not yet sign that bundle. The live evidence still says `q` is not computable, `v_X` is not field-by-field defined, and active countermodels make `Dq[v_X]` nonzero or unproved when the observed metric/coframe/source stack is included. So no local-GR/Newton/PPN/R10/clock/orbit claim is unlocked.

The best next route is not to keep saying "vertical" louder. It is to either derive a constraint/no-pole parent construction that removes `R_AB/Z/phi` before matter sees them, or make the retained `Dq_vertical_leak` and `J_vertical_physical` rows numeric/source-backed. That is the next punch.

## Source Register

{md_table(rows_by_name["sources"], ["source_id", "role", "path_exists", "anchors_found", "missing_anchors", "valid_for_claim"])}

## q Object Verticality Certificate

{md_table(rows_by_name["certificate"], ["cert_id", "required_clause", "formal_statement", "current_status", "certificate_signed", "theorem_zero", "valid_for_claim"])}

## Dq Kernel Countermodel Review

{md_table(rows_by_name["countermodels"], ["countermodel_id", "countermodel", "why_dangerous", "current_status", "countermodel_active", "excluded_now", "valid_for_claim"])}

## Dq Leak Fill Attempt

{md_table(rows_by_name["fill"], ["fill_id", "quantity", "candidate_formula", "candidate_value", "status", "failure_mode", "accepted_live_input", "valid_for_claim"])}

## q/v Acquisition Queue

{md_table(rows_by_name["queue"], ["queue_id", "symbol", "row_type", "needed_action", "current_marker", "priority", "selected_for_next", "valid_for_claim"])}

## Acceptance Gates

{md_table(rows_by_name["gates"], ["gate_id", "criterion", "result", "reason", "gate_passed", "valid_for_claim"])}

## Runner Status

{md_table(rows_by_name["runner"], ["runner_id", "status", "accepted_qv_certificates", "accepted_leak_rows", "reason", "runner_ready", "valid_for_claim"])}

## Decision Ledger

{md_table(rows_by_name["decision"], ["decision_id", "decision", "result", "because", "valid_for_claim"])}

## Next Target

{md_table(rows_by_name["next"], ["next_id", "status", "target_doc", "target_script", "mission", "selected", "valid_for_claim"])}

## Branch Copies

{md_table(branch_rows, ["copy_id", "source_table", "copy_path", "purpose", "exists", "valid_for_claim"])}

## Validation

{md_table(validation, ["validation_id", "passed", "detail", "timestamp_utc"])}
"""
    DOC.write_text(text, encoding="utf-8")


def main() -> None:
    remove_pycache()

    rows_by_name = {
        "sources": source_register_rows(),
        "certificate": certificate_rows(),
        "countermodels": countermodel_rows(),
        "fill": fill_rows(),
        "queue": queue_rows(),
        "gates": gate_rows(),
        "runner": runner_rows(),
        "decision": decision_rows(),
        "next": next_rows(),
    }

    for name, rows in rows_by_name.items():
        write_csv(OUTPUTS[name], rows)

    branch_rows = copy_branch_outputs()
    write_csv(OUTPUTS["branches"], branch_rows)
    rows_by_name["branches"] = branch_rows

    remove_pycache()
    validation = validation_rows(rows_by_name, branch_rows)
    write_csv(OUTPUTS["validation"], validation)
    write_doc(rows_by_name, branch_rows, validation)
    remove_pycache()

    print(f"Wrote {DOC}")
    print(f"Wrote {OUTPUTS['validation']}")
    overall = next(row for row in validation if row["validation_id"] == "VAL2882_OVERALL")
    print(f"VAL2882_OVERALL={overall['passed']}")


if __name__ == "__main__":
    main()

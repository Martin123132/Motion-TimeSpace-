from __future__ import annotations

import csv
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(r"D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main")
POST_CHECKPOINT = ROOT / "post-checkpoint-work"
FORMALIZATION = ROOT / "formalization-workbench"
RESIDUALS = POST_CHECKPOINT / "source-intake" / "mts_residuals"

OUTPUT_DOC = POST_CHECKPOINT / "802-Y5-R10-parent-ZL-evenness-and-gradient-signature-gate.md"
NEXT_TARGET = "803-Y5-R10-transition-shell-exact-cancellation-projector-or-quarantine.md"

SOURCE_REGISTER_PATH = RESIDUALS / "P8_Y5_R10_802_SOURCE_REGISTER.csv"
SIGNATURE_TEST_PATH = RESIDUALS / "P8_Y5_R10_802_PARENT_SIGNATURE_TEST.csv"
LEAKAGE_COORDINATE_PATH = RESIDUALS / "P8_Y5_R10_802_LEAKAGE_COORDINATE_REPAIR.csv"
EVENNESS_GATE_PATH = RESIDUALS / "P8_Y5_R10_802_SCALAR_EVENNESS_GATE.csv"
GRADIENT_GATE_PATH = RESIDUALS / "P8_Y5_R10_802_GRADIENT_POWER_GATE.csv"
TRANSITION_SHELL_PATH = RESIDUALS / "P8_Y5_R10_802_TRANSITION_SHELL_OBSTRUCTION.csv"
CLOSURE_UPDATE_PATH = RESIDUALS / "P8_Y5_R10_802_CLOSURE_UPDATE.csv"
DECISION_PATH = RESIDUALS / "P8_Y5_R10_802_DERIVATION_DECISION.csv"
NONCLAIM_SUMMARY_PATH = RESIDUALS / "P8_Y5_R10_802_NONCLAIM_SUMMARY.csv"
VALIDATION_PATH = RESIDUALS / "P8_Y5_BRR545_802_VALIDATION.csv"

STATUS = "Y5_R10_802_parent_ZL_evenness_partial_far_local_gradient_conditional_transition_shell_open_nonclaim"
CLAIM_CEILING = "partial_signature_gate_only_no_transition_shell_or_Kperp_local_GR_claim"
FORMALIZATION_CUTOFF = datetime(2026, 5, 31, 14, 42, 0)

OUTPUT_PATHS = [
    OUTPUT_DOC,
    SOURCE_REGISTER_PATH,
    SIGNATURE_TEST_PATH,
    LEAKAGE_COORDINATE_PATH,
    EVENNESS_GATE_PATH,
    GRADIENT_GATE_PATH,
    TRANSITION_SHELL_PATH,
    CLOSURE_UPDATE_PATH,
    DECISION_PATH,
    NONCLAIM_SUMMARY_PATH,
    VALIDATION_PATH,
]

SOURCE_SPECS = [
    {
        "source_id": "801_doc",
        "path": POST_CHECKPOINT / "801-Y5-R10-double-zero-fixed-point-parent-mechanism-or-local-branch-closure-ledger.md",
        "needles": ["norm-only dependence on a leakage vector gives pL=pT=2", "Z_L, G_AB, parity/evenness, gradient control, and Kperp are not signed"],
        "role": "immediate 801 scalar double-zero theorem and unsigned parent signatures",
    },
    {
        "source_id": "801_validation",
        "path": RESIDUALS / "P8_Y5_BRR545_801_VALIDATION.csv",
        "needles": ["V801_4_scalar_double_zero_theorem_constructed,pass", "V801_11_no_local_GR_claim,pass"],
        "role": "prior checkpoint validation",
    },
    {
        "source_id": "spine_ZL_candidate",
        "path": FORMALIZATION / "07-unification-spine.md",
        "needles": ["Z_L^A = U_B H_L^A(X_B)", "D_L = sqrt(s_L) give a non-cheating candidate with D_L <= U_B"],
        "role": "candidate leakage vector and distance bound route",
    },
    {
        "source_id": "spine_evenness_and_symmetry",
        "path": FORMALIZATION / "07-unification-spine.md",
        "needles": ["scalar evenness has a clean theorem form if signed leakage coordinates z_L", "leakage_frame_symmetry_partial_vector_tensor_only_scalar_channels_block"],
        "role": "signed coordinate and frame-symmetry status",
    },
    {
        "source_id": "spine_scalar_repair",
        "path": FORMALIZATION / "07-unification-spine.md",
        "needles": ["z_Lcg should be pruned until its reference", "replacing dangerous |z| source terms with smooth quadratic"],
        "role": "scalar-channel stationarity and smooth repair status",
    },
    {
        "source_id": "spine_gradient_and_shell",
        "path": FORMALIZATION / "07-unification-spine.md",
        "needles": ["U_B^2 suppression of far-local gradients", "transition shells with", "Derived local GR is not reached yet"],
        "role": "far-local gradient win and transition-shell obstruction",
    },
    {
        "source_id": "red_ZL_candidate",
        "path": FORMALIZATION / "06-consistency-red-team.md",
        "needles": ["Z_L can be defined from universal X_B ingredients", "D_L <= U_B follows algebraically if H_L is bounded and G_AB is normalized"],
        "role": "red-team candidate invariant and unsigned bound",
    },
    {
        "source_id": "red_scalar_symmetry_block",
        "path": FORMALIZATION / "06-consistency-red-team.md",
        "needles": ["leakage_frame_symmetry_partial_vector_tensor_only_scalar_channels_block", "z_theta, z_dotB, and z_Lcg are true scalar channels"],
        "role": "partial symmetry win and scalar-channel obstruction",
    },
    {
        "source_id": "red_gradient_shell_block",
        "path": FORMALIZATION / "06-consistency-red-team.md",
        "needles": ["repaired_local_gradient_power_far_local_conditional_transition_shell_open", "transition shells have U_B=O(1)"],
        "role": "gradient power and transition-shell obstruction",
    },
]


def utc_stamp() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def needle_status(path: Path, needles: list[str]) -> str:
    if not path.exists():
        return "missing_file"
    source_text = read_text(path)
    missing_needles = [needle for needle in needles if needle not in source_text]
    if missing_needles:
        return "missing_needles:" + ";".join(missing_needles)
    return "pass"


def write_csv(path: Path, rows: list[dict[str, object]], fieldnames: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow(row)


def markdown_table(rows: list[dict[str, object]], columns: list[str]) -> str:
    if not rows:
        return "_No rows._"
    lines = [
        "| " + " | ".join(columns) + " |",
        "| " + " | ".join(["---"] * len(columns)) + " |",
    ]
    for row in rows:
        values = [str(row.get(column, "")).replace("\n", " ").replace("|", "\\|") for column in columns]
        lines.append("| " + " | ".join(values) + " |")
    return "\n".join(lines)


def validation_file_clean(check_number: int) -> tuple[bool, str]:
    validation_file = RESIDUALS / f"P8_Y5_BRR545_{check_number}_VALIDATION.csv"
    if not validation_file.exists():
        return False, f"missing={validation_file}"
    failures: list[str] = []
    with validation_file.open("r", encoding="utf-8", newline="") as handle:
        for row in csv.DictReader(handle):
            if row.get("result") != "pass":
                failures.append(f"{row.get('check_id')}={row.get('result')}")
    if failures:
        return False, ";".join(failures)
    return True, f"{validation_file.name} clean"


def formalization_change_count() -> int:
    if not FORMALIZATION.exists():
        return -1
    return sum(
        1
        for candidate_path in FORMALIZATION.rglob("*")
        if candidate_path.is_file() and datetime.fromtimestamp(candidate_path.stat().st_mtime) > FORMALIZATION_CUTOFF
    )


def source_register_rows(generated_utc: str) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    for spec in SOURCE_SPECS:
        source_path = spec["path"]
        rows.append(
            {
                "source_id": spec["source_id"],
                "path": str(source_path),
                "exists": str(source_path.exists()).lower(),
                "needle_check": needle_status(source_path, spec["needles"]),
                "role": spec["role"],
                "valid_for_claim": "false",
                "generated_utc": generated_utc,
            }
        )
    return rows


def signature_test_rows(generated_utc: str) -> list[dict[str, object]]:
    return [
        {
            "signature_id": "SIG802_0_signed_leakage_coordinates",
            "test": "Can signed primitive leakage coordinates be defined from universal variables rather than absolute-value classifiers?",
            "result": "partial_candidate",
            "derivation_or_block": "Use smooth signed channels z_theta, z_dotB, plus vector/tensor components; prune z_Lcg until its reference is parent-derived.",
            "claim_effect": "makes evenness meaningful but does not parent-sign it",
            "next_action": "derive coordinates from parent/coarse-graining map or keep closure",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "signature_id": "SIG802_1_distance_bound",
            "test": "Does D_L=O(U_B) follow non-cheatingly?",
            "result": "conditional_pass",
            "derivation_or_block": "If Z_L^A=U_B H_L^A(X_B), G_AB positive, and ||H_L||_G<=C_H, then D_L<=C_H U_B.",
            "claim_effect": "usable as finite-margin closure; not parent-derived because H_L and G_AB are unsigned",
            "next_action": "source G_AB from kinetic/Hessian metric and bound H_L",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "signature_id": "SIG802_2_vector_tensor_evenness",
            "test": "Does leakage-frame symmetry remove linear vector/tensor scalar readouts?",
            "result": "conditional_partial_pass",
            "derivation_or_block": "If local background has no preferred leakage-frame direction, reflection/rotation symmetry kills linear vector/tensor contractions.",
            "claim_effect": "removes one class of first-order leaks conditionally",
            "next_action": "derive the symmetry from the parent local vacuum/isotropy branch",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "signature_id": "SIG802_3_scalar_channel_evenness",
            "test": "Does the same symmetry remove true scalar linear channels?",
            "result": "fail_as_parent_signature",
            "derivation_or_block": "No. z_theta and z_dotB are scalar channels; ordinary frame symmetry does not force their linear coefficients to vanish.",
            "claim_effect": "blocks pL/pT promotion unless scalar readouts are parent-signed as smooth quadratic invariants",
            "next_action": "derive stationarity or replace scalar sources with parent-derived Q_theta=z_theta^2 and Q_dotB=z_dotB^2",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "signature_id": "SIG802_4_gradient_power",
            "test": "Does repaired scalar closure suppress gradients?",
            "result": "conditional_far_local_pass_only",
            "derivation_or_block": "If coefficients/log-gradients are bounded and U_B<<1, quadratic scalar readouts give nabla f=O(U_B^2/L_B).",
            "claim_effect": "far-local q_loc can be quiet; transition shells remain unsafe",
            "next_action": "separate transition-shell exact cancellation/projector/quarantine theorem",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "signature_id": "SIG802_5_Kperp",
            "test": "Does any scalar Z_L/evenness repair control K_perp?",
            "result": "fail_separate_tensor_gate",
            "derivation_or_block": "No. K_perp still needs coercive tensor operator, zero/decay boundary data, or explicit local bound.",
            "claim_effect": "blocks full local PPN vector pass",
            "next_action": "return to Kperp after transition shell is not projecting locally",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
    ]


def leakage_coordinate_rows(generated_utc: str) -> list[dict[str, object]]:
    return [
        {
            "coordinate_id": "Z802_0_ztheta",
            "candidate": "z_theta = theta/theta_ref or smooth signed expansion scalar",
            "status": "signed_coordinate_candidate",
            "why_kept": "theta sign is meaningful; avoids E_theta=|theta| cusp as a source",
            "parent_gap": "theta_ref and local stationary reference must be parent-derived",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "coordinate_id": "Z802_1_zdotB",
            "candidate": "z_dotB = tau_B u^mu nabla_mu B_env",
            "status": "signed_coordinate_candidate",
            "why_kept": "time-directed drift sign is meaningful and can be squared smoothly",
            "parent_gap": "tau_B and preferred observer/readout must descend from parent structure",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "coordinate_id": "Z802_2_vector_tensor_modes",
            "candidate": "trace-free/vector/tensor leakage components in a local orthonormal frame",
            "status": "conditional_symmetry_candidate",
            "why_kept": "local isotropy/reflection can kill linear scalar contractions",
            "parent_gap": "must show no preferred local leakage-frame direction",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "coordinate_id": "Z802_3_zLcg",
            "candidate": "z_Lcg",
            "status": "prune_until_reference_derived",
            "why_kept": "not kept as source channel",
            "parent_gap": "universal L_cg reference not parent-derived; including it creates arbitrary scalar leakage",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
    ]


def evenness_gate_rows(generated_utc: str) -> list[dict[str, object]]:
    return [
        {
            "gate_id": "EV802_0_bad_abs_value",
            "input_form": "E_theta=|theta|/(3H_bg) or any |z| source term",
            "power": "O(|z|)",
            "gate_result": "fail_for_double_zero",
            "reason": "absolute-value classifiers are fine for routing but unsafe as local metric/source readouts",
            "replacement_or_requirement": "use smooth signed coordinates and source only through z^2 or stationary coefficients",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "gate_id": "EV802_1_smooth_quadratic_scalar",
            "input_form": "Q_theta=z_theta^2, Q_dotB=z_dotB^2",
            "power": "O(D_L^2)",
            "gate_result": "closure_pass_not_parent_signed",
            "reason": "smooth quadratic readouts remove scalar linear leakage",
            "replacement_or_requirement": "derive why parent action/readout uses Q terms rather than |z| terms",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "gate_id": "EV802_2_norm_only_readout",
            "input_form": "m_L-m_*=M(Q_theta,Q_dotB,R_vec,R_tensor)",
            "power": "O(D_L^2)",
            "gate_result": "conditional_theorem",
            "reason": "all arguments vanish quadratically or are killed by symmetry",
            "replacement_or_requirement": "parent-sign smoothness, stationarity, and no odd scalar terms",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "gate_id": "EV802_3_trace_readout",
            "input_form": "L_cg^-2 F_L-Lambda_loc=T(Q_theta,Q_dotB,R_vec,R_tensor)",
            "power": "O(D_L^2)",
            "gate_result": "conditional_theorem",
            "reason": "same scalar smoothness condition gives pT=2",
            "replacement_or_requirement": "parent-sign trace baseline stationarity and coefficient boundedness",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
    ]


def gradient_gate_rows(generated_utc: str) -> list[dict[str, object]]:
    return [
        {
            "gradient_id": "GR802_0_Z_gradient",
            "assumptions": "Z_L=U_B H_L, |nabla U_B|=O(U_B/L_B), H_L bounded, nabla H_L=O(1/L_B)",
            "derivation": "nabla Z_L=(nabla U_B)H_L+U_B nabla H_L=O(U_B/L_B)",
            "result": "far-local leakage-gradient is linearly screened",
            "status": "conditional_far_local_pass",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "gradient_id": "GR802_1_quadratic_readout_gradient",
            "assumptions": "f=O(Z_L^2), nabla Z_L=O(U_B/L_B), Z_L=O(U_B)",
            "derivation": "nabla f=O(Z_L nabla Z_L)=O(U_B^2/L_B)",
            "result": "far-local scalar q_loc channel gains U_B^2 suppression",
            "status": "conditional_far_local_pass",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "gradient_id": "GR802_2_coefficient_budget",
            "assumptions": "M_2,T_2,S_smooth and log-gradients finite and universal",
            "derivation": "bounded coefficients keep quadratic power counting from being eaten by large prefactors",
            "result": "requires explicit coefficient/source bounds",
            "status": "open_parent_bound",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "gradient_id": "GR802_3_transition_shell",
            "assumptions": "U_B=O(1) in shell near B_env~B_*",
            "derivation": "the U_B^2 small factor is no longer small, so direct local projection can exceed PPN budgets",
            "result": "transition shell must be exactly cancelled, projected away, or quarantined from local metric readout",
            "status": "blocks_derived_local_GR",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
    ]


def transition_shell_rows(generated_utc: str) -> list[dict[str, object]]:
    return [
        {
            "shell_id": "TS802_0_direct_projection",
            "route": "direct local metric projection of transition current",
            "status": "rejected_or_unclaimed",
            "reason": "when U_B=O(1), quadratic far-local suppression is absent",
            "required_repair": "do not treat direct shell projection as local GR safe",
            "next_target": NEXT_TARGET,
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "shell_id": "TS802_1_exact_cancellation",
            "route": "derive exact cancellation of local transition shell contribution",
            "status": "open_best_derivation_route",
            "reason": "would preserve derivability without hiding the shell",
            "required_repair": "parent identity or Bianchi/projector theorem that sets P_loc q_tr=0",
            "next_target": NEXT_TARGET,
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "shell_id": "TS802_2_projector_quarantine",
            "route": "project shell current only into galaxy/cosmology exchange channels",
            "status": "open_closure_route",
            "reason": "keeps local metric branch quiet but must not be selected per dataset",
            "required_repair": "universal projector from parent invariants, not a hand switch",
            "next_target": NEXT_TARGET,
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
    ]


def closure_update_rows(generated_utc: str) -> list[dict[str, object]]:
    return [
        {
            "closure_id": "CU802_0_scalar_closure_refined",
            "update": "Scalar local branch should use smooth quadratic scalar channels and prune z_Lcg until its reference is derived.",
            "status": "cleaner_closure_not_parent_derived",
            "allowed_use": "finite-margin internal calculators only",
            "blocking_gap": "stationarity/evenness not parent-signed",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "closure_id": "CU802_1_far_local_gradient",
            "update": "Far-local gradients can be conditionally U_B^2 suppressed under bounded log-gradient/coefficient assumptions.",
            "status": "conditional_far_local_win",
            "allowed_use": "far-local branch estimates, not transition-shell claims",
            "blocking_gap": "transition shell and coefficients remain unproven",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "closure_id": "CU802_2_full_local_GR_status",
            "update": "Derived GR/Newton remains blocked by transition shell and Kperp.",
            "status": "local_GR_claim_false",
            "allowed_use": "private theory discipline only",
            "blocking_gap": "exact shell cancellation/projector/quarantine plus Kperp theorem still missing",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
    ]


def decision_rows(generated_utc: str) -> list[dict[str, object]]:
    return [
        {
            "decision_id": "D802_0_ZL_parent_signature",
            "question": "Is Z_L/evenness parent-signed?",
            "answer": "No. Signed coordinates and smooth quadratic repairs are candidate/closure structure, not action-derived signatures.",
            "status": "not_parent_signed",
            "next_target": NEXT_TARGET,
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "decision_id": "D802_1_useful_partial_win",
            "question": "Did the gate improve the local route?",
            "answer": "Yes. It isolates true scalar channels, prunes z_Lcg, and gives conditional far-local U_B^2 gradient suppression.",
            "status": "partial_theory_progress",
            "next_target": NEXT_TARGET,
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "decision_id": "D802_2_main_blocker",
            "question": "What blocks derived local GR now?",
            "answer": "Transition shells with U_B=O(1) and Kperp remain the main obstructions; far-local suppression is not enough.",
            "status": "transition_shell_and_Kperp_block",
            "next_target": NEXT_TARGET,
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "decision_id": "D802_3_next_route",
            "question": "What is the next best route?",
            "answer": "Attempt exact transition-shell cancellation, a parent-derived projector theorem, or explicit local quarantine; then return to Kperp.",
            "status": "attempt_transition_shell_theorem",
            "next_target": NEXT_TARGET,
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
    ]


def nonclaim_summary_rows(generated_utc: str) -> list[dict[str, object]]:
    return [
        {
            "status": STATUS,
            "claim_ceiling": CLAIM_CEILING,
            "what_improved": "Z_L route is refined: vector/tensor linear terms can be conditionally removed, scalar channels must be smooth quadratic, and far-local gradients can get U_B^2 suppression.",
            "what_blocks_claim": "Scalar stationarity/evenness is not parent-derived, transition shells lose the small U_B suppression, and Kperp remains open.",
            "next_target": NEXT_TARGET,
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        }
    ]


def all_outputs_scoped() -> bool:
    post_root = POST_CHECKPOINT.resolve()
    return all(path.resolve().is_relative_to(post_root) for path in OUTPUT_PATHS)


def all_rows_nonclaim(row_groups: list[list[dict[str, object]]]) -> bool:
    for row_group in row_groups:
        for row in row_group:
            if "valid_for_claim" in row and str(row["valid_for_claim"]).lower() != "false":
                return False
    return True


def validation_rows(
    sources: list[dict[str, object]],
    signatures: list[dict[str, object]],
    coordinates: list[dict[str, object]],
    evenness: list[dict[str, object]],
    gradients: list[dict[str, object]],
    shells: list[dict[str, object]],
    closures: list[dict[str, object]],
    decisions: list[dict[str, object]],
    summary: list[dict[str, object]],
) -> list[dict[str, object]]:
    source_ok = all(row["exists"] == "true" and row["needle_check"] == "pass" for row in sources)
    prior_ok, prior_detail = validation_file_clean(801)
    row_groups = [sources, signatures, coordinates, evenness, gradients, shells, closures, decisions, summary]
    nonclaim_ok = all_rows_nonclaim(row_groups)
    formalization_count = formalization_change_count()
    scalar_fail = any(row["signature_id"] == "SIG802_3_scalar_channel_evenness" and row["result"] == "fail_as_parent_signature" for row in signatures)
    far_local_pass = any(row["gradient_id"] == "GR802_1_quadratic_readout_gradient" and row["status"] == "conditional_far_local_pass" for row in gradients)
    shell_block = any(row["gradient_id"] == "GR802_3_transition_shell" and row["status"] == "blocks_derived_local_GR" for row in gradients)
    return [
        {"check_id": "V802_0_sources_exist_and_needles", "result": "pass" if source_ok else "fail", "detail": "all source paths exist and needles are present"},
        {"check_id": "V802_1_prior_801_clean", "result": "pass" if prior_ok else "fail", "detail": prior_detail},
        {"check_id": "V802_2_outputs_scoped", "result": "pass" if all_outputs_scoped() else "fail", "detail": str(POST_CHECKPOINT)},
        {"check_id": "V802_3_all_rows_nonclaim", "result": "pass" if nonclaim_ok else "fail", "detail": "all generated rows valid_for_claim=false"},
        {"check_id": "V802_4_ZL_candidate_not_claim", "result": "pass" if any(row["signature_id"] == "SIG802_0_signed_leakage_coordinates" and row["result"] == "partial_candidate" for row in signatures) else "fail", "detail": "signed leakage coordinates remain candidate only"},
        {"check_id": "V802_5_scalar_channel_block_recorded", "result": "pass" if scalar_fail else "fail", "detail": "true scalar channels block parent evenness"},
        {"check_id": "V802_6_smooth_quadratic_repair_nonclaim", "result": "pass" if any(row["gate_id"] == "EV802_1_smooth_quadratic_scalar" and row["gate_result"] == "closure_pass_not_parent_signed" for row in evenness) else "fail", "detail": "quadratic scalar repair is closure only"},
        {"check_id": "V802_7_far_local_gradient_conditional", "result": "pass" if far_local_pass else "fail", "detail": "far-local gradient has conditional U_B^2 suppression"},
        {"check_id": "V802_8_transition_shell_blocks_claim", "result": "pass" if shell_block else "fail", "detail": "transition shell remains local-GR blocker"},
        {"check_id": "V802_9_Kperp_open", "result": "pass" if any(row["signature_id"] == "SIG802_5_Kperp" and row["result"] == "fail_separate_tensor_gate" for row in signatures) else "fail", "detail": "Kperp remains separate tensor gate"},
        {"check_id": "V802_10_next_target_selected", "result": "pass" if decisions[-1]["next_target"] == NEXT_TARGET else "fail", "detail": NEXT_TARGET},
        {"check_id": "V802_11_no_local_GR_claim", "result": "pass" if any(row["status"] == "local_GR_claim_false" for row in closures) else "fail", "detail": "derived GR/Newton remains blocked"},
        {"check_id": "V802_12_formalization_workbench_untouched", "result": "pass" if formalization_count == 0 else "fail", "detail": f"formalization_changed_after_cutoff={formalization_count}"},
        {"check_id": "V802_13_validation_rows_ready", "result": "pass", "detail": "validation table constructed"},
    ]


def build_doc(
    generated_utc: str,
    sources: list[dict[str, object]],
    signatures: list[dict[str, object]],
    coordinates: list[dict[str, object]],
    evenness: list[dict[str, object]],
    gradients: list[dict[str, object]],
    shells: list[dict[str, object]],
    closures: list[dict[str, object]],
    decisions: list[dict[str, object]],
    summary: list[dict[str, object]],
    validations: list[dict[str, object]],
) -> str:
    return f"""# 802 - Y5 R10 Parent ZL Evenness And Gradient Signature Gate

Current result: **`Z_L` is a real route, but not a parent signature yet**. The gate improves the local-GR reduction path by separating three things that were previously tangled: signed leakage coordinates, scalar evenness, and gradient power. Vector/tensor leakage can be conditionally silenced by local reflection/isotropy. True scalar channels cannot. The scalar branch only becomes safe as a smooth quadratic closure (`Q_theta=z_theta^2`, `Q_dotB=z_dotB^2`) with `z_Lcg` pruned until its reference is derived. This gives far-local `U_B^2` gradient suppression if coefficients/log-gradients are bounded, but transition shells with `U_B=O(1)` remain a hard local-PPN obstruction.

Generated UTC: `{generated_utc}`

## Non-Claim Summary

{markdown_table(summary, ["status", "claim_ceiling", "what_improved", "what_blocks_claim", "next_target", "valid_for_claim"])}

## Parent Signature Test

{markdown_table(signatures, ["signature_id", "test", "result", "derivation_or_block", "claim_effect", "next_action", "valid_for_claim"])}

## Leakage Coordinate Repair

{markdown_table(coordinates, ["coordinate_id", "candidate", "status", "why_kept", "parent_gap", "valid_for_claim"])}

## Scalar Evenness Gate

{markdown_table(evenness, ["gate_id", "input_form", "power", "gate_result", "reason", "replacement_or_requirement", "valid_for_claim"])}

## Gradient Power Gate

{markdown_table(gradients, ["gradient_id", "assumptions", "derivation", "result", "status", "valid_for_claim"])}

## Transition Shell Obstruction

{markdown_table(shells, ["shell_id", "route", "status", "reason", "required_repair", "next_target", "valid_for_claim"])}

## Closure Update

{markdown_table(closures, ["closure_id", "update", "status", "allowed_use", "blocking_gap", "valid_for_claim"])}

## Decision

{markdown_table(decisions, ["decision_id", "question", "answer", "status", "next_target", "valid_for_claim"])}

## Source Register

{markdown_table(sources, ["source_id", "path", "exists", "needle_check", "role", "valid_for_claim"])}

## Validation

{markdown_table(validations, ["check_id", "result", "detail"])}

## Verdict

The local route is better than it looked at 800, but still not claimable. The cleanest scalar closure is now:

```text
z_Lcg: pruned until parent reference exists
Q_theta = z_theta^2
Q_dotB = z_dotB^2
m_L - m_* = M(Q_theta, Q_dotB, R_vec, R_tensor)
L_cg^-2 F_L - Lambda_loc = T(Q_theta, Q_dotB, R_vec, R_tensor)
```

For far-local screened regions this can give:

```text
Z_L = U_B H_L,
nabla Z_L = O(U_B/L_B),
nabla(m_L-m_*), nabla T_L = O(U_B^2/L_B).
```

But the boxing bell is not rung yet: in transition shells `U_B=O(1)`, so the suppression can vanish. That shell must be exactly cancelled, universally projected out of the local metric branch, or quarantined by a parent theorem. `K_perp` also remains a separate tensor problem.

## Next Target

`{NEXT_TARGET}`
"""


def write_outputs() -> None:
    generated_utc = utc_stamp()
    sources = source_register_rows(generated_utc)
    signatures = signature_test_rows(generated_utc)
    coordinates = leakage_coordinate_rows(generated_utc)
    evenness = evenness_gate_rows(generated_utc)
    gradients = gradient_gate_rows(generated_utc)
    shells = transition_shell_rows(generated_utc)
    closures = closure_update_rows(generated_utc)
    decisions = decision_rows(generated_utc)
    summary = nonclaim_summary_rows(generated_utc)
    validations = validation_rows(sources, signatures, coordinates, evenness, gradients, shells, closures, decisions, summary)

    write_csv(SOURCE_REGISTER_PATH, sources, ["source_id", "path", "exists", "needle_check", "role", "valid_for_claim", "generated_utc"])
    write_csv(SIGNATURE_TEST_PATH, signatures, ["signature_id", "test", "result", "derivation_or_block", "claim_effect", "next_action", "valid_for_claim", "generated_utc"])
    write_csv(LEAKAGE_COORDINATE_PATH, coordinates, ["coordinate_id", "candidate", "status", "why_kept", "parent_gap", "valid_for_claim", "generated_utc"])
    write_csv(EVENNESS_GATE_PATH, evenness, ["gate_id", "input_form", "power", "gate_result", "reason", "replacement_or_requirement", "valid_for_claim", "generated_utc"])
    write_csv(GRADIENT_GATE_PATH, gradients, ["gradient_id", "assumptions", "derivation", "result", "status", "valid_for_claim", "generated_utc"])
    write_csv(TRANSITION_SHELL_PATH, shells, ["shell_id", "route", "status", "reason", "required_repair", "next_target", "valid_for_claim", "generated_utc"])
    write_csv(CLOSURE_UPDATE_PATH, closures, ["closure_id", "update", "status", "allowed_use", "blocking_gap", "valid_for_claim", "generated_utc"])
    write_csv(DECISION_PATH, decisions, ["decision_id", "question", "answer", "status", "next_target", "valid_for_claim", "generated_utc"])
    write_csv(NONCLAIM_SUMMARY_PATH, summary, ["status", "claim_ceiling", "what_improved", "what_blocks_claim", "next_target", "valid_for_claim", "generated_utc"])
    write_csv(VALIDATION_PATH, validations, ["check_id", "result", "detail"])

    OUTPUT_DOC.write_text(
        build_doc(generated_utc, sources, signatures, coordinates, evenness, gradients, shells, closures, decisions, summary, validations),
        encoding="utf-8",
    )

    failed_checks = [row for row in validations if row["result"] != "pass"]
    if failed_checks:
        failed_text = "; ".join(f"{row['check_id']}={row['detail']}" for row in failed_checks)
        raise SystemExit(f"802 validation failed: {failed_text}")

    print(f"wrote {OUTPUT_DOC}")
    print(f"wrote {VALIDATION_PATH}")
    print(f"status={STATUS}")
    print(f"next={NEXT_TARGET}")


if __name__ == "__main__":
    write_outputs()

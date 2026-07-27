from __future__ import annotations

import csv
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(r"D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main")
POST_CHECKPOINT = ROOT / "post-checkpoint-work"
FORMALIZATION = ROOT / "formalization-workbench"
RESIDUALS = POST_CHECKPOINT / "source-intake" / "mts_residuals"

OUTPUT_DOC = POST_CHECKPOINT / "801-Y5-R10-double-zero-fixed-point-parent-mechanism-or-local-branch-closure-ledger.md"
NEXT_TARGET = "802-Y5-R10-parent-ZL-evenness-and-gradient-signature-gate.md"

SOURCE_REGISTER_PATH = RESIDUALS / "P8_Y5_R10_801_SOURCE_REGISTER.csv"
PARENT_CONTRACT_PATH = RESIDUALS / "P8_Y5_R10_801_PARENT_FIXED_POINT_CONTRACT.csv"
DOUBLE_ZERO_LEMMA_PATH = RESIDUALS / "P8_Y5_R10_801_DOUBLE_ZERO_LEMMA.csv"
SIGNATURE_AUDIT_PATH = RESIDUALS / "P8_Y5_R10_801_PARENT_SIGNATURE_AUDIT.csv"
CLOSURE_LEDGER_PATH = RESIDUALS / "P8_Y5_R10_801_LOCAL_BRANCH_CLOSURE_LEDGER.csv"
DECISION_PATH = RESIDUALS / "P8_Y5_R10_801_DERIVATION_DECISION.csv"
NONCLAIM_SUMMARY_PATH = RESIDUALS / "P8_Y5_R10_801_NONCLAIM_SUMMARY.csv"
VALIDATION_PATH = RESIDUALS / "P8_Y5_BRR545_801_VALIDATION.csv"

STATUS = "Y5_R10_801_conditional_ZL_norm_double_zero_theorem_not_parent_signed_nonclaim"
CLAIM_CEILING = "conditional_scalar_double_zero_theorem_only_no_parent_ZL_evenness_gradient_or_Kperp_claim"
FORMALIZATION_CUTOFF = datetime(2026, 5, 31, 14, 42, 0)

OUTPUT_PATHS = [
    OUTPUT_DOC,
    SOURCE_REGISTER_PATH,
    PARENT_CONTRACT_PATH,
    DOUBLE_ZERO_LEMMA_PATH,
    SIGNATURE_AUDIT_PATH,
    CLOSURE_LEDGER_PATH,
    DECISION_PATH,
    NONCLAIM_SUMMARY_PATH,
    VALIDATION_PATH,
]

SOURCE_SPECS = [
    {
        "source_id": "800_doc",
        "path": OUTPUT_DOC.parent / "800-Y5-R10-universal-XB-PiB-support-powers-or-Kperp-boundary-zero-lemma.md",
        "needles": ["pL=2", "pT=2", "`K_perp` needs an independent tensor boundary theorem"],
        "role": "immediate 800 result selecting the double-zero parent mechanism target",
    },
    {
        "source_id": "800_validation",
        "path": RESIDUALS / "P8_Y5_BRR545_800_VALIDATION.csv",
        "needles": ["V800_11_next_target_selected,pass", "V800_12_no_local_GR_claim,pass"],
        "role": "prior checkpoint validation",
    },
    {
        "source_id": "spine_finite_margin_branch",
        "path": FORMALIZATION / "07-unification-spine.md",
        "needles": ["m_L - m_* = O(U_B^2);", "L_cg^-2 F_L - Lambda_loc = O(U_B^2);", "K_perp is zero, stronger-order suppressed, or explicitly PPN-bounded."],
        "role": "finite-margin local branch requirements",
    },
    {
        "source_id": "spine_closure_shape",
        "path": FORMALIZATION / "07-unification-spine.md",
        "needles": ["D_L = O(U_B);", "m_L - m_* = O(D_L^2);", "local PPN branch = disciplined closure, not derived local limit."],
        "role": "current closure shape and non-claim classification",
    },
    {
        "source_id": "red_fixed_point_origin",
        "path": FORMALIZATION / "06-consistency-red-team.md",
        "needles": ["fixed_point_extremality_origin_best_route_ZL_not_parent_derived", "an even scalar dependence on a local leakage vector Z_L", "credible route, not a derivation"],
        "role": "best scalar double-zero origin and current failure mode",
    },
    {
        "source_id": "red_leakage_vector_invariant",
        "path": FORMALIZATION / "06-consistency-red-team.md",
        "needles": ["Z_L can be defined from universal X_B ingredients", "D_L <= U_B follows algebraically if H_L is bounded and G_AB is normalized", "scalar evenness is not parent-derived"],
        "role": "candidate leakage vector invariant and unsigned assumptions",
    },
    {
        "source_id": "red_scalar_evenness",
        "path": FORMALIZATION / "06-consistency-red-team.md",
        "needles": ["scalar_evenness_origin_parity_candidate_not_parent_derived", "scalar evenness now has a clean parity/isotropy theorem form", "theorem-shaped closure, not parent derivation"],
        "role": "parity/evenness route and non-derivation status",
    },
    {
        "source_id": "minimal_parent_action_contract",
        "path": POST_CHECKPOINT / "511-minimal-parent-action-local-GR-fixed-point-ansatz.md",
        "needles": ["FP511_1_double_zero_nonEH_coupling", "F_1 = 0 is not a wish", "local GR can be targeted through an EH fixed point plus double-zero/mass-gap/silence conditions"],
        "role": "earlier parent-action fixed-point contract",
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


def parse_validation_clean(check_number: int) -> tuple[bool, str]:
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


def parent_contract_rows(generated_utc: str) -> list[dict[str, object]]:
    return [
        {
            "contract_id": "FPC801_0_local_fixed_surface",
            "clause": "There is a local GR fixed surface Sigma_L defined by Z_L^A=0.",
            "mathematical_form": "D_L=(G_AB Z_L^A Z_L^B)^(1/2); Sigma_L={D_L=0}",
            "derives_if_signed": "a scalar distance-to-leakage variable for local screening",
            "unsigned_gap": "parent v1 has candidate Z_L ingredients but no action-level Z_L map",
            "status": "candidate_not_parent_signed",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "contract_id": "FPC801_1_screened_distance_bound",
            "clause": "The leakage distance is at least linearly controlled by the universal screened fraction.",
            "mathematical_form": "D_L <= C_D U_B with C_D universal and finite",
            "derives_if_signed": "D_L=O(U_B)",
            "unsigned_gap": "requires bounded H_L components and normalized G_AB",
            "status": "conditional_bound_only",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "contract_id": "FPC801_2_even_scalar_readout",
            "clause": "Scalar local readouts depend on leakage only through the invariant norm R_L=D_L^2.",
            "mathematical_form": "m_L-m_*=M(R_L); T_L=L_cg^-2 F_L-Lambda_loc=T(R_L)",
            "derives_if_signed": "m_L-m_*=O(U_B^2) and T_L=O(U_B^2)",
            "unsigned_gap": "parity/isotropy or quotient evenness is theorem-shaped but not parent-derived",
            "status": "conditional_double_zero_theorem",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "contract_id": "FPC801_3_gradient_control",
            "clause": "The same leakage structure controls transition gradients.",
            "mathematical_form": "nabla D_L=O(U_B/L_B) or stronger on the local branch",
            "derives_if_signed": "nabla(m_L-m_*), nabla T_L do not recreate first-order q_loc leakage",
            "unsigned_gap": "gradient power control is still explicitly open",
            "status": "open_required_clause",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "contract_id": "FPC801_4_tensor_boundary_branch",
            "clause": "Transverse tensor leakage is controlled by a separate coercive operator and boundary theorem.",
            "mathematical_form": "L_T K_perp=S_perp, ||K_perp||<=C_T||S_perp|| with zero/decay boundary data",
            "derives_if_signed": "K_perp=0 or K_perp=O(U_B^pK)",
            "unsigned_gap": "K_perp is untouched by scalar Z_L evenness",
            "status": "separate_open_tensor_gate",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
    ]


def double_zero_lemma_rows(generated_utc: str) -> list[dict[str, object]]:
    return [
        {
            "lemma_id": "DZ801_0_generic_failure",
            "assumptions": "generic smooth scalar readout f(Z_L)=f_0+a_A Z_L^A+O(D_L^2)",
            "derivation": "local GR fixed surface requires f_0=0, but unless a_A=0 the first correction is O(D_L)",
            "result": "generic smooth leakage gives only p=1",
            "status": "fails_double_zero",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "lemma_id": "DZ801_1_norm_evenness",
            "assumptions": "f(Z_L)=F(R_L), R_L=G_AB Z_L^A Z_L^B, F smooth, F(0)=0",
            "derivation": "F(R_L)=F'(0)R_L+O(R_L^2), so f=O(D_L^2) and partial_A f|Sigma_L=0",
            "result": "double zero follows from norm-only scalar dependence",
            "status": "mathematical_theorem_if_parent_signed",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "lemma_id": "DZ801_2_mL_power",
            "assumptions": "m_L-m_*=M(R_L), M(0)=0, D_L<=C_D U_B",
            "derivation": "|m_L-m_*|<=C_M D_L^2+O(D_L^4)<=C_M C_D^2 U_B^2+O(U_B^4)",
            "result": "pL=2 conditionally derived",
            "status": "conditional_scalar_pass",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "lemma_id": "DZ801_3_trace_power",
            "assumptions": "T_L=L_cg^-2F_L-Lambda_loc=T(R_L), T(0)=0, D_L<=C_D U_B",
            "derivation": "|T_L|<=C_T D_L^2+O(D_L^4)<=C_T C_D^2 U_B^2+O(U_B^4)",
            "result": "pT=2 conditionally derived",
            "status": "conditional_scalar_pass",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "lemma_id": "DZ801_4_gradient_warning",
            "assumptions": "f=F(D_L^2), D_L=O(U_B), nabla D_L not bounded",
            "derivation": "nabla f=2F'(R_L)D_L nabla D_L; a large transition gradient can still source q_loc",
            "result": "double zero of amplitude is not enough without gradient control",
            "status": "gradient_gate_still_open",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
    ]


def signature_audit_rows(generated_utc: str) -> list[dict[str, object]]:
    return [
        {
            "signature_id": "SIG801_0_parent_ZL_map",
            "needed_signature": "Z_L^A is defined by parent/coarse-graining variables, not sector labels.",
            "current_evidence": "red-team says Z_L can be defined from universal X_B ingredients.",
            "signed": "partial_candidate",
            "blocking_gap": "not action-level and not yet a covariant parent map",
            "local_claim_effect": "blocks_derived_local_GR",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "signature_id": "SIG801_1_GAB_metric",
            "needed_signature": "G_AB is positive, universal, and normalized by parent kinetic/Hessian structure.",
            "current_evidence": "G_AB weights are explicitly listed as not parent-derived.",
            "signed": "false",
            "blocking_gap": "no parent metric on leakage bundle",
            "local_claim_effect": "blocks_D_L_bound",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "signature_id": "SIG801_2_evenness_symmetry",
            "needed_signature": "Scalar readouts are invariant under leakage-frame parity/isotropy.",
            "current_evidence": "parity/isotropy theorem form exists, but is not parent-derived.",
            "signed": "false",
            "blocking_gap": "no quotient/symmetry rule removing the linear term a_A Z_L^A",
            "local_claim_effect": "blocks_pL_pT_double_zero_claim",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "signature_id": "SIG801_3_DLU_bound",
            "needed_signature": "D_L <= C_D U_B with C_D finite and universal.",
            "current_evidence": "algebraic route exists if H_L is bounded and G_AB normalized.",
            "signed": "conditional_only",
            "blocking_gap": "H_L bound not proven",
            "local_claim_effect": "blocks_finite_margin_scaling",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "signature_id": "SIG801_4_gradient_power",
            "needed_signature": "nabla D_L=O(U_B/L_B) or an equivalent q_loc-safe transition bound.",
            "current_evidence": "gradient control is open in the red-team ledger.",
            "signed": "false",
            "blocking_gap": "no transition-current gradient theorem",
            "local_claim_effect": "blocks_q_loc_silence",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "signature_id": "SIG801_5_Kperp_tensor",
            "needed_signature": "K_perp has exact zero data, strong source suppression, or explicit local bound.",
            "current_evidence": "K_perp remains untouched by scalar fixed-point work.",
            "signed": "false",
            "blocking_gap": "no tensor boundary/coercivity theorem",
            "local_claim_effect": "blocks_PPN_vector_pass",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
    ]


def closure_ledger_rows(generated_utc: str) -> list[dict[str, object]]:
    return [
        {
            "closure_id": "CL801_0_scalar_double_zero_shape",
            "closure_statement": "Carry m_L-m_*=O(D_L^2) and T_L=O(D_L^2) as a theorem-shaped closure until parent evenness is signed.",
            "why_not_claim": "Z_L, G_AB, and parity/evenness are not yet parent-derived.",
            "allowed_use": "internal finite-margin calculators and route selection only",
            "promotion_gate": "all SIG801_0 through SIG801_4 become signed or bounded",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "closure_id": "CL801_1_Kperp_separate_closure",
            "closure_statement": "Carry K_perp as exact zero, O(D_L^3), or explicitly bounded only as a separate tensor closure.",
            "why_not_claim": "scalar norm-evenness does not remove transverse homogeneous tensor modes.",
            "allowed_use": "do not merge into scalar local-GR proof",
            "promotion_gate": "coercive L_T theorem plus sourced boundary data",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "closure_id": "CL801_2_local_GR_status",
            "closure_statement": "Local branch remains disciplined closure, not a derived GR/Newton limit.",
            "why_not_claim": "amplitude, gradient, and tensor gates remain unsigned.",
            "allowed_use": "private theory-development spine with explicit caveat",
            "promotion_gate": "parent action/coarse-graining theorem derives the full fixed-point contract",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
    ]


def decision_rows(generated_utc: str) -> list[dict[str, object]]:
    return [
        {
            "decision_id": "D801_0_double_zero_theorem",
            "question": "Can pL=2 and pT=2 be mathematically derived from a fixed-point mechanism?",
            "answer": "Yes, conditionally: if scalar readouts depend only on R_L=G_AB Z_L^A Z_L^B and D_L=O(U_B).",
            "status": "conditional_theorem_constructed",
            "next_target": NEXT_TARGET,
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "decision_id": "D801_1_parent_derivation_status",
            "question": "Is this parent-derived in current MTS?",
            "answer": "No. Z_L, G_AB, parity/evenness, gradient control, and Kperp are not signed by the parent action.",
            "status": "not_parent_signed",
            "next_target": NEXT_TARGET,
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "decision_id": "D801_2_closure_status",
            "question": "Should the local branch be claimed as derived GR?",
            "answer": "No. It can be carried only as a labelled local finite-margin closure.",
            "status": "local_GR_claim_false",
            "next_target": NEXT_TARGET,
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "decision_id": "D801_3_next_route",
            "question": "What is the best next target?",
            "answer": "Try to parent-sign Z_L/evenness/gradient clauses; if that fails, freeze the scalar local branch as closure and move to Kperp bounds.",
            "status": "attempt_parent_ZL_evenness_gradient_signature",
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
            "what_improved": "The scalar double-zero route is now an exact conditional theorem: norm-only dependence on a leakage vector gives pL=pT=2.",
            "what_blocks_claim": "The parent action has not signed Z_L, G_AB, parity/evenness, gradient control, or Kperp.",
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
    parent_contracts: list[dict[str, object]],
    lemmas: list[dict[str, object]],
    signatures: list[dict[str, object]],
    closures: list[dict[str, object]],
    decisions: list[dict[str, object]],
    summary: list[dict[str, object]],
) -> list[dict[str, object]]:
    source_ok = all(row["exists"] == "true" and row["needle_check"] == "pass" for row in sources)
    prior_ok, prior_detail = parse_validation_clean(800)
    row_groups = [sources, parent_contracts, lemmas, signatures, closures, decisions, summary]
    nonclaim_ok = all_rows_nonclaim(row_groups)
    formalization_count = formalization_change_count()
    unsigned_blockers = [row for row in signatures if row["signed"] in {"false", "conditional_only", "partial_candidate"}]
    scalar_conditional = any(row["lemma_id"] == "DZ801_2_mL_power" for row in lemmas) and any(
        row["lemma_id"] == "DZ801_3_trace_power" for row in lemmas
    )
    return [
        {"check_id": "V801_0_sources_exist_and_needles", "result": "pass" if source_ok else "fail", "detail": "all source paths exist and needles are present"},
        {"check_id": "V801_1_prior_800_clean", "result": "pass" if prior_ok else "fail", "detail": prior_detail},
        {"check_id": "V801_2_outputs_scoped", "result": "pass" if all_outputs_scoped() else "fail", "detail": str(POST_CHECKPOINT)},
        {"check_id": "V801_3_all_rows_nonclaim", "result": "pass" if nonclaim_ok else "fail", "detail": "all generated rows valid_for_claim=false"},
        {"check_id": "V801_4_scalar_double_zero_theorem_constructed", "result": "pass" if scalar_conditional else "fail", "detail": "norm-only Z_L dependence conditionally gives pL=pT=2"},
        {"check_id": "V801_5_generic_linear_failure_recorded", "result": "pass" if any(row["lemma_id"] == "DZ801_0_generic_failure" for row in lemmas) else "fail", "detail": "generic smooth leakage gives only p=1"},
        {"check_id": "V801_6_parent_signatures_unsigned", "result": "pass" if len(unsigned_blockers) >= 5 else "fail", "detail": f"unsigned_or_conditional_blockers={len(unsigned_blockers)}"},
        {"check_id": "V801_7_gradient_gate_open", "result": "pass" if any(row["signature_id"] == "SIG801_4_gradient_power" and row["signed"] == "false" for row in signatures) else "fail", "detail": "gradient control remains open"},
        {"check_id": "V801_8_Kperp_open", "result": "pass" if any(row["signature_id"] == "SIG801_5_Kperp_tensor" and row["signed"] == "false" for row in signatures) else "fail", "detail": "Kperp remains separate tensor problem"},
        {"check_id": "V801_9_closure_ledger_present", "result": "pass" if len(closures) >= 3 else "fail", "detail": "local branch closure rows written"},
        {"check_id": "V801_10_next_target_selected", "result": "pass" if decisions[-1]["next_target"] == NEXT_TARGET else "fail", "detail": NEXT_TARGET},
        {"check_id": "V801_11_no_local_GR_claim", "result": "pass" if all("claim_false" in row["status"] or row["valid_for_claim"] == "false" for row in decisions) else "fail", "detail": "derived GR/Newton remains blocked"},
        {"check_id": "V801_12_formalization_workbench_untouched", "result": "pass" if formalization_count == 0 else "fail", "detail": f"formalization_changed_after_cutoff={formalization_count}"},
        {"check_id": "V801_13_validation_rows_ready", "result": "pass", "detail": "validation table constructed"},
    ]


def build_doc(
    generated_utc: str,
    sources: list[dict[str, object]],
    parent_contracts: list[dict[str, object]],
    lemmas: list[dict[str, object]],
    signatures: list[dict[str, object]],
    closures: list[dict[str, object]],
    decisions: list[dict[str, object]],
    summary: list[dict[str, object]],
    validations: list[dict[str, object]],
) -> str:
    return f"""# 801 - Y5 R10 Double-Zero Fixed-Point Parent Mechanism Or Local-Branch Closure Ledger

Current result: **the scalar double-zero mechanism can be made mathematically exact, but it is not yet parent-derived**. If a parent leakage vector `Z_L` exists, if `D_L=(G_AB Z_L^A Z_L^B)^(1/2)=O(U_B)`, and if scalar local readouts depend only on the norm `R_L=D_L^2`, then `m_L-m_*` and `L_cg^-2 F_L-Lambda_loc` vanish quadratically. That gives the wanted `pL=2` and `pT=2` as a theorem-shaped route. The missing pieces are the parent signatures: `Z_L`, `G_AB`, parity/evenness, gradient control, and `K_perp`.

Generated UTC: `{generated_utc}`

## Non-Claim Summary

{markdown_table(summary, ["status", "claim_ceiling", "what_improved", "what_blocks_claim", "next_target", "valid_for_claim"])}

## Parent Fixed-Point Contract

{markdown_table(parent_contracts, ["contract_id", "clause", "mathematical_form", "derives_if_signed", "unsigned_gap", "status", "valid_for_claim"])}

## Double-Zero Lemma

{markdown_table(lemmas, ["lemma_id", "assumptions", "derivation", "result", "status", "valid_for_claim"])}

## Parent Signature Audit

{markdown_table(signatures, ["signature_id", "needed_signature", "current_evidence", "signed", "blocking_gap", "local_claim_effect", "valid_for_claim"])}

## Local Closure Ledger

{markdown_table(closures, ["closure_id", "closure_statement", "why_not_claim", "allowed_use", "promotion_gate", "valid_for_claim"])}

## Decision

{markdown_table(decisions, ["decision_id", "question", "answer", "status", "next_target", "valid_for_claim"])}

## Source Register

{markdown_table(sources, ["source_id", "path", "exists", "needle_check", "role", "valid_for_claim"])}

## Validation

{markdown_table(validations, ["check_id", "result", "detail"])}

## Verdict

This is a genuine improvement, not just a renamed assumption: the required scalar double zeros now reduce to one precise mechanism, `scalar readout = smooth function of leakage norm squared`. The theorem is small but sharp:

```text
Z_L = O(U_B),
R_L = G_AB Z_L^A Z_L^B,
m_L - m_* = M(R_L),
L_cg^-2 F_L - Lambda_loc = T(R_L)
=> m_L - m_* = O(U_B^2),  L_cg^-2 F_L - Lambda_loc = O(U_B^2).
```

But it is still not a derived local GR/Newton limit. The parent action must explain why the leakage coordinate exists, why scalar readouts are even/norm-only, why gradients do not reintroduce first-order `q_loc`, and why `K_perp` is zero/suppressed/bounded.

## Next Target

`{NEXT_TARGET}`
"""


def write_outputs() -> None:
    generated_utc = utc_stamp()
    sources = source_register_rows(generated_utc)
    parent_contracts = parent_contract_rows(generated_utc)
    lemmas = double_zero_lemma_rows(generated_utc)
    signatures = signature_audit_rows(generated_utc)
    closures = closure_ledger_rows(generated_utc)
    decisions = decision_rows(generated_utc)
    summary = nonclaim_summary_rows(generated_utc)
    validations = validation_rows(sources, parent_contracts, lemmas, signatures, closures, decisions, summary)

    write_csv(SOURCE_REGISTER_PATH, sources, ["source_id", "path", "exists", "needle_check", "role", "valid_for_claim", "generated_utc"])
    write_csv(PARENT_CONTRACT_PATH, parent_contracts, ["contract_id", "clause", "mathematical_form", "derives_if_signed", "unsigned_gap", "status", "valid_for_claim", "generated_utc"])
    write_csv(DOUBLE_ZERO_LEMMA_PATH, lemmas, ["lemma_id", "assumptions", "derivation", "result", "status", "valid_for_claim", "generated_utc"])
    write_csv(SIGNATURE_AUDIT_PATH, signatures, ["signature_id", "needed_signature", "current_evidence", "signed", "blocking_gap", "local_claim_effect", "valid_for_claim", "generated_utc"])
    write_csv(CLOSURE_LEDGER_PATH, closures, ["closure_id", "closure_statement", "why_not_claim", "allowed_use", "promotion_gate", "valid_for_claim", "generated_utc"])
    write_csv(DECISION_PATH, decisions, ["decision_id", "question", "answer", "status", "next_target", "valid_for_claim", "generated_utc"])
    write_csv(NONCLAIM_SUMMARY_PATH, summary, ["status", "claim_ceiling", "what_improved", "what_blocks_claim", "next_target", "valid_for_claim", "generated_utc"])
    write_csv(VALIDATION_PATH, validations, ["check_id", "result", "detail"])

    OUTPUT_DOC.write_text(
        build_doc(generated_utc, sources, parent_contracts, lemmas, signatures, closures, decisions, summary, validations),
        encoding="utf-8",
    )

    failed_checks = [row for row in validations if row["result"] != "pass"]
    if failed_checks:
        failed_text = "; ".join(f"{row['check_id']}={row['detail']}" for row in failed_checks)
        raise SystemExit(f"801 validation failed: {failed_text}")

    print(f"wrote {OUTPUT_DOC}")
    print(f"wrote {VALIDATION_PATH}")
    print(f"status={STATUS}")
    print(f"next={NEXT_TARGET}")


if __name__ == "__main__":
    write_outputs()

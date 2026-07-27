from __future__ import annotations

import csv
import math
import subprocess
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(r"D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main")
POST_CHECKPOINT = ROOT / "post-checkpoint-work"
FORMALIZATION = ROOT / "formalization-workbench"
RESIDUALS = POST_CHECKPOINT / "source-intake" / "mts_residuals"

OUTPUT_DOC = POST_CHECKPOINT / "831-Y5-R10-parent-Khat-tensor-operator-or-local-branch-closure.md"
SOURCE_REGISTER_PATH = RESIDUALS / "P8_Y5_R10_831_SOURCE_REGISTER.csv"
OPERATOR_CONTRACT_PATH = RESIDUALS / "P8_Y5_R10_831_OPERATOR_CONTRACT.csv"
RANGE_THEOREM_PATH = RESIDUALS / "P8_Y5_R10_831_RANGE_COKERNEL_THEOREM.csv"
PARENT_ADOPTION_PATH = RESIDUALS / "P8_Y5_R10_831_PARENT_ADOPTION_AUDIT.csv"
RUNNER_INPUT_PATH = RESIDUALS / "P8_Y5_R10_831_RANGE_RUNNER_INPUT_TEMPLATE.csv"
RUNNER_OUTPUT_PATH = RESIDUALS / "P8_Y5_R10_831_RANGE_RUNNER_OUTPUT.csv"
DEMOTION_GATE_PATH = RESIDUALS / "P8_Y5_R10_831_DEMOTION_GATE.csv"
DECISION_PATH = RESIDUALS / "P8_Y5_R10_831_DECISION.csv"
NEXT_TARGET_PATH = RESIDUALS / "P8_Y5_R10_831_NEXT_TARGET.csv"
NONCLAIM_SUMMARY_PATH = RESIDUALS / "P8_Y5_R10_831_NONCLAIM_SUMMARY.csv"
VALIDATION_PATH = RESIDUALS / "P8_Y5_BRR545_831_VALIDATION.csv"

STATUS = "Y5_R10_831_tracefree_divergence_range_contract_derived_parent_operator_not_signed_nonclaim"
CLAIM_CEILING = "operator_contract_and_range_cokernel_theorem_only_no_adopted_Khat_owner_no_local_GR_pass"
NEXT_TARGET = "832-Y5-R10-tracefree-divergence-range-theorem-or-cokernel-bound.md"

SOURCE_SPECS = [
    {
        "source_id": "830_doc",
        "path": POST_CHECKPOINT / "830-Y5-R10-Khat-boundary-owner-or-residual-vector-runner.md",
        "needles": [
            "KO830_0_parent_tensor_operator",
            "KO830_5_verdict",
            "831-Y5-R10-parent-Khat-tensor-operator-or-local-branch-closure.md",
        ],
        "role": "immediate Khat owner handoff",
    },
    {
        "source_id": "830_validation",
        "path": RESIDUALS / "P8_Y5_BRR545_830_VALIDATION.csv",
        "needles": [
            "V830_2_khat_owner_not_derived,pass",
            "V830_8_next_target_selected,pass",
            "V830_9_formalization_workbench_untouched,pass",
        ],
        "role": "prior checkpoint validation",
    },
    {
        "source_id": "795_parent_origin",
        "path": POST_CHECKPOINT / "795-Y5-R10-parent-origin-of-tracefree-Khat-solver-or-amplitude-bound.md",
        "needles": [
            "POA795_1_relaxation_source",
            "KAB795_2_PPN_vector",
            "parent_origin_missing",
        ],
        "role": "trace-free Khat solver origin and amplitude warning",
    },
    {
        "source_id": "794_tracefree_solver",
        "path": POST_CHECKPOINT / "794-Y5-R10-tracefree-longitudinal-Khat-solver-or-PPN-bound.md",
        "needles": [
            "V794_5_flat_cancel",
            "V794_8_solver_not_adopted",
            "trace-free condition does not kill the cancellation route",
        ],
        "role": "flat/local trace-free divergence cancellation clue",
    },
    {
        "source_id": "756_metric_response",
        "path": POST_CHECKPOINT / "756-Y5-R10-Gamma-Khat-metric-response-symbol-match-or-q_loc-component-candidate-builder.md",
        "needles": [
            "MRM756_0_variational_contract",
            "RDR756_0_response_doublet_parent_action",
            "metric_response_symbol_match_not_accepted",
        ],
        "role": "metric-response and response-doublet obstruction",
    },
    {
        "source_id": "515_metric_response_audit",
        "path": POST_CHECKPOINT / "515-match-Gamma-eff-Khat-to-metric-response-action.md",
        "needles": [
            "MA515_1_Khat_metric_response",
            "RO515_C_response_displacement_pair",
            "q_loc_zero_false",
        ],
        "role": "older Gamma/Khat metric-response audit",
    },
    {
        "source_id": "513_first_variation",
        "path": POST_CHECKPOINT / "513-Gamma-Khat-q_loc-first-variation-or-demotion.md",
        "needles": [
            "GK513_0_action_existence",
            "IG513_2_metric_variationality",
            "QR513_0_nonvariational_stress",
        ],
        "role": "first-variation and Hilbert-stress contract",
    },
    {
        "source_id": "equation_register_Khat",
        "path": FORMALIZATION / "05-equation-register.md",
        "needles": [
            "`K_MTS = P_MTS[psi,Gamma_mem,matter,g,L_cg]` is still a closure target",
            "q^nu = nabla^nu Gamma_eff - nabla_mu K_hat",
            "The real Solar branch remains open until `q_loc(x)`, boundary data, and amplitude bounds are supplied.",
        ],
        "role": "formal equation register warning for Khat/q_loc",
    },
    {
        "source_id": "spine_Khat",
        "path": FORMALIZATION / "07-unification-spine.md",
        "needles": [
            "L_T K_perp = 0",
            "K_perp source and boundary data vanish with enough order under a coercive local tensor operator.",
            "parent v1 does not derive exact K_hat cancellation",
        ],
        "role": "spine-level tensor operator target and open theorem warning",
    },
]

REQUIRED_NUMERIC_FIELDS = [
    "G_norm",
    "cokernel_fraction",
    "boundary_obstruction_norm",
    "regularizer_norm",
    "coercivity_inverse",
    "kappa_K",
    "observable_response_norm",
    "observable_limit",
]
REQUIRED_SOURCE_FIELDS = [
    "range_theorem_source_path",
    "boundary_condition_source_path",
    "parent_action_source_path",
    "observable_response_source_path",
]


def write_csv(path: Path, rows: list[dict[str, object]], fieldnames: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)


def read_text(path: Path) -> str:
    if not path.exists():
        return ""
    return path.read_text(encoding="utf-8", errors="replace")


def check_needles(path: Path, needles: list[str]) -> str:
    text = read_text(path)
    if not text:
        return "missing_path"
    missing = [needle for needle in needles if needle not in text]
    if missing:
        return "missing_needles:" + ";".join(missing)
    return "pass"


def validation_file_clean(path: Path) -> tuple[bool, str]:
    if not path.exists():
        return False, f"missing={path}"
    failures: list[str] = []
    with path.open("r", encoding="utf-8", newline="") as handle:
        for row in csv.DictReader(handle):
            if row.get("result") != "pass":
                failures.append(f"{row.get('check_id')}={row.get('result')}")
    if failures:
        return False, ";".join(failures)
    return True, f"{path.name} clean"


def formalization_workbench_modified_count() -> int:
    command = (
        "$fw='"
        + str(FORMALIZATION).replace("'", "''")
        + "'; "
        + "$cutoff=[datetime]'2026-05-31T14:42:00'; "
        + "(Get-ChildItem -LiteralPath $fw -Recurse -File | "
        + "Where-Object { $_.LastWriteTime -gt $cutoff }).Count"
    )
    completed = subprocess.run(
        ["powershell", "-NoProfile", "-Command", command],
        check=True,
        capture_output=True,
        text=True,
        timeout=20,
    )
    return int(completed.stdout.strip() or "0")


def source_register_rows(generated_utc: str) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    for spec in SOURCE_SPECS:
        path = spec["path"]
        rows.append(
            {
                "source_id": spec["source_id"],
                "path": str(path),
                "exists": str(path.exists()).lower(),
                "needle_check": check_needles(path, spec["needles"]),
                "role": spec["role"],
                "valid_for_claim": "false",
                "generated_utc": generated_utc,
            }
        )
    return rows


def operator_contract_rows(generated_utc: str) -> list[dict[str, object]]:
    return [
        {
            "contract_id": "OC831_0_domain",
            "object": "trace-free symmetric tensor bundle",
            "equation_or_condition": "K_hat in Gamma(S^2_0 T*Omega_loc); tr_g K_hat=0; D_T K_hat := P_loc nabla_mu K_hat^{mu nu}",
            "derivation_status": "defined_as_contract",
            "what_it_proves": "identifies the exact operator whose range controls q_loc suppression",
            "what_remains_open": "parent action must actually contain this bundle/readout",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "contract_id": "OC831_1_balance_action",
            "object": "minimal Khat balance functional",
            "equation_or_condition": "S_bal=(2 kappa_K)^-1 ||D_T K_hat - G||^2 + S_reg[K_hat] + B, with G^nu=P_loc nabla^nu Gamma_eff",
            "derivation_status": "new_minimal_contract_not_found_in_corpus",
            "what_it_proves": "turns q_loc suppression into a variational problem rather than a plateau axiom",
            "what_remains_open": "MTS parent action must supply S_bal or an equivalent block",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "contract_id": "OC831_2_first_variation",
            "object": "Euler equation for Khat",
            "equation_or_condition": "delta S_bal/delta K_hat = kappa_K^-1 D_T^dagger(D_T K_hat-G)+E_reg+B_K = 0",
            "derivation_status": "derived_from_contract",
            "what_it_proves": "the owner equation is an adjoint-range condition, not simply div K_hat=grad Gamma_eff",
            "what_remains_open": "boundary term B_K and regularizer E_reg must be signed by parent dynamics",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "contract_id": "OC831_3_exact_zero_condition",
            "object": "local residual",
            "equation_or_condition": "r:=G-D_T K_hat; if E_reg=0, B_K=0, and G in Range(D_T), then r=P_coker(D_T)G=0",
            "derivation_status": "derived_range_cokernel_condition",
            "what_it_proves": "the exact q_loc zero condition is a range theorem plus boundary compatibility",
            "what_remains_open": "prove G is in Range(D_T) for the physical local branch",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "contract_id": "OC831_4_bound_condition",
            "object": "nonzero residual bound",
            "equation_or_condition": "||r|| <= ||P_coker(D_T)G|| + ||b_boundary|| + kappa_K C_T ||E_reg||",
            "derivation_status": "derived_contract_bound",
            "what_it_proves": "if exact zero fails, the residual budget has a concrete norm-bound form",
            "what_remains_open": "source-backed C_T, boundary norm, regularizer norm, and response matrices",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "contract_id": "OC831_5_observable_acceptance",
            "object": "local tests",
            "equation_or_condition": "Khat owner pass requires q_residual, Khat amplitude, PPN/R10/clock/orbital/WEP response, and matter descent all below sourced bounds",
            "derivation_status": "acceptance_gate",
            "what_it_proves": "q_loc algebra alone is insufficient for local GR",
            "what_remains_open": "all arena response matrices and matter descent",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
    ]


def range_theorem_rows(generated_utc: str) -> list[dict[str, object]]:
    return [
        {
            "theorem_id": "RT831_0_operator",
            "statement": "Define D_T: K_hat -> P_loc nabla_mu K_hat^{mu nu} on trace-free symmetric tensors over the local domain.",
            "proof_step": "This is the divergence map that appears in q_loc^nu=P_loc(nabla^nu Gamma_eff-nabla_mu K_hat^{mu nu}).",
            "result": "operator_identified",
            "failure_mode": "wrong tensor bundle or projector variation changes D_T",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "theorem_id": "RT831_1_projection_law",
            "statement": "For the quadratic balance functional, the minimizer residual is the orthogonal projection of G onto Coker(D_T), up to regularizer and boundary terms.",
            "proof_step": "Euler gives D_T^dagger r=0; therefore r is orthogonal to Range(D_T), while G-r lies in Range(D_T).",
            "result": "r_star=P_coker(D_T)G_when_Ereg_and_boundary_zero",
            "failure_mode": "non-natural boundary, non-closed range, or hidden metric/projector variation",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "theorem_id": "RT831_2_exact_zero",
            "statement": "Exact local q suppression follows iff P_coker(D_T)G=0 and no boundary/regularizer obstruction is active.",
            "proof_step": "If G is in Range(D_T), choose K_hat with D_T K_hat=G; the positive norm action has zero minimum.",
            "result": "q_loc_zero_reduced_to_range_and_boundary_theorem",
            "failure_mode": "G has a harmonic/cokernel component or source-measure boundary charge",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "theorem_id": "RT831_3_bound",
            "statement": "If exact zero fails, the physical residual is bounded by cokernel, boundary, and regularizer terms.",
            "proof_step": "Use coercivity/inverse bound C_T for D_T^dagger D_T on the controlled subspace.",
            "result": "||q_loc|| <= ||P_coker G|| + ||b_boundary|| + kappa_K C_T ||E_reg||",
            "failure_mode": "no coercivity/no-zero-mode theorem means no quantitative local test pass",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "theorem_id": "RT831_4_tracefree_link",
            "statement": "The earlier flat trace-free solver is reinterpreted as evidence that Range(D_T) can contain gradient-like sources locally.",
            "proof_step": "794 showed trace-free status does not by itself kill the cancellation candidate.",
            "result": "promising_math_not_parent_adoption",
            "failure_mode": "curved-domain, boundary, amplitude, and parent-origin clauses still fail",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
    ]


def parent_adoption_rows(generated_utc: str) -> list[dict[str, object]]:
    return [
        {
            "audit_id": "PA831_0_parent_action_block",
            "required_evidence": "MTS parent action contains S_bal or an equivalent variational Khat operator",
            "current_evidence": "830 and 795 say parent Khat operator/origin remains unsigned",
            "status": "not_found",
            "effect": "operator contract cannot be adopted as parent-derived",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "audit_id": "PA831_1_metric_response_match",
            "required_evidence": "Gamma_eff is action-owned and K_hat is the full Hilbert/metric response or conjugate response field",
            "current_evidence": "515 and 756 fail the current metric-response symbol match",
            "status": "not_found",
            "effect": "q_loc zero cannot be promoted through Ward identity",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "audit_id": "PA831_2_range_theorem",
            "required_evidence": "G=P_loc grad Gamma_eff lies in Range(D_T) for the physical local domain and boundary conditions",
            "current_evidence": "794 gives only a local/flat formal clue; no physical range theorem exists",
            "status": "missing_theorem",
            "effect": "cokernel residual may remain physical",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "audit_id": "PA831_3_boundary_no_flux",
            "required_evidence": "boundary/source-measure term b_boundary vanishes or is quantitatively bounded",
            "current_evidence": "829 and 830 keep boundary/local projection silence open",
            "status": "missing_boundary_theorem",
            "effect": "bulk range cancellation can still leak at boundaries",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "audit_id": "PA831_4_amplitude_and_response",
            "required_evidence": "Khat carrier amplitude and arena response vector are below PPN/R10/clock/orbital/WEP limits",
            "current_evidence": "795 and 830 mark amplitude/response matrices missing",
            "status": "missing_response_matrices",
            "effect": "even exact q_loc algebra would not yet prove local GR",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "audit_id": "PA831_5_verdict",
            "required_evidence": "all parent action, range, boundary, matter, and response clauses close",
            "current_evidence": "multiple required clauses are still missing",
            "status": "not_adopted_closure_only_for_current_corpus",
            "effect": "831 is a derivation contract and mathematical reduction, not a local-GR pass",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
    ]


def runner_input_rows(generated_utc: str) -> list[dict[str, object]]:
    return [
        {
            "row_id": "template_missing_range_inputs",
            "row_status": "blocked_missing_parent_inputs",
            "G_norm": "MISSING_PARENT_INPUT",
            "cokernel_fraction": "MISSING_RANGE_THEOREM",
            "boundary_obstruction_norm": "MISSING_BOUNDARY_INPUT",
            "regularizer_norm": "MISSING_PARENT_INPUT",
            "coercivity_inverse": "MISSING_OPERATOR_BOUND",
            "kappa_K": "MISSING_PARENT_INPUT",
            "observable_response_norm": "MISSING_ARENA_PROJECTION",
            "observable_limit": "MISSING_ARENA_BOUND",
            "range_theorem_source_path": "MISSING_SOURCE_PATH",
            "boundary_condition_source_path": "MISSING_SOURCE_PATH",
            "parent_action_source_path": "MISSING_SOURCE_PATH",
            "observable_response_source_path": "MISSING_SOURCE_PATH",
            "numeric_ready": "false",
            "valid_for_claim": "false",
            "notes": "a claim row needs sourced range/cokernel theorem, boundary condition, parent action block, and observable response",
            "generated_utc": generated_utc,
        }
    ]


def is_missing(value: object) -> bool:
    text = str(value).strip()
    if text == "":
        return True
    upper = text.upper()
    return "MISSING" in upper or upper in {"UNSOURCED", "NONE", "N/A"}


def as_float(value: object) -> float | None:
    if is_missing(value):
        return None
    try:
        parsed = float(str(value))
    except ValueError:
        return None
    if not math.isfinite(parsed):
        return None
    return parsed


def run_range_row(row: dict[str, object], generated_utc: str) -> dict[str, object]:
    missing_numeric = [field for field in REQUIRED_NUMERIC_FIELDS if as_float(row.get(field)) is None]
    missing_sources = [field for field in REQUIRED_SOURCE_FIELDS if is_missing(row.get(field))]
    missing = missing_numeric + missing_sources
    valid_for_claim = str(row.get("valid_for_claim")).lower() == "true"

    if missing:
        return {
            "row_id": row["row_id"],
            "runner_status": "blocked_missing_inputs",
            "q_cokernel_bound": "MISSING_INPUT",
            "q_boundary_bound": "MISSING_INPUT",
            "q_regularizer_bound": "MISSING_INPUT",
            "q_total_bound": "MISSING_INPUT",
            "observable_bound": "MISSING_INPUT",
            "passes_all": "false",
            "block_reason": "missing_fields:" + ";".join(missing),
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        }

    values = {field: as_float(row[field]) for field in REQUIRED_NUMERIC_FIELDS}
    assert all(value is not None for value in values.values())
    q_cokernel = values["cokernel_fraction"] * values["G_norm"]
    q_boundary = values["boundary_obstruction_norm"]
    q_regularizer = values["kappa_K"] * values["coercivity_inverse"] * values["regularizer_norm"]
    q_total = q_cokernel + q_boundary + q_regularizer
    observable_bound = values["observable_response_norm"] * q_total
    passes = valid_for_claim and observable_bound <= values["observable_limit"]
    block_reason = "none" if passes else ("row_valid_for_claim_false" if not valid_for_claim else "observable_bound_exceeds_or_unvalidated")

    return {
        "row_id": row["row_id"],
        "runner_status": "computed_nonclaim" if not valid_for_claim else "computed",
        "q_cokernel_bound": f"{q_cokernel:.16e}",
        "q_boundary_bound": f"{q_boundary:.16e}",
        "q_regularizer_bound": f"{q_regularizer:.16e}",
        "q_total_bound": f"{q_total:.16e}",
        "observable_bound": f"{observable_bound:.16e}",
        "passes_all": str(passes).lower(),
        "block_reason": block_reason,
        "valid_for_claim": "false",
        "generated_utc": generated_utc,
    }


def demotion_gate_rows(generated_utc: str) -> list[dict[str, object]]:
    return [
        {
            "gate_id": "DG831_0_current_corpus_status",
            "question": "Does current MTS derive the Khat tensor owner?",
            "answer": "no",
            "reason": "S_bal/equivalent parent block, range theorem, boundary silence, and response matrices are absent",
            "effect": "local branch remains closure-only for current corpus",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "gate_id": "DG831_1_route_not_dead",
            "question": "Is the route mathematically dead?",
            "answer": "no",
            "reason": "831 reduces exact suppression to a precise range/cokernel theorem for D_T",
            "effect": "next work can attack D_T range and boundary compatibility directly",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "gate_id": "DG831_2_claim_guard",
            "question": "Can local GR, PPN, R10, clock, orbital, or WEP pass be claimed?",
            "answer": "no",
            "reason": "operator contract is not parent-signed and no sourced observable residual rows pass",
            "effect": "no public/local claim from 831",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
    ]


def decision_rows(generated_utc: str) -> list[dict[str, object]]:
    return [
        {
            "decision_id": "D831_0",
            "finding": "exact Khat suppression condition derived as a range/cokernel law",
            "reason": "the variational balance action gives D_T^dagger r=0, so residual equals cokernel projection plus obstruction terms",
            "status": CLAIM_CEILING,
            "claim_allowed": "false",
            "next_target": NEXT_TARGET,
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "decision_id": "D831_1",
            "finding": "parent adoption fails for the current corpus",
            "reason": "no current source signs the Khat balance action, range theorem, boundary theorem, matter descent, or response matrices",
            "status": CLAIM_CEILING,
            "claim_allowed": "false",
            "next_target": NEXT_TARGET,
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
    ]


def next_target_rows(generated_utc: str) -> list[dict[str, object]]:
    return [
        {
            "next_target": NEXT_TARGET,
            "objective": "prove or bound the trace-free divergence range condition D_T K=G on a local domain, including boundary/cokernel terms",
            "include": "flat proof, curved correction, boundary compatibility, cokernel projector, amplitude estimate, no-claim runner",
            "exclude": "adopting Khat owner without parent action, local-GR claim, PPN/R10 pass with placeholders, GitHub action",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        }
    ]


def nonclaim_summary_rows(generated_utc: str) -> list[dict[str, object]]:
    return [
        {
            "status": STATUS,
            "claim_ceiling": CLAIM_CEILING,
            "what_changed": "derived the exact range/cokernel contract for Khat local suppression and installed a missing-input runner",
            "what_is_not_claimed": "parent-derived Khat owner, local GR, PPN, R10, clocks, orbital, WEP, or matter descent",
            "next_target": NEXT_TARGET,
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        }
    ]


def all_valid_for_claim_false(row_groups: list[list[dict[str, object]]]) -> bool:
    for rows in row_groups:
        for row in rows:
            if row.get("valid_for_claim") != "false":
                return False
    return True


def validation_rows(
    source_rows: list[dict[str, object]],
    contract_rows: list[dict[str, object]],
    theorem_rows: list[dict[str, object]],
    adoption_rows: list[dict[str, object]],
    runner_inputs: list[dict[str, object]],
    runner_outputs: list[dict[str, object]],
    demotion_rows: list[dict[str, object]],
    decisions: list[dict[str, object]],
    next_targets: list[dict[str, object]],
    nonclaim: list[dict[str, object]],
) -> list[dict[str, object]]:
    prior_clean, prior_detail = validation_file_clean(RESIDUALS / "P8_Y5_BRR545_830_VALIDATION.csv")
    formalization_count = formalization_workbench_modified_count()
    source_ok = all(row["exists"] == "true" and row["needle_check"] == "pass" for row in source_rows)
    contract_ok = {
        row["contract_id"]
        for row in contract_rows
    }.issuperset({"OC831_1_balance_action", "OC831_2_first_variation", "OC831_3_exact_zero_condition", "OC831_4_bound_condition"})
    theorem_ok = any(row["result"] == "r_star=P_coker(D_T)G_when_Ereg_and_boundary_zero" for row in theorem_rows) and any(
        row["result"] == "q_loc_zero_reduced_to_range_and_boundary_theorem" for row in theorem_rows
    )
    adoption_blocks = any(row["audit_id"] == "PA831_5_verdict" and row["status"] == "not_adopted_closure_only_for_current_corpus" for row in adoption_rows)
    runner_blocks = any(row["row_id"] == "template_missing_range_inputs" and row["passes_all"] == "false" for row in runner_outputs)
    no_missing_passes = not any(row["passes_all"] == "true" and "missing_fields" in row["block_reason"] for row in runner_outputs)
    demotion_ok = any(row["gate_id"] == "DG831_0_current_corpus_status" and row["answer"] == "no" for row in demotion_rows)
    no_claim = (
        not any(row["passes_all"] == "true" for row in runner_outputs)
        and not any(row["claim_allowed"] == "true" for row in decisions)
    )
    nonclaim_ok = all_valid_for_claim_false(
        [source_rows, contract_rows, theorem_rows, adoption_rows, runner_inputs, runner_outputs, demotion_rows, decisions, next_targets, nonclaim]
    )
    next_selected = bool(next_targets) and next_targets[0]["next_target"] == NEXT_TARGET

    return [
        {
            "check_id": "V831_0_sources_exist_and_needles",
            "result": "pass" if source_ok else "fail",
            "detail": "all source paths exist and needles are present" if source_ok else "source register has missing path or needle",
        },
        {
            "check_id": "V831_1_prior_830_clean",
            "result": "pass" if prior_clean else "fail",
            "detail": prior_detail,
        },
        {
            "check_id": "V831_2_operator_contract_complete",
            "result": "pass" if contract_ok else "fail",
            "detail": "balance action, first variation, exact-zero, and bound clauses present",
        },
        {
            "check_id": "V831_3_range_cokernel_theorem_recorded",
            "result": "pass" if theorem_ok else "fail",
            "detail": "residual reduced to P_coker(D_T)G plus obstruction terms",
        },
        {
            "check_id": "V831_4_parent_adoption_blocked",
            "result": "pass" if adoption_blocks else "fail",
            "detail": "current corpus does not adopt Khat owner as parent-derived",
        },
        {
            "check_id": "V831_5_runner_template_blocks_missing",
            "result": "pass" if runner_blocks else "fail",
            "detail": "template_missing_range_inputs is blocked before numeric use",
        },
        {
            "check_id": "V831_6_no_missing_input_passes",
            "result": "pass" if no_missing_passes else "fail",
            "detail": "no row with missing fields passes",
        },
        {
            "check_id": "V831_7_local_branch_demoted_for_current_corpus",
            "result": "pass" if demotion_ok else "fail",
            "detail": "current corpus status is closure-only/nonclaim",
        },
        {
            "check_id": "V831_8_no_data_or_local_GR_claim",
            "result": "pass" if no_claim else "fail",
            "detail": "no data, local-GR, PPN, R10, clock, orbital, or WEP pass selected",
        },
        {
            "check_id": "V831_9_all_rows_nonclaim",
            "result": "pass" if nonclaim_ok else "fail",
            "detail": "all generated rows valid_for_claim=false",
        },
        {
            "check_id": "V831_10_next_target_selected",
            "result": "pass" if next_selected else "fail",
            "detail": NEXT_TARGET,
        },
        {
            "check_id": "V831_11_formalization_workbench_untouched",
            "result": "pass" if formalization_count == 0 else "fail",
            "detail": f"formalization_changed_after_cutoff={formalization_count}",
        },
        {
            "check_id": "V831_12_validation_rows_ready",
            "result": "pass",
            "detail": "validation table constructed",
        },
    ]


def csv_table(rows: list[dict[str, object]], columns: list[str]) -> str:
    header = "| " + " | ".join(columns) + " |"
    separator = "| " + " | ".join("---" for _ in columns) + " |"
    lines = [header, separator]
    for row in rows:
        values = []
        for column in columns:
            text = str(row.get(column, "")).replace("\n", " ").replace("|", "\\|")
            values.append(text)
        lines.append("| " + " | ".join(values) + " |")
    return "\n".join(lines)


def write_document(
    source_rows: list[dict[str, object]],
    contract_rows: list[dict[str, object]],
    theorem_rows: list[dict[str, object]],
    adoption_rows: list[dict[str, object]],
    runner_inputs: list[dict[str, object]],
    runner_outputs: list[dict[str, object]],
    demotion_rows: list[dict[str, object]],
    decisions: list[dict[str, object]],
    next_targets: list[dict[str, object]],
    nonclaim: list[dict[str, object]],
    validation: list[dict[str, object]],
) -> None:
    sections = [
        "# 831 - Y5 R10 Parent Khat Tensor Operator Or Local Branch Closure",
        "",
        "Current result: **the exact local `K_hat` suppression problem has been reduced to a range/cokernel theorem for the trace-free divergence operator, but the parent action does not yet sign the operator**. This is progress: the condition is no longer a vague plateau axiom. It is `P_coker(D_T)G=0` plus boundary, regularizer, amplitude, and observable-response gates.",
        "",
        "## Non-Claim Summary",
        "",
        csv_table(nonclaim, ["status", "claim_ceiling", "what_changed", "what_is_not_claimed", "next_target", "valid_for_claim"]),
        "",
        "## Derived Operator Contract",
        "",
        csv_table(contract_rows, ["contract_id", "object", "equation_or_condition", "derivation_status", "what_it_proves", "what_remains_open", "valid_for_claim"]),
        "",
        "## Range/Cokernel Theorem",
        "",
        csv_table(theorem_rows, ["theorem_id", "statement", "proof_step", "result", "failure_mode", "valid_for_claim"]),
        "",
        "## Parent Adoption Audit",
        "",
        csv_table(adoption_rows, ["audit_id", "required_evidence", "current_evidence", "status", "effect", "valid_for_claim"]),
        "",
        "## Range Runner Input Template",
        "",
        csv_table(runner_inputs, ["row_id", "row_status", "G_norm", "cokernel_fraction", "boundary_obstruction_norm", "parent_action_source_path", "numeric_ready", "valid_for_claim", "notes"]),
        "",
        "## Range Runner Output",
        "",
        csv_table(runner_outputs, ["row_id", "runner_status", "q_total_bound", "observable_bound", "passes_all", "block_reason", "valid_for_claim"]),
        "",
        "## Demotion Gate",
        "",
        csv_table(demotion_rows, ["gate_id", "question", "answer", "reason", "effect", "valid_for_claim"]),
        "",
        "## Decision",
        "",
        csv_table(decisions, ["decision_id", "finding", "reason", "status", "claim_allowed", "next_target", "valid_for_claim"]),
        "",
        "## Next Target",
        "",
        csv_table(next_targets, ["next_target", "objective", "include", "exclude", "valid_for_claim"]),
        "",
        "## Source Register",
        "",
        csv_table(source_rows, ["source_id", "path", "exists", "needle_check", "role", "valid_for_claim"]),
        "",
        "## Validation",
        "",
        csv_table(validation, ["check_id", "result", "detail"]),
        "",
    ]
    OUTPUT_DOC.write_text("\n".join(sections), encoding="utf-8")


def main() -> None:
    generated_utc = datetime.now(timezone.utc).isoformat(timespec="seconds")
    source_rows = source_register_rows(generated_utc)
    contract_rows = operator_contract_rows(generated_utc)
    theorem_rows = range_theorem_rows(generated_utc)
    adoption_rows = parent_adoption_rows(generated_utc)
    runner_inputs = runner_input_rows(generated_utc)
    runner_outputs = [run_range_row(row, generated_utc) for row in runner_inputs]
    demotion_rows = demotion_gate_rows(generated_utc)
    decisions = decision_rows(generated_utc)
    next_targets = next_target_rows(generated_utc)
    nonclaim = nonclaim_summary_rows(generated_utc)
    validation = validation_rows(
        source_rows,
        contract_rows,
        theorem_rows,
        adoption_rows,
        runner_inputs,
        runner_outputs,
        demotion_rows,
        decisions,
        next_targets,
        nonclaim,
    )

    write_csv(SOURCE_REGISTER_PATH, source_rows, ["source_id", "path", "exists", "needle_check", "role", "valid_for_claim", "generated_utc"])
    write_csv(
        OPERATOR_CONTRACT_PATH,
        contract_rows,
        ["contract_id", "object", "equation_or_condition", "derivation_status", "what_it_proves", "what_remains_open", "valid_for_claim", "generated_utc"],
    )
    write_csv(
        RANGE_THEOREM_PATH,
        theorem_rows,
        ["theorem_id", "statement", "proof_step", "result", "failure_mode", "valid_for_claim", "generated_utc"],
    )
    write_csv(
        PARENT_ADOPTION_PATH,
        adoption_rows,
        ["audit_id", "required_evidence", "current_evidence", "status", "effect", "valid_for_claim", "generated_utc"],
    )
    write_csv(
        RUNNER_INPUT_PATH,
        runner_inputs,
        [
            "row_id",
            "row_status",
            "G_norm",
            "cokernel_fraction",
            "boundary_obstruction_norm",
            "regularizer_norm",
            "coercivity_inverse",
            "kappa_K",
            "observable_response_norm",
            "observable_limit",
            "range_theorem_source_path",
            "boundary_condition_source_path",
            "parent_action_source_path",
            "observable_response_source_path",
            "numeric_ready",
            "valid_for_claim",
            "notes",
            "generated_utc",
        ],
    )
    write_csv(
        RUNNER_OUTPUT_PATH,
        runner_outputs,
        [
            "row_id",
            "runner_status",
            "q_cokernel_bound",
            "q_boundary_bound",
            "q_regularizer_bound",
            "q_total_bound",
            "observable_bound",
            "passes_all",
            "block_reason",
            "valid_for_claim",
            "generated_utc",
        ],
    )
    write_csv(
        DEMOTION_GATE_PATH,
        demotion_rows,
        ["gate_id", "question", "answer", "reason", "effect", "valid_for_claim", "generated_utc"],
    )
    write_csv(
        DECISION_PATH,
        decisions,
        ["decision_id", "finding", "reason", "status", "claim_allowed", "next_target", "valid_for_claim", "generated_utc"],
    )
    write_csv(
        NEXT_TARGET_PATH,
        next_targets,
        ["next_target", "objective", "include", "exclude", "valid_for_claim", "generated_utc"],
    )
    write_csv(
        NONCLAIM_SUMMARY_PATH,
        nonclaim,
        ["status", "claim_ceiling", "what_changed", "what_is_not_claimed", "next_target", "valid_for_claim", "generated_utc"],
    )
    write_csv(VALIDATION_PATH, validation, ["check_id", "result", "detail"])
    write_document(
        source_rows,
        contract_rows,
        theorem_rows,
        adoption_rows,
        runner_inputs,
        runner_outputs,
        demotion_rows,
        decisions,
        next_targets,
        nonclaim,
        validation,
    )

    print(f"wrote={OUTPUT_DOC}")
    print(f"wrote={VALIDATION_PATH}")
    print(f"status={STATUS}")
    print(f"claim_ceiling={CLAIM_CEILING}")
    print(f"next_target={NEXT_TARGET}")


if __name__ == "__main__":
    main()

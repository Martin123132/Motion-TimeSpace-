from __future__ import annotations

import csv
import subprocess
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(r"D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main")
POST_CHECKPOINT = ROOT / "post-checkpoint-work"
FORMALIZATION = ROOT / "formalization-workbench"
RESIDUALS = POST_CHECKPOINT / "source-intake" / "mts_residuals"

OUTPUT_DOC = POST_CHECKPOINT / "861-Y5-R10-Ward-owned-boundary-charge-endpoint-and-N5-projector-closure.md"
SOURCE_REGISTER_PATH = RESIDUALS / "P8_Y5_R10_861_SOURCE_REGISTER.csv"
EXACT_READOUT_BRIDGE_PATH = RESIDUALS / "P8_Y5_R10_861_EXACT_READOUT_AMPLITUDE_BRIDGE.csv"
ENDPOINT_AUDIT_PATH = RESIDUALS / "P8_Y5_R10_861_ENDPOINT_EQUATION_AUDIT.csv"
N5_PROJECTOR_PATH = RESIDUALS / "P8_Y5_R10_861_N5_PROJECTOR_CLOSURE_AUDIT.csv"
COFRAME_PULLBACK_PATH = RESIDUALS / "P8_Y5_R10_861_COFRAME_PULLBACK_WARD_LEDGER.csv"
QLOC_CONTRACT_PATH = RESIDUALS / "P8_Y5_R10_861_QLOC_SUPPRESSION_CONTRACT.csv"
CONDITIONAL_THEOREM_PATH = RESIDUALS / "P8_Y5_R10_861_CONDITIONAL_THEOREM_READOUT.csv"
ROUTE_CHOICE_PATH = RESIDUALS / "P8_Y5_R10_861_ROUTE_CHOICE.csv"
CLAIM_GUARD_PATH = RESIDUALS / "P8_Y5_R10_861_CLAIM_GUARD.csv"
DECISION_PATH = RESIDUALS / "P8_Y5_R10_861_DECISION.csv"
NEXT_TARGET_PATH = RESIDUALS / "P8_Y5_R10_861_NEXT_TARGET.csv"
NONCLAIM_SUMMARY_PATH = RESIDUALS / "P8_Y5_R10_861_NONCLAIM_SUMMARY.csv"
VALIDATION_PATH = RESIDUALS / "P8_Y5_BRR545_861_VALIDATION.csv"

PRIOR_VALIDATION_PATH = RESIDUALS / "P8_Y5_BRR545_860_VALIDATION.csv"

STATUS = "Y5_R10_861_exact_readout_bridge_constructed_endpoint_N5_still_open_nonclaim"
CLAIM_CEILING = "conditional_bridge_only_no_endpoint_theorem_no_N5_closure_no_local_GR_claim"
NEXT_TARGET = "862-Y5-R10-trace-lift-endpoint-equation-and-coframe-pullback-closure.md"

SOURCE_SPECS = [
    {
        "source_id": "860_doc",
        "path": POST_CHECKPOINT / "860-Y5-R10-parent-amplitude-law-and-GR-limit-derivation-contract.md",
        "needles": [
            "exact locked amplitude `b_P=2/27`",
            "Ward Projector Blocker Ledger",
            "861-Y5-R10-Ward-owned-boundary-charge-endpoint-and-N5-projector-closure.md",
        ],
        "role": "immediate amplitude/local-GR contract handoff",
    },
    {
        "source_id": "860_validation",
        "path": PRIOR_VALIDATION_PATH,
        "needles": [
            "V860_7_Ward_projector_blockers_ready,pass",
            "V860_10_all_rows_nonclaim,pass",
            "V860_12_formalization_workbench_untouched,pass",
        ],
        "role": "prior checkpoint validation",
    },
    {
        "source_id": "337_exact_pullback",
        "path": POST_CHECKPOINT / "337-exact-parent-pullback-selection-rule-gate.md",
        "needles": [
            "exact_parent_pullback_theorem_constructed_parent_action_premise_open",
            "q_trace = 2/27",
            "epsilon_H = 1",
        ],
        "role": "conditional exact-readout algebra",
    },
    {
        "source_id": "356_Ward_projector",
        "path": POST_CHECKPOINT / "356-parent-action-ward-identity-and-projector-variation.md",
        "needles": [
            "Ward identity",
            "F_P^nu",
            "metric-dependent projector + dropped stress = fake GR",
        ],
        "role": "projector variation force ledger",
    },
    {
        "source_id": "384_first_variation",
        "path": POST_CHECKPOINT / "384-parent-action-first-variation-obstruction-map.md",
        "needles": [
            "observed-coframe selector pullback",
            "Pi_I^matter",
            "first unowned term",
        ],
        "role": "coframe pullback obstruction",
    },
    {
        "source_id": "109_boundary_charge_attempt",
        "path": POST_CHECKPOINT / "109-boundary-charge-two-ninth-theorem-attempt.md",
        "needles": [
            "normalized boundary charge",
            "boundary_charge_unit_defined",
            "product_two_over_nine_derived",
        ],
        "role": "previous failed endpoint/charge theorem attempt",
    },
    {
        "source_id": "347_local_GR_attempt",
        "path": POST_CHECKPOINT / "347-local-GR-parent-reduction-theorem-attempt.md",
        "needles": [
            "N5_projector_stress_Bianchi_safe",
            "T_projector",
            "conditional GR-reduction theorem",
        ],
        "role": "local GR conditional theorem and N5 blocker",
    },
    {
        "source_id": "382_parent_action_contract",
        "path": POST_CHECKPOINT / "382-parent-local-action-minimal-contract.md",
        "needles": [
            "Required Variation Identities",
            "S_projector_P_D",
            "S_boundary_class_only",
        ],
        "role": "minimal parent action sector contract",
    },
    {
        "source_id": "393_Newtonian_source",
        "path": POST_CHECKPOINT / "393-source-normalized-Newtonian-limit-under-identity-closure.md",
        "needles": [
            "nabla^2 Phi = 4 pi G_eff rho_eff",
            "measured GM",
            "not parent-derived",
        ],
        "role": "Newtonian source-normalization gate",
    },
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


def exact_readout_bridge_rows(generated_utc: str) -> list[dict[str, object]]:
    return [
        {
            "bridge_id": "ER861_0_exact_parent_pullback",
            "premise": "full S27 cell equivalence plus exact parent readout projection",
            "mathematical_form": "Tr(P_active H_parent)/27 = 2/27 and Tr(P_active H_parent)/2 = 1",
            "result": "q_trace=2/27 and epsilon_H=1 conditionally",
            "status": "conditional_import_from_337",
            "missing_for_claim": "parent action must prove exact readout rather than Wilsonian reduced EFT",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "bridge_id": "ER861_1_trace_lift_to_endpoint",
            "premise": "FLRW endpoint charge is the three-direction trace lift of the active rank-2 readout",
            "mathematical_form": "DeltaR = 3 q_trace",
            "result": "if q_trace=2/27 then DeltaR=2/9",
            "status": "central_missing_theorem",
            "missing_for_claim": "Ward trace-lift equation tying boundary charge to FLRW endpoint memory",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "bridge_id": "ER861_2_amplitude_identity",
            "premise": "eta=1, a_F=1, DeltaR=2/9",
            "mathematical_form": "b_P = a_F DeltaR/(3 eta^2) = 2/27",
            "result": "exact 2/27 amplitude follows if ER861_0 and ER861_1 are proven",
            "status": "conditional_bridge_constructed_not_proved",
            "missing_for_claim": "eta lock, trace coupling, endpoint theorem",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "bridge_id": "ER861_3_no_target_inversion",
            "premise": "after ER861_0 and ER861_1 the number is fixed algebraically",
            "mathematical_form": "b_P=2/27 independent of argmin_BIC(b_P)",
            "result": "would remove post-fit circularity if parent premises are proved",
            "status": "future_promotion_gate",
            "missing_for_claim": "the premises are still open",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
    ]


def endpoint_audit_rows(generated_utc: str) -> list[dict[str, object]]:
    return [
        {
            "endpoint_id": "EP861_0_charge_unit",
            "object": "Q_*",
            "required_equation": "Q_* = parent-normalized Ward charge unit",
            "current_status": "missing",
            "why_it_blocks": "DeltaR cannot be a prediction without a normalization unit",
            "next_clause": "derive Q_* from exact parent readout/current normalization",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "endpoint_id": "EP861_1_early_endpoint",
            "object": "Q_early",
            "required_equation": "delta S_boundary/dQ_early = 0 before data",
            "current_status": "missing",
            "why_it_blocks": "endpoint value cannot be chosen to make 2/9",
            "next_clause": "boundary Euler/Ward stationarity equation",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "endpoint_id": "EP861_2_today_endpoint",
            "object": "Q_today",
            "required_equation": "delta S_boundary/dQ_today = 0 before data",
            "current_status": "missing",
            "why_it_blocks": "present endpoint cannot be fitted or calibrated from SN/BAO",
            "next_clause": "observer/coframe endpoint selection without local fifth-force leakage",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "endpoint_id": "EP861_3_endpoint_difference",
            "object": "DeltaR",
            "required_equation": "(Q_early-Q_today)/Q_* = 2/9",
            "current_status": "not_derived",
            "why_it_blocks": "2/9 remains theorem target only",
            "next_clause": "prove DeltaR=3 q_trace with q_trace=2/27",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "endpoint_id": "EP861_4_nohair",
            "object": "boundary charge local no-hair",
            "required_equation": "boundary stress has monopole/FLRW endpoint support only; no B_TF or B_0i in local exterior",
            "current_status": "open",
            "why_it_blocks": "boundary charge can otherwise become PPN hair",
            "next_clause": "tie endpoint current to N5 projector/no-hair closure",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
    ]


def n5_projector_rows(generated_utc: str) -> list[dict[str, object]]:
    return [
        {
            "fork_id": "N5_861_0_exact_readout_projector",
            "projector_case": "metric-independent exact parent readout / relative-chain projector",
            "Ward_result": "F_P_bulk=0 if P_D is covariant, constraint-owned, and not varied as a local metric-dependent tensor",
            "local_GR_status": "conditional_best_route",
            "claim_allowed": "false",
            "missing": "parent action must prove exact-readout premise and no coframe pullback source",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "fork_id": "N5_861_1_boundary_only_projector",
            "projector_case": "boundary-only projector charge",
            "Ward_result": "bulk force can vanish away from boundary",
            "local_GR_status": "conditional_only_if_boundary_nohair",
            "claim_allowed": "false",
            "missing": "monopole-only/no shear/vector/clock/WEP boundary theorem",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "fork_id": "N5_861_2_metric_dependent_projector",
            "projector_case": "metric-dependent Hodge/orthogonal projector",
            "Ward_result": "T_projector and F_P are physical",
            "local_GR_status": "not_GR_unless_stress_cancelled_or_bounded",
            "claim_allowed": "false",
            "missing": "compute retained residual or derive cancellation",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "fork_id": "N5_861_3_fixed_external_projector",
            "projector_case": "fixed external projector",
            "Ward_result": "explicit diffeomorphism-breaking force",
            "local_GR_status": "forbidden",
            "claim_allowed": "false",
            "missing": "must be replaced by parent-owned covariant selector",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "fork_id": "N5_861_4_retained_projector_stress",
            "projector_case": "retained bulk projector stress",
            "Ward_result": "conservation can be honest if T_projector is included",
            "local_GR_status": "modified_gravity_residual_until_bounded",
            "claim_allowed": "false",
            "missing": "PPN/local bound map for retained stress",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
    ]


def coframe_pullback_rows(generated_utc: str) -> list[dict[str, object]]:
    return [
        {
            "pullback_id": "CP861_0_fixed_ehat_theorem",
            "term": "delta S_matter/dZ_I at fixed ehat",
            "status": "conditional_zero",
            "risk": "insufficient for parent variation if ehat depends on selector/projector fields",
            "required_resolution": "total variation must include selector pullback",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "pullback_id": "CP861_1_total_variation",
            "term": "(delta S_matter/d ehat^a_mu)(partial ehat^a_mu/partial Z_I)",
            "status": "open_hard",
            "risk": "matter stress sources selector/projector equations and can create WEP/clock/PPN residuals",
            "required_resolution": "partial ehat/partial Z_I=0, pure gauge, universal absorbed constant, or Ward-owned counterstress",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "pullback_id": "CP861_2_exact_identity_coframe",
            "term": "ehat=e in local exterior",
            "status": "best_closure_route",
            "risk": "must be parent-selected, not imposed after the fact",
            "required_resolution": "identity coframe follows from same exact-readout/selector theorem",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "pullback_id": "CP861_3_boundary_endpoint_coframe",
            "term": "boundary endpoint changes observed coframe",
            "status": "must_be_forbidden_or_owned",
            "risk": "endpoint charge becomes local clock/WEP hair",
            "required_resolution": "endpoint charge couples only to FLRW trace/monopole, not local matter coframe",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
    ]


def qloc_contract_rows(generated_utc: str) -> list[dict[str, object]]:
    return [
        {
            "contract_id": "QL861_0_definition",
            "requirement": "derive q_loc^nu from varied parent objects",
            "mathematical_form": "q_loc^nu=P_loc(nabla^nu Gamma_eff-nabla_mu K_hat^{mu nu})",
            "current_status": "definition_retained_not_zero_proved",
            "zero_condition": "Gamma_eff and K_hat are Ward-owned and local projector/boundary forces vanish or are retained",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "contract_id": "QL861_1_exact_readout_zero",
            "requirement": "exact-readout projector produces no local bulk exchange",
            "mathematical_form": "F_P_bulk=0 and F_boundary_local=0 => q_loc^nu=0",
            "current_status": "conditional_on_N5_and_boundary_nohair",
            "zero_condition": "N5_861_0 plus EP861_4 plus CP861_2",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "contract_id": "QL861_2_retained_residual",
            "requirement": "if a projector/boundary term survives, keep it as a local residual",
            "mathematical_form": "q_loc^nu != 0 => PPN/local-bound row, not GR claim",
            "current_status": "fallback_required",
            "zero_condition": "none; score/bound residual instead",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
    ]


def conditional_theorem_rows(generated_utc: str) -> list[dict[str, object]]:
    return [
        {
            "theorem_id": "TH861_0_amplitude_bridge",
            "if_stack": "exact parent readout gives q_trace=2/27; Ward trace lift gives DeltaR=3 q_trace; eta=a_F=1",
            "then_result": "DeltaR=2/9 and b_P=2/27",
            "status": "conditional_bridge_constructed_not_proved",
            "blocking_rows": "ER861_1;EP861_0;EP861_1;EP861_2;CP861_3",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "theorem_id": "TH861_1_local_GR_bridge",
            "if_stack": "exact readout projector has F_P_bulk=0; boundary endpoint has no local hair; ehat=e locally; source normalization closes",
            "then_result": "q_loc^nu=0 and local exterior can reduce to GR/Newton under the existing conditional EH stack",
            "status": "conditional_bridge_constructed_not_proved",
            "blocking_rows": "N5_861_0;EP861_4;CP861_1;QL861_0",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "theorem_id": "TH861_2_failure_branch",
            "if_stack": "trace lift or N5 closure fails",
            "then_result": "2/27 remains empirical closure and local branch remains retained-residual modified-gravity route",
            "status": "fallback_defined",
            "blocking_rows": "retained_projector_stress_or_endpoint_nohair_failure",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
    ]


def route_choice_rows(generated_utc: str) -> list[dict[str, object]]:
    return [
        {
            "route_id": "RC861_0_selected",
            "route": "trace_lift_endpoint_equation_and_coframe_pullback_closure",
            "status": "selected",
            "reason": "exact readout already conditionally owns q_trace=2/27; the missing move is the Ward trace lift to DeltaR plus coframe/projector pullback closure",
            "include": "DeltaR=3 q_trace, endpoint stationarity, Q_*, ehat pullback, boundary no-hair",
            "exclude": "fitted endpoint values, dropped projector stress, plateau q_loc axiom, public claim",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "route_id": "RC861_1_deferred",
            "route": "local_bound_runner_for_retained_projector_stress",
            "status": "deferred",
            "reason": "only needed if the exact-readout/N5 closure attempt fails and a nonzero residual must be bounded",
            "include": "PPN residual coefficients from T_projector or q_loc",
            "exclude": "before deriving or rejecting the zero theorem",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
    ]


def claim_guard_rows(generated_utc: str) -> list[dict[str, object]]:
    return [
        {
            "guard_id": "CG861_0_no_2over27_prediction",
            "claim": "MTS derives b_P=2/27",
            "status": "forbidden",
            "reason": "DeltaR=3 q_trace and endpoint equations remain unproved",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "guard_id": "CG861_1_no_N5_closure",
            "claim": "N5 projector stress is closed",
            "status": "forbidden",
            "reason": "exact-readout projector closure is conditional and coframe pullback remains open",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "guard_id": "CG861_2_no_local_GR",
            "claim": "local GR/Newton is derived",
            "status": "forbidden",
            "reason": "q_loc, source normalization, and PPN residual vector remain theorem/bound targets",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "guard_id": "CG861_3_allowed_conditional_bridge",
            "claim": "conditional bridge between 2/27 amplitude and N5/local-GR machinery is explicit",
            "status": "allowed_private_nonclaim",
            "reason": "861 identifies the shared exact-readout/Ward trace-lift route and the exact blockers",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
    ]


def decision_rows(generated_utc: str) -> list[dict[str, object]]:
    return [
        {
            "decision_id": "D861_0",
            "finding": "conditional_bridge_found_but_not_proved",
            "reason": "exact parent readout gives q_trace=2/27 conditionally; proving DeltaR=3 q_trace would derive the 2/27 amplitude target",
            "status": CLAIM_CEILING,
            "claim_allowed": "false",
            "next_target": NEXT_TARGET,
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "decision_id": "D861_1",
            "finding": "N5_closure_reduces_to_exact_readout_plus_coframe_pullback",
            "reason": "metric-independent exact-readout projectors can avoid bulk F_P, but observed-coframe pullback and boundary no-hair remain open",
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
            "objective": "try to prove DeltaR=3 q_trace and close the observed-coframe pullback so exact-readout N5 closure is not spoiled by matter stress",
            "include": "Ward trace-lift equation, Q_* endpoint unit, boundary stationarity, ehat=e local theorem, no local boundary hair",
            "exclude": "cosmology scoring, fitted endpoints, dropped T_projector, local plateau axiom, formalization-workbench edits",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        }
    ]


def nonclaim_summary_rows(generated_utc: str) -> list[dict[str, object]]:
    return [
        {
            "status": STATUS,
            "claim_ceiling": CLAIM_CEILING,
            "what_changed": "constructed a conditional bridge from exact parent readout q_trace=2/27 to DeltaR=2/9 and mapped N5 projector closure forks",
            "best_partial_result": "DeltaR=3 q_trace would make b_P=q_trace=2/27",
            "hard_blockers": "Ward trace lift, Q_* endpoints, observed-coframe pullback, boundary no-hair",
            "what_is_not_claimed": "2/27 prediction, N5 closure, q_loc zero, local GR/Newton, public evidence",
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
    exact_rows: list[dict[str, object]],
    endpoint_rows: list[dict[str, object]],
    n5_rows: list[dict[str, object]],
    coframe_rows: list[dict[str, object]],
    qloc_rows: list[dict[str, object]],
    theorem_rows: list[dict[str, object]],
    routes: list[dict[str, object]],
    guards: list[dict[str, object]],
    decisions: list[dict[str, object]],
    next_targets: list[dict[str, object]],
    nonclaim: list[dict[str, object]],
) -> list[dict[str, object]]:
    prior_clean, prior_detail = validation_file_clean(PRIOR_VALIDATION_PATH)
    formalization_count = formalization_workbench_modified_count()
    source_ok = all(row["exists"] == "true" and row["needle_check"] == "pass" for row in source_rows)
    exact_ok = any(row["bridge_id"] == "ER861_1_trace_lift_to_endpoint" and row["status"] == "central_missing_theorem" for row in exact_rows)
    endpoint_ok = len(endpoint_rows) == 5 and any(row["object"] == "DeltaR" and row["current_status"] == "not_derived" for row in endpoint_rows)
    n5_ok = len(n5_rows) == 5 and any(row["fork_id"] == "N5_861_0_exact_readout_projector" for row in n5_rows)
    coframe_ok = any(row["pullback_id"] == "CP861_1_total_variation" and row["status"] == "open_hard" for row in coframe_rows)
    qloc_ok = len(qloc_rows) == 3 and any(row["contract_id"] == "QL861_2_retained_residual" for row in qloc_rows)
    theorem_ok = len(theorem_rows) == 3 and any(row["theorem_id"] == "TH861_0_amplitude_bridge" for row in theorem_rows)
    route_ok = any(row["route_id"] == "RC861_0_selected" for row in routes)
    no_claim = not any(row["claim_allowed"] == "true" for row in decisions)
    nonclaim_ok = all_valid_for_claim_false([source_rows, exact_rows, endpoint_rows, n5_rows, coframe_rows, qloc_rows, theorem_rows, routes, guards, decisions, next_targets, nonclaim])
    next_selected = bool(next_targets) and next_targets[0]["next_target"] == NEXT_TARGET
    return [
        {"check_id": "V861_0_sources_exist_and_needles", "result": "pass" if source_ok else "fail", "detail": "all source paths exist and needles are present" if source_ok else "source register has missing path or needle"},
        {"check_id": "V861_1_prior_860_clean", "result": "pass" if prior_clean else "fail", "detail": prior_detail},
        {"check_id": "V861_2_exact_readout_bridge_ready", "result": "pass" if exact_ok else "fail", "detail": "q_trace=2/27 to DeltaR=3q_trace bridge recorded as missing theorem"},
        {"check_id": "V861_3_endpoint_audit_blocks_claim", "result": "pass" if endpoint_ok else "fail", "detail": "Q_*, endpoints, DeltaR, boundary no-hair rows remain open"},
        {"check_id": "V861_4_N5_projector_forks_ready", "result": "pass" if n5_ok else "fail", "detail": "N5 exact-readout, boundary, metric-dependent, external, retained forks recorded"},
        {"check_id": "V861_5_coframe_pullback_open", "result": "pass" if coframe_ok else "fail", "detail": "observed-coframe total variation obstruction remains open"},
        {"check_id": "V861_6_q_loc_contract_ready", "result": "pass" if qloc_ok else "fail", "detail": "q_loc zero and retained residual fallbacks recorded"},
        {"check_id": "V861_7_conditional_theorem_readout_ready", "result": "pass" if theorem_ok else "fail", "detail": "amplitude bridge, local-GR bridge, and failure branch recorded"},
        {"check_id": "V861_8_route_selected", "result": "pass" if route_ok else "fail", "detail": "trace lift endpoint and coframe pullback closure selected"},
        {"check_id": "V861_9_claim_allowed_false", "result": "pass" if no_claim else "fail", "detail": "decision rows keep claim_allowed=false"},
        {"check_id": "V861_10_all_rows_nonclaim", "result": "pass" if nonclaim_ok else "fail", "detail": "all generated rows valid_for_claim=false"},
        {"check_id": "V861_11_next_target_selected", "result": "pass" if next_selected else "fail", "detail": NEXT_TARGET},
        {"check_id": "V861_12_formalization_workbench_untouched", "result": "pass" if formalization_count == 0 else "fail", "detail": f"formalization_changed_after_cutoff={formalization_count}"},
        {"check_id": "V861_13_validation_rows_ready", "result": "pass", "detail": "validation table constructed"},
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
    exact_rows: list[dict[str, object]],
    endpoint_rows: list[dict[str, object]],
    n5_rows: list[dict[str, object]],
    coframe_rows: list[dict[str, object]],
    qloc_rows: list[dict[str, object]],
    theorem_rows: list[dict[str, object]],
    routes: list[dict[str, object]],
    guards: list[dict[str, object]],
    decisions: list[dict[str, object]],
    next_targets: list[dict[str, object]],
    nonclaim: list[dict[str, object]],
    validation: list[dict[str, object]],
) -> None:
    sections = [
        "# 861 - Y5 R10 Ward-Owned Boundary Charge Endpoint And N5 Projector Closure",
        "",
        "Current result: **a conditional bridge exists, but the proof is not closed**. Exact parent readout already conditionally gives `q_trace=2/27`; if the Ward trace lift proves `DeltaR=3 q_trace`, then `DeltaR=2/9` and `b_P=2/27` follow without target inversion. The same exact-readout route is also the cleanest N5 projector path, but observed-coframe pullback and boundary no-hair remain open.",
        "",
        "## Non-Claim Summary",
        "",
        csv_table(nonclaim, ["status", "claim_ceiling", "what_changed", "best_partial_result", "hard_blockers", "what_is_not_claimed", "next_target", "valid_for_claim"]),
        "",
        "## Exact Readout Amplitude Bridge",
        "",
        csv_table(exact_rows, ["bridge_id", "premise", "mathematical_form", "result", "status", "missing_for_claim", "valid_for_claim"]),
        "",
        "## Endpoint Equation Audit",
        "",
        csv_table(endpoint_rows, ["endpoint_id", "object", "required_equation", "current_status", "why_it_blocks", "next_clause", "valid_for_claim"]),
        "",
        "## N5 Projector Closure Audit",
        "",
        csv_table(n5_rows, ["fork_id", "projector_case", "Ward_result", "local_GR_status", "claim_allowed", "missing", "valid_for_claim"]),
        "",
        "## Coframe Pullback Ward Ledger",
        "",
        csv_table(coframe_rows, ["pullback_id", "term", "status", "risk", "required_resolution", "valid_for_claim"]),
        "",
        "## qloc Suppression Contract",
        "",
        csv_table(qloc_rows, ["contract_id", "requirement", "mathematical_form", "current_status", "zero_condition", "valid_for_claim"]),
        "",
        "## Conditional Theorem Readout",
        "",
        csv_table(theorem_rows, ["theorem_id", "if_stack", "then_result", "status", "blocking_rows", "valid_for_claim"]),
        "",
        "## Route Choice",
        "",
        csv_table(routes, ["route_id", "route", "status", "reason", "include", "exclude", "valid_for_claim"]),
        "",
        "## Claim Guard",
        "",
        csv_table(guards, ["guard_id", "claim", "status", "reason", "valid_for_claim"]),
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
    exact_rows = exact_readout_bridge_rows(generated_utc)
    endpoint_rows = endpoint_audit_rows(generated_utc)
    n5_rows = n5_projector_rows(generated_utc)
    coframe_rows = coframe_pullback_rows(generated_utc)
    qloc_rows = qloc_contract_rows(generated_utc)
    theorem_rows = conditional_theorem_rows(generated_utc)
    routes = route_choice_rows(generated_utc)
    guards = claim_guard_rows(generated_utc)
    decisions = decision_rows(generated_utc)
    next_targets = next_target_rows(generated_utc)
    nonclaim = nonclaim_summary_rows(generated_utc)
    validation = validation_rows(
        source_rows,
        exact_rows,
        endpoint_rows,
        n5_rows,
        coframe_rows,
        qloc_rows,
        theorem_rows,
        routes,
        guards,
        decisions,
        next_targets,
        nonclaim,
    )

    write_csv(SOURCE_REGISTER_PATH, source_rows, ["source_id", "path", "exists", "needle_check", "role", "valid_for_claim", "generated_utc"])
    write_csv(EXACT_READOUT_BRIDGE_PATH, exact_rows, ["bridge_id", "premise", "mathematical_form", "result", "status", "missing_for_claim", "valid_for_claim", "generated_utc"])
    write_csv(ENDPOINT_AUDIT_PATH, endpoint_rows, ["endpoint_id", "object", "required_equation", "current_status", "why_it_blocks", "next_clause", "valid_for_claim", "generated_utc"])
    write_csv(N5_PROJECTOR_PATH, n5_rows, ["fork_id", "projector_case", "Ward_result", "local_GR_status", "claim_allowed", "missing", "valid_for_claim", "generated_utc"])
    write_csv(COFRAME_PULLBACK_PATH, coframe_rows, ["pullback_id", "term", "status", "risk", "required_resolution", "valid_for_claim", "generated_utc"])
    write_csv(QLOC_CONTRACT_PATH, qloc_rows, ["contract_id", "requirement", "mathematical_form", "current_status", "zero_condition", "valid_for_claim", "generated_utc"])
    write_csv(CONDITIONAL_THEOREM_PATH, theorem_rows, ["theorem_id", "if_stack", "then_result", "status", "blocking_rows", "valid_for_claim", "generated_utc"])
    write_csv(ROUTE_CHOICE_PATH, routes, ["route_id", "route", "status", "reason", "include", "exclude", "valid_for_claim", "generated_utc"])
    write_csv(CLAIM_GUARD_PATH, guards, ["guard_id", "claim", "status", "reason", "valid_for_claim", "generated_utc"])
    write_csv(DECISION_PATH, decisions, ["decision_id", "finding", "reason", "status", "claim_allowed", "next_target", "valid_for_claim", "generated_utc"])
    write_csv(NEXT_TARGET_PATH, next_targets, ["next_target", "objective", "include", "exclude", "valid_for_claim", "generated_utc"])
    write_csv(NONCLAIM_SUMMARY_PATH, nonclaim, ["status", "claim_ceiling", "what_changed", "best_partial_result", "hard_blockers", "what_is_not_claimed", "next_target", "valid_for_claim", "generated_utc"])
    write_csv(VALIDATION_PATH, validation, ["check_id", "result", "detail"])
    write_document(source_rows, exact_rows, endpoint_rows, n5_rows, coframe_rows, qloc_rows, theorem_rows, routes, guards, decisions, next_targets, nonclaim, validation)

    print(f"wrote={OUTPUT_DOC}")
    print(f"wrote={VALIDATION_PATH}")
    print(f"status={STATUS}")
    print("partial_bridge=DeltaR=3*q_trace with q_trace=2/27 would give DeltaR=2/9 and b_P=2/27")
    print(f"claim_ceiling={CLAIM_CEILING}")
    print(f"next_target={NEXT_TARGET}")


if __name__ == "__main__":
    main()

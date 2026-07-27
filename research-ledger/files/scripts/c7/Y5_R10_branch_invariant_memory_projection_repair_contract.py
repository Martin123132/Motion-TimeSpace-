from __future__ import annotations

import csv
import subprocess
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(r"D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main")
POST_CHECKPOINT = ROOT / "post-checkpoint-work"
FORMALIZATION = ROOT / "formalization-workbench"
RESIDUALS = POST_CHECKPOINT / "source-intake" / "mts_residuals"

OUTPUT_DOC = POST_CHECKPOINT / "857-Y5-R10-branch-invariant-memory-projection-repair-contract.md"
SOURCE_REGISTER_PATH = RESIDUALS / "P8_Y5_R10_857_SOURCE_REGISTER.csv"
PROJECTION_CONTRACT_PATH = RESIDUALS / "P8_Y5_R10_857_BRANCH_INVARIANT_PROJECTION_CONTRACT.csv"
CHANNEL_DECOMPOSITION_PATH = RESIDUALS / "P8_Y5_R10_857_CHANNEL_DECOMPOSITION.csv"
BRANCH_SPLIT_LEDGER_PATH = RESIDUALS / "P8_Y5_R10_857_BRANCH_SPLIT_RESPONSE_LEDGER.csv"
RESPONSE_GATE_PATH = RESIDUALS / "P8_Y5_R10_857_RESPONSE_SOURCE_GATE.csv"
BAO_CONSERVATION_GUARD_PATH = RESIDUALS / "P8_Y5_R10_857_BAO_CONSERVATION_GUARD.csv"
ACCEPTANCE_TEST_PATH = RESIDUALS / "P8_Y5_R10_857_ACCEPTANCE_TESTS.csv"
ROUTE_CHOICE_PATH = RESIDUALS / "P8_Y5_R10_857_ROUTE_CHOICE.csv"
CLAIM_GUARD_PATH = RESIDUALS / "P8_Y5_R10_857_CLAIM_GUARD.csv"
DECISION_PATH = RESIDUALS / "P8_Y5_R10_857_DECISION.csv"
NEXT_TARGET_PATH = RESIDUALS / "P8_Y5_R10_857_NEXT_TARGET.csv"
NONCLAIM_SUMMARY_PATH = RESIDUALS / "P8_Y5_R10_857_NONCLAIM_SUMMARY.csv"
VALIDATION_PATH = RESIDUALS / "P8_Y5_BRR545_857_VALIDATION.csv"

BRANCH_TARGETS_PATH = RESIDUALS / "P8_Y5_R10_856_BRANCH_TARGET_CONSTRAINTS.csv"
PRIOR_VALIDATION_PATH = RESIDUALS / "P8_Y5_BRR545_856_VALIDATION.csv"

STATUS = "Y5_R10_857_branch_invariant_projection_contract_written_nonclaim"
CLAIM_CEILING = "contract_only_no_scored_repair_no_response_source_no_support_claim"
NEXT_TARGET = "858-Y5-R10-branch-invariant-parent-only-memory-stress-test.md"

SOURCE_SPECS = [
    {
        "source_id": "856_doc",
        "path": POST_CHECKPOINT / "856-Y5-R10-memory-projection-repair-or-independent-calibration-source-test.md",
        "needles": [
            "branch-invariant memory-projection repair contract",
            "Memory Projection Repair Contract",
            "857-Y5-R10-branch-invariant-memory-projection-repair-contract.md",
        ],
        "role": "selected repair route",
    },
    {
        "source_id": "856_validation",
        "path": PRIOR_VALIDATION_PATH,
        "needles": [
            "V856_5_route_selected,pass",
            "V856_7_all_rows_nonclaim,pass",
            "V856_9_formalization_workbench_untouched,pass",
        ],
        "role": "prior checkpoint validation",
    },
    {
        "source_id": "856_repair_contract",
        "path": RESIDUALS / "P8_Y5_R10_856_MEMORY_PROJECTION_REPAIR_CONTRACT.csv",
        "needles": [
            "b_response -> 0 must reduce exactly to branch-invariant parent memory",
            "q_B sourced before scoring",
            "Delta chi2_BAO(response)",
        ],
        "role": "unimplemented repair clauses",
    },
    {
        "source_id": "856_branch_targets",
        "path": BRANCH_TARGETS_PATH,
        "needles": ["no_sh0es", "sh0es", "b_eff_target"],
        "role": "branch effective-amplitude targets",
    },
    {
        "source_id": "856_source_test",
        "path": RESIDUALS / "P8_Y5_R10_856_INDEPENDENT_RESPONSE_SOURCE_TEST.csv",
        "needles": [
            "fails_projected_out",
            "fails_too_small",
            "spans_but_unsourced",
        ],
        "role": "failed independent response source test",
    },
]


def write_csv(path: Path, rows: list[dict[str, object]], fieldnames: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


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


def fmt(value: float) -> str:
    return f"{value:.12g}"


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


def branch_values() -> tuple[float, float, float]:
    rows = read_csv(BRANCH_TARGETS_PATH)
    by_branch = {row["branch"]: float(row["b_eff_target"]) for row in rows}
    no_sh0es = by_branch["no_sh0es"]
    sh0es = by_branch["sh0es"]
    return no_sh0es, sh0es, sh0es - no_sh0es


def projection_contract_rows(generated_utc: str) -> list[dict[str, object]]:
    return [
        {
            "contract_id": "BIP857_0_two_channel_identity",
            "clause": "replace branch-specific b_mem readout with parent plus optional response",
            "mathematical_form": "E2_B(z)=E2_LCDM_B(z)+b_P A_P(z)+b_R[B] A_R_B(z)",
            "acceptance_gate": "b_P is branch-invariant; b_R[B] is zero unless sourced before scoring",
            "status": "contract_written_not_scored",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "contract_id": "BIP857_1_parent_invariance",
            "clause": "parent memory channel must not know which calibration branch was used",
            "mathematical_form": "partial_B b_P = 0 and partial_B A_P(z)=0",
            "acceptance_gate": "same b_P and same A_P are used for no_SH0ES and SH0ES branches",
            "status": "required_for_858",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "contract_id": "BIP857_2_response_zero_limit",
            "clause": "response channel must vanish in the absence of an independent local/calibration source",
            "mathematical_form": "q_B=0 or MISSING_SOURCE => b_R[B]=0",
            "acceptance_gate": "branch split in b_eff disappears when q_B is absent",
            "status": "required_for_858",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "contract_id": "BIP857_3_no_target_inversion",
            "clause": "do not infer b_R[B] by subtracting the fitted branch target from the parent amplitude",
            "mathematical_form": "b_R[B] != b_eff_fit[B]-b_P unless q_B and C_R are independently signed first",
            "acceptance_gate": "target-derived response rows remain invalid for claim",
            "status": "guard_written",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "contract_id": "BIP857_4_gr_limit",
            "clause": "cosmology repair must retain the standard zero-memory baseline limit",
            "mathematical_form": "b_P=0 and b_R[B]=0 => E2_B(z)=E2_LCDM_B(z)",
            "acceptance_gate": "null-control parity remains exact before any MTS preference is discussed",
            "status": "required_for_858",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
    ]


def channel_decomposition_rows(generated_utc: str) -> list[dict[str, object]]:
    return [
        {
            "channel_id": "CH857_0_parent_memory",
            "object": "b_P A_P(z)",
            "meaning": "branch-invariant parent memory deformation of the expansion history",
            "allowed_source": "parent derivation or shared-amplitude stress test only",
            "forbidden_source": "separate SH0ES/no-SH0ES fitted b_mem values",
            "current_status": "candidate_channel_not_claimed",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "channel_id": "CH857_1_response_projection",
            "object": "b_R[B] A_R_B(z)",
            "meaning": "optional branch/local response projection",
            "allowed_source": "independent q_B and response coefficient C_R signed before scoring",
            "forbidden_source": "using required response magnitude solved from target split",
            "current_status": "set_to_zero_until_sourced",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "channel_id": "CH857_2_effective_readout",
            "object": "b_eff[B]=b_P+b_R[B]",
            "meaning": "diagnostic readout after parent and response terms are specified",
            "allowed_source": "computed from contract terms",
            "forbidden_source": "primitive independent fitted parameter per branch",
            "current_status": "diagnostic_only",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "channel_id": "CH857_3_calibration_offset",
            "object": "Delta M_B or nuisance offset",
            "meaning": "SN calibration/marginalization mode",
            "allowed_source": "likelihood nuisance accounting",
            "forbidden_source": "promoting a projected-out offset into a physical field amplitude",
            "current_status": "not_a_parent_memory_source",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
    ]


def branch_split_ledger_rows(generated_utc: str) -> list[dict[str, object]]:
    no_sh0es, sh0es, split = branch_values()
    midpoint = 0.5 * (no_sh0es + sh0es)
    return [
        {
            "ledger_id": "BS857_0_no_sh0es_anchor",
            "b_parent_choice": fmt(no_sh0es),
            "required_b_response_no_sh0es": fmt(0.0),
            "required_b_response_sh0es": fmt(split),
            "diagnosis": "matches low-pressure branch but needs unsourced SH0ES response",
            "status": "blocked_without_independent_q_B",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "ledger_id": "BS857_1_midpoint_parent",
            "b_parent_choice": fmt(midpoint),
            "required_b_response_no_sh0es": fmt(no_sh0es - midpoint),
            "required_b_response_sh0es": fmt(sh0es - midpoint),
            "diagnosis": "symmetrizes branch pressure but both responses are target-derived",
            "status": "blocked_without_independent_q_B",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "ledger_id": "BS857_2_sh0es_anchor",
            "b_parent_choice": fmt(sh0es),
            "required_b_response_no_sh0es": fmt(no_sh0es - sh0es),
            "required_b_response_sh0es": fmt(0.0),
            "diagnosis": "matches local-H0-pressure branch but needs unsourced no-SH0ES response",
            "status": "blocked_without_independent_q_B",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "ledger_id": "BS857_3_response_zero_default",
            "b_parent_choice": "single_shared_b_parent_to_be_stress_tested",
            "required_b_response_no_sh0es": fmt(0.0),
            "required_b_response_sh0es": fmt(0.0),
            "diagnosis": "only route that does not smuggle a branch response into the model",
            "status": "selected_for_858_parent_only_stress_test",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
    ]


def response_gate_rows(generated_utc: str) -> list[dict[str, object]]:
    return [
        {
            "gate_id": "RG857_0_independent_q_B",
            "requirement": "q_B must be measured, derived, or otherwise signed independently of the fitted target split",
            "failure_mode": "MISSING_INDEPENDENT_SOURCE or solved-from-target amplitude",
            "action_if_failed": "set b_R[B]=0",
            "status": "failed_currently",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "gate_id": "RG857_1_response_coefficient",
            "requirement": "C_R must come from a parent projection, local geometry, or stated likelihood-response map",
            "failure_mode": "free coefficient tuned to match SH0ES/no-SH0ES split",
            "action_if_failed": "response channel remains closure-only",
            "status": "missing_currently",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "gate_id": "RG857_2_projected_offset_rejection",
            "requirement": "global SN calibration offset cannot source b_R after nuisance projection removes it",
            "failure_mode": "using MU_SH0ES minus m_b_corr as physical memory amplitude",
            "action_if_failed": "reject as source",
            "status": "passed_rejection",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "gate_id": "RG857_3_response_pre_registration",
            "requirement": "response vector and amplitude must be recorded before any scoring run that uses them",
            "failure_mode": "post-hoc response chosen after seeing BIC",
            "action_if_failed": "score as exploratory nonclaim only",
            "status": "required_next",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
    ]


def bao_conservation_guard_rows(generated_utc: str) -> list[dict[str, object]]:
    return [
        {
            "guard_id": "BCG857_0_bao_residual_split",
            "guard": "SN improvement and BAO penalty must be reported separately",
            "mathematical_check": "Delta chi2_total = Delta chi2_SN + Delta chi2_BAO + Delta chi2_priors",
            "status": "required_for_858",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "guard_id": "BCG857_1_no_hidden_bao_breakage",
            "guard": "response or parent memory cannot be preferred if it wins SN by silently breaking BAO",
            "mathematical_check": "BAO residual table and max-pull ledger are mandatory",
            "status": "required_for_858",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "guard_id": "BCG857_2_conservation_branch",
            "guard": "if the response is physical, the parent action must conserve the combined stress-energy",
            "mathematical_check": "nabla_mu(T_parent^{mu nu}+T_response^{mu nu})=0",
            "status": "unsigned_so_response_not_physical_claim",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "guard_id": "BCG857_3_likelihood_projection_branch",
            "guard": "if response is merely observational projection, it cannot be advertised as field-theory dynamics",
            "mathematical_check": "response rows labelled likelihood_level_only",
            "status": "required_if_response_reintroduced",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
    ]


def acceptance_test_rows(generated_utc: str) -> list[dict[str, object]]:
    return [
        {
            "test_id": "AT857_0_shared_parent",
            "test": "same b_P and A_P used in no_SH0ES and SH0ES branches",
            "pass_condition": "no branch-specific b_mem parameter appears in the scored model",
            "current_status": "ready_for_858",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "test_id": "AT857_1_response_zero_default",
            "test": "without independent q_B, b_R[B] is forced to zero",
            "pass_condition": "all response rows are zero or explicitly invalid for claim",
            "current_status": "ready_for_858",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "test_id": "AT857_2_null_control",
            "test": "b_P=0 reproduces fitted baseline/null-control parity",
            "pass_condition": "MTS null row tracks baseline within numerical tolerance",
            "current_status": "required_for_858",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "test_id": "AT857_3_SN_BAO_split",
            "test": "parent-only memory score reports SN and BAO deltas separately",
            "pass_condition": "no total BIC statement without sector ledger",
            "current_status": "required_for_858",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "test_id": "AT857_4_parent_survival",
            "test": "shared parent amplitude remains competitive when response is zero",
            "pass_condition": "858 determines whether signal survives without branch-specific amplitude",
            "current_status": "deferred_to_858",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
    ]


def route_choice_rows(generated_utc: str) -> list[dict[str, object]]:
    return [
        {
            "route_id": "RC857_0_selected",
            "route": "branch_invariant_parent_only_memory_stress_test",
            "status": "selected",
            "reason": "the response source is not signed, so the honest next test is b_R=0 with one shared parent amplitude",
            "include": "shared b_P, b_R=0, null control, SN/BAO split, no branch b_mem fitting",
            "exclude": "target-derived response amplitude, support claim, public evidence",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "route_id": "RC857_1_deferred",
            "route": "independent_response_source_reintroduction",
            "status": "deferred",
            "reason": "can reopen only if q_B and C_R are sourced before scoring",
            "include": "pre-registered response vector and conservation/likelihood label",
            "exclude": "post-hoc split matching",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
    ]


def claim_guard_rows(generated_utc: str) -> list[dict[str, object]]:
    return [
        {
            "guard_id": "CG857_0_no_repaired_score",
            "claim": "the memory projection has passed a repaired fit",
            "status": "forbidden",
            "reason": "857 writes the contract only; no repaired model has been scored",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "guard_id": "CG857_1_no_response_physics",
            "claim": "branch response is physical field dynamics",
            "status": "forbidden",
            "reason": "q_B, C_R, and conservation accounting are unsigned",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "guard_id": "CG857_2_no_branch_knob",
            "claim": "separate branch b_mem values are acceptable evidence",
            "status": "forbidden",
            "reason": "separate b_eff values are diagnostic targets, not primitive parameters",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "guard_id": "CG857_3_allowed_contract",
            "claim": "a private nonclaim contract now blocks branch-specific memory smuggling",
            "status": "allowed_private_nonclaim",
            "reason": "the next scoring target is forced into a stricter parent-only test",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
    ]


def decision_rows(generated_utc: str) -> list[dict[str, object]]:
    return [
        {
            "decision_id": "D857_0",
            "finding": "branch-invariant memory projection contract is now explicit",
            "reason": "b_eff is demoted to diagnostic readout unless it decomposes into b_P plus sourced response",
            "status": CLAIM_CEILING,
            "claim_allowed": "false",
            "next_target": NEXT_TARGET,
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "decision_id": "D857_1",
            "finding": "response channel is set to zero until independently sourced",
            "reason": "856 showed the available calibration/local-response candidates fail or are unsourced",
            "status": CLAIM_CEILING,
            "claim_allowed": "false",
            "next_target": NEXT_TARGET,
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "decision_id": "D857_2",
            "finding": "next fair test is parent-only shared-amplitude stress",
            "reason": "if the lead survives without branch amplitude freedom, the MTS cosmology route becomes much cleaner",
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
            "objective": "score the strict parent-only memory model with one shared b_P and b_R=0",
            "include": "null parity, no_SH0ES and SH0ES branches, SN/BAO sector deltas, BIC/AIC, no branch-specific b_mem",
            "exclude": "response amplitude, target inversion, public claim, formalization-workbench edits",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        }
    ]


def nonclaim_summary_rows(generated_utc: str) -> list[dict[str, object]]:
    return [
        {
            "status": STATUS,
            "claim_ceiling": CLAIM_CEILING,
            "what_changed": "converted the branch split into a strict parent-plus-response contract",
            "selected_route": "parent_only_shared_memory_stress_test",
            "what_is_not_claimed": "support, repaired fit, response physics, local-GR pass, public evidence",
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
    projection_contract: list[dict[str, object]],
    channels: list[dict[str, object]],
    split_ledger: list[dict[str, object]],
    response_gate: list[dict[str, object]],
    bao_conservation: list[dict[str, object]],
    acceptance_tests: list[dict[str, object]],
    routes: list[dict[str, object]],
    guards: list[dict[str, object]],
    decisions: list[dict[str, object]],
    next_targets: list[dict[str, object]],
    nonclaim: list[dict[str, object]],
) -> list[dict[str, object]]:
    prior_clean, prior_detail = validation_file_clean(PRIOR_VALIDATION_PATH)
    formalization_count = formalization_workbench_modified_count()
    source_ok = all(row["exists"] == "true" and row["needle_check"] == "pass" for row in source_rows)
    contract_ok = any("b_P A_P" in row["mathematical_form"] for row in projection_contract) and any("q_B=0" in row["mathematical_form"] for row in projection_contract)
    no_branch_knob = any(row["channel_id"] == "CH857_2_effective_readout" and "diagnostic_only" in row["current_status"] for row in channels)
    split_blocked = any(row["status"] == "blocked_without_independent_q_B" for row in split_ledger) and any(row["status"] == "selected_for_858_parent_only_stress_test" for row in split_ledger)
    response_zero = any(row["gate_id"] == "RG857_0_independent_q_B" and row["action_if_failed"] == "set b_R[B]=0" for row in response_gate)
    bao_guard_ok = any(row["guard_id"] == "BCG857_0_bao_residual_split" for row in bao_conservation) and any(row["guard_id"] == "BCG857_2_conservation_branch" for row in bao_conservation)
    acceptance_ok = len(acceptance_tests) == 5 and any(row["test_id"] == "AT857_4_parent_survival" for row in acceptance_tests)
    route_ok = any(row["route_id"] == "RC857_0_selected" and row["route"] == "branch_invariant_parent_only_memory_stress_test" for row in routes)
    no_claim = not any(row["claim_allowed"] == "true" for row in decisions)
    nonclaim_ok = all_valid_for_claim_false([source_rows, projection_contract, channels, split_ledger, response_gate, bao_conservation, acceptance_tests, routes, guards, decisions, next_targets, nonclaim])
    next_selected = bool(next_targets) and next_targets[0]["next_target"] == NEXT_TARGET
    return [
        {"check_id": "V857_0_sources_exist_and_needles", "result": "pass" if source_ok else "fail", "detail": "all source paths exist and needles are present" if source_ok else "source register has missing path or needle"},
        {"check_id": "V857_1_prior_856_clean", "result": "pass" if prior_clean else "fail", "detail": prior_detail},
        {"check_id": "V857_2_projection_contract_has_parent_and_response", "result": "pass" if contract_ok else "fail", "detail": "contract contains b_P parent channel and zero-response limit"},
        {"check_id": "V857_3_effective_bmem_demoted_to_diagnostic", "result": "pass" if no_branch_knob else "fail", "detail": "b_eff is not a primitive branch parameter"},
        {"check_id": "V857_4_branch_split_not_claimed", "result": "pass" if split_blocked else "fail", "detail": "target-derived responses remain blocked and response-zero route selected"},
        {"check_id": "V857_5_response_gate_sets_missing_source_to_zero", "result": "pass" if response_zero else "fail", "detail": "missing independent q_B forces b_R=0"},
        {"check_id": "V857_6_bao_and_conservation_guards_present", "result": "pass" if bao_guard_ok else "fail", "detail": "BAO split and conservation guards recorded"},
        {"check_id": "V857_7_acceptance_tests_ready", "result": "pass" if acceptance_ok else "fail", "detail": "strict 858 acceptance tests recorded"},
        {"check_id": "V857_8_route_selected", "result": "pass" if route_ok else "fail", "detail": "parent-only shared-memory stress test selected"},
        {"check_id": "V857_9_claim_allowed_false", "result": "pass" if no_claim else "fail", "detail": "decision rows keep claim_allowed=false"},
        {"check_id": "V857_10_all_rows_nonclaim", "result": "pass" if nonclaim_ok else "fail", "detail": "all generated rows valid_for_claim=false"},
        {"check_id": "V857_11_next_target_selected", "result": "pass" if next_selected else "fail", "detail": NEXT_TARGET},
        {"check_id": "V857_12_formalization_workbench_untouched", "result": "pass" if formalization_count == 0 else "fail", "detail": f"formalization_changed_after_cutoff={formalization_count}"},
        {"check_id": "V857_13_validation_rows_ready", "result": "pass", "detail": "validation table constructed"},
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
    projection_contract: list[dict[str, object]],
    channels: list[dict[str, object]],
    split_ledger: list[dict[str, object]],
    response_gate: list[dict[str, object]],
    bao_conservation: list[dict[str, object]],
    acceptance_tests: list[dict[str, object]],
    routes: list[dict[str, object]],
    guards: list[dict[str, object]],
    decisions: list[dict[str, object]],
    next_targets: list[dict[str, object]],
    nonclaim: list[dict[str, object]],
    validation: list[dict[str, object]],
) -> None:
    sections = [
        "# 857 - Y5 R10 Branch-Invariant Memory Projection Repair Contract",
        "",
        "Current result: **the branch split is now fenced behind a parent-plus-response contract**. The allowed cosmology object is not a free branch-specific `b_mem`; it is a branch-invariant parent memory channel plus an optional response channel that is forced to zero unless independently sourced before scoring.",
        "",
        "## Non-Claim Summary",
        "",
        csv_table(nonclaim, ["status", "claim_ceiling", "what_changed", "selected_route", "what_is_not_claimed", "next_target", "valid_for_claim"]),
        "",
        "## Projection Contract",
        "",
        csv_table(projection_contract, ["contract_id", "clause", "mathematical_form", "acceptance_gate", "status", "valid_for_claim"]),
        "",
        "## Channel Decomposition",
        "",
        csv_table(channels, ["channel_id", "object", "meaning", "allowed_source", "forbidden_source", "current_status", "valid_for_claim"]),
        "",
        "## Branch Split Response Ledger",
        "",
        csv_table(split_ledger, ["ledger_id", "b_parent_choice", "required_b_response_no_sh0es", "required_b_response_sh0es", "diagnosis", "status", "valid_for_claim"]),
        "",
        "## Response Source Gate",
        "",
        csv_table(response_gate, ["gate_id", "requirement", "failure_mode", "action_if_failed", "status", "valid_for_claim"]),
        "",
        "## BAO And Conservation Guard",
        "",
        csv_table(bao_conservation, ["guard_id", "guard", "mathematical_check", "status", "valid_for_claim"]),
        "",
        "## Acceptance Tests",
        "",
        csv_table(acceptance_tests, ["test_id", "test", "pass_condition", "current_status", "valid_for_claim"]),
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
    projection_contract = projection_contract_rows(generated_utc)
    channels = channel_decomposition_rows(generated_utc)
    split_ledger = branch_split_ledger_rows(generated_utc)
    response_gate = response_gate_rows(generated_utc)
    bao_conservation = bao_conservation_guard_rows(generated_utc)
    acceptance_tests = acceptance_test_rows(generated_utc)
    routes = route_choice_rows(generated_utc)
    guards = claim_guard_rows(generated_utc)
    decisions = decision_rows(generated_utc)
    next_targets = next_target_rows(generated_utc)
    nonclaim = nonclaim_summary_rows(generated_utc)
    validation = validation_rows(
        source_rows,
        projection_contract,
        channels,
        split_ledger,
        response_gate,
        bao_conservation,
        acceptance_tests,
        routes,
        guards,
        decisions,
        next_targets,
        nonclaim,
    )

    write_csv(SOURCE_REGISTER_PATH, source_rows, ["source_id", "path", "exists", "needle_check", "role", "valid_for_claim", "generated_utc"])
    write_csv(PROJECTION_CONTRACT_PATH, projection_contract, ["contract_id", "clause", "mathematical_form", "acceptance_gate", "status", "valid_for_claim", "generated_utc"])
    write_csv(CHANNEL_DECOMPOSITION_PATH, channels, ["channel_id", "object", "meaning", "allowed_source", "forbidden_source", "current_status", "valid_for_claim", "generated_utc"])
    write_csv(BRANCH_SPLIT_LEDGER_PATH, split_ledger, ["ledger_id", "b_parent_choice", "required_b_response_no_sh0es", "required_b_response_sh0es", "diagnosis", "status", "valid_for_claim", "generated_utc"])
    write_csv(RESPONSE_GATE_PATH, response_gate, ["gate_id", "requirement", "failure_mode", "action_if_failed", "status", "valid_for_claim", "generated_utc"])
    write_csv(BAO_CONSERVATION_GUARD_PATH, bao_conservation, ["guard_id", "guard", "mathematical_check", "status", "valid_for_claim", "generated_utc"])
    write_csv(ACCEPTANCE_TEST_PATH, acceptance_tests, ["test_id", "test", "pass_condition", "current_status", "valid_for_claim", "generated_utc"])
    write_csv(ROUTE_CHOICE_PATH, routes, ["route_id", "route", "status", "reason", "include", "exclude", "valid_for_claim", "generated_utc"])
    write_csv(CLAIM_GUARD_PATH, guards, ["guard_id", "claim", "status", "reason", "valid_for_claim", "generated_utc"])
    write_csv(DECISION_PATH, decisions, ["decision_id", "finding", "reason", "status", "claim_allowed", "next_target", "valid_for_claim", "generated_utc"])
    write_csv(NEXT_TARGET_PATH, next_targets, ["next_target", "objective", "include", "exclude", "valid_for_claim", "generated_utc"])
    write_csv(NONCLAIM_SUMMARY_PATH, nonclaim, ["status", "claim_ceiling", "what_changed", "selected_route", "what_is_not_claimed", "next_target", "valid_for_claim", "generated_utc"])
    write_csv(VALIDATION_PATH, validation, ["check_id", "result", "detail"])
    write_document(source_rows, projection_contract, channels, split_ledger, response_gate, bao_conservation, acceptance_tests, routes, guards, decisions, next_targets, nonclaim, validation)

    print(f"wrote={OUTPUT_DOC}")
    print(f"wrote={VALIDATION_PATH}")
    print(f"status={STATUS}")
    print(f"claim_ceiling={CLAIM_CEILING}")
    print(f"next_target={NEXT_TARGET}")


if __name__ == "__main__":
    main()

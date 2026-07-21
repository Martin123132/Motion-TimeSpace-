from __future__ import annotations

import csv
import subprocess
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[2]
POST = ROOT / "post-checkpoint-work"
FORMAL = ROOT / "formalization-workbench"
SOURCE_DIR = POST / "source-intake" / "mts_residuals"

CHECKPOINT = "4630"
CLAIM_ID = "L-472"
BRANCH_ID = "MTS_R2FR_Y5_PARENT_ACTION_CONTRACT_4630"
MARKER = "PPC4161_CO_NORMALIZED_GAP_AND_SOURCE_COUPLING_PARENT_ACTION_4630"
PACKET_MARKER = "PPC4161_PACKET_PARENT_ACTION_CONTRACT_4630"
DECISION = "PARENT_ACTION_CONTRACT_AND_CONDITIONAL_LOCAL_GR_THEOREM_NONCLAIM"
NEXT_TARGET = "4631-Y5-R2FR-branch-extremum-symmetry-or-parent-coefficient-fill.md"

DOC_PATH = POST / "4630-Y5-R2FR-co-normalized-gap-and-source-coupling-parent-action.md"
FORMAL_PATH = FORMAL / "646-PPC4161-co-normalized-gap-and-source-coupling-parent-action.md"
SPINE_PATH = FORMAL / "07-unification-spine.md"
PACKET_PATH = FORMAL / "180-PPC4161-private-local-packet-integration.md"
CLAIMS_PATH = FORMAL / "02-claims-register.csv"

SOURCE_REGISTER = SOURCE_DIR / "P8_Y5_R2FR_4630_SOURCE_REGISTER.csv"
PARENT_ACTION_CSV = SOURCE_DIR / "P8_Y5_R2FR_4630_PARENT_ACTION_CONTRACT_ROWS.csv"
VARIATION_CSV = SOURCE_DIR / "P8_Y5_R2FR_4630_VARIATION_DERIVATION_ROWS.csv"
INVARIANT_CSV = SOURCE_DIR / "P8_Y5_R2FR_4630_INVARIANT_ALPHA_ROWS.csv"
LOCAL_GR_CSV = SOURCE_DIR / "P8_Y5_R2FR_4630_CONDITIONAL_LOCAL_GR_THEOREM_ROWS.csv"
EVAL_CSV = SOURCE_DIR / "P8_Y5_R2FR_4630_PARENT_ACTION_EVALUATION_ROWS.csv"
CONTROL_CSV = SOURCE_DIR / "P8_Y5_R2FR_4630_CONTROL_ROWS.csv"
BLOCKERS_CSV = SOURCE_DIR / "P8_Y5_R2FR_4630_CLAIM_BLOCKERS.csv"
PROMOTION_CSV = SOURCE_DIR / "P8_Y5_R2FR_4630_PROMOTION_GATES.csv"
DECISION_CSV = SOURCE_DIR / "P8_Y5_R2FR_4630_DECISION.csv"
STATUS_CSV = SOURCE_DIR / "P8_Y5_R2FR_4630_STATUS.csv"
NEXT_CSV = SOURCE_DIR / "P8_Y5_R2FR_4630_NEXT_TARGET.csv"
VALIDATION_CSV = SOURCE_DIR / "P8_Y5_BRR545_4630_VALIDATION.csv"

CSV_4629_NEXT = SOURCE_DIR / "P8_Y5_R2FR_4629_NEXT_TARGET.csv"
CSV_4629_VALIDATION = SOURCE_DIR / "P8_Y5_BRR545_4629_VALIDATION.csv"
CSV_4629_CANONICAL = SOURCE_DIR / "P8_Y5_R2FR_4629_CANONICAL_NORMALIZATION_ROWS.csv"
CSV_4629_SMOKE = SOURCE_DIR / "P8_Y5_R2FR_4629_FIRST_ANCHOR_SMOKE_RUNNER_RESULTS.csv"
CSV_4628_HESSIAN = SOURCE_DIR / "P8_Y5_R2FR_4628_PARENT_HESSIAN_ROWS.csv"
CSV_4627_OWNER = SOURCE_DIR / "P8_Y5_R2FR_4627_BETAT_OWNER_THEOREM_ROWS.csv"
CSV_4627_ZERO = SOURCE_DIR / "P8_Y5_R2FR_4627_BETAT_QEFF_ZERO_ROUTES.csv"
CSV_4621_IDENTITY = SOURCE_DIR / "P8_Y5_R2FR_4621_MEMORY_POSITIVE_OPERATOR_IDENTITY.csv"

PUBLIC_STAGE = Path("D:/Users/ollet/Desktop/Motion-TimeSpace-public-stage")
BACKUP_REPO = Path("D:/Users/ollet/Desktop/laptop-back-up-")


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace") if path.exists() else ""


def write_text(path: Path, body: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(body, encoding="utf-8")


def read_csv(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fieldnames: list[str] = []
    for row in rows:
        for key in row:
            if key not in fieldnames:
                fieldnames.append(key)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow({key: row.get(key, "") for key in fieldnames})


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
        lines.append("| " + " | ".join(str(row.get(header, "")).replace("\n", "<br>") for header in headers) + " |")
    return "\n".join(lines)


def line_of(path: Path, needle: str) -> int:
    if not path.exists() or not needle:
        return 0
    for number, line in enumerate(read_text(path).splitlines(), start=1):
        if needle in line:
            return number
    return 0


def append_once(path: Path, marker: str, block: str) -> None:
    text = read_text(path)
    if marker in text:
        return
    suffix = "\n" if text.endswith("\n") or not text else "\n\n"
    write_text(path, text + suffix + block.strip() + "\n")


def git_clean(path: Path) -> bool:
    if not path.exists() or not (path / ".git").exists():
        return True
    result = subprocess.run(["git", "-C", str(path), "status", "--porcelain"], text=True, capture_output=True, check=False)
    return result.returncode == 0 and result.stdout.strip() == ""


def any_claim_true(rows: list[dict[str, Any]]) -> bool:
    return any(str(value).lower() == "true" for row in rows for key, value in row.items() if key in {"valid_for_claim", "claim_allowed"})


def source_rows(now: str) -> list[dict[str, Any]]:
    specs = [
        ("SRC4630_00_4629_next", CSV_4629_NEXT, "4630-Y5-R2FR-co-normalized-gap-and-source-coupling-parent-action.md", "4629 selected parent action target."),
        ("SRC4630_01_4629_validation", CSV_4629_VALIDATION, "VAL4629_OVERALL", "4629 validation."),
        ("SRC4630_02_4629_co_norm", CSV_4629_CANONICAL, "CAN4629_1_source_coupling_co_normalization", "4629 co-normalization guard."),
        ("SRC4630_03_4629_fail_closed", CSV_4629_SMOKE, "SMK4629_0_current_placeholder", "4629 live branch fail-closed row."),
        ("SRC4630_04_4629_exact_zero", CSV_4629_SMOKE, "SMK4629_1_exact_zero_qeff", "4629 exact-zero algebra row."),
        ("SRC4630_05_4628_hessian", CSV_4628_HESSIAN, "HES4628_1_parent_hessian_definitions", "4628 parent Hessian definitions."),
        ("SRC4630_06_4627_beta_owner", CSV_4627_OWNER, "BTO4627_0_matter_scale_owner", "4627 beta_T owner row."),
        ("SRC4630_07_4627_extremum", CSV_4627_ZERO, "BTZ4627_1_branch_extremum", "4627 branch extremum route."),
        ("SRC4630_08_4621_nohair", CSV_4621_IDENTITY, "MPI4621_2_nohair_zero", "4621 local no-hair condition."),
    ]
    rows: list[dict[str, Any]] = []
    for source_id, path, needle, role in specs:
        text = read_text(path)
        rows.append({
            "checkpoint": CHECKPOINT,
            "source_id": source_id,
            "path": str(path),
            "path_exists": path.exists(),
            "needle": needle,
            "needle_found": needle in text,
            "line": line_of(path, needle),
            "role": role,
            "valid_for_claim": False,
            "timestamp_utc": now,
        })
    return rows


def parent_action_rows(now: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "action_id": "PACT4630_0_minimal_parent_contract",
            "object": "S_parent[g,m,Psi]",
            "contract": "S_grav[g] + int sqrt(-g)[-1/2 Z(m)(partial m)^2 - V_eff(m)] + S_matter[A_m(m)^2 g, Psi] plus explicitly owned nontrace couplings only.",
            "owns": "Z_mem, M2_mem, beta_A, Q_eff, lambda_mem and alpha_AB in one normalization",
            "status": "CONTRACT_WRITTEN_PARENT_COEFFICIENTS_MISSING",
            "valid_for_claim": False,
            "claim_allowed": False,
            "timestamp_utc": now,
        },
        {
            "checkpoint": CHECKPOINT,
            "action_id": "PACT4630_1_local_branch_expansion",
            "object": "m=m0+delta_m",
            "contract": "V_eff'(m0)=0, Z_mem=Z(m0)>0, M2_mem=V_eff''(m0)+environment Hessian >0, beta_A=partial_m ln A_A|m0.",
            "owns": "positive local gap and matter source derivative",
            "status": "EXACT_FORMAL_EXPANSION_CONDITIONAL",
            "valid_for_claim": False,
            "claim_allowed": False,
            "timestamp_utc": now,
        },
        {
            "checkpoint": CHECKPOINT,
            "action_id": "PACT4630_2_extremum_local_GR_route",
            "object": "A_m(m)",
            "contract": "A_m(m)=A0[1+1/2 a2 (m-m0)^2+O((m-m0)^3)] or a parent symmetry forbids the linear term.",
            "owns": "beta_A=0 at first order without setting the field by hand",
            "status": "BEST_DERIVE_ROUTE_UNSIGNED",
            "valid_for_claim": False,
            "claim_allowed": False,
            "timestamp_utc": now,
        },
        {
            "checkpoint": CHECKPOINT,
            "action_id": "PACT4630_3_metric_GR_recovery",
            "object": "S_grav[g]",
            "contract": "Metric sector must reduce locally to Einstein-Hilbert with effective Newton normalization G_N plus allowed cosmological/background constant.",
            "owns": "GR/Newton metric limit; G_N may be measured unless a deeper MTS parent derives the Planck coefficient",
            "status": "METRIC_PARENT_COEFFICIENT_STILL_TO_CONNECT",
            "valid_for_claim": False,
            "claim_allowed": False,
            "timestamp_utc": now,
        },
    ]


def variation_rows(now: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "variation_id": "VAR4630_0_memory_euler_lagrange",
            "starting_point": "S_m^(2)=1/2 int mu[Z_mem (partial delta_m)^2 + M2_mem delta_m^2] - int mu J_mem delta_m",
            "derived_equation": "[-nabla_i(Z_mem nabla^i)+M2_mem] delta_m = J_mem",
            "meaning": "same parent action supplies both the gap operator and the source term",
            "status": "DERIVED_CONDITIONAL",
            "valid_for_claim": False,
            "claim_allowed": False,
            "timestamp_utc": now,
        },
        {
            "checkpoint": CHECKPOINT,
            "variation_id": "VAR4630_1_trace_source_from_matter_scale",
            "starting_point": "S_matter[A_m(m)^2 g,Psi]",
            "derived_equation": "J_mem = beta_T T_obs + beta_EM F^2 + beta_hidden J_hidden + boundary/matching terms",
            "meaning": "beta_T is partial_m ln A_m at the selected branch; it is not a fit knob",
            "status": "DERIVED_SOURCE_OWNER_CONDITIONAL",
            "valid_for_claim": False,
            "claim_allowed": False,
            "timestamp_utc": now,
        },
        {
            "checkpoint": CHECKPOINT,
            "variation_id": "VAR4630_2_canonical_memory_field",
            "starting_point": "phi=sqrt(Z_mem) delta_m",
            "derived_equation": "[-nabla^2 + M2_mem/Z_mem] phi = J_mem/sqrt(Z_mem)",
            "meaning": "m_gap^2 and source strength are co-normalized; rescaling m cannot change physics",
            "status": "DERIVED_INVARIANT_RATIO",
            "valid_for_claim": False,
            "claim_allowed": False,
            "timestamp_utc": now,
        },
        {
            "checkpoint": CHECKPOINT,
            "variation_id": "VAR4630_3_point_body_yukawa",
            "starting_point": "body A has beta_A=partial_m ln M_A|m0 and scalar source q_A=beta_A M_A/sqrt(Z_mem)",
            "derived_equation": "V_phi(r)=-q_A q_B exp(-r/lambda_mem)/(4*pi r); alpha_AB=C_N beta_A beta_B/Z_mem",
            "meaning": "C_N is fixed by the Newtonian/Planck normalization convention; the invariant dependence is beta_A beta_B/Z_mem",
            "status": "DERIVED_UP_TO_GRAVITATIONAL_NORMALIZATION_CONSTANT",
            "valid_for_claim": False,
            "claim_allowed": False,
            "timestamp_utc": now,
        },
    ]


def invariant_rows(now: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "invariant_id": "INV4630_0_range_invariant",
            "quantity": "lambda_mem",
            "formula": "lambda_mem=sqrt(Z_mem/M2_mem)",
            "invariant_under": "m -> c m rescales Z_mem and M2_mem together",
            "claim_status": "needs parent-owned ratio",
            "valid_for_claim": False,
            "claim_allowed": False,
            "timestamp_utc": now,
        },
        {
            "checkpoint": CHECKPOINT,
            "invariant_id": "INV4630_1_amplitude_invariant",
            "quantity": "alpha_AB",
            "formula": "alpha_AB=C_N beta_A beta_B/Z_mem or equivalent Q_eff^2/Z_mem body normalization",
            "invariant_under": "m -> c m if beta_A and Z_mem are transformed from the same parent action",
            "claim_status": "needs parent-owned beta_A,beta_B,Z_mem and C_N convention",
            "valid_for_claim": False,
            "claim_allowed": False,
            "timestamp_utc": now,
        },
        {
            "checkpoint": CHECKPOINT,
            "invariant_id": "INV4630_2_exact_zero_invariant",
            "quantity": "alpha_AB=0",
            "formula": "beta_A=0 or beta_B=0 or Q_eff=0 by parent theorem",
            "invariant_under": "field normalization",
            "claim_status": "best low-scrutiny route if branch extremum/symmetry is signed",
            "valid_for_claim": False,
            "claim_allowed": False,
            "timestamp_utc": now,
        },
    ]


def local_gr_rows(now: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "theorem_id": "TGR4630_0_conditional_statement",
            "assumptions": "Z_mem>0, M2_mem>0, beta_visible=0 by branch extremum/symmetry, no explicit unsourced EM/hidden coupling, and zero incoming boundary scalar flux.",
            "derivation": "The source term J_mem vanishes to first order, so the positive elliptic operator has homogeneous exterior data; by 4621 no-hair, delta_m=0 locally.",
            "result": "No first-order memory fifth force; local motion follows the metric sector.",
            "status": "CONDITIONAL_LOCAL_GR_LIMIT_THEOREM_WRITTEN",
            "valid_for_claim": False,
            "claim_allowed": False,
            "timestamp_utc": now,
        },
        {
            "checkpoint": CHECKPOINT,
            "theorem_id": "TGR4630_1_newtonian_limit",
            "assumptions": "metric sector reduces to Einstein-Hilbert locally with measured G_N and weak-field slow-motion sources",
            "derivation": "With delta_m=0 at first order, the remaining weak-field metric equations are the usual Poisson/Newton limit of the metric sector.",
            "result": "Newtonian mechanics is recovered as GR recovers Newton, not as a separate MTS force law.",
            "status": "CONDITIONAL_ON_METRIC_PARENT_GR_LIMIT",
            "valid_for_claim": False,
            "claim_allowed": False,
            "timestamp_utc": now,
        },
        {
            "checkpoint": CHECKPOINT,
            "theorem_id": "TGR4630_2_ppn_residual",
            "assumptions": "beta_visible=0 exactly at first order and boundary/source terms vanish",
            "derivation": "alpha_AB=0 removes scalar Yukawa and scalar PPN residuals at linear order; surviving effects begin at quadratic/higher-gradient order.",
            "result": "PPN residual vector is zero at first order, with explicit higher-order remainder rather than closure.",
            "status": "CONDITIONAL_FIRST_ORDER_PPN_SILENCE",
            "valid_for_claim": False,
            "claim_allowed": False,
            "timestamp_utc": now,
        },
        {
            "checkpoint": CHECKPOINT,
            "theorem_id": "TGR4630_3_maxwell_em_stress",
            "assumptions": "Maxwell sector is minimally/universally metric-coupled in four dimensions and explicit F^2 or F*F memory couplings are forbidden or parent-owned.",
            "derivation": "Classical Maxwell stress is trace-free under conformal metric coupling, so trace-only beta_T coupling does not source memory at linear order; explicit EM channels must be handled separately.",
            "result": "Maxwell/EM stress can be compatible with the local-GR branch if nontrace EM couplings are selection-rule controlled.",
            "status": "CONDITIONAL_EM_COMPATIBILITY_NOT_FULL_EM_UNIFICATION",
            "valid_for_claim": False,
            "claim_allowed": False,
            "timestamp_utc": now,
        },
    ]


def evaluation_rows(now: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "eval_id": "EVAL4630_0_live_branch",
            "case": "current generated live branch",
            "inputs": "Z_mem=MISSING, M2_mem=MISSING, beta_A=MISSING, C_N=MISSING",
            "result": "FAIL_CLOSED_PARENT_ACTION_NUMBERS_MISSING",
            "meaning": "no empirical/local-GR claim",
            "valid_for_claim": False,
            "claim_allowed": False,
            "timestamp_utc": now,
        },
        {
            "checkpoint": CHECKPOINT,
            "eval_id": "EVAL4630_1_extremum_positive_gap",
            "case": "A_m'(m0)=0, Z_mem>0, M2_mem>0, boundary scalar flux=0",
            "inputs": "symbolic theorem branch",
            "result": "CONDITIONAL_FIRST_ORDER_LOCAL_GR_RECOVERY",
            "meaning": "this is the best derivation route to pursue; still needs parent signature",
            "valid_for_claim": False,
            "claim_allowed": False,
            "timestamp_utc": now,
        },
        {
            "checkpoint": CHECKPOINT,
            "eval_id": "EVAL4630_2_positive_gap_nonzero_beta",
            "case": "Z_mem>0, M2_mem>0, beta_A beta_B nonzero",
            "inputs": "alpha_AB=C_N beta_A beta_B/Z_mem",
            "result": "BOUND_ROUTE_REQUIRED",
            "meaning": "must pass R10/WEP/PPN/orbital bounds; not as clean as exact-zero",
            "valid_for_claim": False,
            "claim_allowed": False,
            "timestamp_utc": now,
        },
        {
            "checkpoint": CHECKPOINT,
            "eval_id": "EVAL4630_3_wrong_normalization",
            "case": "lambda from M2/Z but alpha from independent Q_eff knob",
            "inputs": "mixed normalization",
            "result": "REJECTED_BY_CO_NORMALIZATION_GATE",
            "meaning": "prevents artificial local-GR/R10 pass",
            "valid_for_claim": False,
            "claim_allowed": False,
            "timestamp_utc": now,
        },
    ]


def control_rows(now: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "control_id": "CTL4630_0_no_free_coupling",
            "rule": "beta_A, Q_eff and alpha_AB must come from the same parent action as Z_mem and M2_mem.",
            "violation_blocks_claim": True,
            "timestamp_utc": now,
        },
        {
            "checkpoint": CHECKPOINT,
            "control_id": "CTL4630_1_GN_not_derivation_required_for_limit",
            "rule": "Recovering GR/Newton locally may use measured G_N; deriving G_N is a deeper optional target unless the claim says MTS explains the Planck coefficient.",
            "violation_blocks_claim": False,
            "timestamp_utc": now,
        },
        {
            "checkpoint": CHECKPOINT,
            "control_id": "CTL4630_2_EM_channels_not_silent_by_default",
            "rule": "Trace-free Maxwell stress is silent only for trace/conformal coupling; explicit F^2, F*F or Poynting channels need their own parent selection rule or bound.",
            "violation_blocks_claim": True,
            "timestamp_utc": now,
        },
    ]


def blocker_rows(now: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "blocker_id": "BLK4630_0_parent_coefficients",
            "blocks": "numeric/bound local branch",
            "missing": "same parent action values or exact-zero theorem for Z_mem, M2_mem, beta_A/beta_B and C_N convention",
            "next_action": NEXT_TARGET,
            "valid_for_claim": False,
            "timestamp_utc": now,
        },
        {
            "checkpoint": CHECKPOINT,
            "blocker_id": "BLK4630_1_branch_extremum_signature",
            "blocks": "clean local-GR theorem promotion",
            "missing": "MTS-owned symmetry/extremum proving A_m'(m0)=0 for visible matter on the local branch",
            "next_action": NEXT_TARGET,
            "valid_for_claim": False,
            "timestamp_utc": now,
        },
        {
            "checkpoint": CHECKPOINT,
            "blocker_id": "BLK4630_2_metric_gr_limit",
            "blocks": "full MTS-to-GR reduction",
            "missing": "metric parent action reducing to Einstein-Hilbert with effective G_N and controlled background terms",
            "next_action": "after branch extremum/gap coupling theorem",
            "valid_for_claim": False,
            "timestamp_utc": now,
        },
    ]


def promotion_rows(now: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "gate_id": "PROM4630_0_exact_local_GR",
            "promotion_condition": "Parent action signs Z_mem>0, M2_mem>0, beta_visible=0, no explicit EM/hidden source and zero scalar boundary flux.",
            "current_result": "conditional theorem written; parent signature missing",
            "valid_for_claim": False,
            "claim_allowed": False,
            "timestamp_utc": now,
        },
        {
            "checkpoint": CHECKPOINT,
            "gate_id": "PROM4630_1_bound_route",
            "promotion_condition": "If beta nonzero, co-normalized alpha_AB and lambda_mem pass R10/WEP/PPN/orbital bound rows.",
            "current_result": "blocked numeric parent coefficients missing",
            "valid_for_claim": False,
            "claim_allowed": False,
            "timestamp_utc": now,
        },
        {
            "checkpoint": CHECKPOINT,
            "gate_id": "PROM4630_2_full_GR_reduction",
            "promotion_condition": "Metric sector reduces to Einstein-Hilbert/Newtonian gravity and nonmetric residuals are zero or bounded.",
            "current_result": "blocked metric parent reduction still open",
            "valid_for_claim": False,
            "claim_allowed": False,
            "timestamp_utc": now,
        },
    ]


def decision_rows(now: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "decision_id": "DEC4630_0",
            "decision": DECISION,
            "meaning": "A single parent-action contract now derives the co-normalized gap/source map and gives the clean conditional local-GR route: positive memory gap plus branch-extremum matter coupling makes the first-order memory source vanish, leaving the local metric GR/Newton branch.",
            "status": "NONCLAIM_DERIVATION_ADVANCE",
            "best_route": "try to prove the branch extremum/symmetry A_m'(m0)=0 from MTS structure; otherwise fill co-normalized coefficients and run bounds",
            "next_target": NEXT_TARGET,
            "valid_for_claim": False,
            "claim_allowed": False,
            "timestamp_utc": now,
        }
    ]


def status_rows(now: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "branch_id": BRANCH_ID,
            "status": "PRIVATE_NONCLAIM_DERIVATION_ADVANCE",
            "summary": "parent action contract and conditional local-GR theorem written; next is to sign branch extremum/symmetry or fill parent coefficients",
            "valid_for_claim": False,
            "claim_allowed": False,
            "next_target": NEXT_TARGET,
            "timestamp_utc": now,
        }
    ]


def next_rows(now: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "branch_id": BRANCH_ID,
            "timestamp_utc": now,
            "next_target": NEXT_TARGET,
            "reason": "The cleanest route is now explicit: prove the branch extremum/symmetry that kills beta_visible, or supply co-normalized coefficients for the bound route.",
            "derive_first": "derive A_m'(m0)=0 from MTS branch symmetry/extremum and positive gap",
            "fallback": "fill beta_A,beta_B,Z_mem,M2_mem,C_N and run R10/WEP/PPN bound matrix",
            "valid_for_claim": False,
        }
    ]


def write_doc(now: str, groups: dict[str, list[dict[str, Any]]]) -> None:
    body = f"""# 4630 - Co-normalized Gap And Source Coupling Parent Action

Marker: `{MARKER}`

Branch: `{BRANCH_ID}`

Timestamp: `{now}`

## Result

This checkpoint turns the 4629 co-normalization gate into a parent-action contract and a conditional local-GR theorem.

The minimal local parent structure is:

`S_parent = S_grav[g] + int sqrt(-g)[-1/2 Z(m)(partial m)^2 - V_eff(m)] + S_matter[A_m(m)^2 g, Psi] + owned extra channels`

around `m=m0+delta_m`.

Variation gives:

`[-nabla_i(Z_mem nabla^i)+M2_mem] delta_m = J_mem`

with

`J_mem = beta_T T_obs + beta_EM F^2 + beta_hidden J_hidden + boundary/matching terms`.

Canonical normalization gives:

`phi = sqrt(Z_mem) delta_m`

`[-nabla^2 + M2_mem/Z_mem] phi = J_mem/sqrt(Z_mem)`

so both the range and source amplitude are fixed by the same parent normalization:

`lambda_mem = sqrt(Z_mem/M2_mem)`

`alpha_AB = C_N beta_A beta_B/Z_mem` or the equivalent invariant body-charge form.

## Conditional Local-GR Route

If the local branch has `Z_mem>0`, `M2_mem>0`, zero incoming scalar boundary data, no unsourced explicit EM/hidden channel, and a matter-scale extremum

`A_m(m)=A0[1+1/2 a2 (m-m0)^2+...]`,

then `beta_visible=A_m'(m0)/A_m(m0)=0`.

The first-order memory source vanishes. The exterior equation is homogeneous, and the 4621 positive-operator/no-hair condition gives `delta_m=0` locally. At that order the fifth-force/PPN residual is zero and the remaining local weak-field branch is the metric GR/Newton branch, provided the metric sector reduces to Einstein-Hilbert with measured `G_N`.

This is still nonclaim because the parent extremum/symmetry is not signed yet, but it is now a real derivation target rather than a closure axiom.

## Source Register

{markdown_table(groups["sources"])}

## Parent Action Contract

{markdown_table(groups["parent"])}

## Variation Derivation

{markdown_table(groups["variation"])}

## Invariant Alpha Rows

{markdown_table(groups["invariant"])}

## Conditional Local-GR Theorem Rows

{markdown_table(groups["local_gr"])}

## Parent Action Evaluations

{markdown_table(groups["evaluation"])}

## Controls

{markdown_table(groups["controls"])}

## Blockers

{markdown_table(groups["blockers"])}

## Promotion Gates

{markdown_table(groups["promotions"])}

## Decision

{markdown_table(groups["decisions"])}

## Next Target

`{NEXT_TARGET}`
"""
    write_text(DOC_PATH, body)


def write_formal(now: str) -> None:
    body = f"""# 646 - PPC4161 Co-normalized Gap And Source Coupling Parent Action

Marker: `{MARKER}`

Branch: `{BRANCH_ID}`

4630 gives the local parent-action contract:

`S_parent = S_grav[g] + int sqrt(-g)[-1/2 Z(m)(partial m)^2 - V_eff(m)] + S_matter[A_m(m)^2 g,Psi] + owned extra channels`.

The derived co-normalized equations are:

`[-nabla_i(Z_mem nabla^i)+M2_mem] delta_m = J_mem`,

`phi=sqrt(Z_mem) delta_m`,

`lambda_mem=sqrt(Z_mem/M2_mem)`,

`alpha_AB=C_N beta_A beta_B/Z_mem` up to the chosen Newton/Planck convention.

Conditional local-GR theorem: if `Z_mem>0`, `M2_mem>0`, `beta_visible=0` by a parent branch extremum/symmetry, explicit EM/hidden channels are absent or signed silent, and boundary scalar flux is zero, then the first-order source vanishes and the 4621 positive-operator/no-hair condition gives local `delta_m=0`. The remaining weak-field branch is metric GR/Newton if the metric sector has the Einstein-Hilbert local limit.

Next target: `{NEXT_TARGET}`.
"""
    write_text(FORMAL_PATH, body)


def append_integrations() -> None:
    append_once(
        SPINE_PATH,
        MARKER,
        f"""
## PPC4161 Co-normalized Gap And Source Coupling Parent Action 4630

Marker: `{MARKER}`

4630 writes the parent-action contract that co-normalizes `lambda_mem` and `alpha_AB`. It also isolates the cleanest local-GR route: positive memory gap plus a parent-signed branch extremum/symmetry `A_m'(m0)=0` makes the first-order source vanish, so the 4621 no-hair condition gives local `delta_m=0` rather than an assumed plateau.

Next: `{NEXT_TARGET}`.
""",
    )
    append_once(
        PACKET_PATH,
        PACKET_MARKER,
        f"""
## PPC4161 Packet - Parent Action Contract 4630

Marker: `{PACKET_MARKER}`

Local packet update: the branch now has a concrete parent-action theorem target. If MTS can sign the matter-scale extremum and positive gap, local memory is first-order silent and GR/Newton recovery reduces to the metric-sector GR limit. If not, the bound route needs co-normalized `beta_A`, `Z_mem`, `M2_mem`, and `C_N`.

Next: `{NEXT_TARGET}`.
""",
    )
    if CLAIM_ID not in read_text(CLAIMS_PATH):
        with CLAIMS_PATH.open("a", encoding="utf-8", newline="") as handle:
            writer = csv.writer(handle)
            writer.writerow([
                CLAIM_ID,
                "local_gr_derivation",
                "4630 writes the co-normalized parent-action contract and conditional local-GR theorem for the memory branch.",
                "Generated source register, parent action rows, variation derivation, invariant alpha rows, conditional local-GR theorem rows, evaluations, controls, blockers, promotion gates, decision, status, next target and validation.",
                "parent_action_contract_conditional_local_gr_nonclaim",
                NEXT_TARGET,
                "Treating the conditional branch-extremum theorem as already signed by MTS.",
                "local_gr",
                str(DOC_PATH),
                NEXT_TARGET,
                "No local-GR/Newton/PPN pass until the branch extremum/symmetry, positive gap and metric GR limit are parent-signed or the co-normalized bound route passes.",
            ])


def validation_rows(groups: dict[str, list[dict[str, Any]]]) -> list[dict[str, Any]]:
    checks: list[dict[str, Any]] = []

    def add(check_id: str, status: bool, detail: str) -> None:
        checks.append({
            "checkpoint": CHECKPOINT,
            "check_id": check_id,
            "status": "PASS" if status else "FAIL",
            "detail": detail,
            "valid_for_claim": False,
            "claim_allowed": False,
        })

    sources = groups["sources"]
    all_sources = all(row["path_exists"] and row["needle_found"] for row in sources)
    add("VAL4630_00_sources_exist_and_needles_found", all_sources, "all cited paths/needles found" if all_sources else "missing source path or needle")

    csv_paths = [
        SOURCE_REGISTER,
        PARENT_ACTION_CSV,
        VARIATION_CSV,
        INVARIANT_CSV,
        LOCAL_GR_CSV,
        EVAL_CSV,
        CONTROL_CSV,
        BLOCKERS_CSV,
        PROMOTION_CSV,
        DECISION_CSV,
        STATUS_CSV,
        NEXT_CSV,
    ]
    parse_details: list[str] = []
    parse_ok = True
    for path in csv_paths:
        try:
            parse_details.append(f"{path.name}:{len(read_csv(path))}")
        except Exception as exc:
            parse_ok = False
            parse_details.append(f"{path.name}:ERROR:{exc}")
    add("VAL4630_01_csv_parse", parse_ok, ";".join(parse_details))

    variation_text = read_text(VARIATION_CSV)
    add("VAL4630_02_variation_derives_operator", "VAR4630_0_memory_euler_lagrange" in variation_text and "J_mem" in variation_text, "operator/source derivation present")
    add("VAL4630_03_canonical_alpha_invariant", "alpha_AB=C_N beta_A beta_B/Z_mem" in read_text(INVARIANT_CSV), "invariant alpha row present")
    add("VAL4630_04_conditional_local_gr_theorem", "TGR4630_0_conditional_statement" in read_text(LOCAL_GR_CSV), "conditional local-GR theorem row present")
    add("VAL4630_05_live_branch_fails_closed", "FAIL_CLOSED_PARENT_ACTION_NUMBERS_MISSING" in read_text(EVAL_CSV), "live branch remains fail-closed")
    add("VAL4630_06_extremum_route_present", "CONDITIONAL_FIRST_ORDER_LOCAL_GR_RECOVERY" in read_text(EVAL_CSV), "extremum positive-gap route present")

    generated_groups = list(groups.values())
    no_claims = not any(any_claim_true(group) for group in generated_groups)
    add("VAL4630_07_all_rows_nonclaim", no_claims, "no generated row promotes a claim")

    add("VAL4630_08_doc_marker", MARKER in read_text(DOC_PATH), "checkpoint doc marker present")
    add("VAL4630_09_formal_marker", MARKER in read_text(FORMAL_PATH), "formal marker present")
    add("VAL4630_10_claim_register", CLAIM_ID in read_text(CLAIMS_PATH), "claim register row present")
    add("VAL4630_11_spine_marker", MARKER in read_text(SPINE_PATH), "spine marker present")
    add("VAL4630_12_packet_marker", PACKET_MARKER in read_text(PACKET_PATH), "packet marker present")
    add("VAL4630_13_next_target", NEXT_TARGET in read_text(NEXT_CSV), NEXT_TARGET)
    add("VAL4630_14_public_stage_clean", git_clean(PUBLIC_STAGE), str(PUBLIC_STAGE))
    add("VAL4630_15_backup_repo_clean", git_clean(BACKUP_REPO), str(BACKUP_REPO))

    overall = all(row["status"] == "PASS" for row in checks)
    add("VAL4630_OVERALL", overall, "4630 parent action contract checkpoint")
    return checks


def main() -> None:
    now = utc_now()
    groups = {
        "sources": source_rows(now),
        "parent": parent_action_rows(now),
        "variation": variation_rows(now),
        "invariant": invariant_rows(now),
        "local_gr": local_gr_rows(now),
        "evaluation": evaluation_rows(now),
        "controls": control_rows(now),
        "blockers": blocker_rows(now),
        "promotions": promotion_rows(now),
        "decisions": decision_rows(now),
        "statuses": status_rows(now),
        "nexts": next_rows(now),
    }

    write_csv(SOURCE_REGISTER, groups["sources"])
    write_csv(PARENT_ACTION_CSV, groups["parent"])
    write_csv(VARIATION_CSV, groups["variation"])
    write_csv(INVARIANT_CSV, groups["invariant"])
    write_csv(LOCAL_GR_CSV, groups["local_gr"])
    write_csv(EVAL_CSV, groups["evaluation"])
    write_csv(CONTROL_CSV, groups["controls"])
    write_csv(BLOCKERS_CSV, groups["blockers"])
    write_csv(PROMOTION_CSV, groups["promotions"])
    write_csv(DECISION_CSV, groups["decisions"])
    write_csv(STATUS_CSV, groups["statuses"])
    write_csv(NEXT_CSV, groups["nexts"])

    write_doc(now, groups)
    write_formal(now)
    append_integrations()
    write_csv(VALIDATION_CSV, validation_rows(groups))

    print(f"4630 checkpoint generated: {DOC_PATH}")
    print(f"Validation: {VALIDATION_CSV}")


if __name__ == "__main__":
    main()

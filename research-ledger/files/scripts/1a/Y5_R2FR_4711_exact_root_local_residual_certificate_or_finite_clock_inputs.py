from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterable


ROOT = Path(__file__).resolve().parents[2]
POST = ROOT / "post-checkpoint-work"
FORMAL = ROOT / "formalization-workbench"
SOURCE_DIR = POST / "source-intake" / "mts_residuals"

CHECKPOINT = "4711"
CLAIM_ID = "L-553"
MARKER = "PPC4161_EXACT_ROOT_LOCAL_RESIDUAL_CERTIFICATE_OR_FINITE_CLOCK_INPUTS_4711"
PACKET_MARKER = "PPC4161_PACKET_EXACT_ROOT_LOCAL_RESIDUAL_CERTIFICATE_OR_FINITE_CLOCK_INPUTS_4711"
DECISION = "EXACT_ROOT_NORMAL_EQUATION_CERTIFICATE_DERIVED_PARENT_COHERCIVITY_SOURCE_ROWS_MISSING_NONCLAIM"
NEXT_TARGET = "4712-Y5-R2FR-root-coercivity-source-pack-or-no-cokernel-proof.md"

DOC_PATH = POST / "4711-Y5-R2FR-exact-root-local-residual-certificate-or-finite-clock-inputs.md"
FORMAL_PATH = FORMAL / "727-PPC4161-exact-root-local-residual-certificate-or-finite-clock-inputs.md"
CLAIMS_PATH = FORMAL / "02-claims-register.csv"
SPINE_PATH = FORMAL / "07-unification-spine.md"
PACKET_PATH = FORMAL / "180-PPC4161-private-local-packet-integration.md"
RESUME_PATH = POST / "CURRENT_LOCAL_RESUME.md"

CSV_4710_ZERO = SOURCE_DIR / "P8_Y5_R2FR_4710_TAU_ZERO_OR_EXACT_ROOT_BYPASS_CERTIFICATE.csv"
CSV_4710_FINITE = SOURCE_DIR / "P8_Y5_R2FR_4710_DYNAMIC_CLOCK_FINITE_SOURCE_ROWS.csv"
CSV_4710_VALIDATION = SOURCE_DIR / "P8_Y5_BRR545_4710_VALIDATION.csv"
CSV_3221_THEOREM = SOURCE_DIR / "P8_Y5_R2FR_3221_DEFECT_NORM_SOURCE_ROOT_THEOREM.csv"
CSV_3222_CONTRACT = SOURCE_DIR / "P8_Y5_R2FR_3222_PARENT_ACTION_DEFECT_NORM_CONTRACT.csv"
CSV_3222_VARIATION = SOURCE_DIR / "P8_Y5_R2FR_3222_VARIATION_AND_MAXWELL_LIMIT_PROOF.csv"
CSV_3222_GUARDS = SOURCE_DIR / "P8_Y5_R2FR_3222_STRESS_POYNTING_AND_READOUT_GUARDS.csv"
CSV_3223_FORMULA = SOURCE_DIR / "P8_Y5_R2FR_3223_FINITE_ALPHA_BOUND_FORMULA.csv"
CSV_3223_SCORE = SOURCE_DIR / "P8_Y5_R2FR_3223_RQ_CANDIDATE_SCORECARD.csv"
CSV_3223_SEARCH = SOURCE_DIR / "P8_Y5_R2FR_3223_RQ_SOURCE_SEARCH.csv"
CSV_3229_REDUCTION = SOURCE_DIR / "P8_Y5_R2FR_3229_XI_CLOCK_REDUCTION_WITH_TRANSPORT_ERROR.csv"
CSV_609_NO_LINEAR = SOURCE_DIR / "P8_Y5_R10_609_NO_LINEAR_MARKER_SYMMETRY_GATE.csv"
CSV_4704_IMAGE = SOURCE_DIR / "P8_Y5_R2FR_4704_VISIBLE_IMAGE_PROOF_ATTEMPT.csv"
CSV_4707_ZERO = SOURCE_DIR / "P8_Y5_R2FR_4707_EXACT_ZERO_CONTRACT_ROWS.csv"
CSV_4708_RADOUT = SOURCE_DIR / "P8_Y5_R2FR_4708_RADIOUT_NATURALITY_THEOREM_ROWS.csv"
CSV_4709_THEOREM = SOURCE_DIR / "P8_Y5_R2FR_4709_CLOCK_TAU_MAP_THEOREM_ROWS.csv"

SOURCE_REGISTER = SOURCE_DIR / "P8_Y5_R2FR_4711_SOURCE_REGISTER.csv"
ROOT_CERT_CSV = SOURCE_DIR / "P8_Y5_R2FR_4711_ROOT_NORMAL_EQUATION_CERTIFICATE.csv"
FINITE_CSV = SOURCE_DIR / "P8_Y5_R2FR_4711_FINITE_ROOT_CLOCK_INPUT_ROWS.csv"
GATES_CSV = SOURCE_DIR / "P8_Y5_R2FR_4711_PROMOTION_GATES.csv"
FIREWALL_CSV = SOURCE_DIR / "P8_Y5_R2FR_4711_FIREWALL_ROWS.csv"
DECISION_CSV = SOURCE_DIR / "P8_Y5_R2FR_4711_DECISION.csv"
STATUS_CSV = SOURCE_DIR / "P8_Y5_R2FR_4711_STATUS.csv"
NEXT_CSV = SOURCE_DIR / "P8_Y5_R2FR_4711_NEXT_TARGET.csv"
VALIDATION_CSV = SOURCE_DIR / "P8_Y5_BRR545_4711_VALIDATION.csv"


def now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace") if path.exists() else ""


def line_of(path: Path, needle: str) -> int:
    for index, line in enumerate(text(path).splitlines(), start=1):
        if needle in line:
            return index
    return 0


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fields: list[str] = []
    for row in rows:
        for field in row:
            if field not in fields:
                fields.append(field)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def table(rows: Iterable[dict[str, Any]]) -> str:
    rows = list(rows)
    if not rows:
        return ""
    headers = list(rows[0].keys())
    out = ["| " + " | ".join(headers) + " |", "| " + " | ".join("---" for _ in headers) + " |"]
    for row in rows:
        out.append("| " + " | ".join(str(row.get(h, "")).replace("|", "\\|").replace("\n", " ") for h in headers) + " |")
    return "\n".join(out)


def append_once(path: Path, marker: str, body: str) -> None:
    existing = text(path)
    if marker in existing:
        return
    path.write_text(existing.rstrip() + "\n\n" + body.strip() + "\n", encoding="utf-8")


def source_rows(timestamp: str) -> list[dict[str, Any]]:
    specs = [
        ("SRC4711_00_4710_exact_root", CSV_4710_ZERO, "TZC4710_1_exact_root_bypass", "4710 exact-root bypass handoff"),
        ("SRC4711_01_4710_finite", CSV_4710_FINITE, "DCF4710_0_full_clock_residual_bound", "4710 finite clock bound"),
        ("SRC4711_02_4710_validation", CSV_4710_VALIDATION, "VAL4710_OVERALL", "4710 validation"),
        ("SRC4711_03_3221_first_zero", CSV_3221_THEOREM, "DN3221_1_first_derivative_zero", "defect-norm first derivative zero"),
        ("SRC4711_04_3221_verdict", CSV_3221_THEOREM, "DN3221_5_verdict", "defect-norm parent action not signed"),
        ("SRC4711_05_3222_action", CSV_3222_CONTRACT, "DNC3222_1_action_term", "defect norm EM kinetic action term"),
        ("SRC4711_06_3222_root", CSV_3222_CONTRACT, "DNC3222_2_same_branch_root", "same-branch R_Q root gap"),
        ("SRC4711_07_3222_no_linear", CSV_3222_CONTRACT, "DNC3222_3_no_linear_defect", "no-linear defect gap"),
        ("SRC4711_08_3222_variation", CSV_3222_VARIATION, "VAR3222_0_coefficient_first_variation", "coefficient first variation theorem"),
        ("SRC4711_09_3222_counterexample", CSV_3222_VARIATION, "VAR3222_3_no_linear_defect_counterexample", "linear defect counterexample"),
        ("SRC4711_10_3222_null_guard", CSV_3222_GUARDS, "SPG3222_0_null_wave_guard", "stress/Poynting guard"),
        ("SRC4711_11_3223_exact", CSV_3223_FORMULA, "FORM3223_0_exact_root", "exact root formula"),
        ("SRC4711_12_3223_finite", CSV_3223_FORMULA, "FORM3223_1_offroot_bound", "finite off-root alpha bound"),
        ("SRC4711_13_3223_RZ", CSV_3223_SCORE, "SCORE3223_RZ", "best alpha-owner residual target"),
        ("SRC4711_14_3223_verdict", CSV_3223_SEARCH, "SRCSEARCH3223_VERDICT", "no R_Q source signed"),
        ("SRC4711_15_3229_transport", CSV_3229_REDUCTION, "XIR3229_1_exact_transport_case", "transport exact zero case"),
        ("SRC4711_16_609_no_linear", CSV_609_NO_LINEAR, "NL609_4_no_linear_verdict", "no-linear marker symmetry verdict"),
        ("SRC4711_17_4704_image", CSV_4704_IMAGE, "VIP4704_0_exact_image_zero_theorem", "typed image/no extra F2 zero theorem"),
        ("SRC4711_18_4704_counter", CSV_4704_IMAGE, "VIP4704_2_scalar_functional_countermodel", "scalar functional countermodel"),
        ("SRC4711_19_4707_noHom", CSV_4707_ZERO, "ZERO4707_1_no_extra_F2_subcase", "no-Hom subcase"),
        ("SRC4711_20_4708_readout", CSV_4708_RADOUT, "RRN4708_1_observed_readout_zero", "readout zero theorem"),
        ("SRC4711_21_4709_clock", CSV_4709_THEOREM, "CTM4709_3_clock_Breadout_zero_branch", "clock B_readout zero branch"),
    ]
    rows = []
    for source_id, path, needle, role in specs:
        line = line_of(path, needle)
        rows.append(
            {
                "checkpoint": CHECKPOINT,
                "source_id": source_id,
                "source_path": str(path),
                "path_exists": path.exists(),
                "needle": needle,
                "needle_found": line > 0,
                "source_line": line,
                "role": role,
                "valid_for_claim": False,
                "timestamp_utc": timestamp,
            }
        )
    return rows


def root_certificate_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "cert_id": "RNC4711_0_parent_residual_square_normal_equation",
            "claim_piece": "R_Q=0 from stationarity",
            "statement": "Let S_R[Phi]=1/2 ||R_Q(Phi)||_W^2 plus no independent linear residual source. At a stationary local branch, A_Q^dagger W R_Q + J_root + B_root=0, where A_Q=DR_Q[Phi_*]. If the residual complex has a no-cokernel/coercivity estimate ||R_Q||_W <= C_root ||A_Q^dagger W R_Q|| and J_root=B_root=0, then R_Q=0.",
            "proof": "Stationarity gives A_Q^dagger W R_Q=0 on the homogeneous branch. The coercivity estimate then implies ||R_Q||_W <= 0, hence R_Q=0. No fitted clock or alpha datum enters the proof.",
            "current_status": "EXACT_CONDITIONAL_THEOREM_COHERCIVITY_UNSIGNED",
            "missing_for_claim": "parent residual-square action; no independent linear source; no-cokernel/coercivity; boundary/source silence",
            "valid_for_claim": False,
            "claim_allowed": False,
            "timestamp_utc": timestamp,
        },
        {
            "checkpoint": CHECKPOINT,
            "cert_id": "RNC4711_1_finite_root_bound",
            "claim_piece": "finite R_Q if exact root fails",
            "statement": "If source, boundary or cokernel terms survive, then ||R_Q||_W <= C_root (||J_root|| + ||B_root|| + ||Pi_coker R_Q||).",
            "proof": "Move non-homogeneous terms to the right side of the normal equation and apply the same residual coercivity estimate.",
            "current_status": "FINITE_BOUND_FORMULA_READY_FOR_INPUTS",
            "missing_for_claim": "numeric/source-backed C_root, J_root, B_root and Pi_coker rows",
            "valid_for_claim": False,
            "claim_allowed": False,
            "timestamp_utc": timestamp,
        },
        {
            "checkpoint": CHECKPOINT,
            "cert_id": "RNC4711_2_no_linear_EM_owner_contract",
            "claim_piece": "no-linear EM kinetic owner",
            "statement": "The exact-root clock branch requires Delta Z_A=lambda_D ||R_Q||_P^2 + O(||R_Q||^3_even) with no a<R_Q>, no independent lambda_A F_Q^2 and no hidden/readout scalar f(I_hid)F_Q^2.",
            "proof": "A linear term gives partial_m Delta Z_A|root=a<partial_m R_Q>, generically nonzero. The 4704/4707/4708 rows give the typed no-Hom/readout zero route, but the 609/3222 counter rows show the route is not fully parent-signed.",
            "current_status": "CONTRACT_SHARPENED_NOT_SIGNED",
            "missing_for_claim": "operator-domain exhaustion or exact even-residual symmetry excluding all linear/independent coefficient slots",
            "valid_for_claim": False,
            "claim_allowed": False,
            "timestamp_utc": timestamp,
        },
        {
            "checkpoint": CHECKPOINT,
            "cert_id": "RNC4711_3_clock_alpha_closure_if_root_signs",
            "claim_piece": "clock alpha residual zero",
            "statement": "If RNC4711_0 and RNC4711_2 sign on the same branch as the 4709 fixed clock readout, then R_Q=0, Delta m=0, E_clock_transport=0 and B_readout_clock=0 imply D_tau ln alpha_EM=0.",
            "proof": "Substitute the exact residual root into the 4710 bypass: C_D|Delta m tau_clock_time|, E_HO, E_clock_transport and B_readout_clock vanish on the same branch.",
            "current_status": "EXACT_CONDITIONAL_COMPOSITION_NONCLAIM",
            "missing_for_claim": "same-branch proof that R_Q root, no-linear owner and fixed clock readout are all clauses of one parent action",
            "valid_for_claim": False,
            "claim_allowed": False,
            "timestamp_utc": timestamp,
        },
    ]


def finite_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "row_id": "FRC4711_0_Croot",
            "quantity": "C_root",
            "formula": "||R_Q||_W <= C_root ||A_Q^dagger W R_Q||",
            "units": "operator inverse norm",
            "needed_source": "residual complex no-cokernel/coercivity proof or numeric spectral lower bound",
            "status": "MISSING_PARENT_COHERCIVITY",
            "valid_for_claim": False,
            "claim_allowed": False,
            "timestamp_utc": timestamp,
        },
        {
            "checkpoint": CHECKPOINT,
            "row_id": "FRC4711_1_Jroot",
            "quantity": "J_root",
            "formula": "unowned linear residual forcing in A_Q^dagger W R_Q + J_root + B_root=0",
            "units": "dual residual units",
            "needed_source": "parent action term proving no linear source or source-backed forcing norm",
            "status": "MISSING_NO_LINEAR_SOURCE_PROOF",
            "valid_for_claim": False,
            "claim_allowed": False,
            "timestamp_utc": timestamp,
        },
        {
            "checkpoint": CHECKPOINT,
            "row_id": "FRC4711_2_Broot",
            "quantity": "B_root",
            "formula": "boundary/root flux term left by integration by parts",
            "units": "dual residual boundary units",
            "needed_source": "local boundary/no-flux theorem or finite boundary norm",
            "status": "MISSING_BOUNDARY_SILENCE_OR_BOUND",
            "valid_for_claim": False,
            "claim_allowed": False,
            "timestamp_utc": timestamp,
        },
        {
            "checkpoint": CHECKPOINT,
            "row_id": "FRC4711_3_Picoker",
            "quantity": "Pi_coker R_Q",
            "formula": "residual component invisible to A_Q^dagger W",
            "units": "residual norm",
            "needed_source": "no-cokernel theorem or finite cokernel projection row",
            "status": "MISSING_COKERNEL_CONTROL",
            "valid_for_claim": False,
            "claim_allowed": False,
            "timestamp_utc": timestamp,
        },
        {
            "checkpoint": CHECKPOINT,
            "row_id": "FRC4711_4_Llinear",
            "quantity": "L_linear",
            "formula": "linear EM coefficient leakage a<R_Q> or hidden f(I_hid)F_Q^2",
            "units": "EM kinetic coefficient derivative",
            "needed_source": "operator-domain exhaustion/even-residual symmetry or finite hidden-Hom derivative bound",
            "status": "MISSING_NO_LINEAR_EM_OWNER",
            "valid_for_claim": False,
            "claim_allowed": False,
            "timestamp_utc": timestamp,
        },
    ]


def gate_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "gate_id": "GATE4711_0_exact_root_promote",
            "required": "RNC4711_0 parent residual-square normal equation + no-cokernel + J_root=B_root=0",
            "current_result": "BLOCKED_PARENT_COHERCIVITY_UNSIGNED",
            "if_pass": "R_Q=0 on the local branch",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "checkpoint": CHECKPOINT,
            "gate_id": "GATE4711_1_no_linear_promote",
            "required": "RNC4711_2 no-linear EM owner contract",
            "current_result": "BLOCKED_OPERATOR_DOMAIN_OR_EVEN_SYMMETRY_UNSIGNED",
            "if_pass": "b_alpha first derivative vanishes at root",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "checkpoint": CHECKPOINT,
            "gate_id": "GATE4711_2_clock_promote",
            "required": "GATE4711_0 + GATE4711_1 + 4709 fixed clock readout on one branch",
            "current_result": "BLOCKED_BY_UPSTREAM_GATES",
            "if_pass": "D_tau ln alpha_EM=0 on the local clock branch",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
    ]


def firewall_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "firewall_id": "FW4711_0_no_residual_square_without_parent_action",
            "rule": "Do not use the normal-equation theorem unless the residual-square term is in the parent action, not added after seeing local failures.",
            "status": "ACTIVE",
            "valid_for_claim": False,
            "claim_allowed": False,
            "timestamp_utc": timestamp,
        },
        {
            "checkpoint": CHECKPOINT,
            "firewall_id": "FW4711_1_no_stationarity_to_root_without_cokernel",
            "rule": "Stationarity A_Q^dagger W R_Q=0 does not imply R_Q=0 unless no-cokernel/coercivity is proved.",
            "status": "ACTIVE",
            "valid_for_claim": False,
            "claim_allowed": False,
            "timestamp_utc": timestamp,
        },
        {
            "checkpoint": CHECKPOINT,
            "firewall_id": "FW4711_2_no_scalar_F2_to_full_EM_stress",
            "rule": "The R_Z/F2 coefficient root does not by itself close null-wave stress, Poynting, current normalization or local-GR source transfer.",
            "status": "ACTIVE",
            "valid_for_claim": False,
            "claim_allowed": False,
            "timestamp_utc": timestamp,
        },
    ]


def decision_status_next(timestamp: str) -> tuple[list[dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]]]:
    decision = [
        {
            "checkpoint": CHECKPOINT,
            "branch": "MTS_R2FR_Y5_EXACT_ROOT_NORMAL_EQUATION_4711",
            "decision": DECISION,
            "reason": "4711 derives the exact condition under which the local residual root follows from the parent action: residual-square stationarity plus no-cokernel/coercivity and no boundary/source forcing. The proof is sharp but not yet live because those parent rows are missing.",
            "valid_for_claim": False,
            "claim_allowed": False,
            "timestamp_utc": timestamp,
        }
    ]
    status = [
        {
            "checkpoint": CHECKPOINT,
            "marker": MARKER,
            "claim_id": CLAIM_ID,
            "decision": DECISION,
            "derived": "normal-equation exact-root theorem; finite root bound; no-linear EM owner contract; clock alpha zero composition if root signs",
            "not_derived": "parent residual-square source; no-cokernel/coercivity proof; J_root/B_root silence; no-linear/even-residual EM owner; stress/Poynting transfer",
            "claim_status": "PRIVATE_NONCLAIM",
            "local_GR_public_claim": False,
            "next_target": NEXT_TARGET,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
    ]
    next_rows = [
        {
            "checkpoint": CHECKPOINT,
            "next_id": "NT4711_0",
            "target": NEXT_TARGET,
            "reason": "The root route is now a concrete no-cokernel/coercivity source-pack problem rather than a vague missing R_Q=0 assertion.",
            "derive_first": "prove residual complex no-cokernel/coercivity and boundary/source silence for the parent R_Q branch",
            "fallback": "source finite C_root, J_root, B_root, Pi_coker and L_linear rows and propagate clock bound",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
    ]
    return decision, status, next_rows


def write_documents(timestamp: str, data: dict[str, list[dict[str, Any]]]) -> None:
    DOC_PATH.write_text(
        f"""# 4711 - Exact Root Local Residual Certificate Or Finite Clock Inputs

Marker: `{MARKER}`

Claim register: `{CLAIM_ID}`

Generated UTC: `{timestamp}`

## Result
4711 turns `prove R_Q=0` into a real normal-equation theorem.

Exact route:

```text
S_R[Phi] = 1/2 ||R_Q(Phi)||_W^2
A_Q = D R_Q[Phi_*]
stationarity: A_Q^dagger W R_Q + J_root + B_root = 0
no-cokernel/coercivity: ||R_Q||_W <= C_root ||A_Q^dagger W R_Q||
J_root = B_root = 0
=> R_Q = 0.
```

Finite fallback:

```text
||R_Q||_W <= C_root (||J_root|| + ||B_root|| + ||Pi_coker R_Q||).
```

This is the useful step: the exact-root route is now a precise parent-action/coercivity problem, not a magic declaration that the residual vanishes.

If this root certificate and the no-linear EM owner both sign, then the 4710 clock branch closes:

```text
R_Q=0 + no linear EM kinetic owner + B_readout_clock=0
=> D_tau ln alpha_EM = 0.
```

No public/local-GR claim is made; stress/Poynting/current-normalization gates remain separate.

## Source Register
{table(data["sources"])}

## Root Normal Equation Certificate
{table(data["root"])}

## Finite Root / Clock Input Rows
{table(data["finite"])}

## Promotion Gates
{table(data["gates"])}

## Firewalls
{table(data["firewalls"])}

## Decision
{table(data["decision"])}

## Status
{table(data["status"])}

## Next Target
{table(data["next"])}
""",
        encoding="utf-8",
    )
    FORMAL_PATH.write_text(
        f"""# 727 - PPC4161 Exact Root Local Residual Certificate Or Finite Clock Inputs

Marker: `{MARKER}`

Claim register: `{CLAIM_ID}`

Generated UTC: `{timestamp}`

## Formal Insert
Let `R_Q` be the parent residual and `A_Q=D R_Q[Phi_*]`.

Residual-square branch:

```text
S_R = 1/2 ||R_Q||_W^2.
```

Stationarity gives:

```text
A_Q^dagger W R_Q + J_root + B_root = 0.
```

If:

```text
||R_Q||_W <= C_root ||A_Q^dagger W R_Q||,
J_root=0,
B_root=0,
```

then:

```text
R_Q=0.
```

If not:

```text
||R_Q||_W <= C_root(||J_root||+||B_root||+||Pi_coker R_Q||).
```

The no-linear EM owner must also sign:

```text
Delta Z_A = lambda_D ||R_Q||_P^2
```

with no `a<R_Q>`, no independent `lambda_A F_Q^2`, and no hidden/readout scalar coefficient. Only then does the 4710 exact-root clock branch imply `D_tau ln alpha_EM=0`.
""",
        encoding="utf-8",
    )


def update_registers(timestamp: str) -> None:
    claims = read_csv(CLAIMS_PATH) if CLAIMS_PATH.exists() else []
    fieldnames = list(claims[0].keys()) if claims else [
        "claim_id",
        "domain",
        "claim",
        "current_evidence",
        "status",
        "next_test",
        "key_risk",
        "sector",
        "evidence",
        "next_action",
        "risk",
        "title",
        "notes",
    ]
    row = {field: "" for field in fieldnames}
    row.update(
        {
            "claim_id": CLAIM_ID,
            "domain": "local_gr_empirical_interface",
            "claim": "4711 derives the normal-equation/coercivity certificate that would force the local residual root R_Q=0, plus finite fallback rows if the root proof fails.",
            "current_evidence": "Generated source register, root normal-equation certificate, finite root/clock input rows, promotion gates, firewalls, decision, status, next target and validation.",
            "status": "normal_equation_exact_root_certificate_nonclaim",
            "next_test": NEXT_TARGET,
            "key_risk": "Mistaking stationarity for R_Q=0 without no-cokernel/coercivity, or mistaking scalar F2 coefficient safety for full EM stress/local-GR safety.",
            "sector": "local_gr",
            "evidence": str(DOC_PATH),
            "next_action": NEXT_TARGET,
            "title": "Exact root local residual certificate or finite clock inputs",
            "notes": f"{MARKER}; {DECISION}; generated {timestamp}",
        }
    )
    existing = next((claim for claim in claims if claim.get("claim_id") == CLAIM_ID), None)
    if existing is None:
        claims.append(row)
    else:
        existing.update(row)
    write_csv(CLAIMS_PATH, claims)

    append_once(
        SPINE_PATH,
        MARKER,
        f"""### {MARKER}

- Claim: `{CLAIM_ID}`.
- Status: private nonclaim.
- Movement: `R_Q=0` is now reduced to a normal-equation/coercivity theorem: residual-square parent action, no cokernel, and no boundary/source forcing imply exact local root.
- Finite fallback: `||R_Q||_W <= C_root(||J_root||+||B_root||+||Pi_coker R_Q||)`.
- Firewall: stationarity is not root without no-cokernel, and scalar F2 root is not full EM stress/Poynting/local-GR safety.
- Next: `{NEXT_TARGET}`.
""",
    )
    append_once(
        PACKET_PATH,
        PACKET_MARKER,
        f"""### {PACKET_MARKER}

- Source checkpoint: `{CHECKPOINT}`.
- Decision: `{DECISION}`.
- Packet role: turns exact root into a parent-action no-cokernel/coercivity source-pack problem.
- Validation: `{VALIDATION_CSV}`.
""",
    )
    RESUME_PATH.write_text(
        f"""# Current Local Resume Bookmark

Generated: 2026-07-07

Scope: local/private framework work only. No GitHub push, no public-stage update, no backup-repo operation.

## Latest Local Checkpoint

`4711-Y5-R2FR-exact-root-local-residual-certificate-or-finite-clock-inputs.md`

## What Changed

The exact-root route is now a normal-equation theorem:

```text
S_R = 1/2 ||R_Q||_W^2
A_Q^dagger W R_Q + J_root + B_root = 0
||R_Q||_W <= C_root ||A_Q^dagger W R_Q||
J_root = B_root = 0
=> R_Q = 0.
```

Finite fallback:

```text
||R_Q||_W <= C_root (||J_root|| + ||B_root|| + ||Pi_coker R_Q||).
```

## Current Best Next Target

`{NEXT_TARGET}`

## Do Not Do Next

- Do not claim `R_Q=0` from stationarity unless no-cokernel/coercivity is parent-signed.
- Do not treat scalar `F_Q^2` coefficient safety as full EM stress/Poynting/current safety.
- Do not push to GitHub unless Martin explicitly asks for a GitHub update.
""",
        encoding="utf-8",
    )


def validation_rows(timestamp: str, data: dict[str, list[dict[str, Any]]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []

    def add(check_id: str, passed: bool, detail: str) -> None:
        rows.append({"checkpoint": CHECKPOINT, "check_id": check_id, "passed": passed, "detail": detail, "valid_for_claim": False, "timestamp_utc": timestamp})

    add("VAL4711_0_sources_exist", all(row["path_exists"] for row in data["sources"]), "all source-register paths exist")
    add("VAL4711_1_needles_found", all(row["needle_found"] for row in data["sources"]), "all source-register needles found")
    add("VAL4711_2_normal_equation", any(row["cert_id"] == "RNC4711_0_parent_residual_square_normal_equation" for row in data["root"]), "normal-equation theorem present")
    add("VAL4711_3_finite_bound", any(row["cert_id"] == "RNC4711_1_finite_root_bound" for row in data["root"]), "finite root bound theorem present")
    add("VAL4711_4_no_linear", any(row["cert_id"] == "RNC4711_2_no_linear_EM_owner_contract" for row in data["root"]), "no-linear EM owner contract present")
    add("VAL4711_5_clock_composition", any(row["cert_id"] == "RNC4711_3_clock_alpha_closure_if_root_signs" for row in data["root"]), "clock alpha closure composition present")
    add("VAL4711_6_finite_inputs", len(data["finite"]) >= 5, "finite input rows present")
    add("VAL4711_7_gates", len(data["gates"]) >= 3, "promotion gates present")
    add("VAL4711_8_firewalls", len(data["firewalls"]) >= 3, "firewalls present")
    add("VAL4711_9_next_target", data["next"][0]["target"] == NEXT_TARGET, "4712 next target selected")
    add("VAL4711_10_claim_row_exists", CLAIM_ID in text(CLAIMS_PATH), f"claims register contains {CLAIM_ID}")
    add("VAL4711_11_formal_doc", FORMAL_PATH.exists() and MARKER in text(FORMAL_PATH), "formal doc exists with marker")
    add("VAL4711_12_post_doc", DOC_PATH.exists() and MARKER in text(DOC_PATH), "post checkpoint exists with marker")
    add("VAL4711_13_spine_marker", MARKER in text(SPINE_PATH), "spine marker written")
    add("VAL4711_14_packet_marker", PACKET_MARKER in text(PACKET_PATH), "packet marker written")
    add("VAL4711_15_resume_updated", NEXT_TARGET in text(RESUME_PATH), "resume bookmark updated")

    for csv_path in [SOURCE_REGISTER, ROOT_CERT_CSV, FINITE_CSV, GATES_CSV, FIREWALL_CSV, DECISION_CSV, STATUS_CSV, NEXT_CSV]:
        try:
            parsed = read_csv(csv_path)
            add(f"VAL4711_csv_{csv_path.stem}", len(parsed) > 0, f"{csv_path} parses with {len(parsed)} rows")
        except Exception as exc:
            add(f"VAL4711_csv_{csv_path.stem}", False, f"{csv_path} failed to parse: {exc}")

    claim_values: list[str] = []
    for row_group in [data["root"], data["finite"], data["gates"], data["firewalls"], data["decision"], data["status"], data["next"]]:
        for row in row_group:
            for key in ("valid_for_claim", "claim_allowed", "local_GR_public_claim"):
                if key in row:
                    claim_values.append(str(row[key]).lower())
    add("VAL4711_16_no_claim_rows_true", all(value in {"false", ""} for value in claim_values), "generated rows keep claim flags false")

    pycache = POST / "scripts" / "__pycache__"
    if pycache.exists():
        shutil.rmtree(pycache)
    add("VAL4711_17_pycache_absent", not pycache.exists(), "scripts __pycache__ absent")

    overall = all(str(row["passed"]) == "True" or row["passed"] is True for row in rows)
    add("VAL4711_OVERALL", overall, "PASS" if overall else "FAIL")
    return rows


def main() -> None:
    timestamp = now()
    decision, status, next_rows = decision_status_next(timestamp)
    data: dict[str, list[dict[str, Any]]] = {
        "sources": source_rows(timestamp),
        "root": root_certificate_rows(timestamp),
        "finite": finite_rows(timestamp),
        "gates": gate_rows(timestamp),
        "firewalls": firewall_rows(timestamp),
        "decision": decision,
        "status": status,
        "next": next_rows,
    }

    write_csv(SOURCE_REGISTER, data["sources"])
    write_csv(ROOT_CERT_CSV, data["root"])
    write_csv(FINITE_CSV, data["finite"])
    write_csv(GATES_CSV, data["gates"])
    write_csv(FIREWALL_CSV, data["firewalls"])
    write_csv(DECISION_CSV, data["decision"])
    write_csv(STATUS_CSV, data["status"])
    write_csv(NEXT_CSV, data["next"])

    write_documents(timestamp, data)
    update_registers(timestamp)
    validation = validation_rows(timestamp, data)
    write_csv(VALIDATION_CSV, validation)

    print(f"{CHECKPOINT} complete: {DOC_PATH}")
    print(f"validation: {VALIDATION_CSV}")


if __name__ == "__main__":
    main()

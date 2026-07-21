from __future__ import annotations

import csv
import math
import py_compile
import shutil
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(r"D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main")
POST = ROOT / "post-checkpoint-work"
FORMAL = ROOT / "formalization-workbench"
SOURCE_DIR = POST / "source-intake" / "mts_residuals"
SCRIPT_DIR = POST / "scripts"

CHECKPOINT = "4845"
CLAIM_ID = "L-687"
MARKER = "PPC4161_GAMMA_LOCAL_CONSTANCY_EXCHANGE_AND_SIGMAGAMMA_PROFILE_BOUND_4845"
PACKET_MARKER = "PPC4161_PACKET_GAMMA_RESPONSE_DOUBLET_LOCAL_SUPPRESSION_4845"
DECISION = "RESPONSE_DOUBLET_POSITIVE_ACTION_CONSTRUCTS_ACTIVE_GAMMA_LOCAL_ZERO_AND_QUADRATIC_SOURCE_BOUND_CONSTANT_BACKGROUND_RETAINED_GLOBAL_ADOPTION_OPEN_NONCLAIM"
NEXT_TARGET = "4846-Y5-R2FR-response-doublet-cosmology-local-source-split-or-first-real-SigmaGamma-arena-row.md"
C_LIGHT = 299_792_458.0

DOC_PATH = POST / "4845-Y5-R2FR-Gamma-local-constancy-exchange-and-SigmaGamma-profile-bound.md"
FORMAL_PATH = FORMAL / "861-PPC4161-Gamma-local-constancy-exchange-and-SigmaGamma-profile-bound.md"
CLAIMS_PATH = FORMAL / "02-claims-register.csv"
SPINE_PATH = FORMAL / "07-unification-spine.md"
PACKET_PATH = FORMAL / "180-PPC4161-private-local-packet-integration.md"
RESUME_PATH = POST / "CURRENT_LOCAL_RESUME.md"
RUNNER = SCRIPT_DIR / "gamma_response_doublet_local_suppression_runner.py"

SOURCE_REGISTER = SOURCE_DIR / "P8_Y5_R2FR_4845_SOURCE_REGISTER.csv"
ACTION_CONSTRUCTION = SOURCE_DIR / "P8_Y5_R2FR_4845_RESPONSE_DOUBLET_ACTION_CONSTRUCTION.csv"
SUPPRESSION_THEOREM = SOURCE_DIR / "P8_Y5_R2FR_4845_LOCAL_SUPPRESSION_THEOREM.csv"
EXCHANGE_MAP = SOURCE_DIR / "P8_Y5_R2FR_4845_BIANCHI_EXCHANGE_SIGN_MAP.csv"
RUNNER_INPUT = SOURCE_DIR / "P8_Y5_R2FR_4845_GAMMA_SUPPRESSION_RUNNER_INPUT.csv"
RUNNER_OUTPUT = SOURCE_DIR / "P8_Y5_R2FR_4845_GAMMA_SUPPRESSION_RUNNER_OUTPUT.csv"
DECISION_CSV = SOURCE_DIR / "P8_Y5_R2FR_4845_DECISION_LEDGER.csv"
CLAIM_GATES = SOURCE_DIR / "P8_Y5_R2FR_4845_CLAIM_GATES.csv"
STATUS_CSV = SOURCE_DIR / "P8_Y5_R2FR_4845_STATUS.csv"
NEXT_TARGET_CSV = SOURCE_DIR / "P8_Y5_R2FR_4845_NEXT_TARGET.csv"
VALIDATION_CSV = SOURCE_DIR / "P8_Y5_BRR545_4845_VALIDATION.csv"

SOURCES = {
    "resume": RESUME_PATH,
    "doc_4844": POST / "4844-Y5-R2FR-E00-parent-residual-collapse-from-literal-MTS-action-or-first-physical-coefficient-row.md",
    "candidate": SOURCE_DIR / "P8_GAMMA_OWNER_CANDIDATE_ACTION.csv",
    "quadratic": SOURCE_DIR / "P8_Y5_R10_970_QUADRATIC_MEMORY_ACTION_CONSTRUCTION.csv",
    "contract": SOURCE_DIR / "P8_RESPONSE_DOUBLET_ACTION_CONTRACT.csv",
    "variation": SOURCE_DIR / "P8_RESPONSE_DOUBLET_ACTION_VARIATION.csv",
    "metric": SOURCE_DIR / "P8_RESPONSE_DOUBLET_METRIC_RESPONSE_LEDGER.csv",
    "sources": SOURCE_DIR / "P8_RESPONSE_DOUBLET_EULER_SOURCE_LEDGER.csv",
    "positive": SOURCE_DIR / "P8_EXTRA_SECTOR_SILENCE_ENERGY_IDENTITY.csv",
    "parent_eq": FORMAL / "36-minimal-parent-equations-v0.md",
    "core_consistency": FORMAL / "10-core-consistency-repair.md",
    "matter_4843": POST / "4843-Y5-R2FR-source-universality-branch-reconciliation-and-Newton-chain-propagation.md",
    "physical_lock": SOURCE_DIR / "P8_Y5_R2FR_2973_Z_BASIS_PHYSICAL_LOCK_ATTEMPT.csv",
    "runner": RUNNER,
    "generator": Path(__file__),
}


def now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace") if path.exists() else ""


def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fields = list(dict.fromkeys(field for row in rows for field in row))
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)


def md_safe(value: Any) -> str:
    return str(value).replace("\n", " ").replace("|", "\\|")


def md_table(rows: list[dict[str, Any]], fields: list[str]) -> str:
    header = "| " + " | ".join(fields) + " |"
    separator = "| " + " | ".join("---" for _ in fields) + " |"
    body = ["| " + " | ".join(md_safe(row.get(field, "")) for field in fields) + " |" for row in rows]
    return "\n".join([header, separator, *body])


def append_once(path: Path, marker: str, text: str) -> None:
    existing = read_text(path)
    if marker not in existing:
        write_text(path, existing.rstrip() + "\n\n" + text.strip() + "\n")


def as_float(value: Any) -> float:
    try:
        return float(str(value))
    except (TypeError, ValueError):
        return math.nan


def close_to(value: Any, target: float, rel: float = 1e-12, absolute: float = 1e-30) -> bool:
    number = as_float(value)
    return math.isfinite(number) and abs(number - target) <= max(absolute, rel * max(abs(target), 1.0e-300))


def source_specs() -> list[tuple[str, Path, str, str]]:
    return [
        ("SRC4845_00_resume", SOURCES["resume"], "4846-Y5-R2FR-response-doublet-cosmology-local-source-split", "4845 resume and handoff"),
        ("SRC4845_01_4844", SOURCES["doc_4844"], "Sigma_Gamma", "corrected action normalization and trace-reversed source"),
        ("SRC4845_02_candidate", SOURCES["candidate"], "GO516_A_response_doublet_quadratic_density", "existing response-doublet Gamma owner candidate"),
        ("SRC4845_03_quadratic", SOURCES["quadratic"], "QMA970_2_positivity", "positive quadratic action and energy identity"),
        ("SRC4845_04_contract", SOURCES["contract"], "RD516_1_even_scalar_density", "exchange-even action contract"),
        ("SRC4845_05_variation", SOURCES["variation"], "AV517_5_positive_theorem", "Euler and positive theorem"),
        ("SRC4845_06_metric", SOURCES["metric"], "MR517_4_fixed_point_stress", "same-action metric-response fixed point"),
        ("SRC4845_07_sources", SOURCES["sources"], "Y5_source_normalization", "counterexample ledger preventing overclaim"),
        ("SRC4845_08_positive", SOURCES["positive"], "E506_scalar_positive_operator", "general positive-operator silence identity"),
        ("SRC4845_09_parent_eq", SOURCES["parent_eq"], "q^nu = nabla^nu Gamma_eff - nabla_mu K_hat", "parent exchange-current sign and response pair"),
        ("SRC4845_10_consistency", SOURCES["core_consistency"], "ordinary matter stress-energy is not separately conserved", "older sign statement to reconcile"),
        ("SRC4845_11_matter", SOURCES["matter_4843"], "source-weight loop is closed again", "ordinary matter source-prefactor zero on private branch"),
        ("SRC4845_12_lock", SOURCES["physical_lock"], "LOCK2973_0_q_loc", "scope guard: Gamma carrier does not prove all physical residuals"),
        ("SRC4845_13_runner", SOURCES["runner"], "def evaluate_row", "4845 suppression runner"),
        ("SRC4845_14_generator", SOURCES["generator"], 'CHECKPOINT = "4845"', "4845 generator and validator"),
    ]


def source_register(timestamp: str) -> list[dict[str, Any]]:
    rows = []
    for source_id, path, needle, role in source_specs():
        text = read_text(path)
        rows.append({
            "checkpoint": CHECKPOINT,
            "source_id": source_id,
            "source_path": str(path),
            "exists": path.exists(),
            "needle": needle,
            "needle_found": needle in text,
            "role": role,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        })
    return rows


def action_rows(timestamp: str) -> list[dict[str, Any]]:
    rows = [
        ("RDA4845_0_fields", "response doublet", "R_+^A,R_-^A; Z^A=(R_+^A-R_-^A)/2", "Z is the exchange-odd Gamma carrier only"),
        ("RDA4845_1_symmetry", "exchange symmetry", "E:R_+^A<->R_-^A; Z^A->-Z^A", "ordinary visible matter is exchange-even on the 4843 branch"),
        ("RDA4845_2_density", "corrected Gamma density", "Gamma_eff=Gamma0+1/2 A_AB^mn nabla_m Z^A nabla_n Z^B+1/2 M2_AB Z^A Z^B-J_A Z^A+O(Z^4)", "uses a_Gamma=1 from 4844"),
        ("RDA4845_3_action", "post-checkpoint candidate action", "S_Gamma=-(1/kappa) int sqrt(-g) Gamma_eff", "same action owns Gamma and Pi_Gamma/Khat response"),
        ("RDA4845_4_Euler", "Z Euler equation", "L_AB Z^B=J_A+O(Z^3); L=-nabla(A nabla)+M2", "active operator remains nondegenerate at the local origin"),
        ("RDA4845_5_auxiliary", "algebraic auxiliary limit", "A_AB=0; M2_AB Z^B=J_A", "J=0 and positive M2 force Z=0 without a plateau axiom"),
        ("RDA4845_6_dynamic", "positive dynamic limit", "A>=0, M2>0 after gauge/zero-mode removal", "energy identity gives zero or finite response bound"),
        ("RDA4845_7_scope", "candidate adoption scope", "private post-checkpoint Gamma-carrier branch", "not a unique global derivation from all original MTS primitives"),
    ]
    return [{"construction_id": row_id, "object": obj, "formula": formula, "meaning": meaning, "valid_for_claim": False, "timestamp_utc": timestamp} for row_id, obj, formula, meaning in rows]


def theorem_rows(timestamp: str) -> list[dict[str, Any]]:
    rows = [
        ("LST4845_0_energy", "energy identity", "<Z,LZ>=||Z||_L^2=<Z,J>+B_boundary", "exact on the candidate action"),
        ("LST4845_1_zero", "active local zero", "J_loc=0, B_boundary=0, lambda_gap>0 => Z=0", "Gamma_act=Pi_act=Sigma_act=q_Gamma=0"),
        ("LST4845_2_bound", "finite carrier bound", "||Z||_H1 <= (||J||+B_lift)/lambda_gap", "source and boundary deviations remain measurable"),
        ("LST4845_3_quadratic", "quadratic gravitational suppression", "||Sigma_act|| <= C_Sigma[(||J||+B_lift)/lambda_gap]^2+R_higher", "no linear ordinary-matter Gamma force"),
        ("LST4845_4_acceleration", "local acceleration bound", "epsilon_a <= c^2 r^3 ||Sigma_act||/(3GM)", "direct Newton/orbital comparator"),
        ("LST4845_5_background", "constant Gamma0", "Sigma_total=Gamma0+Sigma_act", "Gamma0 is retained as de-Sitter background and never silently subtracted"),
        ("LST4845_6_qscope", "q_loc scope", "q_Gamma=0 does not imply every PPN/source/even-stress residual is zero", "prevents the old full-rank overclaim"),
        ("LST4845_7_cosmology", "cosmological activation", "nonzero J_cos/history/boundary can drive Z away from zero", "must be derived next rather than inserted as an environment switch"),
    ]
    return [{"theorem_id": row_id, "object": obj, "formula": formula, "consequence": consequence, "valid_for_claim": False, "timestamp_utc": timestamp} for row_id, obj, formula, consequence in rows]


def exchange_rows(timestamp: str) -> list[dict[str, Any]]:
    rows = [
        ("BEX4845_0_field", "G_mn+X_mn=kappa T_mn", "X_mn=Gamma_eff g_mn-2 Pi_Gamma_mn"),
        ("BEX4845_1_Bianchi", "nabla^m X_mn=kappa nabla^m T_mn", "the sign is positive when X is written on the left"),
        ("BEX4845_2_parent_q", "q_n:=nabla^m K_matter_mn=nabla^m X_mn", "matches 36 with K_MTS=-X and q=nabla Gamma-div Khat"),
        ("BEX4845_3_external", "Pi=0 => q_n=partial_n Gamma_G", "a varying external Gamma exchanges with matter and is not separately conservative"),
        ("BEX4845_4_variational", "candidate Z on shell and matter Z-blind => nabla X=0", "diffeomorphism Noether identity closes total conservation"),
        ("BEX4845_5_sign_repair", "older negative-sign line is inconsistent with G+Gamma g=kappa T", "use the positive-sign identity above in future post-checkpoint work"),
    ]
    return [{"exchange_id": row_id, "identity": identity, "meaning": meaning, "valid_for_claim": False, "timestamp_utc": timestamp} for row_id, identity, meaning in rows]


def base_flags() -> dict[str, str]:
    return {"source_signed": "true", "units_signed": "true", "same_branch_signed": "true", "no_cancellation_guard": "true"}


def zero_flags() -> dict[str, str]:
    return {
        **base_flags(),
        "corrected_gamma_normalization_signed": "true",
        "candidate_action_adopted_private_signed": "true",
        "response_doublet_parent_owned_signed": "true",
        "exchange_symmetry_signed": "true",
        "ordinary_matter_exchange_even_signed": "true",
        "no_linear_even_Z_source_signed": "true",
        "positive_operator_gap_signed": "true",
        "local_odd_source_zero_signed": "true",
        "boundary_flux_zero_signed": "true",
        "zero_mode_removed_signed": "true",
        "on_shell_Euler_signed": "true",
        "Gamma0_local_constant_signed": "true",
        "same_action_metric_response_signed": "true",
        "coefficients_regular_at_origin_signed": "true",
        "no_direct_Z_readout_signed": "true",
        "background_force_retained_or_bounded_signed": "true",
    }


def runner_inputs(timestamp: str) -> list[dict[str, Any]]:
    reactivated = zero_flags()
    reactivated["local_odd_source_zero_signed"] = "false"
    return [
        {
            "row_id": "RUN4845_0_live_global_zero_missing",
            "route_type": "active_zero",
            "route": "current global MTS Gamma active-zero attempt",
            "source_path": str(SOURCES["contract"]),
            "equation_ref": "RD516_0..6",
            "notes": "global parent adoption, source and boundary clauses remain unsigned",
            "corrected_gamma_normalization_signed": "true",
            "timestamp_utc": timestamp,
            **base_flags(),
        },
        {
            "row_id": "RUN4845_1_private_candidate_active_zero_pass",
            "route_type": "active_zero",
            "route": "post-checkpoint response-doublet positive-action local zero",
            "source_path": str(SOURCES["quadratic"]),
            "equation_ref": "QMA970_1; QMA970_2; AV517_3; LST4845_1",
            "notes": "private candidate theorem; Gamma0 retained separately",
            "timestamp_utc": timestamp,
            **zero_flags(),
        },
        {
            "row_id": "RUN4845_2_odd_source_reactivation_control",
            "route_type": "active_zero",
            "route": "nonzero local odd-source reactivation control",
            "source_path": str(SOURCES["sources"]),
            "equation_ref": "response-doublet Euler source ledger",
            "notes": "failed J_loc zero must reopen the finite branch",
            "timestamp_utc": timestamp,
            **reactivated,
        },
        {
            "row_id": "RUN4845_3_live_quadratic_bound_missing",
            "route_type": "quadratic_bound",
            "route": "live finite Gamma carrier suppression bound",
            "source_path": str(SOURCES["quadratic"]),
            "equation_ref": "||Z||<=(||J||+B)/lambda_gap",
            "notes": "physical source, gap, response coefficient and arena values missing",
            "candidate_action_adopted_private_signed": "true",
            "same_action_metric_response_signed": "true",
            "timestamp_utc": timestamp,
            **base_flags(),
        },
        {
            "row_id": "RUN4845_4_quadratic_bound_smoke_pass",
            "route_type": "quadratic_bound",
            "route": "quadratic source-suppression arithmetic smoke",
            "source_path": str(SOURCES["quadratic"]),
            "equation_ref": "LST4845_2 through LST4845_4",
            "notes": "rounded nonclaim schema smoke",
            "candidate_action_adopted_private_signed": "true",
            "same_action_metric_response_signed": "true",
            "J_Z_norm_m2": "2.0e-50",
            "boundary_lift_norm_m2": "1.0e-50",
            "lambda_gap_m2": "1.0e-40",
            "C_Sigma_quad_m2": "1.0e-32",
            "R_higher_m2": "1.0e-53",
            "radius_m": "1.0e11",
            "GM_m3_s2": "1.0e20",
            "timestamp_utc": timestamp,
            **base_flags(),
        },
        {
            "row_id": "RUN4845_5_constant_background_smoke_pass",
            "route_type": "constant_background",
            "route": "constant Gamma0 background retained comparator smoke",
            "source_path": str(SOURCES["doc_4844"]),
            "equation_ref": "constant spherical Sigma_Gamma profile",
            "notes": "Gamma0 is retained, not erased by active-background subtraction",
            "Gamma0_background_m2": "1.0e-52",
            "radius_m": "1.0e11",
            "GM_m3_s2": "1.0e20",
            "timestamp_utc": timestamp,
            **base_flags(),
        },
        {
            "row_id": "RUN4845_6_positive_exchange_sign_pass",
            "route_type": "exchange_balance",
            "route": "positive-sign Bianchi exchange balance",
            "source_path": str(SOURCES["parent_eq"]),
            "equation_ref": "nabla X=kappa nabla T=q",
            "notes": "matches the parent q convention with X on the left",
            "div_X_Gamma_m3": "2.0e-60",
            "kappa_div_Tmatter_m3": "2.0e-60",
            "exchange_tolerance_m3": "1.0e-70",
            "timestamp_utc": timestamp,
            **base_flags(),
        },
        {
            "row_id": "RUN4845_7_negative_exchange_sign_control_fails",
            "route_type": "exchange_balance",
            "route": "negative-sign exchange control",
            "source_path": str(SOURCES["core_consistency"]),
            "equation_ref": "older negative-sign line",
            "notes": "control demonstrates the sign mismatch",
            "div_X_Gamma_m3": "2.0e-60",
            "kappa_div_Tmatter_m3": "-2.0e-60",
            "exchange_tolerance_m3": "1.0e-70",
            "timestamp_utc": timestamp,
            **base_flags(),
        },
        {
            "row_id": "RUN4845_8_forbidden_qloc_to_full_sigma",
            "route_type": "active_zero",
            "route": "forbidden qloc shortcut",
            "source_path": str(SOURCES["physical_lock"]),
            "equation_ref": "RG2973_4_q_loc_implication",
            "notes": "QLOC_ZERO_IMPLIES_SIGMA_ZERO is forbidden without this action theorem",
            "timestamp_utc": timestamp,
            **zero_flags(),
        },
        {
            "row_id": "RUN4845_9_forbidden_background_drop",
            "route_type": "constant_background",
            "route": "forbidden background deletion",
            "source_path": str(SOURCES["metric"]),
            "equation_ref": "MR517_4_fixed_point_stress",
            "notes": "BACKGROUND_SUBTRACTION_DROPS_FORCE is forbidden",
            "timestamp_utc": timestamp,
            **base_flags(),
        },
        {
            "row_id": "RUN4845_10_forbidden_even_stress_erasure",
            "route_type": "active_zero",
            "route": "forbidden exchange-even stress erasure",
            "source_path": str(SOURCES["sources"]),
            "equation_ref": "Y6_stress_Bianchi",
            "notes": "EXCHANGE_SYMMETRY_KILLS_EVEN_STRESS is forbidden",
            "timestamp_utc": timestamp,
            **zero_flags(),
        },
        {
            "row_id": "RUN4845_11_forbidden_bound_as_source",
            "route_type": "quadratic_bound",
            "route": "forbidden bound inversion",
            "source_path": str(SOURCES["quadratic"]),
            "equation_ref": "finite suppression comparator",
            "notes": "BOUND_AS_SOURCE cannot define J, lambda_gap or C_Sigma",
            "timestamp_utc": timestamp,
            **base_flags(),
        },
        {
            "row_id": "RUN4845_12_forbidden_measured_GM_source",
            "route_type": "quadratic_bound",
            "route": "forbidden orbital source backfill",
            "source_path": str(SOURCES["matter_4843"]),
            "equation_ref": "no measured GM absorption",
            "notes": "MEASURED_GM_AS_SOURCE is forbidden",
            "timestamp_utc": timestamp,
            **base_flags(),
        },
    ]


def run_runner() -> list[dict[str, str]]:
    subprocess.run([sys.executable, str(RUNNER), str(RUNNER_INPUT), str(RUNNER_OUTPUT)], check=True)
    return read_csv(RUNNER_OUTPUT)


def row_by_id(rows: list[dict[str, str]], row_id: str) -> dict[str, str]:
    return next(row for row in rows if row.get("row_id") == row_id)


def compile_ok(path: Path) -> bool:
    try:
        py_compile.compile(str(path), doraise=True)
    except py_compile.PyCompileError:
        return False
    return True


def cleanup_pycache() -> None:
    pycache = SCRIPT_DIR / "__pycache__"
    if pycache.exists():
        shutil.rmtree(pycache)


def decision_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {"decision_id": "DEC4845_0_construct", "decision": "Adopt the response-doublet positive Gamma carrier as a private post-checkpoint candidate action.", "effect": "turns local silence into an Euler/positivity theorem rather than a plateau closure", "valid_for_claim": False, "timestamp_utc": timestamp},
        {"decision_id": "DEC4845_1_bound", "decision": "Off the exact local branch, Sigma_active is quadratic in odd source and boundary lift over the positive gap.", "effect": "supplies a finite Newton/orbital acceleration bound", "valid_for_claim": False, "timestamp_utc": timestamp},
        {"decision_id": "DEC4845_2_scope", "decision": "Gamma-carrier silence does not erase constant Gamma0, even stress, source-current, PPN or boundary sectors.", "effect": "prevents q_loc zero from being promoted to full local GR", "valid_for_claim": False, "timestamp_utc": timestamp},
        {"decision_id": "DEC4845_3_next", "decision": NEXT_TARGET, "effect": "derive the cosmology/local source split or fill the first physical SigmaGamma arena row", "valid_for_claim": False, "timestamp_utc": timestamp},
    ]


def claim_gate_rows(timestamp: str) -> list[dict[str, Any]]:
    rows = [
        ("CG4845_0_candidate", "response-doublet action constructed", "PASS_PRIVATE_CANDIDATE", "same action owns Gamma carrier and metric response"),
        ("CG4845_1_zero", "source-free active Gamma zero", "PASS_CONDITIONAL_PRIVATE", "positive gap plus zero source/boundary forces Z=0"),
        ("CG4845_2_bound", "quadratic finite suppression", "PASS_FORMULA_VALUES_MISSING", "physical J/gap/response/arena row still needed"),
        ("CG4845_3_background", "constant Gamma0 retained", "PASS_FIREWALL", "background acceleration is scored separately"),
        ("CG4845_4_exchange", "Bianchi exchange sign", "PASS_CORRECTED", "nabla X=kappa nabla T with X on the left"),
        ("CG4845_5_global", "global MTS adoption", "BLOCKED", "candidate is not uniquely derived/adopted by the whole corpus"),
        ("CG4845_6_local_GR", "full local GR/Newton/PPN", "NOT_ALLOWED", "non-Gamma residuals remain"),
    ]
    return [{"gate_id": gate_id, "gate": gate, "status": status, "meaning": meaning, "valid_for_claim": False, "timestamp_utc": timestamp} for gate_id, gate, status, meaning in rows]


def write_resume(timestamp: str) -> None:
    write_text(RESUME_PATH, f"""# Current local resume

Updated: `{timestamp}`
Last checkpoint: `4845-Y5-R2FR-Gamma-local-constancy-exchange-and-SigmaGamma-profile-bound.md`
Marker: `{MARKER}`

## Where we are

4843 restored ordinary source universality. 4844 corrected the Gamma action normalization and derived the trace-reversed source. 4845 now constructs a non-plateau local suppression mechanism:

```text
Gamma_eff = Gamma0
          + 1/2 A_AB^mn nabla_m Z^A nabla_n Z^B
          + 1/2 M2_AB Z^A Z^B - J_A Z^A + O(Z^4)
S_Gamma = -(1/kappa) int sqrt(-g) Gamma_eff
L_AB Z^B = J_A + O(Z^3)
```

Exchange symmetry makes `Z` odd and ordinary local matter even. On the private candidate branch, `J_loc=0`, boundary flux is zero and the positive gap removes zero modes. The energy identity then forces:

```text
Z=0
Gamma_active=Pi_active=Sigma_active=q_Gamma=0.
```

If source or boundary leakage survives:

```text
||Z|| <= (||J||+B_lift)/lambda_gap
||Sigma_active|| <= C_Sigma ((||J||+B_lift)/lambda_gap)^2 + R_higher.
```

## Live blockers

- The candidate action is adopted only inside post-checkpoint private work, not globally derived from every original MTS primitive.
- The cosmology/local activation split must derive `J_cos/history != 0` while keeping ordinary local `J_loc=0`; no arbitrary environment switch is allowed.
- A physical row still needs `J_Z`, boundary lift, `lambda_gap`, `C_Sigma`, radius and an independent source mass.
- `Gamma0` remains a constant background force and must be bounded; it is not deleted by reference subtraction.
- Gamma-carrier silence does not erase even stress, non-source PPN, boundary, non-Hilbert or source-current residuals.

## Next target

`{NEXT_TARGET}`
""")


def validate(timestamp: str, sources: list[dict[str, Any]], outputs: list[dict[str, str]]) -> list[dict[str, Any]]:
    checks: list[dict[str, Any]] = []

    def add(check_id: str, passed: bool, detail: str) -> None:
        checks.append({"check_id": check_id, "passed": bool(passed), "status": "PASS" if passed else "FAIL", "detail": detail, "timestamp_utc": timestamp})

    add("VAL4845_00_sources_exist", all(str(row["exists"]) == "True" for row in sources), "all cited source paths exist")
    add("VAL4845_01_needles_found", all(str(row["needle_found"]) == "True" for row in sources), "all cited source needles found")
    add("VAL4845_02_runner_compiles", compile_ok(RUNNER), "runner compiles")
    add("VAL4845_03_generator_compiles", compile_ok(Path(__file__)), "generator compiles")
    inputs = read_csv(RUNNER_INPUT)
    add("VAL4845_04_output_count", len(outputs) == len(inputs), f"outputs={len(outputs)} inputs={len(inputs)}")
    add("VAL4845_05_claims_false", all(row.get("claim_allowed") == "False" and row.get("valid_for_claim") == "False" for row in outputs), "all rows remain nonclaim")
    live_zero = row_by_id(outputs, "RUN4845_0_live_global_zero_missing")
    add("VAL4845_06_live_zero_blocked", live_zero["runner_status"] == "BLOCKED_GAMMA_ACTIVE_LOCAL_ZERO", live_zero["missing_for_claim"])
    candidate = row_by_id(outputs, "RUN4845_1_private_candidate_active_zero_pass")
    add("VAL4845_07_candidate_zero", candidate["runner_status"] == "GAMMA_ACTIVE_LOCAL_ZERO_PASS_PRIVATE_NONCLAIM" and all(close_to(candidate[field], 0.0) for field in ("Z_H1_bound", "Gamma_active_bound_m2", "Pi_active_bound_m2", "Sigma_active_bound_m2", "q_Gamma_bound_m3")), "candidate active Gamma zero propagates")
    reactivation = row_by_id(outputs, "RUN4845_2_odd_source_reactivation_control")
    add("VAL4845_08_reactivation", reactivation["runner_status"] == "BLOCKED_GAMMA_ACTIVE_LOCAL_ZERO" and "MISSING_local_odd_source_zero_signed" in reactivation["missing_for_claim"], "odd source reopens finite route")
    live_bound = row_by_id(outputs, "RUN4845_3_live_quadratic_bound_missing")
    add("VAL4845_09_live_bound_blocked", live_bound["runner_status"] == "BLOCKED_GAMMA_QUADRATIC_SUPPRESSION_BOUND", live_bound["missing_for_claim"])
    smoke = row_by_id(outputs, "RUN4845_4_quadratic_bound_smoke_pass")
    z_expected = 3.0e-10
    sigma_expected = 9.1e-52
    fraction_expected = (C_LIGHT**2) * sigma_expected * 1.0e33 / (3.0e20)
    add("VAL4845_10_bound_smoke", close_to(smoke["Z_H1_bound"], z_expected) and close_to(smoke["Sigma_active_bound_m2"], sigma_expected) and close_to(smoke["fractional_acceleration_bound"], fraction_expected), "quadratic suppression arithmetic passes")
    background = row_by_id(outputs, "RUN4845_5_constant_background_smoke_pass")
    background_expected = (C_LIGHT**2) * 1.0e-52 * 1.0e33 / (3.0e20)
    add("VAL4845_11_background", close_to(background["background_fractional_acceleration"], background_expected), "constant background remains explicitly scored")
    exchange_ok = row_by_id(outputs, "RUN4845_6_positive_exchange_sign_pass")
    exchange_bad = row_by_id(outputs, "RUN4845_7_negative_exchange_sign_control_fails")
    add("VAL4845_12_exchange_sign", exchange_ok["runner_status"] == "GAMMA_EXCHANGE_BALANCE_PASS_NONCLAIM" and exchange_bad["runner_status"] == "BLOCKED_GAMMA_EXCHANGE_BALANCE", "positive Bianchi sign passes and negative control fails")
    forbidden = [row for row in outputs if row["row_id"].startswith("RUN4845_8_") or row["row_id"].startswith("RUN4845_9_") or row["row_id"].startswith("RUN4845_10_") or row["row_id"].startswith("RUN4845_11_") or row["row_id"].startswith("RUN4845_12_")]
    add("VAL4845_13_forbidden", all(row["runner_status"] == "FAILED_FORBIDDEN_SOURCE_OR_CIRCULAR_ROUTE" for row in forbidden), "all qloc/background/even-stress/bound/source shortcuts fail")
    add("VAL4845_14_resume", NEXT_TARGET in read_text(RESUME_PATH) and "non-plateau local suppression mechanism" in read_text(RESUME_PATH), "resume records theorem and next activation target")
    cleanup_pycache()
    add("VAL4845_15_no_pycache", not (SCRIPT_DIR / "__pycache__").exists(), "scripts __pycache__ removed")
    return checks


def write_docs(timestamp: str, sources: list[dict[str, Any]], action: list[dict[str, Any]], theorem: list[dict[str, Any]], exchange: list[dict[str, Any]], outputs: list[dict[str, str]], validations: list[dict[str, Any]]) -> None:
    doc = f"""# 4845 Y5 R2FR Gamma local constancy exchange and SigmaGamma profile bound

**Status:** 4845 constructs the local suppression mechanism that the previous plateau route lacked. The private post-checkpoint candidate uses an exchange-odd response doublet and a positive action. Its Euler equation forces the active Gamma carrier to zero in a source-free closed local collar, while a nonzero source produces a quadratic, executable `Sigma_Gamma` bound. The constant background `Gamma0` is retained explicitly.

**Decision:** `{DECISION}`.

## Candidate action

Use the 4844 normalization repair and define:

```text
Z^A = (R_+^A-R_-^A)/2,                  E: Z^A -> -Z^A
Gamma_eff = Gamma0
          + 1/2 A_AB^mn nabla_m Z^A nabla_n Z^B
          + 1/2 M2_AB Z^A Z^B - J_A Z^A + O(Z^4)
S_Gamma = -(1/kappa) int sqrt(-g) Gamma_eff.
```

Ordinary matter belongs to the exchange-even visible branch established in 4843. Therefore it cannot generate a linear exchange-odd `J_A Z^A` vertex. Odd history, boundary or transition sources are not erased; they are the finite `J_A` branch.

Variation gives:

```text
L_AB Z^B = J_A + O(Z^3),
L_AB = -nabla_m(A_AB^mn nabla_n) + M2_AB.
```

The algebraic auxiliary limit is `A=0`. The dynamic local limit keeps the positive derivative operator.

## Local zero theorem

On a fixed local collar:

```text
<Z,LZ> = ||Z||_L^2 = <Z,J> + B_boundary.
```

If `lambda_gap>0`, `J_loc=0`, the boundary flux vanishes and gauge/zero modes are removed, positivity forces:

```text
Z=0 and nabla Z=0.
```

Exchange evenness and regular same-action metric response then give:

```text
Gamma_active=0,
Pi_active=0,
Sigma_active=Gamma_active-2Pi_active,00-Pi_active=0,
q_Gamma=nabla_m X_Gamma^mn=0.
```

This is an Euler/energy theorem, not an inserted local-vacuum plateau.

## Finite quadratic branch

For nonzero odd source or boundary lift:

```text
||Z||_H1 <= (||J_Z||+B_lift)/lambda_gap,
||Sigma_active|| <= C_Sigma [(||J_Z||+B_lift)/lambda_gap]^2 + R_higher,
epsilon_a <= c^2 r^3 ||Sigma_active||/(3GM).
```

The absence of a linear term is the useful physical payoff: local active gravity is quadratically suppressed in the exchange-odd source. A real prediction still needs sourced `J_Z`, boundary lift, gap, response coefficient and arena data.

## Background and exchange

The split is:

```text
Sigma_total = Gamma0 + Sigma_active.
```

`Gamma0` is not deleted. If constant it has `q=0` but still produces the de-Sitter `r` acceleration scored by the runner.

With `X_Gamma` on the left of `G+X=kappa T`:

```text
nabla_m X_Gamma^mn = kappa nabla_m T_matter^mn = q_Gamma^n.
```

This positive sign matches the parent equation `K_MTS=-X` and `q=nabla K_matter`. The older negative-sign sentence in the repair note is inconsistent with its displayed Einstein equation and is not carried forward.

## Scope guard

This action controls the Gamma carrier. It does not prove that every source, PPN, even-stress, boundary or readout residual is a component of `Z`. In particular, `q_Gamma=0` alone does not imply full local GR.

## Source register

{md_table(sources, ["source_id", "exists", "needle_found", "role"])}

## Action construction

{md_table(action, ["construction_id", "object", "formula", "meaning"])}

## Suppression theorem

{md_table(theorem, ["theorem_id", "object", "formula", "consequence"])}

## Bianchi exchange map

{md_table(exchange, ["exchange_id", "identity", "meaning"])}

## Runner output

{md_table(outputs, ["row_id", "runner_status", "Z_H1_bound", "Sigma_active_bound_m2", "fractional_acceleration_bound", "background_fractional_acceleration", "exchange_balance_residual_m3", "missing_for_claim"])}

## Validation

{md_table(validations, ["check_id", "status", "detail"])}

## What changed

- The local Gamma route now has a concrete parent-action candidate and a proof, not a plateau declaration.
- Exact local active silence and finite quadratic suppression are two branches of the same Euler equation.
- The Bianchi exchange sign is reconciled with the parent tensor split.
- Cosmological activation and the first physical local profile row are now the next real tests.

## Next target

`{NEXT_TARGET}`
"""
    write_text(DOC_PATH, doc)
    write_text(FORMAL_PATH, f"""# 861 PPC4161 Gamma local constancy exchange and SigmaGamma profile bound

Checkpoint: `{DOC_PATH}`

4845 adopts a private post-checkpoint response-doublet Gamma carrier with an exchange-even positive action. The Euler/energy identity proves `Z=Gamma_active=Pi_active=Sigma_active=q_Gamma=0` on a source-free closed local collar. Off branch, `Sigma_active` is quadratically bounded by `[(||J||+B)/lambda_gap]^2`. Constant `Gamma0` remains an explicit background force.

The construction controls only the Gamma carrier and makes no full local-GR claim. Global MTS adoption, cosmological activation and physical coefficient rows remain open.

Decision: `{DECISION}`

Runner: `{RUNNER}`

Next: `{NEXT_TARGET}`
""")


def update_formal_registers(timestamp: str) -> None:
    claim_row = {
        "claim_id": CLAIM_ID,
        "domain": "local_gr",
        "claim": "Gamma_local_constancy_exchange_and_SigmaGamma_profile_bound",
        "current_evidence": "4845 constructs a response-doublet positive Gamma action whose Euler identity gives exact active local silence and a quadratic finite source bound.",
        "status": "Gamma_response_doublet_private_candidate_nonclaim",
        "next_test": NEXT_TARGET,
        "key_risk": "global parent adoption, cosmology/local source split and physical J/gap/response rows remain open",
        "sector": "local_gr_Newton_metric_residual",
        "evidence": str(DOC_PATH),
        "next_action": NEXT_TARGET,
        "risk": "Gamma-carrier theorem must not be promoted to full PPN/source/even-stress closure",
        "title": "Gamma local constancy exchange and SigmaGamma profile bound",
        "notes": f"{MARKER}; {DECISION}; generated {timestamp}",
    }
    if CLAIM_ID not in read_text(CLAIMS_PATH):
        with CLAIMS_PATH.open("a", encoding="utf-8", newline="") as handle:
            csv.DictWriter(handle, fieldnames=list(claim_row.keys())).writerow(claim_row)
    append_once(SPINE_PATH, MARKER, f"""## PPC4161 4845 Gamma response-doublet local suppression

`{MARKER}` constructs a private positive response-doublet action. Source-free local positivity forces `Z=0`, hence `Gamma_active=Pi_active=Sigma_active=q_Gamma=0`; finite odd source or boundary leakage gives a quadratic `Sigma_active` and acceleration bound. Constant `Gamma0` remains explicit, and unrelated PPN/source/even-stress residuals survive. Decision: `{DECISION}`.""")
    append_once(PACKET_PATH, PACKET_MARKER, f"""## 4845 Gamma response-doublet local suppression

`{PACKET_MARKER}` replaces the local plateau idea with an Euler/energy mechanism. The next task is to derive the cosmology/local source split or fill the first physical `Sigma_Gamma` arena row. Next: `{NEXT_TARGET}`.""")


def main() -> None:
    timestamp = now()
    write_resume(timestamp)
    sources = source_register(timestamp)
    action = action_rows(timestamp)
    theorem = theorem_rows(timestamp)
    exchange = exchange_rows(timestamp)
    inputs = runner_inputs(timestamp)
    write_csv(SOURCE_REGISTER, sources)
    write_csv(ACTION_CONSTRUCTION, action)
    write_csv(SUPPRESSION_THEOREM, theorem)
    write_csv(EXCHANGE_MAP, exchange)
    write_csv(RUNNER_INPUT, inputs)
    write_csv(DECISION_CSV, decision_rows(timestamp))
    write_csv(CLAIM_GATES, claim_gate_rows(timestamp))
    write_csv(STATUS_CSV, [{"checkpoint": CHECKPOINT, "marker": MARKER, "decision": DECISION, "status": "private_candidate_nonclaim", "live_claim_allowed": False, "next_target": NEXT_TARGET, "timestamp_utc": timestamp}])
    write_csv(NEXT_TARGET_CSV, [{"checkpoint": CHECKPOINT, "next_target": NEXT_TARGET, "reason": "derive cosmology/local source activation without an arbitrary selector or source a physical SigmaGamma row", "valid_for_claim": False, "timestamp_utc": timestamp}])
    outputs = run_runner()
    cleanup_pycache()
    validations = validate(timestamp, sources, outputs)
    write_csv(VALIDATION_CSV, validations)
    write_docs(timestamp, sources, action, theorem, exchange, outputs, validations)
    update_formal_registers(timestamp)
    cleanup_pycache()
    failed = [row for row in validations if not row["passed"]]
    if failed:
        raise SystemExit(f"4845 validation failed: {failed}")
    print(f"4845 complete: {DOC_PATH}")


if __name__ == "__main__":
    main()

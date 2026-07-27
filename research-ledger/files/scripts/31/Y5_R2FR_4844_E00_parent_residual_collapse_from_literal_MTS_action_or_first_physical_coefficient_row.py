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

CHECKPOINT = "4844"
CLAIM_ID = "L-686"
MARKER = "PPC4161_E00_PARENT_RESIDUAL_COLLAPSE_FROM_LITERAL_MTS_ACTION_OR_FIRST_PHYSICAL_COEFFICIENT_ROW_4844"
PACKET_MARKER = "PPC4161_PACKET_GAMMA_ACTION_TRACE_REVERSED_E00_4844"
DECISION = "LITERAL_ACTION_FACTOR_TWO_GAMMA_NORMALIZATION_MISMATCH_AND_TRACE_REVERSED_NEWTON_SOURCE_DERIVED_CORRECTED_ACTION_CANDIDATE_STAGED_NONCLAIM"
NEXT_TARGET = "4845-Y5-R2FR-Gamma-local-constancy-exchange-and-SigmaGamma-profile-bound.md"
C_LIGHT = 299_792_458.0

DOC_PATH = POST / "4844-Y5-R2FR-E00-parent-residual-collapse-from-literal-MTS-action-or-first-physical-coefficient-row.md"
FORMAL_PATH = FORMAL / "860-PPC4161-E00-parent-residual-collapse-from-literal-MTS-action-or-first-physical-coefficient-row.md"
CLAIMS_PATH = FORMAL / "02-claims-register.csv"
SPINE_PATH = FORMAL / "07-unification-spine.md"
PACKET_PATH = FORMAL / "180-PPC4161-private-local-packet-integration.md"
RESUME_PATH = POST / "CURRENT_LOCAL_RESUME.md"
RUNNER = SCRIPT_DIR / "gamma_action_E00_trace_reverse_runner.py"

SOURCE_REGISTER = SOURCE_DIR / "P8_Y5_R2FR_4844_SOURCE_REGISTER.csv"
ACTION_AUDIT = SOURCE_DIR / "P8_Y5_R2FR_4844_GAMMA_ACTION_VARIATION_AUDIT.csv"
TRACE_MAP = SOURCE_DIR / "P8_Y5_R2FR_4844_TRACE_REVERSED_NEWTON_MAP.csv"
RUNNER_INPUT = SOURCE_DIR / "P8_Y5_R2FR_4844_GAMMA_E00_RUNNER_INPUT.csv"
RUNNER_OUTPUT = SOURCE_DIR / "P8_Y5_R2FR_4844_GAMMA_E00_RUNNER_OUTPUT.csv"
DECISION_CSV = SOURCE_DIR / "P8_Y5_R2FR_4844_DECISION_LEDGER.csv"
CLAIM_GATES = SOURCE_DIR / "P8_Y5_R2FR_4844_CLAIM_GATES.csv"
STATUS_CSV = SOURCE_DIR / "P8_Y5_R2FR_4844_STATUS.csv"
NEXT_TARGET_CSV = SOURCE_DIR / "P8_Y5_R2FR_4844_NEXT_TARGET.csv"
VALIDATION_CSV = SOURCE_DIR / "P8_Y5_BRR545_4844_VALIDATION.csv"

SOURCES = {
    "resume": RESUME_PATH,
    "core_action": ROOT / "core-mts-framework" / "action-principle" / "the-motion-timespace-action-principle.md",
    "fundamental_action": ROOT / "core-mts-framework" / "action-principle" / "the-fundamental-action-of-motion-timespace-field-theory.md",
    "weak_field": FORMAL / "34-weak-field-projection-derivation.md",
    "consistency": FORMAL / "10-core-consistency-repair.md",
    "equations": FORMAL / "05-equation-register.md",
    "poisson_4719": POST / "4719-Y5-R2FR-local-linearized-GR-limit-and-Poisson-equation-residual-bound.md",
    "eh_4720": POST / "4720-Y5-R2FR-EH-reduction-parent-signature-or-nonEH-operator-coefficient-matrix.md",
    "reconcile_4843": DOC_PATH.parent / "4843-Y5-R2FR-source-universality-branch-reconciliation-and-Newton-chain-propagation.md",
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
        ("SRC4844_00_resume", SOURCES["resume"], "4844-Y5-R2FR-E00-parent-residual-collapse", "4843 selected the literal-action E00 target"),
        ("SRC4844_01_core_action", SOURCES["core_action"], "must contain a term whose variation contributes exactly", "literal action and claimed Gamma field term"),
        ("SRC4844_02_core_equation", SOURCES["core_action"], "Collecting all contributions yields:", "claimed extended Einstein equation"),
        ("SRC4844_03_fundamental_action", SOURCES["fundamental_action"], "The minimal covariant scalar capable of generating", "second statement of Gamma action normalization"),
        ("SRC4844_04_weak_trace", SOURCES["weak_field"], "Use the trace-reversed Einstein equation:", "correct Newtonian curvature projection"),
        ("SRC4844_05_weak_MTS", SOURCES["weak_field"], "S_MTS,00", "trace-reversed MTS source precedent"),
        ("SRC4844_06_consistency", SOURCES["consistency"], "ordinary matter stress-energy is not separately conserved", "Bianchi/exchange-current guard"),
        ("SRC4844_07_equation_redflag", SOURCES["equations"], "its variation is not simply", "metric-dependence variation warning"),
        ("SRC4844_08_poisson_4719", SOURCES["poisson_4719"], "nabla^2 Phi_N = 4*pi*G_eff*rho + (c^2/2)E_00", "raw E00 Poisson map to correct"),
        ("SRC4844_09_eh_4720", SOURCES["eh_4720"], "Lambda_eff_local", "local vacuum residual family"),
        ("SRC4844_10_reconcile_4843", SOURCES["reconcile_4843"], "The next derivation target moves to the metric side", "source-prefactor handoff"),
        ("SRC4844_11_runner", SOURCES["runner"], "def evaluate_row", "4844 action/trace-reverse runner"),
        ("SRC4844_12_generator", SOURCES["generator"], 'CHECKPOINT = "4844"', "4844 generator and validator"),
    ]


def source_register(timestamp: str) -> list[dict[str, Any]]:
    rows = []
    for source_id, path, needle, role in source_specs():
        text = read_text(path)
        rows.append(
            {
                "checkpoint": CHECKPOINT,
                "source_id": source_id,
                "source_path": str(path),
                "exists": path.exists(),
                "needle": needle,
                "needle_found": needle in text,
                "role": role,
                "valid_for_claim": False,
                "timestamp_utc": timestamp,
            }
        )
    return rows


def action_audit_rows(timestamp: str) -> list[dict[str, Any]]:
    rows = [
        ("GAV4844_0_parameterization", "Gamma action normalization", "S_Gamma=-(a_Gamma/kappa) int sqrt(-g) Gamma_G", "DEFINITION", "core literal action has a_Gamma=2"),
        ("GAV4844_1_variation", "metric variation", "G_mn+a_Gamma Gamma_G g_mn-2 a_Gamma Pi_Gamma_mn=kappa T_mn", "EXACT_VARIATION", "Pi_Gamma_mn:=delta Gamma_G/delta g^mn"),
        ("GAV4844_2_literal_factor", "literal core coefficient", "a_Gamma=2", "FACTOR_TWO_MISMATCH", "metric-independent limit gives G_mn+2 Gamma_G g_mn=kappa T_mn"),
        ("GAV4844_3_corrected_factor", "coefficient required by claimed equation", "a_Gamma=1", "CORRECTED_ACTION_CANDIDATE", "use L_LambdaKappa=Gamma_G/kappa for G_mn+Gamma_G g_mn when Pi=0"),
        ("GAV4844_4_metric_response", "dynamic Gamma response", "Pi_Gamma_mn=delta Gamma_G/delta g^mn", "MANDATORY_IF_GAMMA_DEPENDS_ON_METRIC_HISTORY", "cannot vary Gamma_G as an external constant and later call it dynamical"),
        ("GAV4844_5_Bianchi", "local conservation", "nabla^m X_mn=kappa nabla^m T_mn", "CONSTANT_OR_EXCHANGE_REQUIRED", "if Pi=0 and matter is conserved then partial_n Gamma_G=0 locally"),
        ("GAV4844_6_scope", "meaning of correction", "normalization repair plus exact residual map", "CORRECTABLE_NOT_LOCAL_GR_CLAIM", "Gamma profile/exchange and all other non-EH residuals remain"),
    ]
    return [
        {
            "audit_id": audit_id,
            "object": obj,
            "formula": formula,
            "result": result,
            "consequence": consequence,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
        for audit_id, obj, formula, result, consequence in rows
    ]


def trace_map_rows(timestamp: str) -> list[dict[str, Any]]:
    rows = [
        ("TRN4844_0_X", "Einstein-form residual", "X_mn=a_Gamma(Gamma_G g_mn-2 Pi_Gamma_mn)", "enters G_mn+X_mn=kappa T_mn"),
        ("TRN4844_1_trace", "residual trace", "X=a_Gamma(4 Gamma_G-2 Pi_Gamma)", "needed before Newton projection"),
        ("TRN4844_2_trace_reverse", "trace-reversed residual", "Xbar_00=X_00-(1/2)g_00 X", "raw E_00 alone is insufficient for generic residuals"),
        ("TRN4844_3_sigma", "physical local Gamma source", "Sigma_Gamma=a_Gamma[Gamma_G-2 Pi_Gamma_00-Pi_Gamma] for g_00~-1", "units m^-2"),
        ("TRN4844_4_Poisson", "corrected Newton equation", "nabla^2 Phi=4 pi G rho-c^2 Sigma_Gamma+other trace-reversed residuals", "positive constant Gamma gives de-Sitter outward acceleration"),
        ("TRN4844_5_profile", "constant spherical profile", "Delta a_r=(c^2/3) Sigma_Gamma r; |Delta a|/(GM/r^2)=c^2 |Sigma_Gamma| r^3/(3GM)", "local profile/arena comparator ready"),
        ("TRN4844_6_threshold", "arena threshold", "|Sigma_Gamma|<=3 tau_a GM/(c^2 r^3)", "bound is comparator only and cannot define Gamma_G"),
        ("TRN4844_7_4719_repair", "4719 raw E00 map", "replace raw +(c^2/2)E_00 by source-family-specific trace-reversed map", "EH harmonic identity remains useful only after spatial/trace equations are controlled"),
    ]
    return [
        {
            "map_id": map_id,
            "object": obj,
            "formula": formula,
            "meaning": meaning,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
        for map_id, obj, formula, meaning in rows
    ]


def base_flags() -> dict[str, str]:
    return {
        "source_signed": "true",
        "units_signed": "true",
        "same_branch_signed": "true",
        "no_cancellation_guard": "true",
    }


def runner_inputs(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "row_id": "RUN4844_0_literal_action_factor_two_detected",
            "route_type": "action_normalization",
            "route": "literal core MTS Gamma action normalization",
            "source_path": str(SOURCES["core_action"]),
            "equation_ref": "core action lines 116 and 131; claimed field equation line 165",
            "notes": "a_Gamma=2 from -L_LambdaKappa but target coefficient is one",
            "a_gamma_action": "2.0",
            "target_field_equation_coefficient": "1.0",
            "timestamp_utc": timestamp,
            **base_flags(),
        },
        {
            "row_id": "RUN4844_1_corrected_action_candidate_pass",
            "route_type": "action_normalization",
            "route": "corrected Gamma action coefficient candidate",
            "source_path": str(SOURCES["core_action"]),
            "equation_ref": "S_Gamma=-(1/kappa) int sqrt(-g) Gamma_G",
            "notes": "candidate correction only; no core document changed",
            "a_gamma_action": "1.0",
            "target_field_equation_coefficient": "1.0",
            "timestamp_utc": timestamp,
            **base_flags(),
        },
        {
            "row_id": "RUN4844_2_live_trace_source_missing",
            "route_type": "trace_reversed_source",
            "route": "live Gamma metric-response trace source",
            "source_path": str(SOURCES["equations"]),
            "equation_ref": "Gamma variation metric-dependence red flag",
            "notes": "Gamma_G and Pi_Gamma profile values are not yet supplied",
            "a_gamma_action": "1.0",
            "timestamp_utc": timestamp,
            **base_flags(),
        },
        {
            "row_id": "RUN4844_3_trace_response_smoke_pass",
            "route_type": "trace_reversed_source",
            "route": "trace-response arithmetic smoke",
            "source_path": str(SOURCES["weak_field"]),
            "equation_ref": "trace-reversed Einstein source",
            "notes": "nonclaim units/arithmetic smoke",
            "a_gamma_action": "1.0",
            "Gamma_G_m2": "2.0e-52",
            "Pi_Gamma_00_m2": "2.0e-53",
            "Pi_Gamma_trace_m2": "3.0e-53",
            "timestamp_utc": timestamp,
            **base_flags(),
        },
        {
            "row_id": "RUN4844_4_constant_profile_smoke_pass",
            "route_type": "constant_spherical_profile",
            "route": "constant spherical Gamma profile arithmetic smoke",
            "source_path": str(SOURCES["weak_field"]),
            "equation_ref": "TRN4844_4_Poisson; TRN4844_5_profile",
            "notes": "rounded synthetic values; not a physical MTS prediction row",
            "a_gamma_action": "1.0",
            "Gamma_G_m2": "1.0e-52",
            "Pi_Gamma_00_m2": "0.0",
            "Pi_Gamma_trace_m2": "0.0",
            "radius_m": "1.0e11",
            "GM_m3_s2": "1.0e20",
            "timestamp_utc": timestamp,
            **base_flags(),
        },
        {
            "row_id": "RUN4844_5_local_threshold_smoke_pass",
            "route_type": "local_sigma_threshold",
            "route": "local acceleration comparator threshold smoke",
            "source_path": str(SOURCES["poisson_4719"]),
            "equation_ref": "|Sigma_Gamma|<=3 tau GM/(c^2 r^3)",
            "notes": "comparator only; cannot be inverted into parent Gamma coefficient",
            "fractional_acceleration_tolerance": "1.0e-10",
            "radius_m": "1.0e11",
            "GM_m3_s2": "1.0e20",
            "timestamp_utc": timestamp,
            **base_flags(),
        },
        {
            "row_id": "RUN4844_6_Bianchi_constant_Gamma_pass",
            "route_type": "bianchi_gate",
            "route": "locally constant Gamma with separately conserved matter",
            "source_path": str(SOURCES["consistency"]),
            "equation_ref": "nabla X=0 when partial Gamma=0",
            "notes": "constant local vacuum branch",
            "matter_separately_conserved_signed": "true",
            "Gamma_G_local_constant_signed": "true",
            "metric_response_or_exchange_signed": "false",
            "timestamp_utc": timestamp,
            **base_flags(),
        },
        {
            "row_id": "RUN4844_7_Bianchi_variable_external_blocked",
            "route_type": "bianchi_gate",
            "route": "variable external Gamma without response/exchange",
            "source_path": str(SOURCES["consistency"]),
            "equation_ref": "Bianchi exchange-current requirement",
            "notes": "control must block variable Gamma if no dynamic response or matter exchange is signed",
            "matter_separately_conserved_signed": "true",
            "Gamma_G_local_constant_signed": "false",
            "metric_response_or_exchange_signed": "false",
            "timestamp_utc": timestamp,
            **base_flags(),
        },
        {
            "row_id": "RUN4844_8_forbidden_ignore_factor_two",
            "route_type": "action_normalization",
            "route": "forbidden normalization shortcut",
            "source_path": str(SOURCES["core_action"]),
            "equation_ref": "literal action mismatch",
            "notes": "IGNORE_FACTOR_TWO is forbidden",
            "timestamp_utc": timestamp,
            **base_flags(),
        },
        {
            "row_id": "RUN4844_9_forbidden_raw_E00",
            "route_type": "trace_reversed_source",
            "route": "forbidden raw E00 projection",
            "source_path": str(SOURCES["poisson_4719"]),
            "equation_ref": "raw E00 map",
            "notes": "RAW_E00_WITHOUT_TRACE_REVERSE is forbidden for a generic residual",
            "timestamp_utc": timestamp,
            **base_flags(),
        },
        {
            "row_id": "RUN4844_10_forbidden_variable_Gamma_no_exchange",
            "route_type": "bianchi_gate",
            "route": "forbidden variable Gamma declaration",
            "source_path": str(SOURCES["consistency"]),
            "equation_ref": "exchange-current requirement",
            "notes": "VARIABLE_EXTERNAL_GAMMA_NO_EXCHANGE is forbidden",
            "timestamp_utc": timestamp,
            **base_flags(),
        },
        {
            "row_id": "RUN4844_11_forbidden_bound_as_source",
            "route_type": "local_sigma_threshold",
            "route": "forbidden comparator inversion",
            "source_path": str(SOURCES["poisson_4719"]),
            "equation_ref": "Sigma_Gamma threshold",
            "notes": "BOUND_AS_SOURCE cannot define Gamma_G or Pi_Gamma",
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
        {
            "decision_id": "DEC4844_0_factor",
            "decision": "The literal core action coefficient a_Gamma=2 does not produce the claimed +Gamma_G g_mn field term under standard variation.",
            "effect": "corrected candidate uses a_Gamma=1; original main documents remain checkpointed and unchanged",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "decision_id": "DEC4844_1_trace",
            "decision": "The Newton source is the trace-reversed Sigma_Gamma=a_Gamma(Gamma_G-2Pi_00-Pi), not raw E_00.",
            "effect": "replaces a generic raw-E00 shortcut with the correct physical acceleration source",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "decision_id": "DEC4844_2_next",
            "decision": NEXT_TARGET,
            "effect": "derive local constancy/exchange or fill a physical Sigma_Gamma profile row",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
    ]


def claim_gate_rows(timestamp: str) -> list[dict[str, Any]]:
    rows = [
        ("CG4844_0_variation", "Gamma action variation", "PASS_EXACT", "coefficient and metric-response terms derived explicitly"),
        ("CG4844_1_literal_normalization", "literal action matches claimed equation", "FAIL_FACTOR_TWO", "a_Gamma=2 but claimed coefficient is one"),
        ("CG4844_2_corrected_candidate", "corrected action candidate", "PASS_NONCLAIM", "a_Gamma=1 gives claimed coefficient only when metric response is controlled"),
        ("CG4844_3_trace_reverse", "Newton source mapping", "PASS_EXACT", "Sigma_Gamma is trace-reversed physical source"),
        ("CG4844_4_Bianchi", "variable Gamma consistency", "BLOCKED_LIVE", "local constancy or dynamic response/exchange must be signed"),
        ("CG4844_5_profile", "physical local Sigma_Gamma row", "MISSING", "Gamma/Pi profile and arena provenance are not yet supplied"),
        ("CG4844_6_local_GR", "Newton/local-GR claim", "NOT_ALLOWED", "other metric, PPN, boundary and source-current residuals remain"),
    ]
    return [
        {
            "gate_id": gate_id,
            "gate": gate,
            "status": status,
            "meaning": meaning,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
        for gate_id, gate, status, meaning in rows
    ]


def write_resume(timestamp: str) -> None:
    write_text(
        RESUME_PATH,
        f"""# Current local resume

Updated: `{timestamp}`
Last checkpoint: `4844-Y5-R2FR-E00-parent-residual-collapse-from-literal-MTS-action-or-first-physical-coefficient-row.md`
Marker: `{MARKER}`

## Where we are

4843 restored source universality on the literal/private matter branch. 4844 then derives the first live metric-side correction directly from the written MTS action.

The action is parameterized as:

```text
S_Gamma = -(a_Gamma/kappa) int sqrt(-g) Gamma_G
G_mn + a_Gamma Gamma_G g_mn - 2 a_Gamma Pi_Gamma_mn = kappa T_mn
Pi_Gamma_mn := delta Gamma_G/delta g^mn
```

The literal core text has `a_Gamma=2` but claims a unit coefficient. Standard variation therefore exposes a correctable factor-two mismatch. The corrected candidate is `a_Gamma=1`.

For the Newtonian limit, the physical source is trace-reversed:

```text
Sigma_Gamma = a_Gamma (Gamma_G - 2 Pi_Gamma_00 - Pi_Gamma)
nabla^2 Phi = 4 pi G rho - c^2 Sigma_Gamma + other residuals
```

## Live blockers

- `Gamma_G`, `Pi_Gamma_00` and `Pi_Gamma` still need a same-branch local profile or a zero theorem.
- If `Gamma_G` varies, the metric response/dynamic field equation or matter-exchange current is mandatory by Bianchi consistency.
- The core action documents have not been altered; 4844 stages the corrected action in post-checkpoint work.
- Source-prefactor zero from 4843 remains active; non-source PPN, boundary, non-Hilbert and physical source-current gates remain.

## Next target

`{NEXT_TARGET}`
""",
    )


def validate(timestamp: str, sources: list[dict[str, Any]], outputs: list[dict[str, str]]) -> list[dict[str, Any]]:
    checks: list[dict[str, Any]] = []

    def add(check_id: str, passed: bool, detail: str) -> None:
        checks.append(
            {
                "check_id": check_id,
                "passed": bool(passed),
                "status": "PASS" if passed else "FAIL",
                "detail": detail,
                "timestamp_utc": timestamp,
            }
        )

    add("VAL4844_00_sources_exist", all(str(row["exists"]) == "True" for row in sources), "all cited source paths exist")
    add("VAL4844_01_needles_found", all(str(row["needle_found"]) == "True" for row in sources), "all cited source needles found")
    add("VAL4844_02_runner_compiles", compile_ok(RUNNER), "runner compiles")
    add("VAL4844_03_generator_compiles", compile_ok(Path(__file__)), "generator compiles")
    inputs = read_csv(RUNNER_INPUT)
    add("VAL4844_04_output_count", len(outputs) == len(inputs), f"outputs={len(outputs)} inputs={len(inputs)}")
    add("VAL4844_05_claims_false", all(row.get("claim_allowed") == "False" and row.get("valid_for_claim") == "False" for row in outputs), "all rows remain nonclaim")
    literal = row_by_id(outputs, "RUN4844_0_literal_action_factor_two_detected")
    add("VAL4844_06_literal_mismatch", literal["runner_status"] == "ACTION_NORMALIZATION_MISMATCH_DETECTED" and close_to(literal["normalization_mismatch_abs"], 1.0), "literal a_Gamma=2 mismatch detected")
    corrected = row_by_id(outputs, "RUN4844_1_corrected_action_candidate_pass")
    add("VAL4844_07_corrected_candidate", corrected["runner_status"] == "ACTION_NORMALIZATION_PASS_NONCLAIM" and close_to(corrected["normalization_mismatch_abs"], 0.0), "a_Gamma=1 candidate matches claimed coefficient")
    live = row_by_id(outputs, "RUN4844_2_live_trace_source_missing")
    add("VAL4844_08_live_trace_blocked", live["runner_status"] == "BLOCKED_TRACE_REVERSED_GAMMA_SOURCE", live["missing_for_claim"])
    trace = row_by_id(outputs, "RUN4844_3_trace_response_smoke_pass")
    expected_sigma = 1.3e-52
    add("VAL4844_09_trace_smoke", close_to(trace["Sigma_Gamma_m2"], expected_sigma) and close_to(trace["Delta_Poisson_Gamma_s2"], -(C_LIGHT**2) * expected_sigma), "trace-response Sigma and Poisson source compute")
    profile = row_by_id(outputs, "RUN4844_4_constant_profile_smoke_pass")
    expected_acceleration = (C_LIGHT**2) * 1.0e-52 * 1.0e11 / 3.0
    expected_fraction = (C_LIGHT**2) * 1.0e-52 * 1.0e33 / (3.0e20)
    add("VAL4844_10_profile_smoke", close_to(profile["delta_acceleration_m_s2"], expected_acceleration) and close_to(profile["fractional_acceleration_abs"], expected_fraction), "constant spherical profile arithmetic passes")
    threshold = row_by_id(outputs, "RUN4844_5_local_threshold_smoke_pass")
    expected_bound = 3.0 * 1.0e-10 * 1.0e20 / ((C_LIGHT**2) * 1.0e33)
    add("VAL4844_11_threshold_smoke", close_to(threshold["Sigma_Gamma_bound_m2"], expected_bound), "local comparator threshold arithmetic passes")
    bianchi_pass = row_by_id(outputs, "RUN4844_6_Bianchi_constant_Gamma_pass")
    bianchi_fail = row_by_id(outputs, "RUN4844_7_Bianchi_variable_external_blocked")
    add("VAL4844_12_Bianchi_controls", bianchi_pass["runner_status"] == "BIANCHI_GAMMA_GATE_PASS_NONCLAIM" and bianchi_fail["runner_status"] == "BLOCKED_BIANCHI_GAMMA_GATE", "constant branch passes and variable external Gamma blocks")
    forbidden = [row for row in outputs if row["row_id"].startswith("RUN4844_8_") or row["row_id"].startswith("RUN4844_9_") or row["row_id"].startswith("RUN4844_10_") or row["row_id"].startswith("RUN4844_11_")]
    add("VAL4844_13_forbidden_routes", all(row["runner_status"] == "FAILED_FORBIDDEN_SOURCE_OR_CIRCULAR_ROUTE" for row in forbidden), "factor, trace, exchange and bound shortcuts fail")
    add("VAL4844_14_resume_next", NEXT_TARGET in read_text(RESUME_PATH) and "factor-two mismatch" in read_text(RESUME_PATH), "resume records derivation and next profile target")
    cleanup_pycache()
    add("VAL4844_15_no_pycache", not (SCRIPT_DIR / "__pycache__").exists(), "scripts __pycache__ removed")
    return checks


def write_docs(timestamp: str, sources: list[dict[str, Any]], audit: list[dict[str, Any]], trace_map: list[dict[str, Any]], outputs: list[dict[str, str]], validations: list[dict[str, Any]]) -> None:
    doc = f"""# 4844 Y5 R2FR E00 parent residual collapse from literal MTS action or first physical coefficient row

**Status:** 4844 derives the metric-side `Gamma_G` contribution directly from the literal MTS action. It finds a correctable factor-two normalization error in the existing core text and replaces the generic raw-`E_00` Newton shortcut with the correct trace-reversed source `Sigma_Gamma`. No core document is changed at this checkpoint.

**Decision:** `{DECISION}`.

## Exact action variation

Parameterize the vacuum/exchange term as:

```text
S_Gamma = -(a_Gamma/kappa) int sqrt(-g) Gamma_G
Pi_Gamma_mn := delta Gamma_G / delta g^mn
```

Using `delta sqrt(-g)=-1/2 sqrt(-g) g_mn delta g^mn` and the standard Hilbert definition of `T_mn` gives:

```text
G_mn + a_Gamma Gamma_G g_mn - 2 a_Gamma Pi_Gamma_mn = kappa T_mn.
```

The literal core action writes `L_LambdaKappa=2 Gamma_G/kappa` and subtracts it, so `a_Gamma=2`. If `Pi_Gamma_mn=0`, that action yields:

```text
G_mn + 2 Gamma_G g_mn = kappa T_mn,
```

not the claimed unit-coefficient equation. The minimal correction is:

```text
L_LambdaKappa = Gamma_G/kappa,
```

equivalently `a_Gamma=1`. If `Gamma_G` depends on the metric, memory, or fields, the `Pi_Gamma_mn` term is mandatory even after this normalization repair.

## Trace-reversed Newton source

Define:

```text
X_mn = a_Gamma (Gamma_G g_mn - 2 Pi_Gamma_mn)
Xbar_mn = X_mn - 1/2 g_mn X.
```

For `g_00~-1`:

```text
Sigma_Gamma := Xbar_00
             = a_Gamma (Gamma_G - 2 Pi_Gamma_00 - Pi_Gamma).
```

The Newton equation is therefore:

```text
nabla^2 Phi = 4 pi G rho - c^2 Sigma_Gamma
              + other trace-reversed residuals.
```

For a constant spherical `Sigma_Gamma`:

```text
Delta Phi = -(c^2 Sigma_Gamma/6) r^2
Delta a_r = +(c^2 Sigma_Gamma/3) r
|Delta a|/(GM/r^2) = c^2 |Sigma_Gamma| r^3/(3GM).
```

This also shows why a raw Einstein-form `E_00` is not enough for a generic residual: its trace/spatial equations decide the force potential.

## Bianchi gate

If matter is separately conserved:

```text
nabla^m X_mn = 0.
```

For `Pi_Gamma_mn=0`, this forces `partial_n Gamma_G=0` in the local branch. A varying `Gamma_G` therefore requires a dynamic response tensor and its field equation, or an explicit matter-exchange current; it cannot be varied as a constant and interpreted as dynamical afterward.

## Source register

{md_table(sources, ["source_id", "exists", "needle_found", "role"])}

## Action audit

{md_table(audit, ["audit_id", "object", "formula", "result", "consequence"])}

## Trace-reversed map

{md_table(trace_map, ["map_id", "object", "formula", "meaning"])}

## Runner output

{md_table(outputs, ["row_id", "runner_status", "field_equation_gamma_coefficient", "normalization_mismatch_abs", "Sigma_Gamma_m2", "Delta_Poisson_Gamma_s2", "fractional_acceleration_abs", "missing_for_claim"])}

## Validation

{md_table(validations, ["check_id", "status", "detail"])}

## What changed

- A real algebraic error is identified and locally repaired: the written potential coefficient is twice the value required by the claimed equation.
- The physically relevant Newton source is now `Sigma_Gamma`, which includes metric response and trace information.
- Constant and varying `Gamma_G` branches are separated by an executable Bianchi gate.
- The next target is no longer a vague `E_00` coefficient: it is a local `Gamma_G/Pi_Gamma` profile or a same-branch constancy/exchange theorem.

## Next target

`{NEXT_TARGET}`
"""
    write_text(DOC_PATH, doc)
    write_text(
        FORMAL_PATH,
        f"""# 860 PPC4161 E00 parent residual collapse from literal MTS action or first physical coefficient row

Checkpoint: `{DOC_PATH}`

4844 derives the exact `Gamma_G` action response. For `S_Gamma=-(a_Gamma/kappa) int sqrt(-g) Gamma_G`, the field equation contains `a_Gamma Gamma_G g_mn-2a_Gamma Pi_Gamma_mn`. The literal core text has `a_Gamma=2`, so it yields a factor-two coefficient relative to its claimed equation. The corrected candidate uses `a_Gamma=1`.

The Newton source is trace-reversed: `Sigma_Gamma=a_Gamma(Gamma_G-2Pi_Gamma_00-Pi_Gamma)` and `nabla^2 Phi=4piG rho-c^2 Sigma_Gamma+...`. A varying external `Gamma_G` without response/exchange fails the Bianchi gate.

Decision: `{DECISION}`

Runner: `{RUNNER}`

Next: `{NEXT_TARGET}`
""",
    )


def update_formal_registers(timestamp: str) -> None:
    claim_row = {
        "claim_id": CLAIM_ID,
        "domain": "local_gr",
        "claim": "E00_parent_residual_collapse_from_literal_MTS_action_or_first_physical_coefficient_row",
        "current_evidence": "4844 derives the exact Gamma action variation, identifies the literal factor-two normalization mismatch, and replaces raw E00 with the trace-reversed Sigma_Gamma Newton source.",
        "status": "Gamma_action_trace_reverse_runner_private_nonclaim",
        "next_test": NEXT_TARGET,
        "key_risk": "local Gamma/Pi profile and dynamic exchange/Bianchi closure remain missing",
        "sector": "local_gr_Newton_metric_residual",
        "evidence": str(DOC_PATH),
        "next_action": NEXT_TARGET,
        "risk": "corrected action candidate is not yet adopted globally and no physical local Sigma_Gamma row exists",
        "title": "E00 parent residual collapse from literal MTS action or first physical coefficient row",
        "notes": f"{MARKER}; {DECISION}; generated {timestamp}",
    }
    if CLAIM_ID not in read_text(CLAIMS_PATH):
        with CLAIMS_PATH.open("a", encoding="utf-8", newline="") as handle:
            csv.DictWriter(handle, fieldnames=list(claim_row.keys())).writerow(claim_row)
    append_once(
        SPINE_PATH,
        MARKER,
        f"""## PPC4161 4844 Gamma action normalization and trace-reversed E00

`{MARKER}` derives `G_mn+a_Gamma Gamma_G g_mn-2a_Gamma Pi_Gamma_mn=kappa T_mn` from the literal potential action. The core text's `a_Gamma=2` is inconsistent with its claimed unit coefficient; `a_Gamma=1` is the staged correction. The Newton source is `Sigma_Gamma=a_Gamma(Gamma_G-2Pi_Gamma_00-Pi_Gamma)`, not raw `E_00`, and a varying Gamma requires dynamic response/exchange by Bianchi consistency. Decision: `{DECISION}`.""",
    )
    append_once(
        PACKET_PATH,
        PACKET_MARKER,
        f"""## 4844 Gamma action / trace-reversed E00

`{PACKET_MARKER}` converts the metric-side residual into a concrete action-normalization and profile problem. Use `a_Gamma=1` for the claimed unit-coefficient equation, retain `Pi_Gamma_mn` whenever Gamma is dynamical, and score local gravity through `Sigma_Gamma`. Next: `{NEXT_TARGET}`.""",
    )


def main() -> None:
    timestamp = now()
    write_resume(timestamp)
    sources = source_register(timestamp)
    audit = action_audit_rows(timestamp)
    trace_map = trace_map_rows(timestamp)
    inputs = runner_inputs(timestamp)
    write_csv(SOURCE_REGISTER, sources)
    write_csv(ACTION_AUDIT, audit)
    write_csv(TRACE_MAP, trace_map)
    write_csv(RUNNER_INPUT, inputs)
    write_csv(DECISION_CSV, decision_rows(timestamp))
    write_csv(CLAIM_GATES, claim_gate_rows(timestamp))
    write_csv(STATUS_CSV, [{"checkpoint": CHECKPOINT, "marker": MARKER, "decision": DECISION, "status": "private_nonclaim_derivation", "live_claim_allowed": False, "next_target": NEXT_TARGET, "timestamp_utc": timestamp}])
    write_csv(NEXT_TARGET_CSV, [{"checkpoint": CHECKPOINT, "next_target": NEXT_TARGET, "reason": "derive local Gamma constancy/exchange or fill the physical trace-reversed Sigma_Gamma profile", "valid_for_claim": False, "timestamp_utc": timestamp}])
    outputs = run_runner()
    cleanup_pycache()
    validations = validate(timestamp, sources, outputs)
    write_csv(VALIDATION_CSV, validations)
    write_docs(timestamp, sources, audit, trace_map, outputs, validations)
    update_formal_registers(timestamp)
    cleanup_pycache()
    failed = [row for row in validations if not row["passed"]]
    if failed:
        raise SystemExit(f"4844 validation failed: {failed}")
    print(f"4844 complete: {DOC_PATH}")


if __name__ == "__main__":
    main()

from __future__ import annotations

import csv
import math
import sys
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
RESIDUALS = ROOT / "source-intake" / "mts_residuals"
LOCAL_BOUNDS = ROOT / "source-intake" / "local_bounds"
FORMALIZATION = ROOT.parent / "formalization-workbench"
CHECKPOINT_ID = "3667"
BRANCH_ID = "MTS_R2FR_Y5_FEM_ZX_PROFILE_NORMALIZATION_PROOF_OR_FIRST_BOUND_ROW_3667"
DOC = ROOT / "3667-Y5-R2FR-fEM-ZX-profile-normalization-proof-or-first-bound-row.md"

LAMBDA_RATIOS = [0.01, 0.1, 1.0, 10.0, 100.0]


def stamp() -> str:
    return datetime.now(timezone.utc).isoformat()


def base(ts: str) -> dict[str, object]:
    return {
        "timestamp_utc": ts,
        "branch_id": BRANCH_ID,
        "checkpoint_id": CHECKPOINT_ID,
        "valid_for_claim": False,
    }


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace") if path.exists() else ""


def load_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fields: list[str] = []
    for row in rows:
        for key in row:
            if key not in fields:
                fields.append(key)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def parse_csv(path: Path) -> tuple[bool, int]:
    try:
        with path.open("r", newline="", encoding="utf-8") as handle:
            rows = list(csv.DictReader(handle))
        return True, len(rows)
    except Exception:
        return False, 0


def scalar_from_3666_status() -> tuple[float, float, float]:
    rows = load_csv(RESIDUALS / "P8_Y5_R2FR_3666_STATUS.csv")
    if not rows:
        raise RuntimeError("missing 3666 status")
    return (
        float(rows[0]["solar_B_source_EM_total"]),
        float(rows[0]["cassini_gamma_upper_bound"]),
        float(rows[0]["solar_limb_Phi_N_abs_proxy"]),
    )


def r_proxy_from_3666() -> float:
    rows = load_csv(RESIDUALS / "P8_Y5_R2FR_3666_SOLAR_LIMB_GEOMETRY_PROXY.csv")
    if not rows:
        raise RuntimeError("missing 3666 solar-limb geometry proxy")
    return float(rows[0]["r_proxy_m"])


def source_register(ts: str) -> list[dict[str, object]]:
    specs = [
        ("handoff_3666", RESIDUALS / "P8_Y5_R2FR_3666_NEXT_TARGET.csv", "3667-Y5-R2FR-fEM-ZX-profile-normalization-proof-or-first-bound-row.md", "3666 selected this target"),
        ("doc_3666", ROOT / "3666-Y5-R2FR-solar-EM-gamma-envelope-stub-or-fEM-profile-inputs.md", "Q_X^EM_solar = B_source_EM_solar * f_EM", "3666 inserted solar EM source into gamma envelope"),
        ("status_3666", RESIDUALS / "P8_Y5_R2FR_3666_STATUS.csv", "SOLAR_EM_SOURCE_INSERTED_IN_GAMMA_ENVELOPE_NONCLAIM", "3666 scalar/bound/proxy values"),
        ("envelope_3666", RESIDUALS / "P8_Y5_R2FR_3666_INSERTED_SOLAR_GAMMA_ENVELOPE.csv", "ENV3666_2_gamma_EM_profile_bound", "3666 gamma envelope formula"),
        ("geometry_3666", RESIDUALS / "P8_Y5_R2FR_3666_SOLAR_LIMB_GEOMETRY_PROXY.csv", "SLG3666_0_solar_limb_proxy", "3666 solar-limb proxy values"),
        ("requirements_3666", RESIDUALS / "P8_Y5_R2FR_3666_FEM_PROFILE_INPUT_REQUIREMENTS.csv", "REQ3666_4_kG", "3666 open profile/coupling inputs"),
        ("fem_audit_3665", RESIDUALS / "P8_Y5_R2FR_3665_UNIQUE_F2_CLOSURE_AUDIT.csv", "REJECT_ZERO_RETAIN_FINITE_COUPLING_INPUT", "f_EM zero obstruction"),
        ("em_lock_3649", RESIDUALS / "P8_Y5_R2FR_3649_EM_LOCK_CLAUSE_AUDIT.csv", "FAIL_CURRENT_CORPUS_COUNTERTERM_LEGAL", "EM same-frame lock obstruction"),
        ("profile_3658", RESIDUALS / "P8_Y5_R2FR_3658_GAMMA_PROFILE_COEFFICIENT_ROWS.csv", "Yukawa_like_profile", "Yukawa profile kernels"),
        ("bound_formula_3660", RESIDUALS / "P8_Y5_R2FR_3660_GAMMA_BOUND_FORMULAS.csv", "GBF3660_1_gamma_profile_envelope", "Cassini envelope formula"),
        ("hessian_1025", ROOT / "1025-Y5-R10-parent-Hessian-ZX-MX2-range-or-alpha-source-row.md", "lambda_X=sqrt(Z_X/M_X^2)", "Z_X/M_X^2/lambda normalization contract"),
        ("local_bounds", LOCAL_BOUNDS / "local_bound_claims.csv", "Cassini_Shapiro_gamma_2003", "Cassini gamma external comparator row"),
    ]
    rows = []
    for source_id, path, needle, role in specs:
        body = read_text(path)
        rows.append(
            {
                **base(ts),
                "source_id": source_id,
                "path": str(path),
                "exists": path.exists(),
                "needle": needle,
                "needle_found": needle in body,
                "role": role,
            }
        )
    return rows


def closure_attempt_rows(ts: str) -> list[dict[str, object]]:
    return [
        {
            **base(ts),
            "attempt_id": "CLO3667_0_fEM_zero",
            "object": "f_EM zero",
            "derived_statement": "f_EM=0 would follow from a parent unique-F2/no-f_XF2 theorem, but 3649/3665 leave the scalar gauge-kinetic counterterm legal.",
            "formula": "DeltaL=-(1/4) f_X(X_N) F_Q^2 is still allowed unless parent grammar forbids it",
            "result": "ZERO_NOT_CLOSED",
            "accepted_as_zero": False,
            "claim_allowed": False,
        },
        {
            **base(ts),
            "attempt_id": "CLO3667_1_range_chain",
            "object": "Z_X and lambda_X",
            "derived_statement": "For a scalar-like finite branch, the same parent quadratic block gives lambda_X=sqrt(Z_X/M_X^2); this is an exact relation but not a parent-owned numeric value.",
            "formula": "S_X~int[1/2 Z_X |grad X|^2 + 1/2 M_X^2 X^2 - J_X X] => lambda_X=sqrt(Z_X/M_X^2)",
            "result": "RELATION_DERIVED_VALUES_MISSING",
            "accepted_as_zero": False,
            "claim_allowed": False,
        },
        {
            **base(ts),
            "attempt_id": "CLO3667_2_normalization_degeneracy",
            "object": "f_EM/Z_X measurable combinations",
            "derived_statement": "The Cassini EM profile branch cannot separately measure f_EM and Z_X; it sees projection-normalized combinations with k_H, k_G, lambda_X, and the transfer kernel.",
            "formula": "delta_gamma_EM <= C_H(lambda)*mu_H + C_G(lambda)*mu_G + C_other, with mu_H=|k_H f_EM/Z_X| and mu_G=|k_G| f_EM^2/Z_X^2",
            "result": "NORMALIZED_COMBINATION_DERIVED",
            "accepted_as_zero": False,
            "claim_allowed": False,
        },
        {
            **base(ts),
            "attempt_id": "CLO3667_3_projection_status",
            "object": "k_H and k_G",
            "derived_statement": "k_H and k_G are the weak-field projection coefficients from radial profile derivatives into gamma slip; current files derive the profile kernels but do not parent-sign the projection coefficients.",
            "formula": "H=e^(-r/lambda)*(3/r^3+3/(lambda*r^2)+1/(lambda^2*r)); G=e^(-2r/lambda)*(1/r^2+1/(lambda*r))^2",
            "result": "PROFILE_KERNEL_DERIVED_PROJECTION_COEFFICIENTS_MISSING",
            "accepted_as_zero": False,
            "claim_allowed": False,
        },
    ]


def normalized_combination_rows(ts: str, b_sun: float, bound: float) -> list[dict[str, object]]:
    return [
        {
            **base(ts),
            "combo_id": "NC3667_0_muH",
            "symbol": "mu_H",
            "definition": "linear Hessian-STF normalized EM coupling",
            "formula": "mu_H(lambda)=|K_gamma_H(lambda) k_H f_EM/Z_X|",
            "enters_bound_as": "C_H(lambda)*mu_H",
            "coefficient_formula": f"C_H(lambda)=({b_sun:.12e}/(4*pi))*H(r,lambda)/|Phi_N(r)|",
            "cassini_upper_bound": f"{bound:.12e}",
            "current_status": "DERIVED_MEASURABLE_COMBINATION_NONCLAIM",
            "score_ready": False,
            "claim_allowed": False,
        },
        {
            **base(ts),
            "combo_id": "NC3667_1_muG",
            "symbol": "mu_G",
            "definition": "quadratic gradient-square-STF normalized EM coupling",
            "formula": "mu_G(lambda)=|K_gamma_G(lambda) k_G| f_EM^2/Z_X^2",
            "enters_bound_as": "C_G(lambda)*mu_G",
            "coefficient_formula": f"C_G(lambda)=({b_sun:.12e}^2/(16*pi^2))*G(r,lambda)/|Phi_N(r)|",
            "cassini_upper_bound": f"{bound:.12e}",
            "current_status": "DERIVED_MEASURABLE_COMBINATION_NONCLAIM",
            "score_ready": False,
            "claim_allowed": False,
        },
        {
            **base(ts),
            "combo_id": "NC3667_2_joint",
            "symbol": "delta_gamma_EM_envelope",
            "definition": "joint EM profile bound in normalized variables",
            "formula": "C_H(lambda)*mu_H + C_G(lambda)*mu_G + |C_other_gamma| <= B_gamma_Cassini",
            "enters_bound_as": "first finite nonclaim gamma-bound row",
            "coefficient_formula": "H/G kernels use 3658 Yukawa profile; 3667 solar-limb values are scale proxies, not Cassini transfer kernels",
            "cassini_upper_bound": f"{bound:.12e}",
            "current_status": "BOUND_ROW_REDUCED_TO_NORMALIZED_COUPLINGS",
            "score_ready": False,
            "claim_allowed": False,
        },
    ]


def h_kernel(r: float, lam: float) -> float:
    ratio = r / lam
    return math.exp(-ratio) * (3.0 / r**3 + 3.0 / (lam * r**2) + 1.0 / (lam**2 * r))


def g_kernel(r: float, lam: float) -> float:
    ratio = r / lam
    return math.exp(-2.0 * ratio) * (1.0 / r**2 + 1.0 / (lam * r)) ** 2


def finite_bound_rows(ts: str, b_sun: float, bound: float, phi_abs: float, r_proxy: float) -> list[dict[str, object]]:
    rows = []
    for ratio in LAMBDA_RATIOS:
        lam = ratio * r_proxy
        h_value = h_kernel(r_proxy, lam)
        g_value = g_kernel(r_proxy, lam)
        c_h = (b_sun / (4.0 * math.pi)) * h_value / phi_abs
        c_g = (b_sun**2 / (16.0 * math.pi**2)) * g_value / phi_abs
        mu_h_max = bound / c_h if c_h > 0.0 else math.inf
        mu_g_max = bound / c_g if c_g > 0.0 else math.inf
        rows.append(
            {
                **base(ts),
                "bound_id": f"FB3667_lambda_over_r_{ratio:g}",
                "lambda_over_r_proxy": f"{ratio:.12e}",
                "lambda_proxy_m": f"{lam:.12e}",
                "r_proxy_m": f"{r_proxy:.12e}",
                "Phi_N_abs_proxy": f"{phi_abs:.12e}",
                "H_kernel_proxy": f"{h_value:.12e}",
                "G_kernel_proxy": f"{g_value:.12e}",
                "C_H_proxy": f"{c_h:.12e}",
                "C_G_proxy": f"{c_g:.12e}",
                "mu_H_max_if_muG_Cother_zero": f"{mu_h_max:.12e}",
                "mu_G_max_if_muH_Cother_zero": f"{mu_g_max:.12e}",
                "joint_bound_formula": f"{c_h:.12e}*mu_H + {c_g:.12e}*mu_G + |C_other_gamma| <= {bound:.12e}",
                "current_status": "FIRST_FINITE_BOUND_ROW_SCALE_PROXY_NONCLAIM",
                "why_nonclaim": "K_gamma transfer kernel, k_H/k_G units, Z_X normalization, lambda_X parent range, and C_other_gamma are not sourced; solar-limb substitution is a scale proxy",
                "score_ready": False,
                "claim_allowed": False,
            }
        )
    return rows


def input_status_rows(ts: str) -> list[dict[str, object]]:
    specs = [
        ("IN3667_0_fEM_zero", "f_EM zero theorem", "ZERO_NOT_CLOSED", "unique-F2/no-f_XF2 parent signature"),
        ("IN3667_1_ZX", "Z_X normalization", "RELATION_ONLY", "parent quadratic action/Hessian with units"),
        ("IN3667_2_lambda", "lambda_X range", "RELATION_ONLY", "same-branch M_X^2/Z_X value or range theorem"),
        ("IN3667_3_kH", "k_H projection", "MISSING_WEAK_FIELD_PROJECTION", "derive metric slip response coefficient"),
        ("IN3667_4_kG", "k_G projection", "MISSING_WEAK_FIELD_PROJECTION", "prove gradient-square absence or source coefficient"),
        ("IN3667_5_Kgamma", "K_gamma transfer", "MISSING_CASSINI_TRANSFER_KERNEL", "path/impact/readout kernel"),
        ("IN3667_6_Cother", "C_other_gamma floor", "MISSING_COMPONENT_BOUNDS", "boundary/readout/source/nonEH bounds or zero theorem"),
        ("IN3667_7_QnonEM", "Q_X non-EM components", "RETAINED_SOURCE_COMPONENTS", "mass/nuclear/alpha/source-marker/boundary rows"),
    ]
    return [
        {
            **base(ts),
            "input_id": input_id,
            "quantity": quantity,
            "current_status": status,
            "needed_for_claim": needed,
            "claim_allowed": False,
        }
        for input_id, quantity, status, needed in specs
    ]


def claim_gate_rows(ts: str) -> list[dict[str, object]]:
    specs = [
        ("CG3667_0_fEM_zero", "f_EM=0 parent theorem", "FAILED_UNSIGNED_COUNTERTERM_LIVE", "scalar gauge-kinetic counterterm remains legal"),
        ("CG3667_1_normalized_combo", "derive measurable gamma combinations", "PASSED_DERIVATION", "mu_H and mu_G isolate what Cassini can actually bound"),
        ("CG3667_2_first_bound_row", "stage first finite gamma-bound row", "PASSED_SCALE_PROXY_NONCLAIM", "lambda/r sample rows produced with solar-limb proxy"),
        ("CG3667_3_numeric_score", "claim-grade Cassini gamma score", "BLOCKED_BY_KERNEL_AND_PARENT_COEFFICIENTS", "K_gamma, k_H/k_G, lambda_X, Z_X, C_other, and non-EM pieces remain open"),
        ("CG3667_4_local_GR_claim", "local-GR/PPN pass", "ACTIVE_GUARD", "finite bound scaffold is not a local-GR derivation"),
    ]
    return [
        {
            **base(ts),
            "gate_id": gate_id,
            "gate": gate,
            "status": status,
            "reason": reason,
            "claim_allowed": False,
        }
        for gate_id, gate, status, reason in specs
    ]


def status_rows(ts: str, b_sun: float, bound: float, phi_abs: float, r_proxy: float) -> list[dict[str, object]]:
    return [
        {
            **base(ts),
            "status": "NORMALIZED_GAMMA_COUPLINGS_DERIVED_FIRST_BOUND_ROW_NONCLAIM",
            "summary": "3667 refuses the unsigned f_EM zero, derives that Cassini constrains normalized combinations mu_H=|K_gamma_H k_H f_EM/Z_X| and mu_G=|K_gamma_G k_G|f_EM^2/Z_X^2 rather than f_EM or Z_X separately, and stages first finite scale-proxy bound rows.",
            "solar_B_source_EM_total": f"{b_sun:.12e}",
            "cassini_gamma_upper_bound": f"{bound:.12e}",
            "solar_limb_Phi_N_abs_proxy": f"{phi_abs:.12e}",
            "r_proxy_m": f"{r_proxy:.12e}",
            "claim_ceiling": "no f_EM zero, Cassini/gamma score, local-GR, PPN, WEP/R10, Newtonian, source-calibration, or EH-dominance pass is claimed",
            "useful_result": "The next hunt is narrowed: derive k_H/k_G and K_gamma or prove they vanish; do not keep asking for f_EM alone.",
        }
    ]


def next_rows(ts: str) -> list[dict[str, object]]:
    return [
        {
            **base(ts),
            "next_id": "NEXT3667_0",
            "target_doc": "3668-Y5-R2FR-kH-kG-weak-field-projection-zero-or-transfer-kernel-bound.md",
            "target_script": "scripts/Y5_R2FR_3668_kH_kG_weak_field_projection_zero_or_transfer_kernel_bound.py",
            "objective": "derive whether the weak-field projection coefficients k_H and k_G vanish or are fixed by the same-frame metric response; if not, stage K_gamma transfer-kernel and coefficient bound rows",
            "success_gate": "either k_H/k_G profile leakage is parent-zero, or the normalized gamma-bound scaffold has explicit coefficient/kernel rows ready for nonclaim finite scoring",
        }
    ]


def write_doc(
    sources: list[dict[str, object]],
    closure: list[dict[str, object]],
    combos: list[dict[str, object]],
    bounds: list[dict[str, object]],
    inputs: list[dict[str, object]],
    gates: list[dict[str, object]],
    status: list[dict[str, object]],
    next_target: list[dict[str, object]],
) -> None:
    strongest = max(bounds, key=lambda row: float(row["C_H_proxy"]))
    weakest = min(bounds, key=lambda row: float(row["C_H_proxy"]))
    lines = [
        "# 3667 - fEM ZX profile normalization proof or first bound row",
        "",
        f"**Status:** {status[0]['summary']}",
        "",
        f"**Claim ceiling:** {status[0]['claim_ceiling']}.",
        "",
        "## Main result",
        "",
        "The zero route still does not close: the current parent grammar does not forbid `f_X(X_N)F_Q^2`, so `f_EM=0` is not claimed.",
        "",
        "The finite route is now sharper. Cassini does not bound `f_EM` or `Z_X` separately. It bounds normalized combinations:",
        "",
        "`mu_H = |K_gamma_H(lambda) k_H f_EM/Z_X|`,",
        "",
        "`mu_G = |K_gamma_G(lambda) k_G| f_EM^2/Z_X^2`,",
        "",
        "through",
        "",
        "`C_H(lambda) mu_H + C_G(lambda) mu_G + |C_other_gamma| <= B_gamma_Cassini`.",
        "",
        "This is progress because the next derivation target is now `k_H/k_G/K_gamma`, not the naked coupling by itself.",
        "",
        "## Closure attempt",
    ]
    for row in closure:
        lines.append(f"- `{row['attempt_id']}`: {row['result']} - `{row['formula']}`")
    lines.extend(["", "## Normalized combinations"])
    for row in combos:
        lines.append(f"- `{row['symbol']}`: {row['current_status']} - `{row['formula']}`")
    lines.extend(["", "## First finite scale-proxy rows"])
    lines.append(f"- Strongest sampled linear coefficient: `{strongest['bound_id']}` with `C_H={strongest['C_H_proxy']}`.")
    lines.append(f"- Weakest sampled linear coefficient: `{weakest['bound_id']}` with `C_H={weakest['C_H_proxy']}`.")
    for row in bounds:
        lines.append(f"- `{row['bound_id']}`: `{row['joint_bound_formula']}` - {row['current_status']}")
    lines.extend(["", "## Inputs still blocking a claim"])
    for row in inputs:
        lines.append(f"- `{row['quantity']}`: {row['current_status']} - needs {row['needed_for_claim']}")
    lines.extend(["", "## Claim gates"])
    for row in gates:
        lines.append(f"- `{row['gate_id']}`: {row['status']} - {row['gate']}")
    lines.extend(["", "## Next checkpoint", ""])
    lines.append(f"`{next_target[0]['target_doc']}` via `{next_target[0]['target_script']}`.")
    lines.extend(["", "## Sources"])
    for row in sources:
        lines.append(f"- `{row['source_id']}`: `{row['path']}` exists={row['exists']} needle_found={row['needle_found']}")
    DOC.write_text("\n".join(lines) + "\n", encoding="utf-8")


def validate(
    ts: str,
    output_paths: list[Path],
    sources: list[dict[str, object]],
    closure: list[dict[str, object]],
    combos: list[dict[str, object]],
    bounds: list[dict[str, object]],
    inputs: list[dict[str, object]],
    gates: list[dict[str, object]],
    status: list[dict[str, object]],
    next_target: list[dict[str, object]],
) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []

    def add(validation_id: str, ok: bool, detail: str) -> None:
        rows.append(
            {
                "timestamp_utc": ts,
                "branch_id": BRANCH_ID,
                "checkpoint_id": CHECKPOINT_ID,
                "validation_id": validation_id,
                "result": "PASS" if ok else "FAIL",
                "detail": detail,
            }
        )

    csv_status = [parse_csv(path) for path in output_paths if path.suffix.lower() == ".csv"]
    generated = sources + closure + combos + bounds + inputs + gates + status + next_target
    doc_text = read_text(DOC)
    leaks: list[Path] = []
    if FORMALIZATION.exists():
        for pattern in ["*Y5_R2FR_3667*", "3667-Y5-R2FR-*", "P8_Y5*3667*"]:
            leaks.extend(FORMALIZATION.rglob(pattern))

    add("VAL3667_0_sources_exist", all(row["exists"] for row in sources), "every cited source exists")
    add("VAL3667_1_needles_found", all(row["needle_found"] for row in sources), "every source needle found")
    add("VAL3667_2_outputs_exist", all(path.exists() for path in output_paths), "all expected 3667 outputs written")
    add("VAL3667_3_csv_parse", all(ok and count > 0 for ok, count in csv_status), "all generated CSVs parse with rows")
    add("VAL3667_4_zero_refused", not any(str(row["accepted_as_zero"]).lower() == "true" for row in closure), "f_EM zero not accepted")
    add("VAL3667_5_normalized_combos", {"mu_H", "mu_G", "delta_gamma_EM_envelope"}.issubset({str(row["symbol"]) for row in combos}), "mu_H/mu_G envelope combinations present")
    add("VAL3667_6_bound_rows", len(bounds) == len(LAMBDA_RATIOS) and all(float(row["C_H_proxy"]) >= 0.0 and float(row["C_G_proxy"]) >= 0.0 for row in bounds), "finite scale-proxy rows produced for lambda/r grid")
    add("VAL3667_7_bound_formulas", all("mu_H" in row["joint_bound_formula"] and "mu_G" in row["joint_bound_formula"] for row in bounds), "joint bound formulas include normalized variables")
    add("VAL3667_8_inputs_preserved", {"k_H projection", "k_G projection", "K_gamma transfer"}.issubset({str(row["quantity"]) for row in inputs}), "projection and transfer blockers preserved")
    add("VAL3667_9_all_nonclaim", not any(str(row.get("valid_for_claim", "")).lower() == "true" or str(row.get("claim_allowed", "")).lower() == "true" for row in generated), "all generated rows remain nonclaim")
    add("VAL3667_10_no_score_ready", not any(str(row.get("score_ready", "")).lower() == "true" for row in combos + bounds), "combo/bound rows are not score-ready")
    add("VAL3667_11_doc_written", "mu_H" in doc_text and "mu_G" in doc_text and "f_EM=0" in doc_text and "not claimed" in doc_text, "doc records normalized combination derivation and zero refusal")
    add("VAL3667_12_no_formalization_leak", not leaks, "no 3667 checkpoint files in formalization-workbench")
    add("VAL3667_13_next_target", next_target[0]["target_doc"].startswith("3668-") and "kH-kG" in next_target[0]["target_doc"], "3668 kH/kG target selected")
    return rows


def main() -> int:
    ts = stamp()
    RESIDUALS.mkdir(parents=True, exist_ok=True)
    b_sun, bound, phi_abs = scalar_from_3666_status()
    r_proxy = r_proxy_from_3666()
    sources = source_register(ts)
    closure = closure_attempt_rows(ts)
    combos = normalized_combination_rows(ts, b_sun, bound)
    bounds = finite_bound_rows(ts, b_sun, bound, phi_abs, r_proxy)
    inputs = input_status_rows(ts)
    gates = claim_gate_rows(ts)
    status = status_rows(ts, b_sun, bound, phi_abs, r_proxy)
    next_target = next_rows(ts)
    outputs = {
        "sources": RESIDUALS / "P8_Y5_R2FR_3667_SOURCE_REGISTER.csv",
        "closure": RESIDUALS / "P8_Y5_R2FR_3667_CLOSURE_ATTEMPT_ROWS.csv",
        "combos": RESIDUALS / "P8_Y5_R2FR_3667_NORMALIZED_GAMMA_COMBINATION_ROWS.csv",
        "bounds": RESIDUALS / "P8_Y5_R2FR_3667_FIRST_FINITE_GAMMA_BOUND_ROWS.csv",
        "inputs": RESIDUALS / "P8_Y5_R2FR_3667_INPUT_STATUS_ROWS.csv",
        "gates": RESIDUALS / "P8_Y5_R2FR_3667_CLAIM_GATES.csv",
        "status": RESIDUALS / "P8_Y5_R2FR_3667_STATUS.csv",
        "next": RESIDUALS / "P8_Y5_R2FR_3667_NEXT_TARGET.csv",
        "validation": RESIDUALS / "P8_Y5_BRR545_3667_VALIDATION.csv",
    }
    write_csv(outputs["sources"], sources)
    write_csv(outputs["closure"], closure)
    write_csv(outputs["combos"], combos)
    write_csv(outputs["bounds"], bounds)
    write_csv(outputs["inputs"], inputs)
    write_csv(outputs["gates"], gates)
    write_csv(outputs["status"], status)
    write_csv(outputs["next"], next_target)
    write_doc(sources, closure, combos, bounds, inputs, gates, status, next_target)
    generated_paths = [path for key, path in outputs.items() if key != "validation"] + [DOC]
    validation = validate(ts, generated_paths, sources, closure, combos, bounds, inputs, gates, status, next_target)
    write_csv(outputs["validation"], validation)
    failures = [row for row in validation if row["result"] != "PASS"]
    if failures:
        print(f"3667 validation failed: {failures}", file=sys.stderr)
        return 1
    print(f"wrote 3667 checkpoint with {len(validation)} validation checks; normalized gamma combinations derived")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

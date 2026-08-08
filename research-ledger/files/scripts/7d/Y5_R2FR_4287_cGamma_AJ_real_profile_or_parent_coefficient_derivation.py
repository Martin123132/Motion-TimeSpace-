from __future__ import annotations

import csv
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, Iterable, List


ROOT = Path(__file__).resolve().parents[2]
FORMAL = ROOT / "formalization-workbench"
POST = ROOT / "post-checkpoint-work"
SOURCE_DIR = POST / "source-intake" / "mts_residuals"

CHECKPOINT = "4287"
CLAIM_ID = "L-128"
BRANCH = "MTS_R2FR_Y5_CGAMMA_AJ_REAL_PROFILE_OR_PARENT_COEFFICIENT_DERIVATION_4287"
DECISION = "PARENT_ZERO_NOT_DERIVED_AJ_REDUCED_TO_EXPLICIT_STRONG_WINDOW_PROFILE_LAW_NONCLAIM"
MARKER = "PPC4161_CGAMMA_AJ_REAL_PROFILE_OR_PARENT_COEFFICIENT_DERIVATION_4287"
PACKET_MARKER = "PPC4161_PACKET_CGAMMA_AJ_REAL_PROFILE_OR_PARENT_COEFFICIENT_DERIVATION_4287"
NEXT_TARGET = "4288-Y5-R2FR-real-AJ-profile-row-or-parent-kernel-coefficient-source.md"

FORMAL_PATH = FORMAL / "303-PPC4161-cGamma-AJ-real-profile-or-parent-coefficient-derivation.md"
DOC_PATH = POST / "4287-Y5-R2FR-cGamma-AJ-real-profile-or-parent-coefficient-derivation.md"
VALIDATION_PATH = SOURCE_DIR / "P8_Y5_BRR545_4287_VALIDATION.csv"

STAMP = datetime.now(timezone.utc).replace(microsecond=0).isoformat()
MU_XI_COEFFICIENT = 0.1678939074330212
PI_B_COEFFICIENT = 0.167893843691

SOURCES = {
    "SRC4287_00_4286_interface": (
        FORMAL / "302-PPC4161-transition-closure-local-sanity-and-cGamma-AJ-interface-runner.md",
        "The AJ branch remains blocked until those rows are derived or sourced.",
        "4286 blocks closure credit and names the open cGamma/AJ rows.",
    ),
    "SRC4287_01_4280_AJ_reduction": (
        FORMAL / "296-PPC4161-cGamma-parent-memory-equation-AJ-source-coefficient-or-profile-fill.md",
        "A_J,eff_private <= |R_transport_to_local| + |R_Bgrad_to_local|.",
        "4280 reduces the AJ amplitude to transport and B-gradient local residuals.",
    ),
    "SRC4287_02_4187_cGamma_zero": (
        FORMAL / "203-PPC4161-local-memory-support-projector-zero-law-for-cGamma.md",
        "c_Gamma_parent_zero = false",
        "4187 keeps the parent cGamma zero theorem unsigned.",
    ),
    "SRC4287_03_4188_product_bounds": (
        FORMAL / "204-PPC4161-finite-cGamma-product-bound-law.md",
        "C_Gamma_Gdot",
        "4188 supplies finite product-bound channels for nonzero cGamma residuals.",
    ),
    "SRC4287_04_4190_stationarity": (
        FORMAL / "206-PPC4161-local-memory-stationarity-gradient-zero-gate.md",
        "The zero lemma is not closed.",
        "4190 gives the stationarity/gradient zero contract and finite bounds.",
    ),
    "SRC4287_05_4191_fixed_point": (
        FORMAL / "207-PPC4161-memory-fixed-point-equation-and-smooth-minimizer-contract.md",
        "parent_signed = false",
        "4191 gives the fixed-point minimizer route but does not parent-sign it.",
    ),
    "SRC4287_06_4192_Xi_signs": (
        FORMAL / "208-PPC4161-parent-Xi-Hessian-signs-and-boundary-domain.md",
        "Z_Xi > 0    <= D_m > 0",
        "4192 maps Xi signs onto diffusion/relaxation signs and keeps source/boundary open.",
    ),
    "SRC4287_07_4198_amplitude": (
        FORMAL / "214-PPC4161-parent-amplitude-owner-for-Jres.md",
        "strong local requires T_res/tau_L >= 5.95614453762",
        "4198 gives the already-derived order-one strong-window ratio.",
    ),
    "SRC4287_08_4248_memory_equation": (
        FORMAL / "252-PPC4161-cGamma-parent-memory-equation-or-AJ-coefficient-source-fill.md",
        "mu_Xi ~= Pi_B/tau_L",
        "4248 gives the memory normal form and Pi_B/tau_L substitution.",
    ),
    "SRC4287_09_4249_AJ_theorem": (
        FORMAL / "253-PPC4161-AJ-source-coefficient-theorem-or-numeric-fill-pack.md",
        "A_J,eff_private <= |S_A H_L^A| + |D_m Delta_h M_2| + |D_t M_2|.",
        "4249 gives the explicit AJ source coefficient decomposition.",
    ),
    "SRC4287_10_4254_M2_pruning": (
        FORMAL / "258-PPC4161-M2-defect-source-map-pruning-or-real-profile-input-pack.md",
        "R_transport_to_local",
        "4254 routes the M2 defect into explicit transport/B-gradient residuals.",
    ),
}


def common() -> Dict[str, str]:
    return {
        "checkpoint": CHECKPOINT,
        "branch": BRANCH,
        "generated_utc": STAMP,
        "decision": DECISION,
    }


def read_text(path: Path) -> str:
    if not path.exists():
        return ""
    return path.read_text(encoding="utf-8", errors="replace")


def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text.strip() + "\n", encoding="utf-8")


def write_csv(path: Path, rows: List[Dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        path.write_text("", encoding="utf-8")
        return
    fieldnames = list(rows[0].keys())
    for row in rows:
        for key in row:
            if key not in fieldnames:
                fieldnames.append(key)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def csv_rows(path: Path) -> List[Dict[str, str]]:
    if not path.exists():
        return []
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def append_unique_block(path: Path, marker: str, heading: str, body: str) -> None:
    text = read_text(path)
    if marker in text:
        return
    block = f"\n\n## {heading}\n\nMarker: `{marker}`\n\n{body}\n"
    write_text(path, text.rstrip() + block)


def append_claim() -> None:
    path = FORMAL / "02-claims-register.csv"
    text = read_text(path)
    if f"{CLAIM_ID}," in text:
        return
    row = (
        f'{CLAIM_ID},local_gr,'
        f'"4287 converts the cGamma/AJ blocker into an explicit algebraic gate. The parent cGamma-zero and AJ-zero routes remain unsigned, but the finite route is now reduced to A_J,eff_private <= 0.167893843691*Pi_B*(T_res/tau_L)/abs(c_Gamma), equivalently T_res/tau_L >= A_J,eff_private*abs(c_Gamma)/(0.167893843691*Pi_B). This is a calculator-ready nonclaim profile law rather than another closure note.",'
        f'"4287 source register, parent-zero audit, AJ reduction map, cGamma product-bound rows, required profile rows, strong-window calculator, decision and firewall.",'
        f'private_cGamma_AJ_reduced_to_strong_window_profile_law_nonclaim,'
        f'"Fill or derive the first real profile/coefficient row for R_transport_to_local, R_Bgrad_to_local, T_res/tau_L, c_Gamma, Pi_B, or A_J,eff_private; otherwise derive a parent kernel/coefficient theorem that sets the residual pair to zero.",'
        f'"Claiming c_Gamma=0 from unsigned support clauses, treating product bounds as c_Gamma values, using transition closure as AJ credit, or counting control-window rows as physical evidence."\n'
    )
    path.write_text(text.rstrip() + "\n" + row, encoding="utf-8")


def source_rows() -> List[Dict[str, str]]:
    rows: List[Dict[str, str]] = []
    for source_id, (path, needle, role) in SOURCES.items():
        text = read_text(path)
        rows.append(
            {
                **common(),
                "source_id": source_id,
                "path": str(path),
                "exists": str(path.exists()),
                "required_text": needle,
                "required_text_found": str(needle in text),
                "role": role,
                "claim_allowed": "False",
                "valid_for_claim": "False",
            }
        )
    return rows


def parent_zero_audit_rows() -> List[Dict[str, str]]:
    raw = [
        (
            "PZA4287_0_cGamma_parent_support",
            "c_Gamma_parent_zero",
            "UNSIGNED",
            "203 requires five parent support/no-hair clauses; the corpus records c_Gamma_parent_zero=false.",
            "finite product/profile route remains active",
        ),
        (
            "PZA4287_1_stationarity_gradient",
            "D_t Xi_0=0 and grad_perp Xi_0=0",
            "UNSIGNED",
            "206/207 give the fixed-point/minimizer route, but parent_signed=false.",
            "can kill Gdot/xi channels if later signed, not AJ transport/B-gradient by itself",
        ),
        (
            "PZA4287_2_Xi_positive_operator",
            "Z_Xi>0 and M_Xi^2>0",
            "PARTIAL",
            "208 maps signs to D_m>0 and Pi_B/tau_L>0, with residual source/projector and boundary still open.",
            "supports finite bound algebra but not exact local-GR closure",
        ),
        (
            "PZA4287_3_AJ_exact_zero",
            "R_transport_to_local=0 and R_Bgrad_to_local=0",
            "UNSIGNED_GLOBAL",
            "296/258 prove the exact route only if both residuals vanish; 4281 supplies finite-margin collars but not the transition/global shell.",
            "exact AJ zero not available outside support-separated collars",
        ),
        (
            "PZA4287_4_transition_closure_firewall",
            "closure_credit_to_AJ",
            "FORBIDDEN",
            "302 states transition closure cannot fill cGamma/AJ rows.",
            "closure sanity cannot be used as parent coefficient derivation",
        ),
    ]
    return [
        {
            **common(),
            "audit_id": audit_id,
            "object": target,
            "signature_status": status,
            "basis": basis,
            "derived_consequence": consequence,
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
        for audit_id, target, status, basis, consequence in raw
    ]


def aj_reduction_rows() -> List[Dict[str, str]]:
    raw = [
        (
            "AJR4287_0_normal_form",
            "A_J,eff_private = A_src + A_lap + A_drift",
            "252/253",
            "DECOMPOSED",
        ),
        (
            "AJR4287_1_source_zero",
            "A_src=0 on standard Dq/Hperp branch",
            "4280 imports 4277/4243/4239 route",
            "CONDITIONALLY_ZERO_PRIVATE",
        ),
        (
            "AJR4287_2_lap_drift_route",
            "A_lap + A_drift -> R_transport_to_local + R_Bgrad_to_local",
            "296/258",
            "REDUCED_TO_PROFILE_ROWS",
        ),
        (
            "AJR4287_3_residual_bound",
            "A_J,eff_private <= |R_transport_to_local| + |R_Bgrad_to_local|",
            "296",
            "DERIVED_BOUND_FORM",
        ),
        (
            "AJR4287_4_strong_window",
            "A_J,eff_private <= 0.167893843691*Pi_B*(T_res/tau_L)/abs(c_Gamma)",
            "252/296/214",
            "CALCULATOR_READY_NONCLAIM",
        ),
        (
            "AJR4287_5_required_ratio",
            "T_res/tau_L >= A_J,eff_private*abs(c_Gamma)/(0.167893843691*Pi_B)",
            "algebraic rearrangement with Pi_B>0",
            "EXPLICIT_NEXT_GATE",
        ),
    ]
    return [
        {
            **common(),
            "reduction_id": reduction_id,
            "statement": statement,
            "source_basis": source_basis,
            "status": status,
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
        for reduction_id, statement, source_basis, status in raw
    ]


def cgamma_product_bound_rows() -> List[Dict[str, str]]:
    raw = [
        ("CPB4287_0_Gdot", "C_Gamma_Gdot", "2.42e-14", "yr^-1", "204/206/207"),
        ("CPB4287_1_R10", "C_Gamma_R10", "1.0", "dimensionless", "204"),
        ("CPB4287_2_WEP", "C_Gamma_WEP", "6.991812087098392e-15", "dimensionless", "204"),
        ("CPB4287_3_clock", "C_Gamma_clock", "5.15e-05", "dimensionless", "204"),
        ("CPB4287_4_metric", "C_Gamma_metric", "4.0e-09", "dimensionless", "204/206/207"),
        ("CPB4287_5_stress", "C_Gamma_stress", "1.0e-08", "dimensionless", "204"),
        ("CPB4287_6_vector", "C_Gamma_vector", "4.0e-20", "dimensionless", "204"),
    ]
    return [
        {
            **common(),
            "bound_id": bound_id,
            "product_channel": channel,
            "bound_value": bound_value,
            "units": units,
            "source_basis": source_basis,
            "is_bound_on_cGamma_alone": "False",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
        for bound_id, channel, bound_value, units, source_basis in raw
    ]


def required_profile_rows() -> List[Dict[str, str]]:
    raw = [
        ("RPR4287_0", "R_transport_to_local", "dimensionless_or_normalized_AJ", "MISSING_SOURCE_PATH", "MISSING_REAL_PROFILE"),
        ("RPR4287_1", "R_Bgrad_to_local", "dimensionless_or_normalized_AJ", "MISSING_SOURCE_PATH", "MISSING_REAL_PROFILE"),
        ("RPR4287_2", "T_res/tau_L", "dimensionless", "MISSING_SOURCE_PATH", "MISSING_PARENT_NORMALIZATION"),
        ("RPR4287_3", "c_Gamma", "dimensionless_effective_coupling", "MISSING_SOURCE_PATH", "MISSING_PARENT_COEFFICIENT"),
        ("RPR4287_4", "Pi_B_local", "dimensionless", "MISSING_SOURCE_PATH", "MISSING_LOCAL_SCREENING_PROFILE"),
        ("RPR4287_5", "A_J,eff_private", "dimensionless_or_normalized_AJ", "MISSING_SOURCE_PATH", "MISSING_PARENT_OR_PROFILE_AMPLITUDE"),
    ]
    return [
        {
            **common(),
            "row_id": row_id,
            "quantity": quantity,
            "units": units,
            "source_path": source_path,
            "status": status,
            "numeric_value": "MISSING",
            "score_ready": "False",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
        for row_id, quantity, units, source_path, status in raw
    ]


def required_ratio(a_j_eff: float, c_gamma_abs: float, pi_b: float) -> float:
    if a_j_eff == 0.0:
        return 0.0
    if pi_b <= 0.0:
        return float("inf")
    return a_j_eff * c_gamma_abs / (PI_B_COEFFICIENT * pi_b)


def capacity(pi_b: float, tres_over_tau: float, c_gamma_abs: float) -> float:
    if c_gamma_abs <= 0.0:
        return float("inf")
    return PI_B_COEFFICIENT * pi_b * tres_over_tau / c_gamma_abs


def strong_window_rows() -> List[Dict[str, str]]:
    controls = [
        ("SWC4287_0_order_one_fail", 1.0, 1.0, 1.0, 1.0, "EXPECTED_FAIL"),
        ("SWC4287_1_small_AJ_pass", 0.1, 1.0, 1.0, 1.0, "EXPECTED_PASS"),
        ("SWC4287_2_small_cGamma_pass", 1.0, 0.1, 1.0, 1.0, "EXPECTED_PASS"),
        ("SWC4287_3_large_relaxation_pass", 1.0, 1.0, 1.0, 6.0, "EXPECTED_PASS"),
        ("SWC4287_4_low_PiB_fail", 1.0, 1.0, 0.01, 1.0, "EXPECTED_FAIL"),
        ("SWC4287_5_exact_AJ_zero_pass", 0.0, 1.0, 1.0, 0.0, "EXPECTED_PASS"),
    ]
    rows: List[Dict[str, str]] = []
    for control_id, a_j_eff, c_gamma_abs, pi_b, tres_over_tau, expected in controls:
        required = required_ratio(a_j_eff, c_gamma_abs, pi_b)
        allowed = capacity(pi_b, tres_over_tau, c_gamma_abs)
        passes = a_j_eff <= allowed
        rows.append(
            {
                **common(),
                "control_id": control_id,
                "A_J_eff_private": f"{a_j_eff:.12e}",
                "abs_c_Gamma": f"{c_gamma_abs:.12e}",
                "Pi_B": f"{pi_b:.12e}",
                "T_res_over_tau_L": f"{tres_over_tau:.12e}",
                "capacity_AJ_max": f"{allowed:.12e}",
                "required_T_res_over_tau_L": f"{required:.12e}" if required != float("inf") else "inf",
                "passes_window": str(passes),
                "expected": expected,
                "claim_scope": "algebra_control_only",
                "claim_allowed": "False",
                "valid_for_claim": "False",
            }
        )
    return rows


def decision_rows() -> List[Dict[str, str]]:
    return [
        {
            **common(),
            "decision_id": "DEC4287_0",
            "selected_route": "FINITE_AJ_PROFILE_LAW_READY_PARENT_ZERO_STILL_UNSIGNED",
            "meaning": "The exact parent-zero route is not closed. The useful leap is the explicit strong-window law: either make A_J small, make c_Gamma small, raise T_res/tau_L, or derive R_transport=R_Bgrad=0 from the parent.",
            "next_target": NEXT_TARGET,
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
    ]


def firewall_rows() -> List[Dict[str, str]]:
    raw = [
        ("FW4287_0", "Do not claim c_Gamma=0 from the unsigned 203 support/no-hair clauses."),
        ("FW4287_1", "Do not treat cGamma product bounds as direct values of c_Gamma."),
        ("FW4287_2", "Do not transfer transition closure/no-leak credit into AJ profile rows."),
        ("FW4287_3", "Do not treat strong-window control rows as sourced physical measurements."),
        ("FW4287_4", "Do not claim local-GR pass until the required profile rows are numeric, sourced, and within window."),
    ]
    return [
        {
            **common(),
            "firewall_id": firewall_id,
            "forbidden_move": forbidden_move,
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
        for firewall_id, forbidden_move in raw
    ]


def status_rows() -> List[Dict[str, str]]:
    return [
        {
            **common(),
            "status_id": "STATUS4287_0",
            "status": "PARENT_ZERO_UNSIGNED_FINITE_AJ_WINDOW_DERIVED",
            "summary": "4287 does not close derived local GR, but it turns the cGamma/AJ gap into a concrete inequality and required-ratio law for the first real profile row.",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
    ]


def next_target_rows() -> List[Dict[str, str]]:
    return [
        {
            **common(),
            "next_target_id": "NEXT4287_0",
            "target_file": NEXT_TARGET,
            "task": "Try to fill the first real AJ/cGamma profile row or derive a parent kernel coefficient theorem for R_transport_to_local=R_Bgrad_to_local=0.",
            "priority": "highest_local_GR_pressure_point",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
    ]


def formal_doc() -> str:
    order_one_requirement = required_ratio(1.0, 1.0, 1.0)
    return f"""
# 303 cGamma AJ Real Profile Or Parent Coefficient Derivation

Marker: `{MARKER}`

Branch: `{BRANCH}`

Decision: `{DECISION}`

## Result

4287 tries the parent-zero route first.

It does **not** close:

```text
c_Gamma_parent_zero = true,
R_transport_to_local = 0,
R_Bgrad_to_local = 0.
```

The reason is precise rather than vibes: the support/no-hair cGamma clauses remain unsigned, the fixed-point memory theorem is not parent-signed, and transition closure is firewalled from AJ credit.

## Useful Reduction

The live AJ pressure is now reduced to:

```text
A_J,eff_private <= |R_transport_to_local| + |R_Bgrad_to_local|.
```

The finite strong-window form is:

```text
A_J,eff_private <= {PI_B_COEFFICIENT} * Pi_B * (T_res/tau_L) / abs(c_Gamma).
```

Equivalently, for `Pi_B>0`:

```text
T_res/tau_L >= A_J,eff_private * abs(c_Gamma) / ({PI_B_COEFFICIENT} * Pi_B).
```

For the order-one control branch:

```text
A_J,eff_private = 1,
abs(c_Gamma) = 1,
Pi_B = 1
```

the required ratio is:

```text
T_res/tau_L >= {order_one_requirement:.12f}.
```

So the route is no longer just "something is missing". The next row has to do one of four things:

1. derive `R_transport_to_local=R_Bgrad_to_local=0`;
2. source a small enough `A_J,eff_private`;
3. source a small enough `abs(c_Gamma)`;
4. source a large enough `T_res/tau_L` at local `Pi_B`.

## Nonclaim

This is not a local-GR claim. It is the exact local pressure law the next sourced profile or parent theorem must satisfy.
"""


def checkpoint_doc() -> str:
    return f"""
# 4287 - cGamma AJ real profile or parent coefficient derivation

Marker: `{MARKER}`

Decision: `{DECISION}`

4287 tries the parent-zero route and keeps it unsigned. The advance is the finite calculator-ready gate:

```text
A_J,eff_private <= {PI_B_COEFFICIENT} * Pi_B * (T_res/tau_L) / abs(c_Gamma)
```

or:

```text
T_res/tau_L >= A_J,eff_private * abs(c_Gamma) / ({PI_B_COEFFICIENT} * Pi_B).
```

The next target is a real sourced row for `R_transport_to_local`, `R_Bgrad_to_local`, `T_res/tau_L`, `c_Gamma`, `Pi_B`, or `A_J,eff_private`, or a parent theorem that sets the residual pair exactly to zero.
"""


def generated_nonclaim_rows(paths: Dict[str, Path]) -> Iterable[Dict[str, str]]:
    for path in paths.values():
        for row in csv_rows(path):
            yield row


def validation_rows(paths: Dict[str, Path]) -> List[Dict[str, str]]:
    sources = csv_rows(paths["sources"])
    parent_audit = csv_rows(paths["parent_zero_audit"])
    reduction = csv_rows(paths["aj_reduction"])
    bounds = csv_rows(paths["cgamma_product_bounds"])
    required = csv_rows(paths["required_profiles"])
    windows = csv_rows(paths["strong_window"])
    all_generated = list(generated_nonclaim_rows(paths))
    validations = [
        ("VAL4287_0_sources_exist", all(row["exists"] == "True" for row in sources), "all cited source paths exist"),
        ("VAL4287_1_needles_found", all(row["required_text_found"] == "True" for row in sources), "all cited source needles found"),
        (
            "VAL4287_2_parent_zero_unsigned",
            any(row["object"] == "c_Gamma_parent_zero" and row["signature_status"] == "UNSIGNED" for row in parent_audit)
            and any(row["object"] == "R_transport_to_local=0 and R_Bgrad_to_local=0" and row["signature_status"] == "UNSIGNED_GLOBAL" for row in parent_audit),
            "parent zero and exact AJ zero are not claimed",
        ),
        (
            "VAL4287_3_AJ_law_present",
            any("0.167893843691*Pi_B" in row["statement"] for row in reduction)
            and any("T_res/tau_L >=" in row["statement"] for row in reduction),
            "AJ finite strong-window law emitted",
        ),
        (
            "VAL4287_4_product_bounds_are_positive",
            all(float(row["bound_value"]) > 0.0 and row["is_bound_on_cGamma_alone"] == "False" for row in bounds),
            "product bounds parse and are not direct cGamma rows",
        ),
        (
            "VAL4287_5_required_profiles_blocked",
            {"R_transport_to_local", "R_Bgrad_to_local", "T_res/tau_L", "c_Gamma", "Pi_B_local", "A_J,eff_private"}.issubset({row["quantity"] for row in required})
            and all(row["score_ready"] == "False" and row["source_path"] == "MISSING_SOURCE_PATH" for row in required),
            "required profile rows remain explicit missing nonclaim rows",
        ),
        (
            "VAL4287_6_window_controls",
            all(
                (row["expected"] == "EXPECTED_PASS") == (row["passes_window"] == "True")
                for row in windows
            ),
            "strong-window controls behave as expected",
        ),
        (
            "VAL4287_7_order_one_ratio",
            any(
                row["control_id"] == "SWC4287_0_order_one_fail"
                and abs(float(row["required_T_res_over_tau_L"]) - (1.0 / PI_B_COEFFICIENT)) < 1e-10
                for row in windows
            ),
            "order-one required ratio matches reciprocal coefficient",
        ),
        ("VAL4287_8_formal_doc", FORMAL_PATH.exists() and MARKER in read_text(FORMAL_PATH), "formal document written"),
        ("VAL4287_9_checkpoint_doc", DOC_PATH.exists() and DECISION in read_text(DOC_PATH), "post-checkpoint document written"),
        ("VAL4287_10_claim_row", f"{CLAIM_ID}," in read_text(FORMAL / "02-claims-register.csv"), "claim register row added"),
        (
            "VAL4287_11_no_claim_rows",
            all(row.get("claim_allowed", "False") == "False" and row.get("valid_for_claim", "False") == "False" for row in all_generated),
            "all generated rows remain private nonclaim rows",
        ),
    ]
    for name, path in paths.items():
        validations.append((f"VAL4287_csv_{name}", bool(csv_rows(path)), f"{path.name} parses with rows"))
    return [
        {
            **common(),
            "check_id": check_id,
            "description": description,
            "passed": str(passed),
            "evidence": "generated_artifacts",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
        for check_id, passed, description in validations
    ]


def main() -> None:
    SOURCE_DIR.mkdir(parents=True, exist_ok=True)
    paths = {
        "sources": SOURCE_DIR / "P8_Y5_R2FR_4287_SOURCE_REGISTER.csv",
        "parent_zero_audit": SOURCE_DIR / "P8_Y5_R2FR_4287_PARENT_ZERO_AUDIT.csv",
        "aj_reduction": SOURCE_DIR / "P8_Y5_R2FR_4287_AJ_REDUCTION_MAP.csv",
        "cgamma_product_bounds": SOURCE_DIR / "P8_Y5_R2FR_4287_CGAMMA_PRODUCT_BOUNDS.csv",
        "required_profiles": SOURCE_DIR / "P8_Y5_R2FR_4287_REQUIRED_PROFILE_ROWS.csv",
        "strong_window": SOURCE_DIR / "P8_Y5_R2FR_4287_STRONG_WINDOW_CALCULATOR.csv",
        "decision": SOURCE_DIR / "P8_Y5_R2FR_4287_DECISION.csv",
        "firewall": SOURCE_DIR / "P8_Y5_R2FR_4287_CLAIM_FIREWALL.csv",
        "status": SOURCE_DIR / "P8_Y5_R2FR_4287_STATUS.csv",
        "next_target": SOURCE_DIR / "P8_Y5_R2FR_4287_NEXT_TARGET.csv",
    }
    write_csv(paths["sources"], source_rows())
    write_csv(paths["parent_zero_audit"], parent_zero_audit_rows())
    write_csv(paths["aj_reduction"], aj_reduction_rows())
    write_csv(paths["cgamma_product_bounds"], cgamma_product_bound_rows())
    write_csv(paths["required_profiles"], required_profile_rows())
    write_csv(paths["strong_window"], strong_window_rows())
    write_csv(paths["decision"], decision_rows())
    write_csv(paths["firewall"], firewall_rows())
    write_csv(paths["status"], status_rows())
    write_csv(paths["next_target"], next_target_rows())
    write_text(FORMAL_PATH, formal_doc())
    write_text(DOC_PATH, checkpoint_doc())
    append_claim()
    append_unique_block(
        FORMAL / "07-unification-spine.md",
        MARKER,
        "PPC4161 4287 cGamma AJ strong-window gate",
        "4287 does not derive cGamma/AJ zero. It reduces the open local pressure to a concrete nonclaim law: `A_J,eff_private <= 0.167893843691*Pi_B*(T_res/tau_L)/abs(c_Gamma)`, or `T_res/tau_L >= A_J,eff_private*abs(c_Gamma)/(0.167893843691*Pi_B)`. The next live step is no longer generic missingness; it is a real profile/coefficient row or a parent theorem killing both transport and B-gradient residuals.",
    )
    append_unique_block(
        FORMAL / "180-PPC4161-private-local-packet-integration.md",
        PACKET_MARKER,
        "4287 packet cGamma AJ strong-window gate",
        "Packet update: cGamma/AJ remains nonclaim, but it is now calculator-ready. The local branch needs either exact residual-pair zero or sourced values for `A_J,eff_private`, `c_Gamma`, `Pi_B`, and `T_res/tau_L` that pass the strong-window inequality.",
    )
    write_csv(VALIDATION_PATH, validation_rows(paths))
    failed = [row for row in csv_rows(VALIDATION_PATH) if row["passed"] != "True"]
    print(f"{CHECKPOINT}: wrote {len(paths)} csv artifacts plus validation")
    print(f"{CHECKPOINT}: validation rows={len(csv_rows(VALIDATION_PATH))} failed={len(failed)}")
    print(f"{CHECKPOINT}: order-one T_res/tau_L requirement={required_ratio(1.0, 1.0, 1.0):.12f}")
    print(f"{CHECKPOINT}: decision={DECISION}")
    if failed:
        for row in failed:
            print(f"FAILED {row['check_id']}: {row['description']}")
        raise SystemExit(1)


if __name__ == "__main__":
    main()

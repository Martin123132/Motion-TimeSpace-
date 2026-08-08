from __future__ import annotations

import csv
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List


ROOT = Path(__file__).resolve().parents[2]
FORMAL = ROOT / "formalization-workbench"
POST = ROOT / "post-checkpoint-work"
SOURCE_DIR = POST / "source-intake" / "mts_residuals"

CHECKPOINT = "4236"
CLAIM_ID = "L-077"
BRANCH = "MTS_R2FR_Y5_CGAMMA_PARENT_MEMORY_EQUATION_4236"
DECISION = "CGAMMA_PARENT_MEMORY_NORMAL_FORM_AND_AJ_THREE_COEFFICIENT_LEDGER_DERIVED_BOUNDARY_KPERP_CLOSED_SOURCE_COEFFICIENTS_OPEN"
MARKER = "PPC4161_CGAMMA_PARENT_MEMORY_AJ_LEDGER_4236"
PACKET_MARKER = "PPC4161_PACKET_CGAMMA_PARENT_MEMORY_AJ_LEDGER_4236"
NEXT_TARGET = "4237-Y5-R2FR-AJ-source-coefficient-theorem-or-numeric-fill-pack.md"

FORMAL_PATH = FORMAL / "252-PPC4161-cGamma-parent-memory-equation-or-AJ-coefficient-source-fill.md"
DOC_PATH = POST / "4236-Y5-R2FR-cGamma-parent-memory-equation-or-AJ-coefficient-source-fill.md"
VALIDATION_PATH = SOURCE_DIR / "P8_Y5_BRR545_4236_VALIDATION.csv"


@dataclass(frozen=True)
class SourceSpec:
    source_id: str
    path: Path
    required_text: str
    role: str


STAMP = datetime.now(timezone.utc).replace(microsecond=0).isoformat()


SOURCE_SPECS: Dict[str, SourceSpec] = {
    "SRC4236_00_4235_next": SourceSpec(
        "SRC4236_00_4235_next",
        SOURCE_DIR / "P8_Y5_R2FR_4235_NEXT_TARGET.csv",
        "4236-Y5-R2FR-cGamma-parent-memory-equation-or-AJ-coefficient-source-fill.md",
        "4235 selected the parent Gamma_mem equation / AJ source fill target.",
    ),
    "SRC4236_01_4235_decision": SourceSpec(
        "SRC4236_01_4235_decision",
        SOURCE_DIR / "P8_Y5_R2FR_4235_DECISION.csv",
        "Gamma_mem support/source/profile and cGamma normalization are not parent-owned",
        "4235 decision preserves cGamma as the live survivor.",
    ),
    "SRC4236_02_fixed_point": SourceSpec(
        "SRC4236_02_fixed_point",
        FORMAL / "207-PPC4161-memory-fixed-point-equation-and-smooth-minimizer-contract.md",
        "E_Xi := -nabla_a(Z_Xi h^ab nabla_b Xi_0)",
        "Parent memory fixed-point normal form.",
    ),
    "SRC4236_03_hessian": SourceSpec(
        "SRC4236_03_hessian",
        FORMAL / "208-PPC4161-parent-Xi-Hessian-signs-and-boundary-domain.md",
        "J_res = [1 - Pi_B] S_cg + D_m Delta_h m_L - D_t m_L + boundary_in.",
        "Open-system memory equation and residual source.",
    ),
    "SRC4236_04_projector": SourceSpec(
        "SRC4236_04_projector",
        FORMAL / "209-PPC4161-residual-source-projector-and-Xi-profile-amplitude-bound.md",
        "P_loc J_res = 0",
        "Projector-zero target and Green-function profile budget.",
    ),
    "SRC4236_05_support": SourceSpec(
        "SRC4236_05_support",
        FORMAL / "210-PPC4161-source-support-powers-for-Jres.md",
        "J_res = O(U_B^2).",
        "Support-power result for J_res.",
    ),
    "SRC4236_06_parity": SourceSpec(
        "SRC4236_06_parity",
        FORMAL / "211-PPC4161-parent-ZL-parity-signature.md",
        "J_res,bulk = O(U_B^2).",
        "Parity/evenness support condition.",
    ),
    "SRC4236_07_reference": SourceSpec(
        "SRC4236_07_reference",
        FORMAL / "212-PPC4161-scalar-leakage-reference-nulling.md",
        "scalar_double_zero_parent_derived = false.",
        "Scalar leakage reference-null caveat.",
    ),
    "SRC4236_08_smoke": SourceSpec(
        "SRC4236_08_smoke",
        FORMAL / "213-PPC4161-normalized-Jres-profile-smoke.md",
        "strong local Gdot needs",
        "4197 normalized Jres profile pressure.",
    ),
    "SRC4236_09_amplitude": SourceSpec(
        "SRC4236_09_amplitude",
        FORMAL / "214-PPC4161-parent-amplitude-owner-for-Jres.md",
        "A_J,eff = A_src + A_lap + A_drift + A_boundary/U_B^2.",
        "AJ amplitude-owner decomposition.",
    ),
    "SRC4236_10_source_operator": SourceSpec(
        "SRC4236_10_source_operator",
        FORMAL / "215-PPC4161-source-operator-amplitude-AJ-bound.md",
        "A_J,eff <= C_D C_S",
        "Source-operator AJ coefficient contract.",
    ),
    "SRC4236_11_kperp": SourceSpec(
        "SRC4236_11_kperp",
        FORMAL / "250-PPC4161-Kperp-EH-coframe-identity-proof-or-independent-tensor-source-row.md",
        "R_i^K = |W_i^K| N_T/D_T = 0",
        "4234 private Kperp closure.",
    ),
    "SRC4236_12_full_budget": SourceSpec(
        "SRC4236_12_full_budget",
        FORMAL / "251-PPC4161-cGamma-support-nohair-or-full-budget-profile-bound-runner.md",
        "|c_Gamma D_t Xi_0| <= 2.42e-14 yr^-1",
        "4235 full-budget cGamma runner.",
    ),
    "SRC4236_13_support_csv": SourceSpec(
        "SRC4236_13_support_csv",
        SOURCE_DIR / "P8_Y5_R2FR_4235_CGAMMA_SUPPORT_NOHAIR_UPDATE.csv",
        "CGZ4235_2_source_silence",
        "Machine-readable cGamma support/open clauses.",
    ),
    "SRC4236_14_profile_csv": SourceSpec(
        "SRC4236_14_profile_csv",
        SOURCE_DIR / "P8_Y5_R2FR_4235_CGAMMA_FULL_BUDGET_PROFILE_TABLE.csv",
        "Gdot_over_G",
        "Machine-readable full-budget profile rows.",
    ),
}


def common() -> Dict[str, str]:
    return {"timestamp_utc": STAMP, "branch_id": BRANCH, "checkpoint_id": CHECKPOINT}


def read_text(path: Path) -> str:
    if not path.exists():
        return ""
    return path.read_text(encoding="utf-8", errors="replace")


def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text.strip() + "\n", encoding="utf-8")


def write_csv(path: Path, rows: List[Dict[str, str]]) -> None:
    if not rows:
        raise ValueError(f"empty csv: {path}")
    path.parent.mkdir(parents=True, exist_ok=True)
    fieldnames: List[str] = []
    for row in rows:
        for key in row:
            if key not in fieldnames:
                fieldnames.append(key)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def csv_rows(path: Path) -> List[Dict[str, str]]:
    with path.open("r", newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def append_once(path: Path, marker: str, block: str) -> None:
    existing = read_text(path)
    if marker in existing:
        return
    with path.open("a", encoding="utf-8") as handle:
        if existing and not existing.endswith("\n"):
            handle.write("\n")
        handle.write("\n" + block.strip() + "\n")


def source_rows() -> List[Dict[str, str]]:
    rows: List[Dict[str, str]] = []
    for spec in SOURCE_SPECS.values():
        text = read_text(spec.path)
        rows.append(
            {
                **common(),
                "source_id": spec.source_id,
                "path": str(spec.path),
                "exists": str(spec.path.exists()),
                "required_text": spec.required_text,
                "required_text_found": str(spec.required_text in text),
                "role": spec.role,
                "claim_allowed": "False",
                "valid_for_claim": "False",
            }
        )
    return rows


def memory_equation_rows() -> List[Dict[str, str]]:
    rows = [
        ("ME4236_0_field", "Xi_0 := N_0[P_loc Gamma_mem]", "local scalar memory profile projected from Gamma_mem", "definition", "open"),
        ("ME4236_1_operator", "L_Xi = -D_Xi Delta_h + mu_Xi", "positive/self-adjoint local memory operator with mu_Xi ~= Pi_B/tau_L", "derived normal form", "conditional_private"),
        ("ME4236_2_equation", "L_Xi delta Xi = J_res", "parent memory equation around Xi_star", "derived normal form", "conditional_private"),
        ("ME4236_3_source", "J_res = U_B S_cg + D_m Delta_h m_L - D_t m_L + boundary_in", "residual source decomposition", "derived source split", "open"),
        ("ME4236_4_profile", "D_t Xi_res <= |J_res|/(mu_Xi T_res); L_loc grad Xi_res <= (L_loc/L_res)|J_res|/mu_Xi", "profile bounds from Green inverse", "derived bound", "active"),
        ("ME4236_5_full_budget", "|c_Gamma D_t Xi_0| <= 2.42e-14 yr^-1; |c_Gamma L_loc grad_perp Xi_0| <= 4e-9", "full-budget local cGamma rows after Kperp removal", "active bound", "not_scoreable"),
    ]
    return [
        {
            **common(),
            "row_id": row_id,
            "formula": formula,
            "meaning": meaning,
            "result_type": result_type,
            "status": status,
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
        for row_id, formula, meaning, result_type, status in rows
    ]


def aj_coefficient_rows() -> List[Dict[str, str]]:
    rows = [
        ("AJ4236_0_A_src", "A_src", "U_B S_cg = U_B^2 A_src", "source/support leakage amplitude", "unfilled", "derive from parent source-current covariance or fill numeric/source row"),
        ("AJ4236_1_A_lap", "A_lap", "D_m Delta_h m_L = U_B^2 A_lap", "diffusive/leakage Laplacian amplitude", "unfilled", "derive from D_m, Hessian and leakage-gradient scale"),
        ("AJ4236_2_A_drift", "A_drift", "-D_t m_L = U_B^2 A_drift", "residual drift amplitude", "unfilled", "derive from scalar Hessian and residual drift timescale"),
        ("AJ4236_3_A_boundary", "A_boundary", "boundary_in = U_B^2 A_boundary", "boundary/open memory amplitude", "private_zero_open_global", "A_boundary_private=0 in compact no-flux collar; fill flux row for open/global systems"),
        ("AJ4236_4_A_J_eff_private", "A_J_eff_private", "A_J_eff_private = A_src + A_lap + A_drift", "private compact source coefficient after boundary/Kperp closure", "derived_formula_unfilled_values", "fill A_src/A_lap/A_drift or prove each support-silent"),
        ("AJ4236_5_Kperp", "Kperp contribution", "R_i^K=0", "tensor source no longer part of private AJ budget", "private_closed", "public fallback row retained until global no-independent-TT-source is signed"),
    ]
    return [
        {
            **common(),
            "coefficient_id": coefficient_id,
            "coefficient": coefficient,
            "normal_form": normal_form,
            "meaning": meaning,
            "status": status,
            "next_action": next_action,
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
        for coefficient_id, coefficient, normal_form, meaning, status, next_action in rows
    ]


def amplitude_requirement_rows() -> List[Dict[str, str]]:
    rows = [
        (
            "AR4236_0_strong_Gdot",
            "strong local",
            "Gdot/G",
            "U_B=3.796559535779445e-07",
            "U_B^2=1.441386430871784e-13",
            "A_J_eff_private <= 0.1678939074330212 * (mu_Xi T_res)/|c_Gamma|",
            "if mu_Xi ~= Pi_B/tau_L, A_J_eff_private <= 0.167893843691 * Pi_B*(T_res/tau_L)/|c_Gamma|",
            "main hard but plausible window",
        ),
        (
            "AR4236_1_strong_gradient",
            "strong local",
            "xi/gradient",
            "U_B=3.796559535779445e-07",
            "U_B^2=1.441386430871784e-13",
            "A_J_eff_private <= 27751.05907983821 * (mu_Xi L_res/L_loc)/|c_Gamma|",
            "usually looser than Gdot unless L_res/L_loc is tiny",
            "secondary check",
        ),
        (
            "AR4236_2_weak_Gdot",
            "weak local",
            "Gdot/G",
            "U_B=1e-4",
            "U_B^2=1e-8",
            "A_J_eff_private <= 2.42e-06 * (mu_Xi T_res)/|c_Gamma|",
            "if mu_Xi ~= Pi_B/tau_L, A_J_eff_private <= 2.419758e-06 * Pi_B*(T_res/tau_L)/|c_Gamma|",
            "hard unless amplitude is tiny or relaxation ratio is huge",
        ),
        (
            "AR4236_3_alpha3_profile",
            "all local",
            "alpha3",
            "full budget",
            "B_alpha3=4e-20",
            "|c_Gamma profile_alpha3| <= 4e-20",
            "requires an arena profile, not just scalar D_t/gradient proxy",
            "strictest profile row",
        ),
        (
            "AR4236_4_R10_profile",
            "R10",
            "alpha(lambda)",
            "anchor only",
            "B_R10(anchor)=1 at 38.6um",
            "|c_Gamma profile_R10(lambda)| <= alpha_bound(lambda)",
            "not claim-grade until full alpha(lambda) curve or mapped envelope exists",
            "schema only",
        ),
    ]
    return [
        {
            **common(),
            "requirement_id": requirement_id,
            "regime": regime,
            "channel": channel,
            "input_scale": input_scale,
            "support_power": support_power,
            "amplitude_bound": amplitude_bound,
            "converted_bound": converted_bound,
            "interpretation": interpretation,
            "scoreable_now": "False",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
        for requirement_id, regime, channel, input_scale, support_power, amplitude_bound, converted_bound, interpretation in rows
    ]


def source_fill_schema_rows() -> List[Dict[str, str]]:
    rows = [
        ("FILL4236_0_A_src", "A_src", "dimensionless", "parent current/source covariance or numeric source row", "MISSING_PARENT_SOURCE_COVARIANCE_OR_NUMERIC_ROW", "False"),
        ("FILL4236_1_A_lap", "A_lap", "dimensionless", "D_m, Hessian, leakage-gradient scale and source path", "MISSING_LAPLACIAN_COEFFICIENT_ROW", "False"),
        ("FILL4236_2_A_drift", "A_drift", "dimensionless", "residual drift timescale and scalar Hessian/source path", "MISSING_DRIFT_COEFFICIENT_ROW", "False"),
        ("FILL4236_3_T_res_tau_L", "T_res/tau_L", "dimensionless", "parent relaxation/source timescale derivation or measured prior", "MISSING_RELAXATION_RATIO_ROW", "False"),
        ("FILL4236_4_cGamma", "c_Gamma", "declared by parent normalization", "parent memory coupling normalization", "MISSING_CGAMMA_NORMALIZATION_ROW", "False"),
        ("FILL4236_5_profile_a", "profile_a/J_a", "per arena", "projection Jacobian/profile rows for Gdot/xi/alpha3/WEP/clock/R10", "MISSING_ARENA_PROFILE_ROWS", "False"),
        ("FILL4236_6_A_boundary_global", "A_boundary_global", "dimensionless/flux", "only for open/global boundary flux, not compact private collar", "RETAINED_FOR_GLOBAL_FLUX_ONLY", "False"),
    ]
    return [
        {
            **common(),
            "fill_id": fill_id,
            "quantity": quantity,
            "units": units,
            "required_source": required_source,
            "status": status,
            "valid_for_claim": valid,
            "claim_allowed": "False",
        }
        for fill_id, quantity, units, required_source, status, valid in rows
    ]


def decision_rows() -> List[Dict[str, str]]:
    return [
        {
            **common(),
            "decision": DECISION,
            "parent_memory_normal_form_written": "True",
            "AJ_reduced_to_three_private_coefficients": "True",
            "A_boundary_private_zero": "True",
            "Kperp_private_closed_imported": "True",
            "A_src_A_lap_A_drift_filled": "False",
            "cGamma_zero_closed": "False",
            "scoreable_now": "False",
            "why_not_scoreable": "A_src/A_lap/A_drift, T_res/tau_L, c_Gamma normalization and arena profiles remain unfilled",
            "next_highest_pressure": "derive/fill A_src, A_lap and A_drift source coefficients",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
    ]


def firewall_rows() -> List[Dict[str, str]]:
    rows = [
        ("FW4236_0", "No cGamma pass follows from normal form alone.", "A_src/A_lap/A_drift and cGamma/profile rows remain unfilled."),
        ("FW4236_1", "Do not reintroduce Kperp into the private AJ budget.", "4234 closes Kperp privately; public tensor fallback is separate."),
        ("FW4236_2", "Do not treat A_boundary_private=0 as global boundary silence.", "Open/global flux rows remain retained."),
        ("FW4236_3", "Do not claim weak-local viability from the strong-local window.", "Weak local Gdot remains extremely hard unless amplitude is tiny or relaxation huge."),
        ("FW4236_4", "Do not claim R10 from the anchor row.", "Full alpha(lambda) or mapped envelope is still required."),
    ]
    return [
        {
            **common(),
            "rule_id": rule_id,
            "rule": rule,
            "reason": reason,
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
        for rule_id, rule, reason in rows
    ]


def status_rows() -> List[Dict[str, str]]:
    return [
        {
            **common(),
            "status": DECISION,
            "summary": "4236 writes the cGamma parent memory normal form and reduces the private AJ problem to A_src + A_lap + A_drift. Boundary and Kperp are privately closed, but the three source coefficients and cGamma/profile rows are still unfilled.",
            "public_local_GR_claim": "False",
            "next_target": NEXT_TARGET,
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
    ]


def next_target_rows() -> List[Dict[str, str]]:
    return [
        {
            **common(),
            "next_target": NEXT_TARGET,
            "reason": "The parent memory equation is now in normal form; the remaining private cGamma obstruction is the source coefficient triplet.",
            "derive_first": "prove A_src=A_lap=A_drift=0 or bounded from parent source-current covariance, leakage Hessian and drift equations",
            "fill_second": "if proof fails, fill numeric/source rows for A_src, A_lap, A_drift, T_res/tau_L, c_Gamma and arena profiles",
            "fallback": "keep global boundary/Kperp/R10 caveats retained",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
    ]


def formal_doc() -> str:
    return f"""
# 252 - PPC4161 cGamma Parent Memory Equation Or AJ Coefficient Source Fill

Marker: `{MARKER}`

Branch: `{BRANCH}`
Decision: `{DECISION}`

## Result

4236 writes the cGamma memory equation in scoreable normal form:

```text
L_Xi delta Xi = J_res,
L_Xi = -D_Xi Delta_h + mu_Xi,
mu_Xi ~= Pi_B/tau_L,
J_res = U_B S_cg + D_m Delta_h m_L - D_t m_L + boundary_in.
```

Using the support-power branch:

```text
J_res = U_B^2 A_J,eff.
```

After 4234/4235, the private compact branch has:

```text
A_boundary_private = 0,
Kperp_private_static_force = 0.
```

So the live private coefficient ledger reduces to:

```text
A_J,eff_private = A_src + A_lap + A_drift.
```

## Full-Budget Amplitude Law

For the strong local window:

```text
A_J,eff_private <= 0.1678939074330212 * (mu_Xi T_res)/|c_Gamma|.
```

Using `mu_Xi ~= Pi_B/tau_L`:

```text
A_J,eff_private <= 0.167893843691 * Pi_B*(T_res/tau_L)/|c_Gamma|.
```

The gradient row is much looser in the same window, but `alpha3` still needs its own arena profile:

```text
|c_Gamma profile_alpha3| <= 4e-20.
```

## What Is Still Missing

This is not a pass. The unfilled source rows are now exactly:

```text
A_src,
A_lap,
A_drift,
T_res/tau_L,
c_Gamma,
profile_a/J_a.
```

## Next Target

`{NEXT_TARGET}`
"""


def checkpoint_doc() -> str:
    return f"""
# 4236 - cGamma Parent Memory Equation Or AJ Coefficient Source Fill

**Status:** `{DECISION}`.

## Forward Move

This checkpoint reduces the live private cGamma problem to three source coefficients:

```text
A_J,eff_private = A_src + A_lap + A_drift.
```

That is progress: `A_boundary` is privately zero/routed, and `Kperp` no longer belongs in the private AJ budget.

## Still Not A Pass

The three coefficients are not numerically filled or parent-zero yet:

```text
A_src, A_lap, A_drift = unfilled.
```

So the branch remains a serious, testable coefficient problem rather than a local-GR claim.

## Next

`{NEXT_TARGET}`
"""


def update_claim_register() -> None:
    path = FORMAL / "02-claims-register.csv"
    rows = csv_rows(path)
    if any(row.get("claim_id") == CLAIM_ID for row in rows):
        return
    rows.append(
        {
            "claim_id": CLAIM_ID,
            "domain": "local_gr",
            "claim": "The cGamma parent memory equation is now in normal form and the private AJ amplitude ledger is reduced to three source coefficients: A_src, A_lap and A_drift. Boundary and Kperp are privately closed, but the source coefficients, cGamma normalization and arena profiles remain unfilled.",
            "current_evidence": "4236 source register, memory-equation normal form, AJ coefficient ledger, amplitude requirement table, source-fill schema, decision and firewall.",
            "status": "private_cGamma_AJ_three_coefficient_ledger_nonclaim",
            "next_test": "Prove or fill A_src, A_lap and A_drift from parent source-current covariance, leakage Hessian and drift equations; then source T_res/tau_L, cGamma and arena profiles.",
            "key_risk": "Treating the AJ normal form as a numeric bound would overclaim; it is a fillable coefficient ledger, not a pass.",
        }
    )
    with path.open("w", newline="", encoding="utf-8") as handle:
        fieldnames = ["claim_id", "domain", "claim", "current_evidence", "status", "next_test", "key_risk"]
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def update_spine_and_packet() -> None:
    spine_block = f"""
## PPC4161 cGamma Parent Memory Equation AJ Ledger

Marker: `{MARKER}`

4236 writes the parent memory equation normal form:

```text
L_Xi delta Xi = J_res,
J_res = U_B S_cg + D_m Delta_h m_L - D_t m_L + boundary_in.
```

After private boundary/Kperp closure:

```text
A_J,eff_private = A_src + A_lap + A_drift.
```

The strong local Gdot row now demands `A_J,eff_private <= 0.1678939074330212*(mu_Xi T_res)/|c_Gamma|`. This is not a pass; it is the exact coefficient fill target.
"""
    packet_block = f"""
## Packet Update - cGamma Parent Memory Equation AJ Ledger

Marker: `{PACKET_MARKER}`

The private cGamma obstruction has been reduced from an amorphous source/profile problem to:

```text
A_src, A_lap, A_drift, T_res/tau_L, c_Gamma, profile_a/J_a.
```

Boundary and Kperp are not in the private AJ budget. The next work is the source coefficient theorem or numeric/source fill pack.
"""
    append_once(FORMAL / "07-unification-spine.md", MARKER, spine_block)
    append_once(FORMAL / "180-PPC4161-private-local-packet-integration.md", PACKET_MARKER, packet_block)


def validation_rows() -> List[Dict[str, str]]:
    rows: List[Dict[str, str]] = []

    def add(check_id: str, description: str, passed: bool, evidence: str) -> None:
        rows.append(
            {
                **common(),
                "check_id": check_id,
                "description": description,
                "passed": str(bool(passed)),
                "evidence": evidence,
                "claim_allowed": "False",
                "valid_for_claim": "False",
            }
        )

    sources = source_rows()
    memory_rows = memory_equation_rows()
    aj_rows = aj_coefficient_rows()
    amplitude_rows = amplitude_requirement_rows()
    fill_rows = source_fill_schema_rows()
    add("VAL4236_0_sources_exist", "all source paths exist", all(row["exists"] == "True" for row in sources), "source register")
    add("VAL4236_1_needles_found", "all source needles found", all(row["required_text_found"] == "True" for row in sources), "source register")
    add("VAL4236_2_memory_normal_form", "memory equation rows include L_Xi and J_res", {"ME4236_1_operator", "ME4236_3_source"}.issubset({row["row_id"] for row in memory_rows}), "memory rows")
    add("VAL4236_3_AJ_three_coefficients", "AJ private ledger has A_src/A_lap/A_drift", {"A_src", "A_lap", "A_drift"}.issubset({row["coefficient"] for row in aj_rows}), "AJ rows")
    add("VAL4236_4_boundary_private_zero", "A_boundary is private-zero/open-global", any(row["coefficient"] == "A_boundary" and row["status"] == "private_zero_open_global" for row in aj_rows), "AJ rows")
    add("VAL4236_5_Kperp_closed", "Kperp is private closed in AJ ledger", any(row["coefficient"] == "Kperp contribution" and row["status"] == "private_closed" for row in aj_rows), "AJ rows")
    add("VAL4236_6_strong_amplitude", "strong Gdot amplitude coefficient recorded", any(row["requirement_id"] == "AR4236_0_strong_Gdot" and "0.1678939074330212" in row["amplitude_bound"] for row in amplitude_rows), "amplitude rows")
    add("VAL4236_7_fill_schema", "fill schema has unfilled source/profile rows", len(fill_rows) == 7 and all(row["valid_for_claim"] == "False" for row in fill_rows), "fill schema")
    add("VAL4236_8_decision_not_scoreable", "decision keeps scoreable false", decision_rows()[0]["scoreable_now"] == "False", "decision")
    add("VAL4236_9_docs_written", "formal and checkpoint docs exist", FORMAL_PATH.exists() and DOC_PATH.exists(), f"{FORMAL_PATH}; {DOC_PATH}")
    add("VAL4236_10_claim_register", "claims register contains L-077", CLAIM_ID in read_text(FORMAL / "02-claims-register.csv"), str(FORMAL / "02-claims-register.csv"))
    add("VAL4236_11_spine_marker", "spine contains marker", MARKER in read_text(FORMAL / "07-unification-spine.md"), str(FORMAL / "07-unification-spine.md"))
    add("VAL4236_12_packet_marker", "packet contains marker", PACKET_MARKER in read_text(FORMAL / "180-PPC4161-private-local-packet-integration.md"), str(FORMAL / "180-PPC4161-private-local-packet-integration.md"))
    add("VAL4236_13_no_claim_flags", "no generated row is valid for claim", all(row.get("valid_for_claim") != "True" for group in (sources, memory_rows, aj_rows, amplitude_rows, fill_rows, decision_rows(), firewall_rows(), status_rows(), next_target_rows()) for row in group), "all generated groups")
    add("VAL4236_14_next_target", "next target selected", next_target_rows()[0]["next_target"] == NEXT_TARGET, NEXT_TARGET)
    return rows


def main() -> None:
    paths = {
        "source": SOURCE_DIR / "P8_Y5_R2FR_4236_SOURCE_REGISTER.csv",
        "memory": SOURCE_DIR / "P8_Y5_R2FR_4236_MEMORY_EQUATION_NORMAL_FORM.csv",
        "aj": SOURCE_DIR / "P8_Y5_R2FR_4236_AJ_COEFFICIENT_LEDGER.csv",
        "amplitude": SOURCE_DIR / "P8_Y5_R2FR_4236_AMPLITUDE_REQUIREMENT_TABLE.csv",
        "fill": SOURCE_DIR / "P8_Y5_R2FR_4236_SOURCE_FILL_SCHEMA.csv",
        "decision": SOURCE_DIR / "P8_Y5_R2FR_4236_DECISION.csv",
        "firewall": SOURCE_DIR / "P8_Y5_R2FR_4236_CLAIM_FIREWALL.csv",
        "status": SOURCE_DIR / "P8_Y5_R2FR_4236_STATUS.csv",
        "next": SOURCE_DIR / "P8_Y5_R2FR_4236_NEXT_TARGET.csv",
    }
    write_text(FORMAL_PATH, formal_doc())
    write_text(DOC_PATH, checkpoint_doc())
    write_csv(paths["source"], source_rows())
    write_csv(paths["memory"], memory_equation_rows())
    write_csv(paths["aj"], aj_coefficient_rows())
    write_csv(paths["amplitude"], amplitude_requirement_rows())
    write_csv(paths["fill"], source_fill_schema_rows())
    write_csv(paths["decision"], decision_rows())
    write_csv(paths["firewall"], firewall_rows())
    write_csv(paths["status"], status_rows())
    write_csv(paths["next"], next_target_rows())
    update_claim_register()
    update_spine_and_packet()
    write_csv(VALIDATION_PATH, validation_rows())
    failed_rows = [row for row in csv_rows(VALIDATION_PATH) if row["passed"] != "True"]
    print(f"Decision: {DECISION}")
    print(f"Formal: {FORMAL_PATH}")
    print(f"Checkpoint: {DOC_PATH}")
    print(f"Validation: {VALIDATION_PATH}")
    print(f"Validation rows: {len(csv_rows(VALIDATION_PATH))}; failed: {len(failed_rows)}")
    if failed_rows:
        for failed_row in failed_rows:
            print(f"FAILED {failed_row['check_id']}: {failed_row['evidence']}")
        raise SystemExit(1)


if __name__ == "__main__":
    main()

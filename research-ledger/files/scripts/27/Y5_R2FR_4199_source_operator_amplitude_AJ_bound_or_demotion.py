from __future__ import annotations

import csv
import json
import py_compile
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List


ROOT = Path(
    r"D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main"
)
POST = ROOT / "post-checkpoint-work"
SOURCE_DIR = POST / "source-intake" / "mts_residuals"
FORMAL = ROOT / "formalization-workbench"
SCRIPT_PATH = Path(__file__)

CHECKPOINT = "4199"
BRANCH_ID = "MTS_R2FR_Y5_SOURCE_OPERATOR_AJ_BOUND_4199"
DECISION = (
    "SOURCE_OPERATOR_AJ_BOUND_CONTRACT_DERIVED_SUPPORT_POWERS_COMPATIBLE_BUT_COEFFICIENTS_"
    "BOUNDARY_KPERP_PARENT_OWNER_MISSING_DEMOTE_IF_UNSIGNED_NONCLAIM"
)
DOC_PATH = POST / "4199-Y5-R2FR-source-operator-amplitude-AJ-bound-or-demotion.md"
FORMAL_PATH = FORMAL / "215-PPC4161-source-operator-amplitude-AJ-bound.md"
PACKET_180_PATH = FORMAL / "180-PPC4161-private-local-packet-integration.md"
CLAIMS_PATH = FORMAL / "02-claims-register.csv"
SPINE_PATH = FORMAL / "07-unification-spine.md"
CLAIM_ID = "L-040"
SPINE_MARKER = "PPC4161_SOURCE_OPERATOR_AJ_BOUND_4199"
PACKET_MARKER = "PPC4161_PACKET_SOURCE_OPERATOR_AJ_BOUND_4199"
NEXT_TARGET = "4200-Y5-R2FR-Kperp-boundary-zero-or-local-branch-demotion.md"

SUPPORT_STATUS = FORMAL / "runs" / "support_powers_kperp_20260527-181919" / "status.json"
SUPPORT_SUMMARY = FORMAL / "runs" / "support_powers_kperp_20260527-181919" / "summary.csv"
BOUNDARY_STATUS = FORMAL / "runs" / "source_support_boundary_20260527-180012" / "status.json"
BOUNDARY_SUMMARY = FORMAL / "runs" / "source_support_boundary_20260527-180012" / "summary.csv"
POWER_LAWS = FORMAL / "runs" / "20260528-140716-local-source-power-theorem" / "results" / "power_laws.csv"
GRADIENT_BOUNDS = FORMAL / "runs" / "20260528-174151-repaired-local-gradient-power" / "results" / "gradient_bounds.csv"

SOURCES = {
    "SRC4199_00_4198_formal": (
        FORMAL / "214-PPC4161-parent-amplitude-owner-for-Jres.md",
        "A_J,eff = A_src + A_lap + A_drift + A_boundary/U_B^2",
        "4198 amplitude decomposition handoff.",
    ),
    "SRC4199_01_71_law": (
        FORMAL / "71-source-support-boundary-law.md",
        "A_src = sup |S_*|/mu_B",
        "Source-support and boundary-amplitude law.",
    ),
    "SRC4199_02_support_status": (
        SUPPORT_STATUS,
        "window43_required_pS",
        "Prior support-power/Kperp status.",
    ),
    "SRC4199_03_support_summary": (
        SUPPORT_SUMMARY,
        "window43_min_local_required_powers",
        "Prior support-power/Kperp summary.",
    ),
    "SRC4199_04_boundary_status": (
        BOUNDARY_STATUS,
        "strong_support_M_total",
        "Prior boundary/source-support status.",
    ),
    "SRC4199_05_power_laws": (
        POWER_LAWS,
        "source_linear_silence",
        "Local source-power theorem rows.",
    ),
    "SRC4199_06_gradient_bounds": (
        GRADIENT_BOUNDS,
        "requires_bounded_coefficients",
        "Repaired gradient coefficient-bound warning.",
    ),
    "SRC4199_07_boundary_theorem": (
        FORMAL / "192-PPC4161-local-boundary-no-flux-sector-interface-theorem.md",
        "F_rad[tau] != 0  =>  route as boundary charge, not hidden bulk current.",
        "Private local boundary/no-flux selector theorem.",
    ),
}


def now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def common() -> Dict[str, str]:
    return {
        "timestamp_utc": now(),
        "branch_id": BRANCH_ID,
        "checkpoint_id": CHECKPOINT,
    }


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8") if path.exists() else ""


def write_csv(path: Path, rows: List[Dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        raise ValueError(f"no rows for {path}")
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def parse_csv(path: Path) -> List[Dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def parse_json(path: Path) -> Dict[str, object]:
    return json.loads(path.read_text(encoding="utf-8"))


def append_unique_line(path: Path, marker: str, line: str) -> None:
    text = read_text(path)
    if marker in text:
        return
    with path.open("a", encoding="utf-8", newline="") as handle:
        if text and not text.endswith("\n"):
            handle.write("\n")
        handle.write(line)


def append_unique_csv_row(path: Path, key_column: str, key_value: str, row: Dict[str, str]) -> None:
    rows = parse_csv(path)
    if any(existing.get(key_column) == key_value for existing in rows):
        return
    with path.open("a", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writerow(row)


def fmt(value: float) -> str:
    return f"{value:.12g}"


def support_power_passes(available_power: float, required_power: float) -> bool:
    return available_power + 1e-12 >= required_power


def source_rows() -> List[Dict[str, str]]:
    rows: List[Dict[str, str]] = []
    for source_id, (path, required_text, role) in SOURCES.items():
        text = read_text(path)
        rows.append(
            {
                **common(),
                "source_id": source_id,
                "path": str(path),
                "exists": str(path.exists()),
                "required_text": required_text,
                "required_text_found": str(required_text in text),
                "role": role,
                "claim_allowed": "False",
                "valid_for_claim": "False",
            }
        )
    return rows


def amplitude_contract_rows() -> List[Dict[str, str]]:
    entries = [
        (
            "AJC4199_0_source",
            "A_src",
            "U_B S_cg",
            "If S_cg(0,Y)=0 and ||partial_z S_cg||<=C_S, while ||z_L||<=C_D U_B, then ||U_B S_cg||<=U_B^2 C_D C_S.",
            "A_src <= C_D C_S",
            "conditional_operator_Lipschitz_not_parent_numeric",
        ),
        (
            "AJC4199_1_laplacian",
            "A_lap",
            "D_m Delta_h m_L",
            "If m_L=m_*+1/2 H_AB z^A z^B+O(|z|^3), ||H||<=C_M, and leakage gradients are bounded by L_B, then the laplacian term is U_B^2 times a coefficient owned by D_m, C_M and gradient geometry.",
            "A_lap <= D_m C_M C_lap/L_B^2",
            "conditional_requires_scalar_Hessian_and_gradient_bounds",
        ),
        (
            "AJC4199_2_drift",
            "A_drift",
            "-D_t m_L",
            "If the same scalar Hessian bound holds and D_t z_L preserves U_B powers over T_B, then drift is U_B^2 times a coefficient owned by C_M and residual drift geometry.",
            "A_drift <= C_M C_t/T_B",
            "conditional_requires_time_gradient_bounds",
        ),
        (
            "AJC4199_3_boundary",
            "A_boundary/U_B^2",
            "boundary_in",
            "Boundary is harmless only if no-flux/Hamiltonian routing sets it zero, or if M_bdy exp(-ell/ell_scr)/U_B^2 is carried explicitly.",
            "A_boundary_eff <= M_bdy exp(-ell/ell_scr)/U_B^2",
            "conditional_or_demotion_if_unsigned",
        ),
        (
            "AJC4199_4_total",
            "A_J,eff",
            "J_res",
            "Combining the three bulk terms and the boundary term gives the parent-source-operator amplitude contract.",
            "A_J,eff <= C_D C_S + D_m C_M C_lap/L_B^2 + C_M C_t/T_B + A_boundary/U_B^2",
            "bound_contract_derived_coefficients_unsigned",
        ),
    ]
    return [
        {
            **common(),
            "contract_id": contract_id,
            "amplitude": amplitude,
            "term": term,
            "derivation": derivation,
            "bound_form": bound_form,
            "status": status,
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
        for contract_id, amplitude, term, derivation, bound_form, status in entries
    ]


def support_compatibility_rows() -> List[Dict[str, str]]:
    status = parse_json(SUPPORT_STATUS)
    window_required_pS = float(status["window43_required_pS"])
    window_required_pL = float(status["window43_required_pL"])
    weak_required_pS = float(status["weaker_margin_required_pS"])
    weak_required_pL = float(status["weaker_margin_required_pL"])
    rows = [
        (
            "SUP4199_0_strong_source",
            "strong/window43",
            "source",
            1.0,
            window_required_pS,
            "4194 nS=1 exceeds prior required pS for strong local window if amplitude is order-one.",
        ),
        (
            "SUP4199_1_strong_laplacian_drift",
            "strong/window43",
            "m_L/trace",
            2.0,
            window_required_pL,
            "4194 nL=2 exceeds prior required pL/pT for strong local window if coefficients are bounded.",
        ),
        (
            "SUP4199_2_weak_source",
            "weaker U_B=1e-4",
            "source",
            1.0,
            weak_required_pS,
            "4194 nS=1 only just meets weaker source-power requirement; no amplitude slack.",
        ),
        (
            "SUP4199_3_weak_laplacian_drift",
            "weaker U_B=1e-4",
            "m_L/trace",
            2.0,
            weak_required_pL,
            "4194 nL=2 only just meets weaker m_L/trace requirement; no amplitude slack.",
        ),
    ]
    return [
        {
            **common(),
            "compat_id": compat_id,
            "regime": regime,
            "term_family": term_family,
            "available_power": fmt(available_power),
            "required_power": fmt(required_power),
            "power_passes": str(support_power_passes(available_power, required_power)),
            "interpretation": interpretation,
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
        for compat_id, regime, term_family, available_power, required_power, interpretation in rows
    ]


def boundary_kperp_rows() -> List[Dict[str, str]]:
    status = parse_json(BOUNDARY_STATUS)
    support_status = parse_json(SUPPORT_STATUS)
    entries = [
        (
            "BK4199_0_boundary_screening",
            "boundary_AJ",
            f"weak boundary case required ell/ell_scr >= {status['weak_boundary_required_ell_over_ell_scr']}",
            "conditional",
            "boundary mismatch must be screened or Hamiltonian-routed; otherwise A_boundary/U_B^2 can dominate",
        ),
        (
            "BK4199_1_Kperp_zero",
            "K_perp",
            support_status["verdict"],
            "open_or_conditional",
            "scalar source support does not kill transverse homogeneous tensor modes",
        ),
        (
            "BK4199_2_private_no_flux",
            "compact local boundary",
            "192 gives no-flux/Hamiltonian routing only inside private selector branch",
            "private_selector_conditional",
            "not global parent adoption; finite radiative boundary charges must be routed explicitly",
        ),
    ]
    return [
        {
            **common(),
            "boundary_id": boundary_id,
            "quantity": quantity,
            "evidence": evidence,
            "status": status,
            "meaning": meaning,
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
        for boundary_id, quantity, evidence, status, meaning in entries
    ]


def demotion_rows() -> List[Dict[str, str]]:
    entries = [
        (
            "DEM4199_0_parent_operator_pass",
            "all coefficients C_D,C_S,C_M,C_lap,C_t and boundary routing are parent-signed",
            "keep as conditional derived local branch",
            "not_current_state",
        ),
        (
            "DEM4199_1_source_coefficients_unsigned",
            "C_S, scalar Hessian, leakage-gradient constants or D_m normalization are not parent-owned",
            "demote A_J to explicit phenomenological local closure amplitude",
            "current_state",
        ),
        (
            "DEM4199_2_boundary_or_Kperp_unsigned",
            "A_boundary or K_perp zero/bound theorem is unsigned",
            "demote exact local-GR route; retain finite bound runner only",
            "current_state",
        ),
        (
            "DEM4199_3_weak_window_no_slack",
            "weak U_B=1e-4 relies on powers exactly at threshold and has brutal Gdot pressure",
            "do not use weak window as default local safety branch",
            "current_state",
        ),
    ]
    return [
        {
            **common(),
            "demotion_id": demotion_id,
            "condition": condition,
            "action": action,
            "status": status,
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
        for demotion_id, condition, action, status in entries
    ]


def decision_rows() -> List[Dict[str, str]]:
    compat = support_compatibility_rows()
    strong_power_pass = all(row["power_passes"] == "True" for row in compat if row["regime"] == "strong/window43")
    weak_power_pass = all(row["power_passes"] == "True" for row in compat if row["regime"] == "weaker U_B=1e-4")
    return [
        {
            **common(),
            "decision": DECISION,
            "AJ_bound_contract_derived": "True",
            "support_powers_compatible_strong": str(strong_power_pass),
            "support_powers_compatible_weak_threshold_only": str(weak_power_pass),
            "coefficients_parent_signed": "False",
            "boundary_parent_signed": "False",
            "Kperp_parent_signed": "False",
            "current_route_status": "conditional_bound_contract_not_parent_derivation",
            "demote_if_unsigned": "True",
            "public_local_GR_claim_allowed": "False",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
    ]


def claim_firewall_rows() -> List[Dict[str, str]]:
    entries = [
        (
            "FW4199_0_no_exponent_overclaim",
            "Power compatibility is not amplitude ownership; do not claim local GR from nS=1/nL=2 alone.",
        ),
        (
            "FW4199_1_no_coefficient_invention",
            "C_D, C_S, C_M, C_lap, C_t and D_m normalization must be derived or source-backed before any claim.",
        ),
        (
            "FW4199_2_no_boundary_Kperp_hiding",
            "A_boundary and K_perp are separate hazards; do not absorb them into A_J without explicit rows.",
        ),
        (
            "FW4199_3_demote_if_unsigned",
            "If source-operator coefficients remain unsigned, label the local branch phenomenological closure, not derived MTS local GR.",
        ),
    ]
    return [
        {
            **common(),
            "firewall_id": firewall_id,
            "rule": rule,
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
        for firewall_id, rule in entries
    ]


def next_target_rows() -> List[Dict[str, str]]:
    return [
        {
            **common(),
            "next_target": NEXT_TARGET,
            "why": "4199 derives the AJ bound contract and shows powers are compatible, but Kperp/boundary and coefficient ownership remain the decisive blockers.",
            "route_A": "prove K_perp=0 from positive elliptic/static operator, zero boundary, no zero modes and no incoming modes",
            "route_B": "derive explicit C_S and scalar Hessian coefficient bounds from parent source operator",
            "route_C": "demote local branch to finite phenomenological closure with source-backed priors if route_A/B fail",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
    ]


def status_rows(decision: Dict[str, str]) -> List[Dict[str, str]]:
    return [
        {
            **common(),
            "decision": DECISION,
            "summary": "4199 derives the AJ bound contract and confirms support powers are compatible, but coefficient, boundary and Kperp parent ownership are not signed; demotion remains active if unsigned.",
            "AJ_bound_contract_derived": decision["AJ_bound_contract_derived"],
            "current_route_status": decision["current_route_status"],
            "local_GR_claim": "False",
            "public_claim_allowed": "False",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
    ]


def write_docs(decision: Dict[str, str]) -> None:
    formal = f"""# 215 - PPC4161 Source Operator Amplitude AJ Bound

Marker: `{SPINE_MARKER}`
Checkpoint: `{CHECKPOINT}`
Branch: `{BRANCH_ID}`
Decision: `{DECISION}`

## Claim Status

Private nonclaim. This checkpoint derives the `A_J` bound contract but does not parent-sign the required coefficients, boundary routing, or `K_perp` zero theorem.

## Bound Contract

From:

```text
J_res = U_B S_cg + D_m Delta_h m_L - D_t m_L + boundary_in
```

and the 4194-4196 power route:

```text
S_cg = O(U_B),
m_L - m_* = O(U_B^2),
boundary_in = 0/routed or carried,
```

we get:

```text
J_res = U_B^2 A_J,eff
```

with:

```text
A_J,eff <= C_D C_S
         + D_m C_M C_lap/L_B^2
         + C_M C_t/T_B
         + A_boundary/U_B^2.
```

This is the cleanest current source-operator amplitude law.

## What Improved

The exponent route is compatible with prior power gates:

```text
nS = 1,
nL = 2.
```

The strong/window43 local gate needs weaker powers than this. The weaker `U_B=1e-4` gate is only just met, so it has almost no amplitude slack.

## What Did Not Close

The bound is not a parent derivation unless the parent owns:

```text
C_D, C_S, C_M, C_lap, C_t,
D_m normalization,
A_boundary=0/routed or bounded,
K_perp=0 or PPN-bounded.
```

Existing source-support runs already warn that `K_perp` is separate: scalar support does not kill transverse homogeneous tensor modes.

## Verdict

4199 narrows the local branch:

```text
support powers: compatible,
source-operator coefficient ownership: missing,
boundary/Kperp ownership: missing.
```

So the route is not dead, but if the next gate cannot parent-sign boundary/`Kperp` or coefficient bounds, the local branch should be demoted to an explicit phenomenological closure with source-backed priors.

## Next Gate

`{NEXT_TARGET}` should attack `K_perp` and boundary zero directly, because those are not solved by the scalar amplitude law.
"""
    checkpoint = f"""# 4199 - Y5 R2FR Source Operator Amplitude AJ Bound Or Demotion

Decision: `{DECISION}`

## Summary

4199 derives the current best `A_J` amplitude contract:

```text
A_J,eff <= C_D C_S
         + D_m C_M C_lap/L_B^2
         + C_M C_t/T_B
         + A_boundary/U_B^2.
```

The exponent route is compatible:

```text
nS=1, nL=2.
```

But the route is still nonclaim because the coefficients, boundary routing, and `K_perp` zero/bound are not parent-signed.

## Practical Verdict

This is not circling: the next blocker is now specific.

Either prove boundary/`Kperp` zero and source-operator coefficient bounds, or demote the clean local branch to an explicit finite closure with priors.
"""
    FORMAL_PATH.write_text(formal, encoding="utf-8")
    DOC_PATH.write_text(checkpoint, encoding="utf-8")


def write_register_updates(decision: Dict[str, str]) -> None:
    append_unique_csv_row(
        CLAIMS_PATH,
        "claim_id",
        CLAIM_ID,
        {
            "claim_id": CLAIM_ID,
            "domain": "local_gr",
            "claim": "The source-operator A_J bound contract is derived and the support powers nS=1,nL=2 are compatible with prior local power gates, but coefficient ownership, boundary routing and K_perp remain unsigned.",
            "current_evidence": "4199 source audit, A_J amplitude contract, support-power compatibility table, boundary/Kperp ledger, demotion ledger, decision row and nonclaim firewall.",
            "status": "private_AJ_bound_contract_nonclaim_coefficients_boundary_Kperp_unsigned",
            "next_test": "Prove K_perp/boundary zero or source explicit coefficient bounds; otherwise demote local branch to source-backed phenomenological closure.",
            "key_risk": "Support powers can look like a derivation while hiding coefficient blow-up, boundary leakage, or transverse tensor K_perp modes.",
        },
    )
    append_unique_line(
        SPINE_PATH,
        SPINE_MARKER,
        f"""

### PPC4161 Source Operator AJ Bound - 4199

Marker: `{SPINE_MARKER}`
Claim register row: `{CLAIM_ID}`

4199 derives the current source-operator amplitude contract:

```text
A_J,eff <= C_D C_S
         + D_m C_M C_lap/L_B^2
         + C_M C_t/T_B
         + A_boundary/U_B^2.
```

The support powers `nS=1,nL=2` are compatible with prior local power gates, but coefficient ownership, boundary routing and `K_perp` are not parent-signed. Demotion remains active if those clauses stay unsigned.
""",
    )
    append_unique_line(
        PACKET_180_PATH,
        PACKET_MARKER,
        f"""

## PPC4161 Packet Source Operator AJ Bound - 4199

Marker: `{PACKET_MARKER}`

Inside the private packet, `A_J` is no longer a mystery scalar:

```text
A_J,eff = A_src + A_lap + A_drift + A_boundary/U_B^2.
```

The bound contract is clean, but not parent-signed. The packet remains nonclaim until source-operator coefficients and boundary/`Kperp` zero-or-bound are derived.
""",
    )


def all_rows() -> Dict[str, List[Dict[str, str]]]:
    decision = decision_rows()
    return {
        "P8_Y5_R2FR_4199_SOURCE_REGISTER.csv": source_rows(),
        "P8_Y5_R2FR_4199_AJ_BOUND_CONTRACT.csv": amplitude_contract_rows(),
        "P8_Y5_R2FR_4199_SUPPORT_POWER_COMPATIBILITY.csv": support_compatibility_rows(),
        "P8_Y5_R2FR_4199_BOUNDARY_KPERP_LEDGER.csv": boundary_kperp_rows(),
        "P8_Y5_R2FR_4199_DEMOTION_LEDGER.csv": demotion_rows(),
        "P8_Y5_R2FR_4199_DECISION.csv": decision,
        "P8_Y5_R2FR_4199_CLAIM_FIREWALL.csv": claim_firewall_rows(),
        "P8_Y5_R2FR_4199_NEXT_TARGET.csv": next_target_rows(),
        "P8_Y5_R2FR_4199_STATUS.csv": status_rows(decision[0]),
    }


def validate(rows_by_file: Dict[str, List[Dict[str, str]]]) -> List[Dict[str, str]]:
    source = rows_by_file["P8_Y5_R2FR_4199_SOURCE_REGISTER.csv"]
    contract = rows_by_file["P8_Y5_R2FR_4199_AJ_BOUND_CONTRACT.csv"]
    compat = rows_by_file["P8_Y5_R2FR_4199_SUPPORT_POWER_COMPATIBILITY.csv"]
    boundary = rows_by_file["P8_Y5_R2FR_4199_BOUNDARY_KPERP_LEDGER.csv"]
    demotion = rows_by_file["P8_Y5_R2FR_4199_DEMOTION_LEDGER.csv"]
    decision = rows_by_file["P8_Y5_R2FR_4199_DECISION.csv"][0]
    firewall = rows_by_file["P8_Y5_R2FR_4199_CLAIM_FIREWALL.csv"]
    checks = [
        ("VAL4199_0_sources_exist", "all source paths exist", all(row["exists"] == "True" for row in source)),
        ("VAL4199_1_source_tokens", "all source required text markers found", all(row["required_text_found"] == "True" for row in source)),
        ("VAL4199_2_total_bound", "A_J total bound contract exists", any(row["amplitude"] == "A_J,eff" and "A_boundary/U_B^2" in row["bound_form"] for row in contract)),
        ("VAL4199_3_support_powers_pass", "all listed support powers pass compatibility check", all(row["power_passes"] == "True" for row in compat)),
        ("VAL4199_4_weak_no_slack", "weak rows are threshold-only for source and mL/trace", any(row["regime"] == "weaker U_B=1e-4" and row["available_power"] == row["required_power"] for row in compat)),
        ("VAL4199_5_boundary_Kperp_open", "boundary/Kperp ledger includes open/conditional Kperp", any("K_perp" in row["quantity"] and row["status"] == "open_or_conditional" for row in boundary)),
        ("VAL4199_6_demotion_active", "demotion ledger contains current_state rows", any(row["status"] == "current_state" for row in demotion)),
        ("VAL4199_7_decision_nonclaim", "decision says coefficients and boundary/Kperp unsigned", decision["coefficients_parent_signed"] == "False" and decision["boundary_parent_signed"] == "False" and decision["Kperp_parent_signed"] == "False"),
        (
            "VAL4199_8_no_claim_flags",
            "no 4199 row has claim_allowed or valid_for_claim true",
            all(
                row.get("claim_allowed", "False") == "False" and row.get("valid_for_claim", "False") == "False"
                for table in rows_by_file.values()
                for row in table
            ),
        ),
        ("VAL4199_9_firewall_rows", "firewall has four anti-smuggling rows", len(firewall) == 4),
        ("VAL4199_10_docs_written", "formal and checkpoint docs contain decision", DECISION in read_text(FORMAL_PATH) and DECISION in read_text(DOC_PATH)),
        ("VAL4199_11_claim_register", "claim register has L-040", CLAIM_ID in read_text(CLAIMS_PATH)),
        ("VAL4199_12_spine_marker", "spine marker appended", SPINE_MARKER in read_text(SPINE_PATH)),
        ("VAL4199_13_packet_marker", "packet marker appended", PACKET_MARKER in read_text(PACKET_180_PATH)),
    ]
    return [
        {
            **common(),
            "check_id": check_id,
            "check": check,
            "passed": str(bool(passed)),
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
        for check_id, check, passed in checks
    ]


def write_all() -> None:
    SOURCE_DIR.mkdir(parents=True, exist_ok=True)
    rows_by_file = all_rows()
    decision = rows_by_file["P8_Y5_R2FR_4199_DECISION.csv"][0]
    write_docs(decision)
    write_register_updates(decision)
    for filename, rows in rows_by_file.items():
        write_csv(SOURCE_DIR / filename, rows)
    validation = validate(rows_by_file)
    write_csv(SOURCE_DIR / "P8_Y5_BRR545_4199_VALIDATION.csv", validation)
    if not all(row["passed"] == "True" for row in validation):
        failed = [row for row in validation if row["passed"] != "True"]
        raise RuntimeError(f"4199 validation failed: {failed}")
    py_compile.compile(str(SCRIPT_PATH), doraise=True)
    pycache = SCRIPT_PATH.parent / "__pycache__"
    if pycache.exists():
        shutil.rmtree(pycache)


def main() -> None:
    write_all()
    print(DECISION)
    print(f"formal={FORMAL_PATH}")
    print(f"checkpoint={DOC_PATH}")
    print(f"validation={SOURCE_DIR / 'P8_Y5_BRR545_4199_VALIDATION.csv'}")
    print("rows=14 validation checks")


if __name__ == "__main__":
    main()

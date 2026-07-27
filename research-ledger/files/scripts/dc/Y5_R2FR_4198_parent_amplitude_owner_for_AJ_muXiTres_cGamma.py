from __future__ import annotations

import csv
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

CHECKPOINT = "4198"
BRANCH_ID = "MTS_R2FR_Y5_PARENT_AMPLITUDE_OWNER_4198"
DECISION = (
    "PARENT_AMPLITUDE_OWNER_REDUCES_MUXITRES_TO_PIB_TRES_OVER_TAUL_AND_CGAMMA_CEILING_"
    "AJ_BOUNDARY_SOURCE_AMPLITUDES_STILL_UNSIGNED_NONCLAIM"
)
DOC_PATH = POST / "4198-Y5-R2FR-parent-amplitude-owner-for-AJ-muXiTres-cGamma.md"
FORMAL_PATH = FORMAL / "214-PPC4161-parent-amplitude-owner-for-Jres.md"
PACKET_180_PATH = FORMAL / "180-PPC4161-private-local-packet-integration.md"
CLAIMS_PATH = FORMAL / "02-claims-register.csv"
SPINE_PATH = FORMAL / "07-unification-spine.md"
CLAIM_ID = "L-039"
SPINE_MARKER = "PPC4161_PARENT_AMPLITUDE_OWNER_4198"
PACKET_MARKER = "PPC4161_PACKET_PARENT_AMPLITUDE_OWNER_4198"
NEXT_TARGET = "4199-Y5-R2FR-source-operator-amplitude-AJ-bound-or-demotion.md"

BUDGET_4197 = SOURCE_DIR / "P8_Y5_R2FR_4197_REQUIRED_SCALE_TABLE.csv"
DECISION_4197 = SOURCE_DIR / "P8_Y5_R2FR_4197_DECISION.csv"

AJEFF_VALUES = [0.1, 1.0]
RELAXATION_RATIO_VALUES = [0.1, 1.0, 10.0, 100.0]

SOURCES = {
    "SRC4198_00_4197_formal": (
        FORMAL / "213-PPC4161-normalized-Jres-profile-smoke.md",
        "derive A_J,eff",
        "4197 numeric pressure-test handoff.",
    ),
    "SRC4198_01_4197_required_scale": (
        BUDGET_4197,
        "NB4194_strong_local_Gdot_cGamma_1e+00_EFFAJ1",
        "4197 required-scale rows.",
    ),
    "SRC4198_02_4197_decision": (
        DECISION_4197,
        "strong_local_cGamma1_required_muXiT_for_effective_AJ1",
        "4197 decision row.",
    ),
    "SRC4198_03_4192_hessian": (
        FORMAL / "208-PPC4161-parent-Xi-Hessian-signs-and-boundary-domain.md",
        "M_Xi^2  = mu_Xi ~ mu_B = Pi_B/tau_L",
        "4192 maps Xi Hessian to open-system relaxation.",
    ),
    "SRC4198_04_4193_residual": (
        FORMAL / "209-PPC4161-residual-source-projector-and-Xi-profile-amplitude-bound.md",
        "||J_res|| <=",
        "4193 residual source and Green-profile budget.",
    ),
    "SRC4198_05_4194_power": (
        FORMAL / "210-PPC4161-source-support-powers-for-Jres.md",
        "J_res = O(U_B^2)",
        "4194 source-support power result.",
    ),
    "SRC4198_06_4196_scalar": (
        FORMAL / "212-PPC4161-scalar-leakage-reference-nulling.md",
        "z_Lcg    -> pruned",
        "4196 scalar leakage closure status.",
    ),
    "SRC4198_07_202_cgamma": (
        FORMAL / "202-PPC4161-same-coframe-source-memory-zero-law.md",
        "c_Gamma_parent_zero = false",
        "c_Gamma same-coframe memory blocker.",
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


def amplitude_decomposition_rows() -> List[Dict[str, str]]:
    entries = [
        (
            "AMP4198_0_source",
            "U_B S_cg",
            "S_cg=O(U_B) from parity/source covariance route",
            "A_src",
            "A_src <= C_D C_S if ||z_L||<=C_D U_B and ||S_cg||<=C_S||z_L||",
            "not_parent_numeric",
        ),
        (
            "AMP4198_1_laplacian",
            "D_m Delta_h m_L",
            "m_L-m_0=O(U_B^2) from scalar evenness/envelope route",
            "A_lap",
            "A_lap owned by D_m, Hessian of m_L in leakage variables, and leakage-gradient scale L_B",
            "not_parent_numeric",
        ),
        (
            "AMP4198_2_drift",
            "-D_t m_L",
            "m_L-m_0=O(U_B^2) plus bounded time variation of leakage invariants",
            "A_drift",
            "A_drift owned by scalar Hessian, D_t z_L, and residual timescale T_B/T_res",
            "not_parent_numeric",
        ),
        (
            "AMP4198_3_boundary",
            "boundary_in",
            "zero/no-flux/Hamiltonian routing or finite boundary amplitude",
            "A_boundary",
            "A_boundary must be zero/routed or enter A_J,eff as A_boundary/U_B^2",
            "boundary_unsigned",
        ),
        (
            "AMP4198_4_total",
            "J_res=U_B^2 A_J,eff",
            "4194 nJ=2 route plus 4197 boundary-equivalent amplitude",
            "A_J,eff",
            "A_J,eff = A_src + A_lap + A_drift + A_boundary/U_B^2 after common normalization",
            "decomposition_derived_numeric_owner_missing",
        ),
    ]
    return [
        {
            **common(),
            "amplitude_id": amplitude_id,
            "term": term,
            "power_owner": power_owner,
            "amplitude_symbol": amplitude_symbol,
            "amplitude_owner_law": amplitude_owner_law,
            "status": status,
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
        for amplitude_id, term, power_owner, amplitude_symbol, amplitude_owner_law, status in entries
    ]


def gdot_budget_rows() -> List[Dict[str, str]]:
    return [
        row
        for row in parse_csv(BUDGET_4197)
        if row["channel"] == "D_t Xi_0" and row["effective_AJ"] in {"0.1", "1"}
    ]


def relaxation_conversion_rows() -> List[Dict[str, str]]:
    rows: List[Dict[str, str]] = []
    for row in gdot_budget_rows():
        u_b = float(row["window"].startswith("strong") and 3.796559535779445e-7 or 1e-4)
        pi_b = 1.0 - u_b
        required_mu_t = float(row["required_normalized_scale"])
        required_t_over_tau = required_mu_t / pi_b
        rows.append(
            {
                **common(),
                "conversion_id": f"CONV4198_{row['requirement_id']}",
                "source_requirement_id": row["requirement_id"],
                "window": row["window"],
                "assumed_abs_cGamma": row["assumed_abs_cGamma"],
                "effective_AJ": row["effective_AJ"],
                "U_B": fmt(u_b),
                "Pi_B_from_1_minus_U_B": fmt(pi_b),
                "required_muXi_Tres": row["required_normalized_scale"],
                "muXi_law": "mu_Xi ~= mu_B = Pi_B/tau_L",
                "required_Tres_over_tauL": fmt(required_t_over_tau),
                "interpretation": "if mu_Xi=Pi_B/tau_L then T_res/tau_L must exceed this value",
                "claim_allowed": "False",
                "valid_for_claim": "False",
            }
        )
    return rows


def cgamma_ceiling_rows() -> List[Dict[str, str]]:
    rows: List[Dict[str, str]] = []
    base_rows = [
        r
        for r in parse_csv(BUDGET_4197)
        if r["channel"] == "D_t Xi_0" and r["assumed_abs_cGamma"] == "1" and r["effective_AJ"] == "1"
    ]
    for base in base_rows:
        u_b = 3.796559535779445e-7 if base["window"] == "strong_local" else 1e-4
        pi_b = 1.0 - u_b
        base_multiplier = 1.0 / float(base["required_normalized_scale"])
        for a_eff in AJEFF_VALUES:
            for ratio in RELAXATION_RATIO_VALUES:
                mu_t = pi_b * ratio
                ceiling = base_multiplier * mu_t / a_eff
                rows.append(
                    {
                        **common(),
                        "ceiling_id": f"CG4198_{base['window']}_A{a_eff:g}_R{ratio:g}",
                        "window": base["window"],
                        "effective_AJ": fmt(a_eff),
                        "T_res_over_tau_L": fmt(ratio),
                        "Pi_B_from_1_minus_U_B": fmt(pi_b),
                        "muXi_Tres_from_relaxation_law": fmt(mu_t),
                        "base_required_multiplier_cGamma1": fmt(base_multiplier),
                        "max_abs_cGamma_for_Gdot_budget": fmt(ceiling),
                        "passes_if_abs_cGamma_order_1": str(ceiling >= 1.0),
                        "claim_allowed": "False",
                        "valid_for_claim": "False",
                    }
                )
    return rows


def owner_audit_rows() -> List[Dict[str, str]]:
    entries = [
        (
            "OWN4198_0_muXi",
            "mu_Xi T_res",
            "mu_Xi ~= Pi_B/tau_L",
            "partially_derived",
            "turns 4197 scale into T_res/tau_L requirement; numeric tau_L still parent/empirical",
        ),
        (
            "OWN4198_1_AJ",
            "A_J,eff",
            "A_src + A_lap + A_drift + A_boundary/U_B^2",
            "decomposition_derived_coefficients_unsigned",
            "must derive C_S, scalar Hessian, leakage gradients, D_m scale, and boundary amplitude",
        ),
        (
            "OWN4198_2_cGamma",
            "c_Gamma",
            "projection coupling from Gamma_mem to Gdot/preferred-location channels",
            "not_parent_zero",
            "same-coframe law does not kill memory hair; must derive zero/small coefficient or use finite bound",
        ),
        (
            "OWN4198_3_boundary",
            "A_boundary",
            "no-flux/Hamiltonian routing or finite boundary equivalent amplitude",
            "unsigned",
            "cannot be silently set to zero in a claim",
        ),
        (
            "OWN4198_4_strong_window",
            "strong local branch",
            "Pi_B ~= 1 so mu_XiT_res ~= T_res/tau_L",
            "plausible_if_relaxation_ratio_or_AJ_small",
            "for A_J,eff=1 and c_Gamma=1 needs T_res/tau_L around 6",
        ),
        (
            "OWN4198_5_weak_window",
            "weak local branch",
            "U_B=1e-4 leaves U_B^2 too large for Gdot unless c_Gamma/AJ tiny or T_res/tau_L huge",
            "hard",
            "do not use weak local window as local-GR safety story at c_Gamma order 1",
        ),
    ]
    return [
        {
            **common(),
            "owner_id": owner_id,
            "quantity": quantity,
            "owner_law": owner_law,
            "status": status,
            "next_action": next_action,
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
        for owner_id, quantity, owner_law, status, next_action in entries
    ]


def decision_rows(conversions: List[Dict[str, str]], ceilings: List[Dict[str, str]]) -> List[Dict[str, str]]:
    strong_a1_c1 = next(
        row
        for row in conversions
        if row["window"] == "strong_local" and row["effective_AJ"] == "1" and row["assumed_abs_cGamma"] == "1"
    )
    weak_a1_c1 = next(
        row
        for row in conversions
        if row["window"] == "weaker_local" and row["effective_AJ"] == "1" and row["assumed_abs_cGamma"] == "1"
    )
    strong_cg_ratio1 = next(
        row
        for row in ceilings
        if row["window"] == "strong_local" and row["effective_AJ"] == "1" and row["T_res_over_tau_L"] == "1"
    )
    weak_cg_ratio1 = next(
        row
        for row in ceilings
        if row["window"] == "weaker_local" and row["effective_AJ"] == "1" and row["T_res_over_tau_L"] == "1"
    )
    return [
        {
            **common(),
            "decision": DECISION,
            "muXi_owner_law": "mu_Xi ~= Pi_B/tau_L",
            "AJ_owner_decomposition": "A_J,eff=A_src+A_lap+A_drift+A_boundary/U_B^2",
            "strong_AJeff1_cGamma1_required_Tres_over_tauL": strong_a1_c1["required_Tres_over_tauL"],
            "weak_AJeff1_cGamma1_required_Tres_over_tauL": weak_a1_c1["required_Tres_over_tauL"],
            "strong_AJeff1_ratio1_max_abs_cGamma": strong_cg_ratio1["max_abs_cGamma_for_Gdot_budget"],
            "weak_AJeff1_ratio1_max_abs_cGamma": weak_cg_ratio1["max_abs_cGamma_for_Gdot_budget"],
            "parent_AJ_coefficients_signed": "False",
            "parent_cGamma_zero_or_small_signed": "False",
            "boundary_routing_signed": "False",
            "public_local_GR_claim_allowed": "False",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
    ]


def claim_firewall_rows() -> List[Dict[str, str]]:
    entries = [
        (
            "FW4198_0_no_AJ_owner_claim",
            "Do not treat A_J as derived until C_S, scalar Hessian, leakage-gradient, D_m and boundary coefficients are parent-owned.",
        ),
        (
            "FW4198_1_no_cGamma_zero_claim",
            "Do not set c_Gamma to zero or small unless a memory-support/projector theorem or source-backed finite bound supplies it.",
        ),
        (
            "FW4198_2_no_boundary_zero",
            "Do not set A_boundary=0 by convenience; derive no-flux/Hamiltonian routing or keep A_boundary/U_B^2 in A_J,eff.",
        ),
        (
            "FW4198_3_no_weak_window_overclaim",
            "Do not advertise weak local U_B=1e-4 safety for c_Gamma order 1; 4198 keeps it hard unless amplitude/coupling is tiny.",
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
            "why": "4198 reduces the relaxation side but leaves A_J coefficients and c_Gamma parent ownership unsigned.",
            "route_A": "derive C_S and scalar Hessian bounds from the parent source operator/source covariance",
            "route_B": "derive c_Gamma zero/small law from Gamma_mem support/projector verticality",
            "route_C": "derive boundary no-flux/Hamiltonian routing as A_boundary=0 or source a finite A_boundary bound",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
    ]


def status_rows(decision: Dict[str, str]) -> List[Dict[str, str]]:
    return [
        {
            **common(),
            "decision": DECISION,
            "summary": (
                "4198 derives the relaxation conversion mu_Xi T_res ~= Pi_B T_res/tau_L and c_Gamma ceiling law, "
                "but A_J coefficients, c_Gamma parent zero/smallness and boundary routing remain unsigned."
            ),
            "strong_AJeff1_cGamma1_required_Tres_over_tauL": decision["strong_AJeff1_cGamma1_required_Tres_over_tauL"],
            "weak_AJeff1_cGamma1_required_Tres_over_tauL": decision["weak_AJeff1_cGamma1_required_Tres_over_tauL"],
            "local_GR_claim": "False",
            "public_claim_allowed": "False",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
    ]


def write_docs(decision: Dict[str, str]) -> None:
    formal = f"""# 214 - PPC4161 Parent Amplitude Owner For Jres

Marker: `{SPINE_MARKER}`
Checkpoint: `{CHECKPOINT}`
Branch: `{BRANCH_ID}`
Decision: `{DECISION}`

## Claim Status

Private nonclaim. This checkpoint derives the owner map for the 4197 amplitude problem. It does not prove local GR, because the numerical coefficients in `A_J,eff`, finite `c_Gamma`, and boundary routing are not parent-signed.

## Relaxation Owner

4192 maps the Xi mass/relaxation scale to the open-system memory law:

```text
mu_Xi ~= mu_B = Pi_B/tau_L.
```

Therefore:

```text
mu_Xi T_res ~= Pi_B (T_res/tau_L).
```

Since `Pi_B = 1 - U_B`, the 4197 strong local window has `Pi_B ~= 1`.

For `A_J,eff=1` and `|c_Gamma|=1`:

```text
strong local requires T_res/tau_L >= {decision['strong_AJeff1_cGamma1_required_Tres_over_tauL']}
weak local requires   T_res/tau_L >= {decision['weak_AJeff1_cGamma1_required_Tres_over_tauL']}
```

So the strong branch is not absurd if the residual evolves over several local relaxation times. The weak branch remains brutally hard unless the amplitude or coupling is tiny.

## Amplitude Owner

The residual is:

```text
J_res = U_B S_cg + D_m Delta_h m_L - D_t m_L + boundary_in.
```

Under the 4194-4196 power route:

```text
J_res = U_B^2 A_J,eff,
```

with:

```text
A_J,eff = A_src + A_lap + A_drift + A_boundary/U_B^2.
```

The parent must own:

```text
A_src      <= C_D C_S,
A_lap      from D_m, scalar Hessian, and leakage-gradient scale,
A_drift    from scalar Hessian and residual drift timescale,
A_boundary = 0/routed or finite and explicitly carried.
```

## c_Gamma Ceiling

For the `Gdot/G` channel:

```text
|c_Gamma| <= base_multiplier * Pi_B * (T_res/tau_L) / A_J,eff.
```

For `A_J,eff=1` and `T_res/tau_L=1`:

```text
strong local max |c_Gamma| = {decision['strong_AJeff1_ratio1_max_abs_cGamma']}
weak local max |c_Gamma|   = {decision['weak_AJeff1_ratio1_max_abs_cGamma']}
```

So if `c_Gamma` is naturally order one, strong local needs either smaller `A_J,eff` or `T_res/tau_L` around several. Weak local needs a tiny effective coupling/amplitude or a huge relaxation ratio.

## Verdict

4198 moves the missing piece from a vague amplitude problem to four explicit parent obligations:

```text
derive A_src/A_lap/A_drift,
derive or bound A_boundary,
derive or bound c_Gamma,
derive or source tau_L/T_res.
```

No public local-GR claim is allowed.

## Next Gate

`{NEXT_TARGET}` should try to derive `A_src`, scalar Hessian/drift amplitudes, and boundary routing from the parent source operator. If that fails, the local branch must be demoted to an explicit phenomenological closure with source-backed priors.
"""
    checkpoint = f"""# 4198 - Y5 R2FR Parent Amplitude Owner For AJ MuXiTres cGamma

Decision: `{DECISION}`

## Summary

4198 attacks the amplitude-owner problem exposed by 4197.

The useful advance is:

```text
mu_Xi T_res ~= Pi_B (T_res/tau_L).
```

So for the strong local window, `A_J,eff=1`, and `|c_Gamma|=1`, the requirement is roughly:

```text
T_res/tau_L >= {decision['strong_AJeff1_cGamma1_required_Tres_over_tauL']}.
```

That is not dead. It means the residual must evolve over several local relaxation times, or the effective amplitude must be below order one.

The weak window remains hard:

```text
T_res/tau_L >= {decision['weak_AJeff1_cGamma1_required_Tres_over_tauL']}
```

for the same assumptions.

## Nonclaim

The branch still cannot be claimed because `A_J,eff`, `c_Gamma`, and boundary routing are not parent-signed.
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
            "claim": "The parent-amplitude owner map reduces mu_Xi*T_res to Pi_B*T_res/tau_L and derives a c_Gamma ceiling law, but A_J coefficients, boundary amplitude and c_Gamma zero/smallness remain unsigned.",
            "current_evidence": "4198 amplitude decomposition, relaxation conversion table, cGamma ceiling rows, owner audit, decision row and nonclaim firewall.",
            "status": "private_amplitude_owner_partial_nonclaim_AJ_cGamma_boundary_unsigned",
            "next_test": "Derive A_src/A_lap/A_drift and boundary routing from the parent source operator, or demote the clean local branch to source-backed phenomenological closure.",
            "key_risk": "Converting mu_Xi to Pi_B/tau_L can make the strong branch look plausible, but it does not derive A_J or c_Gamma.",
        },
    )
    append_unique_line(
        SPINE_PATH,
        SPINE_MARKER,
        f"""

### PPC4161 Parent Amplitude Owner - 4198

Marker: `{SPINE_MARKER}`
Claim register row: `{CLAIM_ID}`

4198 reduces the relaxation product:

```text
mu_Xi T_res ~= Pi_B (T_res/tau_L).
```

For `A_J,eff=1` and `|c_Gamma|=1`:

```text
strong local requires T_res/tau_L >= {decision['strong_AJeff1_cGamma1_required_Tres_over_tauL']}
weak local requires   T_res/tau_L >= {decision['weak_AJeff1_cGamma1_required_Tres_over_tauL']}
```

The amplitude decomposition is:

```text
A_J,eff = A_src + A_lap + A_drift + A_boundary/U_B^2.
```

Verdict: relaxation side is less mysterious, but `A_J`, `c_Gamma`, and boundary routing remain parent-unsigned.
""",
    )
    append_unique_line(
        PACKET_180_PATH,
        PACKET_MARKER,
        f"""

## PPC4161 Packet Parent Amplitude Owner - 4198

Marker: `{PACKET_MARKER}`

Inside the private packet, `mu_Xi` is now read as the open memory relaxation rate:

```text
mu_Xi ~= Pi_B/tau_L.
```

The local `Gdot/G` pressure is therefore a requirement on `T_res/tau_L`, `A_J,eff`, and `c_Gamma`. The packet remains nonclaim because parent ownership of `A_src`, `A_lap`, `A_drift`, `A_boundary`, and finite/zero `c_Gamma` is still unsigned.
""",
    )


def all_rows() -> Dict[str, List[Dict[str, str]]]:
    conversions = relaxation_conversion_rows()
    ceilings = cgamma_ceiling_rows()
    decision = decision_rows(conversions, ceilings)
    return {
        "P8_Y5_R2FR_4198_SOURCE_REGISTER.csv": source_rows(),
        "P8_Y5_R2FR_4198_AMPLITUDE_DECOMPOSITION.csv": amplitude_decomposition_rows(),
        "P8_Y5_R2FR_4198_RELAXATION_CONVERSION.csv": conversions,
        "P8_Y5_R2FR_4198_CGAMMA_CEILING.csv": ceilings,
        "P8_Y5_R2FR_4198_OWNER_AUDIT.csv": owner_audit_rows(),
        "P8_Y5_R2FR_4198_DECISION.csv": decision,
        "P8_Y5_R2FR_4198_CLAIM_FIREWALL.csv": claim_firewall_rows(),
        "P8_Y5_R2FR_4198_NEXT_TARGET.csv": next_target_rows(),
        "P8_Y5_R2FR_4198_STATUS.csv": status_rows(decision[0]),
    }


def validate(rows_by_file: Dict[str, List[Dict[str, str]]]) -> List[Dict[str, str]]:
    source = rows_by_file["P8_Y5_R2FR_4198_SOURCE_REGISTER.csv"]
    decomp = rows_by_file["P8_Y5_R2FR_4198_AMPLITUDE_DECOMPOSITION.csv"]
    conversions = rows_by_file["P8_Y5_R2FR_4198_RELAXATION_CONVERSION.csv"]
    ceilings = rows_by_file["P8_Y5_R2FR_4198_CGAMMA_CEILING.csv"]
    decision = rows_by_file["P8_Y5_R2FR_4198_DECISION.csv"][0]
    firewall = rows_by_file["P8_Y5_R2FR_4198_CLAIM_FIREWALL.csv"]
    strong_req = float(decision["strong_AJeff1_cGamma1_required_Tres_over_tauL"])
    weak_req = float(decision["weak_AJeff1_cGamma1_required_Tres_over_tauL"])
    strong_cg = float(decision["strong_AJeff1_ratio1_max_abs_cGamma"])
    weak_cg = float(decision["weak_AJeff1_ratio1_max_abs_cGamma"])
    checks = [
        ("VAL4198_0_sources_exist", "all source paths exist", all(row["exists"] == "True" for row in source)),
        ("VAL4198_1_source_tokens", "all source required text markers found", all(row["required_text_found"] == "True" for row in source)),
        ("VAL4198_2_decomposition_total", "A_J effective decomposition row exists", any(row["amplitude_symbol"] == "A_J,eff" for row in decomp)),
        ("VAL4198_3_boundary_carried", "boundary enters as A_boundary/U_B^2", any("A_boundary/U_B^2" in row["amplitude_owner_law"] for row in decomp)),
        ("VAL4198_4_conversion_rows", "conversion rows include strong and weak AJ=1 cGamma=1", any(row["window"] == "strong_local" and row["effective_AJ"] == "1" and row["assumed_abs_cGamma"] == "1" for row in conversions) and any(row["window"] == "weaker_local" and row["effective_AJ"] == "1" and row["assumed_abs_cGamma"] == "1" for row in conversions)),
        ("VAL4198_5_strong_less_hard", "strong required relaxation ratio is far below weak", weak_req > strong_req * 1000),
        ("VAL4198_6_cgamma_ceiling_rows", "cGamma ceiling table has expected rows", len(ceilings) == 2 * len(AJEFF_VALUES) * len(RELAXATION_RATIO_VALUES)),
        ("VAL4198_7_cgamma_strong_larger", "strong cGamma ceiling exceeds weak for same assumptions", strong_cg > weak_cg * 1000),
        ("VAL4198_8_parent_unsigned", "decision keeps AJ, cGamma and boundary unsigned", decision["parent_AJ_coefficients_signed"] == "False" and decision["parent_cGamma_zero_or_small_signed"] == "False" and decision["boundary_routing_signed"] == "False"),
        (
            "VAL4198_9_no_claim_flags",
            "no 4198 row has claim_allowed or valid_for_claim true",
            all(
                row.get("claim_allowed", "False") == "False" and row.get("valid_for_claim", "False") == "False"
                for table in rows_by_file.values()
                for row in table
            ),
        ),
        ("VAL4198_10_firewall_rows", "firewall has four anti-claim rows", len(firewall) == 4),
        ("VAL4198_11_docs_written", "formal and checkpoint docs contain decision", DECISION in read_text(FORMAL_PATH) and DECISION in read_text(DOC_PATH)),
        ("VAL4198_12_claim_register", "claim register has L-039", CLAIM_ID in read_text(CLAIMS_PATH)),
        ("VAL4198_13_spine_marker", "spine marker appended", SPINE_MARKER in read_text(SPINE_PATH)),
        ("VAL4198_14_packet_marker", "packet marker appended", PACKET_MARKER in read_text(PACKET_180_PATH)),
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
    decision = rows_by_file["P8_Y5_R2FR_4198_DECISION.csv"][0]
    write_docs(decision)
    write_register_updates(decision)
    for filename, rows in rows_by_file.items():
        write_csv(SOURCE_DIR / filename, rows)
    validation = validate(rows_by_file)
    write_csv(SOURCE_DIR / "P8_Y5_BRR545_4198_VALIDATION.csv", validation)
    if not all(row["passed"] == "True" for row in validation):
        failed = [row for row in validation if row["passed"] != "True"]
        raise RuntimeError(f"4198 validation failed: {failed}")
    py_compile.compile(str(SCRIPT_PATH), doraise=True)
    pycache = SCRIPT_PATH.parent / "__pycache__"
    if pycache.exists():
        shutil.rmtree(pycache)


def main() -> None:
    write_all()
    print(DECISION)
    print(f"formal={FORMAL_PATH}")
    print(f"checkpoint={DOC_PATH}")
    print(f"validation={SOURCE_DIR / 'P8_Y5_BRR545_4198_VALIDATION.csv'}")
    print("rows=15 validation checks")


if __name__ == "__main__":
    main()

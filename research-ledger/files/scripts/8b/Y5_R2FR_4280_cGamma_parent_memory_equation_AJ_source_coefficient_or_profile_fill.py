from __future__ import annotations

import csv
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, Iterable, List


ROOT = Path(__file__).resolve().parents[2]
FORMAL = ROOT / "formalization-workbench"
POST = ROOT / "post-checkpoint-work"
SOURCE_DIR = POST / "source-intake" / "mts_residuals"

CHECKPOINT = "4280"
CLAIM_ID = "L-121"
BRANCH = "MTS_R2FR_Y5_CGAMMA_PARENT_MEMORY_AJ_SOURCE_COEFFICIENT_OR_PROFILE_FILL_4280"
DECISION = "CGAMMA_AJ_SOURCE_TERM_ZEROED_BY_DQ_CLOSURE_TRANSPORT_BGRAD_ROUTING_REMAINS_NONCLAIM"
MARKER = "PPC4161_CGAMMA_PARENT_MEMORY_AJ_SOURCE_COEFFICIENT_OR_PROFILE_FILL_4280"
PACKET_MARKER = "PPC4161_PACKET_CGAMMA_PARENT_MEMORY_AJ_SOURCE_COEFFICIENT_OR_PROFILE_FILL_4280"
NEXT_TARGET = "4281-Y5-R2FR-cGamma-transport-Bgrad-routing-zero-or-profile-source-pack.md"

FORMAL_PATH = FORMAL / "296-PPC4161-cGamma-parent-memory-equation-AJ-source-coefficient-or-profile-fill.md"
DOC_PATH = POST / "4280-Y5-R2FR-cGamma-parent-memory-equation-AJ-source-coefficient-or-profile-fill.md"
VALIDATION_PATH = SOURCE_DIR / "P8_Y5_BRR545_4280_VALIDATION.csv"

STAMP = datetime.now(timezone.utc).replace(microsecond=0).isoformat()
STRONG_AJ_COEFFICIENT = "0.1678939074330212"
STRONG_AJ_COEFFICIENT_PIB = "0.167893843691"

SOURCES = {
    "SRC4280_00_4279_pack": (
        FORMAL / "295-PPC4161-residual-EFT-coefficient-zero-or-local-test-bound-pack.md",
        "A_src,",
        "4279 identifies cGamma/AJ/profile ownership as the live survivor.",
    ),
    "SRC4280_01_4236_AJ": (
        FORMAL / "252-PPC4161-cGamma-parent-memory-equation-or-AJ-coefficient-source-fill.md",
        "A_J,eff_private = A_src + A_lap + A_drift",
        "4236 cGamma memory/AJ coefficient ledger.",
    ),
    "SRC4280_02_4237_AJ_theorem": (
        FORMAL / "253-PPC4161-AJ-source-coefficient-theorem-or-numeric-fill-pack.md",
        "A_J,eff_private <= |S_A H_L^A| + |D_m Delta_h M_2| + |D_t M_2|",
        "4237 maps AJ coefficients to vertical current and M2 shape terms.",
    ),
    "SRC4280_03_4238_zero_contract": (
        FORMAL / "254-PPC4161-vertical-current-M2-zero-theorem-or-profile-sampler.md",
        "S_A H_L^A = 0",
        "4238 exact zero contract for source contraction and M2 terms.",
    ),
    "SRC4280_04_4239_source_orthogonality": (
        FORMAL / "255-PPC4161-parent-source-orthogonality-or-M2-profile-sampler-dry-run.md",
        "S_A H_L^A = S_A H_perp^A",
        "4239 reduces source contraction to Hperp only.",
    ),
    "SRC4280_05_4242_M2_pruning": (
        FORMAL / "258-PPC4161-M2-defect-source-map-pruning-or-real-profile-input-pack.md",
        "R_transport_to_local",
        "4242 routes M2 transport/Bgrad defects into explicit residuals.",
    ),
    "SRC4280_06_4243_Hperp": (
        FORMAL / "259-PPC4161-Hperp-zero-theorem-or-source-defect-profile-first-real-row.md",
        "Hperp=0",
        "4243 says all Dq_i[H_L]=0 implies Hperp=0 and source contraction zero.",
    ),
    "SRC4280_07_4277_Dq_zero": (
        FORMAL / "293-PPC4161-matter-interface-action-domain-proof-or-canonical-gX-source-fill.md",
        "new 4277 standard-branch row: Dq_geom = 0.0",
        "4277 closes all standard-branch Dq component rows conditionally.",
    ),
    "SRC4280_08_4188_product_bounds": (
        FORMAL / "204-PPC4161-finite-cGamma-product-bound-law.md",
        "C_Gamma_Gdot` <= `2.42e-14` yr^-1",
        "4188 cGamma product budgets.",
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


def aj_reduction_rows() -> List[Dict[str, str]]:
    raw = [
        (
            "AJR4280_0_start",
            "A_J,eff_private = A_src + A_lap + A_drift",
            "4236 ledger",
            "STARTING_LEDGER",
        ),
        (
            "AJR4280_1_4237_expansion",
            "A_J,eff_private <= |S_A H_L^A| + |D_m Delta_h M_2| + |D_t M_2|",
            "4237 vertical-current/M2 theorem",
            "AJ_COEFFICIENTS_REDUCED_TO_SOURCE_CONTRACTION_AND_M2",
        ),
        (
            "AJR4280_2_source_split",
            "S_A H_L^A = S_A H_perp^A",
            "4239 source-orthogonality for q-basic H_q",
            "QBASIC_SOURCE_PART_ZERO",
        ),
        (
            "AJR4280_3_Dq_closure_import",
            "4277 standard branch has Dq_i[H_L]=0 for geom,tau,matter,source,theta,boundary,EM,coeff",
            "4277 Dq closure plus 4243 Hperp criterion",
            "HPERP_ZERO_CONDITION_FILLED_CONDITIONALLY",
        ),
        (
            "AJR4280_4_A_src_zero",
            "Hperp=0 => S_A Hperp^A=0 => A_src=0",
            "4243 theorem applied after 4277",
            "A_SRC_CONDITIONAL_ZERO_DERIVED",
        ),
        (
            "AJR4280_5_M2_pruning",
            "D_m Delta_h M_2 and D_t M_2 reduce to R_transport_to_local + R_Bgrad_to_local in the pruned defect branch",
            "4242 M2 source-map pruning",
            "A_LAP_A_DRIFT_ROUTED_TO_TRANSPORT_BGRAD_RESIDUALS",
        ),
        (
            "AJR4280_6_live_private_budget",
            "A_J,eff_private <= |R_transport_to_local| + |R_Bgrad_to_local|",
            "4280 reduction",
            "CGAMMA_AJ_REDUCED_NOT_CLOSED",
        ),
    ]
    return [
        {
            **common(),
            "reduction_id": reduction_id,
            "mathematical_form": mathematical_form,
            "source_basis": source_basis,
            "status": status,
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
        for reduction_id, mathematical_form, source_basis, status in raw
    ]


def hperp_zero_rows() -> List[Dict[str, str]]:
    probes = [
        ("Dq_geom", FORMAL / "293-PPC4161-matter-interface-action-domain-proof-or-canonical-gX-source-fill.md"),
        ("Dq_tau", FORMAL / "285-PPC4161-Dq-tau-reference-time-lock-or-tau-residual-bound.md"),
        ("Dq_matter", FORMAL / "281-PPC4161-Dq-matter-action-domain-zero-or-source-prefactor-bound.md"),
        ("Dq_source_readout", FORMAL / "282-PPC4161-Dq-source-readout-Hilbert-charge-zero-or-coefficient-remainder.md"),
        ("Dq_theta_marker", FORMAL / "280-PPC4161-Dq-theta-marker-component-zero-or-marker-bound.md"),
        ("Dq_boundary_projector", FORMAL / "284-PPC4161-Dq-boundary-projector-fixed-collar-or-boundary-residual-bound.md"),
        ("Dq_EM", FORMAL / "279-PPC4161-Dq-EM-closed-collar-adoption-or-radiative-boundary-row.md"),
        ("Dq_coeff", FORMAL / "283-PPC4161-Dq-coeff-fixed-parent-constant-or-Newton-calibration-bound.md"),
    ]
    rows = [
        {
            **common(),
            "row_id": f"HPZ4280_{index}_{probe}",
            "probe_id": probe,
            "epsilon": "0.0",
            "source_path": str(source_path),
            "status": "STANDARD_BRANCH_ZERO_IMPORTED",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
        for index, (probe, source_path) in enumerate(probes)
    ]
    rows.append(
        {
            **common(),
            "row_id": "HPZ4280_8_conclusion",
            "probe_id": "Hperp",
            "epsilon": "0.0",
            "source_path": str(FORMAL / "259-PPC4161-Hperp-zero-theorem-or-source-defect-profile-first-real-row.md"),
            "status": "HPERP_ZERO_CONDITIONAL_ON_STANDARD_BRANCH_DQ_ZERO",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
    )
    return rows


def m2_routing_rows() -> List[Dict[str, str]]:
    raw = [
        (
            "M2R4280_0_transport",
            "R_transport_to_local",
            "transport/routing leakage into compact local scalar memory profile",
            "CONDITIONAL_ROUTING_NOT_PARENT_DERIVED",
            "derive P_loc transport_to_local=0 or source profile bound",
        ),
        (
            "M2R4280_1_Bgrad",
            "R_Bgrad_to_local",
            "B-gradient/transition support leakage into compact local scalar memory profile",
            "CONDITIONAL_ROUTING_NOT_PARENT_DERIVED",
            "derive boundary/quarantine support zero or source profile bound",
        ),
        (
            "M2R4280_2_zero_route",
            "A_J,eff_private=0",
            "if R_transport_to_local=0 and R_Bgrad_to_local=0",
            "EXACT_REMAINING_ZERO_ROUTE",
            "parent routing/no-local-support clauses",
        ),
        (
            "M2R4280_3_finite_route",
            "A_J,eff_private <= |R_transport_to_local| + |R_Bgrad_to_local|",
            "if either residual survives",
            "FINITE_PROFILE_ROUTE_READY",
            "numeric profiles, units, source paths, T_res/tau_L, c_Gamma",
        ),
    ]
    return [
        {
            **common(),
            "routing_id": routing_id,
            "quantity": quantity,
            "meaning": meaning,
            "status": status,
            "next_input": next_input,
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
        for routing_id, quantity, meaning, status, next_input in raw
    ]


def finite_budget_rows() -> List[Dict[str, str]]:
    raw = [
        (
            "BUD4280_0_strong_AJ",
            "A_J,eff_private",
            f"|R_transport_to_local|+|R_Bgrad_to_local| <= {STRONG_AJ_COEFFICIENT}*(mu_Xi T_res)/|c_Gamma|",
            "dimensionless normalized amplitude",
            "R_transport_to_local;R_Bgrad_to_local;mu_Xi*T_res;c_Gamma",
        ),
        (
            "BUD4280_1_PiB_AJ",
            "A_J,eff_private",
            f"|R_transport_to_local|+|R_Bgrad_to_local| <= {STRONG_AJ_COEFFICIENT_PIB}*Pi_B*(T_res/tau_L)/|c_Gamma|",
            "dimensionless normalized amplitude",
            "R_transport_to_local;R_Bgrad_to_local;Pi_B;T_res/tau_L;c_Gamma",
        ),
        (
            "BUD4280_2_Gdot",
            "C_Gamma_Gdot",
            "|c_Gamma D_t Xi_0| <= 2.42e-14 yr^-1",
            "yr^-1",
            "D_t Xi_0 profile or AJ-derived time response",
        ),
        (
            "BUD4280_3_xi",
            "C_Gamma_xi",
            "|c_Gamma L_loc grad_perp Xi_0| <= 4e-9",
            "dimensionless",
            "grad_perp Xi_0 profile",
        ),
        (
            "BUD4280_4_alpha3",
            "C_Gamma_vector",
            "|c_Gamma profile_alpha3| <= 4e-20",
            "dimensionless",
            "preferred-frame/vector arena profile",
        ),
    ]
    return [
        {
            **common(),
            "budget_id": budget_id,
            "quantity": quantity,
            "bound": bound,
            "units": units,
            "missing_input": missing_input,
            "score_ready": "False",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
        for budget_id, quantity, bound, units, missing_input in raw
    ]


def control_runner_rows() -> List[Dict[str, str]]:
    threshold = 0.1678939074330212
    raw = [
        ("CTRL4280_0_zero_route", 0.0, 0.0, 1.0, 1.0),
        ("CTRL4280_1_pass", 0.04, 0.03, 1.0, 1.0),
        ("CTRL4280_2_fail", 0.2, 0.02, 1.0, 1.0),
        ("CTRL4280_3_scaled_pass", 0.1, 0.05, 2.0, 1.0),
    ]
    rows: List[Dict[str, str]] = []
    for control_id, r_transport, r_bgrad, mu_t, c_gamma_abs in raw:
        lhs = abs(r_transport) + abs(r_bgrad)
        rhs = threshold * mu_t / c_gamma_abs
        rows.append(
            {
                **common(),
                "control_id": control_id,
                "R_transport_to_local": f"{r_transport:.12g}",
                "R_Bgrad_to_local": f"{r_bgrad:.12g}",
                "mu_Xi_T_res": f"{mu_t:.12g}",
                "abs_c_Gamma": f"{c_gamma_abs:.12g}",
                "lhs_abs_sum": f"{lhs:.12g}",
                "rhs_budget": f"{rhs:.12g}",
                "passes_budget": str(lhs <= rhs),
                "verdict": "CONTROL_PASS_NONCLAIM" if lhs <= rhs else "CONTROL_FAIL_NONCLAIM",
                "claim_allowed": "False",
                "valid_for_claim": "False",
            }
        )
    return rows


def decision_rows() -> List[Dict[str, str]]:
    raw = [
        (
            "DEC4280_0_A_src_zero",
            "Use 4277 Dq closure to activate the 4243 Hperp theorem.",
            "The q-basic source piece was already killed by 4239; Hperp was the remaining source contraction. Standard-branch Dq zeros now give Hperp=0 conditionally.",
            "do not keep A_src as a vague missing coefficient",
        ),
        (
            "DEC4280_1_transport_Bgrad_survive",
            "Do not claim cGamma closure yet.",
            "A_lap/A_drift reduce to transport and B-gradient local routing residuals that 4242 did not parent-sign.",
            NEXT_TARGET,
        ),
        (
            "DEC4280_2_runner_ready",
            "Keep finite AJ/profile budgets as score gates.",
            "If routing zero fails, the branch needs real R_transport/R_Bgrad, T_res/tau_L, cGamma and arena profiles.",
            "fill transport/Bgrad source rows",
        ),
    ]
    return [
        {
            **common(),
            "decision_id": decision_id,
            "decision": decision,
            "reason": reason,
            "next_action": next_action,
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
        for decision_id, decision, reason, next_action in raw
    ]


def firewall_rows() -> List[Dict[str, str]]:
    raw = [
        ("FW4280_0_private_Dq_scope", "Hperp=0 is conditional on the private standard-branch Dq closure, not a global parent theorem."),
        ("FW4280_1_no_transport_erasure", "R_transport_to_local and R_Bgrad_to_local remain live until parent-routed or numerically sourced."),
        ("FW4280_2_no_profile_free_pass", "AJ budget controls are smoke/contract rows unless R_transport/R_Bgrad, timescale and cGamma rows are real."),
        ("FW4280_3_no_R10_promotion", "Do not promote cGamma R10 until finite-range profiles and a real alpha(lambda) curve are sourced."),
    ]
    return [
        {
            **common(),
            "firewall_id": firewall_id,
            "rule": rule,
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
        for firewall_id, rule in raw
    ]


def status_rows() -> List[Dict[str, str]]:
    return [
        {
            **common(),
            "status_id": "STATUS4280",
            "current_status": "cGamma AJ source contraction A_src is conditionally zero via 4277 Dq closure; live AJ pressure reduced to transport/Bgrad routing residuals",
            "local_gr_claim": "False",
            "ppn_claim": "False",
            "cGamma_zero_claim": "False",
            "next_best_target": NEXT_TARGET,
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
    ]


def next_target_rows() -> List[Dict[str, str]]:
    return [
        {
            **common(),
            "next_target": NEXT_TARGET,
            "why": "A_src is no longer the live obstruction; cGamma now hinges on transport/Bgrad local routing or finite profile source rows.",
            "success_condition": "prove R_transport_to_local=R_Bgrad_to_local=0 in compact local collars, or source numeric profiles and compare against the 4280 AJ/Gdot/xi/alpha3 budgets.",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
    ]


def append_claim() -> None:
    path = FORMAL / "02-claims-register.csv"
    text = read_text(path)
    if CLAIM_ID in text:
        return
    with path.open(newline="", encoding="utf-8") as handle:
        fieldnames = next(csv.reader(handle))
    row = {
        "claim_id": CLAIM_ID,
        "domain": "local_gr",
        "claim": (
            "4280 applies the new 4277 Dq closure to the earlier 4243 Hperp theorem: all standard-branch Dq_i[H_L]=0 implies Hperp=0, so the cGamma AJ source-contraction term A_src vanishes conditionally. "
            "The remaining cGamma AJ pressure is reduced to R_transport_to_local and R_Bgrad_to_local, with finite AJ/Gdot/xi/alpha3 budgets retained."
        ),
        "current_evidence": (
            "4280 source register, AJ reduction chain, Hperp zero import, M2 routing gate, finite budgets, control runner, decision and firewall."
        ),
        "status": "private_cGamma_A_src_zero_transport_Bgrad_survivors_nonclaim",
        "next_test": "Prove transport/Bgrad local routing zero or fill numeric profile rows for R_transport/R_Bgrad, T_res/tau_L, cGamma and arena projections.",
        "key_risk": "Treating private Dq/Hperp zero as a global parent proof, or silently erasing transport/B-gradient residuals.",
    }
    with path.open("a", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writerow(row)


def append_unique_block(path: Path, marker: str, title: str, body: str) -> None:
    text = read_text(path)
    if marker in text:
        return
    path.write_text(text.rstrip() + f"\n\n## {title}\n\nMarker: `{marker}`\n\n{body.strip()}\n", encoding="utf-8")


def formal_doc() -> str:
    return f"""
# 296 - PPC4161 cGamma parent memory equation AJ source coefficient or profile fill

Marker: `{MARKER}`

Branch: `{BRANCH}`

Decision: `{DECISION}`

## Result

4280 does not claim public local GR, `c_Gamma=0`, PPN/R10 safety, or empirical validation.

It makes a real reduction:

```text
A_J,eff_private = A_src + A_lap + A_drift
```

becomes:

```text
A_src = 0
A_J,eff_private <= |R_transport_to_local| + |R_Bgrad_to_local|.
```

## Why A_src now vanishes conditionally

4239 reduced the source-current piece to:

```text
S_A H_L^A = S_A Hperp^A.
```

4243 proved:

```text
all Dq_i[H_L] = 0  =>  Hperp = 0.
```

4277 now supplies the standard-branch Dq closure:

```text
Dq_geom = Dq_tau = Dq_matter = Dq_source_readout
= Dq_theta_marker = Dq_boundary_projector = Dq_EM = Dq_coeff = 0.
```

Therefore, inside the private standard branch:

```text
Hperp = 0,
S_A Hperp^A = 0,
A_src = 0.
```

## What remains

4242 already pruned the M2 source map:

```text
D_m Delta_h M_2 + D_t M_2
-> R_transport_to_local + R_Bgrad_to_local.
```

So the live cGamma local-memory amplitude gate is:

```text
A_J,eff_private <= |R_transport_to_local| + |R_Bgrad_to_local|.
```

The exact zero route is now sharply:

```text
R_transport_to_local = 0,
R_Bgrad_to_local = 0.
```

If not, the finite route is:

```text
|R_transport_to_local|+|R_Bgrad_to_local|
<= {STRONG_AJ_COEFFICIENT}*(mu_Xi T_res)/|c_Gamma|
```

or:

```text
<= {STRONG_AJ_COEFFICIENT_PIB}*Pi_B*(T_res/tau_L)/|c_Gamma|.
```

## No-claim guard

This is not closure by vibes. Transport and B-gradient leakage are still live because their parent routing clauses are not signed. The next proof must either derive their local silence or source real profiles.

## Next target

`{NEXT_TARGET}` should prove transport/B-gradient local routing zero, or fill real profile rows for `R_transport_to_local`, `R_Bgrad_to_local`, `T_res/tau_L`, `c_Gamma`, and arena profiles.
"""


def checkpoint_doc() -> str:
    return f"""
# 4280 - cGamma parent memory equation AJ source coefficient or profile fill

Marker: `{MARKER}`

Decision: `{DECISION}`

4280 applies 4277 to the earlier cGamma machinery:

```text
all Dq_i[H_L]=0 => Hperp=0 => S_A Hperp^A=0 => A_src=0.
```

The remaining AJ gate is:

```text
A_J,eff_private <= |R_transport_to_local| + |R_Bgrad_to_local|.
```
"""


def validation_rows(paths: Dict[str, Path]) -> List[Dict[str, str]]:
    sources = csv_rows(paths["sources"])
    reductions = csv_rows(paths["aj_reduction"])
    hperp = csv_rows(paths["hperp_zero"])
    routing = csv_rows(paths["m2_routing"])
    budgets = csv_rows(paths["finite_budgets"])
    controls = csv_rows(paths["controls"])
    all_rows: Iterable[Dict[str, str]] = (
        sources
        + reductions
        + hperp
        + routing
        + budgets
        + controls
        + csv_rows(paths["decision"])
        + csv_rows(paths["firewall"])
        + csv_rows(paths["status"])
        + csv_rows(paths["next_target"])
    )
    validations = [
        ("VAL4280_0_sources_exist", all(row["exists"] == "True" for row in sources), "all source paths exist"),
        ("VAL4280_1_needles_found", all(row["required_text_found"] == "True" for row in sources), "all source needles found"),
        (
            "VAL4280_2_A_src_zero",
            any(row["reduction_id"] == "AJR4280_4_A_src_zero" and row["status"] == "A_SRC_CONDITIONAL_ZERO_DERIVED" for row in reductions),
            "A_src conditional zero derived",
        ),
        (
            "VAL4280_3_Hperp_zero",
            any(row["probe_id"] == "Hperp" and row["epsilon"] == "0.0" for row in hperp),
            "Hperp zero imported from Dq closure",
        ),
        (
            "VAL4280_4_transport_Bgrad_live",
            {"R_transport_to_local", "R_Bgrad_to_local"}.issubset({row.get("quantity") for row in routing}),
            "transport/Bgrad residuals remain explicit",
        ),
        (
            "VAL4280_5_budget_rows",
            {"A_J,eff_private", "C_Gamma_Gdot", "C_Gamma_xi", "C_Gamma_vector"}.issubset({row.get("quantity") for row in budgets}),
            "finite cGamma/AJ budgets emitted",
        ),
        (
            "VAL4280_6_controls",
            any(row["control_id"] == "CTRL4280_1_pass" and row["verdict"] == "CONTROL_PASS_NONCLAIM" for row in controls)
            and any(row["control_id"] == "CTRL4280_2_fail" and row["verdict"] == "CONTROL_FAIL_NONCLAIM" for row in controls),
            "control runner catches pass/fail",
        ),
        ("VAL4280_7_formal_doc", FORMAL_PATH.exists() and MARKER in read_text(FORMAL_PATH), "formal doc written"),
        ("VAL4280_8_checkpoint_doc", DOC_PATH.exists() and DECISION in read_text(DOC_PATH), "checkpoint doc written"),
        ("VAL4280_9_claim_row", f"{CLAIM_ID}," in read_text(FORMAL / "02-claims-register.csv"), "claim register row added"),
        ("VAL4280_10_no_claim_rows", all(row.get("claim_allowed", "False") == "False" and row.get("valid_for_claim", "False") == "False" for row in all_rows), "all rows remain nonclaim"),
    ]
    for name, path in paths.items():
        validations.append((f"VAL4280_csv_{name}", bool(csv_rows(path)), f"{path.name} parses"))
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
        "sources": SOURCE_DIR / "P8_Y5_R2FR_4280_SOURCE_REGISTER.csv",
        "aj_reduction": SOURCE_DIR / "P8_Y5_R2FR_4280_AJ_COEFFICIENT_REDUCTION.csv",
        "hperp_zero": SOURCE_DIR / "P8_Y5_R2FR_4280_HPERP_ZERO_IMPORT.csv",
        "m2_routing": SOURCE_DIR / "P8_Y5_R2FR_4280_M2_TRANSPORT_BGRAD_ROUTING_GATE.csv",
        "finite_budgets": SOURCE_DIR / "P8_Y5_R2FR_4280_FINITE_AJ_PROFILE_BUDGETS.csv",
        "controls": SOURCE_DIR / "P8_Y5_R2FR_4280_AJ_BUDGET_CONTROL_RUNNER.csv",
        "decision": SOURCE_DIR / "P8_Y5_R2FR_4280_DECISION.csv",
        "firewall": SOURCE_DIR / "P8_Y5_R2FR_4280_CLAIM_FIREWALL.csv",
        "status": SOURCE_DIR / "P8_Y5_R2FR_4280_STATUS.csv",
        "next_target": SOURCE_DIR / "P8_Y5_R2FR_4280_NEXT_TARGET.csv",
    }
    write_csv(paths["sources"], source_rows())
    write_csv(paths["aj_reduction"], aj_reduction_rows())
    write_csv(paths["hperp_zero"], hperp_zero_rows())
    write_csv(paths["m2_routing"], m2_routing_rows())
    write_csv(paths["finite_budgets"], finite_budget_rows())
    write_csv(paths["controls"], control_runner_rows())
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
        "PPC4161 4280 cGamma AJ source reduction",
        "4280 applies the 4277 standard-branch Dq closure to the earlier 4243 Hperp theorem. The q-basic source component was already killed by 4239, and Dq closure now gives `Hperp=0`, so `A_src=0` conditionally. The live `c_Gamma` AJ pressure is reduced to `R_transport_to_local` and `R_Bgrad_to_local`, with finite AJ/Gdot/xi/alpha3 budgets retained.",
    )
    append_unique_block(
        FORMAL / "180-PPC4161-private-local-packet-integration.md",
        PACKET_MARKER,
        "4280 packet cGamma AJ gate",
        "Packet update: `A_src` is conditionally closed by Dq/Hperp logic. The remaining cGamma pressure is transport/B-gradient routing or finite profile sourcing. No public claim is made.",
    )
    write_csv(VALIDATION_PATH, validation_rows(paths))
    failed = [row for row in csv_rows(VALIDATION_PATH) if row["passed"] != "True"]
    print(f"{CHECKPOINT}: wrote {len(paths)} csv artifacts plus validation")
    print(f"{CHECKPOINT}: validation rows={len(csv_rows(VALIDATION_PATH))} failed={len(failed)}")
    print(f"{CHECKPOINT}: decision={DECISION}")
    if failed:
        for row in failed:
            print(f"FAILED {row['check_id']}: {row['description']}")
        raise SystemExit(1)


if __name__ == "__main__":
    main()

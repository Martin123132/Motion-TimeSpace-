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

CHECKPOINT = "4235"
CLAIM_ID = "L-076"
BRANCH = "MTS_R2FR_Y5_CGAMMA_FULL_BUDGET_4235"
DECISION = "CGAMMA_FULL_BUDGET_PROFILE_RUNNER_BUILT_TENSOR_NOHAIR_PRIVATE_CLOSED_GAMMAMEM_SUPPORT_AND_AJ_OWNER_STILL_OPEN"
MARKER = "PPC4161_CGAMMA_FULL_BUDGET_PROFILE_RUNNER_4235"
PACKET_MARKER = "PPC4161_PACKET_CGAMMA_FULL_BUDGET_PROFILE_RUNNER_4235"
NEXT_TARGET = "4236-Y5-R2FR-cGamma-parent-memory-equation-or-AJ-coefficient-source-fill.md"

FORMAL_PATH = FORMAL / "251-PPC4161-cGamma-support-nohair-or-full-budget-profile-bound-runner.md"
DOC_PATH = POST / "4235-Y5-R2FR-cGamma-support-nohair-or-full-budget-profile-bound-runner.md"
VALIDATION_PATH = SOURCE_DIR / "P8_Y5_BRR545_4235_VALIDATION.csv"
BOUND_TABLE = SOURCE_DIR / "P8_Y5_R2FR_4173_SOURCE_BACKED_BOUND_TABLE.csv"


@dataclass(frozen=True)
class SourceSpec:
    source_id: str
    path: Path
    required_text: str
    role: str


STAMP = datetime.now(timezone.utc).replace(microsecond=0).isoformat()


SOURCE_SPECS: Dict[str, SourceSpec] = {
    "SRC4235_00_4234_next": SourceSpec(
        "SRC4235_00_4234_next",
        SOURCE_DIR / "P8_Y5_R2FR_4234_NEXT_TARGET.csv",
        "4235-Y5-R2FR-cGamma-support-nohair-or-full-budget-profile-bound-runner.md",
        "4234 selected cGamma support/nohair as the sole private survivor.",
    ),
    "SRC4235_01_4234_decision": SourceSpec(
        "SRC4235_01_4234_decision",
        SOURCE_DIR / "P8_Y5_R2FR_4234_DECISION.csv",
        "shared_budget_private_collapsed_to_cGamma_only",
        "4234 collapses private two-survivor budget to cGamma only.",
    ),
    "SRC4235_02_support_contract": SourceSpec(
        "SRC4235_02_support_contract",
        FORMAL / "203-PPC4161-local-memory-support-projector-zero-law-for-cGamma.md",
        "If all five are parent-owned, `c_Gamma=0` in compact local tests.",
        "Original cGamma support/no-hair zero contract.",
    ),
    "SRC4235_03_product_law": SourceSpec(
        "SRC4235_03_product_law",
        FORMAL / "204-PPC4161-finite-cGamma-product-bound-law.md",
        "|C_Gamma,a| <= B_a.",
        "cGamma product-bound law.",
    ),
    "SRC4235_04_profile_split": SourceSpec(
        "SRC4235_04_profile_split",
        FORMAL / "205-PPC4161-cGamma-profile-projection-coefficient-gate.md",
        "C_Gamma_Gdot = c_Gamma D_t Xi_0",
        "cGamma projection split.",
    ),
    "SRC4235_05_stationarity": SourceSpec(
        "SRC4235_05_stationarity",
        FORMAL / "206-PPC4161-local-memory-stationarity-gradient-zero-gate.md",
        "|D_t Xi_0| <= 2.42e-14 / |c_Gamma|",
        "Full-budget Gdot and gradient profile bounds.",
    ),
    "SRC4235_06_fixed_point": SourceSpec(
        "SRC4235_06_fixed_point",
        FORMAL / "207-PPC4161-memory-fixed-point-equation-and-smooth-minimizer-contract.md",
        "finite_profile_bounds_remain_active = true",
        "Fixed-point/minimizer theorem shape remains unsigned.",
    ),
    "SRC4235_07_hessian": SourceSpec(
        "SRC4235_07_hessian",
        FORMAL / "208-PPC4161-parent-Xi-Hessian-signs-and-boundary-domain.md",
        "J_res = [1 - Pi_B] S_cg",
        "Open-system Xi Hessian and residual source map.",
    ),
    "SRC4235_08_projector": SourceSpec(
        "SRC4235_08_projector",
        FORMAL / "209-PPC4161-residual-source-projector-and-Xi-profile-amplitude-bound.md",
        "P_loc J_res = 0",
        "Residual-source projector zero target.",
    ),
    "SRC4235_09_support_powers": SourceSpec(
        "SRC4235_09_support_powers",
        FORMAL / "210-PPC4161-source-support-powers-for-Jres.md",
        "J_res = O(U_B^2).",
        "Jres support powers.",
    ),
    "SRC4235_10_profile_smoke": SourceSpec(
        "SRC4235_10_profile_smoke",
        FORMAL / "213-PPC4161-normalized-Jres-profile-smoke.md",
        "strong local Gdot needs",
        "Numeric pressure from 4197 assumption-grid smoke.",
    ),
    "SRC4235_11_amplitude_owner": SourceSpec(
        "SRC4235_11_amplitude_owner",
        FORMAL / "214-PPC4161-parent-amplitude-owner-for-Jres.md",
        "strong local max |c_Gamma| = 0.167893843691",
        "cGamma ceiling and AJ owner map.",
    ),
    "SRC4235_12_source_operator": SourceSpec(
        "SRC4235_12_source_operator",
        FORMAL / "215-PPC4161-source-operator-amplitude-AJ-bound.md",
        "K_perp=0 or PPN-bounded.",
        "Old source-operator blocker now improved by 4234.",
    ),
    "SRC4235_13_Kperp_identity": SourceSpec(
        "SRC4235_13_Kperp_identity",
        FORMAL / "250-PPC4161-Kperp-EH-coframe-identity-proof-or-independent-tensor-source-row.md",
        "R_i^K = |W_i^K| N_T/D_T = 0",
        "Kperp private identity removes half-budget split.",
    ),
    "SRC4235_14_bounds": SourceSpec(
        "SRC4235_14_bounds",
        BOUND_TABLE,
        "Gdot_over_G",
        "Source-backed local bound table.",
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
    for source_spec in SOURCE_SPECS.values():
        text = read_text(source_spec.path)
        rows.append(
            {
                **common(),
                "source_id": source_spec.source_id,
                "path": str(source_spec.path),
                "exists": str(source_spec.path.exists()),
                "required_text": source_spec.required_text,
                "required_text_found": str(source_spec.required_text in text),
                "role": source_spec.role,
                "claim_allowed": "False",
                "valid_for_claim": "False",
            }
        )
    return rows


def support_clause_rows() -> List[Dict[str, str]]:
    rows = [
        ("CGZ4235_0_vertical_readout", "Gamma_mem is vertical/readout-only or q-horizontal projection vanishes", "open", "P_loc Gamma_mem source/profile not parent-derived"),
        ("CGZ4235_1_compact_support", "P_loc Gamma_mem=0 in compact local collar or constant part absorbed into calibrated coefficients", "open", "support silence is not parent-owned"),
        ("CGZ4235_2_source_silence", "ordinary bulk source variation of Gamma_mem vanishes or is Hilbert-source absorbed", "open", "J_res/P_loc source projector not zero"),
        ("CGZ4235_3_boundary_flux", "memory flux is Hamiltonian boundary-routed rather than hidden bulk force", "private_pass", "compact no-flux routing available; open/global flux rows retained"),
        ("CGZ4235_4_tensor_nohair", "no homogeneous tensor memory mode survives local projection", "private_pass", "closed privately by 4234 Kperp EH-coframe identity"),
    ]
    return [
        {
            **common(),
            "clause_id": clause_id,
            "support_nohair_clause": clause,
            "private_status_after_4235": status,
            "reason": reason,
            "zero_claim": "False",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
        for clause_id, clause, status, reason in rows
    ]


def full_budget_rows() -> List[Dict[str, str]]:
    wanted = {
        "gamma_minus_1": "C_Gamma_gamma_beta",
        "beta_minus_1": "C_Gamma_gamma_beta",
        "xi": "C_Gamma_xi",
        "alpha1": "C_Gamma_vector",
        "alpha2": "C_Gamma_vector",
        "alpha3": "C_Gamma_vector_or_conservation",
        "zeta3": "C_Gamma_stress",
        "Gdot_over_G": "C_Gamma_Gdot",
        "alpha_Yukawa_at_lambda_38p6um": "C_Gamma_R10",
        "eta_TiPt": "C_Gamma_WEP",
        "redshift_violation_alpha": "C_Gamma_clock",
        "((2+2gamma-beta)/3)-1": "C_Gamma_orbital_combo",
    }
    rows: List[Dict[str, str]] = []
    for bound_row in csv_rows(BOUND_TABLE):
        observable = bound_row["observable"]
        if observable not in wanted:
            continue
        claim_grade = "False" if observable == "alpha_Yukawa_at_lambda_38p6um" else bound_row["source_backed"]
        rows.append(
            {
                **common(),
                "profile_bound_id": f"CGFB4235_{bound_row['bound_id']}",
                "observable": observable,
                "channel": wanted[observable],
                "full_budget": bound_row["allowed_abs_bound"],
                "units": bound_row["units"],
                "half_budget_removed_by_4234": "True",
                "bound_formula": f"|c_Gamma profile_{observable}| <= {bound_row['allowed_abs_bound']} {bound_row['units']}",
                "source_id": bound_row["source_id"],
                "full_curve_available": bound_row["full_curve_available"],
                "scoreable_now": "False",
                "missing_input": "c_Gamma and profile/Jacobian for this arena, or support/nohair zero theorem",
                "claim_grade_bound": claim_grade,
                "claim_allowed": "False",
                "valid_for_claim": "False",
            }
        )
    return rows


def amplitude_status_rows() -> List[Dict[str, str]]:
    rows = [
        ("AJS4235_0_Kperp", "Kperp blocker in 4199", "private_closed", "4234 gives Kperp_private_static_force_zero=true"),
        ("AJS4235_1_boundary", "boundary_in/A_boundary", "private_no_flux_pass_open_global", "compact no-flux collar routes boundary; open/global memory flux remains retained"),
        ("AJS4235_2_source_coefficients", "A_src, A_lap, A_drift", "open", "source-operator coefficients are not parent-owned"),
        ("AJS4235_3_relaxation", "mu_Xi T_res or T_res/tau_L", "open", "strong local requires order-few product for A_J_eff~1 and |c_Gamma|~1"),
        ("AJS4235_4_cGamma_scale", "c_Gamma natural size", "open", "no parent normalization or smallness theorem for c_Gamma"),
        ("AJS4235_5_R10_curve", "alpha(lambda) curve for finite-range row", "open_nonclaim", "R10 anchor remains schema-only, not a full curve"),
    ]
    return [
        {
            **common(),
            "amplitude_id": amplitude_id,
            "object": object_name,
            "status": status,
            "reason": reason,
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
        for amplitude_id, object_name, status, reason in rows
    ]


def decision_rows() -> List[Dict[str, str]]:
    return [
        {
            **common(),
            "decision": DECISION,
            "Kperp_private_removed": "True",
            "tensor_nohair_clause_private_closed": "True",
            "boundary_flux_private_routed": "True",
            "cGamma_zero_closed": "False",
            "full_budget_runner_active": "True",
            "scoreable_now": "False",
            "why_not_scoreable": "Gamma_mem support/source/profile and cGamma normalization are not parent-owned; AJ source coefficients remain unsigned",
            "strictest_full_budget": "alpha3 = 4e-20 dimensionless; Gdot/G = 2.42e-14 yr^-1",
            "next_highest_pressure": "derive parent Gamma_mem equation or fill A_src/A_lap/A_drift/A_boundary and cGamma profile coefficients",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
    ]


def firewall_rows() -> List[Dict[str, str]]:
    rows = [
        ("FW4235_0", "No cGamma zero claim follows from 4235.", "Only tensor no-hair and private Kperp removal improved; Gamma_mem support/source clauses remain open."),
        ("FW4235_1", "No profile score is allowed yet.", "The full-budget table lacks cGamma and arena profile/Jacobian coefficients."),
        ("FW4235_2", "No R10 pass is allowed.", "The R10 row is still anchor-only without a full alpha(lambda) curve or mapped envelope."),
        ("FW4235_3", "No public local-GR claim is allowed.", "Private cGamma survivor and public Kperp/global adoption caveats remain."),
        ("FW4235_4", "No half-budget penalty remains inside the private selector.", "4234 removed Kperp as an extra private static local force; cGamma now uses full budgets."),
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
            "summary": "4235 updates cGamma after Kperp removal: cGamma is now the sole private local non-EH survivor, gets full local budgets, but still needs Gamma_mem support/nohair or sourced profile coefficients.",
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
            "reason": "The remaining private local obstruction is no longer tensor leakage; it is the Gamma_mem source/profile owner.",
            "derive_first": "derive the parent Gamma_mem equation and prove P_loc J_res=0/support silence",
            "fill_second": "if derivation fails, fill A_src, A_lap, A_drift, A_boundary, T_res/tau_L, c_Gamma and arena profiles against full-budget rows",
            "fallback": "keep public Kperp tensor fallback and R10 curve caveats retained",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
    ]


def formal_doc() -> str:
    return f"""
# 251 - PPC4161 cGamma Support-NoHair Or Full-Budget Profile Bound Runner

Marker: `{MARKER}`

Branch: `{BRANCH}`
Decision: `{DECISION}`

## Result

4234 removes `Kperp/c_T` as an extra static force inside the private selector. Therefore the private local non-EH survivor is now:

```text
c_Gamma.
```

4235 refreshes the cGamma gate with full budgets:

```text
|C_Gamma,a| <= B_a
```

instead of the two-survivor half-budget rule.

## What Improved

The five-clause cGamma zero route was:

```text
vertical/readout silence;
compact support silence;
ordinary source silence;
boundary flux routing;
tensor no-hair.
```

After 4234:

```text
boundary flux routing = private pass,
tensor no-hair = private pass.
```

But the core memory/source clauses remain open:

```text
P_loc Gamma_mem = 0      not proved;
P_loc J_res = 0          not proved;
D_t Xi_0 = 0             not proved;
grad_perp Xi_0 = 0       not proved.
```

## Full-Budget Pressure

The sharpest live full-budget rows are:

```text
|c_Gamma profile_alpha3| <= 4e-20,
|c_Gamma D_t Xi_0| <= 2.42e-14 yr^-1,
|c_Gamma L_loc grad_perp Xi_0| <= 4e-9.
```

The R10 row remains nonclaim because it is still anchor-only, not a full alpha(lambda) curve.

## Next Target

`{NEXT_TARGET}`
"""


def checkpoint_doc() -> str:
    return f"""
# 4235 - cGamma Support-NoHair Or Full-Budget Profile Bound Runner

**Status:** `{DECISION}`.

## Forward Move

Kperp is no longer consuming private local budget, so cGamma is now tested alone:

```text
|C_Gamma,a| <= B_a.
```

This is better than 4233: no half-budget split inside the private selector.

## What Remains

The tensor no-hair clause is privately closed, but the real cGamma problem is still live:

```text
Gamma_mem support/source/profile is not parent-owned.
```

So this checkpoint builds the full-budget runner but makes no pass claim.

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
            "claim": "After Kperp is privately routed away, c_Gamma is the sole private local non-EH survivor and now uses full local empirical budgets rather than half-budget shared rows; c_Gamma still requires Gamma_mem support/nohair or source-backed profile coefficients before any local-GR pass.",
            "current_evidence": "4235 source register, cGamma support clause update, full-budget profile table, amplitude owner status, decision and firewall.",
            "status": "private_cGamma_full_budget_runner_nonclaim",
            "next_test": "Derive the parent Gamma_mem equation and prove P_loc J_res=0/support silence, or fill A_src/A_lap/A_drift/A_boundary, T_res/tau_L, c_Gamma and arena profile coefficients.",
            "key_risk": "Treating full-budget availability as a pass would overclaim; the profile/Jacobian and cGamma normalization rows are still missing.",
        }
    )
    with path.open("w", newline="", encoding="utf-8") as handle:
        fieldnames = ["claim_id", "domain", "claim", "current_evidence", "status", "next_test", "key_risk"]
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def update_spine_and_packet() -> None:
    spine_block = f"""
## PPC4161 cGamma Full-Budget Profile Runner

Marker: `{MARKER}`

4235 updates the local branch after Kperp removal. The private local non-EH survivor is now `c_Gamma` alone, so the cGamma product rows use full local budgets:

```text
|C_Gamma,a| <= B_a.
```

The tensor no-hair and boundary-routing clauses are privately closed, but `Gamma_mem` support/source/profile ownership remains open. The next target is the parent `Gamma_mem` equation or the first real `A_J`/profile coefficient fill.
"""
    packet_block = f"""
## Packet Update - cGamma Full-Budget Profile Runner

Marker: `{PACKET_MARKER}`

With `Kperp_private_static_force_zero=true`, the private two-survivor budget collapses to cGamma-only:

```text
|c_Gamma profile_a| <= B_a.
```

No local-GR pass follows. The surviving private local obstruction is `Gamma_mem` support/source/profile ownership.
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
    support = support_clause_rows()
    profile_rows = full_budget_rows()
    add("VAL4235_0_sources_exist", "all source paths exist", all(row["exists"] == "True" for row in sources), "source register")
    add("VAL4235_1_needles_found", "all source needles found", all(row["required_text_found"] == "True" for row in sources), "source register")
    add("VAL4235_2_support_clauses", "five support/nohair clauses present", len(support) == 5, str(len(support)))
    add("VAL4235_3_two_private_passes", "boundary and tensor clauses pass privately", sum(1 for row in support if row["private_status_after_4235"] == "private_pass") == 2, "support update")
    add("VAL4235_4_open_core_clauses", "core memory clauses remain open", sum(1 for row in support if row["private_status_after_4235"] == "open") == 3, "support update")
    add("VAL4235_5_full_budget_rows", "full-budget profile table has local arenas", len(profile_rows) >= 10, str(len(profile_rows)))
    add("VAL4235_6_no_half_budget", "profile rows record half-budget removed", all(row["half_budget_removed_by_4234"] == "True" for row in profile_rows), "profile rows")
    add("VAL4235_7_alpha3_full_budget", "alpha3 full budget restored to 4e-20", any(row["observable"] == "alpha3" and row["full_budget"] == "3.9999999999999998e-20" for row in profile_rows), "profile rows")
    add("VAL4235_8_no_score_now", "no profile row scoreable now", all(row["scoreable_now"] == "False" for row in profile_rows), "profile rows")
    add("VAL4235_9_docs_written", "formal and checkpoint docs exist", FORMAL_PATH.exists() and DOC_PATH.exists(), f"{FORMAL_PATH}; {DOC_PATH}")
    add("VAL4235_10_claim_register", "claims register contains L-076", CLAIM_ID in read_text(FORMAL / "02-claims-register.csv"), str(FORMAL / "02-claims-register.csv"))
    add("VAL4235_11_spine_marker", "spine contains marker", MARKER in read_text(FORMAL / "07-unification-spine.md"), str(FORMAL / "07-unification-spine.md"))
    add("VAL4235_12_packet_marker", "packet contains marker", PACKET_MARKER in read_text(FORMAL / "180-PPC4161-private-local-packet-integration.md"), str(FORMAL / "180-PPC4161-private-local-packet-integration.md"))
    add("VAL4235_13_no_claim_flags", "no generated row is valid for claim", all(row.get("valid_for_claim") != "True" for group in (sources, support, profile_rows, amplitude_status_rows(), decision_rows(), firewall_rows(), status_rows(), next_target_rows()) for row in group), "all generated groups")
    add("VAL4235_14_next_target", "next target selected", next_target_rows()[0]["next_target"] == NEXT_TARGET, NEXT_TARGET)
    return rows


def main() -> None:
    paths = {
        "source": SOURCE_DIR / "P8_Y5_R2FR_4235_SOURCE_REGISTER.csv",
        "support": SOURCE_DIR / "P8_Y5_R2FR_4235_CGAMMA_SUPPORT_NOHAIR_UPDATE.csv",
        "full_budget": SOURCE_DIR / "P8_Y5_R2FR_4235_CGAMMA_FULL_BUDGET_PROFILE_TABLE.csv",
        "amplitude": SOURCE_DIR / "P8_Y5_R2FR_4235_AJ_AMPLITUDE_STATUS.csv",
        "decision": SOURCE_DIR / "P8_Y5_R2FR_4235_DECISION.csv",
        "firewall": SOURCE_DIR / "P8_Y5_R2FR_4235_CLAIM_FIREWALL.csv",
        "status": SOURCE_DIR / "P8_Y5_R2FR_4235_STATUS.csv",
        "next": SOURCE_DIR / "P8_Y5_R2FR_4235_NEXT_TARGET.csv",
    }
    write_text(FORMAL_PATH, formal_doc())
    write_text(DOC_PATH, checkpoint_doc())
    write_csv(paths["source"], source_rows())
    write_csv(paths["support"], support_clause_rows())
    write_csv(paths["full_budget"], full_budget_rows())
    write_csv(paths["amplitude"], amplitude_status_rows())
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

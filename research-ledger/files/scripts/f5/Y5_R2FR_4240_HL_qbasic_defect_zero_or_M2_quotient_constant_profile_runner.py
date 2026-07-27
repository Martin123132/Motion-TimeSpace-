from __future__ import annotations

import csv
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, Iterable, List


ROOT = Path(__file__).resolve().parents[2]
FORMAL = ROOT / "formalization-workbench"
POST = ROOT / "post-checkpoint-work"
SOURCE_DIR = POST / "source-intake" / "mts_residuals"

CHECKPOINT = "4240"
CLAIM_ID = "L-081"
BRANCH = "MTS_R2FR_Y5_HL_QBASIC_DEFECT_OR_M2_PROFILE_RUNNER_4240"
DECISION = "HL_QBASIC_FULL_ZERO_NOT_DERIVED_PROFILE_GRID_DRY_RUNNER_BUILT_FOR_SOURCE_DEFECT_M2_LAP_DRIFT_NONCLAIM"
MARKER = "PPC4161_HL_QBASIC_DEFECT_M2_PROFILE_RUNNER_4240"
PACKET_MARKER = "PPC4161_PACKET_HL_QBASIC_DEFECT_M2_PROFILE_RUNNER_4240"
NEXT_TARGET = "4241-Y5-R2FR-real-Hperp-M2-profile-input-or-M2-quotient-constant-proof.md"

FORMAL_PATH = FORMAL / "256-PPC4161-HL-qbasic-defect-zero-or-M2-quotient-constant-profile-runner.md"
DOC_PATH = POST / "4240-Y5-R2FR-HL-qbasic-defect-zero-or-M2-quotient-constant-profile-runner.md"
VALIDATION_PATH = SOURCE_DIR / "P8_Y5_BRR545_4240_VALIDATION.csv"

BUDGET_STRONG_GDOT = 0.1678939074330212


@dataclass(frozen=True)
class SourceSpec:
    source_id: str
    path: Path
    required_text: str
    role: str


STAMP = datetime.now(timezone.utc).replace(microsecond=0).isoformat()


SOURCE_SPECS: Dict[str, SourceSpec] = {
    "SRC4240_00_4239_next": SourceSpec(
        "SRC4240_00_4239_next",
        SOURCE_DIR / "P8_Y5_R2FR_4239_NEXT_TARGET.csv",
        "4240-Y5-R2FR-HL-qbasic-defect-zero-or-M2-quotient-constant-profile-runner.md",
        "4239 selected the Hperp/M2 runner fork.",
    ),
    "SRC4240_01_4239_formal": SourceSpec(
        "SRC4240_01_4239_formal",
        FORMAL / "255-PPC4161-parent-source-orthogonality-or-M2-profile-sampler-dry-run.md",
        "S_A H_L^A = S_A H_perp^A.",
        "4239 reduced source term to Hperp defect.",
    ),
    "SRC4240_02_4239_budget": SourceSpec(
        "SRC4240_02_4239_budget",
        FORMAL / "255-PPC4161-parent-source-orthogonality-or-M2-profile-sampler-dry-run.md",
        "0.1678939074330212",
        "4239 reduced strong local budget.",
    ),
    "SRC4240_03_leakage_candidate": SourceSpec(
        "SRC4240_03_leakage_candidate",
        FORMAL / "125-local-leakage-vector-invariant.md",
        "H_L^A(X_B);",
        "125 explicitly says H_L is not parent-derived.",
    ),
    "SRC4240_04_component_pool": SourceSpec(
        "SRC4240_04_component_pool",
        FORMAL / "125-local-leakage-vector-invariant.md",
        "| `H_theta` | `E_theta` |",
        "H_L candidate components are invariant-profile functions, not automatically q-fibre directions.",
    ),
    "SRC4240_05_closure_architecture": SourceSpec(
        "SRC4240_05_closure_architecture",
        FORMAL / "85-coarse-graining-invariants-XB.md",
        "closure architecture",
        "85 labels D_L=U_B H_L as closure architecture rather than parent derivation.",
    ),
    "SRC4240_06_source_law": SourceSpec(
        "SRC4240_06_source_law",
        FORMAL / "85-coarse-graining-invariants-XB.md",
        "S_cg(X_B) =",
        "X_B source law branch.",
    ),
    "SRC4240_07_4238_zero": SourceSpec(
        "SRC4240_07_4238_zero",
        FORMAL / "254-PPC4161-vertical-current-M2-zero-theorem-or-profile-sampler.md",
        "Delta_h M_2 = 0,",
        "4238 M2 zero target.",
    ),
    "SRC4240_08_fixed_point": SourceSpec(
        "SRC4240_08_fixed_point",
        FORMAL / "207-PPC4161-memory-fixed-point-equation-and-smooth-minimizer-contract.md",
        "stationary and projected-homogeneous local invariants imply:",
        "Stationary/homogeneous local invariant route.",
    ),
    "SRC4240_09_no_flux": SourceSpec(
        "SRC4240_09_no_flux",
        FORMAL / "192-PPC4161-local-boundary-no-flux-sector-interface-theorem.md",
        "F_side[tau] = 0.",
        "No-flux collar background for harmonic M2 branch.",
    ),
    "SRC4240_10_claim_register": SourceSpec(
        "SRC4240_10_claim_register",
        FORMAL / "02-claims-register.csv",
        "L-080",
        "Prior claim-register anchor for 4239.",
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


def hperp_audit_rows() -> List[Dict[str, str]]:
    rows = [
        ("HA4240_0_qbasic_sublemma", "S_A H_q^A=0", "private_pass", "4239 quotient source descent kills q-basic source piece."),
        ("HA4240_1_full_HL_qbasic", "H_L=H_q", "not_derived", "Current H_L candidate is an X_B closure profile, not parent-signed as wholly q-fibre representative motion."),
        ("HA4240_2_Hperp_zero", "H_perp=0", "not_derived", "Would be a smuggled source zero unless parent proves full q-basic adoption."),
        ("HA4240_3_source_defect", "A_src=sup|S_A H_perp^A|", "active_bound_row", "This is the live reduced source obstruction."),
        ("HA4240_4_M2_constant", "Delta_h M_2=D_t M_2=0", "not_derived", "Requires quotient-constant/harmonic stationary profile proof."),
        ("HA4240_5_runner_route", "profile_grid_runner", "selected", "Use dry-run controls now; replace with real parent profiles later."),
    ]
    return [
        {
            **common(),
            "audit_id": audit_id,
            "condition": condition,
            "status": status,
            "reason": reason,
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
        for audit_id, condition, status, reason in rows
    ]


def profile_control_rows() -> List[Dict[str, str]]:
    controls = [
        ("PC4240_0_zero_control", 0.0, 0.0, 0.0, "pass_control", "constant M2 and no Hperp defect"),
        ("PC4240_1_small_source_defect", 0.01, 0.0, 0.0, "pass_control", "small non-q source defect"),
        ("PC4240_2_large_source_defect", 0.20, 0.0, 0.0, "fail_control", "large non-q source defect"),
        ("PC4240_3_small_lap", 0.0, 0.01, 0.0, "pass_control", "small M2 Laplacian"),
        ("PC4240_4_large_lap", 0.0, 0.20, 0.0, "fail_control", "large M2 Laplacian"),
        ("PC4240_5_small_drift", 0.0, 0.0, 0.01, "pass_control", "small M2 drift"),
        ("PC4240_6_mixed_no_cancel", 0.06, 0.06, 0.06, "fail_control", "mixed row fails under absolute no-cancellation budget"),
    ]
    rows: List[Dict[str, str]] = []
    for control_id, source_defect, lap_term, drift_term, expected, description in controls:
        total_abs = abs(source_defect) + abs(lap_term) + abs(drift_term)
        rows.append(
            {
                **common(),
                "control_id": control_id,
                "description": description,
                "source_defect_abs": f"{source_defect:.12g}",
                "lap_term_abs": f"{lap_term:.12g}",
                "drift_term_abs": f"{drift_term:.12g}",
                "total_abs": f"{total_abs:.12g}",
                "budget_normalized": f"{BUDGET_STRONG_GDOT:.16g}",
                "passes_budget_control": str(total_abs <= BUDGET_STRONG_GDOT),
                "expected_control": expected,
                "matches_expected": str((total_abs <= BUDGET_STRONG_GDOT) == expected.startswith("pass")),
                "claim_allowed": "False",
                "valid_for_claim": "False",
            }
        )
    return rows


def m2_gate_rows() -> List[Dict[str, str]]:
    rows = [
        ("MG4240_0_input_profiles", "H_L^A(x,t), H_AB(x,t), S_A(x,t)", "missing", "Required for real profile run."),
        ("MG4240_1_quotient_constant", "M_2=Mbar(q-homogeneous I_loc)", "open", "Would prove grad_i M2=Delta_h M2=0."),
        ("MG4240_2_harmonic_neumann", "Delta_h M2=0 with no-flux/fixed boundary", "open", "Would prove constant M2 on connected compact collar."),
        ("MG4240_3_stationary", "D_t M2=0", "open", "Requires stationary H_L/H_AB or source-flow invariant."),
        ("MG4240_4_no_cancellation", "use |source|+|lap|+|drift|", "active", "Runner rejects cancellation scoring."),
    ]
    return [
        {
            **common(),
            "gate_id": gate_id,
            "gate": gate,
            "status": status,
            "meaning": meaning,
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
        for gate_id, gate, status, meaning in rows
    ]


def decision_rows() -> List[Dict[str, str]]:
    return [
        {
            **common(),
            "decision": DECISION,
            "forward_move": "Full H_L q-basic zero is rejected as unproved; profile-grid controls now exercise source defect, M2 Laplacian and M2 drift against the reduced 4239 budget.",
            "Hperp_zero_claimed": "False",
            "profile_runner_ready_for_real_inputs": "schema_and_controls_only",
            "scoreable_now": "False",
            "best_next_move": NEXT_TARGET,
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
    ]


def firewall_rows() -> List[Dict[str, str]]:
    rows = [
        ("FW4240_0_no_Hperp_zero", "Do not set H_perp=0 from the current X_B/H_L candidate; it is closure architecture, not parent derivation.", "active"),
        ("FW4240_1_controls_nonclaim", "Control grid pass/fail rows validate runner logic only; they are not physical evidence.", "active"),
        ("FW4240_2_no_cancellation", "Runner uses absolute budget and gives no cancellation credit.", "active"),
        ("FW4240_3_real_inputs_required", "A real local claim needs sourced H_L, H_AB, S_A, D_m, tau ratio, cGamma and arena projections.", "active"),
        ("FW4240_4_private_scope", "All reduced cGamma rows remain private nonclaim until parent signatures or source-backed bounds exist.", "active"),
    ]
    return [
        {
            **common(),
            "firewall_id": firewall_id,
            "rule": rule,
            "status": status,
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
        for firewall_id, rule, status in rows
    ]


def status_rows() -> List[Dict[str, str]]:
    return [
        {
            **common(),
            "status": "private_profile_runner_dry_run_nonclaim",
            "summary": "4240 rejects the unproved Hperp=0 shortcut and builds a dry-run control grid for the reduced source/M2 budget.",
            "scoreable_now": "False",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
    ]


def next_target_rows() -> List[Dict[str, str]]:
    return [
        {
            **common(),
            "next_target": NEXT_TARGET,
            "reason": "The next step is either real parent profile input for Hperp/M2/S_A, or a proof that M2 is quotient-constant/harmonic and stationary.",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
    ]


def all_generated_groups() -> Iterable[List[Dict[str, str]]]:
    return (
        source_rows(),
        hperp_audit_rows(),
        profile_control_rows(),
        m2_gate_rows(),
        decision_rows(),
        firewall_rows(),
        status_rows(),
        next_target_rows(),
    )


def formal_doc() -> str:
    return f"""
# 256 - PPC4161 H_L q-basic defect zero or M2 quotient-constant profile runner

Marker: `{MARKER}`

Branch: `{BRANCH}`
Decision: `{DECISION}`

## Result

4240 refuses the unearned shortcut:

```text
H_perp = 0.
```

The current `X_B/H_L` construction is a disciplined bounded candidate, but the source files still label it as closure architecture rather than a parent derivation. Therefore the safe reduced budget remains:

```text
A_J,eff_private <= |S_A H_perp^A| + |D_m Delta_h M_2| + |D_t M_2|.
```

## Dry-Run Profile Runner

The dry-run grid tests the reduced budget logic with normalized control rows:

```text
total_abs = |S_A H_perp^A| + |D_m Delta_h M_2| + |D_t M_2|.
```

Against the strong local normalized budget:

```text
total_abs <= {BUDGET_STRONG_GDOT} * (mu_Xi T_res)/|c_Gamma|.
```

For the control run, `(mu_Xi T_res)/|c_Gamma|` is set to one. These rows are not physical evidence; they prove the runner catches pass/fail and no-cancellation behavior.

## What Still Needs Real Input

The dry-runner becomes physical only after real source rows are supplied:

```text
H_perp^A(x,t),
H_AB(x,t),
S_A(x,t),
D_m,
T_res/tau_L,
c_Gamma,
arena projections.
```

## Remaining Proof Route

The analytic route is still alive, but exact:

```text
H_perp=0,
Delta_h M_2=0,
D_t M_2=0.
```

No public local-GR claim follows from 4240.

## Next Target

`{NEXT_TARGET}`
"""


def checkpoint_doc() -> str:
    return f"""
# 4240 - H_L q-basic defect zero or M2 quotient-constant profile runner

**Status:** `{DECISION}`.

## Forward Move

4240 rejects the unproved `H_perp=0` shortcut and builds a dry-run control grid for:

```text
|S_A H_perp^A| + |D_m Delta_h M_2| + |D_t M_2|.
```

The runner catches pass, fail, and mixed no-cancellation cases.

## Still Missing

No physical profile has been supplied yet:

```text
H_perp, H_AB, S_A, D_m, T_res/tau_L, c_Gamma, arena projection.
```

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
            "claim": "The current H_L candidate does not justify H_perp=0; 4240 keeps Hperp as an explicit defect and builds a nonclaim dry-run grid for |S_A Hperp|, |D_m Delta_h M2| and |D_t M2| against the reduced local budget.",
            "current_evidence": "4240 source register, Hperp audit, profile control grid, M2 gates, decision and firewall.",
            "status": "private_profile_runner_dry_run_nonclaim",
            "next_test": "Supply real Hperp/M2/S_A profile inputs or prove M2 quotient-constant/harmonic stationary behavior.",
            "key_risk": "Treating control-grid pass rows as physics or setting Hperp=0 by assertion would overclaim.",
        }
    )
    with path.open("w", newline="", encoding="utf-8") as handle:
        fieldnames = ["claim_id", "domain", "claim", "current_evidence", "status", "next_test", "key_risk"]
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def update_spine_and_packet() -> None:
    spine_block = f"""
## PPC4161 H_L q-basic defect / M2 profile runner

Marker: `{MARKER}`

4240 rejects the unproved full `H_L=H_q` shortcut. The live reduced cGamma source/M2 budget is:

```text
|S_A H_perp^A| + |D_m Delta_h M_2| + |D_t M_2|.
```

A dry-run grid now verifies pass/fail/no-cancellation runner logic, but all rows are nonclaim until real parent profiles or exact M2 quotient-constant/harmonic proofs exist.
"""
    packet_block = f"""
## Packet Update - H_L q-basic defect / M2 profile runner

Marker: `{PACKET_MARKER}`

The private packet now treats `H_perp` as an explicit source-defect row. This prevents the cGamma source zero from being smuggled by identifying the whole `H_L` candidate with a q-basic fibre direction.
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
    audit = hperp_audit_rows()
    controls = profile_control_rows()
    gates = m2_gate_rows()
    all_rows = [row for group in all_generated_groups() for row in group]
    pass_controls = [row for row in controls if row["passes_budget_control"] == "True"]
    fail_controls = [row for row in controls if row["passes_budget_control"] == "False"]

    add("VAL4240_0_sources_exist", "all source paths exist", all(row["exists"] == "True" for row in sources), "source register")
    add("VAL4240_1_needles_found", "all source needles found", all(row["required_text_found"] == "True" for row in sources), "source register")
    add("VAL4240_2_Hperp_not_zero", "Hperp zero remains not derived", any(row["condition"] == "H_perp=0" and row["status"] == "not_derived" for row in audit), "Hperp audit")
    add("VAL4240_3_runner_selected", "profile grid runner selected", any(row["condition"] == "profile_grid_runner" and row["status"] == "selected" for row in audit), "Hperp audit")
    add("VAL4240_4_controls_have_pass_fail", "controls include pass and fail rows", len(pass_controls) > 0 and len(fail_controls) > 0, "profile controls")
    add("VAL4240_5_controls_match_expected", "all controls match expected pass/fail", all(row["matches_expected"] == "True" for row in controls), "profile controls")
    add("VAL4240_6_mixed_no_cancel_fails", "mixed no-cancellation control fails", any(row["control_id"] == "PC4240_6_mixed_no_cancel" and row["passes_budget_control"] == "False" for row in controls), "profile controls")
    add("VAL4240_7_M2_gates_open", "M2 quotient/harmonic/stationary gates remain open", {"MG4240_1_quotient_constant", "MG4240_2_harmonic_neumann", "MG4240_3_stationary"}.issubset({row["gate_id"] for row in gates if row["status"] == "open"}), "M2 gates")
    add("VAL4240_8_decision_nonclaim", "decision keeps scoreable false", decision_rows()[0]["scoreable_now"] == "False", "decision")
    add("VAL4240_9_docs_written", "formal and checkpoint docs exist", FORMAL_PATH.exists() and DOC_PATH.exists(), f"{FORMAL_PATH}; {DOC_PATH}")
    add("VAL4240_10_claim_register", "claims register contains L-081", CLAIM_ID in read_text(FORMAL / "02-claims-register.csv"), str(FORMAL / "02-claims-register.csv"))
    add("VAL4240_11_spine_marker", "spine contains marker", MARKER in read_text(FORMAL / "07-unification-spine.md"), str(FORMAL / "07-unification-spine.md"))
    add("VAL4240_12_packet_marker", "packet contains marker", PACKET_MARKER in read_text(FORMAL / "180-PPC4161-private-local-packet-integration.md"), str(FORMAL / "180-PPC4161-private-local-packet-integration.md"))
    add("VAL4240_13_no_claim_flags", "no generated row is valid for claim", all(row.get("valid_for_claim") != "True" for row in all_rows), "all generated groups")
    add("VAL4240_14_next_target", "next target selected", next_target_rows()[0]["next_target"] == NEXT_TARGET, NEXT_TARGET)
    return rows


def main() -> None:
    paths = {
        "source": SOURCE_DIR / "P8_Y5_R2FR_4240_SOURCE_REGISTER.csv",
        "audit": SOURCE_DIR / "P8_Y5_R2FR_4240_HPERP_QBASIC_AUDIT.csv",
        "controls": SOURCE_DIR / "P8_Y5_R2FR_4240_PROFILE_CONTROL_GRID.csv",
        "gates": SOURCE_DIR / "P8_Y5_R2FR_4240_M2_QUOTIENT_GATES.csv",
        "decision": SOURCE_DIR / "P8_Y5_R2FR_4240_DECISION.csv",
        "firewall": SOURCE_DIR / "P8_Y5_R2FR_4240_CLAIM_FIREWALL.csv",
        "status": SOURCE_DIR / "P8_Y5_R2FR_4240_STATUS.csv",
        "next": SOURCE_DIR / "P8_Y5_R2FR_4240_NEXT_TARGET.csv",
    }
    write_text(FORMAL_PATH, formal_doc())
    write_text(DOC_PATH, checkpoint_doc())
    write_csv(paths["source"], source_rows())
    write_csv(paths["audit"], hperp_audit_rows())
    write_csv(paths["controls"], profile_control_rows())
    write_csv(paths["gates"], m2_gate_rows())
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

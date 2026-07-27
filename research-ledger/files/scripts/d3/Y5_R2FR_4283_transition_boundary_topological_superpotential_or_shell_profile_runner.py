from __future__ import annotations

import csv
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, Iterable, List


ROOT = Path(__file__).resolve().parents[2]
FORMAL = ROOT / "formalization-workbench"
POST = ROOT / "post-checkpoint-work"
SOURCE_DIR = POST / "source-intake" / "mts_residuals"

CHECKPOINT = "4283"
CLAIM_ID = "L-124"
BRANCH = "MTS_R2FR_Y5_TRANSITION_BOUNDARY_TOPOLOGICAL_SUPERPOTENTIAL_OR_SHELL_PROFILE_RUNNER_4283"
DECISION = "BOUNDARY_TOPOLOGICAL_ROUTE_FAILS_GENERIC_SHELL_NOFLUX_ONLY_SUPPORT_SEPARATED_PROFILE_RUNNER_BLOCKED_PENDING_REAL_PROFILES_NONCLAIM"
MARKER = "PPC4161_TRANSITION_BOUNDARY_TOPOLOGICAL_SUPERPOTENTIAL_OR_SHELL_PROFILE_RUNNER_4283"
PACKET_MARKER = "PPC4161_PACKET_TRANSITION_BOUNDARY_TOPOLOGICAL_SUPERPOTENTIAL_OR_SHELL_PROFILE_RUNNER_4283"
NEXT_TARGET = "4284-Y5-R2FR-real-transition-shell-profile-calculator-and-threshold-comparator.md"

FORMAL_PATH = FORMAL / "299-PPC4161-transition-boundary-topological-superpotential-or-shell-profile-runner.md"
DOC_PATH = POST / "4283-Y5-R2FR-transition-boundary-topological-superpotential-or-shell-profile-runner.md"
VALIDATION_PATH = SOURCE_DIR / "P8_Y5_BRR545_4283_VALIDATION.csv"

STAMP = datetime.now(timezone.utc).replace(microsecond=0).isoformat()
Q_SUPPRESSION_THRESHOLD = 4.3819265819966744e-17
LOCAL_RESPONSE_THRESHOLD = 4.212667126774669e-17
AJ_STRONG_WINDOW = "0.1678939074330212*(mu_Xi T_res)/|c_Gamma|"

SOURCES = {
    "SRC4283_00_4282_fork": (
        FORMAL / "298-PPC4161-transition-shell-cancellation-projector-theorem-or-profile-source-rows.md",
        "boundary/topological/superpotential owner with zero bulk local response",
        "4282 selects the boundary/topological route or profile runner.",
    ),
    "SRC4283_01_142_boundary_open": (
        FORMAL / "142-owner-spacetime-solder-map-theorem.md",
        "boundary/topological backup remains open",
        "142 leaves boundary/topological backup as the final route after bulk solder failure.",
    ),
    "SRC4283_02_143_boundary_fail": (
        FORMAL / "143-boundary-topological-backup-gate.md",
        "boundary_topological_backup_fails_transition_branch_demoted_closure_only",
        "143 already tests and rejects generic boundary/topological transition closure.",
    ),
    "SRC4283_03_192_noflux_scope": (
        FORMAL / "192-PPC4161-local-boundary-no-flux-sector-interface-theorem.md",
        "If any clause fails, the theorem does not set the leakage to zero.",
        "192 supplies a valid compact-collar no-flux selector, but only under support separation.",
    ),
    "SRC4283_04_233_boundary_flux": (
        FORMAL / "233-PPC4161-boundary-corner-curl-zero-or-flux-bound.md",
        "retained as boundary/Hamiltonian flux, not converted into a hidden bulk force",
        "233 gives the boundary/corner flux guardrail.",
    ),
    "SRC4283_05_216_kperp": (
        FORMAL / "216-PPC4161-Kperp-boundary-zero-or-demotion.md",
        "local no-flux != transverse tensor no-hair",
        "216 prevents boundary/no-flux from silently killing tensor homogeneous modes.",
    ),
    "SRC4283_06_92_threshold": (
        FORMAL / "92-solar-transition-current-ppn-gate.md",
        "required_q_suppression_factor = 4.3819265819966744e-17",
        "92 provides the hard transition-shell profile threshold.",
    ),
    "SRC4283_07_144_response": (
        FORMAL / "144-local-transition-closure-contract.md",
        "normalized local transition response <= 4.212667126774669e-17.",
        "144 provides the local response threshold.",
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
        f'"4283 resolves the boundary/topological fork: the no-flux theorem remains valid only for support-separated compact collars, while the generic transition-shell superpotential/topological route fails because it cannot simultaneously own nonzero q_tr, keep zero bulk local metric response, control finite boundary terms, and guard K_perp. The practical next step is a real transition-shell profile calculator against sourced thresholds.",'
        f'"4283 source register, boundary/topological audit, no-flux selector scope, superpotential no-go rows, shell-profile runner inputs/results, decision and firewall.",'
        f'private_boundary_topological_generic_shell_route_failed_profile_runner_next_nonclaim,'
        f'"Build the real transition-shell profile calculator and compare q_tr/Sigma_metric/AJ profiles against the sourced thresholds.",'
        f'"Using compact-collar no-flux as a theorem through the shell, treating exact topological identities as ownership of generic q_tr, or ignoring finite boundary/Kperp response."\n'
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


def boundary_audit_rows() -> List[Dict[str, str]]:
    raw = [
        (
            "BT4283_0_exact_superpotential",
            "K_A^{mu nu}=nabla_rho U_A^{rho mu nu}",
            "Exact superpotential can be bulk-null/boundary-like, but does not generically own nonzero q_tr.",
            "GENERIC_QTR_OWNERSHIP_NOT_DERIVED",
        ),
        (
            "BT4283_1_exterior_exact_form",
            "J_A=dU_A and dJ_A=0",
            "d^2=0 protects identities, not arbitrary transition current ownership.",
            "TOO_RESTRICTIVE_FOR_GENERIC_QTR",
        ),
        (
            "BT4283_2_topological_density",
            "S_tr,bt=int P(F_A)",
            "Can be bulk metric-null, but becomes locally empty or active only through defects/boundaries.",
            "BULK_NULLITY_INSUFFICIENT",
        ),
        (
            "BT4283_3_boundary_defect",
            "q_tr supported on transition boundary/domain wall",
            "Nontrivial, but finite boundary stress/PPN response must be zero or below threshold.",
            "FINITE_BOUNDARY_RESPONSE_UNCONTROLLED",
        ),
        (
            "BT4283_4_Ward_inflow",
            "delta_g S_boundary + delta_g S_bulk = 0",
            "Would be viable, but no transition Ward/anomaly/inflow law is derived.",
            "WARD_INFLOW_NOT_DERIVED",
        ),
    ]
    return [
        {
            **common(),
            "audit_id": audit_id,
            "candidate": candidate,
            "meaning": meaning,
            "status": status,
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
        for audit_id, candidate, meaning, status in raw
    ]


def noflux_scope_rows() -> List[Dict[str, str]]:
    raw = [
        (
            "NF4283_0_valid_scope",
            "supp(T_local) subset int(W_loc), side/interface pullbacks zero, boundary Hamiltonian fixed/routed",
            "192 closes transition-current leakage in compact support-separated local selector branch.",
            "NOFLUX_SELECTOR_VALID_FOR_SUPPORT_SEPARATED_COLLARS",
        ),
        (
            "NF4283_1_shell_scope_fail",
            "W_loc intersects transition support or finite boundary/domain wall response",
            "Then 192 explicitly reopens a transition-current or boundary-flux row.",
            "NOFLUX_DOES_NOT_CLOSE_GENERIC_SHELL",
        ),
        (
            "NF4283_2_4281_consistency",
            "support-separated no-flux scope is the same mathematical branch as 4281 finite-margin zero",
            "This is not an independent proof through the shell.",
            "REDUCES_TO_FINITE_MARGIN_BRANCH",
        ),
    ]
    return [
        {
            **common(),
            "scope_id": scope_id,
            "condition": condition,
            "meaning": meaning,
            "status": status,
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
        for scope_id, condition, meaning, status in raw
    ]


def superpotential_no_go_rows() -> List[Dict[str, str]]:
    raw = [
        ("NG4283_0", "bulk metric-nullity", "formally possible for exact/topological blocks", "PARTIAL_PASS"),
        ("NG4283_1", "nontrivial q_tr ownership", "not derived for generic transition shell", "FAIL"),
        ("NG4283_2", "finite boundary/support control", "not derived; must be zero or <= threshold", "FAIL"),
        ("NG4283_3", "Ward/inflow identity", "not available", "FAIL"),
        ("NG4283_4", "K_perp guardrail", "boundary/no-flux does not kill transverse tensor no-hair", "FAIL_OR_BOUND_REQUIRED"),
        ("NG4283_5", "combined theorem", "bulk metric-nullity + q_tr ownership + boundary control not satisfied", "GENERIC_BOUNDARY_TOPOLOGICAL_THEOREM_FAILS"),
    ]
    return [
        {
            **common(),
            "no_go_id": no_go_id,
            "clause": clause,
            "meaning": meaning,
            "status": status,
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
        for no_go_id, clause, meaning, status in raw
    ]


def runner_input_rows() -> List[Dict[str, str]]:
    raw = [
        ("IN4283_0", "q_tr_shell_norm", "MISSING_REAL_PROFILE", "dimensionless threshold normalization", str(Q_SUPPRESSION_THRESHOLD), "PROFILE_REQUIRED"),
        ("IN4283_1", "Sigma_metric_shell_response", "MISSING_REAL_PROFILE", "dimensionless local response", str(LOCAL_RESPONSE_THRESHOLD), "PROFILE_REQUIRED"),
        ("IN4283_2", "R_transport_to_local_plus_R_Bgrad_to_local", "MISSING_REAL_PROFILE", "AJ private units", AJ_STRONG_WINDOW, "PROFILE_REQUIRED"),
        ("IN4283_3", "boundary_response", "MISSING_REAL_PROFILE", "dimensionless local response", str(LOCAL_RESPONSE_THRESHOLD), "PROFILE_REQUIRED"),
        ("IN4283_4", "K_perp_boundary_guard", "MISSING_REAL_PROFILE_OR_ZERO_THEOREM", "PPN/tensor response", "source-backed Kperp bound", "BOUND_OR_THEOREM_REQUIRED"),
    ]
    return [
        {
            **common(),
            "input_id": input_id,
            "quantity": quantity,
            "value": value,
            "units": units,
            "threshold_or_requirement": threshold,
            "status": status,
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
        for input_id, quantity, value, units, threshold, status in raw
    ]


def runner_result_rows() -> List[Dict[str, str]]:
    controls = [
        ("CTRL4283_pass_q", "q_tr_shell_norm", 1.0e-18, Q_SUPPRESSION_THRESHOLD),
        ("CTRL4283_fail_q", "q_tr_shell_norm", 1.0e-10, Q_SUPPRESSION_THRESHOLD),
        ("CTRL4283_pass_response", "Sigma_metric_shell_response", 1.0e-18, LOCAL_RESPONSE_THRESHOLD),
        ("CTRL4283_fail_response", "Sigma_metric_shell_response", 1.0e-10, LOCAL_RESPONSE_THRESHOLD),
    ]
    rows: List[Dict[str, str]] = []
    rows.append(
        {
            **common(),
            "result_id": "RUN4283_live",
            "quantity": "live_shell_profile_runner",
            "profile_value": "MISSING_REAL_PROFILE",
            "threshold": "SOURCE_BACKED_THRESHOLDS_AVAILABLE",
            "verdict": "BLOCKED_PENDING_REAL_PROFILE_INPUTS",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
    )
    for control_id, quantity, value, threshold in controls:
        verdict = "CONTROL_PASS_NONCLAIM" if abs(value) <= threshold else "CONTROL_FAIL_NONCLAIM"
        rows.append(
            {
                **common(),
                "result_id": control_id,
                "quantity": quantity,
                "profile_value": f"{value:.12e}",
                "threshold": f"{threshold:.12e}",
                "verdict": verdict,
                "claim_allowed": "False",
                "valid_for_claim": "False",
            }
        )
    return rows


def decision_rows() -> List[Dict[str, str]]:
    return [
        {
            **common(),
            "decision_id": "DEC4283_0",
            "selected_route": "REAL_SHELL_PROFILE_CALCULATOR_NEXT",
            "meaning": "Generic boundary/topological transition theorem fails; compact no-flux survives only as support-separated collar logic; proceed to real shell-profile calculation.",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
    ]


def firewall_rows() -> List[Dict[str, str]]:
    raw = [
        ("FW4283_0", "Do not apply 192 no-flux to collars intersecting transition support."),
        ("FW4283_1", "Do not count exact/topological bulk nullity as ownership of generic q_tr."),
        ("FW4283_2", "Do not ignore finite boundary/domain-wall PPN response."),
        ("FW4283_3", "Do not erase K_perp with scalar boundary/no-flux language."),
        ("FW4283_4", "Do not treat runner control rows as live physics passes."),
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
            "status_id": "STATUS4283_0",
            "status": "GENERIC_BOUNDARY_TOPOLOGICAL_SHELL_THEOREM_FAILED_PROFILE_RUNNER_READY_BLOCKED",
            "summary": "The transition shell route is now profile-runner first unless a genuinely new parent Ward/cohomology mechanism is introduced.",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
    ]


def next_target_rows() -> List[Dict[str, str]]:
    return [
        {
            **common(),
            "next_target_id": "NEXT4283_0",
            "target_file": NEXT_TARGET,
            "task": "Build the real shell-profile calculator for q_tr, Sigma_metric, boundary response, Kperp guardrail, and AJ residuals against sourced thresholds.",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
    ]


def formal_doc() -> str:
    return f"""
# 299 Transition Boundary/Topological Superpotential Or Shell Profile Runner

Marker: `{MARKER}`

Branch: `{BRANCH}`

Decision: `{DECISION}`

## Result

4283 tests the final theorem escape hatch for the transition shell.

The generic boundary/topological route fails as a derivation:

```text
bulk metric-nullity can pass formally,
but nontrivial q_tr ownership is not derived,
finite boundary/support response is not controlled,
Ward/inflow identity is not available,
K_perp guardrail is still open.
```

Therefore:

```text
bulk metric-nullity + nontrivial q_tr ownership + finite boundary/support control
```

is not satisfied.

## What 192 Still Gives

The local no-flux selector remains useful, but its scope is narrower:

```text
supp(T_local) subset int(W_loc),
side/interface pullbacks vanish,
boundary Hamiltonian data are fixed, zero, or explicitly routed.
```

If those clauses hold:

```text
J_tr^nu = 0 through <=2PN.
```

But if the local collar intersects transition support or finite boundary/domain-wall response, the theorem reopens a transition-current or boundary-flux row. So `192` agrees with the 4281 finite-margin branch; it does not prove safety through the shell.

## Runner Interface

The live route is now a real shell-profile calculator.

It must source:

```text
q_tr_shell_norm,
Sigma_metric_shell_response,
R_transport_to_local + R_Bgrad_to_local,
boundary_response,
K_perp_boundary_guard.
```

Thresholds are already source-backed:

```text
|q_tr_shell_norm| <= {Q_SUPPRESSION_THRESHOLD}
|Sigma_metric_shell_response| <= {LOCAL_RESPONSE_THRESHOLD}
```

and the cGamma AJ row must satisfy:

```text
|R_transport_to_local| + |R_Bgrad_to_local| <= {AJ_STRONG_WINDOW}.
```

The runner emitted control pass/fail rows, but the live row remains blocked until real profiles exist.

## Interpretation

This is an important narrowing:

```text
far/local support-separated branch: conditionally safe;
generic transition shell theorem: failed under current corpus;
next route: calculate the shell profile or introduce a genuinely new parent Ward/cohomology mechanism.
```

No public local-GR claim is made.

## Next Target

`{NEXT_TARGET}` should build the real transition-shell profile calculator and threshold comparator.
"""


def checkpoint_doc() -> str:
    return f"""
# 4283 - transition boundary/topological superpotential or shell-profile runner

Marker: `{MARKER}`

Decision: `{DECISION}`

4283 resolves the boundary/topological fork:

```text
generic shell theorem fails;
192 no-flux only applies to support-separated compact collars;
profile runner interface is ready but blocked pending real profile inputs.
```
"""


def validation_rows(paths: Dict[str, Path]) -> List[Dict[str, str]]:
    sources = csv_rows(paths["sources"])
    boundary = csv_rows(paths["boundary"])
    noflux = csv_rows(paths["noflux"])
    nogo = csv_rows(paths["nogo"])
    runner_inputs = csv_rows(paths["runner_inputs"])
    runner_results = csv_rows(paths["runner_results"])
    generated_rows: Iterable[Dict[str, str]] = (
        sources
        + boundary
        + noflux
        + nogo
        + runner_inputs
        + runner_results
        + csv_rows(paths["decision"])
        + csv_rows(paths["firewall"])
        + csv_rows(paths["status"])
        + csv_rows(paths["next_target"])
    )
    validations = [
        ("VAL4283_0_sources_exist", all(row["exists"] == "True" for row in sources), "all source paths exist"),
        ("VAL4283_1_needles_found", all(row["required_text_found"] == "True" for row in sources), "all source needles found"),
        (
            "VAL4283_2_boundary_fail",
            any(row["status"] == "GENERIC_QTR_OWNERSHIP_NOT_DERIVED" for row in boundary)
            and any(row["status"] == "FINITE_BOUNDARY_RESPONSE_UNCONTROLLED" for row in boundary),
            "boundary/topological ownership and finite response blockers emitted",
        ),
        (
            "VAL4283_3_noflux_scope",
            any(row["status"] == "NOFLUX_SELECTOR_VALID_FOR_SUPPORT_SEPARATED_COLLARS" for row in noflux)
            and any(row["status"] == "NOFLUX_DOES_NOT_CLOSE_GENERIC_SHELL" for row in noflux),
            "192 no-flux scope distinguished from generic shell",
        ),
        (
            "VAL4283_4_combined_nogo",
            any(row["status"] == "GENERIC_BOUNDARY_TOPOLOGICAL_THEOREM_FAILS" for row in nogo),
            "combined theorem failure recorded",
        ),
        (
            "VAL4283_5_runner_inputs",
            {"q_tr_shell_norm", "Sigma_metric_shell_response", "R_transport_to_local_plus_R_Bgrad_to_local", "K_perp_boundary_guard"}.issubset(
                {row["quantity"] for row in runner_inputs}
            ),
            "runner input schema covers shell profile quantities",
        ),
        (
            "VAL4283_6_runner_controls",
            any(row["verdict"] == "CONTROL_PASS_NONCLAIM" for row in runner_results)
            and any(row["verdict"] == "CONTROL_FAIL_NONCLAIM" for row in runner_results)
            and any(row["verdict"] == "BLOCKED_PENDING_REAL_PROFILE_INPUTS" for row in runner_results),
            "runner controls and live blocked row emitted",
        ),
        ("VAL4283_7_formal_doc", FORMAL_PATH.exists() and MARKER in read_text(FORMAL_PATH), "formal doc written"),
        ("VAL4283_8_checkpoint_doc", DOC_PATH.exists() and DECISION in read_text(DOC_PATH), "checkpoint doc written"),
        ("VAL4283_9_claim_row", f"{CLAIM_ID}," in read_text(FORMAL / "02-claims-register.csv"), "claim register row added"),
        (
            "VAL4283_10_no_claim_rows",
            all(row.get("claim_allowed", "False") == "False" and row.get("valid_for_claim", "False") == "False" for row in generated_rows),
            "all generated rows remain nonclaim",
        ),
    ]
    for name, path in paths.items():
        validations.append((f"VAL4283_csv_{name}", bool(csv_rows(path)), f"{path.name} parses"))
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
        "sources": SOURCE_DIR / "P8_Y5_R2FR_4283_SOURCE_REGISTER.csv",
        "boundary": SOURCE_DIR / "P8_Y5_R2FR_4283_BOUNDARY_TOPOLOGICAL_AUDIT.csv",
        "noflux": SOURCE_DIR / "P8_Y5_R2FR_4283_NOFLUX_SELECTOR_SCOPE.csv",
        "nogo": SOURCE_DIR / "P8_Y5_R2FR_4283_SUPERPOTENTIAL_NO_GO.csv",
        "runner_inputs": SOURCE_DIR / "P8_Y5_R2FR_4283_SHELL_PROFILE_RUNNER_INPUTS.csv",
        "runner_results": SOURCE_DIR / "P8_Y5_R2FR_4283_SHELL_PROFILE_RUNNER_RESULTS.csv",
        "decision": SOURCE_DIR / "P8_Y5_R2FR_4283_DECISION.csv",
        "firewall": SOURCE_DIR / "P8_Y5_R2FR_4283_CLAIM_FIREWALL.csv",
        "status": SOURCE_DIR / "P8_Y5_R2FR_4283_STATUS.csv",
        "next_target": SOURCE_DIR / "P8_Y5_R2FR_4283_NEXT_TARGET.csv",
    }
    write_csv(paths["sources"], source_rows())
    write_csv(paths["boundary"], boundary_audit_rows())
    write_csv(paths["noflux"], noflux_scope_rows())
    write_csv(paths["nogo"], superpotential_no_go_rows())
    write_csv(paths["runner_inputs"], runner_input_rows())
    write_csv(paths["runner_results"], runner_result_rows())
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
        "PPC4161 4283 boundary/topological fork resolved",
        "4283 resolves the transition-shell boundary/topological fork: generic superpotential/topological ownership fails as a derivation, while 192 no-flux remains valid only for support-separated compact collars. The project must now compute real shell profiles or introduce a genuinely new parent Ward/cohomology mechanism.",
    )
    append_unique_block(
        FORMAL / "180-PPC4161-private-local-packet-integration.md",
        PACKET_MARKER,
        "4283 packet shell-profile runner",
        "Packet update: boundary/topological generic shell closure failed. The finite shell-profile runner interface is ready, with live rows blocked until q_tr, Sigma_metric, AJ, boundary and Kperp profiles are sourced.",
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

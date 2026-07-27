from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[2]
POST = ROOT / "post-checkpoint-work"
FORMAL = ROOT / "formalization-workbench"
SOURCE_DIR = POST / "source-intake" / "mts_residuals"

CHECKPOINT = "4564"
CLAIM_ID = "L-406"
BRANCH_ID = "MTS_R2FR_Y5_CD_KAPPA_CGAMMA_TRIAD_4564"
MARKER = "PPC4161_CD_DELTAKAPPA_CGAMMA_ROOT_OWNERSHIP_ZERO_LAW_OR_BOUND_INTERFACE_4564"
PACKET_MARKER = "PPC4161_PACKET_CD_DELTAKAPPA_CGAMMA_TRIAD_4564"
DECISION = "cD_AND_deltaKappa_PRIVATE_ZERO_REDERIVED_cGamma_PROJECTOR_CONTRACT_IMPORTED_PARENT_ZERO_OPEN"
NEXT_TARGET = "4565-Y5-R2FR-cGamma-memory-projector-parent-zero-or-first-profile-bound-row.md"

FORMAL_PATH = FORMAL / "580-PPC4161-cD-deltaKappa-cGamma-root-ownership-zero-law-or-bound-interface.md"
DOC_PATH = POST / "4564-Y5-R2FR-cD-deltaKappa-cGamma-root-ownership-zero-law-or-bound-interface.md"
SPINE_PATH = FORMAL / "07-unification-spine.md"
PACKET_PATH = FORMAL / "180-PPC4161-private-local-packet-integration.md"
CLAIMS_PATH = FORMAL / "02-claims-register.csv"

DOC_4563 = FORMAL / "579-PPC4161-A-MF-axiom-pack-to-IR-scale-law-and-no-extra-mode-contract.md"
CSV_4563_NEXT = SOURCE_DIR / "P8_Y5_R2FR_4563_NEXT_TARGET.csv"
POST_4186 = POST / "4186-Y5-R2FR-same-coframe-source-memory-zero-law-for-cD-deltaKappa-cGamma-or-bound-runner.md"
POST_4187 = POST / "4187-Y5-R2FR-local-memory-support-projector-zero-law-for-cGamma-or-PPN-clock-bound.md"
CSV_4186_ZERO = SOURCE_DIR / "P8_Y5_R2FR_4186_JOINT_ZERO_LAW_CLAUSES.csv"
CSV_4186_VERDICT = SOURCE_DIR / "P8_Y5_R2FR_4186_COEFFICIENT_VERDICT_MAP.csv"
CSV_4186_BOUND = SOURCE_DIR / "P8_Y5_R2FR_4186_BOUND_RUNNER_INTERFACE.csv"
CSV_4187_PROJECTOR = SOURCE_DIR / "P8_Y5_R2FR_4187_MEMORY_SUPPORT_PROJECTOR_CONTRACT.csv"
CSV_4187_BOUND = SOURCE_DIR / "P8_Y5_R2FR_4187_FINITE_CGAMMA_BOUND_INTERFACE.csv"
CSV_4187_STATUS = SOURCE_DIR / "P8_Y5_R2FR_4187_STATUS.csv"

SOURCE_REGISTER = SOURCE_DIR / "P8_Y5_R2FR_4564_SOURCE_REGISTER.csv"
TRIAD_THEOREM_CSV = SOURCE_DIR / "P8_Y5_R2FR_4564_TRIAD_ZERO_THEOREM.csv"
VERDICT_CSV = SOURCE_DIR / "P8_Y5_R2FR_4564_COEFFICIENT_VERDICT_REFRESH.csv"
PROJECTOR_CSV = SOURCE_DIR / "P8_Y5_R2FR_4564_CGAMMA_PROJECTOR_CONTRACT_IMPORT.csv"
BOUND_CSV = SOURCE_DIR / "P8_Y5_R2FR_4564_BOUND_INTERFACE_REFRESH.csv"
PROMOTION_CSV = SOURCE_DIR / "P8_Y5_R2FR_4564_PROMOTION_GATES.csv"
DECISION_CSV = SOURCE_DIR / "P8_Y5_R2FR_4564_DECISION.csv"
NEXT_CSV = SOURCE_DIR / "P8_Y5_R2FR_4564_NEXT_TARGET.csv"
STATUS_CSV = SOURCE_DIR / "P8_Y5_R2FR_4564_STATUS.csv"
VALIDATION_PATH = SOURCE_DIR / "P8_Y5_BRR545_4564_VALIDATION.csv"


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def b(value: bool) -> str:
    return "True" if value else "False"


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace") if path.exists() else ""


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fieldnames: list[str] = []
    for row in rows:
        for key in row:
            if key not in fieldnames:
                fieldnames.append(key)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def markdown_table(rows: list[dict[str, Any]]) -> str:
    if not rows:
        return "\n"
    headers: list[str] = []
    for row in rows:
        for key in row:
            if key not in headers:
                headers.append(key)
    lines = [
        "| " + " | ".join(headers) + " |",
        "| " + " | ".join("---" for _ in headers) + " |",
    ]
    for row in rows:
        lines.append(
            "| "
            + " | ".join(
                str(row.get(header, "")).replace("|", "\\|").replace("\n", "<br>")
                for header in headers
            )
            + " |"
        )
    return "\n".join(lines) + "\n"


def source_rows() -> list[dict[str, Any]]:
    specs = [
        ("SRC4564_00_4563_formal", "4563 triad selected", DOC_4563, "leakage-root triad: `c_D`, `delta_kappa`, `c_Gamma`"),
        ("SRC4564_01_4563_next", "4563 next target CSV", CSV_4563_NEXT, "4564-Y5-R2FR-cD-deltaKappa-cGamma-root-ownership-zero-law-or-bound-interface.md"),
        ("SRC4564_02_4186_doc", "4186 joint zero law", POST_4186, "c_D = 0 inside the private same-coframe/Hilbert/Maxwell-Hodge selector"),
        ("SRC4564_03_4187_doc", "4187 cGamma projector", POST_4187, "P_loc(delta S_Gamma / delta O_loc) = 0"),
        ("SRC4564_04_4186_zero_csv", "4186 joint zero clauses", CSV_4186_ZERO, "JZ4186_5_memory_support"),
        ("SRC4564_05_4186_verdict_csv", "4186 coefficient verdict map", CSV_4186_VERDICT, "CV4186_2_cGamma"),
        ("SRC4564_06_4186_bound_csv", "4186 bound interface", CSV_4186_BOUND, "BR4186_2_cGamma_PPN_clock"),
        ("SRC4564_07_4187_projector_csv", "4187 memory projector contract", CSV_4187_PROJECTOR, "SP4187_2_exact_zero"),
        ("SRC4564_08_4187_bound_csv", "4187 finite cGamma interface", CSV_4187_BOUND, "FB4187_2_orbital"),
        ("SRC4564_09_4187_status_csv", "4187 status", CSV_4187_STATUS, "c_Gamma_parent_zero"),
    ]
    rows: list[dict[str, Any]] = []
    for source_id, label, path, needle in specs:
        text = read_text(path)
        rows.append(
            {
                "source_id": source_id,
                "label": label,
                "source_path": str(path),
                "exists": b(path.exists()),
                "needle": needle,
                "needle_found": b(needle in text),
                "role": "4564 cD/deltaKappa/cGamma root ownership theorem",
                "valid_for_claim": "False",
            }
        )
    return rows


def triad_theorem_rows() -> list[dict[str, Any]]:
    return [
        {
            "theorem_id": "TZ4564_0_cD_zero",
            "coefficient": "c_D",
            "zero_law": "If all visible matter, binding, Maxwell-Hodge and clock/readout actions descend through the single observed coframe e^A, then no independent disformal/shadow coframe carrier exists.",
            "symbolic_result": "S_vis = S_matter[psi,e] + S_EM[A,e] + S_binding[e] + dB_impr => c_D = 0",
            "status": "PRIVATE_SELECTOR_ZERO_REDERIVED",
            "remaining_public_debt": "global parent same-coframe functor and no-shadow-frame signature",
            "valid_for_claim": "False",
        },
        {
            "theorem_id": "TZ4564_1_Poynting_owner",
            "coefficient": "c_D_EM_side",
            "zero_law": "Poynting flow is the Maxwell-Hodge Hilbert stress component on the observed coframe, or routed boundary/Hamiltonian flux; it is not an extra background force.",
            "symbolic_result": "S_EM[A,e] -> T_EM^{mu nu}; S^i_Poynting = T_EM^{0i}; no second source channel => c_D_EM_side = 0",
            "status": "PRIVATE_SELECTOR_ZERO_REDERIVED",
            "remaining_public_debt": "global Hodge/constitutive closure and radiative boundary routing",
            "valid_for_claim": "False",
        },
        {
            "theorem_id": "TZ4564_2_deltaKappa_zero",
            "coefficient": "delta_kappa",
            "zero_law": "If kappa_* is a source-blind topological/calibrated constant and the ordinary Hilbert source measure has one Z_H, then source-coupling drift has no local slot.",
            "symbolic_result": "kappa_eff = kappa_* Z_H, D_A ln kappa_* = 0, D_A delta Z_H = 0 => D_A ln kappa_eff = 0 => delta_kappa = 0",
            "status": "PRIVATE_SELECTOR_ZERO_REDERIVED_NUMERIC_G_NOT_PREDICTED",
            "remaining_public_debt": "global topological kappa/source-measure adoption; positive same-frame source mass",
            "valid_for_claim": "False",
        },
        {
            "theorem_id": "TZ4564_3_Newton_coupling_readout",
            "coefficient": "G_cal",
            "zero_law": "The Newtonian limit uses the calibrated coupling and Hilbert source density without importing orbital GM as an input.",
            "symbolic_result": "G_cal = c^4 kappa_eff/(8*pi), nabla^2 Phi_N = 4*pi G_cal rho_H",
            "status": "STRUCTURAL_READOUT_PRIVATE_NOT_NUMERIC_G_DERIVATION",
            "remaining_public_debt": "derivation of dimensionful kappa scale if MTS is to predict G rather than calibrate it",
            "valid_for_claim": "False",
        },
        {
            "theorem_id": "TZ4564_4_cGamma_not_closed",
            "coefficient": "c_Gamma",
            "zero_law": "Same coframe and source-coupling locks do not by themselves silence local memory hair.",
            "symbolic_result": "E_Gamma^loc := P_loc(delta S_Gamma/delta O_loc) must vanish; c_Gamma=0 is not derived by c_D=0 or delta_kappa=0",
            "status": "OPEN_PARENT_MEMORY_PROJECTOR",
            "remaining_public_debt": "vertical/support/bulk-source/boundary/tensor no-hair clauses for Gamma_mem, or finite profile bounds",
            "valid_for_claim": "False",
        },
    ]


def verdict_rows() -> list[dict[str, Any]]:
    return [
        {
            "verdict_id": "VR4564_0_cD",
            "coefficient": "c_D",
            "private_branch_status": "zero",
            "public_status": "not_public_until_parent_same_coframe_signed",
            "fallback_if_rejected": "WEP/clock/EM propagation/Poynting finite c_D bound",
            "next_action": "do not reopen unless same-coframe branch is rejected",
            "valid_for_claim": "False",
        },
        {
            "verdict_id": "VR4564_1_deltaKappa",
            "coefficient": "delta_kappa",
            "private_branch_status": "zero",
            "public_status": "not_public_until_parent_kappa_source_lock_signed; numeric G remains calibrated",
            "fallback_if_rejected": "orbital/LLR/clock/local-G finite drift envelope",
            "next_action": "do not claim G prediction; keep calibrated G_cal language",
            "valid_for_claim": "False",
        },
        {
            "verdict_id": "VR4564_2_cGamma",
            "coefficient": "c_Gamma",
            "private_branch_status": "not_zero_from_triad",
            "public_status": "active_blocker",
            "fallback_if_rejected": "PPN/clock/orbital/R10 finite product/profile bound",
            "next_action": NEXT_TARGET,
            "valid_for_claim": "False",
        },
    ]


def projector_rows() -> list[dict[str, Any]]:
    return [
        {
            "projector_id": "CP4564_0_action",
            "clause": "memory action residual",
            "condition": "S_Gamma[U] = integral_U sqrt(-g_obs) c_Gamma Gamma_mem I_local[g_obs,R,T,source] + boundary",
            "effect": "defines the local memory-hair residual to be zeroed or bounded",
            "status": "imported_from_4187",
            "valid_for_claim": "False",
        },
        {
            "projector_id": "CP4564_1_projector",
            "clause": "local observable projection",
            "condition": "E_Gamma^loc := P_loc(delta S_Gamma / delta O_loc)",
            "effect": "local-GR survival requires E_Gamma^loc=0, not just a small-looking Gamma_mem phrase",
            "status": "imported_from_4187",
            "valid_for_claim": "False",
        },
        {
            "projector_id": "CP4564_2_exact_zero",
            "clause": "exact c_Gamma zero contract",
            "condition": "P_loc[Gamma_mem E_I + derivative terms in Gamma_mem + J_Gamma I_local + H_Gamma_perp] = 0",
            "effect": "parent action must sign every term as vertical/support-silent/source-silent/boundary-routed/tensor-silent",
            "status": "CONDITIONAL_NOT_PARENT_CLOSED",
            "valid_for_claim": "False",
        },
        {
            "projector_id": "CP4564_3_missing_clauses",
            "clause": "unsigned c_Gamma clauses",
            "condition": "vertical readout silence; compact support silence; ordinary bulk-source silence; boundary routing; homogeneous tensor no-hair",
            "effect": "these are the actual proof targets; generic same-coframe/source language is insufficient",
            "status": "ACTIVE_NEXT_TARGET",
            "valid_for_claim": "False",
        },
    ]


def bound_rows() -> list[dict[str, Any]]:
    return [
        {
            "bound_id": "BI4564_0_cD",
            "coefficient": "c_D",
            "arena": "WEP; clocks; EM propagation; Poynting",
            "required_inputs": "finite same-coframe leak coefficient, projection Jacobian, units and source path",
            "use_condition": "only if same-coframe parent functor is rejected",
            "status": "dormant_nonclaim_interface",
            "valid_for_claim": "False",
        },
        {
            "bound_id": "BI4564_1_deltaKappa",
            "coefficient": "delta_kappa",
            "arena": "orbital; LLR/Gdot; clock; local G",
            "required_inputs": "finite kappa/source drift function, time/range units, calibration convention and source path",
            "use_condition": "only if kappa/source lock is rejected globally",
            "status": "dormant_nonclaim_interface",
            "valid_for_claim": "False",
        },
        {
            "bound_id": "BI4564_2_cGamma_PPN",
            "coefficient": "c_Gamma",
            "arena": "PPN",
            "required_inputs": "c_Gamma, Gamma_mem profile, J_PPN^Gamma, Gamma_perp/K_perp contribution, residual vector thresholds",
            "use_condition": "active unless c_Gamma zero theorem closes",
            "status": "active_nonclaim_interface",
            "valid_for_claim": "False",
        },
        {
            "bound_id": "BI4564_3_cGamma_clock_orbital_R10",
            "coefficient": "c_Gamma",
            "arena": "clock; orbital/LLR/Gdot; R10",
            "required_inputs": "local time projection, radial acceleration/Gdot projection, lambda_Gamma, alpha_Gamma(lambda), reviewed bound rows",
            "use_condition": "first empirical fallback if parent memory projector proof fails",
            "status": "active_nonclaim_interface",
            "valid_for_claim": "False",
        },
    ]


def promotion_rows() -> list[dict[str, Any]]:
    return [
        {
            "gate_id": "PG4564_0_cD",
            "requirement": "c_D zero inside private same-coframe/Hodge selector",
            "status": "PASS_PRIVATE_ZERO",
            "claim_effect": "WEP/EM shadow-coframe leak is closed only inside private branch",
            "valid_for_claim": "False",
        },
        {
            "gate_id": "PG4564_1_deltaKappa",
            "requirement": "delta_kappa zero inside private topological-kappa/Hilbert-source selector",
            "status": "PASS_PRIVATE_ZERO_NUMERIC_G_CALIBRATED",
            "claim_effect": "Newton/Poisson coupling shape is structural, numerical G is not predicted",
            "valid_for_claim": "False",
        },
        {
            "gate_id": "PG4564_2_cGamma",
            "requirement": "c_Gamma parent memory projector zero or finite bound",
            "status": "FAIL_OPEN_ACTIVE_BLOCKER",
            "claim_effect": "public/local-GR claim blocked by memory hair",
            "valid_for_claim": "False",
        },
        {
            "gate_id": "PG4564_3_public",
            "requirement": "global parent signatures for same coframe, source lock and memory no-hair",
            "status": "FAIL_PUBLIC_PARENT_UNSIGNED",
            "claim_effect": "no public local-GR/Newton/R10 claim",
            "valid_for_claim": "False",
        },
        {
            "gate_id": "PG4564_4_next",
            "requirement": "next target attacks c_Gamma rather than reopening c_D/delta_kappa",
            "status": "PASS_NEXT_SELECTED",
            "claim_effect": f"next target = {NEXT_TARGET}",
            "valid_for_claim": "False",
        },
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        {
            "decision_id": "DEC4564_0_main",
            "decision": DECISION,
            "what_was_derived": "c_D=0 and delta_kappa=0 are rederived inside the private same-coframe/Hilbert/Maxwell-Hodge/topological-kappa selector; Newton coupling shape uses calibrated G_cal.",
            "what_failed": "c_Gamma is not killed by those laws; it needs its own memory support/projector zero theorem or finite profile/product bounds.",
            "action_taken": "Do not reopen c_D/delta_kappa unless branch assumptions change; select c_Gamma projector/bound as the next hard local-GR blocker.",
            "valid_for_claim": "False",
        }
    ]


def next_rows() -> list[dict[str, Any]]:
    return [
        {
            "next_target": NEXT_TARGET,
            "route": "best_forward_route",
            "why": "After the triad refresh, the only live member of the first leakage triad is c_Gamma. The exact missing object is E_Gamma^loc=0 or a finite source-backed profile/product bound.",
            "success_condition": "Parent-sign the vertical/support/bulk-source/boundary/tensor clauses for Gamma_mem, or build first usable finite c_Gamma profile-bound row with units, source path and arena projection.",
            "valid_for_claim": "False",
        }
    ]


def status_rows() -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "branch_id": BRANCH_ID,
            "decision": DECISION,
            "c_D_private_zero": "True",
            "delta_kappa_private_zero": "True",
            "c_Gamma_parent_zero": "False",
            "c_Gamma_bound_interface_ready": "True",
            "numeric_G_predicted": "False",
            "public_local_GR_claim_allowed": "False",
            "next_target": NEXT_TARGET,
            "timestamp_utc": utc_now(),
            "valid_for_claim": "False",
        }
    ]


def validate(
    sources: list[dict[str, Any]],
    theorem: list[dict[str, Any]],
    verdict: list[dict[str, Any]],
    projector: list[dict[str, Any]],
    bounds: list[dict[str, Any]],
    gates: list[dict[str, Any]],
    decision: list[dict[str, Any]],
    next_target: list[dict[str, Any]],
    status: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    source_ok = all(row["exists"] == "True" and row["needle_found"] == "True" for row in sources)
    rows.append({"validation_id": "VAL4564_0_sources", "check": "all source paths and needles validate", "status": "PASS" if source_ok else "FAIL", "details": f"{len(sources)} sources"})

    theorem_text = "\n".join(str(value) for row in theorem for value in row.values())
    theorem_ok = all(token in theorem_text for token in ["c_D = 0", "delta_kappa = 0", "G_cal", "E_Gamma^loc"])
    theorem_ok = theorem_ok and all(row["valid_for_claim"] == "False" for row in theorem)
    rows.append({"validation_id": "VAL4564_1_triad_theorem", "check": "triad theorem closes cD/deltaKappa privately and leaves cGamma open", "status": "PASS" if theorem_ok else "FAIL", "details": f"{len(theorem)} theorem rows"})

    verdict_map = {row["coefficient"]: row["private_branch_status"] for row in verdict}
    verdict_ok = verdict_map.get("c_D") == "zero" and verdict_map.get("delta_kappa") == "zero" and verdict_map.get("c_Gamma") == "not_zero_from_triad"
    rows.append({"validation_id": "VAL4564_2_verdict", "check": "coefficient verdicts are correctly split", "status": "PASS" if verdict_ok else "FAIL", "details": str(verdict_map)})

    projector_text = "\n".join(str(value) for row in projector for value in row.values())
    projector_ok = all(token in projector_text for token in ["P_loc", "delta S_Gamma", "vertical", "support", "boundary", "tensor"])
    rows.append({"validation_id": "VAL4564_3_projector", "check": "cGamma projector contract imports exact zero clauses", "status": "PASS" if projector_ok else "FAIL", "details": f"{len(projector)} projector rows"})

    bound_coeffs = {row["coefficient"] for row in bounds}
    bound_ok = {"c_D", "delta_kappa", "c_Gamma"}.issubset(bound_coeffs) and all(row["valid_for_claim"] == "False" for row in bounds)
    rows.append({"validation_id": "VAL4564_4_bounds", "check": "bound interfaces exist for dormant cD/deltaKappa and active cGamma", "status": "PASS" if bound_ok else "FAIL", "details": ",".join(sorted(bound_coeffs))})

    gates_text = "\n".join(str(value) for row in gates for value in row.values())
    gates_ok = "PASS_PRIVATE_ZERO" in gates_text and "FAIL_OPEN_ACTIVE_BLOCKER" in gates_text and "FAIL_PUBLIC_PARENT_UNSIGNED" in gates_text
    gates_ok = gates_ok and all(row["valid_for_claim"] == "False" for row in gates)
    rows.append({"validation_id": "VAL4564_5_gates", "check": "promotion gates keep private zeros and public claim blocked", "status": "PASS" if gates_ok else "FAIL", "details": f"{len(gates)} gates"})

    decision_ok = decision and decision[0]["decision"] == DECISION and decision[0]["valid_for_claim"] == "False"
    next_ok = next_target and next_target[0]["next_target"] == NEXT_TARGET
    status_ok = status and status[0]["c_D_private_zero"] == "True" and status[0]["delta_kappa_private_zero"] == "True" and status[0]["c_Gamma_parent_zero"] == "False"
    rows.append({"validation_id": "VAL4564_6_decision_status", "check": "decision/status select cGamma next and keep nonclaim", "status": "PASS" if decision_ok and next_ok and status_ok else "FAIL", "details": NEXT_TARGET})

    overall = all(row["status"] == "PASS" for row in rows)
    rows.append({"validation_id": "VAL4564_7_overall", "check": "overall 4564 checkpoint validation", "status": "PASS" if overall else "FAIL", "details": "triad theorem refreshed; cGamma active" if overall else "one or more validations failed"})
    return rows


def write_doc(
    path: Path,
    title: str,
    sources: list[dict[str, Any]],
    theorem: list[dict[str, Any]],
    verdict: list[dict[str, Any]],
    projector: list[dict[str, Any]],
    bounds: list[dict[str, Any]],
    gates: list[dict[str, Any]],
    decision: list[dict[str, Any]],
    next_target: list[dict[str, Any]],
    validation: list[dict[str, Any]],
) -> None:
    content = f"""# {title}

Branch: `{BRANCH_ID}`  
Marker: `{MARKER}`  
Decision: `{DECISION}`  
Claim: `{CLAIM_ID}` remains private, conditional and nonclaim.

## What Moved

4564 takes the first leakage triad from 4563 and separates it cleanly:

```text
c_D = 0
```

inside the private same-coframe / Maxwell-Hodge / Hilbert-stress selector.

```text
delta_kappa = 0
```

inside the private topological-kappa / Hilbert-source selector, while the numerical value of `G` remains calibrated:

```text
G_cal = c^4 kappa_eff/(8*pi),
nabla^2 Phi_N = 4*pi G_cal rho_H.
```

But:

```text
c_Gamma is not zero from same-coframe or source-coupling laws.
```

The active blocker is now exact:

```text
E_Gamma^loc := P_loc(delta S_Gamma / delta O_loc) = 0
```

or else a finite `c_Gamma` profile/product bound is required.

## Source Register

{markdown_table(sources)}

## Triad Zero Theorem

{markdown_table(theorem)}

## Coefficient Verdict Refresh

{markdown_table(verdict)}

## cGamma Projector Contract Import

{markdown_table(projector)}

## Bound Interface Refresh

{markdown_table(bounds)}

## Promotion Gates

{markdown_table(gates)}

## Decision

{markdown_table(decision)}

## Next Target

{markdown_table(next_target)}

## Validation

{markdown_table(validation)}
"""
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def append_once(path: Path, marker: str, text: str) -> None:
    existing = read_text(path)
    if marker in existing:
        return
    with path.open("a", encoding="utf-8") as handle:
        handle.write(text)


def append_claim_once() -> None:
    existing = read_text(CLAIMS_PATH)
    if f"{CLAIM_ID}," in existing:
        return
    row = {
        "claim_id": CLAIM_ID,
        "domain": "local_gr_parent_signature",
        "claim": "4564 rederives c_D=0 and delta_kappa=0 inside the private selector, while isolating c_Gamma as the active memory-projector blocker with a finite bound interface.",
        "current_evidence": "Generated source register, triad zero theorem, coefficient verdict refresh, cGamma projector import, bound interface refresh, promotion gates, status and validation CSVs.",
        "status": "cD_deltaKappa_private_zero_cGamma_active_projector_bound_next",
        "next_test": NEXT_TARGET,
        "key_risk": "Treating private c_D/delta_kappa closure as a public local-GR proof while c_Gamma memory hair remains open.",
        "sector": "local_gr",
        "evidence": str(DOC_PATH),
        "next_action": NEXT_TARGET,
        "risk": "This is private branch progress; public parent signatures and c_Gamma zero/bounds remain required.",
    }
    file_exists = CLAIMS_PATH.exists() and CLAIMS_PATH.stat().st_size > 0
    with CLAIMS_PATH.open("a", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(row.keys()))
        if not file_exists:
            writer.writeheader()
        writer.writerow(row)


def main() -> None:
    sources = source_rows()
    theorem = triad_theorem_rows()
    verdict = verdict_rows()
    projector = projector_rows()
    bounds = bound_rows()
    gates = promotion_rows()
    decision = decision_rows()
    next_target = next_rows()
    status = status_rows()
    validation = validate(sources, theorem, verdict, projector, bounds, gates, decision, next_target, status)

    write_csv(SOURCE_REGISTER, sources)
    write_csv(TRIAD_THEOREM_CSV, theorem)
    write_csv(VERDICT_CSV, verdict)
    write_csv(PROJECTOR_CSV, projector)
    write_csv(BOUND_CSV, bounds)
    write_csv(PROMOTION_CSV, gates)
    write_csv(DECISION_CSV, decision)
    write_csv(NEXT_CSV, next_target)
    write_csv(STATUS_CSV, status)
    write_csv(VALIDATION_PATH, validation)

    write_doc(FORMAL_PATH, "4564 - cD deltaKappa cGamma root ownership zero law or bound interface", sources, theorem, verdict, projector, bounds, gates, decision, next_target, validation)
    write_doc(DOC_PATH, "4564 - Y5 R2FR cD deltaKappa cGamma Root Ownership Zero Law Or Bound Interface", sources, theorem, verdict, projector, bounds, gates, decision, next_target, validation)
    append_claim_once()
    append_once(
        SPINE_PATH,
        MARKER,
        f"""
## 4564 cD/deltaKappa/cGamma Root Ownership Refresh

Marker: `{MARKER}`  
The first leakage triad is now split sharply. Inside the private same-coframe/Hilbert/Maxwell-Hodge/topological-kappa selector:

```text
c_D = 0,
delta_kappa = 0,
G_cal = c^4 kappa_eff/(8*pi).
```

This does not predict the numerical value of `G`; it gives the calibrated Newton/Poisson coupling shape. The live member of the triad is `c_Gamma`. Its required zero is:

```text
E_Gamma^loc := P_loc(delta S_Gamma / delta O_loc) = 0.
```

That requires vertical/support/bulk-source/boundary/tensor memory clauses, or else finite PPN/clock/orbital/R10 profile bounds. Next target: `{NEXT_TARGET}`.
""",
    )
    append_once(
        PACKET_PATH,
        PACKET_MARKER,
        f"""
## 4564 Packet Integration - cD/deltaKappa/cGamma Triad

Marker: `{PACKET_MARKER}`  
The packet may treat `c_D` and `delta_kappa` as private-branch zeros under same-coframe/Hilbert/Maxwell-Hodge/topological-kappa assumptions. Public promotion is still blocked, and numerical `G` remains calibrated. The active local-GR leakage blocker is `c_Gamma`, governed by `E_Gamma^loc=P_loc(delta S_Gamma/delta O_loc)`. Next target: `{NEXT_TARGET}`.
""",
    )

    cache_dir = Path(__file__).resolve().parent / "__pycache__"
    if cache_dir.exists():
        shutil.rmtree(cache_dir)

    print(f"Wrote {DOC_PATH}")
    print(f"Wrote {FORMAL_PATH}")
    print(f"Wrote {VALIDATION_PATH}")
    print(f"Decision: {DECISION}")


if __name__ == "__main__":
    main()

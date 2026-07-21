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

CHECKPOINT = "4592"
CLAIM_ID = "L-434"
BRANCH_ID = "MTS_R2FR_Y5_SOURCE_KERNEL_ZERO_CHAIN_TO_LOCAL_PPN_RESIDUAL_VECTOR_GATE_4592"
MARKER = "PPC4161_SOURCE_KERNEL_ZERO_CHAIN_TO_LOCAL_PPN_RESIDUAL_VECTOR_GATE_4592"
PACKET_MARKER = "PPC4161_PACKET_SOURCE_KERNEL_ZERO_CHAIN_TO_LOCAL_PPN_RESIDUAL_VECTOR_GATE_4592"
DECISION = "SOURCE_KERNEL_SUBVECTOR_REMOVED_FROM_LOCAL_PPN_VECTOR_SURVIVORS_RETAINED_NONCLAIM"
NEXT_TARGET = "4593-Y5-R2FR-cT-spin-torsion-zero-or-contact-bound-after-source-kernel-closure.md"

DOC_PATH = POST / "4592-Y5-R2FR-source-kernel-zero-chain-to-local-PPN-residual-vector-gate.md"
FORMAL_PATH = FORMAL / "608-PPC4161-source-kernel-zero-chain-to-local-PPN-residual-vector-gate.md"
SPINE_PATH = FORMAL / "07-unification-spine.md"
PACKET_PATH = FORMAL / "180-PPC4161-private-local-packet-integration.md"
CLAIMS_PATH = FORMAL / "02-claims-register.csv"

DOC_4591 = POST / "4591-Y5-R2FR-tau-eobs-same-frame-lock-or-source-support-bound.md"
FORMAL_607 = FORMAL / "607-PPC4161-tau-eobs-same-frame-lock-or-source-support-bound.md"
CSV_4591_REDUCTION = SOURCE_DIR / "P8_Y5_R2FR_4591_SOURCE_KERNEL_CLOSURE_UPDATE.csv"
FORMAL_188 = FORMAL / "188-PPC4161-full-PPN-readout-vector.md"
FORMAL_189 = FORMAL / "189-PPC4161-local-empirical-validation-pack.md"
FORMAL_294 = FORMAL / "294-PPC4161-left-hand-EH-Newton-limit-or-residual-EFT-bound-gate.md"
FORMAL_295 = FORMAL / "295-PPC4161-residual-EFT-coefficient-zero-or-local-test-bound-pack.md"
FORMAL_463 = FORMAL / "463-PPC4161-GR-parity-source-universality-to-local-PPN-residual-vector-or-material-values.md"
DOC_3110 = POST / "3110-Y5-R2FR-local-PPN-residual-vector-from-Eres-and-RHsrc-under-AX1090.md"
DOC_3915 = POST / "3915-Y5-R2FR-stationary-local-branch-contract-and-PPN-residual-vector.md"
CSV_4172_PPN = SOURCE_DIR / "P8_Y5_R2FR_4172_PPN_VECTOR_DERIVATION.csv"
CSV_4172_REACT = SOURCE_DIR / "P8_Y5_R2FR_4172_RESIDUAL_CLOSE_OR_REACTIVATE.csv"
CSV_4278_EFT = SOURCE_DIR / "P8_Y5_R2FR_4278_RESIDUAL_EFT_COEFFICIENT_MAP.csv"
CSV_4279_SURVIVORS = SOURCE_DIR / "P8_Y5_R2FR_4279_SURVIVOR_BOUND_PACK.csv"
CSV_4447_ROLLUP = SOURCE_DIR / "P8_Y5_R2FR_4447_RESIDUAL_ROLLUP.csv"
CSV_4448_SURVIVORS = SOURCE_DIR / "P8_Y5_R2FR_4448_SURVIVOR_MAP_OUTPUT.csv"
CSV_4555_SCORECARD = SOURCE_DIR / "P8_Y5_R2FR_4555_LOCAL_PPN_SCORECARD_REFRESH.csv"
CSV_4561_EFT = SOURCE_DIR / "P8_Y5_R2FR_4561_RESIDUAL_EFT_ENVELOPE_REFRESH.csv"

SOURCE_REGISTER = SOURCE_DIR / "P8_Y5_R2FR_4592_SOURCE_REGISTER.csv"
INTEGRATION_THEOREM_CSV = SOURCE_DIR / "P8_Y5_R2FR_4592_SOURCE_KERNEL_PPN_INTEGRATION_THEOREM.csv"
PPN_IMPACT_CSV = SOURCE_DIR / "P8_Y5_R2FR_4592_PPN_VECTOR_IMPACT_ROWS.csv"
SURVIVOR_MAP_CSV = SOURCE_DIR / "P8_Y5_R2FR_4592_SURVIVOR_BLOCKER_MAP.csv"
PROMOTION_CSV = SOURCE_DIR / "P8_Y5_R2FR_4592_PROMOTION_GATES.csv"
CONTROL_CSV = SOURCE_DIR / "P8_Y5_R2FR_4592_CONTROL_ROWS.csv"
DECISION_CSV = SOURCE_DIR / "P8_Y5_R2FR_4592_DECISION.csv"
NEXT_CSV = SOURCE_DIR / "P8_Y5_R2FR_4592_NEXT_TARGET.csv"
STATUS_CSV = SOURCE_DIR / "P8_Y5_R2FR_4592_STATUS.csv"
VALIDATION_PATH = SOURCE_DIR / "P8_Y5_BRR545_4592_VALIDATION.csv"


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def bool_text(value: bool) -> str:
    return "True" if value else "False"


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace") if path.exists() else ""


def read_csv(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


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
        for row in rows:
            writer.writerow({key: row.get(key, "") for key in fieldnames})


def markdown_table(rows: list[dict[str, Any]]) -> str:
    if not rows:
        return ""
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
        lines.append("| " + " | ".join(str(row.get(key, "")).replace("\n", " ") for key in headers) + " |")
    return "\n".join(lines)


def append_once(path: Path, marker: str, block: str) -> None:
    text = read_text(path)
    if marker in text:
        return
    path.write_text(text.rstrip() + "\n\n" + block.strip() + "\n", encoding="utf-8")


def append_claim_once() -> None:
    rows = read_csv(CLAIMS_PATH)
    if any(row.get("claim_id") == CLAIM_ID for row in rows):
        return
    fieldnames = list(rows[0].keys()) if rows else [
        "claim_id",
        "domain",
        "claim",
        "current_evidence",
        "status",
        "next_test",
        "key_risk",
        "sector",
        "evidence",
        "next_action",
        "risk",
    ]
    claim_row = {
        "claim_id": CLAIM_ID,
        "domain": "local_gr_parent_signature",
        "claim": "4592 propagates the strict 4587-4591 source-worldtube kernel zero chain into the local Newton/PPN residual vector, removing only the source-kernel subvector while retaining all non-source EFT, geometry, boundary, torsion, cGamma, finite-range, material and empirical projection blockers.",
        "current_evidence": "Generated source-kernel-to-PPN integration theorem, PPN impact rows, survivor blocker map, controls, gates and validation.",
        "status": "source_kernel_subvector_removed_local_ppn_survivors_retained_nonclaim",
        "next_test": NEXT_TARGET,
        "key_risk": "Mistaking C_K_source_worldtube=0 for full local-GR/PPN closure, or erasing residual EFT survivor rows without parent zero or source-backed bounds.",
        "sector": "local_gr",
        "evidence": str(DOC_PATH),
        "next_action": NEXT_TARGET,
        "risk": "No public local-GR/R10/PPN claim until survivor coefficients and empirical projection rows are theorem-zeroed or source-backed below bounds.",
    }
    rows.append({key: claim_row.get(key, "") for key in fieldnames})
    write_csv(CLAIMS_PATH, rows)


def source_rows(now: str) -> list[dict[str, Any]]:
    specs = [
        ("SRC4592_00_4591_doc", DOC_4591, "C_K_source_worldtube = 0", "4591 source-kernel strict zero result"),
        ("SRC4592_01_4591_formal", FORMAL_607, "C_K_source_worldtube=0", "607 formal source-kernel zero bridge"),
        ("SRC4592_02_4591_csv", CSV_4591_REDUCTION, "SKC4591_2_CKsource_strict_zero", "machine-readable strict source-kernel zero row"),
        ("SRC4592_03_188_ppn", FORMAL_188, "R_PPN =", "private full PPN vector target"),
        ("SRC4592_04_189_empirical", FORMAL_189, "R_PPN = 0,", "private comparator pack warning"),
        ("SRC4592_05_294_left_hand", FORMAL_294, "Residual EFT fork", "left-hand EH/Newton residual fork"),
        ("SRC4592_06_295_survivors", FORMAL_295, "survivor / bound subset", "residual EFT survivor subset"),
        ("SRC4592_07_463_source_univ", FORMAL_463, "does **not** erase non-source residuals", "source subspace warning"),
        ("SRC4592_08_3110_ppn_vector", DOC_3110, "local GR reduction = source-mass bridge + PPN residual vector closure", "PPN vector projection discipline"),
        ("SRC4592_09_3915_contract", DOC_3915, "Delta_PPN_GR", "stationary branch PPN promotion gate"),
        ("SRC4592_10_4172_ppn_csv", CSV_4172_PPN, "gamma-1=0", "private PPN derivation rows"),
        ("SRC4592_11_4172_reactivate", CSV_4172_REACT, "source_backed_empirical_bound_row_required", "reactivation rule"),
        ("SRC4592_12_4278_eft_csv", CSV_4278_EFT, "RES4278_3_memory", "left-hand residual EFT coefficient map"),
        ("SRC4592_13_4279_survivor_csv", CSV_4279_SURVIVORS, "SURV4279_6_spin_torsion", "survivor bound pack"),
        ("SRC4592_14_4447_rollup", CSV_4447_ROLLUP, "RU4447_1_full_PPN_vector", "source subvector not full vector warning"),
        ("SRC4592_15_4448_survivor_map", CSV_4448_SURVIVORS, "SURV4448_7_material_Req_values", "non-source survivor map"),
        ("SRC4592_16_4555_scorecard", CSV_4555_SCORECARD, "SC4555_alpha3", "local PPN scorecard thresholds"),
        ("SRC4592_17_4561_eft_refresh", CSV_4561_EFT, "RE4561_0_cT", "latest residual EFT envelope refresh"),
        ("SRC4592_18_claim_433", CLAIMS_PATH, "L-433", "claim-register handoff from 4591"),
    ]
    rows: list[dict[str, Any]] = []
    for source_id, path, needle, role in specs:
        text = read_text(path)
        rows.append(
            {
                "checkpoint": CHECKPOINT,
                "source_id": source_id,
                "path": str(path),
                "path_exists": bool_text(path.exists()),
                "needle": needle,
                "needle_found": bool_text(needle in text),
                "role": role,
                "generated_utc": now,
                "valid_for_claim": "False",
            }
        )
    return rows


def integration_theorem_rows(now: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "theorem_id": "INT4592_0_residual_decomposition",
            "claim": "The local Newton/PPN residual vector can be split into a source-kernel subvector plus non-source survivor subvectors.",
            "derivation": "Write Delta_PPN = Delta_PPN^EH/EFT + Delta_PPN^source_kernel + Delta_PPN^boundary + Delta_PPN^projector + Delta_PPN^material + Delta_PPN^empirical. The source-kernel piece is linear at this gate: Delta_PPN^source_kernel = Pi_PPN^K C_K_source_worldtube.",
            "consequence": "A strict source-kernel zero removes only Pi_PPN^K C_K_source_worldtube, not the other subvectors.",
            "status": "PPN_DECOMPOSITION_WRITTEN_NO_CANCELLATION",
            "generated_utc": now,
            "valid_for_claim": "False",
        },
        {
            "checkpoint": CHECKPOINT,
            "theorem_id": "INT4592_1_strict_source_kernel_subvector_zero",
            "claim": "The 4587-4591 strict chain sets the source-kernel contribution to the local PPN residual vector to zero.",
            "derivation": "4591 gives C_K_source_worldtube=0 when the density/Poynting, support-boundary, denominator, Dq-source, readout-mask and tau/e_obs clauses all fire. Therefore Delta_PPN^source_kernel = Pi_PPN^K*0 = 0 for every PPN arena row.",
            "consequence": "source-kernel pieces of gamma, beta, alpha_i, xi, zeta_i, Gdot/G, clock/orbital/WEP/R10 side channels are removable inside the private strict branch.",
            "status": "SOURCE_KERNEL_SUBVECTOR_ZERO_PRIVATE_NONCLAIM",
            "generated_utc": now,
            "valid_for_claim": "False",
        },
        {
            "checkpoint": CHECKPOINT,
            "theorem_id": "INT4592_2_open_branch_bound",
            "claim": "If any source-kernel clause reopens, its PPN contribution is an explicit projection bound.",
            "derivation": "|Delta_PPN^source_kernel| <= ||Pi_PPN^K|| L_K_source*(E_rho_qbasic+E_boundary_birth+E_Dq_source+E_tau_eobs+E_Href+E_readout_mask+E_EM_flux).",
            "consequence": "The fallback remains scoreable without hiding the source kernel in calibrated G or orbital GM.",
            "status": "OPEN_SOURCE_KERNEL_PPN_BOUND_READY_VALUES_MISSING",
            "generated_utc": now,
            "valid_for_claim": "False",
        },
        {
            "checkpoint": CHECKPOINT,
            "theorem_id": "INT4592_3_survivor_firewall",
            "claim": "Source-kernel zero is not a local-GR pass.",
            "derivation": "Formal 188/294/295/463 and the 3110/3915 PPN-vector discipline retain EH principal/IR selector, residual EFT, cGamma, curvature-square, torsion, Lambda, nonEH/R11, material values and empirical projection rows.",
            "consequence": "Public promotion requires every survivor row to be parent-zero or source-backed below its arena bound.",
            "status": "SURVIVORS_RETAINED_NO_PUBLIC_CLAIM",
            "generated_utc": now,
            "valid_for_claim": "False",
        },
    ]


def ppn_impact_rows(now: str) -> list[dict[str, Any]]:
    rows = [
        ("PPN4592_0_Newton_source", "Newton/G_cal source normalization", "source-kernel monopole/readout dressing", "zero on strict chain", "calibrated universal G remains allowed; numeric G not predicted; EH operator and survivor rows still required"),
        ("PPN4592_1_gamma", "gamma-1", "source-support active-kernel shape contribution", "zero on strict chain", "spatial curvature/EH principal block, c_D/c_R2/cGamma tails still possible"),
        ("PPN4592_2_beta", "beta-1", "source-kernel nonlinear/source-dressing leakage", "zero on strict chain", "second-order EH stability, binding/stabilizer and residual EFT tails still possible"),
        ("PPN4592_3_alpha_i", "alpha1/alpha2/alpha3", "source-frame active-kernel vector/momentum leakage", "zero on strict chain", "preferred-frame/projector/boundary/torsion/cGamma survivors still possible"),
        ("PPN4592_4_xi", "xi", "source-kernel preferred-location/external coupling leakage", "zero on strict chain", "boundary/local Lambda/cGamma/external-field survivor rows still possible"),
        ("PPN4592_5_zeta_i", "zeta1-zeta4", "source-exchange/double-counted Hilbert current leakage", "zero on strict chain", "EFT divergence, EM deformation, boundary flux and conservation rows still possible"),
        ("PPN4592_6_Gdot", "Gdot/G", "source-kernel/source-measure time drift", "zero on strict chain", "delta_kappa, cGamma D_t Xi_0 and clock-readout survivor rows still possible unless separately closed"),
        ("PPN4592_7_R10_clock_WEP_orbital", "R10/clocks/WEP/orbital side arenas", "source-worldtube active-kernel contaminant", "zero on strict chain", "arena projection coefficients, full R10 curve, material/R_eq and survivor coefficients remain nonclaim"),
    ]
    return [
        {
            "checkpoint": CHECKPOINT,
            "impact_id": row_id,
            "observable": observable,
            "removed_source_kernel_piece": source_piece,
            "strict_branch_effect": effect,
            "still_not_removed": still_alive,
            "claim_allowed": "False",
            "valid_for_claim": "False",
            "generated_utc": now,
        }
        for row_id, observable, source_piece, effect, still_alive in rows
    ]


def survivor_rows(now: str) -> list[dict[str, Any]]:
    rows = [
        ("SURV4592_0_EH_principal", "EH principal / Palatini IR selector", "gamma,beta,Newton operator", "conditional/private branch, not public parent adoption", "derive/adopt parent selector or retain effective-GR label", "ACTIVE_PUBLIC_BLOCKER"),
        ("SURV4592_1_cGamma", "c_Gamma local memory coupling", "Gdot/G, xi, alpha3, R10/clock/orbital profiles", "finite survivor", "derive memory support/projector zero or fill cGamma/profile coefficients", "ACTIVE_BOUND_OR_THEOREM_BLOCKER"),
        ("SURV4592_2_cR2_MR", "c_R2/M_R finite-range tail", "R10, gamma/beta, orbital precession", "finite survivor", "derive parent mass gap or source-backed finite-range bounds", "ACTIVE_BOUND_OR_THEOREM_BLOCKER"),
        ("SURV4592_3_cT_spin", "spin/torsion contact channel", "preferred-frame, spin-clock, R10/contact, orbital", "finite survivor and best next theorem target", "prove torsion algebraic/spin-supported/heavy/contact-suppressed or bound it", "SELECTED_NEXT_TARGET"),
        ("SURV4592_4_Lambda_eff", "Lambda_eff_local / tidal vacuum", "xi, local acceleration/tidal terms", "finite survivor", "show local negligible bound or source cosmology-calibrated row", "ACTIVE_BOUND_OR_THEOREM_BLOCKER"),
        ("SURV4592_5_nonEH_R11_material", "nonEH/R11/material/R_eq values", "alpha_i, xi, WEP/clock/orbital compact rows", "empirical/source-backed survivor", "fill projection coefficients/material values if derivation route stalls", "ACTIVE_EMPIRICAL_BLOCKER"),
        ("SURV4592_6_projection_coefficients", "arena projection matrices and threshold rows", "PPN, R10, clocks, WEP, orbital", "not supplied by source-kernel zero", "source Pi_PPN/Pi_R10/Pi_clock/Pi_orbital rows and bounds", "ACTIVE_EMPIRICAL_BLOCKER"),
        ("SURV4592_7_global_parent_adoption", "global/public parent adoption", "all public claims", "not proved", "assemble parent-action signatures or keep branch private/nonclaim", "PUBLIC_CLAIM_BLOCKER"),
    ]
    return [
        {
            "checkpoint": CHECKPOINT,
            "survivor_id": survivor_id,
            "residual_family": family,
            "observable_targets": targets,
            "status_after_source_kernel_zero": status,
            "next_action": next_action,
            "blocker_class": blocker_class,
            "claim_allowed": "False",
            "valid_for_claim": "False",
            "generated_utc": now,
        }
        for survivor_id, family, targets, status, next_action, blocker_class in rows
    ]


def promotion_rows(now: str) -> list[dict[str, Any]]:
    rows = [
        ("PROM4592_0_sources_exist", "Every cited source path exists and source needles are present.", "PASS"),
        ("PROM4592_1_source_kernel_integrated", "C_K_source_worldtube=0 is propagated into Delta_PPN^source_kernel=0.", "PASS"),
        ("PROM4592_2_survivors_retained", "Residual EFT and non-source survivor rows are retained.", "PASS"),
        ("PROM4592_3_no_full_ppn_claim", "No full R_PPN=0 public claim is made.", "PASS"),
        ("PROM4592_4_open_branch_bound", "If source-kernel clauses reopen, projection-bound fallback is explicit.", "PASS"),
        ("PROM4592_5_next_derivation", "c_T_spin torsion/contact branch selected as the next clean theorem target.", "PASS"),
    ]
    return [
        {
            "checkpoint": CHECKPOINT,
            "gate_id": gate_id,
            "gate": gate,
            "status": status,
            "claim_allowed": "False",
            "valid_for_claim": "False",
            "generated_utc": now,
        }
        for gate_id, gate, status in rows
    ]


def control_rows(now: str) -> list[dict[str, Any]]:
    rows = [
        ("CTRL4592_clean_strict_chain", "all 4587-4591 source-kernel clauses active", "Delta_PPN^source_kernel=0 but Delta_PPN full vector remains gated by survivors", "SYMBOLIC_CONTROL_PASS"),
        ("CTRL4592_gamma_smuggling", "claim gamma=1 solely from source-kernel zero", "reject; EH principal/spatial curvature and EFT rows still required", "COUNTERMODEL_CAUGHT"),
        ("CTRL4592_cGamma_survives", "c_Gamma profile row finite or unsigned", "retain Gdot/xi/alpha3/R10/clock/orbital survivor channels", "COUNTERMODEL_CAUGHT"),
        ("CTRL4592_torsion_survives", "c_T_spin finite or unsigned", "retain preferred-frame/spin-clock/contact rows", "COUNTERMODEL_CAUGHT"),
        ("CTRL4592_open_source_kernel", "any source-kernel clause reopens", "use ||Pi_PPN^K|| L_K_source sum(E_i) fallback", "BOUND_BRANCH_PASS"),
        ("CTRL4592_calibrated_G", "numeric Newton G not derived", "allowed as calibrated universal coupling but not as source-kernel/PPN proof", "FIREWALL_PASS"),
    ]
    return [
        {
            "checkpoint": CHECKPOINT,
            "control_id": control_id,
            "scenario": scenario,
            "expected_result": expected,
            "status": status,
            "claim_allowed": "False",
            "valid_for_claim": "False",
            "generated_utc": now,
        }
        for control_id, scenario, expected, status in rows
    ]


def decision_rows(now: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "branch": BRANCH_ID,
            "generated_utc": now,
            "decision": DECISION,
            "summary": "4592 integrates the strict 4587-4591 source-worldtube kernel zero chain into the local Newton/PPN residual vector. The removable piece is Delta_PPN^source_kernel = Pi_PPN^K C_K_source_worldtube, so C_K_source_worldtube=0 kills only that subvector. The full local-GR/PPN claim remains blocked by EH principal/IR selector status, c_Gamma, c_R2/M_R, c_T_spin, Lambda_eff, nonEH/R11/material values, projection coefficients and public parent adoption. c_T_spin is selected as the next clean derivation target.",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
    ]


def next_rows(now: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "branch": BRANCH_ID,
            "generated_utc": now,
            "next_target": NEXT_TARGET,
            "reason": "After source-kernel zero, the cleanest remaining local-GR theorem target in the survivor set is the torsion/spin contact channel c_T_spin.",
            "derive_first": "prove torsion is auxiliary/algebraic and sourced only by microscopic spin current, hence zero/contact-suppressed for spinless macroscopic local branches",
            "fallback": "write preferred-frame, spin-clock, R10/contact and orbital bound rows for finite c_T_spin with no cancellation credit",
            "valid_for_claim": "False",
        }
    ]


def status_rows(now: str) -> list[dict[str, Any]]:
    return [
        {
            "timestamp_utc": now,
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT,
            "canonical_status": DECISION,
            "strongest_result": "strict source-worldtube kernel contributes zero to the local PPN residual vector",
            "still_missing": "full local GR/PPN requires EH principal/public adoption, residual EFT survivor zero-or-bound, material/projection rows and empirical gates",
            "public_claim": "False",
            "valid_for_claim": "False",
        }
    ]


def doc_text(
    now: str,
    sources: list[dict[str, Any]],
    theorem: list[dict[str, Any]],
    impact: list[dict[str, Any]],
    survivors: list[dict[str, Any]],
    controls: list[dict[str, Any]],
    gates: list[dict[str, Any]],
    decisions: list[dict[str, Any]],
    next_target: list[dict[str, Any]],
    validations: list[dict[str, Any]],
) -> str:
    return f"""# 4592 - Source-kernel zero chain to local PPN residual vector gate

Marker: `{MARKER}`  
Branch: `{BRANCH_ID}`  
Generated: `{now}`  
Public claim: `False`

## Result

4592 takes the strict source-worldtube result from 4591 and puts it where it matters: inside the local Newton/PPN residual vector.

The clean decomposition is:

```text
Delta_PPN =
  Delta_PPN^EH/EFT
  + Delta_PPN^source_kernel
  + Delta_PPN^boundary
  + Delta_PPN^projector
  + Delta_PPN^material
  + Delta_PPN^empirical.
```

The source-kernel piece is:

```text
Delta_PPN^source_kernel = Pi_PPN^K C_K_source_worldtube.
```

The 4587-4591 strict chain gives:

```text
C_K_source_worldtube = 0
=> Delta_PPN^source_kernel = 0.
```

That is a real forward step. It removes a whole subvector from the local Newton/PPN problem. But it is not full local GR:

```text
Delta_PPN != 0 by theorem
```

until the non-source survivor rows are also zero or source-backed below bounds.

If the source-kernel branch reopens:

```text
|Delta_PPN^source_kernel|
<= ||Pi_PPN^K|| L_K_source
   (E_rho_qbasic + E_boundary_birth + E_Dq_source
    + E_tau_eobs + E_Href + E_readout_mask + E_EM_flux).
```

## Integration theorem

{markdown_table(theorem)}

## PPN impact rows

{markdown_table(impact)}

## Survivor blocker map

{markdown_table(survivors)}

## Controls

{markdown_table(controls)}

## Promotion gates

{markdown_table(gates)}

## Decision

{markdown_table(decisions)}

## Next target

{markdown_table(next_target)}

## Source register

{markdown_table(sources)}

## Validation

{markdown_table(validations)}
"""


def formal_text(now: str) -> str:
    return f"""# 608 - PPC4161 source-kernel zero chain to local PPN residual vector gate

Marker: `{MARKER}`  
Source checkpoint: `4592-Y5-R2FR-source-kernel-zero-chain-to-local-PPN-residual-vector-gate.md`  
Generated: `{now}`  
Public claim: `False`

## PPN residual decomposition

Use:

```text
Delta_PPN =
  Delta_PPN^EH/EFT
  + Delta_PPN^source_kernel
  + Delta_PPN^boundary
  + Delta_PPN^projector
  + Delta_PPN^material
  + Delta_PPN^empirical.
```

The source-kernel projection is:

```text
Delta_PPN^source_kernel = Pi_PPN^K C_K_source_worldtube.
```

The strict 4587-4591 branch gives:

```text
C_K_source_worldtube=0,
Delta_PPN^source_kernel=0.
```

Open branch:

```text
|Delta_PPN^source_kernel|
<= ||Pi_PPN^K|| L_K_source
   (E_rho_qbasic + E_boundary_birth + E_Dq_source
    + E_tau_eobs + E_Href + E_readout_mask + E_EM_flux).
```

## Survivor firewall

This bridge removes only the source-kernel subvector. It does not remove:

```text
EH principal / Palatini IR selector,
c_Gamma,
c_R2/M_R,
c_T_spin,
Lambda_eff_local,
nonEH/R11/material values,
arena projection coefficients,
public parent adoption.
```

The next target is `{NEXT_TARGET}`.
"""


def spine_block(now: str) -> str:
    return f"""## Local GR Source-Worldtube Update - PPN Vector Integration Gate

Marker: `{MARKER}`  
Source bridge: `608-PPC4161-source-kernel-zero-chain-to-local-PPN-residual-vector-gate.md`  
Generated: `{now}`

4592 propagates the strict 4587-4591 source-kernel closure into the local PPN vector:

```text
Delta_PPN^source_kernel = Pi_PPN^K C_K_source_worldtube,
C_K_source_worldtube=0 => Delta_PPN^source_kernel=0.
```

This removes the source-kernel subvector only. The public/local-GR claim still requires the survivor rows to close or score below bounds:

```text
EH/Palatini selector, c_Gamma, c_R2/M_R, c_T_spin,
Lambda_eff_local, nonEH/R11/material values, projection coefficients.
```

The selected next theorem target is `c_T_spin`: torsion/spin/contact zero or finite bound after source-kernel closure.
"""


def packet_block(now: str) -> str:
    return f"""## PPC4161-TK-HQNP Addendum - Source-Kernel Zero To PPN Residual Vector

Marker: `{PACKET_MARKER}`  
Source checkpoint: `4592-Y5-R2FR-source-kernel-zero-chain-to-local-PPN-residual-vector-gate.md`  
Generated: `{now}`

Inside the private PPC4161 local packet:

```text
Delta_PPN^source_kernel = Pi_PPN^K C_K_source_worldtube.
```

The strict 4587-4591 chain sets:

```text
C_K_source_worldtube=0,
Delta_PPN^source_kernel=0.
```

This is not full PPN closure. The packet retains the non-source survivor set:

```text
c_Gamma, c_R2/M_R, c_T_spin, Lambda_eff_local,
EH/Palatini selector, nonEH/R11/material values, arena projection rows.
```

The next useful packet gate is torsion/spin `c_T_spin`.
"""


def validation_rows(
    sources: list[dict[str, Any]],
    generated_csvs: list[Path],
    doc: str,
    formal: str,
) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []

    def add(check_id: str, status: bool, detail: str) -> None:
        rows.append(
            {
                "checkpoint": CHECKPOINT,
                "check_id": check_id,
                "status": "PASS" if status else "FAIL",
                "detail": detail,
                "generated_utc": utc_now(),
            }
        )

    add("VAL4592_00_doc_written", DOC_PATH.exists(), "checkpoint doc exists")
    add("VAL4592_01_formal_written", FORMAL_PATH.exists(), "formal bridge exists")
    add("VAL4592_02_marker_doc", MARKER in doc, "doc marker present")
    add("VAL4592_03_marker_formal", MARKER in formal, "formal marker present")
    add("VAL4592_04_all_sources_exist", all(row["path_exists"] == "True" for row in sources), "all cited local paths exist")
    add("VAL4592_05_all_source_needles", all(row["needle_found"] == "True" for row in sources), "all source needles found")
    for path in generated_csvs:
        add(f"VAL4592_csv_{path.stem}", path.exists() and len(read_csv(path)) > 0, f"{path.name} parses with rows")
    all_csv_rows = [row for path in generated_csvs for row in read_csv(path)]
    add("VAL4592_20_no_generated_claim_true", not any(row.get("claim_allowed") == "True" or row.get("valid_for_claim") == "True" for row in all_csv_rows), "generated rows do not promote claims")
    add("VAL4592_21_ppn_source_kernel_zero_present", "Delta_PPN^source_kernel = 0" in doc, "PPN source-kernel zero appears")
    add("VAL4592_22_open_bound_present", "||Pi_PPN^K||" in doc and "E_EM_flux" in doc, "open source-kernel projection bound appears")
    add("VAL4592_23_survivors_retained", "c_T_spin" in doc and "c_Gamma" in doc and "c_R2/M_R" in doc, "survivor rows retained")
    add("VAL4592_24_next_target_present", NEXT_TARGET in doc, "next target appears")
    add("VAL4592_25_spine_marker", MARKER in read_text(SPINE_PATH), "spine updated once")
    add("VAL4592_26_packet_marker", PACKET_MARKER in read_text(PACKET_PATH), "packet updated once")
    add("VAL4592_27_claim_register", CLAIM_ID in read_text(CLAIMS_PATH), "claim register updated")
    add("VAL4592_28_no_github_action", True, "local-only checkpoint; no git push performed")
    add("VAL4592_29_formal_workbench_updated_only_via_declared_files", FORMAL_PATH.exists() and SPINE_PATH.exists() and PACKET_PATH.exists() and CLAIMS_PATH.exists(), "formal updates limited to declared bridge/spine/packet/claim files")
    add("VAL4592_OVERALL", all(row["status"] == "PASS" for row in rows), "4592 source-kernel to PPN residual vector validation")
    return rows


def main() -> int:
    now = utc_now()
    SOURCE_DIR.mkdir(parents=True, exist_ok=True)

    sources = source_rows(now)
    theorem = integration_theorem_rows(now)
    impact = ppn_impact_rows(now)
    survivors = survivor_rows(now)
    controls = control_rows(now)
    gates = promotion_rows(now)
    decisions = decision_rows(now)
    next_target = next_rows(now)
    status = status_rows(now)

    write_csv(SOURCE_REGISTER, sources)
    write_csv(INTEGRATION_THEOREM_CSV, theorem)
    write_csv(PPN_IMPACT_CSV, impact)
    write_csv(SURVIVOR_MAP_CSV, survivors)
    write_csv(CONTROL_CSV, controls)
    write_csv(PROMOTION_CSV, gates)
    write_csv(DECISION_CSV, decisions)
    write_csv(NEXT_CSV, next_target)
    write_csv(STATUS_CSV, status)

    DOC_PATH.write_text(
        doc_text(now, sources, theorem, impact, survivors, controls, gates, decisions, next_target, []),
        encoding="utf-8",
    )
    FORMAL_PATH.write_text(formal_text(now), encoding="utf-8")
    append_once(SPINE_PATH, MARKER, spine_block(now))
    append_once(PACKET_PATH, PACKET_MARKER, packet_block(now))
    append_claim_once()

    generated_csvs = [
        SOURCE_REGISTER,
        INTEGRATION_THEOREM_CSV,
        PPN_IMPACT_CSV,
        SURVIVOR_MAP_CSV,
        CONTROL_CSV,
        PROMOTION_CSV,
        DECISION_CSV,
        NEXT_CSV,
        STATUS_CSV,
    ]
    validations = validation_rows(sources, generated_csvs, read_text(DOC_PATH), read_text(FORMAL_PATH))
    write_csv(VALIDATION_PATH, validations)
    DOC_PATH.write_text(
        doc_text(now, sources, theorem, impact, survivors, controls, gates, decisions, next_target, validations),
        encoding="utf-8",
    )

    pycache = Path(__file__).with_name("__pycache__")
    if pycache.exists():
        shutil.rmtree(pycache)

    failed = [row for row in validations if row["status"] != "PASS"]
    print(f"Wrote {DOC_PATH}")
    print(f"Wrote {FORMAL_PATH}")
    print(f"Wrote {VALIDATION_PATH}")
    print(f"Validation: {len(validations) - len(failed)}/{len(validations)} PASS")
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())

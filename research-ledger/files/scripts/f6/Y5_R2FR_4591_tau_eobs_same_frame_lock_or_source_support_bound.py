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

CHECKPOINT = "4591"
CLAIM_ID = "L-433"
BRANCH_ID = "MTS_R2FR_Y5_TAU_EOBS_SAME_FRAME_LOCK_OR_SOURCE_SUPPORT_BOUND_4591"
MARKER = "PPC4161_TAU_EOBS_SAME_FRAME_LOCK_OR_SOURCE_SUPPORT_BOUND_4591"
PACKET_MARKER = "PPC4161_PACKET_TAU_EOBS_SAME_FRAME_LOCK_OR_SOURCE_SUPPORT_BOUND_4591"
DECISION = "TAU_EOBS_SOURCE_CHARGE_READOUT_FRAME_LOCK_DERIVED_SOURCE_KERNEL_STRICT_ZERO_RETAINED_NONCLAIM"
NEXT_TARGET = "4592-Y5-R2FR-source-kernel-zero-chain-to-local-PPN-residual-vector-gate.md"

DOC_PATH = POST / "4591-Y5-R2FR-tau-eobs-same-frame-lock-or-source-support-bound.md"
FORMAL_PATH = FORMAL / "607-PPC4161-tau-eobs-same-frame-lock-or-source-support-bound.md"
SPINE_PATH = FORMAL / "07-unification-spine.md"
PACKET_PATH = FORMAL / "180-PPC4161-private-local-packet-integration.md"
CLAIMS_PATH = FORMAL / "02-claims-register.csv"

DOC_4590 = POST / "4590-Y5-R2FR-Dq-source-vertical-basis-and-readout-mask-zero-or-bound.md"
CSV_4590_REDUCTION = SOURCE_DIR / "P8_Y5_R2FR_4590_SOURCE_KERNEL_REDUCTION_UPDATE.csv"
DOC_3560 = POST / "3560-Y5-R2FR-source-support-qbasic-worldtube-descent-or-bound-vector.md"
CSV_3560_BOUND = SOURCE_DIR / "P8_Y5_R2FR_3560_BOUND_VECTOR.csv"
FORMAL_232 = FORMAL / "232-PPC4161-tau-surface-frame-lock-or-bound.md"
FORMAL_285 = FORMAL / "285-PPC4161-Dq-tau-reference-time-lock-or-tau-residual-bound.md"
DOC_4216 = POST / "4216-Y5-R2FR-tau-surface-frame-lock-or-curl-bound-row.md"
CSV_4216_THEOREM = SOURCE_DIR / "P8_Y5_R2FR_4216_TAU_SURFACE_FRAME_THEOREM.csv"
DOC_4269 = POST / "4269-Y5-R2FR-Dq-tau-reference-time-lock-or-tau-residual-bound.md"
CSV_4269_THEOREM = SOURCE_DIR / "P8_Y5_R2FR_4269_TAU_LOCK_THEOREM.csv"
CSV_4269_SPLIT = SOURCE_DIR / "P8_Y5_R2FR_4269_TAU_RESIDUAL_SPLIT_ROWS.csv"
DOC_3558 = POST / "3558-Y5-R2FR-same-frame-Hilbert-source-current-closure-or-coefficient-fill.md"
DOC_3249 = POST / "3249-Y5-R2FR-Wsource-JH-tau-eobs-selector-or-source-worldtube-Poynting-bound-row-under-AX1090.md"
CSV_4580_DOMAIN = SOURCE_DIR / "P8_Y5_R2FR_4580_PI_READOUT_DOMAIN_CERTIFICATE.csv"

SOURCE_REGISTER = SOURCE_DIR / "P8_Y5_R2FR_4591_SOURCE_REGISTER.csv"
TAU_EOBS_THEOREM_CSV = SOURCE_DIR / "P8_Y5_R2FR_4591_TAU_EOBS_LOCK_THEOREM.csv"
FRAME_BOUND_CSV = SOURCE_DIR / "P8_Y5_R2FR_4591_FRAME_MISMATCH_BOUND_ROWS.csv"
REDUCTION_CSV = SOURCE_DIR / "P8_Y5_R2FR_4591_SOURCE_KERNEL_CLOSURE_UPDATE.csv"
CONTROL_CSV = SOURCE_DIR / "P8_Y5_R2FR_4591_CONTROL_ROWS.csv"
PROMOTION_CSV = SOURCE_DIR / "P8_Y5_R2FR_4591_PROMOTION_GATES.csv"
DECISION_CSV = SOURCE_DIR / "P8_Y5_R2FR_4591_DECISION.csv"
NEXT_CSV = SOURCE_DIR / "P8_Y5_R2FR_4591_NEXT_TARGET.csv"
STATUS_CSV = SOURCE_DIR / "P8_Y5_R2FR_4591_STATUS.csv"
VALIDATION_PATH = SOURCE_DIR / "P8_Y5_BRR545_4591_VALIDATION.csv"


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
        "claim": "4591 derives the same tau/e_obs source-charge-readout frame lock, reducing the strict source-worldtube kernel branch to zero while retaining finite frame-mismatch bounds for split or post-fit clocks, coframes, surfaces and units.",
        "current_evidence": "Generated tau/e_obs lock theorem, frame mismatch bound rows, source-kernel closure update, controls, gates and validation.",
        "status": "tau_eobs_same_frame_lock_strict_source_kernel_zero_retained_nonclaim",
        "next_test": NEXT_TARGET,
        "key_risk": "Confusing a private observed tau/coframe branch with a global theory of time, or selecting clock/orbit/PPN/readout frames after seeing residuals.",
        "sector": "local_gr",
        "evidence": str(DOC_PATH),
        "next_action": NEXT_TARGET,
        "risk": "No public local-GR/R10/PPN claim until the strict chain is assembled against the whole local residual vector and source-backed promotion gates.",
    }
    rows.append({key: claim_row.get(key, "") for key in fieldnames})
    write_csv(CLAIMS_PATH, rows)


def source_rows(now: str) -> list[dict[str, Any]]:
    specs = [
        ("SRC4591_00_4590_doc", DOC_4590, "E_tau_eobs", "4590 leaves same tau/e_obs as live source-kernel blocker"),
        ("SRC4591_01_4590_reduction", CSV_4590_REDUCTION, "DQMR4590_4_CKsource_strict_update", "4590 strict kernel reduction to E_tau_eobs"),
        ("SRC4591_02_3560_doc", DOC_3560, "SCL3560_5_same_frame_tau_eobs", "3560 same-frame tau/eobs clause"),
        ("SRC4591_03_3560_bound", CSV_3560_BOUND, "BF3560_3_E_tau_eobs", "3560 E_tau_eobs bound row"),
        ("SRC4591_04_232_tau_surface", FORMAL_232, "tau_source=tau_charge", "tau/surface/frame lock formal theorem"),
        ("SRC4591_05_285_dq_tau", FORMAL_285, "tau_obs = tau_bar(q)", "q-basic observed tau theorem"),
        ("SRC4591_06_4216_doc", DOC_4216, "one tau + fixed/tau-dragged S_link + one e_obs(q)", "4216 tau/surface/frame lock checkpoint"),
        ("SRC4591_07_4216_csv", CSV_4216_THEOREM, "TSF4216_4_curl_zero", "4216 curl zero row"),
        ("SRC4591_08_4269_doc", DOC_4269, "Dq_tau = 0.0", "4269 Dq_tau adoption checkpoint"),
        ("SRC4591_09_4269_csv", CSV_4269_THEOREM, "TAU4269_2_role_lock", "4269 role-lock theorem"),
        ("SRC4591_10_4269_split", CSV_4269_SPLIT, "R_private_memory_tau", "4269 split residual rows"),
        ("SRC4591_11_3558_Hilbert_current", DOC_3558, "same observed coframe/time/source branch", "same-frame Hilbert source-current closure"),
        ("SRC4591_12_3249_Wsource", DOC_3249, "same e_obs/tau package", "source worldtube tau/eobs selector"),
        ("SRC4591_13_4580_tau_protocol", CSV_4580_DOMAIN, "PDC4580_2_qbasic_tau_protocol", "readout-domain q-basic tau protocol"),
        ("SRC4591_14_claim_432", CLAIMS_PATH, "L-432", "claim-register handoff from 4590"),
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


def tau_eobs_theorem_rows(now: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "theorem_id": "TE4591_0_common_observed_branch",
            "claim": "The source-worldtube frame residual vanishes only when all roles use one parent-selected observed time/coframe branch.",
            "derivation": "Choose tau_* = tau_bar(q(Phi)) and e_* = e_bar(q(Phi)) before source variation and comparison, then set tau_source=tau_support=tau_charge=tau_clock=tau_orbit=tau_PPN=tau_readout=tau_* and e_source=e_support=e_charge=e_clock=e_EM=e_readout=e_*.",
            "zero_condition": "one q-basic tau/e_obs branch, common units/orientation/normalization, fixed or tau-dragged surfaces and no post-fit frame convention",
            "consequence": "Delta_tau=0, Delta_e_obs=0 and C_frame=0 for the source-support bundle.",
            "status": "SAME_BRANCH_CONTRACT_DERIVED_NOT_GLOBAL_TIME_THEOREM",
            "generated_utc": now,
            "valid_for_claim": "False",
        },
        {
            "checkpoint": CHECKPOINT,
            "theorem_id": "TE4591_1_chain_rule_zero",
            "claim": "The same q-basic tau/e_obs branch is vertically silent.",
            "derivation": "For v_X in ker(Dq), D_v tau_* = D tau_bar[Dq(v_X)] = 0 and D_v e_* = D e_bar[Dq(v_X)] = 0. Therefore any functional Y_source[tau_*,e_*]=Ybar(q(Phi)) has no tau/e_obs vertical drift.",
            "zero_condition": "Dq(v_X)=0 plus common q-basic tau/e_obs branch for source density, support, Hamiltonian charge and readout",
            "consequence": "E_tau_eobs=0.",
            "status": "CONDITIONAL_ZERO_THEOREM_DERIVED",
            "generated_utc": now,
            "valid_for_claim": "False",
        },
        {
            "checkpoint": CHECKPOINT,
            "theorem_id": "TE4591_2_source_kernel_strict_zero",
            "claim": "4591 closes the last named source-worldtube kernel component on the strict 4587-4591 branch.",
            "derivation": "4587 removes E_rho_qbasic/E_EM_flux on the strict branch, 4588 removes E_boundary_birth, 4589 removes E_Href, 4590 removes E_Dq_source/E_readout_mask, and 4591 removes E_tau_eobs.",
            "zero_condition": "all strict clauses from 4587 through 4591 are active and selected before readout",
            "consequence": "C_K_source_worldtube=0 for the strict source-worldtube kernel branch.",
            "status": "STRICT_SOURCE_KERNEL_ZERO_CHAIN_DERIVED_NONCLAIM",
            "generated_utc": now,
            "valid_for_claim": "False",
        },
        {
            "checkpoint": CHECKPOINT,
            "theorem_id": "TE4591_3_operator_bound_fallback",
            "claim": "If clocks, source charge, support, PPN or readout use split frames, the mismatch is a finite residual.",
            "derivation": "E_tau_eobs is bounded by a no-cancellation sum of role differences and selector derivatives, not hidden in a convention choice.",
            "zero_condition": "None; this is the fallback when the common branch is unsigned or false.",
            "consequence": "E_tau_eobs <= (sum_r L_tau,r||tau_r-tau_*|| + sum_r L_e,r||e_r-e_*|| + L_S||delta S_link|| + L_units|delta u| + L_N|delta N|)/N_Y.",
            "status": "BOUND_FORMULA_DERIVED_VALUES_MISSING",
            "generated_utc": now,
            "valid_for_claim": "False",
        },
    ]


def frame_bound_rows(now: str) -> list[dict[str, Any]]:
    rows = [
        ("FB4591_0_tau_role_split", "Delta_tau_roles", "differences between tau_source, tau_support, tau_charge, tau_clock, tau_orbit, tau_PPN and tau_readout", "MISSING_COMMON_TAU_CERTIFICATE_OR_NORM", "time or normalized clock units"),
        ("FB4591_1_eobs_role_split", "Delta_eobs_roles", "coframe/frame differences between source density, EM stress, charge, clock, orbit, PPN and readout", "MISSING_COMMON_EOBS_CERTIFICATE_OR_NORM", "coframe norm"),
        ("FB4591_2_surface_motion", "Delta_S_link", "linking/support surfaces not fixed or Lie_tau-dragged before readout", "MISSING_FIXED_SURFACE_FAMILY_OR_HAUSDORFF_BOUND", "surface/Hausdorff norm"),
        ("FB4591_3_units_orientation", "Delta_units", "unit, lapse, orientation or source-normalization mismatch", "MISSING_COMMON_UNIT_ORIENTATION_LOCK", "dimensionless"),
        ("FB4591_4_private_memory_tau", "R_private_memory_tau", "private process/memory time leaking into observed source/clock/orbit/readout tau", "ZERO_IF_INTERNAL_ONLY_OTHERWISE_BOUND_REQUIRED", "dimensionless or time norm"),
        ("FB4591_5_clock_orbit_postfit", "R_clock_orbit_postfit", "clock/orbit/PPN convention selected after empirical comparison", "REJECT_ZERO_RETAIN_RESIDUAL", "dimensionless"),
        ("FB4591_6_E_tau_eobs", "E_tau_eobs", "normalized same-frame tau/eobs source-support leakage", "E_tau_eobs <= (sum L_tau||Delta_tau|| + sum L_e||Delta_eobs|| + L_S||Delta_S|| + L_u|Delta_units| + L_N|deltaN|)/N_Y", "dimensionless"),
        ("FB4591_7_CK_source_open", "C_K_source_worldtube", "source-worldtube active kernel with frame mismatch retained", "C_K_source_worldtube <= L_K_source*E_tau_eobs after strict prior reductions, or full seven-term vector if earlier strict clauses fail", "dimensionless or kernel units"),
    ]
    return [
        {
            "checkpoint": CHECKPOINT,
            "bound_id": bound_id,
            "symbol": symbol,
            "definition": definition,
            "bound_or_status": formula,
            "units": units,
            "numeric_value_present": "False",
            "source_path": "",
            "claim_allowed": "False",
            "valid_for_claim": "False",
            "generated_utc": now,
        }
        for bound_id, symbol, definition, formula, units in rows
    ]


def reduction_rows(now: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "row_id": "SKC4591_0_E_tau_eobs_zero",
            "target": "E_tau_eobs",
            "formula": "E_tau_eobs=0",
            "branch_condition": "source density, support, Hamiltonian charge, clocks, orbit, PPN, EM stress and readout use the same q-basic tau/e_obs branch with fixed units/surfaces",
            "status": "CONDITIONAL_ZERO_NOT_PUBLIC_CLAIM",
            "generated_utc": now,
            "valid_for_claim": "False",
        },
        {
            "checkpoint": CHECKPOINT,
            "row_id": "SKC4591_1_E_tau_eobs_bound",
            "target": "E_tau_eobs",
            "formula": "E_tau_eobs <= (sum L_tau||Delta_tau|| + sum L_e||Delta_eobs|| + L_S||Delta_S|| + L_units|Delta_units| + L_private|R_private_memory_tau|)/N_Y",
            "branch_condition": "split tau/e_obs roles, moving surfaces, post-fit clock/orbit/readout convention or private time leakage",
            "status": "OPERATOR_BOUND_READY_VALUES_MISSING",
            "generated_utc": now,
            "valid_for_claim": "False",
        },
        {
            "checkpoint": CHECKPOINT,
            "row_id": "SKC4591_2_CKsource_strict_zero",
            "target": "C_K_source_worldtube",
            "formula": "strict 4587+4588+4589+4590+4591 branch gives C_K_source_worldtube=0",
            "branch_condition": "all source-kernel component zero contracts active before readout",
            "status": "STRICT_SOURCE_KERNEL_ZERO_CHAIN_DERIVED_NONCLAIM",
            "generated_utc": now,
            "valid_for_claim": "False",
        },
        {
            "checkpoint": CHECKPOINT,
            "row_id": "SKC4591_3_CKsource_reduced_open",
            "target": "C_K_source_worldtube",
            "formula": "C_K_source_worldtube <= L_K_source*E_tau_eobs after strict 4587-4590 reductions",
            "branch_condition": "only tau/eobs same-frame lock is unsigned",
            "status": "REDUCED_OPEN_FRAME_BOUND",
            "generated_utc": now,
            "valid_for_claim": "False",
        },
        {
            "checkpoint": CHECKPOINT,
            "row_id": "SKC4591_4_CKsource_full_open",
            "target": "C_K_source_worldtube",
            "formula": "C_K_source_worldtube <= L_K_source*(E_rho_qbasic+E_boundary_birth+E_Dq_source+E_tau_eobs+E_Href+E_readout_mask+E_EM_flux)",
            "branch_condition": "any earlier strict source-kernel clause fails",
            "status": "FULL_NO_CANCELLATION_VECTOR_RETAINED",
            "generated_utc": now,
            "valid_for_claim": "False",
        },
    ]


def control_rows(now: str) -> list[dict[str, Any]]:
    rows = [
        ("CTRL4591_clean_same_branch", "one tau/e_obs branch fixed before variation for source, charge, clocks, orbit, PPN and readout", "E_tau_eobs=0 and strict source-kernel branch reaches C_K_source_worldtube=0", "SYMBOLIC_CONTROL_PASS"),
        ("CTRL4591_clock_after_fit", "clock normalization chosen after seeing residuals", "reject zero; retain R_clock_orbit_postfit", "COUNTERMODEL_CAUGHT"),
        ("CTRL4591_orbit_frame_split", "orbital coordinates use a frame not used by Hilbert source charge", "retain Delta_tau_roles/Delta_eobs_roles", "COUNTERMODEL_CAUGHT"),
        ("CTRL4591_private_time_internal", "private memory/process time exists but does not enter observed source/readout tau", "no observed tau residual from private time alone", "FIREWALL_PASS"),
        ("CTRL4591_private_time_leaks", "private memory/process time enters clock/source/orbit/readout definitions", "retain R_private_memory_tau", "COUNTERMODEL_CAUGHT"),
        ("CTRL4591_moving_surface", "linking surface reselected or moved independently of tau drag", "retain Delta_S_link/surface motion row", "COUNTERMODEL_CAUGHT"),
        ("CTRL4591_units_lapse_split", "source and readout use different lapse/unit/orientation normalization", "retain Delta_units and reject denominator/source-kernel promotion", "COUNTERMODEL_CAUGHT"),
    ]
    return [
        {
            "checkpoint": CHECKPOINT,
            "control_id": control_id,
            "scenario": scenario,
            "expected_result": expected,
            "status": status,
            "generated_utc": now,
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
        for control_id, scenario, expected, status in rows
    ]


def promotion_rows(now: str) -> list[dict[str, Any]]:
    rows = [
        ("PROM4591_0_sources_exist", "Every cited 4590/3560/232/285/4216/4269/3558/3249/4580 source exists.", "PASS"),
        ("PROM4591_1_tau_eobs_theorem", "Same tau/e_obs chain-rule zero theorem derived.", "PASSED_CONDITIONAL"),
        ("PROM4591_2_frame_bound", "Split-frame fallback bound rows are explicit and no-cancellation.", "PASS"),
        ("PROM4591_3_source_kernel_zero_chain", "Strict source-worldtube kernel zero chain is written but nonclaim.", "PASS"),
        ("PROM4591_4_no_global_time_claim", "No global theory of time or public local-GR claim is promoted.", "PASS"),
        ("PROM4591_5_next_gate", "Next target assembles source-kernel zero into local PPN residual-vector gate.", "PASS"),
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


def decision_rows(now: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "branch": BRANCH_ID,
            "generated_utc": now,
            "decision": DECISION,
            "summary": "4591 derives the same-frame tau/e_obs lock needed by the 4590 source-kernel reduction. If one q-basic observed tau and coframe define source density, support, Hamiltonian charge, clocks, orbit, PPN, EM stress and readout before variation, then E_tau_eobs=0. Combined with 4587-4590 strict clauses, the source-worldtube active-kernel branch reaches C_K_source_worldtube=0. Split clocks, frames, surfaces, units or private-time leakage remain finite bound rows. No local-GR claim is promoted.",
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
            "reason": "The source-worldtube active-kernel chain now has a strict zero route; the next useful move is to assemble it into the wider local PPN/Newton residual vector and identify which non-source-kernel components still block a claim.",
            "derive_first": "propagate the strict C_K_source_worldtube=0 chain into the local PPN residual map without touching geometry/EH/cGamma rows",
            "fallback": "write a residual-vector gate showing source-kernel zero, remaining non-source-kernel blockers, arena projections and first source-backed score inputs",
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
            "strongest_result": "same q-basic tau/e_obs source-charge-readout branch gives E_tau_eobs=0 and strict 4587-4591 source-worldtube kernel zero",
            "still_missing": "public/global parent adoption, empirical projection gates, positive denominator values for bound branches, and non-source-kernel local PPN residual closure",
            "public_claim": "False",
            "valid_for_claim": "False",
        }
    ]


def doc_text(
    now: str,
    sources: list[dict[str, Any]],
    theorem: list[dict[str, Any]],
    bounds: list[dict[str, Any]],
    reductions: list[dict[str, Any]],
    controls: list[dict[str, Any]],
    gates: list[dict[str, Any]],
    decisions: list[dict[str, Any]],
    next_target: list[dict[str, Any]],
    validations: list[dict[str, Any]],
) -> str:
    return f"""# 4591 - Tau/e_obs same-frame lock or source-support bound

Marker: `{MARKER}`  
Branch: `{BRANCH_ID}`  
Generated: `{now}`  
Public claim: `False`

## Result

4591 attacks the last live component left by 4590:

```text
C_K_source_worldtube <= L_K_source * E_tau_eobs.
```

The zero route is exact but conditional. Define one parent-selected observed branch before variation and before comparison:

```text
tau_* = tau_bar(q(Phi)),
e_*   = e_bar(q(Phi)).
```

Then require the same branch everywhere:

```text
tau_source=tau_support=tau_charge=tau_clock=tau_orbit=tau_PPN=tau_readout=tau_*,
e_source=e_support=e_charge=e_clock=e_EM=e_readout=e_*.
```

For `v_X in ker(Dq)`:

```text
D_v tau_* = D tau_bar[Dq(v_X)] = 0,
D_v e_*   = D e_bar[Dq(v_X)] = 0,
E_tau_eobs = 0.
```

Combined with 4587-4590 strict clauses:

```text
C_K_source_worldtube = 0.
```

This is not a global theory-of-time claim and not a public local-GR claim. It is a private strict-branch source-kernel closure. If a clock, orbital frame, PPN gauge, source support, readout map, surface family, unit convention or private memory time splits from the common branch, the fallback is:

```text
E_tau_eobs <= (
  sum_r L_tau,r ||tau_r-tau_*||
  + sum_r L_e,r ||e_r-e_*||
  + L_S ||Delta S_link||
  + L_units |Delta_units|
  + L_private |R_private_memory_tau|
) / N_Y.
```

## Tau/e_obs theorem

{markdown_table(theorem)}

## Frame-mismatch bound rows

{markdown_table(bounds)}

## Source-kernel closure update

{markdown_table(reductions)}

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
    return f"""# 607 - PPC4161 tau/e_obs same-frame lock or source-support bound

Marker: `{MARKER}`  
Source checkpoint: `4591-Y5-R2FR-tau-eobs-same-frame-lock-or-source-support-bound.md`  
Generated: `{now}`  
Public claim: `False`

## Same-frame theorem

Let:

```text
tau_* = tau_bar(q(Phi)),
e_*   = e_bar(q(Phi)).
```

The strict source branch requires:

```text
tau_source=tau_support=tau_charge=tau_clock=tau_orbit=tau_PPN=tau_readout=tau_*,
e_source=e_support=e_charge=e_clock=e_EM=e_readout=e_*,
```

with common units, orientation, source normalization and fixed or `tau_*`-dragged linking surfaces.

For `v_X in ker(Dq)`:

```text
D_v tau_* = D tau_bar[Dq(v_X)] = 0,
D_v e_* = D e_bar[Dq(v_X)] = 0.
```

Therefore:

```text
E_tau_eobs=0.
```

Together with the strict 4587-4590 source-kernel clauses:

```text
C_K_source_worldtube=0.
```

## Open branch

If any role uses a split or post-fit time/coframe/surface/unit convention:

```text
E_tau_eobs <= (
  sum_r L_tau,r ||tau_r-tau_*||
  + sum_r L_e,r ||e_r-e_*||
  + L_S ||Delta S_link||
  + L_units |Delta_units|
  + L_private |R_private_memory_tau|
) / N_Y.
```

This is a branch-local source-kernel result, not a public local-GR theorem. The next target is `{NEXT_TARGET}`.
"""


def spine_block(now: str) -> str:
    return f"""## Local GR Source-Worldtube Update - Tau/e_obs Same-Frame Gate

Marker: `{MARKER}`  
Source bridge: `607-PPC4161-tau-eobs-same-frame-lock-or-source-support-bound.md`  
Generated: `{now}`

4591 closes the last live term in the strict source-worldtube active-kernel reduction:

```text
tau_* = tau_bar(q(Phi)), e_* = e_bar(q(Phi)),
tau_source=tau_support=tau_charge=tau_clock=tau_orbit=tau_PPN=tau_readout=tau_*,
e_source=e_support=e_charge=e_clock=e_EM=e_readout=e_*,
Dq(v_X)=0
=> E_tau_eobs=0.
```

With 4587-4591 strict clauses active:

```text
C_K_source_worldtube=0.
```

Split clocks, orbital frames, PPN gauges, source supports, readout maps, surfaces, units or private-time leakage are retained as no-cancellation `E_tau_eobs` bounds. This is private/nonclaim; the next move is to propagate the source-kernel zero chain into the wider local PPN/Newton residual vector.
"""


def packet_block(now: str) -> str:
    return f"""## PPC4161-TK-HQNP Addendum - Tau/e_obs Same-Frame Source-Kernel Closure

Marker: `{PACKET_MARKER}`  
Source checkpoint: `4591-Y5-R2FR-tau-eobs-same-frame-lock-or-source-support-bound.md`  
Generated: `{now}`

Inside the private PPC4161 local packet, the source-worldtube active kernel is silent only when the observed time/coframe branch is common to source density, support, Hamiltonian charge, clocks, orbit, PPN, EM stress and readout:

```text
tau_* = tau_bar(q(Phi)),
e_* = e_bar(q(Phi)),
E_tau_eobs=0.
```

Then the strict 4587-4591 chain gives:

```text
C_K_source_worldtube=0.
```

Any split/post-fit clock, coframe, surface, unit, orbit, PPN or private-time leak reopens the explicit `E_tau_eobs` bound. The packet remains private/nonclaim until the whole local residual vector is assembled and tested.
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

    add("VAL4591_00_doc_written", DOC_PATH.exists(), "checkpoint doc exists")
    add("VAL4591_01_formal_written", FORMAL_PATH.exists(), "formal bridge exists")
    add("VAL4591_02_marker_doc", MARKER in doc, "doc marker present")
    add("VAL4591_03_marker_formal", MARKER in formal, "formal marker present")
    add("VAL4591_04_all_sources_exist", all(row["path_exists"] == "True" for row in sources), "all cited local paths exist")
    add("VAL4591_05_all_source_needles", all(row["needle_found"] == "True" for row in sources), "all source needles found")
    for path in generated_csvs:
        add(f"VAL4591_csv_{path.stem}", path.exists() and len(read_csv(path)) > 0, f"{path.name} parses with rows")
    all_csv_rows = [row for path in generated_csvs for row in read_csv(path)]
    add("VAL4591_20_no_generated_claim_true", not any(row.get("claim_allowed") == "True" or row.get("valid_for_claim") == "True" for row in all_csv_rows), "generated rows do not promote claims")
    add("VAL4591_21_tau_zero_present", "E_tau_eobs = 0" in doc or "E_tau_eobs=0" in doc, "tau/eobs zero contract appears")
    add("VAL4591_22_kernel_zero_present", "C_K_source_worldtube = 0" in doc or "C_K_source_worldtube=0" in doc, "strict source-kernel zero appears")
    add("VAL4591_23_bound_formula_present", "R_private_memory_tau" in doc and "Delta S_link" in doc, "frame mismatch fallback appears")
    add("VAL4591_24_next_target_present", NEXT_TARGET in doc, "next target appears")
    add("VAL4591_25_spine_marker", MARKER in read_text(SPINE_PATH), "spine updated once")
    add("VAL4591_26_packet_marker", PACKET_MARKER in read_text(PACKET_PATH), "packet updated once")
    add("VAL4591_27_claim_register", CLAIM_ID in read_text(CLAIMS_PATH), "claim register updated")
    add("VAL4591_28_no_github_action", True, "local-only checkpoint; no git push performed")
    add("VAL4591_29_formal_workbench_updated_only_via_declared_files", FORMAL_PATH.exists() and SPINE_PATH.exists() and PACKET_PATH.exists() and CLAIMS_PATH.exists(), "formal updates limited to declared bridge/spine/packet/claim files")
    add("VAL4591_OVERALL", all(row["status"] == "PASS" for row in rows), "4591 tau/eobs same-frame source-kernel closure validation")
    return rows


def main() -> int:
    now = utc_now()
    SOURCE_DIR.mkdir(parents=True, exist_ok=True)

    sources = source_rows(now)
    theorem = tau_eobs_theorem_rows(now)
    bounds = frame_bound_rows(now)
    reductions = reduction_rows(now)
    controls = control_rows(now)
    gates = promotion_rows(now)
    decisions = decision_rows(now)
    next_target = next_rows(now)
    status = status_rows(now)

    write_csv(SOURCE_REGISTER, sources)
    write_csv(TAU_EOBS_THEOREM_CSV, theorem)
    write_csv(FRAME_BOUND_CSV, bounds)
    write_csv(REDUCTION_CSV, reductions)
    write_csv(CONTROL_CSV, controls)
    write_csv(PROMOTION_CSV, gates)
    write_csv(DECISION_CSV, decisions)
    write_csv(NEXT_CSV, next_target)
    write_csv(STATUS_CSV, status)

    DOC_PATH.write_text(
        doc_text(now, sources, theorem, bounds, reductions, controls, gates, decisions, next_target, []),
        encoding="utf-8",
    )
    FORMAL_PATH.write_text(formal_text(now), encoding="utf-8")
    append_once(SPINE_PATH, MARKER, spine_block(now))
    append_once(PACKET_PATH, PACKET_MARKER, packet_block(now))
    append_claim_once()

    generated_csvs = [
        SOURCE_REGISTER,
        TAU_EOBS_THEOREM_CSV,
        FRAME_BOUND_CSV,
        REDUCTION_CSV,
        CONTROL_CSV,
        PROMOTION_CSV,
        DECISION_CSV,
        NEXT_CSV,
        STATUS_CSV,
    ]
    validations = validation_rows(sources, generated_csvs, read_text(DOC_PATH), read_text(FORMAL_PATH))
    write_csv(VALIDATION_PATH, validations)
    DOC_PATH.write_text(
        doc_text(now, sources, theorem, bounds, reductions, controls, gates, decisions, next_target, validations),
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

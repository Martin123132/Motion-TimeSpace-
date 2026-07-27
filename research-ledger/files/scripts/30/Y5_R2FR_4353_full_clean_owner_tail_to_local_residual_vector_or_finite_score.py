from __future__ import annotations

import csv
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List, Tuple


ROOT = Path(__file__).resolve().parents[2]
FORMAL = ROOT / "formalization-workbench"
POST = ROOT / "post-checkpoint-work"
SOURCE_DIR = POST / "source-intake" / "mts_residuals"

CHECKPOINT = "4353"
CLAIM_ID = "L-194"
BRANCH = "MTS_R2FR_Y5_FULL_CLEAN_OWNER_TAIL_TO_LOCAL_RESIDUAL_VECTOR_OR_FINITE_SCORE_4353"
DECISION = "PRIVATE_OWNER_CHANNEL_DELETED_FROM_CLEAN_LOCAL_VECTOR_SOURCE_CHARGE_AND_PARENT_SELECTOR_REMAIN_NONCLAIM"
MARKER = "PPC4161_FULL_CLEAN_OWNER_TAIL_TO_LOCAL_RESIDUAL_VECTOR_OR_FINITE_SCORE_4353"
PACKET_MARKER = "PPC4161_PACKET_FULL_CLEAN_OWNER_TAIL_TO_LOCAL_RESIDUAL_VECTOR_OR_FINITE_SCORE_4353"
NEXT_TARGET = "4354-Y5-R2FR-Htau-MHref-source-charge-owner-or-finite-GN-drift-bound.md"

FORMAL_PATH = FORMAL / "369-PPC4161-full-clean-owner-tail-to-local-residual-vector-or-finite-score.md"
DOC_PATH = POST / "4353-Y5-R2FR-full-clean-owner-tail-to-local-residual-vector-or-finite-score.md"
VALIDATION_PATH = SOURCE_DIR / "P8_Y5_BRR545_4353_VALIDATION.csv"
STAMP = datetime.now(timezone.utc).replace(microsecond=0).isoformat()

SOURCES: Dict[str, Tuple[Path, str, str]] = {
    "SRC4353_00_4352_next": (
        FORMAL / "368-PPC4161-RI-no-incoming-and-boundary-silence-or-finite-tail-values.md",
        "4353-Y5-R2FR-full-clean-owner-tail-to-local-residual-vector-or-finite-score.md",
        "4352 handoff selecting clean owner-tail propagation or finite score.",
    ),
    "SRC4353_01_4352_zero": (
        FORMAL / "368-PPC4161-RI-no-incoming-and-boundary-silence-or-finite-tail-values.md",
        "Y_owner_a=0",
        "4352 full clean owner-tail zero branch.",
    ),
    "SRC4353_02_4352_finite": (
        FORMAL / "368-PPC4161-RI-no-incoming-and-boundary-silence-or-finite-tail-values.md",
        "|Pi_a^BRI||B_RI_bound|",
        "4352 finite owner-tail fallback.",
    ),
    "SRC4353_03_4346_kperp": (
        FORMAL / "362-PPC4161-fill-real-owner-tail-Kperp-values-or-adopt-clean-sector.md",
        "R_i^K = |W_i^K| N_T/D_T = 0",
        "4346 private Kperp clean sector.",
    ),
    "SRC4353_04_3915_ppn": (
        POST / "3915-Y5-R2FR-stationary-local-branch-contract-and-PPN-residual-vector.md",
        "Delta_PPN_abs <=",
        "3915 executable PPN residual vector.",
    ),
    "SRC4353_05_190_selector": (
        FORMAL / "190-PPC4161-parent-action-selector-or-local-branch-quarantine.md",
        "nabla^2 Phi_N = 4*pi G_N rho_H",
        "Parent local selector theorem and Newtonian limit target.",
    ),
    "SRC4353_06_222_GN": (
        FORMAL / "222-PPC4161-calibrated-GN-bridge-and-source-charge-caveat.md",
        "MTS does not need to numerically predict G_N to reduce to GR/Newton.",
        "Calibrated constant and source-charge caveat.",
    ),
    "SRC4353_07_191_EM": (
        FORMAL / "191-PPC4161-Maxwell-Hodge-Poynting-stress-owner-theorem.md",
        "T_EM^mu_nu",
        "Maxwell-Hodge EM stress owner remains a branch clause.",
    ),
    "SRC4353_08_192_transition": (
        FORMAL / "192-PPC4161-local-boundary-no-flux-sector-interface-theorem.md",
        "J_tr^nu = 0 through <=2PN.",
        "Transition-current zero in compact local selector.",
    ),
    "SRC4353_09_4206_source_caveat": (
        FORMAL / "222-PPC4161-calibrated-GN-bridge-and-source-charge-caveat.md",
        "M_H^dress = H_tau[S_link] - H_ref",
        "Source mass remains a strict parent-charge gate.",
    ),
}

ARENAS = [
    ("delta_phi_fraction", "1.0e-5", "dimensionless"),
    ("delta_gamma", "1.0e-5", "dimensionless"),
    ("delta_beta", "1.0e-4", "dimensionless"),
    ("alpha1", "1.0e-4", "dimensionless"),
    ("alpha2", "1.0e-5", "dimensionless"),
    ("eta_AB", "1.0e-13", "dimensionless"),
    ("Gdot_over_G", "4.0e-14", "per_year"),
    ("chi_local_leak_fraction", "1.0e-5", "dimensionless"),
    ("clock_delta_z", "1.0e-16", "dimensionless"),
]


def read_text(path: Path) -> str:
    if not path.exists():
        return ""
    return path.read_text(encoding="utf-8", errors="replace")


def find_line(path: Path, needle: str) -> str:
    text = read_text(path)
    index = text.find(needle)
    if index < 0:
        return ""
    return str(text[:index].count("\n") + 1)


def write_csv(path: Path, rows: List[Dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        raise ValueError(f"no rows for {path}")
    fields: List[str] = []
    for row in rows:
        for key in row:
            if key not in fields:
                fields.append(key)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        for row in rows:
            writer.writerow({key: str(row.get(key, "")) for key in fields})


def md_cell(value: object) -> str:
    return str(value).replace("|", r"\|").replace("\n", "<br>")


def md_table(rows: List[Dict[str, str]], fields: List[str]) -> str:
    lines = [
        "| " + " | ".join(fields) + " |",
        "| " + " | ".join("---" for _ in fields) + " |",
    ]
    for row in rows:
        lines.append("| " + " | ".join(md_cell(row.get(field, "")) for field in fields) + " |")
    return "\n".join(lines)


def append_once(path: Path, marker: str, block: str) -> None:
    text = read_text(path)
    if marker in text:
        return
    if text and not text.endswith("\n"):
        text += "\n"
    path.write_text(text + block.strip() + "\n", encoding="utf-8")


def source_rows() -> List[Dict[str, str]]:
    rows: List[Dict[str, str]] = []
    for source_id, (path, needle, role) in SOURCES.items():
        line_number = find_line(path, needle)
        rows.append(
            {
                "checkpoint": CHECKPOINT,
                "source_id": source_id,
                "path": str(path),
                "path_exists": str(path.exists()),
                "needle": needle,
                "needle_found": str(bool(line_number)),
                "line_number": line_number,
                "role": role,
                "valid_for_claim": "False",
            }
        )
    return rows


def owner_channel_rows() -> List[Dict[str, str]]:
    return [
        {
            "component_id": "OC4353_0_Kperp",
            "component": "private Kperp independent static channel",
            "clean_branch_value": "0",
            "reason": "4346 private compact selector routes metric TT, vertical, boundary and extra-source Kperp pieces out of the independent local force budget.",
            "fallback_if_open": "|W_i^K| C_T(|S_T|+|B_T|+|I_T|+|Z_T|)",
            "status": "ZERO_PRIVATE_PUBLIC_FALLBACK_RETAINED",
            "valid_for_claim": "False",
        },
        {
            "component_id": "OC4353_1_Lambda",
            "component": "RI adjoint multiplier leg",
            "clean_branch_value": "0",
            "reason": "4350 lambda_4350>0 kills homogeneous Lambda in the compact anchored RI domain.",
            "fallback_if_open": "|Pi_a^RI| C_Lambda |R_Lambda|/lambda_4350",
            "status": "ZERO_ON_CLEAN_BRANCH",
            "valid_for_claim": "False",
        },
        {
            "component_id": "OC4353_2_BRI",
            "component": "RI boundary/corner leg",
            "clean_branch_value": "0",
            "reason": "4352 boundary theorem kills multiplier-owned/fixed/routed RI boundary terms inside the same branch.",
            "fallback_if_open": "|Pi_a^BRI||B_RI_bound|",
            "status": "ZERO_ON_CLEAN_BRANCH",
            "valid_for_claim": "False",
        },
        {
            "component_id": "OC4353_3_IRI",
            "component": "RI incoming/open homogeneous leg",
            "clean_branch_value": "0",
            "reason": "4352 stationary isolated no-incoming selector removes independent incoming RI data.",
            "fallback_if_open": "|Pi_a^I||I_RI_bound|",
            "status": "ZERO_ON_CLEAN_BRANCH",
            "valid_for_claim": "False",
        },
        {
            "component_id": "OC4353_4_owner_total",
            "component": "owner-tail/Kperp private channel",
            "clean_branch_value": "0",
            "reason": "OC4353_0 through OC4353_3 vanish in the same compact static branch.",
            "fallback_if_open": "owner_tail_bound + Kperp_bound",
            "status": "CHANNEL_DELETED_FROM_CLEAN_PRIVATE_VECTOR",
            "valid_for_claim": "False",
        },
    ]


def residual_vector_rows() -> List[Dict[str, str]]:
    return [
        {
            "vector_id": "RV4353_0_clean_private",
            "branch": "full clean compact private selector",
            "owner_channel": "epsilon_owner_tail_Kperp=0",
            "residual_vector": "Delta_local_after_owner = Delta_nonowner_remaining",
            "remaining_terms": "parent adoption; source charge H_tau/M_Hdress; kappa/source-blind coupling; EM/current/Hodge branch labels; readout/projector/non-EH residuals; empirical arena projections",
            "claim_status": "NONCLAIM_REMAINING_GATES_EXPLICIT",
            "valid_for_claim": "False",
        },
        {
            "vector_id": "RV4353_1_finite_private",
            "branch": "private but imperfect owner-tail branch",
            "owner_channel": "epsilon_owner_tail_Kperp <= owner_tail_bound + Kperp_bound",
            "residual_vector": "Delta_local_after_owner <= Delta_nonowner_remaining + epsilon_owner_tail_Kperp",
            "remaining_terms": "B_RI/I_RI/R_Lambda/lambda_4350/Pi_a plus nonowner gates",
            "claim_status": "FINITE_SCORE_VALUES_MISSING",
            "valid_for_claim": "False",
        },
        {
            "vector_id": "RV4353_2_public",
            "branch": "public/global MTS",
            "owner_channel": "not deleted",
            "residual_vector": "Delta_local_public retains owner-tail/Kperp unless global parent signatures are supplied",
            "remaining_terms": "global parent adoption and every selector clause",
            "claim_status": "PUBLIC_PROMOTION_BLOCKED",
            "valid_for_claim": "False",
        },
    ]


def arena_rows() -> List[Dict[str, str]]:
    rows: List[Dict[str, str]] = []
    finite_expr = "|Pi_a^RI|C_Lambda|R_Lambda|/lambda_4350 + |Pi_a^BRI||B_RI_bound| + |Pi_a^I||I_RI_bound| + |W_a^K|C_T N_T"
    for arena, bound, units in ARENAS:
        rows.append(
            {
                "arena_id": f"RV4353_{arena}",
                "arena": arena,
                "arena_bound": bound,
                "units": units,
                "clean_owner_channel": "0",
                "finite_owner_channel": finite_expr,
                "nonowner_residual_policy": "must be theorem-zero or source-backed separately; no cancellation with owner channel",
                "claim_status": "NO_ARENA_PASS_FROM_OWNER_CHANNEL_ALONE",
                "valid_for_claim": "False",
            }
        )
    return rows


def remaining_gate_rows() -> List[Dict[str, str]]:
    return [
        {
            "gate_id": "G4353_0_parent_selector",
            "gate": "parent action selector/global adoption",
            "why_remaining": "4353 deletes a private local channel, not the global parent-action adoption problem.",
            "next_evidence": "parent selector clauses signed or branch kept private/quarantined",
            "status": "OPEN_PUBLIC_PROMOTION_GATE",
            "valid_for_claim": "False",
        },
        {
            "gate_id": "G4353_1_source_charge",
            "gate": "H_tau/M_Hdress source charge",
            "why_remaining": "Newtonian source mass must be the same parent-owned Hilbert/Hamiltonian charge used in the local equation.",
            "next_evidence": "H_tau integrability, fixed H_ref, positive M_Hdress and same-worldtube source measure",
            "status": "NEXT_HIGH_LEVERAGE_GATE",
            "valid_for_claim": "False",
        },
        {
            "gate_id": "G4353_2_coupling",
            "gate": "constant source-blind calibrated kappa_eff/G_N",
            "why_remaining": "MTS need not predict numeric G_N, but must avoid species/source/frame/range/readout drift.",
            "next_evidence": "D_A ln kappa_eff=0 or finite drift bounds",
            "status": "OPEN_SOURCE_COUPLING_GATE",
            "valid_for_claim": "False",
        },
        {
            "gate_id": "G4353_3_EM",
            "gate": "Maxwell-Hodge/current/source once-only branch",
            "why_remaining": "EM/Poynting stress is safe only on the same-Hodge/current/no-radiation branch or via finite residual rows.",
            "next_evidence": "same-Hodge/current/radiative branch labels propagated into source charge",
            "status": "CONDITIONAL_BRANCH_NOT_GLOBAL",
            "valid_for_claim": "False",
        },
        {
            "gate_id": "G4353_4_empirical_projection",
            "gate": "arena projection constants and data tests",
            "why_remaining": "Even finite residual rows need source-backed Pi_a and bounds before R10/PPN/clock/orbital scoring.",
            "next_evidence": "projection constants, units, source paths and no-cancellation score runner",
            "status": "OPEN_EMPIRICAL_GATE",
            "valid_for_claim": "False",
        },
    ]


def runner_rows() -> List[Dict[str, str]]:
    return [
        {
            "runner_id": "RUN4353_0_clean",
            "input": "4352 full clean owner-tail branch plus 4346 Kperp private clean branch",
            "action": "DELETE_OWNER_CHANNEL_FROM_PRIVATE_LOCAL_VECTOR",
            "result": "epsilon_owner_tail_Kperp=0",
            "claim_policy": "no public local-GR claim; remaining gates explicit",
            "valid_for_claim": "False",
        },
        {
            "runner_id": "RUN4353_1_finite",
            "input": "any owner-tail/Kperp clean clause open",
            "action": "KEEP_FINITE_OWNER_SCORE",
            "result": "arena rows retain absolute owner-channel expression",
            "claim_policy": "requires real values before scoring",
            "valid_for_claim": "False",
        },
        {
            "runner_id": "RUN4353_2_next",
            "input": "owner channel deleted privately",
            "action": "ATTACK_SOURCE_CHARGE_AND_COUPLING_GATE",
            "result": NEXT_TARGET,
            "claim_policy": "local Newton/GR now lives or dies on source charge/coupling/readout plus parent adoption",
            "valid_for_claim": "False",
        },
    ]


def firewall_rows() -> List[Dict[str, str]]:
    return [
        {
            "firewall_id": "FW4353_0",
            "rule": "Do not call private owner-channel deletion a public local-GR proof.",
            "reason": "Parent selector, source charge, coupling, readout and empirical gates remain.",
            "status": "ACTIVE",
            "valid_for_claim": "False",
        },
        {
            "firewall_id": "FW4353_1",
            "rule": "Do not use owner-tail zero to absorb source-mass or G_N calibration problems.",
            "reason": "The Newtonian source charge and coupling constant are separate gates.",
            "status": "ACTIVE",
            "valid_for_claim": "False",
        },
        {
            "firewall_id": "FW4353_2",
            "rule": "Do not cancel finite owner-channel residuals against nonowner residuals.",
            "reason": "All fallback vectors are absolute/no-cancellation.",
            "status": "ACTIVE",
            "valid_for_claim": "False",
        },
        {
            "firewall_id": "FW4353_3",
            "rule": "Do not treat calibrated G_N as a predicted fundamental constant.",
            "reason": "The accepted route is GR-like calibrated universal coupling plus strict no-drift/source-charge ownership.",
            "status": "ACTIVE",
            "valid_for_claim": "False",
        },
    ]


def decision_rows() -> List[Dict[str, str]]:
    return [
        {
            "decision_id": "DEC4353_0",
            "decision": DECISION,
            "reason": "The Kperp/RI owner-tail channel can now be removed from the private clean local residual vector, because Kperp is privately routed and the RI owner-tail Lambda, boundary and incoming legs vanish on the same compact static branch. This is a real narrowing, not a final local-GR proof: source charge, calibrated coupling/no-drift, parent selector and empirical projection gates remain.",
            "next_action": NEXT_TARGET,
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
    ]


def status_rows() -> List[Dict[str, str]]:
    return [
        {
            "status_id": "STAT4353_0",
            "item": "owner channel",
            "status": "DELETED_FROM_PRIVATE_CLEAN_VECTOR",
            "note": "epsilon_owner_tail_Kperp=0 only on the compact static clean branch.",
        },
        {
            "status_id": "STAT4353_1",
            "item": "finite owner fallback",
            "status": "RETAINED_FOR_OPEN_BRANCHES",
            "note": "absolute owner-tail/Kperp score remains if any branch clause is unsigned.",
        },
        {
            "status_id": "STAT4353_2",
            "item": "remaining high-leverage gate",
            "status": "SOURCE_CHARGE_AND_COUPLING",
            "note": "H_tau/M_Hdress and kappa_eff no-drift are now the best next attack.",
        },
        {
            "status_id": "STAT4353_3",
            "item": "next target",
            "status": "HTAU_MHREF_SOURCE_CHARGE",
            "note": NEXT_TARGET,
        },
    ]


def next_rows() -> List[Dict[str, str]]:
    return [
        {
            "next_target_id": "NT4353_0",
            "next_target": NEXT_TARGET,
            "target_question": "Can the local Newton/GR source charge and calibrated coupling be parent-owned, or must finite G_N/source-drift rows be scored?",
            "preferred_route": "derive same-worldtube H_tau/M_Hdress ownership with fixed H_ref, positive mass denominator and D_A ln kappa_eff=0",
            "fallback_route": "fill finite source-charge, reference, kappa drift, species/frame/range/readout rows for local PPN/R10/clock scoring",
            "valid_for_claim": "False",
        }
    ]


def build_tables() -> Dict[str, List[Dict[str, str]]]:
    return {
        "sources": source_rows(),
        "owner": owner_channel_rows(),
        "vectors": residual_vector_rows(),
        "arenas": arena_rows(),
        "gates": remaining_gate_rows(),
        "runner": runner_rows(),
        "firewall": firewall_rows(),
        "decision": decision_rows(),
        "status": status_rows(),
        "next": next_rows(),
    }


def write_tables(tables: Dict[str, List[Dict[str, str]]]) -> None:
    mapping = {
        "sources": "P8_Y5_R2FR_4353_SOURCE_REGISTER.csv",
        "owner": "P8_Y5_R2FR_4353_OWNER_CHANNEL_ROWS.csv",
        "vectors": "P8_Y5_R2FR_4353_RESIDUAL_VECTOR_ROWS.csv",
        "arenas": "P8_Y5_R2FR_4353_ARENA_ROWS.csv",
        "gates": "P8_Y5_R2FR_4353_REMAINING_GATE_ROWS.csv",
        "runner": "P8_Y5_R2FR_4353_RUNNER.csv",
        "firewall": "P8_Y5_R2FR_4353_CLAIM_FIREWALL.csv",
        "decision": "P8_Y5_R2FR_4353_DECISION.csv",
        "status": "P8_Y5_R2FR_4353_STATUS.csv",
        "next": "P8_Y5_R2FR_4353_NEXT_TARGET.csv",
    }
    for key, filename in mapping.items():
        write_csv(SOURCE_DIR / filename, tables[key])


def write_docs(tables: Dict[str, List[Dict[str, str]]]) -> None:
    formal = f"""# 369 PPC4161 full clean owner-tail to local residual vector or finite score

Marker: `{MARKER}`

Branch: `{BRANCH}`

Decision: `{DECISION}`

## Claim Status

Private nonclaim. This checkpoint deletes one named private local channel from the clean residual vector; it does not prove public local GR, Newtonian mechanics, Maxwell/QED, calibrated `G_N`, R10, PPN, clock, orbital, or WEP safety.

## Result

4353 propagates the 4346-4352 chain into the local residual vector.

Clean private branch:

```text
Kperp_private = 0,
Lambda = 0,
B_RI = 0,
I_RI = 0

=> epsilon_owner_tail_Kperp = 0
=> Delta_local_after_owner = Delta_nonowner_remaining.
```

This is a real narrowing. The `Kperp/RI owner-tail` channel no longer blocks the compact private local branch.

But it is not a public local-GR proof. The surviving high-leverage gates are now:

```text
parent selector adoption,
H_tau/M_Hdress source charge,
constant source-blind kappa_eff/G_N calibration,
same-Hodge/current EM source ownership,
readout/projector/non-EH residuals,
arena projection constants and empirical scoring.
```

If the owner branch is not clean, the finite owner score remains:

```text
epsilon_owner_tail_Kperp <=
  |Pi_a^RI|C_Lambda|R_Lambda|/lambda_4350
  + |Pi_a^BRI||B_RI_bound|
  + |Pi_a^I||I_RI_bound|
  + |W_a^K|C_T N_T.
```

## Source Register

{md_table(tables["sources"], ["source_id", "path", "path_exists", "needle_found", "line_number", "role", "valid_for_claim"])}

## Owner Channel Rows

{md_table(tables["owner"], ["component_id", "component", "clean_branch_value", "reason", "fallback_if_open", "status", "valid_for_claim"])}

## Residual Vector Rows

{md_table(tables["vectors"], ["vector_id", "branch", "owner_channel", "residual_vector", "remaining_terms", "claim_status", "valid_for_claim"])}

## Arena Rows

{md_table(tables["arenas"], ["arena_id", "arena", "arena_bound", "units", "clean_owner_channel", "finite_owner_channel", "nonowner_residual_policy", "claim_status", "valid_for_claim"])}

## Remaining Gate Rows

{md_table(tables["gates"], ["gate_id", "gate", "why_remaining", "next_evidence", "status", "valid_for_claim"])}

## Runner

{md_table(tables["runner"], ["runner_id", "input", "action", "result", "claim_policy", "valid_for_claim"])}

## Claim Firewall

{md_table(tables["firewall"], ["firewall_id", "rule", "reason", "status", "valid_for_claim"])}

## Decision

{md_table(tables["decision"], ["decision_id", "decision", "reason", "next_action", "claim_allowed", "valid_for_claim"])}

## Status

{md_table(tables["status"], ["status_id", "item", "status", "note"])}

## Next Target

{md_table(tables["next"], ["next_target_id", "next_target", "target_question", "preferred_route", "fallback_route", "valid_for_claim"])}
"""
    post = f"""# 4353 Y5-R2FR full clean owner-tail to local residual vector or finite score

Marker: `{MARKER}`

Decision: `{DECISION}`

## Result

4353 propagates the clean owner branch:

```text
epsilon_owner_tail_Kperp = 0
```

inside the private compact static selector. If any owner clause opens, the finite no-cancellation score remains. The next serious blocker is now source charge and calibrated coupling, not the owner-tail channel.

## Next

{md_table(tables["next"], ["next_target", "target_question", "preferred_route", "fallback_route"])}
"""
    FORMAL_PATH.write_text(formal, encoding="utf-8")
    DOC_PATH.write_text(post, encoding="utf-8")


def append_claim_once() -> None:
    path = FORMAL / "02-claims-register.csv"
    existing = read_text(path)
    if CLAIM_ID in existing:
        return
    with path.open("a", newline="", encoding="utf-8") as handle:
        if existing and not existing.endswith("\n"):
            handle.write("\n")
        csv.writer(handle).writerow(
            [
                CLAIM_ID,
                "local_gr",
                (
                    "4353 propagates the 4346-4352 chain into the local residual vector. In the compact private clean branch, Kperp is routed out of the independent static-force budget, the RI adjoint multiplier vanishes by the 4350 gap, and B_RI/I_RI vanish by the 4352 boundary/no-incoming theorem, so epsilon_owner_tail_Kperp=0. This deletes one named private local channel from Delta_local. It does not prove public local GR/Newton: parent selector adoption, H_tau/M_Hdress source charge, constant source-blind kappa_eff/G_N calibration, EM/current/Hodge branch labels, readout/projector/non-EH residuals and empirical projection constants remain separate gates. Open owner branches retain the finite no-cancellation score."
                ),
                (
                    "4353 source register, owner channel rows, residual vector rows, arena rows, remaining gate rows, runner, firewall, decision, status, next-target and validation CSV."
                ),
                "private_owner_channel_deleted_from_clean_local_vector_nonclaim",
                (
                    "Attack H_tau/M_Hdress source-charge ownership and kappa_eff no-drift, or fill finite source-charge/G_N drift rows for local arena scoring."
                ),
                (
                    "Calling private owner-channel deletion a public local-GR proof; absorbing source-mass/G_N calibration problems into owner-tail zero; cancelling finite residuals; treating calibrated G_N as a predicted fundamental constant."
                ),
            ]
        )


def append_spine_and_packet() -> None:
    spine_block = f"""

## PPC4161 4353 full clean owner-tail to local residual vector

Marker: `{MARKER}`

4353 propagates the clean owner-tail result into the local residual vector. In the compact private branch:

```text
epsilon_owner_tail_Kperp = 0
```

so the `Kperp/RI owner-tail` channel is deleted from the private clean vector. The remaining gates are now source charge, calibrated no-drift coupling, parent selector adoption, EM/current/Hodge branch labels, readout/projector/non-EH residuals and empirical projection constants. Open owner branches retain a finite no-cancellation score.
"""
    packet_block = f"""

## PPC4161 packet update 4353 owner channel removed from clean vector

Marker: `{PACKET_MARKER}`

Packet update: the private compact local branch no longer has the `Kperp/RI owner-tail` channel as an active blocker. The next high-leverage target is source charge and calibrated coupling: `H_tau/M_Hdress`, fixed reference, positive denominator, and source-blind `kappa_eff`.
"""
    append_once(FORMAL / "07-unification-spine.md", MARKER, spine_block)
    append_once(FORMAL / "180-PPC4161-private-local-packet-integration.md", PACKET_MARKER, packet_block)


def validate(tables: Dict[str, List[Dict[str, str]]]) -> List[Dict[str, str]]:
    checks: List[Tuple[str, bool, str]] = []
    formal_text = read_text(FORMAL_PATH)
    checks.append(("formal_doc_written", FORMAL_PATH.exists(), str(FORMAL_PATH)))
    checks.append(("post_doc_written", DOC_PATH.exists(), str(DOC_PATH)))
    checks.append(("marker_in_formal", MARKER in formal_text, MARKER))
    checks.append(("decision_in_formal", DECISION in formal_text, DECISION))
    checks.append(("owner_zero_present", "epsilon_owner_tail_Kperp = 0" in formal_text, "owner channel zero"))
    checks.append(("remaining_gates_present", "H_tau/M_Hdress source charge" in formal_text, "remaining source gate"))
    checks.append(("finite_score_present", "|W_a^K|C_T N_T" in formal_text, "finite fallback"))
    checks.append(("all_sources_exist", all(row["path_exists"] == "True" for row in tables["sources"]), "source paths"))
    checks.append(("all_needles_found", all(row["needle_found"] == "True" for row in tables["sources"]), "source needles"))
    checks.append(("owner_rows_present", len(tables["owner"]) >= 5, str(len(tables["owner"]))))
    checks.append(("vector_rows_present", len(tables["vectors"]) >= 3, str(len(tables["vectors"]))))
    checks.append(("gate_rows_present", len(tables["gates"]) >= 5, str(len(tables["gates"]))))
    checks.append(("arena_rows_present", len(tables["arenas"]) == len(ARENAS), str(len(tables["arenas"]))))
    checks.append(("no_valid_claim_rows", all(row.get("valid_for_claim") == "False" for rows in tables.values() for row in rows if "valid_for_claim" in row), "all generated claim flags false"))
    checks.append(("claim_row_recorded", CLAIM_ID in read_text(FORMAL / "02-claims-register.csv"), CLAIM_ID))
    checks.append(("spine_marker_recorded", MARKER in read_text(FORMAL / "07-unification-spine.md"), MARKER))
    checks.append(("packet_marker_recorded", PACKET_MARKER in read_text(FORMAL / "180-PPC4161-private-local-packet-integration.md"), PACKET_MARKER))
    for filename in [
        "P8_Y5_R2FR_4353_SOURCE_REGISTER.csv",
        "P8_Y5_R2FR_4353_OWNER_CHANNEL_ROWS.csv",
        "P8_Y5_R2FR_4353_RESIDUAL_VECTOR_ROWS.csv",
        "P8_Y5_R2FR_4353_ARENA_ROWS.csv",
        "P8_Y5_R2FR_4353_REMAINING_GATE_ROWS.csv",
        "P8_Y5_R2FR_4353_RUNNER.csv",
        "P8_Y5_R2FR_4353_CLAIM_FIREWALL.csv",
        "P8_Y5_R2FR_4353_DECISION.csv",
        "P8_Y5_R2FR_4353_STATUS.csv",
        "P8_Y5_R2FR_4353_NEXT_TARGET.csv",
    ]:
        path = SOURCE_DIR / filename
        rows = list(csv.DictReader(path.open(newline="", encoding="utf-8"))) if path.exists() else []
        checks.append((f"csv_{filename}_parse_rows", bool(rows), f"{len(rows)} rows"))
    return [
        {
            "checkpoint": CHECKPOINT,
            "check_id": check_id,
            "passed": str(bool(passed)),
            "detail": detail,
            "valid_for_claim": "False",
        }
        for check_id, passed, detail in checks
    ]


def main() -> None:
    SOURCE_DIR.mkdir(parents=True, exist_ok=True)
    tables = build_tables()
    write_tables(tables)
    write_docs(tables)
    append_claim_once()
    append_spine_and_packet()
    validation_rows = validate(tables)
    write_csv(VALIDATION_PATH, validation_rows)
    failures = [row for row in validation_rows if row["passed"] != "True"]
    print(f"{CHECKPOINT}: wrote 10 csv artifacts plus validation")
    print(f"{CHECKPOINT}: validation rows={len(validation_rows)} failed={len(failures)}")
    if failures:
        for row in failures:
            print(f"FAILED {row['check_id']}: {row['detail']}")
        raise SystemExit(1)


if __name__ == "__main__":
    main()

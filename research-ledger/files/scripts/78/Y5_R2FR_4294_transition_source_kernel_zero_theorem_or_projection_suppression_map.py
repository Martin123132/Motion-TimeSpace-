from __future__ import annotations

import csv
import io
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List, Tuple


ROOT = Path(__file__).resolve().parents[2]
FORMAL = ROOT / "formalization-workbench"
POST = ROOT / "post-checkpoint-work"
SOURCE_DIR = POST / "source-intake" / "mts_residuals"

CHECKPOINT = "4294"
CLAIM_ID = "L-135"
BRANCH = "MTS_R2FR_Y5_TRANSITION_SOURCE_KERNEL_ZERO_THEOREM_OR_PROJECTION_SUPPRESSION_MAP_4294"
DECISION = "CONDITIONAL_SOURCE_KERNEL_ZERO_THEOREM_DERIVED_PARENT_SIGNATURE_STILL_REQUIRED_NONCLAIM"
MARKER = "PPC4161_TRANSITION_SOURCE_KERNEL_ZERO_THEOREM_4294"
PACKET_MARKER = "PPC4161_PACKET_TRANSITION_SOURCE_KERNEL_ZERO_THEOREM_4294"
NEXT_TARGET = "4295-Y5-R2FR-parent-action-source-kernel-signature-search-and-leak-projector-reduction.md"

FORMAL_PATH = FORMAL / "310-PPC4161-transition-source-kernel-zero-theorem-or-projection-suppression-map.md"
DOC_PATH = POST / "4294-Y5-R2FR-transition-source-kernel-zero-theorem-or-projection-suppression-map.md"
VALIDATION_PATH = SOURCE_DIR / "P8_Y5_BRR545_4294_VALIDATION.csv"

STAMP = datetime.now(timezone.utc).replace(microsecond=0).isoformat()

EPSILON_AJ_SEED = 0.08394692185032419

SOURCES: Dict[str, Tuple[Path, str, str]] = {
    "SRC4294_00_4293_formal": (
        FORMAL / "309-PPC4161-epsilon-mu-tr-shared-local-bound-runner-WEP-R10-PPN-clocks-orbital.md",
        "order-one projection of epsilon_AJ_seed into local observables fails.",
        "4293 is the pressure map this theorem tries to route around without cheating.",
    ),
    "SRC4294_01_4293_required": (
        SOURCE_DIR / "P8_Y5_R2FR_4293_REQUIRED_SUPPRESSION_ROWS.csv",
        "REQ4293_WEP",
        "4293 required-suppression rows supply the fallback if the zero theorem is not parent-signed.",
    ),
    "SRC4294_02_4293_contract": (
        SOURCE_DIR / "P8_Y5_R2FR_4293_EPSILON_PROJECTION_CONTRACT.csv",
        "PC4293_R10",
        "4293 projection contract identifies which observable sees which leakage component.",
    ),
    "SRC4294_03_4293_degeneracy": (
        SOURCE_DIR / "P8_Y5_R2FR_4293_DEGENERACY_LEDGER.csv",
        "DEG4293_0_universal_static_monopole",
        "4293 degeneracy ledger separates common static monopole from observable leakage.",
    ),
    "SRC4294_04_4292_membership": (
        FORMAL / "308-PPC4161-transition-membership-and-nonEH-monopole-zero-or-shared-residual-vector.md",
        "mu_extra_tr = 0",
        "4292 gives the Hilbert-owned l=0 zero inside the membership selector.",
    ),
    "SRC4294_05_4291_selector": (
        FORMAL / "307-PPC4161-PiM-Htau-private-selector-glue-reactivation-or-residual-transfer.md",
        "transition same-worldtube membership",
        "4291 identifies same-worldtube membership as the live local-source blocker.",
    ),
    "SRC4294_06_Gcal_Newton": (
        FORMAL / "194-PPC4161-calibrated-source-coupling-kappa-to-GN-law.md",
        "Phi_N = -G_cal M_H^dress/r",
        "194 gives the calibrated Newtonian source readout and common GM absorption law.",
    ),
    "SRC4294_07_PPN_vector": (
        FORMAL / "188-PPC4161-full-PPN-readout-vector.md",
        "gamma = 1.",
        "188 gives the private EH/PPN readout where Hilbert source descent has gamma=beta=1.",
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
    fieldnames = list(rows[0].keys()) if rows else []
    for row in rows:
        for key in row:
            if key not in fieldnames:
                fieldnames.append(key)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        if fieldnames:
            writer.writeheader()
            writer.writerows(rows)


def csv_rows(path: Path) -> List[Dict[str, str]]:
    if not path.exists():
        return []
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def csv_line(values: List[str]) -> str:
    handle = io.StringIO()
    writer = csv.writer(handle, lineterminator="")
    writer.writerow(values)
    return handle.getvalue()


def append_unique_block(path: Path, marker: str, heading: str, body: str) -> None:
    text = read_text(path)
    if marker in text:
        return
    block = f"\n\n## {heading}\n\nMarker: `{marker}`\n\n{body}\n"
    write_text(path, text.rstrip() + block)


def append_claim() -> None:
    path = FORMAL / "02-claims-register.csv"
    text = read_text(path)
    if any(line.startswith(f"{CLAIM_ID},") for line in text.splitlines()):
        return
    row = csv_line(
        [
            CLAIM_ID,
            "local_gr",
            (
                "4294 derives the conditional source-kernel zero theorem. If the transition residue is a same-metric, "
                "same-worldtube, Hilbert-owned, static, l=0, universal, range-hair-free source contribution before readout, "
                "then the leak projector P_leak annihilates it: WEP, R10, Gdot, PPN gamma/beta, clock and orbital residual "
                "channels all receive zero first-order contribution. This is not a local-GR claim because the current corpus "
                "has not parent-signed the source-kernel clauses for the raw transition shell."
            ),
            (
                "4294 source register, source-kernel clauses, parent-action signature, zero outcome map, leak-projector "
                "control cases, decision, firewall, status and validation rows."
            ),
            "private_conditional_source_kernel_zero_theorem_nonclaim",
            (
                "Search the parent action for the source-kernel signature, or reduce P_leak q_tr directly to prove the "
                "4293 projection coefficients vanish or meet their required suppression bounds."
            ),
            (
                "Treating the conditional theorem as already parent-signed, claiming local-GR/R10/WEP pass, or hiding "
                "non-kernel leakage inside calibrated GM."
            ),
        ]
    )
    path.write_text(text.rstrip() + "\n" + row + "\n", encoding="utf-8")


def requirement_lookup() -> Dict[str, Dict[str, str]]:
    return {row.get("requirement_id", ""): row for row in csv_rows(SOURCE_DIR / "P8_Y5_R2FR_4293_REQUIRED_SUPPRESSION_ROWS.csv")}


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


def zero_theorem_clause_rows() -> List[Dict[str, str]]:
    raw = [
        (
            "ZK4294_0_same_metric_Hilbert_source",
            "S_tr^H = integral sqrt(-g_obs) L_tr(g_obs, chi; tau)",
            "T_tr^{mu nu}=-(2/sqrt(-g_obs)) delta S_tr^H/delta g_obs_{mu nu}",
            "UNSIGNED_PARENT_CLAUSE",
            "puts the transition in the same observed metric source sector instead of an external force",
        ),
        (
            "ZK4294_1_same_worldtube_before_readout",
            "supp J_tr^H subset W_H before M_H^dress readout",
            "M_H^dress -> M_H^dress + M_tr^H",
            "UNSIGNED_PARENT_CLAUSE",
            "lets the l=0 transition source be calibrated as ordinary source charge",
        ),
        (
            "ZK4294_2_static_l0_exterior",
            "partial_t M_tr^H=0 and Q_{l>=1,tr}=0",
            "Phi_tr_ext = -G_cal M_tr^H/r",
            "UNSIGNED_PARENT_CLAUSE",
            "kills Gdot and multipole/orbital anisotropy leakage",
        ),
        (
            "ZK4294_3_universal_species_blind",
            "delta S_tr^H/delta psi_species has no composition-dependent source charge",
            "eta_source_AB=0",
            "UNSIGNED_PARENT_CLAUSE",
            "kills WEP composition leakage",
        ),
        (
            "ZK4294_4_no_finite_range_hair",
            "no independent propagating Yukawa/range mode in the local residue",
            "alpha_tr(lambda)=0",
            "UNSIGNED_PARENT_CLAUSE",
            "kills R10 finite-range leakage",
        ),
        (
            "ZK4294_5_EH_local_metric_readout",
            "local observed metric obeys the same EH/PPN readout used in 188",
            "gamma=1, beta=1, alpha_clock=0 after common GM absorption",
            "PRIVATE_SELECTOR_SIGNED_BUT_PARENT_BRANCH_DEPENDENT",
            "keeps the transition source from changing gamma/beta/clock readout",
        ),
        (
            "ZK4294_6_leak_projector_zero",
            "P_leak := I - P_Hilbert_l0_static_universal_rangefree_same_metric",
            "P_leak q_tr = 0",
            "DERIVED_IF_ZK4294_0_TO_ZK4294_5",
            "single compact statement of the source-kernel theorem",
        ),
    ]
    return [
        {
            **common(),
            "clause_id": clause_id,
            "clause": clause,
            "mathematical_effect": effect,
            "status": status,
            "why_it_matters": why,
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
        for clause_id, clause, effect, status, why in raw
    ]


def parent_signature_rows() -> List[Dict[str, str]]:
    raw = [
        (
            "PS4294_0_action_split",
            "S_parent = S_EH[g_obs] + S_matter[g_obs,psi] + S_EM[g_obs,A] + S_tr^H[g_obs,chi;tau] + S_leak",
            "S_leak must vanish or be bounded locally",
        ),
        (
            "PS4294_1_Hilbert_descent",
            "T_tr^{mu nu}=-(2/sqrt(-g_obs)) delta S_tr^H/delta g_obs_{mu nu}, nabla_mu T_tr^{mu nu}=0",
            "diffeomorphism invariance makes it source stress, not external q_loc forcing",
        ),
        (
            "PS4294_2_worldtube_membership",
            "supp T_tr subset W_H and M_tr^H=int_W_H rho_tr dV is read before M_H^dress calibration",
            "prevents double-counting and lets GM absorb the monopole",
        ),
        (
            "PS4294_3_kernel_projection",
            "P_kernel q_tr=q_tr and P_leak q_tr=0",
            "this is the exact algebraic target for future parent-action proof",
        ),
        (
            "PS4294_4_observable_nulls",
            "(eta_source_AB, alpha_tr(lambda), dln_mu/dt, gamma-1, beta-1, alpha_clock, delta_orbit)_tr = 0",
            "turns the 4293 bounds into automatic zeros rather than tiny fitted coefficients",
        ),
    ]
    return [
        {
            **common(),
            "signature_id": signature_id,
            "required_parent_signature": signature,
            "role": role,
            "status": "CONTRACT_REQUIRED_NOT_YET_PARENT_SIGNED",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
        for signature_id, signature, role in raw
    ]


def zero_outcome_rows() -> List[Dict[str, str]]:
    reqs = requirement_lookup()
    mapping = [
        ("ZO4294_EPSILON", "epsilon_mu_tr", "mu_extra_tr/(G_cal M_H^dress)", "mu_extra_tr=0 for Hilbert-owned l=0 source", "membership clauses"),
        ("ZO4294_WEP", "eta_source_AB", "Y_WEP", "Y_WEP=0 under universal species-blind source", "REQ4293_WEP"),
        ("ZO4294_GAMMA", "gamma_minus_1", "Y_gamma", "Y_gamma=0 under EH same-metric readout plus common GM absorption", "REQ4293_GAMMA"),
        ("ZO4294_BETA", "beta_minus_1", "Y_beta", "Y_beta=0 under EH same-metric readout plus common GM absorption", "REQ4293_BETA"),
        ("ZO4294_CLOCK", "alpha_clock", "Y_clock", "Y_clock=0 under same clock/metric frame and common GM absorption", "REQ4293_CLOCK"),
        ("ZO4294_ORBIT", "delta_orbit_combo", "Y_orbit", "Y_orbit=0 under static l=0 common GM source and EH readout", "REQ4293_ORBIT"),
        ("ZO4294_GDOT", "Gdot_over_G", "T_drift", "d epsilon_mu_tr/dt=0 under static source-kernel membership", "REQ4293_GDOT_TIMESCALE"),
        ("ZO4294_R10", "alpha_tr(lambda)", "Y_R10(lambda)", "alpha_tr(lambda)=0 when no finite-range hair exists", "REQ4293_R10_ANCHOR"),
    ]
    rows: List[Dict[str, str]] = []
    for outcome_id, observable, coefficient, zero_law, req_id in mapping:
        req = reqs.get(req_id, {})
        rows.append(
            {
                **common(),
                "outcome_id": outcome_id,
                "observable": observable,
                "coefficient_or_channel": coefficient,
                "source_kernel_zero_law": zero_law,
                "prediction_under_source_kernel": "0",
                "fallback_requirement_from_4293": req.get("required_value", "membership clause has no 4293 scalar fallback"),
                "fallback_units": req.get("units", "not_applicable"),
                "status": "ZERO_IF_SOURCE_KERNEL_PARENT_SIGNED_ELSE_USE_4293_BOUND",
                "claim_allowed": "False",
                "valid_for_claim": "False",
            }
        )
    return rows


def control_case_rows() -> List[Dict[str, str]]:
    controls = [
        ("CTRL4294_exact_kernel", True, True, True, True, True, True, "PASS_ALL_LOCAL_RESIDUALS_ZERO"),
        ("CTRL4294_membership_unsigned", False, False, True, True, True, True, "FAIL_THEOREM_NOT_AVAILABLE"),
        ("CTRL4294_species_leak", True, True, True, False, True, True, "FAIL_WEP_LIVE"),
        ("CTRL4294_range_hair", True, True, True, True, False, True, "FAIL_R10_LIVE"),
        ("CTRL4294_time_multipole", True, True, False, True, True, True, "FAIL_GDOT_ORBIT_MULTIPOLE_LIVE"),
        ("CTRL4294_nonEH_readout", True, True, True, True, True, False, "FAIL_PPN_CLOCK_LIVE"),
        ("CTRL4294_worldtube_missing", True, False, True, True, True, True, "FAIL_GM_ABSORPTION_NOT_SIGNED"),
    ]
    rows: List[Dict[str, str]] = []
    for control_id, hilbert, worldtube, static_l0, species_blind, range_free, eh_readout, expected_outcome in controls:
        exact_kernel = hilbert and worldtube and static_l0 and species_blind and range_free and eh_readout
        if exact_kernel:
            actual_outcome = "PASS_ALL_LOCAL_RESIDUALS_ZERO"
        elif not hilbert:
            actual_outcome = "FAIL_THEOREM_NOT_AVAILABLE"
        elif not worldtube:
            actual_outcome = "FAIL_GM_ABSORPTION_NOT_SIGNED"
        elif not species_blind:
            actual_outcome = "FAIL_WEP_LIVE"
        elif not range_free:
            actual_outcome = "FAIL_R10_LIVE"
        elif not static_l0:
            actual_outcome = "FAIL_GDOT_ORBIT_MULTIPOLE_LIVE"
        elif not eh_readout:
            actual_outcome = "FAIL_PPN_CLOCK_LIVE"
        else:
            actual_outcome = "FAIL_UNCLASSIFIED_LEAK"
        rows.append(
            {
                **common(),
                "control_id": control_id,
                "same_metric_Hilbert_source": str(hilbert),
                "same_worldtube_before_readout": str(worldtube),
                "static_l0_exterior": str(static_l0),
                "universal_species_blind": str(species_blind),
                "range_hair_free": str(range_free),
                "EH_metric_readout": str(eh_readout),
                "P_leak_q_tr_zero": str(exact_kernel),
                "actual_outcome": actual_outcome,
                "expected_outcome": expected_outcome,
                "expected_matches_actual": str(actual_outcome == expected_outcome),
                "claim_allowed": "False",
                "valid_for_claim": "False",
            }
        )
    return rows


def decision_rows() -> List[Dict[str, str]]:
    return [
        {
            **common(),
            "decision_id": "D4294_0",
            "decision": DECISION,
            "what_moved": "4294 derives the exact way 4293's harsh bounds can be escaped without tuning: put q_tr in the source kernel so P_leak q_tr=0.",
            "theorem_status": "conditional theorem derived; parent signature not yet located/signed for the raw transition shell",
            "fallback_if_not_signed": "use 4293 suppression bounds for Y_WEP,Y_gamma,Y_beta,Y_clock,Y_orbit,T_drift,alpha_tr(lambda)",
            "next_target": NEXT_TARGET,
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
    ]


def firewall_rows() -> List[Dict[str, str]]:
    raw = [
        ("FW4294_0_conditional_only", "The source-kernel zero theorem is conditional until the parent action signs every kernel clause."),
        ("FW4294_1_no_common_GM_overreach", "Common GM absorption does not absorb species, range, time, multipole, or non-EH metric leakage."),
        ("FW4294_2_no_R10_claim", "Range-free source-kernel membership is a theorem route, not an R10 empirical pass."),
        ("FW4294_3_no_tiny_fit_substitute", "If P_leak q_tr is not zero, 4293's numeric suppression requirements still apply."),
        ("FW4294_4_no_public_local_GR", "No local-GR/Newton/Maxwell pass is claimed from the conditional theorem alone."),
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
            "status_id": "STATUS4294_0",
            "result": "CONDITIONAL_SOURCE_KERNEL_ZERO_THEOREM_DERIVED",
            "P_leak_q_tr_zero_under_kernel": "True",
            "parent_signature_found_for_raw_transition_shell": "False",
            "epsilon_AJ_seed": f"{EPSILON_AJ_SEED:.16g}",
            "best_route": "search parent action for source-kernel signature before fitting tiny projection coefficients",
            "next_target": NEXT_TARGET,
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
    ]


def next_target_rows() -> List[Dict[str, str]]:
    return [
        {
            **common(),
            "target_id": "NEXT4294_0",
            "next_target": NEXT_TARGET,
            "objective": "Inspect parent-action/corpus material for a real source-kernel signature or directly reduce P_leak q_tr.",
            "success_condition": "Either all source-kernel clauses are parent-signed, or each nonzero leak projection is bounded by the 4293 required suppression rows.",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
    ]


def formal_doc() -> str:
    reqs = requirement_lookup()
    return f"""
# 310 transition source-kernel zero theorem or projection suppression map

Marker: `{MARKER}`

Branch: `{BRANCH}`

Decision: `{DECISION}`

## The move

4293 showed that an order-one projection of

```text
epsilon_mu_tr = {EPSILON_AJ_SEED:.17g}
```

into local observables is dead. 4294 derives the non-tuning escape route:

```text
P_leak q_tr = 0.
```

Define the source-kernel projector:

```text
P_kernel := P_Hilbert,l=0,static,universal,range-free,same-metric,same-worldtube,
P_leak   := I - P_kernel.
```

If

```text
q_tr = P_kernel q_tr,
```

then the transition residue is only a common static Hilbert monopole before readout. It renormalizes the local source charge:

```text
M_H^dress -> M_H^dress + M_tr^H,
Phi_N = -G_cal (M_H^dress + M_tr^H)/r,
```

and produces no first-order local precision residuals.

## Conditional theorem

If the parent action signs all clauses:

```text
same-metric Hilbert source,
same-worldtube before readout,
static l=0 exterior,
universal/species-blind coupling,
no finite-range hair,
EH local metric readout,
```

then:

```text
epsilon_mu_tr = 0       for the non-Hilbert monopole channel,
eta_source_AB = 0,
alpha_tr(lambda) = 0,
dln_mu_tr/dt = 0,
gamma - 1 = 0,
beta - 1 = 0,
alpha_clock = 0,
delta_orbit_combo = 0.
```

That is the clean route: not tiny tuning, but a kernel membership proof.

## If the theorem does not close

Then the 4293 suppression bounds remain live:

```text
Y_WEP   <= {reqs.get('REQ4293_WEP', {}).get('required_value', 'MISSING')}
Y_gamma <= {reqs.get('REQ4293_GAMMA', {}).get('required_value', 'MISSING')}
Y_beta  <= {reqs.get('REQ4293_BETA', {}).get('required_value', 'MISSING')}
Y_clock <= {reqs.get('REQ4293_CLOCK', {}).get('required_value', 'MISSING')}
Y_orbit <= {reqs.get('REQ4293_ORBIT', {}).get('required_value', 'MISSING')}
T_drift >= {reqs.get('REQ4293_GDOT_TIMESCALE', {}).get('required_value', 'MISSING')} yr.
```

## Status

This is progress, but it is not a claim. The theorem is derived as a conditional field-theory route. The parent action still has to sign the source-kernel clauses for the raw transition shell.

Next target: `{NEXT_TARGET}`.
"""


def checkpoint_doc() -> str:
    return f"""
# 4294 Y5 R2FR transition source-kernel zero theorem

## Purpose

4294 tries the derivation-first path after the harsh 4293 bounds: can the transition residual be put in an exact source kernel so the local observables see zero leakage?

## Outcome

Yes, conditionally. If `q_tr` is same-metric Hilbert, same-worldtube, static, l=0, universal, range-free and read through the EH local metric branch, then:

```text
P_leak q_tr = 0.
```

This kills WEP/R10/Gdot/PPN/clock/orbital first-order leakage without fitting tiny coefficients.

## Not closed yet

The current corpus has not parent-signed those clauses for the raw transition shell. If the parent signature is not found, the 4293 projection-suppression bounds remain live.
"""


def validation_rows(paths: Dict[str, Path]) -> List[Dict[str, str]]:
    sources = csv_rows(paths["sources"])
    clauses = csv_rows(paths["zero_theorem_clauses"])
    signature = csv_rows(paths["parent_signature"])
    outcomes = csv_rows(paths["zero_outcomes"])
    controls = csv_rows(paths["control_cases"])
    no_claim_rows = True
    for key, path in paths.items():
        if key == "validation":
            continue
        for row in csv_rows(path):
            if row.get("claim_allowed") == "True" or row.get("valid_for_claim") == "True":
                no_claim_rows = False
    validations = [
        ("VAL4294_0_sources_exist", bool(sources) and all(row["exists"] == "True" for row in sources), "all cited local sources exist"),
        ("VAL4294_1_needles_found", bool(sources) and all(row["required_text_found"] == "True" for row in sources), "all source needles found"),
        (
            "VAL4294_2_kernel_clause_complete",
            bool(clauses)
            and any(row["clause_id"] == "ZK4294_6_leak_projector_zero" and row["mathematical_effect"] == "P_leak q_tr = 0" for row in clauses)
            and sum(row["status"].startswith("UNSIGNED") for row in clauses) >= 5,
            "kernel theorem contains leak projector zero and unsigned parent clauses",
        ),
        (
            "VAL4294_3_parent_signature_contract",
            bool(signature)
            and any(row["signature_id"] == "PS4294_3_kernel_projection" and "P_leak q_tr=0" in row["required_parent_signature"] for row in signature),
            "parent-action signature contract includes P_leak target",
        ),
        (
            "VAL4294_4_zero_outcomes_cover_4293",
            {row["observable"] for row in outcomes}
            == {
                "epsilon_mu_tr",
                "eta_source_AB",
                "gamma_minus_1",
                "beta_minus_1",
                "alpha_clock",
                "delta_orbit_combo",
                "Gdot_over_G",
                "alpha_tr(lambda)",
            }
            and all(row["prediction_under_source_kernel"] == "0" for row in outcomes),
            "zero outcome map covers the local bound arenas",
        ),
        (
            "VAL4294_5_control_cases",
            bool(controls) and all(row["expected_matches_actual"] == "True" for row in controls),
            "control cases distinguish exact kernel from live leaks",
        ),
        ("VAL4294_6_formal_doc", FORMAL_PATH.exists() and MARKER in read_text(FORMAL_PATH), "formal document exists with marker"),
        ("VAL4294_7_checkpoint_doc", DOC_PATH.exists() and CHECKPOINT in read_text(DOC_PATH), "post-checkpoint document exists"),
        (
            "VAL4294_8_claim_row",
            any(line.startswith(f"{CLAIM_ID},") for line in read_text(FORMAL / "02-claims-register.csv").splitlines()),
            "claims register contains L-135 private nonclaim row",
        ),
        (
            "VAL4294_9_spine_packet",
            MARKER in read_text(FORMAL / "07-unification-spine.md")
            and PACKET_MARKER in read_text(FORMAL / "180-PPC4161-private-local-packet-integration.md"),
            "spine and packet markers exist",
        ),
        ("VAL4294_10_no_claim_rows", no_claim_rows, "all generated rows remain nonclaim rows"),
    ]
    for name, path in paths.items():
        if name == "validation":
            continue
        validations.append((f"VAL4294_csv_{name}", bool(csv_rows(path)), f"{path.name} parses with rows"))
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
        "sources": SOURCE_DIR / "P8_Y5_R2FR_4294_SOURCE_REGISTER.csv",
        "zero_theorem_clauses": SOURCE_DIR / "P8_Y5_R2FR_4294_SOURCE_KERNEL_ZERO_THEOREM_CLAUSES.csv",
        "parent_signature": SOURCE_DIR / "P8_Y5_R2FR_4294_PARENT_ACTION_SIGNATURE_CONTRACT.csv",
        "zero_outcomes": SOURCE_DIR / "P8_Y5_R2FR_4294_ZERO_OUTCOME_MAP.csv",
        "control_cases": SOURCE_DIR / "P8_Y5_R2FR_4294_LEAK_PROJECTOR_CONTROL_CASES.csv",
        "decision": SOURCE_DIR / "P8_Y5_R2FR_4294_DECISION.csv",
        "firewall": SOURCE_DIR / "P8_Y5_R2FR_4294_CLAIM_FIREWALL.csv",
        "status": SOURCE_DIR / "P8_Y5_R2FR_4294_STATUS.csv",
        "next_target": SOURCE_DIR / "P8_Y5_R2FR_4294_NEXT_TARGET.csv",
        "validation": VALIDATION_PATH,
    }
    write_csv(paths["sources"], source_rows())
    write_csv(paths["zero_theorem_clauses"], zero_theorem_clause_rows())
    write_csv(paths["parent_signature"], parent_signature_rows())
    write_csv(paths["zero_outcomes"], zero_outcome_rows())
    write_csv(paths["control_cases"], control_case_rows())
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
        "PPC4161 4294 transition source-kernel zero theorem",
        (
            "4294 derives the conditional theorem that can make the harsh 4293 local bounds go quiet without tiny tuning: "
            "if `q_tr` lies in the same-metric, same-worldtube, Hilbert, static, l=0, universal, range-free source kernel, "
            "then `P_leak q_tr=0` and the WEP/R10/Gdot/PPN/clock/orbital transition residuals vanish. The parent action "
            "still has to sign this kernel membership for the raw transition shell."
        ),
    )
    append_unique_block(
        FORMAL / "180-PPC4161-private-local-packet-integration.md",
        PACKET_MARKER,
        "4294 packet transition source-kernel theorem",
        (
            "Packet update: local precision safety no longer means hoping `epsilon_mu_tr` is tiny. The clean route is now "
            "`P_leak q_tr=0`; otherwise the 4293 suppression rows remain the fallback empirical map."
        ),
    )
    write_csv(paths["validation"], validation_rows(paths))
    failed = [row for row in csv_rows(paths["validation"]) if row["passed"] != "True"]
    print(f"{CHECKPOINT}: wrote {len(paths) - 1} csv artifacts plus validation")
    print(f"{CHECKPOINT}: validation rows={len(csv_rows(paths['validation']))} failed={len(failed)}")
    print(f"{CHECKPOINT}: decision={DECISION}")
    if failed:
        for row in failed:
            print(f"FAILED {row['check_id']}: {row['description']}")
        raise SystemExit(1)


if __name__ == "__main__":
    main()

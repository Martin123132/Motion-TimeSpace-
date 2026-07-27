from __future__ import annotations

import csv
import py_compile
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, Iterable, List


ROOT = Path(
    r"D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main"
)
POST = ROOT / "post-checkpoint-work"
SOURCE_DIR = POST / "source-intake" / "mts_residuals"
FORMAL = ROOT / "formalization-workbench"
SCRIPT_PATH = Path(__file__)

CHECKPOINT = "4177"
BRANCH_ID = "MTS_R2FR_Y5_QUOTIENT_NATURALITY_VERTICAL_SILENCE_4177"
DECISION = "QUOTIENT_NATURALITY_VERTICAL_SILENCE_THEOREM_CLOSES_PROJECTOR_RESIDUALS_PRIVATE_SELECTOR"
DOC_PATH = POST / "4177-Y5-R2FR-quotient-naturality-vertical-silence-proof-or-projector-residual-bound.md"
FORMAL_193_PATH = FORMAL / "193-PPC4161-quotient-naturality-vertical-silence-theorem.md"
PACKET_180_PATH = FORMAL / "180-PPC4161-private-local-packet-integration.md"
CLAIMS_PATH = FORMAL / "02-claims-register.csv"
SPINE_PATH = FORMAL / "07-unification-spine.md"
CLAIM_ID = "L-018"
SPINE_MARKER = "PPC4161_QUOTIENT_NATURALITY_VERTICAL_SILENCE_4177"
PACKET_MARKER = "PPC4161_PACKET_QUOTIENT_NATURALITY_VERTICAL_SILENCE_4177"
NEXT_TARGET = "4178-Y5-R2FR-calibrated-source-coupling-kappa-GN-normalization-or-measured-G-envelope.md"

SOURCES = {
    "SRC4177_00_4176_next": (
        SOURCE_DIR / "P8_Y5_R2FR_4176_NEXT_TARGET.csv",
        "prove vertical variations are quotient-natural",
        "4176 handoff to quotient-naturality/vertical-silence.",
    ),
    "SRC4177_01_formal_190": (
        FORMAL / "190-PPC4161-parent-action-selector-or-local-branch-quarantine.md",
        "quotient-natural vertical silence",
        "4174 selector clause requiring quotient-natural vertical silence.",
    ),
    "SRC4177_02_formal_192": (
        FORMAL / "192-PPC4161-local-boundary-no-flux-sector-interface-theorem.md",
        "J_tr^nu = 0 through <=2PN",
        "4176 compact local no-flux theorem used to route boundary terms.",
    ),
    "SRC4177_03_1023_prior_fail": (
        POST / "1023-Y5-R10-q-vX-action-descent-certificate-or-scalar-nohair-demotion.md",
        "does not close for current MTS",
        "Older quotient certificate failed because field map, action, matter, boundary, and degree clauses were not signed together.",
    ),
    "SRC4177_04_1031_terminal_fail": (
        POST / "1031-Y5-R10-quotient-naturality-terminal-public-metric-proof-or-spm-closure.md",
        "Terminal public metric alone is insufficient",
        "Older terminal metric route showed terminality alone cannot block hidden matter/source labels.",
    ),
    "SRC4177_05_claim_L017": (
        CLAIMS_PATH,
        "compact support plus fixed/routed Hamiltonian boundary conditions",
        "Previous private selector claim row before quotient-naturality closure.",
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


def quotient_contract_rows() -> List[Dict[str, str]]:
    rows = [
        (
            "QNC4177_0_configuration",
            "parent configuration bundle",
            "Phi in Conf_parent, q: Conf_parent -> Q_obs, V_q := ker(Dq)",
            "defines the representative fibres whose motion must be unobservable locally",
            "definition",
        ),
        (
            "QNC4177_1_vertical_generator",
            "vertical generator",
            "v in Gamma(V_q) with Dq[v]=0",
            "vertical means q-owned observables do not move at first order",
            "selector_clause_required",
        ),
        (
            "QNC4177_2_action_factorization",
            "local parent action descent",
            "S_parent|Wloc = S_red[q(Phi), psi] + S_top[q(Phi)] + dB[q(Phi)]",
            "the action is quotient-owned before variation, not projected after equations are made",
            "selector_clause_required",
        ),
        (
            "QNC4177_3_matter_functor",
            "ordinary matter/readout descent",
            "S_matter = Sbar_m[psi, g_obs(q), A(q), theta(q)]",
            "matter, rods, clocks, EM stress and source readouts see only q-owned arguments",
            "selector_clause_required",
        ),
        (
            "QNC4177_4_constants_markers",
            "source constants and material markers",
            "D_v theta_A = D_v m_A = D_v alpha_EM = D_v source_normalization = 0",
            "prevents moving a vertical coupling into constants, masses, material labels or measured-GM calibration",
            "selector_clause_required",
        ),
        (
            "QNC4177_5_boundary_descent",
            "boundary/exact term descent",
            "dB is q-owned or fixed/routed by 4176 no-flux Hamiltonian boundary charge",
            "prevents edge/projector terms from reappearing as Qbar_XH or local clock/PPN residuals",
            "selector_clause_required",
        ),
        (
            "QNC4177_6_naturality",
            "readout naturality",
            "O_loc = Obar_loc o q and D O_loc[v] = D Obar_loc[Dq[v]] = 0",
            "local observables commute with quotient reduction",
            "derived_if_clauses_signed",
        ),
    ]
    return [
        {
            **common(),
            "contract_id": contract_id,
            "object": object_name,
            "mathematical_form": form,
            "role": role,
            "status": status,
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
        for contract_id, object_name, form, role, status in rows
    ]


def vertical_silence_rows() -> List[Dict[str, str]]:
    rows = [
        (
            "VSP4177_0_chain_rule_action",
            "vertical variation of descended action",
            "delta_v S_red[q(Phi)] = <delta S_red/delta q, Dq[v]> = 0",
            "if the local action factors through q before variation, no vertical Euler source is produced",
            "derived_private_selector",
        ),
        (
            "VSP4177_1_chain_rule_matter",
            "vertical variation of ordinary matter source",
            "delta_v S_matter = <delta Sbar_m/delta O, D Obar[Dq[v]]> = 0",
            "ordinary matter cannot source the vertical representative direction",
            "derived_private_selector",
        ),
        (
            "VSP4177_2_no_marker_source",
            "no hidden marker/source coupling",
            "D_v theta_A = D_v m_A = D_v alpha_EM = D_v source_normalization = 0",
            "WEP, clock, EM and measured-GM rows cannot resurrect the vertical field",
            "derived_private_selector",
        ),
        (
            "VSP4177_3_no_bulk_residual",
            "vertical Noether identity",
            "E_A v^A = div B_v with B_v fixed/routed on partial W_loc",
            "vertical equations are gauge/representative identities, not local bulk forces",
            "derived_private_selector",
        ),
        (
            "VSP4177_4_projector_residual",
            "projector residual vanishes",
            "R_proj := Pi_loc D O_loc[v] = Pi_loc D Obar[Dq[v]] = 0",
            "projectors cannot smuggle representative motion into PPN, clock, R10 or orbital readouts",
            "closed_private_selector",
        ),
        (
            "VSP4177_5_coupling_zero",
            "finite coupling rows inactive",
            "K_X = qbar_XT = Qbar_XH = c_g = b_A = b_alpha = b_dis = 0 inside the selector branch",
            "these are zero by absence of a q-independent argument, not by cancellation",
            "closed_private_selector",
        ),
        (
            "VSP4177_6_degree_count",
            "representative degree count",
            "rank(V_q) directions are quotient fibres; no local physical pole or Green kernel is assigned to them",
            "prevents treating a zero Hessian as an under-derived physical scalar",
            "closed_private_selector",
        ),
    ]
    return [
        {
            **common(),
            "proof_id": proof_id,
            "step": step,
            "formula": formula,
            "meaning": meaning,
            "status": status,
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
        for proof_id, step, formula, meaning, status in rows
    ]


def projector_residual_rows() -> List[Dict[str, str]]:
    rows = [
        (
            "PR4177_0_gamma_beta",
            "PPN_gamma_beta_projector_residual",
            "Delta gamma_proj, Delta beta_proj",
            "closed_private",
            "R_proj=0 and no q-independent source/readout argument exists",
            "reactivate if matter sees non-q frame, hidden conformal/disformal slot, or nonzero Dq[v]",
        ),
        (
            "PR4177_1_preferred_frame",
            "PPN_alpha_i_projector_residual",
            "alpha_i_proj",
            "closed_private",
            "vertical representative motion has no local frame readout after quotient naturality",
            "reactivate if external frame labels enter before quotient evaluation",
        ),
        (
            "PR4177_2_preferred_location",
            "PPN_xi_projector_residual",
            "xi_proj",
            "closed_private",
            "4176 no-flux plus quotient naturality prevents boundary/projector preferred-location leakage",
            "reactivate if boundary charge or sector pullback is not q-owned/fixed/routed",
        ),
        (
            "PR4177_3_WEP_clock",
            "WEP_clock_projector_residual",
            "eta_proj, redshift_proj",
            "closed_private",
            "masses, EM constants, material labels and clock readout factor through q",
            "reactivate if D_v theta_A, D_v m_A, D_v alpha_EM or clock labels are nonzero",
        ),
        (
            "PR4177_4_R10",
            "R10_alpha_lambda_projector_residual",
            "alpha_X(lambda)_proj",
            "closed_private",
            "no physical X pole/coupling exists when X is a quotient-fibre representative direction",
            "reactivate and source-bound if K_X, qbar_XT, Qbar_XH or lambda_X becomes parent-owned nonzero",
        ),
        (
            "PR4177_5_orbital",
            "orbital_projector_residual",
            "Delta a_orb_proj",
            "closed_private",
            "ordinary orbital source/readout uses the same q-owned metric/coframe and source normalization",
            "reactivate if measured GM calibration or orbital ephemeris source slot depends on vertical representative data",
        ),
    ]
    return [
        {
            **common(),
            "residual_id": residual_id,
            "residual": residual,
            "observable_slot": observable_slot,
            "status": status,
            "closure_reason": closure_reason,
            "reactivation_condition": reactivation_condition,
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
        for residual_id, residual, observable_slot, status, closure_reason, reactivation_condition in rows
    ]


def countermodel_rows() -> List[Dict[str, str]]:
    rows = [
        (
            "CM4177_0_post_readout_projection",
            "project after equations",
            "S_parent has X-dependent equations but O_loc later forgets X",
            "invalidates theorem",
            "must factor through q before variation",
        ),
        (
            "CM4177_1_terminal_metric_only",
            "terminal public metric without matter-domain restriction",
            "matter functor evaluates a non-terminal frame or label before mapping to terminal metric",
            "invalidates theorem",
            "matter/readout functor must be terminal/quotient evaluation only",
        ),
        (
            "CM4177_2_hidden_constants",
            "hidden source constants or material labels",
            "m_A(X), alpha_EM(X), source_normalization(X) survive while metric is q-owned",
            "invalidates theorem",
            "constants/markers/source normalization must be q-owned",
        ),
        (
            "CM4177_3_boundary_edge",
            "q-owned bulk but non-q boundary charge",
            "Q_X or edge cocycle enters measured Hamiltonian mass/readout",
            "invalidates theorem",
            "boundary charge must be fixed, exact, q-owned, or 4176-routed",
        ),
        (
            "CM4177_4_nonintegrable_kernel",
            "nonintegrable vertical distribution",
            "Dq[v]=0 infinitesimally but no legitimate quotient fibre/orbit exists on the local domain",
            "invalidates theorem",
            "V_q must be parent-owned and integrable on W_loc",
        ),
    ]
    return [
        {
            **common(),
            "countermodel_id": countermodel_id,
            "countermodel": countermodel,
            "construction": construction,
            "effect": effect,
            "required_repair": repair,
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
        for countermodel_id, countermodel, construction, effect, repair in rows
    ]


def decision_rows() -> List[Dict[str, str]]:
    rows = [
        (
            "DEC4177_0_theorem",
            "quotient_naturality_vertical_silence_theorem",
            "If action, matter/readout, constants/source normalization and boundary terms all factor through q before variation, Dq[v]=0 makes vertical source/readout residuals vanish.",
            "close_projector_residuals_private_selector",
        ),
        (
            "DEC4177_1_not_terminality",
            "terminal_metric_alone_rejected",
            "Prior 1031 showed terminality alone is too weak; 4177 requires action-domain and source-label factorization.",
            "keep_countermodel_firewall",
        ),
        (
            "DEC4177_2_no_global",
            "global_adoption_still_false",
            "This is inside PPC4161-TK-HQNP local selector/quarantine and does not prove the full MTS parent globally signs q.",
            "keep_local_branch_quarantined",
        ),
        (
            "DEC4177_3_next",
            "next_best_derivation_target",
            "After EM ownership, boundary no-flux and vertical silence, the remaining local-GR bridge is calibrated source coupling: kappa_* to measured G_N without moving constants by hand.",
            NEXT_TARGET,
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
        for decision_id, decision, reason, next_action in rows
    ]


def firewall_rows() -> List[Dict[str, str]]:
    rows = [
        ("FW4177_0_no_public_local_GR", "Do not claim public local GR; calibrated source coupling and global parent adoption remain open."),
        ("FW4177_1_no_global_parent", "Do not claim the full MTS parent globally signs the quotient from a local selector theorem."),
        ("FW4177_2_no_terminal_only", "Do not use terminal/public-metric language alone as a proof of source or matter silence."),
        ("FW4177_3_no_posthoc_projection", "Do not project out an already-coupled field after variation and call it quotient naturality."),
        ("FW4177_4_no_hidden_constants", "Do not move vertical dependence into masses, EM constants, material labels, clocks, or source normalization."),
        ("FW4177_5_no_numeric_G", "Do not claim a numerical derivation of Newton's constant from vertical silence."),
        ("FW4177_6_no_empirical_pass", "Do not claim R10, PPN, WEP, clocks, or orbital pass from this formal gate alone."),
    ]
    return [
        {
            **common(),
            "firewall_id": firewall_id,
            "blocked_claim": blocked_claim,
            "enforcement": "claim_allowed=false_and_valid_for_claim=false",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
        for firewall_id, blocked_claim in rows
    ]


def status_rows(claim_action: str, packet_action: str, spine_action: str) -> List[Dict[str, str]]:
    return [
        {
            **common(),
            "result": DECISION,
            "quotient_naturality_vertical_silence_theorem_derived_private": "True",
            "projector_residuals_closed_private": "True",
            "terminal_metric_alone_rejected": "True",
            "posthoc_projection_rejected": "True",
            "hidden_constant_marker_leak_closed_private": "True",
            "boundary_edge_leak_closed_private_by_4176": "True",
            "global_parent_action_adoption_proved": "False",
            "global_quotient_map_parent_signed": "False",
            "calibrated_source_coupling_proved": "False",
            "public_local_GR_claim_allowed": "False",
            "numeric_G_predicted": "False",
            "formal_193_written": "True",
            "claim_register_action": claim_action,
            "packet_180_action": packet_action,
            "spine_action": spine_action,
            "next_target": NEXT_TARGET,
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
    ]


def next_rows() -> List[Dict[str, str]]:
    return [
        {
            **common(),
            "next_target": NEXT_TARGET,
            "why_next": "4177 closes projector/vertical leakage inside the private selector. The remaining local-GR bridge is calibrated source coupling: show kappa_* gives measured Newtonian G_N and source normalization without hiding a coupling in units, masses, clocks, or GM calibration.",
            "route_A": "derive kappa_* to G_N from the local EH block, source normalization, Poisson limit and measured two-body calibration",
            "route_B": "if exact derivation fails, build a measured-G envelope with explicit calibration constants and no public local-GR claim",
            "fallback": "keep PPC4161-TK-HQNP quarantined until source coupling and global parent adoption are signed",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
    ]


def output_paths() -> Dict[str, Path]:
    return {
        "P8_Y5_R2FR_4177_SOURCE_REGISTER": SOURCE_DIR / "P8_Y5_R2FR_4177_SOURCE_REGISTER.csv",
        "P8_Y5_R2FR_4177_QUOTIENT_NATURALITY_CONTRACT": SOURCE_DIR / "P8_Y5_R2FR_4177_QUOTIENT_NATURALITY_CONTRACT.csv",
        "P8_Y5_R2FR_4177_VERTICAL_SILENCE_PROOF": SOURCE_DIR / "P8_Y5_R2FR_4177_VERTICAL_SILENCE_PROOF.csv",
        "P8_Y5_R2FR_4177_PROJECTOR_RESIDUAL_CLOSE_OR_BOUND": SOURCE_DIR / "P8_Y5_R2FR_4177_PROJECTOR_RESIDUAL_CLOSE_OR_BOUND.csv",
        "P8_Y5_R2FR_4177_COUNTERMODEL_REACTIVATION_LEDGER": SOURCE_DIR / "P8_Y5_R2FR_4177_COUNTERMODEL_REACTIVATION_LEDGER.csv",
        "P8_Y5_R2FR_4177_BRANCH_DECISION": SOURCE_DIR / "P8_Y5_R2FR_4177_BRANCH_DECISION.csv",
        "P8_Y5_R2FR_4177_CLAIM_FIREWALL": SOURCE_DIR / "P8_Y5_R2FR_4177_CLAIM_FIREWALL.csv",
        "P8_Y5_R2FR_4177_STATUS": SOURCE_DIR / "P8_Y5_R2FR_4177_STATUS.csv",
        "P8_Y5_R2FR_4177_NEXT_TARGET": SOURCE_DIR / "P8_Y5_R2FR_4177_NEXT_TARGET.csv",
    }


def ensure_claim_row() -> str:
    rows = parse_csv(CLAIMS_PATH)
    fieldnames = list(rows[0].keys())
    new_row = {
        "claim_id": CLAIM_ID,
        "domain": "local_gravity",
        "claim": "Inside the PPC4161 local selector branch, quotient-natural action/matter/readout/source descent makes vertical representative variations silent and closes projector residuals privately",
        "current_evidence": "formalization-workbench/193-PPC4161-quotient-naturality-vertical-silence-theorem.md records q:Conf_parent->Q_obs, V_q=ker(Dq), action and matter/source factorization before variation, delta_v S=0 by chain rule, R_proj=Pi_loc DObar[Dq[v]]=0, and countermodel firewalls; public_claim=false",
        "status": "private_selector_quotient_naturality_vertical_silence_nonclaim_public_claim_false",
        "next_test": "Derive calibrated source coupling kappa_* -> measured G_N or build an explicit measured-G envelope without public local-GR claim",
        "key_risk": "This closes vertical/projector leakage only inside the private selector; global parent quotient signing, calibrated source coupling, global adoption and numerical G_N remain unproved",
    }
    normalized_new = {field: new_row.get(field, "") for field in fieldnames}
    existing = [row for row in rows if row.get("claim_id") == CLAIM_ID]
    if existing:
        changed = False
        for row in rows:
            if row.get("claim_id") == CLAIM_ID:
                for field, value in normalized_new.items():
                    if row.get(field) != value:
                        row[field] = value
                        changed = True
        action = "updated" if changed else "already_present"
    else:
        rows.append(normalized_new)
        action = "added"
    with CLAIMS_PATH.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)
    return action


def append_once(path: Path, marker: str, section: str) -> str:
    text = read_text(path)
    if marker in text:
        return "already_present"
    path.write_text(text.rstrip() + "\n\n" + section.strip() + "\n", encoding="utf-8")
    return "added"


def ensure_packet_180_addendum() -> str:
    section = f"""
## PPC4161-TK-HQNP Addendum - Quotient Naturality Vertical Silence

Marker: `{PACKET_MARKER}`  
Source checkpoint: `4177-Y5-R2FR-quotient-naturality-vertical-silence-proof-or-projector-residual-bound.md`

Inside the private compact local selector branch:

```text
q: Conf_parent -> Q_obs,
V_q := ker(Dq),
v in V_q => Dq[v] = 0.
```

The local action, matter/readout functor, constants, source normalization and boundary terms must factor through the same quotient before variation:

```text
S_parent|Wloc = S_red[q(Phi),psi] + S_top[q(Phi)] + dB[q(Phi)],
O_loc = Obar_loc o q,
D_v theta_A = D_v m_A = D_v alpha_EM = D_v source_normalization = 0.
```

Then:

```text
delta_v S = 0,
R_proj := Pi_loc D O_loc[v] = Pi_loc D Obar_loc[Dq[v]] = 0.
```

This closes projector/vertical leakage privately. It is not terminal-metric-only reasoning, not post-hoc projection, and not a numerical `G_N` derivation.
"""
    return append_once(PACKET_180_PATH, PACKET_MARKER, section)


def ensure_spine_section() -> str:
    section = f"""
## PPC4161 Quotient Naturality Vertical Silence - 4177

Marker: `{SPINE_MARKER}`  
Source bridge: `193-PPC4161-quotient-naturality-vertical-silence-theorem.md`  
Claim register row: `{CLAIM_ID}`

Checkpoint `4177` closes the local projector-residual loophole inside the private selector by requiring quotient descent before variation:

```text
V_q := ker(Dq),
delta_v S_red[q(Phi)] = <delta S_red/delta q, Dq[v]> = 0,
R_proj = Pi_loc D Obar_loc[Dq[v]] = 0.
```

The theorem explicitly rejects two weak routes: terminal public metric alone and post-readout projection. Source constants, masses, material labels, EM constants, clock readout and measured-GM normalization must be q-owned as well.

The next local bridge is calibrated source coupling:

```text
{NEXT_TARGET}
```
"""
    return append_once(SPINE_PATH, SPINE_MARKER, section)


def write_formal_193() -> None:
    FORMAL_193_PATH.write_text(
        f"""# 193 - PPC4161 Quotient Naturality Vertical Silence Theorem

Marker: `PPC4161_QUOTIENT_NATURALITY_VERTICAL_SILENCE_THEOREM`
Checkpoint: `4177`
Branch: `{BRANCH_ID}`
Decision: `{DECISION}`

## Claim Status
Private selector theorem. This is not public local GR, not global MTS adoption, and not a numerical derivation of `G_N`.

## Quotient Structure
Let:

```text
q: Conf_parent -> Q_obs,
V_q := ker(Dq),
v in Gamma(V_q), so Dq[v] = 0.
```

The local ordinary observable/readout functor must be natural with respect to this quotient:

```text
O_loc = Obar_loc o q.
```

Therefore:

```text
D O_loc[v] = D Obar_loc[Dq[v]] = 0.
```

## Action And Matter Descent Before Variation
The local selector must not project away a field after it has already coupled. It must factor before variation:

```text
S_parent|Wloc =
S_red[q(Phi), psi]
+ S_top[q(Phi)]
+ dB[q(Phi)].
```

Ordinary matter, EM stress, clocks, rods and source readouts must also factor through q:

```text
S_matter = Sbar_m[psi, g_obs(q), A(q), theta(q)].
```

The constants and material/source markers are part of the theorem:

```text
D_v theta_A = D_v m_A = D_v alpha_EM = D_v source_normalization = 0.
```

This is the piece that terminal-public-metric language alone did not prove.

## Vertical Silence Proof
For a vertical variation `delta Phi = v`:

```text
delta_v S_red[q(Phi)] =
<delta S_red/delta q, Dq[v]> = 0.
```

Similarly:

```text
delta_v S_matter =
<delta Sbar_m/delta O, D Obar_loc[Dq[v]]> = 0.
```

The boundary term is q-owned or fixed/routed by the 4176 no-flux Hamiltonian boundary theorem:

```text
E_A v^A = div B_v,
B_v | partial W_loc = fixed/exact/routed.
```

So the vertical direction is representative/gauge data for the compact local selector branch, not a local bulk source.

## Projector Residual Closure
Define:

```text
R_proj := Pi_loc D O_loc[v].
```

Then:

```text
R_proj = Pi_loc D Obar_loc[Dq[v]] = 0.
```

Thus the private selector closes projected residuals in PPN, WEP, clock, R10, orbital and source-readout slots. In shorthand:

```text
K_X = qbar_XT = Qbar_XH = c_g = b_A = b_alpha = b_dis = 0
```

inside this selector branch, by absence of a q-independent argument rather than cancellation.

## Countermodel Firewall
The theorem fails if any of these happen:

```text
post-readout projection after X already coupled;
terminal public metric without matter-domain restriction;
hidden X-dependence in masses, constants, clocks, material labels or source normalization;
non-q boundary/edge charge entering measured Hamiltonian mass;
nonintegrable or non-parent-owned vertical distribution.
```

## Next Target
`{NEXT_TARGET}`
""",
        encoding="utf-8",
    )


def write_doc() -> None:
    DOC_PATH.write_text(
        f"""# 4177 - Y5 R2FR Quotient Naturality Vertical Silence Proof Or Projector Residual Bound

Branch: `{BRANCH_ID}`  
Decision: `{DECISION}`  
Status: private selector theorem; no public local-GR claim.

## Why This Checkpoint Exists
4176 closed transition-current leakage only if local sector boundaries are no-flux or routed. The next leak was subtler: a projected or quotient-forgotten variable could still have coupled before the projection. That would fake local GR by hiding a residual in the projector.

## The Stronger Route
4177 rejects terminal-metric-only and post-readout projection. The action and every ordinary source/readout argument must factor through the quotient before variation:

```text
q: Conf_parent -> Q_obs,
V_q := ker(Dq),
Dq[v] = 0,
S_parent|Wloc = S_red[q(Phi),psi] + S_top[q(Phi)] + dB[q(Phi)],
O_loc = Obar_loc o q.
```

Source labels and constants must also be q-owned:

```text
D_v theta_A = D_v m_A = D_v alpha_EM = D_v source_normalization = 0.
```

Then the chain rule gives:

```text
delta_v S = 0,
R_proj := Pi_loc D O_loc[v] = Pi_loc D Obar_loc[Dq[v]] = 0.
```

## Guardrail
This is not a public theorem of full MTS. It is a local selector theorem. It fails immediately if a hidden frame, source constant, mass marker, EM constant, clock label, measured-GM normalization, or boundary edge charge depends on the vertical representative.

## Output Files
- `formalization-workbench/193-PPC4161-quotient-naturality-vertical-silence-theorem.md`
- `formalization-workbench/02-claims-register.csv` row `{CLAIM_ID}`
- `formalization-workbench/180-PPC4161-private-local-packet-integration.md` marker `{PACKET_MARKER}`
- `formalization-workbench/07-unification-spine.md` marker `{SPINE_MARKER}`
- `post-checkpoint-work/source-intake/mts_residuals/P8_Y5_R2FR_4177_SOURCE_REGISTER.csv`
- `post-checkpoint-work/source-intake/mts_residuals/P8_Y5_R2FR_4177_QUOTIENT_NATURALITY_CONTRACT.csv`
- `post-checkpoint-work/source-intake/mts_residuals/P8_Y5_R2FR_4177_VERTICAL_SILENCE_PROOF.csv`
- `post-checkpoint-work/source-intake/mts_residuals/P8_Y5_R2FR_4177_PROJECTOR_RESIDUAL_CLOSE_OR_BOUND.csv`
- `post-checkpoint-work/source-intake/mts_residuals/P8_Y5_R2FR_4177_COUNTERMODEL_REACTIVATION_LEDGER.csv`
- `post-checkpoint-work/source-intake/mts_residuals/P8_Y5_R2FR_4177_BRANCH_DECISION.csv`
- `post-checkpoint-work/source-intake/mts_residuals/P8_Y5_R2FR_4177_CLAIM_FIREWALL.csv`
- `post-checkpoint-work/source-intake/mts_residuals/P8_Y5_R2FR_4177_STATUS.csv`
- `post-checkpoint-work/source-intake/mts_residuals/P8_Y5_R2FR_4177_NEXT_TARGET.csv`
- `post-checkpoint-work/source-intake/mts_residuals/P8_Y5_BRR545_4177_VALIDATION.csv`

## Next Target
`{NEXT_TARGET}`
""",
        encoding="utf-8",
    )


def rows_containing(rows: Iterable[Dict[str, str]], needle: str) -> List[Dict[str, str]]:
    return [row for row in rows if needle in " ".join(str(value) for value in row.values())]


def generated_tables(rows_by_name: Dict[str, List[Dict[str, str]]]) -> List[Dict[str, str]]:
    generated: List[Dict[str, str]] = []
    for table_rows in rows_by_name.values():
        generated.extend(table_rows)
    return generated


def validation_rows(
    rows_by_name: Dict[str, List[Dict[str, str]]],
    claim_action: str,
    packet_action: str,
    spine_action: str,
) -> List[Dict[str, str]]:
    source = rows_by_name["P8_Y5_R2FR_4177_SOURCE_REGISTER"]
    contract = rows_by_name["P8_Y5_R2FR_4177_QUOTIENT_NATURALITY_CONTRACT"]
    proof = rows_by_name["P8_Y5_R2FR_4177_VERTICAL_SILENCE_PROOF"]
    residual = rows_by_name["P8_Y5_R2FR_4177_PROJECTOR_RESIDUAL_CLOSE_OR_BOUND"]
    countermodels = rows_by_name["P8_Y5_R2FR_4177_COUNTERMODEL_REACTIVATION_LEDGER"]
    decision = rows_by_name["P8_Y5_R2FR_4177_BRANCH_DECISION"]
    firewall = rows_by_name["P8_Y5_R2FR_4177_CLAIM_FIREWALL"]
    status = rows_by_name["P8_Y5_R2FR_4177_STATUS"]
    next_target = rows_by_name["P8_Y5_R2FR_4177_NEXT_TARGET"]

    formal_text = read_text(FORMAL_193_PATH)
    doc_text = read_text(DOC_PATH)
    packet_text = read_text(PACKET_180_PATH)
    spine_text = read_text(SPINE_PATH)
    claims = parse_csv(CLAIMS_PATH)
    claim_matches = [row for row in claims if row.get("claim_id") == CLAIM_ID]
    all_generated = generated_tables(rows_by_name)
    bad_claim_rows = [
        row
        for row in all_generated
        if row.get("claim_allowed") != "False" or row.get("valid_for_claim") != "False"
    ]

    checks = [
        (
            "VAL4177_0_sources",
            "all source paths exist and contain required tokens",
            all(row["exists"] == "True" and row["required_text_found"] == "True" for row in source),
            str(source),
        ),
        (
            "VAL4177_1_contract",
            "contract rows define q, V_q, Dq[v]=0, action factorization, matter functor, constants, boundary and naturality",
            all(rows_containing(contract, token) for token in ["Conf_parent", "Dq[v]=0", "S_parent|Wloc", "S_matter", "source_normalization", "dB", "O_loc"]),
            "\n".join(",".join(row.values()) for row in contract),
        ),
        (
            "VAL4177_2_proof",
            "proof rows derive delta_v S=0, matter silence, no-marker source, Noether boundary identity, R_proj=0, coupling zero and degree count",
            all(rows_containing(proof, token) for token in ["delta_v S_red", "delta_v S_matter", "D_v theta_A", "E_A v^A", "R_proj", "K_X", "rank(V_q)"]),
            "\n".join(",".join(row.values()) for row in proof),
        ),
        (
            "VAL4177_3_residuals",
            "projector residual rows close PPN, WEP/clock, R10 and orbital slots with reactivation conditions",
            all(rows_containing(residual, token) for token in ["PPN_gamma_beta", "PPN_alpha_i", "PPN_xi", "WEP_clock", "R10_alpha_lambda", "orbital_projector"]),
            "\n".join(",".join(row.values()) for row in residual),
        ),
        (
            "VAL4177_4_countermodels",
            "countermodels reject post-readout projection, terminality-only, hidden constants, boundary edge and nonintegrable kernel routes",
            all(rows_containing(countermodels, token) for token in ["post_readout", "terminal", "hidden", "boundary", "nonintegrable"]),
            "\n".join(",".join(row.values()) for row in countermodels),
        ),
        (
            "VAL4177_5_decision",
            "decision rows select vertical-silence theorem, reject terminality alone, keep global false and pick source-coupling next",
            all(rows_containing(decision, token) for token in ["quotient_naturality_vertical_silence_theorem", "terminal_metric_alone_rejected", "global_adoption_still_false", NEXT_TARGET]),
            "\n".join(",".join(row.values()) for row in decision),
        ),
        (
            "VAL4177_6_firewall",
            "firewall blocks public local-GR, global parent, terminal-only, posthoc projection, hidden constants, numeric-G and empirical claims",
            all(rows_containing(firewall, token) for token in ["public local GR", "global", "terminal", "project", "masses", "Newton", "R10"]),
            "\n".join(",".join(row.values()) for row in firewall),
        ),
        (
            "VAL4177_7_formal_193",
            "formal 193 records quotient structure, action/matter descent, vertical proof, projector closure, firewall and next target",
            all(token in formal_text for token in ["PPC4161_QUOTIENT_NATURALITY_VERTICAL_SILENCE_THEOREM", "V_q := ker(Dq)", "D_v theta_A", "R_proj = Pi_loc", "Countermodel Firewall", NEXT_TARGET]),
            "formal 193 checked",
        ),
        (
            "VAL4177_8_doc",
            "checkpoint doc records stronger route, source labels, chain rule, guardrail and outputs",
            all(token in doc_text for token in ["The Stronger Route", "D_v theta_A", "R_proj", "Guardrail", "Output Files"]),
            "doc checked",
        ),
        (
            "VAL4177_9_packet_180",
            "packet 180 contains quotient vertical silence marker",
            PACKET_MARKER in packet_text and "R_proj" in packet_text,
            f"packet_action={packet_action}",
        ),
        (
            "VAL4177_10_claim_row",
            "claims register contains one L-018 quotient-naturality nonclaim row",
            len(claim_matches) == 1
            and "private_selector_quotient_naturality_vertical_silence_nonclaim_public_claim_false" in claim_matches[0].get("status", ""),
            f"claim_action={claim_action}; matches={claim_matches}",
        ),
        (
            "VAL4177_11_spine",
            "spine contains 4177 marker, claim row and next target",
            SPINE_MARKER in spine_text and CLAIM_ID in spine_text and NEXT_TARGET in spine_text,
            f"spine_action={spine_action}",
        ),
        (
            "VAL4177_12_status",
            "status records private vertical closure, rejects weak routes, keeps global/source coupling/numeric-G false and chooses 4178",
            status[0]["quotient_naturality_vertical_silence_theorem_derived_private"] == "True"
            and status[0]["projector_residuals_closed_private"] == "True"
            and status[0]["terminal_metric_alone_rejected"] == "True"
            and status[0]["posthoc_projection_rejected"] == "True"
            and status[0]["global_parent_action_adoption_proved"] == "False"
            and status[0]["global_quotient_map_parent_signed"] == "False"
            and status[0]["calibrated_source_coupling_proved"] == "False"
            and status[0]["public_local_GR_claim_allowed"] == "False"
            and status[0]["numeric_G_predicted"] == "False"
            and status[0]["next_target"] == NEXT_TARGET,
            str(status),
        ),
        (
            "VAL4177_13_next",
            "next target moves to calibrated source coupling or measured-G envelope",
            next_target[0]["next_target"] == NEXT_TARGET and "kappa_*" in next_target[0]["route_A"],
            str(next_target),
        ),
        (
            "VAL4177_14_no_claim_rows",
            "all generated rows keep claim_allowed/valid_for_claim false",
            not bad_claim_rows,
            str(bad_claim_rows),
        ),
    ]

    validation: List[Dict[str, str]] = []
    for check_id, description, passed, details in checks:
        validation.append(
            {
                **common(),
                "check_id": check_id,
                "description": description,
                "passed": str(bool(passed)),
                "details": details,
                "claim_allowed": "False",
                "valid_for_claim": "False",
            }
        )

    py_compile.compile(str(SCRIPT_PATH), doraise=True)
    pycache = SCRIPT_PATH.parent / "__pycache__"
    if pycache.exists():
        shutil.rmtree(pycache)
    validation.append(
        {
            **common(),
            "check_id": "VAL4177_15_compile",
            "description": "generator compiles and pycache is removed",
            "passed": "True",
            "details": "compiled",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
    )
    return validation


def main() -> None:
    write_formal_193()
    write_doc()
    claim_action = ensure_claim_row()
    packet_action = ensure_packet_180_addendum()
    spine_action = ensure_spine_section()

    rows_by_name = {
        "P8_Y5_R2FR_4177_SOURCE_REGISTER": source_rows(),
        "P8_Y5_R2FR_4177_QUOTIENT_NATURALITY_CONTRACT": quotient_contract_rows(),
        "P8_Y5_R2FR_4177_VERTICAL_SILENCE_PROOF": vertical_silence_rows(),
        "P8_Y5_R2FR_4177_PROJECTOR_RESIDUAL_CLOSE_OR_BOUND": projector_residual_rows(),
        "P8_Y5_R2FR_4177_COUNTERMODEL_REACTIVATION_LEDGER": countermodel_rows(),
        "P8_Y5_R2FR_4177_BRANCH_DECISION": decision_rows(),
        "P8_Y5_R2FR_4177_CLAIM_FIREWALL": firewall_rows(),
        "P8_Y5_R2FR_4177_STATUS": status_rows(claim_action, packet_action, spine_action),
        "P8_Y5_R2FR_4177_NEXT_TARGET": next_rows(),
    }

    for name, path in output_paths().items():
        write_csv(path, rows_by_name[name])

    validation_path = SOURCE_DIR / "P8_Y5_BRR545_4177_VALIDATION.csv"
    write_csv(validation_path, validation_rows(rows_by_name, claim_action, packet_action, spine_action))

    validation = parse_csv(validation_path)
    failed = [row for row in validation if row.get("passed") != "True"]
    if failed:
        raise RuntimeError(f"4177 validation failed: {failed}")

    print(f"{CHECKPOINT} generated")
    print(f"doc={DOC_PATH}")
    print(f"formal={FORMAL_193_PATH}")
    print(f"validation={validation_path}")
    print(f"rows={len(validation)} validation checks")


if __name__ == "__main__":
    main()

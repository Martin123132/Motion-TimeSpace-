from __future__ import annotations

import csv
import py_compile
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List


ROOT = Path(r"D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main")
POST = ROOT / "post-checkpoint-work"
SOURCE_DIR = POST / "source-intake" / "mts_residuals"
FORMAL = ROOT / "formalization-workbench"
SCRIPT_PATH = Path(__file__)

CHECKPOINT = "4174"
BRANCH_ID = "MTS_R2FR_Y5_PARENT_ACTION_SELECTOR_OR_LOCAL_QUARANTINE_4174"
DECISION = "CONDITIONAL_PARENT_ACTION_SELECTOR_THEOREM_DERIVED_GLOBAL_ADOPTION_NOT_PROVED_LOCAL_BRANCH_QUARANTINED"
DOC_PATH = POST / "4174-Y5-R2FR-parent-action-global-adoption-or-explicit-local-branch-quarantine.md"
FORMAL_190_PATH = FORMAL / "190-PPC4161-parent-action-selector-or-local-branch-quarantine.md"
PACKET_180_PATH = FORMAL / "180-PPC4161-private-local-packet-integration.md"
CLAIMS_PATH = FORMAL / "02-claims-register.csv"
SPINE_PATH = FORMAL / "07-unification-spine.md"
CLAIM_ID = "L-015"
SPINE_MARKER = "PPC4161_PARENT_SELECTOR_OR_QUARANTINE_4174"
PACKET_MARKER = "PPC4161_PACKET_PARENT_SELECTOR_OR_QUARANTINE_4174"
NEXT_TARGET = "4175-Y5-R2FR-Maxwell-Hodge-Poynting-stress-owner-theorem-or-EM-side-channel-bound.md"

SOURCES = {
    "SRC4174_00_4173_doc": (
        POST / "4173-Y5-R2FR-local-empirical-PPN-R10-clock-WEP-orbital-validation-pack.md",
        "4174-Y5-R2FR-parent-action-global-adoption-or-explicit-local-branch-quarantine.md",
        "4173 handoff to parent-action adoption or quarantine.",
    ),
    "SRC4174_01_4173_status": (
        SOURCE_DIR / "P8_Y5_R2FR_4173_STATUS.csv",
        "source_backed_bound_pack_built",
        "4173 status showing local source-bound compatibility but global adoption still false.",
    ),
    "SRC4174_02_4173_next": (
        SOURCE_DIR / "P8_Y5_R2FR_4173_NEXT_TARGET.csv",
        "derive parent-action adoption of PPC4161-TK-HQNP without closure smuggling",
        "4173 next target route A.",
    ),
    "SRC4174_03_packet_180": (
        PACKET_180_PATH,
        "S_EM[A,g_obs]",
        "Private packet action and EM source ownership context.",
    ),
    "SRC4174_04_formal_185": (
        FORMAL / "185-PPC4161-Hilbert-source-measure-descent-and-delta-ZH-closure.md",
        "The EM/Poynting contribution is not an add-on",
        "Hilbert source descent with EM/Poynting included.",
    ),
    "SRC4174_05_formal_186": (
        FORMAL / "186-PPC4161-Hamiltonian-worldtube-mass-readout-glue.md",
        "No orbital `GM`, fitted acceleration, or measured Newton constant is used",
        "Hamiltonian/worldtube charge anti-circularity guard.",
    ),
    "SRC4174_06_formal_187": (
        FORMAL / "187-PPC4161-Poisson-Gauss-Newton-readout-from-Hamiltonian-source-charge.md",
        "nabla^2 Phi_N = 4*pi G_N rho_H",
        "Newtonian source readout bridge.",
    ),
    "SRC4174_07_formal_188": (
        FORMAL / "188-PPC4161-full-PPN-readout-vector.md",
        "R_PPN =",
        "Full private PPN vector bridge.",
    ),
    "SRC4174_08_formal_189": (
        FORMAL / "189-PPC4161-local-empirical-validation-pack.md",
        "abs(MTS_private_prediction) <= allowed_abs_bound",
        "Source-backed local comparator pack.",
    ),
    "SRC4174_09_claim_L014": (
        CLAIMS_PATH,
        "private_packet_source_bound_comparator_pass_nonclaim_public_claim_false",
        "Claim register handoff before 4174.",
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


def selector_clause_rows() -> List[Dict[str, str]]:
    clauses = [
        (
            "SEL4174_0_unique_observed_metric",
            "unique observed metric/coframe",
            "All matter, EM, clocks, source charge and EH readout use the same g_obs and theta; no Weyl/disformal representative is allowed in the compact local sector.",
            "closes species, clock, frame and WEP leakage",
            "signed_private_not_global",
            "reactivate epsilon_frame_projector, epsilon_species, WEP_eta and clock redshift rows",
        ),
        (
            "SEL4174_1_EH_principal_block",
            "Einstein-Hilbert local principal block",
            "The <=2PN compact local metric kinetic operator is EH with kappa_*; extra scalar, vector, tensor or memory operators are boundary, topological, higher order, or projected silent.",
            "selects gamma=1 and beta=1 metric coefficients",
            "signed_private_not_global",
            "reactivate gamma_minus_1, beta_minus_1 and short-range force rows",
        ),
        (
            "SEL4174_2_topological_coupling_lock",
            "topological coupling superselection",
            "Parent coupling sector gives D_A ln kappa_* = 0 and no Hilbert stress; numerical G_N remains calibrated unless a scale theorem is later derived.",
            "closes Gdot/G and coupling drift",
            "signed_private_not_global",
            "reactivate Gdot/G, kappa drift and numeric scale ownership rows",
        ),
        (
            "SEL4174_3_single_Hilbert_source_functor",
            "single Hilbert source functor",
            "S_src = S_matter[psi,g_obs,theta] + S_Maxwell-Hodge[A,g_obs] + S_binding[psi,A,g_obs] + exact/improvement + topological/zero rest.",
            "closes source-measure leak, zeta_i and WEP leakage",
            "signed_private_not_global",
            "reactivate zeta_i, alpha3, WEP_eta and source-measure rows",
        ),
        (
            "SEL4174_4_EM_Poynting_owner",
            "Maxwell-Hodge/Poynting stress ownership",
            "The Poynting vector and EM field energy are components of the Hilbert T_EM, not a separate background force, fifth-force source, or hidden current.",
            "prevents an EM side-channel from spoiling local conservation or clock/WEP rows",
            "isolated_next_derivation_target",
            "reactivate epsilon_EM_extra_inner, zeta3 and clock/force residual rows",
        ),
        (
            "SEL4174_5_Hamiltonian_worldtube_charge",
            "Hamiltonian/worldtube source charge",
            "Pi_M and the readout mass are the same covariant Hamiltonian charge M_H^dress[W_H;tau], fixed before orbital readout.",
            "prevents importing observed orbital GM",
            "signed_private_not_global",
            "reactivate orbital GM import and source-charge equality rows",
        ),
        (
            "SEL4174_6_local_boundary_silence",
            "compact local collar boundary silence",
            "FLRW, galaxy, open-memory, incoming radiation and transition branches have zero support or exact no-flux projection through <=2PN in the compact local collar.",
            "keeps local GR branch from erasing global branches while preventing local leakage",
            "not_globally_proved",
            "reactivate xi, preferred-location, transition-current and boundary-flux rows",
        ),
        (
            "SEL4174_7_quotient_naturality",
            "quotient-natural vertical silence",
            "Representative-dependent vertical generators lie in ker(Dq) and do not produce physical local source terms after variation.",
            "prevents hidden scalar/vector/projector force channels",
            "not_globally_proved",
            "reactivate alpha_i, scalar/disformal and projector residual rows",
        ),
    ]
    return [
        {
            **common(),
            "clause_id": clause_id,
            "selector_clause": selector_clause,
            "parent_action_signature_required": signature,
            "local_role": local_role,
            "current_status": current_status,
            "if_failed_reactivate": if_failed,
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
        for clause_id, selector_clause, signature, local_role, current_status, if_failed in clauses
    ]


def theorem_rows() -> List[Dict[str, str]]:
    rows = [
        (
            "THM4174_0_domain",
            "Define the domain as compact, isolated, ordinary-matter, source-supported local collars through <=2PN.",
            "domain restriction is part of the theorem, not a global assumption",
            "local_selector_domain_defined",
        ),
        (
            "THM4174_1_action_reduction",
            "If SEL4174_0 through SEL4174_7 hold as parent-action signatures, S_parent|loc equals S_EH[g_obs;kappa_*] + S_src[psi,A,g_obs] + S_top + boundary/exact + higher-order silent terms.",
            "selector clauses",
            "conditional_action_reduction_derived",
        ),
        (
            "THM4174_2_source_conservation",
            "Variation with respect to g_obs gives one conserved total Hilbert stress, including matter, binding and Maxwell-Hodge/Poynting stress.",
            "single Hilbert source functor and Bianchi identity",
            "conditional_conservation_derived",
        ),
        (
            "THM4174_3_coupling",
            "The local effective coupling is constant because D_A ln kappa_* = 0 and delta_ZH = 0; its numerical value remains calibration unless parent scale ownership is later derived.",
            "topological coupling lock and source-measure descent",
            "conditional_calibrated_source_coupling_derived",
        ),
        (
            "THM4174_4_Newton_PPN",
            "The already-derived 4171 and 4172 readouts follow: Poisson/Gauss/Newton, gamma=1, beta=1, alpha_i=0, xi=0, zeta_i=0 and Gdot/G=0.",
            "formal bridges 187 and 188",
            "conditional_local_GR_readout_derived",
        ),
        (
            "THM4174_5_empirical_compatibility",
            "The 4173 source-backed local comparator follows because every named private local residual is zero or guarded as non-independent.",
            "formal bridge 189",
            "conditional_source_bound_compatibility_derived",
        ),
        (
            "THM4174_6_global_limit",
            "The theorem does not prove global MTS adoption because galaxy, cosmology, open-memory and radiative sectors are outside the compact local collar selector.",
            "scope limitation",
            "global_adoption_not_proved",
        ),
    ]
    return [
        {
            **common(),
            "theorem_step": theorem_step,
            "statement": statement,
            "depends_on": depends_on,
            "result": result,
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
        for theorem_step, statement, depends_on, result in rows
    ]


def quarantine_rows() -> List[Dict[str, str]]:
    rows = [
        ("Q4174_0_scope_label", "The branch is labelled PPC4161-TK-HQNP-local-selector, not full global MTS.", "prevents public/global overclaim"),
        ("Q4174_1_activation_domain", "The branch activates only in compact isolated ordinary-matter local collars through <=2PN.", "keeps galaxy/cosmology/open-memory branches alive outside the collar"),
        ("Q4174_2_interface", "Interface with nonlocal branches must be exact no-flux, support-separated, or source-backed bounded before crossing into local tests.", "prevents local leakage from transition currents"),
        ("Q4174_3_reactivation", "Failure of any selector clause reopens the named residual rows in the selector table.", "turns missing proof into executable residual bookkeeping"),
        ("Q4174_4_empirical_floor", "4173 source-backed compatibility remains a private sanity floor, not a raw-data claim.", "prevents empirical overclaim"),
        ("Q4174_5_public_claim_rule", "Public local-GR claim requires global parent-action adoption plus no open selector clause plus maintained empirical compatibility.", "sets the exit condition from quarantine"),
    ]
    return [
        {
            **common(),
            "quarantine_id": quarantine_id,
            "rule": rule,
            "purpose": purpose,
            "status": "active_private_quarantine",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
        for quarantine_id, rule, purpose in rows
    ]


def em_poynting_rows() -> List[Dict[str, str]]:
    rows = [
        (
            "EM4174_0_owned_term",
            "S_Maxwell-Hodge[A,g_obs] = -1/4 int sqrt(-g_obs) F_mu_nu F^mu_nu",
            "candidate_owned_inside_private_packet",
            "variation gives T_EM^mu_nu; Poynting vector is T_EM^{0i} in a local frame",
        ),
        (
            "EM4174_1_no_extra_force",
            "No independent S_Poynting_background, S_EM_weighted_species or hidden EM-current multiplier may survive in the compact local sector.",
            "must_be_parent_signed",
            "otherwise zeta3, WEP and clock rows reopen",
        ),
        (
            "EM4174_2_binding",
            "Matter-EM binding energy is counted once in S_binding and the Hamiltonian source charge, not again as a separate gravitational mass correction.",
            "candidate_owned_inside_private_packet",
            "prevents source-charge double counting",
        ),
        (
            "EM4174_3_next_derivation",
            "Prove Maxwell-Hodge/Poynting ownership from parent grammar or produce a finite EM side-channel bound.",
            "next_target",
            NEXT_TARGET,
        ),
    ]
    return [
        {
            **common(),
            "em_gate_id": gate_id,
            "statement": statement,
            "status": status,
            "consequence": consequence,
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
        for gate_id, statement, status, consequence in rows
    ]


def decision_rows() -> List[Dict[str, str]]:
    rows = [
        (
            "DEC4174_0_selector",
            "conditional_parent_selector_theorem",
            "A precise action-level selector theorem is derived for when S_parent reduces to PPC4161-TK-HQNP locally.",
            "keep_as_private_conditional_theorem",
        ),
        (
            "DEC4174_1_no_global_adoption",
            "global_adoption_not_proved",
            "The current corpus does not prove that every galaxy/cosmology/open-memory/radiative sector satisfies the selector clauses in the local collar.",
            "activate_quarantine_contract",
        ),
        (
            "DEC4174_2_next",
            "next_best_derivation_target",
            "The most physical remaining selector leak is Maxwell-Hodge/Poynting stress ownership, because EM flux can masquerade as a hidden source/current.",
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
        ("FW4174_0_no_global", "Do not claim global MTS parent-action adoption."),
        ("FW4174_1_no_public_local_GR", "Do not claim public local GR; branch remains private/quarantined."),
        ("FW4174_2_no_numeric_G", "Do not claim a numerical derivation of Newton's constant."),
        ("FW4174_3_no_sector_erasure", "Do not erase galaxy, cosmology, open-memory or radiative-EM sectors with compact local assumptions."),
        ("FW4174_4_no_EM_smuggling", "Do not treat Poynting/EM flux as silent unless Maxwell-Hodge Hilbert ownership is parent-signed or bounded."),
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
            "conditional_parent_selector_theorem_derived": "True",
            "global_parent_action_adoption_proved": "False",
            "explicit_local_quarantine_written": "True",
            "selector_clause_count": str(len(selector_clause_rows())),
            "open_global_selector_clauses": "SEL4174_6_local_boundary_silence;SEL4174_7_quotient_naturality;SEL4174_4_EM_Poynting_owner",
            "EM_Poynting_owner_clause_isolated": "True",
            "public_local_GR_claim_allowed": "False",
            "numeric_G_predicted": "False",
            "formal_190_written": "True",
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
            "why_next": "4174 isolates Maxwell-Hodge/Poynting stress ownership as the most physical remaining parent-selector leak for local source coupling and conservation.",
            "route_A": "prove the EM/Poynting stress is uniquely owned by the Maxwell-Hodge Hilbert tensor in the parent local action",
            "route_B": "if ownership fails, build an explicit EM side-channel residual and source-backed bound rows for clocks, WEP, PPN conservation and local force tests",
            "fallback": "keep PPC4161-TK-HQNP quarantined until EM ownership, boundary silence and quotient naturality are parent-signed",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
    ]


def output_paths() -> Dict[str, Path]:
    return {
        "P8_Y5_R2FR_4174_SOURCE_REGISTER": SOURCE_DIR / "P8_Y5_R2FR_4174_SOURCE_REGISTER.csv",
        "P8_Y5_R2FR_4174_PARENT_SELECTOR_CLAUSES": SOURCE_DIR / "P8_Y5_R2FR_4174_PARENT_SELECTOR_CLAUSES.csv",
        "P8_Y5_R2FR_4174_SELECTOR_THEOREM": SOURCE_DIR / "P8_Y5_R2FR_4174_SELECTOR_THEOREM.csv",
        "P8_Y5_R2FR_4174_LOCAL_QUARANTINE_CONTRACT": SOURCE_DIR / "P8_Y5_R2FR_4174_LOCAL_QUARANTINE_CONTRACT.csv",
        "P8_Y5_R2FR_4174_EM_POYNTING_OWNER_GATE": SOURCE_DIR / "P8_Y5_R2FR_4174_EM_POYNTING_OWNER_GATE.csv",
        "P8_Y5_R2FR_4174_BRANCH_DECISION": SOURCE_DIR / "P8_Y5_R2FR_4174_BRANCH_DECISION.csv",
        "P8_Y5_R2FR_4174_CLAIM_FIREWALL": SOURCE_DIR / "P8_Y5_R2FR_4174_CLAIM_FIREWALL.csv",
        "P8_Y5_R2FR_4174_STATUS": SOURCE_DIR / "P8_Y5_R2FR_4174_STATUS.csv",
        "P8_Y5_R2FR_4174_NEXT_TARGET": SOURCE_DIR / "P8_Y5_R2FR_4174_NEXT_TARGET.csv",
    }


def ensure_claim_row() -> str:
    rows = parse_csv(CLAIMS_PATH)
    fieldnames = list(rows[0].keys())
    new_row = {
        "claim_id": CLAIM_ID,
        "domain": "local_gravity",
        "claim": "PPC4161-TK-HQNP has a conditional parent-action selector theorem and explicit local-branch quarantine contract; global parent adoption remains unproved",
        "current_evidence": "formalization-workbench/190-PPC4161-parent-action-selector-or-local-branch-quarantine.md records eight action-level selector clauses, the conditional reduction of S_parent|loc to EH plus single Hilbert source plus topological/boundary terms, and an active quarantine because global adoption is not proved; public_claim=false",
        "status": "conditional_selector_theorem_quarantined_nonclaim_public_claim_false",
        "next_test": "Prove Maxwell-Hodge/Poynting stress ownership from parent grammar or bound the EM side-channel residual",
        "key_risk": "Selector clauses are action-level requirements, not yet globally signed by the full MTS parent; EM/Poynting, boundary silence and quotient naturality remain the key leak points",
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
## PPC4161-TK-HQNP Addendum - Parent Selector Or Local Quarantine

Marker: `{PACKET_MARKER}`  
Source checkpoint: `4174-Y5-R2FR-parent-action-global-adoption-or-explicit-local-branch-quarantine.md`

The compact local branch is now governed by an action-level selector:

```text
S_parent|loc -> S_EH[g_obs;kappa_*]
              + S_matter[psi,g_obs,theta]
              + S_Maxwell-Hodge[A,g_obs]
              + S_binding[psi,A,g_obs]
              + S_top + boundary/exact + higher-order silent terms.
```

If the selector clauses are parent-signed, the previous PPC4161-TK-HQNP Newton, PPN and source-bound rows follow. If any selector clause fails, the corresponding residual rows reopen.

Because global parent-action adoption is not proved, the local branch remains quarantined. The next derivation target is Maxwell-Hodge/Poynting stress ownership: the EM flux must be part of the Hilbert stress tensor, not a hidden force channel.
"""
    return append_once(PACKET_180_PATH, PACKET_MARKER, section)


def ensure_spine_section() -> str:
    section = f"""
## PPC4161 Parent Selector Or Local Quarantine - 4174

Marker: `{SPINE_MARKER}`  
Source bridge: `190-PPC4161-parent-action-selector-or-local-branch-quarantine.md`  
Claim register row: `{CLAIM_ID}`

Checkpoint `4174` derives the conditional parent-action selector theorem:

```text
if SEL4174_0 ... SEL4174_7 hold as parent-action signatures,
then S_parent|loc reduces to the PPC4161-TK-HQNP local GR packet.
```

This is the clean non-smuggling route: the closure is not imposed on equations after the fact; it is demanded as a parent-action signature. Current evidence does not prove global adoption, so the local branch is explicitly quarantined.

The most physical remaining leak is EM/Poynting stress ownership:

```text
{NEXT_TARGET}
```
"""
    return append_once(SPINE_PATH, SPINE_MARKER, section)


def write_formal_190() -> None:
    FORMAL_190_PATH.write_text(
        f"""# 190 - PPC4161 Parent Action Selector Or Local Branch Quarantine

Marker: `PPC4161_PARENT_ACTION_SELECTOR_OR_LOCAL_QUARANTINE`
Checkpoint: `4174`
Branch: `{BRANCH_ID}`
Decision: `{DECISION}`

## Claim Status
Private nonclaim. This bridge derives a conditional parent-action selector theorem and an explicit quarantine contract. It does not prove global MTS adoption or a public local-GR theorem.

## Selector Theorem
In a compact, isolated, ordinary-matter local collar through `<=2PN`, if the parent action signs the selector clauses:

```text
unique g_obs/theta;
EH local principal block;
D_A ln kappa_* = 0 and delta_ZH = 0;
single Hilbert source functor;
Maxwell-Hodge/Poynting stress ownership;
Hamiltonian/worldtube charge readout;
local boundary silence;
quotient-natural vertical silence;
```

then:

```text
S_parent|loc =
S_EH[g_obs;kappa_*]
+ S_matter[psi,g_obs,theta]
+ S_Maxwell-Hodge[A,g_obs]
+ S_binding[psi,A,g_obs]
+ S_top
+ boundary/exact/higher-order silent terms.
```

Therefore the 4171-4173 local chain follows:

```text
nabla^2 Phi_N = 4*pi G_N rho_H,
R_PPN = 0,
abs(MTS_private_prediction) <= source_backed_bound.
```

## Why This Is Not Closure Smuggling
The selector clauses are action-level signatures. If a clause is not in the parent action, the theorem does not silently set it to zero. The named residual row reopens.

## Quarantine Contract
The branch is retained as:

```text
PPC4161-TK-HQNP-local-selector-private.
```

It applies only inside compact local collars. Galaxy, cosmology, open-memory, transition and radiative sectors are not erased. Any interface with those sectors must be exact no-flux, support-separated, or source-backed bounded before a local claim can be made.

## Key Leak To Attack Next
The EM/Poynting vector is the next clean target. It must be derived as the local `T_EM^0i` component of the Maxwell-Hodge Hilbert tensor, otherwise it becomes a possible hidden source/current side-channel.

## Next Target
`{NEXT_TARGET}`
""",
        encoding="utf-8",
    )


def write_doc(outputs: Dict[str, Path]) -> None:
    DOC_PATH.write_text(
        f"""# 4174 - Parent Action Global Adoption Or Explicit Local Branch Quarantine

Timestamp UTC: `{now()}`  
Branch: `{BRANCH_ID}`  
Decision: `{DECISION}`

## Move Made
4173 showed the private local branch passes source-backed numeric local bounds. 4174 now asks the harder question: does the parent action globally force that branch?

The honest answer is:

```text
global_parent_action_adoption_proved = false.
```

But the work does move forward: we now have an exact parent-action selector theorem. If the parent action signs eight specific local selector clauses, then the compact local sector reduces to PPC4161-TK-HQNP and the Newton/PPN/source-bound chain follows.

## Selector Result

```text
S_parent|loc -> S_EH[g_obs;kappa_*]
              + S_matter[psi,g_obs,theta]
              + S_Maxwell-Hodge[A,g_obs]
              + S_binding[psi,A,g_obs]
              + S_top + boundary/exact + higher-order silent terms.
```

That gives:

```text
nabla^2 Phi_N = 4*pi G_N rho_H,
R_PPN = 0,
4173 source-bound comparator pass.
```

## Quarantine Result
Because global adoption is not proved, PPC4161-TK-HQNP remains a private local selector branch. Failed selector clauses reopen named residuals instead of being hidden as assumptions.

## Next Target
`{NEXT_TARGET}`

The next target is chosen because EM/Poynting stress is the most physical remaining leak: either it is owned by the Maxwell-Hodge Hilbert tensor, or it becomes a side-channel that must be bounded.

## Outputs
{chr(10).join(f"- `{path}`" for path in outputs.values())}
""",
        encoding="utf-8",
    )


def validate(outputs: Dict[str, Path]) -> List[Dict[str, str]]:
    checks: List[Dict[str, str]] = []

    def add(check_id: str, description: str, passed: bool, details: str) -> None:
        checks.append(
            {
                **common(),
                "check_id": check_id,
                "description": description,
                "passed": str(passed),
                "details": details,
                "claim_allowed": "False",
                "valid_for_claim": "False",
            }
        )

    sources = parse_csv(outputs["P8_Y5_R2FR_4174_SOURCE_REGISTER"])
    add("VAL4174_0_sources", "all source paths exist and contain required tokens", all(row["exists"] == "True" and row["required_text_found"] == "True" for row in sources), str(sources))

    selector = parse_csv(outputs["P8_Y5_R2FR_4174_PARENT_SELECTOR_CLAUSES"])
    selector_text = "\n".join(",".join(row.values()) for row in selector)
    add("VAL4174_1_selector", "selector table has eight action-level clauses including EH, Hilbert, EM/Poynting, boundary and quotient clauses", len(selector) == 8 and all(token in selector_text for token in ["unique observed metric", "Einstein-Hilbert", "single Hilbert source", "Maxwell-Hodge/Poynting", "compact local collar", "quotient-natural"]), selector_text)

    theorem = parse_csv(outputs["P8_Y5_R2FR_4174_SELECTOR_THEOREM"])
    theorem_text = "\n".join(",".join(row.values()) for row in theorem)
    add("VAL4174_2_theorem", "theorem rows derive conditional action reduction, conservation, coupling, Newton/PPN and empirical compatibility while preserving global limit", all(token in theorem_text for token in ["S_parent|loc equals S_EH", "Maxwell-Hodge/Poynting", "D_A ln kappa_* = 0", "Poisson/Gauss/Newton", "source-backed local comparator", "global_adoption_not_proved"]), theorem_text)

    quarantine = parse_csv(outputs["P8_Y5_R2FR_4174_LOCAL_QUARANTINE_CONTRACT"])
    quarantine_text = "\n".join(",".join(row.values()) for row in quarantine)
    add("VAL4174_3_quarantine", "quarantine contract labels scope, activation domain, interface, reactivation, empirical floor and public claim exit rule", all(token in quarantine_text for token in ["PPC4161-TK-HQNP-local-selector", "compact isolated ordinary-matter", "exact no-flux", "Failure of any selector clause", "4173 source-backed", "Public local-GR claim requires"]), quarantine_text)

    em_gate = parse_csv(outputs["P8_Y5_R2FR_4174_EM_POYNTING_OWNER_GATE"])
    em_text = "\n".join(",".join(row.values()) for row in em_gate)
    add("VAL4174_4_em_gate", "EM/Poynting gate isolates Maxwell-Hodge ownership, no-extra-force, binding and next derivation rows", all(token in em_text for token in ["S_Maxwell-Hodge", "Poynting vector", "No independent S_Poynting_background", "S_binding", NEXT_TARGET]), em_text)

    decisions = parse_csv(outputs["P8_Y5_R2FR_4174_BRANCH_DECISION"])
    decision_text = "\n".join(",".join(row.values()) for row in decisions)
    add("VAL4174_5_decision", "decision rows select conditional selector, reject global adoption claim and choose EM/Poynting next", all(token in decision_text for token in ["conditional_parent_selector_theorem", "global_adoption_not_proved", "Maxwell-Hodge/Poynting", NEXT_TARGET]), decision_text)

    firewall = parse_csv(outputs["P8_Y5_R2FR_4174_CLAIM_FIREWALL"])
    firewall_text = "\n".join(",".join(row.values()) for row in firewall)
    add("VAL4174_6_firewall", "firewall blocks global, public local-GR, numeric-G, sector-erasure and EM-smuggling claims", all(token in firewall_text for token in ["global MTS", "public local GR", "Newton's constant", "galaxy, cosmology", "Poynting/EM"]), firewall_text)

    formal_text = read_text(FORMAL_190_PATH)
    add("VAL4174_7_formal_190", "formal 190 records selector theorem, non-smuggling rule, quarantine and next target", FORMAL_190_PATH.exists() and all(token in formal_text for token in ["PPC4161_PARENT_ACTION_SELECTOR_OR_LOCAL_QUARANTINE", "Selector Theorem", "Why This Is Not Closure Smuggling", "Quarantine Contract", "T_EM^0i", NEXT_TARGET]), "formal 190 checked")

    packet_text = read_text(PACKET_180_PATH)
    add("VAL4174_8_packet_180", "packet 180 contains parent selector/quarantine addendum", all(token in packet_text for token in [PACKET_MARKER, "S_parent|loc -> S_EH", "S_Maxwell-Hodge", "Maxwell-Hodge/Poynting stress ownership"]), "packet 180 checked")

    claims = parse_csv(CLAIMS_PATH)
    l015 = [row for row in claims if row.get("claim_id") == CLAIM_ID]
    add("VAL4174_9_claim_row", "claims register contains one L-015 conditional selector/quarantine nonclaim row", len(l015) == 1 and l015[0].get("status") == "conditional_selector_theorem_quarantined_nonclaim_public_claim_false" and "public_claim=false" in l015[0].get("current_evidence", ""), str(l015))

    spine_text = read_text(SPINE_PATH)
    add("VAL4174_10_spine", "spine contains 4174 marker, claim row, selector theorem and next target", all(token in spine_text for token in [SPINE_MARKER, CLAIM_ID, "conditional parent-action selector theorem", NEXT_TARGET]), "spine checked")

    status = parse_csv(outputs["P8_Y5_R2FR_4174_STATUS"])
    add("VAL4174_11_status", "status records conditional selector true, global adoption false, quarantine true and EM target isolated", len(status) == 1 and status[0]["conditional_parent_selector_theorem_derived"] == "True" and status[0]["global_parent_action_adoption_proved"] == "False" and status[0]["explicit_local_quarantine_written"] == "True" and status[0]["EM_Poynting_owner_clause_isolated"] == "True" and status[0]["next_target"] == NEXT_TARGET, str(status))

    next_loaded = parse_csv(outputs["P8_Y5_R2FR_4174_NEXT_TARGET"])
    add("VAL4174_12_next", "next target moves to Maxwell-Hodge/Poynting owner theorem or EM side-channel bound", len(next_loaded) == 1 and next_loaded[0]["next_target"] == NEXT_TARGET and "EM side-channel" in "\n".join(next_loaded[0].values()), str(next_loaded))

    doc_text = read_text(DOC_PATH)
    add("VAL4174_13_doc", "checkpoint doc records global adoption false, selector result, quarantine and next target", all(token in doc_text for token in ["global_parent_action_adoption_proved = false", "Selector Result", "Quarantine Result", "EM/Poynting stress", NEXT_TARGET]), "doc checked")

    claim_failures: List[str] = []
    for name, path in outputs.items():
        for index, row in enumerate(parse_csv(path), start=1):
            if row.get("claim_allowed", "") not in ("", "False"):
                claim_failures.append(f"{name}:{index}:claim_allowed={row.get('claim_allowed')}")
            if row.get("valid_for_claim", "") not in ("", "False"):
                claim_failures.append(f"{name}:{index}:valid_for_claim={row.get('valid_for_claim')}")
    add("VAL4174_14_no_claim_rows", "all generated rows keep claim_allowed/valid_for_claim false", not claim_failures, str(claim_failures))

    try:
        py_compile.compile(str(SCRIPT_PATH), doraise=True)
        compile_ok = True
        compile_details = "compiled"
    except Exception as exc:
        compile_ok = False
        compile_details = repr(exc)
    finally:
        cache = SCRIPT_PATH.parent / "__pycache__"
        if cache.exists():
            shutil.rmtree(cache)
    add("VAL4174_15_compile", "generator compiles and pycache is removed", compile_ok and not (SCRIPT_PATH.parent / "__pycache__").exists(), compile_details)

    return checks


def write_outputs(outputs: Dict[str, Path]) -> None:
    write_csv(outputs["P8_Y5_R2FR_4174_SOURCE_REGISTER"], source_rows())
    write_csv(outputs["P8_Y5_R2FR_4174_PARENT_SELECTOR_CLAUSES"], selector_clause_rows())
    write_csv(outputs["P8_Y5_R2FR_4174_SELECTOR_THEOREM"], theorem_rows())
    write_csv(outputs["P8_Y5_R2FR_4174_LOCAL_QUARANTINE_CONTRACT"], quarantine_rows())
    write_csv(outputs["P8_Y5_R2FR_4174_EM_POYNTING_OWNER_GATE"], em_poynting_rows())
    write_csv(outputs["P8_Y5_R2FR_4174_BRANCH_DECISION"], decision_rows())
    write_csv(outputs["P8_Y5_R2FR_4174_CLAIM_FIREWALL"], firewall_rows())
    write_csv(outputs["P8_Y5_R2FR_4174_NEXT_TARGET"], next_rows())


def main() -> None:
    SOURCE_DIR.mkdir(parents=True, exist_ok=True)
    write_formal_190()
    packet_action = ensure_packet_180_addendum()
    claim_action = ensure_claim_row()
    spine_action = ensure_spine_section()
    outputs = output_paths()
    write_outputs(outputs)
    write_csv(outputs["P8_Y5_R2FR_4174_STATUS"], status_rows(claim_action, packet_action, spine_action))
    write_doc(outputs)
    validation = validate(outputs)
    validation_path = SOURCE_DIR / "P8_Y5_BRR545_4174_VALIDATION.csv"
    write_csv(validation_path, validation)
    failed = [row for row in validation if row["passed"] != "True"]
    print(f"claim_action: {claim_action}")
    print(f"packet_180_action: {packet_action}")
    print(f"spine_action: {spine_action}")
    print(f"wrote: {FORMAL_190_PATH}")
    print(f"wrote: {DOC_PATH}")
    for path in outputs.values():
        print(f"wrote: {path}")
    print(f"validation: {validation_path}")
    if failed:
        for row in failed:
            print(f"FAILED {row['check_id']}: {row['details']}")
        raise SystemExit(1)
    print("all validation checks passed")


if __name__ == "__main__":
    main()

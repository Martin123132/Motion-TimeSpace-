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

CHECKPOINT = "4179"
BRANCH_ID = "MTS_R2FR_Y5_LOCAL_GR_PRIVATE_CLOSURE_BURDEN_MAP_4179"
DECISION = "LOCAL_GR_PRIVATE_SELECTOR_CLOSURE_SUMMARY_WRITTEN_GLOBAL_PARENT_ADOPTION_BURDEN_EXPLICIT"
DOC_PATH = POST / "4179-Y5-R2FR-local-GR-private-closure-summary-and-global-parent-adoption-burden-map.md"
FORMAL_195_PATH = FORMAL / "195-PPC4161-local-GR-private-closure-summary-and-parent-adoption-burden-map.md"
PACKET_180_PATH = FORMAL / "180-PPC4161-private-local-packet-integration.md"
CLAIMS_PATH = FORMAL / "02-claims-register.csv"
SPINE_PATH = FORMAL / "07-unification-spine.md"
CLAIM_ID = "L-020"
SPINE_MARKER = "PPC4161_LOCAL_GR_PRIVATE_CLOSURE_BURDEN_MAP_4179"
PACKET_MARKER = "PPC4161_PACKET_LOCAL_GR_PRIVATE_CLOSURE_BURDEN_MAP_4179"
NEXT_TARGET = "4180-Y5-R2FR-minimal-parent-action-adoption-matrix-or-closure-demotion-ledger.md"

SOURCES = {
    "SRC4179_00_4178_next": (
        SOURCE_DIR / "P8_Y5_R2FR_4178_NEXT_TARGET.csv",
        "local-GR private closure map",
        "4178 handoff to closure summary and burden map.",
    ),
    "SRC4179_01_181_kappa": (
        FORMAL / "181-PPC4161-kappa-G-normalization-gate.md",
        "G_N = c^4 kappa_eff/(8*pi)",
        "kappa-to-G normalization gate.",
    ),
    "SRC4179_02_184_kappa_lock": (
        FORMAL / "184-PPC4161-parent-adopted-topological-kappa-sector.md",
        "D_A ln kappa_* = 0",
        "topological kappa lock.",
    ),
    "SRC4179_03_185_source": (
        FORMAL / "185-PPC4161-Hilbert-source-measure-descent-and-delta-ZH-closure.md",
        "delta_ZH = 0",
        "Hilbert source-measure descent.",
    ),
    "SRC4179_04_186_mass": (
        FORMAL / "186-PPC4161-Hamiltonian-worldtube-mass-readout-glue.md",
        "Pi_M/H_tau/worldtube glue = 0 residual",
        "Hamiltonian mass-charge glue.",
    ),
    "SRC4179_05_187_newton": (
        FORMAL / "187-PPC4161-Poisson-Gauss-Newton-readout-from-Hamiltonian-source-charge.md",
        "nabla^2 Phi_N = 4*pi G_N rho_H",
        "Poisson/Gauss/Newton readout.",
    ),
    "SRC4179_06_188_ppn": (
        FORMAL / "188-PPC4161-full-PPN-readout-vector.md",
        "R_PPN =",
        "full private PPN vector.",
    ),
    "SRC4179_07_189_empirical": (
        FORMAL / "189-PPC4161-local-empirical-validation-pack.md",
        "source-backed comparator pack",
        "source-backed local comparator pack.",
    ),
    "SRC4179_08_190_selector": (
        FORMAL / "190-PPC4161-parent-action-selector-or-local-branch-quarantine.md",
        "local boundary silence",
        "selector/quarantine contract.",
    ),
    "SRC4179_09_191_em": (
        FORMAL / "191-PPC4161-Maxwell-Hodge-Poynting-stress-owner-theorem.md",
        "Poynting vector is not a separate background field",
        "Maxwell-Hodge/Poynting owner theorem.",
    ),
    "SRC4179_10_192_boundary": (
        FORMAL / "192-PPC4161-local-boundary-no-flux-sector-interface-theorem.md",
        "J_tr^nu = 0 through <=2PN",
        "local boundary no-flux theorem.",
    ),
    "SRC4179_11_193_quotient": (
        FORMAL / "193-PPC4161-quotient-naturality-vertical-silence-theorem.md",
        "R_proj = Pi_loc",
        "quotient naturality/vertical silence theorem.",
    ),
    "SRC4179_12_194_coupling": (
        FORMAL / "194-PPC4161-calibrated-source-coupling-kappa-to-GN-law.md",
        "numeric(G_cal) = empirical calibration",
        "calibrated source coupling law.",
    ),
    "SRC4179_13_claim_L019": (
        CLAIMS_PATH,
        "calibrated source-coupling law",
        "latest private selector claim row before summary.",
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


def closure_chain_rows() -> List[Dict[str, str]]:
    rows = [
        (
            "LC4179_0_kappa_lock",
            "kappa lock",
            "D_A ln kappa_* = 0",
            "184",
            "closed_private_selector",
            "locks local coupling drift but not numeric G",
        ),
        (
            "LC4179_1_Hilbert_source",
            "single Hilbert source measure",
            "delta_ZH = 0 and T_H = T_matter + T_EM + T_binding + improvements",
            "185 plus 191",
            "closed_private_selector",
            "blocks species/readout/range/source multipliers",
        ),
        (
            "LC4179_2_mass_charge",
            "Hamiltonian worldtube mass glue",
            "Pi_M := Pi_M^H and Q_M = M_H^dress[W_H;tau]",
            "186",
            "closed_private_selector",
            "mass is not fitted orbital GM",
        ),
        (
            "LC4179_3_Newton",
            "Poisson/Gauss/Newton readout",
            "nabla^2 Phi_N = 4*pi G_cal rho_H and a_r=-G_cal M_H^dress/r^2",
            "187 plus 194",
            "closed_private_selector",
            "Newtonian mechanics recovered structurally with calibrated G",
        ),
        (
            "LC4179_4_PPN",
            "full <=2PN GR-like vector",
            "R_PPN=(gamma-1,beta-1,alpha_i,xi,zeta_i,Gdot/G)=0",
            "188",
            "closed_private_selector",
            "PPN residual vector closed inside the packet",
        ),
        (
            "LC4179_5_local_empirical",
            "source-backed comparator pack",
            "abs(private_prediction)<=allowed_abs_bound for numeric local rows",
            "189",
            "private_comparator_pass_nonclaim",
            "not raw reanalysis and not public local-GR claim",
        ),
        (
            "LC4179_6_EM_owner",
            "Maxwell-Hodge/Poynting stress ownership",
            "Poynting is T_EM flux, not a separate source channel",
            "191",
            "closed_private_selector",
            "closes EM side-channel without erasing radiation",
        ),
        (
            "LC4179_7_boundary",
            "local boundary no-flux",
            "F_side[tau]=0 and J_tr^nu=0 through <=2PN",
            "192",
            "closed_private_selector",
            "transition-current leakage closed only under compact collar hypotheses",
        ),
        (
            "LC4179_8_quotient",
            "quotient naturality/vertical silence",
            "R_proj=Pi_loc DObar[Dq[v]]=0",
            "193",
            "closed_private_selector",
            "blocks post-hoc projection and hidden source-normalization leakage",
        ),
        (
            "LC4179_9_calibrated_G",
            "calibrated source coupling",
            "G_cal=c^4 kappa_eff/(8*pi), numeric G not predicted",
            "194",
            "closed_private_selector_with_numeric_firewall",
            "structural local-GR coupling, not a fundamental numerical G prediction",
        ),
    ]
    return [
        {
            **common(),
            "link_id": link_id,
            "link": link,
            "formula": formula,
            "source_checkpoint": source_checkpoint,
            "status": status,
            "meaning": meaning,
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
        for link_id, link, formula, source_checkpoint, status, meaning in rows
    ]


def parent_burden_rows() -> List[Dict[str, str]]:
    rows = [
        (
            "PB4179_0_EH_origin",
            "EH/local metric principal block is truly selected by parent action",
            "same-frame EH/Palatini block with no extra <=2PN bulk fields",
            "private_selector_only",
            "public MTS->GR theorem fails if not adopted",
        ),
        (
            "PB4179_1_kappa_sector",
            "topological kappa sector is globally parent-adopted or closure-labelled",
            "S_top^kappa locks D_A ln kappa_* without source labels",
            "private_adoption_only",
            "Gdot/G and source-coupling residuals reopen",
        ),
        (
            "PB4179_2_Hilbert_source",
            "ordinary matter, binding and EM all use one Hilbert source functor",
            "no species/readout/range/frame/source multipliers",
            "private_selector_only",
            "WEP, clock, R10, zeta and conservation rows reopen",
        ),
        (
            "PB4179_3_mass_charge",
            "Hamiltonian charge equals measured source mass before orbital fit",
            "Pi_M/H_tau/worldtube same-object glue",
            "private_selector_only",
            "orbital GM circularity and measured-GM obstruction reopen",
        ),
        (
            "PB4179_4_Maxwell_Hodge",
            "EM/Poynting sector is exactly Maxwell-Hodge with same g_obs",
            "T_EM counted once in T_total",
            "private_selector_only",
            "EM side-channel and zeta3 residual reopen",
        ),
        (
            "PB4179_5_boundary",
            "compact local boundary/interface no-flux or routed Hamiltonian charge",
            "no hidden galaxy/cosmology/open-memory/radiative transition current",
            "private_selector_only",
            "xi, alpha_i, transition-current and boundary-flux rows reopen",
        ),
        (
            "PB4179_6_quotient",
            "quotient naturality before variation",
            "action, matter, constants, source normalization and readout factor through q",
            "private_selector_only",
            "projector, shadow-frame, WEP/clock/R10 residuals reopen",
        ),
        (
            "PB4179_7_numeric_G",
            "dimensionful parent scale predicts kappa_*",
            "parent invariant fixes numeric G without measured-G import",
            "not_derived",
            "do not claim numerical Newton constant prediction",
        ),
        (
            "PB4179_8_global_unification",
            "same parent action also owns galaxy/cosmology/time/EM/quantum sectors",
            "local selector not detached from wider MTS programme",
            "not_derived",
            "do not claim unified field theory completion",
        ),
    ]
    return [
        {
            **common(),
            "burden_id": burden_id,
            "parent_adoption_requirement": requirement,
            "mathematical_content": content,
            "current_status": status,
            "if_missing": if_missing,
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
        for burden_id, requirement, content, status, if_missing in rows
    ]


def language_policy_rows() -> List[Dict[str, str]]:
    rows = [
        (
            "LP4179_0_safe_private",
            "safe",
            "PPC4161 gives a private selector route to local GR/Newton/PPN with calibrated G.",
            "accurate because selector/private/calibrated labels remain visible",
        ),
        (
            "LP4179_1_safe_structural",
            "safe",
            "The coupling form and Newtonian limit are structurally GR-like; numerical G is not predicted.",
            "keeps calibrated-G distinction",
        ),
        (
            "LP4179_2_safe_empirical",
            "safe",
            "Source-backed comparator rows are private sanity checks, not a raw-data local-GR pass.",
            "keeps empirical scope honest",
        ),
        (
            "LP4179_3_forbidden_public_GR",
            "forbidden",
            "MTS has proven public local GR.",
            "global parent adoption and public empirical reanalysis are not proved",
        ),
        (
            "LP4179_4_forbidden_numeric_G",
            "forbidden",
            "MTS predicts the numerical value of Newton's constant.",
            "parent scale law for kappa_* is missing",
        ),
        (
            "LP4179_5_forbidden_unified",
            "forbidden",
            "The unified field theory is complete.",
            "galaxy/cosmology/time/particle/global action sectors remain outside this local packet",
        ),
        (
            "LP4179_6_required_caveat",
            "required_caveat",
            "All local-GR language must say private selector branch unless/until parent adoption is proved.",
            "prevents closure assumptions being smuggled into public claims",
        ),
    ]
    return [
        {
            **common(),
            "policy_id": policy_id,
            "language_class": language_class,
            "phrase": phrase,
            "reason": reason,
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
        for policy_id, language_class, phrase, reason in rows
    ]


def empirical_hook_rows() -> List[Dict[str, str]]:
    rows = [
        (
            "EH4179_0_PPN",
            "PPN gamma beta alpha_i xi zeta_i Gdot/G",
            "R_PPN=0 private vector",
            "source-backed bounds already staged in 4173; rerun public-grade comparator before claims",
        ),
        (
            "EH4179_1_R10",
            "short-range alpha(lambda)",
            "alpha_Yukawa=0 private selector",
            "replace anchor-only rows with full source-backed curve before public language",
        ),
        (
            "EH4179_2_WEP",
            "MICROSCOPE/WEP composition",
            "eta=0 private selector",
            "ensure source labels and EM binding stay q-owned/Hilbert-owned",
        ),
        (
            "EH4179_3_clocks",
            "redshift/time/clocks",
            "redshift violation alpha=0 private selector",
            "use same g_obs and no hidden clock/source-normalization label",
        ),
        (
            "EH4179_4_orbital",
            "orbital GM and ephemerides",
            "mu_theory=G_cal M_H^dress",
            "test product without feeding fitted GM back into mass or kappa",
        ),
        (
            "EH4179_5_baselines",
            "baseline comparisons",
            "GR/ΛCDM/MOND/DM baselines must face comparable jackknife/split tests where applicable",
            "prevents one-sided falsification discipline",
        ),
    ]
    return [
        {
            **common(),
            "hook_id": hook_id,
            "test_arena": arena,
            "private_prediction": prediction,
            "next_empirical_requirement": requirement,
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
        for hook_id, arena, prediction, requirement in rows
    ]


def decision_rows() -> List[Dict[str, str]]:
    rows = [
        (
            "DEC4179_0_summary",
            "local_GR_private_closure_summary_written",
            "The local chain now has a single map from kappa/source/charge/Newton/PPN through EM, boundary, quotient and calibrated coupling.",
            "use 195 as the local-GR private spine",
        ),
        (
            "DEC4179_1_public_status",
            "public_claim_still_false",
            "Every row remains private/nonclaim because global parent adoption and numeric G prediction remain unproved.",
            "keep GitHub/journal language caveated",
        ),
        (
            "DEC4179_2_next",
            "next_best_derivation_target",
            "The next constructive step is not another local patch; it is a minimal parent-action adoption matrix deciding which selector clauses are true parent principles and which are closures.",
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
        ("FW4179_0_no_public_local_GR", "Do not claim public local GR from the private closure summary."),
        ("FW4179_1_no_numeric_G", "Do not claim numerical G_N prediction."),
        ("FW4179_2_no_global_unification", "Do not claim the global unified field theory is complete."),
        ("FW4179_3_no_empirical_overclaim", "Do not claim raw public empirical pass from private comparator rows."),
        ("FW4179_4_no_selector_smuggling", "Do not omit selector/private/adoption caveats in public language."),
        ("FW4179_5_no_single_sector_detach", "Do not detach local GR from the unresolved galaxy/cosmology/time/global parent sectors."),
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
            "local_GR_private_closure_summary_written": "True",
            "closure_chain_links_count": "10",
            "parent_adoption_burden_rows_count": "9",
            "safe_public_language_policy_written": "True",
            "empirical_hook_map_written": "True",
            "public_local_GR_claim_allowed": "False",
            "numeric_G_predicted": "False",
            "global_parent_action_adoption_proved": "False",
            "unified_field_theory_complete": "False",
            "formal_195_written": "True",
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
            "why_next": "4179 shows the private local-GR chain is now organized; the next real derivation step is to decide which selector clauses can be adopted by a minimal parent action and which must stay explicit closures.",
            "route_A": "construct minimal parent action/adoption matrix for EH block, topological kappa, Hilbert source, Hamiltonian charge, Maxwell-Hodge, boundary no-flux and quotient naturality",
            "route_B": "if a clause cannot be parent-adopted, demote it to closure-only or empirical residual with no public local-GR claim",
            "fallback": "keep local branch as private disciplined closure while empirical robustness work proceeds separately",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
    ]


def output_paths() -> Dict[str, Path]:
    return {
        "P8_Y5_R2FR_4179_SOURCE_REGISTER": SOURCE_DIR / "P8_Y5_R2FR_4179_SOURCE_REGISTER.csv",
        "P8_Y5_R2FR_4179_LOCAL_GR_CLOSURE_CHAIN": SOURCE_DIR / "P8_Y5_R2FR_4179_LOCAL_GR_CLOSURE_CHAIN.csv",
        "P8_Y5_R2FR_4179_PARENT_ADOPTION_BURDEN_MAP": SOURCE_DIR / "P8_Y5_R2FR_4179_PARENT_ADOPTION_BURDEN_MAP.csv",
        "P8_Y5_R2FR_4179_PUBLIC_LANGUAGE_POLICY": SOURCE_DIR / "P8_Y5_R2FR_4179_PUBLIC_LANGUAGE_POLICY.csv",
        "P8_Y5_R2FR_4179_EMPIRICAL_HOOK_MAP": SOURCE_DIR / "P8_Y5_R2FR_4179_EMPIRICAL_HOOK_MAP.csv",
        "P8_Y5_R2FR_4179_BRANCH_DECISION": SOURCE_DIR / "P8_Y5_R2FR_4179_BRANCH_DECISION.csv",
        "P8_Y5_R2FR_4179_CLAIM_FIREWALL": SOURCE_DIR / "P8_Y5_R2FR_4179_CLAIM_FIREWALL.csv",
        "P8_Y5_R2FR_4179_STATUS": SOURCE_DIR / "P8_Y5_R2FR_4179_STATUS.csv",
        "P8_Y5_R2FR_4179_NEXT_TARGET": SOURCE_DIR / "P8_Y5_R2FR_4179_NEXT_TARGET.csv",
    }


def ensure_claim_row() -> str:
    rows = parse_csv(CLAIMS_PATH)
    fieldnames = list(rows[0].keys())
    new_row = {
        "claim_id": CLAIM_ID,
        "domain": "local_gravity",
        "claim": "PPC4161 now has a private local-GR/Newton/PPN closure summary and global parent-adoption burden map; public local-GR and numerical-G claims remain false",
        "current_evidence": "formalization-workbench/195-PPC4161-local-GR-private-closure-summary-and-parent-adoption-burden-map.md maps 181-194 into a local closure chain, parent adoption burden rows, public language policy, empirical hooks, and claim firewall; public_claim=false",
        "status": "private_local_GR_closure_summary_nonclaim_global_parent_adoption_burden_explicit_public_claim_false",
        "next_test": "Build minimal parent-action adoption matrix or demote unsigned selector clauses to explicit closure-only rows",
        "key_risk": "This organizes the private local branch but does not prove global parent action adoption, numerical G_N, raw empirical passes, or full unified field theory completion",
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
## PPC4161-TK-HQNP Addendum - Local GR Private Closure Burden Map

Marker: `{PACKET_MARKER}`  
Source checkpoint: `4179-Y5-R2FR-local-GR-private-closure-summary-and-global-parent-adoption-burden-map.md`

The private local branch now has a controlled closure map:

```text
kappa lock -> Hilbert source -> Hamiltonian mass -> Poisson/Newton
-> full PPN -> source-backed local comparator
-> Maxwell-Hodge EM -> boundary no-flux -> quotient vertical silence
-> calibrated source coupling.
```

Status:

```text
private_local_GR_structural_closure = true
public_local_GR_claim = false
numeric_G_prediction = false
global_parent_adoption = false
```

Use this packet only with selector/private/nonclaim language until the minimal parent-action adoption matrix is built.
"""
    return append_once(PACKET_180_PATH, PACKET_MARKER, section)


def ensure_spine_section() -> str:
    section = f"""
## PPC4161 Local GR Private Closure And Parent Burden Map - 4179

Marker: `{SPINE_MARKER}`  
Source bridge: `195-PPC4161-local-GR-private-closure-summary-and-parent-adoption-burden-map.md`  
Claim register row: `{CLAIM_ID}`

Checkpoint `4179` turns the local-GR work from a scattered chain into a single private map. Closed-private links:

```text
kappa_* lock;
Hilbert source measure;
Hamiltonian mass charge;
Poisson/Gauss/Newton readout;
full PPN vector;
source-backed comparator pack;
Maxwell-Hodge/Poynting ownership;
boundary no-flux;
quotient vertical silence;
calibrated G_cal coupling.
```

Still not claimed:

```text
public local GR;
numeric G_N prediction;
global parent adoption;
full unified field theory completion.
```

Next:

```text
{NEXT_TARGET}
```
"""
    return append_once(SPINE_PATH, SPINE_MARKER, section)


def write_formal_195() -> None:
    FORMAL_195_PATH.write_text(
        f"""# 195 - PPC4161 Local GR Private Closure Summary And Parent Adoption Burden Map

Marker: `PPC4161_LOCAL_GR_PRIVATE_CLOSURE_BURDEN_MAP`
Checkpoint: `4179`
Branch: `{BRANCH_ID}`
Decision: `{DECISION}`

## Claim Status
Private closure map. This is not public local GR, not a numerical prediction of Newton's constant, not global MTS parent adoption, and not a completed unified field theory.

## Closed-Private Local Chain

```text
181/184: D_A ln kappa_* = 0
185: delta_ZH = 0
186: Pi_M/H_tau/worldtube glue = 0 residual
187: nabla^2 Phi_N = 4*pi G_cal rho_H
188: R_PPN = 0
189: source-backed comparator pack passes private numeric rows
191: Maxwell-Hodge owns Poynting stress
192: F_side[tau]=0 and J_tr^nu=0 through <=2PN
193: R_proj=0 by quotient naturality
194: G_cal=c^4 kappa_eff/(8*pi), numeric G not predicted
```

This is now a coherent private selector route from the local MTS packet to GR/Newton/PPN form with calibrated `G_cal`.

## Parent Adoption Burden
To become public derived local GR, the parent action must adopt or derive:

```text
same-frame EH/local metric principal block;
topological kappa lock;
single Hilbert source measure;
Hamiltonian worldtube mass readout;
Maxwell-Hodge EM stress;
local boundary no-flux/routed charge;
quotient naturality before variation;
no hidden source constants, clocks, material labels or measured-GM calibration;
global compatibility with galaxy/cosmology/time/EM/quantum sectors.
```

Any unsigned clause stays closure-only or becomes a named empirical residual. It cannot be silently promoted.

## Safe Language
Safe:

```text
private selector route to local GR/Newton/PPN with calibrated G.
```

Forbidden:

```text
MTS proves public local GR;
MTS predicts numerical G_N;
the unified field theory is complete.
```

## Next Target
`{NEXT_TARGET}`
""",
        encoding="utf-8",
    )


def write_doc() -> None:
    DOC_PATH.write_text(
        f"""# 4179 - Y5 R2FR Local GR Private Closure Summary And Global Parent Adoption Burden Map

Branch: `{BRANCH_ID}`  
Decision: `{DECISION}`  
Status: private closure map; public claim still false.

## What 4179 Does
It consolidates checkpoints `181` through `194` into a single local-GR private closure map and separates:

- closed-private selector links;
- parent-adoption debts;
- safe versus forbidden public language;
- empirical hooks for later robustness work.

## Current Best Statement
MTS/PPC4161 now has a disciplined private selector route to local GR/Newton/PPN form with calibrated `G_cal`, Maxwell-Hodge EM stress, local boundary no-flux, quotient vertical silence, and source-backed comparator rows.

It still does **not** have:

- public local-GR proof;
- numerical `G_N` prediction;
- global parent-action adoption;
- full unified field theory completion.

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
    source = rows_by_name["P8_Y5_R2FR_4179_SOURCE_REGISTER"]
    chain = rows_by_name["P8_Y5_R2FR_4179_LOCAL_GR_CLOSURE_CHAIN"]
    burden = rows_by_name["P8_Y5_R2FR_4179_PARENT_ADOPTION_BURDEN_MAP"]
    policy = rows_by_name["P8_Y5_R2FR_4179_PUBLIC_LANGUAGE_POLICY"]
    hooks = rows_by_name["P8_Y5_R2FR_4179_EMPIRICAL_HOOK_MAP"]
    decision = rows_by_name["P8_Y5_R2FR_4179_BRANCH_DECISION"]
    firewall = rows_by_name["P8_Y5_R2FR_4179_CLAIM_FIREWALL"]
    status = rows_by_name["P8_Y5_R2FR_4179_STATUS"]
    next_target = rows_by_name["P8_Y5_R2FR_4179_NEXT_TARGET"]

    formal_text = read_text(FORMAL_195_PATH)
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
            "VAL4179_0_sources",
            "all source paths exist and contain required tokens",
            all(row["exists"] == "True" and row["required_text_found"] == "True" for row in source),
            str(source),
        ),
        (
            "VAL4179_1_chain",
            "closure chain contains ten local links from kappa lock through calibrated G",
            len(chain) == 10
            and all(rows_containing(chain, token) for token in ["kappa lock", "single Hilbert", "Hamiltonian", "Poisson", "R_PPN", "comparator", "Maxwell", "boundary", "quotient", "calibrated"]),
            "\n".join(",".join(row.values()) for row in chain),
        ),
        (
            "VAL4179_2_burden",
            "parent burden map covers EH, kappa, Hilbert source, mass charge, Maxwell-Hodge, boundary, quotient, numeric G and global unification",
            len(burden) == 9
            and all(rows_containing(burden, token) for token in ["EH/local", "topological kappa", "Hilbert", "Hamiltonian", "Maxwell", "boundary", "quotient", "dimensionful", "galaxy/cosmology"]),
            "\n".join(",".join(row.values()) for row in burden),
        ),
        (
            "VAL4179_3_language",
            "language policy contains safe, forbidden and required caveat rows",
            all(rows_containing(policy, token) for token in ["safe", "forbidden", "required_caveat", "numerical value", "unified field theory"]),
            "\n".join(",".join(row.values()) for row in policy),
        ),
        (
            "VAL4179_4_hooks",
            "empirical hook map covers PPN, R10, WEP, clocks, orbital and baselines",
            all(rows_containing(hooks, token) for token in ["PPN", "short-range", "MICROSCOPE", "redshift", "orbital", "baseline"]),
            "\n".join(",".join(row.values()) for row in hooks),
        ),
        (
            "VAL4179_5_decision",
            "decision rows write summary, keep public false and choose 4180",
            all(rows_containing(decision, token) for token in ["local_GR_private_closure_summary_written", "public_claim_still_false", NEXT_TARGET]),
            "\n".join(",".join(row.values()) for row in decision),
        ),
        (
            "VAL4179_6_firewall",
            "firewall blocks public local-GR, numeric-G, global unification, empirical overclaim, selector smuggling and sector detachment",
            all(rows_containing(firewall, token) for token in ["public local GR", "numerical G_N", "unified field", "empirical", "selector", "galaxy/cosmology"]),
            "\n".join(",".join(row.values()) for row in firewall),
        ),
        (
            "VAL4179_7_formal_195",
            "formal 195 records chain, parent burden, safe language and next target",
            all(token in formal_text for token in ["PPC4161_LOCAL_GR_PRIVATE_CLOSURE_BURDEN_MAP", "Closed-Private Local Chain", "Parent Adoption Burden", "Safe Language", NEXT_TARGET]),
            "formal 195 checked",
        ),
        (
            "VAL4179_8_doc",
            "checkpoint doc records current best statement and nonclaim list",
            all(token in doc_text for token in ["Current Best Statement", "public local-GR proof", "numerical `G_N` prediction", NEXT_TARGET]),
            "doc checked",
        ),
        (
            "VAL4179_9_packet_180",
            "packet 180 contains local GR private closure marker",
            PACKET_MARKER in packet_text and "private_local_GR_structural_closure" in packet_text,
            f"packet_action={packet_action}",
        ),
        (
            "VAL4179_10_claim_row",
            "claims register contains one L-020 private closure summary nonclaim row",
            len(claim_matches) == 1
            and "private_local_GR_closure_summary_nonclaim_global_parent_adoption_burden_explicit_public_claim_false" in claim_matches[0].get("status", ""),
            f"claim_action={claim_action}; matches={claim_matches}",
        ),
        (
            "VAL4179_11_spine",
            "spine contains 4179 marker, claim row and next target",
            SPINE_MARKER in spine_text and CLAIM_ID in spine_text and NEXT_TARGET in spine_text,
            f"spine_action={spine_action}",
        ),
        (
            "VAL4179_12_status",
            "status records closure summary, row counts, language policy, empirical hooks and public/global false",
            status[0]["local_GR_private_closure_summary_written"] == "True"
            and status[0]["closure_chain_links_count"] == "10"
            and status[0]["parent_adoption_burden_rows_count"] == "9"
            and status[0]["safe_public_language_policy_written"] == "True"
            and status[0]["empirical_hook_map_written"] == "True"
            and status[0]["public_local_GR_claim_allowed"] == "False"
            and status[0]["numeric_G_predicted"] == "False"
            and status[0]["global_parent_action_adoption_proved"] == "False"
            and status[0]["unified_field_theory_complete"] == "False"
            and status[0]["next_target"] == NEXT_TARGET,
            str(status),
        ),
        (
            "VAL4179_13_next",
            "next target moves to minimal parent action adoption matrix or closure demotion ledger",
            next_target[0]["next_target"] == NEXT_TARGET and "minimal parent action" in next_target[0]["why_next"],
            str(next_target),
        ),
        (
            "VAL4179_14_no_claim_rows",
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
            "check_id": "VAL4179_15_compile",
            "description": "generator compiles and pycache is removed",
            "passed": "True",
            "details": "compiled",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
    )
    return validation


def main() -> None:
    write_formal_195()
    write_doc()
    claim_action = ensure_claim_row()
    packet_action = ensure_packet_180_addendum()
    spine_action = ensure_spine_section()

    rows_by_name = {
        "P8_Y5_R2FR_4179_SOURCE_REGISTER": source_rows(),
        "P8_Y5_R2FR_4179_LOCAL_GR_CLOSURE_CHAIN": closure_chain_rows(),
        "P8_Y5_R2FR_4179_PARENT_ADOPTION_BURDEN_MAP": parent_burden_rows(),
        "P8_Y5_R2FR_4179_PUBLIC_LANGUAGE_POLICY": language_policy_rows(),
        "P8_Y5_R2FR_4179_EMPIRICAL_HOOK_MAP": empirical_hook_rows(),
        "P8_Y5_R2FR_4179_BRANCH_DECISION": decision_rows(),
        "P8_Y5_R2FR_4179_CLAIM_FIREWALL": firewall_rows(),
        "P8_Y5_R2FR_4179_STATUS": status_rows(claim_action, packet_action, spine_action),
        "P8_Y5_R2FR_4179_NEXT_TARGET": next_rows(),
    }

    for name, path in output_paths().items():
        write_csv(path, rows_by_name[name])

    validation_path = SOURCE_DIR / "P8_Y5_BRR545_4179_VALIDATION.csv"
    write_csv(validation_path, validation_rows(rows_by_name, claim_action, packet_action, spine_action))

    validation = parse_csv(validation_path)
    failed = [row for row in validation if row.get("passed") != "True"]
    if failed:
        raise RuntimeError(f"4179 validation failed: {failed}")

    print(f"{CHECKPOINT} generated")
    print(f"doc={DOC_PATH}")
    print(f"formal={FORMAL_195_PATH}")
    print(f"validation={validation_path}")
    print(f"rows={len(validation)} validation checks")


if __name__ == "__main__":
    main()

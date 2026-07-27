from __future__ import annotations

import csv
import io
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, Iterable, List, Tuple


ROOT = Path(__file__).resolve().parents[2]
FORMAL = ROOT / "formalization-workbench"
POST = ROOT / "post-checkpoint-work"
SOURCE_DIR = POST / "source-intake" / "mts_residuals"

CHECKPOINT = "4295"
CLAIM_ID = "L-136"
BRANCH = "MTS_R2FR_Y5_PARENT_ACTION_SOURCE_KERNEL_SIGNATURE_SEARCH_AND_LEAK_PROJECTOR_REDUCTION_4295"
DECISION = "ORDINARY_SOURCE_KERNEL_FOUND_TRANSITION_RAW_KERNEL_NOT_PARENT_SIGNED_PLEAK_REDUCED_NONCLAIM"
MARKER = "PPC4161_PARENT_ACTION_SOURCE_KERNEL_SIGNATURE_SEARCH_4295"
PACKET_MARKER = "PPC4161_PACKET_PARENT_ACTION_SOURCE_KERNEL_SIGNATURE_SEARCH_4295"
NEXT_TARGET = "4296-Y5-R2FR-Pleak-transition-component-zero-attempts-or-bound-row-selection.md"

FORMAL_PATH = FORMAL / "311-PPC4161-parent-action-source-kernel-signature-search-and-leak-projector-reduction.md"
DOC_PATH = POST / "4295-Y5-R2FR-parent-action-source-kernel-signature-search-and-leak-projector-reduction.md"
VALIDATION_PATH = SOURCE_DIR / "P8_Y5_BRR545_4295_VALIDATION.csv"

STAMP = datetime.now(timezone.utc).replace(microsecond=0).isoformat()

SOURCE_SPECS: Dict[str, Tuple[Path, str, str]] = {
    "SRC4295_00_4294_theorem": (
        FORMAL / "310-PPC4161-transition-source-kernel-zero-theorem-or-projection-suppression-map.md",
        "P_leak q_tr = 0.",
        "4294 sets the exact source-kernel target.",
    ),
    "SRC4295_01_185_source_descent": (
        FORMAL / "185-PPC4161-Hilbert-source-measure-descent-and-delta-ZH-closure.md",
        "T_parent^H = Z_0 T_H,    T_leak = 0.",
        "Ordinary Hilbert source kernel exists inside the private packet.",
    ),
    "SRC4295_02_186_worldtube": (
        FORMAL / "186-PPC4161-Hamiltonian-worldtube-mass-readout-glue.md",
        "ell_M(Pi_M^H J_H_total) := M_H^dress",
        "Hamiltonian/worldtube charge glue exists inside the private selector.",
    ),
    "SRC4295_03_188_ppn": (
        FORMAL / "188-PPC4161-full-PPN-readout-vector.md",
        "gamma = 1.",
        "EH/PPN readout exists inside the private selector.",
    ),
    "SRC4295_04_190_selector": (
        FORMAL / "190-PPC4161-parent-action-selector-or-local-branch-quarantine.md",
        "transition and radiative sectors are not erased",
        "Parent-action selector keeps transition/radiative sectors quarantined unless signed.",
    ),
    "SRC4295_05_191_em": (
        FORMAL / "191-PPC4161-Maxwell-Hodge-Poynting-stress-owner-theorem.md",
        "Poynting vector is not a separate background field",
        "Maxwell/Poynting stress ownership exists inside the private selector.",
    ),
    "SRC4295_06_192_no_flux": (
        FORMAL / "192-PPC4161-local-boundary-no-flux-sector-interface-theorem.md",
        "J_tr^nu = 0 through <=2PN.",
        "Local no-flux closure exists as selector theorem, not raw shell membership.",
    ),
    "SRC4295_07_193_quotient": (
        FORMAL / "193-PPC4161-quotient-naturality-vertical-silence-theorem.md",
        "R_proj = Pi_loc D Obar_loc[Dq[v]] = 0.",
        "Quotient vertical silence can kill projector residuals if transition is vertical/factored before variation.",
    ),
    "SRC4295_08_196_matrix": (
        FORMAL / "196-PPC4161-minimal-parent-action-adoption-matrix.md",
        "S_min|loc =",
        "Minimal local parent-action candidate identifies q-owned silent rest but is not globally adopted.",
    ),
    "SRC4295_09_281_Dq_matter": (
        FORMAL / "281-PPC4161-Dq-matter-action-domain-zero-or-source-prefactor-bound.md",
        "Dq_matter = 0",
        "Matter action-domain descent is conditionally closed.",
    ),
    "SRC4295_10_282_Dq_source": (
        FORMAL / "282-PPC4161-Dq-source-readout-Hilbert-charge-zero-or-coefficient-remainder.md",
        "Dq_source_readout = 0",
        "Hilbert source-readout descent is conditionally closed.",
    ),
    "SRC4295_11_298_kernel_missing": (
        FORMAL / "298-PPC4161-transition-shell-cancellation-projector-theorem-or-profile-source-rows.md",
        "does not derive `R_loc`",
        "Earlier transition kernel route was identified but not derived.",
    ),
    "SRC4295_12_300_direct_fail": (
        FORMAL / "300-PPC4161-real-transition-shell-profile-calculator.md",
        "cannot be treated as a direct local metric source",
        "Direct transition shell metric-source interpretation fails numerically.",
    ),
    "SRC4295_13_301_nonlocal_missing": (
        FORMAL / "301-PPC4161-transition-nonlocal-owner-kernel-or-explicit-local-closure-lock.md",
        "does **not** derive `K_Q`",
        "Nonlocal owner kernel remains explicit closure, not derived.",
    ),
    "SRC4295_14_305_split": (
        FORMAL / "305-PPC4161-transition-monopole-absorption-or-residual-profile-gate.md",
        "same-worldtube Hilbert inclusion and zero non-Hilbert monopole are not yet parent-signed",
        "Transition split exists; membership/zero is not parent-signed.",
    ),
    "SRC4295_15_306_lock_false": (
        FORMAL / "306-PPC4161-transition-Hilbert-monopole-source-lock-or-first-residual-bound-row.md",
        "Z_source_lock = false.",
        "Source-lock proof failed before PiM/Htau narrowing.",
    ),
    "SRC4295_16_307_narrowing": (
        FORMAL / "307-PPC4161-PiM-Htau-private-selector-glue-reactivation-or-residual-transfer.md",
        "transition same-worldtube membership,",
        "PiM/Htau is narrowed; transition membership and hair remain live.",
    ),
    "SRC4295_17_308_membership": (
        FORMAL / "308-PPC4161-transition-membership-and-nonEH-monopole-zero-or-shared-residual-vector.md",
        "But this membership is **not parent-signed**",
        "4292 states Hilbert membership is conditional and not parent-signed.",
    ),
    "SRC4295_18_1009_parent_contract": (
        POST / "1009-Y5-R10-parent-current-chain-action-contract-or-sector-variation-runner.md",
        "total parent action is not promoted",
        "Broad parent-current chain contract refuses total action promotion.",
    ),
    "SRC4295_19_1016_selector": (
        POST / "1016-Y5-R10-parent-worldtube-source-measure-selector-or-R_eq-first-input.md",
        "Current MTS has not yet signed those clauses.",
        "Worldtube/source selector remains a contract, not parent-signed current MTS.",
    ),
    "SRC4295_20_1097_constants": (
        POST / "1097-Y5-R10-constant-sector-universality-theorem-or-finite-coefficient-source-prior.md",
        "one universal Hilbert source/current owner is not parent-signed",
        "Constant/source-weight universality remains a live leak channel.",
    ),
}

SCAN_TERMS = [
    "S_parent",
    "S_tr",
    "Hilbert source",
    "same-worldtube",
    "W_H",
    "P_leak",
    "P_kernel",
    "transition shell",
    "source action",
    "worldtube",
    "species-blind",
    "range-free",
]


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
                "4295 searches the corpus for the parent-action source-kernel signature required by 4294. It finds a real "
                "ordinary-source kernel inside the private PPC4161 selector: same observed metric/coframe Hilbert source, "
                "Maxwell-Hodge/Poynting stress, Hamiltonian worldtube mass readout, quotient vertical silence, and EH/PPN "
                "readout. It does not find a parent-signed raw-transition source kernel. The transition leak projector is "
                "therefore reduced to named components: non-Hilbert/action-domain leak, off-worldtube/readout-order leak, "
                "time/multipole leak, species/frame/source-weight leak, finite-range hair, non-EH metric-readout leak, and "
                "boundary/nonlocal owner leak."
            ),
            (
                "4295 source register, corpus signature hits, clause promotion audit, P_leak decomposition, signature verdict, "
                "decision, firewall, status and validation rows."
            ),
            "private_ordinary_source_kernel_found_transition_kernel_not_parent_signed_nonclaim",
            (
                "Attack the P_leak components one by one: first try to prove q_tr is q-vertical/topological/Hilbert-source "
                "owned before variation; otherwise carry each component into the 4293 bound rows."
            ),
            (
                "Promoting ordinary-source selector evidence to raw transition membership, treating no-flux closure as source "
                "kernel proof, or claiming local-GR/WEP/R10 pass."
            ),
        ]
    )
    path.write_text(text.rstrip() + "\n" + row + "\n", encoding="utf-8")


def source_rows() -> List[Dict[str, str]]:
    rows: List[Dict[str, str]] = []
    for source_id, (path, needle, role) in SOURCE_SPECS.items():
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


def iter_scan_files() -> Iterable[Path]:
    roots = [FORMAL, POST]
    for scan_root in roots:
        if not scan_root.exists():
            continue
        for path in scan_root.rglob("*"):
            if not path.is_file():
                continue
            if path.suffix.lower() not in {".md", ".txt", ".csv"}:
                continue
            if "source-intake" in path.parts and path.name.startswith("P8_Y5_R2FR_4295"):
                continue
            if path.stat().st_size > 500_000:
                continue
            yield path


def corpus_signature_hit_rows() -> List[Dict[str, str]]:
    rows: List[Dict[str, str]] = []
    for path in iter_scan_files():
        text = read_text(path)
        lower = text.lower()
        terms_found = [term for term in SCAN_TERMS if term.lower() in lower]
        if not terms_found:
            continue
        score = len(terms_found)
        if "not parent-signed" in lower or "not promoted" in lower or "not derived" in lower:
            score += 2
        if "s_parent" in lower and "s_tr" in lower:
            score += 3
        if "p_leak" in lower or "p_kernel" in lower:
            score += 2
        rows.append(
            {
                **common(),
                "hit_id": f"HIT4295_{len(rows):04d}",
                "path": str(path),
                "terms_found": ";".join(terms_found),
                "term_count": str(len(terms_found)),
                "scan_score": str(score),
                "relative_path": str(path.relative_to(ROOT)),
                "claim_allowed": "False",
                "valid_for_claim": "False",
            }
        )
    rows.sort(key=lambda row: (-int(row["scan_score"]), row["relative_path"]))
    selected = rows[:220]
    selected_paths = {row["path"] for row in selected}
    for source_id, (path, _needle, role) in SOURCE_SPECS.items():
        if str(path) in selected_paths:
            continue
        text = read_text(path)
        lower = text.lower()
        terms_found = [term for term in SCAN_TERMS if term.lower() in lower]
        selected.append(
            {
                **common(),
                "hit_id": f"HIT4295_FORCED_{source_id}",
                "path": str(path),
                "terms_found": ";".join(terms_found) if terms_found else "source_register_forced_include",
                "term_count": str(len(terms_found)),
                "scan_score": "forced_source_register",
                "relative_path": str(path.relative_to(ROOT)),
                "claim_allowed": "False",
                "valid_for_claim": "False",
                "role": role,
            }
        )
    return selected


def clause_promotion_rows() -> List[Dict[str, str]]:
    raw = [
        (
            "CLAUSE4295_0_same_metric_Hilbert_source",
            "same-metric Hilbert source for q_tr",
            "PARTIAL_SUPPORT_FOR_ORDINARY_SOURCES_ONLY",
            "185 signs ordinary Hilbert source descent; 137/138/4290/4292 do not parent-sign S_tr^H for raw transition.",
            "SRC4295_01_185_source_descent;SRC4295_14_305_split;SRC4295_17_308_membership",
            "P_nonHilbert_action_domain",
        ),
        (
            "CLAUSE4295_1_same_worldtube_before_readout",
            "q_tr support belongs to W_H before M_H^dress readout",
            "PARTIAL_SUPPORT_FOR_JH_SELECTOR_ONLY",
            "186/4291 solve PiM-Htau inside the selector, but 1016/4292 say current MTS has not signed transition worldtube membership.",
            "SRC4295_02_186_worldtube;SRC4295_16_307_narrowing;SRC4295_19_1016_selector",
            "P_off_worldtube_readout_order",
        ),
        (
            "CLAUSE4295_2_static_l0_exterior",
            "transition exterior is static pure l=0",
            "NOT_PARENT_SIGNED_FOR_RAW_TRANSITION",
            "305 splits monopole from residual vector; Q_l>=1 and dln_mu_tr_dt remain live.",
            "SRC4295_14_305_split;SRC4295_17_308_membership",
            "P_time_multipole",
        ),
        (
            "CLAUSE4295_3_universal_species_blind",
            "transition source is universal and species/frame/source-weight blind",
            "NOT_PARENT_SIGNED_FOR_RAW_TRANSITION",
            "185 removes independent ordinary source weights inside the selector, but 1097 retains source-weight/constant-sector leakage for current MTS.",
            "SRC4295_01_185_source_descent;SRC4295_20_1097_constants",
            "P_species_frame_source_weight",
        ),
        (
            "CLAUSE4295_4_no_finite_range_hair",
            "transition residue has no independent finite-range/radiative hair",
            "NOT_PARENT_SIGNED_FOR_RAW_TRANSITION",
            "4293 says R10 sees finite-range hair; 301 says the nonlocal owner kernel is not derived.",
            "SRC4295_13_301_nonlocal_missing;SRC4295_00_4294_theorem",
            "P_range_hair",
        ),
        (
            "CLAUSE4295_5_EH_local_metric_readout",
            "EH/PPN/clock readout after common GM absorption",
            "PRIVATE_SELECTOR_SUPPORT_NOT_GLOBAL_PARENT_ADOPTION",
            "188/190 support the EH local readout inside the selector; 190 quarantines transition/radiative interfaces.",
            "SRC4295_03_188_ppn;SRC4295_04_190_selector",
            "P_nonEH_metric_readout",
        ),
        (
            "CLAUSE4295_6_boundary_nonlocal_owner",
            "boundary/nonlocal owner routes any remaining q_tr without bulk response",
            "NOT_PARENT_SIGNED_FOR_RAW_TRANSITION",
            "192 supplies no-flux selector clauses; 298/301 say the transition kernel/nonlocal owner remains not derived.",
            "SRC4295_06_192_no_flux;SRC4295_11_298_kernel_missing;SRC4295_13_301_nonlocal_missing",
            "P_boundary_nonlocal_owner",
        ),
    ]
    return [
        {
            **common(),
            "clause_id": clause_id,
            "source_kernel_clause": clause,
            "promotion_status": status,
            "evidence_summary": summary,
            "source_ids": source_ids,
            "leak_component_if_unsigned": leak_component,
            "parent_signed_for_raw_transition": str(status == "PARENT_SIGNED_FOR_RAW_TRANSITION"),
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
        for clause_id, clause, status, summary, source_ids, leak_component in raw
    ]


def pleak_decomposition_rows() -> List[Dict[str, str]]:
    raw = [
        (
            "PLEAK4295_0",
            "P_nonHilbert_action_domain q_tr",
            "transition term is not demonstrably inside S_src/S_tr^H before variation",
            "try S_tr^H[g_obs,chi;tau] Hilbert variation or q-vertical/topological rest proof",
            "epsilon_mu_tr; gamma/beta/clock/source residual",
        ),
        (
            "PLEAK4295_1",
            "P_off_worldtube_readout_order q_tr",
            "transition support/readout order not proven to enter W_H before M_H^dress",
            "prove supp J_tr^H subset W_H before charge readout or retain epsilon_PiH-like residual",
            "GM denominator; orbital/source normalization",
        ),
        (
            "PLEAK4295_2",
            "P_time_multipole q_tr",
            "static l=0 exterior not proven",
            "derive Q_l>=1_tr=0 and dln_mu_tr_dt=0 or score multipole/Gdot rows",
            "Gdot; orbital anisotropy; PPN",
        ),
        (
            "PLEAK4295_3",
            "P_species_frame_source_weight q_tr",
            "universal species/frame/source-weight blindness not proven",
            "derive Y_WEP=0/source blindness or use 4293 WEP suppression",
            "WEP; clocks; source-charge contrast",
        ),
        (
            "PLEAK4295_4",
            "P_range_hair q_tr",
            "finite-range/radiative hair not proven absent",
            "derive alpha_tr(lambda)=0 or use reviewed R10 curve/range map",
            "R10 fifth-force; finite-range local tests",
        ),
        (
            "PLEAK4295_5",
            "P_nonEH_metric_readout q_tr",
            "transition may enter non-EH metric/clock readout outside private selector",
            "derive EH selector adoption for transition interface or use Y_gamma/Y_beta/Y_clock bounds",
            "PPN gamma; beta; clock redshift",
        ),
        (
            "PLEAK4295_6",
            "P_boundary_nonlocal_owner q_tr",
            "boundary/nonlocal owner kernel not derived",
            "derive K_Q/R_loc kernel from parent action or keep explicit no-leak closure",
            "transition local safety; profile/source rows",
        ),
    ]
    return [
        {
            **common(),
            "component_id": component_id,
            "pleak_component": component,
            "meaning": meaning,
            "next_derivation_attempt": next_attempt,
            "observable_pressure": pressure,
            "status": "LIVE_UNLESS_COMPONENT_ZERO_DERIVED_OR_4293_BOUND_SATISFIED",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
        for component_id, component, meaning, next_attempt, pressure in raw
    ]


def verdict_rows() -> List[Dict[str, str]]:
    return [
        {
            **common(),
            "verdict_id": "VERDICT4295_0_ordinary_source_kernel",
            "object": "ordinary local matter/EM/source kernel inside PPC4161 selector",
            "verdict": "FOUND_PRIVATE_SELECTOR_SIGNATURE",
            "evidence": "185+186+188+191+193 establish same-metric Hilbert source, EM stress, worldtube charge, EH/PPN readout and quotient vertical silence inside the private selector.",
            "promotion": "supports ordinary local-GR branch only; not raw transition shell membership",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            **common(),
            "verdict_id": "VERDICT4295_1_raw_transition_kernel",
            "object": "raw transition shell q_tr source kernel",
            "verdict": "NOT_PARENT_SIGNED",
            "evidence": "137/138/298/301/305/306/308/1016/1097 keep the transition action-domain, worldtube, species, range, and owner-kernel clauses unsigned.",
            "promotion": "do not promote 4294 theorem to local-GR claim",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            **common(),
            "verdict_id": "VERDICT4295_2_precise_reduction",
            "object": "P_leak q_tr",
            "verdict": "REDUCED_TO_SEVEN_COMPONENTS",
            "evidence": "4295 P_leak decomposition rows name the remaining leak channels and observable pressure.",
            "promotion": "next work can attack components directly rather than circling generic coupling language",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
    ]


def decision_rows() -> List[Dict[str, str]]:
    return [
        {
            **common(),
            "decision_id": "D4295_0",
            "decision": DECISION,
            "what_moved": "The corpus does contain a real ordinary-source kernel; the missing object is specifically raw-transition membership in that kernel.",
            "best_next": "Attack P_nonHilbert_action_domain and P_off_worldtube_readout_order first, because they decide whether epsilon_mu_tr is ordinary source dressing or a real residual.",
            "next_target": NEXT_TARGET,
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
    ]


def firewall_rows() -> List[Dict[str, str]]:
    raw = [
        ("FW4295_0_no_selector_overpromotion", "Ordinary-source PPC4161 selector evidence cannot be promoted to raw-transition source-kernel membership."),
        ("FW4295_1_no_no_flux_overreach", "No-flux closure is not the same as same-worldtube Hilbert source ownership."),
        ("FW4295_2_no_common_GM_hiding", "Only a static universal l=0 Hilbert source can be absorbed into common GM; all P_leak components remain visible."),
        ("FW4295_3_no_R10_shortcut", "Range-free must be derived; R10 cannot be bypassed by calling the shell a source."),
        ("FW4295_4_nonclaim", "No local-GR, WEP, R10, PPN, clock, orbital, or public theory claim is allowed from 4295."),
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
            "status_id": "STATUS4295_0",
            "ordinary_source_kernel_private_selector": "FOUND",
            "raw_transition_source_kernel_parent_signed": "False",
            "pleak_component_count": str(len(pleak_decomposition_rows())),
            "primary_next_component": "P_nonHilbert_action_domain q_tr",
            "secondary_next_component": "P_off_worldtube_readout_order q_tr",
            "next_target": NEXT_TARGET,
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
    ]


def next_target_rows() -> List[Dict[str, str]]:
    return [
        {
            **common(),
            "target_id": "NEXT4295_0",
            "next_target": NEXT_TARGET,
            "objective": "Try to zero the first P_leak components directly: show q_tr descends as q-vertical/topological/Hilbert-source owned before variation, or turn the surviving component into a 4293-compatible bound row.",
            "priority_order": "P_nonHilbert_action_domain; P_off_worldtube_readout_order; P_time_multipole; P_species_frame_source_weight; P_range_hair; P_nonEH_metric_readout; P_boundary_nonlocal_owner",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
    ]


def formal_doc() -> str:
    return f"""
# 311 parent-action source-kernel signature search and leak-projector reduction

Marker: `{MARKER}`

Branch: `{BRANCH}`

Decision: `{DECISION}`

## What the search found

4295 searched the current local corpus for the actual parent-action signature required by 4294.

The good news:

```text
ordinary local source kernel = found inside the private PPC4161 selector.
```

The corpus has a coherent ordinary-source chain:

```text
same observed metric/coframe Hilbert source,
Maxwell-Hodge/Poynting stress owner,
Hamiltonian worldtube mass charge,
quotient vertical silence,
EH/PPN readout.
```

So the local-GR path is not empty ceremony. There is a real field-theory spine for ordinary sources.

The hard news:

```text
raw transition shell q_tr source-kernel membership = not parent-signed.
```

The source-kernel theorem from 4294 therefore cannot yet be promoted to a local-GR claim for the transition shell.

## Reduced leak projector

4295 reduces the generic statement

```text
P_leak q_tr != proven zero
```

to seven exact components:

```text
P_leak q_tr =
  P_nonHilbert_action_domain q_tr
+ P_off_worldtube_readout_order q_tr
+ P_time_multipole q_tr
+ P_species_frame_source_weight q_tr
+ P_range_hair q_tr
+ P_nonEH_metric_readout q_tr
+ P_boundary_nonlocal_owner q_tr.
```

This is the useful step. The problem is no longer "the coupling" in foggy language. The next proof attempts have named handles.

## Best next attack

Attack first:

```text
P_nonHilbert_action_domain q_tr = 0
```

by proving one of:

```text
q_tr comes from S_tr^H[g_obs,chi;tau] before variation;
q_tr is q-vertical and therefore invisible by quotient naturality;
q_tr is q-owned exact/topological rest with no local bulk response.
```

If that fails, attack:

```text
P_off_worldtube_readout_order q_tr = 0
```

by proving:

```text
supp J_tr^H subset W_H before M_H^dress readout.
```

If neither closes, the component has to go back through the 4293 local bound rows.

## Status

Private nonclaim. No local-GR, WEP, R10, PPN, clock, or orbital pass is claimed.

Next target: `{NEXT_TARGET}`.
"""


def checkpoint_doc() -> str:
    return f"""
# 4295 Y5 R2FR parent-action source-kernel signature search

## Purpose

Search the current corpus for the source-kernel parent-action signature required by 4294, and reduce any failure into exact `P_leak` components.

## Outcome

The ordinary-source kernel exists inside the private selector, but the raw transition shell is not parent-signed into that kernel.

The transition problem is reduced to:

```text
P_nonHilbert_action_domain,
P_off_worldtube_readout_order,
P_time_multipole,
P_species_frame_source_weight,
P_range_hair,
P_nonEH_metric_readout,
P_boundary_nonlocal_owner.
```

## Next

Try to prove the first two components zero before doing more numeric bound rows.
"""


def validation_rows(paths: Dict[str, Path]) -> List[Dict[str, str]]:
    sources = csv_rows(paths["sources"])
    hits = csv_rows(paths["corpus_hits"])
    audit = csv_rows(paths["clause_audit"])
    pleak = csv_rows(paths["pleak_decomposition"])
    verdict = csv_rows(paths["verdict"])
    no_claim_rows = True
    for key, path in paths.items():
        if key == "validation":
            continue
        for row in csv_rows(path):
            if row.get("claim_allowed") == "True" or row.get("valid_for_claim") == "True":
                no_claim_rows = False
    validations = [
        ("VAL4295_0_sources_exist", bool(sources) and all(row["exists"] == "True" for row in sources), "all cited local sources exist"),
        ("VAL4295_1_needles_found", bool(sources) and all(row["required_text_found"] == "True" for row in sources), "all source needles found"),
        (
            "VAL4295_2_corpus_hits_include_core_sources",
            bool(hits)
            and any("185-PPC4161-Hilbert-source-measure" in row["path"] for row in hits)
            and any("1009-Y5-R10-parent-current-chain" in row["path"] for row in hits),
            "corpus signature scan includes core ordinary-source and parent-contract hits",
        ),
        (
            "VAL4295_3_no_raw_transition_parent_signature",
            bool(audit)
            and not any(row["parent_signed_for_raw_transition"] == "True" for row in audit)
            and any(row["promotion_status"] == "PARTIAL_SUPPORT_FOR_ORDINARY_SOURCES_ONLY" for row in audit),
            "audit refuses raw transition promotion while retaining ordinary-source support",
        ),
        (
            "VAL4295_4_pleak_components_complete",
            {row["pleak_component"] for row in pleak}
            == {
                "P_nonHilbert_action_domain q_tr",
                "P_off_worldtube_readout_order q_tr",
                "P_time_multipole q_tr",
                "P_species_frame_source_weight q_tr",
                "P_range_hair q_tr",
                "P_nonEH_metric_readout q_tr",
                "P_boundary_nonlocal_owner q_tr",
            },
            "P_leak decomposition covers all live components",
        ),
        (
            "VAL4295_5_verdict_split",
            any(row["verdict_id"] == "VERDICT4295_0_ordinary_source_kernel" and row["verdict"] == "FOUND_PRIVATE_SELECTOR_SIGNATURE" for row in verdict)
            and any(row["verdict_id"] == "VERDICT4295_1_raw_transition_kernel" and row["verdict"] == "NOT_PARENT_SIGNED" for row in verdict),
            "verdict separates ordinary-source kernel from raw transition kernel",
        ),
        ("VAL4295_6_formal_doc", FORMAL_PATH.exists() and MARKER in read_text(FORMAL_PATH), "formal document exists with marker"),
        ("VAL4295_7_checkpoint_doc", DOC_PATH.exists() and CHECKPOINT in read_text(DOC_PATH), "post-checkpoint document exists"),
        (
            "VAL4295_8_claim_row",
            any(line.startswith(f"{CLAIM_ID},") for line in read_text(FORMAL / "02-claims-register.csv").splitlines()),
            "claims register contains L-136 private nonclaim row",
        ),
        (
            "VAL4295_9_spine_packet",
            MARKER in read_text(FORMAL / "07-unification-spine.md")
            and PACKET_MARKER in read_text(FORMAL / "180-PPC4161-private-local-packet-integration.md"),
            "spine and packet markers exist",
        ),
        ("VAL4295_10_no_claim_rows", no_claim_rows, "all generated rows remain nonclaim rows"),
    ]
    for name, path in paths.items():
        if name == "validation":
            continue
        validations.append((f"VAL4295_csv_{name}", bool(csv_rows(path)), f"{path.name} parses with rows"))
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
        "sources": SOURCE_DIR / "P8_Y5_R2FR_4295_SOURCE_REGISTER.csv",
        "corpus_hits": SOURCE_DIR / "P8_Y5_R2FR_4295_CORPUS_SIGNATURE_HITS.csv",
        "clause_audit": SOURCE_DIR / "P8_Y5_R2FR_4295_CLAUSE_PROMOTION_AUDIT.csv",
        "pleak_decomposition": SOURCE_DIR / "P8_Y5_R2FR_4295_PLEAK_DECOMPOSITION.csv",
        "verdict": SOURCE_DIR / "P8_Y5_R2FR_4295_PARENT_SIGNATURE_VERDICT.csv",
        "decision": SOURCE_DIR / "P8_Y5_R2FR_4295_DECISION.csv",
        "firewall": SOURCE_DIR / "P8_Y5_R2FR_4295_CLAIM_FIREWALL.csv",
        "status": SOURCE_DIR / "P8_Y5_R2FR_4295_STATUS.csv",
        "next_target": SOURCE_DIR / "P8_Y5_R2FR_4295_NEXT_TARGET.csv",
        "validation": VALIDATION_PATH,
    }
    write_csv(paths["sources"], source_rows())
    write_csv(paths["corpus_hits"], corpus_signature_hit_rows())
    write_csv(paths["clause_audit"], clause_promotion_rows())
    write_csv(paths["pleak_decomposition"], pleak_decomposition_rows())
    write_csv(paths["verdict"], verdict_rows())
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
        "PPC4161 4295 source-kernel signature search",
        (
            "4295 finds that the ordinary local source kernel is real inside the private PPC4161 selector, but the raw "
            "transition shell is not parent-signed into that kernel. `P_leak q_tr` is reduced to seven named components, "
            "with `P_nonHilbert_action_domain` and `P_off_worldtube_readout_order` the first proof targets."
        ),
    )
    append_unique_block(
        FORMAL / "180-PPC4161-private-local-packet-integration.md",
        PACKET_MARKER,
        "4295 packet source-kernel signature search",
        (
            "Packet update: stop treating the coupling as fog. The ordinary-source selector kernel exists; the transition "
            "kernel does not yet. The next derivation attacks the first two `P_leak` components directly."
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

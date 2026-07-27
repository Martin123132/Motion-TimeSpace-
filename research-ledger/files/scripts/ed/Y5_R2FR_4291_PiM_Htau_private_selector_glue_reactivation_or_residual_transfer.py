from __future__ import annotations

import csv
import io
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List


ROOT = Path(__file__).resolve().parents[2]
FORMAL = ROOT / "formalization-workbench"
POST = ROOT / "post-checkpoint-work"
SOURCE_DIR = POST / "source-intake" / "mts_residuals"

CHECKPOINT = "4291"
CLAIM_ID = "L-132"
BRANCH = "MTS_R2FR_Y5_PIM_HTAU_PRIVATE_SELECTOR_GLUE_REACTIVATION_OR_RESIDUAL_TRANSFER_4291"
DECISION = "PIM_HTAU_GLUE_ZERO_INSIDE_HAMILTONIAN_SELECTOR_RESIDUAL_TRANSFER_OUTSIDE_SELECTOR_NONCLAIM"
MARKER = "PPC4161_PIM_HTAU_PRIVATE_SELECTOR_GLUE_REACTIVATION_OR_RESIDUAL_TRANSFER_4291"
PACKET_MARKER = "PPC4161_PACKET_PIM_HTAU_PRIVATE_SELECTOR_GLUE_REACTIVATION_OR_RESIDUAL_TRANSFER_4291"
NEXT_TARGET = "4292-Y5-R2FR-transition-membership-and-nonEH-monopole-zero-proof-or-source-residual-vector.md"

FORMAL_PATH = FORMAL / "307-PPC4161-PiM-Htau-private-selector-glue-reactivation-or-residual-transfer.md"
DOC_PATH = POST / "4291-Y5-R2FR-PiM-Htau-private-selector-glue-reactivation-or-residual-transfer.md"
VALIDATION_PATH = SOURCE_DIR / "P8_Y5_BRR545_4291_VALIDATION.csv"

STAMP = datetime.now(timezone.utc).replace(microsecond=0).isoformat()

SOURCES = {
    "SRC4291_00_186_private_charge_glue": (
        FORMAL / "186-PPC4161-Hamiltonian-worldtube-mass-readout-glue.md",
        "ell_M(Pi_M^H J_H_total) := M_H^dress[W_H;tau].",
        "186 already defines the private Hamiltonian mass projector on the same source charge.",
    ),
    "SRC4291_01_186_no_orbital_GM": (
        FORMAL / "186-PPC4161-Hamiltonian-worldtube-mass-readout-glue.md",
        "No orbital `GM`, fitted acceleration, or measured Newton constant is used",
        "186 contains the anti-circularity guard for the private selector.",
    ),
    "SRC4291_02_4156_constraint_map": (
        POST / "4156-Y5-R2FR-PiM-Htau-same-charge-glue-or-radial-source-residual.md",
        "Pi_M^C := D_N[C_tau]|_{J_H[tau]}",
        "4156 supplies the non-circular constraint-map projector construction.",
    ),
    "SRC4291_03_4156_same_charge_conditional": (
        SOURCE_DIR / "P8_Y5_R2FR_4156_CONSTRAINT_MAP_GLUE.csv",
        "SAME_CHARGE_THEOREM_DERIVED_CONDITIONAL_UNSIGNED",
        "4156 says the same-charge theorem is derived conditionally, not globally signed.",
    ),
    "SRC4291_04_4156_status": (
        SOURCE_DIR / "P8_Y5_R2FR_4156_STATUS.csv",
        "same_charge_theorem_derived_conditional",
        "4156 machine status records the conditional same-charge route.",
    ),
    "SRC4291_05_4012_double_zero": (
        SOURCE_DIR / "P8_Y5_R2FR_4012_PIM_HTAU_CHARGE_LOCK_THEOREM.csv",
        "CHG4012_5_double_zero_branch",
        "4012 assembles the PiM/Htau double-zero branch as a conditional theorem.",
    ),
    "SRC4291_06_4160_fixedness": (
        SOURCE_DIR / "P8_Y5_R2FR_4160_PIM_FIXEDNESS_THEOREM.csv",
        "PIM_FIXEDNESS_ZERO_CONDITIONAL",
        "4160 gives fixed-projector variation zero under the selected local packet.",
    ),
    "SRC4291_07_3986_rank_one": (
        SOURCE_DIR / "P8_Y5_R2FR_3986_PIM_HILBERT_EQUALITY_REDUCTION_THEOREM.csv",
        "RANK_ONE_CHARGE_DIRECTION_DERIVED",
        "3986 reduces source amplitude to one mass-charge direction plus explicit residuals.",
    ),
    "SRC4291_08_4108_components": (
        SOURCE_DIR / "P8_Y5_R2FR_4108_PIM_HTAU_SUBDENOMINATOR.csv",
        "R_PiM+R_Htau = C_M+C_shape+C_curl+C_domain+C_ref+C_frame+C_units",
        "4108 names the fallback subdenominator residual components.",
    ),
    "SRC4291_09_4290_blocker": (
        FORMAL / "306-PPC4161-transition-Hilbert-monopole-source-lock-or-first-residual-bound-row.md",
        "Pi_M/H_tau same-branch glue = unsigned,",
        "4290 is the immediate source-lock blocker being refined.",
    ),
    "SRC4291_10_4290_epsilon": (
        SOURCE_DIR / "P8_Y5_R2FR_4290_EPSILON_MU_BOUND_ROW.csv",
        "epsilon_mu_tr = mu_extra_tr/(G_cal M_H^dress)",
        "4290 supplies the first transition non-EH monopole residual.",
    ),
    "SRC4291_11_3998_no_backfill": (
        SOURCE_DIR / "P8_Y5_R2FR_3998_GM_ANTI_BACKFILL_CONTRACT.csv",
        "do not set M_H_ref=mu_obs/G0",
        "3998 forbids replacing the theorem with measured-GM backfill.",
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
                "4291 reconciles the Pi_M/H_tau source-glue ladder. The equality is not empty or merely missing: "
                "inside the private Hamiltonian selector where Pi_M is defined as Pi_M^H / Pi_M^C from the same "
                "covariant Hamiltonian charge, Q_M=ell_M(Pi_M^H J_H_total)=H_tau[S_link]-H_ref=M_H^dress and "
                "epsilon_PiH=0 by construction plus conditional covariant-phase-space glue. Outside that selector, "
                "the same issue remains an explicit fallback residual epsilon_PiH bounded by kernel, commutator, curl, "
                "reference, frame, units, boundary, symplectic, EM-flux and extra-sector components. Thus the 4290 "
                "transition source-lock blocker is narrowed: Pi_M/H_tau is not the main live obstruction inside the "
                "private selector; the remaining live transition requirements are same-worldtube membership and zero/bound "
                "for non-EH monopole epsilon_mu_tr, multipoles and hair."
            ),
            (
                "4291 source register, private selector glue theorem rows, commutative diagram, residual transfer rows, "
                "transition-lock reduction, strict control runner, decision and firewall."
            ),
            "private_PiM_Htau_zero_inside_Hamiltonian_selector_transition_residual_transfer_nonclaim",
            (
                "Prove transition shell membership in the same Hilbert worldtube and derive or bound the non-EH monopole "
                "epsilon_mu_tr plus multipole/time/range/frame residuals."
            ),
            (
                "Claiming global parent adoption of Pi_M/H_tau, using measured orbital GM to define the denominator, "
                "treating the private selector as public evidence, or ignoring the remaining transition non-Hilbert residual vector."
            ),
        ]
    )
    path.write_text(text.rstrip() + "\n" + row + "\n", encoding="utf-8")


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


def glue_theorem_rows() -> List[Dict[str, str]]:
    raw = [
        (
            "GT4291_0_old_private_selector",
            "Hamiltonian selector already defines the mass projector",
            "Pi_M := Pi_M^H and ell_M(Pi_M^H J_H_total) := M_H^dress[W_H;tau]",
            "PRIVATE_SELECTOR_DEFINITION_AVAILABLE",
            "This is a legitimate local-branch definition, not an orbital fit.",
            "epsilon_PiH=0 inside the selector",
        ),
        (
            "GT4291_1_constraint_map_projector",
            "non-circular constraint-map construction",
            "Pi_M^C := D_N[C_tau]|_{J_H[tau]}",
            "CONSTRUCTIVE_ROUTE_AVAILABLE",
            "The projector is the exterior constraint/boundary-charge pushforward from Hilbert source current.",
            "same object as H_tau if the parent map is unique and fixed",
        ),
        (
            "GT4291_2_covariant_phase_space_charge",
            "Hamiltonian charge exactness",
            "delta H_tau[S]=int_S(delta Q_tau-i_tau theta_total)",
            "CONDITIONAL_FROM_186_4012",
            "H_tau is a real charge only when curl/corner/reference/extra terms vanish or are bounded.",
            "path-dependent H_tau becomes epsilon_PiH rather than hidden glue",
        ),
        (
            "GT4291_3_same_worldtube",
            "same Hilbert support and same tau/reference/frame",
            "W_H=closure(supp J_H_total); same tau, H_ref, S_link, frame, units",
            "CONDITIONAL_BRANCH_REQUIREMENT",
            "Prevents choosing a new denominator after seeing local/orbital data.",
            "if not fixed, C_domain/C_ref/C_frame/C_units remain live",
        ),
        (
            "GT4291_4_private_zero",
            "private selector PiM/Htau residual",
            "epsilon_PiH := |ell_M(Pi_M^H J_H_total)-(H_tau[S_link]-H_ref)|/|M_H^dress| = 0",
            "ZERO_INSIDE_PRIVATE_HAMILTONIAN_SELECTOR",
            "This resolves the algebraic PiM/Htau blocker inside the adopted PPC4161-HQ branch.",
            "not global MTS adoption and not public local-GR evidence",
        ),
        (
            "GT4291_5_fallback_residual",
            "outside-selector fallback",
            "epsilon_PiH <= |R_kernel|+|I_commutator|+|C_curl|+|C_ref|+|C_frame|+|C_units|+|R_extra|+|R_symp|+|R_boundary|+|R_EM_flux|",
            "FINITE_RESIDUAL_TRANSFER",
            "If the Hamiltonian selector is not adopted, every failed premise is a named bound component.",
            "no cancellation credit and no measured-GM backfill",
        ),
    ]
    return [
        {
            **common(),
            "theorem_id": theorem_id,
            "claim_piece": claim_piece,
            "formula": formula,
            "status": status,
            "derivation": derivation,
            "implication": implication,
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
        for theorem_id, claim_piece, formula, status, derivation, implication in raw
    ]


def diagram_rows() -> List[Dict[str, str]]:
    raw = [
        ("DG4291_0", "J_H_total", "Pi_M^H", "ell_M(Pi_M^H J_H_total)", "Hilbert current to mass functional", "commutes inside selector"),
        ("DG4291_1", "J_H_total", "Noether/Hamiltonian map", "H_tau[S_link]-H_ref", "same current to covariant Hamiltonian charge", "commutes if H_tau exact"),
        ("DG4291_2", "ell_M(Pi_M^H J_H_total)", "definition lock", "M_H^dress[W_H;tau]", "private branch mass definition", "zero residual by selector"),
        ("DG4291_3", "H_tau[S_link]-H_ref", "worldtube readout", "M_H^dress[W_H;tau]", "same Hamiltonian source charge", "zero residual by selector"),
        ("DG4291_4", "M_H^dress[W_H;tau]", "Poisson/Gauss readout", "G_cal M_H^dress", "Newton source coefficient after one calibrated G", "structural not numeric-G prediction"),
    ]
    return [
        {
            **common(),
            "edge_id": edge_id,
            "from_node": from_node,
            "map": map_name,
            "to_node": to_node,
            "meaning": meaning,
            "status": status,
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
        for edge_id, from_node, map_name, to_node, meaning, status in raw
    ]


def residual_transfer_rows() -> List[Dict[str, str]]:
    raw = [
        ("RT4291_0_epsilon_PiH_private", "epsilon_PiH", "0", "ZERO_INSIDE_PRIVATE_SELECTOR", "Pi_M is defined as the same Hamiltonian mass covector."),
        ("RT4291_1_kernel", "R_kernel", "homogeneous 1/r mass kernel", "FALLBACK_COMPONENT", "Only live outside the selected/unique constraint-map branch."),
        ("RT4291_2_commutator", "I_commutator", "[d,Pi_M]J_H", "FALLBACK_COMPONENT", "Killed if Pi_M is fixed chain map on Hilbert current complex."),
        ("RT4291_3_curl", "C_curl", "d_field alpha_tau", "FALLBACK_COMPONENT", "Killed if H_tau is integrable after corner/reference terms."),
        ("RT4291_4_reference_frame_units", "C_ref+C_frame+C_units", "fixed source denominator data", "FALLBACK_COMPONENT", "Killed only by pre-readout parent ownership."),
        ("RT4291_5_fluxes", "R_extra+R_symp+R_boundary+R_EM_flux", "unowned extra/boundary/radiative terms", "FALLBACK_COMPONENT", "Must be zero, topological, or bounded; Poynting is counted once."),
        ("RT4291_6_transition_remaining", "epsilon_mu_tr+Q_l_ge_1_tr+hair", "non-Hilbert transition residual vector", "LIVE_AFTER_PIM_HTAU_TRANSFER", "This is the next real target after PiM/Htau is moved into the selector."),
    ]
    return [
        {
            **common(),
            "residual_id": residual_id,
            "symbol": symbol,
            "formula_or_component": formula,
            "status": status,
            "meaning": meaning,
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
        for residual_id, symbol, formula, status, meaning in raw
    ]


def transition_reduction_rows() -> List[Dict[str, str]]:
    raw = [
        (
            "TR4291_0_PiM_Htau",
            "Pi_M/H_tau same-branch glue",
            "UNSIGNED in 4290 if asking for global parent adoption",
            "ZERO_INSIDE_PRIVATE_HAMILTONIAN_SELECTOR",
            "do not keep spending effort here unless the task is global parent adoption",
        ),
        (
            "TR4291_1_membership",
            "transition shell belongs to same Hilbert worldtube",
            "not proved by PiM/Htau algebra",
            "LIVE_BLOCKER",
            "prove q_tr^Hilbert-monopole is in J_H_total before readout",
        ),
        (
            "TR4291_2_nonEH_monopole",
            "zero/bound for mu_extra_tr",
            "4290 first bound row exists",
            "LIVE_BLOCKER_WITH_BOUND_ROW",
            "derive mu_extra_tr=0 or score epsilon_mu_tr across arenas",
        ),
        (
            "TR4291_3_multipoles_hair",
            "Q_l>=1_tr plus time/range/frame/species/beta hair",
            "not absorbable into monopole source charge",
            "LIVE_BLOCKER",
            "must be zero or independently bounded",
        ),
        (
            "TR4291_4_updated_verdict",
            "source-lock frontier after 4291",
            "PiM/Htau narrowed; transition residual vector remains",
            "PIM_HTAU_NOT_MAIN_BLOCKER_INSIDE_SELECTOR",
            "next target is transition membership/non-EH monopole proof",
        ),
    ]
    return [
        {
            **common(),
            "reduction_id": reduction_id,
            "item": item,
            "prior_status": prior_status,
            "updated_status": updated_status,
            "next_action": next_action,
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
        for reduction_id, item, prior_status, updated_status, next_action in raw
    ]


def control_rows() -> List[Dict[str, str]]:
    controls = [
        ("CTRL4291_0_private_selector_clean", True, True, True, True, False, False, True, "PASS_PIM_HTAU_ZERO_INSIDE_SELECTOR"),
        ("CTRL4291_1_no_selector", False, True, True, True, False, False, False, "FAIL_SELECTOR_NOT_ADOPTED"),
        ("CTRL4291_2_live_kernel", True, False, True, True, False, False, False, "FAIL_KERNEL_RESIDUAL"),
        ("CTRL4291_3_live_curl", True, True, False, True, False, False, False, "FAIL_HTAU_CURL_RESIDUAL"),
        ("CTRL4291_4_measured_GM_backfill", True, True, True, True, True, False, False, "FAIL_BACKFILL_FORBIDDEN"),
        ("CTRL4291_5_transition_nonEH_live", True, True, True, True, False, True, False, "FAIL_TRANSITION_RESIDUAL_REMAINS"),
    ]
    rows = []
    for control_id, selector, kernel_zero, h_tau_exact, fixed_data, measured_gm, transition_residual, expected, expected_outcome in controls:
        if measured_gm:
            actual = False
            outcome = "FAIL_BACKFILL_FORBIDDEN"
        elif not selector:
            actual = False
            outcome = "FAIL_SELECTOR_NOT_ADOPTED"
        elif not kernel_zero:
            actual = False
            outcome = "FAIL_KERNEL_RESIDUAL"
        elif not h_tau_exact:
            actual = False
            outcome = "FAIL_HTAU_CURL_RESIDUAL"
        elif not fixed_data:
            actual = False
            outcome = "FAIL_DENOMINATOR_DATA_MOVES"
        elif transition_residual:
            actual = False
            outcome = "FAIL_TRANSITION_RESIDUAL_REMAINS"
        else:
            actual = True
            outcome = "PASS_PIM_HTAU_ZERO_INSIDE_SELECTOR"
        rows.append(
            {
                **common(),
                "control_id": control_id,
                "hamiltonian_selector_adopted": str(selector),
                "kernel_zero_or_absorbed": str(kernel_zero),
                "H_tau_exact": str(h_tau_exact),
                "tau_ref_frame_units_fixed": str(fixed_data),
                "measured_GM_backfill_attempt": str(measured_gm),
                "transition_residual_live": str(transition_residual),
                "epsilon_PiH": "0" if actual or transition_residual else "UNSCORED_OR_NONZERO",
                "actual_pass": str(actual),
                "expected_pass": str(expected),
                "expected_outcome": expected_outcome,
                "outcome": outcome,
                "expected_matches_actual": str(actual == expected and outcome == expected_outcome),
                "claim_allowed": "False",
                "valid_for_claim": "False",
            }
        )
    return rows


def decision_rows() -> List[Dict[str, str]]:
    return [
        {
            **common(),
            "decision_id": "D4291_0",
            "decision": DECISION,
            "what_changed": "Pi_M/H_tau is no longer treated as an undifferentiated blocker inside the private Hamiltonian selector; it is zero there and a named epsilon_PiH residual outside it.",
            "still_missing": "transition same-worldtube membership; zero/bound for epsilon_mu_tr; multipoles and time/range/frame/species/beta hair",
            "next_target": NEXT_TARGET,
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
    ]


def firewall_rows() -> List[Dict[str, str]]:
    raw = [
        ("FW4291_0_private_not_public", "PiM/Htau zero is private-selector glue, not global parent adoption."),
        ("FW4291_1_no_GM_backfill", "Measured orbital GM cannot define M_H or hide epsilon_PiH."),
        ("FW4291_2_no_transition_overreach", "Solving PiM/Htau does not prove transition shell membership or kill epsilon_mu_tr."),
        ("FW4291_3_no_double_count", "Poynting/EM energy is counted once through J_H_total or routed as boundary flux."),
        ("FW4291_4_nonclaim_rows", "All 4291 rows stay valid_for_claim=false until parent adoption and empirical residual scoring exist."),
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
            "status_id": "STATUS4291_0",
            "result": "PIM_HTAU_GLUE_ZERO_INSIDE_PRIVATE_SELECTOR_TRANSITION_RESIDUAL_REMAINS",
            "epsilon_PiH_private_selector": "0",
            "global_parent_PiM_Htau_claimed": "False",
            "transition_source_lock_claimed": "False",
            "remaining_primary_blocker": "transition membership and epsilon_mu_tr/non-Hilbert residual vector",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
    ]


def next_target_rows() -> List[Dict[str, str]]:
    return [
        {
            **common(),
            "target_id": "NEXT4291_0",
            "next_target": NEXT_TARGET,
            "objective": "Prove q_tr^Hilbert-monopole is in the same J_H_total/worldtube before readout and derive mu_extra_tr=0, or score epsilon_mu_tr plus multipole/hair residuals.",
            "why": "4291 removes PiM/Htau as the main blocker inside the private selector; remaining failure is transition ownership/non-Hilbert residue.",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
    ]


def formal_doc() -> str:
    return f"""
# 307 PiM Htau private selector glue reactivation or residual transfer

Marker: `{MARKER}`

Branch: `{BRANCH}`

Decision: `{DECISION}`

## Result

4291 rechecks the `Pi_M/H_tau` blocker against the actual corpus.

The important correction is:

```text
Pi_M/H_tau glue is not an empty missing object inside the private Hamiltonian selector.
```

Inside the PPC4161 Hamiltonian-source branch:

```text
Pi_M := Pi_M^H,
ell_M(Pi_M^H J_H_total) := M_H^dress[W_H;tau],
M_H^dress[W_H;tau] = H_tau[S_link] - H_ref.
```

Therefore the private-selector residual is:

```text
epsilon_PiH := |ell_M(Pi_M^H J_H_total) - (H_tau[S_link]-H_ref)|/|M_H^dress| = 0.
```

That does **not** prove global MTS parent adoption. It says the local private branch has a legitimate field-theory source denominator if the Hamiltonian selector is adopted before readout.

## Outside The Selector

If the Hamiltonian selector is not adopted, the fallback residual is:

```text
epsilon_PiH <= |R_kernel| + |I_commutator| + |C_curl| + |C_ref| + |C_frame| + |C_units| + |R_extra| + |R_symp| + |R_boundary| + |R_EM_flux|.
```

No cancellation credit and no measured-`GM` backfill are allowed.

## Impact On 4290

4290 listed two source-lock blockers:

```text
Pi_M/H_tau same-branch glue,
zero non-EH monopole.
```

4291 narrows the first one:

```text
Pi_M/H_tau = solved inside private Hamiltonian selector,
Pi_M/H_tau = explicit epsilon_PiH residual outside selector.
```

So the next live transition problem is not generic source-denominator glue. It is:

```text
transition same-worldtube membership,
epsilon_mu_tr = 0 or bounded,
Q_l>=1_tr = 0 or bounded,
time/range/frame/species/beta hair = 0 or bounded.
```

This is a useful leap: the target has moved from "the coupling" in general to the transition shell's non-Hilbert residue.
"""


def checkpoint_doc() -> str:
    return f"""
# 4291 Y5 R2FR PiM Htau private selector glue reactivation or residual transfer

## Purpose

This checkpoint checks whether 4290's `Pi_M/H_tau` blocker is genuinely still open or whether the earlier PPC4161 Hamiltonian source branch already solved it privately.

## Outcome

Inside the Hamiltonian selector, it is solved by construction and covariant charge glue:

```text
epsilon_PiH = 0.
```

Outside that selector, it remains an explicit fallback residual `epsilon_PiH`, not a vague missing coupling.

## Consequence

The next local-GR/Newton transition target is sharper:

```text
prove transition-shell membership in the same Hilbert worldtube,
or bound epsilon_mu_tr and the non-monopole/hair residual vector.
```
"""


def validation_rows(paths: Dict[str, Path]) -> List[Dict[str, str]]:
    sources = csv_rows(paths["sources"])
    theorem = csv_rows(paths["glue_theorem"])
    residuals = csv_rows(paths["residual_transfer"])
    reduction = csv_rows(paths["transition_reduction"])
    controls = csv_rows(paths["control_runner"])
    no_claim_rows = True
    for key, path in paths.items():
        if key == "validation":
            continue
        for row in csv_rows(path):
            if row.get("claim_allowed") == "True" or row.get("valid_for_claim") == "True":
                no_claim_rows = False
    validations = [
        ("VAL4291_0_sources_exist", bool(sources) and all(row["exists"] == "True" for row in sources), "all cited sources exist"),
        ("VAL4291_1_needles_found", bool(sources) and all(row["required_text_found"] == "True" for row in sources), "all source needles found"),
        (
            "VAL4291_2_private_zero_present",
            any(row["theorem_id"] == "GT4291_4_private_zero" and row["status"] == "ZERO_INSIDE_PRIVATE_HAMILTONIAN_SELECTOR" for row in theorem),
            "private selector zero theorem row exists",
        ),
        (
            "VAL4291_3_fallback_residual_present",
            any(row["theorem_id"] == "GT4291_5_fallback_residual" for row in theorem)
            and any(row["symbol"] == "epsilon_PiH" for row in residuals),
            "outside-selector epsilon_PiH residual exists",
        ),
        (
            "VAL4291_4_transition_reduction",
            any(row["updated_status"] == "PIM_HTAU_NOT_MAIN_BLOCKER_INSIDE_SELECTOR" for row in reduction)
            and any(row["updated_status"] == "LIVE_BLOCKER_WITH_BOUND_ROW" for row in reduction),
            "transition frontier is reduced to membership and epsilon_mu residuals",
        ),
        (
            "VAL4291_5_control_expected_matches_actual",
            bool(controls) and all(row["expected_matches_actual"] == "True" for row in controls),
            "strict control runner has no expected/pass mismatch",
        ),
        ("VAL4291_6_formal_doc", FORMAL_PATH.exists() and MARKER in read_text(FORMAL_PATH), "formal document exists with marker"),
        ("VAL4291_7_checkpoint_doc", DOC_PATH.exists() and CHECKPOINT in read_text(DOC_PATH), "post-checkpoint document exists"),
        (
            "VAL4291_8_claim_row",
            any(line.startswith(f"{CLAIM_ID},") for line in read_text(FORMAL / "02-claims-register.csv").splitlines()),
            "claims register contains L-132 private nonclaim row",
        ),
        ("VAL4291_9_no_claim_rows", no_claim_rows, "all generated rows remain nonclaim rows"),
    ]
    for name, path in paths.items():
        if name == "validation":
            continue
        validations.append((f"VAL4291_csv_{name}", bool(csv_rows(path)), f"{path.name} parses with rows"))
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
        "sources": SOURCE_DIR / "P8_Y5_R2FR_4291_SOURCE_REGISTER.csv",
        "glue_theorem": SOURCE_DIR / "P8_Y5_R2FR_4291_PRIVATE_SELECTOR_GLUE_THEOREM.csv",
        "commutative_diagram": SOURCE_DIR / "P8_Y5_R2FR_4291_COMMUTATIVE_DIAGRAM.csv",
        "residual_transfer": SOURCE_DIR / "P8_Y5_R2FR_4291_EPSILON_PIH_RESIDUAL_TRANSFER.csv",
        "transition_reduction": SOURCE_DIR / "P8_Y5_R2FR_4291_TRANSITION_SOURCE_LOCK_REDUCTION.csv",
        "control_runner": SOURCE_DIR / "P8_Y5_R2FR_4291_CONTROL_RUNNER.csv",
        "decision": SOURCE_DIR / "P8_Y5_R2FR_4291_DECISION.csv",
        "firewall": SOURCE_DIR / "P8_Y5_R2FR_4291_CLAIM_FIREWALL.csv",
        "status": SOURCE_DIR / "P8_Y5_R2FR_4291_STATUS.csv",
        "next_target": SOURCE_DIR / "P8_Y5_R2FR_4291_NEXT_TARGET.csv",
        "validation": VALIDATION_PATH,
    }
    write_csv(paths["sources"], source_rows())
    write_csv(paths["glue_theorem"], glue_theorem_rows())
    write_csv(paths["commutative_diagram"], diagram_rows())
    write_csv(paths["residual_transfer"], residual_transfer_rows())
    write_csv(paths["transition_reduction"], transition_reduction_rows())
    write_csv(paths["control_runner"], control_rows())
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
        "PPC4161 4291 PiM/Htau private selector glue reactivation",
        (
            "4291 reconciles the source-glue ladder: inside the private Hamiltonian selector, "
            "`Pi_M := Pi_M^H` gives `ell_M(Pi_M^H J_H_total)=H_tau[S_link]-H_ref=M_H^dress`, so "
            "`epsilon_PiH=0`. Outside that selector the same issue remains a finite residual vector. "
            "The transition frontier is narrowed to same-worldtube shell membership plus `epsilon_mu_tr`, multipoles and hair."
        ),
    )
    append_unique_block(
        FORMAL / "180-PPC4161-private-local-packet-integration.md",
        PACKET_MARKER,
        "4291 packet PiM/Htau selector zero and transition residual transfer",
        (
            "Packet update: do not keep circling generic `Pi_M/H_tau` inside the private local branch. "
            "The branch already has the Hamiltonian selector zero. The live work moves to transition membership "
            "and the non-Hilbert residual vector."
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

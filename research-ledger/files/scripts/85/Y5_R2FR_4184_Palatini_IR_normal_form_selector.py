from __future__ import annotations

import csv
import py_compile
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List


ROOT = Path(
    r"D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main"
)
POST = ROOT / "post-checkpoint-work"
SOURCE_DIR = POST / "source-intake" / "mts_residuals"
FORMAL = ROOT / "formalization-workbench"
SCRIPT_PATH = Path(__file__)

CHECKPOINT = "4184"
BRANCH_ID = "MTS_R2FR_Y5_PALATINI_IR_NORMAL_FORM_SELECTOR_4184"
DECISION = (
    "CONDITIONAL_PALATINI_IR_SELECTOR_THEOREM_WRITTEN_SELECTOR_ASSUMPTIONS_"
    "NOT_PARENT_DERIVED_RESIDUAL_EFT_BOUND_LEDGER_ACTIVE"
)
DOC_PATH = POST / "4184-Y5-R2FR-Palatini-IR-normal-form-selector-under-AMF-or-residual-EFT-bound.md"
FORMAL_200_PATH = FORMAL / "200-PPC4161-Palatini-IR-normal-form-selector-under-AMF.md"
PACKET_180_PATH = FORMAL / "180-PPC4161-private-local-packet-integration.md"
CLAIMS_PATH = FORMAL / "02-claims-register.csv"
SPINE_PATH = FORMAL / "07-unification-spine.md"
CLAIM_ID = "L-025"
SPINE_MARKER = "PPC4161_PALATINI_IR_NORMAL_FORM_SELECTOR_4184"
PACKET_MARKER = "PPC4161_PACKET_PALATINI_IR_NORMAL_FORM_SELECTOR_4184"
NEXT_TARGET = "4185-Y5-R2FR-extra-invariant-residual-coefficient-map-to-PPN-R10-clocks-or-parent-scale-law.md"

SOURCES = {
    "SRC4184_00_4183_next": (
        SOURCE_DIR / "P8_Y5_R2FR_4183_NEXT_TARGET.csv",
        "derive an IR selector under A_MF",
        "4183 handoff to Palatini IR selector or residual EFT bound.",
    ),
    "SRC4184_01_formal_199": (
        FORMAL / "199-PPC4161-motion-frame-axiom-adoption-consequences-and-test-contract.md",
        "Palatini_EH_forced_by_A_MF_alone = false",
        "formal 199 says A_MF alone does not select Palatini.",
    ),
    "SRC4184_02_4183_normal_form": (
        SOURCE_DIR / "P8_Y5_R2FR_4183_IR_NORMAL_FORM_GATE.csv",
        "NF4183_2_torsion_squared",
        "4183 normal-form ledger of allowed extra invariant terms.",
    ),
    "SRC4184_03_formal_197": (
        FORMAL / "197-PPC4161-EH-local-metric-principal-block-origin-gate.md",
        "leading local two-derivative normal form is Einstein-Cartan/Palatini",
        "earlier conditional EH-origin gate naming the needed normal form.",
    ),
    "SRC4184_04_boundary": (
        FORMAL / "192-PPC4161-local-boundary-no-flux-sector-interface-theorem.md",
        "route as boundary charge, not hidden bulk current",
        "boundary/radiative routing condition.",
    ),
    "SRC4184_05_quotient": (
        FORMAL / "193-PPC4161-quotient-naturality-vertical-silence-theorem.md",
        "Vertical Silence Proof",
        "quotient and vertical representative-silence condition.",
    ),
    "SRC4184_06_source_coupling": (
        FORMAL / "194-PPC4161-calibrated-source-coupling-kappa-to-GN-law.md",
        "G_cal := c^4 kappa_eff/(8*pi)",
        "calibrated source-coupling firewall.",
    ),
    "SRC4184_07_poynting": (
        FORMAL / "191-PPC4161-Maxwell-Hodge-Poynting-stress-owner-theorem.md",
        "Poynting vector is not a separate background field",
        "same-Hodge EM/Poynting owner theorem.",
    ),
    "SRC4184_08_claim_L024": (
        CLAIMS_PATH,
        "A_MF_adoption_consequences_nonclaim",
        "latest claim row before the Palatini selector gate.",
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


def selector_axiom_rows() -> List[Dict[str, str]]:
    rows = [
        (
            "SEL4184_0_A_MF",
            "A_MF motion-frame gauge redundancy",
            "owned_as_candidate",
            "needed to make e, omega, B parent variables",
            "signed in 4183 only as explicit candidate, not older derivation",
        ),
        (
            "SEL4184_1_locality",
            "local covariant four-form action",
            "selector_assumption",
            "forbids nonlocal kernels in compact local collar",
            "not enough alone to choose Palatini",
        ),
        (
            "SEL4184_2_IR_order",
            "leading low-energy action has at most two metric derivatives / one curvature",
            "selector_assumption",
            "demotes curvature-squared and torsion-kinetic terms to EFT residuals",
            "requires parent scale separation or empirical bound",
        ),
        (
            "SEL4184_3_no_extra_light_modes",
            "no unscreened light torsion, scalar, vector, or disformal modes in local branch",
            "selector_assumption",
            "keeps local PPN/clock/R10 branch close to GR",
            "must be derived or bounded",
        ),
        (
            "SEL4184_4_same_coframe",
            "matter and Maxwell-Hodge use g_obs from the same e^A",
            "private_selector_clause",
            "protects WEP and Poynting/Hilbert stress ownership",
            "global parent adoption still open",
        ),
        (
            "SEL4184_5_boundary",
            "boundary/topological pieces are fixed, exact, or Hamiltonian-routed",
            "private_selector_clause",
            "prevents hidden bulk source leakage",
            "global boundary adoption still open",
        ),
        (
            "SEL4184_6_parity",
            "parity-even classical local gravity sector unless parity-odd terms are topological or bounded",
            "selector_assumption",
            "demotes Holst/Nieh-Yan/parity odd pieces to boundary or residual rows",
            "needs explicit policy if spin/torsion matter is included",
        ),
    ]
    return [
        {
            **common(),
            "selector_id": selector_id,
            "selector_clause": clause,
            "status": status,
            "role": role,
            "open_debt": debt,
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
        for selector_id, clause, status, role, debt in rows
    ]


def normal_form_classification_rows() -> List[Dict[str, str]]:
    rows = [
        (
            "NFC4184_0_EC_Palatini",
            "epsilon_ABCD e^A wedge e^B wedge R^CD[omega]",
            "selected_if_all_selector_clauses_hold",
            "unique parity-even local linear-curvature bulk principal term",
            "gives EC/Palatini -> EH after torsion/nonmetricity silence",
        ),
        (
            "NFC4184_1_cosmological",
            "epsilon_ABCD e^A wedge e^B wedge e^C wedge e^D",
            "allowed_relevant_vacuum_term",
            "cosmological/vacuum branch",
            "not a local-GR obstruction but must match cosmology sector",
        ),
        (
            "NFC4184_2_Holst_NiehYan",
            "e_A wedge e_B wedge R^AB and Nieh-Yan combination",
            "boundary_or_parity_residual",
            "classically silent in torsionless vacuum if routed/topological",
            "open if torsion/spin/matter makes it physical",
        ),
        (
            "NFC4184_3_torsion_squares",
            "T^A wedge star T_A and irreducible torsion squares",
            "EFT_residual_unless_parent_zero_or_heavy",
            "extra local spin/preferred-frame/contact effects",
            "needs coefficient map to PPN, R10, clocks, spin tests",
        ),
        (
            "NFC4184_4_curvature_squares",
            "R^AB wedge star R_AB, R^2, Ricci^2",
            "EFT_residual_if_IR_suppressed",
            "higher-derivative short-range/cosmology corrections",
            "needs mass scale or alpha(lambda) bound",
        ),
        (
            "NFC4184_5_disformal_second_metric",
            "matter or EM Hodge owner not equal to g_obs",
            "forbidden_or_explicit_residual",
            "WEP, clock, EM propagation, Poynting source leak",
            "must be zero by same-coframe clause or bounded",
        ),
        (
            "NFC4184_6_memory_couplings",
            "Gamma_mem times R/T/source invariants",
            "local_residual_unless_screened",
            "MTS-specific memory hair in local systems",
            "needs local screening law or sourced bound",
        ),
        (
            "NFC4184_7_boundary_topological",
            "Euler, Pontryagin, GHY/Hamiltonian charges",
            "allowed_if_fixed_exact_or_routed",
            "does not alter local bulk equations when properly routed",
            "non-routed edge charge reopens local source residual",
        ),
    ]
    return [
        {
            **common(),
            "classification_id": classification_id,
            "term_family": term,
            "selector_verdict": verdict,
            "physical_meaning": meaning,
            "gate_or_residual": gate,
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
        for classification_id, term, verdict, meaning, gate in rows
    ]


def theorem_chain_rows() -> List[Dict[str, str]]:
    rows = [
        (
            "TH4184_0_variables",
            "A_MF gives first-order Cartan variables",
            "e^A=D_omega X^A+B^A and g_obs=eta_AB e^A e^B are parent-candidate variables",
            "conditional_on_A_MF",
        ),
        (
            "TH4184_1_classification",
            "IR covariant four-form classification",
            "with local parity-even two-derivative bulk order, the unsuppressed geometry term linear in curvature is EC/Palatini plus vacuum term",
            "conditional_selector_theorem",
        ),
        (
            "TH4184_2_extras",
            "extra A_MF-invariant terms",
            "torsion squares, curvature squares, disformal/second-metric, memory couplings, and unrouted boundary charges are not silent by A_MF alone",
            "residual_ledger_required",
        ),
        (
            "TH4184_3_reduction",
            "EC/Palatini to EH",
            "if torsion/nonmetricity are algebraic and zero/bounded in spinless compact branch, S_EC reduces to S_EH[g_obs] plus routed boundary",
            "conditional_reduction",
        ),
        (
            "TH4184_4_newton",
            "Newton coefficient",
            "with the calibrated source law, G_cal=c^4 kappa_eff/(8*pi) and nabla^2 Phi_N=4*pi G_cal rho_H",
            "structural_not_numeric_prediction",
        ),
        (
            "TH4184_5_limit",
            "selector ownership",
            "the selector assumptions are not yet fully parent-derived by the corpus, so this is not public local GR",
            "public_claim_blocked",
        ),
    ]
    return [
        {
            **common(),
            "chain_id": chain_id,
            "step": step,
            "statement": statement,
            "status": status,
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
        for chain_id, step, statement, status in rows
    ]


def residual_bound_rows() -> List[Dict[str, str]]:
    rows = [
        (
            "RB4184_0_cT",
            "torsion-square coefficient c_T",
            "PPN preferred-frame, spin coupling, R10/contact force",
            "derive c_T=0/heavy from parent or fit upper bound",
            "valid_for_claim=false_until_numeric_or_parent_source",
        ),
        (
            "RB4184_1_cR2",
            "curvature-square coefficient c_R2 or mass M_R",
            "Yukawa/short-range gravity, orbital precession, cosmology",
            "source EFT scale or R10/orbital alpha(lambda) bound",
            "valid_for_claim=false_until_numeric_or_parent_source",
        ),
        (
            "RB4184_2_cD",
            "disformal/second metric coefficient c_D",
            "WEP, clocks, EM propagation, Poynting stress",
            "same-coframe proof or Eotvos/clock/EM bound",
            "valid_for_claim=false_until_zero_or_bound",
        ),
        (
            "RB4184_3_cGamma",
            "local memory coupling c_Gamma",
            "PPN, clocks, R10, local-G variation",
            "derive local screening/silence or build sourced bound",
            "valid_for_claim=false_until_zero_or_bound",
        ),
        (
            "RB4184_4_cBdy",
            "unrouted boundary/edge charge coefficient c_bdy",
            "Hamiltonian mass leakage, radiation/transition current",
            "fixed boundary condition, routed charge, or flux bound",
            "valid_for_claim=false_until_boundary_route_verified",
        ),
        (
            "RB4184_5_deltaKappa",
            "source-coupling drift delta_kappa",
            "Newton coefficient, orbital GM, clock/local G variation",
            "parent kappa lock or measured-G envelope",
            "numeric_G_not_predicted",
        ),
    ]
    return [
        {
            **common(),
            "residual_id": residual_id,
            "coefficient": coefficient,
            "test_arena": arena,
            "next_required_evidence": evidence,
            "status": status,
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
        for residual_id, coefficient, arena, evidence, status in rows
    ]


def decision_rows() -> List[Dict[str, str]]:
    return [
        {
            **common(),
            "decision": DECISION,
            "conditional_Palatini_IR_selector_theorem_written": "True",
            "selector_assumptions_parent_derived": "False",
            "EC_Palatini_selected_if_selector_assumptions_hold": "True",
            "extra_invariant_terms_classified": "True",
            "residual_EFT_bound_ledger_active": "True",
            "EC_to_EH_reduction_conditional_on_torsion_silence": "True",
            "public_local_GR_claim_allowed": "False",
            "numeric_G_predicted": "False",
            "meaning": (
                "A_MF plus explicit IR selector assumptions can isolate the EC/Palatini principal block, "
                "but the selector assumptions themselves remain parent debts and all excluded terms become residual bounds."
            ),
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
    ]


def firewall_rows() -> List[Dict[str, str]]:
    rows = [
        (
            "FW4184_0_selector",
            "A_MF alone selects Einstein-Hilbert.",
            "A_MF plus extra IR selector assumptions conditionally selects EC/Palatini.",
        ),
        (
            "FW4184_1_public_GR",
            "MTS now publicly derives local GR.",
            "This is a private conditional selector theorem; parent derivation and residual bounds remain open.",
        ),
        (
            "FW4184_2_extras",
            "Torsion/curvature/memory/disformal terms are zero automatically.",
            "They are zero only if parent-derived, symmetry-forbidden, heavy, screened, or empirically bounded.",
        ),
        (
            "FW4184_3_G",
            "The numerical value of Newton's constant is predicted.",
            "Only the structural relation G_cal=c^4 kappa_eff/(8*pi) is retained; numeric G remains calibrated.",
        ),
        (
            "FW4184_4_bound_rows",
            "Residual bound rows are evidence of passing local tests.",
            "They are placeholders/contracts until numeric/source-backed bounds are inserted.",
        ),
    ]
    return [
        {
            **common(),
            "firewall_id": firewall_id,
            "forbidden_language": forbidden,
            "safe_language": safe,
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
        for firewall_id, forbidden, safe in rows
    ]


def status_rows(claim_action: str, packet_action: str, spine_action: str) -> List[Dict[str, str]]:
    return [
        {
            **common(),
            "result": DECISION,
            "source_sweep_complete": "True",
            "conditional_Palatini_IR_selector_theorem_written": "True",
            "selector_assumptions_parent_derived": "False",
            "EC_Palatini_selected_if_selector_assumptions_hold": "True",
            "extra_invariant_terms_classified": "True",
            "residual_EFT_bound_ledger_active": "True",
            "public_local_GR_claim_allowed": "False",
            "numeric_G_predicted": "False",
            "formal_200_written": "True",
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
            "why": (
                "4184 isolates the Palatini principal block only under selector assumptions. "
                "The next useful move is to attach coefficients and arenas to every excluded invariant term, "
                "then either derive parent zeros/mass scales or source numeric bounds."
            ),
            "route_A": "derive parent scale laws or zeros for c_T, c_R2, c_D, c_Gamma, c_bdy, and delta_kappa",
            "route_B": "build source-backed local-test bound rows for each coefficient using PPN, R10, WEP, clocks, orbital, and EM propagation arenas",
            "public_claim_policy": "no public local-GR claim until selector assumptions and residual coefficients are parent-derived or bounded",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
    ]


def output_paths() -> Dict[str, Path]:
    names = [
        "P8_Y5_R2FR_4184_SOURCE_REGISTER",
        "P8_Y5_R2FR_4184_IR_SELECTOR_AXIOM_SET",
        "P8_Y5_R2FR_4184_NORMAL_FORM_CLASSIFICATION",
        "P8_Y5_R2FR_4184_PALATINI_REDUCTION_THEOREM_CHAIN",
        "P8_Y5_R2FR_4184_RESIDUAL_EFT_BOUND_LEDGER",
        "P8_Y5_R2FR_4184_BRANCH_DECISION",
        "P8_Y5_R2FR_4184_CLAIM_FIREWALL",
        "P8_Y5_R2FR_4184_STATUS",
        "P8_Y5_R2FR_4184_NEXT_TARGET",
    ]
    return {name: SOURCE_DIR / f"{name}.csv" for name in names}


def write_formal_200() -> None:
    text = f"""# 200 - PPC4161 Palatini IR Normal-Form Selector Under A_MF

Marker: `{SPINE_MARKER}`
Branch: `{BRANCH_ID}`
Decision: `{DECISION}`

## Claim Status

Private conditional theorem. This does not say MTS has publicly derived local GR. It says that if `A_MF` is adopted and a specific IR selector is parent-owned, the Einstein-Cartan/Palatini principal block is the surviving unsuppressed local geometry term. Everything excluded becomes an explicit residual coefficient.

## Selector

The selector is:

```text
A_MF
+ local covariant 4-form action
+ leading low-energy/two-derivative order
+ no extra unscreened light modes
+ same observed coframe for matter and Maxwell-Hodge
+ parity-even classical local gravity, or parity-odd pieces topological/bounded
+ fixed/exact/Hamiltonian-routed boundary terms
```

Under this selector, the local bulk geometry grammar is built from:

```text
e^A, omega^AB, R^AB[omega], T^A, parent scalar invariants, and covariant derivatives.
```

## Conditional Normal-Form Result

At leading parity-even local order, the selected geometry principal block is:

```text
S_EC = (4 kappa_eff)^-1 int epsilon_ABCD e^A wedge e^B wedge R^CD[omega]
       - (Lambda_eff / 12 kappa_eff) int epsilon_ABCD e^A wedge e^B wedge e^C wedge e^D.
```

If torsion/nonmetricity are algebraic and zero or bounded in the compact spinless local branch:

```text
S_EC[e, omega; kappa_eff] -> S_EH[g_obs; kappa_eff] + routed boundary.
```

Together with the calibrated source law:

```text
G_cal = c^4 kappa_eff/(8*pi),
nabla^2 Phi_N = 4*pi G_cal rho_H.
```

This is a structural Newton/GR reduction, not a numerical prediction of `G`.

## Residual Terms

The selector does not let us erase extra terms by hand. It classifies them:

- torsion squares -> coefficient `c_T`;
- curvature squares -> coefficient or mass scale `c_R2/M_R`;
- second metric/disformal matter owner -> coefficient `c_D`;
- local memory couplings -> coefficient `c_Gamma`;
- unrouted boundary/edge charge -> coefficient `c_bdy`;
- source-coupling drift -> `delta_kappa`.

Each coefficient must be parent-zero, symmetry-forbidden, heavy/screened, or source-backed bounded.

## Verdict

```text
conditional_Palatini_IR_selector_theorem_written = true
selector_assumptions_parent_derived = false
EC_Palatini_selected_if_selector_assumptions_hold = true
residual_EFT_bound_ledger_active = true
public_local_GR_claim_allowed = false
```

## Next Target

`{NEXT_TARGET}`
"""
    FORMAL_200_PATH.write_text(text, encoding="utf-8")


def write_doc() -> None:
    text = f"""# 4184 - Y5 R2FR Palatini IR Normal Form Selector Under A_MF Or Residual EFT Bound

Branch: `{BRANCH_ID}`
Decision: `{DECISION}`

## Result

4184 writes the conditional Palatini selector. The useful result is:

```text
A_MF + local covariant 4-form + two-derivative IR order + no extra light modes
+ same-coframe matter/EM + routed boundary
=> EC/Palatini principal block, plus vacuum term, with all other invariants demoted to residual coefficients.
```

## Honest Limit

The selector assumptions are not yet fully parent-derived. Therefore this is still a private conditional theorem, not public local GR.

The key advance is that the excluded terms are no longer vague problems. They are a concrete residual coefficient ledger: `c_T`, `c_R2`, `c_D`, `c_Gamma`, `c_bdy`, and `delta_kappa`.

## Next Target

`{NEXT_TARGET}`
"""
    DOC_PATH.write_text(text, encoding="utf-8")


def ensure_claim_row() -> str:
    rows = parse_csv(CLAIMS_PATH)
    if any(row.get("claim_id") == CLAIM_ID for row in rows):
        return "already_present"
    rows.append(
        {
            "claim_id": CLAIM_ID,
            "domain": "local_gravity",
            "claim": (
                "Under A_MF plus explicit IR selector assumptions, the EC/Palatini principal block is conditionally selected, "
                "but the selector assumptions are not yet parent-derived and excluded invariants remain residual coefficients"
            ),
            "current_evidence": (
                "formalization-workbench/200-PPC4161-Palatini-IR-normal-form-selector-under-AMF.md records the selector clauses, "
                "normal-form classification, EC-to-EH conditional reduction, calibrated source-coupling link, residual EFT bound ledger, and claim firewall"
            ),
            "status": "conditional_Palatini_IR_selector_nonclaim_selector_assumptions_not_parent_derived_residual_EFT_ledger_active",
            "next_test": "Derive parent zeros/mass scales for residual coefficients or source-backed PPN/R10/WEP/clock/orbital/EM bounds",
            "key_risk": (
                "The selector isolates the GR principal block only if its assumptions are adopted; "
                "torsion, curvature-squared, disformal, memory, boundary, and kappa-drift residuals remain open until bounded or derived"
            ),
        }
    )
    write_csv(CLAIMS_PATH, rows)
    return "added"


def ensure_packet_180_addendum() -> str:
    text = read_text(PACKET_180_PATH)
    if PACKET_MARKER in text:
        return "already_present"
    addendum = f"""

## Post-Checkpoint 4184 Palatini IR Normal-Form Selector

Marker: `{PACKET_MARKER}`

`post-checkpoint-work/4184-Y5-R2FR-Palatini-IR-normal-form-selector-under-AMF-or-residual-EFT-bound.md` writes the conditional IR selector:

```text
A_MF + locality + two-derivative IR order + no extra light modes
+ same-coframe matter/EM + routed boundary
=> EC/Palatini principal block conditionally selected.
```

It also keeps the firewall:

```text
selector_assumptions_parent_derived = false
residual_EFT_bound_ledger_active = true
public_local_GR_claim_allowed = false
numeric_G_predicted = false
```
"""
    PACKET_180_PATH.write_text(text.rstrip() + addendum, encoding="utf-8")
    return "added"


def ensure_spine_section() -> str:
    text = read_text(SPINE_PATH)
    if SPINE_MARKER in text:
        return "already_present"
    section = f"""

## PPC4161 Palatini IR Normal-Form Selector

Marker: `{SPINE_MARKER}`

Claim register row: `{CLAIM_ID}`

4184 conditionally selects the EC/Palatini principal block under `A_MF` plus an explicit IR selector: locality, low derivative order, no extra unscreened light modes, same-coframe matter/EM, and routed boundary terms. The selector assumptions remain parent debts, and excluded terms become residual coefficients rather than silent zeros.

Next target:

`{NEXT_TARGET}`
"""
    SPINE_PATH.write_text(text.rstrip() + section, encoding="utf-8")
    return "added"


def validation_rows(
    rows_by_name: Dict[str, List[Dict[str, str]]],
    claim_action: str,
    packet_action: str,
    spine_action: str,
) -> List[Dict[str, str]]:
    paths = output_paths()
    source_ok = all(
        row["exists"] == "True" and row["required_text_found"] == "True"
        for row in rows_by_name["P8_Y5_R2FR_4184_SOURCE_REGISTER"]
    )
    decision = rows_by_name["P8_Y5_R2FR_4184_BRANCH_DECISION"][0]
    status = rows_by_name["P8_Y5_R2FR_4184_STATUS"][0]
    all_generated_rows = [
        row
        for rows in rows_by_name.values()
        for row in rows
    ]
    bad_claim_rows = [
        row
        for row in all_generated_rows
        if row.get("claim_allowed") != "False" or row.get("valid_for_claim") != "False"
    ]
    checks = [
        ("VAL4184_0_sources", "all cited sources exist and contain required text", source_ok, ""),
        ("VAL4184_1_selector", "selector axiom set contains IR order clause", any(row["selector_id"] == "SEL4184_2_IR_order" for row in rows_by_name["P8_Y5_R2FR_4184_IR_SELECTOR_AXIOM_SET"]), ""),
        ("VAL4184_2_palatini", "Palatini selected row exists", any(row["selector_verdict"] == "selected_if_all_selector_clauses_hold" for row in rows_by_name["P8_Y5_R2FR_4184_NORMAL_FORM_CLASSIFICATION"]), ""),
        ("VAL4184_3_residuals", "residual EFT ledger includes memory coefficient", any(row["coefficient"] == "local memory coupling c_Gamma" for row in rows_by_name["P8_Y5_R2FR_4184_RESIDUAL_EFT_BOUND_LEDGER"]), ""),
        ("VAL4184_4_decision", "decision keeps selector assumptions not parent-derived", decision["selector_assumptions_parent_derived"] == "False", str(decision)),
        ("VAL4184_5_public_claim", "public local-GR claim remains false", status["public_local_GR_claim_allowed"] == "False", str(status)),
        ("VAL4184_6_numeric_G", "numeric G remains unpredicted", status["numeric_G_predicted"] == "False", str(status)),
        ("VAL4184_7_formal_200", "formal 200 exists and has marker", FORMAL_200_PATH.exists() and SPINE_MARKER in read_text(FORMAL_200_PATH), str(FORMAL_200_PATH)),
        ("VAL4184_8_doc", "4184 doc exists and has decision", DOC_PATH.exists() and DECISION in read_text(DOC_PATH), str(DOC_PATH)),
        ("VAL4184_9_claim_row", "claim register contains L-025", any(row.get("claim_id") == CLAIM_ID for row in parse_csv(CLAIMS_PATH)), claim_action),
        ("VAL4184_10_packet_180", "packet 180 addendum marker present", PACKET_MARKER in read_text(PACKET_180_PATH), packet_action),
        ("VAL4184_11_spine", "spine marker present", SPINE_MARKER in read_text(SPINE_PATH), spine_action),
        ("VAL4184_12_next", "next target recorded", rows_by_name["P8_Y5_R2FR_4184_NEXT_TARGET"][0]["next_target"] == NEXT_TARGET, NEXT_TARGET),
        ("VAL4184_13_output_paths", "all declared output CSVs exist", all(path.exists() for path in paths.values()), str(paths)),
        ("VAL4184_14_no_claim_rows", "all generated rows keep claim_allowed/valid_for_claim false", not bad_claim_rows, str(bad_claim_rows)),
    ]
    validation = [
        {
            **common(),
            "check_id": check_id,
            "description": description,
            "passed": str(bool(passed)),
            "details": details,
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
        for check_id, description, passed, details in checks
    ]
    py_compile.compile(str(SCRIPT_PATH), doraise=True)
    pycache = SCRIPT_PATH.parent / "__pycache__"
    if pycache.exists():
        shutil.rmtree(pycache)
    validation.append(
        {
            **common(),
            "check_id": "VAL4184_15_compile",
            "description": "generator compiles and pycache is removed",
            "passed": "True",
            "details": "compiled",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
    )
    return validation


def main() -> None:
    write_formal_200()
    write_doc()
    claim_action = ensure_claim_row()
    packet_action = ensure_packet_180_addendum()
    spine_action = ensure_spine_section()

    rows_by_name = {
        "P8_Y5_R2FR_4184_SOURCE_REGISTER": source_rows(),
        "P8_Y5_R2FR_4184_IR_SELECTOR_AXIOM_SET": selector_axiom_rows(),
        "P8_Y5_R2FR_4184_NORMAL_FORM_CLASSIFICATION": normal_form_classification_rows(),
        "P8_Y5_R2FR_4184_PALATINI_REDUCTION_THEOREM_CHAIN": theorem_chain_rows(),
        "P8_Y5_R2FR_4184_RESIDUAL_EFT_BOUND_LEDGER": residual_bound_rows(),
        "P8_Y5_R2FR_4184_BRANCH_DECISION": decision_rows(),
        "P8_Y5_R2FR_4184_CLAIM_FIREWALL": firewall_rows(),
        "P8_Y5_R2FR_4184_STATUS": status_rows(claim_action, packet_action, spine_action),
        "P8_Y5_R2FR_4184_NEXT_TARGET": next_rows(),
    }

    for name, path in output_paths().items():
        write_csv(path, rows_by_name[name])

    validation_path = SOURCE_DIR / "P8_Y5_BRR545_4184_VALIDATION.csv"
    write_csv(validation_path, validation_rows(rows_by_name, claim_action, packet_action, spine_action))

    validation = parse_csv(validation_path)
    failed = [row for row in validation if row.get("passed") != "True"]
    if failed:
        raise RuntimeError(f"4184 validation failed: {failed}")

    print(f"{CHECKPOINT} generated")
    print(f"doc={DOC_PATH}")
    print(f"formal={FORMAL_200_PATH}")
    print(f"validation={validation_path}")
    print(f"rows={len(validation)} validation checks")


if __name__ == "__main__":
    main()

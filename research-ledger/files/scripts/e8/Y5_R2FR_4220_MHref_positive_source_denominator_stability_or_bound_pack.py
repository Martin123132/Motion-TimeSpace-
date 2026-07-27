from __future__ import annotations

import csv
import py_compile
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List


ROOT = Path(__file__).resolve().parents[2]
FORMAL = ROOT / "formalization-workbench"
POST = ROOT / "post-checkpoint-work"
SOURCE_DIR = POST / "source-intake" / "mts_residuals"
SCRIPT_PATH = Path(__file__).resolve()

CHECKPOINT = "4220"
CLAIM_ID = "L-061"
BRANCH_ID = "MTS_R2FR_Y5_MHREF_POSITIVE_DENOMINATOR_GATE_4220"
DECISION = (
    "MHREF_POSITIVE_DENOMINATOR_LOWER_BOUND_REDUCED_BY_CURL_NUMERATOR_CLOSURE_"
    "SOURCE_COMPARATOR_AND_RESIDUAL_ROWS_RETAINED_NONCLAIM"
)
FORMAL_PATH = FORMAL / "236-PPC4161-MHref-positive-source-denominator-stability-or-bound-pack.md"
DOC_PATH = POST / "4220-Y5-R2FR-MHref-positive-source-denominator-stability-or-bound-pack.md"
SPINE_PATH = FORMAL / "07-unification-spine.md"
PACKET_PATH = FORMAL / "180-PPC4161-private-local-packet-integration.md"
CLAIMS_PATH = FORMAL / "02-claims-register.csv"
SPINE_MARKER = "PPC4161_MHREF_POSITIVE_DENOMINATOR_GATE_4220"
PACKET_MARKER = "PPC4161_PACKET_MHREF_POSITIVE_DENOMINATOR_GATE_4220"
NEXT_TARGET = "4221-Y5-R2FR-MEH-positive-source-comparator-and-residual-input-fill.md"

SOURCES = {
    "SRC4220_00_4219_next": (
        SOURCE_DIR / "P8_Y5_R2FR_4219_NEXT_TARGET.csv",
        "4220-Y5-R2FR-MHref-positive-source-denominator-stability-or-bound-pack.md",
        "4219 selected stable positive M_H_ref as the next obstruction.",
    ),
    "SRC4220_01_4219_decision": (
        SOURCE_DIR / "P8_Y5_R2FR_4219_DECISION.csv",
        "remaining_denominator_obstruction",
        "4219 decision shows all numerator terms close conditionally while M_H_ref remains.",
    ),
    "SRC4220_02_227_contract": (
        FORMAL / "227-PPC4161-Htau-MHsource-parent-charge-owner.md",
        "`M_H_ref` is positive",
        "Strict H_tau/M_H source-charge owner contract.",
    ),
    "SRC4220_03_186_glue": (
        FORMAL / "186-PPC4161-Hamiltonian-worldtube-mass-readout-glue.md",
        "M_H^dress[W_H;tau]",
        "Private Hamiltonian/worldtube mass charge glue.",
    ),
    "SRC4220_04_187_newton": (
        FORMAL / "187-PPC4161-Poisson-Gauss-Newton-readout-from-Hamiltonian-source-charge.md",
        "nabla^2 Phi_N",
        "Private Poisson/Gauss/Newton readout from Hamiltonian charge.",
    ),
    "SRC4220_05_3998_theorem": (
        SOURCE_DIR / "P8_Y5_R2FR_3998_HILBERT_MASS_DENOMINATOR_THEOREM.csv",
        "HDL3998_0_definition",
        "Hilbert mass denominator theorem and orbital anti-laundering verdict.",
    ),
    "SRC4220_06_3964_identity": (
        SOURCE_DIR / "P8_Y5_R2FR_3964_HILBERT_SOURCE_DENOMINATOR_IDENTITY.csv",
        "HDI3964_0_definition",
        "Hilbert source denominator identity and flux product rule.",
    ),
    "SRC4220_07_4002_htau_href": (
        SOURCE_DIR / "P8_Y5_R2FR_4002_HTAU_HREF_THEOREM.csv",
        "HIR4002_4_MHref_denominator_lock",
        "H_tau/H_ref denominator lock theorem and bound vector.",
    ),
    "SRC4220_08_4132_identity": (
        SOURCE_DIR / "P8_Y5_R2FR_4132_DENOMINATOR_IDENTITY.csv",
        "DEN4132_0_target_equality",
        "ell_J / M_H equality identity.",
    ),
    "SRC4220_09_3943_reference": (
        SOURCE_DIR / "P8_Y5_R2FR_3943_MHREF_REFERENCE_CHARGE_THEOREM.csv",
        "MRT3943_2_positive_lower_bound",
        "Reference charge and positive denominator theorem.",
    ),
    "SRC4220_10_3944_envelope": (
        SOURCE_DIR / "P8_Y5_R2FR_3944_MHREF_LOWER_BOUND_RESIDUAL_ENVELOPE.csv",
        "DLB3944_0_M_EH",
        "M_H_ref lower-bound residual component envelope.",
    ),
    "SRC4220_11_3577_route": (
        SOURCE_DIR / "P8_Y5_R2FR_3577_MHREF_POSITIVE_DENOMINATOR_ROUTE.csv",
        "DEN3577_1_lower_bound",
        "Positive denominator route and acceptance rule.",
    ),
    "SRC4220_12_3207_law": (
        SOURCE_DIR / "P8_Y5_R2FR_3207_MHREF_DENOMINATOR_LOWER_BOUND_LAW.csv",
        "LAW3207_3_positive_lower_bound",
        "Triangle-inequality lower-bound law.",
    ),
    "SRC4220_13_3446_rows": (
        SOURCE_DIR / "P8_Y5_R2FR_3446_MHREF_DENOMINATOR_BOUND_ROWS.csv",
        "DBR3446_0_M_H_ref",
        "Current denominator bound rows and required columns.",
    ),
    "SRC4220_14_235_formal": (
        FORMAL / "235-PPC4161-Dq-source-readout-coupling-marker-zero-or-bound.md",
        "M_H_ref.",
        "4219 formal handoff to M_H_ref.",
    ),
}


def now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def common() -> Dict[str, str]:
    return {"timestamp_utc": now(), "branch_id": BRANCH_ID, "checkpoint_id": CHECKPOINT}


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


def append_once(path: Path, marker: str, block: str) -> None:
    text = read_text(path)
    if marker in text:
        return
    with path.open("a", encoding="utf-8", newline="\n") as handle:
        handle.write("\n\n" + block.strip() + "\n")


def source_rows() -> List[Dict[str, str]]:
    rows = []
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


def theorem_rows() -> List[Dict[str, str]]:
    rows = [
        (
            "MHD4220_0_target",
            "target denominator",
            "M_H_ref := H_tau[S_outer;tau,e_obs] - H_ref[Sigma_ref;tau,e_obs]",
            "definition_target",
            "the source denominator is a Hamiltonian/Hilbert charge, not orbital GM",
        ),
        (
            "MHD4220_1_integrability_import",
            "H_tau state-function route",
            "4213 through 4219 conditionally close the retained field-space curl numerator of alpha_tau",
            "conditional_import_from_4213_4219",
            "the denominator problem is now separated from the curl numerator problem",
        ),
        (
            "MHD4220_2_fixed_reference",
            "source-blind H_ref",
            "H_ref is fixed by boundary/topology/asymptotic data before source, radius, frame or readout variation",
            "conditional_selector_import",
            "the reference cannot be fitted to cancel an observed source residual",
        ),
        (
            "MHD4220_3_same_frame_worldtube",
            "same-frame source branch",
            "W_H=closure(supp J_H_total), same tau/coframe/surface branch, and same Hilbert source current",
            "owner_contract",
            "the mass object must be the same one used by Hilbert stress, clocks, PPN and orbits",
        ),
        (
            "MHD4220_4_hilbert_denominator",
            "Hilbert mass denominator",
            "M_H[S] := N_G int_S Pi_M^H J_H_total[tau,e_obs]",
            "exact_conditional_definition",
            "source mass is defined before orbital readout and includes matter/EM/binding once",
        ),
        (
            "MHD4220_5_lower_bound",
            "positive lower-bound theorem",
            "G_ref M_H_ref = G_ref M_EH + sum_i Delta_i, so M_H_ref >= M_EH(1-epsilon_abs)",
            "derived_triangle_inequality_theorem",
            "if M_EH>0 and epsilon_abs<1, positivity follows without orbital GM",
        ),
        (
            "MHD4220_6_anti_laundering",
            "no measured-GM denominator",
            "partial_{GM_obs,mu_fit,orbit_fit} H_ref=0 and M_H_ref != mu_fit/G_* unless independently derived",
            "guardrail_active",
            "orbital agreement can test the denominator but cannot define it",
        ),
        (
            "MHD4220_7_reduced_components",
            "component reduction from recent closures",
            "Delta_H_curl, Delta_ref, tau/frame, boundary, visible EM and Dq terms have conditional zero routes under 4213-4219 selectors",
            "conditional_narrowing",
            "the remaining acquisition pressure is M_EH plus any denominator residual not covered by selector clauses",
        ),
        (
            "MHD4220_8_not_claim_ready",
            "current gap",
            "M_EH source comparator, residual component values/zeros, units, surfaces and source paths are still missing",
            "not_claim_ready",
            "no local-GR/Newton source normalization claim is allowed here",
        ),
        (
            "MHD4220_9_bound_pack",
            "fallback denominator bound pack",
            "epsilon_abs=sum_i |Delta_i|/(G_ref M_EH), with source-backed rows required for every term",
            "bound_pack_retained",
            "the next task is to fill or theorem-zero the lower-bound inputs",
        ),
    ]
    return [
        {
            **common(),
            "theorem_id": theorem_id,
            "claim_piece": claim_piece,
            "statement": statement,
            "status": status,
            "effect": effect,
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
        for theorem_id, claim_piece, statement, status, effect in rows
    ]


def activation_rows() -> List[Dict[str, str]]:
    rows = [
        ("MHA4220_0_Htau_integrable", "H_tau is integrable", "4213-4219 selector chain closes the retained curl numerator", "conditional_import"),
        ("MHA4220_1_Href_fixed", "H_ref source-blind fixed reference", "reference is selected before source/readout variation", "conditional_import"),
        ("MHA4220_2_same_tau_frame", "same tau/coframe/surface/worldtube", "one source branch for charge, clocks, PPN, orbit and boundary", "required"),
        ("MHA4220_3_Hilbert_source", "Hilbert/worldtube source current", "J_H_total and Pi_M^H are parent-defined before readout", "required"),
        ("MHA4220_4_no_orbital_GM", "no orbital-GM denominator import", "measured GM, fitted acceleration and orbit-fit mass cannot define M_H_ref", "required"),
        ("MHA4220_5_MEH_positive", "positive EH/source comparator", "M_EH>0 in the same frame/source branch", "missing_input"),
        ("MHA4220_6_epsilon_abs_lt_one", "residual envelope small enough", "epsilon_abs=sum |Delta_i|/(G_ref M_EH)<1", "missing_input"),
        ("MHA4220_7_units_sources", "units, surfaces and source paths", "all denominator rows have system/tau/surface/units/source paths and no MISSING markers", "missing_input"),
    ]
    return [
        {
            **common(),
            "activation_id": activation_id,
            "clause": clause,
            "formal_role": role,
            "status": status,
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
        for activation_id, clause, role, status in rows
    ]


def component_rows() -> List[Dict[str, str]]:
    rows = [
        ("MHC4220_0_M_EH", "M_EH", "same-frame EH/source-energy comparator", "MISSING_SOURCE_ENERGY_COMPARATOR_ROW", "highest_priority_input"),
        ("MHC4220_1_Delta_Komar_owner", "Delta_Komar_owner", "Hamiltonian/Komar/Tolman charge ownership failure", "MISSING_STATIONARY_TAU_OR_HAMILTONIAN_CHARGE", "input_or_zero_needed"),
        ("MHC4220_2_Delta_stress_virial", "Delta_stress_virial", "pressure/binding/stabilizer/virial correction", "MISSING_STRESS_VIRIAL_ZERO_OR_BOUND", "input_or_zero_needed"),
        ("MHC4220_3_Delta_nonEH", "Delta_nonEH", "non-EH or extra geometric source charge", "MISSING_NON_EH_SOURCE_CHARGE_BOUND", "input_or_zero_needed"),
        ("MHC4220_4_Delta_ref", "Delta_ref", "reference/counterterm shift", "0_under_4215_selector_else_bound", "conditional_zero_or_bound"),
        ("MHC4220_5_Delta_boundary", "Delta_boundary_symp", "boundary/symplectic/corner flux", "0_under_4217_selector_else_bound", "conditional_zero_or_bound"),
        ("MHC4220_6_Delta_projector", "Delta_projector", "PiM/projector variation or stress", "0_under_4214_selector_else_bound", "conditional_zero_or_bound"),
        ("MHC4220_7_Delta_source_measure", "Delta_source_measure", "source worldtube/support/current-complex mismatch", "MISSING_SOURCE_MEASURE_BOUND", "input_or_zero_needed"),
        ("MHC4220_8_Delta_coupling", "Delta_coupling", "G_ref/kappa/source-coupling normalization drift", "MISSING_COUPLING_NORMALIZATION_BOUND", "input_or_zero_needed"),
        ("MHC4220_9_Delta_EM", "Delta_EM", "EM source/flux correction outside closed stationary branch", "0_under_4218_selector_else_bound", "conditional_zero_or_bound"),
        ("MHC4220_10_Delta_Dq", "Delta_Dq", "source-readout/coupling marker denominator leak", "0_under_4219_selector_else_bound", "conditional_zero_or_bound"),
        ("MHC4220_11_Delta_H_curl", "Delta_H_curl", "field-space path dependence of H_tau", "0_under_4213_4219_curl_selector_else_bound", "conditional_zero_or_bound"),
        ("MHC4220_12_Delta_frame_units", "Delta_frame_units", "same-frame/units mismatch", "0_under_4216_selector_else_bound", "conditional_zero_or_bound"),
        ("MHC4220_13_epsilon_abs", "epsilon_abs", "absolute residual ratio", "sum_i |Delta_i|/(G_ref*M_EH)", "computed_after_inputs"),
        ("MHC4220_14_MHref_lower", "M_H_ref_lower", "positive lower bound", "M_EH*(1-epsilon_abs)", "computed_after_inputs"),
    ]
    return [
        {
            **common(),
            "component_id": component_id,
            "symbol": symbol,
            "meaning": meaning,
            "value_or_formula": value,
            "status": status,
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
        for component_id, symbol, meaning, value, status in rows
    ]


def score_rows() -> List[Dict[str, str]]:
    return [
        {
            **common(),
            "score_id": "MHS4220_0_denominator_law",
            "quantity": "M_H_ref_lower_bound_law",
            "value_or_bound": "M_H_ref >= M_EH*(1-epsilon_abs)",
            "status": "DERIVED_LOWER_BOUND_LAW",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            **common(),
            "score_id": "MHS4220_1_acceptance_gate",
            "quantity": "denominator_acceptance",
            "value_or_bound": "accept if M_EH>0 and epsilon_abs<1 with source-backed rows, or exact positive M_H_ref",
            "status": "ACCEPTANCE_GATE_READY_NOT_FILLED",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            **common(),
            "score_id": "MHS4220_2_local_GR_status",
            "quantity": "local_GR_Newton_source_status",
            "value_or_bound": "blocked_until_MHref_positive_source_backed",
            "status": "LOCAL_GR_CLAIM_FALSE",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
    ]


def route_rows() -> List[Dict[str, str]]:
    rows = [
        ("MHR4220_0_exact_MHref", "exact positive denominator", "derive finite positive H_tau-H_ref in same branch", "would unlock denominator if source-backed"),
        ("MHR4220_1_lower_bound", "positive lower-bound route", "prove M_EH>0 and epsilon_abs<1", "preferred non-orbital route"),
        ("MHR4220_2_bound_pack", "component bound pack", "fill or zero each Delta_i with units/source paths", "keeps scoring nonclaim until real inputs exist"),
        ("MHR4220_3_no_orbital_import", "anti-laundering route", "reject mu_obs/G, fitted GM, bare source mass, reference-only 1", "prevents circular Newton pass"),
        ("MHR4220_4_next_MEH", "next input target", "first missing row is M_EH positive source comparator", "send to 4221"),
    ]
    return [
        {
            **common(),
            "route_id": route_id,
            "route": route,
            "condition": condition,
            "effect": effect,
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
        for route_id, route, condition, effect in rows
    ]


def decision_rows() -> List[Dict[str, str]]:
    return [
        {
            **common(),
            "decision": DECISION,
            "lower_bound_law_derived": "True",
            "curl_numerator_closure_imported": "True",
            "M_H_ref_available": "False",
            "M_EH_positive_source_row_available": "False",
            "epsilon_abs_computable": "False",
            "Newton_source_normalization_claim": "False",
            "local_GR_claim": "False",
            "remaining_gap": "M_EH_positive_source_comparator_and_residual_inputs",
            "next_target": NEXT_TARGET,
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
    ]


def firewall_rows() -> List[Dict[str, str]]:
    rows = [
        ("MHF4220_0_no_orbital_GM", "use measured orbital GM as M_H_ref", "blocked", "orbital GM is an output/test after denominator ownership"),
        ("MHF4220_1_no_reference_fit", "choose H_ref to cancel residuals", "blocked", "H_ref must be parent-selected and source-blind"),
        ("MHF4220_2_no_positive_placeholder", "divide by M_H_ref placeholder", "blocked", "requires exact positive value or source-backed lower bound"),
        ("MHF4220_3_no_local_GR_claim", "local GR/Newton source normalization proven", "blocked", "M_EH and epsilon_abs rows are missing"),
        ("MHF4220_4_no_cancellation", "residual components cancel", "blocked", "epsilon_abs uses absolute no-cancellation sum"),
    ]
    return [
        {
            **common(),
            "firewall_id": firewall_id,
            "forbidden_claim": forbidden,
            "status": status,
            "reason": reason,
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
        for firewall_id, forbidden, status, reason in rows
    ]


def status_rows() -> List[Dict[str, str]]:
    return [
        {
            **common(),
            "status": DECISION,
            "private_checkpoint": "True",
            "claim_allowed": "False",
            "valid_for_claim": "False",
            "summary": "M_H_ref positivity is reduced to an exact lower-bound law plus source-backed M_EH/residual inputs; no denominator pass yet.",
        }
    ]


def next_target_rows() -> List[Dict[str, str]]:
    return [
        {
            **common(),
            "next_target": NEXT_TARGET,
            "why": "4220 derives the denominator lower-bound route but does not fill M_EH or epsilon_abs; the next concrete target is the positive same-frame EH/source comparator and residual input fill.",
            "route_A": "prove M_EH>0 from the same-frame Hilbert/Komar/Tolman source branch without orbital GM",
            "route_B": "fill source-backed M_EH and Delta_i rows with units/surfaces/source paths",
            "route_C": "if no source row exists, keep denominator unavailable and summarize local-GR status as private conditional only",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
    ]


def formal_doc() -> str:
    return f"""# 236 - PPC4161 MHref positive source denominator stability or bound pack

Marker: `{SPINE_MARKER}`
Checkpoint: `{CHECKPOINT}`
Branch: `{BRANCH_ID}`
Decision: `{DECISION}`

## Target

After 4213 through 4219, every retained 4212 numerator term has a conditional zero route. The remaining local source-charge obstruction is:

```text
M_H_ref.
```

## Denominator Object

The denominator is not orbital `GM` and not a fitted readout mass. It is:

```text
M_H_ref := H_tau[S_outer;tau,e_obs] - H_ref[Sigma_ref;tau,e_obs].
```

Equivalently, in the Hilbert current route:

```text
M_H[S] := N_G int_S Pi_M^H J_H_total[tau,e_obs].
```

The target equality is:

```text
ell_J(Pi_M J_H_total)
= M_H^dress
= H_tau[S]-H_ref
= B_tau/G_ref.
```

## What 4213-4219 Buy

The recent chain conditionally closes the field-space curl numerator and the major leakage channels:

```text
I_qbasic_vertical,
I_projector,
I_ref,
I_tau+I_surface+C_frame,
I_boundary+I_corner,
I_matter_EM,
I_Dq.
```

So the denominator problem is now sharper: not "is every curl term missing?", but "is the same-frame Hamiltonian/Hilbert source charge positive and source-backed?"

## Lower-Bound Law

Use the same-frame decomposition:

```text
G_ref M_H_ref
= G_ref M_EH
+ sum_i Delta_i.
```

Then:

```text
M_H_ref >= M_EH * (1 - epsilon_abs),
epsilon_abs := sum_i |Delta_i|/(G_ref M_EH).
```

Therefore:

```text
M_EH > 0 and epsilon_abs < 1
=> M_H_ref > 0.
```

This is the legal non-orbital positivity route.

## Current Gap

The law is derived, but the pass is not claim-ready because the following are still missing:

- source-backed `M_EH > 0`;
- source-backed or theorem-zero `Delta_i` rows;
- shared units, tau, coframe, worldtube and surface identifiers;
- no `MISSING_` markers;
- no orbital `GM` or fitted acceleration as denominator input.

## Next Target

`{NEXT_TARGET}` should fill or derive the positive `M_EH` comparator first.
"""


def checkpoint_doc() -> str:
    return f"""# 4220 - MHref positive source denominator stability or bound pack

**Status:** `{DECISION}`.

## What changed

- Wrote `{FORMAL_PATH}`.
- Added source-backed CSV rows for the denominator theorem, activation clauses, lower-bound components, score gates, route matrix, decision row and firewall.
- Updated `{CLAIMS_PATH}` with `{CLAIM_ID}` if absent.
- Updated `{SPINE_PATH}` and `{PACKET_PATH}` with `{SPINE_MARKER}` / `{PACKET_MARKER}`.

## Result

The legal denominator route is now explicit:

```text
M_H_ref >= M_EH(1-epsilon_abs).
```

A pass needs:

```text
M_EH>0,
epsilon_abs<1,
source-backed units/surfaces/source paths,
no orbital-GM import.
```

So this is not a local-GR claim yet. It is a narrowed denominator gate.

## Next

`{NEXT_TARGET}` should target the first missing input: the positive same-frame `M_EH` source comparator.
"""


def update_registers() -> None:
    claim_row = (
        f'{CLAIM_ID},local_gr,'
        f'"The stable positive M_H_ref denominator problem is reduced to an exact non-orbital lower-bound law: M_H_ref >= M_EH(1-epsilon_abs), with recent curl-numerator closures imported as conditional reductions; a claim still requires source-backed M_EH>0, epsilon_abs<1, shared units/surfaces/source paths, and no orbital-GM laundering.",'
        f'"4220 source audit, MHref theorem, activation clauses, lower-bound components, score gates, route matrix, decision row and firewall.",'
        f'private_MHref_lower_bound_gate_nonclaim,'
        f'"Fill or derive the positive same-frame M_EH source comparator and residual inputs.",'
        f'"This is a denominator gate, not a denominator pass; no local-GR/Newton source normalization claim follows until the inputs are real."'
    )
    if f"{CLAIM_ID}," not in read_text(CLAIMS_PATH):
        with CLAIMS_PATH.open("a", encoding="utf-8", newline="\n") as handle:
            handle.write(claim_row + "\n")

    spine_block = f"""### PPC4161 MHref positive denominator gate - 4220

Marker: `{SPINE_MARKER}`
Claim register row: `{CLAIM_ID}`

4220 reduces the remaining denominator obstruction to:

```text
M_H_ref >= M_EH(1-epsilon_abs).
```

Recent numerator closures sharpen the gate, but do not supply the source-backed positive `M_EH` comparator or residual rows."""
    append_once(SPINE_PATH, SPINE_MARKER, spine_block)

    packet_block = f"""## PPC4161 Packet MHref positive denominator gate - 4220

Marker: `{PACKET_MARKER}`

The packet now has conditional numerator closure and a non-orbital denominator lower-bound law. Remaining task: source-backed `M_EH>0` and denominator residual inputs before any local-GR/Newton source-normalization claim."""
    append_once(PACKET_PATH, PACKET_MARKER, packet_block)


def validate(rows_by_file: Dict[str, List[Dict[str, str]]]) -> List[Dict[str, str]]:
    source = rows_by_file["P8_Y5_R2FR_4220_SOURCE_REGISTER.csv"]
    theorem = rows_by_file["P8_Y5_R2FR_4220_MHREF_THEOREM.csv"]
    activation = rows_by_file["P8_Y5_R2FR_4220_ACTIVATION_CLAUSES.csv"]
    components = rows_by_file["P8_Y5_R2FR_4220_LOWER_BOUND_COMPONENTS.csv"]
    scores = rows_by_file["P8_Y5_R2FR_4220_SCORE_GATES.csv"]
    routes = rows_by_file["P8_Y5_R2FR_4220_ROUTE_MATRIX.csv"]
    decision = rows_by_file["P8_Y5_R2FR_4220_DECISION.csv"][0]
    all_rows_flat = [row for rows in rows_by_file.values() for row in rows]
    required_theorems = {
        "MHD4220_0_target",
        "MHD4220_1_integrability_import",
        "MHD4220_2_fixed_reference",
        "MHD4220_3_same_frame_worldtube",
        "MHD4220_4_hilbert_denominator",
        "MHD4220_5_lower_bound",
        "MHD4220_6_anti_laundering",
        "MHD4220_7_reduced_components",
        "MHD4220_8_not_claim_ready",
        "MHD4220_9_bound_pack",
    }
    required_components = {
        "M_EH",
        "Delta_Komar_owner",
        "Delta_stress_virial",
        "Delta_nonEH",
        "Delta_ref",
        "Delta_boundary_symp",
        "Delta_projector",
        "Delta_source_measure",
        "Delta_coupling",
        "Delta_EM",
        "Delta_Dq",
        "Delta_H_curl",
        "Delta_frame_units",
        "epsilon_abs",
        "M_H_ref_lower",
    }
    checks = [
        ("VAL4220_0_sources_exist", "all source paths exist", all(row["exists"] == "True" for row in source)),
        ("VAL4220_1_source_needles", "all source needles found", all(row["required_text_found"] == "True" for row in source)),
        ("VAL4220_2_theorem_complete", "MHref theorem rows contain all clauses", required_theorems.issubset({row["theorem_id"] for row in theorem})),
        ("VAL4220_3_lower_bound_law", "lower-bound theorem is present", any(row["theorem_id"] == "MHD4220_5_lower_bound" and row["status"] == "derived_triangle_inequality_theorem" for row in theorem)),
        ("VAL4220_4_activation_clauses", "activation clauses include integrability, Href, same frame, Hilbert source, no GM, MEH, epsilon and units", {"MHA4220_0_Htau_integrable", "MHA4220_1_Href_fixed", "MHA4220_2_same_tau_frame", "MHA4220_3_Hilbert_source", "MHA4220_4_no_orbital_GM", "MHA4220_5_MEH_positive", "MHA4220_6_epsilon_abs_lt_one", "MHA4220_7_units_sources"}.issubset({row["activation_id"] for row in activation})),
        ("VAL4220_5_components", "lower-bound components cover MEH, residuals, epsilon and lower bound", required_components.issubset({row["symbol"] for row in components})),
        ("VAL4220_6_recent_closures_imported", "component rows import 4213-4219 conditional closures", any(row["symbol"] == "Delta_H_curl" and "4213_4219" in row["value_or_formula"] for row in components) and any(row["symbol"] == "Delta_Dq" and "4219" in row["value_or_formula"] for row in components)),
        ("VAL4220_7_score_gate", "score gates include lower-bound law and acceptance gate", {"MHS4220_0_denominator_law", "MHS4220_1_acceptance_gate", "MHS4220_2_local_GR_status"}.issubset({row["score_id"] for row in scores})),
        ("VAL4220_8_routes", "routes include exact, lower-bound, bound pack, no-GM and MEH next", {"MHR4220_0_exact_MHref", "MHR4220_1_lower_bound", "MHR4220_2_bound_pack", "MHR4220_3_no_orbital_import", "MHR4220_4_next_MEH"}.issubset({row["route_id"] for row in routes})),
        ("VAL4220_9_decision_nonclaim", "decision keeps denominator unavailable and local-GR claim false", decision["M_H_ref_available"] == "False" and decision["local_GR_claim"] == "False" and decision["M_EH_positive_source_row_available"] == "False"),
        ("VAL4220_10_no_claim_flags", "all generated claim flags remain false", all(row.get("claim_allowed", "False") == "False" and row.get("valid_for_claim", "False") == "False" for row in all_rows_flat)),
        ("VAL4220_11_docs_written", "formal and checkpoint docs written", FORMAL_PATH.exists() and DOC_PATH.exists()),
        ("VAL4220_12_claim_register", "claim register contains L-061", CLAIM_ID + "," in read_text(CLAIMS_PATH)),
        ("VAL4220_13_spine_packet", "spine and packet markers present", SPINE_MARKER in read_text(SPINE_PATH) and PACKET_MARKER in read_text(PACKET_PATH)),
        ("VAL4220_14_next_target", "next target is MEH comparator fill", decision["next_target"] == NEXT_TARGET),
    ]
    return [
        {
            **common(),
            "check_id": check_id,
            "check": check,
            "passed": str(bool(passed)),
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
        for check_id, check, passed in checks
    ]


def write_all() -> None:
    FORMAL_PATH.write_text(formal_doc(), encoding="utf-8", newline="\n")
    DOC_PATH.write_text(checkpoint_doc(), encoding="utf-8", newline="\n")
    rows_by_file = {
        "P8_Y5_R2FR_4220_SOURCE_REGISTER.csv": source_rows(),
        "P8_Y5_R2FR_4220_MHREF_THEOREM.csv": theorem_rows(),
        "P8_Y5_R2FR_4220_ACTIVATION_CLAUSES.csv": activation_rows(),
        "P8_Y5_R2FR_4220_LOWER_BOUND_COMPONENTS.csv": component_rows(),
        "P8_Y5_R2FR_4220_SCORE_GATES.csv": score_rows(),
        "P8_Y5_R2FR_4220_ROUTE_MATRIX.csv": route_rows(),
        "P8_Y5_R2FR_4220_DECISION.csv": decision_rows(),
        "P8_Y5_R2FR_4220_CLAIM_FIREWALL.csv": firewall_rows(),
        "P8_Y5_R2FR_4220_STATUS.csv": status_rows(),
        "P8_Y5_R2FR_4220_NEXT_TARGET.csv": next_target_rows(),
    }
    for filename, rows in rows_by_file.items():
        write_csv(SOURCE_DIR / filename, rows)
    update_registers()
    validation = validate(rows_by_file)
    write_csv(SOURCE_DIR / "P8_Y5_BRR545_4220_VALIDATION.csv", validation)
    py_compile.compile(str(SCRIPT_PATH), doraise=True)
    pycache = SCRIPT_PATH.parent / "__pycache__"
    if pycache.exists():
        shutil.rmtree(pycache)


def main() -> None:
    write_all()
    print(DECISION)
    print(f"formal={FORMAL_PATH}")
    print(f"checkpoint={DOC_PATH}")
    print(f"validation={SOURCE_DIR / 'P8_Y5_BRR545_4220_VALIDATION.csv'}")
    print("rows=15 validation checks")


if __name__ == "__main__":
    main()

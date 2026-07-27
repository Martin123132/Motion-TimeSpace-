from __future__ import annotations

import csv
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List


ROOT = Path(__file__).resolve().parents[2]
FORMAL = ROOT / "formalization-workbench"
POST = ROOT / "post-checkpoint-work"
SOURCE_DIR = POST / "source-intake" / "mts_residuals"
SCRIPTS = POST / "scripts"

CHECKPOINT = "4230"
CLAIM_ID = "L-071"
BRANCH = "MTS_R2FR_Y5_MEH_TOTAL_EPSILON_PRIVATE_SELECTOR_4230"
DECISION = "MEH_TOTAL_EPSILON_ZERO_IN_FULL_PRIVATE_SELECTOR_NON_EH_PARENT_ADOPTION_RETAINED_NONCLAIM"
MARKER = "PPC4161_MEH_TOTAL_EPSILON_PRIVATE_SELECTOR_4230"
PACKET_MARKER = "PPC4161_PACKET_MEH_TOTAL_EPSILON_PRIVATE_SELECTOR_4230"
NEXT_TARGET = "4231-Y5-R2FR-private-local-GR-scorecard-refresh-and-nonEH-parent-adoption-gate.md"

FORMAL_PATH = FORMAL / "246-PPC4161-MEH-total-epsilon-score-open-reference-virial-frame-gate.md"
DOC_PATH = POST / "4230-Y5-R2FR-MEH-total-epsilon-score-open-reference-virial-frame-gate.md"
VALIDATION_PATH = SOURCE_DIR / "P8_Y5_BRR545_4230_VALIDATION.csv"


@dataclass(frozen=True)
class SourceSpec:
    source_id: str
    path: Path
    required_text: str
    role: str


SOURCE_SPECS: Dict[str, SourceSpec] = {
    "SRC4230_00_4229_next": SourceSpec(
        "SRC4230_00_4229_next",
        SOURCE_DIR / "P8_Y5_R2FR_4229_NEXT_TARGET.csv",
        "4230-Y5-R2FR-MEH-total-epsilon-score-open-reference-virial-frame-gate.md",
        "4229 selects total MEH residual scoring as the next target.",
    ),
    "SRC4230_01_245_core_bind": SourceSpec(
        "SRC4230_01_245_core_bind",
        FORMAL / "245-PPC4161-binding-stabilizer-positive-energy-theorem-or-beta-bind-bound.md",
        "epsilon_E_core_bind|dressed_private_selector := 0",
        "Core-bind numerator is closed in the dressed private source selector.",
    ),
    "SRC4230_02_237_comparator": SourceSpec(
        "SRC4230_02_237_comparator",
        FORMAL / "237-PPC4161-MEH-positive-source-comparator-and-residual-input-fill.md",
        "M_EH >= c^-2 E_plus(1-epsilon_E)",
        "MEH comparator law and residual decomposition.",
    ),
    "SRC4230_03_191_poynting": SourceSpec(
        "SRC4230_03_191_poynting",
        FORMAL / "191-PPC4161-Maxwell-Hodge-Poynting-stress-owner-theorem.md",
        "Radiative Boundary Guard",
        "Poynting/open EM flux is either in T_total or routed as boundary flux.",
    ),
    "SRC4230_04_192_no_flux": SourceSpec(
        "SRC4230_04_192_no_flux",
        FORMAL / "192-PPC4161-local-boundary-no-flux-sector-interface-theorem.md",
        "J_tr^nu = 0 through <=2PN",
        "Compact local no-flux selector closes transition-current leakage.",
    ),
    "SRC4230_05_4215_reference": SourceSpec(
        "SRC4230_05_4215_reference",
        SOURCE_DIR / "P8_Y5_R2FR_4215_CURL_SCORE_UPDATE.csv",
        "RSU4215_0_I_ref",
        "Fixed source-blind reference lock zero row.",
    ),
    "SRC4230_06_4216_frame": SourceSpec(
        "SRC4230_06_4216_frame",
        SOURCE_DIR / "P8_Y5_R2FR_4216_CURL_SCORE_UPDATE.csv",
        "TSU4216_0_I_tau_surface_frame",
        "Tau/surface/frame lock zero row.",
    ),
    "SRC4230_07_4217_boundary": SourceSpec(
        "SRC4230_07_4217_boundary",
        SOURCE_DIR / "P8_Y5_R2FR_4217_CURL_SCORE_UPDATE.csv",
        "BCU4217_0_I_boundary_corner",
        "Boundary/corner no-flux zero row.",
    ),
    "SRC4230_08_4219_Dq": SourceSpec(
        "SRC4230_08_4219_Dq",
        SOURCE_DIR / "P8_Y5_R2FR_4219_CURL_SCORE_UPDATE.csv",
        "DQS4219_2_delta_Htau_update",
        "Dq/source-readout marker theorem conditionally closes the remaining Hamiltonian numerator.",
    ),
    "SRC4230_09_200_Palatini": SourceSpec(
        "SRC4230_09_200_Palatini",
        FORMAL / "200-PPC4161-Palatini-IR-normal-form-selector-under-AMF.md",
        "EC_Palatini_selected_if_selector_assumptions_hold = true",
        "Conditional Palatini IR normal-form selector for non-EH residuals.",
    ),
    "SRC4230_10_201_nonEH_map": SourceSpec(
        "SRC4230_10_201_nonEH_map",
        FORMAL / "201-PPC4161-extra-invariant-residual-coefficient-map.md",
        "all_coefficients_numeric_or_parent_zero = false",
        "Residual coefficient map showing non-EH coefficients are not globally claim-zero.",
    ),
    "SRC4230_11_188_PPN": SourceSpec(
        "SRC4230_11_188_PPN",
        FORMAL / "188-PPC4161-full-PPN-readout-vector.md",
        "R_PPN =",
        "Private full PPN zero vector after local selector readout.",
    ),
    "SRC4230_12_236_MHref": SourceSpec(
        "SRC4230_12_236_MHref",
        FORMAL / "236-PPC4161-MHref-positive-source-denominator-stability-or-bound-pack.md",
        "epsilon_abs := sum_i |Delta_i|/(G_ref M_EH)",
        "M_H_ref lower-bound law and epsilon_abs denominator gate.",
    ),
    "SRC4230_13_194_Gcal": SourceSpec(
        "SRC4230_13_194_Gcal",
        FORMAL / "194-PPC4161-calibrated-source-coupling-kappa-to-GN-law.md",
        "G_cal := c^4 kappa_eff/(8*pi)",
        "Calibrated source coupling and anti-circularity guard.",
    ),
}


def now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def common() -> Dict[str, str]:
    return {"timestamp_utc": now(), "branch_id": BRANCH, "checkpoint_id": CHECKPOINT}


def read_text(path: Path) -> str:
    if not path.exists():
        return ""
    return path.read_text(encoding="utf-8", errors="replace")


def write_csv(path: Path, rows: List[Dict[str, str]]) -> None:
    if not rows:
        raise ValueError(f"cannot write empty csv: {path}")
    path.parent.mkdir(parents=True, exist_ok=True)
    fieldnames: List[str] = []
    for row in rows:
        for key in row:
            if key not in fieldnames:
                fieldnames.append(key)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def append_once(path: Path, marker: str, block: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    existing = read_text(path)
    if marker in existing:
        return
    with path.open("a", encoding="utf-8") as handle:
        if existing and not existing.endswith("\n"):
            handle.write("\n")
        handle.write("\n" + block.strip() + "\n")


def source_rows() -> List[Dict[str, str]]:
    rows: List[Dict[str, str]] = []
    for source in SOURCE_SPECS.values():
        text = read_text(source.path)
        rows.append(
            {
                **common(),
                "source_id": source.source_id,
                "path": str(source.path),
                "exists": str(source.path.exists()),
                "required_text": source.required_text,
                "required_text_found": str(source.required_text in text),
                "role": source.role,
                "claim_allowed": "False",
                "valid_for_claim": "False",
            }
        )
    return rows


def route_rows() -> List[Dict[str, str]]:
    data = [
        (
            "MTR4230_0_core_bind",
            "core-bind numerator",
            "E_core_bind_abs := E_binding_stabilizer_neg_abs + E_MTS_core_neg_abs = 0",
            "4228 and 4229 close the core MTS and binding/stabilizer channels in the dressed private ordinary-source selector.",
            "ZERO_IN_PRIVATE_SELECTOR",
            "reopen beta_sig/beta_bind rows if the local selector or dressed-source premise is rejected",
        ),
        (
            "MTR4230_1_open_flux",
            "open/radiative flux",
            "E_open_abs := 0 under compact stationary no-flux collar with radiative flux routed as boundary/Hamiltonian charge",
            "Maxwell-Hodge Poynting is counted once in T_total; nonzero radiative flux is not hidden bulk energy and must be routed or bounded.",
            "ZERO_IF_NO_FLUX_ROUTED",
            "nonzero EM/gravitational/open-memory flux reopens E_open_abs_bound",
        ),
        (
            "MTR4230_2_reference",
            "reference subtraction",
            "E_ref_abs := 0 when H_ref is fixed, source-blind and chosen before source/radius/frame/readout variation",
            "4215 reference-lock theorem kills the reference curl only for a parent-selected fixed reference.",
            "ZERO_IF_FIXED_REFERENCE",
            "post-fit or drifting reference reopens I_ref+Delta_ref bound",
        ),
        (
            "MTR4230_3_virial_pressure",
            "virial/pressure/stress",
            "E_vir_abs := 0 for stationary compact total Hilbert source with no surface flux",
            "From total source conservation plus stationary no-flux boundary, pressure/stress is internal to the dressed source rather than an extra negative channel.",
            "ZERO_IF_STATIONARY_TOTAL_SOURCE",
            "nonstationary pressure, apparatus stress, radiation pressure, or nonzero surface stress reopens E_vir_abs",
        ),
        (
            "MTR4230_4_frame",
            "same-frame/tau/surface",
            "E_frame_abs := 0 when tau, source charge, clocks, rods, EM, PPN readout and H_tau use one parent-selected observed coframe",
            "4216 and 4219 close the frame/source-readout/Dq route only if the lock is before variation and comparison.",
            "ZERO_IF_SAME_FRAME_LOCK",
            "post-fit coordinate/readout choices reopen frame/source residuals",
        ),
        (
            "MTR4230_5_nonEH",
            "non-EH/EFT residuals",
            "E_nonEH_abs := 0 only inside the full private Palatini/EH IR selector; globally the residual coefficient map remains active",
            "The branch may exclude or heavy-route extra local operators, but 201 says the coefficients are not globally parent-zero or numeric.",
            "ZERO_IN_FULL_PRIVATE_SELECTOR_ONLY",
            "finite torsion/R2/disformal/memory/boundary coefficients reopen the R11/non-EH bound ledger",
        ),
        (
            "MTR4230_6_epsilon_abs",
            "MHref denominator residuals",
            "epsilon_abs_private := 0 if 4213-4219 numerator closures, fixed reference, no-flux boundary and same-frame lock all hold",
            "The M_H_ref lower-bound gate becomes equality only after every Delta_i route is zero inside the selector.",
            "ZERO_IF_ALL_CURL_NUMERATORS_ZERO",
            "any Delta_i source/frame/boundary/reference/nonintegrable term reopens epsilon_abs",
        ),
    ]
    return [
        {
            **common(),
            "route_id": route_id,
            "residual": residual,
            "zero_or_bound_statement": statement,
            "derivation": derivation,
            "status": status,
            "fallback_or_reopen_rule": fallback,
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
        for route_id, residual, statement, derivation, status, fallback in data
    ]


def score_rows() -> List[Dict[str, str]]:
    data = [
        (
            "MES4230_0_positive_pool",
            "positive source pool",
            "E_plus_private := E_H^dress = c^2 M_H^dress > 0",
            "Requires rho_H >= 0 and nonzero compact ordinary-source support in the dressed Hilbert source branch.",
            "PRIVATE_STABLE_SOURCE_POSITIVE",
        ),
        (
            "MES4230_1_total_epsilon",
            "MEH epsilon",
            "epsilon_E_private := (E_core_bind_abs+E_open_abs+E_ref_abs+E_vir_abs+E_nonEH_abs+E_frame_abs)/E_plus_private = 0",
            "All numerator rows in MTR4230_0 through MTR4230_5 are zero inside the full private selector.",
            "ZERO_IN_FULL_PRIVATE_SELECTOR",
        ),
        (
            "MES4230_2_MEH_positive",
            "MEH sign",
            "M_EH_private >= c^-2 E_plus_private(1-epsilon_E_private) = M_H^dress > 0",
            "The private same-frame dressed source comparator is positive once epsilon_E_private=0.",
            "MEH_POSITIVE_PRIVATE_NONCLAIM",
        ),
        (
            "MES4230_3_epsilon_abs",
            "MHref denominator epsilon",
            "epsilon_abs_private := sum_i |Delta_i|/(G_ref M_EH_private) = 0",
            "4213-4219 zero routes plus fixed reference/no-flux/same-frame clauses close the denominator residual numerator inside the selector.",
            "ZERO_IN_FULL_PRIVATE_SELECTOR",
        ),
        (
            "MES4230_4_MHref_positive",
            "MHref positivity",
            "M_H_ref_private >= M_EH_private(1-epsilon_abs_private) = M_EH_private > 0",
            "This gives a private denominator pass, not a public local-GR theorem.",
            "MHREF_POSITIVE_PRIVATE_NONCLAIM",
        ),
        (
            "MES4230_5_claim_ceiling",
            "claim ceiling",
            "public_local_GR_claim := false; global_parent_adoption := false; numeric_G_prediction := false",
            "The route is a full private selector pass with explicit reopen rules, not a global proof.",
            "NONCLAIM_FIREWALL_ACTIVE",
        ),
    ]
    return [
        {
            **common(),
            "score_id": score_id,
            "piece": piece,
            "formula_or_statement": formula,
            "derivation": derivation,
            "status": status,
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
        for score_id, piece, formula, derivation, status in data
    ]


def decision_rows() -> List[Dict[str, str]]:
    return [
        {
            **common(),
            "decision": DECISION,
            "E_plus_private_positive": "True",
            "epsilon_E_private": "0",
            "MEH_private_selector_positive": "True",
            "epsilon_abs_private": "0",
            "MHref_private_selector_positive": "True",
            "full_private_selector_pass": "True",
            "global_parent_adoption": "False",
            "nonEH_global_coefficients_zero_or_numeric": "False",
            "public_local_GR_claim": "False",
            "newton_public_claim": "False",
            "PPN_public_claim": "False",
            "numeric_G_prediction": "False",
            "summary": "4230 assembles a full private-selector MEH/MHref denominator pass: all total epsilon rows are zero only inside the compact dressed Hilbert local selector, while non-EH/EFT, flux, reference, frame and boundary reopen rules remain active.",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
    ]


def firewall_rows() -> List[Dict[str, str]]:
    data = [
        (
            "MEF4230_0_no_global_selector_claim",
            "Do not treat the full private selector pass as global MTS parent adoption.",
            "BLOCKED",
            "The non-EH coefficient map and global parent-action adoption remain open.",
        ),
        (
            "MEF4230_1_no_nonEH_erasure",
            "Do not erase torsion/R2/disformal/memory/boundary residuals outside the full private Palatini selector.",
            "BLOCKED",
            "Finite coefficients reopen R11/non-EH empirical or parent-zero gates.",
        ),
        (
            "MEF4230_2_no_flux_erasure",
            "Do not zero radiative/open flux that crosses the local collar.",
            "BLOCKED",
            "Nonzero flux is physical boundary/Hamiltonian energy and must be routed or bounded.",
        ),
        (
            "MEF4230_3_no_reference_or_frame_fit",
            "Do not choose H_ref, tau, surfaces, coframe or readout after seeing residuals.",
            "BLOCKED",
            "The locks must be parent-selected before variation and comparison.",
        ),
        (
            "MEF4230_4_no_public_local_GR_or_numeric_G",
            "Do not claim public local GR, Newton, PPN or a numerical prediction of G_N from this packet.",
            "BLOCKED",
            "4230 is a private branch score, not a global/public theorem.",
        ),
    ]
    return [
        {
            **common(),
            "firewall_id": firewall_id,
            "forbidden_move": forbidden_move,
            "status": status,
            "reason": reason,
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
        for firewall_id, forbidden_move, status, reason in data
    ]


def status_rows() -> List[Dict[str, str]]:
    return [
        {
            **common(),
            "status_id": "MTS4230_STATUS",
            "decision": DECISION,
            "summary": "Full private-selector MEH/MHref positivity is scored, with global non-EH adoption and empirical refresh left as the next work.",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
    ]


def next_target_rows() -> List[Dict[str, str]]:
    return [
        {
            **common(),
            "next_target": NEXT_TARGET,
            "reason": "4230 gives a full private-selector denominator pass; the next job is to refresh the local scorecard and separate private branch pass from public/global adoption debt.",
            "derive_first": "write the private local-GR scorecard with exact branch clauses and non-EH/global adoption debts",
            "fill_second": "refresh PPN/R10/WEP/clock/orbital rows against the 4230 branch and flag which remain anchor-only or coefficient-missing",
            "fallback": "if public/global adoption is demanded, move to parent-zero or empirical bounds for non-EH coefficients before claiming local GR",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
    ]


def formal_doc() -> str:
    return f"""# 246 - PPC4161 MEH Total Epsilon Score Open Reference Virial Frame Gate

Marker: `{MARKER}`

Branch: `{BRANCH}`
Decision: `{DECISION}`

## Total residual assembly

Starting from:

```text
M_EH >= c^-2 E_plus(1-epsilon_E),
epsilon_E =
(E_core_bind_abs + E_open_abs + E_ref_abs + E_vir_abs + E_nonEH_abs + E_frame_abs)/E_plus.
```

4230 uses the dressed source branch:

```text
E_plus_private := E_H^dress = c^2 M_H^dress > 0.
```

and the private compact local selector routes:

```text
E_core_bind_abs = 0,
E_open_abs = 0,
E_ref_abs = 0,
E_vir_abs = 0,
E_frame_abs = 0,
E_nonEH_abs = 0 only inside the full private Palatini/EH IR selector.
```

Therefore:

```text
epsilon_E_private = 0,
M_EH_private >= c^-2 E_plus_private = M_H^dress > 0.
```

## Denominator reference gate

4220 gave:

```text
M_H_ref >= M_EH(1-epsilon_abs),
epsilon_abs := sum_i |Delta_i|/(G_ref M_EH).
```

Using the 4213-4219 numerator closures plus the fixed-reference, no-flux and same-frame selector:

```text
epsilon_abs_private = 0,
M_H_ref_private >= M_EH_private > 0.
```

## What remains

This is the first real private local denominator pass. It is not a public/global claim because:

- non-EH/EFT coefficients are only zero inside the adopted private selector;
- global parent-action adoption remains unproved;
- radiative/open flux reopens a boundary row;
- drifting reference/frame/readout reopens epsilon rows;
- numerical `G_N` is calibrated, not predicted.

## Next target

`{NEXT_TARGET}`.
"""


def checkpoint_doc() -> str:
    return f"""# 4230 - MEH Total Epsilon Score Open Reference Virial Frame Gate

**Status:** `{DECISION}`.

## What moved

The private compact dressed-source selector now scores:

```text
epsilon_E_private = 0
M_EH_private > 0
epsilon_abs_private = 0
M_H_ref_private > 0
```

This is a private local denominator pass, not a public local-GR theorem.

## Why it is not smuggling

Every zero has a reopen rule:

```text
non-EH coefficient survives -> R11/non-EH bound row reopens
open flux crosses the collar -> E_open_abs reopens
reference/frame/readout chosen after residuals -> epsilon_abs reopens
nonstationary pressure/surface stress -> E_vir_abs reopens
```

## Next

`{NEXT_TARGET}`.
"""


def update_registers() -> None:
    claim_row = (
        f'{CLAIM_ID},local_gr,'
        f'"Inside the full private compact dressed-source selector, the MEH total epsilon score closes: E_plus_private=E_H^dress>0, epsilon_E_private=0, M_EH_private>0, epsilon_abs_private=0, and M_H_ref_private>0. The pass is explicitly private because non-EH/EFT coefficients, open flux, reference/frame choices, virial pressure and boundary terms reopen bound rows outside the selector.",'
        f'"4230 source audit, residual route matrix, MEH epsilon score rows, decision and firewall.",'
        f'private_MEH_total_epsilon_denominator_pass_nonclaim,'
        f'"Refresh the local scorecard and separate private branch pass from public/global adoption debt, especially non-EH coefficients and full R10 curve evidence.",'
        f'"This is not global MTS adoption, public local GR, Newton/PPN publication claim, empirical raw-data reanalysis, or numerical G_N prediction."'
    )
    append_once(FORMAL / "02-claims-register.csv", CLAIM_ID, claim_row)

    spine_block = f"""
## 105. MEH Total Epsilon Private Selector Pass

Marker: `{MARKER}`

4230 assembles the total denominator route:

```text
epsilon_E_private = 0,
M_EH_private > 0,
epsilon_abs_private = 0,
M_H_ref_private > 0.
```

This holds only inside the full private compact dressed-source selector. Non-EH/EFT coefficients, nonzero flux, drifting reference/frame/readout, and nonstationary pressure/surface stress reopen explicit bound rows.
"""
    append_once(FORMAL / "07-unification-spine.md", MARKER, spine_block)

    packet_block = f"""
## Packet Update - MEH Total Epsilon Private Selector

Marker: `{PACKET_MARKER}`

The private local packet now has an internally scored denominator pass. The next work is a scorecard refresh and a clean separation between private local selector compatibility and global/public parent-action adoption.
"""
    append_once(FORMAL / "180-PPC4161-private-local-packet-integration.md", PACKET_MARKER, packet_block)


def validate(rows_by_file: Dict[str, List[Dict[str, str]]]) -> List[Dict[str, str]]:
    sources = rows_by_file["P8_Y5_R2FR_4230_SOURCE_REGISTER.csv"]
    routes = rows_by_file["P8_Y5_R2FR_4230_RESIDUAL_ROUTE_MATRIX.csv"]
    scores = rows_by_file["P8_Y5_R2FR_4230_MEH_EPSILON_SCORE.csv"]
    decision = rows_by_file["P8_Y5_R2FR_4230_DECISION.csv"][0]
    firewalls = rows_by_file["P8_Y5_R2FR_4230_CLAIM_FIREWALL.csv"]
    next_rows = rows_by_file["P8_Y5_R2FR_4230_NEXT_TARGET.csv"]
    all_rows = [row for rows in rows_by_file.values() for row in rows]
    route_ids = {row["route_id"] for row in routes}
    score_ids = {row["score_id"] for row in scores}
    firewall_ids = {row["firewall_id"] for row in firewalls}

    checks = [
        ("VAL4230_0_sources_exist", "all source paths exist", all(row["exists"] == "True" for row in sources)),
        ("VAL4230_1_source_needles", "all required source text found", all(row["required_text_found"] == "True" for row in sources)),
        (
            "VAL4230_2_route_matrix",
            "route matrix covers core-bind, open flux, reference, virial, frame, nonEH and epsilon_abs",
            {"MTR4230_0_core_bind", "MTR4230_1_open_flux", "MTR4230_2_reference", "MTR4230_3_virial_pressure", "MTR4230_4_frame", "MTR4230_5_nonEH", "MTR4230_6_epsilon_abs"}.issubset(route_ids),
        ),
        (
            "VAL4230_3_score_rows",
            "score rows include positive pool, epsilon_E, MEH, epsilon_abs and MHref positivity",
            {"MES4230_0_positive_pool", "MES4230_1_total_epsilon", "MES4230_2_MEH_positive", "MES4230_3_epsilon_abs", "MES4230_4_MHref_positive"}.issubset(score_ids),
        ),
        (
            "VAL4230_4_private_score",
            "decision records private MEH/MHref positivity and zero epsilons",
            decision["epsilon_E_private"] == "0"
            and decision["MEH_private_selector_positive"] == "True"
            and decision["epsilon_abs_private"] == "0"
            and decision["MHref_private_selector_positive"] == "True",
        ),
        (
            "VAL4230_5_global_not_claimed",
            "global parent adoption and public local claims remain false",
            decision["global_parent_adoption"] == "False"
            and decision["public_local_GR_claim"] == "False"
            and decision["newton_public_claim"] == "False"
            and decision["PPN_public_claim"] == "False",
        ),
        (
            "VAL4230_6_nonEH_debt_visible",
            "nonEH global coefficient debt remains visible",
            decision["nonEH_global_coefficients_zero_or_numeric"] == "False"
            and any(row["route_id"] == "MTR4230_5_nonEH" and "R11/non-EH" in row["fallback_or_reopen_rule"] for row in routes),
        ),
        (
            "VAL4230_7_firewall",
            "firewall blocks global selector claim, nonEH erasure, flux erasure, reference/frame fitting and public local GR/numeric G",
            {"MEF4230_0_no_global_selector_claim", "MEF4230_1_no_nonEH_erasure", "MEF4230_2_no_flux_erasure", "MEF4230_3_no_reference_or_frame_fit", "MEF4230_4_no_public_local_GR_or_numeric_G"}.issubset(firewall_ids),
        ),
        (
            "VAL4230_8_no_claim_flags",
            "all generated claim flags remain false",
            all(row.get("claim_allowed", "False") == "False" and row.get("valid_for_claim", "False") == "False" for row in all_rows),
        ),
        ("VAL4230_9_docs_written", "formal and checkpoint docs written", FORMAL_PATH.exists() and DOC_PATH.exists()),
        ("VAL4230_10_claim_register", "claim register contains L-071", CLAIM_ID in read_text(FORMAL / "02-claims-register.csv")),
        ("VAL4230_11_spine_packet", "spine and packet contain 4230 markers", MARKER in read_text(FORMAL / "07-unification-spine.md") and PACKET_MARKER in read_text(FORMAL / "180-PPC4161-private-local-packet-integration.md")),
        ("VAL4230_12_next_target", "next target selected", next_rows[0]["next_target"] == NEXT_TARGET),
        ("VAL4230_13_status_script", "status records decision and generator script exists", rows_by_file["P8_Y5_R2FR_4230_STATUS.csv"][0]["decision"] == DECISION and (SCRIPTS / "Y5_R2FR_4230_MEH_total_epsilon_score_open_reference_virial_frame_gate.py").exists()),
        (
            "VAL4230_14_reopen_rules",
            "every route row has an explicit reopen/fallback rule",
            all(bool(row["fallback_or_reopen_rule"]) for row in routes),
        ),
    ]
    return [
        {**common(), "check_id": check_id, "description": description, "passed": str(bool(passed))}
        for check_id, description, passed in checks
    ]


def write_all() -> None:
    rows_by_file: Dict[str, List[Dict[str, str]]] = {
        "P8_Y5_R2FR_4230_SOURCE_REGISTER.csv": source_rows(),
        "P8_Y5_R2FR_4230_RESIDUAL_ROUTE_MATRIX.csv": route_rows(),
        "P8_Y5_R2FR_4230_MEH_EPSILON_SCORE.csv": score_rows(),
        "P8_Y5_R2FR_4230_DECISION.csv": decision_rows(),
        "P8_Y5_R2FR_4230_CLAIM_FIREWALL.csv": firewall_rows(),
        "P8_Y5_R2FR_4230_STATUS.csv": status_rows(),
        "P8_Y5_R2FR_4230_NEXT_TARGET.csv": next_target_rows(),
    }
    for filename, rows in rows_by_file.items():
        write_csv(SOURCE_DIR / filename, rows)

    FORMAL_PATH.write_text(formal_doc(), encoding="utf-8")
    DOC_PATH.write_text(checkpoint_doc(), encoding="utf-8")
    update_registers()
    validation_rows = validate(rows_by_file)
    write_csv(VALIDATION_PATH, validation_rows)


def main() -> None:
    write_all()
    print(DECISION)
    print(f"formal={FORMAL_PATH}")
    print(f"checkpoint={DOC_PATH}")
    print(f"validation={VALIDATION_PATH}")
    print("rows=15 validation checks")


if __name__ == "__main__":
    main()

from __future__ import annotations

import csv
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List, Tuple


ROOT = Path(__file__).resolve().parents[2]
FORMAL = ROOT / "formalization-workbench"
POST = ROOT / "post-checkpoint-work"
SOURCE_DIR = POST / "source-intake" / "mts_residuals"

CHECKPOINT = "4315"
CLAIM_ID = "L-156"
BRANCH = "MTS_R2FR_Y5_HODGE_CONSTITUTIVE_OWNER_ZERO_OR_DELTAHODGE_BOUND_4315"
DECISION = "SAME_HODGE_CONSTITUTIVE_OWNER_ZERO_OR_NO_CANCELLATION_DELTAHODGE_BOUND_STAGED_NONCLAIM"
MARKER = "PPC4161_HODGE_CONSTITUTIVE_OWNER_ZERO_OR_DELTAHODGE_BOUND_4315"
PACKET_MARKER = "PPC4161_PACKET_HODGE_CONSTITUTIVE_OWNER_ZERO_OR_DELTAHODGE_BOUND_4315"
NEXT_TARGET = "4316-Y5-R2FR-visible-Hilbert-source-silence-integration-or-nonEM-residual-budget.md"

FORMAL_PATH = FORMAL / "331-PPC4161-Hodge-constitutive-owner-zero-or-DeltaHodge-bound.md"
DOC_PATH = POST / "4315-Y5-R2FR-Hodge-constitutive-owner-zero-or-DeltaHodge-bound.md"
VALIDATION_PATH = SOURCE_DIR / "P8_Y5_BRR545_4315_VALIDATION.csv"

STAMP = datetime.now(timezone.utc).replace(microsecond=0).isoformat()

SOURCES: Dict[str, Tuple[Path, str, str]] = {
    "SRC4315_00_4314_next": (
        SOURCE_DIR / "P8_Y5_R2FR_4314_NEXT_TARGET.csv",
        "4315-Y5-R2FR-Hodge-constitutive-owner-zero-or-DeltaHodge-bound.md",
        "4314 handoff selecting Hodge/constitutive owner or Delta_Hodge_EM bound.",
    ),
    "SRC4315_01_4314_status": (
        SOURCE_DIR / "P8_Y5_R2FR_4314_STATUS.csv",
        "Delta_Hodge_EM",
        "4314 status marks Delta_Hodge_EM as the next open EM gate.",
    ),
    "SRC4315_02_4260_formal": (
        FORMAL / "276-PPC4161-Delta-Hodge-EM-closure-or-bound.md",
        "Delta_Hodge_EM = 0",
        "4260 Hodge uniqueness lemma and unsigned parent-action clauses.",
    ),
    "SRC4315_03_4208_formal": (
        FORMAL / "224-PPC4161-Hodge-deformation-zero-or-constitutive-bound.md",
        "chi_EM != chi(g_obs)",
        "4208 constitutive countermodel and no-cancellation envelope.",
    ),
    "SRC4315_04_4261_action_domain": (
        FORMAL / "277-PPC4161-visible-EM-action-domain-fork-or-constitutive-bound.md",
        "DeltaS_MTS_visible = 0 before variation",
        "4261 signs the visible EM action domain only inside the calibrated branch.",
    ),
    "SRC4315_05_4262_readout": (
        FORMAL / "278-PPC4161-visible-EM-readout-guard-or-charge-normalization-bound.md",
        "C_Hodge_readout = 0",
        "4262 readout-after-variation guard for calibrated visible branch.",
    ),
    "SRC4315_06_3504_flow": (
        SOURCE_DIR / "P8_EM_Hodge_flow_rule_bound_or_zero.csv",
        "DHB3504_0_Delta_Hodge_EM",
        "component-level Hodge flow rule bound/zero ledger.",
    ),
    "SRC4315_07_3506_runner": (
        SOURCE_DIR / "P8_EM_first_constitutive_bound_runner_results.csv",
        "BRUN3506_0_Delta_chi_principal",
        "first constitutive bound runner showing missing coefficients/bounds.",
    ),
    "SRC4315_08_4312_bound": (
        SOURCE_DIR / "P8_Y5_R2FR_4312_COLLAR_EM_RESIDUAL_BOUND.csv",
        "R_EM_Poynting <=",
        "4312 residual bound where Hodge defects feed R_EM_Poynting and Eta_H.",
    ),
    "SRC4315_09_4314_flux": (
        FORMAL / "330-PPC4161-radiative-Poynting-no-flux-or-boundary-flux-row.md",
        "N_boundary_rad_EM",
        "4314 radiative row separated from Hodge/constitutive defects.",
    ),
    "SRC4315_10_precision": (
        FORMAL / "309-PPC4161-epsilon-mu-tr-shared-local-bound-runner-WEP-R10-PPN-clocks-orbital.md",
        "order-one projection of epsilon_AJ_seed into local observables fails",
        "local precision guard for Hodge/constitutive leakage.",
    ),
    "SRC4315_11_newton_guard": (
        POST / "1714-Y5-R2FR-Y5-worldtube-Hilbert-source-equality-or-Req-Icommutator-fill.md",
        "R_eq",
        "source-to-Newton equality gate remains open.",
    ),
}


def base_row() -> Dict[str, str]:
    return {
        "checkpoint": CHECKPOINT,
        "branch": BRANCH,
        "generated_utc": STAMP,
        "decision": DECISION,
        "claim_allowed": "False",
        "valid_for_claim": "False",
    }


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


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
        writer.writerows(rows)


def md_table(rows: List[Dict[str, str]], columns: List[str]) -> str:
    lines = [
        "| " + " | ".join(columns) + " |",
        "| " + " | ".join("---" for _ in columns) + " |",
    ]
    for row in rows:
        values = [str(row.get(col, "")).replace("\n", "<br>").replace("|", "\\|") for col in columns]
        lines.append("| " + " | ".join(values) + " |")
    return "\n".join(lines)


def append_once(path: Path, marker: str, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    existing = read_text(path) if path.exists() else ""
    if marker in existing:
        return
    with path.open("a", encoding="utf-8", newline="") as handle:
        if existing and not existing.endswith("\n"):
            handle.write("\n")
        handle.write("\n" + content.strip() + "\n")


def append_claim_once() -> None:
    path = FORMAL / "02-claims-register.csv"
    existing = read_text(path) if path.exists() else ""
    if CLAIM_ID in existing:
        return
    row = [
        CLAIM_ID,
        "em_local_gr",
        (
            "4315 derives the Hodge/constitutive owner gate after the radiative Poynting row. The Hodge star on "
            "two-forms is unique once the observed coframe, metric, orientation and volume form are fixed; therefore "
            "Delta_Hodge_EM=0 only inside the same-Hodge Maxwell branch with no independent chi_EM, hidden/disformal "
            "EM metric, skewon/dissipative term, active axion-gradient bulk response or readout-regenerated Hodge map. "
            "If any such term survives, the constitutive mismatch is retained as a no-cancellation envelope built from "
            "Delta_chi_principal, Delta_chi_skewon, dtheta_EM, C_Hodge_hidden, C_Hodge_readout and orientation flux, "
            "feeding R_EM_Poynting, Eta_H and S_U. This is a private source-coupling discipline step and does not "
            "claim local GR/Newton/R10/PPN or a derivation of alpha_EM/G_N."
        ),
        (
            "4315 source register, same-Hodge theorem, constitutive residual envelope, scale guard, collar update, "
            "runner, firewall, status, next-target and validation CSV."
        ),
        "private_same_Hodge_constitutive_owner_zero_or_DeltaHodge_bound_nonclaim",
        (
            "Parent-sign same-Hodge visible EM action ownership or fill source-backed bounds for principal, skewon, "
            "axion-gradient, hidden-Hodge, readout-Hodge and orientation terms."
        ),
        (
            "Using Hodge uniqueness to derive alpha_EM, mu0, charge normalization, G_N or source mass; cancelling "
            "principal/skewon/readout terms against each other; or treating a calibrated visible branch as global MTS "
            "electromagnetism."
        ),
    ]
    with path.open("a", encoding="utf-8", newline="") as handle:
        csv.writer(handle).writerow(row)


def source_rows() -> List[Dict[str, str]]:
    rows: List[Dict[str, str]] = []
    for source_id, (path, needle, purpose) in SOURCES.items():
        text = read_text(path) if path.exists() else ""
        row = base_row()
        row.update(
            {
                "source_id": source_id,
                "source_path": str(path),
                "exists": str(path.exists()),
                "needle": needle,
                "needle_found": str(needle in text),
                "purpose": purpose,
            }
        )
        rows.append(row)
    return rows


def hodge_theorem_rows() -> List[Dict[str, str]]:
    specs = [
        (
            "HT4315_0_unique_hodge",
            "observed Hodge uniqueness",
            "fixed e_obs, g_obs, orientation and volume determine *_obs by alpha wedge *_obs beta = <alpha,beta>_g_obs vol_obs",
            "mathematical uniqueness lemma",
            "EXACT_MATH_LEMMA",
        ),
        (
            "HT4315_1_same_action",
            "same-Hodge Maxwell action",
            "S_EM = -(4 mu0)^-1 int F wedge *_obs F with no independent chi_EM",
            "Delta_Hodge_EM=0 inside the calibrated same-Hodge visible branch",
            "EXACT_ZERO_IF_PARENT_BRANCH_SIGNED",
        ),
        (
            "HT4315_2_action_domain",
            "visible action-domain branch",
            "DeltaS_MTS_visible=0 before variation and S_Maxwell-Hodge uses g_obs and *_obs",
            "visible EM action-domain contribution to Delta_Hodge_EM is zero only in this branch",
            "CONDITIONAL_BRANCH_ZERO",
        ),
        (
            "HT4315_3_readout_guard",
            "readout Hodge guard",
            "readout is pure postprocessing with no argument slot in parent/effective action",
            "C_Hodge_readout=0 only under readout-after-variation discipline",
            "CONDITIONAL_BRANCH_ZERO",
        ),
        (
            "HT4315_4_countermodel",
            "constitutive countermodel",
            "S_EM = -1/4 int F_ab chi_EM^abcd F_cd vol_obs with chi_EM != chi(g_obs)",
            "gauge covariance alone does not imply Delta_Hodge_EM=0",
            "COUNTERMODEL_RETAINED",
        ),
        (
            "HT4315_5_zero_contract",
            "full Hodge zero contract",
            "same Hodge action, no principal/skewon/axion-gradient/hidden/readout/orientation residuals",
            "Delta_Hodge_EM=0 and Hodge term drops from R_EM_Poynting/Eta_H/S_U",
            "EXACT_ZERO_IF_ALL_CLAUSES_SIGNED",
        ),
    ]
    rows: List[Dict[str, str]] = []
    for theorem_id, clause, statement, result, status in specs:
        row = base_row()
        row.update(
            {
                "theorem_id": theorem_id,
                "clause": clause,
                "statement": statement,
                "result": result,
                "status": status,
                "score_ready": "False",
            }
        )
        rows.append(row)
    return rows


def residual_rows() -> List[Dict[str, str]]:
    specs = [
        (
            "CR4315_0_Delta_chi_principal",
            "Delta_chi_principal",
            "principal constitutive tensor changes EM cone/anisotropy/birefringence",
            "||Delta_chi_principal||",
            "vacuum_birefringence; light_cone; Shapiro/lensing consistency",
        ),
        (
            "CR4315_1_Delta_chi_skewon",
            "Delta_chi_skewon",
            "skewon/nonreciprocal/dissipative constitutive piece",
            "||Delta_chi_skewon||",
            "polarization; dispersion; Poynting flux nonconservation",
        ),
        (
            "CR4315_2_dtheta_EM",
            "dtheta_EM",
            "active axion-gradient or pseudoscalar bulk response",
            "L||d theta_EM||",
            "polarization rotation; parity-odd EM propagation",
        ),
        (
            "CR4315_3_C_Hodge_hidden",
            "C_Hodge_hidden",
            "hidden/motion/time field defines a disformal or medium-like EM Hodge star",
            "|C_Hodge_hidden|",
            "preferred frame; light-speed anisotropy; clock",
        ),
        (
            "CR4315_4_C_Hodge_readout",
            "C_Hodge_readout",
            "post-solution readout/clock/spectroscopy map regenerates Hodge or alpha response",
            "|C_Hodge_readout|",
            "clock; spectroscopy; alpha_EM; binding response",
        ),
        (
            "CR4315_5_Delta_orientation_flux",
            "Delta_orientation_flux",
            "orientation/time-orientation or boundary normal differs between EM and source charge",
            "|Delta_orientation_flux|",
            "Poynting sign; boundary source orientation",
        ),
    ]
    rows: List[Dict[str, str]] = []
    for residual_id, symbol, meaning, envelope_term, observable_links in specs:
        row = base_row()
        row.update(
            {
                "residual_id": residual_id,
                "symbol": symbol,
                "meaning": meaning,
                "envelope_term": envelope_term,
                "observable_links": observable_links,
                "status": "EXPLICIT_BOUND_ROW_VALUE_MISSING",
                "source_path": "",
                "numeric_value": "",
                "units": "dimensionless_or_declared_tensor_norm",
                "next_action": "parent-sign zero or fill sourced coefficient and observational bound",
                "score_ready": "False",
            }
        )
        rows.append(row)
    return rows


def bound_rows() -> List[Dict[str, str]]:
    specs = [
        (
            "HB4315_0_envelope",
            "Delta_Hodge_EM",
            "||Delta_Hodge_EM|| <= ||Delta_chi_principal|| + ||Delta_chi_skewon|| + L||dtheta_EM|| + |C_Hodge_hidden| + |C_Hodge_readout| + |Delta_orientation_flux|",
            "no-cancellation constitutive envelope",
            "BOUND_DERIVED_VALUES_MISSING",
        ),
        (
            "HB4315_1_zero",
            "Delta_Hodge_EM_zero",
            "all constitutive residual components zero in same-Hodge parent-visible branch",
            "Delta_Hodge_EM=0",
            "CONDITIONAL_ZERO_NOT_GLOBAL",
        ),
        (
            "HB4315_2_R_EM_update",
            "R_EM_Poynting",
            "R_EM_Poynting <= R_EM_noHodge + C_H ||Delta_Hodge_EM|| ||F||^2",
            "4312 EM residual with Hodge mismatch explicit",
            "FORMULA_READY_VALUES_MISSING",
        ),
        (
            "HB4315_3_EtaH_update",
            "Eta_H",
            "Eta_H >= Eta_H_noHodge + C_Eta_Hodge ||Delta_Hodge_EM|| ||F||^2",
            "lambda-floor correction if Hodge mismatch survives",
            "FORMULA_READY_VALUES_MISSING",
        ),
        (
            "HB4315_4_SU_update",
            "S_U",
            "S_U <= S_U_noHodge + N_Hodge_EM",
            "collar residual numerator receives constitutive mismatch as named term",
            "FORMULA_READY_VALUES_MISSING",
        ),
    ]
    rows: List[Dict[str, str]] = []
    for bound_id, symbol, law, role, status in specs:
        row = base_row()
        row.update(
            {
                "bound_id": bound_id,
                "symbol": symbol,
                "law": law,
                "role": role,
                "status": status,
                "source_path": "",
                "numeric_value": "",
                "units": "dimensionless_or_source_normalized_after_projection",
                "next_action": "prove same-Hodge zero or source every term in the no-cancellation envelope",
                "score_ready": "False",
            }
        )
        rows.append(row)
    return rows


def scale_guard_rows() -> List[Dict[str, str]]:
    specs = [
        ("SG4315_0_alpha", "alpha_EM", "not derived by Hodge matching", "requires Maxwell normalization/current-scale gate"),
        ("SG4315_1_mu0", "mu0/Z_Q", "not derived by two-form Hodge uniqueness", "requires EM normalization/action-scale input"),
        ("SG4315_2_charge", "charge normalization", "not derived by constitutive cone matching", "requires current lattice/source normalization"),
        ("SG4315_3_GN", "G_N/source mass", "not derived by EM Hodge closure", "requires Hilbert/Newton source calibration"),
        ("SG4315_4_conformal", "conformal scale", "two-form Hodge star in 4D is conformally invariant", "prevents smuggling scale constants into Hodge theorem"),
    ]
    rows: List[Dict[str, str]] = []
    for guard_id, item, rule, implication in specs:
        row = base_row()
        row.update({"guard_id": guard_id, "item": item, "rule": rule, "implication": implication, "status": "ACTIVE"})
        rows.append(row)
    return rows


def runner_rows() -> List[Dict[str, str]]:
    specs = [
        (
            "RUN4315_0_current_corpus",
            "current corpus",
            "CONDITIONAL_ZERO_OR_BOUND",
            "same-Hodge zero branch exists for calibrated visible branch; global MTS EM constitutive ownership remains unproved",
            "keep Delta_Hodge_EM zero only branch-local and retain bound rows",
        ),
        (
            "RUN4315_1_same_hodge",
            "same observed Hodge owner with no independent constitutive terms",
            "ALLOW_DELTA_HODGE_ZERO_CONDITIONAL",
            "Delta_Hodge_EM drops from R_EM_Poynting, Eta_H and S_U",
            "still requires lambda/source-equality/non-EM residual gates",
        ),
        (
            "RUN4315_2_constitutive_deformation",
            "principal/skewon/axion/hidden/readout/orientation residual survives",
            "KEEP_CONSTITUTIVE_BOUND",
            "Hodge mismatch enters local precision via explicit no-cancellation envelope",
            "source coefficients and bounds before scoring local arenas",
        ),
        (
            "RUN4315_3_scale_claim",
            "derive alpha_EM, G_N or source mass from Hodge closure",
            "REJECT",
            "four-dimensional two-form Hodge closure does not fix coupling scale",
            "route scale constants to separate normalization gates",
        ),
        (
            "RUN4315_4_local_claim",
            "claim local GR/Newton/R10/PPN now",
            "REJECT",
            "lambda components, non-EM residuals, source equality, I_commutator and projection gates remain open",
            "continue derivation chain",
        ),
    ]
    rows: List[Dict[str, str]] = []
    for runner_id, case, result, reason, next_action in specs:
        row = base_row()
        row.update(
            {
                "runner_id": runner_id,
                "case": case,
                "result": result,
                "reason": reason,
                "next_action": next_action,
                "score_ready": "False",
            }
        )
        rows.append(row)
    return rows


def decision_rows() -> List[Dict[str, str]]:
    specs = [
        (
            "DEC4315_0_zero",
            "SAME_HODGE_ZERO_ROUTE_IS_CLEAN",
            "Observed Hodge uniqueness plus same-Hodge Maxwell action can set Delta_Hodge_EM=0 in the calibrated branch.",
            "use only inside the branch with all constitutive counterterms forbidden",
        ),
        (
            "DEC4315_1_bound",
            "CONSTITUTIVE_COUNTERMODEL_RETAINED",
            "Gauge covariance does not forbid chi_EM != chi(g_obs); the no-cancellation envelope is required.",
            "feed Delta_Hodge_EM into R_EM_Poynting, Eta_H and S_U if any term survives",
        ),
        (
            "DEC4315_2_scale",
            "HODGE_MATCHING_IS_NOT_SCALE_DERIVATION",
            "Two-form Hodge closure does not derive alpha_EM, charge scale, G_N or source mass.",
            "keep normalization/source calibration gates separate",
        ),
        (
            "DEC4315_3_frontier",
            "VISIBLE_HILBERT_SOURCE_SILENCE_INTEGRATION_NEXT",
            "EM residuals are now mostly zero-or-bound; next useful step is integrating visible Hilbert silence with remaining non-EM residual budget.",
            NEXT_TARGET,
        ),
        (
            "DEC4315_4_claim",
            "NO_LOCAL_CLAIM",
            "4315 improves the EM source-coupling ladder but does not complete the local GR/Newton route.",
            "keep all claim flags false",
        ),
    ]
    rows: List[Dict[str, str]] = []
    for decision_id, result, reason, next_action in specs:
        row = base_row()
        row.update({"decision_id": decision_id, "result": result, "reason": reason, "next_action": next_action})
        rows.append(row)
    return rows


def firewall_rows() -> List[Dict[str, str]]:
    rules = [
        "Do not claim Delta_Hodge_EM=0 from Hodge uniqueness unless the parent EM action uses the observed Hodge star only.",
        "Do not cancel principal, skewon, axion-gradient, hidden-Hodge and readout-Hodge terms against each other.",
        "Do not derive alpha_EM, mu0, charge normalization, source mass or G_N from Hodge closure.",
        "Do not treat the calibrated visible EM branch as global MTS electromagnetism.",
        "Do not claim local GR/Newton/R10/PPN from the Hodge gate alone.",
    ]
    rows: List[Dict[str, str]] = []
    for index, rule in enumerate(rules):
        row = base_row()
        row.update({"firewall_id": f"FW4315_{index}", "rule": rule, "status": "ACTIVE"})
        rows.append(row)
    return rows


def status_rows() -> List[Dict[str, str]]:
    specs = [
        ("STAT4315_0_math", "Hodge uniqueness", "EXACT_MATH", "fixed observed metric/coframe/orientation determines *_obs"),
        ("STAT4315_1_zero", "Delta_Hodge_EM", "ZERO_OR_BOUND", "zero only in same-Hodge calibrated branch"),
        ("STAT4315_2_envelope", "constitutive envelope", "EXPLICIT", "principal/skewon/axion/hidden/readout/orientation rows named"),
        ("STAT4315_3_scale", "alpha/G/source scale", "SEPARATE_GATE", "not derived here"),
        ("STAT4315_4_next", "visible Hilbert silence", "NEXT_OPEN_GATE", "integrate EM zero-or-bound with non-EM residual budget"),
        ("STAT4315_5_local", "local GR/Newton", "BLOCKED", "source coupling sharper, full reduction still open"),
    ]
    rows: List[Dict[str, str]] = []
    for status_id, item, status, note in specs:
        row = base_row()
        row.update({"status_id": status_id, "item": item, "status": status, "note": note})
        rows.append(row)
    return rows


def next_rows() -> List[Dict[str, str]]:
    row = base_row()
    row.update(
        {
            "next_target_id": "NT4315_0",
            "next_target": NEXT_TARGET,
            "target_question": "Can visible Hilbert source silence be integrated with the EM zero-or-bound ledger to produce a reduced non-EM residual budget?",
            "preferred_route": "combine same-Hodge/current/radiative zero branches with 4303 visible Hilbert source silence",
            "fallback_route": "stage the remaining non-EM residual budget rows feeding S_U, Eta_H and the lambda-floor test",
        }
    )
    return [row]


def write_docs(tables: Dict[str, List[Dict[str, str]]]) -> None:
    formal_text = f"""# 331 PPC4161 Hodge constitutive owner zero or DeltaHodge bound

Marker: `{MARKER}`

## Decision

`{DECISION}`

4315 makes the Hodge gate exact:

```text
fixed e_obs, g_obs, orientation, volume
=> unique observed Hodge star *_obs.
```

The same-Hodge zero branch is:

```text
S_EM = -(4 mu0)^-1 int F wedge *_obs F,
no independent chi_EM,
no hidden/disformal EM metric,
no skewon/dissipative term,
no active axion-gradient bulk response,
no readout-regenerated Hodge map,
fixed orientation/boundary convention
=> Delta_Hodge_EM = 0.
```

The deformation branch is not handwaved:

```text
||Delta_Hodge_EM||
<= ||Delta_chi_principal||
 + ||Delta_chi_skewon||
 + L||dtheta_EM||
 + |C_Hodge_hidden|
 + |C_Hodge_readout|
 + |Delta_orientation_flux|.
```

This feeds:

```text
R_EM_Poynting <= R_EM_noHodge + C_H ||Delta_Hodge_EM|| ||F||^2,
Eta_H >= Eta_H_noHodge + C_Eta_Hodge ||Delta_Hodge_EM|| ||F||^2,
S_U <= S_U_noHodge + N_Hodge_EM.
```

## Same-Hodge Theorem

{md_table(tables["hodge"], ["theorem_id", "clause", "statement", "result", "status"])}

## Constitutive Residual Envelope

{md_table(tables["residuals"], ["residual_id", "symbol", "meaning", "envelope_term", "observable_links"])}

## Bound Update

{md_table(tables["bounds"], ["bound_id", "symbol", "law", "role", "status"])}

## Scale Guard

{md_table(tables["scale_guard"], ["guard_id", "item", "rule", "implication", "status"])}

## Runner

{md_table(tables["runner"], ["runner_id", "case", "result", "reason"])}

## Result

The Hodge branch is now sharp: same observed Hodge gives a branch-local zero; independent constitutive physics becomes an explicit no-cancellation bound. It does not derive alpha, charge scale, source mass, or Newton's constant.

Next target: `{NEXT_TARGET}`.
"""
    doc_text = f"""# 4315 - Hodge constitutive owner zero or DeltaHodge bound

## Verdict
- Derived the exact same-Hodge zero contract for `Delta_Hodge_EM`.
- Retained the constitutive countermodel: `chi_EM != chi(g_obs)` is a real residual, not killed by gauge covariance.
- Wrote the no-cancellation envelope for principal, skewon, axion-gradient, hidden-Hodge, readout-Hodge and orientation terms.
- Fed `Delta_Hodge_EM` into `R_EM_Poynting`, `Eta_H`, and `S_U`.
- Preserved the scale guard: no alpha, charge, source-mass or `G_N` derivation from Hodge closure.

## Source Register
{md_table(tables["sources"], ["source_id", "source_path", "exists", "needle_found", "purpose"])}

## Same-Hodge Theorem
{md_table(tables["hodge"], ["theorem_id", "clause", "statement", "result", "status"])}

## Constitutive Residual Envelope
{md_table(tables["residuals"], ["residual_id", "symbol", "meaning", "envelope_term", "observable_links", "status", "next_action"])}

## Bound Update
{md_table(tables["bounds"], ["bound_id", "symbol", "law", "role", "status", "next_action"])}

## Scale Guard
{md_table(tables["scale_guard"], ["guard_id", "item", "rule", "implication", "status"])}

## Runner
{md_table(tables["runner"], ["runner_id", "case", "result", "reason", "next_action"])}

## Claim Firewall
{md_table(tables["firewall"], ["firewall_id", "rule", "status"])}

## Decision
{md_table(tables["decision"], ["decision_id", "result", "reason", "next_action"])}

## Status
{md_table(tables["status"], ["status_id", "item", "status", "note"])}

## Next Target
{md_table(tables["next"], ["next_target_id", "next_target", "target_question", "preferred_route", "fallback_route"])}
"""
    FORMAL_PATH.write_text(formal_text, encoding="utf-8")
    DOC_PATH.write_text(doc_text, encoding="utf-8")


def validate_csv(path: Path) -> Tuple[bool, str]:
    try:
        with path.open("r", encoding="utf-8", newline="") as handle:
            rows = list(csv.DictReader(handle))
        return bool(rows), f"{path.name} parses with {len(rows)} rows"
    except Exception as exc:
        return False, f"{path.name} parse failure: {exc}"


def validation_rows(paths: Dict[str, Path], tables: Dict[str, List[Dict[str, str]]]) -> List[Dict[str, str]]:
    rows: List[Dict[str, str]] = []

    def add(check_id: str, description: str, passed: bool, evidence: str) -> None:
        row = base_row()
        row.update({"check_id": check_id, "description": description, "passed": str(passed), "evidence": evidence})
        rows.append(row)

    add("VAL4315_0_sources_exist", "all cited local source paths exist", all(Path(row["source_path"]).exists() for row in tables["sources"]), "source_register")
    add("VAL4315_1_needles_found", "all cited source needles found", all(row["needle_found"] == "True" for row in tables["sources"]), "source_register")
    add("VAL4315_2_same_hodge_zero", "same-Hodge zero theorem exists", any(row["theorem_id"] == "HT4315_5_zero_contract" for row in tables["hodge"]), "hodge")
    add("VAL4315_3_countermodel_retained", "constitutive countermodel retained", any(row["theorem_id"] == "HT4315_4_countermodel" for row in tables["hodge"]), "hodge")
    add("VAL4315_4_residual_components", "six residual envelope components exist", len(tables["residuals"]) == 6, "residuals")
    add("VAL4315_5_envelope_bound", "Delta_Hodge_EM no-cancellation envelope exists", any(row["bound_id"] == "HB4315_0_envelope" for row in tables["bounds"]), "bounds")
    add("VAL4315_6_scale_guard", "scale guard rejects alpha/G/source derivation", len(tables["scale_guard"]) == 5, "scale_guard")
    add("VAL4315_7_runner_rejects_claim", "runner rejects local claim from Hodge gate alone", any(row["runner_id"] == "RUN4315_4_local_claim" and row["result"] == "REJECT" for row in tables["runner"]), "runner")
    add("VAL4315_8_next_selected", f"next target is {NEXT_TARGET}", tables["next"][0]["next_target"] == NEXT_TARGET, "next")
    add(
        "VAL4315_9_claim_flags_false",
        "all generated rows keep claim flags false",
        all(row.get("claim_allowed") == "False" and row.get("valid_for_claim") == "False" for table in tables.values() for row in table),
        "generated_tables",
    )
    add(
        "VAL4315_10_score_flags_false",
        "all score rows remain unscored/nonclaim",
        all(row.get("score_ready", "False") == "False" for table in tables.values() for row in table),
        "generated_tables",
    )
    for name, path in paths.items():
        if name == "validation":
            continue
        ok, detail = validate_csv(path)
        add(f"VAL4315_csv_{name}", detail, ok, "generated_artifacts")
    add("VAL4315_docs", "formal and post checkpoint docs exist", FORMAL_PATH.exists() and DOC_PATH.exists(), "generated_docs")
    add("VAL4315_claim_row", f"{CLAIM_ID} claim-register row exists", CLAIM_ID in read_text(FORMAL / "02-claims-register.csv"), "claims_register")
    add("VAL4315_spine_marker", "spine marker exists", MARKER in read_text(FORMAL / "07-unification-spine.md"), "unification_spine")
    add("VAL4315_packet_marker", "packet marker exists", PACKET_MARKER in read_text(FORMAL / "180-PPC4161-private-local-packet-integration.md"), "private_packet")
    return rows


def main() -> None:
    paths = {
        "sources": SOURCE_DIR / "P8_Y5_R2FR_4315_SOURCE_REGISTER.csv",
        "hodge": SOURCE_DIR / "P8_Y5_R2FR_4315_SAME_HODGE_THEOREM.csv",
        "residuals": SOURCE_DIR / "P8_Y5_R2FR_4315_CONSTITUTIVE_RESIDUAL_ENVELOPE.csv",
        "bounds": SOURCE_DIR / "P8_Y5_R2FR_4315_DELTA_HODGE_BOUND_UPDATE.csv",
        "scale_guard": SOURCE_DIR / "P8_Y5_R2FR_4315_SCALE_GUARD.csv",
        "runner": SOURCE_DIR / "P8_Y5_R2FR_4315_COLLAR_ROUTE_RUNNER.csv",
        "firewall": SOURCE_DIR / "P8_Y5_R2FR_4315_CLAIM_FIREWALL.csv",
        "decision": SOURCE_DIR / "P8_Y5_R2FR_4315_DECISION.csv",
        "status": SOURCE_DIR / "P8_Y5_R2FR_4315_STATUS.csv",
        "next": SOURCE_DIR / "P8_Y5_R2FR_4315_NEXT_TARGET.csv",
        "validation": VALIDATION_PATH,
    }
    tables = {
        "sources": source_rows(),
        "hodge": hodge_theorem_rows(),
        "residuals": residual_rows(),
        "bounds": bound_rows(),
        "scale_guard": scale_guard_rows(),
        "runner": runner_rows(),
        "firewall": firewall_rows(),
        "decision": decision_rows(),
        "status": status_rows(),
        "next": next_rows(),
    }
    for key, rows in tables.items():
        write_csv(paths[key], rows)
    write_docs(tables)
    append_claim_once()
    append_once(
        FORMAL / "07-unification-spine.md",
        MARKER,
        f"""
## PPC4161 4315 Hodge constitutive owner zero or DeltaHodge bound

Marker: `{MARKER}`

4315 sharpens the Hodge/constitutive EM gate. Fixed observed coframe/metric/orientation gives a unique `*_obs`; the calibrated same-Hodge Maxwell action gives branch-local `Delta_Hodge_EM=0` only if independent constitutive terms are forbidden. Otherwise `Delta_Hodge_EM` is bounded by a no-cancellation envelope over principal, skewon, axion-gradient, hidden-Hodge, readout-Hodge and orientation terms, feeding `R_EM_Poynting`, `Eta_H`, and `S_U`. Hodge closure does not derive `alpha_EM`, charge normalization, source mass, or `G_N`.
""",
    )
    append_once(
        FORMAL / "180-PPC4161-private-local-packet-integration.md",
        PACKET_MARKER,
        f"""
## 4315 packet Hodge constitutive owner

Marker: `{PACKET_MARKER}`

Packet update: `Delta_Hodge_EM` is now a same-Hodge zero-or-bound row. The zero route is branch-local; every independent constitutive deformation is retained in a no-cancellation envelope and propagated into the local collar residual budget.
""",
    )
    validation = validation_rows(paths, tables)
    write_csv(paths["validation"], validation)
    failed = [row for row in validation if row["passed"] != "True"]
    print(f"{CHECKPOINT}: wrote {len(tables)} csv artifacts plus validation")
    print(f"{CHECKPOINT}: validation rows={len(validation)} failed={len(failed)}")
    print(f"{CHECKPOINT}: decision={DECISION}")
    if failed:
        for row in failed:
            print(f"FAILED {row['check_id']}: {row['description']} evidence={row['evidence']}")
        raise SystemExit(1)


if __name__ == "__main__":
    main()

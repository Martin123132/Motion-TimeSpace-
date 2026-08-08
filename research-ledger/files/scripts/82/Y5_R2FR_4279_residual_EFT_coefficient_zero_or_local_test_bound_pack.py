from __future__ import annotations

import csv
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, Iterable, List


ROOT = Path(__file__).resolve().parents[2]
FORMAL = ROOT / "formalization-workbench"
POST = ROOT / "post-checkpoint-work"
SOURCE_DIR = POST / "source-intake" / "mts_residuals"

CHECKPOINT = "4279"
CLAIM_ID = "L-120"
BRANCH = "MTS_R2FR_Y5_RESIDUAL_EFT_COEFFICIENT_ZERO_OR_LOCAL_TEST_BOUND_PACK_4279"
DECISION = "RESIDUAL_EFT_VECTOR_REDUCED_TO_PRIVATE_ZERO_SUBSET_AND_CGAMMA_R2_LAMBDA_BOUND_PACK_NONCLAIM"
MARKER = "PPC4161_RESIDUAL_EFT_COEFFICIENT_ZERO_OR_LOCAL_TEST_BOUND_PACK_4279"
PACKET_MARKER = "PPC4161_PACKET_RESIDUAL_EFT_COEFFICIENT_ZERO_OR_LOCAL_TEST_BOUND_PACK_4279"
NEXT_TARGET = "4280-Y5-R2FR-cGamma-parent-memory-equation-AJ-source-coefficient-or-profile-fill.md"

FORMAL_PATH = FORMAL / "295-PPC4161-residual-EFT-coefficient-zero-or-local-test-bound-pack.md"
DOC_PATH = POST / "4279-Y5-R2FR-residual-EFT-coefficient-zero-or-local-test-bound-pack.md"
VALIDATION_PATH = SOURCE_DIR / "P8_Y5_BRR545_4279_VALIDATION.csv"

STAMP = datetime.now(timezone.utc).replace(microsecond=0).isoformat()

SOURCES = {
    "SRC4279_00_4278_left_hand": (
        FORMAL / "294-PPC4161-left-hand-EH-Newton-limit-or-residual-EFT-bound-gate.md",
        "c_T             torsion/nonmetricity residual",
        "4278 left-hand residual EFT vector.",
    ),
    "SRC4279_01_4185_map": (
        FORMAL / "201-PPC4161-extra-invariant-residual-coefficient-map.md",
        "c_D         second metric / disformal same-coframe leak",
        "4185 residual coefficient map.",
    ),
    "SRC4279_02_4186_zero_law": (
        FORMAL / "202-PPC4161-same-coframe-source-memory-zero-law.md",
        "c_D_private_zero = true",
        "4186 private zero law for c_D and delta_kappa.",
    ),
    "SRC4279_03_4187_cGamma_contract": (
        FORMAL / "203-PPC4161-local-memory-support-projector-zero-law-for-cGamma.md",
        "c_Gamma_parent_zero = false",
        "4187 cGamma zero route fails without memory support/no-hair.",
    ),
    "SRC4279_04_4188_product_bounds": (
        FORMAL / "204-PPC4161-finite-cGamma-product-bound-law.md",
        "C_Gamma_Gdot` <= `2.42e-14` yr^-1",
        "4188 finite cGamma product bounds.",
    ),
    "SRC4279_05_4189_projection": (
        FORMAL / "205-PPC4161-cGamma-profile-projection-coefficient-gate.md",
        "C_Gamma_xi = c_Gamma L_loc |grad_perp Xi_0|",
        "4189 physical cGamma projection split.",
    ),
    "SRC4279_06_4234_Kperp": (
        FORMAL / "250-PPC4161-Kperp-EH-coframe-identity-proof-or-independent-tensor-source-row.md",
        "Kperp/c_T",
        "4234 removes Kperp/c_T as an extra static local force inside the private selector.",
    ),
    "SRC4279_07_4235_full_budget": (
        FORMAL / "251-PPC4161-cGamma-support-nohair-or-full-budget-profile-bound-runner.md",
        "|c_Gamma profile_alpha3| <= 4e-20",
        "4235 cGamma full-budget rows after Kperp removal.",
    ),
    "SRC4279_08_4236_AJ": (
        FORMAL / "252-PPC4161-cGamma-parent-memory-equation-or-AJ-coefficient-source-fill.md",
        "A_J,eff_private = A_src + A_lap + A_drift",
        "4236 cGamma parent-memory/AJ coefficient ledger.",
    ),
    "SRC4279_09_4259_EM": (
        FORMAL / "275-PPC4161-EM-Hodge-component-zero-or-residual-vector.md",
        "Poynting is not an extra background source",
        "4259 Maxwell-Hodge/Poynting stress owner guard.",
    ),
    "SRC4279_10_4268_boundary": (
        FORMAL / "284-PPC4161-Dq-boundary-projector-fixed-collar-or-boundary-residual-bound.md",
        "Dq_boundary_projector = 0",
        "4268 compact fixed collar branch for boundary/projector residuals.",
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
    if not rows:
        path.write_text("", encoding="utf-8")
        return
    fieldnames = list(rows[0].keys())
    for row in rows:
        for key in row:
            if key not in fieldnames:
                fieldnames.append(key)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def csv_rows(path: Path) -> List[Dict[str, str]]:
    if not path.exists():
        return []
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


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


def residual_classifier_rows() -> List[Dict[str, str]]:
    raw = [
        (
            "RC4279_0_cD",
            "c_D",
            "second metric/disformal matter owner",
            "PRIVATE_STANDARD_BRANCH_ZERO",
            "4277 matter-interface descent plus 4186 same-coframe zero law",
            "reopens if hidden matter frame/source-only metric is reintroduced",
        ),
        (
            "RC4279_1_delta_kappa",
            "delta_kappa",
            "source-coupling drift",
            "PRIVATE_STANDARD_BRANCH_ZERO",
            "4186 topological kappa lock plus Hilbert source-measure descent; 4267 fixed coefficient branch",
            "reopens if kappa_eff depends on hidden/local memory fields",
        ),
        (
            "RC4279_2_Kperp_cT_static",
            "Kperp/c_T_static",
            "extra static TT/torsion local force",
            "PRIVATE_COMPACT_SELECTOR_ZERO",
            "4234 decomposes Kperp into EH TT, vertical, boundary, or absent extra source",
            "global no-independent-TT-source parent clause remains unsigned",
        ),
        (
            "RC4279_3_c_bdy",
            "c_bdy",
            "unrouted boundary/edge charge",
            "PRIVATE_COMPACT_COLLAR_ROUTED",
            "4268 fixed no-flux collar and 4235 private boundary routing",
            "open/radiative/global boundary flux still requires source-backed bound",
        ),
        (
            "RC4279_4_cGamma",
            "c_Gamma",
            "local memory/Gamma/Khat coupling",
            "SOLE_PRIVATE_LOCAL_SURVIVOR",
            "4187/4235 leave P_loc Gamma_mem, P_loc J_res, D_t Xi_0 and grad_perp Xi_0 open",
            "must derive parent memory support/no-hair or fill profile/AJ coefficients",
        ),
        (
            "RC4279_5_cR2",
            "c_R2_or_M_R",
            "curvature-squared finite-range tail",
            "RETAINED_FINITE_RANGE_BOUND_ROUTE",
            "4185/4278 map it to R10/PPN/orbital finite-range corrections",
            "needs heavy mass/scale law or source-backed local bound row",
        ),
        (
            "RC4279_6_Lambda",
            "Lambda_eff_local",
            "local vacuum/tidal residual",
            "RETAINED_LOCAL_TIDAL_BOUND_ROUTE",
            "4278 keeps Lambda_eff as residual in the weak-field operator",
            "needs local scale separation or cosmology-calibrated local bound",
        ),
        (
            "RC4279_7_spin_torsion",
            "c_T_spin",
            "spin/torsion contact or non-static torsion mode",
            "RETAINED_SPIN_TORSION_BOUND_ROUTE",
            "4234 kills extra static Kperp force, not every possible spin/torsion operator",
            "needs spinless algebraic elimination proof or spin-torsion bound row",
        ),
    ]
    return [
        {
            **common(),
            "classifier_id": classifier_id,
            "coefficient": coefficient,
            "meaning": meaning,
            "status": status,
            "evidence": evidence,
            "reopen_condition": reopen_condition,
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
        for classifier_id, coefficient, meaning, status, evidence, reopen_condition in raw
    ]


def derived_zero_rows() -> List[Dict[str, str]]:
    raw = [
        (
            "ZERO4279_0_cD",
            "c_D",
            "0",
            FORMAL / "202-PPC4161-same-coframe-source-memory-zero-law.md",
            "single observed coframe + Hilbert source descent + Maxwell-Hodge owner",
            "private selector only",
        ),
        (
            "ZERO4279_1_delta_kappa",
            "delta_kappa",
            "0",
            FORMAL / "202-PPC4161-same-coframe-source-memory-zero-law.md",
            "topological kappa lock + Hilbert source-measure descent",
            "numeric G not predicted",
        ),
        (
            "ZERO4279_2_Kperp_static",
            "Kperp/c_T_static",
            "0",
            FORMAL / "250-PPC4161-Kperp-EH-coframe-identity-proof-or-independent-tensor-source-row.md",
            "EH TT already counted, vertical Dq=0, boundary routed, no independent local TT source in private selector",
            "public no-independent-TT-source remains unsigned",
        ),
        (
            "ZERO4279_3_cPoynt_extra",
            "c_Poynt_extra",
            "0",
            FORMAL / "275-PPC4161-EM-Hodge-component-zero-or-residual-vector.md",
            "Poynting flux is T_EM^0i Hilbert flux, not a second background source",
            "visible Maxwell-Hodge branch only",
        ),
        (
            "ZERO4279_4_c_bdy_compact",
            "c_bdy_compact_collar",
            "0",
            FORMAL / "284-PPC4161-Dq-boundary-projector-fixed-collar-or-boundary-residual-bound.md",
            "fixed compact no-flux collar/projector branch",
            "open boundary/radiation still retained",
        ),
    ]
    return [
        {
            **common(),
            "zero_id": zero_id,
            "coefficient": coefficient,
            "value": value,
            "source_path": str(source_path),
            "derivation_basis": derivation_basis,
            "scope": scope,
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
        for zero_id, coefficient, value, source_path, derivation_basis, scope in raw
    ]


def survivor_bound_rows() -> List[Dict[str, str]]:
    raw = [
        (
            "SURV4279_0_cGamma_Gdot",
            "c_Gamma",
            "Gdot_over_G",
            "|c_Gamma D_t Xi_0| <= 2.42e-14 yr^-1",
            "4188/4189/4235",
            "D_t Xi_0 or A_J source coefficient",
        ),
        (
            "SURV4279_1_cGamma_xi",
            "c_Gamma",
            "PPN_xi_preferred_location",
            "|c_Gamma L_loc grad_perp Xi_0| <= 4e-9",
            "4189/4235",
            "grad_perp Xi_0 profile coefficient",
        ),
        (
            "SURV4279_2_cGamma_alpha3",
            "c_Gamma",
            "PPN_alpha3_vector",
            "|c_Gamma profile_alpha3| <= 4e-20",
            "4235/4236",
            "profile_alpha3 coefficient",
        ),
        (
            "SURV4279_3_cGamma_AJ",
            "c_Gamma",
            "strong_local_window_AJ",
            "A_J,eff_private <= 0.1678939074330212*(mu_Xi T_res)/|c_Gamma|",
            "4236",
            "A_src, A_lap, A_drift, T_res/tau_L, c_Gamma",
        ),
        (
            "SURV4279_4_cR2",
            "c_R2_or_M_R",
            "R10_PPN_orbital_finite_range",
            "require M_R large or |c_R2 profile_a| <= B_a for each local arena",
            "4278 residual map",
            "finite-range projection profile and source-backed alpha(lambda)/PPN/orbital row",
        ),
        (
            "SURV4279_5_Lambda",
            "Lambda_eff_local",
            "local_vacuum_tidal",
            "|Lambda_eff| L_local^2 << local metric residual budget",
            "4278 residual map",
            "local scale L_local and calibrated Lambda_eff/source path",
        ),
        (
            "SURV4279_6_spin_torsion",
            "c_T_spin",
            "spin_torsion_clock_or_orbital",
            "spin/torsion channel must be algebraically eliminated or bounded by arena response",
            "200/250 split",
            "spin source support, torsion mass/coupling, or spinless branch certificate",
        ),
    ]
    return [
        {
            **common(),
            "survivor_id": survivor_id,
            "coefficient": coefficient,
            "arena": arena,
            "bound_or_requirement": bound_or_requirement,
            "source_basis": source_basis,
            "missing_input": missing_input,
            "score_ready": "False",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
        for survivor_id, coefficient, arena, bound_or_requirement, source_basis, missing_input in raw
    ]


def cgamma_target_rows() -> List[Dict[str, str]]:
    raw = [
        ("CGT4279_0_Gdot", "C_Gamma_Gdot", "2.42e-14", "yr^-1", "Gdot_over_G", "D_t Xi_0"),
        ("CGT4279_1_xi", "C_Gamma_xi", "4e-9", "dimensionless", "PPN_xi", "L_loc grad_perp Xi_0"),
        ("CGT4279_2_WEP", "C_Gamma_WEP", "6.991812087098392e-15", "dimensionless", "eta_TiPt", "composition/source projection"),
        ("CGT4279_3_clock", "C_Gamma_clock", "5.15e-05", "dimensionless", "redshift_violation_alpha", "clock readout projection"),
        ("CGT4279_4_stress", "C_Gamma_stress", "1e-08", "dimensionless", "zeta3", "stress/source nonconservation projection"),
        ("CGT4279_5_vector", "C_Gamma_vector", "4e-20", "dimensionless", "alpha3", "preferred-frame/vector profile"),
        ("CGT4279_6_R10", "C_Gamma_R10", "1", "dimensionless", "alpha_Yukawa_at_lambda_38p6um_anchor_only", "finite-range profile; nonclaim until full curve"),
    ]
    return [
        {
            **common(),
            "target_id": target_id,
            "product": product,
            "bound_value": bound_value,
            "units": units,
            "arena_source_label": arena_source_label,
            "needed_profile": needed_profile,
            "source_path": str(FORMAL / "204-PPC4161-finite-cGamma-product-bound-law.md"),
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
        for target_id, product, bound_value, units, arena_source_label, needed_profile in raw
    ]


def em_stress_guard_rows() -> List[Dict[str, str]]:
    return [
        {
            **common(),
            "guard_id": "EM4279_0_poynting_once",
            "statement": "Poynting vector is EM Hilbert stress flux S_i=-T_EM(n,e_i), not an extra background source.",
            "closed_coefficient": "c_Poynt_extra=0",
            "open_residuals": "delta_w_EM;C_XF2;C_JQ;b_alpha;dlnlambda;b_marker;Delta_Hodge_EM;Delta_rad_Poynting;Delta_internal_exchange",
            "source_path": str(FORMAL / "275-PPC4161-EM-Hodge-component-zero-or-residual-vector.md"),
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
    ]


def decision_rows() -> List[Dict[str, str]]:
    raw = [
        (
            "DEC4279_0_vector_reduced",
            "Reduce the 4278 residual vector to a private-zero subset plus a survivor-bound pack.",
            "This prevents re-litigating c_D/delta_kappa/Kperp/Poynting every turn while keeping public claims false.",
            "focus next work on c_Gamma/AJ and finite-range rows",
        ),
        (
            "DEC4279_1_cGamma_priority",
            "Treat c_Gamma as the leading private local survivor.",
            "4234/4235 remove Kperp static force, leaving memory support/source/profile coefficients as the sharp bottleneck.",
            NEXT_TARGET,
        ),
        (
            "DEC4279_2_bound_not_claim",
            "Keep product bounds as target inequalities, not passes.",
            "c_Gamma, profile coefficients and AJ source terms are not parent-owned or sourced.",
            "fill A_src/A_lap/A_drift and profile rows before empirical scoring",
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
        for decision_id, decision, reason, next_action in raw
    ]


def firewall_rows() -> List[Dict[str, str]]:
    raw = [
        ("FW4279_0_private_zero_scope", "c_D, delta_kappa, Kperp/static c_T, c_bdy compact and c_Poynt_extra zeros are private/branch-local, not global parent claims."),
        ("FW4279_1_cGamma_not_small_by_vibes", "c_Gamma is not assumed small; only products with sourced profiles can be scored."),
        ("FW4279_2_no_R10_anchor_claim", "R10 anchor-only rows cannot be promoted to a full finite-range pass without a reviewed alpha(lambda) curve/projection."),
        ("FW4279_3_no_cross_channel_cancellation", "Residual coefficients cannot cancel each other unless a parent identity proves the cancellation before testing."),
        ("FW4279_4_no_numeric_G_prediction", "delta_kappa private zero prevents drift; it does not predict the numerical value of G."),
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
            "status_id": "STATUS4279",
            "current_status": "residual EFT vector reduced: c_D/delta_kappa/private Kperp-static/boundary/Poynting rows routed; c_Gamma plus c_R2/Lambda/spin-torsion finite rows remain",
            "local_gr_claim": "False",
            "newton_claim": "False",
            "ppn_claim": "False",
            "em_claim": "False",
            "next_best_target": NEXT_TARGET,
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
    ]


def next_target_rows() -> List[Dict[str, str]]:
    return [
        {
            **common(),
            "next_target": NEXT_TARGET,
            "why": "after the private-zero subset, the fastest route to a testable local branch is the cGamma memory equation/AJ/profile fill.",
            "success_condition": "derive D_t Xi_0=0 and grad_perp Xi_0=0, or source A_src/A_lap/A_drift, T_res/tau_L, c_Gamma and arena profile coefficients against the 4279 product budgets.",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
    ]


def append_claim() -> None:
    path = FORMAL / "02-claims-register.csv"
    text = read_text(path)
    if CLAIM_ID in text:
        return
    with path.open(newline="", encoding="utf-8") as handle:
        fieldnames = next(csv.reader(handle))
    row = {
        "claim_id": CLAIM_ID,
        "domain": "local_gr",
        "claim": (
            "4279 reduces the 4278 residual EFT vector into a private-zero subset and a survivor-bound pack. c_D and delta_kappa are zero inside the private selector; Kperp/static c_T is routed as EH/vertical/boundary/absent; compact c_bdy and extra Poynting source are routed. "
            "The main surviving local pressure is c_Gamma, with c_R2/M_R, Lambda_eff and spin/torsion finite rows retained."
        ),
        "current_evidence": (
            "4279 source register, residual classifier, derived-zero rows, survivor-bound rows, cGamma target table, EM stress guard, decision and firewall."
        ),
        "status": "private_residual_EFT_vector_reduced_cGamma_bound_pack_nonclaim",
        "next_test": "Derive the cGamma parent memory equation/stationarity profile or fill AJ/profile coefficients against the product budgets.",
        "key_risk": "Promoting private branch zeros to global parent claims, treating cGamma product bounds as cGamma values, or using R10 anchor rows as full finite-range evidence.",
    }
    with path.open("a", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writerow(row)


def append_unique_block(path: Path, marker: str, title: str, body: str) -> None:
    text = read_text(path)
    if marker in text:
        return
    path.write_text(text.rstrip() + f"\n\n## {title}\n\nMarker: `{marker}`\n\n{body.strip()}\n", encoding="utf-8")


def formal_doc() -> str:
    return f"""
# 295 - PPC4161 residual EFT coefficient zero or local test bound pack

Marker: `{MARKER}`

Branch: `{BRANCH}`

Decision: `{DECISION}`

## Result

4279 does not claim public local GR, PPN/R10 safety, clock/WEP/orbital validation, Maxwell completion, or a numerical prediction of `G`.

It reduces the 4278 residual vector from a flat list into two groups:

```text
private-zero / routed subset:
c_D, delta_kappa, Kperp/c_T_static, c_bdy_compact, c_Poynt_extra

survivor / bound subset:
c_Gamma, c_R2/M_R, Lambda_eff_local, c_T_spin
```

## Private-zero subset

Inside the private compact single-coframe selector:

```text
c_D = 0
```

because ordinary matter descends through the same observed coframe and Hilbert source.

Also:

```text
delta_kappa = 0
```

because the local branch uses the topological/fixed kappa lock plus Hilbert source-measure descent. This prevents local drift; it does not predict the numerical value of `G`.

The static extra tensor/torsion force is routed:

```text
K_perp = K_metric_TT + K_vertical + K_boundary + K_extra_source,
```

and in the private compact selector this gives no independent static local force.

For EM:

```text
S_i = -T_EM(n,e_i)
```

so Poynting is already the Maxwell-Hodge Hilbert stress flux, not a second background source. Thus:

```text
c_Poynt_extra = 0
```

unless a future parent action explicitly introduces a new source row.

## Survivor bound pack

The leading private local survivor is:

```text
c_Gamma.
```

Current hard product targets are:

```text
|c_Gamma D_t Xi_0| <= 2.42e-14 yr^-1,
|c_Gamma L_loc grad_perp Xi_0| <= 4e-9,
|c_Gamma profile_alpha3| <= 4e-20,
A_J,eff_private <= 0.1678939074330212*(mu_Xi T_res)/|c_Gamma|.
```

The missing cGamma inputs are now exact:

```text
A_src,
A_lap,
A_drift,
T_res/tau_L,
c_Gamma,
profile_a/J_a.
```

The remaining non-cGamma finite rows are:

```text
c_R2/M_R       finite-range curvature correction,
Lambda_eff     local vacuum/tidal residual,
c_T_spin       non-static spin/torsion contact channel.
```

## No-claim guard

These are not passes. They are target inequalities and conditional private zeros. Public promotion still needs parent signatures, heavy/screened scale laws, or source-backed projection rows with no cross-channel cancellation.

## Next target

`{NEXT_TARGET}` should attack the cGamma parent memory equation and fill or derive `A_src/A_lap/A_drift`, `T_res/tau_L`, `c_Gamma`, and the arena profile coefficients.
"""


def checkpoint_doc() -> str:
    return f"""
# 4279 - residual EFT coefficient zero or local test bound pack

Marker: `{MARKER}`

Decision: `{DECISION}`

4279 reduces the 4278 residual vector:

```text
private routed: c_D, delta_kappa, Kperp/c_T_static, c_bdy_compact, c_Poynt_extra
survivors: c_Gamma, c_R2/M_R, Lambda_eff_local, c_T_spin
```

The main next target is no longer vague local GR; it is:

```text
c_Gamma memory/AJ/profile ownership.
```
"""


def validation_rows(paths: Dict[str, Path]) -> List[Dict[str, str]]:
    sources = csv_rows(paths["sources"])
    classifier = csv_rows(paths["classifier"])
    zeros = csv_rows(paths["zeros"])
    survivors = csv_rows(paths["survivors"])
    cgamma = csv_rows(paths["cgamma_targets"])
    em_guard = csv_rows(paths["em_guard"])
    all_rows: Iterable[Dict[str, str]] = (
        sources
        + classifier
        + zeros
        + survivors
        + cgamma
        + em_guard
        + csv_rows(paths["decision"])
        + csv_rows(paths["firewall"])
        + csv_rows(paths["status"])
        + csv_rows(paths["next_target"])
    )
    validations = [
        ("VAL4279_0_sources_exist", all(row["exists"] == "True" for row in sources), "all source paths exist"),
        ("VAL4279_1_needles_found", all(row["required_text_found"] == "True" for row in sources), "all source needles found"),
        (
            "VAL4279_2_zero_subset",
            {"c_D", "delta_kappa", "Kperp/c_T_static", "c_Poynt_extra", "c_bdy_compact_collar"}.issubset({row.get("coefficient") for row in zeros}),
            "private zero/routed subset emitted",
        ),
        (
            "VAL4279_3_cGamma_survivor",
            any(row["coefficient"] == "c_Gamma" and row["status"] == "SOLE_PRIVATE_LOCAL_SURVIVOR" for row in classifier),
            "cGamma identified as leading private survivor",
        ),
        (
            "VAL4279_4_finite_survivors",
            {"c_R2_or_M_R", "Lambda_eff_local", "c_T_spin"}.issubset({row.get("coefficient") for row in classifier}),
            "non-cGamma finite residual branches retained",
        ),
        (
            "VAL4279_5_cGamma_targets",
            {"C_Gamma_Gdot", "C_Gamma_xi", "C_Gamma_vector"}.issubset({row.get("product") for row in cgamma})
            and any(row.get("target_id") == "CGT4279_5_vector" and row.get("bound_value") == "4e-20" for row in cgamma),
            "cGamma hard product targets emitted",
        ),
        (
            "VAL4279_6_AJ_target",
            any(row["survivor_id"] == "SURV4279_3_cGamma_AJ" and "A_src" in row["missing_input"] for row in survivors),
            "AJ source coefficient target emitted",
        ),
        (
            "VAL4279_7_EM_guard",
            any(row["guard_id"] == "EM4279_0_poynting_once" and row["closed_coefficient"] == "c_Poynt_extra=0" for row in em_guard),
            "Poynting once-only stress guard emitted",
        ),
        ("VAL4279_8_formal_doc", FORMAL_PATH.exists() and MARKER in read_text(FORMAL_PATH), "formal doc written"),
        ("VAL4279_9_checkpoint_doc", DOC_PATH.exists() and DECISION in read_text(DOC_PATH), "checkpoint doc written"),
        ("VAL4279_10_claim_row", f"{CLAIM_ID}," in read_text(FORMAL / "02-claims-register.csv"), "claim register row added"),
        ("VAL4279_11_no_claim_rows", all(row.get("claim_allowed", "False") == "False" and row.get("valid_for_claim", "False") == "False" for row in all_rows), "all rows remain nonclaim"),
    ]
    for name, path in paths.items():
        validations.append((f"VAL4279_csv_{name}", bool(csv_rows(path)), f"{path.name} parses"))
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
        "sources": SOURCE_DIR / "P8_Y5_R2FR_4279_SOURCE_REGISTER.csv",
        "classifier": SOURCE_DIR / "P8_Y5_R2FR_4279_RESIDUAL_CLASSIFIER.csv",
        "zeros": SOURCE_DIR / "P8_Y5_R2FR_4279_DERIVED_ZERO_SUBSET.csv",
        "survivors": SOURCE_DIR / "P8_Y5_R2FR_4279_SURVIVOR_BOUND_PACK.csv",
        "cgamma_targets": SOURCE_DIR / "P8_Y5_R2FR_4279_CGAMMA_FULL_BUDGET_TARGETS.csv",
        "em_guard": SOURCE_DIR / "P8_Y5_R2FR_4279_EM_STRESS_GUARD.csv",
        "decision": SOURCE_DIR / "P8_Y5_R2FR_4279_DECISION.csv",
        "firewall": SOURCE_DIR / "P8_Y5_R2FR_4279_CLAIM_FIREWALL.csv",
        "status": SOURCE_DIR / "P8_Y5_R2FR_4279_STATUS.csv",
        "next_target": SOURCE_DIR / "P8_Y5_R2FR_4279_NEXT_TARGET.csv",
    }
    write_csv(paths["sources"], source_rows())
    write_csv(paths["classifier"], residual_classifier_rows())
    write_csv(paths["zeros"], derived_zero_rows())
    write_csv(paths["survivors"], survivor_bound_rows())
    write_csv(paths["cgamma_targets"], cgamma_target_rows())
    write_csv(paths["em_guard"], em_stress_guard_rows())
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
        "PPC4161 4279 residual EFT vector reduction",
        "4279 reduces the 4278 residual EFT vector into a private-routed subset (`c_D`, `delta_kappa`, `Kperp/c_T_static`, `c_bdy_compact`, `c_Poynt_extra`) and a survivor-bound subset (`c_Gamma`, `c_R2/M_R`, `Lambda_eff_local`, `c_T_spin`). The leading next target is `c_Gamma` memory/AJ/profile ownership, with hard product budgets from the 4188/4189/4235/4236 chain.",
    )
    append_unique_block(
        FORMAL / "180-PPC4161-private-local-packet-integration.md",
        PACKET_MARKER,
        "4279 packet residual EFT bound pack",
        "Packet update: the residual vector is no longer flat. Private branch zeros are quarantined; the active local survivor is `c_Gamma` plus finite-range/tidal/spin-torsion bound rows. No public claim is made.",
    )
    write_csv(VALIDATION_PATH, validation_rows(paths))
    failed = [row for row in csv_rows(VALIDATION_PATH) if row["passed"] != "True"]
    print(f"{CHECKPOINT}: wrote {len(paths)} csv artifacts plus validation")
    print(f"{CHECKPOINT}: validation rows={len(csv_rows(VALIDATION_PATH))} failed={len(failed)}")
    print(f"{CHECKPOINT}: decision={DECISION}")
    if failed:
        for row in failed:
            print(f"FAILED {row['check_id']}: {row['description']}")
        raise SystemExit(1)


if __name__ == "__main__":
    main()

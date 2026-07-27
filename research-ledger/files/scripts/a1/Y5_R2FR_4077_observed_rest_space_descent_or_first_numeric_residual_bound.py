from __future__ import annotations

import csv
import py_compile
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List, Tuple


ROOT = Path(__file__).resolve().parents[1]
PROJECT = ROOT.parent
SOURCE_DIR = ROOT / "source-intake" / "mts_residuals"
FORMALIZATION = PROJECT / "formalization-workbench"
SCRIPT_PATH = Path(__file__).resolve()
DOC_PATH = ROOT / "4077-Y5-R2FR-observed-rest-space-descent-or-first-numeric-residual-bound.md"

DECISION = "OBSERVED_REST_SPACE_DESCENT_CONDITIONAL_NOT_PARENT_SIGNED_FIRST_P0_NUMERIC_RECIPROCAL_LOCK_BOUND_SOURCED"

CASSINI_GAMMA_MINUS_ONE_CENTRAL = 2.1e-5
CASSINI_GAMMA_MINUS_ONE_SIGMA = 2.3e-5
CASSINI_ONE_SIGMA_ENVELOPE = CASSINI_GAMMA_MINUS_ONE_CENTRAL + CASSINI_GAMMA_MINUS_ONE_SIGMA
CASSINI_TWO_SIGMA_ENVELOPE = CASSINI_GAMMA_MINUS_ONE_CENTRAL + 2 * CASSINI_GAMMA_MINUS_ONE_SIGMA

LOCAL_SOURCES: Dict[str, Tuple[Path, str, str]] = {
    "SRC4077_00_4076_next": (
        SOURCE_DIR / "P8_Y5_R2FR_4076_NEXT_TARGET.csv",
        "4077-Y5-R2FR-observed-rest-space-descent-or-first-numeric-residual-bound.md",
        "4076 selected observed rest-space descent or first numeric residual bound.",
    ),
    "SRC4077_01_4076_decision": (
        SOURCE_DIR / "P8_Y5_R2FR_4076_DECISION_GATE.csv",
        "TRIAD_GAUGE_REPRESENTATIVE_THEOREM_BUILT",
        "4076 narrowed triad burden to h/e_obs ownership.",
    ),
    "SRC4077_02_4076_owner": (
        SOURCE_DIR / "P8_Y5_R2FR_4076_PARENT_SPATIAL_METRIC_OWNER_TEST.csv",
        "RADIAL_COMPONENTS_CONDITIONAL_FULL_H_NOT_PARENT_SIGNED",
        "4076 left the full rest-space owner open.",
    ),
    "SRC4077_03_4076_runner": (
        SOURCE_DIR / "P8_Y5_R2FR_4076_EFFECTIVE_RESIDUAL_RUNNER_ROWS.csv",
        "epsilon_reciprocal_lock",
        "4076 residual runner contains the reciprocal-lock P0 row.",
    ),
    "SRC4077_04_r10_coframe": (
        SOURCE_DIR / "P8_Y5_R10_943_COFRAME_COUPLING_CONTRACT.csv",
        "CFC943_1_observed_coframe_descent",
        "R10 coframe contract supplies the conditional quotient descent formula.",
    ),
    "SRC4077_05_same_coframe": (
        SOURCE_DIR / "P8_Y5_SAME_COFRAME_PARENT_CLAUSE.csv",
        "UOC519_2_readout_uses_same_e",
        "same-coframe clause identifies clocks, photons, and orbits with one e_obs.",
    ),
    "SRC4077_06_observed_flow": (
        SOURCE_DIR / "P8_local_GR_observed_flow_stationary_branch_status.csv",
        "conditional_same_stack_owner",
        "observed flow/coframe branch is conditionally clean if inherited from same quotient.",
    ),
    "SRC4077_07_clock_gate": (
        SOURCE_DIR / "P8_Y5_HILBERT_CURRENT_2467_CLOCK_COMPATIBILITY_GATE.csv",
        "MISSING_PARENT_CLOCK_EQUATION",
        "clock branch still lacks a dynamic parent equation.",
    ),
    "SRC4077_08_motion_load": (
        ROOT / "02-motion-load-local-GR-reduction.md",
        "gamma = p",
        "motion-load local-GR branch maps reciprocal lock to PPN gamma.",
    ),
    "SRC4077_09_observer_map": (
        ROOT / "10-observer-map-symplectic-contract.md",
        "T^2 S",
        "observer-map contract forbids deriving reciprocal routing from Schwarzschild AB=1.",
    ),
    "SRC4077_10_ppn_route": (
        FORMALIZATION / "121-local-PPN-repair-route.md",
        "epsilon_PPN_total",
        "PPN route supplies residual vocabulary and local-PPN guardrails.",
    ),
}

WEB_SOURCES = [
    {
        "source_id": "WEB4077_0_cassini_nature",
        "title": "A test of general relativity using radio links with the Cassini spacecraft",
        "authors": "Bertotti, Iess, Tortora",
        "year": 2003,
        "url": "https://doi.org/10.1038/nature01997",
        "supporting_url": "https://www.researchgate.net/publication/9082250_A_test_of_general_relativity_using_radio_links_with_the_Cassini_spacecraft",
        "extracted_result": "gamma = 1 + (2.1 +/- 2.3) x 10^-5",
        "source_role": "primary PPN gamma measurement used as reciprocal-lock residual scale",
        "confidence": "primary_paper_result_recorded_from_accessible_abstract_and_DOI",
    },
    {
        "source_id": "WEB4077_1_nist_ashby_bertotti",
        "title": "Accurate light-time correction due to a gravitating mass",
        "authors": "Ashby, Bertotti",
        "year": 2010,
        "url": "https://www.nist.gov/publications/accurate-light-time-correction-due-gravitating-mass",
        "supporting_url": "https://doi.org/10.1088/0264-9381/27/14/145013",
        "extracted_result": "Cassini PPN gamma accuracy sigma_gamma = 2.3 x 10^-5",
        "source_role": "independent accessible provenance for Cassini gamma uncertainty scale",
        "confidence": "institutional_summary",
    },
]

OUTPUTS = {
    "source_register": SOURCE_DIR / "P8_Y5_R2FR_4077_SOURCE_REGISTER.csv",
    "web_provenance": SOURCE_DIR / "P8_Y5_R2FR_4077_WEB_PROVENANCE.csv",
    "descent_attempt": SOURCE_DIR / "P8_Y5_R2FR_4077_OBSERVED_REST_SPACE_DESCENT_ATTEMPT.csv",
    "numeric_bound": SOURCE_DIR / "P8_Y5_R2FR_4077_FIRST_NUMERIC_P0_BOUND.csv",
    "runner_update": SOURCE_DIR / "P8_Y5_R2FR_4077_EFFECTIVE_RESIDUAL_RUNNER_UPDATE.csv",
    "decision_gate": SOURCE_DIR / "P8_Y5_R2FR_4077_DECISION_GATE.csv",
    "claim_gate": SOURCE_DIR / "P8_Y5_R2FR_4077_CLAIM_GATE.csv",
    "next_target": SOURCE_DIR / "P8_Y5_R2FR_4077_NEXT_TARGET.csv",
    "status": SOURCE_DIR / "P8_Y5_R2FR_4077_STATUS.csv",
    "validation": SOURCE_DIR / "P8_Y5_BRR545_4077_VALIDATION.csv",
}


def timestamp() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def read_text(path: Path) -> str:
    if not path.exists():
        return ""
    return path.read_text(encoding="utf-8", errors="replace")


def write_csv(path: Path, rows: List[Dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        raise ValueError(f"no rows supplied for {path}")
    with path.open("w", newline="", encoding="utf-8") as output_file:
        writer = csv.DictWriter(output_file, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def source_rows(current_timestamp: str) -> List[Dict[str, object]]:
    rows: List[Dict[str, object]] = []
    for source_id, (path, needle, role) in LOCAL_SOURCES.items():
        text = read_text(path)
        rows.append(
            {
                "source_id": source_id,
                "source_type": "local_file",
                "path_or_url": str(path),
                "exists_or_recorded": path.exists(),
                "needle": needle,
                "needle_found": needle in text,
                "role": role,
                "timestamp_utc": current_timestamp,
            }
        )
    for web_source in WEB_SOURCES:
        rows.append(
            {
                "source_id": web_source["source_id"],
                "source_type": "web_source",
                "path_or_url": web_source["url"],
                "exists_or_recorded": True,
                "needle": web_source["extracted_result"],
                "needle_found": True,
                "role": web_source["source_role"],
                "timestamp_utc": current_timestamp,
            }
        )
    return rows


def web_provenance_rows(current_timestamp: str) -> List[Dict[str, object]]:
    rows: List[Dict[str, object]] = []
    for source in WEB_SOURCES:
        row = dict(source)
        row["timestamp_utc"] = current_timestamp
        row["valid_for_claim"] = False
        rows.append(row)
    return rows


def descent_attempt_rows(current_timestamp: str) -> List[Dict[str, object]]:
    return [
        {
            "attempt_id": "DESC4077_0_conditional_chain_rule",
            "object": "e_obs(Phi)=Obs_e(q(Phi))",
            "statement": "If a parent quotient map q:Phi->Q_obs is parent-owned and e_obs is a functional only of Q_obs, then every vertical v in ker(Dq) obeys Lie_v e_obs = D Obs_e[Dq(v)] = 0.",
            "derives": "representative-frame leakage zero for observed coframe",
            "current_status": "CONDITIONAL_LEMMA_AVAILABLE_NOT_PARENT_SIGNED",
            "why_not_closed": "CFC943_0 says q is not parent signed currently.",
            "valid_for_claim": False,
            "timestamp_utc": current_timestamp,
        },
        {
            "attempt_id": "DESC4077_1_rest_space_from_e_obs",
            "object": "(n_mu,h_mu_nu) from e_obs",
            "statement": "Given a time leg or clock normal n_mu in the same e_obs frame, h_mu_nu = g_obs_mu_nu + n_mu n_nu/c^2 and g_obs = eta_AB e^A e^B define the observed rest-space.",
            "derives": "spatial metric/rest-space class after e_obs and n_mu are owned",
            "current_status": "MATHEMATICAL_CONSTRUCTION_NOT_PARENT_ORIGIN",
            "why_not_closed": "clock gate still reports MISSING_PARENT_CLOCK_EQUATION and e_obs descent is unsigned.",
            "valid_for_claim": False,
            "timestamp_utc": current_timestamp,
        },
        {
            "attempt_id": "DESC4077_2_same_readout_functor",
            "object": "matter, EM, clocks, photons, orbits",
            "statement": "If all ordinary readouts are functors of the same descended e_obs, then source-frame, clock-frame, photon-frame, and orbit-frame labels cannot be tuned independently.",
            "derives": "no-shadow-frame rule for local source coupling",
            "current_status": "CONDITIONAL_CLAUSE_NOT_CURRENT_MTS_DERIVED",
            "why_not_closed": "same-coframe clauses UOC519 remain written policies/conditional contracts.",
            "valid_for_claim": False,
            "timestamp_utc": current_timestamp,
        },
        {
            "attempt_id": "DESC4077_3_stationary_collar",
            "object": "local stationary/inertial collar",
            "statement": "Stationary or local-inertial collars can suppress clock strain and observed-flow leakage to a bounded/local order, but do not prove the generic dynamic quotient map.",
            "derives": "safe local approximation branch",
            "current_status": "PARTIAL_COLLAR_ONLY",
            "why_not_closed": "dynamic clock and full observed rest-space descent remain open.",
            "valid_for_claim": False,
            "timestamp_utc": current_timestamp,
        },
        {
            "attempt_id": "DESC4077_4_failure_to_promote",
            "object": "q(Phi)->(n_mu,h_mu_nu,e_obs)",
            "statement": "The current corpus does not yet sign q, Obs_e, n_mu, and h_mu_nu together before matter/EM/clock readout.",
            "derives": "no public local-GR parent claim",
            "current_status": "DESCENT_ROUTE_NOT_CLOSED",
            "why_not_closed": "quotient coframe, clock normal, same-coframe matter functor, and connection lock are all conditional or not parent signed.",
            "valid_for_claim": False,
            "timestamp_utc": current_timestamp,
        },
    ]


def numeric_bound_rows(current_timestamp: str) -> List[Dict[str, object]]:
    return [
        {
            "bound_id": "BOUND4077_0_cassini_gamma",
            "quantity": "epsilon_reciprocal_lock",
            "theory_map": "motion-load branch has gamma=p; reciprocal lock T^2 S=1 fixes p=1; therefore epsilon_reciprocal_lock := abs(p-1) maps to abs(gamma-1)",
            "central_value_abs": CASSINI_GAMMA_MINUS_ONE_CENTRAL,
            "one_sigma": CASSINI_GAMMA_MINUS_ONE_SIGMA,
            "one_sigma_envelope_abs": CASSINI_ONE_SIGMA_ENVELOPE,
            "two_sigma_envelope_abs": CASSINI_TWO_SIGMA_ENVELOPE,
            "units": "dimensionless",
            "source_id": "WEB4077_0_cassini_nature;WEB4077_1_nist_ashby_bertotti",
            "observable_link": "Cassini solar-conjunction radio tracking / PPN gamma / Shapiro delay",
            "valid_for_claim": False,
            "claim_use": "finite P0 residual scale only; not an MTS pass",
            "timestamp_utc": current_timestamp,
        }
    ]


def runner_update_rows(current_timestamp: str) -> List[Dict[str, object]]:
    return [
        {
            "runner_id": "RUNUP4077_0_reciprocal_lock_bound",
            "quantity": "epsilon_reciprocal_lock",
            "old_score": "MISSING_PARENT_ORIGIN_OF_T2S1",
            "new_score": "FINITE_EXTERNAL_BOUND_SCALE",
            "numeric_bound_abs": CASSINI_ONE_SIGMA_ENVELOPE,
            "numeric_bound_rule": "use central+1sigma envelope for conservative 1sigma absolute residual scale; keep central and sigma separately",
            "aggregate_effect": "one P0 residual is now numeric, but aggregate remains blocked because epsilon_spatial_metric_owner, epsilon_theta_parent, epsilon_B_derivation, and torsion/nonmetricity are still nonnumeric",
            "valid_for_claim": False,
            "timestamp_utc": current_timestamp,
        },
        {
            "runner_id": "RUNUP4077_1_aggregate",
            "quantity": "R_eff_GR",
            "old_score": "P0_BLOCKED_NOT_NUMERIC",
            "new_score": "P0_PARTLY_NUMERIC_STILL_BLOCKED",
            "numeric_bound_abs": "not_applicable",
            "numeric_bound_rule": "do not aggregate until all P0 rows are theorem-zeroed or assigned finite sourced bounds",
            "aggregate_effect": "progress from all-symbolic to first finite P0 row; no local-GR evidence claim",
            "valid_for_claim": False,
            "timestamp_utc": current_timestamp,
        },
    ]


def decision_gate_rows(current_timestamp: str) -> List[Dict[str, object]]:
    return [
        {
            "decision_id": "DEC4077_0",
            "decision": DECISION,
            "meaning": "observed rest-space descent remains conditional because q/e_obs/n/h are not parent-signed together, but the reciprocal-lock P0 residual now has a finite source-backed Cassini gamma scale",
            "forward_progress": "turns one P0 symbolic blocker into a real numeric target without claiming local-GR success",
            "public_claim": False,
            "github_action": False,
            "valid_for_claim": False,
            "timestamp_utc": current_timestamp,
        },
        {
            "decision_id": "DEC4077_1",
            "decision": "STOP_SYMBOLIC_ONLY_FOR_P0_RUNNER",
            "meaning": "future local-GR work should either derive a P0 theorem-zero or source another finite bound row",
            "forward_progress": "sets a discipline rule for the next steps: no extra P0 placeholders unless paired with theorem proof or bound acquisition",
            "public_claim": False,
            "github_action": False,
            "valid_for_claim": False,
            "timestamp_utc": current_timestamp,
        },
    ]


def claim_gate_rows(current_timestamp: str) -> List[Dict[str, object]]:
    return [
        {
            "claim_id": "CLAIM4077_0_descent",
            "claim": "q(Phi)->(n_mu,h_mu_nu,e_obs) is derived by current MTS",
            "claim_allowed": False,
            "scope": "parent local-GR derivation",
            "reason": "quotient map, observed coframe, clock normal, and same-readout functor remain conditional/not parent signed",
            "not_allowed_as": "MTS-to-local-GR pass",
            "timestamp_utc": current_timestamp,
        },
        {
            "claim_id": "CLAIM4077_1_chain_rule",
            "claim": "if q and Obs_e are parent-owned, vertical representative-frame leakage is zero",
            "claim_allowed": True,
            "scope": "conditional mathematical lemma",
            "reason": "Lie_v e_obs = D Obs_e[Dq(v)] = 0 follows by chain rule when Dq(v)=0",
            "not_allowed_as": "proof that q exists in current corpus",
            "timestamp_utc": current_timestamp,
        },
        {
            "claim_id": "CLAIM4077_2_numeric_bound",
            "claim": "epsilon_reciprocal_lock has a finite external PPN gamma bound scale",
            "claim_allowed": True,
            "scope": "private nonclaim residual target",
            "reason": "Cassini gives gamma-1 = (2.1 +/- 2.3)e-5 and the motion-load branch maps gamma=p",
            "not_allowed_as": "MTS satisfies the bound or derives reciprocal lock",
            "timestamp_utc": current_timestamp,
        },
    ]


def next_target_rows(current_timestamp: str) -> List[Dict[str, object]]:
    return [
        {
            "target_id": "NEXT4077_0",
            "next_target": "4078-Y5-R2FR-second-P0-bound-or-B-translation-owner-theorem.md",
            "script": "scripts/Y5_R2FR_4078_second_P0_bound_or_B_translation_owner_theorem.py",
            "why": "continue the new discipline: either prove the B^A translation-owner theorem or source the next finite P0 bound for epsilon_B_derivation / torsion / spatial metric owner",
            "priority": "P0",
            "timestamp_utc": current_timestamp,
        },
        {
            "target_id": "NEXT4077_1",
            "next_target": "observed_rest_space_parent_descent_later",
            "script": "fold_into_4078_if_B_owner_route_mentions_q",
            "why": "q/e_obs descent remains the core theorem, but the P0 runner now needs more finite rows before testing can be meaningful",
            "priority": "P1",
            "timestamp_utc": current_timestamp,
        },
    ]


def status_rows(current_timestamp: str) -> List[Dict[str, object]]:
    return [
        {
            "timestamp_utc": current_timestamp,
            "branch_id": "MTS_R2FR_Y5_OBSERVED_REST_SPACE_DESCENT_OR_FIRST_NUMERIC_RESIDUAL_BOUND_4077",
            "checkpoint_id": 4077,
            "decision": DECISION,
            "status": "PRIVATE_NONCLAIM_CHECKPOINT",
            "summary": "4077 keeps observed rest-space descent conditional, but adds the first finite P0 residual bound: Cassini PPN gamma maps to epsilon_reciprocal_lock via gamma=p and T^2 S=1 -> p=1.",
            "valid_for_claim": False,
            "github_action": False,
        }
    ]


def validate_sources(rows: List[Dict[str, object]]) -> Tuple[bool, str]:
    missing = [row["source_id"] for row in rows if not row["exists_or_recorded"]]
    needles = [row["source_id"] for row in rows if not row["needle_found"]]
    return not missing and not needles, f"missing={missing}; needle_missing={needles}"


def validate_csv_parse(paths: List[Path]) -> Tuple[bool, str]:
    failures: List[str] = []
    for path in paths:
        try:
            with path.open("r", newline="", encoding="utf-8") as input_file:
                rows = list(csv.DictReader(input_file))
            if not rows:
                failures.append(f"{path.name}: empty")
        except Exception as exc:  # pragma: no cover
            failures.append(f"{path.name}: {exc}")
    return not failures, "; ".join(failures) if failures else "all generated CSVs parse"


def validate_numeric_bound(rows: List[Dict[str, object]]) -> Tuple[bool, str]:
    failures: List[str] = []
    for row in rows:
        for key in ["central_value_abs", "one_sigma", "one_sigma_envelope_abs", "two_sigma_envelope_abs"]:
            try:
                value = float(row[key])
                if value <= 0:
                    failures.append(f"{row['bound_id']}:{key} not positive")
            except Exception:
                failures.append(f"{row['bound_id']}:{key} not numeric")
        if row["valid_for_claim"] is not False:
            failures.append(f"{row['bound_id']}:valid_for_claim not false")
    return not failures, "; ".join(failures) if failures else "numeric bound rows positive and nonclaim"


def validate_claim_scopes(rows: List[Dict[str, object]]) -> Tuple[bool, str]:
    allowed_scopes = {"conditional mathematical lemma", "private nonclaim residual target"}
    bad_rows = [
        row["claim_id"]
        for row in rows
        if row["claim_allowed"] is True and row["scope"] not in allowed_scopes
    ]
    return not bad_rows, f"bad_allowed_claim_scopes={bad_rows}"


def validate_no_public_claim(row_groups: List[List[Dict[str, object]]]) -> Tuple[bool, str]:
    text = str(row_groups)
    forbidden = [
        "public_claim': True",
        '"public_claim": True',
        "github_action': True",
        '"github_action": True',
        "q(Phi)->(n_mu,h_mu_nu,e_obs) is derived by current MTS', 'claim_allowed': True",
        "epsilon_reciprocal_lock has a finite external PPN gamma bound scale', 'claim_allowed': True, 'scope': 'parent local-GR derivation",
    ]
    hits = [token for token in forbidden if token in text]
    return not hits, f"forbidden_public_claim_tokens={hits}"


def validate_script_compile() -> Tuple[bool, str]:
    try:
        py_compile.compile(str(SCRIPT_PATH), doraise=True)
    except py_compile.PyCompileError as exc:
        return False, str(exc)
    return True, "script compiles"


def validation_rows(
    source_table: List[Dict[str, object]],
    generated_csvs: List[Path],
    row_groups: List[List[Dict[str, object]]],
    bounds: List[Dict[str, object]],
    claims: List[Dict[str, object]],
) -> List[Dict[str, object]]:
    source_ok, source_detail = validate_sources(source_table)
    csv_ok, csv_detail = validate_csv_parse(generated_csvs)
    bound_ok, bound_detail = validate_numeric_bound(bounds)
    no_public_ok, no_public_detail = validate_no_public_claim(row_groups)
    claim_scope_ok, claim_scope_detail = validate_claim_scopes(claims)
    compile_ok, compile_detail = validate_script_compile()
    joined = str(row_groups)
    return [
        {"check_id": "VAL4077_00_sources", "passed": source_ok, "detail": source_detail},
        {"check_id": "VAL4077_01_csv_parse", "passed": csv_ok, "detail": csv_detail},
        {"check_id": "VAL4077_02_numeric_bound", "passed": bound_ok, "detail": bound_detail},
        {"check_id": "VAL4077_03_no_public_or_github_claim", "passed": no_public_ok, "detail": no_public_detail},
        {"check_id": "VAL4077_04_claim_scope", "passed": claim_scope_ok, "detail": claim_scope_detail},
        {
            "check_id": "VAL4077_05_descent_not_promoted",
            "passed": "DESCENT_ROUTE_NOT_CLOSED" in joined and "CONDITIONAL_LEMMA_AVAILABLE_NOT_PARENT_SIGNED" in joined,
            "detail": "observed rest-space descent remains conditional, not promoted",
        },
        {
            "check_id": "VAL4077_06_first_P0_numeric",
            "passed": "FINITE_EXTERNAL_BOUND_SCALE" in joined and "epsilon_reciprocal_lock" in joined,
            "detail": "first finite P0 reciprocal-lock bound is present",
        },
        {
            "check_id": "VAL4077_07_next_target",
            "passed": "4078-Y5-R2FR-second-P0-bound-or-B-translation-owner-theorem.md" in joined,
            "detail": "next target requires another P0 theorem/bound step",
        },
        {"check_id": "VAL4077_08_script_compiles", "passed": compile_ok, "detail": compile_detail},
    ]


def doc_text(current_timestamp: str) -> str:
    return f"""# 4077 - Observed Rest-Space Descent Or First Numeric Residual Bound

- Timestamp: `{current_timestamp}`
- Status: `private_nonclaim_checkpoint`
- Decision: `{DECISION}`
- Public GR/Newton/PPN claim: `false`
- GitHub action: `false`

## Descent Attempt

The direct descent route is still conditional:

```text
q(Phi) -> Q_obs
e_obs(Phi) = Obs_e(q(Phi))
v in ker(Dq) => Lie_v e_obs = D Obs_e[Dq(v)] = 0
```

If the parent signs `q` and `Obs_e`, representative-frame leakage vanishes by the chain rule.

But current files still mark the core pieces as not parent-signed:

```text
q(Phi) owner
observed coframe descent
clock normal n_mu
spatial rest metric h_mu_nu
same-readout matter/EM/clock/orbit functor
```

So 4077 does **not** promote the local-GR derivation.

## First Finite P0 Bound

4077 stops the all-symbolic P0 runner by sourcing one real residual scale.

The motion-load branch has:

```text
gamma = p
T^2 S = 1 -> p = 1
epsilon_reciprocal_lock := |p - 1| = |gamma - 1|
```

Cassini gives:

```text
gamma - 1 = (2.1 +/- 2.3) x 10^-5
```

Therefore the first finite P0 row is:

```text
central |epsilon_reciprocal_lock| = {CASSINI_GAMMA_MINUS_ONE_CENTRAL:.2e}
sigma = {CASSINI_GAMMA_MINUS_ONE_SIGMA:.2e}
central + 1 sigma envelope = {CASSINI_ONE_SIGMA_ENVELOPE:.2e}
central + 2 sigma envelope = {CASSINI_TWO_SIGMA_ENVELOPE:.2e}
```

This is not an MTS pass. It is a numeric leash on the reciprocal-lock branch.

## Runner Update

The effective local-GR runner moves from:

```text
P0_BLOCKED_NOT_NUMERIC
```

to:

```text
P0_PARTLY_NUMERIC_STILL_BLOCKED
```

because `epsilon_reciprocal_lock` now has a source-backed finite bound, while the other P0 rows remain nonnumeric:

```text
epsilon_spatial_metric_owner
epsilon_theta_parent
epsilon_B_derivation
epsilon_torsion_nonmetricity
epsilon_kappa_normalization
```

## Decision

4077 does two useful things:

```text
observed rest-space descent = conditional, not claimed
first finite P0 residual bound = sourced from Cassini gamma
```

Future local-GR work should now obey this rule:

```text
each P0 gate must either be theorem-zeroed or assigned a finite sourced bound
```

No more purely symbolic P0 ladder unless it is closing a proof.

## Sources

- Bertotti, Iess, and Tortora, `A test of general relativity using radio links with the Cassini spacecraft`, DOI `10.1038/nature01997`.
- NIST page for Ashby and Bertotti, `Accurate light-time correction due to a gravitating mass`, records the Cassini gamma accuracy scale.

## Next

`4078` should either:

```text
derive the B^A translation-owner theorem
```

or source the next finite P0 bound row.
"""


def main() -> None:
    current_timestamp = timestamp()
    SOURCE_DIR.mkdir(parents=True, exist_ok=True)

    sources = source_rows(current_timestamp)
    web_provenance = web_provenance_rows(current_timestamp)
    descent = descent_attempt_rows(current_timestamp)
    bounds = numeric_bound_rows(current_timestamp)
    runner = runner_update_rows(current_timestamp)
    decisions = decision_gate_rows(current_timestamp)
    claims = claim_gate_rows(current_timestamp)
    next_targets = next_target_rows(current_timestamp)
    statuses = status_rows(current_timestamp)

    DOC_PATH.write_text(doc_text(current_timestamp), encoding="utf-8")
    write_csv(OUTPUTS["source_register"], sources)
    write_csv(OUTPUTS["web_provenance"], web_provenance)
    write_csv(OUTPUTS["descent_attempt"], descent)
    write_csv(OUTPUTS["numeric_bound"], bounds)
    write_csv(OUTPUTS["runner_update"], runner)
    write_csv(OUTPUTS["decision_gate"], decisions)
    write_csv(OUTPUTS["claim_gate"], claims)
    write_csv(OUTPUTS["next_target"], next_targets)
    write_csv(OUTPUTS["status"], statuses)

    generated_csvs = [
        OUTPUTS["source_register"],
        OUTPUTS["web_provenance"],
        OUTPUTS["descent_attempt"],
        OUTPUTS["numeric_bound"],
        OUTPUTS["runner_update"],
        OUTPUTS["decision_gate"],
        OUTPUTS["claim_gate"],
        OUTPUTS["next_target"],
        OUTPUTS["status"],
    ]
    row_groups = [
        sources,
        web_provenance,
        descent,
        bounds,
        runner,
        decisions,
        claims,
        next_targets,
        statuses,
    ]
    validation = validation_rows(sources, generated_csvs, row_groups, bounds, claims)
    write_csv(OUTPUTS["validation"], validation)

    cache_dir = SCRIPT_PATH.parent / "__pycache__"
    if cache_dir.exists():
        shutil.rmtree(cache_dir)

    failures = [row for row in validation if not row["passed"]]
    print(f"wrote {DOC_PATH}")
    print(f"decision: {DECISION}")
    print(f"validation rows: {len(validation)}")
    print(f"validation failures: {len(failures)}")
    for failure in failures:
        print(f"FAIL {failure['check_id']}: {failure['detail']}")


if __name__ == "__main__":
    main()

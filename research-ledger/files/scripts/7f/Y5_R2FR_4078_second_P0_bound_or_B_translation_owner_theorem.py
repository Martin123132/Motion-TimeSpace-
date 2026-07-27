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
DOC_PATH = ROOT / "4078-Y5-R2FR-second-P0-bound-or-B-translation-owner-theorem.md"

DECISION = "B_TRANSLATION_OWNER_THEOREM_CONDITIONAL_NOT_PARENT_SIGNED_SECOND_P0_PREFERRED_FRAME_BOUND_SOURCED"

ALPHA1_LLR_BOUND = 1.0e-4
ALPHA1_PULSAR_BOUND = 4.0e-5
ALPHA2_PULSAR_BOUND = 2.0e-9

LOCAL_SOURCES: Dict[str, Tuple[Path, str, str]] = {
    "SRC4078_00_4077_next": (
        SOURCE_DIR / "P8_Y5_R2FR_4077_NEXT_TARGET.csv",
        "4078-Y5-R2FR-second-P0-bound-or-B-translation-owner-theorem.md",
        "4077 selected the B-translation owner theorem or second P0 bound target.",
    ),
    "SRC4078_01_4077_decision": (
        SOURCE_DIR / "P8_Y5_R2FR_4077_DECISION_GATE.csv",
        "STOP_SYMBOLIC_ONLY_FOR_P0_RUNNER",
        "4077 established that new P0 work needs theorem-zero or finite bound rows.",
    ),
    "SRC4078_02_4077_runner": (
        SOURCE_DIR / "P8_Y5_R2FR_4077_EFFECTIVE_RESIDUAL_RUNNER_UPDATE.csv",
        "P0_PARTLY_NUMERIC_STILL_BLOCKED",
        "4077 runner has one numeric P0 row and remains blocked.",
    ),
    "SRC4078_03_4071_gauge_test": (
        SOURCE_DIR / "P8_Y5_R2FR_4071_LOCAL_MOTION_FRAME_GAUGE_TEST.csv",
        "FORCES_B_CONDITIONALLY",
        "4071 shows local motion-origin freedom forces B^A conditionally.",
    ),
    "SRC4078_04_4071_theorem": (
        SOURCE_DIR / "P8_Y5_R2FR_4071_CARTAN_ORIGIN_THEOREM_ATTEMPT.csv",
        "EXACT_CONDITIONAL_THEOREM",
        "4071 records the exact conditional gauge-compensator theorem.",
    ),
    "SRC4078_05_4072_variation": (
        SOURCE_DIR / "P8_Y5_R2FR_4072_GAUGE_VARIATION_AND_FIELD_STRENGTHS.csv",
        "B' = Lambda B - D' a",
        "4072 records the B^A inhomogeneous transformation law.",
    ),
    "SRC4078_06_4074_no_go": (
        SOURCE_DIR / "P8_Y5_R2FR_4074_BFIELD_DERIVATION_ATTEMPT.csv",
        "scalar_flow_cannot_be_B_compensator",
        "4074 proves scalar flow cannot derive B^A.",
    ),
    "SRC4078_07_4074_demotion": (
        SOURCE_DIR / "P8_Y5_R2FR_4074_EFFECTIVE_TETRAD_DEMOTION_CONTRACT.csv",
        "epsilon_B_derivation",
        "4074 defines B-derivation residual if effective tetrad is used.",
    ),
    "SRC4078_08_4076_runner": (
        SOURCE_DIR / "P8_Y5_R2FR_4076_EFFECTIVE_RESIDUAL_RUNNER_ROWS.csv",
        "epsilon_frame_gauge_quotient",
        "4076 runner contains frame-gauge quotient residual.",
    ),
    "SRC4078_09_no_abs_frame": (
        PROJECT / "core-mts-framework" / "relativity" / "mbt-special-relativity-a-respectful-extension-of-einstein.md",
        "No Absolute Reference Frame",
        "MTS/MBT source motivates but does not parent-sign local frame gauge.",
    ),
    "SRC4078_10_ppn_route": (
        FORMALIZATION / "121-local-PPN-repair-route.md",
        "epsilon_PPN_total",
        "PPN route supplies local residual vocabulary.",
    ),
}

WEB_SOURCES = [
    {
        "source_id": "WEB4078_0_will_living_review_table4",
        "title": "The Confrontation between General Relativity and Experiment, Table 4",
        "authors": "Clifford M. Will",
        "year": 2014,
        "url": "https://link.springer.com/article/10.12942/lrr-2014-4/tables/4",
        "supporting_url": "https://link.springer.com/article/10.12942/lrr-2014-4",
        "extracted_result": "alpha_1 orbital polarization limit 1e-4 from Lunar laser ranging; 4e-5 from PSR J1738+0333; alpha_2 spin precession limit 2e-9 from millisecond pulsars",
        "source_role": "preferred-frame PPN residual scale",
        "confidence": "peer_reviewed_living_review_table",
    }
]

OUTPUTS = {
    "source_register": SOURCE_DIR / "P8_Y5_R2FR_4078_SOURCE_REGISTER.csv",
    "web_provenance": SOURCE_DIR / "P8_Y5_R2FR_4078_WEB_PROVENANCE.csv",
    "b_theorem": SOURCE_DIR / "P8_Y5_R2FR_4078_B_TRANSLATION_OWNER_THEOREM.csv",
    "preferred_bound": SOURCE_DIR / "P8_Y5_R2FR_4078_SECOND_NUMERIC_P0_BOUND.csv",
    "runner_update": SOURCE_DIR / "P8_Y5_R2FR_4078_EFFECTIVE_RESIDUAL_RUNNER_UPDATE.csv",
    "decision_gate": SOURCE_DIR / "P8_Y5_R2FR_4078_DECISION_GATE.csv",
    "claim_gate": SOURCE_DIR / "P8_Y5_R2FR_4078_CLAIM_GATE.csv",
    "next_target": SOURCE_DIR / "P8_Y5_R2FR_4078_NEXT_TARGET.csv",
    "status": SOURCE_DIR / "P8_Y5_R2FR_4078_STATUS.csv",
    "validation": SOURCE_DIR / "P8_Y5_BRR545_4078_VALIDATION.csv",
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
    for source in WEB_SOURCES:
        rows.append(
            {
                "source_id": source["source_id"],
                "source_type": "web_source",
                "path_or_url": source["url"],
                "exists_or_recorded": True,
                "needle": source["extracted_result"],
                "needle_found": True,
                "role": source["source_role"],
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


def b_theorem_rows(current_timestamp: str) -> List[Dict[str, object]]:
    return [
        {
            "theorem_id": "BTO4078_0_translation_owner",
            "statement": "If the parent MTS action is invariant under local internal motion-origin translations X^A -> X^A + a^A(x), and the observed coframe is e^A = D_omega X^A + B^A, then B^A is forced to transform as B'^A = Lambda^A_B B^B - D'a^A so that e'^A = Lambda^A_B e^B.",
            "proof_sketch": "Under a local translation, D_omega X^A gains D_omega a^A. The only way for e^A to remain covariant without setting local translations to zero is for B^A to absorb the inhomogeneous term. This makes B^A the translational gauge compensator.",
            "result": "EXACT_CONDITIONAL_B_OWNER_THEOREM",
            "current_MTS_status": "LOCAL_TRANSLATION_SYMMETRY_NOT_PARENT_SIGNED",
            "claim_effect": "B^A derivation remains conditional; no local-GR pass.",
            "valid_for_claim": False,
            "timestamp_utc": current_timestamp,
        },
        {
            "theorem_id": "BTO4078_1_import_test",
            "statement": "B^A is not imported GR infrastructure only if local motion-origin translations are a parent symmetry and B^A appears in the parent action before local-GR readout.",
            "proof_sketch": "A compensator introduced after demanding e/g/EH is a closure input. A compensator forced by a parent symmetry and varied in the parent action is derived infrastructure.",
            "result": "DERIVATION_VS_IMPORT_TEST_RESTATED",
            "current_MTS_status": "CRITERION_WRITTEN_NOT_PASSED",
            "claim_effect": "effective tetrad branch remains the honest fallback.",
            "valid_for_claim": False,
            "timestamp_utc": current_timestamp,
        },
        {
            "theorem_id": "BTO4078_2_scalar_no_repair",
            "statement": "No scalar or gradient-only flow variable can substitute for B^A because it lacks the inhomogeneous translation shift.",
            "proof_sketch": "Scalar-built local objects transform homogeneously under frame changes. The B-shift is affine/connection-like, not tensorial.",
            "result": "4074_NO_GO_RETAINED",
            "current_MTS_status": "SCALAR_FLOW_ROUTE_REJECTED",
            "claim_effect": "prevents re-opening the pure scalar shortcut.",
            "valid_for_claim": False,
            "timestamp_utc": current_timestamp,
        },
        {
            "theorem_id": "BTO4078_3_observable_shadow",
            "statement": "If B^A is not parent-owned, its local preferred-frame or shadow-coframe effects must be treated as residuals and bounded by PPN preferred-frame tests.",
            "proof_sketch": "A non-parent frame/solder field can select a frame or leak through g_0i/readout terms. PPN alpha parameters are the weak-field language for preferred-frame leakage.",
            "result": "BOUND_ROUTE_SELECTED_FOR_NEXT_RESIDUAL",
            "current_MTS_status": "PREFERRED_FRAME_COMPONENT_BOUNDABLE",
            "claim_effect": "turns B-owner failure into finite residual acquisition, not public claim.",
            "valid_for_claim": False,
            "timestamp_utc": current_timestamp,
        },
    ]


def preferred_bound_rows(current_timestamp: str) -> List[Dict[str, object]]:
    return [
        {
            "bound_id": "BOUND4078_0_alpha1_preferred_frame",
            "quantity": "epsilon_frame_gauge_quotient_alpha1",
            "theory_map": "unowned B^A/e_obs frame-gauge leakage can produce preferred-frame PPN terms; alpha_1 is used as the conservative weak-field residual scale",
            "bound_abs": ALPHA1_LLR_BOUND,
            "strong_field_companion_bound_abs": ALPHA1_PULSAR_BOUND,
            "units": "dimensionless",
            "source_id": "WEB4078_0_will_living_review_table4",
            "observable_link": "PPN alpha_1 / orbital polarization / Lunar laser ranging",
            "valid_for_claim": False,
            "claim_use": "finite P0 preferred-frame residual scale only; not proof that MTS satisfies alpha_1",
            "timestamp_utc": current_timestamp,
        },
        {
            "bound_id": "BOUND4078_1_alpha2_reference",
            "quantity": "epsilon_frame_gauge_quotient_alpha2_reference",
            "theory_map": "alpha_2 is recorded as a tighter spin-precession preferred-frame reference but not used as the weak-field primary row because the table source marks millisecond pulsars",
            "bound_abs": ALPHA2_PULSAR_BOUND,
            "strong_field_companion_bound_abs": ALPHA2_PULSAR_BOUND,
            "units": "dimensionless",
            "source_id": "WEB4078_0_will_living_review_table4",
            "observable_link": "PPN alpha_2 / spin precession / millisecond pulsars",
            "valid_for_claim": False,
            "claim_use": "reference bound for future spin/frame branch, not current local-GR pass",
            "timestamp_utc": current_timestamp,
        },
    ]


def runner_update_rows(current_timestamp: str) -> List[Dict[str, object]]:
    return [
        {
            "runner_id": "RUNUP4078_0_alpha1_bound",
            "quantity": "epsilon_frame_gauge_quotient",
            "old_score": "MISSING_PARENT_ACTION_SIGNATURE",
            "new_score": "FINITE_EXTERNAL_BOUND_SCALE_ALPHA1",
            "numeric_bound_abs": ALPHA1_LLR_BOUND,
            "numeric_bound_rule": "use alpha_1 <= 1e-4 as conservative weak-field preferred-frame leakage bound; keep alpha_1=4e-5 pulsar value as companion source",
            "aggregate_effect": "second P0 residual becomes numeric; aggregate remains blocked by epsilon_spatial_metric_owner, epsilon_theta_parent, epsilon_B_derivation core, torsion/nonmetricity, and kappa normalization",
            "valid_for_claim": False,
            "timestamp_utc": current_timestamp,
        },
        {
            "runner_id": "RUNUP4078_1_B_owner",
            "quantity": "epsilon_B_derivation",
            "old_score": "BLOCKED_BY_TRANSLATION_CONNECTION",
            "new_score": "EXACT_CONDITIONAL_THEOREM_STILL_PARENT_UNSIGNED",
            "numeric_bound_abs": "not_applicable",
            "numeric_bound_rule": "B^A owner is not numerically bounded as a derivation; only its observable preferred-frame leakage receives alpha bounds",
            "aggregate_effect": "keeps B-derivation as a proof gate separate from preferred-frame residual bounds",
            "valid_for_claim": False,
            "timestamp_utc": current_timestamp,
        },
        {
            "runner_id": "RUNUP4078_2_aggregate",
            "quantity": "R_eff_GR",
            "old_score": "P0_PARTLY_NUMERIC_STILL_BLOCKED",
            "new_score": "P0_TWO_NUMERIC_ROWS_STILL_BLOCKED",
            "numeric_bound_abs": "not_applicable",
            "numeric_bound_rule": "do not aggregate until all P0 rows are theorem-zeroed or assigned finite sourced bounds",
            "aggregate_effect": "two finite P0 rows now exist: Cassini gamma reciprocal lock and alpha_1 preferred-frame leakage",
            "valid_for_claim": False,
            "timestamp_utc": current_timestamp,
        },
    ]


def decision_gate_rows(current_timestamp: str) -> List[Dict[str, object]]:
    return [
        {
            "decision_id": "DEC4078_0",
            "decision": DECISION,
            "meaning": "B^A is exactly forced if local motion-origin translation is a parent symmetry, but current MTS has not parent-signed that symmetry/action; the runner gains a second finite P0 preferred-frame bound from alpha_1",
            "forward_progress": "separates B-derivation proof gate from observable preferred-frame leakage bound",
            "public_claim": False,
            "github_action": False,
            "valid_for_claim": False,
            "timestamp_utc": current_timestamp,
        },
        {
            "decision_id": "DEC4078_1",
            "decision": "P0_RUNNER_NOW_HAS_TWO_NUMERIC_TEETH",
            "meaning": "epsilon_reciprocal_lock has Cassini gamma scale and epsilon_frame_gauge_quotient has alpha_1 scale; remaining P0 gates still block local-GR evidence",
            "forward_progress": "keeps proof discipline while making the empirical residual runner less symbolic",
            "public_claim": False,
            "github_action": False,
            "valid_for_claim": False,
            "timestamp_utc": current_timestamp,
        },
    ]


def claim_gate_rows(current_timestamp: str) -> List[Dict[str, object]]:
    return [
        {
            "claim_id": "CLAIM4078_0_B_theorem",
            "claim": "local translation symmetry would force B^A as compensator",
            "claim_allowed": True,
            "scope": "conditional mathematical theorem",
            "reason": "D X gains D a and B must absorb it for e^A covariance",
            "not_allowed_as": "current MTS parent signs local translation symmetry",
            "timestamp_utc": current_timestamp,
        },
        {
            "claim_id": "CLAIM4078_1_B_derived",
            "claim": "current MTS derives B^A",
            "claim_allowed": False,
            "scope": "parent local-GR derivation",
            "reason": "local motion-origin translation and B^A parent action are not signed by current corpus",
            "not_allowed_as": "MTS-to-GR pass",
            "timestamp_utc": current_timestamp,
        },
        {
            "claim_id": "CLAIM4078_2_alpha1_bound",
            "claim": "alpha_1 provides a finite preferred-frame residual scale",
            "claim_allowed": True,
            "scope": "private nonclaim residual target",
            "reason": "Will Table 4 gives alpha_1 weak-field LLR bound 1e-4",
            "not_allowed_as": "MTS satisfies alpha_1 or derives the frame owner",
            "timestamp_utc": current_timestamp,
        },
    ]


def next_target_rows(current_timestamp: str) -> List[Dict[str, object]]:
    return [
        {
            "target_id": "NEXT4078_0",
            "next_target": "4079-Y5-R2FR-third-P0-bound-or-torsion-nonmetricity-zero-theorem.md",
            "script": "scripts/Y5_R2FR_4079_third_P0_bound_or_torsion_nonmetricity_zero_theorem.py",
            "why": "continue the discipline: either close torsion/nonmetricity by theorem or source a finite P0 bound for it; do not add symbolic gates",
            "priority": "P0",
            "timestamp_utc": current_timestamp,
        },
        {
            "target_id": "NEXT4078_1",
            "next_target": "local_translation_parent_action_source_later",
            "script": "fold_into_future_parent_action_work",
            "why": "B-owner remains theorem-ready but needs parent action adoption, not another restatement",
            "priority": "P1",
            "timestamp_utc": current_timestamp,
        },
    ]


def status_rows(current_timestamp: str) -> List[Dict[str, object]]:
    return [
        {
            "timestamp_utc": current_timestamp,
            "branch_id": "MTS_R2FR_Y5_SECOND_P0_BOUND_OR_B_TRANSLATION_OWNER_THEOREM_4078",
            "checkpoint_id": 4078,
            "decision": DECISION,
            "status": "PRIVATE_NONCLAIM_CHECKPOINT",
            "summary": "4078 strengthens the exact conditional theorem that local motion-origin translations force B^A, keeps it parent-unsigned, and sources the second finite P0 residual row using PPN alpha_1 preferred-frame bounds.",
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
        for key in ["bound_abs", "strong_field_companion_bound_abs"]:
            try:
                value = float(row[key])
                if value <= 0:
                    failures.append(f"{row['bound_id']}:{key} not positive")
            except Exception:
                failures.append(f"{row['bound_id']}:{key} not numeric")
        if row["valid_for_claim"] is not False:
            failures.append(f"{row['bound_id']}:valid_for_claim not false")
    return not failures, "; ".join(failures) if failures else "numeric bounds positive and nonclaim"


def validate_claim_scopes(rows: List[Dict[str, object]]) -> Tuple[bool, str]:
    allowed_scopes = {"conditional mathematical theorem", "private nonclaim residual target"}
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
        "current MTS derives B^A', 'claim_allowed': True",
        "alpha_1 provides a finite preferred-frame residual scale', 'claim_allowed': True, 'scope': 'parent local-GR derivation",
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
        {"check_id": "VAL4078_00_sources", "passed": source_ok, "detail": source_detail},
        {"check_id": "VAL4078_01_csv_parse", "passed": csv_ok, "detail": csv_detail},
        {"check_id": "VAL4078_02_numeric_bound", "passed": bound_ok, "detail": bound_detail},
        {"check_id": "VAL4078_03_no_public_or_github_claim", "passed": no_public_ok, "detail": no_public_detail},
        {"check_id": "VAL4078_04_claim_scope", "passed": claim_scope_ok, "detail": claim_scope_detail},
        {
            "check_id": "VAL4078_05_B_theorem_conditional",
            "passed": "EXACT_CONDITIONAL_B_OWNER_THEOREM" in joined and "LOCAL_TRANSLATION_SYMMETRY_NOT_PARENT_SIGNED" in joined,
            "detail": "B owner theorem exists but remains parent unsigned",
        },
        {
            "check_id": "VAL4078_06_second_P0_numeric",
            "passed": "FINITE_EXTERNAL_BOUND_SCALE_ALPHA1" in joined and "epsilon_frame_gauge_quotient" in joined,
            "detail": "second finite P0 preferred-frame bound is present",
        },
        {
            "check_id": "VAL4078_07_next_target",
            "passed": "4079-Y5-R2FR-third-P0-bound-or-torsion-nonmetricity-zero-theorem.md" in joined,
            "detail": "next target requires torsion/nonmetricity theorem or finite bound",
        },
        {"check_id": "VAL4078_08_script_compiles", "passed": compile_ok, "detail": compile_detail},
    ]


def doc_text(current_timestamp: str) -> str:
    return f"""# 4078 - Second P0 Bound Or B Translation Owner Theorem

- Timestamp: `{current_timestamp}`
- Status: `private_nonclaim_checkpoint`
- Decision: `{DECISION}`
- Public GR/Newton/PPN claim: `false`
- GitHub action: `false`

## B Translation Owner Theorem

4078 tries the derivation route first.

If MTS has a parent-owned local motion-origin symmetry:

```text
X^A -> X^A + a^A(x)
e^A = D_omega X^A + B^A
```

then:

```text
D_omega X^A -> D_omega X^A + D_omega a^A
```

so covariance of `e^A` forces:

```text
B'^A = Lambda^A_B B^B - D'a^A
```

That is an exact conditional theorem. It is the right mathematical route.

But it is still not a current MTS derivation, because the current corpus has not parent-signed local motion-origin translations and a varied `B^A` sector before local-GR readout.

## Second Finite P0 Bound

Since the owner theorem remains conditional, 4078 adds the next finite P0 residual scale.

Unowned frame/solder leakage can show up as preferred-frame PPN terms. The conservative weak-field row uses:

```text
|alpha_1| <= {ALPHA1_LLR_BOUND:.1e}
```

from Will's Living Reviews Table 4, listed as an orbital-polarization bound from Lunar laser ranging. The same table records a tighter companion value:

```text
|alpha_1| <= {ALPHA1_PULSAR_BOUND:.1e}
```

from PSR J1738+0333, and an `alpha_2` reference:

```text
|alpha_2| <= {ALPHA2_PULSAR_BOUND:.1e}
```

from millisecond-pulsar spin precession.

The active weak-field P0 row is therefore:

```text
epsilon_frame_gauge_quotient_alpha1 <= {ALPHA1_LLR_BOUND:.1e}
```

This is not a pass. It is a finite leash on preferred-frame leakage.

## Runner Update

The local-GR residual runner now has two numeric P0 teeth:

```text
epsilon_reciprocal_lock        Cassini gamma scale
epsilon_frame_gauge_quotient   alpha_1 preferred-frame scale
```

The aggregate remains blocked because these are still nonnumeric or theorem-open:

```text
epsilon_spatial_metric_owner
epsilon_theta_parent
epsilon_B_derivation core
epsilon_torsion_nonmetricity
epsilon_kappa_normalization
```

## Decision

```text
B-owner theorem = exact conditional theorem
current B derivation = not parent-signed
second finite P0 bound = sourced alpha_1 preferred-frame row
```

## Sources

- Will, `The Confrontation between General Relativity and Experiment`, Living Reviews in Relativity, Table 4: current PPN limits.

## Next

`4079` should either:

```text
prove torsion/nonmetricity zero or auxiliary suppression
```

or source a finite P0 torsion/nonmetricity bound row.
"""


def main() -> None:
    current_timestamp = timestamp()
    SOURCE_DIR.mkdir(parents=True, exist_ok=True)

    sources = source_rows(current_timestamp)
    web_provenance = web_provenance_rows(current_timestamp)
    b_theorem = b_theorem_rows(current_timestamp)
    bounds = preferred_bound_rows(current_timestamp)
    runner = runner_update_rows(current_timestamp)
    decisions = decision_gate_rows(current_timestamp)
    claims = claim_gate_rows(current_timestamp)
    next_targets = next_target_rows(current_timestamp)
    statuses = status_rows(current_timestamp)

    DOC_PATH.write_text(doc_text(current_timestamp), encoding="utf-8")
    write_csv(OUTPUTS["source_register"], sources)
    write_csv(OUTPUTS["web_provenance"], web_provenance)
    write_csv(OUTPUTS["b_theorem"], b_theorem)
    write_csv(OUTPUTS["preferred_bound"], bounds)
    write_csv(OUTPUTS["runner_update"], runner)
    write_csv(OUTPUTS["decision_gate"], decisions)
    write_csv(OUTPUTS["claim_gate"], claims)
    write_csv(OUTPUTS["next_target"], next_targets)
    write_csv(OUTPUTS["status"], statuses)

    generated_csvs = [
        OUTPUTS["source_register"],
        OUTPUTS["web_provenance"],
        OUTPUTS["b_theorem"],
        OUTPUTS["preferred_bound"],
        OUTPUTS["runner_update"],
        OUTPUTS["decision_gate"],
        OUTPUTS["claim_gate"],
        OUTPUTS["next_target"],
        OUTPUTS["status"],
    ]
    row_groups = [
        sources,
        web_provenance,
        b_theorem,
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

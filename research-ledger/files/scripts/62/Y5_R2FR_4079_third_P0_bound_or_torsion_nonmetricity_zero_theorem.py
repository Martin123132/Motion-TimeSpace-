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
DOC_PATH = ROOT / "4079-Y5-R2FR-third-P0-bound-or-torsion-nonmetricity-zero-theorem.md"

DECISION = "TORSION_NONMETRICITY_ZERO_THEOREM_CONDITIONAL_THIRD_P0_TORSION_BOUND_SOURCED_NORMALIZATION_PENDING"

TORSION_BOUND_GEV_ORDER = 1.0e-31

LOCAL_SOURCES: Dict[str, Tuple[Path, str, str]] = {
    "SRC4079_00_4078_next": (
        SOURCE_DIR / "P8_Y5_R2FR_4078_NEXT_TARGET.csv",
        "4079-Y5-R2FR-third-P0-bound-or-torsion-nonmetricity-zero-theorem.md",
        "4078 selected torsion/nonmetricity theorem or third P0 bound.",
    ),
    "SRC4079_01_4078_runner": (
        SOURCE_DIR / "P8_Y5_R2FR_4078_EFFECTIVE_RESIDUAL_RUNNER_UPDATE.csv",
        "P0_TWO_NUMERIC_ROWS_STILL_BLOCKED",
        "4078 runner has two numeric P0 rows but torsion remains open.",
    ),
    "SRC4079_02_4070_torsion_gate": (
        SOURCE_DIR / "P8_Y5_R2FR_4070_TORSION_EXTRA_MODE_GATE.csv",
        "CLOSABLE_BY_ANTISYMMETRIC_SPIN_CONNECTION_IF_PARENT_SIGNED",
        "4070 states nonmetricity closes with antisymmetric spin connection if parent signed.",
    ),
    "SRC4079_03_4072_variation": (
        SOURCE_DIR / "P8_Y5_R2FR_4072_GAUGE_VARIATION_AND_FIELD_STRENGTHS.csv",
        "CONDITIONAL_PALATINI_REDUCTION",
        "4072 records Palatini spinless torsion reduction route.",
    ),
    "SRC4079_04_4072_action": (
        SOURCE_DIR / "P8_Y5_R2FR_4072_LOCAL_MOTION_FRAME_GAUGE_ACTION.csv",
        "GATE_REQUIRED_NOT_PARENT_SIGNED",
        "4072 keeps torsion/nonmetricity gate required and not parent signed.",
    ),
    "SRC4079_05_axial_torsion": (
        SOURCE_DIR / "P8_Y5_axial_torsion_stiffness_status.csv",
        "DERIVED_SYMBOLIC_NONCLAIM",
        "axial torsion stiffness row is symbolic and not claim-valid.",
    ),
    "SRC4079_06_min_blocks": (
        SOURCE_DIR / "P8_MIN_PARENT_LOCAL_GR_ACTION_BLOCKS.csv",
        "A511_0_EH_core",
        "minimum local GR action blocks define the EH baseline.",
    ),
    "SRC4079_07_ppn_route": (
        FORMALIZATION / "121-local-PPN-repair-route.md",
        "epsilon_PPN_total",
        "PPN route supplies residual vocabulary.",
    ),
}

WEB_SOURCES = [
    {
        "source_id": "WEB4079_0_kostelecky_russell_tasson_prl",
        "title": "Constraints on Torsion from Lorentz Violation",
        "authors": "Kostelecky, Russell, Tasson",
        "year": 2008,
        "url": "https://doi.org/10.1103/PhysRevLett.100.111102",
        "supporting_url": "https://arxiv.org/abs/0712.4393",
        "extracted_result": "constraints involving 19 of 24 independent torsion components down to order 10^-31 GeV",
        "source_role": "finite external torsion bound scale for spin-coupled torsion residual",
        "confidence": "peer_reviewed_PRL_with_arXiv_preprint",
    }
]

OUTPUTS = {
    "source_register": SOURCE_DIR / "P8_Y5_R2FR_4079_SOURCE_REGISTER.csv",
    "web_provenance": SOURCE_DIR / "P8_Y5_R2FR_4079_WEB_PROVENANCE.csv",
    "zero_theorem": SOURCE_DIR / "P8_Y5_R2FR_4079_TORSION_NONMETRICITY_ZERO_THEOREM.csv",
    "third_bound": SOURCE_DIR / "P8_Y5_R2FR_4079_THIRD_NUMERIC_P0_BOUND.csv",
    "runner_update": SOURCE_DIR / "P8_Y5_R2FR_4079_EFFECTIVE_RESIDUAL_RUNNER_UPDATE.csv",
    "decision_gate": SOURCE_DIR / "P8_Y5_R2FR_4079_DECISION_GATE.csv",
    "claim_gate": SOURCE_DIR / "P8_Y5_R2FR_4079_CLAIM_GATE.csv",
    "next_target": SOURCE_DIR / "P8_Y5_R2FR_4079_NEXT_TARGET.csv",
    "status": SOURCE_DIR / "P8_Y5_R2FR_4079_STATUS.csv",
    "validation": SOURCE_DIR / "P8_Y5_BRR545_4079_VALIDATION.csv",
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


def zero_theorem_rows(current_timestamp: str) -> List[Dict[str, object]]:
    return [
        {
            "theorem_id": "TNZ4079_0_nonmetricity_zero",
            "statement": "If the parent local geometry uses an internal Lorentz connection omega_AB=-omega_BA with fixed eta_AB, then Q_AB := -D_omega eta_AB = 0 identically.",
            "proof_sketch": "D_omega eta_AB = -omega_AB - omega_BA, which vanishes for an antisymmetric Lorentz connection.",
            "result": "EXACT_NONMETRICITY_ZERO_IF_LORENTZ_CONNECTION_PARENT_SIGNED",
            "current_MTS_status": "CONDITIONAL_NOT_PARENT_SIGNED",
            "residual_effect": "epsilon_nonmetricity can be theorem-zeroed only on the parent-signed Lorentz-connection branch.",
            "valid_for_claim": False,
            "timestamp_utc": current_timestamp,
        },
        {
            "theorem_id": "TNZ4079_1_spinless_torsion_zero",
            "statement": "For first-order Einstein-Cartan/Palatini action with independent omega and e, no torsion kinetic term, and matter/EM independent of omega in a spinless local exterior, the omega variation algebraically sets T^A = D_omega e^A = 0.",
            "proof_sketch": "The variation of epsilon_ABCD e^A wedge e^B wedge R^CD with respect to omega gives epsilon_ABCD e^A wedge T^B = spin current. With zero spin current and nondegenerate e, the torsion tensor vanishes algebraically.",
            "result": "EXACT_CONDITIONAL_SPINLESS_TORSION_ZERO_THEOREM",
            "current_MTS_status": "PALATINI_BRANCH_CONDITIONAL_PARENT_ACTION_NOT_SIGNED",
            "residual_effect": "epsilon_torsion can be theorem-zeroed only for spinless exterior and no independent torsion source/kinetic terms.",
            "valid_for_claim": False,
            "timestamp_utc": current_timestamp,
        },
        {
            "theorem_id": "TNZ4079_2_spin_source_caveat",
            "statement": "If spinor matter, independent spin current, axial torsion stiffness, or propagating torsion terms are active, torsion is not automatically zero and must be bounded or integrated out.",
            "proof_sketch": "Einstein-Cartan torsion is algebraic in spin current; kinetic/stiffness terms turn it into an auxiliary or propagating residual rather than a theorem-zero.",
            "result": "SPIN_AXIAL_TORSION_BOUND_BRANCH_RETAINED",
            "current_MTS_status": "SYMBOLIC_AXIAL_TORSION_ROW_EXISTS",
            "residual_effect": "epsilon_axial_torsion_spin remains a bound row unless spin-current silence is parent-signed.",
            "valid_for_claim": False,
            "timestamp_utc": current_timestamp,
        },
        {
            "theorem_id": "TNZ4079_3_parent_claim_gate",
            "statement": "The torsion/nonmetricity P0 gate closes only if the parent action chooses the Lorentz-connection EC/Palatini branch and signs the spinless/no-independent-torsion local exterior clauses before PPN readout.",
            "proof_sketch": "The zero theorem is a theorem about a specific parent branch; adopting it after matching GR would be a closure assumption.",
            "result": "ZERO_THEOREM_AVAILABLE_NOT_CURRENT_PUBLIC_CLAIM",
            "current_MTS_status": "LOCAL_GR_CLAIM_STILL_BLOCKED",
            "residual_effect": "runner can record theorem-ready status but not mark local-GR pass.",
            "valid_for_claim": False,
            "timestamp_utc": current_timestamp,
        },
    ]


def third_bound_rows(current_timestamp: str) -> List[Dict[str, object]]:
    return [
        {
            "bound_id": "BOUND4079_0_torsion_lorentz_violation",
            "quantity": "epsilon_axial_torsion_spin_bound",
            "theory_map": "spin-coupled axial/mixed torsion residuals can be constrained through Lorentz-violation searches when the spinless zero theorem is not parent-signed",
            "bound_order": TORSION_BOUND_GEV_ORDER,
            "bound_units": "GeV",
            "components_constrained": "19_of_24_torsion_components",
            "source_id": "WEB4079_0_kostelecky_russell_tasson_prl",
            "observable_link": "fermion Lorentz-violation searches / torsion components",
            "aggregate_conversion": "dimensionless_PPN_aggregate_requires_parent_normalization_map",
            "valid_for_claim": False,
            "claim_use": "finite external torsion scale only; not proof that MTS satisfies torsion constraints",
            "timestamp_utc": current_timestamp,
        }
    ]


def runner_update_rows(current_timestamp: str) -> List[Dict[str, object]]:
    return [
        {
            "runner_id": "RUNUP4079_0_torsion_theorem",
            "quantity": "epsilon_torsion_nonmetricity",
            "old_score": "GATE_REQUIRED_NOT_PARENT_SIGNED",
            "new_score": "EXACT_CONDITIONAL_ZERO_THEOREM_PARENT_UNSIGNED",
            "numeric_bound": "not_applicable_for_zero_theorem",
            "numeric_bound_units": "not_applicable",
            "aggregate_effect": "can become zero if parent signs EC/Palatini Lorentz connection, spinless exterior, and no independent torsion terms",
            "valid_for_claim": False,
            "timestamp_utc": current_timestamp,
        },
        {
            "runner_id": "RUNUP4079_1_torsion_bound",
            "quantity": "epsilon_axial_torsion_spin_bound",
            "old_score": "SYMBOLIC_AXIAL_TORSION_ROW",
            "new_score": "FINITE_EXTERNAL_TORSION_SCALE",
            "numeric_bound": TORSION_BOUND_GEV_ORDER,
            "numeric_bound_units": "GeV",
            "aggregate_effect": "third finite P0-adjacent scale is sourced, but dimensionless PPN aggregation waits for parent normalization map",
            "valid_for_claim": False,
            "timestamp_utc": current_timestamp,
        },
        {
            "runner_id": "RUNUP4079_2_aggregate",
            "quantity": "R_eff_GR",
            "old_score": "P0_TWO_NUMERIC_ROWS_STILL_BLOCKED",
            "new_score": "P0_TWO_DIMENSIONLESS_ROWS_PLUS_TORSION_SCALE_STILL_BLOCKED",
            "numeric_bound": "not_applicable",
            "numeric_bound_units": "mixed",
            "aggregate_effect": "Cassini gamma and alpha_1 are dimensionless; torsion bound is finite but needs map; spatial metric, theta parent, B derivation, and kappa normalization remain open",
            "valid_for_claim": False,
            "timestamp_utc": current_timestamp,
        },
    ]


def decision_gate_rows(current_timestamp: str) -> List[Dict[str, object]]:
    return [
        {
            "decision_id": "DEC4079_0",
            "decision": DECISION,
            "meaning": "torsion and nonmetricity have exact conditional zero theorems in the Lorentz EC/Palatini spinless branch, but current MTS has not parent-signed that branch; a finite external torsion scale is sourced for the spin-coupled residual.",
            "forward_progress": "turns torsion/nonmetricity from an open symbolic gate into a theorem-ready branch plus a sourced torsion bound row",
            "public_claim": False,
            "github_action": False,
            "valid_for_claim": False,
            "timestamp_utc": current_timestamp,
        },
        {
            "decision_id": "DEC4079_1",
            "decision": "DO_NOT_AGGREGATE_TORSION_BOUND_WITHOUT_NORMALIZATION_MAP",
            "meaning": "the torsion scale is in GeV and cannot be mixed with dimensionless PPN residuals until MTS supplies the coupling/normalization map",
            "forward_progress": "prevents fake precision while still recording a real experimental leash",
            "public_claim": False,
            "github_action": False,
            "valid_for_claim": False,
            "timestamp_utc": current_timestamp,
        },
    ]


def claim_gate_rows(current_timestamp: str) -> List[Dict[str, object]]:
    return [
        {
            "claim_id": "CLAIM4079_0_nonmetricity_zero",
            "claim": "nonmetricity vanishes for parent-owned antisymmetric Lorentz connection",
            "claim_allowed": True,
            "scope": "conditional mathematical theorem",
            "reason": "D_omega eta_AB=0 follows from omega_AB=-omega_BA",
            "not_allowed_as": "current MTS parent has signed local GR",
            "timestamp_utc": current_timestamp,
        },
        {
            "claim_id": "CLAIM4079_1_torsion_zero",
            "claim": "spinless EC/Palatini branch gives algebraic torsion zero",
            "claim_allowed": True,
            "scope": "conditional mathematical theorem",
            "reason": "omega variation sets torsion equal to spin current; spinless exterior sets it to zero",
            "not_allowed_as": "generic MTS torsion silence",
            "timestamp_utc": current_timestamp,
        },
        {
            "claim_id": "CLAIM4079_2_torsion_bound",
            "claim": "spin-coupled torsion residual has finite external bound scale",
            "claim_allowed": True,
            "scope": "private nonclaim residual target",
            "reason": "Kostelecky/Russell/Tasson constrain torsion components down to order 10^-31 GeV",
            "not_allowed_as": "MTS satisfies torsion bounds or has dimensionless aggregate score",
            "timestamp_utc": current_timestamp,
        },
        {
            "claim_id": "CLAIM4079_3_local_GR_pass",
            "claim": "torsion/nonmetricity gate is closed for current MTS local GR",
            "claim_allowed": False,
            "scope": "parent local-GR derivation",
            "reason": "zero theorem is branch-conditional and parent action clauses are not signed",
            "not_allowed_as": "MTS-to-local-GR pass",
            "timestamp_utc": current_timestamp,
        },
    ]


def next_target_rows(current_timestamp: str) -> List[Dict[str, object]]:
    return [
        {
            "target_id": "NEXT4079_0",
            "next_target": "4080-Y5-R2FR-kappa-normalization-theorem-or-Gdot-bound.md",
            "script": "scripts/Y5_R2FR_4080_kappa_normalization_theorem_or_Gdot_bound.py",
            "why": "next P0 gate is kappa/G normalization: prove topological constant-G branch or source finite Gdot/G and local G calibration bounds",
            "priority": "P0",
            "timestamp_utc": current_timestamp,
        },
        {
            "target_id": "NEXT4079_1",
            "next_target": "torsion_normalization_map_later",
            "script": "fold_into_spin_particle_branch",
            "why": "torsion bound is finite but needs MTS coupling normalization before dimensionless aggregation",
            "priority": "P1",
            "timestamp_utc": current_timestamp,
        },
    ]


def status_rows(current_timestamp: str) -> List[Dict[str, object]]:
    return [
        {
            "timestamp_utc": current_timestamp,
            "branch_id": "MTS_R2FR_Y5_THIRD_P0_BOUND_OR_TORSION_NONMETRICITY_ZERO_THEOREM_4079",
            "checkpoint_id": 4079,
            "decision": DECISION,
            "status": "PRIVATE_NONCLAIM_CHECKPOINT",
            "summary": "4079 derives conditional EC/Palatini zero theorems for nonmetricity and spinless torsion, keeps them parent-unsigned, and sources a finite torsion scale of order 10^-31 GeV for spin-coupled residuals.",
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
        try:
            value = float(row["bound_order"])
            if value <= 0:
                failures.append(f"{row['bound_id']}:bound_order not positive")
        except Exception:
            failures.append(f"{row['bound_id']}:bound_order not numeric")
        if row["valid_for_claim"] is not False:
            failures.append(f"{row['bound_id']}:valid_for_claim not false")
        if row["aggregate_conversion"] != "dimensionless_PPN_aggregate_requires_parent_normalization_map":
            failures.append(f"{row['bound_id']}:missing normalization warning")
    return not failures, "; ".join(failures) if failures else "torsion bound positive, nonclaim, and normalization-gated"


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
        "torsion/nonmetricity gate is closed for current MTS local GR', 'claim_allowed': True",
        "spin-coupled torsion residual has finite external bound scale', 'claim_allowed': True, 'scope': 'parent local-GR derivation",
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
        {"check_id": "VAL4079_00_sources", "passed": source_ok, "detail": source_detail},
        {"check_id": "VAL4079_01_csv_parse", "passed": csv_ok, "detail": csv_detail},
        {"check_id": "VAL4079_02_numeric_bound", "passed": bound_ok, "detail": bound_detail},
        {"check_id": "VAL4079_03_no_public_or_github_claim", "passed": no_public_ok, "detail": no_public_detail},
        {"check_id": "VAL4079_04_claim_scope", "passed": claim_scope_ok, "detail": claim_scope_detail},
        {
            "check_id": "VAL4079_05_zero_theorems_conditional",
            "passed": "EXACT_CONDITIONAL_SPINLESS_TORSION_ZERO_THEOREM" in joined
            and "EXACT_NONMETRICITY_ZERO_IF_LORENTZ_CONNECTION_PARENT_SIGNED" in joined,
            "detail": "torsion/nonmetricity zero theorems are present",
        },
        {
            "check_id": "VAL4079_06_torsion_bound",
            "passed": "FINITE_EXTERNAL_TORSION_SCALE" in joined and "1e-31" in joined,
            "detail": "finite torsion bound scale is present",
        },
        {
            "check_id": "VAL4079_07_next_target",
            "passed": "4080-Y5-R2FR-kappa-normalization-theorem-or-Gdot-bound.md" in joined,
            "detail": "next target moves to kappa/G normalization",
        },
        {"check_id": "VAL4079_08_script_compiles", "passed": compile_ok, "detail": compile_detail},
    ]


def doc_text(current_timestamp: str) -> str:
    return f"""# 4079 - Third P0 Bound Or Torsion/Nonmetricity Zero Theorem

- Timestamp: `{current_timestamp}`
- Status: `private_nonclaim_checkpoint`
- Decision: `{DECISION}`
- Public GR/Newton/PPN claim: `false`
- GitHub action: `false`

## Zero Theorem

4079 gets a real conditional theorem-zero route.

For nonmetricity:

```text
omega_AB = -omega_BA
Q_AB := -D_omega eta_AB = 0
```

So nonmetricity vanishes identically if the parent signs an internal Lorentz connection.

For torsion in the spinless EC/Palatini branch:

```text
S_EC[e, omega] = (4 kappa)^-1 int epsilon_ABCD e^A wedge e^B wedge R^CD[omega]
```

and the `omega` variation gives the torsion/spin equation. In a spinless local exterior with no independent torsion kinetic/source term:

```text
T^A = D_omega e^A = 0
```

This is exact, but branch-conditional.

## Why It Is Not A Public Pass

The current corpus has not yet parent-signed all required clauses:

```text
Lorentz connection as parent-owned local geometry
spinless/local exterior domain
no independent torsion kinetic term
no axial torsion source leakage
same e_obs matter/EM/clock frame before PPN readout
```

So the theorem is usable as a promotion route, not as a finished local-GR claim.

## Third Finite Bound

If spin-coupled torsion is not theorem-zeroed, it gets a sourced external scale.

Kostelecky, Russell, and Tasson constrain 19 of 24 torsion components down to order:

```text
|T| ~ {TORSION_BOUND_GEV_ORDER:.1e} GeV
```

This is a finite experimental leash on spin-coupled torsion residuals.

Important caveat:

```text
the bound is dimensionful
dimensionless PPN aggregation requires an MTS coupling/normalization map
```

## Runner Update

The local runner now has:

```text
epsilon_reciprocal_lock      numeric Cassini gamma scale
epsilon_frame_gauge_quotient numeric alpha_1 scale
epsilon_torsion_spin         finite GeV torsion scale, normalization pending
```

The aggregate still cannot be claimed because:

```text
epsilon_spatial_metric_owner
epsilon_theta_parent
epsilon_B_derivation core
epsilon_kappa_normalization
torsion dimensionless normalization
```

remain open.

## Decision

```text
torsion/nonmetricity zero theorem = exact conditional
current MTS local-GR pass = false
third P0-adjacent bound = sourced torsion scale
```

## Sources

- Kostelecky, Russell, and Tasson, `Constraints on Torsion from Lorentz Violation`, DOI `10.1103/PhysRevLett.100.111102`, arXiv `0712.4393`.

## Next

`4080` should attack:

```text
kappa_eff / Newton G normalization
```

Either prove the topological constant-G branch, or source finite `Gdot/G` and local-G calibration bounds.
"""


def main() -> None:
    current_timestamp = timestamp()
    SOURCE_DIR.mkdir(parents=True, exist_ok=True)

    sources = source_rows(current_timestamp)
    web_provenance = web_provenance_rows(current_timestamp)
    zero_theorem = zero_theorem_rows(current_timestamp)
    bounds = third_bound_rows(current_timestamp)
    runner = runner_update_rows(current_timestamp)
    decisions = decision_gate_rows(current_timestamp)
    claims = claim_gate_rows(current_timestamp)
    next_targets = next_target_rows(current_timestamp)
    statuses = status_rows(current_timestamp)

    DOC_PATH.write_text(doc_text(current_timestamp), encoding="utf-8")
    write_csv(OUTPUTS["source_register"], sources)
    write_csv(OUTPUTS["web_provenance"], web_provenance)
    write_csv(OUTPUTS["zero_theorem"], zero_theorem)
    write_csv(OUTPUTS["third_bound"], bounds)
    write_csv(OUTPUTS["runner_update"], runner)
    write_csv(OUTPUTS["decision_gate"], decisions)
    write_csv(OUTPUTS["claim_gate"], claims)
    write_csv(OUTPUTS["next_target"], next_targets)
    write_csv(OUTPUTS["status"], statuses)

    generated_csvs = [
        OUTPUTS["source_register"],
        OUTPUTS["web_provenance"],
        OUTPUTS["zero_theorem"],
        OUTPUTS["third_bound"],
        OUTPUTS["runner_update"],
        OUTPUTS["decision_gate"],
        OUTPUTS["claim_gate"],
        OUTPUTS["next_target"],
        OUTPUTS["status"],
    ]
    row_groups = [
        sources,
        web_provenance,
        zero_theorem,
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

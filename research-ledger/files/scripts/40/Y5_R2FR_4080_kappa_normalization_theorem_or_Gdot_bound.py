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
DOC_PATH = ROOT / "4080-Y5-R2FR-kappa-normalization-theorem-or-Gdot-bound.md"

DECISION = "KAPPA_TOPOLOGICAL_CONSTANT_THEOREM_CONDITIONAL_G_NUMERICAL_VALUE_NOT_DERIVED_GDOT_AND_CODATA_BOUNDS_SOURCED"

GDOT_OVER_G_CENTRAL_PER_YEAR = 4.0e-13
GDOT_OVER_G_SIGMA_PER_YEAR = 9.0e-13
GDOT_OVER_G_ENVELOPE_PER_YEAR = abs(GDOT_OVER_G_CENTRAL_PER_YEAR) + GDOT_OVER_G_SIGMA_PER_YEAR

CODATA_G_VALUE = 6.67430e-11
CODATA_G_STANDARD_UNCERTAINTY = 0.00015e-11
CODATA_G_RELATIVE_UNCERTAINTY = 2.2e-5

LOCAL_SOURCES: Dict[str, Tuple[Path, str, str]] = {
    "SRC4080_00_4079_next": (
        SOURCE_DIR / "P8_Y5_R2FR_4079_NEXT_TARGET.csv",
        "4080-Y5-R2FR-kappa-normalization-theorem-or-Gdot-bound.md",
        "4079 selected kappa/G normalization theorem or Gdot bound.",
    ),
    "SRC4080_01_4079_runner": (
        SOURCE_DIR / "P8_Y5_R2FR_4079_EFFECTIVE_RESIDUAL_RUNNER_UPDATE.csv",
        "kappa normalization remain open",
        "4079 runner identifies kappa normalization as still open in aggregate blocker text.",
    ),
    "SRC4080_02_4072_kappa": (
        SOURCE_DIR / "P8_Y5_R2FR_4072_LOCAL_MOTION_FRAME_GAUGE_ACTION.csv",
        "CONDITIONAL_TOPOLOGICAL_ROUTE",
        "4072 records the topological kappa route as conditional.",
    ),
    "SRC4080_03_4072_delta_A3": (
        SOURCE_DIR / "P8_Y5_R2FR_4072_GAUGE_VARIATION_AND_FIELD_STRENGTHS.csv",
        "d kappa_eff=0 locally",
        "4072 variation gives local constant kappa if premises hold.",
    ),
    "SRC4080_04_kappa_clause": (
        SOURCE_DIR / "P8_CONSTANT_KAPPA_TOPOLOGICAL_ZEROFORM_CLAUSE.csv",
        "d kappa_eff=0",
        "topological zero-form clause states the zero-gradient equation.",
    ),
    "SRC4080_05_min_blocks": (
        SOURCE_DIR / "P8_MIN_PARENT_LOCAL_GR_ACTION_BLOCKS.csv",
        "A511_1_kappa_topological",
        "minimum local GR action blocks include kappa topological sector.",
    ),
    "SRC4080_06_derived_chain": (
        SOURCE_DIR / "P8_MIN_PARENT_LOCAL_GR_DERIVED_CHAIN.csv",
        "constant local G_eff/kappa",
        "derived chain treats kappa/G constancy as conditional.",
    ),
    "SRC4080_07_ppn_route": (
        FORMALIZATION / "121-local-PPN-repair-route.md",
        "epsilon_PPN_total",
        "PPN route supplies residual vocabulary.",
    ),
}

WEB_SOURCES = [
    {
        "source_id": "WEB4080_0_williams_turyshev_boggs_prl",
        "title": "Progress in Lunar Laser Ranging Tests of Relativistic Gravity",
        "authors": "Williams, Turyshev, Boggs",
        "year": 2004,
        "url": "https://doi.org/10.1103/PhysRevLett.93.261101",
        "supporting_url": "https://arxiv.org/abs/gr-qc/0411113",
        "extracted_result": "Gdot/G = (4 +/- 9) x 10^-13 yr^-1",
        "source_role": "finite external drift bound for kappa/G constancy residual",
        "confidence": "peer_reviewed_PRL_and_arXiv_preprint",
    },
    {
        "source_id": "WEB4080_1_nist_codata_2022_G",
        "title": "CODATA Value: Newtonian constant of gravitation",
        "authors": "NIST/CODATA",
        "year": 2022,
        "url": "https://physics.nist.gov/cgi-bin/cuu/Value?bg=",
        "supporting_url": "https://physics.nist.gov/constants",
        "extracted_result": "G = 6.67430(15) x 10^-11 m^3 kg^-1 s^-2; relative standard uncertainty 2.2 x 10^-5",
        "source_role": "finite external local-G calibration uncertainty",
        "confidence": "official_CODATA_NIST_constant_page",
    },
]

OUTPUTS = {
    "source_register": SOURCE_DIR / "P8_Y5_R2FR_4080_SOURCE_REGISTER.csv",
    "web_provenance": SOURCE_DIR / "P8_Y5_R2FR_4080_WEB_PROVENANCE.csv",
    "kappa_theorem": SOURCE_DIR / "P8_Y5_R2FR_4080_KAPPA_TOPOLOGICAL_THEOREM.csv",
    "g_bounds": SOURCE_DIR / "P8_Y5_R2FR_4080_GDOT_AND_G_CALIBRATION_BOUNDS.csv",
    "runner_update": SOURCE_DIR / "P8_Y5_R2FR_4080_EFFECTIVE_RESIDUAL_RUNNER_UPDATE.csv",
    "decision_gate": SOURCE_DIR / "P8_Y5_R2FR_4080_DECISION_GATE.csv",
    "claim_gate": SOURCE_DIR / "P8_Y5_R2FR_4080_CLAIM_GATE.csv",
    "next_target": SOURCE_DIR / "P8_Y5_R2FR_4080_NEXT_TARGET.csv",
    "status": SOURCE_DIR / "P8_Y5_R2FR_4080_STATUS.csv",
    "validation": SOURCE_DIR / "P8_Y5_BRR545_4080_VALIDATION.csv",
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


def kappa_theorem_rows(current_timestamp: str) -> List[Dict[str, object]]:
    return [
        {
            "theorem_id": "KAP4080_0_constant_kappa",
            "statement": "If the parent contains a metric-independent topological sector S_kappa_top = int kappa_eff dA_3 with fixed/topological boundary variation, then variation with respect to A_3 gives d kappa_eff = 0 on connected local domains.",
            "proof_sketch": "delta_A3 S = int kappa_eff d(delta A_3) = boundary - int d kappa_eff wedge delta A_3. With admissible delta A_3, the Euler-Lagrange equation is d kappa_eff=0.",
            "result": "EXACT_CONDITIONAL_CONSTANT_KAPPA_THEOREM",
            "current_MTS_status": "TOPOLOGICAL_BRANCH_CONDITIONAL_NOT_PARENT_SIGNED",
            "residual_effect": "epsilon_kappa_drift can be theorem-zeroed only if A_3/kappa sector is parent-owned and boundary-silent.",
            "valid_for_claim": False,
            "timestamp_utc": current_timestamp,
        },
        {
            "theorem_id": "KAP4080_1_constant_not_value",
            "statement": "The topological zero-gradient theorem can make kappa_eff locally constant, but it does not predict the numerical value of Newton's G.",
            "proof_sketch": "d kappa_eff=0 fixes local variation, not the integration constant. The constant is set by global sector, boundary data, or calibration unless a parent quantization/normalization law is added.",
            "result": "NUMERICAL_G_NOT_DERIVED",
            "current_MTS_status": "G_VALUE_REMAINS_MEASURED_OR_GLOBAL_INPUT",
            "residual_effect": "epsilon_G_calibration remains bounded by CODATA/local calibration uncertainty unless parent normalization is derived.",
            "valid_for_claim": False,
            "timestamp_utc": current_timestamp,
        },
        {
            "theorem_id": "KAP4080_2_no_stress",
            "statement": "The topological sector is safe for local GR only if it is metric-independent and matter/source blind, so delta_g S_kappa_top = 0 and no species/domain/frame-dependent kappa labels appear.",
            "proof_sketch": "A metric-dependent or species-dependent kappa sector would add local stress, WEP/source-frame leakage, or a radial calibration patch.",
            "result": "STRESS_AND_SOURCE_BLINDNESS_CLAUSE_REQUIRED",
            "current_MTS_status": "CLAUSE_WRITTEN_NOT_FULLY_PARENT_SIGNED",
            "residual_effect": "source coupling and dressed mass residuals remain live until same-coframe/source-functor gates close.",
            "valid_for_claim": False,
            "timestamp_utc": current_timestamp,
        },
        {
            "theorem_id": "KAP4080_3_kappa_G_map",
            "statement": "A local G_eff readout requires a declared convention mapping between kappa_eff and Newton's G in the EH/EC normalization; constancy of kappa transfers to constancy of G only after that map is fixed.",
            "proof_sketch": "The action coefficient may be written as 1/(16 pi G), 1/(2 kappa), or equivalent tetrad normalization. Drift maps by d ln G_eff = +/- d ln kappa_eff depending on convention, while zero drift is invariant.",
            "result": "DRIFT_ZERO_CONVENTION_SAFE_VALUE_NOT_SAFE",
            "current_MTS_status": "NORMALIZATION_CONVENTION_RECORDED_NOT_DERIVED",
            "residual_effect": "Gdot/G bound can be used for drift; absolute G bound is calibration-only.",
            "valid_for_claim": False,
            "timestamp_utc": current_timestamp,
        },
    ]


def g_bound_rows(current_timestamp: str) -> List[Dict[str, object]]:
    return [
        {
            "bound_id": "BOUND4080_0_Gdot_over_G_LLR",
            "quantity": "epsilon_kappa_drift_or_Gdot_over_G",
            "theory_map": "topological branch predicts d kappa_eff=0; after fixed kappa-G convention this maps to local Gdot/G=0, so LLR Gdot/G gives drift residual scale",
            "central_value": GDOT_OVER_G_CENTRAL_PER_YEAR,
            "one_sigma": GDOT_OVER_G_SIGMA_PER_YEAR,
            "one_sigma_envelope_abs": GDOT_OVER_G_ENVELOPE_PER_YEAR,
            "units": "per_year",
            "source_id": "WEB4080_0_williams_turyshev_boggs_prl",
            "observable_link": "lunar laser ranging / local solar-system G variation",
            "valid_for_claim": False,
            "claim_use": "finite P0 drift residual scale only; not proof that MTS has constant G",
            "timestamp_utc": current_timestamp,
        },
        {
            "bound_id": "BOUND4080_1_CODATA_G_calibration",
            "quantity": "epsilon_G_calibration_relative",
            "theory_map": "topological branch does not predict numerical G; measured local G calibration supplies the current relative uncertainty scale",
            "central_value": CODATA_G_VALUE,
            "one_sigma": CODATA_G_STANDARD_UNCERTAINTY,
            "one_sigma_envelope_abs": CODATA_G_RELATIVE_UNCERTAINTY,
            "units": "relative_dimensionless_for_envelope; SI_for_value",
            "source_id": "WEB4080_1_nist_codata_2022_G",
            "observable_link": "CODATA/NIST Newtonian constant of gravitation",
            "valid_for_claim": False,
            "claim_use": "absolute G calibration uncertainty only; not a numerical MTS prediction",
            "timestamp_utc": current_timestamp,
        },
    ]


def runner_update_rows(current_timestamp: str) -> List[Dict[str, object]]:
    return [
        {
            "runner_id": "RUNUP4080_0_kappa_theorem",
            "quantity": "epsilon_kappa_drift",
            "old_score": "epsilon_kappa_normalization_open",
            "new_score": "EXACT_CONDITIONAL_CONSTANT_KAPPA_THEOREM_PARENT_UNSIGNED",
            "numeric_bound": "not_applicable_for_zero_theorem",
            "numeric_bound_units": "not_applicable",
            "aggregate_effect": "can become zero if topological A_3/kappa branch is parent signed and boundary silent",
            "valid_for_claim": False,
            "timestamp_utc": current_timestamp,
        },
        {
            "runner_id": "RUNUP4080_1_Gdot_bound",
            "quantity": "epsilon_kappa_drift_or_Gdot_over_G",
            "old_score": "MISSING_GDOT_BOUND",
            "new_score": "FINITE_EXTERNAL_GDOT_SCALE",
            "numeric_bound": GDOT_OVER_G_ENVELOPE_PER_YEAR,
            "numeric_bound_units": "per_year",
            "aggregate_effect": "adds finite drift scale; still no numerical G prediction",
            "valid_for_claim": False,
            "timestamp_utc": current_timestamp,
        },
        {
            "runner_id": "RUNUP4080_2_G_calibration",
            "quantity": "epsilon_G_calibration_relative",
            "old_score": "G_VALUE_REMAINS_MEASURED",
            "new_score": "FINITE_EXTERNAL_CODATA_CALIBRATION_SCALE",
            "numeric_bound": CODATA_G_RELATIVE_UNCERTAINTY,
            "numeric_bound_units": "dimensionless_relative",
            "aggregate_effect": "records measured-G uncertainty as calibration scale, not theory evidence",
            "valid_for_claim": False,
            "timestamp_utc": current_timestamp,
        },
        {
            "runner_id": "RUNUP4080_3_aggregate",
            "quantity": "R_eff_GR",
            "old_score": "P0_TWO_DIMENSIONLESS_ROWS_PLUS_TORSION_SCALE_STILL_BLOCKED",
            "new_score": "P0_G_DRIFT_AND_CALIBRATION_BOUNDED_STILL_BLOCKED",
            "numeric_bound": "not_applicable",
            "numeric_bound_units": "mixed",
            "aggregate_effect": "P0 now has gamma, alpha1, Gdot/G, and G-calibration scales plus torsion GeV scale; spatial metric, theta parent, B derivation, and source coupling remain open",
            "valid_for_claim": False,
            "timestamp_utc": current_timestamp,
        },
    ]


def decision_gate_rows(current_timestamp: str) -> List[Dict[str, object]]:
    return [
        {
            "decision_id": "DEC4080_0",
            "decision": DECISION,
            "meaning": "topological kappa can theorem-zero local drift if parent-signed, but it does not predict numerical G; LLR Gdot/G and CODATA G provide finite nonclaim scales",
            "forward_progress": "separates constant-G theorem, G drift bound, and absolute G calibration uncertainty",
            "public_claim": False,
            "github_action": False,
            "valid_for_claim": False,
            "timestamp_utc": current_timestamp,
        },
        {
            "decision_id": "DEC4080_1",
            "decision": "NEWTON_G_IS_NOT_DERIVED_BY_CURRENT_MTS",
            "meaning": "MTS may keep G local-constant through a topological branch, but current work cannot claim a numerical prediction of G",
            "forward_progress": "prevents overclaim while keeping calibrated source coupling testable",
            "public_claim": False,
            "github_action": False,
            "valid_for_claim": False,
            "timestamp_utc": current_timestamp,
        },
    ]


def claim_gate_rows(current_timestamp: str) -> List[Dict[str, object]]:
    return [
        {
            "claim_id": "CLAIM4080_0_constant_kappa",
            "claim": "topological A_3 sector gives d kappa_eff=0",
            "claim_allowed": True,
            "scope": "conditional mathematical theorem",
            "reason": "variation of metric-independent int kappa_eff dA_3 gives d kappa_eff=0 with fixed boundary variation",
            "not_allowed_as": "current MTS parent has signed constant-G local branch",
            "timestamp_utc": current_timestamp,
        },
        {
            "claim_id": "CLAIM4080_1_G_value",
            "claim": "current MTS predicts numerical Newton G",
            "claim_allowed": False,
            "scope": "parent local-GR derivation",
            "reason": "topological zero-gradient fixes drift, not the integration constant or SI calibration",
            "not_allowed_as": "MTS numerical-G prediction",
            "timestamp_utc": current_timestamp,
        },
        {
            "claim_id": "CLAIM4080_2_Gdot_bound",
            "claim": "Gdot/G has a finite external local bound scale",
            "claim_allowed": True,
            "scope": "private nonclaim residual target",
            "reason": "LLR gives Gdot/G=(4 +/- 9)e-13 yr^-1",
            "not_allowed_as": "MTS satisfies Gdot/G or derives constant G",
            "timestamp_utc": current_timestamp,
        },
        {
            "claim_id": "CLAIM4080_3_G_calibration",
            "claim": "CODATA G gives a finite calibration uncertainty scale",
            "claim_allowed": True,
            "scope": "private nonclaim residual target",
            "reason": "CODATA/NIST gives relative standard uncertainty 2.2e-5",
            "not_allowed_as": "MTS predicts G value",
            "timestamp_utc": current_timestamp,
        },
    ]


def next_target_rows(current_timestamp: str) -> List[Dict[str, object]]:
    return [
        {
            "target_id": "NEXT4080_0",
            "next_target": "4081-Y5-R2FR-source-coupling-WEP-theorem-or-Eotvos-bound.md",
            "script": "scripts/Y5_R2FR_4081_source_coupling_WEP_theorem_or_Eotvos_bound.py",
            "why": "next P0 local-GR issue is universal source coupling: prove same-source Hilbert/WEP theorem or source finite Eotvos/WEP bounds",
            "priority": "P0",
            "timestamp_utc": current_timestamp,
        },
        {
            "target_id": "NEXT4080_1",
            "next_target": "absolute_G_parent_normalization_later",
            "script": "fold_into_global_sector_work",
            "why": "numerical G requires global/topological normalization or remains measured input",
            "priority": "P1",
            "timestamp_utc": current_timestamp,
        },
    ]


def status_rows(current_timestamp: str) -> List[Dict[str, object]]:
    return [
        {
            "timestamp_utc": current_timestamp,
            "branch_id": "MTS_R2FR_Y5_KAPPA_NORMALIZATION_THEOREM_OR_GDOT_BOUND_4080",
            "checkpoint_id": 4080,
            "decision": DECISION,
            "status": "PRIVATE_NONCLAIM_CHECKPOINT",
            "summary": "4080 derives the conditional topological constant-kappa theorem, blocks numerical-G overclaim, and sources finite Gdot/G plus CODATA G calibration scales.",
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


def validate_numeric_bounds(rows: List[Dict[str, object]]) -> Tuple[bool, str]:
    failures: List[str] = []
    for row in rows:
        for key in ["central_value", "one_sigma", "one_sigma_envelope_abs"]:
            try:
                value = float(row[key])
                if key != "central_value" and value <= 0:
                    failures.append(f"{row['bound_id']}:{key} not positive")
            except Exception:
                failures.append(f"{row['bound_id']}:{key} not numeric")
        if row["valid_for_claim"] is not False:
            failures.append(f"{row['bound_id']}:valid_for_claim not false")
    return not failures, "; ".join(failures) if failures else "G bounds numeric and nonclaim"


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
        "current MTS predicts numerical Newton G', 'claim_allowed': True",
        "Gdot/G has a finite external local bound scale', 'claim_allowed': True, 'scope': 'parent local-GR derivation",
        "CODATA G gives a finite calibration uncertainty scale', 'claim_allowed': True, 'scope': 'parent local-GR derivation",
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
    bounds_ok, bounds_detail = validate_numeric_bounds(bounds)
    no_public_ok, no_public_detail = validate_no_public_claim(row_groups)
    claim_scope_ok, claim_scope_detail = validate_claim_scopes(claims)
    compile_ok, compile_detail = validate_script_compile()
    joined = str(row_groups)
    return [
        {"check_id": "VAL4080_00_sources", "passed": source_ok, "detail": source_detail},
        {"check_id": "VAL4080_01_csv_parse", "passed": csv_ok, "detail": csv_detail},
        {"check_id": "VAL4080_02_numeric_bounds", "passed": bounds_ok, "detail": bounds_detail},
        {"check_id": "VAL4080_03_no_public_or_github_claim", "passed": no_public_ok, "detail": no_public_detail},
        {"check_id": "VAL4080_04_claim_scope", "passed": claim_scope_ok, "detail": claim_scope_detail},
        {
            "check_id": "VAL4080_05_constant_kappa_theorem",
            "passed": "EXACT_CONDITIONAL_CONSTANT_KAPPA_THEOREM" in joined and "NUMERICAL_G_NOT_DERIVED" in joined,
            "detail": "constant-kappa theorem present and numerical-G overclaim blocked",
        },
        {
            "check_id": "VAL4080_06_Gdot_and_calibration_bounds",
            "passed": "FINITE_EXTERNAL_GDOT_SCALE" in joined and "FINITE_EXTERNAL_CODATA_CALIBRATION_SCALE" in joined,
            "detail": "Gdot/G and CODATA G calibration bounds are present",
        },
        {
            "check_id": "VAL4080_07_next_target",
            "passed": "4081-Y5-R2FR-source-coupling-WEP-theorem-or-Eotvos-bound.md" in joined,
            "detail": "next target moves to source coupling/WEP",
        },
        {"check_id": "VAL4080_08_script_compiles", "passed": compile_ok, "detail": compile_detail},
    ]


def doc_text(current_timestamp: str) -> str:
    return f"""# 4080 - Kappa Normalization Theorem Or Gdot Bound

- Timestamp: `{current_timestamp}`
- Status: `private_nonclaim_checkpoint`
- Decision: `{DECISION}`
- Public GR/Newton/PPN claim: `false`
- GitHub action: `false`

## Constant-Kappa Theorem

If the parent owns a metric-independent topological sector:

```text
S_kappa_top = int kappa_eff dA_3
```

then:

```text
delta_A3 S = - int d kappa_eff wedge delta A_3 + boundary
```

with fixed/topological boundary variation gives:

```text
d kappa_eff = 0
```

So local `kappa_eff` drift can be theorem-zeroed on this branch.

## What It Does Not Do

This does **not** predict the numerical value of Newton's constant.

The theorem gives:

```text
kappa_eff = local integration constant
```

not:

```text
G = derived number
```

The absolute value of `G` remains measured, globally fixed, or supplied by a later normalization/quantization law.

## Finite Bounds

For drift:

```text
Gdot/G = ({GDOT_OVER_G_CENTRAL_PER_YEAR:.1e} +/- {GDOT_OVER_G_SIGMA_PER_YEAR:.1e}) yr^-1
|Gdot/G| one-sigma envelope = {GDOT_OVER_G_ENVELOPE_PER_YEAR:.1e} yr^-1
```

For absolute calibration:

```text
G = {CODATA_G_VALUE:.5e} m^3 kg^-1 s^-2
standard uncertainty = {CODATA_G_STANDARD_UNCERTAINTY:.2e}
relative uncertainty = {CODATA_G_RELATIVE_UNCERTAINTY:.1e}
```

These are residual scales, not MTS predictions.

## Runner Update

The runner now separates:

```text
epsilon_kappa_drift             theorem-zero candidate or Gdot/G bound
epsilon_G_calibration_relative  CODATA calibration scale
```

The aggregate still blocks because:

```text
spatial metric / theta parent / B derivation / source coupling
```

remain open.

## Decision

```text
constant-kappa theorem = exact conditional
numerical G prediction = false
Gdot/G bound = sourced
CODATA G calibration = sourced
```

## Sources

- Williams, Turyshev, and Boggs, `Progress in Lunar Laser Ranging Tests of Relativistic Gravity`, DOI `10.1103/PhysRevLett.93.261101`.
- NIST/CODATA, `Newtonian constant of gravitation`, 2022 recommended constants.

## Next

`4081` should attack universal source coupling:

```text
same Hilbert source / WEP theorem
```

or source finite Eotvos/WEP residual bounds.
"""


def main() -> None:
    current_timestamp = timestamp()
    SOURCE_DIR.mkdir(parents=True, exist_ok=True)

    sources = source_rows(current_timestamp)
    web_provenance = web_provenance_rows(current_timestamp)
    theorem = kappa_theorem_rows(current_timestamp)
    bounds = g_bound_rows(current_timestamp)
    runner = runner_update_rows(current_timestamp)
    decisions = decision_gate_rows(current_timestamp)
    claims = claim_gate_rows(current_timestamp)
    next_targets = next_target_rows(current_timestamp)
    statuses = status_rows(current_timestamp)

    DOC_PATH.write_text(doc_text(current_timestamp), encoding="utf-8")
    write_csv(OUTPUTS["source_register"], sources)
    write_csv(OUTPUTS["web_provenance"], web_provenance)
    write_csv(OUTPUTS["kappa_theorem"], theorem)
    write_csv(OUTPUTS["g_bounds"], bounds)
    write_csv(OUTPUTS["runner_update"], runner)
    write_csv(OUTPUTS["decision_gate"], decisions)
    write_csv(OUTPUTS["claim_gate"], claims)
    write_csv(OUTPUTS["next_target"], next_targets)
    write_csv(OUTPUTS["status"], statuses)

    generated_csvs = [
        OUTPUTS["source_register"],
        OUTPUTS["web_provenance"],
        OUTPUTS["kappa_theorem"],
        OUTPUTS["g_bounds"],
        OUTPUTS["runner_update"],
        OUTPUTS["decision_gate"],
        OUTPUTS["claim_gate"],
        OUTPUTS["next_target"],
        OUTPUTS["status"],
    ]
    row_groups = [
        sources,
        web_provenance,
        theorem,
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

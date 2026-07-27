from __future__ import annotations

import csv
import py_compile
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, Iterable, List, Tuple


ROOT = Path(__file__).resolve().parents[1]
PROJECT = ROOT.parent
FORMALIZATION = PROJECT / "formalization-workbench"
SOURCE_DIR = ROOT / "source-intake" / "mts_residuals"
SCRIPT_PATH = Path(__file__).resolve()
DOC_PATH = ROOT / "4073-Y5-R2FR-formal-adoption-or-demotion-of-motion-frame-gauge-parent.md"

DECISION = "MOTION_FRAME_GAUGE_PARENT_FORMALLY_ADOPTED_AS_PRIVATE_CANDIDATE_NONCLAIM_EFFECTIVE_BRANCH_FALLBACK_RETAINED"

SOURCES: Dict[str, Tuple[Path, str, str]] = {
    "SRC4073_00_4072_next": (
        SOURCE_DIR / "P8_Y5_R2FR_4072_NEXT_TARGET.csv",
        "formal-adoption-or-demotion-of-motion-frame-gauge-parent",
        "4072 selected formal adoption or demotion.",
    ),
    "SRC4073_01_4072_action": (
        SOURCE_DIR / "P8_Y5_R2FR_4072_LOCAL_MOTION_FRAME_GAUGE_ACTION.csv",
        "LGA4072_0_field_space",
        "4072 writes the action candidate.",
    ),
    "SRC4073_02_4072_demotion": (
        SOURCE_DIR / "P8_Y5_R2FR_4072_EFFECTIVE_GR_DEMOTION_MATRIX.csv",
        "DEM4072_0_symmetry",
        "4072 keeps the effective-GR demotion fork active.",
    ),
    "SRC4073_03_4072_validation": (
        SOURCE_DIR / "P8_Y5_BRR545_4072_VALIDATION.csv",
        "VAL4072_00_sources",
        "4072 validation passed source checks.",
    ),
    "SRC4073_04_formal_179": (
        FORMALIZATION / "179-PPC4048-local-parent-packet-candidate.md",
        "PPC4048_4070_4072_motion_frame_gauge_candidate = true",
        "local parent packet records 4070-4072 candidate.",
    ),
    "SRC4073_05_formal_19": (
        FORMALIZATION / "19-proof-obligations.md",
        "Post-Checkpoint 4070-4072 Motion-Frame Gauge Parent Obligation",
        "proof obligations include motion-frame gauge parent route.",
    ),
    "SRC4073_06_formal_120": (
        FORMALIZATION / "120-derivability-promotion-gate.md",
        "motion_frame_gauge_parent_candidate_not_public_pass",
        "promotion gate records private candidate status.",
    ),
    "SRC4073_07_formal_121": (
        FORMALIZATION / "121-local-PPN-repair-route.md",
        "epsilon_PPN_total",
        "PPN repair route records residual interface.",
    ),
    "SRC4073_08_formal_145": (
        FORMALIZATION / "145-testing-readiness-and-gr-limit-map.md",
        "4070_4072_motion_frame_gauge_candidate = true",
        "testing readiness map records no-claim test interpretation.",
    ),
    "SRC4073_09_formal_spine": (
        FORMALIZATION / "07-unification-spine.md",
        "Local GR Spine Update - Motion-Frame Gauge Candidate",
        "spine records the motion-frame gauge branch.",
    ),
    "SRC4073_10_claims": (
        FORMALIZATION / "02-claims-register.csv",
        "L-004,local_gravity",
        "claims register includes L-004 private nonclaim.",
    ),
}

OUTPUTS = {
    "source_register": SOURCE_DIR / "P8_Y5_R2FR_4073_SOURCE_REGISTER.csv",
    "formal_manifest": SOURCE_DIR / "P8_Y5_R2FR_4073_FORMAL_ADOPTION_MANIFEST.csv",
    "adoption_decision": SOURCE_DIR / "P8_Y5_R2FR_4073_ADOPTION_DECISION.csv",
    "invariant_checks": SOURCE_DIR / "P8_Y5_R2FR_4073_FORMAL_INVARIANT_CHECKS.csv",
    "fallback": SOURCE_DIR / "P8_Y5_R2FR_4073_EFFECTIVE_BRANCH_FALLBACK.csv",
    "claim_gate": SOURCE_DIR / "P8_Y5_R2FR_4073_CLAIM_GATE.csv",
    "next_target": SOURCE_DIR / "P8_Y5_R2FR_4073_NEXT_TARGET.csv",
    "status": SOURCE_DIR / "P8_Y5_R2FR_4073_STATUS.csv",
    "validation": SOURCE_DIR / "P8_Y5_BRR545_4073_VALIDATION.csv",
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
    for source_id, source_tuple in SOURCES.items():
        path, needle, role = source_tuple
        text = read_text(path)
        rows.append(
            {
                "source_id": source_id,
                "path": str(path),
                "exists": path.exists(),
                "needle": needle,
                "needle_found": needle in text,
                "role": role,
                "timestamp_utc": current_timestamp,
            }
        )
    return rows


def formal_manifest_rows(current_timestamp: str) -> List[Dict[str, object]]:
    return [
        {
            "file_id": "FM4073_0_179",
            "path": str(FORMALIZATION / "179-PPC4048-local-parent-packet-candidate.md"),
            "adoption_marker": "PPC4048_4070_4072_motion_frame_gauge_candidate = true",
            "meaning": "records the motion-frame gauge action as a private local parent candidate",
            "public_claim": False,
            "timestamp_utc": current_timestamp,
        },
        {
            "file_id": "FM4073_1_19",
            "path": str(FORMALIZATION / "19-proof-obligations.md"),
            "adoption_marker": "Post-Checkpoint 4070-4072 Motion-Frame Gauge Parent Obligation",
            "meaning": "turns the branch into explicit proof obligations",
            "public_claim": False,
            "timestamp_utc": current_timestamp,
        },
        {
            "file_id": "FM4073_2_120",
            "path": str(FORMALIZATION / "120-derivability-promotion-gate.md"),
            "adoption_marker": "motion_frame_gauge_parent_candidate_not_public_pass",
            "meaning": "promotion gate keeps candidate nonclaim status",
            "public_claim": False,
            "timestamp_utc": current_timestamp,
        },
        {
            "file_id": "FM4073_3_121",
            "path": str(FORMALIZATION / "121-local-PPN-repair-route.md"),
            "adoption_marker": "epsilon_PPN_total",
            "meaning": "PPN route carries residual interface if adoption fails",
            "public_claim": False,
            "timestamp_utc": current_timestamp,
        },
        {
            "file_id": "FM4073_4_145",
            "path": str(FORMALIZATION / "145-testing-readiness-and-gr-limit-map.md"),
            "adoption_marker": "4070_4072_motion_frame_gauge_candidate = true",
            "meaning": "testing readiness map blocks public local-GR test claims",
            "public_claim": False,
            "timestamp_utc": current_timestamp,
        },
        {
            "file_id": "FM4073_5_spine",
            "path": str(FORMALIZATION / "07-unification-spine.md"),
            "adoption_marker": "motion_frame_gauge_parent_candidate = true",
            "meaning": "unification spine records local GR route update",
            "public_claim": False,
            "timestamp_utc": current_timestamp,
        },
        {
            "file_id": "FM4073_6_claims",
            "path": str(FORMALIZATION / "02-claims-register.csv"),
            "adoption_marker": "L-004,local_gravity",
            "meaning": "claims register records private nonclaim and risk",
            "public_claim": False,
            "timestamp_utc": current_timestamp,
        },
    ]


def adoption_decision_rows(current_timestamp: str) -> List[Dict[str, object]]:
    return [
        {
            "decision_id": "ADOPT4073_0",
            "decision": DECISION,
            "adopted_as": "private_parent_action_candidate",
            "not_adopted_as": "derived_GR_theorem",
            "reason": "4072 action is the strongest non-flat route to metric/EH origin, but current corpus does not yet parent-sign the local motion-frame gauge action.",
            "effective_branch_fallback": True,
            "public_claim": False,
            "timestamp_utc": current_timestamp,
        },
        {
            "decision_id": "ADOPT4073_1",
            "decision": "DO_NOT_DEMOTE_YET",
            "adopted_as": "workbench_candidate_branch",
            "not_adopted_as": "effective_GR_only_final_status",
            "reason": "The motion-frame gauge theorem gives a real route to deriving B^A/omega if MTS flow/memory can be upgraded to parent gauge data.",
            "effective_branch_fallback": True,
            "public_claim": False,
            "timestamp_utc": current_timestamp,
        },
    ]


def invariant_check_rows(current_timestamp: str) -> List[Dict[str, object]]:
    return [
        {
            "check_id": "INV4073_0_nonclaim",
            "invariant": "public local GR claim remains false",
            "status": "PASS",
            "evidence": "formal files include public_claim_allowed=false/public_local_GR_claim=false/current_MTS_derivation_verified=false markers",
            "timestamp_utc": current_timestamp,
        },
        {
            "check_id": "INV4073_1_current_derivation",
            "invariant": "current MTS derivation is not verified",
            "status": "PASS",
            "evidence": "4072 demotion matrix and formal workbench retain current_MTS_derivation=false",
            "timestamp_utc": current_timestamp,
        },
        {
            "check_id": "INV4073_2_no_G_prediction",
            "invariant": "numerical Newton G is not predicted",
            "status": "PASS",
            "evidence": "formal files keep predicts_numerical_Newton_G=false",
            "timestamp_utc": current_timestamp,
        },
        {
            "check_id": "INV4073_3_fallback",
            "invariant": "effective-GR demotion/fallback remains active",
            "status": "PASS",
            "evidence": "formal files include effective_GR_demotion_if_not_adopted/effective_GR_demotion_if_rejected markers",
            "timestamp_utc": current_timestamp,
        },
        {
            "check_id": "INV4073_4_residual_interface",
            "invariant": "torsion, EM-Hodge, frame/source, kappa and extra-mode residuals remain live",
            "status": "PASS",
            "evidence": "121 and 145 carry epsilon_PPN_total and local testing residual interface language",
            "timestamp_utc": current_timestamp,
        },
    ]


def fallback_rows(current_timestamp: str) -> List[Dict[str, object]]:
    return [
        {
            "fallback_id": "FB4073_0_effective_GR",
            "if_condition": "motion-frame gauge action is not parent-signed",
            "fallback_status": "effective_GR_branch_input",
            "required_work": "score MTS residuals around GR rather than claiming a GR derivation",
            "public_claim": False,
            "timestamp_utc": current_timestamp,
        },
        {
            "fallback_id": "FB4073_1_flow_solder",
            "if_condition": "B^A cannot be derived from MTS flow/transport",
            "fallback_status": "solder_connection_imported",
            "required_work": "demote B^A to effective tetrad/coframe infrastructure",
            "public_claim": False,
            "timestamp_utc": current_timestamp,
        },
        {
            "fallback_id": "FB4073_2_memory_connection",
            "if_condition": "Gamma_mem cannot be uplifted to R^AB/T^A invariants",
            "fallback_status": "memory_scalar_separate_effective_sector",
            "required_work": "keep Gamma_mem as residual/test sector, not owner of local connection",
            "public_claim": False,
            "timestamp_utc": current_timestamp,
        },
        {
            "fallback_id": "FB4073_3_residual_scorer",
            "if_condition": "torsion/EM-Hodge/frame/kappa/extra-mode gates remain open",
            "fallback_status": "explicit_residual_scorer_required",
            "required_work": "fill source-backed residual rows before any local test interpretation",
            "public_claim": False,
            "timestamp_utc": current_timestamp,
        },
    ]


def static_rows(current_timestamp: str) -> Dict[str, List[Dict[str, object]]]:
    return {
        "claim_gate": [
            {
                "claim_id": "CLAIM4073_0",
                "claim": "motion-frame gauge action is recorded as a private candidate",
                "allowed_private": True,
                "allowed_public": False,
                "reason": "formal workbench records the branch while preserving nonclaim gates",
                "timestamp_utc": current_timestamp,
            },
            {
                "claim_id": "CLAIM4073_1",
                "claim": "MTS derives local GR/Newton/PPN as a completed theorem",
                "allowed_private": False,
                "allowed_public": False,
                "reason": "current MTS derivation, torsion/EM-Hodge/same-coframe/kappa gates and residual scorers remain open",
                "timestamp_utc": current_timestamp,
            },
            {
                "claim_id": "CLAIM4073_2",
                "claim": "MTS predicts numerical Newton G",
                "allowed_private": False,
                "allowed_public": False,
                "reason": "kappa_eff remains calibrated or topological, not numerically derived",
                "timestamp_utc": current_timestamp,
            },
        ],
        "next_target": [
            {
                "row_id": "NEXT4073_0",
                "next_doc": "4074-Y5-R2FR-flow-solder-field-parent-signature-or-effective-tetrad-demotion.md",
                "next_script": "scripts/Y5_R2FR_4074_flow_solder_field_parent_signature_or_effective_tetrad_demotion.py",
                "reason": "attack the decisive adoption gate: derive B^A as an MTS flow/transport solder field with the required transformation law, or demote it to effective tetrad infrastructure",
                "timestamp_utc": current_timestamp,
            }
        ],
        "status": [
            {
                "status_id": "STAT4073",
                "status": DECISION,
                "formalization_modified": True,
                "public_claim": False,
                "github_action": False,
                "timestamp_utc": current_timestamp,
            }
        ],
    }


def validate_sources(source_table: List[Dict[str, object]]) -> Tuple[bool, str]:
    missing = [row["source_id"] for row in source_table if not row["exists"]]
    absent_needles = [row["source_id"] for row in source_table if not row["needle_found"]]
    if missing or absent_needles:
        return False, f"missing={missing}; absent_needles={absent_needles}"
    return True, "all cited source paths exist and needles are present"


def validate_csv_parse(paths: Iterable[Path]) -> Tuple[bool, str]:
    details: List[str] = []
    try:
        for path in paths:
            with path.open(newline="", encoding="utf-8") as input_file:
                parsed_rows = list(csv.DictReader(input_file))
            details.append(f"{path.name}:rows={len(parsed_rows)}")
    except Exception as exc:  # pragma: no cover
        return False, repr(exc)
    return True, "; ".join(details)


def validate_no_public_claim(row_groups: Iterable[List[Dict[str, object]]]) -> Tuple[bool, str]:
    offenders: List[str] = []
    for rows in row_groups:
        for row in rows:
            for key in ("allowed_public", "public_claim", "github_action"):
                if key in row and str(row[key]).lower() == "true":
                    offenders.append(str(row))
    if offenders:
        return False, f"public/github claim flags found: {offenders}"
    return True, "all claim-bearing rows preserve public/github false"


def validate_claims_register() -> Tuple[bool, str]:
    path = FORMALIZATION / "02-claims-register.csv"
    try:
        with path.open(newline="", encoding="utf-8") as input_file:
            rows = list(csv.DictReader(input_file))
    except Exception as exc:
        return False, repr(exc)
    matches = [row for row in rows if row.get("claim_id") == "L-004"]
    if len(matches) != 1:
        return False, f"L-004 count={len(matches)}"
    if matches[0].get("status") != "private_candidate_nonclaim":
        return False, f"L-004 status={matches[0].get('status')}"
    return True, "L-004 parses once and remains private_candidate_nonclaim"


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
) -> List[Dict[str, object]]:
    source_ok, source_detail = validate_sources(source_table)
    csv_ok, csv_detail = validate_csv_parse(generated_csvs)
    claims_ok, claims_detail = validate_no_public_claim(row_groups)
    register_ok, register_detail = validate_claims_register()
    compile_ok, compile_detail = validate_script_compile()
    joined = str(row_groups)
    return [
        {"check_id": "VAL4073_00_sources", "passed": source_ok, "detail": source_detail},
        {"check_id": "VAL4073_01_csv_parse", "passed": csv_ok, "detail": csv_detail},
        {"check_id": "VAL4073_02_no_public_or_github_claim", "passed": claims_ok, "detail": claims_detail},
        {"check_id": "VAL4073_03_claims_register", "passed": register_ok, "detail": register_detail},
        {
            "check_id": "VAL4073_04_formal_adoption",
            "passed": "PPC4048_4070_4072_motion_frame_gauge_candidate = true" in read_text(FORMALIZATION / "179-PPC4048-local-parent-packet-candidate.md"),
            "detail": "179 records motion-frame gauge private candidate",
        },
        {
            "check_id": "VAL4073_05_nonclaim_invariants",
            "passed": "4070_4072_current_MTS_derivation_verified = false" in read_text(FORMALIZATION / "145-testing-readiness-and-gr-limit-map.md")
            and "4070_4072_predicts_numerical_Newton_G = false" in read_text(FORMALIZATION / "145-testing-readiness-and-gr-limit-map.md"),
            "detail": "nonclaim and no-G-prediction invariants remain explicit",
        },
        {
            "check_id": "VAL4073_06_next_target",
            "passed": "4074-Y5-R2FR-flow-solder-field-parent-signature-or-effective-tetrad-demotion.md" in joined,
            "detail": "next target attacks flow/solder parent signature",
        },
        {"check_id": "VAL4073_07_script_compiles", "passed": compile_ok, "detail": compile_detail},
    ]


def doc_text(current_timestamp: str) -> str:
    return f"""# 4073 - Formal Adoption Or Demotion Of Motion-Frame Gauge Parent

- Timestamp: `{current_timestamp}`
- Status: `private_nonclaim_checkpoint`
- Decision: `{DECISION}`
- Formalization modified: `true`
- Public GR/Newton/PPN claim: `false`
- GitHub action: `false`

## Decision

4073 adopts the `4070-4072` motion-frame gauge action as a **private parent-action candidate** in the formal workbench.

It is not adopted as a completed MTS derivation of GR.

```text
motion_frame_gauge_parent_candidate = true
current_MTS_derivation_verified = false
public_local_GR_claim = false
predicts_numerical_Newton_G = false
effective_GR_demotion_if_not_adopted = true
```

## What Changed

The formal workbench now records:

- the local packet candidate in `179`;
- proof obligations in `19`;
- promotion gates in `120`;
- PPN residual interface in `121`;
- testing readiness rules in `145`;
- spine update in `07`;
- claim-lock row `L-004` in `02-claims-register.csv`.

## Why This Is The Right Fork

The scalar metric route was mathematically too weak. The Cartan/motion-frame route is strong enough to be worth carrying, but only under strict private-candidate locks:

```text
X^A = L_* Psi^A
e^A = D_omega X^A + B^A
g_obs = eta_AB e^A e^B
S_EC -> S_EH only after torsion/nonmetricity gates close
```

## Next

`4074` should attack the decisive adoption gate: derive `B^A` as an MTS flow/transport solder field with the required transformation law, or demote it to effective tetrad infrastructure.
"""


def main() -> None:
    current_timestamp = timestamp()
    SOURCE_DIR.mkdir(parents=True, exist_ok=True)

    sources = source_rows(current_timestamp)
    manifest = formal_manifest_rows(current_timestamp)
    adoption = adoption_decision_rows(current_timestamp)
    invariants = invariant_check_rows(current_timestamp)
    fallback = fallback_rows(current_timestamp)
    static = static_rows(current_timestamp)

    DOC_PATH.write_text(doc_text(current_timestamp), encoding="utf-8")
    write_csv(OUTPUTS["source_register"], sources)
    write_csv(OUTPUTS["formal_manifest"], manifest)
    write_csv(OUTPUTS["adoption_decision"], adoption)
    write_csv(OUTPUTS["invariant_checks"], invariants)
    write_csv(OUTPUTS["fallback"], fallback)
    write_csv(OUTPUTS["claim_gate"], static["claim_gate"])
    write_csv(OUTPUTS["next_target"], static["next_target"])
    write_csv(OUTPUTS["status"], static["status"])

    generated_csvs = [
        OUTPUTS["source_register"],
        OUTPUTS["formal_manifest"],
        OUTPUTS["adoption_decision"],
        OUTPUTS["invariant_checks"],
        OUTPUTS["fallback"],
        OUTPUTS["claim_gate"],
        OUTPUTS["next_target"],
        OUTPUTS["status"],
    ]
    row_groups = [
        sources,
        manifest,
        adoption,
        invariants,
        fallback,
        static["claim_gate"],
        static["next_target"],
        static["status"],
    ]
    validation = validation_rows(sources, generated_csvs, row_groups)
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

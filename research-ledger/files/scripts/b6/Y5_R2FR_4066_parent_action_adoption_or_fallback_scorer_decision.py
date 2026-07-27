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
DOC_PATH = ROOT / "4066-Y5-R2FR-parent-action-adoption-or-fallback-scorer-decision.md"

DECISION = "PARENT_ACTION_ADOPTION_FIRST_WITH_FALLBACK_SCORER_SHELL_READY"

SOURCES: Dict[str, Tuple[Path, str, str]] = {
    "SRC4066_00_4065_next": (
        SOURCE_DIR / "P8_Y5_R2FR_4065_NEXT_TARGET.csv",
        "parent-action adoption proof or build executable fallback scorer rows",
        "4065 selected this fork decision.",
    ),
    "SRC4066_01_4065_decision": (
        SOURCE_DIR / "P8_Y5_R2FR_4065_DECISION_GATE.csv",
        "GUARDED_FORMAL_APPLICATION_VERIFIED_NONCLAIM",
        "4065 verified the formal guarded chain.",
    ),
    "SRC4066_02_4056_adoption": (
        SOURCE_DIR / "P8_Y5_R2FR_4056_PACKET_ADOPTION_GATE.csv",
        "ADOPT4056_0_one_action",
        "4056 adoption gates define the parent-action target.",
    ),
    "SRC4066_03_4056_fallback": (
        SOURCE_DIR / "P8_Y5_R2FR_4056_DELTAK_FALLBACK_BOUND_VECTOR.csv",
        "DK4056_0_DeltaK",
        "4056 fallback bound families.",
    ),
    "SRC4066_04_4060_fallback": (
        SOURCE_DIR / "P8_Y5_R2FR_4060_CHAIN_FALLBACK_BOUND_VECTOR.csv",
        "CB4060_2_quadratic_remainder",
        "4060 chain/quadratic fallback family.",
    ),
    "SRC4066_05_4061_fallback": (
        SOURCE_DIR / "P8_Y5_R2FR_4061_FALLBACK_BOUND_VECTOR.csv",
        "MASTER_NO_CANCELLATION_BOUND_ACTIVE_UNTIL_PARENT_ADOPTION",
        "4061 CDB fallback family.",
    ),
    "SRC4066_06_4062_fallback": (
        SOURCE_DIR / "P8_Y5_R2FR_4062_FALLBACK_BOUND_VECTOR.csv",
        "FB4062_4_master",
        "4062 calibration and derivative-hair fallback family.",
    ),
    "SRC4066_07_4063_fallback": (
        SOURCE_DIR / "P8_Y5_R2FR_4063_RESIDUAL_FALLBACK_VECTOR.csv",
        "RFB4063_4_master",
        "4063 weak-field readout fallback family.",
    ),
    "SRC4066_08_formal_179": (
        FORMALIZATION / "179-PPC4048-local-parent-packet-candidate.md",
        "fallback_required_if_any_parent_clause_rejected = true",
        "formal packet file records the adoption-vs-fallback rule.",
    ),
    "SRC4066_09_formal_120": (
        FORMALIZATION / "120-derivability-promotion-gate.md",
        "or every rejected clause is routed to its explicit fallback scorer",
        "formal promotion gate preserves fallback rule.",
    ),
    "SRC4066_10_claims_l003": (
        FORMALIZATION / "02-claims-register.csv",
        "Run final parent-action adoption or fallback scorer verification",
        "claims register L-003 names the next proof/scorer fork.",
    ),
}

OUTPUTS = {
    "source_register": SOURCE_DIR / "P8_Y5_R2FR_4066_SOURCE_REGISTER.csv",
    "fork_matrix": SOURCE_DIR / "P8_Y5_R2FR_4066_ADOPTION_VS_SCORER_FORK_MATRIX.csv",
    "adoption_targets": SOURCE_DIR / "P8_Y5_R2FR_4066_PARENT_ACTION_ADOPTION_TARGETS.csv",
    "fallback_scorer_shell": SOURCE_DIR / "P8_Y5_R2FR_4066_FALLBACK_SCORER_SHELL.csv",
    "route_decision": SOURCE_DIR / "P8_Y5_R2FR_4066_ROUTE_DECISION.csv",
    "claim_gate": SOURCE_DIR / "P8_Y5_R2FR_4066_CLAIM_GATE.csv",
    "next_target": SOURCE_DIR / "P8_Y5_R2FR_4066_NEXT_TARGET.csv",
    "status": SOURCE_DIR / "P8_Y5_R2FR_4066_STATUS.csv",
    "validation": SOURCE_DIR / "P8_Y5_BRR545_4066_VALIDATION.csv",
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


def fork_matrix_rows(current_timestamp: str) -> List[Dict[str, object]]:
    return [
        {
            "route_id": "FORK4066_A",
            "route": "parent_action_adoption_first",
            "what_it_tries": "prove the selected local branch is one action-level parent packet rather than stitched closure rows",
            "evidence_for": "4060-4065 create a coherent guarded chain with all formal guards passing",
            "risk": "if action ownership fails, the branch drops to fallback scorers",
            "score": 3,
            "selected": True,
            "timestamp_utc": current_timestamp,
        },
        {
            "route_id": "FORK4066_B",
            "route": "fallback_scorer_first",
            "what_it_tries": "build executable scorer rows before further adoption proof",
            "evidence_for": "fallback formulas exist for Delta_K, source slots, scalar charge, CDB, c_norm, and weak-field residuals",
            "risk": "most fallback rows still need numeric/source inputs, so this quickly becomes data acquisition rather than derivation",
            "score": 1,
            "selected": False,
            "timestamp_utc": current_timestamp,
        },
        {
            "route_id": "FORK4066_C",
            "route": "mixed_adoption_with_scorer_shell",
            "what_it_tries": "pursue parent-action adoption while keeping a normalized scorer shell ready for failed clauses",
            "evidence_for": "matches formal adoption rule: adopt each clause or demote it to a named fallback row",
            "risk": "requires disciplined split so fallback shell is not mistaken for passed bounds",
            "score": 2,
            "selected": True,
            "timestamp_utc": current_timestamp,
        },
    ]


def adoption_target_rows(current_timestamp: str) -> List[Dict[str, object]]:
    return [
        {
            "target_id": "ADOPT4066_0_one_action",
            "clause": "one local <=2PN parent packet",
            "must_show": "all local terms are clauses of one parent action, not stitched closure patches",
            "source_gate": "ADOPT4056_0_one_action",
            "failure_route": "entire local branch remains closure/fallback",
            "priority": "highest",
            "timestamp_utc": current_timestamp,
        },
        {
            "target_id": "ADOPT4066_1_EH_same_source",
            "clause": "EH plus same-source matter/EM/binding",
            "must_show": "observed metric equation is EH with one Hilbert source through <=2PN",
            "source_gate": "WFA4063_0_action and WFA4063_2_source",
            "failure_route": "R_nonEH, source_mismatch, source_slot fallback rows",
            "priority": "highest",
            "timestamp_utc": current_timestamp,
        },
        {
            "target_id": "ADOPT4066_2_Gamma_Khat",
            "clause": "Gamma_ren/K_Gamma Hilbert owner",
            "must_show": "S_GK=-int sqrt|g| Gamma_ren+B_GK; T_GK=T_Hilbert_GK; Khat=K_Gamma; D_GK=0",
            "source_gate": "ADOPT4056_2_q_loc plus 4060 normal-ordering",
            "failure_route": "Delta_K, chain, and quadratic fallback rows",
            "priority": "highest",
            "timestamp_utc": current_timestamp,
        },
        {
            "target_id": "ADOPT4066_3_scalar_boundary",
            "clause": "scalar no-flux/no-boundary-source",
            "must_show": "natural no-flux boundary and fixed outer reference remove local scalar charge",
            "source_gate": "ADOPT4056_3_scalar_charge",
            "failure_route": "Q_phi Yukawa/harmonic scalar-charge fallback",
            "priority": "high",
            "timestamp_utc": current_timestamp,
        },
        {
            "target_id": "ADOPT4066_4_side_channels",
            "clause": "boundary/projector/memory/source-normalization silence",
            "must_show": "4061 CDB kernels, 4046 memory reset, 4047 c_norm zero, and 4062 calibrated-G_N firewall are parent-owned",
            "source_gate": "ADOPT4056_4_side_channels",
            "failure_route": "CDB, cZ, c_norm, alpha/xi, Gdot/range/species fallback rows",
            "priority": "high",
            "timestamp_utc": current_timestamp,
        },
        {
            "target_id": "ADOPT4066_5_readout_firewall",
            "clause": "post-variation local readout",
            "must_show": "PPN, R10, clocks, orbital, EM, and cosmology are tests/readouts, not action-fitting inputs",
            "source_gate": "LAP4056_7_readout_firewall and 4062/4063 no numerical-G guards",
            "failure_route": "public claim blocked and empirical rows quarantined",
            "priority": "high",
            "timestamp_utc": current_timestamp,
        },
    ]


def fallback_shell_rows(current_timestamp: str) -> List[Dict[str, object]]:
    return [
        {
            "shell_id": "SCORE4066_0_DeltaK",
            "failed_clause": "Gamma/Khat adoption rejected",
            "source_rows": "DK4056_0_DeltaK; CB4060_0..2",
            "minimum_inputs": "Delta_K profile, length scale, projector coefficients, Hessian/amplitude if quadratic remainder survives",
            "claim_state": "schema_only_numeric_inputs_missing",
            "timestamp_utc": current_timestamp,
        },
        {
            "shell_id": "SCORE4066_1_source_slots",
            "failed_clause": "hidden matter/EM source-slot silence rejected",
            "source_rows": "DK4056_1_source_slot; RFB4063_1_source_mismatch",
            "minimum_inputs": "c_T, c_EM, source profiles, composition/readout map, mu_extra decomposition",
            "claim_state": "schema_only_numeric_inputs_missing",
            "timestamp_utc": current_timestamp,
        },
        {
            "shell_id": "SCORE4066_2_scalar_charge",
            "failed_clause": "scalar no-flux/no-boundary-source rejected",
            "source_rows": "DK4056_2_scalar_charge",
            "minimum_inputs": "Q_phi, mu_phi, boundary data, multipole convention",
            "claim_state": "schema_only_numeric_inputs_missing",
            "timestamp_utc": current_timestamp,
        },
        {
            "shell_id": "SCORE4066_3_CDB_side_channels",
            "failed_clause": "connection/domain/boundary selected branch rejected",
            "source_rows": "FB4061_0..4",
            "minimum_inputs": "non-LC norm, source-domain connection slopes, projector/domain derivatives, boundary flux/reference/corner profiles",
            "claim_state": "schema_only_numeric_inputs_missing",
            "timestamp_utc": current_timestamp,
        },
        {
            "shell_id": "SCORE4066_4_calibration_derivative_hair",
            "failed_clause": "fixed universal coupling or source-normalization silence rejected",
            "source_rows": "FB4062_1..4; RFB4063_3",
            "minimum_inputs": "Gdot, range/radial derivative, WEP/species, frame and extra-source bounds",
            "claim_state": "schema_only_numeric_inputs_missing",
            "timestamp_utc": current_timestamp,
        },
        {
            "shell_id": "SCORE4066_5_PPN_weakfield",
            "failed_clause": "EH weak-field readout assumptions rejected",
            "source_rows": "RFB4063_0..4; PPN4063 fallback rows",
            "minimum_inputs": "nonEH operator basis, beta/gamma projection, frame map, PPN residual weights",
            "claim_state": "schema_only_numeric_inputs_missing",
            "timestamp_utc": current_timestamp,
        },
    ]


def static_rows(current_timestamp: str) -> Dict[str, List[Dict[str, object]]]:
    return {
        "route_decision": [
            {
                "decision_id": "DEC4066_0",
                "decision": DECISION,
                "reason": "the chain is coherent enough to attempt action-level adoption, while fallback rows are mostly schema-ready but numeric/source-missing",
                "public_claim": False,
                "valid_for_public_claim": False,
                "timestamp_utc": current_timestamp,
            }
        ],
        "claim_gate": [
            {
                "claim_id": "CLAIM4066_0",
                "claim": "best next route is parent-action adoption proof first with fallback scorer shell retained",
                "allowed_private": True,
                "allowed_public": False,
                "reason": "route-selection checkpoint only; does not prove adoption",
                "timestamp_utc": current_timestamp,
            },
            {
                "claim_id": "CLAIM4066_1",
                "claim": "fallback scorer rows are numerically executable for claims",
                "allowed_private": False,
                "allowed_public": False,
                "reason": "minimum numeric/source inputs are still missing",
                "timestamp_utc": current_timestamp,
            },
            {
                "claim_id": "CLAIM4066_2",
                "claim": "MTS publicly derives local GR/Newton/PPN",
                "allowed_private": False,
                "allowed_public": False,
                "reason": "parent-action adoption proof has not yet been completed",
                "timestamp_utc": current_timestamp,
            },
        ],
        "next_target": [
            {
                "row_id": "NEXT4066_0",
                "next_doc": "4067-Y5-R2FR-single-local-parent-action-adoption-proof-or-failure-map.md",
                "next_script": "scripts/Y5_R2FR_4067_single_local_parent_action_adoption_proof_or_failure_map.py",
                "reason": "attack the one-action parent adoption proof directly before spending work on numeric fallback acquisition",
                "timestamp_utc": current_timestamp,
            }
        ],
        "status": [
            {
                "status_id": "STAT4066",
                "status": DECISION,
                "formalization_modified": False,
                "public_claim": False,
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
            for key in ("valid_for_public_claim", "allowed_public", "public_claim"):
                if key in row and str(row[key]).lower() == "true":
                    offenders.append(str(row))
    if offenders:
        return False, f"public claim flags found: {offenders}"
    return True, "all claim-bearing rows preserve public false"


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
    compile_ok, compile_detail = validate_script_compile()
    joined = str(row_groups)
    return [
        {"check_id": "VAL4066_00_sources", "passed": source_ok, "detail": source_detail},
        {"check_id": "VAL4066_01_csv_parse", "passed": csv_ok, "detail": csv_detail},
        {"check_id": "VAL4066_02_no_public_claim", "passed": claims_ok, "detail": claims_detail},
        {
            "check_id": "VAL4066_03_decision_selected",
            "passed": DECISION in joined,
            "detail": "route decision selects parent-action adoption first with scorer shell retained",
        },
        {
            "check_id": "VAL4066_04_fallback_numeric_blocked",
            "passed": "schema_only_numeric_inputs_missing" in joined,
            "detail": "fallback scorer rows remain nonclaim because numeric/source inputs are missing",
        },
        {
            "check_id": "VAL4066_05_next_target",
            "passed": "4067-Y5-R2FR-single-local-parent-action-adoption-proof-or-failure-map.md" in joined,
            "detail": "next target points to single-parent-action adoption proof",
        },
        {"check_id": "VAL4066_06_script_compiles", "passed": compile_ok, "detail": compile_detail},
    ]


def doc_text(current_timestamp: str) -> str:
    return f"""# 4066 - Parent-Action Adoption or Fallback Scorer Decision

- Timestamp: `{current_timestamp}`
- Status: `private_nonclaim_checkpoint`
- Decision: `{DECISION}`
- Public local-GR claim: `false`

## Decision

The best next route is parent-action adoption proof first, with the fallback scorer shell retained.

Reason:

- `4060-4065` now form a coherent guarded local-GR chain.
- The formal workbench accepts the chain only as private/nonclaim.
- Fallback formulas exist, but most are still schema-only because numeric/source inputs are missing.

So the next useful move is not to chase every numeric fallback row yet. It is to test the stronger claim:

```text
Can the selected local branch be owned by one parent action?
```

If yes, the local GR/Newton/PPN route becomes much stronger. If no, the scorer shell in `P8_Y5_R2FR_4066_FALLBACK_SCORER_SHELL.csv` names exactly what must be filled.

## Guard

This decision does not prove adoption and does not allow a public local-GR claim.

```text
formal_adoption_verified = false
fallback_required_if_any_parent_clause_rejected = true
public_local_GR_claim = false
```

## Next

`4067` should attempt the single-local-parent-action adoption proof or produce a failure map.
"""


def main() -> None:
    current_timestamp = timestamp()
    SOURCE_DIR.mkdir(parents=True, exist_ok=True)

    sources = source_rows(current_timestamp)
    fork_matrix = fork_matrix_rows(current_timestamp)
    adoption_targets = adoption_target_rows(current_timestamp)
    fallback_shell = fallback_shell_rows(current_timestamp)
    static = static_rows(current_timestamp)

    DOC_PATH.write_text(doc_text(current_timestamp), encoding="utf-8")
    write_csv(OUTPUTS["source_register"], sources)
    write_csv(OUTPUTS["fork_matrix"], fork_matrix)
    write_csv(OUTPUTS["adoption_targets"], adoption_targets)
    write_csv(OUTPUTS["fallback_scorer_shell"], fallback_shell)
    write_csv(OUTPUTS["route_decision"], static["route_decision"])
    write_csv(OUTPUTS["claim_gate"], static["claim_gate"])
    write_csv(OUTPUTS["next_target"], static["next_target"])
    write_csv(OUTPUTS["status"], static["status"])

    generated_csvs = [
        OUTPUTS["source_register"],
        OUTPUTS["fork_matrix"],
        OUTPUTS["adoption_targets"],
        OUTPUTS["fallback_scorer_shell"],
        OUTPUTS["route_decision"],
        OUTPUTS["claim_gate"],
        OUTPUTS["next_target"],
        OUTPUTS["status"],
    ]
    row_groups = [
        sources,
        fork_matrix,
        adoption_targets,
        fallback_shell,
        static["route_decision"],
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
    print(f"decision: {static['route_decision'][0]['decision']}")
    print(f"validation rows: {len(validation)}")
    print(f"validation failures: {len(failures)}")
    for failure in failures:
        print(f"FAIL {failure['check_id']}: {failure['detail']}")


if __name__ == "__main__":
    main()

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
DOC_PATH = ROOT / "4067-Y5-R2FR-single-local-parent-action-adoption-proof-or-failure-map.md"

DECISION = "LOCAL_SINGLE_ACTION_SKELETON_CONSTRUCTED_CONDITIONALLY_GLOBAL_PARENT_DESCENT_OPEN"

SOURCES: Dict[str, Tuple[Path, str, str]] = {
    "SRC4067_00_4066_next": (
        SOURCE_DIR / "P8_Y5_R2FR_4066_NEXT_TARGET.csv",
        "single-local-parent-action-adoption-proof-or-failure-map",
        "4066 selected direct parent-action adoption proof attempt.",
    ),
    "SRC4067_01_4066_decision": (
        SOURCE_DIR / "P8_Y5_R2FR_4066_ROUTE_DECISION.csv",
        "PARENT_ACTION_ADOPTION_FIRST_WITH_FALLBACK_SCORER_SHELL_READY",
        "4066 chose adoption proof first.",
    ),
    "SRC4067_02_4056_packet": (
        SOURCE_DIR / "P8_Y5_R2FR_4056_LOCAL_PARENT_ACTION_PACKET.csv",
        "LAP4056_0_field_space",
        "4056 defines the local field space and packet clauses.",
    ),
    "SRC4067_03_4056_theorem": (
        SOURCE_DIR / "P8_Y5_R2FR_4056_CONDITIONAL_LOCAL_GR_THEOREM.csv",
        "LGT4056_0_packet",
        "4056 gives the conditional theorem if packet clauses are adopted.",
    ),
    "SRC4067_04_4055_hilbert": (
        SOURCE_DIR / "P8_Y5_R2FR_4055_HILBERT_RESPONSE_DEFINITION.csv",
        "HRD4055_1_parent_action",
        "4055 defines S_GK and the Hilbert owner.",
    ),
    "SRC4067_05_4054_scalar": (
        SOURCE_DIR / "P8_Y5_R2FR_4054_NATURAL_NO_FLUX_SCALAR_CHARGE_THEOREM.csv",
        "NFL4054_2_natural_inner_boundary",
        "4054 supplies scalar no-flux charge silence.",
    ),
    "SRC4067_06_4061_cdb": (
        SOURCE_DIR / "P8_Y5_R2FR_4061_DECISION_GATE.csv",
        "CONNECTION_DOMAIN_BOUNDARY_KERNELS_ZERO",
        "4061 supplies selected CDB kernel silence.",
    ),
    "SRC4067_07_4062_calib": (
        SOURCE_DIR / "P8_Y5_R2FR_4062_CNORM_NEWTON_G_CALIBRATION_LAW.csv",
        "CNG4062_2_calibration_firewall",
        "4062 supplies calibrated-G_N firewall.",
    ),
    "SRC4067_08_4063_weakfield": (
        SOURCE_DIR / "P8_Y5_R2FR_4063_WEAK_FIELD_ASSUMPTION_CONTRACT.csv",
        "WFA4063_0_action",
        "4063 supplies weak-field action assumptions.",
    ),
    "SRC4067_09_formal_179": (
        FORMALIZATION / "179-PPC4048-local-parent-packet-candidate.md",
        "PPC4048_4060_4063_guarded_chain_candidate = true",
        "formal workbench records guarded chain.",
    ),
    "SRC4067_10_formal_claims": (
        FORMALIZATION / "02-claims-register.csv",
        "L-003,local_gravity",
        "claims register keeps 4060-4063 private nonclaim.",
    ),
}

OUTPUTS = {
    "source_register": SOURCE_DIR / "P8_Y5_R2FR_4067_SOURCE_REGISTER.csv",
    "single_action_skeleton": SOURCE_DIR / "P8_Y5_R2FR_4067_SINGLE_ACTION_SKELETON.csv",
    "compatibility_proof": SOURCE_DIR / "P8_Y5_R2FR_4067_VARIATIONAL_COMPATIBILITY_PROOF.csv",
    "adoption_result": SOURCE_DIR / "P8_Y5_R2FR_4067_ADOPTION_RESULT.csv",
    "failure_map": SOURCE_DIR / "P8_Y5_R2FR_4067_FAILURE_MAP.csv",
    "claim_gate": SOURCE_DIR / "P8_Y5_R2FR_4067_CLAIM_GATE.csv",
    "next_target": SOURCE_DIR / "P8_Y5_R2FR_4067_NEXT_TARGET.csv",
    "status": SOURCE_DIR / "P8_Y5_R2FR_4067_STATUS.csv",
    "validation": SOURCE_DIR / "P8_Y5_BRR545_4067_VALIDATION.csv",
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


def single_action_skeleton_rows(current_timestamp: str) -> List[Dict[str, object]]:
    return [
        {
            "term_id": "SKEL4067_0_field_space",
            "term": "Q_parent^loc",
            "definition": "Q_parent^loc = Met_obs x Matter x EM x K_G x Aux_GK x Aux_private with q:Q_parent^loc -> Met_obs",
            "role": "one local variation domain for all selected-branch clauses",
            "owned_by_single_action": True,
            "timestamp_utc": current_timestamp,
        },
        {
            "term_id": "SKEL4067_1_EH",
            "term": "S_EH[g_obs;kappa_*]+S_GHY[g_obs]",
            "definition": "Einstein-Hilbert observed metric block with fixed local coupling",
            "role": "owns local GR/Newton/PPN baseline",
            "owned_by_single_action": True,
            "timestamp_utc": current_timestamp,
        },
        {
            "term_id": "SKEL4067_2_matter_EM",
            "term": "S_matter[psi,g_obs,theta]+S_EM[A,g_obs]+S_binding",
            "definition": "ordinary same-frame/same-Hilbert-source matter, EM, and binding stress",
            "role": "source of T_H and Newtonian M_H without hidden source weights",
            "owned_by_single_action": True,
            "timestamp_utc": current_timestamp,
        },
        {
            "term_id": "SKEL4067_3_GK",
            "term": "S_GK[g,Y] = -int sqrt|g| Gamma_ren + B_GK",
            "definition": "Gamma/Khat Hilbert owner with Khat=K_Gamma",
            "role": "turns q_loc/Khat into Hilbert-response/Ward residual rather than free closure",
            "owned_by_single_action": True,
            "timestamp_utc": current_timestamp,
        },
        {
            "term_id": "SKEL4067_4_auxiliary",
            "term": "S_aux^{no-flux}+S_top+S_vertical+S_reset",
            "definition": "scalar no-flux, topological/q-basic projector-domain, vertical Dq=0, and local reset memory blocks",
            "role": "side-channel silence through local <=2PN order",
            "owned_by_single_action": True,
            "timestamp_utc": current_timestamp,
        },
        {
            "term_id": "SKEL4067_5_readout",
            "term": "post-variation readout map",
            "definition": "PPN, R10, clocks, orbital, EM, and cosmology are readouts after action variation",
            "role": "firewall against fitting local tests into the action",
            "owned_by_single_action": True,
            "timestamp_utc": current_timestamp,
        },
    ]


def compatibility_proof_rows(current_timestamp: str) -> List[Dict[str, object]]:
    return [
        {
            "proof_id": "PROOF4067_0_direct_sum",
            "claim": "A finite direct sum of local differentiable action terms on one field space is one local action.",
            "argument": "All selected blocks in SKEL4067_0..4 are functions of fields in Q_parent^loc and fixed coupling/superselection data.",
            "result": "local single-action skeleton exists through <=2PN",
            "status": "CONSTRUCTIVE_LOCAL_PROOF",
            "timestamp_utc": current_timestamp,
        },
        {
            "proof_id": "PROOF4067_1_no_double_count",
            "claim": "Stationary bound EM, matter, binding, and GK stresses are counted once as Hilbert responses.",
            "argument": "S_matter, S_EM, S_binding, and S_GK are separate variational blocks; readout does not add a second source mass.",
            "result": "same Hilbert source and calibrated G_N readout remain compatible",
            "status": "CONDITIONAL_ON_SAME_SOURCE_BLOCKS",
            "timestamp_utc": current_timestamp,
        },
        {
            "proof_id": "PROOF4067_2_boundary_differentiability",
            "claim": "Boundary terms are differentiability/reference terms, not source-label forces.",
            "argument": "S_GHY and B_GK cancel derivative variation terms; source-blind fixed reference rules prevent readout drift.",
            "result": "boundary/reference terms can live in the same action without a local source leak",
            "status": "CONDITIONAL_ON_4038_4055_BOUNDARY_RULES",
            "timestamp_utc": current_timestamp,
        },
        {
            "proof_id": "PROOF4067_3_auxiliary_silence",
            "claim": "Auxiliary/private sectors can be included without changing local EH equations through <=2PN.",
            "argument": "no-flux scalar charge, q-basic projector/domain, local memory reset, and c_norm firewall give zero selected-branch first-order local sources.",
            "result": "side channels are action clauses, not hidden plateau assumptions, in the selected branch",
            "status": "CONDITIONAL_ON_4046_4047_4061_4062",
            "timestamp_utc": current_timestamp,
        },
        {
            "proof_id": "PROOF4067_4_diffeomorphism",
            "claim": "If the local packet is diffeomorphism invariant, the Hilbert stress satisfies the local Ward identity.",
            "argument": "Each block is scalar/covariant or topological/source-blind in the selected branch; explicit fixed coupling data are not varied as local source labels.",
            "result": "PPN zeta/conservation leakage is absent in the selected branch",
            "status": "LOCAL_WARD_CONDITIONAL",
            "timestamp_utc": current_timestamp,
        },
        {
            "proof_id": "PROOF4067_5_limit",
            "claim": "Under the skeleton, the local observed metric equation reduces to EH plus same Hilbert source through <=2PN.",
            "argument": "4060-4063 remove chain/CDB/c_norm/readout leaks, and 4063 supplies the weak-field EH readout.",
            "result": "conditional local Newton/PPN route follows from one local skeleton",
            "status": "LOCAL_LIMIT_CONDITIONALLY_CONSTRUCTED",
            "timestamp_utc": current_timestamp,
        },
    ]


def adoption_result_rows(current_timestamp: str) -> List[Dict[str, object]]:
    return [
        {
            "result_id": "RES4067_0_local_skeleton",
            "statement": "A single local <=2PN action skeleton for the selected branch is constructively available.",
            "scope": "compact stationary local branch only",
            "status": "CONSTRUCTED_CONDITIONALLY",
            "public_claim": False,
            "timestamp_utc": current_timestamp,
        },
        {
            "result_id": "RES4067_1_parent_descent",
            "statement": "The skeleton is not yet derived as the unique/local limit of the full global MTS parent action.",
            "scope": "whole MTS corpus/global parent theory",
            "status": "OPEN",
            "public_claim": False,
            "timestamp_utc": current_timestamp,
        },
        {
            "result_id": "RES4067_2_local_GR",
            "statement": "Local GR/Newton/PPN follows only conditionally from the skeleton plus prior silence gates.",
            "scope": "private selected-branch theorem candidate",
            "status": "PRIVATE_NONCLAIM",
            "public_claim": False,
            "timestamp_utc": current_timestamp,
        },
    ]


def failure_map_rows(current_timestamp: str) -> List[Dict[str, object]]:
    return [
        {
            "failure_id": "FAIL4067_0_global_parent",
            "open_gap": "global MTS parent action descent",
            "why_it_matters": "a local action skeleton could still be an engineered branch unless derived from the wider MTS parent structure",
            "repair_route": "derive field-space/descent map from core MTS variables to Q_parent^loc",
            "fallback_if_failed": "label local branch as closure/fallback scorer only",
            "timestamp_utc": current_timestamp,
        },
        {
            "failure_id": "FAIL4067_1_uniqueness",
            "open_gap": "uniqueness/minimality of EH local operator",
            "why_it_matters": "non-EH operators could re-enter PPN unless parent symmetries remove them",
            "repair_route": "prove EH-only local exterior or source-bound nonEH operator coefficients",
            "fallback_if_failed": "R_nonEH scorer rows",
            "timestamp_utc": current_timestamp,
        },
        {
            "failure_id": "FAIL4067_2_auxiliary_origin",
            "open_gap": "origin of auxiliary/reset/topological clauses",
            "why_it_matters": "silent clauses must be parent-owned, not manually attached to pass local tests",
            "repair_route": "derive q-basic/projector/reset/no-flux clauses from parent variational grammar",
            "fallback_if_failed": "side-channel scorer rows",
            "timestamp_utc": current_timestamp,
        },
        {
            "failure_id": "FAIL4067_3_global_branch_matching",
            "open_gap": "local branch versus FLRW/galaxy branch matching",
            "why_it_matters": "local no-flux/reset cannot erase cosmology or galaxy memory mechanisms",
            "repair_route": "derive branch selector/descent map with local compact and open/FLRW domains separated",
            "fallback_if_failed": "branch-selector closure",
            "timestamp_utc": current_timestamp,
        },
    ]


def static_rows(current_timestamp: str) -> Dict[str, List[Dict[str, object]]]:
    return {
        "claim_gate": [
            {
                "claim_id": "CLAIM4067_0",
                "claim": "single local <=2PN action skeleton exists for the selected branch",
                "allowed_private": True,
                "allowed_public": False,
                "reason": "constructive local skeleton only; full global parent descent remains open",
                "timestamp_utc": current_timestamp,
            },
            {
                "claim_id": "CLAIM4067_1",
                "claim": "MTS derives local GR/Newton/PPN as a public theorem",
                "allowed_private": False,
                "allowed_public": False,
                "reason": "global parent descent, uniqueness, and fallback verification remain open",
                "timestamp_utc": current_timestamp,
            },
            {
                "claim_id": "CLAIM4067_2",
                "claim": "the local action skeleton is the unique global MTS parent action limit",
                "allowed_private": False,
                "allowed_public": False,
                "reason": "4067 does not prove global parent descent or uniqueness",
                "timestamp_utc": current_timestamp,
            },
        ],
        "next_target": [
            {
                "row_id": "NEXT4067_0",
                "next_doc": "4068-Y5-R2FR-field-space-descent-from-MTS-parent-to-local-action-skeleton.md",
                "next_script": "scripts/Y5_R2FR_4068_field_space_descent_from_MTS_parent_to_local_action_skeleton.py",
                "reason": "the next derivation must show the local skeleton descends from the wider MTS parent field space rather than being an engineered local packet",
                "timestamp_utc": current_timestamp,
            }
        ],
        "status": [
            {
                "status_id": "STAT4067",
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
        {"check_id": "VAL4067_00_sources", "passed": source_ok, "detail": source_detail},
        {"check_id": "VAL4067_01_csv_parse", "passed": csv_ok, "detail": csv_detail},
        {"check_id": "VAL4067_02_no_public_claim", "passed": claims_ok, "detail": claims_detail},
        {
            "check_id": "VAL4067_03_local_skeleton",
            "passed": "single local <=2PN action skeleton" in joined and "CONSTRUCTED_CONDITIONALLY" in joined,
            "detail": "local action skeleton constructed conditionally",
        },
        {
            "check_id": "VAL4067_04_global_open",
            "passed": "global MTS parent action descent" in joined and "OPEN" in joined,
            "detail": "global parent descent remains explicitly open",
        },
        {
            "check_id": "VAL4067_05_next_target",
            "passed": "4068-Y5-R2FR-field-space-descent-from-MTS-parent-to-local-action-skeleton.md" in joined,
            "detail": "next target attacks parent field-space descent",
        },
        {"check_id": "VAL4067_06_script_compiles", "passed": compile_ok, "detail": compile_detail},
    ]


def doc_text(current_timestamp: str) -> str:
    return f"""# 4067 - Single Local Parent Action Adoption Proof or Failure Map

- Timestamp: `{current_timestamp}`
- Status: `private_nonclaim_checkpoint`
- Decision: `{DECISION}`
- Public local-GR claim: `false`

## What Was Constructed

4067 constructs a single local `<=2PN` action skeleton for the selected compact branch:

```text
S_loc^{{<=2PN}}
= S_EH[g_obs;kappa_*] + S_GHY[g_obs]
 + S_matter[psi,g_obs,theta]
 + S_EM[A,g_obs]
 + S_binding
 + S_GK[g,Y]
 + S_aux^{{no-flux}} + S_top + S_vertical + S_reset.
```

This is enough to say, privately and conditionally, that the selected local branch need not be treated as a pile of disconnected closure patches. It can be represented as one local action skeleton if the typed clauses are accepted.

## What Was Not Proven

4067 does **not** prove that this skeleton descends uniquely from the whole MTS parent action. That remains the next major derivation gate.

```text
local_single_action_skeleton = constructed_conditionally
global_parent_descent = open
public_local_GR_claim = false
fallback_required_if_parent_descent_fails = true
```

## Next

`4068` should attempt the parent field-space descent from core MTS variables to this local action skeleton.
"""


def main() -> None:
    current_timestamp = timestamp()
    SOURCE_DIR.mkdir(parents=True, exist_ok=True)

    sources = source_rows(current_timestamp)
    skeleton = single_action_skeleton_rows(current_timestamp)
    proof = compatibility_proof_rows(current_timestamp)
    adoption = adoption_result_rows(current_timestamp)
    failure = failure_map_rows(current_timestamp)
    static = static_rows(current_timestamp)

    DOC_PATH.write_text(doc_text(current_timestamp), encoding="utf-8")
    write_csv(OUTPUTS["source_register"], sources)
    write_csv(OUTPUTS["single_action_skeleton"], skeleton)
    write_csv(OUTPUTS["compatibility_proof"], proof)
    write_csv(OUTPUTS["adoption_result"], adoption)
    write_csv(OUTPUTS["failure_map"], failure)
    write_csv(OUTPUTS["claim_gate"], static["claim_gate"])
    write_csv(OUTPUTS["next_target"], static["next_target"])
    write_csv(OUTPUTS["status"], static["status"])

    generated_csvs = [
        OUTPUTS["source_register"],
        OUTPUTS["single_action_skeleton"],
        OUTPUTS["compatibility_proof"],
        OUTPUTS["adoption_result"],
        OUTPUTS["failure_map"],
        OUTPUTS["claim_gate"],
        OUTPUTS["next_target"],
        OUTPUTS["status"],
    ]
    row_groups = [
        sources,
        skeleton,
        proof,
        adoption,
        failure,
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

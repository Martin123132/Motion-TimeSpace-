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
DOC_PATH = ROOT / "4162-Y5-R2FR-private-packet-to-formal-spine-integration-or-epsilon-score-inputs.md"
FORMAL_DOC_PATH = FORMALIZATION / "180-PPC4161-private-local-packet-integration.md"

TIMESTAMP = datetime.now(timezone.utc).replace(microsecond=0).isoformat()
BRANCH_ID = "MTS_R2FR_Y5_PRIVATE_PACKET_SPINE_INTEGRATION_4162"
CHECKPOINT_ID = "4162"
DECISION = "PRIVATE_PACKET_INTEGRATED_AS_SCOPED_FORMAL_SPINE_BRANCH_NONCLAIM_SCORE_INPUTS_READY"


LOCAL_SOURCES: Dict[str, Tuple[Path, str, str]] = {
    "SRC4162_00_4161_doc": (
        ROOT / "4161-Y5-R2FR-local-parent-packet-adoption-or-first-epsilon-kernel-score.md",
        "epsilon_kernel_private_packet=0",
        "4161 private local packet branch and symbolic kernel zero.",
    ),
    "SRC4162_01_4161_next": (
        SOURCE_DIR / "P8_Y5_R2FR_4161_NEXT_TARGET.csv",
        "formal spine names the private local parent packet",
        "4161 machine-readable next target.",
    ),
    "SRC4162_02_4161_adoption": (
        SOURCE_DIR / "P8_Y5_R2FR_4161_PRIVATE_PACKET_ADOPTION.csv",
        "PRIVATE_BRANCH_ADOPTED_FOR_LOCAL_PROOF",
        "4161 private adoption rows.",
    ),
    "SRC4162_03_4161_clauses": (
        SOURCE_DIR / "P8_Y5_R2FR_4161_PACKET_CLAUSE_MAP.csv",
        "Gamma/Khat/q_loc Hilbert response",
        "4161 packet clause map.",
    ),
    "SRC4162_04_4161_collapse": (
        SOURCE_DIR / "P8_Y5_R2FR_4161_FIRST_ORDER_KERNEL_COLLAPSE.csv",
        "FIRST_ORDER_AHOM_ZERO_PRIVATE_BRANCH",
        "4161 first-order kernel collapse rows.",
    ),
    "SRC4162_05_4161_scorecard": (
        SOURCE_DIR / "P8_Y5_R2FR_4161_EPSILON_KERNEL_SCORECARD.csv",
        "SOURCE_BACKED_ROWS_REQUIRED",
        "4161 scorecard fallback inputs.",
    ),
    "SRC4162_06_4161_firewall": (
        SOURCE_DIR / "P8_Y5_R2FR_4161_CLAIM_FIREWALL.csv",
        "private local branch adoption is not a public claim",
        "4161 claim firewall.",
    ),
    "SRC4162_07_formal_179": (
        FORMALIZATION / "179-PPC4048-local-parent-packet-candidate.md",
        "PPC4048_formal_adoption_verified = false",
        "Existing formal local parent packet candidate.",
    ),
    "SRC4162_08_formal_07": (
        FORMALIZATION / "07-unification-spine.md",
        "Local GR Spine Update",
        "Existing formal unification spine.",
    ),
    "SRC4162_09_formal_19": (
        FORMALIZATION / "19-proof-obligations.md",
        "Post-Checkpoint PPC4048 Local Packet Candidate",
        "Existing proof-obligations spine section.",
    ),
    "SRC4162_10_formal_claims": (
        FORMALIZATION / "02-claims-register.csv",
        "PPC4048 is a conditional local parent-packet candidate",
        "Existing claims register local-gravity row.",
    ),
    "SRC4162_11_script": (
        SCRIPT_PATH,
        DECISION,
        "This generator records the 4162 formal spine bridge.",
    ),
}


def common() -> dict:
    return {
        "timestamp_utc": TIMESTAMP,
        "branch_id": BRANCH_ID,
        "checkpoint_id": CHECKPOINT_ID,
    }


def write_csv(path: Path, rows: List[dict]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fieldnames: List[str] = []
    for row in rows:
        for key in row:
            if key not in fieldnames:
                fieldnames.append(key)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow(row)


def parse_csv(path: Path) -> List[dict]:
    with path.open("r", newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def is_under(path: Path, root: Path) -> bool:
    try:
        path.resolve().relative_to(root.resolve())
        return True
    except ValueError:
        return False


def output_paths() -> Dict[str, Path]:
    return {
        "P8_Y5_R2FR_4162_SOURCE_REGISTER": SOURCE_DIR / "P8_Y5_R2FR_4162_SOURCE_REGISTER.csv",
        "P8_Y5_R2FR_4162_SPINE_INTEGRATION_MAP": SOURCE_DIR / "P8_Y5_R2FR_4162_SPINE_INTEGRATION_MAP.csv",
        "P8_Y5_R2FR_4162_FORMAL_BRANCH_CLAIMS": SOURCE_DIR / "P8_Y5_R2FR_4162_FORMAL_BRANCH_CLAIMS.csv",
        "P8_Y5_R2FR_4162_EPSILON_SCORE_INPUT_CONTRACT": SOURCE_DIR / "P8_Y5_R2FR_4162_EPSILON_SCORE_INPUT_CONTRACT.csv",
        "P8_Y5_R2FR_4162_CLAIM_FIREWALL": SOURCE_DIR / "P8_Y5_R2FR_4162_CLAIM_FIREWALL.csv",
        "P8_Y5_R2FR_4162_FORMAL_DOC_AUDIT": SOURCE_DIR / "P8_Y5_R2FR_4162_FORMAL_DOC_AUDIT.csv",
        "P8_Y5_R2FR_4162_STATUS": SOURCE_DIR / "P8_Y5_R2FR_4162_STATUS.csv",
        "P8_Y5_R2FR_4162_NEXT_TARGET": SOURCE_DIR / "P8_Y5_R2FR_4162_NEXT_TARGET.csv",
    }


def source_rows() -> List[dict]:
    rows: List[dict] = []
    for source_id, (path, needle, role) in LOCAL_SOURCES.items():
        exists = path.exists()
        text = read_text(path) if exists and path.is_file() else ""
        rows.append(
            {
                **common(),
                "source_id": source_id,
                "path": str(path),
                "needle": needle,
                "role": role,
                "exists": str(exists),
                "needle_found": str(bool(exists and needle in text)),
                "claim_allowed": "False",
                "valid_for_claim": "False",
            }
        )
    return rows


def integration_rows() -> List[dict]:
    return [
        {
            **common(),
            "map_id": "SP4162_0_formal_doc",
            "artifact": str(FORMAL_DOC_PATH),
            "integration_action": "create formal workbench bridge document",
            "spine_role": "names the 4161 private local packet as the current scoped first-order local Newton/kernel branch",
            "claim_status": "nonclaim_private_branch",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            **common(),
            "map_id": "SP4162_1_local_spine",
            "artifact": "formalization-workbench/179-PPC4048-local-parent-packet-candidate.md",
            "integration_action": "superseded-by-bridge reference, not overwritten",
            "spine_role": "4162 preserves the older PPC4048 caveats and adds 4157-4161 first-order kernel result as a scoped branch",
            "claim_status": "older_caveats_retained",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            **common(),
            "map_id": "SP4162_2_unification_spine",
            "artifact": "formalization-workbench/07-unification-spine.md",
            "integration_action": "no direct edit in this checkpoint",
            "spine_role": "4162 bridge is the source-ready patch target for a later spine merge",
            "claim_status": "merge_pending",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            **common(),
            "map_id": "SP4162_3_claims_register",
            "artifact": "formalization-workbench/02-claims-register.csv",
            "integration_action": "no direct edit in this checkpoint",
            "spine_role": "claims register should later add a nonclaim local-gravity row for PPC4161 if public-facing docs are refreshed",
            "claim_status": "claim_register_update_pending",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
    ]


def branch_claim_rows() -> List[dict]:
    return [
        {
            **common(),
            "claim_id": "BC4162_0_scope",
            "statement": "PPC4161 is a private compact isolated local <=2PN parent branch.",
            "proof_effect": "may be used internally to derive first-order Newton source normalization in the same-source local branch",
            "not_claim": "not a public local-GR theorem and not global MTS adoption",
            "status": "SCOPED_PRIVATE_BRANCH",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            **common(),
            "claim_id": "BC4162_1_kernel",
            "statement": "Under PPC4161, same-source compact local first-order branch gives epsilon_kernel_private_packet=0.",
            "proof_effect": "a_hom collapses by 4158-4161 when the private packet is accepted",
            "not_claim": "not an empirical score and not a numerical bound",
            "status": "SYMBOLIC_PRIVATE_BRANCH_ZERO",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            **common(),
            "claim_id": "BC4162_2_Newton",
            "statement": "Under PPC4161 and fixed G_ref, mu_obs=G_ref M_H_ref up to higher-order/PPN/readout residuals.",
            "proof_effect": "conditional first-order Newton source normalization route",
            "not_claim": "does not predict numerical G and does not finish full PPN/local GR",
            "status": "CONDITIONAL_PRIVATE_NEWTON_BRANCH",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            **common(),
            "claim_id": "BC4162_3_global",
            "statement": "PPC4161 does not erase cosmology, galaxy, open-memory or radiative-EM sectors.",
            "proof_effect": "local collar assumptions are quarantined from other pillars",
            "not_claim": "not a global-memory or all-sector closure",
            "status": "GLOBAL_SCOPE_GUARD",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
    ]


def score_input_rows() -> List[dict]:
    return [
        {
            **common(),
            "input_id": "EI4162_0_Pi_operator",
            "component": "epsilon_Pi_operator",
            "needed_if": "EH/operator clause rejected or non-EH local operator retained",
            "source_required": "operator variation bound or formal zero certificate",
            "current_status": "ZERO_UNDER_PRIVATE_PACKET_ELSE_SOURCE_REQUIRED",
            "score_ready": "False",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            **common(),
            "input_id": "EI4162_1_boundary_domain",
            "component": "epsilon_Pi_boundary + epsilon_Pi_domain + epsilon_boundary_inner + epsilon_domain_inner",
            "needed_if": "boundary/reference or domain/projector clauses rejected",
            "source_required": "boundary charge, reference drift, support/projector motion and wall flux bounds",
            "current_status": "ZERO_UNDER_PRIVATE_PACKET_ELSE_SOURCE_REQUIRED",
            "score_ready": "False",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            **common(),
            "input_id": "EI4162_2_tau_frame_readout",
            "component": "epsilon_Pi_tau + epsilon_Pi_frame_units + epsilon_Pi_readout + epsilon_surface_mismatch",
            "needed_if": "same tau/frame/units/readout firewall rejected",
            "source_required": "same-generator certificate or mismatch bound",
            "current_status": "ZERO_UNDER_PRIVATE_PACKET_ELSE_SOURCE_REQUIRED",
            "score_ready": "False",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            **common(),
            "input_id": "EI4162_3_EM_symp_incoming",
            "component": "epsilon_EM_extra_inner + epsilon_symp_inner + epsilon_incoming_mass",
            "needed_if": "radiative/nonminimal EM, H_tau curl/corner, or incoming free monopole branch retained",
            "source_required": "Poynting/radiative bound, H_tau integrability bound, no-incoming certificate or incoming-mass upper bound",
            "current_status": "ZERO_UNDER_PRIVATE_PACKET_ELSE_SOURCE_REQUIRED",
            "score_ready": "False",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            **common(),
            "input_id": "EI4162_4_total",
            "component": "epsilon_kernel_score",
            "needed_if": "any private packet clause rejected",
            "source_required": "all active component bounds numeric/source-backed",
            "current_status": "NOT_SCORE_READY",
            "score_ready": "False",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
    ]


def firewall_rows() -> List[dict]:
    return [
        {
            **common(),
            "firewall_id": "FW4162_0_nonclaim",
            "rule": "formal bridge is nonclaim",
            "meaning": "new 180 document records a private branch, not a publishable local-GR victory",
            "status": "ACTIVE",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            **common(),
            "firewall_id": "FW4162_1_no_spine_overwrite",
            "rule": "older spine caveats remain active",
            "meaning": "4162 does not delete or silently supersede 07/19/179 caveats",
            "status": "ACTIVE",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            **common(),
            "firewall_id": "FW4162_2_empirical",
            "rule": "empirical readouts still required",
            "meaning": "PPN, clocks, orbital, R10, EM and cosmology tests remain downstream requirements",
            "status": "ACTIVE",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
    ]


def formal_audit_rows() -> List[dict]:
    return [
        {
            **common(),
            "audit_id": "FA4162_0_formal_doc_created",
            "path": str(FORMAL_DOC_PATH),
            "expected": "exists and contains PPC4161_PRIVATE_LOCAL_PACKET_INTEGRATION",
            "status": "PENDING_UNTIL_WRITE",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            **common(),
            "audit_id": "FA4162_1_main_spine_not_overwritten",
            "path": str(FORMALIZATION / "07-unification-spine.md"),
            "expected": "no direct write in this checkpoint",
            "status": "REFERENCE_ONLY",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            **common(),
            "audit_id": "FA4162_2_claims_register_not_overwritten",
            "path": str(FORMALIZATION / "02-claims-register.csv"),
            "expected": "no direct write in this checkpoint",
            "status": "REFERENCE_ONLY",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
    ]


def status_rows() -> List[dict]:
    return [
        {
            **common(),
            "result": DECISION,
            "formal_spine_bridge_created": "True",
            "formal_doc_path": str(FORMAL_DOC_PATH),
            "private_packet_named_in_formal_workbench": "True",
            "first_order_kernel_zero_recorded_private": "True",
            "public_local_gr_claimed": "False",
            "global_MTS_claimed": "False",
            "numeric_epsilon_kernel_score_ready": "False",
            "older_spine_caveats_preserved": "True",
            "formalization_modified_by_4162": "True",
            "next_target": "4163-Y5-R2FR-formal-spine-claim-register-sync-or-local-PPN-readout-gate.md",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
    ]


def next_rows() -> List[dict]:
    return [
        {
            **common(),
            "next_id": "NEXT4162_0",
            "target_doc": "4163-Y5-R2FR-formal-spine-claim-register-sync-or-local-PPN-readout-gate.md",
            "target_script": "scripts/Y5_R2FR_4163_formal_spine_claim_register_sync_or_local_PPN_readout_gate.py",
            "objective": "either sync the formal claims register/main spine to point at 180 as a nonclaim local branch, or build the first local PPN/readout gate for the PPC4161 private branch",
            "success_gate": "claims register/main spine include PPC4161 with public_claim=false, or PPN/readout residual gates are prepared for gamma/beta/alpha/xi/zeta/Gdot",
            "reason": "4162 creates the formal workbench bridge; next work is either index/claim-register hygiene or downstream readout verification.",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
    ]


def write_formal_doc() -> None:
    FORMAL_DOC_PATH.parent.mkdir(parents=True, exist_ok=True)
    text = f"""# 180 - PPC4161 Private Local Packet Integration

Marker: `PPC4161_PRIVATE_LOCAL_PACKET_INTEGRATION`  
Timestamp UTC: `{TIMESTAMP}`  
Status: `private_spine_branch_nonclaim`  
Claim status: `not_public_local_GR_claim`

## Purpose

This document integrates post-checkpoint `4161` into the formal workbench as a scoped local branch.

It does **not** overwrite the older caveats in `07-unification-spine.md`, `19-proof-obligations.md`, or `179-PPC4048-local-parent-packet-candidate.md`.

## Integrated Branch

For the compact isolated local `<=2PN` same-source branch, adopt privately:

`S_loc^{{<=2PN}}=S_EH[g_obs;kappa_*]+S_matter[psi,g_obs,theta]+S_EM[A,g_obs]+S_binding+S_GK+B_proper+S_top+S_vertical+S_reset`.

This is the `PPC4161` branch.

## Result Imported From 4161

Under `PPC4161`:

`delta Pi_M^C=0`,

`Phi_hidden_inner=0`,

same `S/tau/frame/units` are fixed, and the outer reference is fixed.

Therefore, for the same-source compact local first-order branch:

`delta J_H_total=0 and PPC4161 => a_hom=0`.

Equivalently:

`epsilon_kernel_private_packet=0`.

## Non-Claims

- This is not a public local-GR theorem.
- This is not global MTS corpus adoption.
- This does not predict the numerical value of `G`.
- This does not close full PPN beyond the first-order kernel/source-normalization branch.
- This does not erase cosmology, galaxy, open-memory, or radiative-EM sectors.

## Fallback If Any Clause Is Rejected

Restore:

`epsilon_kernel <= epsilon_Pi_inner + epsilon_hidden_inner + epsilon_surface_mismatch`.

Executable scoring then requires source-backed rows for:

- `epsilon_Pi_operator`;
- `epsilon_Pi_boundary`;
- `epsilon_Pi_domain`;
- `epsilon_Pi_tau`;
- `epsilon_Pi_frame_units`;
- `epsilon_Pi_readout`;
- `epsilon_boundary_inner`;
- `epsilon_domain_inner`;
- `epsilon_symp_inner`;
- `epsilon_EM_extra_inner`;
- `epsilon_incoming_mass`.

## Downstream Gates

Before any public local-GR claim, the branch still needs:

1. claims-register/main-spine sync with `public_claim=false`;
2. local PPN readout gate for `gamma`, `beta`, `alpha_i`, `xi`, `zeta_i`, and `Gdot/G`;
3. clock/orbital/R10/EM checks or explicit nonclaim labels;
4. proof that the local collar assumptions do not leak into FLRW/galaxy/open-memory sectors.

## Source Pointers

- `post-checkpoint-work/4161-Y5-R2FR-local-parent-packet-adoption-or-first-epsilon-kernel-score.md`
- `post-checkpoint-work/source-intake/mts_residuals/P8_Y5_R2FR_4161_FIRST_ORDER_KERNEL_COLLAPSE.csv`
- `post-checkpoint-work/source-intake/mts_residuals/P8_Y5_R2FR_4161_CLAIM_FIREWALL.csv`
- `post-checkpoint-work/4162-Y5-R2FR-private-packet-to-formal-spine-integration-or-epsilon-score-inputs.md`
"""
    FORMAL_DOC_PATH.write_text(text, encoding="utf-8")


def write_doc(outputs: Dict[str, Path]) -> None:
    text = f"""# 4162 - Private Packet To Formal Spine Integration Or Epsilon Score Inputs

Timestamp UTC: `{TIMESTAMP}`  
Branch: `{BRANCH_ID}`  
Decision: `{DECISION}`

## Purpose
4161 adopted `PPC4161` privately and gave:

`epsilon_kernel_private_packet=0`

for the compact isolated local same-source first-order branch.

4162 integrates that result into the formal workbench without converting it into a public local-GR claim.

## Formal Workbench Bridge
Created:

`{FORMAL_DOC_PATH}`.

The bridge names `PPC4161` as a scoped private local parent packet and records:

- the adopted local `<=2PN` action packet;
- the first-order `a_hom=0` result;
- the nonclaim firewall;
- the fallback `epsilon_kernel` score inputs.

## Formal Spine Status
This is a formal-workbench integration artifact, not a wholesale rewrite of the main spine.

Older caveats remain active:

- `07-unification-spine.md` is not overwritten;
- `19-proof-obligations.md` is not overwritten;
- `179-PPC4048-local-parent-packet-candidate.md` is not overwritten;
- `02-claims-register.csv` is not overwritten.

## Score Input Contract
If any `PPC4161` clause is rejected, restore:

`epsilon_kernel <= epsilon_Pi_inner + epsilon_hidden_inner + epsilon_surface_mismatch`.

The first executable score needs source-backed rows for operator, boundary, domain, tau/frame/units/readout, EM, symplectic/corner, and incoming-mass components.

## Verdict
The private local packet is now visible in the formal workbench as a scoped branch. Public local-GR/global-MTS claims remain blocked.

## Outputs
- `{outputs["P8_Y5_R2FR_4162_SOURCE_REGISTER"]}`
- `{outputs["P8_Y5_R2FR_4162_SPINE_INTEGRATION_MAP"]}`
- `{outputs["P8_Y5_R2FR_4162_FORMAL_BRANCH_CLAIMS"]}`
- `{outputs["P8_Y5_R2FR_4162_EPSILON_SCORE_INPUT_CONTRACT"]}`
- `{outputs["P8_Y5_R2FR_4162_CLAIM_FIREWALL"]}`
- `{outputs["P8_Y5_R2FR_4162_FORMAL_DOC_AUDIT"]}`
- `{outputs["P8_Y5_R2FR_4162_STATUS"]}`
- `{outputs["P8_Y5_R2FR_4162_NEXT_TARGET"]}`

## Next Target
- `4163-Y5-R2FR-formal-spine-claim-register-sync-or-local-PPN-readout-gate.md`
- Either sync the claims register/main spine to point at `180` with `public_claim=false`, or build the first local PPN/readout gate for `PPC4161`.
"""
    DOC_PATH.write_text(text, encoding="utf-8")


def write_outputs() -> Dict[str, Path]:
    outputs = output_paths()
    write_formal_doc()
    write_csv(outputs["P8_Y5_R2FR_4162_SOURCE_REGISTER"], source_rows())
    write_csv(outputs["P8_Y5_R2FR_4162_SPINE_INTEGRATION_MAP"], integration_rows())
    write_csv(outputs["P8_Y5_R2FR_4162_FORMAL_BRANCH_CLAIMS"], branch_claim_rows())
    write_csv(outputs["P8_Y5_R2FR_4162_EPSILON_SCORE_INPUT_CONTRACT"], score_input_rows())
    write_csv(outputs["P8_Y5_R2FR_4162_CLAIM_FIREWALL"], firewall_rows())
    write_csv(outputs["P8_Y5_R2FR_4162_FORMAL_DOC_AUDIT"], formal_audit_rows())
    write_csv(outputs["P8_Y5_R2FR_4162_STATUS"], status_rows())
    write_csv(outputs["P8_Y5_R2FR_4162_NEXT_TARGET"], next_rows())
    write_doc(outputs)
    return outputs


def validate(outputs: Dict[str, Path]) -> List[dict]:
    checks: List[dict] = []

    def add(check_id: str, requirement: str, passed: bool, detail: str) -> None:
        checks.append(
            {
                **common(),
                "check_id": check_id,
                "requirement": requirement,
                "passed": str(bool(passed)),
                "detail": detail,
                "claim_allowed": "False",
                "valid_for_claim": "False",
            }
        )

    sources = source_rows()
    add(
        "VAL4162_0_sources",
        "all cited source paths exist and contain required needles",
        all(row["exists"] == "True" and row["needle_found"] == "True" for row in sources),
        "; ".join(f"{row['source_id']} exists={row['exists']} needle={row['needle_found']}" for row in sources),
    )

    csv_ok = True
    csv_detail: List[str] = []
    for name, path in outputs.items():
        try:
            rows = parse_csv(path)
            csv_detail.append(f"{name}:{len(rows)}")
            csv_ok = csv_ok and bool(rows)
        except Exception as exc:
            csv_ok = False
            csv_detail.append(f"{name}:ERR {exc!r}")
    add("VAL4162_1_csv_parse", "all generated CSV outputs parse and are nonempty", csv_ok, ", ".join(csv_detail))

    formal_text = read_text(FORMAL_DOC_PATH) if FORMAL_DOC_PATH.exists() else ""
    formal_tokens = [
        "PPC4161_PRIVATE_LOCAL_PACKET_INTEGRATION",
        "epsilon_kernel_private_packet=0",
        "This is not a public local-GR theorem.",
        "epsilon_kernel <= epsilon_Pi_inner + epsilon_hidden_inner + epsilon_surface_mismatch",
    ]
    add("VAL4162_2_formal_doc", "formal workbench bridge exists and contains marker, result, firewall and fallback", FORMAL_DOC_PATH.exists() and all(token in formal_text for token in formal_tokens), str(FORMAL_DOC_PATH))

    doc_text = read_text(DOC_PATH) if DOC_PATH.exists() else ""
    doc_tokens = [
        DECISION,
        str(FORMAL_DOC_PATH),
        "epsilon_kernel_private_packet=0",
        "07-unification-spine.md` is not overwritten",
        "4163-Y5-R2FR-formal-spine-claim-register-sync-or-local-PPN-readout-gate.md",
    ]
    add("VAL4162_3_doc_tokens", "checkpoint doc records formal bridge, non-overwrite policy and next target", all(token in doc_text for token in doc_tokens), "tokens checked")

    map_text = "\n".join(",".join(row.values()) for row in parse_csv(outputs["P8_Y5_R2FR_4162_SPINE_INTEGRATION_MAP"]))
    map_tokens = ["create formal workbench bridge document", "older_caveats_retained", "merge_pending", "claim_register_update_pending"]
    add("VAL4162_4_map", "integration map records bridge and pending main-spine/claims sync", all(token in map_text for token in map_tokens), "map tokens checked")

    branch_text = "\n".join(",".join(row.values()) for row in parse_csv(outputs["P8_Y5_R2FR_4162_FORMAL_BRANCH_CLAIMS"]))
    branch_tokens = ["SCOPED_PRIVATE_BRANCH", "SYMBOLIC_PRIVATE_BRANCH_ZERO", "CONDITIONAL_PRIVATE_NEWTON_BRANCH", "GLOBAL_SCOPE_GUARD"]
    add("VAL4162_5_branch_claims", "branch rows state private scope, symbolic zero, conditional Newton and global guard", all(token in branch_text for token in branch_tokens), "branch tokens checked")

    score_text = "\n".join(",".join(row.values()) for row in parse_csv(outputs["P8_Y5_R2FR_4162_EPSILON_SCORE_INPUT_CONTRACT"]))
    score_tokens = ["epsilon_Pi_operator", "epsilon_Pi_boundary", "epsilon_Pi_tau", "epsilon_EM_extra_inner", "epsilon_kernel_score", "NOT_SCORE_READY"]
    add("VAL4162_6_score_inputs", "score input rows name required epsilon components and remain not score-ready", all(token in score_text for token in score_tokens), "score tokens checked")

    firewall_text = "\n".join(",".join(row.values()) for row in parse_csv(outputs["P8_Y5_R2FR_4162_CLAIM_FIREWALL"]))
    firewall_tokens = ["formal bridge is nonclaim", "older spine caveats remain active", "empirical readouts still required"]
    add("VAL4162_7_firewall", "firewall rows prevent public/local/global overclaim", all(token in firewall_text for token in firewall_tokens), "firewall tokens checked")

    status = parse_csv(outputs["P8_Y5_R2FR_4162_STATUS"])
    status_ok = (
        len(status) == 1
        and status[0].get("result") == DECISION
        and status[0].get("formal_spine_bridge_created") == "True"
        and status[0].get("private_packet_named_in_formal_workbench") == "True"
        and status[0].get("first_order_kernel_zero_recorded_private") == "True"
        and status[0].get("public_local_gr_claimed") == "False"
        and status[0].get("global_MTS_claimed") == "False"
        and status[0].get("numeric_epsilon_kernel_score_ready") == "False"
        and status[0].get("formalization_modified_by_4162") == "True"
    )
    add("VAL4162_8_status", "status records bridge creation, private zero and no public/global claim", status_ok, str(status))

    next_target = parse_csv(outputs["P8_Y5_R2FR_4162_NEXT_TARGET"])
    next_ok = len(next_target) == 1 and next_target[0].get("target_doc") == "4163-Y5-R2FR-formal-spine-claim-register-sync-or-local-PPN-readout-gate.md"
    add("VAL4162_9_next", "next target is claim-register sync or local PPN readout gate", next_ok, str(next_target))

    all_rows: List[dict] = []
    for path in outputs.values():
        all_rows.extend(parse_csv(path))
    no_claim = all(row.get("claim_allowed") in ("False", "") and row.get("valid_for_claim") in ("False", "") for row in all_rows)
    no_score = all(row.get("score_ready", "False") in ("False", "") for row in all_rows)
    add("VAL4162_10_no_claim", "all generated rows remain nonclaim and no executable score-ready row", no_claim and no_score, f"row_count={len(all_rows)}")

    output_paths_all = list(outputs.values()) + [DOC_PATH, FORMAL_DOC_PATH]
    in_scope = all(is_under(path, ROOT) or is_under(path, FORMALIZATION) for path in output_paths_all)
    formal_outputs = [path for path in output_paths_all if is_under(path, FORMALIZATION)]
    formal_ok = formal_outputs == [FORMAL_DOC_PATH]
    add("VAL4162_11_scope", "outputs stay in post-checkpoint-work plus exactly one new formal workbench bridge", in_scope and formal_ok, f"formal_outputs={[str(p) for p in formal_outputs]}")

    compile_ok = True
    compile_detail = "py_compile ok"
    try:
        py_compile.compile(str(SCRIPT_PATH), doraise=True)
    except Exception as exc:
        compile_ok = False
        compile_detail = repr(exc)
    add("VAL4162_12_compile", "generator script compiles", compile_ok, compile_detail)
    return checks


def main() -> None:
    outputs = write_outputs()
    validation_rows = validate(outputs)
    validation_path = SOURCE_DIR / "P8_Y5_BRR545_4162_VALIDATION.csv"
    write_csv(validation_path, validation_rows)
    pycache = SCRIPT_PATH.parent / "__pycache__"
    if pycache.exists():
        shutil.rmtree(pycache)

    failed = [row for row in validation_rows if row["passed"] != "True"]
    print(f"wrote: {DOC_PATH}")
    print(f"wrote: {FORMAL_DOC_PATH}")
    for path in outputs.values():
        print(f"wrote: {path}")
    print(f"validation: {validation_path}")
    if failed:
        print("failed checks:")
        for row in failed:
            print(f"- {row['check_id']}: {row['detail']}")
        raise SystemExit(1)
    print("all validation checks passed")


if __name__ == "__main__":
    main()

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
DOC_PATH = ROOT / "4163-Y5-R2FR-formal-spine-claim-register-sync-or-local-PPN-readout-gate.md"

CLAIMS_PATH = FORMALIZATION / "02-claims-register.csv"
SPINE_PATH = FORMALIZATION / "07-unification-spine.md"
FORMAL_180_PATH = FORMALIZATION / "180-PPC4161-private-local-packet-integration.md"

TIMESTAMP = datetime.now(timezone.utc).replace(microsecond=0).isoformat()
BRANCH_ID = "MTS_R2FR_Y5_FORMAL_SPINE_CLAIM_SYNC_4163"
CHECKPOINT_ID = "4163"
DECISION = "FORMAL_SPINE_AND_CLAIMS_REGISTER_SYNCED_TO_PPC4161_NONCLAIM_LOCAL_BRANCH"
SPINE_MARKER = "PPC4161_FORMAL_SYNC_4163"
CLAIM_ID = "L-005"


LOCAL_SOURCES: Dict[str, Tuple[Path, str, str]] = {
    "SRC4163_00_4162_doc": (
        ROOT / "4162-Y5-R2FR-private-packet-to-formal-spine-integration-or-epsilon-score-inputs.md",
        "sync the claims register/main spine",
        "4162 handoff to formal spine/claims sync.",
    ),
    "SRC4163_01_4162_next": (
        SOURCE_DIR / "P8_Y5_R2FR_4162_NEXT_TARGET.csv",
        "claims register/main spine include PPC4161",
        "4162 machine-readable next target.",
    ),
    "SRC4163_02_formal_180": (
        FORMAL_180_PATH,
        "PPC4161_PRIVATE_LOCAL_PACKET_INTEGRATION",
        "Formal bridge created by 4162.",
    ),
    "SRC4163_03_claims": (
        CLAIMS_PATH,
        CLAIM_ID,
        "Claims register synced by 4163.",
    ),
    "SRC4163_04_spine": (
        SPINE_PATH,
        SPINE_MARKER,
        "Main spine section synced by 4163.",
    ),
    "SRC4163_05_4161_firewall": (
        SOURCE_DIR / "P8_Y5_R2FR_4161_CLAIM_FIREWALL.csv",
        "private local branch adoption is not a public claim",
        "4161 claim firewall source.",
    ),
    "SRC4163_06_4162_score_inputs": (
        SOURCE_DIR / "P8_Y5_R2FR_4162_EPSILON_SCORE_INPUT_CONTRACT.csv",
        "epsilon_kernel_score",
        "4162 score input contract.",
    ),
    "SRC4163_07_script": (
        SCRIPT_PATH,
        DECISION,
        "This generator records 4163 formal sync.",
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
        "P8_Y5_R2FR_4163_SOURCE_REGISTER": SOURCE_DIR / "P8_Y5_R2FR_4163_SOURCE_REGISTER.csv",
        "P8_Y5_R2FR_4163_FORMAL_SYNC_MAP": SOURCE_DIR / "P8_Y5_R2FR_4163_FORMAL_SYNC_MAP.csv",
        "P8_Y5_R2FR_4163_CLAIMS_REGISTER_AUDIT": SOURCE_DIR / "P8_Y5_R2FR_4163_CLAIMS_REGISTER_AUDIT.csv",
        "P8_Y5_R2FR_4163_SPINE_SECTION_AUDIT": SOURCE_DIR / "P8_Y5_R2FR_4163_SPINE_SECTION_AUDIT.csv",
        "P8_Y5_R2FR_4163_LOCAL_PPN_READOUT_HANDOFF": SOURCE_DIR / "P8_Y5_R2FR_4163_LOCAL_PPN_READOUT_HANDOFF.csv",
        "P8_Y5_R2FR_4163_CLAIM_FIREWALL": SOURCE_DIR / "P8_Y5_R2FR_4163_CLAIM_FIREWALL.csv",
        "P8_Y5_R2FR_4163_STATUS": SOURCE_DIR / "P8_Y5_R2FR_4163_STATUS.csv",
        "P8_Y5_R2FR_4163_NEXT_TARGET": SOURCE_DIR / "P8_Y5_R2FR_4163_NEXT_TARGET.csv",
    }


def ensure_claim_row() -> str:
    rows = parse_csv(CLAIMS_PATH)
    if not rows:
        raise RuntimeError("claims register is empty")
    fieldnames = list(rows[0].keys())
    existing = [row for row in rows if row.get("claim_id") == CLAIM_ID]
    if existing:
        return "already_present"
    new_row = {
        "claim_id": CLAIM_ID,
        "domain": "local_gravity",
        "claim": "PPC4161 is a scoped private local parent-packet branch for first-order Newton source normalization",
        "current_evidence": "formalization-workbench/180-PPC4161-private-local-packet-integration.md records epsilon_kernel_private_packet=0 inside a compact same-source local branch; public_claim=false",
        "status": "private_nonclaim_public_claim_false",
        "next_test": "Build PPC4161 local PPN/readout gate for gamma, beta, alpha_i, xi, zeta_i, and Gdot/G; retain fallback epsilon_kernel score rows if any packet clause is rejected",
        "key_risk": "Private branch adoption may not survive full corpus adoption, PPN readout, or empirical local tests",
    }
    rows.append({key: new_row.get(key, "") for key in fieldnames})
    with CLAIMS_PATH.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow(row)
    return "added"


def ensure_spine_section() -> str:
    text = read_text(SPINE_PATH)
    if SPINE_MARKER in text:
        repaired = text.replace("Claim register row: `L-004`", f"Claim register row: `{CLAIM_ID}`")
        if repaired != text:
            SPINE_PATH.write_text(repaired, encoding="utf-8")
            return "repaired_claim_id"
        return "already_present"
    section = f"""

## 10. Local GR Spine Update - PPC4161 Private Packet Sync

Marker: `{SPINE_MARKER}`  
Source bridge: `180-PPC4161-private-local-packet-integration.md`  
Claim register row: `{CLAIM_ID}`

Post-checkpoints `4157-4162` sharpen the local Newton/source-normalization route into a scoped private local branch:

```text
PPC4161_private_local_packet = true
public_claim = false
global_MTS_claim = false
epsilon_kernel_private_packet = 0
```

The branch says:

```text
delta J_H_total = 0 and PPC4161 => a_hom = 0
```

for the compact isolated same-source first-order local branch.

This is a real spine improvement over the older closure-only local-PPN state: the first-order homogeneous Newton mass kernel has a private parent-packet route.

It is still not a public local-GR theorem because:

- PPC4161 is private/scoped, not global corpus adoption;
- full PPN readout is still required for `gamma`, `beta`, `alpha_i`, `xi`, `zeta_i`, and `Gdot/G`;
- empirical local tests remain downstream;
- rejected packet clauses reactivate `epsilon_kernel <= epsilon_Pi_inner + epsilon_hidden_inner + epsilon_surface_mismatch`;
- cosmology, galaxy, open-memory, and radiative-EM sectors are not erased by the compact local collar assumptions.

The next local-GR spine step is:

```text
4164-Y5-R2FR-PPC4161-local-PPN-readout-gate.md
```
"""
    SPINE_PATH.write_text(text.rstrip() + section + "\n", encoding="utf-8")
    return "added"


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


def sync_map_rows(claim_action: str, spine_action: str) -> List[dict]:
    return [
        {
            **common(),
            "sync_id": "SYNC4163_0_claims",
            "artifact": str(CLAIMS_PATH),
            "action": claim_action,
            "marker": CLAIM_ID,
            "effect": "claims register now points at PPC4161 with private_nonclaim_public_claim_false",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            **common(),
            "sync_id": "SYNC4163_1_spine",
            "artifact": str(SPINE_PATH),
            "action": spine_action,
            "marker": SPINE_MARKER,
            "effect": f"main unification spine now points at formal 180 bridge and {CLAIM_ID}",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
    ]


def claims_audit_rows() -> List[dict]:
    rows = parse_csv(CLAIMS_PATH)
    matches = [row for row in rows if row.get("claim_id") == CLAIM_ID]
    row = matches[0] if matches else {}
    return [
        {
            **common(),
            "audit_id": f"CLAIM4163_0_{CLAIM_ID}_present",
            "claim_id": CLAIM_ID,
            "present": str(bool(matches)),
            "status": row.get("status", ""),
            "claim": row.get("claim", ""),
            "current_evidence": row.get("current_evidence", ""),
            "public_claim_false_encoded": str("public_claim_false" in row.get("status", "") and "public_claim=false" in row.get("current_evidence", "")),
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
    ]


def spine_audit_rows() -> List[dict]:
    text = read_text(SPINE_PATH)
    return [
        {
            **common(),
            "audit_id": "SPINE4163_0_marker",
            "path": str(SPINE_PATH),
            "marker": SPINE_MARKER,
            "marker_present": str(SPINE_MARKER in text),
            "mentions_180": str("180-PPC4161-private-local-packet-integration.md" in text),
            "public_claim_false": str("public_claim = false" in text),
            "fallback_present": str("epsilon_kernel <= epsilon_Pi_inner + epsilon_hidden_inner + epsilon_surface_mismatch" in text),
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
    ]


def ppn_handoff_rows() -> List[dict]:
    return [
        {
            **common(),
            "readout_id": "PPN4163_0_gamma",
            "parameter": "gamma",
            "private_packet_expectation": "gamma=1 under PPC4161 if full <=2PN EH/same-source readout holds",
            "needed_next": "derive/read out gamma residual from PPC4161 metric equations, not just inherited assertion",
            "score_ready": "False",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            **common(),
            "readout_id": "PPN4163_1_beta",
            "parameter": "beta",
            "private_packet_expectation": "beta=1 under PPC4161 if second-order EH/source normalization and q_loc silence hold",
            "needed_next": "derive/read out beta residual and q_loc/GK contribution through O(U^2)",
            "score_ready": "False",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            **common(),
            "readout_id": "PPN4163_2_preferred",
            "parameter": "alpha_i, xi, zeta_i",
            "private_packet_expectation": "zero under fixed domain/projector/frame and same Hilbert source",
            "needed_next": "derive preferred-frame/preferred-location/stress-nonconservation residual vector",
            "score_ready": "False",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            **common(),
            "readout_id": "PPN4163_3_Gdot",
            "parameter": "Gdot/G",
            "private_packet_expectation": "zero under fixed kappa_* / topological kappa branch",
            "needed_next": "link to kappa superselection rows and clock/orbital constraints",
            "score_ready": "False",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
    ]


def firewall_rows() -> List[dict]:
    return [
        {
            **common(),
            "firewall_id": "FW4163_0_claims_register",
            "rule": f"{CLAIM_ID} status must remain private_nonclaim_public_claim_false",
            "status": "ACTIVE",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            **common(),
            "firewall_id": "FW4163_1_spine",
            "rule": "main spine section must include public_claim=false and fallback epsilon_kernel bound",
            "status": "ACTIVE",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            **common(),
            "firewall_id": "FW4163_2_next",
            "rule": "next work must be PPN/readout gate or explicit bound inputs before any stronger claim",
            "status": "ACTIVE",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
    ]


def status_rows(claim_action: str, spine_action: str) -> List[dict]:
    return [
        {
            **common(),
            "result": DECISION,
            "claim_register_synced": "True",
            "claim_register_action": claim_action,
            "main_spine_synced": "True",
            "main_spine_action": spine_action,
            "claim_row_public_claim_false": "True",
            "PPC4161_spine_marker_present": "True",
            "local_PPN_readout_gate_built": "False",
            "public_local_gr_claimed": "False",
            "global_MTS_claimed": "False",
            "next_target": "4164-Y5-R2FR-PPC4161-local-PPN-readout-gate.md",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
    ]


def next_rows() -> List[dict]:
    return [
        {
            **common(),
            "next_id": "NEXT4163_0",
            "target_doc": "4164-Y5-R2FR-PPC4161-local-PPN-readout-gate.md",
            "target_script": "scripts/Y5_R2FR_4164_PPC4161_local_PPN_readout_gate.py",
            "objective": "build the local PPN/readout gate for PPC4161 covering gamma, beta, alpha_i, xi, zeta_i, Gdot/G, and fallback residual components",
            "success_gate": "PPN readout rows either derive the GR values under PPC4161 or emit explicit residual/bound inputs; no public local-GR claim is made",
            "reason": "4163 syncs the formal spine and claim register; the next proof obligation is the actual local PPN/readout gate.",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
    ]


def write_doc(claim_action: str, spine_action: str, outputs: Dict[str, Path]) -> None:
    text = f"""# 4163 - Formal Spine Claim Register Sync Or Local PPN Readout Gate

Timestamp UTC: `{TIMESTAMP}`  
Branch: `{BRANCH_ID}`  
Decision: `{DECISION}`

## Purpose
4162 created `180-PPC4161-private-local-packet-integration.md`, but the main spine and claims register did not yet point at it.

4163 syncs the formal indexes while preserving `public_claim=false`.

## Claims Register Sync
`{CLAIMS_PATH}` now contains:

`{CLAIM_ID}: PPC4161 is a scoped private local parent-packet branch for first-order Newton source normalization`.

Status is:

`private_nonclaim_public_claim_false`.

## Main Spine Sync
`{SPINE_PATH}` now contains marker:

`{SPINE_MARKER}`.

The spine section points to:

- `180-PPC4161-private-local-packet-integration.md`;
- claim row `{CLAIM_ID}`;
- the private result `delta J_H_total = 0 and PPC4161 => a_hom = 0`;
- the fallback `epsilon_kernel <= epsilon_Pi_inner + epsilon_hidden_inner + epsilon_surface_mismatch`.

## Nonclaim Guard
This checkpoint does **not** build the full PPN/readout gate. It only syncs the formal indexes.

The next required local proof gate is:

`4164-Y5-R2FR-PPC4161-local-PPN-readout-gate.md`.

## Outputs
- `{outputs["P8_Y5_R2FR_4163_SOURCE_REGISTER"]}`
- `{outputs["P8_Y5_R2FR_4163_FORMAL_SYNC_MAP"]}`
- `{outputs["P8_Y5_R2FR_4163_CLAIMS_REGISTER_AUDIT"]}`
- `{outputs["P8_Y5_R2FR_4163_SPINE_SECTION_AUDIT"]}`
- `{outputs["P8_Y5_R2FR_4163_LOCAL_PPN_READOUT_HANDOFF"]}`
- `{outputs["P8_Y5_R2FR_4163_CLAIM_FIREWALL"]}`
- `{outputs["P8_Y5_R2FR_4163_STATUS"]}`
- `{outputs["P8_Y5_R2FR_4163_NEXT_TARGET"]}`
"""
    DOC_PATH.write_text(text, encoding="utf-8")


def write_outputs() -> Tuple[Dict[str, Path], str, str]:
    claim_action = ensure_claim_row()
    spine_action = ensure_spine_section()
    outputs = output_paths()
    write_csv(outputs["P8_Y5_R2FR_4163_SOURCE_REGISTER"], source_rows())
    write_csv(outputs["P8_Y5_R2FR_4163_FORMAL_SYNC_MAP"], sync_map_rows(claim_action, spine_action))
    write_csv(outputs["P8_Y5_R2FR_4163_CLAIMS_REGISTER_AUDIT"], claims_audit_rows())
    write_csv(outputs["P8_Y5_R2FR_4163_SPINE_SECTION_AUDIT"], spine_audit_rows())
    write_csv(outputs["P8_Y5_R2FR_4163_LOCAL_PPN_READOUT_HANDOFF"], ppn_handoff_rows())
    write_csv(outputs["P8_Y5_R2FR_4163_CLAIM_FIREWALL"], firewall_rows())
    write_csv(outputs["P8_Y5_R2FR_4163_STATUS"], status_rows(claim_action, spine_action))
    write_csv(outputs["P8_Y5_R2FR_4163_NEXT_TARGET"], next_rows())
    write_doc(claim_action, spine_action, outputs)
    return outputs, claim_action, spine_action


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
        "VAL4163_0_sources",
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
    add("VAL4163_1_csv_parse", "all generated CSV outputs parse and are nonempty", csv_ok, ", ".join(csv_detail))

    claims = parse_csv(CLAIMS_PATH)
    claim_rows = [row for row in claims if row.get("claim_id") == CLAIM_ID]
    claim_row_ok = (
        len(claim_rows) == 1
        and claim_rows[0].get("status") == "private_nonclaim_public_claim_false"
        and "public_claim=false" in claim_rows[0].get("current_evidence", "")
    )
    add("VAL4163_2_claim_row", f"claims register contains one {CLAIM_ID} private nonclaim row", claim_row_ok, str(claim_rows))

    spine_text = read_text(SPINE_PATH)
    spine_tokens = [SPINE_MARKER, "public_claim = false", "180-PPC4161-private-local-packet-integration.md", "epsilon_kernel <= epsilon_Pi_inner + epsilon_hidden_inner + epsilon_surface_mismatch", "4164-Y5-R2FR-PPC4161-local-PPN-readout-gate.md"]
    add("VAL4163_3_spine_section", "main spine contains PPC4161 sync marker, public_claim=false, fallback and next target", all(token in spine_text for token in spine_tokens), "spine tokens checked")

    doc_text = read_text(DOC_PATH) if DOC_PATH.exists() else ""
    doc_tokens = [DECISION, CLAIM_ID, SPINE_MARKER, "private_nonclaim_public_claim_false", "4164-Y5-R2FR-PPC4161-local-PPN-readout-gate.md"]
    add("VAL4163_4_doc_tokens", "checkpoint doc records synced claim, marker, nonclaim status and next target", all(token in doc_text for token in doc_tokens), "doc tokens checked")

    handoff_text = "\n".join(",".join(row.values()) for row in parse_csv(outputs["P8_Y5_R2FR_4163_LOCAL_PPN_READOUT_HANDOFF"]))
    handoff_tokens = ["gamma", "beta", "alpha_i, xi, zeta_i", "Gdot/G"]
    add("VAL4163_5_ppn_handoff", "PPN handoff covers gamma, beta, preferred-frame/location/stress and Gdot", all(token in handoff_text for token in handoff_tokens), "handoff tokens checked")

    firewall_text = "\n".join(",".join(row.values()) for row in parse_csv(outputs["P8_Y5_R2FR_4163_CLAIM_FIREWALL"]))
    firewall_tokens = ["private_nonclaim_public_claim_false", "public_claim=false", "PPN/readout gate"]
    add("VAL4163_6_firewall", "firewall rows preserve nonclaim status and next proof gate", all(token in firewall_text for token in firewall_tokens), "firewall tokens checked")

    status = parse_csv(outputs["P8_Y5_R2FR_4163_STATUS"])
    status_ok = (
        len(status) == 1
        and status[0].get("result") == DECISION
        and status[0].get("claim_register_synced") == "True"
        and status[0].get("main_spine_synced") == "True"
        and status[0].get("claim_row_public_claim_false") == "True"
        and status[0].get("PPC4161_spine_marker_present") == "True"
        and status[0].get("local_PPN_readout_gate_built") == "False"
        and status[0].get("public_local_gr_claimed") == "False"
        and status[0].get("global_MTS_claimed") == "False"
    )
    add("VAL4163_7_status", "status records synced claims/spine and no public/global/local-GR claim", status_ok, str(status))

    next_target = parse_csv(outputs["P8_Y5_R2FR_4163_NEXT_TARGET"])
    next_ok = len(next_target) == 1 and next_target[0].get("target_doc") == "4164-Y5-R2FR-PPC4161-local-PPN-readout-gate.md"
    add("VAL4163_8_next", "next target is PPC4161 local PPN readout gate", next_ok, str(next_target))

    all_rows: List[dict] = []
    for path in outputs.values():
        all_rows.extend(parse_csv(path))
    no_claim = all(row.get("claim_allowed") in ("False", "") and row.get("valid_for_claim") in ("False", "") for row in all_rows)
    no_score = all(row.get("score_ready", "False") in ("False", "") for row in all_rows)
    add("VAL4163_9_no_claim", "all generated rows remain nonclaim and no score-ready row", no_claim and no_score, f"row_count={len(all_rows)}")

    output_paths_all = list(outputs.values()) + [DOC_PATH, CLAIMS_PATH, SPINE_PATH]
    in_scope = all(is_under(path, ROOT) or is_under(path, FORMALIZATION) for path in output_paths_all)
    formal_allowed = {CLAIMS_PATH.resolve(), SPINE_PATH.resolve()}
    formal_outputs = {path.resolve() for path in output_paths_all if is_under(path, FORMALIZATION)}
    add("VAL4163_10_scope", "formal edits are limited to claims register and main spine", in_scope and formal_outputs == formal_allowed, f"formal_outputs={[str(p) for p in formal_outputs]}")

    compile_ok = True
    compile_detail = "py_compile ok"
    try:
        py_compile.compile(str(SCRIPT_PATH), doraise=True)
    except Exception as exc:
        compile_ok = False
        compile_detail = repr(exc)
    add("VAL4163_11_compile", "generator script compiles", compile_ok, compile_detail)
    return checks


def main() -> None:
    outputs, claim_action, spine_action = write_outputs()
    validation_rows = validate(outputs)
    validation_path = SOURCE_DIR / "P8_Y5_BRR545_4163_VALIDATION.csv"
    write_csv(validation_path, validation_rows)
    pycache = SCRIPT_PATH.parent / "__pycache__"
    if pycache.exists():
        shutil.rmtree(pycache)

    failed = [row for row in validation_rows if row["passed"] != "True"]
    print(f"claims_action: {claim_action}")
    print(f"spine_action: {spine_action}")
    print(f"wrote: {DOC_PATH}")
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

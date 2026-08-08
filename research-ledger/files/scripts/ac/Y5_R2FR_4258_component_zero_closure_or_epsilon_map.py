from __future__ import annotations

import csv
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List


ROOT = Path(__file__).resolve().parents[2]
FORMAL = ROOT / "formalization-workbench"
POST = ROOT / "post-checkpoint-work"
SOURCE_DIR = POST / "source-intake" / "mts_residuals"

CHECKPOINT = "4258"
CLAIM_ID = "L-099"
BRANCH = "MTS_R2FR_Y5_COMPONENT_ZERO_CLOSURE_OR_EPSILON_MAP_4258"
DECISION = "EIGHT_COMPONENT_ZERO_ATTEMPT_GEOMETRY_MATURED_OTHERS_BLOCKED_EPSILON_MAP_WRITTEN_NONCLAIM"
MARKER = "PPC4161_COMPONENT_ZERO_CLOSURE_OR_EPSILON_MAP_4258"
PACKET_MARKER = "PPC4161_PACKET_COMPONENT_ZERO_CLOSURE_OR_EPSILON_MAP_4258"
NEXT_TARGET = "4259-Y5-R2FR-attack-EM-Hodge-or-tau-reference-component-zero.md"

FORMAL_PATH = FORMAL / "274-PPC4161-component-zero-closure-or-epsilon-map.md"
DOC_PATH = POST / "4258-Y5-R2FR-component-zero-closure-or-epsilon-map.md"
VALIDATION_PATH = SOURCE_DIR / "P8_Y5_BRR545_4258_VALIDATION.csv"

LOCAL_COMPONENT_CANDIDATE_PATH = SOURCE_DIR / "P8_Y5_R2FR_4258_DQ_COMPONENT_VALUES_CANDIDATE.csv"
COMPONENT_CANDIDATE_4254_PATH = SOURCE_DIR / "P8_Y5_R2FR_4254_DQ_COMPONENT_VALUES_CANDIDATE.csv"

PROBE_ORDER = (
    "Dq_geom",
    "Dq_tau",
    "Dq_matter",
    "Dq_source_readout",
    "Dq_theta_marker",
    "Dq_boundary_projector",
    "Dq_EM",
    "Dq_coeff",
)
COMPONENT_TO_PROBE = {f"{probe}[H_L]": probe for probe in PROBE_ORDER}
CANDIDATE_ID = "DQ_COORDINATE_SEMINORM_SMOKE_4255"

STAMP = datetime.now(timezone.utc).replace(microsecond=0).isoformat()


@dataclass(frozen=True)
class SourceSpec:
    source_id: str
    path: Path
    required_text: str
    role: str


SOURCE_SPECS: Dict[str, SourceSpec] = {
    "SRC4258_00_4244_matrix": SourceSpec(
        "SRC4258_00_4244_matrix",
        SOURCE_DIR / "P8_Y5_R2FR_4244_DQ_COMPONENT_ADOPTION_MATRIX.csv",
        "MISSING_HL_EM_HODGE_CONSTITUTIVE_ZERO",
        "4244 component-by-component adoption matrix.",
    ),
    "SRC4258_01_4245_live_rows": SourceSpec(
        "SRC4258_01_4245_live_rows",
        FORMAL / "261-PPC4161-HL-qbasic-strip-and-Dq-bound-first-input-row.md",
        "Dq_coeff[Hperp]",
        "4245 live Dq_i[Hperp] rows.",
    ),
    "SRC4258_02_4246_geometry": SourceSpec(
        "SRC4258_02_4246_geometry",
        SOURCE_DIR / "P8_Y5_R2FR_4246_GEOMETRY_ZERO_GATES.csv",
        "missing_no_shadow_certificate",
        "4246 geometry zero gate shows the precise blocker.",
    ),
    "SRC4258_03_4247_noshadow": SourceSpec(
        "SRC4258_03_4247_noshadow",
        SOURCE_DIR / "P8_Y5_R2FR_4247_NO_SHADOW_SIGNATURE_AUDIT.csv",
        "fail_current_corpus",
        "4247 rejects current-corpus no-shadow adoption.",
    ),
    "SRC4258_04_4247_epsilon": SourceSpec(
        "SRC4258_04_4247_epsilon",
        SOURCE_DIR / "P8_Y5_R2FR_4247_EPSILON_GEOM_NUMERIC_FILL_CONTRACT.csv",
        "epsilon_geom",
        "4247 five-piece geometry epsilon fill contract.",
    ),
    "SRC4258_05_4257_gap": SourceSpec(
        "SRC4258_05_4257_gap",
        FORMAL / "273-PPC4161-projector-certificate-and-spectral-gap-runner.md",
        "Dq_geom[Hperp]",
        "4257 establishes the parallel matrix-gap route.",
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
    fieldnames: List[str] = []
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
            "4258 attempts the eight Dq_i[Hperp] zero route. It finds Dq_geom has the most mature route "
            "through the five-piece epsilon_geom envelope, while the other seven components remain blocked "
            "at explicit H_L argument certificates. It writes a nonclaim per-component epsilon map."
        ),
        "current_evidence": (
            "4258 source register, descent-zero theorem, component closure audit, 4254 component candidate "
            "map, decision and firewall."
        ),
        "status": "private_component_zero_attempt_epsilon_map_ready_nonclaim",
        "next_test": (
            "Attack Dq_EM via Maxwell-Hodge/Poynting ownership or Dq_tau via reference-time collar, then "
            "promote any true zero into the component candidate file."
        ),
        "key_risk": "Treating conditional selector theorems for v as if they already apply to H_L or Hperp.",
    }
    with path.open("a", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writerow(row)


def source_rows() -> List[Dict[str, str]]:
    rows: List[Dict[str, str]] = []
    for spec in SOURCE_SPECS.values():
        text = read_text(spec.path)
        rows.append(
            {
                **common(),
                "source_id": spec.source_id,
                "path": str(spec.path),
                "exists": str(spec.path.exists()),
                "required_text": spec.required_text,
                "required_text_found": str(spec.required_text in text),
                "role": spec.role,
                "valid_for_claim": "False",
            }
        )
    return rows


def theorem_rows() -> List[Dict[str, str]]:
    raw = [
        (
            "CZ4258_0_descent_zero",
            "component descent-zero lemma",
            "For each component readout R_i, if R_i=Rbar_i(q) on U_good and Hperp has no q-independent representative shadow for that readout, then Dq_i[Hperp]=0.",
            "DERIVED_CONDITIONAL",
            "Needs the H_L/Hperp argument certificate for each component.",
        ),
        (
            "CZ4258_1_all_zero_collapse",
            "all-component collapse",
            "If every Dq_i[Hperp]=0, then E_Dq,Hperp=0 and the Dq-coordinate source-probe branch gives no Hperp source residual.",
            "DERIVED_CONDITIONAL",
            "Depends on all eight component zero certificates, not just geometry.",
        ),
        (
            "CZ4258_2_geometry_L1",
            "geometry fallback envelope",
            "Current geometry route gives epsilon_geom <= epsilon_Oloc + epsilon_coframe + epsilon_projector + epsilon_wall + epsilon_Hodge_geom.",
            "SOURCE_BACKED_BOUND_FORM",
            "This is the mature first component map but remains nonnumeric.",
        ),
        (
            "CZ4258_3_no_cancellation",
            "no-cancellation rule",
            "No component epsilon may be set to zero by cancellation between missing subpieces; each subpiece must be theorem-zero or source-bounded.",
            "NO_SMUGGLE_GUARD",
            "Keeps 4254 valid_for_claim=false until real rows exist.",
        ),
    ]
    return [
        {
            **common(),
            "theorem_id": theorem_id,
            "name": name,
            "statement": statement,
            "status": status,
            "guard": guard,
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
        for theorem_id, name, statement, status, guard in raw
    ]


def component_audit_rows() -> List[Dict[str, str]]:
    adoption = csv_rows(SOURCE_DIR / "P8_Y5_R2FR_4244_DQ_COMPONENT_ADOPTION_MATRIX.csv")
    by_probe = {COMPONENT_TO_PROBE.get(row.get("component", ""), ""): row for row in adoption}
    rows: List[Dict[str, str]] = []
    for probe in PROBE_ORDER:
        adoption_row = by_probe.get(probe, {})
        if probe == "Dq_geom":
            status = "BLOCKED_BY_A_MF_NO_SHADOW_OR_FIVE_PIECE_PROFILE"
            epsilon = "MISSING_EPSILON_GEOM_L1_COMPONENT_VALUES"
            route = "epsilon_geom_L1 = epsilon_Oloc + epsilon_coframe + epsilon_projector + epsilon_wall + epsilon_Hodge_geom"
            best_next = "parent-sign A_MF/no-shadow or fill five geometry epsilon subpieces"
            source = "4246 geometry gates;4247 no-shadow audit;4247 epsilon contract"
        else:
            status = adoption_row.get("HL_argument_status", f"MISSING_HL_ARGUMENT_{probe}")
            epsilon = f"MISSING_ZERO_PROOF_OR_PROFILE_{probe}"
            route = adoption_row.get("HL_argument_gate", "missing component argument gate")
            best_next = adoption_row.get("residual_if_unsigned", f"fill epsilon for {probe}")
            source = adoption_row.get("selector_source_ids", "4244 adoption matrix")
        rows.append(
            {
                **common(),
                "probe_id": probe,
                "zero_status": status,
                "epsilon_symbol": adoption_row.get("bound_symbol", f"epsilon_{probe.replace('Dq_', '')}"),
                "epsilon_placeholder": epsilon,
                "route_or_gate": route,
                "best_next_action": best_next,
                "source_basis": source,
                "zero_claim_allowed": "False",
                "valid_for_claim": "False",
            }
        )
    return rows


def component_candidate_rows(component_audit: List[Dict[str, str]]) -> List[Dict[str, str]]:
    rows: List[Dict[str, str]] = []
    by_probe = {row["probe_id"]: row for row in component_audit}
    for probe in PROBE_ORDER:
        audit = by_probe[probe]
        rows.append(
            {
                **common(),
                "candidate_id": CANDIDATE_ID,
                "probe_id": probe,
                "weight": "1.0",
                "epsilon": audit["epsilon_placeholder"],
                "epsilon_C1": f"MISSING_C1_ZERO_PROOF_OR_PROFILE_{probe}",
                "source_path": str(FORMAL_PATH),
                "valid_for_claim": "False",
            }
        )
    return rows


def decision_rows() -> List[Dict[str, str]]:
    raw = [
        (
            "DEC4258_0_geometry_first",
            "Dq_geom is the nearest component to a real fill because it already has a five-piece epsilon envelope.",
            "It is still blocked by A_MF/no-shadow or numeric profile pieces, not by vague coupling language.",
            "Attack epsilon_coframe/epsilon_Oloc or parent-sign A_MF/no-shadow.",
        ),
        (
            "DEC4258_1_EM_or_tau_next",
            "The best next non-geometry attack is Dq_EM or Dq_tau.",
            "EM has Maxwell-Hodge/Poynting ownership sources; tau has reference/collar sources. Both are more structured than arbitrary coefficients.",
            NEXT_TARGET,
        ),
        (
            "DEC4258_2_4254_feed",
            "4254 now receives a per-component epsilon placeholder map rather than generic missing rows.",
            "The downstream gate remains blocked, but the blocker is more actionable.",
            "Rerun 4254 after any component zero or numeric profile is promoted.",
        ),
    ]
    return [
        {
            **common(),
            "decision_id": decision_id,
            "decision": decision,
            "reason": reason,
            "next_action": next_action,
            "valid_for_claim": "False",
        }
        for decision_id, decision, reason, next_action in raw
    ]


def firewall_rows() -> List[Dict[str, str]]:
    raw = [
        ("FW4258_0_selector_v", "using selector zero theorems for v as if they automatically apply to H_L/Hperp", "H_L_ARGUMENT_CERTIFICATE_REQUIRED"),
        ("FW4258_1_geom", "setting epsilon_geom=0 without A_MF/no-shadow or all five geometry subpieces", "GEOMETRY_SUBPIECES_REQUIRED"),
        ("FW4258_2_EM", "adding Poynting as an extra hidden force after Maxwell-Hodge stress is already counted", "MAXWELL_HODGE_OWNER_GUARD_REQUIRED"),
        ("FW4258_3_all_zero", "claiming E_Dq,Hperp=0 from fewer than eight component zeros", "ALL_EIGHT_COMPONENTS_REQUIRED"),
    ]
    return [
        {
            **common(),
            "firewall_id": firewall_id,
            "forbidden_move": forbidden,
            "required_gate": gate,
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
        for firewall_id, forbidden, gate in raw
    ]


def status_rows() -> List[Dict[str, str]]:
    return [
        {
            **common(),
            "status_id": "STATUS4258_0",
            "summary": (
                "4258 attempts the component-zero path and finds one mature geometry envelope plus seven "
                "explicit H_L argument certificate debts. It feeds 4254 with a sharper nonclaim epsilon map."
            ),
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
    ]


def next_target_rows() -> List[Dict[str, str]]:
    return [
        {
            **common(),
            "next_target": NEXT_TARGET,
            "objective": (
                "Try Dq_EM through Maxwell-Hodge/Poynting ownership or Dq_tau through reference-time collar "
                "descent; promote only theorem-zero or source-backed epsilon rows."
            ),
            "avoid": "Do not promote conditional selector clauses for generic v to Hperp without the H_L argument certificate.",
            "valid_for_claim": "False",
        }
    ]


def formal_doc() -> str:
    return f"""
# 274 - PPC4161 component-zero closure or epsilon map

Marker: `{MARKER}`

Branch: `{BRANCH}`

Decision: `{DECISION}`

## Private nonclaim

4258 does not prove `E_Dq,Hperp=0`, local GR, PPN safety, R10 safety, clock safety, orbital safety, or EM closure. It attempts the direct eight-component zero route and writes the sharper epsilon map needed by 4254.

## General component-zero lemma

For a component readout `R_i`, if:

```text
R_i = Rbar_i(q) on U_good,
Hperp has no q-independent representative shadow for R_i,
```

then:

```text
Dq_i[Hperp] = 0.
```

If all eight components close, then:

```text
E_Dq,Hperp = 0.
```

## Current component verdict

Geometry is the most mature route:

```text
epsilon_geom
<= epsilon_Oloc
 + epsilon_coframe
 + epsilon_projector
 + epsilon_wall
 + epsilon_Hodge_geom.
```

But current 4246/4247 evidence blocks the zero at:

```text
A_MF/no-shadow for Hperp,
same observed coframe parent ownership,
five geometry epsilon subpieces.
```

The other seven components remain blocked at their explicit 4244 `H_L` argument certificates:

```text
Dq_tau, Dq_matter, Dq_source_readout, Dq_theta_marker,
Dq_boundary_projector, Dq_EM, Dq_coeff.
```

## 4254 feed

4258 writes:

```text
P8_Y5_R2FR_4254_DQ_COMPONENT_VALUES_CANDIDATE.csv
```

with per-component placeholders. This is still invalid for claim, but the missing rows are now named by physics route rather than generic absence.

## Next target

`{NEXT_TARGET}` should attack either `Dq_EM` through Maxwell-Hodge/Poynting ownership, or `Dq_tau` through the reference-time/collar descent route.
"""


def checkpoint_doc() -> str:
    return f"""
# 4258 - Y5 R2FR component-zero closure or epsilon map

Packet marker: `{PACKET_MARKER}`

## Result

4258 tried the eight-component zero route. No component is claim-closed, but the first component map is now sharper:

```text
Dq_geom -> epsilon_geom_L1 five-piece envelope.
```

The other seven components inherit explicit 4244 `H_L` argument gates rather than vague missingness.

## Downstream feed

The 4254 component candidate file has been replaced with per-component nonclaim placeholders. Rerunning 4254 should still block, but for named physical reasons.
"""


def validation_rows(paths: Dict[str, Path]) -> List[Dict[str, str]]:
    sources = csv_rows(paths["sources"])
    audit = csv_rows(paths["audit"])
    candidates = csv_rows(paths["candidates"])
    theorems = csv_rows(paths["theorems"])
    rows = [
        ("VAL4258_0_sources_exist", all(row["exists"] == "True" for row in sources), "all source paths exist"),
        ("VAL4258_1_needles_found", all(row["required_text_found"] == "True" for row in sources), "all source needles found"),
        ("VAL4258_2_eight_components", len(audit) == 8, "eight component audit rows emitted"),
        ("VAL4258_3_geom_matured", any(row["probe_id"] == "Dq_geom" and "EPSILON_GEOM" in row["epsilon_placeholder"] for row in audit), "geometry epsilon route named"),
        ("VAL4258_4_4254_candidate_written", COMPONENT_CANDIDATE_4254_PATH.exists(), "4254 component candidate path written"),
        ("VAL4258_5_candidate_nonclaim", len(candidates) == 8 and all(row["valid_for_claim"] == "False" for row in candidates), "candidate rows nonclaim"),
        ("VAL4258_6_no_fake_zeros", all(row["epsilon"].startswith("MISSING_") for row in candidates), "no epsilon zero fabricated"),
        ("VAL4258_7_descent_lemma", any(row["theorem_id"] == "CZ4258_0_descent_zero" for row in theorems), "descent-zero lemma emitted"),
        ("VAL4258_8_claim_row", CLAIM_ID in read_text(FORMAL / "02-claims-register.csv"), "claim register row added"),
        ("VAL4258_9_formal_doc", MARKER in read_text(FORMAL_PATH), "formal marker present"),
        ("VAL4258_10_checkpoint_doc", PACKET_MARKER in read_text(DOC_PATH), "checkpoint marker present"),
    ]
    return [
        {
            **common(),
            "check_id": check_id,
            "description": description,
            "passed": str(bool(passed)),
            "evidence": "generated_artifacts",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
        for check_id, passed, description in rows
    ]


def main() -> None:
    SOURCE_DIR.mkdir(parents=True, exist_ok=True)
    source_path = SOURCE_DIR / "P8_Y5_R2FR_4258_SOURCE_REGISTER.csv"
    theorem_path = SOURCE_DIR / "P8_Y5_R2FR_4258_COMPONENT_ZERO_THEOREMS.csv"
    audit_path = SOURCE_DIR / "P8_Y5_R2FR_4258_COMPONENT_ZERO_CLOSURE_AUDIT.csv"
    decision_path = SOURCE_DIR / "P8_Y5_R2FR_4258_DECISION.csv"
    firewall_path = SOURCE_DIR / "P8_Y5_R2FR_4258_CLAIM_FIREWALL.csv"
    status_path = SOURCE_DIR / "P8_Y5_R2FR_4258_STATUS.csv"
    next_path = SOURCE_DIR / "P8_Y5_R2FR_4258_NEXT_TARGET.csv"

    audit = component_audit_rows()
    candidates = component_candidate_rows(audit)

    write_csv(source_path, source_rows())
    write_csv(theorem_path, theorem_rows())
    write_csv(audit_path, audit)
    write_csv(LOCAL_COMPONENT_CANDIDATE_PATH, candidates)
    write_csv(COMPONENT_CANDIDATE_4254_PATH, candidates)
    write_csv(decision_path, decision_rows())
    write_csv(firewall_path, firewall_rows())
    write_csv(status_path, status_rows())
    write_csv(next_path, next_target_rows())
    write_text(FORMAL_PATH, formal_doc())
    write_text(DOC_PATH, checkpoint_doc())
    append_claim()

    paths = {
        "sources": source_path,
        "theorems": theorem_path,
        "audit": audit_path,
        "candidates": LOCAL_COMPONENT_CANDIDATE_PATH,
    }
    validation = validation_rows(paths)
    write_csv(VALIDATION_PATH, validation)
    failed = [row for row in validation if row["passed"] != "True"]
    print(f"{CHECKPOINT}: wrote 10 csv artifacts")
    print(f"{CHECKPOINT}: validation rows={len(validation)} failed={len(failed)}")
    print(f"{CHECKPOINT}: decision={DECISION}")


if __name__ == "__main__":
    main()

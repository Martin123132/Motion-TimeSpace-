from __future__ import annotations

import csv
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, Iterable, List


ROOT = Path(__file__).resolve().parents[2]
FORMAL = ROOT / "formalization-workbench"
POST = ROOT / "post-checkpoint-work"
SOURCE_DIR = POST / "source-intake" / "mts_residuals"

CHECKPOINT = "4242"
CLAIM_ID = "L-083"
BRANCH = "MTS_R2FR_Y5_M2_DEFECT_SOURCE_MAP_PRUNING_4242"
DECISION = "M2_TRANSPORT_BGRAD_DEFECTS_CONDITIONALLY_ROUTED_NOT_PARENT_DERIVED_HPERP_REMAINS_LIVE_SOURCE_ROW_NONCLAIM"
MARKER = "PPC4161_M2_DEFECT_SOURCE_MAP_PRUNING_4242"
PACKET_MARKER = "PPC4161_PACKET_M2_DEFECT_SOURCE_MAP_PRUNING_4242"
NEXT_TARGET = "4243-Y5-R2FR-Hperp-zero-theorem-or-source-defect-profile-first-real-row.md"

FORMAL_PATH = FORMAL / "258-PPC4161-M2-defect-source-map-pruning-or-real-profile-input-pack.md"
DOC_PATH = POST / "4242-Y5-R2FR-M2-defect-source-map-pruning-or-real-profile-input-pack.md"
VALIDATION_PATH = SOURCE_DIR / "P8_Y5_BRR545_4242_VALIDATION.csv"


@dataclass(frozen=True)
class SourceSpec:
    source_id: str
    path: Path
    required_text: str
    role: str


STAMP = datetime.now(timezone.utc).replace(microsecond=0).isoformat()


SOURCE_SPECS: Dict[str, SourceSpec] = {
    "SRC4242_00_4241_next": SourceSpec(
        "SRC4242_00_4241_next",
        SOURCE_DIR / "P8_Y5_R2FR_4241_NEXT_TARGET.csv",
        "4242-Y5-R2FR-M2-defect-source-map-pruning-or-real-profile-input-pack.md",
        "4241 selected defect source-map pruning or real profile input pack.",
    ),
    "SRC4242_01_4241_formal": SourceSpec(
        "SRC4242_01_4241_formal",
        FORMAL / "257-PPC4161-real-Hperp-M2-profile-input-or-M2-quotient-constant-proof.md",
        "M_2 = M2_pruned_safe + M2_defect.",
        "4241 M2 defect split.",
    ),
    "SRC4242_02_4241_components": SourceSpec(
        "SRC4242_02_4241_components",
        SOURCE_DIR / "P8_Y5_R2FR_4241_M2_COMPONENT_AUDIT.csv",
        "H_transport",
        "Machine-readable open defect components.",
    ),
    "SRC4242_03_routing_projectors": SourceSpec(
        "SRC4242_03_routing_projectors",
        FORMAL / "48-routing-projector-definitions.md",
        "P_loc + P_gal + P_cos = 1",
        "Routing projector identity.",
    ),
    "SRC4242_04_transport_route": SourceSpec(
        "SRC4242_04_transport_route",
        FORMAL / "48-routing-projector-definitions.md",
        "static laboratories and vacuum transition shells do not.",
        "Transport eligibility excludes static local/vacuum collars.",
    ),
    "SRC4242_05_gradient_route": SourceSpec(
        "SRC4242_05_gradient_route",
        FORMAL / "48-routing-projector-definitions.md",
        "homogeneous cosmology and smooth local vacuum shells do not route to chi.",
        "Baryonic-gradient transport routing caveat.",
    ),
    "SRC4242_06_projector_status": SourceSpec(
        "SRC4242_06_projector_status",
        FORMAL / "48-routing-projector-definitions.md",
        "projector_functions_defined_not_derived",
        "Projectors are not parent-derived yet.",
    ),
    "SRC4242_07_no_flux": SourceSpec(
        "SRC4242_07_no_flux",
        FORMAL / "192-PPC4161-local-boundary-no-flux-sector-interface-theorem.md",
        "J_tr^nu = 0 through <=2PN.",
        "Compact no-flux local selector.",
    ),
    "SRC4242_08_transition_routing": SourceSpec(
        "SRC4242_08_transition_routing",
        FORMAL / "93-transition-routing-law.md",
        "sector-label routing fails;",
        "Routing must be conservation-owned, not sector-label bookkeeping.",
    ),
    "SRC4242_09_transition_local_fail": SourceSpec(
        "SRC4242_09_transition_local_fail",
        FORMAL / "92-solar-transition-current-ppn-gate.md",
        "the transition shell is explicitly failed as a local metric source;",
        "Transition shell cannot be hidden as local metric source.",
    ),
    "SRC4242_10_claim_register": SourceSpec(
        "SRC4242_10_claim_register",
        FORMAL / "02-claims-register.csv",
        "L-082",
        "Prior claim-register anchor for 4241.",
    ),
}


def common() -> Dict[str, str]:
    return {"timestamp_utc": STAMP, "branch_id": BRANCH, "checkpoint_id": CHECKPOINT}


def read_text(path: Path) -> str:
    if not path.exists():
        return ""
    return path.read_text(encoding="utf-8", errors="replace")


def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text.strip() + "\n", encoding="utf-8")


def write_csv(path: Path, rows: List[Dict[str, str]]) -> None:
    if not rows:
        raise ValueError(f"empty csv: {path}")
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
    with path.open("r", newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def append_once(path: Path, marker: str, block: str) -> None:
    existing = read_text(path)
    if marker in existing:
        return
    with path.open("a", encoding="utf-8") as handle:
        if existing and not existing.endswith("\n"):
            handle.write("\n")
        handle.write("\n" + block.strip() + "\n")


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
                "claim_allowed": "False",
                "valid_for_claim": "False",
            }
        )
    return rows


def pruning_matrix_rows() -> List[Dict[str, str]]:
    rows = [
        (
            "PM4242_0_transport",
            "M2_defect_transport",
            "conditional_route_to_Pgal_or_chi",
            "If transport eligibility is owned by P_gal/chi and P_loc transport pullback is zero, it is not a compact local scalar source.",
            "projector_defined_not_parent_derived",
        ),
        (
            "PM4242_1_Bgrad",
            "M2_defect_Bgrad",
            "conditional_route_to_transition_boundary_or_quarantine",
            "Smooth local vacuum collars do not route to chi, but transition shells remain dangerous and need quarantine/boundary routing.",
            "transition_profile_or_routing_needed",
        ),
        (
            "PM4242_2_Hperp",
            "Hperp_source_defect",
            "live_local_source_row",
            "No routing theorem removes non-q source leakage; source contraction remains S_A Hperp^A.",
            "open",
        ),
        (
            "PM4242_3_projectors",
            "P_loc/P_gal/P_cos",
            "defined_not_derived",
            "Projectors sum to one and avoid sector labels, but are not parent-derived.",
            "open_public",
        ),
        (
            "PM4242_4_no_flux",
            "compact_no_flux_collar",
            "private_selector_pass",
            "No-flux same-source collar supports local pruning, but does not prove global transition/galaxtic routing.",
            "private_only",
        ),
    ]
    return [
        {
            **common(),
            "prune_id": prune_id,
            "defect": defect,
            "route": route,
            "meaning": meaning,
            "status": status,
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
        for prune_id, defect, route, meaning, status in rows
    ]


def residual_budget_rows() -> List[Dict[str, str]]:
    rows = [
        (
            "RB4242_0_full_defect",
            "A_J,eff_private <= |S_A Hperp^A| + |D_m Delta_h M2_defect| + |D_t M2_defect|",
            "imported reduced defect budget",
            "active_nonclaim",
        ),
        (
            "RB4242_1_routed_defect",
            "A_J,eff_private <= |S_A Hperp^A| + |R_transport_to_local| + |R_Bgrad_to_local|",
            "after conditional routing, transport/Bgrad only enter through explicit local leakage residuals",
            "conditional_private",
        ),
        (
            "RB4242_2_best_case",
            "R_transport_to_local=R_Bgrad_to_local=0 => A_J,eff_private <= |S_A Hperp^A|",
            "best current non-smuggled reduction",
            "not_claimed",
        ),
        (
            "RB4242_3_exact_zero",
            "Hperp=0 and routed residuals zero => A_J,eff_private=0 at leading order",
            "remaining exact-zero path",
            "not_claimed",
        ),
    ]
    return [
        {
            **common(),
            "budget_id": budget_id,
            "formula": formula,
            "meaning": meaning,
            "status": status,
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
        for budget_id, formula, meaning, status in rows
    ]


def routing_gate_rows() -> List[Dict[str, str]]:
    rows = [
        ("RG4242_0_sum", "P_loc + P_gal + P_cos = 1", "private_candidate_pass", "accounting identity exists"),
        ("RG4242_1_no_sector_labels", "routing from invariants, not labels", "private_candidate_pass", "48 defines invariant candidate functions"),
        ("RG4242_2_projector_derivation", "derive projectors from parent coarse-grained source decomposition", "open", "explicitly not derived"),
        ("RG4242_3_transport_local_pullback", "P_loc H_transport = 0 in compact static/vacuum local collar", "conditional", "needs projector ownership and local support conditions"),
        ("RG4242_4_Bgrad_quarantine", "Bgrad transition support is boundary/routed, not local metric source", "conditional", "transition shell direct local source fails and must be quarantined"),
        ("RG4242_5_Hperp", "Hperp=0 or S_A Hperp=0", "open", "remaining live source row"),
    ]
    return [
        {
            **common(),
            "gate_id": gate_id,
            "gate": gate,
            "status": status,
            "evidence_or_need": evidence_or_need,
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
        for gate_id, gate, status, evidence_or_need in rows
    ]


def real_input_pack_rows() -> List[Dict[str, str]]:
    rows = [
        ("RI4242_0_Hperp", "Hperp^A(x,t)", "live local source defect", "MISSING_PARENT_PROFILE"),
        ("RI4242_1_SA", "S_A(x,t)", "source-current Jacobian for Hperp", "MISSING_SOURCE_JACOBIAN"),
        ("RI4242_2_Rtransport", "R_transport_to_local", "local leakage from transport routing failure", "MISSING_PROJECTOR_RESIDUAL"),
        ("RI4242_3_RBgrad", "R_Bgrad_to_local", "local leakage from transition/Bgrad routing failure", "MISSING_TRANSITION_PROFILE"),
        ("RI4242_4_projectors", "P_loc/P_gal/P_cos real profiles", "routing proof or bounded residuals", "MISSING_PARENT_PROJECTOR"),
        ("RI4242_5_budget", "(mu_Xi T_res)/|c_Gamma|", "local cGamma budget owner", "MISSING_TIMESCALE_COUPLING"),
        ("RI4242_6_arena", "alpha3/Gdot/gradient arena projection", "score reduced residuals", "MISSING_ARENA_PROJECTION"),
    ]
    return [
        {
            **common(),
            "input_id": input_id,
            "quantity": quantity,
            "role": role,
            "status": status,
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
        for input_id, quantity, role, status in rows
    ]


def decision_rows() -> List[Dict[str, str]]:
    return [
        {
            **common(),
            "decision": DECISION,
            "forward_move": "Transport and Bgrad M2 defects are conditionally routed/pruned into explicit local residual rows; Hperp remains the live local source defect.",
            "transport_Bgrad_pruned_as_claim": "False",
            "scoreable_now": "False",
            "best_next_move": NEXT_TARGET,
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
    ]


def firewall_rows() -> List[Dict[str, str]]:
    rows = [
        ("FW4242_0_no_routing_claim", "Do not claim transport/Bgrad are gone until parent projectors and support clauses are derived.", "active"),
        ("FW4242_1_no_sector_labels", "Routing must be invariant/conservation-owned, not a sector-name switch.", "active"),
        ("FW4242_2_transition_not_local", "Transition-shell/Bgrad residuals cannot be hidden as local metric source; they need routing or explicit bounds.", "active"),
        ("FW4242_3_Hperp_live", "Hperp remains the live local source row until zeroed or profiled.", "active"),
        ("FW4242_4_nonclaim_inputs", "Real input pack rows are missing and invalid for claim.", "active"),
    ]
    return [
        {
            **common(),
            "firewall_id": firewall_id,
            "rule": rule,
            "status": status,
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
        for firewall_id, rule, status in rows
    ]


def status_rows() -> List[Dict[str, str]]:
    return [
        {
            **common(),
            "status": "private_conditional_routing_pruning_nonclaim",
            "summary": "4242 conditionally routes transport/Bgrad defect pieces out of the compact local scalar source only as explicit residual rows; Hperp remains live.",
            "scoreable_now": "False",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
    ]


def next_target_rows() -> List[Dict[str, str]]:
    return [
        {
            **common(),
            "next_target": NEXT_TARGET,
            "reason": "After routing-pruning, the cleanest remaining local source row is Hperp; next prove Hperp zero or source the first real Hperp/S_A profile row.",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
    ]


def all_generated_groups() -> Iterable[List[Dict[str, str]]]:
    return (
        source_rows(),
        pruning_matrix_rows(),
        residual_budget_rows(),
        routing_gate_rows(),
        real_input_pack_rows(),
        decision_rows(),
        firewall_rows(),
        status_rows(),
        next_target_rows(),
    )


def formal_doc() -> str:
    return f"""
# 258 - PPC4161 M2 defect source-map pruning or real profile input pack

Marker: `{MARKER}`

Branch: `{BRANCH}`
Decision: `{DECISION}`

## Result

4242 partially prunes the `M2_defect` problem without pretending the projectors are parent-derived.

The transport and Bgrad pieces are not accepted as direct compact-local scalar sources. They are routed into explicit residuals:

```text
R_transport_to_local,
R_Bgrad_to_local.
```

So the reduced private budget becomes:

```text
A_J,eff_private
  <= |S_A Hperp^A| + |R_transport_to_local| + |R_Bgrad_to_local|.
```

Best case:

```text
R_transport_to_local = R_Bgrad_to_local = 0
```

leaves:

```text
A_J,eff_private <= |S_A Hperp^A|.
```

## What Is Conditional

The routing/pruning is not a public theorem because:

```text
P_loc/P_gal/P_cos are defined but not parent-derived,
transport routing to chi is candidate-level,
Bgrad transition support needs boundary/quarantine treatment,
Hperp is not zeroed.
```

## Current Live Source Row

The clean remaining target is:

```text
S_A Hperp^A.
```

## Next Target

`{NEXT_TARGET}`
"""


def checkpoint_doc() -> str:
    return f"""
# 4242 - M2 defect source-map pruning or real profile input pack

**Status:** `{DECISION}`.

## Forward Move

Transport and Bgrad defects are conditionally routed into explicit residual rows:

```text
R_transport_to_local,
R_Bgrad_to_local.
```

The live local source target is now:

```text
S_A Hperp^A.
```

## Still Missing

Projectors are not parent-derived, routing residuals are not sourced, and `Hperp` is not zeroed.

## Next

`{NEXT_TARGET}`
"""


def update_claim_register() -> None:
    path = FORMAL / "02-claims-register.csv"
    rows = csv_rows(path)
    if any(row.get("claim_id") == CLAIM_ID for row in rows):
        return
    rows.append(
        {
            "claim_id": CLAIM_ID,
            "domain": "local_gr",
            "claim": "4242 conditionally routes transport and Bgrad M2 defects into explicit local residual rows, leaving Hperp as the live local source target. This is private nonclaim because routing projectors are defined but not parent-derived.",
            "current_evidence": "4242 source register, pruning matrix, residual budget, routing gates, real input pack, decision and firewall.",
            "status": "private_conditional_routing_pruning_nonclaim",
            "next_test": "Prove Hperp=0 / S_A Hperp=0 or source the first real Hperp and S_A profile rows.",
            "key_risk": "Treating candidate routing projectors as parent-derived would hide local source residuals.",
        }
    )
    with path.open("w", newline="", encoding="utf-8") as handle:
        fieldnames = ["claim_id", "domain", "claim", "current_evidence", "status", "next_test", "key_risk"]
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def update_spine_and_packet() -> None:
    spine_block = f"""
## PPC4161 M2 defect source-map pruning

Marker: `{MARKER}`

4242 conditionally routes transport and Bgrad pieces into explicit local residual rows:

```text
R_transport_to_local,
R_Bgrad_to_local.
```

The live cGamma source target is now:

```text
S_A Hperp^A.
```

No public claim follows because the projectors remain defined-not-derived.
"""
    packet_block = f"""
## Packet Update - M2 defect source-map pruning

Marker: `{PACKET_MARKER}`

Transport/Bgrad no longer float as vague scalar-source amplitudes. They are either routed by parent-owned projectors or scored as explicit local residuals. `Hperp` remains the next pressure point.
"""
    append_once(FORMAL / "07-unification-spine.md", MARKER, spine_block)
    append_once(FORMAL / "180-PPC4161-private-local-packet-integration.md", PACKET_MARKER, packet_block)


def validation_rows() -> List[Dict[str, str]]:
    rows: List[Dict[str, str]] = []

    def add(check_id: str, description: str, passed: bool, evidence: str) -> None:
        rows.append(
            {
                **common(),
                "check_id": check_id,
                "description": description,
                "passed": str(bool(passed)),
                "evidence": evidence,
                "claim_allowed": "False",
                "valid_for_claim": "False",
            }
        )

    sources = source_rows()
    pruning = pruning_matrix_rows()
    budget = residual_budget_rows()
    gates = routing_gate_rows()
    inputs = real_input_pack_rows()
    all_rows = [row for group in all_generated_groups() for row in group]

    add("VAL4242_0_sources_exist", "all source paths exist", all(row["exists"] == "True" for row in sources), "source register")
    add("VAL4242_1_needles_found", "all source needles found", all(row["required_text_found"] == "True" for row in sources), "source register")
    add("VAL4242_2_transport_routed", "transport defect routed conditionally", any(row["defect"] == "M2_defect_transport" and "conditional" in row["route"] for row in pruning), "pruning matrix")
    add("VAL4242_3_Bgrad_routed", "Bgrad defect routed conditionally", any(row["defect"] == "M2_defect_Bgrad" and "conditional" in row["route"] for row in pruning), "pruning matrix")
    add("VAL4242_4_Hperp_live", "Hperp remains live", any(row["defect"] == "Hperp_source_defect" and row["status"] == "open" for row in pruning), "pruning matrix")
    add("VAL4242_5_reduced_budget", "residual budget includes Hperp and routing residuals", any("R_transport_to_local" in row["formula"] and "Hperp" in row["formula"] for row in budget), "residual budget")
    add("VAL4242_6_projector_open", "projector derivation remains open", any(row["gate_id"] == "RG4242_2_projector_derivation" and row["status"] == "open" for row in gates), "routing gates")
    add("VAL4242_7_input_pack", "real input pack has Hperp, routing residuals and projectors", {"Hperp^A(x,t)", "R_transport_to_local", "R_Bgrad_to_local", "P_loc/P_gal/P_cos real profiles"}.issubset({row["quantity"] for row in inputs}), "input pack")
    add("VAL4242_8_decision_nonclaim", "decision keeps scoreable false", decision_rows()[0]["scoreable_now"] == "False", "decision")
    add("VAL4242_9_docs_written", "formal and checkpoint docs exist", FORMAL_PATH.exists() and DOC_PATH.exists(), f"{FORMAL_PATH}; {DOC_PATH}")
    add("VAL4242_10_claim_register", "claims register contains L-083", CLAIM_ID in read_text(FORMAL / "02-claims-register.csv"), str(FORMAL / "02-claims-register.csv"))
    add("VAL4242_11_spine_marker", "spine contains marker", MARKER in read_text(FORMAL / "07-unification-spine.md"), str(FORMAL / "07-unification-spine.md"))
    add("VAL4242_12_packet_marker", "packet contains marker", PACKET_MARKER in read_text(FORMAL / "180-PPC4161-private-local-packet-integration.md"), str(FORMAL / "180-PPC4161-private-local-packet-integration.md"))
    add("VAL4242_13_no_claim_flags", "no generated row is valid for claim", all(row.get("valid_for_claim") != "True" for row in all_rows), "all generated groups")
    add("VAL4242_14_next_target", "next target selected", next_target_rows()[0]["next_target"] == NEXT_TARGET, NEXT_TARGET)
    return rows


def main() -> None:
    paths = {
        "source": SOURCE_DIR / "P8_Y5_R2FR_4242_SOURCE_REGISTER.csv",
        "pruning": SOURCE_DIR / "P8_Y5_R2FR_4242_M2_DEFECT_PRUNING_MATRIX.csv",
        "budget": SOURCE_DIR / "P8_Y5_R2FR_4242_RESIDUAL_BUDGET.csv",
        "gates": SOURCE_DIR / "P8_Y5_R2FR_4242_ROUTING_GATES.csv",
        "inputs": SOURCE_DIR / "P8_Y5_R2FR_4242_REAL_INPUT_PACK.csv",
        "decision": SOURCE_DIR / "P8_Y5_R2FR_4242_DECISION.csv",
        "firewall": SOURCE_DIR / "P8_Y5_R2FR_4242_CLAIM_FIREWALL.csv",
        "status": SOURCE_DIR / "P8_Y5_R2FR_4242_STATUS.csv",
        "next": SOURCE_DIR / "P8_Y5_R2FR_4242_NEXT_TARGET.csv",
    }
    write_text(FORMAL_PATH, formal_doc())
    write_text(DOC_PATH, checkpoint_doc())
    write_csv(paths["source"], source_rows())
    write_csv(paths["pruning"], pruning_matrix_rows())
    write_csv(paths["budget"], residual_budget_rows())
    write_csv(paths["gates"], routing_gate_rows())
    write_csv(paths["inputs"], real_input_pack_rows())
    write_csv(paths["decision"], decision_rows())
    write_csv(paths["firewall"], firewall_rows())
    write_csv(paths["status"], status_rows())
    write_csv(paths["next"], next_target_rows())
    update_claim_register()
    update_spine_and_packet()
    write_csv(VALIDATION_PATH, validation_rows())
    failed_rows = [row for row in csv_rows(VALIDATION_PATH) if row["passed"] != "True"]
    print(f"Decision: {DECISION}")
    print(f"Formal: {FORMAL_PATH}")
    print(f"Checkpoint: {DOC_PATH}")
    print(f"Validation: {VALIDATION_PATH}")
    print(f"Validation rows: {len(csv_rows(VALIDATION_PATH))}; failed: {len(failed_rows)}")
    if failed_rows:
        for failed_row in failed_rows:
            print(f"FAILED {failed_row['check_id']}: {failed_row['evidence']}")
        raise SystemExit(1)


if __name__ == "__main__":
    main()

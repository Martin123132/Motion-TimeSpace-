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

CHECKPOINT = "4246"
CLAIM_ID = "L-087"
BRANCH = "MTS_R2FR_Y5_HPERP_GEOMETRY_GATE_EPSILON_GEOM_PROFILE_4246"
DECISION = "HPERP_GEOMETRY_ZERO_NOT_PARENT_SIGNED_EPSILON_GEOM_DECOMPOSED_PROFILE_ROW_REQUIRED_NONCLAIM"
MARKER = "PPC4161_HPERP_GEOMETRY_GATE_EPSILON_GEOM_PROFILE_4246"
PACKET_MARKER = "PPC4161_PACKET_HPERP_GEOMETRY_GATE_EPSILON_GEOM_PROFILE_4246"
NEXT_TARGET = "4247-Y5-R2FR-motion-frame-no-shadow-signature-or-epsilon-geom-numeric-fill.md"

FORMAL_PATH = FORMAL / "262-PPC4161-Hperp-geometry-zero-certificate-or-epsilon-geom-profile-fill.md"
DOC_PATH = POST / "4246-Y5-R2FR-Hperp-geometry-zero-certificate-or-epsilon-geom-profile-fill.md"
VALIDATION_PATH = SOURCE_DIR / "P8_Y5_BRR545_4246_VALIDATION.csv"


@dataclass(frozen=True)
class SourceSpec:
    source_id: str
    path: Path
    required_text: str
    role: str


STAMP = datetime.now(timezone.utc).replace(microsecond=0).isoformat()


SOURCE_SPECS: Dict[str, SourceSpec] = {
    "SRC4246_00_4245_next": SourceSpec(
        "SRC4246_00_4245_next",
        SOURCE_DIR / "P8_Y5_R2FR_4245_NEXT_TARGET.csv",
        "4246-Y5-R2FR-Hperp-geometry-zero-certificate-or-epsilon-geom-profile-fill.md",
        "4245 selected the Hperp geometry zero/profile target.",
    ),
    "SRC4246_01_4245_formal": SourceSpec(
        "SRC4246_01_4245_formal",
        FORMAL / "261-PPC4161-HL-qbasic-strip-and-Dq-bound-first-input-row.md",
        "epsilon_geom >= ||Dq_geom[Hperp]||",
        "4245 first geometry component-bound row.",
    ),
    "SRC4246_02_4245_first_row": SourceSpec(
        "SRC4246_02_4245_first_row",
        SOURCE_DIR / "P8_Y5_R2FR_4245_FIRST_DQ_BOUND_INPUT_ROW.csv",
        "epsilon_geom",
        "4245 machine-readable epsilon_geom row.",
    ),
    "SRC4246_03_projector_clause": SourceSpec(
        "SRC4246_03_projector_clause",
        FORMAL / "230-PPC4161-projector-stress-curl-zero-or-bound.md",
        "P_loc=P_bar(q)",
        "Observed geometry/projector zero clause.",
    ),
    "SRC4246_04_projector_bound": SourceSpec(
        "SRC4246_04_projector_bound",
        FORMAL / "230-PPC4161-projector-stress-curl-zero-or-bound.md",
        "|R_P_metric|",
        "Observed geometry/projector fallback bound.",
    ),
    "SRC4246_05_projector_wall": SourceSpec(
        "SRC4246_05_projector_wall",
        FORMAL / "230-PPC4161-projector-stress-curl-zero-or-bound.md",
        "|R_wall|",
        "Selector wall fallback residual.",
    ),
    "SRC4246_06_hodge_readout": SourceSpec(
        "SRC4246_06_hodge_readout",
        FORMAL / "230-PPC4161-projector-stress-curl-zero-or-bound.md",
        "|R_Hodge_readout|",
        "Geometry/Hodge readout fallback residual.",
    ),
    "SRC4246_07_EH_origin": SourceSpec(
        "SRC4246_07_EH_origin",
        FORMAL / "197-PPC4161-EH-local-metric-principal-block-origin-gate.md",
        "current_MTS_EH_derivation = false",
        "EH/local observed metric origin is still conditional.",
    ),
    "SRC4246_08_motion_frame": SourceSpec(
        "SRC4246_08_motion_frame",
        FORMAL / "198-PPC4161-motion-frame-symmetry-parent-signature-gate.md",
        "A_MF_PARENT_SIGNATURE_NOT_FOUND",
        "Motion-frame symmetry/no-shadow signature missing.",
    ),
    "SRC4246_09_qnatural": SourceSpec(
        "SRC4246_09_qnatural",
        FORMAL / "193-PPC4161-quotient-naturality-vertical-silence-theorem.md",
        "D O_loc[v] = D Obar_loc[Dq[v]] = 0.",
        "Quotient-natural observable descent theorem.",
    ),
    "SRC4246_10_4245_component": SourceSpec(
        "SRC4246_10_4245_component",
        SOURCE_DIR / "P8_Y5_R2FR_4245_DQ_COMPONENT_REDUCTION_MATRIX.csv",
        "Dq_geom[Hperp]",
        "4245 Hperp-only geometry component reduction.",
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
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def append_once(path: Path, marker: str, block: str) -> None:
    current = read_text(path)
    if marker in current:
        return
    write_text(path, current.rstrip() + "\n\n" + block.strip())


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


def geometry_zero_gate_rows() -> List[Dict[str, str]]:
    gates = [
        (
            "GZG4246_0_Hq_stripped",
            "Dq_geom[H_L]=Dq_geom[Hperp]",
            "passed_private",
            "SRC4246_01_4245_formal;SRC4246_10_4245_component",
            "q-basic H_q piece is not part of geometry residual",
        ),
        (
            "GZG4246_1_projector_qbasic",
            "P_loc=P_bar(q) or fixed topological/readout label",
            "conditional_present",
            "SRC4246_03_projector_clause",
            "would remove projector motion if Hperp has no q-independent projector shadow",
        ),
        (
            "GZG4246_2_observed_coframe",
            "e_obs=e_bar(q) and g_obs descends through the observed coframe",
            "conditional_present",
            "SRC4246_03_projector_clause;SRC4246_07_EH_origin",
            "would remove coframe/metric leakage if parent motion-frame symmetry is signed",
        ),
        (
            "GZG4246_3_motion_frame_parent_owner",
            "A_MF parent-signs internal motion-frame labels as local gauge redundancies",
            "missing_parent_signature",
            "SRC4246_08_motion_frame",
            "without this, Hperp can be a representative geometry shadow",
        ),
        (
            "GZG4246_4_no_Hperp_shadow",
            "Hperp has no q-independent observed-geometry/coframe leg",
            "missing_no_shadow_certificate",
            "SRC4246_07_EH_origin;SRC4246_08_motion_frame",
            "this is the exact clause needed for Dq_geom[Hperp]=0",
        ),
        (
            "GZG4246_5_no_wall_Hodge",
            "no active selector wall and no hidden Hodge/readout deformation",
            "conditional_present_not_Hperp_signed",
            "SRC4246_04_projector_bound;SRC4246_05_projector_wall;SRC4246_06_hodge_readout",
            "failure routes to epsilon_wall and epsilon_Hodge_geom",
        ),
    ]
    return [
        {
            **common(),
            "gate_id": gate_id,
            "condition": condition,
            "status": status,
            "source_support": source_support,
            "effect": effect,
            "zero_claim_allowed": "False",
            "valid_for_claim": "False",
        }
        for gate_id, condition, status, source_support, effect in gates
    ]


def epsilon_geom_decomposition_rows() -> List[Dict[str, str]]:
    pieces = [
        (
            "epsilon_Oloc",
            "observed-local metric/readout variation from Hperp",
            "||D_Hperp O_loc|| or |R_P_metric| proxy",
            "SRC4246_04_projector_bound;SRC4246_09_qnatural",
            "MISSING_HPERP_OBSERVED_METRIC_PROFILE",
        ),
        (
            "epsilon_coframe",
            "same-frame/coframe variation from Hperp",
            "||D_Hperp e_obs||",
            "SRC4246_03_projector_clause;SRC4246_07_EH_origin;SRC4246_08_motion_frame",
            "MISSING_MOTION_FRAME_NO_SHADOW_SIGNATURE",
        ),
        (
            "epsilon_projector",
            "projector/domain stress geometry leakage",
            "|R_domain| + |R_denominator| + hidden projector terms",
            "SRC4246_03_projector_clause;SRC4246_04_projector_bound",
            "MISSING_PROJECTOR_DOMAIN_PROFILE",
        ),
        (
            "epsilon_wall",
            "selector wall or active boundary-projector geometry leakage",
            "|R_wall|",
            "SRC4246_05_projector_wall",
            "MISSING_NO_WALL_CERTIFICATE_OR_PROFILE",
        ),
        (
            "epsilon_Hodge_geom",
            "Hodge/readout geometry deformation not already counted as EM stress",
            "|R_Hodge_readout|",
            "SRC4246_06_hodge_readout",
            "MISSING_HODGE_GEOMETRY_READOUT_PROFILE",
        ),
    ]
    return [
        {
            **common(),
            "component": "Dq_geom[Hperp]",
            "quantity": quantity,
            "meaning": meaning,
            "bound_proxy": bound_proxy,
            "source_support": source_support,
            "current_status": current_status,
            "numeric_value": "MISSING",
            "units": "geometry_component_Dq_norm",
            "valid_for_claim": "False",
        }
        for quantity, meaning, bound_proxy, source_support, current_status in pieces
    ]


def epsilon_geom_profile_row() -> List[Dict[str, str]]:
    return [
        {
            **common(),
            "profile_id": "EGP4246_0_profile_row",
            "component": "Dq_geom[Hperp]",
            "quantity": "epsilon_geom",
            "formula": "epsilon_geom <= epsilon_Oloc + epsilon_coframe + epsilon_projector + epsilon_wall + epsilon_Hodge_geom",
            "zero_formula": "epsilon_Oloc=epsilon_coframe=epsilon_projector=epsilon_wall=epsilon_Hodge_geom=0 => Dq_geom[Hperp]=0",
            "required_profile_columns": "system_id;collar_id;Hperp_profile_id;norm_Dq_geom_Hperp;epsilon_Oloc;epsilon_coframe;epsilon_projector;epsilon_wall;epsilon_Hodge_geom;C_geom_norm;units;source_path;assumptions;valid_for_claim",
            "current_status": "decomposed_profile_row_ready_numeric_values_missing",
            "zero_claim_allowed": "False",
            "valid_for_claim": "False",
        }
    ]


def decision_rows() -> List[Dict[str, str]]:
    return [
        {
            **common(),
            "decision_id": "DEC4246",
            "decision": DECISION,
            "scoreable_now": "False",
            "zero_claim_allowed": "False",
            "reason": "The observed-geometry/coframe zero route needs a parent motion-frame/no-shadow signature for Hperp; current 197/198 sources keep that signature conditional or missing.",
            "selected_route": "Keep the derivation-first route alive by attacking A_MF/no-shadow next; otherwise fill epsilon_geom numerically from a local Hperp geometry profile.",
            "next_target": NEXT_TARGET,
            "valid_for_claim": "False",
        }
    ]


def firewall_rows() -> List[Dict[str, str]]:
    rules = [
        ("FW4246_0_no_zero_from_selector", "Projector/coframe selector clauses do not zero Hperp unless Hperp has no q-independent geometry shadow."),
        ("FW4246_1_no_EH_origin_claim", "The EH/local metric origin remains conditional; 4246 does not derive full local GR."),
        ("FW4246_2_no_A_MF_smuggling", "Do not assume the missing motion-frame parent signature A_MF."),
        ("FW4246_3_no_EM_double_count", "Hodge/readout geometry leakage must stay separate from ordinary Maxwell-Hodge EM stress."),
        ("FW4246_4_no_numeric_pass", "epsilon_geom is decomposed but numeric values are still missing."),
    ]
    return [
        {
            **common(),
            "firewall_id": firewall_id,
            "rule": rule,
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
        for firewall_id, rule in rules
    ]


def status_rows() -> List[Dict[str, str]]:
    return [
        {
            **common(),
            "status": DECISION,
            "summary": "4246 rejects an immediate Dq_geom[Hperp]=0 claim because the motion-frame/no-shadow parent signature is missing, but decomposes epsilon_geom into five named profile pieces.",
            "scoreable_now": "False",
            "valid_for_claim": "False",
        }
    ]


def next_target_rows() -> List[Dict[str, str]]:
    return [
        {
            **common(),
            "next_target": NEXT_TARGET,
            "task": "Try to parent-sign the motion-frame/no-shadow condition for Hperp; if that fails, fill epsilon_geom numerically using the decomposed profile columns.",
            "reason": "This is now the sharp fork for the geometry channel: derive A_MF/no-shadow or measure/bound the geometry leakage.",
            "valid_for_claim": "False",
        }
    ]


def all_generated_groups() -> List[List[Dict[str, str]]]:
    return [
        source_rows(),
        geometry_zero_gate_rows(),
        epsilon_geom_decomposition_rows(),
        epsilon_geom_profile_row(),
        decision_rows(),
        firewall_rows(),
        status_rows(),
        next_target_rows(),
    ]


def formal_doc() -> str:
    return f"""
# 262 - PPC4161 Hperp geometry zero certificate or epsilon_geom profile fill

Marker: `{MARKER}`

Branch: `{BRANCH}`

Decision: `{DECISION}`

## Claim Status

Private nonclaim. This does not prove `Dq_geom[Hperp]=0`, local GR, PPN safety, clock safety, R10 safety, or a derived EH parent action.

## Geometry Zero Route

From 4245:

```text
Dq_geom[H_L] = Dq_geom[Hperp].
```

The observed-geometry/coframe selector would give the exact zero only if:

```text
P_loc=P_bar(q),
e_obs=e_bar(q),
g_obs = eta_AB e^A e^B or equivalent observed coframe descends,
Hodge = Hodge[g_obs, orientation],
no active selector wall,
Hperp has no q-independent observed-geometry/coframe leg.
```

The last line is the hard one. Current 197/198 evidence keeps the EH/motion-frame origin conditional:

```text
current_MTS_EH_derivation = false,
A_MF_PARENT_SIGNATURE_NOT_FOUND.
```

Therefore 4246 rejects the immediate zero claim.

## Decomposed Bound

The retained geometry row is:

```text
epsilon_geom >= ||Dq_geom[Hperp]||.
```

Its decomposed no-cancellation envelope is:

```text
epsilon_geom
<= epsilon_Oloc
 + epsilon_coframe
 + epsilon_projector
 + epsilon_wall
 + epsilon_Hodge_geom.
```

Where:

```text
epsilon_Oloc        := observed local metric/readout variation from Hperp,
epsilon_coframe     := same-frame/coframe variation from Hperp,
epsilon_projector   := projector/domain/denominator geometry leakage,
epsilon_wall        := active selector-wall or boundary-projector leakage,
epsilon_Hodge_geom  := Hodge/readout geometry deformation not counted as EM stress.
```

The exact-zero route is still alive, but it now has a named parent-signature target:

```text
A_MF/no-shadow for Hperp
=> epsilon_Oloc=epsilon_coframe=epsilon_projector=epsilon_wall=epsilon_Hodge_geom=0
=> Dq_geom[Hperp]=0.
```

If that fails, the profile columns in `P8_Y5_R2FR_4246_EPSILON_GEOM_PROFILE_ROW.csv` are the next non-cheating empirical/bound route.

## Next Target

`{NEXT_TARGET}` should try to parent-sign the motion-frame/no-shadow condition for Hperp. If not, fill the decomposed `epsilon_geom` row numerically from a local Hperp geometry profile.
"""


def checkpoint_doc() -> str:
    return f"""
# 4246 - Hperp geometry zero certificate or epsilon_geom profile fill

**Status:** `{DECISION}`.

## Result

The geometry zero is not claimed. The reason is precise:

```text
A_MF_PARENT_SIGNATURE_NOT_FOUND
```

means `Hperp` could still carry a representative observed-geometry/coframe shadow.

## What improved

The live geometry residual is now decomposed:

```text
epsilon_geom
<= epsilon_Oloc
 + epsilon_coframe
 + epsilon_projector
 + epsilon_wall
 + epsilon_Hodge_geom.
```

This is the first proper profile row for the Hperp geometry channel.

## Next target

`{NEXT_TARGET}`
"""


def update_claim_register() -> None:
    path = FORMAL / "02-claims-register.csv"
    if CLAIM_ID in read_text(path):
        return
    row = {
        "claim_id": CLAIM_ID,
        "domain": "local_gr",
        "claim": "4246 attacks the first Hperp-only Dq component, Dq_geom[Hperp]. The immediate zero is rejected because the motion-frame/no-shadow parent signature remains missing, but epsilon_geom is decomposed into observed-readout, coframe, projector, wall, and Hodge-geometry pieces.",
        "current_evidence": "4246 source register, geometry zero gate, epsilon_geom decomposition, profile row, decision and firewall.",
        "status": "private_Hperp_geometry_gate_nonclaim",
        "next_test": "Parent-sign A_MF/no-shadow for Hperp, or fill epsilon_geom numerically from a local Hperp geometry profile.",
        "key_risk": "Treating conditional observed-coframe descent as Hperp no-shadow would smuggle the geometry zero and therefore local-GR safety.",
    }
    with path.open("a", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(row.keys()))
        writer.writerow(row)


def update_spine_and_packet() -> None:
    spine_block = f"""
## PPC4161 Hperp geometry gate

Marker: `{MARKER}`

4246 targets the first Hperp-only Dq component:

```text
epsilon_geom >= ||Dq_geom[Hperp]||.
```

The immediate zero is not claimed because the motion-frame/no-shadow parent signature is still missing. The retained decomposed profile is:

```text
epsilon_geom <= epsilon_Oloc + epsilon_coframe + epsilon_projector + epsilon_wall + epsilon_Hodge_geom.
```
"""
    packet_block = f"""
## Packet Update - Hperp geometry gate

Marker: `{PACKET_MARKER}`

The observed-geometry/coframe route has a sharp fork: parent-sign A_MF/no-shadow for Hperp, or fill the decomposed `epsilon_geom` profile row.
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
    gates = geometry_zero_gate_rows()
    pieces = epsilon_geom_decomposition_rows()
    profile = epsilon_geom_profile_row()
    all_rows = [row for group in all_generated_groups() for row in group]

    add("VAL4246_0_sources_exist", "all source paths exist", all(row["exists"] == "True" for row in sources), "source register")
    add("VAL4246_1_needles_found", "all source needles found", all(row["required_text_found"] == "True" for row in sources), "source register")
    add("VAL4246_2_missing_AMF", "motion-frame parent signature remains missing", any(row["gate_id"] == "GZG4246_3_motion_frame_parent_owner" and row["status"] == "missing_parent_signature" for row in gates), "geometry gates")
    add("VAL4246_3_no_shadow_missing", "Hperp no-shadow certificate remains missing", any(row["gate_id"] == "GZG4246_4_no_Hperp_shadow" and row["status"] == "missing_no_shadow_certificate" for row in gates), "geometry gates")
    add("VAL4246_4_zero_not_allowed", "zero claim is not allowed", all(row["zero_claim_allowed"] == "False" for row in gates), "geometry gates")
    add("VAL4246_5_five_pieces", "epsilon_geom has five decomposition pieces", len(pieces) == 5, "epsilon_geom decomposition")
    add("VAL4246_6_piece_names", "epsilon_geom decomposition includes expected pieces", {"epsilon_Oloc", "epsilon_coframe", "epsilon_projector", "epsilon_wall", "epsilon_Hodge_geom"}.issubset({row["quantity"] for row in pieces}), "epsilon_geom decomposition")
    add("VAL4246_7_profile_formula", "profile row has decomposed formula", "epsilon_Oloc" in profile[0]["formula"] and "epsilon_Hodge_geom" in profile[0]["formula"], "profile row")
    add("VAL4246_8_profile_columns", "profile row includes Hperp profile id and component pieces", "Hperp_profile_id" in profile[0]["required_profile_columns"] and "epsilon_wall" in profile[0]["required_profile_columns"], "profile row")
    add("VAL4246_9_decision_nonclaim", "decision keeps scoreable false", decision_rows()[0]["scoreable_now"] == "False", "decision")
    add("VAL4246_10_docs_written", "formal and checkpoint docs exist", FORMAL_PATH.exists() and DOC_PATH.exists(), f"{FORMAL_PATH}; {DOC_PATH}")
    add("VAL4246_11_claim_register", "claims register contains L-087", CLAIM_ID in read_text(FORMAL / "02-claims-register.csv"), str(FORMAL / "02-claims-register.csv"))
    add("VAL4246_12_spine_marker", "spine contains marker", MARKER in read_text(FORMAL / "07-unification-spine.md"), str(FORMAL / "07-unification-spine.md"))
    add("VAL4246_13_packet_marker", "packet contains marker", PACKET_MARKER in read_text(FORMAL / "180-PPC4161-private-local-packet-integration.md"), str(FORMAL / "180-PPC4161-private-local-packet-integration.md"))
    add("VAL4246_14_no_claim_flags", "no generated row is valid for claim", all(row.get("valid_for_claim") != "True" for row in all_rows), "all generated groups")
    add("VAL4246_15_next_target", "next target selected", next_target_rows()[0]["next_target"] == NEXT_TARGET, NEXT_TARGET)
    return rows


def main() -> None:
    paths = {
        "source": SOURCE_DIR / "P8_Y5_R2FR_4246_SOURCE_REGISTER.csv",
        "gates": SOURCE_DIR / "P8_Y5_R2FR_4246_GEOMETRY_ZERO_GATES.csv",
        "decomposition": SOURCE_DIR / "P8_Y5_R2FR_4246_EPSILON_GEOM_DECOMPOSITION.csv",
        "profile": SOURCE_DIR / "P8_Y5_R2FR_4246_EPSILON_GEOM_PROFILE_ROW.csv",
        "decision": SOURCE_DIR / "P8_Y5_R2FR_4246_DECISION.csv",
        "firewall": SOURCE_DIR / "P8_Y5_R2FR_4246_CLAIM_FIREWALL.csv",
        "status": SOURCE_DIR / "P8_Y5_R2FR_4246_STATUS.csv",
        "next": SOURCE_DIR / "P8_Y5_R2FR_4246_NEXT_TARGET.csv",
    }
    write_text(FORMAL_PATH, formal_doc())
    write_text(DOC_PATH, checkpoint_doc())
    write_csv(paths["source"], source_rows())
    write_csv(paths["gates"], geometry_zero_gate_rows())
    write_csv(paths["decomposition"], epsilon_geom_decomposition_rows())
    write_csv(paths["profile"], epsilon_geom_profile_row())
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
